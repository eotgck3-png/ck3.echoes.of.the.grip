# Cybernetics — System Overview and Goals

**Date:** 2026-10-03 · **State described:** the files on disk after the 2026-10-03 track conversion ([docs/specs/cybernetics_track.md](../specs/cybernetics_track.md)).
**Related:** [cybernetics_logic_audit.md](cybernetics_logic_audit.md) (bugs and math) · [cybernetics_content_gaps.md](cybernetics_content_gaps.md) (what to build). Both were written against the pre-conversion four-trait version; §6 says which of their findings still stand.

---

## 1. What the system is

Cybernetic augmentation is a voluntary, escalating body-modification path for rulers. Each step up gives real mechanical power and costs more socially, psychologically and in stress than the last. Past the top step waits **Neurofracture**: a permanent, irreversible collapse with its own violent event pool.

It is the first **mod-exclusive system** built against the temporary map (decided 2026-10-02). It reads nothing from titles, provinces, characters, cultures or faiths, so it survives the map swap.

**Status:** lifted from v1 on 2026-10-02 and converted to a single track trait on 2026-10-03. Static QA passed (gate board, `docs/agent_workflow.md` §6). Art arrived 2026-10-03: 2 trait icons, 4 modifier icons, 3 decision illustrations. **Never played.** It is waiting on the in-game check in spec §9 item 11.

---

## 2. How it works

### 2.1 The player's path
```
 unaugmented ──(offer event accepted)──► AUGMENTED (XP 0)
                                            │  "The Upgrade" event, 100 gold, capital dev ≥ 20
                                            ▼
                                         ENHANCED (XP 50) ──(Partial Removal decision)──► back to Augmented
                                            │  "The Next Stage" event, 200 gold (or a prisoner), capital dev ≥ 35
                                            ▼
                                         OVERCLOCKED (XP 100) ──(Downgrade decision)──► back to Enhanced
                                            │  fracture risk accumulates every year
                                            ▼  risk ≥ 80, or ≥ 60 while stress ≥ 200
                                         NEUROFRACTURED (separate trait, permanent)
```

### 2.2 Two numbers drive everything
| | Tier state | Signature resource |
|---|---|---|
| What | XP on trait `eotg_cybernetics` | character variable `eotg_fracture_risk` |
| Values | exactly **0 / 50 / 100** | 0–100 |
| Visible | yes, an "Integration" bar in the trait tooltip | **no, hidden by design** |
| Who moves it | only `eotg_aug_set_integration_effect` (the 2 upgrade events, the 2 regression decisions) | initiation sets it (0, or 10 for black-market); event options nudge it; the Overclocked yearly pulse adds to it; the cascade resets it; Neurofractured reads it as "episode pressure" |

### 2.3 Stats per tier (totals)
| | Augmented | Enhanced | Overclocked | **Neurofractured** |
|---|---|---|---|---|
| Prowess | +2 | +4 | +8 | **+14** |
| Health | +0.5 | +0.5 | 0 | **−1.0** |
| Stress gain | +10% | +20% | +40% | **+60%** |
| Attraction opinion | −5 | −15 | −30 | **−50** |
| Diplomacy | — | −2 | −5 | **−10** |
| Fertility | — | −20% | −40% | **−80%** |
| Enemy hostile scheme phase | — | +5 | +5 | **+10** |
| Dread gain | — | — | +30% | **+60%** |
| Knight effectiveness | — | — | +10% | **+25%** |
| **Synergy modifier** (on the highest skill) | +1 | +2 | +3 (+10% stress) | **distortion: +5 to the skill, −5 diplomacy, +20% stress** |

The synergy is applied whenever the tier changes. It picks the character's highest skill at that moment and is not re-evaluated afterwards.

### 2.4 Pacing
Everything is driven from `yearly_playable_pulse`, which fires once a year for each count+ character. Five custom on_actions run in order: initiation, tier 1, tier 2, Overclocked, Neurofractured. Each makes at most one weighted roll per pulse, with a "nothing" branch. Cooldown flags are set **only** in the on_action.

| Stage | Roll | Cooldown |
|---|---|---|
| Initiation | a priority chain: one offer at 10–50% depending on the hook | 2–3 years |
| Augmented | weighted, base about 31% a year | 2 years (plus a one-time vassal event outside it) |
| Enhanced | weighted, base about 33% a year | 2–3 years |
| Overclocked | risk accrual, then the threshold check, then a weighted roll of about 52% | 6 months, so in effect every year |
| Neurofractured | weighted, about 59–84% depending on stress and pressure | 1–2 years |

**Fracture risk accrual (Overclocked, per year):** +12 base, +24 if stress ≥ 200, +12 if paranoid, +10 if at war.

---

## 3. Inventory

### 3.1 Events (31)
| File | Events | Hooks |
|---|---|---|
| `eotg_augmentation_initiation.txt` | 5: The Cost of Survival, A Corporate Offer, Aging Hands, Desperation Protocol, A Familiar Change | wounded (+ at war); gold ≥ 500; age ≥ 50 with prowess ≤ 8; an augmented vassal or courtier |
| `eotg_augmentation_tier1.txt` | 6: Phantom Sensation, **The Upgrade** (progression), An Uncomfortable Question (one-time), The Knight's Request, Weight of Silence, The Faster Hand | general; progression gate; has vassals; has knights; at war |
| `eotg_augmentation_tier2.txt` | 6: Emotional Delay, Children Fear Me, **The Next Stage** (progression), The Space Between Us, The Confessor's Warning, Cold Detachment | general; young children; progression gate; married; zealous courtier |
| `eotg_augmentation_tier3.txt` | 7: Violent Impulse, The Mirror, Sleepless, Signal Noise, Clarity, The Delegation, Two Machines | general; at war; vassal opinion < −20; an Overclocked peer |
| `eotg_augmentation_fracture.txt` | 1 + 6: **Neural Cascade** (transformation), Containment Breach, Lucid Moment, The Court Massacre, What the Heir Saw, The Warrant, Dead Reckoning | the cascade; general; stress ≥ 300; primary heir aged 12+; vassal opinion < −30 |

All of them are single-screen events with 2–3 options; the cascade has 1.

### 3.2 Decisions (3)
| Decision | Shown for | Cost / gate | Effect |
|---|---|---|---|
| Partial Removal | Enhanced | 150 gold, stress ≥ 100 | XP → 0 (Augmented), stress relief |
| Overclock Regression | Overclocked | 400 gold, stress ≥ 200 | XP → 50 (Enhanced), 5-year withdrawal modifier |
| Maintenance Protocol | any track tier | 50 gold, 3-year cooldown | Calibrated Systems for 3 years; −8 risk if Overclocked |

### 3.3 Supporting script
| Type | Contents |
|---|---|
| Traits | `eotg_cybernetics` (track: 0/50/100, name and desc switch by XP), `eotg_neurofractured` (hidden in the ruler designer) |
| Static modifiers (26) | 15 tier synergies, 5 Neurofracture distortions, Calibrated Systems, Black Market Implants, Withdrawn from Court, Regression Recovery, Affect Dampened, Running Hot |
| Opinion modifiers (4) | admiration +15, unease −10, fear −25, disgust −20 (all non-decaying) |
| Scripted triggers | `eotg_is_augmented_any`, `eotg_is_aug_tier1/2/3`, `eotg_can_receive_augmented`, `eotg_can_progress_to_enhanced` / `_overclocked`, `eotg_neurofracture_threshold_met`, `eotg_ai_wants_augmentation` |
| Scripted effects | `eotg_aug_initiate_effect`, `eotg_aug_set_integration_effect` (the only path that changes tier), `eotg_aug_refresh_synergy_effect` / `_clear_synergy_effect`, `eotg_add_fracture_risk`, `eotg_trigger_neurofracture`, `eotg_apply_neurofracture_distortion`, `eotg_aug_heal_wounds_effect`, `eotg_clean_all_aug_modifiers` (no caller) |
| Flags | the 4 tier cooldowns, the one-time vassal flag, `eotg_flag_suppress_progression` (set by "resist / delay" options; blocks initiation and progression), the maintenance cooldown |
| Loc | `eotg_augmentation_l_english.yml`, 229 keys |

---

## 4. System goals

### 4.1 Design intent (v1 design doc, `OLD PROJECT VERSION/docs/eotg_cybernetic_augmentation_system.md`)
1. **Power escalates faster than stability.** Each tier gives real advantages, while the social, psychological and stress costs grow out of proportion.
2. **The terminal state has real stakes.** Neurofracture is permanent and irreversible.
3. **It isn't only for the player.** Rulers, knights, generals and courtiers take part. *"AI participation is essential for emergent storytelling."*
4. The tier character arc:
   - Augmented: *socially legible, personally seductive*.
   - Enhanced: *dependency forming, visible alteration*.
   - Overclocked: *unstable, paranoid, near threshold*.
   - Neurofractured: *permanent, feared, catastrophic*.

### 4.2 Your stated goals (this QA round)
5. **More robust than one would expect.** Many events, of different **sizes**, with different **outcomes**, for each **level**.
6. **Neurofractured is a very different extreme,** not a louder Overclocked.
7. **Options cover a wide range of CK3 traits,** so the character's personality shapes the choices on offer.

### 4.3 Rules you decided (spec, 2026-10-03; binding)
8. **Fracture risk stays hidden.** A qualitative hint is deferred and needs its own design call.
9. **XP moves only at tier thresholds** (0/50/100): no drift, no option nudges.
10. Overclocked keeps Enhanced's scheme defence and loses its health bonus.
11. "Static" is augmentation-only vocabulary. The track is labelled "Integration".

### 4.4 Project constraints
12. No title, province, character, culture or faith dependencies until the real map lands.
13. Every flavor event reads or moves `eotg_fracture_risk`, or changes tier (invariant 5).
14. Cooldown authority stays in the on_action. Events are fired only from there, additively.
15. Deferred: Nikios Khanate interaction, the culture/religion reaction table, building gates.

### 4.5 v1's own post-beta roadmap (still unbuilt)
- More initiation hooks (duel shame, a military arms race).
- A full expanded event set.
- A building chain (clinics, neural forge).
- **Augmentation spreading to knights and courtiers.**
- Dynastic events (Cult of Steel, heir fear).
- 3D holding visuals.

---

## 5. Goals against reality

| Goal | Status | Why |
|---|---|---|
| 1. Power outpaces stability | ✔ Met in the numbers | The stat table escalates as intended. The fracture clock makes Overclocked a countdown. |
| 2. Terminal stakes | ◐ Partly | It is permanent, but there is no endgame, no escalation inside Neurofractured, and no decisions. |
| 3. Everyone takes part, AI included | ◐ Partly | The AI is augmented through offers, and knights can be augmented by 2 events. Non-rulers never progress, fracture or get events. |
| 4. The tier arc reads | ◐ Partly | It's present in the loc and modifiers. Event structure and levers are the same at every tier. |
| 5. Robust, varied events | ✘ Not met | 31 single-screen events: no chains, no story cycles, no outcome rolls worth mentioning. |
| 6. Neurofractured is a different extreme | ✘ Not met | Same 3-option shape as Overclocked; nothing takes agency away or reacts across the realm. |
| 7. Wide trait coverage | ✘ Not met | 1 trait-gated option in 31 events; 18 of 36 personality traits never referenced. |
| 8–11. Spec rules | ✔ Implemented | Verified in the files on disk. |
| 12–14. Project constraints | ✔ Met | Map-agnostic, resource-coupled, cooldowns owned by the on_action. |

---

## 6. Status of the earlier QA findings after the conversion

**Fixed by the rework:**
- Timed buffs reusing the permanent synergy keys → `eotg_mod_aug_affect_dampened` / `_running_hot` (audit §1.1).
- Neurofractured free in the ruler designer → `shown_in_ruler_designer = no` (§1.7a). Note: the Augmented-to-Overclocked trait is now **one** trait at `ruler_designer_cost = 20`, and a designed ruler starts at XP 0.
- A Familiar Change counted only Augmented peers → it now counts any track tier (§1.7h).
- Knights got no synergy → they now go through `eotg_aug_initiate_effect`, and only unaugmented knights are picked (part of §1.7i).
- Neurofracture distortion modifiers used positive icons → now negative.

**Still open:** everything else in the logic audit, including:
- the free prisoner upgrade (tier2.003.c);
- the "recovery" options that apply −10 opinion (tier3.006.b, fracture.006.b);
- unimplemented promises (arrest, the Warrant, "mutual");
- unsaved victims who can be family;
- the free wound heal in init.001.b;
- `curious` (5 sites);
- permanent opinions and permanent illegal implants;
- the 6-month Overclocked cooldown;
- the regression stress gates;
- every math finding (stress-200 cliff, accrual against mitigation, no passive Neurofractured pressure).

**Conflict to note:** the content-gaps document (§2 item 5, §5 "Visibility", §6 step 1) recommends making fracture risk visible. That contradicts your decision Q1 (risk stays hidden). Read those items as input for the deferred "qualitative hint" design call, not as a build instruction. The rest of the content-gaps document stands. Its proposed `eotg_aug_install_effect` already exists as `eotg_aug_initiate_effect`.
