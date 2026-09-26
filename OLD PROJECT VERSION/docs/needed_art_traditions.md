# Tradition Art — Needed Icons

All reflavoured traditions reuse vanilla layer 0 (background) and layer 1 (pattern) where they still
make thematic sense. Only layer 4 (the item icon) needs replacement in most cases.

All new icons should be created as `.dds` files at the vanilla size (64×64 px, DXT5 compression).
They go in `gfx/interface/icons/culture_tradition/4-items/`.

A tradition's layers are overridden by adding a new tradition file that references the same ID —
or, simpler, by placing an icon with the same filename that the tradition already uses. Where a
new filename is specified below, a GUI override will also be needed.

---

## TERRAIN / ENVIRONMENTAL

---

### Voidfarers
**Vanilla:** `tradition_seafaring` — `ship.dds` (martial / western)
**Reflavouring:** Seafarers → void-lane navigators. The mechanical identity is identical (long-range mobility, naval bonuses) but the setting is deep space, not ocean.
**New icon:** A stylised void-lane ship — elongated hull, no sails, thruster glow. Distinct from a sailing vessel silhouette.
**Keep layers:** martial background (warfare-adjacent culture), western pattern (fits most cultures using this).

---

### Voidlane Commerce
**Vanilla:** `tradition_maritime_mercantilism` — `ship.dds` (diplo / mediterranean)
**Reflavouring:** Maritime trade empire → corridor-based interstellar commerce. Trade flows through protected transit lanes and relay nexuses rather than sea ports.
**New icon:** A transit node or relay beacon — a geometric hub with radiating lines suggesting routes. Not a ship.
**Keep layers:** diplo background (commerce/negotiation), mediterranean pattern acceptable.

---

### Debris Field Navigators
**Vanilla:** `tradition_forest_fighters` — `forest.dds` (martial / western)
**Reflavouring:** Forest ambush warfare → combat manoeuvring through dense wreck fields and orbital graveyards. Mechanically the same (broken-terrain fighting bonus), visually completely wrong.
**New icon:** A fractured debris field — angular shattered hull fragments arranged like a dense obstacle field, with a small craft implied threading through.
**Keep layers:** martial background fits.

---

### Dense Drift Adapted
**Vanilla:** `tradition_jungle_dwellers` — `jungle.dds` (steward / indian)
**Reflavouring:** Jungle habitat adaptation → life in unstable drift regions and cluttered transit sectors. The mechanical flavour (hazardous environment survival) remains.
**New icon:** A chaotic drift zone — overlapping asteroid/debris shapes with a structure half-obscured, suggesting environmental confusion and adaptation.
**Suggest changing:** layer 1 from `indian` to a default pattern — nothing about this culture is Indian-coded.

---

### Belt Settlers
**Vanilla:** `tradition_hill_dwellers` — `desert_mountains.dds` (steward / indian)
**Reflavouring:** Hill/highland homesteaders → generations raised in asteroid belts and fractured resource fields. Mechanically: terrain resilience.
**New icon:** A cluster of asteroids — irregular rock shapes, with a small habitat structure visible on one. Suggests permanent settlement in a belt.
**Suggest changing:** layer 1 from `indian` to `western` or `default1`.

---

### Fortified Sector Dwellers
**Vanilla:** `tradition_mountain_homes` — `mountain.dds` (steward / mena)
**Reflavouring:** Mountain fortress homes → hardened sector habitats, defensive installations built into difficult terrain. Siege-endurance culture.
**New icon:** A reinforced station cross-section — a thick-walled cylindrical habitat with blast shields, suggesting defensive permanence.
**Keep layers:** steward background (infrastructure focus), mena pattern acceptable.

---

### Sparse Zone Survivors
**Vanilla:** `tradition_dryland_dwellers` — `desert.dds` (steward / mena)
**Reflavouring:** Dryland subsistence → survival in resource-poor dead sectors with little infrastructure support. Same mechanical theme (scarcity hardiness).
**New icon:** An empty void sector — minimal, barren. A single small structure against a dead-star silhouette, or an empty orbit diagram.
**Keep layers:** steward background (resource management), mena acceptable.

---

### Cryozone Veterans
**Vanilla:** `tradition_winter_warriors` — `fight.dds` (learning / western)
**Reflavouring:** Winter campaign warriors → soldiers and civilians hardened by failing thermal infrastructure, frozen frontier systems, dead-reactor sectors.
**New icon:** A cryo-sealed figure or cryo pod — armoured silhouette in ice or thermal isolation gear. Alternatively: a cracked thermal seal symbol.
**Suggest changing:** layer 0 from `learning` to `martial` — this is a hardship-endurance warrior tradition, not scholarly.

---

### Expanse Raiders
**Vanilla:** `tradition_warriors_of_the_dry` — `desert.dds` (martial / mena)
**Reflavouring:** Desert raiders → mobile strike forces operating across the Longlane Expanse and sparse frontier zones where supply lines fail.
**New icon:** A fast raider silhouette — stripped-down attack craft or a mounted strike-force emblem. Speed and aggression over mass.
**Keep layers:** martial background, mena pattern could stay or shift to `default1`.

---

### Void Trawlers
**Vanilla:** `tradition_fishermen` — `ship.dds` (steward / mediterranean)
**Reflavouring:** Artisan fishermen → precision salvage crews and debris harvesters who developed extraordinary coordination extracting resources from dangerous void regions.
**New icon:** A salvage arm or trawl net extended toward debris — mechanical grabber claw, or a ship with nets deployed into a debris field.
**Keep layers:** steward background (production/resource), mediterranean acceptable.

---

## ECONOMIC

---

### Systems Engineers
**Vanilla:** `tradition_artisans` — `artisan.dds` (steward / mena)
**Reflavouring:** Craft artisans → technical specialists and systems maintainers. Cultural identity built around keeping complex infrastructure functional.
**New icon:** A circuit schematic or gear-and-wrench — technical tooling rather than craft tools. Could be a stylised system diagram.
**Keep layers:** steward background fits economic/maintenance focus.

---

### Alloy Forgers
**Vanilla:** `tradition_metal_craftsmanship` — `tools.dds` (steward / mediterranean)
**Reflavouring:** Metalworkers → industrial fabricators and structural metallurgists. The vanilla `tools.dds` is generic enough to be plausible, but a dedicated icon is better.
**New icon:** An alloy ingot or forge press — industrial metalworking rather than craft tools. Heavy, blocky shapes.
**Keep layers:** steward background, mediterranean acceptable.

---

### Industrial Discipline
**Vanilla:** `tradition_hard_working` — `tools.dds` (diplo / indian)
**Reflavouring:** Industrious labourers → a culture that treats productive discipline as civilisational survival doctrine. More systemic than individual craft.
**New icon:** A factory floor symbol or output meter — suggests organised production rather than individual tools. Could be a gear array or assembly line.
**Suggest changing:** layer 1 from `indian` to `default1` or `western`.

---

### Resource Reclaimers
**Vanilla:** `tradition_frugal_armorsmiths` — `shield.dds` (steward / western)
**Reflavouring:** Frugal armour production → salvage-first culture. Nothing wasted; reclaimed materials and recovered tech repurposed for survival.
**New icon:** A recycling/reclaim symbol — broken components being reassembled, or a salvage claw grasping debris. Not a shield.
**Keep layers:** steward background (resource focus) fits.

---

### Transit Enclaves
**Vanilla:** `tradition_caravaneers` — `camel.dds` (diplo / mena)
**Reflavouring:** Desert caravan culture → protected transit hub networks, secure relay stations providing refuge and commerce. The camel icon is unusable.
**New icon:** A transit hub or docking station — geometric space station silhouette with docking arms, or a relay beacon with surrounding ships.
**Keep layers:** diplo background (trade/connection) fits.

---

### Hydroponic Foundations
**Vanilla:** `tradition_agrarian` — `farmland.dds` (steward / indian)
**Reflavouring:** Agricultural society → enclosed food production systems treated as a sacred civilisational responsibility. Not open farmland.
**New icon:** A hydroponic tower or growth tube array — vertical, enclosed, lit from within. Clearly not open-field farming.
**Suggest changing:** layer 1 from `indian` to `default1` or `western`.

---

### Nutrient Syndicates
**Vanilla:** `tradition_pastoralists` — `horses.dds` (steward / mena)
**Reflavouring:** Mobile herding culture → mobile agricultural convoys and nutrient-production operations that move between sectors. The horse icon is unusable.
**New icon:** A mobile processing unit or food convoy — a vessel with agricultural processing equipment, or canisters of nutrient stock.
**Keep layers:** steward background fits.

---

## SOCIAL / GOVERNANCE

---

### Codified Governance
**Vanilla:** `tradition_legalistic` — `quill.dds` (learning / mediterranean)
**Reflavouring:** Medieval legalism → data-codified law systems, procedural continuity across political upheaval. The quill reads as too archaic.
**New icon:** A data tablet or legal terminal — a flat screen or scrolling code display rather than parchment and quill.
**Keep layers:** learning background (knowledge/law focus) fits.

---

### Civic Directorate
**Vanilla:** `tradition_republican_legacy` — `laurel.dds` (steward / mediterranean)
**Reflavouring:** Roman republican legacy → post-collapse civic institutions, public administration, collective governance. The laurel wreath is too Roman-specific.
**New icon:** A directorate seal or civic emblem — abstract institutional symbol, perhaps a stylised assembly hall or administrative crest.
**Keep layers:** steward background (administration) fits.

---

### Communal Infrastructure
**Vanilla:** `tradition_collective_lands` — `farmland.dds` (learning / indian)
**Reflavouring:** Shared farmland → shared maintenance obligations for collective infrastructure. Not agriculture — engineering and upkeep.
**New icon:** Interconnected nodes or a public works symbol — a network of connected structures, or cooperative maintenance imagery.
**Suggest changing:** layer 1 from `indian` to `western` or `default1`.

---

### Merit Ascension
**Vanilla:** `tradition_talent_acquisition` — `greeting.dds` (diplo / mena)
**Reflavouring:** Recognising talent through greeting/patronage → meritocratic advancement systems where competence determines leadership. The greeting icon is weak.
**New icon:** An ascending rank insignia or merit badge — a tiered symbol or upward arrow combined with an administrative mark.
**Keep layers:** diplo background (social/political) acceptable.

---

### Chamber Custodians
**Vanilla:** `tradition_court_eunuchs` — `ceremony.dds` (intrigue / mediterranean)
**Reflavouring:** Court eunuchs → isolated administrative castes who safeguard institutional continuity by separating governance from dynastic ambition.
**New icon:** A vault key or institutional seal — a formal key symbol or sealed chamber emblem. Suggests gatekeeping and custodial authority.
**Keep layers:** intrigue background (hidden influence) fits well.

---

### Oath Networks
**Vanilla:** `tradition_fp2_ritualised_friendship` — `ritualised_friendship.dds` (diplo / western)
**Reflavouring:** Ritualised friendship bonds → formal oath networks structuring political alliances and personal loyalty across vast distances.
**New icon:** An oath clasp or network web — two hands clasped over a radiating connection pattern, or a web of interconnected oath-seals.
**Keep layers:** diplo background fits, western acceptable.

---

### Sector Isolationism
**Vanilla:** `tradition_parochialism` — `city.dds` (intrigue / mediterranean)
**Reflavouring:** Parochial city loyalty → deliberate sector-level isolation, local community loyalty over broader political unity. The city icon reads too medieval.
**New icon:** A closed sector gate or isolation field — a region behind a barrier, or a sector boundary with a hard edge suggesting deliberate closure.
**Keep layers:** intrigue background (inward-looking) fits well.

---

## SPIRITUAL / IDEOLOGICAL

---

### Lineage Reverence
**Vanilla:** `tradition_hereditary_hierarchy` — `king.dds` (diplo / western)
**Reflavouring:** Hereditary political hierarchy → reverence for ancestral deeds as the foundation of political authority and cultural identity. Less about kings, more about lineage memory.
**New icon:** A lineage chain or family tree — abstract branching structure, or a chain of connected generational marks.
**Keep layers:** diplo background (authority/social), western acceptable.

---

### Archive Reverence
**Vanilla:** `tradition_mystical_ancestors` — `philosopher.dds` (learning / mediterranean)
**Reflavouring:** Mystical ancestor spirits → reverence for preserved records, ancestral archives, and historical memory treated as near-sacred objects.
**New icon:** A data archive terminal or memory crystal — a glowing repository, stacked data cores, or a crystalline record structure. Not a philosopher.
**Keep layers:** learning background (knowledge focus) fits perfectly.

---

### Doctrinal Adherents
**Vanilla:** `tradition_zealous_people` — `speech.dds` (learning / mediterranean)
**Reflavouring:** Religious zealotry → ideological unity and doctrinal adherence as collective survival mechanism. Broader than religion — applies to secular ideologies too.
**New icon:** A doctrine codex or ideological emblem — a sealed book or symbolic crest representing an unwavering ideology. More austere than a speech podium.
**Keep layers:** learning background (belief/knowledge) fits.

---

### Sanctified Wardens
**Vanilla:** `tradition_warrior_monks` — `temple.dds` (martial / indian)
**Reflavouring:** Warrior monks → military guardians for whom duty and ideology are inseparable. Sacred wardens of people and doctrine.
**New icon:** A guardian seal or sacred weapon — a stylised warden crest, or a weapon overlaid with a doctrinal symbol. Not a temple.
**Suggest changing:** layer 1 from `indian` to `western` or `default1` for non-Indian cultures using this.

---

## MARTIAL

---

### Bulkhead Defenders
**Vanilla:** `tradition_stalwart_defenders` — `shield.dds` (intrigue / mediterranean)
**Reflavouring:** Stalwart shield-wall defenders → defensive warfare in fortified corridors and hardened installations. A shield is close but reads too medieval.
**New icon:** A reinforced blast door or bulkhead cross-section — thick parallel lines suggesting layered armour or a corridor defence. Distinct from a round shield.
**Keep layers:** intrigue background (defensive/reactive posture) fits.

---

### Bastion Keepers
**Vanilla:** `tradition_castle_keepers` — `city.dds` (martial / western)
**Reflavouring:** Castle-keeping → maintenance of massive defensive strongholds and fortified transit sectors. The city icon is generic and weak for this.
**New icon:** An orbital fortress or hardened station — a heavy geometric structure with weapon emplacements, clearly defensive and permanent.
**Keep layers:** martial background fits.

---

### Through Force Alone
**Vanilla:** `tradition_by_the_sword` — `swords.dds` (learning / mena)
**Reflavouring:** Sword-legitimacy → political authority earned and maintained through strength and the willingness to impose order by force.
**New icon:** A heavy weapon or force sigil — a single large weapon (not crossed swords), or an emblem combining a fist and a political crown. Raw dominance over martial elegance.
**Suggest changing:** layer 0 from `learning` to `martial` — this is a warrior-legitimacy tradition, not a scholarly one.

---

### Rapid Assault Corps
**Vanilla:** `tradition_horse_lords` — `horses.dds` (martial / mena)
**Reflavouring:** Cavalry nomads → fast-strike military formations specialising in rapid assault across vast operational distances. The horse icon is unusable.
**New icon:** A strike craft silhouette or rapid deployment emblem — a fast-moving formation marker, or a single sleek attack vessel.
**Keep layers:** martial background fits.

---

### Siege Behemoths
**Vanilla:** `tradition_lords_of_the_elephant` — `elephant.dds` (learning / indian)
**Reflavouring:** War elephants → massive assault platforms and heavily armoured breakthrough formations. Prestige through overwhelming force.
**New icon:** A siege walker or assault platform — a large, heavily armoured vehicle or bipedal siege machine. Massive, slow, intimidating.
**Suggest changing:** layer 1 from `indian` to `western` or `default1`.

---

### Raid Fleets
**Vanilla:** `tradition_practiced_pirates` — `battle.dds` (intrigue / mediterranean)
**Reflavouring:** Sea pirates → organised void raiding operations, salvage strikes, and aggressive assault as an accepted method of wealth acquisition.
**New icon:** A raider fleet formation — multiple small vessels in attack formation, or a single raider with weapons deployed.
**Keep layers:** intrigue background (opportunistic/criminal edge) fits well.

---

## ADDITIONAL

---

### Archive Tradition
**Vanilla:** `tradition_philosopher_culture` — `philosopher.dds` (learning / indian)
**Reflavouring:** Philosophical inquiry culture → preservation of knowledge and historical continuity as a civilisational defence mechanism.
**New icon:** An archive terminal or data crystal cluster — a glowing knowledge repository, distinct from the `philosopher.dds` sitting figure.
**Suggest changing:** layer 1 from `indian` to `western` or `default1`.

---

### Survivor Lineages
**Vanilla:** `tradition_reverence_for_veterans` — `knight.dds` (martial / mediterranean)
**Reflavouring:** Veteran knights honoured in retirement → survivors of catastrophe honoured as living proof of what civilisation costs to maintain.
**New icon:** A survivor's mark or memorial seal — a scarred emblem, a cracked but intact shield, or a figure bearing visible hardship insignia.
**Keep layers:** martial background acceptable, mediterranean can stay.

---

### Port Sanctuary Codes
**Vanilla:** `tradition_esteemed_hospitality` — `greeting.dds` (diplo / mena)
**Reflavouring:** Generous hospitality culture → formalised docking customs and transit codes ensuring shelter for travellers crossing dangerous regions.
**New icon:** A docking clamp or port beacon — a mechanical docking arm, or a beacon light over a station entrance. Hospitality expressed through infrastructure, not greeting.
**Keep layers:** diplo background fits.

---

### Salvage Pursuers
**Vanilla:** `tradition_hunters` — `hunter.dds` (intrigue / mediterranean)
**Reflavouring:** Game hunters → pursuit teams tracking fugitives, drifting wreckage, and hidden resource caches across unstable sectors.
**New icon:** A pursuit craft or salvage hook — a fast-moving vessel with a tow hook extended, or a targeting reticule over debris.
**Keep layers:** intrigue background (tracking/pursuit) fits well.

---

### Stationbreaker Doctrine
**Vanilla:** `tradition_hit_and_run` — `soldiers4.dds` (martial / mediterranean)
**Reflavouring:** Hit-and-run cavalry tactics → specialised disruption doctrine targeting logistics networks, navigation routes, and operational stability.
**New icon:** A disruption burst or EMP symbol — a radiating interference pattern, or a weapon striking a station's systems node.
**Keep layers:** martial background fits.
