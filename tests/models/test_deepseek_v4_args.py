import json

import pytest

huggingface_hub = pytest.importorskip("huggingface_hub")

from freetoken.models.deepseek_v4.args import _config_path


def _cached_repo(cache, repo_id, files):
    """Lay out an HF hub cache entry (refs/main -> one snapshot) holding ``files``."""
    repo = cache / f"models--{repo_id.replace('/', '--')}"
    snapshot = repo / "snapshots" / "abc123"
    for name, body in files.items():
        path = snapshot / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(body))
    (repo / "refs").mkdir(parents=True)
    (repo / "refs" / "main").write_text("abc123")
    return snapshot


@pytest.fixture
def offline_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(huggingface_hub.constants, "HF_HUB_CACHE", str(tmp_path))
    monkeypatch.setattr(huggingface_hub.constants, "HF_HUB_OFFLINE", True)
    return tmp_path


def test_config_path_resolves_a_repo_id_through_the_hub_cache(offline_cache):
    snapshot = _cached_repo(offline_cache, "org/dsv4", {"inference/config.json": {"dim": 8}})
    assert _config_path("org/dsv4") == str(snapshot / "inference" / "config.json")


def test_config_path_falls_back_to_model_args_json_for_a_repo_id(offline_cache):
    snapshot = _cached_repo(offline_cache, "org/dsv4", {"model_args.json": {"dim": 8}})
    assert _config_path("org/dsv4") == str(snapshot / "model_args.json")


def test_config_path_raises_when_neither_file_exists(offline_cache, tmp_path):
    _cached_repo(offline_cache, "org/dsv4", {"config.json": {}})
    with pytest.raises(FileNotFoundError):
        _config_path("org/dsv4")
    with pytest.raises(FileNotFoundError):
        _config_path(str(tmp_path))  # a local directory without the file


def test_config_path_prefers_inference_config_in_a_local_dir(tmp_path):
    (tmp_path / "inference").mkdir()
    (tmp_path / "inference" / "config.json").write_text("{}")
    (tmp_path / "model_args.json").write_text("{}")
    assert _config_path(str(tmp_path)) == str(tmp_path / "inference" / "config.json")
