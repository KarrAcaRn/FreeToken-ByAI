"""Frontend side of the STT worker: spawn it, wait for its ready ack, route requests to it."""

from __future__ import annotations

import asyncio
import itertools
import multiprocessing as mp
import queue
import threading
from typing import TYPE_CHECKING, Any

from freetoken.utils import init_logger

if TYPE_CHECKING:
    from freetoken.server.args import ServerArgs

logger = init_logger(__name__, "initializer")

# set by start_stt_worker in the API server process; None = no --stt-model
_CLIENT: "SttClient | None" = None


class SttError(RuntimeError):
    pass


class SttClient:
    def __init__(self, model_name: str, req_queue: Any, resp_queue: Any, process: Any) -> None:
        self.model_name = model_name
        self._req, self._resp, self.process = req_queue, resp_queue, process
        self._ids = itertools.count()
        self._pending: dict[int, tuple[asyncio.AbstractEventLoop, asyncio.Future]] = {}
        self._lock = threading.Lock()
        threading.Thread(target=self._read_loop, name="freetoken-stt-reader", daemon=True).start()

    def _read_loop(self) -> None:
        while True:
            msg = self._resp.get()
            with self._lock:
                entry = self._pending.pop(msg["id"], None)
            if entry is None:
                continue
            loop, fut = entry
            loop.call_soon_threadsafe(_settle, fut, msg)

    async def transcribe(self, audio: Any, **options: Any) -> dict[str, Any]:
        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        req_id = next(self._ids)
        with self._lock:
            self._pending[req_id] = (loop, fut)
        self._req.put({"id": req_id, "audio": audio, **options})
        try:
            return await fut
        finally:
            with self._lock:
                self._pending.pop(req_id, None)


def _settle(fut: asyncio.Future, msg: dict[str, Any]) -> None:
    if fut.done():  # the client went away
        return
    if msg["ok"]:
        fut.set_result(msg["result"])
    else:
        fut.set_exception(SttError(msg["error"]))


def get_stt_client() -> SttClient | None:
    return _CLIENT


def start_stt_worker(args: "ServerArgs") -> mp.Process:
    """Spawn the worker and block until it is loaded and warmed up, so the engine started after
    it measures free VRAM with Whisper already resident."""
    global _CLIENT
    from .worker import run_stt_worker

    gpu = args.stt_gpu or (args.gpu_assigned or args.gpu or ("0",))[0]
    req_q, resp_q, ack_q = mp.Queue(), mp.Queue(), mp.Queue()
    p = mp.Process(
        target=run_stt_worker,
        args=(args.stt_model, gpu, "float16", args.stt_timestamps, req_q, resp_q, ack_q, args.shell_mode),
        daemon=False,
        name="freetoken-stt",
    )
    p.start()
    logger.info(f"Loading STT model {args.stt_model} on GPU {gpu} ...")
    while True:
        try:
            msg = ack_q.get(timeout=1.0)
        except queue.Empty:
            if not p.is_alive():
                raise SystemExit(f"STT worker exited during load (exit code {p.exitcode})")
            continue
        if isinstance(msg, tuple) and msg[0] == "error":
            p.join(timeout=10)
            raise SystemExit(f"STT model failed to load: {msg[1]}")
        if isinstance(msg, tuple) and msg[0] == "ready":
            break
    _CLIENT = SttClient(args.stt_served_name, req_q, resp_q, p)
    return p
