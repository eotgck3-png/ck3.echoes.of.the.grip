"""Fixture tests for docs/tools/gen_seller_names.py (CB-42).

Each reject case from docs/specs/cybernetics_v2_seller_names.md §9 item 6, id
derivation, byte-stable output with exactly one BOM, and the --check round trip.
Run: python -m unittest discover docs/tools/tests
"""
import io
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _testutil import tempdir  # noqa: E402
import gen_seller_names as G  # noqa: E402
import textio  # noqa: E402

GOOD = """# header
[companies]
Merrow & Tallis Surgical
Harlow & Venn Surgical

[gangs]
Low Wires

[syndicates]
the Pill Mob
"""


def make(root, body):
    textio.write_text(os.path.join(root, G.LIST_FILE), body, bom=False)


def _read(root, rel):
    with open(os.path.join(root, *rel.split("/")), "rb") as fh:
        return fh.read()


def run(root, check=False):
    buf = io.StringIO()
    code = G.run(root, check=check, out=buf)
    return code, buf.getvalue()


def with_name(section, name, base=GOOD):
    """GOOD with one more name appended under [section]."""
    marker = "[%s]\n" % section
    return base.replace(marker, marker + name + "\n", 1)


class Ids(unittest.TestCase):
    def test_ampersand_and_case(self):
        self.assertEqual(G.derive_id("Merrow & Tallis Surgical", "companies"), "merrow_and_tallis_surgical")

    def test_accents_fold(self):
        self.assertEqual(G.derive_id("Brénnick Fittings", "companies"), "brennick_fittings")

    def test_syndicate_drops_leading_the(self):
        self.assertEqual(G.derive_id("the Pill Mob", "syndicates"), "pill_mob")
        self.assertEqual(G.derive_id("Samulo's Tieflings", "syndicates"), "samulo_s_tieflings")


class Rejects(unittest.TestCase):
    def assertRejected(self, body, needle=None):
        with tempdir() as root:
            make(root, body)
            code, out = run(root)
            self.assertEqual(code, 1, out)
            self.assertIn(G.LIST_FILE + ":", out)
            if needle:
                self.assertIn(needle, out)
            self.assertFalse(os.path.exists(os.path.join(root, *G.OUT_CUSTOM.split("/"))))

    def test_duplicate(self):
        self.assertRejected(with_name("companies", "harlow & venn surgical"), "duplicate")

    def test_id_collision(self):
        self.assertRejected(with_name("companies", "Merrow and Tallis Surgical"), "same as line")

    def test_gang_with_the(self):
        self.assertRejected(with_name("gangs", "the Short Fuses"), "drop 'the'")

    def test_register_never_name_in_gangs(self):
        self.assertRejected(with_name("gangs", "Pill Mob"), "Pill Mob")

    def test_syndicate_never(self):
        self.assertRejected(with_name("syndicates", "Helix"), "not allowed as a syndicate")
        self.assertRejected(with_name("syndicates", "the Codex"), "not allowed as a syndicate")

    def test_name_never(self):
        self.assertRejected(with_name("companies", "Helix Surgical"), "Helix")

    def test_register_error_in_company(self):
        self.assertRejected(with_name("companies", "Blackstar Fittings"), "Blackstar")

    def test_company_word_ban(self):
        self.assertRejected(with_name("companies", "Tallis Works"), "Works")

    def test_gang_salvage_ban(self):
        self.assertRejected(with_name("gangs", "Scrap Kings"), "Scrap")

    def test_leading_red(self):
        self.assertRejected(with_name("gangs", "Red Lanterns"), "Red")

    def test_gang_word_ban(self):
        self.assertRejected(with_name("gangs", "Low Saints"), "Saint")

    def test_hand_imagery(self):
        self.assertRejected(with_name("companies", "Steady Hands Clinic"), "Hand")

    def test_quote_character(self):
        self.assertRejected(with_name("companies", 'Merrow "Best" Clinic'), "not allowed")

    def test_too_long(self):
        self.assertRejected(with_name("companies", "A" * 33), "limit is 32")

    def test_one_company_only(self):
        self.assertRejected(GOOD.replace("Harlow & Venn Surgical\n", ""), "[companies] needs at least 2")

    def test_empty_syndicates(self):
        self.assertRejected(GOOD.replace("the Pill Mob\n", ""), "[syndicates] needs at least 1")

    def test_name_in_two_lists(self):
        self.assertRejected(with_name("gangs", "Harlow & Venn Surgical"), "duplicate")

    def test_name_before_header_and_unknown_header(self):
        self.assertRejected("Stray Name\n" + GOOD, "is not under")
        self.assertRejected(GOOD + "[vendors]\nFoo\n", "unknown header")


class Accepts(unittest.TestCase):
    def test_pill_mob_passes_as_syndicate(self):
        with tempdir() as root:
            make(root, GOOD)
            code, out = run(root)
            self.assertEqual(code, 0, out)
            self.assertIn("companies: 2  gangs: 1  syndicates: 1", out)

    def test_apostrophe_syndicate_passes(self):
        with tempdir() as root:
            make(root, with_name("syndicates", "Samulo's Tieflings"))
            self.assertEqual(run(root)[0], 0)

    def test_syndicate_warn_is_not_an_error(self):
        with tempdir() as root:
            make(root, with_name("syndicates", "P&D"))
            code, out = run(root)
            self.assertEqual(code, 0, out)
            self.assertIn("warning:", out)


class Outputs(unittest.TestCase):
    def test_byte_stable_one_bom(self):
        with tempdir() as root:
            make(root, GOOD)
            self.assertEqual(run(root)[0], 0)
            first = {r: _read(root, r) for r in (G.OUT_CUSTOM, G.OUT_ROLLS, G.OUT_LOC)}
            self.assertEqual(run(root)[0], 0)
            for rel, data in first.items():
                again = _read(root, rel)
                self.assertEqual(data, again, rel)
                self.assertTrue(data.startswith(textio.BOM), rel)
                self.assertEqual(data.count(textio.BOM), 1, rel)

    def test_gang_loc_adds_the_and_syndicate_is_as_written(self):
        with tempdir() as root:
            make(root, GOOD)
            run(root)
            loc = textio.read_text(os.path.join(root, *G.OUT_LOC.split("/")))[0]
            self.assertIn('eotg_aug_seller_gang_low_wires:0 "the Low Wires"', loc)
            self.assertIn('eotg_aug_seller_syn_pill_mob:0 "the Pill Mob"', loc)

    def test_check_round_trip(self):
        with tempdir() as root:
            make(root, GOOD)
            self.assertEqual(run(root, check=True)[0], 1)          # nothing generated yet
            self.assertEqual(run(root)[0], 0)
            self.assertEqual(run(root, check=True)[0], 0)
            make(root, with_name("companies", "Lenwick Fittings"))
            code, out = run(root, check=True)
            self.assertEqual(code, 1)
            self.assertIn("STALE", out)
            self.assertEqual(run(root)[0], 0)
            code, out = run(root, check=True)
            self.assertEqual(code, 0, out)
            self.assertIn("companies: 3", out)

    def test_check_ignores_crlf_line_endings(self):
        """A checkout with core.autocrlf=true turns the generated files to CRLF; --check
        must still call them current, and a real content change still stale."""
        with tempdir() as root:
            make(root, GOOD)
            self.assertEqual(run(root)[0], 0)
            for rel in G.render_all(G.parse(GOOD, G.LIST_FILE)[0]):
                p = os.path.join(root, *rel.split("/"))
                data = _read(root, rel).replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
                self.assertIn(b"\r\n", data)
                with open(p, "wb") as fh:
                    fh.write(data)
            code, out = run(root, check=True)
            self.assertEqual(code, 0, out)
            self.assertIn("seller names are current", out)
            make(root, with_name("companies", "Lenwick Fittings"))
            code, out = run(root, check=True)
            self.assertEqual(code, 1)
            self.assertIn("STALE", out)

    def test_same_content(self):
        self.assertTrue(G.same_content(b"a\r\nb\r\n", b"a\nb\n"))
        self.assertFalse(G.same_content(b"a\nc\n", b"a\nb\n"))
        self.assertFalse(G.same_content(None, b"a\n"))

    def test_single_syndicate_rival_has_no_valid_entry(self):
        """With one syndicate, the _except roll's only entry excludes itself, so the
        rival stays unset and the custom loc falls back to 'a rival syndicate'."""
        with tempdir() as root:
            make(root, GOOD)
            run(root)
            rolls = textio.read_text(os.path.join(root, *G.OUT_ROLLS.split("/")))[0]
            block = rolls.split("eotg_aug_roll_syndicate_except_effect = {")[1]
            self.assertEqual(block.count("1 = {"), 1)
            self.assertIn("NOT = { var:$EXCLUDE$ ?= flag:eotg_aug_syn_pill_mob }", block)
            # S3-2: the guard sits before random_list, so an all-excluded list never reaches it
            guard = block.split("random_list")[0]
            self.assertIn("if = {", guard)
            self.assertIn("OR = {", guard)
            self.assertIn("NOT = { var:$EXCLUDE$ ?= flag:eotg_aug_syn_pill_mob }", guard)

    def test_every_except_roll_is_guarded_and_plain_rolls_are_not(self):
        with tempdir() as root:
            make(root, GOOD)
            run(root)
            rolls = textio.read_text(os.path.join(root, *G.OUT_ROLLS.split("/")))[0]
            for key, _sec, exclude in G.ROLLS:
                body = rolls.split(key + " = {")[1].split("\n}\n")[0]
                guard = body.split("random_list")[0]
                self.assertEqual("OR = {" in guard, bool(exclude), key)
                if exclude:
                    self.assertEqual(guard.count("NOT = { var:$EXCLUDE$"), body.count("1 = {"), key)
            self.assertEqual(rolls.count("{"), rolls.count("}"))

    def test_rerun_leaves_unchanged_files_alone(self):
        with tempdir() as root:
            make(root, GOOD)
            run(root)
            code, out = run(root)
            self.assertEqual(code, 0)
            self.assertNotIn("wrote", out)
            self.assertEqual(out.count("unchanged"), 3)


if __name__ == "__main__":
    unittest.main()
