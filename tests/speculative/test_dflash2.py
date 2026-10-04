"""DFlash2 draft pieces: the dynamic causal conv, the candidate selector and the fp8 draft linear."""

from __future__ import annotations

import pytest
import torch
import torch.nn.functional as F

from freetoken.speculative.dflash.config import DFlashConfig
from freetoken.speculative.dflash.model import (
    _CandidateSelector,
    _Fp8RowLinear,
    _grouped_dynamic_convolve,
)

DFLASH2_CFG = {
    "hidden_size": 64, "vocab_size": 50, "num_hidden_layers": 1,
    "dflash_config": {"block_size": 4, "mask_token_id": 49, "target_layer_ids": [0],
                      "conv_group_size": 16, "conv_kernel_size": 2, "selector_rank": 8, "selector_top_k": 5},
}


def test_config_detects_dflash2():
    cfg = DFlashConfig.from_hf_config(DFLASH2_CFG)
    assert cfg.is_dflash2 and cfg.selector_top_k == 5 and cfg.conv_group_size == 16
    assert not DFlashConfig.from_hf_config({"dflash_config": {"block_size": 16}}).is_dflash2


def test_grouped_dynamic_convolve_is_a_causal_two_tap_conv():
    torch.manual_seed(0)
    T, H, K, G = 6, 32, 2, 8
    hidden = torch.randn(T, H, dtype=torch.float64)
    dynamic = torch.randn(T, K, H // G, dtype=torch.float64)
    base = torch.randn(K, H, dtype=torch.float64)
    out = _grouped_dynamic_convolve(hidden, dynamic, base, G)
    # out[t] = sum_o (base[o] + dynamic[t, o] per group) * hidden[t - o], zero before the block
    expect = torch.zeros_like(hidden)
    for t in range(T):
        for o in range(K):
            if t - o >= 0:
                tap = base[o] + dynamic[t, o].repeat_interleave(G)
                expect[t] += tap * hidden[t - o]
    torch.testing.assert_close(out, expect)


def _selector(seed=0):
    torch.manual_seed(seed)
    sel = _CandidateSelector(DFlashConfig.from_hf_config(DFLASH2_CFG))
    sel.predecessor_codebook = torch.randn(50, 8, dtype=torch.float32)
    sel.successor_codebook = torch.randn(50, 8, dtype=torch.float32)
    sel.hidden_projection.weight = torch.randn(8, 64, dtype=torch.float32)
    return sel


@pytest.fixture(autouse=True)
def _tp1(monkeypatch):
    import freetoken.layers.linear as linear_mod
    from freetoken.distributed import DistributedInfo

    tp = DistributedInfo(rank=0, size=1)
    if hasattr(linear_mod, "get_tp_info"):
        monkeypatch.setattr(linear_mod, "get_tp_info", lambda: tp)


def test_selector_greedy_path_maximizes_each_step():
    sel = _selector()
    hidden = torch.randn(3, 64)
    logits = torch.randn(3, 50)
    anchor = torch.tensor([7])
    path, probs = sel.select(hidden, logits, anchor, None)
    assert probs is None
    proj = hidden @ sel.hidden_projection.weight.T
    prev = 7
    for p in range(3):
        top = torch.topk(logits[p], 5).indices
        scores = logits[p, top] + sel.successor_codebook[top] @ (sel.predecessor_codebook[prev] * proj[p])
        prev = int(top[scores.argmax()])
        assert int(path[p]) == prev


def test_selector_sampling_distribution_lives_on_the_candidates():
    sel = _selector(1)
    logits = torch.randn(3, 50)
    path, probs = sel.select(torch.randn(3, 64), logits, torch.tensor([3]), torch.tensor([0.7]))
    assert probs.shape == (3, 50)
    torch.testing.assert_close(probs.sum(-1), torch.ones(3))
    for p in range(3):
        support = set(torch.nonzero(probs[p]).flatten().tolist())
        assert support <= set(torch.topk(logits[p], 5).indices.tolist())
        assert int(path[p]) in support


@pytest.mark.skipif(not torch.cuda.is_available(), reason="fp8 linear kernel needs CUDA")
def test_fp8_row_linear_tracks_bf16():
    torch.manual_seed(0)
    w = (torch.randn(256, 512) * 0.05).bfloat16()
    lin = _Fp8RowLinear(w.cuda())
    x = torch.randn(5, 512, device="cuda", dtype=torch.bfloat16)
    ref = F.linear(x.float(), w.cuda().float())
    out = lin.forward(x).float()
    assert lin.weight.dtype == torch.float8_e4m3fn and lin.weight_scale.shape == (256,)
    assert (out - ref).abs().max() / ref.abs().max() < 0.05
