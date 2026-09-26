# Closed Alpha Release Checklist — Echoes of the Grip

Audit: 2026-08-28, `main` @ 08f143e. Tiger 1.17.0 vs CK3 1.19.0.6 → 62 errors, 246 warnings.
Localization pass 2026-08-28: warnings 341 → 195 (−146); errors unchanged at 64, none introduced.
**Event wiring pass (2026-08-28) — RESOLVED.** The original "323 of 326 reachable" figure, and my own follow-up "326/326" after retiring the 3 orphans, were both wrong. A transitive pass from true roots found **75 unreachable events (23%)**, plus a second, quieter fault: **40 events that *were* wired but silently cancelled themselves**. Both are now fixed — **328 of 328 events reach the player.** Tiger unchanged at 64 errors / 195 warnings.
Missing-localization findings are now down to a single key, `mena_coa_gfx` (a vanilla CoA group referenced by 3 cultures — belongs to the Gate 3 coat-of-arms item, not to any event system).

**State in one line:** the setting systems are written and correctly wired; the world they run on is not.
326 events, 7 governments, 318 titles defined — and **0 titles that CK3 can parse, place, or assign a holder to**.
Work the gates in order; each unblocks testing for the next.

---

## Gate 1 — Make the galaxy exist

Nothing below this gate is testable. Until Gate 1 closes, launching the mod does not produce a playable world.

- [ ] **Rename every title key to a legal CK3 tier prefix** — BLOCKER
  CK3 reads a title's tier from the first two chars of the key. All titles are `eotg_e_` / `eotg_k_` / `eotg_d_` / `eotg_c_` / `eotg_b_`, which the engine cannot classify. Titles are the one identifier class where the tier prefix leads and `eotg_` follows: `e_eotg_myr_cluster`, `c_eotg_xerxes`, `b_eotg_thornspire`.
  *Tiger:* 81× `warning(validation): expected title`
  *Touches:* `common/landed_titles/`, `history/titles/`, `common/struggle/`, `common/decisions/`, `eotg_titles_l_english.yml` (611 lines)

- [ ] **Give all 287 baronies a `province =` ID** — BLOCKER
  No barony has one; there is no `map_data/` in the repo. A barony without a province is not a holding — not on the map, not holdable, and its county is not territory. Decide first: reskin vanilla's map, or ship our own.
  *Counted:* 1 empire, 6 kingdoms, 24 duchies, 80 counties, 287 baronies / 0 provinces
  *Also missing on every title:* `color`, `capital`

- [ ] **Resolve the empty `history/provinces` replace_path** — BLOCKER
  `descriptor.mod` declares `replace_path="history/provinces"` but no such folder ships. That deletes vanilla province history map-wide: every barony loses its holding, culture and faith. Author province history or drop the line.
  (`replace_path="history/wars"` is the same pattern but harmless — no wars intended at 866.)

- [ ] **Resolve the empty `common/dynasties` replace_path** — BLOCKER
  Same problem: descriptor replaces `common/dynasties`, mod defines none → all dynasties removed. All 24 `dynasty =` references in history are already commented out to work around it, so no house has a name, arms, or succession continuity.

- [ ] **Set title holders and governments in `history/titles/`** — BLOCKER
  `eotg_titles_866.txt` has **zero active `holder =` lines**. Every ownership block (Elrossi, New Cauldron, Trade League, Coldiron, Nikios, Angelia) is commented out; only county cultures are live. With `replace_path="history/titles"` also clearing vanilla, 866 has no rulers anywhere.
  *22 commented blocks, 6 TODOs in file.*

- [ ] **Fix culture/faith syntax on all 23 history characters** — BLOCKER
  Definitions use `culture = culture:eotg_culture_khadrashi` and `religion = faith:eotg_faith_coldiron`. The `culture:`/`faith:` scope prefixes belong inside effects; at definition level vanilla writes the bare key. Characters risk loading with no culture and no faith.
  *Tiger:* `warning(bookmarks)` — bookmark says `eotg_culture_aelvaryn`, history says `culture:eotg_culture_aelvaryn`
  *Affected:* 23 culture + 23 religion lines

- [ ] **Replace the TODO placeholder characters** — BLOCKER
  Great-power heads are still `name = "TODO_ElrossiEmperor"`, `name = "TODO_PrinceOfMyr"`. 23 characters exist for a bookmark needing rulers, heirs, councillors and claimants across 7+ nations.
  *Source material already written:* `docs/Bookmark-Characters`, `docs/bookmark-char-story` (79 KB)

- [ ] **Add the 8 missing bookmark characters** — MAJOR
  Bookmark screen offers one start (Vaelorin). Nine arcs are already written, wired in `eotg_bookmark_char_arcs_start`, and fully localized (550 lines in `eotg_bookmark_chars_l_english.yml`). Only the bookmark entries are missing — cheapest large win on the list.

---

## Gate 2 — Connect the setting systems to the player

Everything here is already written. These are the last hops — assignment, geography, text — that turn finished script into something visible. ~200 events currently sit behind flags no character has.

- [ ] **Assign the 7 governments to titles** — BLOCKER
  No title carries `government = eotg_*_government`, so all 7 government types are dead code at runtime. Behind them: ~200 flavor events, 34 decisions, 7 vassal contract groups, PMC council positions + tasks, the corporate scheme, 2 casus belli. Closes with Gate 1's holder pass.

- [ ] **Author the 4 missing government types** — MAJOR
  Named in the design doc and referenced by name in title history, but nonexistent: `eotg_government_holy_imperium` (Elrossi), `eotg_government_khanate` (Nikios), `eotg_government_conclave` (Angelia), `eotg_government_trade_council` (Gob-Ogre). Without them those nations fall back to vanilla feudalism. Defensible for alpha: ship the imperium + khanate, defer the rest, say so in the notes.

- [ ] **Give the Myr Cluster Wars a geographic region** — BLOCKER
  Struggle declares `regions = {}`. With no region it has no map footprint: county-based involvement, per-phase county effects, phase-restricted CBs and `involvement_prerequisite_percentage` are all inert — membership falls back to culture/faith lists alone. Define `eotg_region_myr_cluster` once baronies have provinces.
  *Working today:* 5 phases, 6 catalysts, `on_start`/`on_change_phase`/`on_join`, ignition seeded 850 AG

- [ ] **Decide the Fate of Iberia gate on the Myr Cluster Wars** — MAJOR
  `history/struggles/eotg_myr_struggle_history.txt` starts the struggle only under `has_dlc_feature = the_fate_of_iberia`. Testers without that DLC get no Cluster Wars at all, with nothing on screen explaining why. Either make the DLC a stated hard requirement, or add an event-driven fallback.

- [x] **Localize the Myr Cluster Wars, name included** — DONE 2026-08-28
  `localization/english/eotg_myr_struggle_l_english.yml`. Display name is **"The Myr Cluster Wars"**; internal key `eotg_myr_struggle` unchanged. Covers struggle name/desc, 5 phases + descs, 5 parameters, 7 phase-effect headers, the settlement decision (4 keys), the proxy-war interaction (3 keys), and all 40 event keys.
  Also localized two classes Tiger does **not** check but the player sees: the 6 catalysts (struggle window) and the 2 proxy opinion modifiers.

- [x] **Localize the Titan Exodus** — DONE 2026-08-28
  `localization/english/eotg_exodus_l_english.yml`. All 10 events (45 keys) plus the 6 modifiers with `_desc` on each.
  *Modifiers:* `refugee_strain`, `integrated_refugees`, `raider_scourge`, `fever_outbreak`, `pressed_levies`, `haven_reputation`

- [x] **Finish the Orrin's Grip opening sequence** — DONE 2026-08-28
  `localization/english/eotg_orrins_grip_l_english.yml`, all 16 keys.
  Correction to the earlier audit: `.0001` was **not** in fact localized. The keys in `eotg_l_english.yml` used the auto-generated `.0001.t` / `.0001.desc` form, but all three events name their keys explicitly (`eotg_orrins_grip_0001_title`), so the old keys could never render. They have been removed.

- [x] **Wire or retire the 3 orphan events** — DONE 2026-08-28
  All three retired and replaced with reachable events, so the flavor budget is unchanged. **The "326 of 326 reachable" claim originally written here was wrong** — see the correction at the top of this file and the audit item below. These three were the orphans the original audit happened to spot; a systematic pass found 75.
  *Why retire rather than wire:* none was an accidentally-dropped wire. `eotg_elven_court.0002`/`.0003` were notification events from an earlier design in which `.0001` branched outward; `.0001` now resolves those outcomes inline and notifies vassals via `send_interface_message`, so wiring them would have double-notified. (`.0002` was also `hidden = yes` while carrying a title and a named option — keys a hidden event can never display.) `eotg_cartel_tax.0004` needed a refusal accumulator that exists nowhere in the codebase.
  **Replacements, each wired into the yearly flavor on_action it belongs to:**
  - `eotg_elven_court.0005` — *The Court's Long Memory*. Fires while `eotg_elven_court_confirmed` holds: the Eternal Court treats a unanimous confirmation as an account opened, not closed. Honor the debt / refuse it / defer.
  - `eotg_elven_court.0006` — *A Throne the Court Did Not Choose*. Fires while `eotg_elven_court_contested` holds: compliance so correct and so slow it reads as a sentence. Buy the ratification / rule without it / outlast it.
  - `eotg_cartel_tax.0005` — *The Bosses Compare Notes*. Delivers `.0004`'s intended beat but counts defiant Bosses **live** via `any_vassal = { count >= 2 has_character_modifier = eotg_cartel_defiant_boss }`, so no accumulator is needed. Break the ringleader / buy them back / concede the cycle.
  *Also added:* 3 opinion modifiers (`eotg_elven_court_debt_honored`, `eotg_cartel_made_an_example`, `eotg_cartel_bought_back`), full loc for all three events, and the retired events' loc keys removed. The `eotg_cartel_shakedown_standoff_tooltip` key was kept alive by reusing it in `.0005`.
  *Retired IDs `.0002`, `.0003`, `.0004` are not to be reused* — noted in both event file headers.

- [x] **Unreachable / self-cancelling event audit — 115 events recovered** — DONE 2026-08-28
  Two independent faults were keeping **115 of 328 events** off the player's screen. Both fixed; **328 of 328 now reach the player.** Tiger unchanged at 64 errors / 195 warnings, nothing flagged in `eotg_on_actions.txt`.

  **Fault 1 — 75 events never wired.** Transitive reachability from true roots (every `trigger_event` in `common/` + `history/`, propagated through the event graph). Confirmed not a false positive: `common/schemes/`, `common/story_cycles/` and `common/character_interactions/` all count as roots, and the mod uses `trigger_event` exclusively — there is no `events = {}` or `random_events = {}` block in any on_action.

  **Fault 2 — 40 events wired but silently self-cancelling.** The worse of the two, because these looked correct. The on_action pattern was:
  `limit = { NOT = { has_character_flag = X_recent } }` → `add_character_flag = X_recent` → `trigger_event = { … days = 5 }`
  …while the event's **own** `trigger` block also re-checked `NOT = { has_character_flag = X_recent }`. The flag is set five days before the event evaluates, so the trigger was always false on arrival. Per `docs/CK3_Modding_Complete_Reference_v1_19.md` line 1262 — *"`trigger = {}` on an event is a re-evaluation guard. If it becomes false before the event fires, the event is silently cancelled."* — every one of these was cancelled with no log entry. This affected events already counted as "wired", so it was invisible to reachability analysis.
  *Fix:* removed the 98 redundant `NOT = { has_character_flag = *_recent }` lines from event trigger blocks across the 6 `*_expanded_events.txt` files, making the on_action the single cooldown authority — which is how the 45 already-working pairs were built. Event triggers keep all their substantive conditions.

  **What was reconnected**

  | Set | Events | How gated |
  |---|---:|---|
  | 6 government flavor sets | 58 | Each event's own trigger conditions lifted into its on_action `limit` (the government check is already supplied by the wrapping `if`), 25% chance, 4-year cooldown |
  | `eotg_fringe` | 11 | Individually gated — these carry **no** trigger blocks, so each `limit` was written to match the state its text describes |
  | `eotg_expulsion` | 6 | One hook; `.0001` self-gates and the rest chain from it |

  **Fringe gates** (written per-event, since nothing self-gates there): `.0001` post-war spoils (`eotg_fringe_was_at_war` + peace + captains + gold); `.0002` insubordination (a captain at negative opinion); `.0004` mutiny (`grip_critical`); `.0008` loot riots (post-war + empty treasury); `.0009` idle warbands (`peace_years >= 4`); `.0015` challenger (`grip_low`); `.0020` supply collapse (at war + `overextended`); `.0021` great plunder (`grip_high` + gold); `.0022` failed raid (`grip_low` + low gold); `.0026` traditionalist backlash (`reform_ready` + hostile captain); `.0029` Ghost Fleet.
  *New narrative link:* `.0029` explicitly describes ships lost in "the failed mutiny", so rather than gate it on ambient state it is now chained to `.0004` — holding firm against the mutiny sets `eotg_fringe_mutiny_failed` (15 yrs), which is what unlocks the Ghost Fleet legend.

  **Expulsion** (`eotg_expulsion.0001`, the file header's own long-standing TODO): wired into `eotg_on_yearly_elven_flavor` at 30%. Its `limit` is deliberately thin — the event already carries a full trigger (elven heritage + a non-elven sub-realm county + a neighbour to receive the displaced), and it sets its own 20-year `eotg_expulsion_edict_issued` flag in `immediate`. Setting a cooldown flag on the on_action side would have reproduced Fault 2 exactly.

  *Playable events per government, before → after:* PMC 23→32, Fringe 24→35, Corporation 23→33, Cartel 17→27, New Cauldron 18→28, Gob-Ogre 17→27, **Elven Monarchy 15→30** (the largest gain, and it was the thinnest government in `docs/system_depth_audit.md`).
  *Tuning note:* the 58 recovered flavor events use a uniform 25% / 4-year cadence, deliberately below the 20–50% of the originally-wired half, so doubling each set's pool does not double event frequency. This is the one number worth revisiting after play-testing.
---

## Gate 3 — Stop the setting reading as medieval Europe

These have no files at all. Each is a place vanilla CK3 shows through the conversion. Not all must ship in a closed alpha — but each deferral is something testers will report, so decide deliberately and record it.

- [ ] **Men-at-arms for a sci-fi setting** — MAJOR
  `common/men_at_arms_types/` absent → every army is vanilla pikemen, archers, heavy cavalry. Loudest remaining tonal break after the map. A first pass needs ~6–7 regiments. (PMC knights are already renamed **Operators** in loc — the naming layer exists, the units don't.)

- [ ] **Name lists for the 28 cultures** — MAJOR
  `common/culture/name_lists/` absent; all 28 cultures point at vanilla lists (roman, french, english, levantine, mongol, norse, sami). Aelvaryn, Khadrashi and Geldmark characters are named Marcus, Pierre, Olaf. Every ruler beyond the 23 scripted ones is generated, so this is what the player reads all campaign.

- [ ] **Coats of arms** — MAJOR
  No `common/coat_of_arms/`, no `gfx/coat_of_arms/`. With the empty dynasties folder, every realm is heraldically blank in the outliner, diplomacy screen, war overview and title view. Generated CoA from vanilla templates is an acceptable alpha answer; nothing is not. (Cultures already declare `coa_gfx = { western_coa_gfx }`.)

- [ ] **Holy sites for the 12 faiths** — MAJOR
  `common/religion/holy_site_types/` absent despite the descriptor replacing that path, and 2 dangling `holy_site` references. Faiths without holy sites lose pilgrimage, holy war targets, and much of their fervor/piety economy. Depends on the map pass (holy sites bind to baronies).

- [ ] **Write down the tech and building strategy** — MINOR
  No custom innovations, traditions or buildings; vanilla's medieval tech tree and holdings are reskinned purely through `localization/english/replace/` (45 override files). Legitimate alpha shortcut — but record it, so a tester who opens the innovation tree and finds Stirrups knows it was deferred, not broken.
  *Also absent:* `laws`, `court_positions`, `ethnicities`, `flavorization`, `game_rules`, `defines`

---

## Gate 4 — Clear the presentation floor

`gfx/` holds 11 files and all 11 are `.gitkeep`. Every icon the mod references is a missing-file warning. Placeholders close this gate — the point is that nothing renders as a blank square.

- [ ] **7 trait icons** — MAJOR
  `eotg_augmented`, `eotg_enhanced`, `eotg_overclocked`, `eotg_neurofractured`, `eotg_grip_survivor`, `eotg_void_touched`, `eotg_honorable_exit`

- [ ] **5 struggle phase icons** — MAJOR
  ignition, escalation, attrition, settlement, conclusion. The struggle window stays pinned open all campaign. Struggle illustration is currently a borrowed vanilla asset: `gfx/interface/illustrations/event_story/fp2_compromise.dds`

- [ ] **Bookmark screen art (4 files)** — MAJOR
  Bookmark illustration, start button, selection icon, Vaelorin's portrait frame. Multiply the last two by 9 once the other bookmark characters land.

- [ ] **Council task + interaction icons (3)** — MINOR
  `task_raise_levies`, `task_study_technology`, `icon_negotiate`. Last 3 missing-file warnings.

- [ ] **Re-run Tiger and commit the accepted baseline** — MINOR
  Separate the known-benign false positives from the real findings and commit that baseline, so the next run is a diff not a re-triage.
  *Known benign (Tiger 1.17 vs CK3 1.19):* ~48 faith/religion-path lookups, 24 culture lookups, 2 `error(filename)` on the 1.19 religion folders
  *Real and open:* 81 expected-title, 146 missing-localization, 19 missing-file

---

## Already alpha-ready — do not reopen

| System | State |
|---|---|
| **Cybernetic augmentation** | Most finished system in the mod. 4-tier trait chain, 3 decisions, 5 yearly on_action hooks, 21 events across 5 files, opinion + static modifiers, complete loc. Needs only icons. |
| **Government definitions** | All 7 properly built — holdings, contract groups, flags, character modifiers, colors — with 34 decisions, 7 obligation contract groups, full concept loc. Need assigning, not writing. |
| **Event corpus** | 326 events across 40 namespaces, 323 reachable. All 9 bookmark char arcs and all 7 government flavor sets written and fully localized. |
| **on_action wiring** | Clean. Vanilla hooks extended with additive `on_actions = { }` chains, never overwritten `effect = { }` blocks — exactly as the project rules require. |
| **Cultures and faiths** | 28 cultures with ethos/heritage/language/traditions/gfx; 11 religions, 12 faiths, 11 heritage + 10 language pillars. Structurally complete apart from name lists. |
| **Struggle architecture** | 5 phases with real transition conditions, 6 catalysts, an ending decision, start/phase-change/join hooks. Only its region and its text are missing. |
