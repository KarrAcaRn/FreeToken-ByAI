"""AdaptiveGate: the baseline is the verify forward scaled to a plain decode step."""

from __future__ import annotations

from freetoken.speculative.utils import AdaptiveGate


class _Event:
    def __init__(self, t: float):
        self.t = t

    def elapsed_time(self, other: _Event) -> float:
        return other.t - self.t

    def synchronize(self) -> None:
        pass


def _cycle(gate: AdaptiveGate, *, cycle_ms: float, verify_ms: float, tokens: int, scale: float):
    gate.record_events(
        cycle=(_Event(0.0), _Event(cycle_ms)),
        target=(_Event(0.0), _Event(verify_ms)),
        out_tokens=tokens,
        baseline_scale=scale,
    )


def _gate() -> AdaptiveGate:
    gate = AdaptiveGate(min_cycles=4, eval_interval=4, warmup_cycles=0, margin=1.15)
    gate.should_run(1)
    return gate


def test_unscaled_proxy_keeps_a_slower_than_plain_cycle():
    # 29 ms per token vs a 26 ms verify forward: within the 1.15 margin of the raw proxy
    gate = _gate()
    for _ in range(4):
        _cycle(gate, cycle_ms=29.0, verify_ms=26.0, tokens=1, scale=1.0)
    assert gate.enabled


def test_scaled_proxy_disables_a_slower_than_plain_cycle():
    # the same cycle against the calibrated plain step (26 x 0.85 = 22.1 ms) is a loss
    gate = _gate()
    for _ in range(4):
        _cycle(gate, cycle_ms=29.0, verify_ms=26.0, tokens=1, scale=0.85)
    assert not gate.enabled


def test_scaled_proxy_keeps_a_winning_cycle():
    gate = _gate()
    for _ in range(8):
        _cycle(gate, cycle_ms=36.0, verify_ms=26.0, tokens=4, scale=0.85)
    assert gate.enabled


def test_first_steps_of_a_request_probe_plain_decode():
    gate = AdaptiveGate(probe_steps=2, probe_after=3)
    assert [gate.should_run(1) for _ in range(6)] == [True, True, True, False, False, True]
    assert gate.probing is False
    # a new request probes again
    assert [gate.should_run(2) for _ in range(4)] == [True, True, True, False]


def test_measured_plain_step_replaces_the_proxy():
    # the proxy (verify 26 ms x 1.0) would keep a 29 ms/token cycle; two timed plain steps
    # of 20 ms say speculation loses
    gate = AdaptiveGate(min_cycles=4, eval_interval=4, warmup_cycles=0, margin=1.15, probe_steps=2,
                        probe_after=0)
    for _ in range(2):
        assert gate.should_run(1) is False
        gate.record_plain_events(_Event(0.0), _Event(20.0))
    assert gate.should_run(1)
    for _ in range(4):
        _cycle(gate, cycle_ms=29.0, verify_ms=26.0, tokens=1, scale=1.0)
    assert not gate.enabled


def test_a_finished_request_does_not_leak_its_verdict_into_a_reused_uid():
    gate = AdaptiveGate(min_cycles=4, eval_interval=4, warmup_cycles=0, margin=1.15, probe_steps=0)
    assert gate.should_run(0)
    for _ in range(4):
        _cycle(gate, cycle_ms=40.0, verify_ms=20.0, tokens=1, scale=1.0)
    assert not gate.enabled
    gate.finish_request()
    assert gate.should_run(0)  # the next request, same id


def test_probing_thins_out_once_the_baseline_has_samples():
    gate = AdaptiveGate(probe_steps=1, probe_after=0, probe_every=4)
    probed = []
    for uid in range(12):
        gate.should_run(uid)
        probed.append(gate.probing)
        if gate.probing:
            gate.record_plain_events(_Event(0.0), _Event(20.0))
        gate.finish_request()
    assert probed[:4] == [True] * 4
    assert sum(probed[4:]) == 2  # every 4th request after that


def test_window_throughput_not_the_median_cycle_decides():
    # most cycles keep 1 token (36 ms), every third keeps 7: 108 ms for 9 tokens = 12 ms/token,
    # faster than a 20 ms plain step, though the median cycle (36 ms/token) is slower
    gate = AdaptiveGate(min_cycles=6, eval_interval=6, warmup_cycles=0, margin=1.15, probe_steps=1,
                        probe_after=0)
    assert gate.should_run(1) is False
    gate.record_plain_events(_Event(0.0), _Event(20.0))
    gate.should_run(1)
    for i in range(12):
        _cycle(gate, cycle_ms=36.0, verify_ms=26.0, tokens=7 if i % 3 == 2 else 1, scale=1.0)
    assert gate.enabled
