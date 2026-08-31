# 866 AG — Bookmark Design Reference

> This document is the canonical reference for what the galaxy looks like at the mod's starting bookmark. All scripted content, history files, characters, and events should be consistent with this.

---

## Timeline Context

| Event | Year |
|---|---|
| Orrin's Grip — the cataclysm | 0 AG |
| Founding of New Cauldron (Mikey the Great) | 131 AG |
| Titan Exodus begins | 131 AG |
| New Cauldron's first election | 131 AG |
| Nikios Khanate: Mercenary Council founded | 600 AG |
| Broken Daimyo ancestors arrive in star systems | ~500 AG |
| Angelia founded by Aasimar divine pilgrims | ~150 AG |
| Nikios Khanate: War of Broken Hooves | ~800–840 AG |
| **► BOOKMARK: 866 AG - After the Crucible ◄** | **866 AG** |
| Hobgoblin Drift Wars in the Wastes | ~900 AG |
| Shatter Stance: Exodus of Shards | ~950 AG |
| Broken Daimyos: first unification attempt | ~920 AG |
| Myr Cluster Wars end | 1300 AG |
| Crime Wars | ~330 AG |
| Galactic League of States (informal) | 1650 AG |
| Orro Invasion of the Second Elrossi Imperium | ~1700 AG |

---

## Nation States at 866 AG

### New Cauldron
- **Government:** Democratic republic, elections every 5 years
- **Founded:** 131 AG by Mikey the Great (formerly Mikey Smalls)
- **Origin:** Survivors who crash-landed on the Titanworld in the ruins of one of the second era's capital cities - newly named 'The Cauldron' - the protective mountain peaks formed a "cauldron" around the wreckage and ruins, leading to it's name
- **Military:** Renowned mercenary legions hired across the galaxy; the Vault Stance serves as elite aristocratic guards
- **866 AG status:** Thriving, confident, ambitious. Entering the Myr Cluster Wars in early phase — their Mercenary Legions are being hired by multiple factions simultaneously
- **Key tension:** The Band of Cock mercenary guild's influence in government vs. pure democratic ideals
- **CK3 government type to design:** Republican/elective with mercenary tradition mechanics

### The Elrossi Imperium
- **Government:** Holy theocratic empire, inspired by the HRE and Imperial France
- **Faith:** Faith of Elross — order, light, sacred martial discipline
- **866 AG status:** Expansionist, holy, entering the Myr Cluster Wars via proxy (the Prince of Myr). Holy Orders serve as crusading forces. The Imperium at 866 is a First Imperium — the "Second" designation reflects a later reformation after collapse
- **Key tension:** Using a proxy leader in the Clusters to avoid domestic dissent vs. direct conquest ambitions
- **Holy sites to define:** Caer Myr (base of the Prince of Myr), Saint Argoth's Hold

### Gob-Ogre Trade League
- **Government:** Corporate oligarchy — 50 Trade Princes, council-led
- **866 AG status:** Aggressively entering the Myr Clusters. Their corporate armies are seizing territory. The external threat of Chad Orc warlord Karim Ibn Al Daveed is not yet realized (he razes Grand Kiln in 880 AG) — so at 866 they are at peak confidence before the coming catastrophe
- **Key tension:** Fifty Trade Princes each pursuing their own interests; infighting simmers beneath expansion
- **CK3 government type to design:** Corporate council with Trade Prince vassal mechanics

### Coldiron Caliphate
- **Government:** Theocratic Caliphate
- **866 AG status:** Faith-driven expansionists pressing into the Myr Clusters from their direction. Will lose the Battle of Lumina Verge to New Cauldron's Mercenary Legions in 885 AG — at 866 they are confident and advancing
- **Key tension:** Holy war justifications for expansion vs. pragmatic resource competition in the Clusters

### Nikios Khanate
- **Government:** Khanate — Khan + Mercenary Council
- **Species:** Centaur
- **866 AG status:** Recovering from the War of Broken Hooves (~800–840 AG). The new Khan has consolidated power but inter-clan distrust lingers. The Mercenary Council (founded 600 AG) remains the economic backbone. They are a Savage Space power — not in the Myr Cluster Wars directly, but selling mercenary contracts to all sides
- **Key tension:** Clan loyalty vs. centralized Khan authority; reliance on tribute payments from weakened neighbors

### Angelia
- **Government:** Conclave of Luminaries (warlords, prophets, clergy)
- **Species:** Aasimar
- **Faith:** Elross, Malvrick, and Yu (all three — more syncretic than the Elrossi Imperium's orthodoxy)
- **866 AG status:** Prosperous and pious. Celestial Hosts (militarized divisions) defend the Border Systems against constant Carrigore Space raids. Noble families are accumulating wealth — seeds of future decadence are sown but not yet visible. Aasimar paladins in golden armor are the iconic image
- **Key tension:** Holy idealism of the Conclave vs. noble family wealth concentration; Baphomet-worshippers are exiled as pariahs

### Broken Daimyos
- **Government:** Fragmented — independent daimyo city-states, no central authority
- **866 AG status:** Pre-unification fragmentation. Dozens of rival daimyos fight over star systems and orbital stations. No Sengoku Jidai has been formally declared yet at this date — that codification comes later. Mercenaries from the Shatter Stance and tiefling warlords exploit the chaos
- **Key tension:** Every daimyo wants unification — on their own terms. The first one to achieve it (Tokugari Yatsume, ~920 AG) is still 54 years away
- **CK3 parallel:** This plays most like vanilla CK3's Ireland or HRE — many equal-strength rulers with no dominant power

### The Shatter Stance
- **Government:** Loose exile alliance, not yet the Ironshard Concord
- **866 AG status:** Still in exile, scattered across the Devoid Systems. The formal Exodus of Shards is a few decades away (~950 AG). At 866 they are bitter, surviving, and beginning to clash with local warlords and alien species. Not yet a unified nation — more like scattered warbands that share a cultural identity
- **Key tension:** Survival and bitter resentment of New Cauldron vs. the chaos of their own fragmentation

---

## The Titan Exodus at 866 AG

The Titan Exodus is not a single event but an ongoing process. At 866 AG, the Titanworld still exists but is increasingly uninhabitable. Refugee fleets continue to arrive in settled space — some carrying entire cultures, others carrying only desperate survivors.

For gameplay, this means:
- Random events can fire where Exodus refugee fleets arrive in your systems
- Some arriving groups are organized (petty kingdoms, religious orders) — potential vassals or threats
- Others are ragged survivors — potential population boosts or destabilizing elements
- The Titan Exodus is a source of new characters, new cultures, and new conflicts throughout the early game

---

## Key 866 AG Scripting Priorities

1. **Bookmark characters** — all major rulers need stats, traits, and dynasty connections
2. **The Myr Cluster Wars** — a struggle system defining the early game's central conflict
3. **Titan Exodus events** — refugee arrival chain, fired from `on_yearly_pulse`, should be reworked so that refugees arriving can either be civilized (actual refugees) or barbaric (invaders) with different options/outcomes each
4. **Elrossi faith** — holy war mechanics, fervor, the Prince of Myr interaction
5. **New Cauldron republic government** — elective mechanics, mercenary contract system
6. **Opening story cycle** — introduces players to 866 AG via three framing events

---

## Lore Notes for Writers

- The Grip is 866 years in the past at this bookmark — it is history, not living memory, but its consequences are still everywhere. The fractured cosmos, the weakened gods, the freed titans — all stem from 0 AG
- Characters born with `eotg_grip_survivor` are carrying bloodline heritage, not personal experience
- "Titan" refers specifically to Orrin (Void) and Yu (Dream) — capital-T Titans. Lower-case "titan" can refer to large creatures or powerful beings
- The Galactic League of States does NOT exist at 866 AG. There is no galaxy-wide law, no neutral arbitrator, no shared military. This is the wild era
- New Cauldron's democratic culture is genuine — not a cynical facade. It is remarkable and beloved, which is why its mercenary military power doesn't feel contradictory to its citizens
