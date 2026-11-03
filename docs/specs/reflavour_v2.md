# Spec: the vanilla-UI reflavour layer, v2 port

**Author:** cloud session (localizer role), 2026-11-03. **Status:** built (cloud, **unvalidated**: no game, Tiger or PX). Next: eotg-localizer review, then a local session diffs every ported key against vanilla 1.20.1.1 (§6), then eotg-qa and eotg-lore-keeper.
**Sources:** v1's layer, `OLD PROJECT VERSION/localization/english/replace/` (54 files, 1,170 distinct keys); the glossary, `docs/specs/glossary_proposal_cloud.md` with its **2026-10-20 owner ruling (County = Shoal)**; v2's shipped `localization/english/replace/eotg_county_term_l_english.yml`.
**Tool:** `docs/tools/reflavour_port.py` re-runs the port (dry run by default; `--write` regenerates the files). **Appendix:** `docs/specs/reflavour_v2_held_keys.md` lists every held key with its reason.

---

## 1. Purpose

The mod is a space setting, but vanilla's interface still says Barony, County, Castle and Peasant. v1 built a reflavour layer of vanilla-key overrides. This pass ports the **interface-term part** of it to v2 with the current glossary, under the rules in the brief:
- one definition per key across `localization/`, `replace/` included;
- port, don't invent;
- canon voice;
- one BOM per file.

## 2. The term table (applied)

| Vanilla | Mod term | Source |
|---|---|---|
| Barony | **System** | glossary §0 |
| County | **Shoal** (plural Shoals, "a Shoal") | owner ruling 2026-10-20. Keys owned by `eotg_county_term_l_english.yml` |
| Duchy | **Sector** | glossary §0 |
| Kingdom | **Expanse** | glossary §0 |
| Empire | **Cluster** | glossary §0 |
| Castle | **Bastion** | glossary §0 |
| City | **Port** | glossary §0 |
| Temple | **Sanctum** | glossary §0 |
| Tribe | **Clanhold** | glossary §0 |
| Peasant | **commoner** | glossary §0 (v1 already applied it) |
| Serf | **bonded worker** | glossary §0 (v1 already applied it) |
| Burgher | Contractor | applied by v1; glossary §5.1 proposes adding the row (not ruled) |
| Chivalry | Valour | applied by v1 (Canadianized here); glossary §5.2 (not ruled) |

**Kept vanilla, by the glossary's proposals (not ruled):** court, courtier, vassal, liege, household, gold, the ruler ranks (Count, Duke…), knight (never hard-coded; see §3.4), and **Realm**.

## 3. What was done

### 3.1 Ported: 461 keys in 37 files

Files are `localization/english/replace/eotg_reflavour_<area>_l_english.yml`, one per v1 source area. `<area>` is the v1 file's name without `eotg_` and `_l_english`. The v1 files were already grouped by vanilla source area, but their exact vanilla origin can't be checked here (no vanilla loc). Each file carries the header line `# UNVERIFIED-VANILLA: keys ported from v1 (CK3 1.19); the local session diffs them against 1.20.1.1`.

The largest: holdings and concepts (63 keys: the tier and holding concept names, castle, city and temple building lines), county/hunt/tour modifiers (50), the setting's building renames (39), title tiers (35; System, Sector, Expanse, Cluster and their government variants), the mount UI (29: transports and skimmers), buildings (25), GUI, factions and memories (22).

### 3.2 Changes to v1's text
1. **County/Region → Shoal**, applied outside `[...]`, `$...$` and `#fmt` tokens. v1 wrote "Region" for the county tier, and some prose still said "county". 23 values changed, including all of glossary §4's lines that survived the filters.
2. **Canadian English:** 36 lines (favour, colour, defence, centre, travelling, labour, rumours, vigour, Valour…).
3. **House style** (eotg_lint L013):
   - em and en dashes become a comma (or a colon in short names);
   - single-quoted speech and scare quotes become unescaped `"..."`;
   - one escaped `\"` is unescaped;
   - trailing spaces are removed.
4. **Formatting tokens are untouched.** `[Concept|E]`, `[x.GetName]`, `$KEY$`, `#S … #!`, `\n` and `[Glossary(...)]` are masked before every substitution.
5. **Three pronoun allowlist entries** in `docs/tools/eotg_lint_pronoun_allowlist.txt`. Each "they/them" refers to plural commoners, not the named scope.

### 3.3 Held: 709 keys (appendix lists each)

| Reason | Keys | Why |
|---|---|---|
| **Event prose** | 469 | Vanilla 1.19 event text (keys with an event id, e.g. `yearly.8100.desc`) where v1 changed only "peasant" to "commoner". (a) The rest of each text is medieval and Earth-set (horses, villages, Sicily, Shiva, the Roman Empire). (b) An event-text override pins 1.19 wording and its data functions, and **a scope that 1.20 renamed or removed would render as a loc error**: higher risk than a concept name. (c) It is the least visible reflavour per key. Recommendation: a later localizer pass on events the mod's players will actually see, after a vanilla diff (§6). |
| **Blocked file: terrains** | 21 | Terrain names wait on the tier-vs-terrain ruling (glossary §3.2, §6.1 items 5–7). v1's names carry tier words ("Asteroid Belt Region", "Debris Cluster"). |
| **Blocked file: custom-loc wordbank** | 25 | Must change in sync with the terrain names (glossary §3.2). |
| **Blocked file: traditions** | 78 | Blocked until the terrain ruling. It also uses "Void" for ordinary space, which collides with the canon Void (glossary §5.4). |
| **Blocked key: `horse_archers`, `horse_archers_lowercase`** | 2 | "Strike Speeders" collides with the mod's own `eotg_maa_strike_speeders` (glossary §5.6; proposed rename "Skimmer Gunners", not ruled). The other mount-UI keys are ported. |
| **Conflicting duplicates in v1** | 44 | v1 defined the same key differently in two files. Choosing between them is a localizer merge (glossary §6.2 step 0). Identical duplicates (122) were collapsed into one copy and ported. |
| **Medieval or Earth word** | 40 | A term key whose value still says knight, archers, crops, harvest, forest, gods, temple, Roman, Persian, Mongol, Meteora… "No medieval words in replaced text". Fix the text, then port. |
| **Removed in local validation** | 16 | Stale against 1.20.1.1 (2), event prose that escaped the event-id filter (4), and no-ops equal to vanilla (10). Listed in the appendix and in `BLOCKED_KEYS`. |
| **Already defined in v2** | 14 | The county concept and tier keys, owned by `eotg_county_term_l_english.yml`. |

The filter is a word list (`MEDIEVAL`, now including "city", and `EARTH` in `docs/tools/reflavour_port.py`). It errs towards holding, and it has at least one false positive: "dungeon" matched `dung…`.

### 3.4 Rules checked (static, cloud)
- **One definition per key:** no key is defined twice anywhere under `localization/` (script check over every `*.yml`).
- **One BOM** at byte 0 of every `replace/` file.
- **No `[scope:`; no "Gob-Corp"; no literal "knight"** in a ported value. Values that said knight were held. Vanilla's own `$…$` passthroughs (the knight culture term) are left as vanilla wrote them.
- **eotg_lint:** 0 new findings against the baseline (L003 format, L010 references, L013 style, L016 BOM).

## 4. Known gaps in what was ported
- **Multi-species voice** (glossary principle 6): the local pass removed "human" from the ported values ("human life" and "other humans" are now neutral). The localizer should still sweep for "man/men".
- **Residual Earth-feudal flavour that passed the word filter:** "the crown", tournaments and "the Devaraja" (vanilla mechanic names), "Lords and Ladies"-style phrasing in held keys. These are tolerable as vanilla mechanic names. The localizer can tighten them.
- **Ruler ranks** still read medieval ("Count of X (Shoal)"), by the glossary's keep-for-now proposal.

## 5. Open questions (for the owner and lore-keeper)
1. **Holding-type names.** v1's set is used: Bastion, Port, Sanctum, Clanhold, Sanctum Bastion (temple citadel), plus government variants (Free Port, Great Sanctum, Chapter Post, Berth…). Confirm them, especially "Sanctum Bastion".
2. **CB-56, building names.** v1's setting building renames are ported (`eotg_reflavour_buildings_setting_l_english.yml`, 39 keys). Confirm them against CB-56 before the real map lands.
3. **"Realm" stays vanilla.** v1 rejected a rename for the same reason as the tier-word rule (`localization_crusade.md:31-35`). Confirm.
4. **Glossary rows not yet ruled but already in the ported text:** Burgher → Contractor, Chivalry → Valour (glossary §6.1 item 10).
5. **Terrain names, "Void", and "Strike Speeders"** (glossary §6.1 items 5–7, 11, 12) unblock 126 held keys.
6. **Event prose:** port a curated set later, or leave vanilla? (§3.3; recommendation: curated, after the vanilla diff.)
7. **Gold:** still "Gold" (glossary §6.1 item 3).

## 6. Local validation steps
1. **Diff against 1.20.1.1.** For each ported key, find the vanilla key. Flag any key that no longer exists (dead override), and any whose vanilla text changed meaning or gained or lost a `[...]` / `$...$` token since 1.19. Fix or drop it. This is the `UNVERIFIED-VANILLA` line in each file header.
2. **Override check.** `replace/` overrides by key whatever the filename (glossary principle 8, `UNVERIFIED-VANILLA`). The shipped county-term file is the precedent; confirm one ported key in game (e.g. the Bastion holding concept).
3. **The usual set:** Tiger, the PX LSP (BOM and loc format), `python docs/tools/eotg_lint.py --baseline docs/tools/eotg_lint_baseline.json`.
4. **In game:**
   - the holding and tier concept tooltips read Bastion, Port, Sanctum, System, Shoal, Sector, Expanse, Cluster;
   - a hunt or tour county modifier reads "this Shoal";
   - the transport and skimmer travel modifiers;
   - no `(BUG:` or raw key text in a ported string.
