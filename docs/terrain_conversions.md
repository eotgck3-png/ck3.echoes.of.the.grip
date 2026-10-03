# Space Terrain Conversions: CK3 to Echoes of the Grip (EotG)

Reference guide mapping Crusader Kings III's vanilla terrains, impassables, and water features to EotG's galactic space terrains.

Terrain in EotG represents **natural astrography** (star density, nebular thickness, gravitational and radiation phenomena, and debris hazards). Man-made infrastructure (stations, ship wreckage, planetary cities, traffic) is decoupled from terrain and handled via holdings and map objects.

---

## 1. Land Terrains

| Vanilla CK3 Key | EotG Space Terrain | Core Astrographical Concept | Vanilla Land % |
|---|---|---|---|
| `plains` | **Open Cluster** | Navigable, standard void with few stellar hazards; accessible systems. | 24.5% |
| `hills` | **Broken Cluster** | Irregular routes, scattered asteroids, and natural stellar debris. | 6.2% |
| `desert` | **Barren Reach** | Vast empty space with very few isolated stars or habitable systems. | 4.3% |
| `mountains` | **Nebula Barrier** | Chokepoints formed by dense, opaque indigo nebulae, radiation, or gravity wells. | 3.9% |
| `taiga` | **Frozen Cluster** | Frigid environments of icy planetoids, frozen dust, and dim blue stars. | 3.6% |
| `drylands` | **Arid Reach** | Low natural moisture/biological resources; warm brown dust and sparse stars. | 3.2% |
| `forest` | **Dense Cluster** | Systems packed tightly together; high destination density, complex transit. | 2.6% |
| `steppe` | **Frontier Reach** | Open, peripheral regions beyond primary galactic routes; widely spaced pale stars. | 2.6% |
| `jungle` | **Nebula Wilds** | Dense, tangled thicket of warm rose/crimson gas filaments and hidden systems. | 1.6% |
| `desert_mountains` | **Barren Barrier** | Extremely harsh combination of sparse resources and hazardous natural barriers. | 1.0% |
| `wetlands` | **Anomaly Fields** | Unstable gravitational anomalies, distortion rings, and lensing arcs warping starlight. | 0.9% |
| `farmlands` | **Fertile Reach** | Unusually high concentration of naturally habitable worlds and warm golden stars. | 0.4% |
| `floodplains` | **Volatile Cluster** | Energetic, highly fluctuating conditions; flaring orange stars and turbulent gas. | 0.4% |
| `oasis` | **Sanctuary Systems** | Rare, calm pockets of favorable space sheltered within hostile expanses. | 0.3% |
| `terraced_hills` | **Layered Cluster** | Terraced corridors and elevation pockets offering defensive advantage. | 0.2% |

---

## 2. In-Depth Terrain Profiles & Art Direction

### Open Cluster (`plains`)
* **Description:** The most navigable and straightforward regions of space. Systems are accessible with minimal stellar hazards. Can host anything from untouched worlds to sprawling civilizations.
* **Art Direction:** Sparse, evenly scattered stars in open dark space; faint dust, almost black background; quietest terrain on the map backdrop.

### Broken Cluster (`hills`)
* **Description:** Scattered systems, difficult routes, stellar debris, and irregular navigation. Travel is possible but less straightforward than through an Open Cluster.
* **Art Direction:** Fragmented region of scattered stellar debris and rocky rubble between irregular star systems. Rubble rendered as dark non-star shapes.

### Nebula Barrier (`mountains`)
* **Description:** Dominated by dense nebulae, severe gravitational phenomena, radiation, or other astronomical obstacles. Natural chokepoints and boundaries.
* **Art Direction:** Vast, cold, opaque wall of deep indigo/violet gas. Low frequency, large scale, starless to contrast with Nebula Wilds.

### Barren Reach (`desert`)
* **Description:** Sparse regions with few habitable or easily exploitable systems. Long distances between viable destinations; isolated settlements rely heavily on self-sufficiency.
* **Art Direction:** Very few isolated faint stars separated by vast darkness; cold, desaturated, near-black void.

### Barren Barrier (`desert_mountains`)
* **Description:** The harshest combination of sparse resources and difficult navigation, acting as formidable frontier boundaries between accessible areas of the galaxy.
* **Art Direction:** Dark, dense dust clouds and sparse debris; almost no stars; hostile, dark, impassable appearance.

### Frozen Cluster (`taiga`)
* **Description:** Extremely cold environments, icy worlds, and frozen bodies. Operating here requires specialized adaptation.
* **Art Direction:** Cold blue-white tones, frost-lit debris, and dim blue stars along a cool temperature spectrum.

### Arid Reach (`drylands`)
* **Description:** Low moisture, sparse naturally habitable environments, and limited biological resources. Sustaining life relies more on imported resources or artificial infrastructure.
* **Art Direction:** Warm brown-grey dust and thin haze, scattering of isolated stars; sun-scorched, depleted look.

### Dense Cluster (`forest`)
* **Description:** Systems packed relatively closely together; high density of navigable destinations. Complex transit and military operations, but rich opportunities for habitation and industry.
* **Art Direction:** Densely packed, bright stars crowded close together with thin gas between them.

### Frontier Reach (`steppe`)
* **Description:** Open regions beyond established routes and galactic centers. May contain newly accessible systems, isolated populations, or unclaimed space.
* **Art Direction:** Widely spaced pale stars, thin faint dust, open and peripheral void.

### Nebula Wilds (`jungle`)
* **Description:** Vast regions enveloped in dense nebulae and unpredictable stellar phenomena. Navigation is difficult, communications unreliable, and systems easily hidden.
* **Art Direction:** Tangled thicket of warm rose and crimson gas filaments; small-scale interwoven strands with numerous dim stars visible through gaps.

### Anomaly Fields (`wetlands`)
* **Description:** High concentrations of gravitational anomalies, radiation phenomena, unstable stellar objects, or unexplained disturbances.
* **Art Direction:** Concentric gravitational lensing rings and distortion arcs warping background starlight; teal and green phenomena.

### Fertile Reach (`farmlands`)
* **Description:** Unusually high concentration of naturally habitable worlds, valuable resources, or otherwise favorable systems. High natural potential, regardless of whether it is developed.
* **Art Direction:** Dense, warm golden stars, soft warm gas, inviting golden glow.

### Volatile Cluster (`floodplains`)
* **Description:** Stellar or environmental conditions fluctuate significantly. Systems may be exceptionally productive while presenting unusual dangers.
* **Art Direction:** Flaring orange stars, dynamic energetic gas, flickering solar flares.

### Sanctuary Systems (`oasis`)
* **Description:** Small pockets of unusually favorable space surrounded by more difficult or inhospitable regions. Reliable places for resupply or strategic refuge.
* **Art Direction:** A gentle, warm golden cluster of stars forming a calm, glowing pocket in deep void.

### Layered Cluster (`terraced_hills`)
* **Description:** Systems distributed across variations in stellar geography, orbital environments, and navigational elevation. Corridors create naturally defensible territory.
* **Art Direction:** Interconnected star pockets separated by contour-following raised dust strata.

---

## 3. Special, Non-Land, and Map Boundary Features

* **Impassable Wastelands (`impassable_mountains`):**
  * Assigned its own dedicated material (`impassable`) distinct from playable `desert_mountains`. Uses the Barren Barrier aesthetic but with star density reduced to near zero (`0.06`) and dark rust tones.
* **System Edge (`eotg_edge` / beaches):**
  * Replaces vanilla beach/coastline materials. Represents the boundary threshold where colonized stellar clusters drop off into deep void.
* **Oceans and Seas:**
  * Rendered as **Deep Void** with dynamic energy shorelines via `gfx/FX/pdxwater.shader`.
* **Rivers:**
  * Rendered as **Stellar Wind Energy Lanes** (self-illuminated glowing warp corridors) via `gfx/FX/river_surface.shader`.

---

## 4. Source Documentation

* Canonical Terrain Scheme: [`docs/terrain_scheme.md`](file:///c:/Users/river/Documents/GitHub/ck3.echoes.of.the.grip/docs/terrain_scheme.md)
* Terrain Materials & Pipeline: [`docs/terrain_materials.md`](file:///c:/Users/river/Documents/GitHub/ck3.echoes.of.the.grip/docs/terrain_materials.md)
* Midjourney Texture Prompts: [`docs/terrain_texture_prompts.md`](file:///c:/Users/river/Documents/GitHub/ck3.echoes.of.the.grip/docs/terrain_texture_prompts.md)
