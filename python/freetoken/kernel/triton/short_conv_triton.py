"""Width-7 causal convolution with slot-indexed [slots, channels, 6] history.

Live requests must have distinct slots. Padding slot -1 leaves state untouched
and produces zero output. Prefill accepts channels-first packed tokens; decode
accepts one token per batch row. Both preserve the input tensor.
"""

import torch
import triton
import triton.language as tl


@triton.jit
def _prefill(X, W, S, CU, IDX, INIT, Y, D: tl.constexpr,
             X0, X1: tl.constexpr, W0: tl.constexpr, W1: tl.constexpr,
             S0: tl.constexpr, S1: tl.constexpr, S2: tl.constexpr,
             Y0, SILU: tl.constexpr, BLOCK: tl.constexpr):
    row = tl.program_id(0)
    channel = tl.program_id(1).to(tl.int64)
    t = tl.program_id(2) * BLOCK + tl.arange(0, BLOCK)
    start = tl.load(CU + row)
    length = tl.load(CU + row + 1) - start
    slot = tl.load(IDX + row).to(tl.int64)
    initial = tl.load(INIT + row) & (slot != -1)
    acc = tl.full((BLOCK,), 0, tl.float32)
    for tap in tl.static_range(7):
        pos = t + tap - 6
        current = tl.load(X + channel * X0 + (start + pos) * X1,
                          (slot != -1) & (t < length) & (pos >= 0) & (pos < length), 0)
        history = tl.load(S + slot * S0 + channel * S1 + (pos + 6) * S2,
                          initial & (t < length) & (pos < 0) & (pos >= -6), 0)
        value = tl.where(pos < 0, history, current).to(tl.float32)
        weight = tl.load(W + channel * W0 + tap * W1).to(tl.float32)
        acc += value * weight
    if SILU:
        acc = acc * tl.sigmoid(acc)
    tl.store(Y + channel * Y0 + start + t, tl.where(slot != -1, acc, 0), t < length)


@triton.jit
def _update(X, W, S, CU, IDX, INIT, Y, D: tl.constexpr,
            X0, X1: tl.constexpr, W0: tl.constexpr, W1: tl.constexpr,
            S0: tl.constexpr, S1: tl.constexpr, S2: tl.constexpr,
            DECODE: tl.constexpr, SILU: tl.constexpr, BLOCK: tl.constexpr):
    row = tl.program_id(0)
    d = tl.program_id(1).to(tl.int64) * BLOCK + tl.arange(0, BLOCK)
    k = tl.arange(0, 8)
    slot = tl.load(IDX + row).to(tl.int64)
    live = (slot != -1) & (d < D)
    if DECODE:
        start = row
        length = 1
        initial = True
    else:
        start = tl.load(CU + row)
        length = tl.load(CU + row + 1) - start
        initial = tl.load(INIT + row)
    # Gather from a complete register window before any overlapping state stores.
    old = tl.load(S + slot * S0 + d[:, None] * S1 + k[None, :] * S2,
                  live[:, None] & initial & (k[None, :] < 6), 0)
    if DECODE:
        x = tl.load(X + row * X0 + d * X1, live, 0)
        values = tl.where(k[None, :] == 6, x[:, None], old)
        weights = tl.load(W + d[:, None] * W0 + k[None, :] * W1,
                          (d[:, None] < D) & (k[None, :] < 7), 0)
        acc = tl.sum(values.to(tl.float32) * weights.to(tl.float32), 1)
        if SILU:
            acc = acc * tl.sigmoid(acc)
        tl.store(Y + row * D + d, tl.where(slot != -1, acc, 0), d < D)
    pos = length - 6 + k
    history = tl.gather(old, tl.broadcast_to(tl.minimum(length + k, 7)[None, :], (BLOCK, 8)), 1)
    if DECODE:
        current = tl.broadcast_to(x[:, None], (BLOCK, 8))
    else:
        current = tl.load(X + d[:, None] * X0 + (start + pos[None, :]) * X1,
                          live[:, None] & (pos[None, :] >= 0) & (pos[None, :] < length), 0)
    tail = tl.where(pos[None, :] < 0, history, current)
    tl.store(S + slot * S0 + d[:, None] * S1 + k[None, :] * S2, tail,
             live[:, None] & (k[None, :] < 6) & (length > 0))


def causal_conv1d_varlen(x, weight, conv_states, cu_seqlens, cache_indices,
                         has_initial_state, max_seq_len=None, activation=None):
    """Packed [channels, tokens] prefill, including continuation chunks shorter than 6.

    Pass host-known max_seq_len for CUDA graph capture. All metadata stays on
    device otherwise, except deriving that optional launch bound.
    """
    dim, total = x.shape
    assert weight.shape == (dim, 7)
    assert conv_states.shape[1:] == (dim, 6)
    assert activation in (None, "silu", "swish")
    batch = cache_indices.numel()
    assert cu_seqlens.numel() == batch + 1
    assert has_initial_state.numel() == batch
    out = torch.empty((dim, total), device=x.device, dtype=x.dtype)
    if batch == 0 or total == 0:
        return out
    if max_seq_len is None:
        max_seq_len = int((cu_seqlens[1:] - cu_seqlens[:-1]).max().item())
    assert 0 < max_seq_len <= 128 * 65535
    with torch.cuda.device(x.device):
        _prefill[(batch, dim, triton.cdiv(max_seq_len, 128))](
            x, weight, conv_states, cu_seqlens, cache_indices, has_initial_state, out,
            dim, *x.stride(), *weight.stride(), *conv_states.stride(), total,
            activation is not None, 128, enable_fp_fusion=False,
        )
        # Separate launch: every output tile must finish reading the old history.
        _update[(batch, triton.cdiv(dim, 32))](
            x, weight, conv_states, cu_seqlens, cache_indices, has_initial_state, out,
            dim, *x.stride(), *weight.stride(), *conv_states.stride(),
            False, False, 32,
        )
    return out


def causal_conv1d_decode(x, conv_state, weight, conv_state_indices, activation=None):
    """Graph-capturable [batch, channels] decode; shifts each live slot by one."""
    batch, dim = x.shape
    assert weight.shape == (dim, 7)
    assert conv_state.shape[1:] == (dim, 6)
    assert conv_state_indices.numel() == batch
    assert activation in (None, "silu", "swish")
    out = torch.empty((batch, dim), device=x.device, dtype=x.dtype)
    if batch == 0:
        return out
    with torch.cuda.device(x.device):
        _update[(batch, triton.cdiv(dim, 32))](
            x, weight, conv_state, None, conv_state_indices, None, out,
            dim, *x.stride(), *weight.stride(), *conv_state.stride(),
            True, activation is not None, 32, enable_fp_fusion=False,
        )
    return out
