"""Gemma 4 E-series (E2B/E4B): per-layer embeddings, KV-layer sharing and the double-wide MLP on a tiny synthetic config."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
import torch

from freetoken.models.gemma4 import parse_config

_LAYER_TYPES = ["sliding_attention", "sliding_attention", "full_attention"] * 2


def _init_tp() -> None:
    from freetoken.distributed import set_tp_info, try_get_tp_info

    if try_get_tp_info() is None:
        set_tp_info(rank=0, size=1)


def _hf_config(*, eseries: bool = True):
    from transformers import Gemma4TextConfig

    # the 12B/26B/31B configs spell the E-series fields out as off
    extra = (
        dict(hidden_size_per_layer_input=32, vocab_size_per_layer_input=64, num_kv_shared_layers=3, use_double_wide_mlp=True)
        if eseries
        else dict(hidden_size_per_layer_input=0, num_kv_shared_layers=0, use_double_wide_mlp=False)
    )
    return Gemma4TextConfig(
        vocab_size=64, hidden_size=128, intermediate_size=96, num_hidden_layers=6, num_attention_heads=2,
        num_key_value_heads=1, head_dim=64, global_head_dim=128, layer_types=_LAYER_TYPES, sliding_window=8,
        max_position_embeddings=256, **extra,
    )


def test_parse_config_maps_shared_layers_to_the_last_owner_of_their_type():
    config = parse_config(_hf_config())
    # layers 3..5 share: 3, 4 are sliding (last sliding owner 1), 5 is full (owner 2)
    assert config.kv_sharing == ((3, 1), (4, 1), (5, 2))
    assert config.kv_source_layer(4) == 1 and config.kv_source_layer(1) is None
    assert config.per_layer_input_size == 32 and config.per_layer_vocab_size == 64
    assert config.double_wide_shared_mlp and config.pad_token_id == 0
    specs = {spec.name: spec.layer_ids for spec in config.kv_cache_group_specs()}
    assert specs == {"full": (2,), "swa": (0, 1)}
    # the attention groups still cover every layer: shared layers keep their attention type
    assert config.is_swa_layer(3) and not config.is_swa_layer(5)


def test_parse_config_without_eseries_fields_keeps_the_old_layout():
    config = parse_config(_hf_config(eseries=False))
    assert config.kv_sharing == () and config.per_layer_input_size == 0 and not config.double_wide_shared_mlp
    specs = {spec.name: spec.layer_ids for spec in config.kv_cache_group_specs()}
    assert specs == {"full": (2, 5), "swa": (0, 1, 3, 4)}


def _checkpoint_tensors(hf) -> dict:
    H, I, P, L = hf.hidden_size, hf.intermediate_size, hf.hidden_size_per_layer_input, hf.num_hidden_layers
    bf16 = torch.bfloat16
    p = "model.language_model."
    tensors = {
        p + "embed_tokens.weight": torch.randn(hf.vocab_size, H, dtype=bf16),
        p + "embed_tokens_per_layer.weight": torch.randn(hf.vocab_size_per_layer_input, L * P, dtype=bf16),
        p + "per_layer_model_projection.weight": torch.randn(L * P, H, dtype=bf16),
        p + "per_layer_projection_norm.weight": torch.randn(P, dtype=bf16),
        p + "norm.weight": torch.randn(H, dtype=bf16),
        # the real checkpoints ship an audio tower the text model never reads
        "model.audio_tower.layers.0.weight": torch.randn(4, dtype=bf16),
    }
    for i, layer_type in enumerate(hf.layer_types):
        lp = f"{p}layers.{i}."
        D = 128 if layer_type == "full_attention" else 64
        inter = 2 * I if i >= 3 else I
        tensors |= {
            lp + "self_attn.q_proj.weight": torch.randn(2 * D, H, dtype=bf16),
            # shared layers still carry k/v in the real checkpoints; the loader must drop them
            lp + "self_attn.k_proj.weight": torch.randn(D, H, dtype=bf16),
            lp + "self_attn.v_proj.weight": torch.randn(D, H, dtype=bf16),
            lp + "self_attn.k_norm.weight": torch.randn(D, dtype=bf16),
            lp + "self_attn.q_norm.weight": torch.randn(D, dtype=bf16),
            lp + "self_attn.o_proj.weight": torch.randn(H, 2 * D, dtype=bf16),
            lp + "mlp.gate_proj.weight": torch.randn(inter, H, dtype=bf16),
            lp + "mlp.up_proj.weight": torch.randn(inter, H, dtype=bf16),
            lp + "mlp.down_proj.weight": torch.randn(H, inter, dtype=bf16),
            lp + "per_layer_input_gate.weight": torch.randn(P, H, dtype=bf16),
            lp + "per_layer_projection.weight": torch.randn(H, P, dtype=bf16),
            lp + "layer_scalar": torch.randn(1, dtype=bf16),
        }
        for norm in ("input_layernorm", "post_attention_layernorm", "pre_feedforward_layernorm",
                     "post_feedforward_layernorm", "post_per_layer_input_norm"):
            tensors[lp + norm + ".weight"] = torch.randn(H, dtype=bf16)
    return tensors


def test_iter_weights_matches_the_model_state_dict(tmp_path, monkeypatch):
    import safetensors.torch

    import freetoken.models.gemma4.weight as weight
    from freetoken.models.gemma4 import Gemma4ForConditionalGeneration

    _init_tp()
    hf = _hf_config()
    tensors = _checkpoint_tensors(hf)
    safetensors.torch.save_file(tensors, str(tmp_path / "model.safetensors"))
    monkeypatch.setattr(weight, "cached_load_hf_config", lambda _p: hf)
    loaded = dict(weight.iter_weights(str(tmp_path), torch.device("cpu"), include_moe_experts=False, include_non_moe=True))

    model = Gemma4ForConditionalGeneration(parse_config(hf))
    expected = model.state_dict()
    assert set(loaded) == set(expected)
    for key, tensor in expected.items():
        assert loaded[key].shape == tensor.shape, key

    p = "model.language_model.layers."
    assert torch.equal(loaded["model.layers.4.self_attn.q_proj.weight"], tensors[p + "4.self_attn.q_proj.weight"])
    assert not any(k.startswith("model.layers.4.self_attn.") and "k_norm" in k for k in loaded)
    assert loaded["model.layers.0.feed_forward.shared_mlp.gate_up_proj.weight"].shape == (2 * 96, 128)
    assert loaded["model.layers.3.feed_forward.shared_mlp.gate_up_proj.weight"].shape == (4 * 96, 128)
    attn = model.model.layers.op_list
    assert attn[3].self_attn.attn_spec.kv_shared and attn[3].self_attn.kv_source == 1
    assert attn[1].self_attn.publishes_kv and not attn[0].self_attn.publishes_kv


def _build_ft(fn):
    torch.set_default_dtype(torch.bfloat16)
    try:
        with torch.device("cuda"):
            return fn()
    finally:
        torch.set_default_dtype(torch.float32)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")
def test_per_layer_inputs_match_the_reference(monkeypatch):
    from transformers.models.gemma4.modeling_gemma4 import Gemma4TextModel

    import freetoken.models.gemma4.model as ft_model

    _init_tp()
    hf_cfg = _hf_config()
    torch.manual_seed(0)
    ref = Gemma4TextModel(hf_cfg).to("cuda", torch.bfloat16).eval()
    ft = _build_ft(lambda: ft_model.Gemma4Model(parse_config(hf_cfg)))
    ft.embed_tokens_per_layer.weight.copy_(ref.embed_tokens_per_layer.weight)
    ft.per_layer_model_projection.weight.copy_(ref.per_layer_model_projection.weight)
    ft.per_layer_projection_norm.weight.copy_(torch.randn_like(ref.per_layer_projection_norm.weight))
    ref.per_layer_projection_norm.weight.data.copy_(ft.per_layer_projection_norm.weight)

    batch = SimpleNamespace(mm_embeds=None)
    monkeypatch.setattr(ft_model, "get_global_ctx", lambda: SimpleNamespace(batch=batch))
    ids = torch.randint(0, 64, (7,), device="cuda")
    x = ref.embed_tokens(ids[None])[0]
    with torch.no_grad():
        expected = ref.project_per_layer_inputs(x[None], ref.get_per_layer_inputs(ids[None], None))[0]
    torch.testing.assert_close(ft._per_layer_inputs(ids, x), expected, atol=2e-2, rtol=2e-2)

    # image rows read the pad row, the reference's multimodal rule
    batch.mm_embeds, batch.mm_rows = torch.zeros(1, 128, device="cuda"), torch.tensor([2], device="cuda")
    padded = ids.clone()
    padded[2] = hf_cfg.pad_token_id
    with torch.no_grad():
        expected = ref.project_per_layer_inputs(x[None], ref.get_per_layer_inputs(padded[None], None))[0]
    torch.testing.assert_close(ft._per_layer_inputs(ids, x), expected, atol=2e-2, rtol=2e-2)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")
@pytest.mark.parametrize("layer_idx", [1, 4])
def test_decoder_layer_matches_the_reference_around_attention(layer_idx):
    """Everything but attention (stubbed to the same output on both sides): MLP width, PLE gate, layer scalar."""
    from transformers.models.gemma4.modeling_gemma4 import Gemma4TextDecoderLayer

    from freetoken.models.gemma4.model import Gemma4DecoderLayer

    _init_tp()
    hf_cfg = _hf_config()
    torch.manual_seed(0)
    ref = Gemma4TextDecoderLayer(hf_cfg, layer_idx).to("cuda", torch.bfloat16).eval()
    with torch.no_grad():
        for name, param in ref.named_parameters():
            param.copy_(torch.randn_like(param) * (0.1 if "proj" in name or "gate" in name else 1.0))
        ref.layer_scalar.fill_(0.75)
    ft = _build_ft(lambda: Gemma4DecoderLayer(parse_config(hf_cfg), layer_idx, prefix=f"model.layers.{layer_idx}"))

    sd = {k: v for k, v in ref.state_dict().items()}
    mapping = {
        "feed_forward.shared_mlp.gate_up_proj.weight": torch.cat([sd["mlp.gate_proj.weight"], sd["mlp.up_proj.weight"]]),
        "feed_forward.shared_mlp.down_proj.weight": sd["mlp.down_proj.weight"],
        "feed_forward.post_feedforward_layernorm.weight": sd["post_feedforward_layernorm.weight"],
        "feed_forward.layer_scalar": sd["layer_scalar"],
    }
    for key, tensor in ft.state_dict().items():
        if key.startswith("self_attn."):
            continue
        tensor.copy_(mapping[key] if key in mapping else sd[key])
    assert ft.feed_forward.shared_mlp.down_proj.weight.shape[1] == (192 if layer_idx == 4 else 96)

    T, H = 5, hf_cfg.hidden_size
    attn_out = torch.randn(T, H, device="cuda", dtype=torch.bfloat16)
    ft.self_attn.forward = lambda h: attn_out.clone()
    ref.self_attn.forward = lambda *a, **k: (attn_out[None], None)
    x = torch.randn(T, H, device="cuda", dtype=torch.bfloat16)
    ple = torch.randn(T, hf_cfg.hidden_size_per_layer_input, device="cuda", dtype=torch.bfloat16)
    with torch.no_grad():
        expected = ref(x[None].clone(), ple[None], shared_kv_states={})[0]
    torch.testing.assert_close(ft.forward(x.clone(), ple), expected, atol=5e-2, rtol=5e-2)


# --------------------------------------------------------------------------- llama.cpp gemma4 GGUF of an E-series model


def _write_eseries_gguf(path, hf, tensors: dict) -> None:
    """What llama.cpp's converter writes for the E-series: per-layer ``feed_forward_length``, PLE tensors
    under their llama.cpp names, k/v kept on the shared layers. Layer 0 mixes Q8_0 q/k with a Q4_0 v
    (the K-quant presets do the same) and keeps its PLE projections F32."""
    import gguf

    Q8, Q4, F32, F16 = (gguf.GGMLQuantizationType.Q8_0, gguf.GGMLQuantizationType.Q4_0,
                        gguf.GGMLQuantizationType.F32, gguf.GGMLQuantizationType.F16)
    L, P, I = hf.num_hidden_layers, hf.hidden_size_per_layer_input, hf.intermediate_size
    w = gguf.GGUFWriter(str(path), "gemma4")
    for key, value in {
        "block_count": L, "context_length": 256, "embedding_length": hf.hidden_size, "attention.head_count": 2,
        "attention.head_count_kv": 1, "attention.key_length": 128, "attention.value_length": 128,
        "attention.key_length_swa": 64, "attention.value_length_swa": 64, "attention.sliding_window": 8,
        "rope.dimension_count": 128, "rope.dimension_count_swa": 64, "attention.shared_kv_layers": 3,
        "embedding_length_per_layer_input": P,
    }.items():
        w.add_uint32(f"gemma4.{key}", value)
    w.add_array("gemma4.feed_forward_length", [2 * I if i >= 3 else I for i in range(L)])
    w.add_array("gemma4.attention.sliding_window_pattern", [t != "full_attention" for t in hf.layer_types])
    for key, value in {"rope.freq_base": 1e6, "rope.freq_base_swa": 1e4, "attention.layer_norm_rms_epsilon": 1e-6,
                       "final_logit_softcapping": 30.0}.items():
        w.add_float32(f"gemma4.{key}", value)
    w.add_uint32("tokenizer.ggml.padding_token_id", 0)

    def add(name: str, t: torch.Tensor, qtype=F32):
        arr = t.float().contiguous().numpy()
        if qtype == F32:
            w.add_tensor(name, arr)
        elif qtype == F16:
            w.add_tensor(name, arr.astype("float16"))
        else:
            w.add_tensor(name, gguf.quants.quantize(arr, qtype), raw_dtype=qtype)

    p = "model.language_model."
    add("token_embd.weight", tensors[p + "embed_tokens.weight"], Q8)
    add("per_layer_token_embd.weight", tensors[p + "embed_tokens_per_layer.weight"], Q8)
    add("per_layer_model_proj.weight", tensors[p + "per_layer_model_projection.weight"], F16)
    add("per_layer_proj_norm.weight", tensors[p + "per_layer_projection_norm.weight"])
    add("output_norm.weight", tensors[p + "norm.weight"])
    add("rope_freqs.weight", torch.tensor([1.0] * 16 + [1e30] * 48))  # partial rotary 0.25 of 128
    names = {
        "self_attn.q_proj.weight": "attn_q", "self_attn.k_proj.weight": "attn_k", "self_attn.v_proj.weight": "attn_v",
        "self_attn.o_proj.weight": "attn_output", "mlp.gate_proj.weight": "ffn_gate", "mlp.up_proj.weight": "ffn_up",
        "mlp.down_proj.weight": "ffn_down", "per_layer_input_gate.weight": "inp_gate", "per_layer_projection.weight": "proj",
        "self_attn.q_norm.weight": "attn_q_norm", "self_attn.k_norm.weight": "attn_k_norm",
        "input_layernorm.weight": "attn_norm", "post_attention_layernorm.weight": "post_attention_norm",
        "pre_feedforward_layernorm.weight": "ffn_norm", "post_feedforward_layernorm.weight": "post_ffw_norm",
        "post_per_layer_input_norm.weight": "post_norm", "layer_scalar": "layer_output_scale",
    }
    for i in range(L):
        for hf_name, gg in names.items():
            t = tensors[f"{p}layers.{i}.{hf_name}"]
            qtype = F32
            if t.ndim == 2:
                qtype = Q4 if (i, gg) == (0, "attn_v") else F32 if (i == 0 and gg in ("inp_gate", "proj")) else Q8
            add(f"blk.{i}.{gg}.weight", t, qtype)
    w.write_header_to_file()
    w.write_kv_data_to_file()
    w.write_tensors_to_file()
    w.close()


@pytest.fixture(scope="module")
def eseries_gguf(tmp_path_factory):
    torch.manual_seed(3)
    hf = _hf_config()
    tensors = _checkpoint_tensors(hf)
    path = tmp_path_factory.mktemp("gguf") / "gemma4-eseries-tiny.gguf"
    _write_eseries_gguf(path, hf, tensors)
    return str(path), hf, tensors


def test_gguf_config_reads_the_eseries_fields(eseries_gguf):
    from freetoken.models.gemma4.gguf import parse_gguf_config
    from freetoken.utils import cached_load_hf_config

    path, hf, _tensors = eseries_gguf
    config, ref = parse_gguf_config(cached_load_hf_config(path)), parse_config(hf)
    for field in ("kv_sharing", "per_layer_input_size", "per_layer_vocab_size", "double_wide_shared_mlp",
                  "intermediate_size", "pad_token_id", "num_kv_heads", "head_dim"):
        assert getattr(config, field) == getattr(ref, field), field
    # the E-series stores attn_v on its full layers, so they are not k_eq_v like the 12B/26B/31B
    assert not config.attention_group_for_layer(2).k_eq_v
    assert config.kv_cache_group_specs() == ref.kv_cache_group_specs()


def test_gguf_weights_fill_the_eseries_model(eseries_gguf):
    from freetoken.models.gemma4 import Gemma4ForCausalLM
    from freetoken.models.gemma4.gguf import iter_gguf_weights, parse_gguf_config
    from freetoken.models.gguf.dequant import GGML_Q8_0, dequantize
    from freetoken.utils import cached_load_hf_config

    _init_tp()
    path, hf, tensors = eseries_gguf
    loaded = {n: t.clone() for n, t in iter_gguf_weights(path, torch.device("cpu"), include_moe_experts=False, include_non_moe=True)}
    expected = Gemma4ForCausalLM(parse_gguf_config(cached_load_hf_config(path))).state_dict()
    assert set(loaded) == set(expected)
    for key, tensor in expected.items():
        assert loaded[key].shape == tensor.shape, key

    def q8(packed: torch.Tensor, cols: int) -> torch.Tensor:
        return dequantize(packed.reshape(-1), GGML_Q8_0, torch.float32).reshape(-1, cols)

    p, tol = "model.language_model.layers.", dict(atol=0.05, rtol=0.05)
    # Q8_0 q|k and a Q4_0 v cannot share one packed tensor: two runs, still the q, k, v row order
    torch.testing.assert_close(
        q8(loaded["model.layers.0.self_attn.qkv_proj.runs.0.qweight"], 128),
        torch.cat([tensors[p + "0.self_attn.q_proj.weight"], tensors[p + "0.self_attn.k_proj.weight"]]).float(), **tol)
    assert loaded["model.layers.0.self_attn.qkv_proj.runs.1.qweight"].shape[0] == 64
    # a shared layer keeps only q; its k / v / k_norm are dropped, its MLP is double-wide
    torch.testing.assert_close(q8(loaded["model.layers.4.self_attn.q_proj.qweight"], 128),
                               tensors[p + "4.self_attn.q_proj.weight"].float(), **tol)
    assert not any(k.startswith("model.layers.4.self_attn.") and ("k_norm" in k or "qkv" in k) for k in loaded)
    assert loaded["model.layers.3.feed_forward.shared_mlp.gate_up_proj.qweight"].shape[0] == 4 * 96
    # unquantized PLE tensors load dense, quantized ones stay packed
    assert torch.equal(loaded["model.layers.0.per_layer_input_gate.weight"], tensors[p + "0.per_layer_input_gate.weight"])
    assert "model.layers.1.per_layer_input_gate.qweight" in loaded
    torch.testing.assert_close(loaded["model.per_layer_model_projection.weight"].float(),
                               tensors["model.language_model.per_layer_model_projection.weight"].float())
    torch.testing.assert_close(q8(loaded["model.embed_tokens_per_layer.qweight"], 6 * 32),
                               tensors["model.language_model.embed_tokens_per_layer.weight"].float(), **tol)
    torch.testing.assert_close(loaded["model.layers.5.post_per_layer_input_norm.weight"],
                               tensors[p + "5.post_per_layer_input_norm.weight"])
