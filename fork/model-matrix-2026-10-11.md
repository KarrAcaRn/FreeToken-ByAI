# Model matrix 2026-10-11

Every model in the local HF cache, measured on `next` and on `next-speed`, the fastest
branch. Use these numbers as the reference point for later speed work.

## Setup

- **Hardware:** RTX 4090 (24 GB), 88 GiB RAM.
- **Software:** torch 2.14.1, triton 3.8.
- **Branches:** `next` ~5c9105c..6b9e5c2a; `next-speed` d13df048.
- **Engine:** in-process `LLM`, fp8 KV (`kv_quant fp8`), image/audio encoders off, greedy.
- **Prefill:** a ~4.2k-token fresh prompt, median of 3 runs.
- **Decode bs1:** `max_running_req 1`, two prompts (code + prose), 256–512 tokens each.
- **5 parallel:** `max_running_req 5`, 5 different prompts × 256 tokens (`ignore_eos`), 2 rounds
  after a warm-up. The value is total tok/s across all 5 and the per-stream rate.
- **`next-speed` online fp8:** bf16 models run with online fp8 (`--online-quant fp8` = `quant_backend
  linear.none=fp8`). It is the `ft serve` default on `next-speed` since 0c84dccf. GGUF and
  NVFP4/FP8 checkpoints keep their own weights; only their remaining bf16 linears become fp8.
- **Raw data:**
  - `next`: `~/.cache/ft-scratch/models1011/results.jsonl`
  - `next-speed`: `~/.cache/ft-scratch/speed1011/results.jsonl` (`f-*` = final single runs,
    `par` = 5 parallel)
  - Scripts `bench.py`, `bench_par.py`, `bench_spec.py`, `run.sh` live next to the data.

## Results

| Model | Decode bs1 tok/s (`next` → `next-speed`) | Prefill tok/s (`next-speed`) | KV tokens (`next-speed`) | 5 parallel: total / per stream (`next-speed`) |
|---|---|---|---|---|
| Qwen3-0.6B bf16 | 494 → 592 | 73,500 | 345k | 2794 / 559 |
| Qwen3-0.6B GGUF Q8_0 | 655 → 646 | 70,800 | 352k | 1643 / 329 |
| Llama-3.2-1B bf16 | 314 → 450 | 54,200 | 1.1M | 2206 / 441 |
| Llama-3.2-1B GGUF Q4_0 | 726 → 712 | 58,400 | 1.2M | 1578 / 316 |
| Qwen2.5-1.5B bf16 | 246 → 344 | 41,200 | 1.3M | 1728 / 346 |
| Qwen2.5-1.5B GGUF Q4_K_M | 499 → 493 | 41,100 | 1.4M | 1159 / 232 |
| Gemma-4-E2B bf16 | 154 → 214 | 24,800 | 3.1M | 1016 / 203 |
| Gemma-4-E2B GGUF QAT | 310 → 307 | 25,500 | 4.1M | 739 / 148 |
| Gemma-4-E4B bf16 | 84 → 122 | 14,600 | 773k | 618 / 124 |
| Gemma-4-E4B GGUF QAT | 195 → 194 | 14,500 | 1.3M | 465 / 93 |
| Mistral-7B bf16 | 61 → 114 | 9,700 | 205k | 560 / 112 |
| Mistral-7B GGUF Q4_K_M | 172 → 176 | 10,100 | 253k | 440 / 88 |
| Qwen3-VL-8B bf16 | 57 → 105 | 9,900 | 159k | 519 / 104 |
| Gemma-4-12B GGUF QAT | 102 → 106 | 5,800 | 321k | 237 / 47 |
| gpt-oss-20b | 182 → 228 | 15,800 | 553k | 520 / 104 |
| Muse-Glimmer-30B NVFP4 | 49 → 54 | 3,000 | 259k | 230 / 46 |
| Gemma-4-26B-A4B NVFP4 | 119 → 153 | 13,200 | 126k | 507 / 102 |
| Qwen3-30B-A3B GGUF Q4_K_M | 226 → 230 | 8,500 | 40k | 452 / 90 |
| Qwen3.6-35B-A3B NVFP4 | 131 → 203 | 15,900 | 172k | 500 / 100 |
| ↳ + DFlash (draft fp8) | code 236 → 348, prose ~187 | | 166k | 387 / 77 |
| Qwen3.6-35B-A3B FP8 | 86 → 94 | 5,400 | 171k | ~100 / 20 (expert thrash) |
| Qwen3.6-35B-A3B GGUF Q4_K_M | 149 → 152 | 8,500 | 176k | 307 / 61 |
| Qwen3.6-35B-A3B GGUF IQ3_S | 192 → 196 | 9,300 | 598k | 434 / 87 |
| Qwen3.8-27B NVFP4 | 45 → 48 | 3,400 | 99k | 201 / 40 (lean config, only 21k KV) |
| ↳ + DFlash | code 150–161 → 188–210, prose 124 | | 32k | does not fit (1.5 GiB short) |
| Qwen3.8-Flash-Next NVFP4 | 21 → 28.5 | 1,600 | 101k | 23 / 4.6 |
| GLM-4.5-Air NVFP4 | did not load → 6.5 | 1,760 | 12k | 4 / 0.8 |

### Notes

- **Online fp8 on bf16 models:** decode is +20–85% and KV up to 2× larger, because the
  weights are half the size. Prefill is equal or slightly slower (the fp8 prefill GEMM sits
  2–13% below bf16 cuBLAS). Outputs change slightly.
- **GGUF:** `next` and `next-speed` are about the same speed. For 5 parallel streams GGUF
  scales worse than bf16 + fp8, because the GGUF batch kernels are weaker.
- **Offloaded MoE experts:** with 5 parallel streams, Qwen3.6 FP8, Flash-Next and GLM need
  more distinct experts than fit in VRAM. Total throughput barely rises or even falls (PCIe
  miss path).
- **Qwen3.8-27B 5-parallel lean config:** `linear_state_cache_ratio 1.0`,
  `max_extend_tokens 4096`. 27B single runs use `--embed-device cpu`.
- **Flash-Next:** `kv_reserve_share 0` gives 29.6 tok/s with 8.4k KV. The best older value
  is 42 tok/s with all experts in RAM (2026-10-07, see `next-speed.md`); that recipe was
  not repeated here.
- **GLM-4.5-Air:** bound by PCIe expert misses, only 975 of 5888 experts fit in VRAM.

### Fixes made while measuring

- **GLM-4.5-Air loads** (5c9105c): the bf16 dense MLP and shared-expert projections are now
  read correctly.
- **Dense GGUF** for `llama`, `qwen2`, `qwen3` (0b59b5e).
- **CUDA graph at the batch-size cap** (`next`): at bs 5 full batches used to run eager.
  Qwen3-0.6B with 5 parallel went from 525 to 2770 tok/s total.
- **Split-k verify attention on `next-speed`** (d13df048): it no longer recompiles for every
  new extend length (1.8–7 s each), and Gemma 4 with head_dim 512 fits into sm_89 shared
  memory.
