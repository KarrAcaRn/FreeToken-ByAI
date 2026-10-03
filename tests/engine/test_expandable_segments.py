from __future__ import annotations

import torch

from freetoken.engine import engine


def _run(monkeypatch, *, accelerator_api: bool) -> list[str]:
    calls: list[str] = []
    monkeypatch.delenv("PYTORCH_ALLOC_CONF", raising=False)
    monkeypatch.delenv("PYTORCH_CUDA_ALLOC_CONF", raising=False)
    monkeypatch.setattr(torch.cuda.memory, "_set_allocator_settings", lambda s: calls.append(f"cuda:{s}"))
    if accelerator_api:
        monkeypatch.setattr(torch._C, "_accelerator_setAllocatorSettings", lambda s: calls.append(f"acc:{s}"), raising=False)
    else:
        monkeypatch.delattr(torch._C, "_accelerator_setAllocatorSettings", raising=False)
    engine._ensure_expandable_segments()
    return calls


def test_prefers_the_accelerator_api(monkeypatch):
    # torch 2.11 deprecates torch.cuda.memory._set_allocator_settings for this one.
    assert _run(monkeypatch, accelerator_api=True) == ["acc:expandable_segments:True"]


def test_falls_back_to_the_cuda_api(monkeypatch):
    assert _run(monkeypatch, accelerator_api=False) == ["cuda:expandable_segments:True"]
