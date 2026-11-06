from __future__ import annotations

from typing import Iterator

import safetensors
import torch
from freetoken.distributed import get_tp_info
from freetoken.models.loader import MergeRule, iter_merged_tensors, iter_weight_files, read_safetensors_header, shard_tensor
from freetoken.models.register import checkpoint_quant_config, get_model_spec
from freetoken.utils import cached_load_hf_config
from tqdm import tqdm

from .config import parse_config

_MERGE_RULES = {
    ".q_proj": MergeRule(".qkv_proj", "q", ("q", "k", "v")),
    ".k_proj": MergeRule(".qkv_proj", "k", ("q", "k", "v")),
    ".v_proj": MergeRule(".qkv_proj", "v", ("q", "k", "v")),
    ".feed_forward.w1": MergeRule(".feed_forward.gate_up_proj", "gate", ("gate", "up")),
    ".feed_forward.w3": MergeRule(".feed_forward.gate_up_proj", "up", ("gate", "up")),
}


def iter_weights(
    model_path: str,
    device: torch.device,
    *,
    include_moe_experts: bool,
    include_non_moe: bool,
) -> Iterator[tuple[str, torch.Tensor]]:
    if not include_non_moe:
        return

    hf_config = cached_load_hf_config(model_path)
    config = parse_config(hf_config)
    quant = checkpoint_quant_config(model_path, hf_config, get_model_spec("Lfm3ForCausalLM"))
    tp_info = get_tp_info()
    input_scales: dict[str, list[torch.Tensor]] = {}
    files = iter_weight_files(model_path)
    shapes = {name: entry["shape"] for file in files
              for name, entry in read_safetensors_header(file).items() if name != "__metadata__"}

    def sharded_tensors() -> Iterator[tuple[str, torch.Tensor]]:
        for file in tqdm(
            files,
            desc="Loading weights",
            disable=not tp_info.is_primary(),
        ):
            with safetensors.safe_open(file, framework="pt", device=str(device)) as f:
                for raw_name in f.keys():
                    name = raw_name.replace(".feed_forward.w2.", ".feed_forward.down_proj.")
                    raw = f.get_tensor(raw_name)
                    module, _, suffix = raw_name.rpartition(".")
                    scheme = quant.scheme_for_name(module)
                    role = suffix
                    if scheme is not None:
                        for candidate, stored in quant.storage(scheme).items():
                            if suffix in stored.names:
                                role = candidate
                                name = name.rsplit(".", 1)[0] + "." + role
                                if stored.reciprocal:
                                    raw = raw.float().reciprocal()
                                break
                    if role == "input_scale":
                        for source, rule in _MERGE_RULES.items():
                            name = name.replace(source + ".", rule.fused_suffix + ".")
                        input_scales.setdefault(name, []).append(raw.float().reshape(()))
                        continue
                    if role == "weight_global":
                        rows = shapes[module + ".weight"][0]
                        raw = raw.float().reshape(()).expand(rows).contiguous()
                    shard_name = name.replace(".feed_forward.w1.", ".feed_forward.gate_proj.").replace(".feed_forward.w3.", ".feed_forward.up_proj.")
                    # Row-parallel globals scale output rows, not the sharded input axis.
                    if role == "weight_global" and any(p in shard_name for p in (".down_proj.", ".o_proj.")):
                        shard_name = "weight_global"
                    if ".conv.in_proj." in name:
                        tensor = torch.cat([part.chunk(tp_info.size, dim=0)[tp_info.rank]
                                            for part in raw.chunk(3, dim=0)], dim=0).contiguous()
                    elif ".conv.out_proj." in name:
                        tensor = raw.chunk(tp_info.size, dim=1)[tp_info.rank].contiguous()
                    elif ".conv.conv." in name:
                        tensor = raw.chunk(tp_info.size, dim=0)[tp_info.rank].contiguous()
                    else:
                        tensor = shard_tensor(
                            shard_name,
                            raw,
                            rank=tp_info.rank,
                            world_size=tp_info.size,
                            num_kv_heads=config.num_kv_heads,
                        )
                    del raw
                    yield name, tensor

    yield from iter_merged_tensors(
        sharded_tensors(),
        _MERGE_RULES,
        model_name="lfm3",
    )
    for name, scales in input_scales.items():
        yield name, torch.stack(scales).max()

__all__ = ["iter_weights"]
