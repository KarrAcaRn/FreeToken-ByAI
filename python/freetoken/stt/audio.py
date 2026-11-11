"""Audio bytes -> 16 kHz mono float32, the input every speech model here takes.

Model-agnostic on purpose: the Whisper runner uses it today, an audio encoder tower in the
engine can use it later. PyAV (the `audio` extra) bundles ffmpeg, so no system binary is needed.
"""

from __future__ import annotations

import io

import numpy as np

SAMPLE_RATE = 16000
# OpenAI's own upload limit for /v1/audio/transcriptions
MAX_AUDIO_BYTES = 25 * 1024 * 1024
MAX_AUDIO_SECONDS = 4 * 3600


class AudioDecodeError(ValueError):
    pass


def decode_audio(data: bytes, max_seconds: float = MAX_AUDIO_SECONDS) -> np.ndarray:
    """Decode any container/codec ffmpeg knows into a 1-D float32 array at SAMPLE_RATE."""
    if not data:
        raise AudioDecodeError("audio file is empty")
    if len(data) > MAX_AUDIO_BYTES:
        raise AudioDecodeError(f"audio file exceeds {MAX_AUDIO_BYTES // (1024 * 1024)} MiB")
    import av

    max_samples = int(max_seconds * SAMPLE_RATE)
    chunks: list[np.ndarray] = []
    total = 0
    try:
        with av.open(io.BytesIO(data), mode="r") as container:
            if not container.streams.audio:
                raise AudioDecodeError("file has no audio stream")
            stream = container.streams.audio[0]
            resampler = av.AudioResampler(format="flt", layout="mono", rate=SAMPLE_RATE)
            for frame in container.decode(stream):
                for out in resampler.resample(frame):
                    chunk = out.to_ndarray().reshape(-1)
                    chunks.append(chunk)
                    total += chunk.size
                if total > max_samples:
                    raise AudioDecodeError(f"audio is longer than {max_seconds:.0f} s")
            # None flushes the resampler's tail
            for out in resampler.resample(None):
                chunks.append(out.to_ndarray().reshape(-1))
    except AudioDecodeError:
        raise
    except Exception as exc:  # noqa: BLE001 -- av raises a wide family of errors for bad input
        raise AudioDecodeError(f"could not decode audio: {exc}") from None
    if not chunks:
        raise AudioDecodeError("audio stream decoded to no samples")
    return np.concatenate(chunks).astype(np.float32, copy=False)
