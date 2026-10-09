# B7 (countdown, endgame, heir): localizer worklist for the W5 re-gating

Source: `events/eotg_augmentation_countdown.txt`, `events/eotg_augmentation_endgame.txt`, `events/eotg_augmentation_heir.txt`, re-gated under `docs/specs/event_quality_v1.md` §13.1 (2026-10-09, eotg-scripter).
Loc file: `localization/english/eotg_augmentation_l_english.yml`.

Every key below **stays the same**. Only the text changes, so the option reads as its new axis (§13.1 step 7). The effects are unchanged. Apply the §12.1 voice rules (first person, implant-agency verbs, rules 12–14) as for the rest of the B7 W1 pass. Check each new line against **every** desc variant listed (B1 lesson 7).

**W7 boundary.** The desc keys of end.002, end.009, end.010 and heir.005 belong to W7 (`event_quality_w7_set_pieces.md` §5.2), so do not touch them here. heir.005.b's **option** text is in this list, because W5 re-axed it. W7 lists that option as "unchanged", so the W7 pass should read the new gate.

No W6 (portrait) change adds a loc key. heir.005 gains a static lower witness portrait (`scope:eotg_witness`), and no text refers to it. No desc path changed.

## Re-axed options (11)

| Key | Old gate | New gate | Current text | What the new text must convey | Desc variants to check |
|---|---|---|---|---|---|
| `eotg_aug_countdown.001.e` | ambitious | tier ≥ duchy | "Not now. Not when I am this close." | Authority: the realm's business comes before the maintenance table, and the calendar is mine to set. Prestige +50, risk +5. Ambition can stay as subtext ("this close"), but the line should read as the seat-holder deferring maintenance by right. | `.desc` only |
| `eotg_aug_countdown.002.d` | paranoid | education_intrigue | "Someone took them from me." | A spymaster's method: who was near me in the missing days, and who benefits. Naming a suspect and arresting them (imprisonment, risk +8). The suspicion is now an investigation, not fear. The suspect is unnamed in loc, as now. | `.desc` and `.desc_voice` (with the voice line, the model "has those days", so the option must not claim the logs are missing) |
| `eotg_aug_countdown.003.d` | honest | education_diplomacy | "Ask the court which is true." | A diplomat's skill: drawing the evening out of the people who were there without it becoming an interrogation. Prestige −50 for asking at all, risk −6. | `.desc` and `.desc_voice` |
| `eotg_aug_countdown.004.e` | compassionate | education_learning | "Sit with [eotg_victim.GetHerHim] while [eotg_victim.GetSheHe] heals." | A physician's competence: I tend the wound myself (victim opinion +, prestige −25, risk −5). Keep both pronoun calls. Shown only when the victim is alive. | `.desc` only (hidden under `.desc_none`: no victim); `.desc_voice` can append |
| `eotg_aug_end.001.d` | brave | tier ≥ duchy | "Awake. I want to watch them take it out." | Authority: the surgeons work under my eye, at my order. Mechanically, the maimed outcome becomes clean and survival gives +100 prestige. `eotg_aug_end.001.d.tt` already describes this; check that it still matches, without changing the mechanics it names. | `.desc` + every odds line (`desc_odds_grim`, `_poor`, `_fair`), `desc_physician`, `desc_free`, `desc_promised`. Hidden for a landless abdicated ruler (end.031.c path). |
| `eotg_aug_heir.001.e` | paranoid | education_intrigue | "[eotg_heir.GetSheHe\|U] wants your seat." | A spymaster's read of motive: the concern is a move on the seat. Heir fear opinion, story dread +1, risk +5. The current line is second person and should become first person ("my seat"). Not shown to a Seamless owner. | `.desc` and `.desc_overclocked`, each with or without `.desc_patient` (the heir the machine saved as a child: the line should still work) |
| `eotg_aug_heir.003.d` | just | tier ≥ duchy | "Then judge me." | Authority used against oneself: convening a formal hearing on my own fitness (prestige −100, dread −1, risk −3). Same register as tier3.006's inquiry (B3). Not shown to a Seamless owner. | `.desc` and `.desc_successor` (round 2: the second heir has seen this before) |
| `eotg_aug_heir.004.ally_b` | arrogant | tier ≥ duchy | "I did not ask for this." | Authority: the seat did not ask for a keeper, and I refuse one on my own standing (heir unease, risk +5). Shown only on the ally outcome. Not shown to a Seamless owner. | `.desc` or `.desc_successor`, `+ .desc_premonition` (if flagged), `+ .desc_ally`. Not `desc_seamless` (guarded off). |
| `eotg_aug_heir.005.b` | compassionate | education_learning | "It was murder." | A learned judgement: I name the act by what law and faith call it. Stress major gain (unchanged). Root is the heir, after succession. This is a W7 set piece: option text only; the desc is W7's. | `eotg_aug_heir.005.desc` (W7 rewrites it; read against the W7 draft in the addendum §6.5) |
| `eotg_aug_heir.007.e` | paranoid | tier ≥ duchy | "[eotg_heir.GetSheHe\|U] will try what the last one tried." | Authority: I put the new heir under watch by right of the seat (heir fear opinion, dread +2, risk +5). Not shown to a Seamless owner. | `.desc_executed`, `.desc_dead`, `.desc_displaced`. "What the last one tried" must hold in all three; under `desc_displaced` the last one tried nothing lethal. |

## Kept personality gates whose text is unchanged

countdown.001.d diligent, .002.e calm, .003.e stubborn, .004.d sadistic, .005.c humble, .006.b paranoid; end.001.c craven, end.002.c zealous, end.009.c ambitious, end.030.b stubborn; heir.001.d honest, heir.003.e wrathful, heir.004.kill_c vengeful, heir.005.c callous, heir.007.d honest. These keep their gate. Some gained a stress row (end.002.c zealous, end.030.b stubborn, heir.001.d and heir.007.d honest, heir.004.kill_c vengeful, heir.005.c callous), but none needs new text.

## Seamless shipped-text fixes (§13.3, L-1; lore-keeper wording, apply as given)

These keys carry first person or "you" in a Seamless event, which breaks the no-first-person register (§12.1 rule 7). Fit each phrase into the existing sentence without adding beats. Each residue line still ends logged, filed or pruned (procedures_lore ruling (a)).

| Key | Current text | Change |
|---|---|---|
| `eotg_aug_heir.004.desc_seamless` | "\n\nThey address the chair, not you. They have understood there is no difference left to make." | Replace with: "\n\nThey address the chair. There is no one else in it to address." This supersedes procedures_lore N5. |
| `eotg_aug_end.041.desc_residue_high` | "...your head tilts the way it used to when you were listening. ..." | Becomes "...the head tilts the way it once did for listening." Keep the resigner's reaction, and end the line logged, filed or pruned. |
| `eotg_aug_end.041.desc_residue_low` | "...Nothing in your face has moved, ..." | Becomes "Nothing in the face at the head of the table has moved." Keep the resigner's half, and end logged, filed or pruned. |
| `eotg_aug_end.011.desc`, `eotg_aug_end.011.desc_named` | "...the quiet in your [ROOT.Char.Custom('eotg_court_seat')]..." | The root reference becomes "the [court seat]": `the [ROOT.Char.Custom('eotg_court_seat')]` (dynamic term, per the dynamic-terms ruling). |
| `eotg_aug_end.011.desc_none` | "...They watch you the way people watch a machine..." | The "you" becomes "...watch the chair." |

Rule 7 keeps the court's speech able to say "you" inside quotes. These are narration, so the fix applies.
