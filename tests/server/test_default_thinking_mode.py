"""Unit tests for the --default-thinking-mode server flag merge logic."""
from __future__ import annotations

from freetoken.server.anthropic_api import convert_anthropic_to_genspec
from freetoken.server.anthropic_models import AnthropicMessagesRequest
from freetoken.server.api_models import ChatCompletionRequest
from freetoken.server.model_meta import thinking_toggle_kwargs
from freetoken.server.openai_api import apply_default_thinking_mode, chat_request_to_genspec
from freetoken.server.responses_api import ResponsesRequest, convert_responses_to_genspec

OFF = thinking_toggle_kwargs(False)
ON = thinking_toggle_kwargs(True)


def test_auto_is_noop():
    assert apply_default_thinking_mode(None, "auto") is None
    assert apply_default_thinking_mode({"enable_thinking": True}, "auto") == {
        "enable_thinking": True
    }
    assert apply_default_thinking_mode(None, None) is None


def test_chat_fills_unset_kwargs():
    assert apply_default_thinking_mode(None, "chat") == OFF
    assert apply_default_thinking_mode({}, "chat") == OFF
    assert apply_default_thinking_mode({"other": 1}, "chat") == {**OFF, "other": 1}


def test_thinking_fills_unset_kwargs():
    assert apply_default_thinking_mode(None, "thinking") == ON
    assert apply_default_thinking_mode({}, "thinking") == ON


def test_explicit_request_value_wins():
    # Explicit per-request values override the server default, both directions.
    assert apply_default_thinking_mode({"enable_thinking": True}, "chat") == {
        "enable_thinking": True
    }
    assert apply_default_thinking_mode({"enable_thinking": False}, "thinking") == {
        "enable_thinking": False
    }
    assert apply_default_thinking_mode({"thinking": False}, "chat") == {"thinking": False}
    assert apply_default_thinking_mode({"thinking_mode": "thinking"}, "chat") == {
        "thinking_mode": "thinking"
    }
    assert apply_default_thinking_mode({"reasoning_effort": "high"}, "chat") == {
        "reasoning_effort": "high"
    }


def test_original_dict_not_mutated():
    original = {"other": 1}
    result = apply_default_thinking_mode(original, "chat")
    assert result == {**OFF, "other": 1}
    assert original == {"other": 1}


def test_unknown_mode_is_noop():
    assert apply_default_thinking_mode({"other": 1}, "bogus") == {"other": 1}


def _chat(**fields):
    return ChatCompletionRequest.model_validate(
        {"model": "m", "messages": [{"role": "user", "content": "hi"}], **fields}
    )


def test_chat_completion_protocol_toggles_beat_the_server_default():
    # The default is folded in after reasoning_effort / thinking.type, so a request that
    # asks for thinking through the protocol still gets it under --default-thinking-mode chat.
    spec = chat_request_to_genspec(_chat(reasoning_effort="high"), {}, default_thinking_mode="chat")
    assert spec.chat_template_kwargs["enable_thinking"] is True
    assert spec.chat_template_kwargs["reasoning_effort"] == "high"
    spec = chat_request_to_genspec(
        _chat(thinking={"type": "enabled"}), {}, default_thinking_mode="chat"
    )
    assert spec.chat_template_kwargs["enable_thinking"] is True
    spec = chat_request_to_genspec(
        _chat(reasoning_effort="none"), {}, default_thinking_mode="thinking"
    )
    assert spec.chat_template_kwargs["enable_thinking"] is False


def test_chat_completion_default_fills_a_bare_request():
    assert chat_request_to_genspec(_chat(), {}, default_thinking_mode="chat").chat_template_kwargs == OFF
    assert chat_request_to_genspec(_chat(), {}, default_thinking_mode="auto").chat_template_kwargs == {}


def test_responses_reasoning_effort_beats_the_server_default():
    req = ResponsesRequest.model_validate(
        {"model": "m", "input": "hi", "reasoning": {"effort": "high"}}
    )
    ctk = convert_responses_to_genspec(req, {}, default_thinking_mode="chat").chat_template_kwargs
    assert ctk["enable_thinking"] is True
    bare = ResponsesRequest.model_validate({"model": "m", "input": "hi"})
    assert convert_responses_to_genspec(bare, {}, default_thinking_mode="chat").chat_template_kwargs == OFF


def test_anthropic_thinking_block_beats_the_server_default():
    req = AnthropicMessagesRequest.model_validate(
        {
            "model": "m",
            "max_tokens": 64,
            "messages": [{"role": "user", "content": "hi"}],
            "thinking": {"type": "enabled", "budget_tokens": 1024},
        }
    )
    ctk = convert_anthropic_to_genspec(req, {}, default_thinking_mode="chat").chat_template_kwargs
    assert ctk["enable_thinking"] is True
