# A. PMC and Cartel owner decisions: comparables and suggested answers (2026-11-03)

`G/` = `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/` (1.20.1.1). Mod paths are repo-relative. Workshop mods are cited **observationally**: technique only, never precedent. A scan of all seven (`common/governments`, `script_values`, `scripted_effects`, `decisions`; grep `reputation|notoriety|infamy`) found **no reputation-style resource and no per-liege contribution cap** in any of them. The only hits were vanilla-copied fp3 files.

Shared vanilla facts used below:
- **`medium_gold_value`** is 6 months of income. It is ×0.25 for a landed non-top ruler with a treasury, has a floor of 50 and a cap of 300 × the era multiplier (0.75 to 3), and is rounded to 5 (`G/common/script_values/01_dynamic_values.txt:93-111`; `00_basic_values.txt:82-113`).
- **LAAMP contract pay** is `50 × employer-tier multiplier`: ×0.5 for a courtier, ×1 for a baron or count, ×3 for a duke, ×4 for a king or emperor (`07_ep3_values.txt:2563-2579, 2697-2735`; the tiers are `00_defines.txt:1838-1840`). Its floor is `min = 25` (`:2735`). The prestige reward is 150 × 1 / 2.5 / 3.5 (`:2592-2613`), and a failure costs −25 × the same multipliers (`:2645-2648`).

---

## PMC OQ1. Standing as a scripted 0–100 variable?
1. **Question.** Keep `eotg_pmc_standing` as a scripted character variable rather than an engine currency?
2. **Vanilla.**
   - Every engine currency is either universal (prestige, piety, dread) or tied to a DLC government flag. For example, influence is gated by `government_has_flag = government_has_influence` (`G/common/on_action/death.txt:1416`).
   - Vanilla shows bespoke meters through a story `basic_counter` (`_story_cycles.info`; `book_translation_story_cycle.txt`), which the mod already copies.
3. **Mods (observational).** None has a custom reputation currency. Godherja's pirate government reuses an engine rule instead (`regiments_prestige_as_gold = yes`, also vanilla at `00_government_types.txt:190`).
4. **Suggested answer: yes.** It is already built and QA'd, and no engine currency means "market reputation".
5. **Confidence:** high.
6. **Script change:** none.

## PMC OQ2. Inheritance share
1. **Question.** What share of standing passes to the primary heir: 75%, 100% or 50%?
2. **Vanilla.**
   - Legitimacy passes at 25%, and only when the heir moves up a tier (`00_defines.txt:316`).
   - Admin influence passes at **20%** by default, rising to 30/40/50% with estate bonuses, and only to a same-house heir (`death.txt:1413-1447`; the bonuses are `07_ep3_values.txt:515-517`).
   - Dynasty renown is held by the dynasty, so it carries over at 100% (`00_defines.txt:1099-1103`).
   - Heir-succession tributary groups keep the whole relationship (`subject_contract_groups.txt:163-164, 192-193`).
   - **The vanilla rule:** personal capital passes at 20–50%; capital that belongs to an institution passes whole.
3. **Mods (observational).** Nothing comparable found.
4. **Suggested answer: keep 75%,** as `max(own, 0.75 × predecessor)`.
   - Standing is the company's name, so it sits on the institutional side of the vanilla rule, but it is still held by one person, so not 100%.
   - 75% matches the Gob-Corp (`eotg_gobcorp_values.txt:53`). The Corporation's 50% (`eotg_corporation_values.txt:53`) suits a personal hold on a board.
   - Under the current drift, a predecessor at 100 leaves 75, which is above the drift threshold of 60, so the name survives one death without being frozen at the cap.
5. **Confidence:** med-high.
6. **Script change:** none (`common/script_values/eotg_pmc_values.txt:51-56` stays `multiply = 0.75`).

## PMC OQ3. Recruit on Reputation sink
1. **Question.** Ship the third decision, which spends 20 standing for a generated Operator every 5 years?
2. **Vanilla.**
   - `recruit_terrain_specialist_decision` costs `minor_gold_value` plus `medium_prestige_value` (150), has a **5-year** cooldown, and creates one skilled fighter. The AI may use it (`00_cultural_tradition_decisions.txt:2, 132-141, 512`). This is the closest analogue.
   - `invite_knights_decision` costs 150 prestige, has a 10-year cooldown, brings 3 knights, and is turned off for the AI (`00_guest_decisions.txt:31, 58, 91-93, 113-114`; `00_decision_values.txt:107-108`).
   - `borrow_from_holy_order_decision` spends 50 piety to draw on a force, on a 15-year cooldown (`00_holy_order_decisions.txt:276, 300, 303`).
   - The engine already generates commanders: vanilla `mercenary_government` sets 5 (`00_government_types.txt:326-335`), and the PMC sets 2 (`eotg_pmc_government.txt:51`).
3. **Mods (observational).** Godherja's `military_unit_government` relies on `court_generate_commanders = 5` alone, with no buy-a-knight verb.
4. **Suggested answer: yes, unchanged** (−20, 5 years, AI reserve 40).
   - Cadence and output match the vanilla specialist decision: one fighter every 5 years.
   - It is the only chosen sink. The sim shows the AI uses it at 0.017–0.054 a year, so it keeps standing a currency rather than a score.
   - Keep the AI on: unlike vanilla's knight invite, the AI's standing economy needs a sink.
5. **Confidence:** high.
6. **Script change:** none.

## PMC OQ4. A visible story
1. **Question.** Make the standing story visible, or show only the modifier?
2. **Vanilla.** The story `visualization` / `basic_counter` fields are documented in `_story_cycles.info` and used by `book_translation_story_cycle.txt` (already cited in CLAUDE.md).
3. **Mods (observational).** Not surveyed.
4. **Suggested answer: visible.** This keeps parity with the Cartel ruling of 2026-10-20 (OQ3 there). A scripted variable has no engine UI, so the story counter is the only place standing can be read.
5. **Confidence:** high.
6. **Script change:** none.

## PMC OQ5. Start values 40 (top) and 20 (vassal)
1. **Question.** Approve the starting standing?
2. **Vanilla.** A new government gets a fixed lump of its own resource, not a conversion: feudal → admin grants monumental influence (`00_ep3_decision_effects.txt:196`; `07_ep3_values.txt:5623-5634`). Dread starts at 0 (`00_defines.txt:121`).
3. **Mods (observational).** None.
4. **Suggested answer: keep 40 / 20.**
   - The sim's AI tops settle at 29.5 / 37.7 / 46.2 / 59.8 (1 / 4 / 8 / 16 vassals), so 40 sits inside that band, and an AI top settles within about 1 to 28 years.
   - Vassals settle at a median of 34–35, so starting at 20 leaves them room to earn standing.
   - 40 is also the AI's Recruit reserve, so a new company does not spend at once.
   - This matches the Gob-Corp (40/20). The Corporation uses 50/20.
5. **Confidence:** high.
6. **Script change:** none (`eotg_pmc_values.txt:38-44`).

## PMC OQ6. First-pass numbers
1. **Question.** Approve the §2.5 / OQ6 numbers?
2. **Vanilla.** See P2 and P6 below for the two numbers the sim questioned. Battle results and drift have no vanilla equivalent (scripted standing only).
3. **Mods (observational).** None.
4. **Suggested answer: approve all, except** contract pay (take P6, below) and the liege share (take the P2 cap and keep +5, below).
   - Battles +2 / −3, drift −2 above 60, Deliver +15, Recruit −20 and the 3- and 5-year cooldowns all hold in the sim, with no dead or pinned states for the AI.
   - The exit (×4, max 400) loop nets at most +50 prestige per 10 years (sim L5), so it is not a farm.
   - The +1 prestige a month at 100 standing is modest.
5. **Confidence:** med.
6. **Script change:** only via P2 and P6.

## PMC OQ7. AI adoption of the PMC
1. **Question.** May the AI take "Run the Realm as a Company"?
2. **Vanilla.**
   - **Mandala:** `ai_potential` restricts feudal and clan rulers to `primary_title.tier <= tier_duchy`; `ai_will_do` is base 20, −15 if not tribal (net 5); it is checked every 36 months (`tgp_east_asia_decisions.txt:64-71, 194-219, 237-241`).
   - **Admin:** base 0, with +50 for each fitting culture ethos or tradition (`06_ep3_admin_decisions.txt:1223-1260`).
   - **Whole-realm feudalism:** hard `is_valid` gates, then base 100 (`80_major_decisions.txt:364-371, 457-463`).
   - **Follow-the-liege conversions:** cost 150 prestige; the AI needs prestige ≥ 150 and takes it at base 0, +100 if its opinion of the liege is ≥ 0 (`80_major_decisions.txt:165-252`).
   - **The vanilla pattern:** rarity comes from narrow eligibility and a low base weight on a long interval.
3. **Mods (observational).**
   - After the End's Sci-Fi submod steers AI behaviour through government `character_modifier` (`ai_war_chance = 2`, `ai_war_cooldown = -0.5`), not through adoption decisions.
   - The Fallen Eagle's legion is vassal-only through `can_get_government = { is_independent_ruler = no }`.
4. **Suggested answer: not yet** (keep `ai_potential = { always = no }`), the same as the Cartel, until V-G11 (leakage) has run. When it opens, use the mandala shape:
   - `ai_potential`: independent; `primary_title.tier <= tier_duchy`; `martial >= 14`; `prestige >= 200`; not at war.
   - `ai_will_do`: base 5, +10 if `martial >= 16`, +10 if `number_of_knights >= max_number_of_knights`.
   - `ai_check_interval_by_tier`: county 120, duchy 120, everything else 0.
   - A "follow the liege" decision for PMC vassals is a separate, later item.
5. **Confidence:** high for "not yet"; low for the numbers.
6. **Script change:** none now. Later: `common/decisions/eotg_pmc_decisions.txt`, the `eotg_decision_pmc_adopt` `ai_potential`, `ai_will_do` and `ai_check_interval_by_tier`.

## PMC OQ8. PMC → Corporation evolution
1. **Question.** Build a decision that turns a PMC into a Corporation and converts standing into Board Influence?
2. **Vanilla.**
   - Feudal → admin does not convert prestige. It grants a fixed lump of the new resource (monumental influence) and offers vassals the switch (`00_ep3_decision_effects.txt:180-204`; `07_ep3_values.txt:5623-5634`).
   - Tribal → feudal costs 200 prestige and converts vassals (`80_major_decisions.txt:348-471`).
   - **The vanilla pattern:** pay in the old currency, start the new one at a set value, and handle vassals explicitly.
3. **Mods (observational).** A Game of Thrones models sellsword companies as landless titles (`05_agot_laamps_merc.txt`: `landless = yes`, `destroy_if_invalid_heir = yes`) that ride vanilla contracts. There is no evolution path in any of the mods.
4. **Suggested answer: defer the build** until the in-game PMC and Corporation checks (V-P*, V-CO*) pass. Both resources now exist, so the original blocker is gone. Fix the shape now so it does not drift:
   - **Name:** "Incorporate", a top-tier decision.
   - **`is_valid`:** standing ≥ 60; no `changed_government_recently`; not at war; not under contract.
   - **`cost`:** prestige 200.
   - **`effect`:** set Board Influence through the Corporation change effect to `20 + 0.5 × standing` (60 → 50, the Corporation's own top start; 100 → 70); zero standing through the PMC change effect; convert PMC vassals; set `changed_government_recently` for 5 years.
   - **AI:** `always = no`.
   - It needs a lore-keeper check before it is built.
5. **Confidence:** med for "defer"; low for the numbers.
6. **Script change:** none now. Later: a new decision in `common/decisions/eotg_pmc_decisions.txt` and a value `eotg_pmc_incorporate_influence_value` in `eotg_pmc_values.txt`.

## PMC OQ9. The §11 events (E1–E5)
1. **Question.** Approve any of the proposed events?
2. **Vanilla.** LAAMP contracts have a failure branch: −25 prestige × the tier multiplier, ×2 on a critical failure (`07_ep3_values.txt:2645-2652`). The PMC's Take a Contract cannot fail.
3. **Mods (observational).** None.
4. **Suggested answer: none now** (owner's rule). When the G2 in-game checks are done, approve **E1 "The Client Won't Pay" first**. It is the only proposal that gives the core verb a failure branch the way vanilla contracts have one. Keep E2–E5 parked.
5. **Confidence:** low to med (an owner taste call).
6. **Script change:** none now.

---

## P2. Deliver Results liege share: +5 → +2, a once-a-year cap, or both?
1. **Question.** How should Standing's scaling with vassal count be tamed?
2. **Vanilla.**
   - Vanilla **caps the aggregate** instead of shrinking each contribution. Dynasty prestige is 0.02 a month per member with a hard cap of 2 a month (`00_defines.txt:1100-1101`), and vassals of the same dynasty contribute 0 (`:1103`).
   - Per-target cadence is a first-class field on interactions: `cooldown_against_recipient` (`_character_interactions.info:222`), e.g. 3 years on `hire_laamp_mercenaries_interaction` (`06_ep3_laamp_interactions.txt:5399`).
   - Size-dependent costs use √(realm size) (`00_defines.txt:1287`, `REALM_SIZE_MULT`).
3. **Mods (observational).** None has a per-liege cap. The mod's own shipped caps are the internal precedent: `eotg_corp_board_eroded` (`common/decisions/eotg_corporation_decisions.txt:156, 163-167`) and `eotg_gobcorp_cornered` (`eotg_gobcorp_decisions.txt:76-81`), both 1-year variables on the liege.
4. **Suggested answer: the cap only, keeping +5.**
   - The AI case does not need a value cut: 16 AI vassals settle at 59.8, inside the spec's design band of 40–70 (§2.5).
   - P2 also trims the 1-vassal realm (29.5 → 27.7).
   - The cap is scale-free and affects nothing at 1 vassal. It bites only under the stress bound (years at 100: 77.8% → 57.0%), and it makes the PMC the third government with the same once-a-year shape.
   - Don't do both.
   - Optional parity follow-up: the Cartel's Lean on the Locals also gives an uncapped +5 to the liege. Engine dread decay softens it, so it is lower priority.
5. **Confidence:** med-high.
6. **Script change:** `common/decisions/eotg_pmc_decisions.txt:141-151`.
   - Add `NOT = { has_variable = eotg_pmc_results_received }` to the `liege ?=` limit.
   - Inside the liege block, add `set_variable = { name = eotg_pmc_results_received years = 1 }`.
   - Keep `eotg_pmc_deliver_liege_value = 5` (`eotg_pmc_values.txt:78`). Drop the P2 hunk from `proposed_tuning.patch`.
   - Loc: the `_liege_tt` text is unchanged; optionally add "(once a year)".

## P6. Take a Contract pay
1. **Question.** Replace the flat `50 + 3 × standing` (the same at every tier) with pay scaled by realm size?
2. **Vanilla.**
   - LAAMP contract pay scales by the employer's tier: 50 × 1 / 3 / 4 for a count / duke / king (`07_ep3_values.txt:2563-2579, 2697-2735`).
   - LAAMP mercenary hire is priced at the seller's `current_military_strength / 10`, with a floor of the buyer's `minor_gold_value` (`:996-999`). The war payment's floor is the employer's `medium_gold_value` (`:1027-1030`).
   - `medium_gold_value` is 6 months of income, with a floor of 50 (`00_basic_values.txt:82`).
   - **The flat formula is off in both directions.** At standing 50, 200 gold every 3 years roughly doubles a count's income, but it is trivial for a king.
3. **Mods (observational).** A Game of Thrones pays its sellswords through vanilla task contracts, so it inherits the employer-tier scaling.
4. **Suggested answer: take P6 as patched, adding a floor:** `(standing / 50 + 0.5) × medium_gold_value`, `min = 50`. That is 0.5–2.5× medium gold, and never less than today's pay at standing 0.
   - **Count** at the floor: 50 / 75 / 125 at standing 0 / 50 / 100.
   - **Duke** (about 10 gold a month): 50 / 90 / 150.
   - **King** (about 30 gold a month): 90 / 270 / 450.
   - These sit in LAAMP's count and king band (50–200 before era scaling).
   - Verify in game with the report's P6 check (a county PMC against a kingdom PMC).
5. **Confidence:** med (not simulated).
6. **Script change:** `common/script_values/eotg_pmc_values.txt:69-73` → `value = eotg_pmc_standing_value  divide = 50  add = 0.5  multiply = medium_gold_value  min = 50`. Loc: the patch's `eotg_decision_pmc_take_contract_desc` line (`proposed_tuning.patch:161-162`).

## P5. Cartel succession grace, 3 → 5 years
1. **Question.** Should the heir's protection from payer walk-offs last 3 or 5 years?
2. **Vanilla.**
   - Dread is personal: it starts at 0 (`BASE_DREAD`) and drifts 0.5 a month toward the baseline (`00_defines.txt:120-122`). With the mod's −0.25 decay multiplier, that is 0.375 a month.
   - Vanilla treats the first **10 years** of a reign as fragile (`SHORT_REIGN_YEARS = 10`, `:486-488`).
   - Vanilla protects tribute with a timed variable on the same shape. Mandala `tributary_can_break_free` is gated by `NOT = { has_variable = tributary_has_been_reasserted_recently }` (`subject_contract_groups.txt:224-228`), set for 12 months (`00_tributary_interactions.txt:5667-5669`; `tgp_mandala_values.txt:64`).
3. **Mods (observational).** None found.
4. **Suggested answer: take it (5 years).**
   - From 0 at 0.375 a month, an heir needs about 53 months to reach `low_dread` 20, so 3 years ends before the climb can finish.
   - The sim halves walk-offs (0.436 → 0.218 with 4 vassals; 0.146 → 0.043 with 16), and dread equilibria are unchanged.
   - 5 years is still half of vanilla's short-reign window.
   - Don't add dread inheritance: dread is engine-personal, and that change is E4's job if E4 is ever approved.
5. **Confidence:** high.
6. **Script change:** `common/on_action/eotg_cartel_on_actions.txt:111` `years = 3` → `years = 5`. Update the "3 years" text in the spec comment at `:95-96`, in `docs/specs/governments_v2_g2_cartel.md` §2.2/§6.3, and in the story `_info` loc line (`proposed_tuning.patch:113-114`).

---

## Summary
1. OQ1: keep standing as a scripted 0–100 variable (high).
2. OQ2: keep 75% inheritance, `max(own, 0.75 × predecessor)`, between vanilla influence's 20–50% and renown's 100% (med-high).
3. OQ3: ship Recruit unchanged (−20, 5 years, AI reserve 40); vanilla's specialist recruit is the same cadence (high).
4. OQ4 and OQ5: visible story; starts 40/20 (high).
5. OQ6: approve all first-pass numbers except contract pay (P6) and the liege share (P2-cap) (med).
6. OQ7: AI adoption stays off until V-G11; later, the mandala shape at tier ≤ duchy, base 5, 120-month interval (high / low).
7. OQ8: defer "Incorporate"; fix its shape now: standing ≥ 60, 200 prestige, influence = 20 + 0.5 × standing (med / low).
8. OQ9: no events now; approve E1 first later (low-med).
9. P2: once-a-year liege cap only, keep +5; no value cut (med-high). P6: `(S/50 + 0.5) × medium_gold_value`, `min = 50` (med).
10. P5: Cartel grace 3 → 5 years (high).
