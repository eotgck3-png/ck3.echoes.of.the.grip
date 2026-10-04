"""Fixture tests for docs/tools/eotg_lint.py: one hit and one non-hit per rule.

Run: python -m unittest discover docs/tools/tests
"""
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
        self.addCleanup(shutil.rmtree, root)
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
    def test_hit(self):
        self.assertHit({"common/decisions/d.txt":
                        "eotg_d = { is_valid = { NOT = { has_character_flag = eotg_cd } } "
                        "is_shown = { has_variable = eotg_v } }"}, "L006", count=2)

    def test_clean(self):
        self.assertClean({"common/decisions/d.txt":
                          "eotg_d = { is_valid = { custom_description = { text = eotg_cd_tt "
                          "NOT = { has_character_flag = eotg_cd } } } "
                          "effect = { add_character_flag = eotg_cd } }"}, "L006")


class L007(LintCase):
    def test_hit_silent_option(self):
        self.assertHit({
            "events/e.txt": EV + "eotg_t.1 = { option = { name = a trigger_event = eotg_t.2 "
                                 "add_character_flag = eotg_f } option = { name = b add_gold = 5 } }",
            "common/scripted_effects/s.txt": "eotg_quiet = { set_variable = { name = eotg_v value = 1 } }",
        }, "L007", count=1, needle="option a")

    def test_hit_via_silent_scripted_effect_and_containers(self):
        self.assertHit({
            "events/e.txt": EV + "eotg_t.1 = { option = { name = a eotg_quiet = yes "
                                 "if = { limit = { always = yes } save_scope_as = eotg_x } } "
                                 "option = { name = b } }",
            "common/scripted_effects/s.txt": "eotg_quiet = { set_variable = { name = eotg_v value = 1 } }",
        }, "L007", count=1)

    def test_clean(self):
        self.assertClean({
            "events/e.txt": EV +
            "eotg_t.1 = { option = { name = a trigger_event = eotg_t.2 custom_tooltip = eotg_tt } "
            "option = { name = b eotg_loud = yes } option = { name = c } }\n"
            "eotg_t.3 = { option = { name = only trigger_event = eotg_t.2 } }\n"
            "eotg_t.4 = { hidden = yes option = { trigger_event = eotg_t.2 } option = { } }",
            "common/scripted_effects/s.txt": "eotg_loud = { add_gold = 5 }",
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


class CLI(unittest.TestCase):
    def setUp(self):
        self.root = make_mod({
            "events/e.txt": EV + "eotg_t.1 = { option = { add_intrigue = 1 } }\n"
                                 "eotg_t.2 = { option = { trigger_event = eotg_t.1 } }",
            "common/scripted_effects/x.txt": "eotg_e = { add_martial = 1 }",
        })
        self.addCleanup(shutil.rmtree, self.root)

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
