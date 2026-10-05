"""Tests for docs/tools/px_event_report.py: the variable-name whitelist follows --root.

Run: python -m unittest discover docs/tools/tests
"""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _testutil import rmtree, tempdir  # noqa: E402,F401
import check_all as C  # noqa: E402
import px_event_report as R  # noqa: E402

# A name only the other checkout uses as a variable; PX asks loc for it.
VAR = "eotg_only_in_other_checkout_xyz"


class RootWhitelist(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="eotg_pxr_")
        self.addCleanup(rmtree, self.root)
        ev = os.path.join(self.root, "events")
        os.makedirs(ev)
        with open(os.path.join(ev, "eotg_x.txt"), "w", encoding="utf-8") as fh:
            fh.write("namespace = eotg_x\n"
                     "eotg_x.1 = { immediate = { set_variable = { name = %s value = 1 } } }\n" % VAR)
        self.out = os.path.join(self.root, "px")
        os.makedirs(self.out)
        graph = {"nodes": [{"id": "on_x", "kind": "on_action"},
                           {"id": "eotg_x.1", "kind": "event", "source": "mod"}],
                 "edges": [{"from": "on_x", "to": "eotg_x.1"}]}
        cov = [{"language": "english", "defined": 1,
                "missing": [{"key": VAR, "file": "events/eotg_x.txt", "line": 2}]}]
        with open(os.path.join(self.out, "px_eventGraph.json"), "w", encoding="utf-8") as fh:
            json.dump(graph, fh)
        with open(os.path.join(self.out, "px_locCoverage.json"), "w", encoding="utf-8") as fh:
            json.dump(cov, fh)

    def run_report(self, *args):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = R.cli([self.out] + list(args))
        return rc, buf.getvalue()

    def test_root_supplies_the_whitelist(self):
        rc, out = self.run_report("--root", self.root)
        self.assertEqual(rc, 0, out)
        self.assertNotIn("missing english loc '%s'" % VAR, out)
        self.assertIn("1 reachable, 0 unreachable", out)

    def test_default_root_is_this_repo(self):
        # without --root the whitelist comes from this checkout, which never sets VAR
        rc, out = self.run_report()
        self.assertEqual(rc, 1, out)
        self.assertIn("missing english loc '%s'" % VAR, out)

    def test_global_variable_list_is_not_loc(self):
        # error.log, first Frontier launch: eotg_frontier_active reported as missing loc
        name = "eotg_some_global_list"
        with open(os.path.join(self.root, "events", "eotg_x.txt"), "a", encoding="utf-8") as fh:
            fh.write("eotg_x.2 = { immediate = { add_to_global_variable_list = "
                     "{ name = %s target = this } } }\n"
                     "eotg_x.3 = { trigger = { any_in_global_list = { variable = eotg_read_only_list "
                     "count >= 1 } } }\n" % name)
        cov = [{"language": "english", "defined": 1,
                "missing": [{"key": k, "file": "events/eotg_x.txt", "line": 3}
                            for k in (name, "eotg_read_only_list", "eotg_real_missing_key")]}]
        with open(os.path.join(self.out, "px_locCoverage.json"), "w", encoding="utf-8") as fh:
            json.dump(cov, fh)
        rc, out = self.run_report("--root", self.root)
        self.assertNotIn("'%s'" % name, out)
        self.assertNotIn("'eotg_read_only_list'", out)
        self.assertIn("missing english loc 'eotg_real_missing_key'", out)   # real gaps still show

    def test_check_all_passes_root(self):
        cmd = C.px_event_report_cmd(self.out, self.root)
        self.assertEqual(cmd[-2:], ["--root", os.path.abspath(self.root)])
        self.assertTrue(cmd[1].endswith("px_event_report.py"))


if __name__ == "__main__":
    unittest.main()
