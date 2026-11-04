# Decisions B: Corporation and Trade Oligarchy (G2), with suggested answers

**Date:** 2026-11-03. **Scope:** Corporation OQ1–OQ10, Trade Oligarchy (`gobcorp`) OQ1–OQ11, sim proposal P1, and the Trade Oligarchy imbalance (sim M1 / P3).
**Inputs:**
- the specs `docs/specs/governments_v2_g2_corporation.md` §14 and `governments_v2_g2_gobcorp.md` §14;
- `docs/specs/governments_v2_g2_succession.md`;
- `docs/qa/mechanics_sim_2026-11-03/REPORT.md`;
- the script in `common/*/eotg_corporation_*`, `common/*/eotg_gobcorp_*`, `common/succession_election/eotg_government_elections.txt` and `common/script_values/eotg_government_succession_values.txt`.

**Path notes:**
- `G/` means `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/` (1.20.1.1).
- `M:<id>/` means `D:/SteamLibrary/steamapps/workshop/content/1158310/<id>/`.

**Mod techniques are observations only.** Under the project rule they are never precedent and never copied. Every recommendation below rests on vanilla or on the mod's own design.

**New numbers in this file:**
- **Scratch runs:** some numbers come from 2,000-run what-ifs made with a copy of the repo sim loop (`docs/tools/sim/whatif/trade_variants.py`, `trade_variants2.py`; it imports `docs/tools/sim` read-only, seed 20261103, 100 years). The baseline reproduces REPORT M1 (4 Princes, AI: First Prince 24.0 / vassal median 57.4; REPORT gives 23.3 / 57.4).
- **Not in the sim:** none of these numbers have been played in game.

---

## Summary table

| # | Decision | Suggested answer | Confidence |
|---|---|---|---|
| CO-OQ1 | Scripted variable or vanilla influence | Scripted (as built) | High |
| CO-OQ2 | Inheritance | 50% (as built) | High |
| CO-OQ3 | Directors erode the CEO | Yes: at most once a year, and only while the director's influence is above the CEO's (as built); amount **−2** (P1) | High |
| **P1** | Erosion −5 → −2 | **Take it**, with the two loc lines | High |
| CO-OQ4 | Visible story | Yes | High |
| CO-OQ5 | Start values | 50 / 20 (as built) | Medium-high |
| CO-OQ6 | First-pass numbers | Approve, with P1; L1 AI uptake raise later | Medium |
| CO-OQ7 | AI adoption | Not yet (`always = no`); later the vanilla affinity shape | High |
| CO-OQ8 | §11 events | None now; E3 first when opened | Medium |
| CO-OQ9 | Keep the councillor +1 | No (as built) | Medium-high |
| CO-OQ10 | Port capital to enter | No: a castle capital is a valid holding | High |
| TO-OQ1 | Scripted 0–100 variable | Yes | High |
| TO-OQ2 | Inheritance | 75% (as built) | Medium-high |
| TO-OQ3 | Index, not a true fraction | Index | High |
| TO-OQ4 | Visible story | Yes | High |
| TO-OQ5 | Start values | 40 / 20 (as built) | Medium |
| TO-OQ6 | First-pass numbers | Approve, **plus the charter-dues war fix** below; reject P3 | Medium |
| TO-OQ7 | AI adoption | Not yet | High |
| TO-OQ8 | §11 events | None now; E4 first when opened | Medium |
| TO-OQ9 | Sort electors by market share | **Yes** (reverses the spec's default); gold as the tie-break | Medium |
| TO-OQ10 | Corner hits every vassal Prince, at most once a year each | Yes (as built); the guard is cheap insurance | High |
| TO-OQ11 | `diplomacy = -1` → `+1` | Yes, `diplomacy = 1` | Medium |
| **IMB** | Princes out-share the First Prince | **Partly a feature, partly a bug.** Fix: the First Prince's war loss is −2 instead of −4 while partner Princes keep trading ("charter dues"). | Medium-high |

---

# Part 1: the Corporation

## CO-OQ1: Scripted variable rather than vanilla influence

1. **Question.** Should board influence be the scripted `eotg_corp_board_influence` (0–100) or vanilla `influence`? If scripted, the T11 probe is skipped.
2. **Vanilla comparables.**
   - `government_has_influence` appears on admin-mechanic governments only: `G/common/governments/00_government_types.txt:530` (administrative), `:884` (celestial), `:1199` (steppe admin), `:1329` (meritocratic), and `01_japan_government_types.txt:72`. Every one of them sets `mechanic_type = administrative` (`:550`, `:824`, `:1132`, `:1265`).
   - Influence is on a different scale: levels at `LEVELS_INFLUENCE = { 1000 2000 4000 8000 16000 }` (`G/common/defines/00_defines.txt:156`), and named amounts of 10 / 30 / 60 / 100 (`G/common/script_values/07_ep3_values.txt:4-7`).
   - The admin passive gains are hard-coded in defines, for being a governor or allied to the top liege (`00_defines.txt:318-320`), and the appointment machinery spends influence (`G/common/succession_appointment/admin_governor.txt:1-60`, `07_appointment_values.txt:394`, `:1406`).
3. **Mod techniques.** Godherja (`M:2326030123/common/governments/gh_government_types.txt:650-790`), AGOT (`M:2962333032/common/governments/00_government_types.txt:457-567`) and After the End (`M:3192256710/common/governments/ate_government_types.txt:114-192`) all get "influence" by making the republic `mechanic_type = administrative`, so they take on the whole admin stack. The one scripted pseudo-currency seen is Fallen Eagle's `ecostability`, a monthly variable clamped to ±150 (`M:3515718688/common/on_action/economic_on_actions.txt:28-75`).
4. **Suggested answer.** **Scripted**, as built. Skip T11.
5. **Confidence.** High. Vanilla ties influence to the admin mechanic, and its scale and spending don't fit the 0–100 bands that the election reads.
6. **Script change.** None.

## CO-OQ2: 50% inheritance to the primary heir

1. **Question.** Should the heir get max(own, 50% of the predecessor's)? Alternatives: 75%, or 0%.
2. **Vanilla comparables.**
   - Legitimacy carries over at 25%, and only when the heir rises in tier: `LEGITIMACY_INHERITED = 0.25` (`G/common/defines/00_defines.txt:316`).
   - Influence keeps at most 50% of its progress on a level drop: `LEVEL_DROP_MAX_RETAINED_PROGRESS_INFLUENCE = 0.5` (`:167`).
   - Prestige, piety and influence are personal currencies and are not inherited.
3. **Mod techniques.** Nothing comparable. AGOT passes bank debt to the heir (`M:2962333032/common/scripted_effects/00_agot_banking_effects.txt:3561`), but that is an asset or liability, not standing.
4. **Suggested answer.** **50%**, as built. Board influence is personal standing, which vanilla carries over at 25–50%. 75% would make the hold on the board a family possession and blunt "a new chief must win the board".
5. **Confidence.** High.
6. **Script change.** None (`eotg_corporation_values.txt:51-56`).

## CO-OQ3: Directors' gains erode the CEO

1. **Question.** Should Court the Board also take from the CEO liege? Orchestrator default, as built: yes, at most once a year per CEO (`eotg_corp_board_eroded`, 1 year), and only while the director's influence after the gain is above the CEO's (`G2 decisions :152-169`).
2. **Vanilla comparables.**
   - **Clan house unity** is vanilla's "members' standing moves the head's number" mechanic. Each year it adds up every adult house member's opinion of the house head, then applies **one** capped step to unity, `minor_unity_gain` or `minor_unity_loss` (= 2), whatever the number of members (`G/common/on_action/yearly_on_actions.txt:1145-1258`, the step at `:1241-1253`; `minor_unity_value = 2` at `G/common/script_values/00_unity_values.txt:7`, loss at `:16`). That is a scale-free yearly cap of 2, the same shape as the built guard, at the P1 value.
   - **Feudal and princely elections:** a powerful vassal gets more vote weight when they are stronger than the ruler (`G/common/succession_election/00_feudal_elective.txt:35-49`, `01_princely_elective.txt:22-35`). So a vassal who outgrows the liege weighs on the liege's succession, and the "only while above the CEO" condition matches that.
3. **Mod techniques.** Godherja's clique-authority laws trade vassal power against liege power with multipliers: at low authority, vassal clique weight ×1.25 and the top liege ×0.8 (`M:2326030123/common/script_values/GH_clique_values.txt:350-383`).
4. **Suggested answer.** **Yes, keep the erosion, the once-a-year cap and the "director above the CEO" condition. Change the amount to −2** (P1).
5. **Confidence.** High.
6. **Script change.** See P1.

## P1: Court the Board erosion −5 → −2

1. **Question.** Should erosion change from −5 to −2? REPORT H1: under full director pressure the CEO is dead at 0. 52.2% of runs stay at 0 for 20+ years with 16 directors; the CEO sits at 0 in 32.2% of years with 8 directors and 8.0% with 4.
2. **Vanilla comparables.**
   - −2 is vanilla's `minor_unity_loss` (`00_unity_values.txt:7,16`), the size of the yearly clan-unity step from member opinion (`yearly_on_actions.txt:1241-1253`).
   - With erosion at 2, the yearly results feed (+3, `eotg_corporation_values.txt:62`) outruns the worst case for erosion (−2 once a year). A solvent CEO at peace therefore nets +1 even when every director courts. At −5 the same CEO nets −2.
3. **Mod techniques.** Same as CO-OQ3.
4. **Suggested answer.** **Take P1.** Sim figures (REPORT P1 table):

   | Scenario | Before | After |
   |---|---|---|
   | 16 directors, `greedy_all`: runs stuck at 0 for 20+ years | 52.2% | 0.0% |
   | 16 directors, `greedy_all`: CEO equilibrium | 0 | 9.6 |
   | 16 directors, AI: CEO equilibrium | 32.5 | 37.5 |
   | 16 directors, player: CEO equilibrium | 47.5 | 55.4 |

   −3 was tested and doesn't fix it: 31.6% of runs still stuck at 0 (REPORT side checks).
5. **Confidence.** High.
6. **Script change.**
   - `common/script_values/eotg_corporation_values.txt:73`: `eotg_corporation_court_erosion_value = -2`.
   - `localization/english/eotg_corporation_l_english.yml:28`: "…falls by 5" → "…falls by 2".
   - `:7`: "Every director who courts the board takes 5 from you." → "A director who courts the board and passes your hold takes 2 from you, at most once a year." The current line also omits the cap and the condition.
   - The patch already in `proposed_tuning.patch` carries the value and the loc.

## CO-OQ4: A visible story

1. **Question.** Should the story be visible (`visible = yes`), so the counter shows?
2. **Vanilla comparables.** `G/common/story_cycles/book_translation_story_cycle.txt:2` (`visible = yes`), with the fields documented in `_story_cycles.info`. Vanilla has no other non-GUI way to show a scripted number. The project's shipped Cartel story uses the same shape.
3. **Mod techniques.** None observed. The mods reviewed that have a pseudo-currency show it through events or GUI.
4. **Suggested answer.** **Yes.**
5. **Confidence.** High.
6. **Script change.** None. Tiger's `visible` / `icon` / `background` / `visualization` warnings are already on the benign list.

## CO-OQ5: Start values 50 (CEO) / 20 (director)

1. **Question.** Should a CEO start at 50 and a director at 20?
2. **Vanilla comparables.**
   - `starting_influence` depends on age and personality, not rank (`G/common/script_values/01_starting_values.txt:248-302`).
   - `starting_merit` does depend on rank for vassal rulers (`:305` onward). Vanilla uses both shapes.
   - Election bands: 40 / 75 (`eotg_corporation_values.txt:98-99`). A CEO at 50 starts with the +1 board vote; directors at 20 must court the board to reach it.
3. **Mod techniques.** None relevant.
4. **Suggested answer.** **50 / 20**, as built.
   - The sim's AI CEO settles at 36.6–39.6 (37.5 after P1). So an AI CEO drifts from just above band 1 (40) to just below it, and its own +1 vote flickers.
   - That is acceptable: a seated chief has to keep the hold to keep the vote.
   - If the owner wants a seated chief to hold band 1, set band 1 to **35** (`eotg_corporation_board_vote_band_1_value`, `:98`) rather than raising the start value.
5. **Confidence.** Medium-high.
6. **Script change.** None. Optional: `:98` 40 → 35, plus the loc "(40+)" in `eotg_corporation_su_vote_board` and the `_info` line.

## CO-OQ6: First-pass numbers

1. **Question.** Approve these?
   - Results +3 / debt −5 a year.
   - Restructure −25 for +10% income and −10% build cost for 5 years, with −10 director opinion.
   - Court +15 / −5 for medium gold.
   - Exit ×2 legitimacy, max 200.
   - Modifier +10% income and +10 vassal opinion at 100.
2. **Vanilla comparables.**
   - Exit cap: `major_legitimacy_gain = 200` (`G/common/script_values/00_legitimacy_values.txt:174`).
   - Court cost: `medium_gold_value` is dynamic, with a floor of 50 (`G/common/script_values/00_basic_values.txt:82`) and a static maximum of 300 (`:83`, scaled by era).
   - `vassal_opinion` is a vanilla modifier key (`G/common/court_types/00_court_types.txt:589`).
   - A 5-year cooldown is shorter than vanilla's major admin decisions (15–20 years, `06_ep3_admin_decisions.txt:24, 309, 779`), but these are recurring government verbs, not one-off reforms.
3. **Mod techniques.**
   - AGOT trims bank value by a multiplier every 5 years (×0.875 + 0.005 × stewardship, cap 0.975) as a drift toward equilibrium (`M:2962333032/events/agot_events/agot_banking_events.txt:5193-5241`).
   - The Corporation needs no such trim: its sources and sinks already settle at about 37–40 (AI).
4. **Suggested answer.** **Approve, with P1** (Court +15 / −2).
   - Sim L1: AI uptake of Court the Board is low, 3.2% a year. Raising its `ai_will_do` base from 5 to 15 is a **separate later step after P1**: at full pressure, P1 already holds the CEO at 9.6 rather than 0.
   - The exit loop is not a farm: 350 prestige for at most 200 legitimacy every 10 years (REPORT L5).
5. **Confidence.** Medium. These are first-pass values; V-CO14 is the real test.
6. **Script change.** P1 only. Later (after V-CO14): `common/decisions/eotg_corporation_decisions.txt:178`, `base = 5` → `15`.

## CO-OQ7: AI adoption

1. **Question.** Should the AI be allowed to take Incorporate the Realm?
2. **Vanilla comparables.**
   - `convert_to_administrative_decision`: `ai_will_do` base 0, raised only by cultural affinity (+50 / +100 for bureaucratic ethos, legalistic tradition, a historically admin culture), and lowered by martial cultures (`G/common/decisions/dlc_decisions/ep_3/06_ep3_admin_decisions.txt:1223-1309`).
   - Vanilla never lets the AI leave the admin government: `convert_to_feudalism_from_administrative_decision` has `ai_potential = { always = no }` (`:1543-1548`).
3. **Mod techniques.** None relevant.
4. **Suggested answer.** **Not yet.** Keep `ai_potential = { always = no }`.
   - When it opens (after V-CO14 and Gate 1), copy vanilla's shape: base 0, with affinity terms on the mod's own cultures.
   - The spec's stewardship and greed terms can stay as secondary terms.
5. **Confidence.** High.
6. **Script change.** None.

## CO-OQ8: The §11 events

1. **Question.** Should the §11 events be built (E1 The Board Meets, E2 A Director Overreaches, E3 Quarterly Losses, E4 Hostile Bid, E5 the v1 lift)?
2. **Vanilla comparables.** Vanilla's admin flavour runs off a yearly pulse with a chance gate, e.g. governance contracts at 70% (`G/common/on_action/yearly_on_actions.txt:1260-1280`). E3 rides the existing debt branch the same way.
3. **Mod techniques.** ATE Sci-Fi fires a yearly "Congress" event for a legislative ruler that trades currencies for one another (`M:3202046724/events/zzz_scifi_enclave_events.txt:2898`, from `common/on_action/yearly_on_actions.txt:10-19`).
4. **Suggested answer.** **None now.** Adding events is the owner's call (project memory). When opened, build **E3 first**: it fires from the CO2 debt branch, which already exists, and both reads and moves the resource. Then E1, which needs a stored vote leader.
5. **Confidence.** Medium.
6. **Script change.** None.

## CO-OQ9: Keep the councillor +1 alongside the influence bands

1. **Question.** Should a councillor of the holder keep +1 vote strength beside the influence bands?
2. **Vanilla comparables.**
   - Vanilla vote strength reads tier, powerful vassal, and a council seat **only** for the court chaplain under a lay-clergy theocracy (`G/common/succession_election/01_princely_elective.txt:37-47`; `00_feudal_elective.txt:50-59`). There is no general councillor bonus.
   - Only rulers can be electors, so a landless councillor never votes anyway.
   - The mod already gives councillors seat priority: +50 (`common/script_values/eotg_government_succession_values.txt:19-20`).
3. **Mod techniques.** Fallen Eagle weights votes by office held, e.g. Praetorian Prefect +75 (`M:3515718688/common/succession_election/TFE_imperial_elective.txt:38-200`). Godherja adds a councillor bonus to the powerbase (`GH_clique_values.txt:241-375`).
4. **Suggested answer.** **No**, as built. A seat is not a hold. The seat-priority +50 already gives councillors the vote; the influence bands give the weight.
5. **Confidence.** Medium-high.
6. **Script change.** None.

## CO-OQ10: Entry requires a Port capital

1. **Question.** Should Incorporate the Realm require a Port (city) capital, given the government is city-primary?
2. **Vanilla comparables.**
   - `valid_holdings` are "holdings that can be held directly by rulers of this government type" (`G/common/governments/_governments.info:426-431`).
   - The Corporation sets `primary_holding = city_holding` and `valid_holdings = { castle_holding }` (`eotg_corporation_government.txt:38-39`), exactly as vanilla `republic_government` (`00_government_types.txt:65-66`). So a castle capital is a valid holding, not a penalized one.
   - Vanilla's own conversion, `convert_to_administrative_decision`, never touches the capital holding (no `set_holding_type` in `06_ep3_admin_decisions.txt:724-1222`).
3. **Mod techniques.** The Godherja republic is city-primary and has no capital requirement (`gh_government_types.txt:650-790`).
4. **Suggested answer.** **No Port requirement.** V-CO10 only records the outcome, and it should pass with no penalty.
5. **Confidence.** High.
6. **Script change.** None. Remove the "UNVERIFIED-VANILLA (V-G17)" capital-penalty worry from spec §6.1 and cite `_governments.info:426-431`.

---

# Part 2: the Trade Oligarchy (internal key `gobcorp`)

## IMB: Princes out-share the First Prince. Feature or bug?

**The finding (REPORT M1, after the local audit).**
- AI vassal Princes settle at 55–57. The First Prince settles at 23–28.
- The First Prince's feed is +1 in peace and −4 in war (`eotg_gobcorp_values.txt:62-63`, ticked on the owner's own `is_at_war` in `eotg_gobcorp_story.txt:100-130`).
- That feed is net 5p − 4 for p = share of years at peace. It is zero at 20% war, and the modelled top is at war about 23% of years.
- Vassals are at war only in their own wars, about 3% of years, so their feed is about +0.85 a year.

**Diagnosis: half feature, half bug.**
- **Feature (keep):** a partner Prince may out-share the First Prince. That is "first among equals, no single head" (spec §8), and vanilla lets a vassal who outgrows the ruler out-vote them: the feudal +1 and princely +2 "more powerful than the ruler" bonus (`00_feudal_elective.txt:35-49`, `01_princely_elective.txt:22-35`). In vanilla admin, governors also gain influence passively, +1 / +1.5 a month (`00_defines.txt:318-320`).
- **Bug (fix):** the *cause and size* of the gap.
  - It is set almost entirely by how often the First Prince fights, not by play. Scratch sweep, 4 Princes, AI:

    | First Prince war share | 10% | 20% | 30% | 40% |
    |---|---|---|---|---|
    | First Prince equilibrium | 54 | 31 | 10 | 2 |

  - The independent ruler fights the charter's external wars. Each Prince's war is private. So the yearly tick charges the First Prince for wars waged on the realm's behalf.
  - **The vote.** A warlike First Prince sits below the first vote band (30); only 1.8% of years are at 30 or above at 40% war.
  - **The AI.** The AI's "behind" term on Corner the Market (+20 below 40) is on permanently.
  - **The market.** "First among equals" becomes "last among equals".
  - **Vanilla offsets the same structural gap at the top.** The admin emperor's own family gets a candidate bonus scaled by the holder's legitimacy (`G/common/succession_appointment/admin_emperor.txt:428-431`, `30 × legitimacy_level`). The top liege also takes a cut of vassal income that keeps flowing through war: admin `monthly_treasury_from_vassals = 0.85` with vassals `monthly_treasury_from_liege_mult = -0.15` (`00_government_types.txt:517, 520-522`); republic vassals pay 20% tax to the liege, 30% with the cultural parameter (`G/common/subject_contracts/contracts/republic.txt:44-98`, value at `:86-87`).

**Options tested (scratch, 2,000 runs; First Prince / vassal median):**

| Variant | 1 Prince, AI | 4, AI | 16, AI | 4, player | 4 Princes, AI, by war share 10 / 20 / 30 / 40% |
|---|---|---|---|---|---|
| Baseline | 28.9 / 55.2 | 24.0 / 57.4 | 27.3 / 56.8 | 49.5 / 47.7 | 54 / 31 / 10 / 2 |
| P3: war −3 for everyone | 39.2 / 57.5 | 34.4 / 59.7 | 36.8 / 59.4 | 62.4 / 49.4 | (knife-edge moves to 25%) |
| Flat dues +1 a year to the First Prince | 73.7 / 57.7 | 70.2 / 60.3 | 71.2 / 60.3 | 91.0 / 48.6 | 93 / 77 / 53 / 29: **overshoots** |
| Dues +0.5 a year | 51.0 / 56.6 | 47.0 / 59.0 | 48.3 / 59.0 | 75.0 / 48.0 | 77 / 54 / 30 / 10: still steep |
| Vassals −1 in their liege's war | 28.9 / 41.4 | 24.0 / 44.2 | 27.3 / 43.5 | 49.5 / 34.1 | levels everyone down; rejected |
| **D: charter dues in war (First Prince war loss −2 while a partner Prince is at peace)** | **49.8 / 56.6** | **44.7 / 58.9** | **46.4 / 58.8** | **75.0 / 47.9** | **64 / 49 / 34 / 18** |

**Suggested answer: D, "charter dues".**
- **The rule.** In a war year, a Trade Oligarchy ruler with at least one Trade Oligarchy vassal at peace loses **2** instead of 4. The partners' trade keeps paying dues to the charter's First Prince while they fight.
  - This is a liege-only feed, shaped on vanilla's war-proof vassal skim.
  - It is **scale-free**: it is the same with 1 or 16 partners, so it cannot repeat the PMC H2 problem, where the gain scaled with vassal count.
  - A lone First Prince with no partners keeps −4.
- **What it gives:**
  - The AI First Prince settles at 45–50 against partners at 57–59: first among equals, slightly behind the strongest partners, never starved.
  - A First Prince who plays (Corners on cooldown) settles at 75, against partners at 48.
  - War sensitivity is roughly halved (64 → 18 across 10–40% war, against 54 → 2).
  - The share of AI years at or above the first vote band rises from 39% to 80%.
- **Rejected:**
  - **P3** (global −3): it lifts the vassals too, and leaves the knife-edge at 25%.
  - **Flat dues:** they overshoot, and the First Prince ends up above the partners in every realm.
  - **"Vassals suffer the liege's war":** it fixes the gap by making everyone poorer.

**Confidence.** Medium-high. The direction rests on vanilla. The exact −2 depends on the real map's war rate, so V-TO14 should record the First Prince's war share.

**Script change.**
- `common/script_values/eotg_gobcorp_values.txt`, after `:63`:
  ```
  # Charter dues (decision IMB, 2026-11-03): at war, but partner Princes still trade.
  # Net war loss for a liege with at least one Trade Oligarchy vassal at peace.
  # Liege-only, scale-free; shape: vanilla's war-proof vassal skim
  # (G/common/governments/00_government_types.txt:517,520-522; republic.txt:86-87).
  eotg_gobcorp_war_loss_charter_value = -2
  ```
- `common/story_cycles/eotg_gobcorp_story.txt:100-130`: add a branch **first** inside the yearly `first_valid`. It stays the single cadence authority:
  ```
  triggered_effect = {
      trigger = {
          story_owner = {
              eotg_gobcorp_is_landed_gobcorp = yes
              is_at_war = yes
              any_vassal = {
                  government_has_flag = eotg_government_is_gobcorp
                  is_at_war = no
              }
          }
      }
      effect = {
          story_owner = {
              eotg_gobcorp_change_market_share_effect = { AMOUNT = eotg_gobcorp_war_loss_charter_value }
          }
      }
  }
  ```
  The existing war branch (−4) and peace branch (+1) follow unchanged.
- **Loc,** `localization/english/eotg_gobcorp_l_english.yml:7`: "Each year at war costs 4." → "Each year at war costs 4, or 2 while partner Princes keep trading."
- **Sim:** `docs/tools/sim/models/gobcorp.py:36` needs the same branch for future reruns (every top in the model has ≥1 vassal, so `top_war = war_loss_charter_value`).
- **Withdraw P3** from `proposed_tuning.patch`.

## TO-OQ1: A scripted 0–100 variable

1. **Question.** Should market share be the scripted `eotg_gobcorp_market_share` (0–100)?
2. **Vanilla comparables.**
   - Vanilla has no trade or market mechanic in 1.20.1.1: no trade, trade-route or merchant system in `G/common/`, only flavour text and modifiers.
   - Gold can't double as a market position, because vanilla spends it on everything (costs throughout `00_basic_values.txt:7-116`).
   - The influence reasoning of CO-OQ1 applies.
3. **Mod techniques.** Fallen Eagle's trade nodes accumulate upstream power through global variables and turn it into province income modifiers (`M:3515718688/common/on_action/trading_on_actions.txt:8-400`). It is geographic, not per character.
4. **Suggested answer.** **Yes.**
5. **Confidence.** High.
6. **Script change.** None.

## TO-OQ2: 75% inheritance

1. **Question.** Should the heir get max(own, 75%)? Alternative: 50%, as the Corporation.
2. **Vanilla comparables.**
   - Personal standing passes at 25–50% (CO-OQ2: `00_defines.txt:167, 316`).
   - Assets (gold, holdings) pass whole to the primary heir. That is engine behaviour, with no define.
   - Market share is a book of business, so it sits between the two.
3. **Mod techniques.** AGOT bank shares pass with the house (`take_share_interaction`, `M:2962333032/common/character_interactions/00_agot_banking_interactions.txt:666`).
4. **Suggested answer.** **75%**, as built. With the IMB fix the First Prince settles at about 46, so an heir starts at about 34, above the first vote band, and the house keeps its book. Candidates are dynasty-only (owner ruling), so the share stays in the house.
5. **Confidence.** Medium-high.
6. **Script change.** None (`eotg_gobcorp_values.txt:51-56`).

## TO-OQ3: Share as an index, not a true fraction

1. **Question.** Should share be an index that need not sum to 100, or a true sum-to-100 market?
2. **Vanilla comparables.** Every vanilla per-character currency is unnormalised: dread, legitimacy, influence, unity (`00_house_unities.txt:1-3`, `default_value = 100`, `min_value = 0`, with no sum across houses). Vanilla never keeps a zero-sum global pool across characters.
3. **Mod techniques.** AGOT's bank shares are a true fixed pool (`var:IB_Shares`). To keep it from printing money it needs a buy price of value × 1.05 (`agot_banking_events.txt:5270-5280`), plus dividends split per share (`:5356-5400`). That is the cost and complexity the spec rejected.
4. **Suggested answer.** **Index.**
5. **Confidence.** High.
6. **Script change.** None.

## TO-OQ4: A visible story

As CO-OQ4: **yes**, high confidence, no change. Vanilla shape: `book_translation_story_cycle.txt:2`.

## TO-OQ5: Start values 40 (First Prince) / 20 (Prince)

1. **Question.** Should the First Prince start at 40 and a Prince at 20?
2. **Vanilla comparables.** As CO-OQ5 (`01_starting_values.txt:248-302`, `:305` onward). The vote bands are 30 / 60 / 90 (`eotg_gobcorp_values.txt:94-96`).
3. **Mod techniques.** None relevant.
4. **Suggested answer.** **40 / 20**, as built.
   - With the IMB fix, 40 is close to the First Prince's AI equilibrium (45–50), so there is no large early swing.
   - Princes climb from 20 to about 57 over about 40 years at +0.85 a year. That gives the early game a First Prince who leads, and a later one who must defend.
5. **Confidence.** Medium. Without the IMB fix, a 40 start just decays to about 24.
6. **Script change.** None.

## TO-OQ6: First-pass numbers

1. **Question.** Approve these?
   - Peace +1 / war −4.
   - Corner +15 own, −5 to each vassal Prince, for major gold, every 5 years.
   - Undercut +10 / −10 for minor gold, every 5 years.
   - Exit ×5 gold, max 500.
   - Modifier +15% income at 100.
2. **Vanilla comparables.**
   - The exit cap of 500 equals `major_gold_max_value_static = 500` (`00_basic_values.txt:116`).
   - Corner costs `major_gold_value` (floor 75, `:115`). Undercut costs `minor_gold_value` (floor 15, `:49`).
   - The +15% income at 100 sits between republic tax shares (20–30%, `republic.txt:86-87, 71-72`) and the admin skim (`00_government_types.txt:517`).
3. **Mod techniques.** Fallen Eagle's AI-only decision raises a trade-node cap by +5 for 500 gold (`M:3515718688/common/decisions/ai_only_decisions.txt:225-240`), the same order of gold per point as Corner.
4. **Suggested answer.**
   - **Approve, with the IMB charter-dues branch.**
   - **Reject P3.** Keep war −4 for Princes' own wars: a private war really is bad for a Prince's trade.
   - Corner's squeeze scales with the number of Princes: −5 each, so −80 in total at 16 Princes for +15. That is acceptable for an index (TO-OQ3), and the AI already avoids it with 3 or more Princes (−10 at `eotg_gobcorp_decisions.txt:105-111`).
   - The exit loop is not a farm: 350 prestige for at most 500 gold every 10 years (REPORT L5).
5. **Confidence.** Medium.
6. **Script change.** The IMB change only.

## TO-OQ7: AI adoption

As CO-OQ7: **not yet**, high confidence, no change. Vanilla shape for later: `06_ep3_admin_decisions.txt:1223-1309`, with exit AI off at `:1543-1548`.

## TO-OQ8: The §11 events

1. **Question.** Should the §11 events be built (E1 A Partner Calls In a Debt, E2 Buy a Vote, E3 Price War, E4 A Ruinous War, E5 the v1 lift)?
2. **Vanilla comparables.** As CO-OQ8 (the yearly pulse and chance gate, `yearly_on_actions.txt:1260-1280`).
3. **Mod techniques.** Fallen Eagle's bribe-a-pot senate decisions (`M:3515718688/common/decisions/TFE_senate_decisions.txt:20, 250-300`) are the shape of E2.
4. **Suggested answer.** **None now** (owner's call). When opened, build **E4 first**: it sits on the war branch the IMB fix touches, so the First Prince gets an active answer to a long war. Then E3, which can be counted from the Undercut effect.
5. **Confidence.** Medium.
6. **Script change.** None.

## TO-OQ9: Sort electors by market share instead of gold

1. **Question.** TO5 made vote *strength* read market share, but elector *selection* still sorts by gold (`eotg_gobcorp_su_prince_priority_value`, `eotg_government_succession_values.txt:47-60`). Should selection also sort by market share? The spec's default is no.
2. **Vanilla comparables.**
   - Vanilla's elector `priority` sorts by the standing that matters to that election. Princely: holder +200, an HRE elector title +75, faith fit +4 to +15 (`G/common/succession_election/01_princely_elective.txt:92-150`).
   - The mod's own rule is that one number drives both the market and the vote (`governments_v2.md` §2, quoted in the spec §1).
   - Today a gold-rich Prince with 0 share takes one of the 9 seats and votes at weight 1, while a Prince with share 70 and little gold may be left out. The sim models electors as the richest 8 (`models/gobcorp.py:85`).
3. **Mod techniques.**
   - AGOT Free Cities: vote strength is raw gold, and electors are house heads (`M:2962333032/common/succession_election/00_agot_free_cities_elective.txt:1-60`).
   - ATE plutocracy: gold × 0.05 + income × 0.5 (`M:3192256710/common/succession_election/high_republic_elective.txt:382`).
   - LotR: county development + income bands (`M:2291024373/common/succession_election/lotr_elective.txt:134-143`).
   - All of them use one measure for both seat and weight.
4. **Suggested answer.** **Yes (reverses the spec default).** Sort by market share, with gold as the tie-break. Keep the `gold > 0` elector trigger: a partner in debt has no say, which is a flavour rule and keeps the trigger cheap.
5. **Confidence.** Medium. It is a coherence fix, not a balance fix.
6. **Script change.**
   - `common/script_values/eotg_government_succession_values.txt:47-60`:
     ```
     eotg_gobcorp_su_prince_priority_value = {
         value = 0
         if = {
             limit = { this = scope:holder }
             add = 2000                                   # holder always seated (princely :92-97)
         }
         else = {
             add = {
                 value = eotg_gobcorp_market_share_value  # 0-100: the seat follows the book
                 multiply = 10
             }
             add = {                                      # tie-break: treasury, 0-9
                 value = gold
                 divide = 100
                 min = 0
                 max = 9
             }
         }
     }
     ```
   - Loc, `localization/english/eotg_government_l_english.yml`:
     - `:70`: "the richest Princes" → "the Princes with the largest market share".
     - `:81`: "the richest first" → "the largest market share first".
   - Sim: `models/gobcorp.py:85`, order by `vas` instead of `v_gold`.
   - Rerun V-SU / V-TO13.

## TO-OQ10: Corner the Market hits every vassal Prince, at most once a year each

1. **Question.** Should Corner hit every vassal Prince including counts, or only duke- and kingdom-tier Princes? Orchestrator default, as built: all of them, each drained at most once a year (`eotg_gobcorp_cornered`, `eotg_gobcorp_decisions.txt:73-87`).
2. **Vanilla comparables.**
   - The feudal election counts every tier, with tier bonuses on top (`00_feudal_elective.txt:20-34`). Vanilla doesn't exempt counts from realm-wide liege actions.
   - The once-a-year guard is the same kind of cap as the yearly clan-unity step (`yearly_on_actions.txt:1241-1253`).
3. **Mod techniques.** None relevant.
4. **Suggested answer.** **Yes, all vassal Princes; keep the guard.**
   - The guard almost never fires. Corner already has a 5-year cooldown on the First Prince, and each Prince has one liege.
   - It bites only when a new First Prince (whose decision cooldown is fresh) corners within a year of the last, or a Prince changes liege. That makes it cheap insurance against a succession double-squeeze.
   - Exempting counts would make the most numerous Princes immune to the top-tier verb.
5. **Confidence.** High.
6. **Script change.** None.

## TO-OQ11: Change `diplomacy = -1` to `+1`

1. **Question.** Should the government's `diplomacy = -1` (carried over from v1, `eotg_gobcorp_government.txt:54`) become `+1`? Assessment P4.
2. **Vanilla comparables.**
   - No vanilla government type gives a skill modifier: none in `00_government_types.txt`. Skills are generic modifiers, so the field is legal but has no vanilla precedent for its value.
   - The election already scores stewardship (`eotg_government_succession_values.txt:64-77`), so a stewardship bonus would count twice.
3. **Mod techniques.** None relevant.
4. **Suggested answer.** **Yes: `diplomacy = 1`.**
   - The fiction is bargaining and partnerships.
   - Diplomacy doesn't double-count in the candidate score, which reads stewardship and gold.
   - It also makes the Trade Oligarchy match the Corporation's `diplomacy = 1` (`eotg_corporation_government.txt:54`) rather than differ from it. The governments still differ in income (+10% against +5%) and in the resource.
5. **Confidence.** Medium. This is a design call with no vanilla anchor.
6. **Script change.** `common/governments/eotg_gobcorp_government.txt:54`: `diplomacy = -1` → `diplomacy = 1`, and the comment `# v1` → `# owner OQ11 (was -1 in v1)`. Recheck V-G checks for the government tooltip.

---

## Election numbers (REPORT Appendix A), for context

| Government | Resource leader's pick wins | Non-dynast would win without the dynasty rule |
|---|---|---|
| Corporation | 58.7–81.3% | 3.7–71.3% (71.3% at 16 directors, all courting) |
| Trade Oligarchy | 61.6–87.2% | 2.7–37.2% |

- The resource-weighted vote is live in both governments, and the owner's dynasty-only candidate rule is what keeps the house on the throne. Neither answer above changes that rule.
- TO-OQ9 makes the elected seats the Princes with the largest share, which strengthens the "leader's pick wins" column without opening candidacy.

## Files referenced
- Scratch what-ifs (not repo):
  - `docs/tools/sim/whatif/trade_variants.py`
  - `docs/tools/sim/whatif/trade_variants.py`
- Repo files to change if the answers are taken:
  - `common/script_values/eotg_corporation_values.txt` (P1)
  - `common/script_values/eotg_gobcorp_values.txt` (IMB)
  - `common/story_cycles/eotg_gobcorp_story.txt` (IMB)
  - `common/script_values/eotg_government_succession_values.txt` (TO-OQ9)
  - `common/governments/eotg_gobcorp_government.txt` (TO-OQ11)
  - `localization/english/eotg_corporation_l_english.yml` :7, :28
  - `localization/english/eotg_gobcorp_l_english.yml` :7
  - `localization/english/eotg_government_l_english.yml` :70, :81
  - `docs/tools/sim/models/gobcorp.py` :36, :85
