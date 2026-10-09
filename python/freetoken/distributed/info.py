from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DistributedInfo:  # should not export from here
    rank: int
    size: int
    # This process among all engine processes (tensor x pipeline parallel); -1 = this group is
    # the whole world. Sharding reads rank/size, process plumbing (spawn, rendezvous, rank-0 I/O
    # and logging) reads these.
    world_rank: int = -1
    world_size: int = -1

    def __post_init__(self):
        assert 0 <= self.rank < self.size
        if self.world_rank < 0:
            object.__setattr__(self, "world_rank", self.rank)
        if self.world_size < 0:
            object.__setattr__(self, "world_size", self.size)
        assert 0 <= self.world_rank < self.world_size

    def is_primary(self) -> bool:
        return self.world_rank == 0


_TP_INFO: DistributedInfo | None = None


def set_tp_info(rank: int, size: int, *, world_rank: int = -1, world_size: int = -1) -> None:
    global _TP_INFO
    if _TP_INFO is not None:
        raise RuntimeError("TP info has been set")
    _TP_INFO = DistributedInfo(rank, size, world_rank, world_size)


def get_tp_info() -> DistributedInfo:
    if _TP_INFO is None:
        raise RuntimeError("TP info has not been set")
    return _TP_INFO


def try_get_tp_info() -> DistributedInfo | None:
    return _TP_INFO


__all__ = ["DistributedInfo", "set_tp_info", "get_tp_info", "try_get_tp_info"]
