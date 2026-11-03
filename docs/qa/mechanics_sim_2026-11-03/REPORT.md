# Mechanics simulation and balance audit (2026-11-03)

**What this is.** A Monte Carlo audit of the mod's five resource economies (Cartel dread, PMC Standing, Corporation Board Influence, Trade Oligarchy Market Share, Frontier progress and strain) and its two long progression systems (the cybernetics tier ladder and Frontier projects). Each model **reads its numbers from the current script** through `docs/tools/sim/pdx_read.py`: values, decision costs and cooldowns, `ai_will_do`, story ticks, `random_list` weights. A tuning change is therefore measured by rerunning `python docs/tools/sim/run_all.py`.

**Base:** `origin/v2-space-map` at `4a6191e`. It already holds Part C with the local session's addendum fixes: the scaled modifiers re-applied on every change; Court the Board erosion at most once a year per CEO, and only while the director's projected influence exceeds the CEO's; Corner the Market draining each Prince at most once a year. **The models read those fixes from the script; none is assumed.**

**Runs:** 10,000 runs × 100 game years per system × realm size (1, 4, 8, 16 vassals of the same government) × policy, seed 20261103. Frontier: 10,000 projects per type and holder kind. The whole grid takes about 2.5 minutes.

**Policies:**
- `ai` follows `ai_will_do` and `ai_check_interval` as written.
- `greedy` is a player at the top with AI vassals: it takes every resource-raising action when valid and affordable, and never spends on a sink.
- `greedy_all` makes every ruler in the realm greedy. It is the stress bound: multiplayer, or AI weights raised.

**Read the numbers as comparisons.** Wars, gold, deaths, opinions and vanilla voting are proxies (the ASSUMPTION list, Appendix C). A before/after difference under the same assumptions is trustworthy. An absolute equilibrium is indicative.

**Charts:** `chart_<system>.png` in this folder, one per system (AI policy, median with a 10–90% band). **Static exploit scan:** `exploit_scan.md`. **Proposed tuning:** `proposed_tuning.patch`, not applied; tuning is the owner's call. `git apply --check` passes on `4a6191e`.

---

## Findings

Each finding gives the evidence (sim numbers; full tables in Appendix A), the script location, and **one** proposed change to a script value or constant, with the sim's before and after.

### HIGH

**H1. Corporation: directors can erode the CEO to zero, even with the once-a-year cap.**
- **Evidence.** With every director courting the board (`greedy_all`), the CEO sits at 0 influence:
  - 57% of years with 16 directors, and 52% of runs stay at 0 for 20+ years;
  - 31% of years with 8 directors;
  - 8% with 4.

  The merged cap holds erosion to −5 a year per CEO, but that still outruns the +3 results feed, and the "below the director's projected value" condition is nearly always true once directors sit at about 83.

  With AI directors as written, the CEO's equilibrium is 39.5 / 38.0 / 34.8 / 29.0 for 1 / 4 / 8 / 16 directors. The decline is gentle only because AI directors court the board about once in 100 years (L1).
- **Why HIGH:** the obvious fix for L1 (more AI uptake), or multiplayer, turns this into a dead CEO resource.
- **Where:** `common/script_values/eotg_corporation_values.txt:73` (`eotg_corporation_court_erosion_value = -5`), read by `common/decisions/eotg_corporation_decisions.txt:113`.
- **Proposal P1:** `eotg_corporation_court_erosion_value = -2`.

  | Scenario | Metric | Before | After |
  |---|---|---|---|
  | 16 directors, `greedy_all` | runs stuck at 0 for 20+ years | 52.4% | 0.0% |
  | 16 directors, `greedy_all` | equilibrium | 0 | 9.3 |
  | 16 directors, AI | equilibrium | 29.0 | 36.0 |
  | 16 directors, player CEO | equilibrium | 44.3 | 54.6 |

**H2. PMC: Standing scales with vassal count.**
- **Evidence.**
  - AI top equilibrium is 29.1 / 36.5 / 44.4 / 58.2 for 1 / 4 / 8 / 16 vassals.
  - A player top reaches 68.4 / 74.5 / 84.0 / 94.0, and with 16 vassals sits at 100 in 19.2% of years.
  - With every vassal greedy: 56.7% of years at 100 (16), 42.6% (8).

  Each vassal's Deliver Results gives the liege +5 with no per-liege cap. This is the same shape as the last two FIX FIRSTs.
- **Where:** `common/script_values/eotg_pmc_values.txt:78` (`eotg_pmc_deliver_liege_value = 5`), used at `common/decisions/eotg_pmc_decisions.txt:102`.
- **Proposal P2:** `eotg_pmc_deliver_liege_value = 2`.

  | Scenario | Metric | Before | After |
  |---|---|---|---|
  | 16 vassals, AI | equilibrium | 58.2 | 41.2 |
  | 1 vassal, AI | equilibrium | 29.1 | 27.5 |
  | 16 vassals, `greedy_all` | years at 100 | 56.7% | 45.8% |

  A structural cap (once a year per liege, as Court the Board now has) would remove the scaling entirely; that is an owner choice beyond a value change. A liege value of 1 brings 16 vassals down to 34.2 (2,000-run check).

### MED

**M1. Trade Oligarchy: the passive feed is net negative, so Princes sink toward 0 and the market-share vote is nearly inert.**
- **Evidence.**
  - +1 a year at peace and −4 at war averages −0.15 a year at the modelled ~23% of years at war.
  - The median vassal Prince holds 7–10 share (AI, all sizes); the First Prince holds 24–28.
  - The election bands start at 30, so vassal electors almost never carry a band. A non-dynast would win without the dynasty rule in 0.0–0.3% of elections, against 4.6–22.3% for the Corporation (AI).
- **Where:** `common/script_values/eotg_gobcorp_values.txt:63` (`eotg_gobcorp_war_loss_value = -4`), read by the yearly tick in `common/story_cycles/eotg_gobcorp_story.txt`.
- **Proposal P3:** `eotg_gobcorp_war_loss_value = -3` (net +0.08 a year).

  | Scenario | Metric | Before | After |
  |---|---|---|---|
  | 4 Princes, AI | First Prince equilibrium | 23.7 | 33.9 |
  | 4 Princes, AI | vassal median | 10.0 | 15.6 |
  | 16 Princes, AI | First Prince equilibrium | 26.8 | 36.5 |
  | 16 Princes, AI | vassal median | 9.4 | 14.9 |

  Peace +2 instead would lift the vassal median to 48 (2,000-run check), too strong. The bands themselves (30/60/90, `eotg_gobcorp_vote_band_*`) are the second lever if vassals should vote by share.

**M2. Cartel: payers walk off right after a succession, because the 3-year grace ends before the heir's dread recovers.**
- **Evidence.**
  - The heir starts with no dread (ASSUMPTION: dread is personal) and climbs toward the payer baseline at 0.375 a month (decay −0.25, read from the government).
  - With 1–3 payers the baseline (4 per payer) sits under `low_dread` 20, so the walk-off starts the year the grace ends.
  - Walk-offs within 5 years of a succession: 0.41 per succession (1 vassal, AI), 0.35 (4), 0.29 (8), 0.17 (16).
- **Where:** `common/on_action/eotg_cartel_on_actions.txt:111` (`years = 3` on `eotg_cartel_succession_grace`).
- **Proposal P5:** `years = 5`, with the story `_info` loc line updated (the patch includes it).

  | Scenario | Metric | Before | After |
  |---|---|---|---|
  | 4 vassals, AI | walk-offs within 5 years of a succession | 0.354 | 0.000 |
  | 4 vassals, AI | mean payers | 1.77 | 1.89 |
  | 16 vassals, AI | walk-offs within 5 years of a succession | 0.165 | 0.000 |

  Dread equilibria are unchanged (58.0, 67.8).

**M3. Cybernetics: the development gate, not the decision, decides who reaches Overclocked.**
- **Evidence.**
  - The Overclocked gate (development 20) is met by the capitals of about 16% of rulers (vanilla history distribution, balance spec §5.1), growing about +1 a decade.
  - A player who always pushes reaches Overclocked in 16.8% of installs, and within 20 years in 12.6% (duke). The balance spec's target for a pushing player was a median of 12 years and 100% within 20.
  - AI: 2.6% ever, median 48 years.
- **Where:** `common/script_values/eotg_augmentation_values.txt:25` (`eotg_aug_dev_gate_overclocked`, value 20).
- **Proposal P4:** `value = 15`.

  | Scenario | Metric | Before | After |
  |---|---|---|---|
  | Player who always pushes | reach Overclocked | 16.8% | 26.1% |
  | Player who always pushes | within 20 years | 12.6% | 20.7% |
  | Player who always pushes | cascade deaths | 4.6% | 7.2% |
  | AI | reach Overclocked | 2.6% | 3.6% |

  Lowering the Enhanced gate (15 → 10) alone changes nothing at Overclocked. **Retune on the real map:** the space map's development distribution decides this, and the balance spec already flags these gates as provisional.

**M4. PMC: Take a Contract pays a flat 50 + 3 × Standing gold at every tier.**
- **Evidence (static, the script's formula).** At Standing 50 the pay is 200 gold every 3 years, about 67 a year:
  - 2.7× a county's modelled yearly income (25);
  - 1.1× a duke's (60);
  - 0.4× a king's (150).

  The costs around it (minor/medium gold) scale with the realm; this pay does not. A county PMC is overpaid and a kingdom PMC barely notices.
- **Where:** `common/script_values/eotg_pmc_values.txt` (`eotg_pmc_contract_pay_value`).
- **Proposal P6:** `(Standing / 50 + 0.5) × medium_gold_value`, 0.5–2.5× medium gold.

  At Standing 50, with medium gold modelled at 60 / 100 / 180 by tier:

  | Tier | Before | After |
  |---|---|---|
  | County | 200 | 90 |
  | Duke | 200 | 150 |
  | King | 200 | 270 |

  Vanilla's `medium_gold_value` itself scales with income, so the real numbers track the realm.

### LOW

**L1. AI vassal-tier decisions are rare.**
- **Evidence.** Yearly AI uptake at typical states, read from `ai_will_do` and `ai_check_interval_by_tier`:

  | Decision | Yearly uptake |
  |---|---|
  | Court the Board | 3.2% |
  | Undercut a Rival Prince | 2.1% |
  | Deliver Results | 6.9% |
  | Lean on the Locals | 6.9% |

  The grid's measured uptakes are lower still: 0.9–1.7% a vassal a year for Court the Board and Undercut, 2.5% for Deliver Results, 3.7–3.9% for Lean. A given AI vassal therefore takes one every 25–100 years, so the Gate 2 vassal-tier content is seldom seen.
- **Proposal:** raise Court the Board's `ai_will_do` base, 5 → 15, so uptake rises from 3.2% to 5.6% a year. **Apply only after P1** (H1 shows what more courting does to the CEO). Not in the patch.

**L2. Frontier strain rarely forces a falter under ordinary conditions, and bites in a hostile world.**
- **Evidence.**
  - Baseline: completion 99–100%; falters 0.0–0.4% per project (administrative 4.0%).
  - Durations are in the owner's bands: Settlement 11 years (median), sponsored 9, unsponsored 12; Research 14.
  - In a hostile world (war reaching the Shoal 25%/yr, Dangerous 40%, occupied 6%/yr), abandonment rises to 10% (Settlement) and 25–26% (Research, Administrative).
- **Strain works as a world-dependent risk. No change proposed.** Sponsor lapses run 0.20 per project (0.52 when every project is sponsored), mostly sponsor deaths.

**L3. Cybernetics: Overclocked is short.** The median from Overclocked to the cascade is 3–4 years (base accrual 12 plus stress), and about 88% of Overclocked rulers cascade. Seamless is 5.5% of installs for a player who pushes, 0.6% for the AI. This is consistent with "Overclocked is a countdown"; it is recorded for the owner, with no change proposed.

**L4. The Kingpin ×0.5 ruling holds.** The yearly start chance for an augmented ruler, read from the on_action `random_list`:

| Ruler | Non-Cartel | Cartel |
|---|---|---|
| AI | 0.76% | 0.38% |
| Player | 2.97% | 1.51% |

**L5. The exploit scan is clean** (`exploit_scan.md`).
- **No net-positive action without a cooldown, and nothing repeatable monthly.** Timed flag and variable guards are read as effective cooldowns: Frontier Invest 1 year, Maintenance Protocol 3 years.
- **Every entry/exit loop needs at least 10 years**, because `changed_government_recently` (5 years) is set on both sides. Per 10-year cycle:
  - the PMC loop nets at most +50 prestige (−200 −150 +400);
  - the Trade Oligarchy loop turns 350 prestige into at most 500 gold;
  - the Corporation and Cartel loops turn 350 prestige into at most 200 legitimacy.

  None is a farm.
- **The AI never adopts any government (entry `ai_potential = always = no`), by design** (OQ4 / OQ7).

---

## How to verify a proposal in game
- **P1/P2:** play 20 years with 8+ vassals of the government, then read the top's resource in the story counter.
- **P3:** the vassal Princes' median share after 30 years of mixed war and peace.
- **P4:** the observer run's Overclocked population (balance spec §9.2).
- **P5:** `kill` a Cartel ruler with 2 payers, then count walk-offs over the next 5 years.
- **P6:** Take a Contract as a county PMC and as a kingdom PMC.

---

## Appendix A: run tables

Generated by `docs/tools/sim/report_tables.py` from `results.json`.

### Government resources (top ruler), 100 years, 10000 runs per cell

| System | Vassals | Policy | Equilibrium | Settles by year | At 0 | At 100 | 20y stuck at 0 | 20y stuck at 100 | Vassal median | Key counts |
|---|---|---|---|---|---|---|---|---|---|---|
| cartel | 1 | ai | 57.5 | 17 | 7.5% | 0.2% | 0.0% | 0.0% | None | accept_per_run_year 0.075, refusal_per_run_year 0.025, walkoff_per_run_year 0.011, tighten_per_run_year 0.021, lean_per_vassal_year 0.037 |
| cartel | 1 | greedy | 34.0 | 15 | 7.1% | 0.0% | 0.0% | 0.0% | None | accept_per_run_year 0.133, refusal_per_run_year 0.265, walkoff_per_run_year 0.036, tighten_per_run_year 0.000, lean_per_vassal_year 0.038 |
| cartel | 1 | greedy_all | 41.2 | 43 | 5.1% | 0.3% | 0.0% | 0.0% | None | accept_per_run_year 0.149, refusal_per_run_year 0.270, walkoff_per_run_year 0.028, tighten_per_run_year 0.000, lean_per_vassal_year 0.159 |
| cartel | 4 | ai | 58.0 | 16 | 6.2% | 0.7% | 0.0% | 0.0% | None | accept_per_run_year 0.095, refusal_per_run_year 0.033, walkoff_per_run_year 0.011, tighten_per_run_year 0.024, lean_per_vassal_year 0.037 |
| cartel | 4 | greedy | 40.5 | 40 | 5.8% | 0.3% | 0.0% | 0.0% | None | accept_per_run_year 0.147, refusal_per_run_year 0.269, walkoff_per_run_year 0.029, tighten_per_run_year 0.000, lean_per_vassal_year 0.037 |
| cartel | 4 | greedy_all | 65.0 | 48 | 3.8% | 2.6% | 0.0% | 0.0% | None | accept_per_run_year 0.190, refusal_per_run_year 0.219, walkoff_per_run_year 0.010, tighten_per_run_year 0.000, lean_per_vassal_year 0.159 |
| cartel | 8 | ai | 61.5 | 12 | 5.1% | 1.9% | 0.0% | 0.0% | None | accept_per_run_year 0.114, refusal_per_run_year 0.030, walkoff_per_run_year 0.010, tighten_per_run_year 0.027, lean_per_vassal_year 0.039 |
| cartel | 8 | greedy | 49.8 | 56 | 4.7% | 1.4% | 0.0% | 0.0% | None | accept_per_run_year 0.172, refusal_per_run_year 0.223, walkoff_per_run_year 0.022, tighten_per_run_year 0.000, lean_per_vassal_year 0.039 |
| cartel | 8 | greedy_all | 75.5 | 30 | 3.7% | 6.6% | 0.0% | 0.0% | None | accept_per_run_year 0.215, refusal_per_run_year 0.121, walkoff_per_run_year 0.006, tighten_per_run_year 0.000, lean_per_vassal_year 0.159 |
| cartel | 16 | ai | 67.8 | 10 | 4.2% | 5.3% | 0.0% | 0.0% | None | accept_per_run_year 0.145, refusal_per_run_year 0.026, walkoff_per_run_year 0.006, tighten_per_run_year 0.033, lean_per_vassal_year 0.039 |
| cartel | 16 | greedy | 66.5 | 46 | 4.0% | 5.5% | 0.0% | 0.0% | None | accept_per_run_year 0.192, refusal_per_run_year 0.184, walkoff_per_run_year 0.009, tighten_per_run_year 0.000, lean_per_vassal_year 0.039 |
| cartel | 16 | greedy_all | 81.0 | 36 | 3.6% | 9.5% | 0.0% | 0.0% | None | accept_per_run_year 0.223, refusal_per_run_year 0.076, walkoff_per_run_year 0.004, tighten_per_run_year 0.000, lean_per_vassal_year 0.159 |
| pmc | 1 | ai | 29.1 | 18 | 0.8% | 0.0% | 0.4% | 0.0% | 30.9 | take_contract_per_run_year 0.065, recruit_per_run_year 0.017, deliver_per_vassal_year 0.025, stand_down_share 0.019 |
| pmc | 1 | greedy | 68.4 | 13 | 0.0% | 0.2% | 0.0% | 0.0% | 30.9 | take_contract_per_run_year 0.233, recruit_per_run_year 0.000, deliver_per_vassal_year 0.025, stand_down_share 0.000 |
| pmc | 1 | greedy_all | 79.4 | 32 | 0.0% | 3.0% | 0.0% | 0.0% | 66.9 | take_contract_per_run_year 0.234, recruit_per_run_year 0.000, deliver_per_vassal_year 0.136, stand_down_share 0.000 |
| pmc | 4 | ai | 36.5 | 0 | 0.2% | 0.0% | 0.0% | 0.0% | 31.3 | take_contract_per_run_year 0.068, recruit_per_run_year 0.026, deliver_per_vassal_year 0.025, stand_down_share 0.008 |
| pmc | 4 | greedy | 74.5 | 22 | 0.0% | 1.9% | 0.0% | 0.0% | 31.2 | take_contract_per_run_year 0.233, recruit_per_run_year 0.000, deliver_per_vassal_year 0.025, stand_down_share 0.000 |
| pmc | 4 | greedy_all | 97.0 | 15 | 0.0% | 24.9% | 0.0% | 0.0% | 66.1 | take_contract_per_run_year 0.233, recruit_per_run_year 0.000, deliver_per_vassal_year 0.136, stand_down_share 0.000 |
| pmc | 8 | ai | 44.4 | 0 | 0.1% | 0.0% | 0.0% | 0.0% | 32.2 | take_contract_per_run_year 0.068, recruit_per_run_year 0.036, deliver_per_vassal_year 0.026, stand_down_share 0.001 |
| pmc | 8 | greedy | 84.0 | 23 | 0.0% | 7.1% | 0.0% | 0.0% | 32.2 | take_contract_per_run_year 0.233, recruit_per_run_year 0.000, deliver_per_vassal_year 0.026, stand_down_share 0.000 |
| pmc | 8 | greedy_all | 98.0 | 6 | 0.0% | 42.6% | 0.0% | 0.1% | 66.3 | take_contract_per_run_year 0.233, recruit_per_run_year 0.000, deliver_per_vassal_year 0.137, stand_down_share 0.000 |
| pmc | 16 | ai | 58.2 | 4 | 0.0% | 0.6% | 0.0% | 0.0% | 32.3 | take_contract_per_run_year 0.074, recruit_per_run_year 0.050, deliver_per_vassal_year 0.026, stand_down_share 0.001 |
| pmc | 16 | greedy | 94.0 | 15 | 0.0% | 19.2% | 0.0% | 0.0% | 32.3 | take_contract_per_run_year 0.233, recruit_per_run_year 0.000, deliver_per_vassal_year 0.026, stand_down_share 0.000 |
| pmc | 16 | greedy_all | 100.0 | 4 | 0.0% | 56.7% | 0.0% | 3.1% | 66.4 | take_contract_per_run_year 0.233, recruit_per_run_year 0.000, deliver_per_vassal_year 0.137, stand_down_share 0.000 |
| corporation | 1 | ai | 39.5 | 13 | 0.3% | 0.6% | 0.0% | 0.1% | 52.5 | court_per_vassal_year 0.009, erosion_per_run_year 0.007, restructure_per_run_year 0.030 |
| corporation | 1 | greedy | 59.4 | 1 | 0.2% | 11.3% | 0.0% | 13.6% | 52.5 | court_per_vassal_year 0.009, erosion_per_run_year 0.004, restructure_per_run_year 0.000 |
| corporation | 1 | greedy_all | 45.9 | 32 | 0.6% | 7.7% | 0.0% | 9.4% | 95.0 | court_per_vassal_year 0.105, erosion_per_run_year 0.077, restructure_per_run_year 0.000 |
| corporation | 4 | ai | 38.0 | 14 | 0.5% | 0.5% | 0.0% | 0.1% | 54.5 | court_per_vassal_year 0.009, erosion_per_run_year 0.026, restructure_per_run_year 0.028 |
| corporation | 4 | greedy | 57.0 | 0 | 0.3% | 10.6% | 0.0% | 12.8% | 54.4 | court_per_vassal_year 0.009, erosion_per_run_year 0.017, restructure_per_run_year 0.000 |
| corporation | 4 | greedy_all | 9.0 | 60 | 7.7% | 2.4% | 0.1% | 3.4% | 83.2 | court_per_vassal_year 0.105, erosion_per_run_year 0.290, restructure_per_run_year 0.000 |
| corporation | 8 | ai | 34.8 | 16 | 0.9% | 0.4% | 0.0% | 0.1% | 55.0 | court_per_vassal_year 0.010, erosion_per_run_year 0.058, restructure_per_run_year 0.025 |
| corporation | 8 | greedy | 53.0 | 7 | 0.4% | 10.1% | 0.0% | 12.6% | 55.0 | court_per_vassal_year 0.010, erosion_per_run_year 0.038, restructure_per_run_year 0.000 |
| corporation | 8 | greedy_all | 1.0 | 36 | 31.1% | 0.7% | 1.7% | 1.1% | 82.9 | court_per_vassal_year 0.112, erosion_per_run_year 0.525, restructure_per_run_year 0.000 |
| corporation | 16 | ai | 29.0 | 20 | 1.9% | 0.3% | 0.0% | 0.1% | 54.9 | court_per_vassal_year 0.010, erosion_per_run_year 0.118, restructure_per_run_year 0.020 |
| corporation | 16 | greedy | 44.2 | 27 | 1.2% | 8.3% | 0.0% | 10.2% | 54.8 | court_per_vassal_year 0.010, erosion_per_run_year 0.083, restructure_per_run_year 0.000 |
| corporation | 16 | greedy_all | 0.0 | 26 | 57.2% | 0.2% | 52.4% | 0.3% | 82.7 | court_per_vassal_year 0.112, erosion_per_run_year 0.736, restructure_per_run_year 0.000 |
| gobcorp | 1 | ai | 28.2 | 31 | 2.0% | 0.1% | 0.0% | 0.0% | 7.0 | corner_per_run_year 0.019, undercut_per_vassal_year 0.000 |
| gobcorp | 1 | greedy | 49.5 | 39 | 0.6% | 1.5% | 0.0% | 0.4% | 5.0 | corner_per_run_year 0.045, undercut_per_vassal_year 0.000 |
| gobcorp | 1 | greedy_all | 49.5 | 39 | 0.6% | 1.5% | 0.0% | 0.4% | 5.0 | corner_per_run_year 0.045, undercut_per_vassal_year 0.000 |
| gobcorp | 4 | ai | 23.7 | 45 | 2.4% | 0.0% | 0.0% | 0.0% | 10.0 | corner_per_run_year 0.013, undercut_per_vassal_year 0.016 |
| gobcorp | 4 | greedy | 50.0 | 44 | 0.7% | 1.5% | 0.0% | 0.5% | 7.1 | corner_per_run_year 0.045, undercut_per_vassal_year 0.016 |
| gobcorp | 4 | greedy_all | 50.0 | 39 | 0.6% | 1.5% | 0.0% | 0.5% | 10.3 | corner_per_run_year 0.045, undercut_per_vassal_year 0.148 |
| gobcorp | 8 | ai | 27.3 | 38 | 2.0% | 0.0% | 0.0% | 0.0% | 9.5 | corner_per_run_year 0.017, undercut_per_vassal_year 0.017 |
| gobcorp | 8 | greedy | 71.1 | 63 | 0.2% | 6.1% | 0.0% | 1.7% | 5.3 | corner_per_run_year 0.072, undercut_per_vassal_year 0.017 |
| gobcorp | 8 | greedy_all | 70.9 | 60 | 0.2% | 6.2% | 0.0% | 1.6% | 8.8 | corner_per_run_year 0.072, undercut_per_vassal_year 0.149 |
| gobcorp | 16 | ai | 26.8 | 39 | 2.1% | 0.0% | 0.0% | 0.0% | 9.4 | corner_per_run_year 0.017, undercut_per_vassal_year 0.017 |
| gobcorp | 16 | greedy | 71.9 | 63 | 0.2% | 6.4% | 0.0% | 2.0% | 5.3 | corner_per_run_year 0.072, undercut_per_vassal_year 0.017 |
| gobcorp | 16 | greedy_all | 71.4 | 62 | 0.2% | 6.3% | 0.0% | 2.0% | 8.9 | corner_per_run_year 0.072, undercut_per_vassal_year 0.149 |

### Elections (at each top-ruler death)

| System | Vassals | Policy | Elections | Resource leader's pick wins | Non-dynast would win without the dynasty rule |
|---|---|---|---|---|---|
| corporation | 1 | ai | 35026 | 76.7% | 4.6% |
| corporation | 1 | greedy | 35231 | 84.8% | 2.1% |
| corporation | 1 | greedy_all | 34858 | 75.8% | 11.2% |
| corporation | 4 | ai | 34888 | 65.5% | 16.0% |
| corporation | 4 | greedy | 35142 | 71.1% | 8.0% |
| corporation | 4 | greedy_all | 35195 | 63.9% | 50.9% |
| corporation | 8 | ai | 35154 | 60.4% | 11.2% |
| corporation | 8 | greedy | 35138 | 65.8% | 6.0% |
| corporation | 8 | greedy_all | 35145 | 59.7% | 45.1% |
| corporation | 16 | ai | 35005 | 60.3% | 22.3% |
| corporation | 16 | greedy | 35211 | 64.4% | 14.1% |
| corporation | 16 | greedy_all | 35308 | 59.0% | 66.9% |
| gobcorp | 1 | ai | 35116 | 98.1% | 0.0% |
| gobcorp | 1 | greedy | 34991 | 99.7% | 0.0% |
| gobcorp | 1 | greedy_all | 34991 | 99.7% | 0.0% |
| gobcorp | 4 | ai | 34963 | 80.6% | 0.1% |
| gobcorp | 4 | greedy | 34705 | 91.3% | 0.0% |
| gobcorp | 4 | greedy_all | 34895 | 89.5% | 0.0% |
| gobcorp | 8 | ai | 34909 | 75.8% | 0.2% |
| gobcorp | 8 | greedy | 35130 | 91.1% | 0.0% |
| gobcorp | 8 | greedy_all | 34997 | 90.1% | 0.0% |
| gobcorp | 16 | ai | 35288 | 75.7% | 0.3% |
| gobcorp | 16 | greedy | 34964 | 91.3% | 0.0% |
| gobcorp | 16 | greedy_all | 35069 | 90.0% | 0.0% |

### Cartel payers and succession

| Vassals | Policy | Payers (last 20 y, mean) | Walk-offs within 5 y of a succession, per succession |
|---|---|---|---|
| 1 | ai | 1.34 | 0.412 |
| 1 | greedy | 2.89 | 0.381 |
| 1 | greedy_all | 3.61 | 0.306 |
| 4 | ai | 1.77 | 0.354 |
| 4 | greedy | 3.55 | 0.312 |
| 4 | greedy_all | 5.13 | 0.118 |
| 8 | ai | 2.18 | 0.287 |
| 8 | greedy | 4.43 | 0.207 |
| 8 | greedy_all | 5.53 | 0.083 |
| 16 | ai | 2.80 | 0.165 |
| 16 | greedy | 5.20 | 0.091 |
| 16 | greedy_all | 5.62 | 0.073 |

### Cybernetics (one ruler from installation; tier by realm size)

| Vassals | Policy | Reach Enhanced | Reach Overclocked | OC within 20 y | Cascade (NF) | Seamless | Cascade death | Natural death | Median years to OC | to NF |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ai | 12.7% | 2.8% | 0.2% | 2.3% | 0.5% | 0.8% | 96.5% | 48.0 | 50.0 |
| 1 | greedy | 33.2% | 16.3% | 12.3% | 14.3% | 5.3% | 4.2% | 93.5% | 14.0 | 17.0 |
| 1 | greedy_all | 33.2% | 16.3% | 12.3% | 14.3% | 5.3% | 4.2% | 93.5% | 14.0 | 17.0 |
| 4 | ai | 12.6% | 2.6% | 0.2% | 2.3% | 0.6% | 0.7% | 96.8% | 48.0 | 50.5 |
| 4 | greedy | 33.2% | 16.8% | 12.6% | 14.8% | 5.5% | 4.6% | 92.9% | 14.0 | 18.0 |
| 4 | greedy_all | 33.2% | 16.8% | 12.6% | 14.8% | 5.5% | 4.6% | 92.9% | 14.0 | 18.0 |
| 8 | ai | 12.9% | 2.6% | 0.2% | 2.3% | 0.5% | 0.9% | 96.4% | 48.5 | 51.0 |
| 8 | greedy | 33.3% | 16.7% | 12.6% | 14.7% | 5.5% | 4.5% | 93.1% | 14.0 | 17.0 |
| 8 | greedy_all | 33.3% | 16.7% | 12.6% | 14.7% | 5.5% | 4.5% | 93.1% | 14.0 | 17.0 |
| 16 | ai | 12.9% | 2.7% | 0.2% | 2.4% | 0.8% | 0.8% | 96.9% | 43.0 | 46.0 |
| 16 | greedy | 33.6% | 17.1% | 13.2% | 15.2% | 5.3% | 5.0% | 92.7% | 14.0 | 18.0 |
| 16 | greedy_all | 33.6% | 17.1% | 13.2% | 15.2% | 5.3% | 5.0% | 92.7% | 14.0 | 18.0 |

### Frontier (one project; 100-year horizon)

| Type / holder | Completed | Abandoned | Years to complete (median / p90) | Falters per project | Sponsor lapses per project |
|---|---|---|---|---|---|
| settlement|ai | 100.0% | 0.0% | 11.0 / 13.0 | 0.001 | 0.204 |
| settlement|player | 100.0% | 0.0% | 11.0 / 13.0 | 0.002 | 0.206 |
| trade|ai | 100.0% | 0.0% | 13.0 / 15.0 | 0.002 | 0.202 |
| trade|player | 100.0% | 0.0% | 13.0 / 15.0 | 0.003 | 0.205 |
| mining|ai | 100.0% | 0.0% | 13.0 / 15.0 | 0.002 | 0.219 |
| mining|player | 99.9% | 0.1% | 13.0 / 15.0 | 0.003 | 0.221 |
| military|ai | 100.0% | 0.0% | 13.0 / 15.0 | 0.000 | 0.219 |
| military|player | 100.0% | 0.0% | 13.0 / 15.0 | 0.000 | 0.223 |
| religious|ai | 99.9% | 0.1% | 14.0 / 16.0 | 0.003 | 0.225 |
| religious|player | 99.9% | 0.1% | 14.0 / 16.0 | 0.004 | 0.227 |
| research|ai | 99.9% | 0.1% | 15.0 / 17.0 | 0.004 | 0.232 |
| research|player | 99.9% | 0.1% | 15.0 / 17.0 | 0.005 | 0.232 |
| administrative|ai | 98.7% | 1.3% | 13.0 / 15.0 | 0.040 | 0.223 |
| administrative|player | 98.7% | 1.3% | 13.0 / 15.0 | 0.043 | 0.220 |
| settlement|ai|sponsored=0.0 | 100.0% | 0.0% | 12.0 / 13.0 | 0.001 | 0.000 |
| settlement|ai|sponsored=1.0 | 100.0% | 0.1% | 9.0 / 12.0 | 0.001 | 0.516 |

### Proposals, before and after

**P1** `corporation` override {'eotg_corporation_court_erosion_value': -2}:

| Vassals | Policy | Metric | Before | After |
|---|---|---|---|---|
| 16 | greedy_all | equilibrium | 0.000 | 9.250 |
| 16 | greedy_all | dead_lo_20y | 0.524 | 0.000 |
| 16 | greedy_all | at_hi | 0.002 | 0.017 |
| 16 | greedy_all | at_lo | 0.572 | 0.058 |
| 16 | greedy_all | vassal_eq | 82.719 | 82.719 |
| 16 | ai | equilibrium | 29.000 | 36.000 |
| 16 | ai | dead_lo_20y | 0.000 | 0.000 |
| 16 | ai | at_hi | 0.003 | 0.004 |
| 16 | ai | at_lo | 0.019 | 0.006 |
| 16 | ai | vassal_eq | 54.902 | 54.902 |
| 16 | greedy | equilibrium | 44.250 | 54.562 |
| 16 | greedy | dead_lo_20y | 0.000 | 0.000 |
| 16 | greedy | at_hi | 0.083 | 0.100 |
| 16 | greedy | at_lo | 0.012 | 0.003 |
| 16 | greedy | vassal_eq | 54.797 | 54.797 |

**P2** `pmc` override {'eotg_pmc_deliver_liege_value': 2}:

| Vassals | Policy | Metric | Before | After |
|---|---|---|---|---|
| 16 | ai | equilibrium | 58.250 | 41.195 |
| 16 | ai | dead_lo_20y | 0.000 | 0.000 |
| 16 | ai | at_hi | 0.006 | 0.000 |
| 16 | ai | at_lo | 0.000 | 0.001 |
| 16 | ai | vassal_eq | 32.266 | 32.266 |
| 1 | ai | equilibrium | 29.109 | 27.500 |
| 1 | ai | dead_lo_20y | 0.004 | 0.006 |
| 1 | ai | at_hi | 0.000 | 0.000 |
| 1 | ai | at_lo | 0.008 | 0.011 |
| 1 | ai | vassal_eq | 30.938 | 30.938 |
| 16 | greedy_all | equilibrium | 100.000 | 100.000 |
| 16 | greedy_all | dead_lo_20y | 0.000 | 0.000 |
| 16 | greedy_all | at_hi | 0.567 | 0.458 |
| 16 | greedy_all | at_lo | 0.000 | 0.000 |
| 16 | greedy_all | vassal_eq | 66.425 | 66.425 |

**P3** `gobcorp` override {'eotg_gobcorp_war_loss_value': -3}:

| Vassals | Policy | Metric | Before | After |
|---|---|---|---|---|
| 4 | ai | equilibrium | 23.656 | 33.875 |
| 4 | ai | dead_lo_20y | 0.000 | 0.000 |
| 4 | ai | at_hi | 0.000 | 0.000 |
| 4 | ai | at_lo | 0.024 | 0.007 |
| 4 | ai | vassal_eq | 10.000 | 15.589 |
| 16 | ai | equilibrium | 26.750 | 36.500 |
| 16 | ai | dead_lo_20y | 0.000 | 0.000 |
| 16 | ai | at_hi | 0.000 | 0.001 |
| 16 | ai | at_lo | 0.021 | 0.006 |
| 16 | ai | vassal_eq | 9.379 | 14.898 |

**P4** `cybernetics` override {'eotg_aug_dev_gate_overclocked': 15}:

| Vassals | Policy | Metric | Before | After |
|---|---|---|---|---|
| 4 | ai | reach_3 | 0.026 | 0.036 |
| 4 | ai | oc_within_20y | 0.002 | 0.003 |
| 4 | ai | cascade_death | 0.007 | 0.012 |
| 4 | greedy | reach_3 | 0.168 | 0.261 |
| 4 | greedy | oc_within_20y | 0.126 | 0.207 |
| 4 | greedy | cascade_death | 0.046 | 0.072 |

**P5** `cartel` override {'eotg_cartel_on_death.years': 5}:

| Vassals | Policy | Metric | Before | After |
|---|---|---|---|---|
| 4 | ai | equilibrium | 58.000 | 58.000 |
| 4 | ai | dead_lo_20y | 0.000 | 0.000 |
| 4 | ai | at_hi | 0.007 | 0.007 |
| 4 | ai | at_lo | 0.062 | 0.060 |
| 4 | ai | post_succession_walkoffs | 0.354 | 0.000 |
| 4 | ai | payers_eq | 1.773 | 1.885 |
| 16 | ai | equilibrium | 67.750 | 67.750 |
| 16 | ai | dead_lo_20y | 0.000 | 0.000 |
| 16 | ai | at_hi | 0.053 | 0.053 |
| 16 | ai | at_lo | 0.042 | 0.042 |
| 16 | ai | post_succession_walkoffs | 0.165 | 0.000 |
| 16 | ai | payers_eq | 2.799 | 2.871 |



## Appendix B: the static exploit scan

See `exploit_scan.md` (generated by `docs/tools/sim/exploit_scan.py`).

## Appendix C: the full ASSUMPTION list

Every number that is not read from the mod's script. The model files carry the same list as `assume()` calls with comments; the reader's `VANILLA_DEFAULTS` holds the vanilla named values. Unresolved names evaluated to 0 or false.

### Models

- `trait_freq`: ({'greedy': 0.12, 'ambitious': 0.12, 'compassionate': 0.1, 'content': 0.1, 'craven': 0.1, 'brave': 0.12, 'paranoid': 0.08, 'sadistic': 0.05, 'callous': 0.08, 'arbitrary': 0.08, 'just': 0.1, 'honest': 0.1, 'arrogant': 0.1, 'cynical': 0.08, 'zealous': 0.1, 'deceitful': 0.1}, 'about 1 in 10 per personality trait (3 traits of ~30)')
- `ruler_mortality_per_year`: (0.035, 'mean reign about 28 years')
- `war_start_per_year`: (0.15, 'a realm enters a war 0.15/yr')
- `war_end_per_year`: (0.5, 'wars last about 2 years; ~23% of years at war')
- `battles_per_war_year`: (2.0, 'Poisson mean, as war leader')
- `battle_win_chance`: (0.5, 'even odds')
- `gold_income_by_tier`: ({2: 25.0, 3: 60.0, 4: 150.0, 5: 300.0}, 'net yearly income')
- `gold_saved_share`: (0.35, 'the rest goes to vanilla spending (MAA, buildings)')
- `debt_shock_per_year`: (0.06, 'chance a year ends in debt (war, ransom, overspend)')
- `realm_shapes`: ({1: (3, [2]), 4: (3, [2, 2, 2, 2]), 8: (4, [3, 3, 2, 2, 2, 2, 2, 2]), 16: (4, [3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])}, '1/4 vassals under a duke, 8/16 under a king, a quarter dukes')
- `DREAD_MONTHLY_CHANGE`: (0.5, 'cited: 00_defines.txt:122 (Cartel spec §2.4)')
- `MAX_DREAD`: (100, 'cited: 00_defines.txt:120')
- `cartel_independent_neighbours`: (6, 'independent neighbouring rulers that can be put on the schedule')
- `cartel_target_tier_mix`: ({2: 0.5, 3: 0.35, 4: 0.15}, 'neighbour highest-tier mix')
- `dread_level_thresholds`: ((40, 80), 'has_dread_level_towards level 1 at dread>=40, level 2 at >=80 (engine; boldness-relative in vanilla)')
- `payer_cease_paying_per_year`: ({1: 0.03, 2: 0.08}, 'vanilla cease_paying_tribute by a low/high-tax payer')
- `heir_starting_dread`: (0.0, 'dread is personal; the heir starts with none')
- `kingpin_chain_dread`: (20.0, 'net dread from a kingpin chain (beats +5..+30, spec I2d §7.2)')
- `vanilla_dread_income`: ((0.6, 12.0), 'dread from vanilla acts (executions, imprisonments, murders): Poisson 0.6 acts a year x +12 before the gain multiplier; the AI Cartel with none sits at 0')
- `cartel_target_rivalry`: ('none', 'no target is a rival or nemesis of the actor in ai_accept')
- `recipient_opinion_sd`: (15.0, 'opinion of the actor ~ N(0, 15) in ai_accept')
- `election_model`: ({'dynasty_candidates': 3, 'candidate_skill': "N(12, 4) stewardship+diplomacy, scored by each election's own skill value", 'self_vote': 'an elector who is a candidate votes for themself (vanilla elector_self_voting_pattern)', 'holder_pattern': 'the holder backs the dynasty candidate with the best skill', 'elector_noise': 'N(0, 15) per elector and candidate on the candidate score', 'non_dynasty_candidates_without_rule': 'every landed vassal elector of the same government'}, 'vanilla voting patterns are scripted modifiers this session cannot read; this is a proxy')
- `pmc_knights`: (4, 'court knights held by a PMC top (knight_limit +2 from the government)')
- `pmc_knight_limit`: (6, 'vanilla limit about 4 plus the government +2')
- `corp_liege_dislikes_director`: (0.25, 'share of directors whose CEO opinion of them is below 0')
- `corp_director_is_powerful_or_councillor`: (0.5, 'chance a director qualifies as an elector beyond the top 6 by tier')
- `capital_dev_share_at_least`: ({10: 0.486, 20: 0.163, 35: 0.013}, 'cited: balance spec §5.1 (vanilla history titles, n = 4,288); log-linear between points')
- `pursue_event_follow_through`: (0.9, 'the sought event: decline options carry factor 0.1 (balance §5.1 item 3)')
- `unsolicited_upgrade_per_year`: (0.03, 'the random Upgrade branches in the tier pools (weights 30 / 25)')
- `upgrade_affordable_share`: (0.7, 'eotg_aug_can_afford_upgrade / gold >= major_gold_value when the AI wants it')
- `stress_level_dist`: ({0: 0.35, 1: 0.35, 2: 0.2, 3: 0.1}, 'Overclocked and later (stress_gain_mult +0.4); resampled with 70% persistence')
- `vendor_flag_shares`: ({'eotg_flag_aug_hidden_flaw': 0.15, 'eotg_flag_aug_vendor_bold': 0.1, 'eotg_flag_aug_vendor_safe': 0.1}, 'install vendor outcomes')
- `event_option_risk_relief_per_year`: (-2.0, 'calm options in the Overclocked / NF pools, averaged')
- `terminal_survivor_risk_reset`: (60.0, 'a non-fatal, non-Seamless terminal outcome leaves risk at 60 (fracture.029 sets 60)')
- `capital_dev_growth_per_year`: (0.1, 'vanilla development growth of a capital, about +1 a decade')
- `implant_technician_employed`: (False, 'no Implant Technician court position (wear relief reads it)')
- `physician_access`: (0.5, 'eotg_has_physician_access at the terminal')
- `frontier_start_dev`: ((0, 3), 'an Unsettled Shoal starts at development 0-3')
- `frontier_start_control`: ((30, 70), 'county control at the start')
- `frontier_control_growth_per_year`: (10, 'vanilla control recovery toward 100')
- `frontier_dev_milestones`: ((33, 66), '+1 development at each milestone (at most 2), eotg_frontier_milestone_effect')
- `frontier_founder_skill`: ((10, 4), 'founder type skill ~ N(10, 4)')
- `frontier_sponsored_share`: (0.4, 'share of projects with a sponsor at start')
- `frontier_sponsor_cannot_pay_per_year`: (0.05, 'sponsor gold below the yearly payment')
- `frontier_sponsor_can_pay_twice`: (0.6, 'at the falter, the sponsor holds 2x the payment')
- `frontier_occupied_per_year`: (0.02, 'the Shoal is occupied in a given year')
- `frontier_war_reaches_per_year`: (0.07, 'holder at war (~23%) x the war reaching the Shoal (~0.3)')
- `frontier_trait_dangerous`: (0.15, 'Shoals with the Dangerous trait')
- `frontier_trait_hostile`: (0.15, 'Shoals with the Hostile trait (no quiet-year ease)')
- `frontier_event_progress_per_year`: (0.5, 'mean progress from the flavour pool')
- `frontier_event_strain_per_year`: (0.1, 'chance the flavour pool adds 1 strain')
- `frontier_player_appoints_founder`: (0.8, 'a player holder replaces a dead founder within the year')
- `frontier_holder_skill`: (10.0, "the holder's type skill read by eotg_frontier_type_input_value")
- `frontier_holder_gold_2x_minor`: (0.6, 'holder gold >= 2 x minor_gold_value at the falter')
- `pmc_under_contract_years`: (2, 'eotg_pmc_under_contract_modifier years = 2 (decision effect)')

### Reader: vanilla named values and unresolved names

- `medium_dread_gain`: cited: Cartel spec §2.5 (Lean +20)
- `miniscule_dread_gain`: cited: Cartel spec §2.5 (Lean liege +5)
- `high_dread`: cited: 00_basic_values.txt:995
- `medium_gold_value`: ASSUMPTION: vanilla scales with income
- `GOLD_BY_TIER`: ASSUMPTION: gold values scale by tier {2: 0.6, 3: 1.0, 4: 1.8, 5: 3.0}
- `minor_gold_value`: ASSUMPTION: vanilla scales with income; county-duke mid value
- `major_gold_value`: ASSUMPTION: vanilla scales with income
- `unresolved:scope:court_position:eotg_aug_implant_technician_court_position`: ASSUMPTION: unresolved name evaluated as 0/false
- `unresolved:piety_level`: ASSUMPTION: unresolved name evaluated as 0/false

### Model choices that are assumptions too
- **Yearly steps** (Cartel dread decays monthly).
- **AI decisions:** `ai_will_do` is the % chance per check (`_decisions.info`), converted to a yearly chance; character interactions use the same rule with `ai_frequency_by_tier`.
- **The greedy policy** never spends a resource on a sink (no Recruit, Restructure or Tighten).
- **Elections:** dynasty candidates (3, skill N(12,4)); electors vote by skill plus noise; electors who are candidates vote for themselves; the holder backs the best dynasty candidate. Vote strength itself is read from each election's `elector_vote_strength`.
- **Exits:** Stand Down is counted but the run continues as a PMC.
- **Cybernetics models one ruler from installation** (installation rates are not modelled), with no downgrade or excision decisions, and no sedation or restraint in the NF drift.
- **Frontier models one project at a time;** realm size does not apply to it.
