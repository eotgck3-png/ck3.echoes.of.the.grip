### HANDOFF (cloud session; validated in the sandbox, not against game files)
- **branch:** `claude/religion-port-fix6-cloud` (from `origin/v2-space-map` @ `c970d3c`)
- **status:** done (FIX 6 items 1–6, and the FIX 1 CRLF check)
- **summary:** applied the `docs/port/religion_1_20/VERIFY_2026-10-04.md` fix list to `docs/tools/port_religions_1_20.py` and regenerated the staged output. Empty doctrine groups were left unfilled (design call).
  1. **Family tenet icons:** all 4 families use the vanilla set (`tenet_banner_known_core` / `_unknown_heretical` / `_known_neutral` / `_unknown_neutral`). The sibling TODOs are gone.
  2. **Divine Order gfx:** `christian_gfx` → `orthodox_gfx`. The rename also applies at religion level if it ever appears there.
  3. **Faith icons:** every faith now has an explicit `icon`. They come from one table, `FAITH_ICON_BY_FAMILY` (`orthodox` for Divine Order) with `DEFAULT_FAITH_ICON = germanic_pagan` for the rest. **These basenames are UNVERIFIED-VANILLA. Check them with `ls game/gfx/interface/icons/faith/` and edit the table if needed** (one line each).
  4. **Hostility doctrine:** every religion gets `doctrine = <family hostility_doctrine>`, never a duplicate. Result: 3 abrahamic, 8 pagan.
  5. **PORT_REPORT.md:**
     - A1, A4, A5 and A7 moved to "Confirmed"; A2 and A3 corrected.
     - The 3 sibling-icon TODOs removed. The per-faith "no icon" TODO is replaced by "replace placeholder icon (B-ART)".
     - New sections: "UNVERIFIED-VANILLA" (the icon basenames; whether the hostility doctrine is required) and "Design calls" (empty doctrine groups, not filled).
  6. **Holy sites:** the commented v1 `holy_site =` lines are now `# holy_sites = { … }` / `# eminent_holy_sites = { }`.
- **FIX 1 (CRLF):**
  - `--check` now ignores CRLF vs LF, and compares only generated files, so `VERIFY_*.md` is left alone.
  - Verified on a real `core.autocrlf=true` clone: the staged files are CRLF there, `--check` passes, 70 unit tests pass, and `eotg_lint --baseline` reports 0 new findings.
- **files:**
  - `docs/tools/port_religions_1_20.py`
  - `docs/tools/tests/test_port_religions.py`
  - `docs/port/religion_1_20/{PORT_REPORT.md, common/religion/**}`
  - this handoff
- **validation:**
  - `python -m unittest discover -s docs/tools/tests` → 70 OK.
  - `port_religions_1_20.py --check` → current, on both the LF and CRLF checkouts.
  - `eotg_lint --baseline` → 28 known, 0 new.
- **unverified-vanilla:**
  - the faith icon basenames `orthodox` and `germanic_pagan`;
  - BEHAVIOUR: whether the hostility doctrine is required, whether empty doctrine groups break anything, and how a missing icon behaves. These are in-game tests per the VERIFY file.
- **needs-human:** none new. The empty doctrine groups stay a design call (B-FAITHS).
