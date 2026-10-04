"""FIX 8: every printing CLI survives a cp1252 console (the owner's Windows default).

Each CLI is run in a subprocess with PYTHONIOENCODING=cp1252 against a small
fixture mod whose output contains non-ASCII characters (arrows, section signs).
Run: python -m unittest discover docs/tools/tests
"""
import io
import os
import subprocess
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _testutil import rmtree, tempdir  # noqa: E402,F401
import pdx_parse as P  # noqa: E402

FILES = {
    "events/eotg_x.txt": "namespace = eotg_x\n"
                         "eotg_x.1 = { title = eotg_x.1.t option = { name = eotg_x.1.a "
                         "trigger_event = eotg_x.2 } }\n"
                         "eotg_x.2 = { title = eotg_x.2.t trigger = { exists = scope:eotg_v } "
                         "option = { name = eotg_x.2.a } }\n",
    "common/decisions/eotg_d.txt": "eotg_decision_x = { effect = { trigger_event = eotg_x.1 } }\n",
    "localization/english/eotg_x_l_english.yml":
        "﻿l_english:\n eotg_x.1.t:0 \"First § → sign\"\n eotg_x.1.a:0 \"A\"\n"
        " eotg_x.2.t:0 \"Second\"\n eotg_x.2.a:0 \"B\"\n"
        " eotg_decision_x:0 \"X\"\n eotg_decision_x_desc:0 \"X — dash\"\n",
    # no BOM: an L003 finding whose path holds a non-ASCII character
    "localization/english/eotg_\u2192_l_english.yml": "l_english:\n",
    "docs/specs/cybernetics_v2_x.md": "# X\n\n### 3.1 New\n\n| Type | Key |\n|---|---|\n"
                                      "| event | `eotg_x.1` → first |\n| event | `eotg_x.9` |\n",
    "OLD PROJECT VERSION/common/religion/religion_types/eotg_r.txt":
        "eotg_religion_x = { family = eotg_rf_x faiths = { eotg_faith_x = { color = { 1 1 1 } } } }\n",
}


class Cp1252Console(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # every absolute path a tool prints holds a non-ASCII character
        cls.root = tempfile.mkdtemp(prefix="eotg_console_\u2192_")
        for rel, text in FILES.items():
            p = os.path.join(cls.root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(text)

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.root)

    def run_cli(self, *args):
        env = dict(os.environ, PYTHONIOENCODING="cp1252")
        p = subprocess.run([sys.executable] + list(args), cwd=self.root, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
        err = p.stderr.decode("utf-8", "replace")
        self.assertNotIn("UnicodeEncodeError", err, err)
        self.assertNotIn("Traceback", err, err)
        return p.returncode, p.stdout.decode("utf-8", "replace")

    def test_gen_test_recipes_event(self):
        rc, out = self.run_cli(os.path.join(TOOLS, "gen_test_recipes.py"), "--root", self.root,
                               "--event", "eotg_x.2")
        self.assertEqual(rc, 0)
        self.assertIn("live route", out)
        self.assertIn("→", out)       # the arrow survives as UTF-8

    def test_gen_test_recipes_write_and_check(self):
        out_md = os.path.join(self.root, "r.md")
        self.assertEqual(self.run_cli(os.path.join(TOOLS, "gen_test_recipes.py"), "--root",
                                      self.root, "--out", out_md)[0], 0)
        self.assertEqual(self.run_cli(os.path.join(TOOLS, "gen_test_recipes.py"), "--root",
                                      self.root, "--out", out_md, "--check")[0], 0)

    def test_spec_conformance(self):
        rc, out = self.run_cli(os.path.join(TOOLS, "spec_conformance.py"), "--root", self.root,
                               "--out", os.path.join(self.root, "c.md"))
        self.assertEqual(rc, 0, out)
        self.assertIn("\u2192", out)

    def test_eotg_lint(self):
        rc, out = self.run_cli(os.path.join(TOOLS, "eotg_lint.py"), "--root", self.root)
        self.assertIn("total:", out)         # findings are fine; a crash is not
        self.assertIn("eotg_\u2192_l_english.yml", out)

    def test_port_religions(self):
        src = os.path.join(self.root, "OLD PROJECT VERSION", "common", "religion")
        rc, out = self.run_cli(os.path.join(TOOLS, "port_religions_1_20.py"), "--src", src,
                               "--out", os.path.join(self.root, "port"))
        self.assertEqual(rc, 0, out)
        self.assertIn("\u2192", out)

    def test_check_all(self):
        # gen_test_recipes --check prints the generated file's absolute path,
        # which holds the root's non-ASCII character
        self.run_cli(os.path.join(TOOLS, "gen_test_recipes.py"), "--root", self.root)
        rc, out = self.run_cli(os.path.join(TOOLS, "check_all.py"), "--root", self.root,
                               "--only", "gen_test_recipes", "--verbose")
        self.assertIn("summary: 1 pass", out)
        self.assertIn("\u2192", out)


class AsciiFallback(unittest.TestCase):
    def test_stream_without_reconfigure_gets_ascii(self):
        class Cp1252Stream(io.StringIO):
            encoding = "cp1252"
        raw = Cp1252Stream()
        old = sys.stdout
        try:
            sys.stdout = raw
            P.utf8_console()
            print("a → b — c 一")
        finally:
            sys.stdout = old
        self.assertEqual(raw.getvalue(), "a -> b - c ?\n")

    def test_utf8_streams_untouched(self):
        buf = io.StringIO()
        old = sys.stdout
        try:
            sys.stdout = buf
            P.utf8_console()
            self.assertIs(sys.stdout, buf)
        finally:
            sys.stdout = old


if __name__ == "__main__":
    unittest.main()
