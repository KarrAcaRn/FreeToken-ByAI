import torch

from freetoken.attention.linear import build_fla_metadata
from freetoken.core import get_global_ctx
from freetoken.distributed import get_tp_info
from freetoken.kernel.causal_conv1d import causal_conv1d_decode, causal_conv1d_varlen
from freetoken.layers import BaseOP, LinearColParallelMerged, LinearRowParallel
from freetoken.utils import div_even


class ConvWeight(BaseOP):
    def __init__(self, channels):
        self.weight = torch.empty(channels, 1, 7)


class Lfm3Conv(BaseOP):
    def __init__(self, config, layer_id: int, *, prefix: str):
        self._layer_id = layer_id
        h = config.hidden_size
        self.in_proj = LinearColParallelMerged(
            h, [h, h, h], has_bias=False, quant_config=config.quant, prefix=f"{prefix}.in_proj",
        )
        self.conv = ConvWeight(div_even(h, get_tp_info().size))
        self.out_proj = LinearRowParallel(
            h, h, has_bias=False, quant_config=config.quant, prefix=f"{prefix}.out_proj",
        )

    def forward(self, x):
        ctx = get_global_ctx()
        batch, pool = ctx.batch, ctx.linear_state_pool
        fla = batch.fla_metadata
        if fla is None:
            fla = batch.fla_metadata = build_fla_metadata(batch, x.device, pool)
        state = pool.conv_states[pool.local_index(self._layer_id)]
        b, c, value = self.in_proj.forward(x).chunk(3, dim=-1)
        conv_in = b * value
        weight = self.conv.weight.squeeze(1)
        if batch.is_prefill:
            if fla.fresh_state_indices is not None:
                state.index_fill_(0, fla.fresh_state_indices, 0)
            y = causal_conv1d_varlen(
                conv_in.T.contiguous(), weight, state, fla.cu_seqlens,
                fla.cache_indices, fla.has_initial_state,
                max_seq_len=fla.max_seq_len, activation=None,
            ).T
            if fla.track_dst is not None:
                state.index_copy_(0, fla.track_dst, conv_in[fla.track_conv_src].transpose(1, 2))
        else:
            y = causal_conv1d_decode(conv_in, state, weight, fla.cache_indices, activation=None)
        return self.out_proj.forward(c * y)
