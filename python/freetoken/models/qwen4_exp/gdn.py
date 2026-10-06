from __future__ import annotations

from freetoken.layers import GatedRMSNorm
from freetoken.layers.quantization import QuantConfig
from freetoken.models.qwen3_5_moe.gdn import Qwen3_5GatedDeltaNet


class Qwen4ExpGatedDeltaNet(Qwen3_5GatedDeltaNet):
    """Qwen3.5's GatedDeltaNet with a configurable output gate: ``output_gate`` is the gate
    activation name from ``LinearGatedDeltaGroupConfig`` ("sigmoid" for Qwen3.8-Flash-Next).
    Everything else -- prefill, decode, the DFlash verify and commit -- is shared."""

    def __init__(
        self, hidden_size, num_k_heads, num_v_heads, head_k_dim, head_v_dim,
        conv_kernel_size, rms_norm_eps, layer_id, output_gate: str = "sigmoid",
        *, quant_config: QuantConfig | None = None, prefix: str = "",
    ):
        super().__init__(
            hidden_size, num_k_heads, num_v_heads, head_k_dim, head_v_dim,
            conv_kernel_size, rms_norm_eps, layer_id, quant_config=quant_config, prefix=prefix,
        )
        self.norm = GatedRMSNorm(head_v_dim, eps=rms_norm_eps, activation=output_gate)


__all__ = ["Qwen4ExpGatedDeltaNet"]
