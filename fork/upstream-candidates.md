# Possible upstream PRs

Changes on `next` that could go to FlashML-org/FreeToken as their own PR. A candidate becomes a
feature branch from `main` (see the branch layout in the fork notes) once we decide to send it.

| Candidate | Commits on `next` | Status |
|---|---|---|
| ft info + pre-load memory preflight | 6890aeb, 291d603, 63e1752 | **Opened as #595** (branch `feat/ft-info`); follow-ups once #562/#574 and #354/#408 merge upstream |
| Load dense Gemma-4 GGUFs end to end | 5b0cb77 (merge of #359), 7f2fc79 | Candidate, see below |

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
