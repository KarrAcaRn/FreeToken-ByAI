"""DFlash2's grouped dynamic causal conv in one launch.

``out[b, t, c] = sum_o (base[o, c] + dynamic[b, t, o, c // group_size]) * x[b, t - o, c]`` over
the taps ``o`` that stay inside block ``b`` (``t - o >= 0``). The torch composition spends ~10
launches per call (zeros, pad, mul, add, addcmul per tap); the draft calls it 20 times per
block, all eager, so the launches -- not the math -- were the cost.
"""

from __future__ import annotations

import torch
import triton
import triton.language as tl


@triton.jit
def _grouped_dynamic_conv_kernel(
    x_ptr, dyn_ptr, base_ptr, out_ptr,
    H, block_len,
    stride_xr, stride_dr, stride_dk, stride_bk, stride_or,
    GROUP: tl.constexpr, TAPS: tl.constexpr, BLOCK_C: tl.constexpr,
):
    row = tl.program_id(0)
    offs = tl.program_id(1) * BLOCK_C + tl.arange(0, BLOCK_C)
    mask = offs < H
    t = row % block_len
    acc = tl.zeros((BLOCK_C,), dtype=tl.float32)
    for o in tl.static_range(TAPS):
        if t >= o:
            x = tl.load(x_ptr + (row - o) * stride_xr + offs, mask=mask, other=0.0).to(tl.float32)
            w = tl.load(base_ptr + o * stride_bk + offs, mask=mask, other=0.0).to(tl.float32)
            d = tl.load(dyn_ptr + row * stride_dr + o * stride_dk + offs // GROUP, mask=mask, other=0.0)
            acc += (w + d.to(tl.float32)) * x
    tl.store(out_ptr + row * stride_or + offs, acc.to(out_ptr.dtype.element_ty), mask=mask)


def grouped_dynamic_conv(
    hidden: torch.Tensor,   # [rows, H], rows = B * block_len
    dynamic: torch.Tensor,  # [rows, taps, groups] (any strides with a unit group stride)
    base: torch.Tensor,     # [taps, H]
    group_size: int,
    block_len: int,
) -> torch.Tensor:
    rows, H = hidden.shape
    taps = base.shape[0]
    assert hidden.stride(-1) == 1 and dynamic.stride(-1) == 1 and base.stride(-1) == 1
    out = torch.empty_like(hidden)
    BLOCK_C = 1024
    _grouped_dynamic_conv_kernel[(rows, triton.cdiv(H, BLOCK_C))](
        hidden, dynamic, base, out, H, block_len,
        hidden.stride(0), dynamic.stride(0), dynamic.stride(1), base.stride(0), out.stride(0),
        GROUP=group_size, TAPS=taps, BLOCK_C=BLOCK_C, num_warps=4,
    )
    return out
