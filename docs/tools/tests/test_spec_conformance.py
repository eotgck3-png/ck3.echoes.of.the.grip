"""Fixture tests for docs/tools/spec_conformance.py.

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
import spec_conformance as S  # noqa: E402

FILES = {
    "events/eotg_x.txt": """namespace = eotg_x
eotg_x.001 = { option = { name = a add_character_flag = eotg_flag_set eotg_fx_effect = yes } }
eotg_x.002 = { trigger = { has_character_flag = eotg_flag_read_only } }
""",
    "common/scripted_effects/eotg_e.txt": "eotg_fx_effect = { }\neotg_secret_effect = { }\n",
    "common/scripted_triggers/eotg_t.txt": "eotg_band_low = { }\neotg_band_high = { }\n",
    "localization/english/eotg_x_l_english.yml": "﻿l_english:\n eotg_x.001.t:0 \"T\"\n",
    # a built spec: 3 ids, 1 missing, plus an exempt line and shorthand
    "docs/specs/cybernetics_v2_alpha.md": """# Alpha

## 3. Identifier table

### 3.1 New

| Type | Key | Where |
|---|---|---|
| event | `eotg_x.001` *First* | `events/eotg_x.txt` |
| scripted effect | `eotg_fx_effect` | effects |
| static modifier | `eotg_mod_gone` | modifiers |

### 3.2 Other

- Bands: `eotg_band_low` / `_high`; flags `eotg_flag_set` and `eotg_flag_read_only`.
- The old `eotg_mod_dropped` is deferred to a later batch.
- Patterns are skipped: `eotg_aug_stress_X_effect`, `eotg_story_`.
- Loc: `eotg_x.001.t`, and `eotg_x_{a,b}_tt`.

```
eotg_in_code_block = yes
```
""",
    # an unbuilt spec: its new event does not exist
    "docs/specs/cybernetics_v2_beta.md": """# Beta

### 3.1 New

| Key | Type |
|---|---|
| `eotg_y.001` | event |
| `eotg_beta_effect` | scripted effect |
| `eotg_x.002` option **c** | new option on an existing event |
""",
    "docs/specs/cybernetics_v2_beta_lore.md": "# Beta lore\n\n- `eotg_beta_tt` wording.\n",
}


def make_mod():
    d = tempfile.mkdtemp(prefix="eotg_conf_")
    for rel, text in FILES.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
    return d


class Analysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = make_mod()
        cls.res = S.analyse(cls.root)
        cls.specs = {s["spec"].split("/")[-1]: s for s in cls.res["specs"]}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root)

    def rows(self, spec):
        return {r["token"]: r for r in self.specs[spec]["ids"]}

    def test_three_ids_one_missing(self):
        r = self.rows("cybernetics_v2_alpha.md")
        self.assertEqual((r["eotg_x.001"]["kind"], r["eotg_x.001"]["status"]), ("event", "defined"))
        self.assertEqual((r["eotg_fx_effect"]["kind"], r["eotg_fx_effect"]["status"]),
                         ("effect", "defined"))
        self.assertEqual((r["eotg_mod_gone"]["kind"], r["eotg_mod_gone"]["status"]),
                         ("modifier", "missing"))
        self.assertTrue(self.specs["cybernetics_v2_alpha.md"]["built"])

    def test_exempt_line(self):
        r = self.rows("cybernetics_v2_alpha.md")["eotg_mod_dropped"]
        self.assertTrue(r["exempt"])
        self.assertEqual(r["status"], "missing")

    def test_shorthand_flags_loc_patterns(self):
        r = self.rows("cybernetics_v2_alpha.md")
        self.assertEqual(r["eotg_band_high"]["status"], "defined")      # `x_low` / `_high`
        self.assertEqual(r["eotg_flag_set"]["status"], "defined")       # set in script
        self.assertEqual(r["eotg_flag_read_only"]["status"], "referenced")   # read, never set
        self.assertEqual(r["eotg_x.001.t"]["kind"], "loc")
        self.assertEqual(r["eotg_x_a_tt"]["status"], "missing")          # brace expansion
        self.assertIn("eotg_x_b_tt", r)
        for skipped in ("eotg_aug_stress_X_effect", "eotg_story_", "eotg_in_code_block", "eotg_x"):
            self.assertNotIn(skipped, r)                                # pattern, prefix, code, path

    def test_unbuilt_and_lore_inherit(self):
        beta = self.specs["cybernetics_v2_beta.md"]
        self.assertFalse(beta["built"])
        self.assertEqual(beta["new_events"], ["eotg_y.001"])     # the existing-event row is not new
        self.assertEqual(self.rows("cybernetics_v2_beta.md")["eotg_beta_effect"]["kind"], "effect")
        self.assertFalse(self.specs["cybernetics_v2_beta_lore.md"]["built"])

    def test_unmentioned(self):
        self.assertEqual(self.res["unmentioned"]["effect"], ["eotg_secret_effect"])
        self.assertNotIn("event", self.res["unmentioned"])     # both events are named somewhere

    def test_report(self):
        text = S.render(self.res)
        self.assertIn("Do not edit by hand", text)
        self.assertIn("| `cybernetics_v2_alpha.md` | yes |", text)
        self.assertIn("| `cybernetics_v2_beta.md` | **no** |", text)
        built = text.split("## Built specs: gaps")[1].split("## Unbuilt specs")[0]
        self.assertIn("`eotg_mod_gone` (modifier, l.11)", built)
        self.assertNotIn("eotg_beta_effect", built)            # unbuilt gaps kept apart
        self.assertIn("Exempt (1): `eotg_mod_dropped`", built)
        self.assertIn("`eotg_secret_effect`", text.split("## In script, mentioned in no spec")[1])


class CLI(unittest.TestCase):
    def test_write_check_crlf_json(self):
        root = make_mod()
        self.addCleanup(shutil.rmtree, root)
        out = os.path.join(root, *S.OUT_REL.split("/"))

        def run(*a):
            with redirect_stdout(io.StringIO()) as buf:
                rc = S.main(["--root", root] + list(a))
            return rc, buf.getvalue()

        self.assertEqual(run("--check")[0], 1)
        self.assertIn("3 missing id(s) in built specs", run()[1])
        self.assertEqual(run("--check")[0], 0)
        with open(out, "rb") as fh:
            data = fh.read()
        with open(out, "wb") as fh:
            fh.write(data.replace(b"\n", b"\r\n"))
        self.assertEqual(run("--check")[0], 0)
        with open(out, "ab") as fh:
            fh.write(b"x\r\n")
        self.assertEqual(run("--check")[0], 1)
        j = os.path.join(root, "c.json")
        run("--json", j, "--out", os.path.join(root, "other.md"))
        with open(j, encoding="utf-8") as fh:
            self.assertEqual(len(json.load(fh)["specs"]), 3)


class RealReportCurrent(unittest.TestCase):
    def test_current(self):
        out = os.path.join(S.DEFAULT_ROOT, *S.OUT_REL.split("/"))
        if not (os.path.isdir(os.path.join(S.DEFAULT_ROOT, "docs", "specs")) and os.path.exists(out)):
            self.skipTest("not running inside the mod repo")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(S.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
