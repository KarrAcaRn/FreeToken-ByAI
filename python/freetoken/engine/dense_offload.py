"""--dense-offload-layers: decoder layers whose weights live in pinned host RAM.

Each offloaded layer's tensors are packed into one pinned host row. Two device staging buffers
take turns: the k-th offloaded layer always computes from buffer ``k % 2``, and its tensor
attributes are bound to views of that buffer once, at setup. Every forward then streams the
rows in on a copy stream (offloaded layer k + 2 starts copying as soon as layer k is done with
the shared buffer) and joins the copy stream back before it returns. The pointers never change,
so the same code runs eagerly and inside CUDA graphs.

What it costs: an offloaded layer crosses PCIe once per forward. Decode at batch 1 cannot hide
that (a 27B layer is ~0.3 GB, ~12 ms at 24 GB/s, against ~0.35 ms to compute it from VRAM); a
long prefill chunk mostly can, because the copy runs while the resident layers in between
compute. What it buys: the freed VRAM goes to the KV pool.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, List, Sequence

import torch

from freetoken.layers import BaseOP
from freetoken.layers.base import OPList
from freetoken.utils import init_logger

logger = init_logger(__name__)

_ALIGN = 256
# Smaller tensors stay resident: norm weights and GDN gates (A_log, dt_bias) are a rounding error
# of a layer's bytes, and some of them are read outside the layer's forward -- the DFlash commit
# replays GDN recurrences with A_log/dt_bias after the verify, when the staging buffer may already
# hold another layer. Anything that big code reads outside forward() would need the same care.
_MIN_TENSOR_BYTES = 1 << 20


@dataclass(frozen=True)
class _Slot:
    owner: Any
    attr: str
    offset: int
    nbytes: int
    dtype: torch.dtype
    shape: torch.Size

    def view(self, row: torch.Tensor) -> torch.Tensor:
        return row[self.offset : self.offset + self.nbytes].view(self.dtype).view(self.shape)


def _owned_ops(layer: BaseOP) -> List[BaseOP]:
    """Every op reachable from ``layer`` through attributes and lists (OPList children included)."""
    seen: dict[int, BaseOP] = {}
    stack: List[Any] = [layer]
    while stack:
        obj = stack.pop()
        if isinstance(obj, BaseOP):
            if id(obj) in seen:
                continue
            seen[id(obj)] = obj
            for name, value in obj.__dict__.items():
                if not name.startswith("_") or isinstance(value, (BaseOP, list, tuple)):
                    stack.append(value)
        elif isinstance(obj, (list, tuple)):
            stack.extend(v for v in obj if isinstance(v, (BaseOP, list, tuple)))
    return list(seen.values())


def _device(device: torch.device | str) -> torch.device:
    """``cuda`` -> ``cuda:<current>``: tensors carry an index, and ``cuda`` never equals ``cuda:0``."""
    device = torch.device(device)
    if device.type == "cuda" and device.index is None:
        device = torch.device("cuda", torch.cuda.current_device())
    return device


def _layout(layer: BaseOP, shared_ops: set[int], device: torch.device) -> tuple[List[_Slot], int]:
    """The layer's own device tensors (public attributes, as ``state_dict`` sees them) back to back
    with 256-byte alignment. Ops reachable from another layer too (a shared rotary cache) stay
    resident: rebinding them would move the other layer's tensors along."""
    slots: List[_Slot] = []
    offset = 0
    for op in _owned_ops(layer):
        if id(op) in shared_ops:
            continue
        for name, value in op.__dict__.items():
            if name.startswith("_") or not isinstance(value, torch.Tensor) or value.device != device:
                continue
            if not value.is_contiguous():
                continue  # a strided view of another tensor: moving it would not free anything
            nbytes = value.numel() * value.element_size()
            if nbytes < _MIN_TENSOR_BYTES:
                continue
            slots.append(_Slot(op, name, offset, nbytes, value.dtype, value.shape))
            offset += -(-nbytes // _ALIGN) * _ALIGN
    return slots, offset


def decoder_layers(model: Any) -> List[BaseOP]:
    """The model's decoder stack (``model.model.layers``), the one dense offload works on."""
    inner = getattr(model, "model", None)
    layers = getattr(inner, "layers", None)
    if not isinstance(layers, OPList) or not layers.op_list:
        raise ValueError(
            f"--dense-offload-layers: {type(model).__name__} has no model.layers decoder stack"
        )
    return list(layers.op_list)


def pick_layers(num_layers: int, count: int) -> List[int]:
    """``count`` layer indices spread evenly over the stack, never layer 0: the copy of each
    offloaded layer overlaps the resident layers before it."""
    count = max(0, min(count, num_layers - 1))
    return sorted({min(num_layers - 1, int((k + 1) * num_layers / (count + 1))) for k in range(count)})


class DenseLayerOffloader:
    """Owns the host rows, the two staging buffers and the copy stream of the offloaded layers."""

    def __init__(self, layers: Sequence[BaseOP], offload_ids: Sequence[int], device: torch.device):
        self.device = device = _device(device)
        self.offload_ids = list(offload_ids)
        self.layers = list(layers)
        owners: dict[int, int] = {}
        for layer in layers:
            for op in _owned_ops(layer):
                owners[id(op)] = owners.get(id(op), 0) + 1
        shared = {k for k, n in owners.items() if n > 1}
        self._layouts = [_layout(self.layers[i], shared, device) for i in self.offload_ids]
        self.row_bytes = max(nbytes for _, nbytes in self._layouts)
        self.host_bytes = sum(nbytes for _, nbytes in self._layouts)
        self.banks = [torch.empty(nbytes, dtype=torch.uint8, pin_memory=True) for _, nbytes in self._layouts]
        for (slots, _), bank in zip(self._layouts, self.banks):
            for s in slots:
                s.view(bank).copy_(getattr(s.owner, s.attr))
        torch.cuda.synchronize(device)
        for k, (slots, _) in enumerate(self._layouts):
            for s in slots:
                setattr(s.owner, s.attr, s.view(self.banks[k]))  # drops the device copy
        self._compact_resident(shared)
        self.staging = torch.empty((2, self.row_bytes), dtype=torch.uint8, device=device)
        for k, (slots, _) in enumerate(self._layouts):
            for s in slots:
                setattr(s.owner, s.attr, s.view(self.staging[k % 2]))
        # every forward copies its rows itself (_begin), so the staging buffers start uninitialized
        self.copy_stream = torch.cuda.Stream(device=device)
        self._begin_event = torch.cuda.Event()
        self._ready = [torch.cuda.Event() for _ in self.offload_ids]
        self._release = [torch.cuda.Event(), torch.cuda.Event()]
        self._wrap_forwards()

    def _compact_resident(self, shared: set[int]) -> None:
        """Re-upload the resident layers back to back. The offloaded tensors sat between them, so
        freeing those in place leaves holes the allocator keeps reserved (on a 27B, 0.6 of 1.5
        GiB); a round trip through host memory hands the freed VRAM back as one block."""
        offloaded = set(self.offload_ids)
        resident = [_layout(layer, shared, self.device)[0] for i, layer in enumerate(self.layers) if i not in offloaded]
        for slots in resident:
            for s in slots:
                setattr(s.owner, s.attr, getattr(s.owner, s.attr).to("cpu"))
        torch.cuda.empty_cache()
        for slots in resident:
            for s in slots:
                setattr(s.owner, s.attr, getattr(s.owner, s.attr).to(self.device))
        torch.cuda.synchronize(self.device)

    @property
    def device_bytes(self) -> int:
        return self.staging.numel()

    def _copy(self, k: int, wait_release: bool) -> None:
        if k >= len(self.offload_ids):
            return
        nbytes = self._layouts[k][1]
        with torch.cuda.stream(self.copy_stream):
            if wait_release:
                self.copy_stream.wait_event(self._release[k % 2])
            self.staging[k % 2, :nbytes].copy_(self.banks[k], non_blocking=True)
            self._ready[k].record(self.copy_stream)

    def _begin(self) -> None:
        compute = torch.cuda.current_stream(self.device)
        # the previous forward's offloaded layers ran on this stream: copying after this point
        # cannot overwrite a buffer they still read
        self._begin_event.record(compute)
        self.copy_stream.wait_event(self._begin_event)
        self._copy(0, wait_release=False)
        self._copy(1, wait_release=False)

    def _end(self) -> None:
        # join the copy stream (graph capture needs every forked stream rejoined)
        torch.cuda.current_stream(self.device).wait_stream(self.copy_stream)

    def _wrap_forwards(self) -> None:
        position = {layer_id: k for k, layer_id in enumerate(self.offload_ids)}
        last = len(self.layers) - 1

        def wrap(i: int, layer: BaseOP, inner: Callable[..., Any]) -> Callable[..., Any]:
            k = position.get(i)

            def forward(*args: Any, **kwargs: Any) -> Any:
                if i == 0:
                    self._begin()
                if k is not None:
                    compute = torch.cuda.current_stream(self.device)
                    compute.wait_event(self._ready[k])
                out = inner(*args, **kwargs)
                if k is not None:
                    self._release[k % 2].record(torch.cuda.current_stream(self.device))
                    self._copy(k + 2, wait_release=True)
                if i == last:
                    self._end()
                return out

            return forward

        for i, layer in enumerate(self.layers):
            if i == 0 or i == last or i in position:
                # an instance attribute shadows the class method; state_dict skips callables
                layer.forward = wrap(i, layer, layer.forward)


def layer_bytes(layers: Sequence[BaseOP], device: torch.device) -> List[int]:
    """Bytes each layer would move to the host (same rules as the offloader's layout)."""
    device = _device(device)
    owners: dict[int, int] = {}
    for layer in layers:
        for op in _owned_ops(layer):
            owners[id(op)] = owners.get(id(op), 0) + 1
    shared = {k for k, n in owners.items() if n > 1}
    return [_layout(layer, shared, device)[1] for layer in layers]


def auto_count(sizes: Sequence[int], fits: Callable[[int], bool]) -> int:
    """Fewest offloaded layers (spread by ``pick_layers``) for which ``fits(freed_bytes)``;
    ``freed_bytes`` already pays for the two staging buffers."""
    n = len(sizes)
    for count in range(0, n):
        ids = pick_layers(n, count)
        freed = sum(sizes[i] for i in ids) - (2 * max(sizes[i] for i in ids) if ids else 0)
        if fits(freed):
            return count
    raise ValueError(
        "--dense-offload-layers auto: even offloading every layer but the first does not reach "
        "--kv-reserve-tokens; lower it"
    )


def parse_count(value: str | int) -> int | None:
    """``N`` -> N, ``auto`` -> None (resolved against --kv-reserve-tokens at load)."""
    if isinstance(value, int):
        return value
    v = str(value).strip().lower()
    if v == "auto":
        return None
    if v.isdigit():
        return int(v)
    raise ValueError(f"--dense-offload-layers takes a layer count or 'auto', got {value!r}")


__all__ = [
    "DenseLayerOffloader", "auto_count", "decoder_layers", "layer_bytes", "parse_count", "pick_layers",
]
