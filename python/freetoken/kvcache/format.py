from __future__ import annotations

from dataclasses import dataclass

import torch

ROW = -1  # one scale per row


@dataclass(frozen=True)
class KVFormat:
    """How one K or V row is stored in the KV pool; the encoding lives in the ``kv_rows.py`` arms of the same name."""

    name: str  # --kv-cache-dtype value and the kernels' KV_FMT
    elem_dtype: torch.dtype | None  # logical element type; None follows the compute dtype
    elem_store_dtype: torch.dtype | None  # dtype of the element tensor; None follows the compute dtype
    scale_dtype: torch.dtype | None = None  # logical scale type; None means no scale tensor
    scale_store_dtype: torch.dtype | None = None  # dtype of the scale tensor
    scale_group: int = ROW  # channels per scale
    pack: int = 1  # logical elements per element-tensor entry
    row_group: int = 0  # channels per e4m3 scale byte stored in the row after its elements; 0 = none

    def __post_init__(self) -> None:
        if (self.elem_dtype is None) != (self.elem_store_dtype is None):
            raise ValueError(f"{self.name}: elem_dtype and elem_store_dtype must be set together")
        if (self.scale_dtype is None) != (self.scale_store_dtype is None):
            raise ValueError(f"{self.name}: scale_dtype and scale_store_dtype must be set together")
        if self.scale_dtype is not None and self.scale_dtype.itemsize != self.scale_store_dtype.itemsize:
            raise ValueError(f"{self.name}: scale_store_dtype must have the size of scale_dtype")

    @property
    def quantized(self) -> bool:
        return self.elem_dtype is not None

    def elem_tensor_dtype(self, compute_dtype: torch.dtype) -> torch.dtype:
        return compute_dtype if self.elem_store_dtype is None else self.elem_store_dtype

    def elem_dim(self, head_dim: int) -> int:
        """Elements of the element tensor per row."""
        if self.elem_dtype is None:
            return head_dim
        group = max(self.pack, self.row_group)
        if head_dim % group:
            raise ValueError(f"{self.name} needs head_dim divisible by {group}, got {head_dim}")
        row_bytes = head_dim * self.elem_dtype.itemsize // self.pack
        if self.row_group:
            row_bytes += head_dim // self.row_group
        if row_bytes % self.elem_store_dtype.itemsize:
            raise ValueError(f"{self.name} cannot store a {head_dim}-wide row")
        return row_bytes // self.elem_store_dtype.itemsize

    def scale_dim(self, head_dim: int) -> int:
        """Scales per row."""
        if self.scale_dtype is None:
            return 0
        if self.scale_group == ROW:
            return 1
        if head_dim % self.scale_group:
            raise ValueError(f"{self.name} needs head_dim divisible by {self.scale_group}, got {head_dim}")
        return head_dim // self.scale_group

    def row_bytes(self, head_dim: int, compute_dtype: torch.dtype, segments: int = 1) -> int:
        """Bytes of one K or V row split into ``segments`` separately scaled parts, its scales included."""
        elem_bytes = self.elem_dim(head_dim) * self.elem_tensor_dtype(compute_dtype).itemsize
        if self.scale_dtype is None:
            return elem_bytes
        return elem_bytes + segments * self.scale_dim(head_dim) * self.scale_store_dtype.itemsize


NONE = KVFormat("none", elem_dtype=None, elem_store_dtype=None)
FP8_PER_TOKEN_HEAD = KVFormat(
    "fp8_per_token_head",
    elem_dtype=torch.float8_e4m3fn,
    elem_store_dtype=torch.uint8,
    scale_dtype=torch.float32,
    scale_store_dtype=torch.float32,
)
INT8_PER_TOKEN_HEAD = KVFormat(
    "int8_per_token_head",
    elem_dtype=torch.int8,
    elem_store_dtype=torch.int8,
    scale_dtype=torch.float32,
    scale_store_dtype=torch.float32,
)
# two e2m1 codes per byte (even channel low), then one e4m3 scale per 16 channels, then an fp32 row scale
NVFP4 = KVFormat(
    "nvfp4",
    elem_dtype=torch.uint8,
    elem_store_dtype=torch.uint8,
    scale_dtype=torch.float32,
    scale_store_dtype=torch.float32,
    pack=2,
    row_group=16,
)

# DeepSeek-V4 / V4.1 layouts, encoded by their own pools (per-tier formats in kvcache/dsv4/row_format.py); names follow vLLM
FP8_DS_MLA = KVFormat("fp8_ds_mla", elem_dtype=None, elem_store_dtype=None)
NVFP4_DS_MLA = KVFormat("nvfp4_ds_mla", elem_dtype=None, elem_store_dtype=None)

KV_FORMATS: dict[str, KVFormat] = {
    fmt.name: fmt for fmt in (NONE, FP8_PER_TOKEN_HEAD, INT8_PER_TOKEN_HEAD, NVFP4, FP8_DS_MLA, NVFP4_DS_MLA)
}
# what a pool with per-row scale tensors and a reader built on kv_rows.py can declare
ROW_SCALE_FORMATS = frozenset({NONE.name, FP8_PER_TOKEN_HEAD.name, INT8_PER_TOKEN_HEAD.name})
# ... plus nvfp4, for the pools and readers that also decode its packed rows
PACKED_ROW_SCALE_FORMATS = ROW_SCALE_FORMATS | {NVFP4.name}


# older --kv-cache-dtype spellings, kept for existing launch scripts
KV_CACHE_DTYPE_ALIASES: dict[str, str] = {"bf16": "auto", "fp8": FP8_PER_TOKEN_HEAD.name}


def canonical_kv_cache_dtype(kv_cache_dtype: str) -> str:
    """A --kv-cache-dtype value with its alias resolved."""
    return KV_CACHE_DTYPE_ALIASES.get(kv_cache_dtype, kv_cache_dtype)


def resolve_kv_format(kv_cache_dtype: str) -> KVFormat:
    """The format of a --kv-cache-dtype value; "auto" never quantizes."""
    kv_cache_dtype = canonical_kv_cache_dtype(kv_cache_dtype)
    if kv_cache_dtype == "auto":
        return NONE
    try:
        return KV_FORMATS[kv_cache_dtype]
    except KeyError:
        raise ValueError(
            f"unknown --kv-cache-dtype {kv_cache_dtype!r}; one of auto, {', '.join(KV_FORMATS)}, {', '.join(KV_CACHE_DTYPE_ALIASES)}"
        ) from None
