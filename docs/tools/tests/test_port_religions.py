"""Tests for docs/tools/port_religions_1_20.py on a fixture religion (2 faiths + a family).

Run: python -m unittest discover docs/tools/tests
"""
import io
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pdx_parse as P  # noqa: E402
import port_religions_1_20 as port  # noqa: E402

FAMILY = """﻿# family header
eotg_rf_test = {
    graphical_faith = "pagan_gfx"    # gfx note
    piety_icon_group = "pagan"
    hostility_doctrine = pagan_hostility_doctrine
    doctrine_background_icon = core_tenet_banner_pagan.dds
}
"""

RELIGIONS = """﻿# file header
# eotg_religion_test: the fixture religion
eotg_religion_test = {
    family = eotg_rf_test
    graphical_faith = "pagan_gfx"
    doctrine = doctrine_theocracy_temporal
    doctrine = doctrine_gender_equal
    traits = {
        virtues = { just brave }
        sins    = { craven }
    }
    localization = {
        # High god
        HighGodName = eotg_god_test
        GoodGodNames = { eotg_god_test eotg_god_other }
    }
    faiths = {
        # first faith
        eotg_faith_one = {
            color = { 0.1 0.2 0.3 }    # teal
            doctrine = tenet_asceticism
            doctrine = tenet_monasticism
            doctrine = doctrine_pluralism_pluralistic
            # holy_site = eotg_hs_x    # TODO
        }
        eotg_faith_two = {
            color = { 0.4 0.5 0.6 }
            icon = eotg_faith_two
            doctrine = tenet_legalism
        }
    }
}

# eotg_religion_stampede: deferred
eotg_religion_stampede = {
    family = eotg_rf_test
    faiths = {
        eotg_faith_stampede = { color = { 1 1 1 } doctrine = tenet_legalism }
    }
}
"""


class PortFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="eotg_port_")
        self.addCleanup(shutil.rmtree, self.tmp)
        self.src = os.path.join(self.tmp, "src")
        for sub, name, text in (("religion_family_types", "eotg_fam.txt", FAMILY),
                                ("religion_types", "eotg_religions.txt", RELIGIONS)):
            os.makedirs(os.path.join(self.src, sub))
            with open(os.path.join(self.src, sub, name), "w", encoding="utf-8") as fh:
                fh.write(text)
        self.out = os.path.join(self.tmp, "out")
        self.rep, self.written = port.port(self.src, self.out, repo_root=self.tmp)
        base = os.path.join(self.out, "common", "religion")
        self.fam = P.parse_file(os.path.join(base, "religion_family_types", "eotg_fam.txt"))
        self.rel = P.parse_file(os.path.join(base, "religion_types", "eotg_religions.txt"))
        self.fth = P.parse_file(os.path.join(base, "faith_types", "eotg_faiths.txt"))

    def read(self, *parts):
        with open(os.path.join(self.out, *parts), encoding="utf-8-sig") as fh:
            return fh.read()

    def test_files_parse_and_have_bom(self):
        for doc in (self.fam, self.rel, self.fth):
            self.assertEqual(doc.errors, [])
            self.assertTrue(doc.bom)

    def test_religion_details_wraps_family_and_gfx(self):
        r = P.first(self.rel.nodes, "eotg_religion_test")
        det = P.first(r.value, "religion_details")
        self.assertEqual([c.key for c in det.value], ["family", "graphical_faith"])
        self.assertIsNone(P.first(r.value, "family"))
        self.assertIsNone(P.first(r.value, "faiths"))
        self.assertEqual([c.value for c in P.find(r.value, "doctrine")],
                         ["doctrine_theocracy_temporal", "doctrine_gender_equal"])
        self.assertTrue(P.first(r.value, "traits"))

    def test_localization_kept_intact(self):
        loc = P.first(P.first(self.rel.nodes, "eotg_religion_test").value, "localization")
        self.assertEqual(P.first(loc.value, "HighGodName").value, "eotg_god_test")
        self.assertEqual([c.key for c in P.first(loc.value, "GoodGodNames").value],
                         ["eotg_god_test", "eotg_god_other"])
        self.assertIn("# High god", self.read("common", "religion", "religion_types",
                                               "eotg_religions.txt"))

    def test_faiths_moved_with_details_tenets_doctrines(self):
        self.assertEqual([n.key for n in self.fth.nodes], ["eotg_faith_one", "eotg_faith_two"])
        one = P.first(self.fth.nodes, "eotg_faith_one")
        det = P.first(one.value, "faith_details")
        self.assertEqual(P.first(det.value, "religion").value, "eotg_religion_test")
        self.assertTrue(P.first(det.value, "color").is_block)
        self.assertEqual([c.key for c in P.first(one.value, "tenets").value],
                         ["tenet_asceticism"])
        self.assertEqual([c.key for c in P.first(one.value, "doctrines").value],
                         ["doctrine_monasticism_encouraged", "doctrine_pluralism_pluralistic"])
        self.assertEqual(P.find(one.value, "doctrine"), [])
        two = P.first(self.fth.nodes, "eotg_faith_two")
        self.assertEqual(P.first(P.first(two.value, "faith_details").value, "icon").value,
                         "eotg_faith_two")
        self.assertIsNone(P.first(two.value, "doctrines"))

    def test_family_icon_renamed_with_todo(self):
        f = P.first(self.fam.nodes, "eotg_rf_test")
        self.assertEqual(P.first(f.value, "tenet_background_icon").value,
                         "core_tenet_banner_pagan")
        self.assertIsNone(P.first(f.value, "doctrine_background_icon"))
        txt = self.read("common", "religion", "religion_family_types", "eotg_fam.txt")
        for k in port.FAMILY_ICON_SIBLINGS:
            self.assertIn("TODO: set %s" % k, txt)
        self.assertIn("# gfx note", txt)

    def test_stampede_dropped_and_logged(self):
        self.assertIsNone(P.first(self.rel.nodes, "eotg_religion_stampede"))
        self.assertIsNone(P.first(self.fth.nodes, "eotg_faith_stampede"))
        self.assertEqual([d[0] for d in self.rep.dropped], ["eotg_religion_stampede"])
        report = self.read("PORT_REPORT.md")
        self.assertIn("eotg_religion_stampede", report)
        self.assertIn("`eotg_faith_stampede`", report)
        self.assertNotIn("eotg_religion_stampede: deferred",
                         self.read("common", "religion", "religion_types", "eotg_religions.txt"))

    def test_stopgap_on_every_top_level_block(self):
        for doc_name in (("religion_family_types", "eotg_fam.txt"),
                         ("religion_types", "eotg_religions.txt"),
                         ("faith_types", "eotg_faiths.txt")):
            text = self.read("common", "religion", *doc_name)
            doc = P.parse_text(text, keep_comments=True)
            for n in doc.nodes:
                if n.is_block:
                    self.assertIn(port.STOPGAP, n.comments, (doc_name, n.key))

    def test_comments_preserved(self):
        faiths = self.read("common", "religion", "faith_types", "eotg_faiths.txt")
        for c in ("# first faith", "# teal", "# holy_site = eotg_hs_x    # TODO"):
            self.assertIn(c, faiths)
        rel = self.read("common", "religion", "religion_types", "eotg_religions.txt")
        self.assertIn("# eotg_religion_test: the fixture religion", rel)

    def test_report_lists_transformations_todos_unverified(self):
        r = self.read("PORT_REPORT.md")
        self.assertIn("`tenet_monasticism` -> `doctrine_monasticism_encouraged`", r)
        self.assertIn("## TODO", r)
        self.assertIn("faith_details has no `icon`", r)
        self.assertIn("## UNVERIFIED-VANILLA assumptions", r)
        self.assertIn("holy sites are commented out", r)

    def test_deterministic(self):
        out2 = os.path.join(self.tmp, "out2")
        port.port(self.src, out2, repo_root=self.tmp)
        self.assertEqual(port._snapshot(self.out), port._snapshot(out2))

    def test_check_flag_and_refuse_live_common(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(port.main(["--src", self.src, "--out", self.out]), 0)
            self.assertEqual(port.main(["--src", self.src, "--out", self.out, "--check"]), 0)
        with open(os.path.join(self.out, "PORT_REPORT.md"), "a") as fh:
            fh.write("tampered\n")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(port.main(["--src", self.src, "--out", self.out, "--check"]), 1)
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            port.main(["--src", self.src, "--out", os.path.join(port.REPO, "common")])


class RealPortIsCurrent(unittest.TestCase):
    """The committed staging output must match a fresh run (skips outside the repo)."""

    def test_current(self):
        if not (os.path.isdir(port.DEFAULT_SRC) and os.path.isdir(port.DEFAULT_OUT)):
            self.skipTest("v1 sources or staged output not present")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(port.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
