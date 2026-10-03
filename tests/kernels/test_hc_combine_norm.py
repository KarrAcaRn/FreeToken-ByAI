"""hc_combine_norm against the split launches it replaces, compared bit for bit.

The fused kernel feeds the next layer, so any bf16 flip compounds across the stack: torch.equal,
not a tolerance.
"""

import pytest
import torch

pytestmark = pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA is required")

HC = 4


def _inputs(num_tokens: int, hc_dim: int, w_shared: bool, res_pad: int, seed: int):
    gen = torch.Generator(device="cuda").manual_seed(seed)
    kw = {"generator": gen, "device": "cuda", "dtype": torch.bfloat16}
    dim = HC * hc_dim
    # res_pad > 0 gives the residual a row stride the split norm never sees
    residual = (torch.randn(num_tokens, dim + res_pad, **kw) * 4.0)[:, :dim]
    block = torch.randn(num_tokens, hc_dim, **kw) * 2.0
    # the inject logits are a strided slice of the merged down GEMM in the model
    inject = torch.randn(num_tokens, 336, **kw)[:, 320 : 320 + HC]
    weight = torch.randn(hc_dim if w_shared else dim, **kw) * 0.5
    return residual, block, inject, weight


@pytest.mark.parametrize("w_shared", [False, True])
@pytest.mark.parametrize("res_pad", [0, 3])
@pytest.mark.parametrize("hc_dim", [2560, 640, 100])
@pytest.mark.parametrize("num_tokens", [1, 7, 300])
def test_hc_combine_norm_bitwise_matches_split(num_tokens, hc_dim, res_pad, w_shared):
    from freetoken.kernel.triton.hc import grouped_gemma_rmsnorm, hc_combine, hc_combine_norm

    residual, block, inject, weight = _inputs(num_tokens, hc_dim, w_shared, res_pad, hc_dim + num_tokens)
    eps = 1e-6

    split_r = hc_combine(residual, block, inject, HC)
    split_n = grouped_gemma_rmsnorm(split_r, weight, eps, HC)
    fused_r, fused_n = hc_combine_norm(residual, block, inject, weight, eps, HC)

    assert torch.equal(fused_r, split_r)
    assert torch.equal(fused_n, split_n)


@pytest.mark.parametrize("hc_dim", [2560, 640, 100])
@pytest.mark.parametrize("num_tokens", [1, 7, 300])
def test_hc_combine_norm_shared_epilogue_bitwise_matches_split(num_tokens, hc_dim):
    from freetoken.kernel.triton.hc import grouped_gemma_rmsnorm, hc_combine, hc_combine_norm
    from freetoken.kernel.triton.moe_shared_gate import shared_gate_mul_add

    residual, routed, inject, weight = _inputs(num_tokens, hc_dim, True, 0, 7 * hc_dim + num_tokens)
    gen = torch.Generator(device="cuda").manual_seed(hc_dim)
    shared = torch.randn(num_tokens, hc_dim, generator=gen, device="cuda", dtype=torch.bfloat16)
    gate = torch.rand(num_tokens, generator=gen, device="cuda", dtype=torch.float32)
    eps = 1e-6

    split_r = hc_combine(residual, shared_gate_mul_add(routed, shared, gate), inject, HC)
    split_n = grouped_gemma_rmsnorm(split_r, weight, eps, HC)
    fused_r, fused_n = hc_combine_norm(residual, routed, inject, weight, eps, HC, shared, gate)

    assert torch.equal(fused_r, split_r)
    assert torch.equal(fused_n, split_n)
