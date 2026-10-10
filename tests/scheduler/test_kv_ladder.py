"""--enable-kv-ladder: the pure rung arithmetic and the serve-flag checks. The rebuild it triggers
is the ordinary runtime cache rebuild (tests/scheduler/test_cache_rebuild.py)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from freetoken.scheduler.kv_ladder import KVLadderCapacityError, KVLadderPolicy

STEP, PAGE = 32_768, 64
KV_PAGE, MOE_SLOT = 1 << 20, 3 << 20


def _policy(budget_slots: int = 6000, ceiling: int = 262_144, floor: int = 512) -> KVLadderPolicy:
    return KVLadderPolicy(
        step_tokens=STEP, max_context_tokens=ceiling, page_size=PAGE,
        pool_budget_bytes=budget_slots * MOE_SLOT, kv_bytes_per_page=KV_PAGE,
        moe_bytes_per_slot=MOE_SLOT, min_moe_slots=floor,
    )


def test_a_request_below_the_rung_keeps_the_geometry():
    p = _policy()
    assert p.initial_tokens == 2 * STEP
    assert p.plan(current_pages=1024, current_moe_slots=5000, input_tokens=1000, max_output_tokens=4000) is None


def test_reaching_the_rung_grows_kv_and_pays_with_moe_slots():
    p = _policy()
    plan = p.plan(current_pages=1024, current_moe_slots=5600, input_tokens=60_000, max_output_tokens=5536)
    assert plan.target_tokens == 3 * STEP and plan.target_pages == 3 * STEP // PAGE
    # what the slots can still afford after the bigger KV, never more than before
    assert plan.target_moe_slots == (6000 * MOE_SLOT - plan.target_pages * KV_PAGE) // MOE_SLOT
    assert plan.target_moe_slots < 5600


def test_a_long_request_skips_rungs_and_stops_at_the_ceiling():
    p = _policy(ceiling=200_000)
    plan = p.plan(current_pages=1024, current_moe_slots=5000, input_tokens=150_000, max_output_tokens=90_000)
    assert plan.target_tokens == 200_000
    assert p.plan(current_pages=200_000 // PAGE, current_moe_slots=5000,
                  input_tokens=150_000, max_output_tokens=90_000) is None


def test_a_rung_below_the_moe_floor_is_refused():
    p = _policy(budget_slots=1000, floor=900)
    with pytest.raises(KVLadderCapacityError, match="minimum 900 MoE slots"):
        p.plan(current_pages=1024, current_moe_slots=950, input_tokens=60_000, max_output_tokens=8000)


class _Config:
    def to_dict(self) -> dict:
        return {"architectures": ["LlamaForCausalLM"], "torch_dtype": "bfloat16"}


def _parse(argv: list[str]):
    from freetoken.server.args import parse_args

    with patch("freetoken.utils.cached_load_hf_config", lambda _path: _Config()):
        return parse_args(["--model", "/models/anon", *argv])


def test_the_flag_reserves_the_first_rung():
    # read kwargs["moe_backend"], which next renamed to moe_strategy: a KeyError at startup
    args, _ = _parse(["--enable-kv-ladder", "--max-running-requests", "1", "--moe-strategy", "offload",
                      "--moe-cache-auto", "--ladder-step-size", "16384"])
    assert args.enable_kv_ladder and args.kv_reserve_tokens >= 2 * 16384


def test_the_default_strategy_needs_no_cache_flag():
    args, _ = _parse(["--enable-kv-ladder", "--max-running-requests", "1"])
    assert args.kv_reserve_tokens >= 2 * STEP


@pytest.mark.parametrize("argv", [
    ["--max-running-requests", "1", "--moe-cache-size", "4000"],
    ["--max-running-requests", "2", "--moe-strategy", "offload", "--moe-cache-auto"],
    ["--max-running-requests", "1", "--moe-strategy", "cpu"],
])
def test_unsupported_setups_are_refused(argv):
    with pytest.raises(SystemExit):
        _parse(["--enable-kv-ladder", *argv])
