from types import SimpleNamespace

import torch
import pytest

from freetoken.engine.engine import (
    DFlashMetrics,
    _dflash_target_verify_graph_enabled_for_config,
)
from freetoken.engine.sample import BatchSamplingArgs
from freetoken.speculative.utils import (
    AdaptiveGate,
    rejection_sample_chain,
    rejection_step,
    sampling_probs,
    select_output_tokens,
    select_streaming_output_tokens,
)


def testselect_output_tokens_accepts_longest_matching_prefix():
    base = torch.tensor([10], dtype=torch.int32)
    candidates = torch.tensor([20, 30, 40], dtype=torch.int32)
    verify = torch.tensor([20, 30, 41, 50], dtype=torch.int32)

    out, accepted = select_output_tokens(base, candidates, verify)

    assert accepted == 2
    assert torch.equal(out, torch.tensor([10, 20, 30, 41], dtype=torch.int32))


def testselect_streaming_output_tokens_waits_until_bonus_after_all_accept():
    base = torch.tensor([10], dtype=torch.int32)
    candidates = torch.tensor([20, 30], dtype=torch.int64)

    out, accepted, done = select_streaming_output_tokens(
        base, candidates, torch.tensor([20, 30], dtype=torch.int32)
    )
    assert done is False
    assert accepted == 2
    assert out.numel() == 0

    out, accepted, done = select_streaming_output_tokens(
        base, candidates, torch.tensor([20, 30, 41], dtype=torch.int32)
    )
    assert done is True
    assert accepted == 2
    assert torch.equal(out, torch.tensor([10, 20, 30, 41], dtype=torch.int32))


def test_dflash_target_verify_graph_follows_the_moe_strategy():
    moe = SimpleNamespace(is_moe=True)
    for strategy, enabled in [("offload", True), ("fused", True), ("cpu", False), ("hybrid", False)]:
        config = SimpleNamespace(moe_strategy=strategy, model_config=moe)
        assert _dflash_target_verify_graph_enabled_for_config(config) is enabled, strategy
    assert _dflash_target_verify_graph_enabled_for_config(
        SimpleNamespace(moe_strategy="auto", model_config=SimpleNamespace(is_moe=False)))


def test_dflash_target_verify_graph_allows_explicit_fused_moe_with_capture_safe_topk():
    config = SimpleNamespace(
        moe_strategy="fused",
        model_config=SimpleNamespace(is_moe=True),
    )

    assert _dflash_target_verify_graph_enabled_for_config(config) is True


def test_dflash_adaptive_gate_disables_when_slower_than_baseline():
    from freetoken.speculative.utils import AdaptiveGate

    gate = AdaptiveGate(min_cycles=4, eval_interval=4, margin=1.05, warmup_cycles=0)
    for _ in range(4):
        gate.record(cycle_ms=29.6, target_ms=6.0, out_tokens=4)
    assert gate.enabled is False
    assert gate.should_run(uid=1) is False


def test_dflash_adaptive_gate_stays_enabled_when_faster_than_baseline():
    from freetoken.speculative.utils import AdaptiveGate

    gate = AdaptiveGate(min_cycles=4, eval_interval=2, margin=1.05, warmup_cycles=0, probe_steps=0)
    for _ in range(10):
        gate.record(cycle_ms=22.0, target_ms=6.0, out_tokens=4)
    assert gate.should_run(uid=1) is True


def test_dflash_adaptive_gate_resets_on_new_request():
    from freetoken.speculative.utils import AdaptiveGate

    gate = AdaptiveGate(min_cycles=4, eval_interval=4, margin=1.05, warmup_cycles=0, probe_steps=0)
    assert gate.should_run(uid=1)
    for _ in range(4):
        gate.record(cycle_ms=29.6, target_ms=6.0, out_tokens=4)
    assert gate.should_run(uid=1) is False
    assert gate.should_run(uid=2) is True


def test_dflash_rejection_chain_accepts_all_when_draft_matches_target():
    from freetoken.speculative.utils import rejection_sample_chain

    V = 8
    base = torch.tensor([5], dtype=torch.int32)
    drafts = torch.tensor([1, 2, 3], dtype=torch.int32)
    draft_probs = torch.zeros(3, V)
    draft_probs[0, 1] = draft_probs[1, 2] = draft_probs[2, 3] = 1.0
    target_probs = torch.zeros(4, V)
    target_probs[0, 1] = target_probs[1, 2] = target_probs[2, 3] = 1.0
    target_probs[3, 7] = 1.0  # bonus distribution

    out, accepted = rejection_sample_chain(
        base, drafts, draft_probs, target_probs,
        uniform=torch.full((3,), 0.5),
    )

    assert accepted == 3
    assert torch.equal(out, torch.tensor([5, 1, 2, 3, 7], dtype=torch.int32))


def test_dflash_rejection_chain_rejects_and_samples_residual():
    from freetoken.speculative.utils import rejection_sample_chain

    V = 8
    base = torch.tensor([5], dtype=torch.int32)
    drafts = torch.tensor([1, 2], dtype=torch.int32)
    draft_probs = torch.zeros(2, V)
    draft_probs[0, 1] = draft_probs[1, 2] = 1.0
    target_probs = torch.zeros(3, V)
    target_probs[0, 6] = 1.0  # target puts zero mass on draft token 1
    target_probs[1, 2] = 1.0
    target_probs[2, 4] = 1.0

    out, accepted = rejection_sample_chain(
        base, drafts, draft_probs, target_probs,
        uniform=torch.full((2,), 0.5),
    )

    assert accepted == 0
    # residual = relu(p - q): p[6]=1, q[1]=1 -> residual one-hot on 6
    assert torch.equal(out, torch.tensor([5, 6], dtype=torch.int32))


def test_sample_and_select_greedy_matches_exact_match():
    from freetoken.engine.engine import _dflash_sample_and_select as sample_and_select

    V = 10
    base = torch.tensor([5], dtype=torch.int32)
    drafts = torch.tensor([1, 2, 3], dtype=torch.int32)
    # target argmax at positions 0..3: [1, 2, 9, 4] -> accept 2, bonus 9
    verify_logits = torch.zeros(4, V)
    verify_logits[0, 1] = 10; verify_logits[1, 2] = 10
    verify_logits[2, 9] = 10  # mismatch: draft[2]=3, target argmax=9
    verify_logits[3, 4] = 10
    args = BatchSamplingArgs(temperatures=None)  # greedy
    worker = SimpleNamespace(last_draft_probs=None)
    sampler = SimpleNamespace(sample=lambda logits, _args: logits.argmax(dim=-1))

    out, accepted = sample_and_select(sampler, args, worker.last_draft_probs, base, drafts, verify_logits, 4)
    assert accepted == 2
    assert torch.equal(out, torch.tensor([5, 1, 2, 9], dtype=torch.int32))

def test_sample_and_select_sampling_uses_rejection_chain():
    from freetoken.engine.engine import _dflash_sample_and_select as sample_and_select

    V = 8
    base = torch.tensor([5], dtype=torch.int32)
    drafts = torch.tensor([1, 2, 3], dtype=torch.int32)
    # draft_probs one-hot on draft tokens; target_probs one-hot on same -> accept all
    draft_probs = torch.zeros(3, V)
    draft_probs[0, 1] = draft_probs[1, 2] = draft_probs[2, 3] = 1.0
    target_probs_logits = torch.zeros(4, V)
    target_probs_logits[0, 1] = 40; target_probs_logits[1, 2] = 40
    target_probs_logits[2, 3] = 40; target_probs_logits[3, 7] = 40
    args = BatchSamplingArgs(temperatures=torch.tensor([1.0]))
    worker = SimpleNamespace(last_draft_probs=draft_probs)

    out, accepted = sample_and_select(None, args, worker.last_draft_probs, base, drafts, target_probs_logits, 4)
    assert accepted == 3
    assert torch.equal(out, torch.tensor([5, 1, 2, 3, 7], dtype=torch.int32))



def test_dflash_target_verify_lens_within_budget_filters_by_commit_memory():
    from freetoken.engine.graph import _dflash_target_verify_lens_within_budget

    pool = SimpleNamespace(
        conv_states=torch.zeros((2, 4, 3, 2), dtype=torch.float32),
        recurrent_states=torch.zeros((2, 4, 1, 3, 3), dtype=torch.float32),
    )
    # per token: conv state 2*3*2 fp32 = 48 B, q/k/v 2*3 + a/b 2*2*1 bf16 = 20 B
    assert _dflash_target_verify_lens_within_budget([1, 2, 3, 4], pool, 272) == [1, 2, 3, 4]
    assert _dflash_target_verify_lens_within_budget([1, 2, 3, 4], pool, 150) == [1, 2]
    assert _dflash_target_verify_lens_within_budget([1, 2, 3, 4], pool, 0) == []
    assert _dflash_target_verify_lens_within_budget([1, 2], None, 0) == [1, 2]


def test_graph_capture_buffer_target_verify_commit_inputs():
    from freetoken.core import Batch, Req
    from freetoken.engine.graph import DFlashVerifyStorage, GraphCaptureBuffer

    pool = SimpleNamespace(
        conv_states=torch.zeros((4, 2, 3, 2), dtype=torch.float32),
        recurrent_states=torch.zeros((4, 2, 1, 3, 3), dtype=torch.float32),
    )
    cpu = torch.device("cpu")
    storage = DFlashVerifyStorage.alloc(
        6, 5, cpu, hidden_size=3, hidden_dtype=torch.bfloat16, num_hidden_layers=1,
        linear_state_pool=pool)
    # two requests of three verify tokens
    buffer = GraphCaptureBuffer.init_dflash_verify(2, 3, cpu, storage)
    reqs = [
        Req(input_ids=torch.tensor([10, 11, 12], dtype=torch.int32), table_idx=i, cached_len=1,
            output_len=1, uid=i, sampling_params=None, cache_handle=None)
        for i in range(2)
    ]
    batch = Batch(reqs=reqs, phase="decode")
    batch.padded_reqs = batch.reqs
    buffer.set_dflash_target_verify_batch(batch, return_linear_snapshots=True)
    fla = batch.fla_metadata
    assert fla.dflash_disable_state_update
    assert fla.cu_seqlens.tolist() == [0, 3, 6]
    assert fla.cache_indices.numel() == 2
    assert fla.dflash_conv_states_buffer.shape == (6, 4, 3, 2)
    assert fla.dflash_gdn_mixed.shape == (4, 6, 3)
    assert fla.dflash_gdn_ab.shape == (4, 2, 6, 1)
    assert buffer.logits.shape == (6, 5) and buffer.hidden_states[0].shape == (6, 3)
    for t in (fla.dflash_conv_states_buffer, fla.dflash_gdn_mixed, fla.dflash_gdn_ab):
        assert t.is_contiguous()
    # a smaller graph views the same storage
    small = GraphCaptureBuffer.init_dflash_verify(1, 2, cpu, storage)
    assert small.logits.data_ptr() == buffer.logits.data_ptr()
