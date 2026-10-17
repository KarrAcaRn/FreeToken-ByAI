"""Builds site/index.html (one self-contained page) from aufgaben/, models.toml and results/runs.jsonl."""
import argparse
import base64
import json
import mimetypes
from pathlib import Path

from . import run as runmod
from .run import ROOT, latest_results, latest_runs, load_models
from .tasks import CATEGORIES, load_tasks

PROMPT_PREVIEW = 6000
# answers that loop until the time limit run to hundreds of KB; the page keeps their start and end
ANSWER_HEAD, ANSWER_TAIL = 3000, 1000


def _short_answer(text: str | None) -> str | None:
    if not text or len(text) <= ANSWER_HEAD + ANSWER_TAIL:
        return text
    cut = len(text) - ANSWER_HEAD - ANSWER_TAIL
    return f"{text[:ANSWER_HEAD]}\n\n[... {cut} Zeichen gekürzt, vollständig im Transkript ...]\n\n{text[-ANSWER_TAIL:]}"


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 3) if xs else None


def _aggregate_runs(runs: dict, tasks) -> list[dict]:
    """One record per (model, task) over its runs: the cell shows solved k/n and the mean score; "runs" keeps each run."""
    fp = {t.id: t.fingerprint for t in tasks}
    out = []
    for (model, task), by_run in runs.items():
        recs = [by_run[k] for k in sorted(by_run)]
        cur = [r for r in recs if r.get("fingerprint") == fp.get(task)]
        use = cur or recs
        ok = [r for r in use if r.get("status") == "ok"]
        agg = {"model": model, "task": task, "fingerprint": use[0].get("fingerprint"),
               "time": max(r.get("time", "") for r in use), "status": "ok" if ok else use[-1].get("status"),
               "reason": None if ok else use[-1].get("reason"), "runs": use}
        if ok:
            graded = [r for r in ok if r.get("passed") is not None]
            agg.update(
                n=len(use), solved_runs=sum(1 for r in graded if r["passed"]),
                passed=None if not graded else all(r["passed"] for r in graded) and len(graded) == len(use),
                score=_mean([r.get("score") for r in graded]) if graded else None,
                decode_tps=_mean([r.get("decode_tps") for r in ok]),
                completion_tokens=_mean([r.get("completion_tokens") for r in ok]),
                total_s=_mean([r.get("total_s") for r in ok]),
                commit=ok[-1].get("commit"), branch=ok[-1].get("branch"), engine=ok[-1].get("engine"),
            )
        out.append(agg)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks-dir", default=str(ROOT / "aufgaben"))
    ap.add_argument("--out", help="Standard: site/index.html, mit --echt site/echt.html")
    ap.add_argument("--banner", help="Hinweiszeile oben auf der Seite")
    ap.add_argument("--hardware", default="RTX 4090 24 GB, 14900K")
    ap.add_argument("--echt", action="store_true", help="Seite 'echtes Verhalten' aus results/echt.jsonl (3 Läufe je Aufgabe)")
    a = ap.parse_args()
    if a.echt and "ARENA_RESULTS" not in __import__("os").environ:
        runmod.RESULTS = ROOT / "results" / "echt.jsonl"
    a.out = a.out or str(ROOT / "site" / ("echt.html" if a.echt else "index.html"))

    tasks = load_tasks(Path(a.tasks_dir))
    models_cfg = load_models()
    results = list(latest_results().values()) if not a.echt else _aggregate_runs(latest_runs(), tasks)
    task_ids = {t.id for t in tasks}
    results = [r for r in results if r["task"] in task_ids and r["model"] in models_cfg]
    short = lambda r: {**r, "answer": _short_answer(r.get("answer"))}
    results = [{**short(r), "runs": [short(x) for x in r["runs"]]} if "runs" in r else short(r) for r in results]
    with_results = {r["model"] for r in results}
    models = [{"id": k, "label": v.get("label", k), "group": v.get("group", "")}
              for k, v in models_cfg.items() if k in with_results or (not with_results and not v.get("skip"))]
    known = {m["id"] for m in models}
    models += [{"id": m, "label": m, "group": "extern"} for m in sorted(with_results - known)]

    tdata = []
    for t in tasks:
        d = {"id": t.id, "title": t.title, "category": t.category, "level": t.level, "summary": t.summary,
             "check_type": t.check_type, "graded": t.check_type != "svg_view", "needs": sorted(t.needs),
             "fingerprint": t.fingerprint,
             "prompt": t.prompt if len(t.prompt) <= PROMPT_PREVIEW else
             t.prompt[:PROMPT_PREVIEW] + f"\n\n[... {len(t.prompt) - PROMPT_PREVIEW} weitere Zeichen ...]",
             "images": [f"data:{mimetypes.guess_type(p.name)[0] or 'image/png'};base64," + base64.b64encode(p.read_bytes()).decode()
                        for p in t.images]}
        if t.check_type == "svg_reference":
            import tomllib
            ref = tomllib.loads((t.dir / "task.toml").read_text())["check"].get("reference", "reference.svg")
            d["reference_svg"] = (t.dir / ref).read_text()
        tdata.append(d)

    data = {"categories": CATEGORIES, "tasks": tdata, "models": models, "results": results,
            "banner": a.banner, "hardware": a.hardware, "mode": "echt" if a.echt else "debug"}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/").replace("\ufffd", "\\ufffd")
    html = (Path(__file__).parent / "site_template.html").read_text().replace("/*DATA*/", blob)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"{out}: {len(tasks)} Aufgaben, {len(models)} Modelle, {len(results)} Ergebnisse, {len(html) // 1024} KiB")


if __name__ == "__main__":
    main()
