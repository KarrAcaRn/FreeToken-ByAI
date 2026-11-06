import torch

from freetoken.core import get_global_ctx
from freetoken.layers import BaseOP, OPList, ParallelLMHead, VocabParallelEmbedding
from freetoken.models.blocks import BaseLLMModel, GatedMLP


class Lfm3RMSNorm(BaseOP):
    def __init__(self, size: int, eps: float):
        self.weight = torch.empty(size)
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Liquid rounds the normalized value before multiplying by the raw weight.
        xf = x.float()
        return (xf * torch.rsqrt(xf.square().mean(-1, keepdim=True) + self.eps)).to(x.dtype) * self.weight


class Lfm3MLP(GatedMLP):
    def forward(self, x):
        gate, up = self.gate_up_proj.forward(x).chunk(2, dim=-1)
        # Match Liquid's bf16 rounding between SiLU and multiplication.
        return self.down_proj.forward(torch.nn.functional.silu(gate) * up)


class Lfm3DecoderLayer(BaseOP):
    def __init__(self, config, layer_id: int, *, prefix: str):
        from .attention import Lfm3Attention
        from .conv import Lfm3Conv

        self._is_conv = config.layer_types[layer_id] == "conv"
        if self._is_conv:
            self.conv = Lfm3Conv(config, layer_id, prefix=f"{prefix}.conv")
        else:
            self.self_attn = Lfm3Attention(config, layer_id, prefix=f"{prefix}.self_attn")
        self.feed_forward = Lfm3MLP(config, quant_config=config.quant, prefix=f"{prefix}.feed_forward")
        self.operator_norm = Lfm3RMSNorm(config.hidden_size, config.rms_norm_eps)
        self.ffn_norm = Lfm3RMSNorm(config.hidden_size, config.rms_norm_eps)
        self.post_operator_norm = Lfm3RMSNorm(config.hidden_size, config.rms_norm_eps) if config.use_sandwich_norm else None
        self.post_ffn_norm = Lfm3RMSNorm(config.hidden_size, config.rms_norm_eps) if config.use_sandwich_norm else None

    def forward(self, x):
        op = self.conv if self._is_conv else self.self_attn
        h = op.forward(self.operator_norm.forward(x))
        if self.post_operator_norm is not None:
            h = self.post_operator_norm.forward(h)
        x = x + h
        h = self.feed_forward.forward(self.ffn_norm.forward(x))
        if self.post_ffn_norm is not None:
            h = self.post_ffn_norm.forward(h)
        return x + h


class Lfm3Model(BaseOP):
    def __init__(self, config):
        self.embed_tokens = VocabParallelEmbedding(
            config.vocab_size, config.hidden_size, quant_config=config.quant,
            prefix="model.embed_tokens",
        )
        self.layers = OPList([
            Lfm3DecoderLayer(config, i, prefix=f"model.layers.{i}")
            for i in range(config.num_layers)
        ])
        self.embedding_norm = Lfm3RMSNorm(config.hidden_size, config.rms_norm_eps)

    def forward(self, input_ids):
        x = self.embed_tokens.forward(input_ids)
        for layer in self.layers.op_list:
            x = layer.forward(x)
        return self.embedding_norm.forward(x)


class Lfm3ForCausalLM(BaseLLMModel):
    def __init__(self, config):
        self.model = Lfm3Model(config)
        self.lm_head = ParallelLMHead(
            config.vocab_size, config.hidden_size,
            tie_word_embeddings=config.tie_word_embeddings,
            tied_embedding=self.model.embed_tokens if config.tie_word_embeddings else None,
            quant_config=config.quant, prefix="lm_head",
        )
        super().__init__()

    def forward(self):
        return self.lm_head.forward(self.model.forward(get_global_ctx().batch.input_ids))
