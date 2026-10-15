"""Streaming OpenAI chat client (stdlib only) that measures TTFT and decode speed."""
import json
import socket
import time
import urllib.error
import urllib.request

# How a model's reasoning block opens and closes in raw text, to cut a reasoning phase short.
# models.toml picks one per model with think_format (default "think").
THINK_FORMATS = {
    "think": ("<think>\n", "\n</think>\n\n"),  # Qwen3.x, GLM
    "harmony": ("<|channel|>analysis<|message|>", "<|end|><|start|>assistant<|channel|>final<|message|>"),  # gpt-oss
    "gemma4": ("<|channel>thought\n", "<channel|>"),
}
STOP_THINKING = "\n\nTime is up. I must stop thinking now and write the final answer immediately."


def get_json(url: str, api_key: str | None = None, timeout: float = 10) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"} if api_key else {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def post_json(url: str, body: dict, api_key: str | None = None, timeout: float = 60) -> dict:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    with urllib.request.urlopen(urllib.request.Request(url, json.dumps(body).encode(), headers), timeout=timeout) as r:
        return json.load(r)


def _stream(url: str, body: dict, api_key: str | None, think_limit: float | None, write_limit: float | None) -> dict:
    """Streams one request. It closes the connection (ft serve then aborts the request) when the model still
    only reasons after think_limit seconds (finish_reason "think") or writes its answer for longer than
    write_limit seconds, counted from the answer's first token (finish_reason "time")."""
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(url, json.dumps(body).encode(), headers)
    content, reasoning, usage, finish = [], [], None, None
    has_content = has_reasoning = False
    chunks = 0
    t0 = time.perf_counter()
    t_first = t_write = None
    # also bounds a request that never streams (stuck prefill, a model that neither reasons nor writes)
    total = (think_limit or 0) + write_limit if write_limit else None
    try:
        with urllib.request.urlopen(req, timeout=total or 3600) as r:
            for raw in r:
                now = time.perf_counter()
                if write_limit and (now - t_write > write_limit if t_write else now - t0 > total):
                    finish = "time"
                    break
                if think_limit and now - t0 > think_limit and has_reasoning and not has_content:
                    finish = "think"
                    break
                line = raw.decode().strip()
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                ev = json.loads(data)
                if ev.get("usage"):
                    usage = ev["usage"]
                for ch in ev.get("choices") or []:
                    d = ch.get("delta") or {}
                    piece_r = d.get("reasoning_content") or d.get("reasoning") or ""
                    piece_c = d.get("content") or ch.get("text") or ""
                    if piece_r or piece_c:
                        chunks += 1
                        if t_first is None:
                            t_first = time.perf_counter()
                    has_reasoning |= bool(piece_r)
                    if piece_c.strip() and not has_content:
                        has_content, t_write = True, time.perf_counter()
                    reasoning.append(piece_r)
                    content.append(piece_c)
                    finish = ch.get("finish_reason") or finish
    except (TimeoutError, socket.timeout):
        finish = "time"
    t_end = time.perf_counter()
    t_first = t_first or t_end
    usage = usage or {}
    # An aborted stream sends no usage; one streamed chunk is about one token.
    out_tok = usage.get("completion_tokens") or chunks
    decode_s = t_end - t_first
    return {
        "content": "".join(content),
        "reasoning": "".join(reasoning),
        "finish_reason": finish,
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": out_tok,
        "ttft_s": round(t_first - t0, 3),
        "total_s": round(t_end - t0, 3),
        "decode_s": round(decode_s, 3),
        # The first token arrives with the prefill, so decode speed counts the remaining ones.
        "decode_tps": round((out_tok - 1) / decode_s, 1) if out_tok > 1 and decode_s > 0 else None,
        "prefill_tps": round(usage["prompt_tokens"] / (t_first - t0), 1) if usage.get("prompt_tokens") and t_first > t0 else None,
    }


def chat(base_url: str, model: str, messages: list, max_tokens: int, api_key: str | None = None,
         temperature: float = 0.0, extra: dict | None = None, think_limit: float | None = None,
         write_limit: float | None = None) -> dict:
    body = {
        "model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature,
        "stream": True, "stream_options": {"include_usage": True}, **(extra or {}),
    }
    return _stream(base_url.rstrip("/") + "/chat/completions", body, api_key, think_limit, write_limit)


def _token_ids(base: str, body: dict, api_key: str | None) -> list[int]:
    return post_json(base + "/tokenize", body, api_key)["token_ids"]


def ask(base_url: str, model: str, messages: list, *, ctx: int | None, max_tokens: int | None = None,
        api_key: str | None = None, extra: dict | None = None, think_limit: float | None = None,
        write_limit: float | None = None, think_format: str = "think") -> dict:
    """One answer: at most think_limit seconds of reasoning, then write_limit seconds for the answer. A model
    still reasoning at think_limit gets its reasoning closed with STOP_THINKING and writes the answer on
    /v1/completions (the radix cache keeps the prefix, so nothing is prefilled twice); the result then has
    think_stopped=True.
    Without max_tokens the answer may fill the free context."""
    base = base_url.rstrip("/")
    try:
        n_prompt = post_json(base + "/tokenize", {"messages": messages, **(extra or {})}, api_key)["tokens"]
    except (urllib.error.URLError, KeyError, ValueError):
        n_prompt = len(json.dumps(messages, ensure_ascii=False)) // 3
    budget = max(256, ctx - n_prompt - 64) if ctx else 32768
    mt = min(max_tokens, budget) if max_tokens else budget
    # Token ids carry no image data, so a prompt with images cannot be continued that way.
    images = any(isinstance(m["content"], list) for m in messages)
    r = chat(base_url, model, messages, mt, api_key=api_key, extra=extra,
             think_limit=None if images else think_limit, write_limit=write_limit)
    r["think_stopped"] = False
    if r["finish_reason"] != "think":
        return r
    opener, closer = THINK_FORMATS[think_format]
    prompt = _token_ids(base, {"messages": messages, **(extra or {})}, api_key)
    open_ids = _token_ids(base, {"input": opener, "add_special_tokens": False}, api_key)
    # Qwen3.6/3.8 templates already open the block in the generation prompt, others leave it to the model.
    if open_ids[0] not in prompt[-3:]:
        prompt += open_ids
    prompt += _token_ids(base, {"input": r["reasoning"].rstrip() + STOP_THINKING + closer,
                                "add_special_tokens": False}, api_key)
    body = {"model": model, "prompt": prompt, "max_tokens": max(256, mt - r["completion_tokens"]), "temperature": 0.0,
            "stream": True, "stream_options": {"include_usage": True}}
    r2 = _stream(base + "/completions", body, api_key, None, write_limit)
    tok = r["completion_tokens"] + r2["completion_tokens"]
    dec = r["decode_s"] + r2["decode_s"]
    r.update(content=r2["content"], finish_reason=r2["finish_reason"], completion_tokens=tok,
             total_s=round(r["total_s"] + r2["total_s"], 3), decode_s=round(dec, 3),
             decode_tps=round((tok - 2) / dec, 1) if dec > 0 and tok > 2 else None, think_stopped=True)
    return r
