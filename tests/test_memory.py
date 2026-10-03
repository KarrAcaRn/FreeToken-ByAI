"""available_host_memory against fake /proc and cgroup trees: the host figure, clamped to the
tightest cgroup limit along the ancestry, with reclaimable page cache counted as free."""

from __future__ import annotations

from pathlib import Path

import pytest

from freetoken.memory import available_host_memory

GiB = 1 << 30


def _meminfo(tmp_path: Path, available: int | None) -> Path:
    path = tmp_path / "meminfo"
    lines = ["MemTotal:       65536000 kB"]
    if available is not None:
        lines.append(f"MemAvailable:   {available // 1024} kB")
    path.write_text("\n".join(lines) + "\n")
    return path


def _group(directory: Path, limit: str, usage: int, inactive: int = 0, v1: bool = False) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    names = ("memory.limit_in_bytes", "memory.usage_in_bytes", "total_inactive_file") if v1 else (
        "memory.max", "memory.current", "inactive_file"
    )
    (directory / names[0]).write_text(f"{limit}\n")
    (directory / names[1]).write_text(f"{usage}\n")
    (directory / "memory.stat").write_text(f"anon 1\n{names[2]} {inactive}\nfile 2\n")


def _call(tmp_path: Path, host: int | None, membership: str):
    proc = tmp_path / "cgroup"
    proc.write_text(membership)
    return available_host_memory(_meminfo(tmp_path, host), tmp_path / "fs", proc)


def test_bare_metal_reads_mem_available(tmp_path):
    _group(tmp_path / "fs" / "user.slice", "max", 3 * GiB)
    assert _call(tmp_path, 40 * GiB, "0::/user.slice\n") == 40 * GiB


def test_container_limit_clamps_the_host_figure(tmp_path):
    _group(tmp_path / "fs" / "docker" / "abc", str(16 * GiB), 10 * GiB)
    assert _call(tmp_path, 40 * GiB, "0::/docker/abc\n") == 6 * GiB


def test_page_cache_counts_as_free(tmp_path):
    # a container that just read its checkpoint: usage at the limit, most of it reclaimable cache
    _group(tmp_path / "fs" / "docker" / "abc", str(16 * GiB), 16 * GiB, inactive=12 * GiB)
    assert _call(tmp_path, 40 * GiB, "0::/docker/abc\n") == 12 * GiB


def test_the_tightest_ancestor_wins(tmp_path):
    _group(tmp_path / "fs" / "kubepods", str(8 * GiB), 7 * GiB)
    _group(tmp_path / "fs" / "kubepods" / "pod1", "max", 1 * GiB)
    assert _call(tmp_path, 40 * GiB, "0::/kubepods/pod1\n") == 1 * GiB


def test_namespaced_root_is_checked(tmp_path):
    # cgroupns: /proc names the host-side path, the mount shows the group itself as the root
    _group(tmp_path / "fs", str(4 * GiB), 1 * GiB)
    assert _call(tmp_path, 40 * GiB, "0::/docker/abc\n") == 3 * GiB


def test_cgroup_v1(tmp_path):
    _group(tmp_path / "fs" / "memory" / "docker" / "abc", str(8 * GiB), 6 * GiB, inactive=GiB, v1=True)
    membership = "12:cpuset:/docker/abc\n4:memory:/docker/abc\n"
    assert _call(tmp_path, 40 * GiB, membership) == 3 * GiB


def test_cgroup_v1_unlimited_sentinel(tmp_path):
    _group(tmp_path / "fs" / "memory" / "x", "9223372036854771712", GiB, v1=True)
    assert _call(tmp_path, 40 * GiB, "4:memory:/x\n") == 40 * GiB


@pytest.mark.parametrize("host,expected", [(None, 2 * GiB), (40 * GiB, 2 * GiB)])
def test_cgroup_alone_when_meminfo_is_missing(tmp_path, host, expected):
    _group(tmp_path / "fs" / "g", str(3 * GiB), GiB)
    assert _call(tmp_path, host, "0::/g\n") == expected


def test_unknown_everywhere_is_none(tmp_path):
    assert available_host_memory(tmp_path / "none", tmp_path / "fs", tmp_path / "none") is None
