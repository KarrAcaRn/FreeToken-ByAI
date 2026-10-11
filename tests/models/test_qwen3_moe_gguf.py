"""llama.cpp ``qwen3moe`` GGUF (Qwen3-30B-A3B) against a tiny synthetic file written with gguf-py."""

from __future__ import annotations

import pytest
import torch

from freetoken.distributed import set_tp_info, try_get_tp_info
from freetoken.utils import cached_load_hf_config
from tests.models.test_qwen3_5_moe_weight import _meta_state_dict

H, Q, KV, D = 64, 2, 1, 64  # hidden, q / kv heads, head dim (rope needs 64+)
E, I, VOCAB, L = 4, 32, 64, 2  # routed experts, expert width, vocab, layers

pytestmark = pytest.mark.filterwarnings("ignore::UserWarning")


@pytest.fixture(scope="module", autouse=True)
def _tp_info():
    if try_get_tp_info() is None:
        set_tp_info(rank=0, size=1)


def _hf_tensors() -> dict[str, torch.Tensor]:
    r = lambda *s: torch.randn(*s) * 0.5  # noqa: E731
    raw = {"embed": r(VOCAB, H), "lm_head": r(VOCAB, H), "norm": r(H)}
    for layer in range(L):
        raw.update({f"{layer}.{k}": v for k, v in {
            "input_norm": r(H), "post_norm": r(H), "q_norm": r(D), "k_norm": r(D), "router": r(E, H),
            "q": r(Q * D, H), "k": r(KV * D, H), "v": r(KV * D, H), "o": r(H, Q * D),
            "exp_gate": r(E, I, H), "exp_up": r(E, I, H), "exp_down": r(E, H, I),
        }.items()})
    return raw


def _write_gguf(path, raw: dict[str, torch.Tensor]) -> None:
    """What llama.cpp's converter writes for qwen3moe: tensors unchanged. Layer 0 keeps v in Q4_0
    next to a Q8_0 q / k (the *_M presets mix types the same way), layer 1's down bank is Q4_0."""
    import gguf

    Q8, Q4, F32 = gguf.GGMLQuantizationType.Q8_0, gguf.GGMLQuantizationType.Q4_0, gguf.GGMLQuantizationType.F32
    w = gguf.GGUFWriter(str(path), "qwen3moe")
    for key, value in {
        "block_count": L, "context_length": 4096, "embedding_length": H, "feed_forward_length": 3 * H,
        "attention.head_count": Q, "attention.head_count_kv": KV, "attention.key_length": D,
        "attention.value_length": D, "expert_count": E, "expert_used_count": 2, "expert_feed_forward_length": I,
    }.items():
        w.add_uint32(f"qwen3moe.{key}", value)
    w.add_float32("qwen3moe.rope.freq_base", 1e6)
    w.add_float32("qwen3moe.attention.layer_norm_rms_epsilon", 1e-6)

    def add(name: str, t: torch.Tensor, qtype=F32):
        arr = t.float().contiguous().numpy()
        if qtype == F32:
            w.add_tensor(name, arr)
        else:
            w.add_tensor(name, gguf.quants.quantize(arr, qtype), raw_dtype=qtype)

    add("token_embd.weight", raw["embed"], Q8)
    add("output.weight", raw["lm_head"], Q8)
    add("output_norm.weight", raw["norm"])
    for layer in range(L):
        blk, x = f"blk.{layer}", lambda k: raw[f"{layer}.{k}"]  # noqa: E731
        add(f"{blk}.attn_norm.weight", x("input_norm"))
        add(f"{blk}.ffn_norm.weight", x("post_norm"))
        add(f"{blk}.attn_q_norm.weight", x("q_norm"))
        add(f"{blk}.attn_k_norm.weight", x("k_norm"))
        add(f"{blk}.ffn_gate_inp.weight", x("router"))
        add(f"{blk}.attn_q.weight", x("q"), Q8)
        add(f"{blk}.attn_k.weight", x("k"), Q8)
        add(f"{blk}.attn_v.weight", x("v"), Q4 if layer == 0 else Q8)
        add(f"{blk}.attn_output.weight", x("o"), Q8)
        add(f"{blk}.ffn_gate_exps.weight", x("exp_gate"), Q8)
        add(f"{blk}.ffn_up_exps.weight", x("exp_up"), Q8)
        add(f"{blk}.ffn_down_exps.weight", x("exp_down"), Q8 if layer == 0 else Q4)
    w.write_header_to_file()
    w.write_kv_data_to_file()
    w.write_tensors_to_file()
    w.close()


@pytest.fixture(scope="module")
def qwen3moe_gguf(tmp_path_factory):
    torch.manual_seed(11)
    raw = _hf_tensors()
    path = tmp_path_factory.mktemp("gguf") / "qwen3moe-tiny.gguf"
    _write_gguf(path, raw)
    return str(path), raw


def _weights(path: str) -> dict[str, torch.Tensor]:
    from freetoken.models.qwen3_moe.gguf import iter_gguf_weights

    return {n: t.clone() for n, t in iter_gguf_weights(path, torch.device("cpu"), include_moe_experts=False, include_non_moe=True)}


def _q8(packed: torch.Tensor, cols: int) -> torch.Tensor:
    from freetoken.models.gguf.dequant import GGML_Q8_0, dequantize

    return dequantize(packed.reshape(-1), GGML_Q8_0, torch.float32).reshape(-1, cols)


def test_config_has_the_hf_geometry(qwen3moe_gguf):
    from freetoken.models.qwen3_moe.gguf import parse_gguf_config

    path, _raw = qwen3moe_gguf
    shim = cached_load_hf_config(path)
    assert shim.architectures == ["Qwen3MoeGGUFForCausalLM"]
    config = parse_gguf_config(shim)
    assert (config.num_layers, config.num_qo_heads, config.num_kv_heads, config.head_dim) == (L, Q, KV, D)
    assert (config.num_experts, config.num_experts_per_tok, config.moe_intermediate_size) == (E, 2, I)
    assert config.norm_topk_prob and not config.tie_word_embeddings and config.moe_enabled
    assert config.rotary_config.rotary_dim == D and config.rotary_config.base == 1e6
    layout = config.gguf_quant_types
    assert layout["expert_gate_up"] == (8, 8) and layout["expert_down"] == (8, 2)
    assert layout["tensors"]["blk.0.attn_v.weight"] == 2 and "blk.0.ffn_up_exps.weight" not in layout["tensors"]


def test_emitted_keys_are_the_model_state_dict(qwen3moe_gguf):
    path, _raw = qwen3moe_gguf
    loaded, state = _weights(path), _meta_state_dict(path)
    assert set(loaded) == set(state)
    for key, tensor in loaded.items():
        assert tensor.shape == state[key].shape, key
    # the Q4_0 v of layer 0 cannot share a packed tensor with its Q8_0 q / k
    assert "model.layers.0.self_attn.qkv_proj.runs.1.qweight" in loaded
    assert "model.layers.1.self_attn.qkv_proj.qweight" in loaded


def test_tensors_load_unchanged(qwen3moe_gguf):
    path, raw = qwen3moe_gguf
    got = _weights(path)
    tol = dict(atol=0.03, rtol=0.03)  # Q8_0
    torch.testing.assert_close(_q8(got["model.layers.1.self_attn.qkv_proj.qweight"], H),
                               torch.cat([raw["1.q"], raw["1.k"], raw["1.v"]]), **tol)
    torch.testing.assert_close(_q8(got["model.layers.0.self_attn.qkv_proj.runs.0.qweight"], H),
                               torch.cat([raw["0.q"], raw["0.k"]]), **tol)
    torch.testing.assert_close(_q8(got["model.layers.0.self_attn.o_proj.qweight"], Q * D), raw["0.o"], **tol)
    torch.testing.assert_close(_q8(got["lm_head.qweight"], H), raw["lm_head"], **tol)
    # plain RMSNorm weights: llama.cpp stores qwen3moe norms without the Gemma 1 + w shift
    for key, ref in (("model.norm.weight", raw["norm"]), ("model.layers.1.input_layernorm.weight", raw["1.input_norm"]),
                     ("model.layers.0.post_attention_layernorm.weight", raw["0.post_norm"]),
                     ("model.layers.0.self_attn.k_norm.weight", raw["0.k_norm"]),
                     ("model.layers.1.mlp.gate.weight", raw["1.router"])):
        torch.testing.assert_close(got[key].float(), ref, atol=0.01, rtol=0.01)


def test_expert_banks_hold_each_experts_gate_then_up_rows(qwen3moe_gguf, monkeypatch):
    import gguf

    from freetoken.models.gguf.dequant import row_bytes
    from freetoken.models.qwen3_moe.gguf import load_q4_0_expert_sources, parse_gguf_config

    path, _raw = qwen3moe_gguf
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    banks = load_q4_0_expert_sources(path, parse_gguf_config(cached_load_hf_config(path)))
    src = {t.name: torch.from_numpy(t.data.copy()).view(torch.uint8).reshape(E, -1) for t in gguf.GGUFReader(path).tensors
           if "_exps." in t.name}
    gate_bytes = I * row_bytes(H, 8)
    for layer in range(L):
        assert torch.equal(banks["gate_up"][layer][:, :gate_bytes], src[f"blk.{layer}.ffn_gate_exps.weight"])
        assert torch.equal(banks["gate_up"][layer][:, gate_bytes:], src[f"blk.{layer}.ffn_up_exps.weight"])
        dn = src[f"blk.{layer}.ffn_down_exps.weight"]
        assert torch.equal(banks["down"][layer][:, : dn.shape[1]], dn)
