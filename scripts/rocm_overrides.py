"""Print uv overrides that pin the ROCm PyTorch stack already installed in this environment.

    python scripts/rocm_overrides.py > /tmp/rocm-overrides.txt
    uv pip install --no-build-isolation --overrides /tmp/rocm-overrides.txt -e .

pyproject.toml pins torch/torchvision/triton for the CUDA build. On ROCm the vendor image
supplies them, so the overrides replace those pins with the exact installed versions: uv then
keeps the ROCm builds or fails, and can never swap in a CUDA wheel from PyPI.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

import torch


def _installed(name: str) -> str | None:
    try:
        return version(name)
    except PackageNotFoundError:
        return None


def main() -> None:
    if getattr(torch.version, "hip", None) is None:
        raise SystemExit("the installed torch is not a ROCm build; use the regular install")
    for name in ("torch", "torchvision", "triton"):
        installed = _installed(name)
        if installed is not None:
            print(f"{name}=={installed}")
    if _installed("triton") is None and _installed("pytorch-triton-rocm") is not None:
        # Upstream ROCm wheels ship Triton under this name; a never-true marker drops the
        # project's triton requirement so the CUDA wheel is not installed over it.
        print("triton; python_version < '0'")


if __name__ == "__main__":
    main()
