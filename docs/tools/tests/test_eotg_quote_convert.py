"""Tests for docs/tools/eotg_quote_convert.py (event_quality_v1 W0e).

Fixtures are the spec's: Konan's, don't, the soldiers' quarters, Custom('KnightCulture'),
'we', speech at value start (vanilla tournament_events.9004.desc shape), speech at value end
(hold_court.7000.desc shape), nested speech across \\n\\n.

Run: python -m unittest discover docs/tools/tests
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _testutil import rmtree  # noqa: E402
import eotg_quote_convert as Q  # noqa: E402
import textio  # noqa: E402


def conv(v):
    return Q.convert_value(v)


def kinds(v):
    return sorted({i.kind for i in Q.analyze_value(v).issues})


class Apostrophes(unittest.TestCase):
    def test_intraword_is_never_a_quote(self):
        for v in ("Konan's ship.", "I don't know.", "it's late", "[x.GetFirstName]'s skull",
                  "the 9's row"):
            new, a = conv(v)
            self.assertEqual(new, v)
            self.assertEqual(a.issues, [], v)
            self.assertFalse(a.has_single_quote_speech, v)

    def test_possessive_plural_goes_to_review(self):
        new, a = conv("He sleeps in the soldiers' quarters.")
        self.assertEqual(new, "He sleeps in the soldiers' quarters.")
        self.assertEqual(kinds(a.value), ["possessive"])
        self.assertFalse(a.has_single_quote_speech)

    def test_word_initial_goes_to_review(self):
        self.assertIn("unpaired-open", kinds("Give 'em hell."))

    def test_custom_call_is_masked(self):
        v = "Offer it to one of my [ROOT.Char.Custom('KnightCulturePluralNoTooltipLowercase')]."
        new, a = conv(v)
        self.assertEqual(new, v)
        self.assertEqual(a.issues, [])
        v2 = "[GetCouncillorPosition( 'councillor_steward' )] nods. 'Fine,' I say."
        self.assertEqual(conv(v2)[0], "[GetCouncillorPosition( 'councillor_steward' )] nods. \"Fine,\" I say.")


class Speech(unittest.TestCase):
    def test_mid_value(self):
        v = "[h.GetSheHe|U] is not shouting. 'Step aside,' [h.GetSheHe] says, 'or I will make you.' It is late."
        new, a = conv(v)
        self.assertTrue(a.auto)
        self.assertEqual(new, "[h.GetSheHe|U] is not shouting. \"Step aside,\" [h.GetSheHe] says, "
                              "\"or I will make you.\" It is late.")

    def test_value_start(self):
        # tournament_events.9004.desc shape: speech opens the value
        new, a = conv("'Go, go faster!' I hear behind me.")
        self.assertTrue(a.auto)
        self.assertEqual(new, "\"Go, go faster!\" I hear behind me.")

    def test_value_end(self):
        # hold_court.7000.desc shape: speech ends the value
        new, a = conv("She leans in and asks, 'Will you hear me?'")
        self.assertTrue(a.auto)
        self.assertEqual(new, "She leans in and asks, \"Will you hear me?\"")

    def test_after_newline_and_colon(self):
        self.assertEqual(conv("\\n\\n'Yes,' she says.")[0], "\\n\\n\"Yes,\" she says.")
        self.assertEqual(conv("Send it with a note: 'I don't remember writing this.'")[0],
                         "Send it with a note: \"I don't remember writing this.\"")

    def test_apostrophe_inside_speech_is_kept(self):
        new, a = conv("'I'll break the terms. You know I will,' he says.")
        self.assertTrue(a.auto)
        self.assertEqual(new, "\"I'll break the terms. You know I will,\" he says.")

    def test_quoted_single_word_goes_to_review(self):
        v = "I said 'we'. I was giving an order: 'We will not be moving the fleet.'"
        new, a = conv(v)
        self.assertEqual(new, v)
        self.assertIn("single-word", kinds(v))
        self.assertTrue(a.has_single_quote_speech)
        self.assertEqual(a.proposed, "I said \"we\". I was giving an order: "
                                     "\"We will not be moving the fleet.\"")

    def test_multi_paragraph_goes_to_review(self):
        v = "'First part.\\n\\nSecond part,' she says."
        new, a = conv(v)
        self.assertEqual(new, v)
        self.assertIn("paragraphs", kinds(v))

    def test_nested_across_paragraphs(self):
        v = "'He told me, 'Wait.'\\n\\nThen he left.'"
        new, a = conv(v)
        self.assertEqual(new, v)
        self.assertTrue(a.issues)

    def test_masked_inside_goes_to_review(self):
        v = "'Thank you, [x.GetFirstName],' she says."
        new, a = conv(v)
        self.assertEqual(new, v)
        self.assertEqual(kinds(v), ["masked-inside"])
        self.assertEqual(a.proposed, "\"Thank you, [x.GetFirstName],\" she says.")

    def test_emp_inside_goes_to_review(self):
        self.assertEqual(kinds("'It closed #EMP before#! I decided,' she says."), ["masked-inside"])

    def test_never_escaped(self):
        new, _ = conv("'Yes,' she says.")
        self.assertNotIn('\\"', new)


class PostCheck(unittest.TestCase):
    def test_only_quote_characters_change(self):
        with self.assertRaises(Q.PostCheckError):
            Q.post_check("'a.' b", "\"a.\" c", [(0, 3)])
        with self.assertRaises(Q.PostCheckError):
            Q.post_check("'a.' b", "\"a.' b", [(0, 3)])
        Q.post_check("'a.' b", "\"a.\" b", [(0, 3)])


class Lines(unittest.TestCase):
    def test_line_parts_kept(self):
        text = (" k.desc:0 \"'Yes,' she says.\" # keep me\r\n"
                " k.t:1 \"Konan's Title\"\r\n"
                "# comment 'x'\r\n")
        res = Q.process_text(text)
        self.assertEqual(len(res.auto), 1)
        self.assertEqual("".join(res.new_lines),
                         " k.desc:0 \"\"Yes,\" she says.\" # keep me\r\n"
                         " k.t:1 \"Konan's Title\"\r\n"
                         "# comment 'x'\r\n")

    def test_comment_with_quote_goes_to_review(self):
        res = Q.process_text(" k:0 \"'Yes,' she says.\" # was \"no\"\n")
        self.assertEqual(res.auto, [])
        self.assertEqual(res.review[0][3][0].kind, "comment-quote")


class Apply(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="eotg_quote_")
        self.addCleanup(rmtree, self.d)
        os.makedirs(os.path.join(self.d, "localization", "english"))
        self.p = os.path.join(self.d, "localization", "english", "eotg_x_l_english.yml")
        with open(self.p, "wb") as fh:
            fh.write(textio.BOM + b"l_english:\r\n k:0 \"'Yes,' she says.\"\r\n"
                     b" j:0 \"the soldiers' mess\"\r\n")

    def raw(self):
        with open(self.p, "rb") as fh:
            return fh.read()

    def test_dry_run_writes_nothing(self):
        before = self.raw()
        res = Q.run(self.d)
        self.assertEqual(Q.summary(res), (1, 1))
        self.assertEqual(self.raw(), before)
        report = Q.format_report(res)
        self.assertIn("AUTO (converted automatically): 1", report)
        self.assertIn("- k:0 \"'Yes,' she says.\"", report)

    def test_apply_keeps_one_bom_and_crlf(self):
        Q.run(self.d, apply=True)
        self.assertEqual(self.raw(), textio.BOM + b"l_english:\r\n k:0 \"\"Yes,\" she says.\"\r\n"
                         b" j:0 \"the soldiers' mess\"\r\n")
        Q.run(self.d, apply=True)     # idempotent: nothing left to convert
        self.assertEqual(textio.count_boms(self.raw()), 1)


class RealTree(unittest.TestCase):
    """The mod's own loc: every AUTO conversion passes the post-check (no exception)."""

    def test_real_tree_dry_run(self):
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))))
        if not os.path.isdir(os.path.join(root, "localization")):
            self.skipTest("no localization/")
        Q.run(root)


if __name__ == "__main__":
    unittest.main()
