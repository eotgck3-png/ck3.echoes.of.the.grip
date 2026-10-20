# Investigation rulings, 2026-10-18 (§2 of the system investigation)

**Source:** `docs/qa/system_investigation_2026-10-18/REPORT.md` §2. **Game:** CK3 1.20.1.1. `G` = `D:/SteamLibrary/steamapps/common/Crusader Kings III/game`. **Author:** eotg-architect, 2026-10-20. **Status:** the owner approved this ruling pass. X2 and P1 are owner rulings (2026-10-20) and are recorded here, not asked.

Specs only. Nothing here adds an event, an option or a beat (owner rule). Ideas that would need one are listed in §13 as suggestions. Everything is map-agnostic: no title, province, culture, faith or character key.

---

## 1. Purpose & gate

The investigation found about 40 gaps. §1 of the report was mechanical and went to fix batch I1. This spec rules the §2 items that needed a design decision, and turns each into an exact script change, a test and a build batch.

- **Cybernetics** (S1, S2, S4, C3, C4, C6, C7, C8/C9, C10) and the **Cartel × kingpin** item (X2) are mod-exclusive. They are exempt from Gate 1 (CLAUDE.md, 2026-10-02 and 2026-10-08) and can be built now.
- **Frontier** (F2) is mod-exclusive and map-agnostic. It is also buildable now.
- **F8/X6** and **P1** are records only. Nothing is built.

## 2. Signature resources touched

| System | Resource | How these rulings move or read it |
|---|---|---|
| Cybernetics | `eotg_fracture_risk` plus tier | S1 routes retainer and knight installs through the procedure roll (tier change plus outcome). C3, C6 and C8/C9 gate when risk and tier move. |
| Cybernetics (realm) | The augmentation law, through `eotg_aug_under_policy` | S1 and S4 decide who answers for contraband work. The new secret's `is_criminal` reads the law. |
| Frontier | Establishment and strain (`sponsor_lapsed` cause) | F2 lapses a sponsorship through the existing strain path. |
| Cartel (G2) | `dread` | X2: the kingpin's dread beats interact with tribute retention (§9). |

No new flavour event is added, so invariant 5 binds nothing new. Every changed option still moves its system's resource.

## 3. Batches

| Batch | Items | Owner | Depends on |
|---|---|---|---|
| **I2a: who answers for unlawful work** | S1, S4, the new secret type | scripter, then localizer | nothing. Highest severity, so build it first. |
| **I2b: presence and pacing guards** | S2, C3, C4, C6, C7, C8/C9, C10 | scripter, then localizer (1 key) | nothing |
| **I2c: Frontier sponsorship terms** | F2 | scripter | nothing |
| **I2d: kingpin under a Cartel** | X2 | scripter, then localizer (1 key) | Must land **before Cartel G2 C2** |
| **Records (no build)** | F8/X6, P1, S7, S8, S9, S13 | orchestrator (taskboard) | — |

QA runs after each batch: Tiger, `px_lsp_diagnostics.js`, `px_vocab_check.py`, the event report. The V-IR tests go into `docs/qa/IN_GAME_SESSION_PLAN.md`.

---

## 4. I2a: who answers for unlawful work (S1, S4)

### 4.1 Rulings

**Rule R-A1. Every install rolls, and every roll knows who chose it.** The retainer decision (init.020 a–d), the knight volunteer (nr.001 a, c, d) and the Iron Retinue installs (`eotg_aug_retinue_install_effect`, retinue.001–.004) go through `eotg_aug_procedure_effect` with a provider. The provider is **derived, not chosen**, so no option is added:
1. a clinic, if the patient's realm allows clinics (`eotg_aug_clinic_open`);
2. otherwise the sponsor's own surgeon, if the sponsor has one for this patient (`eotg_aug_has_surgeon_for`);
3. otherwise the back streets.

The price written on each option is unchanged.

*Why route instead of only running a contraband check:* a bare check under a Ban would need its own "discovered" odds. Those odds would drift from the roll's table (realm spec §3.2). They would also skip infection and rejection, which are the real cost of a Ban: no clinic means a physician or the back streets. Routing reuses one table, and the outcome is revealed by events that already exist (init.011, proc.002). Outside a Ban the roll is the clinic column, which is 95% clean. The cost of the change is small: a retainer install can now become infected or be rejected.

**Rule R-A2. The one who chose the work answers for it (S4).** Every crime path picks one **answerable party**:
- the **sponsor**, when the sponsor is the patient's liege or above (`target_is_liege_or_above`), since they ordered or gave the work;
- otherwise the **patient**, for self-sought work or a gift from outside the patient's chain of lieges.

The answerable party's own liege gains the crime. So:
- **A liege never prosecutes their own gift.** S4 is fixed by construction.
- **An independent sponsor is never a criminal** (lore Q1.4: the lawmaker is not a criminal under their own law).
- **A vassal who orders an unlawful install on their own knight** answers to *their* liege, the one whose Ban they broke.
- **The law never leaves the realm** (Q1.5). A foreign sponsor is never answerable. The patient answers in their own realm, as today.

**Rule R-A3. Undiscovered unlawful work leaves a secret.** If a roll is contraband under `eotg_aug_is_contraband` and the outcome is anything except `discovered` or `death`, the answerable party gains the vanilla secret `eotg_secret_illegal_augmentation`. Vanilla then provides the rest for free:
- the spymaster's Find Secrets task and the hostile scheme (the triggers are generic: `G/common/scripted_triggers/00_councillor_triggers.txt:813-826, 876-880` read `is_criminal_for` / `is_blackmailable_secret_trigger`, with no type whitelist);
- blackmail;
- Expose Secret;
- once exposed, the crime is a lawful reason to imprison (`G/localization/english/game_concepts_l_english.yml:1059`, `game_concept_crime_desc`: "All crimes give Rulers a valid reason to imprison").

The `discovered` outcome keeps its current public path (`eotg_opinion_aug_contraband`, realm.001). It is already a known crime, so no secret is created for it.

**Rule R-A4. AI weights fall under a Ban.** These follow the realm spec §3.3 precedent (the Seek decision ×0.5 under a Ban, `common/decisions/eotg_augmentation_decisions.txt:348`; Offer ×0.25, `common/character_interactions/eotg_augmentation_interactions.txt:404`):

| Where | Change under `eotg_aug_under_policy = { LAW = ban }` (root's realm) |
|---|---|
| `eotg_decision_augment_retainer` `ai_will_do` | `modifier = { factor = 0.5  eotg_aug_under_policy = { LAW = ban } }` |
| init.020 a, b, c, d `ai_chance` | `modifier = { factor = 0.5  eotg_aug_under_policy = { LAW = ban } }` |
| init.020 e ("None of them") `ai_chance` | `modifier = { add = 30  eotg_aug_under_policy = { LAW = ban } }` |
| `eotg_on_yearly_aug_nonruler_check` step 1, `random = { chance = 3 … }` | `modifier = { factor = 0.5  scope:eotg_nr_liege = { eotg_aug_under_policy = { LAW = ban } } }` |
| nr.001 a, c, d `ai_chance` | `modifier = { factor = 0.5  eotg_aug_under_policy = { LAW = ban } }` |
| nr.001 b ("Denied.") `ai_chance` | `modifier = { add = 30  eotg_aug_under_policy = { LAW = ban } }` |

An independent lawmaker who bans augmentation and still augments their own knights pays only the roll (Q1.4). The AI factors make that rare.

### 4.2 Vanilla precedent

| Piece | Precedent |
|---|---|
| Secret type shape | `G/common/secret_types/00_secret_types.txt:620-656` (`secret_embezzler`): realm-law crime, `is_shunned` = not criminal, `on_expose` |
| Field list | `G/common/secret_types/_secret_types.info` (category, is_valid, is_shunned, is_criminal, on_discover, on_expose, on_owner_death) |
| Criminal only to the harmed party | `G/common/scripted_triggers/00_secret_type_triggers.txt:435-447` (`secret_embezzler_is_criminal_trigger`: criminal only if `secret_target` is the owner's liege) |
| Reading a secret's variable from a trigger | the same trigger scans `$OWNER$ = { any_secret = { type = … var:… } }` instead of reading root. Copy that shape. |
| Add through one scripted effect | `G/common/secret_types/00_secret_types.txt:8` (the NOTE), `G/common/scripted_effects/00_secret_effects.txt:500-545` (`give_or_update_embezzler_secret_effect`: check `any_secret`, then `add_secret`, then `random_secret` to set a variable) |
| Exposure notification | `G/common/scripted_effects/00_secret_effects.txt:878-1030` (`secret_exposed_notification_effect`). Unknown types fall to the feed-message `else` at `:1023-1025`, so no new notification event is needed. |
| Category icon | vanilla `G/gfx/interface/icons/secret_categories/civil.dds`, loc `secret_category_civil`. Reuse it: no art. |
| The roll, the crime opinion | already cited in `cybernetics_v2_procedures.md` §4.2 and `cybernetics_v2_realm.md` §4.2 (`illegal_resisted_conversion_opinion`, `G/common/opinion_modifiers/00_religious_opinions.txt:118-123`) |

### 4.3 Identifier table

| Type | Name | File | Notes |
|---|---|---|---|
| secret type | `eotg_secret_illegal_augmentation` | `common/secret_types/eotg_augmentation_secrets.txt` (**new folder**; the orchestrator adds `common/secret_types/` to the CLAUDE.md placement list; no `replace_path`) | shape §4.4 |
| character variable | `eotg_aug_sponsor` (character, `years = 2`) | set by the install paths, read by the roll and the reveal | The 2 years cover the longest reveal delay (back-street Offer, init.011 at 180–540 days, `eotg_augmentation_effects.txt` offer path). Removed by `eotg_aug_contraband_effect`. Otherwise it lapses. |
| secret variable | `eotg_aug_unlicensed` (on the secret, `value = yes`) | set by the give effect | set only when the work was back streets under a License |
| saved scope | `eotg_aug_answerable` | `eotg_aug_save_answerable_effect` | temporary |
| scripted effect | `eotg_aug_save_answerable_effect` | `common/scripted_effects/eotg_augmentation_effects.txt` | patient scope; §4.5 |
| scripted effect | `eotg_aug_give_illegal_work_secret_effect` | same | patient scope; §4.5 |
| scripted effect | `eotg_aug_sponsored_install_effect` (param `SPONSOR`) | same | patient scope; §4.5 |
| scripted trigger | `eotg_aug_illegal_work_is_criminal` (params `OWNER`, `VIEWER`) | `common/scripted_triggers/eotg_augmentation_triggers.txt` | §4.4 |
| edited effects | `eotg_aug_contraband_effect`, `eotg_aug_procedure_roll_effect`, `eotg_aug_retainer_install_effect`, `eotg_aug_retinue_install_effect`, `eotg_aug_offer_install_effect` | same file | §4.5 |
| edited events | init.020 (d's inline block, AI weights), nr.001 (a, c, d, b weights), realm.001 (one triggered desc) | `events/eotg_augmentation_initiation.txt`, `_nonruler.txt`, `_realm.txt` | no new options |

### 4.4 The secret type (full shape)

```
eotg_secret_illegal_augmentation = {
    category = civil                     # vanilla icon + secret_category_civil; no art

    # Valid while the hardware it is about is still in a body. A full removal
    # or Excision dissolves it: the evidence is physical (lore I5).
    is_valid = {
        trigger_if = {
            limit = { exists = scope:secret_target }
            scope:secret_target = { is_alive = yes  eotg_is_augmented_any = yes }
        }
        trigger_else = {
            scope:secret_owner = { eotg_is_augmented_any = yes }
        }
    }

    # A crime only to the owner's liege or above, under that realm's law.
    is_criminal = {
        eotg_aug_illegal_work_is_criminal = { OWNER = scope:secret_owner  VIEWER = scope:target }
    }

    # Otherwise a scandal inside a realm that bans it (secret_embezzler shape).
    is_shunned = {
        NOT = { eotg_aug_illegal_work_is_criminal = { OWNER = scope:secret_owner  VIEWER = scope:target } }
        scope:target.top_liege ?= scope:secret_owner.top_liege
        scope:target = { eotg_aug_under_policy = { LAW = ban } }
    }

    on_expose = {
        save_scope_as = secret
        # Known hardware is now known unlawful hardware: under a License,
        # refusing Demand Removal becomes a crime (eotg_aug_refusal_is_crime).
        if = {
            limit = { exists = scope:secret_target }
            scope:secret_target = {
                if = {
                    limit = { NOT = { has_character_modifier = eotg_mod_illegal_implants } }
                    add_character_modifier = eotg_mod_illegal_implants
                }
            }
        }
        else = {
            scope:secret_owner = {
                if = {
                    limit = { NOT = { has_character_modifier = eotg_mod_illegal_implants } }
                    add_character_modifier = eotg_mod_illegal_implants
                }
            }
        }
        secret_exposed_notification_effect = yes
    }
    # on_discover, on_owner_death: not set (engine default; vanilla deviant, homosexual)
}
```

```
# OWNER is answerable; VIEWER is the character judging. Vanilla scan shape:
# 00_secret_type_triggers.txt:435-447.
eotg_aug_illegal_work_is_criminal = {
    $OWNER$ = { target_is_liege_or_above = $VIEWER$ }
    NOT = { scope:secret_target ?= $VIEWER$ }          # S4, explicit (also true by R-A2)
    $VIEWER$ = {
        OR = {
            eotg_aug_under_policy = { LAW = ban }
            AND = {
                eotg_aug_under_policy = { LAW = license }
                $OWNER$ = {
                    any_secret = {
                        type = eotg_secret_illegal_augmentation
                        has_variable = eotg_aug_unlicensed
                    }
                }
            }
        }
    }
}
```

If the law moves to Tolerate or Favor, the secret stays but is inert: neither criminal nor shunned, so it is worthless for blackmail. That is correct under LAW AT 866, because the ruler's own law decides.

### 4.5 Script changes

**(1) `eotg_aug_save_answerable_effect`** (patient scope; saves `scope:eotg_aug_answerable`):
```
eotg_aug_save_answerable_effect = {
    save_temporary_scope_as = eotg_aug_answerable
    if = {
        limit = {
            var:eotg_aug_sponsor ?= { is_alive = yes }
            target_is_liege_or_above = var:eotg_aug_sponsor
        }
        var:eotg_aug_sponsor = { save_temporary_scope_as = eotg_aug_answerable }
    }
}
```

**(2) `eotg_aug_contraband_effect`** (rewrite of the head; realm.001 firing and the cooldown flag unchanged):
```
eotg_aug_contraband_effect = {
    if = {
        limit = { eotg_aug_is_contraband = yes }
        eotg_aug_save_answerable_effect = yes
        scope:eotg_aug_answerable = {
            if = {
                limit = { is_independent_ruler = no  exists = liege }
                save_scope_as = eotg_contraband_subject
                reverse_add_opinion = { target = liege  modifier = eotg_opinion_aug_contraband }
                liege = { …the existing player-liege block, unchanged… }
            }
        }
    }
    hidden_effect = { remove_variable = eotg_aug_sponsor }    # if present
}
```

**(3) `eotg_aug_give_illegal_work_secret_effect`** (patient scope). Called from the roll (step 4):
```
eotg_aug_give_illegal_work_secret_effect = {
    save_temporary_scope_as = eotg_aug_illegal_patient
    eotg_aug_save_answerable_effect = yes
    scope:eotg_aug_answerable = {
        if = {
            limit = {
                is_independent_ruler = no
                exists = liege
                NOT = { any_secret = { type = eotg_secret_illegal_augmentation } }
            }
            if = {
                limit = { this = scope:eotg_aug_illegal_patient }
                add_secret = { type = eotg_secret_illegal_augmentation }
            }
            else = {
                add_secret = { type = eotg_secret_illegal_augmentation  target = scope:eotg_aug_illegal_patient }
            }
            if = {
                limit = { scope:eotg_proc_provider ?= flag:backstreet  eotg_aug_under_policy = { LAW = license } }
                random_secret = {
                    type = eotg_secret_illegal_augmentation
                    set_variable = { name = eotg_aug_unlicensed  value = yes }
                }
            }
        }
    }
}
```
One secret per answerable party is enough. A sponsor with several augmented knights carries one secret that names the first of them. This is the embezzler "give or update" idea without the update.

**(4) `eotg_aug_procedure_roll_effect`**: after the existing hidden risk block and before the death line, in the patient scope:
```
if = {
    limit = {
        NOT = { scope:eotg_proc_kind = flag:removal }
        NOT = { scope:eotg_proc_outcome = flag:discovered }
        NOT = { scope:eotg_proc_outcome = flag:death }
        eotg_aug_is_contraband = yes
    }
    hidden_effect = { eotg_aug_give_illegal_work_secret_effect = yes }
}
```
This covers every roll caller (ruler self-installs, upgrades and repairs too). A Ban now leaves a lasting risk on all unlawful work, not only on the retainer paths.

**(5) `eotg_aug_sponsored_install_effect = { SPONSOR }`** (patient scope; run after `eotg_aug_initiate_effect`):
```
eotg_aug_sponsored_install_effect = {
    save_temporary_scope_as = eotg_aug_sponsored_patient
    hidden_effect = { set_variable = { name = eotg_aug_sponsor  value = $SPONSOR$  years = 2 } }
    custom_tooltip = eotg_aug_proc.install_tt              # existing key
    if = {
        limit = { eotg_aug_clinic_open = yes }
        hidden_effect = { eotg_aug_procedure_effect = { PATIENT = scope:eotg_aug_sponsored_patient  PROVIDER = clinic  PROCEDURE = install  SURGEON = scope:eotg_aug_sponsored_patient } }
    }
    else_if = {
        limit = { $SPONSOR$ = { eotg_aug_has_surgeon_for = { PATIENT = scope:eotg_aug_sponsored_patient } } }
        $SPONSOR$ = { eotg_aug_save_surgeon_effect = yes }
        hidden_effect = { eotg_aug_procedure_effect = { PATIENT = scope:eotg_aug_sponsored_patient  PROVIDER = physician  PROCEDURE = install  SURGEON = scope:eotg_proc_surgeon } }
    }
    else = {
        hidden_effect = { eotg_aug_procedure_effect = { PATIENT = scope:eotg_aug_sponsored_patient  PROVIDER = backstreet  PROCEDURE = install  SURGEON = scope:eotg_aug_sponsored_patient } }
    }
}
```
- `eotg_aug_retainer_install_effect` gains `eotg_aug_sponsored_install_effect = { SPONSOR = root }` after its initiate line. This covers init.020 a, b and c.
- init.020 d's inline block gains the same line after `eotg_aug_initiate_effect`.
- nr.001 a, c and d gain it in `scope:eotg_champion` after their initiate line (root = the liege). In c the knight pays, but the liege granted it, so the liege is the sponsor.
- `eotg_aug_retinue_install_effect` gains it after its initiate line (callers run it in knight scope with root = the ruler).
- If the outcome is death (back streets only), the knight dies on the table, as on every other back-street install. The existing `after` and Retinue starts read `any_knight` and so already tolerate it.

**(6) `eotg_aug_offer_install_effect`** gains, in `scope:recipient` and before its roll: `hidden_effect = { set_variable = { name = eotg_aug_sponsor  value = scope:actor  years = 2 } }`. Nothing else changes.

**(7) realm.001**: one `triggered_desc` in the desc block for a subject who ordered the work rather than received it: `triggered_desc = { trigger = { scope:eotg_contraband_subject = { eotg_is_augmented_any = no } } desc = eotg_aug_realm.001.desc_ordered }`. Option b already hides for an unaugmented subject (its `has_trait = eotg_cybernetics` condition), so a and c remain.

### 4.6 Loc surface (I2a)

| Key | Note |
|---|---|
| `eotg_secret_illegal_augmentation` | Name. Suggested: "Unlawful Implant Work" |
| `eotg_secret_illegal_augmentation_desc` | Use vanilla data contexts as in `G/localization/english/secrets_l_english.yml:48, 107` (`[TARGET_CHARACTER.GetShortUIName]`). One key serves both cases (with and without a target). The localizer copies the vanilla shape of a targetless secret (`secret_deviant_desc`) and checks in game that the target form renders. |
| `eotg_secret_illegal_augmentation_tooltip_desc` | `[CHARACTER.GetShortUINameNoFormat\|U]` form, as `:76` |
| `eotg_secret_illegal_augmentation_type_desc` | as `:94` |
| `eotg_aug_realm.001.desc_ordered` | "word has reached you" that the subject *had* implant work done on someone at their court, outside the law |

No vanilla string needs a `replace/` override.

### 4.7 Tests

- **V-IR1** (Ban, vassal): a vassal count under a top-liege Ban takes init.020 a. The roll uses a physician or the back streets, never the clinic. If clean, the vassal (not the knight) holds `eotg_secret_illegal_augmentation` with target = the knight. The top liege's spymaster on Find Secrets can surface it. Once exposed, the top liege can imprison the **vassal**, and the knight gains `eotg_mod_illegal_implants`.
- **V-IR2** (S4): a liege under a Ban Offers implants to a courtier through the back streets, forced to `discovered` (console or reloads). The liege gets **no** Unlawful Implants opinion on the courtier and no realm.001. If the liege is a vassal, *their* liege gets the opinion on them, and realm.001 shows `desc_ordered`.
- **V-IR3** (Q1.4): an independent ruler under their own Ban augments a knight. No secret, no opinion.
- **V-IR4** (Tolerate): init.020 a rolls the clinic column. No secret ever.
- **V-IR5** (License): back-street self-install by a vassal. The secret carries `eotg_aug_unlicensed`. A clinic install under License leaves nothing.
- **V-IR6** (removal): full removal of a secret's patient. The secret drops (`is_valid` fails).
- **V-IR7** (AI, observer run): over 20 years under a Ban, knight initiations fall by about half or more against Tolerate (the realm spec §9.2 observer counter 2, split by law).
- **V-IR8** (static): `grep -n "eotg_aug_initiate_effect" events/eotg_augmentation_initiation.txt events/eotg_augmentation_nonruler.txt common/scripted_effects/eotg_augmentation_effects.txt`. Every hit in init.020, nr.001, the retainer, retinue and offer effects is followed in the same block by `eotg_aug_sponsored_install_effect` or a roll.
- **G-check:** the engine grants an imprisonment reason for an exposed secret that is `is_criminal` to the imprisoner (game concept text says so). Confirm in V-IR1, with error.log clean.

---

## 5. I2b: presence and pacing guards

### 5.1 S2: the physician must have the patient in hand

**Rule.** A procedure or Examine by the **actor's own hands** (physician or Implant Technician, own or borrowed) needs the patient **at the actor's court**: a courtier, a pool or foreign-court guest, or the actor's prisoner. The patient must also be available (not travelling, not in an activity, not commanding). Prisoners are exempt from `is_available`, because a dungeon is local. **Clinic and back-street sends stay remote.** The patient goes to them in their own realm.

The surgeon side is unchanged. A borrowed technician "will see to your implants for a year" without moving (realm lore R8). That is a lore conceit, and it is kept.

**Vanilla:** `G/common/character_interactions/06_ep3_interactions.txt:4461-4476`: the court physician operates only on a courtier or guest (`is_courtier_of` / `is_pool_guest_of` / `is_foreign_court_guest_of`) who `is_available = yes`.

**Changes** (`common/character_interactions/eotg_augmentation_interactions.txt`):

| Where | Add |
|---|---|
| Offer, `send_option` physician (`flag = eotg_aug_provider_physician`), `is_valid` | `custom_description = { text = eotg_aug_patient_present_tt  scope:recipient = { eotg_aug_patient_at_court_of = { ACTOR = scope:actor } } }` and `scope:recipient = { is_available = yes }` |
| Demand Removal, the same send option | the same two lines |
| Examine, `is_valid_showing_failures_only` (new block) | `scope:recipient = { custom_description = { text = eotg_aug_patient_present_tt  eotg_aug_patient_at_court_of = { ACTOR = scope:actor } } }`, and `trigger_if = { limit = { scope:recipient = { is_imprisoned_by = scope:actor } } always = yes } trigger_else = { scope:recipient = { is_available = yes } }` |
| Examine `ai_accept` comment | "Vassals, spouses and family at other courts" becomes "guests". The modifiers stay. |

New trigger in `common/scripted_triggers/eotg_augmentation_triggers.txt`:
```
# The patient is in the actor's hands (S2; vanilla 06_ep3_interactions.txt:4461-4476)
eotg_aug_patient_at_court_of = {
    OR = {
        is_courtier_of = $ACTOR$
        is_pool_guest_of = $ACTOR$
        is_foreign_court_guest_of = $ACTOR$
        is_imprisoned_by = $ACTOR$
    }
}
```

**Consequence, accepted:** Examine on a landed vassal now needs them as a guest, for example at a feast. That is "physical and local" (interactions spec §7 register; lore I5/I6).

**Loc:** `eotg_aug_patient_present_tt`, e.g. "[recipient.GetFirstName] is not at your court". The vanilla `COURTIER_OR_GUEST` key is not reused, because ours also admits prisoners.

**Tests.**
- **V-IR9:** Offer to a spouse living at another court: the physician option is greyed with the new tooltip, and the clinic and back streets still work.
- **V-IR10:** Examine a courtier who is away travelling: invalid. Examine a prisoner: valid.

### 5.2 C3: the Intervention needs a cooldown

**Rule.** tier3.020 fires at most once per **2 years** per ruler, whatever the answer. The cooldown lives in the two firing sites only (invariant 4). The existing `eotg_flag_aug_intervention_refused` stays as the "refused" state the Heir's Arc reads.

| Site | Change |
|---|---|
| `eotg_on_yearly_aug_overclocked_check`, the Intervention entry (`common/on_action/eotg_augmentation_on_actions.txt`, weight 30) | trigger gains `NOT = { has_character_flag = eotg_flag_aug_intervention_cd }`; effect gains `add_character_flag = { flag = eotg_flag_aug_intervention_cd  years = 2 }` |
| `eotg_story_aug_countdown`, branch 7b (`common/story_cycles/eotg_augmentation_stories.txt`) | trigger gains `story_owner = { NOT = { has_character_flag = eotg_flag_aug_intervention_cd } }`; effect gains the same flag on `story_owner`. While it is blocked, stage 4 holds and the next tick retries. |

tier3.020's own `trigger` reads neither flag.

**Identifiers:** `eotg_flag_aug_intervention_cd` (character flag, 2 years).

**Vanilla:** cooldown flags set in the firing pulse, as the mod's own house rule (lesson 5) and every vanilla yearly pool, e.g. `G/common/on_action/yearly_on_actions.txt`. The neighbouring entries in the same list already do it (`eotg_flag_oc_event_cooldown`).

**Test V-IR11:** a ruler at risk 45 accepts tier3.020 (a). With the console, force a pulse and a Countdown tick in the same year: no second tier3.020 for 2 years.

### 5.3 C4: the inherit lock expires

**Rule.** The lock variable itself carries the 6-year timeout the spec intended. The written-but-unread safety flag is retired.

| Where | Change |
|---|---|
| `eotg_aug_inherit_start_effect` | first line: `eotg_aug_inherit_close_effect = yes` (a clean slate, so stale `eotg_inh_*` state from an expired tree never leaks). `set_variable = { name = eotg_inh_heir  value = scope:eotg_inh_heir }` becomes `… years = 6 }`. Delete `add_character_flag = { flag = eotg_flag_aug_inh_active  years = 6 }`. |
| `eotg_aug_inherit_close_effect` | delete `remove_character_flag = eotg_flag_aug_inh_active` |
| `cybernetics_v2_fracturing_inheritance.md` §table, line 131 | the orchestrator notes that the flag is retired by this ruling |

The guards (`NOT = { has_variable = eotg_inh_heir }` at four on_action sites and in `eotg_aug_inherit_can_start`; `var:eotg_inh_heir ?= root` in the non-ruler pulse) need no change. An expired variable reads as absent.

**Vanilla:** timed variables, `set_variable = { … years = }`, `G/common/story_cycles/story_cycle_party_baron.txt:116-120` (already cited in the mod's Retinue story).

**Test V-IR12:** start a tree (debug effect), then advance 6 years without closing it (`eotg_inh_force` or a skipped leaf). `eotg_inh_heir` is gone. The ruler can start the Heir's Arc, and the tree again after its 3-year cooldown.

### 5.4 C6: an end state for the deposed Neurofractured

**Rule.** For an abdicated ruler, **Into Restraints is the end state**: they are held, and the hardware is held still. Their risk freezes at its value at abdication.
- `eotg_aug_abdicate_effect` also sets `add_character_flag = eotg_flag_aug_restrained` with no duration, matching its permanent `eotg_mod_aug_restrained`. Every restraint reader then treats them as restrained if they ever hold land again.
- `eotg_on_yearly_aug_nonruler_check` step 4 ("Drift once fractured") gains `NOT = { has_character_flag = eotg_flag_aug_abdicated }` in its limit.

Step 5 (liege events about them) stays. The heir still gets "Something Is Wrong With Them" about the parent at court, which is the point of the beat.

*Why not a terminal event:* that is a new event (owner rule; see §13).

**Vanilla:** none directly. The precedent is the mod's own treatment rows (`eotg_aug_nf_drift_value`, "Restraints −4"). The ruler rule "slowed, never paused" is for a ruler under pressure. A deposed, restrained ex-ruler is outside that loop by design.

**Test V-IR13:** end.030 (a) abdication. Five yearly pulses later the ex-ruler's `eotg_fracture_risk` is unchanged, and `has_character_flag = eotg_flag_aug_restrained` is set.

### 5.5 C7: pause the Heir's Arc

**Rule.** A landless owner **pauses** the arc. It ends (spent, `eotg_flag_aug_heir_arc_done`) only on abdication, or after **3 paused ticks** (about 6 years at `years = {1 2}`, `chance = 70`).

Replace the first branch of `eotg_story_aug_heir_arc`'s `first_valid` with two branches:
```
triggered_effect = {
    trigger = { story_owner = { has_character_flag = eotg_flag_aug_abdicated } }
    effect = {
        story_owner = { add_character_flag = eotg_flag_aug_heir_arc_done }
        end_story = yes
    }
}
triggered_effect = {
    trigger = { story_owner = { is_landed = no } }
    effect = {
        change_variable = { name = eotg_paused_ticks  add = 1 }      # starts absent = 0
        if = {
            limit = { var:eotg_paused_ticks >= 3 }
            story_owner = { add_character_flag = eotg_flag_aug_heir_arc_done }
            end_story = yes
        }
    }
}
```
A matching branch with no stage change is the wait. The counter is cumulative across separate landless stints, which bounds total pausing.

**Identifiers:** story variable `eotg_paused_ticks`. Add it to the story-variable list in the file header.

**Vanilla:** the end shape is `G/common/story_cycles/story_cycle_take_mandate_of_heaven.txt:172-189`. The wait shape is the admin eunuch re-target tick, `G/common/story_cycles/ep3_story_cycle_admin_eunuch.txt:145-182` (already cited by the same story's branch 0b, "an heir under 14 is waited for").

**Test V-IR14 (G):** a landed NF ruler with a running arc loses all titles (console `remove_title`), then regains a county within 2 ticks. The arc resumes at its stage. An end.030 abdication still ends it.

### 5.6 C8/C9: children don't climb, and knights settle

**Rules.**
- **C8.** Adulthood gates progression and the Countdown. Add `is_adult = yes` to `eotg_can_progress_to_enhanced` and `eotg_can_progress_to_overclocked` (`common/scripted_triggers/eotg_augmentation_triggers.txt:88-107`), and to the `limit` of `eotg_aug_try_start_countdown_effect` (one place covers its three callers). The Pursue decision already needs `is_available_adult`.
- **C9.** Non-rulers honour the settling floor. In `eotg_on_yearly_aug_nonruler_check` step 2, the progression `if` limit gains `NOT = { has_character_flag = eotg_flag_aug_settling }`. `eotg_aug_initiate_effect` and `eotg_aug_set_integration_effect` already set the flag on everyone.

A tier-3 child (via an inherited title) keeps their tier. This rule only stops further climbing and a new Countdown.

**Vanilla:** age gates in pulses, `G/common/scripted_triggers/00_available_for_events_triggers.txt:802-810` (the availability family already used by I1 C1).

**Tests.**
- **V-IR15:** a 10-year-old tier-1 ruler with dev ≥ 15 never progresses until 16.
- **V-IR16:** a knight installed through nr.001 cannot reach tier 2 inside 5 years. Console: force `eotg_aug_nr_progress_chance` to 100 and check.

### 5.7 C10: Iron Retinue membership is per court

**Rule.** `eotg_flag_aug_iron_retinue` and `eotg_flag_aug_retinue_permanent` mean "in this court's Program". They are removed when the knight leaves the court, and from the owner's knights when the owner dies. The heir never ran the Program.

| Where | Change |
|---|---|
| `common/on_action/eotg_augmentation_on_actions.txt` | additive: `on_leave_court = { on_actions = { eotg_on_leave_court_aug } }`. New `eotg_on_leave_court_aug = { trigger = { OR = { has_character_flag = eotg_flag_aug_iron_retinue  has_character_flag = eotg_flag_aug_retinue_permanent } } effect = { remove_character_flag = eotg_flag_aug_iron_retinue  remove_character_flag = eotg_flag_aug_retinue_permanent } }` |
| `eotg_story_aug_retinue` `on_owner_death` | before `end_story`: `story_owner = { every_knight = { limit = { eotg_aug_is_retinue_knight = yes } remove_character_flag = eotg_flag_aug_iron_retinue  remove_character_flag = eotg_flag_aug_retinue_permanent } }` |

**Vanilla:** `G/common/on_action/court_maintenance_on_actions.txt:34-38` (`on_leave_court`: root = the character, `scope:old_employer`; fires before `on_join_court`). It has a top-level `effect`, so ours **must** be the additive `on_actions = { }` form (invariant 4).

**Test V-IR17 (G):** a retinue knight who leaves for another court (console `move_to_pool` or a release) loses both flags, and `eotg_aug_nr_progress_chance` reads 10 for them. Also confirm whether `every_knight` still lists the knights inside `on_owner_death`. If it does not, drop the second row and rely on `on_leave_court` firing during the court hand-off. The orchestrator records which.

**Owner:** scr (as the report's Owner column). This is a mechanical item placed in I2b for one QA pass.

### 5.8 Loc surface (I2b)

`eotg_aug_patient_present_tt`. No other keys.

---

## 6. I2c: Frontier sponsorship terms (F2)

### 6.1 Rules

A sponsorship is an arrangement between a **sponsor** and **the holder who accepted it**. It lapses (strain cause `sponsor_lapsed`, the existing toast to the holder) when any of these hold at the Region's yearly tick:
1. The sponsor is **imprisoned**, or **no longer a landed count or above**.
2. The sponsor is **at war with the holder**.
3. **The holder changed, and the old holder is still alive** (conquest, revocation, grant away). If the old holder died (inheritance), the arrangement passes to the new holder and the record updates.
4. (Existing.) The sponsor died, or became the holder.

`.010`, the Sponsor decision's `is_shown` and `.003`'s trigger offer no Region whose holder is at war with the would-be sponsor. `eotg_frontier_can_sponsor` also needs `is_imprisoned = no`.

**The completion reward reads the same validity.** `eotg_frontier_has_valid_sponsor` is tightened, so every reader (the pay effect, the completion branch at `common/scripted_effects/eotg_frontier_effects.txt:1335`, and the event triggers that list it) agrees without per-site edits.

### 6.2 Vanilla precedent

- War voids a backing: `G/common/great_projects/types/01_pam_projects.txt:5551-5561` (a contribution location is invalid while its top liege is `is_at_war_with` or `has_truce` with the founder).
- Imprisonment voids action: `G/common/schemes/scheme_types/befriend_scheme.txt:50-57`.
- The tick as the only cadence authority: the existing `eotg_frontier_check_sponsor_effect` (`:833`), run before `eotg_frontier_sponsor_pay_effect` (`:739-740`).

### 6.3 Changes

| Where | Change |
|---|---|
| `eotg_frontier_has_valid_sponsor` (`common/scripted_triggers/eotg_frontier_triggers.txt:144`) | becomes: `exists = var:eotg_frontier_sponsor`; `var:eotg_frontier_sponsor = { is_alive = yes  is_imprisoned = no  is_landed = yes  highest_held_title_tier >= tier_county }`; `holder ?= { NOT = { is_at_war_with = prev.var:eotg_frontier_sponsor } }` (`prev` = the county, as `eotg_frontier_faiths_differ` already does) |
| `eotg_frontier_can_sponsor` | add `is_imprisoned = no` |
| `eotg_frontier_set_sponsor_effect` | after `set_variable eotg_frontier_sponsor`: `set_variable = { name = eotg_frontier_sponsor_holder  value = holder }` |
| `eotg_frontier_drop_sponsor_effect` | also `remove_variable = eotg_frontier_sponsor_holder` (if present) |
| `eotg_frontier_check_sponsor_effect` | after the two existing branches, add: **(a) backfill/inheritance:** if `var:eotg_frontier_sponsor` exists and (`NOT = { has_variable = eotg_frontier_sponsor_holder }` or the recorded holder `is_alive = no`), set the record to `holder`. **(b) lapse:** `else_if` the sponsor exists and (`eotg_frontier_has_valid_sponsor = no` or (`NOT = { var:eotg_frontier_sponsor_holder = holder }` and the recorded holder is alive)) → save `eotg_frontier_lapsed_sponsor`, `eotg_frontier_clear_sponsor_effect`, `eotg_frontier_add_strain_effect = { CAUSE = sponsor_lapsed }`, the existing holder toast `eotg_frontier_toast_sponsor_lapsed`. Order: dead → became holder → (a) → (b). |
| `.010` immediate, the three `ordered_in_global_list` limits; the Sponsor decision `is_shown` list | add `holder ?= { NOT = { is_at_war_with = root } }` |
| `.003` `trigger` | add the same world-state test between the offering sponsor and root (the holder): `NOT = { is_at_war_with = scope:eotg_frontier_sponsor }` |

**Identifier:** county variable `eotg_frontier_sponsor_holder`. Save-compatible: a missing record is backfilled by (a).

**Loc:** none. The `sponsor_lapsed` cause, its band tooltip and .005's lapse descs already exist.

### 6.4 Tests

- **V-IR18:** A sponsors B's Frontier; A declares war on B. At the next tick: the lapse toast and strain; no payment that year; no completion reward to A.
- **V-IR19:** C conquers the county. At the next tick the sponsorship lapses.
- **V-IR20:** B dies and B's heir inherits. The sponsorship continues, and `eotg_frontier_sponsor_holder` is the heir.
- **V-IR21:** A is imprisoned: lapse. `.010` for an at-war ruler lists none of the enemy's Frontiers.

---

## 7. I2d: kingpin under a Cartel (X2, OWNER RULING 2026-10-20: make it rarer)

### 7.1 Ruling

The owner chose to make it rarer, not to gate it: under a Cartel ruler the kingpin chain starts at **half** the rate. The fiction is **a rival boss moving in** on the ruler's own ground.

| Where | Change |
|---|---|
| `eotg_on_yearly_aug_kingpin_check` (`common/on_action/eotg_aug_kingpin_on_actions.txt`), the `2 = { … }` entry | add `modifier = { factor = 0.5  government_has_flag = eotg_government_is_cartel }` (the government flag, never a government key). The existing ×1.5 under a Ban still stacks. |
| `eotg_aug_kingpin.001` desc | prepend one `first_valid` group with a single `triggered_desc = { trigger = { government_has_flag = eotg_government_is_cartel } desc = eotg_aug_kingpin.001.desc_rival_boss }`. It is a framing line placed before the existing reporter, kind and method lines, and adds no option. |

The `kind` weights (crew, syndicate, front, hired) are unchanged. **The syndicate kind stays Patron-only**, and a Cartel is never read as one of the canon syndicates (governments_v2 §264, LQ6).

**Vanilla precedent:** government-flag weight modifiers, e.g. `G/common/scripted_rules/01_grant_title_rules.txt:39-42` (the flag test). Weighted `random_list` modifiers in the same on_action already follow the vanilla shape.

### 7.2 Dread and Cartel G2 tribute retention: no clamp

The kingpin's beats add dread directly (`add_dread` 5–30 per beat; `events/eotg_augmentation_kingpin.txt`, the largest is +30 at `.066.b`; `eotg_aug_kingpin_effects.txt:1192` +10). Under a Cartel:
- **The Cartel's `dread_gain_mult = 0.25` applies**, so +30 becomes +37.5.
- **G2 retention reads raw dread.** Payers walk below `low_dread` 20 (G2 §5.4). A kingpin beat therefore **delays walk-off and funds** Put on the Schedule and Tighten (G2 §2.3, §4).
- **The effect is transient.** Kingpin dread is not baseline (`dread_baseline_add` comes only from payers, G2 §2.7). It decays at 0.375 a month under G2's corrected `dread_decay_mult = -0.25`, so +37.5 fades in about 8 years.
- **It is bounded.** The kingpin is once per life (`eotg_flag_aug_had_kingpin`), now half as likely for a Cartel, and the engine clamps dread at `max_dread`.

**Ruling: accept, no clamp.** G2 §2.1–2.3 already made dread a universal currency: other systems write it directly, and the authority rule covers Cartel files only. Crushing a rival boss makes payers fear you more, which is the coherent reading. This item is closed for CB-57 Q8. **No change to G2.**

### 7.3 Loc, tests

**Loc:** `eotg_aug_kingpin.001.desc_rival_boss` (one line: someone has set up on your ground and does not pay you). Lore-keeper reviews it against LQ6.

**Tests.**
- **V-IR22 (static):** `grep -n "eotg_government_is_cartel" common/on_action/eotg_aug_kingpin_on_actions.txt` finds one hit. Grep for `eotg_cartel_government` in the same file finds none (flag, not key).
- **V-IR23:** on the British Isles test sub-mod, a Cartel ruler forced into kingpin.001 (console) sees the rival-boss line first. A PMC ruler does not.

---

## 8. F8/X6: Local Ruler government under a mod-government liege (record; nothing built)

**Finding.** `eotg_frontier_grant_local_ruler_effect` always uses `republic_government` (city) or `theocracy_government` (church).

**Ruling: correct for now, and vanilla-consistent.** A Local Ruler is a **barony** holder. Vanilla gives city barons a republic and church barons a theocracy under any liege. The governments spec already records that city baronies in a PMC realm get republic burghers "as in a feudal one" (`governments_v2.md` §131, V-G20). Under Frontier A1 (`frontier_v4.md`):
- Corporation and Gob-Corp holders (city-primary) keep the Port themselves, so no Local Ruler is created for them.
- Only PMC, Cartel and feudal holders hand a city to a local, and the republic burgher is the vanilla answer.

**What can be done now:** nothing to build. Building a picker now would be a dead branch (robustness plan F5). **Later trigger:** if G2 defines a **barony-tier** mod government (for example a Corporation branch office under a PMC), the one change is a liege-flag ladder for `LOCAL_GOVERNMENT` at the two call sites (`common/scripted_effects/eotg_frontier_effects.txt` settlement/trade/religious branches). It reads `top_liege = { government_has_flag = eotg_government_is_<gov> }`. The orchestrator keeps this under CB-60 as frontier_v4 D4-4.

**Test:** report §3 "F8" in-game check (the contract of a Local Ruler under a mod-government liege). No V-IR.

## 9. P1: `government_is_feudal` (OWNER RULING 2026-10-20: keep them distinct)

**Ruling.** No mod government sets `government_is_feudal`. PMC, Corporation, Cartel and Gob-Corp keep their identity flags only.

**What the flag would have unlocked** (vanilla 1.20.1.1, 370 reads in about 90 files):

| Category | Reads (approx.) | Examples |
|---|---|---|
| Cosmetic titles and loc | ~160 | `common/council_positions/00_council_positions.txt` (92, council names by tier), `common/customizable_localization/00_es_custom_loc.txt` (54), `10_ach_custom_loc.txt` (13), accolade names (4), clothing (3), event backgrounds, CoA |
| Vassalage and contracts | ~35 | `offer_vassalization_interaction` / `offer_fealty_interaction` (15: low/medium/high starting obligations, religious-exemption AI), `special_contracts.txt` (10: scutage, march), `feudal.txt` / `nomad.txt` contracts (8), `tributary_war_participation_obligation` |
| Succession laws | ~20 | single-heir, partition and elective laws (`00_law_triggers.txt` 8; `01_title_succession_laws.txt` 6, e.g. `feudal_elective_succession_law`) |
| Government conversion decisions | ~25 | `convert_to_feudalism_*`, `convert_feudalism_to_clan_*`, major decisions (`80_major_decisions.txt` 7) |
| Activities and lifestyle events | ~30 | hold-court petitions (13), coronation (5), stewardship duty, wealth and domain events (8) |
| Realm traditions, council tasks, misc. | ~25 | `tradition_castle_keepers`, `_city_keepers`, `_hereditary_hierarchy`; kurultai and chancellor tasks; seize-realm scheme; tribal development penalty |

**Consequence, accepted.** The four governments miss the cosmetic tier titles (covered by their own flavorization), vanilla vassalization obligations, the vanilla succession-law menu (each already has its own law, governments_v2 §370), and some hold-court and stewardship flavour. In return, no vanilla feudal content mis-fires on them, and their identity stays clean.

**Suggestions only (hand-ports to consider in G2; nothing approved):**
1. Starting-obligation send options on vassalization towards a mod-government recipient (`00_character_interactions.txt:401-430` shape).
2. A scutage-like special contract per government's own `vassal_contract_group` (`special_contracts.txt` shape).
3. An elective succession law per government (already planned: governments_v2 §368).
4. The two realm traditions `tradition_castle_keepers` / `_city_keepers` widened by a culture-side check, if the playtest misses them.

## 10. Notes S7, S8, S9, S13 (accepted; nothing built)

| ID | Ruling | Reason / precedent |
|---|---|---|
| **S7** Ban opinion reaches only direct vassals and courtiers | **Accept.** | The opinion lands on those who can act on the lawmaker: direct vassals (factions) and courtiers. Deeper vassals react through their own liege. The law's vassal-stance AI (realm spec §4.1) already reads the whole realm. |
| **S8** A realm that breaks free starts on Tolerate | **Accept (G).** | A new independent ruler holds their own realm laws at the group default (`eotg_aug_policy_laws`, `default = eotg_aug_policy_tolerate`), as vanilla realm law groups do. LAW AT 866: the new top ruler sets their own law. Report §3 "S8" confirms it in game. |
| **S9** Demand Removal can't use a clinic under a Ban | **Accept, by design.** | Realm spec §3.2: sanctioned clinics do not operate under a Ban, for any purpose. Physician and back streets remain (the physician needs presence after S2). |
| **S13** The Patron debt dies with its owner | **Accept; existing deferral.** | `cybernetics_v2_reprisal.md` §171, §369 and phase5 §5: inherited debt stays deferred. |

---

## 11. Lore constraints

- **LAW AT 866** (SETTING LORE ERRATA; `REVIEW_866.md`): every law is the realm's own ruler's. Q1.1–Q1.6 (`cybernetics_v2_realm_lore.md`) bind I2a. The answerable party's own liege acts, inside the realm, with no apparatus. Discovery is hearsay. The lawmaker is never a criminal under their own law. Nothing reaches outside the realm. The secret's loc must not say register, record, warrant, authority, inspector or permit. The grep `authorit|warrant|magistrat|inspector|registry|permit|regulat` must be empty on the new keys.
- **Physical and local** (interactions lore I5/I6; interactions spec §7, §834): S2's presence rule. A secret exists because evidence lives in a body (`is_valid` drops on removal). Never a log, scan or signal.
- **Favor is regard, not provision** (realm lore Q2): unaffected.
- **Kingpin** (`cybernetics_v2_kingpin.md` §5.2.1; governments_v2 §264, LQ6): a Cartel is never a canon syndicate. Never name Blackstar, Shadow Markets, Black Contracts, Blackline, P&D, Calix, the Pill Mob or the Concrete Cartel. The rival boss stays unnamed.
- **Canadian English** for every new string.
- **Route to eotg-lore-keeper:** the four secret strings, `eotg_aug_realm.001.desc_ordered`, `eotg_aug_kingpin.001.desc_rival_boss`, `eotg_aug_patient_present_tt`.

## 12. Definition of done

1. Tiger, `px_lsp_diagnostics.js` and `px_vocab_check.py` are clean on the touched files, except the CLAUDE.md known-benign list. Tiger 1.17 may not know some secret-type fields. Check any finding on `common/secret_types/` against `_secret_types.info` and `00_secret_types.txt` before calling it real.
2. **I2a:** V-IR1–V-IR8 pass. `grep -rn "add_secret" common events` finds only `eotg_aug_give_illegal_work_secret_effect`. The secret type has all four loc keys (PX loc coverage).
3. **I2b:** V-IR9–V-IR17 pass. `eotg_flag_aug_inh_active` has 0 hits. `eotg_flag_aug_intervention_cd` is set only in the overclocked on_action and the Countdown story (cooldown authority grep). No event `trigger` reads it.
4. **I2c:** V-IR18–V-IR21 pass. `eotg_frontier_sponsor_holder` is written only by the set, drop and check effects.
5. **I2d:** V-IR22–V-IR23 pass. Lands before Cartel G2 C2 (orchestrator checks the order on CB-57).
6. **No new event, option or `namespace`** in any batch: `git diff --stat` shows no new `= {` event ids, and PX's event graph count is unchanged.
7. Map-agnostic: `grep -nE "(title|province|culture|faith|character):[a-z]" ` on the touched lines is empty.
8. Taskboard: CB-57 Q8 closed (§7), P1 closed (§9), F8/X6 kept under CB-60 as D4-4 with the later trigger (§8).

## 13. Deferred and suggestions (owner's call; not in any batch)

- **Ruler-side installs without a roll.** 14 sites call `eotg_aug_initiate_effect` with no procedure roll nearby, for example init.004 (desperation, accepted in realm spec §4.2), init.007, init.013, init.017, the Patron reinstalls (patron.005/.008/.009), heir.005, and tier1.004/.015/.018. They are outside S1, which is about retainers and knights. QA should list each one with its documented reason. Any site without a reason becomes an S1 follow-up that uses `eotg_aug_sponsored_install_effect`.
- **Suggestion:** a terminal beat for a Neurofractured non-ruler at risk 100 (today they sit at the clamp). This would be a new event.
- **Suggestion:** a "fine paid" path that clears the secret, mirroring realm.001 c. This would be a new option.
- **Suggestion:** a sponsor-side toast when F2 lapses a sponsorship (today only the holder is told). This would need a new loc key and send; small, but it is a new beat.
- **Integration ranks 1–2** (decision alerts, game concepts) and ranks 4–5 (memories, game rules) are outside this ruling pass (report §5).
- **G-checks carried:** the S8 law on independence; V-IR14 and V-IR17 engine behaviour; the exposed-secret imprisonment reason (V-IR1).

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Build batch I2a (S1/S4 and the new secret type) from docs/specs/investigation_rulings_2026-10-18.md §4, then I2b (§5), I2c (§6) and I2d (§7, before Cartel G2 C2); no new events or options.
- files: docs/specs/investigation_rulings_2026-10-18.md
- needs-loc: eotg_secret_illegal_augmentation, _desc, _tooltip_desc, _type_desc; eotg_aug_realm.001.desc_ordered; eotg_aug_patient_present_tt; eotg_aug_kingpin.001.desc_rival_boss
- needs-lore: review the seven new strings against Q1 (no apparatus, hearsay), I5/I6 (physical evidence) and LQ6 (the rival boss is not a canon syndicate)
- needs-human: none to start. The in-game G-checks V-IR1 (exposed-secret imprisonment reason), V-IR14, V-IR17 and S8 go into the session plan. The orchestrator adds `common/secret_types/` to the CLAUDE.md placement list and closes CB-57 Q8 and P1.
