# Spec: Cybernetics v2 — event expansion (index)

**Author:** eotg-architect, 2026-10-03
**Authorised by:** the human, relayed by the coordinator 2026-10-03: *"start working on the events in docs/qa/cybernetics_event_content_proposal.md; add additional choices for traits/outcomes where you see fit, or for events you see as lacking, while maintaining a cohesive story in the event chains."*
**Builds on:** [cybernetics_track.md](cybernetics_track.md) (track trait, implemented). **Inputs:** `docs/qa/cybernetics_event_content_proposal.md`, `cybernetics_content_gaps.md`, `cybernetics_logic_audit.md`, `cybernetics_system_overview.md`.
**Gate:** 3 (Systems), built against the temporary map under `docs/agent_workflow.md` §5 rule 2. **Not blocked.**

This file is the index. It holds the open questions, the rules every phase obeys, the shared identifiers, the on_action map and the story threads. Each phase has its own file and can be built, QA'd and committed on its own:

| Phase | File | Content | Depends on |
|---|---|---|---|
| **0** | [cybernetics_v2_phase0.md](cybernetics_v2_phase0.md) | Balance calls from the logic audit, applied. Shared foundations: helper effects and triggers, victim picker, stress helpers, gold values, lesson modifiers. | track spec |
| **1** | [cybernetics_v2_phase1.md](cybernetics_v2_phase1.md) | Trait-reactivity pass on the existing 31 events: violent-option stress, dominated options, trait-gated options, skill-farming conversion. | 0 |
| **2** | [cybernetics_v2_phase2.md](cybernetics_v2_phase2.md) | Entry hooks (Initiation I-01–I-04, I-06–I-08, I-10, I-11; I-05 and I-09 are Phase 5), the parent-death hook, 4 decisions. | 0 |
| **3** | [cybernetics_v2_phase3.md](cybernetics_v2_phase3.md) | Neurofractured mode. **3a:** pressure drift and bands, 3 band pools, The Heir's Arc, the real Warrant, Containment Regency, personality scramble. **3b:** the four endgames, Total Integration, `eotg_death_cascade`, 5 Neurofractured decisions. | 0 (3b needs 3a's band triggers) |
| **4** | [cybernetics_v2_phase4.md](cybernetics_v2_phase4.md) | Tier content: **4a** Augmented, **4b** Enhanced (incl. `on_birth_child`), **4c** Overclocked. Includes the voice's first two beats. | 0 |
| **5** | [cybernetics_v2_phase5.md](cybernetics_v2_phase5.md) | Large arcs: The Countdown, The Patron, The Iron Retinue (+ I-09 The Arms Race). | 0; 2 (initiation slots); 3a (cascade hand-off); 4c (Countdown stage 5 fires The Intervention) |
| **6** | [cybernetics_v2_phase6.md](cybernetics_v2_phase6.md) | Non-ruler lifecycle on `random_yearly_everyone_pulse`. | 0 |

The order follows content-gaps §6, with the logic-audit design calls pulled forward into Phase 0. Gaps §6 step 1 ("make risk visible") is **overruled** by the human's Q1 decision; Phase 0 keeps only its "fixes" half. Phases 4 and 6 can be built in any order after 0. Phase 5 needs 2, 3a and 4c. Thread beats tolerate absent phases (see §4).

---

## 0. Decisions

> **Resolved 2026-10-03:** the human accepted every recommendation below (B1–B6, Q7–Q11) as written. Build them; nothing in this table is open.

> **Standing rule (human, 2026-10-03):** when an event-design question arises, settle it from vanilla precedent, follow the architect's recommendation, and cite the vanilla file. Do not route it back as a question. Builders apply the same rule to design-level gaps they meet during implementation, and record the vanilla citation in a comment.

The current values are in the audit references.

| # | Call | Today | **Recommendation** | Why |
|---|---|---|---|---|
| **B1** | Neurofractured passive pressure drift (audit §2.3) | none: pressure only moves when options are picked, so the ≥30/≥60 weights rarely fire | **+8 a year, plus +4 per stress level (vanilla `stress_level` 1–3).** Sedation −6, Restraints −4. Calm options −5 to −10. | The band pools (Phase 3a) need pressure to move without the player's help. Calm ruler: Fracture band in ~4 years, Storm in ~8. Ruler at stress level 3: Storm in ~3 years. The terminal event at ≥95 arrives in roughly 6–12 years, which is long enough to play the mode, short enough to end. |
| **B2** | The stress-200 cliff (audit §2.2.1) | stress ≥ 200 both adds +24 a year **and** drops the threshold 80 → 60, so time to cascade falls from 7 pulses to 2 at one stress point | **Graded accrual, fixed threshold.** Accrual = 12 + 8 × `stress_level` (+12 paranoid, +10 at war). Threshold **80 always**. | Calm: 7 pulses. Level 1: 4. Level 2: 3. Level 3: 3. Stress still matters at every level, with no single-point cliff. The Countdown (Phase 5) then has 1–3 years of omens to play out. `eotg_neurofracture_threshold_met` loses its stressed branch. |
| **B3** | Regression decisions' stress gate (audit §2.2.6), plus risk kept on regression (§2.2.5) | Partial Removal needs stress ≥ 100; Downgrade needs stress ≥ 200, so a calm ruler cannot leave early. Regressing keeps all the risk. | **Drop both stress gates.** Cost: Partial Removal `medium_gold_value`, Downgrade `major_gold_value`, 25% cheaper at `stress_level >= 2` or with the Intervention flag (Phase 4c). **Downgrade halves `eotg_fracture_risk`.** | Prudence should be possible. Halving risk keeps "the damage partly stays" without the 82-in-one-pulse trap. |
| **B4** | Cooldowns 1.7e (Overclocked `months = 6`) and 1.7f (Neurofractured 12-month race) | OC effectively rolls every year; NF depends on same-day expiry order | **OC `months = 11`** (every pulse, stated honestly). While the Countdown story runs, the OC roll's nothing-weight doubles. **NF `months = 11`**; Court Massacre `months = 23`. The cascade guard in `eotg_trigger_neurofracture` → `months = 11`. | Matches the audit's fix, and makes the intent explicit. The Countdown carries the OC drama, so the random roll steps back. |
| **B5** | Scaled vs flat gold | flat 25–400 | **Scaled** vanilla script values (`tiny_` / `minor_` / `medium_` / `major_gold_value`) everywhere, existing costs included (mapping in Phase 0 §3). | Flat costs are trivial for emperors and ruinous for counts. Vanilla's values are realm-relative and map-agnostic. |
| **B6** | Permanent-skill farming (audit §2.4) | ~10 repeatable options give permanent skill; +4–8 over a lifetime | **Convert repeatable flavor rewards to 5-year "lesson" modifiers** (4 new keys, Phase 0). Permanent skill only at milestones: tier changes, endgames, chain conclusions. Permanent *losses* stay. | Vanilla reserves permanent skill for milestones. A lesson re-applied refreshes its timer and does not stack. |
| Q7 | Containment Regency on a capable adult | — | Use vanilla `designate_diarch` + `try_start_diarchy = regency` (precedent `events/bookmark_events.txt:2247`). **Needs an in-game check:** the engine may end a regency whose liege fails `regency_for_personal_reasons_trigger`. Fallback, built only if the check fails: add the vanilla `isolating_modifier` (one of the trigger's OR terms) for the regency's duration. | Vanilla `regency` has `start = always`, `end = always = no`. Code-side expiry for capable lieges is unverified. |
| Q8 | The Sickly Child (I-07) augments a child | — | Build it, with heavy stress weight on compassionate/just/zealous and a dedicated child-arc flag. **Lore-keeper and human to confirm tone.** | Strongest moral hook in the proposal. It also seeds the non-ruler lifecycle and the Heir's Arc. |
| Q9 | Total Integration ends the Neurofractured episodes | — | **Yes.** Total Integration replaces `eotg_neurofractured`, the episode pool stops, and the court leaves. The person is gone and the machine runs smoothly. | It makes Total Integration a different end state, not a louder Neurofractured. It needs a 3rd trait icon (art debt, human). |
| Q10 | The Clinic (gaps §3.3) | — | **Deferred.** It is a building-adjacent arc, and the v1 roadmap already defers building gates. | Keeps phases shippable without art. |
| Q11 | Legitimise Black-Market Implants (gaps §4) | — | **Not specced.** The scripter's in-flight audit fix 1.7c makes the illegal-implants modifier removable. If that fix chose a new decision, it already exists; if it chose maintenance, no decision is needed. | Avoid re-speccing an in-flight fix. |

**Decided here (flag only):**
- **Loc key form.** New events keep the existing files' dot form (`eotg_aug_tier1.007.t / .desc / .a`) rather than the brief's `eotg_<system>_NNNN_t`. All 229 existing keys are dot-form and explicit, and mixing forms in one namespace is worse than either one. Same one-definition and BOM rules.
- **No per-option risk tooltips.** The gaps doc's "custom tooltip on every option that moves risk" is a visibility item, overruled by Q1. Risk is told through event prose, the band pools, the Countdown, and the maintenance line already approved ("the static quiets").
- **The Warrant** uses a vanilla `liberty_faction`, falling back to `independence_faction` (Phase 3a). No claimant faction: the heir usually holds no claim.

---

## 1. Rules every phase obeys

1. **Identifiers.** `eotg_` prefix on every key. Story cycles are `eotg_story_aug_*`. No landed titles. Shared opinion modifiers are system-scoped (`eotg_opinion_aug_*`) because only this system uses them.
2. **Tier state.** Integration XP changes only at 0/50/100 through `eotg_aug_set_integration_effect`. Leaving the system entirely (Rejection failure, Remove Implants, Excision) uses the new `eotg_aug_remove_all_effect` (Phase 0), which removes the trait rather than setting XP. Total Integration and Neurofractured are separate traits.
3. **Hidden risk.** No number, bar, counter or story-cycle `basic_counter` ever shows `eotg_fracture_risk`. Story cycles are `visible = no` (the vanilla default). Prose may react to the band; tooltips may not quantify it.
4. **Signature coupling (invariant 5).** Every flavor event has at least one option that calls `eotg_add_fracture_risk` (on root or a saved augmented character), **or** changes tier, **or** reads the band in a `trigger`/`triggered_desc`. **Below Overclocked, prefer + moves and reads.** − moves at risk 0 are clamped away (audit §2.2.3), so a "calm" option at tiers 1–2 should pay off in another resource, not a cosmetic −3.
5. **Cooldown authority.**
   - Small events: branches in the tier `random_list` inside the existing custom on_actions. The cooldown flag is set in the branch.
   - Chain stages: fired with `trigger_event = { id = … days = {…} }` from the previous stage. No flags.
   - Story cycles: their `effect_group` timing is the cooldown.
   - Decisions: `cooldown = {}` or a flag set in the decision effect.
   - No event `trigger = {}` checks a cooldown flag. Event triggers are world-state guards that mirror the firing branch.
6. **Options.**
   - Shape: 3 universal options plus 1–2 trait-gated ones where it fits. A trait-gated option uses `trigger = { has_trait = X }` **and** `trait = X` for the icon.
   - A trait option may be the better deal for a character who has that trait. That is vanilla practice: trait options reward the trait. **Amended 2026-10-03** after Phase 1 QA; the earlier rule, "must not dominate the universal ones", contradicted vanilla. What it must not do is make a *universal* option pointless for characters without the trait, and universal options must not dominate each other (audit §2.5).
   - Every option has an `ai_chance` with ≥2 trait modifiers. Base 30 is the default. A decline or no-op may go down to 10, and the option an offer exists to sell may go up to 40 (vanilla bases run 0–100). *Amended 2026-10-04, CB-26 L9.*
   - The shape above applies to **choice** events. Chain-outcome stages and notifications (init.008, init.012, tier1.017, end.010, fracture.028) may have one or two options. *CB-26 S12.*
   - Every morally loaded option uses one of the stress helpers in Phase 0 §2.4.
7. **Victims.** Every character hurt or killed by an **episode** (the implant's violence the ruler did not choose) is picked with `eotg_aug_pick_victim_effect` and named in loc. Never bare `random_courtier`. This covers audit §1.5.
   - **Chosen targets are different** (*CB-26 L4/S5*). A person the story names and the ruler then decides to harm is picked by a dedicated scripted trigger and named in loc: the Errand's critic (patron.004, `eotg_aug_patron_critic_candidate`), an accused, a rival. That is not an episode, and the weighted picker does not apply.
8. **Gold.** Scaled script values only (B5).
9. **Map-agnostic.** No title, province, character, culture or faith keys. Faith reactions go through `zealous`, `cynical`, `theologian`, `lifestyle_mystic` and piety only. Created characters (the Patron's envoy) inherit `root.culture` / `root.faith` by scope, never by key.
10. **Traits.** Every trait named in this spec was checked in `game/common/traits/00_traits.txt`. **`curious` and `pensive` are childhood traits** (`category = childhood`, `maximum_age = 15`) and are never used. Substitutes: `eccentric`, `erudite`, `education_learning_3/4`, `lifestyle_physician`, `shy`.
11. **Loc.** UTF-8 BOM, bare `[x.GetName]` (never `[scope:x]`), one definition per key, dot-form keys (above). The localizer gets per-phase key lists.
12. **Do not touch the in-flight fixes.** The scripter is currently fixing audit §1.2, §1.3, parts of §1.4 (tier3.006.a arrest, tier3.007.a mutual opinion), §1.6, §1.7b/c/g and init.001.b. This spec references existing events **by id and option letter only**, never by line, and does not re-spec those fixes. If an in-flight fix and this spec touch the same option, the in-flight fix lands first and this spec's change is applied on top.

---

## 2. On_action map (all names verified)

| Hook | Status | Evidence | Extended by | Phase |
|---|---|---|---|---|
| `yearly_playable_pulse` | in use | PX `on_actions.log:3335`; `game/common/on_action/yearly_on_actions.txt:973` ("count+ characters") | the 5 existing `eotg_on_yearly_aug_*` on_actions; new branches inside them | 0–5 |
| `random_yearly_everyone_pulse` | new | PX `on_actions.log:2123`; `yearly_on_actions.txt:3172` ("once a year for all characters, random point") | `eotg_on_yearly_aug_nonruler_check` | 6 |
| `on_birth_child` | new | PX `on_actions.log:1931`; `child_birth_on_actions.txt:861` (root = newborn; `scope:mother`, `scope:father`, `scope:real_father`) | `eotg_on_birth_aug_parent_check` | 4b |
| `on_death` | new | PX `on_actions.log:1199`; `death.txt:7` (root = dying character, `scope:death_reason`, `scope:killer`) | `eotg_on_death_aug_hardware` (2), `eotg_on_death_aug_grief` (4b) | 2, 4b |

All four are extended additively (`on_actions = { eotg_… }`), never with a top-level `effect`/`trigger` on the vanilla hook. Catalog lesson 13 applies: no `on_yearly_playable`. QA runs `docs/tools/px_vocab_check.py`, which catches dead hooks, on every phase.

**Scope verification.** Every effect and trigger this spec places was checked against PX's `~/.vscode/extensions/jdeffner.px-toolkit-0.5.0/data/ck3/script_docs/{effects,triggers,event_targets}.log` for existence and supported scope. All are `character` scope where used (`create_faction`, `designate_diarch`, `try_start_diarchy`, `set_diarchy_swing`, `imprison`, `release_from_prison` (on the prisoner), `depose`, `set_player_character`, `move_to_pool`, `add_hook`, `death`, `create_story`, `add_tyranny`, `change_current_weight`, the relation setters and removers, `every_close_family_member`, `random_owned_story`). The exceptions: `add_faction_discontent` (faction scope, used inside `every_targeting_faction`) and `end_story` / `make_story_owner` (story scope, used inside `random_owned_story` or the story's own blocks). PX lists `duel` and `divorce` as scope "none"; vanilla calls both from character scope, as this spec does. QA confirms scope with Tiger.

---

## 3. Shared identifiers (defined once, in the phase noted)

### 3.1 Scripted triggers (`common/scripted_triggers/eotg_augmentation_triggers.txt`)
| Key | Phase | Meaning |
|---|---|---|
| `eotg_aug_pressure_flicker` / `_fracture` / `_storm` | 0 | `eotg_fracture_risk` < 30 / 30–59 / ≥ 60 (treat a missing variable as 0). Named for the Neurofractured bands, and used at Overclocked too. |
| `eotg_has_physical_loss` | 0 | `maimed` OR `one_legged` OR `one_eyed` OR `blind` |
| `eotg_has_physician_access` | 0 | self `lifestyle_physician`, OR `employs_court_position = court_physician_court_position` |
| `eotg_aug_victim_candidate` | 0 | used by the victim picker (Phase 0 §2.2) |
| `eotg_aug_has_heir_arc` | 3a | `any_owned_story = { story_type = eotg_story_aug_heir_arc }` |
| `eotg_aug_has_countdown` / `_patron` / `_retinue` | 5 | `any_owned_story = { story_type = eotg_story_aug_countdown }` (and the patron and retinue stories). The filter field is `story_type`; to end one, `random_owned_story = { limit = { story_type = … }  end_story = yes }`. *CB-26 S2.* |

### 3.2 Scripted effects (`common/scripted_effects/eotg_augmentation_effects.txt`)
| Key | Phase |
|---|---|
| `eotg_aug_pick_victim_effect` (params `NAME`, `FAMILY_FACTOR`) | 0 |
| `eotg_aug_pick_second_victim_effect` (params `NAME`, `FAMILY_FACTOR`, `EXCLUDE`) | 0 |
| `eotg_aug_remove_all_effect` | 0 |
| `eotg_aug_restore_loss_effect` | 0 |
| `eotg_aug_voice_advance_effect` (param `STAGE`) | 0 |
| `eotg_aug_stress_{surgery,embrace,reject,wound,murder,cruelty,tyranny,lie,neglect}_effect` (9) | 0 |
| `eotg_aug_scramble_personality_effect`, `eotg_aug_forget_relation_effect` | 3a |
| `eotg_aug_raise_warrant_effect`, `eotg_aug_start_containment_regency_effect` (params `KEEPER`, `SWING`) | 3a |
| `eotg_aug_total_integration_effect`, `eotg_aug_cascade_death_effect`, `eotg_aug_excision_effect` | 3b |
| `eotg_aug_nr_cascade_effect` (non-ruler cascade; never `eotg_trigger_neurofracture`) | 6 |

### 3.3 Variables and flags
| Key | Type | Set by | Read by |
|---|---|---|---|
| `eotg_fracture_risk` | char var 0–100 (existing) | many | everything |
| `eotg_aug_voice` | char var 0–5 (5 = Seamless: "no voice now") | `eotg_aug_voice_advance_effect` | Phases 3–5 descs and options (Thread T1) |
| `eotg_aug_focus` | char var (`flag:limbs` / `flag:senses` / `flag:nerves`) | tier1.021 (Phase 4a) | Phases 4b–5 |
| `eotg_parent_hardware` | char var → the dead parent, 5 years | `eotg_on_death_aug_hardware` | init.013 |
| `eotg_flag_aug_hidden_flaw` | char flag (permanent) | init.011, init.013 | OC accrual (+4/yr); Countdown starts at 40 not 50 |
| `eotg_flag_aug_vendor_safe` / `_bold` | char flag (permanent until removal) | tier2.013 | OC accrual −3 / +3 |
| `eotg_flag_aug_absent_at_birth` | flag on the **child**, permanent | tier2.010 | Heir's Arc weights |
| `eotg_flag_aug_intervention_refused` / `_discount` | char flags, 2 years | tier3.020 | Heir's Arc; B3 regression discount |
| `eotg_flag_aug_breach_victim` | flag on victim, 30 days | victim picker callers | fracture.002.c |
| `eotg_flag_aug_iron_retinue` | flag on knight, permanent | retinue story | Phase 6 weights |
| `eotg_flag_aug_child_patient` | flag on child, permanent | init.014/.015 | Phase 6; Heir's Arc |
| `eotg_flag_aug_restrained` / `_sedated` | char flags, decision-owned | Phase 3b decisions | NF on_action weights; drift |
| per-system event cooldowns | char flags | on_actions only | on_actions only |

### 3.4 New data objects (by phase)
| Type | Keys | Phase |
|---|---|---|
| static modifiers | `eotg_mod_aug_lesson_{prowess,learning,intrigue,martial}` | 0 |
| | `eotg_mod_aug_removal_withdrawal`, `eotg_mod_aug_infection`, `eotg_mod_aug_clean_install`, `eotg_mod_aug_bridge_strain` | 2 |
| | `eotg_mod_aug_restrained`, `eotg_mod_aug_sedated`, `eotg_mod_aug_excision_recovery` | 3b |
| | `eotg_mod_aug_bold_firmware`, `eotg_mod_aug_clarity_campaign`, `eotg_mod_aug_dulled_senses`, `eotg_mod_aug_overheated`, `eotg_mod_aug_optimised_levies`, `eotg_mod_aug_optimised_levies_trimmed` (CB-26 M1), `eotg_mod_aug_tampered` | 4 |
| | `eotg_mod_aug_patron_clause`, `eotg_mod_aug_patron_clause_final`, `eotg_mod_aug_patron_throttle`, `eotg_mod_aug_iron_retinue` | 5 |
| character template | `eotg_aug_patron_envoy_template` (`common/scripted_character_templates/eotg_augmentation_templates.txt`) | 5 |
| opinion modifiers | `eotg_opinion_aug_grateful_patient` (+20, 10y) | 2 |
| | `eotg_opinion_aug_falsely_accused` (−30, 10y), `eotg_opinion_aug_unmade` (−40, decaying) | 3 |
| | `eotg_opinion_aug_passed_over` (−15, 5y by default; retinue.005.d applies 10y) | 5 |
| trait | `eotg_total_integration` | 3b |
| death reason | `eotg_death_cascade` (`common/deathreasons/eotg_augmentation_deaths.txt`) | 3b |
| story cycles (`common/story_cycles/eotg_augmentation_stories.txt`) | `eotg_story_aug_heir_arc` | 3a |
| | `eotg_story_aug_countdown`, `eotg_story_aug_patron`, `eotg_story_aug_retinue` | 5 |
| decisions | `eotg_decision_seek_augmentation`, `_remove_implants`, `_consult_physician`, `_augment_retainer` | 2 |
| | `eotg_decision_aug_restraints`, `_aug_sedation`, `_aug_appoint_warden`, `_aug_embrace_cascade`, `_aug_excision` | 3b |
| namespaces (new) | `eotg_aug_heir`, `eotg_aug_end` | 3 |
| | `eotg_aug_countdown`, `eotg_aug_patron`, `eotg_aug_retinue` | 5 |
| | `eotg_aug_nr` | 6 |
| icons (human) | `gfx/interface/icons/traits/eotg_total_integration.dds` | 3b |

New folders shipped: `common/story_cycles/` (Phase 3a), `common/deathreasons/` (Phase 3b), `common/scripted_character_templates/` (Phase 5). None gets a `replace_path`. Add all three to the placement table in `CLAUDE.md` (orchestrator).

### 3.5 Event files
New events go in the existing file for their namespace: `events/eotg_augmentation_{initiation,tier1,tier2,tier3,fracture}.txt`. New namespaces get new files:
- `events/eotg_augmentation_heir.txt`
- `events/eotg_augmentation_endgame.txt`
- `events/eotg_augmentation_countdown.txt`
- `events/eotg_augmentation_patron.txt`
- `events/eotg_augmentation_retinue.txt`
- `events/eotg_augmentation_nonruler.txt`

---

## 4. Threads (what keeps the chains one story)

| # | Thread | Beats (event id → phase) | Rule that keeps it robust to build order |
|---|---|---|---|
| **T1** | **The voice.** The implant's second perspective, introduced quietly and paid off in Neurofractured. Stored in `eotg_aug_voice` 0–4. | 1 "a second self": tier2.020 *The Second Self* (4b) → 2 "it replies": tier3.012 *First Contact* (4c) → 3 "we": fracture.022 *We* (3a; specced as *The Second Voice*) → 4 "access granted": fracture.017 *Terms of Access*, a (3a). Payoff descs: fracture.026 *The Last Lucid Moment*, fracture.027 *The Cascade*, the Countdown stages, and `eotg_decision_aug_embrace_cascade` (needs Neurofractured **and** Storm **and** voice ≥ 3 or `eotg_flag_aug_may_embrace`). *CB-26: fracture.007 dropped (M12); Embrace condition per phase 3 (S3).* | `eotg_aug_voice_advance_effect` only ever raises the value. Every beat has a `triggered_desc` for "this is the first time you notice it", so Phase 3 works before Phase 4 exists. |
| **T2** | **The Patron's debt.** Somebody paid; they were buying you. | patron.001 offer (from init.018 or the initiation branch) → 4 demands over years → patron.006 final demand / betrayal; patron.008 *The Paper* once the implants are out ([new beats](cybernetics_v2_new_beats.md) §5.2). The firmware throttle pushes risk and can start the Countdown early. | Self-contained story cycle. It ends on owner death or settlement. |
| **T3** | **The Heir's Arc.** The dynasty watches the ruler break. | Seeds: tier2.010 *Absent at the Birth* flags the child; tier2.018 *Space Between Us* resolution; tier3.020 *The Intervention* refused. Arc: heir.001 Concern → fracture.005 *What the Heir Saw* (existing, re-homed) → heir.003 *The Heir's Warning* → heir.004 *The Heir's Choice* (ally / usurp / kill). Round 2 for a later heir: heir.007 *The Next in Line* → heir.003 → heir.004 ([new beats](cybernetics_v2_new_beats.md) §5.1); never a third. | Seeds only shift weights. With no seeds the arc runs on base weights. |
| **T4** | **The Iron Retinue → the non-rulers.** Augmentation spreads to the people around you, and they break too. | init.002.c, tier1.004.a, `eotg_decision_augment_retainer` (2) → retinue story (5) → `eotg_aug_nr.*` (6). Also feeds tier3.007 *Two Machines*, init.005 *Back From the Capital*, fracture.024 *The Same Pattern*. | Phase 6 reads the augmented non-ruler state directly in `eotg_on_yearly_aug_nonruler_check` and only *weights* by the retinue flag. (`eotg_aug_is_nonruler` was removed as unused, 2026-10-04.) |
| **T5** | **The physician.** Medicine as the counterweight. | `eotg_has_physician_access` cheapens or safens: init.006 (Prosthetic), init.007/.008 (Bridge), tier1.013–.015 (Rejection), maintenance, `eotg_decision_consult_physician`, Excision death odds. | Pure trigger; no state. |
| **T6** | **Flaws you can't see.** Cheap hardware comes due. | init.011 hidden flaw, init.013 a parent's hardware → `eotg_flag_aug_hidden_flaw` → +4 OC accrual, Countdown at 40. | The flag is only read in two places. |
| **T7** | **Focus.** What you chose to replace first. | tier1.021 sets `eotg_aug_focus` (limbs / senses / nerves). Read by: tier1.017 (limbs: duel bonus), tier2.012 & tier3.017–.018 (senses: truer warnings), tier2.020 & tier3.012 (nerves: the voice comes early), tier3.024 (limbs/senses: decisive odds in The Engagement's roll; CB-26 S6). | Absent focus = neutral branch. |

---

## 5. Loc estimate and review routing

| Phase | New events (incl. stages) | Approx. new loc keys | Notes |
|---|---|---|---|
| 0 | 0 | ~15 | lesson modifiers (8), revised decision tooltips (2), misc |
| 1 | 0 | ~60 | ~40 new trait-option keys, ~10 desc variants, revised option text where behaviour changed |
| 2 | 14 (init.006–.018, .020) | ~120 | 4 decisions × 4 keys, 4 modifiers, 1 opinion |
| 3 | 34 (3a 26 incl. 4 heir events; 3b 8) | ~270 | band pools, the Heir's Arc, endgames, 5 decisions, the TI trait (2), death reason (1), 3 modifiers, 2 opinions, voice variants |
| 4 | 48 (4a 16, 4b 15, 4c 17) | ~290 | 6 modifiers |
| 5 | 19 (Countdown 6, Patron 7, Retinue 5, init.019) | ~140 | stories are invisible: no story-panel loc |
| 6 | 6 | ~40 | |
| **Total** | **~121** | **~935** | The proposal's "~49 new" counted arcs. Chain stages are counted individually here. |

**Lore review: done (eotg-lore-keeper, 2026-10-03).** Its must-fix items, names and suggestions are folded into the phase files. The rules below bind the localizer, which applies the wording items **as it localizes each phase**, and every builder writing loc-facing text.

**1. Voice register rule** (Thread T1; every `[voice]` line and all Neurofractured text). The voice is the implant's predictive model of its user, running slightly ahead of them.
- It is **internal**: inside thought, precise, legible. It logs, schedules, forecasts, and requests access. It is *you, a half-second early.*
- It is **never** external, never at the edge of hearing, never whispering, never "answers", never comes "from" anywhere, and is never "the Eye".
- The Void is the opposite: external, at the edge of hearing, from an unknown source. A Void-Touched augmented ruler sees both systems, so the two registers must never blur. Not even as a character's belief.

**2. Banned in voice and Neurofractured text:** Void, Orrin, Kyros, the Eye (capitalised, or "it watches"), breach, rift, tear, whisper, "at the edge of hearing", hollow, silent speaker, "answers", "speaks from", prison, possess/possession, demon, pact, abyss, frenzy, and "grip" as a metaphor (it is the cataclysm's name). **Added 2026-10-04 (docs/lore review):** Carrigore, who is the archetypal whisperer inside Yu's mind (`docs/lore/An Adventurers Account of The First Era.md:1023-1037`). An arcane component in hardware never gives the voice a speaker. *Memory of Tomorrow* is the implant's **forecast stored as a memory**, never a vision or prophecy.

**3. Licensing is always local, and the licensing authority is never named: no court, regulator, registry or licensing body appears in text. Sellers (clinics, fitters, dealers and back-street crews) may be named from the CB-42 lists (`cybernetics_v2_seller_names.md`). 'Sanctioned' always means sanctioned under the realm's own law.** (Lore-keeper ruling, 2026-10-05.) Never "galactic", "League", "standard-issue", "interstellar regulation", or any named authority. init.018.a keeps "a sanctioned clinic" after the seller's name. The black market is about cheap, unvetted hardware under the holder's own law and clergy, not prohibition. **Confirmed 2026-10-04 against `docs/lore/`:** no supranational court, arbitrator or licensing body exists at 866. Acathea's Codex Unbound and arbitration come in 950 (`Third era Nations.md:21-26`), and the Galactic League is informal from 1650 (`Third era Events.md:1066`). **Never name** the real 866 implant players in hand-written text, as a company, a gang or anywhere else: Blackstar Corporation, Shadow Markets, Black Contract(s), Blackline, P&D, Calix, Pill Mob / Pillwake / Red Pills / Dr. Pill, Concrete Cartel. **The one exception is the generated syndicate name**: Pill Mob comes off this list for the Patron's syndicate only, which takes its name from the owner's `[syndicates]` list of canon syndicates through generated custom loc (item 7). In hand-written loc, Pill Mob, Pillwake, Red Pills and Dr. Pill stay banned. (Owner ruling 2026-10-05, CB-42; `cybernetics_v2_seller_names.md` §5.4.) Never name Acathea, the Codex, Archivists, a Conclave or a Tribunal as a higher authority. Never write "Trauma Team" (a trademark). No remote-kill or "terminate the wearer" mechanics: those belong to Blackstar in 1300. No state subsidy or programme framing: New Cauldron, 1610.

**4. No monotheistic invocations** ("Thank God", "God forgive", "be shriven"). The content fires for every faith, and several faiths are non-theistic. Either drop the invocation, or use the faith's own god-name loc function.

**5. Multi-species setting:** "self" or "personhood", never "humanity" or "human".

**6. Medieval leaks:** masons → work crew; palace → residence; scribes → archivists or the logs; horse → bulkhead (nr.004).

**7. Names fixed by the review:**

| Item | Name |
|---|---|
| Total Integration trait | **"Seamless"** (key stays `eotg_total_integration`) |
| `eotg_death_cascade` | **"died in a neural cascade"** |
| fracture.017 | **Terms of Access** |
| end.009 | **Hand Over the Controls** (no "open"/"through" in its options) |
| retinue.003 | **The Iron Ranks** |
| decision / end.020 | **Appoint a Warden** (`eotg_decision_aug_appoint_warden`) |
| fracture.002 | **Containment Failure** |
| the Patron | Named once per story from the owner's `[syndicates]` list of canon syndicates; 'the syndicate' / 'the syndicate envoy' on later mentions. Reprisal P7 and U1 still bind: the name never appears with P7's ownership words, and the lien desc (`eotg_mod_aug_patron_clause_final_desc`) never names the syndicate. No white-glove imagery. (Owner ruling 2026-10-05, CB-42; `cybernetics_v2_seller_names.md` §5.4.) |
| tier2.020.c | "Designate it" |

**8. Localizer-applied wording items** (from the review; behaviour unchanged):
- zealous "Begone" → "No device speaks for me." (tier3.012.e, fracture.017.e);
- "answers" → "replies" / "responds";
- the Seamless voice-5 line is "There is no voice now. There is no one left for it to speak to.";
- fracture.010 "the overlay labels your own face";
- fracture.008 "a designation, not a name";
- fracture.014's door is drawn by the spatial overlay;
- init.015's hum is audible hardware (coil whine);
- the I-07 child arc is narrated from the parent's side.

**Deferred (decided by the standing rule): zealous vs Industrial Survivalism.** Vanilla's zealous reactions are faith-generic (zealous is a personality trait, not a doctrine), so zealous lines here stay **faith-neutral** ("as I was made"). A zealous Creedwright blessing the implant needs a doctrine or tenet gate. That is deferred until v2 has faiths from the region briefs, and must not be built against the temporary map.

**For the human (from the review, not blocking):** the CYBERNETIC "VOICE" errata text and the Helix-at-866 errata choice are in the lore-keeper's report.

---

## 6. Definition of done (every phase)

1. **Tiger, `docs/tools/px_lsp_diagnostics.js` and `docs/tools/px_vocab_check.py` all clean** on the phase's files, except the known-benign items listed in `CLAUDE.md` §Validation. Commands as given there. Tiger is the only one that checks scope. Every phase file repeats this as item 0 of its own done list.
2. Every new event is reachable from a named on_action branch, chain stage, story cycle or decision (QA reachability audit). No event is fired by nothing.
3. QA audit 8: every new flavor event couples to `eotg_fracture_risk` or tier, per §1 rule 4.
4. No event `trigger` checks a cooldown flag (lesson 5).
5. `grep -rnE '\bcurious\b|\bpensive\b' events common` returns nothing.
6. `grep -rn 'random_courtier' events/eotg_augmentation_*.txt` returns only non-violent uses (picking a witness or speaker) or chosen targets filtered by a dedicated scripted trigger (rule 7), each followed by `save_scope_as`.
7. No `basic_counter`, `visible = yes` or number on `eotg_fracture_risk` anywhere (hidden-risk rule).
8. Loc: every key the phase lists exists once, BOM, no `[scope:`.
9. **Human, in game:** the phase's own check list (each phase file, final section).

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Finish Phase 0 (its mechanics and identifiers are unchanged by the lore fold-in), then build Phase 1, then the later phases in the index's order, applying index §5 and the standing vanilla-precedent rule.
- files: docs/specs/cybernetics_v2.md, docs/specs/cybernetics_v2_phase0.md … cybernetics_v2_phase6.md
- needs-loc: per phase (each phase file's "Loc" section). The localizer applies index §5 items 1–8 while localizing each phase.
- needs-lore: re-review the Phase 3a/4c voice loc once drafted
- needs-human: Helix-at-866 errata choice and the CYBERNETIC "VOICE" errata (lore-keeper report); 3rd trait icon `eotg_total_integration.dds` (Seamless); Q7 regency in-game check after Phase 3a; add `common/story_cycles/`, `common/deathreasons/` and `common/scripted_character_templates/` to CLAUDE.md's placement table
