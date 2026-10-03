"""List upstream PRs that still need a fork decision, and render the decision log."""

import argparse
import json
import pathlib
import subprocess
import urllib.request

UPSTREAM = "FlashML-org/FreeToken"
HERE = pathlib.Path(__file__).parent
LOG = HERE / "pr-decisions.json"
TABLE = HERE / "pr-decisions.md"
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
    for pr in prs:
        entry = log.get(str(pr["number"]))
        if entry is None:
            yield pr
        elif entry["decision"] in RECHECK_ON_NEW_HEAD and entry.get("head_sha") != pr["head"]["sha"]:
            yield pr


def render(log):
    rows = ["# Upstream PR decisions", "",
            "Generated from `pr-decisions.json` by `python3 fork/pr_queue.py --render`.", "",
            "| PR | Title | Authors | Decision | Reason |", "|---|---|---|---|---|"]
    for num in sorted(log, key=int, reverse=True):
        e = log[num]
        reason = e["reason"].replace("|", "\\|").replace("\n", " ")
        gpu = " (GPU untested)" if e.get("gpu_untested") else ""
        link = f"[#{num}](https://github.com/{UPSTREAM}/pull/{num})"
        # names only: the emails stay in the JSON for Co-authored-by trailers
        authors = ", ".join(a.split(" <")[0] for a in e.get("authors", []))
        by = f" by #{e['superseded_by']}" if e.get("superseded_by") else ""
        rows.append(f"| {link} | {e['title']} | {authors} | {e['decision']}{by}{gpu} | {reason} |")
    TABLE.write_text("\n".join(rows) + "\n")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def overlap(num, log):
    """What may already cover PR ``num``: main's commits since its base and other PRs on its files."""
    ref = f"refs/pr-heads/{num}"
    # refs/pr-heads/ stays out of the branch list
    if subprocess.run(["git", "fetch", "-q", "upstream", f"+refs/pull/{num}/head:{ref}"]).returncode:
        raise SystemExit(f"#{num} has no upstream PR head (an issue number?)")
    open_nums = [pr["number"] for pr in open_prs() if pr["number"] != num]
    git("fetch", "-q", "upstream", *[f"+refs/pull/{n}/head:refs/pr-heads/{n}" for n in open_nums])
    base = git("merge-base", "main", ref).strip()
    files = set(git("diff", "--name-only", f"{base}..{ref}").split())
    print(f"# PR #{num}: {len(files)} files, base {base[:12]}")
    if not files:
        print("nothing left to apply: main already contains this PR's head")
        return
    # main moved on after the PR branched: a fix or refactor there may make it obsolete
    print("## main since the PR's base, on its files")
    print(git("log", "--oneline", f"{base}..main", "--", *files) or "(none)\n", end="")
    print("## other open PRs touching the same files")
    hits, decided = [], []
    for n in open_nums:
        shared = files & set(git("diff", "--name-only", f"main...refs/pr-heads/{n}").split())
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
