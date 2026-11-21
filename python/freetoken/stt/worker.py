"""Speech-to-text worker process: one Whisper checkpoint on one GPU, requests run one at a time.

It lives outside the paged LLM engine: Whisper is an encoder-decoder with cross-attention, and at
0.8B parameters a transformers forward is fast enough that batching is not worth an engine path.
"""

from __future__ import annotations

import time
from typing import Any

import numpy as np

from .audio import SAMPLE_RATE

# Whisper's fixed window; longer input switches transformers to sequential long-form decoding
WINDOW_SECONDS = 30
# windows per generate call on the no-timestamps path
WINDOW_BATCH = 8


def _segment(index: int, start: float, end: float, text: str) -> dict[str, Any]:
    # one leading space per segment is Whisper's word separator, kept so segments join cleanly
    return {"id": index, "start": round(start, 2), "end": round(end, 2), "text": text if text[:1].isspace() else " " + text}


class WhisperRunner:
    def __init__(self, model_path: str, device: Any, dtype: Any, timestamps: bool = True) -> None:
        import torch
        from transformers import WhisperForConditionalGeneration, WhisperProcessor

        self.device, self.dtype = device, dtype
        # some fine-tunes (TheStageAI/thewhisper-*) no longer emit timestamp tokens; transformers'
        # long-form decoding seeks by them and drops text without, so those decode fixed windows
        self.timestamps = timestamps
        self.processor = WhisperProcessor.from_pretrained(model_path)
        self.model = WhisperForConditionalGeneration.from_pretrained(
            model_path, dtype=dtype, attn_implementation="sdpa"
        ).to(device)
        self.model.eval()
        self._torch = torch

    def _features(self, audio: np.ndarray) -> dict[str, Any]:
        if audio.size <= WINDOW_SECONDS * SAMPLE_RATE:
            inputs = self.processor(audio, sampling_rate=SAMPLE_RATE, return_tensors="pt")
        else:
            inputs = self.processor(
                audio,
                sampling_rate=SAMPLE_RATE,
                return_tensors="pt",
                truncation=False,
                padding="longest",
                return_attention_mask=True,
            )
        out = {"input_features": inputs.input_features.to(self.device, self.dtype)}
        if "attention_mask" in inputs:
            out["attention_mask"] = inputs.attention_mask.to(self.device)
        return out

    def _detect_language(self, input_features: Any) -> str | None:
        # first window only, the way Whisper itself picks the language
        lang_ids = self.model.detect_language(input_features[:, :, : WINDOW_SECONDS * 100])
        token = self.processor.tokenizer.convert_ids_to_tokens(int(lang_ids[0]))
        return token.strip("<|>") if isinstance(token, str) else None

    def transcribe(
        self,
        audio: np.ndarray,
        language: str | None = None,
        task: str = "transcribe",
        prompt: str | None = None,
        temperature: float = 0.0,
    ) -> dict[str, Any]:
        kwargs: dict[str, Any] = {"task": task}
        if language:
            kwargs["language"] = language
        if prompt:
            kwargs["prompt_ids"] = self.processor.get_prompt_ids(prompt, return_tensors="pt").to(
                self.device
            )
        if temperature > 0:
            kwargs.update(do_sample=True, temperature=temperature)
        if self.timestamps:
            feats = self._features(audio)
            detected = language or self._detect_language(feats["input_features"])
            segments = self._generate_timestamped(feats, kwargs)
        else:
            segments, first_window = self._generate_windows(audio, kwargs)
            detected = language or self._detect_language(first_window)
        return {
            "text": "".join(s["text"] for s in segments).strip(),
            "language": detected,
            "duration": round(audio.size / SAMPLE_RATE, 3),
            "segments": segments,
        }

    def _generate_timestamped(self, feats: dict[str, Any], kwargs: dict[str, Any]) -> list[dict]:
        out = self.model.generate(**feats, **kwargs, return_timestamps=True, return_segments=True)
        tok = self.processor.tokenizer
        return [
            _segment(i, float(seg["start"]), float(seg["end"]), tok.decode(seg["tokens"], skip_special_tokens=True))
            for i, seg in enumerate(out["segments"][0])
        ]

    def _generate_windows(self, audio: np.ndarray, kwargs: dict[str, Any]) -> tuple[list[dict], Any]:
        """Independent 30 s windows, batched; a word cut at a window edge may be garbled."""
        step = WINDOW_SECONDS * SAMPLE_RATE
        # a sub-second tail window mostly yields a hallucinated "Thank you."
        starts = [s for s in range(0, audio.size, step) if s == 0 or audio.size - s >= SAMPLE_RATE]
        tok = self.processor.tokenizer
        segments: list[dict] = []
        first_window = None
        for b in range(0, len(starts), WINDOW_BATCH):
            batch = [audio[s : s + step] for s in starts[b : b + WINDOW_BATCH]]
            feats = self.processor(batch, sampling_rate=SAMPLE_RATE, return_tensors="pt")
            input_features = feats.input_features.to(self.device, self.dtype)
            if first_window is None:
                first_window = input_features[:1]
            ids = self.model.generate(input_features, **kwargs, return_timestamps=False)
            for s, text in zip(starts[b : b + WINDOW_BATCH], tok.batch_decode(ids, skip_special_tokens=True)):
                end = min(s + step, audio.size) / SAMPLE_RATE
                segments.append(_segment(len(segments), s / SAMPLE_RATE, end, text))
        return segments, first_window

    def warmup(self) -> None:
        """The largest batch once, so the caching allocator already holds the peak before the
        engine measures free VRAM."""
        windows = 1 if self.timestamps else WINDOW_BATCH
        self.transcribe(np.zeros(windows * WINDOW_SECONDS * SAMPLE_RATE, dtype=np.float32), language="en")
        self._torch.cuda.synchronize(self.device)


def run_stt_worker(
    model_path: str,
    gpu: str,
    dtype_name: str,
    timestamps: bool,
    req_queue: Any,
    resp_queue: Any,
    ack_queue: Any,
    detach: bool = False,
) -> None:
    from freetoken.gpu_select import bind_assigned_gpu, set_assigned_gpu
    from freetoken.server.launch import _detach_process_group, _report_startup_error
    from freetoken.utils import init_logger

    if detach:  # shell mode, see _detach_process_group
        _detach_process_group()

    logger = init_logger(__name__, "stt")
    try:
        set_assigned_gpu(gpu)
        import torch

        device = bind_assigned_gpu()
        torch.set_grad_enabled(False)
        free_before = torch.cuda.mem_get_info(device)[0]
        runner = WhisperRunner(model_path, device, getattr(torch, dtype_name), timestamps)
        runner.warmup()
        used = free_before - torch.cuda.mem_get_info(device)[0]
    except Exception as exc:  # noqa: BLE001 -- surface the reason, then let it propagate
        _report_startup_error(ack_queue, exc)
        raise
    logger.info(f"STT model {model_path} ready on {device}, {used / 2**30:.2f} GiB VRAM")
    ack_queue.put(("ready", {"vram_bytes": used}))

    while True:
        try:
            req = req_queue.get()
        except KeyboardInterrupt:  # ^C reaches the whole group; the parent tears us down
            return
        if req is None:
            return
        t0 = time.perf_counter()
        try:
            with torch.inference_mode():
                result = runner.transcribe(
                    req["audio"],
                    language=req.get("language"),
                    task=req.get("task", "transcribe"),
                    prompt=req.get("prompt"),
                    temperature=req.get("temperature") or 0.0,
                )
            elapsed = time.perf_counter() - t0
            logger.info(
                f"STT {req['task']}: {result['duration']:.1f} s audio in {elapsed:.2f} s "
                f"(RTFx {result['duration'] / max(elapsed, 1e-6):.1f})"
            )
            resp_queue.put({"id": req["id"], "ok": True, "result": result})
        except Exception as exc:  # noqa: BLE001 -- one bad request must not kill the worker
            logger.exception("STT request failed")
            resp_queue.put({"id": req["id"], "ok": False, "error": f"{type(exc).__name__}: {exc}"})
