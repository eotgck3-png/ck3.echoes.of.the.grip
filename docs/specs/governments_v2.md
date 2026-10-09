# Spec: Governments v2: PMC, Corporation, Gob-Corp, Cartel

**Author:** eotg-architect, 2026-10-08. **Status:** draft for lore-keeper review, then scripter (Phase G1).
**Scope:** four governments: `eotg_pmc_government`, `eotg_corporation_government`, `eotg_gobcorp_government`, `eotg_cartel_government`. Fringe, New Cauldron and Elven Monarchy are out of scope. Nikios is deferred (invariant 9).
**Vanilla:** CK3 1.20.0.3. In this document, `G/` means `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/`.

**Keys confirmed.** The cartographer's assumed keys stand unchanged: `eotg_pmc_government`, `eotg_corporation_government`, `eotg_cartel_government`, `eotg_gobcorp_government`. They are v1's keys and carry the `eotg_` prefix (invariant 1).

---

## 1. Purpose & gate

These four governments run the mod's commercial and criminal realms: a private military company, a human corporate oligarchy, the goblin-and-ogre trade oligarchy, and a criminal enterprise that has become a state. Normally they are Gate 2 work. **The owner ruled on 2026-10-08 that they are a mod-exclusive exception, like cybernetics.** That means:
- they are built and tested before Gate 1, on the vanilla-map British Isles test sub-mod (`docs/test_submods/british_isles/`);
- mod script must not name any title, province, culture, faith or character. The engine decides which ruler holds which government from history data, and that data belongs to the test sub-mod (the cartographer's job, §12).

The work runs in two phases:
- **Phase G1, "playable"** (this spec, buildable now): each government loads, can be set in history, and plays sensibly for the player and the AI. G1 has no flavour events.
- **Phase G2, "deep"** (outline only, §14): the Gate 2 definition of done. That means a signature resource, a role ladder, decisions, events and interactions for each government. **New events need owner approval** (memory: event expansion is the owner's call).

**Not blocked.** The owner's gate ruling unblocks G1 and G2. Only G2 items that need real titles (named nations, bookmarks) wait for Gate 1.

---

## 2. Signature resource

**G1 has no flavour events**, so the rule that every flavour event moves the resource (invariant 5) has nothing to apply to yet. The resources are fixed here so that G2 content is built against them from its first event (v1 lesson 6). None of them is built in G1.

| Government | Signature resource (G2) | Type | Why |
|---|---|---|---|
| PMC | `eotg_pmc_standing`: the company's market reputation, 0 to 100 | character variable, on every PMC ruler at any tier | Robustness plan 0.2: the PMC's income and standing come from outside the realm. Completed contracts raise it; controversy and defeats lower it. |
| Corporation | `eotg_corp_board_influence`: the ruler's hold on the board, 0 to 100 | character variable, on every Corporation ruler | v1 design doc §3.4. A currency spent by major acts and earned by deals. |
| Gob-Corp | `eotg_gobcorp_market_share`: the Trade Prince's share of the market, 0 to 100 | character variable, on every Gob-Corp ruler | v1 design doc §2.3/§2.5. Vote weight is derived from it, so one number drives both the market and the vote. |
| Cartel | **Dread** (vanilla) | engine currency | v1 design doc §4.2. Engine-native, already shown in the UI, and AI-aware. The Cartel's G1 character modifier already makes dread decay faster (§5.4). |

G2 rule: every Gob-Corp, Corporation and PMC flavour event moves or reads its variable through one scripted effect per government (`eotg_<gov>_change_<resource>_effect`, clamped 0 to 100). Every Cartel event moves or reads `dread`.

---

## 3. Identifier table (Phase G1)

Owner = the agent who writes it. "Shared" means it is used by more than one government.

### 3.1 Script objects

| Type | Key(s) | Owner |
|---|---|---|
| government | `eotg_pmc_government`, `eotg_corporation_government`, `eotg_gobcorp_government`, `eotg_cartel_government` | scripter |
| government flag (identity) | `eotg_government_is_pmc`, `eotg_government_is_corporation`, `eotg_government_is_gobcorp`, `eotg_government_is_cartel` | scripter |
| government flag (shared family) | `eotg_government_is_corporate` (Corporation + Gob-Corp; v1 precedent, the only v1 government flag in real use) | scripter |
| succession law (group `succession_order_laws`) | `eotg_pmc_succession_law`, `eotg_corporation_succession_law`, `eotg_gobcorp_succession_law`, `eotg_cartel_succession_law` | scripter |
| subject contract group | `eotg_pmc_vassal`, `eotg_corporation_vassal`, `eotg_gobcorp_vassal`, `eotg_cartel_vassal` (v1 names kept) | scripter |
| subject contract (tax tree) | `eotg_pmc_contractor_fee`, `eotg_corporation_assessment`, `eotg_gobcorp_market_tithe`, `eotg_cartel_loyalty_tax` | scripter |
| subject contract (levy tree) | `eotg_pmc_operational_levy`, `eotg_corporation_security_levy`, `eotg_gobcorp_security_levy`, `eotg_cartel_territory_tribute` | scripter |
| obligation levels | `<contract>_none`, `_low`, `_standard`, `_high`, `_extortionate` for each of the 8 contracts above (40 keys) | scripter |
| flavourization: title rank | `eotg_<tier>_<gov>`, where tier ∈ {`barony`,`county`,`duchy`,`kingdom`,`empire`} and gov ∈ {`pmc`,`corporation`,`gobcorp`,`cartel`} (20 keys, e.g. `eotg_duchy_pmc`) | scripter |
| flavourization: vassal rank | `eotg_<gov>_<tier>_male` / `_female` (5 tiers × 2 genders × 4 = 40 keys, e.g. `eotg_pmc_duchy_male`) | scripter |
| flavourization: top rank (independent) | `eotg_<gov>_top_<tier>_male` / `_female` for tiers county to empire (4 × 2 × 4 = 32 keys, e.g. `eotg_pmc_top_duchy_male`) | scripter |
| customizable loc (vanilla key override) | `KnightCulture` (its 7 vanilla children inherit through `parent =`, so they are not redefined) | scripter |
| scripted trigger | `eotg_gov_knight_realm_is_pmc` / `_corporation` / `_gobcorp` / `_cartel` (character: the character's own government, or an unlanded character's employer's) | scripter |
| scripted effect | `eotg_gov_ensure_succession_law_effect` (character: adds the government's own succession law if the ruler has none valid; §7.2) | scripter |
| on_action (mod) | `eotg_gov_on_game_start`, `eotg_gov_on_government_change` | scripter |
| decision (debug only) | `eotg_decision_gov_debug_become_pmc` / `_corporation` / `_gobcorp` / `_cartel`, `eotg_decision_gov_debug_become_feudal` | scripter |
| government icon (placeholder) | `gfx/interface/icons/government_types/eotg_pmc_government.dds` (and the other three) | orchestrator (copied from vanilla; real art is human debt) |

### 3.2 Loc keys (localizer; full list in §9)
Government display keys, law keys, contract keys, flavourization keys, knight terms (`eotg_knight_<term>` + 7 suffix variants each), debug decision keys.

### 3.3 Reserved for G2 (named now, not built)
`eotg_pmc_standing`, `eotg_corp_board_influence`, `eotg_gobcorp_market_share` (variables); the role-ladder triggers in §14.2; event namespaces `eotg_pmc`, `eotg_corp`, `eotg_gobcorp`, `eotg_cartel`. Loc keys follow `eotg_<ns>_NNNN_t` / `_desc` / `_a`.

---

## 4. File placement

| File | Contents |
|---|---|
| `common/governments/eotg_pmc_government.txt` (+ `_corporation_`, `_gobcorp_`, `_cartel_`) | one government per file (v1 and `eotg_unclaimed_government.txt` precedent) |
| `common/subject_contracts/contracts/eotg_government_obligations.txt` | the 8 contracts |
| `common/subject_contracts/groups/eotg_government_contract_groups.txt` | the 4 groups |
| `common/laws/eotg_government_succession_laws.txt` | the 4 succession laws (1.20 laws carry `law_group_type`, so this file adds to the vanilla group without touching it) |
| `common/flavorization/eotg_government_flavorization.txt` | the 92 rank entries |
| `common/customizable_localization/eotg_knight_culture.txt` | the `KnightCulture` override |
| `common/scripted_triggers/eotg_government_triggers.txt` | knight-realm triggers |
| `common/scripted_effects/eotg_government_effects.txt` | succession safety net |
| `common/on_action/eotg_government_on_actions.txt` | additive hooks (§7) |
| `common/decisions/eotg_government_debug_decisions.txt` | 5 debug decisions |
| `localization/english/eotg_government_l_english.yml` | all G1 loc (UTF-8 with one BOM) |
| `gfx/interface/icons/government_types/eotg_*_government.dds` | placeholder icons |

**Orchestrator: add these to the `CLAUDE.md` placement list:** `common/subject_contracts/contracts/`, `common/subject_contracts/groups/`, `common/flavorization/`, `gfx/interface/icons/government_types/`. These folders are new to v2. No `replace_path` for any of them (invariant 3).

---

## 5. The four governments (Phase G1)

### 5.0 Fields shared by all four, with precedent

Every field below is listed in `G/common/governments/_governments.info`, or (`allow_accolades`, `realm_mask_*`, `royal_court`) used verbatim by vanilla 1.20 governments. **Tiger 1.17 and PX don't validate 1.20 government fields.** QA checks these blocks by hand against the cited lines, as for `eotg_unclaimed_government` (see that file's header).

| Field | Value (all four) | Precedent | Why |
|---|---|---|---|
| `government_rules.create_cadet_branches` | `yes` | feudal `00_government_types.txt:7` | playable and dynastic |
| `government_rules.rulers_should_have_dynasty` | `yes` | feudal :8, clan :98, tribal :189, admin :453; every playable vanilla government | **Deviation from v1 (`no`).** A lowborn ruler without a dynasty ends the game for the player at death. Every unplayable vanilla type (republic, mercenary, holy order) leaves it unset. |
| `government_rules.dynasty_named_realms` | `no` | admin :454, celestial :798 | the realm takes its title's name, not the house name |
| `government_rules.legitimacy` | `yes` | feudal :10; default `yes` (`.info:49`) | **Deviation from v1 for the Cartel (`no`).** No playable landed vanilla government sets `no`. v1's three `add_legitimacy` calls went silently inert under `no` (robustness plan F1b). The Cartel gets its identity from dread (§5.4). |
| `government_rules.allow_accolades` | `yes` | feudal :11, admin :469, mandala :940 | robustness plan 2.1; the PMC's Operators especially |
| `government_rules.use_as_base_on_landed` | `yes` | admin :458, celestial :801, mandala :930; `.info:73-77` | an heir who is landed for the first time takes the predecessor's government |
| `government_rules.sticky_government` | `yes` | admin :462, nomad :647, celestial :805 | the government survives title changes |
| `government_rules.use_as_base_on_rank_up` | **not set** (default `no`) | — | so a feudal conqueror of a PMC kingdom does not turn PMC; the governments spread only by inheritance and grants |
| `fallback` | **not set** | vanilla priorities start at 1 (`:16, :110, :480, :830`) | never a fallback government |
| `primary_heritages`, `preferred_religions` | **not set** | — | map-agnostic. They also never make the engine prefer these governments |
| `can_get_government` | **not set** in G1 | feudal, clan, republic and the test sub-mod's offmap government all omit it | A guard risks heirs failing it and dropping to feudal at succession. **Leakage** (random new castle rulers getting a mod government) is checked in game (V-G11). If V-G11 finds leakage, G1.1 adds the guard in §5.6. |
| `mechanic_type` | **not set** | republic `:64-92` has none | 1.20 mechanics (administrative influence, nomad herds, mandala piety) are hard-coded to their mechanic and need subsystems the mod lacks (robustness plan 2.6). Influence for the Corporation is a G2 probe (§14.5). |
| `royal_court` | `any` | feudal :14, clan :105, admin :472 | a kingdom-tier ruler gets the court screen, as feudal ones do |
| `vassal_contract_group` | `eotg_<gov>_vassal` (§6) | feudal :22 | own obligations, generic vassal-contract UI (§6.3) |
| `ai = { use_legends = yes }` | — | feudal :24-26 | otherwise the AI defaults, which are vanilla's settled-ruler behaviour |
| flags, always present | `government_is_settled`, `government_uses_domain_limit`, `government_uses_crown_authority` | feudal :29-35 | **`government_uses_crown_authority` is load-bearing.** The crown-authority law group requires it (`G/common/law_groups/00_realm_law_groups.txt:2`). Without crown authority a ruler can never change succession law, because `can_change_succession_laws` comes from crown authority 2 (`00_realm_laws.txt:147`, read by `00_legal_triggers.txt:41-46`). Revocation and vassal-war rules and tributaries (`can_have_tributaries`, crown authority 1, `:64`) all come from it too. |
| flags, never present | `government_is_feudal`, `government_is_clan`, `government_is_republic`, `government_is_mercenary` | — | **`government_is_feudal`** is read 369 times in 93 vanilla files (feudal special contracts, feudal events, partition laws). Carrying it would make these governments feudal in everything but name. The other three are unplayable labels (`G/localization/english/government_l_english.yml:272-285`). |
| `color` / `realm_mask_offset` / `realm_mask_scale` | per government (below) | feudal :59-61 | government map mode. The colours are checked against every vanilla colour (v1's Cartel colour copied tribal's dark red, `:251`). |

**Holdings follow two vanilla shapes, verbatim:**
- **Castle governments (PMC, Cartel)** use feudal's (`:18-20`): `primary_holding = castle_holding`, `valid_holdings = { temple_citadel_holding }`, `required_county_holdings = { castle_holding city_holding church_holding }`.
- **City governments (Corporation, Gob-Corp)** use republic's (`:65-67`): `primary_holding = city_holding`, `valid_holdings = { castle_holding }`, `required_county_holdings = { city_holding castle_holding church_holding }`.
- **Deviation from v1:** v1 gave the PMC and Cartel `valid_holdings = { city_holding }` and a castle-only `required_county_holdings`. That combination appears nowhere in vanilla. The vanilla shapes are known to work with the AI's building and baron generation. City baronies in a PMC realm therefore get republic burghers, as in a feudal one; V-G20 records it.

### 5.1 PMC: `eotg_pmc_government`

**Identity.** A military state run as a business: a command hierarchy that sells force. In v1 it is the proto-corporate foundation, standing to the Corporation as tribal stands to feudal, and generic across races (`EOTG_Government_Design_Document_v2.md` §6). Knights are **Operators** (v1 header and loc). Its v1 identity is contracts: income and standing earned outside the realm (robustness plan 0.2). **Canon is thin** (LQ3). The 866 sources show mercenary bands (the Laughing Blades, SETTING LORE body :361) and hired legions (New Cauldron's, in the unreviewed `docs/lore/NATIONS_AT_866_AG.md`), but no named PMC state.

**Fields beyond §5.0:**
```
government_rules += { disable_regnal_numbers = yes }    # celestial :816, meritocratic :1259; robustness plan 2.2 ("a command, not a line of kings")
court_generate_commanders = 2                            # .info:427-432 (int multiplier); mercenary/holy order use 5 (:335, :373)
character_modifier = {
    knight_limit = 2                                     # landless adventurer :594 (+2)
    knight_effectiveness_mult = 0.15                     # v1
    men_at_arms_maintenance = -0.1                       # admin :514 uses the same modifier (+0.5)
    mercenary_hire_cost_mult = -0.2                      # admin :513 (+2); the PMC knows the market
}
flags = { eotg_government_is_pmc  government_is_settled  government_uses_domain_limit  government_uses_crown_authority }
color = hsv{ 0.20 0.60 0.55 }                            # olive drab; v1's orange clashed with steppe_admin {255 110 40} and meritocratic {250 100 0}
realm_mask_offset = { 0.0 0.01 }  realm_mask_scale = { 1 1 }   # feudal :60-61
```
Holdings: the castle shape. Succession: `eotg_pmc_succession_law` (§7.1). Contracts: `eotg_pmc_vassal` (§6).

**Coupling with existing systems (G1: none built; all optional):**
- **Cybernetics, "a hired crew between contracts"** (`cybernetics_v2_kingpin.md` §5.2.1, `flag:hired`): G2 may raise the hired-kind weight under a PMC liege. That would be one weight line in the kingpin roll, behind `government_has_flag = eotg_government_is_pmc`.
- **The Iron Retinue** (cybernetics Phase 5) is about knights. Under a PMC its loc already reads "Operators" through `Custom('KnightCulture…')` (CB-48), with no edit.
- **Frontier mercenary organizations** (`frontier_v3.md` §5): a PMC ruler can already sponsor through `eotg_frontier_can_sponsor` (landed count or above). G2 may add a PMC branch to *Guns for Hire* (.040).
- **Unclaimed:** passes `eotg_unclaimed_can_claim` (`eotg_unclaimed_triggers.txt:67-74`). The AI throttle reads `domain_limit`, which the `government_uses_domain_limit` flag guarantees.

**Risks and mitigations:**

| Risk (source) | Mitigation |
|---|---|
| The top role exists only at empire tier (v1 `eotg_st_is_contractor_general` = `highest_held_title_tier = tier_empire`, `eotg_pmc_triggers.txt:30-33`). The test PMC is an independent **duke**, so it would read "Field Director". | §8: the top rank goes to any independent ruler, at any tier. The G2 role ladder is relative (§14.2). |
| PMC knights are "Champion"/"Fāris" today (CB-48) | §10 override |
| AI over-recruits or goes bankrupt with cheap MAA (−10% maintenance) | small modifier; V-G12 watches gold over 50 years |

**V-G items:** V-G1–V-G12, V-G14 (accolades), V-G18–V-G20.

### 5.2 Corporation: `eotg_corporation_government`

**Identity.** Human corporate oligarchy, polished at the top and cut-throat below: account directors and operations chiefs scheme against each other, and the board above them plays a slow game of influence (v1 design doc §3, §3.2). Its v1 identity is board influence as a spendable political currency. Canon exemplars at 866 include P&D Corporate Space (Board of Directors, in the unreviewed `NATIONS_AT_866_AG.md` :237-246). Helix's 866 structure is **not** a board with a CEO (ERRATA "HELIX CORPORATION"). Government text names no nation (§11).

**Fields beyond §5.0:**
```
government_rules += { disable_regnal_numbers = yes }    # as PMC; corporations don't number their chief executives
character_modifier = {
    monthly_income_mult = 0.05                           # v1; vanilla gov use: herder/unclaimed shape
    diplomacy = 1                                        # v1; skills are generic modifiers (.info:721-733)
    build_gold_cost = -0.1
    levy_size = -0.15                                    # admin :502 (-0.5); security is a line item, not a host
}
flags = { eotg_government_is_corporation  eotg_government_is_corporate  government_is_settled  government_uses_domain_limit  government_uses_crown_authority }
color = hsv{ 0.50 0.75 0.75 }                            # teal; v1's 0.58 sat close to feudal's blue (0.67)
realm_mask_offset = { 0.0 -0.01 }  realm_mask_scale = { 1 1 }  # republic :90-91
```
Holdings: the city shape. Succession: `eotg_corporation_succession_law`. Contracts: `eotg_corporation_vassal`.

**Coupling (G1: none built):**
- **Cybernetics clinics** (`cybernetics_v2_realm.md`): the augmentation realm laws have no `required_government_flag` (`:198`), so a Corporation can already hold them. G2 candidates: a Corporation discount on the clinic of record; a `flag:front` kingpin weight. **Never name P&D or any 866 implant player** (cybernetics §5.3 never-name list; LQ4).
- **Frontier, "a corporation as a Sponsor"** (`frontier_v3.md` §7): the documented hook (`eotg_frontier_offer_backing_effect`) is how G2 plugs in. Nothing is built in G1.
- **Unclaimed:** as the PMC.

**Risks and mitigations:**

| Risk | Mitigation |
|---|---|
| A city-primary **playable** government is untested in vanilla (republic is unplayable) | V-G3 and V-G17: play it, build, hold castles. The fallback, if broken, is the castle shape (one field change). |
| The capital barony is a castle in vanilla history (Brittany) | §12: the cartographer makes the test capital a city |
| Castle barons under a Corporation take a government the engine chooses | V-G20 records the result. Either result is acceptable for G1. |

**V-G items:** V-G1–V-G13 except V-G13 (tributaries), V-G15 (royal court, kingdom tier), V-G17, V-G20.

### 5.3 Gob-Corp: `eotg_gobcorp_government`

**Identity.** The goblin-and-ogre trade oligarchy: fifty Trade Princes in factional market competition under a precarious Director-General, where internal politics are as dangerous as external war (v1 design doc §2). Canon at 866: the Gob-Ogre Trade League is under Karim's attack from 851 (REVIEW_866), "corporate oligarchy, 50 Trade Princes, council-led" (`866_bookmark_design.md:48-52`). Whether a Director-General exists at 866 is LQ2. Its v1 identity is vote weight: power is bought and counted.

**Fields beyond §5.0:**
```
government_rules += { disable_regnal_numbers = yes }
character_modifier = {
    monthly_income_mult = 0.1                            # v1
    diplomacy = -1                                       # v1
    levy_size = -0.1
    mercenary_hire_cost_mult = -0.15                     # the Princes hoard private mercenary armies (unreviewed NATIONS :55; LQ2)
}
ai = { use_legends = yes  arrange_marriage = yes }       # v1 had arrange_marriage; yes is the default (.info:603)
flags = { eotg_government_is_gobcorp  eotg_government_is_corporate  government_is_settled  government_uses_domain_limit  government_uses_crown_authority }
color = hsv{ 0.10 0.85 0.60 }                            # brass; v1's 0.12/0.90/0.75 sat near celestial's yellow {250 230 10}
realm_mask_offset = { 0.0 -0.01 }  realm_mask_scale = { 1 1 }  # republic :90-91
```
Holdings: the city shape. Succession: `eotg_gobcorp_succession_law`. Contracts: `eotg_gobcorp_vassal`.

**Coupling (G1: none):**
- **Frontier trade network** (`frontier_v3.md` §7, `eotg_frontier_set_trade_network_effect`) is the natural G2 consumer of `eotg_gobcorp_market_share`.
- **Unclaimed:** as the PMC.

**Risks:** as the Corporation (the city shape). Also, v1's shared `eotg_market_faction_cycle` reached only Corporation and Gob-Corp, through `eotg_government_is_corporate` (robustness plan 2.2). The flag is kept so a G2 lift still works.

**V-G items:** as the Corporation, without V-G15 (the test Gob-Corp is a duke).

### 5.4 Cartel: `eotg_cartel_government`

**Identity.** A criminal enterprise that achieved statehood. Dread is the currency of power, and the top of the organization is always under threat from within (v1 design doc §4). It expands by **tribute, not raids**: it puts independent neighbours on a payment schedule (v1 robustness plan 1.1, 2.2). **Canon correction (LQ1):** v1 named the Slate Syndicate as the exemplar. The Slate Syndicate is post-866 (`Third era Nations.md:1403-1405`; unreviewed NATIONS :720 gives 1400 AG). At 866 the land is the Concrete Cartel's ("Under-Bosses of the Concrete Board", NATIONS :136-145). The Concrete Cartel is on the cybernetics never-name list. The government text names no nation.

**Fields beyond §5.0:**
```
government_rules += {
    ask_for_tribute = yes                                # mandala :934; enables offer_tributary_status_interaction
                                                         # (G/common/character_interactions/00_tributary_interactions.txt:4456-4480,
                                                         #  is_available: government_allows = ask_for_tribute; no DLC gate)
    count_tributaries_for_title_requirements = yes       # mandala :938
}
character_modifier = {
    intrigue = 2                                         # v1
    diplomacy = -2                                       # v1
    dread_gain_mult = 0.25
    dread_decay_mult = 0.25                              # v1 used dread_decay_add (defined but used once in vanilla); _mult is the common form (59 uses)
}
flags = { eotg_government_is_cartel  government_is_settled  government_uses_domain_limit  government_uses_crown_authority }
color = hsv{ 0.92 0.80 0.55 }                            # crimson; v1's hsv{0.0 0.85 0.35} duplicated tribal hsv{0.02 0.75 0.36} (:251)
realm_mask_offset = { 0.0 0.01 }  realm_mask_scale = { 1 1 }   # feudal
```
**No `deny_powerful_vassal`.** It was rejected in v1 for design reasons (robustness plan 2.2): the Cartel's drama needs strong internal bosses. **No `government_can_raid_rule`** (v1 1.1). **Tributaries need crown authority ≥ 1**: `can_have_tributaries_trigger` reads the realm-law flag `can_have_tributaries` (`G/common/scripted_triggers/mpo_scripted_triggers.txt:912-916`), and crown authority 1, the group default (`00_realm_law_groups.txt:3`), grants it (`00_realm_laws.txt:64`). A Cartel that drops to crown authority 0 loses the interaction, as vanilla intends.

Holdings: the castle shape. Succession: `eotg_cartel_succession_law`. Contracts: `eotg_cartel_vassal`. The tributary contract is vanilla's `tributary_settled` (`G/common/subject_contracts/groups/subject_contract_groups.txt:72-86`).

**Coupling (G1: none):**
- **Cybernetics syndicates, Patron and Kingpin** (`cybernetics_v2_kingpin.md` §5.1.3, §5.2.1): G2 may tilt kingpin kind weights under a Cartel liege (crew ×1.5, the same mechanism as the Ban law). **The syndicate kind stays Patron-only** (ruling, index §5 item 3). The generated syndicate names are canon syndicates, and a Cartel government must not be read as one of them (LQ6).
- **Unclaimed:** placeholders carry `cannot_be_vassal_or_liege`, so they are never tributary targets (`00_tributary_interactions.txt` `is_shown`). Tribute works only on real independent rulers. In the test, those are the Spain pockets (§12).

**Risks:**

| Risk | Mitigation |
|---|---|
| The AI spams tributary offers or over-extends | vanilla interaction AI, unchanged; V-G13 and V-G12 |
| Faster dread decay makes the AI ruler permanently low-dread and weak | modest +25%; V-G12 |
| Rank vocabulary ("Underboss", "Boss") clashes with the cybernetics "no mafia vocabulary" rule (B2) | LQ6. The rule binds the kingpin chain; whether it binds this government is for the lore-keeper to rule. |

**V-G items:** V-G1–V-G13, V-G15.

### 5.5 Vanilla precedent summary (file:line)
- Government shapes: `G/common/governments/00_government_types.txt` feudal :5-62, republic :64-92, admin :450-558, celestial :794-920, mandala :922-1099; field spec `_governments.info:1-719`.
- The project's own custom-government precedent: `common/governments/eotg_unclaimed_government.txt` (header) and `docs/test_submods/british_isles/common/governments/eotg_test_bi_offmap_government.txt` (use_as_base_on_landed + sticky for heir continuity).
- **Contradiction reported:** the ck3-modding skill's `governments.md` shows a pre-1.15 shape (rules at the top level, a `vassal_contract = { }` list). Vanilla 1.20 uses `government_rules = { }` and `vassal_contract_group`. **Vanilla wins.** The skill should be corrected upstream.

### 5.6 G1.1 fallback, only if V-G11 shows leakage: `can_get_government`
```
can_get_government = {
    OR = {
        government_has_flag = eotg_government_is_<gov>               # keeps it on re-evaluation
        liege ?= { government_has_flag = eotg_government_is_<gov> } # mandala :951-954 shape
        employer ?= { government_has_flag = eotg_government_is_<gov> }
        has_character_flag = eotg_gov_grant_<gov>                   # set by the debug and G2 adoption effects before change_government
    }
}
```
Not built in G1: if it is wrong, it breaks the heir path, which is worse than leakage.

---

## 6. Vassal contracts

### 6.1 Groups (shape: `G/common/subject_contracts/groups/subject_contract_groups.txt:1-16`)
```
eotg_pmc_vassal         = { contracts = { eotg_pmc_contractor_fee        eotg_pmc_operational_levy     war_declaration_rights council_rights title_revocation_rights } }
eotg_corporation_vassal = { contracts = { eotg_corporation_assessment    eotg_corporation_security_levy war_declaration_rights council_rights title_revocation_rights } }
eotg_gobcorp_vassal     = { contracts = { eotg_gobcorp_market_tithe      eotg_gobcorp_security_levy    war_declaration_rights council_rights title_revocation_rights } }
eotg_cartel_vassal      = { contracts = { eotg_cartel_loyalty_tax        eotg_cartel_territory_tribute war_declaration_rights council_rights title_revocation_rights } }
```
- **The three vanilla rights are generic.** `war_declaration_rights` has no `is_shown`. `council_rights` hides only for nomad lieges, and `title_revocation_rights` only on a jizya faith split (`G/common/subject_contracts/contracts/special_contracts.txt:476-580`).
- **Excluded:**
  - `special_contract` and `fortification_rights`/`coinage_rights`: feudal economy content, `government_is_feudal` ×10 in `special_contracts.txt`;
  - `succession_rights`: only shown with `can_have_confederate_partition_succession_law_trigger`, which needs feudal or tribal, `:443-446`;
  - `religious_rights`, `jizya`, `kurultai`: faith- or nomad-specific.
- v1's third obligations (board seat rights, enforcement rights, field commission) are **G2**. Each sets a flag that only G2 content reads.

### 6.2 Contracts (shape: `G/common/subject_contracts/contracts/feudal.txt:128-190`, `feudal_government_levies`)
**Copy the levy tree's shape for both trees**, with fixed numbers. Feudal's tax tree computes its AI desire through `government_has_flag = government_is_feudal` branches (`feudal.txt:29-115`), which never fire for these governments. For each contract:
- `display_mode = tree`; `icon = gold_icon` for the tax tree, `icon = soldier_icon` for the levy tree (v1 used both);
- 5 levels, `_none` → `_extortionate`, chained by `parent`, at `position = { 0..4 0 }`;
- copy `subject_opinion`, `ai_liege_desire`, `ai_subject_desire`, `score` and `flag` **by position** from `feudal_government_levies` (`:133-190`): exempt +10/1/5/2, low +5/2/4/1, normal default 0/3/3/0, high −15/4/2/−1 with `flag = obligation_high_levies`, extortionate −25/5/…;
- for tax trees, use the matching feudal tax flags at the same positions (the scripter copies them from `feudal.txt:1-127`). Vanilla AI and opinion logic read these flags.

| Contract | none | low | standard (**default**) | high | extortionate | Identity |
|---|---|---|---|---|---|---|
| `eotg_pmc_contractor_fee` (tax) | 0 | 0.025 | **0.05** | 0.10 | 0.15 | low cash |
| `eotg_pmc_operational_levy` (levies) | 0 | 0.15 | **0.35** | 0.45 | 0.6 | troops owed |
| `eotg_corporation_assessment` (tax) | 0 | 0.05 | **0.15** | 0.20 | 0.25 | cash owed |
| `eotg_corporation_security_levy` (levies) | 0 | 0.05 | **0.10** | 0.20 | 0.30 | few troops |
| `eotg_gobcorp_market_tithe` (tax) | 0 | 0.05 | **0.125** | 0.175 | 0.225 | cash |
| `eotg_gobcorp_security_levy` (levies) | 0 | 0.05 | **0.15** | 0.25 | 0.35 | |
| `eotg_cartel_loyalty_tax` (tax) | 0 | 0.05 | **0.10** | 0.20 | 0.30 | the steep top end is the "loyalty tax" |
| `eotg_cartel_territory_tribute` (levies) | 0 | 0.10 | **0.25** | 0.35 | 0.5 | feudal-like |

Feudal reference: taxes 0 / 0.025 / **0.10** / 0.15 / 0.25 (`G/common/script_values/00_goverment_values.txt:75-79`); levies 0 / 0.1 / **0.25** / 0.35 / 0.5. **These numbers are first-pass balance.** V-G12 is the check.

### 6.3 The modify-contract UI
`liege_modify_vassal_contract_interaction` and `vassal_modify_vassal_contract_interaction` are shown for any ruler whose contract has modifiable obligations, unless the government is administrative or nomadic (`G/common/character_interactions/00_modifiy_vassal_contract.txt:15-24, 327-337`). No override is needed.

---

## 7. Wiring

### 7.1 Succession laws (shape: `G/common/laws/00_succession_laws.txt:249-347`, `single_heir_succession_law`)

**Why the mod needs its own:**
- Every vanilla realm succession law is unavailable or unsafe for a government that isn't feudal or clan:
  - partition and high partition need `government_is_feudal`, `_clan` or `_japan_feudal` (`G/common/scripted_triggers/00_law_triggers.txt:268-280`);
  - city succession needs `government_is_republic` (`:589-591`), and generates a successor: unplayable;
  - appointment and acclamation need the administrative mechanic (`:641-670`);
  - single heir needs the culture innovation `innovation_primogeniture` (`:343-370`). A map-agnostic government can't depend on a culture's innovations.
- So a ruler of these governments could otherwise be left with **no valid succession law**.

Four laws, one per government (separate names for the UI). Each:
```
eotg_<gov>_succession_law = {
    law_group_type = succession_order_laws        # vanilla group, G/common/law_groups/00_succession_law_groups.txt:1
    index = <50..53>                               # above vanilla's range (the scripter checks for no collision)
    potential   = { government_has_flag = eotg_government_is_<gov> }
    can_have    = { government_has_flag = eotg_government_is_<gov> }
    can_keep    = { government_has_flag = eotg_government_is_<gov> }
    can_pass    = { can_change_succession_law_trigger = yes }    # vanilla :270, G/common/scripted_triggers/00_legal_triggers.txt:49
    should_start_with = { government_has_flag = eotg_government_is_<gov> }
    succession = { order_of_succession = inheritance  traversal_order = children  rank = oldest  title_division = single_heir }
    flag = advanced_succession_law                 # as single_heir :303
    pass_cost   = { prestige = change_succession_law_prestige_cost }
    revoke_cost = { prestige = change_succession_law_prestige_cost }
    ai_will_do  = { value = 3 }                    # as single_heir :330-332
}
```
- **Single heir, not partition.** Partition fragments AI realms in a 4-realm test and isn't the identity of any of the four governments.
- Board elections, wealth votes and violent succession are **G2**, as title succession laws with `order_of_succession = election` and an `election_type` in `common/succession_election/` (shape: `G/common/laws/01_title_succession_laws.txt:2-34`, `feudal_elective_succession_law`).
- The vanilla gender law (`succession_gender_laws`, default `male_preference_law`) is unchanged.
- **The vanilla single heir law stays available** when the culture has the innovation, so players may pick either.

### 7.2 Safety net (additive on_actions, invariant 4)
The default-law rule ("the first law in definition order whose `should_start_with` is true", `G/common/laws/_laws.info:300-308`) puts vanilla's partition law ahead of the mod's. Whether the engine skips it on `can_have` is not documented. Vanilla itself forces laws after setup with the same effect (`G/common/on_action/game_start.txt:2503`, `add_realm_law_skip_effects = theocratic_elective_succession_law`).

```
# common/on_action/eotg_government_on_actions.txt
on_game_start          = { on_actions = { eotg_gov_on_game_start } }          # vanilla G/common/on_action/game_start.txt
on_government_change   = { on_actions = { eotg_gov_on_government_change } }   # vanilla G/common/on_action/government_on_actions.txt:4 (root = character)

eotg_gov_on_game_start = {
    effect = {
        every_ruler = {
            limit = {
                OR = {
                    government_has_flag = eotg_government_is_pmc
                    government_has_flag = eotg_government_is_corporation
                    government_has_flag = eotg_government_is_gobcorp
                    government_has_flag = eotg_government_is_cartel
                }
            }
            eotg_gov_ensure_succession_law_effect = yes
        }
    }
}
eotg_gov_on_government_change = { effect = { eotg_gov_ensure_succession_law_effect = yes } }
```

`eotg_gov_ensure_succession_law_effect` (character scope): for each government, `if` the ruler has that government's flag and has neither `eotg_<gov>_succession_law` nor `single_heir_succession_law`, then `add_realm_law_skip_effects = eotg_<gov>_succession_law`. **No cooldown** is involved, so the cooldown-authority rule (invariant 4) doesn't apply. No event is fired.

**Tier gating:** these are not content pulses. They run on every ruler of the four governments at every tier, which is the role-ladder rule (v1 lesson 4) in its simplest form.

### 7.3 Debug decisions (`debug_only = yes`; shape: `common/decisions/eotg_unclaimed_decisions.txt:9-24`)
- `eotg_decision_gov_debug_become_<gov>` (4): `is_shown = { debug_only = yes  is_landed = yes  NOT = { government_has_flag = eotg_government_is_<gov> } }`. The effect is `change_government = eotg_<gov>_government`. The on_change hook then sets the law.
- `eotg_decision_gov_debug_become_feudal`: back to `feudal_government`, which tests `can_keep` dropping the mod law (V-G16).
- `ai_check_interval_by_tier` is 0 at every tier, as in the precedent.

These decisions are test tools and are not reachable in a normal game.

---

## 8. Rank and realm names (flavourization)

**Shape:** `G/common/flavorization/00_title_holders.txt`: `count_feudal_male` :8518-8525, `county_feudal` :8534-8539, `count_republic_male_*` with `top_liege = no` :3415-3426, and admin `priority = 50` :10419-10428. Field spec: ck3-modding `reference/common/flavorization/_flavourization.info`.

**Rules:**
- Every entry sets `governments = { eotg_<gov>_government }` and `flavourization_rules = { top_liege = no }`, so the **character's own** government counts, not the top liege's. A Corporation vassal of a feudal king is named as a Corporation ruler. (The default `top_liege = yes` would name him from the king's government, `_flavourization.info` "top_liege".)
- **Title rank** (`type = title`, tiers barony to empire): `priority = 60`.
- **Vassal rank** (`type = character`, `special = holder`, `gender` male or female, tiers barony to empire): `priority = 60`, plus `only_vassals = yes`.
- **Top rank** (the same, tiers county to empire): `priority = 61`, plus `only_independent = yes`. **The independent ruler gets the top name at any tier.** This is the correction to v1's absolute ladder.
- No `name_lists` or `heritages`: map-agnostic. Priority 60 beats every vanilla culture entry, which all list vanilla governments anyway.

**Proposed names (all are LQ5, for the lore-keeper to confirm or replace).** Female keys default to the same word unless the lore-keeper supplies a form. If the lore-keeper vetoes a title-rank word, that entry is dropped and the vanilla word shows.

| | Barony | County | Duchy | Kingdom | Empire | **Top (independent, any tier)** |
|---|---|---|---|---|---|---|
| PMC ruler | Post Commander | Contractor | Field Director | Executive Commander | — | **Contractor-General** |
| PMC title | Garrison | Command | Theatre | Field Army | Company | |
| Corporation ruler | Site Manager | Account Director | Operations Chief | Regional Director | — | **CEO** |
| Corporation title | Site | Branch | Division | Group | Conglomerate | |
| Gob-Corp ruler | Works Boss | Trade Prince | Trade Prince | Merchant Lord | — | **Director-General** |
| Gob-Corp title | Works | Concession | Monopoly | Bloc | League | |
| Cartel ruler | Den Keeper | Street Lord | Underboss | Boss | — | **Grand Underlord** |
| Cartel title | Den | Turf | Racket | Outfit | Cartel | |

- Ruler ranks at county to kingdom are v1's role ladder (robustness plan "The role ladder that already exists"). Barony ranks and all title ranks are new proposals.
- An empire-tier vassal is impossible, so the vassal entry at empire exists only for spouses. It reuses the top word.
- **Glossary guard:** none of these words may be one of the glossary's tier words (System, Region, Sector, Expanse, Cluster; `OLD PROJECT VERSION/docs/localization_crusade.md:15-27`). This table passes. "Directorate" was avoided because New Cauldron uses it.

---

## 9. Loc surface (`localization/english/eotg_government_l_english.yml`; UTF-8 with exactly one BOM, Canadian English, bare `[x.GetName]`)

For each of the 4 governments (`<g>` = the full key, e.g. `eotg_pmc_government`). The key set copies vanilla's feudal and clan keys (`G/localization/english/government_l_english.yml`):

| Key | Content |
|---|---|
| `<g>` | name: "PMC", "Corporation", "Gob-Corp", "Cartel" (LQ2 for "Gob-Corp") |
| `<g>_adjective`, `<g>_realm` | |
| `<g>_desc` | 2–4 sentences: identity plus the G1 mechanics (holdings, contract identity, the Cartel's tributaries). Names no nation (§11). |
| `<g>_with_icon` | `@government_type_<vanilla>! $<g>$`: reuse a vanilla text icon (unclaimed precedent: `@government_type_herder!`). PMC: mercenary; Corporation: administrative; Gob-Corp: republic; Cartel: clan. The localizer confirms each `@` icon exists. |
| `<g>_filter_option`, `<g>_filter_option_desc` | character-finder filter |
| `<g>_obligations`, `<g>_vassals_label` | contract UI |
| `<g>_vassal_opinion`, `<g>_opinion`, `<g>_tax_contribution_add`, `<g>_tax_contribution_mult`, `<g>_levy_contribution_add`, `<g>_levy_contribution_mult` | **engine-generated modifier names**. Vanilla defines them for every government (e.g. `republic_government_vassal_opinion`). They show in any tooltip that uses them. |

Also:
- **Laws (4 each):** `eotg_<gov>_succession_law`, `_subname`, `_effects` (shape: `succession_laws_l_english.yml:14-16`).
- **Contracts (8):** `<contract>`; each of its 5 levels `<contract>_<level>` and `<contract>_<level>_short` (shape: `feudal_government_levies`, `feudal_levies_low`, `feudal_levies_low_short`).
- **Flavourization:** 92 keys, one per entry key in §3.1, text from §8.
- **Knight terms:** §10, 4 terms × 8 keys.
- **Debug decisions (5):** `<key>`, `<key>_desc`, `<key>_tooltip`, `<key>_confirm`.

**No `replace/` override is needed.** `KnightCulture` is overridden in script (§10), not in loc. Vanilla's knight loc keys are untouched.

---

## 10. The knight term (CB-48)

**Mechanism.** Vanilla picks the term per character through the customizable loc `KnightCulture` (`G/common/customizable_localization/00_knight_culture.txt:1-89`), using language pillar and faith. Seven child entries inherit with `parent = KnightCulture` and a `suffix` (`:91-123`). **The mod redefines the key `KnightCulture` only** (a key-level override, the same mechanism as `herders_and_tributary_constraints`, pitfalls §16). The children are not redefined, so they follow automatically.

```
# common/customizable_localization/eotg_knight_culture.txt
KnightCulture = {
    type = character
    text = { trigger = { eotg_gov_knight_realm_is_pmc = yes }         localization_key = eotg_knight_operator }
    text = { trigger = { eotg_gov_knight_realm_is_corporation = yes } localization_key = eotg_knight_agent }
    text = { trigger = { eotg_gov_knight_realm_is_gobcorp = yes }     localization_key = eotg_knight_strongarm }
    text = { trigger = { eotg_gov_knight_realm_is_cartel = yes }      localization_key = eotg_knight_enforcer }
    text = { localization_key = knight_default  fallback = yes }      # vanilla "Knight" (00_knight_culture.txt:85-88)
}
```
- **Vanilla's culture and faith blocks are not copied.** They name `christianity_religion`, `language_frankish` and 15 other real-world keys (`:5-83`). Mod script must not name culture or faith keys (the gate ruling), and those keys will not exist once the mod ships its own cultures.
  - Consequence in the vanilla-map test: vanilla-government characters see "Knight" instead of Champion, Fāris or Bushi. That is the CB-48 intent ("this also fixes vanilla's own knight UI").
  - Vanilla's landless-adventurer "Champion" block is dropped as well. The owner can restore it as one government block if wanted.
- **The trigger** `eotg_gov_knight_realm_is_<gov>`:
  ```
  OR = {
      government_has_flag = eotg_government_is_<gov>
      AND = { is_landed = no  employer ?= { government_has_flag = eotg_government_is_<gov> } }
  }
  ```
  The scope may be a ruler (vanilla's own block tests `has_government` on it, `:5`) or an unlanded knight, whose realm is the employer's.
- **Pitfalls entry (orchestrator adds it when this ships):** "Key-level override of `KnightCulture`." Confirm it with `logs/database_conflicts.log`, which should show `KnightCulture` overridden by `eotg_knight_culture.txt`. After every CK3 update, diff vanilla's `00_knight_culture.txt` for new child suffixes.

**Every suffix variant, per term** (the suffixes are from `00_knight_culture.txt:91-123`; the key shapes copy `G/localization/english/knight_culture_l_english.yml:30-31, 67-70, 96-97`):

| Key | Example (Operator) |
|---|---|
| `eotg_knight_operator` | `"[Concept( 'knight', '$eotg_knight_operator_no_tooltip|q$' )|E]"` |
| `eotg_knight_operator_plural` | `"[Concept( 'knight', '$eotg_knight_operator_no_tooltip_plural|q$' )|E]"` |
| `eotg_knight_operator_no_tooltip` | "Operator" |
| `eotg_knight_operator_no_tooltip_plural` | "Operators" |
| `eotg_knight_operator_no_tooltip_lowercase` | "operator" |
| `eotg_knight_operator_no_tooltip_lowercase_plural` | "operators" |
| `eotg_knight_operator_no_tooltip_lowercase_plural_possessive` | "operators'" |
| `eotg_knight_operator_no_tooltip_lowercase_adjective` | "operator" (vanilla's "champion" pattern, `:70`) |

The other three terms get the same 8 keys: `eotg_knight_agent`, `eotg_knight_strongarm`, `eotg_knight_enforcer`. The terms are owner question OQ1. Apart from the PMC's, they are proposals.

---

## 11. Lore constraints

- **Precedence:** ERRATA → dated `docs/lore` entries (to 866) → `866_bookmark_design.md` → SETTING LORE body (`CLAUDE.md` Canon). `docs/lore/NATIONS_AT_866_AG.md` is untracked and unreviewed. It is cited here only as a pointer, never as canon.
- **No authority above the polity at 866** (ERRATA "LAW AT 866"). Contracts, tribute and licences are enforced only by the realm that presses them. No government text mentions a galactic court, a League, arbitration, a registry or a licensing body.
- **Map-agnostic text:** no government description, rank name or knight term names a nation (P&D, Helix, the Gob-Ogre Trade League, the Concrete Cartel, the Slate Syndicate) or a person.
  - This also keeps the cybernetics never-name list (`cybernetics_v2.md:211`) intact, since the list includes P&D and the Concrete Cartel.
  - Generic words ("a board", "fifty princes" as a description of the form, "bosses") are allowed if LQ2 and LQ6 clear them.
- **No remote-kill, state augmentation programme or AI Secretariat** framing anywhere (ERRATA "CYBERNETICS AT 866").
- **The Slate Syndicate does not exist at 866** (`Third era Nations.md:1403-1405`). v1's Cartel header is wrong for this bookmark (LQ1).
- **Helix at 866 is not "board and CEO"** (ERRATA "HELIX CORPORATION"). Don't describe the Corporation government as Helix's.
- **Canadian English** (colour, -ize).

---

## 12. Test placement: cartographer handoff (history data only, `docs/test_submods/british_isles/isles_assignments.csv`)

**Verified vanilla 1.20 keys** (`G/common/landed_titles/00_landed_titles.txt`, title tree parsed; 1066.9.15 holders from `G/history/titles/`; ages from `G/history/characters/`):

| Owner's ask | Vanilla title | Finding |
|---|---|---|
| Duchy of Paris | **`d_valois`** (loc "Valois") | **There is no `d_paris` or `d_ile_de_france`.** Paris is `b_paris` in `c_ile_de_france`, the capital county of `d_valois` (k_france). Counties: c_ile_de_france, c_brie_francaise, c_vermandois, c_valois, c_amiens, c_beaumont, c_clermont. |
| Kingdom of Brittany | **`k_brittany`** | one duchy, `d_brittany` (c_vannes, c_nantes, c_cornouaille, c_french_leon, c_penthievre, c_rennes). k_brittany is vacant at 1066. |
| Kingdom of León | **`k_leon`** | `d_leon` (c_leon, c_benavente, c_zamora, c_salamanca, c_avila) + `d_asturias` (c_asturias_de_oviedo, c_pravia) |
| Gob-Corp, a duke on the Mediterranean coast | **`d_provence`** (recommended) | Coastal counties c_provence (b_toulon, b_marseille) and c_nice; it lies in k_burgundy, **which is in e_france in 1.20**, so inside the test zone. Its holder at 1066 is a single duke (420). The alternative, `d_languedoc` (Montpellier, Béziers, Narbonne), has an inland capital (c_albi) and no single duke in 1066, so it is not recommended. |

**Status (coordinator, 2026-10-08):** the generator already places these, with feudal stand-ins until G1 lands. It has Raoul (40406) on d_valois, **Konan II (348)** on k_brittany, Alfonso VI (108500) on k_leon and Bertrand (420) on d_provence, each with vassal counts on the same government (two of them generated lowborn). All capitals are castles. How that build compares with this spec:
- **Holders are accepted.** G1 sets no `can_get_government` (§5.0), and history `government =` sets the government directly. Culture (French, Breton, Castilian, Occitan, Asturleonese) and faith (Catholic) are irrelevant: no government reads either.
- **Lowborn vassals** get a dynasty when landed, because of `rulers_should_have_dynasty = yes`.
- **Capital holdings:**
  - PMC and Cartel: a castle is right.
  - Corporation and Gob-Corp: a castle works, since castle is in `valid_holdings`, so there's no penalty. **Recommended:** set the `holding` column to `city_holding` for the two realms' capital baronies, so the primary holding is tested (V-G17). Without that, V-G17 can't pass.
- **Brittany:** Konan II **dies 1066.12.11** in vanilla history, three months in. Either keep him, which makes V-G9 (the heir keeps the government) the first thing that happens to the Corporation test ruler, or use the layout below (Hoël, 178, as king; Konan as vassal duke), which tests the same thing without ending the player's start. The cartographer and owner choose. Both are valid G1 tests.
- **Keys unchanged.**

**Rows (the spec's reference layout).** The cartographer confirms every id is alive at 1066.9.15; the generator validates this.

| title | holder | liege | government | scope | note |
|---|---|---|---|---|---|
| `d_valois` | `40406` | `0` | `eotg_pmc_government` | `realm` | **PMC duke: Raoul of Valois (b. 1021, d. 1074).** Recommended over Philip I (214), who is **14 at the start** and would put the PMC test under a regency (OQ2). |
| `c_ile_de_france` | `40406` | | | | Paris in the PMC domain; capital barony `b_paris` **must be a castle** (the cartographer checks vanilla history/provinces) |
| `c_valois`, `c_amiens` | `40406` | | | | his vanilla counties |
| `c_brie_francaise`, `c_beaumont` | `214` | `d_valois` | | | Philip I as a vassal Contractor (a minor vassal is harmless) |
| `c_vermandois` | `418` | `d_valois` | | | Herbert (b. 1032) |
| `c_clermont` | `303412` | `d_valois` | | | Renaud (b. 1010) |
| `k_brittany` | `178` | `0` | `eotg_corporation_government` | `realm` | **Corporation king: Hoël (b. 1030, d. 1084).** |
| `c_nantes`, `c_cornouaille` | `178` | | | | his domain; capital `c_nantes`, barony `b_nantes` **made a city** |
| `d_brittany` | `348` | `k_brittany` | | | **Conan II as vassal duke (Operations Chief). He dies 1066.12.11 in vanilla history**: a free test that a Corporation heir keeps the government (V-G9). |
| `c_vannes`, `c_rennes` | `348` | | | | Conan's domain |
| `c_french_leon` | `10059` | `k_brittany` | | | Morvan |
| `c_penthievre` | `346` | `k_brittany` | | | Eudes (b. 999) |
| `k_leon` | `108500` | `0` | `eotg_cartel_government` | `realm` | **Cartel king: Alfonso VI (b. 1040).** |
| `d_leon`, `c_leon`, `c_benavente`, `c_salamanca`, `c_avila` | `108500` | | | | domain; `b_leon` a castle |
| `c_zamora` | `108501` | `k_leon` | | | Urraca (b. 1033) |
| `d_asturias`, `c_asturias_de_oviedo` | `108512` | `k_leon` | | | Rodrigo as a vassal duke (Underboss) |
| `c_pravia` | `asturleonese0078` | `d_asturias` | | | Pedro, a count under the duke: three tiers in one realm |
| `d_provence`, `c_provence` | `420` | `0` | `eotg_gobcorp_government` | `realm` | **Gob-Corp duke: Bertrand (b. 1047).** The capital barony of `c_provence` (`b_toulon`, listed first) is **made a city**. |
| `c_venaissin` | `32534` | `d_provence` | | | |
| `c_nice` | `20315` | `d_provence` | | | coastal vassal |
| `c_forcalquier` | `40802` | `d_provence` | | | |

**Why these setups:**
- **Each realm has vassals at one or two tiers**, so contracts (V-G6) and rank names (V-G7) can be tested.
- **Tributary targets for the Cartel** (V-G13) are the independent pockets Toledo (clan), Córdoba (republic), Gipuzkoa (tribal) and Barcelona (feudal). Unsworn counties are never targets (§5.4).
- **Neighbours:** William of Normandy (feudal) and the Archbishop of Reims border the PMC; Unsworn counties surround all four, so the claim interaction (V-G19) gets exercised.

**Sequencing:** history that names `eotg_*_government` fails to resolve until the scripter's G1 government files exist. Regenerate and load only after G1 lands.

**Bookmark:** add none of these to the bookmark screen. They need vanilla bookmark portraits (sub-mod README). Pick them on the map.

---

## 13. Definition of done (Phase G1)

**Static (eotg-qa):**
1. Tiger is clean except the known-benign list in `CLAUDE.md`. PX LSP and `px_vocab_check.py` are clean over the new files. PX `locCoverage` shows no missing `eotg_` key.
2. QA checks all four government blocks by hand against `_governments.info` and the vanilla lines cited in §5 (Tiger 1.17 can't).
3. `grep -rnE 'eotg_[ekdcb]_'` is empty. No title, province, culture, faith or character key appears in any G1 file. The test sub-mod CSV is history data and is exempt.
4. Each `<g>` key appears in the 4 government files, each flavourization entry and the law `potential`. Each `eotg_government_is_<gov>` flag is read by ≥1 trigger (no dead flags: robustness plan F5).
5. The loc file has exactly one BOM and no `[scope:`, and every §9 key is defined exactly once.

**In game (human, British Isles sub-mod with the §12 rows; checklist V-G below):**
6. V-G1 to V-G12 pass for all four. V-G13 passes for the Cartel; V-G14, V-G15, V-G17 and V-G20 are recorded.
7. A 50-year observer run (V-G12) ends with all four realms alive, with a valid succession law, solvent, and with no ruler stuck on an invalid law.

### V-G checklist (in game, `-debug_mode`)
| ID | Check | Pass |
|---|---|---|
| V-G1 | The game loads; error.log shows nothing from the 12 new files; `database_conflicts.log` lists the `KnightCulture` override | yes |
| V-G2 | The four test rulers and their realm-scope vassals show the right government (character window, government map mode) | yes |
| V-G3 | Each test ruler can be picked on the map and played (not "Is unplayable") | yes |
| V-G4 | The realm screen shows `eotg_<gov>_succession_law` with a named heir. After crown authority 2, the law can be changed to vanilla Primogeniture if the culture has the innovation | yes |
| V-G5 | Crown authority laws are listed and passable | yes |
| V-G6 | Modify Vassal Contract shows the government's 2 trees + 3 rights with loc. The player changes a level; an AI liege changes one over time | yes |
| V-G7 | An independent ruler shows the top rank ("Contractor-General Raoul"); vassals show tier ranks; titles show the government's rank word | yes |
| V-G8 | The Knights tab and cybernetics lines using `KnightCulture` say Operator / Agent / Strongarm / Enforcer; William's knights say "Knight" | yes |
| V-G9 | Conan II's death (1066.12.11): his heir holds d_brittany **as Corporation**. Also `kill` each top ruler in console: the heir keeps the government and the law | yes |
| V-G10 | Grant a county to a courtier in each realm; record the new vassal's government (expected: the liege's) | recorded |
| V-G11 | Leakage: after 50 years, the government map mode shows a mod government only in the four realms and their conquests or grants | yes, else build §5.6 |
| V-G12 | 50-year AI run: no realm without a succession law, no permanent bankruptcy, no law-change churn, the realms claim Unsworn counties | yes |
| V-G13 | Cartel: Offer Tributary Status is available against an independent pocket. A tributary forms (`tributary_settled`); tributary land counts toward title creation | yes |
| V-G14 | PMC: accolades are available | yes |
| V-G15 | Kingdom-tier Brittany and León have a royal court | yes |
| V-G16 | Debug decisions: William becomes each government and gets its law; "become feudal" drops the mod law to a feudal one | yes |
| V-G17 | Corporation and Gob-Corp: a city capital and a held castle cause no invalid-holding penalty; the AI builds | yes |
| V-G18 | The government map-mode colours are distinct from every vanilla government | yes |
| V-G19 | The four realms can use the Unclaimed claim interaction and the Frontier decisions | yes |
| V-G20 | Record the government of generated barons: castle barons under the Corporation, city barons under the PMC | recorded |

---

## 14. Phase G2 outline ("deep"; needs owner approval for every new event)

### 14.1 Priorities
| P | Item | Notes |
|---|---|---|
| **P1** | Role-ladder triggers (§14.2) and the signature resources (§2), with one change effect each | no events; gate for everything below |
| **P1** | One vassal-tier and one top-tier **decision** per government that moves the resource | closes robustness plan F8 (PMC, Gob-Corp: 0 vassal decisions in v1) |
| **P1** | Pulse wiring: `yearly_playable_pulse` (**not** `on_yearly_playable`, v1 lesson 13), one mod on_action per government with Section A (any tier, role trigger) and Section B (top) | the cooldown lives in the on_action only (lesson 5) |
| **P2** | Lift v1 events after a coupling audit: PMC 32, Corporation 33, Gob-Corp 27, Cartel 27 (`OLD PROJECT VERSION/events/eotg_{pmc,corporation,corp,gobcorp,cartel}_*`) | each must move or read its resource or be dropped. The 28 tier-neutral events of robustness plan 0.3 go first. |
| **P2** | Third contract obligation per government (board seat, enforcement rights, field commission) with consumers | v1 §6 |
| **P2** | Elective succession: board election (Corporation), wealth-weighted vote (Gob-Corp), takeover (Cartel), command succession (PMC); title succession laws plus `common/succession_election/` | shape: `01_title_succession_laws.txt:2-34` |
| **P3** | CBs (v1 `eotg_boardroom_war`, proxy war), the Sabotage Rival scheme, the PMC Logistics Officer council seat, PMC → Corporation evolution decision, the Cartel faction set | v1 design doc §2.5, §3.3, §3.6, §4.5, §6.3, §6.5 |
| **P3** | Coupling to cybernetics and Frontier (§5.1–5.4 "Coupling") | optional, one-line weight or branch each, behind a government flag |

### 14.2 The role ladder (relative, not absolute)
For each government, `eotg_<gov>_role_top` is the independent ruler of that government at any tier. Then `eotg_<gov>_role_county` / `_duchy` / `_kingdom` match **vassals** by `highest_held_title_tier`. A trigger at every tier is the Gate 2 rule; the v1 names map across (e.g. `eotg_st_is_field_director` → `eotg_pmc_role_duchy`).

### 14.3 Gate 2 DoD (for when G2 closes)
- `government_rules` per the robustness plan §2: done in G1.
- Role-ladder triggers at all 4 tiers.
- Signature resource in every flavour event (QA audit 8).
- on_action wiring with 100% reachability and 0 self-cancelling events.
- Decisions at vassal and top tier.
- A human plays 5 years as each government and sees at least one government event.

### 14.4 Owner approval needed
Every new event, option or beat (G2 P1 decisions included, if they fire events).

### 14.5 Probes
Does vanilla influence work without `mechanic_type = administrative`? Influence is read through the `government_has_influence` flag in activities and buildings, but its gain is coded for admin (`G/common/defines/00_defines.txt:318-320`). If it works, the Corporation's board influence could be vanilla influence. Probe it with a debug decision in G2.

---

## 15. Deferred (consciously cut from G1)

| Item | Why |
|---|---|
| `can_get_government` | Heir-path risk; built only if V-G11 shows leakage (§5.6) |
| `mechanic_type`, influence, treasury, `house_unity`, `domicile_type`, `tax_slot_type` | each needs a subsystem the mod lacks (robustness plan 2.6) |
| Elective and violent successions | G2 P2 |
| Government-specific CBs, schemes, council positions | G2 P3 |
| `opinion_of_liege` per government | G2. Needs a resource to key off. |
| Real government icons | art debt (human). G1 uses placeholder copies of vanilla icons (§3.1). |
| Fringe, New Cauldron, Elven Monarchy | not in this request |
| Vanilla culture and faith knight terms | dropped from the `KnightCulture` override by the map-agnostic rule (§10). The mod's cultures can add blocks after Gate 1. |
| Named exemplar nations and bookmark characters | Gate 1 (real map) |

---

## 16. Owner questions (kept to what precedent can't settle)

- **OQ1, knight terms.** The proposals are PMC **Operator** (v1), Corporation **Agent** (your example), Gob-Corp **Strongarm**, Cartel **Enforcer**, and everyone else **Knight** (vanilla's `knight_default`). Approve, or give replacements. Adjective forms follow vanilla's pattern (the word itself).
- **OQ2, the PMC test ruler.** Philip I (214), who holds Paris in vanilla, is 14 at the start, so the PMC test would run under a regency. **Recommendation:** Raoul of Valois (40406), 45, as duke holding Paris, with Philip as a vassal count. Proceeding with Raoul unless you say otherwise. The Brittany layout (Hoël as king; Conan II as a vassal duke who dies in December 1066, which tests succession) is proceeding on the same terms.
- **Settled by precedent, for your information** (no answer needed):
  - every government is dynastic (`rulers_should_have_dynasty = yes`) and has legitimacy, the Cartel included (v1 had both `no`);
  - the holdings copy feudal's and republic's;
  - G1 succession is single-heir, and elections come in G2.

## 17. Lore questions (eotg-lore-keeper)

- **LQ1:** Confirm that the Slate Syndicate is post-866 and that the 866 cartel-state is the Concrete Cartel. Confirm that the Cartel government's text may describe the form without naming it.
- **LQ2:** Gob-Corp:
  - Is "Gob-Corp" a canon name for the government form, or is a different display name wanted (the polity is the Gob-Ogre Trade League)?
  - Is there a **Director-General** at 866, or only the Council of Fifty Trade Princes (`866_bookmark_design.md:49`, "council-led")? This decides the top rank.
  - Rule on the "princes hoard mercenaries" modifier, which comes from unreviewed NATIONS :55.
- **LQ3:** PMC: is a PMC state canon at 866, or is it a mod-original form (acceptable, but recorded as such)? Are "Operator" and the ladder Contractor → Field Director → Executive Commander → Contractor-General acceptable?
- **LQ4:** Corporation: confirm the ladder Account Director → Operations Chief → Regional Director → CEO, and that government text names no corporation (P&D, Helix, Blackstar, Calix).
- **LQ5:** All of the §8 rank names, especially the new barony ranks and every title-rank word. Also the female forms of "Lord" ranks (Merchant Lord, Street Lord, Grand Underlord).
- **LQ6:** Does the cybernetics "no mafia vocabulary" rule (kingpin seller spec B2) bind the Cartel government's ranks (Underboss, Boss, Racket, Outfit)? Does "Cartel" as a title rank collide with the canon syndicate names used by the Patron?
- **LQ7:** Is `docs/lore/NATIONS_AT_866_AG.md` (untracked) a reviewed source? Until ruled, this spec cites it only as a pointer.

---

### HANDOFF
- status: done
- next: eotg-lore-keeper
- ask: Review docs/specs/governments_v2.md against canon (LQ1–LQ7: rank names, knight terms, Gob-Corp naming and Director-General, the Slate Syndicate date, mafia vocabulary, NATIONS_AT_866_AG.md status). eotg-scripter then builds Phase G1 (§3–§8, §10), and eotg-localizer writes §9.
- files: docs/specs/governments_v2.md
- needs-loc: §9 (government display and modifier keys ×4, 4 laws × 3, 8 contracts × 11, 92 flavourization keys, 4 knight terms × 8, 5 debug decisions × 4)
- needs-lore: LQ1–LQ7 (§17)
- needs-human: OQ1 knight terms and OQ2 the PMC test ruler (§16); in-game V-G1–V-G20 after G1 lands; orchestrator: add the 4 new folders to the CLAUDE.md placement list, copy 4 placeholder government icons, add the KnightCulture pitfalls entry when it ships; cartographer: the §12 rows in isles_assignments.csv, loaded only after the scripter's G1
