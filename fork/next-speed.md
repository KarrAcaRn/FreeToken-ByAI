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

## Opt-in: `--online-quant fp8`

Same as `--quant-backend linear.none=fp8`. A checkpoint's bf16 linear weights (projections,
an untied lm_head) are quantized at load to e4m3 with one fp32 scale per output row and run
through the W8A16 kernels (GEMV at M=1, the small-M tiles, the triton GEMM for prefill,
which is within 2-13% of bf16 cuBLAS). Layers with fewer than 1024 outputs (MoE routers,
GDN `in_proj_ba`, shared-expert gates) stay bf16; tied lm_heads stay bf16; auto kernel
selection never picks it. `ft info` prices the smaller weights. Outputs change slightly:
greedy answers on the sample prompts stayed the same and the 16k-token retrieval test holds,
but this is a numerics change, hence opt-in.

| Model (4k prefill / decode bs=1 / KV tokens) | bf16 weights | --online-quant fp8 |
|---|---|---|
| Qwen3.6-35B-A3B NVFP4 (fp8 KV, 32k reserve) | 15389 / 149.8 / 9097 expert slots | 15091 / 209.9 (+40%) / 9876 slots |
| Qwen3-VL-8B-Instruct | 9701 / 58.0 / 30k | 9814 / 103.6 (+79%) / 82k |
| gpt-oss-20b | 13672 / 173.4 / 259k | 13279 / 216.3 (+25%) / 295k |
| Muse-Glimmer-30B NVFP4 | 2736 / 45.8 / 69k | 2944 / 53.3 (+16%) / 131k |

Qwen3.8-27B-NVFP4 has no large bf16 linears (its projections are fp8, its lm_head NVFP4), so
the option does nothing there.

## Qwen3.8-Flash-Next on 24 GB VRAM + 30 GB RAM (64 GB results below)

`RadixArk/Qwen3.8-Flash-Next-NVFP4` (126 GB: ~68 GB experts, 47.7 GB PLE table) runs with the
disk tier, the checkpoint on cephfs (no local NVMe):

    ft serve --model RadixArk/Qwen3.8-Flash-Next-NVFP4 --text-model-only --max-running-requests 1 \
      --kv-cache-dtype fp8 --moe-disk-tier on --expert-ram-experts 160 --ple-backend disk \
      --disable-moe-prefill-overlap --disk-tier-graph --cuda-graph-max-bs 1 --online-quant fp8 \
      --expert-profile flash-next-profile.json   # scripts/record_expert_profile.py

Where a decode token went (2.4 tok/s, 128 RAM experts by id): 417 ms per token, 287 ms of it in
the synchronous disk fetches (~96 experts per token, 2 per layer, each layer waiting the ~4 ms
ceph latency); the GPU idled ~87%. ~19% of the 24,576 experts fit the VRAM slot cache, 23% of
the activated ones miss it.

| Step | disk experts/token | decode tok/s |
|---|---|---|
| 48 RAM experts/layer by id | - | 2.2 |
| 128 by id | 95.8 | 2.40-2.52 |
| 128 ranked by Strata's profile | 80.9 | 2.69 |
| 128 ranked by our own coding-prompt profile | 69.8 | 2.99 |
| 160 ranked (RAM limit: ~2 GB left) | 58.2 | 3.20-3.28 |
| + all of a layer's disk segments read at once | 58.3 | 4.14 |
| + `--disk-tier-graph --cuda-graph-max-bs 1` | 58.3 | **4.99** |

After the disk wait, the rest of a token was host work, not data: the GPU ran 31 ms of the
~460 ms (profiled), PCIe copies ~20 ms; the host issued ~760 memcpys, ~530 launches and
~1100 syncs per token. Three fixes, each with greedy output identical to the reference:
the prefill copies only the routed RAM experts (it streamed the whole RAM prefix, ~400 MB
per layer); a layer's disk misses read all their segments at once (an expert's 9 tensors
lie scattered in the shard, and the 7 reads used to go one after another); and
`--disk-tier-graph` moves the per-layer host fetch behind a stream-memop flag handshake with
a coordinator thread, so the decode runs as a CUDA graph.

Measured and dropped: router lookahead prefetch (next layer's router on this layer's MoE
input, Strata's `RouterLookahead`): recall 34%, precision 31% on Flash-Next, and on ceph the
wrong reads plus the page-cache pressure made it slower (1.26 tok/s). Buffered reads through
the page cache instead of pinned RAM experts: slower (1.45 tok/s). An exclusive RAM tier
(ranks after the VRAM share): worse, the shared LRU slot cache does not keep the top ranks.
Bigger levers left, both larger projects: 2-3 bit experts (Strata's Q2/IQ2 GGUFs, ~35 GB,
would fit RAM + VRAM and drop the disk from decode) and Flash-Next's MTP head for speculative
decoding (Strata claims 1.6-1.8x).

### DFlash on Flash-Next (`PixelML/Qwen3.8-Flash-Next-NVFP4-DFlash`)

The DeepSpec drafter (5 layers, 1 GB bf16) runs through the DFlash path:
`--speculative-algorithm dflash --speculative-draft-model-path
PixelML/Qwen3.8-Flash-Next-NVFP4-DFlash --speculative-dflash-block-size 3`. It needed the
flat DSpark config and its query-zero shift, hidden-state taps in qwen4_exp (the HC-contracted
block input of the next layer), QSA verify graphs, a verify mode for the PLE conv history and
n-gram context (committed after the verify like the GDN states), disk-PLE staging for the
verify graph, and verify blocks routed through the decode slot cache. Greedy output equals
plain decode (blocks 2 and 6 byte-identical; block 3 differs in one comment word, a near-tie).

Same coding prompt, 160 RAM experts, `--disk-tier-graph`, adaptive gate off:

| Block (drafts) | tokens/cycle | acceptance | experts/layer (active, missed) | decode tok/s |
|---|---|---|---|---|
| plain | 1 | - | 12.5, 3.0 | 4.99 |
| 2 (1) | 1.88 | 88% | - | 4.25 |
| 3 (2) | 2.71 | 86% | 19.4, 5.7 | 4.71-4.81 |
| 6 (5) | 4.11 | 62% | 25.9, 8.1 | 4.21 |

The drafter predicts well, but here a verify costs like its experts: a cycle at block 3 is
551 ms, 545 of it the verify replay (the draft 3 ms, context store 3 ms, GDN commit 1 ms),
and every extra token in the block brings new experts to read from ceph. With the defaults
the adaptive gate measures this and switches speculation off. The verify graph itself takes
~19 ms of GPU time (len 6, experts resident), so with the experts in RAM (or a disk that
serves many small reads in parallel) the same acceptance would be a 2-4x decode gain. More
CPU threads for the reads do not help on 8 vCPUs (48 workers: plain 4.46, block 3 4.17);
batching an expert's scattered segments through io_uring is the open lever.

### After the RAM upgrade (64 GB, 2026-10-06)

Same recipe, profile re-recorded on the coding prompts (the top 320 experts per layer take
98.6% of the decode routing), 400 generated tokens:

| Config | decode tok/s |
|---|---|
| plain, 160 RAM experts (30 GB box) | 4.99 |
| plain, 320 RAM experts | **18.6-20.7** |
| DFlash block 3, 320 RAM experts | 11.7-14.7 |
| DFlash block 6, 320 RAM experts | 9.7-10.0 |
| 400 RAM experts | OOM kill (49.5 GB anon RSS) |

320 is the practical limit for 64 GB. With the disk mostly out of decode, plain is 4x
faster, and DFlash now loses. Not profiled yet; the likely cause is that a verify block still pulls more experts from RAM to VRAM than
one token does, and that costs more than the accepted drafts save. The adaptive gate
switches it off. Batching does not help either (`--max-running-requests 5
--cuda-graph-max-bs 5`): one request alone 12.6 tok/s, five at once 11.4 tok/s in total,
because the union of routed experts grows with the batch. A 4k-token prefill runs at 190 tok/s.

Where the time goes now (per-step timing, 300 tokens, adaptive gate off):

| | step (median) | tokens/step | ms/token | disk experts/step |
|---|---|---|---|---|
| plain | 46.5 ms | 1 | 58 | 8.0 |
| DFlash block 3 | 132 ms (verify 126) | 1.85 | 85 | 25.2 |

About 1.7% of the routed experts come from disk either way, so a verify block reads ~3x
the experts of a token. In plain decode the disk takes ~25 of 62 ms per token: a layer with
one disk miss waits 2.9 ms, with two 4.8 ms. The latency is small (a 4 KB read 0.4 ms);
the cost is that one expert's 2.4 MB (3x800 KB weights, 3x100 KB scales, each block
contiguous in its layer's shard) sits in one or two 4 MB ceph objects, i.e. on one OSD:
~3 ms, while ceph serves ~2.1 GB/s in aggregate. Chunked parallel reads of the same range
barely help (3.1 -> 2.8 ms), and our cephfs key may not set striped file layouts. A
simulated software striping (each expert as 8x300 KB pieces in 8 different objects, 16
threads) reads one expert in 1.9 ms and two in 3.1 ms, an estimated 8-10% decode gain; it
would need a ~23 GB expert-major copy of the tail experts. Parked until new hardware.

## Not done: options that need a decision

- **DFlash block size.** `--speculative-dflash-block-size 16` (drafter trained at 8):
  code prompts +17-23%, prose slightly lower, 12-prompt total +1.6%. A usage hint, not a
  code change.
- Smaller items: fla GDN chunk kernels are H100-tuned (~45 ms per 4k prefill, maybe ~1%);
  fusing silu*mul into the NVFP4 down GEMV (~0.7% decode); `in_proj_ba` bf16 GEMV (~1%).
