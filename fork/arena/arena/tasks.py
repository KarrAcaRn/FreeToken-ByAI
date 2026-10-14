"""Loads tasks from aufgaben/<id>/task.toml (format: see README.md)."""
import base64
import hashlib
import mimetypes
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .checks import CHECKERS, Check

CATEGORIES = {"code": "Programmieren", "image": "Bild", "text": "Textverständnis"}


@dataclass
class Task:
    id: str
    category: str
    title: str
    summary: str
    level: str
    prompt: str
    images: list[Path]
    needs: frozenset
    max_tokens: int
    check: Callable[[str], Check]
    check_type: str
    fingerprint: str  # changes whenever any file of the task changes; old results then show as outdated
    dir: Path
    followups: list  # [{"prompt", "when_missing": [...], "when_found": [...]}], see README

    def messages(self) -> list:
        if not self.images:
            return [{"role": "user", "content": self.prompt}]
        parts = []
        for p in self.images:
            mime = mimetypes.guess_type(p.name)[0] or "image/png"
            parts.append({"type": "image_url", "image_url": {"url": f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()}})
        parts.append({"type": "text", "text": self.prompt})
        return [{"role": "user", "content": parts}]


def _fingerprint(d: Path) -> str:
    h = hashlib.sha256()
    # The sample solution only feeds `arena.check`; editing it must not invalidate model results.
    for f in sorted(p for p in d.rglob("*") if p.is_file() and p.name != "musterloesung.md"):
        h.update(f.relative_to(d).as_posix().encode())
        h.update(f.read_bytes())
    return h.hexdigest()[:12]


def load_task(d: Path) -> Task:
    cfg = tomllib.loads((d / "task.toml").read_text())
    prompt = cfg.get("prompt") or (d / cfg.get("prompt_file", "prompt.md")).read_text()
    for name in cfg.get("attach", []):
        prompt = prompt.replace("{{" + name + "}}", (d / name).read_text())
    images = [d / x for x in cfg.get("images", [])]
    needs = set(cfg.get("needs", []))
    if images:
        needs.add("vision")
    category = cfg["category"]
    if category not in CATEGORIES:
        raise ValueError(f"{d.name}: category muss eine von {sorted(CATEGORIES)} sein")
    chk = cfg["check"]
    return Task(
        id=d.name, category=category, title=cfg["title"], summary=cfg.get("summary", ""),
        level=cfg.get("level", "mittel"), prompt=prompt.strip(), images=images, needs=frozenset(needs),
        max_tokens=int(cfg.get("max_tokens", 8192)), check=CHECKERS[chk["type"]](chk, d),
        check_type=chk["type"], fingerprint=_fingerprint(d), dir=d,
        followups=[{"prompt": f["prompt"].strip(), "when_missing": f.get("when_missing", []),
                    "when_found": f.get("when_found", [])} for f in cfg.get("followups", [])],
    )


def load_tasks(root: Path, only: list[str] | None = None) -> list[Task]:
    dirs = sorted(p for p in root.iterdir() if (p / "task.toml").exists() and not p.name.startswith("_"))
    if only:
        dirs = [p for p in dirs if p.name in only]
    return [load_task(p) for p in dirs]
