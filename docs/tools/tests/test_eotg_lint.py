"""Fixture tests for docs/tools/eotg_lint.py: one hit and one non-hit per rule.

Run: python -m unittest discover docs/tools/tests
"""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _testutil import rmtree, tempdir  # noqa: E402,F401
import eotg_lint as L  # noqa: E402

BOM = "﻿"
LOC_OK = BOM + "l_english:\n"


def make_mod(files):
    d = tempfile.mkdtemp(prefix="eotg_lint_")
    for rel, text in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
    return d


class LintCase(unittest.TestCase):
    def run_rule(self, files, rule, allowlist=frozenset()):
        root = make_mod(files)
        self.addCleanup(rmtree, root)
        return L.lint(root, {rule}, allowlist=set(allowlist))

    def assertHit(self, files, rule, needle=None, count=None, **kw):
        res = [f for f in self.run_rule(files, rule, **kw) if f.rule == rule]
        self.assertTrue(res, "expected %s finding" % rule)
        if needle:
            self.assertTrue(any(needle in f.message for f in res),
                            "%r not in %s" % (needle, [f.message for f in res]))
        if count is not None:
            self.assertEqual(len(res), count, [str(f) for f in res])
        return res

    def assertClean(self, files, rule, **kw):
        res = [f for f in self.run_rule(files, rule, **kw) if f.rule == rule]
        self.assertEqual(res, [], [str(f) for f in res])


class L001(LintCase):
    def test_hit_namespace_effect_flag_variable_onaction(self):
        files = {
            "events/a.txt": "namespace = foo\nfoo.1 = { option = { add_character_flag = my_flag "
                            "set_variable = { name = myvar value = 1 } } }",
            "common/scripted_effects/x.txt": "bad_effect = { }\n@local = 3",
            "common/on_action/o.txt": "on_death = { on_actions = { my_hook } }\nmy_hook = { }",
        }
        res = self.assertHit(files, "L001")
        msgs = " | ".join(f.message for f in res)
        for needle in ("namespace 'foo'", "scripted effect 'bad_effect'", "flag 'my_flag'",
                       "variable 'myvar'", "custom on_action 'my_hook'"):
            self.assertIn(needle, msgs)
        self.assertNotIn("@local", msgs)
        self.assertNotIn("on_death", msgs)   # vanilla hook, not custom

    def test_clean(self):
        self.assertClean({
            "events/a.txt": "namespace = eotg_x\neotg_x.1 = { option = { add_character_flag = "
                            "{ flag = eotg_f days = 3 } set_variable = { name = eotg_v value = 1 } "
                            "add_character_flag = $FLAG$ } }",
            "common/scripted_effects/x.txt": "eotg_effect = { }",
            "common/landed_titles/t.txt": "k_eotg_realm = { }",
            "common/on_action/o.txt": "on_death = { on_actions = { eotg_hook } }\neotg_hook = { }",
        }, "L001")


class L002(LintCase):
    def test_hit(self):
        self.assertHit({"common/landed_titles/t.txt": "eotg_k_realm = { }"}, "L002",
                       needle="eotg_k_realm")

    def test_hit_in_loc_and_comments(self):
        self.assertHit({"localization/english/a_l_english.yml": LOC_OK + ' k:0 "x" # eotg_d_x\n'},
                       "L002", count=1)

    def test_clean(self):
        self.assertClean({"common/landed_titles/t.txt": "k_eotg_realm = { d_eotg_core = { } }\n"
                                                        "eotg_beast = 1"}, "L002")


class L003(LintCase):
    def test_missing_bom_and_header(self):
        res = self.assertHit({"localization/english/a_l_english.yml": 'l_french:\n k:0 "v"\n'},
                             "L003")
        msgs = " ".join(f.message for f in res)
        self.assertIn("missing UTF-8 BOM", msgs)
        self.assertIn("l_english:", msgs)

    def test_scope_and_duplicates_across_replace(self):
        res = self.assertHit({
            "localization/english/a_l_english.yml": LOC_OK + ' k:0 "[scope:x.GetName]"\n',
            "localization/english/replace/b_l_english.yml": LOC_OK + ' k:0 "again"\n',
        }, "L003", count=2)
        self.assertTrue(any("[scope:" in f.message for f in res))
        dup = [f for f in res if "duplicate" in f.message][0]
        self.assertEqual(dup.file, "localization/english/replace/b_l_english.yml")
        self.assertIn("a_l_english.yml:2", dup.message)

    def test_clean(self):
        self.assertClean({
            "localization/english/a_l_english.yml": LOC_OK + ' k:0 "[x.GetName]"\n',
            "localization/english/b_l_english.yml": BOM + "# comment\nl_english:\n j:0 \"v\"\n",
        }, "L003")


class L004(LintCase):
    def test_dead_hook(self):
        self.assertHit({"common/on_action/o.txt": "on_yearly_playable = { on_actions = { eotg_a } }"},
                       "L004", needle="yearly_playable_pulse")

    def test_effect_on_vanilla_hook(self):
        self.assertHit({"common/on_action/o.txt": "on_death = { effect = { add_gold = 1 } }"},
                       "L004", needle="overwrites vanilla")

    def test_clean(self):
        self.assertClean({"common/on_action/o.txt":
                          "yearly_playable_pulse = { on_actions = { eotg_a } events = { eotg_x.1 } }\n"
                          "eotg_a = { trigger = { always = yes } effect = { add_gold = 1 } }"},
                         "L004")


EV = "namespace = eotg_t\n"


class L005(LintCase):
    def test_hit_option_and_decision(self):
        res = self.assertHit({
            "events/e.txt": EV + "eotg_t.1 = { option = { remove_trait = brave } option = { } }",
            "common/decisions/d.txt": "eotg_d = { effect = { remove_character_modifier = eotg_m "
                                      "remove_opinion = { target = root modifier = eotg_o } } }",
        }, "L005", count=3)
        self.assertTrue(any("remove_opinion" in f.message for f in res))

    def test_clean_guarded(self):
        self.assertClean({
            "events/e.txt": EV + "eotg_t.1 = { option = { if = { limit = { has_trait = brave } "
                                 "remove_trait = brave } "
                                 "hidden_effect = { remove_trait = craven } "
                                 "random_list = { 10 = { trigger = { has_trait = calm } "
                                 "remove_trait = calm } } } }",
            "common/decisions/d.txt": "eotg_d = { effect = { every_vassal = { limit = { "
                                      "has_opinion_modifier = { target = root modifier = eotg_o } } "
                                      "remove_opinion = { target = root modifier = eotg_o } } } }",
        }, "L005")

    def test_clean_invisible_contexts(self):
        # immediate blocks, hidden events and on_actions show no tooltip
        self.assertClean({
            "events/e.txt": EV + "eotg_t.1 = { immediate = { remove_trait = brave } }\n"
                                 "eotg_t.2 = { hidden = yes option = { remove_trait = brave } }",
            "common/on_action/o.txt": "eotg_a = { effect = { remove_trait = brave } }",
        }, "L005")

    def test_wrong_guard_still_hits(self):
        self.assertHit({"events/e.txt": EV + "eotg_t.1 = { option = { if = { limit = { "
                                             "has_trait = craven } remove_trait = brave } } }"},
                       "L005", count=1)


class L006(LintCase):
    def test_hit_is_valid_and_nested(self):
        self.assertHit({"common/decisions/d.txt":
                        "eotg_d = { is_valid = { NOT = { has_character_flag = eotg_cd } } "
                        "is_valid_showing_failures_only = { OR = { has_variable = eotg_v "
                        "has_global_variable = eotg_g } } }"}, "L006", count=3)

    def test_clean_is_shown_and_wrapped(self):
        # a failed is_shown hides the decision, so a raw flag there never renders
        self.assertClean({"common/decisions/d.txt":
                          "eotg_d = { is_shown = { has_character_flag = eotg_f "
                          "NOT = { has_variable = eotg_v } } "
                          "is_valid = { custom_description = { text = eotg_cd_tt "
                          "NOT = { has_character_flag = eotg_cd } } } "
                          "effect = { add_character_flag = eotg_cd } }"}, "L006")


class L007(LintCase):
    SE = {"common/scripted_effects/s.txt":
          "eotg_later = { trigger_event = { id = eotg_t.9 days = 3 } }\n"
          "eotg_quiet = { set_variable = { name = eotg_v value = 1 } }\n"
          "eotg_risk = { change_variable = { name = eotg_risk add = 5 } }\n"
          "eotg_story = { create_story = eotg_story_x }"}

    def files(self, options):
        f = dict(self.SE)
        f["events/e.txt"] = EV + "eotg_t.1 = { %s option = { name = nope } }" % options
        return f

    def test_hit_bare_trigger_event(self):
        # init.018.e: only `trigger_event = { id = ... days = 1 }`, looked like "Not yet."
        self.assertHit(self.files("option = { name = a trigger_event = { id = eotg_t.2 days = 1 } }"),
                       "L007", count=1, needle="option a")

    def test_hit_deferred_forms(self):
        self.assertHit(self.files(
            "option = { name = a eotg_later = yes save_scope_as = eotg_x } "
            "option = { name = b hidden_effect = { trigger_event = eotg_t.2 } } "
            "option = { name = c eotg_story = yes } "
            "option = { name = d start_scheme = { type = murder target = scope:x } } "
            "option = { name = e if = { limit = { always = yes } trigger_event = eotg_t.3 } }"),
            "L007", count=5)

    def test_clean_hidden_resource_moves(self):
        # the hidden-risk design keeps these silent on purpose (FIX 2)
        self.assertClean(self.files(
            "option = { name = a eotg_risk = yes } "
            "option = { name = b set_variable = { name = eotg_focus value = flag:x } } "
            "option = { name = c add_character_flag = eotg_f } "
            "option = { name = d eotg_quiet = yes trigger_event = eotg_t.2 } "
            "option = { name = e trigger_event = eotg_t.2 add_character_flag = eotg_f }"), "L007")

    def test_clean_tooltip_single_hidden(self):
        self.assertClean({
            "events/e.txt": EV +
            "eotg_t.1 = { option = { name = a trigger_event = eotg_t.2 custom_tooltip = eotg_tt } "
            "option = { name = b add_gold = 5 trigger_event = eotg_t.2 } option = { name = c } }\n"
            "eotg_t.3 = { option = { name = only trigger_event = eotg_t.2 } }\n"
            "eotg_t.4 = { hidden = yes option = { trigger_event = eotg_t.2 } option = { } }",
        }, "L007")


class L008(LintCase):
    def test_hit(self):
        self.assertHit({"events/e.txt": EV + "eotg_t.1 = { immediate = { add_intrigue = 1 } }"},
                       "L008", needle="add_intrigue_skill")

    def test_clean(self):
        self.assertClean({"events/e.txt": EV + "eotg_t.1 = { immediate = { add_intrigue_skill = 1 } }",
                          "common/modifiers/m.txt": "eotg_m = { intrigue = 2 }"}, "L008")


class L009(LintCase):
    def test_hit_orphan_and_self_only(self):
        res = self.assertHit({"events/e.txt": EV +
                              "eotg_t.1 = { }\neotg_t.2 = { option = { trigger_event = eotg_t.2 } }"},
                             "L009", count=2)
        self.assertEqual(sorted(f.message.split()[1] for f in res), ["eotg_t.1", "eotg_t.2"])

    def test_clean_all_firing_forms(self):
        self.assertClean({
            "events/e.txt": EV + "".join("eotg_t.%d = { }\n" % i for i in range(1, 7)) +
            "eotg_t.9 = { option = { trigger_event = eotg_t.1 } }",
            "common/on_action/o.txt": "eotg_a = { events = { eotg_t.2 } "
                                      "random_events = { 100 = eotg_t.3 } "
                                      "first_valid = { eotg_t.4 } }",
            "common/decisions/d.txt": "eotg_d = { effect = { trigger_event = { id = eotg_t.5 days = 3 } } }",
            "common/story_cycles/s.txt": "eotg_s = { effect_group = { triggered_effect = { "
                                         "effect = { trigger_event = eotg_t.6 } } } }",
            "common/scripted_effects/x.txt": "eotg_fire = { trigger_event = eotg_t.9 }",
        }, "L009")


class L010(LintCase):
    LOC = LOC_OK + ' eotg_t.1.t:0 "t"\n eotg_t.1.desc:0 "d"\n eotg_t.1.a:0 "a"\n' \
                   ' eotg_d:0 "d"\n eotg_d_desc:0 "d"\n trait_eotg_tr:0 "t"\n' \
                   ' trait_eotg_tr_desc:0 "t"\n eotg_m:0 "m"\n eotg_m_desc:0 "m"\n'

    def test_hit(self):
        res = self.assertHit({
            "events/e.txt": EV + "eotg_t.1 = { title = eotg_t.1.t desc = { first_valid = { "
                                 "triggered_desc = { trigger = { always = yes } desc = eotg_t.1.desc_x } "
                                 "desc = eotg_t.1.desc } } option = { name = eotg_t.1.b } }",
            "common/decisions/d.txt": "eotg_d2 = { }",
            "common/traits/t.txt": "eotg_tr2 = { }",
            "common/modifiers/m.txt": "eotg_m2 = { }",
            "localization/english/a_l_english.yml": self.LOC,
        }, "L010")
        missing = sorted(f.message.split("'")[1] for f in res)
        self.assertEqual(missing, sorted([
            "eotg_t.1.desc_x", "eotg_t.1.b", "eotg_d2", "eotg_d2_desc",
            "trait_eotg_tr2", "trait_eotg_tr2_desc", "eotg_m2", "eotg_m2_desc"]))

    def test_clean_and_allowlist(self):
        self.assertClean({
            "events/e.txt": EV + "eotg_t.1 = { title = eotg_t.1.t desc = eotg_t.1.desc "
                                 "option = { name = eotg_t.1.a } option = { name = vanilla_ok } }",
            "common/decisions/d.txt": "eotg_d = { }",
            "common/traits/t.txt": "eotg_tr = { }\neotg_tr3 = { name = eotg_m desc = eotg_m_desc }",
            "common/modifiers/m.txt": "eotg_m = { }",
            "localization/english/a_l_english.yml": self.LOC,
        }, "L010", allowlist={"vanilla_ok"})


class Suppression(LintCase):
    BAD = EV + "eotg_t.1 = { option = { name = a trigger_event = eotg_t.2 } option = { } }"

    def test_allow_on_previous_line(self):
        src = EV + ("eotg_t.1 = {\n"
                    "\t# eotg_lint: allow L007 the follow-up event explains itself\n"
                    "\toption = { name = a trigger_event = eotg_t.2 }\n"
                    "\toption = { }\n}")
        self.assertClean({"events/e.txt": src}, "L007")
        self.assertClean({"events/e.txt": src}, "L000")

    def test_allow_on_same_line_multi_rule(self):
        src = EV + ("eotg_t.1 = {\n\toption = { name = a trigger_event = eotg_t.2 }"
                    "  # eotg_lint: allow L005,L007 deliberate cliffhanger\n\toption = { }\n}")
        self.assertClean({"events/e.txt": src}, "L007")

    def test_allow_other_rule_does_not_suppress(self):
        src = EV + ("eotg_t.1 = {\n\t# eotg_lint: allow L005 wrong rule\n"
                    "\toption = { name = a trigger_event = eotg_t.2 }\n\toption = { }\n}")
        self.assertHit({"events/e.txt": src}, "L007", count=1)

    def test_allow_without_reason_is_l000_and_does_not_suppress(self):
        src = EV + ("eotg_t.1 = {\n\t# eotg_lint: allow L007\n"
                    "\toption = { name = a trigger_event = eotg_t.2 }\n\toption = { }\n}")
        self.assertHit({"events/e.txt": src}, "L000", count=1, needle="without a reason")
        self.assertHit({"events/e.txt": src}, "L007", count=1)

    def test_allow_bad_rule_ids(self):
        self.assertHit({"events/e.txt": EV + "# eotg_lint: allow L999 because\n"}, "L000",
                       needle="unknown rule")
        self.assertHit({"events/e.txt": EV + "# eotg_lint: allow everything\n"}, "L000",
                       needle="without a rule id")

    def test_allow_in_loc(self):
        self.assertClean({"localization/english/eotg_a_l_english.yml": LOC_OK +
                          ' # eotg_lint: allow L011 they = the crowd around them\n'
                          ' eotg_k:0 "[x.GetName] watches as they leave."\n'}, "L011")


class L011(LintCase):
    def loc(self, value, name="eotg_a_l_english.yml"):
        return {"localization/english/" + name: LOC_OK + ' eotg_k:0 "%s"\n' % value}

    def test_hit(self):
        self.assertHit(self.loc("[eotg_victim.GetName] is gone. They left nothing."), "L011",
                       needle="eotg_victim")
        self.assertHit(self.loc("[ROOT.Char.GetFirstName] keeps their counsel."), "L011")

    def test_clean(self):
        for v in ("[eotg_victim.GetName] is gone. [eotg_victim.GetSheHe|U] left nothing.",
                  "[a.GetName] and [b.GetName] argue; they will not stop.",   # two characters
                  "The syndicate sends word. They want payment.",            # no character
                  "[eotg_victim.GetName] stares at the crowd; the themes repeat."):
            self.assertClean(self.loc(v), "L011")
        # only eotg_*.yml files are checked
        self.assertClean(self.loc("[x.GetName] left their sword.", "other_l_english.yml"), "L011")

    def test_allowlist(self):
        root = make_mod(self.loc("[x.GetName] watches them go."))
        self.addCleanup(rmtree, root)
        mod = L.Mod(root)
        self.assertEqual(len(L.rule_l011(mod, allowlist=set())), 1)
        self.assertEqual(L.rule_l011(mod, allowlist={"eotg_k"}), [])


class L012(LintCase):
    def run12(self, key, value):
        root = make_mod({"localization/english/eotg_a_l_english.yml":
                         LOC_OK + ' %s:0 "%s"\n' % (key, value)})
        self.addCleanup(rmtree, root)
        return L.rule_l012(L.Mod(root))

    def test_never_names_are_errors(self):
        for v in ("A Blackstar courier waits.", "Bought on the Shadow Markets.",
                  "under a Black Contract", "P&D sends regards.", "the Codex forbids it",
                  "the Archivists object", "a galactic standard", "Trauma Team inbound",
                  "per interstellar regulation"):
            res = self.run12("eotg_aug_init.001.desc", v)
            self.assertTrue(res and all(f.severity == "ERROR" for f in res), (v, res))

    def test_register_words_are_warnings(self):
        for v in ("a faint whisper", "at the edge of hearing", "the Void hums", "it answers you",
                  "remote control", "a network of clinics", "the warrant arrives",
                  "a programme of grants", "demons in the wiring"):
            res = self.run12("eotg_fracture.010.desc", v)
            self.assertTrue(res and all(f.severity == "WARNING" for f in res), (v, res))
            self.assertIn("eotg_fracture.010.desc", res[0].message)

    def test_clean_and_scope(self):
        for v in ("The archivists log it.", "the overlay labels your own face",
                  "a demonstration of the fittings", "the void of the contract", "he replies"):
            self.assertEqual(self.run12("eotg_aug_tier1.001.desc", v), [], v)
        # keys outside the cybernetics prefixes are not checked
        self.assertEqual(self.run12("eotg_void.0010.desc", "a whisper from the Void"), [])
        # [functions] and $keys$ are not text
        self.assertEqual(self.run12("eotg_mod_aug_x", "[GetPlayer.GetVoidName] $galactic$"), [])

    def test_register_file_is_valid(self):
        reg = L.load_register()
        self.assertTrue(reg["key_prefixes"])
        self.assertGreaterEqual(len(reg["error"]), 19)
        self.assertGreaterEqual(len(reg["warning"]), 29)


class L013(LintCase):
    LOC = "localization/english/eotg_a_l_english.yml"

    def loc(self, *entries):
        return LOC_OK + "".join(' %s:0 "%s"\n' % e for e in entries)

    def test_a_dashes(self):
        self.assertHit({self.LOC: self.loc(("eotg_x.1.desc", "A pause \u2014 then nothing."))},
                       "L013", "L013a eotg_x.1.desc: em dash")
        self.assertHit({self.LOC: self.loc(("eotg_x.1.desc", "years 850\u2013866"))},
                       "L013", "en dash")
        self.assertClean({self.LOC: self.loc(("eotg_x.1.desc", "A pause, then nothing - fine."))},
                         "L013")

    def test_b_british(self):
        res = self.assertHit({self.LOC: self.loc(
            ("eotg_x.1.desc", "The Colour of honour; they realised it afterwards."))}, "L013",
            count=4)
        msgs = " | ".join(f.message for f in res)
        for w in ("'Colour'", "'honour'", "'realised'", "'afterwards'"):
            self.assertIn(w, msgs)
        self.assertIn("(US: color)", msgs)
        self.assertHit({self.LOC: self.loc(("eotg_x.1.desc", "its organisation"))}, "L013",
                       "'organisation'")

    def test_b_clean_and_exceptions(self):
        self.assertClean({self.LOC: self.loc(
            ("eotg_x.1.desc", "The color of honor. They rise; the wise promise, otherwise noise. "
                              "Raised, rising, surprised, precise, exercise, the Tide-Crowned. "
                              "[ROOT.Char.GetColour] $honour_key$ #colour text#!"))}, "L013")
        # exceptions are data: an extra exception silences a word
        root = make_mod({self.LOC: self.loc(("eotg_x.1.desc", "the Grey Margrave"))})
        self.addCleanup(rmtree, root)
        st = L.load_style()
        self.assertTrue(L.rule_l013(L.Mod(root), st))
        st["exceptions"].append("Grey Margrave")
        self.assertEqual(L.rule_l013(L.Mod(root), st), [])

    def test_c_whitespace(self):
        for v, needle in (("Two  spaces.", "double space"), (" Leading.", "leading whitespace"),
                          ("Trailing. ", "trailing whitespace")):
            self.assertHit({self.LOC: self.loc(("eotg_x.1.desc", v))}, "L013", needle)
        self.assertClean({self.LOC: self.loc(("eotg_x.1.desc", "One space. \\n\\nThen more."))},
                         "L013")

    EV = """namespace = eotg_x
eotg_x.1 = {
    desc = {
        first_valid = {
            triggered_desc = { trigger = { always = yes } desc = eotg_x.1.desc_a }
            desc = eotg_x.1.desc_b
        }
        triggered_desc = { trigger = { always = yes } desc = eotg_x.1.desc_app }
        first_valid = {
            triggered_desc = { trigger = { always = no } desc = eotg_x.1.desc_late }
        }
    }
    option = { name = eotg_x.1.a }
}
"""

    def test_d_appended_desc(self):
        files = {"events/e.txt": self.EV, self.LOC: self.loc(
            ("eotg_x.1.desc_a", "Opener."), ("eotg_x.1.desc_b", "Other opener."),
            ("eotg_x.1.desc_app", "Runs on."), ("eotg_x.1.desc_late", "Late."))}
        res = self.assertHit(files, "L013", "L013d eotg_x.1.desc_app", count=1)
        self.assertIn("eotg_x.1", res[0].message)

    def test_d_clean_and_skipped(self):
        files = {"events/e.txt": self.EV, self.LOC: self.loc(
            ("eotg_x.1.desc_a", "Opener."), ("eotg_x.1.desc_b", "Other opener."),
            ("eotg_x.1.desc_app", "\\n\\nNew paragraph."), ("eotg_x.1.desc_late", "Late."))}
        self.assertClean(files, "L013")
        root = make_mod(files)
        self.addCleanup(rmtree, root)
        stats = {}
        L.lint(root, {"L013"}, stats=stats)
        self.assertEqual(len(stats["skipped"]["L013d"]), 1)
        self.assertIn("eotg_x.1.desc_late", stats["skipped"]["L013d"][0])

    def test_d_simple_desc_and_first_segment(self):
        ev = ("namespace = eotg_x\neotg_x.2 = { desc = eotg_x.2.desc option = { name = a } }\n"
              "eotg_x.3 = { desc = { triggered_desc = { trigger = { always = yes } "
              "desc = eotg_x.3.desc } } }\n")
        self.assertClean({"events/e.txt": ev, self.LOC: self.loc(
            ("eotg_x.2.desc", "No prefix."), ("eotg_x.3.desc", "Opener, no prefix."))}, "L013")


class L014(LintCase):
    LOC = "localization/english/eotg_a_l_english.yml"

    def files(self, *keys, **extra):
        f = {self.LOC: LOC_OK + "".join(' %s:0 "x"\n' % k for k in keys)}
        f.update(extra)
        return f

    def test_dead_key(self):
        self.assertHit(self.files("eotg_x.1.desc_orphan"), "L014",
                       "'eotg_x.1.desc_orphan' is defined but nothing references it", count=1)

    def test_referenced(self):
        files = self.files(
            "eotg_x.1.t",                       # literal in script
            "eotg_tt_quoted",                   # quoted literal in script
            "eotg_decision_d", "eotg_decision_d_desc", "eotg_decision_d_tooltip",
            "eotg_decision_d_confirm",          # decision conventions
            "eotg_mod_m", "eotg_mod_m_desc",    # modifier
            "trait_eotg_t", "trait_eotg_t_1_desc", "trait_eotg_t_2_character_desc",
            "trait_track_eotg_t",               # leveled trait
            "eotg_opinion_o",                   # opinion modifier
            "eotg_inner", "eotg_outer",         # $KEY$ in loc ($eotg_inner$ inside eotg_outer)
            "eotg_gui_label",                   # referenced from a .gui
            "not_ours_key",                     # not an eotg key: never checked
            **{"events/e.txt": 'namespace = eotg_x\neotg_x.1 = { title = eotg_x.1.t '
                               'option = { name = eotg_outer custom_tooltip = "eotg_tt_quoted" } }',
               "common/decisions/d.txt": "eotg_decision_d = { }",
               "common/modifiers/m.txt": "eotg_mod_m = { }",
               "common/traits/t.txt": "eotg_t = { }",
               "common/opinion_modifiers/o.txt": "eotg_opinion_o = { opinion = 5 }",
               "gfx/interface/x.gui": 'text = "eotg_gui_label"'})
        files[self.LOC] = files[self.LOC].replace(' eotg_outer:0 "x"', ' eotg_outer:0 "$eotg_inner$"')
        self.assertClean(files, "L014")
        # conventions are data: drop decisions and their keys become dead
        root = make_mod(files)
        self.addCleanup(rmtree, root)
        conv = L.load_conventions()
        del conv["folders"]["decisions"]
        dead = sorted(f.message.split("'")[1] for f in L.rule_l014(L.Mod(root), conv))
        self.assertEqual(dead, ["eotg_decision_d_confirm", "eotg_decision_d_desc",
                                "eotg_decision_d_tooltip"])


class CLI(unittest.TestCase):
    def setUp(self):
        self.root = make_mod({
            "events/e.txt": EV + "eotg_t.1 = { option = { add_intrigue = 1 } }\n"
                                 "eotg_t.2 = { option = { trigger_event = eotg_t.1 } }",
            "common/scripted_effects/x.txt": "eotg_e = { add_martial = 1 }",
        })
        self.addCleanup(rmtree, self.root)

    def run_main(self, *args):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = L.main(["--root", self.root] + list(args))
        return rc, buf.getvalue()

    def test_exit_codes_and_baseline(self):
        rc, out = self.run_main("--rule", "L008")
        self.assertEqual(rc, 1)
        self.assertEqual(out.count("L008 '"), 2)
        bl = os.path.join(self.root, "bl.json")
        rc, _ = self.run_main("--rule", "L008", "--write-baseline", bl)
        rc, out = self.run_main("--rule", "L008", "--baseline", bl)
        self.assertEqual(rc, 0, out)
        self.assertIn("0 new", out)
        # a new finding beyond the baseline fails
        with open(os.path.join(self.root, "events/e.txt"), "a") as fh:
            fh.write("\neotg_t.3 = { option = { add_learning = 1 } }\n")
        rc, out = self.run_main("--rule", "L008", "--baseline", bl)
        self.assertEqual(rc, 1)
        self.assertIn("add_learning", out)

    def test_baseline_ignores_line_drift(self):
        bl = os.path.join(self.root, "bl.json")
        self.run_main("--rule", "L008", "--write-baseline", bl)
        p = os.path.join(self.root, "events/e.txt")
        with open(p) as fh:
            text = fh.read()
        with open(p, "w") as fh:
            fh.write("\n\n\n" + text)
        rc, out = self.run_main("--rule", "L008", "--baseline", bl)
        self.assertEqual(rc, 0, out)

    def test_paths_filter_and_json(self):
        js = os.path.join(self.root, "out.json")
        rc, out = self.run_main("--rule", "L008", "--json", js,
                                os.path.join(self.root, "common"))
        with open(js) as fh:
            data = json.load(fh)
        self.assertEqual([f["file"] for f in data["findings"]],
                         ["common/scripted_effects/x.txt"])
        self.assertEqual(rc, 1)

    def test_unknown_rule(self):
        with self.assertRaises(SystemExit):
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                L.main(["--root", self.root, "--rule", "L999"])


class RealRepoBaseline(unittest.TestCase):
    """The committed baseline must cover the current tree (skips outside the repo)."""

    def test_repo_matches_baseline(self):
        root = L.DEFAULT_ROOT
        bl = os.path.join(L.HERE, "eotg_lint_baseline.json")
        if not (os.path.isdir(os.path.join(root, "events")) and os.path.exists(bl)):
            self.skipTest("not running inside the mod repo")
        new, _ = L.split_baseline(L.lint(root), L.load_baseline(bl))
        self.assertEqual(new, [], "\n".join(str(f) for f in new))


if __name__ == "__main__":
    unittest.main()
