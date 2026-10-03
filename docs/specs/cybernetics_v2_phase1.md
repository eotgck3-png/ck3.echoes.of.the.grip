# Cybernetics v2 — Phase 1: trait-reactivity pass on the existing 31 events

Index: [cybernetics_v2.md](cybernetics_v2.md). Rules in index §1 apply. Needs Phase 0 (stress helpers, victim picker, lesson modifiers, gold values).

**Purpose & gate.** Gate 3. Not blocked. This is the cheapest large gain in feel (content-gaps §6 step 2). It does five things to the existing events:
- adds trait-gated options;
- puts `stress_impact` on all 14 violent options (audit §3.3);
- fixes dominated options (audit §2.5);
- moves every random victim onto the saved, weighted picker (audit §1.5);
- converts flat gold and permanent-skill rewards (B5, B6).

No new event ids. Firing and cooldowns are unchanged.

**Signature resource.** Every event already couples. New options add or read `eotg_fracture_risk` where shown (**Risk** column). Below Overclocked, only + moves are added (index §1 rule 4).

**How to read the tables.**
- Events and options are referenced by **id and option letter**. Line numbers are deliberately absent: the scripter's in-flight fixes are moving them.
- New options take the next free letters (d, e…) and sit after the universal options.
- Each `[trait]` option = `trigger = { has_trait = trait }` + `trait = trait`, plus an `ai_chance` with base 30 and +30 for its own trait.
- "helper X" = `eotg_aug_stress_X_effect` (Phase 0 §2.4).
- "lesson X" = `add_character_modifier = { modifier = eotg_mod_aug_lesson_X  years = 5 }`.
- Where an option keeps its existing stress block, the helper is **added**. Where a trait appears in both, the helper replaces the bespoke line for that trait.

---

## 1. Initiation (`events/eotg_augmentation_initiation.txt`)

| Event | Change to existing options | New options | Risk |
|---|---|---|---|
| **init.001** The Cost of Survival | a: + helper surgery. b: already fixed in flight (`eotg_aug_ease_wound_effect`, 50%); no change. c: unchanged. | **d [craven]** "Anything, so I never feel that again." Same as a, but sets risk to 5 instead of 0 (fear-driven over-install). Stress: craven minor loss. **e [cynical]** "Flesh was only ever a first draft." Same as a, +50 prestige, −50 piety. | a/d/e set initial risk |
| **init.002** A Corporate Offer | a: now **costs** `remove_short_term_gold = medium_gold_value` (it was free: the syndicate sells, it doesn't give) + helper surgery. b: "+1 intrigue" → lesson intrigue (B6). c: knight path unchanged. | **d [greedy]** "Haggle them down." Pay `minor_gold_value`, then install as a, + `add_character_flag = eotg_flag_aug_hidden_flaw` (cheap hardware: Thread T6), risk set to 5. | a/d set risk; d adds the flaw flag |
| **init.003** Aging Hands | a: + helper surgery. | **d [arrogant]** "I will not grow old in front of them." As a, +100 prestige, risk set to 5. **e [humble]** "Let age have me." As b, +50 piety, stress: humble minor loss. | a/d set risk |
| **init.004** Desperation Protocol | a: + helper surgery. b: + helper reject. | **d [brave]** "I will finish this war as I am." As b, +75 prestige. Stress: brave minor loss. **e [craven]** "Do all of it. Now." As a, risk set to 15 instead of 10, + lesson prowess. Stress: craven medium loss. | a/e set risk |
| **init.005** A Familiar Change | a: + helper surgery. c: "+1 learning" → lesson learning (B6). | **d [cynical]** "Ask them what it cost." As a, pay `minor_gold_value`, peer gets `eotg_opinion_aug_admiration`. **e [paranoid]** "What did they put inside you?" Peer gets `eotg_opinion_aug_unease`, + lesson intrigue, + `eotg_flag_suppress_progression` 2 years. | a/d set risk |

## 2. Augmented (`events/eotg_augmentation_tier1.txt`)

| Event | Change to existing options | New options | Risk |
|---|---|---|---|
| **tier1.001** Phantom Sensation | a: + helper neglect. b: cost `tiny_gold_value` (B5). c: "+1 learning" → lesson learning (B6). | **d [diligent]** "Log it. Test it. Fix it." `eotg_mod_implant_calibrated` **1 year** (b gives 2), no gold. Stress: diligent minor loss. **e [lazy]** "It'll pass." Stress: lazy minor loss, + helper neglect. Risk +3. | c +2, e +3 |
| **tier1.002** The Upgrade | a: cost `medium_gold_value` (B5). Trait options are added when Phase 4a turns this into the 3-stage First Upgrade; nothing else here. | — | tier change |
| **tier1.003** An Uncomfortable Question | b: + helper cruelty. c: + helper cruelty. | **d [honest]** "The truth: I don't know what I'm becoming." Vassal gets `eotg_opinion_aug_reassured` (exists). Stress: honest minor loss. Risk +2 (saying it aloud makes it real). **e [deceitful]** "There is nothing to tell." Vassal gets `eotg_opinion_aug_unease`, + lesson intrigue, + helper lie. | c +3, d +2 |
| **tier1.004** The Knight's Request | c: + helper cruelty (audit §3.3). | **d [generous]** "Granted, at my expense." Pay `minor_gold_value`; the knight gets `eotg_aug_initiate_effect` **and** `eotg_opinion_aug_grateful_patient` (Phase 2 key; until Phase 2 ships, use `eotg_opinion_aug_admiration`). **e [paranoid]** "Who told you to ask me this?" Knight gets `eotg_opinion_aug_fear`; root gets lesson intrigue. Stress: paranoid minor loss. | a/d tier change (knight); add `eotg_add_fracture_risk = { AMOUNT = 0 }` on the knight in a/d so the variable exists from install |
| **tier1.005** Weight of Silence | **Dominated fix (audit §2.5):** c becomes +50 prestige (was 75) **and** risk +5 (holding the processing pause in check strains it). | **d [shy]** "Leave the hall." −50 prestige, stress: shy medium loss. Risk +2. **e [gregarious]** "Make it theatre." +100 prestige, +5 dread, risk +5. Stress: gregarious minor loss. | a +3, c +5, d +2, e +5 |
| **tier1.006** The Faster Hand | a: "+1 prowess" → lesson prowess (B6). **Dominated fix:** b gets +50 piety and helper reject; c: "+1 learning" → lesson learning, plus risk +2. | **d [brave]** "Again." Lesson prowess, +150 prestige, 20% `increase_wounds_effect = { REASON = fight }`, risk +6. **e [lifestyle_blademaster]** "That was my blade, not the machine's." Lesson prowess, +75 prestige. Stress: blademaster-holder minor loss. Risk −0; the event couples through a/c/d. | a +3, c +2, d +6 |

## 3. Enhanced (`events/eotg_augmentation_tier2.txt`)

| Event | Change to existing options | New options | Risk |
|---|---|---|---|
| **tier2.001** Emotional Delay | b: + helper reject. c: cost `minor_gold_value`. | **d [compassionate]** "Then I will sit with them until I feel it." Spouse and children (alive, at court) get `eotg_opinion_aug_reassured`. Stress: compassionate minor loss, base minor gain. **e [callous]** "Good." `eotg_mod_aug_affect_dampened` 5 years, risk +4. Stress: callous minor loss. | c +8, e +4 |
| **tier2.002** Children Fear Me | a: + helper cruelty. | **c (universal)** "Show them how it works." Children aged ≥6 get `eotg_opinion_aug_reassured`; root gets lesson learning. Risk +2. **d [compassionate]** "Hold them anyway." Children get `eotg_opinion_aug_reassured`. Stress: compassionate medium loss. **e [sadistic]** "Fear is the first lesson." +20 dread, children get `eotg_opinion_aug_fear`, helper cruelty. Risk +5. | a +3, c +2, e +5 |
| **tier2.003** The Next Stage | a: cost `major_gold_value`, + helper surgery. c: in-flight fix (cost) + helper wound (audit §3.3, torturing a prisoner). | **d [ambitious]** "Whatever it costs." As a, plus helper embrace; risk +5. **e [content]** "This is enough. I am enough." As b, + `eotg_flag_suppress_progression` 5 years. Stress: content medium loss. | tier change; c +5, d +5 |
| **tier2.004** The Space Between Us | **Dominated fix:** b ("I am the same person") becomes a gamble with helper lie: 50% spouse `eotg_opinion_aug_reassured`, 50% `eotg_opinion_aug_disgust`. | **d [deceitful]** "Perform the old warmth." Spouse gets `eotg_opinion_aug_reassured`, helper lie (deceitful loses nothing), risk +3 (performing emotion is work for the implant). (Phase 4b chains stages 2–3 off a/b/c/d.) | a −3 (kept), c +5, d +3 |
| **tier2.005** The Confessor's Warning | **Dominated fix:** b ("Hear them out") now also sets `eotg_flag_suppress_progression` 3 years (you promise to go no further). c: + helper cruelty. | **d [cynical]** "Your god has no say over my body." +50 prestige, −50 piety, confessor `eotg_opinion_aug_disgust`. Stress: cynical minor loss. Risk +2. **e [theologian]** "Then let us argue it properly." `duel = { skill = learning  target = scope:confessor … }`: win (weighted by the learning gap) = confessor `eotg_opinion_aug_admiration`, +75 piety; lose = −50 piety, confessor `eotg_opinion_aug_disgust`. Duel shape as vanilla `events/activities/chariot_race_activity/chariot_ongoing_events_jp.txt:195`. | b −5, c +3, d +2 |
| **tier2.006** Cold Detachment | b: + helper reject. c: "+1 learning" → lesson learning. | **d [eccentric]** "Fascinating. Let it run." Lesson learning, risk +6. Stress: eccentric minor loss. **e [stubborn]** "I will drag it up by the roots if I have to." Remove `eotg_mod_aug_affect_dampened` if held. Stress: base minor gain, stubborn minor loss. Risk +2. | c +3, d +6, e +2 |

## 4. Overclocked (`events/eotg_augmentation_tier3.txt`)

| Event | Change to existing options | New options | Risk |
|---|---|---|---|
| **tier3.001** Violent Impulse | **Victims (audit §1.5):** `immediate` → `eotg_aug_pick_victim_effect = { NAME = eotg_victim  FAMILY_FACTOR = 0.05 }`. The desc names `scope:eotg_victim` (with a no-one-near variant). b/c act on `scope:eotg_victim` with option `trigger = { exists = scope:eotg_victim }`. b: + helper wound. c: + helper murder. | **d [calm]** "Breathe. Count. Walk out." −50 prestige (you leave mid-audience), risk −6. Stress: calm medium loss. **e [wrathful]** "Take it out on the practice posts." +10 dread, risk +5. Stress: wrathful medium loss. | a −3, b +5, c +15, d −6, e +5 |
| **tier3.002** The Mirror | c: "+3 prowess permanent" → **+1 permanent prowess + lesson prowess** (B6: c is repeatable, but "remove more flesh" is the closest thing to a milestone, so it keeps 1 permanent point). | **d [arrogant]** "Perfect." +150 prestige, risk +12. Stress: arrogant minor loss. **e [humble]** "Cover the mirrors." −50 prestige, risk −5. Stress: humble medium loss. | all options |
| **tier3.003** Sleepless | c: keep the permanent −2/−2 (a loss, not farmable). | **d [diligent]** "Then use the hours." `add_gold = minor_gold_value`, risk +10. Stress: diligent minor loss. **e [lazy]** "Lie there anyway." Helper neglect, risk +5. Stress: lazy minor loss. | b +20, c −10, d +10, e +5 |
| **tier3.004** Signal Noise | **Victims:** c's target → `eotg_aug_pick_victim_effect = { NAME = eotg_suspect  FAMILY_FACTOR = 0.05 }` in `immediate`; the desc names them. c: + helper cruelty. b: cost `minor_gold_value`. | **d [trusting]** "These are my people. Shut the alerts off." `scope:eotg_suspect` gets `eotg_opinion_aug_reassured`, risk +5. Stress: trusting medium loss. **e [paranoid]** "Seventeen? It missed some." `imprison = { target = scope:eotg_suspect  type = dungeon }` (vanilla form, `events/activities/hunt_activity/hunt_events.txt:529`), lesson intrigue, helper tyranny, risk +10. Stress: paranoid minor loss. | a +5, b −5, c +10, d +5, e +10 |
| **tier3.005** Clarity | c: "+1 learning" → lesson learning. | **d [brave]** "Lead the charge myself." +250 prestige, lesson prowess, 20% `increase_wounds_effect = { REASON = battle }`, risk +10. **e [craven]** "Let the machine command from the rear." +100 prestige, risk +6. Stress: craven medium loss. | a +8, b +3, d +10, e +6 |
| **tier3.006** The Delegation | a: in-flight fix (arrest) + helper tyranny. b: in-flight fix. c: + helper cruelty. | **d [just]** "Convene an inquiry into my own fitness." −150 prestige, the disaffected vassals get `eotg_opinion_aug_reassured`, risk −5. Stress: just medium loss. | c +12, d −5 |
| **tier3.007** Two Machines | a: in-flight fix (mutual). b: "+1 intrigue" → lesson intrigue. c: "+2 prowess both" → lesson prowess for both. | **d [gregarious]** "Recruit them." `scope:other_machine` gets `eotg_opinion_aug_admiration`; root gets lesson martial. Risk +5 on both. (Phase 4c adds the duel/alliance follow-up.) | b +5, c +10 ×2, d +5 ×2 |

## 5. Neurofractured (`events/eotg_augmentation_fracture.txt`)

| Event | Change to existing options | New options | Risk |
|---|---|---|---|
| **fracture.0001** Neural Cascade | **Victim:** `immediate` uses the picker (`NAME = eotg_victim`, `FAMILY_FACTOR = 0.05`, 40% chance as before); the desc names them. Keep the single forced option a: loss of agency is the point. | — | (cascade is the tier change) |
| **fracture.002** Containment Failure (renamed from *Containment Breach*, lore review; the c-option text reads "witnesses to the failure") | **Victims:** `immediate` → picker for the wounded (`eotg_victim`, 50%) and the killed (`eotg_victim_dead`, 20%, via `eotg_aug_pick_second_victim_effect`), `FAMILY_FACTOR = 0.05`. The wounded victim gets `eotg_flag_aug_breach_victim` 30 days. a: + helper cruelty. c: "execute the survivors" → `every_courtier = { limit = { has_character_flag = eotg_flag_aug_breach_victim } … }` (audit §1.5) + helper murder. | **d [sadistic]** "Again." Picker for one more wounded courtier, +30 dread, risk +15. Stress: sadistic medium loss. **e [compassionate]** "Tend them with my own hands." `scope:eotg_victim` (if exists) gets `eotg_opinion_aug_grateful_patient` (Phase 2 key; admiration until then), −50 prestige, risk −5. | a +10, b −10, d +15, e −5 |
| **fracture.003** Lucid Moment | **Dominated fix:** c ("Weakness disgusts me") → stress `medium_stress_impact_loss` (was massive), risk +15 (was +10). | **d [zealous]** "Pray, while you still know the words." +100 piety, risk −5. Stress: zealous medium loss. | b −10, c +15, d −5 |
| **fracture.004** The Court Massacre | **Victims:** `immediate` → picker ×2 (`eotg_victim_dead` killed, `eotg_victim` wounded), `FAMILY_FACTOR = 0.25` (Storm-scale, deliberate). The flat "20% spouse" block is **removed**: the family weight replaces it. a: + helper cruelty. | **c (universal)** "Bury them with honours." −100 prestige, +50 piety, risk −3. **d [just]** "Hand myself to the court's judgement." −200 prestige, `add_tyranny = -20`, risk −8. Stress: just medium loss. **e [callous]** "Replace them by morning." +20 dread, risk +5. Stress: callous minor loss. | a +10, b −5, c −3, d −8, e +5 |
| **fracture.005** What the Heir Saw | a: + helper cruelty. c: + helper cruelty. (Phase 3a re-homes this event into the Heir's Arc; its options stay.) | **d [honest]** "Tell them everything." Heir gets `eotg_opinion_aug_reassured`, risk −5. Stress: honest medium loss. **e [deceitful]** "It was a seizure. Nothing more." Helper lie; heir 50% reassured / 50% unease. | a +5, b −5, d −5 |
| **fracture.006** The Warrant | a: + helper tyranny. c: + helper cruelty. (Phase 3a makes the faction real and adds its trait options.) | — | c +20 |
| **fracture.007** Dead Reckoning | a: `add_gold = minor_gold_value` (B5). **Dominated fix:** c ("Burn them") → `medium_stress_impact_loss`, −100 prestige, risk −5. | **d [greedy]** "Sell them." `add_gold = medium_gold_value`, −50 prestige, risk +10. **e [generous]** "Give them to the vassals who need them." Vassals with opinion < 0 get `eotg_opinion_aug_reassured`, risk −3. | a +15, c −5, d +10, e −3 |

---

## 6. Coverage after Phase 1

Personality traits that now appear **on screen**, i.e. gated options, not just AI weights or helpers:
arrogant, brave, callous, calm, compassionate, content, craven, cynical, deceitful, diligent, eccentric, generous, greedy, gregarious, honest, humble, just, lazy, paranoid, sadistic, shy, stubborn, trusting, wrathful, zealous (25 of 36).

Also gated on screen: `lifestyle_blademaster` and `theologian`.

Reached only through stress helpers in this phase: forgiving, arbitrary, vengeful.

Left for Phase 4 (each has a planned gated option there): ambitious (tier1.021), chaste, lustful, temperate, gluttonous, fickle, impatient, patient, forgiving, vengeful.

## 7. Loc (eotg-localizer)
- ~40 new option keys: every **new options** cell above (`<event>.d`, `.e`, and the new `c` on tier2.002 / fracture.004).
- Desc variants: tier3.001, tier3.004, fracture.0001, .002, .004 each get a `triggered_desc` naming the victim, plus a "no one was near" variant (~10 keys).
- Revise existing option text where behaviour changed: init.002.a (now a purchase), tier1.005.c, tier1.006.b, tier2.004.b, tier2.005.b, fracture.003.c, fracture.004 (no explicit spouse line), fracture.007.c.

## 8. Definition of done
0. **Validation, all three clean** on the phase's files, except the known-benign items listed in `CLAUDE.md` §Validation: Tiger 1.17.0 (scratch descriptor), `docs/tools/px_lsp_diagnostics.js` (PX language server, headless) and `docs/tools/px_vocab_check.py` (engine vocabulary + dead hooks). Tiger is the only one of the three that checks scope.
1. Each of the 14 options in audit §3.3 calls a stress helper (QA greps by event.option).
2. `random_courtier` no longer appears in an `increase_wounds_effect` or `death` context in tier3/fracture files; all such sites use the picker and name the victim.
3. Every new option has `trigger` + `trait` (trait options) and an `ai_chance`.
4. No permanent `add_*_skill` with a positive value remains in a repeatable flavor option, except tier3.002.c's +1 prowess.
5. No flat gold literal remains in the five event files.
6. **Human, in game:** a brave, a craven and a cynical ruler each see different options on init.001/init.004. A Violent Impulse names its victim.
