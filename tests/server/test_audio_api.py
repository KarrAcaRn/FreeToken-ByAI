from __future__ import annotations

import io
import os
import wave
from types import SimpleNamespace

import numpy as np
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

pytest.importorskip("av")
pytest.importorskip("multipart")

from freetoken.server.audio_api import register_audio_routes  # noqa: E402
from freetoken.stt.audio import SAMPLE_RATE, AudioDecodeError, decode_audio  # noqa: E402

RESULT = {
    "text": "Hello there. General Kenobi.",
    "language": "en",
    "duration": 3.2,
    "segments": [
        {"id": 0, "start": 0.0, "end": 1.5, "text": " Hello there."},
        {"id": 1, "start": 1.5, "end": 3.2, "text": " General Kenobi."},
    ],
}


def wav_bytes(seconds: float = 1.0, rate: int = 44100, channels: int = 2) -> bytes:
    t = np.arange(int(seconds * rate)) / rate
    pcm = (np.sin(2 * np.pi * 440 * t) * 20000).astype("<i2")
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(np.repeat(pcm[:, None], channels, axis=1).tobytes())
    return buf.getvalue()


class FakeStt:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    async def transcribe(self, audio, **options):
        self.calls.append({"samples": audio.size, **options})
        return RESULT


def make_client(stt=None, maintenance_state="serving"):
    app = FastAPI()
    state = SimpleNamespace(maintenance_state=maintenance_state)
    register_audio_routes(app, lambda: state, lambda: stt)
    return TestClient(app)


def post(client, path="/v1/audio/transcriptions", data=None, audio=None):
    files = {"file": ("clip.wav", wav_bytes() if audio is None else audio, "audio/wav")}
    return client.post(path, data=data or {}, files=files)


def test_transcription_forwards_options_and_returns_openai_json():
    """Red if the route stops passing the form fields through or drops OpenAI's json shape."""
    stt = FakeStt()
    resp = post(make_client(stt), data={"model": "whisper-1", "language": "German", "prompt": "Kenobi", "temperature": "0.2"})
    assert resp.status_code == 200
    assert resp.json() == {"text": RESULT["text"], "usage": {"type": "duration", "seconds": 4}}
    (call,) = stt.calls
    assert call == {"samples": SAMPLE_RATE, "task": "transcribe", "language": "de", "prompt": "Kenobi", "temperature": 0.2}


def test_translation_ignores_language_and_sets_the_task():
    """Red if a translation request forwards a source language (Whisper translates into English only)."""
    stt = FakeStt()
    resp = post(make_client(stt), "/v1/audio/translations", data={"language": "de", "response_format": "verbose_json"})
    body = resp.json()
    assert (body["task"], body["language"], body["segments"]) == ("translate", "english", RESULT["segments"])
    assert stt.calls[0]["task"] == "translate" and stt.calls[0]["language"] is None


@pytest.mark.parametrize(
    "fmt,expected",
    [
        ("text", "Hello there. General Kenobi."),
        ("srt", "1\n00:00:00,000 --> 00:00:01,500\nHello there.\n\n2\n00:00:01,500 --> 00:00:03,200\nGeneral Kenobi.\n\n"),
        ("vtt", "WEBVTT\n\n00:00:00.000 --> 00:00:01.500\nHello there.\n\n00:00:01.500 --> 00:00:03.200\nGeneral Kenobi.\n\n"),
    ],
)
def test_plain_response_formats(fmt, expected):
    """Red if the srt/vtt timestamp layout (comma vs dot, cue numbering) or text output changes."""
    resp = post(make_client(FakeStt()), data={"response_format": fmt})
    assert resp.status_code == 200 and resp.text == expected


@pytest.mark.parametrize(
    "data,audio,param",
    [
        ({"response_format": "xml"}, None, "response_format"),
        ({"language": "klingon"}, None, "language"),
        ({"temperature": "hot"}, None, "temperature"),
        ({}, b"not audio at all", "file"),
        ({}, b"", "file"),
    ],
)
def test_bad_requests_are_400_and_name_the_field(data, audio, param):
    """Red if invalid input reaches the worker (a 500 there) instead of failing in the route."""
    stt = FakeStt()
    resp = post(make_client(stt), data=data, audio=audio)
    assert resp.status_code == 400 and resp.json()["error"]["param"] == param
    assert stt.calls == []


def test_unavailable_states():
    """Red if the routes answer without an STT model, or before the engine is serving."""
    assert post(make_client(None)).status_code == 404
    assert post(make_client(FakeStt(), maintenance_state="loading")).status_code == 503
    resp = make_client(FakeStt()).post("/v1/audio/transcriptions", data={"model": "x"})
    assert resp.status_code == 400 and resp.json()["error"]["param"] == "file"


def test_decode_audio_resamples_to_16k_mono():
    """Red if decode_audio stops downmixing or resampling (Whisper's features assume 16 kHz mono)."""
    audio = decode_audio(wav_bytes(seconds=2.0, rate=44100, channels=2))
    assert audio.dtype == np.float32 and audio.ndim == 1
    assert abs(audio.size - 2 * SAMPLE_RATE) <= 32
    assert 0.5 < float(np.abs(audio).max()) <= 1.0
    with pytest.raises(AudioDecodeError, match="longer than"):
        decode_audio(wav_bytes(seconds=2.0), max_seconds=1.0)


WHISPER_MODEL = os.environ.get("FREETOKEN_WHISPER_MODEL")
WHISPER_CLIP = os.environ.get("FREETOKEN_WHISPER_CLIP")


@pytest.mark.needs_weights
@pytest.mark.skipif(not (WHISPER_MODEL and WHISPER_CLIP), reason="FREETOKEN_WHISPER_MODEL / _CLIP not set")
def test_long_form_keeps_every_repetition():
    """A clip repeated three times (> 30 s) yields three times the words. Red if the long-form
    path drops text, as transformers' timestamp seeking does on a checkpoint without timestamp
    tokens unless --stt-no-timestamps is set."""
    torch = pytest.importorskip("torch")
    if not torch.cuda.is_available():
        pytest.skip("needs CUDA")
    from freetoken.stt.worker import WhisperRunner

    clip = decode_audio(open(WHISPER_CLIP, "rb").read())
    assert 11 * SAMPLE_RATE <= clip.size <= 30 * SAMPLE_RATE, "use a 11-30 s speech clip"
    runner = WhisperRunner(WHISPER_MODEL, torch.device("cuda"), torch.float16)
    with torch.inference_mode():
        single = runner.transcribe(clip, language="en")["text"]
        result = runner.transcribe(np.concatenate([clip] * 3), language="en")
    ratio = len(result["text"].split()) / len(single.split())
    assert 2.7 <= ratio <= 3.3
    assert result["segments"][-1]["end"] > 2.5 * clip.size / SAMPLE_RATE
