# next-ROCm

`next-ROCm` is our `next` plus the upstream ROCm PRs that we could not run here (no AMD GPU, no ROCm on the dev box), and the gfx1151 pieces of #260 that `next` still lacks. It exists so someone with a Strix Halo (gfx1151, 128 GB unified memory) can test one branch and report back. CUDA behaviour is unchanged: every change is HIP-gated, docs, or tests.

Status: built and unit-tested on CPU only (CUDA build path and CPU suite pass). Nothing on this branch has run on an AMD GPU yet.

## What it contains

Upstream PRs merged on top of `next`:

| PR | What it does |
|---|---|
| #687 | `moe_align_block_size` takes a pure-torch path on ROCm with Triton >= 3.8 (`tl.histogram` miscompiles there); `FREETOKEN_MOE_ALIGN_IMPL=torch\|triton` forces a path. Our follow-up commit relaxes its `packaging<26` cap |
| #763 | AIME e2e memory check uses `torch.cuda.mem_get_info` on ROCm instead of `nvidia-smi` (test only) |
| #535 | `docker/rocm/Dockerfile.rocm10.1.0` (ROCm 10.1, torch 2.14.0+rocm10.1.0, Triton 3.8) and the `.github/workflows/rocm-ci.yml` validation workflow |
| #764 | CPU/hybrid MoE on ROCm: kernel IO for the expert handshake plus a graph replay probe; decode graphs are turned off when the probe fails, instead of replaying stale expert inputs |

Parts of #260 ("ROCm: validate native gfx1151 serving on Strix Halo"), one commit:

- `hip_compat.h`: `cudaDevAttrCanUseHostPointerForRegisteredMem` maps to the real `hipDeviceAttributeCanUseHostPointerForRegisteredMem`, not `hipDeviceAttributeUnifiedAddressing`; gfx1150/gfx1151 are listed as targets.
- `jit/fast_index_copy.cuh` `host_ptr_identity()`: returns false when an attribute query fails, and on HIP clears the failed query from the last-error slot.
- `kernel/utils.py` `_rocm_link_flags`: searches `lib64` and `lib`, picks the numerically newest `libamdhip64.so.N`, atomically replaces a stale or broken `freetoken/rocm-lib/libamdhip64.so` symlink (left after a ROCm upgrade), and honours `XDG_CACHE_HOME`. C++-only `load_aot`/`load_jit` modules skip the HIP runtime lookup.
- `setup.py` `_rocm_paths`: `lib64` + numeric SONAME choice.
- `docs/install_amd.md`: short Strix Halo section.
- Tests: link-flag tests (stale/broken link, lib64 + numeric SONAME, C++-only skip), gfx1151 never passes an NVIDIA SM gate, unified memory on HIP auto-picks `fused`.

## Not taken, and why

| PR | Why not |
|---|---|
| #260 remainder | Superseded on `next`: runtime bring-up by #132/#241/#134/#316, Triton/torch 2.14 work by #587, the old Qwen/Gemma GGUF loaders and HIP GGUF kernels by vendored ggml-cuda (#690, #701, #702). The rest is host-specific benchmark harnesses and docs, a ROCm-10-only setup preflight that would reject ROCm 7.x, install-contract changes to `pyproject.toml`, and generic server features. A few fixes are kept on hold as C1-C6 below |
| #217 | Superseded: its foundation is in #132/#134/#241, its ~10k lines of own GGUF HIP kernels are replaced by ggml-cuda; the rest is benches, CI and generic features |
| #317 | Serializes #260's auxiliary expert banks, which nothing on `next` produces; not ROCm |
| #135 | RCCL for tensor parallel. A single Strix Halo runs TP=1, which never uses PyNCCL. Revisit for multi-GPU ROCm |
| #23, #137 | Fully absorbed by #132/#241/#134 |
| #378, #667 | Superseded by upstream #670 (cpu-moe executor split with GPU sync backends) + #764 (on this branch); #687 covers #667's moe_align part |

## Tester checklist (Strix Halo, gfx1151, 128 GB unified memory)

### 1. Environment

- Linux with an amdgpu kernel driver and firmware that support gfx1151 (kernel >= 6.14 recommended).
- Memory split: either a large BIOS UMA carve-out (for example 96 GB), or a small carve-out (0.5-2 GB) plus a raised GTT limit on the kernel command line (`ttm.pages_limit=31457280 ttm.page_pool_size=31457280`, about 120 GiB in 4 KiB pages). Write down which one you used.
- Base image: `docker/rocm/Dockerfile.rocm10.1.0` (ROCm 10.1, torch 2.14.0+rocm10.1.0, Triton 3.8). Bare metal with ROCm 7.14 or 10.x and a PyTorch build with native gfx1151 kernels also works (same install steps).

```bash
docker build -f docker/rocm/Dockerfile.rocm10.1.0 -t freetoken-rocm10 docker/rocm
docker run --rm -it --device=/dev/kfd --device=/dev/dri \
  --group-add="$(getent group video | cut -d: -f3)" --group-add="$(getent group render | cut -d: -f3)" \
  --ipc=host --shm-size=32g \
  -e PYTORCH_ROCM_ARCH=gfx1151 -e FREETOKEN_ROCM_ARCH=gfx1151 \
  -v "$PWD:/workspace/FreeToken" -v "$HOME/models:/models" -w /workspace/FreeToken \
  freetoken-rocm10 bash
unset HSA_OVERRIDE_GFX_VERSION
```

Record what HIP reports, because KV and expert caches are sized from it:

```bash
python - <<'EOF'
import torch; p = torch.cuda.get_device_properties(0)
print(torch.__version__, torch.version.hip, p.gcnArchName, "integrated", p.is_integrated,
      "warp", p.warpSize, "mem_get_info GiB", [x / 2**30 for x in torch.cuda.mem_get_info()])
EOF
rocminfo | grep -E 'gfx|Marketing'
```

Expected: `gfx1151`, `integrated True` (if False, export `FREETOKEN_UNIFIED_MEMORY=1`), warp 32.

### 2. Install

```bash
python scripts/rocm_overrides.py > /tmp/rocm-overrides.txt   # pins the torch/triton the image ships
uv pip install --python "$(command -v python)" --no-build-isolation --overrides /tmp/rocm-overrides.txt -e .
python setup.py build_ext --inplace
python -c "import freetoken.kernel._pinned_tensor, freetoken.kernel._cpu_moe; print('ext ok')"
python -c "from freetoken.kernel.pinned import _host_ptr_identity; print('host_ptr_identity', _host_ptr_identity())"
```

Do not install the `[accel]`, `[fi]` or `[sgl]` extras (CUDA-only). Expected `host_ptr_identity True`.

### 3. Unit tests on the device

```bash
python -m pytest -q tests/utils/test_rocm_arch.py tests/kernels/test_rocm_launch_kwargs.py \
  tests/engine/test_attention_backend_arch.py tests/kernels/test_e4m3_compat.py tests/kernels/test_pinned_tensor.py \
  tests/moe/test_fused_copy.py tests/moe/test_fused_moe.py tests/kernels/test_triton_attention.py \
  tests/kernels/test_ggml.py tests/models/qwen4_exp/test_qsa_kernels.py tests/moe/test_offload.py
# moe_align (#687), incl. the unpatched real-device gate test
python -m pytest -q tests/kernels/test_moe_align.py
python -m pytest -q "tests/kernels/test_moe_align.py::test_dispatch_picks_correct_impl_for_real_device"
FREETOKEN_MOE_ALIGN_IMPL=triton python -m pytest -q "tests/kernels/test_moe_align.py::test_dispatch_picks_correct_impl_for_real_device"
# CPU / hybrid MoE (#764)
python -m pytest -q tests/moe/test_cpu_moe.py tests/moe/test_cpu_moe_fp8_block.py \
  tests/engine/test_moe_cpu_layers.py tests/moe/test_hybrid_fetch.py tests/moe/test_dsfp4_prequant.py
FREETOKEN_CPU_MOE_FLAG_SYNC=0 python -m pytest -q tests/moe/test_cpu_moe.py
# everything else
python -m pytest -q -m "not slow" tests
```

`tests/kernels/test_ggml.py` is the first real check that the vendored ggml-cuda HIP build compiles and is correct on gfx1151. The `FREETOKEN_MOE_ALIGN_IMPL=triton` run is expected to fail on Triton 3.8 (that is the miscompile #687 routes around); report whether it does.

### 4. Models

Run in this order; each on `ft serve --model <M> --text-model-only --max-running-requests 1 --enable-metrics-report --memory-ratio 0.8`. Ask the same prompts at temperature 0 (capital of Australia, 17*23, reverse a string in Python) and log prefill and decode tok/s, KV tokens and expert slots.

| # | Model | Path exercised |
|---|---|---|
| 1 | `Qwen/Qwen3-0.6B` | smoke: dense bf16, Triton attention, JIT kernels, graph capture |
| 2 | `google/gemma-4-12B-it-qat-q4_0-gguf` | dense GGUF through ggml-cuda HIP |
| 3 | `unsloth/Qwen3.6-35B-A3B-GGUF` (UD-Q4_K_M) | MoE GGUF with mixed K-quants, GDN |
| 4 | `RedHatAI/Qwen3.6-35B-A3B-NVFP4` | NVFP4 Triton MoE, watch prefill for C1 |
| 5 | `google/gemma-4-26B-A4B-it-qat-q4_0-gguf` | #260's second reference model |
| 6 | `Qwen/Qwen3.6-35B-A3B-FP8` | fp8-block experts, emulated e4m3 on HIP |
| 7 | `Qwen/Qwen3.8-27B-FP8` | dense fp8 per-tensor |
| 8 | `openai/gpt-oss-20b` | MXFP4 on the pure-Triton path |
| 9 | `gesong2077/GLM-4.5-Air-NVFP4` | large MoE, resident on unified memory |

Configs per model (B-D only when needed or for MoE):

| Config | Extra flags | When |
|---|---|---|
| A | none (`auto` picks `fused` on unified memory; graphs on) | always. The log must say `Unified-memory GPU detected; auto-selecting 'fused'` for MoE models |
| B | `--cuda-graph-max-bs 0` | if A fails during graph capture |
| C | `--moe-strategy offload --moe-cache-auto`, and once `--moe-strategy hybrid` | MoE models; greedy text must match A |
| D | `--skip-prefill-warmup` | only if startup dies in the prefill warmup |

For CPU/hybrid MoE (config C with `hybrid`, or `--moe-cpu-layers N`) check the startup log:

- Success: `CPU MoE executor ready: ... handshake=kernel`.
- Fallbacks (report which one): `cpu-moe kernel IO unavailable (...)`; `cpu-moe kernel IO graph probe failed (...); using eager decode`; `CPU MoE IO/handshake is not graph-safe on every TP rank for this dtype; disabling decode graphs`. On ROCm only bf16 activations are graph-safe, so a non-bf16 model always gets the last line.
- Repeat one hybrid run with `FREETOKEN_CPU_MOE_FLAG_SYNC=0` (host-callback sync): it must still produce the same greedy text.

### 5. Conditional fixes (port only when the symptom shows up)

| # | Symptom | What to do |
|---|---|---|
| C1 | `HSA_STATUS_ERROR_MEMORY_APERTURE_VIOLATION` or garbage in NVFP4 MoE prefill (model 4) | Report it with the log. Fix candidate: #260 `4fb00399`, route `fused_experts_nvfp4` to `fused_experts_decode_nvfp4_serial` on HIP (`moe/fused_nvfp4.py`) |
| C2 | Graph capture fails inside a GEMM (`hipErrorStreamCaptureUnsupported`, "error 900") | Retry with `TORCH_BLAS_PREFER_HIPBLASLT=0`, then with config B. Fix candidate: a HIP-only eager GEMM warmup before capture in `engine/graph.py::_capture_graphs` |
| C3 | Graph capture or process spawn fails with a tqdm / multiprocessing semaphore error | Report it. Fix candidate: HIP-gated `tqdm.set_lock(threading.RLock())` in `engine/graph.py` |
| C4 | Offload decode prints NaN or `!!!!` (config C only) | Not fixable here (flashlib `slot_cache.lru_ensure`). Use config A (`fused`) and report it |
| C5 | Triton `out of resource: shared memory` (64 KiB LDS) or a `tl.dot` lowering error with M < 16 | Report kernel name and traceback. Fix pattern: `kernel/triton/qsa/attend.py::_rocm_fit_tile` or a `block_h >= 16` clamp, HIP-gated |
| C6 | Building the prebuilt kernel cache (`freetoken-kernel-cache`, `kernel/aot.py::compile_and_package_kernels`) fails a static_assert on legacy fast_index_copy specs | Report it. Fix candidate: #260's `legacy_fast_index_copy_is_supported` filter (`kernel/aot.py`, `kernel/fast_index_copy.py`) |

### 6. What to report back

- Section 1 output (torch/HIP versions, `gcnArchName`, `is_integrated`, `mem_get_info` before and after model load), memory split used, kernel version.
- `host_ptr_identity` value.
- Unit tests: pass/fail counts per command, and the full traceback of every failure (attach the pytest log).
- Per model and config: pass/fail, the first error with traceback, the startup log (the MoE strategy line and, for CPU/hybrid, the `CPU MoE executor ready` or fallback line), prefill and decode tok/s, KV tokens and expert slots, and whether the answers to the three prompts are correct.
- Which of C1-C6 triggered.
