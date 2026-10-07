from __future__ import annotations

from unittest.mock import patch

from freetoken.server.args import ServerArgs, parse_args


class _Config:
    def to_dict(self) -> dict:
        return {"architectures": ["LlamaForCausalLM"], "torch_dtype": "bfloat16"}


def _parse(*extra):
    with patch("freetoken.utils.cached_load_hf_config", lambda _path: _Config()):
        args, _run_shell = parse_args(["--model", "/models/anon", *extra])
    return args


def test_the_default_prefill_length_is_not_marked_explicit():
    args = _parse()
    assert args.max_extend_tokens == ServerArgs.max_extend_tokens
    assert args.max_extend_tokens_explicit is False


def test_a_given_prefill_length_is_marked_explicit_under_either_spelling():
    for flag in ("--max-prefill-length", "--max-extend-length"):
        args = _parse(flag, str(ServerArgs.max_extend_tokens))  # even when equal to the default
        assert args.max_extend_tokens == ServerArgs.max_extend_tokens
        assert args.max_extend_tokens_explicit is True
