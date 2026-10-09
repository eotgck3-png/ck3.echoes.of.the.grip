# B8 samples: patron, procedures, tamper, interactions, realm loc (W1 + W4 + W5 reframes)

File: `localization/english/eotg_augmentation_l_english.yml`, prefixes `eotg_aug_patron.*`, `eotg_aug_proc.*`, `eotg_aug_tamper.*`, `eotg_aug_int.*`, `eotg_aug_realm.*`. Refreshed from the current loc after the lore and QA fixes.

Scorecard rows (voice first / second / neutral, dialogue):
- patron (9 events): 100 / 0 / 0, 77.8%.
- procedures (6): 83.3 / 0 / 16.7, 50.0%. proc.004 is Seamless and unchanged; it is the 16.7%.
- tamper (3): 100 / 0 / 0, 66.7%.
- interactions (2): 50 / 0 / 50, 50.0%. int.001 stays neutral (root is the actor, never narrated), int.002 is first person.
- realm (1): 100 / 0 / 0, 100%.
- Lint against baseline: 0 new.

**1. eotg_aug_patron.003.desc and .003.e**
- desc: "...From now on only the syndicate's technicians are to service my implants. "Quality control," the envoy says, "and any other hands in the casing would end the support." The firmware has been set to notice."
- 003.e (duchy+): "By the right of my seat, I bar the syndicate's technicians."

**2. eotg_aug_patron.006.desc_writeoff and .006.e (the dare must work in the write-off)**
- desc_writeoff: "The envoy does not sit down. [syndicate] has reviewed my account and closed it. "The syndicate does not service broken units," the envoy says. "What you owe is due now.""
- 006.e (martial): "My guard is set. Tell them to come in force, and see what it costs them."

**3. eotg_aug_realm.001 (R1: independent "my law", a vassal liege "the realm I hold my lands under")**
- desc: "Word has reached me, and a courtier says it quietly: "It is [subject]. [She] has had implant work done that the realm's law does not allow.""
- desc_ban_v: "The realm I hold my lands under prohibits augmentation, and [she] lives under it."
- 001.e (duchy+): "Arrest [subject], and make a public example of [subject] under the realm's law."

**4. eotg_aug_proc.001.desc and eotg_aug_int.002.desc (fitter lines, root as the patient or actor)**
- proc.001: "...The clinic has a table, a team and a price. "Cheaper hands can be found," a fitter tells me, "and they will not ask to see a record.""
- int.002: "Everything taken from [recipient] has been cleaned and laid out on a tray. It is mine to do with as I like. "Mind the edges on the casings," the one who did the cutting says."

## Reframes (7)
patron.001.e (intrigue) "Question the envoy on who stands behind the money, then decline." / patron.002.e (stewardship) "Audit the invoice line by line, and offer what it is worth." (success: "The envoy considers the audit, and halves the figure."; failure: "The envoy takes note of the audit, and of me.") / patron.003.e (duchy+) above / patron.004.e (duchy+, no assumption about the critic's faith) "Never. And I will name the request before the court." / patron.005.d (duchy+, works with and without a named heir) "My heirs are not collateral. No contract binds them." / patron.006.e (martial) above / realm.001.e (duchy+) above.

## Notes for the reviewer
- The patron absent-envoy letters (`desc_*_absent`) were left as written: W9 owns them.
- Root checks: patron, proc and realm roots are the ruler or patient. In tamper.002 and .003 root is the scheme owner ("my agents"); in tamper.004 root is the victim. In int.001 and .002 root is the actor of the interaction.
- patron.008.e outcomes now read "My household holds/upholds...", not a court.
- Speakers: envoy, collector, clinic technician or fitter, lead agent, courtier. All are generic or guarded by the scope, and none assumes kinship, rank or acquaintance.
- Time-of-day words: none in these families (grep returns 0).
- "Our scholars' hardware" in proc.005.desc was kept (lore wording, not a root voice).
