from __future__ import annotations

import torch
import torch.nn.functional as F
from freetoken.layers import BaseOP, OPList, RMSNorm, LinearReplicated
from freetoken.layers.rotary import get_rope

from .config import DFlashConfig


def _dflash_causal_context_block_mask(
    context_len: int,
    block_len: int,
    device: torch.device,
) -> torch.Tensor:
    mask = torch.ones((block_len, context_len + block_len), dtype=torch.bool, device=device)
    mask[:, context_len:] = torch.tril(
        torch.ones((block_len, block_len), dtype=torch.bool, device=device)
    )
    return mask


def _dflash_context_block_mask(
    context_len: int,
    block_len: int,
    device: torch.device,
    *,
    layer_type: str,
    is_causal: bool | None,
    sliding_window: int | None,
) -> torch.Tensor | None:
    causal = layer_type == "sliding_attention" if is_causal is None else is_causal
    window = sliding_window if layer_type == "sliding_attention" else None
    if not causal and window is None:
        return None

    query_position = context_len + torch.arange(block_len, device=device)[:, None]
    key_position = torch.arange(context_len + block_len, device=device)[None, :]
    visible = torch.ones((block_len, context_len + block_len), dtype=torch.bool, device=device)
    if causal:
        visible &= key_position <= query_position
    if window is not None:
        visible &= query_position - key_position < window
        if not causal:
            visible &= key_position - query_position < window
    return visible


class _DFlashAttention(BaseOP):
    """Draft attention over committed target context plus a causal draft block."""

    def __init__(self, config: DFlashConfig, layer_id: int):
        self.layer_id = layer_id
        self.head_dim = config.head_dim
        self.num_qo_heads = config.num_attention_heads
        self.num_kv_heads = config.num_key_value_heads
        self.qo_attn_dim = self.num_qo_heads * self.head_dim
        self.kv_attn_dim = self.num_kv_heads * self.head_dim
        self.layer_type = (
            config.layer_types[layer_id]
            if layer_id < len(config.layer_types)
            else "full_attention"
        )
        self.is_causal = config.is_causal
        self.sliding_window = config.sliding_window
        dtype = torch.bfloat16

        self.q_proj = LinearReplicated(config.hidden_size, self.qo_attn_dim, has_bias=False)
        self.k_proj = LinearReplicated(config.hidden_size, self.kv_attn_dim, has_bias=False)
        self.v_proj = LinearReplicated(config.hidden_size, self.kv_attn_dim, has_bias=False)
        self.o_proj = LinearReplicated(self.qo_attn_dim, config.hidden_size, has_bias=False)
        self.q_proj.weight = self.q_proj.weight.to(dtype)
        self.k_proj.weight = self.k_proj.weight.to(dtype)
        self.v_proj.weight = self.v_proj.weight.to(dtype)
        self.o_proj.weight = self.o_proj.weight.to(dtype)

        self.q_norm = RMSNorm(self.head_dim, eps=config.rms_norm_eps)
        self.k_norm = RMSNorm(self.head_dim, eps=config.rms_norm_eps)
        self.q_norm.weight = self.q_norm.weight.to(dtype)
        self.k_norm.weight = self.k_norm.weight.to(dtype)

        self.rotary = get_rope(
            head_dim=self.head_dim,
            rotary_dim=self.head_dim,
            max_position=config.max_position_embeddings,
            base=config.rope_theta,
        )
        # Scratch for the in-place rope kernel's unused counterpart argument;
        # avoids two torch.empty_like allocations per layer per draft call.
        self._rope_scratch_q: torch.Tensor | None = None
        self._rope_scratch_k: torch.Tensor | None = None

    @staticmethod
    def _rope_scratch_for(scratch: torch.Tensor | None, ref: torch.Tensor) -> torch.Tensor:
        if (
            scratch is None
            or scratch.shape != ref.shape
            or scratch.dtype != ref.dtype
            or scratch.device != ref.device
        ):
            scratch = torch.empty_like(ref)
        return scratch

    def to(self, device):
        """Move all weights and buffers (including rotary cos_sin_cache) to device."""
        for name, param in self.__dict__.items():
            if isinstance(param, torch.Tensor) and param.device.type != device.type:
                setattr(self, name, param.to(device))
            elif hasattr(param, 'weight') and isinstance(getattr(param, 'weight', None), torch.Tensor):
                if param.weight.device.type != device.type:
                    param.weight = param.weight.to(device)
                if getattr(param, 'bias', None) is not None and param.bias.device.type != device.type:
                    param.bias = param.bias.to(device)
            # Move _cos_sin_cache in RotaryEmbedding (private attr, starts with _)
            if isinstance(param, BaseOP):
                for attr_name, attr_val in param.__dict__.items():
                    if isinstance(attr_val, torch.Tensor) and attr_val.device.type != device.type:
                        setattr(param, attr_name, attr_val.to(device))
        return self

    def _apply_rope_inplace(self, positions, query, key):
        if self.rotary._cos_sin_cache.device.type != query.device.type:
            self.rotary._cos_sin_cache = self.rotary._cos_sin_cache.to(query.device)
        from freetoken.kernel.backend import is_flashinfer_installed
        if is_flashinfer_installed():
            from flashinfer import apply_rope_with_cos_sin_cache_inplace as _apply_rope
        else:
            from freetoken.kernel.triton.rope import apply_rope_with_cos_sin_cache_inplace as _apply_rope
        _apply_rope(
            positions=positions,
            query=query,
            key=key,
            head_size=self.head_dim,
            cos_sin_cache=self.rotary._cos_sin_cache,
            is_neox=self.rotary.is_neox,
        )

    def project_context_kv(self, context, positions):
        context_k = self.k_proj.forward(context).view(-1, self.num_kv_heads, self.head_dim)
        context_v = self.v_proj.forward(context).view(-1, self.num_kv_heads, self.head_dim)
        self.k_norm.forward_inplace(context_k)
        context_k_flat = context_k.reshape(-1, self.kv_attn_dim)
        self._apply_rope_inplace(
            positions,
            torch.empty_like(context_k_flat),
            context_k_flat,
        )
        return context_k_flat.view(-1, self.num_kv_heads, self.head_dim), context_v

    def forward(self, hidden_states, positions, context_kvs, attn_masks):
        """``hidden_states`` holds B blocks of equal length; block ``b`` attends to its own
        context ``context_kvs[b]`` (with ``attn_masks[b]``) and causally/bidirectionally to
        its own rows."""
        q = self.q_proj.forward(hidden_states)
        block_k = self.k_proj.forward(hidden_states)
        block_v = self.v_proj.forward(hidden_states)

        q = q.view(-1, self.num_qo_heads, self.head_dim)
        block_k = block_k.view(-1, self.num_kv_heads, self.head_dim)
        block_v = block_v.view(-1, self.num_kv_heads, self.head_dim)

        self.q_norm.forward_inplace(q)
        self.k_norm.forward_inplace(block_k)

        q_flat = q.reshape(-1, self.qo_attn_dim)
        self._rope_scratch_q = self._rope_scratch_for(self._rope_scratch_q, q_flat)
        self._apply_rope_inplace(positions, q_flat, self._rope_scratch_q)
        q = q_flat.view(-1, self.num_qo_heads, self.head_dim)

        block_k_flat = block_k.reshape(-1, self.kv_attn_dim)
        self._rope_scratch_k = self._rope_scratch_for(self._rope_scratch_k, block_k_flat)
        self._apply_rope_inplace(
            positions,
            self._rope_scratch_k,
            block_k_flat,
        )
        block_k = block_k_flat.view(-1, self.num_kv_heads, self.head_dim)

        group_size = self.num_qo_heads // self.num_kv_heads
        block_len = hidden_states.shape[0] // len(context_kvs)
        scale = self.head_dim ** -0.5
        if attn_masks is None:
            return self.o_proj.forward(self._fi_attention(q, block_k, block_v, context_kvs, block_len, scale))
        outs = []
        for b, ((context_k, context_v), attn_mask) in enumerate(zip(context_kvs, attn_masks)):
            rows = slice(b * block_len, (b + 1) * block_len)
            k_expanded = torch.cat([context_k, block_k[rows]], dim=0).repeat_interleave(group_size, dim=1)
            v_expanded = torch.cat([context_v, block_v[rows]], dim=0).repeat_interleave(group_size, dim=1)
            # SDPA expects [batch, num_heads, seq, head_dim]
            q_t = q[rows].transpose(0, 1).unsqueeze(0)  # [1, num_qo, block_len, head_dim]
            k_t = k_expanded.transpose(0, 1).unsqueeze(0)  # [1, num_qo, ctx_len + block_len, head_dim]
            v_t = v_expanded.transpose(0, 1).unsqueeze(0)
            mask = attn_mask.unsqueeze(0).unsqueeze(0) if attn_mask is not None else None
            attn = F.scaled_dot_product_attention(q_t, k_t, v_t, attn_mask=mask, scale=scale)
            outs.append(attn.squeeze(0).transpose(0, 1))
        out = torch.cat(outs, dim=0).reshape(-1, self.qo_attn_dim)
        return self.o_proj.forward(out)


    def fi_mask(self) -> tuple[bool, int]:
        """(causal, window_left) of this layer's mask in FlashInfer's terms: queries sit at the
        end of the keys, and a window w keeps keys with q_pos - k_pos < w."""
        causal = self.layer_type == "sliding_attention" if self.is_causal is None else bool(self.is_causal)
        window = self.sliding_window if self.layer_type == "sliding_attention" else None
        return causal, (window - 1 if window is not None else -1)

    def _fi_attention(self, q, block_k, block_v, context_kvs, block_len, scale):
        """The SDPA loop's result without expanding K/V to every query head or building a
        mask: FlashInfer reads the grouped heads directly."""
        from flashinfer import single_prefill_with_kv_cache

        causal, window_left = self.fi_mask()
        outs = []
        for b, (context_k, context_v) in enumerate(context_kvs):
            rows = slice(b * block_len, (b + 1) * block_len)
            outs.append(single_prefill_with_kv_cache(
                q[rows], torch.cat([context_k, block_k[rows]]), torch.cat([context_v, block_v[rows]]),
                causal=causal, sm_scale=scale, window_left=window_left,
            ))
        out = outs[0] if len(outs) == 1 else torch.cat(outs)
        return out.reshape(-1, self.qo_attn_dim)


class _Fp8RowLinear(BaseOP):
    """W8A16 replacement for a draft ``LinearReplicated``: e4m3 weight with one fp32 scale per
    output row (``--speculative-draft-quant fp8``). Halves the draft's VRAM and read traffic;
    the target verifies every token, so this can only move the acceptance rate."""

    def __init__(self, weight: torch.Tensor):
        w = weight.float()
        scale = w.abs().amax(dim=1).clamp(min=1e-12) / torch.finfo(torch.float8_e4m3fn).max
        self.weight = (w / scale[:, None]).to(torch.float8_e4m3fn)
        self.weight_scale = scale.contiguous()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        from freetoken.kernel.triton.fp8_pertensor_linear import fp8_pertensor_linear

        return fp8_pertensor_linear(x, self.weight, self.weight_scale)


def _grouped_dynamic_convolve(
    hidden: torch.Tensor, dynamic: torch.Tensor, base: torch.Tensor, group_size: int,
    block_len: int | None = None,
) -> torch.Tensor:
    """Causal conv over the positions of each block: ``hidden`` [B * T, H] (B blocks of
    ``block_len`` T, default one block), ``dynamic`` [B * T, K, groups] (per-position,
    per-group taps), ``base`` [K, H] (static per-channel taps)."""
    rows, hidden_size = hidden.shape
    length = block_len or rows
    groups = hidden_size // group_size
    blocks = hidden.view(rows // length, length, groups, group_size)
    dynamic = dynamic.reshape(rows // length, length, base.shape[0], groups, 1)
    output = torch.zeros_like(blocks)
    for offset in range(base.shape[0]):
        values = blocks if offset == 0 else F.pad(blocks[:, :-offset], (0, 0, 0, 0, offset, 0))
        output = output + base[offset].view(1, 1, groups, group_size).to(hidden.dtype) * values
        output = torch.addcmul(output, dynamic[:, :, offset], values)
    return output.view_as(hidden)


class _GroupedDynamicCausalConv(BaseOP):
    """DFlash2's two-tap dynamic convolution: ``prepare`` convolves the normed input and returns
    the taps for ``finish``, which convolves the sublayer output."""

    def __init__(self, hidden_size: int, kernel_size: int, group_size: int):
        self.kernel_size = kernel_size
        self.group_size = group_size
        self.groups = hidden_size // group_size
        self.base_kernel = torch.empty(2, kernel_size, hidden_size, dtype=torch.bfloat16)
        self.kernel_projection = LinearReplicated(hidden_size, 2 * kernel_size * self.groups, has_bias=False)
        self.kernel_projection.weight = self.kernel_projection.weight.to(torch.bfloat16)

    def prepare(self, hidden: torch.Tensor, block_len: int) -> tuple[torch.Tensor, torch.Tensor]:
        dynamic = self.kernel_projection.forward(hidden).view(-1, 2, self.kernel_size, self.groups)
        out = _grouped_dynamic_convolve(hidden, dynamic[:, 0], self.base_kernel[0], self.group_size, block_len)
        return out, dynamic[:, 1]

    def finish(self, hidden: torch.Tensor, dynamic: torch.Tensor, block_len: int) -> torch.Tensor:
        return _grouped_dynamic_convolve(hidden, dynamic, self.base_kernel[1], self.group_size, block_len)


class _CandidateSelector(BaseOP):
    """DFlash2's path selector: each draft position keeps its top-k tokens; a low-rank
    predecessor x successor score, conditioned on the draft hidden state, picks one coherent
    path through them, starting from the verified anchor token."""

    def __init__(self, config: DFlashConfig):
        self.top_k = int(config.selector_top_k)
        rank = int(config.selector_rank)
        self.predecessor_codebook = torch.empty(config.vocab_size, rank, dtype=torch.bfloat16)
        self.successor_codebook = torch.empty(config.vocab_size, rank, dtype=torch.bfloat16)
        self.hidden_projection = LinearReplicated(config.hidden_size, rank, has_bias=False)
        self.hidden_projection.weight = self.hidden_projection.weight.to(torch.bfloat16)

    def select(
        self,
        hidden: torch.Tensor,             # [B, P, hidden] draft hidden states of the candidate positions
        logits: torch.Tensor,             # [B, P, vocab]
        anchor_id: torch.Tensor,          # [B] the verified token before each block
        temperature: torch.Tensor | None,  # [B]; None = greedy
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        """(paths [B, P], draft distributions [B, P, vocab] over the chosen candidates or None
        when greedy). 2-D ``hidden``/``logits`` are one block."""
        single = hidden.dim() == 2
        if single:
            hidden, logits = hidden.unsqueeze(0), logits.unsqueeze(0)
        unary, candidates = torch.topk(logits, self.top_k, dim=-1, sorted=False)  # [B, P, k]
        hidden = self.hidden_projection.forward(hidden)
        successors = F.embedding(candidates, self.successor_codebook)  # [B, P, k, rank]
        predecessor = anchor_id[: hidden.shape[0]].to(candidates.dtype)  # [B]
        temp = None if temperature is None else temperature.reshape(-1, 1)
        path, q_rows = [], []
        for position in range(hidden.shape[1]):
            pred = F.embedding(predecessor, self.predecessor_codebook) * hidden[:, position]  # [B, rank]
            scores = unary[:, position] + (
                successors[:, position] @ pred.to(successors.dtype).unsqueeze(-1)).squeeze(-1)
            if temp is None:
                index = torch.argmax(scores, dim=-1, keepdim=True)
            else:
                q = torch.softmax(scores.float() / temp, dim=-1)
                index = torch.multinomial(q, 1)
                q_rows.append(torch.zeros(
                    (q.shape[0], logits.shape[-1]), dtype=q.dtype, device=q.device,
                ).scatter_(1, candidates[:, position], q))
            predecessor = candidates[:, position].gather(1, index)[:, 0]
            path.append(predecessor)
        paths = torch.stack(path, dim=1)
        probs = torch.stack(q_rows, dim=1) if q_rows else None
        if single:
            return paths[0], (probs[0] if probs is not None else None)
        return paths, probs


class _DFlashMLP(BaseOP):
    """Standard SwiGLU MLP for draft model."""

    def __init__(self, config: DFlashConfig):
        dtype = torch.bfloat16
        self.gate_proj = LinearReplicated(config.hidden_size, config.intermediate_size, has_bias=False)
        self.up_proj = LinearReplicated(config.hidden_size, config.intermediate_size, has_bias=False)
        self.down_proj = LinearReplicated(config.intermediate_size, config.hidden_size, has_bias=False)
        self.gate_proj.weight = self.gate_proj.weight.to(dtype)
        self.up_proj.weight = self.up_proj.weight.to(dtype)
        self.down_proj.weight = self.down_proj.weight.to(dtype)

    def to(self, device):
        """Move all weights and buffers to device."""
        for name, param in self.__dict__.items():
            if isinstance(param, torch.Tensor) and param.device.type != device.type:
                setattr(self, name, param.to(device))
            elif isinstance(param, BaseOP):
                param.to(device)
        return self

    def forward(self, x):
        return self.down_proj.forward(F.silu(self.gate_proj.forward(x)) * self.up_proj.forward(x))


class _DFlashDecoderLayer(BaseOP):
    """One draft decoder layer: cross-attention + MLP with pre-norm."""

    def __init__(self, config: DFlashConfig, layer_id: int):
        self.self_attn = _DFlashAttention(config, layer_id)
        self.mlp = _DFlashMLP(config)
        self.input_layernorm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.post_attention_layernorm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.input_layernorm.weight = self.input_layernorm.weight.to(torch.bfloat16)
        self.post_attention_layernorm.weight = self.post_attention_layernorm.weight.to(torch.bfloat16)
        self.attention_conv: _GroupedDynamicCausalConv | None = None
        self.mlp_conv: _GroupedDynamicCausalConv | None = None
        if config.is_dflash2:
            self.attention_conv = _GroupedDynamicCausalConv(
                config.hidden_size, config.conv_kernel_size, config.conv_group_size)
            self.mlp_conv = _GroupedDynamicCausalConv(
                config.hidden_size, config.conv_kernel_size, config.conv_group_size)

    def to(self, device):
        """Move all weights and buffers to device."""
        for name, param in self.__dict__.items():
            if isinstance(param, torch.Tensor) and param.device.type != device.type:
                setattr(self, name, param.to(device))
            elif isinstance(param, BaseOP):
                param.to(device)
        return self

    def forward(
        self,
        hidden_states: torch.Tensor,                          # [B * block_len, hidden]
        positions: torch.Tensor,
        context_kvs: list[tuple[torch.Tensor, torch.Tensor]],  # per block
        attn_masks: list[torch.Tensor | None],                 # per block
    ) -> torch.Tensor:
        block_len = hidden_states.shape[0] // len(context_kvs)
        # Pre-norm cross-attention
        residual = hidden_states
        hidden_states = self.input_layernorm.forward(hidden_states)
        if self.attention_conv is not None:
            hidden_states, taps = self.attention_conv.prepare(hidden_states, block_len)
        hidden_states = self.self_attn.forward(hidden_states, positions, context_kvs, attn_masks)
        if self.attention_conv is not None:
            hidden_states = self.attention_conv.finish(hidden_states, taps, block_len)
        hidden_states = residual + hidden_states

        # Pre-norm MLP
        residual = hidden_states
        hidden_states = self.post_attention_layernorm.forward(hidden_states)
        if self.mlp_conv is not None:
            hidden_states, taps = self.mlp_conv.prepare(hidden_states, block_len)
        hidden_states = self.mlp.forward(hidden_states)
        if self.mlp_conv is not None:
            hidden_states = self.mlp_conv.finish(hidden_states, taps, block_len)
        hidden_states = residual + hidden_states

        return hidden_states


def _fi_draft_attention_ok(head_dim: int) -> bool:
    from freetoken.kernel import backend

    return head_dim in (64, 128, 256) and backend.is_flashinfer_installed()


class DFlashDraftModel(BaseOP):
    """DFlash draft model: lightweight block-diffusion model for speculative decoding.

    Predicts an entire block of tokens in parallel using cross-attention to the
    target model's intermediate hidden states. Borrows the target model's
    embedding and LM head.
    """

    def __init__(self, config: DFlashConfig):
        self.config = config
        dtype = torch.bfloat16
        # Project concatenated target hidden states -> hidden_size
        self.fc = LinearReplicated(config.context_dim, config.hidden_size, has_bias=False)
        self.fc.weight = self.fc.weight.to(dtype)
        self.hidden_norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.hidden_norm.weight = self.hidden_norm.weight.to(dtype)
        # Draft layers
        self.layers = OPList(
            [_DFlashDecoderLayer(config, i) for i in range(config.num_hidden_layers)]
        )
        self.norm = RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.norm.weight = self.norm.weight.to(dtype)
        self.candidate_selector = _CandidateSelector(config) if config.is_dflash2 else None

    def quantize_fp8(self, device: torch.device) -> None:
        """Swap every large projection for an ``_Fp8RowLinear`` built on ``device``, one weight at a time."""
        def swap(owner: BaseOP, name: str) -> None:
            linear = getattr(owner, name)
            setattr(owner, name, _Fp8RowLinear(linear.weight.to(device)))

        swap(self, "fc")
        for layer in self.layers.op_list:
            for name in ("q_proj", "k_proj", "v_proj", "o_proj"):
                swap(layer.self_attn, name)
            for name in ("gate_proj", "up_proj", "down_proj"):
                swap(layer.mlp, name)
            for conv in (layer.attention_conv, layer.mlp_conv):
                if conv is not None:
                    swap(conv, "kernel_projection")

    def to(self, device):
        """Move all weights and buffers (including rotary cos_sin_cache) to device."""
        def _move(obj):
            if isinstance(obj, torch.Tensor) and obj.device.type != device.type:
                return obj.to(device)
            if isinstance(obj, list):
                return [_move(x) for x in obj]
            if isinstance(obj, BaseOP):
                for attr_name, attr_val in obj.__dict__.items():
                    new_val = _move(attr_val)
                    if new_val is not attr_val:
                        setattr(obj, attr_name, new_val)
            return obj

        for name, param in self.__dict__.items():
            new_val = _move(param)
            if new_val is not param:
                setattr(self, name, new_val)
        return self

    def project_context_features(self, context_features: torch.Tensor) -> torch.Tensor:
        return self.hidden_norm.forward(self.fc.forward(context_features))

    def forward(
        self,
        mask_embeds: torch.Tensor,    # [B * block_size, hidden] — embedded anchor + mask tokens per block
        positions: torch.Tensor,      # [B * block_size] — positions for RoPE
        context_kv_cache: list[list[tuple[torch.Tensor, torch.Tensor]]],  # per block, per layer: K, V
    ) -> torch.Tensor:
        """Run draft model forward, return hidden states [B * block_size, hidden].

        The caller applies the target model's LM head to get logits.
        """
        block_len = mask_embeds.shape[0] // len(context_kv_cache)
        # The attention mask depends only on (context_len, block_len, layer kind);
        # build each once instead of once per layer and block.
        masks: dict[tuple, torch.Tensor | None] = {}
        h = mask_embeds
        use_fi = _fi_draft_attention_ok(self.layers.op_list[0].self_attn.head_dim)
        for i, layer in enumerate(self.layers.op_list):
            attn = layer.self_attn
            kvs = [cache[i] for cache in context_kv_cache]
            if use_fi:
                h = layer.forward(h, positions, kvs, None)
                continue
            layer_masks = []
            for context_k, _ in kvs:
                key = (context_k.shape[0], attn.layer_type, attn.is_causal, attn.sliding_window)
                if key not in masks:
                    masks[key] = _dflash_context_block_mask(
                        key[0],
                        block_len,
                        mask_embeds.device,
                        layer_type=attn.layer_type,
                        is_causal=attn.is_causal,
                        sliding_window=attn.sliding_window,
                    )
                layer_masks.append(masks[key])
            h = layer.forward(h, positions, kvs, layer_masks)

        return self.norm.forward(h)


__all__ = ["DFlashDraftModel", "_dflash_causal_context_block_mask"]
