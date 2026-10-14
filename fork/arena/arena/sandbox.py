"""Runs model-written Python under bubblewrap: no network, read-only system, 1 GiB address space."""
import glob
import json
import resource
import subprocess
import tempfile
from pathlib import Path

# Imports the answer as module `solution`, then runs every test_* function of tests.py on its own.
HARNESS = r'''
import json, signal, sys, types
def _alarm(*_): raise TimeoutError("Test dauerte länger als %(per_test)d s")
signal.signal(signal.SIGALRM, _alarm)
def emit(d): print("@@RESULT@@" + json.dumps(d)); sys.exit()
mod = types.ModuleType("solution")
sys.modules["solution"] = mod
try:
    signal.alarm(5)
    exec(compile(open("solution.py").read(), "solution.py", "exec"), mod.__dict__)
    signal.alarm(0)
except BaseException as e:
    emit({"load_error": repr(e)[:300]})
ns = {"__name__": "tests"}
exec(compile(open("tests.py").read(), "tests.py", "exec"), ns)
out = {}
for name, fn in list(ns.items()):
    if not (name.startswith("test_") and callable(fn)):
        continue
    try:
        signal.alarm(%(per_test)d)
        fn()
        signal.alarm(0)
        out[name] = None
    except BaseException as e:
        signal.alarm(0)
        out[name] = (type(e).__name__ + ": " + str(e))[:200]
emit({"results": out})
'''


def _limits():
    resource.setrlimit(resource.RLIMIT_AS, (1 << 30, 1 << 30))
    resource.setrlimit(resource.RLIMIT_FSIZE, (16 << 20, 16 << 20))


def bwrap(workdir: str, argv: list[str], timeout: float) -> subprocess.CompletedProcess | None:
    """Runs argv inside workdir (mounted at /work) without network; None on timeout."""
    cmd = [
        "bwrap", "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib64", "/lib64",
        "--symlink", "usr/bin", "/bin", "--ro-bind", "/etc/alternatives", "/etc/alternatives",
    ]
    for cfg in glob.glob("/etc/fpc*.cfg"):
        cmd += ["--ro-bind", cfg, cfg]
    cmd += ["--bind", workdir, "/work", "--chdir", "/work", "--tmpfs", "/tmp", "--proc", "/proc", "--dev", "/dev",
            "--unshare-all", "--die-with-parent", "--new-session", *argv]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, preexec_fn=_limits)
    except subprocess.TimeoutExpired:
        return None


def run_tests(solution: str, tests_py: str, per_test: int = 5, timeout: float = 120.0) -> dict:
    with tempfile.TemporaryDirectory(prefix="arena-") as d:
        Path(d, "solution.py").write_text(solution)
        Path(d, "tests.py").write_text(tests_py)
        Path(d, "harness.py").write_text(HARNESS % {"per_test": per_test})
        p = bwrap(d, ["/usr/bin/python3", "-I", "harness.py"], timeout)
        if p is None:
            return {"error": f"Zeitlimit {timeout:.0f} s überschritten"}
        for line in p.stdout.splitlines():
            if line.startswith("@@RESULT@@"):
                return json.loads(line[len("@@RESULT@@"):])
        return {"error": (p.stderr or p.stdout)[-400:] or f"Exit-Code {p.returncode}"}


def run_pascal(program: str, test_names: list[str], timeout: float = 60.0) -> dict:
    """Compiles program.pas with Free Pascal (Delphi mode) and runs it; lines '@@T name OK|FAIL msg'."""
    with tempfile.TemporaryDirectory(prefix="arena-") as d:
        Path(d, "program.pas").write_text(program)
        p = bwrap(d, ["/usr/bin/fpc", "-Mdelphi", "-O1", "-vew", "-otests", "program.pas"], 120)
        if p is None:
            return {"error": "Kompilieren dauerte zu lange"}
        if p.returncode != 0 or not Path(d, "tests").exists():
            errs = [l for l in p.stdout.splitlines() if "Error" in l or "Fatal" in l]
            return {"compile_error": "\n".join(errs[:4])[:600] or p.stdout[-600:]}
        p = bwrap(d, ["./tests"], timeout)
        if p is None:
            return {"error": f"Programm lief länger als {timeout:.0f} s"}
        res = {n: "kein Ergebnis (Absturz?)" for n in test_names}
        for line in p.stdout.splitlines():
            if line.startswith("@@T "):
                _, name, rest = line.split(" ", 2)
                res[name] = None if rest == "OK" else rest[5:][:200]
        return {"results": res}
