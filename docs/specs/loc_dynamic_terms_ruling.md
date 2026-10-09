# Ruling: hard-coded loc terms that should be dynamic

**Status:** FINAL (Round 2, 2026-10-08). The lore-keeper's answers are recorded in §2, and no item is still pending.
**Input:** `docs/qa/loc_dynamic_terms_audit_2026-10-08.md` (the "audit"). Match keys by key, not by line number.
**Gate:** this is loc hygiene on mod-exclusive systems (cybernetics, frontier). It is exempt from the Gate 1 block (`CLAUDE.md`, 2026-10-02) and touches no title, province, culture or faith key.
**Ownership:**
- The cybernetics files (`localization/english/eotg_augmentation_l_english.yml`, `events/eotg_augmentation_*`, `common/*/eotg_augmentation_*`) belong to the Cybernetics Modding session.
- The frontier files belong to whoever holds frontier.
- Both are routed through the orchestrator. Nothing here is applied, and nothing is committed.

## 0. Corrections to the audit (verified in script)

Five premises in the audit are wrong. The rulings below rest on what the script does.

1. **`eotg_champion` in `eotg_aug_nr.*` is not always a knight** (audit 1.1). `eotg_on_yearly_aug_nonruler_check` (`common/on_action/eotg_augmentation_on_actions.txt`) saves the scope on any augmented non-ruler employed by a count+ liege. `eotg_aug_is_retinue_knight` is only a ×1.5 weight there.
   - nr.001 and nr.002 require `is_knight = yes`.
   - nr.003, nr.004 and nr.006 (the latter via `eotg_aug_nr_cascade_effect`) take knights or courtiers.
   - **nr.005 requires `is_knight = no`.**
   - So the knight term is correct only in nr.001 and nr.002.
   - In tier1.016 the champion does come from `ordered_knight` (`events/eotg_augmentation_tier1.txt:2031-2038`, saved in `immediate`), so the knight term is correct there.
2. **The seven "My own physician." event options are already dynamic** (audit 1.3). Each has a triggered `name = { trigger = { eotg_aug_surgeon_is_technician = yes } text = eotg_aug_opt_technician }` ("My implant technician."):
   - `procedures.txt:148-155, 588-596, 973-979`
   - `tier1.txt:345`, `tier2.txt:528`, `tamper.txt:367`, `initiation.txt:2767`
   - Vanilla uses the same plain-then-triggered `name` shape (`events/activities/coronation_activity/coronation_events_klank.txt:1372-1375`).

   The plain text appears only when the surgeon is the court physician. Every one of these options requires `eotg_aug_has_surgeon_for = { PATIENT = root }`, whose final branch (`this != $PATIENT$`) rules out the ruler operating on themself. So the plain label never misnames anyone.
3. **`Custom('CouncilPosition')` does not follow government flavour** (audit 1.2). In vanilla `common/customizable_localization/00_councillor_custom_loc.txt:1-100` it branches only on the Celestial ministry titles, and otherwise returns the fixed keys `councillor_spymaster` etc. The council position's own `name` desc is the one that varies, for example by `government_has_merit` (`common/council_positions/00_council_positions.txt:417-440`). Its loc accessor is `GetCouncillorPosition( '…' ).GetPositionName`, used in vanilla at `localization/english/event_localization/court_events/court_events_george_l_english.yml:6` ("my [ROOT.Char.GetCouncillorPosition( 'councillor_steward' ).GetPositionName]"). This ruling uses that form, with vanilla's capitalization (no `|l`).
4. **The 3.1 citation is a comment.** `eotg_augmentation_decisions.txt:915` is a comment. The 5-year flag is set at:
   - `common/on_action/eotg_augmentation_on_actions.txt:451`
   - `common/scripted_effects/eotg_augmentation_effects.txt:134`
   - `common/scripted_effects/eotg_augmentation_effects.txt:161`
5. **The augmentation events fire on `yearly_playable_pulse`** (`on_actions.txt:84-97`), which includes landless playable characters. `GetCapitalLocation` is unsafe in an unconditional desc there (see 2.2).

**Audit ruling item 5 (council-seat flavour in governments v2):** none is planned.
- `docs/specs/governments_v2.md` §15 defers "Government-specific … council positions" to G2 P3.
- §14 P3 lists only a *new* seat (the PMC Logistics Officer), not renames of the vanilla five.
- 1.2 is still approved: vanilla's seat names already vary (merit governments, theocratic chaplain), and any later rename through the council position's `name` flows through `GetPositionName` at no extra cost. Its value is lower, as the audit said.

**Knight-term article check:** no current or approved string puts "a"/"an" before a `KnightCulture` call. Checked with `grep -rnE "\b[Aa]n? \[[^]]*KnightCulture" localization/`, which returns nothing. Every approved string below uses "the", "your", "my best" or a plural. This matters: the CB-48 override (`common/customizable_localization/eotg_knight_culture.txt`) has "Operator" as a term, which would need "an".

---

## 1. Verdicts

Legend:
- **A** = APPROVED as the audit proposed
- **AWC** = APPROVED-WITH-CHANGE (the final text is in §3)
- **R** = REJECTED
- **PL** = PENDING-LORE
- **NS** = NEEDS-SCRIPT

### 1.1 Champion / knight term
| Key | Verdict | Reason |
|---|---|---|
| `eotg_aug_tier1.016.c` | AWC | A specific knight is sent (`eotg_champion`, saved in `immediate`). Name them and keep the role through the knight term, with no article. |
| `eotg_aug_tier1.016.c.success` | A | The scope exists when the duel desc renders. |
| `eotg_aug_tier1.016.c.failure` | A | Same. |
| `eotg_aug_nr.001.t` | A | nr.001 is knight-gated (`is_knight = yes`, step 1). Lore confirms tone in Q1. |
| `eotg_aug_nr.002.t` | AWC | Knight-gated (step 2 `is_knight = yes`). Use the knight term, not the name: the title should keep the role. |
| `eotg_aug_nr.004.t` | AWC | The champion may be a courtier, so the knight term would be false. Use the name. `GetFirstNameNoTooltip` in titles: vanilla `activities/journey_activity_l_english.yml:442`. |
| `eotg_aug_nr.004.desc` | AWC | Name instead of "the champion", rephrased so the pronoun does not repeat. |
| `eotg_aug_nr.005.t` | AWC | nr.005 requires `is_knight = no`, so the knight term is wrong by construction. Use the design name already in the event file header (`events/eotg_augmentation_nonruler.txt:9`, "The Familiar Change"). |
| `eotg_aug_nr.006.t` | AWC | The cascade hits knights or courtiers. A neutral title that reads the signature resource: "What the Cascade Left". |
| Loc comment lines `# eotg_aug_nr.001/.002/.004/.005/.006 …` | AWC | Keep the comments in step with the titles (localizer). |

### 1.2 Council seats
| Key | Verdict | Reason |
|---|---|---|
| `eotg_aug_tier2.012.desc` | AWC | `eotg_flagged` = `cp:councillor_spymaster` of root (`tier2.txt:1646`). Use `GetPositionName`, not `Custom('CouncilPosition')` (§0.3). |
| `eotg_aug_tier2.012.c` *(not in the audit)* | AWC | "Spymasters keep odd hours." hard-codes the seat in a plural. Rephrase without the seat word. |
| `eotg_aug_end.020.c` | AWC | `eotg_warden_chancellor` = `cp:councillor_chancellor` of root (`endgame.txt:632`). Use `GetPositionName`. |
| `eotg_aug_tier2.011.c` | AWC | The option requires `cp:councillor_steward` (`tier2.txt:1522-1527`). Use `GetPositionName`. |
| `eotg_aug_tier2.011.c.success` | AWC | Same. |
| `eotg_aug_tier2.011.c.failure` | AWC | Same. |
| `eotg_mod_aug_optimised_levies_trimmed_desc` | AWC | No reliable ROOT in a modifier desc. The audit's "Your treasury cut…" is wrong (a treasury does not cut), so use passive voice. |
| `eotg_aug_act.002.e` | AWC | "The marshal" is the tournament official, not the council seat. No scope is saved, so rephrase to remove the seat word. No script needed. |

### 1.3 Physician vs. implant technician: **option (a)**, scoped
| Key | Verdict | Reason |
|---|---|---|
| `eotg_aug_proc.001.b`, `eotg_aug_proc.003.b`, `eotg_aug_proc.005.b`, `eotg_aug_tier1.002.f`, `eotg_aug_tier2.003.f`, `eotg_aug_tamper.004.b`, `eotg_aug_init.018.c` | R | Already dynamic (§0.2). The plain text renders only when the surgeon is the court physician, so it is true. |
| `eotg_aug_send_physician` | AWC | Interaction send option. `localization` takes a static key (`_character_interactions.info:329-330`). The surgeon may be the actor's technician, a borrowed technician, the court physician, or the actor themself (`eotg_aug_save_surgeon_effect`, `eotg_augmentation_effects.txt:1910-1926`). Use generic wording. |
| `eotg_aug_send_physician_tt` | AWC | Same. |
| `eotg_aug_send_salvage_physician_tt` | AWC | Same. |
| `eotg_aug_send_physician_valid_tt` | R | Already accurate ("a physician or implant technician"). |
| `eotg_aug_proc.001.desc_physician` | AWC | Gated on `eotg_aug_has_surgeon_for`, which includes technicians. Use generic wording in the shape of `eotg_aug_proc.005.desc_surgeon`. |
| `eotg_aug_proc.003.desc_physician` | AWC | Same. |
| `eotg_aug_end.001.desc_physician` | AWC | Stays "physician": it is gated on `eotg_has_physician_access` (a court physician **or** the ruler's own `lifestyle_physician`), never on a technician. But "Your physician … stays at the table" is false when the ruler is the physician and also the patient. Reword so it holds in both cases. |

**Keys that keep "physician"**, because the script requires a court physician or physician access:
- `eotg_aug_init.017.*`: `scope:eotg_physician` is the court physician or root (`initiation.txt:775, 2466-2492`), and `desc_self` covers root.
- `eotg_aug_end.001.desc_physician`, with the reworded text in §3.
- `eotg_aug_init.013.desc`: "[parent]'s physician" is flavour with no mechanic attached.
- All seven option keys above, in their plain (court-physician) form.

`eotg_aug_inherit.010.desc_physician` already says "surgeon" and needs no change.

### 2.1 Name the character
| Key | Verdict | Reason |
|---|---|---|
| `eotg_aug_init.005.desc` | AWC | Name `eotg_aug_peer` (a vassal or courtier saved in `immediate`). Lore Q2 overruled "the capital": the final first sentence names the clinic (row 2.2). |
| `eotg_aug_tier2.004.desc` | A | `eotg_aug_spouse` comes from `random_spouse` in `immediate`, and the event requires `is_married`. `GetWifeHusband`: vanilla `bookmark/bookmark_china_1066_l_english.yml:30`. |
| `eotg_aug_end.020.a` | A | `eotg_warden_spouse` = `primary_spouse`. |
| `eotg_fracture.005.desc` | AWC | Keep the role and add the name, so the heir relationship still reads. |
| `eotg_aug_init.013.t` | AWC | `eotg_dead_parent` is always a parent (`every_child` → `var:eotg_parent_hardware`, `on_actions.txt:470-475`). Needs `\|U` in a title (vanilla `[ROOT.Char.GetMotherFather\|U]`, 29 uses). |
| `eotg_fracture.026.b` | NS | No heir scope is saved. The option already requires `exists = primary_heir`. Spec below. |
| `eotg_aug_tier2.006.desc` | R | No dead advisor exists in script. Naming one means a new on_death trigger, which is new event design and so the user's call (memory: event expansion). Moved to §5. |

**NS spec: `eotg_fracture.026.b`**
- **File:** `events/eotg_augmentation_fracture.txt`, event `eotg_fracture.026`, inside the existing `immediate = { hidden_effect = { … } }`, after the keeper block (around :4262-4276).
- **Add:** `primary_heir ?= { save_scope_as = eotg_lucid_heir }`
- **Shape:** `eotg_aug_end.020`'s `primary_heir = { save_scope_as = eotg_warden_heir }` (`events/eotg_augmentation_endgame.txt:622`). The `?=` guard is the mod's own pattern at `fracture.txt:4266/4272`.
- **New identifier:** `eotg_lucid_heir` (saved scope). It is unused anywhere in the tree (grep clean).
- **The option's trigger stays as it is.** `exists = primary_heir` is the world-state guard. This is not a cooldown, so lesson 5 is not touched.
- **Loc, after the script lands:** `eotg_fracture.026.b` → `"Beg [eotg_lucid_heir.GetFirstName] to act."`

### 2.2 The capital by name
| Key | Verdict | Reason |
|---|---|---|
| `eotg_aug_init.003.desc` | AWC | Lore Q2: never name the capital. A zero-script rewording drops "the capital", which fits landless rulers too (Exodus fleets; the event runs on `yearly_playable_pulse`). |
| `eotg_aug_tier1.002.desc` | AWC | Same Q2 ruling: "has arrived in the capital" becomes "has come in". |
| `eotg_aug_init.005.desc` (the capital) | AWC | Lore Q2 overrule. The peer is the player's own vassal or courtier, and canon has no central clinic city (ERRATA "CYBERNETICS AT 866"). The install is `PROVIDER = clinic`, so the sentence names a clinic. This is merged into the 2.1 row for the same key. |
| `eotg_aug_init.005.t` | AWC | Lore Q2: "Back From the Capital" becomes "Back From the Clinic". |
| `eotg_aug_tier3.023.e` | R | An option label reads better generic (the audit agrees). |

### 2.3 Faith words
| Key | Verdict | Reason |
|---|---|---|
| `eotg_fracture.026.e` | AWC | Lore Q3 confirmed `PriestNeuterPlural` (vanilla 47 uses, `custom_localization/divinity_custom_loc_l_english.yml:52`) but overruled the verb. "Confess" is sacramental, and several canon faiths are non-theistic. Final: "Lay it all before the [ROOT.Char.GetFaith.PriestNeuterPlural]." The event-file comment changes to match (§3.2). |
| `eotg_aug_tier2.005.d` | R | "The faith has no say over my body." is true for any faith and stronger as written. Naming the faith adds nothing (lore Q3 confirmed). |
| `eotg_frontier.041.desc_order` | R | "a holy order of your faith" is already correct and generic. |
| `eotg_aug_act.006.t` | R | "Holy site" is a game concept (the audit agrees). |
| Prayer lines, "Bless the glass", rites | R | Vanilla has no dynamic prayer verb (the audit agrees). |

The faith-term dependency this creates is in §6 (religion-port follow-ups).

### 3. Consistency
| Item | Verdict | Reason |
|---|---|---|
| 3.1 "five years" / "5 years" | A (keep and comment) | Correct today. Vanilla also writes durations into text. Add sync comments beside the script values (scripter). The tooltip stays explicit. |
| 3.2 "Realm" | R | `GetRealmOrDomicile` differs only for domicile governments, and no player runs the Unclaimed placeholder. |

### Counts
Counts are per key, as in the tables above (the seven option keys count as 7, and the prayer-line group as 1).

| Verdict | Count | Keys |
|---|---|---|
| APPROVED | 6 | tier1.016.c.success, tier1.016.c.failure, nr.001.t, tier2.004.desc, end.020.a, 3.1 |
| APPROVED-WITH-CHANGE | 27 + the loc comment lines | tier1.016.c, nr.002.t, nr.004.t, nr.004.desc, nr.005.t, nr.006.t; tier2.012.desc, tier2.012.c, end.020.c, tier2.011.c, .c.success, .c.failure, the modifier desc, act.002.e; send_physician, send_physician_tt, send_salvage_physician_tt, proc.001.desc_physician, proc.003.desc_physician, end.001.desc_physician; init.005.desc, init.005.t, fracture.005.desc, init.013.t; init.003.desc, tier1.002.desc; fracture.026.e |
| NEEDS-SCRIPT | 1 | fracture.026.b |
| PENDING-LORE | 0 | — |
| REJECTED | 15 | the 7 options, send_physician_valid_tt, tier2.006.desc, tier3.023.e, tier2.005.d, frontier.041.desc_order, act.006.t, prayer lines, 3.2 |

---

## 2. Lore-keeper answers (resolved, Round 2)

All three questions are closed. The original questions are summarized with each answer.

1. **Knight-term titles (1.1): CONFIRMED, all five as written.** That is nr.001 "The [knight term] Volunteers", nr.002 "Your [knight term]'s New Edge", nr.004 "[Name]'s Mistake", nr.005 "The Familiar Change" and nr.006 "What the Cascade Left".
   - "Champion" does not survive as a rank. In canon it means a divine or Titanic sponsor's man (SETTING LORE:328, :798; Third era files FE:870, :901), or the post-866 P&D "Company Champions" (NA:3972-3975).
   - `common/customizable_localization/eotg_knight_culture.txt:17` already drops vanilla's Champion term. It stays dropped.
   - "Cascade" is the system's own word ("died in a neural cascade", fracture.027).
   - The CB-48 terms are **ruled**, not pending: Operator / Specialist / Strongarm / Brute (`governments_v2.md:506, :681`).
2. **The capital (2.2): CONFIRMED generic, but reworded; init.005 OVERRULED.**
   - "The capital" as a common noun is in voice for 866 (NA:1343, :1648, :2876; SETTING LORE:545).
   - Never name a world or station. The System name adds nothing.
   - init.003 and tier1.002 get a zero-script rewording that drops "the capital", so it also reads right for landless rulers (Exodus fleets; REVIEW_866:31; NA:1442-1447).
   - init.005 is overruled. The peer is the player's own vassal or courtier (`initiation.txt:563-575`), so "returned from the capital" contradicts itself. Canon has no central clinic city (ERRATA "CYBERNETICS AT 866", :60-62), and the install is `PROVIDER = clinic` (:588). The title and first sentence name a clinic.
3. **Clergy (2.3): mechanism CONFIRMED, verb OVERRULED.**
   - `PriestNeuterPlural` stands. Canon office-holders include Plutocracy "assessors" (`866_religions:168`), Ancestor Veneration "Name-Keepers" (:205) and Deep Warren "Deepkeepers" (:222).
   - "Confess" is sacramental, and several faiths are non-theistic: Survivalism :228-233, Secular Codes :235-245, Plutocracy :160-169. This is the same class of problem as the invocation ban in `cybernetics_v2.md` §5.4.
   - Final text: "Lay it all before the [ROOT.Char.GetFaith.PriestNeuterPlural]."
   - `tier2.005.d` naming the faith: CONFIRMED no.
   - Lore found nothing else in §3.1 that contradicts canon or the 866 voice.

---

## 3. Work order (APPROVED and APPROVED-WITH-CHANGE only)

Apply only what is listed here. No item is pending; everything below is final.

### 3.1 Localizer: `localization/english/eotg_augmentation_l_english.yml` (cybernetics session, via the orchestrator)
Keep UTF-8 with BOM. Each line keeps its `:0` version. The old text is quoted exactly. New text goes inside the quotes as written, and `\n\n` is literal.

| Key | Old | New |
|---|---|---|
| `eotg_aug_tier1.016.c` | `Send my champion.` | `Send [eotg_champion.GetFirstName], my best [ROOT.Char.Custom('KnightCultureNoTooltipLowercase')].` |
| `eotg_aug_tier1.016.c.success` | `Your champion wins the bout.` | `[eotg_champion.GetFirstName] wins the bout for you.` |
| `eotg_aug_tier1.016.c.failure` | `Your champion loses the bout.` | `[eotg_champion.GetFirstName] loses the bout.` |
| `eotg_aug_nr.001.t` | `The Champion Volunteers` | `The [ROOT.Char.Custom('KnightCultureNoTooltip')] Volunteers` |
| `eotg_aug_nr.002.t` | `Your Champion's New Edge` | `Your [ROOT.Char.Custom('KnightCultureNoTooltip')]'s New Edge` |
| `eotg_aug_nr.004.t` | `The Champion's Mistake` | `[eotg_champion.GetFirstNameNoTooltip]'s Mistake` |
| `eotg_aug_nr.004.desc` | `[eotg_victim.GetFirstName] is hurt, and [eotg_champion.GetFirstName] is the reason. The champion did not mean it. [eotg_champion.GetSheHe\|U] is sure of that, and so is everyone who saw it, and nobody is sure what the champion would have meant if [eotg_champion.GetSheHe] had been given the time to mean anything.` | `[eotg_victim.GetFirstName] is hurt, and [eotg_champion.GetFirstName] is the reason. It was not meant. [eotg_champion.GetSheHe\|U] is sure of that, and so is everyone who saw it, and nobody is sure what [eotg_champion.GetFirstName] would have meant if [eotg_champion.GetSheHe] had been given the time to mean anything.` |
| `eotg_aug_nr.005.t` | `A Changed Champion` | `The Familiar Change` |
| `eotg_aug_nr.006.t` | `The Broken Champion` | `What the Cascade Left` |
| comment above nr.001 | `# eotg_aug_nr.001 The Champion Volunteers` | `# eotg_aug_nr.001 The Knight Volunteers (knight term)` |
| comment above nr.002 | `# eotg_aug_nr.002 Your Champion's New Edge` | `# eotg_aug_nr.002 Your Knight's New Edge (knight term)` |
| comment above nr.004 | `# eotg_aug_nr.004 The Champion's Mistake` | `# eotg_aug_nr.004 [Name]'s Mistake` |
| comment above nr.005 | `# eotg_aug_nr.005 A Changed Champion` | `# eotg_aug_nr.005 The Familiar Change` |
| comment above nr.006 | `# eotg_aug_nr.006 The Broken Champion` | `# eotg_aug_nr.006 What the Cascade Left` |
| `eotg_aug_tier2.012.desc` | `Your spymaster, [eotg_flagged.GetFirstName], is flagged.` *(first sentence only; the rest is unchanged)* | `Your [ROOT.Char.GetCouncillorPosition( 'councillor_spymaster' ).GetPositionName], [eotg_flagged.GetFirstName], is flagged.` |
| `eotg_aug_tier2.012.c` | `Spymasters keep odd hours. Leave it.` | `Odd hours come with the seat. Leave it.` |
| `eotg_aug_end.020.c` | `[eotg_warden_chancellor.GetFirstNameNoTooltip], your chancellor.` | `[eotg_warden_chancellor.GetFirstNameNoTooltip], your [ROOT.Char.GetCouncillorPosition( 'councillor_chancellor' ).GetPositionName].` |
| `eotg_aug_tier2.011.c` | `Have the steward check the arithmetic.` | `Have my [ROOT.Char.GetCouncillorPosition( 'councillor_steward' ).GetPositionName] check the arithmetic.` |
| `eotg_aug_tier2.011.c.success` | `The steward finds the sums sound and trims the plan where the vassals would have felt it.` | `Your [ROOT.Char.GetCouncillorPosition( 'councillor_steward' ).GetPositionName] finds the sums sound and trims the plan where the vassals would have felt it.` |
| `eotg_aug_tier2.011.c.failure` | `The steward checks the arithmetic, and the plan does not survive it.` | `Your [ROOT.Char.GetCouncillorPosition( 'councillor_steward' ).GetPositionName] checks the arithmetic, and the plan does not survive it.` |
| `eotg_mod_aug_optimised_levies_trimmed_desc` | `The steward cut the parts of the schedule the vassals would have felt. What remains is smaller, and no one has complained of it.` | `The schedule was cut where the vassals would have felt it. What remains is smaller, and no one has complained of it.` |
| `eotg_aug_act.002.e` | `Declare my implants to the marshal.` | `Declare my implants before the bout.` |
| `eotg_aug_send_physician` | `My own physician` | `My own surgeon` |
| `eotg_aug_send_physician_tt` | `Your physician does the work, for less than a clinic charges.` | `Your own surgeon does the work, for less than a clinic charges.` |
| `eotg_aug_send_salvage_physician_tt` | `Your physician does the cutting, with care for what else is there.` | `Your own surgeon does the cutting, with care for what else is there.` |
| `eotg_aug_proc.001.desc_physician` | `\n\nYour physician knows these implants, and has offered to do it for less.` | `\n\nSomeone you can call on knows these implants, and has offered to do it for less.` |
| `eotg_aug_proc.003.desc_physician` | `\n\nYour physician has looked at the injury and your implants both, and could do the fitting for less.` | `\n\nSomeone you can call on has looked at the injury and your implants both, and could do the fitting for less.` |
| `eotg_aug_end.001.desc_physician` | `\n\nYour physician has reviewed the case personally and stays at the table. It helps.` | `\n\nThe case has had a physician's eye on it from the start. It helps.` |
| `eotg_aug_init.005.t` | `Back From the Capital` | `Back From the Clinic` |
| `eotg_aug_init.005.desc` | `Someone you know has returned from the capital different.` *(first sentence only; the rest is unchanged)* | `[eotg_aug_peer.GetFirstName] went to a clinic and came back different.` |
| `eotg_aug_init.003.desc` | `A technician in the capital offers a solution, for a price.` *(third sentence only; the rest is unchanged)* | `A technician has sought you out with a solution, for a price.` |
| `eotg_aug_tier1.002.desc` | `The newest model from [ROOT.Char.Custom('eotg_aug_cl_company')] has arrived in the capital.` *(first sentence only)* | `The newest model from [ROOT.Char.Custom('eotg_aug_cl_company')] has come in.` |
| `eotg_aug_tier2.004.desc` | `For weeks your spouse has said very little.` *(first sentence only)* | `For weeks your [eotg_aug_spouse.GetWifeHusband], [eotg_aug_spouse.GetFirstName], has said very little.` |
| `eotg_aug_end.020.a` | `[eotg_warden_spouse.GetFirstNameNoTooltip], your spouse.` | `[eotg_warden_spouse.GetFirstNameNoTooltip], your [eotg_warden_spouse.GetWifeHusband].` |
| `eotg_fracture.005.desc` | `Your heir was in the room. The exact details of what happened vary by account. What is agreed: the heir watched. [eotg_watching_heir.GetSheHe\|U] does not speak of it.` | `Your heir, [eotg_watching_heir.GetFirstName], was in the room. The exact details of what happened vary by account. What is agreed: [eotg_watching_heir.GetSheHe] watched. [eotg_watching_heir.GetSheHe\|U] does not speak of it.` |
| `eotg_aug_init.013.t` | `A Parent's Hardware` | `Your [eotg_dead_parent.GetMotherFather\|U]'s Hardware` |
| `eotg_fracture.026.e` | `Confess before the clergy.` | `Lay it all before the [ROOT.Char.GetFaith.PriestNeuterPlural].` |

In the table, `\|` is Markdown escaping. In the yml it is a plain `|`.

**After the script change below lands** (not before, or the string shows an unset scope):

| Key | Old | New |
|---|---|---|
| `eotg_fracture.026.b` | `Beg the heir to act.` | `Beg [eotg_lucid_heir.GetFirstName] to act.` |

### 3.2 Scripter (cybernetics session, via the orchestrator)
1. **`events/eotg_augmentation_fracture.txt`, `eotg_fracture.026` `immediate` → `hidden_effect`:** append `primary_heir ?= { save_scope_as = eotg_lucid_heir }` after the keeper `if`/`else_if` block. This is the full spec from §1 2.1. Change nothing else in the event.
2. **Sync comments (3.1). Comments only, no logic change.** Add the comment on the line above each of:
   - `common/on_action/eotg_augmentation_on_actions.txt:451` (`add_character_flag = { flag = eotg_flag_aug_settling  years = 5 }`)
   - `common/scripted_effects/eotg_augmentation_effects.txt:134`
   - `common/scripted_effects/eotg_augmentation_effects.txt:161`

   The comment to add: `# keep in sync with loc eotg_decision_aug_pursue_next_stage_desc ("five years") and _settling_tt ("5 years")`
3. **Sync comment (3.1), frontier owner:** above `add_county_modifier = { modifier = eotg_frontier_mod_merc_escort  years = 5 }` in `events/eotg_frontier_events.txt` (around :2316), add `# keep in sync with loc eotg_frontier.040.a_tt ("five years")`.
4. **Comment only, `events/eotg_augmentation_fracture.txt:4387`** (above the `eotg_fracture.026.e` option): replace `# [zealous] "Confess before the clergy."` with `# [zealous] "Lay it all before the clergy."`.
5. **Optional, comment only:** update the title list in the `events/eotg_augmentation_nonruler.txt` header (:5-10) to the new nr titles.

### 3.3 Validation (eotg-qa, after both owners)
- PX LSP and `px_vocab_check.py` on `localization` and `events`.
- Tiger: no new errors. `GetCouncillorPosition`, `GetPositionName`, `GetWifeHusband`, `GetMotherFather`, `GetFirstNameNoTooltip` and `KnightCulture*` all have vanilla precedent.
- In game, on the British Isles test sub-mod:
  - trigger `eotg_aug_tier2.012` and `eotg_aug_tier2.011`, and check that the seat name renders;
  - trigger `eotg_aug_nr.001` under a mod government, and check that the knight term renders (CB-48).

---

## 4. Lore constraints
Bound by `CLAUDE.md` §Canon. Nothing ruled here names a nation, faith, culture or person. The three lore points were settled by the lore-keeper in Round 2 (§2). The new text introduces no spelling-sensitive words; Canadian English applies to any further edits.

## 5. Deferred
- **`eotg_aug_tier2.006.desc` (the dead advisor).** Naming one needs a death-hook trigger that records a long-serving councillor. That is a new event beat, so it is the user's call.
- **Self-surgeon tooltip in interactions.** `eotg_aug_send_physician_tt` could become a `first_valid` `current_description` ("You do the work yourself") when the actor is the surgeon. The `.info` allows a desc there (`_character_interactions.info:322-323`). It is cosmetic, so it is left for the cybernetics session if wanted.
- **Named capital (2.2):** closed. Lore rules the capital is never named.
- **Religion-port follow-ups:** see §6.

## 6. Religion-port follow-ups

These are not loc tasks. They go into the religion port spec when it is written (the v1 religions need a 1.20 port, `CLAUDE.md` §File placement). Neither is urgent while the mod runs on vanilla faiths.

1. **Faith-term keys for every ported faith.** Each faith in `common/religion/faith_types/` must define the loc behind:
   - `PriestNeuter` / `PriestNeuterPlural` (plus male and female forms)
   - `HouseOfWorship`
   - `HighGodName`

   Otherwise `eotg_fracture.026.e` and every vanilla string that reads them shows a blank. Canon office-holders to use:
   - Plutocracy: "assessors" (`866_religions:168`)
   - Ancestor Veneration: "Name-Keepers" (:205)
   - Deep Warren: "Deepkeepers" (:222)

   Lore proposals where canon is silent (eotg-lore-keeper should confirm at port time):
   - Survivalism: "log-keepers"
   - Secular Codes: "auditors"
2. **`eotg_aug_tier2.005.desc` assumes a theistic faith.** "…the faith has a word for it. Desecration." fires for any zealous courtier (`events/eotg_augmentation_tier2.txt:776-781`). Once v1 religions are ported, that is false for a Survivalism zealot and doubtful for Plutocracy. Fix at port time with one of:
   - **(a)** a `first_valid` triggered desc variant for pragmatic-family faiths (no "desecration" framing); or
   - **(b)** gating those faiths out of the event trigger.

   Architect's recommendation: **(a)**. The event's signature-resource coupling stays reachable for every faith, and vanilla's faith-flavoured desc splits use the same shape. Rule it when the religion port spec names the families.

### HANDOFF
- status: done
- next: eotg-localizer
- ask: Apply §3.1 of `docs/specs/loc_dynamic_terms_ruling.md` to `eotg_augmentation_l_english.yml` (cybernetics session, via the orchestrator). Apply `eotg_fracture.026.b` only after scripter item §3.2.1 lands. The scripter applies §3.2 items 1-4 (item 3 is frontier-owned). Then eotg-qa runs §3.3.
- files: docs/specs/loc_dynamic_terms_ruling.md
- needs-loc: §3.1, 32 keys + 5 comment lines now; fracture.026.b after the script change
- needs-lore: none (§6 asks lore to confirm two proposed office-holder words at religion-port time)
- needs-human: none
