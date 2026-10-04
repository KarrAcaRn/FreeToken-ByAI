"""The draft's context: each draft layer's K/V of the target hidden states it attends to.

Preallocated when the draft loads (before the KV pool is sized), so the draft never grows
VRAM behind the budget's back. A sliding-window layer only ever reads its last ``window``
positions, so it keeps a ``2 * window`` buffer and compacts the tail to the front when it
fills; a full-attention layer keeps every position up to ``max_len``. Positions are absolute
(RoPE is applied when an entry is stored) and contiguous: an append that does not continue
the stored run restarts the context at its own start.
"""

from __future__ import annotations

import torch


class DraftContextCache:
    def __init__(
        self,
        windows: list[int | None],
        max_len: int,
        num_kv_heads: int,
        head_dim: int,
        dtype: torch.dtype,
        device: torch.device,
    ):
        self.windows = [w if w is not None and w < max_len else None for w in windows]
        self.max_len = max_len
        caps = [min(2 * w, max_len) if w is not None else max_len for w in self.windows]
        shape = (num_kv_heads, head_dim)
        self.k = [torch.empty((cap, *shape), dtype=dtype, device=device) for cap in caps]
        self.v = [torch.empty((cap, *shape), dtype=dtype, device=device) for cap in caps]
        self.lens = [0] * len(windows)
        self.end_pos = 0  # absolute position after the last stored entry

    @staticmethod
    def nbytes_for(
        windows: list[int | None], max_len: int, num_kv_heads: int, head_dim: int, elem_size: int
    ) -> int:
        caps = [min(2 * w, max_len) if w is not None and w < max_len else max_len for w in windows]
        return sum(caps) * 2 * num_kv_heads * head_dim * elem_size

    @property
    def nbytes(self) -> int:
        return sum(t.numel() * t.element_size() for t in self.k + self.v)

    @property
    def rows_needed(self) -> int | None:
        """How many trailing rows of an append any layer keeps (None: all of them)."""
        if any(w is None for w in self.windows):
            return None
        return max(self.windows, default=0)

    def clear(self) -> None:
        self.lens = [0] * len(self.lens)
        self.end_pos = 0

    def truncate(self, pos: int) -> None:
        """Drop the entries at absolute positions >= ``pos``."""
        if pos >= self.end_pos:
            return
        drop = self.end_pos - pos
        self.lens = [max(0, n - drop) for n in self.lens]
        self.end_pos = pos

    def append(self, layer_kv: list[tuple[torch.Tensor, torch.Tensor]], start_pos: int, n: int) -> None:
        """Store ``n`` positions from ``start_pos`` on. ``layer_kv[i]`` holds the trailing
        rows layer ``i`` keeps (all ``n``, or at least its window when ``n`` is larger)."""
        if start_pos != self.end_pos:
            if start_pos < self.end_pos:
                self.truncate(start_pos)
            else:
                self.clear()
        end_pos = start_pos + n
        if end_pos > self.max_len:
            raise ValueError(f"draft context position {end_pos} exceeds max_len {self.max_len}")
        for i, (new_k, new_v) in enumerate(layer_kv):
            k, v, window, length = self.k[i], self.v[i], self.windows[i], self.lens[i]
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
            self.lens[i] = length + rows
        self.end_pos = end_pos

    def layer_kv(self, i: int) -> tuple[torch.Tensor, torch.Tensor]:
        """The entries layer ``i`` attends to: the last ``window`` (or all) positions."""
        length = self.lens[i]
        start = length - min(length, self.windows[i]) if self.windows[i] is not None else 0
        return self.k[i][start:length], self.v[i][start:length]

    def all_layer_kv(self) -> list[tuple[torch.Tensor, torch.Tensor]]:
        return [self.layer_kv(i) for i in range(len(self.lens))]


__all__ = ["DraftContextCache"]
