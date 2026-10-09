# Loc audit: hard-coded terms that should be dynamic (2026-10-08)

**Status:** proposal. Nothing is applied. eotg-architect rules on each item, with a lore-keeper consult where marked. Implementation goes through the orchestrator: the cybernetics files belong to the Cybernetics Modding session.

**Scope:** all 8 files in `localization/english/` (3,676 lines). Line numbers are as of 2026-10-08 and drift when those files change, so match on the key.

**Method:**
1. Grep for twelve term families: knight, rank, liege/court, council seat, faith, gendered words, places, army, house, numbers, people, and "they" left beside a scoped character.
2. Read every hit.
3. Check scopes in `events/`.
4. Check every proposed function against vanilla 1.20. eotg-vanilla-scout cited a `file:line` for each; the citations are in the appendix.

Nothing here proposes a function that vanilla lacks.

Already fine, so not listed:
- Government ranks come through `common/flavorization` (92 entries).
- 7 knight terms in the cybernetics file already use `KnightCulture`.
- Pronouns are handled by the 2026-10-04 pass (the leftovers are with the Cybernetics session's localizer).
- Debug strings.
- Flavour numbers in prose ("seventeen threats", "six minutes").

---

## Priority 1: wrong for some players today

### 1.1 "Champion" means a knight here, so use the knight term
`eotg_champion` is a retinue knight (`eotg_aug_is_retinue_knight`, `common/on_action/eotg_augmentation_on_actions.txt:1663-1710`). tier1.016's champion comes from `ordered_knight` (`events/eotg_augmentation_tier1.txt:2031`). Rule: never hard-code "knight"; use `KnightCulture` on the realm owner, with no "a"/"an" before it.

| Key (file:line) | Now | Proposed |
|---|---|---|
| `eotg_aug_tier1.016.c` (aug:1014) | Send my champion. | Send one of my [ROOT.Char.Custom('KnightCulturePluralNoTooltipLowercase')]. |
| `eotg_aug_tier1.016.c.success` (aug:1015) | Your champion wins the bout. | [eotg_champion.GetFirstName] wins the bout for you. *(scope is saved in the option, tier1.txt:2076)* |
| `eotg_aug_tier1.016.c.failure` (aug:1016) | Your champion loses the bout. | [eotg_champion.GetFirstName] loses the bout. |
| `eotg_aug_nr.001.t` (aug:1621) | The Champion Volunteers | The [ROOT.Char.Custom('KnightCultureNoTooltip')] Volunteers |
| `eotg_aug_nr.002.t` (aug:1630) | Your Champion's New Edge | [eotg_champion.GetFirstName]'s New Edge |
| `eotg_aug_nr.004.t` (aug:1650) | The Champion's Mistake | The [ROOT.Char.Custom('KnightCultureNoTooltip')]'s Mistake |
| `eotg_aug_nr.004.desc` (aug:1651) | …The champion did not mean it… | …[eotg_champion.GetFirstName] did not mean it… |
| `eotg_aug_nr.005.t` (aug:1660) | A Changed Champion | A Changed [ROOT.Char.Custom('KnightCultureNoTooltip')]. **Breaks the no-article rule**, so use "[eotg_champion.GetFirstName], Changed" or "Not Quite the Same". |
| `eotg_aug_nr.006.t` (aug:1669) | The Broken Champion | The Broken [ROOT.Char.Custom('KnightCultureNoTooltip')] |

Note: until CB-48 (the mod's own `KnightCulture` override per government) lands, these show vanilla's fallback ("Knight"/"Champion"). Converting now means they pick up CB-48 automatically.

### 1.2 Council seats: name them through the seat, not a fixed English word
Vanilla's seat names vary by government (`council_l_english.yml:90`: the theocratic chaplain is "Archbishop"). Governments v2 may flavour them for the PMC, Corporation, Cartel and Gob-Corp. Hard-coded "spymaster", "chancellor" and "steward" won't follow.

| Key (file:line) | Now | Proposed | Scope |
|---|---|---|---|
| `eotg_aug_tier2.012.desc` (aug:1130) | Your spymaster, [eotg_flagged.GetFirstName], is flagged. | [eotg_flagged.GetFirstName], your [eotg_flagged.Custom('CouncilPosition')\|l], is flagged. | eotg_flagged holds the seat |
| `eotg_aug_end.020.c` (aug:853) | [eotg_warden_chancellor.GetFirstNameNoTooltip], your chancellor. | …, your [eotg_warden_chancellor.Custom('CouncilPosition')\|l]. | holds the seat |
| `eotg_aug_tier2.011.c` / `.c.success` / `.c.failure` (aug:1122-1124) | the steward | the [ROOT.Char.GetCouncillorPosition('councillor_steward').GetPositionName\|l] | realm owner |
| `eotg_mod_aug_optimised_levies_trimmed_desc` (aug:1753) | The steward cut… | A modifier desc has no reliable ROOT, so **rephrase** instead: "Your treasury cut…" | none |
| `eotg_aug_act.002.e` (aug:2124) | Declare my implants to the marshal. | Whose marshal is it (the host's?)? No scope is saved in-event. **Needs a scripter check** before a function can be chosen; otherwise rephrase to "Declare my implants to the stewards of the field." | unknown |

### 1.3 "Physician" when the hands may be an Implant Technician's
`eotg_aug_send_physician_valid_tt` (aug:1924) says the provider is "a physician or implant technician". The procedure effect saves the technician as `eotg_proc_surgeon` (`common/scripted_effects/eotg_augmentation_effects.txt:1913`). Yet the option text always says "physician".

Affected keys:
- `eotg_aug_proc.001.b` (1808), `.003.b` (1844), `.005.b` (2215)
- `eotg_aug_tier1.002.f` (1870), `eotg_aug_tier2.003.f` (1872), `eotg_aug_tamper.004.b` (2044), `eotg_aug_init.018.c` (460): "My own physician."
- `eotg_aug_send_physician` / `_tt` (1917-1918), `eotg_aug_send_salvage_physician_tt` (1925)
- `eotg_aug_proc.001.desc_physician` / `.003.desc_physician` (1806, 1842)

Proposed, pick one:
- **(a)** Generic wording that is true for both: "My own surgeon." / "Your own surgeon does the work…". This needs no script change.
- **(b)** Dynamic: `[eotg_proc_surgeon.Custom('GetCouncilOrCourtPosition')|l]` (vanilla `00_relations.txt:9431`). This only works where `eotg_proc_surgeon` is saved **before** the option displays, so it needs a scripter check per event.

Recommendation: (a), because it is safe everywhere. Keep "physician" only in strings where the script requires a court physician (init.017, end.001.desc_physician).

---

## Priority 2: should be dynamic, low risk

### 2.1 Name the character the event already has
These are "someone" or role nouns where the event saves the scope. CK3 writing names people.

| Key (file:line) | Now | Proposed |
|---|---|---|
| `eotg_aug_init.005.desc` (aug:131) | Someone you know has returned from the capital different. | [eotg_aug_peer.GetFirstName] has returned from [ROOT.Char.GetCapitalLocation.GetName] different. |
| `eotg_aug_tier2.004.desc` (aug:215) | For weeks your spouse has said very little. | For weeks your [eotg_aug_spouse.GetWifeHusband], [eotg_aug_spouse.GetFirstName], has said very little. |
| `eotg_aug_end.020.a` (aug:851) | …, your spouse. | …, your [eotg_warden_spouse.GetWifeHusband]. |
| `eotg_fracture.005.desc` (aug:335) | Your heir was in the room… the heir watched. | [eotg_watching_heir.GetFirstName] was in the room… [eotg_watching_heir.GetSheHe] watched. |
| `eotg_aug_init.013.t` (aug) | A Parent's Hardware | Your [eotg_dead_parent.GetMotherFather]'s Hardware |
| `eotg_fracture.026.b` (aug:716) | Beg the heir to act. | Name the heir. **But fracture.026 saves no heir scope** (it saves only `eotg_keeper`, :4268-4274), so this needs a script change. Defer, or use `[ROOT.Char.GetPlayerHeir…]` once that form is verified. |
| `eotg_aug_tier2.006.desc` (aug:232) | A long-serving advisor is dead… | No scope is saved, so this needs script. Defer. |

### 2.2 The capital by name
Vanilla form (101 uses): `[ROOT.Char.GetCapitalLocation.GetTitle.GetNameNoTierNoTooltip]`. A simpler one is `GetCapitalLocation.GetName` (25 uses).

| Key (file:line) | Now | Proposed |
|---|---|---|
| `eotg_aug_init.003.desc` (aug:117) | A technician in the capital offers… | A technician in [ROOT.Char.GetCapitalLocation.GetName] offers… |
| `eotg_aug_init.005.desc` (aug:131) | from the capital | (see 2.1) |
| `eotg_aug_tier1.002.desc` (aug:148) | …has arrived in the capital. | …has arrived in [ROOT.Char.GetCapitalLocation.GetName]. |
| `eotg_aug_tier3.023.e` (aug:1389) | Command from the capital. | Keep. An option label reads better generic. |

**Lore question:** is the capital a world, station or barony name in this setting? `GetCapitalLocation.GetName` returns the province (barony) name. Under the glossary, which name should the prose show: the System's or the planet's?

### 2.3 Faith words
These come from the faith, so they follow the player's religion. Vanilla gives `GetFaith.PriestNeuterPlural`, `HouseOfWorship`, `GetAdjective` and `HighGodName`.

| Key (file:line) | Now | Proposed |
|---|---|---|
| `eotg_fracture.026.e` (aug:718) | Confess before the clergy. | Confess before the [ROOT.Char.GetFaith.PriestNeuterPlural]. |
| `eotg_aug_tier2.005.d` (aug:226) | The faith has no say over my body. | Optional: "No [ROOT.Char.GetFaith.GetAdjectiveNoTooltip] [ROOT.Char.GetFaith.PriestNeuter] has a say over my body." |
| `eotg_frontier.041.desc_order` (frontier:369) | a holy order of your faith | a holy order of the [ROOT.Char.GetFaith.GetAdjective] faith (optional) |
| `eotg_aug_act.006.t` (aug:2160) | At the Holy Site | Keep. "Holy site" is a game concept and generic. |
| Prayer lines (aug:321, 428), "Bless the glass" (546), rites (982; kingpin:250) | — | **Keep.** Vanilla has no dynamic prayer verb (the scout checked). |

**Lore and architecture dependency:** these functions read the faith's own loc keys. The mod's 1.20 faiths (not ported yet) must define `PriestNeuter`/plural, `HouseOfWorship` and `HighGodName` for every faith, or they show blanks. That is a checklist item for the religion port, not a loc task. **Lore question:** do Grip faiths have clergy at all, and are they called priests?

---

## Priority 3: consistency, optional

### 3.1 Numbers that copy a script value
- `eotg_decision_aug_pursue_next_stage_desc` (aug:892) says "five years", and `_settling_tt` (aug:895) says "5 years". This matches the 5-year flag `eotg_flag_aug_settling` (`common/decisions/eotg_augmentation_decisions.txt:915`).
- `eotg_frontier.040.a_tt` (frontier:363) says "five years". This matches `years = 5` (`events/eotg_frontier_events.txt:2317`).

All of these are correct today. Vanilla also writes durations into text. Options:
- keep, and add a `# keep in sync with …` comment beside the script value; or
- rephrase without the number ("Each stage needs years to settle…") and let the trigger tooltip carry it.

The tooltip `_settling_tt` should stay explicit. Recommendation: keep and comment.

### 3.2 "Realm"
"Realm" is used about 40 times (augmentation policy laws, aug:2058-2087). Vanilla's `Custom('GetRealmOrDomicile')` only differs for domicile governments (nomad/herder). The only herder-style mod government is the Unclaimed placeholder, which no player runs. **No change.**

---

## Rulings needed

**Architect:**
1. 1.3: (a) or (b).
2. 1.2 `act.002.e`: scope or rephrase.
3. 2.1: whether fracture.026 and tier2.006 get a scope (new script) or stay generic.
4. 3.1: keep-and-comment or rephrase.
5. Whether council-seat flavour per government is planned in governments v2. If not, 1.2 is still correct but lower value.

**Lore-keeper:**
1. 1.1: are the nr.* titles acceptable with the knight term? CB-48 will give per-government words.
2. 2.2: what the capital is called in prose.
3. 2.3: Grip clergy terminology, and whether `tier2.005.d` should name the faith.

## Appendix: vanilla citations
All paths are under `game/`.
- `KnightCulture*` variants: `common/customizable_localization/00_knight_culture.txt:1,91-121`; usage `localization/english/accolades/accolades_l_english.yml:859-860`.
- `Custom('CouncilPosition')`: `common/customizable_localization/00_councillor_custom_loc.txt:1`; usage `localization/english/diarchies/diarchies_l_english.yml:132`.
- `GetCouncillorPosition('…').GetPositionName`: `localization/english/dlc/pam/pam_ecclesiastical_domicile_l_english.yml:68`.
- `Custom('GetCouncilOrCourtPosition')`: `common/customizable_localization/00_relations.txt:9431`; usage `localization/english/dlc/fp3/dlc_fp3_clan_events_l_english.yml:60`.
- `GetWifeHusband`, `GetMotherFather`: `localization/english/bookmark/bookmark_china_1066_l_english.yml:30`.
- `GetCapitalLocation.GetName`: 25 uses in vanilla loc, e.g. `[ROOT.Char.GetCapitalLocation.GetName]`.
- `GetFaith.PriestNeuter`/`PriestNeuterPlural`: `localization/english/custom_localization/divinity_custom_loc_l_english.yml:48-52`.
- `GetFaith.GetAdjective`: `localization/english/artifacts/artifacts_l_english.yml:809`.
- These do not exist in vanilla, so they are not proposed: a prayer-verb function, a culture adjective, `GetLordLady`/`GetKingQueen` (vanilla has `GetLadyLord`/`Custom('GetQueenKing')`), and any Custom that renames levies or men-at-arms per government.
