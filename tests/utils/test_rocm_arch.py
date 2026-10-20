import ast
import hashlib
import importlib
import os
import pathlib
import sys
import types
from types import SimpleNamespace

import torch

from freetoken.utils import arch


def _clear_arch_caches() -> None:
    arch.get_rocm_gfx_arch.cache_clear()


def _compat_link(cache_root: pathlib.Path, runtime: pathlib.Path) -> pathlib.Path:
    key = hashlib.sha1(str(runtime.resolve()).encode()).hexdigest()[:12]
    return cache_root / "freetoken" / "rocm-lib" / key / "libamdhip64.so"


def _setup_rocm_paths(rocm_home):
    """setup.py's _rocm_paths, loaded alone: importing setup.py would run the build."""
    source = pathlib.Path(__file__).resolve().parents[2] / "setup.py"
    tree = ast.parse(source.read_text())
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "_rocm_paths")
    namespace = {"Path": pathlib.Path, "os": os, "re": __import__("re"), "importlib": importlib, "ROCM_HOME": rocm_home}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), "exec"), namespace)
    return namespace["_rocm_paths"]


def test_rocm_arch_prefers_visible_device_over_multi_arch_build_env(monkeypatch):
    monkeypatch.setattr(arch, "is_rocm", lambda: True)
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "current_device", lambda: 0)
    monkeypatch.setattr(
        torch.cuda,
        "get_device_properties",
        lambda _device: SimpleNamespace(gcnArchName="gfx1201:sramecc-:xnack-"),
    )
    monkeypatch.setenv("FREETOKEN_ROCM_ARCH", "gfx1100;gfx1200")
    _clear_arch_caches()

    assert arch.get_rocm_gfx_arch() == "gfx1201"

    _clear_arch_caches()


def test_rocm_arch_falls_back_to_cross_compile_env(monkeypatch):
    monkeypatch.setattr(arch, "is_rocm", lambda: True)
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    monkeypatch.setenv("FREETOKEN_ROCM_ARCH", "gfx1200;gfx1201")
    _clear_arch_caches()

    assert arch.get_rocm_gfx_arch() == "gfx1200"

    _clear_arch_caches()


def test_gfx1151_never_satisfies_nvidia_sm_gates(monkeypatch):
    # Strix Halo reports a CUDA-style capability of (11, 5), which would pass every SM gate.
    monkeypatch.setattr(torch.version, "hip", "7.1")
    monkeypatch.setattr(torch.version, "cuda", None)
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "current_device", lambda: 0)
    monkeypatch.setattr(torch.cuda, "get_device_capability", lambda *_args: (11, 5))
    monkeypatch.setattr(
        torch.cuda,
        "get_device_properties",
        lambda _device: SimpleNamespace(gcnArchName="gfx1151"),
    )
    arch.is_rocm.cache_clear()
    arch._get_torch_cuda_version.cache_clear()
    _clear_arch_caches()

    try:
        assert arch.is_rocm() is True
        assert arch.get_rocm_gfx_arch() == "gfx1151"
        assert arch._get_torch_cuda_version() is None
        assert arch.is_sm90_supported() is False
        assert arch.is_sm100_supported() is False
        assert arch.is_sm90_family() is False
        assert arch.is_sm100_family() is False
    finally:
        arch.is_rocm.cache_clear()
        arch._get_torch_cuda_version.cache_clear()
        _clear_arch_caches()


def test_hip_cflags_target_only_resolved_arch(monkeypatch):
    from freetoken.kernel import utils

    monkeypatch.setenv("FREETOKEN_ROCM_ARCH", "gfx1200;gfx1201")
    monkeypatch.setattr(arch, "get_rocm_gfx_arch", lambda: "gfx1201")

    arch_list = utils._rocm_arch_list()
    flags = utils._hip_cflags(["-Wno-unused-command-line-argument"], arch_list)

    assert arch_list == ["gfx1201"]
    assert "--offload-arch=gfx1201" in flags
    assert "--offload-arch=gfx1200" not in flags


def test_rocm_loaders_pin_tvm_ffi_to_resolved_arch(monkeypatch):
    from freetoken.kernel import utils

    builds = []

    def record_build(*_args, **kwargs):
        builds.append(
            (
                os.environ[utils.ROCM_ARCH_LIST_ENV],
                kwargs["extra_cuda_cflags"],
            )
        )
        return object()

    tvm_ffi = types.ModuleType("tvm_ffi")
    tvm_ffi.__path__ = []
    tvm_ffi_cpp = types.ModuleType("tvm_ffi.cpp")
    tvm_ffi_cpp.load = record_build
    tvm_ffi_cpp.load_inline = record_build
    monkeypatch.setitem(sys.modules, "tvm_ffi", tvm_ffi)
    monkeypatch.setitem(sys.modules, "tvm_ffi.cpp", tvm_ffi_cpp)
    monkeypatch.setenv(utils.DISABLE_KERNEL_CACHE_ENV, "1")
    monkeypatch.setenv(utils.ROCM_ARCH_LIST_ENV, "gfx1100 gfx1200")
    monkeypatch.setattr(utils, "_is_rocm", lambda: True)
    monkeypatch.setattr(utils, "_rocm_arch_list", lambda: ["gfx1201"])
    monkeypatch.setattr(utils, "_rocm_link_flags", lambda: [])

    utils.load_aot("test_rocm_aot_arch", cuda_files=["unused.cu"])
    utils.load_jit("test_rocm_jit_arch", cuda_files=["unused.cu"])

    assert builds == [
        ("gfx1201", [*utils.DEFAULT_HIP_CFLAGS, "--offload-arch=gfx1201"]),
        ("gfx1201", [*utils.DEFAULT_HIP_CFLAGS, "--offload-arch=gfx1201"]),
    ]
    assert os.environ[utils.ROCM_ARCH_LIST_ENV] == "gfx1100 gfx1200"


def test_rocm_link_flags_support_versioned_modular_sdk(monkeypatch, tmp_path):
    import torch.utils.cpp_extension as cpp_extension

    from freetoken.kernel import utils

    sdk = tmp_path / "sdk"
    library_dir = sdk / "lib"
    library_dir.mkdir(parents=True)
    versioned_runtime = library_dir / "libamdhip64.so.7"
    versioned_runtime.write_bytes(b"")
    real_find_spec = importlib.util.find_spec

    def find_spec(name: str):
        if name == "_rocm_sdk_core":
            return SimpleNamespace(submodule_search_locations=[str(sdk)])
        return real_find_spec(name)

    monkeypatch.delenv("ROCM_HOME", raising=False)
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.setattr(cpp_extension, "ROCM_HOME", None)
    monkeypatch.setattr(importlib.util, "find_spec", find_spec)
    monkeypatch.setattr(pathlib.Path, "home", lambda: tmp_path)
    utils._rocm_link_flags.cache_clear()

    # A link left behind by an earlier ROCm install must be replaced, not reused.
    stale_runtime = tmp_path / "retired-rocm" / "lib" / "libamdhip64.so.6"
    stale_runtime.parent.mkdir(parents=True)
    stale_runtime.write_bytes(b"")
    compat_link = _compat_link(tmp_path / ".cache", versioned_runtime)
    compat_dir = compat_link.parent
    compat_dir.mkdir(parents=True)
    compat_link.symlink_to(stale_runtime)

    flags = utils._rocm_link_flags()

    assert f"-L{compat_dir}" in flags
    assert f"-Wl,-rpath,{library_dir}" in flags
    assert compat_link.resolve() == versioned_runtime.resolve()

    utils._rocm_link_flags.cache_clear()


def test_rocm_link_flags_replace_broken_compat_link(monkeypatch, tmp_path):
    import torch.utils.cpp_extension as cpp_extension

    from freetoken.kernel import utils

    library_dir = tmp_path / "sdk" / "lib"
    library_dir.mkdir(parents=True)
    runtime = library_dir / "libamdhip64.so.7"
    runtime.write_bytes(b"")
    xdg_cache = tmp_path / "xdg-cache"
    compat_link = _compat_link(xdg_cache, runtime)
    compat_link.parent.mkdir(parents=True)
    compat_link.symlink_to(tmp_path / "removed-rocm" / "libamdhip64.so.6")
    monkeypatch.setenv("ROCM_HOME", str(tmp_path / "sdk"))
    monkeypatch.setenv("XDG_CACHE_HOME", str(xdg_cache))
    monkeypatch.setattr(cpp_extension, "ROCM_HOME", None)
    utils._rocm_link_flags.cache_clear()

    try:
        utils._rocm_link_flags()
        assert compat_link.resolve(strict=True) == runtime.resolve()
        assert sorted(p.name for p in compat_link.parent.iterdir()) == ["libamdhip64.so"]
    finally:
        utils._rocm_link_flags.cache_clear()


def test_rocm_link_flags_support_lib64_and_numeric_sonames(monkeypatch, tmp_path):
    import torch.utils.cpp_extension as cpp_extension

    from freetoken.kernel import utils

    sdk = tmp_path / "sdk"
    library_dir = sdk / "lib64"
    library_dir.mkdir(parents=True)
    # "9" sorts after "10" lexically; the numerically newer runtime must win.
    older_runtime = library_dir / "libamdhip64.so.9"
    newer_runtime = library_dir / "libamdhip64.so.10"
    older_runtime.write_bytes(b"")
    newer_runtime.write_bytes(b"")
    xdg_cache = tmp_path / "xdg-cache"
    monkeypatch.setenv("ROCM_HOME", str(sdk))
    monkeypatch.setenv("XDG_CACHE_HOME", str(xdg_cache))
    monkeypatch.setattr(cpp_extension, "ROCM_HOME", None)
    utils._rocm_link_flags.cache_clear()

    try:
        flags = utils._rocm_link_flags()
        compat_link = _compat_link(xdg_cache, newer_runtime)
        assert f"-L{compat_link.parent}" in flags
        assert f"-Wl,-rpath,{library_dir}" in flags
        assert compat_link.resolve() == newer_runtime.resolve()
    finally:
        utils._rocm_link_flags.cache_clear()


def test_rocm_cpp_only_loaders_skip_runtime_link_discovery(monkeypatch):
    from freetoken.kernel import utils

    recorded = []

    def record_build(*_args, **kwargs):
        recorded.append(kwargs)
        return object()

    def reject_runtime_lookup():
        raise AssertionError("C++-only builds must not look up libamdhip64")

    tvm_ffi = types.ModuleType("tvm_ffi")
    tvm_ffi.__path__ = []
    tvm_ffi_cpp = types.ModuleType("tvm_ffi.cpp")
    tvm_ffi_cpp.load = record_build
    tvm_ffi_cpp.load_inline = record_build
    monkeypatch.setitem(sys.modules, "tvm_ffi", tvm_ffi)
    monkeypatch.setitem(sys.modules, "tvm_ffi.cpp", tvm_ffi_cpp)
    monkeypatch.setenv(utils.DISABLE_KERNEL_CACHE_ENV, "1")
    monkeypatch.setattr(utils, "_is_rocm", lambda: True)
    monkeypatch.setattr(utils, "_rocm_link_flags", reject_runtime_lookup)

    utils.load_aot("test_cpp_only_aot", cpp_files=["unused.cpp"])
    utils.load_jit("test_cpp_only_jit", cpp_files=["unused.cpp"])

    assert [call["extra_ldflags"] for call in recorded] == [utils.DEFAULT_LDFLAGS, utils.DEFAULT_LDFLAGS]


def _versioned_sdk(monkeypatch, tmp_path, names, subdir="lib"):
    import torch.utils.cpp_extension as cpp_extension

    sdk = tmp_path / "sdk"
    library_dir = sdk / subdir
    library_dir.mkdir(parents=True)
    for name in names:
        (library_dir / name).write_bytes(b"")
    monkeypatch.setenv("ROCM_HOME", str(sdk))
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg-cache"))
    monkeypatch.setattr(cpp_extension, "ROCM_HOME", None)
    return sdk, library_dir


def test_rocm_link_flags_skip_non_soname_files(monkeypatch, tmp_path):
    from freetoken.kernel import utils

    _, library_dir = _versioned_sdk(monkeypatch, tmp_path, ["libamdhip64.so.7", "libamdhip64.so.7.debug", "libamdhip64.so.9.bak"])
    utils._rocm_link_flags.cache_clear()
    try:
        utils._rocm_link_flags()
        compat_link = _compat_link(tmp_path / "xdg-cache", library_dir / "libamdhip64.so.7")
        assert compat_link.resolve(strict=True) == (library_dir / "libamdhip64.so.7").resolve()
    finally:
        utils._rocm_link_flags.cache_clear()


def test_rocm_link_flags_refuse_to_replace_regular_file(monkeypatch, tmp_path):
    import pytest

    from freetoken.kernel import utils

    _, library_dir = _versioned_sdk(monkeypatch, tmp_path, ["libamdhip64.so.7"])
    compat_link = _compat_link(tmp_path / "xdg-cache", library_dir / "libamdhip64.so.7")
    compat_link.parent.mkdir(parents=True)
    compat_link.write_bytes(b"not a link")
    utils._rocm_link_flags.cache_clear()
    try:
        with pytest.raises(RuntimeError, match="Refusing to replace non-symlink"):
            utils._rocm_link_flags()
        assert compat_link.read_bytes() == b"not a link"
    finally:
        utils._rocm_link_flags.cache_clear()


def test_rocm_link_flags_replace_symlink_loop(monkeypatch, tmp_path):
    from freetoken.kernel import utils

    _, library_dir = _versioned_sdk(monkeypatch, tmp_path, ["libamdhip64.so.7"])
    compat_link = _compat_link(tmp_path / "xdg-cache", library_dir / "libamdhip64.so.7")
    compat_link.parent.mkdir(parents=True)
    compat_link.symlink_to(compat_link)
    utils._rocm_link_flags.cache_clear()
    try:
        utils._rocm_link_flags()
        assert compat_link.resolve(strict=True) == (library_dir / "libamdhip64.so.7").resolve()
    finally:
        utils._rocm_link_flags.cache_clear()


def test_rocm_link_flags_key_link_dir_by_runtime_and_ignore_relative_xdg(monkeypatch, tmp_path):
    from freetoken.kernel import utils

    first = tmp_path / "a" / "libamdhip64.so.7"
    second = tmp_path / "b" / "libamdhip64.so.7"
    for runtime in (first, second):
        runtime.parent.mkdir(parents=True)
        runtime.write_bytes(b"")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("XDG_CACHE_HOME", "relative-cache")
    monkeypatch.setattr(pathlib.Path, "home", lambda: tmp_path / "home")

    first_dir = utils._rocm_compat_link_dir(first.resolve())
    second_dir = utils._rocm_compat_link_dir(second.resolve())

    assert first_dir != second_dir
    assert first_dir.parent == tmp_path / "home" / ".cache" / "freetoken" / "rocm-lib"
    assert not (tmp_path / "relative-cache").exists()
    assert (first_dir / "libamdhip64.so").resolve(strict=True) == first.resolve()
    assert (second_dir / "libamdhip64.so").resolve(strict=True) == second.resolve()
    # A second call (another rank, same install) reuses the link.
    assert utils._rocm_compat_link_dir(first.resolve()) == first_dir
    assert sorted(p.name for p in first_dir.iterdir()) == ["libamdhip64.so"]


def test_rocm_loaders_link_hip_runtime_for_device_sources(monkeypatch):
    from freetoken.kernel import utils

    recorded = []

    def record_build(*_args, **kwargs):
        recorded.append(kwargs["extra_ldflags"])
        return object()

    tvm_ffi = types.ModuleType("tvm_ffi")
    tvm_ffi.__path__ = []
    tvm_ffi_cpp = types.ModuleType("tvm_ffi.cpp")
    tvm_ffi_cpp.load = record_build
    tvm_ffi_cpp.load_inline = record_build
    monkeypatch.setitem(sys.modules, "tvm_ffi", tvm_ffi)
    monkeypatch.setitem(sys.modules, "tvm_ffi.cpp", tvm_ffi_cpp)
    monkeypatch.setenv(utils.DISABLE_KERNEL_CACHE_ENV, "1")
    monkeypatch.setattr(utils, "_is_rocm", lambda: True)
    monkeypatch.setattr(utils, "_rocm_arch_list", lambda: ["gfx1151"])
    link_flags = ["-L/cache/rocm-lib/0123456789ab", "-Wl,-rpath,/sdk/lib"]
    monkeypatch.setattr(utils, "_rocm_link_flags", lambda: link_flags)

    utils.load_aot("test_rocm_aot_link", cuda_files=["unused.cu"])
    utils.load_jit("test_rocm_jit_link", cuda_files=["unused.cu"])

    assert recorded == [utils.DEFAULT_LDFLAGS + link_flags] * 2


def test_setup_rocm_paths_support_lib64_and_numeric_sonames(monkeypatch, tmp_path):
    sdk, library_dir = _versioned_sdk(
        monkeypatch, tmp_path, ["libamdhip64.so.9", "libamdhip64.so.10", "libamdhip64.so.11.debug"], subdir="lib64"
    )
    (sdk / "include" / "hip").mkdir(parents=True)
    (sdk / "include" / "hip" / "hip_runtime.h").write_text("")
    real_find_spec = importlib.util.find_spec
    monkeypatch.setattr(importlib.util, "find_spec", lambda name: None if name == "_rocm_sdk_core" else real_find_spec(name))

    include_dirs, library_dirs, runtime_lib = _setup_rocm_paths(None)()

    assert include_dirs == [str(sdk / "include")]
    assert library_dirs == [str(library_dir)]
    assert runtime_lib == ":libamdhip64.so.10"
