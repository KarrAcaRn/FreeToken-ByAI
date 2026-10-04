"""DFlash draft context: the windowed K/V cache and the multi-turn carry-over."""

from __future__ import annotations

import torch

from freetoken.speculative.dflash.context import DraftContextCache
from freetoken.speculative.dflash.worker import DFlashWorker


def _cache(windows, max_len=64, slots=1):
    return DraftContextCache(windows, max_len, 1, 1, torch.float32, torch.device("cpu"), num_slots=slots)


def _kv(start, n, layers):
    # each entry stores its own absolute position, so a view shows which positions it holds
    rows = torch.arange(start, start + n, dtype=torch.float32).view(n, 1, 1)
    return [(rows, -rows) for _ in range(layers)]


def _positions(cache, i, slot=0):
    k, v = cache.layer_kv(slot, i)
    assert torch.equal(v, -k)
    return k.flatten().int().tolist()


def test_sliding_layer_keeps_its_window_across_compactions():
    cache = _cache([4, None])
    for start in range(0, 20, 3):
        cache.append(0, _kv(start, 3, 2), start, 3)
    assert cache.end_pos[0] == 21
    assert _positions(cache, 0) == [17, 18, 19, 20]
    assert _positions(cache, 1) == list(range(21))
    assert cache.k[0].shape[1] == 8  # 2 x window, preallocated


def test_long_append_keeps_only_the_window_tail():
    cache = _cache([4])
    cache.append(0, _kv(0, 2, 1), 0, 2)
    # the caller may pass just the rows a layer keeps (rows_needed) for a long prefill chunk
    cache.append(0, _kv(8, 4, 1), 2, 10)
    assert cache.end_pos[0] == 12
    assert _positions(cache, 0) == [8, 9, 10, 11]


def test_rows_needed():
    assert _cache([4, 6]).rows_needed == 6
    assert _cache([4, None]).rows_needed is None
    assert _cache([128]).rows_needed is None  # a window past max_len is full attention


def test_truncate_and_non_contiguous_append():
    cache = _cache([None])
    cache.append(0, _kv(0, 10, 1), 0, 10)
    cache.append(0, _kv(6, 2, 1), 6, 2)  # rewinds to 6, then appends
    assert _positions(cache, 0) == list(range(8))
    cache.append(0, _kv(20, 2, 1), 20, 2)  # a gap restarts the context
    assert _positions(cache, 0) == [20, 21]
    assert cache.end_pos[0] == 22


def test_nbytes_matches_allocation():
    cache = DraftContextCache([4, None], 64, 2, 8, torch.bfloat16, torch.device("cpu"))
    assert cache.nbytes == DraftContextCache.nbytes_for([4, None], 64, 2, 8, 2)


def _worker(slots=1):
    worker = DFlashWorker.__new__(DFlashWorker)
    worker.context = _cache([None], slots=slots)
    worker._slot_of = {}
    worker._parked = []
    worker._free_slots = list(range(slots))
    return worker


def _store(worker, uid, start, n):
    worker.context.append(worker.slot_of(uid), _kv(start, n, 1), start, n)


def test_next_turn_continues_the_finished_conversation():
    worker = _worker()
    prompt = torch.arange(100, 110)
    worker.begin_request(1, prompt, 0)
    _store(worker, 1, 0, 10)
    _store(worker, 1, 10, 3)  # decode
    reply = torch.cat([prompt, torch.tensor([7, 8, 9, 5])])
    worker.finish_request(1, reply)
    # the radix cache serves the first 12 tokens of the next turn
    nxt = torch.cat([reply, torch.tensor([1, 2])])
    worker.begin_request(2, nxt, 12)
    slot = worker.slot_of(2)
    assert worker.context.end_pos[slot] == 12
    # a later chunk of the same request keeps everything
    _store(worker, 2, 12, 4)
    worker.begin_request(2, nxt, 16)
    assert worker.context.end_pos[slot] == 16


def test_unrelated_request_starts_empty():
    worker = _worker()
    worker.begin_request(1, torch.arange(10), 0)
    _store(worker, 1, 0, 10)
    worker.finish_request(1, torch.arange(10))
    worker.begin_request(2, torch.arange(10).flip(0), 5)
    assert worker.context.end_pos[worker.slot_of(2)] == 0


def test_no_cached_prefix_starts_empty():
    worker = _worker()
    worker.begin_request(1, torch.arange(10), 0)
    _store(worker, 1, 0, 10)
    worker.finish_request(1, torch.arange(10))
    worker.begin_request(2, torch.arange(10), 0)
    assert worker.context.end_pos[worker.slot_of(2)] == 0


def test_concurrent_requests_hold_their_own_slots_and_continue_the_matching_one():
    worker = _worker(slots=2)
    a, b = torch.arange(0, 10), torch.arange(50, 60)
    worker.begin_request(1, a, 0)
    worker.begin_request(2, b, 0)
    slot_a, slot_b = worker.slot_of(1), worker.slot_of(2)
    assert {slot_a, slot_b} == {0, 1}
    _store(worker, 1, 0, 10)
    _store(worker, 2, 0, 10)
    worker.finish_request(1, a)
    worker.finish_request(2, b)
    # a follow-up of the first conversation finds its slot although the second parked later
    worker.begin_request(3, torch.cat([a, torch.tensor([1])]), 8)
    assert worker.slot_of(3) == slot_a and worker.context.end_pos[slot_a] == 8
    # a new conversation takes the remaining parked slot
    worker.begin_request(4, torch.arange(90, 99), 0)
    assert worker.slot_of(4) == slot_b and worker.context.end_pos[slot_b] == 0
