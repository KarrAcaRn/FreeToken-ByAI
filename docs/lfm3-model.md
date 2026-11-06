# LFM3 model integration (part 3)

> Historical handoff from part 3. Open-work and unavailable-checkpoint statements
> below describe that stage, not current support. Parts 4-5 completed bf16, FP8
> and NVFP4 serving validation. See [current validation](lfm3.md),
> [supported models](models.md#lfm3-text) and [completion report](lfm3-report.md).

## Scope and decisions

The package `python/freetoken/models/lfm3/` implements the text architecture
`Lfm3ForCausalLM`, including the identical Base architecture. It loads original
HF names, fuses Q/K/V and w1/w3 separately, keeps the per-head attention gate
independent, and ties the LM head to `model.embed_tokens` when configured.
The quantization name map uses w1/w3 and w2, not gate_proj/up_proj/down_proj.

Corrections and additions to the original plan:

- Use part 2's `ShortConvGroupConfig`, not an extra `SlotStateSpec`. Read the
  current conv slab on every forward, carry six raw B*x values, and snapshot
  those inputs through `track_conv_src` into the hybrid radix track slots.
- All attention layers share one full paged-KV group. Sliding layers pass the
  configured window per call. Both installed HF `sliding_window_overlay` and
  Triton use `k > q - window`; 256 includes the current token without adjustment.
- Translate default partial RoPE to proportional RoPE: frequencies are spaced
  over the full head and their tail is zero. In addition, Liquid rounds cos/sin
  to the activation dtype before its fp32 rotation. The shared original table
  is not modified; LFM3 caches a rounded table. FP32 uses the Triton rope kernel
  because FlashInfer's installed rope kernel accepts only 16-bit activations.
- Plain RMSNorm is insufficient to reproduce Liquid's rounding: normalize in
  fp32, cast to the activation dtype, then multiply by the raw weight (no +1).
  Likewise, round SiLU before multiplying by the MLP up projection.
- Normalized K and V must have matching row strides for the shared KV store.
- Registration also needs the architecture's entry in `kernel/aot_models.py`;
  the live-registry coverage test found this requirement.

Unsupported `conv_bias=True`, convolution widths other than 7, and non-default
RoPE scaling fail explicitly. Speculative decoding remains rejected by part 2.
The parser defaults are `qwen3_coder` for tools and `qwen3` for reasoning.

## Checkpoint and reference verification

The supplied local snapshot paths were absent in this worker. The reference
files under `~/.cache/ft-scratch/lfm3/` were present and their config loaded
successfully through the existing `trust_remote_code=True` path. Synthetic
configs without `auto_map` exercised the existing RawConfigShim fallback.
No changes to `utils/hf.py` were necessary.

The safetensors header and chat template were fetched from LiquidAI/LFM3-1.7B
revision `ac2586a34f1a1c03329dbdcdefabd8b6478ddaa7`. All 286 source tensors map
onto the model's 240 fused tensor names with exact shapes. There is no separate
LM-head tensor. The template confirms XML-style function/parameter tool calls,
`<think>...</think>`, and `enable_thinking` defaulting to true.

The independent Torch reference in `tests/models/lfm3/lfm3_hf_ref.py` transcribes
that revision's math, using unfused HF names, full-sequence PyTorch convolution,
and HF's default SDPA attention. It contains no FreeToken cache or model code.
A direct diagnostic against the remote-code Liquid implementation on the toy
23-token prompt measured maximum logit differences of 0.01416 (Torch reference)
and 0.01074 (FreeToken), in bf16 with fp32 GEMM reductions.

## Validation

Tests use a seeded six-layer checkpoint with mixed conv/full/sliding layers,
window 8, hidden size 128 and separate query/KV head counts. They cover:

- one-shot prefill and chunks ending at 3, 7, 8, 9, 14, 17 and 23 tokens;
- five token-by-token decode steps, eager and through the production GraphRunner,
  including one real request padded to a two-row graph;
- unequal-length batched requests, sandwich norms enabled and disabled;
- a real hybrid-radix hit at token 64 restoring a tracked conv snapshot,
  compared with both a cold run and the reference;
- a completed request's dirty state slot reused for a fresh three-token prompt;
- exact zero-tail inverse frequencies at the shipping 128-dimensional head size.

The model/cache/backend/graph harness follows the existing tiny-engine tests;
it does not launch a server. Both bf16 and fp32 execution are checked against a
reference of the same dtype. Attention reductions and norms use fp32. Tests
set `allow_bf16_reduced_precision_reduction=False` and restore it afterwards:
otherwise cuBLAS may truncate reductions differently for fused versus separate
projection shapes. The fixed logit tolerance is `atol=rtol=0.02`; it was not
increased to accommodate those differences. A completely fp32 model is not
bitwise equivalent to bf16 execution (the exploratory cross-dtype comparisons
exceeded this tolerance); the final parity matrix compares matching dtypes.

An intentional `window + 1` mutation failed the prefill logit assertion; the
original implementation was restored before the final suite. All GPU tests
skip automatically without CUDA. No tests require a downloaded checkpoint.

On RTX 4090 with driver 595.99.02 and the existing FreeToken venv:

```bash
export PATH=/home/basti/claude/FreeToken-ByAI/.venv/bin:/usr/local/cuda/bin:$PATH
export CUDA_HOME=/usr/local/cuda
export PYTHONPATH="$PWD/python"
python -m pytest tests/models/lfm3 -q --basetemp ~/.cache/ft-pytest/lfm3
python -m pytest tests/models tests/engine tests/scheduler tests/kvcache tests/attention tests/layers tests/server tests/tokenizer -m 'not slow' -q --basetemp ~/.cache/ft-pytest/lfm3
```

The standalone parity matrix passed **15 tests**. Python compilation and
`git diff --check` passed. The first complete regression run had **2579 passed,
252 skipped, 5 deselected, 1 failed**; the failure was the missing AOT entry,
which was then added. The final regression result is recorded below.

## Handoff

The real 1.7B serving run, 50-token HF comparison, long prompts, chat/tools and
load/KV/throughput measurements remain part 4. FP8/NVFP4 execution and optional
GGUF support remain part 5; this change prepares their checkpoint name mapping
but makes no claim that those checkpoints were executed. No server was started.
Two pre-existing GPU processes were left untouched. Work stayed on the assigned
task branch; no branch switch, merge, push or PR operation was performed.

Final full-suite result: **2580 passed, 252 skipped, 5 deselected**, 21 warnings,
112.48 seconds. This includes all 15 LFM3 parity cases on the GPU. The requested
pytest base directory was removed after the run; diagnostic logs remain in
`~/.cache/ft-scratch/lfm3/`.
