import torch

from freetoken.models.glm4_moe.weight import _iter_resident_linear


class _Reader:
    def __init__(self, tensors):
        self._t = tensors

    def has(self, name):
        return name in self._t

    def get(self, name):
        return self._t[name]


def test_ignored_projection_loads_bf16():
    # gesong2077/GLM-4.5-Air-NVFP4 lists the dense MLP and shared experts under `ignore`
    w = torch.randn(8, 16, dtype=torch.bfloat16)
    out = dict(_iter_resident_linear(_Reader({"m.gate_proj.weight": w}), "m.gate_proj"))
    assert list(out) == ["m.gate_proj.weight"]
    assert torch.equal(out["m.gate_proj.weight"], w)


def test_quantized_projection_loads_nvfp4():
    t = {
        "m.up_proj.weight": torch.zeros(8, 8, dtype=torch.uint8),
        "m.up_proj.weight_scale": torch.ones(8, 1).to(torch.float8_e4m3fn),
        "m.up_proj.weight_scale_2": torch.tensor([0.5]),
    }
    out = dict(_iter_resident_linear(_Reader(t), "m.up_proj"))
    assert set(out) == {"m.up_proj.weight", "m.up_proj.weight_scale", "m.up_proj.weight_global"}
    assert out["m.up_proj.weight_global"].shape == (8,)
