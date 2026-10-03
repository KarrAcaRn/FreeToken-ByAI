"""Inserted radix keys own their storage: a request's ids are a view into its whole input-plus-output
token buffer, and a cached prefix that kept the view would keep that buffer alive after the request."""
from __future__ import annotations

import pytest
import torch

from .adapters import iter_nodes, slots_tensor
from .driver import CacheSpec, Session

TOKENS = 16
BUFFER = 32_768  # the output budget a request's id buffer is sized for


def _insert(session: Session, ids: torch.Tensor) -> None:
    cache, slots = session.ad.cache, slots_tensor(range(1, TOKENS + 1))
    if session.spec.kind == "plain":
        cache.insert_prefix(ids, slots)
    elif session.spec.kind == "swa":
        cache.insert(ids, slots, swa_evicted_seqlen=0, update_kv_after_len=0)
    else:
        cache.insert(ids, slots, 1)


@pytest.mark.parametrize("spec", [CacheSpec("plain", 1), CacheSpec("swa", 1, window=4), CacheSpec("hybrid", 1)],
                         ids=lambda s: s.kind)
def test_inserted_keys_do_not_retain_the_request_buffer(spec):
    session = Session(spec)
    buffer = torch.zeros(BUFFER, dtype=torch.int32)
    buffer[:TOKENS] = torch.arange(1, TOKENS + 1, dtype=torch.int32)
    _insert(session, buffer[:TOKENS])
    keys = [node._key for node, _ in iter_nodes(session.ad.root)]
    assert keys and all(key.untyped_storage().nbytes() <= TOKENS * key.element_size() for key in keys)
