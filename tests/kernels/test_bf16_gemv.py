"""The single-row bf16 GEMV behind ``UnquantizedLinearMethod``: which layers select it, which calls
take it, and that it matches F.linear. Every call it declines must be F.linear bit for bit."""

from __future__ import annotations

import pytest
import torch
import torch.nn.functional as F

from freetoken.kernel.triton.bf16_gemv import single_row_bf16
from freetoken.layers.quantization import KernelSelectionError, LinearConfig, UnquantizedLinearMethod, select_kernel
from freetoken.layers.quantization.linear.unquantized import (
    GEMV_MIN_OUT_FEATURES,
    TorchLinearKernel,
    TritonGemvLinearKernel,
)

BF16 = torch.bfloat16
cuda = pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA required")


# --------------------------------------------------------------------------- selection (CPU)


def _select(n: int, requested: str = "auto"):
    return select_kernel(UnquantizedLinearMethod.candidates, requested, LinearConfig(1024, n))


@pytest.fixture
def nvidia_host(monkeypatch):
    from freetoken.kernel import backend

    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(backend, "is_rocm", lambda: False)


def test_a_host_without_cuda_keeps_torch(monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    assert type(_select(4096)) is TorchLinearKernel
    with pytest.raises(KernelSelectionError):
        _select(4096, "gemv")


def test_rocm_keeps_torch(monkeypatch):
    from freetoken.kernel import backend

    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(backend, "is_rocm", lambda: True)
    assert type(_select(4096)) is TorchLinearKernel


def test_nvidia_selects_the_gemv_for_wide_layers_only(nvidia_host):
    assert type(_select(GEMV_MIN_OUT_FEATURES)) is TritonGemvLinearKernel
    assert type(_select(151936)) is TritonGemvLinearKernel
    assert type(_select(GEMV_MIN_OUT_FEATURES - 1)) is TorchLinearKernel


def test_quant_backend_overrides_the_width_heuristic(nvidia_host):
    assert type(_select(4096, "torch")) is TorchLinearKernel
    assert type(_select(64, "gemv")) is TritonGemvLinearKernel


@pytest.mark.parametrize("x_shape,w_shape,x_dtype,w_dtype,transposed,ok", [
    ((1, 64), (32, 64), BF16, BF16, False, True),
    ((1, 1, 64), (32, 64), BF16, BF16, False, True),
    ((64,), (32, 64), BF16, BF16, False, True),
    ((2, 64), (32, 64), BF16, BF16, False, False),        # decode bs>1 / prefill
    ((0, 64), (32, 64), BF16, BF16, False, False),        # empty batch
    ((1, 64), (32, 64), torch.float32, BF16, False, False),  # DSV4's fp32 activation stream
    ((1, 64), (32, 64), torch.float16, torch.float16, False, False),
    ((1, 64), (32, 64), BF16, BF16, True, False),         # column-major weight
    ((2, 32), (32, 64), BF16, BF16, False, False),        # numel == K but the wrong last dim
])
def test_single_row_bf16(x_shape, w_shape, x_dtype, w_dtype, transposed, ok):
    x = torch.zeros(x_shape, dtype=x_dtype)
    w = torch.zeros(w_shape[::-1], dtype=w_dtype).t() if transposed else torch.zeros(w_shape, dtype=w_dtype)
    assert single_row_bf16(x, w) is ok


def test_layer_wide_triton_request_leaves_bf16_linears_on_auto():
    """``linear=triton`` targets the quantized linears; the bf16 GEMV is opted into only by its own name."""
    from freetoken.layers.quantization import LayerKind, QuantBackend, QuantKind

    assert QuantBackend.parse("linear=triton").select(LayerKind.LINEAR, QuantKind.NONE) == "auto"
    assert QuantBackend.parse("linear.none=torch").select(LayerKind.LINEAR, QuantKind.NONE) == "torch"
    assert QuantBackend.parse("linear.none=gemv").select(LayerKind.LINEAR, QuantKind.NONE) == "gemv"


@pytest.mark.parametrize("x_shape,w_shape,w_dtype", [
    ((48,), (32, 64), BF16),     # x narrower than the weight: the kernel would read past x
    ((80,), (32, 64), BF16),
    ((1, 64), (32, 64), BF16),   # bf16_gemv takes a flat row
    ((64,), (32, 64), torch.float16),
])
def test_gemv_refuses_mismatched_operands(x_shape, w_shape, w_dtype):
    from freetoken.kernel.triton.bf16_gemv import bf16_gemv

    with pytest.raises(ValueError):
        bf16_gemv(torch.zeros(x_shape, dtype=BF16), torch.zeros(w_shape, dtype=w_dtype), BF16)


def test_dsv4_wrapper_refuses_a_mismatched_width():
    from freetoken.kernel.triton.dsv4.bf16_linear import bf16_linear_fp32

    with pytest.raises(ValueError):
        bf16_linear_fp32(torch.zeros(1, 48, dtype=BF16), torch.zeros(32, 64, dtype=BF16))


def test_cpu_tensors_take_f_linear():
    torch.manual_seed(0)
    x = torch.randn(1, 64, dtype=BF16)
    w = torch.randn(32, 64, dtype=BF16)
    assert torch.equal(TritonGemvLinearKernel().linear(x, w, None), F.linear(x, w))


# --------------------------------------------------------------------------- GPU


# (4096, 4096) a square o_proj; (12288+2*1024, 5120) a fused qkv; (1000, 6112) N and K tails;
# (151936, 2048) a vocab-wide LM head.
SHAPES = [(4096, 4096), (14336, 5120), (1000, 6112), (151936, 2048)]


@cuda
@pytest.mark.parametrize("N,K", SHAPES)
@pytest.mark.parametrize("lead", [(1,), (1, 1), ()])
def test_gemv_matches_f_linear(N: int, K: int, lead: tuple[int, ...]):
    torch.manual_seed(N + K)
    w = torch.randn(N, K, device="cuda", dtype=BF16) * 0.02
    x = torch.randn(*lead, K, device="cuda", dtype=BF16)
    y = TritonGemvLinearKernel().linear(x, w, None)
    y_ref = F.linear(x, w)
    assert y.shape == y_ref.shape and y.dtype == BF16
    exact = (x.double().reshape(1, K) @ w.double().t()).reshape(y.shape)
    # both round one fp32 sum to bf16; only the accumulation order differs
    tol = 2 * 2.0 ** -8 * exact.abs().max().item()
    assert (y.float() - exact).abs().max().item() <= tol
    assert (y_ref.float() - exact).abs().max().item() <= tol


@cuda
@pytest.mark.parametrize("N,K", [(7, 5000), (1024, 96), (33, 8200)])
def test_bf16_out_is_the_rounded_fp32_out(N: int, K: int):
    """One accumulation, two stores: the bf16 caller gets exactly the DSV4 fp32 result rounded,
    including for a strided x and a K past one 4096 block with a masked tail."""
    from freetoken.kernel.triton.bf16_gemv import bf16_gemv

    torch.manual_seed(K)
    w = torch.randn(N, K, device="cuda", dtype=BF16)
    x = torch.randn(K, 2, device="cuda", dtype=BF16)[:, 1]
    y32 = bf16_gemv(x, w, torch.float32)
    ref = (w.double() @ x.double()).float()
    assert (y32 - ref).abs().max().item() < 1e-4 * ref.abs().max().item()
    assert torch.equal(bf16_gemv(x, w, BF16), y32.to(BF16))


@cuda
def test_single_row_launches_the_gemv(monkeypatch):
    import freetoken.kernel.triton.bf16_gemv as mod

    calls = []
    real = mod.bf16_gemv
    monkeypatch.setattr(mod, "bf16_gemv", lambda *a: calls.append(a) or real(*a))
    w = torch.randn(1024, 512, device="cuda", dtype=BF16)
    TritonGemvLinearKernel().linear(torch.randn(1, 512, device="cuda", dtype=BF16), w, None)
    assert len(calls) == 1


@cuda
@pytest.mark.parametrize("case", ["two_rows", "prefill", "fp32_x", "bias", "column_major_w"])
def test_declined_calls_are_f_linear_exactly(case: str, monkeypatch):
    import freetoken.kernel.triton.bf16_gemv as mod

    def boom(*_):
        raise AssertionError("GEMV taken")

    monkeypatch.setattr(mod, "bf16_gemv", boom)
    torch.manual_seed(0)
    K, N = 512, 1024
    x = torch.randn(1, K, device="cuda", dtype=BF16)
    w = torch.randn(N, K, device="cuda", dtype=BF16)
    b = None
    if case == "two_rows":
        x = torch.randn(2, K, device="cuda", dtype=BF16)
    elif case == "prefill":
        x = torch.randn(300, K, device="cuda", dtype=BF16)
    elif case == "fp32_x":
        x = x.float()
    elif case == "bias":
        b = torch.randn(N, device="cuda", dtype=BF16)
    elif case == "column_major_w":
        w = torch.randn(K, N, device="cuda", dtype=BF16).t()
    got = TritonGemvLinearKernel().linear(x, w, b)
    want = TorchLinearKernel().linear(x, w, b)
    assert torch.equal(got, want)


@cuda
def test_gemv_replays_under_cuda_graph():
    torch.manual_seed(0)
    K, N = 2048, 4096
    w = torch.randn(N, K, device="cuda", dtype=BF16) * 0.02
    x = torch.randn(1, K, device="cuda", dtype=BF16)
    kernel = TritonGemvLinearKernel()
    kernel.linear(x, w, None)  # compile outside capture, as the engine's warmup does
    torch.cuda.synchronize()
    graph = torch.cuda.CUDAGraph()
    with torch.cuda.graph(graph):
        y = kernel.linear(x, w, None)
    x.copy_(torch.randn(1, K, device="cuda", dtype=BF16))
    graph.replay()
    torch.cuda.synchronize()
    assert torch.equal(y, kernel.linear(x, w, None))


@cuda
def test_dsv4_fp32_wrapper_still_matches_its_reference():
    from freetoken.kernel.triton.dsv4.bf16_linear import bf16_linear_fp32

    torch.manual_seed(0)
    w = torch.randn(1024, 4096, device="cuda", dtype=BF16)
    x = torch.randn(1, 4096, device="cuda", dtype=BF16)
    y = bf16_linear_fp32(x, w)
    ref = F.linear(x.double(), w.double()).float()
    assert y.dtype == torch.float32
    assert (y - ref).abs().max().item() < 1e-3 * ref.abs().max().item()


def test_online_fp8_is_only_ever_requested(nvidia_host):
    """--online-quant fp8 changes the model's numerics: auto never picks it, a request does."""
    from freetoken.layers.quantization.linear.unquantized import OnlineFp8LinearKernel

    assert type(_select(151936)) is TritonGemvLinearKernel
    assert type(_select(64)) is not OnlineFp8LinearKernel
    assert type(_select(151936, "fp8")) is OnlineFp8LinearKernel


@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")
@pytest.mark.parametrize("M", [1, 8, 300])
def test_online_fp8_tracks_the_bf16_linear(M):
    from types import SimpleNamespace

    from freetoken.layers.quantization.linear.unquantized import OnlineFp8LinearKernel

    torch.manual_seed(0)
    kernel = OnlineFp8LinearKernel()
    w = torch.randn(2048, 1024, device="cuda", dtype=BF16) * 0.05
    gate = torch.randn(64, 1024, device="cuda", dtype=BF16) * 0.05
    big = SimpleNamespace(weight=w.clone(), bias=None)
    small = SimpleNamespace(weight=gate.clone(), bias=None)
    kernel.finalize(big)
    kernel.finalize(small)
    assert big.weight.dtype == torch.float8_e4m3fn and big.online_fp8_scale.shape == (2048,)
    assert small.weight.dtype == BF16  # routers and gates stay bf16

    x = torch.randn(M, 1024, device="cuda", dtype=BF16)
    ref = F.linear(x.float(), w.float())
    rel = ((kernel.apply(big, x).float() - ref).norm() / ref.norm()).item()
    assert rel < 3e-2, rel
    assert torch.equal(kernel.apply(small, x), TritonGemvLinearKernel().apply(small, x))
