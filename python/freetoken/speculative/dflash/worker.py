from __future__ import annotations

from typing import TYPE_CHECKING

import torch
from freetoken.engine.graph import project_lm_head_all_positions

from freetoken.speculative.dflash.config import DFlashConfig
from freetoken.speculative.dflash.context import DraftContextCache
from freetoken.speculative.dflash.model import DFlashDraftModel
from freetoken.speculative.dflash.weight import iter_dflash_weights

if TYPE_CHECKING:
    from freetoken.engine.engine import Engine


class DFlashWorker:
    """Orchestrates DFlash draft generation and target-head projection."""

    def __init__(
        self,
        draft_model_path: str,
        target_model,
        engine: Engine,
        device: torch.device,
        block_size: int | None = None,
        draft_quant: str = "none",
        linear_state_bytes_per_token: int = 0,
        max_context_len: int = 32768,
    ):
        from freetoken.utils import cached_load_hf_config

        # Load draft config
        hf_config = cached_load_hf_config(draft_model_path)
        self.config = DFlashConfig.from_hf_config(hf_config)
        if block_size is not None:
            self.config.block_size = block_size

        self.block_size = self.config.block_size
        self.mask_token_id = self.config.mask_token_id
        self.target_layer_ids = set(self.config.target_layer_ids)
        self.device = device
        self.engine = engine

        # Create and load draft model
        self.draft_model = DFlashDraftModel(self.config)
        # fp8: read to host and quantize one weight at a time, so the bf16 copy never sits in VRAM
        load_device = torch.device("cpu") if draft_quant == "fp8" else device
        state_dict = {}
        for name, t in iter_dflash_weights(draft_model_path, load_device):
            state_dict[name] = t
        self.draft_model.load_state_dict(state_dict)
        if draft_quant == "fp8":
            self.draft_model.quantize_fp8(device)
        self.draft_model.to(device)

        # Borrow target model's embedding and LM head
        self.target_embed = target_model.model.embed_tokens
        self.target_lm_head = target_model.lm_head

        # The draft's context K/V, preallocated before the KV pool is sized (see context.py)
        self.context = DraftContextCache(
            self.config.layer_windows,
            max_context_len,
            self.config.num_key_value_heads,
            self.config.head_dim,
            torch.bfloat16,
            device,
        )
        self._uid: int | None = None
        self._last_tokens: torch.Tensor | None = None  # the finished request's ids, for carry-over
        self._mask_embeds: torch.Tensor | None = None
        self._draft_input_storage: torch.Tensor | None = None
        self.last_draft_probs: torch.Tensor | None = None
        self._position_offsets = torch.arange(self.block_size, dtype=torch.int32, device=device)
        # Hybrid GDN targets: the verify graphs keep one boundary state per verified token. Hold
        # that memory now, before the KV pool is sized; the graph capture takes it over.
        self._verify_reserve: torch.Tensor | None = None
        if linear_state_bytes_per_token and self.block_size > 1:
            self._verify_reserve = torch.empty(
                self.block_size * linear_state_bytes_per_token, dtype=torch.uint8, device=device)
        # ... plus the pre-verify copy of the request's slot, kept for the whole run
        self._pre_verify_flat: torch.Tensor | None = None
        self._pre_verify_views: tuple[torch.Tensor, torch.Tensor] | None = None
        if linear_state_bytes_per_token:
            self._pre_verify_flat = torch.empty(
                linear_state_bytes_per_token + 256, dtype=torch.uint8, device=device)

    def release_verify_reserve(self) -> None:
        self._verify_reserve = None

    def pre_verify_snapshot(self, pool) -> tuple[torch.Tensor, torch.Tensor] | None:
        """(conv, recurrent) views of the persistent pre-verify buffer, shaped like one ``pool`` slot."""
        if self._pre_verify_flat is None:
            return None
        if self._pre_verify_views is None:
            conv, rec = pool.conv_states[:, 0], pool.recurrent_states[:, 0]
            conv_bytes = conv.numel() * conv.element_size()
            rec_start = -(-conv_bytes // 256) * 256  # keep the recurrent view aligned
            rec_bytes = rec.numel() * rec.element_size()
            assert rec_start + rec_bytes <= self._pre_verify_flat.numel()
            self._pre_verify_views = (
                self._pre_verify_flat[:conv_bytes].view(conv.dtype).view(conv.shape),
                self._pre_verify_flat[rec_start : rec_start + rec_bytes].view(rec.dtype).view(rec.shape),
            )
        return self._pre_verify_views

    def begin_request(self, uid: int, token_ids: torch.Tensor, cached_len: int) -> None:
        """Called on each prefill chunk: a new request keeps the previous request's context
        through its cached prefix when that request's tokens match it (a multi-turn chat
        continues the last conversation), and starts empty otherwise."""
        if uid == self._uid:
            return
        self._uid = uid
        prev = self._last_tokens
        self._last_tokens = None
        if (
            cached_len > 0
            and prev is not None
            and self.context.end_pos >= cached_len
            and prev.numel() >= cached_len
            and torch.equal(prev[:cached_len], token_ids[:cached_len].to(prev.dtype))
        ):
            self.context.truncate(cached_len)
        else:
            self.context.clear()

    def finish_request(self, token_ids: torch.Tensor) -> None:
        """Remember the finished request's tokens behind the stored context (host ids)."""
        self._uid = None
        self._last_tokens = token_ids[: self.context.end_pos].clone()
        self.last_draft_probs = None

    def store_hidden_states(self, hidden_states: list[torch.Tensor], start_position: int) -> None:
        """Project target-layer hidden states ([tokens, hidden] each, positions from
        ``start_position``) into every draft layer's context K/V."""
        rows = hidden_states[0].shape[0]
        if rows == 0:
            return
        keep = self.context.rows_needed
        skip = rows - keep if keep is not None and rows > keep else 0
        features = torch.cat([h[skip:] for h in hidden_states], dim=-1)
        context = self.draft_model.project_context_features(features)
        positions = torch.arange(
            start_position + skip, start_position + rows, dtype=torch.int32, device=context.device
        )
        layer_kv = [
            layer.self_attn.project_context_kv(context, positions)
            for layer in self.draft_model.layers.op_list
        ]
        self.context.append(layer_kv, start_position, rows)

    def target_logits(self, hidden_states: torch.Tensor) -> torch.Tensor:
        """Project target hidden states without LMHead's prefill last-token slicing."""
        return project_lm_head_all_positions(self.target_lm_head, hidden_states)

    def draft_logits(self, hidden_states: torch.Tensor) -> torch.Tensor:
        logits = self.target_logits(hidden_states)
        config = getattr(self, "config", None)
        logits = logits * float(getattr(config, "output_multiplier", 1.0))
        softcap = getattr(config, "final_logit_softcapping", None)
        if softcap is not None and float(softcap) > 0:
            logits = torch.tanh(logits / float(softcap)) * float(softcap)
        return logits

    @property
    def context_length(self) -> int:
        return self.context.end_pos

    def _draft_input_embeds(self, base_token_id: torch.Tensor) -> torch.Tensor:
        if self.block_size == 1:
            return self.target_embed.forward(base_token_id[:1])

        config = getattr(self, "config", None)
        scale = float(getattr(config, "input_embedding_scale", 1.0))
        base_embed = self.target_embed.forward(base_token_id[:1]) * scale
        mask_embeds = getattr(self, "_mask_embeds", None)
        if mask_embeds is None:
            mask_ids = torch.full(
                (self.block_size - 1,),
                self.mask_token_id,
                dtype=torch.int32,
                device=self.device,
            )
            mask_embeds = (self.target_embed.forward(mask_ids) * scale).detach()
            self._mask_embeds = mask_embeds
        storage = getattr(self, "_draft_input_storage", None)
        if (
            storage is None
            or storage.shape != (self.block_size, base_embed.shape[1])
            or storage.dtype != base_embed.dtype
            or storage.device != base_embed.device
        ):
            storage = torch.empty(
                (self.block_size, base_embed.shape[1]),
                dtype=base_embed.dtype,
                device=base_embed.device,
            )
            storage[1:].copy_(mask_embeds)
            self._draft_input_storage = storage
        storage[:1].copy_(base_embed)
        return storage

    def _draft_positions(self, position: int) -> torch.Tensor:
        offsets = getattr(self, "_position_offsets", None)
        if offsets is None or offsets.numel() != self.block_size or offsets.device != self.device:
            offsets = torch.arange(self.block_size, dtype=torch.int32, device=self.device)
            self._position_offsets = offsets
        return offsets + position

    def draft(
        self,
        base_token_id: torch.Tensor,       # [1] — the anchor: the last emitted token
        position: int,                      # position of the anchor
        sampling_args=None,                 # BatchSamplingArgs; None / greedy -> argmax drafts
    ) -> torch.Tensor:
        """Generate block_size draft tokens in parallel over the stored context.

        Returns: draft_tokens [block_size]
        """
        bs = self.block_size
        mask_embeds = self._draft_input_embeds(base_token_id)
        positions = self._draft_positions(position)
        draft_hidden = self.draft_model.forward(mask_embeds, positions, self.context.all_layer_kv())

        # Only positions 1..bs-1 are candidate draft tokens. Position 0 is the
        # sampled target base token and is not consumed by the engine.
        if bs == 1:
            return base_token_id[:1]
        logits = self.draft_logits(draft_hidden[1:])  # [bs - 1, vocab]
        selector = self.draft_model.candidate_selector
        if selector is not None:
            temperature = None
            if sampling_args is not None and sampling_args.temperatures is not None:
                temperature = sampling_args.temperatures[:1]
            candidate_tokens, self.last_draft_probs = selector.select(
                draft_hidden[1:], logits, base_token_id, temperature)
            return torch.cat([base_token_id[:1].to(candidate_tokens.dtype), candidate_tokens])
        if sampling_args is not None and sampling_args.temperatures is not None:
            # Non-greedy: sample candidates (upstream DFlash samples drafts too) and
            # stash the filtered draft distribution for rejection-sampling verify.
            from freetoken.speculative.utils import sampling_probs

            draft_probs = sampling_probs(logits, sampling_args)
            candidate_tokens = torch.multinomial(draft_probs, 1)[:, 0]
            self.last_draft_probs = draft_probs
        else:
            candidate_tokens = torch.argmax(logits, dim=-1)
            self.last_draft_probs = None
        return torch.cat([base_token_id[:1].to(candidate_tokens.dtype), candidate_tokens])


__all__ = ["DFlashWorker"]
