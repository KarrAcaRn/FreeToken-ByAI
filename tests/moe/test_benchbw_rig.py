"""``ft bench bw`` synthetic rigs: the bench banks and the decode-shaped PCIe gather."""

import pytest
import torch

pytestmark = pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")


def test_bench_bank_is_filled_pinned_and_released():
    from freetoken.moe import benchbw as bb

    t = bb._bench_bank(4, 1000, dtype=torch.bfloat16)
    assert t.shape == (4, 1000) and t.dtype == torch.bfloat16
    assert t.is_pinned()
    assert bool((t.view(torch.uint8) == bb._BENCH_FILL).all())  # written, never zero pages
    # the GPU reads it zero-copy through its host address
    dev = t.view(torch.uint8).to("cuda", non_blocking=True)
    torch.cuda.synchronize()
    assert bool((dev == bb._BENCH_FILL).all())
    del t, dev
    bb._release_bench_banks()
    assert bb._BENCH_BANKS == []


def test_gather_rig_copies_top_k_experts_per_step():
    from freetoken.moe import benchbw as bb

    wl = bb.Workload("tiny", 256, 128, 8, 2, ("nvfp4",))
    step, step_bytes = bb._build_gather_rig("nvfp4", wl, torch.device("cuda"))
    cache = step.cache
    assert int(cache.num_indices.item()) == wl.top_k
    assert step_bytes == wl.top_k * bb._expert_bytes("nvfp4", wl.hidden, wl.inter)
    for dst in cache.bank_caches.values():
        dst.zero_()
    seen = set()
    for _ in range(4):
        step()
        seen.add(tuple(cache.src_indices[: wl.top_k].tolist()))
    torch.cuda.synchronize()
    assert len(seen) > 1  # every step reads a different set of experts
    slots = cache.evict_slots[: wl.top_k].long()
    for dst in cache.bank_caches.values():
        assert bool((dst[slots].view(torch.uint8) == bb._BENCH_FILL).all())
    del step, cache, dst
    bb._release_bench_banks()
