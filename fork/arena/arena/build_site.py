"""Builds site/index.html (one self-contained page) from aufgaben/, models.toml and results/runs.jsonl."""
import argparse
import base64
import json
import mimetypes
from pathlib import Path

from .run import ROOT, latest_results, load_models
from .tasks import CATEGORIES, load_tasks

PROMPT_PREVIEW = 6000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks-dir", default=str(ROOT / "aufgaben"))
    ap.add_argument("--out", default=str(ROOT / "site" / "index.html"))
    ap.add_argument("--banner", help="Hinweiszeile oben auf der Seite")
    ap.add_argument("--hardware", default="RTX 4090 24 GB, 14900K")
    a = ap.parse_args()

    tasks = load_tasks(Path(a.tasks_dir))
    models_cfg = load_models()
    results = list(latest_results().values())
    task_ids = {t.id for t in tasks}
    results = [r for r in results if r["task"] in task_ids and r["model"] in models_cfg]
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
            "banner": a.banner, "hardware": a.hardware}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = (Path(__file__).parent / "site_template.html").read_text().replace("/*DATA*/", blob)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"{out}: {len(tasks)} Aufgaben, {len(models)} Modelle, {len(results)} Ergebnisse, {len(html) // 1024} KiB")


if __name__ == "__main__":
    main()
