from __future__ import annotations

import copy
from types import SimpleNamespace

import pytest
import torch


def test_cuda_quant_types_have_packed_row_layouts():
    from freetoken.layers.gguf import _DEQUANT, _MMQ, _MMVQ
    from freetoken.models.gguf.dequant import BLOCK_SHAPE

    expected = {
        2: (32, 18),
        3: (32, 20),
        6: (32, 22),
        7: (32, 24),
        8: (32, 34),
        10: (256, 84),
        11: (256, 110),
        12: (256, 144),
        13: (256, 176),
        14: (256, 210),
        16: (256, 66),
        17: (256, 74),
        18: (256, 98),
        19: (256, 50),
        20: (32, 18),
        21: (256, 110),
        22: (256, 82),
        23: (256, 136),
        29: (256, 56),
    }

    assert {quant_type: BLOCK_SHAPE[quant_type] for quant_type in expected} == expected
    assert _MMVQ == set(expected)
    assert _DEQUANT == set(expected)
    assert _MMQ == {2, 3, 6, 7, 8, 10, 11, 12, 13, 14}


def test_gguf_config_shim_can_be_masked_like_hf_config():
    from freetoken.models.gguf.config import GgufConfigShim

    shim = GgufConfigShim(
        architectures=["Gemma4GGUFForCausalLM"],
        model_path="model.gguf",
        model_type="gemma4",
        metadata={},
        vocab_size=4,
        tie_word_embeddings=True,
    )
    masked = copy.copy(shim)
    masked.audio_config = None
    assert masked.audio_config is None


class _Tensor:
    def __init__(self, name: str, ggml_type: int, packed: torch.Tensor):
        self.name = name
        self.ggml_type = ggml_type
        self._packed = packed

    def packed(self) -> torch.Tensor:
        return self._packed


def test_quant_layout_detects_dense_and_per_layer_expert_types(monkeypatch):
    from freetoken.models.gemma4 import gguf
    from freetoken.models.gguf import reader

    tensors = [
        _Tensor("token_embd.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.0.attn_q.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.0.attn_k.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.0.attn_v.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.0.attn_output.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.0.ffn_gate.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.0.ffn_up.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.0.ffn_down.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.0.ffn_gate_up_exps.weight", 21, torch.empty(4, 11, dtype=torch.uint8)),
        _Tensor("blk.0.ffn_down_exps.weight", 20, torch.empty(4, 13, dtype=torch.uint8)),
        _Tensor("blk.1.attn_q.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.1.attn_k.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.1.attn_output.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.1.ffn_gate.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.1.ffn_up.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.1.ffn_down.weight", 8, torch.empty(1, 34, dtype=torch.uint8)),
        _Tensor("blk.1.ffn_gate_up_exps.weight", 23, torch.empty(4, 17, dtype=torch.uint8)),
        _Tensor("blk.1.ffn_down_exps.weight", 8, torch.empty(4, 19, dtype=torch.uint8)),
    ]
    monkeypatch.setattr(reader, "iter_gguf_tensors", lambda _path: iter(tensors))

    layout = gguf._gguf_quant_layout("model.gguf", 2, 4)

    assert layout["embedding"] == 8
    assert layout["qkv"] == (8, 8)
    assert layout["shared_gate_up"] == (8, 8)
    assert layout["expert_gate_up"] == (21, 23)
    assert layout["expert_down"] == (20, 8)
    assert layout["expert_gate_up_bytes"] == (11, 17)
    assert layout["expert_down_bytes"] == (13, 19)


def test_mixed_expert_loader_pads_slots_but_preserves_packed_bytes(monkeypatch):
    from freetoken.models.gemma4 import gguf
    from freetoken.models.gguf import reader

    config = SimpleNamespace(
        num_layers=2,
        num_experts=2,
        hidden_size=32,
        moe_intermediate_size=32,
        gguf_quant_types={
            "expert_gate_up": (21, 23),
            "expert_down": (20, 8),
            "expert_gate_up_bytes": (7, 11),
            "expert_down_bytes": (5, 13),
        },
    )
    gu0 = torch.arange(14, dtype=torch.uint8).reshape(2, 7)
    dn0 = torch.arange(10, dtype=torch.uint8).reshape(2, 5)
    gu1 = torch.arange(22, dtype=torch.uint8).reshape(2, 11)
    dn1 = torch.arange(26, dtype=torch.uint8).reshape(2, 13)
    tensors = [
        _Tensor("blk.0.ffn_gate_up_exps.weight", 21, gu0),
        _Tensor("blk.0.ffn_down_exps.weight", 20, dn0),
        _Tensor("blk.1.ffn_gate_up_exps.weight", 23, gu1),
        _Tensor("blk.1.ffn_down_exps.weight", 8, dn1),
    ]
    monkeypatch.setattr(reader, "iter_gguf_tensors", lambda _path: iter(tensors))
    monkeypatch.setattr(gguf, "_require_tp1", lambda _what: None)
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)

    banks = gguf.load_q4_0_expert_sources("model.gguf", config)

    assert [tuple(t.shape) for t in banks["gate_up"]] == [(2, 11), (2, 11)]
    assert [tuple(t.shape) for t in banks["down"]] == [(2, 13), (2, 13)]
    torch.testing.assert_close(banks["gate_up"][0][:, :7], gu0)
    torch.testing.assert_close(banks["down"][0][:, :5], dn0)
    torch.testing.assert_close(banks["gate_up"][1], gu1)
    torch.testing.assert_close(banks["down"][1], dn1)


def test_gguf_expert_gemm_passes_independent_quant_types(monkeypatch):
    from freetoken.kernel import gguf as kernel
    from freetoken.moe import fused_q4_0
    from freetoken.moe.fused_q4_0 import fused_experts_gguf_q4_0

    calls = []

    def fake_moe(x, weight, ids, top_k, quant_type, row, tokens):
        calls.append((quant_type, tuple(weight.shape), top_k, row, tokens))
        return torch.ones(tokens * top_k, row, dtype=x.dtype)

    monkeypatch.setattr(kernel, "ggml_moe_a8_vec", fake_moe)
    monkeypatch.setitem(fused_q4_0._ACT, "silu", lambda x: x[:, : x.shape[1] // 2])
    hidden = torch.ones(1, 4)
    gate_up = torch.empty(2, 32, dtype=torch.uint8)
    down = torch.empty(2, 48, dtype=torch.uint8)
    weights = torch.ones(1, 1)
    ids = torch.zeros(1, 1, dtype=torch.int32)

    out = fused_experts_gguf_q4_0(
        hidden,
        gate_up,
        down,
        weights,
        ids,
        "silu",
        gate_up_quant_type=21,
        down_quant_type=20,
        intermediate_size=3,
        hidden_size=4,
    )

    assert out.shape == (1, 4)
    assert [call[0] for call in calls] == [21, 20]


def test_unquantized_gguf_linear_reads_its_bytes_as_floats():
    """An F32 / F16 projection keeps its bytes in the uint8 qweight; the GEMM must view them as floats."""
    from freetoken.layers.gguf import GGUFLinear

    for quant_type, dtype in ((0, torch.float32), (1, torch.float16)):
        weight = torch.randn(5, 64).to(dtype)
        op = GGUFLinear(64, 5, quant_type)
        op.qweight = weight.view(torch.uint8)
        x = torch.randn(3, 64)
        torch.testing.assert_close(op.forward(x), x @ weight.float().T, atol=1e-2, rtol=1e-2)


def test_mixed_type_fused_projection_runs_one_gemm_per_type_run():
    from freetoken.layers.gguf import GGUFLinear, GGUFMergedLinear, gguf_linear, gguf_type_runs

    assert gguf_type_runs([8, 4, 2, 2], [8, 8, 0, 0]) == [(0, 2, 8), (2, 4, 0)]
    assert gguf_type_runs([8, 4, 2], [8, 0, 8]) == [(0, 1, 8), (1, 2, 0), (2, 3, 8)]
    assert isinstance(gguf_linear(256, [8, 4], [12, 12]), GGUFLinear)
    op = gguf_linear(64, [3, 2, 4], [0, 0, 1])
    assert isinstance(op, GGUFMergedLinear)
    assert set(op.state_dict()) == {"runs.0.qweight", "runs.1.qweight"}
    w32, w16 = torch.randn(5, 64), torch.randn(4, 64).half()
    op.load_state_dict({"runs.0.qweight": w32.view(torch.uint8), "runs.1.qweight": w16.view(torch.uint8)})
    x = torch.randn(2, 64)
    torch.testing.assert_close(op.forward(x), x @ torch.cat([w32, w16.float()]).T, atol=1e-2, rtol=1e-2)


def test_large_gguf_batches_dequantize_for_a_bf16_gemm(monkeypatch):
    from freetoken.kernel import gguf as kernel
    from freetoken.layers.gguf import fused_mul_mat_gguf

    calls = []
    monkeypatch.setattr(kernel, "ggml_mul_mat_vec_a8", lambda w, x, t, n: calls.append("mmvq") or x.new_zeros(x.shape[0], n))
    monkeypatch.setattr(kernel, "ggml_mul_mat_a8", lambda w, x, t, n: calls.append("mmq") or x.new_zeros(x.shape[0], n))
    monkeypatch.setattr(kernel, "ggml_dequantize", lambda w, t, m, n, dtype: calls.append("dequant") or torch.zeros(m, n, dtype=dtype))
    q8, iq3 = torch.empty(4, 34, dtype=torch.uint8), torch.empty(4, 110, dtype=torch.uint8)
    for rows, qweight, quant_type in ((6, q8, 8), (16, q8, 8), (32, q8, 8), (16, iq3, 21)):
        fused_mul_mat_gguf(torch.zeros(rows, 32 if quant_type == 8 else 256), qweight, quant_type)
    assert calls == ["mmvq", "mmq", "dequant", "dequant"]


@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")
def test_gguf_expert_prefill_dequant_path_matches_the_gemv():
    import gguf

    from freetoken.moe.fused_q4_0 import _DEQUANT_MIN_TOKENS, fused_experts_gguf_q4_0

    torch.manual_seed(0)
    E, H, I, T, K = 40, 256, 128, _DEQUANT_MIN_TOKENS, 4
    q8 = gguf.GGMLQuantizationType.Q8_0
    quant = lambda w: torch.from_numpy(gguf.quants.quantize(w.numpy(), q8)).reshape(E, -1).cuda()  # noqa: E731
    gate_up, down = quant(torch.randn(E * 2 * I, H) * 0.05), quant(torch.randn(E * H, I) * 0.05)
    # pad each slot like the fixed-width mixed banks do
    gate_up = torch.cat([gate_up, torch.zeros(E, 64, dtype=torch.uint8, device="cuda")], dim=1)
    x = torch.randn(T, H, device="cuda", dtype=torch.bfloat16)
    ids = torch.randint(0, E - 3, (T, K), device="cuda", dtype=torch.int32)  # some experts unused
    weights = torch.rand(T, K, device="cuda")
    kwargs = dict(gate_up_quant_type=8, down_quant_type=8, intermediate_size=I, hidden_size=H)
    gemv = fused_experts_gguf_q4_0(x, gate_up, down, weights, ids, "silu", is_prefill=False, **kwargs)
    prefill = fused_experts_gguf_q4_0(x, gate_up, down, weights, ids, "silu", is_prefill=True, **kwargs)
    cos = torch.nn.functional.cosine_similarity(gemv.float().flatten(), prefill.float().flatten(), dim=0)
    assert cos > 0.999  # the GEMV quantizes activations to q8_1, the prefill GEMM reads them in bf16
