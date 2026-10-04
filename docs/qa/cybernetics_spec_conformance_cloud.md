# Cybernetics v2 — Spec Conformance Audit (cloud)

> **STATIC, UNVALIDATED.** This was a cloud session with no game files, no Tiger, no PX and no game run. Every finding comes from reading the repo. Items that depend on how the engine behaves are marked `UNVERIFIED-VANILLA`.

**Date:** 2026-10-04 · **Branch:** `claude/focused-dirac-ixo81h` (from `v2-space-map` @ `8e28720`) · **Taskboard:** CB-24

**Compared:**
- **Specs:** `docs/specs/cybernetics_v2.md` (the index) and `cybernetics_v2_phase0.md`–`phase6.md`.
- **Script:**
  - `common/*/eotg_augmentation_*`
  - `common/story_cycles/eotg_augmentation_stories.txt`
  - `common/deathreasons/eotg_augmentation_deaths.txt`
  - `common/scripted_character_templates/eotg_augmentation_templates.txt`
  - `events/eotg_augmentation_*.txt` (11 files, 152 events, 670 options)
  - `localization/english/eotg_augmentation_l_english.yml`

**Excluded, as already known:**
- the CB-15 loose ends;
- everything in `docs/qa/cybernetics_qa_round2.md`;
- the CB-22 balance topics (progression speed, the AI decision layer, AI throttles, Augmented cost, Neurofractured agency, Seamless and Sedation, outcome rolls, thread links, coping and congenital hooks, the non-ruler rate).

**Method:**
- **Checks 2–5 (mechanical):** done with scripts that parse the block structure. Each check is listed below.
- **Checks 1 and 6 (per-phase spec vs script):** five read-only reviewers (Phases 1, 2, 3 and 4 one each; Phases 5 and 6 together). Together they made about 1,250 checks. I re-read the cited lines for every MEDIUM finding and for a sample of the LOW ones before including them.

**Owners:**
- **architect:** the spec is wrong, ambiguous, self-contradictory, or needs to ratify a deviation the script already made.
- **scripter:** the script should change.
- **localizer:** the loc should change.

---

## 0. Summary

| Check | Result |
|---|---|
| 1. Spec identifiers exist with the same key | **Pass.** All 248 `eotg_` identifiers in the specs exist as exact tokens in the script, once brace and suffix shorthands are expanded (9 stress helpers, 4 lessons, 9 new decisions, band triggers, vendor, intervention and treatment flags). Every data object in index §3.4 is defined. Event counts per phase match index §5 exactly (P2 14, P3 26 + 8, P4 16 / 15 / 17, P5 19, P6 6). |
| 2. Every event is fired by something | **Pass. 0 orphans.** The graph runs from the 4 vanilla hooks, 12 decisions and 4 story cycles, through 9 custom on_actions and 51 scripted effects, and reaches all 152 events. No reference points to an undefined event. All 4 story types have a `create_story`. |
| 3. Loc keys | **Pass.** BOM `ef bb bf` present. 1,334 keys, every line well-formed with `:0`, 0 duplicates (this is the only `.yml` in `localization/`, and there is no `replace/`). Every key referenced from script is defined. The only keys not referenced from script are `trait_track_eotg_cybernetics` and `_desc`, which the engine reads. No `[scope:` anywhere. One semantic loc mismatch: M5. |
| 4. CLAUDE.md invariants | **Pass, with notes.** `grep -rnE 'eotg_[ekdcb]_'` is empty. Every flag, variable and saved scope is `eotg_`-prefixed, except the 7 known CB-15 names. The 4 vanilla hooks are extended only through `on_actions = { }`. No event `trigger` reads a cooldown flag (the one flag read, `eotg_flag_aug_abdicated` in end.031, is a state flag). Every multi-option event moves or reads `eotg_fracture_risk` or tier. The 6 that don't (fracture.0001, fracture.028, end.002, end.010, end.011, end.030) are transformation, notification or endgame-outcome stages, not flavor events. |
| 5. Temporary-map rule | **Pass.** No title, province, character, culture or faith keys. The envoy template takes `culture = root.culture` and `faith = root.faith` by scope. |
| 6. Spec contradictions | **19 found** (§3). None blocks anything; all belong to the architect. |

**Findings: 0 HIGH, 12 MEDIUM, 43 LOW** (§2: 24 script-against-spec, 9 of them unratified deviations; §3: 19 contradictions between specs).

The script follows the specs closely. Most mismatches are deliberate, commented deviations (often marked "final QA" or "orchestrator ruling") that were never written back into the spec. The fastest fix is for the architect to ratify or reject the items in §1 and §3 in one pass.

---

## 1. MEDIUM

| # | Where (script) | Spec says | Script does | Owner |
|---|---|---|---|---|
| M1 | `events/eotg_augmentation_tier2.txt:1258-1276` (tier2.011.c); loc `eotg_augmentation_l_english.yml:1093`; modifier `common/modifiers/eotg_augmentation_modifiers.txt:260-264` | `phase4.md:229`: "50%: as a, **without the vassal penalty**. 50%: nothing." | Success applies the full `eotg_mod_aug_optimised_levies`, which carries `vassal_opinion = -5`. The success loc ("trims the plan where the vassals would have felt it") tells the player there is no penalty. The option is also gated on `cp:councillor_steward` (which hides a universal option when there is no steward) and adds stewardship × 2 to the odds. Neither is in the spec. | architect (approve a penalty-free variant modifier, or the current behaviour), then the scripter or localizer makes effect and loc agree |
| M2 | `events/eotg_augmentation_tier2.txt:353-376` (tier2.003.d) | `phase1.md:53`: "As a, plus **helper embrace**; risk +5." | Calls `eotg_aug_stress_surgery_effect` plus an ad-hoc `ambitious` loss. The embrace helper is never called, so eccentric characters lose relief and zealous, content and humble characters lose the gain. The comment cites a "Phase 1 QA" ruling that appears in no doc. | architect (amend or confirm), then the scripter |
| M3 | `events/eotg_augmentation_initiation.txt:705-727` (init.006.c) | `phase2.md:76`: the physician gets `eotg_opinion_aug_grateful_patient`. | Gives `eotg_opinion_aug_admiration` for 10 years, citing an "orchestrator ruling" that is recorded nowhere. | architect (record the ruling) or the scripter (revert) |
| M4 | `events/eotg_augmentation_initiation.txt:665-670` (init.006.a); compare e at `:762-779` | `phase2.md:74`: a costs `medium_gold_value`, ×0.75 with physician access. e is "As a". | a always charges full price (the comment cites an orchestrator ruling). e still applies the ×0.75, so two options the spec calls identical are priced differently. | architect, then the scripter |
| M5 | `events/eotg_augmentation_initiation.txt:2555-2564`; `common/scripted_effects/eotg_augmentation_effects.txt:1210-1229` | `phase5.md:181` and done-list `:278`: init.020 starts the Retinue only when root **already has another** augmented knight, at `phase = 2`. | The test `any_knight = { eotg_is_augmented_any = yes }` counts the knight just installed, so the story starts after the first knight, at `phase = 1`. The comment marks this as a deliberate "final QA" change. | architect (ratify and amend §3.1 and §7.5) or the scripter (revert) |
| M6 | `common/scripted_effects/eotg_augmentation_effects.txt:228-232`; `common/modifiers/eotg_augmentation_modifiers.txt` ~288 | `phase5.md:253`: "All modifiers go into `eotg_clean_all_aug_modifiers` (patron and retinue modifiers are removed on the owner's full removal)." | Only `eotg_mod_aug_iron_retinue` is removed. `eotg_mod_aug_patron_clause`, `_clause_final` and `_throttle` are kept on purpose ("the debt survives the implants"). | architect (the spec line or the script must change) |
| M7 | `common/story_cycles/eotg_augmentation_stories.txt:404-469` and its copy at `:472-531` (Patron tick) | `phase5.md:122-124`: the order is (1) envoy dead or gone → .007; (2) `grievance >= 3` → .006; (3) by demand. | `grievance >= 3 OR demand >= 4` → .006 is checked first, then the envoy. A skip is also added: demand 2 with no valid critic jumps to .005. Both are commented as deviations. **Side effect:** .006 can fire while `scope:eotg_patron_envoy` is dead, so it is shown in the portrait and the betrayal text. | architect (ratify and amend §2.3); scripter (guard .006's envoy references with `is_alive`) |
| M8 | `common/scripted_triggers/eotg_augmentation_triggers.txt:304-311`; `events/eotg_augmentation_patron.txt:442-462` (patron.004) | `phase5.md:152`: the critic is "a zealous courtier, else a random courtier". By context, someone at your court. | `eotg_aug_patron_critic_candidate` doesn't exclude the syndicate envoy, who is a courtier and can roll `zealous` (`random_traits = yes`). The syndicate can then ask you to murder its own envoy, and the next tick fires .007 *A New Envoy*. (Separate from round-2 M10, which is about `is_adult`.) | scripter (exclude the story's envoy) |
| M9 | `common/on_action/eotg_augmentation_on_actions.txt:1321-1366` and `:1399-1471` | `phase6.md:43`: progression is "Silent; nr.002 reports it". `phase6.md:52`: nr.002 is a weight-10 entry in the step-5 list. | nr.002 is not in the step-5 list. It fires from step 2 on a successful progression, which sets the liege cooldown and skips step 5 for that character. The script's reading is the coherent one: a list entry could report a progression that never happened. | architect (amend phase6 §1) |
| M10 | `events/eotg_augmentation_nonruler.txt:506-530` (nr.004.d); compare a at `:448-466` | `phase6.md:102,105`: "d [just] A trial. +50 prestige; then as a." a calls the tyranny helper. | d imprisons, applies risk −5 and the wound helper, but **not** `eotg_aug_stress_tyranny_effect`. This may be intended (a trial isn't tyranny for a just ruler), but the spec doesn't say so. | scripter, or the architect carves out the exception |
| M11 | `common/on_action/eotg_augmentation_on_actions.txt:1003-1019`; `events/eotg_augmentation_heir.txt:525` | `phase3.md:31` and `:409`: the arc starts whenever no Heir's Arc story exists and a primary heir of 14+ is alive ("no cooldown; the story owns its pacing"). | heir.004 sets a permanent `eotg_flag_aug_heir_arc_done`, and the on_action never restarts the arc while it is set. A later heir (after the first is executed in heir.004's kill branch, or sidelined by a usurp) never gets an arc. Read literally, the spec instead restarts the arc the year after heir.004. | architect (pick the intended behaviour) |
| M12 | `events/eotg_augmentation_fracture.txt:955-960` (fracture.007) | Index `cybernetics_v2.md:177` (T1) names fracture.007 *Dead Reckoning* as a voice payoff desc. | One static `desc = eotg_fracture.007.desc` with no `eotg_aug_voice` variant. Phase 3 says nothing about fracture.007's desc. | architect (drop it from T1), or the scripter and localizer add the variant |

---

## 2. LOW: script against spec

| # | Where (script) | Spec says | Script does | Owner |
|---|---|---|---|---|
| L1 | `common/decisions/eotg_augmentation_decisions.txt:8-13`, `:19-60`, `:63-128` | `phase0.md:53`: "`is_valid_showing_failures_only` mirrors the gold check" on both regression decisions. | No such block. The header comment explains that the engine blocks an unaffordable `cost` by itself. `UNVERIFIED-VANILLA`: that `cost` alone greys the decision out with a reason. | architect (amend Phase 0) |
| L2 | `events/eotg_augmentation_initiation.txt:88-102` (init.001.c) | Index `cybernetics_v2.md:66` (rule 6): a trait-gated option uses `trigger` **and** `trait =`. `phase1.md:30`: "c: unchanged". | Gated on `zealous OR content OR humble`, with no `trait =` icon. This is a pre-v2 option, the only trait-gated option in the system without an icon (a full scan of 670 options). | scripter (add `trait = zealous`, or split the option) |
| L3 | `events/eotg_augmentation_endgame.txt:384-415` (end.011 a/b/c) | Index `cybernetics_v2.md:68-69`: every option's `ai_chance` has ≥2 trait modifiers, and morally loaded options use a stress helper. | The `ai_chance` uses only gold, war and dread. c adds `add_tyranny = 20` with no tyranny helper. These are the only multi-option events in the system with no trait modifier in `ai_chance`. | scripter |
| L4 | `events/eotg_augmentation_patron.txt:446-462` (patron.004 critic) | Index `cybernetics_v2.md:70` (rule 7) and done-item 6 (`:254`): victims come from the picker, and `random_courtier` is used only for non-violent picks. | A bare `random_courtier` picks a character who is murdered in option a. `phase5.md:152` prescribes this, so the specs disagree (see also S5). The victim is flagged `eotg_flag_aug_breach_victim`. | architect |
| L5 | `events/eotg_augmentation_initiation.txt:119-125` (init.001.d), `:437-445` (init.004.e) | `phase1.md:30,33`: "Same as a", with craven minor loss (001.d) and craven medium loss (004.e). | Both write the surgery lines by hand (correctly avoiding the helper's craven gain). 004.e keeps a's `base` and `content` lines, but 001.d drops them, although 001.a has them (`:55-58`). A craven ruler gets −15 on 001.d and −30 base plus −30 on 004.e. | scripter (restore a's base and content lines on 001.d if "same as a" is literal) |
| L6 | `events/eotg_augmentation_fracture.txt:149-183`, `:193-211` (fracture.002) | `phase1.md:75`: `FAMILY_FACTOR = 0.05` for both picks. | 0.25 in Storm, else 0.05. This follows `phase0.md:128` and `phase3.md:570`, which the Phase 1 row predates. | architect (amend the Phase 1 row) |
| L7 | `events/eotg_augmentation_initiation.txt:992` (init.008) | `phase2.md:95`: `increase_wounds_effect = { REASON = wounds }`. | `increase_wounds_no_death_effect = { REASON = wounds }`, commented as avoiding a death before the event opens. `UNVERIFIED-VANILLA`: `REASON = wounds` is valid for the no-death variant. | architect (amend) |
| L8 | `events/eotg_augmentation_initiation.txt:1522-1526` (init.012, lost) | `phase2.md:137`: `add_trait = wounded_1`. | `increase_wounds_no_death_effect = { REASON = treatment }`, commented as not resetting an already-wounded ruler to rank 1. `UNVERIFIED-VANILLA`: `REASON = treatment`. | architect (amend) |
| L9 | init.011.b `:1414` (40), .011.c `:1432` (20), .014.c `:1817` (20), .018.a `:2334` (40), .018.c `:2375` (40), .018.d `:2385` (10), .018.e `:2398` (20), .020.a `:2476` (40), .020.b `:2493` (20), .020.c `:2510` (20), .020.e `:2545` (10), all in `events/eotg_augmentation_initiation.txt` | `phase2.md:70`: every option's `ai_chance` has base 30. | The bases listed (in brackets) differ. | scripter, or the architect loosens the rule |
| L10 | `common/decisions/eotg_augmentation_decisions.txt:204-206`, `:242-244`, `:280-282`, `:331-333`, `:383-385`, `:423-425`, `:460-462`, `:530-532` | `phase2.md:209` and `phase3.md:541`: `decision_misc.dds` (or the human's illustrations). | Vanilla placeholders `decision_smith`, `decision_physician`, `decision_knight_kneeling`, `decision_prison` and `decision_realm`, plus the mod's `eotg_decision_partial_removal.dds` for Augment Retainer. Only Embrace uses `decision_misc`. `UNVERIFIED-VANILLA`: that those vanilla `.dds` files exist in 1.20. | scripter (or the architect accepts the placeholders) |
| L11 | `common/on_action/eotg_augmentation_on_actions.txt:117-134` | `phase2.md:20,137`: `eotg_flag_aug_backalley_retry` lets init.010 fire "regardless of cooldown". It gives no chance and says nothing about the other branches. | The retry is a 50% `random` in an `if`, with the normal list as its `else_if`. While the 2-year flag is held, a failed roll skips the whole list (including Parent's Hardware and the Prosthetic). | architect (state the chance, and whether the list still rolls) |
| L12 | `events/eotg_augmentation_initiation.txt:2713-2724` (init.019.e) | `phase5.md:241`: e is `[content]`. | A universal option with no gate or icon. The comment says this is "final QA", because a, c and d cost gold. | architect (ratify) |
| L13 | `common/scripted_effects/eotg_augmentation_effects.txt:1129`; `events/eotg_augmentation_patron.txt:880` | `phase5.md:105`: the envoy is created at `location = root.capital_province`. | `location = root.location`, which differs while the ruler travels or campaigns. | scripter |
| L14 | `common/scripted_effects/eotg_augmentation_effects.txt:706-750`; only caller `events/eotg_augmentation_fracture.txt:2450-2453` (fracture.018.a) | `phase3.md:115`: save `scope:eotg_forgotten`; "callers name them in loc". | The scope is saved, but no loc or event text uses `eotg_forgotten` (a grep finds it only in the effect). Only the engine's relation-removal tooltip would name them. | localizer + scripter |
| L15 | `events/eotg_augmentation_fracture.txt:2694-2713` (fracture.020 reveal) | `phase3.md:261`: "desc varies by truth × what was done". `phase3.md:554` budgets the reveal at ×6. | 5 variants. The one `desc_true` reads the same whether you arrested, watched, executed or spared a real traitor. (Separate from round-2 H1, which covers the false branch's opinion.) | architect or localizer |
| — | **Unratified value deviations** (commented in the script; the spec was never updated). Each is LOW, owner architect (ratify, or the scripter reverts): | | | |
| L16 | `events/eotg_augmentation_tier1.txt:1204` (tier1.011.c) | `phase4.md:73`: +25 prestige only. | Also risk +2. | architect |
| L17 | `events/eotg_augmentation_tier1.txt:1337,1341` (tier1.012.a) | `phase4.md:78`: no progression lock and no helper. | Adds `eotg_flag_suppress_progression` for 1 year and the reject helper. | architect |
| L18 | `events/eotg_augmentation_tier1.txt:1443` (tier1.013.a) | `phase4.md:86`: no cost. | Adds `eotg_mod_withdrawn_from_court` for 3 months. | architect |
| L19 | `events/eotg_augmentation_tier1.txt:1755` (tier1.016.a) | `phase4.md:105`: no risk. | Risk +2. | architect |
| L20 | `events/eotg_augmentation_tier3.txt:2513` (tier3.019.b) | `phase4.md:430`: risk +5 only. | Also +50 prestige. | architect |
| L21 | `events/eotg_augmentation_tier3.txt:2932` (tier3.023.c) | `phase4.md:451`: risk +3 only. | Also a 5-year `eotg_mod_aug_lesson_martial`. | architect |
| L22 | `events/eotg_augmentation_tier3.txt:1609-1643` (tier3.014.b) | `phase4.md:381`: "you learn the truth (desc)", which can't happen, because the desc is shown before the option. | Reports the result with `send_interface_toast` inside `hidden_effect` (cites vanilla hunt.8540). `UNVERIFIED-VANILLA`: a toast fires from inside `hidden_effect`. | architect (amend the spec to say "toast") |
| L23 | `events/eotg_augmentation_tier2.txt:1822-1832` (tier2.015 → .016) | `phase4.md:257-262`: only a and d say "→ .016", but .016 reads "Outcome from .015 a/d, else rolled". | a, c and d fire .016; b ends the chain. | architect (state which options fire .016) |
| L24 | `common/on_action/eotg_augmentation_on_actions.txt:493-505`; `events/eotg_augmentation_tier1.txt:1273-1284` (tier1.012) | `phase4.md:31,77`: the trigger includes a bare `has_trait = cynical`, which lets a cynical ruler with no pious courtier get the event with no `eotg_pious` and no valid desc. | Drops the bare `cynical` and adds `theologian` courtiers. The script is right. | architect (fix the spec trigger) |

---

## 3. LOW: contradictions inside the specs (all architect)

| # | Spec A | Spec B | Script follows |
|---|---|---|---|
| S1 | Index `cybernetics_v2.md:124`: `eotg_aug_voice` is "char var 0–4". | `phase3.md:459`: Total Integration sets it to 5. | Phase 3 (`effects.txt:915`) |
| S2 | Index `cybernetics_v2.md:104`, `phase3.md:31,453` and `phase5.md:33,181`: `any_owned_story = { type = … }` and `random_owned_story = { type = … end_story = yes }`. | The script uses `story_type = …`, with a `limit` inside `random_owned_story` (`triggers.txt:228,280-290`; `effects.txt:857-858,1109-1110`). | The script. `UNVERIFIED-VANILLA`: confirm `story_type` is the vanilla field (expected), then fix the spec text. |
| S3 | Index T1 `cybernetics_v2.md:177`: Embrace "needs voice ≥ 3 **or** Storm". | `phase3.md:538`: NF **and** Storm **and** (voice ≥ 3 or `eotg_flag_aug_may_embrace`). | Phase 3 (`decisions.txt:502-512`) |
| S4 | Index `cybernetics_v2.md:116`: `eotg_aug_start_containment_regency_effect` takes `KEEPER`. | `phase3.md:130`: `KEEPER` and `SWING`. | Phase 3 (`effects.txt:811-834`) |
| S5 | Index rule 7 (`:70`) and done-item 6 (`:254`): never pick a victim with a bare `random_courtier`. | `phase5.md:152`: the Errand's murder target is "a random courtier". | Phase 5 (L4) |
| S6 | Index T7 `cybernetics_v2.md:183`: "tier3.023 (limbs/senses: clarity odds)". | `phase4.md:455`: the focus read is in tier3.024's roll. | Phase 4 (`tier3.txt:3019-3027`). tier3.023 reads no focus. |
| S7 | Index T7 `:183`: tier3.012 reads nerves focus. | `phase4.md:322,363` define no focus read for First Contact. | The index (on_action `:868-871`, ×1.5). Phase 4 should record it. |
| S8 | `phase4.md:13`: "Below Overclocked, moves are + only." Index rule 4 (`:58`) says only "prefer +". | `phase4.md:123,126`: tier1.018 a/d move an Augmented copycat's risk −10. | `phase4.md:123,126` (`tier1.txt:2097,2155`) |
| S9 | `phase4.md:365`: First Contact option a is "Answer it." | `phase4.md:363` and index §5 item 2 (`:207`) ban "answers". | The ban (loc :1242 "Reply to it.") |
| S10 | Index T1 (`:177`): beat 2 is tier3.012 *First Contact*, and every beat has a "first time you notice it" desc. | `phase4.md:404`: tier3.022's insight outcome advances the voice to 2. The First Contact branch needs voice < 2 (on_action `:862-866`), so The Bleed can consume beat 2 without the scene. tier3.022's `desc_insight` (loc :1297) doesn't introduce the voice. | Both, as written: the gap is in the design. Cap insight at 1, or give .022 a first-contact variant. |
| S11 | `phase3.md:144`: universal options are a–c, trait options d–e. | `phase3.md:315,505-507,529`: 026.d, 007.f and end.020 d/e are universal. | The per-event lines. Reword the convention. |
| S12 | Index rule 6 (`:66`): 3 universal + 1–2 trait options. | `phase2.md:98-100,137`: init.008 has one option, init.012 has one universal + one brave. | Phase 2 |
| S13 | Index `:86`: `on_death` is at `death.txt:7`. | `phase2.md:61`: `death.txt:1`. | — (citation only) |
| S14 | `phase2.md:145`: init.013.e is +5 risk "if the ruler is already augmented". | init.013 fires only for unaugmented rulers (event trigger `initiation.txt:1600-1603`; on_action `:129-133,179-183`). | Drops the dead clause. Delete it from the spec. |
| S15 | `phase5.md:159`: without an heir, only "grievance +1" options remain. | `phase5.md:161,163`: b and d are grievance +2. | The per-option lines (`patron.txt:639-682`) |
| S16 | `phase5.md:228`: `eotg_flag_aug_retinue_permanent` doubles Phase 6 progression "for flagged knights". | `phase6.md:43`: the **liege** has the flag. | Both: the knights carry it (`retinue.txt:654-657`), and the on_action accepts either (`:1338-1341`). |
| S17 | `phase5.md:250`: `eotg_opinion_aug_passed_over` is applied for `years = 5`, matching index §3.4. | `phase5.md:231`: retinue.005.d applies it for `years = 10`. | 10 years (`retinue.txt:699`) |
| S18 | `phase5.md:267`: "5 modifiers and 1 opinion". | `phase5.md:246-249` and index §3.4 list 4 (`_retinue_resentment` dropped). | 4 |
| S19 | `phase6.md:110`: the nr.005 desc "names what changed". | `phase6.md:128`: a generic desc plus the vanilla trait-gain tooltip. | Generic (`nonruler.txt:575,593-595`) |

---

## 4. UNVERIFIED-VANILLA items for the local session
1. **L1:** with `cost = { gold = … }` alone, the decision is unavailable and shows why when it can't be afforded, with no `is_valid_showing_failures_only` needed (`decisions.txt:19-128`).
2. **L7 and L8:** `increase_wounds_no_death_effect` accepts `REASON = wounds` and `REASON = treatment` (`initiation.txt:992,1522-1526`).
3. **L10:** `decision_smith.dds`, `decision_physician.dds`, `decision_knight_kneeling.dds`, `decision_prison.dds`, `decision_realm.dds` and `decision_misc.dds` exist in 1.20 `gfx/interface/illustrations/decisions/`.
4. **L22:** `send_interface_toast` inside `hidden_effect` still shows the toast (`tier3.txt:1609-1643`).
5. **S2:** the story filter field is `story_type` (not `type`) in `any_owned_story` and `random_owned_story` `limit`.

## 5. Suggested order
1. **Architect, one pass:** ratify or reject the "final QA" and "orchestrator ruling" deviations (M3–M7, M9, M11, L12, L16–L21) and fix §3's contradictions. Most of it is spec text.
2. **Scripter:**
   - M8 (envoy as critic) and M7's dead-envoy guard;
   - M1, after the architect's call;
   - M2, M10, L2, L3, L5, L13, once the specs are settled.
3. **Localizer:** M1's success text if the penalty stays, L14 (name the forgotten person), L15 (the sixth reveal variant), and M12 if the voice variant is kept.
4. **Local session:** the five `UNVERIFIED-VANILLA` checks above, plus Tiger and PX on any fix.

---

## 6. Local verification (2026-10-04, orchestrator, eotg-qa and eotg-vanilla-scout)

**Verdict: reliable.** All 12 MEDIUM findings were confirmed and none was refuted. Line numbers in §1–§3 are stale because commit 5a97355 and the uncommitted QA-round-2 work moved them. Search by event ID, not line.

**Corrections to the report:**
- **M7: the kill is already safe.** `eotg_aug_patron_betray_effect` guards the envoy with `is_alive`. Only the patron.006 right portrait (which checks `exists` only) and the two descs, which open with "The envoy comes…", need a dead-envoy guard. There is also an uncovered side case: an envoy who is alive but has left court can still be murdered remotely by options c and e.
- **M8 is understated.** The envoy doesn't need to roll zealous. The `else` branch picks from any adult courtier, so the envoy is a normal-odds target. If picked, the envoy is also drawn twice, as critic and as envoy. This is a real bug.
- **M10:** both options now use `imprison_character_effect`, which applies vanilla tyranny. The gap is stress only.
- **L3 is moot.** end.011 only fires for Seamless characters, and Total Integration strips every personality trait, so trait modifiers in `ai_chance` would be dead code.
- **L5's numbers:** craven gets −15 on 001.d and −45 on 004.e (`minor` = −15, `medium` = −30).
- **The 7 unprefixed scopes noted under check 4 / CB-15 are stale.** They were renamed in the working tree.

**UNVERIFIED-VANILLA items (§4), settled against 1.20.0.3:**
1. **`cost` alone:** this is the vanilla convention. Vanilla never puts a gold check in `is_valid`; its gold tests are AI-only. Whether a reason is shown when the cost is unaffordable is decided by the engine and can only be checked in game.
2. **`REASON = wounds` / `treatment`:** valid. In the no-death effect the value is just `flag:$REASON$`, and both have vanilla death reasons (`death_wounds`, `death_treatment`).
3. **Decision pictures:** all six `decision_*.dds` exist, and every `reference` in the decisions file resolves. Augment a Courtier reuses `eotg_decision_partial_removal.dds`; see CB-05.
4. **Toast in `hidden_effect`:** this is a vanilla pattern (hunt.8540) and is fine.
5. **`story_type` vs `type`:** both are used widely in vanilla. The script is valid, so S2 is only a spec wording tidy-up.
