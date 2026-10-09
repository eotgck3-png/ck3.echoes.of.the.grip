# B8 localizer worklist: patron, procedures, tamper, interactions, realm (event_quality_v1 W5)

eotg-scripter finished the script half on 2026-10-09. The keys stay the same. Only the option text changes, so that it reads as the new axis (§13.1 step 7). Voice and quote rules are in §12. No desc path changed in B8: no `first_valid` or `triggered_desc` was added, removed or re-gated. The only other new script is portrait animations (W6) and stress rows. Each row lists the desc variants the new text has to work with (§13.1 step 7, B1 lesson 7).

Loc file: `localization/english/eotg_augmentation_l_english.yml`. The patron keys are around lines 1477–1538 (plus `.003.desc_voice` at 1743 and `.006.desc_writeoff` at 1744). realm.001 is around 2165–2180.

Patron letters are W9 and are not part of this batch. patron.008 and .009 were not re-gated, because each has only one personality gate.

## Re-axed options (text must change)

| Key | Current text | Old gate | New gate | What the text must convey | Desc variants to check |
|---|---|---|---|---|---|
| `eotg_aug_patron.001.e` | "Who are you, really?" | paranoid (icon) | `education_intrigue`, `skill = intrigue` | Seeing through the front: you question the envoy for who stands behind the money, then decline. It reads as a spymaster's probe, not as fear. You still decline, and you gain the intrigue lesson. | `.desc` only |
| `eotg_aug_patron.002.e` | "Ask for honest terms." | honest (icon) | `education_stewardship`, `skill = stewardship` | Auditing the invoice line by line (the "ongoing support" line is the obvious target) and offering to pay what it is actually worth. Success halves the bill. Failure means the envoy takes offence (grievance). | `.desc` only. The branch texts `.002.e.success` / `.002.e.failure` ("halves the figure" / "takes note of the request, and of you") already fit; check that they still follow from an audit. |
| `eotg_aug_patron.003.e` | "Their hands will never touch me." | paranoid (icon) | `highest_held_title_tier >= tier_duchy`, no icon | A refusal by right: the seat decides who services its body, and the syndicate's technicians are barred. It reads as command, not suspicion. The firmware still answers (risk), and the grievance rises. | `.desc` **and** `.desc_voice` (voice 2+: "the model has already priced the refusal"). The refusal must not contradict the model having anticipated it. |
| `eotg_aug_patron.004.e` | "Never, and they will hear of your asking." | just (icon) | `highest_held_title_tier >= tier_duchy`, no icon | A public refusal from the seat: the request is named before the court. That is the prestige gain. It should read as authority, not just as principle. Grievance +2. | `.desc` only. The critic may or may not be zealous, so don't presume the critic's faith. |
| `eotg_aug_patron.005.d` | "Not my child." | compassionate (option d) | **Folded** (§13.1 3c, B8 QA): now a `name = { trigger = { has_trait = compassionate } text = … }` variant on option b ("Never."). Option d is retired. | It is b's refusal (grievance +2) as a compassionate ruler says it. The current text fits, so a light touch at most. | `.desc` (named heir) **and** `.desc_no_heir` ("your next child"). b shows with or without an heir, so the text must not presume a living heir. |
| `eotg_aug_patron.006.e` | "Come and take it from me." | brave (icon) | `education_martial`, `skill = martial` | A soldier's dare, made with the guard already set: tell them to come in force and see what that costs them. The envoy dies (betrayal), and prestige rises by 200. It should read as a commander's judgement, not bravado. | `.desc_writeoff`, `.desc_betrayal`, `.desc_settlement`. The option needs the envoy present, so the `_absent` variants never show with it. In `.desc_writeoff` the syndicate is cutting a broken unit loose; the dare must work there too. |
| `eotg_aug_realm.001.e` | "The realm's law holds, for everyone." | just (icon) | `highest_held_title_tier >= tier_duchy`, no icon | Making the arrest a public example, by the seat's authority (it is option a plus prestige). | `.desc_ban` / `.desc_license` (independent: "your law") **and** `.desc_ban_v` / `.desc_license_v` (a vassal liege: "the law of your realm", lore R1). The text must not claim the law as root's own. "The realm's law" already works for both. Also check the tier lines (`.desc_nf/_oc/_enh/_aug`) and `.desc_courtier`. |

## Kept personality gates (text unchanged; listed for context)

- patron: .001.d greedy, .002.d deceitful, .003.d diligent, .004.d sadistic, .005.e ambitious, .006.d deceitful, .007.b paranoid, .008.e just, .009.e wrathful;
- procedures: .001.f zealous, .003.f cynical, .020.e zealous;
- tamper: .002.b sadistic, .004.e paranoid;
- interactions: .002.e cynical;
- realm: .001.f greedy.

No text change is needed for these.

## Not text, for awareness

- New stress rows show as stress tooltips, and none needs loc. They are tamper.004.e paranoid, int.002.e cynical, realm.001.f greedy, and realm.001.e just (a response row).
- The new `skill =` icons replace the trait icons on the re-axed options. No loc.
- W6 adds no keys. proc.004 (Seamless) keeps its `idle` portrait on purpose.
