"""Gemma 4 GGUF adapter: build the FreeToken ``ModelConfig`` from GGUF metadata.

The GGUF checkpoint's geometry is identical to the HF gemma4 model (hybrid
SWA/full attention with ``k_eq_v`` full layers, 128 routed experts + shared MLP,
final-logit softcap; the E2B/E4B add per-layer embeddings, KV-sharing layers and
a double-wide MLP), so this produces the *same* ``ModelConfig`` as
``gemma4.config.parse_config`` -- only the source is GGUF KV metadata instead of a
HF config object. transformers' own GGUF->config conversion is rejected by the
gemma4 strict dataclass (per-layer ``num_key_value_heads`` array), so we read the
metadata directly. ``expert_quant`` keeps the legacy ``"q4_0"`` provider tag, while
the tensor table records the actual dense and per-layer routed-expert GGML types.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

import torch

from freetoken.models.config import (
    FullAttentionGroupConfig,
    ModelConfig,
    RotaryConfig,
    SWAAttentionGroupConfig,
)
from freetoken.models.gguf.dequant import (
    GGML_BF16,
    GGML_F16,
    GGML_F32,
    GGML_Q4_0,
    GGML_Q6_K,
    dequantize,
    row_bytes,
)
from freetoken.models.gguf.experts import (
    gguf_expert_specs as _gguf_expert_specs,
    uses_mixed_gguf_experts as _uses_mixed_gguf_experts,
)

if TYPE_CHECKING:
    from freetoken.models.gguf.config import GgufConfigShim


def _full_rotary_dim(shim: "GgufConfigShim", full_head_dim: int) -> int:
    """Rotated width of the full-attention layers, recovered from ``rope_freqs.weight``.

    llama.cpp writes ``rope.dimension_count = full head_dim`` and carries gemma4's
    partial_rotary_factor as a divisor tensor instead: ``[1.0] * n_rot//2 + [1e30] * rest``,
    which drives the unrotated tail's frequencies to zero (ggml ops.cpp ``theta / ff``).
    Count the untouched entries to get the rotated width back.
    """
    from freetoken.models.gguf.reader import iter_gguf_tensors

    for t in iter_gguf_tensors(shim.model_path):
        if t.name == "rope_freqs.weight":  # F32, so the packed bytes ARE the values
            freqs = t.packed().reshape(-1).view(torch.float32)
            return int((freqs == 1.0).sum().item()) * 2
    # A metadata-only GGUF (an FTW dir's source_metadata.gguf) has no tensor table. Every
    # released gemma4 sets partial_rotary_factor 0.25 on the full layers, and the converter
    # asserts rope_type == "proportional" (llama.cpp conversion/gemma.py).
    return full_head_dim // 4


def _gguf_quant_layout(model_path: str, num_layers: int, num_experts: int) -> dict | None:
    """Discover native tensor types without touching the tensor payloads.

    ``tensors`` maps every non-expert tensor name to its ggml type (K-quant files mix
    types inside one fused projection). A metadata-only FTW source has no tensor table,
    in which case ``None`` keeps the historical Q4_0/Q6_K defaults.
    """
    from freetoken.models.gguf.reader import iter_gguf_tensors

    tensors: dict[str, int] = {}
    expert_gate_up = [None] * num_layers
    expert_down = [None] * num_layers
    expert_gate_up_bytes = [None] * num_layers
    expert_down_bytes = [None] * num_layers

    for tensor in iter_gguf_tensors(model_path):
        suffix = tensor.name.split(".", 2)[2] if tensor.name.startswith("blk.") else None
        if suffix == "ffn_gate_up_exps.weight":
            layer = int(tensor.name.split(".")[1])
            expert_gate_up[layer] = tensor.ggml_type
            expert_gate_up_bytes[layer] = tensor.packed().numel()
        elif suffix == "ffn_down_exps.weight":
            layer = int(tensor.name.split(".")[1])
            expert_down[layer] = tensor.ggml_type
            expert_down_bytes[layer] = tensor.packed().numel()
        else:
            tensors[tensor.name] = tensor.ggml_type

    if not tensors:
        return None
    if "token_embd.weight" not in tensors:
        raise ValueError("gemma4 GGUF has no token_embd.weight")

    layout: dict[str, object] = {"embedding": tensors["token_embd.weight"], "tensors": tensors}
    for layer in range(num_layers):
        missing = [
            sfx for sfx in ("attn_q.weight", "attn_output.weight", "ffn_gate.weight", "ffn_up.weight", "ffn_down.weight")
            if f"blk.{layer}.{sfx}" not in tensors
        ]
        if missing:
            raise ValueError(f"gemma4 GGUF layer {layer} lacks {missing}")
    if not num_experts:  # dense checkpoint: no routed-expert tensors to lay out
        return layout
    for role, values in (("expert_gate_up", expert_gate_up), ("expert_down", expert_down)):
        missing = [i for i, value in enumerate(values) if value is None]
        if missing:
            raise ValueError(f"gemma4 GGUF {role} tensors are missing in layers {missing}")
        layout[role] = tuple(values)
    # Total packed bytes per expert. The loader stores each expert contiguously in
    # a fixed-width cache slot and passes the slot stride to the CUDA kernel.
    layout["expert_gate_up_bytes"] = tuple(int(n) // num_experts for n in expert_gate_up_bytes)
    layout["expert_down_bytes"] = tuple(int(n) // num_experts for n in expert_down_bytes)
    return layout


def _kv_sharing(swa_pattern: list[bool], num_shared: int) -> tuple[tuple[int, int], ...]:
    """Mirror of ``gemma4.config._kv_sharing``: each of the last ``num_shared`` layers reads the
    KV of the last non-shared layer of its attention type."""
    num_layers = len(swa_pattern)
    first_shared = num_layers - num_shared
    if num_shared <= 0 or first_shared <= 0:
        return ()
    last_owner = {is_swa: i for i, is_swa in enumerate(swa_pattern[:first_shared])}
    return tuple((i, last_owner[swa_pattern[i]]) for i in range(first_shared, num_layers))


def _ffn_widths(ffn, num_layers: int, shared: set[int]) -> tuple[int, bool]:
    """``(intermediate_size, double_wide_shared_mlp)`` from llama.cpp's ``feed_forward_length``,
    a per-layer array when the KV-sharing layers run a 2x MLP (gemma-4-E2B)."""
    widths = [int(x) for x in ffn] if hasattr(ffn, "__len__") else [int(ffn)] * num_layers
    base = widths[0]
    double_wide = any(w == 2 * base for w in widths)
    want = [2 * base if double_wide and i in shared else base for i in range(num_layers)]
    if widths != want:
        raise NotImplementedError(f"gemma4 GGUF per-layer feed_forward_length {widths} is not a supported layout")
    return base, double_wide


def parse_gguf_config(shim: "GgufConfigShim") -> ModelConfig:
    m = shim.metadata

    def g(key: str):
        val = m.get(f"gemma4.{key}")
        if val is None:
            raise KeyError(f"missing GGUF metadata key gemma4.{key}")
        return val

    num_layers = int(g("block_count"))
    hidden = int(g("embedding_length"))
    num_qo_heads = int(g("attention.head_count"))
    # llama.cpp writes head_count_kv as a SCALAR when every layer shares a KV head
    # count, and only as a per-layer array when they differ (e.g. gemma-4-E2B: 1).
    _kv = g("attention.head_count_kv")
    kv_per_layer = [int(x) for x in _kv] if hasattr(_kv, "__len__") else [int(_kv)] * num_layers
    # True -> sliding-window (SWA) layer, False -> full attention.
    swa_pattern = [bool(x) for x in g("attention.sliding_window_pattern")]
    assert len(swa_pattern) == num_layers, "sliding_window_pattern length != block_count"

    swa_layer_ids = tuple(i for i, is_swa in enumerate(swa_pattern) if is_swa)
    full_layer_ids = tuple(i for i, is_swa in enumerate(swa_pattern) if not is_swa)

    swa_head_dim = int(g("attention.key_length_swa"))
    full_head_dim = int(g("attention.key_length"))
    swa_kv = int(kv_per_layer[swa_layer_ids[0]]) if swa_layer_ids else int(kv_per_layer[0])
    full_kv = int(kv_per_layer[full_layer_ids[0]]) if full_layer_ids else int(kv_per_layer[0])

    layout = _gguf_quant_layout(shim.model_path, num_layers, int(m.get("gemma4.expert_count", 0) or 0))
    # E-series (gemma-4-E2B/E4B): per-layer embeddings and a tail of layers that read an earlier layer's KV
    per_layer_input_size = int(m.get("gemma4.embedding_length_per_layer_input", 0) or 0)
    kv_sharing = _kv_sharing(swa_pattern, int(m.get("gemma4.attention.shared_kv_layers", 0) or 0))
    if (per_layer_input_size or kv_sharing) and layout is None:
        raise NotImplementedError(
            f"{shim.model_path}: no GGUF tensor table (a converted FTW dir?); serve the E-series .gguf directly"
        )
    shared = {layer for layer, _ in kv_sharing}
    intermediate_size, double_wide = _ffn_widths(g("feed_forward_length"), num_layers, shared)
    if layout is None:
        # the non-E-series layout (the E-series is refused above without a tensor table)
        k_eq_v = True
    else:
        # llama.cpp reuses k as v when a full layer stores no attn_v (31B / 26B / 12B); the E-series stores one
        owners = [i for i in full_layer_ids if i not in shared]
        k_eq_v = not any(f"blk.{i}.attn_v.weight" in layout["tensors"] for i in owners)

    pad_token_id = m.get("tokenizer.ggml.padding_token_id")
    max_pos = int(g("context_length"))
    # Dense Gemma-4 checkpoints (gemma-4-12B-it, gemma-4-31B-it) carry no expert fields
    # in their GGUF metadata; only MoE members (e.g. Gemma-4-26B-A4B) do. Mirror the HF
    # side (gemma4.config.parse_config): default the expert fields to 0 and derive
    # moe_enabled from them instead of assuming every GGUF is MoE.
    num_experts = int(m.get("gemma4.expert_count", 0) or 0)
    num_experts_per_tok = int(m.get("gemma4.expert_used_count", 0) or 0)
    moe_intermediate_size = int(m.get("gemma4.expert_feed_forward_length", 0) or 0)
    moe_enabled = num_experts > 0
    full_rotary = RotaryConfig(
        head_dim=full_head_dim,
        rotary_dim=_full_rotary_dim(shim, full_head_dim),
        max_position=max_pos,
        base=float(g("rope.freq_base")),
        # gemma4's full layers are partial-rotary ("proportional"): the tail dims must come
        # out unrotated. llama.cpp expresses that with rope.dimension_count == full head_dim
        # plus a rope_freqs divisor tensor, so a plain "default" rope here would rotate dims
        # that have to be identity (conversion/gemma.py generate_extra_tensors).
        scaling={"rope_type": "proportional"},
    )
    swa_rotary = RotaryConfig(
        head_dim=swa_head_dim,
        rotary_dim=int(g("rope.dimension_count_swa")),
        max_position=max_pos,
        base=float(g("rope.freq_base_swa")),
        scaling=None,
    )

    return ModelConfig(
        num_layers=num_layers,
        num_qo_heads=num_qo_heads,
        num_kv_heads=full_kv,
        head_dim=full_head_dim,
        hidden_size=hidden,
        vocab_size=int(shim.vocab_size),
        intermediate_size=intermediate_size,
        hidden_act="gelu_tanh",
        rms_norm_eps=float(g("attention.layer_norm_rms_epsilon")),
        tie_word_embeddings=bool(shim.tie_word_embeddings),
        rotary_config=full_rotary,
        num_experts=num_experts,
        num_experts_per_tok=num_experts_per_tok,
        moe_intermediate_size=moe_intermediate_size,
        norm_topk_prob=True,
        model_type="gemma4",
        architectures=list(shim.architectures),
        moe_enabled=moe_enabled,
        # Native-Q4_0 offload-cache path for the routed experts (MoE checkpoints only).
        expert_quant="q4_0" if moe_enabled else "none",
        moe_weight_format="q4_0" if moe_enabled else "none",
        gguf_quant_types=layout,
        use_qk_norm=True,
        attn_sm_scale=1.0,
        final_logit_softcapping=float(g("final_logit_softcapping")),
        embedding_scale=float(hidden) ** 0.5,
        per_layer_input_size=per_layer_input_size,
        per_layer_vocab_size=int(shim.vocab_size) if per_layer_input_size else 0,
        kv_sharing=kv_sharing,
        double_wide_shared_mlp=double_wide,
        pad_token_id=None if pad_token_id is None else int(pad_token_id),
        attention_groups=(
            FullAttentionGroupConfig(
                name="full",
                layer_ids=full_layer_ids,
                num_kv_heads=full_kv,
                head_dim=full_head_dim,
                rotary_config=full_rotary,
                k_eq_v=k_eq_v,
            ),
            SWAAttentionGroupConfig(
                name="swa",
                layer_ids=swa_layer_ids,
                num_kv_heads=swa_kv,
                head_dim=swa_head_dim,
                rotary_config=swa_rotary,
                sliding_window=int(g("attention.sliding_window")),
            ),
        ),
    )


# --------------------------------------------------------------------------------------
# Weight loading: GGUF tensor names -> FreeToken gemma4 module params.
# --------------------------------------------------------------------------------------

# Per-layer 1:1 norm/scale tensors (gguf suffix -> freetoken module-relative name). All
# are tiny F32 tensors dequantized to bf16.
_LAYER_SCALAR_MAP = {
    "attn_norm.weight": "input_layernorm.weight",
    "attn_q_norm.weight": "self_attn.q_norm.weight",
    "attn_k_norm.weight": "self_attn.k_norm.weight",
    "post_attention_norm.weight": "post_attention_layernorm.weight",
    "ffn_norm.weight": "pre_feedforward_layernorm.weight",
    "pre_ffw_norm_2.weight": "feed_forward.pre_feedforward_layernorm_2.weight",
    "post_ffw_norm.weight": "feed_forward.post_feedforward_layernorm.weight",
    "post_ffw_norm_1.weight": "feed_forward.post_feedforward_layernorm_1.weight",
    "post_ffw_norm_2.weight": "feed_forward.post_feedforward_layernorm_2.weight",
    "layer_output_scale.weight": "feed_forward.layer_scalar",
    "ffn_gate_inp.weight": "feed_forward.router.proj.weight",
    "ffn_gate_inp.scale": "feed_forward.router.scale",
    "ffn_down_exps.scale": "feed_forward.router.per_expert_scale",
}
# Expert weight tensors (handled by the offload bank loader, not iter_gguf_weights).
_EXPERT_SUFFIXES = ("ffn_gate_up_exps.weight", "ffn_down_exps.weight")


def _to_bf16(t) -> torch.Tensor:
    """Dequantize a GgufTensor (F32/F16/Q*) to a dense bf16 tensor of its torch shape."""
    flat = dequantize(t.packed().reshape(-1), t.ggml_type, torch.bfloat16)
    return flat.reshape(t.shape)


def _require_tp1(what: str) -> None:
    """GGUF quant layers / expert banks are not sharded; reject TP>1 with a clear
    error instead of failing later on a confusing shape mismatch (mirrors the HF
    gemma4 loader's TP=1 restriction)."""
    from freetoken.distributed import get_tp_info

    if get_tp_info().size > 1:
        raise NotImplementedError(
            f"gemma4 GGUF {what} currently supports TP=1 only "
            "(GGUF quant layers and expert banks are not tensor-parallel sharded)."
        )


def _unquantized(quant_type: int) -> bool:
    return quant_type in (GGML_F32, GGML_F16, GGML_BF16)


def iter_gguf_weights(
    model_path: str,
    device,
    *,
    include_moe_experts: bool,
    include_non_moe: bool,
) -> Iterator[tuple[str, torch.Tensor]]:
    """Yield (param_name, tensor) for every non-expert gemma4 param.

    Quantized projections (attention q/k/v/o, shared-MLP gate/up/down) and the
    embedding stay in their native packed block layout and are yielded as ``.qweight``
    (uint8); norms / router / per-layer scalars dequantize to bf16. q/k/v and gate/up
    are fused by concatenating packed rows along the output dim (same input dim ->
    same ``row_bytes``), one run per ggml type. Routed experts are served from the
    offload cache, so they are skipped here (asserts the offload contract like the
    other MoE models). The E-series per-layer-embedding tensors stay packed when
    quantized and load as bf16 otherwise (``convert_gemma4_to_gguf`` builds the same).
    """
    from freetoken.layers.gguf import gguf_linear_entries
    from freetoken.models.gguf.reader import iter_gguf_tensors
    from freetoken.utils import cached_load_hf_config

    config = parse_gguf_config(cached_load_hf_config(model_path))
    # A dense checkpoint has no routed experts, so the engine asking for them is moot.
    assert not (include_moe_experts and config.moe_enabled), (
        "gemma4 GGUF stores experts as Q4_0 and only supports the offload backend; "
        "experts are loaded into the offload cache via load_q4_0_expert_sources()."
    )
    assert include_non_moe
    _require_tp1("weight loading")

    # Full-attention layers ship no attn_v (k reused as v); SWA layers do. Knowing which
    # is which lets us emit the fused qkv as soon as its parts are present.
    k_eq_v_layers = {
        lid
        for lid in range(config.num_layers)
        if isinstance(config.attention_group_for_layer(lid), FullAttentionGroupConfig)
        and config.attention_group_for_layer(lid).k_eq_v
    }
    kv_shared_layers = {layer for layer, _ in config.kv_sharing}
    # E-series tensors that become a dense bf16 op when the file stores them unquantized
    ple_globals = {
        "per_layer_token_embd.weight": "model.embed_tokens_per_layer",
        "per_layer_model_proj.weight": "model.per_layer_model_projection",
    }
    ple_layer = {"inp_gate.weight": "per_layer_input_gate", "proj.weight": "per_layer_projection"}

    # Per-layer fusion buffers: layer -> {slot: (packed[out, row_bytes], ggml type)}.
    qkv_buf: dict[int, dict[str, tuple[torch.Tensor, int]]] = {}
    gate_up_buf: dict[int, dict[str, tuple[torch.Tensor, int]]] = {}

    def layer_of(name: str) -> int:
        return int(name.split(".")[1])

    def packed_or_dense(target: str, t) -> tuple[str, torch.Tensor]:
        if _unquantized(t.ggml_type):
            return f"{target}.weight", _to_bf16(t)
        return f"{target}.qweight", t.packed()

    for t in iter_gguf_tensors(model_path):
        name = t.name
        if name == "token_embd.weight":
            yield "model.embed_tokens.qweight", t.packed()  # Q6_K packed table
            continue
        if name == "output_norm.weight":
            yield "model.norm.weight", _to_bf16(t)
            continue
        if name == "per_layer_proj_norm.weight":
            yield "model.per_layer_projection_norm.weight", _to_bf16(t)
            continue
        if name in ple_globals:
            yield packed_or_dense(ple_globals[name], t)
            continue
        if name == "rope_freqs.weight":
            continue  # rope frequencies recomputed in-engine
        if not name.startswith("blk."):
            continue
        if any(name.endswith(sfx) for sfx in _EXPERT_SUFFIXES):
            continue  # routed experts -> offload banks

        layer = layer_of(name)
        suffix = name.split(".", 2)[2]  # after "blk.N."
        base = f"model.layers.{layer}"

        if layer in kv_shared_layers:
            # a KV-sharing layer attends over its source's KV: only its q projection is used
            if suffix in ("attn_k.weight", "attn_v.weight", "attn_k_norm.weight"):
                continue
            if suffix == "attn_q.weight":
                yield f"{base}.self_attn.q_proj.qweight", t.packed()
                continue
        if suffix == "post_norm.weight":
            yield f"{base}.post_per_layer_input_norm.weight", _to_bf16(t)
            continue
        if suffix in ple_layer:
            yield packed_or_dense(f"{base}.{ple_layer[suffix]}", t)
            continue

        if suffix in _LAYER_SCALAR_MAP:
            rel = _LAYER_SCALAR_MAP[suffix]
            tensor = _to_bf16(t)
            if rel.endswith("layer_scalar"):
                tensor = tensor.reshape(1)
            yield f"{base}.{rel}", tensor
            continue

        # Quantized projections: keep packed; fuse q/k/v and gate/up.
        part = (t.packed(), t.ggml_type)
        if suffix == "attn_q.weight":
            qkv_buf.setdefault(layer, {})["q"] = part
        elif suffix == "attn_k.weight":
            qkv_buf.setdefault(layer, {})["k"] = part
        elif suffix == "attn_v.weight":
            qkv_buf.setdefault(layer, {})["v"] = part
        elif suffix == "ffn_gate.weight":
            gate_up_buf.setdefault(layer, {})["gate"] = part
        elif suffix == "ffn_up.weight":
            gate_up_buf.setdefault(layer, {})["up"] = part
        elif suffix == "attn_output.weight":
            yield f"{base}.self_attn.o_proj.qweight", t.packed()
        elif suffix == "ffn_down.weight":
            yield f"{base}.feed_forward.shared_mlp.down_proj.qweight", t.packed()
        else:
            raise ValueError(f"unmapped gemma4 GGUF tensor: {name}")

        # Emit fused qkv once all parts are present: k_eq_v full layers reuse k as v
        # (no attn_v tensor), SWA layers wait for their separate attn_v.
        slots = qkv_buf.get(layer)
        if slots is not None and "q" in slots and "k" in slots:
            if layer in k_eq_v_layers:
                v = slots["k"]
            elif "v" in slots:
                v = slots["v"]
            else:
                v = None
            if v is not None:
                yield from gguf_linear_entries(f"{base}.self_attn.qkv_proj", [slots["q"], slots["k"], v])
                del qkv_buf[layer]
        gu = gate_up_buf.get(layer)
        if gu is not None and "gate" in gu and "up" in gu:
            yield from gguf_linear_entries(f"{base}.feed_forward.shared_mlp.gate_up_proj", [gu["gate"], gu["up"]])
            del gate_up_buf[layer]

    assert not qkv_buf, f"incomplete qkv groups: {sorted(qkv_buf)}"
    assert not gate_up_buf, f"incomplete gate_up groups: {sorted(gate_up_buf)}"


# --------------------------------------------------------------------------------------
# Model layer swap: dense bf16 Linear/Embedding -> native GGUF-quant ops.
# --------------------------------------------------------------------------------------


def is_gguf_model(config: ModelConfig) -> bool:
    """True when the model was parsed from a GGUF checkpoint (native-quant path). A dense GGUF
    has no Q4_0 experts, so its recorded tensor layout is what marks it."""
    return (
        getattr(config, "moe_weight_format", None) == "q4_0"
        or getattr(config, "gguf_quant_types", None) is not None
    )


class GGUFTiedLMHead:
    """Tied LM head over a native Q6_K embedding table (logits via ggml matmul).

    Holds only a reference to the GGUF embedding (no params of its own -> empty
    state_dict), mirroring ``ParallelLMHead`` with ``tie_word_embeddings``. TP=1 only.
    """

    def __init__(self, embedding, quant_type: int):
        self._embedding = embedding
        self._quant_type = quant_type

    def state_dict(self, *, prefix: str = "", result=None):
        return result if result is not None else {}

    def load_state_dict(self, state_dict, *, prefix: str = "", _internal: bool = False):
        state_dict.pop(f"{prefix}.weight", None)
        state_dict.pop(f"{prefix}.bias", None)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        from freetoken.core import get_global_ctx
        from freetoken.layers.gguf import fused_mul_mat_gguf

        batch = get_global_ctx().batch
        if batch.is_prefill:
            indices = batch.attn_metadata.get_last_indices(batch.size)
            x = x[indices].contiguous()
        return fused_mul_mat_gguf(x, self._embedding.qweight, self._quant_type)


def convert_gemma4_to_gguf(model, config: ModelConfig) -> None:
    """In place: replace gemma4's dense projections + embedding with native GGUF ops.

    Quantized in the checkpoint -> swapped: attention qkv/o, shared-MLP gate_up/down
    and the token embedding (also the tied LM head), plus the E-series per-layer
    embedding table and projections when the file quantized them. Left as dense
    bf16 (F32 in the GGUF): the router gate, all RMSNorms, the per-layer scalars, and
    the routed experts (served from the offload cache).
    """
    from freetoken.layers.gguf import GGUFEmbedding, GGUFLinear, gguf_linear

    layout = config.gguf_quant_types
    tensors = layout["tensors"] if layout is not None else None

    def qt(name: str) -> int:
        return GGML_Q4_0 if tensors is None else tensors[name]

    def swap_fused(owner, attr, sizes: list[int], names: list[str]):
        in_features = getattr(owner, attr).weight.shape[1]
        setattr(owner, attr, gguf_linear(in_features, sizes, [qt(n) for n in names]))

    def swap_linear(owner, attr, name: str, *, keep_dense: bool = False):
        quant_type = qt(name)
        if keep_dense and _unquantized(quant_type):
            return
        lin = getattr(owner, attr)
        out_features, in_features = lin.weight.shape
        setattr(owner, attr, GGUFLinear(in_features, out_features, quant_type, has_bias=lin.bias is not None))

    embedding_type = layout["embedding"] if layout is not None else GGML_Q6_K
    inner = model.model
    embed = GGUFEmbedding(
        num_embeddings=config.vocab_size,
        embedding_dim=config.hidden_size,
        quant_type=embedding_type,
        embed_scale=config.embedding_scale,
    )
    inner.embed_tokens = embed

    for layer_id, layer in enumerate(inner.layers.op_list):
        blk = f"blk.{layer_id}"
        attn = layer.self_attn
        if attn.kv_source is not None:
            swap_linear(attn, "q_proj", f"{blk}.attn_q.weight")
        else:
            # a k_eq_v layer's v rows are a copy of its k rows
            v = "attn_k" if getattr(config.attention_group_for_layer(layer_id), "k_eq_v", False) else "attn_v"
            swap_fused(
                attn, "qkv_proj", [attn.q_dim, attn.kv_dim, attn.kv_dim],
                [f"{blk}.attn_q.weight", f"{blk}.attn_k.weight", f"{blk}.{v}.weight"],
            )
        swap_linear(attn, "o_proj", f"{blk}.attn_output.weight")
        mlp = layer.feed_forward.shared_mlp
        inter = mlp.down_proj.weight.shape[1]
        swap_fused(mlp, "gate_up_proj", [inter, inter], [f"{blk}.ffn_gate.weight", f"{blk}.ffn_up.weight"])
        swap_linear(mlp, "down_proj", f"{blk}.ffn_down.weight")
        if config.per_layer_input_size:
            swap_linear(layer, "per_layer_input_gate", f"{blk}.inp_gate.weight", keep_dense=True)
            swap_linear(layer, "per_layer_projection", f"{blk}.proj.weight", keep_dense=True)

    if config.per_layer_input_size:
        swap_linear(inner, "per_layer_model_projection", "per_layer_model_proj.weight", keep_dense=True)
        table_type = qt("per_layer_token_embd.weight")
        if not _unquantized(table_type):
            inner.embed_tokens_per_layer = GGUFEmbedding(
                num_embeddings=config.per_layer_vocab_size,
                embedding_dim=config.num_layers * config.per_layer_input_size,
                quant_type=table_type,
                embed_scale=float(config.per_layer_input_size) ** 0.5,
            )

    if config.tie_word_embeddings:
        model.lm_head = GGUFTiedLMHead(embed, embedding_type)


# --------------------------------------------------------------------------------------
# Routed-expert host banks (native Q4_0) for the offload cache.
# --------------------------------------------------------------------------------------

def load_q4_0_expert_sources(
    model_path: str, config: ModelConfig, *, layer_sink=None
) -> dict[str, list[torch.Tensor]]:
    """Per-layer host banks of the routed experts' native Q4_0 block bytes.

    ``gate_up`` is one ``[E, 2I, H//32*18]`` tensor per layer and ``down`` one
    ``[E, H, I//32*18]`` per layer (independent :class:`HostBank` allocations) -- each
    expert's packed rows verbatim from the GGUF (no dequant), whole layers arriving in
    one shot (gate_up + down = 2 writes/layer), so the offload cache streams whole
    experts to the ggml MoE kernels.

    ``layer_sink=None`` (serving): pin each layer's two banks as they complete via an
    internally-owned :class:`PinPipeline` (or, on a CUDA-less host, allocate the mmap
    banks but never pin -- the CPU executor reads them pageable). ``layer_sink`` given
    (converter): the completion tracker fires into it instead -- nothing here is pinned,
    and the sink may release banks it has written out, so the returned tensors are only
    valid until then (the caller owns that tradeoff).
    """
    from freetoken.models.gguf.reader import iter_gguf_tensors
    from freetoken.moe.host_banks import LayerCompletionTracker, PinPipeline, alloc_layer_banks

    _require_tp1("expert banks")
    L, E = config.num_layers, config.num_experts
    H, I = config.hidden_size, config.moe_intermediate_size
    h_bytes, i_bytes = row_bytes(H, GGML_Q4_0), row_bytes(I, GGML_Q4_0)
    mixed = _uses_mixed_gguf_experts(config)
    if mixed and layer_sink is not None:
        raise NotImplementedError(
            "converting mixed-type GGUF expert banks to FTW is not supported yet; "
            "serve the source GGUF directly"
        )
    hb = alloc_layer_banks(_gguf_expert_specs(config), L)  # lazy anon mmaps (unpinned)
    banks = {name: [b.tensor for b in hb[name]] for name in hb}
    seen_gu, seen_dn = set(), set()

    def _load(sink) -> None:
        tracker = LayerCompletionTracker(2, hb, sink) if sink is not None else None  # gate_up + down
        for t in iter_gguf_tensors(model_path):
            if not t.name.startswith("blk."):
                continue
            layer = int(t.name.split(".")[1])
            if t.name.endswith("ffn_gate_up_exps.weight"):
                packed = t.packed().reshape(E, -1)
                if mixed:
                    banks["gate_up"][layer][:, : packed.shape[1]].copy_(packed)
                else:
                    banks["gate_up"][layer].copy_(packed.reshape(E, 2 * I, h_bytes))
                seen_gu.add(layer)
            elif t.name.endswith("ffn_down_exps.weight"):
                packed = t.packed().reshape(E, -1)
                if mixed:
                    banks["down"][layer][:, : packed.shape[1]].copy_(packed)
                else:
                    banks["down"][layer].copy_(packed.reshape(E, H, i_bytes))
                seen_dn.add(layer)
            else:
                continue
            if tracker is not None:
                tracker.note(layer)

    if layer_sink is not None:
        _load(layer_sink)
    elif torch.cuda.is_available():
        with PinPipeline() as pins:
            _load(pins)
    else:
        _load(None)  # CUDA-less: mmap banks stay pageable, never pinned

    want = set(range(L))
    assert seen_gu == want and seen_dn == want, (
        f"missing Q4_0 expert layers: gate_up {sorted(want - seen_gu)}, "
        f"down {sorted(want - seen_dn)}"
    )
    return banks


def dummy_q4_0_expert_sources(config: ModelConfig) -> dict[str, list[torch.Tensor]]:
    from freetoken.models.gguf.experts import dummy_gguf_expert_sources

    return dummy_gguf_expert_sources(config)


__all__ = [
    "parse_gguf_config",
    "iter_gguf_weights",
    "convert_gemma4_to_gguf",
    "is_gguf_model",
    "load_q4_0_expert_sources",
    "dummy_q4_0_expert_sources",
]
