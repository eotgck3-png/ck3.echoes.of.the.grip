# Terrain scheme (2026-09-25)

The canonical mapping of CK3's land terrains to EotG galactic terrain. **Supersedes**
`OLD PROJECT VERSION/docs/needed_art_terrains.txt` and the v1 localisation
`eotg_terrains_l_english.yml`.

## The change from v1

v1 named terrains after **civilisation**: Debris Cluster (orbital wreckage), Fortified Sector
(military installations), Core Trade Corridor (stations and traffic), Stable Relay Nexus.

This scheme names them after **astrography** — the natural character of the region — and explicitly
decouples terrain from development:

- *Fertile Reach*: "High natural potential, not high existing development."
- *Frontier Reach*: "Remote and peripheral, without assuming who's living there."
- *Sanctuary Systems*: "regardless of whether they are occupied or developed."
- *Arid Reach*: "Arid environmental conditions without implying low development."

Consequence for art: terrain textures are built from **star density, nebula density, debris and
phenomena** — never from stations, ships, wreckage or city lights. Those belong to holdings and map
objects.

## The 15 land terrains

| CK3 terrain | EotG name | Core idea | Land % |
|---|---|---|---|
| plains | **Open Cluster** | The galactic equivalent of ordinary plains — accessible, few hazards | 24.5% |
| hills | **Broken Cluster** | Fragmented, irregular space | 6.2% |
| desert | **Barren Reach** | Sparse and inhospitable, not necessarily primitive | 4.3% |
| mountains | **Nebula Barrier** | Difficult space that creates strategic chokepoints | 3.9% |
| taiga | **Frozen Cluster** | Cold, hostile space with substantial potential | 3.6% |
| drylands | **Arid Reach** | Arid conditions without implying low development | 3.2% |
| forest | **Dense Cluster** | Lots of systems packed together | 2.6% |
| steppe | **Frontier Reach** | Remote and peripheral, without assuming who lives there | 2.6% |
| jungle | **Nebula Wilds** | Dense, mysterious, dangerous stellar wilderness | 1.6% |
| desert_mountains | **Barren Barrier** | Sparse, hostile frontier that also functions as a barrier | 1.0% |
| wetlands | **Anomaly Fields** | Unpredictable astronomical hazards | 0.9% |
| farmlands | **Fertile Reach** | High natural potential, not high existing development | 0.4% |
| floodplains | **Volatile Cluster** | High potential accompanied by instability | 0.4% |
| oasis | **Sanctuary Systems** | A naturally favourable pocket within otherwise difficult space | 0.3% |
| terraced_hills | **Layered Cluster** | Layered geography giving defensive advantage without being a true barrier | 0.2% |

Land percentages are measured from the vanilla map; the mod's own map will differ, but the shape —
a few dominant terrains and a long tail — will hold. They drive the variant allocation in
`docs/terrain_materials.md`.

## Full descriptions

**Open Cluster** — The most navigable and geographically straightforward regions of space. Systems
are relatively accessible from one another, with few major stellar hazards or navigational
obstacles. Can contain anything from untouched worlds to sprawling civilizations.

**Fertile Reach** — Regions containing an unusually high concentration of naturally habitable
worlds, valuable resources, or otherwise favorable systems. Desirable targets for colonization,
though a Fertile Reach need not actually be developed.

**Broken Cluster** — Scattered systems, difficult routes, stellar debris, and irregular navigation.
Travel is possible but less straightforward than through an Open Cluster.

**Nebula Barrier** — Dominated by dense nebulae, severe gravitational phenomena, radiation, or other
astronomical obstacles. Routes are constrained and predictable approaches become natural defensive
boundaries.

**Barren Reach** — Sparse regions with few habitable or easily exploitable systems. Long distances
between viable destinations, but isolated settlements and valuable installations can still exist.

**Barren Barrier** — The harshest combination of sparse resources and difficult navigation. Natural
barriers between more accessible areas of the galaxy.

**Dense Cluster** — Systems packed relatively closely together, a high density of navigable
destinations. Complexity makes travel and military operations more involved, but provides many
opportunities for habitation, industry, and strategic positioning.

**Frozen Cluster** — Extremely cold environments, icy worlds, frozen bodies. Resources and viable
settlements may still exist, but operating here requires adaptation.

**Nebula Wilds** — Vast regions enveloped in dense nebulae and unpredictable stellar phenomena.
Navigation is difficult, communications unreliable, and isolated systems can remain hidden.

**Anomaly Fields** — Unusually high concentrations of gravitational anomalies, radiation phenomena,
unstable stellar objects, or other unexplained disturbances. Conditions vary considerably from
system to system.

**Frontier Reach** — Open regions beyond the more established routes and centers of galactic
activity. May contain newly accessible systems, isolated populations, old settlements, or completely
unclaimed space.

**Volatile Cluster** — Stellar or environmental conditions fluctuate significantly. Systems may be
exceptionally productive while simultaneously presenting unusual dangers.

**Sanctuary Systems** — Small pockets of unusually favorable space surrounded by more difficult or
inhospitable regions. Reliable places for habitation, resupply, or strategic refuge.

**Arid Reach** — Low moisture, sparse naturally habitable environments, limited biological
resources. May contain valuable minerals, isolated habitable worlds, or extensive settlements, but
sustaining life relies more on imported resources or artificial infrastructure.

**Layered Cluster** — Systems distributed across pronounced variations in stellar geography, orbital
environments, and navigational elevation. Routes follow constrained corridors and interconnected
pockets, creating naturally defensible but still highly traversable territory.

## Outstanding work this creates

- **Localisation is stale.** `OLD PROJECT VERSION/localization/english/replace/eotg_terrains_l_english.yml`
  carries the v1 names (Open Transit Expanse, Debris Cluster, Fortified Sector…) and covers only 14
  terrains. It needs rewriting to these 15 names, including the `combat_*` keys
  ("Defending in …"). Gate 4, `eotg-localizer`.
- **Terrain icons and battle backgrounds** described in the v1 art doc are still needed and their
  descriptions are now wrong — they were written for the civilisation framing.
- Material ids are unaffected: they stay keyed to the vanilla terrain key (`eotg_plains_*`,
  `eotg_forest_*`), which is what the engine and the terrain index use. Only display names change.
