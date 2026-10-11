# Architect Brief — Frontier Systems and the Unsworn Government (QA 2026-10-11)

**For:** `eotg-architect`. **From:** the QA assessment in [frontier_unsworn_qa.md](frontier_unsworn_qa.md) (read-only, at `0abde1d`, CK3 1.20.0.4). That report has the full evidence; this brief keeps only what **needs a design ruling or a spec change**. Pure script bugs and loc fixes that need no ruling go straight to the scripter and localizer, and are listed in §6 only so you can see the whole picture.

**Inputs:** [`docs/design/frontier_systems.md`](../design/frontier_systems.md) (intent; read-only for you), specs [`frontier_v1.md`](../specs/frontier_v1.md), [`frontier_v2.md`](../specs/frontier_v2.md), [`frontier_v3.md`](../specs/frontier_v3.md), [`frontier_unclaimed_regions.md`](../specs/frontier_unclaimed_regions.md), [`governments_v2.md`](../specs/governments_v2.md).

**Constraints every ruling keeps:**
- **Map-agnostic** (no title, province, culture or faith keys).
- **Invariant 5:** every flavor event reads or moves `eotg_frontier_progress`.
- **Hidden values** (`frontier_v1.md:85`): progress (0–100) and strain (0–8) are never shown as numbers; players see qualitative states only.
- **The text rules of `frontier_unclaimed_regions.md` §D** (LAW AT 866).
- **New events, options and beats are the human's call** (standing rule): propose them, don't spec them as decided.
- **Settle event-design questions from vanilla precedent**, and cite the file.

**What's already sound** (don't reopen):
- the county-title state machine and hand-off to vanilla outcomes;
- the 8 design hooks;
- the herder-pattern Unsworn placeholder;
- the trigger override, which matches vanilla byte for byte apart from its two marked lines;
- pacing of 6–16 years to Settled, which hits the owner's 10–16 unsponsored / 8–10 sponsored target.

---

## 1. Decisions needed, ranked

### A1. Settled city and church holdings produce nothing for most holders (HIGH, verified)
- **Where:** `common/scripted_effects/eotg_frontier_effects.txt` ~760–790 (completion results by type), `eotg_frontier_build_holding_effect` ~838–875.
- **Problem:** Settlement and Trade create a `city_holding`, Religious a `church_holding`, and the barony is given **directly to the county holder** (`change_title_holder` to `scope:eotg_frontier_holder`). Feudal, Cartel and PMC holders may only hold castles and temple-citadels (vanilla `common/governments/00_government_types.txt:18-19`; mod `eotg_cartel_government.txt:49-50`, `eotg_pmc_government.txt:37-38`). Vanilla then shows "Due to being the wrong holding type… the holding produces no levies or taxes" (`localization/english/holdings_l_english.yml:36`). The headline reward of 3 of 7 project types does nothing for most rulers.
- **Options:**
  1. **(Recommended)** When the holding type isn't valid for the holder, create a vassal to hold it: the settlers' leader as mayor (city), or an elder as bishop (church). Culture and faith come from the county by scope (the existing template pattern, `eotg_frontier_templates.txt`). Vanilla's own shape is cities and temples held by vassals. It also delivers design §7 ("Local Ruler ≠ Political Owner"), which today is never realized: .004 gives the founder only gold or prestige.
  2. Pick the holding type by the holder's government (a castle for feudal, a city for corporate). This is simpler, but it drops the project-type flavour.
  3. Keep it, and document a "no-yield" barony as intended. Not recommended.
- **Depends on:** in-game check **V8** (who actually holds the new barony). Write the rule so it is correct either way.
- **Also decide:** whether the new vassal is a courtier template, the founder (if not the holder), or a new character. Design §5–7 lean to the founder becoming the Local Ruler.

### A2. AI participation is near-inert (the biggest design gap)
- **Evidence:**
  - Establish runs at `ai_check_interval_by_tier` 48–60 months, a 10–35% `ai_will_do` (`eotg_frontier_decisions.txt:155-169`), and only with gold ≥ 2× `medium_gold_value`. The mean wait after a claim is **about 11–50 years (typically 25–35)**.
  - The map-wide cap is 8 active, with 1 per AI (`eotg_frontier_values.txt:230`).
  - Claiming has a worldwide 180-day gap (`eotg_unclaimed_values.txt:23`), so **2 claims a year**, against **about 0.5–0.7 Regions settled a year**.
  - The per-AI cap of 2 counts `eotg_unclaimed_claimed` forever (`eotg_unclaimed_triggers.txt:84-90`), so claimed-but-unestablished counties pile up.
  - AI holders get **no flavour events** (`eotg_frontier_effects.txt:644`).
  - **Result:** design §23 ("the galaxy builds itself") happens mostly where the player acts.
- **Rulings needed:**
  1. **Establish AI:** recommend `ai_will_do` 40–60 when the AI holds a claimed Unsettled county, a 24-month interval and a 1× gold gate. Vanilla 1.20 pattern: `ai_check_interval_by_tier` with conditional `ai_will_do` that goes to 0 or high.
  2. **Map cap:** scale it with the number of Unclaimed counties (for example 8 + 1 per 20 Unclaimed) instead of a flat 8.
  3. **Backlog:** either gate the AI claim interaction on affording claim plus Establish, or **close UD3/UQ11** (an AI-held claim that's never established lapses back to Unclaimed after N years; recommend 10, AI only). Recommend both.
  4. **AI Frontier life:** decide whether AI Frontiers get any scripted outcomes beyond sponsor offers (e.g. silent strain and progress rolls equivalent to the player's event pool) so AI projects can falter and recover. No player-visible events needed.
- **Verify with:** a 50-year observer run on the British Isles test sub-mod (161 Unsworn counties). Bands to judge against are yours to set; suggest Unclaimed share at year 30 and settled Regions per decade.

### A3. Event pacing: a per-ruler cap and same-day bursts (MEDIUM, verified)
- **Evidence:** the cooldown is per county (`eotg_frontier_event_cd`, 3 years, then a 50% roll; `eotg_frontier_effects.txt:642-660`). Every held Frontier ticks inside one `every_held_title` in the same `yearly_playable_pulse` (`eotg_frontier_on_actions.txt:35-46`), and events fire with no delay. That is about 2 events a year with 8 Frontiers and about 5 with 20, **all on one day**. The AI is capped (`frontier_v1.md:89`); players aren't.
- **Recommend:** a ruler-level marker allowing one flavour roll per ruler per pulse, plus `trigger_event = { … days = { 1 120 } }`. Events already re-check their state in their triggers, so a delay is safe.
- **Also rule on:** "funding removes the story". A fully funded project gets about 1.5 events in its life against about 3.0 bare. Either accept it, or key the roll to elapsed years rather than per tick.

### A4. Strain sources: war, and the founder gap (MEDIUM)
1. **War strain** (`eotg_frontier_effects.txt:530-537`): any war the holder is in, including a distant ally call, adds +1 a year, and a quiet year doesn't follow it. Eight war years fail any non-Military project, and CK3's AI is often at war. **Recommend:** strain only when the county is occupied or has hostile armies present, or when the holder is war leader or defender.
2. **Founder death:** a new founder can be named only through .002 (behind the 3-year cooldown) or .005, while "no founder" strain accrues yearly with no ease. **Recommend:** a founder's death clears `eotg_frontier_event_cd` for that county, or add an "Appoint a Founder" decision (a county-picker widget, the vanilla pattern already used in this file). The decision is the cleaner of the two.
3. **AI auto-founder** (`eotg_frontier_effects.txt:514-519`): a child or imprisoned AI holder is set as founder but fails `eotg_frontier_has_valid_founder` (`triggers.txt:65-78`), so the project fails from "no founder" strain alone. A script fix (limit to an adult, unimprisoned holder, else the best adult courtier); listed so the founder rules stay one design.

### A5. The .005 AI order: spec or code? (MEDIUM)
- `frontier_v1.md:538` (§6.6) sets the AI order: "d if possible; else b if gold ≥ 2×minor; else a". The script (`events/eotg_frontier_events.txt:914-989`) uses flat weights d 100 / b 50 / c 20 / a 10. The AI takes d only ~55% of the time, about 11% picks c (which isn't in the order), and b is gated at 1×.
- **Rule:** which is intended. If the spec stands, the scripter adds `modifier = { factor = 0 }` gates (vanilla `events/dlc/ep3/ep3_admin_events.txt:133,166`). If the weights stand, update §6.6.
- **Related drift:** §6.6(c) says the type is "re-picked from eligible", but the code forces `flag:settlement` (code and loc agree). Update the spec, or rule otherwise.

### A6. The Unsworn placeholder playability fallback (HIGH, gated on V-U1)
- Vanilla's `basic_is_valid_for_yearly_events_trigger` (`common/scripted_triggers/00_available_for_events_triggers.txt:802-816`) gates only on `is_playable_character`, and nothing in `eotg_unclaimed_government.txt` makes a placeholder unplayable. Spec mitigations **M2** (a second key-level override keeping placeholders out of vanilla yearly events) and **M3** (a lobby warning) are not built.
- **Rule now, so the scripter can act the day V-U1 reports:** confirm M2's exact override target and its scope. It goes in the same file and follows pitfalls §16, so the vanilla body is copied verbatim plus one marked line.
- Also decide how M3 surfaces: vanilla has no lobby hook for this, so it is probably an `on_game_start_after_lobby` check that warns or swaps the player.

### A7. Unsworn release and claim rules (MEDIUM)
1. **Capital guard** (`eotg_unclaimed_effects.txt:35`): `eotg_unclaimed_release_effect` doesn't enforce UQ5 (the capital stays with its holder). Only the separate trigger `eotg_unclaimed_would_release` does. The Frontier test sub-mod releases the Sardinian judges' counties directly, probably including their capitals. **Rule:** does the effect enforce UQ5 itself (recommended: skip `holder.capital_county` when the holder isn't Unsworn), or is it a documented precondition on callers?
2. **Non-capital baronies** (`:454-475` claim, `:135-153` create): only the county and its capital barony move. A placeholder holding another barony becomes a permanent, war-immune, un-vassalizable enclave. **Recommend:** both effects move every barony in the county held by the old placeholder, and the yearly sweep gets a rule that an Unsworn holder whose capital county isn't Unclaimed vanishes. Keep §10.5 (non-capital baronies `holding = none`) binding on the cartographer.
3. **Discoverability:** the claim exists only as a character interaction on a placeholder (`eotg_unclaimed_interactions.txt`, `icon_personal`). **Recommend:** add a "Raise Your Colours" **decision** using the county-picker widget. `eotg_decision_frontier_explore` already lists in-reach Unclaimed counties (`eotg_frontier_decisions.txt:970-976`). Keep the interaction.
4. **Blocked-war feedback:** spec §14 names `eotg_unclaimed_defender_tt`, which isn't built. The defender line in the override has no `custom_tooltip`, so a blocked declaration shows auto-generated trigger text. Confirm it's still wanted, and that it may sit inside the override (it changes the override's text only for the Unsworn branch).

### A8. Legibility and sponsor value (MEDIUM; must respect the hidden-value rule)
- **Legibility:** no surface shows what drives progress, how far along a project is, or strain, except .002's description bands.
  - **Recommend** qualitative bands in the Invest, Build and county-modifier tooltips: "work is slow / steady / fast", "about a decade remains / a few years / nearly settled", "the settlers are strained". These are customizable-localization or triggered descs, never numbers, consistent with `frontier_v1.md:85`.
- **Sponsor economics:** investing gives +5 per `minor_gold_value` against a sponsor's +3 per minor paid (`eotg_frontier_values.txt:177-183, 217`), and the sponsor gets nothing back but opinion.
  - **Recommend:** raise the sponsor input (e.g. +10 before pacing).
  - **Recommend:** give the sponsor a completion reward (prestige plus opinion, or a share of the settled Region's 25-year modifier).

### A9. Vocabulary rulings (for the lore-keeper and localizer)
1. **"Pressure":** it is the player word for Frontier strain at frontier loc lines 93, 96, 132, 290 and 365. v1 Void owns "Void Pressure", and cybernetics was already moved off it. **Rule who owns "pressure"** alongside `void_lift_plan_cloud.md` §3c. Recommend Frontier uses **"strain"**, which matches the variable. The literal "pressure seal" (line 83) stays.
2. **"Frontier Legacy: Trade/Industry/Defence/Learning/Faith"** (loc 197–206): collides with vanilla dynasty Legacies and the mod's Confluence Legacies. Recommend **"Frontier Roots: …"**. Avoid "Heritage", which is vanilla's culture pillar. Keys can stay.

### A10. Modularity (LOW, ruling only)
- Design §2.1 says Frontier must not depend on other systems. There are 17 live Unclaimed references inside Frontier core:
  - `eotg_frontier_triggers.txt:41, 271-272, 288`
  - `eotg_frontier_effects.txt:691, 1715, 1795-1812`
  - `eotg_frontier_decisions.txt:515-516, 928, 971`
  - `eotg_frontier_on_actions.txt:32, 64`
  - `events/eotg_frontier_events.txt:907-908`

  Frontier won't load without the Unclaimed files.
- **Rule:** route them through one documented seam file owned by Unclaimed (e.g. scripted triggers and effects Frontier calls, which Unclaimed defines), or record the coupling as accepted in `frontier_unclaimed_regions.md`.

### A11. Smaller rulings
- **Abandon −1 development:** it is keyed to `milestone >= 1`, not to development granted this attempt (`eotg_frontier_effects.txt:966-968`), so repeated resettle/abandon cycles drain development. Re-confirm "Abandon keeps its −1" (`frontier_v1_verification.md:101`), or key it to this attempt's grant.
- **Holy-order variables:** a holy order is stored in a county variable (`eotg_frontier_effects.txt:1639`). Faith-valued variables have vanilla precedent; holy-order-valued ones don't. Approve the `?=` fall-through to the lapse branch, or store the order's leader instead.
- **Danger counters:** the escort and garrison tooltips claim they neutralize danger, but the raider event (.034) keeps its +10 weight for Dangerous Regions (`eotg_frontier_effects.txt:1404`), unlike the beacon's −5 for Remote. Rule whether the escort and garrison counter the event weight. Recommended: −5 each, matching the beacon.

---

## 2. Content gaps (proposals for the human, not specs)
Design §11 coverage:
- **Positive:** 3 of 7. Missing: population growth, a skilled settler, an infrastructure breakthrough, a trade route.
- **Negative:** 3 of 8. Missing: disease, hostile inhabitants, collapse, shortage. Raiders exist only as description lines in .002.
- **Political:** 3 of 6. Missing: the founder disputes ownership, a religious dispute, cultural tension.

**Option quality:** all 71 options have fixed outcomes. There are **0 trait-gated options and 0 `stress_impact`**, and only 14 of 36 personality traits appear, in AI weights only.

**Cheapest first step (no new events):** add `stress_impact` to the morally loaded options (.033.a driving exhausted crews, .005.a abandoning settlers, .031.a) and skill-weighted `random_list` outcomes to existing events. `event_quality_v1.md:698` (B12) planned only a light pass here.

**Other design-brief gaps:**
- the founder is auto-picked (design §5 wants adventurers, dynasty members and merchants as candidates);
- Research projects yield no technology or innovation;
- no vanilla buildings are placed on completion;
- a .005 "lead it yourself" option, which .002.e offers but .005 doesn't.

Frame these as suggestions for the human to approve before any spec.

---

## 3. In-game checks that gate your rulings
Run in this order, **after the main session links the test sub-mod to the repo**. The installed `eotg_test_frontier_vanilla` is a stale 2026-10-05 copy that doesn't release Sardinia or mark Unknown counties.

| Check | Gates |
|---|---|
| **V-U1** — can a placeholder be played or picked in the lobby? | A6 |
| **V8** — who holds the new barony at completion; is it dead for a feudal holder? | A1 |
| **V-U14** — do placeholders count as `neighboring_rulers` (for vassal actors too)? | A2 (do AI claims happen at all?) |
| **V-U9 / V-U8** — `on_title_gain` on scripted transfers; transfers inside `on_death` | A7 |
| **V-U3** — `supply_limit_mult_for_others` actually affects other governments' armies | Unsworn attrition (owner decision UQ7) |
| **V-U15** — a release from a corporate holder (the `use_as_base_on_landed` flash) | A7 |

---

## 4. Suggested output
One amendment spec, e.g. `docs/specs/frontier_v4.md` (or a `frontier_v3.md` amendment plus a `frontier_unclaimed_regions.md` amendment), covering A1–A8 and A10–A11. Put A9 in a short loc and lore note. Batch the A6 work so it ships the day V-U1 reports. Keep §2 as a proposal list for the human.

## 5. Not for you (FYI; scripter and localizer act directly)
- **Scripter:**
  - "Back a Frontier" has no cooldown (add `cooldown = { years = 1 }`);
  - .004.a pays gold at root's scale but credits it at the founder's (save the value first);
  - .004.b hard-codes prestige (use script values);
  - Unsworn `change_government` should run after `becomes_independent`;
  - the yearly Unsworn sweep walks `every_living_character` (track holders in a global list instead).
- **Localizer:** four lines that promise what the script doesn't do:
  - the abandon decision ("What was built stays");
  - the claim tooltip ("You may now Establish", while the Region is Unknown);
  - .040's military description (conquest phrasing; the company actually backs you);
  - .030's "better terms" with identical mechanics.

  Plus casing and term consistency. GQF-001 is not a bug: close it. The glossary is Barony→System, County→Region.

---

### HANDOFF
- status: done
- next: eotg-architect
- ask: Rule on A1–A11 and write an amendment spec (Frontier + Unclaimed) from this brief; send A9 to the lore-keeper and localizer; return §2 to the human as proposals.
- files: docs/qa/frontier_unsworn_architect_brief.md, docs/qa/frontier_unsworn_qa.md
- needs-loc: A9 renames ("strain", "Frontier Roots"), A8 qualitative bands, A7 `eotg_unclaimed_defender_tt` and the "Raise Your Colours" decision keys
- needs-lore: who owns "pressure" (with void_lift_plan_cloud.md §3c); "Frontier Roots" naming
- needs-human: link the Frontier test sub-mod to the repo; in-game checks V-U1, V8, V-U14 (§3); approve or decline the §2 content proposals
