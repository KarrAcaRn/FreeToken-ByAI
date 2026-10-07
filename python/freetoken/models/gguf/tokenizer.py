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

# GGUF architecture -> converter key of transformers < 5.19 (integrations.ggml); the
# integrations.gguf converter of 5.19+ takes the GGUF architecture as is.
_TOKENIZER_ARCH = {"gemma4": "gemma4_text"}


def _convert_gguf_tokenizer(arch: str, tok_dict: dict):
    """``tok_dict``: the ``tokenizer.ggml.*`` metadata with that prefix stripped."""
    try:
        from transformers.integrations.gguf import GGUF_TOKENIZER_MAPPING, convert_gguf_tokenizer
    except ImportError:
        from transformers.integrations.ggml import convert_gguf_tokenizer

        return convert_gguf_tokenizer(_TOKENIZER_ARCH.get(arch, arch), tok_dict)
    # 5.19+ reads transformers' own names for these keys (ggml.model -> tokenizer_type, ...)
    renamed = {
        name: tok_dict[key[len("ggml."):]]
        for key, name in GGUF_TOKENIZER_MAPPING["tokenizer"].items()
        if key.startswith("ggml.") and key[len("ggml."):] in tok_dict
    }
    return convert_gguf_tokenizer(arch, renamed)


def load_gguf_tokenizer(model_path: str):
    from transformers import PreTrainedTokenizerFast

    meta = load_gguf_metadata(model_path)
    arch = gguf_architecture(model_path)
    tok_dict: dict[str, Any] = {
        k[len("tokenizer.ggml.") :]: v
        for k, v in meta.items()
        if k.startswith("tokenizer.ggml.")
    }
    fast, _extra = _convert_gguf_tokenizer(arch, tok_dict)

    tokens = tok_dict["tokens"]

    def tok_for(id_key: str, default: str) -> str:
        tid = meta.get(f"tokenizer.ggml.{id_key}")
        return tokens[int(tid)] if tid is not None and int(tid) < len(tokens) else default

    # gemma4 chat turns end with <turn|>; prefer it as eos so chat generation halts
    # (the formal <eos> is also a stop id, see gguf_eos_token_ids).
    turn_end = "<turn|>" if "<turn|>" in tokens else None
    tokenizer = PreTrainedTokenizerFast(
        tokenizer_object=fast,
        bos_token=tok_for("bos_token_id", "<bos>"),
        eos_token=turn_end or tok_for("eos_token_id", "<eos>"),
        unk_token=tok_for("unknown_token_id", "<unk>"),
        pad_token=tok_for("padding_token_id", "<pad>"),
    )

    # GGUF user-defined tokens already exist in the model vocabulary with fixed
    # IDs, but transformers' GGUF conversion may not register them as AddedToken
    # entries. In that state convert_tokens_to_ids("<think>") returns the correct
    # vocabulary ID while encode("<think>") incorrectly splits it into ordinary
    # subword tokens. Restore their atomic-token behavior without marking them
    # special and without changing vocabulary size or IDs.
    token_types = tok_dict.get("token_type")
    if token_types is not None:
        added_tokens = []
        for token_id, (token, token_type) in enumerate(zip(tokens, token_types)):
            if int(token_type) != 4:
                continue
            if tokenizer.convert_tokens_to_ids(token) != token_id:
                continue
            if tokenizer.encode(token, add_special_tokens=False) == [token_id]:
                continue
            added_tokens.append(
                AddedToken(
                    token,
                    single_word=False,
                    lstrip=False,
                    rstrip=False,
                    normalized=False,
                    special=False,
                )
            )

        if added_tokens:
            vocab_size_before = len(tokenizer)
            tokenizer.add_tokens(added_tokens, special_tokens=False)
            if len(tokenizer) != vocab_size_before:
                raise RuntimeError(
                    "restoring GGUF user-defined tokens unexpectedly changed vocabulary size"
                )

    chat_template = meta.get("tokenizer.chat_template")
    if chat_template:
        tokenizer.chat_template = chat_template
    return tokenizer


def gguf_eos_token_ids(model_path: str, tokenizer) -> set[int]:
    """Stop ids for GGUF generation: the formal <eos> plus the chat turn end <turn|>."""
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
    for name in ("<eos>", "<turn|>"):
        try:
            ids.add(tokens.index(name))
        except ValueError:
            pass
    return ids


__all__ = ["load_gguf_tokenizer", "gguf_eos_token_ids"]
