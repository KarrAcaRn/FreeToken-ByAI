"""The draft's context: each draft layer's K/V of the target hidden states it attends to, one
slot per request.

Preallocated when the draft loads (before the KV pool is sized), so the draft never grows
VRAM behind the budget's back. A sliding-window layer only ever reads its last ``window``
positions, so it keeps ``window + COMPACT_SLACK`` rows per slot and compacts the tail to the
front when they fill. A full-attention layer keeps its last ``FULL_ATTENTION_CAP`` positions:
preallocating a model's whole position range (262k on Qwen3.6) per request would take the
VRAM an offloaded MoE needs for its experts, and the target verifies every drafted token, so
the cap can only move the acceptance rate of very long conversations. Positions are absolute
(RoPE is applied when an entry is stored) and contiguous: an append that does not continue
the slot's stored run restarts its context at the append's start.
"""

from __future__ import annotations

import torch


COMPACT_SLACK = 1024
FULL_ATTENTION_CAP = 16384


def _windows(windows: list[int | None], max_len: int) -> list[int | None]:
    """The rows each layer reads: its window, a full layer's cap, or None (all of max_len)."""
    out = []
    for w in windows:
        w = FULL_ATTENTION_CAP if w is None else min(w, FULL_ATTENTION_CAP)
        out.append(w if w < max_len else None)
    return out


def _caps(windows: list[int | None], max_len: int) -> list[int]:
    return [min(w + COMPACT_SLACK, max_len) if w is not None else max_len for w in _windows(windows, max_len)]


class DraftContextCache:
    def __init__(
        self,
        windows: list[int | None],
        max_len: int,
        num_kv_heads: int,
        head_dim: int,
        dtype: torch.dtype,
        device: torch.device,
        num_slots: int = 1,
    ):
        self.windows = _windows(windows, max_len)
        self.max_len = max_len
        self.num_slots = num_slots
        shape = (num_kv_heads, head_dim)
        caps = _caps(windows, max_len)
        self.k = [torch.empty((num_slots, cap, *shape), dtype=dtype, device=device) for cap in caps]
        self.v = [torch.empty((num_slots, cap, *shape), dtype=dtype, device=device) for cap in caps]
        self.lens = [[0] * len(windows) for _ in range(num_slots)]
        self.end_pos = [0] * num_slots  # per slot: absolute position after its last entry

    @staticmethod
    def nbytes_for(
        windows: list[int | None], max_len: int, num_kv_heads: int, head_dim: int, elem_size: int,
        num_slots: int = 1,
    ) -> int:
        return num_slots * sum(_caps(windows, max_len)) * 2 * num_kv_heads * head_dim * elem_size

    @property
    def nbytes(self) -> int:
        return sum(t.numel() * t.element_size() for t in self.k + self.v)

    @property
    def rows_needed(self) -> int | None:
        """How many trailing rows of an append any layer keeps (None: all of them)."""
        if any(w is None for w in self.windows):
            return None
        return max(self.windows, default=0)

    def clear(self, slot: int = 0) -> None:
        self.lens[slot] = [0] * len(self.windows)
        self.end_pos[slot] = 0

    def truncate(self, slot: int, pos: int) -> None:
        """Drop the slot's entries at absolute positions >= ``pos``."""
        if pos >= self.end_pos[slot]:
            return
        drop = self.end_pos[slot] - pos
        self.lens[slot] = [max(0, n - drop) for n in self.lens[slot]]
        self.end_pos[slot] = pos

    def append(
        self, slot: int, layer_kv: list[tuple[torch.Tensor, torch.Tensor]], start_pos: int, n: int
    ) -> None:
        """Store ``n`` positions from ``start_pos`` on. ``layer_kv[i]`` holds the trailing
        rows layer ``i`` keeps (all ``n``, or at least its window when ``n`` is larger)."""
        if start_pos != self.end_pos[slot]:
            if start_pos < self.end_pos[slot]:
                self.truncate(slot, start_pos)
            else:
                self.clear(slot)
        end_pos = start_pos + n
        if end_pos > self.max_len:
            raise ValueError(f"draft context position {end_pos} exceeds max_len {self.max_len}")
        lens = self.lens[slot]
        for i, (new_k, new_v) in enumerate(layer_kv):
            k, v, window, length = self.k[i][slot], self.v[i][slot], self.windows[i], lens[i]
            rows = min(n, new_k.shape[0])
            if window is not None and rows > window:
                rows = window
            new_k, new_v = new_k[new_k.shape[0] - rows :], new_v[new_v.shape[0] - rows :]
            if rows < n:  # only the tail of this append survives: the older run is out of window
                length = 0
            if length + rows > k.shape[0]:
                assert window is not None, "a full-attention layer never compacts"
                keep = max(0, min(length, window - rows))
                k[:keep].copy_(k[length - keep : length].clone())
                v[:keep].copy_(v[length - keep : length].clone())
                length = keep
            k[length : length + rows].copy_(new_k)
            v[length : length + rows].copy_(new_v)
            lens[i] = length + rows
        self.end_pos[slot] = end_pos

    def layer_kv(self, slot: int, i: int) -> tuple[torch.Tensor, torch.Tensor]:
        """The entries layer ``i`` of ``slot`` attends to: the last ``window`` (or all) positions."""
        length = self.lens[slot][i]
        start = length - min(length, self.windows[i]) if self.windows[i] is not None else 0
        return self.k[i][slot, start:length], self.v[i][slot, start:length]

    def all_layer_kv(self, slot: int = 0) -> list[tuple[torch.Tensor, torch.Tensor]]:
        return [self.layer_kv(slot, i) for i in range(len(self.windows))]


__all__ = ["DraftContextCache"]
