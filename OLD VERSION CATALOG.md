# Old Version Catalog — `OLD PROJECT VERSION/`

**For:** agents (and humans) starting work on the new iteration of *Echoes of the Grip* who need to know what the previous version already built, where it lives, and what to trust.

**Snapshot:** the folder is a byte-for-byte copy of git `main @ 8ea702a` ("aug 30", committed 2026-08-31) plus six untracked Tiger output logs and a `.vscode/settings.json`. Ten files show whole-file diffs against HEAD but only in line endings/BOM, not content. 287 files total. Nothing in it is wired into the current repo root; the working tree shows the whole old layout as deleted (`git status` → ` D ...`) because it was moved into this folder.

**One-line state at snapshot:** *"the setting systems are written and correctly wired; the world they run on is not."* — 359 events across 41 namespaces, 7 governments, 28 cultures, 12 faiths, 318 titles... and **0 titles CK3 could parse, place, or assign a holder to.** It never produced a playable world.

---

## 1. Read-first documents (in this order)

| File | What it is | Trust level |
|---|---|---|
| `CLAUDE.md` | Project rules: `eotg_` prefix on everything, file placement table, loc rules, on_action merge rules, Tiger command | High — still applies |
| `docs/closed_alpha_checklist.md` | The gating audit (2026-08-28). Gate 1–4 blockers, plus "already alpha-ready" table. **Best single summary of what worked and what didn't** | High |
| `docs/system_depth_audit.md` | Per-government content depth ranking + cross-cutting findings (flavor layer decoupled, opinion-modifier namespace leakage) | High |
| `docs/government_robustness_plan.md` | Engine-level government findings (F1–F10), the 4-tier role ladder per government, verified `government_rules` defaults | High |
| `docs/SETTING LORE` | Canonical cosmology & history to 866 AG. **ERRATA block at top overrides body text** (Orrin is loose in the material plane; Orro belongs to the Orrin pantheon) | Canon |
| `docs/866_bookmark_design.md` | Nation-by-nation state at 866 AG, timeline, scripting priorities | Canon |
| `docs/866_religions` | Religion/faith/family spec, rewritten 2026-08-29 to match shipped script | High |
| `docs/EOTG_Government_Design_Document_v2.md` | Design doc for the 6 (then 7) governments | Design intent — script diverged in places |
| `docs/Fringe_Gov_Concept.md` | Fringe government design (the template all others were cut from) | Design |
| `docs/eotg_cybernetic_augmentation_system.md` | Augmentation design; implementation *exceeds* it (31 events shipped vs 15 specified) | Design |
| `docs/confluence_legacies_system_pitch.md` | Confluence Legacies pitch; v1 shipped | Design |
| `docs/localization_crusade.md` | Reflavor glossary (County→System, etc.), one-definition rule for `replace/` | High |
| `docs/CK3_Modding_Complete_Reference_v1_19.md` | 1,770-line CK3 1.19 scripting reference | Mostly good. **Known error:** it teaches `[scope:x.GetName]` in loc; real loc uses bare `[x.GetName]` |
| `docs/title_hierarchy.md` | Full e/k/d/c/b tree with intended province IDs (0–287) | Reference — never applied to script |
| `docs/Bookmark-Characters`, `docs/bookmark-char-story`, `docs/EOTG_Events_Characters` | Narrative source for the 9 bookmark character arcs (~80 KB) | Lore |
| `docs/Events-to-do.md` | 20,403-line Fringe event design dump (~2,190 event headings). Far more than was ever implemented | Idea bank only |
| `docs/art_needed*.txt`, `needed_art_*` | Every missing art asset, with sizes/formats | Reference |

`CONTRIBUTING.md` and `README.md` are standard; README's directory tree is aspirational (lists folders that never existed).

---

## 2. What was built — by system

### 2.1 Governments (7) — `common/governments/`
`eotg_cartel_government`, `eotg_corporation_government`, `eotg_elven_monarchy_government`, `eotg_fringe_government`, `eotg_gobcorp_government`, `eotg_new_cauldron_government`, `eotg_pmc_government`.

Each government has a matched file set (same stem `eotg_<gov>_*`):
- `common/script_values/` — signature resources
- `common/scripted_effects/` and `common/scripted_triggers/` — incl. a **4-tier role ladder** (26 role triggers total; most unused, see robustness plan)
- `common/subject_contracts/contracts/` + `groups/` — 7 obligation contract groups
- `common/decisions/` — 34 decisions total (Fringe 9 incl. 4 reform paths; NC 8; PMC 4; Cartel 4; Corp 2; Elven 2; Gob-Corp 1)
- `events/eotg_<gov>_*_events.txt` + `events/eotg_<gov>_expanded_events.txt` (~19 flavor events per gov)
- `localization/english/eotg_<gov>_l_english.yml` + `_expanded_l_english.yml`
- `common/customizable_localization/eotg_government_loc.txt` — government-flavored title/rank names

Government-specific extras: Corporation has an interaction (`eotg_hostile_acquisition_interaction`), a scheme (`eotg_sabotage_rival`), a CB (`eotg_boardroom_war`); PMC has a council position (`eotg_pmc_logistics_officer`) + 3 tasks; Corp/Cartel/Gob-Corp share `eotg_market_faction_cycle` story cycle.

**Known problems (never fixed):** no title ever carried `government = eotg_*` so all 7 were dead at runtime; all 7 use the same 4 `government_rules`; Fringe (the raiding government) lacked `government_can_raid_rule`; Cartel/Fringe set `legitimacy = no` but events still call `add_legitimacy`; flavor events never touch the signature resources. Four governments named in design (`holy_imperium`, `khanate`, `conclave`, `trade_council`) were never written.

### 2.2 Cybernetic Augmentation — most finished system
Traits `eotg_augmented → eotg_enhanced → eotg_overclocked`, plus `eotg_neurofractured`. 3 decisions, 5 yearly on_action hooks, 31 events in 5 files (`eotg_augmentation_{initiation,tier1,tier2,tier3,fracture}.txt`), modifiers, opinions, full loc. Needed icons only.

### 2.3 Void Corruption — built 2026-08-29/30
Signature variable `eotg_void_exposure` (0–100) with band modifiers. Stages: Whispers → Bargain → Void-touched → Hollowed; `eotg_void_defiant` resist path. Traits `eotg_void_touched`, `eotg_void_hollowed`, `eotg_void_defiant`. 15 events in `eotg_void_{whispers,touched_events,hollowing}.txt`, 3 decisions, 5 hooks, full loc. Deliberately does **not** mirror augmentation's structure.

### 2.4 Confluence Legacies — v1 shipped
County-variable schema, `eotg_se_legacy_*` effects (seed/make_known/set_condition/refresh_modifier/add_attention/add_integrity/cooldown/fire_discovery/seed_capital/seed_random), 16 events in `eotg_legacy_events.txt`, decision `eotg_decision_survey_legacies`, on_actions, modifiers, opinions, loc.

### 2.5 Myr Cluster Wars (struggle)
`common/struggle/struggles/eotg_myr_struggle.txt` — 5 phases (ignition/escalation/attrition/settlement/conclusion), 6 catalysts, start/phase-change/join hooks, ending decision `eotg_decision_myr_settlement`, CB `eotg_proxy_war`, interaction `eotg_direct_proxy_war_interaction`, 9 events. Seeded 850 AG in `history/struggles/` **behind `has_dlc_feature = the_fate_of_iberia`**. `regions = {}` was empty — no map footprint.

### 2.6 Titan Exodus
10 events (`eotg_exodus_events.txt`), 6 modifiers, yearly pulse hook, waning after 1000 AG. Functional but thin (no decisions/traits; refugees never form a culture/faction).

### 2.7 Orrin's Grip opening + bookmark character arcs
`eotg_story_866_opening` story cycle + 3 events. 9 bookmark character arcs (7thlegion, clayd, coldiron, lanius, newcauldron_char, ratfolk, rughan, tradeleague, xerxes — one file each) wired via `eotg_bookmark_char_arcs_start`, 568-line loc file. Only **one** bookmark entry (Vaelorin, `eotg_char_90001`) ever existed in `common/bookmarks/`.

### 2.8 Elven expulsion chain
`eotg_expulsion_events.txt` — 1,212 lines, 6 events. Was unreachable for most of the project; wired into `eotg_on_yearly_elven_flavor` on 2026-08-28.

### 2.9 Cultures & religion
- **28 cultures** in `common/culture/cultures/eotg_cultures.txt` (aelvaryn, thalassyr, brackwateri, virens, veltrani, caldryx, duskvein, cauldrani, halrethi, tangentine, khadrashi, sternstahl, noctivar, solvari, istrovan, zeladani, nyssari, geldmark, brokari, kelmori, drogmari, thrakani, skarrin, veskari, gnashvok, uvreki, vanthari, orovane). 11 heritage + 10 language pillars. **All point at vanilla name lists** — no `common/culture/name_lists/`.
- **4 religion families** (`eotg_rf_divine_order`, `_titan_worship`, `_ancestral`, `_pragmatic`), **12 religions, 13 faiths** in `common/religion/religion_types/eotg_religions.txt` (2,219 lines). `eotg_religion_gods_l_english.yml` (596 lines) holds the god-name loc blocks — these are load-bearing for vanilla loc tags. No holy sites were ever defined despite the descriptor replacing that path.

### 2.10 Men-at-arms — Gate 3, shipped
8 sci-fi regiments in `common/men_at_arms_types/`: line_troopers, recon_drones, railgun_teams, aegis_wardens, strike_speeders, combat_walkers, orbital_breachers, operators (PMC knights). Loc in `eotg_maa_l_english.yml`.

### 2.11 Titles & history — **the part that never worked**
- `common/landed_titles/eotg_landed_titles.txt`: 1 empire (`eotg_e_myr_cluster`), 6 kingdoms, 24 duchies, 80 counties, 287 baronies. **Keys use `eotg_e_/k_/d_/c_/b_` prefixes, which CK3 cannot classify** (tier is read from the first two chars — must be `e_eotg_...`). **No barony has `province =`**, no `color`, no `capital`. There is no `map_data/`.
- `history/titles/eotg_titles_866.txt`: 80 blocks, **zero active `holder =` lines** — all ownership commented out.
- `history/characters/eotg_characters_866.txt`: 23 characters (`eotg_char_10001…90011`), with `TODO_` placeholder names on great-power heads. Uses `culture = culture:eotg_x` / `religion = faith:eotg_x` — **syntax unverified against vanilla** (vanilla writes bare keys).
- `descriptor.mod` declares `replace_path` for `history/provinces`, `history/wars`, `common/dynasties`, `common/religion/holy_site_types` — **none of those folders ship**, so vanilla is wiped with nothing replacing it. All 24 `dynasty =` refs were commented out to work around the empty dynasties path.

### 2.12 Localization
- 33 mod loc files in `localization/english/` (UTF-8 BOM).
- **52 vanilla-override files in `localization/english/replace/`** — the "localization crusade" reskinning vanilla strings to the setting (County→System, peasants→commoners, castles→holdings, etc.). Glossary and one-definition rule in `docs/localization_crusade.md`. Vanilla tech tree, buildings, terrains, and 39 traditions are reflavored *only* through these overrides — no custom innovations/buildings exist.

### 2.13 on_actions — `common/on_action/`
`eotg_on_actions.txt` (2,535 lines) is the hub: vanilla hooks (`on_yearly_playable`, `on_game_start_after_lobby`, `on_title_gain`, `on_death`, `on_war_started`, `on_raid_action_start`) extended **additively** via `on_actions = { eotg_... }`, never `effect = {}`. Separate files for augmentation, void, legacy, char arcs. The project used `trigger_event` exclusively — no `events = {}` / `random_events = {}` blocks anywhere.

### 2.14 gfx/
11 files, all `.gitkeep`. **Zero art assets exist.** Every referenced icon was a missing-file warning.

---

## 3. Validation state at snapshot

- Tiger 1.17.0 vs CK3 1.19.0.6 baseline: **~64 errors / 195 warnings** (see `tiger_clean2.txt`, newest). Earlier runs: `tiger_clean.txt`, `tiger_output2–4.txt` (ANSI-colored). `tiger_output.txt` is a failed run (wrong game path).
- **Known benign** (Tiger 1.17 predates the 1.19 religion folder rename): ~48 faith/religion-path lookups, 24 culture lookups, 2 `error(filename)` on `religion_types/` / `religion_family_types/`. Do not "fix" these.
- **Real:** 81 `expected title` (the `eotg_e_` key problem), missing-file warnings for icons.
- 328/328 events reachable, 0 self-cancelling (after the 2026-08-28 audit that recovered 115 events). The 31 events added afterwards (Void Corruption, Xerxes arc, elven succession, cartel loyalty-tax) were not re-audited.

Tiger invocation that worked (Bash):
```
"/c/Users/river/tools/ck3-tiger-windows-v1.17.0/ck3-tiger.exe" --game "D:/SteamLibrary/steamapps/common/Crusader Kings III/game" "echoes_of_the_grip.mod"
```

---

## 4. Lessons the old version paid for — carry these forward

1. **Title keys must lead with the tier:** `e_eotg_x`, `k_eotg_x`, `c_eotg_x`, `b_eotg_x`. The old `eotg_e_x` form cost the whole map. This is the one identifier class where `eotg_` goes second.
2. **Baronies need `province =` and a `map_data/`** before anything else is testable. Decide "reskin vanilla map" vs "ship own map" *first*. Everything in Gates 2–4 sat untested because Gate 1 never closed.
3. **Never declare a `replace_path` for a folder you don't ship.** The old descriptor silently deleted vanilla dynasties, province history and holy sites.
4. **Assign governments to titles in history**, or the government content is invisible. Also gate government content on role triggers at *every* tier, not just empire — the old flavor sets reached only 7 characters in the world.
5. **Event `trigger = {}` is a re-evaluation guard.** If the on_action sets a cooldown flag and the event trigger also checks it, the event silently cancels. Keep cooldown authority in one place (the on_action).
6. **Couple flavor events to the signature resource** from day one. 41% of the old corpus was vignettes that never moved the number defining the government.
7. **Loc scope syntax:** `[x.GetName]`, not `[scope:x.GetName]`. Explicit event loc keys (`eotg_ns_0001_title`) make auto `.0001.t` keys dead.
8. **God-name loc blocks are load-bearing;** tenets are faith-level only; families need `hostility_doctrine`.
9. **Skill effects need the `_skill` suffix** (`add_intrigue_skill`, not `add_intrigue`).
10. **Shared opinion modifiers should not carry a government prefix** — `eotg_fringe_*` modifiers ended up used by six governments.
11. **Name lists, CoAs, holy sites, and icons** were all deferred and all became tester-visible problems. Budget them early.
12. Struggle behind `has_dlc_feature = the_fate_of_iberia` with no fallback means testers without the DLC see nothing and get no explanation.
13. **`on_yearly_playable` is not a hook** — it is named only in `_on_actions.info` prose; the game fires `yearly_playable_pulse`. v1's augmentation, legacy and hub (`eotg_on_actions.txt`) on_actions all extended the dead name, so those events never fired. Found 2026-10-02 lifting augmentation; every remaining "lift as-is" system needs its hook rewired. `docs/tools/px_vocab_check.py` catches it (`docs/pitfalls.md` §12).

---

## 5. Safe to lift verbatim vs. rewrite

| Lift as-is (with `eotg_` audit) | Rewrite / re-derive |
|---|---|
| Augmentation system (all files) | `common/landed_titles/` — rekey + add provinces/colors/capitals |
| Void corruption system | `history/titles/` — holders, governments, all of it |
| Confluence Legacies v1 | `history/characters/` — real names, bare culture/faith keys, dynasties |
| Cultures + pillars (add name lists) | `descriptor.mod` replace_path list |
| Religions/faiths/families + god loc | Government `government_rules` blocks (per robustness plan §2) |
| Men-at-arms types | On_action tier gating (empire-only → role ladder) |
| `localization/english/replace/` overrides | Bookmarks (9 chars, not 1) |
| Struggle definition (add `regions`) | Flavor event ↔ resource coupling |
| Scripted effects/triggers, script values | Anything referencing `eotg_e_/k_/d_/c_/b_` title keys (`common/struggle/`, `common/decisions/`, `eotg_titles_l_english.yml`) |
| Docs: SETTING LORE, 866_bookmark_design, 866_religions, localization_crusade | README's directory tree |

---

## 6. Quick numbers

| Thing | Count |
|---|---|
| Files | 287 (11 are `.gitkeep`) |
| Event files / events / namespaces | 44 / 359 / 41 (the 328-event reachability audit predates the Void system; the 31 newer events were never re-audited) |
| Governments | 7 (+4 designed, unwritten) |
| Decisions | 38 |
| Traits | 9 |
| Cultures / heritage / language pillars | 28 / 11 / 10 |
| Religion families / religions / faiths | 4 / 12 / 13 |
| Titles e/k/d/c/b | 1 / 6 / 24 / 80 / 287 (0 provinces) |
| History characters | 23 |
| Men-at-arms | 8 |
| Scripted effects / triggers files | 12 / 13 |
| Loc files (mod / replace) | 33 / 52 |
| Docs | 24 files, incl. one 20k-line idea dump |
| Git commits | 22, 2026-04 → 2026-08-31 |
