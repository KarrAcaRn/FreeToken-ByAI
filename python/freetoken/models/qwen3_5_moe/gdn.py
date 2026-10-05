from __future__ import annotations

import torch
import torch.nn.functional as F
from freetoken.core import get_global_ctx
from freetoken.kernel.causal_conv1d import causal_conv1d_decode, causal_conv1d_varlen
from freetoken.layers import BaseOP, GatedRMSNorm, LinearColParallelMerged, LinearReplicated
from freetoken.layers.quantization import QuantConfig

from .gdn_kernels import gdn_decode_fla, gdn_prefill_chunk_fla


def _dflash_conv_history(pre_state: torch.Tensor, conv_in: torch.Tensor) -> torch.Tensor:
    """``pre_state`` [B, conv_dim, kernel - 1] and ``conv_in`` [B * T, conv_dim] (B verify
    blocks of T tokens) -> each block's conv input stream [B, conv_dim, kernel - 1 + T]."""
    blocks = conv_in.view(pre_state.shape[0], -1, conv_in.shape[-1]).transpose(1, 2)
    return torch.cat([pre_state, blocks.to(pre_state.dtype)], dim=-1)


def _dflash_conv_state_steps(pre_state: torch.Tensor, conv_in: torch.Tensor) -> torch.Tensor:
    """Rolling conv state after each token of B short DFlash verify blocks: ``[B * T, conv_dim,
    kernel - 1]`` from ``pre_state`` [B, conv_dim, kernel - 1] and ``conv_in`` [B * T, conv_dim]."""
    history = _dflash_conv_history(pre_state, conv_in)
    width, length = pre_state.shape[-1], history.shape[-1] - pre_state.shape[-1]
    steps = torch.stack([history[..., i + 1 : i + 1 + width] for i in range(length)], dim=1)
    return steps.reshape(-1, *steps.shape[2:])


def _dflash_conv_mixed_steps(
    pre_state: torch.Tensor,
    conv_in: torch.Tensor,
    weight: torch.Tensor,
) -> torch.Tensor:
    """Depthwise causal-conv outputs [B * T, conv_dim] of B DFlash verify blocks, without
    state mutation."""
    history = _dflash_conv_history(pre_state, conv_in)
    kernel, length = weight.shape[-1], history.shape[-1] - pre_state.shape[-1]
    windows = torch.stack([history[..., i : i + kernel] for i in range(length)], dim=1)
    mixed = (windows * weight.to(windows.dtype)).sum(dim=-1)  # [B, T, conv_dim]
    return F.silu(mixed).reshape(-1, mixed.shape[-1]).to(conv_in.dtype)


class _DepthwiseConv1d(BaseOP):
    """Holds the depthwise conv weight ``[conv_dim, 1, K]`` (key ``conv1d.weight``)."""

    def __init__(self, conv_dim: int, kernel: int):
        self.weight = torch.empty(conv_dim, 1, kernel)


class Qwen3_5GatedDeltaNet(BaseOP):
    """GatedDeltaNet op using the vendored flash-linear-attention triton kernels
    (``freetoken.kernel.fla``) for the recurrence and a per-request
    recurrent + conv state held in ``ctx.linear_state_pool`` (keyed by ``Req.table_idx``).

    Parameter names match HF (``in_proj_qkv``/``in_proj_z``/``in_proj_b``/``in_proj_a``/
    ``conv1d``/``A_log``/``dt_bias``/``norm``/``out_proj``). Handles prefill (incl. chunked
    continuation) and single-token decode; state is fresh when ``req.cached_len == 0``.
    """

    def __init__(
        self, hidden_size, num_k_heads, num_v_heads, head_k_dim, head_v_dim,
        conv_kernel_size, rms_norm_eps, layer_id, *, quant_config: QuantConfig | None = None,
        prefix: str = "",
    ):
        self.layer_id = layer_id
        # The fla chunk/decode kernels read+write the recurrent state and the per-chunk h as
        # [V, K] while the LinearStatePool declares it [K, V]; these coincide (and the
        # hybrid-radix snapshot scatter h[h_row]->slot is a plain copy) only when the two head
        # dims are equal. Qwen3.5/3.6 satisfy this (128/128); guard any future config.
        assert head_k_dim == head_v_dim, (
            f"GatedDeltaNet requires head_k_dim == head_v_dim, got {head_k_dim} != {head_v_dim}"
        )
        self.num_k_heads = num_k_heads
        self.num_v_heads = num_v_heads
        self.head_k_dim = head_k_dim
        self.head_v_dim = head_v_dim
        self.key_dim = num_k_heads * head_k_dim
        self.value_dim = num_v_heads * head_v_dim
        self.conv_dim = 2 * self.key_dim + self.value_dim
        self.conv_kernel_size = conv_kernel_size
        # quantized checkpoints quantize qkv|z but not b|a, so the fusion splits into a qkvz GEMM and a ba GEMM with their own schemes (matches sglang / vLLM)
        self._split_in_proj = (
            quant_config is not None and quant_config.scheme_for(f"{prefix}.in_proj_qkvz") is not None
        )

        self._in_proj_split = [self.conv_dim, self.value_dim, num_v_heads, num_v_heads]
        if self._split_in_proj:
            self.in_proj_qkvz = LinearColParallelMerged(
                hidden_size, [self.conv_dim, self.value_dim], has_bias=False,
                quant_config=quant_config, prefix=f"{prefix}.in_proj_qkvz",
            )
            self.in_proj_ba = LinearColParallelMerged(
                hidden_size, [num_v_heads, num_v_heads], has_bias=False,
                quant_config=quant_config, prefix=f"{prefix}.in_proj_ba",
            )
        else:
            # Fused input projection (one GEMM instead of four): qkv | z | b | a.
            self.in_proj = LinearColParallelMerged(
                hidden_size, self._in_proj_split, has_bias=False,
                quant_config=quant_config, prefix=f"{prefix}.in_proj",
            )
        self.conv1d = _DepthwiseConv1d(self.conv_dim, conv_kernel_size)
        # Recurrence-gating params kept in fp32 (exp/softplus is precision-sensitive,
        # and the fla kernel reads them as fp32) -- matches HF/sglang, and avoids a
        # per-call .float() upcast in the decode wrapper. The weight loader exempts
        # *.A_log / *.dt_bias from the model-dtype downcast.
        self.dt_bias = torch.empty(num_v_heads, dtype=torch.float32)
        self.A_log = torch.empty(num_v_heads, dtype=torch.float32)
        self.norm = GatedRMSNorm(head_v_dim, eps=rms_norm_eps)
        self.out_proj = LinearReplicated(
            self.value_dim, hidden_size, has_bias=False,
            quant_config=quant_config, prefix=f"{prefix}.out_proj",
        )

    def _gate_params(self, a: torch.Tensor, b: torch.Tensor):
        beta = b.sigmoid()
        g = -self.A_log.exp() * F.softplus(a.float() + self.dt_bias)
        return g, beta

    def _conv_weight(self) -> torch.Tensor:
        return self.conv1d.weight.squeeze(1)  # [conv_dim, kernel] for the fused kernel

    def _conv_prefill(self, conv_in, pool, cu_seqlens, cache_indices, has_initial_state,
                      max_seq_len=None) -> torch.Tensor:
        """Varlen causal conv (fused sgl_kernel) with silu; reads/updates each request's
        conv state in place by ``cache_indices`` slot. ``conv_in`` [total, conv_dim].
        ``cu_seqlens`` / ``cache_indices`` / ``has_initial_state`` / ``max_seq_len`` come from
        FLAMetadata; the last is host-known so the launch needs no D2H sync."""
        li = pool.local_index(self.layer_id)
        x = conv_in.transpose(0, 1).contiguous()  # [conv_dim, total]
        out = causal_conv1d_varlen(x, self._conv_weight(), pool.conv_states[li],
                                   cu_seqlens, cache_indices, has_initial_state,
                                   max_seq_len=max_seq_len)
        return out.transpose(0, 1)  # [total, conv_dim]

    def _conv_decode(self, conv_in: torch.Tensor, table_idx: torch.Tensor, pool) -> torch.Tensor:
        """Single-token causal conv update (fused sgl_kernel) by ``table_idx`` slot;
        updates conv state in place, no host loop -> CUDA-graph capturable.
        ``conv_in`` [B, conv_dim] -> silu(conv) [B, conv_dim]."""
        li = pool.local_index(self.layer_id)
        return causal_conv1d_decode(conv_in, pool.conv_states[li], self._conv_weight(), table_idx)

    def _write_track_snapshot(self, pool, li: int, conv_in: torch.Tensor,
                              h: torch.Tensor, fla) -> None:
        """Snapshot this layer's recurrent + conv state at the chunk-aligned track boundary
        into a donatable pool slot, on the forward stream (hybrid-radix extra_buffer path).
        SSM: ``recurrent_states[li, dst] = h[0, h_row]`` -- a DIRECT copy (h is [V,K], the
        state pool is [K,V]; they coincide because GDN requires head_k_dim == head_v_dim).
        Conv: the last (kernel-1) raw conv-input timesteps ending at the boundary."""
        rec = pool.recurrent_states[li]
        rec.index_copy_(0, fla.track_dst, h[0, fla.track_h_row].to(rec.dtype))
        cv = pool.conv_states[li]
        # conv_in [total, conv_dim]; gather the (kernel-1) window per tracked req.
        conv_win = conv_in[fla.track_conv_src].transpose(-1, -2).contiguous()  # [nt, conv_dim, K-1]
        cv.index_copy_(0, fla.track_dst, conv_win.to(cv.dtype))

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        ctx = get_global_ctx()
        batch = ctx.batch
        pool = ctx.linear_state_pool
        total = hidden_states.shape[0]
        dtype = hidden_states.dtype

        # Per-forward GDN metadata (cu_seqlens / cache_indices / continuation flags),
        # built once and shared by all GDN layers. The scheduler/graph set it; build it
        # lazily here (cached on the batch) for direct-op callers (tests).
        fla = batch.fla_metadata
        if fla is None:
            from freetoken.attention.linear import build_fla_metadata

            fla = build_fla_metadata(batch, hidden_states.device)
            batch.fla_metadata = fla

        if self._split_in_proj:
            qkvz = self.in_proj_qkvz.forward(hidden_states)
            conv_in, z = torch.split(qkvz, [self.conv_dim, self.value_dim], dim=-1)
            ba = self.in_proj_ba.forward(hidden_states)
            b, a = torch.split(ba, [self.num_v_heads, self.num_v_heads], dim=-1)
        else:
            proj = self.in_proj.forward(hidden_states)
            conv_in, z, b, a = torch.split(proj, self._in_proj_split, dim=-1)
        z = z.reshape(total, self.num_v_heads, self.head_v_dim)
        li = pool.local_index(self.layer_id)

        dflash_conv_buffer = getattr(fla, "dflash_conv_states_buffer", None)
        if batch.is_decode or dflash_conv_buffer is not None:
            # Fused fla decode kernel: gating + in-kernel l2norm + recurrent update +
            # per-request state read/write-by-index, all in one kernel (no gather/scatter,
            # no clone, no external l2norm). q/k stay at num_k_heads (kernel handles GQA).
            if dflash_conv_buffer is not None:
                pre_conv_state = pool.conv_states[li].index_select(0, fla.cache_indices.to(torch.long))
                dflash_conv_buffer[:, li].copy_(
                    _dflash_conv_state_steps(pre_conv_state, conv_in)
                )
                mixed = _dflash_conv_mixed_steps(pre_conv_state, conv_in, self._conv_weight())
                if fla.dflash_gdn_mixed is not None:
                    fla.dflash_gdn_mixed[li].copy_(mixed)
                    fla.dflash_gdn_ab[li, 0].copy_(a)
                    fla.dflash_gdn_ab[li, 1].copy_(b)
            else:
                mixed = self._conv_decode(conv_in, fla.cache_indices, pool)  # [B, conv_dim]
            B = mixed.shape[0]
            qf, kf, vf = torch.split(mixed, [self.key_dim, self.key_dim, self.value_dim], dim=-1)
            q = qf.reshape(1, B, self.num_k_heads, self.head_k_dim).to(dtype)
            k = kf.reshape(1, B, self.num_k_heads, self.head_k_dim).to(dtype)
            v = vf.reshape(1, B, self.num_v_heads, self.head_v_dim).to(dtype)
            core_out = gdn_decode_fla(
                q, k, v, a, b, A_log=self.A_log, dt_bias=self.dt_bias,
                state_source=pool.recurrent_states[li], indices=fla.cache_indices,
                cu_seqlens=fla.cu_seqlens, scale=self.head_k_dim ** -0.5,
                disable_state_update=fla.dflash_disable_state_update,
            )
        else:
            if self.key_dim % 64 == 0 and conv_in.stride(-1) == 1:
                # token-major conv straight into contiguous q/k/v: no transposes, no copies
                from freetoken.kernel.triton.causal_conv1d_triton import causal_conv1d_varlen_split

                qf, kf, vf = causal_conv1d_varlen_split(
                    conv_in, self._conv_weight(), pool.conv_states[li], fla.cu_seqlens,
                    fla.cache_indices, fla.has_initial_state, self.key_dim, fla.max_seq_len)
            else:
                mixed = self._conv_prefill(
                    conv_in, pool, fla.cu_seqlens, fla.cache_indices, fla.has_initial_state,
                    fla.max_seq_len)
                qf, kf, vf = torch.split(mixed, [self.key_dim, self.key_dim, self.value_dim], dim=-1)
            # fla chunk handles GQA in-kernel: q/k stay at num_k_heads, v at num_v_heads.
            q = qf.reshape(1, total, self.num_k_heads, self.head_k_dim).to(dtype)
            k = kf.reshape(1, total, self.num_k_heads, self.head_k_dim).to(dtype)
            v = vf.reshape(1, total, self.num_v_heads, self.head_v_dim).to(dtype)
            g, beta = self._gate_params(a, b)
            g = g.reshape(1, total, self.num_v_heads)
            beta = beta.float().reshape(1, total, self.num_v_heads)
            # The chunk kernel reads + writes back initial_state[cache_indices] in place;
            # fresh sequences (cached_len==0) must start from a zeroed slot.
            if fla.fresh_state_indices is not None:
                pool.recurrent_states[li].index_fill_(0, fla.fresh_state_indices, 0.0)
            track = fla.track_dst is not None
            result = gdn_prefill_chunk_fla(
                q, k, v, g, beta,
                state_source=pool.recurrent_states[li], indices=fla.cache_indices,
                cu_seqlens=fla.cu_seqlens, scale=self.head_k_dim ** -0.5,
                return_h=track,
            )
            if track:
                core_out, h = result
                self._write_track_snapshot(pool, li, conv_in, h, fla)
            else:
                core_out = result

        core_out = core_out.reshape(-1, self.head_v_dim)
        z = z.reshape(-1, self.head_v_dim)
        out = self.norm.forward(core_out, z).reshape(total, -1)
        return self.out_proj.forward(out)


    def dflash_commit(
        self,
        pool,
        slot: torch.Tensor,        # [1] int32: the request's live slot
        cu_seqlens: torch.Tensor,  # [2] int32: [0, n]
        mixed: torch.Tensor,       # [n, conv_dim]: the verify's post-conv q/k/v of the kept tokens
        ab: torch.Tensor,          # [2, n, num_v_heads]: their raw a/b gates
    ) -> None:
        """Advance the live recurrent state over the first n tokens of a DFlash verify, from
        the inputs the verify stored (it left the slot untouched)."""
        n = mixed.shape[0]
        qf, kf, vf = torch.split(mixed, [self.key_dim, self.key_dim, self.value_dim], dim=-1)
        gdn_decode_fla(
            qf.reshape(1, n, self.num_k_heads, self.head_k_dim),
            kf.reshape(1, n, self.num_k_heads, self.head_k_dim),
            vf.reshape(1, n, self.num_v_heads, self.head_v_dim),
            ab[0], ab[1], A_log=self.A_log, dt_bias=self.dt_bias,
            state_source=pool.recurrent_states[pool.local_index(self.layer_id)], indices=slot,
            cu_seqlens=cu_seqlens, scale=self.head_k_dim ** -0.5,
        )


__all__ = ["Qwen3_5GatedDeltaNet"]
