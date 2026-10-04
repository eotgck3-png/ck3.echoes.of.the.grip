"""Fixture tests for docs/tools/gen_test_recipes.py.

One fixture mod with: a fire-cold event, a saved-scope event, a story event, a
flag-gated event, a tier-gated event, a hidden event and one fired on a knight.
Run: python -m unittest discover docs/tools/tests
"""
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gen_test_recipes as G  # noqa: E402

BOM = "﻿"
FILES = {
    "common/scripted_triggers/eotg_t.txt": """
eotg_is_aug_tier3 = {
    has_trait = eotg_cybernetics
    has_trait_xp = { trait = eotg_cybernetics value >= 100 }
}
""",
    "common/on_action/eotg_o.txt": """
yearly_playable_pulse = { on_actions = { eotg_on_yearly } }
eotg_on_yearly = {
    effect = {
        if = {
            limit = { eotg_is_aug_tier3 = yes }
            random_list = {
                10 = { trigger_event = eotg_t.1 }
                10 = { trigger = { gold >= 100 } trigger_event = eotg_t.4 }
                10 = { trigger_event = eotg_t.5 }
            }
        }
    }
}
""",
    "common/story_cycles/eotg_s.txt": """
eotg_story_x = {
    on_setup = { set_variable = { name = eotg_stage value = 1 } }
    effect_group = {
        days = 30
        triggered_effect = {
            trigger = { var:eotg_stage = 1 }
            effect = { story_owner = { trigger_event = eotg_t.3 } }
        }
    }
}
""",
    "common/decisions/eotg_d.txt": """
eotg_decision_start = {
    is_shown = { is_landed = yes }
    effect = { create_story = eotg_story_x }
}
""",
    "events/eotg_test_tier3.txt": """
namespace = eotg_t
# fire cold
eotg_t.1 = {
    type = character_event
    title = eotg_t.1.t
    desc = eotg_t.1.desc
    immediate = { trigger_event = eotg_t.6 }
    option = {
        name = eotg_t.1.a
        random_courtier = { save_scope_as = eotg_victim }
        add_character_flag = eotg_flag_x
        trigger_event = eotg_t.2
    }
    option = {
        name = eotg_t.1.b
        every_knight = { trigger_event = eotg_t.7 }
    }
}
# saved scope from the parent
eotg_t.2 = {
    type = character_event
    title = eotg_t.2.t
    desc = eotg_t.2.desc
    option = { name = eotg_t.2.a scope:eotg_victim = { add_gold = 1 } }
}
# story
eotg_t.3 = {
    type = character_event
    title = eotg_t.3.t
    trigger = { any_owned_story = { story_type = eotg_story_x } }
    option = { name = eotg_t.3.a }
}
# tier gated
eotg_t.4 = {
    type = character_event
    title = eotg_t.4.t
    trigger = { eotg_is_aug_tier3 = yes  has_trait = brave }
    option = { name = eotg_t.4.a }
}
# flag gated
eotg_t.5 = {
    type = character_event
    title = eotg_t.5.t
    trigger = { has_character_flag = eotg_flag_x }
    option = { name = eotg_t.5.a }
}
# hidden
eotg_t.6 = {
    type = character_event
    hidden = yes
    immediate = { add_gold = 5 }
}
# fired on a knight, reads a duel value inside its duel
eotg_t.7 = {
    type = character_event
    title = eotg_t.7.t
    option = {
        name = eotg_t.7.a
        duel = { skill = prowess value = 10  50 = { compare_modifier = { value = scope:duel_value } } }
    }
}
""",
    "localization/english/eotg_t_l_english.yml": BOM + "l_english:\n" + "".join(
        ' %s:0 "%s"\n' % kv for kv in (
            ("eotg_t.1.t", "The First"), ("eotg_t.2.t", "The Victim [eotg_victim.GetName]"),
            ("eotg_t.2.desc", "[eotg_victim.GetFirstName] stares."),
            ("eotg_t.3.t", "Story Beat"), ("eotg_t.4.t", "Tier Three"),
            ("eotg_t.5.t", "Flagged | Piped"), ("eotg_t.7.t", "The Knight"))),
}


def make_mod(files=FILES):
    d = tempfile.mkdtemp(prefix="eotg_recipes_")
    for rel, text in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
    return d


class Recipes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = make_mod()
        cls.recipes, cls.text = G.generate(cls.root)
        cls.by = {r["id"]: r for r in cls.recipes}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root)

    def test_fire_cold(self):
        r = self.by["eotg_t.1"]
        self.assertEqual(r["fire_cold"], "yes")
        self.assertEqual(r["title"], "The First")
        self.assertEqual(r["fire"], "event eotg_t.1")
        self.assertEqual(r["fired_by"], ["on_action yearly_playable_pulse → eotg_on_yearly"])
        # its context (the tier the pulse requires) is offered for realistic content
        self.assertEqual(r["setup_recommended"], [
            ["console", "effect eotg_aug_initiate_effect = yes"],
            ["console", "effect add_trait_xp = { trait = eotg_cybernetics value = 100 }"]])

    def test_saved_scope(self):
        r = self.by["eotg_t.2"]
        self.assertEqual(r["fire_cold"], "no")
        self.assertEqual(r["missing"], ["needs scope:eotg_victim, saved by event eotg_t.1 option a"])
        self.assertEqual(r["fired_by"], ["event eotg_t.1 option a"])
        self.assertEqual(r["live_route"], "on_action yearly_playable_pulse → eotg_on_yearly → "
                         "event eotg_t.1 option a → this event; then let time run (yearly "
                         "pulses and stories pace it)")

    def test_story(self):
        r = self.by["eotg_t.3"]
        self.assertEqual(r["fire_cold"], "no")
        self.assertEqual(r["missing"], ["needs story eotg_story_x running "
                                        "(created by decision eotg_decision_start)"])
        self.assertEqual(r["fired_by"], ["story eotg_story_x"])
        # story-scope conditions (var:eotg_stage) are not the player's setup
        self.assertEqual(r["setup_recommended"], [])
        self.assertTrue(r["live_route"].startswith(
            "decision eotg_decision_start → story eotg_story_x → this event"))

    def test_tier_gated(self):
        r = self.by["eotg_t.4"]
        self.assertEqual(r["fire_cold"], "setup")
        self.assertEqual(r["setup"], [
            ["console", "effect eotg_aug_initiate_effect = yes"],
            ["console", "effect add_trait_xp = { trait = eotg_cybernetics value = 100 }"],
            ["console", "add_trait brave"]])
        self.assertEqual(r["setup_recommended"], [["console", "effect add_gold = 100"]])
        self.assertEqual(r["live_route"], "")

    def test_flag_gated(self):
        r = self.by["eotg_t.5"]
        self.assertEqual(r["fire_cold"], "no")
        self.assertEqual(r["missing"], ["needs flag eotg_flag_x, set by event eotg_t.1 option a"])
        self.assertIn(["console", "effect add_character_flag = eotg_flag_x"], r["setup"])
        self.assertTrue(r["live_route"].startswith(
            "first get flag eotg_flag_x (event eotg_t.1 option a); then on_action"), r["live_route"])

    def test_hidden(self):
        r = self.by["eotg_t.6"]
        self.assertTrue(r["hidden"])
        self.assertEqual(r["fired_by"], ["event eotg_t.1 immediate"])
        self.assertIn("hidden: runs silently, check its effects", self.text)

    def test_fired_on_other_and_duel_value(self):
        r = self.by["eotg_t.7"]
        self.assertEqual(r["fire"], "event eotg_t.7 <character id>")
        self.assertIn("every_knight", r["fire_note"])
        self.assertEqual(r["fire_cold"], "yes", r["missing"])   # duel_value is set by duel

    def test_markdown_layout(self):
        t = self.text
        self.assertTrue(t.startswith("# Console recipes"))
        self.assertIn("Do not edit by hand", t)
        self.assertIn("HOW_TO_TEST_IN_GAME.md", t)
        self.assertIn("| **Total** | | **7** | **3** | **1** | **3** |", t)
        self.assertIn("## Overclocked", t)        # file stem *_tier3 -> test-plan heading
        self.assertIn("Flagged \\| Piped", t)       # pipes escaped in cells

    def test_deterministic(self):
        _, again = G.generate(self.root)
        self.assertEqual(self.text, again)


class CLI(unittest.TestCase):
    def setUp(self):
        self.root = make_mod()
        self.addCleanup(shutil.rmtree, self.root)
        self.out = os.path.join(self.root, *G.OUT_REL.split("/"))

    def run_main(self, *args):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = G.main(["--root", self.root] + list(args))
        return rc, buf.getvalue()

    def test_write_check_crlf_stale(self):
        self.assertEqual(self.run_main("--check")[0], 1)       # not written yet
        rc, out = self.run_main()
        self.assertEqual(rc, 0)
        self.assertIn("7 events", out)
        self.assertEqual(self.run_main("--check")[0], 0)
        with open(self.out, "rb") as fh:
            data = fh.read()
        with open(self.out, "wb") as fh:                         # a CRLF checkout
            fh.write(data.replace(b"\n", b"\r\n"))
        self.assertEqual(self.run_main("--check")[0], 0)
        with open(self.out, "ab") as fh:
            fh.write(b"edited\r\n")
        rc, out = self.run_main("--check")
        self.assertEqual(rc, 1)
        self.assertIn("STALE", out)

    def test_event_and_json(self):
        rc, out = self.run_main("--event", "eotg_t.2")
        self.assertEqual(rc, 0)
        self.assertIn("fire cold:  NO", out)
        self.assertIn("needs scope:eotg_victim", out)
        self.assertFalse(os.path.exists(self.out))
        j = os.path.join(self.root, "r.json")
        self.run_main("--json", j)
        with open(j, encoding="utf-8") as fh:
            self.assertEqual(len(json.load(fh)), 7)
        from contextlib import redirect_stderr
        with redirect_stderr(io.StringIO()):
            self.assertEqual(self.run_main("--event", "eotg_nope.1")[0], 2)


class RealRecipesCurrent(unittest.TestCase):
    """The committed recipes must match a fresh run (skips outside the repo)."""

    def test_current(self):
        out = os.path.join(G.DEFAULT_ROOT, *G.OUT_REL.split("/"))
        if not (os.path.isdir(os.path.join(G.DEFAULT_ROOT, "events")) and os.path.exists(out)):
            self.skipTest("not running inside the mod repo")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(G.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
