# Cybernetics v2: the syndicate's reprisal (the paper is sold)

**Author:** eotg-architect, 2026-10-04
**Authorised by:** the human, relayed by the coordinator 2026-10-04 ("proceed"). This is new content. It closes the open question in [cybernetics_v2_new_beats.md](cybernetics_v2_new_beats.md) §10, which is also recorded in [cybernetics_v2_phase5.md](cybernetics_v2_phase5.md) §2.4 (cost table) and §5.
**Index:** [cybernetics_v2.md](cybernetics_v2.md). Index §1 rules 1–12 and the §5 lore register apply.
**Lore review:** approved 2026-10-04 with must-fixes P1–P7 and ruling U1, all folded in below. The verdict and its renderings are in [cybernetics_v2_reprisal_lore.md](cybernetics_v2_reprisal_lore.md), which is **binding** for script and loc (§7, §8).
**Checked against:** the **committed** Patron script at `6c64f2c` (db0c550 and later): `events/eotg_augmentation_patron.txt` (.006 at :800-969, .008 at :1088-1255), `eotg_story_aug_patron` in `common/story_cycles/eotg_augmentation_stories.txt` (:480-…, both cadences), `eotg_aug_patron_betray_effect` in `common/scripted_effects/eotg_augmentation_effects.txt` (:1420-1438), `eotg_aug_patron_envoy_present` in `common/scripted_triggers/eotg_augmentation_triggers.txt` (:360-365), `eotg_aug_patron_envoy_template` in `common/scripted_character_templates/eotg_augmentation_templates.txt`. Line numbers are as of that commit and are for orientation only (index §1 rule 12).
**Builds on specs, not unbuilt script:** [procedures](cybernetics_v2_procedures.md) (patron installs are **not rolled**, procedures §4.5 table "Not rolled"), [interactions](cybernetics_v2_interactions.md) and [realm](cybernetics_v2_realm.md). This spec uses nothing from those three that is not yet built. It only has to land after them because they edit the same effects, stories and loc files (§4, build order).

**Size.**
- **1 new event** (patron.009). Below the 3-event flag; no further yes needed.
- 1 new option on an existing event (patron.006 f).
- 1 new scripted effect, 1 new story variable, 1 changed scripted effect (`eotg_aug_patron_betray_effect` gains an `else` branch), 1 changed `after` block (.006), 1 new tick entry per Patron cadence.
- 13 loc keys.
- No new modifier, opinion, trait, decision, on_action, namespace, scheme type, character template, icon or art. The murder scheme is vanilla's.

---

## 1. Purpose & gate

When a ruler betrays the syndicate, the built script punishes the **hardware**: the firmware throttle, risk +25, and the Countdown at Overclocked. Three cases slip through it (new_beats §10):

- **(a)** An owner with no implants (after patron.008 d "The paper is worth nothing now", or any removal) who betrays at .006. The only cost is the envoy's murder.
- **(b)** The envoy is dead or gone when .006 fires, and the owner is not deceitful. c and e need the envoy, and d is deceitful-only, so there is **no betrayal route**: only sign (a) or buy out (b).
- **(c)** An owner with no implants, no envoy present, whose .006 d [deceitful] fails. The betray effect neither kills (no envoy) nor punishes (no hardware). The only cost is the lie stress.

**The answer: the syndicate sells the paper.** None of its hardware is left in the ruler to stop servicing, and there is no authority to appeal to (LAW AT 866), so it acts through people. A betrayal that leaves the syndicate without a firmware lever does not end the debt. The story stays alive, and on its next tick a **collector** arrives in person. The collector holds the paper and has people. The ruler pays, signs, takes the stock that came with the paper against the debt (a sale, P7), refuses, or (if wrathful) seizes the collector. A refusal, or a failed seizure, starts a **vanilla murder scheme** by the collector against the ruler: agents, physical and local, discoverable by vanilla's spymaster machinery.

Case (b) also needs a route: **.006 f "Burn the terms. Send no answer."** It is a universal defiance option, shown only when the envoy is absent. It calls the same betray effect. An augmented owner gets the firmware throttle; an owner with no implants gets the collector.

**Gate 3 (Systems), on the temporary map** (`docs/agent_workflow.md` §5 rule 2; `CLAUDE.md` mod-exclusive exception). **Not blocked.** No title, province, character, culture or faith keys. The collector is created from the envoy template with `root.culture` / `root.faith` by scope (index §1 rule 9).

---

## 2. Signature resource

The system's signature is **`eotg_fracture_risk` plus tier** (index §1 rule 4). The owner this spec targets has **no implants**, so the risk variable does not exist and must not be recreated (QA round 2 M3). The human's allowance for that owner, from new_beats §2, applies: **the Patron debt itself (the story and its state) and the tier**.

| Piece | How it couples |
|---|---|
| .006 f | Calls `eotg_aug_patron_betray_effect`. For an augmented owner: throttle, **risk +25**, Countdown at tier 3. For an owner with no implants: sets the story's `eotg_paper_sold`, which keeps the debt alive. |
| Betray effect, new `else` | Moves the debt's state (`eotg_paper_sold`) instead of ending the story. |
| patron.009 | **c changes tier** (back into the system at tier 1, risk 25). a, b and e(success) close the debt; d and e(failure) turn it into the collector's scheme. The desc reads how the betrayal happened (the envoy dead or not). |

No new resource is introduced. The reprisal is the debt continuing by other means.

---

## 3. Identifier table

### 3.1 New

| Key | Type | Owner | Notes |
|---|---|---|---|
| `eotg_aug_patron.009` | event (namespace `eotg_aug_patron`, exists) | scripter | ***The Collector*** (title pending lore-keeper; alternative *The Paper Changes Hands*) |
| `eotg_aug_patron.006` option **f** | new option on an existing event | scripter | "Burn the terms. Send no answer." (lore P2) Shown only when the envoy is absent |
| `eotg_paper_sold` | story variable on `eotg_story_aug_patron` (bare, one-shot) | scripter | Set by `eotg_aug_patron_betray_effect` when the owner has no implants. Read by the tick and by .006 `after`. Same convention as `eotg_paper_served` |
| `eotg_aug_patron_collect_effect` | scripted effect (owner scope; `scope:eotg_patron_collector` saved) | scripter | The collector's reprisal: a vanilla murder scheme against root, with a gold fallback (§5.4) |
| `eotg_patron_collector` | saved scope (event-local, patron.009) | scripter | The collector, created in .009's `immediate` |

### 3.2 Changed

| Key | Change |
|---|---|
| `eotg_aug_patron_betray_effect` | New `else` branch on the existing `eotg_is_augmented_any = yes` test (§5.2) |
| `eotg_aug_patron.006` `after` | Ends the story only when `eotg_paper_sold` is not set (§5.2) |
| `eotg_story_aug_patron` tick | One new `triggered_effect`, second in the `first_valid` of **both** cadences (§5.3) |

### 3.3 Reused, not new

`eotg_aug_patron_envoy_template` (the collector is created from it: greedy/ambitious/deceitful, intrigue 10–14, which suits a collector), `eotg_aug_patron_envoy_present`, `eotg_aug_patron_can_pay` / `eotg_aug_patron_pay_effect`, `eotg_aug_initiate_effect`, `eotg_add_fracture_risk`, `eotg_mod_aug_patron_clause`, `eotg_mod_aug_patron_clause_final`, `eotg_mod_aug_excision_recovery`, `eotg_flag_aug_had_patron` (**unchanged**: one syndicate debt per life), the stress helpers `eotg_aug_stress_{surgery,tyranny}_effect`. Vanilla: the `murder` scheme, `imprison_character_effect`, `add_visiting_courtier`, `move_to_pool`, `start_scheme`, `can_start_scheme`.

No landed titles. `grep -rnE 'eotg_[ekdcb]_'` stays empty.

---

## 4. File placement

| File | Change |
|---|---|
| `common/scripted_effects/eotg_augmentation_effects.txt` | `eotg_aug_patron_betray_effect`: the `else` branch. New `eotg_aug_patron_collect_effect` directly below it. Header comments updated (callers). |
| `common/story_cycles/eotg_augmentation_stories.txt` | `eotg_story_aug_patron`: the collection entry in **both** cadences (the two `first_valid` bodies stay identical). Header comment updated. |
| `events/eotg_augmentation_patron.txt` | .006: option f, the `after` change, header comment. New .009 after .008. File header: add .009 to the event list and the fires-from map. |
| `localization/english/eotg_augmentation_l_english.yml` | 13 keys (§7). UTF-8 BOM. |

No new folder. No `replace_path`.

**Build order (the queue):** procedures → interactions → realm → **reprisal**. The reprisal depends on none of the other three, but all four edit `eotg_augmentation_effects.txt` and the loc file, so it is built last, serially, on top of whatever the realm build leaves. It touches no line those specs change. If the queue is reordered, the reprisal can move anywhere after procedures without a spec change.

---

## 5. Wiring

### 5.1 How the three cases close

| Owner | Envoy at .006 | Betrayal routes | Cost after this spec | Was |
|---|---|---|---|---|
| augmented | present | c, e, d (50%) | murder, throttle, risk +25, Countdown at tier 3 | unchanged |
| augmented | absent | **f**, d (50%) | throttle, risk +25, Countdown at tier 3 | d only (**case b**) |
| no implants | present | c, e, d (50%) | the envoy's murder **and the collector** (.009) | murder only (**case a**) |
| no implants | absent | **f**, d (50%) | **the collector** (.009) | no route, or lie stress only (**cases b, c**) |

The firmware punishment and the collector never stack. An owner gets one or the other, decided by whether any of the syndicate's hardware is still in the owner **at the moment of betrayal** (the throttle is a local absence: the servicing stops).

### 5.2 patron.006 changes

**Option f, "Burn the terms. Send no answer."** (lore P2)
```
option = {
    name = eotg_aug_patron.006.f
    trigger = { eotg_aug_patron_envoy_present = no }
    eotg_aug_patron_betray_effect = yes
    add_prestige = 50
    ai_chance = {
        base = 20
        modifier = { add = 20  has_trait = stubborn }
        modifier = { add = 10  has_trait = arrogant }
        modifier = { add = -20  has_trait = craven }
    }
}
```
- Placed after e. It is universal, so with the envoy absent .006 shows three universal options (a, b, f) and d [deceitful], which is rule 6's shape. With the envoy present it is hidden, and c is the in-person betrayal. The two are mirrors: c refuses the envoy in the room, f refuses the **message**, not a messenger.
- **No murder stress:** nobody dies. +50 prestige, the same as .007 c and .008 d (a refusal is seen to be made).
- Desc: the three existing `_absent` variants deliver the terms without the envoy in the room, but **only one of them has a courier** (lore P2; the earlier claim that all three do was wrong). f therefore names no messenger: the ruler burns the terms and sends no answer, which reads true under every `_absent` desc.

**`eotg_aug_patron_betray_effect`, the new branch.** The existing `if = { limit = { eotg_is_augmented_any = yes } … }` gains:
```
else = {
    # Reprisal spec §5.2: none of the syndicate's hardware is left in the owner
    # to stop servicing. The syndicate sells the paper;
    # the story stays alive and its next tick sends the collector (.009).
    scope:eotg_patron_story ?= { set_variable = eotg_paper_sold }
    custom_tooltip = eotg_aug_patron_paper_sold_tt
}
```
- `scope:eotg_patron_story` is saved in .006's `immediate`, the effect's only caller, so the `?=` is belt-and-braces.
- The envoy-murder branch above it is unchanged. Case (a) with the envoy present still murders the envoy **and** sells the paper.
- The tooltip appears on c, e, d(failure) and f for an owner with no implants. It is prose, never a number (§7).

**.006 `after`.** Replace `scope:eotg_patron_story ?= { end_story = yes }` with:
```
scope:eotg_patron_story ?= {
    if = {
        limit = { NOT = { has_variable = eotg_paper_sold } }
        end_story = yes
    }
}
```
a, b and d(success) never set the variable, so they still end the story. The story parks only after a betrayal by an owner with no implants. This is the same pattern as new_beats §5.1, where heir.004 parks the arc at stage 5 instead of ending it.

### 5.3 The tick: the collection entry

New `triggered_effect` in `eotg_story_aug_patron`, in **both** cadences, placed **second**: after the landless ending and before the Neurofractured write-off.
```
# Reprisal spec §5.3: the paper has been sold (a betrayal by an owner with
# no implants, eotg_aug_patron_betray_effect). The collector comes in person.
# Shadows every later entry, so a parked story never re-fires .006 (grievance
# >= 3 or demand >= 4 still hold) or .007 (the envoy is dead). The tick is the
# cooldown authority (index §1 rule 5); .009 checks no flag. Vanilla shape:
# story_cycle_pledge_loyalty_to_liege_overdue.txt:188-207.
triggered_effect = {
    trigger = { has_variable = eotg_paper_sold }
    effect = {
        story_owner = { trigger_event = { id = eotg_aug_patron.009  days = { 1 30 } } }
    }
}
```
- **Why second.** The landless exit must still win: a landless owner's debt ends, as now. The write-off and the paper entry cannot match an owner with no implants anyway, but this entry has to sit above the `always` entry, which would otherwise fire .006 again (grievance or demand is still at its Final Demand value) or .007 (the envoy is dead).
- **Pacing.** The collector arrives at the next tick: 2–3 years after the betrayal (3–4 on read terms), plus 1–30 days. The syndicate takes its time selling the paper.
- **No re-fire.** Every .009 option ends the story (`after`). If .009's trigger fails in the 1–30 days, the next tick fires it again; nothing loops, because the variable is only cleared by `end_story`.
- **Existing exits still apply while parked:** landless (entry 1), owner death (`on_owner_death`). The debt still dies with the owner (inherited debt stays deferred, phase5 §5).
- **The story's `on_end`** already removes the open-ended clause and sends a living envoy to the pool. A dead envoy is skipped by its `is_alive` guard.

### 5.4 patron.009 *The Collector*

- **Fired by:** the collection entry (§5.3), to the owner. Nothing else.
- **Trigger** (world-state guard mirroring the entry; no flags): `eotg_aug_has_patron = yes`.
- **Immediate:**
  ```
  hidden_effect = {
      random_owned_story = {
          limit = { story_type = eotg_story_aug_patron }
          save_scope_as = eotg_patron_story
          var:eotg_envoy ?= { save_scope_as = eotg_patron_envoy }
      }
  }
  create_character = {
      template = eotg_aug_patron_envoy_template
      location = root.location
      culture = root.culture
      faith = root.faith
      save_scope_as = eotg_patron_collector
  }
  add_visiting_courtier = scope:eotg_patron_collector
  ```
  The `create_character` shape is .007's own (and `eotg_aug_patron_accept_effect`'s). The collector is a **guest**, not a courtier: they came on business and are not in the ruler's service. Vanilla shape for adding a created or fetched character as a guest: `hold_court_events_general.txt:597-599`.
- **Theme** `intrigue`. **Portraits:** left root, `stress`. Right `scope:eotg_patron_collector`, `scheme`.
- **Desc:** `eotg_aug_patron.009.desc`, plus `triggered_desc = { trigger = { scope:eotg_patron_envoy ?= { is_alive = no } }  desc = eotg_aug_patron.009.desc_envoy_dead }` (appended; the collector mentions the last envoy once). That keeps a betrayal by murder and a betrayal by message from reading the same.
- **`after`:** `hidden_effect = { scope:eotg_patron_story ?= { end_story = yes } }`. Every option ends the debt as a story. d and e(failure) hand it to the collector's scheme.

| Opt | Text (loc intent) | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| **a** | "Pay what the paper says." | `eotg_aug_patron_can_pay = { BASE = major_gold_value  MULT = 2 }` | `eotg_aug_patron_pay_effect = { BASE = major_gold_value  MULT = 2 }` (the .006 buy-out price, scaled by the terms: betraying saved nothing); collector `move_to_pool = yes` | base 30; +20 honest; +10 diligent; −20 greedy |
| **b** | "Sign the lien on my revenues." | — (the ungated fallback) | remove `eotg_mod_aug_patron_clause` if held; `add_character_modifier = eotg_mod_aug_patron_clause_final` (guarded: `NOT = { has_character_modifier = eotg_mod_aug_patron_clause_final }`; the once-per-life flag already makes a second lien impossible, so the guard is belt-and-braces); collector `move_to_pool = yes` | base 30; +20 content; +10 craven; −20 ambitious |
| **c** | "Take the hardware against the debt." (lore P7) | `eotg_is_augmented_any = no`; `NOT = { has_character_modifier = eotg_mod_aug_excision_recovery }` | **Tier change.** `eotg_aug_initiate_effect = yes`; `hidden_effect = { eotg_add_fracture_risk = { AMOUNT = 25 } }` (the betrayal's own number: stock made to measure and sold against the debt, not fitted with care); `eotg_aug_stress_surgery_effect = yes`; collector `move_to_pool = yes`. Not rolled: a patron install (procedures §4.5, "Not rolled"). No lien, no gold. | base 20; +20 ambitious; +10 cynical; `factor = 0` zealous |
| **d** | "There is no debt. We are done." (lore P4: not an expulsion; the collector chooses to stay) | — | `add_prestige = 50`; `hidden_effect = { eotg_aug_patron_collect_effect = yes }`; `custom_tooltip = eotg_aug_patron.009.d.tt`. The collector stays as a guest. | base 20; +20 stubborn; +10 brave; −20 craven |
| **e [wrathful]** | "Seize the collector, and the paper." (lore rendering) | `has_trait = wrathful`; `trait = wrathful` | `random_list` with a desc per branch (the patron.002.e / .008.e shape). **50** (+15 if `prowess >= 12`) success, desc `.e.success`: `imprison_character_effect = { TARGET = scope:eotg_patron_collector  IMPRISONER = root }`; `add_dread = minor_dread_gain`. **50** failure, desc `.e.failure`: `add_prestige = -50`; `hidden_effect = { eotg_aug_patron_collect_effect = yes }`. Lore P5: the collector's people stop the seizure, nobody is taken, and the collector **stays on as a guest** (no `move_to_pool`). Both: `stress_impact = { wrathful = minor_stress_impact_loss }`. | base 30; +30 wrathful; +10 vengeful |

**Balance.**
- a costs the most gold, b costs income forever, and c costs the body (into the system again at tier 1 with risk 25, for an owner who chose to leave). c is a **sale of stock against the debt** (lore P7): the paper came with a case of the syndicate's stock made to this ruler's measure, and the ruler takes it at the paper's price. After c the ruler owns the hardware outright; nothing about c gives the syndicate any hold. d costs nothing now and puts a murder scheme on the ruler. None dominates.
- e rewards wrathful with a coin flip that can end it cleanly. Imprisoning a guest with no reason costs tyranny through `imprison_character_effect` (`00_prison_effects.txt:1644`), which is the intended price of seizing someone under your own roof. Vanilla's own note in that file prefers an opinion with an imprisonment reason for "custom situations". Here the arbitrary seizure **is** the point of the option, so the tyranny stays.
- An owner who re-augmented between .006 and the tick (by any route) loses c (its trigger). a, b, d and e still apply. This edge is accepted: the paper was sold when none of the syndicate's hardware was left in the owner.

**`eotg_aug_patron_collect_effect`** (owner scope; `scope:eotg_patron_collector` saved):
```
# Reprisal spec §5.4. The collector's people come for the ruler: a vanilla
# murder scheme (agents, physical, local; discovery is vanilla's). Started as
# vanilla starts one from script: hold_court_events_general.txt:20719-20722
# (can_start_scheme guard), :20816-20819 (start_scheme). AI owners execute it
# through murder_scheme.txt:337-343 (on_semiyearly prep). If the scheme cannot
# start, the collector's people take what they can carry instead.
# Callers: eotg_aug_patron.009 (d, e failure).
eotg_aug_patron_collect_effect = {
    if = {
        limit = {
            scope:eotg_patron_collector ?= {
                is_alive = yes
                is_imprisoned = no
                can_start_scheme = { type = murder  target_character = root }
            }
        }
        scope:eotg_patron_collector = {
            start_scheme = { type = murder  target_character = root }
        }
    }
    else = {
        remove_short_term_gold = medium_gold_value
    }
}
```
- **Why murder, and why the ruler.** The collector has no court to hold a prisoner in, so vanilla abduction is out: `abduct_scheme.txt` `allow` needs a perk or camp parameter and `valid` needs `is_ruler = yes` (:25-46). `murder` needs only `age >= 14` and a free owner (`murder_scheme.txt:25-28`). A ruler who will not pay is made an example of, by hand. The tamper scheme (interactions §4.4) is not used: its target must be augmented (`eotg_aug_tamper_target`), and this owner has nothing to tamper with.
- **Visible threat, secret scheme.** The scheme start is inside `hidden_effect`, and d's tooltip says what is coming in prose (§7). The scheme itself stays secret, as every vanilla murder scheme is. The player's spymaster and vanilla's breach and discovery events (`hostile_scheme_discovery_events.txt`) are how it is found. Once found, the ruler can imprison the collector through vanilla, because the murder discovery gives the reason.
- **The fallback** covers only an engine refusal (for example, the collector somehow already imprisoned). `remove_short_term_gold` may put the ruler into debt. That is intended: "debt" is literal here.

### 5.5 AI against the HQ2 targets

HQ2 (balance §0): at year 30, 25–40% of AI count+ rulers augmented; ≥ 15% of those at the top band; ≥ 1 terminal outcome per 10 Neurofractured rulers per decade.

**Funnel.** To reach .009 an AI ruler must: be offered the Patron (initiation check weight 15, once per life); accept; end up with no implants (Remove Implants, Excision, Salvage, Demand Removal, Rejection) while the debt is live; reach .006; and then betray (c, e, d-failure, or f). Each of those steps is a minority branch. **Expected: well under 1 collector per 100 AI ruler-decades.** The observer run decides (§9 item 7).

| Lever | Pushes | Expected effect at year 30 |
|---|---|---|
| .006 f (augmented owner, envoy absent) | top band **up** slightly (risk +25, Countdown at tier 3) | Negligible. The envoy is absent at .006 only after deaths or departures. It adds a betrayal route where AI previously had to sign or pay. |
| .009 c (re-install) | augmented share **up** | Under +0.5 point. A traitless AI picks c about 20–29% of the time (a 30 / b 30 / c 20 / d 20, or b 43 / c 29 / d 29 when it cannot pay). |
| .009 d / e(failure) → murder scheme | none on HQ2 | A traitless AI refuses about 20–29% of the time. The collector's success against a ruler with a spymaster is vanilla's. HQ2's terminal target counts Neurofractured endings, not murders, so this does not move it. |

**Tuning rule** (balance §9.2): change only `ai_chance` numbers. The observer run gains three counters (§9 item 7).

---

## 6. Vanilla precedent

All paths under `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/`.

| Mechanism | File:line | Used for |
|---|---|---|
| A character starts a vanilla murder scheme from script, gated by `can_start_scheme` | `events/activities/hold_court_activity/hold_court_events_general.txt:20708-20722` (`can_start_scheme = { type = murder  target_character = … }`), `:20808-20830` (`start_scheme = { type = murder  target_character = scope:victim }`) | `eotg_aug_patron_collect_effect` |
| `start_scheme` field set (`type`, `target_character`) | PX `script_docs/effects.log` `start_scheme` | same |
| Murder `allow` / `valid` (age 14, free; target has a location) | `common/schemes/scheme_types/murder_scheme.txt:25-75` | why a guest can own it |
| AI scheme owners execute through the semiyearly prep | `murder_scheme.txt:337-343` | the collector acts without a player |
| Abduction needs a ruler with a perk | `common/schemes/scheme_types/abduct_scheme.txt:25-46` | why not abduct |
| A created or fetched character is added as a guest | `hold_court_events_general.txt:597-599` (`add_visiting_courtier`) | .009 immediate |
| A guest leaves for the pool | `hold_court_events_general.txt:508` (`move_to_pool`, already cited in the Patron `on_end`) | .009 a, b, c |
| Imprisonment with vanilla's tyranny handling | `common/scripted_effects/00_prison_effects.txt:1644` (`imprison_character_effect`) | .009 e |
| A story outlives its climax and delivers a later beat instead of ending | `common/story_cycles/ep3_story_cycle_admin_eunuch.txt:145-182`; the mod's own heir arc dormant stage 5 (new_beats §5.1) | the `eotg_paper_sold` park |
| One-shot story variable read by the tick before firing an event | `common/story_cycles/story_cycle_pledge_loyalty_to_liege_overdue.txt:188-207` | the collection entry |
| An option that acts on a story character requires them alive and at court | `events/story_cycles/peasant_affair/story_cycle_peasant_affair_events.txt:1173-1178` | f is the converse: shown only when the envoy is **not** present |

**Deviation.** A **guest** owns the murder scheme. Vanilla's script start (hold court 8160) uses a vassal or courtier, and agent groups include `guests` on the owner side (`murder_scheme.txt` `agent_groups_owner_perspective`). Nothing in `allow` or `valid` excludes a guest. The reason: a collector in the ruler's service would be dismissable through vanilla and would read wrong. Whether the engine runs it to completion is engine check (a) in §9.

---

## 7. Loc surface (eotg-localizer)

13 new keys plus 1 revised shipped key, dot form (index §0), UTF-8 BOM, bare `[x.GetName]`, ~~US spelling~~ Canadian English (supersedes US spelling: owner ruling 2026-10-04, loc commit 4168bb8), appended descs start with `\n\n`. No `replace/` override. **No number and no "risk", "odds" or "chance"** in any of them.

**The renderings in [cybernetics_v2_reprisal_lore.md](cybernetics_v2_reprisal_lore.md) §Renderings are binding** (P2–P7). The localizer may polish them within the rules below, but does not rewrite them. They are not copied here, so there is one source.

| Key | Binding text |
|---|---|
| `eotg_aug_patron.006.f` | lore file (P2: "Burn the terms. Send no answer.") |
| `eotg_aug_patron_paper_sold_tt` | lore file (P3: never "reach"; the throttle is a local absence) |
| `eotg_aug_patron.009.t`, `.desc`, `.desc_envoy_dead` | lore file (title *The Collector*, ratified) |
| `eotg_aug_patron.009.a`, `.b`, `.c`, `.d`, `.d.tt`, `.e`, `.e.success`, `.e.failure` | lore file (P4 for `.d` / `.d.tt`, P5 for `.e.failure`, P7 for `.c`) |

**Revised shipped key (U1, decided holder-neutral under the human's "proceed with recommendations"):**

| Key | Change |
|---|---|
| `eotg_mod_aug_patron_clause_final_desc` | Replace the text with the lore file's U1 rendering: "A permanent share of the revenues goes to whoever holds the paper, in exchange for the debt being closed. It is paid every month, and it will be paid for as long as there are revenues." The display name "Syndicate Lien" stays. Loc-only (still one definition; no script change). It makes .009 b read true when the collector, not the syndicate, holds the paper. |

**Register rules (binding):**
- **P6, pronouns.** The collector is a scoped single character: gendered pronouns (`[eotg_patron_collector.GetSheHe]`, `GetHerHis`, `GetHerHim`, `|U` at sentence start), never singular "they". The plural "their people" (the collector's crew) stays plural.
- **P7, payment in kind is a sale of stock.** The paper came with a case of the syndicate's stock, made to this ruler's measure, and the ruler takes it at the paper's price. **Never write** "theirs", "the syndicate's again", "back in their hands", "on their schedule", "serviced by them", "under contract", "owned", "obedience", "loyalty", "bound", "leash", or anything about who holds the firmware. **This applies to script comments too** (the scripter's comments on .009 c, the betray effect and the collect effect).
- **Holding the paper.** The collector *holds* the paper as property. Never "lawful", "rightful", "claim", "title to the debt", "bounty", "assigned", and nothing from the realm-lore apparatus list.
- **"Murder" and "Enforcers" never reach loc.** In-world, the paper is worth more as an example than as a sum; the prose shows it without naming the act.

**Vanilla strings:** the murder scheme's own UI and outcome events are vanilla's and need no override. They name the collector by `GetName`.

---

## 8. Lore constraints

From `docs/lore/REVIEW_866.md`, index §5, and the three binding lore files ([procedures_lore](cybernetics_v2_procedures_lore.md), [interactions_lore](cybernetics_v2_interactions_lore.md), [realm_lore](cybernetics_v2_realm_lore.md)):

- **Agents and debt, never a remote act.** The reprisal is a person who arrived, a sum, a lien, and people who come by hand. No kill switch, no shutdown, no firmware acting at a distance (Blackstar, 1300; REVIEW_866 "Rules"). The throttle on an augmented betrayer stays what lore I-ruling 5 made it: a **local absence** (the servicing stopped). The interactions §7 banned-word list applies to every key here: never "signal", "transmit", "remote", "from afar", "kill switch", "override code", "shut down", "terminate", "brick", "hack", "virus", "upload", "network".
- **No authority above the polity** (LAW AT 866). The syndicate has no court to take the paper to, so it sells it to someone who acts through people. The collector cites no law, licence, tribunal or registry. The realm_lore list also applies: no "authority", "warrant", "magistrate", "inspector", "registry".
- **Physical and local only** (interactions lore I5/I6). The collector arrives in person; their people are at the door. Any tracing of the scheme is vanilla's.
- **The syndicate stays unnamed** (index §5.3, §5.7). "The syndicate", "the collector". Never Blackstar, Black Contract(s), Shadow Markets, the Enforcer Corps, Cogblade Enforcers, **Black Cogs**, **Chains of Greed**, P&D, Calix, Pill Mob, Concrete Cartel, Helix, Pale Hand, Consortium, Compact, Continuity, Rooks, "Corp"/"Co.", or white-glove imagery. "Enforcers" never reaches loc.
- **Tone model (corrected, lore P1).** The line "the Chains of Greed, a web of debt and contracts enforced through mercenary enforcers" belongs to the **Black Cogs Consortium, 1130** (`docs/lore/Third era Nations.md:723-730`), not to Blackstar. It is cited as a **post-866 tone model only**: nothing from it exists at 866, and neither its names nor its institutions are used.
- **.009 c must not imply control through implants.** Blackstar's Black Contracts bound labour "through neural implants" (Third era Nations.md:862-864). At 866 that reads as remote control and is out. c is a **sale of stock against the debt** (lore P7; §7 register rule), with the careless fitting as its cost. Afterwards the ruler owns the hardware. It is never a leash, an obedience or a loyalty enforced through the hardware, and nothing says who holds the firmware.
- **No monotheistic invocations; "self" not "humanity"; no medieval leaks** (index §5.4–5.6): residence, not palace; guards and people, not men-at-arms.
- **Nikios Khanate:** untouched (invariant 9).
- **Lore review done (2026-10-04):** P1–P7 and U1 are folded in. The title *The Collector*, selling the debt, the murder scheme and the guest are approved. The items that were routed:
  1. the title *The Collector* (or *The Paper Changes Hands*);
  2. whether a syndicate **selling a debt** to a collector fits 866 AG;
  3. a **murder scheme** as the enforcement, rather than a beating or a seizure of goods;
  4. .009 c against the Black Contracts line above (now a sale of stock, P7);
  5. the collector as a **guest** at the debtor's court.

---

## 9. Definition of done

0. **Validation, all three clean** on the touched files, except the `CLAUDE.md` known-benign list: Tiger 1.17.0 (scratch descriptor), `docs/tools/px_lsp_diagnostics.js`, `docs/tools/px_vocab_check.py`. Tiger is the only one that checks scope (`can_start_scheme` and `start_scheme` in the collector's scope, `imprison_character_effect` params).
1. **Reachability (PX event graph):** patron.009 is reached from `eotg_story_aug_patron` in **both** cadences, and from nothing else. .006 f is reachable whenever .006 fires with the envoy absent.
2. **Coupling (QA audit 8):** .009 c calls `eotg_aug_initiate_effect` (tier change); .006 f calls `eotg_aug_patron_betray_effect`.
3. **No cooldown in an event trigger:** .009's `trigger` is `eotg_aug_has_patron = yes` only; it reads neither `eotg_paper_sold` nor any flag.
4. **Story park:**
   - `grep -n eotg_paper_sold common events` shows one `set_variable` (in the betray effect's `else`), one read in .006 `after`, and one read per cadence in the tick.
   - The two Patron `first_valid` bodies are identical (diff shows nothing).
   - The collection entry is second in each, after the landless entry.
5. **Case table (§5.1) holds by inspection:**
   - the betray effect's `if` / `else` on `eotg_is_augmented_any` means the throttle and the paper are never both applied;
   - .006 f's trigger is `eotg_aug_patron_envoy_present = no`;
   - c and e keep their presence gate.
6. **Lore register:** `grep -niE "remote|signal|transmit|from afar|kill.?switch|override code|shut ?down|terminate|brick|hack|virus|upload|network|blackstar|black contract|shadow market|enforcer|cogblade|p&d|calix|pill ?mob|concrete cartel|helix|pale hand|authorit|warrant|magistrat|registry|murder|bounty|lawful|rightful|black cogs|chains of greed|theirs|under contract|owned|obedien|loyalty|bound|leash"` over the 13 new keys and the revised `eotg_mod_aug_patron_clause_final_desc` returns nothing (lore P1, P7 and the rulings). Also `grep -niE "\breach"` over `eotg_aug_patron_paper_sold_tt`, `eotg_aug_patron.009.desc`, `.d.tt`, `.e`, `.e.success` and `.e.failure` returns nothing (lore P3). The P7 terms (`theirs|under contract|owned|obedien|loyalty|bound|leash`) are also grepped over the script comments on .009 c, `eotg_aug_patron_betray_effect` and `eotg_aug_patron_collect_effect`.
7. **Observer run** (balance §9.2) gains three counters per decade: .006 f taken (augmented / no implants); .009 fired, with the option split; collector murder schemes started and succeeded.
8. **Loc:** all 13 keys exist exactly once, with BOM and no `[scope:`. They use the lore file's renderings (polish allowed, no rewrite). `eotg_mod_aug_patron_clause_final_desc` carries the U1 text and is still defined once. The collector is gendered (P6).
9. **Human, in game (temporary map):**
   - **Case a.** Accept the Patron, take Remove Implants, take .008 d. At .006 (betrayal tone, envoy present), take c. The envoy dies, the story is still there (`any_owned_story`), and at the next tick .009 fires with `desc_envoy_dead`.
   - **Case b.** An augmented Patron owner. Console-kill the envoy, console-set the story's grievance to 3. .006 fires with an `_absent` desc and shows a, b, f (plus d if deceitful). Take f: throttle, no collector, and the story ends. Repeat with an owner who has no implants: no throttle, and .009 at the next tick.
   - **Case c.** A deceitful owner with no implants and the envoy absent. Take .006 d until it fails (reload). .009 follows at the next tick.
   - **.009 d.** The collector stays as a guest. The character's scheme list (or the console) shows a murder scheme against you. Let it run with a spymaster: vanilla discovery and outcome events fire and name the collector.
   - **.009 c.** The ruler is back at tier 1. No lien. The story is gone.
   - **.009 e.** Success: the collector is in your prison, with the vanilla tyranny tooltip. Failure: the collector is a guest with a murder scheme.
   - **Engine checks (not settled by vanilla):**
     - (a) a character created with `create_character` and added with `add_visiting_courtier` can own a `murder` scheme against the host that progresses, and the AI executes it (`murder_scheme.txt:337-343`). If it cannot, the fallback branch runs and the human decides whether to use `add_courtier` instead (one line);
     - (b) `remove_short_term_gold` takes a ruler below zero (fallback only).

---

## 10. Deferred

| Item | Why |
|---|---|
| **The collector after the scheme** (a second collector, an escalation chain) | Lean. One event and the vanilla scheme close all three cases. Vanilla's 10-year murder cooldown and its retry rules decide whether the collector tries again. |
| **The reprisal on an augmented betrayer as well** | The firmware throttle is that owner's reprisal. Stacking the collector on top makes betrayal strictly worse for augmented owners than for anyone else. |
| **Inherited debt** (phase5 §5) | Unchanged. The paper still dies with the owner, even when it has been sold. |
| **A Realm-law interaction** (Ban makes the collector's c install contraband) | patron.008 c ignores the realm law too. Unify both when realm QA finds it matters in play. |
| **Bespoke collector template** | The envoy template's greedy/ambitious/deceitful and intrigue 10–14 already suit a collector. Add one only if playtest finds the collector indistinguishable from the envoy. |
| **Collector name / CoA** | The collector is a created character who takes a name from root's culture. No name list is needed. |

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Build docs/specs/cybernetics_v2_reprisal.md §3–§5 after procedures → interactions → realm (§4 build order); script comments follow the P7 register (§7). Then eotg-localizer: §7, with docs/specs/cybernetics_v2_reprisal_lore.md §Renderings binding, plus the U1 rewrite of the shipped eotg_mod_aug_patron_clause_final_desc. Then eotg-qa (§9, with item 6's extended greps).
- files: docs/specs/cybernetics_v2_reprisal.md (lore P1–P7 and U1 folded in); docs/specs/cybernetics_v2_reprisal_lore.md (binding, committed by the lore-keeper)
- new events (1): eotg_aug_patron.009 The Collector (fired by the collection entry in eotg_story_aug_patron, both cadences). Plus: option eotg_aug_patron.006 f "Burn the terms. Send no answer."; effect eotg_aug_patron_collect_effect; story variable eotg_paper_sold; changed eotg_aug_patron_betray_effect (else branch) and the .006 `after` block.
- needs-loc (13 new + 1 revised): eotg_aug_patron.006.f, eotg_aug_patron_paper_sold_tt, eotg_aug_patron.009.t, .desc, .desc_envoy_dead, .a, .b, .c, .d, .d.tt, .e, .e.success, .e.failure; revised eotg_mod_aug_patron_clause_final_desc (U1)
- needs-lore: none open (P1–P7, U1 folded in)
- needs-human: §9 item 9 in-game checks, including engine checks (a) a guest as murder-scheme owner and (b) `remove_short_term_gold` into debt; the observer run's three new counters (§9 item 7)
