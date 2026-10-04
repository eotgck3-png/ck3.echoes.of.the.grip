"""Tests for docs/tools/check_all.py: requirement detection and skip/pass/fail logic.

Run: python -m unittest discover docs/tools/tests
"""
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import check_all as C  # noqa: E402

PY = sys.executable


class Requirements(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = self.tmp.name
        self.exe = os.path.join(self.dir, "Code.exe")
        open(self.exe, "w").close()
        self.missing = os.path.join(self.dir, "nope")

    def test_present(self):
        env = {"EOTG_CK3_GAME": self.dir, "EOTG_PX_DIR": self.dir,
               "EOTG_VSCODE_EXE": self.exe, "EOTG_TIGER_EXE": self.exe}
        for n in ("game", "px", "vscode", "tiger"):
            self.assertTrue(C.requirement(n, env)[0], n)

    def test_absent(self):
        env = {"EOTG_CK3_GAME": self.missing, "EOTG_PX_DIR": self.missing,
               "EOTG_VSCODE_EXE": self.missing, "EOTG_TIGER_EXE": self.dir}  # a dir, not a file
        for n in ("game", "px", "vscode", "tiger"):
            ok, detail = C.requirement(n, env)
            self.assertFalse(ok, n)
            self.assertTrue(detail)

    def test_unknown(self):
        with self.assertRaises(ValueError):
            C.requirement("nonsense", {})


class RunLogic(unittest.TestCase):
    ENV_NONE = {"EOTG_CK3_GAME": "/nonexistent/game", "EOTG_PX_DIR": "/nonexistent/px",
                "EOTG_VSCODE_EXE": "/nonexistent/code", "EOTG_TIGER_EXE": "/nonexistent/tiger"}

    def test_skip_when_requirement_missing(self):
        r = C.run_check(C.Check("px", [PY, "-c", "print(1)"], needs=("px", "game")),
                        dict(os.environ, **self.ENV_NONE))
        self.assertEqual(r.status, "SKIP")
        self.assertIn(C.SKIP_LOCAL, r.detail)
        self.assertIn("PX Toolkit", r.detail)

    def test_skip_reason(self):
        r = C.run_check(C.Check("qa/show_option.py", skip_reason="interactive tool, needs --key"))
        self.assertEqual((r.status, r.detail), ("SKIP", "skipped: interactive tool, needs --key"))

    def test_pass_fail_and_informational(self):
        ok = C.run_check(C.Check("ok", [PY, "-c", "print('all good')"]))
        self.assertEqual((ok.status, ok.detail), ("PASS", "all good"))
        bad = C.run_check(C.Check("bad", [PY, "-c", "import sys; print('boom'); sys.exit(3)"]))
        self.assertEqual(bad.status, "FAIL")
        self.assertIn("exit 3", bad.detail)
        info = C.run_check(C.Check("tiger", None, run=lambda env: (2, "x\ny"),
                                   informational=True))
        self.assertEqual(info.status, "RAN")

    def test_cannot_start_is_fail(self):
        r = C.run_check(C.Check("ghost", ["/nonexistent/binary/xyz"]))
        self.assertEqual(r.status, "FAIL")
        self.assertIn("could not run", r.detail)

    def test_main_exit_code_and_table(self):
        checks = [C.Check("good", [PY, "-c", "pass"]),
                  C.Check("needs-game", [PY, "-c", "pass"], needs=("game",)),
                  C.Check("fails", [PY, "-c", "import sys; sys.exit(1)"])]
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = C.main([], checks=checks, env=dict(os.environ, **self.ENV_NONE))
        out = buf.getvalue()
        self.assertEqual(rc, 1)
        self.assertIn("summary: 1 pass, 1 fail, 1 skipped, 0 ran", out)
        self.assertIn(C.SKIP_LOCAL, out)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = C.main(["--only", "good", "--only", "needs"], checks=checks,
                        env=dict(os.environ, **self.ENV_NONE))
        self.assertEqual(rc, 0)

    def test_default_checks_cover_tools(self):
        names = [c.name for c in C.default_checks()]
        for n in ("eotg_lint (vs baseline)", "px_vocab_check", "px_lsp_diagnostics", "ck3-tiger",
                  "qa/event_graph.py", "qa/show_option.py"):
            self.assertIn(n, names)
        self.assertNotIn("qa/aug_parse.py", names)
        by = {c.name: c for c in C.default_checks()}
        self.assertEqual(set(by["px_vocab_check"].needs), {"px", "game"})
        self.assertIn("vscode", by["px_lsp_diagnostics"].needs)
        self.assertIsNotNone(by["qa/progression_sim.py"].skip_reason)


class RootAndLogs(unittest.TestCase):
    def test_default_checks_use_root(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "events"))
            by = {c.name: c for c in C.default_checks(d)}
            lint = by["eotg_lint (vs baseline)"]
            self.assertIn(os.path.abspath(d), lint.cmd)
            self.assertEqual(lint.cwd, os.path.abspath(d))
            self.assertEqual(by["qa/event_graph.py"].cmd[-1], os.path.abspath(d))
            self.assertEqual(by["px_vocab_check"].env_extra["EOTG_MOD_ROOT"], os.path.abspath(d))
            # no v1 sources in that checkout -> the port check is skipped, not failed
            self.assertIsNotNone(by["port_religions_1_20 --check"].skip_reason)

    def test_root_must_look_like_a_mod(self):
        with tempfile.TemporaryDirectory() as d, redirect_stdout(io.StringIO()):
            from contextlib import redirect_stderr
            with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
                C.main(["--root", d])

    def test_tiger_log_dir(self):
        with tempfile.TemporaryDirectory() as d:
            path, note = C.tiger_log_path({"EOTG_LOG_DIR": d}, root=C.ROOT)
            self.assertEqual(os.path.dirname(path), d)
            self.assertEqual(note, "")
        path, note = C.tiger_log_path({}, root=C.ROOT)
        self.assertEqual(os.path.dirname(path), tempfile.gettempdir())
        # never inside the repo
        inside = os.path.join(C.ROOT, "docs")
        path, note = C.tiger_log_path({"EOTG_LOG_DIR": inside}, root=C.ROOT)
        self.assertFalse(C._inside(path, C.ROOT))
        self.assertIn("inside a repo", note)


if __name__ == "__main__":
    unittest.main()
