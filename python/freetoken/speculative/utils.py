"""Algorithm-agnostic helpers shared by all speculative decoding workers."""

from __future__ import annotations

import statistics
from collections import deque
from typing import Any, NamedTuple, TYPE_CHECKING

import torch

if TYPE_CHECKING:
    from freetoken.core import Batch
    from freetoken.engine.sample import BatchSamplingArgs


# ---------------------------------------------------------------------------
# Output selection (greedy exact-match verify)
# ---------------------------------------------------------------------------

def select_output_tokens(
    base_token: torch.Tensor,
    draft_candidates: torch.Tensor,
    verify_tokens: torch.Tensor,
) -> tuple[torch.Tensor, int]:
    """Greedy verify: accept while draft == target argmax, bonus = first mismatch."""
    if verify_tokens.numel() < draft_candidates.numel() + 1:
        raise ValueError("verify_tokens must contain one prediction per draft plus one bonus")
    accepted = contiguous_accept_len(draft_candidates, verify_tokens)
    bonus = verify_tokens[accepted : accepted + 1]
    return torch.cat([
        base_token[:1],
        draft_candidates[:accepted].to(base_token.dtype),
        bonus.to(base_token.dtype),
    ]), accepted


def contiguous_accept_len(
    draft_candidates: torch.Tensor,
    verify_tokens: torch.Tensor,
) -> int:
    matches = draft_candidates == verify_tokens[: draft_candidates.numel()].to(draft_candidates.dtype)
    if matches.numel() == 0:
        return 0
    mismatches = torch.nonzero(~matches, as_tuple=False)
    if mismatches.numel() == 0:
        return matches.numel()
    return int(mismatches[0, 0].item())


def select_streaming_output_tokens(
    base_token: torch.Tensor,
    draft_candidates: torch.Tensor,
    verify_tokens: torch.Tensor,
) -> tuple[torch.Tensor, int, bool]:
    """Streaming greedy verify with early-stop. Returns (output, accepted, done)."""
    accepted = 0
    checked = min(draft_candidates.numel(), verify_tokens.numel())
    for i in range(checked):
        if int(draft_candidates[i].item()) != int(verify_tokens[i].item()):
            bonus = verify_tokens[i : i + 1]
            return torch.cat([
                base_token[:1],
                draft_candidates[:accepted].to(base_token.dtype),
                bonus.to(base_token.dtype),
            ]), accepted, True
        accepted += 1
    if verify_tokens.numel() > draft_candidates.numel():
        bonus = verify_tokens[accepted : accepted + 1]
        return torch.cat([
            base_token[:1],
            draft_candidates[:accepted].to(base_token.dtype),
            bonus.to(base_token.dtype),
        ]), accepted, True
    return torch.empty((0,), dtype=base_token.dtype, device=base_token.device), accepted, False


# ---------------------------------------------------------------------------
# Speculative (rejection) sampling for non-greedy decoding
# ---------------------------------------------------------------------------

def sampling_probs(logits: torch.Tensor, args: BatchSamplingArgs) -> torch.Tensor:
    """Temperature + top_k/top_p filtered probability distribution."""
    temperature = float(args.temperatures[0].item())
    top_k = int(args.top_k[0].item()) if args.top_k is not None else 0
    top_p = float(args.top_p[0].item()) if args.top_p is not None else 1.0

    scores = logits.float() / max(temperature, 1e-6)
    vocab_size = scores.shape[-1]
    indices = None
    if 0 < top_k < vocab_size:
        scores, indices = torch.topk(scores, top_k, dim=-1)
    probs = torch.softmax(scores, dim=-1)
    if top_p < 1.0:
        sorted_probs, order = probs.sort(dim=-1, descending=True)
        keep = sorted_probs.cumsum(dim=-1) - sorted_probs < top_p
        sorted_probs = sorted_probs * keep
        probs = torch.zeros_like(probs).scatter(-1, order, sorted_probs)
        probs = probs / probs.sum(dim=-1, keepdim=True)
    if indices is not None:
        probs = torch.zeros_like(logits, dtype=probs.dtype).scatter(-1, indices, probs)
    return probs


def rejection_residual_sample(p_row: torch.Tensor, q_row: torch.Tensor) -> torch.Tensor:
    residual = (p_row - q_row).clamp_min(0)
    total = residual.sum()
    residual = torch.where(
        total > 0,
        residual / total.clamp_min(torch.finfo(residual.dtype).tiny),
        p_row,
    )
    return torch.multinomial(residual[None], 1)[0]


def rejection_step(
    p_row: torch.Tensor,
    q_row: torch.Tensor,
    draft_token: int,
    uniform: float,
) -> tuple[bool, torch.Tensor | None]:
    if (uniform * q_row[draft_token] < p_row[draft_token]).item():
        return True, None
    return False, rejection_residual_sample(p_row, q_row)


def rejection_sample_chain(
    base_token: torch.Tensor,
    draft_tokens: torch.Tensor,
    draft_probs: torch.Tensor,
    target_probs: torch.Tensor,
    *,
    uniform: torch.Tensor | None = None,
) -> tuple[torch.Tensor, int]:
    gamma = draft_tokens.numel()
    tokens64 = draft_tokens.to(torch.int64)
    p = target_probs[:gamma].gather(-1, tokens64[:, None])[:, 0]
    q = draft_probs.gather(-1, tokens64[:, None])[:, 0]
    u = (
        torch.rand(gamma, dtype=torch.float32, device=p.device)
        if uniform is None
        else uniform.to(device=p.device, dtype=torch.float32)
    )
    accepted = int((u * q < p).to(torch.int32).cumprod(0).sum().item())
    if accepted == gamma:
        bonus = torch.multinomial(target_probs[gamma : gamma + 1], 1)[0]
    else:
        bonus = rejection_residual_sample(target_probs[accepted], draft_probs[accepted])
    return torch.cat([
        base_token[:1],
        draft_tokens[:accepted].to(base_token.dtype),
        bonus.to(base_token.dtype),
    ]), accepted


def use_sampling_verify(args: BatchSamplingArgs, draft_probs: torch.Tensor | None) -> bool:
    return args.temperatures is not None and draft_probs is not None


def request_sampling_args(args: BatchSamplingArgs | None, row: int) -> BatchSamplingArgs | None:
    """One request's sampling args out of a batch's (temperatures None: it decodes greedily)."""
    if args is None:
        return None
    from freetoken.engine.sample import BatchSamplingArgs
    greedy_mask = getattr(args, "greedy_mask", None)
    if args.temperatures is None or (greedy_mask is not None and bool(greedy_mask[row])):
        return BatchSamplingArgs(temperatures=None)
    pick = lambda t: t[row : row + 1] if isinstance(t, torch.Tensor) else t  # noqa: E731
    return BatchSamplingArgs(temperatures=pick(args.temperatures), top_k=pick(args.top_k), top_p=pick(args.top_p))


def repeat_sampling_args(args: BatchSamplingArgs, repeat: int) -> BatchSamplingArgs:
    if args.temperatures is None:
        return args
    from freetoken.engine.sample import BatchSamplingArgs
    return BatchSamplingArgs(
        temperatures=args.temperatures.repeat(repeat),
        top_k=args.top_k.repeat(repeat) if isinstance(args.top_k, torch.Tensor) else args.top_k,
        top_p=args.top_p.repeat(repeat) if isinstance(args.top_p, torch.Tensor) else args.top_p,
    )


# ---------------------------------------------------------------------------
# Linear (GDN) state snapshot / restore
# ---------------------------------------------------------------------------

def snapshot_linear_state_slot(
    pool: Any, slot: int, out: tuple[torch.Tensor, torch.Tensor] | None = None
) -> tuple[torch.Tensor, torch.Tensor]:
    """Copy one GDN slot's (conv, recurrent) state, into ``out`` when given (no allocation)."""
    if out is None:
        return pool.conv_states[:, slot].clone(), pool.recurrent_states[:, slot].clone()
    out[0].copy_(pool.conv_states[:, slot])
    out[1].copy_(pool.recurrent_states[:, slot])
    return out


def restore_linear_state_slot(
    pool: Any, slot: int, snapshot: tuple[torch.Tensor, torch.Tensor]
) -> None:
    conv_state, recurrent_state = snapshot
    pool.conv_states[:, slot].copy_(conv_state)
    pool.recurrent_states[:, slot].copy_(recurrent_state)


def restore_linear_state_for_commit(
    pool: Any,
    slot: int,
    pre_verify_snapshot: tuple[torch.Tensor, torch.Tensor],
    verify_snapshots: list[tuple[torch.Tensor, torch.Tensor]],
    commit_len: int,
) -> None:
    if commit_len <= 0:
        snapshot = pre_verify_snapshot
    elif commit_len <= len(verify_snapshots):
        snapshot = verify_snapshots[commit_len - 1]
    else:
        raise ValueError(f"commit_len={commit_len} exceeds verify snapshots={len(verify_snapshots)}")
    restore_linear_state_slot(pool, slot, snapshot)


def commit_graph_linear_state(
    gdn_layers: list,
    pool: Any,
    slot: torch.Tensor,
    cu_seqlens: torch.Tensor,
    graph_snapshots: tuple[torch.Tensor, torch.Tensor, torch.Tensor],
    commit_len: int,
) -> None:
    """Advance the live GDN slot over the first ``commit_len`` tokens of a graph verify, which
    left the slot untouched: copy the conv state after the last kept token and replay each
    layer's recurrence from the inputs the verify stored. ``slot`` is ``[1]`` int32 and
    ``cu_seqlens`` is ``[0, commit_len]`` int32, both on the device."""
    if commit_len <= 0:
        return
    conv_steps, mixed, ab = graph_snapshots
    if commit_len > conv_steps.shape[0]:
        raise ValueError(f"commit_len={commit_len} exceeds graph snapshots={conv_steps.shape[0]}")
    pool.conv_states.index_copy_(1, slot.long(), conv_steps[commit_len - 1].unsqueeze(1))
    for layer in gdn_layers:
        li = pool.local_index(layer.layer_id)
        layer.dflash_commit(pool, slot, cu_seqlens, mixed[li, :commit_len], ab[li, :, :commit_len])


# ---------------------------------------------------------------------------
# Verify state snapshot / restore (batch + req fields)
# ---------------------------------------------------------------------------

class VerifyState(NamedTuple):
    batch_phase: str
    batch_input_ids: torch.Tensor
    batch_positions: torch.Tensor
    batch_out_loc: torch.Tensor | None
    batch_padded_reqs: list
    batch_fla_metadata: Any
    batch_linear_table_idx: torch.Tensor | None
    reqs: tuple[tuple[int, int, int], ...]  # per request: (input_len, cached_len, device_len)


def snapshot_verify_state(batch: Batch) -> VerifyState:
    return VerifyState(
        batch_phase=batch.phase,
        batch_input_ids=batch.input_ids,
        batch_positions=batch.positions,
        batch_out_loc=batch.out_loc,
        batch_padded_reqs=batch.padded_reqs,
        batch_fla_metadata=batch.fla_metadata,
        batch_linear_table_idx=batch.linear_table_idx,
        reqs=tuple((r.input_ids.numel(), r.cached_len, r.device_len) for r in batch.reqs),
    )


def restore_verify_state(batch: Batch, state: VerifyState) -> None:
    for req, (input_len, cached_len, device_len) in zip(batch.reqs, state.reqs, strict=True):
        req.input_ids = req._ids_buf[:input_len]
        req.cached_len = cached_len
        req.device_len = device_len
    batch.phase = state.batch_phase
    batch.input_ids = state.batch_input_ids
    batch.positions = state.batch_positions
    batch.out_loc = state.batch_out_loc
    batch.padded_reqs = state.batch_padded_reqs
    batch.fla_metadata = state.batch_fla_metadata
    batch.linear_table_idx = state.batch_linear_table_idx


def clone_hidden_outputs(hidden_states: list[torch.Tensor]) -> list[torch.Tensor]:
    return [hidden.clone() for hidden in hidden_states]


# ---------------------------------------------------------------------------
# Adaptive gate (shared by all spec algorithms)
# ---------------------------------------------------------------------------

class AdaptiveGate:
    """Per-request measured fallback: disables spec decode when it measures
    slower than plain decode by more than ``margin``.

    The baseline is measured: ``probe_steps`` decode steps of a request, after its first
    ``probe_after``, run without speculation (``probing``) and the caller times them
    (``record_plain_events``); the recent ones form the baseline. Requests probe until
    there are a few samples, then every ``probe_every``-th one. (The very first steps
    after a prefill are skipped: an offloaded MoE runs them on a prefill-churned cache.) Until there is one, the cycle's own verify forward
    times ``baseline_scale`` (the caller's calibrated plain/verify ratio) stands in. A
    measured step matters where the calibration cannot see the cost: an offloaded MoE
    verify streams the experts of every drafted token."""

    def __init__(
        self,
        *,
        min_cycles: int = 12,
        eval_interval: int = 8,
        margin: float = 1.15,
        warmup_cycles: int = 4,
        window: int = 32,
        auto_disable_after: int = 3,
        reprobe_every: int = 8,
        probe_steps: int = 2,
        probe_after: int = 4,
        probe_every: int = 4,
    ):
        self.min_cycles = min_cycles
        self.eval_interval = eval_interval
        self.margin = margin
        self.warmup_cycles = warmup_cycles
        self.auto_disable_after = auto_disable_after
        self.reprobe_every = reprobe_every
        self._window: deque[tuple[float, float, int]] = deque(maxlen=window)
        self._pending_events: list = []
        self._uid: int | None = None
        self.enabled = True
        self._records = 0
        self._evaluated = False
        self._consecutive_disables = 0
        self._off_requests = 0
        self._req_cycle_ms = 0.0
        self._req_tokens = 0
        self._req_target_ms: list[float] = []
        self.probe_steps = probe_steps
        self.probe_after = probe_after
        self._req_steps = 0
        self.probe_every = probe_every
        self._requests = 0
        self._probe_request = True
        self.probing = False
        self._plain_ms: deque[float] = deque(maxlen=16)
        self._pending_plain: list = []

    def finish_request(self) -> None:
        """The current request finished: settle its verdict and start the next one fresh
        (request ids can repeat, e.g. across offline generate() calls)."""
        if self._uid is not None:
            self._finish_request()
            self.reset(None)

    def should_run(self, uid: int) -> bool:
        if self._uid is None:
            self._uid = uid
        elif uid != self._uid:
            self._finish_request()
            self.reset(uid)
        step = self._req_steps
        self._req_steps += 1
        self.probing = (
            self.enabled and self._probe_request
            and self.probe_after <= step < self.probe_after + self.probe_steps
        )
        return self.enabled and not self.probing

    def record_plain_events(self, start, end) -> None:
        """Time one plain decode step taken while ``probing`` (CUDA events, read lazily)."""
        self._pending_plain.append((start, end))

    def _baseline_ms(self, proxy_ms: list[float]) -> float:
        if self._pending_plain:
            self._pending_plain[-1][1].synchronize()
            self._plain_ms.extend(s.elapsed_time(e) for s, e in self._pending_plain)
            self._pending_plain = []
        samples = self._plain_ms or proxy_ms
        return statistics.median_low(sorted(samples))

    def _finish_request(self) -> None:
        self._drain_pending()
        if len(self._req_target_ms) < self.min_cycles:
            return
        overall = self._req_cycle_ms / max(self._req_tokens, 1)
        baseline = self._baseline_ms(self._req_target_ms)
        if overall > baseline * self.margin:
            self._consecutive_disables += 1
        else:
            self._consecutive_disables = 0

    def reset(self, uid: int | None = None) -> None:
        self._uid = uid
        self._window.clear()
        self._pending_events.clear()
        self._records = 0
        self._evaluated = False
        self._req_cycle_ms = 0.0
        self._req_tokens = 0
        self._req_target_ms = []
        self._req_steps = 0
        self._requests += 1
        self._probe_request = (
            len(self._plain_ms) + len(self._pending_plain) < 4 or self._requests % self.probe_every == 0
        )
        self.enabled = True
        if self._consecutive_disables >= self.auto_disable_after:
            self._off_requests += 1
            if self._off_requests % self.reprobe_every != 0:
                self.enabled = False

    def _record_ms(self, cycle_ms: float, target_ms: float, out_tokens: int) -> None:
        self._records += 1
        if self._records <= self.warmup_cycles:
            return
        self._req_cycle_ms += cycle_ms
        self._req_tokens += out_tokens
        self._req_target_ms.append(target_ms)
        self._window.append((cycle_ms, target_ms, out_tokens))

    def record(self, *, cycle_ms: float, target_ms: float, out_tokens: int) -> None:
        if not self.enabled or out_tokens <= 0:
            return
        self._record_ms(cycle_ms, target_ms, out_tokens)
        n = self._records - self.warmup_cycles
        if n >= self.min_cycles and n % self.eval_interval == 0:
            self._evaluate()

    def record_events(self, *, cycle, target, out_tokens: int, baseline_scale: float = 1.0) -> None:
        if not self.enabled or out_tokens <= 0:
            return
        self._pending_events.append((cycle, target, out_tokens, baseline_scale))
        n = self._records + len(self._pending_events) - self.warmup_cycles
        if n < self.min_cycles or n % self.eval_interval:
            return
        self._drain_pending()
        self._evaluate()

    def _drain_pending(self) -> None:
        if not self._pending_events:
            return
        self._pending_events[-1][0][1].synchronize()
        pending, self._pending_events = self._pending_events, []
        for (cycle_start, cycle_end), (target_start, target_end), tokens, scale in pending:
            self._record_ms(
                cycle_start.elapsed_time(cycle_end),
                target_start.elapsed_time(target_end) * scale,
                tokens,
            )

    def _evaluate(self) -> None:
        if not self._window:
            return
        self._evaluated = True
        tokens = sum(t for _, _, t in self._window)
        if not tokens:
            return
        # throughput over the window: a median of per-cycle ratios overstates the cost when
        # acceptance swings (many 1-token cycles, a few long ones)
        cycle_ms_per_token = sum(c for c, _, _ in self._window) / tokens
        baseline_ms = self._baseline_ms([t for _, t, _ in self._window])
        if cycle_ms_per_token > baseline_ms * self.margin:
            self.enabled = False
            from freetoken.utils import init_logger
            logger = init_logger(__name__)
            logger.warning_rank0(
                f"[SPEC_ADAPTIVE] disabling spec decode for this request: "
                f"cycle {cycle_ms_per_token:.3f} ms/token > "
                f"baseline proxy {baseline_ms * self.margin:.3f} ms/token "
                f"(plain decode estimate {baseline_ms:.3f} ms, margin {self.margin})"
            )
