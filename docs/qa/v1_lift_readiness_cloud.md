# v1 Lift-Readiness Audit (cloud)

> **STATIC, UNVALIDATED.** This audit came from a cloud session with no game files, no Tiger and no PX, and nothing was run in game. Every finding comes from reading `OLD PROJECT VERSION/` and the v2 root. Anything that depends on how the engine behaves is marked `UNVERIFIED-VANILLA`.

**Date:** 2026-10-04 · **Branch:** `claude/focused-dirac-ixo81h` (on `v2-space-map`) · **Scope:** every row in the **lift** column of `OLD VERSION CATALOG.md` §5.

**Not opened, by instruction:** `common/*/eotg_augmentation_*`, `events/eotg_augmentation_*`, `docs/specs/cybernetics_*`, `gfx/`, `map_data/`, and their v1 copies. The v2 augmentation loc was used only for exact-key collision lookups. **Augmentation is not audited:** it was lifted on 2026-10-02 and rebuilt as cybernetics v2.

**Method:**
- **Mechanical sweeps (mine), over all 84 non-augmentation v1 loc files and all v1 script:**
  - the dead hook;
  - title-key and DLC greps;
  - BOM, header, `:0`, `[scope:`;
  - duplicate keys and v2 collisions.
- **Per-system review:** five read-only reviewers worked to one checklist (A–J): inventory, dependencies, dead hooks, identifier hygiene, map coupling, event reachability and coupling, loc, v2 collisions, canon, verdict. The checklist was built from `CLAUDE.md` invariants 1–9, catalog §4 lessons 1–13 and `docs/pitfalls.md`.
- **Verification:** I re-read the cited lines for every BLOCKER and for at least one HIGH per system.

**Owners:** scripter · localizer · cartographer · architect · lore-keeper · vanilla-scout · human · orchestrator.

---

## 0. Verdicts

| Lift-column row | Verdict | Blockers | H | M | L | Fix-list size |
|---|---|---|---|---|---|---|
| Augmentation | **already lifted** (cybernetics v2) | — | — | — | — | out of scope |
| Void Corruption | **READY-WITH-FIXES**. The cult branch is blocked by B-FAITHS. | 0 | 6 | 9 | 7 | ~8 script fixes, 2 bugs, ~7 loc/canon rewrites, 3 architect/lore calls |
| Confluence Legacies v1 | **READY-WITH-FIXES** | 0 | 4 | 4 | 6 | ~9 script edits plus a 6–12 string loc pass after a lore ruling |
| Cultures + pillars | **READY-WITH-FIXES** as a `# STOPGAP` lift (`docs/agent_workflow.md:56`) | 0 | 0 | 4 | 5 | ~7 small |
| Religions / faiths / families + god loc | **READY-WITH-FIXES** as a stopgap, without the Nikios faith. Holy sites and HoF titles are blocked by Gate 1. | 0 | 2 | 5 | 4 | ~10 |
| Men-at-arms types | **READY-WITH-FIXES** | 0 | 0 | 5 | 3 | ~4 |
| Struggle definition | **BLOCKED** by B-CULTURES, B-FAITHS, a Gate 1 region and the DLC-gate decision | 4 | 3 | 3 | 6 | ~6 script fixes once unblocked |
| Scripted effects / triggers / script values | **BLOCKED** for the 21 government files. **DROP** the 2 generic files. The rest go with their own systems. | 1 | 1 | 4 | 4 | — |
| `localization/english/replace/` | **READY-WITH-FIXES** for 49 of 52 files. 3 are **BLOCKED** on a vocabulary ruling. | 1 | 2 | 4 | 5 | ~250 key edits |
| Docs: SETTING LORE, 866_bookmark_design, 866_religions | **BLOCKED** on human canon rulings (copying is trivial) | 0 | 4 | 6 | 5 | ~6 rulings, ~8 text fixes |
| Docs: localization_crusade | **READY-WITH-FIXES** once the `replace/` rulings land | (counted with the docs row above) | | | | |

**Totals:** 6 BLOCKER, 22 HIGH, 44 MEDIUM, 45 LOW.

**Lift now (no human input needed):**
1. Void, without the cult branch.
2. Legacies, without the 7 history-character seeds and the Exodus tie-in.
3. Men-at-arms.
4. Cultures and religions as marked stopgaps, Nikios cut.

**Human rulings needed:** listed in §3.

---

## 1. Cross-cutting (mechanical sweeps)

| # | Sev | Finding | Where | Owner |
|---|---|---|---|---|
| X1 | HIGH | **Dead hook (lesson 13, CB-10).** These files extend `on_yearly_playable`, which never fires: | `OLD PROJECT VERSION/common/on_action/eotg_on_actions.txt:11`; `eotg_legacy_on_actions.txt:7` | scripter |
| | | • the hub, which carries Void (`:11-13`, parent `:76-84`), Myr (`:33`) and Exodus; | | |
| | | • Legacies. | | |
| | | Every lifted on_action needs `yearly_playable_pulse = { on_actions = { … } }` in its own file, not the hub. Then run `px_vocab_check.py`. | | |
| X2 | MEDIUM | **Catalog §5 is stale.** It says `common/struggle/` and `common/decisions/` reference `eotg_[ekdcb]_` title keys. A grep finds 0 hits there. The only hits are in the rewrite column: | `eotg_titles_l_english.yml` (509 hits), `common/landed_titles/` (399), `history/titles/` (89), `history/characters/` (5), and a comment at `replace/eotg_title_tiers_l_english.yml:36` | orchestrator (fix catalog §5) |
| | | Also, `eotg_proxy_war` is the Corporation government's CB, not the struggle's, and the government effect, trigger and value files are not lift-as-is (S3). | | |
| X3 | — | **Loc mechanics: clean.** | 84 files, 5,206 keys | — |
| | | • Every file has the BOM, the `l_english:` header and no `[scope:`. | | |
| | | • 0 keys collide with v2 `eotg_augmentation_l_english.yml`. | | |
| | | • 4 lines use `:1`: `replace/eotg_sin_sermon_serf_misc_l_english.yml:109,117,161` and `replace/eotg_stewardship_serf_misc_l_english.yml:80` (harmless). | | |
| | | • Duplicate keys exist only in `replace/` (R1). | | |
| X4 | — | **DLC gates:** only one, `history/struggles/eotg_myr_struggle_history.txt:10` (S2-B4). | | |
| X5 | — | **v2 collisions:** none. v2 has no culture, religion, MAA, struggle, script-value or Void/Legacy identifiers. | | |

---

## 2. Per system
File paths are under `OLD PROJECT VERSION/` unless they start with a v2 path.

### V. Void Corruption: READY-WITH-FIXES
**Inventory:**
- **Events:** 15, namespace `eotg_void`, in `events/eotg_void_{whispers,touched_events,hollowing}.txt`.
- **Script:** 5 on_actions, 3 decisions, 2 traits, 9 modifiers, 5 opinion modifiers, 11 effects and 14 triggers, in `common/*/eotg_void_*`.
- **Loc:** 139 keys.
- **Blocks to extract from shared files:**
  - hub `eotg_on_actions.txt:11-13,76-84`;
  - `eotg_traits.txt:25-40` (`eotg_void_touched`);
  - `eotg_modifiers.txt:7-14` (`eotg_mod_void_aura`);
  - `eotg_l_english.yml:7-9,12`.
- 0 orphans. Lesson 5 holds.

| Sev | Where | Finding | Fix | Owner |
|---|---|---|---|---|
| HIGH | hub `eotg_on_actions.txt:11-13` | X1: the whole system sits on the dead hook. | New `eotg_void_on_actions.txt` registration on `yearly_playable_pulse`. | scripter |
| HIGH | `eotg_void_effects.txt:90`, `eotg_void_triggers.txt:40`, `eotg_void_whispers.txt:135,425` | Depends on trait `eotg_grip_survivor` (`eotg_traits.txt:10`), which isn't in v2 and is shared with the rewrite-column history characters. | Decide who owns the trait: lift it with Void, or cut the bloodline branches. | architect → scripter |
| HIGH | `eotg_void_triggers.txt:50-52` | Faith key `eotg_religion_void_reverence` drives the cult branch at 11 sites. This is B-FAITHS, and it breaks the map-agnostic rule. | Doctrine or tenet check (as CB-12), or `always = no` until faiths exist. | architect → scripter |
| HIGH ✔ | `eotg_void_effects.txt:69-71` against `eotg_void_triggers.txt:74-79` | **Bug:** shelter sets the Voidwalker flag on the **ruler**, but the trigger looks for it on `any_courtier`. So the Voidwalker Ward decision never shows, the −6 accrual never applies, and event 0004 can repeat at −100 piety each time. | Create a flagged Voidwalker courtier (character template). | scripter |
| HIGH | loc `eotg_void_l_english.yml:93,94,49,36-37` (plus script comments) | Contradicts the Orrin ERRATA. The narration states as fact that Orrin is "sealed", and that something waits "on the other side of the seal". The opinion modifiers "Marked/Refused by the Eye" read as fact. | Frame it as the cult's belief; keep the narration agnostic. | lore-keeper → localizer |
| HIGH ✔ | loc `:93,94,95` (also `:30,110,140,155-156`) | **Register drift onto the cybernetic voice (CB-11):** the Bargain arrives "in your own interior language … indistinguishable from your own thought". | Make the Void external: through the floor, the scar or the seal. | architect → localizer |
| MED | loc `:15,20`; key `eotg_mod_void_pressure` (`eotg_void_modifiers.txt:23`; `eotg_void_effects.txt:41,50,199`) | "Void Pressure" vocabulary (QA round 2 §3.2). | Rename the band, or rule that "pressure" belongs to Void now that cybernetics uses "static". | architect → localizer + scripter |
| MED | `eotg_void_touched_events.txt:138,244,501` | Unprefixed saved scopes `void_child`, `void_confessor`, `void_vassal` (invariant 1). | Prefix them with `eotg_`. | scripter |
| MED | `eotg_void_hollowing.txt:116-187,196-291` | 0031 and 0032 never read or move `eotg_void_exposure`. 17 of 56 options don't touch it (invariant 5). | Rule that the trait is the resource after Hollowing, or add a stage-D variable. | architect |
| MED | `eotg_void_hollowing.txt:77-94`; `eotg_void_touched_events.txt:182-194,280-299` | Options promise more than they do: 0030.c "Abdicate" doesn't abdicate; 0021.c doesn't foster; 0022.c "silenced" only applies an opinion. | Make them real, or reword. | scripter / localizer |
| MED | loc `:65,93,94,125` | "Eight hundred and sixty-six years" is hard-coded and goes stale after 866. | Vaguer wording. | localizer |
| MED | `eotg_void_effects.txt:215-245` | Insight +2 skill modifiers can be re-applied repeatedly (commune decision every 10 years; stacking is `UNVERIFIED-VANILLA`). | Guard on the modifier being present. | scripter |
| MED | `eotg_scripted_effects.txt:10-26` | `eotg_se_apply/remove_void_corruption` bypass the exposure state machine. They have no callers. | Don't lift them. | scripter |
| MED | `eotg_void_traits.txt:17,37`; `eotg_traits.txt:29` | No trait icons. Modifiers and decisions use vanilla placeholders (lesson 11). | B-ART. | human |
| MED | SETTING LORE `:127,218` | Lore has Voidwalkers *worshipping* the Void; v1 casts them as its wardens. | Ruling. | lore-keeper |
| LOW | various | Unused identifiers: flag `eotg_flag_void_bargain_offered`; triggers `eotg_st_is_void_hollowed`, `_void_rift_contact`, `_void_resists`; trait flags. | Prune. | scripter |
| LOW | various | `eotg_mod_void_aura_desc` is missing. | Add it. | localizer |
| LOW | `eotg_void_triggers.txt:105-107` | The defiance comment doesn't match the behaviour. | Fix the comment. | scripter |
| LOW | various | British spellings (v2 text is American). | Respell. | localizer |
| LOW | loc `:155` | "a Tuesday" is a real-world weekday. | Reword. | localizer |
| LOW | various | "Hollowed" is used for both a trait and an opinion modifier. | Rename one. | localizer |
| LOW | various | Engine names to confirm: themes, `advantage`, `max_hostile_schemes_add`, `every_knight`, `lunatic_1`, `possessed_1` (`UNVERIFIED-VANILLA`). | Check against vanilla. | vanilla-scout |

### L. Confluence Legacies v1: READY-WITH-FIXES
**Inventory:**
- **Events:** 16, namespace `eotg_legacy`.
- **Script:** 1 decision, 10 effects, 17 triggers, 11 modifiers, 4 opinion modifiers, 3 hook extensions and 3 custom on_actions.
- **Loc:** 127 keys.
- **Docs:** the pitch doc.
- Self-contained: no blocks in shared files. 0 orphans. Lesson 5 holds. All keys present.

| Sev | Where | Finding | Fix | Owner |
|---|---|---|---|---|
| HIGH ✔ | `common/on_action/eotg_legacy_on_actions.txt:7` | Dead hook (X1). The aftermath pool, attention decay and the Exodus path never ran in v1. | `yearly_playable_pulse`. | scripter |
| HIGH ✔ | `eotg_legacy_on_actions.txt:189-201` | Hard-codes 7 history characters (`eotg_char_20001`, `10002`, `30001`, `40001`, `90002`, `90001`, `90003`), which breaks the temporary-map rule. They are no-ops at runtime behind an `exists` guard (`eotg_legacy_effects.txt:151`). | Lift without them; re-add as bookmark seeding after Gate 1. | scripter → cartographer |
| HIGH | `eotg_legacy_on_actions.txt:43-58` | Uses `eotg_exodus_haven_reputation` (`eotg_exodus_modifiers.txt:57`). Titan Exodus is in neither catalog column and isn't in v2. This was the only passive discovery path. | Drop it; add a taskboard item "re-add with Exodus". | scripter + orchestrator |
| HIGH ✔ | loc `eotg_legacy_l_english.yml:21,58,74,137,139,155`; pitch `:5` | **Canon:** the buried sites are called "Second Era" and "eight centuries" old. SETTING LORE `:85` puts the Second Era at ~131–850 AG, *after* the Grip, so the text contradicts itself. "The Confluence" (loc 13–15, 143–149) and "Hell's administrative layers" (93, 141) aren't in canon. | Ruling, likely "pre-Grip"; send the terms to the vault; rewrite the loc. | lore-keeper / human → localizer |
| MED | `common/decisions/eotg_legacy_decisions.txt:56-58` | The survey fallback can re-seed a county that already has a site. Seeding resets its state and leaves the old county modifier on. | Add `NOT = { eotg_st_legacy_site = yes }`. | scripter |
| MED | `eotg_legacy_effects.txt:102-112` | 0104 "Exhausted Legacy" fires again on every further integrity loss at 0. | Fire only when crossing to 0. | scripter |
| MED | `eotg_legacy_on_actions.txt:32-39,69-75,97-102,124-133` | `every_sub_realm_county` runs on the yearly pulse for every ruler (performance). | Iterate held county titles instead (`UNVERIFIED-VANILLA` names). | scripter |
| MED | `events/eotg_legacy_events.txt:247-263` | 0004 "Honest Geology" is a vignette that only gives +10 prestige (invariant 5). | Nudge attention or seed odds. | scripter |
| LOW | `events/eotg_legacy_events.txt:171` | Direct `add_trait = wounded_1`. | Use `increase_wounds_effect` (`UNVERIFIED-VANILLA`). | scripter |
| LOW | `events/eotg_legacy_events.txt:611-619` | 0021 always creates `eotg_legacy_heir`, who is then never used (orphan character). | Create only when needed, or use the character. | scripter |
| LOW | various | Dead definitions: opinion `eotg_legacy_enclave_protected`, triggers `eotg_st_legacy_site`, `eotg_st_holds_known_legacy`. | Use or cut. | scripter |
| LOW | `eotg_legacy_triggers.txt:74-126` | 8 generic `eotg_st_edu_*` helpers live in a system file and will invite duplicates. | Move to a shared triggers file. | architect |
| LOW | various | Redundant gold check. | Remove one. | scripter |
| LOW | various | `monthly_county_control_decline_add` and the hook names `on_title_gain` / `on_game_start_after_lobby` need confirming (`UNVERIFIED-VANILLA`). | Check against vanilla. | vanilla-scout |

**Testability caveat:** the system does nothing until landed characters exist, and v2 has no `history/`. Either Gate 1 closes, or the human classifies Legacies as mod-exclusive and testable on the temporary map. The taskboard lists it as Gate 2/3 (CB-10).

### C. Cultures + pillars: READY-WITH-FIXES (stopgap)
**Inventory:** 28 cultures, 11 heritages, 10 languages. Loc: 112 + 74 keys, all complete. `intake/regions/` and `intake/setting/` hold only `.gitkeep` ✔, so there are no briefs to diverge from. `docs/agent_workflow.md:56` ✔ allows a lift marked `# STOPGAP: replace from briefs`.

| Sev | Where | Finding | Fix | Owner |
|---|---|---|---|---|
| MED | `common/culture/cultures/eotg_cultures.txt` (28 `name_list =`) | All point at vanilla lists (roman ×7, english ×7, …), so testers saw "Marcus" (`docs/closed_alpha_checklist.md:126-127`). | Keep as a marked stopgap; build `name_lists/` from briefs. The intake template asks for 60+ names per sex. | scripter + localizer via intake |
| MED | every culture and pillar block | No STOPGAP marks. | Add `# STOPGAP: replace from briefs`. | scripter |
| MED | `common/culture/pillars/eotg_pillars.txt` | Language colours are vanilla named colours, including a suspect `trojan` (`UNVERIFIED-VANILLA`). | Confirm, or use RGB. | vanilla-scout → scripter |
| MED | — | CB-17 can key on mod-defined `eotg_heritage_*` pillars. It is still culture-coupled, so it stays post-map. | No lift action. | architect |
| LOW | `eotg_cultures.txt` | Ethnicities `caucasian_northern/_southern`. Non-human peoples render as humans. | Confirm the keys (`UNVERIFIED-VANILLA`); B-ART. | vanilla-scout / human |
| LOW | `eotg_cultures.txt` | DLC-prefixed traditions `tradition_fp2_ritualised_friendship` and `tradition_fp3_frontier_warriors` (`:132,199`). | Confirm they work without the DLC (`UNVERIFIED-VANILLA`). | vanilla-scout |
| LOW | `eotg_cultures.txt` | Terrain traditions (`seafaring` ×7, `mountain_homes`, …) are inert on a space map. | Review. | architect |
| LOW | `eotg_cultures.txt:3,201,337`; `eotg_heritage_l_english.yml:68` | Comment drift, and "Transit League" (elsewhere "Trade League"). | Fix. | localizer |
| LOW | `localization/english/eotg_names_l_english.yml` | Belongs with history/characters, not cultures. | Lift it there. | — |
| LOW | `eotg_heritage_l_english.yml:20-21,55-56` | Helix framed as remnants depends on CB-06. | Wait for the ruling. | human → lore-keeper |

### R. Religions / faiths / families + god loc: READY-WITH-FIXES (stopgap, Nikios cut)
**Inventory:**
- 4 families, each with `hostility_doctrine` ✔ (lesson 8).
- 12 religions, each with 20 doctrines.
- 13 faiths, each with 3 tenets at faith level ✔.
- Loc: 104 + 556 keys. All 548 god-loc keys referenced by script are defined.
- No `title:` or `province` references.

| Sev | Where | Finding | Fix | Owner |
|---|---|---|---|---|
| HIGH ✔ | `common/religion/religion_types/eotg_religions.txt:562-746`; loc `eotg_religions_l_english.yml:71-79`, `:23`; `eotg_religion_gods_l_english.yml:243-280` | `eotg_religion_stampede`, the "Centaur faith of the Nikios Khanate" (invariant 9). Nothing else references it. | Exclude it (leaving 11 religions and 12 faiths); trim the centaur sentence from the `eotg_rf_ancestral` desc. | scripter + localizer |
| HIGH | the whole file | Tiger 1.17 never parsed `religion_types/` (`docs/866_religions:336-343`), so 59 doctrine, 25 tenet and 30 trait keys are unchecked. Most suspect: `tenet_sacred_destruction` (`:1106`), `tenet_pursuit_of_power` (`:2215`), `tenet_pursuit_of_knowledge`, `tenet_adaptive` (`UNVERIFIED-VANILLA`). | One vanilla-scout pass before the lift. | vanilla-scout → scripter |
| MED | `eotg_religions.txt:14` and others | `doctrine_temporal_head` / `_spiritual_head` on 4 faiths, but no `religious_head` title exists (Gate 1). | Add head titles after Gate 1. | cartographer → scripter |
| MED | `eotg_religions.txt:189-190` (commented) | No holy sites (lesson 11). Don't add a `replace_path` for `holy_site_types` until the folder ships (invariant 3). | Build after Gate 1. | cartographer + scripter |
| MED | `eotg_religions.txt:1472-1474` | CB-12: Industrial Survivalism's tenets are all shared with other faiths, so there is nothing machine-sacred to key on. | Decide on a mod-defined doctrine or tenet. | architect |
| MED | — | STOPGAP marks needed (`agent_workflow.md:56`). | Add them. | scripter |
| MED | `eotg_religions_l_english.yml:123` | "Helix remnants" depends on CB-06. | Wait for the ruling. | human |
| LOW | `eotg_religion_families.txt:16-46` | Borrows `christian_gfx` / `pagan_gfx`; no faith icons. `docs/art_needed.txt:620` cites the stale `religions/` path. | B-ART; fix the path. | human |
| LOW | — | No holy orders or reserved names. | Accepted gap. | — |
| LOW | `eotg_religion_families.txt:12`; `eotg_religions.txt:1960` | Canon tensions: Malvrick as a Son of Yu but in titan worship; Deep Warren lists Elross as evil. | Ruling. | lore-keeper |
| LOW | `closed_alpha_checklist.md:172` | Count drift ("11/12" vs 12/13). | Correct the count. | — |

### M. Men-at-arms types: READY-WITH-FIXES
**Inventory:** 8 types in `common/men_at_arms_types/eotg_maa_types.txt`, 16 loc keys. No events or hooks, no culture or innovation gates.

| Sev | Where | Finding | Fix | Owner |
|---|---|---|---|---|
| MED ✔ | `eotg_maa_types.txt:275-280` | Operators' `can_recruit` needs `government_has_flag = eotg_government_is_pmc/_corporate`. Those flags only exist on v1 governments (rewrite column), so Operators load but can never be recruited. Gob-Corp would also qualify. | Lift as a forward reference noted in the government spec, or hold Operators back. | architect → scripter |
| MED | `:282-284` | `government_allows = subject_men_at_arms` (`UNVERIFIED-VANILLA`). | Confirm. | vanilla-scout |
| MED | `:33-36,66-70,100-105,135-139,170-176,206-211,264-268` | Terrain bonuses use vanilla terrain keys. Valid only if the v2 map keeps those keys. | Confirm against the v2 map. | cartographer → scripter |
| MED | `replace/eotg_mounts_ui_l_english.yml:53-54` | Vanilla `horse_archers` is renamed "Strike Speeders", the same name as `eotg_maa_strike_speeders`, so two units would share a name. | Rename one. | localizer |
| MED | `eotg_maa_types.txt:4-5` against `eotg_maa_l_english.yml:9` | The loc promises "no horses, no bowmen", but vanilla MAA stay recruitable. | Decide whether to hide vanilla MAA. | human → architect |
| LOW | various | Icons and illustrations use vanilla regiment keys; `illustration` / `ai_quality` field shapes are `UNVERIFIED-VANILLA`. | Confirm; B-ART. | vanilla-scout / human |
| LOW | — | No unlock gating ("rare" walkers available on day one). | Design note. | architect |
| LOW | — | MAA is a Gate 3 item but references no titles, cultures or faiths, so it arguably qualifies as mod-exclusive. | Human ruling. | human |

### S. Myr Cluster Wars struggle: BLOCKED
**Inventory:**
- 1 struggle (5 phases), 6 catalysts, history seed.
- 9 events, 1 decision, 1 interaction, 1 modifier, 2 opinion modifiers, 1 effect, 2 triggers.
- Loc: 86 keys.
- Hub blocks: `eotg_on_actions.txt:33,42,67,2372-2508`.
- Inbound calls from `events/eotg_story_orrins_grip.txt:125-161`.
- No title keys (X2). No vignettes: flavor events move catalysts.

| Sev | Where | Finding | Fix | Owner |
|---|---|---|---|---|
| BLOCKER ✔ | `common/struggle/struggles/eotg_myr_struggle.txt:24-52` | 16 v1 culture keys (B-CULTURES; temporary-map rule). | Re-derive from briefs. | architect → scripter |
| BLOCKER | `:53-62` | 8 v1 faith keys (B-FAITHS). | Re-derive from briefs. | architect → scripter |
| BLOCKER ✔ | `:66` | `regions = {}`: no map footprint. | Needs `eotg_region_myr_cluster` (Gate 1). | cartographer → scripter |
| BLOCKER ✔ | `history/struggles/eotg_myr_struggle_history.txt:10` | `has_dlc_feature = the_fate_of_iberia` with no fallback (lesson 12). | Choose: a stated DLC requirement, or an event-driven fallback. | human → architect |
| HIGH | hub `eotg_on_actions.txt:11,33` | Dead hook (X1): events 0011–0014 and 2 catalysts never fire. | Move to its own `eotg_myr_on_actions.txt` on `yearly_playable_pulse`. | scripter |
| HIGH | `eotg_myr_struggle.txt:6,43`; loc `:8,14,120,133` | "Helix remnant" conflicts with open CB-06 (SETTING LORE `:302-306` says "active"). | Wait for CB-06. | human → lore-keeper → localizer |
| HIGH | `common/decisions/eotg_myr_decisions.txt:36-39`; `eotg_myr_struggle.txt:282-289` | Ending by `change_struggle_phase` to a phase with no duration or `future_phases` may not end the struggle or fire 0090 (`UNVERIFIED-VANILLA`). | Compare with vanilla `end_struggle`. | vanilla-scout → scripter |
| MED | `eotg_myr_struggle.txt:125-127,168-171,218-221,261-263` | 5 `involved_parameters` that nothing reads, while the loc (`:39`) promises their effects. | Implement or delete. | architect → scripter / localizer |
| MED | `:230,272` | Modifier names `monthly_county_control_*` (`UNVERIFIED-VANILLA`). | Confirm. | scripter (PX) |
| MED | `common/character_interactions/eotg_myr_interactions.txt:63` | `hegemony` tier in `ai_frequency_by_tier` (`UNVERIFIED-VANILLA`). | Confirm. | vanilla-scout |
| LOW | `:96-282` | Phase keys `struggle_eotg_myr_phase_*` don't lead with `eotg_`. | Rename, or record the exception. | architect |
| LOW | `:49-51` | Nyssari labelled "mercenary interlopers" vs their culture comment. | Ruling. | lore-keeper |
| LOW | loc `:87` | "sixteen years" is hard-coded. | Reword. | localizer |
| LOW | history `:8` | `on_start` fires at 850 during history setup. | Confirm behaviour (`UNVERIFIED-VANILLA`). | vanilla-scout |
| LOW | various | Placeholder art. | B-ART. | human |
| LOW | `common/casus_belli_types/eotg_proxy_war.txt` | This is the Corporation's CB (its flag `eotg_proxy_war_active` is never read). | Move it with the Corporation rewrite. | architect |

### SE. Scripted effects / triggers / script values: BLOCKED (per file)

| Files | Verdict |
|---|---|
| `eotg_scripted_effects.txt`, `eotg_scripted_triggers.txt` | **DROP.** No callers. The Void helpers bypass the state machine (HIGH). One trigger is a TODO stub. Move `eotg_st_is_void_touched` into the Void lift only if wanted. |
| `eotg_exodus_triggers.txt` | Ready, but goes with a Titan Exodus lift, which is in neither catalog column. |
| `eotg_{myr,legacy,void}_{effects,triggers}.txt` | Go with their own systems (S, L, V above). |
| 21 government files: `eotg_{cartel,corporation,elven_monarchy,fringe,gobcorp,new_cauldron,pmc}_{effects,triggers,values}.txt` | **BLOCKER.** Every role trigger keys on `has_government = eotg_<gov>_government` with the empire-topped tier ladder (`eotg_cartel_triggers.txt:10-32` and others). The effects fire government event namespaces and use ~30 government modifiers. Elven needs `heritage:eotg_heritage_elf`. Lift each with its government, after the architect re-specs the ladder (rewrite column). |

| Sev | Where | Finding | Owner |
|---|---|---|---|
| MED | lines listed per file in the reviewer notes | Dead code to prune at lift: 5 role triggers, 5 other triggers, 7 effects and 5 values that are never referenced (e.g. `eotg_cartel_triggers.txt:10,17`; `eotg_pmc_triggers.txt:10,17`; `eotg_new_cauldron_triggers.txt:57,70,83`; `eotg_corporation_values.txt:34,37`). | scripter |
| MED | `eotg_pmc_values.txt:6-13` vs `eotg_pmc_effects.txt:8-9,24-25,41-42` | Effects hard-code the same numbers the values define. | scripter |
| MED | `eotg_corporation_triggers.txt:12-22` | Overlapping roles: a duchy holder is both Account Director and Operations Chief. | architect |
| MED | `eotg_fringe_effects.txt:6-171`; `eotg_cartel_effects.txt:42-45` | Vocabulary collisions: the Fringe resource `eotg_fringe_grip` collides with "the Grip" and `eotg_grip_survivor`; `eotg_cartel_defiance_pressure` overlaps Void's "Pressure". | lore-keeper → architect |
| LOW | `eotg_new_cauldron_effects.txt:17,25,95` | Unprefixed scopes `nc_election_winner` / `_runner_up`; a `years = 0` flag. | scripter |
| LOW | `eotg_gobcorp_effects.txt:79-81` | Unguarded `var:eotg_faction_role`. | scripter |
| LOW | `eotg_cartel_values.txt:38` | Unused `@` constant. | scripter |
| — | — | Clean: `add_legitimacy` here only targets Elven (`legitimacy = yes`; the Cartel/Fringe problem is in events). No skill-suffix, title-key or DLC issues. | — |

### RP. `localization/english/replace/`: READY-WITH-FIXES (49 of 52); 3 BLOCKED
**Inventory:** 52 files (not 53, and not 49 as `.claude/agents/eotg-localizer.md:14` says). 1,339 definitions, 1,170 unique keys, all vanilla keys. Clean: BOM, header, no `[scope:`, no title keys, 0 collisions with v2 loc.

| Sev | Where | Finding | Fix | Owner |
|---|---|---|---|---|
| BLOCKER ✔ | 166 keys across file pairs (e.g. `eotg_stewardship_events` ↔ `eotg_stewardship_serf_misc`: 13; `journey_events.50.b.tt` in 3 files) | **Invariant 6 is broken.** 44 of the duplicates have *different* text, so one edit is silently lost. The count matches the open list at `docs/localization_crusade.md:216-261`, so nothing has been fixed since. | Merge the 44; delete the 122 identical copies; rerun the check at `localization_crusade.md:268-271`. | localizer |
| HIGH ✔ | `replace/eotg_terrains_l_english.yml:2-19`; `eotg_custom_loc_wordbank_l_english.yml:44-67`; v2 `docs/terrain_scheme.md:28-42` | **Tier words collide with terrain words.** The glossary uses System/Region/Sector/Expanse/Cluster for barony through empire. v1 terrains reuse all five, and v2's new scheme names six terrains "… Cluster" (the empire word). | Human ruling, then rewrite the terrain and wordbank keys together. | human → localizer |
| HIGH | e.g. `eotg_county_hunt_tour_modifiers_l_english.yml:24,29,42,84,93,97,101`; `eotg_tgp_dlc_commoner_l_english.yml:64,82,88` | ~30 override values still say "County" next to a `[county\|E]` tooltip that reads "Region". | Change to Region. | localizer |
| MED | `eotg_traditions_l_english.yml:11-27` | Traditions are built on the stale v1 terrain names. | Hold until the terrain ruling. | localizer |
| MED | `eotg_traditions_l_english.yml:5,6,8,9,32,33,113` | "Void" is used for ordinary space ("Voidfarers", "voidlanes"), which collides with the canon Void (CB-11). | Review; likely "starlane". | lore-keeper → localizer |
| MED | `intake/README.md:23-32` | "Region" is both the county tier word and intake's word for a map area. | Record the distinction in the glossary. | localizer / architect |
| MED | `localization_crusade.md:19-21,37-41` | The glossary's reasoning rests on v1 title names. | Recheck after Gate 1. | localizer |
| LOW | — | "Strike Speeders" name clash (see M). | Rename one. | localizer |
| LOW | — | Substitutions missing from the glossary: burgher → "contractor", chivalry → "Valor", eunuchs → "Chamber Custodians". | Add them. | localizer |
| LOW | — | Ruler ranks (Count, Duke…) are not overridden. | Note the gap. | localizer |
| LOW | — | Unescaped inner `"` (`eotg_court_relation_events_l_english.yml:48,54`). | Confirm tolerated (`UNVERIFIED-VANILLA`). | vanilla-scout |
| LOW | — | Whether `replace/` overrides by key regardless of filename; none match vanilla filenames (`UNVERIFIED-VANILLA`). | Confirm. | vanilla-scout |
| — | — | **CB-08 (UI terms) is not pre-empted.** No override renames court, courtier, vassal, knight, household, gold or liege. The v2 cybernetics loc has zero `[x\|E]` links to the 41 overridden concepts, so the lift won't change cybernetics text. ~58 override values contain those terms in prose and would need revising if CB-08 renames any. | — | — |

### D. Docs
**Lift status:** none of the four is in v2 `docs/`. Every v2 reference points into the frozen tree: `CLAUDE.md` (Canon section), `docs/cloud_agent_prompt.md:46`, `.claude/agents/eotg-*.md`, `circlebackTaskboard.md:145-169`.

| Sev | Where | Finding | Fix | Owner |
|---|---|---|---|---|
| HIGH | `circlebackTaskboard.md:147,154` | CB-06 and CB-07 tell the human to paste errata into `OLD PROJECT VERSION/docs/SETTING LORE`, which `CLAUDE.md` calls frozen. | Lift SETTING LORE to v2 `docs/` first and repoint the references. | orchestrator / human |
| HIGH ✔ | SETTING LORE `:31,334,797` vs `:615`; `866_bookmark_design.md:11,110` | **The Grip is dated two ways.** SETTING LORE says ~1,000 years before mod start, with 0 AG as the recovery. Its own `:615` and the bookmark doc say 866 years (0 AG). `CLAUDE.md` and `intake/README.md:42,58` follow 866. Not on the taskboard. | Human ruling, then an ERRATA line. | human → lore-keeper |
| HIGH | SETTING LORE `:209-212` vs `866_bookmark_design.md:112` | "Titan" means Yu, Orrin and Carrigore in one doc, and Orrin and Yu only in the other. | Ruling. | human |
| HIGH | `866_religions:147` vs `866_bookmark_design.md:44`; SETTING LORE `:262` | "Second" Elrossi Imperium vs "First" at 866, vs "Holy Elrossi Empire". | Ruling. | human → lore-keeper |
| MED | SETTING LORE `:150,286,808` vs `866_bookmark_design.md:32-82` | The major-power rosters differ: Trade Federation of Thorum vs Gob-Ogre League, New Cauldron and the others. SETTING LORE never mentions New Cauldron or the Titan Exodus. | Ruling. | human |
| MED | SETTING LORE `:212` vs `:270` | Carrigore is "Neutral Evil" in one place and "Chaotic Evil" in the other. | Ruling. | human |
| MED | v2 `CLAUDE.md` (Canon), `intake/README.md:58`, `.claude/agents/eotg-lore-keeper.md:24-25` | v2 "fixed points" have no canon source: "Myr Cluster Wars ignited 850 AG" (only v1 script; SETTING LORE `:803` has the Divine Awakening at 850) and "Exodus wanes after 1000 AG". | Put both in ERRATA, or soften. | human → lore-keeper |
| MED ✔ | `.claude/agents/eotg-lore-keeper.md:13`; `.claude/agents/eotg-localizer.md:25`; `OLD VERSION CATALOG.md:26` | v2 files misstate the docs. The lore-keeper file lists a "Malvrick is not Carrigore" errata that SETTING LORE `:7-24` doesn't contain. The glossary is described as "County→System…", but the actual glossary is Barony→System, County→Region, Castle→Bastion. | Correct the files. | orchestrator |
| MED | `866_religions:4-6,139-143` | Describes v1 code as "shipped". | Relabel as the v1 reference design. | architect / lore-keeper |
| MED | `866_bookmark_design.md:16,19,58-63`; `866_religions:193-199` | Nikios content (invariant 9). | Mark deferred in the lifted copies. | lore-keeper |
| LOW | `866_bookmark_design.md:101` | Says `on_yearly_pulse`; the real hook is `yearly_playable_pulse`. | Fix. | lore-keeper |
| LOW | `localization_crusade.md:38,40,49` | Cites `eotg_k_…`, `eotg_d_…`, `eotg_b_*` title keys, which breaks invariant 2 in text. | Rekey or drop. | localizer |
| LOW | `866_bookmark_design.md:24` | Timeline out of order: Crime Wars ~330 AG is listed after 1300 AG. | Reorder. | lore-keeper |
| LOW | — | "history, not living memory" vs `CLAUDE.md`'s "living history". | Reconcile wording. | lore-keeper |
| — | SETTING LORE `:211,511,688` | ERRATA handling is fine: the body's "imprisoned" lines are explicitly superseded, and `866_religions` applies the ERRATA consistently. | — | — |

**Not re-reported (already on the taskboard):** CB-06 (Helix), CB-07 (the voice errata), CB-08 (UI terms), CB-12.

---

## 3. Decisions for the human (collected)
1. **Date of the Grip:** ~1,000 years before 866, or 0 AG? (Docs, HIGH.)
2. **Who the Titans are:** Yu, Orrin and Carrigore, or Orrin and Yu? Is the Elrossi Imperium "First" or "Second" at 866? Which roster of major powers is canon? Carrigore's alignment?
3. **Fixed points:** should "Myr Cluster Wars ignited 850 AG" and "Exodus wanes after 1000 AG" go into ERRATA?
4. **Lift SETTING LORE into v2 `docs/`** so CB-06 and CB-07 have an editable target.
5. **Tier words vs terrain words** (System/Region/Sector/Expanse/Cluster). This blocks the `replace/` terrains, wordbank and traditions files, and touches v2 `docs/terrain_scheme.md`.
6. **Myr DLC gate:** hard requirement, or fallback?
7. **Is Legacies (and MAA) mod-exclusive,** so it can be tested on the temporary map before Gate 1?
8. **Hide vanilla MAA?** The MAA loc promises no horses or bowmen.
9. **Confirm stopgap lifts of cultures and religions,** since `intake/` is empty.
10. Already open on the taskboard: CB-06 (Helix), which gates text in cultures, religions and the struggle.

## 4. UNVERIFIED-VANILLA list (for vanilla-scout and the local session)
1. All 59 doctrine, 25 tenet and 30 virtue/sin keys in `eotg_religions.txt`. Priority: `tenet_sacred_destruction`, `tenet_pursuit_of_power`, `tenet_pursuit_of_knowledge`, `tenet_adaptive`.
2. Language colour names (`trojan`), ethnicity keys, the DLC-prefixed traditions.
3. `government_allows = subject_men_at_arms`; the MAA `illustration` and `ai_quality` shapes; regiment icon keys.
4. Struggle end via `change_struggle_phase` vs `end_struggle`; `hegemony` in `ai_frequency_by_tier`; `monthly_county_control_*` modifiers; `on_start` at a history date.
5. Hooks `on_title_gain`, `on_game_start_after_lobby`, `on_war_started`, `on_death`; whether on_actions in a list run in order.
6. Whether `add_character_modifier` stacks or refreshes (Void insight).
7. Void engine names: themes `corruption`, `disaster`, `dread`, `secret`, `mental_health`; `advantage`; `max_hostile_schemes_add`; `every_knight`; `lunatic_1`; `possessed_1`; `trigger` inside a `random_list` entry.
8. `replace/`: whether it overrides by key regardless of filename; tolerance of unescaped inner quotes.

---

## 5. Handoff
This block is kept inside `docs/qa/` because this task allowed no files outside it.

### HANDOFF (cloud session, unvalidated)
- **branch:** `claude/focused-dirac-ixo81h`
- **status:** done
- **summary:** Static lift-readiness audit of every catalog §5 lift-column row. Augmentation was skipped (already lifted, and off-limits).
  - Lift now: Void (minus the cult branch), Legacies (minus the 7 character seeds and the Exodus tie-in), MAA, and cultures and religions as stopgaps (Nikios cut).
  - Blocked: the Myr struggle, the 21 government script files, 3 `replace/` files, and the canon docs.
  - Every lifted system must move off the dead `on_yearly_playable` hook.
  - `replace/` still carries 166 duplicate keys (44 conflicting).
- **files:** `docs/qa/v1_lift_readiness_cloud.md` (new)
- **unverified-vanilla:** §4
- **needs-local-validation:** none for this branch. Tiger and PX on each system as it is lifted.
- **needs-loc:**
  - Void: Orrin, voice, pressure and "866 years" rewrites;
  - Legacies: "Second Era" strings;
  - `replace/`: dedupe, County → Region;
  - none now.
- **needs-lore:** §3 items 1–3; Voidwalkers; "Confluence"; "Hell's administrative layers"; Nyssari; Malvrick's family.
- **needs-human:** §3.
- **taskboard (proposed):**
  - Add lift items per system with the verdicts above.
  - Add "re-add the Legacies Exodus path with the Exodus lift".
  - Fix the stale catalog §5 claims (X2).
  - Fix the agent files (D, MED).
  - Add the Grip-date canon question.
  - CB-10 and CB-11 now have concrete fix lists here.

---

## 6. Local verification (2026-10-04, eotg-qa; vanilla 1.20.0.3)

**Verdict: PASS, with three corrections.**
- **Mechanical facts:** high reliability. Every recomputed count matched.
- **Recommendations:** medium reliability.
- **Blockers:** none of the 6 is false. B4 (the Myr DLC gate) is OVERSTATED: it copies vanilla's exact shape (`iberian_struggle_history.txt:4-13`), so it's a design ruling for the human, not a defect.

**Corrections:**
1. **Religions can't be lifted as a stopgap copy.** CK3 1.20 changed the schema:
   - religion fields sit inside `religion_details = { }`;
   - faiths live in a separate `common/religion/faith_types/`;
   - tenets and doctrines are lists, in new `tenet_types/`, `doctrine_types/` and `rite_types/` folders;
   - the family field `doctrine_background_icon` became `tenet_background_icon`.

   v1 is the 1.19 shape, so religions need a 1.20 port, and Tiger 1.17 can't validate one. Also, `tenet_monasticism` (`eotg_religions.txt:556`) doesn't exist in 1.20. The four suspects in §4.1 all exist.
2. **Stale against same-day commits.** CB-06 (Helix) and CB-07 (voice) were closed in 1578f85, with errata pasted into SETTING LORE. Every SETTING LORE line citation here is off by about +17 lines.
3. **"Lift now, no human input" is wrong for Void and Legacies.** Each needs the human to designate it mod-exclusive (§3 Q7 should cover Void too). Void also needs: the Voidwalker bug fixed (confirmed; event 0004 re-rolls every 5 years at −100 piety), an owner for `eotg_grip_survivor` (wider than reported), and the loc rewrites at `:93-95` and `:94`. The cult-branch faith check has **23** call sites, not 11. Legacies loc waits on the "Second Era", "Confluence" and "Hell" ruling.

**Per-item notes:**
- MAA is SAFE.
- Cultures are allowed but premature (Pipeline E: stopgaps only when Gate 1 can't close without them).
- H-V5 (voice-register drift) is confirmed for `:93-95` only.
- In the `replace/` statistics, deleting the identical copies removes 125 definitions, not 122.
