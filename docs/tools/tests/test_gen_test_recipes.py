"""Fixture tests for docs/tools/gen_test_recipes.py.

One fixture mod with: a fire-cold event, a saved-scope event, a story event, a
flag-gated event, a tier-gated event, a hidden event and one fired on a knight.
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
        rmtree(cls.root)

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


# -- FIX 9: Frontier-shaped fixtures (title scopes, option saves) --------------
REGION = {
    "common/scripted_triggers/eotg_r.txt": """
eotg_r_is_open = { var:eotg_r_state ?= flag:open }
eotg_r_done = {
    var:eotg_r_progress >= 100
    development_level >= 2
}
""",
    "common/scripted_effects/eotg_r.txt": """
eotg_r_tick_effect = {
    save_scope_as = eotg_r_county
    if = {
        limit = { eotg_r_done = yes }
        holder = { trigger_event = eotg_r.2 }
    }
    else_if = {
        limit = { holder = { is_ai = no } }
        holder = { trigger_event = eotg_r.5 }
    }
}
eotg_r_finish_effect = {
    save_scope_as = eotg_r_county
    remove_variable = eotg_r_state
}
eotg_r_pick_effect = {
    random_courtier = { save_scope_as = $NAME$ }
}
""",
    "common/on_action/eotg_r.txt": """
yearly_playable_pulse = { on_actions = { eotg_on_r } }
eotg_on_r = {
    effect = {
        every_held_title = {
            limit = { tier = tier_county  eotg_r_is_open = yes }
            eotg_r_tick_effect = yes
        }
    }
}
""",
    "common/decisions/eotg_r.txt": """
eotg_decision_r_debug = {
    is_shown = { debug_only = yes }
    effect = { capital_county = { set_variable = { name = eotg_r_state value = flag:open } } }
}
eotg_decision_r_start = {
    effect = {
        capital_county = { save_scope_as = eotg_r_county }
        trigger_event = eotg_r.1
        trigger_event = eotg_r.3
        trigger_event = eotg_r.4
        trigger_event = eotg_r.6
    }
}
""",
    "events/eotg_r.txt": """
namespace = eotg_r
# the Region is passed in by the decision; its state is a title variable
eotg_r.1 = {
    title = eotg_r.1.t
    trigger = { scope:eotg_r_county = { eotg_r_is_open = yes } }
    option = { name = eotg_r.1.a  scope:eotg_r_county = { set_variable = { name = eotg_r_progress value = 0 } } }
}
# fired by a county-scope effect; its option re-saves the Region only AFTER
# reading it, which does not make it fire cold
eotg_r.2 = {
    title = eotg_r.2.t
    trigger = { scope:eotg_r_county = { eotg_r_done = yes } }
    option = { name = eotg_r.2.a  scope:eotg_r_county = { eotg_r_finish_effect = yes } }
}
# the desc reads a scope only an option saves: missing
eotg_r.3 = {
    title = eotg_r.3.t
    desc = eotg_r.3.desc
    option = {
        name = eotg_r.3.a
        random_courtier = { save_scope_as = eotg_r_helper }
        scope:eotg_r_helper = { add_gold = 1 }
    }
}
# the same, read only after the option saved it: fire cold
eotg_r.4 = {
    title = eotg_r.4.t
    option = {
        name = eotg_r.4.a
        random_courtier = { save_scope_as = eotg_r_helper2 }
        scope:eotg_r_helper2 = { add_gold = 1 }
    }
}
# a guarded read only: fire cold, with a note
eotg_r.5 = {
    title = eotg_r.5.t
    desc = {
        first_valid = {
            triggered_desc = { trigger = { scope:eotg_r_county ?= { tier = tier_county } } desc = eotg_r.5.desc_a }
            desc = eotg_r.5.desc_b
        }
    }
    option = { name = eotg_r.5.a }
}
# a scope saved through an effect parameter in immediate
eotg_r.6 = {
    title = eotg_r.6.t
    immediate = { eotg_r_pick_effect = { NAME = eotg_r_victim } }
    option = { name = eotg_r.6.a  scope:eotg_r_victim = { add_gold = 1 } }
}
""",
    "localization/english/eotg_r_l_english.yml": BOM + "l_english:\n"
        ' eotg_decision_r_debug:0 "(Debug) Mark Region Open"\n'
        ' eotg_r.3.desc:0 "[eotg_r_helper.GetName] waits."\n',
}


class TitleScopesAndOptionSaves(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = make_mod(REGION)
        cls.recipes, cls.text = G.generate(cls.root)
        cls.by = {r["id"]: r for r in cls.recipes}

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.root)

    def consoles(self, r, key="setup"):
        return [t for k, t in r[key] if k == "console"]

    def test_title_condition_is_a_county_line_not_a_character_line(self):
        r = self.by["eotg_r.1"]
        self.assertEqual(r["fire_cold"], "no")
        self.assertIn("needs scope:eotg_r_county, saved by decision eotg_decision_r_start",
                      r["missing"])
        self.assertIn("effect <county> = { set_variable = { name = eotg_r_state "
                      "value = flag:open } }", self.consoles(r))
        self.assertNotIn("effect set_variable = { name = eotg_r_state value = flag:open }",
                         self.consoles(r))
        notes = " | ".join(t for k, t in r["setup"] if k == "note")
        self.assertIn("'(Debug) Mark Region Open' (eotg_decision_r_debug)", notes)
        self.assertIn("capital_county", notes)

    def test_effect_context_in_county_scope(self):
        r = self.by["eotg_r.2"]
        cons = self.consoles(r) + self.consoles(r, "setup_recommended")
        self.assertIn("effect <county> = { set_variable = { name = eotg_r_progress value = 100 } }",
                      cons)
        self.assertIn("effect <county> = { change_development_level = 2 }", cons)
        self.assertFalse(any(c.startswith("effect set_variable") for c in cons), cons)
        # fired on the county's holder: the event's root, plain `event`
        self.assertEqual(r["fire"], "event eotg_r.2")
        self.assertEqual(r["fired_by"], ["effect eotg_r_tick_effect \u2190 on_action "
                                         "yearly_playable_pulse \u2192 eotg_on_r"])

    def test_option_save_does_not_provide_for_the_trigger(self):
        r = self.by["eotg_r.2"]
        self.assertEqual(r["fire_cold"], "no")
        self.assertTrue(any("scope:eotg_r_county" in m for m in r["missing"]), r["missing"])

    def test_holder_condition_goes_to_the_root(self):
        r = self.by["eotg_r.5"]
        self.assertIn(["note", "must be the player"], r["setup_recommended"])

    def test_option_order(self):
        self.assertEqual(self.by["eotg_r.3"]["fire_cold"], "no")
        self.assertIn("needs scope:eotg_r_helper, saved by event eotg_r.3 option a",
                      self.by["eotg_r.3"]["missing"])
        self.assertEqual(self.by["eotg_r.4"]["fire_cold"], "yes", self.by["eotg_r.4"]["missing"])

    def test_guarded_read_is_a_note(self):
        r = self.by["eotg_r.5"]
        self.assertEqual(r["fire_cold"], "yes", r["missing"])
        self.assertTrue(any("reads scope:eotg_r_county if present" in t for _, t in r["setup"]),
                        r["setup"])

    def test_param_save_in_immediate(self):
        r = self.by["eotg_r.6"]
        self.assertEqual(r["fire_cold"], "yes", r["missing"])


class CLI(unittest.TestCase):
    def setUp(self):
        self.root = make_mod()
        self.addCleanup(rmtree, self.root)
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
