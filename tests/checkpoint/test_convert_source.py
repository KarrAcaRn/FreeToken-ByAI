"""Resolving the convert source: an HF repo id becomes a snapshot dir holding weights AND metadata."""

import fnmatch
import json
import os

import huggingface_hub
import pytest
from freetoken.checkpoint.convert import (
    _copy_metadata,
    _resolve_source,
    _source_fingerprint,
    convert_checkpoint,
)
from freetoken.utils import hf

COMMIT = "0123abcd"
REPO = {
    "config.json": json.dumps({"architectures": ["FakeForCausalLM"]}),
    "generation_config.json": "{}",
    "tokenizer.json": "{}",
    "tokenizer_config.json": "{}",
    "modeling_fake.py": "# remote code",
    "model.safetensors.index.json": json.dumps({"weight_map": {"w": "model-00001-of-00001.safetensors"}}),
    "model-00001-of-00001.safetensors": "shard",
    "pytorch_model.bin": "legacy duplicate",
}


@pytest.fixture
def fake_hub(tmp_path, monkeypatch):
    calls = []
    snap = tmp_path / "hub" / "snapshots" / COMMIT

    def snapshot_download(repo_id, *, revision=None, allow_patterns=None, ignore_patterns=None, **_):
        calls.append({"repo_id": repo_id, "revision": revision})
        if repo_id != "org/model":
            raise huggingface_hub.utils.RepositoryNotFoundError(f"404 {repo_id}")
        for name, body in REPO.items():
            if allow_patterns and not any(fnmatch.fnmatch(name, p) for p in allow_patterns):
                continue
            if ignore_patterns and any(fnmatch.fnmatch(name, p) for p in ignore_patterns):
                continue
            snap.mkdir(parents=True, exist_ok=True)
            (snap / name).write_text(body)
        return str(snap)

    def hf_hub_download(repo_id, filename, **_):
        if repo_id != "org/model":
            raise huggingface_hub.utils.RepositoryNotFoundError(f"404 {repo_id}")
        path = tmp_path / "index.json"
        path.write_text(REPO[filename])
        return str(path)

    monkeypatch.setattr(hf, "snapshot_download", snapshot_download)
    monkeypatch.setattr(hf, "hf_hub_download", hf_hub_download)
    monkeypatch.setattr(huggingface_hub, "snapshot_download", snapshot_download)
    return calls


def test_repo_id_resolves_to_self_contained_snapshot(fake_hub, tmp_path):
    src = _resolve_source("org/model")
    assert sorted(os.listdir(src)) == sorted(n for n in REPO if n != "pytorch_model.bin")
    assert fake_hub[-1]["revision"] == COMMIT

    out = tmp_path / "ftw"
    copied = _copy_metadata(src, str(out))
    assert sorted(copied) == [
        "config.json", "generation_config.json", "modeling_fake.py", "tokenizer.json", "tokenizer_config.json",
    ]
    empty = tmp_path / "empty"
    empty.mkdir()
    assert _source_fingerprint(src, None, device="cpu") != _source_fingerprint(str(empty), None, device="cpu")


def test_local_path_is_untouched(fake_hub, tmp_path):
    assert _resolve_source(str(tmp_path)) == str(tmp_path)
    gguf = tmp_path / "m.gguf"
    gguf.write_bytes(b"")
    assert _resolve_source(str(gguf)) == str(gguf)
    assert fake_hub == []


def test_invalid_repo_id_fails_before_conversion(fake_hub, tmp_path):
    with pytest.raises(SystemExit, match="org/missing"):
        convert_checkpoint("org/missing", str(tmp_path / "ftw"))
    assert not (tmp_path / "ftw").exists()
