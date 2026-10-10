"""Host-bank shapes of routed experts served natively from a GGUF file.

Shared by every GGUF MoE family. A layout whose routed experts are all Q4_0 keeps the
legacy ``[E, rows, row_bytes]`` banks; any other type (K- and I-quants, or types that
differ by layer) gets fixed-width byte slots sized for the widest layer, and
``gguf_quant_types`` tells the kernel how to decode each layer.
"""

from __future__ import annotations

import torch

from .dequant import GGML_Q4_0, row_bytes


def q4_0_expert_specs(config) -> dict[str, tuple[tuple[int, ...], torch.dtype]]:
    E = config.num_experts
    H, I = config.hidden_size, config.moe_intermediate_size
    return {
        "gate_up": ((E, 2 * I, row_bytes(H, GGML_Q4_0)), torch.uint8),
        "down": ((E, H, row_bytes(I, GGML_Q4_0)), torch.uint8),
    }


def uses_mixed_gguf_experts(config) -> bool:
    layout = getattr(config, "gguf_quant_types", None)
    if layout is None:
        return False
    return any(
        quant_type != GGML_Q4_0
        for role in ("expert_gate_up", "expert_down")
        for quant_type in layout.get(role, ())
    )


def gguf_expert_specs(config) -> dict[str, tuple[tuple[int, ...], torch.dtype]]:
    if not uses_mixed_gguf_experts(config):
        return q4_0_expert_specs(config)
    layout = config.gguf_quant_types
    E = config.num_experts
    return {
        "gate_up": ((E, max(layout["expert_gate_up_bytes"])), torch.uint8),
        "down": ((E, max(layout["expert_down_bytes"])), torch.uint8),
    }


def dummy_gguf_expert_sources(config) -> dict[str, list[torch.Tensor]]:
    """Random expert banks shaped like the GGUF expert loaders' output (--use-dummy-weight)."""
    from freetoken.moe.host_banks import alloc_layer_banks, pin_banks

    hb = alloc_layer_banks(gguf_expert_specs(config), config.num_layers)
    banks = {name: [b.tensor for b in hb[name]] for name in hb}
    for t in banks["gate_up"] + banks["down"]:
        t.random_(0, 256)
    if torch.cuda.is_available():
        pin_banks(hb)  # match the other dummies: pin-after-fill (no-op mmap fill on CPU-only)
    return banks


__all__ = ["q4_0_expert_specs", "uses_mixed_gguf_experts", "gguf_expert_specs", "dummy_gguf_expert_sources"]
