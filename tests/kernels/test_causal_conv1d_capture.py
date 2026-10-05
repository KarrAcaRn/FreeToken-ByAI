"""The varlen GDN conv must be CUDA-graph capturable: its ``max_seq_len`` is host-known
metadata everywhere the scheduler calls it, and deriving it on device costs a D2H sync that
is illegal inside a capture region."""

from __future__ import annotations

import pytest
import torch

from freetoken.kernel.causal_conv1d import causal_conv1d_varlen

requires_cuda = pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA is required")


def _conv_inputs(device, *, lens=(4, 2), conv_dim=8, kernel=4):
    total = sum(lens)
    cu = torch.tensor([0, *lens], dtype=torch.int32).cumsum(0).to(torch.int32).to(device)
    return dict(
        x=torch.randn(conv_dim, total, device=device, dtype=torch.bfloat16),
        weight=torch.randn(conv_dim, kernel, device=device, dtype=torch.bfloat16),
        conv_states=torch.randn(
            len(lens) + 1, conv_dim, kernel - 1, device=device, dtype=torch.bfloat16
        ),
        cu_seqlens=cu,
        cache_indices=torch.arange(1, len(lens) + 1, dtype=torch.int32, device=device),
        has_initial_state=torch.ones(len(lens), dtype=torch.bool, device=device),
    )


def _call(inputs, **extra):
    return causal_conv1d_varlen(
        inputs["x"],
        inputs["weight"],
        inputs["conv_states"],
        inputs["cu_seqlens"],
        inputs["cache_indices"],
        inputs["has_initial_state"],
        **extra,
    )


@requires_cuda
def test_varlen_conv_skips_the_device_to_host_sync_when_max_seq_len_is_given(monkeypatch):
    device = torch.device("cuda")
    inputs = _conv_inputs(device)
    original_item = torch.Tensor.item
    calls = []

    def counted_item(self):
        calls.append(tuple(self.shape))
        return original_item(self)

    monkeypatch.setattr(torch.Tensor, "item", counted_item)

    _call(inputs, max_seq_len=4)
    torch.cuda.synchronize()

    assert calls == []


@requires_cuda
def test_varlen_conv_still_derives_max_seq_len_on_device_by_default(monkeypatch):
    import freetoken.kernel.backend as _backend

    device = torch.device("cuda")
    inputs = _conv_inputs(device)
    original_item = torch.Tensor.item
    calls = []

    def counted_item(self):
        calls.append(tuple(self.shape))
        return original_item(self)

    # The sync this asserts on lives in the triton fallback; on an install with sgl_kernel
    # the native kernel needs no max_seq_len and calls no .item(). Force the fallback so the
    # test proves the claim on any install rather than only where the fallback is selected.
    monkeypatch.setattr(_backend, "is_sgl_kernel_installed", lambda: False)
    monkeypatch.setattr(torch.Tensor, "item", counted_item)

    _call(inputs)
    torch.cuda.synchronize()

    assert calls, "the default path must still work without host-side metadata"


@requires_cuda
def test_varlen_conv_with_host_metadata_matches_the_device_derived_result():
    device = torch.device("cuda")
    inputs = _conv_inputs(device)
    baseline_states = inputs["conv_states"].clone()
    # sgl_kernel convolves ``x`` in place (the triton fallback returns a fresh tensor), so
    # both inputs have to be reset between the two calls being compared.
    baseline_x = inputs["x"].clone()

    device_derived = _call(inputs).clone()
    device_states = inputs["conv_states"].clone()

    inputs["conv_states"].copy_(baseline_states)
    inputs["x"].copy_(baseline_x)
    host_known = _call(inputs, max_seq_len=4).clone()

    assert torch.equal(host_known, device_derived)
    assert torch.equal(inputs["conv_states"], device_states)


@requires_cuda
def test_varlen_conv_replays_inside_a_cuda_graph():
    device = torch.device("cuda")
    inputs = _conv_inputs(device)
    baseline_states = inputs["conv_states"].clone()
    baseline_x = inputs["x"].clone()

    def reset():
        inputs["conv_states"].copy_(baseline_states)
        inputs["x"].copy_(baseline_x)  # sgl_kernel mutates x in place; the fallback does not

    expected = _call(inputs, max_seq_len=4).clone()
    expected_states = inputs["conv_states"].clone()

    stream = torch.cuda.Stream()
    stream.wait_stream(torch.cuda.current_stream())
    with torch.cuda.stream(stream):
        for _ in range(3):
            reset()
            _call(inputs, max_seq_len=4)
    torch.cuda.current_stream().wait_stream(stream)
    torch.cuda.synchronize()

    graph = torch.cuda.CUDAGraph()
    reset()
    with torch.cuda.graph(graph, stream=stream, capture_error_mode="thread_local"):
        captured = _call(inputs, max_seq_len=4)
    reset()
    graph.replay()
    torch.cuda.synchronize()

    assert torch.equal(captured, expected)
    assert torch.equal(inputs["conv_states"], expected_states)


def test_prefill_fla_metadata_carries_the_host_known_longest_extend_len():
    from freetoken.attention.linear import build_fla_metadata
    from freetoken.core import Batch, Req, SamplingParams

    reqs = []
    for index, length in enumerate((5, 2, 9)):
        req = Req(
            input_ids=torch.arange(length, dtype=torch.int32),
            table_idx=index,
            cached_len=0,
            output_len=1,
            uid=index,
            sampling_params=SamplingParams(),
            cache_handle=None,
        )
        req.linear_slot_idx = index + 1
        reqs.append(req)
    batch = Batch(reqs=reqs, phase="prefill")
    batch.padded_reqs = batch.reqs

    fla = build_fla_metadata(batch, torch.device("cpu"))

    assert fla.max_seq_len == 9


@requires_cuda
def test_split_conv_matches_the_channels_first_conv():
    """GDN prefill convolves the token-major qkvz slice straight into contiguous q/k/v; it must
    equal the channels-first triton conv (same fp32 math) and leave the same conv states."""
    from freetoken.kernel.triton.causal_conv1d_triton import (
        causal_conv1d_varlen as triton_conv,
        causal_conv1d_varlen_split,
    )

    torch.manual_seed(0)
    lens, conv_dim, split = (37, 2, 300), 448, 128  # a 1-token-short request keeps state history
    total = sum(lens)
    qkvz = torch.randn(total, conv_dim + 96, device="cuda", dtype=torch.bfloat16)
    x = qkvz[:, :conv_dim]
    weight = torch.randn(conv_dim, 4, device="cuda", dtype=torch.bfloat16)
    states = torch.randn(5, conv_dim, 3, device="cuda", dtype=torch.bfloat16)
    cu = torch.tensor([0, *lens], dtype=torch.int32).cumsum(0).to(torch.int32).cuda()
    idx = torch.tensor([3, 1, 4], dtype=torch.int32, device="cuda")
    init = torch.tensor([True, True, False], device="cuda")

    ref_states = states.clone()
    ref = triton_conv(x.t().contiguous(), weight, ref_states, cu, idx, init, max_seq_len=max(lens)).t()
    q, k, v = causal_conv1d_varlen_split(x, weight, states, cu, idx, init, split, max_seq_len=max(lens))

    assert q.is_contiguous() and k.is_contiguous() and v.is_contiguous()
    assert torch.equal(torch.cat([q, k, v], dim=1), ref)
    assert torch.equal(states, ref_states)
