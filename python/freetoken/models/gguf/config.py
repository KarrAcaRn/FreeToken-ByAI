"""GGUF config shim: the object the model registry sees for a ``.gguf`` model.

``cached_load_hf_config`` returns one of these for GGUF paths instead of a HF
``PretrainedConfig``. It carries the architecture key (so the registry can dispatch),
the raw GGUF metadata dict, and a few derived facts that need the tensor table
(``vocab_size``, ``tie_word_embeddings``). The per-arch ``parse_gguf_config`` reads
``metadata`` to build the FreeToken ``ModelConfig``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .reader import gguf_architecture, load_gguf_metadata, gguf_tensor_names

# GGUF ``general.architecture`` -> FreeToken registry key (a GGUF-specific spec that
# reuses the model classes but a GGUF parse_config / iter_weights).
GGUF_ARCH_TO_REGISTRY: dict[str, str] = {
    "gemma4": "Gemma4GGUFForCausalLM",
    "llama": "LlamaGGUFForCausalLM",
    "minimax-m2": "MiniMaxM2GGUFForCausalLM",
    "minimax-m3": "MiniMaxM3GGUFForCausalLM",
    "muse-glimmer": "MuseGlimmerGGUFForCausalLM",
    "qwen2": "Qwen2GGUFForCausalLM",
    "qwen3": "Qwen3GGUFForCausalLM",
    "qwen3moe": "Qwen3MoeGGUFForCausalLM",
    "qwen35": "Qwen3_5GGUFForCausalLM",
    "qwen35moe": "Qwen3_5MoeGGUFForCausalLM",
    "qwen4exp": "Qwen4ExpGGUFForCausalLM",
}


@dataclass(frozen=True)
class GgufConfigShim:
    architectures: list[str]
    model_path: str
    model_type: str
    metadata: dict[str, Any]
    vocab_size: int
    tie_word_embeddings: bool
    # --hf-overrides a GGUF accepts: only the rope keys (see GGUF_OVERRIDE_KEYS)
    overrides: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Minimal HF-config-like dict for trunk code that introspects the config
        (e.g. server arg parsing reads ``torch_dtype`` to resolve ``--dtype auto``).
        GGUF weights dequantize to a bf16 compute path."""
        return {
            "architectures": list(self.architectures),
            "model_type": self.model_type,
            "torch_dtype": "bfloat16",
            "vocab_size": self.vocab_size,
            "tie_word_embeddings": self.tie_word_embeddings,
        }


def _vocab_size(model_path: str) -> int:
    from .reader import _reader

    for t in _reader(model_path).tensors:
        if t.name == "token_embd.weight":
            return int(t.shape[-1])  # ggml [hidden, vocab] -> vocab is last
    # A metadata-only GGUF (an FTW dir's source_metadata.gguf) strips the tensor table, so
    # fall back to the tokenizer vocab. llama.cpp sizes token_embd's rows to n_vocab =
    # len(tokenizer.ggml.tokens), so this equals the tensor-derived value exactly.
    toks = load_gguf_metadata(model_path).get("tokenizer.ggml.tokens")
    if toks is not None:
        return len(toks)
    raise ValueError(f"GGUF {model_path}: no token_embd.weight to size the vocab")


# rope only: everything else a GGUF describes is baked into its tensors
GGUF_OVERRIDE_KEYS = frozenset({"rope_scaling", "rope_parameters", "max_position_embeddings"})
# the GGUF parsers that pass their HF config through apply_rope_overrides()
GGUF_ROPE_ARCHS = frozenset({"llama", "qwen2", "qwen3", "qwen3moe"})


def apply_rope_overrides(shim: GgufConfigShim, hf: Any) -> Any:
    """Apply the shim's rope --hf-overrides to a GGUF parser's HF config namespace (YaRN only)."""
    if max_position := shim.overrides.get("max_position_embeddings"):
        hf.max_position_embeddings = int(max_position)
    scaling = shim.overrides.get("rope_scaling") or shim.overrides.get("rope_parameters")
    if scaling is not None:
        scaling = dict(scaling)
        scaling.setdefault("rope_type", scaling.pop("type", None))
        if scaling["rope_type"] != "yarn":
            raise NotImplementedError(f"{shim.model_path}: only a YaRN rope override is supported for a GGUF")
        if (hf.rope_scaling or {}).get("rope_type", "default") not in ("default", "yarn"):
            raise NotImplementedError(f"{shim.model_path}: YaRN on top of {hf.rope_scaling['rope_type']} rope is not supported")
        hf.rope_scaling = {**(hf.rope_scaling or {}), **scaling}
    return hf


def build_gguf_shim(model_path: str, overrides: dict[str, Any] | None = None) -> GgufConfigShim:
    if unknown := set(overrides or {}) - GGUF_OVERRIDE_KEYS:
        raise ValueError(f"--hf-overrides on a GGUF accepts only {sorted(GGUF_OVERRIDE_KEYS)}; got {sorted(unknown)}")
    arch = gguf_architecture(model_path)
    if overrides and arch not in GGUF_ROPE_ARCHS:
        raise ValueError(f"--hf-overrides is not supported for a {arch!r} GGUF (rope overrides: {sorted(GGUF_ROPE_ARCHS)})")
    registry_key = GGUF_ARCH_TO_REGISTRY.get(arch)
    if registry_key is None:
        raise ValueError(
            f"GGUF architecture {arch!r} is not supported "
            f"(known: {sorted(GGUF_ARCH_TO_REGISTRY)})"
        )
    names = gguf_tensor_names(model_path)
    metadata = load_gguf_metadata(model_path)
    if names:
        # No separate output projection -> embeddings are tied.
        tie_word_embeddings = "output.weight" not in names
    else:
        # Metadata-only GGUF (an FTW dir's source_metadata.gguf): the tensor table is
        # stripped, so the fact travels as a KV written at convert time.
        from .reader import OUTPUT_WEIGHT_PRESENT_KV

        present = metadata.get(OUTPUT_WEIGHT_PRESENT_KV)
        if present is None:
            raise ValueError(
                f"{model_path}: metadata-only GGUF lacks {OUTPUT_WEIGHT_PRESENT_KV!r}; "
                "reconvert the checkpoint with the current freetoken.checkpoint.convert"
            )
        tie_word_embeddings = not present
    return GgufConfigShim(
        architectures=[registry_key],
        model_path=model_path,
        model_type=arch,
        metadata=metadata,
        vocab_size=_vocab_size(model_path),
        tie_word_embeddings=tie_word_embeddings,
        overrides=dict(overrides or {}),
    )


__all__ = ["GgufConfigShim", "GGUF_ARCH_TO_REGISTRY", "GGUF_OVERRIDE_KEYS", "apply_rope_overrides", "build_gguf_shim"]
