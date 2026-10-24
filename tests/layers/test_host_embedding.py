"""--embed-weights host: the lookup reads a pinned host table zero-copy and matches the on-device table."""

from __future__ import annotations

import pytest
import torch

pytestmark = pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")


def _tp(monkeypatch, rank: int, size: int):
    import freetoken.layers.embedding as emb_mod
    from freetoken.distributed import DistributedInfo

    tp_info = DistributedInfo(rank=rank, size=size)
    monkeypatch.setattr(emb_mod, "get_tp_info", lambda: tp_info)


def _embedding(vocab, dim, dtype, *, embed_scale=None):
    from freetoken.layers.embedding import VocabParallelEmbedding

    emb = VocabParallelEmbedding(vocab, dim, embed_scale=embed_scale)
    emb.weight = torch.randn(emb.num_embeddings_tp, dim, dtype=dtype, device="cuda")
    return emb


def _pin(emb) -> torch.Tensor:
    from freetoken.kernel.pinned import alloc_pinned_tensor

    device_table = emb.weight
    emb.weight = alloc_pinned_tensor(*device_table.shape, dtype=device_table.dtype)
    emb.weight.copy_(device_table)
    return device_table


@pytest.mark.parametrize("dtype", [torch.bfloat16, torch.float16, torch.float32])
@pytest.mark.parametrize("dim", [64, 2880, 5120, 10752])
@pytest.mark.parametrize("embed_scale", [None, 45.25])
def test_host_table_matches_device(monkeypatch, dtype, dim, embed_scale):
    _tp(monkeypatch, 0, 1)
    emb = _embedding(517, dim, dtype, embed_scale=embed_scale)
    ids = torch.tensor([0, 5, 516, 5, 300], device="cuda")
    ref = emb.forward(ids)
    emb._embed_scale_t = None
    _pin(emb)
    assert not emb.weight.is_cuda and emb.weight.is_pinned()
    assert torch.equal(emb.forward(ids), ref)


def test_host_table_tp_shard(monkeypatch):
    # rank 1 of 2 holds rows [2050, 4099); other ids contribute zeros before the all-reduce
    _tp(monkeypatch, 1, 2)
    emb = _embedding(4099, 128, torch.bfloat16)
    full = _pin(emb)
    ids = torch.tensor([0, 2049, 2050, 3000, 4098], device="cuda")
    out = emb.quant_method.embed(emb, ids)
    assert torch.count_nonzero(out[:2]) == 0
    assert torch.equal(out[2:], full[ids[2:] - 2050])


def test_host_lookup_replays_in_cuda_graph(monkeypatch):
    _tp(monkeypatch, 0, 1)
    emb = _embedding(1000, 512, torch.bfloat16)
    ref_table = _pin(emb)
    ids = torch.zeros(8, dtype=torch.long, device="cuda")
    emb.forward(ids)  # compile outside capture
    graph = torch.cuda.CUDAGraph()
    with torch.cuda.graph(graph):
        out = emb.forward(ids)
    ids.copy_(torch.arange(100, 108))
    graph.replay()
    torch.cuda.synchronize()
    assert torch.equal(out, ref_table[100:108])


def test_tied_tables_stay_on_the_gpu(monkeypatch):
    from freetoken.layers.base import BaseOP, OPList
    from freetoken.layers.embedding import ParallelLMHead, host_movable_embeddings

    _tp(monkeypatch, 0, 1)

    # a bare head carrying only the tie: the quant method is not under test
    monkeypatch.setattr(ParallelLMHead, "__init__", lambda self, tied: setattr(self, "tied_embedding", tied))

    class Inner(BaseOP):
        def __init__(self):
            self.embed_tokens = _embedding(64, 32, torch.bfloat16)
            self.per_layer = OPList([_embedding(16, 32, torch.bfloat16)])

    class Model(BaseOP):
        def __init__(self, tie):
            self.model = Inner()
            self.lm_head = ParallelLMHead(self.model.embed_tokens if tie else None)

    untied = Model(tie=False)
    assert host_movable_embeddings(untied) == [untied.model.embed_tokens, untied.model.per_layer.op_list[0]]
    # gemma4 E-series: the main table is tied, its per-layer table still moves
    tied = Model(tie=True)
    assert host_movable_embeddings(tied) == [tied.model.per_layer.op_list[0]]
