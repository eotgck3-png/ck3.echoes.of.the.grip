"""Tests for docs/tools/eotg_event_quality.py (event_quality_v1 W0b, §15).

The voice classifier and the dialogue regex are pattern-based (report caveat: +-5 points);
these tests pin them so any drift is visible.

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
from _testutil import rmtree  # noqa: E402
import eotg_event_quality as E  # noqa: E402
import pdx_parse  # noqa: E402

PERS = {"brave", "craven", "paranoid", "trusting", "wrathful", "calm"}


class Voice(unittest.TestCase):
    def test_second_person(self):
        self.assertEqual(E.voice_label("You wake with blood on your sleeve."), "2nd")

    def test_first_person(self):
        self.assertEqual(E.voice_label("I wake with blood on my sleeve."), "1st")

    def test_neutral(self):
        self.assertEqual(E.voice_label("The youngest ones flinch now."), "neutral")
        self.assertEqual(E.voice_label(""), "none")

    def test_speech_is_stripped_before_counting(self):
        # all the "you" is inside speech: narration is neutral
        self.assertEqual(E.voice_label('The surgeon looks up. "You will walk. Your leg is fine."'),
                         "neutral")
        self.assertEqual(E.voice_label("The surgeon looks up. 'You will walk. Your leg is fine.'"),
                         "neutral")
        self.assertEqual(E.voice_label('The surgeon looks up. \\"You will walk.\\"'), "neutral")
        # NPC speech to me, narrated in first person
        self.assertEqual(E.voice_label('"You did not know your own name," she tells me.'), "1st")

    def test_functions_are_stripped(self):
        self.assertEqual(E.voice_label("[ROOT.Char.GetFirstName] looks at [you.GetName]."),
                         "neutral")

    def test_majority_wins(self):
        self.assertEqual(E.voice_label("I see you. You see me. You know."), "2nd")
        self.assertEqual(E.voice_label("I see you."), "neutral")

    def test_counts(self):
        self.assertEqual(E.voice_counts("I told myself my plan; you heard."), (3, 1))


class Speech(unittest.TestCase):
    """evq.py's SPEECH regex, unchanged."""

    def test_hits(self):
        for t in ('He says, "Go now."', "She says: 'It is early, act now.'", '\\"Run\\"'):
            self.assertTrue(E.SPEECH.search(t), t)

    def test_misses(self):
        for t in ("Konan's ship.", "I said 'we'.", "No speech here."):
            self.assertFalse(E.SPEECH.search(t), t)

    def test_opens_on_loc_function(self):
        # B7 review: speech that opens with a [..] call
        t = 'She looks up. "[ROOT.Char.GetFirstName], sit down."'
        self.assertTrue(E.SPEECH.search(t), t)
        self.assertFalse(E.SPEECH.search('The file [x.GetName] is shut.'))


def opt(text):
    return E._parse_option("option = " + text)


class Gates(unittest.TestCase):
    def test_personality_on_root(self):
        g = E.option_gates(opt("{ name = a trigger = { has_trait = brave } }"), PERS)
        self.assertEqual((g["axis"], g["personality"]), ("personality", ["brave"]))
        g = E.option_gates(opt("{ trigger = { OR = { has_trait = brave has_trait = calm } } }"), PERS)
        self.assertEqual(g["personality"], ["brave", "calm"])

    def test_not_root_or_negated(self):
        for t in ("{ trigger = { scope:spouse = { has_trait = brave } } }",
                  "{ trigger = { NOT = { has_trait = brave } } }",
                  "{ trigger = { any_vassal = { has_trait = brave } } }"):
            self.assertEqual(E.option_gates(opt(t), PERS)["axis"], "other", t)

    def test_education_skill_tier(self):
        self.assertEqual(E.option_gates(opt("{ skill = intrigue }"), PERS)["axis"], "education")
        self.assertEqual(E.option_gates(opt(
            "{ trigger = { has_trait = education_intrigue_3 } }"), PERS)["axis"], "education")
        self.assertEqual(E.option_gates(opt("{ trigger = { diplomacy >= 12 } }"), PERS)["axis"],
                         "education")
        self.assertEqual(E.option_gates(opt(
            "{ trigger = { highest_held_title_tier >= tier_duchy } }"), PERS)["axis"], "tier")

    def test_ungated_and_non_personality_trait(self):
        self.assertEqual(E.option_gates(opt("{ name = x add_gold = 5 }"), PERS)["axis"], "ungated")
        self.assertEqual(E.option_gates(opt("{ trigger = { has_trait = eotg_aug_1 } }"),
                                        PERS)["axis"], "other")


EVENT = """namespace = eotg_t
eotg_t.1 = {
\ttype = character_event
\ttitle = eotg_t.1.t
\tdesc = {
\t\tdesc = eotg_t.1.desc
\t\ttriggered_desc = { trigger = { always = yes } desc = eotg_t.1.desc_more }
\t}
\ttheme = intrigue
\toverride_background = { reference = corridor_night }
\toverride_effect_2d = { reference = smoke }
\tleft_portrait = { character = root animation = worry }
\tright_portrait = { character = root triggered_animation = { trait = brave animation = anger } }
\timmediate = { play_music_cue = mx_cue_death }
\toption = { name = eotg_t.1.a trait = brave trigger = { has_trait = brave } stress_impact = { craven = 1 } ai_chance = { base = 1 } }
\toption = { name = eotg_t.1.b trigger = { has_trait = paranoid } add_internal_flag = dangerous ai_chance = { base = 1 }
\t\tsend_interface_toast = { type = event_toast_effect_bad title = eotg_t.1.toast } }
\toption = { name = eotg_t.1.c skill = intrigue ai_chance = { base = 1 } }
\tafter = { send_interface_toast = { type = event_toast_effect_good title = eotg_t.1.toast_b } }
}
eotg_t.2 = { hidden = yes immediate = { } }
eotg_t.3 = {
\ttype = letter_event
\topening = eotg_t.3.opening
\tsender = root
\tdesc = eotg_t.3.desc
\toption = { name = eotg_t.3.a }
}
"""
LOC = ('﻿l_english:\n'
       ' eotg_t.1.desc:0 "I wake. #EMP Now#! [ROOT.Char.Custom(\'X\')] \\"Run,\\" she says."\n'
       ' eotg_t.1.desc_more:0 "\\n\\nThe court waits."\n'
       ' eotg_t.3.desc:0 "You will not hear from us again."\n')


class Analyze(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="eotg_evq_")
        self.addCleanup(rmtree, self.d)
        for rel, text in (("events/eotg_t.txt", EVENT),
                          ("localization/english/eotg_t_l_english.yml", LOC)):
            p = os.path.join(self.d, *rel.split("/"))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="") as fh:
                fh.write(text)

    def rows(self):
        return {r["id"]: r for r in E.analyze(self.d, E.load_loc(self.d), PERS)}

    def test_event_fields(self):
        rows = self.rows()
        self.assertNotIn("eotg_t.2", rows)              # hidden
        r = rows["eotg_t.1"]
        self.assertEqual(r["backgrounds"], ["corridor_night"])
        self.assertEqual(r["effects_2d"], ["smoke"])
        self.assertEqual(r["toasts"], 2)                 # option + after
        self.assertEqual(r["music_cues"], 1)
        self.assertEqual(r["internal_flags"], ["dangerous"])
        self.assertEqual(r["triggered_animation"], 1)
        self.assertEqual(r["animations"], ["anger", "worry"])
        self.assertTrue(r["emp"] and r["custom_loc"] and r["paragraphs"] and r["speech"])
        self.assertEqual(r["voice"], "1st")
        self.assertEqual(r["main_desc_key"], "eotg_t.1.desc")
        self.assertEqual(r["opt_trait"], 1)
        self.assertEqual(r["personality_gates"], 2)
        self.assertEqual(r["gate_axes"], {"personality": 2, "education": 1})
        l = rows["eotg_t.3"]
        self.assertTrue(l["letter"] and l["sender"])
        self.assertEqual(l["opening_key"], "eotg_t.3.opening")
        self.assertEqual(l["voice"], "2nd")

    def test_summary_and_check(self):
        data = E.build(self.d, PERS)
        s = data["summary"]["mod"]
        self.assertEqual(s["events"], 2)
        self.assertEqual(s["override_background_pct"], 50.0)
        self.assertEqual(s["events_2plus_personality_gates"], 1)
        self.assertEqual(s["letter_events"], 1)
        md = E.render_md(data)
        self.assertIn("| Events (non-hidden) | – | – | **2** |", md)
        self.assertIn("`eotg_t.1`", md)
        self.assertIsNone(E.event_breakdown(data, "eotg_t.9"))
        self.assertIn("personality", E.event_breakdown(data, "eotg_t.1"))
        # --check: stale before writing, current after
        with redirect_stdout(io.StringIO()):
            self.assertEqual(E.main(["--root", self.d, "--check"]), 1)
            self.assertEqual(E.main(["--root", self.d]), 0)
            self.assertEqual(E.main(["--root", self.d, "--check"]), 0)
        with open(os.path.join(self.d, *E.OUT_JSON.split("/")), encoding="utf-8") as fh:
            self.assertEqual(json.load(fh)["summary"]["mod"]["events"], 2)


class Traits(unittest.TestCase):
    def test_cached_list(self):
        t = E.load_personality_traits()
        self.assertGreaterEqual(len(t), 30)
        self.assertIn("brave", t)
        self.assertNotIn("education_intrigue_1", t)

    def test_vanilla_reader(self):
        d = tempfile.mkdtemp(prefix="eotg_traits_")
        self.addCleanup(rmtree, d)
        p = os.path.join(d, "common", "traits")
        os.makedirs(p)
        with open(os.path.join(p, "00_traits.txt"), "w", encoding="utf-8") as fh:
            fh.write("brave = {\n\tcategory = personality\n\topposites = { craven }\n}\n"
                     "education_x = {\n\tcategory = education\n}\n"
                     "# commented = { category = personality }\n")
        self.assertEqual(E.vanilla_personality_traits(d), ["brave"])


if __name__ == "__main__":
    unittest.main()
