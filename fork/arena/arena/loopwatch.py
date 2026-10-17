"""Watch a running Prüfstand for answers that loop: reads the ARENA_LIVE file every minute.

    ARENA_LIVE=results/live.txt python -m arena.run ...      # in one shell
    python -m arena.loopwatch results/live.txt                # in another

Prints a line only when the tail of the text currently streaming repeats itself.
"""
import json
import sys
import time
import zlib

TAIL = 4000


def looping(text: str) -> str | None:
    """Why the tail of text looks like a loop, or None."""
    tail = text[-TAIL:]
    if len(tail) < 1500:
        return None
    # the last 150 characters occur again and again in the tail
    probe = tail[-150:]
    n = tail.count(probe)
    if n >= 3:
        return f"letzte 150 Zeichen {n}x im Ende"
    ratio = len(zlib.compress(tail.encode())) / len(tail.encode())
    if ratio < 0.12:
        return f"Ende komprimiert auf {ratio:.0%}"
    return None


def check(path: str) -> str | None:
    try:
        head, _, rest = open(path, encoding="utf-8", errors="replace").read().partition("\n")
        meta = json.loads(head)
    except (OSError, ValueError):
        return None
    if meta.get("done"):
        return None
    reasoning, _, content = rest.partition("\n=====ANTWORT=====\n")
    part, text = ("Antwort", content) if meta.get("content_chars") else ("Denkphase", reasoning)
    why = looping(text)
    if not why:
        return None
    snippet = " ".join(text[-160:].split())
    return (f"LOOP? {meta['model']} {part} nach {meta['elapsed_s']:.0f} s "
            f"({meta['reasoning_chars']}+{meta['content_chars']} Z.): {why} | ...{snippet}")


def main():
    path = sys.argv[1]
    every = float(sys.argv[2]) if len(sys.argv) > 2 else 60
    while True:
        msg = check(path)
        if msg:
            print(msg, flush=True)
        time.sleep(every)


if __name__ == "__main__":
    main()
