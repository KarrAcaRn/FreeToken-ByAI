"""OpenAI-style fake server for testing the pipeline without a GPU: answers with each task's musterloesung.md.

  python -m arena.fake_server --tasks-dir vorlagen --port 19199 [--wrong]
"""
import argparse
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .tasks import load_tasks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks-dir", required=True)
    ap.add_argument("--port", type=int, default=19199)
    ap.add_argument("--wrong", action="store_true", help="falsche Antworten liefern")
    ap.add_argument("--tps", type=float, default=80.0)
    ap.add_argument("--think", type=float, default=0.0, help="Sekunden Denkphase (reasoning_content) vor der Antwort")
    a = ap.parse_args()
    tasks = load_tasks(Path(a.tasks_dir))

    def answer_for(messages):
        c = messages[-1]["content"]
        text = c if isinstance(c, str) else " ".join(p.get("text", "") for p in c if p.get("type") == "text")
        for t in tasks:
            if t.prompt[:200] in text or json.dumps(t.prompt)[1:150] in text:
                ms = t.dir / "musterloesung.md"
                ans = ms.read_text() if ms.exists() else "keine Musterlösung"
                return ans.replace("71", "65").replace("0,38", "0,30").replace("[::-1]", "").replace("#333", "#3a7") if a.wrong else ans
        return "unbekannte Aufgabe"

    class H(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _json(self, obj):
            b = json.dumps(obj).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

        def do_GET(self):
            if self.path == "/health":
                self._json({"status": "ok"})
            elif self.path == "/v1/models":
                self._json({"data": [{"id": "fake", "context_length": 32768}]})
            else:
                self.send_error(404)

        def do_POST(self):
            req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            if self.path == "/v1/tokenize":
                # Fake token ids: one per byte, so a continuation prompt decodes back to its text.
                text = json.dumps(req["messages"]) if "messages" in req else req["input"]
                ids = list(text.encode())
                return self._json({"tokens": len(ids), "token_ids": ids})
            completion = self.path == "/v1/completions"
            if completion:
                text = bytes(req["prompt"]).decode(errors="replace")
                ans = answer_for([{"content": text}])
            else:
                ans = answer_for(req["messages"])
            words = ans.split(" ")
            self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
            time.sleep(0.05)
            t_think = time.time() + (0 if completion else a.think)
            try:
                while time.time() < t_think:
                    d = {"choices": [{"index": 0, "delta": {"reasoning_content": "hmm "}, "finish_reason": None}]}
                    self.wfile.write(f"data: {json.dumps(d)}\n\n".encode()); self.wfile.flush()
                    time.sleep(1 / a.tps)
                for i, w in enumerate(words):
                    piece = w + (" " if i < len(words) - 1 else "")
                    d = {"choices": [{"index": 0, "text": piece} if completion else
                                     {"index": 0, "delta": {"content": piece}, "finish_reason": None}]}
                    self.wfile.write(f"data: {json.dumps(d)}\n\n".encode()); self.wfile.flush()
                    time.sleep(1 / a.tps)
            except (BrokenPipeError, ConnectionResetError):
                return
            self.wfile.write(f"data: {json.dumps({'choices': [{'index': 0, 'delta': {}, 'finish_reason': 'stop'}]})}\n\n".encode())
            usage = {"prompt_tokens": len(json.dumps(req.get("messages") or req["prompt"])) // 4, "completion_tokens": len(words), "total_tokens": 0}
            self.wfile.write(f"data: {json.dumps({'choices': [], 'usage': usage})}\n\ndata: [DONE]\n\n".encode())

    ThreadingHTTPServer(("127.0.0.1", a.port), H).serve_forever()


if __name__ == "__main__":
    main()
