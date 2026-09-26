# Echoes of the Grip — Title Hierarchy Reference
# For use by Claude Code when generating landed_titles, title history, and character history files.
# Last updated: definition.csv v288 entries (IDs 0–287)

## Conventions
- **Capital** designations cascade upward: a barony marked `[COUNTY CAPITAL]` is the holding
  that defines the county title. The first barony listed under each county is always the capital.
- County capital = first barony of the county
- Duchy capital = first county of the duchy (and its first barony)
- Kingdom capital = first duchy of the kingdom (and its capital chain)
- Empire capital = first kingdom (Myr Core → Xerxes Reach → County of Xerxes → xerxes)
- Province IDs correspond directly to entries in `map_data/definition.csv`
- All title keys should use the prefix `eotg_` in landed_titles.txt

## Capital Chain Summary

| Level   | Title                        | Capital Key             | Province ID |
|---------|------------------------------|-------------------------|-------------|
| Empire  | Myr Cluster                  | xerxes                  | 1           |
| Kingdom | The Myr Core                 | xerxes                  | 1           |
| Duchy   | Xerxes Reach                 | xerxes                  | 1           |
| County  | County of Xerxes             | xerxes                  | 1           |
| Kingdom | The Cauldron Marches         | bastion_halreth         | 71          |
| Duchy   | Vanguard March               | bastion_halreth         | 71          |
| County  | County of Bastion Halreth    | bastion_halreth         | 71          |
| Kingdom | The Coldiron Marches         | frostfall               | 118         |
| Duchy   | Coldiron March               | frostfall               | 118         |
| County  | County of Frostfall          | frostfall               | 118         |
| Kingdom | The Lanius Expanse           | caer_myr                | 151         |
| Duchy   | Lanius Systems               | caer_myr                | 151         |
| County  | County of Caer Myr           | caer_myr                | 151         |
| Kingdom | The Charter Principalities   | brokers_exchange        | 192         |
| Duchy   | Broker's Reach               | brokers_exchange        | 192         |
| County  | County of Brokers Exchange   | brokers_exchange        | 192         |
| Kingdom | The Outer Marches            | chitterholm             | 233         |
| Duchy   | Warrens                      | chitterholm             | 233         |
| County  | County of Chitterholm        | chitterholm             | 233         |

---

## Empire: Myr Cluster
> Capital: `xerxes` (Province 1)
> The overarching empire title spanning all six kingdoms.

---

## Kingdom: The Myr Core
> Capital: `xerxes` (Province 1) via Duchy of Xerxes Reach → County of Xerxes

### Duchy: Xerxes Reach
> Capital: `xerxes` (Province 1) via County of Xerxes
> Duchy capital county: County of Xerxes

#### County of Xerxes `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 1 | `xerxes` | **[COUNTY CAPITAL]** |
| 2 | `the_wend` | |
| 3 | `the_sunken` | |
| 4 | `thornspire` | |
| 5 | `veldris_reach` | |
| 6 | `irongate_passage` | |

#### County of Auric Belt
| Province ID | Key | Notes |
|-------------|-----|-------|
| 7 | `auric_belt` | **[COUNTY CAPITAL]** |
| 8 | `crestfall` | |
| 9 | `pellio` | |
| 10 | `vaulted_reach` | |
| 11 | `kethara` | |

#### County of Kaeltrix
| Province ID | Key | Notes |
|-------------|-----|-------|
| 12 | `kaeltrix` | **[COUNTY CAPITAL]** |
| 13 | `driftshard` | |
| 14 | `emberveil` | |
| 15 | `hollowed_expanse` | |
| 16 | `rimeglass` | |

#### County of Pellion
| Province ID | Key | Notes |
|-------------|-----|-------|
| 31 | `pellion_gate` | **[COUNTY CAPITAL]** |
| 32 | `pellio_reach` | |
| 33 | `keth_hollow` | |

---

### Duchy: Aphionian Belt
> Capital: `aphion_crossing` (Province 17) via County of Aphion

#### County of Aphion `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 17 | `aphion_crossing` | **[COUNTY CAPITAL]** |
| 18 | `cinderhull` | |
| 19 | `starfall_breach` | |
| 20 | `ashen_threshold` | |

#### County of Lumina Verge
| Province ID | Key | Notes |
|-------------|-----|-------|
| 21 | `lumina_verge` | **[COUNTY CAPITAL]** |
| 22 | `pyrestone` | |
| 23 | `blazewatch` | |
| 24 | `the_searing` | |

#### County of Verdant Straits
| Province ID | Key | Notes |
|-------------|-----|-------|
| 25 | `verdant_straits` | **[COUNTY CAPITAL]** |
| 26 | `heatwall` | |
| 27 | `torchrun` | |

#### County of Grand Kiln
| Province ID | Key | Notes |
|-------------|-----|-------|
| 28 | `grand_kiln` | **[COUNTY CAPITAL]** |
| 29 | `furnace_drift` | |
| 30 | `meltspire` | |

#### County of Cindergate
| Province ID | Key | Notes |
|-------------|-----|-------|
| 34 | `cindergate` | **[COUNTY CAPITAL]** |
| 35 | `ashrun` | |
| 36 | `the_scorch` | |

---

### Duchy: Coreward Expanse
> Capital: `nebras_hollow` (Province 37) via County of Nebras Hollow

#### County of Nebras Hollow `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 37 | `nebras_hollow` | **[COUNTY CAPITAL]** |
| 38 | `halvenmere` | |
| 39 | `verdance` | |
| 40 | `rustgrove` | |
| 41 | `the_deepcore` | |

#### County of Concordance
| Province ID | Key | Notes |
|-------------|-----|-------|
| 42 | `concordance` | **[COUNTY CAPITAL]** |
| 43 | `coreline` | |
| 44 | `driftpoint` | |
| 45 | `vaultwatch` | |

#### County of Corefall
| Province ID | Key | Notes |
|-------------|-----|-------|
| 46 | `corefall` | **[COUNTY CAPITAL]** |
| 47 | `helix_margin` | |
| 48 | `prismhold` | |
| 49 | `stardepth` | |

---

### Duchy: Helix Remnant
> Capital: `helixfall` (Province 50) via County of Helixfall

#### County of Helixfall `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 50 | `helixfall` | **[COUNTY CAPITAL]** |
| 51 | `the_fracture` | |
| 52 | `ruin_drift` | |

#### County of Fracturepoint
| Province ID | Key | Notes |
|-------------|-----|-------|
| 53 | `fracturepoint` | **[COUNTY CAPITAL]** |
| 54 | `shattered_relay` | |
| 55 | `the_breach` | |
| 56 | `shard_margin` | |

#### County of Remnant Core
| Province ID | Key | Notes |
|-------------|-----|-------|
| 57 | `remnant_core` | **[COUNTY CAPITAL]** |
| 58 | `helix_tomb` | |
| 59 | `the_collapse` | |

---

### Duchy: The Siege Reaches
> Capital: `the_bulwark` (Province 60) via County of the Bulwark
> Lore: Defensive lines held by Myr Cluster peoples against the First of the Third Elrossi crusade.

#### County of the Bulwark `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 60 | `the_bulwark` | **[COUNTY CAPITAL]** |
| 61 | `ironhold` | |
| 62 | `siege_line` | |
| 63 | `rampart` | |

#### County of Vanguard Wall
| Province ID | Key | Notes |
|-------------|-----|-------|
| 64 | `vanguard_wall` | **[COUNTY CAPITAL]** |
| 65 | `the_redoubt` | |
| 66 | `flankmark` | |

#### County of Orveth
| Province ID | Key | Notes |
|-------------|-----|-------|
| 67 | `orveth` | **[COUNTY CAPITAL]** |
| 68 | `orveth_span` | |
| 69 | `the_standfirm` | |
| 70 | `ashguard` | |

---

## Kingdom: The Cauldron Marches
> Capital: `bastion_halreth` (Province 71) via Duchy of Vanguard March → County of Bastion Halreth

### Duchy: Vanguard March
> Capital: `bastion_halreth` (Province 71) via County of Bastion Halreth

#### County of Bastion Halreth `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 71 | `bastion_halreth` | **[COUNTY CAPITAL]** |
| 72 | `vanguard_span` | |
| 73 | `the_forewall` | |
| 74 | `ironveil` | |

#### County of Silver Crest
| Province ID | Key | Notes |
|-------------|-----|-------|
| 75 | `silver_crest` | **[COUNTY CAPITAL]** |
| 76 | `marchwall` | |
| 77 | `boldwatch` | |
| 78 | `stormveil` | |

#### County of Bridgehead
| Province ID | Key | Notes |
|-------------|-----|-------|
| 79 | `bridgehead` | **[COUNTY CAPITAL]** |
| 80 | `coldfront` | |
| 81 | `emberveil_crossing` | |
| 82 | `ironwall` | |

---

### Duchy: Helix Fringe
> Capital: `helixport` (Province 83) via County of Helix

#### County of Helix `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 83 | `helixport` | **[COUNTY CAPITAL]** |
| 84 | `the_spiral` | |
| 85 | `prismgate` | |
| 86 | `coilwatch` | |

#### County of Fringefall
| Province ID | Key | Notes |
|-------------|-----|-------|
| 87 | `fringefall` | **[COUNTY CAPITAL]** |
| 88 | `arcline` | |
| 89 | `the_loophole` | |
| 90 | `warpwatch` | |

#### County of Tangent
| Province ID | Key | Notes |
|-------------|-----|-------|
| 91 | `the_tangent` | **[COUNTY CAPITAL]** |
| 92 | `deviance` | |
| 93 | `breakpoint` | |
| 94 | `edgewatch` | |
| 95 | `torsion_reach` | |

---

### Duchy: Emberline March
> Capital: `emberline` (Province 96) via County of Emberline

#### County of Emberline `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 96 | `emberline` | **[COUNTY CAPITAL]** |
| 97 | `charrun` | |
| 98 | `scorchwall` | |

#### County of Cinderfall
| Province ID | Key | Notes |
|-------------|-----|-------|
| 99 | `cinderfall` | **[COUNTY CAPITAL]** |
| 100 | `burnwatch` | |
| 101 | `flamegate` | |

#### County of Ashveil
| Province ID | Key | Notes |
|-------------|-----|-------|
| 102 | `ashveil` | **[COUNTY CAPITAL]** |
| 103 | `the_ashline` | |
| 104 | `cinder_margin` | |

---

### Duchy: The Forge Marches
> Capital: `mikey_iv` (Province 105) via County of Mikey IV
> Lore: Future Duergar rebellion region. Mikey IV is a tall barony — designed for heavy development as a regional capital.

#### County of Mikey IV `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 105 | `mikey_iv` | **[COUNTY CAPITAL]** — tall location, prioritise building slots |
| 106 | `the_deep_vein` | |
| 107 | `stonehollow` | |
| 108 | `forge_depths` | |
| 109 | `anvil_reach` | |

#### County of Dûmholt
| Province ID | Key | Notes |
|-------------|-----|-------|
| 110 | `dumholt` | **[COUNTY CAPITAL]** |
| 111 | `ironseam` | |
| 112 | `the_underbore` | |

#### County of the Karak Line
| Province ID | Key | Notes |
|-------------|-----|-------|
| 113 | `karak_line` | **[COUNTY CAPITAL]** |
| 114 | `stonemarsh` | |
| 115 | `the_delve` | |

#### County of Ashvein
| Province ID | Key | Notes |
|-------------|-----|-------|
| 116 | `ashvein` | **[COUNTY CAPITAL]** |
| 117 | `the_quarry` | |

---

## Kingdom: The Coldiron Marches
> Capital: `frostfall` (Province 118) via Duchy of Coldiron March → County of Frostfall

### Duchy: Coldiron March
> Capital: `frostfall` (Province 118) via County of Frostfall

#### County of Frostfall `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 118 | `frostfall` | **[COUNTY CAPITAL]** |
| 119 | `coldiron_span` | |
| 120 | `shatterpeak` | |
| 121 | `glacial_hold` | |

#### County of Frostblade
| Province ID | Key | Notes |
|-------------|-----|-------|
| 122 | `frostblade` | **[COUNTY CAPITAL]** |
| 123 | `coldwatch` | |
| 124 | `icegate` | |
| 125 | `rimeguard` | |

#### County of Snowveil
| Province ID | Key | Notes |
|-------------|-----|-------|
| 126 | `snowveil` | **[COUNTY CAPITAL]** |
| 127 | `arcticline` | |
| 128 | `blizzardwatch` | |
| 129 | `winterhold` | |
| 130 | `permafrost_reach` | |

---

### Duchy: Aegis Corridor
> Capital: `aegis_crossing` (Province 131) via County of Aegis Crossing

#### County of Aegis Crossing `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 131 | `aegis_crossing` | **[COUNTY CAPITAL]** |
| 132 | `concordspire` | |
| 133 | `the_covenant` | |
| 134 | `pact_drift` | |

#### County of Sternstahl
| Province ID | Key | Notes |
|-------------|-----|-------|
| 135 | `sternstahl_reach` | **[COUNTY CAPITAL]** |
| 136 | `imperial_hold` | |
| 137 | `the_threshold` | |

#### County of Celestial Codex
| Province ID | Key | Notes |
|-------------|-----|-------|
| 138 | `celestial_codex` | **[COUNTY CAPITAL]** |
| 139 | `firststar` | |
| 140 | `the_codex` | |

---

### Duchy: Sable Verge
> Capital: `sable_reach` (Province 141) via County of Sable

#### County of Sable `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 141 | `sable_reach` | **[COUNTY CAPITAL]** |
| 142 | `darkline` | |
| 143 | `voidwatch` | |

#### County of Nightfall
| Province ID | Key | Notes |
|-------------|-----|-------|
| 144 | `nightfall` | **[COUNTY CAPITAL]** |
| 145 | `shadowgate` | |
| 146 | `eclipsepoint` | |

#### County of Penumbra
| Province ID | Key | Notes |
|-------------|-----|-------|
| 147 | `penumbra` | **[COUNTY CAPITAL]** |
| 148 | `duskline` | |
| 149 | `twilight_reach` | |
| 150 | `obsidian_margin` | |

---

## Kingdom: The Lanius Expanse
> Capital: `caer_myr` (Province 151) via Duchy of Lanius Systems → County of Caer Myr
> Lore: Elrossi Principality homeland. Caer_myr is the kingdom and duchy capital.

### Duchy: Lanius Systems
> Capital: `caer_myr` (Province 151) via County of Caer Myr

#### County of Caer Myr `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 151 | `caer_myr` | **[COUNTY CAPITAL]** — kingdom and duchy capital |
| 152 | `vulturehold` | |
| 153 | `carrion_drift` | |

#### County of Siege Hold
| Province ID | Key | Notes |
|-------------|-----|-------|
| 154 | `siege_hold` | **[COUNTY CAPITAL]** |
| 155 | `scourgefall` | |
| 156 | `ravenfall` | |

#### County of the Strikeline
| Province ID | Key | Notes |
|-------------|-----|-------|
| 157 | `the_strikeline` | **[COUNTY CAPITAL]** |
| 158 | `velantir` | |

#### County of Dawnstrike
| Province ID | Key | Notes |
|-------------|-----|-------|
| 159 | `dawnstrike` | **[COUNTY CAPITAL]** |
| 160 | `taloncrest` | |
| 161 | `aethon` | |
| 162 | `the_circling` | |

#### County of Lanius Span
| Province ID | Key | Notes |
|-------------|-----|-------|
| 163 | `lanius_span` | **[COUNTY CAPITAL]** |
| 164 | `elrossi_span` | |
| 165 | `the_principate` | |

#### County of Elrossi Reach
| Province ID | Key | Notes |
|-------------|-----|-------|
| 166 | `elrossi_reach` | **[COUNTY CAPITAL]** |
| 167 | `the_faithful` | |
| 168 | `sanctum_drift` | |

---

### Duchy: Starward Reach
> Capital: `starward` (Province 169) via County of Starward
> Lore: Elrossi holy order territory — Starward Wardens, Silver Lion, Istrova.

#### County of Starward `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 169 | `starward` | **[COUNTY CAPITAL]** |
| 170 | `wardens_drift` | |
| 171 | `the_citadel` | |
| 172 | `luminance` | |

#### County of Silver Lion
| Province ID | Key | Notes |
|-------------|-----|-------|
| 173 | `silver_lion` | **[COUNTY CAPITAL]** |
| 174 | `celestian_hold` | |
| 175 | `dawnsong` | |
| 176 | `sunward` | |

#### County of Istrova
| Province ID | Key | Notes |
|-------------|-----|-------|
| 177 | `solantis` | **[COUNTY CAPITAL]** |
| 178 | `istrova` | |
| 179 | `istrova_span` | |
| 180 | `the_shield` | |

---

### Duchy: Silver Veil
> Capital: `silver_veil` (Province 181) via County of Silver Veil
> Lore: Crusader/knight order territory — Star Lance, Order Fall, Zeladon.

#### County of Silver Veil `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 181 | `silver_veil` | **[COUNTY CAPITAL]** |
| 182 | `veil_crossing` | |
| 183 | `lionmere` | |
| 184 | `star_lance` | |
| 185 | `the_crusade` | |
| 186 | `lancefall` | |

#### County of Zeladon
| Province ID | Key | Notes |
|-------------|-----|-------|
| 187 | `zeladon` | **[COUNTY CAPITAL]** |
| 188 | `zeladon_span` | |
| 189 | `the_pale` | |
| 190 | `order_fall` | |
| 191 | `relicholm` | |

---

## Kingdom: The Charter Principalities
> Capital: `brokers_exchange` (Province 192) via Duchy of Broker's Reach → County of Brokers Exchange

### Duchy: Broker's Reach
> Capital: `brokers_exchange` (Province 192) via County of Brokers Exchange
> Lore: Gob-Ogre Trade League corporate territory. New Aldenmere and Harrow's Claim are independent human settlements at start date.

#### County of Brokers Exchange `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 192 | `brokers_exchange` | **[COUNTY CAPITAL]** |
| 193 | `grubmarket` | |
| 194 | `krongeld` | |
| 195 | `geldspire` | |
| 196 | `inkwell` | |

#### County of Iron Pact
| Province ID | Key | Notes |
|-------------|-----|-------|
| 197 | `iron_pact_depot` | **[COUNTY CAPITAL]** |
| 198 | `geldtrace` | |
| 199 | `the_bourse` | |
| 200 | `skarntoll` | |
| 201 | `bondwatch` | |

#### County of Cofferfall
| Province ID | Key | Notes |
|-------------|-----|-------|
| 202 | `cofferfall` | **[COUNTY CAPITAL]** |
| 203 | `grimstock` | |
| 204 | `geldmire` | |
| 205 | `the_ledger` | |

#### County of Geldrun
| Province ID | Key | Notes |
|-------------|-----|-------|
| 206 | `geldrun` | **[COUNTY CAPITAL]** |
| 207 | `slag_market` | |
| 208 | `the_yield` | |

#### County of New Aldenmere
> Lore: Independent human settlement at bookmark date — not under Gob-Ogre control at start.
| Province ID | Key | Notes |
|-------------|-----|-------|
| 209 | `new_aldenmere` | **[COUNTY CAPITAL]** |
| 210 | `aldenmere_reach` | |
| 211 | `harrows_post` | |

#### County of Harrow's Claim
> Lore: Independent human settlement at bookmark date — adjacent to New Aldenmere, not under Gob-Ogre control at start.
| Province ID | Key | Notes |
|-------------|-----|-------|
| 212 | `harrows_claim` | **[COUNTY CAPITAL]** |
| 213 | `settlers_rest` | |
| 214 | `new_veth` | |

---

### Duchy: Pioneer Marches
> Capital: `pioneer_span` (Province 215) via County of Pioneer

#### County of Pioneer `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 215 | `pioneer_span` | **[COUNTY CAPITAL]** |
| 216 | `deepmark` | |
| 217 | `firstfall` | |

#### County of Trailhead
| Province ID | Key | Notes |
|-------------|-----|-------|
| 218 | `trailhead` | **[COUNTY CAPITAL]** |
| 219 | `waystation` | |
| 220 | `farsight` | |

#### County of Outpost
| Province ID | Key | Notes |
|-------------|-----|-------|
| 221 | `the_outpost` | **[COUNTY CAPITAL]** |
| 222 | `frontier_span` | |
| 223 | `edgepost` | |
| 224 | `waymark` | |

---

### Duchy: Halcyon Strip
> Capital: `halcyon_reach` (Province 225) via County of Halcyon

#### County of Halcyon `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 225 | `halcyon_reach` | **[COUNTY CAPITAL]** |
| 226 | `serenfall` | |
| 227 | `calmwatch` | |
| 228 | `quietline` | |

#### County of Stillwater
| Province ID | Key | Notes |
|-------------|-----|-------|
| 229 | `stillwater` | **[COUNTY CAPITAL]** |
| 230 | `peacewatch` | |
| 231 | `solace_span` | |
| 232 | `dawnhaven` | |

---

## Kingdom: The Outer Marches
> Capital: `chitterholm` (Province 233) via Duchy of Warrens → County of Chitterholm

### Duchy: Warrens
> Capital: `chitterholm` (Province 233) via County of Chitterholm
> Lore: Ratfolk territory. Txic_gate references Txic'Er lore name. Skarlforge references Skarlmagicka.

#### County of Chitterholm `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 233 | `chitterholm` | **[COUNTY CAPITAL]** |
| 234 | `rustspire` | |
| 235 | `skarlforge` | |

#### County of Scrapyard
| Province ID | Key | Notes |
|-------------|-----|-------|
| 236 | `scrapyard` | **[COUNTY CAPITAL]** |
| 237 | `the_gnaw` | |
| 238 | `the_burrow` | |

#### County of Txic Gate
| Province ID | Key | Notes |
|-------------|-----|-------|
| 239 | `txic_gate` | **[COUNTY CAPITAL]** |
| 240 | `gnaxtun` | |
| 241 | `deepburrow` | |
| 242 | `the_underworks` | |

#### County of Skrix Deep
| Province ID | Key | Notes |
|-------------|-----|-------|
| 243 | `skrix_deep` | **[COUNTY CAPITAL]** |
| 244 | `the_gnawing` | |
| 245 | `burrownest` | |

---

### Duchy: Rust Verge
> Capital: `rust_hollow` (Province 246) via County of Rust Hollow
> Lore: Industrial ruins of the collapsed Gob-Ogre Trade League.

#### County of Rust Hollow `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 246 | `rust_hollow` | **[COUNTY CAPITAL]** |
| 247 | `corrode` | |
| 248 | `scrapline` | |

#### County of Ironwaste
| Province ID | Key | Notes |
|-------------|-----|-------|
| 249 | `ironwaste` | **[COUNTY CAPITAL]** |
| 250 | `the_decay` | |
| 251 | `oxidespire` | |

---

### Duchy: Dead Reach
> Capital: `the_dead` (Province 252) via County of the Dead

#### County of the Dead `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 252 | `the_dead` | **[COUNTY CAPITAL]** |
| 253 | `derelict` | |

#### County of Wreckhold
| Province ID | Key | Notes |
|-------------|-----|-------|
| 254 | `wreckhold` | **[COUNTY CAPITAL]** |
| 255 | `the_silence` | |

#### County of Graveline
| Province ID | Key | Notes |
|-------------|-----|-------|
| 256 | `graveline` | **[COUNTY CAPITAL]** |
| 257 | `the_forgotten` | |
| 258 | `hollowfield` | |
| 259 | `ashen_span` | |

---

### Duchy: Uvrek
> Capital: `uvrek` (Province 260) via County of Uvrek
> Lore: Fringe independent governments and minor companies — isolated systems, no major faction allegiance.

#### County of Uvrek `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 260 | `uvrek` | **[COUNTY CAPITAL]** |
| 261 | `uvrek_span` | |
| 262 | `uvrek_margin` | |

#### County of Vorshaan
| Province ID | Key | Notes |
|-------------|-----|-------|
| 263 | `vorshaan` | **[COUNTY CAPITAL]** |
| 264 | `vorshaan_drift` | |
| 265 | `the_vorsway` | |

#### County of the Drifting
| Province ID | Key | Notes |
|-------------|-----|-------|
| 266 | `the_drifting` | **[COUNTY CAPITAL]** |
| 267 | `skeld_margin` | |
| 268 | `outermark` | |
| 269 | `the_fringe` | |

---

### Duchy: Varek's Silence
> Capital: `vareks_edge` (Province 270) via County of Varek's Edge
> Lore: Deep uninhabited frontier — sparse, abandoned, no known inhabitants at bookmark date.

#### County of Varek's Edge `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 270 | `vareks_edge` | **[COUNTY CAPITAL]** |
| 271 | `the_stillness` | |
| 272 | `far_nothing` | |

#### County of the Hollow Dark
| Province ID | Key | Notes |
|-------------|-----|-------|
| 273 | `hollow_dark` | **[COUNTY CAPITAL]** |
| 274 | `the_dim` | |
| 275 | `lost_signal` | |

#### County of the Pale Beyond
| Province ID | Key | Notes |
|-------------|-----|-------|
| 276 | `pale_beyond` | **[COUNTY CAPITAL]** |
| 277 | `the_uncharted` | |
| 278 | `deepwatch` | |

---

### Duchy: The Far Drift
> Capital: `drifting_dark` (Province 279) via County of the Drifting Dark
> Lore: Deep uninhabited frontier — lost systems, no reliable navigation data.

#### County of the Drifting Dark `[DUCHY CAPITAL COUNTY]`
| Province ID | Key | Notes |
|-------------|-----|-------|
| 279 | `drifting_dark` | **[COUNTY CAPITAL]** |
| 280 | `the_current` | |
| 281 | `far_margin` | |

#### County of the Lost Reach
| Province ID | Key | Notes |
|-------------|-----|-------|
| 282 | `lost_reach` | **[COUNTY CAPITAL]** |
| 283 | `adrift` | |
| 284 | `the_wander` | |

#### County of the Outer Pale
| Province ID | Key | Notes |
|-------------|-----|-------|
| 285 | `outer_pale` | **[COUNTY CAPITAL]** |
| 286 | `the_scatter` | |
| 287 | `last_light` | |

---

## Quick Reference: All Province IDs

| ID | Key | County | Duchy | Kingdom |
|----|-----|--------|-------|---------|
| 0 | ocean | — | — | — |
| 1 | xerxes | County of Xerxes | Xerxes Reach | The Myr Core |
| 2 | the_wend | County of Xerxes | Xerxes Reach | The Myr Core |
| 3 | the_sunken | County of Xerxes | Xerxes Reach | The Myr Core |
| 4 | thornspire | County of Xerxes | Xerxes Reach | The Myr Core |
| 5 | veldris_reach | County of Xerxes | Xerxes Reach | The Myr Core |
| 6 | irongate_passage | County of Xerxes | Xerxes Reach | The Myr Core |
| 7 | auric_belt | County of Auric Belt | Xerxes Reach | The Myr Core |
| 8 | crestfall | County of Auric Belt | Xerxes Reach | The Myr Core |
| 9 | pellio | County of Auric Belt | Xerxes Reach | The Myr Core |
| 10 | vaulted_reach | County of Auric Belt | Xerxes Reach | The Myr Core |
| 11 | kethara | County of Auric Belt | Xerxes Reach | The Myr Core |
| 12 | kaeltrix | County of Kaeltrix | Xerxes Reach | The Myr Core |
| 13 | driftshard | County of Kaeltrix | Xerxes Reach | The Myr Core |
| 14 | emberveil | County of Kaeltrix | Xerxes Reach | The Myr Core |
| 15 | hollowed_expanse | County of Kaeltrix | Xerxes Reach | The Myr Core |
| 16 | rimeglass | County of Kaeltrix | Xerxes Reach | The Myr Core |
| 17 | aphion_crossing | County of Aphion | Aphionian Belt | The Myr Core |
| 18 | cinderhull | County of Aphion | Aphionian Belt | The Myr Core |
| 19 | starfall_breach | County of Aphion | Aphionian Belt | The Myr Core |
| 20 | ashen_threshold | County of Aphion | Aphionian Belt | The Myr Core |
| 21 | lumina_verge | County of Lumina Verge | Aphionian Belt | The Myr Core |
| 22 | pyrestone | County of Lumina Verge | Aphionian Belt | The Myr Core |
| 23 | blazewatch | County of Lumina Verge | Aphionian Belt | The Myr Core |
| 24 | the_searing | County of Lumina Verge | Aphionian Belt | The Myr Core |
| 25 | verdant_straits | County of Verdant Straits | Aphionian Belt | The Myr Core |
| 26 | heatwall | County of Verdant Straits | Aphionian Belt | The Myr Core |
| 27 | torchrun | County of Verdant Straits | Aphionian Belt | The Myr Core |
| 28 | grand_kiln | County of Grand Kiln | Aphionian Belt | The Myr Core |
| 29 | furnace_drift | County of Grand Kiln | Aphionian Belt | The Myr Core |
| 30 | meltspire | County of Grand Kiln | Aphionian Belt | The Myr Core |
| 31 | pellion_gate | County of Pellion | Xerxes Reach | The Myr Core |
| 32 | pellio_reach | County of Pellion | Xerxes Reach | The Myr Core |
| 33 | keth_hollow | County of Pellion | Xerxes Reach | The Myr Core |
| 34 | cindergate | County of Cindergate | Aphionian Belt | The Myr Core |
| 35 | ashrun | County of Cindergate | Aphionian Belt | The Myr Core |
| 36 | the_scorch | County of Cindergate | Aphionian Belt | The Myr Core |
| 37 | nebras_hollow | County of Nebras Hollow | Coreward Expanse | The Myr Core |
| 38 | halvenmere | County of Nebras Hollow | Coreward Expanse | The Myr Core |
| 39 | verdance | County of Nebras Hollow | Coreward Expanse | The Myr Core |
| 40 | rustgrove | County of Nebras Hollow | Coreward Expanse | The Myr Core |
| 41 | the_deepcore | County of Nebras Hollow | Coreward Expanse | The Myr Core |
| 42 | concordance | County of Concordance | Coreward Expanse | The Myr Core |
| 43 | coreline | County of Concordance | Coreward Expanse | The Myr Core |
| 44 | driftpoint | County of Concordance | Coreward Expanse | The Myr Core |
| 45 | vaultwatch | County of Concordance | Coreward Expanse | The Myr Core |
| 46 | corefall | County of Corefall | Coreward Expanse | The Myr Core |
| 47 | helix_margin | County of Corefall | Coreward Expanse | The Myr Core |
| 48 | prismhold | County of Corefall | Coreward Expanse | The Myr Core |
| 49 | stardepth | County of Corefall | Coreward Expanse | The Myr Core |
| 50 | helixfall | County of Helixfall | Helix Remnant | The Myr Core |
| 51 | the_fracture | County of Helixfall | Helix Remnant | The Myr Core |
| 52 | ruin_drift | County of Helixfall | Helix Remnant | The Myr Core |
| 53 | fracturepoint | County of Fracturepoint | Helix Remnant | The Myr Core |
| 54 | shattered_relay | County of Fracturepoint | Helix Remnant | The Myr Core |
| 55 | the_breach | County of Fracturepoint | Helix Remnant | The Myr Core |
| 56 | shard_margin | County of Fracturepoint | Helix Remnant | The Myr Core |
| 57 | remnant_core | County of Remnant Core | Helix Remnant | The Myr Core |
| 58 | helix_tomb | County of Remnant Core | Helix Remnant | The Myr Core |
| 59 | the_collapse | County of Remnant Core | Helix Remnant | The Myr Core |
| 60 | the_bulwark | County of the Bulwark | The Siege Reaches | The Myr Core |
| 61 | ironhold | County of the Bulwark | The Siege Reaches | The Myr Core |
| 62 | siege_line | County of the Bulwark | The Siege Reaches | The Myr Core |
| 63 | rampart | County of the Bulwark | The Siege Reaches | The Myr Core |
| 64 | vanguard_wall | County of Vanguard Wall | The Siege Reaches | The Myr Core |
| 65 | the_redoubt | County of Vanguard Wall | The Siege Reaches | The Myr Core |
| 66 | flankmark | County of Vanguard Wall | The Siege Reaches | The Myr Core |
| 67 | orveth | County of Orveth | The Siege Reaches | The Myr Core |
| 68 | orveth_span | County of Orveth | The Siege Reaches | The Myr Core |
| 69 | the_standfirm | County of Orveth | The Siege Reaches | The Myr Core |
| 70 | ashguard | County of Orveth | The Siege Reaches | The Myr Core |
| 71 | bastion_halreth | County of Bastion Halreth | Vanguard March | The Cauldron Marches |
| 72 | vanguard_span | County of Bastion Halreth | Vanguard March | The Cauldron Marches |
| 73 | the_forewall | County of Bastion Halreth | Vanguard March | The Cauldron Marches |
| 74 | ironveil | County of Bastion Halreth | Vanguard March | The Cauldron Marches |
| 75 | silver_crest | County of Silver Crest | Vanguard March | The Cauldron Marches |
| 76 | marchwall | County of Silver Crest | Vanguard March | The Cauldron Marches |
| 77 | boldwatch | County of Silver Crest | Vanguard March | The Cauldron Marches |
| 78 | stormveil | County of Silver Crest | Vanguard March | The Cauldron Marches |
| 79 | bridgehead | County of Bridgehead | Vanguard March | The Cauldron Marches |
| 80 | coldfront | County of Bridgehead | Vanguard March | The Cauldron Marches |
| 81 | emberveil_crossing | County of Bridgehead | Vanguard March | The Cauldron Marches |
| 82 | ironwall | County of Bridgehead | Vanguard March | The Cauldron Marches |
| 83 | helixport | County of Helix | Helix Fringe | The Cauldron Marches |
| 84 | the_spiral | County of Helix | Helix Fringe | The Cauldron Marches |
| 85 | prismgate | County of Helix | Helix Fringe | The Cauldron Marches |
| 86 | coilwatch | County of Helix | Helix Fringe | The Cauldron Marches |
| 87 | fringefall | County of Fringefall | Helix Fringe | The Cauldron Marches |
| 88 | arcline | County of Fringefall | Helix Fringe | The Cauldron Marches |
| 89 | the_loophole | County of Fringefall | Helix Fringe | The Cauldron Marches |
| 90 | warpwatch | County of Fringefall | Helix Fringe | The Cauldron Marches |
| 91 | the_tangent | County of Tangent | Helix Fringe | The Cauldron Marches |
| 92 | deviance | County of Tangent | Helix Fringe | The Cauldron Marches |
| 93 | breakpoint | County of Tangent | Helix Fringe | The Cauldron Marches |
| 94 | edgewatch | County of Tangent | Helix Fringe | The Cauldron Marches |
| 95 | torsion_reach | County of Tangent | Helix Fringe | The Cauldron Marches |
| 96 | emberline | County of Emberline | Emberline March | The Cauldron Marches |
| 97 | charrun | County of Emberline | Emberline March | The Cauldron Marches |
| 98 | scorchwall | County of Emberline | Emberline March | The Cauldron Marches |
| 99 | cinderfall | County of Cinderfall | Emberline March | The Cauldron Marches |
| 100 | burnwatch | County of Cinderfall | Emberline March | The Cauldron Marches |
| 101 | flamegate | County of Cinderfall | Emberline March | The Cauldron Marches |
| 102 | ashveil | County of Ashveil | Emberline March | The Cauldron Marches |
| 103 | the_ashline | County of Ashveil | Emberline March | The Cauldron Marches |
| 104 | cinder_margin | County of Ashveil | Emberline March | The Cauldron Marches |
| 105 | mikey_iv | County of Mikey IV | The Forge Marches | The Cauldron Marches |
| 106 | the_deep_vein | County of Mikey IV | The Forge Marches | The Cauldron Marches |
| 107 | stonehollow | County of Mikey IV | The Forge Marches | The Cauldron Marches |
| 108 | forge_depths | County of Mikey IV | The Forge Marches | The Cauldron Marches |
| 109 | anvil_reach | County of Mikey IV | The Forge Marches | The Cauldron Marches |
| 110 | dumholt | County of Dûmholt | The Forge Marches | The Cauldron Marches |
| 111 | ironseam | County of Dûmholt | The Forge Marches | The Cauldron Marches |
| 112 | the_underbore | County of Dûmholt | The Forge Marches | The Cauldron Marches |
| 113 | karak_line | County of the Karak Line | The Forge Marches | The Cauldron Marches |
| 114 | stonemarsh | County of the Karak Line | The Forge Marches | The Cauldron Marches |
| 115 | the_delve | County of the Karak Line | The Forge Marches | The Cauldron Marches |
| 116 | ashvein | County of Ashvein | The Forge Marches | The Cauldron Marches |
| 117 | the_quarry | County of Ashvein | The Forge Marches | The Cauldron Marches |
| 118 | frostfall | County of Frostfall | Coldiron March | The Coldiron Marches |
| 119 | coldiron_span | County of Frostfall | Coldiron March | The Coldiron Marches |
| 120 | shatterpeak | County of Frostfall | Coldiron March | The Coldiron Marches |
| 121 | glacial_hold | County of Frostfall | Coldiron March | The Coldiron Marches |
| 122 | frostblade | County of Frostblade | Coldiron March | The Coldiron Marches |
| 123 | coldwatch | County of Frostblade | Coldiron March | The Coldiron Marches |
| 124 | icegate | County of Frostblade | Coldiron March | The Coldiron Marches |
| 125 | rimeguard | County of Frostblade | Coldiron March | The Coldiron Marches |
| 126 | snowveil | County of Snowveil | Coldiron March | The Coldiron Marches |
| 127 | arcticline | County of Snowveil | Coldiron March | The Coldiron Marches |
| 128 | blizzardwatch | County of Snowveil | Coldiron March | The Coldiron Marches |
| 129 | winterhold | County of Snowveil | Coldiron March | The Coldiron Marches |
| 130 | permafrost_reach | County of Snowveil | Coldiron March | The Coldiron Marches |
| 131 | aegis_crossing | County of Aegis Crossing | Aegis Corridor | The Coldiron Marches |
| 132 | concordspire | County of Aegis Crossing | Aegis Corridor | The Coldiron Marches |
| 133 | the_covenant | County of Aegis Crossing | Aegis Corridor | The Coldiron Marches |
| 134 | pact_drift | County of Aegis Crossing | Aegis Corridor | The Coldiron Marches |
| 135 | sternstahl_reach | County of Sternstahl | Aegis Corridor | The Coldiron Marches |
| 136 | imperial_hold | County of Sternstahl | Aegis Corridor | The Coldiron Marches |
| 137 | the_threshold | County of Sternstahl | Aegis Corridor | The Coldiron Marches |
| 138 | celestial_codex | County of Celestial Codex | Aegis Corridor | The Coldiron Marches |
| 139 | firststar | County of Celestial Codex | Aegis Corridor | The Coldiron Marches |
| 140 | the_codex | County of Celestial Codex | Aegis Corridor | The Coldiron Marches |
| 141 | sable_reach | County of Sable | Sable Verge | The Coldiron Marches |
| 142 | darkline | County of Sable | Sable Verge | The Coldiron Marches |
| 143 | voidwatch | County of Sable | Sable Verge | The Coldiron Marches |
| 144 | nightfall | County of Nightfall | Sable Verge | The Coldiron Marches |
| 145 | shadowgate | County of Nightfall | Sable Verge | The Coldiron Marches |
| 146 | eclipsepoint | County of Nightfall | Sable Verge | The Coldiron Marches |
| 147 | penumbra | County of Penumbra | Sable Verge | The Coldiron Marches |
| 148 | duskline | County of Penumbra | Sable Verge | The Coldiron Marches |
| 149 | twilight_reach | County of Penumbra | Sable Verge | The Coldiron Marches |
| 150 | obsidian_margin | County of Penumbra | Sable Verge | The Coldiron Marches |
| 151 | caer_myr | County of Caer Myr | Lanius Systems | The Lanius Expanse |
| 152 | vulturehold | County of Caer Myr | Lanius Systems | The Lanius Expanse |
| 153 | carrion_drift | County of Caer Myr | Lanius Systems | The Lanius Expanse |
| 154 | siege_hold | County of Siege Hold | Lanius Systems | The Lanius Expanse |
| 155 | scourgefall | County of Siege Hold | Lanius Systems | The Lanius Expanse |
| 156 | ravenfall | County of Siege Hold | Lanius Systems | The Lanius Expanse |
| 157 | the_strikeline | County of the Strikeline | Lanius Systems | The Lanius Expanse |
| 158 | velantir | County of the Strikeline | Lanius Systems | The Lanius Expanse |
| 159 | dawnstrike | County of Dawnstrike | Lanius Systems | The Lanius Expanse |
| 160 | taloncrest | County of Dawnstrike | Lanius Systems | The Lanius Expanse |
| 161 | aethon | County of Dawnstrike | Lanius Systems | The Lanius Expanse |
| 162 | the_circling | County of Dawnstrike | Lanius Systems | The Lanius Expanse |
| 163 | lanius_span | County of Lanius Span | Lanius Systems | The Lanius Expanse |
| 164 | elrossi_span | County of Lanius Span | Lanius Systems | The Lanius Expanse |
| 165 | the_principate | County of Lanius Span | Lanius Systems | The Lanius Expanse |
| 166 | elrossi_reach | County of Elrossi Reach | Lanius Systems | The Lanius Expanse |
| 167 | the_faithful | County of Elrossi Reach | Lanius Systems | The Lanius Expanse |
| 168 | sanctum_drift | County of Elrossi Reach | Lanius Systems | The Lanius Expanse |
| 169 | starward | County of Starward | Starward Reach | The Lanius Expanse |
| 170 | wardens_drift | County of Starward | Starward Reach | The Lanius Expanse |
| 171 | the_citadel | County of Starward | Starward Reach | The Lanius Expanse |
| 172 | luminance | County of Starward | Starward Reach | The Lanius Expanse |
| 173 | silver_lion | County of Silver Lion | Starward Reach | The Lanius Expanse |
| 174 | celestian_hold | County of Silver Lion | Starward Reach | The Lanius Expanse |
| 175 | dawnsong | County of Silver Lion | Starward Reach | The Lanius Expanse |
| 176 | sunward | County of Silver Lion | Starward Reach | The Lanius Expanse |
| 177 | solantis | County of Istrova | Starward Reach | The Lanius Expanse |
| 178 | istrova | County of Istrova | Starward Reach | The Lanius Expanse |
| 179 | istrova_span | County of Istrova | Starward Reach | The Lanius Expanse |
| 180 | the_shield | County of Istrova | Starward Reach | The Lanius Expanse |
| 181 | silver_veil | County of Silver Veil | Silver Veil | The Lanius Expanse |
| 182 | veil_crossing | County of Silver Veil | Silver Veil | The Lanius Expanse |
| 183 | lionmere | County of Silver Veil | Silver Veil | The Lanius Expanse |
| 184 | star_lance | County of Silver Veil | Silver Veil | The Lanius Expanse |
| 185 | the_crusade | County of Silver Veil | Silver Veil | The Lanius Expanse |
| 186 | lancefall | County of Silver Veil | Silver Veil | The Lanius Expanse |
| 187 | zeladon | County of Zeladon | Silver Veil | The Lanius Expanse |
| 188 | zeladon_span | County of Zeladon | Silver Veil | The Lanius Expanse |
| 189 | the_pale | County of Zeladon | Silver Veil | The Lanius Expanse |
| 190 | order_fall | County of Zeladon | Silver Veil | The Lanius Expanse |
| 191 | relicholm | County of Zeladon | Silver Veil | The Lanius Expanse |
| 192 | brokers_exchange | County of Brokers Exchange | Broker's Reach | The Charter Principalities |
| 193 | grubmarket | County of Brokers Exchange | Broker's Reach | The Charter Principalities |
| 194 | krongeld | County of Brokers Exchange | Broker's Reach | The Charter Principalities |
| 195 | geldspire | County of Brokers Exchange | Broker's Reach | The Charter Principalities |
| 196 | inkwell | County of Brokers Exchange | Broker's Reach | The Charter Principalities |
| 197 | iron_pact_depot | County of Iron Pact | Broker's Reach | The Charter Principalities |
| 198 | geldtrace | County of Iron Pact | Broker's Reach | The Charter Principalities |
| 199 | the_bourse | County of Iron Pact | Broker's Reach | The Charter Principalities |
| 200 | skarntoll | County of Iron Pact | Broker's Reach | The Charter Principalities |
| 201 | bondwatch | County of Iron Pact | Broker's Reach | The Charter Principalities |
| 202 | cofferfall | County of Cofferfall | Broker's Reach | The Charter Principalities |
| 203 | grimstock | County of Cofferfall | Broker's Reach | The Charter Principalities |
| 204 | geldmire | County of Cofferfall | Broker's Reach | The Charter Principalities |
| 205 | the_ledger | County of Cofferfall | Broker's Reach | The Charter Principalities |
| 206 | geldrun | County of Geldrun | Broker's Reach | The Charter Principalities |
| 207 | slag_market | County of Geldrun | Broker's Reach | The Charter Principalities |
| 208 | the_yield | County of Geldrun | Broker's Reach | The Charter Principalities |
| 209 | new_aldenmere | County of New Aldenmere | Broker's Reach | The Charter Principalities |
| 210 | aldenmere_reach | County of New Aldenmere | Broker's Reach | The Charter Principalities |
| 211 | harrows_post | County of New Aldenmere | Broker's Reach | The Charter Principalities |
| 212 | harrows_claim | County of Harrow's Claim | Broker's Reach | The Charter Principalities |
| 213 | settlers_rest | County of Harrow's Claim | Broker's Reach | The Charter Principalities |
| 214 | new_veth | County of Harrow's Claim | Broker's Reach | The Charter Principalities |
| 215 | pioneer_span | County of Pioneer | Pioneer Marches | The Charter Principalities |
| 216 | deepmark | County of Pioneer | Pioneer Marches | The Charter Principalities |
| 217 | firstfall | County of Pioneer | Pioneer Marches | The Charter Principalities |
| 218 | trailhead | County of Trailhead | Pioneer Marches | The Charter Principalities |
| 219 | waystation | County of Trailhead | Pioneer Marches | The Charter Principalities |
| 220 | farsight | County of Trailhead | Pioneer Marches | The Charter Principalities |
| 221 | the_outpost | County of Outpost | Pioneer Marches | The Charter Principalities |
| 222 | frontier_span | County of Outpost | Pioneer Marches | The Charter Principalities |
| 223 | edgepost | County of Outpost | Pioneer Marches | The Charter Principalities |
| 224 | waymark | County of Outpost | Pioneer Marches | The Charter Principalities |
| 225 | halcyon_reach | County of Halcyon | Halcyon Strip | The Charter Principalities |
| 226 | serenfall | County of Halcyon | Halcyon Strip | The Charter Principalities |
| 227 | calmwatch | County of Halcyon | Halcyon Strip | The Charter Principalities |
| 228 | quietline | County of Halcyon | Halcyon Strip | The Charter Principalities |
| 229 | stillwater | County of Stillwater | Halcyon Strip | The Charter Principalities |
| 230 | peacewatch | County of Stillwater | Halcyon Strip | The Charter Principalities |
| 231 | solace_span | County of Stillwater | Halcyon Strip | The Charter Principalities |
| 232 | dawnhaven | County of Stillwater | Halcyon Strip | The Charter Principalities |
| 233 | chitterholm | County of Chitterholm | Warrens | The Outer Marches |
| 234 | rustspire | County of Chitterholm | Warrens | The Outer Marches |
| 235 | skarlforge | County of Chitterholm | Warrens | The Outer Marches |
| 236 | scrapyard | County of Scrapyard | Warrens | The Outer Marches |
| 237 | the_gnaw | County of Scrapyard | Warrens | The Outer Marches |
| 238 | the_burrow | County of Scrapyard | Warrens | The Outer Marches |
| 239 | txic_gate | County of Txic Gate | Warrens | The Outer Marches |
| 240 | gnaxtun | County of Txic Gate | Warrens | The Outer Marches |
| 241 | deepburrow | County of Txic Gate | Warrens | The Outer Marches |
| 242 | the_underworks | County of Txic Gate | Warrens | The Outer Marches |
| 243 | skrix_deep | County of Skrix Deep | Warrens | The Outer Marches |
| 244 | the_gnawing | County of Skrix Deep | Warrens | The Outer Marches |
| 245 | burrownest | County of Skrix Deep | Warrens | The Outer Marches |
| 246 | rust_hollow | County of Rust Hollow | Rust Verge | The Outer Marches |
| 247 | corrode | County of Rust Hollow | Rust Verge | The Outer Marches |
| 248 | scrapline | County of Rust Hollow | Rust Verge | The Outer Marches |
| 249 | ironwaste | County of Ironwaste | Rust Verge | The Outer Marches |
| 250 | the_decay | County of Ironwaste | Rust Verge | The Outer Marches |
| 251 | oxidespire | County of Ironwaste | Rust Verge | The Outer Marches |
| 252 | the_dead | County of the Dead | Dead Reach | The Outer Marches |
| 253 | derelict | County of the Dead | Dead Reach | The Outer Marches |
| 254 | wreckhold | County of Wreckhold | Dead Reach | The Outer Marches |
| 255 | the_silence | County of Wreckhold | Dead Reach | The Outer Marches |
| 256 | graveline | County of Graveline | Dead Reach | The Outer Marches |
| 257 | the_forgotten | County of Graveline | Dead Reach | The Outer Marches |
| 258 | hollowfield | County of Graveline | Dead Reach | The Outer Marches |
| 259 | ashen_span | County of Graveline | Dead Reach | The Outer Marches |
| 260 | uvrek | County of Uvrek | Uvrek | The Outer Marches |
| 261 | uvrek_span | County of Uvrek | Uvrek | The Outer Marches |
| 262 | uvrek_margin | County of Uvrek | Uvrek | The Outer Marches |
| 263 | vorshaan | County of Vorshaan | Uvrek | The Outer Marches |
| 264 | vorshaan_drift | County of Vorshaan | Uvrek | The Outer Marches |
| 265 | the_vorsway | County of Vorshaan | Uvrek | The Outer Marches |
| 266 | the_drifting | County of the Drifting | Uvrek | The Outer Marches |
| 267 | skeld_margin | County of the Drifting | Uvrek | The Outer Marches |
| 268 | outermark | County of the Drifting | Uvrek | The Outer Marches |
| 269 | the_fringe | County of the Drifting | Uvrek | The Outer Marches |
| 270 | vareks_edge | County of Varek's Edge | Varek's Silence | The Outer Marches |
| 271 | the_stillness | County of Varek's Edge | Varek's Silence | The Outer Marches |
| 272 | far_nothing | County of Varek's Edge | Varek's Silence | The Outer Marches |
| 273 | hollow_dark | County of the Hollow Dark | Varek's Silence | The Outer Marches |
| 274 | the_dim | County of the Hollow Dark | Varek's Silence | The Outer Marches |
| 275 | lost_signal | County of the Hollow Dark | Varek's Silence | The Outer Marches |
| 276 | pale_beyond | County of the Pale Beyond | Varek's Silence | The Outer Marches |
| 277 | the_uncharted | County of the Pale Beyond | Varek's Silence | The Outer Marches |
| 278 | deepwatch | County of the Pale Beyond | Varek's Silence | The Outer Marches |
| 279 | drifting_dark | County of the Drifting Dark | The Far Drift | The Outer Marches |
| 280 | the_current | County of the Drifting Dark | The Far Drift | The Outer Marches |
| 281 | far_margin | County of the Drifting Dark | The Far Drift | The Outer Marches |
| 282 | lost_reach | County of the Lost Reach | The Far Drift | The Outer Marches |
| 283 | adrift | County of the Lost Reach | The Far Drift | The Outer Marches |
| 284 | the_wander | County of the Lost Reach | The Far Drift | The Outer Marches |
| 285 | outer_pale | County of the Outer Pale | The Far Drift | The Outer Marches |
| 286 | the_scatter | County of the Outer Pale | The Far Drift | The Outer Marches |
| 287 | last_light | County of the Outer Pale | The Far Drift | The Outer Marches |
