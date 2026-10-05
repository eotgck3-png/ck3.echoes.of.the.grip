# Build order — Myr Clusters
Source briefs: intake/regions/myr_clusters/ (74 files, read 2026-10-05) + intake/setting/religion_{commerce,elross,secular_codes,void_reverence}.md
Intake state: every brief is **new and uncommitted** (`git status`: untracked). No builder has consumed any input yet, so nothing below is marked "changed since consumed".

**Scope ruling (owner, relayed by the orchestrator, 2026-10-05):** Gate 1 only. The aim is a world that loads, with placeholder history for everything. Cultures and religions use **vanilla placeholders**, and every such line carries `# STOPGAP: replace from briefs`. The 28 culture and 11 religion briefs are **deferred**: their completeness is recorded below, but nothing is scheduled from them.

---

## 0. Read this before building anything

1. **REGION.md is empty (0 bytes).** So are HANDOFF.md and the exporter's QUESTIONS.md. That means there is no map footprint (no position, neighbours, terrain, chokepoints or cluster shape), no polity list, no build priorities and no constraints from the lore owner. The order below takes its priorities from `intake/README.md` §"What a builder needs most" and from the Gate 1 DoD in `docs/agent_workflow.md` instead.
2. **No brief cites a vault note.** Every Sources line points at repo files: `OLD PROJECT VERSION/docs/title_hierarchy.md`, `OLD PROJECT VERSION/docs/Bookmark-Characters`, `OLD PROJECT VERSION/history/characters/eotg_characters_866.txt`, v1 `common/` and loc, and `docs/lore/*`. The briefs are re-exports of v1 material, not of the Obsidian vault. `Bookmark-Characters` line 5 calls its cultures and religions "temporary placeholders", and the briefs inherit that. Treat any fact that came only from v1 as provisional.
3. **Province ids 1–287 in the title briefs are v1 ids.** They were keyed against v1's `definition.csv` (`title_hierarchy.md` line 3: "definition.csv v288 entries (IDs 0–287)"). v2 has no `map_data/definition.csv` (only `seasons.txt`). Do not write `province =` until the human's map lands and either keeps these ids or supplies a mapping (see Q-H1).
4. **Mod governments do not exist in v2** (there is no `common/governments/`). The briefs name `eotg_government_{cauldron_republic, trade_council, caliphate, feudal, elven_monarchy, ratfolk_revolutionary}`. These are Gate 2. For Gate 1, use a vanilla government on each title, marked `# STOPGAP`, and record the brief's intended government in a comment beside it.
5. **Nikios Khanate:** none of the 74 briefs mentions it. Nothing to defer.

---

## Ready to build (Gate 1)

Ordered as Gate 1 needs it. "Ready" means the briefs settle enough to author the item now. Items that also need province ids can be **drafted** now but not **landed** until the map exists (Blocked B1).

### 1. Title tree, Myr Clusters (landed_titles), draft → eotg-cartographer
- **Read:** `titles_myr_core.md`, `titles_cauldron_marches.md`, `titles_coldiron_marches.md`, `titles_lanius_expanse.md`, `titles_charter_principalities.md`, `titles_outer_marches.md`; `OLD PROJECT VERSION/docs/title_hierarchy.md` for the capital-chain convention (the first barony of a county is its capital; the first county of a duchy is the duchy capital).
- **Counts:** 1 empire, 6 kingdoms, 24 duchies, 80 counties, 287 baronies. Every county names a capital barony. No duplicate barony keys and no duplicate province ids.
- **Identifiers to create (tier-first):**
  - `e_eotg_myr_cluster`. Its capital is the Xerxes chain, per `title_hierarchy.md`. Its name, adjective and colour are missing (B4).
  - `k_eotg_myr_core` (5 duchies / 18 counties / 70 baronies)
  - `k_eotg_cauldron_marches` (4 / 13 / 47)
  - `k_eotg_coldiron_marches` (3 / 9 / 33)
  - `k_eotg_lanius_expanse` (3 / 11 / 41)
  - `k_eotg_charter_principalities` (3 / 11 / 41)
  - `k_eotg_outer_marches` (6 / 18 / 55)
  - `d_eotg_*` / `c_eotg_*` / `b_eotg_*`: key them from the names in each brief's Tree. The barony keys are given bare (`bastion_halreth`), so prefix them `b_eotg_`. The Notes line "`_eotg_`" is a typo for `b_eotg_`.
- **Builder judgement to record in comments:**
  - Duchy and county colours: the briefs give kingdom colours only, in words.
  - Strip the stray backticks from county names (e.g. "Bastion Halreth `").
- **Cannot land without:** `province =` on all 287 baronies (B1).
- **Lore flags:** C-T1 (Helix), C-T2 (Iron Pact).

### 2. Dynasties (common/dynasties) → eotg-cartographer
- **Read:** `dynasty_*.md` (11).
- **Create:** dynasties for Al-Khadrin, Broad-Jaw, Davan, Gildspanner, Grimweave, Kestrel-Vire, Solvaerath, Sylvaerath, Varayne, the Vessel Collective and Vultarre (keys `eotg_dynasty_*`). Mottos are given for all 11.
- **Culture field:** omit it, or point it at the vanilla placeholder with `# STOPGAP`. Do not create the brief cultures.
- **Not settled:** "Standing at 866" (boilerplate in all 11), cadet houses ("None" in all 11). Neither blocks loading.

### 3. Kingdom holders and bookmark leads (history/characters) → eotg-cartographer
- **Read:** the `ruler_*.md` below, plus their `dynasty_*.md`.
- **Usable fields:** name, short name, sex, birth date, dynasty and the education line ("`diplomacy_4` — Grey Eminence" and so on).
- **Culture and faith:** vanilla placeholder `# STOPGAP`. Keep the brief's culture and faith name in a comment so the later swap is mechanical.
- **Personality traits are NOT in the briefs.** Every brief says "defined in mod history files". Leave them out until Q-R1 is answered. Do not lift them from `Bookmark-Characters` on your own authority (see Q-R1).
- **Ready (5):** Vaelorin Sylvaerath (b. 724.3.1), Caelorin Solvaerath (829.3.1), Caliph Marzuk Al-Khadrin (799.1.10), Grezzik Gildspanner (809.2.5), Skrit Grimweave (831.6.1). Each holds a kingdom in a title brief and is a bookmark lead.
- Character keys `eotg_char_*`, per the existing v1 scheme, or as `docs/specs/history_syntax.md` decides.

### 4. Kingdom title history (history/titles) → eotg-cartographer
- **Read:** the "Holders at 866" table in each titles brief.
- **Ready (5):**
  - `k_eotg_myr_core` → Vaelorin
  - `k_eotg_coldiron_marches` → Marzuk
  - `k_eotg_lanius_expanse` → Caelorin
  - `k_eotg_charter_principalities` → Grezzik
  - `k_eotg_outer_marches` → Skrit
- **Holding date:** the briefs give "since 850 AG" for every title. Use it, but see C-T3 (Skrit, Grimweave).
- **Government:** vanilla `# STOPGAP`, with the brief's mod government in a comment.
- **Duchies and counties:** every duchy and county holder in the briefs is a placeholder ("Provincial Lord / Council", "Local Magistrate / Captain"). Placeholder-history stopgap, pending Q-T2: the kingdom holder holds every duchy and county in that kingdom. Mark each line `# STOPGAP: holder unknown (Q-T2)`. Do **not** invent named placeholder characters.
- **Empire:** leave `e_eotg_myr_cluster` unheld. The briefs name no holder; see Q-T4.

### 5. Province history (history/provinces), draft → eotg-cartographer
- **Read:** the title briefs' Tree sections.
- **What to write:** 287 land provinces, each with a vanilla placeholder culture and faith (`# STOPGAP`) and a holding. Every barony's holding type reads "city/castle/temple", i.e. unanswered. Stopgap: castle on each county capital, city on the rest, every line `# STOPGAP: holding unknown (Q-T1)`.
- **Cannot land without:** province ids (B1).

### 6. Bookmark (common/bookmarks), partial → eotg-cartographer
- **Read:** the "Bookmark lead?" line in each ruler brief.
- **Leads:** the briefs name 9, matching the target of 9: Vaelorin, Clayd, Corven, Lireth, Grezzik, Rughan, Marzuk, Caelorin, Skrit. Five are landed and ready (item 3). Build the bookmark with those five and add the other four when B3 clears.
- **Card pitches:** the "Bookmark lead?" lines; the localizer authors them.
- **Bookmark name:** "After the Crucible" (`866_bookmark_design.md` line 1/22). No brief states it, so confirm it (Q-B1).

### 7. Supporting characters (history/characters), after items 3–6 → eotg-cartographer
- **Characters (10):** Qadir and Samir Al-Khadrin, Mother-Vessel Threelatch, Lyssa Varayne, Ilyr Kavos, Serapion Vale, Dorian Valek, Mirelle Voss, Nibrak Coilmint and President Marlen. None holds a title in the briefs, and Gate 1 does not need any of them.
- **Build them as courtiers** (same stopgap rules as item 3), with these exceptions:
  - Leave parent links out until Q-R2 answers them. Marzuk's pitch mentions "fractious sons", but no Family section names any child.
  - Six of them have dynasty assignments the dynasty briefs do not confirm (C-R3). Build those six lowborn until Q-R3 settles it: Ilyr Kavos, Serapion Vale, Dorian Valek, Mirelle Voss, Nibrak Coilmint, Marlen. Mark each `# STOPGAP`.

---

## Blocked

| # | Item | Blocked on |
|---|---|---|
| B1 | `province =` on 287 baronies; landing items 1 and 5; anything Tiger checks against `definition.csv` | Human-supplied `map_data/` (only `seasons.txt` exists in v2). Q-H1: does the new `definition.csv` keep v1 ids 1–287 in `title_hierarchy.md` order, or will a mapping be supplied? |
| B2 | Holder of `k_eotg_cauldron_marches` | The brief names **two** holders, "President Marlen / Senator Lireth Davan" (`titles_cauldron_marches.md` Top title + Holders). Q-T3. |
| B3 | Bookmark leads Clayd Kestrel-Vire, Corven Vultarre, Rughan Broad-Jaw and Lireth Davan: their titles, title history and bookmark slots | No title brief gives any of them a title. Clayd: ERRATA HELIX says the remnant holds three counties in different duchies, but none is named (Q-T5, C-T1). Corven: the 7th Mercenary Legion has no title (Q-T6). Rughan: no title (Q-T7). Lireth: see B2. Their characters can be authored now (item 3 rules) as unlanded, but the bookmark cannot feature them. |
| B4 | Name, adjective, colour and holder of `e_eotg_myr_cluster` | There is no title brief for the empire. All six kingdom briefs cite it as de jure liege. Q-T4. |
| B5 | Region map shape: neighbours, terrain per province, chokepoints, adjacencies, `geographical_regions` | REGION.md is empty. Q-G1–Q-G3. The cartographer can only draw against counts (287 provinces / 80 counties / 24 duchies / 6 kingdoms, contiguous id ranges per kingdom). |
| B6 | Real holders of all 24 duchies and 80 counties | Every holder row is a placeholder, and 5 of the 6 holder tables stop after 3 duchies / 9 counties. Q-T2. Stopgap in item 4. |
| B7 | Holding type of all 287 baronies | "city/castle/temple" everywhere. Q-T1. Stopgap in item 5. |

### Deferred by the owner (not scheduled; completeness recorded)

**Cultures (28: aelvaryn, brackwateri, brokari, caldryx, cauldrani, drogmari, duskvein, geldmark, gnashvok, halrethi, istrovan, kelmori, khadrashi, noctivar, nyssari, orovane, skarrin, solvari, sternstahl, tangentine, thalassyr, thrakani, uvreki, vanthari, veltrani, veskari, virens, zeladani)**
- All headings are present. Apart from the name and the "Descended from" line, all 28 are the same template:
  - Ethos "Stoic", martial customs "Equal" and a single practice ("Adaptive survival").
  - Heritage "Human" and language "Regional" for every one, including the elves (Aelvaryn, Thalassyr), goblins (Geldmark, Gnashvok, Kelmori), ogres (Drogmari, Thrakani) and ratfolk (Skarrin, Veskari).
  - Name lists "Unknown".
  - Look `western_clothing_gfx`.
  - Sources: v1 `eotg_cultures.txt` and loc only.
- 13 of them are used by a ruler: Aelvaryn, Cauldrani, Drogmari, Geldmark, Istrovan, Khadrashi, Nyssari, Skarrin, Solvari, Uvreki, Veltrani, Veskari, Virens. The other 15 are named by no ruler, title or region brief.

**Religions (7 region + 4 setting: civic_secular, coldiron, deep_warren, firstlight, forge_tradition, plutocracy, survivalism; commerce, elross, secular_codes, void_reverence)**
- All headings are present and the content is substantive: doctrines, vocabulary and three tenets per faith. Each is lifted from v1 `eotg_religions.txt` and loc. It fits the 1.20 split, with families `eotg_rf_{divine_order, pragmatic, ancestral, titan_worship}` → `religion_types/` (`religion_details`) → `faith_types/` (`faith_details`, list tenets).
- Defects to settle before they are scheduled:
  - 18 holy-site county keys are not in any title tree: `aphiona, brokers_deep, coldiron, dead_reach, far_drift, forge_reach, gildhall, helix_prime, new_cauldron, new_xerxes, old_xerxes, rust_verge, saint_argoths_hold, the_first_vault, the_great_anvil, vanguard, warren_core, yashuun`. Of these, dead_reach, far_drift and rust_verge are duchies.
  - The "Where it is dominant" lines name rulers in roles their ruler briefs contradict (C-F1).
  - Civic Secular is defined twice, in `secular_codes.md` and `religion_civic_secular.md`, with different holy orders and dominance text.
  - Ruler faith links point at religions, not faiths. Corven, Dorian and Lyssa link Secular Codes, which has two faiths.
- When they are scheduled, vanilla-scout should confirm the tenet and doctrine keys exist in 1.20, especially `tenet_sacred_destruction`, `tenet_monasticism`, `doctrine_consanguinity_dynastic` and `doctrine_monasticism_encouraged`.

---

## Loc surface (Gate 1 only) → eotg-localizer, after items 1–6
- **Titles:**
  - 1 empire (name, adjective missing).
  - 6 kingdoms with adjectives: Myrian Core, Cauldron Marcher, Coldiron Caliphate, Lanius Principality, Charter Commercial Zone, "The Warrens & Outer Frontier". The last two read as descriptions, not adjectives; see Q-T8.
  - 24 duchies and 80 counties, names only.
  - 287 baronies, **keys only**. Display names must be derived from the keys (`the_wend` → "The Wend"). Record that as builder judgement.
  - The diacritic county Dûmholt (ASCII `dumholt`).
  - County "Mikey IV" (Q-T9).
- **Characters:** the 19 ruler names and short names. Some carry office prefixes in the full name: "President", "Senator", "Caliph", "Grand Warden", "Arch-Prelate", "Mother-Vessel".
- **Dynasties:** 11 names and 11 mottos.
- **Bookmark:** the bookmark name, plus 9 epithets and pitches (e.g. "The Tide-Crowned", "The Last Shotcaller", "The Contract Marshal", "The Civic Firewall", "The Profit-Taker", "The Builder", "The Keeper of the Ice Mandate", "The Prince of Myr", "The Fractured Architect").
- **Deferred with their briefs:** culture names and adjectives, faith and religion names and adjectives, god vocabulary.
- Canadian English throughout.

## Canon flags → eotg-lore-keeper
Precedence: ERRATA > dated docs/lore entries ≤866 > `866_bookmark_design.md` > SETTING LORE body. The briefs' own Sources are listed for each.

**Titles (Gate 1-relevant)**
- **C-T1 Helix footprint.** ERRATA HELIX (2026-10-04) says Helix holds **three counties in different duchies**, not one contiguous block. `titles_myr_core.md` has a whole **duchy** "Helix Remnant" (Helixfall, Fracturepoint, Remnant Core, all in one duchy), and `titles_cauldron_marches.md` adds a duchy "Helix Fringe" (County Helix). Neither has Helix as holder. (Sources: title_hierarchy.md, v1 landed_titles.) Also, REVIEW_866 item 5 says Clayd stays silent "until the Helix region brief". Rule whether `ruler_clayd_kestrel_vire.md` counts as that brief.
- **C-T2 Iron Pact.** `titles_charter_principalities.md` has County "Iron Pact" (barony `iron_pact_depot`). The Iron Pact forms in **950** (EV, "Iron Pact and Consolidation (950–1130)"). Is it an anachronistic name at 866? (Sources: title_hierarchy.md.)
- **C-T3 Outer Marches holder date.** Skrit holds `k_eotg_outer_marches` "since 850 AG". `dynasty_grimweave.md` founds the house in 851, and EV dates the Warrens revolution **860–915**. (Sources: title_hierarchy.md; EV 383-510.)
- **C-T4 Who holds the Myr kingdoms.** EV says four powers **border** the Clusters (Trade League, New Cauldron, Coldiron Caliphate, Second Elrossi Imperium). The briefs make the heads of those powers (the Caliph, the President of New Cauldron, the Trade League chair) holders of kingdoms **inside** `e_eotg_myr_cluster`. v1 history instead gave them their home realms (`eotg_e_coldiron_caliphate`, `eotg_k_cauldron`, `eotg_e_gob_ogre_league`; `eotg_characters_866.txt` lines 37-118, commented out). `866_bookmark_design.md` puts New Cauldron on the Titanworld.
- **C-T5 Trade League.** "Charter Principalities" appears in no canon source. Canon names the Gob-Ogre Trade League (Fifty Trade Princes). REVIEW_866 also has the League **under Karim's attack from 851**, which supersedes the bookmark design's "peak confidence".
- **C-T6 Xerxes.** `k_eotg_myr_core` is capitalled on County Xerxes, held by Vaelorin. That is consistent with ERRATA XERXES. But the still-open REVIEW_866 question (old drowned Xerxes vs New Xerxes, founded 851 by Corbin David) is untouched, and New Xerxes appears only as a religion holy site (`c_eotg_new_xerxes`, "Dome 2"), not in the tree.

**Rulers and dynasties (Gate 1-relevant)**
- **C-R1 Prince of Myr's faith.** Canon: Caer Myr "became a beacon of Elrossi faith" (EV), the Elrossi holy sites include Caer Myr (`866_bookmark_design.md`), and the Prince rallied "crusading Holy Orders". `ruler_caelorin_solvaerath.md`, `ruler_ilyr_kavos.md` and `ruler_serapion_vale.md` all give **Firstlight**. `religion_elross.md` has Serapion and Ilyr as Elrossi officers. (Sources: Bookmark-Characters, `firstlight_placeholder`.)
- **C-R2 Era wording.** `dynasty_davan.md` says "First Era democratic founders of The Cauldron". `religion_firstlight.md` says "First Dawnkeepers of the First Era". By the REVIEW_866 eras ruling, the First Era is the Titans' war, before the Grip. New Cauldron was founded in 131 AG by Mikey the Great (`866_bookmark_design.md`).
- **C-R3 Dynasty membership.** These ruler briefs put people into houses whose member lists omit them and whose surnames they do not carry:
  - Marlen → Davan. v1 had `eotg_dynasty_cauldron_council` (`eotg_characters_866.txt` l.67).
  - Ilyr Kavos → Solvaerath
  - Serapion Vale → Sylvaerath
  - Dorian Valek → Vultarre
  - Mirelle Voss → Kestrel-Vire (she leads the opposition to Clayd, the head of that house)
  - Nibrak Coilmint → Gildspanner
- **C-R4 Cauldron founding.** `religion_civic_secular.md` and `setting/religion_secular_codes.md` say "First Consul Vane Kestrel (c. 150 AG)" established the charter. Canon has Mikey the Great founding New Cauldron, with its first election, in 131 AG.

**Religions (deferred, recorded for the lore-keeper now)**
- **C-F1 Characters in roles their briefs contradict** ("Where it is dominant" / Head lines):
  - Firstlight: "Princess Lyssa Varayne", "Baroness Lireth Davan"
  - Civic Secular: "Consul Clayd", "Praetor Mirelle Voss"
  - Deep Warren: Marlen
  - Forge: "Baron Skrit Grimweave"
  - Plutocracy: "Consul Nibrak"
  - Elross: "Arch-Legate Corven Vultarre" (the ruler brief makes him Secular Codes, 7th Legion), "Tribune Ilyr Kavos"
  - Survivalism: Dorian as an Outer Marches warlord
  - Firstlight says "no holy orders active", but Ilyr Kavos leads "the Starward Wardens holy order" under Firstlight.
- **C-F2 Yu.** `religion_elross.md` says Yu "lies sealed in the Dream". ERRATA YU (2026-10-04) says he is no longer sealed.
- **C-F3 Gods acting since 850.** Three briefs have gods acting openly since 850:
  - `religion_elross.md`: Elross "acting openly across the stars"
  - `religion_coldiron.md`: Frozt "answering their prayers directly"
  - `religion_civic_secular.md`: "public denial of divine existence has become impossible"

  REVIEW_866: gods were "left in stasis by Zer'kaath in 850".
- **C-F4 Malvrick and the Voidwalkers.** `setting/religion_void_reverence.md` makes Malvrick the dark god of the Void and makes Voidwalkers his worshippers. REVIEW_866 says Malvrick is the Malvrick Confederated Orders (a Divine Order fit), and the Voidwalkers are its warrior order, not worshippers. ERRATA YU has Yu blessing Malvrick's orders. Firstlight, Coldiron and Elross also list Malvrick as an evil god.
- **C-F5 The Rift.** `religion_void_reverence.md` holy site: "the fabric of reality tore in 0 AG". REVIEW_866: the Rift is a separate plane, ruptured by Zer'kaath in **850** and closed by the Shardbearers.
- **C-F6 Elrossi chronology.** `religion_elross.md` founder: "Emperor Cassian I (c. 80 AG)", and Saint Argoth "in the 4th century". REVIEW_866 dates the Second Imperium from 500 and makes Ferdinand IV Emperor at 851.
- **C-F7 Exodus date.** `religion_survivalism.md` says "1st-century survivor-crews of the Titan Exodus flotillas". The Exodus begins in 131 AG (REVIEW_866).
- **C-F8 LAW AT 866.** Three passages describe authority above the polity:
  - Contract-Sworn holy site: "multi-cluster mercenary charters are registered and arbitrated"
  - Plutocracy: Gildhall "where all inter-cluster exchange rates are fixed"
  - Commerce: "universal galactic credit standard"

  ERRATA LAW AT 866 says no such authority exists.
- **C-F9 New Xerxes "Dome 2" quarter.** It appears as a holy site in Commerce and Plutocracy, and may describe a post-866 state (New Xerxes bazaars date from 870).

## Questions for the vault
See intake/regions/myr_clusters/QUESTIONS.md. The exporter's own QUESTIONS.md was empty, so nothing was merged or deduplicated.
