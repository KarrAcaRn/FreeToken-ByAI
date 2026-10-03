"""Qwen3.8-Flash-Next checkpoint reader (the NVFP4 and the official block-fp8 releases).

Three separate paths, because the checkpoint's three weight classes live in different places:

* :func:`iter_weights` -- every dense (non-expert) tensor, with the ``model.language_model.`` prefix stripped and fused where the model expects one buffer. See ``_DenseFuser``.
* :func:`load_ple_table` -- the 47.7 GiB FP8 n-gram table, 128 checkpoint shards concatenated into one pinned :class:`HostBank`.
* :func:`nvfp4_expert_spec` -- how the routed NVFP4 experts are named, for the offload cache's expert reader.

Dropped: ``mtp.*`` (speculative head, including its stacked ``mtp.layers.0.mlp.experts.*``); ``model.visual.*`` is kept only when the model built the tower.
"""

from __future__ import annotations

import contextlib
import json
import math
import os
import re
import struct
from dataclasses import dataclass
from typing import Iterator

import safetensors
import torch
from freetoken.distributed import get_tp_info
from freetoken.models.qwen3_vl.weight import rename_vl_prefix

from freetoken.models.config import VISION_KEY_PREFIXES
from freetoken.models.loader import drop_page_cache, iter_weight_files
from freetoken.models.nvfp4_banks import (
    Nvfp4ExpertSourceSpec,
)
from freetoken.layers.quantization import get_quant_config
from freetoken.models.register import get_model_spec
from freetoken.moe.host_banks import HostBank, read_range_into
from freetoken.utils import cached_load_hf_config, download_hf_weight
from freetoken.utils.progress import byte_bar
from tqdm import tqdm

# Routed NVFP4 experts (nvidia modelopt layout): per-expert, un-fused. Matched against the RAW
# weight_map key in nvfp4_banks. The ``model.language_model.`` anchor excludes the MTP head's
# stacked ``mtp.layers.N.mlp.experts.*`` tensors.
_EXPERT_KEY_RE = re.compile(
    r"^model\.language_model\.layers\.(?P<layer>\d+)\.mlp\.experts\.(?P<expert>\d+)\."
    r"(?P<proj>gate_proj|up_proj|down_proj)\.(?P<kind>weight|weight_scale|weight_scale_2)$"
)
_EXPERT_RE = re.compile(r"\.mlp\.experts\.\d+\.")
_NVFP4_SOURCE_SPEC = Nvfp4ExpertSourceSpec(
    key_pattern=_EXPERT_KEY_RE,
    proj_to_role={"gate_proj": "gate", "up_proj": "up", "down_proj": "down"},
    layer_to_bank=lambda layer, config: layer,  # every layer is MoE
    desc="Qwen3.8-Flash-Next NVFP4 experts",
)
# Per-tensor modelopt quant scales; consumed with their ``.weight`` (experts) or unused.
_SCALE_SUFFIXES = (".weight_scale", ".weight_scale_2", ".input_scale")

# The n-gram table itself: too big for the dense state dict, loaded by load_ple_table.
_PLE_TABLE_INFIX = ".ple.ple_embedding.ngram_embedding."
_PLE_SHARD_RE = re.compile(
    r"\.ple\.ple_embedding\.ngram_embedding\.shard_(?P<shard>\d+)\.weight$"
)
_PLE_SCALE_SUFFIX = ".ple.ple_embedding.ngram_embedding.weight_scale"
_PLE_FILE_BYTES = 4 << 30  # ple-table-*.safetensors written by ftw_side_files

# Zero-centered Qwen4ExpTextRMSNorm weights, loaded RAW: GroupedPlusOneRMSNorm / GemmaPlusOneRMSNorm
# and the vendored grouped_gemma_rmsnorm all apply (1+w) at runtime in fp32, so folding the +1 into
# the bf16 weight here would double-apply it and round away small |w|. The GDN gated norm
# (linear_attn.norm) is a plain weight*x norm and is not in this set.
_ZERO_CENTERED_NORM_SUFFIXES = (
    ".hc_norm.weight",
    ".ple.norm_key.weight",
    ".ple.norm_query.weight",
    ".ple.norm_conv.weight",
    ".self_attn.q_norm.weight",
    ".self_attn.k_norm.weight",
    ".self_attn.indexer.q_layernorm.weight",
    ".self_attn.indexer.k_layernorm.weight",
)

# The per-layer HC mix reads the low-rank down projection and the injection logits from one GEMM; vLLM pads the merged rows to a multiple of 16 for cuBLAS (hyperconnection.py pad_size).
# The top-level hyper_connection_mixer has no injection and never fuses.
_PAD_TO = {"input_mix_weight_down_block_inject": 16}
_HC_WITH_INJECT = (".attn_hyper_connection", ".mlp_hyper_connection")
_KIND_SUFFIXES = (".weight_scale_inv", ".weight")
_FP8_DTYPES = (torch.float8_e4m3fn, torch.float8_e5m2)
_ELEM_DTYPES = {"e4m3": torch.float8_e4m3fn}


def _rename(raw_name: str) -> str | None:
    """Checkpoint key -> FreeToken state-dict key, or None to skip."""
    if raw_name.startswith("mtp."):
        return None
    if _PLE_TABLE_INFIX in raw_name:
        return None  # n-gram table + its scale: load_ple_table
    if _EXPERT_RE.search(raw_name):
        return None  # routed experts: offload source banks
    if raw_name.endswith(_SCALE_SUFFIXES):
        return None
    return rename_vl_prefix(raw_name)


def _split_kind(name: str) -> tuple[str, str]:
    """``name`` -> ``(module, kind)``; kind is "" for tensors that are neither a weight nor a block scale."""
    for suffix in _KIND_SUFFIXES:
        if name.endswith(suffix):
            return name[: -len(suffix)], suffix
    return name, ""


class _DenseFuser:
    """Concatenates checkpoint projection parts into the model's merged buffers, per kind (weight / block scale).

    The part table is the family's packed_modules_mapping. The QuantConfig picks the GDN in_proj layout and validates each part against the scheme the model built its buffer from.
    """

    def __init__(self, quant, packed: tuple[tuple[str, tuple[str, ...]], ...]) -> None:
        self.quant = quant
        self.groups = {fused: parts for fused, parts in packed if fused != "experts"}  # experts: bank reader
        self.by_part: dict[str, list[tuple[str, int]]] = {}
        for fused, parts in self.groups.items():
            for idx, part in enumerate(parts):
                self.by_part.setdefault(part, []).append((fused, idx))
        self.buf: dict[tuple[str, str], dict[int, torch.Tensor]] = {}

    def scheme(self, module: str):
        return None if self.quant is None else self.quant.scheme_for(module)

    def _target(self, parent: str, leaf: str) -> tuple[str, int] | None:
        candidates = self.by_part.get(leaf)
        if not candidates:
            return None
        if len(candidates) > 1:
            # GDN: quantized checkpoints split qkv|z from the bf16 b|a; same test as gdn.py
            split = self.scheme(f"{parent}.in_proj_qkvz") is not None
            keep = {"in_proj_qkvz", "in_proj_ba"} if split else {"in_proj"}
            candidates = [c for c in candidates if c[0] in keep]
            if not candidates:
                raise ValueError(f"{parent}.{leaf}: no merged projection for the {'split' if split else 'fused'} GDN layout")
        fused, idx = candidates[0]
        if fused in _PAD_TO and not parent.endswith(_HC_WITH_INJECT):
            return None
        return f"{parent}.{fused}", idx

    def check(self, module: str, name: str, tensor: torch.Tensor) -> None:
        """``tensor`` (checkpoint key ``name``) must match the scheme the model built ``module`` from."""
        scheme = self.scheme(module)
        if name.endswith(".weight_scale_inv"):
            if scheme is None or not scheme.has("weight_scale_inv"):
                raise ValueError(f"{name}: {module} has no block scale in the checkpoint's quant config ({scheme})")
            return
        is_fp8 = tensor.dtype in _FP8_DTYPES
        if scheme is None:
            if is_fp8:
                raise ValueError(f"{name} is {tensor.dtype} but the checkpoint's quant config declares {module} unquantized")
            return
        expected = _ELEM_DTYPES.get(scheme.weight.elem)
        if expected is not None and tensor.dtype is not expected:
            raise ValueError(f"{name} is {tensor.dtype} but the checkpoint's quant config declares {module} {scheme}")
        rows, cols = (scheme.weight.group or (1, 1))
        if rows > 1 and tensor.shape[0] % rows or cols > 1 and tensor.shape[1] % cols:
            raise ValueError(f"{name}: {tuple(tensor.shape)} is not a multiple of the {rows}x{cols} scale block of {module}")

    def check_unfused(self, name: str, tensor: torch.Tensor) -> None:
        module, kind = _split_kind(name)
        if kind == ".weight_scale_inv" or (kind == ".weight" and tensor.dtype in _FP8_DTYPES):
            self.check(module, name, tensor)

    def fuse(self, name: str, tensor: torch.Tensor) -> list[tuple[str, torch.Tensor]] | None:
        """Buffer a part; return the merged ``[(name, tensor)]`` once its kind is complete, ``[]`` while incomplete, ``None`` if ``name`` is not a part."""
        module, kind = _split_kind(name)
        if not kind:
            return None
        parent, _, leaf = module.rpartition(".")
        hit = self._target(parent, leaf)
        if hit is None:
            return None
        fused, idx = hit
        self.check(fused, name, tensor)
        slots = self.buf.setdefault((fused, kind), {})
        slots[idx] = tensor
        parts = self.groups[fused.rpartition(".")[2]]
        if len(slots) < len(parts):
            return []
        del self.buf[(fused, kind)]
        rows = [slots[i] for i in range(len(parts))]
        pad_to = _PAD_TO.get(fused.rpartition(".")[2], 0) if kind == ".weight" else 0
        pad = (-sum(t.shape[0] for t in rows)) % pad_to if pad_to else 0
        if pad:
            rows.append(torch.zeros(pad, *rows[0].shape[1:], dtype=rows[0].dtype, device=rows[0].device))
        return [(fused + kind, torch.cat(rows, dim=0))]


def iter_weights(
    model_path: str,
    device: torch.device,
    *,
    include_moe_experts: bool,
    include_non_moe: bool,
    include_vision: bool = True,
) -> Iterator[tuple[str, torch.Tensor]]:
    """Yield the dense (non-expert) weights, prefix-stripped and fused to the model's buffers.

    Keys keep the checkpoint's module names below the stripped prefix, so the emitted set is the model's state dict minus the routed experts.
    A dense projection is bf16 or 128x128 block-fp8 (``.weight`` e4m3 + ``.weight_scale_inv``) as the checkpoint's QuantConfig says: the official releases skip everything but the routed experts, the community NVFP4-FP8 requants quantize the attention / GDN projections.
    Fusions, per kind: attention q|k|v -> ``qkv_proj``; GDN ``in_proj_{qkv,z,b,a}`` -> ``in_proj``, or ``in_proj_qkvz`` + bf16 ``in_proj_ba`` when qkv|z is quantized; shared-expert gate|up -> ``gate_up_proj``; each per-layer HC's ``input_mix_weight_down`` | ``block_inject_weight`` -> a zero-padded ``input_mix_weight_down_block_inject``.
    ``include_moe_experts`` is accepted for the loader contract but never yields anything: the routed experts are NVFP4 and always come from the offload cache's expert reader.
    """
    if get_tp_info().size > 1:
        raise NotImplementedError("qwen4_exp weight loading supports TP=1 only")
    if not include_non_moe:
        return

    hf_config = cached_load_hf_config(model_path)
    spec = get_model_spec(hf_config.architectures[0])
    fuser = _DenseFuser(get_quant_config(), spec.packed_modules_mapping)
    for file in tqdm(
        iter_weight_files(model_path),
        desc="Loading weights",
        disable=not get_tp_info().is_primary(),
    ):
        with safetensors.safe_open(file, framework="pt", device=str(device)) as f:
            for raw_name in f.keys():
                name = _rename(raw_name)
                if name is None:
                    continue
                if not include_vision and name.startswith(VISION_KEY_PREFIXES):
                    continue
                tensor = f.get_tensor(raw_name)
                fused = fuser.fuse(name, tensor)
                if fused is None:
                    fuser.check_unfused(name, tensor)
                    yield name, tensor
                else:
                    yield from fused

    assert not fuser.buf, f"Incomplete projection fusions: {sorted(k[0] + k[1] for k in fuser.buf)}"


def iter_vision_weights(model_path: str, device: torch.device) -> Iterator[tuple[str, torch.Tensor]]:
    """The vision tower alone, named as iter_weights names it."""
    for file in iter_weight_files(model_path):
        with safetensors.safe_open(file, framework="pt", device=str(device)) as f:
            for raw_name in f.keys():
                name = _rename(raw_name)
                if name is not None and name.startswith(VISION_KEY_PREFIXES):
                    yield name, f.get_tensor(raw_name)


# ======================================================================================
# PLE n-gram table
# ======================================================================================


@dataclass(frozen=True)
class PleTable:
    """The filled n-gram table: one pinned host bank plus the checkpoint's per-tensor FP8 scale."""

    bank: HostBank
    weight_scale: torch.Tensor  # scalar, checkpoint dtype (bf16)

    @property
    def tensor(self) -> torch.Tensor:
        """``[total_rows, ngram_head_dim]`` float8_e4m3fn view of the bank."""
        return self.bank.tensor


_PLE_ST_DTYPE = "F8_E4M3"


def _safetensors_header(path: str) -> tuple[dict, int]:
    with open(path, "rb") as fh:
        n = struct.unpack("<Q", fh.read(8))[0]
        return json.loads(fh.read(n)), 8 + n


def _ple_table_files(folder: str) -> list[str]:
    """Shards holding a piece of the n-gram table, from the index when there is one."""
    index = os.path.join(folder, "model.safetensors.index.json")
    if not os.path.exists(index):
        return sorted(iter_weight_files(folder))
    with open(index, encoding="utf-8") as fh:
        weight_map = json.load(fh)["weight_map"]
    files = {shard for name, shard in weight_map.items() if _PLE_TABLE_INFIX in name}
    return sorted(os.path.join(folder, shard) for shard in files)


def ftw_side_files(model_path: str, out_dir: str) -> list[str]:
    """Write the PLE n-gram table tensors, and only those, into ``ple-table-*.safetensors`` next to an FTW checkpoint.

    The table is served from safetensors files in the checkpoint dir (see load_ple_table), not from FTW entries."""
    from safetensors.torch import save_file

    folder = download_hf_weight(model_path)
    written: list[str] = []
    batch: dict[str, torch.Tensor] = {}
    size = 0

    def flush():
        nonlocal batch, size
        if batch:
            name = f"ple-table-{len(written):05d}.safetensors"
            save_file(batch, os.path.join(out_dir, name))
            written.append(name)
            batch, size = {}, 0

    for path in _ple_table_files(folder):
        with safetensors.safe_open(path, framework="pt", device="cpu") as f:
            for key in f.keys():
                if _PLE_TABLE_INFIX not in key:
                    continue
                t = f.get_tensor(key)
                batch[key] = t
                size += t.numel() * t.element_size()
                if size >= _PLE_FILE_BYTES:
                    flush()
    flush()
    return written


@dataclass(frozen=True)
class PleShards:
    """The validated shard set: ``parts[i]`` is shard i's ``(path, absolute file offset)``, each ``rows_per_part x cols`` fp8 bytes."""

    parts: list[tuple[str, int]]
    rows_per_part: int
    cols: int
    scale: torch.Tensor  # scalar, checkpoint dtype

    @property
    def total_rows(self) -> int:
        return len(self.parts) * self.rows_per_part

    @property
    def nbytes(self) -> int:
        return self.total_rows * self.cols


def ple_table_rows(qwen4_args) -> int:
    """Rows the hash addresses, padded the way HF sizes its n-gram embedding (the one PLE table is layer 0's)."""
    from .ple import derive_ngram_hash_constants

    _, sizes, _ = derive_ngram_hash_constants(
        vocab_size=1,  # only the multipliers depend on it
        ngram_size=qwen4_args.ngram_size,
        num_ngram_heads=qwen4_args.num_ngram_heads,
        ngram_vocab_size_base=qwen4_args.ngram_vocab_size_base,
        ple_layer_index=0,
    )
    div = qwen4_args.make_ngram_vocab_size_divisible_by
    return -(-sum(sizes) // div) * div


def scan_ple_table(folder: str, qwen4_args) -> PleShards:
    """Validate the checkpoint's ``ngram_embedding.shard_<i>`` set against the config before either backend touches a row."""
    parts: dict[int, tuple[str, int]] = {}
    where: dict[int, str] = {}
    shape: list[int] | None = None
    scale_at: tuple[str, str] | None = None
    for path in _ple_table_files(folder):
        header, base = _safetensors_header(path)
        data_bytes = os.path.getsize(path) - base
        for key, meta in header.items():
            if key == "__metadata__":
                continue
            at = f"{key} in {path}"
            if key.endswith(_PLE_SCALE_SUFFIX):
                if scale_at is not None:
                    raise ValueError(f"PLE weight_scale {at}: expected one scale, already read {scale_at[1]} in {scale_at[0]}")
                scale_at = (path, key)
                continue
            match = _PLE_SHARD_RE.search(key)
            if match is None:
                continue
            if meta["dtype"] != _PLE_ST_DTYPE:
                raise ValueError(f"PLE shard {at}: dtype {meta['dtype']}, expected {_PLE_ST_DTYPE}")
            if len(meta["shape"]) != 2 or (shape is not None and meta["shape"] != shape):
                raise ValueError(f"PLE shard {at}: shape {meta['shape']}, expected {shape or '2-D'}")
            shape = meta["shape"]
            begin, end = meta["data_offsets"]
            if not 0 <= begin <= end <= data_bytes or end - begin != shape[0] * shape[1]:
                raise ValueError(
                    f"PLE shard {at}: data_offsets [{begin}, {end}), expected {shape[0] * shape[1]} bytes "
                    f"within the file's {data_bytes} data bytes"
                )
            idx = int(match.group("shard"))
            if idx in parts:
                raise ValueError(f"PLE shard {at}: duplicate index {idx}, already read {where[idx]}")
            parts[idx] = (path, base + begin)
            where[idx] = at

    n_parts = int(qwen4_args.split_ngram_parts)
    if not parts or sorted(parts) != list(range(n_parts)):
        missing = sorted(set(range(n_parts)) - set(parts))
        extra = sorted(set(parts) - set(range(n_parts)))
        raise ValueError(
            f"PLE table in {folder}: expected shards 0..{n_parts - 1}, found {len(parts)} "
            f"(missing {missing[:8]}, unexpected {extra[:8]})"
        )
    if scale_at is None:
        raise ValueError(f"PLE table in {folder}: no {_PLE_SCALE_SUFFIX[1:]} tensor")
    # read only now: safe_open validates the whole file, which would mask the per-shard errors above
    with safetensors.safe_open(scale_at[0], framework="pt", device="cpu") as f:
        scale = f.get_tensor(scale_at[1])
    value = float(scale.float().reshape(-1)[0]) if scale.numel() == 1 else math.nan
    if not math.isfinite(value) or value <= 0:
        raise ValueError(
            f"PLE weight_scale {scale_at[1]} in {scale_at[0]}: expected one finite positive value, got {scale.tolist()}"
        )
    rows, cols = shape
    want_rows = ple_table_rows(qwen4_args)
    if cols != qwen4_args.ngram_head_dim or rows * n_parts != want_rows:
        raise ValueError(
            f"PLE table in {folder} ({where[0]}): {n_parts} shards of {[rows, cols]} = {rows * n_parts} rows, "
            f"expected {want_rows} rows of {qwen4_args.ngram_head_dim} as the config addresses"
        )
    return PleShards([parts[i] for i in range(n_parts)], rows, cols, scale.reshape(()))


# Headroom left after the bank commits: the dense weights, CUDA context and staging buffers still allocate
# afterwards, and MemAvailable counts page cache that is reclaimable only in principle.
_PLE_HOST_MARGIN = 4 << 30


def _admit_host_table(nbytes: int) -> None:
    from freetoken.memory import available_host_memory

    avail = available_host_memory()
    if avail is not None and nbytes + _PLE_HOST_MARGIN > avail:
        raise MemoryError(
            f"PLE table needs {nbytes / 2**30:.1f} GiB of host RAM plus {_PLE_HOST_MARGIN / 2**30:.0f} GiB headroom, "
            f"but this process can take only {avail / 2**30:.1f} GiB; use --ple-backend disk to read rows from the checkpoint"
        )


def load_ple_table(model_path: str, qwen4_args, *, pin: bool = True,
                   workers: int = 8, chunk: int = 8 << 20) -> PleTable:
    """Concatenate the checkpoint's ``ngram_embedding.shard_<i>`` tensors into one pinned host bank.

    The checkpoint splits the table into ``split_ngram_parts`` equal row blocks named by shard
    index and scattered over the ``model-plefp8-*`` shards in header (lexicographic) order, so the
    bank is filled shard by shard at ``shard_index * rows_per_shard``. Each read is O_DIRECT: the
    table is ~47.7 GiB and must not also sit in the page cache while the bank holds the same bytes.
    """
    shards = scan_ple_table(download_hf_weight(model_path), qwen4_args)
    _admit_host_table(shards.nbytes)
    bank = HostBank((shards.total_rows, shards.cols), torch.float8_e4m3fn)
    shard_bytes = shards.rows_per_part * shards.cols
    try:
        with byte_bar(shards.nbytes, "Loading PLE table") as bar:
            buf = bank.memoryview()
            for shard, (path, offset) in enumerate(shards.parts):
                read_range_into(buf, path, file_offset=offset, nbytes=shard_bytes,
                                dest_offset=shard * shard_bytes, workers=workers, chunk=chunk)
                bar.update(shard_bytes)
        if pin and torch.cuda.is_available():
            bank.pin()
    except BaseException:
        with contextlib.suppress(Exception):  # the load failure is the error worth reporting
            bank.free()
        raise
    return PleTable(bank=bank, weight_scale=shards.scale)


# ======================================================================================
# Routed NVFP4 experts
# ======================================================================================


def nvfp4_expert_spec(model_path: str, config):
    return _NVFP4_SOURCE_SPEC


__all__ = [
    "nvfp4_expert_spec",
    "PleTable",
    "iter_weights",
    "load_ple_table",
    "scan_ple_table",
]
