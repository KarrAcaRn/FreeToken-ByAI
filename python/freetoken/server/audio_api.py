"""OpenAI /v1/audio/transcriptions + /v1/audio/translations, served by the --stt-model worker."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse, Response

from .openai_api import _maintenance_gate, create_error_response

RESPONSE_FORMATS = ("json", "text", "verbose_json", "srt", "vtt")


def _timestamp(seconds: float, sep: str) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def to_srt(segments: list[dict[str, Any]]) -> str:
    return "".join(
        f"{i}\n{_timestamp(s['start'], ',')} --> {_timestamp(s['end'], ',')}\n{s['text'].strip()}\n\n"
        for i, s in enumerate(segments, 1)
    )


def to_vtt(segments: list[dict[str, Any]]) -> str:
    return "WEBVTT\n\n" + "".join(
        f"{_timestamp(s['start'], '.')} --> {_timestamp(s['end'], '.')}\n{s['text'].strip()}\n\n"
        for s in segments
    )


def _language_name(code: str | None) -> str | None:
    # OpenAI's verbose_json names the language ("english"), the request takes the code ("en")
    from transformers.models.whisper.tokenization_whisper import LANGUAGES

    return LANGUAGES.get(code, code) if code else None


def _language_code(value: str) -> str | None:
    """ISO code for a code or an English name ("de", "German"); None when Whisper lacks it."""
    from transformers.models.whisper.tokenization_whisper import LANGUAGES, TO_LANGUAGE_CODE

    value = value.strip().lower()
    return value if value in LANGUAGES else TO_LANGUAGE_CODE.get(value)


def render_result(result: dict[str, Any], response_format: str, task: str) -> Response:
    usage = {"type": "duration", "seconds": int(-(-result["duration"] // 1))}
    if response_format == "text":
        return PlainTextResponse(result["text"])
    if response_format == "srt":
        return PlainTextResponse(to_srt(result["segments"]), media_type="application/x-subrip")
    if response_format == "vtt":
        return PlainTextResponse(to_vtt(result["segments"]), media_type="text/vtt")
    if response_format == "verbose_json":
        return JSONResponse({
            "task": task,
            "language": _language_name(result["language"]),
            "duration": result["duration"],
            "text": result["text"],
            "segments": result["segments"],
            "usage": usage,
        })
    return JSONResponse({"text": result["text"], "usage": usage})


def register_audio_routes(app: FastAPI, get_state: Callable[[], Any], get_client: Callable[[], Any]) -> None:
    async def handle(request: Request, task: str) -> Response:
        client = get_client()
        if client is None:
            return create_error_response(
                "this server has no speech-to-text model (start it with --stt-model)", 404
            )
        if (gate := _maintenance_gate(get_state())) is not None:
            return gate
        try:
            form = await request.form()
        except Exception as exc:  # noqa: BLE001 -- not multipart, or a malformed body
            return create_error_response(f"expected a multipart/form-data body: {exc}")
        upload = form.get("file")
        if upload is None or isinstance(upload, str):
            return create_error_response("missing audio upload in field 'file'", param="file")
        response_format = form.get("response_format") or "json"
        if response_format not in RESPONSE_FORMATS:
            return create_error_response(
                f"response_format must be one of {', '.join(RESPONSE_FORMATS)}", param="response_format"
            )
        try:
            temperature = float(form.get("temperature") or 0.0)
        except ValueError:
            return create_error_response("temperature must be a number", param="temperature")
        # translations always target English; the source language is detected
        language = (form.get("language") or None) if task == "transcribe" else None
        if language is not None and (language := _language_code(language)) is None:
            return create_error_response(f"unknown language {form.get('language')!r}", param="language")

        from freetoken.stt.audio import AudioDecodeError, decode_audio

        data = await upload.read()
        try:
            audio = await asyncio.to_thread(decode_audio, data)
        except AudioDecodeError as exc:
            return create_error_response(str(exc), param="file")

        from freetoken.stt.client import SttError

        try:
            result = await client.transcribe(
                audio,
                task=task,
                language=language,
                prompt=form.get("prompt") or None,
                temperature=temperature,
            )
        except SttError as exc:
            return create_error_response(str(exc), 500, err_type="server_error")
        return render_result(result, response_format, task)

    @app.post("/v1/audio/transcriptions")
    async def v1_audio_transcriptions(request: Request):
        return await handle(request, "transcribe")

    @app.post("/v1/audio/translations")
    async def v1_audio_translations(request: Request):
        return await handle(request, "translate")
