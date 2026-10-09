"""Pipeline parallelism (--pp-size): each process owns a contiguous run of decoder layers.

Stage ``r`` builds only layers ``[start_r, end_r)`` (plus the embedding on the first stage and
the final norm / LM head on the last), keeps the KV, GDN state and expert banks of those layers
only, and hands its residual stream to stage ``r + 1`` over NCCL. Every stage runs the same
scheduler (like TP ranks do), the last one samples and broadcasts the tokens on the CPU group.
"""

from __future__ import annotations

import dataclasses
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, List, Sequence, Tuple

import torch

from freetoken.layers.base import StateLessOP

if TYPE_CHECKING:
    from freetoken.models.config import ModelConfig


@dataclass(frozen=True)
class PipelineStage:
    """Stage ``rank`` of ``size``: decoder layers ``[start, end)`` of the model's ``num_layers``."""

    rank: int
    size: int
    start: int
    end: int
    num_layers: int

    @property
    def is_first(self) -> bool:
        return self.rank == 0

    @property
    def is_last(self) -> bool:
        return self.rank == self.size - 1

    def owns_layer(self, layer_id: int) -> bool:
        return self.start <= layer_id < self.end


_STAGE: PipelineStage | None = None


def set_pipeline_stage(stage: PipelineStage | None) -> None:
    global _STAGE
    _STAGE = stage


def get_pipeline_stage() -> PipelineStage | None:
    """This process's stage; None without pipeline parallelism."""
    return _STAGE


def split_layers(num_layers: int, stages: int, spec: str | Sequence[int] | None = None) -> List[Tuple[int, int]]:
    """``[start, end)`` per stage. ``spec`` lists the layer count of each stage ("16,16,16");
    without it the layers split evenly and the earlier stages take the remainder (the last
    stage also carries the LM head)."""
    if stages < 1:
        raise ValueError(f"pipeline size must be >= 1, got {stages}")
    if spec is None or spec == "":
        if num_layers < stages:
            raise ValueError(f"{num_layers} decoder layers cannot fill {stages} pipeline stages")
        base, extra = divmod(num_layers, stages)
        counts = [base + (1 if i < extra else 0) for i in range(stages)]
    else:
        items = spec.split(",") if isinstance(spec, str) else list(spec)
        try:
            counts = [int(x) for x in items]
        except ValueError:
            raise ValueError(f"--pp-layer-split must be comma-separated layer counts, got {spec!r}") from None
        if len(counts) != stages:
            raise ValueError(f"--pp-layer-split names {len(counts)} stages, --pp-size is {stages}")
        if any(c < 1 for c in counts):
            raise ValueError(f"every pipeline stage needs at least one layer, got {counts}")
        if sum(counts) != num_layers:
            raise ValueError(f"--pp-layer-split covers {sum(counts)} layers, the model has {num_layers}")
    ranges, start = [], 0
    for count in counts:
        ranges.append((start, start + count))
        start += count
    return ranges


def stage_model_config(model_config: ModelConfig, layers: Tuple[int, int]) -> ModelConfig:
    """``model_config`` narrowed to one stage: its attention groups keep only the stage's layer
    ids, so the KV and GDN state pools (and their cost models) size for those layers alone."""
    start, end = layers
    if not 0 <= start < end <= model_config.num_layers:
        raise ValueError(f"pipeline stage layers {layers} outside [0, {model_config.num_layers})")
    groups = []
    for group in model_config.attention_groups:
        ids = tuple(i for i in group.layer_ids if start <= i < end)
        if not ids:
            raise ValueError(
                f"pipeline stage [{start}, {end}) holds no {group.name} attention layer; every stage "
                "needs at least one layer of each attention kind (pick another --pp-layer-split)"
            )
        changes = {"layer_ids": ids}
        if getattr(group, "num_index_layers", 0) == len(group.layer_ids):
            changes["num_index_layers"] = len(ids)  # one index slab per attention layer (QSA)
        elif getattr(group, "num_index_layers", 0):
            raise ValueError(f"pipeline stages do not support the shared indexers of the {group.name} group")
        groups.append(dataclasses.replace(group, **changes))
    return dataclasses.replace(model_config, attention_groups=tuple(groups), pp_layers=(start, end))


_LAYER_KEY = re.compile(r"^(?:model\.)?(?:language_model\.)?layers\.(\d+)\.")


def keeps_weight(
    name: str,
    *,
    head: Iterable[str] = ("model.embed_tokens.",),
    tail: Iterable[str] = ("lm_head.", "model.norm."),
) -> bool:
    """Whether this process loads the checkpoint tensor ``name`` (named as the model's state
    dict): its stage's own layers, the ``head`` tensors on the first stage, the ``tail`` tensors
    on the last. Always True without pipeline parallelism."""
    stage = _STAGE
    if stage is None:
        return True
    m = _LAYER_KEY.match(name)
    if m is not None:
        return stage.owns_layer(int(m.group(1)))
    if name.startswith(tuple(head)):
        return stage.is_first
    if name.startswith(tuple(tail)):
        return stage.is_last
    return True


class PipelineMissingLayer(StateLessOP):
    """Stands in for a decoder layer another stage owns, so layer ids keep their list index."""

    def __init__(self, layer_id: int):
        super().__init__()
        self._layer_id = layer_id

    def forward(self, *args, **kwargs):
        raise RuntimeError(f"decoder layer {self._layer_id} belongs to another pipeline stage")


def stage_input(batch, rows: int, width: int, dtype: torch.dtype, device: torch.device) -> torch.Tensor:
    """The residual stream a non-first stage starts from: what the previous stage sent, or zeros
    when nothing was received (the engine's warmup and graph-capture forwards)."""
    hidden = getattr(batch, "pp_hidden", None)
    if hidden is not None:
        return hidden[:rows]
    return torch.zeros(rows, width, dtype=dtype, device=device)


class PipelineComm:
    """Point-to-point hand-off of the residual stream between neighbouring stages.

    The NCCL ops run on the process group's own streams: a send starts once the engine stream
    has produced its tensor and never blocks the engine stream, a receive makes the engine stream
    wait for its data. A sent tensor stays referenced until ``release`` says the receiver is done
    with it (the scheduler calls it once the batch's tokens came back)."""

    def __init__(self, pp_rank: int, pp_size: int, world_ranks: Sequence[int]):
        import torch.distributed as dist

        self.pp_rank = pp_rank
        self.pp_size = pp_size
        self._ranks = list(world_ranks)
        # every rank creates the group (new_group is collective); the p2p ops then use per-pair communicators
        self._group = dist.new_group(ranks=self._ranks, backend="nccl")
        self._pending: dict[int, list] = {}

    @property
    def is_first(self) -> bool:
        return self.pp_rank == 0

    @property
    def is_last(self) -> bool:
        return self.pp_rank == self.pp_size - 1

    def send(self, tag: int, hidden: torch.Tensor) -> None:
        import torch.distributed as dist

        assert not self.is_last
        work = dist.isend(hidden, dst=self._ranks[self.pp_rank + 1], group=self._group)
        self._pending.setdefault(tag, []).append((work, hidden))

    def recv(self, rows: int, width: int, dtype: torch.dtype, device: torch.device) -> torch.Tensor:
        import torch.distributed as dist

        assert not self.is_first
        buf = torch.empty(rows, width, dtype=dtype, device=device)
        work = dist.irecv(buf, src=self._ranks[self.pp_rank - 1], group=self._group)
        work.wait()  # the current stream waits for the data; the CPU does not
        return buf

    def release(self, tag: int) -> None:
        for work, _ in self._pending.pop(tag, ()):
            work.wait()

    def release_all(self) -> None:
        for tag in list(self._pending):
            self.release(tag)
