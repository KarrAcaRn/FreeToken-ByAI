from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, List

import torch
from freetoken.utils import is_sm90_supported, nvtx_annotate

if TYPE_CHECKING:
    from freetoken.core import Batch


@dataclass
class PenaltyArgs:
    # Read on the engine stream at sample time, not from Req.input_ids at prepare time: under
    # overlap scheduling the previous step's token is in token_pool but not yet on the host.
    token_pool: torch.Tensor  # [tables, max_seq_len] int32
    index: torch.Tensor  # int64 [4, P]: batch row, table_idx, prompt_len, generated count
    weights: torch.Tensor  # float32 [2, P]: frequency, presence
    max_len: int  # max generated count over the P rows


@dataclass
class BatchSamplingArgs:
    temperatures: torch.Tensor | None
    top_k: torch.Tensor | None = None
    top_p: torch.Tensor | None = None
    greedy_mask: torch.Tensor | None = None
    penalties: PenaltyArgs | None = None
    logprob_rows: torch.Tensor | None = None
    max_top_logprobs: int = 0


def make_device_tensor(data: List, dtype: torch.dtype, device: torch.device) -> torch.Tensor:
    return torch.tensor(data, dtype=dtype, pin_memory=True).to(device, non_blocking=True)


def apply_penalties(logits: torch.Tensor, pen: PenaltyArgs) -> torch.Tensor:
    """Return an fp32 copy of ``logits`` with OpenAI presence/frequency penalties applied."""
    rows, table_idx, starts, lens = pen.index
    frequency, presence = pen.weights
    vocab = logits.shape[-1]
    offs = torch.arange(pen.max_len, device=logits.device)
    valid = offs < lens[:, None]
    pos = torch.where(valid, starts[:, None] + offs, starts[:, None])
    tokens = pen.token_pool[table_idx[:, None], pos].long().clamp_(0, vocab - 1)
    counts = torch.zeros(rows.numel(), vocab, dtype=torch.float32, device=logits.device)
    counts.scatter_add_(1, tokens, valid.to(torch.float32))
    penalty = counts * frequency[:, None] + (counts > 0).to(torch.float32) * presence[:, None]
    out = logits.to(torch.float32, copy=True)
    out.index_add_(0, rows, penalty, alpha=-1.0)
    return out


def sample_impl(
    logits: torch.Tensor,
    temperatures: torch.Tensor,
    top_k: torch.Tensor | int | None,
    top_p: torch.Tensor | float | None,
) -> torch.Tensor:
    from freetoken.kernel.backend import is_flashinfer_installed

    if is_flashinfer_installed():
        import flashinfer.sampling as sampling
    else:
        import freetoken.kernel.triton.sampling as sampling

    probs = sampling.softmax(logits, temperatures, enable_pdl=is_sm90_supported())
    if top_k is None and top_p is None:
        return sampling.sampling_from_probs(probs)

    if top_p is None:
        assert top_k is not None
        return sampling.top_k_sampling_from_probs(probs, top_k)

    if top_k is None:
        assert top_p is not None
        return sampling.top_p_sampling_from_probs(probs, top_p)

    assert top_k is not None and top_p is not None
    return sampling.top_k_top_p_sampling_from_probs(probs, top_k, top_p)


@dataclass
class Sampler:
    device: torch.device
    vocab_size: int

    def prepare(self, batch: Batch, token_pool: torch.Tensor | None = None) -> BatchSamplingArgs:
        params = [r.sampling_params for r in batch.reqs]
        penalties = self._prepare_penalties(batch, token_pool)
        is_greedy = [p.is_greedy for p in params]
        want_logprobs = [p.logprobs for p in params]
        logprob_rows = (
            make_device_tensor(want_logprobs, torch.bool, self.device)
            if any(want_logprobs)
            else None
        )
        max_top_logprobs = min(
            max((p.top_logprobs for p in params if p.logprobs), default=0), self.vocab_size
        )
        if all(is_greedy):
            return BatchSamplingArgs(
                temperatures=None,
                penalties=penalties,
                logprob_rows=logprob_rows,
                max_top_logprobs=max_top_logprobs,
            )

        MIN_P = MIN_T = 1e-6
        # Greedy outputs are selected explicitly in sample(); use neutral sampling
        # parameters for those rows instead of approximating argmax at low temperature.
        ts = [1.0 if g else max(p.temperature, MIN_T) for p, g in zip(params, is_greedy)]
        top_ks = [
            p.top_k if not g and p.top_k >= 1 else self.vocab_size
            for p, g in zip(params, is_greedy)
        ]
        top_ps = [
            1.0 if g else min(max(p.top_p, MIN_P), 1.0)
            for p, g in zip(params, is_greedy)
        ]
        temperatures = make_device_tensor(ts, torch.float32, self.device)
        top_k, top_p = None, None
        if any(k != self.vocab_size for k in top_ks):
            top_k = make_device_tensor(top_ks, torch.int32, self.device)
        if any(p < 1.0 for p in top_ps):
            top_p = make_device_tensor(top_ps, torch.float32, self.device)
        greedy_mask = (
            make_device_tensor(is_greedy, torch.bool, self.device) if any(is_greedy) else None
        )
        return BatchSamplingArgs(
            temperatures,
            top_k=top_k,
            top_p=top_p,
            greedy_mask=greedy_mask,
            penalties=penalties,
            logprob_rows=logprob_rows,
            max_top_logprobs=max_top_logprobs,
        )

    def _prepare_penalties(
        self, batch: Batch, token_pool: torch.Tensor | None
    ) -> PenaltyArgs | None:
        if token_pool is None:
            return None
        index: List[List[int]] = [[], [], [], []]
        weights: List[List[float]] = [[], []]
        for i, req in enumerate(batch.reqs):
            p = req.sampling_params
            # Called before complete_one(): device_len - prompt_len is the number of tokens
            # this request has generated so far (0 on its final prefill chunk).
            generated = req.device_len - req.prompt_len
            if not p.has_penalty or generated <= 0:
                continue
            for column, value in zip(index, (i, req.table_idx, req.prompt_len, generated)):
                column.append(value)
            weights[0].append(p.frequency_penalty)
            weights[1].append(p.presence_penalty)
        if not index[0]:
            return None
        return PenaltyArgs(
            token_pool=token_pool,
            index=make_device_tensor(index, torch.int64, self.device),
            weights=make_device_tensor(weights, torch.float32, self.device),
            max_len=max(index[3]),
        )

    @nvtx_annotate("Sampler")
    def sample(self, logits: torch.Tensor, args: BatchSamplingArgs) -> torch.Tensor:
        with torch.cuda.nvtx.range("Sampler"):
            if args.penalties is not None:
                logits = apply_penalties(logits, args.penalties)
            if args.temperatures is None:  # greedy sampling
                return torch.argmax(logits, dim=-1)
            tokens = sample_impl(logits.float(), args.temperatures, args.top_k, args.top_p)
            if args.greedy_mask is not None:
                # Mixed batches still run probability sampling for all rows, but
                # greedy rows must follow argmax's deterministic tie-breaking.
                greedy_tokens = torch.argmax(logits, dim=-1).to(tokens.dtype)
                tokens = torch.where(args.greedy_mask, greedy_tokens, tokens)
            return tokens

    def compute_logprobs(
        self,
        logits: torch.Tensor,
        sampled_tokens: torch.Tensor,
        args: BatchSamplingArgs,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor] | None:
        if args.logprob_rows is None:
            return None

        requested_rows = torch.nonzero(args.logprob_rows, as_tuple=False).flatten()
        if requested_rows.numel() == 0:
            return None

        request_logits = logits.index_select(0, requested_rows).float()
        # Reported values are raw model logprobs (pre-temperature log_softmax over logits).
        request_logprobs = torch.log_softmax(request_logits, dim=-1)

        request_tokens = sampled_tokens.to(dtype=torch.long, device=logits.device).index_select(
            0, requested_rows
        )
        request_row_idx = torch.arange(requested_rows.numel(), device=logits.device)
        request_chosen_logprobs = request_logprobs[request_row_idx, request_tokens]

        chosen_logprobs = torch.full(
            (logits.shape[0],), float("nan"), dtype=torch.float32, device=logits.device
        )
        chosen_logprobs.index_copy_(0, requested_rows, request_chosen_logprobs)

        if args.max_top_logprobs > 0:
            request_top_logprobs, request_top_ids = torch.topk(
                request_logprobs, k=args.max_top_logprobs, dim=-1
            )
            top_ids = torch.full(
                (logits.shape[0], args.max_top_logprobs),
                -1,
                dtype=torch.int32,
                device=logits.device,
            )
            top_logprobs = torch.full(
                (logits.shape[0], args.max_top_logprobs),
                float("-inf"),
                dtype=torch.float32,
                device=logits.device,
            )
            top_ids[requested_rows] = request_top_ids.to(torch.int32)
            top_logprobs[requested_rows] = request_top_logprobs
        else:
            top_ids = torch.empty((logits.shape[0], 0), dtype=torch.int32, device=logits.device)
            top_logprobs = torch.empty((logits.shape[0], 0), dtype=torch.float32, device=logits.device)

        return (
            chosen_logprobs.to("cpu", non_blocking=True),
            top_ids.to("cpu", non_blocking=True),
            top_logprobs.to("cpu", non_blocking=True),
        )
