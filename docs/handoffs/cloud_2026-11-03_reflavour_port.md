# Reflavour port: vanilla-UI terms (cloud, 2026-11-03)

Brief (Part D): port v1's `replace/` reflavour layer to v2 with the current glossary (County = Shoal), one
definition per key, port-don't-invent, BOM, one file per source area, plus a spec.

### HANDOFF (cloud session, unvalidated)
- branch: claude/reflavour-port-cloud (from v2-space-map at 5e6a755)
- status: done
- summary:
  - **Ported 477 v1 term keys into 37 files.** The files are
    `localization/english/replace/eotg_reflavour_<area>_l_english.yml`, each with the required
    `UNVERIFIED-VANILLA` header. They cover concepts, holdings, title tiers, buildings, modifiers, traits, GUI,
    mounts and relationship reasons.
  - **County/Region → Shoal** in prose: 23 values, applied outside formatting tokens.
  - **House-style fixes:** Canadian spelling on 36 lines; dashes, quotes and stray spaces.
  - **Held 693 keys, each listed with its reason** in `docs/specs/reflavour_v2_held_keys.md`:
    - **469 event-prose keys.** Vanilla 1.19 event text with only peasant → commoner changed. Ported, they would
      pin stale text and scopes and stay medieval in tone.
    - **124 in files blocked by pending rulings:** terrains, the wordbank, traditions.
    - **2 "Strike Speeders" keys.**
    - **44 conflicting v1 duplicates.**
    - **40 term keys still carrying a medieval or Earth word.**
    - **14 already owned by `eotg_county_term_l_english.yml`.**
  - **No key is defined twice anywhere in `localization/`.** One BOM per file. No `[scope:`, no "Gob-Corp", no
    literal "knight".
  - **eotg_lint: 0 new findings.** Three plural-pronoun keys were allowlisted, with reasons.
  - **Re-runnable tool:** `docs/tools/reflavour_port.py`, a dry run by default (`--write` regenerates the files).
    Its docstring notes that the hand-applied house-style fixes are not redone.
- files:
  - `localization/english/replace/eotg_reflavour_*.yml` (37 new)
  - `docs/specs/reflavour_v2.md`
  - `docs/specs/reflavour_v2_held_keys.md`
  - `docs/tools/reflavour_port.py`
  - `docs/tools/eotg_lint_pronoun_allowlist.txt` (+3)
- unverified-vanilla:
  - `localization/english/replace/eotg_reflavour_*.yml:3` (every file) — the keys are ported from v1 (CK3 1.19).
    Diff each against 1.20.1.1: dead keys, changed tokens, changed meaning (spec §6.1).
  - spec §6.2 — `replace/` overrides by key whatever the filename (glossary principle 8). The shipped
    county-term file is the precedent.
  - The filter's word list errs towards holding (spec §3.3). One known false positive: "dungeon".
- needs-local-validation: Tiger + PX on `localization/english/replace/`. Also run the spec §6 vanilla diff and the
  in-game checks: holding and tier tooltips, a Shoal county modifier, the travel transports.
- needs-loc:
  - merge the 44 conflicting duplicates;
  - fix and port the 40 medieval-word term keys;
  - sweep for "human" / "man" (spec §4);
  - after the rulings, the 126 blocked keys;
  - the event-prose decision (spec §5.6).
- needs-lore: the holding-type names (spec §5.1), the CB-56 building names (§5.2), "Sanctum Bastion", and the
  government title-tier variants (Free Port, Chapter Post, Berth, Armada…).
- needs-human: the open questions in spec §5:
  - holding names;
  - CB-56;
  - "Realm" stays;
  - Burgher → Contractor and Chivalry → Valour as glossary rows;
  - the terrain, Void and Strike Speeders rulings (glossary §6.1);
  - event prose;
  - gold.
- taskboard: (orchestrator to copy)
  - CB-08 / the glossary items: the port landed for interface terms. The 693 held keys are the remaining
    `replace/` work, split by reason.
  - The glossary §6.2 step 0 dedupe applies only to the 44 held conflicts. The 122 identical duplicates were
    collapsed in the port.
