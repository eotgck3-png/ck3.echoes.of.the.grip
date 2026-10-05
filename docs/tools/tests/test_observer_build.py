"""docs/tools/observer/tools/build_observer.py writes sub-mod files with exactly one BOM.

Run: python -m unittest discover docs/tools/tests
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "observer", "tools"))
sys.path.insert(0, HERE)
from _testutil import rmtree  # noqa: E402
import build_observer as B  # noqa: E402
import textio  # noqa: E402


class ObserverWrite(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="eotg_obs_")
        self.addCleanup(rmtree, self.d)
        self.old = B.OUT
        B.OUT = Path(self.d)
        self.addCleanup(setattr, B, "OUT", self.old)

    def test_rewrite_twice_one_bom(self):
        rel = "common/on_action/eotg_observer_on_actions.txt"
        src = os.path.join(self.d, "src.txt")
        with open(src, "wb") as fh:                     # a source with stacked BOMs
            fh.write(textio.BOM * 3 + b"eotg_x = { }\n")
        for _ in range(2):
            B.write(rel, B.read(Path(src)))
            B.write(rel, B.read(B.OUT / rel))          # and its own output, re-read
        with open(os.path.join(self.d, rel), "rb") as fh:
            raw = fh.read()
        self.assertEqual(raw, textio.BOM + b"eotg_x = { }\n")

    def test_loc_has_one_bom(self):
        B.write("localization/english/x_l_english.yml", B.loc_keys([]))
        with open(os.path.join(self.d, "localization/english/x_l_english.yml"), "rb") as fh:
            raw = fh.read()
        self.assertTrue(raw.startswith(textio.BOM + b"l_english:"))
        self.assertEqual(textio.count_boms(raw), 1)


if __name__ == "__main__":
    unittest.main()
