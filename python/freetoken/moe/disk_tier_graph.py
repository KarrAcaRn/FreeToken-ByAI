"""CUDA-graph-capturable decode fetch for the disk tier.

The v0 fetch (:meth:`DiskTier.fetch_pending`) runs on the host between kernels: per MoE layer
it reads the miss list back (a stream sync), reads the disk experts and launches the copies.
With 48 layers that is 48 syncs plus hundreds of eager launches per token, and the decode
cannot be captured. Here the host work moves to a coordinator thread behind a flag handshake
on stream memory operations (the CPU executor's mechanism), so a layer's decode is a fixed
sequence of device work:

    ensure_experts                 (slot cache: miss list on the device)
    split kernel                   disk misses -> list, RAM misses compacted in place
    D2H list -> ready flag         (cuStreamWriteValue)
    wait done flag                 (cuStreamWaitValue) <- coordinator: reads every segment of
                                   every disk miss at once into a pinned arena, writes a copy
                                   table (src, dst, bytes) and sets done
    H2D copy table, copy kernel    arena -> slot rows
    copy_missing (RAM misses), GEMM

Stream order makes one arena safe: layer l's copy kernel completes before layer l+1 raises
its ready flag.
"""

from __future__ import annotations

import ctypes
import os
import threading
import time

import numpy as np
import torch
import triton
import triton.language as tl

from freetoken.kernel.pinned import alloc_pinned_tensor
from freetoken.moe.host_banks import HostBank
from freetoken.utils import init_logger

logger = init_logger(__name__)

_ALIGN = 4096
_COPY_CHUNK = 64 << 10  # bytes per copy program


@triton.jit
def _split_misses_kernel(evict_ptr, src_ptr, num_ptr, disk_ids_ptr, disk_slots_ptr, disk_num_ptr,
                         ram, BLOCK: tl.constexpr):
    """Misses with a row >= ram go to the disk list; the rest stay, compacted, for copy_missing."""
    offs = tl.arange(0, BLOCK)
    n = tl.load(num_ptr)
    valid = offs < n
    src = tl.load(src_ptr + offs, mask=valid, other=0)
    slot = tl.load(evict_ptr + offs, mask=valid, other=0)
    disk = valid & (src >= ram)
    keep = valid & (src < ram)
    disk_pos = tl.cumsum(disk.to(tl.int32), 0) - 1
    keep_pos = tl.cumsum(keep.to(tl.int32), 0) - 1
    tl.store(disk_ids_ptr + disk_pos, src, mask=disk)
    tl.store(disk_slots_ptr + disk_pos, slot, mask=disk)
    tl.debug_barrier()
    tl.store(src_ptr + keep_pos, src, mask=keep)
    tl.store(evict_ptr + keep_pos, slot, mask=keep)
    tl.store(num_ptr, tl.sum(keep.to(tl.int32), 0))
    tl.store(disk_num_ptr, tl.sum(disk.to(tl.int32), 0))


@triton.jit
def _table_copy_kernel(table_ptr, count_ptr, CHUNK: tl.constexpr, BLOCK: tl.constexpr):
    """table[i] = (src address, dst address, bytes); 4-byte words, sources read uncached
    (the host rewrote them since the last layer)."""
    i = tl.program_id(0)
    if i >= tl.load(count_ptr):
        return
    src = tl.load(table_ptr + 3 * i).to(tl.pointer_type(tl.int32))
    dst = tl.load(table_ptr + 3 * i + 1).to(tl.pointer_type(tl.int32))
    words = tl.load(table_ptr + 3 * i + 2) // 4
    start = tl.program_id(1) * (CHUNK // 4)
    for w0 in range(start, tl.minimum(start + CHUNK // 4, words), BLOCK):
        offs = w0 + tl.arange(0, BLOCK)
        mask = offs < words
        tl.store(dst + offs, tl.load(src + offs, mask=mask, cache_modifier=".cv"), mask=mask)


class DiskTierGraphFetch:
    """The capturable decode fetch of one :class:`DiskTier` (see the module docstring)."""

    def __init__(self, tier, cache, num_layers: int, max_misses: int, workers) -> None:
        from freetoken.kernel import _cpu_moe  # stream memops live there

        probe = alloc_pinned_tensor(1, dtype=torch.int64)
        probe.zero_()
        if not _cpu_moe.memops_probe(torch.cuda.current_stream().cuda_stream, probe.data_ptr()):
            raise RuntimeError("--disk-tier-graph needs CUDA stream memory operations, which this "
                               "driver/device does not support (vGPU, WDDM, old driver)")
        self._tier = tier
        self._cache = cache
        self._pool = workers
        self._max = max_misses
        dev = cache.device
        self._disk_ids = torch.zeros(max_misses, dtype=torch.int32, device=dev)
        self._disk_slots = torch.zeros(max_misses, dtype=torch.int32, device=dev)
        self._disk_num = torch.zeros(1, dtype=torch.int32, device=dev)
        self._h_ids = alloc_pinned_tensor(max_misses, dtype=torch.int32)
        self._h_slots = alloc_pinned_tensor(max_misses, dtype=torch.int32)
        self._h_num = alloc_pinned_tensor(1, dtype=torch.int32)
        self._ready = alloc_pinned_tensor(num_layers, dtype=torch.int64)
        self._done = alloc_pinned_tensor(num_layers, dtype=torch.int64)
        self._ready.zero_()
        self._done.zero_()
        segs_per_expert = sum(len(tier._dst_slices[b]) for b in range(len(tier._banks)))
        self._max_rows = max_misses * segs_per_expert
        self._h_table = alloc_pinned_tensor(self._max_rows * 3 + 1, dtype=torch.int64)
        self._table = torch.zeros(self._max_rows * 3 + 1, dtype=torch.int64, device=dev)
        # per expert: every segment's aligned read, plus the fp16 rows the global scales expand into
        per_expert = sum(
            nb + 2 * _ALIGN for b in range(len(tier._banks)) for _s, _o, nb in tier._index.row_segments(b, 0, 0))
        per_expert += sum(tier._row_bytes[b] + _ALIGN for b in (2, 5) if b < len(tier._row_bytes))
        self._arena = HostBank((max_misses * per_expert,), torch.uint8)
        self._arena.pin()
        self._max_bytes = max(nb for b in range(len(tier._banks)) for _s, _o, nb in tier._index.row_segments(b, 0, 0))
        self._ready_np = self._ready.numpy()
        self._done_np = self._done.numpy()
        self._error: BaseException | None = None
        self._thread = threading.Thread(target=self._coordinator, name="disk-tier-graph", daemon=True)
        self._thread.start()

    # ------------------------------------------------------------------ device side
    def fetch(self, layer_id: int) -> None:
        """Enqueue this layer's disk fetch on the current stream (eager or captured)."""
        from freetoken.kernel import _cpu_moe

        cache = self._cache
        if self._error is not None:
            raise RuntimeError("disk-tier graph coordinator failed") from self._error
        block = triton.next_power_of_2(max(self._max, 16))
        _split_misses_kernel[(1,)](
            cache.evict_slots, cache.src_indices, cache.num_indices,
            self._disk_ids, self._disk_slots, self._disk_num, self._tier._ram, BLOCK=block,
        )
        self._h_ids.copy_(self._disk_ids, non_blocking=True)
        self._h_slots.copy_(self._disk_slots, non_blocking=True)
        self._h_num.copy_(self._disk_num, non_blocking=True)
        stream = torch.cuda.current_stream().cuda_stream
        _cpu_moe.memop_submit(stream, self._done.data_ptr(), self._ready.data_ptr(), layer_id)
        _cpu_moe.memop_sync(stream, self._done.data_ptr(), layer_id)
        self._table.copy_(self._h_table, non_blocking=True)
        chunks = triton.cdiv(self._max_bytes, _COPY_CHUNK)
        _table_copy_kernel[(self._max_rows, chunks)](
            self._table, self._table[self._max_rows * 3:], CHUNK=_COPY_CHUNK, BLOCK=1024, num_warps=4,
        )

    # ------------------------------------------------------------------ host side
    def _coordinator(self) -> None:
        torch.cuda.set_device(self._cache.device)
        while True:
            hot = np.flatnonzero(self._ready_np)
            if hot.size == 0:
                time.sleep(0)  # yield the GIL; the decode thread drives the model meanwhile
                continue
            for layer in hot.tolist():
                self._ready_np[layer] = 0
                try:
                    self._serve(layer)
                except BaseException as exc:  # noqa: BLE001 -- surfaced by fetch()
                    self._error = exc
                    logger.error(f"disk-tier graph coordinator: {exc!r}")
                    self._h_table[self._max_rows * 3] = 0
                self._done_np[layer] = 1

    def _serve(self, layer: int) -> None:
        tier = self._tier
        n = int(self._h_num[0])
        if n > self._max:
            raise RuntimeError(f"{n} disk misses in one layer exceed the graph fetch capacity {self._max}")
        ids, slots = self._h_ids[:n].tolist(), self._h_slots[:n].tolist()
        arena, table = self._arena, self._h_table.numpy()
        reads, rows, pos = [], 0, 0
        for e, slot in zip(ids, slots):
            for bank_idx, (_host, gpu_cache) in enumerate(tier._banks):
                row = gpu_cache[slot]
                for (d0, d1), (shard_idx, off, nbytes) in zip(tier._dst_slices[bank_idx],
                                                               tier._index.row_segments(bank_idx, layer, e)):
                    _fd, direct = tier._fd(shard_idx)
                    a0, slen = ((off & ~(_ALIGN - 1)), ((off + nbytes - (off & ~(_ALIGN - 1)) + _ALIGN - 1) & ~(_ALIGN - 1))) \
                        if direct else (off, nbytes)
                    reads.append((arena.addr + pos, shard_idx, a0, slen))
                    src = pos + off - a0
                    # the slice's own address: a 2-D bank row (gate|up) slices whole rows
                    dst = row[d0:d1]
                    if bank_idx in (2, 5):
                        # per-expert fp32 global scale -> the fp16 row it is broadcast into
                        out_bytes = dst.numel() * dst.element_size()
                        reads[-1] = reads[-1] + ((src, pos + slen, dst.numel()),)
                        table[3 * rows: 3 * rows + 3] = (arena.addr + pos + slen, dst.data_ptr(), out_bytes)
                        pos += ((slen + out_bytes + _ALIGN - 1) & ~(_ALIGN - 1))
                    else:
                        table[3 * rows: 3 * rows + 3] = (arena.addr + src, dst.data_ptr(), nbytes)
                        pos += (slen + _ALIGN - 1) & ~(_ALIGN - 1)
                    rows += 1
        for f in [self._pool.submit(self._read, r) for r in reads]:
            f.result()
        table[self._max_rows * 3] = rows
        tier._fetches += n
        tier._fetch_bytes += sum(tier._row_bytes) * n

    def _read(self, item) -> None:
        addr, shard_idx, a0, slen = item[:4]
        fd, _direct = self._tier._fd(shard_idx)
        os.preadv(fd, [(ctypes.c_char * slen).from_address(addr)], a0)
        if len(item) == 5:  # global-scale segment: expand the fp32 scalar into an fp16 row
            src, dst, count = item[4]
            arena = self._arena.tensor
            val = arena[src:src + 4].view(torch.float32)[0].to(torch.float16)
            arena[dst:dst + 2 * count].view(torch.float16).fill_(val)


__all__ = ["DiskTierGraphFetch"]
