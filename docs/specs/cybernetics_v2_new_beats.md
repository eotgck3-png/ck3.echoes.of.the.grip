# Cybernetics v2: new beats (the later heir's arc; the paper after removal)

**Author:** eotg-architect, 2026-10-04
**Authorised by:** the human, relayed by the coordinator 2026-10-04. Both optional beats in [cybernetics_v2_conformance_rulings.md](cybernetics_v2_conformance_rulings.md) §3 are approved: (1) an Heir's Arc for a later heir; (2) a Patron beat after the implants are removed.
**Index:** [cybernetics_v2.md](cybernetics_v2.md). Every rule in index §1 applies, and so do the §5 voice and licensing rules. Where this file amends phase 3 §4 or phase 5 §2, the amendment is marked in those files and this file is the authority.
**Checked against:** the working tree on `v2-space-map` at `dc2b55a`, **plus the uncommitted CB-27 M7/M8 patron fixes**: `eotg_aug_patron_envoy_present`, the envoy exclusion in `eotg_aug_patron_critic_candidate`, the `_absent` descs on patron.006, and the guarded `eotg_aug_patron_betray_effect`. Everything below builds on top of those fixes and changes none of them.

**Gate.** 3 (Systems), on the temporary map under `docs/agent_workflow.md` §5 rule 2. **Not blocked.** Neither beat references a title, province, character, culture or faith.

**Size.** 2 new events (heir.007, patron.008), 2 new desc variants on existing events (heir.003, heir.004), 4 new story variables, 1 new scripted effect (a refactor), 21 loc keys. No new modifier, opinion, flag key type, decision or on_action.

---

## 1. Purpose & gate

**Beat A: The Next in Line.** Today heir.004 ends the Heir's Arc and sets the permanent `eotg_flag_aug_heir_arc_done`, so a ruler whose first heir is executed, dies or is passed over never faces the dynasty again (M11). After this change the arc can run **once more, shorter**, for the next primary heir: one new scene, then the Warning and the Choice again, with descs that remember the first heir. Round 2 is final. Once a ruler has had two climaxes, the arc never fires again. That keeps M11's point (no loop), and the dynasty still gets to answer a ruler who silenced the first heir.

**Beat B: The Paper.** Since M6 the debt survives removal: `eotg_mod_aug_patron_clause` and `_clause_final` stay, and under W3 only the firmware throttle goes. Today the story then just keeps ticking through demands written for a body the syndicate no longer services. One new event fires the first time the Patron's tick finds the owner with no implants. The syndicate re-prices a debt whose collateral is gone ("the syndicate still holds the paper"), and the owner has to pay, sign, go back under the knife, refuse, or (if just) take the contract to their own court.

Gate 3. Not blocked.

---

## 2. Signature resource

| Beat | Resource | How it couples (index §1 rule 4) |
|---|---|---|
| A | `eotg_fracture_risk` on the ruler, and the story's `eotg_heir_dread`, which weights heir.004 | Every heir.007 option moves risk **and** dread, like heir.001. (A Seamless owner's risk moves are no-ops by design in `eotg_add_fracture_risk`; dread still moves.) |
| B | The Patron story's `eotg_grievance` (and the story's existence). The owner has no implants, so `eotg_fracture_risk` does not exist and must not be recreated (QA round 2 M3). | c **changes tier** (re-install). d and e(failure) move `eotg_grievance`. a, b and e(success) **end the debt**. This is the "owner with no implants" coupling the human allowed. |

---

## 3. Identifier table

### 3.1 New

| Key | Type | Owner | Notes |
|---|---|---|---|
| `eotg_aug_heir.007` | event (namespace `eotg_aug_heir`, exists) | scripter | *The Next in Line* (lore-keeper to confirm the title) |
| `eotg_aug_patron.008` | event (namespace `eotg_aug_patron`, exists) | scripter | *The Paper* (lore-keeper to confirm the title) |
| `eotg_round` | story variable on `eotg_story_aug_heir_arc` (1 or 2) | scripter | Set to 1 in `on_setup`, 2 at the reprise |
| `eotg_prior_heir` | story variable (character) | scripter | The first heir, copied from `eotg_heir` at the reprise |
| `eotg_prior_choice` | story variable (`flag:ally` / `usurp` / `kill_failed` / `kill_success` / `executed`) | scripter | Written by heir.004 (immediate) and heir.004 `kill_c` |
| `eotg_paper_served` | story variable on `eotg_story_aug_patron` (bare, one-shot) | scripter | Set by the tick when it fires patron.008 |
| `eotg_aug_heir_seed_dread_effect` | scripted effect (story scope) | scripter | **Refactor only**: the five dread seeds now inlined in the arc's `on_setup` (absent at birth, intervention refused, estranged parent, opinion < −20, child patient −1 with clamp), moved verbatim into an effect so `on_setup` and the reprise share them |

Story variables follow the existing `eotg_` prefix convention for story variables (`eotg_heir`, `eotg_stage`, `eotg_demand` …).

### 3.2 Reused (no new key)

`eotg_flag_aug_heir_arc_done`, `eotg_flag_aug_heir_ally`, `eotg_flag_aug_heir_keeper`, `eotg_opinion_aug_{reassured,fear,admiration}`, `eotg_mod_aug_lesson_learning`, `eotg_mod_aug_patron_clause`, `eotg_mod_aug_patron_clause_final`, `eotg_mod_aug_excision_recovery`, `eotg_aug_initiate_effect`, `eotg_add_fracture_risk`, `eotg_aug_patron_pay_effect` / `eotg_aug_patron_can_pay`, `eotg_aug_patron_grievance_effect`, `eotg_aug_patron_envoy_present`, the stress helpers `eotg_aug_stress_{cruelty,surgery}_effect`.

### 3.3 Not new

No modifier, opinion, trait, character flag, decision, on_action, namespace, icon or art. Art: both events use existing themes and portraits.

---

## 4. File placement

| File | Change |
|---|---|
| `common/story_cycles/eotg_augmentation_stories.txt` | Heir arc: `on_setup` (round, seed refactor), new dormant/reprise entry, branch-1 guard. Patron: one new tick entry **in both cadences** (the two copies stay identical). Header comments updated. |
| `common/scripted_effects/eotg_augmentation_effects.txt` | New `eotg_aug_heir_seed_dread_effect`. `eotg_aug_total_integration_effect`: add a stage guard (§5.1 step 5). |
| `events/eotg_augmentation_heir.txt` | New heir.007. heir.003: desc variant. heir.004: desc variant, prior-choice write, round-dependent ending. `kill_c`: prior-choice write. File header updated. |
| `events/eotg_augmentation_fracture.txt` | fracture.026 b: add a stage guard (§5.1 step 5). Nothing else. |
| `events/eotg_augmentation_patron.txt` | New patron.008. File header updated. **No change to .001–.007.** |
| `localization/english/eotg_augmentation_l_english.yml` | 21 keys (§7). UTF-8 BOM. |

No new folder. No `replace_path`.

---

## 5. Wiring

### 5.1 Beat A: the later heir (`eotg_story_aug_heir_arc`)

**Design choice: a shorter follow-on, not a re-run.** Re-running heir.001 *Concern* and fracture.005 *What the Heir Saw* for the second heir would be false. That heir lived through round 1 and has already seen the ruler break, and has watched what happened to the person who stood where they stand now. So round 2 opens with one new scene (heir.007), where the new heir arrives knowing, and then goes straight to the Warning (heir.003) and the Choice (heir.004), each with a desc that names the predecessor. That makes 3 beats instead of 5, and it ends for good.

**Design choice: the same story, kept alive.** The arc is not restarted from the on_actions. heir.004 parks the story in a **dormant stage 5** instead of ending it, and the story's own tick looks for the next heir. Consequences:
- The two on_action start sites (NF step 2, and OC per balance §5.8(a)) and `eotg_flag_aug_heir_arc_done` are **unchanged**. The flag still means "no on_action ever creates a second arc story for this ruler". Index §1 rule 5 holds: the story's `effect_group` timing (`years = { 1 2 }`, `chance = 70`) is the only pacing. There is no cooldown, flag or timer.
- The existing exits still apply in dormancy: landless (sets the done flag, ends), regressed or left the system (branch 0, ends), Excision (ends), owner death (ends).

**Steps (scripter):**

1. **`on_setup`.** Add `set_variable = { name = eotg_round  value = 1 }`. Replace the five inlined seed blocks with `eotg_aug_heir_seed_dread_effect = yes`, keeping the same order and the same clamp. Behaviour is unchanged.

2. **New dormant entry.** Insert it in the `first_valid` **after branch 0** (left the system / regressed) and **before branch 1** (heir changed). Its trigger is `var:eotg_stage = 5` **only**, so a dormant story with no successor matches this entry, does nothing, and never falls through to branch 1:
   ```
   triggered_effect = {
       trigger = { var:eotg_stage = 5 }
       effect = {
           if = {
               limit = {
                   story_owner = {
                       primary_heir ?= {
                           is_alive = yes
                           age >= 14
                           NOT = { this = scope:story.var:eotg_heir }
                       }
                   }
               }
               set_variable = { name = eotg_prior_heir  value = var:eotg_heir }
               set_variable = { name = eotg_heir  value = story_owner.primary_heir }
               set_variable = { name = eotg_round  value = 2 }
               set_variable = { name = eotg_heir_dread  value = 0 }
               eotg_aug_heir_seed_dread_effect = yes
               # what the new heir watched happen to the last one
               if = { limit = { var:eotg_prior_choice = flag:executed }  change_variable = { name = eotg_heir_dread  add = 2 } }
               else_if = {
                   limit = { OR = { var:eotg_prior_choice = flag:usurp  var:eotg_prior_choice = flag:kill_failed } }
                   change_variable = { name = eotg_heir_dread  add = 1 }
               }
               clamp_variable = { name = eotg_heir_dread  min = 0  max = 10 }
               set_variable = { name = eotg_stage  value = 2 }
               story_owner = {
                   remove_character_flag = eotg_flag_aug_heir_ally    # that ally is gone (fracture.027 reads it)
                   trigger_event = { id = eotg_aug_heir.007  days = { 1 30 } }
               }
           }
       }
   }
   ```
   (If `var:eotg_prior_heir` is missing, NOT `this = …` must still evaluate. When `var:eotg_heir` can be unset, guard it with `exists = scope:story.var:eotg_heir` in an OR, as branch 1 already does.)
   - **Who counts as "a later heir":** anyone who is now the primary heir and is not the round-1 heir. That covers every case the human named: the first heir **died** (any cause), was **executed** in heir.004 `kill_c`, or was **sidelined** after a usurp or a failed kill. "Sidelined" means **no longer primary heir**: disinherited through vanilla, passed over by a succession-law change, or dropped out of the line. An imprisoned usurper who is *still* the primary heir is not sidelined, because there is no later heir yet. The player's lever there is vanilla disinheritance. This is deliberate. The arc follows `primary_heir`, as branch 1 already does.
   - An heir under 14 is waited for: the entry matches and does nothing until they turn 14.

3. **Branch 1 guard.** Add `var:eotg_stage < 5` to branch 1's trigger. This is belt-and-braces, because step 2 already shadows it. Within round 2, branch 1 still passes the arc to a third heir one stage back if the second heir dies mid-arc, exactly as in round 1. That is a hand-off inside a round, not a third round.

4. **heir.004 ending (immediate, `hidden_effect` block at the end).** Keep `add_character_flag = eotg_flag_aug_heir_arc_done`. Replace the unconditional `end_story` with:
   ```
   scope:eotg_heir_story = {
       set_variable = { name = eotg_prior_choice  value = scope:eotg_heir_choice }
       if = {
           limit = { has_variable = eotg_round  var:eotg_round >= 2 }
           end_story = yes
       }
       else = { set_variable = { name = eotg_stage  value = 5 } }
   }
   ```
   In **`kill_c`** ("Execute them."), before the death, add `scope:eotg_heir_story = { set_variable = { name = eotg_prior_choice  value = flag:executed } }`. The option runs after the immediate, so it overwrites `kill_failed`. On kill success the owner dies in heir.006, and `on_owner_death` ends the dormant story as it does now.

5. **Stage writers outside the story must not wake a dormant arc.** Each of these gets `var:eotg_stage < 4` added to the `limit` of its `random_owned_story`:
   - `eotg_aug_total_integration_effect` (sets stage 3);
   - fracture.026 b "Beg the heir to act" (sets stage 3, dread −2).

   Without the guard, Seamless or a Last Lucid Moment would fire heir.004 a second time against the **same** heir. With it, a Seamless owner in round 2 (stage 2) still jumps to the Choice, as intended. `eotg_decision_aug_appoint_warden`'s AI weight reads `var:eotg_stage >= 2`. A dormant arc (5) still counts as "the arc reached the Warning", which is true, so it is unchanged.

6. **Descs (heir.003, heir.004).** For round 2 a successor opener replaces the base desc. heir.003: wrap the single desc in a `first_valid` whose first entry is `triggered_desc = { trigger = { scope:eotg_heir_story.var:eotg_round ?= 2 } desc = eotg_aug_heir.003.desc_successor }`, falling back to `eotg_aug_heir.003.desc`. heir.004: do the same for the leading `desc = eotg_aug_heir.004.desc` only. The premonition and outcome descs that follow are unchanged. Both immediates already save `scope:eotg_heir_story` before the desc is shown. In each immediate, also save `var:eotg_prior_heir` as `scope:eotg_prior_heir` (`var:eotg_prior_heir ?= { save_scope_as = eotg_prior_heir }`) for the loc.

**Pacing (no cooldown).**
- The earliest reprise is the first tick after heir.004 (1–2 years, 70% per roll). heir.003 comes one tick later, and heir.004 one tick after that.
- A second climax lands about 3–6 years after the first. Seamless or an absent successor makes it later.
- Three beats over that span is in line with round 1's density.

#### heir.007 *The Next in Line*

- Fired by: the dormant entry (step 2), to the owner.
- Event `trigger` (a world-state guard mirroring the branch; no flags): `any_owned_story = { story_type = eotg_story_aug_heir_arc  exists = var:eotg_heir  var:eotg_heir = { is_alive = yes } }`.
- `immediate`: same `hidden_effect` save as heir.001 (`scope:eotg_heir_story`, `scope:eotg_heir`), plus `var:eotg_prior_heir ?= { save_scope_as = eotg_prior_heir }`.
- Portraits:
  - left: root, `worry`.
  - right: `scope:eotg_heir`, `worry`.
  - lower right: `scope:eotg_prior_heir`, with `animate_if_dead = yes`, `animation = dead` when not alive, else `stress`. Precedent: heir.005 for the dead portrait; vanilla `ep3_story_cycle_admin_eunuch.8010` shows the dead predecessor beside the successor.
- Desc: `first_valid`:

  | Trigger | Key |
  |---|---|
  | `var:eotg_prior_choice = flag:executed` (read on the story) | `desc_executed` |
  | `scope:eotg_prior_heir = { is_alive = no }` | `desc_dead` |
  | otherwise | `desc_displaced` |

- Options (choice event, index §1 rule 6: 3 universal + 2 trait-gated). Each option moves `eotg_heir_dread` on `scope:eotg_heir_story` and risk on root. Like heir.001, there is no stage change in the options; the tick set stage 2.

| Opt | Text (loc) | Effect | Dread | Risk | ai_chance |
|---|---|---|---|---|---|
| **a** | "You will not end as they did." | heir `eotg_opinion_aug_reassured` 5y | −1 | −3 | base 30; +20 compassionate; +10 gregarious; −10 paranoid |
| **b** | "Then you know what I am." | heir `eotg_opinion_aug_fear` 10y; `eotg_aug_stress_cruelty_effect` | +1 | +3 | base 30; +20 arrogant; +20 callous; −20 compassionate |
| **c** | "Learn from it. Keep me, if it comes to that." | heir `eotg_flag_aug_heir_keeper`; heir `eotg_opinion_aug_admiration` 5y | −1 | −5 | base 30; +20 humble; +20 trusting; −20 paranoid |
| **d [honest]** | "Tell them how it ended." | heir `eotg_opinion_aug_reassured` 5y and `eotg_mod_aug_lesson_learning` 5y; **if** prior choice is `executed`, `add_prestige = -50` (the admission costs) | −1 | −3 | base 30; +30 honest; +10 just |
| **e [paranoid]** | "They will try what the last one tried." | heir `eotg_opinion_aug_fear` 10y; `eotg_aug_stress_cruelty_effect` | +2 | +5 | base 30; +30 paranoid; +10 vengeful |

Universal options do not dominate one another: a is calm and cheap, b buys fear at a risk cost, and c gives the best risk relief but hands the heir the keeper flag, which strengthens their hand in heir.004 (ally +20, and diarchy eligibility in heir.003 c). Trait options follow the amended rule 6 and may be the better deal for their trait.

### 5.2 Beat B: the paper (`eotg_story_aug_patron`)

**Depends on (ratified 2026-10-04):** the tick order in phase5 §2.3, the presence gate `eotg_aug_patron_envoy_present` and the betrayal cost table in phase5 §2.4 (.006), and the throttle inside the augmented branch of `eotg_aug_patron_betray_effect` (rulings §4).

**Where it fires.** A new `triggered_effect` in the Patron tick, in **both** cadences (`years = { 2 3 }` and the read-terms `years = { 3 4 }`). The two copies stay identical, per the file's own rule. Order inside `first_valid`:
1. landless → end (unchanged);
2. Neurofractured write-off (unchanged; an owner with no implants is never Neurofractured);
3. **NEW: the paper**;
4. the existing `always` entry (.006 / .007 / .002–.005).

```
triggered_effect = {
    trigger = {
        NOT = { has_variable = eotg_paper_served }
        var:eotg_demand < 4
        var:eotg_grievance < 3
        story_owner = { eotg_is_augmented_any = no }
        var:eotg_envoy ?= {
            is_alive = yes
            is_courtier_of = scope:story.story_owner
        }
    }
    effect = {
        set_variable = eotg_paper_served
        story_owner = { trigger_event = { id = eotg_aug_patron.008  days = { 1 30 } } }
    }
}
```

- **Once per story.** `eotg_paper_served` is set in the tick, which keeps the tick as the cooldown authority (index §1 rule 5). The event checks no flag. Vanilla shape: `story_cycle_pledge_loyalty_to_liege_overdue.txt:188-207`.
- **Final Demand first.** If the Final Demand is already due (demand ≥ 4 or grievance ≥ 3), the entry yields and .006 comes as it does now. The .006 descs already work for an absent envoy (M7).
- **Envoy present.** If the envoy is dead or gone, the entry yields to the existing `.007` *A New Envoy*, and the paper comes on the next tick with the new envoy. So patron.008 needs no `_absent` desc.
- **Re-install, then remove again.** If the owner re-installs (c) and later removes the implants a second time, nothing new fires, because the variable is set. The normal demand sequence continues, as it does today.

**How the story can end, for an owner with no implants:**

| Path | Result |
|---|---|
| .008 a, pay the principal | settled, story ends |
| .008 b, sign the lien | `_clause_final` (permanent), story ends |
| .008 e success [just] | contract voided under the holder's own law, story ends |
| .008 d, refuse | grievance raised to 3, so the **next tick fires .006** (betrayal tone); every .006 option ends the story |
| .008 e failure | grievance +1, the sequence continues, the debt is still live |
| .008 c, re-install | back in the system, the sequence continues from the current demand |
| the existing exits | landless, owner death |

#### patron.008 *The Paper*

- Fired by: the tick entry above, to the owner.
- Event `trigger` (a world-state guard mirroring the entry): `eotg_aug_has_patron = yes`, `eotg_is_augmented_any = no`.
- `immediate`: the standard patron save (`scope:eotg_patron_story`, `var:eotg_envoy ?= { save_scope_as = eotg_patron_envoy }`), as in .002.
- Portraits:
  - left: root, `thinking`.
  - right: `scope:eotg_patron_envoy` with `trigger = { eotg_aug_patron_envoy_present = yes }` (the M7 pattern), `steward`.
- Theme `stewardship_wealth_focus`.
- Desc: `eotg_aug_patron.008.desc`, plus `triggered_desc = { trigger = { has_character_modifier = eotg_mod_aug_patron_clause }  desc = eotg_aug_patron.008.desc_clause }` (the exclusivity clause still bills for technicians with nothing left to service; this is the M6 ruling made visible).
- **No `after` demand increment.** This is not one of the four demands; it is the re-pricing. Options end the story themselves where they should.

| Opt | Text (loc) | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| **a** | "Pay off the principal." | `eotg_aug_patron_can_pay = { BASE = major_gold_value  MULT = 1 }` | `eotg_aug_patron_pay_effect = { BASE = major_gold_value  MULT = 1 }` (the terms scale it); `scope:eotg_patron_story = { end_story = yes }` (on_end removes the clause and sends the envoy to the pool) | base 30; +20 honest; +10 diligent; −20 greedy |
| **b** | "Sign the lien." | — (the ungated fallback) | `remove_character_modifier = eotg_mod_aug_patron_clause`; `add_character_modifier = eotg_mod_aug_patron_clause_final`; end story | base 30; +20 content; +10 patient; −20 ambitious |
| **c** | "Let them put it back." | `NOT = { has_character_modifier = eotg_mod_aug_excision_recovery }` (the body will not take it yet) | `eotg_aug_initiate_effect = yes`; `eotg_add_fracture_risk = { AMOUNT = 15 }` (their firmware, and it remembers); `add_character_modifier = eotg_mod_aug_patron_clause` (open-ended; on_end removes it); `eotg_aug_stress_surgery_effect = yes`. **Tier change.** Story continues. | base 30; +20 ambitious; −20 zealous; −20 paranoid |
| **d** | "The paper is worth nothing now." | — | grievance up to 3 (`if = { limit = { scope:eotg_patron_story.var:eotg_grievance < 3 } scope:eotg_patron_story = { set_variable = { name = eotg_grievance  value = 3 } } }`); `scope:eotg_patron_envoy ?= { add_opinion = { modifier = eotg_opinion_aug_disgust  target = root  years = 5 } }`; `add_prestige = 50` | base 30; +20 stubborn; +10 wrathful; −20 craven |
| **e [just]** | "Let my own court read the contract." | `has_trait = just`; `trait = just` | `random_list`: **50** (+15 if `stewardship >= 12`) success, desc `.e.success`: `add_prestige = 100`, end story. **50** failure, desc `.e.failure`: `add_prestige = -100`, `eotg_aug_patron_grievance_effect = { AMOUNT = 1 }`. `stress_impact = { just = minor_stress_impact_loss }` | base 30; +30 just; +10 honest |

**Balance.**
- a costs gold now; b costs income forever; c costs the body back and resumes the debt; d is free now but brings the Final Demand next tick. None dominates.
- e is a just ruler's due process. It is a gamble on prestige, consistent with the trait-option rule.
- c is the only way back into the system from this event. It re-enters at tier 1 with risk 15 and the settling flag from `eotg_aug_initiate_effect`, which is a real cost for someone who chose to leave.

**Known consequence (deferred, §10).** If d leads to .006 and the owner betrays the syndicate there, the owner has no hardware to punish. The W3 follow-up is now in (throttle inside the augmented branch of `eotg_aug_patron_betray_effect`; rulings §4), so the only cost is the envoy's murder (the murder stress helper, plus vanilla murder consequences). If the envoy has also died or left court by the time .006 fires, only d [deceitful] is left as a betrayal route, and its failure costs nothing but lie stress (phase5 §2.4 cost table). This spec does not touch the betray effect.

---

## 6. Vanilla precedent

| Mechanic | Vanilla | Use here |
|---|---|---|
| A story outlives its central character and re-targets a successor instead of ending | `common/story_cycles/ep3_story_cycle_admin_eunuch.txt:145-182` (the tick tests `var:eunuch` dead / imprisoned / gone); `events/dlc/ep3/ep3_story_cycle_admin_eunuch_events.txt:6021-6097` (8010: the dead predecessor's portrait, `scope:story = { set_variable = { name = eunuch value = scope:student } }`, story continues; or `end_story`) | Dormant stage 5 → reprise; heir.007's dead-predecessor portrait |
| Re-target the arc to the new primary heir | The mod's own branch 1, from `story_cycle_murders_at_court.txt:131-160` (var checks in a `first_valid` tick) | Unchanged, guarded |
| One-shot story variable set in the tick before firing an event | `common/story_cycles/story_cycle_pledge_loyalty_to_liege_overdue.txt:188-207` (`NOT = { has_variable = …_received_intro_event }`, then `set_variable = …` and `trigger_event`) | `eotg_paper_served` |
| Dead portrait | `animate_if_dead = yes` (already in heir.005) | heir.007 lower right |
| Option outcome roll with a desc per branch | patron.002.e (the mod's existing shape, vanilla `random_list` with `desc`) | patron.008.e |
| A ruler-only story ends when landless | `story_cycle_take_mandate_of_heaven.txt:172-189` (already cited in the file) | Unchanged in both stories |

No deviation from vanilla shape.

---

## 7. Loc surface (eotg-localizer)

21 keys, dot form (index §0), UTF-8 BOM, bare `[x.GetName]` / `[x.GetFirstName]`, one definition each. US spelling. No `replace/` override.

**heir (11)**

| Key | Content |
|---|---|
| `eotg_aug_heir.007.t` | "The Next in Line" (pending lore-keeper) |
| `eotg_aug_heir.007.desc_executed` | `[eotg_heir.GetFirstName]` comes to you knowing that you had `[eotg_prior_heir.GetFirstName]` put to death. They are the heir now, because the last one is not. Measured and frightened. |
| `eotg_aug_heir.007.desc_dead` | `[eotg_prior_heir.GetFirstName]` is dead. `[eotg_heir.GetFirstName]` was there for all of it and has inherited the question along with the place. No accusation about the death itself. |
| `eotg_aug_heir.007.desc_displaced` | `[eotg_prior_heir.GetFirstName]` lives, but no longer stands first. `[eotg_heir.GetFirstName]` saw how that happened. |
| `eotg_aug_heir.007.a`–`.e` | the option texts in §5.1 |
| `eotg_aug_heir.003.desc_successor` | heir.003's Warning, from a second heir who has seen it said once before, by `[eotg_prior_heir.GetFirstName]`. Shorter and less rehearsed. |
| `eotg_aug_heir.004.desc_successor` | heir.004's opener for a second heir: the question is settled, and they know how it went the last time. The outcome descs that follow (`desc_ally` …) are unchanged and must still read correctly after it. |

**patron (10)**

| Key | Content |
|---|---|
| `eotg_aug_patron.008.t` | "The Paper" (pending lore-keeper) |
| `eotg_aug_patron.008.desc` | The syndicate learns that the hardware it paid for is out of you. The debt is not. The paper names you, not the implants. Write it so it reads true whether the envoy delivers it in person or their office does. |
| `eotg_aug_patron.008.desc_clause` | (appended) The exclusivity clause still bills each month for technicians who have nothing left to service. |
| `eotg_aug_patron.008.a`–`.e` | the option texts in §5.2 |
| `eotg_aug_patron.008.e.success` | Your court finds the contract has no standing under your law. |
| `eotg_aug_patron.008.e.failure` | Your court upholds the contract. The syndicate notes that you asked. |

**Register.**
- There are no **[voice]** lines. patron.008's owner has no implants, so no voice.
- heir.007, heir.003.desc_successor and heir.004.desc_successor reach a Neurofractured or Seamless owner. If they mention the implant at all, index §5 items 1–2 bind: internal, logs, forecasts; none of the banned words.

---

## 8. Lore constraints

- **The syndicate is never named** (index §5.7): "the syndicate", "the syndicate envoy". No Helix, Pale Hand, Consortium, Compact, Continuity, Rooks, "Corp"/"Co.", no white-glove imagery.
- **Licensing and law are local and unnamed** (index §5.3). patron.008.e is the holder's **own** court, never a galactic, League or interstellar authority. 866 AG: there is no Galactic League yet (CLAUDE.md §Canon).
- **No monotheistic invocations; "self", not "humanity"** (index §5.4–5.5). heir.007 fires for every faith and species.
- **Medieval leaks** (index §5.6): residence, not palace; the logs or archivists, not scribes.
- **Voice register** (index §5.1–5.2) for any implant line in heir text.
- **Nikios Khanate:** nothing here touches it (invariant 9).
- **Route to lore-keeper:** the titles *The Next in Line* and *The Paper*; and whether a holder's court can void a syndicate contract in the setting's 866 AG legal landscape (the brief says the black market lives under "the holder's own law and clergy", which this reads as allowing it).

---

## 9. Definition of done

0. **Validation, all three clean** on the touched files, except the known-benign items in `CLAUDE.md` §Validation: Tiger 1.17.0 (scratch descriptor), `docs/tools/px_lsp_diagnostics.js`, `docs/tools/px_vocab_check.py`. Tiger is the only one that checks scope (`var:eotg_prior_heir` in story scope, `scope:story.var:eotg_heir` inside `primary_heir`).
1. **Reachability (PX event graph):** heir.007 is reached from `eotg_story_aug_heir_arc`; patron.008 from `eotg_story_aug_patron` in both cadences. Neither is fired by anything else.
2. **Coupling (QA audit 8):** every heir.007 option calls `eotg_add_fracture_risk` and moves `eotg_heir_dread`. patron.008 c changes tier, and d and e(failure) move `eotg_grievance`.
3. **No cooldown in an event trigger:** neither new event's `trigger` reads `eotg_paper_served`, `eotg_round`, `eotg_flag_aug_heir_arc_done` or any cooldown flag.
4. **heir.004** ends the story only when `eotg_round >= 2`; otherwise it sets `eotg_stage = 5`. It still sets `eotg_flag_aug_heir_arc_done` in both cases. The on_action start sites are byte-identical to before.
5. `eotg_aug_total_integration_effect` and fracture.026 b set stage 3 only when `var:eotg_stage < 4`.
6. The two Patron tick copies are identical (a diff of the two `first_valid` blocks shows no difference).
7. `grep -n "eotg_paper_served" common events` shows one `set_variable` and one `has_variable` per cadence, and nothing in `events/`.
8. Loc: all 21 keys exist once, BOM, no `[scope:`.
9. **Human, in game (temporary map):**
   - NF count with an adult primary heir and a second child aged 14+. Drive the arc to heir.004 (console-set the story's stage to 3). Take kill_failed, then "Execute them."
     - Within 1–2 ticks heir.007 fires with `desc_executed`.
     - Then heir.003 and heir.004 fire with the successor opener.
     - After the second heir.004 the story is gone (`any_owned_story`), and no arc ever starts again, even with a third heir.
   - Same setup, but take Ally. The first heir stays primary heir, and **no** reprise fires for 5+ years.
   - Accept the Patron, take Remove Implants. On the next tick, patron.008 fires (with `desc_clause` if .003 a/c/d was taken).
     - Pick d: the next tick fires .006 in betrayal tone.
     - Reload and pick c: the ruler is tier 1 with the clause, and the next tick resumes the demand sequence.
   - Patron owner who removes implants while the envoy is dead: .007 comes first, then .008 on the following tick.

---

## 10. Deferred

- **A third round.** The arc ends after round 2. Two climaxes per ruler is the cap. M11's reason (no loop) still holds past two.
- **Syndicate retaliation against an owner with no hardware** (after .008 d → .006 betrayal). Today the only cost is the envoy's murder. A real reprisal (a vanilla hostile scheme by a created agent, or a claim on revenues) is new scope. It would also change `eotg_aug_patron_betray_effect`, which this spec was asked not to touch beyond need. For the human.
  - **Same open question, two more cases (from CB-27 M7, recorded 2026-10-04; not designed).** Both come from .006 firing before .007 (phase5 §2.3) with the envoy dead or gone, and both are in phase5 §2.4's cost table.
    - **Envoy absent: no betrayal route for a non-deceitful owner.** c and e need the envoy present, and d is deceitful-only. Such an owner can only sign (a) or buy out (b). This holds whether or not the owner has implants.
    - **No implants, envoy absent, d fails: lie stress only.** The betray effect neither kills (no envoy) nor punishes (no hardware), and the murder stress is gated on presence. In practice d is a free exit for a deceitful owner who has left the system.
  - One answer settles all three. Whatever reprisal the syndicate takes when it cannot reach the hardware, or when its envoy is not there, is the human's call. Until then the script stays as built.
- **Inherited patron debt** (phase 5 §5), unchanged. The paper still dies with the owner.
- **A paper beat for a Neurofractured owner.** The write-off already covers it (balance §5.8).
- **Dependencies, not deferrals:**
  - **W3** (the throttle removed in `eotg_clean_all_aug_modifiers`) and the rulings §2 follow-up (throttle into the augmented branch of the betray effect) are **both in the working tree** as of 2026-10-04: uncommitted, QA-passed for script, ratified in rulings §4.
  - patron.008 does not depend on them, and its loc must not mention the throttle.

---

### HANDOFF
- status: done
- next: eotg-lore-keeper
- ask: Review docs/specs/cybernetics_v2_new_beats.md: the titles "The Next in Line" (heir.007) and "The Paper" (patron.008); whether a holder's own court voiding a syndicate contract (patron.008.e) fits 866 AG canon; the loc briefs in §7 against index §5. Then hand to eotg-scripter (§4–§5; after CB-27 M7/M8 and W3 are committed), then eotg-localizer (§7), then eotg-qa (§9).
- files: docs/specs/cybernetics_v2_new_beats.md; amendment notes in docs/specs/cybernetics_v2.md, docs/specs/cybernetics_v2_phase3.md, docs/specs/cybernetics_v2_phase5.md, docs/specs/cybernetics_v2_conformance_rulings.md
- needs-loc: 21 keys, §7 (eotg_aug_heir.007.*, eotg_aug_heir.003.desc_successor, eotg_aug_heir.004.desc_successor, eotg_aug_patron.008.*)
- needs-lore: the two titles; patron.008.e's local-court premise
- needs-human: §10, syndicate retaliation against an owner with no hardware (optional new scope); the §9 item 9 in-game checks after the build

---

## 11. Lore review (eotg-lore-keeper, 2026-10-04): binding loc wording

**Verdict:** no canon contradiction and no design change. Both titles are approved. patron.008.e's premise is approved: there is no authority above the polity at 866 AG. Its text always says "your court" / "your law", never an abstract or higher authority, never the liege's law, and "court" stays faith-neutral.

**Must-fix: use this exact text.**
- **N1** `eotg_aug_heir.007.desc_dead`: "[eotg_prior_heir.GetFirstName] is dead, and [eotg_heir.GetFirstName] is first in line now. They know what was asked of the last heir, and what you answered. They have inherited the question along with the place."
- **N2** `eotg_aug_heir.003.desc_successor`: "[eotg_heir.GetFirstName] has brought the incident logs and a date. This has been said to you once before, by [eotg_prior_heir.GetFirstName], and [eotg_heir.GetFirstName] knows how that went. They do not rehearse it. 'Step aside,' they say, 'or I will make you.'"
- **N3** `eotg_aug_heir.004.desc_successor`: "[eotg_heir.GetFirstName] has decided. They know how this went the last time, and they have decided anyway. The question is settled, and only the method remains." This one must not name `eotg_prior_heir`, because the descs that follow open with "They…" and would read as the predecessor.
- **N4** `eotg_aug_patron.008.desc`: "The hardware is out of you, and the syndicate knows it. The debt is not. The paper names you, not the implants, and the syndicate still holds the paper. The terms have been re-priced for a body it no longer services."
- **N5** `eotg_aug_patron.008.e.success`: "Your court finds the contract has no standing under your law. The syndicate does not contest it. There is nowhere else to take it."

**Suggested renderings, adopted:**
- `heir.007.desc_executed`: "[eotg_heir.GetFirstName] comes to you knowing that you had [eotg_prior_heir.GetFirstName] put to death. They are first in line now because the one before them is not. They speak evenly, and keep their hands where you can see them." Never render the heir's "voice": that word is reserved for the implant.
- `heir.007.desc_displaced`: "[eotg_prior_heir.GetFirstName] lives, but no longer stands first. [eotg_heir.GetFirstName] does, and knows how the change was made."
- `heir.007.a`: "What happened to them will not happen to you."
- `patron.008.b`: "Sign the lien on my revenues."
- `patron.008.e.failure`: "Your court upholds the contract. The syndicate is sent a copy of the ruling."
- `patron.008.desc_clause` starts with `\n\n`.

**Noted for a later loc pass (out of scope):** the shipped `eotg_aug_heir.001.e` "They want the throne." uses a medieval word. If a region brief ever puts the Pill Boys (a First-Era "criminal syndicate in salvage economy") in play at 866, keep salvage imagery out of Patron text.
