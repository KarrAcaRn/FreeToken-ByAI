"""Single-row GEMV over a bf16 weight: one pass over HBM, upcast in registers, fp32 accumulate.

At M == 1 the weight read is the whole cost. cuBLAS runs a single-row bf16 ``F.linear`` on GEMM
tiles that leave bandwidth on the table (~770 GB/s against ~945 GB/s achievable on a 3090 Ti);
this kernel streams the weight once, two output rows per CTA, and stores in the caller's dtype.

Two callers share it: the dense bf16 linear at decode bs=1 (``bf16`` out, see
``layers/quantization/linear/unquantized.py``) and DeepSeek-V4's fp32-math projections
(``fp32`` out, ``kernel/triton/dsv4/bf16_linear.py``).
"""

from __future__ import annotations

import torch
import triton
import triton.language as tl


@triton.jit
def _bf16_gemv_kernel(
    x_ptr, w_ptr, out_ptr, N, K,
    stride_xk, stride_wn, stride_wk,
    BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr,
):
    pid = tl.program_id(0)
    offs_n = pid * BLOCK_N + tl.arange(0, BLOCK_N)
    n_mask = offs_n < N
    w_row = w_ptr + offs_n[:, None] * stride_wn
    acc = tl.zeros((BLOCK_N,), tl.float32)
    for k0 in range(0, K, BLOCK_K):
        offs_k = k0 + tl.arange(0, BLOCK_K)
        k_mask = offs_k < K
        w = tl.load(w_row + offs_k[None, :] * stride_wk,
                    mask=n_mask[:, None] & k_mask[None, :], other=0.0).to(tl.float32)
        xk = tl.load(x_ptr + offs_k * stride_xk, mask=k_mask, other=0.0).to(tl.float32)
        acc += tl.sum(w * xk[None, :], axis=1)
    tl.store(out_ptr + offs_n, acc.to(out_ptr.dtype.element_ty), mask=n_mask)


def bf16_gemv(x: torch.Tensor, weight: torch.Tensor, out_dtype: torch.dtype) -> torch.Tensor:
    """``weight @ x`` for ``x`` [K] and ``weight`` [N, K] bf16; returns [N] in ``out_dtype``."""
    if weight.dim() != 2 or weight.dtype != torch.bfloat16:
        raise ValueError(f"bf16_gemv wants a 2-D bf16 weight, got {tuple(weight.shape)} {weight.dtype}")
    N, K = weight.shape
    # the kernel indexes x by the weight's K, so a narrower x would be read out of bounds
    if x.dim() != 1 or x.shape[0] != K:
        raise ValueError(f"bf16_gemv: x {tuple(x.shape)} does not match weight width K={K}")
    if x.device != weight.device:
        raise ValueError(f"bf16_gemv: x on {x.device}, weight on {weight.device}")
    out = torch.empty(N, dtype=out_dtype, device=x.device)
    # BN=2 -> N/2 CTAs spreads the GEMV across SMs; BLOCK_K covering all of K avoids a K-loop
    # up to 4096. Tuned on H100 (~2 TB/s at N=1024).
    BLOCK_N = 2
    BLOCK_K = min(triton.next_power_of_2(K), 4096)
    _bf16_gemv_kernel[(triton.cdiv(N, BLOCK_N),)](
        x, weight, out, N, K,
        x.stride(0), weight.stride(0), weight.stride(1),
        BLOCK_N=BLOCK_N, BLOCK_K=BLOCK_K, num_warps=4,
    )
    return out


def single_row_bf16(x: torch.Tensor, weight: torch.Tensor) -> bool:
    """Whether ``F.linear(x, weight)`` is one bf16 row against a row-major bf16 [N, K] weight.

    Shape, dtype and layout only; the caller checks the device and the bias."""
    if weight.dim() != 2 or x.dim() == 0:
        return False
    K = weight.shape[1]
    return (
        x.dtype == torch.bfloat16 and weight.dtype == torch.bfloat16
        and x.shape[-1] == K and x.numel() == K and K > 0
        and weight.stride(1) == 1
    )


__all__ = ["bf16_gemv", "single_row_bf16"]
