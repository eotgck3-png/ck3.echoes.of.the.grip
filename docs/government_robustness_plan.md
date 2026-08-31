# Government Robustness Plan — Echoes of the Grip

Prepared 2026-08-29. Companion to `closed_alpha_checklist.md` and `system_depth_audit.md`.

**Goal:** seven governments that are mechanically distinct from each other, playable at every
tier, and meeting the structural standards vanilla sets for its own government types — while
staying unique to the mod.

**Current state in one line:** the governments are well-differentiated in *content* (events,
modifiers, decisions) and completely undifferentiated at the *engine* level, and almost all of
their content is visible only to seven characters in the world.

Baseline for regression checks: **Tiger 64 errors / 195 warnings, 328/328 events reachable,
0 self-cancelling events.** Any step that moves those numbers needs explaining.

---

## Findings this plan addresses

| # | Finding | Severity | Evidence |
|---|---|---|---|
| F1 | All 7 governments draw on the **same 4 rules** out of vanilla's 48, differing only by on/off | **Major** | 3 distinct value-sets across 7 governments; vanilla governments carry 4–22 rules each |
| F1b | Cartel and Fringe set `legitimacy = no`, but 3 of their events still call `add_legitimacy` — those effects are **silently inert** | **Moderate** | `eotg_cartel_expanded_events.txt:763`, `eotg_fringe_events.txt:390`, `eotg_fringe_expanded_events.txt:666` |
| F2 | **Fringe cannot raid** despite being the mod's raiding government | **Critical** | `government_can_raid_rule` is on Cartel, absent on Fringe; Fringe has a raid on_action hook, a 3-event ally-raid file, and 11 raid references in its flavor set |
| F3 | Almost all government events reach only the empire-tier ruler | **Major** | All 7 flavor on_actions gate on an empire-tier role trigger; only 7 events in the whole mod reach a vassal |
| F4 | 4 role triggers defined and **never referenced**; 7 more have token use | **Major** | `street_lord`, `underboss`, `star_warden`, `field_director` = 0 refs |
| F5 | 5 of 7 government flags are dead | Moderate | `eotg_government_is_cartel` / `_democracy` / `_elven_monarchy` / `_fringe` / `_pmc` = 0 refs |
| F6 | `allow_accolades` missing on all 7 | Moderate | Present on 14 of 17 vanilla governments |
| F7 | Vassal contracts are 2–3 deep vs vanilla feudal's 11 | Moderate | `common/subject_contracts/groups/` |
| F8 | Vassal-facing decisions: Fringe 4, Cartel/Corp/NC 1 each, **PMC / Gob-Ogre / Elven 0** | Moderate | Decision role gating |
| F9 | `ai` block on 1 of 7 governments (vanilla: 10 of 17) | Minor | Only `eotg_gobcorp_government` |
| F10 | Never used: `mechanic_type`, `royal_court`, `can_get_government`, `realm_mask_scale` / `realm_mask_offset` | Minor–Major | `realm_mask_*` is on 16 of 17 vanilla governments |

### The role ladder that already exists

Every government defines a complete four-tier ladder — 26 role triggers. The identity work is
done; most of the ladder is simply unused.

| Government | County | Duchy | Kingdom | Empire |
|---|---|---|---|---|
| Cartel | Street Lord *(0 refs)* | Underboss *(0 refs)* | Boss | Grand Underlord |
| Corporation | Account Director *(6)* | Operations Chief *(1)* | Regional Director | CEO |
| Elven Monarchy | Star Warden *(0 refs)* | Celestial Lord | Eternal Regent *(2)* | Starborn Sovereign |
| Gob-Ogre | Trade Prince *(3)* | Trade Prince | Merchant Lord *(4)* | Director-General |
| New Cauldron | Governor *(6)* | Senator | State *(3)* | President |
| PMC | Contractor | Field Director *(0 refs)* | Executive Commander | Contractor-General |
| Fringe | Captain | Captain | Overlord | Overlord |

Fringe is the outlier and the model: `eotg_st_is_fringe_captain` is the most-used role trigger
in the mod at 51 references.

---

## Phase 0 — Assess before changing

Nothing here edits game files. The point is to avoid prescribing engine rules whose behaviour
has not been confirmed, and to make design intent explicit before writing to it.

### 0.1 Establish which `government_rules` are safe to adopt — **DONE 2026-08-29**

Checking defaults in `common/governments/_governments.info` invalidated three of this plan's own
2.2 proposals. This is exactly what the phase existed to catch:

| Rule | Documented default | Verdict |
|---|---|---|
| `sticky_government` | `no` | Setting `= yes` is meaningful ✓ |
| `house_aspirations` | `no` | Setting `= yes` is meaningful ✓ |
| `always_use_patronym` | `no` | Setting `= yes` is meaningful ✓ |
| `disable_regnal_numbers` | `no` | Setting `= yes` is meaningful ✓ |
| `deny_powerful_vassal` | `no` | Meaningful, but rejected for Cartel on design grounds (see 2.2) |
| `affected_by_development` | **`yes`** | **Proposal was backwards.** Vanilla only ever sets it `= no`, and does so for exactly the raider archetypes (tribal, wanua, nomad). For Fringe the meaningful move is `= no`, not `= yes` — but that is a real nerf to Fringe counties, so treat it as a design decision rather than a parity fix. |
| `court_generate_spouses` | **`yes`** | **Proposals were no-ops.** Vanilla only ever sets it `= no`. Drop it from the Corporation / New Cauldron / PMC rows. |
| `allow_accolades` | **undocumented** | Not in `_governments.info` at all, but vanilla declares it explicitly on 14 of 17 governments (10 yes, 4 no). The four `no` cases are mercenary, holy order, landless adventurer and herder — the non-noble types. Since the default is unknowable from the docs, follow vanilla practice and set it **explicitly** on all 7. `yes` throughout, PMC included: its knights are already renamed *Operators* in loc, and accolades are precisely the elite-named-unit system that fits. |

The deferral list below stands unchanged — several vanilla rules are not free-standing and pull in
whole DLC subsystems the mod does not have:

- **Requires supporting content — do NOT adopt yet:** `administrative`, `treasury`,
  `replace_gold_cost_by_treasury`, `noble_families`, `merit`, `obedience`, `radiance`,
  `barter`, `landless_playable`, `subject_men_at_arms`, `use_maa_maintenance`,
  `conditional_maa_refill`. The last three need `common/men_at_arms_types/`, which is absent
  (alpha checklist, Gate 3).
- **Method:** for each candidate, grep vanilla for which governments carry it, then check
  whether those governments also declare a `mechanic_type` or a folder the mod lacks. If they
  do, defer the rule.

### 0.2 Decide each government's mechanical identity

One sentence per government stating what it does that no other does. This drives Phase 2 and
keeps the rules pass from becoming decoration. Straw-man to argue with:

| Government | Proposed mechanical identity |
|---|---|
| Fringe | Raiding plus unstable authority (`fringe_grip` decay, four reform paths) |
| Cartel | Dread economy — loyalty extracted, never owed |
| Corporation | Board influence as a spendable political currency |
| Gob-Ogre | Vote weight — power is bought and counted |
| New Cauldron | Elections and Senate consent as a recurring constraint |
| PMC | Contracts — income and legitimacy come from outside the realm |
| Elven Monarchy | Court ratification and isolationism; the slowest, most legitimist government |

### 0.3 Confirm the tier-neutral event set — **DONE 2026-08-29, set corrected to 28**

Re-reading the descriptions caught **4 false positives** in the 32. The original filter looked for
mentions of the *top role* ("Underlord", "President"), so it missed events that betray liege-POV by
referring to the player's **subordinates** instead:

| Event | Why it is liege-POV after all |
|---|---|
| `eotg_corp_flavor.0017` | Junior Directors petition *you* for board representation |
| `eotg_fringe.0016` | "the captains grow restless. They come to you" |
| `eotg_fringe.0030` | "one of the captains has brought their crew's concerns directly to you" |
| `eotg_fringe.0032` | a captain publicly challenges *your* fitness to lead |

Two flagged by the same sweep were re-confirmed as genuinely portable and kept:
`eotg_fringe.0031` (the crew and the raid spoils — a Captain has both) and `eotg_pmc_flavor.0016`
(junior operators petitioning; operators are troops, and a Field Director commands them).

**Final set: 28 events** — PMC 14, Cartel 6, Fringe 4, Corporation 3, Gob-Ogre 1.


The 32 events listed in 1.2 were classified by (a) no vassal references and (b) no mention of a
top role or central body in their localization. Re-read each one's `desc` before re-gating — the
filter is textual, and a couple may still read as liege-POV.

### 0.4 Record the pre-change baseline

Re-run Tiger, the reachability pass and the self-cancellation check; note the numbers. Every
later phase is judged against them.

---

## Phase 1 — Zero-risk corrections

No new content. Each item is small, independently verifiable, and reversible.

### 1.1 Move raiding to Fringe; give Cartel tributaries — F2 — **DONE 2026-08-29**

The flag was on the wrong government. Both halves applied:

- **Fringe** — `government_can_raid_rule` added to `flags`. The government's own header called it
  a coalition of raiders, and it carried an `on_raid_action_start` hook, a 3-event ally-raid file
  and 11 raid references in flavor, while being unable to raid.
- **Cartel** — `government_can_raid_rule` **removed**. A cartel does not sack a neighbour. In its
  place, `ask_for_tribute` and `count_tributaries_for_title_requirements` were added to
  `government_rules`, so the Cartel expands by putting independent neighbours on a payment
  schedule. Full investigation notes under 2.2.

Both file headers record the change and the reasoning.

- **Verified:** Tiger unchanged at 64 errors / 195 warnings, nothing flagged in `governments/`,
  and both new rules parse cleanly.
- **Still needs an in-game test** (blocked on Gate 1): raiding needs an adjacent raidable target,
  and the tributary interaction needs independent rulers on the map. Tiger cannot see either.

### 1.2 Re-gate the tier-neutral events — F3 — **DONE 2026-08-29 (28 events)**

All five applicable `eotg_on_yearly_<gov>_flavor` on_actions were split into Section A (any tier,
gated on the broad government trigger) and Section B (top tier). Per-event comments travel with
their blocks. Applied: **PMC 14, Cartel 6, Fringe 4, Corporation 3, Gob-Ogre 1.**

Elven Monarchy and New Cauldron were untouched — they have no tier-neutral events at all, which is
what Phase 3.1 exists to fix.

**Verified:** `trigger_event` count unchanged at 166, brace balance 0, reachability 359/359,
self-cancellation 0 of 157 pairs, and **zero Tiger findings in `eotg_on_actions.txt`**.

> **Attribution note.** The Tiger totals moved during this step (errors 64→66, warnings 195→147,
> untidy 15→0) because of parallel edits elsewhere in the repo — a new Void system
> (`eotg_void_triggers.txt`, `eotg_void_decisions.txt`, `eotg_void_on_actions.txt`), plus culture,
> history-character and localization changes. All three new errors trace to those files, none to
> this change. Re-baseline Tiger once that work settles.

Two comments inside the Fringe blocks said "overlord" and were reworded to "any tier" after the
move, since they now sit in Section A.

#### Original plan text



Restructure each `eotg_on_yearly_<gov>_flavor` into two sections inside its existing `effect`:

```
eotg_on_yearly_cartel_flavor = {
    effect = {
        # Section A — any Cartel ruler, any tier
        if = { limit = { eotg_st_is_cartel_ruler = yes }
            ...tier-neutral blocks...
        }
        # Section B — Grand Underlord only
        if = { limit = { eotg_st_is_grand_underlord = yes }
            ...liege-bound blocks...
        }
    }
}
```

Preferred over a separate on_action: no new registration, each government's content stays in one
place, and the two sections are mutually exclusive by tier — so the existing `_recent` cooldown
flags need no changes.

**The 32 events to move:**

| Government | Events |
|---|---|
| PMC (14) | `eotg_pmc_flavor.0002 .0003 .0006 .0007 .0009 .0010 .0014 .0016 .0018 .0019 .0020 .0021 .0022 .0023` |
| Fringe (7) | `eotg_fringe.0016 .0023 .0028 .0029 .0030 .0031 .0032` |
| Cartel (6) | `eotg_cartel_flavor.0005 .0009 .0010 .0011 .0012 .0018` |
| Corporation (4) | `eotg_corp_flavor.0003 .0007 .0012 .0017` |
| Gob-Ogre (1) | `eotg_gobcorp_flavor.0018` |

Broad-government triggers already exist for Section A: `eotg_st_is_cartel_ruler`,
`eotg_st_is_corporation_ruler`, `eotg_st_is_gobcorp_ruler`, `eotg_st_is_pmc_ruler`,
`eotg_st_is_fringe_ruler`, `eotg_st_is_elven_monarch`. New Cauldron has no broad trigger — add
`eotg_st_is_nc_ruler` when Phase 3 needs it.

- **Verify:** reachability and self-cancellation passes stay clean; a duchy-tier character of
  each government now has at least one eligible flavor event.
- **Risk:** low-to-moderate. The real risk is *tone*, not script — an event written for an
  emperor reading oddly for a count. Mitigated by 0.3.

### 1.3 Resolve the dead government flags — F5

Either use them or drop them. Recommended: **use them**, converting gating from
`has_government = eotg_X_government` to `government_has_flag = eotg_government_is_X`. That
matches vanilla's idiom (1,100+ uses) and allows shared capabilities. The mod already does this
correctly with `eotg_government_is_corporate`, shared by Corporation and Gob-Ogre (5 refs).

Low priority on its own — do it opportunistically while touching each government file.

### 1.4 Resolve the 4 dead role triggers — F4

`eotg_st_is_street_lord`, `eotg_st_is_underboss`, `eotg_st_is_star_warden`,
`eotg_st_is_field_director`. Do **not** delete them — they are the natural anchors for Phase 3
content. Add a comment in `common/scripted_triggers/` marking them as reserved, so a future
audit does not read them as cruft.

---

## Phase 2 — Engine-level differentiation

This phase closes F1 and the bulk of the vanilla-standards gap.

### 2.1 Add `allow_accolades` to all 7 — F6

Present on 14 of 17 vanilla governments, absent on all 7 here, so the knight-fame system is
silently off mod-wide. Cheapest single credibility win. Uses vanilla accolade types — the mod
has no `common/accolade_types/`, which is fine, vanilla's are inherited.

### 2.2 Differentiate `government_rules` per government — F1

Apply only rules cleared in 0.1. Starting proposal, to be revised against 0.2:

| Government | Add | Rationale |
|---|---|---|
| Fringe | `always_use_patronym` | Tribal-adjacent raider profile. `affected_by_development` dropped — default is already `yes`; see 0.1 |
| Cartel | ~~`deny_powerful_vassal`~~ — **rejected, see below** | — |
| Corporation | `sticky_government` | Corporate continuity. `court_generate_spouses` dropped — no-op, default `yes` |
| Gob-Ogre | `sticky_government` | The League persists across Director-Generals |
| New Cauldron | *(none yet)* | `court_generate_spouses` dropped — no-op, default `yes`. Needs a fresh candidate |
| PMC | `disable_regnal_numbers` | A command, not a line of kings. `court_generate_spouses` dropped — no-op |
| Elven Monarchy | `house_aspirations`, `sticky_government` | Longest-memory, most legitimist |

#### `deny_powerful_vassal` for Cartel — investigated 2026-08-29, **rejected**

The earlier caution here was **wrong on the facts and right on the instinct**. Corrections:

- Vanilla's own documentation (`common/governments/_governments.info:196`) states: *"Characters with
  this government rule will never become powerful vassals."* It applies to the **vassal's own**
  government, not the liege's.
- **No Cartel content depends on `is_powerful_vassal`** — zero references in any Cartel file. The
  claimed breakage of the loyalty-tax and Shakedown machinery does not exist:
  `eotg_st_cartel_shakedown_eligible` gates on faction commitment and liege vulnerability, never on
  powerful-vassal status. Adopting the rule would break nothing.
- A related correction: `system_depth_audit.md` lists `eotg_market_faction_cycle` as shared by
  Corporation / Cartel / Gob-Corp. It is not. The cycle requires
  `liege = { government_has_flag = eotg_government_is_corporate }`, a flag only Corporation and
  Gob-Ogre carry, so **Cartel never participates**.

Rejected anyway, for design reasons rather than technical ones. The rule strips powerful-vassal
status from Cartel Bosses, which removes their council rights — working directly against this
plan's central goal of making vassal tiers worth playing. Vanilla pairs it with tributaries on
Mandala (`deny_powerful_vassal = yes #LET HAVOC ENSUE!`) because Mandala's power comes from
*outside* the realm. The mod's Cartel is the opposite: its entire drama — Loyalty Tax, the
Shakedown faction, the Hostile Takeover — is generated by strong internal Bosses. Flattening them
would remove the tension the content is built on.

#### Cartel tributaries — investigated 2026-08-29, **adopted**

Applied in place of raiding (see 1.1). Verified before adopting:

- `ask_for_tribute` enables the vanilla `offer_tributary_status_interaction`, gated on
  `government_allows = ask_for_tribute` and targeting **independent rulers only** — so tributaries
  are foreign powers, never your own Bosses. Exactly a protection racket at state scale.
- **No DLC gate anywhere**: zero `has_dlc` / `dlc_feature` checks in
  `common/character_interactions/00_tributary_interactions.txt`, in
  `common/subject_contracts/groups/subject_contract_groups.txt`, or in
  `common/subject_contracts/contracts/default_tributary.txt`. Mandala's `has_tgp_dlc_trigger`
  gates *adopting Mandala*, not the tributary system.
- **No new content required**: vanilla supplies the `tributary_settled` contract group
  (`default_tributary_taxes`, `_levies`, `_prestige`, `tributary_war_participation_obligation`).
- `count_tributaries_for_title_requirements` added alongside it, so tributary land counts toward
  title creation — a cartel that grows by putting neighbours on a payment schedule.
- Mandala is the **only** vanilla government using `ask_for_tribute`, so this stays distinctive
  rather than borrowed.
- *Untestable until Gate 1* — needs independent rulers on the map.

### 2.3 Add `realm_mask_scale` / `realm_mask_offset` — F10

On 16 of 17 vanilla governments. Copy sensible values from the nearest vanilla analogue per
government. Cosmetic, but near-universal in vanilla.

### 2.4 Add `ai` blocks to the remaining 6 — F9

Only Gob-Ogre has one. Without them, AI rulers of the other six behave identically regardless of
government, which undercuts the differentiation bought in 2.2.

### 2.5 Add `can_get_government` — F10

Controls who may adopt each government. Currently unrestricted, so nothing prevents incoherent
conversions. Ties directly into Fringe's four reform decisions (`reform_feudal`, `reform_cartel`,
`reform_corporation`, `reform_pmc`), which are the mod's main government-change path.

### 2.6 Defer, and record the deferral

`mechanic_type`, `royal_court`, `domicile_type`, `tax_slot_type` — each needs a supporting
subsystem the mod does not have. Note them in the alpha checklist as deliberate deferrals, so a
tester who notices a plain court screen knows it was a decision rather than a bug.

---

## Phase 3 — Content for the tier gaps

### 3.1 Vassal-POV flavor for Elven Monarchy and New Cauldron — F3

These two scored **zero** tier-neutral events. Their flavor is entirely Eternal Court and Senate
business, structurally invisible to vassals. They need new writing, not re-gating.

- **Elven Monarchy** — target `eotg_st_is_star_warden` (county) and `eotg_st_is_celestial_lord`
  (duchy). Natural material: serving a Sovereign whose confirmation you did or did not support;
  being asked to enforce Court Purity locally; the long-lived vassal who outlasts liege after
  liege.
- **New Cauldron** — target `eotg_st_is_nc_governor` and `eotg_st_is_nc_senator`. Natural
  material: constituency pressure, voting against your own State, campaign season seen from
  below.
- **Suggested scope:** 6–8 events each, matching the existing flavor-file shape (three options,
  `ai_chance` weights, cooldown flag, own `trigger` block **without** a `_recent` re-check).

### 3.2 Vassal decisions where there are none — F8

PMC, Gob-Ogre and Elven Monarchy have zero vassal-facing decisions. Fringe (4) is the model —
`distribute_spoils`, `forge_unified`, `rule_through_fear` and `suppress_captains` all work for
Captains as well as Overlords.

- **PMC:** a Field Director or Contractor negotiating their own sub-contract.
- **Gob-Ogre:** a Trade Prince building vote weight — this also closes the `system_depth_audit.md`
  finding that Gob-Ogre has a voting system with nothing to vote on and one decision in total.
- **Elven:** a Celestial Lord petitioning the Court.

### 3.3 Deepen vassal contracts — F7

Two to three obligations per government, against vanilla feudal's eleven. The structure is
correct and the contract types are properly defined, so this is depth rather than repair. Target
5–6 each, expressing the government's identity — Cartel a protection cut and territory rights,
PMC deployment terms and exclusivity.

---

## Phase 4 — Verification

Run after **each** phase, not only at the end.

1. **Tiger** — 64 errors / 195 warnings baseline. Investigate any delta. The known-benign classes
   (~48 faith/religion-path lookups, 24 culture-pillar lookups, 2 `error(filename)`) are Tiger
   1.17 vs CK3 1.19 artefacts documented in the alpha checklist — do not "fix" them.
2. **Reachability** — must stay 328/328, or match the new total after Phase 3.
3. **Self-cancellation** — no event whose own `trigger` re-checks a cooldown flag its on_action
   sets. This is the fault that silently killed 40 events; re-check after every on_action edit.
4. **Tier-coverage matrix** — a new check to build: for each government × each tier, count
   eligible events and decisions. No cell should be zero.
5. **In-game smoke test** — Tiger cannot see raid capability, accolades, AI behaviour or tone.
   Steps 1.1, 2.1, 2.2 and 2.4 all need an actual campaign.

---

## Sequencing and effort

| Order | Item | Effort | Payoff |
|---|---|---|---|
| 1 | 1.1 Fringe raid flag | Minutes | Repairs the mod's most identity-defining government |
| 2 | 0.1–0.4 assessment | Half a session | Prevents wrong rules landing in Phase 2 |
| 3 | 1.2 Re-gate 32 events | 1 session | Largest single content gain; no writing required |
| 4 | 2.1 `allow_accolades` | Minutes | Vanilla-standard parity |
| 5 | 2.2 `government_rules` | 1 session + testing | Closes the critical F1 |
| 6 | 2.4 `ai` blocks | 1 session | Makes 2.2 visible in AI play |
| 7 | 3.1 Elven + NC vassal events | 2–3 sessions | Closes the last tier gaps |
| 8 | 3.2 Vassal decisions | 1–2 sessions | Gives vassals agency, not just events |
| 9 | 2.3, 2.5, 1.3, 1.4, 3.3 | 1–2 sessions | Polish and vanilla parity |

**Dependencies:** 1.2 should follow 0.3; 2.4 should follow 2.2. Nothing here depends on Gate 1 of
the alpha checklist — all of it is testable in isolation *except* the in-game smoke tests, which
need a loadable world and therefore Gate 1.

---

## Explicitly out of scope

- `mechanic_type` and bespoke government UI — needs subsystems the mod does not have (see 2.6).
- Men-at-arms-dependent rules — blocked on `common/men_at_arms_types/` (alpha checklist, Gate 3).
- The 4 missing government types (Holy Imperium, Khanate, Conclave, Trade Council) — tracked in
  the alpha checklist; this plan covers only the 7 that exist.
- Nikios Khanate content — deferred by standing decision.
