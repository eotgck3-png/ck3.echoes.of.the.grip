# Cybernetics — Content Gaps (v2)

**Date:** 2026-10-04 · **State reviewed:** the working tree on `v2-space-map` after `22253cf`. It includes the uncommitted balance-spec work (B1/B2: Pursue the Next Stage, the override options, the congenital and coping-trait options). The two new beats in `docs/specs/cybernetics_v2_new_beats.md` (heir.007, patron.008) are specced but not built.
**Replaces:** [cybernetics_content_gaps.md](cybernetics_content_gaps.md), superseded 2026-10-03. Most of its proposals were built in v2 Phases 0–6.
**Audience:** the human and `eotg-architect`, who turns Part 1 into a spec. Event names and identifiers here are working proposals; the architect fixes the real ones.

**Every proposal obeys:**
- **Map-agnostic.** No title, province, character, culture or faith keys. Faith reactions only through `zealous` / `cynical` / `theologian` / piety.
- **Invariant 5.** Every flavor event moves or reads `eotg_fracture_risk`, or changes tier.
- **Hidden risk** (spec Q1). No tooltip quantifies risk.
- **XP moves only at 0/50/100** through `eotg_aug_set_integration_effect`.
- **Leaving the system goes through `eotg_aug_remove_all_effect`.**
- Index §1 rules on options, victims, scaled gold and cooldown authority.

---

# Part 1 — Procedures, providers and repairs (approved by the human, 2026-10-04)

## 1.1 What exists today

**Where you get the first implant matters. Nothing else does.**

| Procedure | Provider choice? | What can go wrong |
|---|---|---|
| **First install, via Seek Augmentation (`init.018`)** | Yes: sanctioned clinic / own physician / back streets | **Clinic:** nothing (medium gold, risk 0, 2 years Calibrated). **Physician:** nothing (75% cost, risk 0, 3 years Calibrated). **Back streets:** tiny gold, risk 5, then a roll 6–18 months later (`init.011`). |
| Back-alley roll (`init.011`) | — | Clean 35 (+15 with the intrigue edge); clean with hidden flaw 15 (permanent +4 risk a year); infection 20 (+10 under strain); rejection 15, leading to `init.012` (60% implants lost plus a wound step, 40% saved); discovered 10 (Black Market Implants); excellent 5. **About 60% of back-alley jobs go wrong**, but the worst case is losing the implants and taking a wound: no death, no maiming. |
| Other install offers (wound, corporate, aging, desperation, prosthetic, neural bridge, cynic, parent's hardware, duel shame, physician's proposal) | Fixed by the event | Mostly none. Desperation and the craven back-alley variant feed the same `init.011` roll. The Neural Bridge has its own settle stage. |
| **Upgrade to Enhanced** (`tier1.002` → `.021` → `.022`) | No; you choose the body part, not the provider | None from the procedure. |
| **Upgrade to Overclocked** (`tier2.003`; Bidding War `tier2.013/.014`) | The Bidding War offers careful or bold vendors (they shift later risk) | None from the procedure. |
| **Partial Removal, Downgrade Protocol, Remove the Implants** (decisions) | No | None. Flat cost plus a withdrawal modifier. |
| **Cut It Out** (Excision, `end.001`) | No back-alley version; a physician helps | Weighted roll: death 15 (25 on the craven option, +25 if Neurofractured, +10 if Overclocked, −15 with a physician), maimed 30, clean 30 (+15 with a physician). |
| **Healing wounds** | — | Five first-install options heal a wound fully, and one eases it. **Only at first install.** |
| **Replacing a lost limb, eye or sight** | — | The Prosthetic (`init.006`) removes one of blind / one_legged / maimed / one_eyed, worst first. Its option .f covers a clubfoot or hunchback, and the Neural Bridge covers infirm / incapable. **Only for an unaugmented character.** |

**The gaps:**
1. Reputable providers have **zero** risk, while the back alley goes wrong **most** of the time with no severe tail.
2. Upgrades and removals have no provider choice.
3. **Once augmented, a character can never repair a new injury.** A ruler who loses a leg in battle while Enhanced can't get a prosthetic.

## 1.2 Design goals
1. **Bad outcomes are rare at reputable providers and real at the back alley.** Severe outcomes (death, maiming, losing an eye) happen **only** at the back alley, and rarely. Excision keeps its own deliberately dangerous odds.
2. **Every procedure offers a provider choice:** install, both upgrades, every removal, and repairs. The back alley is always the cheap option.
3. **Augmented characters can repair injuries**, rarely: only when they are actually hurt.
4. **One shared outcome roll**, so the odds live in one place and stay consistent across procedures.

## 1.3 Proposal

### A. One outcome roll for every procedure
A new scripted effect, working name `eotg_aug_procedure_outcome_effect = { PROVIDER = clinic|physician|backstreet  PROCEDURE = install|upgrade|removal|repair }`. It saves the result as a scope value (`flag:clean`, `flag:infection` …) for the follow-up event's desc, the way `init.011` already does.

**Target odds** (weights out of 100). The architect tunes the exact values; the bands are the requirement.

| Outcome | Clinic | Physician | Back streets | Effect |
|---|---|---|---|---|
| Clean | 95 | 90 (+1 per point of the physician's learning above 10, max 96) | 62 | — |
| Excellent | 1 | 2 | 3 | `eotg_mod_aug_clean_install` (exists) |
| Infection | 3 | 5 | 10 | `eotg_mod_aug_infection` (exists); cleared by Consult the Physician |
| Hidden flaw | 0 | 1 | 8 | `eotg_flag_aug_hidden_flaw` (exists) |
| Rejection | 1 | 2 | 6 | install/upgrade: the `init.012`-style roll; removal: hardware left in (see C) |
| Discovered | 0 | 0 | 5 | `eotg_mod_aug_illegal_implants` (exists) |
| **Severe tail** | 0 | 0 | **3–4**, split: maimed or one_eyed 2, blinded 1, death on the table 0.5–1 (installs and removals only, never repairs) | vanilla traits; `death_treatment` |
| **Total bad** | **~4%** | **~8%** | **~32%, of which ~3–4% severe** | |

**Existing modifiers carry over as modifiers on the roll:**
- the back-alley intrigue edge (`eotg_flag_aug_chain_edge`) and strain flags;
- the craven "put me under" and discreet variants;
- `eotg_flag_aug_vendor_safe` from the Bidding War;
- the physician's skill (vanilla precedent: risky treatment in `common/scripted_effects/20_health_effects.txt`, where critical success and failure scale with the physician).

**Rebalance `init.011` onto this table.** It keeps its five descs and adds one for the severe tail.

### B. A provider choice at every procedure
| Procedure | How the choice appears | Back-street price |
|---|---|---|
| First install (`init.018`) | Exists. Clinic and physician now also roll (rarely). | tiny gold (unchanged) |
| Other install offers | Each offer keeps its fiction, mapped to a provider. The corporate offer and physician's proposal count as clinic or physician; desperation and the back-alley chain as back-street. Where an offer has a "cheaper" option, it is back-street. | — |
| Upgrade to Enhanced (`tier1.002`) | Add a back-street option, a, d and e count as clinic. Stage `.022` "Installation" reads the outcome and adds an outcome desc. | ~50% of the upgrade cost |
| Upgrade to Overclocked (`tier2.003`, `.013/.014`) | **Fold it into the Bidding War:** careful vendor = clinic, bold vendor = back-street (keeping its later-risk role), plus the physician where available. `tier2.003` without the war gets a back-street option. | ~50% |
| Partial Removal, Downgrade, Remove the Implants | The decision fires a new small event, working title "Who Takes It Out?", with clinic / physician / back streets. The decision's cost becomes the clinic price; back-street is cheaper. | ~40% |
| Excision (`end.001`) | Add a back-street table: cheap, death +10, maimed +10. The physician keeps its −15 death bonus. | ~40% |
| Repair (new, C) | In the repair event. | ~50% |

**Removal-specific bad outcome, "Fragments":** hardware left in. A new timed modifier, working name `eotg_mod_aug_fragments`, with health −0.25 and stress gain +5% for 5 years. A later Consult the Physician (or the clinic) removes it. The character is still out of the system (`eotg_aug_remove_all_effect` has already run), so risk is **not** recreated (QA round 2 M3).

### C. Repairs for characters who are already augmented
**Trigger.** Vanilla `on_trait_gained` (`common/on_action/traits_on_actions.txt:6`; root is the character, `scope:trait` the trait gained), extended additively. Limit:
- `eotg_is_augmented_any = yes`;
- `scope:trait` is one of wounded_2 / wounded_3 / maimed / one_legged / one_eyed / blind / disfigured;
- not on a repair cooldown (`eotg_flag_aug_repair_cooldown`, 3 years, set in the on_action).

wounded_1 is excluded so routine scrapes don't spam. Fire after a short delay, `days = { 7 30 }`.

**Events** (new, working names):

| Event | When | Options (3 universal + trait-gated) |
|---|---|---|
| **Spare Parts** (repair offer) | Track tiers (Augmented, Enhanced, Overclocked) | **Clinic** (medium gold) / **Own physician** (75%, needs physician access) / **Back streets** (~50%) / *Live with it* (stress helper; zealous / content relief). Trait options: `lifestyle_physician` "Hand me the tools" (self-repair, cheap, physician table at your own learning); `cynical` "Improve it while you're in there" (lesson prowess, +risk); `craven` "Put me under"; `zealous` "No more metal" (refuse, piety). |
| **Spare Parts, after** | Stage 2, 14–45 days later | Outcome desc from the roll. Clean: `eotg_aug_restore_loss_effect` / `eotg_aug_heal_wounds_effect`; bad: the table. |
| **No Clinic Will Touch It** | Neurofractured | Clinics refuse a Neurofractured patient: only the physician (at worse odds) or the back streets. A Storm-band variant can trigger an episode on the table. |
| **Self-Mending** | Seamless | One option, no choice. The machine repairs the body itself: the injury is removed and nothing else changes. It underlines that the person is gone. |

**Coupling (invariant 5).** Every repair adds risk, scaled by tier: Augmented +2, Enhanced +4, Overclocked +6, Neurofractured +8 (pressure). Back-street adds +3 more. A Seamless repair moves nothing (risk is a no-op there by design).

**Rarity.** The trigger needs a real injury, plus the 3-year cooldown. A ruler sees this roughly once or twice a reign at most.

**Unaugmented characters are not covered.** A ruler left maimed by Excision is unaugmented and already eligible for **The Prosthetic** (`init.006`), so nothing new is needed.

### D. Identifier sketch (for the architect)
- **Scripted effects:** `eotg_aug_procedure_outcome_effect` (A); a `eotg_aug_provider_cost_value` script value (one cost scale per provider).
- **Events:** a small namespace `eotg_aug_proc` ("Who Takes It Out?", repair offer, repair stage 2, Neurofractured variant, Seamless variant), plus new outcome descs on `init.011`, `tier1.022`, `tier2.014` and `end.001`.
- **Modifier:** `eotg_mod_aug_fragments`. Flag: `eotg_flag_aug_repair_cooldown`.
- **Loc:** roughly 70–90 keys. "Static" vocabulary only. Back-alley register follows the existing `init.010–.012` and the lore-keeper's rules: no named clinics and no named syndicate.

### E. Vanilla precedent
- Risky treatment, with physician-scaled success, critical failure, wounds and death: `common/scripted_effects/20_health_effects.txt`.
- `increase_wounds_no_death_effect` (REASON = treatment): already used in `init.012`.
- `on_trait_gained` with `scope:trait = trait:x`: `common/on_action/traits_on_actions.txt`.
- `employs_court_position = court_physician_court_position`: already used through `eotg_has_physician_access`.

### F. Calls for the architect (settle from vanilla precedent, per the standing rule)
- The exact weights, inside the bands in A.
- Whether wounded_2 is enough to trigger a repair, or only wounded_3 and lost body parts.
- Whether the Neurofractured repair can trigger an episode, or stays a cost and odds penalty.

The upgrade and removal choices change existing decisions and events. The repair line adds about 5 new events. **The human approved this direction on 2026-10-04.**

---

# Part 2 — Assessment: where the system is still missing content

**Method.**
- Inventoried the current tree: 153 events, 13 decisions, 4 story cycles, 7 hooks (`yearly_playable_pulse`, `on_death`, `random_yearly_everyone_pulse`, `on_birth_child`, `on_combat_end_winner/loser`, `on_game_start_after_lobby`).
- Ran `docs/tools/qa/trait_coverage.py`.
- Checked which CK3 systems reference the cybernetics traits.
- Already covered, not repeated here: round 2's ten design issues (balance spec, largely in the tree) and the two new beats.

**The headline:** the system is rich in **events about yourself** and thin everywhere CK3 lets you act on **other people**. No character interaction, scheme, activity, court position, law or men-at-arms type references `eotg_cybernetics`. Within its own scope, two end states (Seamless, and life after removal) are dead ends.

| # | Gap | Why it matters for "cybernetics in CK3" | Proposal | Size |
|---|---|---|---|---|
| **G1** | **Procedures, providers and repairs** | See Part 1. | Part 1. | M |
| **G2** | **Seamless has no ongoing life.** Only end.010 and end.011 are written for it. A Seamless ruler may live for decades, and no pulse fires for the state. | Total Integration is meant to be a distinct end state. Today it is a stat block followed by silence. | A small Seamless pool (4–6 events) on the yearly pulse: the court that left; the machine governs well and coldly (stewardship windfalls, council resignations); the heir confronts what's in the chair; one rare "flicker of the old self" (one option, no choice). Plus the Self-Mending repair from Part 1. | S–M |
| **G3** | **Nothing marks a former augmentation.** `eotg_aug_remove_all_effect` clears every variable and leaves no marker (`common/scripted_effects/eotg_augmentation_effects.txt` ~440–467). Only patron.008 (specced) reacts to removal. | Removal is a real choice (three decisions plus Excision) with no aftermath beyond a withdrawal modifier. | Set a permanent `eotg_flag_aug_former` in the remove-all effect, plus a 3–4 event pool: *Phantom Static*; *The Clinic Calls* (a discounted re-install offer, a relapse temptation); *Welcome Back* (zealous courtiers warm to you, cynical ones don't); *What Was Taken* (an Excision survivor who was maimed is pointed to the Prosthetic). | S |
| **G4** | **No character interactions.** Every lever is a decision about yourself; Augment Retainer covers only knights. | CK3's social play runs through interactions. Today you can't offer an implant to your spouse, pressure a vassal to remove theirs, or ask an ally for their surgeon. | 2–3 interactions (`common/character_interactions/`): **Offer Augmentation** (a courtier, vassal or adult family member accepts by AI weights, with opinion either way); **Demand Removal** (from a vassal or courtier, using hook or opinion, with a refusal penalty); optionally **Lend Your Surgeon** (an ally's physician access). | M |
| **G5** | **No schemes.** Tampering exists only as a one-off event (tier2.015/.016). | Intrigue is CK3's other core loop. "Sabotage their implants" is the most natural hostile scheme this system could add, usable by the player and the AI. | A hostile scheme **Tamper with Implants** (1.13+ scheme format, `common/schemes/`): target is augmented; success means a forced risk spike, an infection or an episode; discovery uses vanilla scheme exposure. Keep tier2.015 as the defensive event. | M–L |
| **G6** | **No vanilla activities.** Feasts, hunts, tournaments and pilgrimages never react to implants. | Tournaments especially: an augmented contestant is a built-in drama (cheating accusations, banned entrants, rigged contests). Activities are where AI and player characters meet. | 1–2 events per activity type, through each activity's existing pulse and on_actions. Start with tournaments: an augmented contestant, a ruling on "enhanced" entrants, a duel against the machine. Then hunts (sensors find the quarry; the beast spooks at the hum). | M |
| **G7** | **No realm-level policy.** Augmentation is purely personal. You can't ban, license or encourage it in your realm, and vassals never react to your policy. | Feudal rulers legislate. A policy lever makes the "world" part of the system controllable and gives zealous and cynical vassals something to fight over. | A decision **Augmentation Edict** (ban / license / encourage) that sets a realm-holder flag and modifier. It changes vassal augment weights in the yearly pulse, gives opinion to zealous vassals (ban) or cynical and ambitious ones (encourage), and makes back-street discovery harsher under a ban. Map-agnostic. **Later:** faith doctrines and cultural traditions after Gate 1 (already deferred). | M |
| **G8** | **Augmented prisoners are only test subjects.** | Capturing an augmented enemy should matter. | A prisoner interaction or prison event, **Salvage**: strip the implants (forced `eotg_aug_remove_all_effect` on the prisoner, Fragments likely, dread, kinslayer and tyranny rules per round 2 M4/M5), then install the salvage at a discount or sell it. A higher ransom for an augmented prisoner. | S |
| **G9** | **Six personality traits are still thin** (deferred in balance §10): chaste 1, fickle 1, impatient 1 trait-gated option; lustful, gluttonous, temperate 2 each. Stress coverage is equally thin. Forgiving and arbitrary have 1 gated option each, though they carry stress. | The "options cover a multitude of traits" goal is met on count but not on depth for these six. | Add one gated option per thin trait in existing events. Natural fits: lustful/chaste in A Lover's Touch and The Space Between Us; gluttonous/temperate in Dulled Palate and The Feast You Didn't Eat; impatient in Tremor and the Pursue decision; fickle in the regression decisions. No new events. | S |
| **G10** | **No dedicated court position.** The vanilla physician is reused everywhere. | A hireable "Implant Technician" would be a visible, ongoing lever (cheaper maintenance, better procedure odds), and court positions are how CK3 surfaces a specialist. | A court position (`common/court_positions/`) available to rulers with the trait or a licence edict (G7). Feeds the physician's role in the Part 1 table. Needs loc; check whether it needs art. | M |
| **G11** | **No augmented men-at-arms.** The Iron Retinue covers knights only. | War is half of CK3. | Deferred: men-at-arms types touch culture innovations. Revisit after Gate 1 alongside the v1 men-at-arms lift. | — |
| **G12** | **The Clinic (Q10), faith and culture reactions** | Already deferred. | Unchanged: Clinic until building gates; faith and culture after Gate 1. | — |

## Recommended order
1. **Part 1 (G1):** approved. Architect spec next.
2. **G3 and G2:** small, and they close the two dead-end states. Can be specced alongside Part 1, since both touch the remove-all effect and the endgame.
3. **G9:** cheap depth on an existing goal; no new events.
4. **G4 and G5** (interactions and the tampering scheme): the biggest gain in "plays like CK3". They give the player levers over other people and give the AI a way to use the system against the player.
5. **G7, then G10:** the realm layer. The edict first, since the court position can hang off it.
6. **G6:** activity integration. G8 can ride along with G4 (it is an interaction).

**New events need the human's sign-off** (the balance spec's rule). Part 1 is approved. G2, G3, G5, G6 and G8 add new events and would need a yes. G4, G7, G9 and G10 are mostly new interactions, decisions and options on existing events.
