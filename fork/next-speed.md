# next-speed: where the engine loses time, and what was done about it

Branch `next-speed` (from `next`, 2026-10-05). Hardware: RTX 4090 (sm_89, 24 GB, 128 SMs,
~916 GB/s copy bandwidth, ~165 TFLOPS bf16 / ~330 TFLOPS fp8 with fp32 accumulate) in an
8-vCPU VM. Main model: `RadixArk/Qwen3.8-27B-NVFP4` (64 layers: 48 GDN + 16 full attention;
MLP NVFP4, GDN/attention projections FP8 W8A8 static, lm_head NVFP4), fp8 KV cache,
`--memory-ratio 0.95 --max-prefill-length 4096`. Drafter: `z-lab/Qwen3.8-27B-DFlash2`
(fp8 draft quant, `--embed-device cpu`).

Tool: `benchmarks/bench_offline.py` (in-process, no HTTP): fresh random-token prefill,
decode as long-minus-short generation, `--natural` decodes chat prompts (needed for
speculative decoding), `--profile[-prefill]` writes a torch trace.

## Results (next -> next-speed, same flags, same machine)

| Qwen3.8-27B-NVFP4 | next | next-speed | |
|---|---|---|---|
| Prefill, 4k-token prompt | 3041 tok/s | 3357 tok/s | +10.4% |
| Prefill, 16k-token prompt | 3015 tok/s | 3181 tok/s | +5.5% |
| Decode bs=1, short context | 45.2 tok/s | 46.1-46.6 tok/s | +2-3% |
| Decode bs=1, 20k context | 41.6 tok/s | 44.0 tok/s | +5.8% |
| Decode bs=4 (aggregate) | 155.8 tok/s | 160.2 tok/s | +2.8% |
| DFlash2, 12 chat prompts | 102.6 tok/s | 119.4 tok/s | +16.4% (3.88 tokens/cycle on both; 37.8 -> 32.5 ms/cycle) |
| DFlash2, 15.5k-token context | 81.8 tok/s | 143.0 tok/s | +75% |

Other models (4k prefill / decode bs=1):

| Model | next | next-speed |
|---|---|---|
| Qwen3.6-35B-A3B NVFP4 (MoE offload, fp8 KV) | 13286 / 143.8 | 14968 (+12.7%) / 145.5 |
| Qwen3-VL-8B-Instruct (bf16) | 10147 / 57.1 | 10142 / 56.7 (noise) |
| gpt-oss-20b | ~14250 / ~187 | ~14300 / ~186.5 (noise, re-measured 2x) |
| Muse-Glimmer-30B NVFP4 | 2791 / 48.7 | 2866 (+2.7%) / 48.7 |

Full `-m "not slow"` suite on the 4090: 3029 passed, 0 failed.

## Where the time goes

**Decode bs=1 is bandwidth-bound.** A token reads ~17.6 GB of weights (NVFP4 MLP 10.3 GB,
FP8 projections 7.2 GB, lm_head 0.7 GB): at 916 GB/s that is 19.2 ms, a ceiling of ~52
tok/s. Per step (22.25 ms before): NVFP4 GEMVs 11.7 ms (~880 GB/s), FP8 GEMMs 8.5 ms
(208 cuBLAS calls, ~850 GB/s; q/k/v and qkv/z run as separate GEMMs because row-wise
`_scaled_mm` is unsafe on sm_89 with torch < 2.12), ~730 small kernels 1.5 ms, idle 0.5 ms.

**Prefill is compute-bound and already at peak where it matters.** 4k tokens took 1351 ms:
MLP bf16 GEMMs (NVFP4 dequantized to bf16 + cuBLAS) 812 ms at ~172 TFLOPS (bf16 peak; exact
W4A16 numerics cannot use the fp8 tensor cores: e2m1 x e4m3 block scale needs more than
3 mantissa bits), FP8 GEMMs 170 ms at fp8 peak. The losses were copies (~160 ms, 12%) and
a slow attention kernel (62 ms, ~55 TFLOPS; grows quadratically with the prompt).

**DFlash cycles were verify-GEMM bound at short context, verify-attention bound at long.**

## What changed (one commit each)

Prefill:
- `perf(nvfp4)` scratch chunks: cuBLAS writes each chunk into `out[:, n0:n1]` (ldc = N);
  the temp + copy went away (45 ms / 4k).
- `perf(fp8)` per-part fallback: each part's `_scaled_mm` writes its column slice instead
  of `torch.cat` (27 ms / 4k, bit-identical).
- `perf(gdn)` split conv: the triton conv reads the token-major qkvz slice and writes q|k|v
  as three contiguous buffers; transposes and the fla `.contiguous()` copies vanished
  (1373 -> 327 us per layer; also +12.7% prefill on Qwen3.6-35B-A3B).
- `perf(attention)` FlashInfer FA2 prefill inside the triton backend (fp8 KV pins triton):
  fresh chunks attend their own bf16 K/V, later chunks gather + dequantize the cached
  prefix in front (132 vs ~55 TFLOPS at head_dim 256).

Decode:
- `perf(fp8)` small-M triton W8A8 (M <= 16, only where row-wise cuBLAS is unavailable):
  in-kernel activation quant with `_static_quant`'s rounding, all fused parts in one
  launch, per-row scale; ~890 vs ~760 GB/s on attention q|k|v, rows bit-identical across
  batch sizes up to 16.
- `perf(attention)` decode split-k sized to the GPU (8..32 splits instead of a fixed 8):
  a 20k-token fp8 cache was read at ~290 GB/s by 32 programs.
- `perf(nvfp4)` two pipeline stages for the bm16 small-M GEMM on ~100 KB-smem GPUs (+4-7%).

DFlash:
- `perf(fp8)` small-M W8A16 tiles (16x32x256): the fp8 draft's projections 400 -> 880 GB/s.
- `perf(dflash)` draft attention through FlashInfer (grouped heads, window_left) instead
  of SDPA over head-expanded K/V with an explicit mask.
- `perf(dflash)` fused DFlash2 grouped dynamic conv (~340 eager launches per cycle -> 20).
- `perf(dflash)` greedy candidate-path selector in one kernel (~84 launches -> 1).
- `perf(dflash)` GDN commit after a graph verify replayed as a CUDA graph.
- `perf(attention)` split-k verify attention: Q tokens x GQA heads per program, the cache
  read once per slice (2.3 -> 0.16 ms per layer at 15k context).

## Tried and dropped

- Overlapping the NVFP4 dequant with the cuBLAS GEMM on a side stream: -5% per gate_up in a
  microbenchmark, nothing end to end (and a slightly larger transient). Reverted.
- Split-K for the fp8 small-M GEMM: retuned tiles without split-K did as well.
- The torch profiler overstates host overhead: the GDN-commit graph cut profiled idle
  18% -> 13% but gained ~0.4% unprofiled. Judge launch-overhead work by unprofiled runs.

## Not done: options that need a decision

- **DFlash block size.** `--speculative-dflash-block-size 16` (drafter trained at 8):
  code prompts +17-23%, prose slightly lower, 12-prompt total +1.6%. A usage hint, not a
  code change.
- **Online fp8 for bf16 weights (opt-in).** Qwen3.6-35B-A3B keeps its attention/GDN
  projections and lm_head in bf16: 52% + 16% of its decode step, already at the bandwidth
  roof. Per-row fp8 (as `--speculative-draft-quant fp8` does for the drafter) would halve
  those bytes, roughly +30% decode, but changes the model's numerics.
- Smaller items: fla GDN chunk kernels are H100-tuned (~45 ms per 4k prefill, maybe ~1%);
  fusing silu*mul into the NVFP4 down GEMV (~0.7% decode); `in_proj_ba` bf16 GEMV (~1%).
