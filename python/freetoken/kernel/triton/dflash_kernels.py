"""DFlash2 draft pieces as single launches: the grouped dynamic causal conv and the greedy
candidate-path selector, both run eagerly every draft block.

Conv: ``out[b, t, c] = sum_o (base[o, c] + dynamic[b, t, o, c // group_size]) * x[b, t - o, c]`` over
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


@triton.jit
def _selector_greedy_kernel(
    unary_ptr, cand_ptr, hproj_ptr, pred_cb_ptr, succ_cb_ptr, anchor_ptr, out_ptr,
    P, K, RANK,
    stride_ub, stride_up, stride_cb, stride_cp, stride_hb, stride_hp, stride_ob,
    BLOCK_K: tl.constexpr, BLOCK_R: tl.constexpr,
):
    b = tl.program_id(0)
    offs_k = tl.arange(0, BLOCK_K)
    offs_r = tl.arange(0, BLOCK_R)
    k_mask = offs_k < K
    r_mask = offs_r < RANK
    prev = tl.load(anchor_ptr + b).to(tl.int64)
    for p in range(P):
        # same bf16 roundings as the torch path: pred * hidden, the successor dot, the add
        pred = tl.load(pred_cb_ptr + prev * RANK + offs_r, mask=r_mask, other=0.0)
        h = tl.load(hproj_ptr + b * stride_hb + p * stride_hp + offs_r, mask=r_mask, other=0.0)
        pv = (pred.to(tl.float32) * h.to(tl.float32)).to(tl.bfloat16).to(tl.float32)
        cand = tl.load(cand_ptr + b * stride_cb + p * stride_cp + offs_k, mask=k_mask, other=0)
        succ = tl.load(succ_cb_ptr + cand[:, None] * RANK + offs_r[None, :],
                       mask=k_mask[:, None] & r_mask[None, :], other=0.0).to(tl.float32)
        dot = tl.sum(succ * pv[None, :], axis=1).to(tl.bfloat16).to(tl.float32)
        un = tl.load(unary_ptr + b * stride_ub + p * stride_up + offs_k, mask=k_mask, other=0.0).to(tl.float32)
        scores = (un + dot).to(tl.bfloat16).to(tl.float32)
        scores = tl.where(k_mask, scores, -float("inf"))
        best = tl.max(scores, axis=0)
        idx = tl.min(tl.where(scores == best, offs_k, BLOCK_K), axis=0)  # first max, like argmax
        prev = tl.sum(tl.where(offs_k == idx, cand, 0), axis=0).to(tl.int64)
        tl.store(out_ptr + b * stride_ob + p, prev)


def selector_greedy_paths(
    unary: torch.Tensor,        # [B, P, k] top-k logits
    candidates: torch.Tensor,   # [B, P, k] their token ids
    hidden_proj: torch.Tensor,  # [B, P, rank]
    pred_codebook: torch.Tensor,  # [vocab, rank]
    succ_codebook: torch.Tensor,  # [vocab, rank]
    anchor: torch.Tensor,       # [>= B]
) -> torch.Tensor:
    """DFlash2's greedy path through the per-position candidates, one launch for all
    positions: each step scores the candidates against the previous pick and keeps the best."""
    B, P, K = candidates.shape
    rank = hidden_proj.shape[-1]
    assert pred_codebook.is_contiguous() and succ_codebook.is_contiguous()
    assert unary.stride(-1) == 1 and candidates.stride(-1) == 1 and hidden_proj.stride(-1) == 1
    out = torch.empty((B, P), dtype=candidates.dtype, device=candidates.device)
    _selector_greedy_kernel[(B,)](
        unary, candidates, hidden_proj, pred_codebook, succ_codebook, anchor, out,
        P, K, rank,
        unary.stride(0), unary.stride(1), candidates.stride(0), candidates.stride(1),
        hidden_proj.stride(0), hidden_proj.stride(1), out.stride(0),
        BLOCK_K=triton.next_power_of_2(K), BLOCK_R=triton.next_power_of_2(rank), num_warps=4,
    )
    return out
