> Superseded by `docs/specs/cybernetics_v2.md` and `docs/qa/cybernetics_test_plan.md` (2026-10-03). Kept as history; do not use as a current description.

# Cybernetics (Augmentation) — Logic QA Audit

> **Note (2026-10-03):** this audit predates the conversion to one track trait (`eotg_cybernetics`, spec `docs/specs/cybernetics_track.md`). Findings §1.1, §1.7a, §1.7h and the knight synergy part of §1.7i are fixed. The rest still stand, with trait names now read as tiers of `eotg_cybernetics`. See [cybernetics_system_overview.md](cybernetics_system_overview.md) §6.

**Date:** 2026-10-02 · **Scope:** logic, math, call correctness, option/trait coverage, robustness against the "more than one would expect" goal. Not in scope: loc prose, icons (deferred), lore.

**Files reviewed (all read in full):**
`common/on_action/eotg_augmentation_on_actions.txt`, `common/scripted_effects/eotg_augmentation_effects.txt`, `common/scripted_triggers/eotg_augmentation_triggers.txt`, `common/traits/eotg_augmentation_traits.txt`, `common/modifiers/eotg_augmentation_modifiers.txt`, `common/opinion_modifiers/eotg_augmentation_opinions.txt`, `common/decisions/eotg_augmentation_decisions.txt`, `events/eotg_augmentation_{initiation,tier1,tier2,tier3,fracture}.txt`.

**How it was checked:** every effect and trigger compared against vanilla CK3 game files (the install is now **1.20.0.3**), plus a Tiger run. Tiger needs a descriptor, and the repo has no `echoes_of_the_grip.mod` (the command in CLAUDE.md fails with "Could not read .mod file"), so I ran it with a temporary descriptor in the scratchpad.

---

## 0. Summary

| Area | Verdict |
|---|---|
| Parses / loads | **Clean.** In the cybernetics files Tiger reports only (a) `has_personal_tenet_flag` / `change_spiritual_fulfillment`, which are 1.20 tokens inside vanilla's `increase_wounds_effect` that Tiger 1.17 doesn't know (benign), and (b) the four missing trait icons (deferred). |
| Call correctness | Mostly right. `has_trait = wounded` (group), `highest_skill`, `increase_wounds_effect` + its REASONs, `death_murder`, `death_suicide`, `remove_short_term_gold`, `add_tyranny`, `depressed_1`, the themes, `yearly_playable_pulse`, and `modifier` inside `random`/`random_list` are all valid vanilla usage. **Six logic bugs** where the call does something different from what the option claims (§1). |
| Math | The fracture clock works, but it has **a cliff at stress 200**, **mitigation can never keep pace with accrual**, **risk moves before Overclocked are mostly lost to the 0 floor**, and **Neurofractured "episode pressure" has no passive input**, so its ≥60 band is rarely reached (§2). |
| Trait coverage | **Thin.** In 31 events there is **1** option gated on a personality trait. **18 of 36** vanilla personality traits are never referenced. `stress_impact` reads only 7 traits. 14 violent options carry no stress response at all (§3). |
| Robustness goal | **Not met yet.** 31 events, all single-screen, all 2–3 options, no chains, no story cycles, no realm-scale arcs. Neurofractured is the same shape as Overclocked with bigger numbers, not "a very different extreme" (§4–5). |

---

## 1. Logic bugs (the call does not do what the option says)

Ranked by severity.

### 1.1 Temporary event buffs reuse the permanent synergy modifier IDs — HIGH
The "education synergy" modifiers are permanent (added with no duration by `eotg_apply_edu_synergy_*`). Four event options add **the same modifier IDs** with a duration:

| Site | Adds |
|---|---|
| [tier2.txt:38](../../events/eotg_augmentation_tier2.txt#L38) (2.001.a) | `eotg_mod_enh_intrigue_bonus`, 3 years |
| [tier2.txt:369](../../events/eotg_augmentation_tier2.txt#L369) (2.006.a) | `eotg_mod_enh_intrigue_bonus`, 2 years |
| [tier3.txt:176](../../events/eotg_augmentation_tier3.txt#L176) (3.003.b) | `eotg_mod_oc_martial_bonus`, 2 years |
| [tier3.txt:285](../../events/eotg_augmentation_tier3.txt#L285) (3.005.a) | `eotg_mod_oc_martial_bonus`, 1 year |

For an intrigue-highest Enhanced ruler or a martial-highest Overclocked one, the event re-adds the modifier they already hold. Whether the engine refreshes it to timed or stacks a second copy, the result is wrong: either the permanent synergy expires after 1–3 years, or the next `remove_character_modifier` in a tier change strips both copies. For everyone else it works, but the buff is labelled as the "education synergy", which is confusing.
**Fix:** add separate modifiers, e.g. `eotg_mod_enh_detachment_focus` and `eotg_mod_oc_sleepless_drive`, and add them to `eotg_clean_all_aug_modifiers`.

### 1.2 "Test it on prisoners" skips the 200-gold upgrade cost — HIGH
[tier2.txt:171-189](../../events/eotg_augmentation_tier2.txt#L171-L189). Option c performs the full Enhanced → Overclocked upgrade with **no gold cost**. Its only costs are +15 dread (a benefit to many players) and +5 risk. Any ruler with a prisoner has a strictly cheaper path to the strongest tier than option a's 200 gold.
**Fix:** charge at least part of the cost (e.g. `remove_short_term_gold = 100`), or make the result probabilistic (a `random_list` where failure kills the prisoner and nothing upgrades).

### 1.3 "Opinion recovery" options make opinion worse — HIGH
- [tier3.txt:362-379](../../events/eotg_augmentation_tier3.txt#L362-L379) (3.006.b, "Hear them out. Set conditions." — the header comment says *opinion recovery*)
- [fracture.txt:374-390](../../events/eotg_augmentation_fracture.txt#L374-L390) (fracture.006.b, "Offer concessions" — the comment says *opinion improves*)

Both apply `eotg_opinion_aug_unease`, which is **−10**, to vassals who are already below −20 / −30. They pay 100–200 prestige to lower opinion further.
**Fix:** add a positive modifier (e.g. new `eotg_opinion_aug_reassured`, +15, 5 years), and remove fear/unease from those vassals with `remove_opinion`.

### 1.4 Options whose text promises effects that are not implemented — MEDIUM
| Event | Promise | What actually happens |
|---|---|---|
| [tier3.006.a](../../events/eotg_augmentation_tier3.txt#L343) "Have them arrested." | Arrest | Dread, tyranny and an opinion change. **No imprisonment.** |
| [fracture.006](../../events/eotg_augmentation_fracture.txt#L338) "The Warrant — a vassal files a formal rebellion" | Rebellion | **No faction, war, or claimant.** All three options are resource swaps. |
| [tier3.007.a](../../events/eotg_augmentation_tier3.txt#L443) "mutual positive opinion" | Two-way opinion | One-way only (the other machine → root). |

**Fix:** `imprison` the worst-opinion vassal from a saved scope, with `imprison_character_effect` or a vanilla arrest attempt. For The Warrant, have the vassal start or join a vanilla faction, or open a war through a vanilla CB, so it doesn't depend on mod titles. For 3.007.a, add root → other_machine as well.

### 1.5 Random violence has no saved victim and can hit the ruler's own family — MEDIUM
`random_courtier` picks the victim with no limit except `is_alive` at [tier3.txt:53, 70](../../events/eotg_augmentation_tier3.txt#L53), [fracture.txt:43, 77, 85, 210, 214](../../events/eotg_augmentation_fracture.txt#L77). Courtiers include the ruler's **spouse, children and heir**. None of these sites calls `save_scope_as`, so the loc **cannot name who was killed or wounded**: the player loses an heir to an unnamed "random court casualty".
[fracture.002.c](../../events/eotg_augmentation_fracture.txt#L117-L131) "Execute the survivors" kills **every** courtier with any `wounded` rank, including people wounded by unrelated events years earlier, and family.
**Fix:** save every victim (`save_scope_as = eotg_victim`), name them in the desc, and decide deliberately whether family is eligible. For the "survivors" option, flag the people wounded *in this event* (`add_character_flag = { flag = eotg_flag_breach_victim days = 30 }`) and filter on that flag. Weighting victims with `weight = { modifier = { ... } }` keeps family possible but rare, which suits Neurofractured.

### 1.6 `curious` is a childhood trait — five AI weights are dead — LOW
`curious` is `category = childhood`, `maximum_age = 15` in vanilla. Adult rulers never have it, so these modifiers never apply: [init.txt:361](../../events/eotg_augmentation_initiation.txt#L361), [tier1.txt:69](../../events/eotg_augmentation_tier1.txt#L69), [tier1.txt:399](../../events/eotg_augmentation_tier1.txt#L399), [tier2.txt:396](../../events/eotg_augmentation_tier2.txt#L396), [tier3.txt:314](../../events/eotg_augmentation_tier3.txt#L314).
**Fix:** replace with adult equivalents: `education_learning_3/4`, `lifestyle_physician`, `erudite`, `intellect_good_*`, or `eccentric`.

### 1.7 Smaller logic issues
| # | Issue | Where | Fix |
|---|---|---|---|
| a | **Ruler designer:** Enhanced, Overclocked and Neurofractured have `ruler_designer_cost = 0` and no `shown_in_ruler_designer = no`, so a designed ruler may take Neurofractured (+14 prowess) **for free**, with no distortion modifier. Confirm in game. | [traits.txt:42, 62, 84](../../common/traits/eotg_augmentation_traits.txt#L42) | `shown_in_ruler_designer = no` on tiers 2–4 (vanilla pattern, e.g. `depressed_1`). |
| b | **Opinions never expire.** All four opinion modifiers are `decaying = no` and no `add_opinion` call passes `years`, so they are permanent. 3.006.c applies −25 fear to **every vassal, forever**. | [opinions.txt](../../common/opinion_modifiers/eotg_augmentation_opinions.txt) | Pass `years = 5`–`10`, or switch to `decaying = yes` with `monthly_change`. |
| c | **Illegal implants never go away.** The modifier is added with no duration and nothing removes it (maintenance doesn't). That is −0.5 health and −2 diplomacy for life. | [init.txt:235](../../events/eotg_augmentation_initiation.txt#L235) | Make maintenance (or a new "Legitimise the Implants" decision) remove it. |
| d | **`eotg_clean_all_aug_modifiers` is never called.** It's dead code, since no full-removal path exists. | [effects.txt:148](../../common/scripted_effects/eotg_augmentation_effects.txt#L148) | Use it in an Excision decision (§5), or delete it. |
| e | **The Overclocked cooldown does nothing.** It is `months = 6` on a yearly pulse, so it has always expired by the next pulse and Overclocked effectively rolls every year. Tiers 1/2 use 2 years. | [on_actions.txt:268-311](../../common/on_action/eotg_augmentation_on_actions.txt#L268) | Say what you mean: delete it (annual), or use `years = 2`. |
| f | **Neurofractured 12-month flags race the 12-month pulse.** Whether next year's pulse sees the flag depends on expiry timing on the same day. This also affects the guard in `eotg_trigger_neurofracture`. | [on_actions.txt:346-397](../../common/on_action/eotg_augmentation_on_actions.txt#L346), [effects.txt:194](../../common/scripted_effects/eotg_augmentation_effects.txt#L194) | Use `months = 11` (every pulse) or `months = 23` (every other pulse). |
| g | **Adding `callous` to an heir who may be `compassionate`** (opposites). No guard. | [fracture.txt:323-326](../../events/eotg_augmentation_fracture.txt#L323) | `limit = { NOT = { has_trait = compassionate } }`. |
| h | **init.005 only sees the `eotg_augmented` tier.** An Enhanced or Overclocked peer doesn't count, in either the on_action or the event trigger. | [on_actions.txt:104](../../common/on_action/eotg_augmentation_on_actions.txt#L104), [init.txt:293](../../events/eotg_augmentation_initiation.txt#L293) | Use `eotg_is_augmented_any = yes`. |
| i | **Knights augmented by init.002.c or tier1.004.a** get no synergy modifier, no risk variable, and **never progress or get events.** Only `yearly_playable_pulse` characters (count+) do. Courtiers are frozen at Augmented forever, which also makes tier3.007 (overclocked courtier) nearly unreachable. | init.002.c, tier1.004.a | Fine if intentional, but write it down. Otherwise add a `random_yearly_everyone_pulse`-style hook filtered to `eotg_is_augmented_any`. |

---

## 2. Math

### 2.1 Event frequency per pulse (off cooldown)
| Tier | Always-eligible weight | Max weight | "Nothing" | P(event), base | P(event), all conditions met | Cooldown |
|---|---|---|---|---|---|---|
| Augmented | 45 | 130 | 100 | **31%** | **57%** | 2 y |
| Enhanced | 50 | 135 | 100 | **33%** | **57%** | 2–3 y |
| Overclocked | 110 | 210 | 100 | **52%** | **68%** | none in effect (1.7e) |
| Neurofractured (pressure 0) | 73 | 198 | 50 | **59%** | **80%** | ~1 y (racy) |
| Neurofractured (pressure ≥60) | 61.5 | 266.5 | 50 | 55% | **84%** | |

With the 2-year cooldown, an Augmented ruler sees about one event every 3–4 years. The progression event ("The Upgrade") is ~15% of a roll even when eligible, so the expected time to *be offered* Enhanced is roughly 6–10 years. Escalation is fine, but at the low tiers the player will see the same six events many times.

### 2.2 Fracture clock (`eotg_fracture_risk`, Overclocked only)
Accrual per pulse: base 12, stress ≥ 200 +24, paranoid +12, at war +10. Threshold is 80, **or 60 if stress ≥ 200**. Clamped to 0–100.

Pulses until the cascade, with no event choices and starting risk R₀ = 0:

| Situation | Per year | Threshold | Cascade at pulse |
|---|---|---|---|
| Calm, peace | 12 | 80 | **7** |
| Calm + maintenance every 3 y | ≈ 9.3 | 80 | ~9 |
| Paranoid | 24 | 80 | 4 |
| At war | 22 | 80 | 4 |
| **Stress ≥ 200** | 36 | 60 | **2** |
| Stress + paranoid + war | 58 | 60 | 2 (1 if R₀ ≥ 2) |

**Findings:**
1. **The stress-200 cliff is double-counted.** Crossing 200 both triples accrual and lowers the threshold, so time-to-cascade drops from 7 years to 2 in a single stress point. Overclocked adds +40% stress gain on the trait, and +10% more from the OC synergy modifier, so most Overclocked rulers cross 200 quickly. In practice, Overclocked lasts about 2–4 years for most players. If that's the intent, fine; if 5–8 years is meant, pick one lever: either the +24, or the lower threshold.
2. **Mitigation can't keep pace.** The most you can claw back per year is roughly 2.7 from maintenance (−8 per 3 y) plus the occasional −3 to −10 event option, about **3–5/yr against an accrual of at least 12**. The cascade is inevitable unless you regress. That's a legitimate design ("Overclocked is a countdown"), but then the −3 / −5 options are cosmetic and the tooltips should say "slows", not "reduces".
3. **Risk moves before Overclocked are mostly lost.** Initiation sets risk to 0 (10 for black-market). Tier 1/2 "−3 / −5 risk" options are clamped at 0 and do nothing unless the player previously took a "+" option. Realistic Overclocked entry risk is 0–25, worth about 0–2 pulses.
4. **Maintenance at risk 0 is wasted** for the same reason: the −8 is clamped away.
5. **The regression decision keeps the risk.** Dropping from Overclocked at risk 70 to Enhanced and coming back puts the ruler at 82+ within one pulse. Either reset or halve risk on regression, or say in the tooltip that the damage stays.
6. **The regression gate is inverted.** `eotg_decision_overclock_regression` requires **stress ≥ 200** ([decisions.txt:67](../../common/decisions/eotg_augmentation_decisions.txt#L67)), and partial removal requires ≥ 100 ([decisions.txt:21](../../common/decisions/eotg_augmentation_decisions.txt#L21)). A calm, prudent ruler who wants out early *cannot* leave. By the time they're allowed to, they're on the 2-year clock. Suggest dropping the stress gate and scaling cost instead (cheaper when stressed or at high risk).

### 2.3 Neurofractured "episode pressure"
The cascade resets risk to 0, and after that **nothing raises it passively**. Only option choices move it (+20 at most, −10 at least). A player who picks the moderate options sits at 0–20 permanently, so the ≥30 and ≥60 weightings in the on_action ([on_actions.txt:336-398](../../common/on_action/eotg_augmentation_on_actions.txt#L336)) rarely fire. **Fix:** add passive drift (e.g. +8/yr, +15 if stress ≥ 300), and let the "calm" options push it back down. Then the bands become a real state the player manages.

### 2.4 Skill and modifier math
- **The diplomacy synergy branch is nearly unreachable at higher tiers.** Each synergy effect runs right after `add_trait`, and the trait applies diplomacy −2 / −5 / −10. If trait modifiers count toward `highest_skill` in the same effect (verify in game), a diplomat must lead their next skill by >2 / >5 / >10 to keep the diplomacy bonus. At Neurofractured that is practically never.
- **The synergy is a snapshot.** It's computed once at tier change and never re-evaluated as skills drift. Either rename it ("Imprint", fixed at install) or refresh it in the yearly on_action.
- **Permanent skill gains in flavor events are farmable.** tier1.001.c (+1 learning, repeatable every ~3 y), tier1.006.a/c, tier2.006.c, tier3.002.c (+3 prowess), tier3.005.c, tier3.007.b/c, init.002.b (+1 intrigue *for declining*), init.005.c. Over a 20-year augmented life, that's about **+4–8 permanent skill** from small events. Vanilla reserves permanent skill for milestones; use timed modifiers instead.
- **All gold costs are flat** (25 / 50 / 75 / 100 / 150 / 200 / 400). That's trivial for an emperor and prohibitive for a count. Vanilla scales with script values (e.g. `medium_gold_value`).

### 2.5 Dominated options (one choice is better on every axis)
| Event | Dominant | Why |
|---|---|---|
| init.001 | **b** "Find another way" | **Fully heals the wound for free** ([init.txt:60-73](../../events/eotg_augmentation_initiation.txt#L60)), the same medical benefit as accepting, with no implant. Make b a chance to heal or a rank reduction. |
| tier1.005 | c | +75 prestige, no cost; a and b both *lose* 25 prestige. |
| tier1.006 | c over b | Same +50 prestige; c adds +1 learning, b adds stress. |
| tier2.004 | a over b | Same −10 opinion; a also gives stress relief and −3 risk. |
| tier2.005 | b | +100 piety, stress relief, −5 risk, no cost. |
| fracture.003 | c | **−100 stress** for +10 pressure and some dread. This is the best stress tool in the mod. |
| fracture.007 | c | −100 stress for only −50 prestige. |

---

## 3. Option and trait coverage

### 3.1 Options per event
Every event has 2–3 options; Neurofractured's cascade (0001) has 1. Only **1 option in 31 events** is gated on a personality trait (init.001.c, zealous/content/humble). The rest are gated on gold, prisoners or courtiers, or not at all. Traits appear only in `ai_chance`, which the player never sees.

Vanilla's typical shape is 3 universal options plus 1–2 trait-gated ones (`trigger = { has_trait = X }` with `trait = X` to show the icon), and `stress_impact` lists covering 3–6 traits per option.

### 3.2 Vanilla personality traits (36) — referenced anywhere in the system
**Used (18):** content (30 refs), callous (27), ambitious (22), zealous (19), compassionate (16), brave (15), humble (11), patient (9), arrogant (7), paranoid (6), wrathful (4), gregarious (3), vengeful (2), honest (2), greedy (2), generous (1), diligent (1), arbitrary (1).

**Never used (18):** **craven**, **cynical**, **sadistic**, **just**, **deceitful**, calm, impatient, shy, trusting, forgiving, stubborn, fickle, eccentric, lazy, temperate, gluttonous, chaste, lustful.

The gaps in bold are the obvious ones. **Craven** is the counterpart of brave, which appears 15 times; a coward facing body modification is a core reaction. **Cynical** is the counterpart of zealous (19 refs) and the natural augmentation enthusiast. **Sadistic** belongs on every violence option. **Just** should react to murdering courtiers. **Deceitful** fits the spouse "I am the same person" lie.

**Only 7 traits in `stress_impact`:** zealous, ambitious, humble, content, compassionate, honest, brave.

### 3.3 Violent or cruel options with **no** `stress_impact`
A compassionate, just or forgiving ruler feels nothing on any of these:
tier1.004.c · tier2.003.c (torture prisoner) · tier3.001.b (wound courtier) · **tier3.001.c (murder courtier)** · tier3.004.c · tier3.006.a · tier3.006.c · fracture.002.a · **fracture.002.c (mass execution)** · fracture.004.a · fracture.005.a · fracture.005.c · fracture.006.a · fracture.006.c.

Suggested baseline for murder and execution: `compassionate = major_stress_impact_gain`, `just = medium_stress_impact_gain`, `forgiving = medium_stress_impact_gain`, `sadistic = medium_stress_impact_loss`, `wrathful = minor_stress_impact_loss`.

### 3.4 Non-personality traits that should matter and don't
| Group | Traits (verified in vanilla) | Use |
|---|---|---|
| **Physical loss** — the obvious entry hook | `maimed`, `one_eyed`, `one_legged`, `blind`, `disfigured`, `infirm`, `incapable` | Today only `wounded` opens initiation. A prosthetic that **removes `one_legged` / `blind` / `maimed`** is the strongest pitch the system can make, and it doesn't exist. |
| Lifestyle / education | `lifestyle_physician`, `education_learning_3/4`, `erudite`, `lifestyle_blademaster`, `education_martial_4`, `theologian`, `lifestyle_mystic` | A physician calibrates their own implants (cheaper maintenance, unique option). A blademaster gets extra from the prowess options. A theologian or mystic offers faith-framed resistance. |
| Congenital | `intellect_good_*`, `shrewd`, `physique_good_*`, `strong` | Change the rejection or fracture odds. A genius copes better and a strong body accepts more. |
| Mental health | `depressed_1`, `depressed_genetic`, `lunatic_1`, `lunatic_genetic`, `possessed_1` | Neurofractured interplay: a lunatic who fractures should play very differently. Today only `depressed_1` is granted, at 30% in fracture.004.b. |

---

## 4. Robustness against the stated goal

> "many different events, of different sizes, with different outcomes, for different levels, and then a very different extreme for events when Neurofractured"

| Requirement | Today | Gap |
|---|---|---|
| Many events | 5 initiation / 6 / 6 / 7 / 6 + cascade = **31** | About 3 years of content per tier at observed frequencies; repeats begin quickly. |
| Different **sizes** | **All single-screen.** No follow-ups, no `trigger_event` chains, no story cycles, no activities, no realm events beyond opinion sweeps. | No medium or large tier exists. |
| Different **outcomes** | Outcomes are fixed. Only 4 options in the whole system have a random result (tier3.004.a, fracture.003.a, fracture.004.b, fracture.005.c). | No `random_list` success/failure, no outcomes that depend on skill or trait, no delayed consequences. |
| Different **levels** | Each tier has its own pool ✔ | Same structure, numbers and resource levers at every tier: prestige, dread, piety, a small risk move. |
| **Neurofractured as an extreme** | Same 3-option shape as Overclocked, with larger dread and more corpses | Nothing takes agency away, nothing escalates over time, no endgame, no decisions, no realm or succession consequences. |

---

## 5. Recommended expansion (for the architect to spec)

### 5.1 Target content matrix
| Tier | Small (1 screen, local nudge) | Medium (2–3 stage chain, named character, delayed follow-up) | Large (multi-year story cycle / realm-wide / war / faction) | Total |
|---|---|---|---|---|
| Initiation | 6 (one per entry hook: wound, **lost limb/eye**, age, wealth, peer, faith-cynic) | 2 (black-market surgery with complication follow-up; syndicate contract with strings) | 1 (a corporate patron who later calls in the debt) | 9 |
| Augmented | 8 | 3 | 1 | 12 |
| Enhanced | 8 | 3 | 1 | 12 |
| Overclocked | 8 | 4 | 2 | 14 |
| Neurofractured | 6 per pressure band × 3 bands | 4 | 3 (regency, warrant war, endgame) | ~25 |

Option standard: **3 universal options + 1–2 trait-gated** (with `trait = X` for the icon), a `stress_impact` covering 4+ traits on every morally loaded option, and at least one option per event that **reads or moves `eotg_fracture_risk`** (invariant 5).

### 5.2 Trait pairs to spread across the pool
brave/craven (fear of surgery) · zealous/cynical (faith vs. progress) · calm/wrathful (violent impulse) · patient/impatient (waiting for calibration) · honest/deceitful (hiding it) · gregarious/shy (court reaction) · trusting/paranoid (signal noise) · compassionate/callous/sadistic (violence) · just/arbitrary (punishment) · forgiving/vengeful (aftermath) · fickle/stubborn (regression decisions) · eccentric (embraces the strange) · diligent/lazy (maintenance) · greedy/generous (cost) · temperate/gluttonous and chaste/lustful (the body and its appetites, the spouse).

### 5.3 Making Neurofractured a *different kind* of play
1. **Loss of agency.** Some events have one forced option, or an option whose text differs from its result: "The implant decides" rolls a hidden `random_list`. The player stops being sure their choice is honoured.
2. **Unreliable perception.** The implant reports a plot that doesn't exist. Act on it (imprison or execute a saved "conspirator"), and a follow-up months later reveals they were innocent, with opinion and tyranny fallout. This plays off tier3.004 "Signal Noise", which already sets it up.
3. **Pressure bands as states,** with passive drift (§2.3). For example:
   - 0–29 *Flicker*: odd, small, eerie events.
   - 30–59 *Fracture*: violence and lost time.
   - 60+ *Cascade storm*: the realm reacts, with regency attempts and the warrant war.

   Each band gets its own pool.
4. **The realm responds.** fracture.006 should actually start a faction or war. Add a **Containment Regency** in which spouse or heir takes the council, via a vanilla regency mechanism if one fits, or a story cycle. Add an heir arc that runs across several events instead of the repeating one-off fracture.005.
5. **Personality scrambling.** A cascade episode swaps one personality trait for its opposite, or removes a relation (friend or lover forgotten). Uses only vanilla traits, so it survives the map swap.
6. **Endgames** (Neurofractured has none today):
   - *Excision* (surgery: high death chance; survivor loses all tiers and gains `maimed`; uses `eotg_clean_all_aug_modifiers`).
   - *Total Integration* (personality traits wiped, enormous stats, the court abandons you).
   - *Death by cascade*.
   - *Abdication into restraints*.
7. **Neurofractured decisions** (it has zero today): *Restraints* (less violence, prestige loss), *Sedation Regimen* (gold per year, pressure −, skills −), *Name a Keeper* (appoint a guardian or regent), *Embrace the Cascade*, *Excision*.

### 5.4 Decisions — current vs. needed
| Exists | Missing |
|---|---|
| Partial removal (Enhanced → Augmented) | Removal from Augmented (back to unaugmented) |
| Overclock regression | Neurofractured: Restraints / Sedation / Keeper / Excision / Embrace (above) |
| Maintenance (Augmented–Overclocked) | Legitimise illegal implants (1.7c) · Seek a physician (cheaper with `lifestyle_physician` at court) · Augment a courtier or knight on demand · AI-facing seek-augmentation decision (today the AI only joins via random offers) |

---

## 6. Verified correct (no action)
- The on_action is wired additively into `yearly_playable_pulse` (`on_actions = { }`). Cooldown authority sits only in the on_action, as the invariant requires.
- `eotg_trigger_neurofracture` sets the Neurofractured cooldown before the Neurofractured check runs in the same pulse, so the cascade and a fracture event can't land in the same pulse (subject to 1.7f).
- On a cascade pulse, the threshold check correctly replaces that year's flavor roll (`if` / `else_if`).
- Tier changes remove the previous tier's synergy modifiers. I traced all six paths: the 3 progressions, 2 regression decisions and the cascade. No permanent modifier is orphaned (except the collisions in 1.1).
- `eotg_aug_heal_wounds_effect` correctly handles the `wounded` trait group, rank by rank.
- `eotg_add_fracture_risk` initialises the variable when it's missing, so knights and ruler-designer characters can't error on it.
- `random_list` entries correctly use `trigger` and `modifier`. `random = { chance modifier }` in fracture.003.a is valid.
- All four traits list each other as opposites, so no character can hold two tiers.
- Identifiers carry the `eotg_` prefix throughout. No title, faith, culture or province dependencies, so the system meets the temporary-map rule.
- `eotg_ai_wants_augmentation` is used (init.002.a ai_chance). It is the only use; consider using it in the other initiation offers too.

---

## 7. Fix order
1. §1.1 modifier collisions, §1.2 free upgrade, §1.3 inverted "recovery" options, init.001.b free heal (small, mechanical: scripter).
2. §1.7a ruler designer, §1.7b opinion durations, §1.7c illegal implants, §1.6 `curious` (small: scripter).
3. §3.3 add `stress_impact` to the 14 violent options; add craven / cynical / sadistic / just / deceitful options to existing events (scripter + localizer).
4. §2.2 / §2.3 rebalance the fracture clock and add Neurofractured drift. Decide the cliff and the regression gate first (architect decision, then scripter).
5. §1.4 / §1.5 make the promised effects real and save victim scopes (scripter + localizer).
6. §5 expansion: needs an architect spec (`docs/specs/cybernetics_v2.md`) before any building.

Separately: CLAUDE.md's Tiger command points at `echoes_of_the_grip.mod`, which isn't in the repo, so it fails as written. Also, the game is now 1.20 and Tiger 1.17 warns that it targets 1.18.3.
