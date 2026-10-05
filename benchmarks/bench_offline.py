"""In-process prefill / decode throughput of one model, without the HTTP stack.

    python benchmarks/bench_offline.py <model> [--prefill 4096] [--decode 256] [--bs 1,4]
        [--engine '{"max_running_req": 4}'] [--profile out.json]

Prefill: fresh random-token prompts (no prefix-cache hit), max_tokens=1, median of runs.
Decode: tokens/s of one request (bs=1) and aggregate tokens/s for larger batches, measured
as the difference between a long and a 1-token generation of the same prompts.
"""

from __future__ import annotations

import argparse
import json
import statistics
import time

import torch

from freetoken.core import SamplingParams
from freetoken.llm import LLM


def _prompts(rng: torch.Generator, n: int, length: int, vocab: int) -> list[list[int]]:
    # Low ids are ordinary BPE tokens in every Qwen/Llama vocab; specials live at the top.
    return [torch.randint(1000, min(vocab, 100000), (length,), generator=rng).tolist() for _ in range(n)]


_NATURAL = [
    "Write a Python class implementing an LRU cache with get/put in O(1), with docstrings and a short usage example.",
    "Solve step by step: a train leaves at 9:40 at 84 km/h, a second one at 10:05 at 102 km/h on the same track. When does the second catch up?",
    "Explain how a transformer language model generates text, for a curious high-school student, in about 400 words.",
    "Write a bash script that finds the 10 largest files under a directory, prints their sizes human-readable and handles spaces in names.",
]


def _natural(llm: LLM, n: int) -> list[str]:
    """Chat-templated real prompts: speculative decoding needs text a draft can predict."""
    tok = llm.tokenizer
    return [
        tok.apply_chat_template([{"role": "user", "content": _NATURAL[i % len(_NATURAL)]}],
                                tokenize=False, add_generation_prompt=True, enable_thinking=False)
        for i in range(n)
    ]


def _timed(llm: LLM, prompts, max_tokens: int, ignore_eos: bool = True) -> float:
    sp = SamplingParams(temperature=0.0, ignore_eos=ignore_eos, max_tokens=max_tokens)
    torch.cuda.synchronize()
    t = time.perf_counter()
    llm.generate(prompts, sp)
    torch.cuda.synchronize()
    return time.perf_counter() - t


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("--prefill", type=int, default=4096)
    ap.add_argument("--decode", type=int, default=256)
    ap.add_argument("--decode-prompt", type=int, default=512)
    ap.add_argument("--bs", default="1")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--natural", action="store_true",
                    help="decode on chat prompts (stops at EOS) instead of random tokens; per-prompt tok/s")
    ap.add_argument("--text-only", action="store_true", help="--text-model-only")
    ap.add_argument("--engine", default="{}", help="JSON kwargs for SchedulerConfig")
    ap.add_argument("--profile", default=None, help="write a torch profiler trace of decode steps")
    ap.add_argument("--profile-prefill", default=None, help="write a torch profiler trace of one prefill")
    args = ap.parse_args()

    kwargs = {"max_running_req": max(int(b) for b in args.bs.split(","))}
    kwargs.update(json.loads(args.engine))
    if args.text_only:
        from freetoken.mm.config import ENCODER_KINDS, MultimodalConfig

        kwargs["mm"] = MultimodalConfig(disabled_encoders=frozenset(ENCODER_KINDS))
    llm = LLM(args.model, **kwargs)
    vocab = llm.tokenizer.vocab_size
    rng = torch.Generator().manual_seed(0)
    out: dict = {"model": args.model, "engine": {k: v for k, v in kwargs.items() if k != "mm"}}

    _timed(llm, _prompts(rng, 1, 256, vocab), 8)  # warm-up

    if args.prefill:
        times = [_timed(llm, _prompts(rng, 1, args.prefill, vocab), 1) for _ in range(args.runs + 1)][1:]
        out["prefill_tok_s"] = round(args.prefill / statistics.median(times))
        if args.profile_prefill:
            from torch.profiler import ProfilerActivity, profile

            p = _prompts(rng, 1, args.prefill, vocab)
            with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
                _timed(llm, p, 1)
            prof.export_chrome_trace(args.profile_prefill)
            print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=40))

    if args.natural:
        rates = []
        for p in _natural(llm, len(_NATURAL)):
            t1 = _timed(llm, [p], 1)
            sp = SamplingParams(temperature=0.0, max_tokens=args.decode + 1)
            torch.cuda.synchronize()
            t = time.perf_counter()
            n = len(llm.generate([p], sp)[0]["token_ids"])
            torch.cuda.synchronize()
            rates.append((n - 1) / (time.perf_counter() - t - t1))
        out["natural_decode_tok_s"] = [round(r, 1) for r in rates]
        out["natural_decode_mean"] = round(statistics.mean(rates), 1)
        print("RESULT " + json.dumps(out))
        return

    for bs in (int(b) for b in args.bs.split(",")):
        res = []
        for _ in range(args.runs):
            p = _prompts(rng, bs, args.decode_prompt, vocab)
            t1 = _timed(llm, p, 1)
            p = _prompts(rng, bs, args.decode_prompt, vocab)
            tn = _timed(llm, p, args.decode + 1)
            res.append(bs * args.decode / (tn - t1))
        out[f"decode_bs{bs}_tok_s"] = round(statistics.median(res), 1)

    if args.profile:
        from torch.profiler import ProfilerActivity, profile

        p = _prompts(rng, 1, args.decode_prompt, vocab)
        with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
            _timed(llm, p, 33)
        prof.export_chrome_trace(args.profile)
        print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=40))

    print("RESULT " + json.dumps(out))


if __name__ == "__main__":
    main()
