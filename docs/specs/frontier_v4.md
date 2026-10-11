# Spec: Frontier Systems v4 (amendment: QA rulings A1–A11, Frontier + Unsworn / Unclaimed Regions)

**Author:** eotg-architect, 2026-10-11. **Status:** ruled, not built. The human approved the dispatch on 2026-10-11.
**Amends:** [`frontier_v1.md`](frontier_v1.md), [`frontier_v2.md`](frontier_v2.md), [`frontier_v3.md`](frontier_v3.md), [`frontier_unclaimed_regions.md`](frontier_unclaimed_regions.md) (its §D owner decisions still bind), and one line of [`governments_v2.md`](governments_v2.md). Where this spec and an amended spec disagree, **this spec wins**. Each amended spec carries a pointer back here.
**Input:** [`docs/qa/frontier_unsworn_architect_brief.md`](../qa/frontier_unsworn_architect_brief.md) (cited as *brief Ax*); evidence in [`docs/qa/frontier_unsworn_qa.md`](../qa/frontier_unsworn_qa.md); the government assessment [`docs/qa/government_assessment_2026-10-11/shared_infra.md`](../qa/government_assessment_2026-10-11/shared_infra.md) (B1, G3), [`government_template.md`](government_template.md) §6.2. Intent: [`docs/design/frontier_systems.md`](../design/frontier_systems.md) (read-only; cited as *design §n*).
**Vanilla:** CK3 **1.20.0.4**, `G` = `D:/SteamLibrary/steamapps/common/Crusader Kings III/game`. I re-checked every vanilla line cited below in this session. Line numbers the brief took from `0abde1d` were re-checked too and still hold.

---

## 0. Rulings at a glance

| # | Ruling | Batch | Gated on |
|---|---|---|---|
| A1 | A completed city or church System goes to a **new local vassal** (the settlers' leader, a factor, or the mission elder) under the holder. The holder keeps it only if their own seat is the same holding type. Castles stay with the holder. | 2 | V8 (DoD only; the rule is written to be correct either way) |
| A2 | AI: Establish every 24 months at a 25–50 base weight with a 1× gold gate; the map cap scales with Unclaimed space (8 + 1 per 20, max 24); an AI claim needs gold for claim + Establish and no claimed county still waiting; AI Frontiers get silent strain/progress rolls; AI exploring of claimed Unknown space is sped up. The AI-only lapse (UD3) is a **human question** (it reopens owner default UQ11). | 1 | V-U14 decides whether AI claims happen at all (fallback in §A7.3) |
| A3 | One flavour roll per ruler per pulse; flavour events fire 1–120 days later. "Funding removes the story" is **accepted**. | 1 | none |
| A4 | War strain only when the holder leads a war or hostile armies stand in the Region. A new **Appoint a Founder** decision. The AI auto-founder must be an adult, free character. | 1 | none |
| A5 | **The spec order stands** (d; else b if gold ≥ 2× minor; else a). The AI never picks c. The code moves to it. §6.6(c) is corrected to "switches to Settlement" (code wins). | 1 | none |
| A6 | M2 = key-level override of `basic_is_valid_for_yearly_events_trigger` only. M3 = a GAME_OVER entry through a key-level override of the scripted rule `is_character_allowed_to_be_player`. A real **pulse probe** replaces the current V-U1 readout, which can't answer the question. | probe: 1; M2/M3: 3 | V-U1a (probe), V-U1b + T14 |
| A7 | The release effect enforces the capital rule itself. Claim and placeholder replacement move every barony the old placeholder held, and the sweep dissolves enclaves. A **Raise Your Colours** decision is added, sharing one cooldown variable with the interaction. `eotg_unclaimed_defender_tt` is built inside the override, mirroring vanilla's herder line. | 1 (7.1–7.2), 2 (7.3–7.4) | V-U9/V-U8/V-U15 (DoD) |
| A8 | Qualitative bands (pace, time left, strain, and what weighs on it) in the Invest, Build and Abandon tooltips. Sponsor input 6 → **8** pre-pace. The sponsor gets a completion reward (prestige plus the holder's goodwill). | 2 | none |
| A9 | Frontier says **"strain"**, never "pressure"; "Frontier Legacy" → **"Frontier Roots"**. Recommendation only; ownership of "pressure" goes to the lore-keeper. | loc | needs-lore |
| A10 | **Coupling accepted and recorded** (`frontier_unclaimed_regions.md` §21). New Frontier → Unclaimed reads go through variables only (a soft seam). | docs (done here) | none |
| A11 | Abandon's −1 development applies only when this attempt granted development, and the grant can be re-earned. The holy-order variable is approved with `?=` fall-through. Escort and garrison each take −5 off .034's weight. | 1 | none |
| — | Option depth: `stress_impact` rows on 6 existing options, plus `duel` rolls on .032.c and .033.c | 4 | none (coordinate with event_quality B12) |

---

## 1. Purpose & gate

This amendment fixes what the 2026-10-11 QA found in Frontier Systems and the Unsworn / Unclaimed Regions layer. Nothing here is a new system:
- dead completion holdings;
- near-inert AI;
- event bursts;
- blunt war strain;
- the founder gap;
- AI-order drift;
- unbuilt playability mitigations;
- release and claim edge cases;
- legibility;
- vocabulary;
- coupling.

**Gate 3 (Systems)**, built under the **mod-exclusive exemption** (CLAUDE.md, decided 2026-10-02; Unclaimed is a Frontier sub-system, `frontier_unclaimed_regions.md` §1). **Not blocked by Gate 1.** Everything stays map-agnostic.

Batches 1, 2 and 4 can be built now. Batch 3 (A6) is **conditional**: it is fully specified so it can be built the day V-U1 and T14 report.

## 2. Signature resource

Unchanged:
- **Frontier:** `eotg_frontier_progress` (hidden, 0–100; county variable). Its pressure value `eotg_frontier_strain` (hidden, 0–8) is read and moved alongside it.
- **Unclaimed:** `eotg_unclaimed_county` (`frontier_unclaimed_regions.md` §2).

**How v4 touches them:**
- **No new events.** Every existing flavour event still moves or reads progress or strain (invariant 5; QA verified 19/19).
- **The AI silent roll** (A2.4) moves progress or strain in every branch. It is not an event, but it follows the same rule.
- **The legibility bands** (A8) read progress and strain and print words only. The hidden-value rule of `frontier_v1.md` §R ("players see consequences, never numbers") binds every key in §7.
- **The decision and the release guard** (A7) set or read `eotg_unclaimed_county` through the existing effects only.

---

## 3. Rulings

### A1. Settled city and church Systems: a local vassal holds them

**Ruling (option 1, refined).** When a completion creates a **city** (Settlement, Trade) or **church** (Religious) System, it goes to a **local character as the holder's vassal**, unless the holder's own capital barony is already that holding type. Castles (Military) always go to the holder.

**Why this test.** No vanilla trigger asks "may this government hold holding type X": no `valid_holdings` reader exists in script, and I grepped `G/common` and `G/events`. The capital test is the government-agnostic proxy:
- a ruler seated in a city (vanilla republic, the mod's Corporation and Gob-Corp, which are city-primary: `eotg_corporation_government.txt:38`) keeps a Port;
- a ruler seated in a temple (theocracy) keeps a Sanctum;
- everyone else (feudal, clan, Cartel, PMC: castle-primary; `G/common/governments/00_government_types.txt:18-19`, `eotg_cartel_government.txt:49-50`, `eotg_pmc_government.txt:37-38`) gets a vassal.

Castles are valid for every settled government the mod uses, so Military is unchanged.

**Vanilla precedent:**
- **A city given to a character as a vassal, with a republic government:** `G/events/activities/hold_court_activity/hold_court_events_joe.txt:507-521` (hold_court.8300.a: `change_government = republic_government`, `create_title_and_vassal_change { type = granted }`, `change_title_holder` on `province.barony`, resolve). Also `G/events/activities/hold_court_activity/hold_court_events_general.txt:6912-6945` (hold_court.6060.b: `set_holding_type = city_holding`, then the barony is granted to a character).
- **A church held by a created priest, with a theocracy government:** `hold_court_events_joe.txt:1224` (`priest_character_template`, `dynasty = none`, culture/faith/rite from the county by scope) and `:1240-1260` (granted, then `change_government = theocracy_government` after the resolve).
- **Vanilla's own shape** is cities and temples held by vassals: feudal's `required_county_holdings = { castle_holding city_holding church_holding }` (`00_government_types.txt:20`), with the city and church baronies normally held by vassals.

**Who the local ruler is** (no new template):

| Type | Local ruler | Already created today? |
|---|---|---|
| Settlement | the settlers' leader (`eotg_frontier_create_leader_effect`) | yes |
| Trade | a new character from `eotg_frontier_settler_leader_template` (the factor), created only when the vassal path runs | no |
| Religious | the mission elder (`eotg_frontier_elder_template`), with `dynasty = none` as vanilla's priest | yes |

- **Culture and faith:** the holder's, by scope, as every Frontier figure is today. A mission of the holder's faith gets an elder of that faith.
- **Government:**
  - city → `republic_government`, set before the grant (hold_court.8300.a order);
  - church → `theocracy_government`, set after the resolve (hold_court.8320.a order).
  - These are vanilla keys, not map keys. Per-government mod variants (a corporate Port under a Corporation) are deferred (§12 D4-4).
- **Not the founder.** Owner ruling Q12 (`frontier_v1.md` §R: "the founder and sponsor never own the result by default") stands. Whether a founder who is not the holder should become the Local Ruler instead (design §7, "Local Ruler: House Veyra") reopens Q12, so it goes to the human (§13 H1).

**Correct either way for V8.** After `set_holding_type`, the new barony may be held by the county holder, by nobody, or by someone else (V8 is still open). Both paths run one `create_title_and_vassal_change` from `scope:eotg_frontier_holder` and `change_title_holder` to the chosen character, whoever held it before.
- The holder path keeps today's "skip if the holder already holds it" check.
- The vassal path never skips.

**This narrows Q12 for two holding types.** The political owner is still the county holder (the System sits in their realm, under their law). The holder no longer holds those two holding types personally. Confirmation is asked in §13 H1. Batch 2 waits on V8 anyway, so the owner has time.

**Script changes** (`common/scripted_effects/eotg_frontier_effects.txt`):
1. `eotg_frontier_complete_effect`:
   - clear `scope:eotg_frontier_local_ruler` at entry;
   - **reorder the Settlement and Religious rows** so the figure is created **before** the holding is built, then `save_scope_as = eotg_frontier_local_ruler` on it;
   - the row calls become:
     - Settlement and Trade: `eotg_frontier_build_holding_effect = { HOLDING = city_holding LOCAL_RULER = yes LOCAL_GOVERNMENT = republic_government }`;
     - Religious: `HOLDING = church_holding LOCAL_RULER = yes LOCAL_GOVERNMENT = theocracy_government`;
     - Military: `HOLDING = castle_holding LOCAL_RULER = no LOCAL_GOVERNMENT = none`.
2. `eotg_frontier_build_holding_effect` (`HOLDING`, `LOCAL_RULER`, `LOCAL_GOVERNMENT`): after the barony is saved, branch on:
   ```
   limit = {
       always = $LOCAL_RULER$                     # shape: eotg_frontier_abandon_effect's always = $FAILED$
       scope:eotg_frontier_holder = {
           capital_province ?= { NOT = { has_holding_type = $HOLDING$ } }
       }
   }
   ```
   - **true:** `eotg_frontier_grant_local_ruler_effect = { GOVERNMENT = $LOCAL_GOVERNMENT$ }`;
   - **false:** today's grant to the holder;
   - the no-slot fallback (development +1, control +10) is unchanged, and the figure stays a courtier.
3. **New** `eotg_frontier_grant_local_ruler_effect` (county scope; `GOVERNMENT`):
   - if `scope:eotg_frontier_local_ruler` doesn't exist, create one from `eotg_frontier_settler_leader_template` (holder's culture and faith, location the county's `title_province`) and save it;
   - then, from `scope:eotg_frontier_holder`: `create_title_and_vassal_change = { type = granted save_scope_as = eotg_frontier_change add_claim_on_loss = no }`, then `scope:eotg_frontier_new_barony = { change_title_holder = { holder = scope:eotg_frontier_local_ruler change = scope:eotg_frontier_change } }`, then `resolve_title_and_vassal_change`;
   - set the government in the order given above;
   - save `scope:eotg_frontier_local_ruler` for the hooks and for .004's tooltip.
4. **.004** gets one custom tooltip, `eotg_frontier.004.local_ruler_tt`, shown only when the Region's type is Settlement, Trade or Religious and the holder's seat is not that holding type. Text: "A local leader will hold the new System as your vassal." Option effects are otherwise unchanged.

**Design §7 is delivered** for three of seven types: Founder, Sponsor, Local Ruler and Political Owner are now four different characters.

### A2. AI participation

**A2.1 Establish** (`common/decisions/eotg_frontier_decisions.txt`, `eotg_decision_frontier_establish`):

| Field | Now | v4 |
|---|---|---|
| `ai_check_interval_by_tier` | county 60, duchy+ 48 | **county 24, duchy+ 24** (barony 0) |
| `ai_will_do` base | 10 | **25**; **+25** if any held county that `eotg_frontier_can_establish` also has `eotg_unclaimed_claimed` (they paid to claim it; a variable read, so the soft seam of A10) |
| gold gate | factor 0 below 2× cost | **factor 0 below 1× cost; factor 0.5 below 2× cost** |
| trait lines | +10 stewardship ≥ 12, +10 ambitious, +5 diligent, −10 lazy, −10 content | unchanged |

- **Precedent:** the mod's own verified decision shape (`eotg_frontier_decisions.txt:149-169`). The vanilla pattern of conditional `ai_will_do` (factor 0 or high) is `G/events/dlc/ep3/ep3_admin_events.txt:130-145`.
- **Expected:** a mean wait after a claim of about 2–4 years, down from 25–35.

**A2.1b Explore** (`eotg_decision_frontier_explore`): claimed Unknown space must be explored before Establish, so it needs the same speed-up:
- interval county 24, duchy+ 24;
- `ai_will_do` +40 if any held county is `eotg_unclaimed_claimed` and Unknown or Partial.

**A2.2 Map cap** (`common/script_values/eotg_frontier_values.txt`, `eotg_frontier_ai_cap_value`):
```
eotg_frontier_ai_cap_value = {
    value = 8
    if = {
        limit = { has_global_variable = eotg_unclaimed_count }
        add = { value = global_var:eotg_unclaimed_count  divide = 20  floor = yes }
    }
    max = 24
}
```
- **New global variable** `eotg_unclaimed_count`: the size of `eotg_unclaimed_counties`. It is set by `eotg_unclaimed_game_start_effect` (after the split) and by `eotg_unclaimed_sweep_effect` (every year). Each counts with `every_in_global_list` + `change_global_variable`, the shape of the existing readout (`eotg_unclaimed_effects.txt:410-413`).
- **If Unclaimed is absent** the variable is absent and the cap is 8, so the coupling is soft (A10).
- **Max 24** bounds tick cost.
- **Per AI:** still 1 Frontier (owner, `frontier_v1.md` §R "AI: … tune later"; this is the tuning).

**A2.3 Backlog** (`common/scripted_triggers/eotg_unclaimed_triggers.txt`, `common/script_values/eotg_unclaimed_values.txt`):
1. **Afford claim and Establish:** `eotg_unclaimed_ai_gold_floor_value = { value = eotg_unclaimed_claim_gold_value add = eotg_frontier_establish_cost_value }`, read in the actor's scope. Unclaimed may read Frontier, per `frontier_unclaimed_regions.md` §1.
2. **Nothing still waiting:** `eotg_unclaimed_ai_may_claim` gains:
   ```
   NOT = { any_held_title = { tier = tier_county  has_variable = eotg_unclaimed_claimed  eotg_frontier_is_frontier = no } }
   ```
   An AI with a claimed county that isn't yet a Frontier claims nothing more. The owner's cap of 2 claimed-but-unsettled counties (UQ10) stays, and this tightens it.
3. **UD3, an AI-only lapse after 10 years: specified, not decided.** Owner decision UQ11 accepted the default of no lapse (`frontier_unclaimed_regions.md` §D). Reopening it is the human's call (§13 H2). If approved, it ships in batch 2 as specified in §A2.3-opt below.

**A2.3-opt (only if H2 is approved):**
- The claim effect sets the county variable `eotg_unclaimed_claim_window` (yes, 10 years) when the actor is AI.
- The yearly sweep releases (`eotg_unclaimed_release_effect`, so A7.1's capital guard applies) any county that has all of: `eotg_unclaimed_claimed`, no window, `eotg_frontier_is_frontier = no`, an AI holder.
- It then toasts nobody: AI only. No loc beyond a debug readout count.

**A2.4 AI Frontier life** (`eotg_frontier_event_roll_effect`, AI branch). **Ruling: yes**, silent scripted outcomes, no events.
- **When:** after the existing AI sponsor and backer paths, an AI holder (not a placeholder) whose Region still has no `eotg_frontier_event_cd` gets a 50% roll. When it passes, set the 3-year `eotg_frontier_event_cd` (the same single authority) and run the new `eotg_frontier_ai_silent_roll_effect`.
- **The pool** (a `random_list`, the mod's verified shape, `frontier_v2.md` F2):

| Weight | Outcome | Modifiers |
|---|---|---|
| 35 | strain +1, cause `hardship` | +10 Hostile without an Orbital Station; +10 Dangerous without a Garrison Post or escort |
| 35 | progress +3 | +10 Rich Resources |
| 15 | progress −3 | +5 Remote without a Navigation Beacon |
| 15 | strain −1 | none |

- **Expected drift is about +0.2 strain per roll:** AI projects can now falter and recover.
- **Precedent:** the mod's own AI-to-AI backing resolved in script (`eotg_frontier_effects.txt:662-722`); vanilla's AI-only branches in events (`if = { limit = { is_ai = yes } }`).
- This partly closes deferral D2-3 (`frontier_v2.md` §14). AI flavour **events** stay deferred.

**Verification (50-year observer run, British Isles test sub-mod, 161 Unsworn counties; needs V-U14):**
- **Unclaimed share at year 30:** between **60% and 92%**. Below 60% is a land rush. Above 92% is inert: fewer than about 13 claims.
- **Settled Regions per decade, decades 2–5:** **4–16.**
- **At least 1 AI Frontier settled by year 20.** No AI ever holds more than 1 claimed county that isn't a Frontier.
- Claimed-but-not-Frontier counties older than 10 years: **≤ 25%** of claimed counties at year 30. This is the H2 decision's evidence.

### A3. Event pacing

**Ruling:**
- **One flavour roll per ruler per pulse**, chosen at random among that ruler's eligible Regions.
- **Every flavour event fires with `days = { 1 120 }`.** Precedent for the delay: `G/events/yearly_events/court_yearly_events.txt:1880-1888` (`trigger_event = { id = … days = { 50 100 } }`); the mod already delays .037 the same way (`frontier_v2.md` §B3), and saved scopes travel with it.
- **Not delayed:** completion (.004) and failure (.005) stay immediate.

**Wiring (the cooldown authority stays in the on_action and the roll; no event trigger reads either):**
1. `eotg_frontier_tick_effect` step 4: the final `else_if` (roll) branch becomes `add_to_temporary_list = eotg_frontier_roll_ready`. It no longer calls the roll.
2. `eotg_on_yearly_frontier_tick` (`common/on_action/eotg_frontier_on_actions.txt`): after the `every_held_title` loop, add `random_in_list = { list = eotg_frontier_roll_ready eotg_frontier_roll_chosen_effect = yes }`. Precedent: `G/common/scripted_effects/00_ai_conqueror_effects.txt:289`.
3. **New** `eotg_frontier_roll_chosen_effect` (county): `save_scope_as = eotg_frontier_county`, `holder = { save_temporary_scope_as = eotg_frontier_holder }`, `eotg_frontier_event_roll_effect = yes`.
4. In `eotg_frontier_flavor_pick_effect` and the founderless `.002` in the roll, every `holder = { trigger_event = eotg_frontier.0xx }` becomes `holder = { trigger_event = { id = eotg_frontier.0xx days = { 1 120 } } }`. Every flavour event already re-checks the Region's state in its trigger and options (verification Q-B1), so a delay is safe.
5. **The debug tick decision** does the same `random_in_list` after its own loop.

**"Funding removes the story": accepted.** A funded project is shorter, so it sees fewer rolls (about 1.5 against 3.0). The owner's 4–6 prompt budget (`frontier_v2.md` §9.1) is a ceiling, not a floor, and vanilla's yearly pools are per character-year, not per venture (`G/common/on_action/yearly_on_actions.txt:3018`). A funded project also draws the backer events (.003, .030, .031), so it isn't silent. Revisit only if playtesting says the funded path feels empty.

### A4. Strain sources

**A4.1 War strain.** New county trigger `eotg_frontier_war_reaches`. It reads `scope:eotg_frontier_holder`, which the tick saves at entry:
```
eotg_frontier_war_reaches = {
    eotg_frontier_war_strains = yes                     # not a Military project (unchanged)
    scope:eotg_frontier_holder = { is_at_war = yes }
    OR = {
        scope:eotg_frontier_holder = { any_character_war = { is_war_leader = prev } }
        any_county_province = {
            any_army_in_location = { army_owner ?= { is_at_war_with = scope:eotg_frontier_holder } }
        }
    }
}
```
- **Where:** the tick's war line uses it in place of `holder = { is_at_war = yes } eotg_frontier_war_strains = yes`.
- **Occupation** stays its own cause (`occupied`).
- **Precedent:**
  - `G/common/character_interactions/00_war.txt:718-724` (`any_character_war = { is_war_leader = root }`);
  - `G/common/on_action/yearly_on_actions.txt:1896-1898` (`location ?= { any_army_in_location = { … } }`);
  - `G/common/on_action/army_on_actions.txt:651-653` (`army_owner`).
- **Loc:** `.005.desc_war` text may stay; it already describes the war reaching the Region.

**A4.2 Founder gap: a new decision `eotg_decision_frontier_appoint_founder` ("Appoint a Founder").**
- **Shown:** `eotg_frontier_holds_founderless = yes` (new character trigger: holds a Frontier whose `eotg_frontier_has_valid_founder = no`).
- **Widget:** the county picker, exactly as Invest (`eotg_frontier_decisions.txt:221-275`; vanilla `G/common/decisions/dlc_decisions/pam/pam_decisions.txt:1395`, `G/common/decisions/50_holy_site_decisions.txt:147`). Items are the founderless Frontiers. The default is the one with the most strain.
- **Effect:** save the county, run `eotg_frontier_pick_founder_effect` (below), then `eotg_frontier_set_founder_effect = { FOUNDER = scope:eotg_frontier_candidate }`. Custom tooltip `eotg_decision_frontier_appoint_founder_effect_tt` names the candidate.
- **Cost:** none. Founding is the player's attention, not their gold; .002(d) also costs nothing.
- **No cooldown needed:** the decision disappears once the founder is valid.
- **AI:** `ai_potential = { always = no }`. The AI is handled in the tick (A4.3).
- **Why a decision and not "death clears the cooldown":** clearing `eotg_frontier_event_cd` from `on_death` would make a second writer of the cooldown authority (lesson 5). It would also still leave the player waiting on a 50% roll.
- **Why not fire .002:** .002's only ungated option (b, "Push through", +4 progress / +1 strain) would become repeatable on demand.
- The .002 founderless variant stays in the roll as it is.

**A4.3 AI auto-founder.** **New** `eotg_frontier_pick_founder_effect` (county; saves `scope:eotg_frontier_candidate`, or clears it):
- the adult, unimprisoned courtier of the holder with the highest `eotg_frontier_type_skill_value`;
- or the holder, if the holder is adult and free and at least as skilled;
- else none.

**New** `eotg_frontier_type_skill_value` (character scope; reads `scope:eotg_frontier_county.var:eotg_frontier_type`): martial for Military, learning for Religious and Research, stewardship otherwise. This mirrors `eotg_frontier_founder_bonus_value`.

The tick's AI line becomes: if an AI holder and `eotg_frontier_pick_founder_effect` found a candidate, set them. Otherwise strain accrues as now, and the AI's Abandon weight (strain ≥ 6) eventually acts. Precedent: the Establish decision's own pick (`eotg_frontier_decisions.txt:127-144`).

### A5. The .005 AI order: the spec stands

**Ruling:** `frontier_v1.md` §6.6's order is intended: d if possible; else b if gold ≥ 2× minor; else a. The AI never picks c: scaling back would discard the type the AI chose for its traits. The code moves to the spec with vanilla's `factor = 0` gates (`G/events/dlc/ep3/ep3_admin_events.txt:130-145`) in `events/eotg_frontier_events.txt` .005:

| Option | `ai_chance` |
|---|---|
| d (backer pays double) | base 100 |
| b (new hands) | base 50; `factor = 0` if d's conditions hold; `factor = 0` if gold < 2 × `minor_gold_value` |
| c (scale back) | base 0 |
| a (let it go) | base 10; `factor = 0` if d's conditions hold; `factor = 0` if b's trigger holds and gold ≥ 2 × minor |

**Spec drift:** §6.6(c) now reads "switches the type to Settlement", the code and loc as built (`frontier_v1.md` §B5). The mark-up is applied in `frontier_v1.md`.

### A6. Unsworn playability (conditional; batch 3, plus a probe in batch 1)

**New fact (static, this session).** `is_playable_character` is a **vanilla scripted trigger**, not an engine trigger (`G/common/scripted_triggers/00_available_for_events_triggers.txt:964-980`: `is_ruler`, and landed above barony). A placeholder holds a county, so **it always passes**. The current probe (`eotg_unclaimed_debug_readout_effect`, which toasts on `is_playable_character`) therefore always reports "playable" and **cannot answer V-U1**.

V-U1 is split into two parts:
- **V-U1a:** does the engine fire `random_yearly_playable_pulse` for a placeholder? That pulse is vanilla's random yearly-event pool, gated by `basic_is_valid_for_yearly_events_trigger` (`G/common/on_action/yearly_on_actions.txt:3018-3021`).
- **V-U1b:** can a placeholder be picked in the lobby? The government assessment found it is not on the vanilla blacklist (`shared_infra.md` B1; CB-54).

**Batch 1 probe (debug tooling, no gating):**
- `random_yearly_playable_pulse = { on_actions = { eotg_unclaimed_debug_pulse_probe } }` in `common/on_action/eotg_unclaimed_on_actions.txt`. The child's trigger is `{ debug_only = yes eotg_is_unclaimed_holder = yes }`, and its effect adds 1 to the global `eotg_unclaimed_debug_pulsed`, setting it first if absent.
- `debug_only` in an on_action: `G/common/on_action/game_start.txt:7288`.
- The parent's trigger gates its children, so a count above 0 after one game year in `-debug_mode` means placeholders get vanilla yearly events.
- The readout toasts the count (`eotg_unclaimed_debug_pulsed_tt`). `eotg_unclaimed_debug_playable_tt` is re-texted to say it reports only the scripted check, "expected yes; not proof of lobby play".

**M2 (build if V-U1a > 0).** Key-level override of `basic_is_valid_for_yearly_events_trigger` in `common/scripted_triggers/eotg_vanilla_overrides_triggers.txt`:
- a **byte-exact copy** of `00_available_for_events_triggers.txt:802-816` at 1.20.0.4, plus one first-child line `NOT = { government_has_flag = eotg_government_is_unclaimed }   # EOTG`;
- the pitfalls §16 procedure;
- the file header lists the new key and version;
- `database_conflicts.log` must show `Overriding entry 'basic_is_valid_for_yearly_events_trigger'`.

**Scope: only this key.**
- **It is the gate of the random yearly pool** (`yearly_on_actions.txt:3020`), struggle pulses (`struggle_on_actions.txt:12`) and one combat path (`combat_on_actions.txt:609`).
- **Not `is_valid_for_narrow_yearly_events` / `_adult`** (`:819`, `:838`): these are used inside 13 event files whose events are reached through pulses this key already gates. The scripter confirms with eotg-vanilla-scout that none of the 13 is fired from an ungated pulse. If one is, add that key to the same override, using the same procedure.
- **Not `is_playable_character`** (752 references): it is far too broad, and vanilla's herders pass it too, so vanilla never relies on it to exclude scenery.
- **Residual, accepted:** the effects inside the other playable pulses (`yearly_playable_pulse`, the three- and five-year pulses) are gated by government flags or tier, and placeholders have no realm to act on.

**M3 (build if V-U1b says pickable; form chosen by T14).** The vanilla mechanism that makes republics, mercenaries and holy orders unplayable is the scripted rule `is_character_allowed_to_be_player` (`G/common/scripted_rules/00_rules.txt:151-249`). A post-lobby toast cannot stop play; this rule can.
- **If T14 shows a key-level override in a separately named file works:** new file `common/scripted_rules/zz_eotg_rules.txt`, a byte-exact copy of the rule at 1.20.0.4 plus one entry inside the `scope:will_override_government = no` branch, beside the republic and mercenary entries:
  ```
  custom_description = {
      text = "EOTG_GAME_OVER_CANNOT_PLAY_UNSWORN"
      NOT = { government_has_flag = eotg_government_is_unclaimed }
  }   # EOTG
  ```
  Loc keys `EOTG_GAME_OVER_CANNOT_PLAY_UNSWORN` and `NOT_EOTG_GAME_OVER_CANNOT_PLAY_UNSWORN`. The `NOT_` form is engine-derived, per vanilla's pair at `G/localization/english/gui/ingame_main_l_english.yml:83-84`. The pitfalls entry gets a second key.
  - **New folder:** `common/scripted_rules/` must be added to CLAUDE.md's placement list (orchestrator).
- **If only a full-file override works:** the owner's choice (§13 H3). The recommendation follows `government_template.md` §6.2(b): accept, plus the owner-approved lobby warning (UQ1). That is an additive `on_game_start_after_lobby` → `eotg_unclaimed_on_lobby_check`, with effect `every_player = { limit = { eotg_is_unclaimed_holder = yes } send_interface_toast = { title = eotg_unclaimed_toast_unplayable left_icon = this } }`. `every_player` precedent: `G/common/on_action/game_start.txt:3840`.
- **Not chosen: swapping the player.** Vanilla can do it (`set_player_character`, `game_start.txt:3796-3799`), but there is no map-agnostic way to choose whom.

**Related ruling (government assessment G3): Unsworn has no succession law. Accepted and recorded.**
- **Why:** succession is scripted (`on_death` replaces the placeholder before death; `frontier_unclaimed_regions.md` §5.3), so any engine default is cosmetic.
- **Check:** look at the realm screen during the V-U1 sitting. If it shows "Anarchy" or churns a law every year, give the government vanilla's least-intrusive law in a follow-up.

### A7. Release and claim rules

**A7.1 The capital guard lives in the effect.** New county trigger `eotg_unclaimed_may_release`:
```
eotg_unclaimed_may_release = {
    NOT = {
        holder ?= {
            eotg_is_unclaimed_folk = no
            eotg_is_unclaimed_holder = no
            NOT = { has_character_flag = eotg_unclaimed_splitting }
        }
        this = holder.capital_county
    }
}
```
- `eotg_unclaimed_release_effect`'s whole body is wrapped in `if = { limit = { eotg_unclaimed_may_release = yes } … }`. A real ruler's capital is never released, whoever calls.
- **What it leaves alone:** seeds (flagged `eotg_unclaimed_splitting`) and placeholders (folk, or the government) are not "real", so game start, death replacement and adoption are unaffected.
- `eotg_unclaimed_would_release` gains `eotg_unclaimed_may_release = yes` in place of its own capital line, so there is **one** statement of UQ5.
- **Test sub-mod consequence:** `docs/test_submods/frontier_vanilla` releases five Sardinian counties at start. Those that are a judge's capital now stay with the judge.
  - The scripter updates the README to list what actually releases.
  - If fewer than two Sardinian counties end up Unclaimed, release one more non-capital county there. Vanilla keys are allowed in the sub-mod.
  - No judge ends up landless: that is the U2 check.

**A7.2 Every barony the old placeholder held moves; enclaves dissolve.** New county effect `eotg_unclaimed_move_baronies_effect` (`OLD`, `NEW`, `CHANGE`): `every_county_province = { barony = { if = { limit = { holder ?= $OLD$ } change_title_holder = { holder = $NEW$ change = $CHANGE$ } } } }`. It runs inside the already open title change.

**Callers:**
- `eotg_unclaimed_claim_effect`, with OLD = the placeholder and NEW = the claimant. This replaces the capital-only block at `:459-472`.
- `eotg_unclaimed_create_holder_effect`, **only when `scope:eotg_unclaimed_previous` is folk**: death replacement or adoption, with OLD = the previous placeholder. When the previous holder is a real ruler, §6.1 still binds: only the capital barony moves (`frontier_unclaimed_regions.md` §6.1, unchanged).

**Sweep rule (d)**, in `eotg_unclaimed_sweep_effect`, applies to every Unsworn holder that holds no Unclaimed county:
- each barony it holds goes to that barony's county holder (granted);
- then `eotg_unclaimed_vanish_effect`;
- count it in `eotg_unclaimed_sweep_fixed`.

**Iterate the global holder list** the scripter adds under brief §5 ("track holders in a global list") if it exists by then, else `every_ruler` with `eotg_is_unclaimed_holder = yes`.

**Cartographer:** `frontier_unclaimed_regions.md` §10.5 (non-capital baronies `holding = none`) stays binding.

**A7.3 Raise Your Colours as a decision.** New `eotg_decision_unclaimed_raise_colours` in `common/decisions/eotg_unclaimed_decisions.txt`. Unclaimed owns it.
- **`is_shown`:** `eotg_unclaimed_can_claim = yes`, plus `any_in_global_list = { variable = eotg_unclaimed_counties eotg_unclaimed_in_reach = { ACTOR = root } }`.
- **`is_valid`** (custom descriptions, words only):
  - the cooldown is ready (`eotg_unclaimed_colours_ready = yes`);
  - gold ≥ `eotg_unclaimed_claim_gold_value`;
  - prestige ≥ `eotg_unclaimed_claim_prestige_value`.
- **Widget:** the county picker.
  - **Items:** `every_in_global_list = { variable = eotg_unclaimed_counties limit = { eotg_unclaimed_in_reach = { ACTOR = scope:actor } } add_to_list = item_list }`.
  - **Default and AI:** the most developed. `ordered_in_global_list` is already used in `eotg_frontier_pick_expedition_target_effect`; carry its UNVERIFIED marker.
  - **Precedent:** the expedition picker, which already lists in-reach Unclaimed counties (`eotg_frontier_decisions.txt:956-996`).
- **Effect:** save `scope:selected_item` as the target, then `custom_tooltip = eotg_unclaimed_claim_effect_tt`, `custom_tooltip = eotg_unclaimed_claim_returns_tt`, and `eotg_unclaimed_claim_effect = { TARGET = scope:eotg_unclaimed_target }`.
- **The interaction is kept** as it is.

**One cooldown authority for both paths.** Remove the interaction's `cooldown = { years = 5 }`.
- `eotg_unclaimed_claim_effect` sets the actor variable `eotg_unclaimed_colours_cd` (yes, `years = 5`).
- Both the interaction (`is_valid_showing_failures_only`) and the decision read it through the new character trigger `eotg_unclaimed_colours_ready = { NOT = { has_variable = eotg_unclaimed_colours_cd } }`, with the tooltip `eotg_unclaimed_claim_cooldown_tt`.
- Precedent for a decision gated on a timed marker: vanilla `cooldown` on decisions (`G/common/decisions/00_cultural_tradition_decisions.txt:141`) would be per-path, which is why one variable is used.
- **The AI gap moves too.** `set_global_variable eotg_unclaimed_ai_gap` moves from the interaction's `on_accept` into `eotg_unclaimed_claim_effect`, under `is_ai = yes`, so every path throttles.

**AI on the decision:** `ai_check_interval_by_tier` all 0 and `ai_potential = { always = no }`, **unless V-U14 fails** (placeholders are not `neighboring_rulers`, so the interaction's AI never fires).
- **In that case (batch 2 conditional item):** the decision's AI turns on (interval county 36, duchy+ 24; `ai_potential = { eotg_unclaimed_ai_may_claim = yes }`; `ai_will_do` as the interaction's, §8.4) and the interaction's `ai_frequency_by_tier` goes to 0.
- **Exactly one AI path is ever live.** The decision's distance reach doesn't depend on `neighboring_rulers`.

**A7.4 The blocked-war message.** In `eotg_vanilla_overrides_triggers.txt`, the bare defender line becomes:
```
custom_tooltip = {
    text = eotg_unclaimed_defender_tt
    government_has_flag = eotg_government_is_unclaimed
}   # EOTG (defender)
```
- **Placement:** still a separate child of the NOR, sibling of vanilla's herder `custom_tooltip`. One trigger inside, so there is no AND problem (the 2026-10-06 correction).
- **Mirrors vanilla's herder entry** (`G/common/scripted_triggers/00_war_and_peace_triggers.txt:1144-1152`), whose text is `is_a_herder_defender_tt` (`G/localization/english/interactions_l_english.yml:168`). That text uses `[defender.GetShortUIName]` and points to the retrieval interaction; ours points to Raise Your Colours.
- **Allowed:** we own this copy, and the change alters only the Unsworn branch's text. The file header's "two marked lines" becomes "two marked places".

### A8. Legibility and sponsor value

**A8.1 Qualitative bands.** New county effect `eotg_frontier_legibility_tooltip_effect`. It prints `custom_tooltip` lines inside `if/else_if` branches, so only the true branch renders. That is the mod's verified pattern (`eotg_frontier_decisions.txt:281-291`, the waiting tooltip).

**Called from the effect blocks of:**
- Invest (`scope:eotg_frontier_county ?= { … }`);
- Build;
- Abandon.

**Not in modifier descriptions:** a county modifier description has no reliable scope for data functions. Deferred (§12 D4-6).

**Bands** (thresholds read hidden values; **no key prints a number**):

| Line | Condition (post-pace `eotg_frontier_yearly_gain_value` = G) | Key |
|---|---|---|
| Pace | G < 1 | `eotg_frontier_band_stalled_tt` (time line suppressed) |
| | 1 ≤ G < 6 | `eotg_frontier_band_pace_slow_tt` |
| | 6 ≤ G < 9 | `eotg_frontier_band_pace_steady_tt` |
| | G ≥ 9 | `eotg_frontier_band_pace_fast_tt` |
| Time left (`eotg_frontier_years_left_value`) | progress 100 with a floor unmet | (the existing `eotg_decision_frontier_invest_waiting_tt`; no time line) |
| | ≥ 8 | `eotg_frontier_band_time_decade_tt` |
| | 3–7 | `eotg_frontier_band_time_years_tt` |
| | < 3 | `eotg_frontier_band_time_near_tt` |
| Strain (the .002 bands, 4 and 6) | < 4 | `eotg_frontier_band_strain_calm_tt` |
| | 4–5 | `eotg_frontier_band_strain_strained_tt` |
| | ≥ 6 | `eotg_frontier_band_strain_breaking_tt` |
| What weighs on it (strain ≥ 4 only; `var:eotg_frontier_last_cause`) | one of 7 causes | `eotg_frontier_band_cause_no_founder_tt`, `_low_control_tt`, `_occupied_tt`, `_war_tt`, `_sponsor_lapsed_tt`, `_danger_tt`, `_hardship_tt` |

**New** `eotg_frontier_years_left_value` (county): `value = 100`, `subtract = var:eotg_frontier_progress`, `divide = { value = eotg_frontier_yearly_gain_value min = 1 }`. The pace thresholds put a typical bare project (G ≈ 7) at "steady" and a sponsored one (G ≈ 10–12) at "fast".

**A8.2 Sponsor input:** `eotg_frontier_sponsor_bonus_value` **6 → 8** pre-pace, which is +4 a year after the ×0.5 pace.
- **Not +10:** the brief's +10 would take a sponsored Settlement to about 7.5 years, under the owner's 8–10 band.
- **Re-paced with 8:**
  - sponsored Settlement is about **8.1 years**, from 9;
  - sponsored Research is about **9.8 years**, from 11;
  - every type lands in 8–10.
- Unsponsored pacing is unchanged.

**A8.3 Sponsor completion reward.** New county effect `eotg_frontier_reward_sponsor_effect`, called in `eotg_frontier_complete_effect` after the type row and before `eotg_frontier_settle_effect` (which drops the sponsor). If `eotg_frontier_has_valid_sponsor = yes`:
- the sponsor gets `add_prestige = medium_prestige_value` (150; `G/common/script_values/00_basic_values.txt:1002`);
- the holder gets `add_opinion = { modifier = eotg_frontier_opinion_pleased target = <sponsor> years = 10 }`, an existing shared modifier with no government prefix;
- the sponsor gets a toast `eotg_frontier_toast_backing_settled` (left icon the sponsor, right icon the county).

**Not chosen:** a share of the Region's 25-year modifier. County modifiers can't be split to a non-holder, and a new character modifier would be new art and loc for little gain.

### A9. Vocabulary (recommendation; needs-lore)

1. **"Pressure" has no owner.**
   - The Void lift plan (`void_lift_plan_cloud.md` §3c) recommends Void moves to "Undertow"; cybernetics moved to "the static"; the Cartel's key `eotg_cartel_defiance_pressure` is internal.
   - **Recommendation:** "pressure" stays a plain English word that no system names its resource with. Frontier calls its value **"strain"**, which matches `eotg_frontier_strain`.
   - **Localizer:** re-word frontier loc lines 93, 96, 132, 290 and 365 to "strain". Keep line 83's literal "pressure seal".
   - **Lore-keeper:** confirm the ownership rule alongside §3c.
2. **"Frontier Legacy: …" → "Frontier Roots: …"** (loc lines 197–206; keys unchanged).
   - It collides with vanilla dynasty Legacies and the mod's Confluence Legacies.
   - Not "Heritage": that is vanilla's culture pillar.
   - Lore-keeper confirms the name.

### A10. Modularity: coupling accepted, seam rule for new code

**Ruling:** record the 17 Frontier → Unclaimed references (brief A10) as **accepted coupling**. The record is a new §21 in `frontier_unclaimed_regions.md`, applied in this pass.

**Reasons:**
1. The owner made Unclaimed Frontier's "Option B" (2026-10-06), so the two ship as one feature.
2. Rerouting the references through Unclaimed-defined seam triggers would still leave Frontier unable to load without Unclaimed (an undefined scripted trigger is a load error). The cost would buy no real modularity.
3. **Design §2.1's list** (Greater Drifts, Patronage, corporate governments, …) doesn't name Unclaimed. Its "a custom claims system" line is answered by Raise Your Colours leaving no CK3 claim (`frontier_unclaimed_regions.md` §D).

**Rule for all new code, from v4 on:**
- New Frontier → Unclaimed reads go through **variables and global variables only** (`eotg_unclaimed_claimed`, `eotg_unclaimed_county`, `eotg_unclaimed_count`, the list `eotg_unclaimed_counties`). These degrade to "absent" if Unclaimed is removed.
- Never through Unclaimed's scripted triggers or effects.
- Unclaimed → Frontier calls are unrestricted (Unclaimed §1 depends on Frontier).

**v4's own new references obey this:**
- A2.1 reads `eotg_unclaimed_claimed`;
- A2.2 reads `eotg_unclaimed_count`.

### A11. Smaller rulings

1. **Abandon −1 development: keyed to this attempt.** The intent of `frontier_v1_verification.md` Q5 is "no farming". This keeps the intent and drops the drain.
   - **New project variable** `eotg_frontier_dev_granted_now` (0–2): `eotg_frontier_grant_milestone_dev_effect` adds 1 whenever it actually grants. It is removed with the other project variables (`eotg_frontier_clear_project_effect`).
   - **`eotg_frontier_abandon_effect`:** replace `var:eotg_frontier_milestone >= 1` with `var:eotg_frontier_dev_granted_now ?= …` at 1 or more. When true: `change_development_level = -1`, and **lower `eotg_frontier_dev_granted` by 1**, so the lost step can be re-earned by a later attempt.
   - **Farming check:** at most +2 development net, over any number of attempts.
2. **The holy-order variable: approved with `?=` fall-through.**
   - **Why the order is kept:** storing the order's leader instead would lose "the order's *next* leader", which is owner rule Q3-5.
   - **The change:** in `eotg_frontier_resolve_faith_successor_effect`, `var:eotg_frontier_pending_order = {` becomes `var:eotg_frontier_pending_order ?= {`, and the faith branch likewise for symmetry. A disbanded order then leaves `scope:eotg_frontier_successor` unset, and the existing lapse branch runs. QA check F6 (error.log after a holy-order succession) confirms it.
3. **Danger counters: −5 each, matching the beacon.** In `eotg_frontier_flavor_pick_effect`, .034's entry gains:
   - `modifier = { add = -5 has_county_modifier = eotg_frontier_trait_dangerous has_county_modifier = eotg_frontier_infra_garrison_post }`;
   - and the same for `eotg_frontier_mod_merc_escort`.
   - **The weight floor stays 5** (5 + 10 − 5 − 5), so the event never vanishes.
   - The tooltips stay true. The localizer softens only words that claim the raider *event* is gone.

### Option depth (in scope: existing options only; batch 4)

House form `stress_impact = { <trait> = <value> }`. The mod uses the old form until event_quality W11 (`event_quality_v1.md:188`). Vanilla still accepts it in 32 event files, and its 1.20 form is `stress_and_fulfillment_impact` (`G/events/dlc/ep3/ep3_admin_events.txt:125-133`).

| Option | Stress rows |
|---|---|
| `.005.a` Let it go | compassionate `medium_stress_impact_gain`; diligent `minor_stress_impact_gain`; stubborn `minor_stress_impact_gain`; lazy `minor_stress_impact_loss` |
| `.033.a` Back the founder (drive the crews) | compassionate `medium_stress_impact_gain`; callous `minor_stress_impact_loss` |
| `.033.b` Side with the settlers | ambitious `minor_stress_impact_gain`; compassionate `minor_stress_impact_loss` |
| `.031.a` No say for the backer | humble `minor_stress_impact_gain`; arrogant `minor_stress_impact_loss` |
| `.032.b` Refuse the terms | generous `minor_stress_impact_gain`; compassionate `minor_stress_impact_gain`; stubborn `minor_stress_impact_loss` |
| `.034.b` Make do | compassionate `minor_stress_impact_gain` |

**Outcome rolls** (vanilla `duel`, `G/events/yearly_events/court_yearly_events.txt:1240-1281`):

| Option | Duel | Success | Failure |
|---|---|---|---|
| `.032.c` Talk them round | `skill = diplomacy`, `value = average_skill_rating`, success 60 / failure 40, `compare_modifier` ±2 | strain −1 (as now) | no strain change |
| `.033.c` Settle it myself | the same | strain −1 (as now) | no strain change (the gold is still spent) |

- The .032.c diplomacy gate stays.
- AI weights are unchanged.
- Each branch carries a `desc` key (§7).
- **Coordination:** event_quality batch B12 (frontier) must take these rows as given. If B12 runs first, it builds them; if it runs after, it keeps them. Either way, report them as "added" rows.

---

## 4. Identifier table (all new unless marked)

| Type | Key | System | Ruling |
|---|---|---|---|
| scripted effect | `eotg_frontier_grant_local_ruler_effect` | Frontier | A1 |
| scripted effect (changed params) | `eotg_frontier_build_holding_effect` (+`LOCAL_RULER`, `LOCAL_GOVERNMENT`) | Frontier | A1 |
| saved scope | `eotg_frontier_local_ruler` | Frontier | A1 |
| scripted effect | `eotg_frontier_ai_silent_roll_effect` | Frontier | A2.4 |
| global variable | `eotg_unclaimed_count` | Unclaimed (set) / Frontier (read) | A2.2 |
| county variable (optional, H2) | `eotg_unclaimed_claim_window` | Unclaimed | A2.3-opt |
| temporary list | `eotg_frontier_roll_ready` | Frontier | A3 |
| scripted effect | `eotg_frontier_roll_chosen_effect` | Frontier | A3 |
| scripted trigger | `eotg_frontier_war_reaches` | Frontier | A4.1 |
| decision | `eotg_decision_frontier_appoint_founder` | Frontier | A4.2 |
| scripted trigger | `eotg_frontier_holds_founderless` | Frontier | A4.2 |
| scripted effect | `eotg_frontier_pick_founder_effect` | Frontier | A4.2, A4.3 |
| script value | `eotg_frontier_type_skill_value` | Frontier | A4.3 |
| on_action (debug) | `eotg_unclaimed_debug_pulse_probe` (child of `random_yearly_playable_pulse`) | Unclaimed | A6 |
| global variable (debug) | `eotg_unclaimed_debug_pulsed` | Unclaimed | A6 |
| vanilla key override (cond.) | `basic_is_valid_for_yearly_events_trigger` | Unclaimed | A6 M2 |
| vanilla scripted-rule override (cond.) | `is_character_allowed_to_be_player` (file `zz_eotg_rules.txt`) | Unclaimed | A6 M3 |
| on_action (cond., fallback) | `eotg_unclaimed_on_lobby_check` (child of `on_game_start_after_lobby`) | Unclaimed | A6 M3 fallback |
| scripted trigger | `eotg_unclaimed_may_release` | Unclaimed | A7.1 |
| scripted effect | `eotg_unclaimed_move_baronies_effect` | Unclaimed | A7.2 |
| scripted effect | `eotg_unclaimed_dissolve_enclave_effect` | Unclaimed | A7.2 (sweep rule d) |
| decision | `eotg_decision_unclaimed_raise_colours` | Unclaimed | A7.3 |
| character variable | `eotg_unclaimed_colours_cd` (5 years) | Unclaimed | A7.3 (single cooldown authority) |
| scripted trigger | `eotg_unclaimed_colours_ready` | Unclaimed | A7.3 |
| scripted effect | `eotg_frontier_legibility_tooltip_effect` | Frontier | A8.1 |
| script value | `eotg_frontier_years_left_value` | Frontier | A8.1 |
| scripted effect | `eotg_frontier_reward_sponsor_effect` | Frontier | A8.3 |
| county variable | `eotg_frontier_dev_granted_now` | Frontier | A11.1 |
| changed values | `eotg_frontier_ai_cap_value`, `eotg_frontier_sponsor_bonus_value` (6→8), `eotg_unclaimed_ai_gold_floor_value` | both | A2.2, A8.2, A2.3 |
| changed triggers | `eotg_unclaimed_ai_may_claim`, `eotg_unclaimed_would_release` | Unclaimed | A2.3, A7.1 |
| removed field | `cooldown = { years = 5 }` on `eotg_unclaimed_claim_interaction` | Unclaimed | A7.3 |

**No landed titles, no new events, no new templates, no new modifiers, no new opinion modifiers, no gfx.** Name lists, CoAs and holy sites: none touched. Icons: the two new decisions use `decision_realm.dds` like every Frontier decision. The Raise Your Colours decision painting is added to the art list (`C:/Users/river/Desktop/EotG_Art_Needed.md`; owner: human).

## 5. File placement

| File | Changes | Owner |
|---|---|---|
| `common/scripted_effects/eotg_frontier_effects.txt` | A1, A2.4, A3, A4.3, A8.1, A8.3, A11.1–3 | scripter |
| `common/scripted_triggers/eotg_frontier_triggers.txt` | A4.1, A4.2 | scripter |
| `common/script_values/eotg_frontier_values.txt` | A2.2, A4.3, A8.1, A8.2 | scripter |
| `common/decisions/eotg_frontier_decisions.txt` | A2.1, A2.1b, A4.2, A8.1 calls, debug tick (A3) | scripter |
| `common/on_action/eotg_frontier_on_actions.txt` | A3 | scripter |
| `events/eotg_frontier_events.txt` | A1 (.004 tooltip), A5 (.005 `ai_chance`), option depth | scripter |
| `common/scripted_effects/eotg_unclaimed_effects.txt` | A2.2 count, A2.3-opt, A7.1, A7.2, A7.3 (cooldown and gap in the claim effect) | scripter |
| `common/scripted_triggers/eotg_unclaimed_triggers.txt` | A2.3, A7.1, A7.3 | scripter |
| `common/script_values/eotg_unclaimed_values.txt` | A2.3 | scripter |
| `common/character_interactions/eotg_unclaimed_interactions.txt` | A7.3 (cooldown and gap moved; the V-U14 AI switch) | scripter |
| `common/decisions/eotg_unclaimed_decisions.txt` | A7.3 | scripter |
| `common/on_action/eotg_unclaimed_on_actions.txt` | A6 probe; A6 M3 fallback (cond.) | scripter |
| `common/scripted_triggers/eotg_vanilla_overrides_triggers.txt` | A7.4; A6 M2 (cond.) | scripter |
| `common/scripted_rules/zz_eotg_rules.txt` (**new folder**, cond.) | A6 M3 | scripter; orchestrator adds the folder to CLAUDE.md |
| `docs/test_submods/frontier_vanilla/` | A7.1 README and the Sardinia list | scripter |
| `localization/english/eotg_frontier_l_english.yml` | §7 | localizer |
| `localization/english/eotg_unclaimed_l_english.yml` | §7 | localizer |
| `docs/pitfalls.md` | override keys added (A6, A7.4) | orchestrator |

No `replace_path`. No descriptor change.

## 6. Wiring

| Item | Fired by | Tiers | Cooldown authority |
|---|---|---|---|
| Frontier tick | `yearly_playable_pulse` → `eotg_on_yearly_frontier_tick` (unchanged) | every playable holder (county–hegemony) | `eotg_frontier_tick_year` (unchanged) |
| Flavour roll | the same on_action, after the loop, through `random_in_list` over `eotg_frontier_roll_ready` | every tier | per county `eotg_frontier_event_cd` (set only in the roll) + one roll per ruler per pulse (the list). No event trigger reads either |
| AI silent roll | inside the roll, AI branch | every tier | the same `eotg_frontier_event_cd` |
| Appoint a Founder | player decision | county–hegemony (`ai_check_interval_by_tier` all 0) | none (shown only while founderless) |
| Establish / Explore AI | decisions | county 24, duchy+ 24, barony 0 | the decision interval |
| Raise Your Colours (decision and interaction) | player; AI per V-U14 | county+ | `eotg_unclaimed_colours_cd` (actor, 5 years) + global `eotg_unclaimed_ai_gap` (AI, 180 days), each set only in `eotg_unclaimed_claim_effect` |
| Unclaimed count, enclave rule, (opt.) lapse | `yearly_global_pulse` → sweep (unchanged) | none | the sweep's yearly cadence |
| Pulse probe | `random_yearly_playable_pulse` (additive) | debug only | none (counter) |
| M3 fallback | `on_game_start_after_lobby` (additive) | none | once |

**Role triggers at every tier:** every decision keeps every tier key. New Frontier entry points exclude placeholders through the existing `eotg_is_unclaimed_folk` / `_holder` guards (M1).

## 7. Loc surface

**`eotg_frontier_l_english.yml`** (UTF-8 BOM, Canadian English, bare `[x.GetName]`, no numbers for progress or strain, dynamic knight term):
- A1: `eotg_frontier.004.local_ruler_tt`.
- A4.2: `eotg_decision_frontier_appoint_founder`, `_desc`, `_confirm`, `_pick_tt`, `_effect_tt` (names `[eotg_frontier_candidate.GetName]`).
- A8.1: `eotg_frontier_band_stalled_tt`, `_pace_slow_tt`, `_pace_steady_tt`, `_pace_fast_tt`, `_time_decade_tt`, `_time_years_tt`, `_time_near_tt`, `_strain_calm_tt`, `_strain_strained_tt`, `_strain_breaking_tt`, and `eotg_frontier_band_cause_{no_founder,low_control,occupied,war,sponsor_lapsed,danger,hardship}_tt`. That is 17 keys, all prefixed `eotg_frontier_band_`.
- A8.3: `eotg_frontier_toast_backing_settled`.
- Option depth: `eotg_frontier.032.c_success`, `.032.c_failure`, `.033.c_success`, `.033.c_failure`.
- A9 (existing keys, text only): lines 93, 96, 132, 290 and 365 ("pressure" → strain wording); 197, 199, 201, 203 and 205 ("Frontier Legacy:" → "Frontier Roots:", pending lore).

**`eotg_unclaimed_l_english.yml`:**
- A6: `eotg_unclaimed_debug_pulsed_tt` (new), and `eotg_unclaimed_debug_playable_tt` (re-text).
- A6, conditional:
  - `EOTG_GAME_OVER_CANNOT_PLAY_UNSWORN` and `NOT_EOTG_GAME_OVER_CANNOT_PLAY_UNSWORN`. These are engine-derived forms; flag both for the prefix lint as a deliberate exception;
  - or `eotg_unclaimed_toast_unplayable`.
- A7.3: `eotg_decision_unclaimed_raise_colours` ("Raise Your Colours"), `_desc` (LAW AT 866: "…yours for as long as you can hold it. Nobody else has to agree…", §D), `_confirm`, `_pick_tt`; `eotg_unclaimed_claim_cooldown_tt`.
- A7.4: `eotg_unclaimed_defender_tt`: "[defender.GetShortUIName] is Unsworn and cannot be attacked", pointing to Raise Your Colours. Shape: vanilla `interactions_l_english.yml:168`.
- A2.3-opt, only if H2 is approved: the debug readout count line in the existing `eotg_unclaimed_debug_counts_tt`.

**No `replace/` overrides.** No vanilla string changes.

**Glossary check (localizer):** Region = county, System = barony. No "mayor", "bishop", "charter" or "village" in mod text. Vanilla's own government labels on the new vassals are a lore note (§8).

## 8. Lore constraints

- **LAW AT 866** (`frontier_unclaimed_regions.md` §D):
  - the Raise Your Colours decision text never says a claim is filed, registered, recognized, licensed or chartered, or that others must respect it;
  - the local vassal of A1 holds the System **under the holder's law**: no authority above the polity;
  - don't borrow vanilla's "Grant charter" phrasing (hold_court.8300.a).
- **Time-neutral Frontier text** (`frontier_v1.md` §V); no named factions; no Void; Canadian English.
- **Band text:** words only. "About a decade remains" is a phrase, not a figure; never "8 years".
- **Needs-lore:**
  1. Ownership of "pressure" (A9.1).
  2. "Frontier Roots" (A9.2).
  3. The A1 vassals show vanilla government names ("Republic", "Theocracy") in their character windows. Does that read acceptably at 866, or is a reflavour of those labels a Gate-4 item for the localizer? A display question only; it doesn't block the build.

## 9. Vanilla precedent (summary, all re-checked at 1.20.0.4)

| Change | Vanilla file:line |
|---|---|
| City granted to a vassal + republic | `G/events/activities/hold_court_activity/hold_court_events_joe.txt:507-521`; `hold_court_events_general.txt:6912-6945` |
| Church held by a created priest + theocracy | `hold_court_events_joe.txt:1224`, `:1240-1260` |
| Feudal holdings and required county holdings | `G/common/governments/00_government_types.txt:18-20` |
| "Wrong holding type" rule | `G/localization/english/holdings_l_english.yml:36` |
| `factor = 0` `ai_chance` gates | `G/events/dlc/ep3/ep3_admin_events.txt:130-145` |
| Delayed `trigger_event` | `G/events/yearly_events/court_yearly_events.txt:1880-1888` |
| `random_in_list` | `G/common/scripted_effects/00_ai_conqueror_effects.txt:289` |
| War leader / armies in a location / army owner | `G/common/character_interactions/00_war.txt:718-724`; `G/common/on_action/yearly_on_actions.txt:1896-1898`; `G/common/on_action/army_on_actions.txt:651-653` |
| County-picker widget | `G/common/decisions/dlc_decisions/pam/pam_decisions.txt:1334, 1395`; `G/common/decisions/50_holy_site_decisions.txt:119, 147` |
| Decision cooldown (why not used) | `G/common/decisions/00_cultural_tradition_decisions.txt:141` |
| Yearly-event gate | `G/common/scripted_triggers/00_available_for_events_triggers.txt:802-816`; `is_playable_character` `:964-980`; `G/common/on_action/yearly_on_actions.txt:3018-3021` |
| Playable blacklist | `G/common/scripted_rules/00_rules.txt:151-249`; loc pair `G/localization/english/gui/ingame_main_l_english.yml:83-84` |
| Player swap (not used) / `every_player` | `G/common/on_action/game_start.txt:3796-3799`, `:3840` |
| `debug_only` in an on_action | `G/common/on_action/game_start.txt:7288` |
| Herder defender tooltip | `G/common/scripted_triggers/00_war_and_peace_triggers.txt:1144-1152`; `G/localization/english/interactions_l_english.yml:168` |
| `duel` outcome roll | `G/events/yearly_events/court_yearly_events.txt:1240-1281` |
| Stress forms | `G/events/dlc/ep3/ep3_admin_events.txt:125-133` (1.20 form); the old `stress_impact` is still in 32 vanilla event files |
| `medium_prestige_value` | `G/common/script_values/00_basic_values.txt:1002` |

**Deviations, each with its reason:**
- A1's capital-type proxy: no vanilla `valid_holdings` reader exists.
- A7.3's variable cooldown: one authority shared by two entry points.
- A6 M2 limited to one key: blast radius.

## 10. Definition of done

**Static (QA):**
1. Tiger clean on all Frontier and Unclaimed files, except the CLAUDE.md known-benign families (county-picker widget ×5 per new widget, override strict-scopes, `rite`, `allow_accolades`).
2. The PX language server and `px_vocab_check.py` show 0 new findings.
3. `px_event_report.py`: 19/19 Frontier events still reachable; 0 orphans.
4. Greps:
   - `grep -rnE 'eotg_[ekdcb]_'` is empty;
   - `grep -nE 'title:|province:|culture:|faith:|character:'` over both systems' `common/` files returns nothing (map-agnostic);
   - no event `trigger = { }` reads `eotg_frontier_event_cd`, `eotg_frontier_roll_ready`, `eotg_unclaimed_colours_cd` or `eotg_unclaimed_ai_gap`;
   - no loc key in §7 contains `Var('eotg_frontier_progress'` or `Var('eotg_frontier_strain'` (the debug readout keys excepted).
5. `eotg_frontier_progress` or `_strain` is moved in every branch of `eotg_frontier_ai_silent_roll_effect`. Every flavour event still moves or reads one of them.
6. Override files: `database_conflicts.log` lists exactly the overridden keys, which in batch 3 may add `basic_is_valid_for_yearly_events_trigger` and `is_character_allowed_to_be_player`. Each body diffs against vanilla 1.20.0.4 with only the `# EOTG` lines different.

**In game, and which check gates which item:**

| Item | Check | Pass |
|---|---|---|
| A3 | Hold 3+ Frontiers; run the debug tick 5 times | never more than 1 flavour event per ruler per tick; events land on different days |
| A4.1 | Join an ally's distant war (not leader, no army in the Region); tick 3× | no `war` strain. As war leader: +1 per tick |
| A4.2 | Kill the founder | Appoint a Founder appears; after use, the founder is valid and no `no_founder` strain accrues next tick |
| A4.3 | Give an AI holder a child or imprisoned founder (console) | the next tick sets an adult courtier or the holder |
| A5 | Static: the `ai_chance` factors match §A5 | — |
| A1 | **V8**, then each of Settlement, Trade and Religious completed under a feudal holder, and Settlement under a Corporation holder (British Isles sub-mod) | feudal: the new barony is held by the local ruler, a vassal of the holder, republic or theocracy; no "wrong holding type" warning on the holder. Corporation: the holder keeps the Port. Military: the holder keeps the castle |
| A2 | **V-U14**, then the 50-year observer run | the §A2 bands |
| A6 probe → M2 | **V-U1a**: one game year in `-debug_mode` | readout `eotg_unclaimed_debug_pulsed` > 0 ⇒ build M2; after M2, a second run reads 0 |
| A6 M3 | **V-U1b** (lobby pick), then **T14** | after M3, the pick is refused with the Unsworn GAME_OVER text, and a republic is still refused |
| A7.1 | **U2**: the Frontier sub-mod start | no Sardinian judge is landless; the debug release on a capital does nothing |
| A7.2 | Give a placeholder a second barony (console); claim it | the claimant holds both; a stray placeholder baron is dissolved by the next sweep (readout "fixed" ≥ 1) |
| A7.3 | Use the decision | lists exactly the in-reach Unclaimed Regions; a second claim within 5 years is blocked on both paths |
| A7.4 | Declare war on an Unsworn holder | the CB list shows `eotg_unclaimed_defender_tt` |
| A7 (other) | **V-U9 / V-U8 / V-U15** as in `frontier_unclaimed_regions.md` §12 | — |
| A8 | Hover Invest, Build, Abandon | three band lines in words; no digits for progress or strain |
| A11.1 | Abandon a project that granted no development this attempt | development unchanged |
| A11.2 | **F6**: a holy-order backer's succession after disbanding the order | no error.log line; Sponsor Lapse toast |

## 11. Build batches (scripter takes them in order)

**Batch 1: script fixes needing no in-game check.**
- A3 (roll list + delay);
- A4.1–A4.3;
- A5;
- A7.1 (+ the sub-mod README) and A7.2 (+ sweep rule d);
- A11.1–A11.3;
- AI: A2.1, A2.1b, A2.2 (+ `eotg_unclaimed_count`), A2.3 items 1–2, A2.4;
- the A6 pulse probe and the readout re-text.

The brief §5 FYI fixes (Back-a-Frontier cooldown, .004.a gold, .004.b prestige values, `change_government` order, the sweep's holder list) ride along: the scripter acts on them directly. Then the localizer (the batch 1 keys in §7), then QA.

**Batch 2: player-facing additions.**
- A1, built correct-either-way; its DoD waits for V8;
- A8.1–A8.3;
- A7.3, with the V-U14 AI switch as a conditional sub-item;
- A7.4;
- A2.3-opt **only if H2 is approved**.

Then the localizer, then QA.

**Batch 3: conditional on V-U1 / T14.**
- M2 if V-U1a > 0;
- M3 in the T14 form, or the fallback toast if H3 says so;
- the G3 follow-up only if the V-U1 sitting shows "Anarchy".

**Batch 4: option depth.** Stress rows and two duels, folded into event_quality B12 (§3, "Option depth").

**Loc and lore (parallel):** A9 goes to eotg-lore-keeper first, then the localizer.

## 12. Deferred

- **D4-1 New events, options and beats:** the human's call. See §14.
- **D4-2 Founder choice beyond auto-pick** (adventurers, dynasty members, merchants; design §5). It needs a candidate picker with character targets, which is new UI work. Proposal in §14.
- **D4-3 A founder as Local Ruler** (design §7): owner question H1, since it reopens Q12.
- **D4-4 Per-government local-ruler governments:** a corporate Port, a Cartel front. Waits for governments_v2 G2.
- **D4-5 Theocratic holders and castles:** the A1 proxy gives a theocrat a Military project's castle. Accepted until a theocratic mod government exists.
- **D4-6 Bands in county-modifier descriptions:** no reliable scope for data functions. Decision tooltips and .002 carry them.
- **D4-7 AI flavour events** (`frontier_v2.md` D2-3): silent rolls only for now.
- **D4-8 The cost of the explore and Raise Your Colours pickers** on the real map: both scan every Unclaimed county with a distance test. Re-measure after Gate 1 (QA §3).
- **D4-9 Research output** (technology or innovation) and **vanilla buildings on completion:** these are proposals (§14), not fixes.
- **D4-10 Narrow yearly-event triggers in M2:** added only if vanilla-scout finds an ungated path (A6).

## 13. Questions for the human

- **H1 (A1):** City and church Systems from a finished Frontier now go to a new local leader as the holder's vassal, unless the holder is seated in that holding type. That narrows your Q12 ruling ("the holder gets the new holding"). Confirm. Separately: should a founder who is not the holder become that Local Ruler instead (design §7, "House Veyra")?
- **H2 (A2.3):** You accepted "no lapse" for claimed-but-never-established counties (UQ11). With the v4 AI fixes the backlog should mostly clear on its own. Do you also want **AI-only** claims to lapse back to Unclaimed after 10 years without a Frontier? It's specified and ready; the 50-year run will show whether it's needed.
- **H3 (A6 M3):** If T14 shows only a full-file override of `00_rules.txt` works, do you accept "playable Unsworn plus a warning toast" until Gate 1 (recommended, `government_template.md` §6.2), or want the full 250-line file copied and re-diffed each patch?
- **H4 (§14):** Approve or decline each content proposal below. None is built until you do.

## 14. Proposals for the human (NOT specified as decided)

From brief §2. Each needs your approval before any spec.
1. **New events for design §11's gaps:**
   - **Positive:** population growth, a skilled settler, an infrastructure breakthrough, a trade route.
   - **Negative:** disease, hostile inhabitants, collapse, shortage. Raiders today exist only as .002 description lines.
   - **Political:** the founder disputes ownership, a religious dispute, cultural tension.
2. **Trait-gated options:** 0 of 71 options are gated today, and 14 of 36 personality traits appear, in AI weights only. Personality, education and tier option variants would follow the event_quality §12 pairing rules.
3. **Founder choice** (design §5): a picker offering adventurers, dynasty members and merchants as founders, not only the best courtier or the holder.
4. **Research projects yield a technology or innovation** (cultural innovation progress for the holder's culture).
5. **Vanilla buildings placed on completion**, beyond holdings and modifiers.
6. **A .005 "Lead it yourself" option**, as .002(e) offers.

---

### HANDOFF
- status: done
- next: eotg-scripter (batch 1), with eotg-lore-keeper on A9 in parallel
- ask: Build batch 1 of `docs/specs/frontier_v4.md` §11 (A3, A4, A5, A7.1–7.2, A11, the AI items of A2, and the A6 pulse probe), plus the brief §5 FYI fixes. Then hand the batch-1 loc keys to the localizer and the result to QA. Batch 2 follows; batch 3 waits for V-U1a/b and T14.
- files: docs/specs/frontier_v4.md (new); pointer notes in docs/specs/frontier_v1.md, frontier_v2.md, frontier_v3.md, frontier_unclaimed_regions.md (incl. new §21 coupling record), governments_v2.md
- needs-loc: §7. Batch 1: `eotg_decision_frontier_appoint_founder` (+`_desc`, `_confirm`, `_pick_tt`, `_effect_tt`), `eotg_unclaimed_debug_pulsed_tt`, re-text of `eotg_unclaimed_debug_playable_tt`. Batch 2: `eotg_frontier.004.local_ruler_tt`, 17 `eotg_frontier_band_*_tt`, `eotg_frontier_toast_backing_settled`, `eotg_decision_unclaimed_raise_colours` (+`_desc`, `_confirm`, `_pick_tt`), `eotg_unclaimed_claim_cooldown_tt`, `eotg_unclaimed_defender_tt`. Batch 3: `EOTG_GAME_OVER_CANNOT_PLAY_UNSWORN` + `NOT_` form, or `eotg_unclaimed_toast_unplayable`. Batch 4: `.032.c_success/_failure`, `.033.c_success/_failure`. A9 re-texts after the lore ruling.
- needs-lore: (1) who owns "pressure" (A9.1, with void_lift_plan_cloud.md §3c); recommendation: no system owns it, Frontier says "strain". (2) "Frontier Roots" for the five legacy modifiers. (3) Whether vanilla "Republic"/"Theocracy" labels on the new local vassals read acceptably at 866 (display only).
- needs-human: H1 (A1 narrows Q12; founder as Local Ruler?), H2 (AI-only claim lapse, reopens UQ11), H3 (M3 fallback if T14 fails), H4 (§14 content proposals). In-game, in order: link the Frontier test sub-mod (QA H2), V-U1a (pulse probe, after batch 1), V-U1b + T14, V8, V-U14, V-U9/V-U8, V-U15, U2, then the 50-year AI observer run. Orchestrator: add `common/scripted_rules/` to CLAUDE.md placement when M3 is built; add the new override keys to docs/pitfalls.md §16.
