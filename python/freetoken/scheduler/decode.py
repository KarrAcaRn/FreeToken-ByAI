from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Set

from freetoken.core import Batch, Req


@dataclass
class DecodeManager:
    page_size: int
    running_reqs: Set[Req] = field(default_factory=set)

    def filter_reqs(self, reqs: Iterable[Req]) -> None:
        self.running_reqs = {req for req in self.running_reqs.union(reqs) if req.can_decode}

    def remove_req(self, req: Req) -> None:
        self.running_reqs.discard(req)

    def abort_req(self, uid: int) -> Req | None:
        for req in self.running_reqs:
            if req.uid == uid:
                self.running_reqs.remove(req)
                return req
        return None

    @property
    def inflight_tokens(self) -> int:
        tokens_reserved = (self.page_size - 1) * len(self.running_reqs)  # 1 page reserved
        return sum(req.remain_len for req in self.running_reqs) + tokens_reserved

    def schedule_next_batch(self, exclude: Set[Req] = frozenset(), max_size: int | None = None) -> Batch | None:
        """All running requests, or (pipeline parallelism) at most ``max_size`` of those not in
        ``exclude``, oldest first."""
        reqs = sorted((req for req in self.running_reqs if req not in exclude), key=lambda req: req.uid)
        if max_size is not None:
            reqs = reqs[:max_size]
        if not reqs:
            return None
        return Batch(reqs=reqs, phase="decode")

    @property
    def runnable(self) -> bool:
        return len(self.running_reqs) > 0
