# FreeToken-ByAI (fork of FreeToken)

> **Looking for FreeToken itself?** For the installer, the desktop app and the official version,
> please go to **[FlashML-org/FreeToken](https://github.com/FlashML-org/FreeToken)**
> (downloads at [flashml.ai](https://www.flashml.ai/)). This repository is not the official
> project.

## What this fork is

This is a fork of [FlashML-org/FreeToken](https://github.com/FlashML-org/FreeToken). Its
`main` branch mirrors upstream `main` one to one; the work happens on the **`next`** branch.

`next` goes through the open upstream pull requests one by one, sorts them, and tentatively
merges the ones that look sensible. Where a pull request needs it, we add a follow-up commit
(a fixup or our own version of the change), and every decision is recorded with its reason in
[`fork/pr-decisions.json`](fork/pr-decisions.json) and
[`fork/pr-decisions.md`](fork/pr-decisions.md).

## What we only take

We only take pull requests that we can review properly **and** test ourselves. All checks run
on a single NVIDIA RTX 4090 (24 GB, sm_89) with 30 GB of system RAM under Linux, with these
models:

- `RadixArk/Qwen3.8-27B-NVFP4` (dense, hybrid attention)
- `RedHatAI/Qwen3.6-35B-A3B-NVFP4` (MoE, expert offload)
- `google/gemma-4-12B-it-qat-q4_0-gguf` (GGUF, sliding-window attention)
- `Qwen/Qwen3-0.6B` (quick server checks)

That is why this branch does **not** contain the ROCm patches, nor the patches for very large
cards or models (multi-GPU tensor parallelism, DeepSeek-V4, Kimi-K3, full GLM-5.3, ...), nor
patches for platforms we cannot run (Windows, macOS). Those are not judged as wrong: they wait
until they can be tested, or arrive through the upstream sync once upstream merges them.

Upstream pull requests not adopted on `next`:

<!-- fork:not-adopted:start -->
[#23](https://github.com/FlashML-org/FreeToken/pull/23), [#24](https://github.com/FlashML-org/FreeToken/pull/24), [#30](https://github.com/FlashML-org/FreeToken/pull/30), [#31](https://github.com/FlashML-org/FreeToken/pull/31), [#59](https://github.com/FlashML-org/FreeToken/pull/59), [#64](https://github.com/FlashML-org/FreeToken/pull/64), [#65](https://github.com/FlashML-org/FreeToken/pull/65), [#69](https://github.com/FlashML-org/FreeToken/pull/69), [#70](https://github.com/FlashML-org/FreeToken/pull/70), [#71](https://github.com/FlashML-org/FreeToken/pull/71), [#93](https://github.com/FlashML-org/FreeToken/pull/93), [#104](https://github.com/FlashML-org/FreeToken/pull/104), [#105](https://github.com/FlashML-org/FreeToken/pull/105), [#116](https://github.com/FlashML-org/FreeToken/pull/116), [#118](https://github.com/FlashML-org/FreeToken/pull/118), [#125](https://github.com/FlashML-org/FreeToken/pull/125), [#126](https://github.com/FlashML-org/FreeToken/pull/126), [#131](https://github.com/FlashML-org/FreeToken/pull/131), [#133](https://github.com/FlashML-org/FreeToken/pull/133), [#134](https://github.com/FlashML-org/FreeToken/pull/134), [#135](https://github.com/FlashML-org/FreeToken/pull/135), [#137](https://github.com/FlashML-org/FreeToken/pull/137), [#160](https://github.com/FlashML-org/FreeToken/pull/160), [#185](https://github.com/FlashML-org/FreeToken/pull/185), [#189](https://github.com/FlashML-org/FreeToken/pull/189), [#192](https://github.com/FlashML-org/FreeToken/pull/192), [#196](https://github.com/FlashML-org/FreeToken/pull/196), [#197](https://github.com/FlashML-org/FreeToken/pull/197), [#199](https://github.com/FlashML-org/FreeToken/pull/199), [#210](https://github.com/FlashML-org/FreeToken/pull/210), [#217](https://github.com/FlashML-org/FreeToken/pull/217), [#241](https://github.com/FlashML-org/FreeToken/pull/241), [#251](https://github.com/FlashML-org/FreeToken/pull/251), [#253](https://github.com/FlashML-org/FreeToken/pull/253), [#260](https://github.com/FlashML-org/FreeToken/pull/260), [#264](https://github.com/FlashML-org/FreeToken/pull/264), [#266](https://github.com/FlashML-org/FreeToken/pull/266), [#267](https://github.com/FlashML-org/FreeToken/pull/267), [#268](https://github.com/FlashML-org/FreeToken/pull/268), [#270](https://github.com/FlashML-org/FreeToken/pull/270), [#275](https://github.com/FlashML-org/FreeToken/pull/275), [#285](https://github.com/FlashML-org/FreeToken/pull/285), [#292](https://github.com/FlashML-org/FreeToken/pull/292), [#293](https://github.com/FlashML-org/FreeToken/pull/293), [#294](https://github.com/FlashML-org/FreeToken/pull/294), [#295](https://github.com/FlashML-org/FreeToken/pull/295), [#296](https://github.com/FlashML-org/FreeToken/pull/296), [#298](https://github.com/FlashML-org/FreeToken/pull/298), [#300](https://github.com/FlashML-org/FreeToken/pull/300), [#309](https://github.com/FlashML-org/FreeToken/pull/309), [#317](https://github.com/FlashML-org/FreeToken/pull/317), [#327](https://github.com/FlashML-org/FreeToken/pull/327), [#368](https://github.com/FlashML-org/FreeToken/pull/368), [#378](https://github.com/FlashML-org/FreeToken/pull/378), [#380](https://github.com/FlashML-org/FreeToken/pull/380), [#390](https://github.com/FlashML-org/FreeToken/pull/390), [#398](https://github.com/FlashML-org/FreeToken/pull/398), [#400](https://github.com/FlashML-org/FreeToken/pull/400), [#405](https://github.com/FlashML-org/FreeToken/pull/405), [#406](https://github.com/FlashML-org/FreeToken/pull/406), [#413](https://github.com/FlashML-org/FreeToken/pull/413), [#447](https://github.com/FlashML-org/FreeToken/pull/447), [#451](https://github.com/FlashML-org/FreeToken/pull/451), [#456](https://github.com/FlashML-org/FreeToken/pull/456), [#460](https://github.com/FlashML-org/FreeToken/pull/460), [#466](https://github.com/FlashML-org/FreeToken/pull/466), [#468](https://github.com/FlashML-org/FreeToken/pull/468), [#491](https://github.com/FlashML-org/FreeToken/pull/491), [#498](https://github.com/FlashML-org/FreeToken/pull/498), [#499](https://github.com/FlashML-org/FreeToken/pull/499), [#502](https://github.com/FlashML-org/FreeToken/pull/502), [#505](https://github.com/FlashML-org/FreeToken/pull/505), [#525](https://github.com/FlashML-org/FreeToken/pull/525), [#535](https://github.com/FlashML-org/FreeToken/pull/535), [#558](https://github.com/FlashML-org/FreeToken/pull/558), [#563](https://github.com/FlashML-org/FreeToken/pull/563), [#580](https://github.com/FlashML-org/FreeToken/pull/580), [#581](https://github.com/FlashML-org/FreeToken/pull/581), [#582](https://github.com/FlashML-org/FreeToken/pull/582), [#583](https://github.com/FlashML-org/FreeToken/pull/583), [#586](https://github.com/FlashML-org/FreeToken/pull/586), [#602](https://github.com/FlashML-org/FreeToken/pull/602), [#603](https://github.com/FlashML-org/FreeToken/pull/603)
<!-- fork:not-adopted:end -->

## Reviewed pull requests still open upstream

Generated from [`fork/pr-decisions.json`](fork/pr-decisions.json) and updated with every
review batch. "Our follow-up" names the fixup or reimplementation we added on top of a pull
request, and whether we offered it back upstream. Pull requests that upstream has merged or
closed drop out of these tables; the JSON keeps their decisions.

<!-- fork:pr-table:start -->
### Bug fixes we adopted (47)

| PR | Title | Status | Why | Our follow-up |
|---|---|---|---|---|
| [#593](https://github.com/FlashML-org/FreeToken/pull/593) | fix(checkpoint): refuse converting into a directory that already holds an FTW | Adopted + fixup | Converting into a directory that already holds an FTW overwrote shards under a stale index; now refused | Check runs before resolving the source, so an HF repo is not downloaded first ([7671a66](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/7671a66)) |
| [#592](https://github.com/FlashML-org/FreeToken/pull/592) | fix(mm): classify image fetch errors and re-check redirect targets | Adopted | Image fetch redirects now re-check --allowed-media-domains; 400 bodies no longer leak local paths or errno text |  |
| [#589](https://github.com/FlashML-org/FreeToken/pull/589) | fix(checkpoint): resolve HF repo Ids before conversion | Reimplemented | Converting from an HF repo id failed; ids are now resolved before conversion | Resolves inside convert_checkpoint, also fetches tokenizer/metadata files, with tests ([2d84a1d](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/2d84a1d)) |
| [#575](https://github.com/FlashML-org/FreeToken/pull/575) | fix(windows): build the extensions and JIT kernels with MSVC | Adopted | Builds the extensions and JIT kernels with MSVC on Windows; Linux device code unchanged |  |
| [#572](https://github.com/FlashML-org/FreeToken/pull/572) | fix(server): keep a silent stream alive and notice a client that left | Adopted | SSE keep-alive comments during long silent prefills, plus disconnect detection during the silence |  |
| [#565](https://github.com/FlashML-org/FreeToken/pull/565) | fix(ple): strict shard schema/geometry, nofollow + bounded discovery, mutation evidence, and pinned-bank admission/rollback | Reimplemented | PLE shard schema/geometry checks shared by both backends; pinned admission against host RAM with rollback | Builds on #334's memory helper; leaves out nofollow discovery and digest re-validation ([270b3a5](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/270b3a5)) |
| [#564](https://github.com/FlashML-org/FreeToken/pull/564) | fix(server): do not auto-select qwen3 parser for instruct-2507 | Adopted | --reasoning-parser auto no longer picks qwen3 for Instruct-2507 checkpoints (empty content) |  |
| [#562](https://github.com/FlashML-org/FreeToken/pull/562) | fix(engine): charge the attention workspace in moe-cache-auto sizing | Adopted + fixup | --moe-cache-auto now charges the attention backend's workspace, avoiding startup OOM at tight --memory-ratio | Runtime rebuild fit check (validate_rebuild) charges the workspace too ([ae16716](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/ae16716)) |
| [#559](https://github.com/FlashML-org/FreeToken/pull/559) | fix(kvcache): clone inserted radix keys to release request buffers | Adopted + fixup | Radix keys were views into whole request buffers, keeping large buffers alive; keys are now cloned | Adds the regression test across plain/SWA/hybrid caches ([d6aa64c](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/d6aa64c)) |
| [#531](https://github.com/FlashML-org/FreeToken/pull/531) | fix(server): clamp /v1/models context_length to the allocated KV pool | Adopted + fixup | /v1/models advertised the model ceiling instead of the allocated KV pool; context_length now clamped | Uses only the engine-reported page_size, with a test ([09bd83d](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/09bd83d)) |
| [#527](https://github.com/FlashML-org/FreeToken/pull/527) | fix(sampling): apply presence and frequency penalties | Reimplemented | API accepted presence/frequency penalties but ignored them; they are now applied | Counts rebuilt each step from generated tokens (overlap-safe), [-2, 2] enforced with 400, tests ([5a4987c](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/5a4987c)) |
| [#495](https://github.com/FlashML-org/FreeToken/pull/495) | fix(scheduler): wait for rank subscribers before first broadcast | Adopted | ZMQ slow-joiner race could drop a broadcast and hang TP ranks; rank 0 now waits for subscribers |  |
| [#494](https://github.com/FlashML-org/FreeToken/pull/494) | fix(gemma4): load mixed-quant GGUF checkpoints | Adopted | Mixed-quant Gemma-4 GGUFs failed to load; odd tensors are dequantized/repacked and per-expert strides passed |  |
| [#493](https://github.com/FlashML-org/FreeToken/pull/493) | fix(gemma4): load mixed compressed-tensors nvfp4 | Adopted + fixup | Gemma-4 compressed-tensors checkpoints mixing nvfp4 and unquantized tensors failed to load | Disk-tier family test excludes gemma4 from the static-spec check ([76e3300](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/76e3300)) |
| [#488](https://github.com/FlashML-org/FreeToken/pull/488) | fix(swa): keep the prompt head's windowed KV so fan-out can reuse a shared prefix | Adopted + fixup | With SWA the radix cache dropped a shared prompt head's windowed KV, so fan-out re-prefilled it | Stress test no longer hides the GPU from the whole pytest session ([6f18f27](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/6f18f27)) |
| [#487](https://github.com/FlashML-org/FreeToken/pull/487) | fix(server): hoist system messages to front for templates requiring system-first | Reimplemented | Qwen3.6+ templates raise on a later system message; system messages are now merged to the front | Renders as sent and only retries with system messages hoisted on a TemplateError ([d609fe6](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/d609fe6)) |
| [#475](https://github.com/FlashML-org/FreeToken/pull/475) | fix(tokenizer): respect explicit enable_thinking=false even when tools present | Adopted | Offering tools forced thinking on, overriding an explicit enable_thinking=false; now respected |  |
| [#464](https://github.com/FlashML-org/FreeToken/pull/464) | fix(scheduler): match stop strings with incremental decoding | Adopted + fixup | Stop strings spanning multi-token characters were missed; scheduler now matches the detokenizer's text | Adds five tests (four fail before) ([ea0b4c3](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/ea0b4c3)) |
| [#461](https://github.com/FlashML-org/FreeToken/pull/461) | fix(server): loopback-bind the TP rendezvous store, add --dist-port | Adopted + fixup | TP rendezvous store listened on all interfaces without auth; now bound to loopback, plus --dist-port | Windows keeps the previous store with a warning ([5157d7e](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/5157d7e)) |
| [#459](https://github.com/FlashML-org/FreeToken/pull/459) | fix(checkpoint): validate FTW v1 indexes eagerly | Adopted + fixup | FTW indexes are validated eagerly at open, raising FTWFormatError instead of failing deep in mmap/O_DIRECT | Gaps inside shards accepted (ftw_hotfix.py leaves them); overlaps still rejected ([d5dff2f](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/d5dff2f)) |
| [#440](https://github.com/FlashML-org/FreeToken/pull/440) | fix(models): build o_proj row-parallel in the remaining column-parallel families | Adopted | gemma4, qwen3_5_moe and muse_glimmer o_proj now row-parallel; replicated o_proj was wrong under TP>1 |  |
| [#439](https://github.com/FlashML-org/FreeToken/pull/439) | fix(scheduler): read the prefill chunk cap from the pool, not a snapshot | Adopted | Prefill chunk cap was a construction-time snapshot, so cache rebuilds never refreshed it; now re-read from the pool |  |
| [#435](https://github.com/FlashML-org/FreeToken/pull/435) | fix(server): resolve JSON Schema refs and union types in tool arguments | Adopted + fixup | Resolves JSON Schema $ref, type unions and anyOf/oneOf when typing tool-call arguments | Keeps the string default for untyped tool params; only unions and unresolved refs parse loosely ([13fcbdf](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/13fcbdf)) |
| [#430](https://github.com/FlashML-org/FreeToken/pull/430) | fix(glm4_moe): load compressed-tensors NVFP4 expert checkpoints | Adopted + fixup | glm4_moe expert reader only knew modelopt names, so compressed-tensors NVFP4 banks loaded scales without weights | Adds dialect tests and moves glm4_moe out of the static-spec test ([f88727c](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/f88727c)) |
| [#414](https://github.com/FlashML-org/FreeToken/pull/414) | fix(kernel): order the batch-memcpy probe against the current stream | Adopted | Batch-memcpy probe raced its zero-fill against the copy, silently disabling --moe-prefill-hit-d2d; now stream-ordered |  |
| [#412](https://github.com/FlashML-org/FreeToken/pull/412) | fix(bench): show how to use custom bandwidth profiles | Adopted | ft bench bw -o now prints the FREETOKEN_BENCHBW_PATH export needed for serving to read the custom profile |  |
| [#399](https://github.com/FlashML-org/FreeToken/pull/399) | fix(cpu-moe): honor padded fp8 scale strides, add avx512f tier and float64 parity (builds on #36) | Adopted | Adds block-FP8 CPU expert GEMV (from #36) with padded scale strides, an avx512f tier and float64 parity tests |  |
| [#359](https://github.com/FlashML-org/FreeToken/pull/359) | fix(gemma4): support dense Gemma-4 GGUF checkpoints | Adopted + fixup | Dense Gemma-4 GGUF checkpoints failed to parse/load; expert fields now default to 0 | Native-quant swap and offload assertion fixed for dense GGUF; conflict with #494 resolved ([7f2fc79](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/7f2fc79)); offered upstream (candidate, see fork/upstream-candidates.md) |
| [#346](https://github.com/FlashML-org/FreeToken/pull/346) | fix(server): stop gemma4 tool-call markers leaking into content | Adopted + fixup | Partial or malformed Gemma-4 tool-call markers leaked into content; a scrub hook now strips them | A closed unparseable block is dropped whole, so the text after it is kept ([737e04e](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/737e04e)) |
| [#334](https://github.com/FlashML-org/FreeToken/pull/334) | fix(memory): honor cgroup memory limits when sizing expert banks | Reimplemented | Loader sized expert banks against host MemAvailable, so containers were OOM-killed; cgroup limits now honored | ~90-line version: clamps to the tightest cgroup v2/v1 limit and counts inactive_file as free ([106a2b8](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/106a2b8)) |
| [#316](https://github.com/FlashML-org/FreeToken/pull/316) | fix(rocm): avoid indirect host pointers during HIP graph capture | Adopted + fixup | Under HIP graph capture the fused expert copy lost its host mappings; now falls back to per-bank copies on ROCm | Test stub given next's _disk_tier attribute ([8c1f4fe](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/8c1f4fe)) |
| [#315](https://github.com/FlashML-org/FreeToken/pull/315) | Fix GGUF user-defined token atomicity | Adopted | GGUF user-defined tokens (e.g. <think>) were split into subwords; now re-added as atomic tokens when needed |  |
| [#278](https://github.com/FlashML-org/FreeToken/pull/278) | fix(moe): match the benchbw verdict to the served model's expert size | Adopted | Offload-vs-hybrid pick used one bench verdict per expert format for all models; now matched to the model's expert size |  |
| [#245](https://github.com/FlashML-org/FreeToken/pull/245) | fix(engine): handle torch 2.9 allocator API deprecation | Reimplemented | torch deprecates _set_allocator_settings (used for expandable segments); now uses the replacement API | Uses torch._C._accelerator_setAllocatorSettings with the old call as fallback (PR's API missing in 2.11) ([36a467b](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/36a467b)) |
| [#233](https://github.com/FlashML-org/FreeToken/pull/233) | fix(engine): probe the real WSL pin budget instead of guessing 40% RAM | Reimplemented | WSL refuses pinning well below the 40%-of-RAM guess, so loads died; the pin budget is now probed | Probes up to the old estimate via the pinned extension, returns 0 when nothing pins, cached ([d792900](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/d792900)) |
| [#223](https://github.com/FlashML-org/FreeToken/pull/223) | fix(server): validate sampling params and rebuild timeout at the API layer | Adopted | Invalid sampling params (temperature<0, top_p, top_k=0, non-finite) now return 400; rebuild timeout is bounded |  |
| [#222](https://github.com/FlashML-org/FreeToken/pull/222) | fix(server): guarantee AbortMsg delivery on stream cancellation | Adopted + fixup | Abort is now delivered from the stream's finally and non-streaming requests are watched for disconnects | Request-ring and --api-key middlewares made pure ASGI so disconnects reach the handler ([f8de64f](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/f8de64f)); offered upstream (candidate, see fork/upstream-candidates.md) |
| [#221](https://github.com/FlashML-org/FreeToken/pull/221) | fix(daemon): harden /bench/run child lifecycle, bound request models | Adopted + fixup | Client disconnect left the /bench/run child running; now torn down via its process group; request ports bounded | Windows lacks os.killpg; the child is stopped directly there (test added) ([275590e](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/275590e)) |
| [#211](https://github.com/FlashML-org/FreeToken/pull/211) | fix(gguf): chunk the moe_vec z grid past the 65535 cap | Adopted | GGUF MoE GEMV put tokens*top_k on gridDim.z (cap 65535), so large prefills failed; z is now chunked with an offset |  |
| [#198](https://github.com/FlashML-org/FreeToken/pull/198) | fix(engine): reserve explicit KV pages during MoE auto-sizing | Reimplemented | Expert cache took the memory needed by forced KV pages (--num-pages/--num-tokens with --moe-cache-auto) | KV floor applied in the shared plan_moe_cache_auto (engine and ft info), with a test ([a73f98f](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/a73f98f)) |
| [#190](https://github.com/FlashML-org/FreeToken/pull/190) | fix(gemma4-gguf): accept scalar attention.head_count_kv | Adopted + fixup | Gemma-4 GGUF parser crashed when llama.cpp writes attention.head_count_kv as a scalar; now normalised to a per-layer list | Adds the missing test (fails before) ([f1b0ccf](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/f1b0ccf)) |
| [#177](https://github.com/FlashML-org/FreeToken/pull/177) | fix(attention): map grouped decode heads to KV groups | Adopted | Triton grouped decode kernel used the wrong KV head for GQA groups spanning a partial 16-head tile; blocks now per KV group |  |
| [#169](https://github.com/FlashML-org/FreeToken/pull/169) | fix(engine): load prefill triton kernels at startup, not mid-request | Adopted | Prefill Triton kernels loaded mid-request; warmup now runs on every backend over a length ladder, plus --skip-prefill-warmup |  |
| [#159](https://github.com/FlashML-org/FreeToken/pull/159) | fix(kernel): GGUF JIT extension fails to build with gcc under C++17 - compile as C++20 | Adopted | GGUF JIT extension failed to build with some g++ versions under C++17; now compiled as C++20 (CUDA branch) |  |
| [#153](https://github.com/FlashML-org/FreeToken/pull/153) | fix(bench): skip an unsupported slot count instead of aborting the sweep | Adopted | bench_offload_cache_copy skips a geometry the cache refuses instead of aborting; exits 1 if a requested one measured nothing |  |
| [#144](https://github.com/FlashML-org/FreeToken/pull/144) | fix(kernel): clear the latched CUDA error before raising in pinned_tensor | Adopted | A refused pin left the CUDA error latched, breaking the next unrelated CUDA call; the error is now cleared before raising |  |
| [#88](https://github.com/FlashML-org/FreeToken/pull/88) | Fix: minor issue of tqdm lock leak during termination with TP | Adopted | Scheduler uses a threading.RLock for tqdm instead of a multiprocessing semaphore that could leak at TP termination |  |

### Improvements we adopted (37)

| PR | Title | Status | Why | Our follow-up |
|---|---|---|---|---|
| [#596](https://github.com/FlashML-org/FreeToken/pull/596) | feat(engine): --embed-device cpu keeps the input embedding in RAM | Our own PR | Input embedding table in pinned host RAM: +75k tokens of context on the 27B (our own PR to upstream) | our own upstream PR |
| [#595](https://github.com/FlashML-org/FreeToken/pull/595) | feat(server): add ft info and a pre-load memory preflight | Our own PR | Forecasts GPU memory and fit before loading (ft info); ft serve refuses configs that cannot fit (our own PR to upstream) | our own upstream PR |
| [#594](https://github.com/FlashML-org/FreeToken/pull/594) | feat(qwen4_exp): support ModelOpt QAD checkpoints (NVFP4 PLE tables, MXFP8 dense) | Adopted + fixup | Loads qwen4_exp ModelOpt QAD checkpoints: NVFP4-packed PLE tables and MXFP8 dense scales | Scan checks row count against the n-gram config; cuda gather oob test indexes per row ([a2b4fe2](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/a2b4fe2)) |
| [#591](https://github.com/FlashML-org/FreeToken/pull/591) | perf(moe): fold the shared-expert gate epilogue into hc_combine_norm | Reimplemented | Folds the shared-expert gate epilogue into hc_combine_norm (stacked on #590) | Passes shared/gate explicitly and links each layer to its consumer norm ([f965dfa](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/f965dfa)) |
| [#590](https://github.com/FlashML-org/FreeToken/pull/590) | perf(model): fuse hc combine with the next block's RMSNorm via hc_combine_norm | Reimplemented | Fuses the hc combine with the next block's RMSNorm, one launch fewer per block | Both kernels share one _gemma_rmsnorm helper so they match by construction; added tests ([f965dfa](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/f965dfa)) |
| [#587](https://github.com/FlashML-org/FreeToken/pull/587) | feat(rocm): run on RDNA3/RDNA4 with torch 2.14/2.15 and ROCm 7.14/10 | Reimplemented | Adds ROCm support for RDNA3/RDNA4 with torch 2.14/2.15 and ROCm 7.14/10 | CUDA pins untouched, C++20 only for ROCm torch>=2.14, functional memop check with fallback ([c362171](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/c362171)) |
| [#585](https://github.com/FlashML-org/FreeToken/pull/585) | perf(linear): run a single-row bf16 projection as one GEMV | Reimplemented | Runs a single-row bf16 projection as one GEMV, a decode bs=1 bandwidth win | NVIDIA-only, >=512 out features, opt-out via linear.none=torch, covers the tied LM head ([8b1e34d](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/8b1e34d)) |
| [#578](https://github.com/FlashML-org/FreeToken/pull/578) | perf(moe): dequant nvfp4 prefill experts by bit placement and load activations contiguously | Adopted | NVFP4 MoE prefill experts dequantized by bit placement, ~6x faster GEMM with bit-identical output |  |
| [#577](https://github.com/FlashML-org/FreeToken/pull/577) | feat(kvcache): keep prefill-chunk GDN checkpoints in a pinned host bank | Adopted | Hybrid GDN prompts diverging before the last chunk re-prefilled from token 0; opt-in pinned bank keeps per-chunk checkpoints |  |
| [#574](https://github.com/FlashML-org/FreeToken/pull/574) | feat(engine): --vram-reserve-mb keeps VRAM free at the largest prefill | Adopted | Adds opt-in --vram-reserve-mb: measures the real prefill peak and shrinks the expert cache to keep VRAM free |  |
| [#553](https://github.com/FlashML-org/FreeToken/pull/553) | feat(server): publish cumulative prefill and decode timing on /v1/stats | Adopted | Publishes cumulative prefill/decode timing on /v1/stats so pollers can compute tok/s |  |
| [#551](https://github.com/FlashML-org/FreeToken/pull/551) | improve installation success rate with higher timeout and retries | Adopted + fixup | Raises uv HTTP timeout and retries to fix installer timeouts on slow links | Values are defaults, so a user-set UV_HTTP_TIMEOUT still wins ([4377773](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/4377773)) |
| [#507](https://github.com/FlashML-org/FreeToken/pull/507) | feat(glm5_next): serve GLM-5.3-Flash with tensor parallelism | Adopted + fixup | Adds tensor parallelism for glm5_next (GLM-5.3-Flash); TP=1 paths unchanged | TP test fixture given num_key_value_heads for transformers 5.16 ([8d1bb61](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/8d1bb61)) |
| [#504](https://github.com/FlashML-org/FreeToken/pull/504) | feat(server): serve per-request inference metrics under --enable-metrics-report | Adopted + fixup | Adds opt-in per-request TTFT/prefill/decode metrics (--enable-metrics-report) on chat, messages and responses | Abort test stub given the new _prefill_start map ([361ef5a](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/361ef5a)) |
| [#500](https://github.com/FlashML-org/FreeToken/pull/500) | perf(moe): single-launch prefill buffer invalidation without hidden sync | Adopted + fixup | Prefill buffer invalidation is now a single launch without a hidden host sync | Trimmed comments to the repo's style ([58cd469](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/58cd469)) |
| [#484](https://github.com/FlashML-org/FreeToken/pull/484) | feat(scheduler): interleave decode steps into long prefill runs | Adopted | Adds opt-in --decode-interleave-every N so long chunked prefills no longer stall in-flight decodes |  |
| [#477](https://github.com/FlashML-org/FreeToken/pull/477) | feat(server): expose POST /v1/tokenize endpoint for client-side token counting | Adopted + fixup | Adds POST /v1/tokenize for client-side token counting | Messages path converted via chat_request_to_genspec so counts match usage; invalid body is 400 ([11d040f](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/11d040f)) |
| [#476](https://github.com/FlashML-org/FreeToken/pull/476) | feat(server): add --default-thinking-mode flag for server-wide thinking default | Adopted + fixup | Adds --default-thinking-mode for a server-wide thinking default when clients send none | Default applies last, so per-request reasoning_effort/thinking settings still win ([a1ac14b](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/a1ac14b)) |
| [#429](https://github.com/FlashML-org/FreeToken/pull/429) | qwen4_exp: build o_proj row-parallel, as every other family does | Adopted | qwen4_exp o_proj is now row-parallel; replicated o_proj would skip the all-reduce under TP>1 |  |
| [#408](https://github.com/FlashML-org/FreeToken/pull/408) | feat(kvcache): add nvfp4 kv quantization | Adopted + fixup | Adds nvfp4 KV cache on top of #354: 3.46x the bf16 KV tokens, opt-in (~15% slower decode at 8k) | kv_row_bytes sizes the packed row instead of raising 'unknown kv_quant' ([53a72b0](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/53a72b0)) |
| [#354](https://github.com/FlashML-org/FreeToken/pull/354) | feat(kvcache): store the KV cache as fp8 e4m3 codes (--kv-cache-dtype fp8) | Adopted + fixup | Adds fp8 e4m3 KV cache (--kv-cache-dtype fp8) with per-token/head scales; roughly doubles KV capacity on the 27B | Test doubles for newer attributes, a one-ulp tolerance on sm_89, docs say MLA/DSA is covered ([8f00988](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/8f00988), [194b137](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/194b137), [61a16c9](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/61a16c9)) |
| [#341](https://github.com/FlashML-org/FreeToken/pull/341) | feat(bench): add reproducible serving performance harness | Adopted + fixup | Adds a reproducible client-side serving benchmark (TTFT, decode, prefix-cache cases) for a running server | Sends --api-key as bearer; treats a missing prompt_tokens_details as a cache miss ([b36d49d](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/b36d49d), [23d92b6](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/23d92b6)); offered upstream (candidate, see fork/upstream-candidates.md) |
| [#337](https://github.com/FlashML-org/FreeToken/pull/337) | feat(moe): NVMe disk tier for MoE expert banks | Adopted + fixup | Adds opt-in NVMe disk tier (--moe-disk-tier) so expert banks larger than host RAM can run | Windows mmap flags, empty-bank pin_prefix, and a stale family test fixed ([4d2fa42](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/4d2fa42)) |
| [#305](https://github.com/FlashML-org/FreeToken/pull/305) | feat(server): add --api-key bearer authentication | Adopted | Adds --api-key bearer authentication (tests, docs, CORS preflight, shell client sends the key) |  |
| [#258](https://github.com/FlashML-org/FreeToken/pull/258) | feat(dflash): support dflash | Adopted + fixup | Speculative decoding with DFlash drafts; with our DFlash2 support and fixes the 27B decodes 2.5-4.4x faster (and batches concurrent requests), the offloaded Qwen3.6 MoE ~2x on code and math | DFlash2 drafts and an fp8 draft option; triton and FlashInfer verify graphs (fp8 and bf16 KV); the per-request KV page leak fixed and the integrity check back on; one target forward per cycle instead of two; prefix reuse with a windowed draft context; the GDN commit replays the recurrence (no per-token verify states); verify graphs for an offloaded MoE; a gate that measures plain decode; logprobs on multi-token steps; ft info prices draft, context and verify buffers; batched speculation for several decoding requests ([99a2093](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/99a2093), [d16bc96](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/d16bc96), [9a3714d](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/9a3714d), [4c03cb7](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/4c03cb7), [7c19c2e](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/7c19c2e), [4b05651](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/4b05651), [e214732](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/e214732), [4364741](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/4364741), [b498b6d](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/b498b6d), [f86a265](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/f86a265), [c1acd76](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/c1acd76), [8a31b70](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/8a31b70), [1459aa8](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/1459aa8), [aff024c](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/aff024c), [0a56c36](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/0a56c36), [ff4d485](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/ff4d485), [24d779b](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/24d779b), [da10591](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/da10591), [dbd8d0e](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/dbd8d0e), [57efe5c](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/57efe5c), [bbccd0c](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/bbccd0c), [a876274](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/a876274), [592a471](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/592a471)) |
| [#254](https://github.com/FlashML-org/FreeToken/pull/254) | feat(bench): pass ft serve options through '--' in bench_decode_moe | Adopted | bench_decode_moe now passes ft serve options through '--' instead of mirroring server flags |  |
| [#231](https://github.com/FlashML-org/FreeToken/pull/231) | feat(moe): --moe-collect-stats, so expert-cache behaviour is measurable | Adopted | Adds --moe-collect-stats: logs expert-cache miss rate, worst layers and a routing oracle bound |  |
| [#230](https://github.com/FlashML-org/FreeToken/pull/230) | feat(server): add TLS certificate support | Adopted | Adds --ssl-certfile/--ssl-keyfile for serving over HTTPS via uvicorn |  |
| [#224](https://github.com/FlashML-org/FreeToken/pull/224) | feat(server): OpenAI-compatible logprobs for chat and legacy completions | Adopted | Adds OpenAI-compatible logprobs/top_logprobs for chat and legacy completions (400 when a parser would hide tokens) |  |
| [#191](https://github.com/FlashML-org/FreeToken/pull/191) | refactor(server): dedupe maintenance gate across API entrypoints | Adopted | Moves duplicated maintenance 503 gate into server/maintenance.py so all API entrypoints answer consistently |  |
| [#154](https://github.com/FlashML-org/FreeToken/pull/154) | GGUF: read multi-shard checkpoints | Adopted | Split multi-shard GGUFs were unopenable; the reader now resolves the shard set and aggregates tensor tables |  |
| [#145](https://github.com/FlashML-org/FreeToken/pull/145) | test(e2e): let the cache-rebuild gate run on reasoning checkpoints | Adopted | Cache-rebuild e2e test checked reply text, which reasoning models put in reasoning_content; now checks completion_tokens |  |
| [#138](https://github.com/FlashML-org/FreeToken/pull/138) | GGUF kernels: raise on unsupported quant type instead of returning uninitialized memory | Adopted | GGUF kernel dispatchers returned uninitialized memory on an unknown quant type; they now raise with the supported list |  |
| [#109](https://github.com/FlashML-org/FreeToken/pull/109) | feat(server): expose swa_full_tokens_ratio as a startup CLI flag | Adopted | Adds --swa-full-tokens-ratio to size the SWA window pool at load, not only via /v1/cache/rebuild |  |
| [#108](https://github.com/FlashML-org/FreeToken/pull/108) | feat(server): Add OpenAI /v1/models/{model_id} endpoint | Adopted | Adds OpenAI-compatible GET /v1/models/{model_id} for clients that validate a model name (404 for unknown names) |  |
| [#90](https://github.com/FlashML-org/FreeToken/pull/90) | docs(install): document NCCL dev libraries for multi-GPU tensor parallelism | Adopted | Documents libnccl-dev: the pynccl JIT links with -lnccl, so the first TP launch failed at link time without it |  |
| [#56](https://github.com/FlashML-org/FreeToken/pull/56) | kernel: clamp zero-size host registrations; WDDM lock-pool hint on pin failure | Reimplemented | Empty expert banks failed to allocate; now an empty bank gets one block, an empty tensor and device_ptr()=0 | Own fix at the mmap level (0-byte mmap fails before host_register); RLIMIT_MEMLOCK hint dropped ([a433799](https://github.com/KarrAcaRn/FreeToken-ByAI/commit/a433799)) |

### Not adopted (83)

| PR | Title | Status | Why |
|---|---|---|---|
| [#498](https://github.com/FlashML-org/FreeToken/pull/498) | feat(qwen4_exp): support channel-wise fp8 dense weights and per-row PLE loaders | Rejected | Special-case loaders for one non-standard checkpoint dialect; conflicts with #594's PLE/dense rework |
| [#468](https://github.com/FlashML-org/FreeToken/pull/468) | fix(engine): reject fa attention backend below sm_90 at config time | Rejected | Refuted: fa backend works on sm_89 (RTX 4090); the gate would block a working backend on Ada |
| [#466](https://github.com/FlashML-org/FreeToken/pull/466) | fix(utils): tolerate coalesced msgpack frames in zmq pull queues | Rejected | Masks a likely sender-side race instead of fixing it; partial frames still crash; Windows-only, not reproducible |
| [#456](https://github.com/FlashML-org/FreeToken/pull/456) | Lowvram 4gb | Rejected | Built on an old main, would revert much current code, adds debug prints and AI logs; CPU embedding planned as our own |
| [#451](https://github.com/FlashML-org/FreeToken/pull/451) | docs(moe): report shared expert banks across replicas | Rejected | Documents a shared-bank experiment relying on an external shim not in the repo; FreeToken does not contain it |
| [#398](https://github.com/FlashML-org/FreeToken/pull/398) | feat(kvcache): add ISO3/ISO4 KV-cache quantization (--kv-cache-iso) | Rejected | ISO3/ISO4 KV produce garbage on Qwen3-0.6B, ~7x slower 8k decode, full attention only, ~1k lines of custom CUDA |
| [#380](https://github.com/FlashML-org/FreeToken/pull/380) | ci(container): настроить сборку образа | Rejected | Image publishing is upstream infrastructure the fork does not need; documented command fails (no --host 0.0.0.0) |
| [#327](https://github.com/FlashML-org/FreeToken/pull/327) | Feat/native gguf llama | Rejected | Fails to load a standard Llama GGUF, caps context at 8192, ignores Llama 3 rope scaling, no tests |
| [#295](https://github.com/FlashML-org/FreeToken/pull/295) | Add Docker container capability | Rejected | Image installs freetoken from PyPI, not the checkout, so fork changes are missing; claims unsupported Pascal GPUs |
| [#266](https://github.com/FlashML-org/FreeToken/pull/266) | fix(server): hide qwen transport markers from semantic responses | Rejected | Quote-heuristic text filter for Qwen markers, no reproduction; an exact token-level fix would be smaller |
| [#264](https://github.com/FlashML-org/FreeToken/pull/264) | fix(build): honor explicit and versioned CUDA toolkits | Rejected | Requires nvcc minor version to match torch, refusing working setups (13.1 vs cu130); #132's major-only check suffices |
| [#253](https://github.com/FlashML-org/FreeToken/pull/253) | feat(sm70): support Volta / Tesla V100 via torch 2.10 cu128 downgrade | Rejected | Downgrades the whole stack to torch 2.10/cu128 for V100; would drop native kernels on newer GPUs |
| [#251](https://github.com/FlashML-org/FreeToken/pull/251) | add a dockerfile ( based-cuda ) | Rejected | Image clones upstream instead of the checkout, runs a nonexistent module (ft) and does not bind 0.0.0.0 |
| [#192](https://github.com/FlashML-org/FreeToken/pull/192) | demo: intentionally duplicate maintenance gate (radar fixture) | Rejected | Deliberate code duplication as a fixture for an external radar tool; #191 dedupes the gate instead |
| [#160](https://github.com/FlashML-org/FreeToken/pull/160) | cpu-device: OR-switch device resolver + RoPE multi-head fallback fix | Rejected | Drops csrc from package-data, but GGUF and other JIT kernels compile from it at runtime; wheel installs would break |
| [#126](https://github.com/FlashML-org/FreeToken/pull/126) | Add fp8 KV-cache quantization (--kv-dtype) | Rejected | Fixed fp8 scale 1.0 ignores checkpoint scales and yields NaN (garbage on Qwen3-0.6B); MHA + fi only, no tests |
| [#125](https://github.com/FlashML-org/FreeToken/pull/125) | test(pinned): use mapped memory for UVA pointer check | Rejected | Not reproducible: next's pageable-pointer check passes on CUDA 13.2; dropping the assertion only loses coverage |
| [#558](https://github.com/FlashML-org/FreeToken/pull/558) | feat(server): --api-key flag for bearer token auth on the HTTP API | Superseded | Already covered by #305 (more complete --api-key) |
| [#505](https://github.com/FlashML-org/FreeToken/pull/505) | fix(scheduler): preserve pending hybrid checkpoint across prefill chunks | Superseded | Already covered by #577, which contains this fix verbatim |
| [#405](https://github.com/FlashML-org/FreeToken/pull/405) | fix(models): serve qwen4_exp FTW checkpoints with PLE streamed from source | Superseded | Already covered by #420 (converter writes the PLE table; ftw_hotfix.py adds it to older FTWs) |
| [#390](https://github.com/FlashML-org/FreeToken/pull/390) | fix(models): better support for mixed-precision compressed-tensors NVFP4 | Superseded | Already covered by #438 (QuantConfig reader); next's tests cover these mixed-precision layouts |
| [#368](https://github.com/FlashML-org/FreeToken/pull/368) | feat(gguf): implement Q8_0 dequantization | Superseded | Already covered by #494, which dequantizes Q8_0 and all GGML types via the gguf reference dequantizer |
| [#309](https://github.com/FlashML-org/FreeToken/pull/309) | feat(kvcache): add reliable quantized KV cache | Superseded | Already covered by #354 + #408; this one crashed fp8 at graph capture and degraded q4_0 |
| [#296](https://github.com/FlashML-org/FreeToken/pull/296) | feat(qwen3_5_moe): support compressed-tensors NVFP4 experts with block-fp8 dense side | Superseded | Already covered by #438 (QuantConfig reader); next's tests include this layout (ct_block_moe) |
| [#294](https://github.com/FlashML-org/FreeToken/pull/294) | fix(qwen3_5_moe): detect shared-expert quant for modelopt mixed checkpoints | Superseded | Already covered by #438 (QuantConfig reader); next's tests include this layout (modelopt_mixed_fp8_shared) |
| [#292](https://github.com/FlashML-org/FreeToken/pull/292) | feat: support GLM-5.3-Flash NVFP4 | Superseded | Already covered by #507 (upstream GLM-5.3-Flash support); provisioning scripts out of scope |
| [#285](https://github.com/FlashML-org/FreeToken/pull/285) | Fix/windows serving | Superseded | KV-quant core covered by #354 + #408, MSVC build by #575; remaining Windows fixes would need separate PRs |
| [#275](https://github.com/FlashML-org/FreeToken/pull/275) | fix: [BUG] qwen3_5 dense: mixed-precision NVFP4 crashes in ct_bf16_fuse (Float8 × BFloat16 promotion) | Superseded | Already covered by #438 (QuantConfig reader); next's tests include this layout (ct_mixed_dense) |
| [#270](https://github.com/FlashML-org/FreeToken/pull/270) | glm5_next: support GLM-5.3-Flash (hybrid KDA + DSA, mHC, NVFP4 expert offload) | Superseded | Already covered by #507 (upstream GLM-5.3-Flash support) and #479 (image input) |
| [#268](https://github.com/FlashML-org/FreeToken/pull/268) | feat(kvcache): sub-byte Q4_0 and Q6_0 KV cache quantization | Superseded | Already covered by #354 + #408 (earlier version of #309's sub-byte KV work) |
| [#185](https://github.com/FlashML-org/FreeToken/pull/185) | fix(kernel): launch GGUF MoE GEMV token axis on grid.x, not grid.z | Superseded | Already covered by #211 (chunks the moe_vec z grid past the 65535 cap); this PR's test passes on next |
| [#64](https://github.com/FlashML-org/FreeToken/pull/64) | gemma4/gguf: accept a scalar attention.head_count_kv | Superseded | Already covered by #190 (same scalar head_count_kv fix), adopted with a test |
| [#23](https://github.com/FlashML-org/FreeToken/pull/23) | feat: add simple ROCm GPU support for RDNA3 (gfx1100-1103) | Superseded | Already covered by #132 (RDNA3/RDNA4 ROCm runtime foundation): is_rocm, gfx arch detection, HIP flags and hip_compat.h on next |
| [#118](https://github.com/FlashML-org/FreeToken/pull/118) | fix(scheduler): clamp admission to the actual KV pool so oversized prompts fail loudly | Obsolete | next's max_seq_len already is min(context, KV tokens); oversized prompts get an immediate HTTP 400 |
| [#31](https://github.com/FlashML-org/FreeToken/pull/31) | fix: preload dense NVFP4 decode kernels before graph capture | Obsolete | Targets Nvfp4DenseLinear classes next no longer has (#418); late-load stall does not show on the RTX 4090 (~27 s capture) |
| [#267](https://github.com/FlashML-org/FreeToken/pull/267) | Add loopback runtime process identity endpoint | Feature, later | Sound, unused in this fork for now; adopt when needed |
| [#603](https://github.com/FlashML-org/FreeToken/pull/603) | feat(deepseek-v41): support text and vision serving | Deferred | DeepSeek-V4.1 too large for this machine; maintainer branch, expected to land upstream (8 conflicts with next) |
| [#602](https://github.com/FlashML-org/FreeToken/pull/602) | fix(moe): fit Qwen3.8 Flash Next FP8 banks across host and GPU memory | Deferred | FP8 expert layers kept in VRAM when host RAM is short; deferred - the FP8 model and RAM shortage cannot be reproduced here |
| [#586](https://github.com/FlashML-org/FreeToken/pull/586) | refactor(hf): merge an override into the section's own dict, with no fallback [draft] | Deferred | Draft - revisit when ready |
| [#583](https://github.com/FlashML-org/FreeToken/pull/583) | docs(gpu): name the NVML free-memory read in gpu_select, and the platform the test fakes [draft] | Deferred | Draft - revisit when ready; Windows cannot be tested here |
| [#582](https://github.com/FlashML-org/FreeToken/pull/582) | test(quant): skip declined local checkpoints and label cache paths portably [draft] | Deferred | Draft - revisit when ready |
| [#581](https://github.com/FlashML-org/FreeToken/pull/581) | test(checkpoint): read an FTW checkpoint through the mmap path [draft] | Deferred | Draft - revisit when ready; Windows cannot be tested here |
| [#580](https://github.com/FlashML-org/FreeToken/pull/580) | fix(windows): stop on backend death through the server's own SIGTERM handler [draft] | Deferred | Draft - revisit when ready; Windows cannot be tested here |
| [#563](https://github.com/FlashML-org/FreeToken/pull/563) | feat(moe): pin hot experts so fp8 qwen3.8-flash-next serves on a 48gb card | Deferred | User's call: own project later (9.4k lines, not opt-in, conflicts with #337); ideally with GPU test setup |
| [#535](https://github.com/FlashML-org/FreeToken/pull/535) | ci(rocm): add ROCm 10.0.0 Dockerfile and validation workflow | Deferred | Needs upstream's self-hosted ROCm runner and unadopted ROCm PRs; revisit with #217 |
| [#525](https://github.com/FlashML-org/FreeToken/pull/525) | feat(kvcache): host-resident prefix tier for hybrid GDN models (snapshots + KV pages) | Deferred | Stacked on #499 |
| [#502](https://github.com/FlashML-org/FreeToken/pull/502) | feat(deepseek_v4): serve image input on the V4-Flash-Vision release | Deferred | DeepSeek-V4 too large for this machine; reworks shared mm code, needs careful review |
| [#499](https://github.com/FlashML-org/FreeToken/pull/499) | feat(kvcache): host-RAM KV tier for sparse-attention models (--kv-host-pages) | Deferred | fp8 parts already on main via #354; host-RAM KV tier serves only Flash-Next, untested, cannot run here |
| [#491](https://github.com/FlashML-org/FreeToken/pull/491) | refactor(moe): extract hybrid decode orchestration [draft] | Deferred | Draft - revisit when ready |
| [#460](https://github.com/FlashML-org/FreeToken/pull/460) | feat(models): support deepseek v4.1 with native fp8-fp4 kv storage | Deferred | DeepSeek-V4.1 too large for this machine |
| [#447](https://github.com/FlashML-org/FreeToken/pull/447) | feat(moe): owner-local expert parallelism and tensor parallelism | Deferred | Needs multi-GPU and Flash-Next weights, neither available here |
| [#413](https://github.com/FlashML-org/FreeToken/pull/413) | fix(models): support llm-compressor NVFP4 MoE export variants | Deferred | Needs reimplementation on the QuantConfig layers (#418/#438, conflicts in all files); needs a real export to test |
| [#406](https://github.com/FlashML-org/FreeToken/pull/406) | docs(models): qualify full GLM-5.3 on H200 Serverless | Deferred | GLM-5.3 too large for this machine |
| [#400](https://github.com/FlashML-org/FreeToken/pull/400) | plan(rocm): unified gfx1100 MoE optimization plan [draft] | Deferred | Draft - revisit when ready; ROCm cannot be tested here |
| [#378](https://github.com/FlashML-org/FreeToken/pull/378) | fix(rocm): make CPU MoE graph replay safe [draft] | Deferred | Draft - revisit when ready; ROCm cannot be tested here |
| [#317](https://github.com/FlashML-org/FreeToken/pull/317) | fix(ftw): preserve auxiliary expert banks | Deferred | Stacked on #260 |
| [#300](https://github.com/FlashML-org/FreeToken/pull/300) | feat: Automatic KV/MoE Laddering for decode speed vs context-length trade off ( upto 33% faster decode )  | Deferred | Needs rework on next (uses renamed moe_backend kwarg, conflicts, no tests); revisit with the MoE work |
| [#298](https://github.com/FlashML-org/FreeToken/pull/298) | Support poolside/Laguna-S-2.1-NVFP4, and fix serving from source on Windows | Deferred | Laguna model too large and Windows not testable here; should be split into two PRs |
| [#293](https://github.com/FlashML-org/FreeToken/pull/293) | fix(qwen4_exp): fix NVFP4 FTW weight loading, QSA indexer, and PLE tables [draft] | Deferred | Draft - revisit when ready; Flash-Next cannot run here |
| [#260](https://github.com/FlashML-org/FreeToken/pull/260) | ROCm: validate native gfx1151 serving on Strix Halo | Deferred | ROCm - cannot be tested here; revisit with #217, #535, #317 |
| [#241](https://github.com/FlashML-org/FreeToken/pull/241) | rocm: fix native extensions, kernel JIT builds, and Triton PTX fallbacks for gfx1150 | Deferred | ROCm - cannot be tested here; also edits shared CUDA headers, revisit with the other ROCm PRs |
| [#217](https://github.com/FlashML-org/FreeToken/pull/217) | feat(rocm): AMD ROCm runtime for RDNA3/4 with native Qwen3.5-MoE GGUF decode parity | Deferred | ROCm - cannot be tested here; revisit with the other ROCm PRs |
| [#210](https://github.com/FlashML-org/FreeToken/pull/210) | GGUF: serve DeepSeek-V4-Flash | Deferred | DeepSeek-V4 too large for this machine |
| [#199](https://github.com/FlashML-org/FreeToken/pull/199) | fix(moe): report non-hybrid fetch telemetry accurately [draft] | Deferred | Draft - revisit when ready |
| [#197](https://github.com/FlashML-org/FreeToken/pull/197) | fix(server): preserve Poolside typed argument coercion [draft] | Deferred | Draft - revisit when ready; Laguna cannot run here |
| [#196](https://github.com/FlashML-org/FreeToken/pull/196) | perf(gguf): sm_120 dispatch thresholds + upstream int8-MMA MMQ port (Ornith) | Deferred | Tuned for sm_120, not available here; 27.8k lines, too large for batch review; own project later |
| [#189](https://github.com/FlashML-org/FreeToken/pull/189) | fix(installer): strip AppImage library paths from children [draft] | Deferred | Draft - revisit when ready |
| [#137](https://github.com/FlashML-org/FreeToken/pull/137) | feat(rocm): serve on AMD GPUs through the HIP toolchain | Deferred | ROCm - cannot be tested here; revisit with the other ROCm PRs |
| [#135](https://github.com/FlashML-org/FreeToken/pull/135) | test(distributed): preserve the single-rank communication path [draft] | Deferred | Draft - revisit when ready; ROCm/multi-GPU cannot be tested here |
| [#134](https://github.com/FlashML-org/FreeToken/pull/134) | fix(rocm): explicitly gate NVFP4 CUDA backends [draft] | Deferred | Draft - revisit when ready; ROCm cannot be tested here |
| [#133](https://github.com/FlashML-org/FreeToken/pull/133) | test(rocm): cover split and masked JIT paths [draft] | Deferred | Draft - revisit when ready; ROCm cannot be tested here |
| [#131](https://github.com/FlashML-org/FreeToken/pull/131) | GGUF: support all quant types, add qwen35moe | Deferred | User's call: own project later (5.9k lines, partly overlaps #494, 53 commits behind next) |
| [#116](https://github.com/FlashML-org/FreeToken/pull/116) | fix(dsv4): honor prefill limits and derive SWA capacity | Deferred | DeepSeek-V4 too large for this machine; revisit with #105 |
| [#105](https://github.com/FlashML-org/FreeToken/pull/105) | fix(dsv4): honor an explicit --max-prefill-length instead of silently forcing single-pass prefill | Deferred | DeepSeek-V4 too large for this machine; revisit with #116 |
| [#104](https://github.com/FlashML-org/FreeToken/pull/104) | feat(models): support TP for qwen3_5_moe | Deferred | Needs multi-GPU |
| [#93](https://github.com/FlashML-org/FreeToken/pull/93) | feat: add native Kimi-K3 inference support | Deferred | Kimi-K3 too large for this machine |
| [#71](https://github.com/FlashML-org/FreeToken/pull/71) | [3/3] perf(dsv4): add hardware-aware adaptive verification | Deferred | Needs multi-GPU and DeepSeek-V4, neither available here |
| [#70](https://github.com/FlashML-org/FreeToken/pull/70) | [1/3] feat(dsv4): add tensor-parallel DeepSeek-V4 runtime | Deferred | Needs multi-GPU and DeepSeek-V4, neither available here |
| [#69](https://github.com/FlashML-org/FreeToken/pull/69) | [2/3] feat(dsv4): implement exact DSpark speculative decoding | Deferred | Needs multi-GPU and DeepSeek-V4, neither available here |
| [#65](https://github.com/FlashML-org/FreeToken/pull/65) | Apple Silicon Metal backend (ft serve on macOS arm64) | Deferred | macOS / Apple Silicon - cannot be tested here |
| [#59](https://github.com/FlashML-org/FreeToken/pull/59) | Add Gemma-4 E-series (E2B/E4B) support: PLE, KV-layer sharing, double-wide MLP, and a dense GGUF parser | Deferred | Needs rework on next (13-file conflict with Gemma-4 changes); own project later, E2B/E4B are testable here |
| [#30](https://github.com/FlashML-org/FreeToken/pull/30) | fix(deepseek_v4): resolve HF repo ids to local cache when serving | Deferred | DeepSeek-V4 too large for this machine; revisit with #105 and #116 |
| [#24](https://github.com/FlashML-org/FreeToken/pull/24) | fix(cuda): support Turing GPUs | Deferred | Needs reimplementation on next (conflicts with #132, would drop A100 prebuilt kernels); Turing cannot be tested here |
<!-- fork:pr-table:end -->

## Our own additions

### Done

- **`ft info` and a pre-load memory preflight.** `ft info <model> [ft serve flags]` forecasts
  what `ft serve` would put on the GPU (weights, expert cache, KV cache, context) and whether it
  fits, without loading a weight; `ft serve` refuses a configuration that cannot fit before
  spending minutes on the load. Within ~2% of the real allocation. Opened upstream as
  [#595](https://github.com/FlashML-org/FreeToken/pull/595).
- **CPU-resident input embeddings** (`--embed-device cpu`): the input-embedding table moves to
  pinned host RAM and the GPU reads the looked-up rows over PCIe, inside the CUDA graphs. On
  Qwen3.8-27B with the fp8 KV cache the context grows from 25k to 100k tokens, with the same
  prefill and decode speed and token-identical greedy output. `ft info` prices the flag and
  suggests it. The idea comes from [#456](https://github.com/FlashML-org/FreeToken/pull/456); to
  be offered upstream as its own pull request.
- **Speculative decoding with DFlash/DFlash2** (built on
  [#258](https://github.com/FlashML-org/FreeToken/pull/258)): `--speculative-algorithm dflash
  --speculative-draft-model-path z-lab/Qwen3.8-27B-DFlash2 --speculative-draft-quant fp8`. We
  added DFlash2 drafts (the only ones published for Qwen3.8-27B), an fp8 draft, verify graphs
  for the triton and FlashInfer backends (fp8 and bf16 KV), fixed a KV page leak per request,
  and cut the loop to one target forward per cycle (the PR ran two). Prefix reuse stays on: the draft's context is a
  windowed, preallocated cache that carries over to the next turn of the same chat, so a
  follow-up turn starts in 0.1–0.2 s instead of re-prefilling the conversation. On the hybrid
  GDN target the commit replays the recurrence over the accepted tokens instead of storing a
  147 MiB state per drafted token, which keeps 64k tokens of context (32k with the radix
  cache's GDN snapshots) instead of 27k. Qwen3.8-27B decodes 190–200 tok/s instead of 45 on
  code and math and ~115 on prose; on Qwen3.6-35B-A3B with expert offload, code and math go
  from 140–150 to 290–300 tok/s. The adaptive gate times real plain decode steps and turns
  speculation off for a request where the draft loses (German prose on the MoE);
  `--disable-speculative-adaptive` keeps it on. With `--max-running-requests N` several
  decoding requests draft together and share one batched verify forward: four concurrent
  prompts on the 27B decode ~240 tok/s in total instead of ~123 one after another (an
  offloaded MoE keeps one request per verify, where batching streams more experts than it
  saves). Logprobs are reported per emitted token. For
  comparison, the 27B's own MTP head (simulated offline on the same prompts) accepts about as
  many tokens per cycle as DFlash2 at MTP=7 (4.7 vs 4.3–4.5), but drafting 7 tokens takes 7
  sequential steps (13 ms) instead of one 7 ms pass: ~150 instead of ~200 tok/s on code.
- **No more ~0.8 s first-token floor on MoE offload:** every prefill streamed all expert layers
  over PCIe, because the GPU expert cache filled only during decode and the copy of cached
  experts was off. The cache now starts filled (9.2k of Qwen3.6-35B-A3B's 10.2k experts) and a
  prefill copies only the missing experts over PCIe: a short prompt's first token comes after
  ~170 ms instead of 790 ms, a 6k-token prompt prefills in 1.15 s instead of 1.6 s, with
  unchanged decode speed and output. `--disable-moe-prefill-hit-d2d` restores the old copy. On
  branch `fix/moe-ttft`, meant for an upstream pull request.
- **Offload instead of a misleading hybrid pick:** `ft bench bw` recommended `hybrid` for
  Qwen3.6-35B-A3B here, which then decoded at 20 tok/s instead of 140 with `offload`. Two
  causes: hybrid's CPU workers took every core, so the engine thread waited for each layer
  (fixed: 20 -> 103 tok/s), and hybrid pays a GPU-CPU round trip on every layer, which only
  pays off when the GPU expert cache misses often. Measured, hybrid wins only when the cache
  holds under ~15% of the experts (5%: 61 vs 50 tok/s; 20%: 64 vs 75; 92%: 103 vs 140), so a
  profile-picked hybrid now falls back to offload above that. On branch `fix/moe-hybrid-pick`,
  meant for an upstream pull request.
- **Upstream pull requests we keep although their authors closed them** (closed without a
  merge or a replacement upstream, so they no longer show in the tables above; the bugs are
  still on upstream `main`):
  - [#340](https://github.com/FlashML-org/FreeToken/pull/340) by dejay2: `--moe-cache-auto`
    reserves the KV pool's dummy page 0. Without it the plan can hand that page's bytes to
    expert slots (OOM at boot with large pages) and `--kv-reserve-tokens` delivers one page
    too few; here Qwen3.6-35B-A3B with `--kv-reserve-tokens 32768` gets 32850 tokens.
  - [#339](https://github.com/FlashML-org/FreeToken/pull/339) by dejay2: the Triton fallback
    of the varlen GDN/KDA prefill conv no longer reads the longest request back from the GPU,
    a sync that breaks CUDA-graph capture on every install without `sgl_kernel`. Confirmed by
    two reviewers on RTX 4090s; capture tests included.
  - [#269](https://github.com/FlashML-org/FreeToken/pull/269) by sime2408: a tokenizer or
    detokenizer worker that dies at startup reports its error instead of only "exited during
    load".
  - Dropped again: [#338](https://github.com/FlashML-org/FreeToken/pull/338) (fused PLE n-gram
    hash). The kernel is correct, but its own review thread measured no end-to-end gain, since
    decode replays the hash inside the CUDA graph; not worth fork-only code on PLE paths that
    upstream keeps reworking.
- **Fixes found while reviewing, offered back upstream:**
  - dense Gemma-4 GGUF checkpoints load end to end (on top of
    [#359](https://github.com/FlashML-org/FreeToken/pull/359));
  - pure ASGI middlewares, so an abandoned non-streaming request is really aborted (the missing
    piece of [#222](https://github.com/FlashML-org/FreeToken/pull/222));
  - `bench_serving.py`: `--api-key` and correct fresh-prefill rates with cache reporting (on
    [#341](https://github.com/FlashML-org/FreeToken/pull/341)).
- Many smaller fixups on adopted pull requests; see "Our follow-up" in the tables above.

### Planned next

- **Hot-expert pinning**, our own version of
  [#563](https://github.com/FlashML-org/FreeToken/pull/563).
- **Model support:** Qwen3.5/3.6-MoE GGUF
  ([#131](https://github.com/FlashML-org/FreeToken/pull/131)), Gemma-4 E2B/E4B
  ([#59](https://github.com/FlashML-org/FreeToken/pull/59)), more llm-compressor NVFP4 export
  variants ([#413](https://github.com/FlashML-org/FreeToken/pull/413)).

## Using this branch

Build and run it from source as described in the upstream
[installation guide](docs/install.md) and [CLI reference](docs/cli.md), on the `next` branch.
FreeToken is licensed under the terms in [LICENSE](LICENSE).
