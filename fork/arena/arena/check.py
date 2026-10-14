"""Checks a task before any model sees it: loads task.toml and runs the checker on musterloesung.md.

  python -m arena.check                     # alle Aufgaben in aufgaben/
  python -m arena.check vorlagen/svg-beispiel
"""
import sys
from pathlib import Path

from .run import ROOT
from .tasks import load_task


def main():
    args = sys.argv[1:] or [str(p) for p in sorted((ROOT / "aufgaben").iterdir()) if (p / "task.toml").exists()]
    bad = 0
    for a in args:
        d = Path(a).resolve()
        try:
            t = load_task(d)
        except Exception as e:
            print(f"FEHLER  {d.name}: task.toml lädt nicht: {e!r}")
            bad += 1
            continue
        ms = d / "musterloesung.md"
        if not ms.exists():
            print(f"?       {t.id}: lädt ({t.category}, {t.check_type}), aber ohne musterloesung.md ungeprüft")
            continue
        c = t.check(ms.read_text())
        print(f"{'OK     ' if c.passed else 'FEHLER '} {t.id}: Musterlösung {'besteht' if c.passed else 'besteht NICHT'} - {c.detail}")
        bad += not c.passed
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
