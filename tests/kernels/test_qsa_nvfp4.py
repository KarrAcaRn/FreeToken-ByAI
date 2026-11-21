"""QSA sparse attention over the packed NVFP4 KV tier."""

from __future__ import annotations

import pytest
import torch

from freetoken.kernel.triton.kv_rows import store_kv_rows
from freetoken.kernel.triton.qsa import qsa_sparse_paged_attention
from freetoken.kvcache.format import NVFP4

pytestmark = pytest.mark.skipif(
    not torch.cuda.is_available(), reason="Triton attention needs CUDA"
)

PAGE = 64
HEAD_DIM = 64
ROW = NVFP4.elem_dim(HEAD_DIM)


def _layout(rows: int, topk: int):
    block_table = torch.tensor(
        [[0, 1, 2], [2, 1, 0]], dtype=torch.int32, device="cuda"
    ).contiguous()
    indices = (
        torch.arange(topk, dtype=torch.int32, device="cuda")[None, :] + 32
    ).repeat(rows, 1).contiguous()
    token_to_req = torch.arange(rows, dtype=torch.int32, device="cuda") % 2
    return indices, block_table, token_to_req.contiguous()


def _store(k, v, kv_heads):
    slots = k.shape[0]
    k_rows = torch.zeros((slots, kv_heads, ROW), dtype=torch.uint8, device="cuda")
    v_rows = torch.zeros_like(k_rows)
    k_scale = torch.zeros((slots, kv_heads, 1), dtype=torch.float32, device="cuda")
    v_scale = torch.zeros_like(k_scale)
    out_loc = torch.arange(slots, dtype=torch.int32, device="cuda")
    store_kv_rows(NVFP4, k, v, out_loc, k_rows, v_rows, k_scale, v_scale)
    return k_rows, v_rows, k_scale, v_scale


def _decode(rows: torch.Tensor, row_scale: torch.Tensor):
    """Decode with torch, independently of the Triton read path under test."""
    codes, block = rows[..., : HEAD_DIM // 2], rows[..., HEAD_DIM // 2:]
    code = torch.stack(((codes & 15).long(), (codes >> 4).long()), dim=-1).flatten(-2)
    magnitude = torch.tensor(
        [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0], device=rows.device
    )[code & 7]
    value = torch.where(code < 8, magnitude, -magnitude)
    block = block.view(torch.float8_e4m3fn).to(torch.float32)
    return (value * block.repeat_interleave(16, dim=-1) * row_scale).to(torch.bfloat16)


@pytest.mark.parametrize(("rows", "kv_heads"), [(1, 1), (16, 2)])
def test_qsa_nvfp4_matches_its_bf16_decode(rows, kv_heads):
    """Page-table indirection must address the same packed slot, its block bytes and its row scale."""
    torch.manual_seed(19)
    pages, query_heads, slots = 3, 2 * kv_heads, 3 * PAGE
    k = torch.randn(slots, kv_heads * HEAD_DIM, device="cuda", dtype=torch.bfloat16)
    v = torch.randn_like(k) * 0.25
    k_rows, v_rows, k_scale, v_scale = _store(k, v, kv_heads)

    q = torch.randn(rows, query_heads, HEAD_DIM, device="cuda", dtype=torch.bfloat16)
    indices, block_table, token_to_req = _layout(rows, topk=64)
    packed_shape = (pages, PAGE, kv_heads, ROW)
    dense_shape = (pages, PAGE, kv_heads, HEAD_DIM)
    got = qsa_sparse_paged_attention(
        q, k_rows.view(packed_shape), v_rows.view(packed_shape), indices, block_table, token_to_req,
        kv_format=NVFP4, k_scale=k_scale, v_scale=v_scale,
    )
    want = qsa_sparse_paged_attention(
        q,
        _decode(k_rows, k_scale).view(dense_shape),
        _decode(v_rows, v_scale).view(dense_shape),
        indices,
        block_table,
        token_to_req,
    )
    # the kernel applies the row scales after its dots, the reference rounds them into bf16 first
    torch.testing.assert_close(got.float(), want.float(), atol=2e-2, rtol=2e-2)


def test_qsa_nvfp4_splitk_reads_value_rows():
    """A zero query makes the split-K result the selected V-row average."""
    torch.manual_seed(23)
    slots = 3 * PAGE
    v = torch.randn(slots, HEAD_DIM, device="cuda", dtype=torch.bfloat16)
    k_rows, v_rows, k_scale, v_scale = _store(v, v, 1)
    q = torch.zeros(1, 2, HEAD_DIM, device="cuda", dtype=torch.bfloat16)
    args = _layout(1, topk=64)
    packed = (3, PAGE, 1, ROW)
    got = qsa_sparse_paged_attention(
        q, k_rows.view(packed), v_rows.view(packed), *args,
        kv_format=NVFP4, k_scale=k_scale, v_scale=v_scale,
    )
    ref = _decode(v_rows, v_scale).view(3, PAGE, 1, HEAD_DIM)
    want = qsa_sparse_paged_attention(q, ref, ref, *args)
    torch.testing.assert_close(got.float(), want.float(), atol=1e-2, rtol=1e-2)
