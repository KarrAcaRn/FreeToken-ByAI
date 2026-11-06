from dataclasses import dataclass
from typing import Any

from freetoken.models.config import (
    FullAttentionGroupConfig, ModelConfig, RotaryConfig, ShortConvGroupConfig,
)


@dataclass(frozen=True)
class Lfm3Config(ModelConfig):
    layer_types: tuple[str, ...] = ()
    sliding_window: int = 256
    sliding_rotary: RotaryConfig | None = None
    use_sandwich_norm: bool = True


def parse_config(hf_config: Any) -> Lfm3Config:
    c = hf_config
    types = tuple(c.layer_types)
    if len(types) != c.num_hidden_layers or set(types) - {"conv", "full_attention", "sliding_attention"}:
        raise ValueError("LFM3 needs one supported layer_type per decoder layer")
    if getattr(c, "conv_bias", False):
        raise ValueError("LFM3 conv_bias=True is not supported")
    if c.conv_L_cache != 7:
        raise ValueError("LFM3 requires conv_L_cache=7")
    if c.sliding_window <= 0:
        raise ValueError("LFM3 sliding_window must be positive")
    dim = getattr(c, "head_dim", None) or c.hidden_size // c.num_attention_heads

    def rotary(kind):
        params = dict(c.rope_parameters[kind])
        if params.get("rope_type", "default") != "default":
            raise ValueError("LFM3 currently supports default rope_parameters only")
        factor = params.get("partial_rotary_factor", 1.0)
        if not 0 < factor <= 1:
            raise ValueError("LFM3 partial_rotary_factor must be in (0, 1]")
        # Liquid spaces frequencies over the whole head and zeroes their tail.
        return RotaryConfig(dim, int(dim * factor), c.max_position_embeddings,
                            params["rope_theta"], {"rope_type": "proportional"})

    full, sliding = rotary("full_attention"), rotary("sliding_attention")
    attn_ids = tuple(i for i, kind in enumerate(types) if kind != "conv")
    conv_ids = tuple(i for i, kind in enumerate(types) if kind == "conv")
    groups = []
    if attn_ids:
        groups.append(FullAttentionGroupConfig(
            "full", attn_ids, c.num_key_value_heads, dim, full,
            per_layer_sliding_window="sliding_attention" in types,
        ))
    if conv_ids:
        groups.append(ShortConvGroupConfig("linear", conv_ids, c.hidden_size, c.conv_L_cache))
    return Lfm3Config(
        num_layers=c.num_hidden_layers, num_qo_heads=c.num_attention_heads,
        num_kv_heads=c.num_key_value_heads, head_dim=dim, hidden_size=c.hidden_size,
        vocab_size=c.vocab_size, intermediate_size=c.intermediate_size,
        rms_norm_eps=c.norm_eps, rotary_config=full, hidden_act="silu",
        tie_word_embeddings=c.tie_word_embeddings, num_experts=0,
        num_experts_per_tok=0, moe_intermediate_size=0, norm_topk_prob=False,
        model_type=c.model_type, architectures=c.architectures,
        attention_groups=tuple(groups), layer_types=types,
        sliding_window=c.sliding_window, sliding_rotary=sliding,
        use_sandwich_norm=c.use_sandwich_norm,
    )
