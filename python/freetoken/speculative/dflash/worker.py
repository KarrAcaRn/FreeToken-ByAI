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
        verify_row_bytes: int = 0,
        verify_batch: int = 1,
        target_hidden_size: int = 0,
        max_context_len: int = 32768,
        num_context_slots: int = 1,
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
            num_slots=num_context_slots,
        )
        # one context slot per running request; a finished request's slot stays parked (with
        # the token ids behind it) until a new request continues it or needs the room
        self._slot_of: dict[int, int] = {}
        self._parked: list[tuple[int, torch.Tensor]] = []  # oldest first
        self._free_slots = list(range(num_context_slots))
        self._mask_embeds: torch.Tensor | None = None
        self._draft_input_storage: torch.Tensor | None = None
        self._position_offsets = torch.arange(self.block_size, dtype=torch.int32, device=device)
        # The verify graphs keep, per verified token, its logits, the hidden states the draft
        # reads and (GDN targets) the conv state and recurrence inputs the commit replays. Hold
        # that memory now, before the KV pool is sized; the graph capture takes it over.
        self._verify_reserve: torch.Tensor | None = None
        if verify_row_bytes and self.block_size > 1:
            row = verify_row_bytes + len(self.target_layer_ids) * target_hidden_size * 2
            # the largest verify graph: verify_batch requests at the full block
            self._verify_reserve = torch.empty(
                verify_batch * self.block_size * row, dtype=torch.uint8, device=device)

    def release_verify_reserve(self) -> None:
        self._verify_reserve = None

    def begin_request(self, uid: int, token_ids: torch.Tensor, cached_len: int) -> None:
        """Called on each prefill chunk. A new request continues a parked context whose tokens
        match its cached prefix (the next turn of a chat continues the last one), else takes a
        free slot, else the oldest parked one, and starts empty."""
        if uid in self._slot_of:
            return
        slot = None
        if cached_len > 0:
            for i in range(len(self._parked) - 1, -1, -1):
                s, prev = self._parked[i]
                if (
                    self.context.end_pos[s] >= cached_len
                    and prev.numel() >= cached_len
                    and torch.equal(prev[:cached_len], token_ids[:cached_len].to(prev.dtype))
                ):
                    slot = s
                    del self._parked[i]
                    self.context.truncate(slot, cached_len)
                    break
        if slot is None:
            if self._free_slots:
                slot = self._free_slots.pop()
            else:
                slot = self._parked.pop(0)[0]
            self.context.clear(slot)
        self._slot_of[uid] = slot

    def slot_of(self, uid: int) -> int | None:
        return self._slot_of.get(uid)

    def finish_request(self, uid: int, token_ids: torch.Tensor) -> None:
        """Park the finished request's context with its tokens (host ids) for a continuation."""
        slot = self._slot_of.pop(uid, None)
        if slot is None:
            return
        self._parked.append((slot, token_ids[: self.context.end_pos[slot]].clone()))

    def store_hidden_states(self, slot: int, hidden_states: list[torch.Tensor], start_position: int) -> None:
        """Project target-layer hidden states ([tokens, hidden] each, positions from
        ``start_position``) into every draft layer's context K/V of ``slot``."""
        self.store_hidden_states_batch([(slot, 0, hidden_states[0].shape[0], start_position)], hidden_states)

    def store_hidden_states_batch(
        self, spans: list[tuple[int, int, int, int]], hidden_states: list[torch.Tensor]
    ) -> None:
        """Store several requests' rows with one projection: ``spans`` are (slot, first row,
        rows, start position) into ``hidden_states`` ([tokens, hidden] per target layer)."""
        keep = self.context.rows_needed
        picks, kept = [], []
        for slot, first, rows, start in spans:
            if rows <= 0 or slot is None:
                continue
            skip = rows - keep if keep is not None and rows > keep else 0
            picks.append((first + skip, rows - skip, start + skip))
            kept.append((slot, rows, start, rows - skip))
        if not picks:
            return
        if len(picks) == 1:
            first, n, _ = picks[0]
            features = torch.cat([h[first : first + n] for h in hidden_states], dim=-1)
        else:
            index = torch.cat([torch.arange(f, f + n) for f, n, _ in picks]).to(hidden_states[0].device)
            features = torch.cat([h.index_select(0, index) for h in hidden_states], dim=-1)
        context = self.draft_model.project_context_features(features)
        positions = torch.cat([
            torch.arange(p, p + n, dtype=torch.int32) for _, n, p in picks
        ]).to(context.device, non_blocking=True)
        layer_kv = [
            layer.self_attn.project_context_kv(context, positions)
            for layer in self.draft_model.layers.op_list
        ]
        row = 0
        for slot, rows, start, n in kept:
            self.context.append(slot, [(k[row : row + n], v[row : row + n]) for k, v in layer_kv], start, rows)
            row += n

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

    def _draft_input_embeds(self, base_tokens: torch.Tensor) -> torch.Tensor:
        """[B * block_size, hidden]: each block is its anchor's embedding, then mask tokens."""
        scale = float(getattr(self.config, "input_embedding_scale", 1.0))
        if self._mask_embeds is None:
            mask_ids = torch.full(
                (self.block_size - 1,), self.mask_token_id, dtype=torch.int32, device=self.device
            )
            self._mask_embeds = (self.target_embed.forward(mask_ids) * scale).detach()
        n = base_tokens.numel()
        storage = self._draft_input_storage
        if storage is None or storage.shape[0] < n * self.block_size:
            hidden = self._mask_embeds.shape[1]
            storage = torch.empty(
                (n * self.block_size, hidden), dtype=self._mask_embeds.dtype, device=self.device
            )
            storage.view(n, self.block_size, hidden)[:, 1:].copy_(self._mask_embeds)
            self._draft_input_storage = storage
        embeds = storage[: n * self.block_size]
        embeds.view(n, self.block_size, -1)[:, 0].copy_(self.target_embed.forward(base_tokens) * scale)
        return embeds

    def draft(
        self,
        slots: list[int],                   # each request's context slot
        base_tokens: torch.Tensor,          # [B] int32 — each request's anchor: its last emitted token
        positions: list[int],               # each anchor's position
        sampling_args=None,                 # BatchSamplingArgs; None / greedy -> argmax drafts
    ) -> tuple[torch.Tensor, list[torch.Tensor | None]]:
        """Draft a block per request, all blocks in one forward over their own contexts.

        Returns (tokens [B, block_size] with the anchors first, each request's draft
        distribution [block_size - 1, vocab] for rejection-sampling verify, or None when
        it drafted greedily)."""
        from freetoken.speculative.utils import request_sampling_args, sampling_probs

        n, bs = len(slots), self.block_size
        embeds = self._draft_input_embeds(base_tokens)
        pos = (self._position_offsets[None, :] + torch.tensor(
            positions, dtype=torch.int32, device=self.device)[:, None]).reshape(-1)
        hidden = self.draft_model.forward(embeds, pos, [self.context.all_layer_kv(s) for s in slots])
        # position 0 of each block is the anchor; 1..bs-1 are the candidates
        hidden = hidden.view(n, bs, -1)[:, 1:]
        logits = self.draft_logits(hidden.reshape(n * (bs - 1), -1)).view(n, bs - 1, -1)
        rows = [request_sampling_args(sampling_args, b) for b in range(n)]
        sampled = [r is not None and r.temperatures is not None for r in rows]
        selector = self.draft_model.candidate_selector
        if selector is not None and (all(sampled) or not any(sampled)):
            temperature = (
                torch.cat([r.temperatures for r in rows]) if all(sampled) else None
            )
            candidates, probs = selector.select(hidden, logits, base_tokens, temperature)
            draft_probs = list(probs) if probs is not None else [None] * n
        else:
            picks, draft_probs = [], []
            for b in range(n):
                if selector is not None:
                    path, q = selector.select(
                        hidden[b], logits[b], base_tokens[b : b + 1],
                        rows[b].temperatures if sampled[b] else None,
                    )
                elif sampled[b]:
                    # sample candidates (upstream DFlash samples drafts too) and keep the
                    # filtered draft distribution for rejection-sampling verify
                    q = sampling_probs(logits[b], rows[b])
                    path = torch.multinomial(q, 1)[:, 0]
                else:
                    path, q = torch.argmax(logits[b], dim=-1), None
                picks.append(path)
                draft_probs.append(q)
            candidates = torch.stack(picks)
        tokens = torch.cat([base_tokens.view(n, 1).to(candidates.dtype), candidates], dim=1)
        return tokens, draft_probs


__all__ = ["DFlashWorker"]
