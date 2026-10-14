"""Checkers selected by [check] type in task.toml. Each returns a Check for one model answer."""
import io
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .sandbox import run_pascal, run_tests


@dataclass
class Check:
    passed: bool | None  # None = shown on the site without a verdict (svg_view)
    score: float | None
    detail: str = ""
    artifact: dict | None = None  # e.g. {"svg": "..."}, shown on the site
    found: list | None = None  # names of answer groups that matched (follow-ups key on these)
    missing: list | None = None


def final_answer(text: str) -> str:
    hits = re.findall(r"ANTWORT\s*:\s*(.+)", text, flags=re.IGNORECASE)
    return hits[-1].strip() if hits else text.strip()


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).casefold()
    s = re.sub(r"(?<=\d)[.\s'](?=\d{3}\b)", "", s)  # 4.850 / 4 850 -> 4850
    return re.sub(r"\s+", " ", s)


def answer(cfg: dict, task_dir: Path):
    """Keyword check on the final 'ANTWORT:' line (or the whole answer if there is none).

    [[check.groups]] (name, regex) suits free-text answers: every group is one finding that must match somewhere.
    """
    need_all = [_norm(x) for x in cfg.get("all", [])]
    need_any = [_norm(x) for x in cfg.get("any", [])]
    forbid = [_norm(x) for x in cfg.get("none", [])]
    pattern = cfg.get("regex")
    groups = [(g["name"], re.compile(g["regex"], flags=re.IGNORECASE | re.DOTALL), g.get("must_not", False),
               re.compile(g["unless_before"], flags=re.IGNORECASE) if g.get("unless_before") else None)
              for g in cfg.get("groups", [])]
    final_line = cfg.get("final_line", not groups)

    def check(text: str) -> Check:
        a = _norm(final_answer(text) if final_line else text)
        parts = [(x, x in a) for x in need_all]
        if need_any:
            parts.append(("eins von " + "/".join(need_any), any(x in a for x in need_any)))
        if pattern:
            parts.append((pattern, re.search(pattern, a, flags=re.IGNORECASE) is not None))
        for name, rx, must_not, unless in groups:
            # A negation inside the match or earlier in the same clause ("nicht etwa ..., sondern") excuses it.
            hit = any(not (unless and unless.search(re.split(r"[.,!?;:]", a[max(0, m.start() - 80):m.start()])[-1] + m.group(0)))
                      for m in rx.finditer(a))
            parts.append(("nicht: " + name if must_not else name, hit != must_not))
        bad = [x for x in forbid if x in a]
        score = (sum(ok for _, ok in parts) / len(parts) if parts else 1.0) * (0 if bad else 1)
        missing = [x for x, ok in parts if not ok]
        if groups:
            detail = f"{sum(ok for _, ok in parts)}/{len(parts)} erwartete Punkte gefunden"
        else:
            detail = "Antwort: " + a[:160]
        if missing:
            detail += " | fehlt: " + ", ".join(missing)
        if bad:
            detail += " | verboten: " + ", ".join(bad)
        return Check(score == 1.0, round(score, 3), detail,
                     found=[x for x, ok in parts if ok], missing=missing)

    return check


def code_block(text: str, langs=("python", "py", "python3", "")) -> str | None:
    blocks = re.findall(r"```([a-zA-Z0-9_+-]*)[ \t]*\n(.*?)```", text, flags=re.DOTALL)
    picked = [b for lang, b in blocks if lang.lower() in langs]
    # Models often add a short usage example after the solution; the solution is the longest block.
    return max(picked, key=len) if picked else None


def python_tests(cfg: dict, task_dir: Path):
    """Runs tests.py (test_* functions, `from solution import ...`) against the answer's code block."""
    tests_py = (task_dir / cfg.get("tests", "tests.py")).read_text()
    forbidden = cfg.get("forbidden", [])
    per_test = int(cfg.get("per_test_seconds", 5))

    def check(text: str) -> Check:
        src = code_block(text)
        if src is None:
            return Check(False, 0.0, "kein Python-Codeblock in der Antwort")
        for pat in forbidden:
            if re.search(pat, src):
                return Check(False, 0.0, f"verbotenes Muster im Code: {pat}")
        r = run_tests(src, tests_py, per_test=per_test)
        if "error" in r:
            return Check(False, 0.0, r["error"])
        if "load_error" in r:
            return Check(False, 0.0, "Code lädt nicht: " + r["load_error"])
        res = r["results"]
        if not res:
            return Check(False, 0.0, "tests.py enthält keine test_*-Funktionen")
        fails = {k: v for k, v in res.items() if v is not None}
        ok = len(res) - len(fails)
        detail = f"{ok}/{len(res)} Tests bestanden"
        if fails:
            detail += "; " + "; ".join(f"{k}: {v}" for k, v in list(fails.items())[:3])
        return Check(not fails, round(ok / len(res), 3), detail)

    return check


def extract_svg(text: str) -> str | None:
    m = re.findall(r"<svg\b.*?</svg>", text, flags=re.DOTALL | re.IGNORECASE)
    return m[-1] if m else None


def rasterize(svg: str, w: int, h: int) -> np.ndarray:
    import cairosvg
    from PIL import Image

    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=w, output_height=h, unsafe=False)
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    return np.asarray(Image.alpha_composite(bg, im).convert("RGB"), dtype=np.int16)


def svg_reference(cfg: dict, task_dir: Path):
    """Renders the answer's SVG and compares it pixel by pixel with reference.svg."""
    ref = (task_dir / cfg.get("reference", "reference.svg")).read_text()
    w, h = int(cfg["width"]), int(cfg["height"])
    need = float(cfg.get("min_match", 0.98))
    tol = int(cfg.get("color_tolerance", 48))
    ref_px = rasterize(ref, w, h)
    # Anti-aliased borders differ between equivalent shapes; only flat areas (2 px off any edge) count.
    edge = np.zeros(ref_px.shape[:2], dtype=bool)
    edge[:, 1:] |= (ref_px[:, 1:] != ref_px[:, :-1]).any(-1)
    edge[1:, :] |= (ref_px[1:, :] != ref_px[:-1, :]).any(-1)
    for _ in range(2):
        e = edge.copy()
        e[1:] |= edge[:-1]; e[:-1] |= edge[1:]; e[:, 1:] |= edge[:, :-1]; e[:, :-1] |= edge[:, 1:]
        edge = e
    mask = ~edge

    def check(text: str) -> Check:
        svg = extract_svg(text)
        if svg is None:
            return Check(False, 0.0, "kein <svg> in der Antwort")
        try:
            px = rasterize(svg, w, h)
        except Exception as e:
            return Check(False, 0.0, f"SVG nicht renderbar: {e!r}"[:200], {"svg": svg})
        ok = (np.abs(px - ref_px).max(-1) <= tol) & mask
        score = float(ok.sum() / mask.sum())
        return Check(score >= need, round(score, 4),
                     f"{score:.1%} der Flächenpixel wie Referenz (nötig {need:.0%})", {"svg": svg})

    return check


PASCAL_UNITS = {"sysutils", "math", "classes", "types", "strutils", "dateutils"}

PASCAL_HELPERS = """
type
  EArenaCheck = class(Exception);
  TArenaTest = procedure;

procedure Check(Cond: Boolean; const Msg: string);
begin
  if not Cond then raise EArenaCheck.Create(Msg);
end;

procedure CheckNear(Actual, Expected, Tol: Double; const Msg: string);
begin
  if IsNan(Actual) or (Abs(Actual - Expected) > Tol) then
    raise EArenaCheck.Create(Format('%s: erwartet %.4f, erhalten %.4f', [Msg, Expected, Actual]));
end;

procedure RunArenaTest(const Name: string; P: TArenaTest);
begin
  try
    P;
    WriteLn('@@T ', Name, ' OK');
  except
    on E: Exception do WriteLn('@@T ', Name, ' FAIL ', E.ClassName, ': ', E.Message);
  end;
end;
"""


def pascal_program(code: str, tests: str, names: list[str]) -> str:
    """Turns a Delphi answer (bare routines, a unit or a console program) into one test program."""
    s = re.sub(r"\{\$APPTYPE[^}]*\}", "", code, flags=re.IGNORECASE)
    units = []

    def grab(m):
        units.extend(u.strip().split(" in ")[0].strip() for u in m.group(1).split(","))
        return ""

    s = re.sub(r"\buses\b([^;]*);", grab, s, flags=re.IGNORECASE)
    if re.search(r"^\s*unit\s+[\w.]+\s*;", s, flags=re.IGNORECASE | re.MULTILINE):
        s = re.sub(r"^\s*unit\s+[\w.]+\s*;", "", s, count=1, flags=re.IGNORECASE | re.MULTILINE)
        # The interface section only repeats the headers that implementation defines again.
        s = re.sub(r"\binterface\b.*?\bimplementation\b", "", s, count=1, flags=re.IGNORECASE | re.DOTALL)
        s = re.sub(r"\b(initialization|finalization)\b.*$", "", s, flags=re.IGNORECASE | re.DOTALL)
        s = re.sub(r"\bend\s*\.\s*$", "", s.rstrip(), flags=re.IGNORECASE)
    elif re.search(r"^\s*program\s+[\w.]+\s*;", s, flags=re.IGNORECASE | re.MULTILINE):
        s = re.sub(r"^\s*program\s+[\w.]+\s*;", "", s, count=1, flags=re.IGNORECASE | re.MULTILINE)
        mains = [m.start() for m in re.finditer(r"^begin\b", s, flags=re.IGNORECASE | re.MULTILINE)]
        if mains:
            s = s[:mains[-1]]
    keep = ["SysUtils", "Math"]
    for u in units:
        base = re.sub(r"^(System|Vcl|Winapi)\.", "", u, flags=re.IGNORECASE)
        if base.lower() in PASCAL_UNITS and base.lower() not in {k.lower() for k in keep}:
            keep.append(base)
    calls = "".join(f"  RunArenaTest('{n}', @{n});\n" for n in names)
    return (f"program arena_tests;\n{{$mode delphi}}{{$H+}}\nuses {', '.join(keep)};\n\n{s.strip()}\n\n"
            f"{PASCAL_HELPERS}\n{tests}\n\nbegin\n{calls}end.\n")


def pascal_tests(cfg: dict, task_dir: Path):
    """Compiles the answer's Delphi code with Free Pascal (-Mdelphi) together with the Test_* procedures of tests.pas."""
    tests = (task_dir / cfg.get("tests", "tests.pas")).read_text()
    names = re.findall(r"^\s*procedure\s+(Test_\w+)\s*;", tests, flags=re.IGNORECASE | re.MULTILINE)
    forbidden = cfg.get("forbidden", [])

    def check(text: str) -> Check:
        src = code_block(text, ("delphi", "pascal", "pas", "objectpascal", "object-pascal", "dpr", ""))
        if src is None:
            return Check(False, 0.0, "kein Delphi-/Pascal-Codeblock in der Antwort")
        for pat in forbidden:
            if re.search(pat, src, flags=re.IGNORECASE):
                return Check(False, 0.0, f"verbotenes Muster im Code: {pat}")
        r = run_pascal(pascal_program(src, tests, names), names)
        if "error" in r:
            return Check(False, 0.0, r["error"])
        if "compile_error" in r:
            return Check(False, 0.0, "kompiliert nicht: " + r["compile_error"])
        res = r["results"]
        if not res:
            return Check(False, 0.0, "tests.pas enthält keine Test_*-Prozeduren")
        fails = {k: v for k, v in res.items() if v is not None}
        ok = len(res) - len(fails)
        detail = f"{ok}/{len(res)} Tests bestanden"
        if fails:
            detail += "; " + "; ".join(f"{k}: {v}" for k, v in list(fails.items())[:3])
        return Check(not fails, round(ok / len(res), 3), detail)

    return check


def svg_view(cfg: dict, task_dir: Path):
    """No verdict: renders the answer's SVG for the site and notes a few facts (text present, background)."""
    expect_text = cfg.get("expect_text", [])

    def check(text: str) -> Check:
        svg = extract_svg(text)
        if svg is None:
            return Check(False, 0.0, "kein <svg> in der Antwort")
        try:
            import cairosvg
            from PIL import Image

            im = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=256, unsafe=False))).convert("RGBA")
        except Exception as e:
            return Check(False, 0.0, f"SVG nicht renderbar: {e!r}"[:200], {"svg": svg})
        px = np.asarray(im)
        border = np.concatenate([px[0], px[-1], px[:, 0], px[:, -1]])
        if (border[:, 3] == 0).all():
            bg = "transparent"
        elif (border[:, 3] == 255).all() and (np.abs(border[:, :3].astype(int) - border[0, :3]).max() <= 8):
            bg = "einfarbig #%02x%02x%02x" % tuple(border[0, :3])
        else:
            bg = "uneinheitlich (Motiv reicht an den Rand oder mehrfarbig)"
        notes = [f"Hintergrund {bg}"]
        src = re.sub(r"\s+", " ", svg).casefold()
        for t in expect_text:
            notes.append(f"Text '{t}' {'gefunden' if t.casefold() in src else 'nicht als Text im SVG'}")
        return Check(None, None, "ohne Bewertung - " + "; ".join(notes), {"svg": svg})

    return check


CHECKERS = {"svg_view": svg_view, "pascal_tests": pascal_tests, "answer": answer, "python_tests": python_tests, "svg_reference": svg_reference}
