"""bf16-weight GEMV with on-chip upcast + fp32 accumulate/output (DeepSeek-V4).

Several DSV4 decode ops need fp32 *math* on bf16 weights (the compressor wkv/wgate
gated pool, the MoE router) for numerical stability. Doing it as
``F.linear(x.float(), w.float())`` materializes an fp32 copy of the weight in HBM
every step (read bf16 + write fp32 + re-read fp32) and runs a heavier fp32 GEMM.

The shared ``bf16_gemv`` kernel instead streams the bf16 weight from HBM once, upcasts
to fp32 in registers, and accumulates in fp32 -> fp32 output. Same precision as the
reference (only the fp32 accumulation *order* differs, ~1e-6), at the HBM cost of a
plain bf16 read. Decode is M==1 (a GEMV); M>1 (prefill) falls back to F.linear.
"""

from __future__ import annotations

import torch
import torch.nn.functional as F

from freetoken.kernel.triton.bf16_gemv import bf16_gemv


def bf16_linear_fp32(x: torch.Tensor, weight: torch.Tensor) -> torch.Tensor:
    """``out = x @ weight.T`` in fp32, reading ``weight`` (bf16) straight from HBM.

    ``x``: ``[..., K]`` (leading dims collapse to M). ``weight``: ``[N, K]`` bf16.
    Returns ``[..., N]`` fp32. Bit-exact to ``F.linear(x.float(), weight.float())``
    up to fp32 accumulation order; for M>1 it *is* that call (prefill)."""
    *lead, K = x.shape
    N = weight.shape[0]
    M = 1
    for d in lead:
        M *= d
    if M != 1:
        return F.linear(x.float(), weight.float())
    return bf16_gemv(x.reshape(K).contiguous(), weight, torch.float32).reshape(*lead, N)


__all__ = ["bf16_linear_fp32"]
