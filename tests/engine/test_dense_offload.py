"""--dense-offload-layers: layer choice, ``auto`` sizing, and the offloader itself (eager and inside
a CUDA graph, against the same stack kept resident)."""

from __future__ import annotations

import pytest
import torch

from freetoken.engine.dense_offload import auto_count, parse_count, pick_layers
from freetoken.layers import BaseOP
from freetoken.layers.base import OPList


def test_pick_layers_spreads_and_skips_layer_zero():
    assert pick_layers(64, 8) == [7, 14, 21, 28, 35, 42, 49, 56]
    assert pick_layers(10, 0) == []
    assert pick_layers(4, 10) == [1, 2, 3]  # never more than all but layer 0
    for n, c in ((64, 16), (48, 5), (7, 3)):
        ids = pick_layers(n, c)
        assert len(ids) == c and 0 not in ids and ids == sorted(set(ids))


def test_auto_count_is_the_fewest_layers_that_fit():
    sizes = [100] * 10
    # offloading c layers frees 100 c minus two 100-byte staging buffers
    assert auto_count(sizes, lambda freed: freed >= 0) == 0
    assert auto_count(sizes, lambda freed: freed >= 300) == 5
    with pytest.raises(ValueError, match="--kv-reserve-tokens"):
        auto_count(sizes, lambda freed: freed >= 10_000)


def test_parse_count():
    assert parse_count("0") == 0 and parse_count("12") == 12 and parse_count(3) == 3
    assert parse_count("auto") is None and parse_count(" AUTO ") is None
    with pytest.raises(ValueError):
        parse_count("0.5")


class _Norm(BaseOP):
    def __init__(self, dim: int):
        self.weight = torch.randn(dim, device="cuda", dtype=torch.bfloat16)  # < 1 MiB: stays resident

    def forward(self, x):
        return x * self.weight


class _Layer(BaseOP):
    def __init__(self, dim: int):
        self.w_in = torch.randn(dim, dim, device="cuda", dtype=torch.bfloat16) / dim ** 0.5
        self.w_out = torch.randn(dim, dim, device="cuda", dtype=torch.bfloat16) / dim ** 0.5
        self.norm = _Norm(dim)

    def forward(self, x):
        return x + torch.relu(self.norm.forward(x) @ self.w_in.T) @ self.w_out.T


class _Inner(BaseOP):
    def __init__(self, n: int, dim: int):
        self.layers = OPList([_Layer(dim) for _ in range(n)])

    def forward(self, x):
        for layer in self.layers.op_list:
            x = layer.forward(x)
        return x


class _Model(BaseOP):
    def __init__(self, n: int, dim: int):
        self.model = _Inner(n, dim)

    def forward(self, x):
        return self.model.forward(x)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")
def test_offloaded_stack_matches_resident_eager_and_in_a_graph():
    from freetoken.engine.dense_offload import DenseLayerOffloader, decoder_layers

    torch.manual_seed(0)
    dim, n = 1024, 7
    model = _Model(n, dim)
    x = torch.randn(4, dim, device="cuda", dtype=torch.bfloat16)
    want = model.forward(x)
    torch.cuda.synchronize()
    before = torch.cuda.memory_allocated()

    layers = decoder_layers(model)
    off = DenseLayerOffloader(layers, pick_layers(n, 3), torch.device("cuda"))
    torch.cuda.synchronize()
    # three layers of 2 x 2 MiB moved, two 4 MiB staging buffers added; the 2 KiB norms stay
    assert off.host_bytes == 3 * 2 * dim * dim * 2
    assert before - torch.cuda.memory_allocated() == off.host_bytes - off.device_bytes
    assert layers[off.offload_ids[0]].norm.weight.is_cuda
    assert layers[off.offload_ids[0]].w_in.data_ptr() == off.staging[0].data_ptr()

    assert torch.equal(model.forward(x), want)  # eager, twice: the staging buffers are reused
    assert torch.equal(model.forward(x), want)

    stream = torch.cuda.Stream()
    with torch.cuda.stream(stream):
        model.forward(x)  # warm-up on the capture stream
    torch.cuda.current_stream().wait_stream(stream)
    graph = torch.cuda.CUDAGraph()
    with torch.cuda.graph(graph):
        out = model.forward(x)
    for _ in range(3):
        graph.replay()
        torch.cuda.synchronize()
        assert torch.equal(out, want)
    assert torch.equal(model.forward(x), want)  # eager again after replays


@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")
def test_decoder_layers_needs_a_model_layers_stack():
    from freetoken.engine.dense_offload import decoder_layers

    class _Flat(BaseOP):
        def forward(self, x):
            return x

    with pytest.raises(ValueError, match="model.layers"):
        decoder_layers(_Flat())
