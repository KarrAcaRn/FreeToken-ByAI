"""Qwen3.8-Flash-Next checkpoint reader (bf16, block-fp8, ModelOpt and llm-compressor exports).

Three separate paths, because the checkpoint's three weight classes live in different places:

* :func:`iter_weights` -- every dense (non-expert) tensor, with the ``model.language_model.`` prefix stripped and fused where the model expects one buffer. See ``_DenseReader``.
* :func:`load_ple_table` -- the n-gram table (47.7 GiB fp8 or 95.4 GiB bf16), 128 checkpoint shards concatenated into one pinned :class:`HostBank`.
* :func:`nvfp4_expert_spec` -- how the routed NVFP4 experts are named under the checkpoint's dialect, for the offload cache's expert reader.

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
from freetoken.layers.quantization import QuantConfig, QuantKind, QuantScheme, get_quant_config
from freetoken.models.register import get_model_spec
from freetoken.moe.host_banks import HostBank, read_range_into
from freetoken.utils import cached_load_hf_config, download_hf_weight
from freetoken.utils.progress import byte_bar
from tqdm import tqdm

# Routed NVFP4 experts: per-expert, un-fused. Matched against the RAW weight_map key in nvfp4_banks.
# The ``model.language_model.`` anchor excludes the MTP head's stacked ``mtp.layers.N.mlp.experts.*`` tensors.
_EXPERT_KEY_RE = (
    r"^model\.language_model\.layers\.(?P<layer>\d+)\.mlp\.experts\.(?P<expert>\d+)\."
    r"(?P<proj>gate_proj|up_proj|down_proj)\.(?P<kind>{kinds})$"
)
_EXPERT_RE = re.compile(r"\.mlp\.experts\.\d+\.")
# role -> the expert bank reader's canonical (ModelOpt) tensor kind
_BANK_KINDS = {"weight": "weight", "weight_scale": "weight_scale", "weight_global": "weight_scale_2"}

# leaves the model builds as quant-aware Linear layers: their tensors are read under the QuantConfig
_LINEAR_LEAVES = frozenset({
    "q_proj", "k_proj", "v_proj", "o_proj", "index_qk_proj",
    "in_proj_qkv", "in_proj_z", "in_proj_b", "in_proj_a", "out_proj",
    "gate_proj", "up_proj", "down_proj",
    "input_mix_weight_down", "block_inject_weight", "input_mix_weight_up",
    "key_proj", "value_proj", "lm_head",
})
# activation scales of modules whose scheme carries no input_scale role
_DROPPED_SUFFIXES = frozenset({"input_scale", "input_global_scale"})
_ELEM_DTYPES = {"e4m3": torch.float8_e4m3fn, "e2m1": torch.uint8}
_QUANT_DTYPES = (torch.float8_e4m3fn, torch.float8_e5m2, torch.uint8, torch.int8)

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


def _rename(raw_name: str) -> str | None:
    """Checkpoint key -> FreeToken state-dict key, or None to skip."""
    if raw_name.startswith("mtp."):
        return None
    if _PLE_TABLE_INFIX in raw_name:
        return None  # n-gram table + its scale: load_ple_table
    if _EXPERT_RE.search(raw_name):
        return None  # routed experts: offload source banks
    # static KV-cache scales of the quantizers; the KV cache runs in the engine's dtype
    if raw_name.endswith((".k_scale", ".v_scale", ".q_scale", ".prob_scale")):
        return None
    return rename_vl_prefix(raw_name)


def _per_row_scale(scale: torch.Tensor, rows: int) -> torch.Tensor:
    """Per-tensor scalar or per-channel ``[rows, 1]`` scale -> fp32 ``[rows]``; any other count is refused rather than broadcast onto the wrong rows."""
    flat = scale.reshape(-1).to(torch.float32)
    if flat.numel() == 1:
        return flat.expand(rows).contiguous()
    if flat.numel() != rows:
        raise ValueError(f"scale has {flat.numel()} elements for a weight with {rows} output rows (shape {tuple(scale.shape)}); expected 1 or {rows}")
    return flat.contiguous()


class _DenseReader:
    """Routes each Linear tensor to the buffer its module's scheme declares; packed projections are concatenated per role once every part is in.

    The part table is the family's packed_modules_mapping. The QuantConfig picks the GDN in_proj layout and, through its dialect's storage names, which checkpoint tensor fills which role.
    """

    def __init__(self, quant: QuantConfig | None, packed: tuple[tuple[str, tuple[str, ...]], ...]) -> None:
        self.quant = quant
        self.groups = {fused: parts for fused, parts in packed if fused != "experts"}  # experts: bank reader
        self.by_part: dict[str, list[tuple[str, int]]] = {}
        for fused, parts in self.groups.items():
            for idx, part in enumerate(parts):
                self.by_part.setdefault(part, []).append((fused, idx))
        # target module -> (part count, {part: {role: tensor}}, {part: the roles its module stores}, scheme)
        self.pending: dict[str, tuple[int, dict[int, dict[str, torch.Tensor]], dict[int, set[str]], QuantScheme | None]] = {}

    def scheme(self, module: str) -> QuantScheme | None:
        return None if self.quant is None else self.quant.scheme_for(module)

    def target(self, module: str) -> tuple[str, int, int]:
        """``(fused module, part index, part count)``; a standalone linear is its own single-part target."""
        parent, _, leaf = module.rpartition(".")
        candidates = self.by_part.get(leaf)
        if not candidates:
            return module, 0, 1
        if len(candidates) > 1:
            # GDN: quantized checkpoints split qkv|z from b|a; same test as gdn.py
            split = self.scheme(f"{parent}.in_proj_qkvz") is not None
            keep = {"in_proj_qkvz", "in_proj_ba"} if split else {"in_proj"}
            candidates = [c for c in candidates if c[0] in keep]
        fused, idx = candidates[0]
        if fused in _PAD_TO and not parent.endswith(_HC_WITH_INJECT):
            return module, 0, 1
        return f"{parent}.{fused}", idx, len(self.groups[fused])

    def add(self, name: str, tensor: torch.Tensor) -> list[tuple[str, torch.Tensor]] | None:
        """Take one tensor; the emitted ``[(name, tensor)]`` once its target module is complete, ``[]`` before, None if ``name`` is not a Linear's tensor."""
        module, _, suffix = name.rpartition(".")
        if module.rpartition(".")[2] not in _LINEAR_LEAVES:
            return None
        scheme = self.scheme(module)
        roles = {"weight": "weight"} if scheme is None else {n: r for r, e in self.quant.storage(scheme).items() for n in e.names}
        role = roles.get(suffix)
        if role is None:
            if suffix in _DROPPED_SUFFIXES:
                return []
            raise ValueError(f"{name}: the checkpoint's quant config declares {module} {scheme or 'unquantized'}, stored as {sorted(roles)}")
        if role == "weight":
            self._check_weight(name, module, scheme, tensor)
        target, idx, count = self.target(module)
        _, parts, expected, _ = self.pending.setdefault(target, (count, {}, {}, scheme))
        part = parts.setdefault(idx, {})
        if role in part:
            raise ValueError(f"{name}: {module} already has its {role} from another checkpoint tensor")
        part[role] = tensor
        expected[idx] = set(roles.values())
        if scheme is not None and set(part) == expected[idx]:
            parts[idx] = self._finish(module, scheme, part)
        if len(parts) < count or any(set(parts[i]) != expected[i] for i in parts):
            return []
        del self.pending[target]
        return self._emit(target, [parts[i] for i in range(count)], scheme)

    def missing(self) -> list[str]:
        """One line per incomplete module: the roles its parts still lack."""
        lines = []
        for target, (count, parts, expected, _scheme) in sorted(self.pending.items()):
            lacking = sorted(set().union(*(expected[i] - set(parts[i]) for i in parts)))
            if len(parts) < count:
                lacking.append(f"{count - len(parts)} of {count} fused parts")
            lines.append(f"{target}: missing {lacking}")
        return lines

    @staticmethod
    def _check_weight(name: str, module: str, scheme: QuantScheme | None, tensor: torch.Tensor) -> None:
        if scheme is None:
            if tensor.dtype in _QUANT_DTYPES:
                raise ValueError(f"{name} is {tensor.dtype} but the checkpoint's quant config declares {module} unquantized")
            return
        elem = _ELEM_DTYPES.get(scheme.weight.elem)
        if elem is None:
            raise ValueError(f"{name}: qwen4_exp has no dense reader for {scheme}")
        if tensor.dtype is not elem:
            raise ValueError(f"{name} is {tensor.dtype} but the checkpoint's quant config declares {module} {scheme}")
        rows, cols = tensor.shape[0], tensor.shape[1] * (2 if scheme.weight.elem == "e2m1" else 1)
        block_rows, block_cols = scheme.weight.group or (1, 1)
        if block_rows > 1 and rows % block_rows or block_cols > 1 and cols % block_cols:
            raise ValueError(f"{name}: {rows}x{cols} is not a multiple of the {block_rows}x{block_cols} scale block of {module}")

    def _finish(self, module: str, scheme: QuantScheme, part: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
        """Validate one complete part against ``scheme`` and put its scales in the layer's form."""
        storage = self.quant.storage(scheme)
        part = {role: 1.0 / t.to(torch.float32) if storage[role].reciprocal else t for role, t in part.items()}
        weight = part["weight"]
        rows, cols = weight.shape[0], weight.shape[1] * (2 if scheme.weight.elem == "e2m1" else 1)
        block_rows, block_cols = scheme.weight.group or (1, 1)
        scale_role = "weight_scale_inv" if "weight_scale_inv" in part else "weight_scale"
        out = dict(part)
        if block_cols < 0:
            try:
                out[scale_role] = _per_row_scale(part[scale_role], rows)
            except ValueError as exc:
                raise ValueError(f"{module}.{scale_role}: {exc}") from None
        else:
            want = (rows // block_rows, cols // block_cols)
            if tuple(part[scale_role].shape) != want:
                raise ValueError(f"{module}: {scale_role} is {tuple(part[scale_role].shape)}, expected {want} for {scheme}")
            if scheme.weight.scale == "e4m3" and part[scale_role].dtype is not torch.float8_e4m3fn:
                raise ValueError(f"{module}: {scale_role} is {part[scale_role].dtype} but {scheme} stores e4m3 scales")
        if "weight_global" in part:
            g = part["weight_global"].reshape(-1).to(torch.float32)
            if g.numel() != 1:
                raise ValueError(f"{module}: weight_global has {g.numel()} elements, expected one per-tensor scale")
            out["weight_global"] = g.expand(rows).contiguous()
        if "input_scale" in part:
            out["input_scale"] = part["input_scale"].reshape(()).to(torch.float32)
        return out

    @staticmethod
    def _emit(target: str, parts: list[dict[str, torch.Tensor]], scheme: QuantScheme | None) -> list[tuple[str, torch.Tensor]]:
        pad_to = _PAD_TO.get(target.rpartition(".")[2], 0)
        if pad_to and scheme is not None:
            raise ValueError(f"{target}: qwen4_exp pads this fusion to {pad_to} rows and reads it bf16 only, the checkpoint's quant config declares {scheme}")
        out = []
        for role in parts[0]:
            tensors = [part[role] for part in parts]
            if role == "input_scale":
                # fused parts read the same activation, so one range covers them: max is exact then and safe if they drift
                out.append((f"{target}.{role}", torch.stack(tensors).max()))
                continue
            pad = (-sum(t.shape[0] for t in tensors)) % pad_to if pad_to else 0
            if pad:
                tensors.append(torch.zeros(pad, *tensors[0].shape[1:], dtype=tensors[0].dtype, device=tensors[0].device))
            out.append((f"{target}.{role}", tensors[0] if len(tensors) == 1 else torch.cat(tensors, dim=0)))
        return out


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
    Each Linear is read under the scheme the checkpoint's QuantConfig gives it, the same answer the model built its buffers from, so bf16, per-channel / per-tensor fp8, block-fp8, MXFP8 and NVFP4 projections in any mix land as the model's state dict.
    Fusions, per role: attention q|k|v -> ``qkv_proj``; GDN ``in_proj_{qkv,z,b,a}`` -> ``in_proj``, or ``in_proj_qkvz`` + ``in_proj_ba`` when qkv|z is quantized; shared-expert gate|up -> ``gate_up_proj``; each per-layer HC's ``input_mix_weight_down`` | ``block_inject_weight`` -> a zero-padded ``input_mix_weight_down_block_inject``.
    ``include_moe_experts`` is accepted for the loader contract but never yields anything: the routed experts are NVFP4 and always come from the offload cache's expert reader.
    """
    if get_tp_info().size > 1:
        raise NotImplementedError("qwen4_exp weight loading supports TP=1 only")
    if not include_non_moe:
        return

    hf_config = cached_load_hf_config(model_path)
    spec = get_model_spec(hf_config.architectures[0])
    reader = _DenseReader(get_quant_config(), spec.packed_modules_mapping)
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
                emitted = None if name.startswith(VISION_KEY_PREFIXES) else reader.add(name, tensor)
                if emitted is None:
                    yield name, tensor
                else:
                    yield from emitted

    if reader.pending:
        lines = reader.missing()
        shown = "\n  ".join(lines[:8]) + (f"\n  ... {len(lines) - 8} more" if len(lines) > 8 else "")
        raise ValueError(f"checkpoint is missing tensors the quant config declares for {len(lines)} modules:\n  {shown}")


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
    """The filled n-gram table: one pinned host bank plus the checkpoint's per-tensor scale (1 for a bf16 table).

    FP8 / bf16 checkpoints fill the bank with e4m3 / bf16 rows; NVFP4 checkpoints fill it with packed
    uint8 rows (two e2m1 codes per byte) plus ``scale_bank``, the per-16-element fp8 block
    scales, and keep the global scalar in ``weight_scale`` (``weight_scale_2`` upstream)."""

    bank: HostBank
    weight_scale: torch.Tensor  # scalar, checkpoint dtype (bf16)
    scale_bank: HostBank | None = None  # ``[total_rows, ngram_head_dim // 16]`` fp8, NVFP4 only

    @property
    def tensor(self) -> torch.Tensor:
        """Bank view: ``[total_rows, ngram_head_dim]`` in the stored dtype (fp8 / bf16), or uint8 packed rows when NVFP4."""
        return self.bank.tensor


_PLE_ST_DTYPES = {"F8_E4M3": torch.float8_e4m3fn, "BF16": torch.bfloat16}
_PLE_SCALE_DTYPE = "F8_E4M3"
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
    """The validated shard set: ``parts[i]`` is shard i's ``(path, absolute file offset)``, each ``rows_per_part x cols`` values of ``dtype``."""

    parts: list[tuple[str, int]]
    rows_per_part: int
    cols: int  # stored values per row: head_dim fp8 / bf16 values, or head_dim / 2 bytes when NVFP4-packed
    scale: torch.Tensor  # scalar, checkpoint dtype (1 for a bf16 table without one); NVFP4's global weight_scale_2
    packed: bool = False
    # NVFP4 only: shard i's per-16-element fp8 block scales, ``rows_per_part x cols // 8`` bytes each
    block_parts: list[tuple[str, int]] | None = None
    dtype: torch.dtype = torch.float8_e4m3fn  # stored row dtype; uint8 when NVFP4-packed

    @property
    def row_bytes(self) -> int:
        return self.cols * self.dtype.itemsize

    @property
    def total_rows(self) -> int:
        return len(self.parts) * self.rows_per_part

    @property
    def nbytes(self) -> int:
        return self.total_rows * (self.row_bytes + (self.cols // 8 if self.packed else 0))


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

    FP8 tables carry e4m3 rows and one ``weight_scale``, bf16 tables bf16 rows and an optional one; NVFP4 tables carry packed uint8 rows, a
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
                if meta["dtype"] != _PLE_SCALE_DTYPE:
                    raise ValueError(f"PLE block scale {at}: dtype {meta['dtype']}, expected {_PLE_SCALE_DTYPE}")
                if len(meta["shape"]) != 2 or (block_shape is not None and meta["shape"] != block_shape):
                    raise ValueError(f"PLE block scale {at}: shape {meta['shape']}, expected {block_shape or '2-D'}")
                block_shape = meta["shape"]
                expect, found = block_shape, blocks
            else:
                if meta["dtype"] not in (*_PLE_ST_DTYPES, _PLE_PACKED_DTYPE) or dtype not in (None, meta["dtype"]):
                    expected = dtype or f"one of {sorted((*_PLE_ST_DTYPES, _PLE_PACKED_DTYPE))}"
                    raise ValueError(f"PLE shard {at}: dtype {meta['dtype']}, expected {expected} for every shard")
                dtype = meta["dtype"]
                if len(meta["shape"]) != 2 or (shape is not None and meta["shape"] != shape):
                    raise ValueError(f"PLE shard {at}: shape {meta['shape']}, expected {shape or '2-D'}")
                shape = meta["shape"]
                expect, found = shape, parts
            begin, end = meta["data_offsets"]
            want_bytes = expect[0] * expect[1] * (2 if not is_block and dtype == "BF16" else 1)
            if not 0 <= begin <= end <= data_bytes or end - begin != want_bytes:
                raise ValueError(
                    f"PLE shard {at}: data_offsets [{begin}, {end}), expected {want_bytes} bytes "
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
    if scale_at is None and dtype != "BF16":
        raise ValueError(f"PLE table in {folder}: no {scalar_suffix[1:]} tensor")
    if scale_at is None:
        scale = torch.tensor(1.0, dtype=torch.bfloat16)  # an unscaled bf16 table
    else:
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
        dtype=torch.uint8 if packed else _PLE_ST_DTYPES[dtype],
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
    table is ~47.7 GiB (fp8) and must not also sit in the page cache while the bank holds the same bytes.
    An fp8 table needs the checkpoint's scalar ``weight_scale``; a bf16 table without one is unscaled.
    """
    shards = scan_ple_table(download_hf_weight(model_path), qwen4_args)
    _admit_host_table(shards.nbytes)
    bank = HostBank((shards.total_rows, shards.cols), shards.dtype)
    jobs = [(shards.parts, bank, shards.row_bytes)]
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


def nvfp4_expert_spec(model_path: str, config) -> Nvfp4ExpertSourceSpec:
    """The per-expert NVFP4 layout under the checkpoint's dialect names (ModelOpt or llm-compressor)."""
    quant = get_quant_config()
    stored = quant.stored_tensors(QuantKind.NVFP4)
    kind_map = {stored[role].name: kind for role, kind in _BANK_KINDS.items()}
    return Nvfp4ExpertSourceSpec(
        key_pattern=re.compile(_EXPERT_KEY_RE.format(kinds="|".join(map(re.escape, kind_map)))),
        proj_to_role={"gate_proj": "gate", "up_proj": "up", "down_proj": "down"},
        layer_to_bank=lambda layer, config: layer,  # every layer is MoE
        desc=f"Qwen3.8-Flash-Next NVFP4 experts ({quant.dialect})",
        kind_map=kind_map,
        global_reciprocal=stored["weight_global"].reciprocal,
    )


__all__ = [
    "nvfp4_expert_spec",
    "PleTable",
    "iter_weights",
    "load_ple_table",
    "ple_table_is_packed",
    "scan_ple_table",
]
