"""Streaming OpenAI chat client (stdlib only) that measures TTFT and decode speed."""
import json
import time
import urllib.request


def get_json(url: str, api_key: str | None = None, timeout: float = 10) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"} if api_key else {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def chat(base_url: str, model: str, messages: list, max_tokens: int, api_key: str | None = None,
         temperature: float = 0.0, timeout: float = 3600, extra: dict | None = None) -> dict:
    body = {
        "model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature,
        "stream": True, "stream_options": {"include_usage": True}, **(extra or {}),
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(base_url.rstrip("/") + "/chat/completions", json.dumps(body).encode(), headers)
    content, reasoning, usage, finish = [], [], None, None
    chunks = 0
    t0 = time.perf_counter()
    t_first = None
    with urllib.request.urlopen(req, timeout=timeout) as r:
        for raw in r:
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
                piece_c = d.get("content") or ""
                if piece_r or piece_c:
                    chunks += 1
                    if t_first is None:
                        t_first = time.perf_counter()
                reasoning.append(piece_r)
                content.append(piece_c)
                finish = ch.get("finish_reason") or finish
    t_end = time.perf_counter()
    t_first = t_first or t_end
    usage = usage or {}
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
