"""The auto-sized CPU MoE pool leaves the engine thread a core of its own."""

from __future__ import annotations

import pytest

from freetoken.moe.cpu_executor import auto_pool_cores


@pytest.mark.parametrize(
    "cores, flag_sync, workers, coord",
    [
        (list(range(8)), True, list(range(6)), 6),  # 8-core VM: 6 workers + coordinator + engine
        (list(range(8)), False, list(range(7)), -1),
        (list(range(4)), True, [0, 1], 2),
        (list(range(3)), True, [0, 1], 2),  # too few cores to reserve the engine one
        (list(range(2)), True, [0, 1], -1),
    ],
)
def test_auto_pool_leaves_the_engine_thread_a_core(cores, flag_sync, workers, coord):
    assert auto_pool_cores(cores, flag_sync) == (workers, coord)
