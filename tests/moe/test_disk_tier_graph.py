from __future__ import annotations

import pytest
import torch

if not torch.cuda.is_available():  # pragma: no cover
    pytest.skip("CUDA required", allow_module_level=True)

from freetoken.kernel.pinned import alloc_pinned_tensor
from freetoken.moe.disk_tier_graph import _split_misses_kernel, _table_copy_kernel


def test_split_moves_disk_misses_out_and_compacts_the_rest():
    evict = torch.tensor([5, 6, 7, 8, 9, 0, 0, 0], dtype=torch.int32, device="cuda")
    src = torch.tensor([1, 40, 2, 50, 3, 0, 0, 0], dtype=torch.int32, device="cuda")
    num = torch.tensor([5], dtype=torch.int32, device="cuda")
    ids = torch.full((8,), -1, dtype=torch.int32, device="cuda")
    slots = torch.full((8,), -1, dtype=torch.int32, device="cuda")
    disk_num = torch.zeros(1, dtype=torch.int32, device="cuda")
    _split_misses_kernel[(1,)](evict, src, num, ids, slots, disk_num, 32, BLOCK=16)
    assert disk_num.item() == 2 and ids[:2].tolist() == [40, 50] and slots[:2].tolist() == [6, 8]
    assert num.item() == 3 and src[:3].tolist() == [1, 2, 3] and evict[:3].tolist() == [5, 7, 9]


def test_table_copy_lands_host_bytes_in_row_slices():
    """Each table row copies host bytes to a device address -- here the two halves of a 2-D
    gate|up bank row, whose slice offsets are whole rows, not elements."""
    bank = torch.zeros(4, 6, 8, dtype=torch.uint8, device="cuda")  # [slots, rows, bytes]
    host = alloc_pinned_tensor(2 * 3 * 8, dtype=torch.uint8)
    host.copy_(torch.arange(48, dtype=torch.uint8))
    row = bank[2]
    table_h = alloc_pinned_tensor(3 * 4 + 1, dtype=torch.int64)
    table_h.zero_()
    table_h[0:3] = torch.tensor([host.data_ptr(), row[0:3].data_ptr(), 24])
    table_h[3:6] = torch.tensor([host.data_ptr() + 24, row[3:6].data_ptr(), 24])
    table_h[12] = 2
    table = table_h.cuda()
    _table_copy_kernel[(4, 1)](table, table[12:], CHUNK=1024, BLOCK=256)
    torch.cuda.synchronize()
    assert torch.equal(row.reshape(-1).cpu(), torch.arange(48, dtype=torch.uint8))
    assert bank[1].count_nonzero() == 0 and bank[3].count_nonzero() == 0
