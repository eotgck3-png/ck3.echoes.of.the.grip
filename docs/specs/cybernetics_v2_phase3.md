# Cybernetics v2 — Phase 3: Neurofractured mode and the endgames

Index: [cybernetics_v2.md](cybernetics_v2.md). Rules in index §1 apply. Needs Phase 0 (drift, band triggers, picker, stress helpers). **3a** ships alone. **3b** needs 3a's on_action restructure and band triggers.

**Purpose & gate.** Gate 3. Not blocked. *"I don't control this anymore."* Neurofractured stops being a louder Overclocked. It gets:
- pressure that drifts through three hidden bands, each with its own pool;
- outcomes that do not match the button pressed;
- false information that is corrected months later;
- identity erosion;
- named victims;
- the realm reacting: a real faction, a regency, an heir who acts;
- four endings.

**Signature resource.** `eotg_fracture_risk` read as **pressure**:
- Phase 0's drift raises it every year;
- calm options lower it;
- the band selects the pool;
- ≥ 95 fires the terminal event.

Every event below moves it, or (endgames) changes tier.

---

# 3a — Bands, pools, the Heir's Arc, the realm

## 1. On_action: `eotg_on_yearly_aug_neurofractured_check` (rewritten)

Order inside `effect`, all under `limit = { has_trait = eotg_neurofractured }`:

1. **Drift** (Phase 0 §1.2). Always runs.
2. **Heir's Arc start** (no cooldown; the story owns its pacing): `if` `is_landed = yes`, `eotg_aug_has_heir_arc = no` (`any_owned_story = { story_type = eotg_story_aug_heir_arc }`), NOT `eotg_flag_aug_heir_arc_done`, and `primary_heir ?= { is_alive = yes  age >= 14 }`, then `create_story = eotg_story_aug_heir_arc`. **The arc runs once per ruler** (*CB-26 M11*): heir.004, and the story's landless exit, set the permanent `eotg_flag_aug_heir_arc_done`. Balance §5.8(a) adds a second start site at Overclocked with the same guard.
3. **Terminal.** `if` `var:eotg_fracture_risk >= 95` and NOT `eotg_flag_aug_terminal_cooldown`: set that flag (`months = 11`) and fire **fracture.027** *The Cascade*. This replaces the year's roll.
4. **`else_if`** NOT `eotg_flag_nf_event_cooldown` → three band lists (`if` storm / `else_if` fracture / `else` flicker). Each branch sets `eotg_flag_nf_event_cooldown` `months = 11` unless stated otherwise.

While `eotg_flag_aug_restrained` is set, the weight of every branch marked **V** (violent) is multiplied by 0.25 (`modifier = { factor = 0.25  has_character_flag = eotg_flag_aug_restrained }`).

**Storm band (`eotg_aug_pressure_storm`)**

| Weight | Trigger (mirrored as the event trigger) | Event |
|---|---|---|
| 35 | `any_vassal = { opinion = { target = root  value < -30 } }` | fracture.006 *The Warrant* (made real, §3) |
| 30 | `basic_eligible_for_diarchy_trigger = yes`, `has_active_diarchy = no`, a keeper exists (spouse, or adult primary heir) | fracture.025 *Containment Regency* |
| 40 **V** | `stress_level >= 2` | fracture.004 *The Court Massacre* (cooldown `months = 23`) |
| 30 **V** | — | fracture.002 *Containment Failure* |
| 20 | NOT `eotg_flag_aug_scramble_cooldown` (set here, 5 years) | fracture.018 *Scrambled* |
| 10 | NOT `eotg_flag_aug_last_lucid` (set here, 5 years) | fracture.026 *The Last Lucid Moment* |
| 8 | — | fracture.007 *Dead Reckoning* |
| 40 | — | nothing |

**Fracture band (`eotg_aug_pressure_fracture`)**

| Weight | Trigger | Event |
|---|---|---|
| 40 **V** | — | fracture.002 *Containment Failure* |
| 30 **V** | — | fracture.016 *Blood on the Sleeve* |
| 25 | — | fracture.017 *Terms of Access* |
| 20 | NOT scramble cooldown (set, 5 years) | fracture.018 *Scrambled* |
| 25 | `any_courtier = { eotg_aug_victim_candidate = yes }` | fracture.019 *The Flagged Name* |
| 15 | `any_courtier = { eotg_aug_victim_candidate = yes  NOT = { is_close_family_of = root } }` | fracture.021 *The Missing Courtier* |
| 20 | `OR = { NOT = { has_variable = eotg_aug_voice }  var:eotg_aug_voice < 3 }` | fracture.022 *We* |
| 15 | — | fracture.023 *The Wrong War* |
| 20 | `any_courtier = { eotg_is_augmented_any = yes }` | fracture.024 *The Same Pattern* |
| 5 | — | fracture.007 *Dead Reckoning* |
| 60 | — | nothing |

**Flicker band (`eotg_aug_pressure_flicker`)**

| Weight | Trigger | Event |
|---|---|---|
| 15 | — | fracture.003 *Lucid Moment* |
| 25 | `OR = { exists = primary_heir  is_married = yes }` | fracture.008 *Wrong Name* |
| 25 | — | fracture.009 *Lost Hour* |
| 20 | — | fracture.010 *The Mirror Doesn't Blink* |
| 20 | `any_courtier = { eotg_aug_victim_candidate = yes }` | fracture.011 *Conversations With No One* |
| 20 | `OR = { any_relation = { type = friend }  any_relation = { type = lover }  is_married = yes }` | fracture.012 *The Familiar Stranger* |
| 15 | — | fracture.013 *Memory of Tomorrow* |
| 15 | — | fracture.014 *The Door* |
| 15 | `any_vassal = { is_alive = yes }` | fracture.015 *The Unsent Letter* |
| 60 | — | nothing |

`fracture.005` *What the Heir Saw* **leaves** the random pool: the Heir's Arc fires it (§4). The existing ≥30/≥60 weight modifiers are deleted; the bands replace them.

## 2. Shared 3a effects (`common/scripted_effects/eotg_augmentation_effects.txt`)

**`eotg_aug_scramble_personality_effect`.** One `random_list` with 34 entries, weight 10 each. Each entry is `trigger = { has_trait = A }  remove_trait = A  add_trait = B` for the pairs below, read from vanilla `opposites` (`game/common/traits/00_traits.txt`):

| Pair |
|---|
| brave ↔ craven |
| calm ↔ wrathful |
| chaste ↔ lustful |
| content ↔ ambitious |
| diligent ↔ lazy |
| fickle ↔ stubborn |
| forgiving ↔ vengeful |
| generous ↔ greedy |
| gregarious ↔ shy |
| honest ↔ deceitful |
| humble ↔ arrogant |
| just ↔ arbitrary |
| patient ↔ impatient |
| temperate ↔ gluttonous |
| trusting ↔ paranoid |
| zealous ↔ cynical |
| compassionate → callous, callous → compassionate, sadistic → compassionate |

That is 16 pairs × 2 = 32 entries, plus the 2 one-way lines in the last row. Fallback entry (weight 1, `trigger` none of the above): `add_trait = paranoid`. Always remove before adding (opposites). `eccentric` is never touched.

**`eotg_aug_forget_relation_effect`.** First valid of:
- `random_relation = { type = soulmate }` → `remove_relation_soulmate`;
- `best_friend` → `remove_relation_best_friend`;
- `lover` → `remove_relation_lover`;
- `friend` → `remove_relation_friend`.

Save the person as `scope:eotg_forgotten` and give them `eotg_opinion_aug_unease` (5 years). The effect names them itself, with a toast after the fact: `hidden_effect = { send_interface_toast = { title = eotg_aug_forget_relation_toast  left_icon = scope:eotg_forgotten } }` (vanilla hidden-outcome toast, hunt.8540, as tier3.014.b). Callers roll it on the click, so no option tooltip can name the person in advance. *CB-26 L14.*

**`eotg_aug_raise_warrant_effect`.** Caller saves `scope:eotg_warrant_vassal`. Shape copied from vanilla `prelude_events_0010_screw_over_guest_effect` (`events/activities/coronation_activity/prelude_events.txt:236`).
```
if = { limit = { any_targeting_faction = { always = yes } }          # root is the target
    every_targeting_faction = { add_faction_discontent = major_discontent_gain } }
else_if = { limit = { scope:eotg_warrant_vassal = { can_create_faction = { type = liberty_faction  target = root } } }
    scope:eotg_warrant_vassal = { create_faction = { type = liberty_faction  target = root } } }
else_if = { limit = { scope:eotg_warrant_vassal = { can_create_faction = { type = independence_faction  target = root } } }
    scope:eotg_warrant_vassal = { create_faction = { type = independence_faction  target = root } } }
else = { every_vassal = { limit = { opinion = { target = root  value < 0 } }
    add_opinion = { modifier = eotg_opinion_aug_disgust  target = root  years = 5 } } }   # the warrant circulates
```
Liberty (lower crown authority) is the thematic fit: "bind the mad ruler", not "replace them". The vanilla factions and CBs then run the war. No mod titles are involved.

**`eotg_aug_start_containment_regency_effect = { KEEPER = scope:x  SWING = n }`.**
```
if = { limit = { basic_eligible_for_diarchy_trigger = yes  has_active_diarchy = no
                 $KEEPER$ = { is_alive = yes  is_adult = yes  is_imprisoned = no } }
    designate_diarch = $KEEPER$
    try_start_diarchy = regency
    set_diarchy_swing = $SWING$
    add_character_flag = eotg_flag_aug_containment_regency }
```
Precedent: `events/bookmark_events.txt:2247–2249`. **Q7:** an in-game check is needed that a capable adult's regency persists. If the engine ends it, add vanilla `isolating_modifier` with `years = 3` inside this effect. `isolating_modifier` is an OR term of `regency_for_personal_reasons_trigger`, `common/scripted_triggers/00_diarchy_scripted_triggers.txt:205`.

## 3. Events — `events/eotg_augmentation_fracture.txt` (namespace `eotg_fracture`)

Conventions:
- Universal options come first, trait options after (usually a–c, then d–e). A universal option may follow a trait option where an event gained one later (fracture.026.d, fracture.007.f, end.020 d/e). *CB-26 S11.*
- "picker(N, F)" = `eotg_aug_pick_victim_effect = { NAME = N  FAMILY_FACTOR = F }`.
- Every option moves risk unless marked "—". The event couples through at least one option.
- Desc `triggered_desc` variants on `var:eotg_aug_voice` are marked **[voice]**: 0–1 "a thought that arrives a half-second before you think it", 2 "it" (the model), 3 "we", 4 "we, on agreed terms". Every **[voice]** line follows the register rule and banned-word list in index §5.

### Flicker band — eerie, small, wrong

**fracture.008 Wrong Name.**
- **Saved:** `eotg_named` (primary heir, else spouse). `eotg_dead_name`: `random_child = { even_if_dead = yes  limit = { is_alive = no } }`, else a dead parent, else a dead spouse. With none, the **[voice]** variant applies: "a designation, not a name: a string of characters and a number".
- **a** "Laugh it off." −25 prestige. Risk −3.
- **b** "Insist you said it right." `eotg_named` gets `eotg_opinion_aug_fear`. Helper lie. Risk +5.
- **c** "Ask them to say their name back to you." Stress minor gain. Risk −5.
- **d [compassionate]** "Say their real name until it sticks." `eotg_named` gets `eotg_opinion_aug_reassured`. Risk −5.
- **e [arrogant]** "Then that is their name now." +5 dread. `eotg_named` gets fear. Risk +5.

**fracture.009 Lost Hour.**
- **a** "Find out what I did." `random_list`:
  - 50: nothing;
  - 30: you signed something, `remove_short_term_gold = minor_gold_value`;
  - 20: picker(`eotg_victim`, 0.05) wounded (`REASON = attacked`), named in the option's follow-up text.

  Risk +3.
- **b** "Don't look." Helper neglect. Risk +5.
- **c** "Have someone watch me." −25 prestige. Risk −5.
- **d [paranoid]** "Lock the door from the outside." `eotg_mod_withdrawn_from_court` 1 year. Risk −3.
- **e [diligent]** "Log every minute from now on." Risk −6. Stress: diligent minor loss.

**fracture.010 The Mirror Doesn't Blink.** Technological framing: the implant's overlay renders your reflection a moment late. It echoes tier3.002 *The Mirror*: a desc variant applies if the ruler ever saw it (flag `eotg_flag_aug_saw_mirror`, set by tier3.002 options from this phase on).
- **a** "Break it." Stress minor loss. Risk +3.
- **b** "Stare back." **[voice]**: at voice ≥ 2 the overlay labels your own face. Risk +5.
- **c** "Cover every mirror in the residence." −25 prestige. Risk −3.
- **d [zealous]** "Bless the glass." +50 piety. Risk −3.
- **e [eccentric]** "Talk to it." `eotg_aug_voice_advance_effect = { STAGE = 2 }`: if they never had *First Contact*, this is it. Risk +5.

**fracture.011 Conversations With No One.** Saved `eotg_witness`: picker(…, 0), used only as a witness.
- **a** "I was rehearsing." Helper lie. 50%: the witness gets `eotg_opinion_aug_unease`. —
- **b** "Tell them who I was speaking to." Voice advance 2. The witness gets fear. Risk +5.
- **c** "Pay for their silence." `remove_short_term_gold = minor_gold_value`. Risk −3.
- **d [shy]** "Leave. Now." −25 prestige. Stress shy minor loss. Risk +3.
- **e [deceitful]** "You heard nothing." Lesson intrigue. Helper lie.

**fracture.012 The Familiar Stranger.** Saved `eotg_stranger`: a friend, else a lover, else the spouse.
- **a** "Pretend." Helper lie. Risk +3.
- **b** "Tell them you don't know them any more." Remove the relation with them, using the same effect bodies as `eotg_aug_forget_relation_effect` but targeted at `scope:eotg_stranger`. They get `eotg_opinion_aug_disgust`. Risk −3.
- **c** "Ask them who you used to be." They get `eotg_opinion_aug_reassured`. Stress minor gain. Risk −5.
- **d [trusting]** "If they say so, it's so." Reassured. —
- **e [paranoid]** "An impostor." They get fear. Helper tyranny. Risk +5.

**fracture.013 Memory of Tomorrow.**
- **a** "Write it down." Sets `eotg_flag_aug_premonition` 1 year. A `triggered_desc` in fracture.027 / heir.004 reads it: "you remember this". Risk +3.
- **b** "Act on it." 50%: +100 prestige. 50%: −100 prestige. Risk +5.
- **c** "Ignore it." Stress minor gain. Risk −3.
- **d [eccentric]** "Stake the treasury on it." 50%: `add_gold = medium_gold_value`. 50%: `remove_short_term_gold = medium_gold_value`. Risk +5.
- **e [patient]** "Wait and see if it comes." Risk −5.

**fracture.014 The Door.** Desc: the implant's spatial overlay has drawn a door on a load-bearing wall. It is hardware, not a threshold.
- **a** "Have a work crew cut it." `remove_short_term_gold = minor_gold_value`, −50 prestige. Risk −5.
- **b** "Walk through it anyway." 30%: `increase_wounds_effect = { REASON = fall }` on root. Risk +5.
- **c** "Let the court pretend there is a door." −25 prestige. Risk −2.
- **d [stubborn]** "It's there. I'll wait for it to open." Risk +5.
- **e [humble]** "Then I am wrong. Help me." −50 prestige. Risk −5.

**fracture.015 The Unsent Letter.**
- **Saved:** `eotg_addressee`, a random vassal. In `immediate`, set a local variable to `flag:confession` / `flag:threat` / `flag:devotion` (equal weights). The desc varies on it.
- **a** "Burn it." Risk −3.
- **b** "Send it." By type:
  - confession: the addressee gets unease, −50 prestige;
  - threat: fear, +10 dread;
  - devotion: admiration.

  Risk +5.
- **c** "Read it aloud to the court." −100 prestige. Risk +3.
- **d [honest]** "Send it with a note: *I don't remember writing this.*" The addressee gets reassured. Risk −3.
- **e [deceitful]** "Rewrite it into something useful." Lesson intrigue. Risk +3.

### Fracture band — violence and lost time

**fracture.016 Blood on the Sleeve.**
- **`immediate`:** picker(`eotg_victim`, 0.05). `random_list`: 60 wounded (`increase_wounds_effect = { REASON = attacked }`); 40 dead (`death = { death_reason = death_murder  killer = root }`). Set a local variable for the outcome. The desc shows only the blood. **Without a victim**, the event reads "the blood is your own": root gets `wounded_1`.
- **a** "Find out whose it is." The option text names the victim. If dead: `add_tyranny = 5`. Risk +5.
- **b** "Burn the shirt." Helper lie. Risk +10.
- **c** "Confess it to the court." −150 prestige. Stress: honest minor loss. Risk −8.
- **d [callous]** "Does it matter whose?" +10 dread. Risk +5.
- **e [just]** "Pay blood-price to their kin." `remove_short_term_gold = medium_gold_value`. The victim's close family at court gets `eotg_opinion_aug_reassured`. Risk −5.

All options carry helper wound (if wounded) or helper murder (if dead).

**fracture.017 Terms of Access** (T1, beat 4; renamed per lore review 2026-10-03). A **permissions request**: the implant's model asks for wider access to act ahead of you. It is a transaction, never a pact. **[voice]** desc; at voice < 2, "for the first time, it requests access". Agency is unreliable: some options roll a hidden `random_list`, and an override fires **fracture.028** *The Terms*, a 1-option notification saying what access the implant granted itself. **Mechanics are unchanged from the original spec.**
- **a** "Grant it." Voice advance 4. Lesson martial + lesson intrigue, +100 prestige. Risk +15.
- **b** "Deny it." `hidden_effect` `random_list`: 70 honoured (risk −5); 30 **override** (as a, minus the lessons; fire fracture.028). The tooltip shows only the denial.
- **c** "Negotiate the terms." `random_list` 50 + 3 × intrigue: partial terms (lesson intrigue, risk +5); else risk +10.
- **d [ambitious]** "What do I get in return?" As a, +150 prestige. Risk +20.
- **e [zealous]** "No device speaks for me." `hidden_effect`: 85 honoured (risk −8, +50 piety); 15 override → fracture.028.

**fracture.018 Scrambled.** The scramble happens inside the options, so the trait change shows in the tooltip.
- **a** "Who was I?" `eotg_aug_scramble_personality_effect`. 25%: `eotg_aug_forget_relation_effect`. Risk +5.
- **b** "Hold on to it." `random = { chance = 50  eotg_aug_scramble_personality_effect }`. Stress medium gain. —
- **c** "Let it go. Let all of it go." Scramble twice. Risk −5: the fight ends.
- **d [stubborn]** "No." `random = { chance = 20  … }`. Stress: stubborn medium loss. —
- **e [fickle]** "Does it matter?" Scramble. Stress: fickle medium loss. Risk −3.

**fracture.019 / .020 The Flagged Name** (specced as *The False Traitor*; unreliable perception).

*fracture.019.* `immediate`:
- saves `eotg_accused`: `random_vassal` (alive), else picker(…, 0.05);
- sets `eotg_aug_accusation_true`: `random_list` 20 true / 80 false, stored as a variable on root;
- fires fracture.020 from every option, 90–180 days later.

Options:
- **a** "Arrest them." `imprison = { target = scope:eotg_accused  type = dungeon }`. Helper tyranny. Risk +5.
- **b** "Have them watched." Risk +3.
- **c** "Execute them." `scope:eotg_accused = { death = { death_reason = death_execution  killer = root } }`. Helper murder. +20 dread. Risk +10.
- **d [paranoid]** "Their family too." Imprison the accused and their close family at root's court. `add_tyranny = 20`. Risk +12.
- **e [trusting]** "No. Not them." The accused gets reassured. Risk +5 (overriding the implant costs).

`death_execution` is a vanilla reason (`game/common/deathreasons/00_event_deaths.txt`, checked).

*fracture.020 (the truth).* The desc varies by truth × what was done: **6 variants**, `desc_true_spared` (true, and the ruler spared them via .019.e), `desc_true`, `desc_false_executed`, `_arrested`, `_watched`, `_spared`. Options a–d are merged by round 2 into a release option plus one ungated fallback whose name picks by case; on the true-and-spared path its name is `eotg_fracture.020.c_spared` and it gives **no** prestige (risk +5 stays). *CB-26 L15.*
- If false: the accused's close family and the accused (if alive) get `eotg_opinion_aug_falsely_accused`; `add_tyranny = 10` if they were executed.
- **a** (false, imprisoned) "Release them. I was wrong." `release_from_prison`. Risk −5.
- **b** (false) "I was right anyway." Helper lie, `add_tyranny = 10`. Risk +10.
- **c** (true) "As I knew." +100 prestige. Risk +5. (The implant was right this once, so you will trust it next time.)

**fracture.021 The Missing Courtier.** `immediate`: picker(`eotg_missing`, 0). `random_list` 50 left court (`move_to_pool`) / 50 dead (`death_murder`, killer root). The desc doesn't say which.
- **a** "Search for them." `remove_short_term_gold = minor_gold_value`. If they left: `add_courtier = scope:eotg_missing` (found). If dead: found dead. Risk −3.
- **b** "I ordered it. It is done." +15 dread, `add_tyranny = 5`. Risk +10.
- **c** "Ask the guards what I said." Reveals "you did order it". Helper murder. Risk +5.
- **d [just]** "Open an inquiry, even if it ends at my door." −100 prestige. Risk −6.

**fracture.022 We** (specced as *The Second Voice*; T1, beat 3). **All options** run voice advance 3 first: the slip already happened.
- **a** "We — I. I meant I." Stress minor gain. Risk −5.
- **b** "We." +10 dread. The spouse gets unease. Risk +10.
- **c** "Put it in the logs." Lesson learning. Risk +3.
- **d [arrogant]** "We are more than any one ruler." +100 prestige. Risk +10.
- **e [humble]** "Help me. Please." The spouse and the heir get reassured; −100 prestige. Risk −8.

**fracture.023 The Wrong War.** Variant by `is_at_war`. At peace, "you are mustering for a war that does not exist". At war, "you are accepting a surrender no one offered".
- **a** "Stand them down." / "Recall the envoys." −50 prestige. Risk −3.
- **b** "The enemy is coming." / "They surrendered; I saw it." `remove_short_term_gold = minor_gold_value`; vassals with opinion < 0 get unease. Risk +8.
- **c** "Show me the maps." Lesson martial. Risk −5.
- **d [wrathful]** "Then I will make one." +15 dread. Risk +10.
- **e [calm]** "Wait for the scouts." Risk −6.

**fracture.024 The Same Pattern** (T4: the ruler alone notices an augmented courtier changing). Saved `eotg_changed`: `random_courtier = { limit = { eotg_is_augmented_any = yes } }`.
- **a** "Watch them." Risk +3.
- **b** "Confront them." 50%: they admit it (their risk −10, admiration). 50%: they deny it (unease). Root risk +3.
- **c** "Have them restrained." `imprison = { type = house_arrest }`. Helper tyranny. Their risk −10. Root risk +5.
- **d [compassionate]** "Sit with them. You both know what this is." Both risk −5. Their opinion is reassured.
- **e [paranoid]** "They report to the implant." They get fear. Root risk +8.

### Storm band — the realm reacts

**fracture.006 The Warrant (made real; audit §1.4).**
- **`immediate`:** `eotg_warrant_vassal` = `ordered_vassal = { order_by = { value = 0  subtract = "opinion(root)" } }` (the worst opinion), then `eotg_aug_raise_warrant_effect`. The desc names the vassal and says whether a faction formed or the warrant circulated.
- **a** "Crush any who stand against me." Existing effects, + `imprison = { target = scope:eotg_warrant_vassal  type = dungeon }` + helper tyranny. Risk unchanged (existing).
- **b** "Offer concessions." In-flight fix (reassured), + `every_targeting_faction = { add_faction_discontent = -50 }`.
- **c** "Let the implant decide." `hidden_effect` 50/50: as a, or `every_targeting_faction = { add_faction_discontent = 100 }` (code fires the faction demand). Risk +20 (existing).
- **d [just]** "Submit to their tribunal." −100 prestige, `every_targeting_faction = { add_faction_discontent = -100 }`. Vassals with opinion < 0 get reassured. Risk −10.
- **e [gregarious]** "Bring them to my table." `duel = { skill = diplomacy  target = scope:eotg_warrant_vassal … }`. Win: the vassal is reassured, discontent −50. Lose: discontent +25. Risk +3.

**fracture.025 Containment Regency.** Saved `eotg_keeper`: spouse (adult, free), else the adult primary heir. Desc: they come to you with the council behind them.
- **a** "Let them." `eotg_aug_start_containment_regency_effect = { KEEPER = scope:eotg_keeper  SWING = 60 }`. −100 prestige. Risk −10.
- **b** "No one takes what is mine." The keeper gets disgust. +20 dread. Helper cruelty. 30%: `eotg_aug_raise_warrant_effect` with the keeper as `eotg_warrant_vassal`, **if** the keeper is a landed vassal. Risk +10.
- **c** "On my terms." Regency at `SWING = 30`. −50 prestige. Risk −5.
- **d [paranoid]** "They've planned this for months." `imprison = { target = scope:eotg_keeper  type = house_arrest }`. Helper tyranny. Risk +12.
- **e [content]** "Take it. Please, take it." Regency at `SWING = 80`. Stress: content major loss. Risk −15.

**fracture.026 The Last Lucid Moment.** **[voice]** desc; if `eotg_flag_aug_premonition` is set, "you remember this".
- **a** "Ask for help." Regency with the keeper at `SWING = 50` if eligible; else `eotg_mod_withdrawn_from_court` 2 years. Risk −15.
- **b** "Beg the heir to act." If an Heir's Arc exists: `set_variable` its `stage = 3`, `heir_dread −2` (the heir comes as an ally). Risk −10.
- **c** "Embrace it." Voice advance 4, `eotg_flag_aug_may_embrace` (permanent). Risk +20.
- **d** "Cut it out of me." Fire `eotg_aug_end.001` (Excision, 3b). —
- **e [zealous]** "Confess before the clergy." +200 piety. Risk −10.

**fracture.027 The Cascade** (terminal, at ≥ 95). The player picks a **stance**, not an outcome: the implant decides. The desc is generic, with **[voice]** and premonition variants. Each option rolls a `random_list`; the result fires its follow-up.

| Outcome | Base | a "Let go." | b "Hold on." | c **[brave]** "Fight it." | d **[stubborn]** "Not yet." | Result |
|---|---|---|---|---|---|---|
| death | 35 (+15 `stress_level >= 3`, +10 `health < 2`) | — | +10 | — | — | `eotg_aug_cascade_death_effect` |
| total integration | 25 (+25 voice ≥ 4, +15 `eotg_flag_aug_may_embrace`) | +15 | — | −10 | −10 | `eotg_aug_total_integration_effect` → end.010 |
| excision chance | 15 (+15 phys) | — | — | — | — | end.001 with `eotg_flag_aug_excision_free` (the surgeons were already in the room) |
| abdication | 15 (+15 an Heir's Arc ended "ally" or regency active) | — | — | — | — | end.030 |
| it passes | 10 | — | +30 | +40 | +30 | fracture.029: risk set 60; picker ×2 (Storm, 0.25) wounded; +50 dread |

Every non-death outcome counts as moving risk or tier.

**fracture.028 The Terms** (notification, 1 option). It tells you what the implant agreed to. Coupling: it is the chain stage of .017, whose override already moved risk.

**fracture.029 It Passes** (notification). It names the wounded. **a** "Again it passes." **b [humble]** "Next time it won't." Risk −5.

### Changed existing events (3a)
- **fracture.004** moves to the Storm band (§1) and keeps the Phase 1 changes.
- **fracture.005** is fired by the Heir's Arc (§4). Each option also adjusts the story's `heir_dread`:

  | Option | heir_dread |
  |---|---|
  | a | +1 |
  | b | −1 |
  | c | +2 |
  | d | −1 |
  | e | 0 |

  `scope:watching_heir` becomes the story's heir variable.
- **tier3.002** (Phase 3 touch): every option sets `eotg_flag_aug_saw_mirror` (permanent), for fracture.010.

## 4. The Heir's Arc — `eotg_story_aug_heir_arc` (T3)

`common/story_cycles/eotg_augmentation_stories.txt`, `visible = no` (default). Shape copied from `game/common/story_cycles/story_cycle_murders_at_court.txt`.

- **`on_setup`:**
  - `set_variable heir = story_owner.primary_heir`;
  - `stage = 0`;
  - `heir_dread` = 0
    - +1 if the heir has `eotg_flag_aug_absent_at_birth`,
    - +1 if the owner has `eotg_flag_aug_intervention_refused`,
    - +1 if `heir opinion of owner < -20`.
- **`on_owner_death`:** `end_story = yes`.
- **`effect_group`:** `years = { 1 2 }`, `chance = 70`, `first_valid`:
  1. `var:heir` is dead, or is no longer `story_owner.primary_heir` → if a new primary heir aged ≥ 14 exists, set `heir` to them and `stage = max(stage − 1, 0)`; else `end_story = yes`.
  2. `stage = 0` → owner gets **heir.001**; `stage = 1`.
  3. `stage = 1` → owner gets **fracture.005** (saved `watching_heir` = `var:heir`); `stage = 2`.
  4. `stage = 2` → owner gets **heir.003**; `stage = 3`.
  5. `stage = 3` and owner not in the Flicker band → owner gets **heir.004**; `stage = 4`. heir.004 ends the story.
- **End conditions.** Excision and Total Integration also touch the story:
  - excision → `end_story`;
  - Total Integration → `stage = 3` (the heir must decide about the machine).

Events in `events/eotg_augmentation_heir.txt`, namespace `eotg_aug_heir`. `scope:eotg_heir` is saved from the story's `var:heir` in each `immediate`.

**heir.001 Concern.**
- **a** "Reassure them." The heir gets reassured. `heir_dread −1`. Risk −3.
- **b** "This is not your concern." The heir gets unease. `heir_dread +1`. Risk +3.
- **c** "Then learn to keep me, if it comes to that." Heir flag `eotg_flag_aug_heir_keeper`; the heir gets admiration. Risk −5.
- **d [honest]** "Tell them the truth." Reassured; the heir gets lesson learning. `heir_dread −1`. Risk −3.
- **e [paranoid]** "They want the throne." Fear. `heir_dread +1`. Risk +5.

**heir.003 The Heir's Warning.** "Step aside, or I will make you."
- **a** "I'll seek treatment." Owner flag `eotg_flag_aug_promised_treatment` 2 years (halves the Excision cost, 3b). `heir_dread −1`. Risk −5.
- **b** "Threaten them." Fear, +10 dread, helper cruelty. `heir_dread +2`. Risk +5.
- **c** "Then keep me." Regency with `KEEPER = scope:eotg_heir`, `SWING = 50`, if eligible; else the keeper flag. `heir_dread −2`. Risk −10.
- **d [just]** "Then judge me." −100 prestige. `heir_dread −1`. Risk −3.
- **e [wrathful]** "Get out." Disgust. `heir_dread +2`. Risk +5.

**heir.004 The Heir's Choice.** The heir decides. `immediate` runs `random_list`:

| Choice | Weight |
|---|---|
| **Ally** | 40 − 15 × `heir_dread` (min 5); +20 heir compassionate or honest; +20 heir has the keeper flag or is diarch; +20 heir opinion ≥ 20 |
| **Usurp** | 30 + 10 × `heir_dread`; +20 ambitious; +10 arrogant |
| **Kill** | 10 + 10 × `heir_dread`; +25 callous or sadistic; +15 vengeful; ×0 if the heir is compassionate |

Ally effect: regency `SWING = 40`, or reassured. Usurp effect: if the heir is a landed vassal, `eotg_aug_raise_warrant_effect` led by them; else regency with the heir at `SWING = 90` (vanilla regency allows overthrow at ≥ 95). Kill effect: 50% (+20 if heir intrigue ≥ 15) success → fire **heir.005 to the heir**, who kills root there. On failure, the owner's options follow.

Owner options, by outcome:

| Outcome | Option | Text | Effect | Risk |
|---|---|---|---|---|
| Ally | **a** | "Thank them." | — | −10 |
| Ally | **b [arrogant]** | "I did not ask for this." | heir unease | +5 |
| Usurp | **a** | "Let them have it." | −200 prestige | −5 |
| Usurp | **b** | "Fight." | +30 dread; imprison the heir if they are a courtier | +10 |
| Kill, failed | **a** | "Imprison them." | `imprison type = dungeon`; helper tyranny | +5 |
| Kill, failed | **b** | "Forgive them." | heir reassured | −5 |
| Kill, failed | **c [vengeful]** | "Execute them." | `death_execution`; helper murder | +15 |

The story ends after any outcome, and heir.004 sets the owner's permanent `eotg_flag_aug_heir_arc_done`: the arc never restarts for this ruler, even for a later heir (*CB-26 M11*; a later-heir arc is new scope, rulings §3).

> **Amended 2026-10-04 by [cybernetics_v2_new_beats.md](cybernetics_v2_new_beats.md) §5.1 (human-approved).** heir.004 still sets `eotg_flag_aug_heir_arc_done`, so no on_action ever creates a second arc story. But in round 1 it parks the story at a dormant `eotg_stage = 5` instead of ending it. The story's tick gives the next primary heir (14+, not the round-1 heir) a shorter round 2: heir.007 *The Next in Line* → heir.003 → heir.004, with successor descs. Round 2 ends the story for good. `eotg_aug_total_integration_effect` and fracture.026 b set stage 3 only while `eotg_stage < 4`. That file is the authority.

**heir.005 What Must Be Done** (fires to the heir, on Kill success). `immediate`: `scope:eotg_parent_ruler = { death = { death_reason = death_murder  killer = root } }`. The player becomes the heir by normal succession.
- **a** "It was mercy." —
- **b [compassionate]** "It was murder." Stress major gain.
- **c [callous]** "It was necessary." +100 prestige.
- **d** "Take the implants." The heir has `var:eotg_parent_hardware` set by on_death (Phase 2). Install as init.013.a. **Coupling:** tier change.

---

# 3b — Endgames, Total Integration, decisions

## 5. Data objects

**Trait `eotg_total_integration`** (`common/traits/eotg_augmentation_traits.txt`):

| Field | Value |
|---|---|
| category | `health` |
| icon | `eotg_total_integration.dds` (**human art; 3rd icon**) |
| opposites | `{ eotg_cybernetics  eotg_neurofractured }` |
| `shown_in_ruler_designer` | `no` |
| `can_have_children` | `no` (`_traits.info`) |
| modifiers | prowess +20; martial, stewardship, intrigue and learning +4 each; diplomacy −8; `attraction_opinion` −60; `general_opinion` −20; `stress_gain_mult` −0.75 (the machine does not suffer); `dread_gain_mult` 1.0 |
| AI values | `ai_compassion` −50, `ai_rationality` +50, `ai_honor` −20 |

**Display name "Seamless"** (lore review 2026-10-03). The key stays `eotg_total_integration` (the endgame's internal name), so Phase 0's forward references remain valid. Desc register: "There is no seam left between them and the system. Nothing in them argues any more. Decisions arrive finished." Use "self"/"personhood", never "humanity". `eotg_is_augmented_any` gains `has_trait = eotg_total_integration`. The NF on_action does not run for it, so Total Integration has **no episode pool** (Q9).

**Death reason** `common/deathreasons/eotg_augmentation_deaths.txt`: `eotg_death_cascade = { icon = "death_unknown.dds" }`. Shape from `game/common/deathreasons/00_event_deaths.txt`; fields per `_death_reasons.info`. Loc key `eotg_death_cascade`: "died in a neural cascade" (lore review 2026-10-03).

**Modifiers** (all go into `eotg_clean_all_aug_modifiers`):

| Key | Contents |
|---|---|
| `eotg_mod_aug_restrained` | prowess −4, diplomacy −2, `monthly_prestige_gain_mult` −0.25, `dread_gain_mult` 0.2 |
| `eotg_mod_aug_sedated` | martial, stewardship, intrigue, learning and diplomacy −2 each; `stress_gain_mult` −0.2; `monthly_income_mult` −0.1 (the regimen's cost, scaled) |
| `eotg_mod_aug_excision_recovery` | health −1, prowess −4, `stress_gain_mult` 0.2 |

**Opinions:**
- `eotg_opinion_aug_falsely_accused` −30, applied `years = 10` (used in 3a);
- `eotg_opinion_aug_unmade` −40, `decaying = yes`, `monthly_change = 0.5` (fields per `ck3-modding/reference/common/opinion_modifiers/*.info`: decaying requires `monthly_change` or a duration).

## 6. Effects
- **`eotg_aug_cascade_death_effect`:** `death = { death_reason = eotg_death_cascade }`.
- **`eotg_aug_excision_effect`:** `eotg_aug_remove_all_effect`, `eotg_mod_aug_excision_recovery` 5 years, `add_trait = scarred`. End any Heir's Arc (`random_owned_story = { limit = { story_type = eotg_story_aug_heir_arc }  end_story = yes }`).
- **`eotg_aug_total_integration_effect`:**
  - `remove_trait = eotg_neurofractured`, `add_trait = eotg_total_integration`;
  - `remove_trait` each of the 36 personality traits (no-ops when not held);
  - `eotg_clean_all_aug_modifiers`;
  - `remove_variable = eotg_fracture_risk`;
  - `set_variable eotg_aug_voice = 5` (loc: "There is no voice now. There is no one left for it to speak to." No seam is left, so there is no second voice);
  - every friend, best friend, lover and soulmate relation removed (`every_relation = { type = … }` + the remove effects);
  - every vassal gets `eotg_opinion_aug_unmade`;
  - Heir's Arc `stage = 3`;
  - fire end.010.

## 7. Endgame events (`events/eotg_augmentation_endgame.txt`, namespace `eotg_aug_end`)

**end.001 Excision — The Surgeons.** Fired from: `eotg_decision_aug_excision`, fracture.026.d, fracture.027 (excision outcome), fracture.007.f, end.031.c. Desc gives the odds as words, not numbers. Death odds are surgical, not fracture risk.

| Outcome | Weight |
|---|---|
| death | NF 40 / tier 3 25 / tier 2 15; −15 phys; −10 `eotg_flag_aug_promised_treatment` |
| survive, maimed | 30 |
| survive, clean | 30, +15 phys |

Death uses `death = { death_reason = death_treatment }` (vanilla). Survivors run `eotg_aug_excision_effect`, plus `add_trait = maimed` in the maimed branch, then end.002.

- **a** "Begin." Cost `major_gold_value`, ×0.5 with the promised flag; 0 with `eotg_flag_aug_excision_free`.
- **b** "Not today." No effect.
- **c [craven]** "Put me under. Don't wake me if it goes wrong." As a, death +10. Stress: craven medium loss.
- **d [brave]** "Awake. I want to watch them take it out." As a; maimed weight → clean. +100 prestige on survival.

**end.002 Silence** (survivors).
- **a** "It's quiet." Stress medium loss.
- **b** "I miss it." Stress minor gain.
- **c [zealous]** "Quiet. At last." +100 piety.

Coupling: the chain stage of a tier exit.

**end.009 Hand Over the Controls** (from `eotg_decision_aug_embrace_cascade`; renamed per lore review). Desc lists what will go: friends, personality, children. It speaks of the **self** or **personhood**, never "humanity". No option text may contain "open" or "through".
- **a** "Yes." `eotg_aug_total_integration_effect`.
- **b** "...No." Risk −10.
- **c [ambitious]** "Yes. All of it." As a, +200 prestige.

**end.010 There Is No Static** (Total Integration notification).
- **a** "Continue."

**end.011 The Empty Hall** (fired 180 days after end.010). `immediate`: every courtier who is not close family and has opinion < 0 → `move_to_pool`. The desc gives the number gone.
- **a** "Hire replacements." `remove_short_term_gold = major_gold_value`.
- **b** "Let them go."
- **c** "Make them stay." +50 dread, `add_tyranny = 20`. **Too late:** the departures already happened in `immediate`. This only sets the tone.

Coupling: reads the Total Integration trait (event trigger).

**end.020 Appoint a Warden** (from the decision; renamed per lore review: "Keeper" sat too close to the Name-Keepers clergy). Candidates saved: spouse, adult primary heir, `cp:councillor_chancellor`.
- **a / b / c** Pick one: regency with them at `SWING = 50`. Risk −8.
- **d** "And give them the crown." → end.030.
- **e** "No one." No effect.

**end.030 Into Restraints** (abdication). Precedent for the player hand-off: `common/decisions/dlc_decisions/tgp/tgp_dynastic_cycle_decisions.txt:2155–2170` (`set_player_character` to the heir, then the stepping-down effect). Effect:
1. save `scope:eotg_successor = primary_heir`;
2. if `is_ai = no`, `set_player_character = scope:eotg_successor`;
3. `depose = yes`;
4. `eotg_mod_aug_restrained` permanent;
5. `add_character_flag = eotg_flag_aug_abdicated`;
6. fire end.031 to the successor in 30 days.

Options:
- **a** "Go quietly."
- **b [stubborn]** "Drag me." +20 dread on the successor.

**end.031 The Locked Wing** (to the successor; the old ruler is a courtier and still Neurofractured). Saved `eotg_old_ruler`.
- **a** "Keep them comfortable." Old ruler risk −10.
- **b** "Keep them chained." Old ruler risk +5; helper cruelty.
- **c** "Have it cut out of them." → end.001 for `scope:eotg_old_ruler`, fired to them with the successor paying.
- **d** "End it quietly." `death_murder` killer root; helper murder.

Coupling: moves the old ruler's risk, or changes their tier.

**Existing event touched in 3b:** **fracture.007.f** (new universal option) "Read the last page: how to cut it out." → end.001.

## 8. Decisions (`common/decisions/eotg_augmentation_decisions.txt`)

| Key | is_shown | is_valid | Cost / cooldown | Effect | AI |
|---|---|---|---|---|---|
| `eotg_decision_aug_restraints` | `has_trait = eotg_neurofractured`, NOT `eotg_flag_aug_restrained` | — | `minor_gold_value` | `eotg_flag_aug_restrained` + `eotg_mod_aug_restrained`, both `years = 3` (renewable when it lapses). Violent NF weights ×0.25; drift −4 (Phase 0). | `ai_potential = { OR = { has_trait = compassionate  has_trait = content } }`; base 10 |
| `eotg_decision_aug_sedation` | NF, NOT `eotg_flag_aug_sedated` | — | `medium_gold_value` | `eotg_flag_aug_sedated` + `eotg_mod_aug_sedated`, `years = 5`. Drift −6. | `stress_level >= 2`; base 15 |
| `eotg_decision_aug_appoint_warden` | NF, `has_active_diarchy = no`, `basic_eligible_for_diarchy_trigger = yes` | a candidate exists | `cooldown = { years = 5 }` | → end.020 | base 5, +20 if the heir is an adult |
| `eotg_decision_aug_embrace_cascade` | NF, `eotg_aug_pressure_storm = yes`, `OR = { var:eotg_aug_voice >= 3  has_character_flag = eotg_flag_aug_may_embrace }` | — | — | → end.009 | +30 ambitious, +20 callous, −50 compassionate |
| `eotg_decision_aug_excision` | `OR = { eotg_is_aug_tier3 = yes  has_trait = eotg_neurofractured }` (**tier 2 removed**, owner ruling 2026-10-05, below) | `gold >= major_gold_value` (or the promised flag) | `cooldown = { years = 5 }`; cost is charged in end.001 | → end.001 | `stress_level >= 3`; base 3 (superseded by balance §5.2) |

**Owner ruling, 2026-10-05: one removal step per stage** (source: the owner, after the first in-game playtest; relayed in `docs/handoffs/orchestrator_2026-10-05_cyber-fix-batch.md` part B). Each stage shows the player exactly one way down, plus Excision only where nothing gentler is left:

| Stage | Removal decisions shown |
|---|---|
| Augmented (tier 1) | Remove the Implants (`eotg_decision_remove_implants`), safe full removal |
| Enhanced (tier 2) | Partial Implant Removal (`eotg_decision_partial_removal`) **only** |
| Overclocked (tier 3) | Initiate Downgrade Protocol (`eotg_decision_overclock_regression`), plus Cut It Out (`eotg_decision_aug_excision`) as the last resort |
| Neurofractured | Cut It Out (`eotg_decision_aug_excision`) |

Excision is no longer shown at Enhanced. An Enhanced character who wants everything out steps down to Augmented first, then takes Remove the Implants. The event routes into end.001 (fracture.026.d, fracture.027, fracture.007.f, end.031.c) are Neurofractured-only already and are unchanged.

Loc (localizer, same ruling): reword `eotg_decision_aug_excision`'s desc and tooltip so the danger and finality are unmistakable. It can kill; everything comes out; it costs major gold. It must read clearly unlike Remove the Implants, the safe tier-1 exit. No numbers, no "odds" or "chance" (index §0, no per-option risk tooltips).

Pictures (*CB-26 L10*, vanilla placeholders accepted): Restraints `decision_prison.dds`, Sedation and Excision `decision_physician.dds`, Appoint a Warden `decision_realm.dds`, Embrace `decision_misc.dds`. Bespoke art is human art debt.

---

## 9. Loc (≈ 270 keys)

**3a:**
- 22 fracture events (.008–.029) at ~6 keys each;
- **[voice]** variants: 4 events × 4;
- picker "no one near" variants;
- Wrong Name dead-name variants;
- Unsent Letter ×3;
- Wrong War ×2;
- False Traitor reveal ×6;
- heir.001 / .003 / .004 (×3 outcomes) / .005.

**3b:**
- 8 end events;
- 5 decisions × 4 keys;
- `trait_eotg_total_integration` + `_desc`;
- `eotg_death_cascade`;
- 3 modifiers × 2;
- 2 opinions.

## 10. Definition of done
0. **Validation, all three clean** on the phase's files, except the known-benign items listed in `CLAUDE.md` §Validation: Tiger 1.17.0 (scratch descriptor), `docs/tools/px_lsp_diagnostics.js` (PX language server, headless) and `docs/tools/px_vocab_check.py` (engine vocabulary + dead hooks). Tiger is the only one of the three that checks scope.
1. The NF on_action has drift → heir story → terminal → band lists, in that order. `fracture.005` is not in any list.
2. No event `trigger` reads `eotg_flag_nf_event_cooldown`, the scramble flag, the last-lucid flag or the terminal flag.
3. `common/story_cycles/` and `common/deathreasons/` exist, with no `replace_path`.
4. Every violent site names its victim. Family factor 0.25 appears only at Storm-band sites, 0.05 elsewhere, 0 where stated.
5. `eotg_aug_raise_warrant_effect` creates a vanilla faction or adds discontent to one. It never references a title.
6. **Human, in game:**
   - Console-set `eotg_fracture_risk` to 10 / 45 / 70 on a Neurofractured count and confirm the pool shifts.
   - A Warrant creates a liberty faction (or adds discontent).
   - A Containment Regency persists for a year (**Q7**).
   - Scrambled visibly swaps a trait.
   - Risk 96 fires The Cascade.
   - Excision can kill or free.
   - Total Integration strips personality and stops episodes.
