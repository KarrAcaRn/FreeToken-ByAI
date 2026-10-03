"""Every NVFP4 family must hand the disk tier a source spec.

The loader releases expert rows ``[K, E)`` for every family, so a family that reaches
that release without an index would serve zeroed experts silently. These tests pin the
hook (``nvfp4_expert_spec``, resolved by ``moe.expert_pieces.nvfp4_expert_spec_of``)
that keeps the disk index and the loader reading the same rows.
"""
from __future__ import annotations

import importlib

import pytest

# Families whose NVFP4 experts load through the shared reader (nvfp4_expert_spec).
NVFP4_FAMILIES = [
    "qwen3_5_moe", "qwen4_exp", "glm4_moe", "glm5_next", "gemma4", "minimax_m2", "minimax_m3",
]


@pytest.mark.parametrize("family", NVFP4_FAMILIES)
def test_family_exposes_a_source_spec_hook(family):
    mod = importlib.import_module(f"freetoken.models.{family}.weight")
    getter = getattr(mod, "nvfp4_expert_spec", None)
    assert callable(getter), (
        f"{family} defines _NVFP4_SOURCE_SPEC but exposes no nvfp4_expert_spec, so "
        "the disk tier cannot build a disk index for it")


@pytest.mark.parametrize(
    "family", [f for f in NVFP4_FAMILIES if f not in ("glm5_next", "glm4_moe", "qwen3_5_moe", "gemma4")]
)
def test_hook_returns_the_spec_the_loader_uses(family):
    # glm5_next and glm4_moe are excluded here only because their hooks read the checkpoint
    # config to pick between the compressed-tensors and modelopt namings; the test below
    # covers them.
    # qwen3_5_moe and gemma4 build their spec from the installed QuantConfig's dialect, so they
    # have no static spec to compare; test_qwen3_5_moe_weight and test_gemma4_compressed_tensors
    # drive the loader through that same hook.
    mod = importlib.import_module(f"freetoken.models.{family}.weight")
    spec = mod.nvfp4_expert_spec("unused/for/these/families", None)
    assert spec is mod._NVFP4_SOURCE_SPEC
    assert spec.key_pattern.groupindex.keys() >= {"layer", "expert", "proj", "kind"}
    assert set(spec.proj_to_role.values()) == {"gate", "up", "down"}


@pytest.mark.parametrize("family", ["glm5_next", "glm4_moe"])
def test_hook_follows_the_checkpoint_quant_method(monkeypatch, family):
    mod = importlib.import_module(f"freetoken.models.{family}.weight")

    class _Cfg:
        def __init__(self, method):
            self.quantization_config = {"quant_method": method}

    monkeypatch.setattr(mod, "cached_load_hf_config", lambda path: _Cfg("compressed-tensors"))
    assert mod.nvfp4_expert_spec("p", None) is mod._NVFP4_CT_SOURCE_SPEC
    monkeypatch.setattr(mod, "cached_load_hf_config", lambda path: _Cfg("modelopt"))
    assert mod.nvfp4_expert_spec("p", None) is mod._NVFP4_SOURCE_SPEC


def test_glm4_moe_compressed_tensors_names_fold_onto_the_modelopt_kinds():
    # gesong2077/GLM-4.5-Air-NVFP4 (llm-compressor): weight_packed | weight_scale |
    # weight_global_scale, plus input_global_scale that the W4A16 expert path never reads.
    from freetoken.models.nvfp4_banks import _canon_kind

    mod = importlib.import_module("freetoken.models.glm4_moe.weight")
    spec = mod._NVFP4_CT_SOURCE_SPEC
    base = "model.layers.3.mlp.experts.17.down_proj."
    kinds = {}
    for suffix in ("weight_packed", "weight_scale", "weight_global_scale", "input_global_scale"):
        m = spec.key_pattern.match(base + suffix)
        kinds[suffix] = _canon_kind(spec, m.group("kind")) if m else None
    assert kinds == {
        "weight_packed": "weight",
        "weight_scale": "weight_scale",
        "weight_global_scale": "weight_scale_2",
        "input_global_scale": None,
    }
    assert spec.global_reciprocal
    # the modelopt spec must not pick up the compressed-tensors names (the bug: only the
    # shared weight_scale spelling matched, so the banks filled with scales and no weights)
    assert not mod._NVFP4_SOURCE_SPEC.key_pattern.match(base + "weight_packed")


def test_provider_refuses_a_family_without_a_spec(monkeypatch):
    """A family with no hook must fail at load, not release rows and serve zeros."""
    from freetoken.layers.quantization import QuantKind
    from freetoken.moe import expert_banks
    from freetoken.moe.disk_tier import DiskTierSpec

    monkeypatch.setattr("freetoken.moe.expert_pieces.nvfp4_expert_spec_of",
                        lambda path, config: None)

    class _Kernel:
        name = "triton"

    class _Method:
        kind = QuantKind.NVFP4
        kernel = _Kernel()

    class _Cfg:
        num_moe_layers = 1
        architectures = ["SomeMoEForCausalLM"]

    with pytest.raises(NotImplementedError, match="nvfp4_expert_spec"):
        expert_banks._method_expert_banks(
            "does/not/matter", _Cfg(), _Method(), None, False,
            False, 8, 8 << 20, disk_tier=DiskTierSpec(ram_experts=1))
