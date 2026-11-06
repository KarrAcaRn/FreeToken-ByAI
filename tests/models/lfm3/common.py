"""Synthetic HF checkpoint and the real model/cache/backend/graph execution path."""
import json
from dataclasses import replace

import pytest
import torch
from safetensors.torch import save_file

from freetoken.core import Batch, Context, Req, SamplingParams, set_global_ctx

requires_cuda = pytest.mark.skipif(not torch.cuda.is_available(), reason="needs CUDA")


def checkpoint(folder, sandwich=True):
    c = dict(
        architectures=['Lfm3ForCausalLM'], model_type='lfm3', num_hidden_layers=6,
        layer_types=['conv', 'full_attention', 'conv', 'sliding_attention', 'full_attention', 'conv'],
        hidden_size=128, intermediate_size=256, head_dim=64, num_attention_heads=4,
        num_key_value_heads=2, vocab_size=256, norm_eps=1e-5, conv_L_cache=7,
        conv_bias=False, use_sandwich_norm=sandwich, sliding_window=8,
        tie_word_embeddings=True, max_position_embeddings=512,
        rope_parameters={'full_attention': dict(rope_type='default', rope_theta=1e6, partial_rotary_factor=0.5),
                         'sliding_attention': dict(rope_type='default', rope_theta=1e4)},
    )
    gen = torch.Generator().manual_seed(31)
    w = {}

    def weight(name, shape, norm=False):
        t = torch.randn(shape, generator=gen) * (0.08 if norm else 0.025)
        w[name + '.weight'] = (t + 1 if norm else t).bfloat16()

    weight('model.embed_tokens', (256, 128))
    weight('model.embedding_norm', (128,), True)
    for i, kind in enumerate(c['layer_types']):
        p = f'model.layers.{i}'
        for name in ['operator_norm', 'ffn_norm'] + (['post_operator_norm', 'post_ffn_norm'] if sandwich else []):
            weight(p + '.' + name, (128,), True)
        for name, shape in [('w1', (256, 128)), ('w3', (256, 128)), ('w2', (128, 256))]:
            weight(p + '.feed_forward.' + name, shape)
        if kind == 'conv':
            for name, shape in [('in_proj', (384, 128)), ('conv', (128, 1, 7)), ('out_proj', (128, 128))]:
                weight(p + '.conv.' + name, shape)
        else:
            for name, shape in [('q_proj', (256, 128)), ('k_proj', (128, 128)), ('v_proj', (128, 128)), ('o_proj', (128, 256)), ('gate_proj', (4, 128))]:
                weight(p + '.self_attn.' + name, shape)
            for name in ['q_norm', 'k_norm']:
                weight(p + '.self_attn.' + name, (64,), True)
    (folder / 'config.json').write_text(json.dumps(c))
    save_file(w, str(folder / 'model.safetensors'))
    return c, w


class TinyEngine:
    def __init__(self, folder, graphs=False, dtype=torch.bfloat16):
        from freetoken.attention.linear import LinearAttnBackend
        from freetoken.attention.triton import TritonAttentionBackend
        from freetoken.engine.engine import _materialize_loaded_weight_state_dict
        from freetoken.engine.graph import GraphRunner
        from freetoken.kvcache import create_kvcache_pool
        from freetoken.kvcache.linear_state_pool import LinearStatePool
        from freetoken.layers import set_rope_device
        from freetoken.layers.quantization import NoQuantConfig
        from freetoken.layers.quantization.method import finalize_quant
        from freetoken.models import create_model
        from freetoken.models.lfm3 import iter_weights, parse_config
        from freetoken.scheduler.cache import CacheManager
        from freetoken.utils.hf import cached_load_hf_config
        from freetoken.utils.torch_utils import torch_dtype

        self.device = torch.device('cuda')
        self.previous_stream = torch.cuda.current_stream()
        self.stream = torch.cuda.Stream()
        self.stream.wait_stream(self.previous_stream)
        torch.cuda.set_stream(self.stream)
        set_rope_device(self.device)
        self.config = replace(parse_config(cached_load_hf_config(str(folder))), quant=NoQuantConfig())
        with torch.device('meta'), torch_dtype(dtype):
            self.model = create_model(self.config)
        weights = iter_weights(str(folder), self.device, include_moe_experts=False, include_non_moe=True)
        state = _materialize_loaded_weight_state_dict(self.model.state_dict(), weights, device=self.device)
        self.model.load_state_dict(state)
        finalize_quant(self.model)
        self.ctx = Context(page_size=1)
        set_global_ctx(self.ctx)
        self.ctx.page_table = torch.zeros(4, 512, dtype=torch.int32, device='cuda')
        self.ctx.page_table[3].fill_(2048)
        self.ctx.kv_cache = create_kvcache_pool(self.config, num_pages=2049, page_size=1,
                                             dtype=dtype, device=self.device)
        self.pool = LinearStatePool(self.config.linear_attention_group(), 32, dtype, self.device)
        self.ctx.linear_state_pool = self.pool
        self.backend = self.ctx.attn_backend = TritonAttentionBackend(self.config)
        self.linear = LinearAttnBackend(self.device, self.pool)
        self.cache = CacheManager(2048, 1, self.ctx.page_table, 'hybrid_radix', linear_state_pool=self.pool)
        self.dummy = Req(torch.tensor([0], dtype=torch.int32), 3, 0, 1, -1, SamplingParams(), None)
        self.dummy.linear_slot_idx = 0
        self.graph = GraphRunner(torch.cuda.current_stream(), self.device, self.model.forward,
                                 self.backend, [2] if graphs else [], None, 0, 512,
                                 self.dummy, linear_backend=self.linear)

    def request(self, tokens, row=0, cached=True):
        from freetoken.scheduler.prefill import PendingReq
        pending = PendingReq(input_ids=torch.tensor(tokens, dtype=torch.int32), uid=row,
                             sampling_params=SamplingParams(max_tokens=128))
        match = self.cache.match_req(pending, max_len=None if cached else 0)
        hit = match.cuda_handle.cached_len
        req = Req(pending.input_ids, row, hit, 128, row, SamplingParams(), match.cuda_handle)
        req.linear_slot_idx = self.pool.alloc(1)[0]
        req.mamba_ping_pong = tuple(self.pool.alloc(2))
        self.cache.lock(req.cache_handle)
        if hit:
            self.ctx.page_table[row, :hit] = match.cuda_handle.get_matched_indices()
            self.pool.copy_from(match.mamba_value, req.linear_slot_idx)
        return req

    def forward(self, reqs, decode=False):
        self.cache.allocate_paged(reqs)
        batch = Batch(reqs, 'decode' if decode else 'prefill')
        self.graph.pad_batch(batch)
        batch.input_ids = torch.cat([r.input_ids[r.cached_len:r.device_len] for r in batch.padded_reqs]).cuda()
        batch.positions = torch.cat([torch.arange(r.cached_len, r.device_len) for r in batch.padded_reqs]).cuda()
        batch.out_loc = torch.cat([self.ctx.page_table[r.table_idx, r.cached_len:r.device_len] for r in batch.padded_reqs])
        self.backend.prepare_metadata(batch)
        self.linear.prepare_metadata(batch)
        with self.ctx.forward_batch(batch):
            out = self.graph.replay(batch) if self.graph.can_use_cuda_graph(batch) else self.model.forward()
        return out[:len(reqs)].float().clone()

    def close(self):
        self.graph.destroy_cuda_graphs()
        self.previous_stream.wait_stream(self.stream)
        torch.cuda.set_stream(self.previous_stream)
