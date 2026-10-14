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
    a = ap.parse_args()
    tasks = load_tasks(Path(a.tasks_dir))

    def answer_for(messages):
        c = messages[-1]["content"]
        text = c if isinstance(c, str) else " ".join(p.get("text", "") for p in c if p.get("type") == "text")
        for t in tasks:
            if t.prompt[:200] in text:
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
            ans = answer_for(req["messages"])
            words = ans.split(" ")
            self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
            time.sleep(0.05)
            for i, w in enumerate(words):
                d = {"choices": [{"index": 0, "delta": {"content": w + (" " if i < len(words) - 1 else "")}, "finish_reason": None}]}
                self.wfile.write(f"data: {json.dumps(d)}\n\n".encode()); self.wfile.flush()
                time.sleep(1 / a.tps)
            self.wfile.write(f"data: {json.dumps({'choices': [{'index': 0, 'delta': {}, 'finish_reason': 'stop'}]})}\n\n".encode())
            usage = {"prompt_tokens": len(json.dumps(req["messages"])) // 4, "completion_tokens": len(words), "total_tokens": 0}
            self.wfile.write(f"data: {json.dumps({'choices': [], 'usage': usage})}\n\ndata: [DONE]\n\n".encode())

    ThreadingHTTPServer(("127.0.0.1", a.port), H).serve_forever()


if __name__ == "__main__":
    main()
