# LFM3 infrastructure (part 2)

> Historical handoff from part 2. Open-work and unavailable-checkpoint statements
> below describe that stage, not current support. Parts 4-5 completed bf16, FP8
> and NVFP4 serving validation. See [current validation](lfm3.md),
> [supported models](models.md#lfm3-text) and [completion report](lfm3-report.md).

This change prepares the engine for LFM3; it does not register or load the model.

## Decisions and corrections to the original plan

- Hybrid state is structural, not a `ModelSpec` flag. `ShortConvGroupConfig`
  participates in `has_linear_attention`, `linear_attention_group()` and
  `is_linear_layer()`. It owns no paged KV. The existing engine/scheduler therefore
  allocate `LinearStatePool` and select `hybrid_radix` (unless explicitly naive).
- A standalone group is preferable to a GDN subclass: short convolution has no
  key/value heads, output gate or recurrence. The group declares `conv_dim` and
  `conv_kernel_dim` (default 7). TP divides channels evenly. Its history is
  `pool.conv_states[pool.local_index(layer_id)]`, shaped `[slots, H/TP, 6]`.
  `recurrent_states` and `host_recurrent_states` are `None`; no dummy recurrence
  storage is allocated. GDN/KDA retain their existing geometry and dtypes.
- `SlotStateSpec` alone could not create a pool in the original engine. Additional
  slot states can still accompany either kind of group, but the primary short-conv
  history uses the existing conv slab, avoiding duplicate history allocations.
- All 11 attention layers will share one `FullAttentionGroupConfig` with
  `per_layer_sliding_window=True`. This adds SWA to the *backend requirements*,
  while the KV spec stays FULL with `sliding_window=None`. No SWA pool or window
  eviction is introduced. Auto selects Triton; incompatible explicit backends
  (including either half of a prefill/decode pair) are rejected.
- The model must pass `AttentionSpec(sliding_window=256)` only on its five sliding
  layers. The other six layers remain full attention. Triton applies the mask to
  the full indices when no separate SWA indices exist.
- Speculation is rejected for short-conv groups before weights load, including
  DFlash, which does not take the ordinary `spec_verify` validation path.
- Host-bank byte reporting previously indexed a layer instead of a slot. It now
  reports all layers of one slot, matching device accounting. This corrects the
  startup memory log; it does not change GDN allocation or execution.

## Contract for the model implementation (part 3)

The engine attaches `LinearAttnBackend` for either state group. It builds
`batch.fla_metadata` without executing GDN kernels:

- `cache_indices`: live slots, independent of request table indices;
- `cu_seqlens`, `has_initial_state`, `fresh_state_indices`, `max_seq_len`: packed
  prefill boundaries and whether to use existing history;
- `track_dst`, `track_boundary_row`, `track_conv_src`: the deepest chunk-aligned
  interior snapshot and its last six input positions;
- decode graph capture uses persistent slot-index buffers, refreshed on replay.

Pass `has_initial_state` into the width-7 varlen dispatcher so reused fresh slots
ignore old history (equivalent to PLE's fresh-state masking). Snapshot the last
six **B*x inputs**, not convolution outputs, at `track_conv_src` into `track_dst`.
Do this before any operation that could overwrite the inputs. The live final
history is updated by the convolution. Snapshot donation, host archive/restore,
COW, reset and rebuild then use the existing pool lifecycle. Re-read the pool slab
on each forward because rebuild replaces its storage. Chunk alignment remains
that of the existing hybrid radix cache.

BF16 history for the real 13 x 2048 x 6 geometry costs 319488 bytes per physical
slot at TP=1, divided by TP. Hybrid slot sizing remains four working slots per
running request, snapshot-cache slots, and the padding sink. The forecast charges
only this history, without GDN recurrent state or GDN chunk activations.

## Open work

A dedicated SWA pool combined with hybrid radix (variant B) remains deferred.
Part 3 supplies the model, its snapshot writes and end-to-end parity checks.
Checkpoint serving, HF token comparisons and throughput/load-time measurements
belong to part 4; FP8/NVFP4 and optional GGUF validation belong to part 5.

## Validation

On NVIDIA RTX 4090, driver 595.99.02, using the existing FreeToken venv and
`CUDA_HOME=/usr/local/cuda`, `PYTHONPATH=$PWD/python`:

```bash
python -m pytest tests/models tests/engine tests/scheduler tests/kvcache tests/attention tests/layers tests/spec -m 'not slow' --basetemp ~/.cache/ft-pytest/lfm3 -q
```

Result: **1371 passed, 234 skipped, 5 deselected**, 21 warnings, 315.44 seconds.
This includes the existing GDN/KDA model, scheduler, pool and speculative tests.
The new GPU test compares short-conv graph replay after two slot remappings with
an independent tensor convolution/history update. CPU checks cover TP=1/2/4
byte counts, host snapshot round trips, COW/reset/rebuild, prefill track indices,
forecast versus physical allocations, and the backend matrix on sm_89.

A mutation removing only the additional SWA backend requirement makes the new
sm_89 auto-selection test fail with `fi != triton`. The mutation ran in a separate
Python process and did not change source files. Python compilation and
`git diff --check` also passed. The direct `pytest` executable initially failed
collection because a test imports `tests.models`; `python -m pytest` includes
the checkout root and collected the complete suite successfully.

No model server or checkpoint benchmark was run in this infrastructure step.
Two pre-existing GPU processes were left untouched; all test processes started
for this change exited. Native extensions were copied from the permitted
`ft-next-wt` source into this checkout; no C++ source changed.

Final targeted rerun after the last edits: **81 passed**, 11 warnings, 5.93 seconds
(backend matrix, short-conv forecast, pool lifecycle and GPU graph replay).
