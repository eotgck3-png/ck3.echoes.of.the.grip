## QA report: Gob-Corp / Trade Oligarchy (`eotg_gobcorp_government`), deep assessment, 2026-10-11
Tools: PX LSP `common localization`: 6 warnings, all the known-benign `building_walls_*` missing-loc; none in government files. `px_vocab_check common`: 0 findings. `eotg_lint --baseline`: 0 findings. Tiger not run. Logs: `scratchpad/govassess/gob_*.txt`.
Paths: `GOV` = `common/governments/eotg_gobcorp_government.txt`; `V/` = vanilla game; `GT` = `V/common/governments/00_government_types.txt`; `TPL` = `docs/specs/government_template.md`.

### Scorecard
| Area | Verdict | Evidence | Std |
|---|---|---|---|
| P0 blacklist | MEETS | `GOV:56-62` carries no republic, mercenary, holy order, admin, theocracy, ecclesiastical or adventurer flag (republic appears only in comment `:15`). Read against `V/common/scripted_rules/00_rules.txt:151-249`. The mod has no `common/scripted_rules/`. | P0 |
| P1/P2 dynastic | MEETS | `GOV:25-26`; `inherit_from_dynastic_government` unset | P1, P2 |
| P3 succession law | MEETS (untested) | `common/laws/eotg_government_succession_laws.txt:89-119` gates on the identity flag; safety net at `common/on_action/eotg_government_on_actions.txt:10-51` and `common/scripted_effects/eotg_government_effects.txt:33-41`. Vanilla single heir is barred (`00_law_triggers.txt:343-397`). | P3, §3.5 |
| P4 playable character | MEETS | The test ruler is a duke. `V/.../00_available_for_events_triggers.txt:964-980` | P4 |
| P5 heir keeps government | MEETS (untested) | `GOV:30-31`; `use_as_base_on_rank_up` unset | P5 |
| P6 GOVERNMENT_TYPES | MEETS | `common/defines/eotg_government_defines.txt:20-39` matches `V/common/defines/00_defines.txt:550-571` verbatim; key at `:44`. The sub-mod copy is in step (`zz_eotg_test_bi_government_defines.txt:13-37`). | P6 |
| P7 can_get / fallback | PARTIAL | Both left unset on purpose (`GOV:13-15`). Leakage is untested (T7). | P7 |
| P8 bookmark / designer | FAILS / N-A | No sub-mod bookmark character uses it (`docs/test_submods/british_isles/common/bookmarks/bookmarks/00_bookmarks.txt`). It is reachable only by a map pick or the debug decision. The designer only assigns tribal, clan and feudal (vanilla), so N-A. | P8 |
| Q1 core verb | FAILS | Feudal verb. It differs from feudal only by the modifiers at `GOV:44-49` | §2 Q1 |
| Q2 resource | FAILS | `eotg_gobcorp_market_share` is specced (`governments_v2.md:33`) and absent from script | Q2, §3.11 |
| Q3 vassal model | PARTIAL | Own group (`groups/eotg_government_contract_groups.txt:37-45`). The trees are feudal's levy shape with new numbers (`contracts/eotg_government_obligations.txt:275-399`). No `opinion_of_liege`. | Q3, §3.3 |
| Q4 succession fits fiction | FAILS (conflict) | Single heir, oldest child (`laws:101-106`; loc `:69-70` "Oldest Child Inherits"), against "no single head" (`governments_v2.md:203`) | Q4 |
| Q5 entry / exit | FAILS | Only the debug decision (`common/decisions/eotg_government_debug_decisions.txt:74-104`). Forced-exit behaviour undefined. | Q5 |
| Q6 AI | PARTIAL | `GOV:51-54`; contract AI desire set; no `grant_vassal_ai_will_do`, `possible_grant_vassal_governments` or `ai_ruler_desired_*` | Q6, §3.14 |
| Q7 / §3.15 UI | PARTIAL | Free surfaces only. Resource display missing (no resource). | §3.15 |
| §3.1 fields | MEETS | Every field has a vanilla `.txt` site: rules `GT:7,8,10,11`, admin `GT:454,458,462`, `disable_regnal_numbers` `GT:816`, `royal_court` `GT:14`, holdings `GT:65-67`, `ai` `GT:25,73`, mask `GT:90-91`. No `.info`-only field. `diplomacy` has no government site but is a generic modifier (`GI:721-733`). | §3.1 |
| §3.2 flags | PARTIAL | Identity flag read by the law, effect, trigger and on_action. Family flag `eotg_government_is_corporate` (`GOV:58`) has **zero readers**. That is a documented exception (`governments_v2.md:50`). | §3.2 |
| §3.3 contracts | MEETS (min) | 5+5 chained levels; `subject_opinion`, AI and score copied by position from `V/.../feudal.txt:128-190`; three generic rights | §3.3 |
| §3.4 laws | MEETS (min) | Crown authority flag `GOV:61` | §3.4 |
| §3.6 holdings | MEETS (untested) | Republic city shape verbatim; V-G17 | §3.6 |
| §3.7 MAA / knights | PARTIAL | `men_at_arms_maintenance`, `levy_size` only | §3.7 |
| §3.8 decisions / interactions / CBs | FAILS | None beyond debug | §3.8 |
| §3.13 modifier | MEETS | `GOV:44-49`; no `top_liege_character_modifier` | §3.13 |
| §3.16 loc | MEETS | `localization/english/eotg_government_l_english.yml:32-46, 68-70, 118-139, 208-230, 270-277, 294-297, 310-311`. One BOM, no `[scope:`. Shows "Trade Oligarchy" wherever the government is named. | §3.16 |
| Icon | PARTIAL | 70×70, byte-identical to vanilla `republic_government.dds` | §3.16 |
| §3.17 text icon | PARTIAL (min) | `@government_type_republic!` (`loc:36`); exists at `V/gui/texticons.gui:4767` | §3.17 |
| §3.18 flavourization | MEETS | `common/flavorization/eotg_government_flavorization.txt:593-877`: 23 entries, priority 60/61, `top_liege = no`, no name lists. Shape matches `00_title_holders.txt:8518-8539`. | §3.18 |
| §3.19 on_actions | MEETS (min) | Additive (`on_actions.txt:10-22`); succession net only | §3.19 |
| §3.21 knight term | MEETS | `eotg_knight_culture.txt:41-46`; 8 loc keys `loc:270-277` | §3.21 |
| Species-neutral | MEETS | `loc:35` names no species or nation | spec OQ3 |

### BLOCKERS
None for G1 as scoped. The build matches `governments_v2.md` §5.3, §6.2, §7, §8, §9 and §10 field for field, and the template classifies all four governments as "playable reskins" (`TPL:507`). **Measured against the template's standard for a *distinct* government, though, it fails Q1, Q2, Q4, Q5 and §3.8.** It is feudal plus four modifiers, its own rank names and a renamed contract.

### GAPS
- [G1] **Succession contradicts the fiction.** The fiction says "no single head" (`governments_v2.md:203`). The law is single heir, oldest child (`laws:101-106`), and the loc names it Charter Succession / "Oldest Child Inherits" (`loc:68-70`). `royal_court = any` (`GOV:35`) and the "First Prince" top rank at any tier reinforce one head. TPL Q4 requires this to be recorded as debt. It sits on the owner question list (`TPL:681`), but nothing marks it as owner-accepted. Owner: eotg-architect.
- [G2] **No signature resource.** `eotg_gobcorp_market_share` is unbuilt, so invariant 5 has nothing to bind G2 events to. Owner: eotg-architect, then eotg-scripter.
- [G3] **No entry or exit decision, and no forced-exit story.** Owner: eotg-architect.
- [G4] **No P8 bookmark entry.** Owner: eotg-cartographer, if the owner wants it (sub-mod bookmark portraits are the cost, `TPL:421`).
- [G5] **The succession net covers only game start and government change.** A courtier landed by a Gob-Corp liege takes the government through `use_as_base_on_landed`. Whether `on_government_change` fires on a first landing is unknown. If it does not, the default-law pick (`_laws.info:300-308`) decides the law. Test before adding a hook. Owner: eotg-scripter.
- [G6] `grant_vassal_ai_will_do`, `opinion_of_liege` and `top_liege_character_modifier` are absent (§3.14, Q3).

### POLISH
- [P1] Comments cite other mods as precedent, against the owner rule of 2026-10-11: `common/defines/eotg_government_defines.txt:11` (After the End) and `common/customizable_localization/eotg_knight_culture.txt:8-9` (TFE). Replace them with vanilla cites. Owner: eotg-scripter.
- [P2] A stale comment says "Terms: OQ1 defaults (PENDING OWNER)" (`eotg_knight_culture.txt:18`). OQ1 is RULED (`governments_v2.md:681`).
- [P3] A stale doc line says the government keys are "not defined yet" (`docs/test_submods/british_isles/README.md:115-116`). Owner: eotg-cartographer.
- [P4] Fiction: `diplomacy = -1` (`GOV:46`, carried over from v1) penalizes the core skill of a trade oligarchy, whose fiction is bargaining and partnerships. Recommend `diplomacy = 1` or `stewardship`. Owner: eotg-architect.
- [P5] The vassal-group desc says "trade bloc" (`loc:311`), but "Bloc" is the kingdom title rank (`loc:211`), so the word is ambiguous.
- [P6] `has_government = feudal_government` appears at `eotg_government_debug_decisions.txt:155`, in debug only. TPL §5.1.5 says no `has_government`.

### Spec conformance (`governments_v2.md`)
- **Built as specced:** §5.0 fields; §5.3 block (modifier, ai, flags, colour, mask); §6 group and trees (numbers match `:324-325`); §7.1 law and §7.2 net; §8 rank table (`:428-429`); §9 loc with "Trade Oligarchy" (OQ3); §10 Strongarm; §12 d_provence assignment (`k_burgundy.txt:199-203`).
- **Deferred by the spec to G2 (`:636-640`):** market share, decisions, 27 v1 events, wealth-weighted elective succession, and the `eotg_market_faction_cycle` reader of the family flag.

### Fiction fit
The fiction fits on desc, ranks, knights and colour. Species-neutral is met: the desc reads "partners of every stripe" and names no goblin or ogre. Mechanically, "power is bought and counted" and "rivalry inside the charter" have no expression, and "no single head" is actively contradicted (G1).

### Top 3 recommendations
1. **Get an owner ruling on G1.** Either accept single heir as recorded G1 debt (and rename the subname away from "Oldest Child Inherits" toward charter wording), or prioritize the G2 wealth-weighted elective law with dynasty-limited electors (P1-safe).
2. **Build `eotg_gobcorp_market_share` with the §3.15 default display.** That means one clamped change effect, init and teardown in the existing on_action branches, and a scaled modifier plus a story-cycle counter. Then build one vassal-tier and one top-tier decision that move it (`governments_v2.md:636`).
3. **Run CB-49 T1, T3, T5 and T7 before G2 builds on this.** Every "MEETS (untested)" above rests on them, the city shape (V-G17) especially.

### Unverifiable without in-game test
- **Pickable at 1066 with no remap (T1).** Pick Bertrand (420) on the map; no `GAME_OVER_CANNOT_PLAY_*` appears and the government reads "Trade Oligarchy".
- **Clean load (T2).** error.log has no "preregistered modifier" or "Unexpected token" lines from `GOV`. `database_conflicts.log` shows only the `KnightCulture` override.
- **Heir keeps law and government (T3, V-G4).** `kill` Bertrand; the heir keeps the government and has `eotg_gobcorp_succession_law`.
- **Erosion through a feudal relative (T4).** Record the resulting government.
- **New vassals (T5, G5).** Grant a county to a courtier and record the vassal's government and succession law (whether `on_government_change` fired).
- **Debug conversion (T6, V-G16).** The debug decision converts in and back; the law is added and then dropped.
- **No leakage (T7).** After a 50-year observer run, the government is confined to the Provence pocket.
- **50-year AI health (T8, V-G12).** No bankruptcy, no lawless rulers.
- **Surfaces (T9, V-G8).** "First Prince" at duke tier; "Strongarms" in the Knights tab and lowercase lines; brass map colour.
- **City shape (V-G17).** No invalid-holding penalty for the castle; the AI builds.

### Verdict
**PASS (pending in-game)** as a G1 playable reskin. **FAIL** as a distinct government under `TPL` §2: no verb, no resource, and succession that contradicts "no single head".
