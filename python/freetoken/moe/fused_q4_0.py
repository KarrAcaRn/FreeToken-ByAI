"""Grouped expert GEMM over native GGUF Q4_0 banks (borrowed ggml MoE kernels).

Ports vLLM/sglang's ``_fused_moe_gguf`` MMVQ path onto FreeToken's offload-cache
interface: the experts are streamed to the GPU as packed Q4_0 block bytes and
dequantized *inside* ``ggml_moe_a8_vec`` -- no bf16 expert copy is materialized. We
use the MMVQ (vector) kernel for both prefill and decode: it consumes ``topk_ids``
directly (no ``moe_align_block_size`` needed) and on small batches it is the right
choice anyway. ``topk_ids`` already index the streamed cache slots (decode) or the
materialized layer positions (prefill).
"""

from __future__ import annotations

import torch

from freetoken.layers.activation import gelu_and_mul, gelu_tanh_and_mul, silu_and_mul
from freetoken.models.gguf.dequant import GGML_Q4_0, row_bytes

_ACT = {"silu": silu_and_mul, "gelu": gelu_and_mul, "gelu_tanh": gelu_tanh_and_mul}


def fused_experts_gguf_q4_0(
    hidden_states: torch.Tensor,
    gate_up_q: torch.Tensor,  # [num_slots, 2I, H//32*18] uint8
    down_q: torch.Tensor,  # [num_slots, H, I//32*18] uint8
    topk_weights: torch.Tensor,
    topk_ids: torch.Tensor,
    activation: str,
    *,
    gate_up_quant_type: int = GGML_Q4_0,
    down_quant_type: int = GGML_Q4_0,
    intermediate_size: int | None = None,
    hidden_size: int | None = None,
    is_prefill: bool = False,
) -> torch.Tensor:
    from freetoken.kernel.gguf import ggml_moe_a8_vec

    act_fn = _ACT.get(activation)
    if act_fn is None:
        raise ValueError(f"unsupported MoE activation {activation!r}")

    num_tokens = hidden_states.shape[0]
    n2 = 2 * intermediate_size if intermediate_size is not None else gate_up_q.shape[1]
    h = hidden_size if hidden_size is not None else down_q.shape[1]
    top_k = topk_ids.shape[1]
    if is_prefill and num_tokens >= _DEQUANT_MIN_TOKENS:
        return _fused_experts_gguf_dequant(
            hidden_states, gate_up_q, down_q, topk_weights, topk_ids, activation,
            gate_up_quant_type, down_quant_type, n2 // 2, h,
        )

    # gate_up: [num_tokens*top_k, 2I] -> activation -> [num_tokens*top_k, I]
    gate_up = ggml_moe_a8_vec(
        hidden_states, gate_up_q, topk_ids, top_k, int(gate_up_quant_type), n2, num_tokens
    )
    inter = act_fn(gate_up)
    # down: each of the num_tokens*top_k intermediate rows uses its own expert id.
    out = ggml_moe_a8_vec(
        inter, down_q, topk_ids, 1, int(down_quant_type), h, num_tokens * top_k
    )
    out = out.reshape(num_tokens, top_k, h) * topk_weights.reshape(num_tokens, top_k, 1).to(
        out.dtype
    )
    return out.sum(dim=1)


# From this many tokens on, the GEMV re-reads each expert once per routed row and loses to
# dequantizing the used experts to bf16 for the Triton grouped GEMM.
_DEQUANT_MIN_TOKENS = 512
# experts dequantized at once: bounds the bf16 transient (~6 MiB per Qwen3.6 expert)
_DEQUANT_CHUNK = 32


def _fused_experts_gguf_dequant(
    hidden_states: torch.Tensor,
    gate_up_q: torch.Tensor,
    down_q: torch.Tensor,
    topk_weights: torch.Tensor,
    topk_ids: torch.Tensor,
    activation: str,
    gate_up_quant_type: int,
    down_quant_type: int,
    inter: int,
    hidden: int,
) -> torch.Tensor:
    """Prefill: per chunk of used experts, dequantize their packed rows to bf16 and run the
    bf16 grouped GEMM over the routed rows that chose them (sorted by expert, top_k=1)."""
    from freetoken.kernel.gguf import ggml_dequantize
    from freetoken.moe.fused import fused_experts_impl

    num_tokens, top_k = topk_ids.shape
    flat_ids = topk_ids.reshape(-1).long()
    order = torch.argsort(flat_ids, stable=True)
    sorted_ids = flat_ids[order]
    used, counts = torch.unique_consecutive(sorted_ids, return_counts=True)
    counts_host = counts.tolist()
    gu_rows = gate_up_q.reshape(gate_up_q.shape[0], -1)
    dn_rows = down_q.reshape(down_q.shape[0], -1)
    out = torch.zeros(num_tokens, hidden, device=hidden_states.device, dtype=torch.float32)
    tokens = order // top_k
    weights = topk_weights.reshape(-1)[order].to(torch.float32)
    start = 0
    for c0 in range(0, len(counts_host), _DEQUANT_CHUNK):
        chunk = used[c0 : c0 + _DEQUANT_CHUNK]
        n = sum(counts_host[c0 : c0 + _DEQUANT_CHUNK])
        c = chunk.numel()
        # a fixed-width GGUF slot may be padded past this layer's packed bytes
        gu = gu_rows.index_select(0, chunk)[:, : 2 * inter * row_bytes(hidden, gate_up_quant_type)]
        dn = dn_rows.index_select(0, chunk)[:, : hidden * row_bytes(inter, down_quant_type)]
        w1 = ggml_dequantize(gu.reshape(c * 2 * inter, -1), gate_up_quant_type, c * 2 * inter, hidden, hidden_states.dtype)
        w2 = ggml_dequantize(dn.reshape(c * hidden, -1), down_quant_type, c * hidden, inter, hidden_states.dtype)
        rows = slice(start, start + n)
        local = torch.repeat_interleave(
            torch.arange(c, device=chunk.device, dtype=torch.int32),
            counts[c0 : c0 + _DEQUANT_CHUNK],
            output_size=n,
        ).unsqueeze(1)
        x = hidden_states.index_select(0, tokens[rows])
        y = fused_experts_impl(
            x, w1.view(c, 2 * inter, hidden), w2.view(c, hidden, inter),
            torch.ones(n, 1, device=x.device, dtype=torch.float32), local, activation,
        )
        out.index_add_(0, tokens[rows], y.to(torch.float32) * weights[rows, None])
        start += n
    return out.to(hidden_states.dtype)


__all__ = ["fused_experts_gguf_q4_0"]
