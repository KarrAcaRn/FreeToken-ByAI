"""List upstream PRs that still need a fork decision, and render the decision log."""

import argparse
import json
import pathlib
import subprocess
import urllib.request

UPSTREAM = "FlashML-org/FreeToken"
# The fork's integration branch: main mirrors upstream, adopted PRs land here.
WORK = "next"
HERE = pathlib.Path(__file__).parent
LOG = HERE / "pr-decisions.json"
TABLE = HERE / "pr-decisions.md"
README = HERE.parent / "README.md"
FORK = "KarrAcaRn/FreeToken-ByAI"
ADOPTED = {"adopted": "Adopted", "adopted-with-fixups": "Adopted + fixup", "reimplemented": "Reimplemented", "own": "Our own PR"}
NOT_ADOPTED = {"superseded": "Superseded", "obsolete": "Obsolete", "rejected": "Rejected",
               "deferred": "Deferred", "feature": "Feature, later"}
# A changed head on a deferred PR means the blocker may be gone.
RECHECK_ON_NEW_HEAD = {"deferred"}


def open_prs():
    prs, page = [], 1
    while True:
        url = f"https://api.github.com/repos/{UPSTREAM}/pulls?state=open&per_page=100&page={page}"
        with urllib.request.urlopen(url) as resp:
            batch = json.load(resp)
        prs += batch
        if len(batch) < 100:
            return prs
        page += 1


def load_log():
    return json.loads(LOG.read_text()) if LOG.exists() else {}


def pending(prs, log):
    """Undecided PRs, deferred ones whose head moved or whose ``revisit_with`` PR got a decision,
    and -- once nothing else is left -- the PRs deferred with ``revisit: "after-queue"``."""
    todo, last = [], []
    for pr in prs:
        entry = log.get(str(pr["number"]))
        if entry is None:
            todo.append(pr)
        elif entry.get("revisit") == "after-queue":
            last.append(pr)
        # stacked on another PR: review once that one is decided
        elif entry["decision"] == "deferred" and str(entry.get("revisit_with")) in log:
            todo.append(pr)
        # the log keeps a 12-char head; GitHub reports the full sha
        elif entry["decision"] in RECHECK_ON_NEW_HEAD and not pr["head"]["sha"].startswith(entry.get("head_sha", "")):
            todo.append(pr)
    return todo or last


def render(log):
    rows = ["# Upstream PR decisions", "",
            "Generated from `pr-decisions.json` by `python3 fork/pr_queue.py --render`.", "",
            "| PR | Title | Authors | Decision | Reason |", "|---|---|---|---|---|"]
    for num in sorted(log, key=int, reverse=True):
        e = log[num]
        reason = e["reason"].replace("|", "\\|").replace("\n", " ")
        gpu = " (GPU untested)" if e.get("gpu_untested") else ""
        gpu += " (revisit after the queue)" if e.get("revisit") == "after-queue" else ""
        gpu += f" (revisit with #{e['revisit_with']})" if e.get("revisit_with") else ""
        link = f"[#{num}](https://github.com/{UPSTREAM}/pull/{num})"
        # names only: the emails stay in the JSON for Co-authored-by trailers
        authors = ", ".join(a.split(" <")[0] for a in e.get("authors", []))
        by = f" by #{e['superseded_by']}" if e.get("superseded_by") else ""
        rows.append(f"| {link} | {e['title']} | {authors} | {e['decision']}{by}{gpu} | {reason} |")
    TABLE.write_text("\n".join(rows) + "\n")
    render_readme(log)


def _is_fix(title: str) -> bool:
    import re

    head = re.sub(r"^(\[[^\]]*\]\s*)+", "", title).strip().lower()
    return head.startswith("fix")


def _short(e: dict) -> str:
    text = e.get("summary") or e["reason"].split(". ")[0]
    return text.replace("|", "/").replace("\n", " ")


def _followup(e: dict) -> str:
    def link(h):
        return f"[{h}](https://github.com/{FORK}/commit/{h})"

    parts = []
    commits = [c for c in e.get("commits", []) if c and " " not in c]
    if e["decision"] == "adopted-with-fixups":
        note = e.get("fixup") or "our fixup"
        parts.append(f"{note} ({', '.join(link(c) for c in commits[1:]) or 'see log'})")
    elif e["decision"] == "reimplemented":
        parts.append(f"{e.get('fixup') or 'our version'} ({', '.join(link(c) for c in commits)})")
    if e.get("upstream_followup"):
        parts.append(e["upstream_followup"])
    return "; ".join(parts).replace("|", "/")


def render_readme(log):
    """Fill the generated blocks of README.md between their markers."""
    if not README.exists():
        return
    text = README.read_text()

    def block(name: str, body: str) -> None:
        nonlocal text
        start, end = f"<!-- fork:{name}:start -->", f"<!-- fork:{name}:end -->"
        if start in text and end in text:
            head, rest = text.split(start, 1)
            text = head + start + "\n" + body + "\n" + end + rest.split(end, 1)[1]

    def pr(num):
        return f"[#{num}](https://github.com/{UPSTREAM}/pull/{num})"

    entries = sorted(log.values(), key=lambda e: -int(e["number"]))
    not_adopted = [e for e in entries if e["decision"] in NOT_ADOPTED]
    block("not-adopted", ", ".join(pr(e["number"]) for e in sorted(not_adopted, key=lambda e: int(e["number"]))))

    def table(rows, with_followup):
        head = "| PR | Title | Status | Why |" + (" Our follow-up |" if with_followup else "")
        sep = "|---|---|---|---|" + ("---|" if with_followup else "")
        out = [head, sep]
        for e in rows:
            label = ADOPTED.get(e["decision"]) or NOT_ADOPTED.get(e["decision"], e["decision"])
            title = e["title"].replace("|", "/")
            line = f"| {pr(e['number'])} | {title} | {label} | {_short(e)} |"
            out.append(line + (f" {_followup(e)} |" if with_followup else ""))
        return "\n".join(out)

    adopted = [e for e in entries if e["decision"] in ADOPTED]
    fixes = [e for e in adopted if _is_fix(e["title"])]
    improvements = [e for e in adopted if not _is_fix(e["title"])]
    order = {"rejected": 0, "superseded": 1, "obsolete": 2, "feature": 3, "deferred": 4}
    not_adopted.sort(key=lambda e: (order[e["decision"]], -int(e["number"])))
    body = "\n\n".join([
        f"### Bug fixes we adopted ({len(fixes)})", table(fixes, True),
        f"### Improvements we adopted ({len(improvements)})", table(improvements, True),
        f"### Not adopted ({len(not_adopted)})", table(not_adopted, False),
    ])
    block("pr-table", body)
    README.write_text(text)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def overlap(num, log):
    """What may already cover PR ``num``: the work branch's commits since its base and other PRs on its files."""
    ref = f"refs/pr-heads/{num}"
    # refs/pr-heads/ stays out of the branch list
    if subprocess.run(["git", "fetch", "-q", "upstream", f"+refs/pull/{num}/head:{ref}"]).returncode:
        raise SystemExit(f"#{num} has no upstream PR head (an issue number?)")
    open_nums = [pr["number"] for pr in open_prs() if pr["number"] != num]
    git("fetch", "-q", "upstream", *[f"+refs/pull/{n}/head:refs/pr-heads/{n}" for n in open_nums])
    base = git("merge-base", WORK, ref).strip()
    files = set(git("diff", "--name-only", f"{base}..{ref}").split())
    print(f"# PR #{num}: {len(files)} files, base {base[:12]}")
    if not files:
        print(f"nothing left to apply: {WORK} already contains this PR's head")
        return
    # the work branch moved on after the PR branched: a fix or refactor there may make it obsolete
    print(f"## {WORK} since the PR's base, on its files")
    print(git("log", "--oneline", f"{base}..{WORK}", "--", *files) or "(none)\n", end="")
    print("## other open PRs touching the same files")
    hits, decided = [], []
    for n in open_nums:
        shared = files & set(git("diff", "--name-only", f"{WORK}...refs/pr-heads/{n}").split())
        if not shared:
            continue
        if str(n) in log:
            decided.append(f"#{n} {log[str(n)]['decision']}")
        else:
            hits.append((len(shared), n, shared))
    # most shared files first: a PR touching only a hub file like args.py is rarely a duplicate
    for count, n, shared in sorted(hits, key=lambda h: (-h[0], -h[1])):
        print(f"#{n} [{count}]: {', '.join(sorted(shared))}")
    if decided:
        print(f"## already decided: {', '.join(decided)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--render", action="store_true", help="rewrite pr-decisions.md and exit")
    ap.add_argument("--overlap", type=int, metavar="N", help="show what may make PR N duplicate or obsolete")
    args = ap.parse_args()
    log = load_log()
    if args.render:
        render(log)
        return
    if args.overlap is not None:
        overlap(args.overlap, log)
        return
    todo = sorted(pending(open_prs(), log), key=lambda p: (p["draft"], -p["number"]))
    for pr in todo[: args.limit]:
        draft = " [draft]" if pr["draft"] else ""
        print(f"{pr['number']}\t{pr['head']['sha'][:12]}\t{pr['user']['login']}\t{pr['title']}{draft}")
    print(f"# {len(todo)} pending")


if __name__ == "__main__":
    main()
