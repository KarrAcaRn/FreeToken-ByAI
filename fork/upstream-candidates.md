# Possible upstream PRs

Changes on `next` that could go to FlashML-org/FreeToken as their own PR. A candidate becomes a
feature branch from `main` (see the branch layout in the fork notes) once we decide to send it.

| Candidate | Commits on `next` | Status |
|---|---|---|
| ft info + pre-load memory preflight | 6890aeb, 291d603, 63e1752 | **Opened as #595** (branch `feat/ft-info`); follow-ups once #562/#574 and #354/#408 merge upstream |
| Load dense Gemma-4 GGUFs end to end | 5b0cb77 (merge of #359), 7f2fc79 | Candidate, see below |
| bench_serving: --api-key and the zero-hit cache report | b36d49d, 23d92b6 (on top of #341) | Candidate, see below |
| Pure ASGI middlewares, so #222's non-streaming abort works | f8de64f (on top of #222) | Candidate, see below |
| MoE offload: preload the expert slot cache, prefill hit-D2D by default | 2012f9e (branch `fix/moe-ttft`, from main) | Candidate, ready as a branch; see below |
| Profile-picked hybrid falls back to offload for large expert caches; CPU pool leaves the engine a core | 74e0ece (branch `fix/moe-hybrid-pick`, from main) | Candidate, ready as a branch; see below |
| Non-stream tool calls: the detector decides (Llama 3.2 bare-JSON calls) | 925e5f8 | Candidate, applies to upstream main as is; see below |
| gpt-oss: tool recipient in the role header | 3b54232 | Candidate, applies to upstream main as is; see below |
| Llama 3.2: tool name under the "function" key | 0c6aec0 | Candidate, applies to upstream main as is; see below |
| Qwen3 Instruct checkpoints (VL, Coder) get no qwen3 reasoning parser | bfc41c7 (on top of #564) | Suggest on #564, which is still open upstream |
| Hoist a system message the template silently drops (Qwen3-VL, gpt-oss) | 2b3563c (on top of our #487 version) | Candidate together with #487's approach |

## Load dense Gemma-4 GGUFs end to end

Upstream PR #359 (opened by Cyber-Marty, commit by Circle-Cheng <yc.22319139@gmail.com>) lets a dense Gemma-4 GGUF's config parse, but on its own the model
still cannot load. Our fixup 7f2fc79 adds the two missing pieces:

- `is_gguf_model` keyed on the Q4_0 expert format, which a dense GGUF does not have, so the model
  was built bf16 and failed on the packed weights (`KeyError: 'model.embed_tokens.weight'`). It
  now also recognises a GGUF by its recorded tensor layout (`gguf_quant_types`).
- `iter_gguf_weights` asserted the offload contract even without experts; it now asserts it only
  for MoE checkpoints.
- Plus the merge resolution against #494: `_gguf_quant_layout` lays out expert tensors only when
  the checkpoint has experts (it demanded them in every layer and divided by `num_experts`).

Tested: google/gemma-4-12B-it-qat-q4_0-gguf on an RTX 4090 (driver 595.91.07) - loads, 158.7k KV
tokens (preflight forecast 155.7k), correct answers, ~95 tok/s decode, ~1090 tok/s prefill;
`tests/models/test_gemma4_gguf_config.py` (incl. a regression test for the detection) and
`test_gemma4_gguf_rope.py` against the real GGUF pass.

How to send it (decide when we do it):
- #359 is still open upstream: suggest the two fixes there (comment / PR against its branch), so
  its author can complete it - or
- a follow-up PR on top of #359 once it is merged, or
- one PR with #359's commit (Co-authored-by: Circle-Cheng <yc.22319139@gmail.com>) plus our fixes, linking
  #359 and its issue #357.

Upstream main has no #494 (mixed-quant GGUF), so a branch from `main` needs the quant-layout part
dropped or adapted, like `feat/ft-info` was.

## bench_serving: --api-key and the zero-hit cache report

Upstream PR #341 (tuxevil, still open) adds `benchmarks/bench_serving.py`, a client-wall serving
benchmark. Two fixes on top of it:

- b36d49d: `--api-key` (default `$FREETOKEN_API_KEY`, like `ft serve`) sent as
  `Authorization: Bearer`. Without it the harness gets 401 from a server started with
  `--api-key`. Note: `--api-key` itself comes from upstream PR #305, which upstream main may not
  have yet - then this part waits for #305 (or ships as a no-op option).
- 23d92b6: the server omits `prompt_tokens_details` for a zero prefix-cache hit (sglang
  convention), so every fresh prompt read as "no cache report" and the fresh-prefill rate - the
  harness's main number - was always n/a. The harness now probes once whether a repeated prompt
  reports a hit; when it does, an absent object counts as a miss. This one applies to upstream
  main as is.

Tested: RedHatAI/Qwen3.6-35B-A3B-NVFP4 on an RTX 4090, `ft serve ... --enable-cache-report
--api-key` and `python benchmarks/bench_serving.py --prefill-sizes 1024,4096`: 401 without the
key; with it fresh prefill 1325 tok/s (1k) / 5238 tok/s (4k), prefix hits 4032/4096 detected,
decode ~150 tok/s. `tests/benchmarks/test_bench_serving.py` (16 tests) passes.

How to send it: #341 is still open, so the natural route is to suggest both fixes there (review
comment or a PR against its branch); otherwise a follow-up PR once #341 merges.

## Pure ASGI middlewares, so #222's non-streaming abort works

Upstream PR #222 (Artemowka22, open) aborts an abandoned non-streaming request once
`request.is_disconnected()` turns true. Starlette's BaseHTTPMiddleware (`@app.middleware("http")`)
never passes the client's disconnect to the endpoint, and upstream main already has one
(`_record_request_middleware`), so in a real server that check never fires - #222's own tests use
mocks. f8de64f rewrites the middlewares as pure ASGI (same order; the request ring still records
at response start) and adds a test that keeps BaseHTTPMiddleware off the app.

Tested: Qwen/Qwen3-0.6B on an RTX 4090, `ft serve --max-running-requests 1`; a 4000-token
non-streaming chat request dropped after 1 s: the next request waited 7.4 s before (the abandoned
one decoded to the end), 0.12 s after. A minimal FastAPI repro shows the cause in isolation
(endpoint sees the disconnect after 0.3 s without the middleware, never with it).

How to send it: suggest it on #222 (it is the missing piece for that PR), or as its own small
fix PR that also benefits upstream main (its _record_request_middleware alone hides disconnects
from every handler). On main only the request-ring middleware exists (no --api-key yet).

## MoE offload: preloaded expert slot cache and prefill hit-D2D by default

Branch `fix/moe-ttft` (from main, commit 2012f9e). On an offloaded MoE every request paid a
fixed ~0.8 s before its first token: prefill streams whole expert layers into the double
buffer, the slot cache (filled only by decode misses) held 342 of 10240 experts, and
`--moe-prefill-hit-d2d` was off. The branch fills the free slots after startup and makes
hit-D2D the default (`--disable-moe-prefill-hit-d2d`; `--moe-prefill-hit-d2d` still parses).

Tested on RedHatAI/Qwen3.6-35B-A3B-NVFP4, RTX 4090 (PCIe 4.0), CUDA 13.1, plain main + branch:
22-token prompt TTFT 787 -> 160 ms, 6.3k-token prompt 1.60 -> 1.15 s, decode ~150 tok/s and
greedy output unchanged; tests/moe (incl. two new fill_slots tests), tests/engine,
tests/scheduler, tests/server pass. Without cudaMemcpyBatchAsync (CUDA < 13) hit-D2D still
falls back to full-layer copies, so the preload then only helps the first decode steps; a
fallback that gathers misses with the fused index-copy kernel would cover that.
If upstream merges #601 first, its unified-memory inert-flag warning lists
`--moe-prefill-hit-d2d` as set; with the new default it must name `--disable-moe-prefill-hit-d2d`
instead (as next's 1b43e59 does).

## Profile-picked hybrid only for small expert caches

Branch `fix/moe-hybrid-pick` (from main, commit 74e0ece). `ft bench bw` rates the CPU MoE
kernel 3.1x the PCIe gather for RedHatAI/Qwen3.6-35B-A3B-NVFP4 on an RTX 4090 with an 8-core
host, so `auto` picked hybrid, which then decoded at 20 tok/s instead of offload's 140.

- The auto-sized CPU pool pinned 7 workers plus the flag coordinator to the 8 cores, so the
  engine's main thread waited for a time slice per MoE layer. Auto sizing now leaves it a core
  (`auto_pool_cores`): 20 -> 103 tok/s.
- Hybrid pays a GPU<->CPU round trip (~0.1 ms) per layer per decode step, and an LRU cache under
  skewed routing misses far less than its size suggests. Decode tok/s offload vs hybrid by the
  share of experts in the slot cache: 5% 50/61, 10% 59/64, 20% 75/64, 50% 113/87, 92% 140/103.
  A profile-picked hybrid now decodes on offload when the cache holds >= 15% of the experts
  (`_profile_hybrid_target`, after the cache is sized); explicit `--moe-strategy hybrid` is
  unchanged. The threshold comes from this one box; a profile could carry it per machine later.

Tested on plain main + branch: auto with the profile falls back to offload at 152 tok/s with
greedy output identical to explicit offload; with a 10% cache it stays hybrid; tests/moe and
tests/engine pass (new tests/engine/test_profile_hybrid_pick.py).



## Tool-call fixes found by rendering the new test models (2026-10-05, CPU only)

Each model's own chat template renders an assistant tool call; the part the model would generate
went through the server's reasoning split and tool parser (`_split_reasoning`, `_parse_tool_response`).

- 925e5f8: `_parse_tool_response` parsed only when the reply held one of the global opener tags.
  Llama 3.2 emits custom-tool calls as bare JSON (`{"name": ..., "parameters": ...}`), which
  `Llama32Detector` handles and streaming already parsed; non-stream returned it as content. The
  gate now asks the detector's `has_tool_call` (checked: no detector is narrower than the old tags
  for what it parses).
- 3b54232: Harmony allows `<|start|>assistant to=functions.x<|channel|>commentary ...` (recipient
  in the role header), which gpt-oss-20b's own template renders. The harmony reasoning parser read
  the recipient only from the channel header, so the call became content holding the JSON. It now
  moves the recipient into the channel header before scanning (non-stream and streaming).
- 0c6aec0 (found in the live run): Llama-3.2-1B-Instruct emits `{"type": "function", "function":
  "get_weather", "parameters": {...}}`. `parse_base_json` read only `"name"`, and with unknown-tool
  forwarding on the call reached the client as `name: null`. The name is now hoisted from
  `"function"` (non-stream and streaming); a nameless call is dropped.

Tested: tests/server + tests/tokenizer pass, each new test fails without its fix. Live on the
RTX 4090 (2026-10-05): Llama-3.2-1B-Instruct, gpt-oss-20b and Qwen3-VL-8B-Instruct each return a
parsed get_weather call (stream and non-stream), plain answers keep a non-empty content, and a
mid-conversation system message takes effect.
