"""Re-grade stored answers after a task's check changed but its prompt did not.

    python -m arena.regrade --task delphi-result-init --old-fingerprint e155a6b1c8b9

Every newest result of the task that still carries the old fingerprint is checked again with the new
rules. When the run would have taken the same course (follow-up asked or not, no correction rounds), a
copy with the new fingerprint and score is appended to results/runs.jsonl. When the new check would
have changed the course - a follow-up the model now does not need, or one it now would get - the result
is left alone and listed: rerun it with `python -m arena.run --model <id> --task <task> --force`.
"""
import argparse
import json
from pathlib import Path

from .run import ROOT, append, latest_results
from .tasks import load_tasks

FOLLOWUP_MARK = "\n\n--- Nachfrage: "


def _followup_for(t, c):
    return next((f for f in t.followups if not c.passed and c.missing is not None
                 and any(m in c.missing for m in f["when_missing"])
                 and all(x in (c.found or []) for x in f["when_found"])), None)


def regrade(rec: dict, t) -> tuple[dict | None, str]:
    """(new record or None, why); None means the course would differ, so only a rerun is honest."""
    if rec.get("retries"):
        return None, "hatte Korrekturdurchgänge"
    answer = rec.get("answer") or ""
    # runs.jsonl keeps only the last 20000 characters, so a longer answer may have lost its first round
    if rec.get("answer_chars") and rec["answer_chars"] > len(answer):
        return None, "Antwort nur gekürzt gespeichert"
    first = answer.split(FOLLOWUP_MARK)[0]
    c = t.check(first)
    fu = _followup_for(t, c)
    asked = rec.get("followup")
    if (fu is not None) != (asked is not None):
        return None, "Nachfrage würde jetzt " + ("gestellt" if fu is not None else "entfallen")
    if t.retries and not c.passed and c.kind in t.retries["on"]:
        return None, "würde jetzt Korrekturdurchgänge bekommen"
    if fu is not None:
        first_c = c
        c = t.check(answer)
        c.score = round(c.score * fu["score_factor"], 3)
        c.detail += f" (nach Nachfrage x{fu['score_factor']:g})"
        asked = {**asked, "first_score": first_c.score, "first_detail": first_c.detail}
    new = {**rec, "fingerprint": t.fingerprint, "passed": c.passed, "score": c.score, "detail": c.detail,
           "artifact": c.artifact, "followup": asked, "regraded_from": rec["fingerprint"]}
    if rec.get("think_stopped"):
        new["detail"] += f" (Denken nach {rec['think_limit'] / 60:g} min abgebrochen)"
    last = (rec.get("turns") or [{}])[-1].get("finish_reason")
    if last == "time" and not c.passed:
        new["detail"] += f" (Schreibzeit {rec['write_limit'] / 60:g} min abgelaufen)"
    if last == "length" and not c.passed:
        new["detail"] += " (Kontext voll)" if not t.max_tokens else f" (Tokenlimit {t.max_tokens} erreicht)"
    return new, "neu bewertet"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--old-fingerprint", required=True, help="nur Ergebnisse mit genau diesem Fingerabdruck")
    ap.add_argument("--tasks-dir", default=str(ROOT / "aufgaben"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    [t] = load_tasks(Path(a.tasks_dir), [a.task])
    rerun = []
    for (model, task), rec in sorted(latest_results().items()):
        if task != t.id or rec.get("fingerprint") != a.old_fingerprint or rec.get("status") != "ok":
            continue
        new, why = regrade(rec, t)
        if new is None:
            rerun.append(model)
            print(f"{model}: NEU LAUFEN LASSEN - {why}")
            continue
        change = "" if (new["score"], new["passed"]) == (rec["score"], rec["passed"]) else f"  (vorher {rec['score']})"
        print(f"{model}: score {new['score']}{change}")
        if not a.dry_run:
            append(new)
    if rerun:
        print("\nneu laufen lassen: python -m arena.run " + " ".join(f"--model {m}" for m in rerun)
              + f" --task {t.id} --force")


if __name__ == "__main__":
    main()
