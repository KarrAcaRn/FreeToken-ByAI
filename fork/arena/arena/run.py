"""Runs tasks against models and appends results to results/runs.jsonl.

  python -m arena.run --model qwen3-0.6b                      # start ft serve per models.toml, run all tasks
  python -m arena.run --model all --task code-beispiel        # every model, one task
  python -m arena.run --url http://127.0.0.1:1919/v1 --name extern-test   # an already running server
"""
import argparse
import datetime as dt
import glob
import json
import os
import shlex
import signal
import subprocess
import sys
import time
import tomllib
import urllib.error
from pathlib import Path

from .client import chat, get_json
from .tasks import load_tasks

ROOT = Path(__file__).resolve().parent.parent
RESULTS = Path(os.environ.get("ARENA_RESULTS", ROOT / "results" / "runs.jsonl"))


def load_models() -> dict:
    return tomllib.loads((ROOT / "models.toml").read_text())


def latest_results() -> dict:
    """(model, task) -> newest record."""
    out = {}
    if RESULTS.exists():
        for line in RESULTS.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                out[(r["model"], r["task"])] = r
    return out


def append(rec: dict):
    RESULTS.parent.mkdir(exist_ok=True)
    with RESULTS.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def git_rev(path: str) -> str | None:
    try:
        return subprocess.run(["git", "-C", path, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or None
    except OSError:
        return None


def run_tasks(url: str, model_id: str, served: str, caps: set, ctx: int | None, tasks, meta: dict, force: bool, api_key=None):
    done = latest_results()
    for t in tasks:
        old = done.get((model_id, t.id))
        if old and old.get("fingerprint") == t.fingerprint and old["status"] in ("ok", "skipped") and not force:
            print(f"  {t.id}: aktuelles Ergebnis vorhanden, übersprungen (--force zum Wiederholen)")
            continue
        rec = {"model": model_id, "task": t.id, "fingerprint": t.fingerprint,
               "time": dt.datetime.now().isoformat(timespec="seconds"), **meta}
        missing = t.needs - caps
        approx_prompt = len(t.prompt) // 3 + 800 * len(t.images)
        if missing:
            rec.update(status="skipped", reason="kann das Modell nicht: " + ", ".join(sorted(missing)))
        elif ctx and approx_prompt + t.max_tokens > ctx:
            rec.update(status="skipped", reason=f"Kontext zu klein (~{approx_prompt} + {t.max_tokens} > {ctx} Tokens)")
        else:
            try:
                r = chat(url, served, t.messages(), t.max_tokens, api_key=api_key)
            except urllib.error.HTTPError as e:
                rec.update(status="error", reason=f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}")
            except Exception as e:
                rec.update(status="error", reason=repr(e)[:300])
            else:
                c = t.check(r["content"])
                turns = [r]
                answer = r["content"]
                asked = None
                fu = next((f for f in t.followups if not c.passed and c.missing is not None
                           and any(m in c.missing for m in f["when_missing"])
                           and all(x in (c.found or []) for x in f["when_found"])), None)
                if fu is not None:
                    msgs = t.messages() + [{"role": "assistant", "content": r["content"]},
                                           {"role": "user", "content": fu["prompt"]}]
                    try:
                        r2 = chat(url, served, msgs, t.max_tokens, api_key=api_key)
                    except Exception as e:
                        asked = {"prompt": fu["prompt"], "error": repr(e)[:300]}
                    else:
                        turns.append(r2)
                        answer = r["content"] + "\n\n--- Nachfrage: " + fu["prompt"] + " ---\n\n" + r2["content"]
                        first = c
                        c = t.check(answer)
                        asked = {"prompt": fu["prompt"], "first_score": first.score, "first_detail": first.detail}
                tok = sum(x["completion_tokens"] or 0 for x in turns)
                dec = sum(x["decode_s"] for x in turns)
                rec.update(status="ok", passed=c.passed, score=c.score, detail=c.detail, artifact=c.artifact,
                           answer=answer[-20000:], reasoning_chars=sum(len(x["reasoning"]) for x in turns),
                           followup=asked, finish_reason=turns[-1]["finish_reason"], prompt_tokens=r["prompt_tokens"],
                           completion_tokens=tok, ttft_s=r["ttft_s"], total_s=round(sum(x["total_s"] for x in turns), 3),
                           decode_tps=round((tok - len(turns)) / dec, 1) if dec > 0 and tok > len(turns) else None,
                           prefill_tps=r["prefill_tps"])
                if turns[-1]["finish_reason"] == "length" and not c.passed:
                    rec["detail"] += f" (Tokenlimit {t.max_tokens} erreicht)"
        append(rec)
        if rec["status"] == "ok":
            fu = " nach Nachfrage" if rec.get("followup") else ""
            print(f"  {t.id}: {'BESTANDEN' if rec['passed'] else 'nicht bestanden'}{fu} score={rec['score']} "
                  f"{rec['completion_tokens']} tok, {rec['total_s']} s, {rec['decode_tps']} tok/s - {rec['detail'][:100]}")
        else:
            print(f"  {t.id}: {rec['status']} - {rec['reason']}")


def serve(model_id: str, m: dict, port: int, log: Path):
    hub = os.path.expanduser(os.environ.get("HF_HUB", "~/.cache/huggingface/hub"))
    paths = sorted(glob.glob(os.path.join(hub, m["path"])))
    if not paths:
        raise SystemExit(f"{model_id}: kein Checkpoint für {m['path']} unter {hub}")
    tree = os.path.expanduser(m.get("worktree", "~/claude/ft-speed-wt"))
    venv = os.path.expanduser("~/claude/FreeToken-ByAI/.venv/bin")
    env = dict(os.environ, PATH=f"{venv}:/usr/local/cuda/bin:" + os.environ["PATH"], CUDA_HOME="/usr/local/cuda",
               PYTHONPATH=f"{tree}/python")
    cmd = [f"{venv}/ft", "serve", paths[0], "--port", str(port), "--served-model-name", model_id] + shlex.split(m.get("flags", ""))
    log.parent.mkdir(parents=True, exist_ok=True)
    print(f"[{model_id}] {' '.join(cmd)}")
    proc = subprocess.Popen(cmd, env=env, stdout=log.open("w"), stderr=subprocess.STDOUT, start_new_session=True)
    base = f"http://127.0.0.1:{port}"
    t0 = time.time()
    while True:
        if proc.poll() is not None:
            raise RuntimeError(f"ft serve beendet (rc {proc.returncode}), siehe {log}")
        try:
            h = get_json(base + "/health")
            if h.get("status") == "ok":
                break
            if h.get("status") == "error":
                raise RuntimeError(h.get("message"))
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            pass
        if time.time() - t0 > m.get("load_timeout", 1800):
            raise RuntimeError("Ladezeit überschritten")
        time.sleep(3)
    return proc, base + "/v1", round(time.time() - t0), tree


def stop(proc):
    try:
        os.killpg(proc.pid, signal.SIGTERM)
        proc.wait(60)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", action="append", help="id aus models.toml oder 'all' (mehrfach möglich)")
    ap.add_argument("--task", action="append", help="nur diese Aufgabe(n)")
    ap.add_argument("--url", help="bereits laufender OpenAI-Endpunkt, z. B. http://127.0.0.1:1919/v1")
    ap.add_argument("--name", help="Modell-id für --url")
    ap.add_argument("--caps", default="", help="Fähigkeiten für --url, z. B. vision")
    ap.add_argument("--api-key", default=os.environ.get("ARENA_API_KEY"))
    ap.add_argument("--port", type=int, default=19190)
    ap.add_argument("--force", action="store_true", help="auch Aufgaben mit aktuellem Ergebnis wiederholen")
    ap.add_argument("--tasks-dir", default=str(ROOT / "aufgaben"))
    a = ap.parse_args()

    tasks = load_tasks(Path(a.tasks_dir), a.task)
    if not tasks:
        raise SystemExit(f"keine Aufgaben in {a.tasks_dir}")
    if a.url:
        name = a.name or "extern"
        models = load_models()
        caps = set(filter(None, a.caps.split(","))) or set(models.get(name, {}).get("caps", []))
        served = get_json(a.url.rstrip("/") + "/models", a.api_key)["data"][0]
        run_tasks(a.url, name, served["id"], caps, served.get("context_length"), tasks,
                  {"engine": "extern", "url": a.url}, a.force, a.api_key)
        return

    models = load_models()
    ids = [k for k, v in models.items() if not v.get("skip")] if not a.model or "all" in a.model else a.model
    for mid in ids:
        if mid not in models:
            raise SystemExit(f"unbekanntes Modell {mid}; bekannt: {', '.join(models)}")
        m = models[mid]
        done = latest_results()
        todo = [t for t in tasks if a.force or (done.get((mid, t.id)) or {}).get("fingerprint") != t.fingerprint
                or done[(mid, t.id)]["status"] == "error"]
        if not todo:
            print(f"[{mid}] alles aktuell")
            continue
        log = ROOT / "results" / "logs" / f"{mid}.log"
        try:
            proc, url, load_s, tree = serve(mid, m, a.port, log)
        except Exception as e:
            print(f"[{mid}] Start fehlgeschlagen: {e}")
            for t in todo:
                append({"model": mid, "task": t.id, "fingerprint": t.fingerprint, "status": "error",
                        "reason": f"Server startet nicht: {e}"[:300], "time": dt.datetime.now().isoformat(timespec="seconds")})
            continue
        try:
            ctx = get_json(url + "/models")["data"][0].get("context_length")
            print(f"[{mid}] bereit nach {load_s} s, Kontext {ctx}")
            meta = {"engine": "freetoken", "commit": git_rev(tree), "branch": Path(tree).name, "load_s": load_s, "ctx": ctx}
            run_tasks(url, mid, mid, set(m.get("caps", [])), ctx, todo, meta, True)
        finally:
            stop(proc)


if __name__ == "__main__":
    sys.exit(main())
