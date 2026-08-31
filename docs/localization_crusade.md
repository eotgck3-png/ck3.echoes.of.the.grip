# Localization Crusade — Echoes of the Grip

Status as of 2026-08-29. Companion to `closed_alpha_checklist.md`.

**Goal:** a player reading any vanilla string should never be pulled out of the
setting. No peasants, no castles, no horses — the provinces are star systems.

---

## The glossary

Every future override must use these. The tier ladder was set by the mod author
on 2026-08-29 and supersedes an earlier draft.

| Vanilla | EotG | Why |
|---|---|---|
| Barony | **System** | One star system |
| County | **Region** | Several systems |
| Duchy | **Sector** | Duchies are "Xerxes Reach", "Aphionian Belt" |
| Kingdom | **Expanse** | The mod already has "The Lanius Expanse", a kingdom |
| Empire | **Cluster** | The mod's empire is literally "The Myr Cluster" |
| Castle | **Bastion** | |
| City | **Port** | |
| Temple | **Sanctum** | |
| Tribe | **Clanhold** | |
| Peasant | **Commoner** | Established by the earlier pass; 93% complete |
| Serf | **Bonded worker** | Established by the earlier pass; 100% complete |

### Why the kingdom tier is not "Realm"

"Realm" was the first choice and was rejected. Vanilla uses the word **916
times** to mean "everything a character rules, at any tier" —
`game_concept_realm_law`, `_realm_heir`, `_realm_priest`, `_realm_capital`, and
every `[realm|E]` link. A count holding no kingdom still has a Realm Capital and
Realm Law, so the word would have carried two meanings in the same tooltip.

**"Expanse" appears exactly once in all of vanilla**, making it effectively
free, and it already matches `eotg_k_lanius_expanse` ("The Lanius Expanse"),
which is a kingdom. The only overlaps are cosmetic and inside the mod's own
names: the duchy `eotg_d_coreward_expanse` ("Coreward Expanse") is a Sector, and
three terrain strings use the word. Neither competes with a UI concept.

### One open friction

**Barony titles still say "Station".** `eotg_titles_l_english.yml` names them
"Xerxes Station", "Crestfall Station" while the barony *tier* is now "System",
so the UI reads "Xerxes Station (System)". This mirrors vanilla's own
county/barony name sharing (County of York, Barony of York) so it is not wrong,
but a rename pass over the `eotg_b_*` keys would tighten it. Deliberately not
done here — it is a content decision, not a loc fix.

Non-feudal tier variants keep their vanilla *role* while losing the medieval
word: republics trade in Ports and Charters, theocracies in Sanctums and
Hierarchates, tribal/clan realms in Clanholdings.

---

## How the override layer works

Files live in `localization/english/replace/`. Two rules matter:

1. **A key may be defined only ONCE across the whole `replace/` folder.**
   If two files define it, CK3 silently keeps one and the other edit is lost.
   See the open defect below.
2. **Concept links are keys, not display text.** Renaming `game_concept_castle`
   to "Bastion" makes every `[castle|E]` link in vanilla render as "Bastion"
   automatically — across hundreds of files this mod never touches. Never
   rewrite `[castle|E]` to `[bastion|E]`; that concept does not exist and the
   link breaks silently. The same applies to `$game_concept_x$` self-references,
   which is why most vanilla descriptions needed no rewrite at all.

This is why the tier pass is only ~110 keys but changes text almost everywhere.

---

## Coverage

Measured against 167,225 vanilla English strings.

| Term | Vanilla lines | Uncovered keys | Status |
|---|---:|---:|---|
| serf | 28 | 0 | **Done** |
| peasant | 393 | 42 | **Nearly done** |
| castle | 98 | 85 | Names + concept links done; event prose outstanding |
| village | 130 | 116 | Names done; event prose outstanding |
| bishop | 141 | 138 | Outstanding |
| knight | 321 | 317 | Outstanding — but arguably setting-appropriate |
| **horse** | **433** | **413** | **All building NAMES done.** Remainder is event prose |
| tavern | 53 | 52 | Outstanding |
| candle | 41 | 41 | Outstanding |
| parchment | 24 | 24 | Outstanding |
| cathedral | 20 | 19 | Outstanding — see holy-site note below |
| chivalry | 18 | 18 | Outstanding |

**Read this table with care.** "Uncovered keys" counts every key containing the
word, so it is dominated by one-shot event descriptions and moves slowly even
when a pass lands well. The buildings pass of 2026-08-29 changed only 14 of the
427 `horse` keys — but those 14 were every stables, horse-pasture and grazing
building *name*, which is the text a player actually reads, repeatedly, in the
build menu. Judge a pass by what it puts on screen, not by this column.

### Prioritise by visibility, not by count

A game concept or holding name is read hundreds of times per campaign; an event
description is read once. The passes completed so far deliberately took the
small, high-traffic sets first — tiers, holdings, terrains, men-at-arms — which
is why ~110 keys moved more text than the previous ~1,000.

Done by that measure so far: title tiers, holdings, terrains, men-at-arms, and
(2026-08-29) **building names** — the stables, horse-pasture, hillside-grazing,
jousting, mill and market-village lines, mapped as:

| Vanilla line | EotG | Rationale |
|---|---|---|
| Stables | **Vehicle Bays** | Ground transport and couriers |
| Horse Pastures | **Skimmer Yards** | Feeds light cavalry = Strike Speeders |
| Hillside Grazing | **Belt Claims** | Hills are "Asteroid Belt Region" |
| Jousting Lists | **Trial Grounds** | Martial training, not sport |
| Windmills / Watermills | **Turbine Fields / Hydro Plants** | |
| Manor Houses | **Estate Compounds** | |
| Monasteries | **Meditation Retreats** | Matches existing "Meditation Halls" |

Also 2026-08-29, a second pass took the **short UI labels** (modifier names,
trait tracks, accolades, lifestyle focus, dynasty mottos) and the **custom-loc
word bank**. Mounts became transports and skimmers, `horse_archers` became
Strike Speeders to match the mod's own men-at-arms, Chivalry became **Valor**,
and the village modifiers became settlements.

### The custom-loc word bank is the highest-leverage file in the game

`custom_localization/regional_custom_loc_l_english.yml` is not shown anywhere on
its own. It is the bank of words CK3 splices *inline* into event prose through
customizable_localization — FortifiedBuilding, TerrainType, LocalAnimal. One key
there surfaces in dozens of unrelated events.

It also held a bug this project created: `eotg_terrains_l_english.yml` renamed
the terrain **types** shown in the UI ("Asteroid Belt Region", "Debris Cluster")
but not these inline forms, so event prose still said "hills" and "forest" right
beside a tooltip that said something else. `eotg_custom_loc_wordbank_l_english.yml`
closes it. **Keep those two files in sync** — changing one without the other
re-opens the inconsistency.

### Council positions and traits: smaller than they looked

Both were listed here as large gaps (23 and 72 keys). On inspection almost all
of it is *vanilla-religion-specific variants* — `councillor_court_chaplain_
buddhism_religion_duchy`, `trait_crusader_hellenism`, and ~100 siblings. This
mod ships its own religions, so those never resolve. The genuinely reachable
set is about six keys (`trait_crusader`, `trait_crusader_king*` fallbacks, the
generic councillor titles), and the councillor titles — Chancellor, Marshal,
Steward, Spymaster — already read fine in a sci-fi setting. Only "Court
Chaplain" is really medieval. **Treat any uncovered-key count in this document
as an upper bound until the religion/culture-variant keys are filtered out.**

### Three decisions left to the author

Flagged rather than silently changed, because they touch the mod's own
religious design rather than being vocabulary slips:

* **The pilgrimage cluster (~55 keys).** The mod ships
  `doctrine_pilgrimage_local_rites`, so pilgrimages exist in this setting and
  the word is not Earth-specific. Left whole.
* **"Crusade" / `trait_crusader` / `ghw_crusade`.** `docs/SETTING LORE`
  describes Elrossi Holy Orders as "crusading forces", so the word may be
  deliberate.
* **Bishop terms.** A faith-structure decision.

Remaining after that is event prose — large, low-visibility, best done
opportunistically.

### How to find the next tranche

The scan that produced the UI-label set, worth repeating:

```bash
# labels, not prose: short values, no \n, no [scope] refs, no #formatting
grep -E "^ [A-Za-z0-9_.]+:[0-9]+ \"[^\"]{1,60}\"$" vanilla_all.txt \
  | grep -vE "\\\\n|\[|#" \
  | grep -vE "^ (PORTRAIT_MODIFIER|HEADER_|[bcdke]_[a-z])" \
  | grep -vE "^ [A-Z][a-z]+:[0-9]+ "
```

Then match the term against the **value** with word boundaries, never the key —
otherwise "Camilla" matches `mill` and "Serfoji" matches `serf`, which is what
made the first attempt at this useless.

### Real-world references

A scan of the mod's *own* override files found survivors that the earlier
peasant→commoner pass had left in place: "viking raider" (fixed), plus
"Roman Empire" in `bookmark.1071.desc`, "old Roman infrastructure" in
`empower_sicilian_parliament_decision_desc`, and "false-pope"/"Rome" in
`iberia_north_africa.0111.desc`. Those three are tied to vanilla bookmarks,
Sicily and the Iberia struggle respectively, so they may never fire on this
mod's map — left alone deliberately rather than forgotten.

The vanilla holy-site buildings (Canterbury, Cologne, Lund, Uppsala, Santiago,
Hagia Sophia) are the same case: real-world names, but bound to vanilla map
provinces. Revisit once the map pass settles which holy sites exist.

---

## Open defect — duplicate keys in `replace/`

**166 keys are defined in more than one file. For 44 of them the two files
disagree, so one edit is silently discarded.** The folder grew by vanilla
source file rather than by subject, so `eotg_travel_events` and
`eotg_travel_misc_commoner` both legitimately wanted the same strings — one did
the peasant→commoner pass, the other did a different substitution on the same
line, and only one survives.

The remaining 122 duplicates are byte-identical and therefore harmless.

Nothing here is caused by the tier pass — those files are clean.

**The 44 conflicting keys:**

    councillor_spouse_stewardship.1011.desc.serfs :: eotg_stewardship_events_l_english.yml eotg_stewardship_serf_misc_l_english.yml 
    court.7300.a :: eotg_court_relation_events_l_english.yml eotg_peasant_commoner_misc_l_english.yml 
    ep1_flavor.0021.desc :: eotg_bp_ep_mpo_dlc_commoner_l_english.yml eotg_ep1_ep3_laamp_misc_l_english.yml 
    ep3_laamp_decision_event.1040.desc_outro_physician :: eotg_ep1_ep3_laamp_misc_l_english.yml eotg_ep3_dlc_commoner_l_english.yml 
    epidemic_events.1060.desc.mid.faith :: eotg_ce1_epidemics_legends_commoner_l_english.yml eotg_epidemic_events_l_english.yml 
    fp3_decision.0003.desc_recently :: eotg_fp1_fp2_fp3_events_l_english.yml eotg_fp_dlc_commoner_l_english.yml 
    health.1003.desc :: eotg_health_events_l_english.yml eotg_lifestyle_health_commoner_l_english.yml 
    health.safe_treatment.6.desc :: eotg_health_events_l_english.yml eotg_sermon_prayer_buildings_l_english.yml 
    hold_court.1021.desc :: eotg_activity_events_l_english.yml eotg_feast_hunt_hold_court_l_english.yml 
    hold_court.5010.desc :: eotg_activity_events_l_english.yml eotg_feast_hunt_hold_court_l_english.yml 
    internal_affairs.50.desc :: eotg_peasant_commoner_misc_l_english.yml eotg_travel_events_l_english.yml 
    journey_events.50.b.tt :: eotg_lifestyle_health_commoner_l_english.yml eotg_stewardship_serf_misc_l_english.yml eotg_travel_events_l_english.yml 
    journey_pauper_king_modifier_desc :: eotg_lifestyle_health_commoner_l_english.yml eotg_stewardship_serf_misc_l_english.yml eotg_travel_events_l_english.yml 
    legend_peasant_emperor_desc :: eotg_ce1_epidemics_legends_commoner_l_english.yml eotg_tgp_ep3_legends_l_english.yml 
    lifestyle_nicknames.1000.desc_good :: eotg_lifestyle_health_commoner_l_english.yml eotg_peasant_commoner_misc_l_english.yml 
    marshal_task.1001.desc :: eotg_peasant_commoner_misc_l_english.yml eotg_stewardship_events_l_english.yml 
    mpo_events_tova.0003.desc :: eotg_activities_dlc_events_l_english.yml eotg_bp_ep_mpo_dlc_commoner_l_english.yml 
    physician_epidemic_events.1024.desc :: eotg_ce1_epidemics_legends_commoner_l_english.yml eotg_physician_humors_misc_l_english.yml 
    playdate_joined_beating_log :: eotg_peasant_commoner_misc_l_english.yml eotg_tour_pilgrimage_playdate_l_english.yml 
    religious_interaction.2401.desc_lost :: eotg_court_relation_events_l_english.yml eotg_physician_humors_misc_l_english.yml 
    roaming_battlefield_prayer_key :: eotg_activities_dlc_events_l_english.yml eotg_prayer_buildings_l_english.yml 
    roaming_intro_terrain_snippet_farmlands :: eotg_activities_contracts_commoner_l_english.yml eotg_activities_dlc_events_l_english.yml 
    stewardship_domain_special.1002.desc.blaming :: eotg_stewardship_events_l_english.yml eotg_travel_misc_commoner_l_english.yml 
    stewardship_domain_special.1319.desc :: eotg_stewardship_events_l_english.yml eotg_travel_misc_commoner_l_english.yml 
    stewardship_domain_special.1320.desc :: eotg_stewardship_events_l_english.yml eotg_travel_misc_commoner_l_english.yml 
    stewardship_domain_special.1413.desc :: eotg_stewardship_events_l_english.yml eotg_travel_misc_commoner_l_english.yml 
    stewardship_domain_special.8012.b :: eotg_burgher_corvee_concepts_l_english.yml eotg_stewardship_events_l_english.yml 
    stewardship_duty.1071.a :: eotg_stewardship_events_l_english.yml eotg_stewardship_serf_misc_l_english.yml 
    stewardship_duty.1071.b :: eotg_stewardship_events_l_english.yml eotg_stewardship_serf_misc_l_english.yml 
    stewardship_duty.1071.c :: eotg_stewardship_events_l_english.yml eotg_stewardship_serf_misc_l_english.yml 
    stewardship_duty.1071.desc :: eotg_stewardship_events_l_english.yml eotg_stewardship_serf_misc_l_english.yml 
    stewardship_duty.1072.a :: eotg_stewardship_events_l_english.yml eotg_stewardship_serf_misc_l_english.yml 
    stewardship_duty.1072.desc.relationship :: eotg_stewardship_events_l_english.yml eotg_stewardship_serf_misc_l_english.yml 
    stewardship_duty.1072.desc.rival :: eotg_stewardship_events_l_english.yml eotg_stewardship_serf_misc_l_english.yml 
    stewardship_duty.1072.desc.vassal :: eotg_stewardship_events_l_english.yml eotg_stewardship_serf_misc_l_english.yml 
    stewardship_duty_special.1205.desc :: eotg_lifestyle_health_commoner_l_english.yml eotg_stewardship_events_l_english.yml 
    strategy_fed_peasants_larders_modifier :: eotg_lifestyle_health_commoner_l_english.yml eotg_lifestyle_misc_events_l_english.yml 
    stress_threshold.1711.desc.ambitious :: eotg_burgher_corvee_concepts_l_english.yml eotg_stress_events_l_english.yml 
    stress_threshold.1711.desc.zealous :: eotg_burgher_corvee_concepts_l_english.yml eotg_stress_events_l_english.yml 
    tour_travel.1001.title :: eotg_sin_sermon_serf_misc_l_english.yml eotg_tour_pilgrimage_playdate_l_english.yml 
    travel.bad_cermon :: eotg_sermon_prayer_buildings_l_english.yml eotg_travel_events_l_english.yml 
    travel_events.4038.desc :: eotg_sermon_prayer_buildings_l_english.yml eotg_travel_events_l_english.yml 
    travel_events_bp3.15.c :: eotg_bp_ep_mpo_dlc_commoner_l_english.yml eotg_physician_humors_misc_l_english.yml 
    tribal.1303.c :: eotg_court_relation_events_l_english.yml eotg_peasant_commoner_misc_l_english.yml 

**Suggested fix:** for each pair, merge both substitutions into one string and
delete the other definition, leaving a pointer comment where it was removed —
the pattern used in `eotg_game_concepts_wars_commoner_l_english.yml` for
`game_concept_county_control_desc`. Re-run the check after any edit:

```bash
cd localization/english/replace
grep -hoE "^ [A-Za-z0-9_.]+:" *.yml | sed 's/^ //;s/:$//' | sort | uniq -d
```
