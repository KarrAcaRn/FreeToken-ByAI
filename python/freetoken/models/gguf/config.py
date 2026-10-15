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
    "qwen35moe": "Qwen3_5MoeGGUFForCausalLM",
    "qwen3moe": "Qwen3MoeGGUFForCausalLM",
    # dense: Llama 3.x and Mistral (both ``llama``), Qwen2/2.5, Qwen3 (models/gguf/dense.py)
    "llama": "LlamaGGUFForCausalLM",
    "qwen2": "Qwen2GGUFForCausalLM",
    "qwen3": "Qwen3GGUFForCausalLM",
}


@dataclass
class GgufConfigShim:
    architectures: list[str]
    model_path: str
    model_type: str
    metadata: dict[str, Any]
    vocab_size: int
    tie_word_embeddings: bool
    # --hf-overrides a GGUF accepts: only the rope keys (see GGUF_OVERRIDE_KEYS)
    overrides: dict[str, Any] = field(default_factory=dict)

    def rope(self, head_dim_default: int | None = None) -> tuple[int, dict[str, Any] | None]:
        """(max_position, rope scaling or None) from the metadata, with any rope override applied:
        llama.cpp writes YaRN as ``<arch>.rope.scaling.{type,factor,original_context_length}``."""
        arch, md = self.model_type, self.metadata
        max_position = int(self.overrides.get("max_position_embeddings") or md[f"{arch}.context_length"])
        scaling = self.overrides.get("rope_scaling") or self.overrides.get("rope_parameters")
        if scaling is not None:
            scaling = dict(scaling)
            scaling.setdefault("rope_type", scaling.pop("type", None))
            if scaling["rope_type"] != "yarn":
                raise NotImplementedError(f"{self.model_path}: only a YaRN rope override is supported for a GGUF")
            return max_position, scaling
        kind = md.get(f"{arch}.rope.scaling.type")
        if kind in (None, "none"):
            return max_position, None
        if kind != "yarn":
            raise NotImplementedError(f"{self.model_path}: rope scaling {kind!r} in a {arch} GGUF is not supported")
        return max_position, {
            "rope_type": "yarn",
            "factor": float(md[f"{arch}.rope.scaling.factor"]),
            "original_max_position_embeddings": int(md[f"{arch}.rope.scaling.original_context_length"]),
        }

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
# the GGUF parsers that build their rope from GgufConfigShim.rope()
GGUF_ROPE_ARCHS = frozenset({"llama", "qwen2", "qwen3", "qwen3moe"})


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


__all__ = ["GgufConfigShim", "GGUF_ARCH_TO_REGISTRY", "GGUF_OVERRIDE_KEYS", "build_gguf_shim"]
