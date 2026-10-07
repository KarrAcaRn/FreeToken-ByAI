"""DFlash decode-loop verify: every step stages its host-side inputs like a plain decode forward."""

from __future__ import annotations

from contextlib import contextmanager, nullcontext
from types import SimpleNamespace

import pytest
import torch

from freetoken.engine.engine import Engine
from freetoken.engine.sample import BatchSamplingArgs

VOCAB = 8


class _Model:
    """Greedy target that always predicts token 5; records each forward_host_ctx entry."""

    def __init__(self):
        self.host_ctx = []  # (use_graph, input token) per step
        self.inside = False

    @contextmanager
    def forward_host_ctx(self, batch, use_graph):
        self.host_ctx.append((use_graph, int(batch.input_ids[0])))
        self.inside = True
        yield
        self.inside = False

    def forward(self, return_hidden_layers=None):
        assert self.inside, "the eager step ran outside forward_host_ctx"
        return _logits(), [torch.zeros(1, 4)]


def _logits():
    logits = torch.full((1, VOCAB), -1.0)
    logits[0, 5] = 1.0
    return logits


class _GraphRunner:
    def __init__(self, model, use_graph):
        self.model, self.use_graph = model, use_graph

    def can_use_cuda_graph(self, batch):
        return self.use_graph

    def can_return_hidden_layers(self, ids):
        return True

    def replay(self, batch, return_hidden_layers=None):
        assert self.model.inside, "the graph replay ran outside forward_host_ctx"
        return _logits(), [torch.zeros(1, 4)]


def _engine(use_graph):
    model = _Model()
    eng = SimpleNamespace(
        dflash_worker=SimpleNamespace(target_layer_ids={0}),
        linear_state_pool=None,
        device=torch.device("cpu"),
        page_table=torch.arange(64).view(1, 64),
        attn_backend=SimpleNamespace(prepare_metadata=lambda batch: None),
        ctx=SimpleNamespace(forward_batch=lambda batch: nullcontext()),
        graph_runner=_GraphRunner(model, use_graph),
        model=model,
        sampler=SimpleNamespace(sample=lambda logits, args: logits.argmax(-1)),
    )
    return eng, model


@pytest.mark.parametrize("use_graph", [True, False])
def test_each_verify_step_runs_in_forward_host_ctx(use_graph):
    eng, model = _engine(use_graph)
    req = SimpleNamespace(table_idx=0, cached_len=10, device_len=11)
    batch = SimpleNamespace(reqs=[req])
    base = torch.tensor([3], dtype=torch.int32)
    drafts = torch.tensor([5, 5, 6], dtype=torch.int32)  # the third draft is rejected
    verify_input = torch.cat([base, drafts])
    out, accepted, _hidden, logits = Engine._dflash_verify_decode_loop(
        eng, batch, req, BatchSamplingArgs(temperatures=None), base, drafts, verify_input, 10, 0, None,
    )
    assert accepted == 2
    assert out.tolist() == [3, 5, 5, 5]
    assert logits.shape[0] == 3
    # one staged step per verified token, with the step's own token and the dispatch kind
    assert model.host_ctx == [(use_graph, 3), (use_graph, 5), (use_graph, 5)]
