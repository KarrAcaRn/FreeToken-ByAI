# Copyright 2026 The HuggingFace Team. All rights reserved.
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).
"""Torch transcription of LiquidAI/LFM3-1.7B modeling_lfm3.py,
revision ac2586a34f1a1c03329dbdcdefabd8b6478ddaa7.

Uses the original unfused checkpoint names, PyTorch SDPA (the HF default) and stateless full
sequence convolution. No FreeToken operations or cache logic enter the oracle.
"""
import torch
import torch.nn.functional as F


def inv_freq(dim, base, factor):
    angles = int(dim * factor) // 2
    return torch.cat((1 / base ** (torch.arange(0, 2 * angles, 2).float() / dim),
                      torch.zeros(dim // 2 - angles)))


class Reference:
    def __init__(self, config, weights, dtype=torch.bfloat16):
        self.c = config
        self.w = {k: v.to(device="cuda", dtype=dtype) for k, v in weights.items()}

    def __call__(self, tokens):
        c, w = self.c, self.w
        x = F.embedding(torch.tensor(tokens, device="cuda"), w['model.embed_tokens.weight'])

        def linear(x, name):
            return F.linear(x, w[name + '.weight'])

        def norm(x, name):
            xf = x.float()
            return (xf * torch.rsqrt(xf.square().mean(-1, keepdim=True) + c['norm_eps'])).to(x.dtype) * w[name + '.weight']

        def rope(x, kind):
            params = c['rope_parameters'][kind]
            freqs = torch.arange(len(tokens), device=x.device)[:, None] * inv_freq(
                c['head_dim'], params['rope_theta'], params.get('partial_rotary_factor', 1),
            ).to(x.device)[None, :]
            emb = torch.cat((freqs, freqs), -1)[:, None, :]
            a, b = x.float().chunk(2, -1)
            return (x.float() * emb.cos().to(x.dtype).float() + torch.cat((-b, a), -1) * emb.sin().to(x.dtype).float()).to(x.dtype)

        for i, kind in enumerate(c['layer_types']):
            p = f'model.layers.{i}'
            h = norm(x, p + '.operator_norm')
            if kind == 'conv':
                b, gate, value = linear(h, p + '.conv.in_proj').chunk(3, -1)
                z = (b * value).T[None]
                z = F.conv1d(z, w[p + '.conv.conv.weight'], padding=6, groups=c['hidden_size'])[0, :, :len(tokens)].T
                h = linear(gate * z, p + '.conv.out_proj')
            else:
                a = p + '.self_attn'
                q = rope(norm(linear(h, a + '.q_proj').view(-1, c['num_attention_heads'], c['head_dim']), a + '.q_norm'), kind)
                k = rope(norm(linear(h, a + '.k_proj').view(-1, c['num_key_value_heads'], c['head_dim']), a + '.k_norm'), kind)
                v = linear(h, a + '.v_proj').view(-1, c['num_key_value_heads'], c['head_dim'])
                k = k.repeat_interleave(c['num_attention_heads'] // c['num_key_value_heads'], 1)
                v = v.repeat_interleave(c['num_attention_heads'] // c['num_key_value_heads'], 1)
                pos = torch.arange(len(tokens), device=x.device)
                mask = pos[None, :] <= pos[:, None]
                if kind == 'sliding_attention':
                    mask &= pos[None, :] > pos[:, None] - c['sliding_window']
                out = F.scaled_dot_product_attention(
                    q.transpose(0, 1)[None], k.transpose(0, 1)[None], v.transpose(0, 1)[None],
                    attn_mask=mask, scale=c['head_dim'] ** -0.5,
                )[0].transpose(0, 1)
                out = out * linear(h, a + '.gate_proj').sigmoid()[..., None]
                h = linear(out.flatten(1), a + '.o_proj')
            if c['use_sandwich_norm']:
                h = norm(h, p + '.post_operator_norm')
            x = x + h
            h = norm(x, p + '.ffn_norm')
            h = linear(F.silu(linear(h, p + '.feed_forward.w1')) * linear(h, p + '.feed_forward.w3'), p + '.feed_forward.w2')
            if c['use_sandwich_norm']:
                h = norm(h, p + '.post_ffn_norm')
            x = x + h
        return F.linear(norm(x, 'model.embedding_norm'), w['model.embed_tokens.weight']).float()
