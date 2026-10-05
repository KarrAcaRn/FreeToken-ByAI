"""bf16 Linear: torch, plus a Triton GEMV for the single-row decode case."""

from __future__ import annotations

from typing import Any

import torch
import torch.nn.functional as F

from freetoken.kernel import backend

from ..registry import LayerKind, register_method
from ..scheme import QuantKind
from .base import LinearConfig, LinearKernel, LinearMethod

# The GEMV gives each CTA two output rows; below this a layer has too few CTAs to fill the GPU.
GEMV_MIN_OUT_FEATURES = 512


class TorchLinearKernel(LinearKernel):
    name = "torch"

    def apply(self, layer: Any, x: torch.Tensor) -> torch.Tensor:
        return self.linear(x, layer.weight, layer.bias)

    def linear(self, x: torch.Tensor, w: torch.Tensor, b: torch.Tensor | None) -> torch.Tensor:
        # an fp32 activation stream (DeepSeek-V4's compressors) upcasts the bf16 weight on the fly, as the reference does
        if w.dtype != x.dtype:
            w = w.to(x.dtype)
            b = b.to(x.dtype) if b is not None else None
        return F.linear(x, w, b)


class TritonGemvLinearKernel(TorchLinearKernel):
    """torch, except one bf16 row without bias (decode bs=1) reads the weight through a Triton GEMV."""

    name = "gemv"

    def unusable_reason(self, cfg: LinearConfig) -> str | None:
        if not torch.cuda.is_available():
            return "no CUDA device"
        if backend.is_rocm():
            return "the GEMV is only measured on NVIDIA GPUs"
        return None

    def worth_it(self, cfg: LinearConfig) -> bool:
        return cfg.out_features >= GEMV_MIN_OUT_FEATURES

    def linear(self, x: torch.Tensor, w: torch.Tensor, b: torch.Tensor | None) -> torch.Tensor:
        from freetoken.kernel.triton.bf16_gemv import bf16_gemv, single_row_bf16

        if b is None and x.is_cuda and x.device == w.device and single_row_bf16(x, w):
            return bf16_gemv(x.reshape(-1), w, x.dtype).reshape(*x.shape[:-1], w.shape[0])
        return super().linear(x, w, b)


# Smaller outputs are routers and gate projections (MoE gate, GDN in_proj_ba): cheap to read
# and precision-sensitive, so the opt-in fp8 kernel leaves them in bf16.
ONLINE_FP8_MIN_OUT_FEATURES = 1024


class OnlineFp8LinearKernel(TritonGemvLinearKernel):
    """Opt-in (``--online-quant fp8``): a bf16 checkpoint's weight is quantized at load to e4m3
    with one fp32 scale per output row and read through the W8A16 kernels, halving the bytes a
    bandwidth-bound decode step streams. Changes the model's numerics, so never auto-picked."""

    name = "fp8"

    def unusable_reason(self, cfg: LinearConfig) -> str | None:
        return None if torch.cuda.is_available() else "no CUDA device"

    def worth_it(self, cfg: LinearConfig) -> bool:
        return False

    def finalize(self, layer: Any) -> None:
        w = layer.weight
        if (w.dim() != 2 or w.dtype not in (torch.bfloat16, torch.float16) or not w.is_cuda
                or w.shape[0] < ONLINE_FP8_MIN_OUT_FEATURES):
            return
        # row chunks bound the fp32 temporaries (a 248k-vocab lm_head is 5 GB in fp32)
        q = torch.empty(w.shape, dtype=torch.float8_e4m3fn, device=w.device)
        scale = torch.empty(w.shape[0], dtype=torch.float32, device=w.device)
        rows = max(1, (64 << 20) // w.shape[1])
        for r0 in range(0, w.shape[0], rows):
            chunk = w[r0 : r0 + rows].float()
            s = chunk.abs().amax(dim=1).clamp(min=1e-12) / torch.finfo(torch.float8_e4m3fn).max
            q[r0 : r0 + rows] = (chunk / s[:, None]).to(torch.float8_e4m3fn)
            scale[r0 : r0 + rows] = s
        layer.weight = q
        layer.online_fp8_scale = scale

    def apply(self, layer: Any, x: torch.Tensor) -> torch.Tensor:
        scale = getattr(layer, "online_fp8_scale", None)
        if scale is None:
            return super().apply(layer, x)
        from freetoken.kernel.triton.fp8_pertensor_linear import fp8_pertensor_linear

        return fp8_pertensor_linear(x, layer.weight, scale, layer.bias)


@register_method(QuantKind.NONE, LayerKind.LINEAR)
class UnquantizedLinearMethod(LinearMethod):
    candidates = (TritonGemvLinearKernel, TorchLinearKernel, OnlineFp8LinearKernel)

    def create_weights(self, layer: Any) -> None:
        g = self.cfg
        layer.weight = torch.empty(g.out_features, g.in_features)
