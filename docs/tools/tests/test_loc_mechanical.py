"""Tests for docs/tools/qa/loc_mechanical.py's quote-form check (event_quality_v1 W0c).

The check was inverted on 2026-10-08: an unescaped inner " is vanilla's speech form and
passes; an escaped \\", an odd number of inner ", and '...' speech are warned.

Run: python -m unittest discover docs/tools/tests
"""
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _testutil import rmtree  # noqa: E402

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(TOOLS, "qa", "loc_mechanical.py")

LOC = ("﻿l_english:\n"
       ' eotg_aug_a.desc:0 "I wait. "Step aside," she says, "or I will make you.""\n'
       ' eotg_aug_b.desc:0 "She says, \\"Go.\\""\n'
       ' eotg_aug_c.desc:0 "An unclosed "quote here."\n'
       " eotg_aug_d.desc:0 \"'Step aside,' she says.\"\n"
       " eotg_aug_e.desc:0 \"Konan's ship, the soldiers' quarters.\"\n")


class QuoteForm(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="eotg_locmech_")
        self.addCleanup(rmtree, self.d)
        files = {"localization/english/eotg_augmentation_l_english.yml": LOC}
        for sub in ("decisions/eotg_augmentation_decisions.txt",
                    "modifiers/eotg_augmentation_modifiers.txt",
                    "opinion_modifiers/eotg_augmentation_opinions.txt",
                    "traits/eotg_augmentation_traits.txt"):
            files["common/" + sub] = ""
        files["events/eotg_augmentation_x.txt"] = (
            "namespace = eotg_aug\neotg_aug.1 = { desc = eotg_aug_a.desc }\n")
        for rel, text in files.items():
            p = os.path.join(self.d, *rel.split("/"))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="") as fh:
                fh.write(text)

    def test_inverted(self):
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        out = subprocess.run([sys.executable, SCRIPT, self.d], stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, env=env).stdout.decode("utf-8")
        self.assertNotIn("INNERQUOTE", out)
        lines = [l for l in out.splitlines() if l.startswith("WARNING")]
        got = sorted((l.split()[1], l.split()[3]) for l in lines)
        self.assertEqual(got, [("ESCQUOTE", "eotg_aug_b.desc"), ("ODDQUOTE", "eotg_aug_c.desc"),
                               ("SQSPEECH", "eotg_aug_d.desc")], out)


if __name__ == "__main__":
    unittest.main()
