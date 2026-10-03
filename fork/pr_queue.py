"""List upstream PRs that still need a fork decision, and render the decision log."""

import argparse
import json
import pathlib
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
            "| PR | Title | Decision | Reason |", "|---|---|---|---|"]
    for num in sorted(log, key=int, reverse=True):
        e = log[num]
        reason = e["reason"].replace("|", "\\|").replace("\n", " ")
        gpu = " (GPU untested)" if e.get("gpu_untested") else ""
        link = f"[#{num}](https://github.com/{UPSTREAM}/pull/{num})"
        rows.append(f"| {link} | {e['title']} | {e['decision']}{gpu} | {reason} |")
    TABLE.write_text("\n".join(rows) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--render", action="store_true", help="rewrite pr-decisions.md and exit")
    args = ap.parse_args()
    log = load_log()
    if args.render:
        render(log)
        return
    todo = sorted(pending(open_prs(), log), key=lambda p: (p["draft"], -p["number"]))
    for pr in todo[: args.limit]:
        draft = " [draft]" if pr["draft"] else ""
        print(f"{pr['number']}\t{pr['head']['sha'][:12]}\t{pr['user']['login']}\t{pr['title']}{draft}")
    print(f"# {len(todo)} pending")


if __name__ == "__main__":
    main()
