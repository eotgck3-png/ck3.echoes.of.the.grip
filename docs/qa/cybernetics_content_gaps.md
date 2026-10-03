# Cybernetics — Content Gaps and What's Needed

> **Note (2026-10-03):** the "make fracture risk visible" items (§2.5, §5 Visibility, §6 step 1) conflict with the decision that risk stays hidden (spec Q1). Treat them as input for the deferred "qualitative hint" design call. See [cybernetics_system_overview.md](cybernetics_system_overview.md) §6.

**Date:** 2026-10-03 · **Companion to:** [cybernetics_logic_audit.md](cybernetics_logic_audit.md) (bugs and math). This file covers **content**: what a player can do or experience in the system, where it runs thin, and what to build.

**Constraint on every proposal (temporary-map rule, 2026-10-02):** nothing may depend on specific titles, provinces, characters, cultures or faiths. Everything below uses only vanilla traits, vanilla mechanics, and the mod's own `eotg_` identifiers. Faith reactions go through `zealous`/`cynical`/piety, never a named faith. Every flavor event must read or move `eotg_fracture_risk` (invariant 5).

Event names and identifiers here are **working proposals**. `eotg-architect` fixes the real ones in a spec.

---

## 1. What exists today

| Stage | Events | Shape | Decisions |
|---|---|---|---|
| Initiation | 5 | all single-screen, 2–3 options | — |
| Augmented | 6 | all single-screen, 3 options | Maintenance |
| Enhanced | 6 | all single-screen, 2–3 options | Maintenance, Partial removal |
| Overclocked | 7 | all single-screen, 3 options | Maintenance, Regression |
| Neurofractured | 1 cascade + 6 | all single-screen, 1–3 options | **none** |
| **Total** | **31** | **0 chains, 0 story cycles, 0 realm arcs** | **3** |

---

## 2. Where it's lacking (cross-cutting)

1. **One size only.** Every event is one screen with an immediate result. No follow-ups, no "six months later", no multi-year arcs. The system never builds tension; it just ticks.
2. **Outcomes are fixed.** Picking an option always yields the same result. Only 4 options in the whole system roll anything. Nothing depends on skill (a prowess duel, an intrigue check against tampering) or on traits beyond AI weights.
3. **Traits don't change what the player sees.** One option in 31 events is unlocked by a personality trait. Half of vanilla's personality traits (craven, cynical, sadistic, just, deceitful, shy, trusting, calm, lustful, chaste and more) never appear. The player's character shapes nothing on screen.
4. **Too few reasons to get augmented.** The entry hooks are a wound, wealth, old age and an augmented peer. The strongest reason, **replacing a lost limb or eye**, is missing: `maimed`, `one_legged`, `one_eyed` and `blind` all exist in vanilla, and no implant ever removes them.
5. **The signature resource is invisible.** `eotg_fracture_risk` is a hidden variable. The player can't see how close the cascade is, and options that move it say nothing in their tooltips. A countdown the player can't read builds no dread.
6. **Each tier feels the same.** Every tier has the same levers (prestige, dread, piety, a small risk change) and the same structure. Moving up a tier changes the numbers, not the experience.
7. **Repetition arrives fast.** With 6–7 events per tier and a 2-year cooldown, a ruler sees the full pool in about 10 years and then repeats.
8. **Only landed rulers have a lifecycle.** Knights and courtiers augmented by events never progress, never fracture and never get an event. The system can't show "your champion is losing it".
9. **Neurofractured isn't a different mode.** It has the same three-option shape with more corpses. It has no escalation, no endgame, no realm reaction and no decisions. This is the biggest gap relative to the goal.
10. **Thin decisions.** There are three decisions, none for Neurofractured, none for unaugmented characters who want in, and none that use court physicians or lifestyle traits.

---

## 3. What's needed, by stage

Sizes: **S** = one screen, local nudge. **M** = 2–3 stages over months, a named character, a random or skill-checked result. **L** = multi-year story cycle or realm-wide consequence.

### 3.1 Initiation (have 5 → target ~11)
| Proposal | Size | Hook | What makes it work |
|---|---|---|---|
| **The Prosthetic** | S/M | `maimed` / `one_legged` / `one_eyed` / `blind` | The implant **removes the loss trait**. It's the flagship pitch. With `lifestyle_physician` at court the surgery is cheaper and safer. |
| **The Neural Bridge** | M | `infirm` / `incapable` | A last resort that restores function but starts risk high. Stage 2 rolls rejection. |
| **The Cynic's Argument** | S | `cynical`, high learning | A ruler who *seeks* it out instead of being offered it. Zealous courtiers react. |
| **Back-Alley Surgery** | M (3 stages) | low gold, at war, or `deceitful` | Cheap now; 6–18 months later complications roll **infection / rejection / fine / hidden flaw** (risk +). |
| **The Patron** | L (story cycle) | wealthy, `ambitious` or `greedy` | A syndicate pays for the implant, then calls in favours for years: gold, a hostage, a war. Refusing has teeth. |
| **A Parent's Hardware** | M | parent was augmented (flag set on their death) | The heir is offered the old implants: cheap, but tuned to someone else. |
| **The Sickly Child** | M | child with `ill` / `infirm` | Augment a child to save them. Moral weight: compassionate/just stress, zealous outrage, and the child grows up augmented. |
| **Seek Augmentation** (decision) | — | any eligible ruler | The player chooses when; today it only happens if a random offer lands. The AI uses it through `eotg_ai_wants_augmentation`. |

### 3.2 Augmented (have 6 → target ~12)
**Small** (each with 1–2 trait-gated options):
- *Firmware Itch*: diligent/lazy. Skipping maintenance vs. doing it yourself.
- *Dulled Palate*: gluttonous/temperate. Taste is fading.
- *A Lover's Touch*: lustful/chaste. A partner flinches at the metal (attraction, spouse opinion).
- *The Training Yard*: brave/craven, `lifestyle_blademaster`. The implant outperforms you.
- *The Stare*: shy/gregarious. Court reactions at a feast.
- *A Tithe for Purity*: zealous/cynical. A pious courtier asks for penance.

**Medium:**
- *Rejection*: fever → crisis → roll: recover / implant fails (**back to unaugmented**, gains `wounded_1`) / recover with risk +.
- *The Challenge*: a rival knight challenges the "machine". A prowess check decides it; win or lose has consequences.
- *Copycat*: a vassal gets a botched black-market implant and begs for help. Pay, refuse, or take it as leverage (hook).

**Large:**
- *The Iron Retinue*: augment your knights as an ongoing programme. A gold sink, stronger knights, and a court that grows uneasy. Doubles as the non-ruler lifecycle (§3.6).

### 3.3 Enhanced (have 6 → target ~12)
**Small:**
- *Numbers, Not Faces*: just/arbitrary. You judge a case by pure logic.
- *The Late Grief*: forgiving/vengeful. A death you feel weeks too late.
- *Perfect Recall*: honest/deceitful. The implant remembers every lie told to you.
- *Absent at the Birth*: hook `on_birth_child`. Detachment at your child's birth.
- *Market Ledger*: greedy/generous. The implant optimises taxes ruthlessly.
- *Trust Protocol*: trusting/paranoid. The implant flags your spymaster.

**Medium:**
- *The Bidding War*: two vendors compete for your next upgrade. The choice sets your later risk curve.
- *Tampering*: an enemy attempts to hack the implant. An intrigue check; failure means a temporary loss of control or risk +.
- *The Space Between Us*, extended: today's single spouse event becomes 3 stages ending in reconciliation, estrangement or divorce.

**Large:**
- *The Clinic*: found a clinic at court. It costs gold, cuts maintenance cost, draws syndicate attention, and causes zealous unrest. It gives augmented courtiers somewhere to come from.

### 3.4 Overclocked (have 7 → target ~14)
This tier is a countdown, so the content should *feel* like one.

**Small:**
- *Tremor*: patient/impatient.
- *Phantom Orders*: calm/wrathful. You give an order you don't remember deciding.
- *Heat Spike*: health hit unless you pay.
- *The Feast You Didn't Eat*: gluttonous/temperate.
- *First Contact*: the first time the implant "speaks". It plants the voice that Neurofractured pays off.
- *Sleepwalker*: the court finds you at the walls at night.

**Medium:**
- *Two Machines*, extended: today's peer event escalates to a duel or an alliance.
- *The Plot*: the implant names a conspirator. Act (imprison or execute the saved character) or wait. **Months later a follow-up reveals whether they were guilty**; usually they weren't.
- *The Bleed*: a sudden risk spike. Roll: early cascade, survival with scarring, or survival with insight.
- *The Intervention*: spouse or heir begs you to regress. It leads into the regression decision at a discount.

**Large:**
- *Countdown* (story cycle, starts at risk ≥ 50): omens escalate every few months. The player can *see* the end coming, and the story ends in either the cascade or regression.
- *The Clarity Campaign*: in a war, Overclocked clarity pushes for a decisive engagement. A realm-scale gamble with prestige and risk.

### 3.5 Neurofractured — a different mode (have 6 → target ~25)
Neurofractured should stop playing like a CK3 event chain and start taking control away from the player.

**a. Pressure bands as states.** `eotg_fracture_risk` drifts upward every year (e.g. +8, or +15 when stress ≥ 300). The calm options pull it down. Each band has its own pool:

| Band | Feel | Example events |
|---|---|---|
| 0–29 **Flicker** | eerie, small, wrong | *Wrong Name* (you call your heir by a dead person's name); *Lost Hour*; *The Mirror Doesn't Blink*; *Conversations With No One* |
| 30–59 **Fracture** | violence, lost time | *Containment Breach* (exists); *Blood on the Sleeve* (a victim is found and you don't remember); *The Voice Bargains*; *Scrambled* (a personality trait swaps for its opposite) |
| 60+ **Cascade Storm** | the realm reacts | *The Warrant* (made real: faction or war); *Containment Regency*; *The Massacre* (exists); *The Heir's Choice* |

**b. Mechanics found nowhere else in the mod:**
- **The implant decides.** Some options roll a hidden `random_list`, so the result may not match the text. Some events have one forced option.
- **Unreliable perception.** Events show false information: a plot that isn't there, a "traitor" who is loyal. The truth arrives later.
- **Identity erosion.** Personality traits swap for their opposites, friendships and lovers are forgotten (relations removed), and the desc text changes voice as pressure rises.
- **Named victims.** Every casualty is saved and named. Family can be hit, but rarely, and it's deliberate when it happens.

**c. The realm responds** (all vanilla mechanics):
- *Containment Regency*: spouse or heir takes control through vanilla diarchy/regency effects (`start_diarchy`, used in `events/diarchy_events/`).
- *The Warrant*: a vassal faction forms or a vanilla CB war opens on "cognitive grounds".
- *The Heir's Arc*: a 3–4 event story cycle in which the heir watches, fears, and finally acts (ally, usurper or killer).

**d. Endgames** (Neurofractured has none today; each should be reachable):

| Ending | Route | Result |
|---|---|---|
| **Excision** | decision or event | Surgery with a high death chance. A survivor loses all tiers and gains `maimed`; uses the unused `eotg_clean_all_aug_modifiers`. |
| **Total Integration** | Embrace the Cascade at 60+ | Personality traits wiped, enormous stats, the court abandons you. A unique trait. |
| **Death by Cascade** | pressure maxes out | A dedicated death event and death reason. |
| **Restraints / Abdication** | decision | Hand power on and live out your days confined. |

### 3.6 Non-ruler lifecycle (missing entirely)
Hook `random_yearly_everyone_pulse` (verified in vanilla), filtered to `eotg_is_augmented_any = yes` and `is_playable_character = no`. Augmented knights and courtiers then progress slowly and occasionally fracture, and the event fires **to their liege** ("Your champion attacked a guard"). This is also what makes *Two Machines* and *A Familiar Change* reachable through courtiers.

---

## 4. Decisions needed (have 3 → target ~11)

| Decision | Who | Purpose |
|---|---|---|
| **Seek Augmentation** | unaugmented, eligible | Player-driven entry. AI uses it too. |
| **Remove Implants** | Augmented | The only tier with no exit today. Back to unaugmented, with a withdrawal modifier. |
| **Consult a Physician** | any tier, `lifestyle_physician` at court or in self | Cheaper, stronger maintenance. Uses a lifestyle trait as the gate. |
| **Legitimise Black-Market Implants** | has `eotg_mod_illegal_implants` | Removes that modifier, which is permanent today. |
| **Augment a Retainer** | any tier | Choose a knight or courtier to augment instead of waiting for a random event. |
| **Restraints** | Neurofractured | Fewer violent episodes, prestige and diplomacy cost. |
| **Sedation Regimen** | Neurofractured | Yearly gold, pressure −, skills −. |
| **Name a Keeper** | Neurofractured | Appoint a guardian or regent (diarchy). |
| **Embrace the Cascade** | Neurofractured, 60+ | Path to Total Integration. |
| **Excision** | Enhanced and up | High-risk full removal (§3.5d). |

The existing three need rework too; see the logic audit. Regression is gated on stress, and maintenance can't remove illegal implants.

---

## 5. Supporting script needed

| Type | Needed |
|---|---|
| **Visibility** | A risk-band line in the trait desc (vanilla traits support `triggered_desc`, as `00_traits.txt` does), and a `custom_tooltip` on every option that moves risk ("The implants grow restless" / "...settle"). |
| Scripted effects | `eotg_aug_install_effect` (trait + risk + synergy, replacing 5 copy-pasted blocks); `eotg_aug_remove_all_effect`; `eotg_aug_pick_victim_effect` (weighted, saves the scope); `eotg_aug_scramble_personality_effect`; risk-tooltip wrappers. |
| Scripted triggers | `eotg_has_physical_loss`; `eotg_risk_band_flicker` / `_fracture` / `_storm`; `eotg_has_physician_access`. |
| Modifiers | Separate IDs for temporary buffs (the audit's §1.1); withdrawal; clinic; restraints; sedation; a Total Integration trait. |
| Opinions | Durations on all four existing ones. New positive ones: `reassured`, `grateful_patient`. |
| Story cycles | Patron, Countdown, Heir's Arc, Iron Retinue, Clinic (`common/story_cycles/`). |
| On_actions | `random_yearly_everyone_pulse` (non-rulers), `on_birth_child` (Absent at the Birth). Also a death hook that sets the "parent was augmented" flag on children, for *A Parent's Hardware*. |
| Death reason | `eotg_death_cascade`. |
| Loc | About 80 new events × (title, desc, 4 options) plus decisions, tooltips and band descs. That's roughly 500 keys for the localizer. |

---

## 6. Suggested build order

1. **Visibility and fixes.** Make risk visible and fix the audit's bugs. Every later addition depends on the player being able to read the countdown.
2. **Trait reactivity pass on the 31 existing events.** Add one trait-gated option each, plus full `stress_impact`. This is the cheapest large gain in feel.
3. **Entry hooks and decisions.** The Prosthetic, Seek Augmentation, Remove Implants, Physician.
4. **Neurofractured mode.** Drift and bands, the band pools, the endgames, the Neurofractured decisions. This is the headline differentiator.
5. **Medium chains per tier.** Rejection, Tampering, The Plot, The Bleed.
6. **Large arcs.** Countdown, Patron, Heir's Arc, Regency, Clinic, Iron Retinue.
7. **Non-ruler lifecycle.**

Each phase starts with an `eotg-architect` spec in `docs/specs/`, as the agent workflow requires. Phases 2 and 3 can be specced together.
