"""The varlen GDN conv must be CUDA-graph capturable: its ``max_seq_len`` is host-known
metadata everywhere the scheduler calls it, and deriving it on device costs a D2H sync that
is illegal inside a capture region."""

from __future__ import annotations

from types import SimpleNamespace

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
@pytest.mark.parametrize("kernel,activation", [(4, "silu"), (7, None)])
def test_varlen_conv_skips_the_device_to_host_sync_when_max_seq_len_is_given(monkeypatch, kernel, activation):
    device = torch.device("cuda")
    inputs = _conv_inputs(device, kernel=kernel)
    original_item = torch.Tensor.item
    calls = []

    def counted_item(self):
        calls.append(tuple(self.shape))
        return original_item(self)

    monkeypatch.setattr(torch.Tensor, "item", counted_item)

    _call(inputs, max_seq_len=4, activation=activation)
    torch.cuda.synchronize()

    assert calls == []


@requires_cuda
@pytest.mark.parametrize("kernel,activation", [(4, "silu"), (7, None)])
def test_varlen_conv_still_derives_max_seq_len_on_device_by_default(monkeypatch, kernel, activation):
    import freetoken.kernel.backend as _backend

    device = torch.device("cuda")
    inputs = _conv_inputs(device, kernel=kernel)
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

    _call(inputs, activation=activation)
    torch.cuda.synchronize()

    assert calls, "the default path must still work without host-side metadata"


@requires_cuda
@pytest.mark.parametrize("kernel,activation", [(4, "silu"), (7, None)])
def test_varlen_conv_with_host_metadata_matches_the_device_derived_result(kernel, activation):
    device = torch.device("cuda")
    inputs = _conv_inputs(device, kernel=kernel)
    baseline_states = inputs["conv_states"].clone()
    # sgl_kernel convolves ``x`` in place (the triton fallback returns a fresh tensor), so
    # both inputs have to be reset between the two calls being compared.
    baseline_x = inputs["x"].clone()

    device_derived = _call(inputs, activation=activation).clone()
    device_states = inputs["conv_states"].clone()

    inputs["conv_states"].copy_(baseline_states)
    inputs["x"].copy_(baseline_x)
    host_known = _call(inputs, max_seq_len=4, activation=activation).clone()

    assert torch.equal(host_known, device_derived)
    assert torch.equal(inputs["conv_states"], device_states)


@requires_cuda
@pytest.mark.parametrize("kernel,activation", [(4, "silu"), (7, None)])
def test_varlen_conv_replays_inside_a_cuda_graph(kernel, activation):
    device = torch.device("cuda")
    inputs = _conv_inputs(device, kernel=kernel)
    baseline_states = inputs["conv_states"].clone()
    baseline_x = inputs["x"].clone()

    def reset():
        inputs["conv_states"].copy_(baseline_states)
        inputs["x"].copy_(baseline_x)  # sgl_kernel mutates x in place; the fallback does not

    expected = _call(inputs, max_seq_len=4, activation=activation).clone()
    expected_states = inputs["conv_states"].clone()

    stream = torch.cuda.Stream()
    stream.wait_stream(torch.cuda.current_stream())
    with torch.cuda.stream(stream):
        for _ in range(3):
            reset()
            _call(inputs, max_seq_len=4, activation=activation)
    torch.cuda.current_stream().wait_stream(stream)
    torch.cuda.synchronize()

    graph = torch.cuda.CUDAGraph()
    reset()
    with torch.cuda.graph(graph, stream=stream, capture_error_mode="thread_local"):
        captured = _call(inputs, max_seq_len=4, activation=activation)
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

    pool = SimpleNamespace(conv_states=torch.zeros(1, 1, 1, 3))
    fla = build_fla_metadata(batch, torch.device("cpu"), pool)

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


@requires_cuda
@pytest.mark.parametrize("kernel,activation", [(4, "silu"), (4, None), (7, None), (7, "silu")])
@pytest.mark.parametrize("initial", [False, True])
@pytest.mark.parametrize("dtype", [torch.bfloat16, torch.float32])
def test_slot_conv_matches_torch_across_short_chunks_and_decode(monkeypatch, kernel, activation, initial, dtype):
    """Guard tap order, short-chunk history, slot routing and accidental activation."""
    import torch.nn.functional as F
    import freetoken.kernel.backend as backend
    from freetoken.kernel.causal_conv1d import causal_conv1d_decode

    # Width 7 must bypass sgl even when it is reported installed.
    monkeypatch.setattr(backend, "is_sgl_kernel_installed", lambda: kernel == 7)
    torch.manual_seed(42)
    dim, history = 35, kernel - 1
    lens = (1, 2, 3, 4, 5, 137, 9)
    slots = (5, 2, 7, 1, 6, 3, -1)
    idx = torch.tensor(slots, device="cuda", dtype=torch.int32)
    cu = torch.tensor([0, *lens], dtype=torch.int32).cumsum(0).to(device="cuda", dtype=torch.int32)
    init = torch.tensor([initial and i < 5 for i in range(len(lens))], device="cuda")
    weight = torch.randn(dim, kernel, device="cuda", dtype=dtype)
    states = torch.randn(9, dim, history, device="cuda", dtype=dtype)
    expected_states = states.clone()
    # Strided views cover a token-major projection slice and a layer's state slab.
    states = torch.stack((states, states), dim=-1)[..., 0]
    x = torch.randn(sum(lens), dim + 3, device="cuda", dtype=dtype)[:, :dim].t()
    original_x = x.clone()
    expected = torch.zeros_like(x)
    offset = 0
    for row, (length, slot) in enumerate(zip(lens, slots)):
        if slot != -1:
            left = expected_states[slot] if initial and row < 5 else torch.zeros_like(expected_states[slot])
            joined = torch.cat((left, original_x[:, offset:offset + length]), dim=1)
            ref = F.conv1d(joined.float()[None], weight.float()[:, None], groups=dim)[0]
            expected[:, offset:offset + length] = F.silu(ref) if activation else ref
            expected_states[slot] = joined[:, -history:]
        offset += length
    actual = causal_conv1d_varlen(x, weight, states, cu, idx, init, max_seq_len=max(lens), activation=activation)
    tol = 2e-2 if dtype == torch.bfloat16 else 2e-6
    live_tokens = torch.arange(sum(lens), device="cuda") < sum(lens[:-1])
    torch.testing.assert_close(actual[:, live_tokens], expected[:, live_tokens], atol=tol, rtol=tol)
    torch.testing.assert_close(states, expected_states, atol=0, rtol=0)
    if kernel == 7:
        assert torch.equal(x, original_x)
        assert torch.count_nonzero(actual[:, ~live_tokens]) == 0

    for step in range(3):
        tokens = torch.randn(len(slots), dim * 2, device="cuda", dtype=dtype)[:, ::2]
        expected = torch.zeros_like(tokens)
        for row, slot in enumerate(slots):
            if slot == -1:
                continue
            joined = torch.cat((expected_states[slot], tokens[row, :, None]), dim=1)
            ref = F.conv1d(joined.float()[None], weight.float()[:, None], groups=dim)[0, :, 0]
            expected[row] = F.silu(ref) if activation else ref
            expected_states[slot] = joined[:, -history:]
        if kernel == 7 and step == 0:
            saved = states.clone()
            stream = torch.cuda.Stream()
            stream.wait_stream(torch.cuda.current_stream())
            with torch.cuda.stream(stream):
                causal_conv1d_decode(tokens, states, weight, idx, activation=activation)
            torch.cuda.current_stream().wait_stream(stream)
            states.copy_(saved)
            graph = torch.cuda.CUDAGraph()
            with torch.cuda.graph(graph, stream=stream):
                actual = causal_conv1d_decode(tokens, states, weight, idx, activation=activation)
            states.copy_(saved)
            graph.replay()
        else:
            actual = causal_conv1d_decode(tokens, states, weight, idx, activation=activation)
        torch.testing.assert_close(actual[:-1], expected[:-1], atol=tol, rtol=tol)
        torch.testing.assert_close(states, expected_states, atol=0, rtol=0)
        if kernel == 7:
            assert torch.count_nonzero(actual[-1]) == 0
