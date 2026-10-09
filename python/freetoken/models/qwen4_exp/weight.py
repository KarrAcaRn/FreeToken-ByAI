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
from freetoken.distributed.pipeline import keeps_weight
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


# state-dict prefixes only the last pipeline stage builds
_PP_TAIL = ("lm_head.", "model.hyper_connection_mixer.")


def _rename(raw_name: str, quant) -> str | None:
    """Checkpoint key -> FreeToken state-dict key, or None to skip.

    ``quant`` is the checkpoint's QuantConfig when the file can carry quantized tensors;
    ``None`` skips every scale, correct where weights are never quantized (the vision tower)."""
    if raw_name.startswith("mtp."):
        return None
    if _PLE_TABLE_INFIX in raw_name:
        return None  # n-gram table + its scale: load_ple_table
    if _EXPERT_RE.search(raw_name):
        return None  # routed experts: offload source banks
    if raw_name.endswith(_SCALE_SUFFIXES):
        return _dialect_scale_rename(raw_name, quant) if quant is not None else None
    return rename_vl_prefix(raw_name)


def _dialect_scale_rename(raw_name: str, quant) -> str | None:
    """A scale the dialect stores under a name the state dict does not use, renamed per its storage table; None to skip.

    ModelOpt exports MXFP8 block scales as ``.weight_scale`` while the module loads them as ``weight_scale_inv``."""
    if not raw_name.endswith(".weight_scale"):
        return None
    module = rename_vl_prefix(raw_name[: -len(".weight_scale")])
    scheme = quant.scheme_for(module)
    if scheme is None:
        return None
    for role, stored in quant.storage(scheme).items():
        if stored.name == "weight_scale" and role.endswith("_scale_inv"):
            return module + "." + role
    return None


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
    A dense projection is bf16, 128x128 block-fp8 (``.weight`` e4m3 + ``.weight_scale_inv``) or MXFP8 (e4m3 + e8m0 per 32, stored ``.weight_scale``) as the checkpoint's QuantConfig says: the official releases skip everything but the routed experts, the community requants quantize the attention / GDN projections.
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
                name = _rename(raw_name, fuser.quant)
                if name is None:
                    continue
                if not include_vision and name.startswith(VISION_KEY_PREFIXES):
                    continue
                if not keeps_weight(name, tail=_PP_TAIL):
                    continue  # another pipeline stage's tensor
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
                name = _rename(raw_name, None)
                if name is not None and name.startswith(VISION_KEY_PREFIXES):
                    yield name, f.get_tensor(raw_name)


# ======================================================================================
# PLE n-gram table
# ======================================================================================


@dataclass(frozen=True)
class PleTable:
    """The filled n-gram table: one pinned host bank plus the checkpoint's per-tensor scale.

    FP8 checkpoints fill the bank with e4m3 rows; NVFP4 checkpoints fill it with packed
    uint8 rows (two e2m1 codes per byte) plus ``scale_bank``, the per-16-element fp8 block
    scales, and keep the global scalar in ``weight_scale`` (``weight_scale_2`` upstream)."""

    bank: HostBank
    weight_scale: torch.Tensor  # scalar, checkpoint dtype (bf16)
    scale_bank: HostBank | None = None  # ``[total_rows, ngram_head_dim // 16]`` fp8, NVFP4 only

    @property
    def tensor(self) -> torch.Tensor:
        """Bank view: ``[total_rows, ngram_head_dim]`` fp8, or uint8 packed rows when NVFP4."""
        return self.bank.tensor


_PLE_ST_DTYPE = "F8_E4M3"
_PLE_PACKED_DTYPE = "U8"
_PLE_SCALE2_SUFFIX = ".ple.ple_embedding.ngram_embedding.weight_scale_2"
_PLE_SHARD_SCALE_RE = re.compile(
    r"\.ple\.ple_embedding\.ngram_embedding\.shard_(?P<shard>\d+)\.weight_scale$"
)


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


def ple_table_is_packed(model_path: str) -> bool:
    """True when the n-gram table shards are NVFP4-packed: reads headers, no payloads."""
    folder = download_hf_weight(model_path)
    for path in _ple_table_files(folder):
        header, _ = _safetensors_header(path)
        for key, meta in header.items():
            if _PLE_SHARD_RE.search(key) is not None:
                return meta["dtype"] == _PLE_PACKED_DTYPE
    return False


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
    cols: int  # stored bytes per row: head_dim fp8 codes, or head_dim / 2 when NVFP4-packed
    scale: torch.Tensor  # scalar, checkpoint dtype; NVFP4's global weight_scale_2
    packed: bool = False
    # NVFP4 only: shard i's per-16-element fp8 block scales, ``rows_per_part x cols // 8`` bytes each
    block_parts: list[tuple[str, int]] | None = None

    @property
    def total_rows(self) -> int:
        return len(self.parts) * self.rows_per_part

    @property
    def nbytes(self) -> int:
        return self.total_rows * (self.cols + (self.cols // 8 if self.packed else 0))


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
    """Validate the checkpoint's ``ngram_embedding.shard_<i>`` set against the config before either backend touches a row.

    FP8 tables carry e4m3 rows and one ``weight_scale``; NVFP4 tables carry packed uint8 rows, a
    ``shard_<i>.weight_scale`` block-scale tensor per shard and the global ``weight_scale_2``."""
    parts: dict[int, tuple[str, int]] = {}
    blocks: dict[int, tuple[str, int]] = {}
    where: dict[int, str] = {}
    blocks_at: dict[int, str] = {}
    shape: list[int] | None = None
    block_shape: list[int] | None = None
    dtype: str | None = None
    scalars: dict[str, tuple[str, str]] = {}  # suffix -> (path, key)
    for path in _ple_table_files(folder):
        header, base = _safetensors_header(path)
        data_bytes = os.path.getsize(path) - base
        for key, meta in header.items():
            if key == "__metadata__":
                continue
            at = f"{key} in {path}"
            suffix = next((x for x in (_PLE_SCALE2_SUFFIX, _PLE_SCALE_SUFFIX) if key.endswith(x)), None)
            if suffix is not None:
                if suffix in scalars:
                    name = suffix.rpartition(".")[2]
                    raise ValueError(f"PLE {name} {at}: expected one scale, already read {scalars[suffix][1]} in {scalars[suffix][0]}")
                scalars[suffix] = (path, key)
                continue
            match = _PLE_SHARD_RE.search(key)
            is_block = False
            if match is None:
                match = _PLE_SHARD_SCALE_RE.search(key)
                if match is None:
                    continue
                is_block = True
            if is_block:
                if meta["dtype"] != _PLE_ST_DTYPE:
                    raise ValueError(f"PLE block scale {at}: dtype {meta['dtype']}, expected {_PLE_ST_DTYPE}")
                if len(meta["shape"]) != 2 or (block_shape is not None and meta["shape"] != block_shape):
                    raise ValueError(f"PLE block scale {at}: shape {meta['shape']}, expected {block_shape or '2-D'}")
                block_shape = meta["shape"]
                expect, found = block_shape, blocks
            else:
                if meta["dtype"] not in (_PLE_ST_DTYPE, _PLE_PACKED_DTYPE) or dtype not in (None, meta["dtype"]):
                    raise ValueError(f"PLE shard {at}: dtype {meta['dtype']}, expected {dtype or _PLE_ST_DTYPE}")
                dtype = meta["dtype"]
                if len(meta["shape"]) != 2 or (shape is not None and meta["shape"] != shape):
                    raise ValueError(f"PLE shard {at}: shape {meta['shape']}, expected {shape or '2-D'}")
                shape = meta["shape"]
                expect, found = shape, parts
            begin, end = meta["data_offsets"]
            if not 0 <= begin <= end <= data_bytes or end - begin != expect[0] * expect[1]:
                raise ValueError(
                    f"PLE shard {at}: data_offsets [{begin}, {end}), expected {expect[0] * expect[1]} bytes "
                    f"within the file's {data_bytes} data bytes"
                )
            idx = int(match.group("shard"))
            seen = blocks_at if is_block else where
            if idx in found:
                raise ValueError(f"PLE shard {at}: duplicate index {idx}, already read {seen[idx]}")
            found[idx] = (path, base + begin)
            seen[idx] = at

    n_parts = int(qwen4_args.split_ngram_parts)
    if not parts or sorted(parts) != list(range(n_parts)):
        missing = sorted(set(range(n_parts)) - set(parts))
        extra = sorted(set(parts) - set(range(n_parts)))
        raise ValueError(
            f"PLE table in {folder}: expected shards 0..{n_parts - 1}, found {len(parts)} "
            f"(missing {missing[:8]}, unexpected {extra[:8]})"
        )
    packed = dtype == _PLE_PACKED_DTYPE
    rows, cols = shape
    if packed:
        if sorted(blocks) != list(range(n_parts)) or block_shape != [rows, cols // 8]:
            raise ValueError(
                f"NVFP4 PLE table in {folder}: expected block-scale shards 0..{n_parts - 1} of {[rows, cols // 8]}, "
                f"found {len(blocks)} of {block_shape}"
            )
    # NVFP4 keeps the global scalar in weight_scale_2; FP8 exports carry it as weight_scale
    scalar_suffix = _PLE_SCALE2_SUFFIX if packed else _PLE_SCALE_SUFFIX
    scale_at = scalars.get(scalar_suffix)
    if scale_at is None:
        raise ValueError(f"PLE table in {folder}: no {scalar_suffix[1:]} tensor")
    # read only now: safe_open validates the whole file, which would mask the per-shard errors above
    with safetensors.safe_open(scale_at[0], framework="pt", device="cpu") as f:
        scale = f.get_tensor(scale_at[1])
    value = float(scale.float().reshape(-1)[0]) if scale.numel() == 1 else math.nan
    if not math.isfinite(value) or value <= 0:
        raise ValueError(
            f"PLE {scalar_suffix.rpartition('.')[2]} {scale_at[1]} in {scale_at[0]}: expected one finite positive value, "
            f"got {scale.tolist()}"
        )
    width = cols * 2 if packed else cols
    want_rows = ple_table_rows(qwen4_args)
    if width != qwen4_args.ngram_head_dim or rows * n_parts != want_rows:
        raise ValueError(
            f"PLE table in {folder} ({where[0]}): {n_parts} shards of {[rows, width]} = {rows * n_parts} rows, "
            f"expected {want_rows} rows of {qwen4_args.ngram_head_dim} as the config addresses"
        )
    return PleShards(
        [parts[i] for i in range(n_parts)], rows, cols, scale.reshape(()), packed=packed,
        block_parts=[blocks[i] for i in range(n_parts)] if packed else None,
    )


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
    bank = HostBank((shards.total_rows, shards.cols), torch.uint8 if shards.packed else torch.float8_e4m3fn)
    jobs = [(shards.parts, bank, shards.cols)]
    scale_bank = None
    if shards.packed:
        scale_bank = HostBank((shards.total_rows, shards.cols // 8), torch.float8_e4m3fn)
        jobs.append((shards.block_parts, scale_bank, shards.cols // 8))
    try:
        with byte_bar(shards.nbytes, "Loading PLE table") as bar:
            for src, dst, row_bytes in jobs:
                buf = dst.memoryview()
                shard_bytes = shards.rows_per_part * row_bytes
                for shard, (path, offset) in enumerate(src):
                    read_range_into(buf, path, file_offset=offset, nbytes=shard_bytes,
                                    dest_offset=shard * shard_bytes, workers=workers, chunk=chunk)
                    bar.update(shard_bytes)
        if pin and torch.cuda.is_available():
            bank.pin()
            if scale_bank is not None:
                scale_bank.pin()
    except BaseException:
        with contextlib.suppress(Exception):  # the load failure is the error worth reporting
            bank.free()
            if scale_bank is not None:
                scale_bank.free()
        raise
    return PleTable(bank=bank, weight_scale=shards.scale, scale_bank=scale_bank)


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
    "ple_table_is_packed",
    "scan_ple_table",
]
