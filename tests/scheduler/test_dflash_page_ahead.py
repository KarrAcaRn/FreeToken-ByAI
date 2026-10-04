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


def _hybrid():
    from freetoken.kvcache.linear_state_pool import LinearStatePool
    from freetoken.models.config import LinearGatedDeltaGroupConfig

    g = LinearGatedDeltaGroupConfig(
        name="linear", layer_ids=(0,), num_key_heads=2, num_value_heads=4,
        key_head_dim=16, value_head_dim=16, conv_kernel_dim=4, output_gate="silu",
    )
    pool = LinearStatePool(group=g, num_slots=16, dtype=torch.bfloat16,
                           device=torch.device("cpu"), tp_size=1)
    page_table = torch.zeros(2, 256, dtype=torch.int32)
    return pool, CacheManager(256, 1, page_table, "hybrid_radix", linear_state_pool=pool)


@pytest.mark.parametrize("state_ahead", [False, True])
def test_hybrid_finish_frees_ahead_pages(state_ahead):
    pool, cm = _hybrid()
    req = _req(cm, list(range(1, 20)), max_new=100)
    req.linear_slot_idx, req.mamba_ping_pong = pool.alloc(1)[0], tuple(pool.alloc(2))
    for a in [3, 7, 0]:
        cm.allocate_paged([req], ahead=BLOCK)
        req.append_host(torch.arange(a + 1, dtype=torch.int32))
        req.cached_len = req.device_len
    req.linear_state_ahead = state_ahead
    with cm.lazy_free_region():
        cm.cache_req(req, finished=True)
    cm.check_integrity()
    tree_slots = cm.prefix_cache.mamba_evictable_size + cm.prefix_cache.mamba_protected
    # a state that ran past cached_len is never attached to the cached prefix
    assert tree_slots == (0 if state_ahead else 1)
    assert pool.num_free_slots + tree_slots == pool.num_slots - 1


@pytest.mark.parametrize("eos_at,ahead", [(None, False), (3, False), (1, True), (0, True)])
def test_multi_token_drain_marks_a_state_past_the_stop(eos_at, ahead):
    from freetoken.scheduler.scheduler import Scheduler

    eos = 99
    tokens = torch.tensor([5, 6, 7, 8], dtype=torch.int32)  # 3 accepted drafts + the bonus
    if eos_at is not None:
        tokens[eos_at] = eos
    req = Req(input_ids=torch.arange(1, 11, dtype=torch.int32), table_idx=0, cached_len=9,
              output_len=50, uid=0, sampling_params=SamplingParams(), cache_handle=None)
    req.cached_len, req.device_len = 10, 11  # complete_one ran: the anchor's KV is in
    freed = []
    sched = SimpleNamespace(
        eos_token_ids={eos}, finished_reqs=set(), _match_stop_str=lambda r: None,
        decode_manager=SimpleNamespace(remove_req=lambda r: None),
        _free_req_resources=lambda r: freed.append((r.cached_len, r.linear_state_ahead)),
    )
    finished = set()
    outputs = SimpleNamespace(next_tokens_cpu=tokens, num_tokens=4)
    Scheduler._drain_multi_token(sched, req, outputs, 0, 4, [], finished, None)
    kept = 4 if eos_at is None else eos_at + 1
    # every kept token but the last has its KV written
    assert req.cached_len == 9 + kept
    assert req.input_ids.numel() == 10 + kept
    if eos_at is None:
        assert not finished and not freed
    else:
        assert freed == [(9 + kept, ahead)]


def test_multi_token_drain_reads_each_requests_own_count():
    from freetoken.scheduler.scheduler import Scheduler

    # two requests, rows 4 apart: the first kept 2 tokens, the second 4
    flat = torch.tensor([5, 6, -1, -1, 7, 8, 9, 10], dtype=torch.int32)
    outputs = SimpleNamespace(next_tokens_cpu=flat, num_tokens=4, token_counts=(2, 4))
    sched = SimpleNamespace(eos_token_ids=set(), finished_reqs=set(), _match_stop_str=lambda r: None,
                            decode_manager=None, _free_req_resources=None)
    reqs = []
    for uid in range(2):
        req = Req(input_ids=torch.arange(1, 11, dtype=torch.int32), table_idx=uid, cached_len=9,
                  output_len=50, uid=uid, sampling_params=SamplingParams(), cache_handle=None)
        req.cached_len, req.device_len = 10, 11
        reqs.append(req)
    reply = []
    for i, req in enumerate(reqs):
        Scheduler._drain_multi_token(sched, req, outputs, i, 4, reply, set(), None)
    assert [m.next_token for m in reply] == [5, 6, 7, 8, 9, 10]
    assert [r.cached_len for r in reqs] == [11, 13]
