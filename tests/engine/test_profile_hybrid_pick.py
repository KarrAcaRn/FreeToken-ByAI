"""A `ft bench bw` profile picks hybrid from bandwidths alone; the engine keeps it only while
the GPU slot cache leaves enough misses for the CPU, and the auto-sized CPU pool leaves the
engine thread a core of its own."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from freetoken.engine.engine import _profile_hybrid_target, _resident_expert_share
from freetoken.moe.cpu_executor import auto_pool_cores


def _config(cache_size: int, *, overlap: bool = True, layers: int = 40, experts: int = 256):
    model_config = SimpleNamespace(num_experts=experts, num_moe_layers=layers, decode_target="hybrid")
    return SimpleNamespace(
        model_config=model_config,
        moe_cache_size=cache_size,
        moe_prefill_overlap=overlap,
        moe_strategy="hybrid",
    )


def test_resident_share_excludes_the_prefill_double_buffer():
    assert _resident_expert_share(_config(512 + 5120)) == pytest.approx(0.5)
    assert _resident_expert_share(_config(5120, overlap=False)) == pytest.approx(0.5)
    assert _resident_expert_share(_config(512)) == 0.0
    assert _resident_expert_share(_config(10**6)) == 1.0


@pytest.mark.parametrize("cache_size", [512 + 2048, 9902])  # 20% and 92% of 10240 experts
def test_mostly_resident_cache_falls_back_to_offload(cache_size):
    config = _config(cache_size)
    assert _profile_hybrid_target(config) == "gpu"
    assert config.moe_strategy == "offload"
    assert config.model_config.decode_target == "gpu"


def test_small_cache_keeps_the_profile_hybrid():
    config = _config(512 + 1024)  # 10% resident: enough misses for the CPU to win
    assert _profile_hybrid_target(config) == "hybrid"
    assert config.moe_strategy == "hybrid"
    assert config.model_config.decode_target == "hybrid"


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
