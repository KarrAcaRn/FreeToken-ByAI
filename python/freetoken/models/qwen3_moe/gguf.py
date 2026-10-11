"""Qwen3-MoE (llama.cpp arch ``qwen3moe``, e.g. Qwen3-30B-A3B) served from a GGUF file.

The geometry is the HF qwen3_moe model's (full attention with q/k norms on every layer,
routed experts without a shared expert), so this builds the same ``ModelConfig`` as
``config.parse_config`` from GGUF metadata. llama.cpp's converter stores this family's
tensors unchanged: plain RMSNorm weights, no q/k row permutation (NeoX rope). Projections,
the embedding and the LM head stay in their packed ggml blocks (``layers.gguf``); the
routed experts are streamed from host banks by the offload cache.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

import torch

from freetoken.layers.gguf import GGUFEmbedding, GGUFLinear, GGUFLMHead, gguf_linear, gguf_linear_entries
from freetoken.models.config import ModelConfig, RotaryConfig
from freetoken.models.gguf.dequant import dequantize
from freetoken.models.gguf.experts import (
    SPLIT_EXPERT_SUFFIXES,
    dummy_gguf_expert_sources,
    load_split_gguf_expert_sources,
    split_expert_quant_layout,
)

if TYPE_CHECKING:
    from freetoken.models.gguf.config import GgufConfigShim


def _require_tp1(what: str) -> None:
    from freetoken.distributed import get_tp_info

    if get_tp_info().size > 1:
        raise NotImplementedError(
            f"qwen3moe GGUF {what} supports TP=1 only "
            "(GGUF quant layers and expert banks are not tensor-parallel sharded)"
        )


def parse_gguf_config(shim: "GgufConfigShim") -> ModelConfig:
    arch = shim.model_type

    def g(key: str, default=None):
        val = shim.metadata.get(f"{arch}.{key}", default)
        if val is None:
            raise KeyError(f"missing GGUF metadata key {arch}.{key}")
        return val

    num_layers = int(g("block_count"))
    hidden = int(g("embedding_length"))
    num_q, num_kv = int(g("attention.head_count")), int(g("attention.head_count_kv"))
    head_dim = int(g("attention.key_length", hidden // num_q))
    moe_inter = int(g("expert_feed_forward_length"))
    if shim.metadata.get(f"{arch}.rope.scaling.type") not in (None, "none"):
        raise NotImplementedError(f"{shim.model_path}: rope scaling in a {arch} GGUF is not supported")
    rotary = RotaryConfig(
        head_dim=head_dim,
        rotary_dim=int(g("rope.dimension_count", head_dim)),
        max_position=int(g("context_length")),
        base=float(g("rope.freq_base")),
        scaling=None,
    )
    return ModelConfig(
        num_layers=num_layers,
        num_qo_heads=num_q,
        num_kv_heads=num_kv,
        head_dim=head_dim,
        hidden_size=hidden,
        vocab_size=int(shim.vocab_size),
        intermediate_size=int(g("feed_forward_length", 0)),
        hidden_act="silu",
        rms_norm_eps=float(g("attention.layer_norm_rms_epsilon")),
        tie_word_embeddings=bool(shim.tie_word_embeddings),
        rotary_config=rotary,
        num_experts=int(g("expert_count")),
        num_experts_per_tok=int(g("expert_used_count")),
        moe_intermediate_size=moe_inter,
        # no GGUF key carries it: llama.cpp's qwen3moe graph always renormalizes the top-k weights
        norm_topk_prob=True,
        moe_enabled=True,
        model_type=arch,
        architectures=list(shim.architectures),
        # the GGUF expert provider's tag; gguf_quant_types records the real per-layer types
        expert_quant="q4_0",
        moe_weight_format="q4_0",
        gguf_quant_types=split_expert_quant_layout(shim.model_path, num_layers, hidden, moe_inter, arch),
    )


def is_gguf_model(config: ModelConfig) -> bool:
    return getattr(config, "gguf_quant_types", None) is not None


def convert_qwen3_moe_to_gguf(model, config: ModelConfig) -> None:
    """In place: swap the attention projections, the embedding and the LM head for packed
    GGUF ops whose buffers match ``iter_gguf_weights``. Norms and the router stay dense;
    the routed experts stay on the offload cache."""
    tensors = config.gguf_quant_types["tensors"]
    H = config.hidden_size
    inner = model.model
    inner.embed_tokens = GGUFEmbedding(config.vocab_size, H, tensors["token_embd.weight"])
    if config.tie_word_embeddings:
        from freetoken.models.gemma4.gguf import GGUFTiedLMHead

        model.lm_head = GGUFTiedLMHead(inner.embed_tokens, tensors["token_embd.weight"])
    else:
        model.lm_head = GGUFLMHead(config.vocab_size, H, tensors["output.weight"])
    for i, layer in enumerate(inner.layers.op_list):
        attn = layer.self_attn
        attn.qkv_proj = gguf_linear(
            H, [attn.qo_attn_dim, attn.kv_attn_dim, attn.kv_attn_dim],
            [tensors[f"blk.{i}.attn_{part}.weight"] for part in ("q", "k", "v")],
        )
        attn.o_proj = GGUFLinear(attn.qo_attn_dim, H, tensors[f"blk.{i}.attn_output.weight"])


def _dense(t) -> torch.Tensor:
    return dequantize(t.packed().reshape(-1), t.ggml_type, torch.bfloat16).reshape(t.shape)


def iter_gguf_weights(
    model_path: str,
    device,
    *,
    include_moe_experts: bool,
    include_non_moe: bool,
) -> Iterator[tuple[str, torch.Tensor]]:
    """Yield every non-expert param: projections and the embedding as packed ``qweight``
    bytes (q/k/v fused, one run per ggml type), norms and the router dequantized."""
    from freetoken.models.gguf.reader import iter_gguf_tensors
    from freetoken.utils import cached_load_hf_config

    assert not include_moe_experts, (
        "qwen3moe GGUF routed experts load into the offload banks (load_q4_0_expert_sources)"
    )
    assert include_non_moe
    _require_tp1("weight loading")
    config = parse_gguf_config(cached_load_hf_config(model_path))
    dense = {
        "attn_norm.weight": "input_layernorm.weight",
        "ffn_norm.weight": "post_attention_layernorm.weight",
        "attn_q_norm.weight": "self_attn.q_norm.weight",
        "attn_k_norm.weight": "self_attn.k_norm.weight",
        "ffn_gate_inp.weight": "mlp.gate.weight",
    }
    qkv = ("attn_q.weight", "attn_k.weight", "attn_v.weight")
    pending: dict[int, dict[int, tuple[torch.Tensor, int]]] = {}

    for t in iter_gguf_tensors(model_path):
        name = t.name
        if name == "token_embd.weight":
            yield "model.embed_tokens.qweight", t.packed()
            continue
        if name == "output.weight":
            if not config.tie_word_embeddings:
                yield "lm_head.qweight", t.packed()
            continue
        if name == "output_norm.weight":
            yield "model.norm.weight", _dense(t)
            continue
        if not name.startswith("blk."):
            raise ValueError(f"unmapped qwen3moe GGUF tensor: {name}")
        layer = int(name.split(".")[1])
        suffix = name.split(".", 2)[2]
        base = f"model.layers.{layer}"
        if suffix in SPLIT_EXPERT_SUFFIXES:
            continue  # routed experts -> offload banks
        if suffix in dense:
            yield f"{base}.{dense[suffix]}", _dense(t)
        elif suffix == "attn_output.weight":
            yield f"{base}.self_attn.o_proj.qweight", t.packed()
        elif suffix in qkv:
            slots = pending.setdefault(layer, {})
            slots[qkv.index(suffix)] = (t.packed(), t.ggml_type)
            if len(slots) == 3:
                del pending[layer]
                yield from gguf_linear_entries(f"{base}.self_attn.qkv_proj", [slots[i] for i in range(3)])
        else:
            raise ValueError(f"unmapped qwen3moe GGUF tensor: {name}")

    assert not pending, f"incomplete GGUF qkv projections in layers {sorted(pending)}"


def load_q4_0_expert_sources(model_path: str, config: ModelConfig, *, layer_sink=None) -> dict[str, list[torch.Tensor]]:
    """Per-layer host banks of the routed experts' packed ggml bytes (``load_split_gguf_expert_sources``)."""
    _require_tp1("expert banks")
    return load_split_gguf_expert_sources(model_path, config, layer_sink=layer_sink)


def dummy_q4_0_expert_sources(config: ModelConfig) -> dict[str, list[torch.Tensor]]:
    return dummy_gguf_expert_sources(config)


__all__ = [
    "parse_gguf_config",
    "iter_gguf_weights",
    "convert_qwen3_moe_to_gguf",
    "is_gguf_model",
    "load_q4_0_expert_sources",
    "dummy_q4_0_expert_sources",
]
