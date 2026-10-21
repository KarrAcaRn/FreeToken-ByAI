"""Hybrid auto fetch split for layer kinds without an `ft bench bw` row: the engine's startup
measurement (benchbw.measure_hybrid_split), its per-GPU cache (bench_profile), and how the
engine combines it with the profile rows."""

from types import SimpleNamespace

import pytest
import torch

from freetoken.moe import bench_profile as bp

KEY = bp.layer_kind_key("mxfp4_triton", {}, 256, 128, 2, 0)


def test_startup_split_cache_round_trip(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    assert bp.load_startup_hybrid_fraction("GPU-x", KEY) is None
    bp.save_startup_hybrid_split("GPU-x", KEY, {"cpu_moe_overlap_gbs": 30.0,
                                                 "pcie_gather_overlap_gbs": 10.0})
    assert bp.load_startup_hybrid_fraction("GPU-x", KEY) == pytest.approx(0.25)
    assert bp.load_startup_hybrid_fraction("GPU-y", KEY) is None  # per GPU
    # never under benchbw/, where the profile lookup would take it for a profile
    assert bp.latest_profile_path() is None


def _method(fmt: str, hidden: int, inter: int, opts: dict | None = None):
    cfg = SimpleNamespace(hidden=hidden, local_intermediate=inter, top_k=2, num_experts=8,
                          activation="silu", alpha=1.702, limit=None)
    return SimpleNamespace(cfg=cfg, cpu_spec=lambda: (fmt, dict(opts or {})))


@pytest.fixture
def two_kinds(tmp_path, monkeypatch):
    """A model with a bf16 and an nvfp4 layer kind; the profile has a row for the bf16 one only."""
    from freetoken.engine import engine as eng
    from freetoken.env import ENV
    from freetoken.moe import benchbw

    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    monkeypatch.setattr(ENV.HYBRID_STARTUP_BENCH, "value", True)
    methods = [_method("bf16", 256, 128), _method("nvfp4", 256, 64), _method("bf16", 256, 128)]
    monkeypatch.setattr(eng, "offload_layer_methods", lambda model: methods)
    monkeypatch.setattr(eng, "_profile_gpu", lambda index=None: ("FAKE GPU", "GPU-x"))
    monkeypatch.setattr(eng, "_cpu_pool_thread_counts", lambda requested: {6})
    rows = {bp.layer_kind_key("bf16", {}, 256, 128, 2, 6): {"cpu_moe_gbs": 100.0, "pcie_gather_gbs": 40.0}}
    monkeypatch.setattr(bp, "load_layer_kinds", lambda **kw: rows)
    benched = []

    def measure(fmt, wl, device, num_threads):
        benched.append((fmt, wl.hidden, wl.inter))
        return {"cpu_moe_overlap_gbs": 30.0, "pcie_gather_overlap_gbs": 10.0}

    monkeypatch.setattr(benchbw, "measure_hybrid_split", measure)
    engine = SimpleNamespace(model=None, device=torch.device("cpu"),
                             cpu_moe_executor=SimpleNamespace(num_threads=6, isa="avx2"))
    engine._profile_layer_rows = lambda: eng.Engine._profile_layer_rows(engine)
    config = SimpleNamespace(moe_hybrid_max_fetch=-1, moe_cpu_threads=0, tp_info=SimpleNamespace(size=1))
    return eng, engine, config, benched


def test_startup_bench_covers_only_the_kinds_without_a_row(two_kinds):
    eng, engine, config, benched = two_kinds
    split = eng.Engine._startup_hybrid_fractions(engine, config)
    assert benched == [("nvfp4", 256, 64)]
    assert split == {("nvfp4", (), 256, 64, 2): pytest.approx(0.25)}
    # the next launch reads the cached measurement
    assert eng.Engine._startup_hybrid_fractions(engine, config) == split
    assert len(benched) == 1


def test_profile_rows_first_then_the_startup_split(two_kinds):
    eng, engine, config, _ = two_kinds
    split = eng.Engine._startup_hybrid_fractions(engine, config)
    cache = SimpleNamespace(hybrid_max_fetch=None, hybrid_fetch_fraction=None, locked_hybrid=frozenset())
    eng.Engine._resolve_hybrid_fetch(engine, config, cache, split)
    assert cache.hybrid_max_fetch == 1
    assert cache.hybrid_fetch_fraction == [pytest.approx(0.4), pytest.approx(0.25), pytest.approx(0.4)]
    # without a startup split the row-less layer keeps the fixed cap (fraction 0)
    eng.Engine._resolve_hybrid_fetch(engine, config, cache, {})
    assert cache.hybrid_fetch_fraction == [pytest.approx(0.4), 0.0, pytest.approx(0.4)]


def test_startup_bench_off_switch_and_explicit_cap(two_kinds, monkeypatch):
    from freetoken.env import ENV

    eng, engine, config, benched = two_kinds
    monkeypatch.setattr(ENV.HYBRID_STARTUP_BENCH, "value", False)
    assert eng.Engine._startup_hybrid_fractions(engine, config) == {}
    monkeypatch.setattr(ENV.HYBRID_STARTUP_BENCH, "value", True)
    config.moe_hybrid_max_fetch = 2
    assert eng.Engine._startup_hybrid_fractions(engine, config) == {}
    assert benched == []


@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")
def test_measure_hybrid_split_returns_an_overlapped_pair():
    pytest.importorskip("freetoken.kernel._cpu_moe", reason="the CPU MoE executor is not built")
    from freetoken.moe import benchbw as bb

    wl = bb.Workload("tiny", 256, 128, 8, 2, ("bf16",))
    entry = bb.measure_hybrid_split("bf16", wl, torch.device("cuda"), num_threads=2, seconds=0.2)
    assert entry["cpu_moe_overlap_gbs"] > 0 and entry["pcie_gather_overlap_gbs"] > 0
    assert 0.0 < bp.fetch_fraction(entry) <= 1.0
    assert bb._BENCH_BANKS == []  # released
    assert bb._SYNTH_BANK_BUDGET == 2 << 30  # budget restored
