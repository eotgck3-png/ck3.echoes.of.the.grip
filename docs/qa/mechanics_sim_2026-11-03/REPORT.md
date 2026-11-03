# Mechanics simulation and balance audit (2026-11-03)

**What this is.** A Monte Carlo audit of the mod's five resource economies (Cartel dread, PMC Standing, Corporation Board Influence, Trade Oligarchy Market Share, Frontier progress and strain), its two long progression systems (the cybernetics tier ladder and Frontier projects), and Void Corruption (exposure and Hollowing depth; section near the end). Each model **reads its numbers from the current script** through `docs/tools/sim/pdx_read.py`: values, decision costs and cooldowns, `ai_will_do`, story ticks, `random_list` weights. A tuning change is therefore measured by rerunning `python docs/tools/sim/run_all.py`.

**Base:** `origin/v2-space-map` at `4a6191e`. It already holds Part C with the local session's addendum fixes: the scaled modifiers re-applied on every change; Court the Board erosion at most once a year per CEO, and only while the director's projected influence exceeds the CEO's; Corner the Market draining each Prince at most once a year. **The models read those fixes from the script; none is assumed.**

**Runs:** 10,000 runs × 100 game years per system × realm size (1, 4, 8, 16 vassals of the same government) × policy, seed 20261103. Frontier: 10,000 projects per type and holder kind.

**Reproduce every number here:** `python docs/tools/sim/run_all.py --checks --hostile` (numpy and matplotlib). About 6.5 minutes on the local machine; about 3 minutes on the 4-core cloud container. `--checks` adds the 2,000-run side checks and the war-share sweep; `--hostile` adds the Frontier hostile world (L2). `results.json` is not committed (gitignored): it is deterministic from the seed.

**Revised 2026-11-03 (H2a), after the local audit reran the sim:** vassals now carry their own war state (they had taken the top's), the cybernetics development sample is conditioned on the initiation gate, the Cartel walk-off is measured over 10 years, and P6 is marked not simulated. M1, M2, M3 and M4 are rewritten; the recommendation table below is new.

**Policies:**
- `ai` follows `ai_will_do` and `ai_check_interval` as written.
- `greedy` is a player at the top with AI vassals: it takes every resource-raising action when valid and affordable, and never spends on a sink.
- `greedy_all` makes every ruler in the realm greedy. It is the stress bound: multiplayer, or AI weights raised.

**Read the numbers as comparisons.** Wars, gold, deaths, opinions and vanilla voting are proxies (the ASSUMPTION list, Appendix C). A before/after difference under the same assumptions is trustworthy. An absolute equilibrium is indicative.

**Charts:** `chart_<system>.png` in this folder, one per system (`chart_void.png`: the contact sweep) (AI policy, median with a 10–90% band). **Static exploit scan:** `exploit_scan.md`. **Proposed tuning:** `proposed_tuning.patch`, not applied; tuning is the owner's call. `git apply --check` passes on the merged tree (`v2-space-map` with the Void post-merge fixes). The patch now carries the matching loc for P1, P2, P3, P5 and P6.

---

## Recommendations

| Call | Proposal | Change | Why (this rerun) |
|---|---|---|---|
| **Take now** | **P5** | Cartel succession grace 3 → 5 years (`eotg_cartel_on_actions.txt:111`, story loc) | Walk-offs within 10 years of a succession halve: 0.436 → 0.218 (4 vassals), 0.146 → 0.043 (16). Dread equilibria unchanged. |
| **Take now** | **P1** | Court the Board erosion −5 → −2 (`eotg_corporation_values.txt:73`, two loc lines) | A dead CEO resource under full director pressure goes away (runs stuck at 0 for 20+ years: 52.2% → 0.0%); AI and player CEOs gain 5–8 points. |
| **Owner call (structural)** | **P2-cap** | Deliver Results feeds the liege at most once a year (as Court the Board's cap). Not a value change: a guard variable in the decision. | Against the AI as written it only trims the 16-vassal equilibrium (59.8 → 56.2) because AI vassals deliver rarely; under full pressure years at 100 fall 77.8% → 57.0%. P2's value change does more for the AI case (→ 42.8). Choose the shape: a cap (scale-free, mild) or the value (P2, strong). |
| **Take now** | **V1** | Void: Touched accrual term +6 → +2 (`eotg_void_values.txt:16`) | The six Touched events are almost never seen: Touched lasts a median 4 years under a 5-year cooldown. V1 raises them 5.5× (0.038 → 0.211 per 100 seat-years) and trims Hollowings (26.4% → 22.8% of seats in 100 years). See the Void section. |
| **Owner call** | **V2** | Void: 0004 roll 12% → 25% (`eotg_void_on_actions.txt:184`) | The Voidwalker arrives too late to matter (Touched, given contact: 34.7% without one, 31.4% as scripted). V2 doubles arrivals (0.50 → 0.94 per 100 seat-years) for a small cut (31.4% → 29.3%). Whether Voidwalkers should be common is a design call. |
| **Keep** | Q5 | Void contact 4% player / 1% AI (`eotg_void_values.txt:60-66`) | Within 50 years: 86.6% of player seats contacted and 13.4% ever Touched; AI 40.3% and 4.6%. Scales almost linearly with the rate (sweep below). |
| **Hold** | P2 | Deliver Results liege +5 → +2 | Wait for the P2-cap decision: both together over-correct the small realm. |
| **Hold** | P3 | Trade Oligarchy war loss −4 → −3 | The finding flipped (M1): vassal Princes already out-share the First Prince. P3 lifts the First Prince (23.3 → 33.8) but rests on the war-share proxy, which sits on the knife-edge (feed turns negative above 20% war; the model has ~23%). Measure the real war share first. |
| **Hold** | P4 | Overclocked gate 20 → 15 | With the initiation gate conditioned, a pushing player already reaches Overclocked in 34% of installs; P4 takes it to 51% and cascade deaths 9.4% → 14.5%. Retune on the real map's development distribution. |
| **Hold** | P6 | Contract pay scaled by medium gold | **Not simulated:** the gold proxy is about 2× vanilla's medium gold, and vanilla's floor of 50 (`00_basic_values.txt:82`) gives a count and a duke the same 75. |

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

  With AI directors as written, the CEO's equilibrium is 39.6 / 38.5 / 36.6 / 32.5 for 1 / 4 / 8 / 16 directors. The decline is gentle only because AI directors court the board about once in 100 years (L1).
- **Why HIGH:** the obvious fix for L1 (more AI uptake), or multiplayer, turns this into a dead CEO resource.
- **Nested realms (local audit).** Only the top's **direct** vassals can erode the CEO: the erosion branch tests `liege ?= { eotg_corporation_role_top = yes }` (`common/decisions/eotg_corporation_decisions.txt:152-158`), so a count under a duke under the CEO erodes the duke's influence, not the CEO's. The model treats every director as a direct vassal, so the 16-director rows overstate a nested realm; read the **4–8 director rows** as the realistic case (CEO at 0 in 8.0% of years with 4 directors under full pressure, 32.2% with 8).
- **Where:** `common/script_values/eotg_corporation_values.txt:73` (`eotg_corporation_court_erosion_value = -5`), read by `common/decisions/eotg_corporation_decisions.txt:113`.
- **Proposal P1:** `eotg_corporation_court_erosion_value = -2`.

  | Scenario | Metric | Before | After |
  |---|---|---|---|
  | 16 directors, `greedy_all` | runs stuck at 0 for 20+ years | 52.2% | 0.0% |
  | 16 directors, `greedy_all` | equilibrium | 0 | 9.6 |
  | 16 directors, AI | equilibrium | 32.5 | 37.5 |
  | 16 directors, player CEO | equilibrium | 47.5 | 55.4 |

**H2. PMC: Standing scales with vassal count.**
- **Evidence.**
  - AI top equilibrium is 29.5 / 37.7 / 46.2 / 59.8 for 1 / 4 / 8 / 16 vassals.
  - A player top with 16 vassals reaches 96.0 and sits at 100 in 23.7% of years.
  - With every vassal greedy (16): 77.8% of years at 100.

  Each vassal's Deliver Results gives the liege +5 with no per-liege cap. Vassals now deliver only in their own peace years (H2a fix), which makes the scaling slightly stronger than the first run showed.
- **Where:** `common/script_values/eotg_pmc_values.txt:78` (`eotg_pmc_deliver_liege_value = 5`), used at `common/decisions/eotg_pmc_decisions.txt:102`.
- **Proposal P2:** `eotg_pmc_deliver_liege_value = 2`. **Variant P2-cap (structural, owner call):** the liege gains from at most one Deliver Results a year.

  | Scenario | Metric | Before | P2 (+2) | P2-cap |
  |---|---|---|---|---|
  | 16 vassals, AI | equilibrium | 59.8 | 42.8 | 56.2 |
  | 1 vassal, AI | equilibrium | 29.5 | 27.7 | 29.5 |
  | 16 vassals, `greedy_all` | years at 100 | 77.8% | 59.7% | 57.0% |

  A liege value of 1 brings 16 AI vassals down to 35.8 (`--checks`, 2,000 runs). The cap is scale-free but mild against AI vassals, who deliver rarely (L1); the value change is strong but also trims the one-vassal case.

### MED

**M1. Trade Oligarchy: the First Prince, not the vassals, is the one the passive feed starves; vassal Princes out-share their First Prince.**
- **Correction (H2a).** The first run gave vassal Princes their liege's war state. The script ticks on each owner's own `is_at_war`, and a vassal is not at war because its liege is (the repo's ruling, `common/scripted_triggers/eotg_frontier_triggers.txt:383-386`). With vassals carrying their own wars (about 3% of years), the finding flips.
- **Evidence.**
  - Vassal Princes: median share 55–57 (AI, all sizes), not 7–10.
  - The First Prince: 23–28. Its feed (+1 peace, −4 war) is net negative above a **20% war share** (the knife-edge; `--checks` sweep): 54.6 at 10% war, 31.3 at 20%, 10.0 at 30%. The model's top is at war about 23% of years.
  - The market-share vote is live: without the dynasty rule a non-dynast would win 32–37% of elections with 4+ Princes (9.6% with 1).
- **Open question flipped:** vassal Princes out-share the First Prince by about 30 points. Whether that is the intended "first among equals" or a problem is an owner call.
- **Where:** `common/script_values/eotg_gobcorp_values.txt:63` (`eotg_gobcorp_war_loss_value = -4`), read by the yearly tick in `common/story_cycles/eotg_gobcorp_story.txt`.
- **Proposal P3:** `eotg_gobcorp_war_loss_value = -3` (feed turns negative above 25% war instead of 20%). **Hold** (recommendation table).

  | Scenario | Metric | Before | After |
  |---|---|---|---|
  | 4 Princes, AI | First Prince equilibrium | 23.3 | 33.8 |
  | 4 Princes, AI | vassal median | 57.4 | 59.7 |
  | 16 Princes, AI | First Prince equilibrium | 27.0 | 37.0 |
  | 16 Princes, AI | vassal median | 56.5 | 59.0 |

  Peace +2 instead would put vassals at 89–90 and the First Prince at 59–60 (`--checks`), too strong.

**M2. Cartel: payers walk off after a succession, because the 3-year grace ends before the heir's dread recovers.**
- **Correction (H2a).** The first run measured walk-offs within 5 years; with a 5-year grace that window is empty by construction, so P5 read 0.000. The metric is now walk-offs within **10 years** of a succession.
- **Evidence.**
  - The heir starts with no dread (ASSUMPTION: dread is personal) and climbs toward the payer baseline at 0.375 a month (decay −0.25, read from the government).
  - With 1–3 payers the baseline (4 per payer) sits under `low_dread` 20, so the walk-off starts the year the grace ends.
  - Walk-offs within 10 years of a succession: 0.516 per succession (1 vassal, AI), 0.436 (4), 0.318 (8), 0.146 (16).
- **Where:** `common/on_action/eotg_cartel_on_actions.txt:111` (`years = 3` on `eotg_cartel_succession_grace`).
- **Proposal P5:** `years = 5`, with the story `_info` loc line updated (the patch includes it). **Take now.**

  | Scenario | Metric | Before | After |
  |---|---|---|---|
  | 4 vassals, AI | walk-offs within 10 years of a succession | 0.436 | 0.218 |
  | 4 vassals, AI | mean payers | 1.82 | 1.93 |
  | 16 vassals, AI | walk-offs within 10 years of a succession | 0.146 | 0.043 |

  Dread equilibria are unchanged (59.0, 70.0).

**M3. Cybernetics: the development gate, not the decision, decides who reaches Overclocked.**
- **Correction (H2a).** Initiation itself needs capital development ≥ 10 (`common/scripted_triggers/eotg_augmentation_triggers.txt:87-88`), so every installed ruler comes from the ≥ 10 part of the distribution. The first run sampled all capitals.
- **Evidence.**
  - The Overclocked gate (development 20) is met by about 34% of installed rulers' capitals (vanilla history distribution, balance spec §5.1, conditioned on ≥ 10), growing about +1 a decade.
  - A player who always pushes reaches Overclocked in 34.0% of installs, and within 20 years in 26.1% (duke). The balance spec's target for a pushing player was a median of 12 years and 100% within 20.
  - AI: 5.5% ever, median 46 years.
- **Where:** `common/script_values/eotg_augmentation_values.txt:25` (`eotg_aug_dev_gate_overclocked`, value 20).
- **Proposal P4:** `value = 15`. **Hold:** retune on the real map.

  | Scenario | Metric | Before | After |
  |---|---|---|---|
  | Player who always pushes | reach Overclocked | 34.0% | 50.7% |
  | Player who always pushes | within 20 years | 26.1% | 41.8% |
  | Player who always pushes | cascade deaths | 9.4% | 14.5% |
  | AI | reach Overclocked | 5.5% | 7.5% |

  The space map's development distribution decides this, and the balance spec already flags these gates as provisional.

**M4. PMC: Take a Contract pays a flat 50 + 3 × Standing gold at every tier. (Static finding; P6 not simulated.)**
- **Evidence (static, the script's formula).** At Standing 50 the pay is 200 gold every 3 years at every tier, while the costs around it (minor and medium gold) scale with the realm.
- **Where:** `common/script_values/eotg_pmc_values.txt` (`eotg_pmc_contract_pay_value`).
- **Proposal P6:** `(Standing / 50 + 0.5) × medium_gold_value`, 0.5–2.5× medium gold. **Not simulated, hold.** The sim's gold proxy runs about 2× vanilla's medium gold, and vanilla's `medium_gold_value` has a floor of 50 (`00_basic_values.txt:82`, local audit), so at the floor a count and a duke both get 75 at Standing 50. The first run's P6 table (90 / 150 / 270) used the inflated proxy and is withdrawn. The patch keeps P6 with its loc for the owner to judge against vanilla numbers in game.

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
  - Baseline: completion 99–100%; falters 0.0–0.4% per project (administrative about 4%).
  - Durations are in the owner's bands (Appendix A).
  - In a hostile world (`--hostile`: war reaching the Shoal 25%/yr, Dangerous 40%, occupied 6%/yr, AI holder), abandonment rises to 1.2% (Settlement), 4.3% (Research) and 9.2% (Administrative). The first run's 10% / 25–26% came from an unrecorded setting and did not reproduce; these figures replace them.
- **Strain works as a world-dependent risk. No change proposed.**

**L3. Cybernetics: Overclocked is short.** The median from Overclocked to the cascade is about 4 years (base accrual 12 plus stress), and about 88% of Overclocked rulers cascade. Seamless is 11% of installs for a player who pushes, 1.1% for the AI. This is consistent with "Overclocked is a countdown"; it is recorded for the owner, with no change proposed.

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

## Void Corruption (added 2026-11-03, H2b)

**Model:** `docs/tools/sim/models/void.py`. It reads the merged Void script through `pdx_read.py`:
- the accrual block (`eotg_void_values.txt:11-43`), the Voidwalker −6 (`:35`), the Hollowing start and drift (`:46-53`), and the contact chance with its `is_ai` branch (`:60-66`);
- the stage triggers as written;
- the band thresholds inside the two refresh effects;
- every event slot of `eotg_on_yearly_void_check` (`eotg_void_on_actions.txt:33-190`): chance or weight, sibling total and the cooldown it sets;
- every option of the 15 events: AI weight, exposure and depth amounts, wards and stage effects, with the `eotg_void_*` scripted effects walked inline.

It follows the on_action's order: accrual, the forced Hollowing, one roll by stage, then the Voidwalker only if nothing fired. **ASSUMPTIONS:**
- option availability 0.35 for any gated option;
- AI weights for players too, so player and AI differ only in contact rate;
- a lone realm with no Touched neighbours;
- no Grip Survivors (R2: nobody bears the trait yet).

Seats run 50 years (sweep) or 100 years (timings), 10,000 each. Full tables are in Appendix A; the chart is `chart_void.png`.

### HIGH

**VH1. The Touched stage is a four-year sprint hidden behind the cooldown, so its six events are almost never seen.**
- **Evidence.**
  - A Touched ruler accrues +8 a year (base 2, Touched 6) from 50–75 to 100, so Touched lasts a median of **4 years** (quartiles 2–5), and **85%** of Touched rulers are Hollowed.
  - The Bargain (0010) or Taken Anyway (0011) that made them Touched set a 5-year cooldown (`eotg_void_on_actions.txt:125-139`). The Hollowing fires regardless of the cooldown (`:46-50`), so the stage-C roll (`:79-121`) rarely gets a turn.
  - All six stage-C events together fire **0.038 per 100 seat-years** (player, 4% contact), against 0.203 player Hollowings, so stage-C events are about 7× rarer than Hollowings (0.067 is the AI 1% / 50-year rate). A player meets any one of the six stage-C events about once in 2,600 seat-years. **Local audit 2026-11-03:** the binding constraint is the shared 5-year cooldown set by 0010/0011 (`eotg_void_on_actions.txt:127,137`); cutting that cooldown to 2 years alone takes stage C from 0.037 to 0.245 per seat-century without lengthening Touched (a more direct lever than V1, which gives 0.227 and stretches Touched to about 6 years). V2 is about rarity (0.46–0.50 Voidwalkers per 100 seat-years, about 29% seated), not lateness.
- **Where:** `common/script_values/eotg_void_values.txt:16` (`has_trait = eotg_void_touched`, `add = 6`).
- **Proposal V1:** `add = 2`.

  | Metric (player seat, 4% contact, 100 years) | Before | After |
  |---|---|---|
  | Stage-C events per 100 seat-years | 0.038 | 0.211 |
  | Touched duration, median years | 4 | 6 |
  | Seats ever Hollowed | 26.4% | 22.8% |
  | Seats ever Touched | 30.9% | 30.9% |

  A term of 0 would give 0.36 and 7 years (2,000-run check, the same model). +2 keeps the Hollowing a real threat.

### MED

**VM1. The Voidwalker arrives too late to matter.**
- **Evidence.**
  - 0004 rolls 12% a year (`eotg_void_on_actions.txt:175-189`). It needs exposure ≥ 20 and a free cooldown, and option a (seat them) is one of four.
  - Share of contacted rulers who become Touched: 34.7% with no Voidwalker, **31.4% as scripted**, 0.3% with a Voidwalker seated at contact.
  - The model reads the −6 (`eotg_void_values.txt:35`): a seated Voidwalker turns an untouched ruler's accrual negative, so it is near-total protection, but it rarely arrives in time.
  - Voidwalkers created: 0.50 per 100 seat-years. About two in three of these are not seated: they wander (option b or c) or are killed (option d).
- **Where:** `common/on_action/eotg_void_on_actions.txt:184` (`chance = 12`).
- **Proposal V2:** `chance = 25`. **Owner call:** it makes Voidwalkers about twice as common in the world.

  | Metric (player seat, 4% contact, 100 years) | Before | After |
  |---|---|---|
  | Voidwalkers created per 100 seat-years | 0.50 | 0.94 |
  | Touched, given contact | 31.4% | 29.3% |
  | Seats ever Hollowed | 26.4% | 24.3% |

  The stronger lever would be the exposure gate (`>= 20` at `:180`). It is not proposed, because it changes when the visit fits the story.

### LOW

**VL1. Owner question Q5, the contact rate: keep 4% player / 1% AI.**
- **Evidence (50-year seats):**

  | Contact rate | Contacted | Ever Touched | Ever Hollowed |
  |---|---|---|---|
  | 0.5% | 22.9% | 2.5% | 2.0% |
  | 1% (AI default) | 40.3% | 4.6% | 3.3% |
  | 2% | 64.3% | 8.2% | 6.3% |
  | 4% (player default) | 86.6% | 13.4% | 10.2% |

  The shares scale almost linearly. Under the 4/1 default, about one AI ruler in 20 is ever Touched within 50 years, so the Void stays rare in the world while a player meets it.
  - **Stage timings (player):** contact to Touched takes a median of 28–29 years (quartiles 19–55). Touched to Hollowed takes 4 years, or 6 with a Voidwalker seated at contact (it is rare to be Touched at all then).
- **Proposed value change: none** (keep `eotg_void_contact_chance_value` at 4 / 1).

**VL2. The Voidwalker's accrual term is not a lever.**
- **Evidence.** Changing −6 to −4 (V3, simulated) moves nothing measurable: Touched 30.9% → 31.8% of seats, inside the noise, because few Voidwalkers are seated.
- **Proposed value change: none.**

**VL3. The exploit scan is clean for the Void** (`exploit_scan.md`, Void section).
- The Warding Rite (−20, piety 200) and the Voidwalker Ward (−35, gold 100 and piety 150) share one flag cooldown. It is set inside the scripted effects, which the scan now walks inline: 10 and 8 years. So relief runs at most −2 to −4.4 a year, plus the ward modifier's −5 a year accrual while it holds.
- Commune adds exposure (+20) in trade for an Insight, on a 10-year `cooldown`. It is inert while `eotg_void_is_cult_faith` is `always = no`.
- No Void decision has F1 or F4.

---

## How to verify a proposal in game
- **P1/P2:** play 20 years with 8+ vassals of the government, then read the top's resource in the story counter.
- **P3:** the vassal Princes' median share after 30 years of mixed war and peace.
- **P4:** the observer run's Overclocked population (balance spec §9.2).
- **P5:** `kill` a Cartel ruler with 2 payers, then count walk-offs over the next 5 years.
- **V1/V2:** the harness VD tests set up the states; then play a Touched ruler 10 years and count stage-C events.
- **P2-cap:** with 8 PMC vassals, count Deliver Results in one year and the liege's standing gain.
- **P6:** Take a Contract as a county PMC and as a kingdom PMC, and read the pay against vanilla's medium gold.

---

## Appendix A: run tables

Generated by `docs/tools/sim/report_tables.py` from `results.json` (run with `--checks --hostile`).

### Government resources (top ruler), 100 years, 10000 runs per cell

| System | Vassals | Policy | Equilibrium | Settles by year | At 0 | At 100 | 20y stuck at 0 | 20y stuck at 100 | Vassal median | Key counts |
|---|---|---|---|---|---|---|---|---|---|---|
| cartel | 1 | ai | 57.8 | 18 | 7.4% | 0.2% | 0.0% | 0.0% | None | accept_per_run_year 0.076, refusal_per_run_year 0.025, walkoff_per_run_year 0.011, tighten_per_run_year 0.021, lean_per_vassal_year 0.045 |
| cartel | 1 | greedy | 34.5 | 16 | 6.9% | 0.1% | 0.0% | 0.0% | None | accept_per_run_year 0.135, refusal_per_run_year 0.267, walkoff_per_run_year 0.035, tighten_per_run_year 0.000, lean_per_vassal_year 0.045 |
| cartel | 1 | greedy_all | 41.8 | 54 | 4.9% | 0.3% | 0.0% | 0.0% | None | accept_per_run_year 0.150, refusal_per_run_year 0.272, walkoff_per_run_year 0.027, tighten_per_run_year 0.000, lean_per_vassal_year 0.169 |
| cartel | 4 | ai | 59.0 | 14 | 5.9% | 0.9% | 0.0% | 0.0% | None | accept_per_run_year 0.098, refusal_per_run_year 0.033, walkoff_per_run_year 0.011, tighten_per_run_year 0.025, lean_per_vassal_year 0.045 |
| cartel | 4 | greedy | 42.2 | 42 | 5.4% | 0.4% | 0.0% | 0.0% | None | accept_per_run_year 0.151, refusal_per_run_year 0.268, walkoff_per_run_year 0.027, tighten_per_run_year 0.000, lean_per_vassal_year 0.045 |
| cartel | 4 | greedy_all | 67.0 | 97 | 3.7% | 4.5% | 0.0% | 0.0% | None | accept_per_run_year 0.191, refusal_per_run_year 0.212, walkoff_per_run_year 0.007, tighten_per_run_year 0.000, lean_per_vassal_year 0.169 |
| cartel | 8 | ai | 63.0 | 12 | 4.8% | 2.4% | 0.0% | 0.0% | None | accept_per_run_year 0.121, refusal_per_run_year 0.029, walkoff_per_run_year 0.009, tighten_per_run_year 0.029, lean_per_vassal_year 0.047 |
| cartel | 8 | greedy | 54.8 | 58 | 4.5% | 2.0% | 0.0% | 0.0% | None | accept_per_run_year 0.177, refusal_per_run_year 0.216, walkoff_per_run_year 0.018, tighten_per_run_year 0.000, lean_per_vassal_year 0.047 |
| cartel | 8 | greedy_all | 80.5 | 98 | 3.5% | 13.6% | 0.0% | 0.0% | None | accept_per_run_year 0.216, refusal_per_run_year 0.111, walkoff_per_run_year 0.003, tighten_per_run_year 0.000, lean_per_vassal_year 0.169 |
| cartel | 16 | ai | 70.0 | 10 | 4.0% | 7.1% | 0.0% | 0.0% | None | accept_per_run_year 0.157, refusal_per_run_year 0.025, walkoff_per_run_year 0.004, tighten_per_run_year 0.035, lean_per_vassal_year 0.047 |
| cartel | 16 | greedy | 70.8 | 42 | 3.8% | 8.2% | 0.0% | 0.0% | None | accept_per_run_year 0.197, refusal_per_run_year 0.169, walkoff_per_run_year 0.005, tighten_per_run_year 0.000, lean_per_vassal_year 0.047 |
| cartel | 16 | greedy_all | 95.5 | 96 | 3.5% | 25.7% | 0.0% | 0.1% | None | accept_per_run_year 0.225, refusal_per_run_year 0.058, walkoff_per_run_year 0.001, tighten_per_run_year 0.000, lean_per_vassal_year 0.169 |
| pmc | 1 | ai | 29.5 | 19 | 0.7% | 0.0% | 0.3% | 0.0% | 34.5 | take_contract_per_run_year 0.065, recruit_per_run_year 0.017, deliver_per_vassal_year 0.028, stand_down_share 0.017 |
| pmc | 1 | greedy | 68.6 | 13 | 0.0% | 0.2% | 0.0% | 0.0% | 34.2 | take_contract_per_run_year 0.233, recruit_per_run_year 0.000, deliver_per_vassal_year 0.028, stand_down_share 0.000 |
| pmc | 1 | greedy_all | 80.3 | 35 | 0.0% | 3.3% | 0.0% | 0.0% | 69.1 | take_contract_per_run_year 0.233, recruit_per_run_year 0.000, deliver_per_vassal_year 0.146, stand_down_share 0.000 |
| pmc | 4 | ai | 37.7 | 6 | 0.1% | 0.0% | 0.0% | 0.0% | 34.3 | take_contract_per_run_year 0.068, recruit_per_run_year 0.028, deliver_per_vassal_year 0.029, stand_down_share 0.004 |
| pmc | 4 | greedy | 75.6 | 20 | 0.0% | 2.3% | 0.0% | 0.0% | 34.3 | take_contract_per_run_year 0.234, recruit_per_run_year 0.000, deliver_per_vassal_year 0.028, stand_down_share 0.000 |
| pmc | 4 | greedy_all | 98.0 | 12 | 0.0% | 30.5% | 0.0% | 0.0% | 68.3 | take_contract_per_run_year 0.233, recruit_per_run_year 0.000, deliver_per_vassal_year 0.146, stand_down_share 0.000 |
| pmc | 8 | ai | 46.2 | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 35.2 | take_contract_per_run_year 0.069, recruit_per_run_year 0.039, deliver_per_vassal_year 0.030, stand_down_share 0.001 |
| pmc | 8 | greedy | 86.2 | 22 | 0.0% | 8.6% | 0.0% | 0.0% | 35.2 | take_contract_per_run_year 0.233, recruit_per_run_year 0.000, deliver_per_vassal_year 0.030, stand_down_share 0.000 |
| pmc | 8 | greedy_all | 100.0 | 6 | 0.0% | 55.7% | 0.0% | 1.8% | 68.6 | take_contract_per_run_year 0.233, recruit_per_run_year 0.000, deliver_per_vassal_year 0.147, stand_down_share 0.000 |
| pmc | 16 | ai | 59.8 | 28 | 0.0% | 1.0% | 0.0% | 0.0% | 35.3 | take_contract_per_run_year 0.076, recruit_per_run_year 0.054, deliver_per_vassal_year 0.030, stand_down_share 0.000 |
| pmc | 16 | greedy | 96.0 | 12 | 0.0% | 23.7% | 0.0% | 0.0% | 35.2 | take_contract_per_run_year 0.234, recruit_per_run_year 0.000, deliver_per_vassal_year 0.030, stand_down_share 0.000 |
| pmc | 16 | greedy_all | 100.0 | 4 | 0.0% | 77.8% | 0.0% | 56.8% | 68.6 | take_contract_per_run_year 0.233, recruit_per_run_year 0.000, deliver_per_vassal_year 0.147, stand_down_share 0.000 |
| corporation | 1 | ai | 39.6 | 11 | 0.3% | 0.5% | 0.0% | 0.1% | 65.0 | court_per_vassal_year 0.007, erosion_per_run_year 0.005, restructure_per_run_year 0.031 |
| corporation | 1 | greedy | 59.7 | 1 | 0.2% | 11.3% | 0.0% | 13.8% | 64.5 | court_per_vassal_year 0.007, erosion_per_run_year 0.004, restructure_per_run_year 0.000 |
| corporation | 1 | greedy_all | 45.0 | 37 | 0.6% | 7.0% | 0.0% | 8.4% | 98.0 | court_per_vassal_year 0.105, erosion_per_run_year 0.082, restructure_per_run_year 0.000 |
| corporation | 4 | ai | 38.5 | 10 | 0.5% | 0.5% | 0.0% | 0.1% | 64.7 | court_per_vassal_year 0.007, erosion_per_run_year 0.022, restructure_per_run_year 0.029 |
| corporation | 4 | greedy | 58.0 | 0 | 0.2% | 10.6% | 0.0% | 12.6% | 64.6 | court_per_vassal_year 0.007, erosion_per_run_year 0.015, restructure_per_run_year 0.000 |
| corporation | 4 | greedy_all | 9.0 | 57 | 8.0% | 1.9% | 0.0% | 2.5% | 85.8 | court_per_vassal_year 0.105, erosion_per_run_year 0.300, restructure_per_run_year 0.000 |
| corporation | 8 | ai | 36.6 | 12 | 0.7% | 0.4% | 0.0% | 0.1% | 65.0 | court_per_vassal_year 0.008, erosion_per_run_year 0.048, restructure_per_run_year 0.026 |
| corporation | 8 | greedy | 54.2 | 0 | 0.3% | 10.1% | 0.0% | 12.5% | 65.1 | court_per_vassal_year 0.008, erosion_per_run_year 0.033, restructure_per_run_year 0.000 |
| corporation | 8 | greedy_all | 0.5 | 36 | 32.2% | 0.3% | 1.8% | 0.4% | 85.7 | court_per_vassal_year 0.112, erosion_per_run_year 0.541, restructure_per_run_year 0.000 |
| corporation | 16 | ai | 32.5 | 14 | 1.2% | 0.3% | 0.0% | 0.1% | 64.8 | court_per_vassal_year 0.008, erosion_per_run_year 0.096, restructure_per_run_year 0.021 |
| corporation | 16 | greedy | 47.5 | 14 | 0.7% | 8.4% | 0.0% | 10.2% | 64.8 | court_per_vassal_year 0.008, erosion_per_run_year 0.070, restructure_per_run_year 0.000 |
| corporation | 16 | greedy_all | 0.0 | 25 | 58.4% | 0.1% | 52.2% | 0.2% | 85.3 | court_per_vassal_year 0.112, erosion_per_run_year 0.752, restructure_per_run_year 0.000 |
| gobcorp | 1 | ai | 28.1 | 34 | 2.0% | 0.1% | 0.0% | 0.0% | 55.2 | corner_per_run_year 0.019, undercut_per_vassal_year 0.000 |
| gobcorp | 1 | greedy | 49.9 | 44 | 0.6% | 1.6% | 0.0% | 0.4% | 47.0 | corner_per_run_year 0.045, undercut_per_vassal_year 0.000 |
| gobcorp | 1 | greedy_all | 49.9 | 44 | 0.6% | 1.6% | 0.0% | 0.4% | 47.0 | corner_per_run_year 0.045, undercut_per_vassal_year 0.000 |
| gobcorp | 4 | ai | 23.3 | 47 | 2.4% | 0.0% | 0.0% | 0.0% | 57.4 | corner_per_run_year 0.013, undercut_per_vassal_year 0.016 |
| gobcorp | 4 | greedy | 49.5 | 39 | 0.7% | 1.5% | 0.0% | 0.5% | 47.6 | corner_per_run_year 0.045, undercut_per_vassal_year 0.016 |
| gobcorp | 4 | greedy_all | 49.7 | 39 | 0.6% | 1.6% | 0.0% | 0.5% | 47.8 | corner_per_run_year 0.045, undercut_per_vassal_year 0.148 |
| gobcorp | 8 | ai | 27.1 | 38 | 2.1% | 0.0% | 0.0% | 0.0% | 56.4 | corner_per_run_year 0.017, undercut_per_vassal_year 0.017 |
| gobcorp | 8 | greedy | 71.4 | 61 | 0.2% | 6.3% | 0.0% | 1.9% | 39.9 | corner_per_run_year 0.072, undercut_per_vassal_year 0.017 |
| gobcorp | 8 | greedy_all | 72.0 | 61 | 0.2% | 6.4% | 0.0% | 1.9% | 39.9 | corner_per_run_year 0.072, undercut_per_vassal_year 0.149 |
| gobcorp | 16 | ai | 27.0 | 39 | 2.0% | 0.0% | 0.0% | 0.0% | 56.5 | corner_per_run_year 0.017, undercut_per_vassal_year 0.017 |
| gobcorp | 16 | greedy | 72.0 | 62 | 0.2% | 6.4% | 0.0% | 1.9% | 39.8 | corner_per_run_year 0.072, undercut_per_vassal_year 0.017 |
| gobcorp | 16 | greedy_all | 72.0 | 64 | 0.2% | 6.3% | 0.0% | 2.0% | 40.1 | corner_per_run_year 0.072, undercut_per_vassal_year 0.149 |

### Elections (at each top-ruler death)

| System | Vassals | Policy | Elections | Resource leader's pick wins | Non-dynast would win without the dynasty rule |
|---|---|---|---|---|---|
| corporation | 1 | ai | 35084 | 74.2% | 7.4% |
| corporation | 1 | greedy | 35101 | 81.3% | 3.7% |
| corporation | 1 | greedy_all | 35026 | 74.2% | 12.3% |
| corporation | 4 | ai | 35198 | 64.2% | 23.2% |
| corporation | 4 | greedy | 35032 | 68.6% | 12.4% |
| corporation | 4 | greedy_all | 35260 | 62.5% | 55.0% |
| corporation | 8 | ai | 35156 | 59.7% | 16.2% |
| corporation | 8 | greedy | 34620 | 63.7% | 9.1% |
| corporation | 8 | greedy_all | 35174 | 58.9% | 50.1% |
| corporation | 16 | ai | 35041 | 59.9% | 30.8% |
| corporation | 16 | greedy | 35027 | 62.8% | 19.1% |
| corporation | 16 | greedy_all | 34845 | 58.7% | 71.3% |
| gobcorp | 1 | ai | 35380 | 80.4% | 9.6% |
| gobcorp | 1 | greedy | 34894 | 87.2% | 2.7% |
| gobcorp | 1 | greedy_all | 34894 | 87.2% | 2.7% |
| gobcorp | 4 | ai | 34887 | 68.4% | 32.3% |
| gobcorp | 4 | greedy | 35137 | 74.1% | 10.6% |
| gobcorp | 4 | greedy_all | 35009 | 72.8% | 10.2% |
| gobcorp | 8 | ai | 35275 | 62.1% | 36.3% |
| gobcorp | 8 | greedy | 35041 | 75.6% | 4.3% |
| gobcorp | 8 | greedy_all | 34765 | 75.0% | 3.5% |
| gobcorp | 16 | ai | 35094 | 61.6% | 37.2% |
| gobcorp | 16 | greedy | 35039 | 75.5% | 4.5% |
| gobcorp | 16 | greedy_all | 34840 | 75.3% | 3.9% |

### Cartel payers and succession

| Vassals | Policy | Payers (last 20 y, mean) | Walk-offs within 5 y of a succession | within 10 y |
|---|---|---|---|---|
| 1 | ai | 1.36 | 0.416 | 0.516 |
| 1 | greedy | 2.96 | 0.381 | 0.606 |
| 1 | greedy_all | 3.64 | 0.291 | 0.468 |
| 4 | ai | 1.82 | 0.346 | 0.436 |
| 4 | greedy | 3.70 | 0.285 | 0.457 |
| 4 | greedy_all | 5.21 | 0.082 | 0.124 |
| 8 | ai | 2.33 | 0.253 | 0.318 |
| 8 | greedy | 4.67 | 0.173 | 0.289 |
| 8 | greedy_all | 5.60 | 0.039 | 0.047 |
| 16 | ai | 3.00 | 0.125 | 0.146 |
| 16 | greedy | 5.34 | 0.058 | 0.092 |
| 16 | greedy_all | 5.72 | 0.027 | 0.027 |

### Cybernetics (one ruler from installation; tier by realm size)

| Vassals | Policy | Reach Enhanced | Reach Overclocked | OC within 20 y | Cascade (NF) | Seamless | Cascade death | Natural death | Median years to OC | to NF |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ai | 25.0% | 5.4% | 0.4% | 4.7% | 1.2% | 1.6% | 96.2% | 47.0 | 50.0 |
| 1 | greedy | 65.4% | 34.0% | 25.9% | 30.1% | 11.0% | 9.4% | 89.0% | 14.0 | 18.0 |
| 1 | greedy_all | 65.4% | 34.0% | 25.9% | 30.1% | 11.0% | 9.4% | 89.0% | 14.0 | 18.0 |
| 4 | ai | 25.2% | 5.5% | 0.4% | 4.8% | 1.1% | 1.8% | 95.8% | 46.0 | 48.0 |
| 4 | greedy | 64.5% | 34.0% | 26.1% | 30.4% | 11.0% | 9.4% | 88.6% | 14.0 | 18.0 |
| 4 | greedy_all | 64.5% | 34.0% | 26.1% | 30.4% | 11.0% | 9.4% | 88.6% | 14.0 | 18.0 |
| 8 | ai | 25.5% | 5.6% | 0.4% | 4.9% | 1.1% | 1.8% | 95.8% | 48.0 | 51.0 |
| 8 | greedy | 64.0% | 33.8% | 26.1% | 30.1% | 10.7% | 9.4% | 89.0% | 14.0 | 17.0 |
| 8 | greedy_all | 64.0% | 33.8% | 26.1% | 30.1% | 10.7% | 9.4% | 89.0% | 14.0 | 17.0 |
| 16 | ai | 25.0% | 5.3% | 0.4% | 4.5% | 1.2% | 1.7% | 95.9% | 47.0 | 50.0 |
| 16 | greedy | 65.1% | 33.8% | 25.8% | 29.8% | 11.0% | 9.2% | 89.1% | 14.0 | 17.0 |
| 16 | greedy_all | 65.1% | 33.8% | 25.8% | 29.8% | 11.0% | 9.2% | 89.1% | 14.0 | 17.0 |

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
| 16 | greedy_all | equilibrium | 0.000 | 9.625 |
| 16 | greedy_all | dead_lo_20y | 0.522 | 0.000 |
| 16 | greedy_all | at_hi | 0.001 | 0.013 |
| 16 | greedy_all | at_lo | 0.584 | 0.057 |
| 16 | greedy_all | vassal_eq | 85.272 | 85.272 |
| 16 | ai | equilibrium | 32.500 | 37.500 |
| 16 | ai | dead_lo_20y | 0.000 | 0.000 |
| 16 | ai | at_hi | 0.003 | 0.004 |
| 16 | ai | at_lo | 0.012 | 0.005 |
| 16 | ai | vassal_eq | 64.824 | 64.824 |
| 16 | greedy | equilibrium | 47.500 | 55.375 |
| 16 | greedy | dead_lo_20y | 0.000 | 0.000 |
| 16 | greedy | at_hi | 0.084 | 0.103 |
| 16 | greedy | at_lo | 0.007 | 0.002 |
| 16 | greedy | vassal_eq | 64.822 | 64.822 |

**P2** `pmc` override {'eotg_pmc_deliver_liege_value': 2}:

| Vassals | Policy | Metric | Before | After |
|---|---|---|---|---|
| 16 | ai | equilibrium | 59.751 | 42.839 |
| 16 | ai | dead_lo_20y | 0.000 | 0.000 |
| 16 | ai | at_hi | 0.010 | 0.000 |
| 16 | ai | at_lo | 0.000 | 0.000 |
| 16 | ai | vassal_eq | 35.253 | 35.253 |
| 1 | ai | equilibrium | 29.547 | 27.703 |
| 1 | ai | dead_lo_20y | 0.003 | 0.004 |
| 1 | ai | at_hi | 0.000 | 0.000 |
| 1 | ai | at_lo | 0.007 | 0.010 |
| 1 | ai | vassal_eq | 34.453 | 34.453 |
| 16 | greedy_all | equilibrium | 100.000 | 100.000 |
| 16 | greedy_all | dead_lo_20y | 0.000 | 0.000 |
| 16 | greedy_all | at_hi | 0.778 | 0.597 |
| 16 | greedy_all | at_lo | 0.000 | 0.000 |
| 16 | greedy_all | vassal_eq | 68.575 | 68.575 |

**P2-cap** `pmc` override {'pmc_deliver_liege_once_a_year': True}:

| Vassals | Policy | Metric | Before | After |
|---|---|---|---|---|
| 16 | ai | equilibrium | 59.751 | 56.223 |
| 16 | ai | dead_lo_20y | 0.000 | 0.000 |
| 16 | ai | at_hi | 0.010 | 0.002 |
| 16 | ai | at_lo | 0.000 | 0.000 |
| 16 | ai | vassal_eq | 35.253 | 35.253 |
| 1 | ai | equilibrium | 29.547 | 29.547 |
| 1 | ai | dead_lo_20y | 0.003 | 0.003 |
| 1 | ai | at_hi | 0.000 | 0.000 |
| 1 | ai | at_lo | 0.007 | 0.007 |
| 1 | ai | vassal_eq | 34.453 | 34.453 |
| 16 | greedy_all | equilibrium | 100.000 | 100.000 |
| 16 | greedy_all | dead_lo_20y | 0.000 | 0.000 |
| 16 | greedy_all | at_hi | 0.778 | 0.570 |
| 16 | greedy_all | at_lo | 0.000 | 0.000 |
| 16 | greedy_all | vassal_eq | 68.575 | 68.575 |

**P3** `gobcorp` override {'eotg_gobcorp_war_loss_value': -3}:

| Vassals | Policy | Metric | Before | After |
|---|---|---|---|---|
| 4 | ai | equilibrium | 23.306 | 33.758 |
| 4 | ai | dead_lo_20y | 0.000 | 0.000 |
| 4 | ai | at_hi | 0.000 | 0.000 |
| 4 | ai | at_lo | 0.024 | 0.007 |
| 4 | ai | vassal_eq | 57.379 | 59.686 |
| 16 | ai | equilibrium | 26.954 | 37.000 |
| 16 | ai | dead_lo_20y | 0.000 | 0.000 |
| 16 | ai | at_hi | 0.000 | 0.000 |
| 16 | ai | at_lo | 0.020 | 0.005 |
| 16 | ai | vassal_eq | 56.521 | 59.040 |

**P4** `cybernetics` override {'eotg_aug_dev_gate_overclocked': 15}:

| Vassals | Policy | Metric | Before | After |
|---|---|---|---|---|
| 4 | ai | reach_3 | 0.055 | 0.075 |
| 4 | ai | oc_within_20y | 0.004 | 0.007 |
| 4 | ai | cascade_death | 0.018 | 0.024 |
| 4 | greedy | reach_3 | 0.340 | 0.507 |
| 4 | greedy | oc_within_20y | 0.261 | 0.418 |
| 4 | greedy | cascade_death | 0.094 | 0.145 |

**P5** `cartel` override {'eotg_cartel_on_death.years': 5}:

| Vassals | Policy | Metric | Before | After |
|---|---|---|---|---|
| 4 | ai | equilibrium | 59.000 | 59.000 |
| 4 | ai | dead_lo_20y | 0.000 | 0.000 |
| 4 | ai | at_hi | 0.009 | 0.009 |
| 4 | ai | at_lo | 0.059 | 0.057 |
| 4 | ai | post_succession_walkoffs | 0.346 | 0.000 |
| 4 | ai | post_succession_walkoffs_10y | 0.436 | 0.218 |
| 4 | ai | payers_eq | 1.821 | 1.931 |
| 16 | ai | equilibrium | 70.000 | 70.000 |
| 16 | ai | dead_lo_20y | 0.000 | 0.000 |
| 16 | ai | at_hi | 0.071 | 0.071 |
| 16 | ai | at_lo | 0.040 | 0.039 |
| 16 | ai | post_succession_walkoffs | 0.125 | 0.000 |
| 16 | ai | post_succession_walkoffs_10y | 0.146 | 0.043 |
| 16 | ai | payers_eq | 3.002 | 3.060 |


### Side checks (`--checks`, 2,000 runs each)

| Check | Override | Vassals | Policy | Equilibrium | Vassal median | 20y stuck at 0 | At 100 |
|---|---|---|---|---|---|---|---|
| P2-alt | {'eotg_pmc_deliver_liege_value': 1} | 16 | ai | 35.8 | 35.2 | 0.0% | 0.0% |
| P3-alt | {'eotg_gobcorp_peace_gain_value': 2} | 4 | ai | 60.0 | 90.0 | 0.0% | 2.5% |
| P3-alt | {'eotg_gobcorp_peace_gain_value': 2} | 16 | ai | 59.2 | 89.4 | 0.0% | 2.7% |
| P1-cap-alt | {'eotg_corporation_court_erosion_value': -3} | 16 | greedy_all | 0.0 | 85.3 | 31.6% | 0.4% |

**Trade Oligarchy war-share sweep** (4 Princes, AI; the top's own war share varied):

| Top war share | Passive feed / year | First Prince equilibrium | Vassal median |
|---|---|---|---|
| 10.0% | +0.50 | 54.6 | 59.4 |
| 15.0% | +0.25 | 43.9 | 58.6 |
| 20.0% | +0.00 | 31.2 | 57.7 |
| 25.0% | -0.25 | 20.2 | 57.2 |
| 30.0% | -0.50 | 10.0 | 56.8 |

### Frontier in a hostile world (`--hostile`: war reaches the Shoal 25%/yr, Dangerous 40%, occupied 6%/yr; AI holder)

| Type | Completed | Abandoned | Years to complete (median / p90) | Falters per project |
|---|---|---|---|---|
| settlement | 98.8% | 1.2% | 11.0 / 13.0 | 0.032 |
| trade | 97.5% | 2.5% | 13.0 / 15.0 | 0.072 |
| mining | 97.5% | 2.5% | 13.0 / 15.0 | 0.075 |
| military | 100.0% | 0.0% | 13.0 / 15.0 | 0.001 |
| religious | 96.7% | 3.3% | 14.0 / 16.0 | 0.097 |
| research | 95.7% | 4.3% | 15.0 / 17.0 | 0.124 |
| administrative | 90.8% | 9.2% | 13.0 / 16.0 | 0.275 |

### Void Corruption (`models/void.py`; 50-year seats, contact sweep)

Script values read: contact 4% player / 1% AI; Hollowing start 25, drift +4/yr; exposure bands [25.0, 50.0, 75.0]; depth bands [50.0, 85.0].

| Ruler | Contact rate | Seeded by 10 / 25 / 50 y | Ever Touched by 10 / 25 / 50 y | Touched or Hollowed now at 50 y | Ever Hollowed by 50 y | Voidwalkers created / 100 seat-years |
|---|---|---|---|---|---|---|
| ai | script default (1%) | 10.1% / 22.5% / 40.3% | 0.0% / 0.6% / 4.6% | 2.8% | 3.3% | 0.16 |
| ai | 0.5% (0.5%) | 4.7% / 11.9% / 22.9% | 0.0% / 0.2% / 2.5% | 1.7% | 2.0% | 0.10 |
| ai | 1.0% (1%) | 10.1% / 22.5% / 40.3% | 0.0% / 0.6% / 4.6% | 2.8% | 3.3% | 0.16 |
| ai | 2.0% (2%) | 18.5% / 39.6% / 64.3% | 0.0% / 1.0% / 8.2% | 5.2% | 6.3% | 0.29 |
| ai | 4.0% (4%) | 33.5% / 63.7% / 86.6% | 0.0% / 2.1% / 13.4% | 7.9% | 10.2% | 0.46 |
| player | script default (4%) | 33.5% / 63.7% / 86.6% | 0.0% / 2.1% / 13.4% | 7.9% | 10.2% | 0.46 |
| player | 0.5% (0.5%) | 4.7% / 11.9% / 22.9% | 0.0% / 0.2% / 2.5% | 1.7% | 2.0% | 0.10 |
| player | 1.0% (1%) | 10.1% / 22.5% / 40.3% | 0.0% / 0.6% / 4.6% | 2.8% | 3.3% | 0.16 |
| player | 2.0% (2%) | 18.5% / 39.6% / 64.3% | 0.0% / 1.0% / 8.2% | 5.2% | 6.3% | 0.29 |
| player | 4.0% (4%) | 33.5% / 63.7% / 86.6% | 0.0% / 2.1% / 13.4% | 7.9% | 10.2% | 0.46 |

**Stage timings** (player rate, 100-year seats; quartiles in years):

| Voidwalker | Seeded | Touched, given seeded | Hollowed, given Touched | Contact → Touched (25/50/75) | Touched → Hollowed (25/50/75) |
|---|---|---|---|---|---|
| never seated | 98.1% | 34.7% | 85.0% | [19.0, 28.0, 55.0] | [2.0, 4.0, 5.0] |
| as scripted (0004) | 98.4% | 31.4% | 85.4% | [20.0, 29.0, 55.0] | [2.0, 4.0, 5.0] |
| seated at contact | 98.2% | 0.3% | 81.5% | [36.0, 44.0, 58.5] | [5.25, 6.0, 7.0] |

**Void proposals, before and after** (player seat, 4% contact, 100 years, 0004 as scripted):

| Proposal | Override | Metric | Before | After |
|---|---|---|---|---|
| V1 | `{'void.term.has_trait=eotg_void_touched': 2}` | stage_c_per_100_seat_years | 0.038 | 0.211 |
| V1 | `{'void.term.has_trait=eotg_void_touched': 2}` | touched_years_median | 4.000 | 6.000 |
| V1 | `{'void.term.has_trait=eotg_void_touched': 2}` | ever_touched_100y | 0.309 | 0.309 |
| V1 | `{'void.term.has_trait=eotg_void_touched': 2}` | ever_hollow_100y | 0.264 | 0.228 |
| V1 | `{'void.term.has_trait=eotg_void_touched': 2}` | touched_given_seeded | 0.314 | 0.314 |
| V1 | `{'void.term.has_trait=eotg_void_touched': 2}` | voidwalkers_per_100_seat_years | 0.500 | 0.514 |
| V2 | `{'void.slot.0004.chance': 25}` | stage_c_per_100_seat_years | 0.038 | 0.033 |
| V2 | `{'void.slot.0004.chance': 25}` | touched_years_median | 4.000 | 4.000 |
| V2 | `{'void.slot.0004.chance': 25}` | ever_touched_100y | 0.309 | 0.288 |
| V2 | `{'void.slot.0004.chance': 25}` | ever_hollow_100y | 0.264 | 0.243 |
| V2 | `{'void.slot.0004.chance': 25}` | touched_given_seeded | 0.314 | 0.293 |
| V2 | `{'void.slot.0004.chance': 25}` | voidwalkers_per_100_seat_years | 0.500 | 0.940 |
| V3 | `{'void.term.eotg_void_has_voidwalker=yes': -4}` | stage_c_per_100_seat_years | 0.038 | 0.042 |
| V3 | `{'void.term.eotg_void_has_voidwalker=yes': -4}` | touched_years_median | 4.000 | 4.000 |
| V3 | `{'void.term.eotg_void_has_voidwalker=yes': -4}` | ever_touched_100y | 0.309 | 0.318 |
| V3 | `{'void.term.eotg_void_has_voidwalker=yes': -4}` | ever_hollow_100y | 0.264 | 0.267 |
| V3 | `{'void.term.eotg_void_has_voidwalker=yes': -4}` | touched_given_seeded | 0.314 | 0.323 |
| V3 | `{'void.term.eotg_void_has_voidwalker=yes': -4}` | voidwalkers_per_100_seat_years | 0.500 | 0.498 |

## Appendix B: the static exploit scan

See `exploit_scan.md` (generated by `docs/tools/sim/exploit_scan.py`).

## Appendix C: the full ASSUMPTION list

Every number that is not read from the mod's script. The model files carry the same list as `assume()` calls with comments; the reader's `VANILLA_DEFAULTS` holds the vanilla named values. Unresolved names evaluated to 0 or false.

### Models

- `trait_freq`: ({'greedy': 0.12, 'ambitious': 0.12, 'compassionate': 0.1, 'content': 0.1, 'craven': 0.1, 'brave': 0.12, 'paranoid': 0.08, 'sadistic': 0.05, 'callous': 0.08, 'arbitrary': 0.08, 'just': 0.1, 'honest': 0.1, 'arrogant': 0.1, 'cynical': 0.08, 'zealous': 0.1, 'deceitful': 0.1}, 'about 1 in 10 per personality trait (3 traits of ~30)')
- `ruler_mortality_per_year`: (0.035, 'mean reign about 28 years')
- `war_start_per_year`: (0.15, 'a realm enters a war 0.15/yr')
- `war_end_per_year`: (0.5, 'wars last about 2 years; ~23% of years at war')
- `vassal_own_war_start_per_year`: (0.015, 'a vassal starts its own war 0.015/yr, ending at war_end_per_year: ~3% of years')
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
- `void_option_gate_open`: (0.35, 'an option with a trigger (education, personality, age, heir) is open to a given ruler; cult-gated options are closed (eotg_void_is_cult_faith is always = no)')
- `void_education_learning_share`: (0.2, 'one of five educations')
- `void_lunatic_or_possessed_share`: (0.02, 'lunatic_1/_genetic or possessed_1/_genetic')
- `void_piety_level_3_share`: (0.15, 'piety_level >= 3')
- `void_stress_200_share`: (0.05, 'stress >= 200 in a given year')
- `void_ruler_start_age`: ((30, 10), 'a ruler takes the seat at N(30, 10)')
- `void_near_touched`: (False, 'no Void-Touched courtier, vassal or spouse (a lone realm)')
- `void_stage_c_slot_open`: ({'0020': 0.23, '0021': 0.5, '0022': 0.6, '0024': None, '0025': 0.3}, 'P(the slot trigger holds): at war ~23%, a child under 12, a zealous courtier, a vassal below -20; 0024 reads age')

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
- **War state is per owner (H2a):** the top at war about 23% of years, each vassal about 3% from its own wars; a liege's war does not put its vassals at war.
- **Every director, payer and Prince is a direct vassal of the top** (no nesting; see H1).
