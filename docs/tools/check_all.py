"""Run every repo check that can run here, skip the rest, print one summary table.

    python docs/tools/check_all.py [--only NAME ...] [--verbose] [--list]

Runs, from the repo root:
  - eotg_lint against docs/tools/eotg_lint_baseline.json
  - the docs/tools unit tests
  - port_religions_1_20 --check (staged 1.20 religion output is current)
  - docs/tools/qa/*.py analysis scripts (those that need no arguments)
  - px_vocab_check.py                     needs the PX Toolkit + the game install
  - px_lsp_diagnostics.js                 needs VS Code (+ PX Toolkit + game)
  - px_lsp event graph -> px_event_report needs VS Code (+ PX Toolkit + game)
  - ck3-tiger                             needs Tiger + the game install
Anything whose requirement is missing prints "skipped: needs local install".

Local paths default to the owner's machine (see CLAUDE.md) and can be overridden:
  EOTG_CK3_GAME   game folder         (default D:/SteamLibrary/steamapps/common/Crusader Kings III/game)
  EOTG_PX_DIR     PX extension folder (default newest ~/.vscode/extensions/jdeffner.px-toolkit-*)
  EOTG_VSCODE_EXE VS Code executable  (default C:/Users/river/AppData/Local/Programs/Microsoft VS Code/Code.exe)
  EOTG_TIGER_EXE  ck3-tiger           (default C:/Users/river/tools/ck3-tiger-windows-v1.17.0/ck3-tiger.exe)
Exit status 1 when any check FAILs; skips never fail. Standard library only.
"""
import argparse
import glob
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PY = sys.executable or "python"

DEFAULTS = {
    "EOTG_CK3_GAME": "D:/SteamLibrary/steamapps/common/Crusader Kings III/game",
    "EOTG_VSCODE_EXE": "C:/Users/river/AppData/Local/Programs/Microsoft VS Code/Code.exe",
    "EOTG_TIGER_EXE": "C:/Users/river/tools/ck3-tiger-windows-v1.17.0/ck3-tiger.exe",
}
# qa scripts that are libraries or need arguments; never run unattended
QA_MODULES = {"aug_parse.py"}
QA_NEEDS_ARGS = {"show_option.py": "needs --key", "option_ai_weights.py": "needs --prefix",
                 "progression_sim.py": "needs weight arguments"}
SKIP_LOCAL = "skipped: needs local install"


# ------------------------------------------------------------ requirements
def _env(env, name):
    v = env.get(name)
    return v if v else DEFAULTS.get(name)


def find_px(env):
    d = env.get("EOTG_PX_DIR")
    if d:
        return d if os.path.isdir(d) else None
    hits = sorted(glob.glob(os.path.join(os.path.expanduser("~"), ".vscode", "extensions",
                                         "jdeffner.px-toolkit-*")))
    return hits[-1] if hits else None


def requirement(name, env=None):
    """(ok, detail) for one requirement: game, px, vscode, tiger."""
    env = os.environ if env is None else env
    if name == "game":
        p = _env(env, "EOTG_CK3_GAME")
        return (bool(p) and os.path.isdir(p), "game install (%s)" % p)
    if name == "px":
        p = find_px(env)
        return (p is not None, "PX Toolkit (%s)" % (p or "~/.vscode/extensions/jdeffner.px-toolkit-*"))
    if name == "vscode":
        p = _env(env, "EOTG_VSCODE_EXE")
        return (bool(p) and os.path.isfile(p), "VS Code (%s)" % p)
    if name == "tiger":
        p = _env(env, "EOTG_TIGER_EXE")
        return (bool(p) and os.path.isfile(p), "ck3-tiger (%s)" % p)
    raise ValueError("unknown requirement %r" % name)


# ------------------------------------------------------------ checks
class Check:
    def __init__(self, name, cmd=None, needs=(), skip_reason=None, run=None, env_extra=None,
                 informational=False):
        self.name = name
        self.cmd = cmd              # list[str], run with cwd=ROOT
        self.needs = tuple(needs)
        self.skip_reason = skip_reason
        self.run_fn = run           # callable(env) -> (rc, output), instead of cmd
        self.env_extra = env_extra or {}
        self.informational = informational   # ran, but the exit code is not a verdict


class Result:
    def __init__(self, name, status, detail, seconds=0.0, output=""):
        self.name = name
        self.status = status        # PASS | FAIL | SKIP | RAN
        self.detail = detail
        self.seconds = seconds
        self.output = output


def _last_line(text):
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    return lines[-1][:110] if lines else ""


def run_check(check, env=None, root=ROOT):
    env = dict(os.environ if env is None else env)
    if check.skip_reason:
        return Result(check.name, "SKIP", "skipped: " + check.skip_reason)
    missing = [requirement(n, env)[1] for n in check.needs if not requirement(n, env)[0]]
    if missing:
        return Result(check.name, "SKIP", "%s: %s" % (SKIP_LOCAL, "; ".join(missing)))
    env.update(check.env_extra)
    t = time.time()
    try:
        if check.run_fn:
            rc, out = check.run_fn(env)
        else:
            p = subprocess.run(check.cmd, cwd=root, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, timeout=1800)
            rc, out = p.returncode, p.stdout.decode("utf-8", errors="replace")
    except (OSError, subprocess.SubprocessError) as e:
        return Result(check.name, "FAIL", "could not run: %s" % e, time.time() - t)
    secs = time.time() - t
    if check.informational:
        return Result(check.name, "RAN", "exit %d; %s" % (rc, _last_line(out)), secs, out)
    return Result(check.name, "PASS" if rc == 0 else "FAIL",
                  ("exit %d; " % rc if rc else "") + _last_line(out), secs, out)


def _px_event_report(env):
    exe = _env(env, "EOTG_VSCODE_EXE")
    with tempfile.TemporaryDirectory() as out:
        e = dict(env, ELECTRON_RUN_AS_NODE="1")
        p = subprocess.run([exe, os.path.join("docs", "tools", "px_lsp_diagnostics.js"), "events",
                            "--request=eventGraph", "--request=locCoverage", "--out=" + out],
                           cwd=ROOT, env=e, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=1800)
        if not os.path.exists(os.path.join(out, "px_eventGraph.json")):
            return 1, p.stdout.decode("utf-8", errors="replace") + "\nno px_eventGraph.json written"
        q = subprocess.run([PY, os.path.join("docs", "tools", "px_event_report.py"), out],
                           cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return q.returncode, q.stdout.decode("utf-8", errors="replace")


def _tiger(env):
    exe = _env(env, "EOTG_TIGER_EXE")
    log = os.path.join(tempfile.gettempdir(), "eotg_tiger_check_all.log")
    p = subprocess.run([exe, "--game", _env(env, "EOTG_CK3_GAME"), "echoes_of_the_grip.mod"],
                       cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       timeout=3600)
    out = p.stdout.decode("utf-8", errors="replace")
    with open(log, "w", encoding="utf-8") as fh:
        fh.write(out)
    return p.returncode, "%s\nlog: %s (triage against CLAUDE.md known-benign list)" % (out, log)


def default_checks(root=ROOT):
    t = os.path.join("docs", "tools")
    checks = [
        Check("eotg_lint (vs baseline)",
              [PY, os.path.join(t, "eotg_lint.py"), "--quiet",
               "--baseline", os.path.join(t, "eotg_lint_baseline.json")]),
        Check("unit tests (docs/tools/tests)",
              [PY, "-m", "unittest", "discover", "-s", os.path.join(t, "tests")]),
        Check("port_religions_1_20 --check",
              [PY, os.path.join(t, "port_religions_1_20.py"), "--check"]),
    ]
    for f in sorted(glob.glob(os.path.join(root, t, "qa", "*.py"))):
        base = os.path.basename(f)
        if base in QA_MODULES:
            continue
        name = "qa/" + base
        if base in QA_NEEDS_ARGS:
            checks.append(Check(name, skip_reason="interactive tool, " + QA_NEEDS_ARGS[base]))
        else:
            checks.append(Check(name, [PY, os.path.join(t, "qa", base), "."]))
    checks += [
        Check("px_vocab_check", [PY, os.path.join(t, "px_vocab_check.py"), "common", "events"],
              needs=("px", "game")),
        Check("px_lsp_diagnostics", None, needs=("vscode", "px", "game"),
              run=lambda env: _run_simple(
                  [_env(env, "EOTG_VSCODE_EXE"), os.path.join(t, "px_lsp_diagnostics.js"),
                   "common", "events", "localization"], dict(env, ELECTRON_RUN_AS_NODE="1"))),
        Check("px_event_report (via px_lsp)", None, needs=("vscode", "px", "game"),
              run=_px_event_report),
        Check("ck3-tiger", None, needs=("tiger", "game"), run=_tiger, informational=True),
    ]
    return checks


def _run_simple(cmd, env):
    p = subprocess.run(cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, timeout=1800)
    return p.returncode, p.stdout.decode("utf-8", errors="replace")


def format_table(results):
    w = max([len(r.name) for r in results] + [5])
    lines = ["%-*s  %-4s  %6s  %s" % (w, "check", "stat", "secs", "detail"),
             "%s  %s  %s  %s" % ("-" * w, "-" * 4, "-" * 6, "-" * 40)]
    for r in results:
        lines.append("%-*s  %-4s  %6.1f  %s" % (w, r.name, r.status, r.seconds, r.detail))
    counts = {s: sum(1 for r in results if r.status == s) for s in ("PASS", "FAIL", "SKIP", "RAN")}
    lines.append("")
    lines.append("summary: %(PASS)d pass, %(FAIL)d fail, %(SKIP)d skipped, %(RAN)d ran "
                 "(informational)" % counts)
    return "\n".join(lines)


def main(argv=None, checks=None, env=None):
    ap = argparse.ArgumentParser(description="Run all repo checks; skip what needs a local install.")
    ap.add_argument("--only", action="append", default=[],
                    help="run only checks whose name contains this text (repeatable)")
    ap.add_argument("--list", action="store_true", help="list checks and requirements, run nothing")
    ap.add_argument("--verbose", action="store_true", help="print each check's full output")
    args = ap.parse_args(argv)
    checks = default_checks() if checks is None else checks
    if args.only:
        checks = [c for c in checks if any(o in c.name for o in args.only)]
    if args.list:
        for c in checks:
            print("%-32s needs: %s" % (c.name, ", ".join(c.needs) or "-"))
        return 0
    results = []
    for c in checks:
        r = run_check(c, env)
        results.append(r)
        if args.verbose and r.output:
            print("=== %s ===\n%s" % (r.name, r.output.rstrip()))
    print(format_table(results))
    return 1 if any(r.status == "FAIL" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
