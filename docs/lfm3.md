# LFM3 validation record

Validated on 2026-11-06 on RTX 4090 (24 GB, sm_89), NVIDIA 595.99.02,
PyTorch 2.14.1+cu130 and Transformers 5.18.0, with parts 1-3 through
`7063d0be`. The previously missing CephFS checkpoint is now accessible.
No model/kernel changes were needed in part 4. Part 5 checkpoint quantization
results are consolidated below; online FP8 below is a separate runtime conversion.

## Required correction to the serving recipe

**Pass `--online-quant none` for bf16 validation.** This fork defaults to
online FP8 even when the checkpoint is bf16. The initial server log showed
`quant_backend='linear.none=fp8'`; its larger differences were not a bf16
parity result. With the explicit flag, the log shows `quant_backend=None`.
The existing CLI behavior was not changed for other models.

```bash
export PATH=/home/basti/claude/FreeToken-ByAI/.venv/bin:/usr/local/cuda/bin:$PATH
export CUDA_HOME=/usr/local/cuda
export PYTHONPATH="$PWD/python"
LFM3_SNAPSHOT="$HOME/.cache/huggingface/hub/models--LiquidAI--LFM3-1.7B/snapshots/ac2586a34f1a1c03329dbdcdefabd8b6478ddaa7"
ft serve --model-path "$LFM3_SNAPSHOT" --port 19500 --online-quant none \
  --max-running-requests 4 --max-seq-len-override 16384 \
  --max-extend-length 2048 --cuda-graph-max-bs 4 \
  --enable-cache-report --enable-metrics-report
```

Auto selects `triton`, `hybrid_radix`, page size 1, `qwen3` reasoning and
`qwen3_coder` tools. Graphs capture batch sizes 1, 2 and 4. Wait for
`/v1/cache/status` to report `state=serving`; `/health` alone can succeed
before generation is available. Stop each server by its recorded PID.

## HF comparison

HF loaded this exact snapshot with `trust_remote_code=True`,
`dtype=torch.bfloat16`, `attn_implementation='sdpa'`; no separate venv or
reference-code edits were needed. Both sides used the checkpoint template
with `add_generation_prompt=True, enable_thinking=False`. `/v1/tokenize`
confirmed identical input IDs for all four cases. The completions endpoint
received those IDs with `temperature=0, max_tokens=50, ignore_eos=true`.
Each final comparison started with a flushed cache.

HF used cached token-by-token decode. A direct FreeToken run using the
existing model/cache/GraphRunner parity harness, enlarged for the real
checkpoint, recorded token IDs and raw top-2 logits. Its decoded per-token
outputs matched the server's logprob token list in all four cases. Both used
PyTorch's default bf16 reduction setting; disabling reduced-precision GEMM
reductions was also examined, but was not substituted into the reported run.

Positions below are **one-based generated-token positions**.

| Prompt | Input tokens | First 50 greedy tokens vs HF |
| --- | ---: | --- |
| Explain why the sky is blue in three sentences. | 21 | 50/50 identical |
| Write a Python function that returns the unique items of a list while preserving order. Explain its complexity. | 31 | 50/50 identical |
| Describe how to grow tomatoes in a balcony container, including watering and sunlight. | 27 | First divergence at 30; bf16 tie |
| Beginning/middle secret-code retrieval | 8347 | 50/50 identical, across five prefill chunks |

At position 30 of the tomato prompt, with the **same 29-token generated
prefix**, the raw logits were:

| Candidate | Token ID | HF bf16 | FreeToken bf16 |
| --- | ---: | ---: | ---: |
| ` &` | 900 | 23.375 | 23.375 |
| newline | 207 | 23.250 | 23.375 |

HF selects ` &`; FreeToken's argmax selects the lower ID at the exact tie.
The FT gap is 0, the HF gap is 0.125 (one bf16 ULP at this magnitude). This
is the near-tie exception, not a claim of 50-token equality for this prompt.
No larger-margin first divergence remains in the cold bf16 comparison.

For contrast, the discarded online-FP8 run diverged at positions 48, 27
and 11 for sky, code and long input, with FT top-2 gaps 0.625, 0.125 and
0.125 respectively (HF gaps 0, 0.125 and 0.25). Explicitly retaining bf16
weights removes these three divergences. The separate bf16 reduction-mode
diagnostic also changed HF's own greedy output, confirming that reduction
settings must be kept fixed when comparing these close logits.

The long input starts with `At the beginning of this archive the first
secret code is ORCHID-731. Remember it.`, then repeats `The archive records
ordinary deliveries of paper, pencils, and envelopes. No special codes
appear in these records.` plus a newline 180 times. The middle sentence is
`At the middle of this archive the second secret code is COBALT-492.
Remember it.`, followed by the same 180 repetitions, then `What are the
first and second secret codes? Reply with both codes only.` The server log
shows chunks of 2048, 2048, 2048, 2048 and 155 tokens. Both codes were
recovered. With thinking enabled, the final content was just the two codes,
with reasoning separately parsed. With thinking disabled this checkpoint
can still generate reasoning-like prose and a stray `</think>` on this
repetitive input; disabling thinking is a template instruction, not a
constraint on generated tokens. The raw HF continuation likewise begins
with reasoning-like prose. This is an output-quality limitation.

## API, cache and concurrency

- `17 * 23` returned 391 with thinking off and on. Thinking-on responses
  had separate `reasoning_content`. Both streaming responses reconstructed
  exactly the corresponding buffered content/reasoning fields.
- The coding request produced a set-based `unique_in_order` function.
  Executing it on `[3, 1, 3, 2, 1]` returned `[3, 1, 2]`.
- `get_weather` parsed as a structured tool call with JSON arguments
  `{"city":"Berlin","unit":"celsius"}` and `finish_reason=tool_calls`.
  After a tool result reporting 18 C and sunny, the assistant reported
  those values. That continuation also reported 131 cached prompt tokens.
- A multi-turn balcony-project chat reported **128 cached tokens** on the
  253-token follow-up. Its 57-token answer named careful watering and full
  sunlight. The message was exactly equal after flushing the cache, where
  the reported hit was zero, and again after a full server restart
  (`cached_prompt_tokens=0`, 253 input tokens).
- Four simultaneous requests used mixed lengths 21, 31, 27 and 8347,
  each generating 100 tokens. Logs prove four active requests. Sky and
  long outputs matched individual runs exactly. Code and tomatoes differed
  only after a first equal-prefix bf16 tie, detailed below. This does **not**
  establish unconditional batch-invariant text for arbitrary prompts.
- A second mixed-length batch (22, 246, 28, 9044 tokens) returned exactly
  the individual answers for all four requests: `2+2 = 4`, `PINEAPPLE`,
  `Katze`, and `ORCHID, COBALT`. The long request retrieved labels from
  beginning and middle with 750 background repetitions on each side.

The first concurrent-run divergences have the following top-2 logprobs
(logprob differences equal logit differences):

| Prompt / position | Candidates | Individual | Concurrent |
| --- | --- | --- | --- |
| Code / 29 | ` occurrences`, ` occurrence` | -0.824011, -0.949011 | -0.854615, -0.854615 |
| Tomatoes / 30 | ` &`, newline | -1.019635, -1.019635 | -0.966135, -1.091135 |

Each has an exact tie on one side and a one-ULP gap on the other. The
unquantized backend uses a fp32-accumulating Triton GEMV for a single bf16
row and torch GEMM for larger batches; attention also partitions reductions
by batch size. Bitwise batch invariance is not guaranteed by these paths.
These measured ties explain why full greedy strings can differ without
request-state corruption; they are retained here rather than hidden by
choosing only the four stable-answer prompts.

## Measurements

Single-run observations, not an A/B performance claim; desktop GPU processes
occupied about 0.5 GiB. All numbers below use **bf16**, CUDA graphs enabled,
and the command above (the online-FP8 exploratory run is excluded).

| Measurement | Result |
| --- | ---: |
| Safetensors weight-load progress timer | 1.73 s |
| CLI parsed arguments to API ready (log timestamps) | about 9 s, warm kernel cache |
| Allocated full KV capacity (log) | 769988 tokens, 16.15 GiB K+V |
| Cold 8347-token prefill | 237.197 ms, 35190.20 tok/s |
| Decode bs=1, that long prompt | 192.90 tok/s, 219 generated tokens |
| Decode bs=1, coding prompt | 196.95 tok/s |
| Four active requests, steady decode scheduler interval | 515.61 aggregate tok/s |
| Four mixed requests, 400 generated tokens including prefill/HTTP time | 1.0473 s, about 382 aggregate tok/s |

Do not compare the last two rows as the same metric. The first parallel
scheduler interval includes the long prefill and measured 275.32 tok/s;
the later 515.61 tok/s interval had four requests decoding. No throughput
claim is made for maximum context or sustained production load.

## Verification and handoff

```bash
python -m pytest tests/models tests/engine tests/scheduler tests/kvcache tests/attention tests/layers \
  -m 'not slow' -q --basetemp ~/.cache/ft-pytest/lfm3
FREETOKEN_REBUILD_TEST_MODEL="$LFM3_SNAPSHOT" \
FREETOKEN_REBUILD_EXTRA_ARGS='--online-quant none --max-running-requests 4 --max-seq-len-override 16384 --max-extend-length 2048 --cuda-graph-max-bs 4' \
  python -m pytest tests/e2e/test_cache_rebuild.py -q --basetemp ~/.cache/ft-pytest/lfm3
```

The optional real-server rebuild test passed: **1 passed in 19.20 s**,
including KV resizing, conv-state pool resizing, graph recapture, flush,
and refusal of an impossible allocation without losing serving capability.
Final regression: **1419 passed, 214 skipped, 5 deselected**, 21 warnings
in 126.11 s, including all 15 LFM3 parity cases. The earlier blocked attempt
had 1381 passed / 228 skipped; restoring checkpoint access enabled more
checkpoint-dependent coverage. `git diff --check` passed. No C++ source
changed, so no extension rebuild was necessary.

Local scripts, inputs, raw HF/FT logits and API responses are retained in
`~/.cache/ft-scratch/lfm3-part4/` (`hf_run.py`, `direct_run.py`, `api_run.py`,
`chat_run.py`, `stable_batch.py`, corresponding JSON/log files).
`hf_default.json` is the reported HF baseline; `hf.json` is the separate
fp32-reduction diagnostic. No new regression test was added because no
production-model arithmetic or state bug was found. Existing model parity
tests already cover the relevant state transitions.

All work remains on the assigned Tasks-Board branch, not `feat/lfm3` from
the superseded parent plan. No branch switch, merge, push, or change to the
protected worktrees was made.

Every server launched for this task was stopped, all HF/diagnostic/pytest
processes exited, and `~/.cache/ft-pytest/lfm3` was deleted. The final
`nvidia-smi --query-compute-apps=pid --format=csv,noheader` still lists
**235776 and 236743**, the pre-existing GNOME remote desktop and Ptyxis
processes. No task-owned GPU process remains; the literal empty-list
condition is not met because these desktop processes were left untouched.

## FP8 and NVFP4 validation (part 5)

2026-11-06, same RTX 4090 and environment as above, based on `a2166909`.
The command above was used with these `--model-path` values, one server at a
time, keeping `--online-quant none` and all other flags identical:

- FP8: `~/.cache/huggingface/hub/models--LiquidAI--LFM3-1.7B-FP8/snapshots/243955da95b1cd68026f293b29de4b4c13f3638f`
- NVFP4: `~/.cache/huggingface/hub/models--LiquidAI--LFM3-1.7B-NVFP4/snapshots/5f8f594ffc22400b02a11e00e2d9393a9371c161`

### Loader correction and execution semantics

The existing registry correctly maps `gate_up_proj` to `w1|w3`, `down_proj`
to `w2`, and `qkv_proj` to `q_proj|k_proj|v_proj`. However, `QuantConfig`
declares storage roles; it does not translate the tensors yielded by the
family loader. The first FP8 serve failed with
`KeyError: model.layers.0.feed_forward.gate_up_proj.weight_scale_inv`.
The LFM3 loader now translates dialect storage names before sharding/fusion:

- compressed-tensors `weight_scale` becomes `weight_scale_inv`, with its
  bf16 values unchanged (these are multiplicative dequantization scales).
- ModelOpt `weight_scale_2` becomes fp32 `weight_global`, expanded per output
  row before fusion, preserving different globals for w1 and w3. Row-parallel
  projections retain all output-row globals. Weight shapes are read from all
  shard headers, so a global need not share a file with its weight.
- `input_scale` remains a fp32 scalar; fused parts use their maximum, matching
  the existing dense readers. The sm_89 execution path does not consume it.

A scan of every two-dimensional non-embedding weight against its dialect and
mapped scheme found **116 FP8 / 37 bf16** projections in FP8 and **72 NVFP4 /
81 bf16** projections in NVFP4. Thus conv and gates remain bf16 in both, and
all attention remains bf16 in NVFP4. Norms and tied embeddings stay bf16.

The FP8 backend is `TritonFp8BlockLinearKernel`: 128x128 weight scales,
dynamic per-token group-128 FP8 activations above one row, W8A16 GEMV at one
row. The NVFP4 log selects `TritonNvfp4LinearKernel`, rejecting b12x (requires
sm_120/sm_121) and cuBLAS (NVFP4 tensor cores require sm_100+). It transposes
packed weights/scales to the K-major resident layout and dequantizes in its
Triton kernel with bf16 activations: **W4A16**, not W4A4 activation emulation.
The separately available `emulation` backend is not selected. Native W4A4
hardware and tensor-parallel serving were not tested here.

### Token comparison and quality

Reuse part 4's saved exact input token IDs and cold bf16 API responses from
`lfm3-part4/inputs.json` and `ft_api.json`. Flush before every completion;
`temperature=0`, `max_tokens=50`, `ignore_eos=true`, `logprobs=2`.
Compare the ordered per-token strings returned by the API, not retokenized
completion text. Counts below are equal prefixes, not total matching tokens;
divergence positions are one-based. No new HF quantized-reference run is claimed.

| Prompt | FP8 prefix / first divergence | NVFP4 prefix / first divergence |
| --- | --- | --- |
| Sky, 21 input tokens | 15 / 16 | 11 / 12 |
| Python unique items, 31 input tokens | 28 / 29 | 0 / 1 |
| Tomatoes, 27 input tokens | 50 / none within 50 | 29 / 30 |
| Secret codes, 8347 input tokens (additional case) | 12 / 13 | 8 / 9 |

Both sky explanations discuss scattering; both coding continuations describe
order-preserving deduplication; both tomato answers start a container-growing
guide. NVFP4's first coding token is `**` rather than bf16's `To`, so a zero
matching prefix here is a change of answer format, not incoherent output.
A longer NVFP4 request produced a complete `unique_items` function; executing
its first code block on `[3, 1, 3, 2, 1]` gave `[3, 1, 2]`. The subsequent
example-test block was truncated at the 700-token limit.
Both long-input continuations identify ORCHID-731 and COBALT-492 but retain
reasoning-like prose despite disabled thinking, as already seen in bf16.

Chat with thinking disabled and enabled returned 391 for `17 * 23` for both
checkpoints; enabled thinking produced separate `reasoning_content`.
**Quality caveat:** NVFP4's thinking-disabled answer included a malformed
written multiplication row (`153` for the shifted `17 * 20`) before correctly
stating `340 + 51 = 391`. This is not a claim of error-free arithmetic or
quantized/bf16 equivalence. These samples are plausibility checks, not a
quality benchmark, and early quantization divergences were not dismissed as
bf16 near-ties.

### Measurements

API `timings` fields, cold prefix cache; these first requests include warmup
and scheduling effects. Decode uses 49 intervals for 50 generated tokens.

| Measurement | FP8 | NVFP4 |
| --- | ---: | ---: |
| Weight-load timer | 1.19 s | 1.92 s |
| CLI args to API ready | about 11 s | about 15 s |
| Allocated KV tokens | 828635 | 851863 |
| K+V memory | 17.39 GiB | 17.87 GiB |
| 8347-token prefill | 242.406 ms | 255.197 ms |
| Long prefill tok/s | 34433.93 | 32708.10 |
| Long decode tok/s | 163.07 | 193.62 |
| Coding prefill tok/s | 891.30 | 1092.04 |
| Coding decode tok/s | 167.46 | 201.59 |

### Optional GGUF

A range read of the first 64 KiB of `LFM3-1.7B-BF16.gguf` from
[LiquidAI/LFM3-1.7B-GGUF](https://huggingface.co/LiquidAI/LFM3-1.7B-GGUF/tree/cd0c74c575b5c416f3011b5b4c298077f26ca8c2)
confirmed `general.architecture = lfm3` (revision
`cd0c74c575b5c416f3011b5b4c298077f26ca8c2`). No full GGUF was downloaded.
The vendored constants only know LFM2/LFM2MOE; there is no LFM3 GGUF config
adapter or tensor mapping. Adding a constant alone would not establish the
mixed layer layout, sandwich norms, attention gates and per-type proportional
RoPE. That separate adapter and parity validation are deferred; GGUF is
**unsupported**, not silently routed through LFM2.

### Verification artifacts

Local logs, API responses, exact input reuse script and GGUF inspection are
in `~/.cache/ft-scratch/lfm3-part5/`. The original failed FP8 startup is
`fp8-server.log`; successful startup is `fp8-fixed-server.log`.
The two new cases in the existing `tests/models/lfm3/test_parity.py` compare
loaded fused FP8/NVFP4 weights against independent dequantization, including
distinct w1/w3 globals and weights/scales in separate shards. Replacing globals
with 1 intentionally failed the numerical assertion (maximum relative error
3); the mutation was restored. This guards silent scaling corruption, not
only whether startup raises an error. The original 15 GPU parity cases also
passed; the expanded standalone run was **17 passed**, 11 warnings, 9.19 s.

Final part 5 regression command:

```bash
export PATH=/home/basti/claude/FreeToken-ByAI/.venv/bin:/usr/local/cuda/bin:$PATH
export CUDA_HOME=/usr/local/cuda
export PYTHONPATH="$PWD/python"
python -m pytest tests/models tests/engine tests/scheduler tests/kvcache \
  tests/attention tests/layers tests/server tests/tokenizer tests/kernels \
  -m 'not slow' -q --basetemp ~/.cache/ft-pytest/lfm3
```

Result: **3266 passed, 317 skipped, 10 deselected**, 13 warnings in
**463.14 s**, including all 17 LFM3 cases. The run included first-time GGML
CUDA JIT compilation; no C++ source was changed. `git diff --check` passed.
The loader/test fix is commit `44fc2665`.

All task-owned servers and test processes exited, and
`~/.cache/ft-pytest/lfm3` was removed. The final compute-process query still
lists the same pre-existing **235776** (GNOME remote desktop) and **236743**
(Ptyxis). Thus **no task-owned GPU process remains**, but the literal globally
empty-list condition is not met; unrelated desktop processes were not killed.
