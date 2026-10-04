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
