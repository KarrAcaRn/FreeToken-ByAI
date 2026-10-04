"""DFlash draft context: the windowed K/V cache and the multi-turn carry-over."""

from __future__ import annotations

import torch

from freetoken.speculative.dflash.context import DraftContextCache
from freetoken.speculative.dflash.worker import DFlashWorker


def _cache(windows, max_len=64):
    return DraftContextCache(windows, max_len, 1, 1, torch.float32, torch.device("cpu"))


def _kv(start, n, layers):
    # each entry stores its own absolute position, so a view shows which positions it holds
    rows = torch.arange(start, start + n, dtype=torch.float32).view(n, 1, 1)
    return [(rows, -rows) for _ in range(layers)]


def _positions(cache, i):
    k, v = cache.layer_kv(i)
    assert torch.equal(v, -k)
    return k.flatten().int().tolist()


def test_sliding_layer_keeps_its_window_across_compactions():
    cache = _cache([4, None])
    for start in range(0, 20, 3):
        cache.append(_kv(start, 3, 2), start, 3)
    assert cache.end_pos == 21
    assert _positions(cache, 0) == [17, 18, 19, 20]
    assert _positions(cache, 1) == list(range(21))
    assert cache.k[0].shape[0] == 8  # 2 x window, preallocated


def test_long_append_keeps_only_the_window_tail():
    cache = _cache([4])
    cache.append(_kv(0, 2, 1), 0, 2)
    # the caller may pass just the rows a layer keeps (rows_needed) for a long prefill chunk
    cache.append(_kv(8, 4, 1), 2, 10)
    assert cache.end_pos == 12
    assert _positions(cache, 0) == [8, 9, 10, 11]


def test_rows_needed():
    assert _cache([4, 6]).rows_needed == 6
    assert _cache([4, None]).rows_needed is None
    assert _cache([128]).rows_needed is None  # a window past max_len is full attention


def test_truncate_and_non_contiguous_append():
    cache = _cache([None])
    cache.append(_kv(0, 10, 1), 0, 10)
    cache.append(_kv(6, 2, 1), 6, 2)  # rewinds to 6, then appends
    assert _positions(cache, 0) == list(range(8))
    cache.append(_kv(20, 2, 1), 20, 2)  # a gap restarts the context
    assert _positions(cache, 0) == [20, 21]
    assert cache.end_pos == 22


def test_nbytes_matches_allocation():
    cache = DraftContextCache([4, None], 64, 2, 8, torch.bfloat16, torch.device("cpu"))
    assert cache.nbytes == DraftContextCache.nbytes_for([4, None], 64, 2, 8, 2)


def _worker():
    worker = DFlashWorker.__new__(DFlashWorker)
    worker.context = _cache([None])
    worker._uid = None
    worker._last_tokens = None
    worker.last_draft_probs = None
    return worker


def test_next_turn_continues_the_finished_conversation():
    worker = _worker()
    prompt = torch.arange(100, 110)
    worker.begin_request(1, prompt, 0)
    worker.context.append(_kv(0, 10, 1), 0, 10)
    worker.context.append(_kv(10, 3, 1), 10, 3)  # decode
    reply = torch.cat([prompt, torch.tensor([7, 8, 9, 5])])
    worker.finish_request(reply)
    # the radix cache serves the first 12 tokens of the next turn
    nxt = torch.cat([reply, torch.tensor([1, 2])])
    worker.begin_request(2, nxt, 12)
    assert worker.context.end_pos == 12
    # a later chunk of the same request keeps everything
    worker.context.append(_kv(12, 4, 1), 12, 4)
    worker.begin_request(2, nxt, 16)
    assert worker.context.end_pos == 16


def test_unrelated_request_starts_empty():
    worker = _worker()
    worker.begin_request(1, torch.arange(10), 0)
    worker.context.append(_kv(0, 10, 1), 0, 10)
    worker.finish_request(torch.arange(10))
    other = torch.arange(10).flip(0)
    worker.begin_request(2, other, 5)
    assert worker.context.end_pos == 0


def test_no_cached_prefix_starts_empty():
    worker = _worker()
    worker.begin_request(1, torch.arange(10), 0)
    worker.context.append(_kv(0, 10, 1), 0, 10)
    worker.finish_request(torch.arange(10))
    worker.begin_request(2, torch.arange(10), 0)
    assert worker.context.end_pos == 0
