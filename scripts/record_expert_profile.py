"""Record a disk-tier expert profile (``--expert-profile``) from your own prompts.

Runs the model with the disk tier, counts which experts every MoE layer routes to while
decoding the prompts, and writes ``{"layers": [[expert ids, hottest first], ...]}``. Use
prompts like the ones you will serve; the profile decides which experts the
``--expert-ram-experts`` RAM prefix holds.

    python scripts/record_expert_profile.py MODEL OUT.json --prompts prompts.txt \\
        [--max-tokens 160] [--engine '{"expert_ram_experts": 128, ...}']

``prompts.txt`` holds one prompt per line. The engine defaults match the Qwen3.8-Flash-Next
disk-tier recipe in fork/next-speed.md; ``--engine`` overrides any SchedulerConfig field.
"""

from __future__ import annotations

import argparse
import json

import torch

from freetoken.core import SamplingParams
from freetoken.llm import LLM
from freetoken.mm.config import ENCODER_KINDS, MultimodalConfig


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("out")
    ap.add_argument("--prompts", required=True)
    ap.add_argument("--max-tokens", type=int, default=160)
    ap.add_argument("--engine", default="{}")
    args = ap.parse_args()

    kwargs = dict(
        max_running_req=1, kv_quant="fp8", moe_disk_tier="on", expert_ram_experts=128,
        ple_backend="disk", moe_prefill_overlap=False, cuda_graph_max_bs=0,
        mm=MultimodalConfig(disabled_encoders=frozenset(ENCODER_KINDS)),
    )
    kwargs.update(json.loads(args.engine))
    kwargs.pop("expert_profile", None)  # counts must be in the checkpoint's own expert ids
    kwargs["moe_collect_stats"] = True
    llm = LLM(args.model, **kwargs)
    cache = llm.engine.moe_offload_cache
    cache.decode_freq.zero_()
    with open(args.prompts, encoding="utf-8") as f:
        prompts = [line.strip() for line in f if line.strip()]
    for text in prompts:
        p = llm.tokenizer.apply_chat_template([{"role": "user", "content": text}], tokenize=False,
                                              add_generation_prompt=True)
        llm.generate([p], SamplingParams(max_tokens=args.max_tokens, temperature=0.0))
    freq = cache.decode_freq.cpu()
    order = [torch.argsort(freq[layer], descending=True, stable=True).tolist() for layer in range(freq.shape[0])]
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"layers": order}, f)
    top = torch.sort(freq.float(), dim=1, descending=True).values.cumsum(1) / freq.sum(1, keepdim=True).clamp(min=1)
    ram = kwargs["expert_ram_experts"]
    print(f"{len(prompts)} prompts; the top {ram} experts per layer take {top[:, ram - 1].mean().item():.1%} "
          f"of the decode routing")


if __name__ == "__main__":
    main()
