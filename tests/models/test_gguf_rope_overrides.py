"""Rope-only --hf-overrides on a GGUF: YaRN merges into the parser's rope dict, everything else is refused."""

from types import SimpleNamespace

import pytest

from freetoken.models.gguf.config import apply_rope_overrides, build_gguf_shim

_YARN = {"rope_type": "yarn", "factor": 4.0, "original_max_position_embeddings": 32768}


def _shim(overrides: dict) -> SimpleNamespace:
    return SimpleNamespace(model_path="/models/anon.gguf", overrides=overrides)


def test_a_yarn_override_keeps_the_files_rope_theta():
    hf = SimpleNamespace(rope_scaling={"rope_theta": 1e6, "rope_type": "default"}, max_position_embeddings=40960)
    apply_rope_overrides(_shim({"rope_scaling": _YARN, "max_position_embeddings": 131072}), hf)
    assert hf.rope_scaling == {"rope_theta": 1e6, **_YARN}
    assert hf.max_position_embeddings == 131072


def test_the_hf_type_spelling_and_a_file_without_scaling_work():
    hf = SimpleNamespace(rope_scaling=None, max_position_embeddings=8192)
    apply_rope_overrides(_shim({"rope_parameters": {"type": "yarn", "factor": 2.0}}), hf)
    assert hf.rope_scaling == {"rope_type": "yarn", "factor": 2.0}
    assert hf.max_position_embeddings == 8192


def test_no_override_leaves_the_config_alone():
    hf = SimpleNamespace(rope_scaling={"rope_theta": 1e6, "rope_type": "default"}, max_position_embeddings=40960)
    apply_rope_overrides(_shim({}), hf)
    assert hf.rope_scaling == {"rope_theta": 1e6, "rope_type": "default"}


@pytest.mark.parametrize(
    ("existing", "override"),
    [({"rope_type": "default"}, {"rope_type": "linear", "factor": 2.0}), ({"rope_type": "llama3", "factor": 8.0}, _YARN)],
    ids=["not-yarn", "on-top-of-llama3"],
)
def test_other_rope_overrides_are_refused(existing, override):
    hf = SimpleNamespace(rope_scaling=existing, max_position_embeddings=8192)
    with pytest.raises(NotImplementedError):
        apply_rope_overrides(_shim({"rope_scaling": override}), hf)


def test_non_rope_override_keys_are_refused_before_reading_the_file():
    with pytest.raises(ValueError, match="accepts only"):
        build_gguf_shim("/nonexistent.gguf", {"num_hidden_layers": 2})
