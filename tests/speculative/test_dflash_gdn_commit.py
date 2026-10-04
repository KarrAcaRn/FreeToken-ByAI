"""DFlash GDN commit: replaying the recurrence over the kept tokens from the stored inputs gives
the state the decode kernel reaches after them (what the verify used to store per token)."""

from __future__ import annotations

import pytest
import torch

pytestmark = pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")


@pytest.mark.parametrize("commit_len", [1, 3, 8])
def test_replayed_state_matches_the_kernels_intermediate_state(commit_len):
    from freetoken.kernel.fla import fused_sigmoid_gating_delta_rule_update
    from freetoken.models.qwen3_5_moe.gdn_kernels import gdn_decode_fla

    torch.manual_seed(0)
    dev, n, hk, hv, dk, dv, slots, slot = "cuda", 8, 2, 4, 32, 32, 3, 1
    q = torch.randn(1, n, hk, dk, device=dev, dtype=torch.bfloat16)
    k = torch.randn(1, n, hk, dk, device=dev, dtype=torch.bfloat16)
    v = torch.randn(1, n, hv, dv, device=dev, dtype=torch.bfloat16)
    a = torch.randn(n, hv, device=dev, dtype=torch.bfloat16)
    b = torch.randn(n, hv, device=dev, dtype=torch.bfloat16)
    A_log = torch.randn(hv, device=dev)
    dt_bias = torch.randn(hv, device=dev)
    state0 = torch.randn(slots, hv, dk, dv, device=dev)
    idx = torch.tensor([slot], dtype=torch.int32, device=dev)
    cu = torch.tensor([0, n], dtype=torch.int32, device=dev)

    # the old verify: no state update, one intermediate state per token
    ref_states = torch.zeros(1, n, hv, dk, dv, device=dev)
    pool = state0.clone()
    fused_sigmoid_gating_delta_rule_update(
        A_log=A_log, a=a, dt_bias=dt_bias, softplus_beta=1.0, softplus_threshold=20.0,
        q=q, k=k, v=v, b=b, initial_state_source=pool, initial_state_indices=idx,
        scale=dk ** -0.5, use_qk_l2norm_in_kernel=True, cu_seqlens=cu,
        disable_state_update=True, intermediate_states_buffer=ref_states,
        intermediate_state_indices=torch.zeros(1, dtype=torch.int32, device=dev),
    )
    assert torch.equal(pool, state0), "the verify must leave the slot untouched"

    # the commit: advance the slot over the first commit_len tokens
    c = commit_len
    gdn_decode_fla(
        q[:, :c], k[:, :c], v[:, :c], a[:c], b[:c], A_log=A_log, dt_bias=dt_bias,
        state_source=pool, indices=idx, scale=dk ** -0.5,
        cu_seqlens=torch.tensor([0, c], dtype=torch.int32, device=dev),
    )
    torch.testing.assert_close(pool[slot], ref_states[0, c - 1], rtol=0, atol=0)
    assert torch.equal(pool[0], state0[0]) and torch.equal(pool[2], state0[2])
