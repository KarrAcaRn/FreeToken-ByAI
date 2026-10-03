"""Single-launch invalidation of the MoE prefill overlap buffers: fixed-shape, so unlike the
boolean-mask index it replaces it never hides a device-to-host sync per layer."""

import torch
import triton
import triton.language as tl


@triton.jit
def _invalidate_slots_kernel(
    id_of_slot_ptr,   # (num_slots,) int32 -- slot -> expert id, -1 if empty
    slot_for_id_ptr,  # (num_layers * num_experts) int32 -- expert id -> slot, -1 if not resident
    usage_ptr,        # (num_slots,) int64 -- last-used step; zeroed so these slots are
                      # the argmin(usage) victims in ensure_experts' eviction
    slot_start,
    n,
    BLOCK: tl.constexpr,
):
    i = tl.program_id(0) * BLOCK + tl.arange(0, BLOCK)
    m = i < n
    e = tl.load(id_of_slot_ptr + slot_start + i, mask=m, other=-1)
    # clear the expert's residency flag; empty slots (-1) are masked out
    tl.store(slot_for_id_ptr + e, -1, mask=m & (e >= 0))
    tl.store(id_of_slot_ptr + slot_start + i, -1, mask=m)
    tl.store(usage_ptr + slot_start + i, 0, mask=m)


def invalidate_prefill_slots(
    id_of_slot: torch.Tensor,
    slot_for_id: torch.Tensor,
    usage: torch.Tensor,
    slot_start: int,
    num_experts: int,
) -> None:
    """Free the ``num_experts`` slots starting at ``slot_start`` (fixed shape, no sync).

    ``slot_for_id`` may be the 2-D ``(num_layers, num_experts)`` map: ids are flat
    (``layer * num_experts + expert``) and the tensor is contiguous, so the kernel's
    flat addressing matches the ``view(-1)`` the eager path used.
    """
    # The raw-pointer kernel cannot clamp like the eager slices did; refuse a buffer
    # that does not fit instead of reading past the cache.
    if slot_start + num_experts > id_of_slot.numel():
        raise ValueError(
            f"prefill buffer [{slot_start}, {slot_start + num_experts}) exceeds "
            f"id_of_slot size {id_of_slot.numel()}"
        )
    # The kernel needs a CUDA context; CPU test caches keep the old eager path, where
    # the hidden sync is harmless (no enqueued GPU work to drain).
    if id_of_slot.device.type != "cuda":
        old_ids = id_of_slot[slot_start : slot_start + num_experts]
        slot_for_id.view(-1)[old_ids[old_ids >= 0].long()] = -1
        old_ids.fill_(-1)
        usage[slot_start : slot_start + num_experts].zero_()
        return
    grid = ((num_experts + 255) // 256,)
    _invalidate_slots_kernel[grid](
        id_of_slot, slot_for_id, usage, slot_start, num_experts, BLOCK=256
    )
