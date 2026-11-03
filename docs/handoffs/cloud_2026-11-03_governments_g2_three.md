# Governments G2: PMC, Corporation and Trade Oligarchy signature resources (cloud, 2026-11-03)

Brief: specs shaped like the Cartel's for the three remaining governments, then batch 1 (resource core) for each,
copying the Cartel's validated C1 shapes. Pattern: `docs/specs/governments_v2_g2_cartel.md` and the shipped
`eotg_cartel_*` files (not touched).

### HANDOFF (cloud session, unvalidated)
- branch: claude/governments-g2-three-cloud (from v2-space-map at 7f363f2)
- status: done. All three specs are written, and all three batch-1 builds (P1, CO1, TO1) are built. Later batches
  are specced, not built.
- summary:
  - **Specs.** Each has the Cartel's structure: kind of build and core verb; resource; clamped change effect;
    inheritance; sources and sinks; init and teardown; the §3.15 display; identifier table and story; top- and
    vassal-tier decisions; entry and exit (AI adoption `always = no`); AI and grant fields; lore; loc surface;
    batches; "Proposed events: OWNER APPROVAL REQUIRED" (E1–E5 each); DoD with V-tests; deferred; owner questions
    last, each with a recommended default.
    - **PMC**, `eotg_pmc_standing`:
      - verb: sell the company's force on contract. *Take a Contract* (top) pays gold scaled by standing and
        raises it; *Deliver Results* (vassal) raises its own standing plus a share for a PMC liege; *Recruit on
        Reputation* is a sink that buys an Operator courtier;
      - battles won and lost feed standing (P2), with a yearly drift above 60;
      - exit: *Stand Down the Company* converts standing to prestige. Single-heir succession is kept, per the
        succession spec §11.
    - **Corporation**, `eotg_corp_board_influence` (reserved name kept): the CEO's hold on the board.
      - *Push Through a Restructuring* (top) spends it for income;
      - *Court the Board* (vassal) raises the director's own influence and **erodes the CEO's** (−5);
      - a yearly results feed: solvent +3, in debt −5;
      - batch CO5 makes the built board election read influence bands instead of the councillor proxy.
    - **Trade Oligarchy**, `eotg_gobcorp_market_share`: a contested index.
      - *Corner the Market* (top) takes 5 from every partner Prince;
      - *Undercut a Rival Prince* (vassal) takes 10 from one rival, a weighted random pick, so no picker widget;
      - peace +1 and war −4 a year;
      - batch TO5 swaps the election's gold vote bands for market-share bands.
  - **Batch 1 build, per government:**
    - the role-ladder triggers;
    - the reader, clamp, start and inheritance values;
    - the change, sync, init and teardown effects;
    - a scaled character modifier;
    - a visible story with a `basic_counter` and a monthly self-heal/sync tick;
    - additive on_actions (game start, after lobby, government change, title gain, death);
    - BOM-correct loc.
  - **The resource has exactly one writer**, its change effect (checked by grep). Init, inheritance and every
    later decision go through it. Teardown leaves the variable dormant rather than removing it, so it stays the
    only writer. The exits zero it through the change effect.
  - **Resources follow `primary_heir`.** In `on_death` the heir ends with the higher of its own value and a share
    of the predecessor's: PMC 75%, Corporation 50%, Trade Oligarchy 75%. Under an election, `primary_heir` is the
    vote leader. Init keeps an inherited value rather than overwriting it with the start value.
  - No events or options were added. The Cartel files, the governments and the election file are unchanged
    (their edits are later batches).
- files:
  - new specs:
    - `docs/specs/governments_v2_g2_pmc.md`
    - `docs/specs/governments_v2_g2_corporation.md`
    - `docs/specs/governments_v2_g2_gobcorp.md`
  - new script (×3, for `<g>` = `pmc`, `corporation`, `gobcorp`):
    - `common/scripted_triggers/eotg_<g>_triggers.txt`
    - `common/script_values/eotg_<g>_values.txt`
    - `common/scripted_effects/eotg_<g>_effects.txt`
    - `common/modifiers/eotg_<g>_modifiers.txt`
    - `common/story_cycles/eotg_<g>_story.txt`
    - `common/on_action/eotg_<g>_on_actions.txt`
  - new loc: `localization/english/eotg_pmc_l_english.yml`, `eotg_corporation_l_english.yml`,
    `eotg_gobcorp_l_english.yml` (10 keys each; one BOM each, checked `ef bb bf`)
  - this handoff
- unverified-vanilla:
  - **Built code** (everything else copies a shipped Cartel shape):
    - `common/modifiers/eotg_pmc_modifiers.txt:16`, `eotg_corporation_modifiers.txt:16`,
      `eotg_gobcorp_modifiers.txt:16` — fractional per-unit values (0.01, 0.001, 0.1, 0.0015) under
      `display_mode = scaled`. The Cartel used an integer. Check the character-window tooltip (V-P2, V-CO2,
      V-TO2).
    - Not marked in code because the skill documents the form (`variables.md`): `scope:x.var:y` reads in the
      inheritance values (`common/script_values/eotg_<g>_values.txt:52`) and the story sync
      (`common/scripted_effects/eotg_<g>_effects.txt:48`). The Cartel read `scope:x.dread`, not a variable.
      Check that both values come through in game (V-P4, V-P2).
    - `vassal_opinion` as a modifier key in `eotg_corporation_modifiers.txt`. It is used by shipped mod files
      (5 hits), but they weren't traced to their vanilla source here.
  - **Spec-only** (not built):
    - PMC §5.1 — the combat side → primary-participant link (`side_primary_participant`) on
      `on_combat_end_winner` / `_loser`.
    - PMC §4.1 — a cheap neighbour-at-war check for `ai_will_do` (fallback `is_at_war`).
    - PMC §4.3, §6.1 — a knight-count trigger (fallback: drop the term, or `martial >= 14`); the commander trait
      list.
    - Corporation §4.2 — the `opinion` form in `ai_will_do` (the Cartel uses `"opinion(scope:x)"` in a value).
    - Corporation §6.1 and Trade Oligarchy §6.1 — whether a castle capital is penalized under the city shape
      (V-G17); the capital-holding check form (OQ10).
    - Trade Oligarchy §4.1 — `major_gold_value` (the repo reads `minor_` and `medium_` only); the
      `any_vassal = { count >= 3 }` form.
    - Trade Oligarchy §4.2 — a `weight` block on `random_vassal` reading the candidate's script value (the
      Cartel's walk-off uses the same shape on `random_tributary`).
    - Trade Oligarchy §6.2 — a war-length trigger (fallback `is_at_war`).
- needs-local-validation: Tiger + PX on `common/{scripted_triggers,script_values,scripted_effects,modifiers,story_cycles,on_action}/eotg_{pmc,corporation,gobcorp}_*.txt`
  and `localization/english/eotg_{pmc,corporation,gobcorp}_l_english.yml`.
  - Expected benign: the story fields `visible` / `icon` / `background` / `visualization` (CLAUDE.md).
  - Only `docs/tools/eotg_lint.py` ran here: 0 new findings against the baseline.
  - In game, on the British Isles sub-mod:
    - V-P1–V-P5 (Raoul, d_valois);
    - V-CO1–V-CO5 (Hoël and Konan, k_brittany);
    - V-TO1–V-TO5 (Bertrand, d_provence).
- needs-loc: localizer review of the 30 batch-1 keys. The P3/P4, CO3/CO4 and TO3/TO4 decision loc is listed in
  each spec's §9, and is not written yet.
- needs-lore (each spec's §8):
  - The names: Standing / The Company's Name / Take a Contract / Deliver Results / Recruit on Reputation /
    Run the Realm as a Company / Stand Down the Company.
  - Board Influence / The Board / Hold on the Board / Push Through a Restructuring / Court the Board /
    Incorporate the Realm / Dissolve the Board. Is "CEO" acceptable in prose?
  - Market Share / The Charter Market / Corner the Market / Undercut a Rival Prince / Sign the Charter /
    Dissolve the Charter.
  - Is the PMC's unnamed "client" compatible with "LAW AT 866"? It is a private deal.
- needs-human:
  - **Owner questions, each with a recommended default:**
    - **PMC (`governments_v2_g2_pmc.md` §14):**
      - OQ1: a scripted variable (yes);
      - OQ2: 75% inheritance (yes);
      - OQ3: include the Recruit sink (yes);
      - OQ4: a visible story, the mod's third (yes);
      - OQ5: start 40 / 20 (yes);
      - OQ6: first-pass numbers (approve);
      - OQ7: AI adoption (not yet);
      - OQ8: PMC → Corporation evolution (defer);
      - OQ9: events E1–E5 (none yet).
    - **Corporation (`governments_v2_g2_corporation.md` §14):**
      - OQ1: scripted, not vanilla influence; skip T11 (scripted);
      - OQ2: 50% inheritance (yes);
      - OQ3: directors erode the CEO by 5 (yes);
      - OQ4: a visible story (yes);
      - OQ5: start 50 / 20 (yes);
      - OQ6: numbers (approve);
      - OQ7: AI adoption (not yet);
      - OQ8: events (none yet);
      - OQ9: keep the councillor +1 in the election alongside the bands (no);
      - OQ10: entry requires a Port capital (no; record V-CO10 first).
    - **Trade Oligarchy (`governments_v2_g2_gobcorp.md` §14):**
      - OQ1: scripted (yes);
      - OQ2: 75% inheritance (yes);
      - OQ3: share as an index, not a sum-to-100 market (index);
      - OQ4: a visible story (yes);
      - OQ5: start 40 / 20 (yes);
      - OQ6: numbers (approve);
      - OQ7: AI adoption (not yet);
      - OQ8: events (none yet);
      - OQ9: sort electors by share (no, keep gold);
      - OQ10: Corner hits every vassal Prince, counts included (yes);
      - OQ11: `diplomacy = -1` → `+1` (yes, separately).
  - **In game:** the batch-1 V-tests above, run with CB-49.
  - **The British Isles data has no Trade Oligarchy vassal.** V-TO8 needs two made by console (V-TO9).
- taskboard: (orchestrator to copy; not edited here)
  - New item per government: "G2 <gov> batch 1 in-game validation (V-x1–V-x5)". Owner human; soft dependency
    CB-49.
  - New item per government: "G2 <gov> batches 2–5/6 build after owner rulings". Owner eotg-scripter; blocked by
    the owner questions.
  - **CO5 and TO5 edit `common/succession_election/eotg_government_elections.txt`.** That needs a V-SU re-run;
    sequence it after the succession pass's own validation.
  - Owner decisions: the OQ lists above, and the events (E1–E5 per government).
  - Closes, once validated: template §9.2 item 1 (no signature resource) for these three; assessment GAPs
    pmc G1/Q2, corporation G3, gobcorp G2. Entry/exit (Q5) and grants (§3.14) close with batch 4.
