from __future__ import annotations

import json
import struct

import pytest

from freetoken.moe.expert_profile import load_expert_order, new_of_old


def _strata(path, pairs, layers, experts):
    with open(path, "wb") as f:
        f.write(b"STRP" + struct.pack("<5I", 1, layers, experts, len(pairs), len(pairs)))
        for layer, e in pairs:
            f.write(struct.pack("<HH", layer, e))


def test_strata_profile_ranks_each_layer_in_its_global_order(tmp_path):
    path = tmp_path / "p.bin"
    _strata(path, [(1, 3), (0, 2), (1, 0), (0, 2), (0, 1)], layers=2, experts=4)
    order = load_expert_order(str(path), 2, 4)
    assert order == [[2, 1, 0, 3], [3, 0, 1, 2]]  # unranked experts follow in natural order
    assert new_of_old(order) == [[2, 1, 0, 3], [1, 2, 3, 0]]


def test_json_profile_and_its_checks(tmp_path):
    path = tmp_path / "p.json"
    path.write_text(json.dumps({"layers": [[1], [0, 1]]}))
    assert load_expert_order(str(path), 2, 2) == [[1, 0], [0, 1]]
    with pytest.raises(ValueError, match="2 layers"):
        load_expert_order(str(path), 3, 2)
    bad = tmp_path / "bad.bin"
    _strata(bad, [(0, 0)], layers=4, experts=8)
    with pytest.raises(ValueError, match="4x8"):
        load_expert_order(str(bad), 2, 8)
