from __future__ import annotations

from typing import TYPE_CHECKING

import torch
from freetoken.attention import AttentionSpec
from freetoken.core import get_global_ctx
from freetoken.layers import BaseOP, GemmaRMSNorm, LinearColParallelMerged, LinearOProj, LinearQKVMerged
from freetoken.layers.rotary import get_rope
from freetoken.models.config import FullAttentionGroupConfig, SWAAttentionGroupConfig
from freetoken.utils import nvtx_annotate

if TYPE_CHECKING:
    from freetoken.models.config import ModelConfig


class Gemma4Attention(BaseOP):
    """Gemma 4 attention for one full-context or SWA layer.

    A KV-sharing layer (E-series tail) projects only q and attends over its source layer's
    paged KV; the source hands its fresh k/v to the shared layers through ``_kv_stash``."""

    def __init__(self, config: ModelConfig, layer_id: int, *, prefix: str = ""):
        self.layer_id = layer_id
        self.kv_source = config.kv_source_layer(layer_id)
        self.publishes_kv = any(source == layer_id for _, source in config.kv_sharing)
        # {source layer id: (k, v)} for the current forward, shared by every layer of the model
        self._kv_stash: dict[int, tuple[torch.Tensor, torch.Tensor]] = {}
        group = config.attention_group_for_layer(layer_id)
        self.is_swa = isinstance(group, SWAAttentionGroupConfig)
        if not isinstance(group, (FullAttentionGroupConfig, SWAAttentionGroupConfig)):
            raise ValueError(f"Gemma4Attention does not support {group.kind!r} layers")
        rotary_config = group.rotary_config
        self.head_dim = group.head_dim
        self.num_kv_heads = group.num_kv_heads
        self.num_qo_heads = config.num_qo_heads
        self.k_eq_v = isinstance(group, FullAttentionGroupConfig) and group.k_eq_v

        self.q_dim = self.num_qo_heads * self.head_dim
        self.kv_dim = self.num_kv_heads * self.head_dim
        if self.kv_source is None:
            self.qkv_proj = LinearQKVMerged(
                config.hidden_size,
                self.head_dim,
                self.num_qo_heads,
                self.num_kv_heads,
                has_bias=False,
                quant_config=config.quant,
                prefix=f"{prefix}.qkv_proj",
            )
            self.k_norm = GemmaRMSNorm(self.head_dim, eps=config.rms_norm_eps)
            self.v_norm = GemmaRMSNorm(self.head_dim, eps=config.rms_norm_eps, with_scale=False)
        else:
            self.q_proj = LinearColParallelMerged(
                config.hidden_size,
                [self.q_dim],
                has_bias=False,
                quant_config=config.quant,
                prefix=f"{prefix}.q_proj",
            )
        # Row-parallel, as every other family with a column-parallel qkv builds o_proj:
        # each rank's attention output is its local head slice, so o_proj takes the sharded
        # input dim and all-reduces the partial sums. At TP=1 this degenerates to the previous
        # replicated behaviour exactly (div_even(x, 1) == x, all-reduce skipped), so it is a
        # no-op today and correct whenever this family gains tensor parallelism.
        self.o_proj = LinearOProj(
            self.q_dim, config.hidden_size, has_bias=False,
            quant_config=config.quant, prefix=f"{prefix}.o_proj",
        )
        self.q_norm = GemmaRMSNorm(self.head_dim, eps=config.rms_norm_eps)
        self.attn_spec = AttentionSpec(
            sliding_window=group.sliding_window if self.is_swa else None,
            sm_scale=config.attn_sm_scale,
            bidirectional_mm_blocks=self.is_swa and group.bidirectional_mm_blocks,
            kv_shared=self.kv_source is not None,
        )
        self.rotary = get_rope(
            head_dim=self.head_dim,
            rotary_dim=rotary_config.rotary_dim,
            max_position=rotary_config.max_position,
            base=rotary_config.base,
            rope_scaling=(
                tuple(rotary_config.scaling.items())
                if rotary_config.scaling
                else None
            ),
        )

    def _apply_rope(
        self,
        positions: torch.Tensor,
        q: torch.Tensor,
        k: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        positions = positions.reshape(-1)
        if positions.device != q.device or positions.dtype != torch.long:
            positions = positions.to(device=q.device, dtype=torch.long)
        q_view = q.contiguous().view(q.shape[0], -1)
        k_view = k.contiguous().view(k.shape[0], -1)
        self.rotary.forward(positions, q_view, k_view)
        return q_view.view_as(q), k_view.view_as(k)

    def _forward_shared(self, x: torch.Tensor) -> torch.Tensor:
        ctx = get_global_ctx()
        T = x.shape[0]
        q = self.q_norm.forward(self.q_proj.forward(x).view(T, self.num_qo_heads, self.head_dim))
        # rotary rotates q and k in place together; a throwaway k keeps the source's k intact
        k_dummy = q.new_empty(T, self.num_kv_heads, self.head_dim)
        q, _ = self._apply_rope(ctx.batch.positions, q, k_dummy)
        k, v = self._kv_stash[self.kv_source]
        o = ctx.attn_backend.forward(
            q.contiguous(), k, v, self.kv_source, ctx.batch, attn_spec=self.attn_spec
        )
        return self.o_proj.forward(o.reshape(T, self.num_qo_heads * self.head_dim))

    @nvtx_annotate("MHA")
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.kv_source is not None:
            return self._forward_shared(x)
        ctx = get_global_ctx()
        positions = ctx.batch.positions
        T = x.shape[0]

        qkv = self.qkv_proj.forward(x)
        q_lin, k_lin, v_lin = qkv.split(
            (self.q_dim, self.kv_dim, self.kv_dim),
            dim=-1,
        )
        del qkv
        q = q_lin.view(T, self.num_qo_heads, self.head_dim)
        k = k_lin.view(T, self.num_kv_heads, self.head_dim)
        v = v_lin.view(T, self.num_kv_heads, self.head_dim)

        q = self.q_norm.forward(q)
        k = self.k_norm.forward(k)
        v = self.v_norm.forward(v)

        q, k = self._apply_rope(positions, q, k)

        k = k.reshape(T, self.num_kv_heads * self.head_dim).contiguous()
        v = v.reshape(T, self.num_kv_heads * self.head_dim).contiguous()
        if self.publishes_kv:
            self._kv_stash[self.layer_id] = (k, v)
        o = ctx.attn_backend.forward(
            q.contiguous(),
            k,
            v,
            self.layer_id,
            ctx.batch,
            attn_spec=self.attn_spec,
        )
        o = o.reshape(T, self.num_qo_heads * self.head_dim)
        return self.o_proj.forward(o)


__all__ = ["Gemma4Attention"]
