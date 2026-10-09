"""Pipeline parallelism (--pp-size) pieces that need no GPU: the layer split, the per-stage model
config, the per-stage model build, the checkpoint filters and the scheduler's in-flight rule."""

from __future__ import annotations

import contextlib
import os
from types import SimpleNamespace
from unittest.mock import patch

import pytest
import torch

from freetoken.distributed import DistributedInfo
from freetoken.distributed import pipeline as pp
from freetoken.scheduler.decode import DecodeManager

FLASH_NEXT = "RadixArk/Qwen3.8-Flash-Next-NVFP4"
QWEN36 = "RedHatAI/Qwen3.6-35B-A3B-NVFP4"


def _cached(model: str) -> bool:
    hub = os.path.expanduser("~/.cache/huggingface/hub")
    return os.path.isdir(os.path.join(hub, "models--" + model.replace("/", "--")))


# --------------------------------------------------------------------------- #
# layer split
# --------------------------------------------------------------------------- #
def test_even_split_gives_the_remainder_to_the_earlier_stages():
    assert pp.split_layers(48, 3) == [(0, 16), (16, 32), (32, 48)]
    assert pp.split_layers(40, 3) == [(0, 14), (14, 27), (27, 40)]
    assert pp.split_layers(5, 1) == [(0, 5)]


def test_explicit_split():
    assert pp.split_layers(48, 3, "20,16,12") == [(0, 20), (20, 36), (36, 48)]


@pytest.mark.parametrize("spec", ["16,16", "16,16,15", "24,24,0", "a,b,c"])
def test_bad_split_is_rejected(spec):
    with pytest.raises(ValueError):
        pp.split_layers(48, 3, spec)


def test_more_stages_than_layers_is_rejected():
    with pytest.raises(ValueError):
        pp.split_layers(2, 3)


# --------------------------------------------------------------------------- #
# checkpoint filter
# --------------------------------------------------------------------------- #
@contextlib.contextmanager
def _stage(rank: int, size: int, start: int, end: int, num_layers: int):
    pp.set_pipeline_stage(pp.PipelineStage(rank, size, start, end, num_layers))
    try:
        yield
    finally:
        pp.set_pipeline_stage(None)


def test_every_tensor_is_kept_without_stages():
    assert pp.keeps_weight("model.layers.40.mlp.gate.weight")
    assert pp.keeps_weight("lm_head.weight")


def test_middle_stage_keeps_its_layers_only():
    with _stage(1, 3, 16, 32, 48):
        assert pp.keeps_weight("model.layers.16.self_attn.qkv_proj.weight")
        assert pp.keeps_weight("model.layers.31.mlp.gate.weight")
        assert not pp.keeps_weight("model.layers.15.mlp.gate.weight")
        assert not pp.keeps_weight("model.layers.32.mlp.gate.weight")
        assert not pp.keeps_weight("model.embed_tokens.weight")
        assert not pp.keeps_weight("lm_head.weight")
        assert not pp.keeps_weight("model.norm.weight")


def test_first_and_last_stage_keep_head_and_tail():
    with _stage(0, 2, 0, 24, 48):
        assert pp.keeps_weight("model.embed_tokens.weight")
        assert not pp.keeps_weight("lm_head.weight")
    with _stage(1, 2, 24, 48, 48):
        assert not pp.keeps_weight("model.embed_tokens.weight")
        assert pp.keeps_weight("lm_head.weight")
        assert pp.keeps_weight("model.hyper_connection_mixer.hc_norm.weight", tail=("model.hyper_connection_mixer.",))


# --------------------------------------------------------------------------- #
# decode scheduling: requests in flight wait, a batch takes its share
# --------------------------------------------------------------------------- #
class _Req:
    can_decode = True

    def __init__(self, uid: int):
        self.uid = uid


def _req(uid: int):
    return _Req(uid)


def test_decode_batch_skips_requests_in_flight_and_caps_its_size():
    reqs = [_req(i) for i in range(5)]
    dm = DecodeManager(page_size=1, running_reqs=set(reqs))
    assert [r.uid for r in dm.schedule_next_batch().reqs] == [0, 1, 2, 3, 4]
    batch = dm.schedule_next_batch(exclude={reqs[0], reqs[2]}, max_size=2)
    assert [r.uid for r in batch.reqs] == [1, 3]
    assert dm.schedule_next_batch(exclude=set(reqs)) is None


def _pipeline_scheduler(depth: int, reqs):
    """A Scheduler shell that runs pipeline_loop over a real DecodeManager and records what it
    launches and drains, without an engine."""
    from freetoken.scheduler.scheduler import Scheduler

    s = Scheduler.__new__(Scheduler)
    s._pp_depth = depth
    s._pp_inflight = __import__("collections").deque()
    s._pending_rebuild = None
    s._pending_abort_acks = set()
    s.prefill_budget = 1024
    s.prefill_manager = SimpleNamespace(runnable=False, schedule_next_batch=lambda budget: None)
    s.decode_manager = DecodeManager(page_size=1, running_reqs=set(reqs))
    s.receive_msg = lambda blocking: []
    no_op = SimpleNamespace(wait_stream=lambda other: None)
    s.stream = no_op
    s.engine = SimpleNamespace(stream=no_op)
    s.engine_stream_ctx = contextlib.nullcontext()
    s._restore_linear_states = lambda batch: None
    s._prepare_batch = lambda batch: SimpleNamespace(batch=batch)
    s.send_result = lambda messages: None
    s.launched, s.drained = [], []

    def forward(fi):
        s.launched.append([r.uid for r in fi.batch.reqs])
        return SimpleNamespace()

    s._forward = forward
    s._pp_collect = lambda data: data
    s._process_last_data = lambda data: s.drained.append([r.uid for r in data[0].batch.reqs])
    return s


def test_pipeline_loop_runs_one_request_per_stage():
    reqs = [_req(i) for i in range(3)]
    s = _pipeline_scheduler(3, reqs)
    for _ in range(9):
        s.pipeline_loop()
    # three single-request batches fill the pipeline; then each drain frees one request,
    # which goes straight back in behind the other two
    assert s.launched[:6] == [[0], [1], [2], [0], [1], [2]]
    assert s.drained[:3] == [[0], [1], [2]]
    for i, uids in enumerate(s.launched):
        # a request is never launched again before its previous batch was drained
        earlier = [b for b in s.launched[:i] if uids[0] in b]
        assert s.drained.count(uids) >= len(earlier)


def test_pipeline_loop_with_one_request_waits_for_each_token():
    s = _pipeline_scheduler(3, [_req(7)])
    for _ in range(4):
        s.pipeline_loop()
    assert s.launched == [[7], [7]]
    assert s.drained == [[7], [7]]


def test_pipeline_loop_splits_many_requests_into_stage_shares():
    reqs = [_req(i) for i in range(6)]
    s = _pipeline_scheduler(3, reqs)
    for _ in range(3):
        s.pipeline_loop()
    assert s.launched == [[0, 1], [2, 3], [4, 5]]


# --------------------------------------------------------------------------- #
# per-stage model config and model build (real checkpoint configs, no weights)
# --------------------------------------------------------------------------- #
@pytest.fixture(autouse=True)
def _single_tp_rank():
    from freetoken.distributed import set_tp_info, try_get_tp_info

    if try_get_tp_info() is None:
        set_tp_info(rank=0, size=1)


def _stage_config(model: str, rank: int, size: int):
    from freetoken.engine.config import EngineConfig
    from freetoken.mm.config import ENCODER_KINDS, MultimodalConfig

    cfg = EngineConfig(
        model_path=model, tp_info=DistributedInfo(0, 1), dtype=torch.bfloat16,
        pp_info=DistributedInfo(rank, size), moe_strategy="offload",
        mm=MultimodalConfig(disabled_encoders=frozenset(ENCODER_KINDS)),  # stages are text-only
    )
    mc = cfg.model_config
    object.__setattr__(mc, "moe_strategy", "offload")
    return mc


@pytest.mark.parametrize(("model", "size"), [(FLASH_NEXT, 3), (QWEN36, 2), (QWEN36, 3)])
def test_stage_configs_cover_the_model_once(model, size):
    if not _cached(model):
        pytest.skip(f"{model} not in the HF cache")
    stages = [_stage_config(model, r, size) for r in range(size)]
    num_layers = stages[0].num_layers
    owned = [lid for mc in stages for lid in range(num_layers) if mc.owns_layer(lid)]
    assert owned == list(range(num_layers))
    assert sum(mc.num_moe_layers for mc in stages) == num_layers
    offset = 0
    for mc in stages:
        assert mc.moe_bank_offset == offset
        offset += mc.num_moe_layers
        start, end = mc.pp_layers
        for group in mc.attention_groups:
            assert group.layer_ids and all(start <= i < end for i in group.layer_ids)
        for spec in mc.kv_cache_group_specs():
            if spec.num_index_layers:
                assert spec.num_index_layers == spec.num_layers
    assert stages[0].pp_is_first and not stages[0].pp_is_last
    assert stages[-1].pp_is_last and not stages[-1].pp_is_first


@pytest.mark.parametrize(("model", "size"), [(FLASH_NEXT, 3), (QWEN36, 2)])
def test_stage_models_partition_the_state_dict(model, size):
    if not _cached(model):
        pytest.skip(f"{model} not in the HF cache")
    from freetoken.layers.moe import iter_moe_layers
    from freetoken.layers.rotary import set_rope_device
    from freetoken.models import create_model
    from freetoken.utils import torch_dtype

    set_rope_device(torch.device("cpu"))
    seen: dict[str, int] = {}
    for rank in range(size):
        mc = _stage_config(model, rank, size)
        with torch.device("meta"), torch_dtype(torch.bfloat16):
            m = create_model(mc)
        assert m.supports_pipeline_parallel
        keys = m.state_dict().keys()
        for k in keys:
            seen[k] = seen.get(k, 0) + 1
        assert any(k.startswith("model.embed_tokens.") for k in keys) == (rank == 0)
        assert any(k.startswith("lm_head.") for k in keys) == (rank == size - 1)
        # the offload cache numbers its layers from 0 on every stage
        assert [layer.layer_id for layer in iter_moe_layers(m)] == list(range(mc.num_moe_layers))
    assert max(seen.values()) == 1, [k for k, n in seen.items() if n > 1][:5]


@pytest.mark.parametrize(("model", "size"), [(FLASH_NEXT, 3), (QWEN36, 2)])
def test_each_expert_tensor_goes_to_exactly_one_stage(model, size):
    if not _cached(model):
        pytest.skip(f"{model} not in the HF cache")
    import freetoken.moe.expert_pieces as ep
    from freetoken.models import nvfp4_banks

    counts: dict[str, int] = {}
    for rank in range(size):
        mc = _stage_config(model, rank, size)
        captured = {}

        def fake(tensors, locate, **kw):
            captured["wanted"] = locate.__self__
            return iter(())

        with patch.object(ep, "per_expert_pieces", fake):
            # builds the name -> (bank layer, expert, role) map from the shard index; reads no tensor
            nvfp4_banks.iter_nvfp4_expert_pieces(model, mc, ep.nvfp4_expert_spec_of(model, mc))
        wanted = captured["wanted"]
        assert sorted({bank for bank, _, _ in wanted.values()}) == list(range(mc.num_moe_layers))
        start, end = mc.pp_layers
        assert all(start <= int(k.split("layers.")[1].split(".")[0]) < end for k in wanted)
        for k in wanted:
            counts[k] = counts.get(k, 0) + 1
    full = _stage_config(model, 0, 1)
    assert len(counts) == full.num_moe_layers * full.num_experts * 9
    assert set(counts.values()) == {1}


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
class _HfConfig:
    def to_dict(self) -> dict:
        return {"architectures": ["LlamaForCausalLM"], "torch_dtype": "bfloat16"}


def _parse(*extra):
    from freetoken.server.args import parse_args

    with patch("freetoken.utils.cached_load_hf_config", lambda _path: _HfConfig()):
        return parse_args(["--model", "/models/anon", *extra])[0]


def test_pp_size_reaches_the_server_args():
    args = _parse("--pp-size", "3", "--pp-layer-split", "16,16,16", "--gpu", "0,1,2")
    assert args.pp_info == DistributedInfo(0, 3)
    assert args.pp_layer_split == "16,16,16"
    assert args.tp_info.size == 1


@pytest.mark.parametrize("extra", [
    ("--pp-size", "2", "--tp-size", "2"),
    ("--pp-layer-split", "8,8"),
    ("--pp-size", "3", "--gpu", "0,1"),
    ("--pp-size", "0"),
])
def test_bad_pp_flags_are_rejected(extra):
    with pytest.raises(SystemExit):
        _parse(*extra)


def test_world_rank_drives_primary():
    info = DistributedInfo(0, 1, world_rank=2, world_size=3)
    assert info.rank == 0 and info.size == 1
    assert not info.is_primary()
    assert DistributedInfo(0, 1).world_size == 1 and DistributedInfo(0, 1).is_primary()
