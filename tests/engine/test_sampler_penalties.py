"""OpenAI presence/frequency penalties in the Sampler: counted over generated tokens only."""

from __future__ import annotations

import pytest
import torch
from freetoken.core import Batch, Req, SamplingParams
from freetoken.engine import sample as sample_mod
from freetoken.engine.sample import PenaltyArgs, Sampler, apply_penalties
from freetoken.scheduler.prefill import ChunkedReq

VOCAB = 16


def make_req(table_idx: int, prompt: list[int], params: SamplingParams, cls=Req) -> Req:
    return cls(
        input_ids=torch.tensor(prompt, dtype=torch.int32),
        table_idx=table_idx,
        cached_len=0,
        output_len=8,
        uid=table_idx,
        sampling_params=params,
        cache_handle=None,
    )


def decode_step(req: Req, token_pool: torch.Tensor, token: int) -> None:
    """What forward_batch + the scheduler's token_pool write do for one sampled token; the
    host-side input_ids is deliberately left behind, as under overlap scheduling."""
    token_pool[req.table_idx, req.device_len] = token
    req.complete_one()


@pytest.fixture
def cpu_sampler(monkeypatch):
    monkeypatch.setattr(
        sample_mod, "make_device_tensor", lambda data, dtype, device: torch.tensor(data, dtype=dtype)
    )
    return Sampler(torch.device("cpu"), VOCAB)


def test_apply_penalties_matches_openai_formula():
    token_pool = torch.zeros(3, 12, dtype=torch.int32)
    # row 0's prompt holds token 7 (must not count); its output is [3, 3, 5]
    token_pool[1, :6] = torch.tensor([7, 7, 7, 3, 3, 5])
    # row 2's output is [7], followed by stale pool contents that must not count
    token_pool[2, :5] = torch.tensor([1, 2, 7, 9, 9])
    pen = PenaltyArgs(
        token_pool=token_pool,
        index=torch.tensor([[0, 2], [1, 2], [3, 2], [3, 1]]),
        weights=torch.tensor([[0.5, -1.0], [0.25, 2.0]]),
        max_len=3,
    )
    logits = torch.randn(3, VOCAB, dtype=torch.bfloat16)
    out = apply_penalties(logits, pen)

    expected = logits.float().clone()
    expected[0, 3] -= 0.5 * 2 + 0.25
    expected[0, 5] -= 0.5 * 1 + 0.25
    expected[2, 7] -= -1.0 * 1 + 2.0
    assert out.dtype == torch.float32
    torch.testing.assert_close(out, expected)
    assert logits.dtype == torch.bfloat16  # caller's buffer untouched


def test_prepare_skips_unpenalized_and_tokenless_rows(cpu_sampler):
    token_pool = torch.zeros(4, 32, dtype=torch.int32)
    plain = make_req(0, [1, 2, 3], SamplingParams())
    penalized = make_req(1, [4, 4, 4, 4], SamplingParams(frequency_penalty=1.0))
    chunk = make_req(2, [5, 6], SamplingParams(presence_penalty=1.0), cls=ChunkedReq)

    # final prefill chunk: nothing generated yet -> the no-penalty fast path
    args = cpu_sampler.prepare(Batch(reqs=[plain, penalized, chunk], phase="prefill"), token_pool)
    assert args.penalties is None and args.temperatures is None
    assert cpu_sampler.prepare(Batch(reqs=[plain], phase="decode"), None).penalties is None

    decode_step(plain, token_pool, 9)
    decode_step(penalized, token_pool, 9)
    decode_step(penalized, token_pool, 11)
    args = cpu_sampler.prepare(Batch(reqs=[plain, penalized], phase="decode"), token_pool)
    pen = args.penalties
    assert pen.index.tolist() == [[1], [1], [4], [2]]
    assert pen.max_len == 2

    out = apply_penalties(torch.zeros(2, VOCAB), pen)
    assert out[0].eq(0).all()
    assert out[1, 9] == -1.0 and out[1, 11] == -1.0 and out[1, 4] == 0.0


def test_greedy_rows_follow_penalized_argmax(cpu_sampler):
    token_pool = torch.zeros(2, 32, dtype=torch.int32)
    a = make_req(0, [1], SamplingParams(presence_penalty=2.0))
    b = make_req(1, [1], SamplingParams())
    for req in (a, b):
        decode_step(req, token_pool, 3)
    logits = torch.zeros(2, VOCAB)
    logits[:, 3] = 1.0
    logits[:, 4] = 0.5
    args = cpu_sampler.prepare(Batch(reqs=[a, b], phase="decode"), token_pool)
    assert cpu_sampler.sample(logits, args).tolist() == [4, 3]


@pytest.mark.parametrize("field", ["presence_penalty", "frequency_penalty"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), 2.001, -3.0])
def test_sampling_params_reject_invalid_penalty(field, value):
    with pytest.raises(ValueError, match=field):
        SamplingParams(**{field: value})


@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")
def test_mixed_batch_on_gpu():
    device = torch.device("cuda")
    sampler = Sampler(device, VOCAB)
    token_pool = torch.zeros(4, 64, dtype=torch.int32, device=device)
    sampled_pen = make_req(0, [1, 2], SamplingParams(temperature=1.0, frequency_penalty=2.0))
    greedy_pen = make_req(1, [1, 2], SamplingParams(presence_penalty=1.0))
    sampled = make_req(2, [1, 2], SamplingParams(temperature=1.0, top_k=2))
    greedy = make_req(3, [1, 2], SamplingParams())
    reqs = [sampled_pen, greedy_pen, sampled, greedy]
    for _ in range(40):
        for req in reqs:
            decode_step(req, token_pool, 5)

    logits = torch.full((4, VOCAB), -1e4, device=device)
    logits[:, 5] = 10.0
    logits[:, 6] = 9.5
    args = sampler.prepare(Batch(reqs=reqs, phase="decode"), token_pool)
    torch.cuda.synchronize()
    for _ in range(20):
        tokens = sampler.sample(logits, args).tolist()
        # 40 repeats * 2.0 pushes token 5 to -70: the sampled row can only draw token 6
        assert tokens[0] == 6
        assert tokens[1] == 6  # 10 - 1 < 9.5
        assert tokens[2] in (5, 6)
        assert tokens[3] == 5
