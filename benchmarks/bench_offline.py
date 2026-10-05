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


def _timed(llm: LLM, prompts, max_tokens: int) -> float:
    sp = SamplingParams(temperature=0.0, ignore_eos=True, max_tokens=max_tokens)
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
