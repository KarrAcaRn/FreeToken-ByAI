"""Catch shifted windows/rope, reordered gates, and lost or cross-request conv state."""
import pytest
import torch

from .common import TinyEngine, checkpoint, requires_cuda
from .lfm3_hf_ref import Reference, inv_freq

# Six sandwich layers amplify bf16 rounding. Both HF SDPA and Triton accumulate
# attention in fp32 with bf16 weights and activations; 0.02 absolute + relative
# covers reduction order and the bf16 rounding against the additional fp32 oracle.
ATOL = RTOL = 0.02


def compare(got, want):
    torch.testing.assert_close(got.float(), want.float(), atol=ATOL, rtol=RTOL)


def tokens(n, seed=6):
    return torch.randint(3, 256, (n,), generator=torch.Generator().manual_seed(seed)).tolist()


def test_zero_tail_rope():
    from freetoken.layers.rotary import _rope_frequencies
    from freetoken.models.lfm3.config import parse_config
    from freetoken.utils.hf import RawConfigShim

    c = RawConfigShim(dict(
        layer_types=['conv', 'full_attention', 'sliding_attention'], num_hidden_layers=3,
        hidden_size=2048, head_dim=128, num_attention_heads=16, num_key_value_heads=4,
        conv_L_cache=7, sliding_window=256, max_position_embeddings=262144,
        rope_parameters={'full_attention': dict(rope_type='default', rope_theta=1e6, partial_rotary_factor=0.5),
                         'sliding_attention': dict(rope_type='default', rope_theta=1e4)},
        norm_eps=1e-5, vocab_size=128000, intermediate_size=7680,
        tie_word_embeddings=True, model_type='lfm3', architectures=['Lfm3ForCausalLM'],
        use_sandwich_norm=True,
    ))
    rope = parse_config(c).rotary_config
    actual, _ = _rope_frequencies(rope.head_dim, rope.rotary_dim, rope.base, rope.scaling)
    torch.testing.assert_close(actual, inv_freq(128, 1e6, 0.5), atol=0, rtol=0)


@requires_cuda
@pytest.mark.parametrize('graphs', [False, True])
@pytest.mark.parametrize('chunks', [None, [3, 4, 1, 1, 5, 3, 6]])
def test_prefill_chunks_decode_and_padding(tmp_path, graphs, chunks, reference_dtype):
    c, w = checkpoint(tmp_path)
    ref = Reference(c, w, dtype=reference_dtype)
    eng = TinyEngine(tmp_path, graphs, dtype=reference_dtype)
    ids = tokens(23)
    req = eng.request(ids)
    ends = [23] if chunks is None else torch.tensor(chunks).cumsum(0).tolist()
    try:
        for end in ends:
            req.device_len = end
            got = eng.forward([req])
            compare(got[0], ref(ids[:end])[-1])
            req.cached_len = end
        for token in tokens(5, seed=7):
            req.append_host(torch.tensor([token], dtype=torch.int32))
            req.complete_one()
            ids.append(token)
            compare(eng.forward([req], decode=True)[0], ref(ids)[-1])
    finally:
        eng.close()


@requires_cuda
@pytest.mark.parametrize('sandwich', [True, False])
def test_ragged_batch_and_reused_slot(tmp_path, sandwich, reference_dtype):
    c, w = checkpoint(tmp_path, sandwich)
    ref = Reference(c, w, dtype=reference_dtype)
    eng = TinyEngine(tmp_path, graphs=True, dtype=reference_dtype)
    seqs = [tokens(19), tokens(11, 8)]
    reqs = [eng.request(seq, row=i) for i, seq in enumerate(seqs)]
    try:
        compare(eng.forward(reqs), torch.stack([ref(seq)[-1] for seq in seqs]))
        for r in reqs:
            r.cached_len = r.device_len
        for step in range(4):
            for i, r in enumerate(reqs):
                token = 30 + step + i
                seqs[i].append(token)
                r.append_host(torch.tensor([token], dtype=torch.int32))
                r.complete_one()
            compare(eng.forward(reqs, decode=True), torch.stack([ref(seq)[-1] for seq in seqs]))
        slot = reqs[0].linear_slot_idx
        eng.cache.cache_req(reqs[0], finished=True)
        eng.cache.flush()
        new = eng.request(tokens(3, 22), row=0, cached=False)
        # Force reuse through the pool's public allocator, retaining other leases.
        while new.linear_slot_idx != slot:
            new.linear_slot_idx = eng.pool.alloc(1)[0]
        compare(eng.forward([new])[0], ref(tokens(3, 22))[-1])
    finally:
        eng.close()


@requires_cuda
def test_radix_restores_track_snapshot(tmp_path, reference_dtype):
    c, w = checkpoint(tmp_path)
    ref = Reference(c, w, dtype=reference_dtype)
    eng = TinyEngine(tmp_path, dtype=reference_dtype)
    ids = tokens(79)
    donor = eng.request(ids)
    try:
        compare(eng.forward([donor])[0], ref(ids)[-1])
        donor.cached_len = donor.device_len
        eng.cache.cache_req(donor, finished=False)
        fork = ids[:64] + tokens(9, 24)
        hit = eng.request(fork, row=1)
        assert hit.cached_len == 64
        warm = eng.forward([hit])
        cold = eng.request(fork, row=2, cached=False)
        compare(warm, eng.forward([cold]))
        compare(warm[0], ref(fork)[-1])
    finally:
        eng.close()


@pytest.mark.parametrize('kind', ['fp8', 'nvfp4'])
def test_quantized_mlp_dequantization(tmp_path, kind):
    """Keep w1/w3 order and distinct globals through fusion."""
    import json
    from safetensors.torch import save_file
    from freetoken.models.lfm3.weight import iter_weights
    from freetoken.models.register import checkpoint_quant_config, get_model_spec
    from freetoken.utils.hf import RawConfigShim

    c, _ = checkpoint(tmp_path)
    if kind == 'fp8':
        c['quantization_config'] = dict(quant_method='compressed-tensors',
            ignore=['re:.*conv.*', 're:.*self_attn.*', 'lm_head'],
            config_groups={'g': dict(targets=['Linear'], weights=dict(
                num_bits=8, type='float', strategy='block', block_structure=[128, 128]),
                input_activations=dict(num_bits=8, type='float', strategy='group', group_size=128, dynamic=True))})
    else:
        c['quantization_config'] = dict(quant_method='modelopt', quant_algo='NVFP4',
            ignore=['*conv*', '*self_attn*', 'lm_head'])
    (tmp_path / 'config.json').write_text(json.dumps(c))
    tensors, scales, reference = {}, {}, {}
    prefix = 'model.layers.0.feed_forward.'
    for index, (leaf, shape) in enumerate([('w1', (256, 128)), ('w3', (256, 128)), ('w2', (128, 256))], 1):
        name = prefix + leaf
        rows, cols = shape
        if kind == 'fp8':
            w = torch.arange(rows * cols).reshape(shape).remainder(9).sub(4).to(torch.float8_e4m3fn)
            s = torch.full((rows // 128, cols // 128), index / 16, dtype=torch.bfloat16)
            tensors[name + '.weight'] = w
            scales[name + '.weight_scale'] = s
            reference[leaf] = w.float() * s.float().repeat_interleave(128, 0).repeat_interleave(128, 1)
        else:
            # E2M1 nibbles 2 and 4 decode to 1 and 2, respectively.
            tensors[name + '.weight'] = torch.full((rows, cols // 2), 0x42, dtype=torch.uint8)
            scales[name + '.weight_scale'] = torch.full((rows, cols // 16), 0.5, dtype=torch.float8_e4m3fn)
            scales[name + '.weight_scale_2'] = torch.tensor(index / 4, dtype=torch.float32)
            scales[name + '.input_scale'] = torch.tensor(index / 8, dtype=torch.float32)
            reference[leaf] = torch.tensor([1., 2.]).repeat(rows, cols // 2) * 0.5 * (index / 4)
    save_file(tensors, str(tmp_path / 'model.safetensors'))
    save_file(scales, str(tmp_path / 'scales.safetensors'))
    quant = checkpoint_quant_config(str(tmp_path), RawConfigShim(**c), get_model_spec('Lfm3ForCausalLM'))
    assert quant.scheme_for('model.layers.0.conv.in_proj') is None
    assert quant.scheme_for('model.layers.1.self_attn.qkv_proj') is None
    assert quant.scheme_for(prefix + 'gate_up_proj') == quant.scheme_for(prefix + 'down_proj')
    loaded = dict(iter_weights(str(tmp_path), torch.device('cpu'), include_moe_experts=False, include_non_moe=True))
    for target, leaves in [('gate_up_proj', ['w1', 'w3']), ('down_proj', ['w2'])]:
        name = prefix + target
        w = loaded[name + '.weight']
        if kind == 'fp8':
            s = loaded[name + '.weight_scale_inv'].float()
            actual = w.float() * s.repeat_interleave(128, 0).repeat_interleave(128, 1)
        else:
            lut = torch.tensor([0., .5, 1., 1.5, 2., 3., 4., 6., -0., -.5, -1., -1.5, -2., -3., -4., -6.])
            decoded = lut[torch.stack((w & 15, w >> 4), dim=-1).long()].flatten(1)
            actual = decoded * loaded[name + '.weight_scale'].float().repeat_interleave(16, 1)
            actual *= loaded[name + '.weight_global'][:, None]
            assert loaded[name + '.weight_global'].dtype == torch.float32
            assert loaded[name + '.input_scale'].shape == ()
            assert loaded[name + '.input_scale'].item() == (2 / 8 if len(leaves) == 2 else 3 / 8)
        expected = torch.cat([reference[leaf] for leaf in leaves], dim=0)
        torch.testing.assert_close(actual, expected, atol=0, rtol=0)
