"""DFlash allocates KV pages a verify block ahead of device_len. Pages held from one step must
not be re-allocated (overwritten in the page table, leaked) by the next, and a finish frees
them all: the idle integrity check holds. CPU, real CacheManager, no engine."""
from __future__ import annotations

from types import SimpleNamespace

import pytest
import torch

from freetoken.core import Req, SamplingParams
from freetoken.scheduler.cache import CacheManager

BLOCK = 8


def _req(cm, ids, max_new):
    match = cm.match_req(SimpleNamespace(input_ids=torch.tensor(ids, dtype=torch.int32), input_len=len(ids)))
    req = Req(input_ids=torch.tensor(ids, dtype=torch.int32), table_idx=0, cached_len=0,
              output_len=max_new, uid=0, sampling_params=SamplingParams(), cache_handle=match.cuda_handle)
    cm.lock(req.cache_handle)
    cm.allocate_paged([req])            # prefill
    req.cached_len = req.device_len
    return req


@pytest.mark.parametrize("cache_type", ["naive", "radix"])
@pytest.mark.parametrize("accepted", [[0, 3, 7, 1, 5], [7, 7, 7], [0, 0, 0, 0]])
def test_verify_blocks_neither_leak_nor_reuse_pages(cache_type, accepted):
    page_table = torch.zeros(2, 256, dtype=torch.int32)
    cm = CacheManager(256, 1, page_table, cache_type)
    req = _req(cm, list(range(1, 20)), max_new=100)
    for a in accepted:
        before = page_table[0, : req.paged_len].clone()
        cm.allocate_paged([req], ahead=BLOCK)
        # pages already held keep their slots
        assert torch.equal(page_table[0, : before.numel()], before)
        held = page_table[0, : req.paged_len]
        assert held.unique().numel() == held.numel(), "a slot is mapped twice"
        # the step commits the base token plus `a` accepted drafts
        req.append_host(torch.arange(a + 1, dtype=torch.int32))
        req.cached_len = req.device_len
    with cm.lazy_free_region():
        cm.cache_req(req, finished=True)
    cm.check_integrity()
