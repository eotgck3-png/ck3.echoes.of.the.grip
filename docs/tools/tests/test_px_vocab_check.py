"""Tests for docs/tools/px_vocab_check.py: nested subject-contract level keys count as definitions.

Run: python -m unittest discover docs/tools/tests
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import px_vocab_check as V  # noqa: E402

CONTRACT = """
eotg_test_contract = {
    display_mode = radiobutton
    obligation_levels = {
        eotg_level_low = {
            levies = 0.1
            ai_liege_desire = { value = 10 }
        }
        eotg_level_high = { default = yes }
    }
    not_a_level = { x = 1 }
}
other_contract = {
    obligation_levels = { other_level = { } }
}
"""


class ObligationLevels(unittest.TestCase):
    def test_levels_found_only_one_block_below(self):
        self.assertEqual(V.obligation_levels(CONTRACT),
                         {"eotg_level_low", "eotg_level_high", "other_level"})

    def test_no_levels_block(self):
        self.assertEqual(V.obligation_levels("a = { b = { c = 1 } }"), set())

    def test_comments_stripped_first(self):
        text = "\n".join(V.strip_comments("c = { obligation_levels = { # x = {\n lvl = { } } }"))
        self.assertEqual(V.obligation_levels(text), {"lvl"})


if __name__ == "__main__":
    unittest.main()
