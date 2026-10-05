"""Expert usage profiles for the disk tier: which experts of each layer are hot.

With ``--expert-profile`` the disk tier renumbers every MoE layer's experts by rank (the
hottest becomes id 0) right after the router's top-k. Everything past that point -- the
pinned RAM prefix ``[0, --expert-ram-experts)``, the identity prefill slots, the slot cache --
then works on the renumbered ids, so RAM holds the experts a conversation needs most instead
of whichever ids happen to be lowest, and fewer misses go to disk.

Accepted formats:
* Strata's ``STRP`` v1 profile (``data/expert-profile.bin`` of github.com/Niko1221/Strata,
  MIT): a global ranking of (layer, expert) pairs; each layer keeps the order its pairs have.
* JSON ``{"layers": [[expert ids, hottest first], ...]}`` (one list per MoE layer).
Experts a profile does not rank keep their natural order after the ranked ones.
"""

from __future__ import annotations

import json
import struct


def _strata_pairs(blob: bytes, num_layers: int, num_experts: int) -> list[tuple[int, int]]:
    _version, nl, ne, _slots, n = struct.unpack_from("<5I", blob, 4)
    if (nl, ne) != (num_layers, num_experts):
        raise ValueError(f"expert profile is {nl}x{ne}, the model has {num_layers}x{num_experts} experts")
    return [struct.unpack_from("<HH", blob, 24 + 4 * i) for i in range(n)]


def load_expert_order(path: str, num_layers: int, num_experts: int) -> list[list[int]]:
    """Per MoE layer, the original expert ids in renumbered order (hottest first)."""
    with open(path, "rb") as f:
        blob = f.read()
    if blob[:4] == b"STRP":
        ranked: list[list[int]] = [[] for _ in range(num_layers)]
        for layer, expert in _strata_pairs(blob, num_layers, num_experts):
            ranked[layer].append(expert)
    else:
        ranked = [list(map(int, layer)) for layer in json.loads(blob)["layers"]]
        if len(ranked) != num_layers:
            raise ValueError(f"expert profile ranks {len(ranked)} layers, the model has {num_layers}")
    order = []
    for layer, ids in enumerate(ranked):
        seen = set()
        row = []
        for e in ids:
            if not 0 <= e < num_experts:
                raise ValueError(f"expert profile layer {layer}: expert {e} out of range")
            if e not in seen:
                seen.add(e)
                row.append(e)
        row += [e for e in range(num_experts) if e not in seen]
        order.append(row)
    return order


def new_of_old(order: list[list[int]]) -> list[list[int]]:
    """Inverse of ``load_expert_order``: per layer, original id -> renumbered id."""
    inv = []
    for row in order:
        layer = [0] * len(row)
        for new, old in enumerate(row):
            layer[old] = new
        inv.append(layer)
    return inv


__all__ = ["load_expert_order", "new_of_old"]
