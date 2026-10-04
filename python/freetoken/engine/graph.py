from __future__ import annotations

import gc
import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List

import torch
import torch.nn.functional as F
from freetoken.core import Batch, Req, get_global_ctx
from freetoken.distributed import get_tp_info
from freetoken.utils import init_logger, mem_GB
from freetoken.utils.progress import emit_progress
from tqdm import tqdm

if TYPE_CHECKING:
    from freetoken.attention import BaseAttnBackend
    from freetoken.models import BaseLLMModel
    from freetoken.moe.offload_cache import OffloadMoeCache

logger = init_logger(__name__)


def project_lm_head_all_positions(lm_head, hidden_states: torch.Tensor) -> torch.Tensor:
    """Project every hidden row through an LM head, bypassing prefill last-token slicing."""
    tied = getattr(lm_head, "tied_embedding", None)
    if tied is not None:
        logits = lm_head.tied_kernel.linear(hidden_states, tied.weight, lm_head.bias)
    elif getattr(lm_head, "quant_method", None) is not None:
        # the head's own kernel: a quantized (e.g. NVFP4) head stores packed weights
        logits = lm_head.quant_method.apply(lm_head, hidden_states)
    else:
        logits = F.linear(hidden_states, lm_head.weight, getattr(lm_head, "bias", None))
    tp_size = getattr(lm_head, "tp_size", 1)
    if tp_size == 1:
        return logits

    output_tensor = lm_head._comm.all_gather(logits)
    input_shape = logits.shape
    output_tensor = output_tensor.view((tp_size,) + input_shape)
    output_tensor = output_tensor.permute(1, 0, 2).contiguous()
    output_tensor = output_tensor.reshape(input_shape[:1] + (tp_size * input_shape[1],))
    return output_tensor[:, : lm_head.num_embeddings]


@dataclass
class GraphCaptureBuffer:
    input_ids: torch.Tensor
    out_loc: torch.Tensor
    positions: torch.Tensor
    # [3, bs] t/h/w rope positions; allocated only for mrope models (else None).
    mrope_positions: torch.Tensor | None
    logits: torch.Tensor
    hidden_states: list[torch.Tensor] | None
    table_idx: torch.Tensor  # per-request slot id for GatedDeltaNet state gather/scatter
    # Decode GDN query indptr = arange(bs+1); a constant per captured bs, filled once.
    fla_cu_seqlens: torch.Tensor
    fla_has_initial_state: torch.Tensor | None = None
    # DFlash verify on a GDN target: per-token conv states and recurrence inputs (FLAMetadata)
    dflash_conv_states: torch.Tensor | None = None
    dflash_gdn_mixed: torch.Tensor | None = None
    dflash_gdn_ab: torch.Tensor | None = None

    @classmethod
    def init(
        cls,
        bs: int,
        vocab_size: int,
        device: torch.device,
        mrope: bool = False,
        *,
        hidden_size: int | None = None,
        hidden_dtype: torch.dtype | None = None,
        num_hidden_layers: int = 0,
        linear_state_pool=None,
    ) -> GraphCaptureBuffer:
        hidden_states = None
        if num_hidden_layers > 0:
            assert hidden_size is not None
            assert hidden_dtype is not None
            hidden_states = [
                torch.empty(bs, hidden_size, dtype=hidden_dtype, device=device)
                for _ in range(num_hidden_layers)
            ]
        return GraphCaptureBuffer(
            input_ids=torch.zeros(bs, dtype=torch.int32, device=device),
            out_loc=torch.zeros(bs, dtype=torch.int32, device=device),
            positions=torch.zeros(bs, dtype=torch.int32, device=device),
            mrope_positions=(
                torch.zeros(3, bs, dtype=torch.int32, device=device) if mrope else None
            ),
            logits=torch.empty(bs, vocab_size, dtype=torch.float32, device=device),
            hidden_states=hidden_states,
            table_idx=torch.zeros(bs, dtype=torch.int32, device=device),
            fla_cu_seqlens=torch.arange(bs + 1, dtype=torch.int32, device=device),
        )

    @classmethod
    def init_dflash_verify(
        cls,
        verify_len: int,
        vocab_size: int,
        device: torch.device,
        *,
        hidden_size: int | None = None,
        hidden_dtype: torch.dtype | None = None,
        num_hidden_layers: int = 0,
        linear_state_pool=None,
        shared_storage: tuple[torch.Tensor, torch.Tensor] | None = None,
    ) -> GraphCaptureBuffer:
        buffer = cls.init(
            verify_len,
            vocab_size,
            device,
            hidden_size=hidden_size,
            hidden_dtype=hidden_dtype,
            num_hidden_layers=num_hidden_layers,
        )
        buffer.table_idx = torch.zeros(1, dtype=torch.int32, device=device)
        buffer.fla_cu_seqlens = torch.tensor([0, verify_len], dtype=torch.int32, device=device)
        buffer.fla_has_initial_state = torch.ones(1, dtype=torch.bool, device=device)
        if linear_state_pool is not None:
            # contiguous views of storage shared by every verify len (the graphs never run at
            # once), laid out [len, layers, ...] / [layers, len, ...] / [layers, 2, len, ...]
            if shared_storage is None:
                shared_storage = _alloc_dflash_verify_storage(
                    linear_state_pool, verify_len, hidden_dtype or torch.bfloat16, device)
            conv, rec = linear_state_pool.conv_states, linear_state_pool.recurrent_states
            layers, conv_dim, num_v = conv.shape[0], conv.shape[2], rec.shape[2]
            conv_shape = (verify_len, layers, conv_dim, conv.shape[3])
            mixed_shape = (layers, verify_len, conv_dim)
            ab_shape = (layers, 2, verify_len, num_v)
            conv_store, input_store = shared_storage
            buffer.dflash_conv_states = conv_store[: math.prod(conv_shape)].view(conv_shape)
            n_mixed = math.prod(mixed_shape)
            buffer.dflash_gdn_mixed = input_store[:n_mixed].view(mixed_shape)
            buffer.dflash_gdn_ab = input_store[n_mixed : n_mixed + math.prod(ab_shape)].view(ab_shape)
        return buffer

    def set_batch(self, batch: Batch) -> None:
        from freetoken.attention.linear import FLAMetadata

        _slice = slice(batch.padded_size)
        bs = batch.padded_size
        batch.input_ids = self.input_ids[_slice]
        batch.out_loc = self.out_loc[_slice]
        batch.positions = self.positions[_slice]
        if self.mrope_positions is not None:
            batch.mrope_positions = self.mrope_positions[:, _slice]
        batch.linear_table_idx = self.table_idx[_slice]
        # Decode GDN metadata reads the persistent cu_seqlens (constant arange) and the
        # persistent table_idx slot map, so the captured kernels see stable addresses.
        batch.fla_metadata = FLAMetadata(
            cu_seqlens=self.fla_cu_seqlens[: bs + 1], cache_indices=self.table_idx[_slice]
        )

    def copy_from(self, batch: Batch) -> None:
        _slice = slice(batch.padded_size)
        self.input_ids[_slice] = batch.input_ids
        if batch.out_loc is not None:
            self.out_loc[_slice] = batch.out_loc
        self.positions[_slice] = batch.positions
        if self.mrope_positions is not None:
            self.mrope_positions[:, _slice] = batch.mrope_positions
        if batch.linear_table_idx is not None:
            self.table_idx[_slice] = batch.linear_table_idx

    def copy_dflash_verify_from(self, batch: Batch, verify_len: int) -> None:
        self.input_ids[:verify_len] = batch.input_ids[:verify_len]
        if batch.out_loc is not None:
            self.out_loc[:verify_len] = batch.out_loc[:verify_len]
        self.positions[:verify_len] = batch.positions[:verify_len]
        if batch.linear_table_idx is not None:
            self.table_idx[:1] = batch.linear_table_idx[:1]

    def set_dflash_target_verify_batch(
        self,
        batch: Batch,
        verify_len: int,
        *,
        return_linear_snapshots: bool = False,
    ) -> None:
        from freetoken.attention.linear import FLAMetadata

        batch.input_ids = self.input_ids[:verify_len]
        batch.out_loc = self.out_loc[:verify_len]
        batch.positions = self.positions[:verify_len]
        batch.linear_table_idx = self.table_idx[:1]
        linear = return_linear_snapshots
        if linear and self.dflash_conv_states is None:
            raise RuntimeError("DFlash target verify graph requires linear snapshot buffers")
        batch.fla_metadata = FLAMetadata(
            cu_seqlens=self.fla_cu_seqlens[:2],
            cache_indices=self.table_idx[:1],
            has_initial_state=self.fla_has_initial_state,
            dflash_disable_state_update=linear,
            dflash_conv_states_buffer=self.dflash_conv_states if linear else None,
            dflash_gdn_mixed=self.dflash_gdn_mixed if linear else None,
            dflash_gdn_ab=self.dflash_gdn_ab if linear else None,
        )


def _determine_cuda_graph_bs(
    cuda_graph_bs: List[int] | None,
    cuda_graph_max_bs: int | None,
    free_memory: int,
) -> List[int]:
    if cuda_graph_bs is not None:
        return cuda_graph_bs

    free_memory_gb = free_memory / (1 << 30)
    if cuda_graph_max_bs is None:
        if free_memory_gb > 80:  # H200
            cuda_graph_max_bs = 256
        else:
            cuda_graph_max_bs = 160

    if cuda_graph_max_bs < 1:
        return []

    candidates = [1, 2, 4] + list(range(8, cuda_graph_max_bs + 1, 8))
    return [bs for bs in candidates if bs <= cuda_graph_max_bs]


def get_free_memory(device: torch.device) -> int:
    return torch.cuda.mem_get_info(device)[0]


def _dflash_target_verify_lens_within_budget(
    lens: List[int],
    linear_state_pool,
    budget_bytes: int,
    hidden_dtype: torch.dtype = torch.bfloat16,
) -> List[int]:
    """Keep the verify lens whose GDN commit buffers fit in ``budget_bytes``. All target-verify
    graphs share one buffer sized for the longest kept len (the graphs never run at once). A
    dropped len falls back to decode-loop verify at runtime, so this is a pure
    performance/robustness gate."""
    if linear_state_pool is None:
        return list(lens)
    per_token_bytes = dflash_verify_bytes_per_token(linear_state_pool, hidden_dtype)
    return [n for n in sorted(lens) if n * per_token_bytes <= budget_bytes]


def dflash_verify_bytes_per_token(linear_state_pool, hidden_dtype: torch.dtype) -> int:
    """Bytes a verified token keeps for the GDN commit: per linear layer, the conv state after
    it, its post-conv q/k/v and its a/b gates (the commit replays the recurrence from them)."""
    conv = linear_state_pool.conv_states        # [layers, slots, conv_dim, K-1]
    rec = linear_state_pool.recurrent_states    # [layers, slots, heads, K, V]
    layers, conv_dim, num_v = conv.shape[0], conv.shape[2], rec.shape[2]
    elem = torch.empty((), dtype=hidden_dtype).element_size()
    return conv[:, 0].numel() * conv.element_size() + layers * (conv_dim + 2 * num_v) * elem


def _alloc_dflash_verify_storage(linear_state_pool, verify_len: int, hidden_dtype, device):
    conv, rec = linear_state_pool.conv_states, linear_state_pool.recurrent_states
    layers, conv_dim, num_v = conv.shape[0], conv.shape[2], rec.shape[2]
    return (
        torch.empty(verify_len * conv[:, 0].numel(), dtype=conv.dtype, device=device),
        torch.empty(verify_len * layers * (conv_dim + 2 * num_v), dtype=hidden_dtype, device=device),
    )


class GraphRunner:
    def __init__(
        self,
        stream: torch.cuda.Stream,
        device: torch.device,
        model: BaseLLMModel,
        attn_backend: BaseAttnBackend,
        cuda_graph_bs: List[int] | None,
        cuda_graph_max_bs: int | None,
        free_memory: int,
        max_seq_len: int,
        vocab_size: int,
        dummy_req: Req,
        moe_offload_cache: OffloadMoeCache | None = None,
        mrope: bool = False,
        hidden_layer_ids: set[int] | None = None,
        hidden_size: int | None = None,
        hidden_dtype: torch.dtype | None = None,
        dflash_target_verify_lens: list[int] | None = None,
    ) -> None:
        cuda_graph_bs = _determine_cuda_graph_bs(
            cuda_graph_bs=cuda_graph_bs,
            cuda_graph_max_bs=cuda_graph_max_bs,
            free_memory=free_memory,
        )
        self.attn_backend = attn_backend
        self.max_graph_bs = max(cuda_graph_bs) if cuda_graph_bs else 0
        self.graph_bs_list = sorted(cuda_graph_bs)
        self.dummy_req = dummy_req
        self.moe_offload_cache = moe_offload_cache
        self.mrope = mrope
        self.stream = stream
        self.device = device
        self.hidden_layer_ids = set(hidden_layer_ids or [])
        self.hidden_size = hidden_size
        self.hidden_dtype = hidden_dtype
        self.dflash_target_verify_lens = sorted(set(dflash_target_verify_lens or []))
        # verify len -> plain decode time / verify time, for the adaptive gate's baseline
        self.dflash_plain_over_verify: Dict[int, float] = {}
        self._plain_decode_ms: float | None = None
        self._capture_graphs(max_seq_len, vocab_size, model)

    def _reset_moe_offload_cache(self) -> None:
        if self.moe_offload_cache is not None:
            self.moe_offload_cache.reset()

    def _capture_graphs(self, max_seq_len: int, vocab_size: int, model: BaseLLMModel):
        # Mark the post-weights "warmup" phase for /health: this stretch (graph capture — or the
        # remaining readiness work when graphs are disabled) moves no bytes, so without this the
        # loader would sit at 100% (last byte bar) until the ready ack. total=0 ⇒ the desktop
        # reads it as an indeterminate phase and animates the bar. Must precede the
        # graphs-disabled early return so that config gets the phase too.
        emit_progress("Capturing CUDA graphs / warming up", 0, 0)
        self.graph_map: Dict[int, torch.cuda.CUDAGraph] = {}
        self.dflash_target_verify_graph_map: Dict[int, torch.cuda.CUDAGraph] = {}
        self.dflash_target_verify_buffers: Dict[int, GraphCaptureBuffer] = {}
        if self.max_graph_bs == 0:
            return logger.info_rank0("CUDA graph is disabled.")

        self.attn_backend.init_capture_graph(max_seq_len=max_seq_len, bs_list=self.graph_bs_list)

        torch.cuda.synchronize(self.device)
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats(self.device)

        logger.info_rank0(f"Start capturing CUDA graphs with sizes: {self.graph_bs_list}")
        free_memory = get_free_memory(self.device)
        logger.info_rank0(f"Free GPU memory before capturing CUDA graphs: {mem_GB(free_memory)}")

        self.buffer = GraphCaptureBuffer.init(
            self.max_graph_bs,
            vocab_size,
            self.device,
            mrope=self.mrope,
            hidden_size=self.hidden_size,
            hidden_dtype=self.hidden_dtype,
            num_hidden_layers=len(self.hidden_layer_ids),
        )
        self._reset_moe_offload_cache()

        pbar = tqdm(
            sorted(self.graph_bs_list, reverse=True),
            desc="Preparing for capturing CUDA graphs...",
            unit="batch",
            disable=not get_tp_info().is_primary(),  # disable for non-primary ranks
        )
        pool = None
        for bs in pbar:
            free_memory = get_free_memory(self.device)
            pbar.desc = f"Capturing graphs: bs = {bs:<3} | avail_mem = {mem_GB(free_memory)}"
            pbar.refresh()
            graph = torch.cuda.CUDAGraph()
            batch = Batch(reqs=[self.dummy_req] * bs, phase="decode")
            batch.padded_reqs = batch.reqs
            self.attn_backend.prepare_for_capture(batch)
            self.buffer.set_batch(batch)
            # capture on the dummy linear-state slot so GatedDeltaNet gather/scatter
            # touches scratch (real slot indices are written by copy_from on replay). Hybrid-
            # radix decouples the GDN slot from table_idx -> use the GDN padding slot.
            dummy_slot = (self.dummy_req.linear_slot_idx
                          if self.dummy_req.linear_slot_idx is not None
                          else self.dummy_req.table_idx)
            self.buffer.table_idx[:bs].fill_(dummy_slot)
            with get_global_ctx().forward_batch(batch):
                self._run_model_into_buffer(model, bs)
                # Keep the offload cache warmed for capture. Resetting here forces
                # CUDA graph capture to replay cold-cache expert copies.
                with torch.cuda.graph(graph, pool=pool, stream=self.stream):
                    self._run_model_into_buffer(model, bs)
                self._reset_moe_offload_cache()
            if pool is None:
                pool = graph.pool()  # reuse cuda graph handle to reduce memory
            self.graph_map[bs] = graph

        self._reset_moe_offload_cache()
        free_memory = get_free_memory(self.device)
        logger.info_rank0(f"Free GPU memory after capturing CUDA graphs: {mem_GB(free_memory)}")
        if self.dflash_target_verify_lens and 1 in self.graph_map:
            # timed now, while the decode buffers still hold the bs=1 capture inputs
            self._plain_decode_ms = self._time_replay(self.graph_map[1])
        self._capture_dflash_target_verify_graphs(max_seq_len, vocab_size, model, pool)

    def _capture_dflash_target_verify_graphs(
        self,
        max_seq_len: int,
        vocab_size: int,
        model: BaseLLMModel,
        pool,
    ) -> None:
        if not self.dflash_target_verify_lens:
            return
        linear_state_pool = get_global_ctx().linear_state_pool
        shared_storage = None
        if linear_state_pool is not None:
            # the engine released the draft worker's reservation for this buffer just before
            budget = int(get_free_memory(self.device) * 0.9)
            kept = _dflash_target_verify_lens_within_budget(
                self.dflash_target_verify_lens, linear_state_pool, budget, self.hidden_dtype
            )
            if len(kept) < len(self.dflash_target_verify_lens):
                logger.warning_rank0(
                    "DFlash target verify graphs limited to lens "
                    f"{kept or '[]'} (snapshot memory budget); longer verifies "
                    "fall back to decode-loop verify."
                )
            self.dflash_target_verify_lens = kept
            if not kept:
                return
            shared_storage = _alloc_dflash_verify_storage(
                linear_state_pool, max(kept), self.hidden_dtype, self.device)
        init_verify = getattr(self.attn_backend, "init_dflash_target_verify_capture_graph", None)
        prepare_capture = getattr(self.attn_backend, "prepare_for_dflash_target_verify_capture", None)
        if init_verify is None or prepare_capture is None:
            logger.warning_rank0("DFlash target verify CUDA graph is disabled for this attention backend.")
            return

        init_verify(max_seq_len=max_seq_len, verify_lens=self.dflash_target_verify_lens)
        for verify_len in self.dflash_target_verify_lens:
            graph = torch.cuda.CUDAGraph()
            buffer = GraphCaptureBuffer.init_dflash_verify(
                verify_len,
                vocab_size,
                self.device,
                hidden_size=self.hidden_size,
                hidden_dtype=self.hidden_dtype,
                num_hidden_layers=len(self.hidden_layer_ids),
                linear_state_pool=linear_state_pool,
                shared_storage=shared_storage,
            )
            buffer.fla_cu_seqlens = torch.tensor(
                [0, verify_len], dtype=torch.int64, device=self.device
            )
            batch = Batch(reqs=[self.dummy_req], phase="decode")
            batch.padded_reqs = batch.reqs
            prepare_capture(batch, verify_len)
            buffer.set_dflash_target_verify_batch(
                batch,
                verify_len,
                return_linear_snapshots=linear_state_pool is not None,
            )
            buffer.input_ids.fill_(0)
            buffer.positions.copy_(torch.arange(verify_len, dtype=torch.int32, device=self.device))
            buffer.out_loc.fill_(0)
            dummy_slot = (self.dummy_req.linear_slot_idx
                          if self.dummy_req.linear_slot_idx is not None
                          else self.dummy_req.table_idx)
            buffer.table_idx.fill_(dummy_slot)
            with get_global_ctx().forward_batch(batch):
                self._run_dflash_target_verify_into_buffer(model, verify_len, buffer)
                with torch.cuda.graph(graph, pool=pool, stream=self.stream):
                    self._run_dflash_target_verify_into_buffer(model, verify_len, buffer)
                self._reset_moe_offload_cache()
            self.dflash_target_verify_graph_map[verify_len] = graph
            self.dflash_target_verify_buffers[verify_len] = buffer
            if self._plain_decode_ms is not None:
                verify_ms = self._time_replay(graph)
                if verify_ms > 0:
                    self.dflash_plain_over_verify[verify_len] = self._plain_decode_ms / verify_ms

        logger.info_rank0(
            f"DFlash target verify graphs captured for lens {self.dflash_target_verify_lens}"
        )
        if self.dflash_plain_over_verify:
            ratios = ", ".join(f"{n}: {r:.2f}" for n, r in self.dflash_plain_over_verify.items())
            logger.info_rank0(
                f"DFlash plain decode {self._plain_decode_ms:.2f} ms; plain/verify ratio by len {{{ratios}}}"
            )

    def _time_replay(self, graph: torch.cuda.CUDAGraph, iters: int = 10) -> float:
        """Median ms of a captured graph replayed on its own (dummy) capture inputs."""
        graph.replay()  # warm
        times = []
        for _ in range(iters):
            start = torch.cuda.Event(enable_timing=True)
            end = torch.cuda.Event(enable_timing=True)
            start.record(self.stream)
            graph.replay()
            end.record(self.stream)
            end.synchronize()
            times.append(start.elapsed_time(end))
        self._reset_moe_offload_cache()
        return sorted(times)[len(times) // 2]
    def _run_model_into_buffer(
        self,
        model: BaseLLMModel,
        bs: int,
        buffer: GraphCaptureBuffer | None = None,
        offset: int = 0,
    ) -> None:
        if buffer is None:
            buffer = self.buffer
        if self.hidden_layer_ids:
            logits, hidden_states = model.forward(return_hidden_layers=self.hidden_layer_ids)
            assert buffer.hidden_states is not None
            assert len(hidden_states) == len(buffer.hidden_states)
            buffer.logits[offset : offset + bs].copy_(logits[:bs])
            for dst, src in zip(buffer.hidden_states, hidden_states):
                dst[offset : offset + bs].copy_(src[:bs])
            return
        buffer.logits[offset : offset + bs].copy_(model.forward()[:bs])

    def _run_dflash_target_verify_into_buffer(
        self,
        model: BaseLLMModel,
        bs: int,
        buffer: GraphCaptureBuffer,
        offset: int = 0,
    ) -> None:
        hidden, hidden_states = model.model.forward(
            get_global_ctx().batch.input_ids,
            return_hidden_layers=self.hidden_layer_ids,
        )
        logits = project_lm_head_all_positions(model.lm_head, hidden)
        buffer.logits[offset : offset + bs].copy_(logits[:bs])
        if buffer.hidden_states is None:
            return
        assert len(hidden_states) == len(buffer.hidden_states)
        for dst, src in zip(buffer.hidden_states, hidden_states):
            dst[offset : offset + bs].copy_(src[:bs])

    def can_use_cuda_graph(self, batch: Batch) -> bool:
        return batch.is_decode and batch.size <= self.max_graph_bs

    def can_return_hidden_layers(self, hidden_layer_ids: set[int] | None) -> bool:
        return set(hidden_layer_ids or []) == self.hidden_layer_ids

    def can_use_dflash_target_verify_graph(self, batch: Batch, verify_len: int) -> bool:
        return (
            batch.size == 1
            and batch.padded_size == 1
            and batch.input_ids.numel() == verify_len
            and verify_len in self.dflash_target_verify_graph_map
        )

    def replay_dflash_target_verify(
        self,
        batch: Batch,
        verify_len: int,
        *,
        return_hidden_layers: set[int] | None = None,
        return_linear_snapshots: bool = False,
    ) -> torch.Tensor | tuple[torch.Tensor, list[torch.Tensor]]:
        assert self.can_use_dflash_target_verify_graph(batch, verify_len)
        wants_hidden = bool(return_hidden_layers)
        assert not wants_hidden or self.can_return_hidden_layers(return_hidden_layers)
        buffer = self.dflash_target_verify_buffers[verify_len]
        assert not wants_hidden or buffer.hidden_states is not None
        assert not return_linear_snapshots or buffer.dflash_conv_states is not None
        original_phase = batch.phase
        batch.phase = "decode"
        try:
            buffer.copy_dflash_verify_from(batch, verify_len)
            buffer.set_dflash_target_verify_batch(
                batch,
                verify_len,
                return_linear_snapshots=return_linear_snapshots,
            )
            prepare_replay = getattr(self.attn_backend, "prepare_for_dflash_target_verify_replay")
            prepare_replay(batch, verify_len)
            self.dflash_target_verify_graph_map[verify_len].replay()
        finally:
            batch.phase = original_phase
        logits = buffer.logits[:verify_len]
        linear_snapshots = None
        if return_linear_snapshots:
            # per-token conv states and the recurrence inputs, for the commit
            linear_snapshots = (
                buffer.dflash_conv_states[:verify_len],
                buffer.dflash_gdn_mixed[:, :verify_len],
                buffer.dflash_gdn_ab[:, :, :verify_len],
            )
        if wants_hidden:
            assert buffer.hidden_states is not None
            if return_linear_snapshots:
                return logits, [h[:verify_len] for h in buffer.hidden_states], linear_snapshots
            return logits, [h[:verify_len] for h in buffer.hidden_states]
        if return_linear_snapshots:
            return logits, linear_snapshots
        return logits

    def replay(
        self,
        batch: Batch,
        *,
        return_hidden_layers: set[int] | None = None,
    ) -> torch.Tensor | tuple[torch.Tensor, list[torch.Tensor]]:
        assert self.can_use_cuda_graph(batch)
        wants_hidden = bool(return_hidden_layers)
        assert not wants_hidden or self.can_return_hidden_layers(return_hidden_layers)
        assert not wants_hidden or self.buffer.hidden_states is not None
        self.buffer.copy_from(batch)
        g = self.graph_map[batch.padded_size]
        self.attn_backend.prepare_for_replay(batch)
        g.replay()
        logits = self.buffer.logits[: batch.size]
        if wants_hidden:
            assert self.buffer.hidden_states is not None
            return logits, [h[: batch.size] for h in self.buffer.hidden_states]
        return logits

    def pad_batch(self, batch: Batch) -> None:
        padded_size = (  # choose the first available batch size
            next(bs for bs in self.graph_bs_list if bs >= batch.size)
            if self.can_use_cuda_graph(batch)
            else batch.size
        )
        batch.padded_reqs = batch.reqs + [self.dummy_req] * (padded_size - batch.size)

    # NOTE: This must be called before freeing NCCL resources to prevent program hang
    def destroy_cuda_graphs(self) -> None:
        # Drop the CUDAGraph objects (and the shared mempool they hold) AND the static
        # GraphCaptureBuffer tensors ([max_bs, vocab] logits + input/out_loc/positions/...).
        # Dropping the references is the load-bearing step; without it a runtime rebuild's
        # free-before-alloc cannot reclaim this GPU memory. empty_cache() is left to the
        # caller / next capture (GraphRunner._capture_graphs already runs it).
        self.graph_map = {}
        self.dflash_target_verify_graph_map = {}
        self.dflash_target_verify_buffers = {}
        self.buffer = None
        gc.collect()
