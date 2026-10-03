"""qwen4_exp weight loading against synthetic checkpoints shaped like the released ones.

The tensors are tiny but the key names, dtypes and the fusion geometry that matters
(hc_lowrank=320 + hc_count=4 -> a 12-row zero pad; 128-row block scales) are the real ones.
"""

from __future__ import annotations

import json
import random
from types import SimpleNamespace

import pytest
import torch
from safetensors.torch import save_file

from freetoken.distributed import set_tp_info, try_get_tp_info
from freetoken.kernel.aot_models import SUPPORTED_MODELS, expert_bank_row_bytes
from freetoken.models.qwen4_exp.weight import (
    _ZERO_CENTERED_NORM_SUFFIXES,
    _DenseFuser,
    iter_weights,
    load_ple_table,
)
from freetoken.models.register import get_model_spec
from freetoken.moe.host_banks import HostBank, read_range_into

from .common import LM, RADIXARK_NVFP4, hf_config, install_quant_config, meta_state_dict, mixed_precision_quant

H = 128  # hidden_size; every block-fp8 projection needs in/out multiples of 128
HC = 4  # hc_count
LR = 320  # hc_lowrank; kept real so the merged HC pad is the real (-(320+4)) % 16 = 12
HCH = HC * H  # hyper-connection stream width
KH, VH, HD = 2, 4, 32  # GDN key / value heads, head dim: qkv rows 256, z rows 128
QH, KVH, AHD = 4, 2, 64  # QSA q / kv heads, head dim: q rows 512, k / v rows 128
IHD = 64  # indexer head dim
BLOCK = 128
E, I = 3, 6  # routed experts, moe_intermediate_size
NGRAM_DIM, NGRAM_ROWS, NGRAM_SHARDS = 4, 7, 4


@pytest.fixture(scope="session", autouse=True)
def _tp_info():
    if try_get_tp_info() is None:
        set_tp_info(rank=0, size=1)


def _bf16(*shape: int) -> torch.Tensor:
    return torch.randn(*shape).to(torch.bfloat16)


def _hc_weights(prefix: str, inject: bool) -> dict[str, torch.Tensor]:
    w = {
        f"{prefix}.hc_norm.weight": _bf16(HCH),
        f"{prefix}.input_mix_weight_down.weight": _bf16(LR, HCH),
        f"{prefix}.input_mix_weight_up.weight": _bf16(HCH, LR),
    }
    if inject:
        w[f"{prefix}.block_inject_weight.weight"] = _bf16(HC, HCH)
    return w


def _fp8_scale(weight: torch.Tensor) -> torch.Tensor:
    return torch.rand(weight.shape[0] // BLOCK, weight.shape[1] // BLOCK) + 0.5


def _raw_checkpoint(dense_fp8: bool = False) -> dict[str, torch.Tensor]:
    """Layer 0 = GDN + PLE, layer 1 = QSA; plus the mtp / visual / routed-expert noise.

    ``dense_fp8`` stores the attention and GDN qkv|z / out projections as 128x128 block-fp8 (e4m3 ``.weight`` + fp32 ``.weight_scale_inv``) like the community NVFP4-FP8 requants.
    """
    lm = "model.language_model"
    raw: dict[str, torch.Tensor] = {
        f"{lm}.embed_tokens.weight": _bf16(11, H),
        "lm_head.weight": _bf16(11, H),
    }
    raw.update(_hc_weights(f"{lm}.hyper_connection_mixer", inject=False))
    for layer in (0, 1):
        raw.update(_hc_weights(f"{lm}.layers.{layer}.attn_hyper_connection", inject=True))
        raw.update(_hc_weights(f"{lm}.layers.{layer}.mlp_hyper_connection", inject=True))
        raw.update({
            f"{lm}.layers.{layer}.mlp.gate.weight": _bf16(E, H),
            f"{lm}.layers.{layer}.mlp.shared_expert.gate_proj.weight": _bf16(I, H),
            f"{lm}.layers.{layer}.mlp.shared_expert.up_proj.weight": _bf16(I, H),
            f"{lm}.layers.{layer}.mlp.shared_expert.down_proj.weight": _bf16(H, I),
            f"{lm}.layers.{layer}.mlp.shared_expert_gate.weight": _bf16(1, H),
        })
        for expert in range(E):
            base = f"{lm}.layers.{layer}.mlp.experts.{expert}"
            for proj, out, inn in (("gate_proj", I, H), ("up_proj", I, H), ("down_proj", H, I)):
                raw[f"{base}.{proj}.weight"] = torch.randint(
                    0, 256, (out, inn // 2), dtype=torch.uint8
                )
                raw[f"{base}.{proj}.weight_scale"] = torch.ones(
                    out, inn // 16 or 1, dtype=torch.float8_e4m3fn
                )
                raw[f"{base}.{proj}.weight_scale_2"] = torch.tensor(0.5)
                raw[f"{base}.{proj}.input_scale"] = torch.tensor(0.25)
    gdn = f"{lm}.layers.0.linear_attn"
    raw.update({
        f"{gdn}.in_proj_qkv.weight": _bf16(2 * KH * HD + VH * HD, H),
        f"{gdn}.in_proj_z.weight": _bf16(VH * HD, H),
        f"{gdn}.in_proj_b.weight": _bf16(VH, H),
        f"{gdn}.in_proj_a.weight": _bf16(VH, H),
        f"{gdn}.conv1d.weight": _bf16(2 * KH * HD + VH * HD, 1, 4),
        f"{gdn}.A_log": _bf16(VH),
        f"{gdn}.dt_bias": _bf16(VH),
        f"{gdn}.norm.weight": _bf16(HD),
        f"{gdn}.out_proj.weight": _bf16(H, VH * HD),
    })
    ple = f"{lm}.layers.0.ple"
    raw.update({
        f"{ple}.key_proj.weight": _bf16(HCH, H),
        f"{ple}.value_proj.weight": _bf16(H, H),
        f"{ple}.norm_key.weight": _bf16(HCH),
        f"{ple}.norm_query.weight": _bf16(HCH),
        f"{ple}.norm_conv.weight": _bf16(HCH),
        f"{ple}.conv1d.weight": _bf16(HCH, 1, 4),
        f"{ple}.ple_embedding.layer_multipliers": torch.randint(1, 1 << 40, (3,)),
        f"{ple}.ple_embedding.ngram_heads_offsets": torch.arange(4),
        f"{ple}.ple_embedding.ngram_heads_vocab_sizes": torch.full((4,), 5),
    })
    attn = f"{lm}.layers.1.self_attn"
    raw.update({
        f"{attn}.q_proj.weight": _bf16(2 * QH * AHD, H),
        f"{attn}.k_proj.weight": _bf16(KVH * AHD, H),
        f"{attn}.v_proj.weight": _bf16(KVH * AHD, H),
        f"{attn}.o_proj.weight": _bf16(H, QH * AHD),
        f"{attn}.q_norm.weight": _bf16(AHD),
        f"{attn}.k_norm.weight": _bf16(AHD),
        f"{attn}.indexer.index_qk_proj.weight": _bf16(5 * IHD, H),
        f"{attn}.indexer.q_layernorm.weight": _bf16(IHD),
        f"{attn}.indexer.k_layernorm.weight": _bf16(IHD),
    })
    raw.update({
        "mtp.hyper_connection_mixer.hc_norm.weight": _bf16(HCH),
        "mtp.layers.0.self_attn.q_proj.weight": _bf16(2 * QH * AHD, H),
        "mtp.layers.0.mlp.experts.gate_up_proj": _bf16(E, 2 * I, H),
        "mtp.layers.0.mlp.experts.down_proj": _bf16(E, H, I),
        "model.visual.blocks.0.attn.qkv.weight": _bf16(3 * H, H),
        "model.visual.merger.norm.weight": _bf16(H),
    })
    if dense_fp8:
        for module in (f"{gdn}.in_proj_qkv", f"{gdn}.in_proj_z", f"{gdn}.out_proj",
                       *(f"{attn}.{p}_proj" for p in "qkvo")):
            weight = raw[f"{module}.weight"]
            raw[f"{module}.weight"] = weight.to(torch.float8_e4m3fn)
            raw[f"{module}.weight_scale_inv"] = _fp8_scale(weight)
    return raw


FP8_DENSE_QUANT = mixed_precision_quant(gdn_layers=(0,), attn_layers=(1,), moe_layers=(0, 1))


def _config_json(quantization_config) -> dict:
    cfg = hf_config(
        num_layers=2, head_dim=AHD, num_q=QH, num_kv=KVH, index_head_dim=IHD, index_heads=2,
        budget=16, hidden=H, max_position=4096, rope_theta=10000.0,
        layer_types=["linear_attention", "full_attention"],
        linear_num_key_heads=KH, linear_num_value_heads=VH,
        linear_key_head_dim=HD, linear_value_head_dim=HD,
        hc_lowrank=LR, ple_layer_ids=[1],
        num_experts=E, moe_intermediate_size=I, shared_expert_intermediate_size=I,
    )
    return {**vars(cfg), "text_config": vars(cfg.text_config), "quantization_config": quantization_config}


def _ngram_table() -> tuple[dict[str, torch.Tensor], torch.Tensor]:
    prefix = "model.language_model.layers.0.ple.ple_embedding.ngram_embedding"
    shards = {
        f"{prefix}.shard_{i}.weight": (
            torch.arange(i * NGRAM_ROWS * NGRAM_DIM, (i + 1) * NGRAM_ROWS * NGRAM_DIM)
            .remainder(200).to(torch.uint8).view(NGRAM_ROWS, NGRAM_DIM).view(torch.float8_e4m3fn)
        )
        for i in range(NGRAM_SHARDS)
    }
    scale = torch.tensor([0.125], dtype=torch.bfloat16)
    shards[f"{prefix}.weight_scale"] = scale
    return shards, scale


def _write_checkpoint(folder, raw: dict[str, torch.Tensor], quantization_config) -> tuple[str, dict[str, torch.Tensor]]:
    table, _scale = _ngram_table()
    # Spread the dense tensors over two shards so the fusion buffer has to survive a file
    # boundary, and put the n-gram table in its own shards like the real checkpoint does.
    names = sorted(raw)
    save_file({n: raw[n] for n in names[::2]}, str(folder / "model-bf16-00001.safetensors"))
    save_file({n: raw[n] for n in names[1::2]}, str(folder / "model-bf16-00002.safetensors"))
    shard_names = sorted(table)
    save_file({n: table[n] for n in shard_names[:2]}, str(folder / "model-plefp8-00000.safetensors"))
    save_file({n: table[n] for n in shard_names[2:]}, str(folder / "model-plefp8-00001.safetensors"))
    (folder / "config.json").write_text(json.dumps(_config_json(quantization_config)))
    return str(folder), {**raw, **table}


def _load(folder: str, *, vision: bool = True) -> dict[str, torch.Tensor]:
    install_quant_config(folder)
    return {
        name: tensor.clone()
        for name, tensor in iter_weights(
            folder, torch.device("cpu"), include_moe_experts=True, include_non_moe=True, include_vision=vision
        )
    }


@pytest.fixture(scope="module")
def checkpoint(tmp_path_factory) -> tuple[str, dict[str, torch.Tensor]]:
    torch.manual_seed(0)
    return _write_checkpoint(tmp_path_factory.mktemp("qwen4_exp_ckpt"), _raw_checkpoint(), None)


@pytest.fixture(scope="module")
def loaded(checkpoint) -> dict[str, torch.Tensor]:
    return _load(checkpoint[0])


@pytest.fixture(scope="module")
def checkpoint_fp8(tmp_path_factory) -> tuple[str, dict[str, torch.Tensor]]:
    torch.manual_seed(1)
    return _write_checkpoint(
        tmp_path_factory.mktemp("qwen4_exp_fp8_ckpt"), _raw_checkpoint(dense_fp8=True), FP8_DENSE_QUANT
    )


@pytest.fixture(scope="module")
def loaded_fp8(checkpoint_fp8) -> dict[str, torch.Tensor]:
    return _load(checkpoint_fp8[0])


def test_tower_keys_come_out_under_the_prefix_load_weight_filters(loaded):
    assert {n for n in loaded if "visual" in n} == {"visual.blocks.0.attn.qkv.weight", "visual.merger.norm.weight"}


def test_mtp_experts_and_table_never_loaded(loaded):
    for name in loaded:
        assert not name.startswith("mtp.")
        assert ".mlp.experts." not in name
        assert "ngram_embedding" not in name
        assert not name.endswith((".weight_scale", ".weight_scale_2", ".input_scale", ".weight_scale_inv"))


def test_hc_merge_is_down_then_inject_then_zero_pad(loaded, checkpoint):
    _folder, raw = checkpoint
    key = "model.layers.0.attn_hyper_connection.input_mix_weight_down_block_inject.weight"
    merged = loaded[key]
    assert merged.shape == (LR + HC + 12, HCH)  # pad = (-(320 + 4)) % 16
    down = raw["model.language_model.layers.0.attn_hyper_connection.input_mix_weight_down.weight"]
    inject = raw["model.language_model.layers.0.attn_hyper_connection.block_inject_weight.weight"]
    assert torch.equal(merged[:LR], down)
    assert torch.equal(merged[LR:LR + HC], inject)
    assert torch.equal(merged[LR + HC:], torch.zeros(12, HCH, dtype=merged.dtype))


def test_top_level_mixer_keeps_the_unmerged_down(loaded, checkpoint):
    _folder, raw = checkpoint
    got = loaded["model.hyper_connection_mixer.input_mix_weight_down.weight"]
    assert got.shape == (LR, HCH)
    assert torch.equal(
        got, raw["model.language_model.hyper_connection_mixer.input_mix_weight_down.weight"]
    )
    assert torch.equal(
        loaded["model.hyper_connection_mixer.input_mix_weight_up.weight"],
        raw["model.language_model.hyper_connection_mixer.input_mix_weight_up.weight"],
    )


def test_qkv_fusion_slices_back_to_q_k_v(loaded, checkpoint):
    _folder, raw = checkpoint
    attn = "model.language_model.layers.1.self_attn"
    parts = [raw[f"{attn}.{p}_proj.weight"] for p in ("q", "k", "v")]
    fused = loaded["model.layers.1.self_attn.qkv_proj.weight"]
    assert fused.shape == (2 * QH * AHD + 2 * KVH * AHD, H)  # q carries the output gate
    for part, back in zip(parts, torch.split(fused, [p.shape[0] for p in parts], dim=0)):
        assert torch.equal(part, back)


def test_gdn_in_proj_slices_round_trip(loaded, checkpoint):
    _folder, raw = checkpoint
    gdn = "model.language_model.layers.0.linear_attn"
    parts = [raw[f"{gdn}.in_proj_{p}.weight"] for p in ("qkv", "z", "b", "a")]
    fused = loaded["model.layers.0.linear_attn.in_proj.weight"]
    assert fused.shape == (sum(p.shape[0] for p in parts), H)
    splits = torch.split(fused, [p.shape[0] for p in parts], dim=0)
    for part, back in zip(parts, splits):
        assert torch.equal(part, back)


def test_shared_expert_gate_up_merge(loaded, checkpoint):
    _folder, raw = checkpoint
    base = "model.language_model.layers.1.mlp.shared_expert"
    merged = loaded["model.layers.1.mlp.shared_expert.gate_up_proj.weight"]
    assert torch.equal(merged[:I], raw[f"{base}.gate_proj.weight"])
    assert torch.equal(merged[I:], raw[f"{base}.up_proj.weight"])


ZERO_CENTERED = (
    "model.layers.0.attn_hyper_connection.hc_norm.weight",
    "model.layers.0.mlp_hyper_connection.hc_norm.weight",
    "model.hyper_connection_mixer.hc_norm.weight",
    "model.layers.0.ple.norm_key.weight",
    "model.layers.0.ple.norm_query.weight",
    "model.layers.0.ple.norm_conv.weight",
    "model.layers.1.self_attn.q_norm.weight",
    "model.layers.1.self_attn.k_norm.weight",
    "model.layers.1.self_attn.indexer.q_layernorm.weight",
    "model.layers.1.self_attn.indexer.k_layernorm.weight",
)


def test_zero_centered_norms_are_loaded_raw(loaded, checkpoint):
    """(1+w) is applied at runtime in fp32, so the loader must not fold it into the bf16 weight."""
    _folder, raw = checkpoint
    for name in ZERO_CENTERED:
        raw_name = name.replace("model.", "model.language_model.", 1)
        assert torch.equal(loaded[name], raw[raw_name]), name


def test_the_zero_centered_suffix_list_covers_every_such_norm():
    assert {n for n in ZERO_CENTERED if n.endswith(_ZERO_CENTERED_NORM_SUFFIXES)} == set(ZERO_CENTERED)
    assert not "model.layers.0.linear_attn.norm.weight".endswith(_ZERO_CENTERED_NORM_SUFFIXES)


def test_gdn_gated_norm_passes_through(loaded, checkpoint):
    _folder, raw = checkpoint
    assert torch.equal(
        loaded["model.layers.0.linear_attn.norm.weight"],
        raw["model.language_model.layers.0.linear_attn.norm.weight"],
    )


def test_hash_constants_stay_int64(loaded):
    for leaf in ("layer_multipliers", "ngram_heads_offsets", "ngram_heads_vocab_sizes"):
        assert loaded[f"model.layers.0.ple.ple_embedding.{leaf}"].dtype is torch.int64


def _ple_args(**overrides) -> SimpleNamespace:
    """A config addressing exactly NGRAM_SHARDS x NGRAM_ROWS rows: one head over the prime 23, padded to 28."""
    fields = dict(ngram_size=2, num_ngram_heads=1, ngram_vocab_size_base=23,
                  make_ngram_vocab_size_divisible_by=NGRAM_SHARDS * NGRAM_ROWS,
                  split_ngram_parts=NGRAM_SHARDS, ngram_head_dim=NGRAM_DIM)
    return SimpleNamespace(**{**fields, **overrides})


def test_load_ple_table_concatenates_shards_in_index_order(checkpoint):
    folder, raw = checkpoint
    table = load_ple_table(folder, _ple_args(), pin=False)
    assert table.tensor.shape == (NGRAM_SHARDS * NGRAM_ROWS, NGRAM_DIM)
    assert table.tensor.dtype is torch.float8_e4m3fn
    prefix = "model.language_model.layers.0.ple.ple_embedding.ngram_embedding"
    for shard in range(NGRAM_SHARDS):
        rows = table.tensor[shard * NGRAM_ROWS: (shard + 1) * NGRAM_ROWS]
        assert torch.equal(rows.view(torch.uint8),
                           raw[f"{prefix}.shard_{shard}.weight"].view(torch.uint8))
    assert table.weight_scale.dtype is torch.bfloat16
    assert float(table.weight_scale) == 0.125


def test_load_ple_table_rejects_a_shard_count_mismatch(checkpoint):
    folder, _raw = checkpoint
    with pytest.raises(ValueError, match=r"shards 0\.\.4, found 4 \(missing \[4\]"):
        load_ple_table(folder, _ple_args(split_ngram_parts=NGRAM_SHARDS + 1), pin=False)


# ======================================================================================
# PLE shard-set validation (both backends) and the pinned load's admission / cleanup
# ======================================================================================

_PLE_PREFIX = "model.language_model.layers.0.ple.ple_embedding.ngram_embedding"


@pytest.fixture
def ple_folder(tmp_path):
    """Just the n-gram table, one file; returns (folder, the file, its tensors)."""
    tensors, _scale = _ngram_table()
    path = tmp_path / "model-plefp8-00000.safetensors"
    save_file(tensors, str(path))
    return tmp_path, path, tensors


def _rewrite(path, tensors=None, header_fn=None):
    """Re-save ``tensors`` to ``path``, then let ``header_fn`` edit the raw safetensors header in place."""
    if tensors is not None:
        save_file(tensors, str(path))
    if header_fn is not None:
        data = path.read_bytes()
        n = int.from_bytes(data[:8], "little")
        header = json.loads(data[8:8 + n])
        header_fn(header)
        blob = json.dumps(header).encode()
        blob += b" " * (-len(blob) % 8)
        path.write_bytes(len(blob).to_bytes(8, "little") + blob + data[8 + n:])


def _shard(i: int) -> str:
    return f"{_PLE_PREFIX}.shard_{i}.weight"


def test_scan_ple_table_maps_both_backends(ple_folder):
    from freetoken.models.qwen4_exp.ple_disk import source_from_safetensors
    from freetoken.models.qwen4_exp.weight import scan_ple_table

    folder, path, tensors = ple_folder
    shards = scan_ple_table(str(folder), _ple_args())
    assert (shards.total_rows, shards.cols, float(shards.scale)) == (NGRAM_SHARDS * NGRAM_ROWS, NGRAM_DIM, 0.125)
    data = path.read_bytes()
    for i, (file, offset) in enumerate(shards.parts):
        assert file == str(path)
        assert data[offset:offset + NGRAM_ROWS * NGRAM_DIM] == tensors[_shard(i)].view(torch.uint8).numpy().tobytes()
    source = source_from_safetensors(str(folder), _ple_args())
    assert source.paths == [str(path)] and source.extent_file == [0] * NGRAM_SHARDS
    assert source.extent_base == [offset for _, offset in shards.parts]
    assert (source.total_rows, source.row_bytes, source.scale) == (NGRAM_SHARDS * NGRAM_ROWS, NGRAM_DIM, 0.125)


def _with(tensors, **changes):
    out = dict(tensors)
    for key, value in changes.items():
        if value is None:
            del out[key]
        else:
            out[key] = value
    return out


_SCALE = f"{_PLE_PREFIX}.weight_scale"
_FP8 = torch.float8_e4m3fn


@pytest.mark.parametrize("edit, match", [
    (lambda t: _with(t, **{_shard(2): t[_shard(2)].view(torch.uint8)}),
     r"shard_2\.weight in .*model-plefp8-00000\.safetensors: dtype U8, expected F8_E4M3"),
    (lambda t: _with(t, **{_shard(3): torch.zeros(NGRAM_ROWS + 1, NGRAM_DIM, dtype=_FP8)}),
     r"shard_3\.weight in .*: shape \[8, 4\], expected \[7, 4\]"),
    (lambda t: _with(t, **{_shard(0): torch.zeros(NGRAM_ROWS * NGRAM_DIM, dtype=_FP8)}),
     r"shard_0\.weight in .*: shape \[28\], expected 2-D"),
    (lambda t: _with(t, **{_shard(3): None, _shard(4): t[_shard(3)]}),
     r"expected shards 0\.\.3, found 4 \(missing \[3\], unexpected \[4\]\)"),
    (lambda t: _with(t, **{f"{_PLE_PREFIX}.shard_01.weight": t[_shard(1)].clone()}),
     r"shard_0?1\.weight in .*: duplicate index 1, already read .*shard_0?1\.weight"),
    (lambda t: _with(t, **{_SCALE: None}), r"no .*weight_scale tensor"),
    (lambda t: _with(t, **{_SCALE: torch.tensor([0.0], dtype=torch.bfloat16)}), r"finite positive value, got \[0\.0\]"),
    (lambda t: _with(t, **{_SCALE: torch.tensor(-1.0, dtype=torch.bfloat16)}), r"finite positive value, got -1\.0"),
    (lambda t: _with(t, **{_SCALE: torch.tensor(float("nan"), dtype=torch.bfloat16)}), r"finite positive value, got nan"),
    (lambda t: _with(t, **{_SCALE: torch.tensor(float("inf"), dtype=torch.bfloat16)}), r"finite positive value, got inf"),
    (lambda t: _with(t, **{_SCALE: torch.ones(2, dtype=torch.bfloat16)}), r"finite positive value, got \[1\.0, 1\.0\]"),
])
def test_scan_ple_table_rejects_a_bad_shard_set(ple_folder, edit, match):
    from freetoken.models.qwen4_exp.weight import scan_ple_table

    folder, path, tensors = ple_folder
    _rewrite(path, edit(tensors))
    with pytest.raises(ValueError, match=match):
        scan_ple_table(str(folder), _ple_args())


def test_scan_ple_table_rejects_a_second_scale(ple_folder):
    from freetoken.models.qwen4_exp.weight import scan_ple_table

    folder, _path, _tensors = ple_folder
    save_file({_SCALE: torch.tensor(0.5, dtype=torch.bfloat16)}, str(folder / "model-plefp8-00001.safetensors"))
    with pytest.raises(ValueError, match=r"00001\.safetensors: expected one scale, already read .*00000\.safetensors"):
        scan_ple_table(str(folder), _ple_args())


def test_scan_ple_table_rejects_bad_data_offsets(ple_folder):
    from freetoken.models.qwen4_exp.weight import scan_ple_table

    folder, path, _tensors = ple_folder

    def shrink(header):
        begin, end = header[_shard(1)]["data_offsets"]
        header[_shard(1)]["data_offsets"] = [begin, end - 1]

    _rewrite(path, header_fn=shrink)
    with pytest.raises(ValueError, match=r"shard_1\.weight in .*: data_offsets \[\d+, \d+\), expected 28 bytes"):
        scan_ple_table(str(folder), _ple_args())

    # a truncated file: the last tensor's bytes run past EOF
    _rewrite(path, _ngram_table()[0])
    path.write_bytes(path.read_bytes()[:-3])
    with pytest.raises(ValueError, match=r"data_offsets .* within the file's \d+ data bytes"):
        scan_ple_table(str(folder), _ple_args())


@pytest.mark.parametrize("overrides", [
    dict(split_ngram_parts=NGRAM_SHARDS - 1),
    dict(ngram_head_dim=NGRAM_DIM * 2),
    dict(make_ngram_vocab_size_divisible_by=32),  # 23 padded to 32 rows, the shards hold 28
])
def test_scan_ple_table_rejects_a_config_mismatch(ple_folder, overrides):
    from freetoken.models.qwen4_exp.weight import ple_table_rows, scan_ple_table

    folder, _path, _tensors = ple_folder
    args = _ple_args(**overrides)
    with pytest.raises(ValueError, match=rf"expected {'shards' if 'split_ngram_parts' in overrides else ple_table_rows(args)}"):
        scan_ple_table(str(folder), args)


def test_ple_table_rows_pads_like_hf():
    from freetoken.models.qwen4_exp.config import parse_config
    from freetoken.models.qwen4_exp.weight import ple_table_rows

    args = parse_config(hf_config()).qwen4_args
    # 4 heads over the primes after 999: 1009 + 1013 + 1019 + 1021 = 4062, padded to a multiple of 8
    assert ple_table_rows(args) == 4064


def _no_bank(*_args, **_kwargs):
    raise AssertionError("HostBank allocated")


def test_load_ple_table_validates_before_allocating(ple_folder, monkeypatch):
    import freetoken.models.qwen4_exp.weight as weight

    folder, path, tensors = ple_folder
    _rewrite(path, _with(tensors, **{_SCALE: None}))
    monkeypatch.setattr(weight, "HostBank", _no_bank)
    with pytest.raises(ValueError, match="weight_scale"):
        load_ple_table(str(folder), _ple_args(), pin=False)


def test_load_ple_table_refuses_a_table_larger_than_host_ram(ple_folder, monkeypatch):
    import freetoken.models.qwen4_exp.weight as weight

    folder, _path, _tensors = ple_folder
    monkeypatch.setattr("freetoken.memory.available_host_memory", lambda: weight._PLE_HOST_MARGIN)
    monkeypatch.setattr(weight, "HostBank", _no_bank)
    with pytest.raises(MemoryError, match=r"0\.0 GiB of host RAM plus 4 GiB headroom, .* 4\.0 GiB; use --ple-backend disk"):
        load_ple_table(str(folder), _ple_args(), pin=False)

    monkeypatch.undo()
    monkeypatch.setattr("freetoken.memory.available_host_memory", lambda: None)  # unknown -> proceed
    assert load_ple_table(str(folder), _ple_args(), pin=False).tensor.shape == (NGRAM_SHARDS * NGRAM_ROWS, NGRAM_DIM)


@pytest.mark.parametrize("stage", ["fill", "pin", "fill+free"])
def test_load_ple_table_frees_the_bank_on_failure(ple_folder, monkeypatch, stage):
    import freetoken.models.qwen4_exp.weight as weight
    from freetoken.moe import host_banks

    folder, _path, _tensors = ple_folder
    banks: list[HostBank] = []

    class _Tracked(HostBank):
        __slots__ = ()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            banks.append(self)

    def fail(*_args, **_kwargs):
        raise OSError("disk went away")

    monkeypatch.setattr(weight, "HostBank", _Tracked)
    monkeypatch.setattr("freetoken.memory.available_host_memory", lambda: None)
    if stage == "pin":
        monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
        monkeypatch.setattr(_Tracked, "pin", fail)
    else:
        monkeypatch.setattr(weight, "read_range_into", fail)
    if stage == "fill+free":
        def free_fails(self):
            raise RuntimeError("free failed")

        monkeypatch.setattr(_Tracked, "free", free_fails)
    live = len(host_banks._LIVE_BUFFERS)

    with pytest.raises(OSError, match="disk went away"):  # never masked by the cleanup
        load_ple_table(str(folder), _ple_args())
    assert len(banks) == 1
    if stage != "fill+free":
        assert len(host_banks._LIVE_BUFFERS) == live
        assert all(b is not banks[0]._buf for b in host_banks._LIVE_BUFFERS)
        assert not banks[0].tensor.view(torch.uint8).any()  # the filled pages were dropped


# ======================================================================================
# read_range_into: the O_DIRECT byte-range read the PLE table load is built on
# ======================================================================================


@pytest.fixture(scope="module")
def blob(tmp_path_factory) -> tuple[str, bytes]:
    data = random.Random(7).randbytes(5_000_003)
    path = tmp_path_factory.mktemp("blob") / "data.bin"
    path.write_bytes(data)
    return str(path), data


@pytest.mark.parametrize("file_offset, nbytes, dest_offset", [
    (1, 4095, 0),                 # sub-block, unaligned source
    (2239, 1_000_000, 0),         # the real checkpoint's header-end phase
    (4095, 4097, 1),              # straddles two block boundaries
    (4_999_000, 1003, 123_456),   # runs to EOF
])
def test_read_range_into_matches_the_file(blob, file_offset, nbytes, dest_offset):
    path, data = blob
    bank = HostBank((6_000_000,), torch.uint8)
    view = bank.memoryview()
    got = read_range_into(view, path, file_offset=file_offset, nbytes=nbytes,
                          dest_offset=dest_offset, chunk=1 << 20)
    assert got == nbytes
    assert bytes(view[dest_offset:dest_offset + nbytes]) == data[file_offset:file_offset + nbytes]


def test_read_range_into_is_chunk_and_thread_safe(blob):
    path, data = blob
    bank = HostBank((6_000_000,), torch.uint8)
    view = bank.memoryview()
    read_range_into(view, path, file_offset=2239, nbytes=4_000_000, dest_offset=1024,
                    workers=8, chunk=64 << 10)
    assert bytes(view[1024:1024 + 4_000_000]) == data[2239:2239 + 4_000_000]


def test_read_range_into_rejects_a_short_destination(blob):
    path, _data = blob
    bank = HostBank((1024,), torch.uint8)
    with pytest.raises(ValueError, match="destination holds"):
        read_range_into(bank.memoryview(), path, file_offset=0, nbytes=1 << 20)


# ======================================================================================
# AOT shape table
# ======================================================================================


def test_aot_entry_carries_the_checkpoint_geometry():
    entry = next(m for m in SUPPORTED_MODELS
                 if m.architecture == "Qwen4ExpForConditionalGeneration")
    assert (entry.hidden_size, entry.moe_intermediate_size, entry.top_k) == (2560, 640, 10)
    assert entry.kv_groups == ((2, 256),)
    rows = expert_bank_row_bytes("nvfp4", entry.hidden_size, entry.moe_intermediate_size)
    assert set(rows) == {"gate_up_packed", "gate_up_scale", "gate_up_global",
                         "down_packed", "down_scale", "down_global"}
    for name, nbytes in rows.items():
        assert nbytes % 16 == 0, name  # fused multi-bank copy only engages on 16B multiples


def test_every_registry_architecture_is_claimed_by_an_aot_entry():
    from freetoken.models.register import _MODEL_REGISTRY

    claimed = {m.architecture for m in SUPPORTED_MODELS}
    claimed |= {a for m in SUPPORTED_MODELS for a in m.arch_aliases}
    assert "Qwen4ExpForConditionalGeneration" in claimed
    assert set(_MODEL_REGISTRY) - claimed == set()


@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs cuda")
def test_fusion_pad_rides_the_tensor_device():
    """safetensors loads straight to cuda; a cpu-allocated pad row would break torch.cat."""
    fuser = _DenseFuser(None, get_model_spec("Qwen4ExpForConditionalGeneration").packed_modules_mapping)
    down = torch.randn(320, 64, device="cuda", dtype=torch.bfloat16)
    inject = torch.randn(4, 64, device="cuda", dtype=torch.bfloat16)
    assert fuser.fuse("model.layers.0.attn_hyper_connection.input_mix_weight_down.weight", down) == []
    [(key, fused)] = fuser.fuse("model.layers.0.attn_hyper_connection.block_inject_weight.weight", inject)
    assert key == "model.layers.0.attn_hyper_connection.input_mix_weight_down_block_inject.weight"
    assert fused.device.type == "cuda" and fused.shape[0] == 336
    assert torch.equal(fused[324:], torch.zeros(12, 64, device="cuda", dtype=torch.bfloat16))


# ======================================================================================
# the reader against the model the engine builds, for each released quant layout
# ======================================================================================


@pytest.fixture(scope="module")
def checkpoint_nvfp4(tmp_path_factory) -> tuple[str, dict[str, torch.Tensor]]:
    """bf16 dense tensors under a real ModelOptConfig whose ignore list covers them (RadixArk)."""
    torch.manual_seed(2)
    return _write_checkpoint(tmp_path_factory.mktemp("qwen4_exp_nvfp4_ckpt"), _raw_checkpoint(), RADIXARK_NVFP4)


FP8_MODULES = (
    "model.layers.1.self_attn.qkv_proj", "model.layers.1.self_attn.o_proj",
    "model.layers.0.linear_attn.in_proj_qkvz", "model.layers.0.linear_attn.out_proj",
)


@pytest.mark.parametrize("fixture", ["checkpoint", "checkpoint_nvfp4", "checkpoint_fp8"])
def test_emitted_keys_are_the_model_state_dict(fixture, request):
    """The reader fills exactly the buffers the engine builds from the same config, block-fp8 ones with the stored dtypes."""
    folder, _raw = request.getfixturevalue(fixture)
    loaded, state = _load(folder, vision=False), meta_state_dict(folder)
    assert set(loaded) == set(state)
    if fixture != "checkpoint_fp8":
        assert loaded["model.layers.0.linear_attn.in_proj.weight"].dtype is torch.bfloat16
        return
    for module in FP8_MODULES:
        for kind in (".weight", ".weight_scale_inv"):
            assert loaded[module + kind].shape == state[module + kind].shape, module + kind
        assert loaded[module + ".weight"].dtype is state[module + ".weight"].dtype is torch.float8_e4m3fn
        assert loaded[module + ".weight_scale_inv"].dtype is torch.float32  # the engine casts it to the bf16 buffer at load


def _assert_fused_per_kind(loaded, raw, fused: str, parts: list[str]) -> None:
    for kind in (".weight", ".weight_scale_inv"):
        sources = [raw[f"{p}{kind}"].view(torch.uint8) for p in parts]
        merged = loaded[fused + kind]
        assert merged.dtype is raw[f"{parts[0]}{kind}"].dtype
        for source, back in zip(sources, torch.split(merged.view(torch.uint8), [s.shape[0] for s in sources], dim=0)):
            assert torch.equal(source, back)


def test_fp8_projections_fuse_per_kind(loaded_fp8, checkpoint_fp8):
    _folder, raw = checkpoint_fp8
    attn, gdn = f"{LM}.layers.1.self_attn", f"{LM}.layers.0.linear_attn"
    _assert_fused_per_kind(loaded_fp8, raw, "model.layers.1.self_attn.qkv_proj", [f"{attn}.{p}_proj" for p in "qkv"])
    _assert_fused_per_kind(loaded_fp8, raw, "model.layers.0.linear_attn.in_proj_qkvz", [f"{gdn}.in_proj_qkv", f"{gdn}.in_proj_z"])
    assert torch.equal(loaded_fp8["model.layers.0.linear_attn.out_proj.weight_scale_inv"], raw[f"{gdn}.out_proj.weight_scale_inv"])
    assert torch.equal(
        loaded_fp8["model.layers.0.linear_attn.in_proj_ba.weight"],
        torch.cat([raw[f"{gdn}.in_proj_b.weight"], raw[f"{gdn}.in_proj_a.weight"]], dim=0),
    )
    for name in ("model.layers.0.linear_attn.in_proj_ba.weight", "model.layers.1.mlp.shared_expert.gate_up_proj.weight",
                 "model.layers.1.self_attn.indexer.index_qk_proj.weight", "lm_head.weight",
                 "model.hyper_connection_mixer.input_mix_weight_down.weight",
                 "model.layers.0.attn_hyper_connection.input_mix_weight_down_block_inject.weight"):
        assert loaded_fp8[name].dtype is torch.bfloat16


ATTN = f"{LM}.layers.1.self_attn"
REJECTED = [
    pytest.param(None, lambda w: {f"{ATTN}.q_proj.weight": w, f"{ATTN}.q_proj.weight_scale_inv": _fp8_scale(w)},
                 r"q_proj\.weight_scale_inv", id="scale the config does not declare"),
    pytest.param(None, lambda w: {f"{ATTN}.o_proj.weight": w.to(torch.float8_e4m3fn)},
                 r"o_proj\.weight is torch\.float8", id="fp8 weight the config declares bf16"),
    pytest.param(FP8_DENSE_QUANT, lambda w: {f"{ATTN}.{p}_proj.weight": w.clone() for p in "qkv"},
                 r"[qkv]_proj\.weight is torch\.bfloat16", id="bf16 weight the config declares fp8"),
    pytest.param(FP8_DENSE_QUANT, lambda w: {f"{ATTN}.q_proj.weight": w[:-64].to(torch.float8_e4m3fn), f"{ATTN}.q_proj.weight_scale_inv": _fp8_scale(w)},
                 "128x128", id="part that is not a 128-row multiple"),
]


@pytest.mark.parametrize("quantization_config, tensors, match", REJECTED)
def test_checkpoint_disagreeing_with_its_quant_config_is_rejected(tmp_path, quantization_config, tensors, match):
    save_file(tensors(_bf16(2 * QH * AHD, H)), str(tmp_path / "model.safetensors"))
    (tmp_path / "config.json").write_text(json.dumps(_config_json(quantization_config)))
    with pytest.raises(ValueError, match=match):
        _load(str(tmp_path))
