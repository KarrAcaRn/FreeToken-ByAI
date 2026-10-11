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


# Routed experts stored as separate gate / up / down ``[E, rows, row_bytes]`` stacks
# (llama.cpp qwen35moe, qwen3moe); read by the bank loader, not the dense weight pass.
SPLIT_EXPERT_SUFFIXES = ("ffn_gate_exps.weight", "ffn_up_exps.weight", "ffn_down_exps.weight")


def split_expert_quant_layout(model_path: str, num_layers: int, hidden: int, moe_inter: int, arch: str) -> dict:
    """ggml type of every non-expert tensor plus the per-layer routed-expert types and slot bytes."""
    from .reader import iter_gguf_tensors

    tensors: dict[str, int] = {}
    experts: dict[str, list[int | None]] = {sfx: [None] * num_layers for sfx in SPLIT_EXPERT_SUFFIXES}
    for t in iter_gguf_tensors(model_path):
        if t.name.startswith("blk."):
            layer = int(t.name.split(".")[1])
            suffix = t.name.split(".", 2)[2]
            if layer >= num_layers:
                continue  # NextN / MTP block
            if suffix in experts:
                experts[suffix][layer] = t.ggml_type
                continue
        tensors[t.name] = t.ggml_type
    if not tensors:
        raise NotImplementedError(
            f"{model_path}: no GGUF tensor table (a converted FTW dir?); serve the .gguf file directly"
        )
    missing = {sfx: [i for i, v in enumerate(types) if v is None] for sfx, types in experts.items()}
    missing = {sfx: ids for sfx, ids in missing.items() if ids}
    if missing:
        raise ValueError(f"{arch} GGUF routed-expert tensors missing: {missing}")
    gate, up, down = (tuple(experts[sfx]) for sfx in SPLIT_EXPERT_SUFFIXES)
    split = [i for i in range(num_layers) if gate[i] != up[i]]
    if split:
        raise NotImplementedError(
            f"{arch} GGUF: ffn_gate_exps and ffn_up_exps differ in ggml type in layers {split}; "
            "the fused gate_up expert bank needs one type per layer"
        )
    return {
        "tensors": tensors,
        "expert_gate_up": gate,
        "expert_down": down,
        "expert_gate_up_bytes": tuple(2 * moe_inter * row_bytes(hidden, t) for t in gate),
        "expert_down_bytes": tuple(hidden * row_bytes(moe_inter, t) for t in down),
    }


def load_split_gguf_expert_sources(model_path: str, config, *, layer_sink=None) -> dict[str, list[torch.Tensor]]:
    """Per-layer host banks of the routed experts' packed ggml bytes, verbatim from the file.

    ``gate_up`` holds each expert's gate rows followed by its up rows (one GEMV computes
    the fused ``[gate | up]`` the activation splits), ``down`` its down rows. A non-Q4_0
    layout stores each expert as one fixed-width byte slot. ``layer_sink`` as in the
    gemma4 loader (the converter; mixed layouts refuse it).
    """
    from freetoken.moe.host_banks import LayerCompletionTracker, PinPipeline, alloc_layer_banks

    from .reader import iter_gguf_tensors

    L, E = config.num_layers, config.num_experts
    mixed = uses_mixed_gguf_experts(config)
    if mixed and layer_sink is not None:
        raise NotImplementedError(
            "converting non-Q4_0 GGUF expert banks to FTW is not supported; serve the source GGUF directly"
        )
    hb = alloc_layer_banks(gguf_expert_specs(config), L)
    banks = {name: [b.tensor for b in hb[name]] for name in hb}
    seen: dict[str, set[int]] = {sfx: set() for sfx in SPLIT_EXPERT_SUFFIXES}

    def _place(t) -> int | None:
        if not t.name.startswith("blk."):
            return None
        layer, suffix = int(t.name.split(".")[1]), t.name.split(".", 2)[2]
        if suffix not in seen or layer >= L:
            return None
        packed = t.packed().reshape(E, -1)
        width = packed.shape[1]
        if suffix == "ffn_down_exps.weight":
            dst = banks["down"][layer].view(E, -1)[:, :width]
        else:
            # gate and up share a type (checked in split_expert_quant_layout), so up starts one gate width in
            start = width if suffix == "ffn_up_exps.weight" else 0
            dst = banks["gate_up"][layer].view(E, -1)[:, start : start + width]
        dst.copy_(packed)
        seen[suffix].add(layer)
        return layer

    def _load(sink) -> None:
        tracker = LayerCompletionTracker(3, hb, sink) if sink is not None else None  # gate + up + down
        for t in iter_gguf_tensors(model_path):
            layer = _place(t)
            if layer is not None and tracker is not None:
                tracker.note(layer)

    if layer_sink is not None:
        _load(layer_sink)
    elif torch.cuda.is_available():
        with PinPipeline() as pins:
            _load(pins)
    else:
        _load(None)

    missing = {sfx: sorted(set(range(L)) - got) for sfx, got in seen.items() if got != set(range(L))}
    assert not missing, f"missing GGUF expert layers: {missing}"
    return banks


__all__ = [
    "SPLIT_EXPERT_SUFFIXES",
    "q4_0_expert_specs",
    "uses_mixed_gguf_experts",
    "gguf_expert_specs",
    "dummy_gguf_expert_sources",
    "split_expert_quant_layout",
    "load_split_gguf_expert_sources",
]
