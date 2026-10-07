"""Hybrid auto fetch split without an `ft bench bw` profile: the engine's startup measurement
(benchbw.measure_hybrid_split) and its per-GPU cache (bench_profile)."""

import pytest
import torch

from freetoken.moe import bench_profile as bp

GEOMETRY = {"hidden": 256, "inter": 128, "experts": 8, "top_k": 2}


def test_fraction_from_entry_prefers_the_overlapped_pair():
    assert bp.hybrid_fraction_from_entry(
        {"cpu_moe_overlap_gbs": 30.0, "pcie_gather_overlap_gbs": 20.0,
         "cpu_moe_gbs": 40.0, "pcie_gather_gbs": 10.0}) == pytest.approx(0.4)
    assert bp.hybrid_fraction_from_entry({"cpu_moe_gbs": 40.0, "pcie_gather_gbs": 10.0}) == 0.25
    assert bp.hybrid_fraction_from_entry({}) is None


def test_startup_split_cache_round_trip(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    key = bp.startup_split_key("mxfp4", GEOMETRY)
    assert key == "mxfp4_triton:256x128x8x2"
    assert bp.load_startup_hybrid_fraction("GPU-x", key) is None
    bp.save_startup_hybrid_split("GPU-x", key, {"cpu_moe_overlap_gbs": 30.0,
                                                 "pcie_gather_overlap_gbs": 10.0})
    assert bp.load_startup_hybrid_fraction("GPU-x", key) == pytest.approx(0.25)
    assert bp.load_startup_hybrid_fraction("GPU-y", key) is None  # per GPU
    # never under benchbw/, where the profile lookup would take it for a profile
    assert bp.latest_profile_path() is None


@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")
def test_measure_hybrid_split_returns_an_overlapped_pair():
    pytest.importorskip("freetoken.kernel._cpu_moe", reason="the CPU MoE executor is not built")
    from freetoken.moe import benchbw as bb

    wl = bb.Workload("tiny", 256, 128, 8, 2, ("bf16",))
    entry = bb.measure_hybrid_split("bf16", wl, torch.device("cuda"), num_threads=2, seconds=0.2)
    assert entry["cpu_moe_overlap_gbs"] > 0 and entry["pcie_gather_overlap_gbs"] > 0
    assert 0.0 < bp.hybrid_fraction_from_entry(entry) <= 1.0
    assert bb._BENCH_BANKS == []  # released
    assert bb._SYNTH_BANK_BUDGET == 2 << 30  # budget restored
