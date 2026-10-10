from __future__ import annotations


def test_gguf_user_defined_tokens_preserve_atomic_vocab_ids(monkeypatch):
    """GGUF USER_DEFINED tokens must remain atomic after GGUF -> HF conversion.

    Regression: Qwen3.6 GGUF contains <think> and </think> as USER_DEFINED
    vocabulary entries. transformers' GGUF conversion can preserve their vocab
    IDs while still allowing the pre-tokenizer to split their text into ordinary
    subword tokens. That changes the actual prompt token IDs seen by the model.
    """
    from tokenizers import Tokenizer
    from tokenizers.models import WordLevel
    from tokenizers.pre_tokenizers import Whitespace

    import freetoken.models.gguf.tokenizer as gguf_tokenizer

    tokens = [
        "<unk>",      # 0
        "<bos>",      # 1
        "<eos>",      # 2
        "<pad>",      # 3
        "<",          # 4
        "think",      # 5
        ">",          # 6
        "</",         # 7
        "<think>",    # 8  USER_DEFINED
        "</think>",   # 9  USER_DEFINED
        "hello",      # 10
    ]

    # GGUF TokenType:
    # NORMAL=1, UNKNOWN=2, CONTROL=3, USER_DEFINED=4.
    token_types = [
        2,
        3,
        3,
        3,
        1,
        1,
        1,
        1,
        4,
        4,
        1,
    ]

    metadata = {
        "tokenizer.ggml.tokens": tokens,
        "tokenizer.ggml.token_type": token_types,
        "tokenizer.ggml.unknown_token_id": 0,
        "tokenizer.ggml.bos_token_id": 1,
        "tokenizer.ggml.eos_token_id": 2,
        "tokenizer.ggml.padding_token_id": 3,
    }

    backend = Tokenizer(
        WordLevel(
            vocab={token: idx for idx, token in enumerate(tokens)},
            unk_token="<unk>",
        )
    )

    # This intentionally reproduces the bug: punctuation is pre-tokenized,
    # so the vocabulary entry <think> exists at ID 8 but plain encoding would
    # otherwise produce "<" + "think" + ">".
    backend.pre_tokenizer = Whitespace()

    monkeypatch.setattr(
        gguf_tokenizer,
        "load_gguf_metadata",
        lambda _path: metadata,
    )
    monkeypatch.setattr(
        gguf_tokenizer,
        "gguf_architecture",
        lambda _path: "synthetic",
    )

    def fake_convert_gguf_tokenizer(_arch, _tok_dict):
        return backend, {}

    monkeypatch.setattr(
        "transformers.integrations.ggml.convert_gguf_tokenizer",
        fake_convert_gguf_tokenizer,
    )

    tokenizer = gguf_tokenizer.load_gguf_tokenizer("synthetic.gguf")

    # Independent source of truth: these IDs come from the synthetic GGUF
    # vocabulary above, not from the implementation under test.
    assert tokenizer.convert_tokens_to_ids("<think>") == 8
    assert tokenizer.convert_tokens_to_ids("</think>") == 9

    assert tokenizer.encode(
        "<think>",
        add_special_tokens=False,
    ) == [8]

    assert tokenizer.encode(
        "</think>",
        add_special_tokens=False,
    ) == [9]

    # Restoring atomicity must not create new embedding/vocabulary IDs.
    assert len(tokenizer) == len(tokens)

    # USER_DEFINED does not mean HF "special token".
    assert "<think>" not in tokenizer.all_special_tokens
    assert "</think>" not in tokenizer.all_special_tokens


def test_qwen35moe_gguf_tokenizer_uses_the_qwen35_split_and_im_end(monkeypatch):
    """qwen35moe has no transformers converter key (qwen2 builds the BPE), splits combining
    marks with their letters like the source tokenizer.json, stops on <|im_end|>, and has no
    <unk> that a default could append to the vocab."""
    from tokenizers import Tokenizer
    from tokenizers.models import WordLevel
    from tokenizers.pre_tokenizers import Whitespace

    import freetoken.models.gguf.tokenizer as gguf_tokenizer

    tokens = ["<|endoftext|>", "<|im_start|>", "<|im_end|>", "a", "b"]
    metadata = {
        "tokenizer.ggml.tokens": tokens,
        "tokenizer.ggml.token_type": [3, 3, 3, 1, 1],
        "tokenizer.ggml.pre": "qwen35",
        "tokenizer.ggml.bos_token_id": 0,
        "tokenizer.ggml.eos_token_id": 2,
    }
    backend = Tokenizer(WordLevel(vocab={t: i for i, t in enumerate(tokens)}, unk_token="a"))
    backend.pre_tokenizer = Whitespace()
    seen = []
    monkeypatch.setattr(gguf_tokenizer, "load_gguf_metadata", lambda _path: metadata)
    monkeypatch.setattr(gguf_tokenizer, "gguf_architecture", lambda _path: "qwen35moe")
    monkeypatch.setattr(
        "transformers.integrations.ggml.convert_gguf_tokenizer",
        lambda arch, _tok: seen.append(arch) or (backend, {}),
    )

    tokenizer = gguf_tokenizer.load_gguf_tokenizer("qwen.gguf")

    assert seen == ["qwen2"]
    assert tokenizer.eos_token == "<|im_end|>" and tokenizer.unk_token is None
    assert len(tokenizer) == len(tokens)
    assert gguf_tokenizer.gguf_eos_token_ids("qwen.gguf", tokenizer) == {0, 2}
    # U+0915 U+093F: a letter and its combining vowel sign stay one pre-token (qwen2's split cuts them)
    pieces = [p for p, _ in backend.pre_tokenizer.pre_tokenize_str("\u0915\u093f x")]
    assert len(pieces) == 2
