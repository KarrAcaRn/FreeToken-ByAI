# Possible upstream PRs

Changes on `next` that could go to FlashML-org/FreeToken as their own PR. A candidate becomes a
feature branch from `main` (see the branch layout in the fork notes) once we decide to send it.

| Candidate | Commits on `next` | Status |
|---|---|---|
| ft info + pre-load memory preflight | 6890aeb, 291d603, 63e1752 | **Opened as #595** (branch `feat/ft-info`); follow-ups once #562/#574 and #354/#408 merge upstream |
| Load dense Gemma-4 GGUFs end to end | 5b0cb77 (merge of #359), 7f2fc79 | Candidate, see below |
| bench_serving: --api-key and the zero-hit cache report | b36d49d, 23d92b6 (on top of #341) | Candidate, see below |
| Pure ASGI middlewares, so #222's non-streaming abort works | f8de64f (on top of #222) | Candidate, see below |

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
