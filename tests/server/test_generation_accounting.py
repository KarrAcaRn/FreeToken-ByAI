"""The shared generation layer logs each request with its real token totals, so accounting is
independent of which endpoint served it — covering what the HTTP middleware can't record for a
stream (it fires before the totals are known)."""
from __future__ import annotations

import asyncio
import os
import sys
from types import SimpleNamespace

import pytest

# Same shim as the sibling server tests: the venv may hold a non-editable install, and without
# this the file only tests the source tree when a test that does insert it collects first.
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_PY = os.path.join(_ROOT, "python")
if _PY not in sys.path:
    sys.path.insert(0, _PY)

from freetoken.message import UserReply  # noqa: E402
from freetoken.server import api_server, request_ring  # noqa: E402
from freetoken.server.generation import (  # noqa: E402
    GenDone,
    GenSpec,
    GenTimings,
    build_metrics,
    generate_events,
    generate_full,
    timings_block,
)


@pytest.fixture(autouse=True)
def served_model_name():
    """_record_generation stamps the row from api_server._served_model_name(), which reads the
    module-global app state -- not the state handed to generate_*. Pin it so the recorded model
    name is deterministic instead of a leftover from whichever test ran before."""
    prev = api_server._GLOBAL_STATE
    api_server._GLOBAL_STATE = SimpleNamespace(
        config=SimpleNamespace(served_model_name="unit-model")
    )
    yield
    api_server._GLOBAL_STATE = prev


class FakeState:
    """Yields canned acks in place of the scheduler; carries only what the generation helpers
    read (`config.reasoning_parser`, `config.served_model_name`, `wait_for_ack`)."""

    def __init__(self, replies: list[UserReply]) -> None:
        self.config = SimpleNamespace(
            mm=SimpleNamespace(text_model_only=False, disabled_encoders=frozenset()),
            model_path="/m",
            served_model_name="unit-model",
            tool_call_parser="llama3",
            reasoning_parser=None,
        )
        self._replies = replies

    def new_user(self) -> int:
        return 42

    async def wait_for_ack(self, uid: int):
        assert uid == 42
        for reply in self._replies:
            yield reply


def _ack(
    prompt: int = 0,
    completion: int = 0,
    out: str = "",
    finished: bool = False,
    cached: int = 0,
    prefill_ms: float = 0.0,
    timings: dict | None = None,
) -> UserReply:
    return UserReply(
        uid=42,
        incremental_output=out,
        finished=finished,
        prompt_tokens_delta=prompt,
        completion_tokens_delta=completion,
        cached_tokens=cached,
        prefill_ms=prefill_ms,
        finish_reason="stop" if finished else None,
        timings=timings,
    )


def _sched_timings(**over) -> dict:
    """A scheduler ReqStats.finish payload: raw spans and counts, no derived rates."""
    t = dict(queue_ms=0.0, cache_n=0, prompt_n=0, prompt_ms=0.0, predicted_n=0,
             predicted_ms=0.0, draft_n=0, draft_n_accepted=0)
    t.update(over)
    return t


def _timings_state() -> SimpleNamespace:
    return SimpleNamespace(config=SimpleNamespace(enable_timings_report=True))


def _spec() -> GenSpec:
    return GenSpec(messages=[{"role": "user", "content": "hi"}], sampling_params=SimpleNamespace())


def _row(*, ttft_ms: int | None) -> request_ring.RequestRecord:
    return request_ring.RequestRecord(
        ts="2026-01-01T00:00:00Z", method="POST", path="/v1/messages", status=200,
        model="unit-model", duration_ms=1000, ttft_ms=ttft_ms, prompt_tokens=1,
        completion_tokens=1, stream=True, error=None,
    )


def _last_row() -> dict:
    rows, _ = request_ring.requests_since(0, 1000)
    return rows[-1]


@pytest.mark.parametrize("pools, expected", [(None, 1), ({"page_size": 64}, 64)])
def test_stats_reports_backend_page_size(pools, expected):
    from freetoken.server.stats import StatsTracker, build_stats

    tracker = StatsTracker()
    tracker.kv_total_pages = 130
    config = SimpleNamespace(served_model_name="unit-model", max_seq_len=262144,
                             page_size=1, served_modalities=(), model_config=SimpleNamespace())
    state = SimpleNamespace(stats=tracker, config=config, cache_pools=pools)
    doc = build_stats(state, 0, 0)
    assert doc["kv"] == {"used_pages": 0, "total_pages": 130, "page_size": expected}


def test_non_stream_records_the_request_with_real_token_totals():
    request_ring.reset()
    st = FakeState([_ack(prompt=5, completion=1, out="a"), _ack(completion=2, out="bc", finished=True)])
    result = asyncio.run(generate_full(42, _spec(), st, source="/v1/chat/completions"))
    assert (result.prompt_tokens, result.completion_tokens) == (5, 3)
    row = _last_row()
    assert row["path"] == "/v1/chat/completions"
    assert row["stream"] is False
    assert (row["prompt_tokens"], row["completion_tokens"]) == (5, 3)
    assert row["status"] == 200 and row["error"] is None
    assert row["model"] == "unit-model"


def test_stream_records_the_totals_from_gendone():
    request_ring.reset()
    st = FakeState([_ack(prompt=7, completion=1, out="x"), _ack(completion=4, out="yz", finished=True)])

    async def drain():
        done = None
        async for ev in generate_events(42, _spec(), st, source="/v1/messages"):
            if isinstance(ev, GenDone):
                done = ev
        return done

    done = asyncio.run(drain())
    assert (done.prompt_tokens, done.completion_tokens) == (7, 5)
    row = _last_row()
    assert row["path"] == "/v1/messages" and row["stream"] is True
    assert (row["prompt_tokens"], row["completion_tokens"]) == (7, 5)


def test_stream_still_records_the_row_when_the_client_disconnects_mid_stream():
    request_ring.reset()
    st = FakeState([_ack(prompt=9, completion=2, out="p"), _ack(completion=2, out="q", finished=True)])

    async def abort_after_first():
        gen = generate_events(42, _spec(), st, source="/v1/responses")
        async for _ev in gen:
            break  # the consumer stops early
        await gen.aclose()  # Starlette closes the generator on disconnect -> runs the finally

    asyncio.run(abort_after_first())
    row = _last_row()
    # Still logged on disconnect (the point); tokens are 0 since GenDone never arrived.
    assert row["path"] == "/v1/responses" and row["stream"] is True
    assert row["prompt_tokens"] == 0 and row["completion_tokens"] == 0


def test_a_generation_error_records_the_row_as_failed():
    request_ring.reset()
    st = FakeState([UserReply(uid=42, incremental_output="", finished=True, error="boom")])
    try:
        asyncio.run(generate_full(42, _spec(), st, source="/v1/chat/completions"))
    except Exception:
        pass
    row = _last_row()
    assert row["status"] == 500 and row["error"] == "boom"


def test_no_source_opts_out_of_recording():
    request_ring.reset()
    st = FakeState([_ack(prompt=1, completion=1, out="z", finished=True)])
    asyncio.run(generate_full(42, _spec(), st))  # no source
    rows, _ = request_ring.requests_since(0, 1000)
    assert rows == []


def test_stream_records_a_ttft_within_the_request_duration():
    request_ring.reset()
    st = FakeState([_ack(prompt=3, completion=1, out="a"), _ack(completion=1, out="b", finished=True)])

    async def drain():
        async for _ev in generate_events(42, _spec(), st, source="/v1/messages"):
            pass

    asyncio.run(drain())
    row = _last_row()
    assert row["ttft_ms"] is not None and 0 <= row["ttft_ms"] <= row["duration_ms"]


def test_non_stream_records_no_ttft():
    """generate_full hands the client one response: there is no first-token instant to observe."""
    request_ring.reset()
    st = FakeState([_ack(prompt=3, completion=2, out="ab", finished=True)])
    asyncio.run(generate_full(42, _spec(), st, source="/v1/chat/completions"))
    assert _last_row()["ttft_ms"] is None


def test_ttft_mean_covers_only_the_rows_that_have_one():
    """Non-streaming generations and middleware-logged rows carry no TTFT; averaging them in
    as zeros would drag the mean toward 0 as soon as anything hits /health."""
    request_ring.reset()
    for ms in (100, 200, 300):
        request_ring.record_request(_row(ttft_ms=ms))
    request_ring.record_request(_row(ttft_ms=None))
    assert request_ring.requests_ttft_mean_ms() == 200


def test_ttft_mean_is_zero_without_samples():
    request_ring.reset()
    request_ring.record_request(_row(ttft_ms=None))
    assert request_ring.requests_ttft_mean_ms() == 0


# ------------------------------------------------------- per-request metrics
# The timings ride the same ack stream the token totals do, so they are covered here rather
# than in each adapter's file; the adapter tests only check that the object reaches the wire.
def test_prefill_ms_from_the_engine_reaches_the_result_unchanged():
    """The scheduler measures the prefill span; the generation layer must pass it through
    rather than re-deriving it from ack arrival times (which batch together)."""
    st = FakeState([
        _ack(prompt=100, cached=40),
        _ack(completion=1, out="a", prefill_ms=12.5),
        _ack(completion=1, out="b", finished=True),
    ])
    result = asyncio.run(generate_full(42, _spec(), st))
    assert result.gen_timings.prefill_ms == 12.5
    assert result.cached_tokens == 40


# A real gap between acks, so a TTFT taken at the wrong ack is distinguishable from one taken
# at the right one; FakeState yields its whole list within a single event-loop tick.
_GAP_S = 0.02
_GAP_MS = _GAP_S * 1000


class PacedState(FakeState):
    async def wait_for_ack(self, uid: int):
        assert uid == 42
        for index, reply in enumerate(self._replies):
            if index:
                await asyncio.sleep(_GAP_S)
            yield reply


def test_ttft_is_measured_at_the_first_generated_token_not_the_admission_ack():
    """The admission ack carries prompt_tokens and no token; timing TTFT from it would report
    roughly the queue time for every request."""
    st = PacedState([
        _ack(prompt=5),
        _ack(completion=1, out="hi"),
        _ack(completion=1, out="!", finished=True),
    ])
    result = asyncio.run(generate_full(42, _spec(), st))
    # One gap to the first token (not zero, as an admission-timed TTFT would give), two to the end.
    assert _GAP_MS * 0.5 < result.gen_timings.ttft_ms < _GAP_MS * 1.9
    assert result.gen_timings.total_ms > result.gen_timings.ttft_ms + _GAP_MS * 0.5
    assert result.gen_timings.decode_ms > _GAP_MS * 0.5


def test_ttft_counts_a_token_the_detokenizer_held_back():
    """A token whose text is withheld (a trailing partial-stop prefix) is still a generated
    token: TTFT keys off completion_tokens_delta, not off non-empty output -- otherwise it
    would skip to the ack after it."""
    st = PacedState([
        _ack(prompt=5),
        _ack(completion=1, out=""),
        _ack(completion=1, out="done", finished=True),
    ])
    result = asyncio.run(generate_full(42, _spec(), st))
    assert _GAP_MS * 0.5 < result.gen_timings.ttft_ms < _GAP_MS * 1.9


def test_stream_gendone_carries_the_same_timings():
    st = FakeState([
        _ack(prompt=8, cached=2),
        _ack(completion=1, out="x", prefill_ms=7.0),
        _ack(completion=1, out="y", finished=True),
    ])

    async def drain():
        return [ev async for ev in generate_events(42, _spec(), st) if isinstance(ev, GenDone)]

    (done,) = asyncio.run(drain())
    assert done.gen_timings.prefill_ms == 7.0
    assert done.gen_timings.ttft_ms > 0.0


def test_build_metrics_splits_prompt_tokens_into_cached_and_prefilled():
    metrics = build_metrics(
        prompt_tokens=8192, completion_tokens=256, cached_tokens=6144,
        timings=GenTimings(ttft_ms=320.5, prefill_ms=410.0, decode_ms=5120.0, total_ms=5480.2),
    )
    # The identity the issue asks for: prompt_tokens == cached_prompt_tokens + prefill_tokens.
    assert metrics["cached_prompt_tokens"] + metrics["prefill_tokens"] == 8192
    assert metrics["prefill_tokens"] == 2048
    assert metrics["prefill_tokens_per_second"] == round(2048 / 0.410, 2)
    # Decode divides by completion_tokens - 1: the first token came out of prefill.
    assert metrics["decode_tokens_per_second"] == round(255 / 5.120, 2)
    assert metrics["decode_tokens"] == 256
    assert metrics["ttft_ms"] == 320.5
    assert metrics["total_time_ms"] == 5480.2


def test_build_metrics_rates_are_zero_rather_than_dividing_by_zero():
    metrics = build_metrics(
        prompt_tokens=10, completion_tokens=1, cached_tokens=0, timings=GenTimings()
    )
    assert metrics["prefill_tokens_per_second"] == 0.0
    # One generated token spans no decode interval, so there is no rate to report.
    assert metrics["decode_tokens_per_second"] == 0.0
    assert metrics["prefill_tokens"] == 10


def test_timings_block_follows_llama_cpp_semantics():
    t = timings_block(_timings_state(), _sched_timings(
        queue_ms=500.0, cache_n=800, prompt_n=200, prompt_ms=2500.0,
        predicted_n=21, predicted_ms=2000.0,
    ))
    # prompt_n excludes the cache; decode steps are n - 1 (llama.cpp semantics).
    assert t["cache_n"] == 800
    assert t["prompt_n"] == 200
    assert t["prompt_per_second"] == 80.0  # 200 evaluated tokens / 2.5 s
    assert t["predicted_n"] == 21
    assert t["predicted_per_second"] == 10.0  # 20 decode steps / 2.0 s
    assert t["prompt_ms"] == 2500.0 and t["predicted_ms"] == 2000.0
    assert t["queue_ms"] == 500.0  # FreeToken extension
    assert "draft_n" not in t and "draft_n_accepted" not in t  # no drafting


def test_timings_block_is_opt_in_and_needs_measured_spans():
    raw = _sched_timings(prompt_n=10, prompt_ms=100.0, predicted_n=2, predicted_ms=50.0)
    # off without the flag: usage.prompt_tokens - prompt_n would still leak the cache hit
    assert timings_block(SimpleNamespace(config=SimpleNamespace()), raw) is None
    # the responses helpers may pass no state at all
    assert timings_block(None, raw) is None
    # errors and aborts deliver no scheduler timings
    assert timings_block(_timings_state(), None) is None


def test_timings_report_is_on_by_default_on_next_and_can_be_turned_off():
    """next keeps serving timings by default (upstream opts in); the flag is a BooleanOptionalAction."""
    from freetoken.server.args import ServerArgs

    assert ServerArgs.enable_timings_report is True
    raw = _sched_timings(prompt_n=10, prompt_ms=100.0, predicted_n=2, predicted_ms=50.0)
    on = SimpleNamespace(config=SimpleNamespace(enable_timings_report=ServerArgs.enable_timings_report))
    assert timings_block(on, raw) is not None
    off = SimpleNamespace(config=SimpleNamespace(enable_timings_report=False))
    assert timings_block(off, raw) is None


def test_timings_block_rates_survive_the_edge_shapes():
    state = _timings_state()
    # one output token: the first rides the last prompt batch, so no decode steps
    t = timings_block(state, _sched_timings(prompt_n=10, prompt_ms=100.0, predicted_n=1, predicted_ms=0.001))
    assert t["predicted_per_second"] == 0.0 and t["predicted_per_token_ms"] == 0.0
    # fully cached prompt: nothing was evaluated
    t = timings_block(state, _sched_timings(prompt_n=0, prompt_ms=100.0, predicted_n=2, predicted_ms=50.0))
    assert t["prompt_per_second"] == 0.0 and t["prompt_per_token_ms"] == 0.0
    # values are passed through unrounded
    t = timings_block(state, _sched_timings(prompt_n=3, prompt_ms=1234.5678, predicted_n=2, predicted_ms=50.0))
    assert t["prompt_ms"] == 1234.5678 and t["prompt_per_token_ms"] == 1234.5678 / 3
    # speculative decoding adds the draft counters, and only then
    t = timings_block(state, _sched_timings(prompt_n=3, prompt_ms=300.0, predicted_n=5,
                                            predicted_ms=400.0, draft_n=64, draft_n_accepted=40))
    assert t["draft_n"] == 64 and t["draft_n_accepted"] == 40


def test_gen_done_and_result_carry_the_scheduler_timings():
    raw = _sched_timings(queue_ms=5.0, prompt_n=7, prompt_ms=70.0, predicted_n=5, predicted_ms=80.0)
    st = FakeState([
        _ack(prompt=7, completion=1, out="x"),
        _ack(completion=4, out="yz", finished=True, timings=raw),
    ])

    async def drain():
        done = None
        async for ev in generate_events(42, _spec(), st):
            if isinstance(ev, GenDone):
                done = ev
        return done

    done = asyncio.run(drain())
    assert done.timings is raw  # the terminal ack's scheduler spans, unchanged

    result = asyncio.run(generate_full(42, _spec(), FakeState(
        [_ack(prompt=5, completion=1, out="a"), _ack(completion=2, out="bc", finished=True, timings=raw)]
    )))
    assert result.timings is raw
