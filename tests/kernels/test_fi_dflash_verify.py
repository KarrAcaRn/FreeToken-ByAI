"""DFlash target-verify CUDA graphs on the FlashInfer backend: a graph captured on dummy
requests, re-planned for real ones, must attend exactly like the eager extend path."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
import torch

pytest.importorskip("flashinfer")
pytestmark = pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")

NUM_PAGES, QO_HEADS, KV_HEADS, HEAD_DIM = 1024, 8, 2, 128


class _FakeKVCache:
    def __init__(self, device: torch.device):
        self.device = device
        self.dtype = torch.bfloat16
        shape = (NUM_PAGES, 1, KV_HEADS, HEAD_DIM)
        self.k = torch.randn(shape, dtype=self.dtype, device=device)
        self.v = torch.randn(shape, dtype=self.dtype, device=device)

    def store_kv(self, k, v, out_loc, layer_id):
        self.k[out_loc.long()] = k.view(-1, 1, KV_HEADS, HEAD_DIM)
        self.v[out_loc.long()] = v.view(-1, 1, KV_HEADS, HEAD_DIM)

    def k_cache(self, layer_id):
        return self.k

    def v_cache(self, layer_id):
        return self.v


def _backend(monkeypatch):
    from freetoken.attention.fi import FlashInferBackend

    device = torch.device("cuda")
    kv_cache = _FakeKVCache(device)
    page_table = torch.randperm(NUM_PAGES, device=device).to(torch.int32).view(4, -1)
    ctx = SimpleNamespace(kv_cache=kv_cache, page_table=page_table)
    monkeypatch.setattr("freetoken.attention.fi.get_global_ctx", lambda: ctx)
    monkeypatch.setattr("freetoken.attention.fi.get_tp_info", lambda: SimpleNamespace(size=1))
    config = SimpleNamespace(num_qo_heads=QO_HEADS, num_kv_heads=KV_HEADS, head_dim=HEAD_DIM)
    return FlashInferBackend(config), kv_cache, page_table


def _verify_batch(page_table, prefixes: list[int], verify_len: int):
    reqs = [
        SimpleNamespace(table_idx=i, cached_len=c, device_len=c + verify_len, extend_len=verify_len)
        for i, c in enumerate(prefixes)
    ]
    out_loc = torch.cat([page_table[r.table_idx, r.cached_len : r.device_len] for r in reqs])
    return SimpleNamespace(
        reqs=reqs, padded_reqs=reqs, size=len(reqs), is_decode=False, out_loc=out_loc, attn_metadata=None,
    )


def _reference(q, kv_cache, page_table, prefixes, verify_len):
    group = QO_HEADS // KV_HEADS
    outs = []
    for b, c in enumerate(prefixes):
        slots = page_table[b, : c + verify_len].long()
        k = kv_cache.k[slots, 0].float().repeat_interleave(group, dim=1)  # [kv, heads, d]
        v = kv_cache.v[slots, 0].float().repeat_interleave(group, dim=1)
        qb = q[b * verify_len : (b + 1) * verify_len].float()
        scores = torch.einsum("qhd,khd->hqk", qb, k) / HEAD_DIM**0.5
        q_pos = torch.arange(c, c + verify_len, device=q.device)[:, None]
        mask = torch.arange(c + verify_len, device=q.device)[None, :] <= q_pos
        scores = scores.masked_fill(~mask[None], float("-inf"))
        outs.append(torch.einsum("hqk,khd->qhd", scores.softmax(-1), v))
    return torch.cat(outs).to(q.dtype)


@pytest.mark.parametrize("bs", [1, 3])
def test_fi_dflash_verify_graph_matches_eager_extend(monkeypatch, bs):
    backend, kv_cache, page_table = _backend(monkeypatch)
    verify_len, max_seq_len = 8, page_table.shape[1]
    backend.init_dflash_target_verify_capture_graph(max_seq_len, [(bs, verify_len)])
    rows = bs * verify_len
    device = kv_cache.device
    q = torch.zeros(rows, QO_HEADS, HEAD_DIM, dtype=torch.bfloat16, device=device)
    k = torch.zeros(rows, KV_HEADS, HEAD_DIM, dtype=torch.bfloat16, device=device)
    v = torch.zeros_like(k)
    out_loc = torch.zeros(rows, dtype=torch.int32, device=device)

    capture_batch = SimpleNamespace(size=bs, out_loc=out_loc, attn_metadata=None)
    backend.prepare_for_dflash_target_verify_capture(capture_batch, verify_len)
    backend.forward(q, k, v, 0, capture_batch)
    torch.cuda.synchronize()
    graph = torch.cuda.CUDAGraph()
    with torch.cuda.graph(graph):
        out = backend.forward(q, k, v, 0, capture_batch)

    # the same graph serves verifies at different prefix lengths
    for prefixes in ([37, 200, 5][:bs], [130, 1, 240][:bs]):
        real_q = torch.randn_like(q)
        real_k, real_v = torch.randn_like(k), torch.randn_like(v)
        batch = _verify_batch(page_table, prefixes, verify_len)

        eager_batch = _verify_batch(page_table, prefixes, verify_len)
        backend.prepare_metadata(eager_batch)
        eager = backend.forward(real_q, real_k, real_v, 0, eager_batch)

        backend.prepare_metadata(batch)
        backend.prepare_for_dflash_target_verify_replay(batch, verify_len)
        q.copy_(real_q)
        k.copy_(real_k)
        v.copy_(real_v)
        out_loc.copy_(batch.out_loc)
        graph.replay()
        torch.cuda.synchronize()

        ref = _reference(real_q, kv_cache, page_table, prefixes, verify_len)
        # the graph plan splits the KV differently from the eager one: close, not bitwise
        torch.testing.assert_close(out.float(), eager.float(), atol=2e-2, rtol=2e-2)
        torch.testing.assert_close(out.float(), ref.float(), atol=2e-2, rtol=2e-2)
