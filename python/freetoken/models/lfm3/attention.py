from dataclasses import replace
from functools import cache

import torch

from freetoken.attention.base import AttentionSpec
from freetoken.core import get_global_ctx
from freetoken.layers import LinearColParallelMerged
from freetoken.layers.rotary import RotaryEmbedding
from freetoken.models.qwen3.attention import Qwen3Attention

from .model import Lfm3RMSNorm


@cache
def _liquid_rope(rope, dtype):
    # HF casts cos/sin to the activation dtype before its fp32 rotation.
    table = rope._cos_sin_cache.to(dtype).float()
    result = RotaryEmbedding(rope.head_size, rope.rotary_dim, table)
    if dtype == torch.float32:
        from freetoken.kernel.triton.rope import apply_rope_with_cos_sin_cache_inplace
        result.apply_rope_with_cos_sin_cache_inplace = apply_rope_with_cos_sin_cache_inplace
    return result


class Lfm3Attention(Qwen3Attention):
    def __init__(self, config, layer_id: int, *, prefix: str):
        sliding = config.layer_types[layer_id] == "sliding_attention"
        rotary = config.sliding_rotary if sliding else config.rotary_config
        super().__init__(replace(config, rotary_config=rotary), layer_id, prefix=prefix)
        self.rotary = _liquid_rope(self.rotary, torch.get_default_dtype())
        self.q_norm = Lfm3RMSNorm(self.head_dim, config.rms_norm_eps)
        self.k_norm = Lfm3RMSNorm(self.head_dim, config.rms_norm_eps)
        self.gate_proj = LinearColParallelMerged(
            config.hidden_size, [config.num_qo_heads], has_bias=False,
            quant_config=config.quant, prefix=f"{prefix}.gate_proj",
        )
        # HF and Triton both use k > q - window, including the current token.
        self._spec = AttentionSpec(sliding_window=config.sliding_window if sliding else None)

    def forward(self, x):
        ctx = get_global_ctx()
        q, k, v = self.qkv_proj.forward(x).split(
            [self.qo_attn_dim, self.kv_attn_dim, self.kv_attn_dim], dim=-1,
        )
        q = self.q_norm.forward(q.reshape(-1, self.num_qo_heads, self.head_dim))
        k = self.k_norm.forward(k.reshape(-1, self.num_kv_heads, self.head_dim))
        q, k = self.rotary.forward(
            ctx.batch.get_attn_positions(), q.flatten(1), k.flatten(1),
        )
        o = ctx.attn_backend.forward(
            q.view(-1, self.num_qo_heads, self.head_dim), k, v.contiguous(),
            self.layer_id, ctx.batch, attn_spec=self._spec,
        )
        gate = self.gate_proj.forward(x).sigmoid().unsqueeze(-1)
        o = o.reshape(-1, self.num_qo_heads, self.head_dim) * gate
        return self.o_proj.forward(o.flatten(1))
