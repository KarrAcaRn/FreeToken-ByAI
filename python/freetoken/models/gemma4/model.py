from __future__ import annotations

from typing import TYPE_CHECKING

import torch
import torch.nn.functional as F
from freetoken.core import get_global_ctx
from freetoken.layers import (
    BaseOP,
    GemmaRMSNorm,
    LinearReplicated,
    OPList,
    ParallelLMHead,
    VocabParallelEmbedding,
)
from freetoken.utils import nvtx_annotate

from freetoken.models.blocks import BaseLLMModel, embed_input_ids

from .attention import Gemma4Attention
from .moe import Gemma4DenseMLP, Gemma4MLP
from .vision import Gemma4MultimodalEmbedder, Gemma4UnifiedVisionEmbedder, Gemma4VisionModel

if TYPE_CHECKING:
    from freetoken.message import MMItem
    from freetoken.models.config import ModelConfig


class Gemma4DecoderLayer(BaseOP):
    """Gemma 4 decoder block: attention sandwich + feed-forward sandwich, scaled by a
    per-layer ``layer_scalar``. The feed-forward is the dual (shared MLP || routed MoE)
    branch for MoE checkpoints, or a single dense MLP branch for dense checkpoints.
    E-series layers add a gated per-layer-embedding residual before the scalar."""

    def __init__(self, config: ModelConfig, layer_id: int, *, prefix: str = ""):
        self._layer_id = layer_id
        self.self_attn = Gemma4Attention(config, layer_id, prefix=f"{prefix}.self_attn")
        self._has_ple = config.per_layer_input_size > 0
        if config.is_moe:
            if self._has_ple:
                raise NotImplementedError("Gemma 4 per-layer embeddings with MoE layers")
            self.feed_forward = Gemma4MLP(config, layer_id, prefix=f"{prefix}.feed_forward")
        else:
            double_wide = config.double_wide_shared_mlp and config.kv_source_layer(layer_id) is not None
            self.feed_forward = Gemma4DenseMLP(
                config,
                prefix=f"{prefix}.feed_forward",
                intermediate_size=2 * config.intermediate_size if double_wide else None,
            )

        eps = config.rms_norm_eps
        H = config.hidden_size
        self.input_layernorm = GemmaRMSNorm(H, eps=eps)
        self.post_attention_layernorm = GemmaRMSNorm(H, eps=eps)
        self.pre_feedforward_layernorm = GemmaRMSNorm(H, eps=eps)
        if self._has_ple:
            P = config.per_layer_input_size
            self.per_layer_input_gate = LinearReplicated(
                H, P, has_bias=False, quant_config=config.quant, prefix=f"{prefix}.per_layer_input_gate"
            )
            self.per_layer_projection = LinearReplicated(
                P, H, has_bias=False, quant_config=config.quant, prefix=f"{prefix}.per_layer_projection"
            )
            self.post_per_layer_input_norm = GemmaRMSNorm(H, eps=eps)

    @nvtx_annotate("Layer_{}", layer_id_field="_layer_id")
    def forward(self, x: torch.Tensor, per_layer_input: torch.Tensor | None = None) -> torch.Tensor:
        # --- attention sandwich ---
        residual = x
        h = self.input_layernorm.forward(x)
        h = self.self_attn.forward(h)
        h = self.post_attention_layernorm.forward(h)
        pre_ff, x = self.pre_feedforward_layernorm.forward_add_residual(h, residual)
        if not self._has_ple:
            return self.feed_forward.forward(pre_ff, x)
        x = self.feed_forward.forward_unscaled(pre_ff, x)
        g = F.gelu(self.per_layer_input_gate.forward(x), approximate="tanh") * per_layer_input
        g = self.post_per_layer_input_norm.forward(self.per_layer_projection.forward(g))
        return (x + g) * self.feed_forward.layer_scalar


class Gemma4Model(BaseOP):
    def __init__(self, config: ModelConfig, *, prefix: str = "model"):
        self.embed_tokens = VocabParallelEmbedding(
            num_embeddings=config.vocab_size,
            embedding_dim=config.hidden_size,
            embed_scale=config.embedding_scale,
        )
        self.layers = OPList(
            [
                Gemma4DecoderLayer(config, layer_id, prefix=f"{prefix}.layers.{layer_id}")
                for layer_id in range(config.num_layers)
            ]
        )
        self.norm = GemmaRMSNorm(config.hidden_size, eps=config.rms_norm_eps)

        self._kv_stash: dict[int, tuple[torch.Tensor, torch.Tensor]] = {}
        for layer in self.layers.op_list:
            layer.self_attn._kv_stash = self._kv_stash

        self._num_layers = config.num_layers
        self._ple_size = config.per_layer_input_size
        self._pad_token_id = config.pad_token_id or 0
        if self._ple_size:
            L, P, H = config.num_layers, config.per_layer_input_size, config.hidden_size
            # --embed-device cpu moves this (untied) table to pinned host RAM like any input embedding
            self.embed_tokens_per_layer = VocabParallelEmbedding(
                num_embeddings=config.per_layer_vocab_size,
                embedding_dim=L * P,
                embed_scale=float(P) ** 0.5,
            )
            self.per_layer_model_projection = LinearReplicated(
                H, L * P, has_bias=False, quant_config=config.quant, prefix=f"{prefix}.per_layer_model_projection"
            )
            self.per_layer_projection_norm = GemmaRMSNorm(P, eps=config.rms_norm_eps)

    def _per_layer_inputs(self, input_ids: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
        """``[T, num_layers, per_layer_input_size]``: the token's per-layer row plus a projection of its embedding."""
        batch = get_global_ctx().batch
        if batch.mm_embeds is not None:
            # multimodal rows look up the pad row, as the reference does
            input_ids = input_ids.index_fill(0, batch.mm_rows, self._pad_token_id)
        T = x.shape[0]
        tok = self.embed_tokens_per_layer.forward(input_ids).view(T, self._num_layers, self._ple_size)
        proj = self.per_layer_model_projection.forward(x) * (x.shape[-1] ** -0.5)
        proj = self.per_layer_projection_norm.forward(proj.view(T, self._num_layers, self._ple_size))
        return (proj + tok) * (2.0**-0.5)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        x = embed_input_ids(self.embed_tokens, input_ids, get_global_ctx().batch)
        ple = self._per_layer_inputs(input_ids, x) if self._ple_size else None
        for i, layer in enumerate(self.layers.op_list):
            x = layer.forward(x) if ple is None else layer.forward(x, ple[:, i])
        self._kv_stash.clear()
        return self.norm.forward(x)


class Gemma4ForCausalLM(BaseLLMModel):
    def __init__(self, config: ModelConfig):
        self.model = Gemma4Model(config)
        self.lm_head = ParallelLMHead(
            num_embeddings=config.vocab_size,
            embedding_dim=config.hidden_size,
            tie_word_embeddings=config.tie_word_embeddings,
            tied_embedding=self.model.embed_tokens if config.tie_word_embeddings else None,
            quant_config=config.quant,
            prefix="lm_head",
        )
        self._final_logit_softcapping = config.final_logit_softcapping
        super().__init__()

        # GGUF checkpoints carry native block-quantized weights: swap the dense
        # projections + embedding for GGUF-quant ops (experts stay on the offload cache).
        from .gguf import convert_gemma4_to_gguf, is_gguf_model

        if is_gguf_model(config):
            convert_gemma4_to_gguf(self, config)

    def forward(self) -> torch.Tensor:
        output = self.model.forward(get_global_ctx().batch.input_ids)
        logits = self.lm_head.forward(output)
        if self._final_logit_softcapping is not None:
            cap = self._final_logit_softcapping
            logits = torch.tanh(logits / cap) * cap
        return logits


class Gemma4ForConditionalGeneration(Gemma4ForCausalLM):
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        if config.is_multimodal:
            self.vision_tower = Gemma4VisionModel(config.vision_config)
            self.embed_vision = Gemma4MultimodalEmbedder(config.vision_config)

    def place_encoder_weights(self, mode: str) -> None:
        self.vision_tower.place_weights(mode)

    def encode(self, item: MMItem) -> torch.Tensor:
        device = self.embed_vision.embedding_projection.weight.device
        feature = item.feature.to(device, non_blocking=True)[None]
        positions = item.position_ids.to(device, non_blocking=True).long()[None]
        return self.embed_vision.forward(self.vision_tower.forward(feature, positions))


class Gemma4UnifiedForConditionalGeneration(Gemma4ForCausalLM):
    """The gemma4_unified release: no vision tower, a linear embedder turns each 48x48 super-patch into one soft token."""

    def __init__(self, config: ModelConfig):
        super().__init__(config)
        if config.is_multimodal:
            self.vision_embedder = Gemma4UnifiedVisionEmbedder(config.vision_config)
            self.embed_vision = Gemma4MultimodalEmbedder(config.vision_config)

    def place_encoder_weights(self, mode: str) -> None:
        """Nothing to stream: the embedder is a few dense tensors, resident under either placement."""
        if mode not in ("gpu", "host"):
            raise ValueError(f"unknown vision weight placement {mode!r}")

    def encode(self, item: MMItem) -> torch.Tensor:
        device = self.embed_vision.embedding_projection.weight.device
        feature = item.feature.to(device, non_blocking=True)[None]
        positions = item.position_ids.to(device, non_blocking=True).long()[None]
        return self.embed_vision.forward(self.vision_embedder.forward(feature, positions))[0]


__all__ = ["Gemma4ForCausalLM", "Gemma4ForConditionalGeneration", "Gemma4UnifiedForConditionalGeneration"]
