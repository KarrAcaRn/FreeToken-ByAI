"""Dense llama.cpp GGUFs (archs ``llama``, ``qwen2``, ``qwen3``) on the HF model classes.

Llama 3.x, Mistral (llama.cpp writes it as ``llama``), Qwen2/2.5 and dense Qwen3 share one
layer layout: fused qkv (+ bias on qwen2, + q/k norms on qwen3), o_proj, fused gate_up and
down. The projections, the embedding and the LM head stay in their packed ggml blocks
(``layers.gguf``); norms are dequantized.

Two llama.cpp conventions are undone here:

- ``llama`` q/k rows are permuted for llama.cpp's interleaved (GPT-J) rope; the HF classes
  rotate halves (NeoX), so the rows are permuted back. Each packed row holds one output row,
  so this is a row gather on the quantized bytes.
- Llama 3.x stores its rope scaling as a ``rope_freqs.weight`` tensor of per-pair frequency
  divisors instead of metadata; it becomes the ``freq_factors`` rope type.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

import torch

from freetoken.layers.gguf import GGUFEmbedding, GGUFLinear, GGUFLMHead, gguf_linear, gguf_linear_entries
from freetoken.models.config import ModelConfig, RotaryConfig
from freetoken.models.gguf.dequant import dequantize

if TYPE_CHECKING:
    from freetoken.models.gguf.config import GgufConfigShim

DENSE_GGUF_ARCHS = ("llama", "qwen2", "qwen3")
_QKV = ("attn_q", "attn_k", "attn_v")


def _require_tp1() -> None:
    from freetoken.distributed import get_tp_info

    if get_tp_info().size > 1:
        raise NotImplementedError("dense GGUF models support TP=1 only (GGUF quant layers are not sharded)")


def _dense(t) -> torch.Tensor:
    return dequantize(t.packed().reshape(-1), t.ggml_type, torch.bfloat16).reshape(t.shape)


def parse_gguf_config(shim: "GgufConfigShim") -> ModelConfig:
    from freetoken.models.gguf.reader import iter_gguf_tensors

    arch = shim.model_type
    assert arch in DENSE_GGUF_ARCHS, arch

    def g(key: str, default=None):
        val = shim.metadata.get(f"{arch}.{key}", default)
        if val is None:
            raise KeyError(f"missing GGUF metadata key {arch}.{key}")
        return val

    hidden = int(g("embedding_length"))
    num_q = int(g("attention.head_count"))
    num_kv = int(g("attention.head_count_kv", num_q))
    head_dim = int(g("attention.key_length", hidden // num_q))
    types: dict[str, int] = {}
    freq_factors = None
    for t in iter_gguf_tensors(shim.model_path):
        types[t.name] = t.ggml_type
        if t.name == "rope_freqs.weight":
            # fp32: bf16 would shift every rope frequency by up to 0.4%
            freq_factors = tuple(dequantize(t.packed().reshape(-1), t.ggml_type, torch.float32).tolist())
    if not types:
        raise NotImplementedError(f"{shim.model_path}: no GGUF tensor table; serve the .gguf file directly")
    max_position, scaling = shim.rope()
    if freq_factors and scaling:
        raise NotImplementedError(f"{shim.model_path}: YaRN on top of rope_freqs (Llama 3.x) is not supported")
    rotary = RotaryConfig(
        head_dim=head_dim,
        rotary_dim=int(g("rope.dimension_count", head_dim)),
        max_position=max_position,
        base=float(g("rope.freq_base", 10_000.0)),
        scaling={"rope_type": "freq_factors", "factors": freq_factors} if freq_factors else scaling,
    )
    return ModelConfig(
        num_layers=int(g("block_count")),
        num_qo_heads=num_q,
        num_kv_heads=num_kv,
        head_dim=head_dim,
        hidden_size=hidden,
        vocab_size=int(shim.vocab_size),
        intermediate_size=int(g("feed_forward_length")),
        hidden_act="silu",
        rms_norm_eps=float(g("attention.layer_norm_rms_epsilon")),
        tie_word_embeddings=bool(shim.tie_word_embeddings),
        rotary_config=rotary,
        num_experts=0,
        num_experts_per_tok=0,
        moe_intermediate_size=0,
        norm_topk_prob=False,
        model_type=arch,
        architectures=list(shim.architectures),
        gguf_quant_types={"tensors": types},
    )


def is_dense_gguf(config: ModelConfig) -> bool:
    return getattr(config, "gguf_quant_types", None) is not None


def convert_dense_to_gguf(model, config: ModelConfig) -> None:
    """In place: swap the projections, the embedding and the LM head for packed GGUF ops
    whose buffers match ``iter_gguf_weights``. Norms stay dense."""
    _require_tp1()
    types = config.gguf_quant_types["tensors"]
    H, inter = config.hidden_size, config.intermediate_size
    inner = model.model
    inner.embed_tokens = GGUFEmbedding(config.vocab_size, H, types["token_embd.weight"])
    if config.tie_word_embeddings:
        from freetoken.models.gemma4.gguf import GGUFTiedLMHead

        model.lm_head = GGUFTiedLMHead(inner.embed_tokens, types["token_embd.weight"])
    else:
        model.lm_head = GGUFLMHead(config.vocab_size, H, types["output.weight"])
    for i, layer in enumerate(inner.layers.op_list):
        attn, mlp = layer.self_attn, layer.mlp
        attn.qkv_proj = gguf_linear(
            H, [attn.qo_attn_dim, attn.kv_attn_dim, attn.kv_attn_dim],
            [types[f"blk.{i}.{p}.weight"] for p in _QKV],
            has_bias=f"blk.{i}.attn_q.bias" in types,
        )
        attn.o_proj = GGUFLinear(attn.qo_attn_dim, H, types[f"blk.{i}.attn_output.weight"])
        mlp.gate_up_proj = gguf_linear(H, [inter, inter], [types[f"blk.{i}.ffn_{p}.weight"] for p in ("gate", "up")])
        mlp.down_proj = GGUFLinear(inter, H, types[f"blk.{i}.ffn_down.weight"])


def unpermute_llama_rows(rows: torch.Tensor, n_head: int) -> torch.Tensor:
    """Undo llama.cpp's q/k permutation (``convert_hf_to_gguf.LlamaModel.permute``) on
    ``[out, ...]`` rows: per head, row ``2j + s`` goes back to ``s * head_dim/2 + j``."""
    out = rows.shape[0]
    return rows.reshape(n_head, out // n_head // 2, 2, *rows.shape[1:]).transpose(1, 2).reshape(rows.shape)


def iter_gguf_weights(
    model_path: str,
    device,
    *,
    include_moe_experts: bool,
    include_non_moe: bool,
) -> Iterator[tuple[str, torch.Tensor]]:
    """Yield every param: projections and the embedding as packed ``qweight`` bytes (q/k/v
    and gate/up fused, one run per ggml type), biases and norms dequantized."""
    from freetoken.models.gguf.reader import iter_gguf_tensors
    from freetoken.utils import cached_load_hf_config

    assert include_non_moe  # dense: no routed experts, so include_moe_experts has nothing to add
    _require_tp1()
    config = parse_gguf_config(cached_load_hf_config(model_path))
    permute = {"attn_q": config.num_qo_heads, "attn_k": config.num_kv_heads} if config.model_type == "llama" else {}
    dense = {
        "attn_norm.weight": "input_layernorm.weight",
        "ffn_norm.weight": "post_attention_layernorm.weight",
        "attn_q_norm.weight": "self_attn.q_norm.weight",
        "attn_k_norm.weight": "self_attn.k_norm.weight",
    }
    fused = {  # suffix -> (target, part index, part count)
        **{f"{p}.weight": ("self_attn.qkv_proj", j, 3) for j, p in enumerate(_QKV)},
        "ffn_gate.weight": ("mlp.gate_up_proj", 0, 2),
        "ffn_up.weight": ("mlp.gate_up_proj", 1, 2),
    }
    pending: dict[str, dict[int, tuple[torch.Tensor, int]]] = {}
    biases: dict[int, dict[int, torch.Tensor]] = {}

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
        if name == "rope_freqs.weight":
            continue  # folded into the rope config
        if not name.startswith("blk."):
            raise ValueError(f"unmapped {config.model_type} GGUF tensor: {name}")
        layer = int(name.split(".")[1])
        suffix = name.split(".", 2)[2]
        base = f"model.layers.{layer}"
        if suffix in dense:
            yield f"{base}.{dense[suffix]}", _dense(t)
        elif suffix == "attn_output.weight":
            yield f"{base}.self_attn.o_proj.qweight", t.packed()
        elif suffix == "ffn_down.weight":
            yield f"{base}.mlp.down_proj.qweight", t.packed()
        elif suffix in fused:
            target, j, n = fused[suffix]
            rows = t.packed()
            head = suffix.split(".")[0]
            if head in permute:
                rows = unpermute_llama_rows(rows, permute[head])
            slots = pending.setdefault(f"{base}.{target}", {})
            slots[j] = (rows, t.ggml_type)
            if len(slots) == n:
                del pending[f"{base}.{target}"]
                yield from gguf_linear_entries(f"{base}.{target}", [slots[k] for k in range(n)])
        elif suffix in {f"{p}.bias" for p in _QKV}:
            parts = biases.setdefault(layer, {})
            parts[_QKV.index(suffix.split(".")[0])] = _dense(t)
            if len(parts) == 3:
                del biases[layer]
                yield f"{base}.self_attn.qkv_proj.bias", torch.cat([parts[k] for k in range(3)])
        else:
            raise ValueError(f"unmapped {config.model_type} GGUF tensor: {name}")

    assert not pending, f"incomplete GGUF fused projections: {sorted(pending)}"
    assert not biases, f"incomplete GGUF qkv biases in layers {sorted(biases)}"


__all__ = [
    "DENSE_GGUF_ARCHS",
    "parse_gguf_config",
    "iter_gguf_weights",
    "convert_dense_to_gguf",
    "is_dense_gguf",
    "unpermute_llama_rows",
]
