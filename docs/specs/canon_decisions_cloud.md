# Canon decisions: dossier for the human (cloud)

> **Input only. Nothing here is decided.** This dossier was compiled in a cloud session from static reads of `OLD PROJECT VERSION/` and the v2 root. It had no game files and no vault access. Every quote was re-read against the current files. Anything that depends on how the engine behaves is marked `UNVERIFIED-VANILLA`.
>
> **Date:** 2026-10-04 · **Branch:** `claude/canon-void-glossary-cloud` (from `v2-space-map` @ `3b45660`) · **Owner after you:** eotg-lore-keeper (ERRATA wording), then intake for the vault questions, then the owners each answer touches.

## How to use this
- Each section has four parts:
  - **sources**, quoted verbatim with `file:line`, with the ERRATA first;
  - the **contradictions** between them;
  - **options**, each saying which systems and text it would change;
  - **one question** to answer here or to send to the vault.
- **Precedence:** v2 `CLAUDE.md` names SETTING LORE (ERRATA over body) and `866_bookmark_design.md` as canon, without ranking them. `.claude/agents/eotg-lore-keeper.md:13-14` lists SETTING LORE first. Several questions below are exactly the points where those two disagree, so a **standing precedence rule** would settle part of them at once (question 0).
- **Stale line numbers:** SETTING LORE's ERRATA block grew on 2026-10-03/04, so every body line moved down about 17. The line numbers in `docs/qa/v1_lift_readiness_cloud.md` §2 D and §3 are stale. The numbers here are current.
- **Out of scope:** the cybernetics files. Per CB-28, the cybernetics syndicate stays unnamed.

## Questions at a glance
| # | Question | Section |
|---|---|---|
| 0 | When SETTING LORE and `866_bookmark_design.md` disagree, which wins by default? | — |
| 1 | Is "the Grip" the 0 AG cataclysm 866 years before the bookmark, and the same event as "Orrin's Grip"? Does "Second Era" name the civilisation before it, or SETTING LORE's 131–850 AG period? | §1 |
| 2a | Which beings are Titans (Yu, Orrin, Carrigore?), and is Yu still sealed or freed and at war with Orrin? | §2a |
| 2b | Is the Elrossi state at 866 the First or Second Imperium, and is its formal name "Holy Elrossi Empire" or "Elrossi Imperium"? | §2b |
| 2c | Which realms are the major powers at 866, and is the Gob-Ogre Trade League the Trade Federation of Thorum? | §2c |
| 2d | Is Carrigore Neutral Evil or Chaotic Evil, and does SETTING LORE:287 describe the god or its host? | §2d |
| 3 | Should "Myr Cluster Wars ignited 850 AG" and "Exodus began 131, ongoing at 866, wanes ~1000 AG" become ERRATA canon? | §3 |
| 4.1 | Where (which duchies) are Helix's three counties, and are the "Helix peoples" wider than the polity? | §4.1 |
| 4.2 | Is any Helix county on or beside drowned Xerxes? | §4.2 |
| 4.3 | What government does Helix run at 866? | §4.3 |
| 4.4 | Does Clayd hold all three counties, and what are his canonical age and education? | §4.4 |
| 4.5 | Are the Pale Hand ties still rumour only? | §4.5 |
| 5 | Are the Voidwalkers Void worshippers, wardens, both, or disputed? Is Malvrick's faith Divine Order or Titan-facing? | §5 |

**Note on Helix (CB-28 point 1):** the v1 draft `OLD PROJECT VERSION/docs/title_hierarchy.md:163-185,251-277` gives Helix **two whole duchies** (six counties). This conflicts with the ERRATA ruling of three counties in different duchies (`SETTING LORE:34-36`). Neither v1 Helix duchy may be lifted as written (§4.1).

---

## 1. When was the Grip, and is it the same event as "Orrin's Grip"? (audit §3 item 1)

> **Line-number note.** The ERRATA block now runs to line 42. Every SETTING LORE line cited in `docs/qa/v1_lift_readiness_cloud.md` has moved down 17 lines:

| Audit cite | Now |
|---|---|
| `:31` | `:48` |
| `:85` | `:102` |
| `:100` | `:117` |
| `:334` | `:351` |
| `:615` | `:632` |
| `:797` | `:814` |
| `:801` | `:816` |
| `:803` | `:821` |

### 1.1 Sources
All paths are under `OLD PROJECT VERSION/` unless they start with a v2 root path.

| file:line | Verbatim (trimmed) | Asserts |
|---|---|---|
| `docs/SETTING LORE:8-42` (ERRATA) | Entries for Orrin, Orro, Xerxes, the cybernetic voice and Helix | **The ERRATA says nothing about the Grip's date or the era names.** |
| `docs/SETTING LORE:2` | "HISTORY UP TO 866 AG" | AG is the dating system. |
| `docs/SETTING LORE:48` | "THE GRIP (Circa -1000 years before mod start)" | The Grip happened about 1,000 years before 866 (≈ −134 AG). |
| `docs/SETTING LORE:55` | "Technology of pre-Grip civilization mostly lost" | The earlier civilisation is called "pre-Grip", not "Second Era". |
| `docs/SETTING LORE:57-58` | "FIRST ERA: POST-GRIP RECOVERY (0-131 AG) / Duration: ~131 years of rebuilding" | First Era = 0–131 AG. |
| `docs/SETTING LORE:102-103` | "SECOND ERA: TECHNOLOGICAL EXPANSION & CONSOLIDATION (~131-180 AG → ~850 AG)" | Second Era comes after the Grip. |
| `docs/SETTING LORE:117-119` | "Orrin's Grip Emergence (~131-180 AG) … Unknown planar force (later identified as Orrin-related) emerges" | Orrin's Grip is a separate crisis around 131 AG. |
| `docs/SETTING LORE:175` | "THIRD ERA: DIVINE MEDDLING & FRAGMENTATION (~850 AG → Present 866 AG)" | Third Era = 850 AG onward. |
| `docs/SETTING LORE:351` | "THE GRIP CRISIS (~1000 years before mod, recovered by 0 AG)" | 0 AG marks the end of recovery. |
| `docs/SETTING LORE:356` | "Recovery took entire First Era" | Conflicts with `:351`. |
| `docs/SETTING LORE:365-366` | "ORRIN'S GRIP EMERGENCE (~131-180 AG) / New planar threat" | Orrin's Grip ≈ 131 AG. |
| `docs/SETTING LORE:617-620` | "Pre-Grip: Advanced tech created by ancients … Second Era: Tech reconstruction & innovation" | Pre-Grip ≠ Second Era. |
| `docs/SETTING LORE:631-632` | "The Grip left dimensional scars … ~866 years of "scar tissue" managing rift zones" | **The Grip = 0 AG.** Contradicts `:48`. |
| `docs/SETTING LORE:665-666` | "The Shardbearers (… ~131-180 AG) / … shaped early Third Era history" | Calls 131–180 AG "Third Era", which contradicts `:175`. |
| `docs/SETTING LORE:814-817` | "~-1000 years: THE GRIP … ~0 AG: FIRST ERA BEGINS … ~131 AG: FIRST WAR (… Orrin's Grip emerges…)" | Quick-reference timeline repeats the −1000 date. |
| `docs/SETTING LORE:821` | "~850 AG: THIRD ERA BEGINS / DIVINE AWAKENING" | — |
| `docs/866_bookmark_design.md:3` | "the canonical reference for what the galaxy looks like at the mod's starting bookmark" | Claims canon status. |
| `docs/866_bookmark_design.md:11` | "\| Orrin's Grip — the cataclysm \| 0 AG \|" | **Orrin's Grip = the cataclysm = 0 AG.** |
| `docs/866_bookmark_design.md:35` | "crash-landed on the Titanworld in the ruins of one of the second era's capital cities" | Second Era cities were already ruins by 131 AG, so the Second Era is pre-Grip. |
| `docs/866_bookmark_design.md:110` | "The Grip is 866 years in the past at this bookmark — it is history, not living memory … all stem from 0 AG" | 0 AG. |
| `docs/confluence_legacies_system_pitch.md:5-6` | "Orrin's Grip did not merely destroy the Second Era. It forced worlds … together into the Third Era's strange geography." | Second Era is pre-Grip; Third Era is post-Grip. |
| `README.md:5`, `:13` | "merged the First and Second Material Planes in the cataclysm known as **Orrin's Grip (0 AG)**" / "The Third Era begins at **0 AG**" | Same reading, plus a "Material Plane" sense of "Second". |
| `CONTRIBUTING.md:174,176` | "`0 AG` — Orrin's Grip; the cataclysm that ends the Second Era" / "`1851 AG` — The main gameplay bookmark" | Same; also a stale 1851 bookmark. |
| `CLAUDE.md:11`, `:130` | "**866 AG** (After the Grip)" / "Orrin's Grip (the cataclysm) was **866 years ago** — living history, not myth" | — |
| `common/bookmarks/bookmarks/eotg_bookmarks.txt:7-8,12` | "the "year" shown in-game will be 866 AD by the engine … refer to it as 866 AG" / `start_date = 866.1.1` | Engine year = AG year. |
| `common/traits/eotg_traits.txt:8` | "bloodline traces back to those who passed through Orrin's Grip" | Used by `eotg_grip_survivor`. |
| `common/story_cycles/eotg_story_cycle_866_opening.txt:5` | "the memory of Orrin's Grip (866 years old)" | — |
| `events/eotg_story_orrins_grip.txt:5,12` | "866 years since Orrin's Grip — living history, not myth." | — |
| `common/scripted_triggers/eotg_scripted_triggers.txt:19-20` | "landed ruler in the Third Era setting" (`eotg_st_is_third_era_ruler`) | Third Era = now. |
| `common/on_action/eotg_legacy_on_actions.txt:188` | "New Cauldron stands on a Second Era capital" | — |
| `events/eotg_legacy_events.txt:2` | "the buried inheritance of the Second Era" | — |
| `common/men_at_arms_types/eotg_maa_types.txt:23,196` | "post-Grip warfare" / "the closest thing to Second Era armor" | — |
| `common/scripted_triggers/eotg_void_triggers.txt:7-8` | "Grip-era rift sites … re-activating across 850-866 AG" | — |
| `localization/english/eotg_orrins_grip_l_english.yml:9` | "the Grip is 866 years past — history, not living memory" | — |
| `localization/english/eotg_orrins_grip_l_english.yml:18-19` | "Eight hundred and sixty-six years … Orrin's Grip … the hour that ended the Second Era and began the one you are standing in." | — |
| `localization/english/eotg_l_english.yml:5` | "Orrin's Grip — the tunnel through the hells that shattered the Second Material Plane." | "Second" used as a plane, not an era. |
| `localization/english/eotg_l_english.yml:48`; `eotg_new_cauldron_l_english.yml:7` | "built from the very ruins of Orrin's Grip" / "founded in 131 AG by Mikey the Great from the ruins of Orrin's Grip" | — |
| `localization/english/eotg_legacy_l_english.yml:5` | "Orrin's Grip fused worlds, stations, and planes into the Third Era's strange geography." | — |
| `localization/english/eotg_legacy_l_english.yml:14,41,135` | "eight centuries" | Fits a Grip at 0 AG. |
| `localization/english/eotg_legacy_l_english.yml:21,58,74,137,139,155` | "Second Era …" | — |
| `localization/english/eotg_void_l_english.yml:65,93,94,125` | "eight hundred and sixty-six years" | Hard-coded year count. |
| `localization/english/eotg_void_l_english.yml:22,133` | "Second Era route-charts / route-work" | — |
| `localization/english/eotg_religions_l_english.yml:96` | "866 years declining to ask" | — |
| `localization/english/eotg_maa_l_english.yml:14,34` | "predate the Grip" / "Second Era armor" | — |
| `docs/Events-to-do.md:11,17`; `common/scripted_effects/eotg_fringe_effects.txt:17` | "GRIP SYSTEM" / "The Grip Weakens" | **Homonym:** Fringe's resource is also called "Grip". |
| v2 `CLAUDE.md:75` | "866 AG: the Grip was 866 years ago and is living history" | — |
| v2 `intake/README.md:42,58` | "Dates are years After the Grip (AG)." / "the Grip was 866 years ago" | — |
| v2 `.claude/agents/eotg-lore-keeper.md:22-23` | "(verify against SETTING LORE before quoting) / Orrin's Grip was 866 years ago" | — |
| v2 `.claude/agents/eotg-localizer.md:8`, `eotg-intake.md:22` | "866 years after a cataclysm" / "the Grip 866 years ago" | — |

**Not found anywhere:** a canon line that settles whether "the Grip" and "Orrin's Grip" are the same event. Outside SETTING LORE, every file uses the two interchangeably.

### 1.2 Contradictions
1. **Date.** These put the Grip about 1,000 years before 866:
   - SETTING LORE `:48`, `:351`, `:814`

   These put it 866 years before (0 AG):
   - SETTING LORE `:632`
   - `866_bookmark_design.md:11,110`
   - v1 README, CONTRIBUTING and CLAUDE.md
   - v1 events, story cycle and loc
   - v2 `CLAUDE.md:75`, `intake/README.md`, the agent files
2. **What 0 AG marks.** SETTING LORE `:351` says "recovered by 0 AG", but `:57`/`:356` say recovery filled the First Era. If 0 AG is not the Grip, "After the Grip" is a misnomer.
3. **One event or two.** SETTING LORE `:117`/`:365`/`:816` treat Orrin's Grip as a separate crisis around 131 AG. Elsewhere it is the 0 AG cataclysm.
4. **Era names.**
   - SETTING LORE: First Era 0–131, Second Era 131–850, Third Era 850 onward.
   - v1 README, CONTRIBUTING, the loc, the pitch and `866_bookmark_design.md:35`: Second Era = pre-Grip; Third Era = 0 AG onward.
   - SETTING LORE `:666` contradicts its own `:175`.
5. **"Second" as an era or a plane.** `eotg_l_english.yml:5` and README `:5` say "Second Material Plane".
6. **Wording.** "living history, not myth" vs "history, not living memory" (`866_bookmark_design.md:110`, `eotg_orrins_grip_l_english.yml:9`). Same meaning, opposite wording.
7. **New Cauldron's founding site.**
   - `866_bookmark_design.md:35` has the founders crash-land "on the Titanworld".
   - `eotg_exodus_l_english.yml:88` and `events/eotg_exodus_events.txt:641` say Mikey's generation "fled" the Titanworld.

### 1.3 Options, and what each would change
**A. AG counts from the Grip. The Grip = Orrin's Grip = 0 AG. Second Era = pre-Grip; Third Era = 0 AG onward. SETTING LORE's −1000 date, its "Orrin's Grip ~131" and its era table are errors.**
- **ERRATA** supersedes SETTING LORE `:48`, `:57`, `:102-103`, `:117-122`, `:175`, `:351-356`, `:365-370`, `:600-626` and `:814-821`.
- The ~131 AG crisis needs a new name.
- **Already consistent:** the v1 loc, the pitch, `eotg_st_is_third_era_ruler`, and every v2 file.
- **Still open:** "Second Material Plane". The audit's Legacies finding ("Second Era" strings, `v1_lift_readiness_cloud.md:123`) becomes resolved.

**B. SETTING LORE's body governs. The Grip ≈ 1,000 years before 866; 0 AG = end of recovery; Orrin's Grip ≈ 131 AG; eras 0–131 / 131–850 / 850 onward.**
- **Rewrite as "about a thousand years":**
  - v2 `CLAUDE.md:75`, `intake/README.md:58`, the lore-keeper, localizer and intake agent files
  - `866_bookmark_design.md:11,110`
  - `eotg_orrins_grip_l_english.yml:9,18,19`, the story cycle and events
  - `eotg_void_l_english.yml:65,93,94,125`, `eotg_religions_l_english.yml:96`
- **Redefine AG:** `intake/README.md:42`.
- **Change every "Second Era" string to "pre-Grip"**, and "eight centuries" to "a thousand years":
  - `eotg_legacy_l_english.yml`, `eotg_void_l_english.yml:22,133`
  - `eotg_maa_types.txt:196`, `eotg_legacy_on_actions.txt:188`, `events/eotg_legacy_events.txt:2`, the pitch
- `eotg_st_is_third_era_ruler` then means "since 850".

**C. AG counts from the Grip (0 AG). "Orrin's Grip" is a separate, later event around 131 AG.**
- Fix only SETTING LORE `:48`, `:351`, `:814`.
- **Change "Orrin's Grip" to "the Grip"** where it means the cataclysm:
  - `866_bookmark_design.md:11`
  - `eotg_traits.txt:8`, `eotg_l_english.yml:5`
  - `eotg_orrins_grip_l_english.yml:18-19`, the pitch, `eotg_legacy_l_english.yml:5`
- New Cauldron "from the ruins of Orrin's Grip" in 131 AG then fits as written.
- **Still to choose:** an era table, A's or B's.

**D. Answer only the date (0 AG); send era names and Grip/Orrin's Grip identity to the vault.**
- A one-line ERRATA entry.
- The "Second Era"/"Third Era" strings and `eotg_st_is_third_era_ruler` stay open on the taskboard.

### 1.4 Question
> Is "the Grip" the 0 AG cataclysm 866 years before the bookmark, the same event as "Orrin's Grip", and does "Second Era" name the civilisation before it (Third Era = 0 AG onward) or SETTING LORE's 131–850 AG period?

---

## 2. Titans, the Elrossi state, the major powers, and Carrigore (audit §3 item 2)

The SETTING LORE line numbers in `docs/qa/v1_lift_readiness_cloud.md:263-266` have shifted by +17:

| Audit cites | Now |
|---|---|
| 209–212 | 226–229 |
| 262 | 279 |
| 270 | 287 |
| 150 | 167 |
| 286 | 303 |
| 808 | 825 |

The audit also says SETTING LORE "never mentions New Cauldron". That is inaccurate: it appears once, as a location (`SETTING LORE:533`).

Shorthand in this section:
- `SL` = `OLD PROJECT VERSION/docs/SETTING LORE`
- `BD` = `OLD PROJECT VERSION/docs/866_bookmark_design.md`
- `RE` = `OLD PROJECT VERSION/docs/866_religions`
- Other paths are under `OLD PROJECT VERSION/`.

### 2a. Who are the Titans?
| file:line | Verbatim (trimmed) | Asserts |
|---|---|---|
| SL:9-15 (ERRATA) | "Orrin is NO LONGER imprisoned there — he is now in the material plane." | Frees Orrin only. Says nothing of Yu or Carrigore. |
| SL:226-229 | "THREE TITAN POWERS (Cosmic level entities): - YU THE STAINED: Lawful Neutral, Order/Justice, SEALED in The Dream - ORRIN THE EYE: Chaotic Evil, War/Chaos, IMPRISONED in The Void - CARRIGORE: Neutral Evil, Cosmos/Corruption, ACTIVE/EMERGED (major threat)" | **Three Titans.** |
| SL:231-235 | "YU PANTHEON … Primary Sons of Yu: … MALVRICK (Lawful Evil): Darkness, Void, Secrets" | Malvrick is a Son of Yu. |
| SL:527, 710-714 | "The Dream: Where Yu is sealed" / "YU THE STAINED: Sealed God of Order … Imprisoned in The Dream; no direct action" | Yu is sealed; no erratum changes this. |
| SL:698-701 | "CARRIGORE: Cosmic Destruction Entity … Not imprisoned/sealed like Yu and Orrin" | Carrigore is treated as their peer. |
| SL (whole file) | — | "Titan" appears only at `:226`. No mention of "Titan Exodus" or "Titanworld". |
| BD:110 | "The fractured cosmos, the weakened gods, the freed titans — all stem from 0 AG" | The Titans are freed. |
| BD:112 | "\"Titan\" refers specifically to Orrin (Void) and Yu (Dream) — capital-T Titans. Lower-case \"titan\" can refer to large creatures" | **Two Titans.** |
| BD:35, 85-87 | "crash-landed on the Titanworld" / "At 866 AG, the Titanworld still exists but is increasingly uninhabitable." | — |
| RE:113-114 | "eotg_rf_titan_worship … Looks past the sons to the Titans. Void Reverence. Reserved for future Carrigore and Orrin cults." | Carrigore is under titan worship. |
| RE:130-135 | "UNRESOLVED TENSION — VOID REVERENCE: … Malvrick is a Son of Yu, which argues for Divine Order." | — |
| `README.md:5,7` | "Orrin, Titan of the Void, tore through the fabric of reality…" / "freed titans … the looming shadow of Orrin and Yu's war" | — |
| `common/religion/religion_family_types/eotg_religion_families.txt:12-14,22-24` | "Divine Order — Yu and his sons: Elross, Bohemut, Malvrick…" / "Titan Reverence — looks past the sons to the Titans themselves … Carrigore and Orrin faiths on the backlog." | — |
| `common/religion/religion_types/eotg_religions.txt:929-931,961,1030,1037` | "# Fringe cults that venerate Carrigore and the Void" / `family = eotg_rf_titan_worship` / "HighGodName = eotg_god_malvrick" / "GoodGodNames = { eotg_god_malvrick eotg_god_carrigore … }" / "EvilGodNames = { eotg_god_elross eotg_god_yu … }" | The Titan-worship religion lists the Titan **Yu as evil**. |
| `eotg_religions.txt:110,117` (also 488, 1222) | "GoodGodNames = { eotg_god_elross eotg_god_yu … }" / "EvilGodNames = { eotg_god_carrigore eotg_god_orrin eotg_god_malvrick …}" | Elross faiths count Malvrick, a Son of Yu, as evil. |
| `localization/english/eotg_religions_l_english.yml:9-10` | "Yu the Stained (sealed in the Dream) and Orrin the Eye are Titans; Carrigore is the third." | **Three Titans.** |
| `localization/english/eotg_religions_l_english.yml:21-22` | "…through Elross, Bohemut and Malvrick … the same sealed father." / "…Yu sealed in the Dream, Orrin the Eye somewhere loose in the world, Carrigore feeding at the edges of it … the Grip was anything other than a Titan's work" | — |
| `localization/english/eotg_orrins_grip_l_english.yml:11,18,19` | "The Titans are Orrin (Void) and Yu (Dream), and they are still at war somewhere out in the dark." | **Two Titans, at war.** |
| `localization/english/eotg_l_english.yml:48` | "…And somewhere in the dark between stars, Orrin and Yu still war. This is 866 AG." | Yu is active. |
| `common/modifiers/eotg_modifiers.txt:25-27` | "devastation from the ongoing Titan wars" | — |
| v2 `.claude/agents/eotg-lore-keeper.md:13` | "Known errata already there: … Malvrick is not Carrigore." | **No such erratum exists** in SL:7-44. |

**Contradictions:**
1. **How many Titans?**
   - Three (Yu, Orrin, Carrigore): SL:226-229, religions loc `:9-10,:22`, RE:113-114.
   - Two (Orrin, Yu): BD:112, `eotg_orrins_grip_l_english.yml:11`.
2. **Is Yu sealed or free?**
   - Sealed: SL:227/527/710-714, religions loc `:21-22`.
   - Freed and at war: BD:110, README:7, `eotg_l_english.yml:48`, orrins_grip loc.
3. **Carrigore's nature.** SL calls it a Titan Power (`:229`), a "god of destruction" (`:288`) and a "Cosmic Destruction Entity" (`:698`), and puts it in neither pantheon.
4. **The Titanworld has no source in SL.** Nothing says which Titan it is named for.
5. **Malvrick's placement.**
   - Divine Order family: SL, `eotg_religion_families.txt`, religions loc `:21`.
   - His religion sits in titan worship (`eotg_religions.txt:931`, flagged at RE:130-135).
   - Elross faiths count him evil, yet Angelia worships him (BD:68).
6. **Titan worship lists a Titan (Yu) as evil** (`eotg_religions.txt:1037`).
7. **The lore-keeper agent file cites an erratum that does not exist** (see the last table row).

**Options and what each changes:**
- **A. Three Titans, as SL says.**
  - Add an erratum on BD:112. The orrins_grip text is incomplete rather than wrong.
  - Titan worship stays as planned (RE:291 Carrigore, RE:303 Orrin).
  - Add the fact to the lore-keeper and intake fixed points.
  - Yu sealed vs. freed is still open.
- **B. Two Titans; Carrigore is a lesser cosmic power.**
  - Erratum on SL:226-229 and the SL:701 framing.
  - Rewrite religions loc `:9-10,:22`, the `eotg_religion_families.txt:22-23` comment, and RE:113-114/291.
  - Carrigore's backlog religion needs a new family (with hostility and graphics), or "titan worship" becomes a misnomer.
- **C. Orrin and Yu are capital-T Titans; Carrigore is a Titan-class power of different origin.**
  - One ERRATA line plus a clause on BD:112.
  - Religions loc and RE survive as written.
- **Rider for every option:**
  - Decide Malvrick's family: keep him under titan worship, or move him to `eotg_rf_divine_order`. A move changes `eotg_religions.txt:931`, RE:130-135/185, the families comment, and religions loc `:96`.
  - Fix the phantom erratum at `eotg-lore-keeper.md:13`.

**Question:**
> Which beings are Titans at 866 AG (Yu, Orrin, Carrigore?), and is Yu still sealed in the Dream or freed and at war with Orrin?

### 2b. The Elrossi state: First or Second Imperium at 866, and is it the "Holy Elrossi Empire"?
| file:line | Verbatim (trimmed) | Asserts |
|---|---|---|
| SL ERRATA | — | Silent. |
| SL:140,147 | "Holy Elrossi Empire beginning to form as religious-political entity" / "Forming from scattered Elross-worshipping lands (not yet unified peak)" | Formed during the Second Era. |
| SL:279-285 | "HOLY ELROSSI EMPIRE (Lawful Good theocracy) … Capital: Elyria (Holy City) … Territory: Vast, dominant political force" | — |
| SL:742-746 | "High religious hierarchy with emperor/empress figure" | — |
| SL (whole file) | — | Never "Imperium", never "First" or "Second". |
| BD:26 | "\| Orro Invasion of the Second Elrossi Imperium \| ~1700 AG \|" | A Second Imperium exists by 1700. |
| BD:41-46 | "### The Elrossi Imperium … The Imperium at 866 is a First Imperium — the \"Second\" designation reflects a later reformation after collapse … **Holy sites to define:** Caer Myr …, Saint Argoth's Hold" | **First** at 866. |
| RE:145-149 | "Backbone of the Second Elrossi Imperium. Acting openly since 850 AG. … governed from Elyria." | **Second**, in the present tense. |
| `common/religion/religion_types/eotg_religions.txt:9` | "# Backbone of the Second Elrossi Imperium's moral and military authority." | Second. |
| `docs/art_needed.txt:626` | "(Second Elrossi Imperium's faith)" | Second. |
| `history/characters/eotg_characters_866.txt:20-23` | "At 866 AG this is the First Elrossi Imperium (the \"Second\" designation comes later after a period of collapse and reformation)." | First. |
| `history/titles/eotg_titles_866.txt:12-17` | "# eotg_e_elrossi_imperium = { … government = eotg_government_holy_imperium    # TODO" | Commented out; that government doesn't exist; the key form breaks invariant 2. |
| `localization/english/eotg_religions_l_english.yml:35,107` | "The Imperium's official reading of Elross, governed from Elyria" | — |
| `localization/english/eotg_myr_struggle_l_english.yml:6,14,66`; `eotg_orrins_grip_l_english.yml:32-33` | "The Elrossi Imperium fights at arm's length through the Prince of Myr…" | — |
| `docs/title_hierarchy.md:192`; `docs/EOTG_Events_Characters:21` | "against the First of the Third Elrossi crusade" / "from the First of the Third" | A third numbering scheme, never defined. |
| `docs/title_hierarchy.md:429-431` | "Capital: `caer_myr` … Lore: Elrossi Principality homeland." | Caer Myr belongs to Lanius. |
| `localization/english/eotg_heritage_l_english.yml:30` | "Descendants of the old Elrossi colonial network … the cultural memory of a lost order." | An earlier lost Elrossi network; no source links it to the numbering. |

**Contradictions:**
1. **First or Second.**
   - First: BD:44, the characters file.
   - Second (present tense): RE:147, `eotg_religions.txt:9`, `art_needed.txt:626`.
   - BD:26 (Second by ~1700) supports "First".
2. **Name.** SL always says "Holy Elrossi Empire"; every later file says "Elrossi Imperium".
3. **Seat.** Elyria (SL:281, RE:149) vs. holy site Caer Myr (BD:46), which `title_hierarchy.md` places in Lanius.
4. **"First of the Third"** is never defined.
5. **Government.** `eotg_government_holy_imperium` is referenced but doesn't exist (`docs/closed_alpha_checklist.md:61`).

**Options and what each changes:**
- **A. "Elrossi Imperium", First at 866.**
  - Edit RE:147, `eotg_religions.txt:9`, `art_needed.txt:626`.
  - ERRATA: SL's "Holy Elrossi Empire" = the (First) Imperium.
  - Gate 1 title `e_eotg_elrossi_imperium`, displayed without the ordinal.
- **B. Second at 866.**
  - Edit BD:26/44 and the characters file.
  - The vault must supply a First Imperium and its collapse before 866 (touches heritage loc `:30`).
- **C. Formal name "Holy Elrossi Empire".**
  - Rewrite religions, Myr struggle, orrins_grip and names loc, the README, and the Gate 1 title key and name.
- **D. Both names stand; no ordinal in player text.**
  - Drop "Second" at RE:147 and `eotg_religions.txt:9`; add one ERRATA line.

**Question:**
> At 866 AG, is the Elrossi state the First or the Second Imperium, and is its formal name "Holy Elrossi Empire" or "Elrossi Imperium"?

### 2c. Who are the major powers at 866?
| file:line | Verbatim (trimmed) | Asserts |
|---|---|---|
| SL:82 | "TRADE FEDERATION OF THORUM: Early merchant organizing" | Founded in the First Era. |
| SL:167, 825 | "Clear major powers have emerged (Elrossi, Coldiron, Trade Federation)" | **Three.** |
| SL:277-308 | "MAJOR POWERS (Tier 1): HOLY ELROSSI EMPIRE … CARRIGORE SPACE … COLDIRON CALIPHATE … TRADE FEDERATION OF THORUM (Neutral mercantile) - Worship: Bohemut … - Type: Merchant consortium … - Territory: Trade routes, coastal cities" | Four Tier 1 entries. |
| SL:296-301 | "COLDIRON CALIPHATE … Conflict: Opposes Holy Elrossi Empire; isolationist theology … defensive expansion" | — |
| SL:310-345 | "SECONDARY POWERS (Tier 2): THE PALE HAND … HELIX CORPORATION … THE LAUGHING BLADES … THE WARRENS … DOMAIN OF THE ETERNAL KING … ORRIN WARPARTY" | — |
| SL:533 | "New Cauldron: Advanced tech sector" | Only as a location. |
| SL:754-758 | "Trade Federation of Thorum - Merchant council leadership … Secular/neutral orientation … Attempts to remain apart from religious conflicts" | — |
| SL (whole file) | — | Never mentions Gob-Ogre, Angelia, the Daimyos, the Shatter Stance, Nikios, Lanius or the Myr Cluster Wars. |
| BD:3 | "the canonical reference for what the galaxy looks like at the mod's starting bookmark" | Also claims canon status. |
| BD:30-81 | "### New Cauldron … ### The Elrossi Imperium … ### Gob-Ogre Trade League … ### Coldiron Caliphate … ### Nikios Khanate … ### Angelia … ### Broken Daimyos … ### The Shatter Stance" | **Eight** states. |
| BD:49-50 | "Corporate oligarchy — 50 Trade Princes" / "Aggressively entering the Myr Clusters … Karim Ibn Al Daveed is not yet realized (he razes Grand Kiln in 880 AG) — so at 866 they are at peak confidence" | — |
| BD:56 | "Faith-driven expansionists pressing into the Myr Clusters" (Coldiron) | — |
| BD:59-63 | "### Nikios Khanate … **Species:** Centaur" | **Deferred (invariant 9).** |
| `README.md:26-33` | New Cauldron … Elrossi … Gob-Ogre … Coldiron … Nikios … Angelia … Broken Daimyos | Seven (no Shatter Stance). |
| `common/struggle/struggles/eotg_myr_struggle.txt:3-6` | "Four great powers contest the Cluster: the Elrossi Imperium …, New Cauldron's mercenary legions, the Gob-Ogre Trade League, and the Coldiron Caliphate" | — |
| `history/titles/eotg_titles_866.txt:12-69` | Elrossi, Cauldron (`eotg_government_cauldron_republic`), Gob-Ogre (`_trade_council`), Coldiron (`_caliphate`), Nikios, Angelia (`_conclave`) | All commented out. **Six referenced governments don't exist.** |
| `common/landed_titles/eotg_landed_titles.txt:8-533` | "eotg_e_myr_cluster = { eotg_k_myr_core … eotg_k_lanius_expanse … }" | The only defined empire. |
| `docs/title_hierarchy.md:540,681` | "Gob-Ogre Trade League corporate territory." / "Industrial ruins of the collapsed Gob-Ogre Trade League." | The League has **collapsed**. |
| `history/characters/eotg_characters_866.txt:12-17,82-91` | ID ranges for each power, Shatter Stance empty / "Karim … campaign begins ~851 AG" / Kazrik `faith:eotg_faith_commerce` | — |
| `history/characters/eotg_characters_866.txt:41-43` vs `:332-335`; `docs/bookmark-char-story:3`; `docs/EOTG_Events_Characters:14` | Vessarion is the Elrossi "Prince of Myr" / Caelorin of Lanius is the "Prince of Myr" ("Fabricated propaganda title") | **Two Princes of Myr.** |
| `docs/EOTG_Events_Characters:277,292` | "Gob-Ogre Trade League · Last Standing Trade Prince" / "others died … to Karim Ibn Al'Daveed's Chad Orc campaign" | Karim has already struck. |
| `docs/EOTG_Events_Characters:553-562` | Win-condition empires: New Cauldron, 7th Legion, Warrens, Helix, Coldiron, Gob-Ogre, Lanius, Xerxes | No Elrossi. |
| `docs/Bookmark-Characters` (headings) | XERXES, HELIX, 7TH LEGION, NEW CAULDRON, GOB–OGRE, COLDIRON, LANIUS, RATFOLK | — |
| `common/governments/*.txt` | Cartel, Corporation, Elven Monarchy, Fringe, Gob-Corp ("…of the Gob-Ogre Trade League"), New Cauldron, PMC | Only two map to roster nations. |
| `localization/english/eotg_l_english.yml:24-41` | "eotg_culture_goborc:0 \"Gob-Ogre\" … eotg_culture_centaur … eotg_culture_aasimar … eotg_culture_nippon:0 \"Daimyo\"" | Loc for cultures that aren't defined. |
| `localization/english/eotg_religions_l_english.yml:52`; RE:49-57 | "…share a federation with them…" / Bohemites trade alongside goblins inside the League | Hints that Federation = League. |
| v2 `.claude/agents/eotg-lore-keeper.md:13-14` | lists SETTING LORE first, then 866_bookmark_design | v2 ranks SL above BD. `CLAUDE.md:75` lists both with no order. |

**Contradictions:**
1. **The rosters disagree:**

   | Source | Count | Powers |
   |---|---|---|
   | SL | 3 (+ Carrigore Space) | Elrossi, Coldiron, Trade Federation |
   | BD | 8 | New Cauldron, Elrossi, Gob-Ogre, Coldiron, Nikios, Angelia, Broken Daimyos, Shatter Stance |
   | README | 7 | BD minus the Shatter Stance |
   | v1 struggle | 4 | Elrossi, New Cauldron, Gob-Ogre, Coldiron |
   | v1 title history | 6 | Elrossi, New Cauldron, Gob-Ogre, Coldiron, Nikios, Angelia |
   | Playable arcs | 8 | Xerxes, Helix, 7th Legion, New Cauldron, Gob-Ogre, Coldiron, Lanius, Ratfolk (no Elrossi) |

   Only Elrossi and Coldiron are on every list.
2. **SL's Tier 2 powers are absent** from BD and from v1 script.
3. **New Cauldron's scale.** SL has only a "tech sector"; BD has a 735-year-old republic.
4. **Trade Federation of Thorum vs. Gob-Ogre Trade League:**
   - For them being one polity: both are the merchant power; Bohemut worship; "federation" in religions loc `:52`.
   - Against: SL's polity is secular, neutral and coastal, and founded 0–131 AG; BD's is an aggressive 50-prince oligarchy.
5. **The League at 866.**
   - At peak (BD:50).
   - Karim's campaign already under way since ~851, princes dead (the characters file, `EOTG_Events_Characters:292`).
   - "Collapsed" (`title_hierarchy.md:681`).
6. **Coldiron.** Isolationist and defensive (SL) vs. expansionist (BD:56).
7. **The Prince of Myr** is two different characters.
8. **No v1 script backs BD's roster.**
   - Two of seven governments match; six are referenced but missing.
   - No empire or kingdom keys are defined (and they use the invalid `eotg_e_` form).
   - Four cultures have loc but no definition.
9. **Nikios** appears throughout but is deferred.

**Options and what each changes:**
- **A. BD's roster is canon for 866.**
  - ERRATA: SL:277-345 describe the setting outside the 866 scope.
  - Gate 1 builds New Cauldron, Elrossi, Gob-Ogre, Coldiron, Angelia, the Broken Daimyos and the Shatter Stance (Nikios deferred).
  - The architect specs the missing governments.
- **B. SL's roster is canon** (Elrossi, Coldiron, Thorum; Carrigore Space as a threat).
  - Rewrite BD:30-81, the README, the struggle, the opening loc and the scope of `Bookmark-Characters`.
  - Demoting New Cauldron breaks its exclusive government and its arcs.
- **C. Merge: League = Federation of Thorum.**
  - One ERRATA line.
  - Settle its posture and its state at 866.
  - Gate 1 title naming; possibly reconcile the ruler's faith (Commerce vs. Plutocracy).
- **D. They are distinct.**
  - Thorum needs its own nation brief, map place and culture.
  - Revise religions loc `:52`.
- **Any option** must also settle the Prince of Myr and Karim's timing before bookmark history is written.

**Question:**
> Which realms are the major (Tier 1) powers at 866 AG, and is the Gob-Ogre Trade League the same polity as the Trade Federation of Thorum?

### 2d. What is Carrigore's alignment?
| file:line | Verbatim (trimmed) | Asserts |
|---|---|---|
| SL ERRATA | — | Silent. |
| SL:229 | "CARRIGORE: Neutral Evil, Cosmos/Corruption, ACTIVE/EMERGED (major threat)" | **Neutral Evil** (the entity, in the Titan list). |
| SL:262-264,268 | "SAMULO THE STARDRINKER (Demigod, Neutral Evil) … Carrigore Space, Cult of the Cosmos" / "Samulo spreads Carrigore worship" | — |
| SL:287-290 | "CARRIGORE SPACE (Chaotic Evil chaos entity + followers) - Leader: Carrigore (god of destruction) - Type: Extradimensional threat, chaotic military force" | **Chaotic Evil**, in the heading of the *polity*. |
| SL:526, 698-701, 760-763 | "Extradimensional chaos realm" / "Cosmic Destruction Entity" / "Carrigore (entity) as supreme commander … Blue hobgoblin generals" | No alignment given. |
| BD:69 | "defend the Border Systems against constant Carrigore Space raids" | — |
| RE:291-297 | "eotg_religion_carrigore … eotg_faith_cult_of_cosmos (organised, ambitious…) and eotg_faith_feral_star (uncoordinated frontier shamans…)" | One ordered faith and one chaotic one. |
| `common/religion/religion_types/eotg_religions.txt:112,300,483,666,849,1217,1772,1955` | "DevilName = eotg_god_carrigore" | Carrigore is the Devil in 8 religions. |
| `eotg_religions.txt:1020,1030` | "WaterGodName = eotg_god_carrigore" / GoodGodNames includes Carrigore | Revered in Void Reverence. |
| `localization/english/eotg_religion_gods_l_english.yml:41-42` | "eotg_god_carrigore:0 \"Carrigore\"" | Name only; no alignment anywhere in loc. |

**Contradictions:**
1. SL:229 says Neutral Evil (the entity); SL:287 says Chaotic Evil, but in the heading of "entity + followers". Whether `:287` describes the god or the faction is unclear.
2. Carrigore's domain and nature are given three ways, and it sits in neither pantheon.
3. Samulo is "unaligned" (`:262`) yet spreads Carrigore worship.

**Options.** CK3 has no alignment field (`UNVERIFIED-VANILLA`), so whichever option is chosen lands in faith design (backlog RE:291-297), faith and god loc, and the tone of Carrigore Space.
- **A. Neutral Evil god, Chaotic Evil host.** One ERRATA line. No file changes. The two backlog faiths split along these lines.
- **B. Chaotic Evil throughout.** Erratum on SL:229. The "organised" Cult of the Cosmos needs a rethink.
- **C. Neutral Evil throughout.** Erratum on the SL:287 heading. Carrigore Space becomes disciplined rather than frenzied.
- **D. Drop alignments from canon.** D&D alignments never show in game; the lore-keeper stops citing them.

**Question:**
> Is Carrigore Neutral Evil or Chaotic Evil, and does the "Chaotic Evil" label at SETTING LORE:287 describe the god or only the Carrigore Space host?

---

## 3. Fixed points with no canon source: "Myr Cluster Wars ignited 850 AG" and "Exodus wanes after 1000 AG" (audit §3 item 3)

### 3.1 Sources
| file:line | Verbatim (trimmed) | Asserts |
|---|---|---|
| `docs/SETTING LORE:31-34` (ERRATA Helix) | "Its corporate command dissolved when Xerxes flooded in 850 AG" | The Xerxes flood was in 850. No war is mentioned. |
| `docs/SETTING LORE:178-179,187,821` | "850 AG Threshold Events: / - Gods begin actively meddling…" / "~850-855 AG: Divine Awakening Phase" | **850 AG is a divine threshold.** |
| `docs/SETTING LORE:508,515` | "Xerxes: Major city in Myr Clusters region" / "Myr Clusters: Campaign 3 major region" | **No "Myr Cluster Wars" anywhere in SETTING LORE.** |
| `docs/SETTING LORE:226-229` (and the whole file) | — | **No "Titan Exodus", "Titanworld" or "Mikey" anywhere in SETTING LORE.** New Cauldron appears only at `:533`. |
| `docs/866_bookmark_design.md:13` | "\| Titan Exodus begins \| 131 AG \|" | — |
| `docs/866_bookmark_design.md:23` | "\| Myr Cluster Wars end \| 1300 AG \|" | An end date is given; **no start date.** |
| `docs/866_bookmark_design.md:37,44,50,56` | "Entering the Myr Cluster Wars in early phase" … | In an early phase at 866. |
| `docs/866_bookmark_design.md:87` | "The Titan Exodus is not a single event but an ongoing process. At 866 AG, the Titanworld still exists but is increasingly uninhabitable." | Ongoing. **No waning date.** |
| `docs/866_religions:147,236` | "Acting openly since 850 AG." | 850 AG is divine. |
| `docs/EOTG_Events_Characters:58,68` | "survived the Water Oni flooding of 850 AG" | Flood in 850. |
| `docs/EOTG_Events_Characters:339` | "Declared the Myr Cluster Jihad in 851." | Coldiron's front opens in **851**. |
| `docs/EOTG_Events_Characters:543` | "Three phases: Brewing → Ongoing → Ending" | v1 script has 5 phases. |
| `docs/EOTG_Events_Characters:605` | "Xerxes the Hero unified the Myr Clusters … spent three centuries and one catastrophic flood" | An earlier Myr conflict. |
| `docs/bookmark-char-story:4639` | "responsible for the flooding of Xerxes in 851" | **851**, against the ERRATA's 850. |
| `docs/closed_alpha_checklist.md:65` | "ignition seeded 850 AG" | — |
| `docs/system_depth_audit.md:71` | "an Exodus "still ongoing" after 735 years fires at the same rate in 866 as in 1200" | The waning date was added after this audit. |
| `CLAUDE.md:131-133`; `README.md:19-20`; `CONTRIBUTING.md:175` | "The Myr Cluster Wars **just ignited** (850 AG)" / "The Titan Exodus (begun 131 AG) is still ongoing — the last refugees … continue trickling" | The likely origin of the v2 wording. |
| `history/struggles/eotg_myr_struggle_history.txt:2,7` | "The Myr Cluster Wars ignite in 850 AG — sixteen years before the 866 AG bookmark" / `850.1.1 = {` | **The script that carries the date.** |
| `history/characters/eotg_characters_866.txt:5-6,41,84` | "Myr Cluster Wars just ignited (850 AG)" / "Prince of Myr … (installed ~850 AG)" / "Karim Ibn Al Daveed's campaign begins ~851 AG" | — |
| `common/struggle/struggles/eotg_myr_struggle.txt:3` | "Ignited 850 AG; historically ends ~1300 AG" | — |
| `events/eotg_story_orrins_grip.txt:6-7,64,116` | "The Myr Cluster Wars ignited sixteen years ago" | — |
| `common/on_action/eotg_on_actions.txt:2260` | "THE WANING (1000 AG): the Titanworld is nearly empty by the year 1000." | **The only source for the 1000 AG date is v1 script.** |
| `common/on_action/eotg_on_actions.txt:2269-2360` | `current_year >= 1000` / `< 1000` | Hard-coded gates. |
| `events/eotg_exodus_events.txt:13-19,633-641,663` | "eotg_exodus.0009 — The Last Fleets (one-time ~1000 AG…)" | — |
| `localization/english/eotg_exodus_l_english.yml:5-11,34,86,88,91` | "The Exodus began in 131 AG and is still running … From 1000 AG the arrivals thin to a trickle" / "Eight and a half centuries after…" | — |
| `localization/english/eotg_myr_struggle_l_english.yml:5,9,14,87` | "Ignited 850 AG, sixteen years before the bookmark" / "grind on until 1300 AG" | — |
| `localization/english/eotg_orrins_grip_l_english.yml:25,32-33` | "every season since 131 AG" / "Sixteen years ago, four powers reached for the Myr Clusters in the same decade" | The fronts open within one decade, not one year. |
| v2 `CLAUDE.md:75`; `intake/README.md:58` | "the Titan Exodus is ongoing; the Myr Cluster Wars ignited 850 AG" | — |
| v2 `.claude/agents/eotg-lore-keeper.md:22,24-25` | "(verify against SETTING LORE before quoting)" / "it wanes after 1000 AG" / "ignited 850 AG" | SETTING LORE has neither. |
| v2 `.claude/agents/eotg-intake.md:22`; `OLD VERSION CATALOG.md:68` | "Myr Wars since 850" / "waning after 1000 AG" | — |

### 3.2 Contradictions
1. **The 850 AG date for the Myr Cluster Wars has no canon source.** It comes only from v1 script, loc and READMEs, and the v2 files copied it. In SETTING LORE, 850 is the Divine Awakening. `866_bookmark_design.md` gives only an end date (1300).
2. **850 or 851?** The ERRATA flood, `EOTG_Events_Characters:58` and the struggle history say 850. These say 851:
   - Coldiron's jihad (`EOTG_Events_Characters:339`)
   - Karim's campaign (`eotg_characters_866.txt:84`)
   - the Xerxes flood (`bookmark-char-story:4639`, which contradicts the ERRATA)
   - "in the same decade" (`eotg_orrins_grip_l_english.yml:32`)
3. **The 1000 AG waning comes only from v1 script and loc.** `866_bookmark_design.md:87` says only "ongoing". SETTING LORE has no Exodus at all.
4. **Year counts drift.** "Eight centuries" (`events/eotg_exodus_events.txt:641`) vs "eight and a half" (loc `:88`) at 1000 AG. Minor.
5. **Is the Exodus fading at 866?** v1 README `:19` says refugees are "trickling" at 866. `866_bookmark_design.md:87` and `eotg_orrins_grip_l_english.yml:25` say fleets are still arriving in force.
6. **Phase count.** 3 phases (design doc) vs 5 (v1 script). The Myr lift will meet this.

### 3.3 Options, and what each would change
**A. Put both in the ERRATA as written** ("ignited 850 AG"; "Exodus began 131 AG, ongoing at 866, wanes around 1000 AG").
- The struggle history, the Exodus year gates and the waning events lift unchanged.
- Correct `bookmark-char-story:4639`, `EOTG_Events_Characters:339` and `eotg_characters_866.txt:84` to 850, or recast them as fronts that opened after the ignition.

**B. Ratify 850 and "ongoing at 866"; leave the waning date to the vault.**
- Drop "wanes after 1000 AG" from `eotg-lore-keeper.md:24` and catalog `:68`.
- Make the Exodus gates (`eotg_on_actions.txt:2260-2365`) one tunable value, or hold them.
- Soften or hold the "~1000 AG" Exodus loc.

**C. Soften both into ranges** ("the early 850s, about sixteen years before the bookmark"; "ongoing and slowly thinning").
- The engine date stays `850.1.1`.
- Soften `eotg_myr_struggle_l_english.yml:5,14`.
- Reword v2 `CLAUDE.md:75`, `intake/README.md:58`, `eotg-lore-keeper.md:24-25` and `eotg-intake.md:22`.

**D. Strike both from the v2 "fixed points" until the vault answers.**
- Edit v2 `CLAUDE.md:75`, `intake/README.md:58` and the agent files.
- The Myr struggle lift (its start date) and any Exodus lift become blocked.

### 3.4 Question
> Should "the Myr Cluster Wars ignited in 850 AG (the year of the Xerxes flood)" and "the Titan Exodus began 131 AG, is ongoing at 866 and wanes around 1000 AG" become ERRATA canon, or does the vault date them differently?

---

## 4. Helix: CB-28's five open points

> **Line-number note.** The SETTING LORE body has shifted down about 17 lines. `docs/qa/v1_lift_readiness_cloud.md` still cites `:302-306` (now `:319-323`) and `:127,218` (now `:144,235`).

### 4.0 Sources shared by every point
| file:line | Verbatim (trimmed) | Asserts |
|---|---|---|
| `OLD PROJECT VERSION/docs/SETTING LORE:31-37` (ERRATA) | "At 866 AG Helix is a REMNANT in structure and ACTIVE AND GROWING in fact. The pre-collapse corporation is gone. Its corporate command dissolved when Xerxes flooded in 850 AG … it holds THREE COUNTIES, and they lie in DIFFERENT duchies, not in one contiguous block." | Landed, holding 3 non-contiguous counties. |
| `SETTING LORE:38-41` (ERRATA) | "\"Corporate board structure; CEO authority\" … describes Helix BEFORE 850 and is superseded for 866 AG … \"Remnant\" means post-collapse, not dwindling." | The board/CEO structure is superseded. |
| `SETTING LORE:319-323` | "HELIX CORPORATION (Neutral tech-focused) - Type: Technology company, assassination/espionage … - Status at 866 AG: Active and growing" | — |
| `SETTING LORE:446-450` | "6. PALE HAND OPERATIONS (850-866 AG, not widely known) … - Helix Corporation expanding mysteriously" | — |
| `SETTING LORE:777-781` | "Helix Corporation - Corporate board structure; CEO authority … - Growing in influence; connections unclear - Suspected ties to Pale Hand conspiracy" | — |
| `circlebackTaskboard.md` (CB-28) | the five points; "**The cartographer must not lift it as written.**" | — |

`866_bookmark_design.md`, `intake/` (no briefs yet) and `docs/specs/regions/` (empty) never mention Helix.

### 4.1 Where are the 3 counties?

**The v1 draft conflicts with the ERRATA.** `title_hierarchy.md` gives Helix **two whole duchies** (6 counties, 30 baronies). The ERRATA allows 3 counties, each in a different duchy. Neither v1 Helix duchy can be lifted as written.

| file:line | Verbatim | Asserts |
|---|---|---|
| `OLD PROJECT VERSION/docs/title_hierarchy.md:163-164` | "### Duchy: Helix Remnant" / "> Capital: `helixfall` (Province 50) via County of Helixfall" | A whole duchy. |
| `title_hierarchy.md:166,173,181,185` | "#### County of Helixfall `[DUCHY CAPITAL COUNTY]`" / "#### County of Fracturepoint" / "#### County of Remnant Core" / "\| 58 \| `helix_tomb` \|" | 3 counties, provinces 50–59. |
| `title_hierarchy.md:251-252` | "### Duchy: Helix Fringe" / "> Capital: `helixport` (Province 83) via County of Helix" | A second whole duchy. |
| `title_hierarchy.md:254,262,270` | "#### County of Helix" / "#### County of Fringefall" / "#### County of Tangent" | 3 more counties, provinces 83–95. |
| `title_hierarchy.md:860-869` | "\| 50 \| helixfall \| County of Helixfall \| Helix Remnant \| The Myr Core \|" … | Kingdom: **The Myr Core**. |
| `title_hierarchy.md:893-905` | "\| 83 \| helixport \| County of Helix \| Helix Fringe \| The Cauldron Marches \|" … | Kingdom: **The Cauldron Marches**. |
| `title_hierarchy.md:157,857` | "\| 47 \| helix_margin \| County of Corefall \| Coreward Expanse \| The Myr Core \|" | A Helix-named barony in a third duchy. |
| `title_hierarchy.md:12` | "All title keys should use the prefix `eotg_` in landed_titles.txt" | The source of the invalid `eotg_d_` keys (invariant 2). |
| `common/landed_titles/eotg_landed_titles.txt:94-111,158-175,86-88` | "eotg_d_helix_remnant = {" … "eotg_d_helix_fringe = {" … "eotg_b_helix_margin = {}" | The draft as script. |
| `history/titles/eotg_titles_866.txt:143-158,194-209` | "# ── HELIX REMNANT ──" / "eotg_c_helixfall = { 866.1.1 = { culture = culture:eotg_culture_virens } }" … "eotg_c_fringefall … eotg_culture_tangentine" | **No holder and no government.** Two of the Fringe counties carry Cauldron-listed culture. Whether `culture =` is valid in title history is `UNVERIFIED-VANILLA`. |
| `common/struggle/struggles/eotg_myr_struggle.txt:6,43-47` | "fought over the homes of the Helix remnant locals." / "# Helix remnant locals" virens / veltrani / caldryx / duskvein | The whole Cluster is Helix homeland. |
| `localization/english/eotg_myr_struggle_l_english.yml:14,120,133` | "Beneath all four live the Helix remnant peoples, whose worlds these are" / "… a recognition of Helix remnant title …" | — |
| `docs/EOTG_Events_Characters:107,134` | "Domain limit intentionally constrained — tight, controlled territory" / "`eotg_ghost_corporate_continuity` … Stabilises dispersed holdings." | **Dispersed** holdings, which fits the ERRATA. |

**Contradictions:**
1. Two whole duchies in the draft and in v1 script vs 3 non-contiguous counties in the ERRATA.
2. The struggle text makes the whole Cluster Helix homeland. That works only if the Helix **peoples** (a culture sphere) are distinct from the Helix **polity**.
3. v1 history puts Cauldron culture on two of the Helix Fringe counties.
4. SETTING LORE `:320` "Technology company" vs ERRATA `:32` "corporation is gone".

**Options:**
- **A. One county in each of three duchies.** For example, the Remnant area, the Fringe area, and Coreward Expanse near `helix_margin`.
  - Changes: Gate 1 titles and duchy names, title loc (`eotg_titles_l_english.yml:27-34,100-126,329-373`), history, the Helix region brief.
- **B. Three counties in different kingdoms** (Myr Core, Cauldron Marches, a third). This fits "dispersed holdings".
  - Changes: as A, plus the struggle text (scattered enclaves instead of "whose worlds these are").
- **C. All three in The Myr Core, one of them in Xerxes Reach.** This links to 4.2.
  - Changes: the Gate 1 Myr Core layout and the Clayd arc.
- **D. "Helix" is a culture sphere across many counties; the polity holds only 3.**
  - Changes: none to the heritage and culture loc; the struggle loc `:14,:120,:133` must separate polity from peoples.

**Question:**
> Where, and in which duchies, do Helix's three counties lie, and are the "Helix peoples" a wider culture sphere than the three-county polity?

### 4.2 Is any county on or near Xerxes?
| file:line | Verbatim | Asserts |
|---|---|---|
| `SETTING LORE:20-24` (ERRATA) | "Xerxes is a PERSON … The city, the planet and the system are all named after him … ruled at 866 AG by Vaelorin Sylvaerath" | Vaelorin holds Xerxes. |
| `docs/bookmark-char-story:510-512` | "# **THE GHOSTS BENEATH XERXES**" / "### *Helix Corp Remnants Narrative Arc*" | — |
| `docs/bookmark-char-story:945` | "> Helix died before Xerxes drowned." | — |
| `docs/bookmark-char-story:1181,1206` | "* Gain Claim on Xerxes County" / "Clayd begins openly planning reclamation of Xerxes." | Helix does **not** hold Xerxes. |
| `events/eotg_clayd_events.txt:257-259` | "# \"Helix should rule what weaker systems couldn't.\" — ascendancy" | The script grants **no** Xerxes claim (the design doc does). |
| `docs/EOTG_Events_Characters:106,110` | "**Human (Xerxes drainage district)**" / "When the flood took Xerxes in 850 and corporate command dissolved…" | Clayd comes from Xerxes. |
| `docs/EOTG_Events_Characters:58` | "Aelthorin Sylvaerath governs the elven population of Xerxes … Helix Corp academy trained" | Names the ruler Aelthorin, not Vaelorin. |
| `docs/EOTG_Events_Characters:593` | "Helix Corp once backed Xerxes the Hero of Myr … Clayd grew up in the drainage channels beneath those towers." | — |
| `common/on_action/eotg_legacy_on_actions.txt:196-199` | "# Clayd's Helix remnant lives above a buried metropolis of their own people" / "# Vaelorin's seat at Xerxes keeps an archive fragment" | Helix's seat is separate from Vaelorin's. |
| `localization/english/eotg_bookmark_chars_l_english.yml:181,199` | "Helix was already dead before Xerxes drowned." / "I stand overlooking a reconstructed Helix facility. Drainage tunnels." | — |
| `docs/title_hierarchy.md:50-59` | "### Duchy: Xerxes Reach" … "\| 3 \| `the_sunken` \|" | — |

Adjacency can't be checked here (`map_data/` is off-limits). By title tree alone, the Helix Remnant duchy shares The Myr Core with Xerxes Reach.

**Contradictions:**
1. "Buried metropolis of their own people" and "Ghosts *Beneath* Xerxes" vs "Gain Claim on Xerxes County".
2. Xerxes' ruler is Aelthorin (`EOTG_Events_Characters:58`) vs Vaelorin (ERRATA `:23`; `history/characters/eotg_characters_866.txt:129-130`).

**Options:**
- **A. One county is the drowned under-city, separate from Vaelorin's Xerxes.**
  - Changes: split Xerxes Reach at Gate 1; the claim targets Vaelorin's county.
- **B. Near, not on.** One county borders Xerxes Reach.
  - Changes: map placement only.
- **C. Not near.** Xerxes is only origin and memory.
  - Changes: rewrite the "buried metropolis" comment; the arc title becomes figurative.

**Question:**
> Does any Helix county sit on or beside drowned Xerxes, and is the "buried metropolis" under Helix's seat Xerxes itself?

### 4.3 What is its government?
| file:line | Verbatim | Asserts |
|---|---|---|
| `common/governments/eotg_corporation_government.txt:2-6` | "Corporation Government — Cyberpunk corporate oligarchy … Board of Regional Directors elects the CEO." | — |
| `docs/EOTG_Government_Design_Document_v2.md:139-140` | "**Key:** `eotg_corporation_government`" / "**Nations:** P&D Co, Helix Corp remnants, human corporate minor nations" | Helix was the intended user. |
| `docs/EOTG_Government_Design_Document_v2.md:147-153` | "\| Kingdom \| Regional Director …" / "\| Empire \| CEO \| … Elected by Board of Regional Directors \|" | The ladder needs kingdom and empire tiers. |
| `docs/EOTG_Government_Design_Document_v2.md:468` | "`eotg_corporation_government` is reachable via PMC evolution but not independently assigned to any starting nation" | — |
| `events/eotg_pmc_command_events.txt:217-218` | "change_government = eotg_corporation_government" | The only path into it in v1. |
| `history/titles/eotg_titles_866.txt:143-158,194-209` | (no `government =`) | — |
| `docs/EOTG_Events_Characters:123` | "`eotg_corporate_continuity` \| CUSTOM. Inherited Helix governance." | — |
| `docs/bookmark-char-story:918,1021` | "Helix begins evolving into authoritarian continuity-state." / "Helix becomes paranoid authoritarian apparatus." | — |

**Contradictions:**
1. The Corporation government's board/CEO model is the structure the ERRATA supersedes.
2. Its kingdom and empire roles can't be filled by a 3-county realm (engine behaviour `UNVERIFIED-VANILLA`).
3. The design doc names Helix as a Corporation user, but v1 never assigned it.

**Options:**
- **A. The Corporation government as-is.**
  - Changes: `government =` in history. The loc keeps board/CEO text, which contradicts the ERRATA.
- **B. The Corporation government reframed as "continuity".**
  - Changes: `common/customizable_localization/eotg_government_loc.txt`, `eotg_corporation_l_english.yml:3-6`, an architect spec.
- **C. A new `eotg_` continuity government.**
  - Changes: a new spec and government. Waits for the governments rewrite.
- **D. A vanilla government as a stopgap.**
  - Changes: history only.

**Question:**
> At 866, does Helix run the v1 Corporation government (board and CEO), a reframed or new "continuity" government, or a stopgap until governments are lifted?

### 4.4 Who leads it?
| file:line | Verbatim | Asserts |
|---|---|---|
| `docs/Bookmark-Characters:51-63` | "# 🏭 HELIX REMNANTS" / "## Clayd Kestrel-Vire" / "*\"The Last Shotcaller\"*" / "Former Rook enforcer turned post-collapse Helix strongman." / "* Age: 41" | — |
| `docs/Bookmark-Characters:592-600` | "## Mirelle Voss" / "Former Helix executive opposing Clayd internally." / "* Age: 54" | An internal rival. |
| `docs/EOTG_Events_Characters:106,110` | "**Age:** 44 · **Male** · … **Education:** `intrigue_killer_3`" / "He became Helix's continuity by elimination." | — |
| `docs/EOTG_Events_Characters:558` | "\| Helix Corp (Clayd) \| `e_ascendant_compact_helix` \| The Ascendant Compact of Helix \|" | A future empire title. |
| `history/characters/eotg_characters_866.txt:149-169` | "eotg_char_90002 = { name = \"Clayd\" … culture = culture:eotg_culture_virens … 825.6.15 = { birth = yes } … add_trait = education_intrigue_4" | Age 41, education intrigue 4. |
| `history/characters/eotg_characters_866.txt:434-440` | "OPTIONAL CHARACTERS" … "eotg_char_90010 = { name = \"Mirelle\" …" | — |
| `common/on_action/eotg_char_arc_actions.txt:36-40` | "character:eotg_char_90002 = { is_alive = yes is_landed = yes }" | The arc needs Clayd to be landed. |

**Contradictions:**
1. Clayd's age is 41 in one source and 44 in another.
2. His education is intrigue 4 vs intrigue_killer_3, and his trait sets differ.
3. No v1 source gives him a title, so the v1 arc never fires.

**Options:**
- **A. Clayd holds all three counties.** This fits "tight, controlled territory".
- **B. Clayd holds two; Mirelle Voss holds one as his vassal.** Mirelle becomes a required character.
- **C. Clayd holds one or two; an independent rival holds the rest.** Helix is then not one realm (affects 4.3).
- **D. Clayd is liege over three vassal counts** (new characters).

Each option changes the holders in `history/titles` and the character history. The intake ruler briefs settle age and education.

**Question:**
> Does Clayd hold all three Helix counties himself, or do Mirelle Voss or others hold some as vassals or rivals, and what are his canonical age and education?

### 4.5 Pale Hand ties
| file:line | Verbatim | Asserts |
|---|---|---|
| `SETTING LORE:780-781` | "- Growing in influence; connections unclear - Suspected ties to Pale Hand conspiracy" | Suspected only. |
| `SETTING LORE:449` | "- Helix Corporation expanding mysteriously" (under "PALE HAND OPERATIONS … not widely known") | — |
| `SETTING LORE:312-317` | "THE PALE HAND (Neutral Evil corporate/assassination) … Leadership: Secret … Origins unclear; role in current events unknown" | — |
| `SETTING LORE:200,210,218` | "Pale Hand conspiracy operations reported but unconfirmed" … "spreading but not yet exposed" | — |
| ERRATA `:31-41` | (silent on the Pale Hand) | — |

No v1 script, loc, history or character doc mentions the Pale Hand. No source contradicts another.

**Options:**
- **A. Suspected only.** No change; future loc can rumour it.
- **B. Confirmed tie.** A new ERRATA entry and Helix brief. The cybernetics syndicate stays unnamed either way.
- **C. Explicitly unrelated.** ERRATA amends `:449` and `:781`.

**Question:**
> Are Helix's Pale Hand ties still unconfirmed rumour at 866, or does the vault settle them?

### 4.6 Other Helix text each answer touches
Paths under `OLD PROJECT VERSION/`:
- **Cultures and heritage** (4.1-D):
  - `common/culture/cultures/eotg_cultures.txt:76-83` (HELIX SPHERE: virens, veltrani, caldryx, duskvein)
  - `common/culture/pillars/eotg_pillars.txt:58,205`
  - `localization/english/eotg_cultures_l_english.yml:14-26`
  - `localization/english/eotg_heritage_l_english.yml:20-21,55-56,87-88,112`
- **Religion** (consistent with the ERRATA; also CB-12):
  - `common/religion/religion_types/eotg_religions.txt:1296-1298` ("Industrial survivalism faith of the Helix Remnants")
  - `docs/866_religions:227-233,261`
  - `localization/english/eotg_religions_l_english.yml:120-123`
- **Myr struggle** (4.1, 4.4):
  - `common/struggle/struggles/eotg_myr_struggle.txt:6,43`
  - `localization/english/eotg_myr_struggle_l_english.yml:8,14,120,133`
- **Titles** (4.1): `localization/english/eotg_titles_l_english.yml:27-34,100-102,124-126,329,333-342,372-373`.
- **Clayd arc** (4.2, 4.4):
  - `common/modifiers/eotg_modifiers.txt:691,758-774` (`eotg_helix_restoration`, `eotg_helix_ascendant`, `eotg_fortress_helix`)
  - `localization/english/eotg_bookmark_chars_l_english.yml:56-58,181-199,454,496`
  - `events/eotg_clayd_events.txt`, `events/eotg_rughan_events.txt:51`
  - `docs/bookmark-char-story:512-1334`, `docs/EOTG_Events_Characters:92-146`
- **Minor:** `docs/confluence_legacies_system_pitch.md:679` ("a Helix archive"), `docs/needed_art_terrains.txt:256`.
- **Aside:** Karim Ibn Al Daveed appears as a "Chad Orc warlord" (`866_bookmark_design.md:50`) and a "Deep-one hybrid" Shardbearer (`EOTG_Events_Characters:10-11`). Whether they are the same person is unsettled.

---

## 5. Voidwalkers: Void worshippers or wardens against it?

### 5.1 Sources
| file:line | Verbatim (trimmed) | Asserts |
|---|---|---|
| `SETTING LORE:10-16` (ERRATA Orrin) | "The Void was once Orrin's prison, but Orrin is NO LONGER imprisoned there … that influence is UNEXPLAINED … Characters attributing Void phenomena to Orrin are voicing a belief, not a confirmed fact." | — |
| `SETTING LORE:143-144` | "MALVRICK worship: Underground cults persisting despite mainstream pressure" / "Voidwalkers (Malvrick sect): Secret society forming around void worship" | **Worship.** |
| `SETTING LORE:232-235` | "Primary Sons of Yu: … MALVRICK (Lawful Evil): Darkness, Void, Secrets \| Voidwalkers (mostly destroyed), underground cults" | Malvrick is a Son of Yu. |
| `SETTING LORE:270,375,598,818` | "Voidwalker Remnants: Malvrick worship continues underground" / "Malvrick worship driven underground; Voidwalkers hunted" | — |
| `SETTING LORE:398-403` | "VOIDWALKER HUNTS & DESTRUCTION (~200-700 AG …) - Voidwalker sect hunted by Elrossi-aligned powers - Most public Voidwalker temples destroyed … - By 850 AG: Voidwalkers nearly extinct as organized group" | They had temples; the Elrossi hunted them. |
| `SETTING LORE:423-426` | "PLANAR RIFT RE-ACTIVATION (850-866 AG) - Grip-era rift sites … - Dimensional seals weakening" | **No wards are mentioned anywhere in lore.** |
| `SETTING LORE:443` | "Underground Malvrick/Voidwalker cults re-emerging" | — |
| `docs/866_bookmark_design.md:68` | "**Faith:** Elross, Malvrick, and Yu (all three …)" | Angelia openly honours Malvrick. |
| `docs/866_religions:130-135` | "UNRESOLVED TENSION — VOID REVERENCE: … Malvrick is a Son of Yu, which argues for Divine Order … stays in eotg_rf_titan_worship" | — |
| `docs/866_religions:185-191` | "eotg_religion_void_reverence … FAITH eotg_faith_void_cult — venerates the breach itself." | — |
| `common/religion/religion_types/eotg_religions.txt:928-931,961` | "# Fringe cults that venerate Carrigore and the Void" / `family = eotg_rf_titan_worship` / "HighGodName = eotg_god_malvrick" | The comment says Carrigore; the high god is Malvrick. |
| `common/religion/religion_family_types/eotg_religion_families.txt:12` | "# Divine Order — Yu and his sons: Elross, Bohemut, Malvrick…" | — |
| `localization/english/eotg_religions_l_english.yml:94-96` | "eotg_religion_void_reverence_adherent:0 \"Voidwalker\"" / "\"Voidwalkers\"" / "… His Voidwalkers were hunted across five centuries and are, officially, extinct." | **v1 names the worshippers "Voidwalkers".** |
| `localization/english/eotg_l_english.yml:63-64` | "Void Reverence" / "Cult of the Grip" | — |
| `common/scripted_triggers/eotg_void_triggers.txt:6-16` | "The Void is the prison of ORRIN THE EYE -- sealed … MALVRICK … is the god whose VOIDWALKER sect alone understood how to ward these places … That tension is the system." | **Warden.** Also states Orrin "sealed" as fact. |
| `common/scripted_triggers/eotg_void_triggers.txt:48-52,70-78` | "faith = { religion_tag = eotg_religion_void_reverence }" / "# TRUE if a surviving Voidwalker -- a Malvrick heretic -- is sheltering…" | — |
| `common/scripted_effects/eotg_void_effects.txt:94-97` vs `:146-150` | Void-revering faith: exposure **+5** / "A sheltered Voidwalker maintains the wards…": exposure **−6** | v1 contradicts itself. |
| `common/opinion_modifiers/eotg_void_opinions.txt:26-29` | "# Void Cult faithful and Voidwalker remnants read the same condition as favor." | A worship reading inside v1. |
| `common/decisions/eotg_void_decisions.txt:4-6,58-61` | "heretic ward; needs a sheltered Voidwalker" / "Malvrick's sect was hunted to near-extinction for knowing exactly this." | — |
| `common/traits/eotg_void_traits.txt:14-15` | "Voidwalker doctrine holds that Orrin cannot take what is given back." | — |
| `events/eotg_void_whispers.txt:308-313,372-382` | "A surviving Voidwalker … asks for shelter. They are the only people alive who still know the wards." / "Turn them over to the Elrossi." | — |
| `localization/english/eotg_void_l_english.yml:41,44-45,85` | "weaker than what the Voidwalkers knew" / "… hunted across five centuries for knowing precisely this" / "she is a Voidwalker … her order spent four hundred years learning to close these things … offers the only real ward you will ever be given." | **Warden.** |
| `localization/english/eotg_void_l_english.yml:94` | "Orrin the Eye is sealed and cannot act" | Stated as fact; contradicts the ERRATA. |
| `docs/system_depth_audit.md:98` | "Malvrick's hunted **Voidwalkers** supply the only real ward" | The v1 design decision. |
| v2 `.claude/agents/eotg-lore-keeper.md:13` | "Known errata already there: … Malvrick is not Carrigore." | **Not in the ERRATA block.** |

### 5.2 Contradictions
1. **Worship vs warden.**
   - Lore: void worship (`SETTING LORE:144,270,375,399`) and temples (`:401`), and never mentions wards.
   - v1: they are the only ones who know the wards (`eotg_void_triggers.txt:72`, `eotg_void_effects.txt:8`, `eotg_void_whispers.txt:311-312`, `eotg_void_l_english.yml:85`).
2. **v1 contradicts itself.** "Voidwalker" is the Void Reverence adherent name, and that faith *raises* exposure. A Voidwalker courtier *lowers* it.
3. **Malvrick's family.** Lore makes him a Son of Yu, but his religion sits in titan worship (flagged unresolved in `866_religions:130-135`).
4. **"Heretic."** v1 calls them heretics; lore says only "persecuted". Angelia openly honours Malvrick (`866_bookmark_design.md:68`).
5. **Carrigore.**
   - `eotg_religions.txt:929` says the religion venerates "Carrigore and the Void", but its high god is Malvrick.
   - The lore-keeper's "Malvrick is not Carrigore" errata does not exist in the ERRATA block.
6. **Orrin "sealed" stated as fact.** This needs fixing whatever the Voidwalker ruling:
   - `eotg_void_triggers.txt:6-7`, `eotg_void_effects.txt:5-7`, `eotg_void_decisions.txt:115`, `eotg_void_traits.txt:15`
   - `eotg_void_l_english.yml:49,94`, and the opinion modifiers "Marked/Refused by the Eye" (`:36-37`)
7. **Dates.** The hunts ran ~200–700 AG (`SETTING LORE:398`), but the loc variously says "five centuries" or "five hundred years".

### 5.3 Options, and what each would change
- **A. Lore wins: they worship; the ward is a rite of that devotion.**
  - Reframe `eotg_void_l_english.yml:4,41,44-45,85` and the script comments.
  - The adherent name and the opinion comment stay.
  - Sheltering one becomes harbouring a Void worshipper, so the cult branch and the Voidwalker courtier merge into one.
- **B. A new ERRATA makes them wardens; the Elrossi misread warding as worship.**
  - Amend `SETTING LORE:144,270,375,399-403`.
  - Rename or re-describe the Void Reverence adherents (`eotg_religions_l_english.yml:94-96`) and the opinion comment.
  - Event 0004 and the decisions stay as written.
- **C. Split the name.** The historic sect leaves two heirs: the Cult of the Grip (breach worship) and a few surviving ward-keepers.
  - Decide which group gets the "Voidwalker" adherent name; name the keepers explicitly in 0004, the ward decision and 0023.
  - The lift plan treats them as two branches.
- **D. Disputed in-world, as with Orrin.**
  - Every narrated "the only people who still know the wards" becomes attributed belief.
  - Mechanics unchanged.

The courtier-flag bug and the Orrin rewrites are needed under every option (see the Void lift plan).

### 5.4 Questions
> **Human:** At 866, are the Voidwalkers worshippers of the Void, its wardens, both, or disputed in-world?

> **Vault:** Is Malvrick's Void faith a Divine Order heresy (a Son of Yu) or a Titan-facing cult, and does Carrigore figure in it?

---

## 6. Handoff
### HANDOFF (cloud session, unvalidated)
- **branch:** `claude/canon-void-glossary-cloud`
- **status:** done (dossier only; nothing decided)
- **files:** `docs/specs/canon_decisions_cloud.md`
- **needs-human:** questions 0–5 above.
- **needs-lore:** turn each ruling into an ERRATA line in SETTING LORE.
  - Consider lifting SETTING LORE into v2 `docs/` first (audit §2 D), so the ERRATA has an editable home.
  - Fix the phantom "Malvrick is not Carrigore" erratum cited in `.claude/agents/eotg-lore-keeper.md:13`.
- **needs-vault (via intake):**
  - §4.1–4.5 (the Helix region brief);
  - §5 (Malvrick's faith);
  - §2c (the Trade Federation of Thorum);
  - any date question the human sends on.
- **taskboard (proposed):**
  - one waiting-human item per question 0–3 and 5, or one combined "Canon dossier" item;
  - CB-28 now points here;
  - add a lore-keeper task to refresh the stale SETTING LORE line numbers in `docs/qa/v1_lift_readiness_cloud.md`.
