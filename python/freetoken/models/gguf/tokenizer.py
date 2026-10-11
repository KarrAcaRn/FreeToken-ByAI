"""Build a HF fast tokenizer from a GGUF file's embedded tokenizer metadata.

transformers' ``AutoTokenizer.from_pretrained(gguf_file=...)`` first builds the HF
config, which the gemma4 strict dataclass rejects (per-layer ``num_key_value_heads``
array). So we call the GGUF->fast tokenizer converter directly on the
``tokenizer.ggml.*`` metadata, bypassing config entirely.
"""

from __future__ import annotations

from typing import Any

from tokenizers import AddedToken

from .reader import gguf_architecture, load_gguf_metadata

# GGUF architecture -> transformers GGUF tokenizer-converter key. qwen35moe / qwen3moe are
# GPT2-style BPEs that transformers has no converter key for; the qwen2 converter builds the same BPE.
_TOKENIZER_ARCH = {"gemma4": "gemma4_text", "qwen35moe": "qwen2", "qwen3moe": "qwen2", "qwen3": "qwen2"}

# Chat turn end first (it becomes eos, so chat generation halts there), then the formal
# document end; every name present in the vocab is a stop id.
_STOP_TOKENS = {
    "gemma4": ("<turn|>", "<eos>"),
    "qwen35moe": ("<|im_end|>", "<|endoftext|>"),
    "qwen3moe": ("<|im_end|>", "<|endoftext|>"),
    "qwen2": ("<|im_end|>", "<|endoftext|>"),
    "qwen3": ("<|im_end|>", "<|endoftext|>"),
    "llama": ("<|eot_id|>", "<|end_of_text|>", "</s>"),
}

# tokenizer.ggml.pre -> the split regex of the source tokenizer.json, where the qwen2
# converter's default differs. Qwen3.5 counts combining marks (\p{M}) as letters.
_PRE_SPLIT = {
    # Llama 3.x: digits split into runs of up to three
    "llama-bpe": (
        r"(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}{1,3}"
        r"| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+"
    ),
    "qwen35": (
        r"(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?[\p{L}\p{M}]+|\p{N}"
        r"| ?[^\s\p{L}\p{M}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+"
    ),
}


def load_gguf_tokenizer(model_path: str):
    from transformers import PreTrainedTokenizerFast
    from transformers.integrations.ggml import convert_gguf_tokenizer

    meta = load_gguf_metadata(model_path)
    arch = gguf_architecture(model_path)
    conv_arch = _TOKENIZER_ARCH.get(arch, arch)
    tok_dict: dict[str, Any] = {
        k[len("tokenizer.ggml.") :]: v
        for k, v in meta.items()
        if k.startswith("tokenizer.ggml.")
    }
    if arch == "llama" and tok_dict.get("model") == "gpt2":
        # Llama 3.x ships a byte-level BPE; transformers' llama converter builds SentencePiece
        conv_arch = "gpt2"
    fast, _extra = convert_gguf_tokenizer(conv_arch, tok_dict)
    split = _PRE_SPLIT.get(tok_dict.get("pre"))
    if split is not None:
        from tokenizers import Regex, pre_tokenizers

        fast.pre_tokenizer = pre_tokenizers.Sequence([
            pre_tokenizers.Split(Regex(split), behavior="isolated", invert=False),
            pre_tokenizers.ByteLevel(add_prefix_space=False, trim_offsets=False, use_regex=False),
        ])

    if arch == "llama" and conv_arch == "llama" and tok_dict.get("add_space_prefix", True):
        # SentencePiece llama vocabs (Mistral): prefix-space only the start of the text, not every
        # fragment after a special token, like llama.cpp and the tokenizer.json (Metaspace "first")
        from tokenizers import pre_tokenizers

        fast.normalizer = None
        fast.pre_tokenizer = pre_tokenizers.Metaspace(replacement="\u2581", prepend_scheme="first", split=False)

    tokens = tok_dict["tokens"]

    def tok_for(id_key: str, default: str) -> str | None:
        tid = meta.get(f"tokenizer.ggml.{id_key}")
        if tid is not None and int(tid) < len(tokens):
            return tokens[int(tid)]
        # a default absent from this vocab (Qwen has no <unk>) would be appended as a new token
        return default if default in tokens else None

    turn_end = next((t for t in _STOP_TOKENS.get(arch, ()) if t in tokens), None)
    tokenizer = PreTrainedTokenizerFast(
        tokenizer_object=fast,
        bos_token=tok_for("bos_token_id", "<bos>"),
        eos_token=turn_end or tok_for("eos_token_id", "<eos>"),
        unk_token=tok_for("unknown_token_id", "<unk>"),
        pad_token=tok_for("padding_token_id", "<pad>"),
    )
    if arch == "llama" and tok_dict.get("add_bos_token", True) and tokenizer.bos_token is not None:
        # llama.cpp prepends BOS for llama vocabs (Llama 3's <|begin_of_text|>, Mistral's <s>) like
        # their tokenizer.json; neither the BPE nor the SentencePiece converter does
        from tokenizers import processors

        bos, bos_id = tokenizer.bos_token, tokenizer.bos_token_id
        template = processors.TemplateProcessing(
            single=f"{bos} $A", pair=f"{bos} $A {bos}:1 $B:1", special_tokens=[(bos, bos_id)]
        )
        tokenizer.backend_tokenizer.post_processor = (
            processors.Sequence([processors.ByteLevel(trim_offsets=False), template]) if conv_arch == "gpt2" else template
        )

    # GGUF user-defined tokens already exist in the model vocabulary with fixed
    # IDs, but transformers' GGUF conversion may not register them as AddedToken
    # entries. In that state convert_tokens_to_ids("<think>") returns the correct
    # vocabulary ID while encode("<think>") incorrectly splits it into ordinary
    # subword tokens. Restore their atomic-token behavior without marking them
    # special and without changing vocabulary size or IDs.
    token_types = tok_dict.get("token_type")
    if token_types is not None:
        # Same for control tokens (type 3: Llama 3's <|start_header_id|>, ...), which stay special.
        added_tokens, control_tokens = [], []
        for token_id, (token, token_type) in enumerate(zip(tokens, token_types)):
            if int(token_type) not in (3, 4):
                continue
            if tokenizer.convert_tokens_to_ids(token) != token_id:
                continue
            if tokenizer.encode(token, add_special_tokens=False) == [token_id]:
                continue
            special = int(token_type) == 3
            (control_tokens if special else added_tokens).append(
                AddedToken(
                    token,
                    single_word=False,
                    lstrip=False,
                    rstrip=False,
                    normalized=False,
                    special=special,
                )
            )

        if added_tokens or control_tokens:
            vocab_size_before = len(tokenizer)
            tokenizer.add_tokens(added_tokens, special_tokens=False)
            tokenizer.add_tokens(control_tokens, special_tokens=True)
            if len(tokenizer) != vocab_size_before:
                raise RuntimeError(
                    "restoring GGUF user-defined tokens unexpectedly changed vocabulary size"
                )

    chat_template = meta.get("tokenizer.chat_template")
    if chat_template:
        tokenizer.chat_template = chat_template
    return tokenizer


def gguf_eos_token_ids(model_path: str, tokenizer) -> set[int]:
    """Stop ids for GGUF generation: the formal eos plus the architecture's chat turn end."""
    meta = load_gguf_metadata(model_path)
    tokens = meta["tokenizer.ggml.tokens"]
    ids: set[int] = set()
    if tokenizer.eos_token_id is not None:
        ids.add(int(tokenizer.eos_token_id))
    eid = meta.get("tokenizer.ggml.eos_token_id")
    if eid is not None:
        ids.add(int(eid))
    # Look the stop tokens up in the vocab directly (convert_tokens_to_ids would map an
    # absent name to <unk>, wrongly adding it as a stop id).
    for name in _STOP_TOKENS.get(gguf_architecture(model_path), ()):
        try:
            ids.add(tokens.index(name))
        except ValueError:
            pass
    return ids


__all__ = ["load_gguf_tokenizer", "gguf_eos_token_ids"]
