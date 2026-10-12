# Spec: Frontier Systems v5 (owner ruling H4: approved content)

**Author:** eotg-architect, 2026-10-12. **Status:** ruled, not built.
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
| 1 | New events, **round 2** (positive events) | approved; not yet specified | §9 D5-1 | — |
| 5 | Vanilla buildings placed on completion | approved; scout check passed | §3.5 | 5D |
| 3 | Founder choice picker | deferred | D4-2 (unchanged) | — |

**Option count in `events/eotg_frontier_events.txt`:** 71 today. After 5A it is 72, after 5B 86, and after 5C 114 (86 + 28 in the seven new events).

---

## 1. Purpose & gate

H4 approved new content for Frontier Systems. This spec covers all of it except round 2 of the new events. It adds:
- one option on .005;
- one completion reward;
- trait, education and tier variety on the existing events;
- seven new events;
- buildings on completion.

**Gate 3 (Systems)**, built under the **mod-exclusive exemption** (CLAUDE.md, decided 2026-10-02). **Not blocked by Gate 1.** Everything stays map-agnostic:
- no `title:`, `province:`, `culture:`, `faith:` or `character:` references;
- the culture and faith checks in §3.4 compare scopes and never name one;
- the buildings in §3.5 are vanilla keys, which exist on any map.

**Scope rule from the owner:** #6 and #2 add **options only**. The only new events are the seven round-1 events in §3.4, which the owner approved on 2026-10-12. No beats, follow-ups or chains beyond what is written here.

## 2. Signature resource

Unchanged: `eotg_frontier_progress` (hidden, 0–100, county variable) and its strain value `eotg_frontier_strain` (hidden, 0–8).

**How v5 touches them:**
- **Every new option** in §3.1, §3.3 and §3.4 moves progress or strain (a stricter rule than invariant 5, which binds only per event). The only exceptions are the ungated "moment has passed" exits, which exist already.
- **The seven new events** each move strain or progress in every option (§3.4 tables).
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

A Research Frontier runs for decades, can fail, and pays out once. **Amount: 10** (twice a single great-project contribution), **+5** when the Region holds a Research Facility, Ancient Ruins or Anomalous (the existing `eotg_frontier_mod_legacy_learning` condition minus the type check, `eotg_frontier_effects.txt:1798-1808`). That is 15 at most, three vanilla contributions. The fallback (no fascination) is `add_learning_lifestyle_xp = major_lifestyle_xp` (300, `G/common/script_values/00_lifestyle_values.txt:9`), the Cathedral's fallback with the research skill swapped in.

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

**The new options** (letters continue each event's sequence; every trigger also repeats the event's Region-state check, as the sibling options do):

| Option | Axis and gate | Text intent (localizer writes) | Effects | Stress (step 5) | AI |
|---|---|---|---|---|---|
| `.002.g` | **personality** `patient` (`trait = patient`, `has_trait`); valid founder | Slow the work and wait the year out | strain −1 (`eotg_frontier_ease_strain_effect`); progress −2; `custom_tooltip = eotg_frontier.002.g_tt` | `patient = minor_stress_impact_loss` | base 30 |
| `.002.h` | **education** `education_stewardship`, `skill = stewardship`; valid founder | Recut the ration ledger | `remove_short_term_gold = tiny_gold_value` (`G/common/script_values/01_dynamic_values.txt:13`); strain −1; `eotg_frontier.002.ease_tt` | — | base 30; +10/+20/+20 for `education_stewardship_3/_4/_5` |
| `.003.c` | **education** `education_intrigue`, `skill = intrigue`; as .003.a | Accept, once I know what they would rather keep quiet | as .003.a (set sponsor, progress +3, toast) **plus** strain −1; `accept_tt` + `ease_tt` | — | as .003.a's opinion modifiers; +10/+20/+20 by tier |
| `.005.f` | **tier** `highest_held_title_tier >= tier_duchy`; `prestige >= medium_prestige_value`; strain at failure | Order my vassals' crews in | `add_prestige = { value = medium_prestige_value multiply = -1 }` (`G/common/script_values/00_basic_values.txt:1002`); strain −3 (three ease calls; 8 → 5); progress unchanged; `custom_tooltip = eotg_frontier.005.f_tt` | — | base 10; −10 each for `shy`, `content`, `craven` (§13.1 step 3b) |
| `.030.c` | **education** `education_diplomacy`, `skill = diplomacy`; valid sponsor; rival exists | Let each backer hear what the other offered | keep the current backer; current backer `add_opinion eotg_frontier_opinion_pleased` (10 years); strain −1; progress +2; `custom_tooltip = eotg_frontier.030.c_tt` | — | base 30; +10/+20/+20 by tier |
| `.031.d` | **personality** `deceitful` | Promise them a say, and let the promise lapse | progress +2; sponsor pleased (10 years); `custom_tooltip = eotg_frontier.031.no_say_tt` (existing: the backer gains no say) | `deceitful = minor_stress_impact_loss` | base 20 |
| `.032.e` | **tier** `highest_held_title_tier >= tier_duchy`; settlers variant only (`NOT = { exists = scope:eotg_frontier_overlord }`) | Remind them whose Region this is | strain −1; progress −1; `add_dread = minor_dread_gain` (`00_basic_values.txt:731`); `custom_tooltip = eotg_frontier.032.e_tt` | — | base 10; −10 each for `shy`, `content`, `craven` |
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
  - `desc_hostile`: the Region is Hostile, and the air itself is part of it.
  - Voice line (lore): "The scrubbers on the lower decks failed a month ago, and now the coughing has spread to every berth."

| Opt | Gate | Intent | Effects | Stress | AI |
|---|---|---|---|---|---|
| a | `gold >= minor_gold_value` | Seal a quarantine berth and pay the medics | −`minor_gold_value`; P −1; `.050.a_tt` | — | 40, −20 greedy |
| b | education `education_learning` | Trace it to the scrubbers myself | S −1; `.002.ease_tt` | — | 30 + tiers |
| c | ungated (guarded) | Keep the crews working | P +2; S +1 `hardship`; `.002.push_tt` | `compassionate = medium_stress_impact_gain`; `callous = minor_stress_impact_loss` | 20 |

**eotg_frontier.051: The Ones Who Were Here First** (hostile inhabitants; `eotg_bg_field_camp`)
- **desc:** the people already living in the Region (a few hardy families, or raiders working out of it) have turned on the camp. No named group and no species.
  - `desc_dangerous`: the Region was known to be Dangerous.
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
| a | — (Region check only) | Evacuate the section and rebuild it right | P −4; S −1; `.052.a_tt` | — | 30 |
| b | personality `diligent` | I will walk the frame with the crews myself | P −2; S −1; `.052.a_tt` | `diligent = minor_stress_impact_loss` | 30 |
| c | education `education_stewardship` | Salvage the frame and reroute the crews | P −1; `.052.c_tt` | — | 30 + tiers |
| d | ungated (guarded) | Shore it up and keep the crews inside | P +1; S +1 `hardship`; `.002.push_tt` | `compassionate = medium_stress_impact_gain`; `callous = minor_stress_impact_loss` | 20 |

**eotg_frontier.053: Patched Seals** (shortage; `eotg_bg_barren_world`)
- **desc:** air, water, ice, spare parts or fuel running short.
  - `desc_remote`: the Region is Remote, and the next run is far off.
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
| d | ungated (guarded) | The coin was mine, and so is the Region | founder slighted (if alive); S +1 `dispute`; `.054.d_tt` | `humble = minor_stress_impact_gain`; `arrogant = minor_stress_impact_loss` | 20 |

**Text constraint (a):** the tooltip must not promise the System outright. If the founder is invalid at completion, A1 gives it to the created figure, so the line is conditional ("if [eotg_frontier_founder.GetSheHe] still leads it when the work is done").

**eotg_frontier.055: Two Chapels** (religious dispute; `eotg_bg_council`, because `temple*` backgrounds are rejected in §14.1)
- **desc:** settlers of different faiths will not share a chapel. Scoped faiths only, and never a name. Zeal is rising.
  - `desc_founder`: the founder's faith differs from the settlers'.
  - `desc_county`: the Region's faith differs from mine.
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
  - `desc_county`: the Region's culture differs from mine.
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

**Not added:** landed titles, modifiers, opinion modifiers, character templates, story cycles, decisions, gfx, `replace/`. Icons: the `trait =` icons are vanilla. No art request. Name lists, CoAs, holy sites: none touched.

## 5. File placement

| File | Changes | Owner |
|---|---|---|
| `events/eotg_frontier_events.txt` | .005.e, .002.e trigger (5A); 14 options (5B); .050–.056 and .005 `desc_dispute` (5C) | scripter |
| `common/scripted_effects/eotg_frontier_effects.txt` | `eotg_frontier_research_fascination_effect` + call (5A); flavour-pick entries, cause chain (5C); `eotg_frontier_place_building_effect`, `eotg_frontier_completion_building_effect` + call (5D) | scripter |
| `common/scripted_triggers/eotg_frontier_triggers.txt` | `eotg_frontier_faiths_differ`, `eotg_frontier_cultures_differ` (5C) | scripter |
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

**Role triggers at every tier:** the roll already excludes Unsworn placeholders (v4 M1 guards). Tier gates are option gates, not event gates, so every tier sees every event.

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

**No `replace/`.** Follow-up for the localizer, not this spec: a building reskin set (Hospices, Guild Halls, Barracks, and Chapel (Monasteries line) → "Meditation Retreats") under the one-definition rule (§8, D5-4).

**"rite" (.041.d, lore ruling 2026-10-12):** acceptable as plain lowercase text. It must **never** be linked as `[rite|E]` (that would point at the 1.20 rite concept). QA greps the new loc for `rite|E`.

**Glossary:** Region (county), System (barony), Frontier, backer, strain, Unsworn, Unclaimed Region. Never "pressure" (v4 A9), "charter", "mayor", "bishop" or "village".

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
| #5 (**V-B2**) | Fill a Region's slots (console) before completion | `extra_building_slot` is added and the building placed; whether a building whose `can_construct` is unmet sits inert is recorded either way |
| #5 (**V-B3**) | Hover .004's completion options for each holding type | record whether the building line shows (QA 5D: `scope:eotg_frontier_new_barony` may be unset at preview, so only Research may show it); acceptable either way, note it |
| #5 (**V-B4**) | Complete a Trade Frontier | `guild_halls_01` is present once the new city has `city_01` |

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

5A must come first, because 5C's tooltips reuse .002/.005 keys. 5B and 5D are independent of each other.

## 12. Deferred

- **D5-1 #1 round 2** (population growth, a skilled settler, an infrastructure breakthrough, a trade route): approved by the owner, not yet specified. It needs its own lore pass, like round 1, and is specced once those constraints are in.
- **D4-2 Founder choice picker** (#3): deferred by the owner, unchanged.
- **D5-2 New strain causes for the physical events** (sickness and collapse as their own causes): they reuse `hardship`/`danger`, which keeps the band and .005 surface small. Revisit if playtest shows "hardship" is too vague.
- **D5-3 Building upgrades over time** (level 02+ as the System matures): new beats, so the owner's call.
- **D5-4 Building reskin loc:** the localizer, after the lore ruling (§8).
- **D5-5 AI flavour events:** silent rolls only (D4-7). The round-1 events are player-facing.
- **D5-6 `stress_impact` → `stress_and_fulfillment_impact`:** with event_quality W11 after CB-18; all new rows use the house's old form.

## 13. Questions for the human

None. H4 is ruled. The needs-lore items in §8 go to eotg-lore-keeper.

---

### HANDOFF
- status: done
- next: eotg-scripter (batch 5A), then 5B, 5C, 5D in order; eotg-lore-keeper reviews the 5C loc (§8 items 1–3 are ruled)
- ask: Build batch 5A of `docs/specs/frontier_v5.md` §11 (.005.e, the .002.e adult/free fix, the A5 AI amendment, and #4's fascination reward). Hand the 5A loc keys to the localizer and the result to QA. 5B (14 gated options), 5C (events .050–.056 and the `dispute` cause) and 5D (completion buildings) follow, each closed out per event_quality §13.1 step 10 where it applies.
- files: docs/specs/frontier_v5.md (new); docs/specs/frontier_v4.md (§13/§14 H4 ruled, header, D4-1/D4-9, handoff)
- needs-loc: §7. 5A: `eotg_frontier.005.e`, `.005.lead_tt`, `eotg_frontier_research_fascination_tt`. 5B: 14 option names + 9 tooltips. 5C: 7 × (t, desc, variants, a–d) + 18 tooltips + `eotg_frontier.005.desc_dispute` + `eotg_frontier_band_cause_dispute_tt`.
- needs-lore: items 1–3 ruled 2026-10-12 (§8): Chapel (Monasteries line) stays, fascination accepted with CB-36 dependency, "rite" plain text only. Remaining: a review of the 5C loc against §8.
- needs-human: none. In game after the build: #6, #4, R1 and V-B1 to V-B4 (§10).
