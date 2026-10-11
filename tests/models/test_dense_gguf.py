"""Dense llama.cpp GGUFs (``llama`` / ``qwen2`` / ``qwen3``) against tiny synthetic files written with gguf-py."""

from __future__ import annotations

import pytest
import torch

from freetoken.distributed import set_tp_info, try_get_tp_info
from freetoken.utils import cached_load_hf_config
from tests.models.test_qwen3_5_moe_weight import _meta_state_dict

H, Q, KV, D, I, VOCAB, L = 64, 2, 1, 64, 96, 64, 2  # rope needs head dim 64+

pytestmark = pytest.mark.filterwarnings("ignore::UserWarning")


@pytest.fixture(scope="module", autouse=True)
def _tp_info():
    if try_get_tp_info() is None:
        set_tp_info(rank=0, size=1)


def _llama_cpp_permute(w: torch.Tensor, n_head: int) -> torch.Tensor:
    """``convert_hf_to_gguf.LlamaModel.permute``: HF half-rotation rows -> llama.cpp interleaved rows."""
    return w.reshape(n_head, 2, w.shape[0] // n_head // 2, *w.shape[1:]).swapaxes(1, 2).reshape(w.shape)


def _raw() -> dict[str, torch.Tensor]:
    r = lambda *s: torch.randn(*s) * 0.5  # noqa: E731
    raw = {"embed": r(VOCAB, H), "lm_head": r(VOCAB, H), "norm": r(H), "rope_freqs": 1 + torch.rand(D // 2) * 7}
    for layer in range(L):
        raw.update({f"{layer}.{k}": v for k, v in {
            "input_norm": r(H), "post_norm": r(H), "q_norm": r(D), "k_norm": r(D),
            "q": r(Q * D, H), "k": r(KV * D, H), "v": r(KV * D, H), "o": r(H, Q * D),
            "q_bias": r(Q * D), "k_bias": r(KV * D), "v_bias": r(KV * D),
            "gate": r(I, H), "up": r(I, H), "down": r(H, I),
        }.items()})
    return raw


def _write_gguf(path, arch: str, raw: dict[str, torch.Tensor]) -> None:
    """What llama.cpp's converter writes: llama permutes q / k for its interleaved rope, ships
    Llama 3's rope scaling as rope_freqs and ties the embedding (no output.weight); qwen2 carries
    qkv biases, qwen3 q / k norms. Layer 0 keeps v and up in Q4_0 next to Q8_0 (the *_M mixes)."""
    import gguf

    Q8, Q4, F32 = gguf.GGMLQuantizationType.Q8_0, gguf.GGMLQuantizationType.Q4_0, gguf.GGMLQuantizationType.F32
    w = gguf.GGUFWriter(str(path), arch)
    for key, value in {
        "block_count": L, "context_length": 4096, "embedding_length": H, "feed_forward_length": I,
        "attention.head_count": Q, "attention.head_count_kv": KV, "attention.key_length": D,
        "attention.value_length": D, "rope.dimension_count": D,
    }.items():
        w.add_uint32(f"{arch}.{key}", value)
    w.add_float32(f"{arch}.rope.freq_base", 5e5)
    w.add_float32(f"{arch}.attention.layer_norm_rms_epsilon", 1e-5)

    def add(name: str, t: torch.Tensor, qtype=F32):
        arr = t.float().contiguous().numpy()
        if qtype == F32:
            w.add_tensor(name, arr)
        else:
            w.add_tensor(name, gguf.quants.quantize(arr, qtype), raw_dtype=qtype)

    add("token_embd.weight", raw["embed"], Q8)
    if arch == "llama":
        add("rope_freqs.weight", raw["rope_freqs"])
    else:
        add("output.weight", raw["lm_head"], Q8)
    add("output_norm.weight", raw["norm"])
    for layer in range(L):
        blk, x = f"blk.{layer}", lambda k: raw[f"{layer}.{k}"]  # noqa: E731
        q, k = x("q"), x("k")
        if arch == "llama":
            q, k = _llama_cpp_permute(q, Q), _llama_cpp_permute(k, KV)
        add(f"{blk}.attn_norm.weight", x("input_norm"))
        add(f"{blk}.ffn_norm.weight", x("post_norm"))
        if arch == "qwen3":
            add(f"{blk}.attn_q_norm.weight", x("q_norm"))
            add(f"{blk}.attn_k_norm.weight", x("k_norm"))
        add(f"{blk}.attn_q.weight", q, Q8)
        add(f"{blk}.attn_k.weight", k, Q8)
        add(f"{blk}.attn_v.weight", x("v"), Q4 if layer == 0 else Q8)
        if arch == "qwen2":
            for part in ("q", "k", "v"):
                add(f"{blk}.attn_{part}.bias", x(f"{part}_bias"))
        add(f"{blk}.attn_output.weight", x("o"), Q8)
        add(f"{blk}.ffn_gate.weight", x("gate"), Q8)
        add(f"{blk}.ffn_up.weight", x("up"), Q4 if layer == 0 else Q8)
        add(f"{blk}.ffn_down.weight", x("down"), Q8)
    w.write_header_to_file()
    w.write_kv_data_to_file()
    w.write_tensors_to_file()
    w.close()


@pytest.fixture(scope="module", params=["llama", "qwen2", "qwen3"])
def dense_gguf(request, tmp_path_factory):
    torch.manual_seed(5)
    raw = _raw()
    path = tmp_path_factory.mktemp("gguf") / f"{request.param}-tiny.gguf"
    _write_gguf(path, request.param, raw)
    return request.param, str(path), raw


def _weights(path: str) -> dict[str, torch.Tensor]:
    from freetoken.models.gguf.dense import iter_gguf_weights

    return {n: t.clone() for n, t in iter_gguf_weights(path, torch.device("cpu"), include_moe_experts=True, include_non_moe=True)}


def _q8(packed: torch.Tensor, cols: int) -> torch.Tensor:
    from freetoken.models.gguf.dequant import GGML_Q8_0, dequantize

    return dequantize(packed.reshape(-1), GGML_Q8_0, torch.float32).reshape(-1, cols)


def test_unpermute_inverts_llama_cpp_permute():
    from freetoken.models.gguf.dense import unpermute_llama_rows

    w = torch.arange(4 * 64 * 3).reshape(4 * 64, 3)
    assert torch.equal(unpermute_llama_rows(_llama_cpp_permute(w, 4), 4), w)


def test_config_has_the_hf_geometry(dense_gguf):
    from freetoken.models.gguf.dense import parse_gguf_config

    arch, path, raw = dense_gguf
    shim = cached_load_hf_config(path)
    assert shim.architectures == [{"llama": "LlamaGGUFForCausalLM", "qwen2": "Qwen2GGUFForCausalLM",
                                   "qwen3": "Qwen3GGUFForCausalLM"}[arch]]
    config = parse_gguf_config(shim)
    assert (config.num_layers, config.num_qo_heads, config.num_kv_heads, config.head_dim) == (L, Q, KV, D)
    assert config.intermediate_size == I and not config.moe_enabled and config.rotary_config.base == 5e5
    assert config.tie_word_embeddings == (arch == "llama")
    scaling = config.rotary_config.scaling
    if arch == "llama":
        assert scaling["rope_type"] == "freq_factors"
        torch.testing.assert_close(torch.tensor(scaling["factors"]), raw["rope_freqs"])
    else:
        assert scaling is None


def test_emitted_keys_are_the_model_state_dict(dense_gguf):
    arch, path, _raw = dense_gguf
    loaded, state = _weights(path), _meta_state_dict(path)
    assert set(loaded) == set(state)
    for key, tensor in loaded.items():
        assert tensor.shape == state[key].shape, key
    # layer 0's Q4_0 v / up cannot share a packed tensor with their Q8_0 neighbours
    assert "model.layers.0.self_attn.qkv_proj.runs.1.qweight" in loaded
    assert "model.layers.0.mlp.gate_up_proj.runs.1.qweight" in loaded
    assert ("model.layers.0.self_attn.qkv_proj.bias" in loaded) == (arch == "qwen2")


def test_tensors_load_in_hf_layout(dense_gguf):
    arch, path, raw = dense_gguf
    got = _weights(path)
    tol = dict(atol=0.03, rtol=0.03)  # Q8_0
    # llama's q / k come back in HF row order (the permutation undone on the packed rows)
    torch.testing.assert_close(_q8(got["model.layers.1.self_attn.qkv_proj.qweight"], H),
                               torch.cat([raw["1.q"], raw["1.k"], raw["1.v"]]), **tol)
    torch.testing.assert_close(_q8(got["model.layers.0.self_attn.qkv_proj.runs.0.qweight"], H),
                               torch.cat([raw["0.q"], raw["0.k"]]), **tol)
    torch.testing.assert_close(_q8(got["model.layers.1.mlp.gate_up_proj.qweight"], H),
                               torch.cat([raw["1.gate"], raw["1.up"]]), **tol)
    torch.testing.assert_close(_q8(got["model.layers.0.mlp.down_proj.qweight"], I), raw["0.down"], **tol)
    if arch == "qwen2":
        torch.testing.assert_close(got["model.layers.0.self_attn.qkv_proj.bias"].float(),
                                   torch.cat([raw["0.q_bias"], raw["0.k_bias"], raw["0.v_bias"]]), atol=0.01, rtol=0.01)
    if arch == "qwen3":
        torch.testing.assert_close(got["model.layers.1.self_attn.q_norm.weight"].float(), raw["1.q_norm"], atol=0.01, rtol=0.01)
    assert ("lm_head.qweight" in got) == (arch != "llama")


def test_freq_factors_rope_divides_the_frequencies():
    from freetoken.layers.rotary import _rope_frequencies

    factors = tuple(float(f) for f in 1 + torch.arange(D // 2) / 4)
    base, _ = _rope_frequencies(D, D, 5e5, None)
    scaled, attn = _rope_frequencies(D, D, 5e5, {"rope_type": "freq_factors", "factors": factors})
    torch.testing.assert_close(scaled, base / torch.tensor(factors))
    assert attn == 1.0
