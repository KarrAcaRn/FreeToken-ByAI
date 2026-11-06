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
