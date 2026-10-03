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


@register_method(QuantKind.NONE, LayerKind.LINEAR)
class UnquantizedLinearMethod(LinearMethod):
    candidates = (TritonGemvLinearKernel, TorchLinearKernel)

    def create_weights(self, layer: Any) -> None:
        g = self.cfg
        layer.weight = torch.empty(g.out_features, g.in_features)
