from __future__ import annotations

import pytest
import torch

if not torch.cuda.is_available():  # pragma: no cover
    pytest.skip("CUDA required", allow_module_level=True)

import freetoken.kernel.triton.nvfp4_linear as L

DEV = "cuda"
_E2M1 = torch.tensor([0, 0.5, 1, 1.5, 2, 3, 4, 6, -0.0, -0.5, -1, -1.5, -2, -3, -4, -6])


def _weight(N: int, K: int, seed: int = 0):
    g = torch.Generator().manual_seed(seed)
    packed = torch.randint(0, 256, (N, K // 2), dtype=torch.uint8, generator=g)
    scale = (torch.rand(N, K // 16, generator=g) + 0.5).to(torch.float8_e4m3fn)
    gscale = torch.full((N,), 0.01, dtype=torch.float16)
    codes = torch.stack([packed & 0xF, packed >> 4], dim=-1).reshape(N, K).long()
    dense = _E2M1[codes] * scale.float().repeat_interleave(16, dim=1) * gscale.float()[:, None]
    return packed.to(DEV), scale.to(DEV), gscale.to(DEV), dense.to(DEV)


@pytest.mark.parametrize("chunk_rows", [None, 256, 512])
def test_prefill_gemm_matches_dequant_reference(chunk_rows, monkeypatch):
    """M > 64 dequantizes to a bf16 scratch, N-chunked when the weight exceeds the chunk;
    every chunk lands in its own column slice of the output."""
    M, N, K = 200, 1000, 512
    packed, scale, gscale, dense = _weight(N, K)
    if chunk_rows is not None:
        monkeypatch.setattr(L, "_SCRATCH_CHUNK_BYTES", chunk_rows * K * 2)
    wt, st = L.nvfp4_transpose_resident(packed, scale)
    x = torch.randn(M, K, device=DEV, dtype=torch.bfloat16)

    y = L.nvfp4_dense_linear_t(x, wt, st, gscale)

    ref = x.float() @ dense.t()
    torch.testing.assert_close(y.float(), ref, rtol=2e-2, atol=2e-2 * ref.abs().max().item())
