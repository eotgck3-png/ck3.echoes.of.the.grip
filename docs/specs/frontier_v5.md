# Spec: Frontier Systems v5 (owner ruling H4: approved content)

Term update 2026-10-20: player-facing county term is Shoal (was Region).

**Author:** eotg-architect, 2026-10-12; round 2 (§3.6, §3.7, batch 5E) added 2026-10-18. **Status:** ruled; 5A–5D built, 5E specified, not built.
**Ruling:** owner H4, 2026-10-12, recorded in [`frontier_v4.md`](frontier_v4.md) §13/§14.
**Amends:** [`frontier_v4.md`](frontier_v4.md) §A5 (the .005 AI order gains option e) and §12 (D4-9 moves into scope). Where they disagree, **this spec wins**. Everything else in v1–v4 and [`frontier_unclaimed_regions.md`](frontier_unclaimed_regions.md) still binds.
**Builds on:** v4 batches 1, 2 and 4, all committed (`01f6422`, `627423a`, `b1c0432`). Batch 4 added the response stress rows (.005.a, .031.a, .032.b, .033.a, .033.b, .034.b) and the duels on .032.c and .033.c. This spec keeps all of them.
**House rules:** [`event_quality_v1.md`](event_quality_v1.md) §12 (voice, quotes) and §13 (re-gating rubric) apply to every option and line below.
**Inputs for §3.4 and §3.5:** the eotg-lore-keeper's canon constraints for round 1 and the eotg-vanilla-scout building check, both relayed by the orchestrator on 2026-10-12 and quoted where used.
**Vanilla:** CK3 **1.20.0.4** (`launcher-settings.json` rawVersion). `G` = `D:/SteamLibrary/steamapps/common/Crusader Kings III/game`. Every vanilla line cited below was re-checked in this session.

---

## 0. Rulings at a glance

| # (§14) | Item | Owner | Here | Batch |
|---|---|---|---|---|
| 6 | .005 "Lead it yourself" (option e) | approved | §3.1 | 5A |
| 4 | Research projects yield cultural fascination progress for the holder's culture | approved | §3.2 | 5A |
| 2 | Trait-gated options: 14 new gated options on 12 existing events (6 personality, 6 education, 2 tier) | approved | §3.3 | 5B |
| 1 | New events, **round 1**: seven events, .050–.056 (sickness, the people already there, collapse, shortage, the founder's claim, two chapels, separate berths) | approved; lore input received | §3.4 | 5C |
| 1 | New events, **round 2**: four positive events, .057–.060 (population growth, a skilled settler, an infrastructure breakthrough, a trade route), plus the Seamless guard on the roll | approved; lore input received 2026-10-18 | §3.6, §3.7 | 5E |
| 5 | Vanilla buildings placed on completion | approved; scout check passed | §3.5 | 5D |
| 3 | Founder choice picker | deferred | D4-2 (unchanged) | — |

**Option count in `events/eotg_frontier_events.txt`:** 71 before v5. After 5A it is 72, after 5B 86, after 5C 114 (86 + 28 in the seven new events), and after 5E 130 (+16 in the four round-2 events).

---

## 1. Purpose & gate

H4 approved new content for Frontier Systems. This spec covers all of it. It adds:
- one option on .005;
- one completion reward;
- trait, education and tier variety on the existing events;
- seven new events in round 1 and four positive events in round 2 (§3.6, added 2026-10-18);
- buildings on completion;
- a Seamless guard on the flavour roll (§3.7).

**Gate 3 (Systems)**, built under the **mod-exclusive exemption** (CLAUDE.md, decided 2026-10-02). **Not blocked by Gate 1.** Everything stays map-agnostic:
- no `title:`, `province:`, `culture:`, `faith:` or `character:` references;
- the culture and faith checks in §3.4 compare scopes and never name one;
- the buildings in §3.5 are vanilla keys, which exist on any map.

**Scope rule from the owner:** #6 and #2 add **options only**. The only new events are the seven round-1 events in §3.4 and the four round-2 events in §3.6, all approved by the owner (H4, 2026-10-12). No beats, follow-ups or chains beyond what is written here.

**Mod-exclusive check for §3.7:** the Seamless guard reads a mod trait (`eotg_total_integration`), which is not a title, province, character, culture or faith. It is map-agnostic (§3.7).

## 2. Signature resource

Unchanged: `eotg_frontier_progress` (hidden, 0–100, county variable) and its strain value `eotg_frontier_strain` (hidden, 0–8).

**How v5 touches them:**
- **Every new option** in §3.1, §3.3 and §3.4 moves progress or strain (a stricter rule than invariant 5, which binds only per event). The only exceptions are the ungated "moment has passed" exits, which exist already.
- **The seven round-1 events and the four round-2 events** each move strain or progress in every option (§3.4 and §3.6 tables).
- **The Seamless guard (§3.7)** routes a Seamless player's roll to the silent roll, which moves progress or strain in every branch (`eotg_frontier_ai_silent_roll_effect`), so a Seamless Frontier still lives.
- **#4 and #5** are completion rewards. They run inside `eotg_frontier_complete_effect`, which runs only at completion (progress and floors met), so they read the resource by construction.
- **One new strain cause, `dispute`** (§3.4.1), for the three political events. It feeds the same 0–8 strain and gets its own band line and .005 description line, so failure still names its cause (`frontier_v1.md` §6.3).
- **Hidden-value rule** (`frontier_v1.md` §R): every new tooltip is in words. No number for progress or strain.

---

## 3. Items

### 3.1 #6: .005 "Lead it yourself" (option e)

**What .002.e does today** (`events/eotg_frontier_events.txt:492-509`): in the Without a Founder variant, `eotg_frontier_set_founder_effect = { FOUNDER = root }`, `custom_tooltip = eotg_frontier.002.founder_tt`, AI base 30 (+20 diligent). It is free and changes nothing else.

**Why .005 needs more than a copy.** .005 fires at strain 8 (`eotg_frontier_strain_fail_value`, `common/script_values/eotg_frontier_values.txt:243-245`). An option that only sets the founder would leave strain at 8, and the next tick would fire .005 again. So .005.e mirrors **.005.b** ("New hands", `:975-1016`): set the founder, then `eotg_frontier_restart_effect` (half the progress stays, and strain goes to 4; `common/scripted_effects/eotg_frontier_effects.txt:1489-1503`). The difference is who leads and what it costs: b costs `minor_gold_value` and brings in the best steward, while e costs the ruler's own time, which is shown as stress.

**The option** (insert after .005.b, before .005.c):

| Field | Value |
|---|---|
| `name` | `eotg_frontier.005.e` |
| `trigger` | `scope:eotg_frontier_county = { eotg_frontier_is_frontier = yes  var:eotg_frontier_strain >= eotg_frontier_strain_fail_value  NOT = { var:eotg_frontier_founder ?= root } }`, plus `is_adult = yes` and `is_imprisoned = no` on root |
| effects | `scope:eotg_frontier_county = { eotg_frontier_set_founder_effect = { FOUNDER = root }  eotg_frontier_restart_effect = yes }`; `add_stress = minor_stress_gain` (`G/common/script_values/00_stress_values.txt:6`); `custom_tooltip = eotg_frontier.005.lead_tt` |
| `stress_impact` (response rows, no icon; §13.1 step 4) | `diligent = minor_stress_impact_loss`; `lazy = medium_stress_impact_gain`; `content = minor_stress_impact_gain` |
| `ai_chance` | `base = 0`; `modifier = { add = 40  OR = { has_trait = diligent  has_trait = ambitious } }`; plus the **same two `factor = 0` gates as .005.b's sponsor gate** (a backer who can pay double means the AI takes d) |

**Why the adult and free check.** `eotg_frontier_has_valid_founder` requires the founder to be adult and free (`common/scripted_triggers/eotg_frontier_triggers.txt:65-80`). A child or imprisoned ruler named as founder would be invalid on the next tick, and the Frontier would take `no_founder` strain at once.
- **Ride-along fix:** .002.e lacks this check. Add `is_adult = yes` and `is_imprisoned = no` to its trigger in the same batch. That is a bug fix, not a new beat.

**A1 interaction (founder first, H1).** When root is the founder, `eotg_frontier_founder_can_rule` already fails ("the holder" row of its edge-case table, `eotg_frontier_triggers.txt:86-97`), so a city or church System goes to the created figure. The localizer must not claim that leading it yourself makes the System yours.

**Amendment to v4 §A5 (the AI order).** d; else b if gold ≥ 2× minor; else **e (weight 40) against a (weight 10), and e only if root is diligent or ambitious**; the AI never picks c.
- A trait-less AI still abandons as before.
- Option a's weights are unchanged.
- Static check: the `ai_chance` blocks match this paragraph.

### 3.2 #4: Research projects advance the holder's culture's fascination

**The vanilla effect, verified.** Vanilla has two culture-scope effects:
1. `add_innovation_progress = { value = … target = <innovation> }` needs a **named innovation target** (`G/events/dlc/tgp/tgp_tribute_mission_events.txt:1063-1066`; picked by `tribute_mission_1000_set_innovation_reward_effect`, `:884-906`). Picking a target means either naming an innovation (not map-agnostic) or writing an eligibility picker. **Rejected.**
2. `add_fascination_progress = <value>` advances whatever innovation the culture is **currently fascinated by**. It names nothing, so it fits a map-agnostic system. **Chosen.**

**Vanilla shape copied:** the Cathedral great project's contribution (`G/common/great_projects/types/01_pam_projects.txt:617-632`):
- `culture = { culture_has_any_fascination = yes }`, then `custom_tooltip = { text = … culture = { add_fascination_progress = 5 } }`;
- `else = { add_stewardship_lifestyle_xp = major_lifestyle_xp }`.

The tribute mission falls back the same way: fascination progress when no innovation target exists (`tgp_tribute_mission_events.txt:1051-1068`).

**Units and amount.** The value is in percent of the innovation: vanilla loc renders `add_spread_progress_global` as `$VALUE|V0%$` (`G/localization/english/effects_l_english.yml:1869`), and `add_fascination_progress` points at the same string (`:1877`). Vanilla sizes:

| Source | Amount | File:line |
|---|---|---|
| Cathedral contribution (one stage of a great project) | 5 | `01_pam_projects.txt:627` |
| Tribute mission reward | 5 (`tribute_reward_fascination_progress_value`) | `G/common/script_values/tgp_tribute_mission_values.txt:20` |
| "Invest!" in a dynastic-cycle event (one option) | 2.5 | `G/events/dlc/tgp/tgp_dynastic_cycle_flavor_events.txt:818` |
| Architect bonus | 5 | `G/events/dlc/tgp/tgp_movement_events.txt:511` |

A Research Frontier runs for decades, can fail, and pays out once. **Amount: 10** (twice a single great-project contribution), **+5** when the Shoal holds a Research Facility, Ancient Ruins or Anomalous (the existing `eotg_frontier_mod_legacy_learning` condition minus the type check, `eotg_frontier_effects.txt:1798-1808`). That is 15 at most, three vanilla contributions. The fallback (no fascination) is `add_learning_lifestyle_xp = major_lifestyle_xp` (300, `G/common/script_values/00_lifestyle_values.txt:9`), the Cathedral's fallback with the research skill swapped in.

**Script.**
- **New script value** `eotg_frontier_research_fascination_value` (COUNTY scope): `value = 10`, then `if = { limit = { OR = { has_county_modifier = eotg_frontier_infra_research_facility  has_county_modifier = eotg_frontier_trait_ancient_ruins  has_county_modifier = eotg_frontier_trait_anomalous } } add = 5 }`.
- **New scripted effect** `eotg_frontier_research_fascination_effect` (COUNTY scope; needs `scope:eotg_frontier_holder`, which `eotg_frontier_complete_effect` saves at `:1059`):
  1. `save_temporary_scope_value_as = { name = eotg_frontier_fascination  value = eotg_frontier_research_fascination_value }`. The value is evaluated in the county, because the culture scope cannot read county modifiers. This is the purse pattern of .004.a (`events/eotg_frontier_events.txt:770`).
  2. `scope:eotg_frontier_holder = { if = { limit = { culture = { culture_has_any_fascination = yes } }  custom_tooltip = { text = eotg_frontier_research_fascination_tt  culture = { add_fascination_progress = scope:eotg_frontier_fascination } } }  else = { add_learning_lifestyle_xp = major_lifestyle_xp } }`
- **Call site:** the `flag:research` branch of `eotg_frontier_complete_effect` (`eotg_frontier_effects.txt:1118-1125`), after the founder's `add_learning_skill`. That effect runs for player and AI completions alike (.004 fires for every holder, `:743`), so AI research Frontiers advance their cultures too.
- **Whose culture:** the **holder's** (`scope:eotg_frontier_holder.culture`), never the county's and never the founder's. The holder paid for it.

**Dependency: CB-36** (taskboard; lore ruling 2026-10-12). #4 has no script guard against advancing `eotg_innovation_self_repairing_machinery`; its era gate (`culture_era_early_medieval`, `eotg_innovations.txt:29`; AI ×0 below it, `:39-48`) is what keeps it ahead of the 866 cultures, and that holds only while they start tribal. If CB-36 moves the 866 cultures into the early medieval era, CB-36 must re-point the gate (as `eotg_innovations.txt:15-17` already says); #4 needs no change.

**Farming check.** Completion ends the Frontier (`eotg_frontier_settle_effect`), so the reward fires once per completed project. Restart (.005.b/e) keeps the project and pays nothing. There are no milestone payouts, by design: abandon-and-restart around a milestone would farm them, which is the v1 Q5 problem.

### 3.3 #2: Trait-gated options (event_quality §13.1 steps 1–10)

**Starting point (step 1, inventory).** 0 of 71 options are gated on a root trait. Today:
- .001.f gates on the `learning` skill;
- .032.c gates on the `diplomacy` skill;
- .033.c gates on gold.

Fourteen personality traits appear, in `ai_chance` and animations only. The batch-4 response rows are on ungated options. Steps 2–4 (keep one personality gate, re-axis the others, move stress) therefore have nothing to re-gate. What #2 adds is **new gated options**, one personality gate per event at most. Existing options and their effects are unchanged.

**Out of scope, with reasons:**
- **.001 (project type), .021 (what to build), .010 (whom to back):** structural menus. A gated variant would be a project type or building only some rulers can choose.
- **.020 and .042 (reports from decisions):** two options each. The skill gate on .042.b's AI weight is enough.
- **.004 (completion):** its options decide only the founder's reward, and #5 and #4 add to its outcome.
- **.037 (a follow-up to .035.a):** one reachable beat.

These stay ungated, which the spread rule (step 6) allows.

**The new options** (letters continue each event's sequence; every trigger also repeats the event's Shoal-state check, as the sibling options do):

| Option | Axis and gate | Text intent (localizer writes) | Effects | Stress (step 5) | AI |
|---|---|---|---|---|---|
| `.002.g` | **personality** `patient` (`trait = patient`, `has_trait`); valid founder | Slow the work and wait the year out | strain −1 (`eotg_frontier_ease_strain_effect`); progress −2; `custom_tooltip = eotg_frontier.002.g_tt` | `patient = minor_stress_impact_loss` | base 30 |
| `.002.h` | **education** `education_stewardship`, `skill = stewardship`; valid founder | Recut the ration ledger | `remove_short_term_gold = tiny_gold_value` (`G/common/script_values/01_dynamic_values.txt:13`); strain −1; `eotg_frontier.002.ease_tt` | — | base 30; +10/+20/+20 for `education_stewardship_3/_4/_5` |
| `.003.c` | **education** `education_intrigue`, `skill = intrigue`; as .003.a | Accept, once I know what they would rather keep quiet | as .003.a (set sponsor, progress +3, toast) **plus** strain −1; `accept_tt` + `ease_tt` | — | as .003.a's opinion modifiers; +10/+20/+20 by tier |
| `.005.f` | **tier** `highest_held_title_tier >= tier_duchy`; `prestige >= medium_prestige_value`; strain at failure | Order my vassals' crews in | `add_prestige = { value = medium_prestige_value multiply = -1 }` (`G/common/script_values/00_basic_values.txt:1002`); strain −3 (three ease calls; 8 → 5); progress unchanged; `custom_tooltip = eotg_frontier.005.f_tt` | — | base 10; −10 each for `shy`, `content`, `craven` (§13.1 step 3b) |
| `.030.c` | **education** `education_diplomacy`, `skill = diplomacy`; valid sponsor; rival exists | Let each backer hear what the other offered | keep the current backer; current backer `add_opinion eotg_frontier_opinion_pleased` (10 years); strain −1; progress +2; `custom_tooltip = eotg_frontier.030.c_tt` | — | base 30; +10/+20/+20 by tier |
| `.031.d` | **personality** `deceitful` | Promise them a say, and let the promise lapse | progress +2; sponsor pleased (10 years); `custom_tooltip = eotg_frontier.031.no_say_tt` (existing: the backer gains no say) | `deceitful = minor_stress_impact_loss` | base 20 |
| `.032.e` | **tier** `highest_held_title_tier >= tier_duchy`; settlers variant only (`NOT = { exists = scope:eotg_frontier_overlord }`) | Remind them whose Shoal this is | strain −1; progress −1; `add_dread = minor_dread_gain` (`00_basic_values.txt:731`); `custom_tooltip = eotg_frontier.032.e_tt` | — | base 10; −10 each for `shy`, `content`, `craven` |
| `.033.d` | **personality** `impatient` | Both camps work double shifts until it is done | progress +5; strain +1 (`CAUSE = hardship`); `eotg_frontier.002.push_tt` | `impatient = minor_stress_impact_loss` | base 30 |
| `.034.d` | **education** `education_martial`, `skill = martial` | Send an armed party to recover what can be saved | progress −1; no strain; `custom_tooltip = eotg_frontier.034.d_tt` | — | base 30; +10/+20/+20 by tier |
| `.034.e` | **personality** `temperate` | Cut every ration, mine first | strain +1 (`hardship`); progress unchanged; `custom_tooltip = eotg_frontier.034.e_tt` | `temperate = minor_stress_impact_loss` | base 30 |
| `.035.d` | **education** `education_learning`, `skill = learning`; ruins variant (`scope:eotg_frontier_found ?= flag:ruins`) | Catalogue it before anyone touches it | as .035.a (Ancient Ruins trait, the .037 follow-up) but progress **+4** on a Research project and **+1** otherwise (a: +3 / −2); `eotg_frontier.035.a_tt` | — | base 30; +10/+20/+20 by tier |
| `.036.c` | **personality** `content` | Take what the crews need, and leave the rest | progress +2; strain −1; no trait; `custom_tooltip = eotg_frontier.036.c_tt` | `content = minor_stress_impact_loss` | base 30 |
| `.040.d` | **education** `education_martial`, `skill = martial`; company exists; .040's pool condition (Dangerous, or Military with no backer) | Drill the settlers and hold it ourselves | strain −1; progress −1; no fee; `custom_tooltip = eotg_frontier.040.d_tt` | — | base 30; +10/+20/+20 by tier |
| `.041.d` | **personality** `zealous`; faith backer exists | Lead the first rite there myself | `add_piety = minor_piety_value`; strain −1; progress +2; `custom_tooltip = eotg_frontier.041.d_tt` | `zealous = minor_stress_impact_loss` | base 30 |

**Step 5, pairing:** each personality option carries the `trait =` icon, the `has_trait` trigger and a stress row for that trait, as `G/events/dlc/ep2/wedding_events/ep2_wedding_events_ewan.txt:3759-3778` does (shy: `trigger`, `trait`, a stress entry). Education and tier options get **no icon** (§13.1 step 3a/3b). Education options use `skill = <skill>`, as the mod's B1 precedent does (`events/eotg_augmentation_activities.txt:469-481`).

**Step 6, spread** (this file, after 5B):
- 6 personality, 6 education and 2 tier gates.
- Education by skill: stewardship 1, intrigue 1, diplomacy 1, martial 2, learning 1. The largest share is 33%, under 50%.
- The file has ≥ 5 gated options, at least one education gate and at least one tier gate. **Holds.**
- **After 5C** (§3.4 adds 6 personality, 4 education and 1 tier gate): education is stewardship 2, intrigue 1, diplomacy 2, martial 2, learning 3, so the largest share is 30%. **Still holds.**

**At most one personality gate per event:** holds. The six #2 personality gates are on six different events (.002, .031, .033, .034, .036, .041), and round 1 puts one on each of six events. No L017 floor exception is needed (step 9).

**Step 8, coverage floor:** gates are only added, so no trait's count falls. Four of the eight thin-coverage traits (`trait_coverage.py` "gated" ≤ 3 on 2026-10-08: patient, impatient, content, temperate) gain a gate here, and `arbitrary` gains one in §3.4. The choices follow step 2(b): where two traits fit the text equally, the thinner one was picked.

**Step 7, text:** the localizer writes each option against **every** desc variant of its event:
- .002: the founder variants (g and h require a valid founder, so they never show in Without a Founder);
- .003: `desc_replace`;
- .034: Dangerous and Remote;
- .035: ruins only (d is ruins-gated);
- .041: head, order and none (d requires a backer, so never none).

Options are first person or imperative (§12.1 rule 8). No numbers.

**Step 10, close-out:** the 5B batch report lists the stress rows **added** (six: one per personality pairing above; .005.e's three response rows are reported under 5A) and **moved** (none). Then regenerate the L017 baseline (`docs/tools/eotg_lint_baseline.json` via `docs/tools/eotg_lint.py`) and rerun `docs/tools/eotg_event_quality.py --event` for the frontier file. The report shows the `\byou\b` grep over the new loc.

### 3.4 #1 round 1: seven new events (.050–.056)

**Owner approval:** 2026-10-12. **Lore input:** eotg-lore-keeper constraints, relayed 2026-10-12 (§8 quotes them).

#### 3.4.1 Shared rules for all seven

- **Shape:** `type = character_event`, `theme = realm`, an `override_background` from `event_quality_v1.md` §14.1 (named per event), and a `left_portrait = root` with W6 `triggered_animation`s. Add a `right_portrait` where a named character speaks. Copy the shape of .034 (`events/eotg_frontier_events.txt:2156-2257`).
- **Trigger:** world state only, never a cooldown:
  - `exists = scope:eotg_frontier_county`;
  - `scope:eotg_frontier_county = { holder ?= root  eotg_frontier_is_frontier = yes … }`. The `holder ?= root` re-check is v4 QA F1, because the roll delays the event by 1–120 days;
  - plus each event's own condition (the tables below).
- **`immediate`:** re-derive the scopes the event needs. Set `scope:eotg_frontier_founder` from `var:eotg_frontier_founder`, as .004 does at `:746-755`, so the events also work fired from the console.
- **Options:** every gated option repeats `eotg_frontier_is_frontier = yes`. The **last option is ungated** and guards its own effects with `if = { limit = { eotg_frontier_is_frontier = yes } … }` (the qa_noopt rule, `:429-432`). Every option moves strain or progress (§2).
- **Gates follow §3.3:**
  - at most one personality gate per event, paired with its icon and stress row;
  - education gates carry `skill =` and the `_3/_4/_5` AI tiers;
  - tier gates carry no icon, AI base 10 and counter-trait negatives;
  - ungated options carry response stress rows (§13.1 step 4).
- **Voice (§12.1):** main desc first person, present tense; appended variants neutral or third person, carrying I/me/my where they refer to root (rule 13); at most one NPC line per desc, in unescaped double quotes (§12.2), true for every character the scope can resolve to (rule 14). Canadian English. No dashes.
- **New strain cause `dispute`** (political events .054–.056), handled like the existing causes:
  - `eotg_frontier_add_strain_effect = { CAUSE = dispute }`;
  - a new `else_if` in `eotg_frontier_legibility_tooltip_effect`'s cause chain (`eotg_frontier_effects.txt:636-664`) → `eotg_frontier_band_cause_dispute_tt`;
  - a new `triggered_desc` in .005's cause list (`events/eotg_frontier_events.txt:847-874`) → `eotg_frontier.005.desc_dispute`, inserted before the hardship default.

  The physical events use existing causes: sickness, collapse and shortage are `hardship`; the people already there are `danger`.
- **No new modifiers, templates, opinion modifiers or art.** The events reuse `eotg_frontier_mod_hard_year` and the existing opinion modifiers (`eotg_frontier_opinion_pleased` / `_slighted`). The `trait =` icons are vanilla.

#### 3.4.2 Wiring

Seven new entries in `eotg_frontier_flavor_pick_effect`'s `random_list` (`common/scripted_effects/eotg_frontier_effects.txt:1861-1966`). Each one is `holder = { trigger_event = { id = eotg_frontier.05x  days = { 1 120 } } }`, matching every sibling. **Cooldown authority stays in the roll** (`eotg_frontier_event_cd` and the one-roll-per-ruler list, v4 A3). No event trigger reads either.

| Event | Roll weight | Roll `trigger` (eligibility) |
|---|---|---|
| .050 | 10; +10 `eotg_frontier_trait_hostile` without `eotg_frontier_infra_orbital_station`; +5 progress ≥ 33 | none |
| .051 | 5; +10 `eotg_frontier_trait_dangerous`; −5 Dangerous with `eotg_frontier_infra_garrison_post`; −5 Dangerous with `eotg_frontier_mod_merc_escort` (the A11.3 counter pattern; floor 5) | none |
| .052 | 5; +5 progress ≥ 66; +5 Hostile without an Orbital Station | progress ≥ 20 (something to collapse) |
| .053 | 10; +10 `eotg_frontier_trait_remote`; −5 Remote with `eotg_frontier_infra_navigation_beacon`; +5 no `var:eotg_frontier_sponsor` | none |
| .054 | 10 | `eotg_frontier_has_valid_founder = yes`; `NOT = { holder = var:eotg_frontier_founder }`; progress ≥ 50 |
| .055 | 10; +10 `var:eotg_frontier_type ?= flag:religious` | `eotg_frontier_faiths_differ = yes` (below) |
| .056 | 10; +5 `var:eotg_frontier_type ?= flag:settlement` | `eotg_frontier_cultures_differ = yes` (below) |

**Two new scripted triggers** (COUNTY scope; map-agnostic, comparing scopes only):
- `eotg_frontier_faiths_differ`: `OR = { NOT = { faith = holder.faith }  AND = { eotg_frontier_has_valid_founder = yes  var:eotg_frontier_founder = { NOT = { faith = prev.faith } } } }`. The second `prev` is the county, one step up, which is the pattern of `eotg_frontier_has_valid_founder`.
- `eotg_frontier_cultures_differ`: the same with `culture`.

The events repeat these in their own `trigger` (world state, not cooldown), so a conversion during the delay voids the event.

**AI:** unchanged. AI Frontiers get silent rolls only (v4 A2.4, D4-7), so the new events are player-facing. The `ai_chance` blocks still exist, for the AI-controlled-player edge case and for completeness.

#### 3.4.3 The events

Weights and triggers are in §3.4.2. "S" = strain, "P" = progress. Every option's text is written by the localizer from the intent and the lore voice line.

**eotg_frontier.050: Sickness in the Berths** (disease; `eotg_bg_clinic`)
- **desc:** habitat sickness: fouled recycled water, bad air from failing scrubbers, or a fever in crowded berths.
  - `desc_hostile`: the Shoal is Hostile, and the air itself is part of it.
  - Voice line (lore): "The scrubbers on the lower decks failed a month ago, and now the coughing has spread to every berth."

| Opt | Gate | Intent | Effects | Stress | AI |
|---|---|---|---|---|---|
| a | `gold >= minor_gold_value` | Seal a quarantine berth and pay the medics | −`minor_gold_value`; P −1; `.050.a_tt` | — | 40, −20 greedy |
| b | education `education_learning` | Trace it to the scrubbers myself | S −1; `.002.ease_tt` | — | 30 + tiers |
| c | ungated (guarded) | Keep the crews working | P +2; S +1 `hardship`; `.002.push_tt` | `compassionate = medium_stress_impact_gain`; `callous = minor_stress_impact_loss` | 20 |

**eotg_frontier.051: The Ones Who Were Here First** (hostile inhabitants; `eotg_bg_field_camp`)
- **desc:** the people already living in the Shoal (a few hardy families, or raiders working out of it) have turned on the camp. No named group and no species.
  - `desc_dangerous`: the Shoal was known to be Dangerous.
  - Voice line (lore): "The families who were here first have stopped trading with us, and last night they cut the beacon's power line."

| Opt | Gate | Intent | Effects | Stress | AI |
|---|---|---|---|---|---|
| a | `gold >= minor_gold_value` | Trade with them, not orders | −`minor_gold_value`; S −1; `.002.ease_tt` | — | 30 |
| b | personality `forgiving` | Forget the cut line; offer them berths in the camp | S −1; P +1; `.051.b_tt` | `forgiving = minor_stress_impact_loss` | 30 |
| c | tier `>= tier_duchy`; `prestige >= minor_prestige_value` | Send my own soldiers to hold the line | −`minor_prestige_value`; S −1; P +1; `.051.c_tt` | — | 10; −10 craven, content, shy |
| d | ungated (guarded) | Guard the line and keep building | P +2; S +1 `danger`; `.002.push_tt` | `wrathful = minor_stress_impact_loss`; `compassionate = minor_stress_impact_gain` | 20 |

**eotg_frontier.052: The Frame Is Cracking** (collapse; `eotg_bg_field_camp`)
- **desc:** structural failure: seals giving, a section losing pressure, the frame cracking. No self-repairing machinery.
  - `desc_late`: progress ≥ 66; the oldest sections were built fastest.
  - Voice line (lore): "Half the habitat ring has lost pressure, and the crews say the frame itself is cracking."

| Opt | Gate | Intent | Effects | Stress | AI |
|---|---|---|---|---|---|
| a | — (Shoal check only) | Evacuate the section and rebuild it right | P −4; S −1; `.052.a_tt` | — | 30 |
| b | personality `diligent` | I will walk the frame with the crews myself | P −2; S −1; `.052.a_tt` | `diligent = minor_stress_impact_loss` | 30 |
| c | education `education_stewardship` | Salvage the frame and reroute the crews | P −1; `.052.c_tt` | — | 30 + tiers |
| d | ungated (guarded) | Shore it up and keep the crews inside | P +1; S +1 `hardship`; `.002.push_tt` | `compassionate = medium_stress_impact_gain`; `callous = minor_stress_impact_loss` | 20 |

**eotg_frontier.053: Patched Seals** (shortage; `eotg_bg_barren_world`)
- **desc:** air, water, ice, spare parts or fuel running short.
  - `desc_remote`: the Shoal is Remote, and the next run is far off.
  - Voice line (lore): "We are patching seals with seals we already patched once."

| Opt | Gate | Intent | Effects | Stress | AI |
|---|---|---|---|---|---|
| a | `gold >= minor_gold_value × 2` | Buy what we lack, whatever it costs | −(`minor_gold_value` × 2); S −1; P +1; `.053.a_tt` | — | 30, −20 greedy |
| b | valid sponsor who can pay `eotg_frontier_sponsor_payment_value` | Our backer covers it | sponsor pays; S −1; `.002.ease_tt` (shape: .034.c) | — | 40 |
| c | personality `generous`; `gold >= minor_gold_value` | Open my own stores to the crews | −`minor_gold_value`; S −1; P +1; `.053.c_tt` | `generous = minor_stress_impact_loss` | 30 |
| d | ungated (guarded) | Ration it | S +1 `hardship`; `eotg_frontier_mod_hard_year` 2 years; `.053.d_tt` | `gluttonous = minor_stress_impact_gain`; `temperate = minor_stress_impact_loss` | 20 |

**eotg_frontier.054: Whose Systems Are These?** (the founder disputes ownership; `eotg_bg_council`; right portrait: the founder)
- **desc:** the founder presses for more: a vassal's claim argued under the holder's own law. No court, arbiter or outside authority exists.
  - `desc_ruler`: shown when `eotg_frontier_founder_can_rule` holds for the type's holding, so the founder already stands to hold the System under A1.
  - Voice line (lore, the founder's one spoken line): "[eotg_frontier_founder.GetName] says the Systems were built with [eotg_frontier_founder.GetHerHis] sweat, not my coin."

| Opt | Gate | Intent | Effects | Stress | AI |
|---|---|---|---|---|---|
| a | founder `is_landed = no`; `var:eotg_frontier_type` is settlement, trade or religious | The System will be theirs to hold, under me | founder `eotg_frontier_opinion_pleased` (10 years); S −1; `.054.a_tt` (conditional: if they still lead it at completion; A1 founder first) | — | 30 |
| b | `gold >= minor_gold_value` | A purse, and back to work | purse to the founder (the .004.a pattern, `:770-772`); founder pleased; P +2; `.054.b_tt` | — | 30, −20 greedy |
| c | personality `arbitrary` | What I gave, I can give to another | founder `eotg_frontier_opinion_slighted` (10 years); `add_dread = minor_dread_gain`; S −1; `.054.c_tt` | `arbitrary = minor_stress_impact_loss` | 30 |
| d | ungated (guarded) | The coin was mine, and so is the Shoal | founder slighted (if alive); S +1 `dispute`; `.054.d_tt` | `humble = minor_stress_impact_gain`; `arrogant = minor_stress_impact_loss` | 20 |

**Text constraint (a):** the tooltip must not promise the System outright. If the founder is invalid at completion, A1 gives it to the created figure, so the line is conditional ("if [eotg_frontier_founder.GetSheHe] still leads it when the work is done").

**eotg_frontier.055: Two Chapels** (religious dispute; `eotg_bg_council`, because `temple*` backgrounds are rejected in §14.1)
- **desc:** settlers of different faiths will not share a chapel. Scoped faiths only, and never a name. Zeal is rising.
  - `desc_founder`: the founder's faith differs from the settlers'.
  - `desc_county`: the Shoal's faith differs from mine.
  - Voice line (lore): "The settlers will not share a chapel with the crews who came with the second convoy."

| Opt | Gate | Intent | Effects | Stress | AI |
|---|---|---|---|---|---|
| a | — | One chapel, shared by rota | S −1; P −1; `.055.a_tt` | — | 30 |
| b | education `education_learning` | Hear both sides and write the rota myself | S −1; P +1; `.002.ease_tt` | — | 30 + tiers |
| c | personality `cynical`; `gold >= minor_gold_value` | Build two chapels and end the argument | −`minor_gold_value`; S −2; `.055.c_tt` | `cynical = minor_stress_impact_loss` | 30 |
| d | ungated (guarded) | My faith keeps the chapel | `add_piety = minor_piety_value`; S +1 `dispute`; `.055.d_tt` | `zealous = minor_stress_impact_loss`; `compassionate = minor_stress_impact_gain` | 20, +20 zealous |

**eotg_frontier.056: Their Own Berths** (cultural tension; `eotg_bg_field_camp`)
- **desc:** settler groups keep apart: their own berths, songs and grudges. No species and no "human". The Exodus brings newcomers, but the event does not name it.
  - `desc_founder`: the founder's culture differs from the settlers'.
  - `desc_county`: the Shoal's culture differs from mine.
  - Voice line (lore): "The newcomers keep their own berths, their own songs and their own grudges."

| Opt | Gate | Intent | Effects | Stress | AI |
|---|---|---|---|---|---|
| a | — | Let them keep their own berths | S −1; P −1; `.056.a_tt` | — | 30 |
| b | education `education_diplomacy` | Find the words both camps will hear | S −1; P +1; `.002.ease_tt` | — | 30 + tiers |
| c | personality `just` | One rule for every berth, enforced the same | S −1; P +1; `.056.c_tt` | `just = minor_stress_impact_loss` | 30 |
| d | ungated (guarded) | One roster, one berth list, starting now | P +2; S +1 `dispute`; `.056.d_tt` | `compassionate = minor_stress_impact_gain`; `stubborn = minor_stress_impact_loss` | 20 |

**Vanilla culture handling** (`docs/design/frontier_systems.md:625-645`): .056 changes no culture. Long-term drift stays vanilla's.

### 3.5 #5: Vanilla buildings on completion

**Scout verdict (2026-10-12): workable.** Re-checked here:
- **Effect:** `add_building = <key>` in province scope.
- **Slot guard:** vanilla `upgrade_farm_building` (`G/common/scripted_effects/01_building_upgrade_effects.txt:7-22`) adds `extra_building_slot` (`G/common/modifiers/00_province_modifiers.txt:173-176`, `building_slot_add = 1`, stacking) when `free_building_slots = 0` and the building is missing, then calls `add_building`.
- **Prerequisites:** tier-1 buildings require the holding's base building (`hospices_01` `can_construct`: `building_requirement_castle_city_church = { LEVEL = 01 }`, `G/common/buildings/00_common_buildings.txt:3-12`; `guild_halls_01`: `has_building_or_higher = city_01`, `00_city_buildings.txt:2273-2277`). So the building is placed **after** `set_holding_type`.
- **Correction to the scout note:** `building_barracks_requirement_terrain` is **empty in 1.20.0.4**. Its whole `OR` is commented out (`G/common/scripted_triggers/00_building_requirement_triggers.txt:368-382`), so barracks have no terrain gate now. The guard below still calls it, which costs nothing and survives a patch that restores it.

**Placement table** (level 01 only; the province is `scope:eotg_frontier_new_barony.title_province` for the types that build a holding):

| Type | Building | Province | Guard and fallback |
|---|---|---|---|
| Settlement | `hospices_01` (`00_common_buildings.txt:3`) | the new city System | — |
| Trade | `guild_halls_01` (`00_city_buildings.txt:2273`) | the new city System | — |
| Military | `barracks_01` (`00_standard_military_buildings.txt:4107`) | the new castle System | `building_barracks_requirement_terrain = yes`, else `hospices_01` |
| Religious | `monastic_schools_01` (`00_temple_buildings.txt:4144`; church or temple-citadel holding unless a rite allows any) | the new church System | `has_holding_type = church_holding`, else `hospices_01` |
| Research | `monastic_schools_01` if the county's `title_province` is a church holding, else `hospices_01` | the county's capital System (Research builds no holding) | as left |
| Mining, Administrative | none | — | modifier-only, unchanged |

`scriptorium_01` is **not used**: it needs `has_dlc_feature = legends` (`00_temple_buildings.txt:3635-3643`).

**Script.**
- **New scripted effect** `eotg_frontier_place_building_effect = { BUILDING = <key> }`, PROVINCE scope, in vanilla's shape:
  - `if = { limit = { NOT = { has_building_or_higher = $BUILDING$ }  free_building_slots = 0 }  add_province_modifier = extra_building_slot  add_building = $BUILDING$ }`;
  - `else_if = { limit = { NOT = { has_building_or_higher = $BUILDING$ } }  add_building = $BUILDING$ }`;
  - plus `has_holding = yes` in both limits (no holding means no building).
- **New scripted effect** `eotg_frontier_completion_building_effect`, COUNTY scope, called in `eotg_frontier_complete_effect` **after** each type's `eotg_frontier_build_holding_effect` and **before** `eotg_frontier_settle_rewards_effect`:
  - `if = { limit = { exists = scope:eotg_frontier_new_barony } … }` for the holding types. The **no-slot branch** of `build_holding` (the `else` after the slot branch, which sets the scope at `:1366` after clearing it at `:1352`) leaves `scope:eotg_frontier_new_barony` unset, so nothing is placed: the existing fallback (development and control) stands.
  - Research uses `title_province` directly.
- The building goes into the **Local Ruler's** holding when A1 grants it (city or church). That is intended: the System is theirs, under the holder.
- **Tooltip:** the effect's own `add_building` line shows in .004's option tooltips, since `eotg_frontier_complete_effect` is not hidden there. No new loc key is needed for the effect.

**Untested in game (V-B1 to V-B4 in §10):** whether `add_building` bypasses `can_construct`, and whether a building whose `is_enabled` fails sits inert.

**Names:** the v2 mod has no building reskin loc, so placed buildings read with vanilla names. "Hospices", "Guild Halls" and "Barracks" are acceptable placeholders (orchestrator, 2026-10-12). `monastic_schools_01` **stays** (eotg-lore-keeper, 2026-10-12): at level 01 vanilla displays it as **"Chapel" (Monasteries line)**; "Monastic Schools" is the level-03 name (`G/localization/english/buildings_l_english.yml:500,502,508`). "Chapel" is an acceptable placeholder. Future reskin target for the line: **"Meditation Retreats"** (`OLD PROJECT VERSION/docs/localization_crusade.md:121`), done in the localizer's reskin pass (D5-4), not in this spec.

### 3.6 #1 round 2: four positive events (.057–.060)

**Owner approval:** H4, 2026-10-12 (D5-1); specified 2026-10-18. **Lore input:** eotg-lore-keeper constraints, relayed 2026-10-18 (§8 "Round 2" quotes them). **Ids:** the next free after .056, in the order the owner listed them: .057 population growth, .058 a skilled settler, .059 an infrastructure breakthrough, .060 a trade route.

**Scope (owner rule):** these four events, each with the usual mix of one plain option, one personality gate, one education or tier gate and one ungated guarded exit. Nothing else. Further ideas are in §12 as suggestions only.

#### 3.6.1 Shared rules

**Everything in §3.4.1 applies unchanged**, except the strain-cause paragraph: round 2 adds no cause, and its one strain gain (.057.d) uses `hardship`. In short:
- `character_event`, `theme = realm`, an `override_background` from §14.1, W6 animations, and a right portrait only where a character speaks or is offered;
- a world-state trigger (`holder ?= root`, `eotg_frontier_is_frontier = yes`, plus the event's own condition), and never a cooldown;
- `immediate` re-derives `scope:eotg_frontier_founder` (as .050, `events/eotg_frontier_events.txt:3418-3427`);
- every gated option repeats `eotg_frontier_is_frontier = yes`, and the last option is ungated and guards its effects;
- every option moves progress or strain, which is stricter than invariant 5;
- the §3.3 gate rules and the §12.1 voice rules.

**Round-2 additions:**
- **Seamless:** a Seamless root cannot reach these events (S6 statement): rule (a), through the roll guard and the in-flight trigger guard in §3.7.
- **Animations:** the default `animation` is a positive one (`happiness` or `personality_rational`), with W6 `triggered_animation`s for `greedy` and `paranoid` (`dismissal` / `paranoia`), so a suspicious ruler doesn't beam at good news.
- **Positive, not free.** Each event's ungated exit is a smaller gain, a gain paid for in strain, or a gain in coin rather than progress. No option is a pure "take the reward" with no trade-off against its siblings.
- **New in round 2:** one character template (.058). There are no new modifiers, opinion modifiers, causes or art. .060 reuses the existing `eotg_frontier_trait_trade_route` through `eotg_frontier_add_trait_effect` (`common/scripted_effects/eotg_frontier_effects.txt:1749-1759`).
- **No innovation, fascination or culture effect** in any option. In particular nothing grants or advances `eotg_innovation_self_repairing_machinery` (lore, .059).

#### 3.6.2 Wiring

There are four new entries at the end of `eotg_frontier_flavor_pick_effect`'s `random_list`, after .056. Each is `holder = { trigger_event = { id = eotg_frontier.05x / .060  days = { 1 120 } } }`, as for every sibling. **Cooldown authority stays in the roll.** Each event repeats its roll `trigger` as world state in its own `trigger`.

| Event | Roll weight | Roll `trigger` (eligibility) |
|---|---|---|
| .057 | 10; +10 `eotg_frontier_trait_habitable`; +5 `eotg_frontier_infra_habitat`; +5 `var:eotg_frontier_type ?= flag:settlement` | `var:eotg_frontier_progress >= 20`; `var:eotg_frontier_strain <= 3` (a camp worth staying in) |
| .058 | 10; +5 `eotg_frontier_trait_hostile`; +5 `eotg_frontier_trait_remote` (where skills are scarcest) | none |
| .059 | 5; +10 `eotg_frontier_trait_ancient_ruins` or `eotg_frontier_trait_ancient_infrastructure` (one modifier, `OR`); +5 `flag:research`; +5 `eotg_frontier_infra_research_facility` | `var:eotg_frontier_progress >= 20` (something built to improve) |
| .060 | 5; +15 `eotg_frontier_trait_trade_route`; +5 `eotg_frontier_infra_trade_station`; +5 `flag:trade` | `var:eotg_frontier_progress >= 33` (berths for a ship to stop at) |

**Pool balance.** With every event eligible, the pool's base weight is 185 before round 2 and 215 after it. So the four positive events take about 14% of rolls before modifiers. The pool's other good news (.003, .036, .040, .041) is mostly offers with strings attached.

**AI:** unchanged. AI Frontiers get silent rolls (v4 A2.4, D4-7), so the events are player-facing. The `ai_chance` blocks exist for the AI-controlled-player case.

#### 3.6.3 The events

"S" = strain and "P" = progress, as in §3.4.3. The localizer writes the text from the intent and the §8 round-2 constraints. Voice lines below are the architect's **suggestions** for the localizer and lore-keeper, not canon text.

**eotg_frontier.057: Berths Filling** (population growth; `eotg_bg_field_camp`)
- **desc:** the families are staying. The berths are full, the first children born in the Shoal are crying in them, and newcomers keep arriving on later convoys. There is no Exodus by name, no refugees from a named war and no farmland.
  - `desc_habitable` (Shoal has `eotg_frontier_trait_habitable`): some of them have stopped sealing their doors at night.
  - Suggested voice line (a crew chief, one line): "Three births this month, and nobody on the last convoy has asked for passage home."

| Opt | Gate | Intent | Effects | Stress | AI |
|---|---|---|---|---|---|
| a | `gold >= minor_gold_value` | Open new berths before the next convoy docks | −`minor_gold_value`; P +3; `.057.a_tt` | — | 40, −20 greedy |
| b | personality `gregarious` | I go down to the berths and greet the new families myself | P +2; S −1; `.057.b_tt` | `gregarious = minor_stress_impact_loss` | 30 |
| c | education `education_diplomacy` | Settle who berths where before anyone quarrels over it | S −1; P +1; `.057.c_tt` | — | 30 + tiers |
| d | ungated (guarded) | Let them come, and fit them in where they fit | P +2; S +1 `hardship` (crowding); `.057.d_tt` | `compassionate = minor_stress_impact_gain`; `ambitious = minor_stress_impact_loss` | 20 |

**eotg_frontier.058: A Pair of Steady Hands** (a skilled settler; `eotg_bg_office`; right portrait: the settler)
- **immediate** (inside `hidden_effect`, after the founder re-derive): `create_character` with `template = eotg_frontier_skilled_settler_template`, `location = scope:eotg_frontier_county.title_province`, `culture = root.culture` and `faith = root.faith`, saved as `scope:eotg_frontier_settler`. Culture and faith come from the holder, as in `eotg_frontier_create_figure_effect` (`eotg_frontier_effects.txt:1960-1971`).
- **after:** `if = { limit = { scope:eotg_frontier_settler ?= { is_alive = yes  NOT = { is_courtier_of = root } } }  scope:eotg_frontier_settler = { silent_disappearance_effect = yes } }`. An unhired settler leaves no stray character. This follows vanilla `court.4750`: the template is created in `immediate` (`G/events/court_events/court_events_general.txt:3299-3304`) and a rejected created character gets `silent_disappearance_effect` in `after` (`:3446-3462`; effect `G/common/scripted_effects/00_death_management_effects.txt:20`).
- **desc**, with the archetype keyed to the settler's education (lore list):
  - `desc_engineer` (`education_stewardship`): a habitat or life-support engineer, or a frame welder or salvager;
  - `desc_surveyor` (`education_learning`): a survey geologist, or a medic;
  - `desc_pilot` (`education_martial`): a pilot who knows the approaches;
  - the plain `desc` is the fallback.

  The settler is not a canon figure, not Titan-touched or arcane, not a veteran of a named war and not sent by a corporation. The text may mention clinic-fitted hardware if it reads as bought and paid for. **No cybernetics trait is added** to the settler, so the event depends on cybernetics only through §3.7's one trigger.
  - Suggested voice line (the settler): "I have kept worse air than this breathing. Pay me fairly and I will keep yours."
- **Deal (the .040 pattern, lore):** the work is paid for, and the Shoal stays mine. The settler gains no claim, no say and no title. Each hiring tooltip says so.

| Opt | Gate | Intent | Effects | Stress | AI |
|---|---|---|---|---|---|
| a | `gold >= minor_gold_value` | Sign [eotg_frontier_settler.GetHerHim] on at a fair wage | fee to the settler (the .040.a pattern: `save_temporary_scope_value_as` + `pay_short_term_gold`, `events/eotg_frontier_events.txt:3122-3123`) of `minor_gold_value`; `add_courtier = scope:eotg_frontier_settler`; P +3; `.058.a_tt` | — | 40, −20 greedy |
| b | personality `lazy`; `gold >= tiny_gold_value` | Put [eotg_frontier_settler.GetHerHim] over the crews, and rest easier | fee of `tiny_gold_value`; `add_courtier`; S −1; P +1; `.058.b_tt` | `lazy = minor_stress_impact_loss` | 30 |
| c | education `education_intrigue`; `gold >= tiny_gold_value` | Learn what [eotg_frontier_settler.GetSheHe] would rather not say, and hire [eotg_frontier_settler.GetHerHim] for less | fee of `tiny_gold_value`; `add_courtier`; the settler gets `eotg_frontier_opinion_slighted` toward root for 10 years (the .054.c shape); P +3; `.058.c_tt` | — | 30 + tiers |
| d | ungated (guarded) | Let [eotg_frontier_settler.GetHerHim] work for the crews, not for me | not hired (the `after` block removes the settler); P +1; `.058.d_tt` | `paranoid = minor_stress_impact_loss`; `trusting = minor_stress_impact_gain` | 20 |

**New template** `eotg_frontier_skilled_settler_template`, in `common/scripted_character_templates/eotg_frontier_templates.txt`, shaped like `eotg_frontier_settler_leader_template` (`:10-33`) and vanilla `poet_template` (`G/common/scripted_character_templates/01_ep1_character_templates.txt:1158-1170`). As in the mod's other templates, culture and faith are not set in it.
- `age = { 22 50 }`; `gender_female_chance = 50`;
- personality: `random_traits_list = { count = 1  diligent = {}  patient = {}  stubborn = {}  calm = {} }`;
- education: `random_traits_list = { count = 1` with `education_stewardship_2` and `_3` at weight 20 each, `education_learning_2` and `_3` at 20 each, and `education_martial_2` at 20 `}`;
- `random_traits = yes`;
- `stewardship = { 6 12 }`, `learning = { 6 12 }`, `martial = { 6 12 }`.

**eotg_frontier.059: Older Than Any Record** (an infrastructure breakthrough; `eotg_bg_cavern`)
- **desc:** the crews recover a technique from salvage "older than any record": a scrubber design that holds, a sounder frame that reads true, or a fix for water reclamation. The parts are made and fitted by hand.
  - **Banned:** self-repairing or self-replicating machinery, colony AI, terraforming, new drives, fabricators or printers (orchestrator ruling, pending the owner).
  - `desc_ruins` (Shoal has `eotg_frontier_trait_ancient_ruins` or `eotg_frontier_trait_ancient_infrastructure`): the salvage came out of the Shoal's own ruins.
  - Suggested voice line (a fitter): "Whoever built this knew more about air than we do. I can copy it. I cannot tell you why it works."

| Opt | Gate | Intent | Effects | Stress | AI |
|---|---|---|---|---|---|
| a | `gold >= minor_gold_value` | Fit it in every section, whatever it costs | −`minor_gold_value`; P +3; `.059.a_tt` | — | 40, −20 greedy |
| b | personality `calm` | Test it on one section, then the rest | S −1; P +2; `.059.b_tt` | `calm = minor_stress_impact_loss` | 30 |
| c | education `education_stewardship` | Write it into every crew's work orders | P +4; `.059.c_tt` | — | 30 + tiers |
| d | ungated (guarded) | Fit it where it is needed most, and keep the crews moving | P +2; `.059.d_tt` | `diligent = minor_stress_impact_loss`; `lazy = minor_stress_impact_gain` | 20 |

**eotg_frontier.060: Ships That Stop** (a trade route opens; `eotg_bg_underlevel_day`)
- **desc:** independent captains who used to pass through now stop. This matches the trade-route trait's own text (`localization/english/eotg_frontier_l_english.yml:170-171`). Raiding is real and routes shift around trouble, but the trouble is not named.
  - **Banned:** the League, a galactic market, protected lanes, treaty bodies, tariff unions, Thorum or the Trade Federation, hyperlanes or jump gates.
  - Any deal is a personal bargain, enforced by my own law.
  - `desc_route` (Shoal already has `eotg_frontier_trait_trade_route`): the ships I knew passed through have started to dock.
  - Suggested voice line (a captain): "The old run is too hot this year. Yours is quiet, and your berths are honest."

| Opt | Gate | Intent | Effects | Stress | AI |
|---|---|---|---|---|---|
| a | `gold >= minor_gold_value` | Build them proper berths and a beacon to find them by | −`minor_gold_value`; P +2; `eotg_frontier_add_trait_effect = { TRAIT = eotg_frontier_trait_trade_route  FLAG = trade_route }` (adds the trait only if it is missing and there is room; it fires the discovery hook, `:1749-1759`); `.060.a_tt`, conditional: the route is marked on the captains' charts only if it is new | — | 40, −20 greedy |
| b | personality `gluttonous`; `gold >= tiny_gold_value` | A proper meal for every captain who docks | −`tiny_gold_value`; P +2; S −1; `.060.b_tt` | `gluttonous = minor_stress_impact_loss` | 30 |
| c | tier `highest_held_title_tier >= tier_duchy` | They trade under my law, and whoever raids them answers to me | P +2; S −1; `add_prestige = minor_prestige_gain` (`G/common/script_values/00_basic_values.txt:1034`); `.060.c_tt` | — | 10; −10 each for shy, content, craven |
| d | ungated (guarded) | Let them dock, and take a berth fee from each | `add_gold = tiny_gold_value`; P +1; `.060.d_tt` | `greedy = minor_stress_impact_loss`; `generous = minor_stress_impact_gain` | 20 |

**Text constraint (.060.c):** the protection is the holder's personal word, enforced by the holder's own law. There are no protected lanes, no treaty and no authority above the polity (§8 LAW AT 866).

**Gate spread after 5E** (§13.1 step 6):
- 16 personality, 13 education and 4 tier gates.
- Education by skill: stewardship 3, intrigue 2, diplomacy 3, martial 2, learning 3. The largest share is 23%.
- There is at most one personality gate per event.
- All four new personality gates go to thin-coverage traits (gregarious, lazy, calm and gluttonous each had 3 `trait =` icons across `events/` on 2026-10-18), per step 2(b).

**Option count:** 114 after 5C, unchanged by 5D, and **130** after 5E (16 new options).

### 3.7 Seamless guard on the Frontier roll (5E)

**The gap.** `eotg_frontier_event_roll_effect` (`common/scripted_effects/eotg_frontier_effects.txt:884-985`) sends every **player** holder the founderless .002, or a pick from the pool, and checks no trait. A Seamless (`eotg_total_integration`) player therefore gets first-person text from rounds 1 and 2 and from the older pool events. `event_quality_v1.md` §12.5 rule 7 gives a Seamless ruler the log register.

**Decision: rule (a), exclude at the caller** (`event_quality_v1.md` §12.5.1 S1). Rule (b) is not right for the Frontier:
- (b) is reserved for events in the Seamless arc and for the three that ship a Seamless option by design (S2). No Frontier event is either.
- Doing (b) here would mean a `desc_seamless` and option-name variants on 22 events, which is new loc on a scale the owner has not asked for.
- (a) costs a Seamless ruler nothing mechanically. Their Frontier lives on through the **silent roll** that AI Frontiers already use (v4 A2.4). That is a faithful fit: a ruler past the threshold runs the project as a process, not as a run of personal choices.

**Is the trait check a dependency on cybernetics content?** It is a reference to a mod trait key. It is not a title, province, character, culture or faith, so it is **map-agnostic** and survives the map swap (CLAUDE.md, mod-exclusive rule). It does couple two mod systems. If `eotg_total_integration` were ever removed, the check would break. Both systems ship in one tree, and the kingpin and augmentation triggers already read the same trait (`common/scripted_triggers/eotg_aug_kingpin_triggers.txt:27`). To keep the coupling to **one line**, it lives in a single new Frontier trigger.

**Script (scripter):**
1. **New scripted trigger** `eotg_frontier_can_hear_flavor` (CHARACTER scope), in `common/scripted_triggers/eotg_frontier_triggers.txt`: `NOT = { has_trait = eotg_total_integration }`, with a comment citing §12.5 and this section.
2. **The caller** (`eotg_frontier_event_roll_effect`):
   - the first branch's limit becomes `holder = { is_ai = no  eotg_frontier_can_hear_flavor = yes }`;
   - insert a new `else_if = { limit = { holder = { is_ai = no } } … }` **before** the AI-to-AI sponsor offer, so a Seamless player never has a backer set silently. Its body is the silent-roll block, verbatim: `random = { chance = 50  set_variable = { name = eotg_frontier_event_cd  value = yes  years = 3 }  eotg_frontier_ai_silent_roll_effect = yes }`;
   - **cooldown authority stays in this one effect**, and the event cooldown is set only when the roll passes, as now. The later AI-only `if` blocks (`holder = { is_ai = yes … }`) already skip a player.
3. **The founderless case.** With .002's Without a Founder variant closed to them, a Seamless player would take `no_founder` strain every year. In `eotg_frontier_tick_effect`, the auto-pick limit (`eotg_frontier_effects.txt:692`, `holder = { is_ai = yes }`) becomes `holder = { OR = { is_ai = yes  eotg_frontier_can_hear_flavor = no } }`. The Appoint a Founder decision (v4 A4.2) still works for them.
4. **In-flight guard** (S1 exception: the threshold can be crossed inside the 1–120 day delay): add `eotg_frontier_can_hear_flavor = yes` on root to the `trigger` of every pool event: .002, .003, .030–.036, .040, .041 and .050–.060 (22 events). It is a state guard, not a cooldown (lesson 5 does not apply). The `.003` guard also covers `eotg_frontier_offer_backing_effect` (`:2433-2449`), which nothing calls yet.

**Not covered: residue that is player-initiated or structural** (D5-7):
- .001, .010, .020, .021 and .042 come from decisions a Seamless player chooses to take.
- .037 is a follow-up to .035.a.
- .004 (completion) and .005 (failure) are structural and **must** fire, or a Seamless Frontier could never end.

These still show first-person text to a Seamless player. **Partly resolved (orchestrator ruling, 2026-10-18, applying event_quality_v1 §12.5 rule (b) as B13 did):** .004 and .005 now carry Seamless register variants (batch 5E). The decision `is_shown` review for the others is still the owner's call (§13).

---

## 4. Identifier table (all new unless marked)

| Type | Key | Item |
|---|---|---|
| event option | `eotg_frontier.005.e` | #6 |
| event options | `.002.g`, `.002.h`, `.003.c`, `.005.f`, `.030.c`, `.031.d`, `.032.e`, `.033.d`, `.034.d`, `.034.e`, `.035.d`, `.036.c`, `.040.d`, `.041.d` | #2 |
| events | `eotg_frontier.050` … `eotg_frontier.056` (namespace `eotg_frontier`, existing) | #1 R1 |
| strain cause flag | `flag:dispute` (value of `eotg_frontier_last_cause`) | #1 R1 |
| scripted trigger | `eotg_frontier_faiths_differ` (county) | #1 R1 |
| scripted trigger | `eotg_frontier_cultures_differ` (county) | #1 R1 |
| script value | `eotg_frontier_research_fascination_value` (county) | #4 |
| temporary scope value | `eotg_frontier_fascination` | #4 |
| scripted effect | `eotg_frontier_research_fascination_effect` (county) | #4 |
| scripted effect | `eotg_frontier_place_building_effect` (`BUILDING`; province) | #5 |
| scripted effect | `eotg_frontier_completion_building_effect` (county) | #5 |
| changed effect | `eotg_frontier_complete_effect` (calls the two above) | #4, #5 |
| changed effect | `eotg_frontier_flavor_pick_effect` (7 entries) | #1 R1 |
| changed effect | `eotg_frontier_legibility_tooltip_effect` (cause `dispute`) | #1 R1 |
| changed event | `.005` desc (`desc_dispute`), `.002.e` trigger (adult, free) | #1 R1, #6 |
| vanilla keys used, not defined | `add_fascination_progress`, `culture_has_any_fascination`, `add_building`, `extra_building_slot`, `hospices_01`, `guild_halls_01`, `barracks_01`, `monastic_schools_01`, `building_barracks_requirement_terrain` | #4, #5 |
| events | `eotg_frontier.057` (Berths Filling), `.058` (A Pair of Steady Hands), `.059` (Older Than Any Record), `.060` (Ships That Stop) (namespace `eotg_frontier`, existing) | #1 R2 |
| event options | `.057.a`–`.d`, `.058.a`–`.d`, `.059.a`–`.d`, `.060.a`–`.d` (16) | #1 R2 |
| character template | `eotg_frontier_skilled_settler_template` | #1 R2 (.058) |
| saved scope | `eotg_frontier_settler` (event scope, .058) | #1 R2 |
| temporary scope value | `eotg_frontier_fee` (existing name, reused for the .058 wage; .040.a pattern) | #1 R2 |
| scripted trigger | `eotg_frontier_can_hear_flavor` (character; NOT Seamless) | §3.7 |
| changed effect | `eotg_frontier_flavor_pick_effect` (4 more entries) | #1 R2 |
| changed effect | `eotg_frontier_event_roll_effect` (Seamless branch → silent roll) | §3.7 |
| changed effect | `eotg_frontier_tick_effect` (founder auto-pick also for a Seamless player) | §3.7 |
| changed events | `trigger` of .002, .003, .030–.036, .040, .041, .050–.060 (in-flight Seamless guard) | §3.7 |
| existing keys reused | `eotg_frontier_trait_trade_route`, `eotg_frontier_add_trait_effect`, `eotg_frontier_opinion_slighted`, `flag:hardship` | #1 R2 |
| vanilla keys used, not defined | `silent_disappearance_effect`, `is_courtier_of`, `pay_short_term_gold`, `minor_prestige_gain`, `tiny_gold_value`; traits `gregarious`, `lazy`, `calm`, `gluttonous` | #1 R2 |

**Not added:** landed titles, modifiers, opinion modifiers, story cycles, decisions, gfx, `replace/`. One character template (round 2, .058) is the only new non-event definition beyond the triggers and effects listed above. Icons: the `trait =` icons are vanilla. No art request. Name lists, CoAs, holy sites: none touched. The .058 settler takes the holder's culture name list (no new names).

## 5. File placement

| File | Changes | Owner |
|---|---|---|
| `events/eotg_frontier_events.txt` | .005.e, .002.e trigger (5A); 14 options (5B); .050–.056 and .005 `desc_dispute` (5C); .057–.060 and the in-flight Seamless guard on 22 pool-event triggers (5E) | scripter |
| `common/scripted_effects/eotg_frontier_effects.txt` | `eotg_frontier_research_fascination_effect` + call (5A); flavour-pick entries, cause chain (5C); `eotg_frontier_place_building_effect`, `eotg_frontier_completion_building_effect` + call (5D); four flavour-pick entries, the Seamless branch in `eotg_frontier_event_roll_effect`, the auto-pick limit in `eotg_frontier_tick_effect` (5E) | scripter |
| `common/scripted_triggers/eotg_frontier_triggers.txt` | `eotg_frontier_faiths_differ`, `eotg_frontier_cultures_differ` (5C); `eotg_frontier_can_hear_flavor` (5E) | scripter |
| `common/scripted_character_templates/eotg_frontier_templates.txt` | `eotg_frontier_skilled_settler_template` (5E) | scripter |
| `common/script_values/eotg_frontier_values.txt` | `eotg_frontier_research_fascination_value` (5A) | scripter |
| `localization/english/eotg_frontier_l_english.yml` | §7 | localizer |
| `docs/tools/eotg_lint_baseline.json` | regenerated after 5B and after 5C (§13.1 step 10) | scripter |

No `replace_path`, no descriptor change, no new folder.

## 6. Wiring

| Item | Fired by | Tiers | Cooldown authority |
|---|---|---|---|
| .005.e, .005.f | .005 (the tick at strain 8, `eotg_frontier_effects.txt:747`) | every holder; .005.f duchy+ | none (state-gated) |
| #2 options | their events (unchanged callers) | every tier; .005.f and .032.e duchy+ | the events' existing callers |
| .050–.056 | `yearly_playable_pulse` → `eotg_on_yearly_frontier_tick` → the flavour roll → `eotg_frontier_flavor_pick_effect`, delay 1–120 days | every playable holder (county–hegemony) | `eotg_frontier_event_cd` + one roll per ruler (v4 A3), in the roll only |
| #4, #5 | `eotg_frontier_complete_effect` (.004 options; .004 fires for every holder) | every tier | once per completion |
| .057–.060 | as .050–.056: `yearly_playable_pulse` → `eotg_on_yearly_frontier_tick` → roll → `eotg_frontier_flavor_pick_effect`, delay 1–120 days | every playable, non-Seamless player holder (county–hegemony); .060.c duchy+ | the roll only, as above |
| §3.7 Seamless branch | `eotg_frontier_event_roll_effect` (the same roll) | Seamless player holders, every tier | the same `eotg_frontier_event_cd`, set only when the roll passes |

**Role triggers at every tier:** the roll already excludes Unsworn placeholders (v4 M1 guards), and after 5E it also sends Seamless players to the silent roll (§3.7). Tier gates are option gates, not event gates, so every tier sees every event.

## 7. Loc surface

**`eotg_frontier_l_english.yml`** (UTF-8 BOM, Canadian English, bare `[x.GetName]`, words not numbers for progress or strain, §12 voice, unescaped double quotes for speech, no dashes, dynamic knight term if soldiers are named):

- **5A:**
  - `eotg_frontier.005.e`;
  - `eotg_frontier.005.lead_tt`: I lead it myself, half the work stands, and the strain eases. It must not say the System will be root's (§3.1);
  - `eotg_frontier_research_fascination_tt`: shape `pam_great_project_types_l_english.yml:130`, with `[culture|E]` and `[cultural_fascination|E]`. It may show the percent, as vanilla does, because fascination progress is not a Frontier hidden value.
- **5B:**
  - 14 option names: `eotg_frontier.002.g`, `.002.h`, `.003.c`, `.005.f`, `.030.c`, `.031.d`, `.032.e`, `.033.d`, `.034.d`, `.034.e`, `.035.d`, `.036.c`, `.040.d`, `.041.d`;
  - 9 tooltips: `.002.g_tt`, `.005.f_tt`, `.030.c_tt`, `.032.e_tt`, `.034.d_tt`, `.034.e_tt`, `.036.c_tt`, `.040.d_tt`, `.041.d_tt`.
  - Reused: `.002.ease_tt`, `.002.push_tt`, `.003.accept_tt`, `.031.no_say_tt`, `.035.a_tt`.
- **5C:**
  - per event: `eotg_frontier.05x.t`, `.desc`, and the variants (`.050.desc_hostile`, `.051.desc_dangerous`, `.052.desc_late`, `.053.desc_remote`, `.054.desc_ruler`, `.055.desc_founder`, `.055.desc_county`, `.056.desc_founder`, `.056.desc_county`);
  - options `.05x.a`–`.d` (28);
  - tooltips: `.050.a_tt`, `.051.b_tt`, `.051.c_tt`, `.052.a_tt`, `.052.c_tt`, `.053.a_tt`, `.053.c_tt`, `.053.d_tt`, `.054.a_tt`, `.054.b_tt`, `.054.c_tt`, `.054.d_tt`, `.055.a_tt`, `.055.c_tt`, `.055.d_tt`, `.056.a_tt`, `.056.c_tt`, `.056.d_tt`;
  - `eotg_frontier.005.desc_dispute`;
  - `eotg_frontier_band_cause_dispute_tt`.
- **5D:** none. The `add_building` line is vanilla effect loc.
- **5E (§3.6):**
  - titles and descs: `eotg_frontier.057.t`, `.057.desc`, `.057.desc_habitable`; `.058.t`, `.058.desc`, `.058.desc_engineer`, `.058.desc_surveyor`, `.058.desc_pilot`; `.059.t`, `.059.desc`, `.059.desc_ruins`; `.060.t`, `.060.desc`, `.060.desc_route`;
  - options `.057.a`–`.d`, `.058.a`–`.d`, `.059.a`–`.d`, `.060.a`–`.d` (16);
  - tooltips (16): `.057.a_tt`–`.d_tt`, `.058.a_tt`–`.d_tt`, `.059.a_tt`–`.d_tt`, `.060.a_tt`–`.d_tt`. The .058 hiring tooltips (a, b, c) say the work is paid for and the Shoal stays mine. `.060.a_tt` is conditional on the route being new. `.060.c_tt` describes my own law and personal word.
  - .058 text uses `[eotg_frontier_settler.GetName]`, `.GetSheHe`, `.GetHerHim` and `.GetHerHis` (bare, never `scope:`).
  - The §3.7 guard needs no loc.

**No `replace/`.** Follow-up for the localizer, not this spec: a building reskin set (Hospices, Guild Halls, Barracks, and Chapel (Monasteries line) → "Meditation Retreats") under the one-definition rule (§8, D5-4).

**"rite" (.041.d, lore ruling 2026-10-12):** acceptable as plain lowercase text. It must **never** be linked as `[rite|E]` (that would point at the 1.20 rite concept). QA greps the new loc for `rite|E`.

**Glossary:** Shoal (county), System (barony), Frontier, backer, strain, Unsworn, Unclaimed Shoal. Never "pressure" (v4 A9), "charter", "mayor", "bishop" or "village".

## 8. Lore constraints

**Canon order:** SETTING LORE ERRATA, then the dated `docs/lore/` entries, then `866_bookmark_design.md`, then the SETTING LORE body (CLAUDE.md "Canon").

**Standing (v1–v4):**
- **LAW AT 866:** nothing exists above the polity: no arbitration, tribunal, League or Archive. A backer never owns the result or gains a say (`frontier_v4.md:66,93,99`). A Local Ruler holds under the holder's own law.
- Time-neutral Frontier text (`frontier_v1.md` §V). Don't name factions (`frontier_v3.md:20`, `frontier_v2.md:41`). No Void, and no "charter" meaning a higher authority (`frontier_v1.md:94,659`). No "human" or "humanity", and no medieval words.

**Round 1, from the eotg-lore-keeper (2026-10-12), binding on §3.4:**
1. **Sickness:** habitat sickness (bad air, fouled recycled water, radiation; it ties to the Hostile trait), or a fever in crowded berths.
   - *Banned:* "plague" and "pestilence" (the Awakening Plague is 1725), buboes, miasma, leeches, blaming Orro as fact, implant rejection.
   - *Use:* sickness, fever, scrubbers, quarantine berth, medic.
2. **The people already there:** raiders (raiding is active at 866: SETTING LORE:364, 451-454, 823), people already living there ("a few hardy families", the Unsworn), or generic beasts. There is no canon native species.
   - *Banned:* naming the Laughing Blades, Carrigore or the Black Wyrms.
3. **Collapse:** structural or social, not ecological. Seal failures and stations going dark are established (loc:90).
   - *Banned:* self-repairing machinery (not until 975).
4. **Shortage:** air, water, ice, spare parts, fuel ("ore, ice and volatiles", loc:169).
5. **The founder's claim:** under H1 the founder may be the Local Ruler (a vassal). The holder stays the political owner, and the dispute is a vassal pressing for more, settled under the holder's own law.
   - *Banned:* any outside court or arbiter.
6. **Two chapels:** scoped faiths only. There are four families, and only the Divine Order is hostile (866_religions:104-125). Zeal is rising (SETTING LORE:446-449). A church-holding founder may be of another faith (`frontier_v4.md:144`).
   - *Banned:* naming gods or faiths, Orrin cults, the Void.
7. **Separate berths:** settler cultures persist, and vanilla handles the long term (`frontier_systems.md:625-645`). The Exodus is bringing refugees (`REVIEW_866.md:31`).
   - *Banned:* naming species, "human".

**Round 2, from the eotg-lore-keeper (2026-10-18), binding on §3.6:**
- **All of the standing rules above still apply.** Nothing exists above the polity. The text is time-neutral: no Exodus, dates or named powers. No Void, "charter", "human" or "humanity", species names, or the cybernetics never-name words.
- **Register:** first person, present tense. Every desc variant carries I, me or my. At most one NPC line, in double quotes. Canadian English. No dashes.
- **Words to use:** Shoal, System, settlers, crews, berths, stations, supply runs, convoys, survey, beacon, port of call.
- **Banned words:** village, manor, peasants, serfs, barony, castle, masons, palace, horses, cart, caravan, guild, harvest, season, tithe, market town, "holding slot", gears, cogs, clockwork, steam, brass, automaton.
1. **Population growth (.057):** families stay, berths fill, the first children are born in the Shoal, and newcomers arrive on later convoys. Not the Exodus by name, not refugees from a named war, not farmland.
2. **Skilled settler (.058):** the archetypes are a habitat or life-support engineer, a survey geologist, a pilot who knows the approaches, a medic, and a frame welder or salvager. Clinic-fitted hardware is acceptable if it reads as bought and paid for. Not a canon figure, not Titan-touched or arcane, not a veteran of a named war, not sent by a corporation. The deal follows the .040 pattern: the work is paid for, and the Shoal stays mine. A generated settler uses a vanilla-shaped template (§3.6.3, vanilla cited).
3. **Infrastructure breakthrough (.059):** scrubbers, a sounder frame, a water-reclamation fix, or a technique recovered from salvage "older than any record"; parts made and fitted by hand.
   - *Banned:* self-repairing or self-replicating machinery, colony AI, terraforming, new drives, fabricators or printers. The last two are an orchestrator ruling, pending the owner (§13).
   - It must **not** grant `eotg_innovation_self_repairing_machinery`.
4. **Trade route (.060):** independent captains who already pass through now stop (loc:170-171). Raiding is active and routes shift around trouble, but the cause is not named.
   - *Banned:* the League, a galactic market, protected lanes, treaty bodies, tariff unions, Thorum or the Trade Federation, hyperlanes or jump gates.
   - Any deal is a personal bargain, enforced by my own law.

**#4 (lore ruling 2026-10-12: accepted, no guard):** fascination progress is generic culture advancement. If a culture is fascinated by the mod's `eotg_innovation_self_repairing_machinery`, a Research Frontier speeds it, and that is allowed. The ERRATA (SETTING LORE:64-70) makes self-repair researchable before 975; 975 is when the Gnomes reached it, not a floor. The innovation's own gate governs timing: `culture_era = culture_era_early_medieval` (`common/culture/innovations/eotg_innovations.txt:29`), AI ×0 below that era (`:39-48`). **Dependency: CB-36** (§3.2). The event-text ban in round-1 item 3 stays: no self-repairing machinery in Frontier event text.

**Lore questions raised by this spec:**
**Ruled by eotg-lore-keeper, 2026-10-12** (none open):
1. `monastic_schools_01` stays; its level-01 display name is "Chapel" (Monasteries line), an acceptable placeholder; reskin target "Meditation Retreats" (§3.5, D5-4).
2. Fascination reaching self-repairing machinery: accepted, no guard; depends on CB-36 (§3.2).
3. "rite" in .041.d: acceptable as plain lowercase text, never `[rite|E]` (§7).

## 9. Vanilla precedent (re-checked at 1.20.0.4 this session)

| Change | Vanilla file:line |
|---|---|
| Fascination progress with a fallback, behind a tooltip | `G/common/great_projects/types/01_pam_projects.txt:617-632` |
| Fascination fallback when no innovation target exists | `G/events/dlc/tgp/tgp_tribute_mission_events.txt:1051-1068`; target picker `:884-906` |
| Fascination amounts | `G/common/script_values/tgp_tribute_mission_values.txt:20`; `G/events/dlc/tgp/tgp_dynastic_cycle_flavor_events.txt:818`; `G/events/dlc/tgp/tgp_movement_events.txt:511` |
| Progress is in percent | `G/localization/english/effects_l_english.yml:1869, 1877` |
| Lifestyle XP sizes | `G/common/script_values/00_lifestyle_values.txt:7-9` |
| Personality option pairing (trigger, icon, stress) | `G/events/dlc/ep2/wedding_events/ep2_wedding_events_ewan.txt:3759-3778` |
| Name variant by trait | `G/events/dlc/ep3/ep3_admin_events.txt:512-523` |
| Education option with `skill =` (mod B1 precedent) | `events/eotg_augmentation_activities.txt:469-481` |
| `add_building` with a slot guard | `G/common/scripted_effects/01_building_upgrade_effects.txt:7-22`; `G/common/modifiers/00_province_modifiers.txt:173-176` |
| Building prerequisites | `G/common/buildings/00_common_buildings.txt:3-12`; `00_city_buildings.txt:2273-2277`; `00_standard_military_buildings.txt:4107-4112`; `00_temple_buildings.txt:4144-4160`, `:3635-3643` |
| Barracks terrain trigger (empty in 1.20) | `G/common/scripted_triggers/00_building_requirement_triggers.txt:368-382` |
| Value names | `minor_stress_gain` `00_stress_values.txt:6`; `minor_dread_gain` `00_basic_values.txt:731`; `medium_prestige_value` `:1002`; `tiny_gold_value` `01_dynamic_values.txt:13` |
| Delayed `trigger_event`, `factor = 0` gates, `duel` | as `frontier_v4.md` §9 |
| A character created from a template in `immediate`, offered, and removed in `after` if refused (.058) | `G/events/court_events/court_events_general.txt:3299-3304` (court.4750 `create_character`, `template = poet_template`), `:3446-3462` (`after`, `silent_disappearance_effect`); template shape `G/common/scripted_character_templates/01_ep1_character_templates.txt:1158-1170`; effect `G/common/scripted_effects/00_death_management_effects.txt:20` (kills with `death_disappearance` only if `is_ruler = no`) |
| `is_courtier_of = root` | `G/events/activities/chariot_race_activity/chariot_race_ongoing_events.txt:108` |
| `minor_prestige_gain` | `G/common/script_values/00_basic_values.txt:1034` |
| Seamless exclusion at the caller | `event_quality_v1.md` §12.5.1 S1 (mod rule, built on vanilla's role gating at the caller) |

**Round-2 deviation, stated:** court.4750 picks a pool character first and creates one only if none fits. .058 always creates one, because a pool search by culture or skill would add a picker for a one-off settler. The holder-culture creation matches the mod's own Frontier figures (`eotg_frontier_create_figure_effect`).

**Game version:** round 2 was checked against the installed **1.20.1.1** (orchestrator); the cited lines were read in this session.

**Deviations, each with its reason:**
- **Fascination instead of `add_innovation_progress`:** the named-target form isn't map-agnostic.
- **Amounts above a single vanilla contribution:** one payout for a decades-long project.
- **No vanilla-building reskin:** names are acceptable placeholders, and a `replace/` block would breach "one definition per key" until the localizer's reskin pass.

## 10. Definition of done

**Static (QA):**
1. Tiger is clean on the Frontier files, apart from the CLAUDE.md known-benign families (county-picker widget, override strict-scopes, `rite`). The PX language server and `px_vocab_check.py` show 0 new findings; `add_fascination_progress`, `culture_has_any_fascination`, `add_building` and `free_building_slots` must resolve in the vocab check.
2. `px_event_report.py`: 26/26 Frontier events reachable (19 + 7); 0 orphans; 0 missing `eotg_` loc.
3. **Invariant 5, per option:** each of the 14 #2 options, .005.e and each of the 28 round-1 options calls `eotg_frontier_add_progress_effect`, `eotg_frontier_add_strain_effect`, `eotg_frontier_ease_strain_effect` or `eotg_frontier_restart_effect`. QA greps each option block.
4. **Re-gating checks** (`eotg_event_quality.py --event`, `eotg_lint.py`):
   - 0 events with 2+ personality gates (L017);
   - 12 personality, 10 education and 3 tier gates in the file after 5C;
   - no education skill above 50%;
   - every personality gate has `trait =` and a stress row for the same trait;
   - every education gate has `skill =` and the `_3/_4/_5` AI tiers;
   - tier gates have no icon and AI base 10.
5. **Greps:**
   - `grep -rnE 'eotg_[ekdcb]_'` is empty;
   - `grep -nE 'title:|province:|culture:|faith:|character:'` over the changed files returns nothing;
   - no event `trigger = { }` reads `eotg_frontier_event_cd` or `eotg_frontier_roll_ready`;
   - no new loc key contains `Var('eotg_frontier_progress'` or `Var('eotg_frontier_strain'`;
   - the round-1 loc contains none of: plague, pestilence, miasma, human, charter, Void, Orrin, tribunal, arbiter, League, Archive.
6. **Voice:** the `\byou\b` grep over the new desc keys returns only quoted speech. Every new desc key carries I, me or my (§12.1 rule 13).
7. **Round 2 (5E), static:**
   - **V-R2a, reachability:** `px_event_report.py` shows 30/30 Frontier events reachable (26 + 4); 0 orphans; 0 missing `eotg_` loc.
   - **V-R2b, invariant 5 per option:** each of the 16 options in .057–.060 calls `eotg_frontier_add_progress_effect`, `eotg_frontier_add_strain_effect` or `eotg_frontier_ease_strain_effect`. QA greps each option block.
   - **V-R2c, gates:** 16 personality, 13 education and 4 tier gates in the file; no education skill above 50%; 0 events with 2+ personality gates (L017). The four new personality gates carry `trait =` and their stress row; the three education gates carry `skill =` and `_3/_4/_5`; .060.c has no icon, AI base 10 and the three negatives.
   - **V-R2d, no cooldown in triggers:** no trigger in .057–.060 reads `eotg_frontier_event_cd` or `eotg_frontier_roll_ready`.
   - **V-R2e, no innovation:** `grep -n 'innovation\|fascination\|culture = {' ` over the .057–.060 blocks returns nothing.
   - **V-R2f, round-2 loc greps:** the new keys contain none of the §8 round-2 banned words (village, manor, peasant, serf, barony, castle, mason, palace, horse, cart, caravan, guild, harvest, season, tithe, market town, holding slot, gears, cogs, clockwork, steam, brass, automaton, League, galactic market, protected lane, treaty, tariff, Thorum, Trade Federation, hyperlane, jump gate, self-repair, self-replicat, terraform, fabricator, printer, Exodus, refugee, human, charter, Void). No `[scope:`. No dashes (`—`, `–`, ` - `). Every desc key carries I, me or my.
   - **V-R2g, Seamless guard:** `eotg_frontier_can_hear_flavor` exists once. It is read in `eotg_frontier_event_roll_effect`, in `eotg_frontier_tick_effect`'s auto-pick limit and in all 22 pool-event triggers. `has_trait = eotg_total_integration` appears in no Frontier file except that trigger.
   - **V-R2h, map-agnostic:** the §10.5 `title:|province:|culture:|faith:|character:` grep is still empty over the changed files.

**In game:**

| Item | Check | Pass |
|---|---|---|
| #6 | Console-set strain 8 on a Frontier where the founder is someone else; take e | root is founder; progress halved; strain 4; .005 does not refire next tick. As a child ruler (console), e is not shown |
| #6 AI | Static | `ai_chance` matches §3.1 |
| #4 | Complete a Research project as a ruler whose culture has a fascination, with an Anomalous trait | the culture's fascination advances by 15 points; without a fascination, learning lifestyle XP is gained instead |
| #2 | For each of the 14 options, a ruler with and one without the gate | shown only with the gate; personality options show the trait icon; stress applies |
| R1 | Debug tick with each event's condition set (console traits, faith or culture swaps) | each fires within 120 days, only when eligible; `holder ?= root` voids it after a console title transfer |
| R1 cause | Take .054.d at strain 7, then tick | .005 shows `desc_dispute`; the Abandon tooltip shows the dispute cause line |
| #5 (**V-B1**) | Complete Settlement, Trade, Military and Religious under a feudal holder; Research with a church capital and without one | each new System holds its building at level 01; no error.log line; Mining and Administrative place nothing |
| #5 (**V-B2**) | Fill a Shoal's slots (console) before completion | `extra_building_slot` is added and the building placed; whether a building whose `can_construct` is unmet sits inert is recorded either way |
| #5 (**V-B3**) | Hover .004's completion options for each holding type | record whether the building line shows (QA 5D: `scope:eotg_frontier_new_barony` may be unset at preview, so only Research may show it); acceptable either way, note it |
| #5 (**V-B4**) | Complete a Trade Frontier | `guild_halls_01` is present once the new city has `city_01` |
| R2 (**V-R2-1**) | Debug tick with each round-2 condition set (progress and strain by console, Habitable, ruins, trade-route traits) | each of .057–.060 fires within 120 days, only when eligible; .057 never at strain 4+; .059 and .057 never below progress 20; .060 never below 33 |
| R2 (**V-R2-2**) | .058: take each of a–d, then check the character list | a, b and c: the settler is my courtier, the fee went to them (a: minor, b and c: tiny), c leaves them slighted; d: the settler is dead by disappearance (`after`), with no stray unlanded character; no error.log line |
| R2 (**V-R2-3**) | .058 with a settler of each education | the desc variant matches (engineer, surveyor, pilot) |
| R2 (**V-R2-4**) | .060.a on a Shoal without the trade-route trait and with trait room; then again on one that has it | the trait is added and the discovery hook fires once; second time no trait change, and the tooltip says so |
| §3.7 (**V-R2-5**) | `add_trait = eotg_total_integration` on a player holder with a Frontier; debug-tick a dozen times | no Frontier pool event (.002, .003, .030–.036, .040, .041, .050–.060) fires; progress and strain still move (silent roll); a founderless Frontier gets a founder auto-picked |
| §3.7 (**V-R2-6**) | Queue a pool event (debug tick until one is pending), then add the trait before it fires | the event does not fire (in-flight guard) |
| §3.7 (**V-R2-7**) | Remove the trait again | pool events resume on the next eligible roll |

## 11. Build batches (scripter takes them in order, after v4 batches 1, 2 and 4)

**Batch 5A: #6 and #4** (small, self-contained).
- .005.e;
- the .002.e adult/free fix;
- the A5 AI amendment;
- `eotg_frontier_research_fascination_value`, `eotg_frontier_research_fascination_effect` and its call.

Then the localizer (5A keys), then QA.

**Batch 5B: #2 trait-gated options.** The 14 options in §3.3. Close-out per §13.1 step 10: report the added stress rows, regenerate the L017 baseline, run the scorecard. Then the localizer, against every desc variant, then QA. This batch may be folded into event_quality B12 (frontier), which must then take these options as given.

**Batch 5C: #1 round 1.**
- `flag:dispute` (cause chain and .005 `desc_dispute`);
- the two `_differ` triggers;
- events .050–.056;
- the seven roll entries.

Close-out as 5B. Then the localizer, then **eotg-lore-keeper reviews the 5C loc** against §8 before QA.

**Batch 5D: #5 buildings.** The two building effects and the call in `eotg_frontier_complete_effect`. QA passed statically (2026-10-12); V-B1 to V-B4 are in-game. The building name is ruled (§3.5).

**Batch 5E: #1 round 2 and the Seamless guard** (§3.6, §3.7).
- `eotg_frontier_skilled_settler_template`;
- events .057–.060;
- the four roll entries;
- `eotg_frontier_can_hear_flavor`, and its three uses: the roll's Seamless branch → silent roll, the tick's auto-pick limit, and the in-flight guard on 22 pool-event triggers.

Close-out as 5B (§13.1 step 10: report the four added stress rows, regenerate the L017 baseline, run the scorecard). Then the localizer (§7 5E keys), then **eotg-lore-keeper reviews the 5E loc** against §8 round 2, then QA (§10.7, V-R2-1 to V-R2-7 in game).

5A must come first, because 5C's tooltips reuse .002/.005 keys. 5B and 5D are independent of each other. 5E follows 5C: it extends the same `random_list` and guards the round-1 triggers.

## 12. Deferred

- ~~**D5-1 #1 round 2**~~: specified 2026-10-18 as §3.6 (batch 5E), with the lore pass in §8.
- **D5-7 Seamless residue** (§3.7): .001, .010, .020, .021, .037 and .042 still show first-person text to a Seamless player. They are decision-fired or chained, and need an `is_shown` review; that is the owner's call (§13 Q2). .004 and .005 got rule (b) register variants in batch 5E (orchestrator ruling, 2026-10-18).
- **Round-2 suggestions (owner's call; not specified, not to be built):**
  - a .058 option that makes the settler the Frontier's founder when none is valid (a fifth option on an approved event);
  - a follow-up in which the .057 children come of age in the Shoal (a new beat);
  - a .060 follow-up when the route's captains are raided (a new beat);
  - .059 recording the recovered technique as county history for the legacy roll (new state).
- **D4-2 Founder choice picker** (#3): deferred by the owner, unchanged.
- **D5-2 New strain causes for the physical events** (sickness and collapse as their own causes): they reuse `hardship`/`danger`, which keeps the band and .005 surface small. Revisit if playtest shows "hardship" is too vague.
- **D5-3 Building upgrades over time** (level 02+ as the System matures): new beats, so the owner's call.
- **D5-4 Building reskin loc:** the localizer, after the lore ruling (§8).
- **D5-5 AI flavour events:** silent rolls only (D4-7). The round-1 events are player-facing.
- **D5-6 `stress_impact` → `stress_and_fulfillment_impact`:** with event_quality W11 after CB-18; all new rows use the house's old form.

## 13. Questions for the human

H4 is ruled. The needs-lore items in §8 go to eotg-lore-keeper. Round 2 raises two questions, and neither blocks 5E:
1. **Q1, fabricators and printers (.059):** the orchestrator banned them pending the owner. The spec follows the ban. Should it stand?
2. **Q2, Seamless residue (D5-7):** .004 and .005 got Seamless register variants in batch 5E (orchestrator ruling, 2026-10-18, following the B13 precedent; the owner may reverse it). Still open: should the decision-fired Frontier events (.001, .010, .020, .021, .037, .042) be hidden from or given variants for a Seamless player?

---

### HANDOFF (2026-10-18, round 2)
- status: done
- next: eotg-scripter (batch 5E, after 5C is committed), then eotg-localizer, then eotg-lore-keeper (5E loc review), then eotg-qa
- ask: Build batch 5E of `docs/specs/frontier_v5.md` §11. That is §3.6 (template `eotg_frontier_skilled_settler_template`, events .057–.060, four roll entries) and §3.7 (`eotg_frontier_can_hear_flavor`, the Seamless branch to the silent roll, the tick auto-pick limit, and the in-flight guard on 22 pool-event triggers). Close out per §13.1 step 10.
- files: docs/specs/frontier_v5.md (§0, §1, §2, §3.6, §3.7, §4–§13 updated)
- needs-loc: §7 5E: 4 titles, 4 descs + 5 variants, 16 options, 16 tooltips
- needs-lore: review the 5E loc against §8 round 2; the voice lines in §3.6.3 are suggestions only
- needs-human: §13 Q1 (fabricators/printers ban), Q2 (Seamless residue on .004/.005 and decisions, D5-7). In game: V-R2-1 to V-R2-7.

### HANDOFF (2026-10-12)
- status: done
- next: eotg-scripter (batch 5A), then 5B, 5C, 5D in order; eotg-lore-keeper reviews the 5C loc (§8 items 1–3 are ruled)
- ask: Build batch 5A of `docs/specs/frontier_v5.md` §11 (.005.e, the .002.e adult/free fix, the A5 AI amendment, and #4's fascination reward). Hand the 5A loc keys to the localizer and the result to QA. 5B (14 gated options), 5C (events .050–.056 and the `dispute` cause) and 5D (completion buildings) follow, each closed out per event_quality §13.1 step 10 where it applies.
- files: docs/specs/frontier_v5.md (new); docs/specs/frontier_v4.md (§13/§14 H4 ruled, header, D4-1/D4-9, handoff)
- needs-loc: §7. 5A: `eotg_frontier.005.e`, `.005.lead_tt`, `eotg_frontier_research_fascination_tt`. 5B: 14 option names + 9 tooltips. 5C: 7 × (t, desc, variants, a–d) + 18 tooltips + `eotg_frontier.005.desc_dispute` + `eotg_frontier_band_cause_dispute_tt`.
- needs-lore: items 1–3 ruled 2026-10-12 (§8): Chapel (Monasteries line) stays, fascination accepted with CB-36 dependency, "rite" plain text only. Remaining: a review of the 5C loc against §8.
- needs-human: none. In game after the build: #6, #4, R1 and V-B1 to V-B4 (§10).
