# Mechanics simulation and balance audit (cloud, 2026-11-03)

Brief (Part F): a simulation harness that models every resource economy and progression system from the actual
script, runs it hard (10,000 × 100 years per system and realm size), reports where the mechanics break, and
proposes value-level tuning, without changing any game script.

### HANDOFF (cloud session, unvalidated)
- branch: claude/mechanics-sim-cloud (from origin/v2-space-map at 4a6191e)
- status: done
- summary:
  - **Base.** `origin/v2-space-map` already holds Part C and the addendum fixes (scaled modifier re-applied;
    Court the Board erosion capped once a year per CEO and only while the director's projected influence exceeds
    the CEO's; Corner the Market once a year per Prince). The models read these from the script rather than
    assuming them.
  - **The script reader** `docs/tools/sim/pdx_read.py`, built on `pdx_parse.py`, evaluates against numpy arrays:
    script values, scripted triggers, decision costs, cooldowns, check intervals, `ai_potential` and
    `ai_will_do`, story `effect_group` intervals, `random_list` weights, and change-effect amounts with their
    conditions. Vanilla named values come from an ASSUMPTION table. `Script.overrides` provides what-if tuning.
  - **Six models** in `docs/tools/sim/models/`, each citing the files it reads:
    - **Cartel:** monthly dread decay, the scaled baseline, demand / acceptance / refusal, Tighten, Lean, the
      walk-off, succession grace, and Kingpin rarity from its `random_list`;
    - **PMC:** the battle feed, drift, the three decisions, exit, inheritance;
    - **Corporation:** the results feed, Restructure, Court the Board with the merged cap, the board election;
    - **Trade Oligarchy:** the peace/war feed, Corner with the merged cap, Undercut (weighted rival), the
      wealth election;
    - **Cybernetics:** settling, the Pursue decision, development gates, the Overclocked accrual calls with
      their conditions, the cascade, NF drift, and the terminal event's option and outcome tables;
    - **Frontier:** the yearly gain formula, completion floors, strain causes, ease, sponsor lapse
      (I2c / F2), and the falter event's options.
  - **Three policies:** `ai` (`ai_will_do` as written), `greedy` (a player at the top with AI vassals) and
    `greedy_all` (everyone greedy; the stress bound).
  - **Runs:** the full grid, 10,000 runs × 100 years × sizes 1/4/8/16, seed 20261103, about 2.5 minutes.
    Results are in `results.json`, with six PNG charts.
  - **The static exploit scan** `docs/tools/sim/exploit_scan.py` reads timed flag and variable guards as
    effective cooldowns. It found no F1 / F4 and no farmable entry/exit loop.
  - **Findings:**
    - **HIGH H1:** Corporation directors can erode the CEO to 0 (52% of runs stuck at 0 for 20+ years with 16
      greedy directors, even with the cap).
    - **HIGH H2:** PMC Standing scales with vassal count (AI equilibrium 29 with 1 vassal, 58 with 16).
    - **MED M1:** the Trade Oligarchy feed is net negative (vassal median 7–10; the vote bands are inert).
    - **MED M2:** Cartel payers walk off right after a succession (0.35 per succession).
    - **MED M3:** cybernetics development gates dominate (a player who pushes reaches Overclocked in 16.8% of
      installs).
    - **MED M4:** the PMC contract pay is tier-flat.
    - **LOW L1–L5:** AI vassal decisions are rare; Frontier strain is world-dependent; Overclocked is short;
      the Kingpin ×0.5 ruling holds; the exploit scan is clean.
  - **`proposed_tuning.patch`** holds P1–P6, one value each, plus the Cartel loc line. `git apply --check`
    passes on 4a6191e. It is **not applied**: tuning is the owner's call.
- files:
  - `docs/tools/sim/`: `pdx_read.py`, `common.py`, `exploit_scan.py`, `run_all.py`, `report_tables.py`,
    `README.md`, `models/{__init__,gov_common,cartel,pmc,corporation,gobcorp,cybernetics,frontier}.py`
  - `docs/qa/mechanics_sim_2026-11-03/`: `REPORT.md`, `results.json`, `exploit_scan.md`,
    `proposed_tuning.patch`, `chart_{cartel,pmc,corporation,gobcorp,cybernetics,frontier}.png`
  - this handoff
  - **No game script, loc or asset changed.**
- unverified-vanilla: none in game script (none was written). The sim's own engine assumptions are in
  `REPORT.md` Appendix C. The weightiest, which decide absolute numbers rather than comparisons, are:
  - `docs/tools/sim/pdx_read.py` `VANILLA_DEFAULTS` — the vanilla gold values (`minor_`/`medium_`/
    `major_gold_value` scale with income in vanilla; per-tier constants here);
  - `docs/tools/sim/models/cartel.py` — `has_dread_level_towards` thresholds (40 / 80); the heir's starting
    dread (0); vanilla dread income (Poisson 0.6 × +12 a year);
  - `docs/tools/sim/common.py` — the war frequency (~23% of years at war), mortality 3.5% a year, gold
    income by tier;
  - `docs/tools/sim/models/cybernetics.py` — the capital development distribution (from balance spec §5.1)
    and its growth.
- needs-local-validation: none for the mod (no script changed). Optional: rerun `python docs/tools/sim/run_all.py`
  after any tuning, and apply `proposed_tuning.patch` on a branch only if the owner approves. Tiger + PX would
  then run on the five changed script files plus `localization/english/eotg_cartel_l_english.yml` (the patch
  keeps the BOM).
- needs-loc: only if P5 is approved: the Cartel story `_info` line ("3 years" → "5 years", already in the patch).
- needs-lore: none.
- needs-human: owner rulings on P1–P6 (REPORT.md "Findings"). Also on L1: whether to raise AI vassal-tier uptake,
  but only after P1.
- taskboard: (orchestrator to copy)
  - New item: "Rule on mechanics-sim proposals P1–P6 (`docs/qa/mechanics_sim_2026-11-03/REPORT.md`); apply
    `proposed_tuning.patch` for those approved".
  - New item: "Rerun the sim after the real map lands (cybernetics development gates, M3) and after any tuning".
