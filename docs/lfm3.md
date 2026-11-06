# LFM3 bf16 validation (part 4)

## Status: blocked before checkpoint execution

On 2026-11-06, the assigned task branch contained parts 1-3 through
`7063d0be`. The real checkpoint validation is **not complete**. The synthetic
parity results in [part 3](lfm3-model.md) do not establish real-checkpoint
generation parity or serving throughput.

The requested snapshot was absent:

```text
~/.cache/huggingface/hub/models--LiquidAI--LFM3-1.7B/snapshots/ac2586a34f1a1c03329dbdcdefabd8b6478ddaa7
```

Hugging Face's API resolved that exact revision and listed its model weights,
tokenizer, template and remote-code files. Downloading it with the installed
`huggingface_hub.snapshot_download` failed with:

```text
PermissionError: [Errno 13] Permission denied: '/mnt/cephfs_Buero/ki_modelle/huggingface'
```

The HF hub cache is a symlink to
`/mnt/cephfs_Buero/ki_modelle/huggingface/hub`; `findmnt /mnt/cephfs_Buero`
reported no mount. Restore the intended cache mount/access, provide the
snapshot, or authorize an alternative download location before continuing.
The shared cache symlink was not changed.

The RTX 4090 (24 GB, driver 595.99.02) also had two pre-existing compute
processes: PID 136120 (`decider_server.main`, 3426 MiB) and PID 205015
(`run_server.py`, 4854 MiB). Neither was stopped. Release these workloads
before measuring throughput and requiring an empty compute-process list.

On retry, the compute-process list was empty: the GPU blocker is resolved.
The snapshot was still absent, `findmnt /mnt/cephfs_Buero` still reported no
mount, and a fresh `snapshot_download` attempt failed with the same
`PermissionError`. Checkpoint access remains the prerequisite for execution.

## Requested checkpoint checks

| Check | Result |
| --- | --- |
| Three identical tokenized prompts, 50 greedy tokens vs HF bf16 | Not run: weights unavailable |
| First divergence and same-prefix top-2 logits | Not measured |
| Chat, thinking on/off, streaming reasoning, coding | Not run |
| Structured tool call and tool-result round | Not run |
| At least 8k tokens, beginning/middle retrieval and HF parity | Not run |
| Multi-turn radix hit vs cold output | Not run |
| Parallel mixed lengths vs individual greedy outputs | Not run |
| Optional real-server cache rebuild | Not run |
| Load time, KV capacity, prefill/decode throughput, CUDA graphs | No real-checkpoint measurements |

No serving or HF model process was started. No real-checkpoint divergence
was observed or ruled out, and no model fix is justified by this attempt.
FP8/NVFP4 and optional GGUF remain part 5.

## Regression verification

Environment: existing `/home/basti/claude/FreeToken-ByAI/.venv`, PyTorch
`2.14.1+cu130`, Transformers `5.18.0`, this checkout's Python sources and
native extensions. Command:

```bash
export PATH=/home/basti/claude/FreeToken-ByAI/.venv/bin:/usr/local/cuda/bin:$PATH
export CUDA_HOME=/usr/local/cuda
export PYTHONPATH="$PWD/python"
python -m pytest tests/models tests/engine tests/scheduler tests/kvcache tests/attention tests/layers \
  -m 'not slow' -q --basetemp ~/.cache/ft-pytest/lfm3
```

Result: **1381 passed, 228 skipped, 5 deselected**, 21 warnings in 112.60 s.
This includes `tests/models/lfm3`; it uses synthetic weights, not the missing checkpoint.
The local execution log is `~/.cache/ft-scratch/lfm3-part4/regression.log`.
The pytest temporary directory was removed. After the test process exited,
`nvidia-smi --query-compute-apps=pid --format=csv,noheader` listed only the
pre-existing PIDs 136120 and 205015. No GPU process from this task remains.
The retry started no GPU process and confirmed an empty compute-process list.
