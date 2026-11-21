from __future__ import annotations

import torch
import triton
import triton.language as tl
from triton.language import target_info

from freetoken.kernel.triton.e4m3_compat import (
    e2m1_code_f32,
    e4m3_f32_to_u8,
    e4m3_native_cx,
    e4m3_u8_to_f32,
    f32_to_e4m3,
    round_e4m3,
)
from freetoken.kvcache.format import KVFormat


@triton.jit
def _kv_tile_gfx12_bf16(ptrs, mask, TRANSPOSE: tl.constexpr):
    # Force VOP3 (e64): LLVM's word-0 packed intrinsic selects an invalid VOP1 on gfx12.
    # Recheck plain FP8 casts when upgrading Triton (triton-lang/triton#11809).
    codes = tl.load(ptrs, mask=mask, other=0, cache_modifier=".cg")
    lo = tl.inline_asm_elementwise(
        "v_cvt_pk_f32_fp8_e64 $0, $1 op_sel:[0,0]", "=v,v", [codes],
        dtype=tl.uint64, is_pure=True, pack=1)
    hi = tl.inline_asm_elementwise(
        "v_cvt_pk_f32_fp8_e64 $0, $1 op_sel:[1,0]", "=v,v", [codes],
        dtype=tl.uint64, is_pure=True, pack=1)
    # Every finite E4M3FN value is exactly representable in BF16.
    a = (lo >> 16).to(tl.uint16).to(tl.bfloat16, bitcast=True)
    b = (lo >> 48).to(tl.uint16).to(tl.bfloat16, bitcast=True)
    c = (hi >> 16).to(tl.uint16).to(tl.bfloat16, bitcast=True)
    d = (hi >> 48).to(tl.uint16).to(tl.bfloat16, bitcast=True)
    if TRANSPOSE:
        a, b, c, d = tl.trans(a), tl.trans(b), tl.trans(c), tl.trans(d)
    values = tl.interleave(tl.interleave(a, c), tl.interleave(b, d))
    if TRANSPOSE:
        values = tl.trans(values)
    return values


@triton.jit
def kv_tile(ptrs, mask, FMT: tl.constexpr):
    """One K or V tile in the dtype ``tl.dot`` takes."""
    if FMT == "none":
        tile = tl.load(ptrs, mask=mask, other=0.0)
    elif FMT == "fp8_per_token_head":
        codes = tl.load(ptrs, mask=mask, other=0)
        if e4m3_native_cx():
            tile = codes.to(tl.float8e4nv, bitcast=True).to(tl.bfloat16)
        else:
            tile = e4m3_u8_to_f32(codes).to(tl.bfloat16)
    elif FMT == "int8_per_token_head":
        tile = tl.load(ptrs, mask=mask, other=0).to(tl.bfloat16)
    return tile


@triton.jit
def kv_tile_rows(
    ptr, slots, head, stride_slot, stride_head, row_mask,
    D: tl.constexpr, BLOCK_D: tl.constexpr, TRANSPOSE: tl.constexpr,
):
    """Read four E4M3FN codes per uint32 load and return a BF16 K or V tile."""
    tl.static_assert(D % 4 == 0)
    base = (ptr + head * stride_head).to(tl.pointer_type(tl.uint32))
    row_stride = stride_slot // 4
    dims = tl.arange(0, BLOCK_D // 4)
    if TRANSPOSE:
        ptrs = base + slots[None, :] * row_stride + dims[:, None]
        mask = row_mask[None, :] & (dims[:, None] < D // 4)
    else:
        ptrs = base + slots[:, None] * row_stride + dims[None, :]
        mask = row_mask[:, None] & (dims[None, :] < D // 4)
    return _kv_tile_gfx12_bf16(ptrs, mask, TRANSPOSE)


@triton.jit
def stage_tile(x):
    if target_info.is_hip():
        return x
    # Triton moves a dot operand's conversion back to its load past any side-effect-free op, so every warp would decode the whole tile; this asm stops that
    return tl.inline_asm_elementwise("mov.b32 $0, $1;", "=r,r", [x], dtype=tl.float32, is_pure=False, pack=1)


@triton.jit
def kv_tile_staged(ptrs, mask, FMT: tl.constexpr):
    """kv_tile for a tile that every warp of the CTA reads in full: on NVIDIA it decodes once per CTA and hands the bf16 tile to the MMA through shared memory; on HIP it is kv_tile."""
    if FMT == "none":
        tile = tl.load(ptrs, mask=mask, other=0.0)
    else:
        codes = tl.load(ptrs, mask=mask, other=0)
        if FMT == "fp8_per_token_head":
            if e4m3_native_cx():
                x = codes.to(tl.float8e4nv, bitcast=True).to(tl.float32)
            else:
                x = e4m3_u8_to_f32(codes)
        else:
            x = codes.to(tl.float32)
        tile = stage_tile(x).to(tl.bfloat16)
    return tile


@triton.jit
def kv_row_scale(ptrs, mask, FMT: tl.constexpr):
    """Row scales of a tile; all ones without scales, so the caller's multiply folds away."""
    if FMT == "none":
        scale = tl.full(mask.shape, 1.0, tl.float32)
    else:
        scale = tl.load(ptrs, mask=mask, other=0.0)
    return scale


@triton.jit
def kv_tile_nvfp4(rows, dims, mask, D: tl.constexpr, STAGED: tl.constexpr = False):
    """An nvfp4 K or V tile in bf16 without its row scale. ``rows`` point at each row's
    start and broadcast against the channels ``dims``; the D-wide row holds D / 2 code
    bytes (even channel in the low nibble) and then one e4m3 scale byte per 16 channels."""
    packed = tl.load(rows + dims // 2, mask=mask, other=0).to(tl.int32)
    codes = tl.where((dims & 1) == 0, packed & 15, packed >> 4)
    block = tl.load(rows + (D // 2 + dims // 16), mask=mask, other=0)
    # e2m1 x e4m3 has at most six significant bits, so the bf16 tile is exact
    x = e2m1_code_f32(codes) * e4m3_u8_to_f32(block)
    if STAGED:
        x = stage_tile(x)
    return x.to(tl.bfloat16)


@triton.jit
def _encode_e2m1(x):
    # round to nearest, ties to the even code
    a = tl.abs(x)
    code = tl.full(x.shape, 0, tl.int32)
    code = tl.where(a > 0.25, 1, code)
    code = tl.where(a >= 0.75, 2, code)
    code = tl.where(a > 1.25, 3, code)
    code = tl.where(a >= 1.75, 4, code)
    code = tl.where(a > 2.5, 5, code)
    code = tl.where(a >= 3.5, 6, code)
    code = tl.where(a > 5.0, 7, code)
    return code | tl.where(x < 0, 8, 0)


@triton.jit
def _store_nvfp4_segment(src, stride_src, dst, START: tl.constexpr, WIDTH: tl.constexpr, D: tl.constexpr, BLOCKS: tl.constexpr):
    """Encode the WIDTH channels ``src[c * stride_src]`` as channels START.. of the D-wide nvfp4 row at ``dst``; returns the segment's row scale."""
    blocks = tl.arange(0, BLOCKS)
    dims = blocks[:, None] * 16 + tl.arange(0, 16)[None, :]
    x = tl.load(src + dims * stride_src, mask=dims < WIDTH, other=0.0).to(tl.float32)
    amax = tl.max(tl.abs(x), axis=1)
    # 6 * 448: the largest e2m1 code times the largest e4m3 block scale
    row_scale = tl.maximum(tl.max(amax, axis=0), 1e-10) / 2688.0
    block_scale = round_e4m3(tl.minimum(tl.div_rn(amax, 6.0 * row_scale), 448.0))
    # quantize against the block scale as stored, e4m3 rounding and underflow included
    denom = tl.where(block_scale > 0, block_scale * row_scale, 1.0)
    normalized = tl.where(block_scale[:, None] > 0, tl.div_rn(x, denom[:, None]), 0.0)
    lo, hi = tl.split(_encode_e2m1(normalized).reshape(BLOCKS, 8, 2))
    byte_dims = blocks[:, None] * 8 + tl.arange(0, 8)[None, :]
    tl.store(dst + START // 2 + byte_dims, (lo | (hi << 4)).to(tl.uint8), mask=byte_dims < WIDTH // 2)
    tl.store(dst + D // 2 + START // 16 + blocks, e4m3_f32_to_u8(block_scale), mask=blocks < WIDTH // 16)
    return row_scale


def kv_scale_args(
    kv_format: KVFormat,
    k_cache: torch.Tensor,
    v_cache: torch.Tensor,
    k_scale: torch.Tensor | None,
    v_scale: torch.Tensor | None,
    placeholder: torch.Tensor,
    shape: tuple[int, int] | None = None,
) -> tuple[torch.Tensor, torch.Tensor, int, int]:
    """Scale pointers and slot strides for a launch; a format without scales never reads them. ``shape`` is ``(slots, heads)`` when the caches are paged."""
    if not kv_format.quantized:
        assert k_cache.is_floating_point() and v_cache.is_floating_point()
        return placeholder, placeholder, 0, 0
    assert k_cache.dtype == v_cache.dtype == kv_format.elem_store_dtype
    assert k_scale.dtype == v_scale.dtype == kv_format.scale_store_dtype
    shape = tuple(k_cache.shape[:2]) if shape is None else shape
    assert tuple(k_scale.shape[:2]) == tuple(v_scale.shape[:2]) == shape
    assert k_scale.stride(1) == v_scale.stride(1) == 1
    return k_scale, v_scale, k_scale.stride(0), v_scale.stride(0)


@triton.jit
def _encode_row(x, FMT: tl.constexpr):
    amax = tl.maximum(tl.max(tl.abs(x), axis=0), 1e-10)
    if FMT == "fp8_per_token_head":
        scale = amax / 448.0
        q = tl.clamp(x / scale, -448.0, 448.0)
        if e4m3_native_cx():
            codes = f32_to_e4m3(q).to(tl.uint8, bitcast=True)
        else:
            codes = e4m3_f32_to_u8(round_e4m3(q))
    elif FMT == "int8_per_token_head":
        scale = amax / 127.0
        q = x / scale
        # the int8 cast truncates, so round half away from zero first
        codes = tl.clamp(tl.where(q >= 0, q + 0.5, q - 0.5), -128.0, 127.0).to(tl.int8)
    return codes, scale


@triton.jit
def _kv_store_kernel(
    k_src,
    v_src,
    k_dst,
    v_dst,
    k_scale_dst,
    v_scale_dst,
    slots,
    stride_kt,
    stride_vt,
    stride_kd,
    stride_vd,
    stride_ks,
    stride_vs,
    D: tl.constexpr,
    BLOCK_D: tl.constexpr,
    FMT: tl.constexpr,
):
    token = tl.program_id(0)
    head = tl.program_id(1)
    slot = tl.load(slots + token).to(tl.int64)
    offs = tl.arange(0, BLOCK_D)
    mask = offs < D
    row = head * D + offs

    k_row = tl.load(k_src + token * stride_kt + row, mask=mask, other=0.0).to(tl.float32)
    v_row = tl.load(v_src + token * stride_vt + row, mask=mask, other=0.0).to(tl.float32)
    k_codes, k_scale = _encode_row(k_row, FMT)
    v_codes, v_scale = _encode_row(v_row, FMT)

    tl.store(k_dst + slot * stride_kd + row, k_codes, mask=mask)
    tl.store(v_dst + slot * stride_vd + row, v_codes, mask=mask)
    tl.store(k_scale_dst + slot * stride_ks + head, k_scale)
    tl.store(v_scale_dst + slot * stride_vs + head, v_scale)


@triton.jit
def _kv_store_nvfp4_kernel(
    k_src, v_src, k_dst, v_dst, k_scale_dst, v_scale_dst, slots,
    stride_kt, stride_vt, stride_kd, stride_vd, stride_ks, stride_vs,
    D: tl.constexpr,
    E: tl.constexpr,
    BLOCKS: tl.constexpr,
):
    token = tl.program_id(0)
    head = tl.program_id(1)
    slot = tl.load(slots + token).to(tl.int64)
    k_scale = _store_nvfp4_segment(k_src + token * stride_kt + head * D, 1, k_dst + slot * stride_kd + head * E, 0, D, D, BLOCKS)
    v_scale = _store_nvfp4_segment(v_src + token * stride_vt + head * D, 1, v_dst + slot * stride_vd + head * E, 0, D, D, BLOCKS)
    tl.store(k_scale_dst + slot * stride_ks + head, k_scale)
    tl.store(v_scale_dst + slot * stride_vs + head, v_scale)


@triton.jit
def _latent_store_nvfp4_kernel(
    c_src, r_src, dst, scale_dst, slots,
    stride_ct, stride_cd, stride_rt, stride_rd, stride_d, stride_s,
    D_V: tl.constexpr,
    D_R: tl.constexpr,
    BLOCKS_V: tl.constexpr,
    BLOCKS_R: tl.constexpr,
):
    token = tl.program_id(0)
    slot = tl.load(slots + token).to(tl.int64)
    row = dst + slot * stride_d
    tl.store(scale_dst + slot * stride_s, _store_nvfp4_segment(c_src + token * stride_ct, stride_cd, row, 0, D_V, D_V + D_R, BLOCKS_V))
    if D_R > 0:
        tl.store(
            scale_dst + slot * stride_s + 1,
            _store_nvfp4_segment(r_src + token * stride_rt, stride_rd, row, D_V, D_R, D_V + D_R, BLOCKS_R),
        )


def store_kv_rows(
    fmt: KVFormat,
    k: torch.Tensor,
    v: torch.Tensor,
    out_loc: torch.Tensor,
    k_cache: torch.Tensor,
    v_cache: torch.Tensor,
    k_scale: torch.Tensor,
    v_scale: torch.Tensor,
) -> None:
    """Quantize ``[tokens, heads * head_dim]`` K and V rows and write codes and scales to the ``out_loc`` slots."""
    tokens = k.shape[0]
    if tokens == 0:
        return
    _, heads, elem_dim = k_cache.shape
    head_dim = k.shape[1] // heads
    assert elem_dim == fmt.elem_dim(head_dim), (elem_dim, head_dim, fmt.name)
    assert k.shape == v.shape == (tokens, heads * head_dim), (k.shape, v.shape, heads, head_dim)
    assert k.stride(1) == v.stride(1) == 1 and k_cache.stride(1) == v_cache.stride(1) == elem_dim
    assert k_cache.dtype == v_cache.dtype == fmt.elem_store_dtype
    assert k_scale.dtype == v_scale.dtype == fmt.scale_store_dtype
    assert k_scale.shape[:2] == k_cache.shape[:2] and v_scale.shape[:2] == v_cache.shape[:2]
    assert k_scale.stride(1) == v_scale.stride(1) == 1
    if fmt.name == "nvfp4":
        _kv_store_nvfp4_kernel[(tokens, heads)](
            k, v, k_cache, v_cache, k_scale, v_scale, out_loc,
            k.stride(0), v.stride(0), k_cache.stride(0), v_cache.stride(0), k_scale.stride(0), v_scale.stride(0),
            D=head_dim, E=elem_dim, BLOCKS=triton.next_power_of_2(max(head_dim // 16, 1)),
            # the encoder divides by the scale it stores; a fused multiply-add would round differently
            num_warps=1, enable_fp_fusion=False,
        )
        return
    _kv_store_kernel[(tokens, heads)](
        k,
        v,
        k_cache,
        v_cache,
        k_scale,
        v_scale,
        out_loc,
        k.stride(0),
        v.stride(0),
        k_cache.stride(0),
        v_cache.stride(0),
        k_scale.stride(0),
        v_scale.stride(0),
        D=head_dim,
        BLOCK_D=triton.next_power_of_2(head_dim),
        FMT=fmt.name,
        num_warps=1,
    )



@triton.jit
def _latent_store_kernel(
    c_src,
    r_src,
    dst,
    scale_dst,
    slots,
    stride_ct,
    stride_cd,
    stride_rt,
    stride_rd,
    stride_d,
    stride_s,
    D_V: tl.constexpr,
    D_R: tl.constexpr,
    BLOCK_V: tl.constexpr,
    BLOCK_R: tl.constexpr,
    FMT: tl.constexpr,
):
    token = tl.program_id(0)
    slot = tl.load(slots + token).to(tl.int64)
    offs_v = tl.arange(0, BLOCK_V)
    mask_v = offs_v < D_V
    latent = tl.load(c_src + token * stride_ct + offs_v * stride_cd, mask=mask_v, other=0.0).to(tl.float32)
    codes, scale = _encode_row(latent, FMT)
    tl.store(dst + slot * stride_d + offs_v, codes, mask=mask_v)
    tl.store(scale_dst + slot * stride_s, scale)
    if D_R > 0:
        offs_r = tl.arange(0, BLOCK_R)
        mask_r = offs_r < D_R
        rope = tl.load(r_src + token * stride_rt + offs_r * stride_rd, mask=mask_r, other=0.0).to(tl.float32)
        codes, scale = _encode_row(rope, FMT)
        tl.store(dst + slot * stride_d + D_V + offs_r, codes, mask=mask_r)
        tl.store(scale_dst + slot * stride_s + 1, scale)


def store_latent_rows(
    fmt: KVFormat,
    c_kv: torch.Tensor,
    k_rope: torch.Tensor,
    out_loc: torch.Tensor,
    rows: torch.Tensor,
    scale: torch.Tensor,
) -> None:
    """Quantize MLA latent rows ``c_kv | k_rope`` into the ``[slots, latent_dim]`` pool, each part with its own scale."""
    tokens = c_kv.shape[0]
    if tokens == 0:
        return
    d_v, d_r = c_kv.shape[-1], k_rope.shape[-1]
    assert k_rope.shape[0] == tokens and rows.shape[1] == fmt.elem_dim(d_v + d_r) and rows.stride(1) == 1
    assert rows.dtype == fmt.elem_store_dtype and scale.dtype == fmt.scale_store_dtype
    assert scale.shape == (rows.shape[0], 2) and scale.stride(1) == 1
    if fmt.name == "nvfp4":
        assert d_v % 16 == 0 and d_r % 16 == 0, (d_v, d_r)
        _latent_store_nvfp4_kernel[(tokens,)](
            c_kv, k_rope, rows, scale, out_loc,
            c_kv.stride(0), c_kv.stride(1), k_rope.stride(0), k_rope.stride(1), rows.stride(0), scale.stride(0),
            D_V=d_v, D_R=d_r, BLOCKS_V=triton.next_power_of_2(max(d_v // 16, 1)), BLOCKS_R=triton.next_power_of_2(max(d_r // 16, 1)),
            num_warps=1, enable_fp_fusion=False,
        )
        return
    _latent_store_kernel[(tokens,)](
        c_kv,
        k_rope,
        rows,
        scale,
        out_loc,
        c_kv.stride(0),
        c_kv.stride(1),
        k_rope.stride(0),
        k_rope.stride(1),
        rows.stride(0),
        scale.stride(0),
        D_V=d_v,
        D_R=d_r,
        BLOCK_V=triton.next_power_of_2(d_v),
        BLOCK_R=triton.next_power_of_2(max(d_r, 1)),
        FMT=fmt.name,
        num_warps=1,
    )
