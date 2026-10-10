"""FREETOKEN_FP8_LM_HEAD: a bf16 checkpoint weight block-quantized to fp8 at load, served by the
float-scale fp8-block GEMV."""

from __future__ import annotations

import types

import pytest
import torch

from freetoken.layers.quantization import LinearConfig
from freetoken.layers.quantization.linear.fp8_block import Fp8BlockQuantizeAtLoadLinearMethod
from freetoken.layers.quantization.scheme import fp8_block_qat_scheme


def _method(k: int, n: int) -> Fp8BlockQuantizeAtLoadLinearMethod:
    return Fp8BlockQuantizeAtLoadLinearMethod(LinearConfig(k, n, scheme=fp8_block_qat_scheme("float")))


def test_the_qat_scheme_selects_its_kernel():
    # the inherited float-scale check asserted an FP8_BLOCK scheme, so FREETOKEN_FP8_LM_HEAD=1
    # failed while building the lm_head
    assert _method(256, 512).kernel.name == "triton_qat"


@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")
@pytest.mark.parametrize("m", [1, 7])
def test_quantized_at_load_matches_the_bf16_linear(m):
    k, n = 512, 1024
    method = _method(k, n)
    layer = types.SimpleNamespace(bias=None)
    method.create_weights(layer)
    w = torch.randn(n, k, dtype=torch.bfloat16, device="cuda") / k**0.5
    layer.weight = w.clone()
    method.kernel.finalize(layer)
    assert layer.weight.dtype == torch.float8_e4m3fn
    x = torch.randn(m, k, dtype=torch.bfloat16, device="cuda")
    out = method.kernel.apply(layer, x)
    ref = torch.nn.functional.linear(x, w)
    # e4m3 keeps ~3 mantissa bits: compare the whole output, not each element
    err = (out.float() - ref.float()).norm() / ref.float().norm()
    assert err < 0.05, err
