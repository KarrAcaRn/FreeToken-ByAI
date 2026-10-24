from __future__ import annotations

import collections
import itertools
import os
import re
from dataclasses import dataclass
from typing import Callable, Collection

import safetensors
import torch
from freetoken.distributed import get_tp_info
from freetoken.utils import download_hf_weight
from tqdm import tqdm

LayerToBank = Callable[[int, object], int | None]
DropPageCache = Callable[[str], None]


@dataclass(frozen=True)
class Nvfp4ExpertSourceSpec:
    key_pattern: re.Pattern[str]
    proj_to_role: dict[str, str]
    layer_to_bank: LayerToBank
    desc: str
    # Maps checkpoint tensor-kind names onto the canonical (modelopt) kinds, e.g.
    # compressed-tensors' weight_packed -> weight, weight_global_scale -> weight_scale_2.
    kind_map: dict[str, str] | None = None
    # The checkpoint stores the QUANT-side global scale (local fp8 scales were
    # multiplied by it before the cast); the banks keep its reciprocal.
    global_reciprocal: bool = False
    # The checkpoint stores the block scales as a lossless CSF slab pair instead of
    # the plain E4M3 matrix (e.g. "weight_scale.nvfp4_csf_fixed" /
    # "weight_scale.nvfp4_csf_exceptions"); scale_decoder expands the parts into the
    # plain matrix the banks consume.
    scale_pair: tuple[str, ...] | None = None
    scale_decoder: Callable[..., torch.Tensor] | None = None


def _canon_kind(spec: "Nvfp4ExpertSourceSpec", kind: str) -> str:
    return spec.kind_map.get(kind, kind) if spec.kind_map else kind


def _ingest_global(spec: "Nvfp4ExpertSourceSpec", tensor: torch.Tensor) -> torch.Tensor:
    if spec.global_reciprocal:
        tensor = 1.0 / tensor.float()
    return tensor.to(torch.float32)


def _activation_scale():
    """The checkpoint tensor of the NVFP4 static activation scale under the installed dialect, or None."""
    from freetoken.layers.quantization import QuantKind, get_quant_config

    try:
        quant = get_quant_config()
    except RuntimeError:
        return None
    if quant is None or QuantKind.NVFP4 not in quant.STORAGE:
        return None
    return quant.stored_tensors(QuantKind.NVFP4).get("input_scale")


def _ingest(spec: "Nvfp4ExpertSourceSpec", act, role: str, tensor: torch.Tensor) -> torch.Tensor:
    if role.endswith("_global"):
        return _ingest_global(spec, tensor)
    if role.endswith("_input"):
        tensor = tensor.float()
        return 1.0 / tensor if act.reciprocal else tensor
    return tensor


def _num_moe_layers(config) -> int:
    value = getattr(config, "num_moe_layers", None)
    if value is not None:
        return int(value)
    return int(config.num_layers) - int(getattr(config, "first_k_dense_replace", 0))


def _bank_layer(spec: Nvfp4ExpertSourceSpec, layer: int, config) -> int | None:
    bank_layer = spec.layer_to_bank(layer, config)
    if bank_layer is None:
        return None
    num_layers = _num_moe_layers(config)
    if bank_layer < 0 or bank_layer >= num_layers:
        raise ValueError(
            f"{spec.desc}: bank layer {bank_layer} for checkpoint layer {layer} "
            f"is outside [0, {num_layers})"
        )
    return bank_layer


def _kind_suffix(kind: str) -> str:
    return {"weight": "", "weight_scale": "_scale", "weight_scale_2": "_global"}[kind]


# gate/up and their block scales carry I on the row axis, down and its scales on the column axis; the
# per-expert global scale has no I axis and is shared by every rank.
_I_AXIS = {"gate": 0, "up": 0, "gate_scale": 0, "up_scale": 0, "down": 1, "down_scale": 1}


def shard_nvfp4_piece(role: str, t: torch.Tensor, *, rank: int, tp_size: int) -> torch.Tensor:
    """This rank's block of the intermediate dim in one NVFP4 expert tensor, in its own storage."""
    axis = _I_AXIS.get(role)
    if tp_size == 1 or axis is None:
        return t
    total = t.shape[axis]
    if total % tp_size:
        raise ValueError(f"NVFP4 expert piece {role!r} has {total} entries on axis {axis}, not divisible by TP={tp_size}")
    step = total // tp_size
    return t.narrow(axis, rank * step, step).clone(memory_format=torch.contiguous_format)


def decode_csf_scales(fixed: torch.Tensor, exceptions: torch.Tensor) -> torch.Tensor:
    """Expand the CSF slab encoding of an NVFP4 per-16 scale into the plain E4M3 matrix (CPU).

    ``fixed`` is U8 ``[slabs, 16 * (1 + row_bytes)]``: the first 16 bytes of each slab hold the
    per-row scale bases (one byte per row of the slab's 16 rows), the rest are row-major code
    bytes with column c at bit 4c. ``exceptions`` is U32 records, ``pos = rec & 0xFFFFFF``
    (row-major scale index, below 2**24) and ``value = rec >> 24`` (the exact E4M3 byte),
    applied after base + offset.
    """
    if fixed.ndim != 2 or fixed.dtype != torch.uint8:
        raise ValueError(f"CSF fixed slab tensor is {tuple(fixed.shape)} {fixed.dtype}, expected U8 [slabs, slab_bytes]")
    slabs, slab_bytes = fixed.shape
    row_bytes = slab_bytes // 16 - 1
    if row_bytes < 1 or slab_bytes != 16 * (1 + row_bytes):
        raise ValueError(f"CSF slab width {slab_bytes} does not hold 16 bases plus 16 * row_bytes code bytes")
    rows = slabs * 16
    cols = row_bytes * 2
    data = fixed.to(torch.int16)
    base = data[:, :16].reshape(rows, 1)
    codes = data[:, 16:].reshape(rows, row_bytes)
    bits = 4 * torch.arange(cols)
    scale = (base + ((codes[:, bits // 8] >> bits % 8) & 0x0F)) & 0xFF
    if exceptions.numel():
        # Records are U32 on disk or raw U8 bytes; the bit math runs in int64 because CPU torch
        # has no uint32 shifts and uint32 -> int32 casts wrap records with the sign bit set.
        rec = exceptions.reshape(-1)
        if rec.dtype == torch.uint8:
            rec = rec.view(torch.uint32)
        if rec.dtype not in (torch.uint32, torch.int32):
            raise ValueError(f"CSF exceptions are U32 records (or U8 bytes), got {rec.dtype}")
        rec = rec.to(torch.int64)
        scale = scale.to(torch.int32)
        flat = scale.view(-1)
        flat.scatter_(0, rec & 0xFFFFFF, ((rec >> 24) & 0xFF).to(torch.int32))
    return scale.to(torch.uint8).view(torch.float8_e4m3fn)


def iter_nvfp4_expert_pieces(
    model_path: str,
    config,
    spec: Nvfp4ExpertSourceSpec,
    *,
    layers: Collection[int] | None = None,
    parallel: bool = False,
    workers: int = 8,
    chunk: int = 8 << 20,
    drop_page_cache: DropPageCache | None = None,
    primary: bool = True,
    skip_experts_from: int | None = None,
    expert_order: list[list[int]] | None = None,
):
    """One piece per routed expert: ``gate`` / ``up`` / ``down`` codes plus their ``_scale``
    (fp8 block scales) and ``_global`` (the per-tensor scale, reciprocal for quant-side dialects,
    fp32) companions, straight from the safetensors shards. When every expert also stores the
    dialect's static activation scale, the pieces carry it as fp32 ``_input`` (dequant side).

    Serial reads walk the shards in order; ``parallel`` uses the chunked O_DIRECT reader. Either
    way tensors of one expert may span shards, so they are grouped by (layer, expert) as they land.
    ``layers`` (bank layer ids, default all) reads only those layers' experts.

    ``skip_experts_from`` (the disk tier): experts ``[skip_experts_from, E)`` are disk-resident.
    The serial reader never calls ``get_tensor`` for them (no I/O); the parallel reader filters
    them at the reader (the whole-shard read is unchanged, but no per-expert work happens). Each
    skipped expert still yields an EMPTY piece so the bank fill completes the layer without
    touching the (released) tail rows.
    """
    from freetoken.models.loader import drop_page_cache as _drop
    from freetoken.models.loader import safetensors_weight_map
    from freetoken.moe.expert_pieces import per_expert_pieces

    drop = drop_page_cache or _drop
    folder = download_hf_weight(model_path)
    weight_map = safetensors_weight_map(folder)

    from freetoken.moe.expert_profile import new_of_old

    renumber = new_of_old(expert_order) if expert_order is not None else None
    keep = None if layers is None else set(layers)
    act = _activation_scale()
    wanted: dict[str, tuple[int, int, str]] = {}
    pair_kinds = spec.scale_pair
    for name in weight_map:
        match = spec.key_pattern.match(name)
        if match is None:
            continue
        bank_layer = _bank_layer(spec, int(match.group("layer")), config)
        if bank_layer is None or (keep is not None and bank_layer not in keep):
            continue
        # bank rows use the disk tier's renumbered ids (identity without a profile)
        row = renumber[bank_layer][int(match.group("expert"))] if renumber is not None else int(match.group("expert"))
        if skip_experts_from is not None and row >= skip_experts_from:
            continue  # disk-resident: never read
        proj = match.group("proj")
        if proj not in spec.proj_to_role:
            raise ValueError(f"{spec.desc}: unknown NVFP4 expert projection {proj!r}")
        kind = _canon_kind(spec, match.group("kind"))
        role = spec.proj_to_role[proj]
        if pair_kinds is not None:
            if kind in pair_kinds:
                wanted[name] = (bank_layer, row, f"{role}~{kind}")
            elif kind in ("weight", "weight_scale_2"):
                wanted[name] = (bank_layer, row, role + _kind_suffix(kind))
            else:
                raise ValueError(f"{spec.desc}: unknown NVFP4 expert tensor kind {kind!r}")
        elif kind not in ("weight", "weight_scale", "weight_scale_2"):
            raise ValueError(f"{spec.desc}: unknown NVFP4 expert tensor kind {kind!r}")
        else:
            wanted[name] = (bank_layer, row, role + _kind_suffix(kind))
        if kind == "weight" and act is not None:
            act_name = name[: match.start("kind")] + act.name
            if act_name in weight_map:
                wanted[act_name] = (bank_layer, row, role + "_input")
    resident = min(skip_experts_from, config.num_experts) if skip_experts_from is not None else config.num_experts
    experts = (_num_moe_layers(config) if keep is None else len(keep)) * resident
    acts = [name for name, (_, _, slot) in wanted.items() if slot.endswith("_input")]
    # a partial set serves no W4A4 kernel; the pieces then carry none
    if len(acts) != experts * 3:
        for name in acts:
            del wanted[name]
        acts = []
    # A CSF checkpoint keeps every input_scale in its own trailing shard; streaming them
    # with the weights makes the first piece wait on that shard while every other tensor
    # piles up unread in the queue. The CSF path reads them out of band instead.
    act_keys: dict[str, tuple[int, int, str]] = {}
    if pair_kinds is not None:
        for name in acts:
            act_keys[name] = wanted.pop(name)
        acts = list(act_keys)
    per_expert = (3 * (2 + len(pair_kinds)) + (3 if acts else 0)) if pair_kinds is not None else (12 if acts else 9)
    streamed = per_expert - (3 if pair_kinds is not None and acts else 0)
    if len(wanted) != experts * streamed:
        raise ValueError(f"{spec.desc}: found {len(wanted)} expert tensors, expected {experts * streamed}")

    tp = get_tp_info()

    def _local(name: str, tensor: torch.Tensor) -> torch.Tensor:
        role = wanted[name][2]
        if role.endswith(("_global", "_input")):
            return _ingest(spec, act, role, tensor)
        return shard_nvfp4_piece(role, tensor, rank=tp.rank, tp_size=tp.size)

    def _serial():
        by_shard: dict[str, list[str]] = collections.defaultdict(list)
        for name, shard in weight_map.items():
            if name in wanted:
                by_shard[shard].append(name)
        for shard in tqdm(sorted(by_shard), desc=f"Loading {spec.desc}", disable=not primary):
            path = os.path.join(folder, shard)
            drop(path)
            with safetensors.safe_open(path, framework="pt", device="cpu") as f:
                for name in by_shard[shard]:
                    piece = _local(name, f.get_tensor(name))
                    yield name, piece
                    del piece
            drop(path)

    def _parallel():
        from freetoken.models.weight import iter_expert_tensors_parallel

        for name, tensor in iter_expert_tensors_parallel(folder, lambda n: n in wanted, workers=workers, chunk=chunk):
            yield name, _local(name, tensor)

    # CSF checkpoints stream the slab parts as separate tensors; group them back into the
    # same logical roles (plus the W4A4 input scales when the set is complete), decoding
    # the scale pair on the fly.
    roles = list(spec.proj_to_role.values())
    slots_per_expert = {
        slot
        for role in roles
        for slot in [f"{role}", f"{role}_global", *(f"{role}~{kind}" for kind in pair_kinds or ())]
    }
    act_index = {key: name for name, key in act_keys.items()}

    def _csf_pieces(decoder):
        acts_in: dict[str, torch.Tensor] = {}
        if act_keys:
            act_shards: dict[str, list[str]] = collections.defaultdict(list)
            for name in act_keys:
                act_shards[weight_map[name]].append(name)
            for shard in tqdm(sorted(act_shards), desc=f"Loading {spec.desc} scales", disable=not primary):
                path = os.path.join(folder, shard)
                drop(path)
                with safetensors.safe_open(path, framework="pt", device="cpu") as f:
                    for name in act_shards[shard]:
                        acts_in[name] = _ingest(spec, act, act_keys[name][2], f.get_tensor(name))
                drop(path)

        def _assemble(layer: int, expert: int, parts: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
            grouped: dict[str, torch.Tensor] = {}
            for role in roles:
                grouped[role] = parts[role].unsqueeze(0)
                grouped[f"{role}_global"] = parts[f"{role}_global"].reshape(1, -1)
                if acts:
                    grouped[f"{role}_input"] = acts_in[act_index[(layer, expert, f"{role}_input")]].reshape(1, -1)
                # the slab pair encodes the full matrix: decode first, then take this rank's slice
                scale = decoder(*[parts[f"{role}~{kind}"] for kind in pair_kinds])
                grouped[f"{role}_scale"] = shard_nvfp4_piece(
                    f"{role}_scale", scale, rank=tp.rank, tp_size=tp.size
                ).unsqueeze(0)
            return grouped

        yield from per_expert_pieces(
            _parallel() if parallel else _serial(),
            wanted.get,
            tensors_per_expert=len(slots_per_expert),
            assemble=_assemble,
        )

    if pair_kinds is None:
        pieces = per_expert_pieces(_parallel() if parallel else _serial(), wanted.get, tensors_per_expert=per_expert)
    elif spec.scale_decoder is None:
        raise ValueError(f"{spec.desc}: scale_pair requires a scale_decoder")
    else:
        pieces = _csf_pieces(spec.scale_decoder)
    if skip_experts_from is not None:
        pieces = itertools.chain(pieces, _disk_skip_pieces(config, skip_experts_from))
    return pieces


def _disk_skip_pieces(config, skip_from: int):
    """Empty pieces for the disk-resident experts ``[skip_from, E)``: the rows are
    complete without a checkpoint read (``build_expert_banks`` marks them written,
    pins only the prefix, and releases the tail)."""
    for bank_layer in range(_num_moe_layers(config)):
        for e in range(skip_from, config.num_experts):
            yield bank_layer, e, e + 1, {}


__all__ = ["Nvfp4ExpertSourceSpec", "decode_csf_scales", "iter_nvfp4_expert_pieces"]
