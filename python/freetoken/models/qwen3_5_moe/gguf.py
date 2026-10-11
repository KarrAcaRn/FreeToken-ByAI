"""Qwen3.5 / 3.6 MoE (llama.cpp arch ``qwen35moe``) served from a GGUF file.

The geometry is the HF qwen3_5_moe model's (GatedDeltaNet layers with a full-attention
layer every ``full_attention_interval``, routed experts plus a gated shared expert), so
this builds the same ``ModelConfig`` as ``config.parse_config`` from GGUF metadata.
Projections and the embedding stay in their packed ggml blocks (``layers.gguf``), the
routed experts are streamed from host banks by the offload cache.

llama.cpp's converter (``conversion/qwen.py``) rewrites four things the loader undoes:

* ``ssm_a`` holds ``A = -exp(A_log)``; the loader yields ``log(-A)``.
* every RMSNorm weight except the GDN gated norm is stored as ``1 + w``, the form
  ``GemmaRMSNorm`` reads, so unlike ``weight.py`` nothing is added.
* with fewer K than V heads the V heads are tiled (``[k0v0, k1v0, .., k0v1, ..]``) instead
  of grouped by K head (``_LinearAttentionVReorderBase``). Rows of the packed in-projections
  are permuted back at load; ``ssm_out`` carries V along its columns, which cuts through
  quant blocks, so its input activation is tiled at run time instead.
* the parts of a fused projection may be stored in different ggml types (the GDN beta /
  alpha rows stay F32 next to a quantized qkv); ``gguf_linear`` keeps one GEMM per run.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

import torch

from freetoken.layers.gguf import GGUFLinear, gguf_linear, gguf_linear_entries
from freetoken.models.config import (
    FullAttentionGroupConfig,
    LinearGatedDeltaGroupConfig,
    ModelConfig,
    RotaryConfig,
)
from freetoken.models.gguf.dequant import dequantize
from freetoken.models.gguf.experts import (
    SPLIT_EXPERT_SUFFIXES,
    load_split_gguf_expert_sources,
    split_expert_quant_layout,
)

if TYPE_CHECKING:
    from freetoken.models.gguf.config import GgufConfigShim


def _require_tp1(what: str) -> None:
    from freetoken.distributed import get_tp_info

    if get_tp_info().size > 1:
        raise NotImplementedError(
            f"qwen35moe GGUF {what} supports TP=1 only "
            "(GGUF quant layers and expert banks are not tensor-parallel sharded)"
        )


def parse_gguf_config(shim: "GgufConfigShim") -> ModelConfig:
    arch = shim.model_type

    def g(key: str, default=None):
        val = shim.metadata.get(f"{arch}.{key}", default)
        if val is None:
            raise KeyError(f"missing GGUF metadata key {arch}.{key}")
        return val

    num_layers = int(g("block_count")) - int(g("nextn_predict_layers", 0))
    hidden = int(g("embedding_length"))
    num_q, num_kv = int(g("attention.head_count")), int(g("attention.head_count_kv"))
    head_dim = int(g("attention.key_length"))
    num_experts = int(g("expert_count"))
    moe_inter = int(g("expert_feed_forward_length"))

    # GDN: group_count = K heads, time_step_rank = V heads, state_size = the shared head dim
    state = int(g("ssm.state_size"))
    k_heads, v_heads = int(g("ssm.group_count")), int(g("ssm.time_step_rank"))
    if v_heads * state != int(g("ssm.inner_size")) or v_heads % k_heads:
        raise ValueError(
            f"{shim.model_path}: GDN geometry K={k_heads} V={v_heads} state={state} "
            f"inner={g('ssm.inner_size')} is not the qwen35moe layout"
        )
    interval = int(g("full_attention_interval"))
    full_ids = tuple(i for i in range(num_layers) if (i + 1) % interval == 0)
    linear_ids = tuple(i for i in range(num_layers) if (i + 1) % interval != 0)

    # text-only: the interleaved mrope sections collapse to plain partial NeoX rope
    rotary = RotaryConfig(
        head_dim=head_dim,
        rotary_dim=int(g("rope.dimension_count")),
        max_position=int(g("context_length")),
        base=float(g("rope.freq_base")),
        scaling=None,
    )
    groups = tuple(sorted(
        (
            FullAttentionGroupConfig(
                name="full", layer_ids=full_ids, num_kv_heads=num_kv, head_dim=head_dim, rotary_config=rotary,
            ),
            LinearGatedDeltaGroupConfig(
                name="linear",
                layer_ids=linear_ids,
                num_key_heads=k_heads,
                num_value_heads=v_heads,
                key_head_dim=state,
                value_head_dim=state,
                conv_kernel_dim=int(g("ssm.conv_kernel")),
                output_gate="silu",
            ),
        ),
        key=lambda grp: grp.layer_ids[0] if grp.layer_ids else 1 << 30,
    ))
    return ModelConfig(
        num_layers=num_layers,
        num_qo_heads=num_q,
        num_kv_heads=num_kv,
        head_dim=head_dim,
        hidden_size=hidden,
        vocab_size=int(shim.vocab_size),
        intermediate_size=0,
        hidden_act="silu",
        rms_norm_eps=float(g("attention.layer_norm_rms_epsilon")),
        tie_word_embeddings=bool(shim.tie_word_embeddings),
        rotary_config=rotary,
        num_experts=num_experts,
        num_experts_per_tok=int(g("expert_used_count")),
        moe_intermediate_size=moe_inter,
        shared_expert_intermediate_size=int(g("expert_shared_feed_forward_length")),
        norm_topk_prob=True,
        moe_enabled=True,
        use_qk_norm=True,
        model_type=arch,
        architectures=list(shim.architectures),
        attention_groups=groups,
        # the GGUF expert provider's tag; gguf_quant_types records the real per-layer types
        expert_quant="q4_0",
        moe_weight_format="q4_0",
        gguf_quant_types=split_expert_quant_layout(shim.model_path, num_layers, hidden, moe_inter, arch),
    )


def is_gguf_model(config: ModelConfig) -> bool:
    return getattr(config, "gguf_quant_types", None) is not None


# --------------------------------------------------------------------------------------
# V-head order
# --------------------------------------------------------------------------------------


def untile_v(t: torch.Tensor, dim: int, k_heads: int, v_per_k: int, head_dim: int) -> torch.Tensor:
    """Inverse of llama.cpp's ``_reorder_v_heads`` along ``dim`` (tiled -> grouped by K head)."""
    shape = list(t.shape)
    dim %= len(shape)
    view = shape[:dim] + [v_per_k, k_heads, head_dim] + shape[dim + 1:]
    return t.reshape(view).transpose(dim, dim + 1).contiguous().reshape(shape)


class GGUFTiledVInputLinear(GGUFLinear):
    """``ssm_out``: its packed columns are in llama.cpp's tiled V-head order, so the grouped
    GDN output is tiled before the GEMM (a column permutation would split quant blocks)."""

    def __init__(self, in_features: int, out_features: int, quant_type: int, k_heads: int, v_per_k: int):
        super().__init__(in_features, out_features, quant_type)
        self._k_heads = k_heads
        self._v_per_k = v_per_k

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        n = x.shape[0]
        x = x.view(n, self._k_heads, self._v_per_k, -1).transpose(1, 2).reshape(n, -1)
        return super().forward(x)


# --------------------------------------------------------------------------------------
# Model op swap
# --------------------------------------------------------------------------------------


def _tensor_type(config: ModelConfig, name: str) -> int:
    try:
        return config.gguf_quant_types["tensors"][name]
    except KeyError:
        raise ValueError(f"qwen35moe GGUF has no tensor {name!r}") from None


def convert_qwen3_5_to_gguf(model, config: ModelConfig) -> None:
    """In place: swap the dense projections, the embedding and the LM head for packed GGUF
    ops whose buffers match ``iter_gguf_weights``. Norms, routers, the shared-expert gate and
    the GDN conv / A_log / dt_bias stay dense; the routed experts stay on the offload cache."""
    from freetoken.layers.gguf import GGUFEmbedding, GGUFLMHead

    def qt(name: str) -> int:
        return _tensor_type(config, name)

    H = config.hidden_size
    inner = model.model
    inner.embed_tokens = GGUFEmbedding(config.vocab_size, H, qt("token_embd.weight"))
    if config.tie_word_embeddings:
        from freetoken.models.gemma4.gguf import GGUFTiedLMHead

        model.lm_head = GGUFTiedLMHead(inner.embed_tokens, qt("token_embd.weight"))
    else:
        model.lm_head = GGUFLMHead(config.vocab_size, H, qt("output.weight"))

    for i, layer in enumerate(inner.layers.op_list):
        blk = f"blk.{i}"
        if config.is_linear_layer(i):
            gdn = layer.linear_attn
            assert not gdn._split_in_proj
            gdn.in_proj = gguf_linear(H, list(gdn._in_proj_split), [
                qt(f"{blk}.{part}.weight") for part in ("attn_qkv", "attn_gate", "ssm_beta", "ssm_alpha")
            ])
            v_per_k = gdn.num_v_heads // gdn.num_k_heads
            out_type = qt(f"{blk}.ssm_out.weight")
            gdn.out_proj = (
                GGUFTiledVInputLinear(gdn.value_dim, H, out_type, gdn.num_k_heads, v_per_k)
                if v_per_k > 1 else GGUFLinear(gdn.value_dim, H, out_type)
            )
        else:
            attn = layer.self_attn
            attn.qkv_proj = gguf_linear(H, list(attn._qkv_split), [
                qt(f"{blk}.attn_{part}.weight") for part in ("q", "k", "v")
            ])
            attn.o_proj = GGUFLinear(attn.qo_attn_dim, H, qt(f"{blk}.attn_output.weight"))
        shared = layer.mlp.shared_expert
        inter = config.shared_expert_intermediate_size
        shared.gate_up_proj = gguf_linear(
            H, [inter, inter], [qt(f"{blk}.ffn_gate_shexp.weight"), qt(f"{blk}.ffn_up_shexp.weight")]
        )
        shared.down_proj = GGUFLinear(inter, H, qt(f"{blk}.ffn_down_shexp.weight"))


# --------------------------------------------------------------------------------------
# Weight loading
# --------------------------------------------------------------------------------------


def _dense(t, dtype: torch.dtype = torch.bfloat16) -> torch.Tensor:
    """A GgufTensor dequantized to a dense tensor of its torch shape."""
    return dequantize(t.packed().reshape(-1), t.ggml_type, dtype).reshape(t.shape)


def iter_gguf_weights(
    model_path: str,
    device,
    *,
    include_moe_experts: bool,
    include_non_moe: bool,
) -> Iterator[tuple[str, torch.Tensor]]:
    """Yield every non-expert param: projections and the embedding as packed ``qweight``
    bytes (V-head rows un-tiled), the rest dequantized."""
    from freetoken.models.gguf.reader import iter_gguf_tensors
    from freetoken.utils import cached_load_hf_config

    assert not include_moe_experts, (
        "qwen35moe GGUF routed experts load into the offload banks (load_q4_0_expert_sources)"
    )
    assert include_non_moe
    _require_tp1("weight loading")
    config = parse_gguf_config(cached_load_hf_config(model_path))
    gdn = config.linear_attention_group()
    K, D = gdn.num_key_heads, gdn.value_head_dim
    R = gdn.num_value_heads // K
    qk_rows = 2 * K * gdn.key_head_dim

    def untile(t: torch.Tensor, dim: int, head_dim: int) -> torch.Tensor:
        return untile_v(t, dim, K, R, head_dim) if R > 1 else t

    # fused projections: target -> ordered GGUF parts, emitted once every part arrived
    fused_parts = {
        "self_attn.qkv_proj": ("attn_q.weight", "attn_k.weight", "attn_v.weight"),
        "linear_attn.in_proj": ("attn_qkv.weight", "attn_gate.weight", "ssm_beta.weight", "ssm_alpha.weight"),
        "mlp.shared_expert.gate_up_proj": ("ffn_gate_shexp.weight", "ffn_up_shexp.weight"),
    }
    part_of = {sfx: (target, idx) for target, sfxs in fused_parts.items() for idx, sfx in enumerate(sfxs)}
    plain = {
        "attn_output.weight": "self_attn.o_proj.qweight",
        "ssm_out.weight": "linear_attn.out_proj.qweight",
        "ffn_down_shexp.weight": "mlp.shared_expert.down_proj.qweight",
    }
    # already 1 + w (llama.cpp folds the Gemma shift in), or plain weights
    dense = {
        "attn_norm.weight": "input_layernorm.weight",
        "post_attention_norm.weight": "post_attention_layernorm.weight",
        "attn_q_norm.weight": "self_attn.q_norm.weight",
        "attn_k_norm.weight": "self_attn.k_norm.weight",
        "ssm_norm.weight": "linear_attn.norm.weight",
        "ffn_gate_inp.weight": "mlp.gate.weight",
    }
    pending: dict[tuple[int, str], dict[int, tuple[torch.Tensor, int]]] = {}

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
            raise ValueError(f"unmapped qwen35moe GGUF tensor: {name}")
        layer = int(name.split(".")[1])
        suffix = name.split(".", 2)[2]
        if layer >= config.num_layers or suffix in SPLIT_EXPERT_SUFFIXES:
            continue  # NextN / MTP block (not served), routed experts (banks)
        base = f"model.layers.{layer}"

        if suffix in dense:
            yield f"{base}.{dense[suffix]}", _dense(t)
        elif suffix == "ffn_gate_inp_shexp.weight":
            yield f"{base}.mlp.shared_expert_gate.weight", _dense(t).reshape(1, -1)
        elif suffix == "ssm_a":
            a = untile(_dense(t, torch.float32), 0, 1)
            if not bool((a < 0).all()):
                raise ValueError(f"{name}: expected llama.cpp's A = -exp(A_log) < 0, got max {a.max().item()}")
            yield f"{base}.linear_attn.A_log", torch.log(-a)
        elif suffix == "ssm_dt.bias":
            yield f"{base}.linear_attn.dt_bias", untile(_dense(t, torch.float32), 0, 1)
        elif suffix == "ssm_conv1d.weight":
            w = _dense(t)  # [conv_dim, kernel]
            w = torch.cat([w[:qk_rows], untile(w[qk_rows:], 0, D)])
            yield f"{base}.linear_attn.conv1d.weight", w.unsqueeze(1)
        elif suffix in plain:
            yield f"{base}.{plain[suffix]}", t.packed()
        elif suffix in part_of:
            target, idx = part_of[suffix]
            packed = t.packed()
            # whole packed rows move, never a block, so the permutation is exact
            if suffix == "attn_qkv.weight":
                packed = torch.cat([packed[:qk_rows], untile(packed[qk_rows:], 0, D)])
            elif suffix == "attn_gate.weight":
                packed = untile(packed, 0, D)
            elif suffix in ("ssm_beta.weight", "ssm_alpha.weight"):
                packed = untile(packed, 0, 1)
            slots = pending.setdefault((layer, target), {})
            slots[idx] = (packed, t.ggml_type)
            if len(slots) == len(fused_parts[target]):
                del pending[(layer, target)]
                yield from gguf_linear_entries(f"{base}.{target}", [slots[i] for i in range(len(slots))])
        else:
            raise ValueError(f"unmapped qwen35moe GGUF tensor: {name}")

    assert not pending, f"incomplete fused GGUF projections: {sorted(pending)}"


# --------------------------------------------------------------------------------------
# Routed-expert host banks for the offload cache
# --------------------------------------------------------------------------------------


def load_q4_0_expert_sources(model_path: str, config: ModelConfig, *, layer_sink=None) -> dict[str, list[torch.Tensor]]:
    """Per-layer host banks of the routed experts' packed ggml bytes (``load_split_gguf_expert_sources``)."""
    _require_tp1("expert banks")
    return load_split_gguf_expert_sources(model_path, config, layer_sink=layer_sink)


def dummy_q4_0_expert_sources(config: ModelConfig) -> dict[str, list[torch.Tensor]]:
    from freetoken.models.gguf.experts import dummy_gguf_expert_sources

    return dummy_gguf_expert_sources(config)


__all__ = [
    "parse_gguf_config",
    "iter_gguf_weights",
    "convert_qwen3_5_to_gguf",
    "is_gguf_model",
    "load_q4_0_expert_sources",
    "dummy_q4_0_expert_sources",
    "untile_v",
]
