# Questions for the vault — Myr Clusters

Written by eotg-intake on 2026-10-05 from the first read of this folder. The exporter's QUESTIONS.md was empty, so nothing is merged or repeated. Build order: `docs/specs/regions/myr_clusters.md`.

**Ranking:** owner instruction (2026-10-05): Gate 1 first. Questions that block titles, provinces, history or the bookmark come first. Culture and religion questions come last, because those briefs are deferred.

**A note for the exporter.** Every Sources line in this batch names a repo file (`OLD PROJECT VERSION/...`, `docs/lore/...`), not a vault note. The questions below therefore cite those Sources lines. Where the vault says something different from the v1 file, the vault wins. Please re-export with the vault note paths.

## Gate 1 blockers

### Whole batch
- Q-X1. All briefs > Sources (Sources: OLD PROJECT VERSION/*, docs/lore/*): were these briefs written from the Obsidian vault, or from the v1 repo files they cite? If the vault has notes for the Myr Clusters, please re-export with vault paths in the Sources lines.
- Q-X2. REGION.md, HANDOFF.md (Sources: none; the files are 0 bytes): REGION.md is empty. Please export it. It is the first thing every builder needs.

### REGION.md (empty)
- Q-G1. REGION.md > Map footprint (Sources: none): where do the Myr Clusters sit on the galaxy map, and which regions or nations border them? Canon says the Trade League, New Cauldron, the Coldiron Caliphate and the Second Elrossi Imperium border them (docs/lore/Third era Events.md:383-390).
- Q-G2. REGION.md > Map footprint (Sources: none): what terrain is each kingdom or duchy (systems / worlds / stations, and which CK3 terrain each maps to)? Which provinces are chokepoints or impassable?
- Q-G3. REGION.md > Map footprint (Sources: none): the title briefs give 287 baronies in 80 counties, 24 duchies and 6 kingdoms. Is that the intended province count? How are the six kingdoms laid out relative to each other?
- Q-G4. REGION.md > Build priorities / Constraints and don'ts (Sources: none): what does the lore owner want playable first, and what must builders not change?

### Map ids (for the human, not the vault)
- Q-H1. titles_*.md > Tree "Province ID" (Sources: OLD PROJECT VERSION/docs/title_hierarchy.md): ids 1–287 are v1 `definition.csv` ids. Will the new `map_data/definition.csv` keep these ids in this order, or will a mapping be supplied?

### Title briefs
- Q-T1. titles_*.md > Tree (Sources: OLD PROJECT VERSION/docs/title_hierarchy.md): every barony's holding type reads "city/castle/temple". Which one is each barony? At minimum, which is each county capital?
- Q-T2. titles_*.md > Holders at 866 (Sources: OLD PROJECT VERSION/docs/title_hierarchy.md; docs/lore/REVIEW_866.md:22-35): every duchy and county holder is "Provincial Lord / Council" or "Local Magistrate / Captain". Who holds each duchy and county at 866? If the kingdom holder holds them directly, please say so. In five of the six briefs the table also stops after three duchies and nine counties: Myr Core, Cauldron Marches, Lanius Expanse, Charter Principalities and Outer Marches.
- Q-T3. titles_cauldron_marches.md > Top title / Holders at 866 (Sources: OLD PROJECT VERSION/docs/title_hierarchy.md): the holder is given as "President Marlen / Senator Lireth Davan". Which one holds k_eotg_cauldron_marches? What does the other hold?
- Q-T4. (missing brief) e_eotg_myr_cluster (Sources: de jure liege line in all six titles briefs): there is no title brief for the empire. What are its name, adjective and colour? Does anyone hold it at 866, or is it vacant on purpose?
- Q-T5. titles_myr_core.md > Duchy Helix Remnant; titles_cauldron_marches.md > Duchy Helix Fringe (Sources: OLD PROJECT VERSION/docs/title_hierarchy.md): ERRATA HELIX says Helix holds three counties in different duchies. Which three counties does Clayd Kestrel-Vire hold, and under which duchies?
- Q-T6. ruler_corven_vultarre.md > Bookmark lead (Sources: OLD PROJECT VERSION/docs/Bookmark-Characters): Corven is a bookmark lead commanding the 7th Mercenary Legion, but no title brief gives him a title. What does he, or the Legion, hold at 866?
- Q-T7. ruler_rughan_broad_jaw.md > Bookmark lead (Sources: OLD PROJECT VERSION/docs/Bookmark-Characters): Rughan is a bookmark lead with no title in any titles brief. What does he hold at 866?
- Q-T8. titles_charter_principalities.md, titles_outer_marches.md > Top title (Sources: OLD PROJECT VERSION/docs/title_hierarchy.md): the adjectives "Charter Commercial Zone" and "The Warrens & Outer Frontier" read as descriptions. What adjective does the vault use? Is "Charter Principalities" the Gob-Ogre Trade League's name for its Myr holdings?
- Q-T9. titles_cauldron_marches.md > Tree, County "Mikey IV" (Sources: OLD PROJECT VERSION/docs/title_hierarchy.md): is "Mikey IV" the intended in-game name? Please confirm the spelling of "Dûmholt" too.
- Q-T10. titles_*.md > Holders at 866, "since 850 AG" (Sources: docs/lore/Third era Events.md:383-510): every title's holder date is 850. Is that the vault's date for each? In particular, Skrit Grimweave's house is founded in 851 (dynasty_grimweave.md) and the Warrens revolution runs 860–915.
- Q-T11. titles_*.md > Holders at 866 (Sources: OLD PROJECT VERSION/history/characters/eotg_characters_866.txt): are the Caliph, the President of New Cauldron and the Trade League chair holding these Myr kingdoms, or their home realms with the Myr kingdoms beneath them? Are the home realms on this map?

### Ruler briefs
- Q-R1. ruler_*.md (all 19) > Personality and capability (Sources: OLD PROJECT VERSION/docs/Bookmark-Characters): each brief says traits are "defined in mod history files" and lists none. What personality and other traits does the vault give? Bookmark-Characters lists three personality traits plus extras for each. Are those canon?
- Q-R2. ruler_*.md (all 19) > Family / Life so far / At 866 (Sources: OLD PROJECT VERSION/docs/Bookmark-Characters; bookmark-char-story): these sections are the same boilerplate in all 19. What does the vault give for parents, spouses (with years), children and dated events? Specifically, are Qadir and Samir Marzuk's sons, as his pitch ("fractious sons") implies?
- Q-R3. ruler_marlen.md, ruler_ilyr_kavos.md, ruler_serapion_vale.md, ruler_dorian_valek.md, ruler_mirelle_voss.md, ruler_nibrak_coilmint.md > Dynasty (Sources: OLD PROJECT VERSION/history/characters/eotg_characters_866.txt): each is assigned to a house whose surname they do not carry and whose dynasty brief does not list them (Davan, Solvaerath, Sylvaerath, Vultarre, Kestrel-Vire, Gildspanner). What house is each in? v1 had Marlen in a "Cauldron Council" house.
- Q-R4. ruler_marlen.md > Education (Sources: OLD PROJECT VERSION/history/characters/eotg_characters_866.txt): education is "Unknown". Does the vault give one?

### Bookmark
- Q-B1. (no brief) Bookmark name (Sources: OLD PROJECT VERSION/docs/866_bookmark_design.md:1): is the 866 bookmark called "After the Crucible"?

## Deferred by owner (cultures and religions): answer after the above

### Culture briefs (all 28)
- Q-C1. culture_*.md > Identity, Heritage group (Sources: OLD PROJECT VERSION/common/culture/cultures/eotg_cultures.txt): every culture is "Human", including the elves (Aelvaryn, Thalassyr), goblins (Geldmark, Gnashvok, Kelmori), ogres (Drogmari, Thrakani) and ratfolk (Skarrin, Veskari). What heritage and language does each have?
- Q-C2. culture_*.md > Character (same Sources): all 28 read "Stoic / Equal / Adaptive survival". What ethos, martial custom and three to five practices does the vault give each?
- Q-C3. culture_*.md > Naming (same Sources): male and female name lists are "Unknown" for all 28. Does the vault have name lists?
- Q-C4. culture_*.md > Identity, Where it lives (same Sources): all 28 say "Myr Clusters". Where is each concentrated, and in what share? 15 of them (Brackwateri, Brokari, Caldryx, Duskvein, Gnashvok, Halrethi, Kelmori, Noctivar, Orovane, Sternstahl, Tangentine, Thalassyr, Thrakani, Vanthari, Zeladani) are used by no ruler.

### Religion briefs
- Q-F1. religion_*.md > Faiths, Holy sites (Sources: OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt): 18 holy-site counties are not in any title tree (aphiona, brokers_deep, coldiron, dead_reach, far_drift, forge_reach, gildhall, helix_prime, new_cauldron, new_xerxes, old_xerxes, rust_verge, saint_argoths_hold, the_first_vault, the_great_anvil, vanguard, warren_core, yashuun). Which existing county is each, or should it be added to a tree?
- Q-F2. religion_firstlight.md, religion_civic_secular.md, religion_deep_warren.md, religion_forge_tradition.md, religion_plutocracy.md, religion_survivalism.md, setting/religion_elross.md > Faiths, Where it is dominant (same Sources): these lines give rulers roles that contradict their ruler briefs. Examples: Lyssa Varayne as a Myr Core princess, Clayd as a Cauldron consul, Skrit as a Forge baron, and Corven, Serapion and Ilyr as Elrossi officers. Which is right?
- Q-F3. ruler_caelorin_solvaerath.md, ruler_ilyr_kavos.md, ruler_serapion_vale.md > Faith (Sources: OLD PROJECT VERSION/docs/Bookmark-Characters, `firstlight_placeholder`): canon makes the Prince of Myr's Caer Myr a beacon of Elrossi faith. Are these three Firstlight or Orthodox Elrossi?
- Q-F4. ruler_corven_vultarre.md, ruler_dorian_valek.md, ruler_lyssa_varayne.md > Faith (Sources: as Q-F3): the link points to Secular Codes, which has two faiths. Is each Contract-Sworn or Civic Secular?
- Q-F5. religion_civic_secular.md vs setting/religion_secular_codes.md > Civic Secular (same Sources): the faith is described twice, with different holy orders and dominance. Which one is canonical?
- Q-F6. religion_firstlight.md > Head of faith (same Sources): "Position vacant or held by the venerable high lamptender". Which is it at 866, and who?
