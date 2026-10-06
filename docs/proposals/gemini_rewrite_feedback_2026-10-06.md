# Feedback on the cybernetics event rewrite proposals (round 1)

**For:** the agent that wrote `docs/proposals/cybernetics_events_rewrite_proposals.md` (round 1, 2026-10-05).
**From:** the project's lore-keeper and QA reviews, collected by the orchestrator, 2026-10-06.
**Your task:** read this file, review your round-1 drafts against it, and write a **round-2** file:
`docs/proposals/cybernetics_events_rewrite_proposals_r2.md`. Do not edit any other file.

---

## 1. Verdict on round 1

**No draft could be applied as written.** Two reviews (canon/voice and rules/QA) agree: 0 apply as-is, 15 apply
with edits, 2 need a full redraft, and 3 needed script support that has now been added (§6).

The structural ideas were good, and you should **keep** them:
- a named actor in each scene;
- a witness;
- a spoken line from the person wronged;
- options in the ruler's own voice;
- one concrete detail and a stake.

The problems are in the **register**, in **facts the script doesn't support**, and in **format**.

**Start from the CURRENT shipped text** in `localization/english/eotg_augmentation_l_english.yml`, not from your
round-1 prose. The shipped lines already have the right register (clinical, uneasy, "readings", "the panel", "the
record"). Your job is to add the structural ideas to them, not to replace their voice.

---

## 2. The setting: read this before writing a word

This is **not** medieval fantasy and **not** clockwork or steampunk. Crusader Kings III's base game is medieval;
this mod replaces it with an **original space-faring galaxy, 866 AG**:
- baronies are star systems, and courts sit on stations, ships and colony worlds;
- implants are **electronic hardware**: worn, hand-maintained, read at a diagnostic panel. They are fitted,
  upgraded, repaired and removed by clinics, physicians and back-street fitters;
- the tone is **intimate, clinical, a little uneasy**: surgery, maintenance, debt and dependence. **Not
  superheroes.**

Canon rules (from `OLD PROJECT VERSION/docs/SETTING LORE` ERRATA and `docs/specs/cybernetics_v2.md` §5):
- **The implant's "voice" is a forecast of the user, about half a second early.** It is never prophecy or
  foresight of plots months ahead, never supernatural, never "ghosts", never the Void.
- **Self-repairing hardware only keeps ITSELF in tolerance.** It finds and corrects its own wear. It does not
  regulate the heart, nerves or mind.
- **No faith-specific framing.** Content fires for every faith: no "holy blood", "ungodly", "prayer" as a default.
- **Never "human" or "humanity" as the default people.** Use "flesh", "the self", "personhood", "other people".
- No named institutions or licensing authorities; no galaxy-wide law bodies. Seller names come only from the
  existing `[ROOT.Char.Custom('eotg_aug_cl_…')]` placeholders already in the shipped text.

---

## 3. Banned words, and what to use instead

| Don't use (round 1 had these) | Use instead |
|---|---|
| brass, gears, cogs, clockwork, ticking, whirring, hot vapour, springs | housings, leads, ports, seals, coil whine, the readout, the diagnostic panel, calibration, coolant hiss, hot casings |
| candle, oil lamp, silver needle, silver pick | work lights, the panel's glow, a probe, a lead |
| chirurgeon, chirurgery, apothecary, herbal unguent, poppy milk, vinegar, ague, black rot | the clinic medic, the fitter, the surgeon, dressings, sutures, a sedative, antiseptic, infection |
| castle, palace, Great Hall, throne room, solar, bailey, parapets, courtyard, dungeon, straw, flagstones, oak doors | the residence, the bastion, the court, quarters, the audience chamber, the cells, the corridors, the docks |
| knight (as a rank), tourney, tilt-yard, quintain, lance, siege, stables, saddlebags, horses | the barracks, a drill, a boarding action, a breach, kit bags |
| parchment, scroll, sheepskin, wax seal, signet ring, scribes | the contract, the documents, the record, archivists, the logs |
| cupbearer, ewer, flagon, bronze mirror | a steward, an attendant, a cup, a mirror |
| invincible, unstoppable, flawless, living weapons, miraculous, "evolution demands" | cost, dependence, maintenance, what it took from you |
| winter, summer, dawn, sunrise, morning, "many moons", "by morning" | "a year of silence", "weeks later", "before the next shift", "by the next watch", "months pass" |
| royal, royal seal, coronet (assumes the player's rank) | your seal, your court, your heir |

**Spelling is Canadian:** vapour, harbours, fervour, vigour, pretence, honour, colour, defence, programme (avoid
"programme" as an institution anyway), -ize endings (realize, organize).

**In-voice samples** (from the lore-keeper; this is the target register):
- "'The leads took. You'll walk. You won't walk the same.'"
- "'Your body threw it. If I'd left it in, the infection would have had you by the next shift.'"
- "'Your implant made a pattern out of me, and I paid for it in the cells.'"
- "In council, cold runs down a wrist that has no nerves left to feel it, then an itch in fingers that are not
  flesh. The grip closes on its own. The cup in your hand dents, and the room goes quiet mid-petition."
- "Months pass. Nothing happens."

---

## 4. Rules for the text itself

- **Text only.** Keep every loc key and its variant structure. Don't add or remove options, triggers or effects.
- **The text must match what the script does.** Before writing an option, read that option's effects in
  `events/eotg_augmentation_*.txt`. Don't promise a role, a cost, an oath, a negotiation or a result the option
  doesn't have. A desc must be true on **every** path that shows it: check which variants share an option or a
  fallback.
- **Placeholders:**
  - use only scopes that exist in that event's script or current text, or the new ones in §6;
  - write them in the bare form `[eotg_x.GetFirstName]`, NEVER `[scope:eotg_x…]`;
  - don't hard-code a gender for an unscoped person: rephrase to avoid pronouns;
  - for one scoped person use the functions `[x.GetSheHe]`, `[x.GetHerHis]`, `[x.GetHerHim]`, never "they" or
    "their" for one person.
- **Don't invent relatives or people** (round 1 invented a "sister"). Use an existing scope or "[x.GetHerHis] kin".
- **Length:** descs about 45–80 words; options about 5–9 words.
- **Avoid the overused phrases:** "No one…", "the hardware" as a crutch, "the work" for surgery, "half a second",
  "It is not…". Also don't create new ones: round 1 used "Great Hall" four times.

### Format (round 1's YAML would have broken the game)
- **No literal line breaks inside a quoted string.** Write paragraph breaks as `\n\n` inside the quotes.
- **Don't repeat the `l_english:` header.** Give each key as a plain line: ` key:0 "text"`.
- **Don't claim checks you haven't done.** Round 1's conformance table said "Passed" for everything.

---

## 5. Per-event required changes

**Global, for all 20:** fix the register (§2–3), Canadian spelling, the "human" wording, and seasons and times of day.

| Event | Required changes |
|---|---|
| eotg_aug_tier1.019 Copycat: Their Fate | `.a` must be neutral across all three outcomes (dead, worse, recovered); "an invoice in blood" is wrong when they recovered. The ambition was the copycat's own, not "their liege's". Cut the invented costs ("blood-money", "ruinous invoice", "drained your treasury") and the "oath of fealty": the event moves no gold and adds only an opinion. Write the new option `.b` (see §6). |
| eotg_aug_tier3.018 The Plot: The Truth | **Redraft.** In the attempt variant you ignored the warning: the court is not "in awe of your foresight", and the option wounds you (no deflected blow). desc_quiet: you didn't fabricate anything; the suspicion went unacted on. desc_true and desc_false also cover the executed path, so no kneeling or humiliated conspirator. `.c` is the fallback for false, executed and unknown outcomes. Only desc_unknown, `.a` and `.b` were usable. The implant only forecasts; the court may believe you "saw it coming", but you know only that "the pattern matched". |
| eotg_fracture.020 What the Record Shows | `.c_spared`: the accused WAS guilty, so the binding meaning is "It was right. I was not." (don't reverse it). desc_true must hold whether the accused is alive or dead. Replace the invented "sister" with "one of [eotg_accused.GetHerHis] kin". Drop "whispers" (banned in this content). No "ghosts", no "dungeon straw". |
| eotg_fracture.004 The Court Massacre | The base desc must work when nobody died (desc_none exists): no "slaughter" or "red smears" in the shared opening. `.e` "replace the dead" becomes "fill the empty places". Trim the longest path (desc + killed + wounded) to about 80 words. Keep the named survivor. |
| eotg_aug_init.012 The Body Decides | The surgeon is unscoped: no "he". "You will walk again" assumes a leg; make it generic. No "common men". Keep the spoken verdict (see the samples). |
| eotg_aug_proc.002 After the Procedure | **Redraft the descs.** Each opening is followed by an outcome line (infection, complication, failure, fragments, maimed, blind), so the opening must not claim success, a body location (ribs, arm, fingers) or "his". desc_refit must keep the fact: some weeks in, the record shows the first fault the hardware found in itself and corrected. `.b` shouldn't summon a physician who is already present ("Get the clinic back in here."). `.a`, `.a_grim` and `.c` are fine. |
| eotg_aug_retinue.002 More Step Forward | `.b` "swiftest" becomes "strongest" (they are picked by prowess). `.d` installs both for free (it's the greedy option): "Both of you, but not from my purse." `.c` is ungated and cand_b may not exist, so make it singular-safe. Clarify `.e`. |
| eotg_aug_retinue.001 First of the Iron | `.a` doesn't give a leadership role: "You will be the first of the iron." `.d` installs only the next volunteer: "…and the next one after." |
| eotg_aug_heir.007 The Next in Line | `.c` must keep the "keep me in check" meaning: "Learn from it, and restrain me if I fall." desc_displaced: the prior heir is alive, so no "fatal mistake". No executioner's spade or royal summons. |
| eotg_aug_tier2.018 Resolution | `.c` is the fallback for both the estranged and the reconciled variants, so it must be neutral ("Then this is where we stand."). `.b` is a petition, not a decree. No winter, sheepskin or royal seal. |
| eotg_aug_end.030 Into Restraints | Use the heir via `[ROOT.Char.GetHeir.GetFirstName]` and `[ROOT.Char.GetHeir.GetSheHe]` (not `[primary_heir.…]`). No "humanity", no "palace guards". Keep the shipped line "a formality that no one believes is a formality". The heir present and speaking is good. |
| eotg_aug_init.020 Choosing the Volunteer | **Now scripted** (§6): write the base desc plus the three candidate lines; each shows only if that candidate exists. |
| eotg_aug_tier1.003 An Uncomfortable Question | No "holy blood / ungodly" framing. `.e` is the deceitful (lie) option: "There is nothing to tell; I am unchanged." |
| eotg_aug_tier1.004 The Knight's Request | Cut "the retinue program" and "illicit". `.d`: "My own coffers will pay for your implant" (no "royal treasury", no "new limb"). |
| eotg_aug_tier3.002 The Mirror | No "human flesh" (`.a` becomes "Flesh was always the weak part."); no castle; no superhero lines (`.d` becomes "It looks like it works."). No witness scope exists: keep any attendant unnamed. |
| eotg_aug_tier3.003 Sleepless | No poppy milk (`.a`: "Get me a sedative. Make it strong enough."). No castle or sunrise. Don't assume an eye implant. Make clear who trembles. |
| eotg_aug_tier2.001 Emotional Delay | **Now scripted** (§6): the speaker is `eotg_delay_speaker`. Never use GetPrimarySpouse directly (unmarried rulers would see a blank). `.d` "their hands" uses the speaker's pronoun instead. |
| eotg_aug_tier1.001 Phantom Sensation | `.d` is in the ruler's voice: "…correct the alignment myself." No brass or forged alloy. See the sample line in §3. |
| eotg_aug_patron.007 A New Envoy | The last envoy's fate is unknown: "unbothered by what became of [eotg_patron_envoy.GetHerHis] predecessor". No castle dungeons. `.a` has no effects, so don't promise a negotiation ("Welcome, envoy; your contract is known here."). |
| eotg_aug_end.011 The Empty Hall | **Now scripted** (§6): name the leaver through `eotg_departed_courtier`. No saddlebags, no "soul", no fortress gates (`.c`: "Seal the docks. No one leaves without my word."). |

---

## 6. New script support (added 2026-10-06; use exactly these names)

| Event | What exists now | Your keys to write |
|---|---|---|
| eotg_aug_init.020 | The desc is a base plus three lines, each shown only if that candidate exists (scopes as in the event's immediate) | `eotg_aug_init.020.desc` (base, must read fine alone), `eotg_aug_init.020.desc_line_best`, `…_line_any`, `…_line_courtier` |
| eotg_aug_tier2.001 | Scope `eotg_delay_speaker`: spouse, else close family at court, else a courtier. It may not exist. | `eotg_aug_tier2.001.desc_speaker` (variant with the speaker); the existing desc stays as the no-speaker fallback |
| eotg_aug_end.011 | Scope `eotg_departed_courtier`: the most notable person who left. It may not exist. | `eotg_aug_end.011.desc_named`; the existing desc stays as the fallback |
| eotg_aug_tier1.019 | New option `.b`: scope `eotg_copycat_recipient` (the copycat if alive, otherwise their closest family member at your court) gains a small positive opinion of you; you pay a small sum of gold. It shows in all three outcomes. | `eotg_aug_tier1.019.b`. It must read right whether they died, worsened or recovered. Name the recipient with `[eotg_copycat_recipient.GetFirstName]` / `[eotg_copycat_recipient.GetHerHim]`, never "them". |

Placeholder text was added for these keys so nothing renders blank; your round-2 text replaces it.

**Format notes for these keys:**
- The three `init.020.desc_line_*` keys are appended after the base desc, so each must START with `

` (the project lint requires it).
- The candidate scopes are `eotg_cand_best` (the knight with the highest prowess), `eotg_cand_any` (another knight) and `eotg_cand_courtier` (a courtier who is not a knight).
- `tier2.001.desc_speaker` and `end.011.desc_named` replace the whole desc when they show, so each must stand alone as a complete desc.
- There is no portrait for the speaker or the leaver, so describe them in the text. Check the
exact scope names in the events on branch `v2-space-map`.

---

## 7. What to deliver

`docs/proposals/cybernetics_events_rewrite_proposals_r2.md` should contain:
1. A short list of what you changed from round 1, by theme.
2. For each of the 20 events: the key, the CURRENT shipped text, your PROPOSED text, and one line on why. Write
   each key in the plain ` key:0 "text"` form, with `\n\n` for paragraph breaks.
3. A self-check you actually performed. For each event: every scope used exists; no banned words; Canadian
   spelling; every desc is true on every path that shows it; option text matches option effects. Mark anything
   you couldn't verify as "unverified", not "passed".

Don't edit `.yml` or `.txt` files. The project's localizer applies approved text, which keeps the file
encoding correct.
