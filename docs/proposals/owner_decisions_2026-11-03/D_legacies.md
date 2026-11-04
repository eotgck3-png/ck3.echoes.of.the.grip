# Decisions: Grip Legacies (formerly Confluence Legacies), `docs/specs/legacies_v2.md` §10

**Scope:** suggested answers for Q7, Q4, Q8, Q9, Q10 and the 0105 dynasty gate, with Q2 noted. Read-only research, 2026-11-03.

**Precedence:**
- **Vanilla** is CK3 1.20.1.1. Citations are `G/<path>:line`, where G = `D:/SteamLibrary/steamapps/common/Crusader Kings III/game`.
- **Workshop mods** are listed as technique only. None is precedent, and nothing below copies from them.

**Method:**
- read the spec (amendment block, §2–§5, §10, Appendix B), the sim report and the sim model `docs/tools/sim/models/legacies.py`;
- read the v1 events, decision and modifiers in `OLD PROJECT VERSION/`;
- **re-ran the sim with variants.** The runner is `docs/tools/sim/whatif/legacies_variants.py`. It imports the repo model's readers unchanged and replaces only the yearly loop. It uses 20,000 sites × 100 years with seed 20261103, so its numbers compare directly with Appendix B. P0 reproduces the repo package within 0.1 pp.

---

## 0. Before the decisions: three sim findings that change the spec's numbers

The spec's Q8, Q9 and Q10 defaults rest on numbers that the model does not compute the way the spec designs the system. The direction of each default mostly holds, but the figures quoted to the owner are off:

| # | Model behaviour (`legacies.py`) | Spec design | Effect when corrected (variant run) |
|---|---|---|---|
| **S1** | The Extracted drain calls `change_integrity(s, …, y, [])` (`legacies.py:266`) with a throwaway queue, so **0104 never fires at a drain crossing**. | §3.3: the integrity writer fires 0104 at every crossing, from any writer. | With 0104 fired (run P0b): **Unstable falls from 17.8% to 7.6%**, Sealed rises from 26.3% to 34.6%, and 0104 runs 0.17 per site-century (0.00 before). The "Unstable at 18%" warning in Appendix B is an artefact of this. |
| **S2** | The floor is `if s.att > floor: s.att = max(floor, …)` (`legacies.py:243-245`), so **a site below 25 never decays at all.** Attention below the gate ratchets upward. | §3.1 1a: only a site marked `eotg_legacy_reached_rumoured` stops at 25. Every other site decays −2 a year to 0. | With the spec's marker semantics (P1), **0101 runs 0.11 per site-century, not 0.35–0.39** (Q10's quoted "0.61" uses the same model). Only **about 7% of known sites ever reach 25** after decay, and **0.4% reach 50**. |
| **S3** | The model is one site per holder and never creates a new one. The survey yield (0.20 new sites per survey that finds nothing) is reported only for **players**. | The v1 survey (`eotg_legacy_decisions.txt:10-100`) has `is_shown` for every landed count and an `ai_will_do` with base 15. **AI rulers survey too** (the model reads 6.9% a year) and hit the same fallback. | **Up to about 1.4 new sites per AI ruler-century,** an upper bound because `ai_potential` (gold ≥ 150, not at war) is not modelled. Across the galaxy that is far more than the 3 seeded per 100 counties (Q9 below). |

**Corrected package** (P1: 0105 on a dynasty change, drain −1, gate 25, floor 25 with the marker, 0104 fired at the crossing), AI holder, after 100 years:
- end state: **Governed 53.9%, Extracted 1.9%, Sealed 34.3%, Unstable 7.8%**;
- 16.9% of sites reach integrity 0, a median 69 years after discovery;
- events per site-century: aftermath 1.16; 0101 0.11; 0104 0.17; 0105 0.28.

**Sim fixes to hand to whoever owns `docs/tools/sim`** (I am read-only here):
1. queue and fire 0104 from the drain crossing;
2. model the marker floor;
3. optionally, add a galaxy-level seeding scenario for S3;
4. optionally, add non-death county transfers. Conquest is not modelled at all (see 0105).

---

## Q7. Is Legacies mod-exclusive, so it can be built on the temporary map before Gate 1?

**1. Question.** CLAUDE.md lets a system bypass the Gate 1 hold if it "must not depend on specific titles, provinces, characters, cultures or faiths, so they survive the map swap" (also `docs/agent_workflow.md:142`). After spec §4, does Legacies qualify?

**2. Vanilla comparables.** Vanilla builds site systems in two ways, and Legacies v2 deliberately takes the first:
- **Procedural, map-agnostic:**
  - epidemics roll `outbreak_chance` per province from a script value, with no named provinces (G `common/epidemics/00_epidemics.txt:176-193`; base value G `common/script_values/06_ce1_epidemics_values.txt:17,72`);
  - county state set inside `every_county` (G `common/scripted_effects/00_history_effects.txt:13-20`), the iterator spec §4.1 uses.
- **Hand-placed, map-bound:**
  - Mandala temple complexes seeded at game start by province id, some pre-ruined with `ruin_great_building = yes` and indexed into `mandala_poi_list` (G `common/on_action/game_start.txt:6233-6244`);
  - wanderer points of interest keyed to province ids (G `common/scripted_effects/00_wanderer_lifestyle_effects.txt:3-57`);
  - special-building POIs built from `every_special_building_province` (G `common/travel/point_of_interest_types/travel_point_of_interest_types.txt:189-194`).
- **Spec §4.1 already splits the two:** procedural seeding now, and the 7 v1 named capitals deferred to bookmark seeding after Gate 1. That is the vanilla split.

**3. Mod techniques (observational).** Every overhaul checked hand-places its ruins:
- Godherja: `ruined_district_01` with `can_construct_potential = { always = no }` and +30 `travel_danger`, plus a rebuild decision on a 5-year cooldown (`GH_ruin_buildings.txt:10-60`, `GH_ruin_rebuild_decisions.txt:17`);
- AGOT: `ruin_01` … `medium_ruin_*` holding buildings (`00_agot_ruin_buildings.txt:4-220`);
- LotR: `activity_explore_history` over named wonder buildings, on a 10-year cooldown (`lotr_explore_history.txt:283-416, 885`);
- TFE: great-project chains such as `TFE_hadrians_wall_01-03` (`TFE_great_project_buildings.txt:185-245`).

None of them could be tested before its map existed. A procedural design is the only kind that can be.

**4. Suggested answer: yes, mod-exclusive,** on four conditions, each checkable:
- (a) **No map keys** in any Legacies file. This must be empty:
  `grep -nE "title:|province:|culture:|faith:|character:|\b[ekdcb]_eotg_" common/*/eotg_legacy_* events/eotg_legacy_*`.
  The two faith-flavoured options read traits (`zealous`), not faiths (spec §4.3).
- (b) **Test bed:** the British Isles test sub-mod (`docs/test_submods/british_isles`), as for the governments, plus the V-L cases in the test harness. At 3% of about 3,430 vanilla counties that is roughly 100 sites, enough to exercise every path.
- (c) **The deferrals are recorded, not stubbed:** bookmark seeding of the 7 named sites (cartographer, after Gate 1) and the Exodus path (Q4).
- (d) **The Q9 cap ships with it** (below). A procedural system that grows without bound is the one thing the temporary map would hide, because on a small test map the runaway looks like density.

**5. Confidence: high.**
- The spec meets the stated criteria word for word.
- The precedents (cybernetics; the PMC/Corporation/Cartel/Gob-Corp exemption) are the same shape.
- The vault questions (Q2) do not block it: the modifier key `eotg_mod_legacy_planar_warded` is name-neutral, and loc defaults can ship and be re-worded.

**6. Changes:**
- CLAUDE.md, the "Work is done through agents" paragraph: add "**Grip Legacies** is also exempt (owner, <date>); tested on the British Isles test sub-mod; specced in `docs/specs/legacies_v2.md`."
- The `docs/agent_workflow.md` §6 gate board: Legacies, exempt.
- Taskboard CB-67: change the status to "ready to build".
- Spec header status line: "No game script … until the owner rules Q7" becomes "Q7 ruled yes (<date>)".
- Spec §9: add V-L24, the grep guard in (a).

---

## Q4. Exodus re-entry

**1. Question.** v1 had a passive discovery path: 10% a year for a ruler with `eotg_exodus_haven_reputation` who holds a hidden site (`OLD PROJECT VERSION/common/on_action/eotg_legacy_on_actions.txt:40-58`). Titan Exodus is not in v2. Drop the path now, or keep a stub, and how should it come back?

**2. Vanilla comparables.**
- **The producer calls the consumer's effect; the consumer does not poll.**
  - Pilgrimages create legend seeds by calling `create_legend_seed` from the pilgrimage's own effect (G `common/scripted_effects/00_pilgrimage_effects.txt:1384-1406`). The legend system never checks for pilgrims.
  - Natural disasters raise a catalyst in the dynastic-cycle situation from the disaster side (G `common/on_action/dynastic_cycle_on_actions.txt:155-171`).
- **Rate scale.** 10% a year sits between vanilla's per-attempt seed chances, `legend_seed_chance_low = 15` and `_very_low = 5` (G `common/script_values/06_ce1_legends_values.txt:15-18`). It is also above the AI survey rate the sim reads, 6.9% a year.

**3. Mod techniques.** None of the seven mods ties ruin discovery to a refugee or migration system. ATE's (disabled) salvage chain changes trouble odds by whether the site is in the explorer's realm and shares their faith: 30%, 50% or 75% trouble (`salvage_events.txt`, `salvage.10`). An outsider connection changes outcomes, not discovery.

**4. Suggested answer: drop now, with no stub (spec default), and re-enter with the dependency reversed.**
- When Titan Exodus is lifted, **the Exodus pulse calls Legacies, not the reverse.** In the Exodus's own yearly on_action, for a ruler with the haven modifier who `eotg_legacy_holds_hidden_site = yes`:
  `random = { chance = eotg_exodus_legacy_reveal_chance_value  random_held_county = { limit = { eotg_legacy_is_hidden_site = yes } eotg_legacy_fire_discovery_effect = yes } }`, with the value at **10**.
  - `eotg_legacy_fire_discovery_effect` is already a firing point that sets the 3-year site cooldown (spec §3.3), so cooldown authority is unchanged.
  - Legacies needs no reference to Exodus, and the system stays map- and system-agnostic.
- **Keep 10%.** It roughly doubles AI discovery for havens (6.9% to about 16% a year) and does nothing for players, who already find every hidden site in their first survey (Appendix B, B1).
- **Canon:** the Exodus began in 131 AG and is ongoing at 866 with no fixed end (`docs/lore/REVIEW_866.md:31,71`). The re-entry must not bring back v1's "wanes after 1000 AG".

**5. Confidence: high** for dropping it now (invariant 4: everything must be fired; a stub that reads a modifier which does not exist is dead code). **Medium** for the re-entry shape, which is Exodus's spec to own.

**6. Changes:**
- Spec §4.2, last bullet: change the taskboard note to "Exodus re-entry: Exodus's yearly pulse calls `eotg_legacy_fire_discovery_effect` (10%, `eotg_exodus_legacy_reveal_chance_value`) for a haven holding a hidden site; Legacies owns no Exodus code."
- Spec §10 Q4: add "dependency direction: Exodus → Legacies".
- Taskboard CB-67: replace the "re-add the Titan Exodus path" note with the same text.

---

## Q8. Integrity drain on Extracted sites

**1. Question.** v1 had no passive drain, so Extracted was a permanent +20% tax. The default is −1 a year on condition 4 only (`eotg_legacy_extracted_drain_value`). Is that the right rate and shape?

**2. Vanilla comparables.**
- **Artifact durability is the direct model.**
  - Decay is **1.0 a year** in storage or equipped, and **0.0 on display** or enshrined (G `common/defines/00_defines.txt:1577-1580`). Vanilla decays what is used and spares what is kept, the same split as Extracted against Governed and Sealed.
  - Maximum durability is 60, 75, 100 or 150 by rarity (`:1570-1573`), so an artifact in use lasts 60 to 150 years.
  - Thresholds fire warnings at 20 and 5 (`:1574-1575`; G `common/on_action/inventory_on_actions.txt:106-125`), and breaking at 0 has its own hook (`:45-51`).
  - An Antiquarian slows decay by 7% to 35% (G `common/court_positions/types/00_court_positions.txt:1137,1333-1345`).
- **Herder county fertility** is the depletion resource on counties, and it has a regrowth leg: growth and decline factors move toward an equilibrium (G `00_defines.txt:1066-1069`; `county_fertility_growth_add = 1` from a camp, G `common/buildings/00_nomad_buildings.txt:77-79`; nomad `county_fertility_decline_add = -15`, G `common/governments/00_government_types.txt:680`). Script changes come in steps of 5, 10, 20 or 30 (G `common/script_values/09_mpo_values.txt:754-761`).
- **Integrity 80 at −1 a year** gives an 80-year life, inside the 60–150 artifact band. The **median of 69 years** to 0 (option losses included) sits close to a common artifact's 60.

**3. Mod techniques.** No overhaul uses a numeric site stock. Depletion is modelled per attempt:
- ATE's salvage roll has a **10% "ruins collapse"** branch in every outcome table (`salvage.20`: 30/60/10 + 10 collapse, or 50/45/5 + 10 with a competitor);
- ATE Sci-Fi's salvage decision is 10 disaster / 20 accident / 50 nothing / 19 trinket / 1 firearm, behind 1,000 gold, an Antiquarian and a 5-year flag (`zzz_scifi_artifacts_decisions.txt:10-80`).

Legacies' stock plus drain is the more legible CK3 form: the player watches a number fall, as with artifact durability.

**4. Suggested answer: −1 a year on Extracted only, as specced.** Variant results (corrected model, AI holder):

| Drain | Reach 0 | Median years | Extracted at end | Unstable at end | 0104 per site-century |
|---|---|---|---|---|---|
| none (v1) | 0% | none | 10.9% | 0.6% | 0.00 |
| **−1 (default)** | **16.9%** | **69** | **1.9%** | **7.8%** | **0.17** |
| −0.5 | 0.4% | 79 | 17.9% | 1.7% | 0.00 |
| −1 only at integrity ≤ 50 | 5.6% | 49 | 13.0% | 3.4% | 0.06 |
| −2 (repo run) | 16.5% | 34 | 0.1% | 9.9%* | |

\* repo model; it does not fire 0104 at the drain crossing (S1).

- **−0.5 is v1 again:** almost no site ever ends.
- **"Only below 50"** keeps Extracted as a free bonus for about 30 years and halves the cost.
- **−1** matches the artifact rate and the pitch ("Exploit … site degradation"). The "Unstable 18%" concern in Appendix B disappears once 0104 is wired (S1). Most crossings resolve through 0104.a into Sealed.
- **No regrowth leg** (unlike fertility). Governed and Sealed already drain 0, which is vanilla's display rule, and 0104.a and 0104.c restore through the writer. Adding a regrowth leg would be a new mechanic, not a tuning value.

**5. Confidence: high.** The rate, the shape and the vanilla precedent agree, and the corrected numbers are better than the ones quoted to the owner.

**6. Changes:**
- Spec §10 Q8 and Appendix B: replace "Extracted ends at 1% … Unstable at 9%" and the package "Unstable 18%" with the corrected figures above. Delete the "if that is too high, drain only below 50" line, which is answered: rejected.
- Script: as specced. `eotg_legacy_extracted_drain_value = -1`, read in §3.1 step 1b.
- **Optional, new content, owner approval (spec §11):** an early warning at integrity 20, the vanilla `ARTIFACT_LOW_DURABILITY` pattern. A modifier description or tooltip costs nothing; a new event needs approval.

---

## Q9. Seeding density, and whether to halve the survey's own seeding

**1. Question.** Is `eotg_legacy_seed_chance_value = 3` (3% of counties) right, and should 0002.a's seeding branches (30 + 25 of 100) be halved so players accumulate fewer sites (about 4 per player-century)?

**2. Vanilla comparables.**
- **Density of "special place" content per county, vanilla map** (counted 2026-11-03; 3,430 county definitions in `G/common/landed_titles/`):
  - special buildings or slots in 234 provinces (`G/history/provinces/`), about **6.8%** of counties;
  - holy sites in 256 distinct counties (278 definitions, `G/common/religion/holy_site_types/`), about **7.5%**.

  At 3%, Legacies is under half of either. That fits canon's "only fragments" (EV:48).
- **Vanilla caps dynamic population with a global tally.**
  - Landless adventurers are counted in the global list `laamps_tally` (added at G `common/on_action/game_start.txt:6106-6110` and G `common/scripted_effects/07_dlc_ep3_scripted_effects.txt:673-676`, maintained at G `common/on_action/title_on_actions.txt:60-64` and `yearly_on_actions.txt:3370-3372`).
  - Creation is refused once `global_variable_list_size = { name = laamps_tally  value >= too_many_laamps_value }` (G `common/character_interactions/06_ep3_laamp_interactions.txt:1961-1964`).
  - The cap is a named value with a game-rule switch (G `common/script_values/07_ep3_values.txt:5304-5331`; rule G `common/game_rules/00_game_rules.txt:1558-1561`).
- **Per-character caps on seeding:** a pilgrimage drops a legend seed at most once per character (`has_character_flag = pilgrim_legend` / `add_character_flag`, G `00_pilgrimage_effects.txt:1376,1405`), at a 15% base (`:1384-1385`).
- **Tuning controls:**
  - epidemics use a named base (`outbreak_chance_base_low = 0.01`, % per province-year, G `06_ce1_epidemics_values.txt:17`), a frequency game rule (G `00_game_rules.txt:249-261`), and a recent-outbreak damper list (`06_ce1_epidemics_values.txt:1869-1893`);
  - legends do not spread without an owner (G `common/legends/legend_types/00_legends.txt:168-179`).

**3. Mod techniques.** No overhaul seeds ruins procedurally (Q7 §3). Rate limits there are decision cooldowns (5 years in Godherja, 10 in LotR) and steep costs (ATE Sci-Fi: 1,000 gold and an Antiquarian). There is no mod technique to copy for a density cap. Vanilla's tally is the model.

**4. Suggested answer: keep 3%; do not halve 0002.a; add a global cap instead.**
- **Keep `eotg_legacy_seed_chance_value = 3`.** It is below vanilla's special-place density and fits canon. 82% of seeded sites are found within 25 years by the AI; that pace is the decision cooldown, not the density.
- **Halving 0002.a's branches does almost nothing.** Computed from the script (`yield_calc.py`):

  | Change | New sites per empty survey | Per player-century | Per AI ruler-century (max) |
  |---|---|---|---|
  | as is | 0.203 | 4.07 | 1.40 |
  | 0002.a 30/25 → 15/12.5 | 0.193 (−5%) | 3.86 | 1.33 |
  | fallback 0002/0003 weights 40/20 → 20/10 | 0.145 | 2.90 | 1.00 |
  | every seeding branch at 50% | 0.102 | 2.03 | 0.70 |

  `random_list` weights renormalise. 0002.a's "unstable seam" branch (20) also seeds, 0002.b seeds at 70%, and 0003.e seeds at 40%. Halving two weights moves the yield 5%.
- **The real exposure is AI seeding, galaxy-wide (S3).** At up to 1.4 new sites per AI ruler-century, with 30% to 40% of counties under a surveying ruler, the galaxy gains up to **+40 to +55 sites per 100 counties per century**, against 3 seeded. Even at a quarter of that (`ai_potential` gold), density quadruples within a century. The MED-1 guard only stops seeding into counties that already have a site. That breaks "only fragments" and is the actual Q9 decision.
- **Cap, vanilla's laamp shape:**
  - `eotg_legacy_seed_effect` also does `add_to_global_variable_list = { name = eotg_legacy_site_list  target = this }`. It is the only writer of the list; v2 never destroys a site.
  - The game-start seeding loop (`every_county`, already present) counts counties once into the global variable `eotg_legacy_county_count` (`change_global_variable`, as at G `common/on_action/faction_on_actions.txt:26`).
  - `eotg_legacy_site_cap_value = { value = global_var:eotg_legacy_county_count  multiply = eotg_legacy_site_cap_share_value }`, with `eotg_legacy_site_cap_share_value = 0.06`. That is **6% of counties, 2× the start density**, about vanilla's special-building density.
  - A new trigger, `eotg_legacy_site_cap_reached = { global_variable_list_size = { name = eotg_legacy_site_list  value >= eotg_legacy_site_cap_value } }`.
  - In the survey's fallback `random_list`, the 0002 and 0003 entries get `modifier = { factor = 0  eotg_legacy_site_cap_reached = yes }`, so at the cap every empty survey is 0004 "Honest Geology". That uses the same `modifier` mechanism the spec already uses for MED-4.
- **Per-ruler restraint (recommended, optional):** the 0002/0003 entries also get `factor = 0` when the ruler already holds any site (`any_held_county = { eotg_legacy_is_site = yes }`). A ruler's survey can then create at most their first site. Further sites come by conquest, inheritance or game-start seeding. Player accumulation drops from about 4 per century to one per site-less ruler. This is the pilgrim-legend idea (one seed per character), keyed to "holds a site" so it stays a resource gate rather than a lifetime flag.
- **Later, not now:** a game rule `eotg_legacy_density` (1%, 3%, 5%, and caps of 2%, 6%, 10%), on the vanilla epidemic-frequency and laamp-number pattern. It needs loc and UI, so it can wait for the first playtest.

**5. Confidence: high** that halving 0002.a is ineffective (arithmetic from the script). **Medium-high** that the cap is needed; the AI rate is an upper bound, and the size of the gap makes the conclusion robust. **Medium** on the exact share (0.06); the owner's taste and playtests decide it.

**6. Changes:**
- Spec §10 Q9: replace the "cut 0002.a in half" sentence with the table above and the cap.
- Spec §6.1 and §6.2: new identifiers `eotg_legacy_site_list` (global list), `eotg_legacy_county_count` (global variable), `eotg_legacy_site_cap_value`, `eotg_legacy_site_cap_share_value` (0.06) and `eotg_legacy_site_cap_reached`.
- Spec §4.1: the seeding loop also counts counties.
- Spec §5.2 MED-1: the decision fallback gets the two `factor = 0` modifiers.
- Spec §9 tests:
  - V-L25: at the cap, 20 surveys produce only 0004;
  - V-L26: a ruler who holds a site never sees 0002 or 0003 seed.
- Appendix B, B5: "player" becomes "every surveying ruler, AI included" (S3).

---

## Q10. The rival-claim gate (0101)

**1. Question.** v1 gated 0101 at attention 50, which is never reached. The default is gate 25 plus a decay floor at 25 for sites that have reached 25, claimed to give 0.61 per site-century (0.35 in the package). Are those the right gate and floor?

**2. Vanilla comparables (attention and visibility).**
- **Legends hold a band and step down slowly.** An unmaintained legend loses one quality level only after **25 years** (G `common/defines/00_defines.txt:1825`). Spread needs an owner (G `00_legends.txt:168-179`); an unowned legend shrinks by at least 2 provinces a month (`00_defines.txt:1820-1821`).
- **Dread drifts toward a baseline, not to 0,** by 0.5 a month (G `00_defines.txt:122`). That is a floor.
- **Claims come from history, not from noise:** a house gains an artifact claim after holding the artifact 50 years (G `00_defines.txt:1581`).

Together these support a floor that holds once reached and is lost only by a deliberate act, which is the spec's marker design.

**3. Mod techniques.** ATE's salvage tables put a competitor's presence directly into the outcome odds (great finds 10% → 5%, poor 30% → 50%; `salvage.20`). Competition is a consequence of being noticed, not a background tax. There is no comparable rival-claim system in the other mods.

**4. Suggested answer: gate 25, floor 25, marker semantics as in the spec; accept the corrected rate.** Variant results (spec semantics, package otherwise):

| Variant | 0101 per site-century | Sites ever ≥ 25 / ≥ 50 |
|---|---|---|
| **gate 25, floor 25 (default)** | **0.11** | 6.9% / 0.4% |
| + decay −1 | 0.15 | 7.8% / 0.9% |
| + 0101 chance 25 → 40 | 0.12 | 7.1% / 0.4% |
| gate 20, floor 20 | 0.25 | 8.9% / 0.5% |
| gate 15, floor 15 | 0.59 | 7.0% / 0.5% |
| gate 50 (v1), floor 25 | 0.00 | |
| repo semantics (below 25 never decays) | 0.36 | |

- **Why 0.11 is right, not too low.** Only the loud choices reach 25 in one step: 0010.d monument +35, 0020.c mandate +35, 0021.c publish +20 stacked. About 7% of known sites get there, and those draw **about 1.5 rival claims per century each.** That is the pitch's rule ("most likely at *Contested* or *Renowned*"; "public acts and visible … raise Attention"): rivals follow publicity. Gate 15 would make rival claims a tax on quiet sites.
- **The levers that don't work:** a slower decay and a higher chance each add at most 0.04. The only real lever is the gate value. If the owner wants rival claims about twice as often, take **gate 20 / floor 20** (0.25), which is still tied to loud choices; in that case the band table should say "Rumoured 20–49".
- **The alternative design the repo sim actually measured** ("attention never decays below 25") gives 0.36. It is simpler to script, because it needs no marker variable. But low attention then only ratchets up, so a quietly sealed site keeps every point it ever gained and drifts toward a claim. That contradicts "Seal … lowers Attention" (pitch). Not recommended.
- **Consequence for the bands:** 0.4% of sites ever reach 50, so Contested and Renowned are effectively unreachable with the v1 amounts. Leave them in the spec as reserved; the owner may want an attention-raising event later (§11).

**5. Confidence: medium.** The mechanism is well supported; the "right" frequency is a taste call, and the variant table is the menu.

**6. Changes:**
- Spec §10 Q10 and Appendix B (B4 and the package bullet): replace "0.61 per site-century" and "0.35" with **0.11** (gate 25 + floor 25, marker semantics), and give the gate-20 option at 0.25.
- Spec §2.2: add "about 7% of known sites reach Rumoured; Contested and Renowned are reserved (≤ 0.4%)".
- Script: as specced. No value change unless the owner picks gate 20, in which case `eotg_legacy_rival_gate_value = 20` and `eotg_legacy_attention_floor_value = 20`. The band text in §2.2 moves with them.
- Sim: fix S2 so the model matches §3.1 1a.

---

## 0105 dynasty gate (NEW-5)

**1. Question.** `on_title_gain` fires on every inheritance, so v1's 0105 ran at every succession (2.6 per site-century) and its reseal option ratcheted sites into Sealed. Should 0105 fire only when the county leaves the dynasty, using `OR = { NOT = { exists = root.dynasty } NOT = { scope:previous_holder.dynasty ?= root.dynasty } }`?

**2. Vanilla comparables.**
- **Vanilla's own dynasty test, in the same hook:** herd carries over on a nomad title only `exists = root.dynasty` + `scope:previous_holder.dynasty ?= root.dynasty` (G `common/on_action/title_on_actions.txt:474-475`). The spec negates exactly this.
- **County arrangements survive succession and break on other transfers:** the `isolate_capital_decision_modifier` is removed unless `scope:transfer_type` is inheritance, abdication, appointment_succession or election (G `title_on_actions.txt:993-1006`). The transfer-type flags are listed at `:3-26`.
- **Hostile transfers get the penalty:** `COUNTY_CONTROL_LOSS_ON_HOSTILE_OWNER_CHANGE = 75` applies "due to conquest" only (G `00_defines.txt:1060`). Artifacts that follow a title are logged as `conquest` for conquest, usurpation, revocation or faction demand (G `title_on_actions.txt:1133-1140`).
- **Dedicated hooks exist:** `on_title_gain_inheritance` (`:3328`) and `on_title_gain_usurpation` (`:3406`).

**3. Mod techniques.** None of the mods has a site-transfer event to compare. Godherja's and AGOT's ruins are buildings, and buildings carry no holder memory.

**4. Suggested answer: adopt the dynasty gate as specced.** Corrected variants:

| 0105 gate | 0105 per site-century | Sealed | Governed |
|---|---|---|---|
| none (every succession, v1) | 2.54 | 67.5% | 25.9% |
| **dynasty change (default)** | **0.28** | **34.3%** | **53.9%** |
| dynasty change + 1%/yr conquest-type transfers (assumed) | 1.01 | 47.5% | 42.6% |

- **Why the dynasty form and not `scope:transfer_type`:** the dynasty test catches inheritance out of the dynasty (elective, matrilineal, a lowborn heir), which the transfer-type test misses. Nearly every conquest is already a dynasty change. Adding `transfer_type` conquest flags only adds the rare same-dynasty conquest.
- **Note the remaining driver.** Sealed at 34% (not the 26% quoted) comes partly from 0104.a "stabilize", which writes Sealed (S1). The model has **no conquest**, so in a warring galaxy Sealed will sit nearer 45% (third row, at an assumed 1% a year). The ratchet is 0105.c "reseal" (Sealed is left only through 0104.c). If the owner wants Sealed lower, that is an option change, not a gate change: for example, 0105.c is not offered for a Governed site, or its AI weight drops from 30 to 15. Raise it with the owner separately; it is out of scope for this decision.

**5. Confidence: high** for the gate (a verbatim vanilla test, safe for lowborn holders per the amendment). **Medium** on the end-state shares, because conquest is not modelled.

**6. Changes:**
- Spec §5.2 NEW-5 and Appendix B (B2 and the package): Sealed **34%** and Governed **54%** with 0104 wired. Add one line: "conquest is not modelled; at 1%/yr transfers Sealed ≈ 48%".
- Script: as specced (§3.2).
- Optional, owner: the 0105.c ratchet note above, added to §10 as Q11.

---

## Q2. Names and vault (noted; canon, not answered here)

- **Defaults stand pending the vault:**
  - player-facing "Grip Legacies"; "Confluence" is never reintroduced (collides with the Confluence Accord, NA:1490);
  - the fourth family is "Hellshard", "a shard of one of the hells the Grip dragged the worlds through" (EV:20-21, EV:49-50).
- **Vault questions:**
  - (a) any source for "the Confluence";
  - (b) the fourth family's name: Hellshard, Limbo Pocket or Planar Pocket;
  - (c) can a hell keep an administration (0040).
- **The ERAS errata** (Grip at 0 AG; Second Era before it, `REVIEW_866.md:90-95`) waits on the human.
- **None of these blocks Q7.** Script keys are name-neutral (`eotg_mod_legacy_planar_warded`), and Appendix A's loc can ship with the defaults.

---

## Appendix: variant runs (reproducible)

`python docs/tools/sim/whatif/legacies_variants.py 20000` (main table) and `… 20000 q10` (Q10 table). It imports `docs/tools/sim/models/legacies.py` read-only (seed 20261103, AI holder unless noted).

| Run | Governed | Extracted | Sealed | Unstable | Reach 0 (median y) | Aftermath per site-century | 0101 | 0104 | 0105 |
|---|---|---|---|---|---|---|---|---|---|
| P0 repo package (reproduces Appendix B) | 54.0% | 1.8% | 26.3% | 17.8% | 16.9% (69) | 1.13 | 0.36 | 0.00 | 0.27 |
| P0b P0 + 0104 at the drain crossing | 54.0% | 1.8% | 34.6% | 7.6% | 16.9% (69) | 1.33 | 0.39 | 0.17 | 0.27 |
| **P1 spec package (marker floor + 0104)** | **53.9%** | **1.9%** | **34.3%** | **7.8%** | **16.9% (69)** | **1.16** | **0.11** | **0.17** | **0.28** |
| P2 P1, floor skips Sealed | 53.6% | 1.8% | 34.6% | 7.8% | 17.2% (69) | 1.19 | 0.11 | 0.17 | 0.28 |
| P3 P1, drain only at ≤ 50 | 54.1% | 13.0% | 28.8% | 3.4% | 5.6% (49) | 1.20 | 0.11 | 0.06 | 0.27 |
| P4 P1, drain −0.5 | 54.3% | 17.9% | 26.0% | 1.7% | 0.4% (79) | 1.24 | 0.11 | 0.00 | 0.27 |
| P5 P1 + 1%/yr conquest-type transfers | 42.6% | 1.7% | 47.5% | 6.4% | 15.2% (69) | 1.21 | 0.12 | 0.15 | 1.01 |
| P6 P1, 0105 at every succession | 25.9% | 1.1% | 67.5% | 4.2% | 12.1% (59) | 1.25 | 0.12 | 0.12 | 2.54 |
| P7 P1, gate 50 | 53.8% | 1.8% | 34.5% | 7.6% | 17.1% (69) | 1.06 | 0.00 | 0.17 | 0.28 |
| P8 P1, player holder | 53.1% | 0.0% | 36.5% | 8.0% | 18.9% (69) | 1.33 | 0.12 | 0.19 | 0.32 |

**Limits:**
- Peak attention is measured after the year's decay step.
- The 0104 crossing in the runner does not set the spec's 3-year site cooldown (minor).
- AI survey uptake ignores `ai_potential` (gold ≥ 150, not at war), so the S3 figures are upper bounds.
- P5's 1%/yr transfer rate is an assumption, not a measurement.
