"""Host RAM a process can still allocate: ``MemAvailable``, clamped to its cgroup's memory limit.

Inside a container ``/proc/meminfo`` describes the host, so a loader sized against it alone is
OOM-killed by the cgroup mid-load. The cgroup headroom counts reclaimable page cache as free, as
``MemAvailable`` does: reading a checkpoint fills the cache up to the limit, and charging it would
read a container that just loaded its weights as full.
"""

from __future__ import annotations

from pathlib import Path

# cgroup v1 spells "no limit" as a page-aligned value near 2**63
_V1_UNLIMITED = 1 << 60


def _read(path: Path) -> str | None:
    try:
        return path.read_text()
    except (OSError, UnicodeDecodeError):
        return None


def _stat_field(text: str | None, key: str) -> int:
    for line in (text or "").splitlines():
        name, _, value = line.partition(" ")
        if name == key and value.strip().isdigit():
            return int(value)
    return 0


def _headroom(directory: Path, v1: bool) -> int | None:
    """Limit minus non-reclaimable usage of one cgroup, or None when it sets no limit."""
    limit_file, usage_file, inactive = (
        ("memory.limit_in_bytes", "memory.usage_in_bytes", "total_inactive_file")
        if v1
        else ("memory.max", "memory.current", "inactive_file")
    )
    limit, usage = _read(directory / limit_file), _read(directory / usage_file)
    if limit is None or usage is None or not limit.strip().isdigit() or not usage.strip().isdigit():
        return None  # "max", or no memory controller at this level
    if v1 and int(limit) >= _V1_UNLIMITED:
        return None
    working_set = int(usage) - _stat_field(_read(directory / "memory.stat"), inactive)
    return max(0, int(limit) - max(0, working_set))


def _cgroup_headroom(cgroup_root: Path, proc_cgroup: Path) -> int | None:
    """The tightest headroom from this process's cgroup up to the hierarchy root (v2, else v1)."""
    v2_path = v1_path = None
    for line in (_read(proc_cgroup) or "").splitlines():
        hierarchy, _, rest = line.partition(":")
        controllers, _, path = rest.partition(":")
        if hierarchy == "0" and not controllers:
            v2_path = path
        elif "memory" in controllers.split(","):
            v1_path = path
    tightest = None
    for root, path, v1 in ((cgroup_root, v2_path, False), (cgroup_root / "memory", v1_path, True)):
        if path is None:
            continue
        # a cgroup namespace mounts the process's own group as the root while /proc may still
        # name the host-side path, so the root itself is always checked as well
        directory = root.joinpath(*Path(path).parts[1:])
        levels = [directory, *(p for p in directory.parents if root in (p, *p.parents))]
        for level in dict.fromkeys([*levels, root]):
            room = _headroom(level, v1)
            if room is not None:
                tightest = room if tightest is None else min(tightest, room)
        if tightest is not None:
            return tightest
    return None


def available_host_memory(
    meminfo: Path = Path("/proc/meminfo"),
    cgroup_root: Path = Path("/sys/fs/cgroup"),
    proc_cgroup: Path = Path("/proc/self/cgroup"),
) -> int | None:
    """Bytes of host RAM this process can still take, or None when neither source is readable."""
    host = None
    for line in (_read(meminfo) or "").splitlines():
        if line.startswith("MemAvailable:"):
            host = int(line.split()[1]) * 1024
            break
    cgroup = _cgroup_headroom(cgroup_root, proc_cgroup)
    if host is None or cgroup is None:
        return cgroup if host is None else host
    return min(host, cgroup)


__all__ = ["available_host_memory"]
