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
    # Pipeline stage: the residual stream received from the previous stage (non-first stages)
    # and the one handed to the next (non-last stages, which then have no logits)
    pp_in: torch.Tensor | None = None
    pp_out: torch.Tensor | None = None
    # DFlash verify graphs: (requests, verify len); on a GDN target, per-token conv states and
    # recurrence inputs (FLAMetadata)
    dflash_shape: tuple[int, int] = (1, 1)
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
        pp_stage: tuple[bool, bool, int] | None = None,
    ) -> GraphCaptureBuffer:
        """``pp_stage``: (first, last, residual width) of this pipeline stage."""
        hidden_states = None
        pp_in = pp_out = None
        if pp_stage is not None:
            first, last, width = pp_stage
            dtype = hidden_dtype or torch.get_default_dtype()
            if not first:
                pp_in = torch.zeros(bs, width, dtype=dtype, device=device)
            if not last:
                pp_out = torch.zeros(bs, width, dtype=dtype, device=device)
                vocab_size = 0
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
            pp_in=pp_in,
            pp_out=pp_out,
        )

    @classmethod
    def init_dflash_verify(
        cls,
        bs: int,
        verify_len: int,
        device: torch.device,
        storage: DFlashVerifyStorage,
    ) -> GraphCaptureBuffer:
        """Buffers of one (bs, verify_len) verify graph. The large ones (logits, hidden states,
        GDN commit inputs) are views of ``storage``, shared by every verify graph -- they never
        run at once."""
        rows = bs * verify_len
        buffer = GraphCaptureBuffer(
            input_ids=torch.zeros(rows, dtype=torch.int32, device=device),
            out_loc=torch.zeros(rows, dtype=torch.int32, device=device),
            positions=torch.zeros(rows, dtype=torch.int32, device=device),
            mrope_positions=None,
            logits=storage.logits[:rows],
            hidden_states=[h[:rows] for h in storage.hidden] if storage.hidden else None,
            table_idx=torch.zeros(bs, dtype=torch.int32, device=device),
            fla_cu_seqlens=torch.arange(
                0, (bs + 1) * verify_len, verify_len, dtype=torch.int32, device=device),
            fla_has_initial_state=torch.ones(bs, dtype=torch.bool, device=device),
            dflash_shape=(bs, verify_len),
        )
        if storage.conv is not None:
            layers, conv_dim, km1, num_v = storage.gdn_dims
            conv_shape = (rows, layers, conv_dim, km1)
            mixed_shape = (layers, rows, conv_dim)
            ab_shape = (layers, 2, rows, num_v)
            buffer.dflash_conv_states = storage.conv[: math.prod(conv_shape)].view(conv_shape)
            n_mixed = math.prod(mixed_shape)
            buffer.dflash_gdn_mixed = storage.inputs[:n_mixed].view(mixed_shape)
            buffer.dflash_gdn_ab = storage.inputs[n_mixed : n_mixed + math.prod(ab_shape)].view(ab_shape)
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
        if self.pp_in is not None:
            batch.pp_hidden = self.pp_in[_slice]

    def copy_from(self, batch: Batch) -> None:
        _slice = slice(batch.padded_size)
        if self.pp_in is not None:
            assert batch.pp_hidden is not None, "a non-first pipeline stage replays on received rows"
            self.pp_in[_slice] = batch.pp_hidden[_slice]
        self.input_ids[_slice] = batch.input_ids
        if batch.out_loc is not None:
            self.out_loc[_slice] = batch.out_loc
        self.positions[_slice] = batch.positions
        if self.mrope_positions is not None:
            self.mrope_positions[:, _slice] = batch.mrope_positions
        if batch.linear_table_idx is not None:
            self.table_idx[_slice] = batch.linear_table_idx

    def copy_dflash_verify_from(self, batch: Batch) -> None:
        bs, verify_len = self.dflash_shape
        rows = bs * verify_len
        self.input_ids[:rows] = batch.input_ids[:rows]
        if batch.out_loc is not None:
            self.out_loc[:rows] = batch.out_loc[:rows]
        self.positions[:rows] = batch.positions[:rows]
        if batch.linear_table_idx is not None:
            self.table_idx[:bs] = batch.linear_table_idx[:bs]

    def set_dflash_target_verify_batch(self, batch: Batch, *, return_linear_snapshots: bool = False) -> None:
        from freetoken.attention.linear import FLAMetadata

        bs, verify_len = self.dflash_shape
        rows = bs * verify_len
        batch.input_ids = self.input_ids[:rows]
        batch.out_loc = self.out_loc[:rows]
        batch.positions = self.positions[:rows]
        batch.linear_table_idx = self.table_idx[:bs]
        linear = return_linear_snapshots
        if linear and self.dflash_conv_states is None:
            raise RuntimeError("DFlash target verify graph requires linear snapshot buffers")
        batch.fla_metadata = FLAMetadata(
            cu_seqlens=self.fla_cu_seqlens[: bs + 1],
            cache_indices=self.table_idx[:bs],
            has_initial_state=self.fla_has_initial_state[:bs],
            dflash_disable_state_update=linear,
            dflash_conv_states_buffer=self.dflash_conv_states if linear else None,
            dflash_gdn_mixed=self.dflash_gdn_mixed if linear else None,
            dflash_gdn_ab=self.dflash_gdn_ab if linear else None,
        )


@dataclass
class DFlashVerifyStorage:
    """Flat storage the verify graphs' large buffers view (see init_dflash_verify)."""

    logits: torch.Tensor                 # [rows, vocab] fp32
    hidden: list[torch.Tensor]           # per returned target layer: [rows, hidden]
    conv: torch.Tensor | None = None     # GDN: per-token conv states
    inputs: torch.Tensor | None = None   # GDN: per-token q/k/v + a/b gates
    gdn_dims: tuple[int, int, int, int] = (0, 0, 0, 0)  # layers, conv_dim, kernel-1, value heads

    @classmethod
    def alloc(cls, rows, vocab_size, device, *, hidden_size, hidden_dtype, num_hidden_layers,
              linear_state_pool=None) -> DFlashVerifyStorage:
        storage = cls(
            logits=torch.empty(rows, vocab_size, dtype=torch.float32, device=device),
            hidden=[torch.empty(rows, hidden_size, dtype=hidden_dtype, device=device)
                    for _ in range(num_hidden_layers)],
        )
        if linear_state_pool is not None:
            conv, rec = linear_state_pool.conv_states, linear_state_pool.recurrent_states
            layers, conv_dim, km1, num_v = conv.shape[0], conv.shape[2], conv.shape[3], rec.shape[2]
            storage.conv = torch.empty(rows * conv[:, 0].numel(), dtype=conv.dtype, device=device)
            storage.inputs = torch.empty(
                rows * layers * (conv_dim + 2 * num_v), dtype=hidden_dtype, device=device)
            storage.gdn_dims = (layers, conv_dim, km1, num_v)
        return storage


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
        dflash_verify_batch_sizes: list[int] | None = None,
        pp_stage: tuple[bool, bool, int] | None = None,
    ) -> None:
        self.pp_stage = pp_stage
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
        self.dflash_verify_batch_sizes = sorted(set(dflash_verify_batch_sizes or []))
        # verify len -> plain decode time / verify time, for the adaptive gate's baseline
        self.dflash_plain_over_verify: Dict[int, float] = {}
        self._plain_decode_ms: float | None = None
        # a model whose graphs wait on a host fill (disk PLE) releases that wait for the
        # timing replays, which run on the capture inputs with no fill
        self._prime_replay = getattr(model, "prime_graph_replay", None)
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
        self.dflash_target_verify_graph_map: Dict[tuple[int, int], torch.cuda.CUDAGraph] = {}
        self.dflash_target_verify_buffers: Dict[tuple[int, int], GraphCaptureBuffer] = {}
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
            pp_stage=self.pp_stage,
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
        init_verify = getattr(self.attn_backend, "init_dflash_target_verify_capture_graph", None)
        prepare_capture = getattr(self.attn_backend, "prepare_for_dflash_target_verify_capture", None)
        if init_verify is None or prepare_capture is None:
            logger.warning_rank0("DFlash target verify CUDA graph is disabled for this attention backend.")
            self.dflash_target_verify_lens = []
            return
        # one request at every verify len; batches of requests at the full block
        block = max(self.dflash_target_verify_lens)
        max_bs = getattr(self.attn_backend, "dflash_verify_max_bs", 1)
        shapes = [(1, n) for n in self.dflash_target_verify_lens] + [
            (b, block) for b in self.dflash_verify_batch_sizes if 1 < b <= max_bs
        ]
        linear_state_pool = get_global_ctx().linear_state_pool
        if linear_state_pool is not None:
            # the engine released the draft worker's reservation for this buffer just before
            budget = int(get_free_memory(self.device) * 0.9)
            per_row = dflash_verify_bytes_per_token(linear_state_pool, self.hidden_dtype)
            kept = [(b, n) for b, n in shapes if b * n * per_row <= budget]
            if len(kept) < len(shapes):
                logger.warning_rank0(
                    f"DFlash target verify graphs limited to {kept or '[]'} (commit buffer memory "
                    "budget); other verifies fall back to the decode-loop verify."
                )
            shapes = kept
        self.dflash_target_verify_lens = [n for b, n in shapes if b == 1]
        if not shapes:
            return
        storage = DFlashVerifyStorage.alloc(
            max(b * n for b, n in shapes), vocab_size, self.device,
            hidden_size=self.hidden_size, hidden_dtype=self.hidden_dtype,
            num_hidden_layers=len(self.hidden_layer_ids), linear_state_pool=linear_state_pool,
        )
        init_verify(max_seq_len=max_seq_len, shapes=shapes)
        dummy_slot = (self.dummy_req.linear_slot_idx
                      if self.dummy_req.linear_slot_idx is not None
                      else self.dummy_req.table_idx)
        for bs, verify_len in shapes:
            graph = torch.cuda.CUDAGraph()
            buffer = GraphCaptureBuffer.init_dflash_verify(bs, verify_len, self.device, storage)
            batch = Batch(reqs=[self.dummy_req] * bs, phase="decode")
            batch.padded_reqs = batch.reqs
            prepare_capture(batch, verify_len)
            buffer.set_dflash_target_verify_batch(
                batch, return_linear_snapshots=linear_state_pool is not None
            )
            buffer.positions.copy_(
                torch.arange(verify_len, dtype=torch.int32, device=self.device).repeat(bs))
            buffer.table_idx.fill_(dummy_slot)
            rows = bs * verify_len
            with get_global_ctx().forward_batch(batch):
                self._run_dflash_target_verify_into_buffer(model, rows, buffer)
                with torch.cuda.graph(graph, pool=pool, stream=self.stream):
                    self._run_dflash_target_verify_into_buffer(model, rows, buffer)
                self._reset_moe_offload_cache()
            self.dflash_target_verify_graph_map[bs, verify_len] = graph
            self.dflash_target_verify_buffers[bs, verify_len] = buffer
            if bs == 1 and self._plain_decode_ms is not None:
                verify_ms = self._time_replay(graph)
                if verify_ms > 0:
                    self.dflash_plain_over_verify[verify_len] = self._plain_decode_ms / verify_ms

        logger.info_rank0(f"DFlash target verify graphs captured for (requests, len) {shapes}")
        if self.dflash_plain_over_verify:
            ratios = ", ".join(f"{n}: {r:.2f}" for n, r in self.dflash_plain_over_verify.items())
            logger.info_rank0(
                f"DFlash plain decode {self._plain_decode_ms:.2f} ms; plain/verify ratio by len {{{ratios}}}"
            )

    def _time_replay(self, graph: torch.cuda.CUDAGraph, iters: int = 10) -> float:
        """Median ms of a captured graph replayed on its own (dummy) capture inputs."""
        prime = self._prime_replay or (lambda: None)
        prime()
        graph.replay()  # warm
        self.stream.synchronize()  # a primed wait must be consumed before the next prime
        times = []
        for _ in range(iters):
            start = torch.cuda.Event(enable_timing=True)
            end = torch.cuda.Event(enable_timing=True)
            prime()
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
        out = buffer.pp_out if buffer.pp_out is not None else buffer.logits
        out[offset : offset + bs].copy_(model.forward()[:bs])

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
            batch.padded_size == batch.size
            and batch.input_ids.numel() == batch.size * verify_len
            and (batch.size, verify_len) in self.dflash_target_verify_graph_map
        )

    def replay_dflash_target_verify(
        self,
        batch: Batch,
        verify_len: int,
        *,
        return_hidden_layers: set[int] | None = None,
        return_linear_snapshots: bool = False,
    ):
        """Verify ``batch.size`` requests of ``verify_len`` tokens each. Returns the logits
        [rows, vocab], then the hidden states (when asked) and the GDN commit inputs (when
        asked): per-token conv states, post-conv q/k/v and a/b gates."""
        assert self.can_use_dflash_target_verify_graph(batch, verify_len)
        wants_hidden = bool(return_hidden_layers)
        assert not wants_hidden or self.can_return_hidden_layers(return_hidden_layers)
        key = (batch.size, verify_len)
        buffer = self.dflash_target_verify_buffers[key]
        assert not wants_hidden or buffer.hidden_states is not None
        assert not return_linear_snapshots or buffer.dflash_conv_states is not None
        original_phase = batch.phase
        batch.phase = "decode"
        try:
            buffer.copy_dflash_verify_from(batch)
            buffer.set_dflash_target_verify_batch(batch, return_linear_snapshots=return_linear_snapshots)
            self.attn_backend.prepare_for_dflash_target_verify_replay(batch, verify_len)
            self.dflash_target_verify_graph_map[key].replay()
        finally:
            batch.phase = original_phase
        rows = batch.size * verify_len
        out = [buffer.logits[:rows]]
        if wants_hidden:
            out.append([h[:rows] for h in buffer.hidden_states])
        if return_linear_snapshots:
            out.append((
                buffer.dflash_conv_states[:rows],
                buffer.dflash_gdn_mixed[:, :rows],
                buffer.dflash_gdn_ab[:, :, :rows],
            ))
        return out[0] if len(out) == 1 else tuple(out)

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
        if self.buffer.pp_out is not None:
            # every padded row: the next stage replays the same padded batch
            return self.buffer.pp_out[: batch.padded_size]
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
