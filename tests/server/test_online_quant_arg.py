"""next-speed serves bf16 linears as online fp8 by default; an explicit linear kernel or
--online-quant none opts out."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from freetoken.server.args import parse_args


class _Config:
    def to_dict(self) -> dict:
        return {"architectures": ["LlamaForCausalLM"], "torch_dtype": "bfloat16"}


def _quant_backend(argv: list[str]) -> str | None:
    with patch("freetoken.utils.cached_load_hf_config", lambda _path: _Config()):
        return parse_args(["--model", "/models/anon", *argv])[0].quant_backend


@pytest.mark.parametrize(
    "argv, expected",
    [
        ([], "linear.none=fp8"),
        (["--online-quant", "fp8"], "linear.none=fp8"),
        (["--online-quant", "none"], None),
        (["--quant-backend", "moe.nvfp4=triton"], "moe.nvfp4=triton,linear.none=fp8"),
        (["--quant-backend", "linear.none=torch"], "linear.none=torch"),
        (["--quant-backend", "linear=gemv"], "linear=gemv"),
        (["--quant-backend", "linear=gemv", "--online-quant", "fp8"], "linear=gemv,linear.none=fp8"),
    ],
)
def test_online_fp8_is_the_default(argv, expected):
    assert _quant_backend(argv) == expected
