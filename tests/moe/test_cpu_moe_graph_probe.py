"""ROCm CPU-MoE graph probe (CpuMoeExecutor._check_hip_graph_capture) without a GPU.

CPU-only: torch.cuda's stream/graph API is replaced by a recorder whose replay re-runs the
captured ops, and the executor's submit/sync by a CPU stand-in, so the probe's decision logic
(accumulate-path comparison, error handling) runs here.
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace

import pytest
import torch

from freetoken.moe import cpu_executor
from freetoken.moe.cpu_executor import CpuMoeExecutor


class _Stream:
    def wait_stream(self, other):
        pass

    def synchronize(self):
        pass


class _Graph:
    def __init__(self):
        self.nodes = []

    def replay(self):
        for node in self.nodes:
            node()


@pytest.fixture
def fake_cuda(monkeypatch):
    state = SimpleNamespace(current=_Stream(), capturing=None, synchronized=0)
    default = state.current

    @contextlib.contextmanager
    def stream(s):
        prev, state.current = state.current, s
        try:
            yield
        finally:
            state.current = prev

    @contextlib.contextmanager
    def graph(g, stream=None):
        prev, state.current = state.current, stream or state.current
        state.capturing = g
        try:
            yield
        finally:
            state.capturing = None
            state.current = prev

    def synchronize(device=None):
        state.synchronized += 1

    monkeypatch.setattr(torch.version, "hip", "7.14.0", raising=False)
    monkeypatch.setattr(torch.cuda, "Stream", _Stream)
    monkeypatch.setattr(torch.cuda, "current_stream", lambda device=None: state.current)
    monkeypatch.setattr(torch.cuda, "stream", stream)
    monkeypatch.setattr(torch.cuda, "CUDAGraph", _Graph)
    monkeypatch.setattr(torch.cuda, "graph", graph)
    monkeypatch.setattr(torch.cuda, "is_current_stream_capturing", lambda: state.capturing is not None)
    monkeypatch.setattr(torch.cuda, "synchronize", synchronize)
    state.default = default
    return state


def _compute(layer, hidden, weights, ids):
    return (hidden.float() * (weights * (ids >= 0)).sum(-1, keepdim=True) + layer).bfloat16()


def _executor(state, monkeypatch, *, fault=None):
    """An executor shell whose submit/sync run on the CPU and are recorded while capturing."""
    ex = object.__new__(CpuMoeExecutor)
    ex.H, ex.top_k, ex.num_experts, ex.num_layers = 16, 2, 4, 2
    ex.max_tokens = 1
    ex.device = torch.device("cpu")
    ex._flag_sync = ex._kernel_io = True
    ex._unhealthy = False
    ex._graph_capture_safe = True

    def run(op):
        if state.capturing is not None:
            state.capturing.nodes.append(op)
        else:
            op()

    def decode_submit(layer, hidden, weights, ids):
        if fault == "raise" and state.capturing is not None:
            raise RuntimeError("hipErrorStreamCaptureInvalidated")
        out = torch.empty_like(hidden)
        run(lambda: out.copy_(_compute(layer, hidden, weights, ids)))
        return (out,)

    def decode_sync(pending, add_to=None):
        (out,) = pending
        if add_to is None:
            return out
        if fault == "accumulate" and state.capturing is not None:
            # A stale combine: overwrites the GPU partial sum instead of adding to it.
            run(lambda: add_to.copy_(out))
        else:
            run(lambda: add_to.add_(out))
        return add_to

    ex.decode_submit = decode_submit
    ex.decode_sync = decode_sync
    warnings = []
    monkeypatch.setattr(cpu_executor, "logger", SimpleNamespace(warning_rank0=warnings.append))
    return ex, warnings


def test_graph_probe_accepts_matching_graph(fake_cuda, monkeypatch):
    ex, warnings = _executor(fake_cuda, monkeypatch)
    ex._check_hip_graph_capture()
    assert ex.graph_capture_safe(torch.bfloat16)
    assert warnings == []


def test_graph_probe_rejects_accumulate_mismatch(fake_cuda, monkeypatch):
    ex, warnings = _executor(fake_cuda, monkeypatch, fault="accumulate")
    ex._check_hip_graph_capture()
    assert not ex.graph_capture_safe(torch.bfloat16)
    assert len(warnings) == 1 and "add_to combine differs from eager" in warnings[0]


def test_graph_probe_error_disables_graphs_and_keeps_eager(fake_cuda, monkeypatch):
    ex, warnings = _executor(fake_cuda, monkeypatch, fault="raise")
    ex._check_hip_graph_capture()
    assert not ex.graph_capture_safe(torch.bfloat16)
    assert len(warnings) == 1
    assert "capture/replay raised RuntimeError: hipErrorStreamCaptureInvalidated" in warnings[0]
    assert "using eager decode" in warnings[0]
    assert fake_cuda.capturing is None and fake_cuda.current is fake_cuda.default
    assert fake_cuda.synchronized == 1

    hidden = torch.randn(1, ex.H).bfloat16()
    weights = torch.tensor([[0.25, 0.75]])
    ids = torch.tensor([[1, -1]], dtype=torch.int32)
    assert torch.equal(ex.decode(1, hidden, weights, ids), _compute(1, hidden, weights, ids))


def test_graph_probe_error_after_watchdog_still_fails(fake_cuda, monkeypatch):
    ex, warnings = _executor(fake_cuda, monkeypatch)

    def wedged():
        ex._unhealthy = True
        raise RuntimeError("doorbell never answered")

    ex._probe_kernel_graph_io = wedged
    with pytest.raises(RuntimeError, match="doorbell never answered"):
        ex._check_hip_graph_capture()
    assert warnings == []
