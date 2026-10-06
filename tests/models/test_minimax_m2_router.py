import torch

from freetoken.distributed import set_tp_info, try_get_tp_info
from freetoken.engine.engine import _materialize_loaded_weight_state_dict
from freetoken.models.minimax_m2.config import parse_config
from freetoken.models.minimax_m2.moe import MiniMaxM2SparseMoeBlock
from freetoken.utils.hf import RawConfigShim
from freetoken.utils.torch_utils import torch_dtype


def test_selection_bias_stays_fp32_through_materialize():
    """The checkpoint keeps e_score_correction_bias fp32; the engine casts loaded weights to
    the declared dtype, so a bias declared in the model dtype (bf16) loses the small
    within-layer differences that decide the top-k (same bug as upstream #609)."""
    n_exp = 8
    hf = RawConfigShim({
        "architectures": ["MiniMaxM2ForCausalLM"], "model_type": "minimax_m2",
        "hidden_size": 64, "intermediate_size": 32, "num_hidden_layers": 1,
        "num_attention_heads": 2, "num_key_value_heads": 1, "head_dim": 32,
        "vocab_size": 128, "hidden_act": "silu", "rms_norm_eps": 1e-6,
        "max_position_embeddings": 4096, "num_local_experts": n_exp,
        "num_experts_per_tok": 2, "rotary_dim": 16,
    })
    if try_get_tp_info() is None:
        set_tp_info(rank=0, size=1)
    with torch.device("meta"), torch_dtype(torch.bfloat16):
        block = MiniMaxM2SparseMoeBlock(parse_config(hf), layer_id=0, prefix="model.layers.0.mlp")
    key = "model.layers.0.mlp.e_score_correction_bias"
    bias = torch.linspace(8.0, 8.06, n_exp)  # distinct in fp32, ties in bf16 (step 0.0625)
    state = block.state_dict(prefix="model.layers.0.mlp")
    loaded = _materialize_loaded_weight_state_dict({key: state[key]}, [(key, bias)],
                                                   device=torch.device("cpu"))[key]
    assert loaded.dtype == torch.float32
    assert torch.equal(loaded, bias)
