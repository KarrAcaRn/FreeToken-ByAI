"""Slot-indexed causal depthwise convolution via sgl_kernel or Triton.

State is updated in place in [num_slots, conv_dim, kernel-1] layout.
Activation defaults to silu. Width 7 always uses a dedicated Triton path;
pass activation=None for LFM3's short convolution.
"""
from __future__ import annotations

import torch

_PAD_SLOT_ID = -1


def causal_conv1d_varlen(
    x: torch.Tensor,            # [conv_dim, total_tokens] (channels-first, last dim contiguous)
    weight: torch.Tensor,       # [conv_dim, kernel]
    conv_states: torch.Tensor,  # [num_slots, conv_dim, kernel-1] (updated in place)
    cu_seqlens: torch.Tensor,   # [batch+1] int32 prefix sums of per-request lengths
    cache_indices: torch.Tensor,    # [batch] int32 slot id per request
    has_initial_state: torch.Tensor,  # [batch] bool (carry conv state across chunks)
    max_seq_len: int | None = None,   # host-known longest extend_len; None derives it on device
    activation: str | None = "silu",
) -> torch.Tensor:
    """Varlen (prefill) depthwise causal conv; returns activation(conv) and refreshes
    ``conv_states[cache_indices]`` with each request's tail.

    Whether ``x`` survives depends on the backend: sgl_kernel convolves ``x`` in place and
    returns it, while the triton fallback leaves ``x`` untouched and returns a new tensor.
    Callers must use the returned tensor and must not rely on ``x`` afterwards (every
    current call site builds ``x`` fresh and never reads it again).

    ``max_seq_len`` only sizes the triton launch grid. Deriving it from ``cu_seqlens`` costs a
    D2H sync per prefill, which is illegal under CUDA graph capture, so the scheduler passes the
    host value it already has."""
    from freetoken.kernel.backend import is_sgl_kernel_installed

    assert activation in (None, "silu", "swish")
    if weight.shape[-1] == 7:
        from freetoken.kernel.triton.short_conv_triton import causal_conv1d_varlen as short_conv

        return short_conv(
            x, weight, conv_states, cu_seqlens, cache_indices, has_initial_state,
            max_seq_len=max_seq_len, activation=activation,
        )

    if not is_sgl_kernel_installed():
        from freetoken.kernel.triton.causal_conv1d_triton import (
            causal_conv1d_varlen as triton_causal_conv1d_varlen,
        )

        return triton_causal_conv1d_varlen(
            x, weight, conv_states, cu_seqlens, cache_indices, has_initial_state,
            max_seq_len=max_seq_len, activation=activation,
        )

    from sgl_kernel import causal_conv1d_fwd

    if x.stride(-1) != 1:
        x = x.contiguous()
    causal_conv1d_fwd(
        x, weight, None, conv_states,
        cu_seqlens.to(torch.int32), cache_indices.to(torch.int32),
        has_initial_state, activation is not None, _PAD_SLOT_ID,
    )
    return x


def causal_conv1d_verify(
    x: torch.Tensor,                # [batch, conv_dim, seqlen] (any strides)
    conv_state: torch.Tensor,       # [num_slots, conv_dim, kernel-1] (rolled in place)
    weight: torch.Tensor,           # [conv_dim, kernel]
    conv_state_indices: torch.Tensor,          # [batch] int32 slot id per request
    intermediate_conv_window: torch.Tensor,    # [rows, steps, conv_dim, kernel-1], row = batch row
) -> torch.Tensor:
    """Speculative-verify conv; triton only, as sgl_kernel's update keeps no per-token window."""
    from freetoken.kernel.triton.causal_conv1d_triton import (
        causal_conv1d_verify as triton_causal_conv1d_verify,
    )

    return triton_causal_conv1d_verify(x, conv_state, weight, conv_state_indices, intermediate_conv_window)


def causal_conv1d_decode(
    x: torch.Tensor,                # [batch, conv_dim] (one token per request)
    conv_state: torch.Tensor,       # [num_slots, conv_dim, kernel-1] (in place)
    weight: torch.Tensor,           # [conv_dim, kernel]
    conv_state_indices: torch.Tensor,  # [batch] int32 slot id per request
    activation: str | None = "silu",
) -> torch.Tensor:
    """Single-token (decode) causal conv update; shifts+appends the new
    token into ``conv_state[conv_state_indices]`` in place and returns activation(conv)."""
    from freetoken.kernel.backend import is_sgl_kernel_installed

    assert activation in (None, "silu", "swish")
    if weight.shape[-1] == 7:
        from freetoken.kernel.triton.short_conv_triton import causal_conv1d_decode as short_conv

        return short_conv(x, conv_state, weight, conv_state_indices, activation=activation)

    if not is_sgl_kernel_installed():
        from freetoken.kernel.triton.causal_conv1d_triton import (
            causal_conv1d_decode as triton_causal_conv1d_decode,
        )

        return triton_causal_conv1d_decode(x, conv_state, weight, conv_state_indices, activation=activation)

    from sgl_kernel import causal_conv1d_update

    x = x.unsqueeze(-1)
    causal_conv1d_update(
        x, conv_state, weight, None, activation is not None, None,
        conv_state_indices.to(torch.int32), _PAD_SLOT_ID,
    )
    return x.squeeze(-1)
