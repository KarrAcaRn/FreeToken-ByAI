"""Stop strings: the scheduler matches against the same incrementally decoded text the
detokenizer streams, so a stop the scheduler reports is the stop the frontend trims.

A byte-level tokenizer stands in for byte-level BPE: a CJK character or emoji spans several
tokens, which a decode window sized in tokens per stop *character* cannot cover.
"""
from __future__ import annotations

from types import SimpleNamespace

import torch

from freetoken.message import DetokenizeMsg
from freetoken.scheduler.scheduler import Scheduler
from freetoken.tokenizer.detokenize import DetokenizeManager

EOS = 256


class ByteTokenizer:
    eos_token_id = EOS

    def decode(self, ids):
        return bytes(i for i in ids if i < 256).decode("utf-8", errors="replace")

    def batch_decode(self, batch):
        return [self.decode(ids) for ids in batch]


PROMPT = list(b"Q:")


def _ids(text: str) -> list[int]:
    return list(text.encode("utf-8"))


def _step_matches(output: list[int], stop_strs: list[str]) -> list[str | None]:
    """The scheduler's per-step stop check over ``output`` delivered one token at a time."""
    sched = Scheduler.__new__(Scheduler)
    sched.tokenizer = ByteTokenizer()
    sched.eos_token_ids = {EOS}
    budget = len(output) + 8
    req = SimpleNamespace(
        sampling_params=SimpleNamespace(stop_strs=stop_strs),
        max_device_len=len(PROMPT) + budget,
        output_len=budget,
        can_decode=True,
        stop_decode_status=None,
        input_ids=torch.tensor(PROMPT, dtype=torch.int32),
    )
    matches = []
    for tok in output:
        req.input_ids = torch.cat([req.input_ids, torch.tensor([tok], dtype=torch.int32)])
        matches.append(Scheduler._match_stop_str(sched, req))
    return matches


def test_a_multi_token_stop_string_matches_on_its_last_token():
    # "停止" is 6 byte tokens; the old window decoded max_chars + 1 = 3 tokens and never
    # saw the whole stop.
    output = _ids("好的停止了")
    matches = _step_matches(output, ["停止"])
    first = next(i for i, m in enumerate(matches) if m)
    assert matches[first] == "停止"
    assert first == len(_ids("好的停止")) - 1


def test_a_stop_is_not_matched_inside_an_incomplete_character():
    # The stop is the replacement character the half-decoded emoji renders as; the frontend
    # never shows that text, so the scheduler must not match it either.
    matches = _step_matches(_ids("a🙂b"), ["�"])
    assert not any(matches)


def test_the_stop_spans_steps_after_the_text_buffer_is_trimmed():
    output = _ids("x" * 50 + " END")
    matches = _step_matches(output, ["END"])
    assert matches[-1] == "END" and not any(matches[:-1])


def test_the_detokenizer_trims_the_stop_the_scheduler_matched():
    output = _ids("好的停止了")
    matches = _step_matches(output, ["停止"])
    stop_at = next(i for i, m in enumerate(matches) if m)
    detok = DetokenizeManager(ByteTokenizer(), frozenset({EOS}))
    text = ""
    for i, tok in enumerate(output[: stop_at + 1]):
        done = i == stop_at
        text += detok.detokenize(
            [
                DetokenizeMsg(
                    uid=1,
                    next_token=tok,
                    finished=done,
                    finish_reason="stop" if done else None,
                    matched_stop=matches[i],
                    stop_strs=["停止"],
                )
            ]
        )[0]
    assert text == "好的"


def test_detokenize_advances_a_request_seen_twice_in_one_batch():
    detok = DetokenizeManager(ByteTokenizer(), frozenset({EOS}))
    msgs = [
        DetokenizeMsg(uid=7, next_token=t, finished=False) for t in _ids("ab")
    ]
    assert "".join(detok.detokenize(msgs)) == "ab"
