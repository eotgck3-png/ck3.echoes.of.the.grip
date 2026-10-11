## QA assessment: Corporation government (`eotg_corporation_government`), 2026-10-11
Standard: `docs/specs/government_template.md`. Design: `docs/specs/governments_v2.md` §5.2, §6–§10, §14.5. Read-only; Tiger not run (another agent).
Tools: PX LSP `common localization` reported 6 findings, all `building_walls_*` missing-loc (known benign). `px_vocab_check common` found 0. `eotg_lint` found 0 new. Corporation loc: one BOM, no `[scope:`, no duplicate keys.
Paths: `GOV` = `common/governments/eotg_corporation_government.txt`, `V/` = vanilla game root.

### Scorecard
| Area | Verdict | Evidence | Ref |
|---|---|---|---|
| P0 playable blacklist | MEETS | Only vanilla flags are settled, domain_limit and crown_authority (GOV:55-61). None is in `V/common/scripted_rules/00_rules.txt:151-249`. The mod ships no `scripted_rules/`. | §1 P0, §5.1.8 |
| P1 dynastic | MEETS | GOV:25-26 | P1 |
| P2 inherit default | MEETS | unset | P2 |
| P3 succession law | PARTIAL (untested) | `eotg_government_succession_laws.txt:57-87`: the potential/can_have/can_keep/should_start_with all read the identity flag. Vanilla `single_heir_succession_law` (index 3) has `should_start_with` true on `innovation_primogeniture` (`V/common/laws/00_succession_laws.txt:289-296`) but fails `can_have` (`00_law_triggers.txt:371-397`). The safety net covers it (`eotg_government_effects.txt:24-32`, on_actions :10-51). V-G4 has not been run. | P3, §3.5 |
| P4 is_playable_character | MEETS | the test ruler is a king | P4 |
| P5 heir keeps government | MEETS (untested) | GOV:30-31 | P5, T3 |
| Fiction: board vs single heir | **FAILS** | Single-heir "Executive Succession / Oldest Child Inherits" (loc :65-67) against the desc phrase "run by a board" (loc :20) | §2 Q4 identity test |
| P6 GOVERNMENT_TYPES | MEETS | The 20 vanilla entries diff identical to `V/common/defines/00_defines.txt:550-573`. The key is at `eotg_government_defines.txt:43`. The sub-mod copy matches (it adds only its offmap government). | P6, §5.1.4 |
| P7 can_get_government / leakage | PARTIAL | Deliberately unset, with no fallback. The leakage risk is higher than for the castle governments; see G2. | P7, T7 |
| P8 bookmark / designer | FAILS | Sub-mod bookmarks name no Corporation ruler. The designer assigns only tribal/clan/feudal (`V/common/on_action/ruler_designer.txt:147-161`). Reachable by map pick only. | P8 |
| §2 distinctness | FAILS (reskin) | See §2 below | Q1–Q7 |
| §3.1 field validity | MEETS | Every field has a vanilla `.txt` call site: create_cadet_branches/rulers_should_have_dynasty/legitimacy/allow_accolades `GT:7-11`; dynasty_named_realms `:454`; use_as_base_on_landed `:458`; sticky `:462`; disable_regnal_numbers `:816`; royal_court `:14`; city shape `:65-67`; realm_mask `:90-91`. No field appears only in `.info`. | §3.1, §4.6 |
| §3.2 flags | PARTIAL | The identity flag has readers (law :61-67, trigger :22-25, effect :26, on_action :30). The family flag `eotg_government_is_corporate` (GOV:57) has **zero readers** repo-wide. This is a documented exception (`governments_v2.md` §3.1, §13.4), but its consumer, the `eotg_market_faction_cycle` lift, is unbuilt. | §3.2, F5 |
| §3.3 contracts | PARTIAL (min) | Group `eotg_government_contract_groups.txt:27-35`; trees `eotg_government_obligations.txt:147-272`. Five chained levels with ai desire, score and flags copied by position from `V/.../feudal.txt:128-190`. No obligation reads a resource. | §3.3 |
| §3.4 realm laws | MEETS (min) | crown authority via GOV:60 | §3.4 |
| §3.6 holdings | PARTIAL | republic shape, verbatim; a playable city-primary government is untested (V-G17) | §3.6 |
| §3.7 MAA/levies/knights | PARTIAL | `levy_size = -0.15` only (GOV:48) | §3.7 |
| §3.8 decisions/interactions/CBs | FAILS | Debug decisions only (`eotg_government_debug_decisions.txt:41-70`). The "become feudal" decision uses `has_government = feudal_government` (:155), which §5.1.5 forbids. | §3.8 |
| §3.11 resource | FAILS | `eotg_corp_board_influence` is reserved and unbuilt: no variable, no change effect, no init or teardown | Q2, §3.11 |
| §3.13 character_modifier | MEETS | GOV:44-49. All four modifiers have vanilla use (herder `GT:757`, `00_duchy_capital_buildings.txt:1503`, feast modifiers, admin `GT:502`). No top_liege modifier. | §3.13 |
| §3.14 AI / grants | PARTIAL | `use_legends` only (GOV:51-53). No `grant_vassal_ai_will_do` and no `possible_grant_vassal_governments`. The law and every contract level have `ai_will_do`/desire. | §3.14 |
| opinion_of_liege | FAILS (deferred) | absent | Q3 |
| §3.15 resource UI | FAILS | no resource to show | §3.15 |
| §3.16 loc | MEETS | All §3.16 keys are present: loc :17-31, law :65-67, group :308-309, contracts :96-117, flavour :185-207 (23 entries = 23 keys), knight :262-269 (8), debug :290-293. Level `_desc` keys are absent, as in vanilla. | §3.16 |
| Icon | PARTIAL | 70x70, **byte-identical** to vanilla `administrative_government.dds` | §3.16 |
| Text icon | PARTIAL | borrowed `@government_type_administrative!` (loc :21; exists `V/gui/texticons.gui:4645`) | §3.17 |
| §3.18 flavourization | MEETS | `eotg_government_flavorization.txt:307-590`: priority 60/61, `top_liege = no`, no name_lists or heritages, glossary-clean | §3.18 |
| §3.19 on_actions | MEETS (min) | additive (on_actions :10-22); succession net only, no resource init | §3.19 |
| §3.21 knight term | MEETS | `eotg_knight_culture.txt:35-40`. The 7 children diff identical to vanilla `00_knight_culture.txt:91+`. 8 loc keys. | §3.21 |

### §2 Distinctness: what differs from feudal mechanically
- **Holdings:** city-primary instead of castle (GOV:38-40).
- **Character modifiers:** +5% income, +1 diplomacy, -10% build cost, -15% levies (GOV:44-49).
- **Contracts:** default tax 0.15 vs feudal 0.10, default levy 0.10 vs 0.25. The feudal AI tax-desire branches are dropped.
- **Cosmetic:** no regnal numbers, title-named realms (not dynasty-named), own rank names, "Specialist" knights.
- **Same as feudal:**
  - Q1 verb: conquer and inherit;
  - Q2 resource: none;
  - Q3 vassal model: feudal-shaped trees;
  - Q4 succession: single heir;
  - Q5 entry/exit: debug only;
  - Q6 AI: vanilla defaults;
  - Q7 UI: free surfaces only.

This is a **playable feudal reskin**, which is what G1 intended (`governments_v2.md` §1, template §6.1).

### Spec conformance
G1 is built exactly as specified in §5.2, §6.1-6.2, §7.1-7.3, §8, §9 and §10, with the §12 rows in the sub-mod history (`docs/test_submods/british_isles/history/titles/k_brittany.txt:22-26, 152-154`). Everything Corporation-specific in §14 is unbuilt: board influence, the third "board seat" obligation, board election, `eotg_boardroom_war`, and the §14.5 influence probe (T11). The desc (loc :20) promises things no mechanic delivers: directors who "scheme against one another" for the favour of the board, and a board that "plays a slow game of influence".

### BLOCKERS (to call it a playable government per template)
None in script. Playability rests on the unrun CB-49 checks: V-G3, V-G4, V-G9 and V-G17.

### GAPS
- G1 [design, eotg-architect, owner]: the succession/fiction contradiction (Q4). The owner question in template HANDOFF (2) is still open; record the debt or rule on it.
- G2 [design, architect] (**[inferred]**, engine): city-primary leakage. Corporation (and Gob-Corp) share `primary_holding = city_holding` with `republic_government`, and none of the three has a `can_get_government` (`GT:64-92`). If the engine picks a government for a newly landed city ruler by primary holding, any city barony on the map can turn Corporation. T7/V-G11 must check city baronies **outside** Brittany specifically. The prepared guard is `governments_v2.md` §5.6.
- G3 [scripter]: no signature resource, decisions, `opinion_of_liege`, `grant_vassal_ai_will_do`, or entry/exit path (Q2, Q3, Q5).
- G4 [scripter]: `has_government = feudal_government` at `eotg_government_debug_decisions.txt:155` violates §5.1.5. Use `government_has_flag = government_is_feudal`.
- G5 [cartographer]: `docs/test_submods/british_isles/README.md:89` says Konan II (348) holds `k_brittany`. History and the CSV (`isles_assignments.csv:69`) have Hoël (178) as king and Konan as vassal duke. Row :88 is also stale (Philippe vs Raoul). The tester will look for the wrong ruler.

### POLISH
- Comments cite other mods, against the owner rule of 2026-10-11 (mods are not sources): `common/defines/eotg_government_defines.txt:11` (After the End) and `common/customizable_localization/eotg_knight_culture.txt:8-9` (TFE). Owner: scripter.
- `eotg_knight_culture.txt:18` still says "PENDING OWNER", but OQ1 is ruled. `:10` says "7 suffixed loc keys"; there are 8.
- `eotg_government_obligations.txt:12` claims "vanilla AI and opinion logic read" `obligation_high_*`. No script reader exists in `V/common`; this is engine-side and unverified. `:14-15` lists `_desc` keys that are not shipped (vanilla omits them too).
- The law has no `modifier` block (vanilla single heir `:304-309`: player_heir_opinion and so on).
- The icon is placeholder art (art debt).

### Top 3 recommendations
1. **Run CB-49 before any G2 work.** V-G3, V-G4, V-G9 and V-G17, plus V-G11 with city baronies counted outside the seeded realms (G2). If leakage shows, ship the §5.6 guard first.
2. **Build `eotg_corp_board_influence`**: variable, a clamped `eotg_corporation_change_board_influence_effect`, init and teardown in `eotg_gov_on_government_change`, and the §3.15 default display (scaled modifier plus story counter). Add one vassal-tier and one top-tier "deal" decision that move it. Skip T11 unless the owner still wants vanilla influence.
3. **Get the Q4 ruling from the owner.** Either the G2 board election (title law plus `succession_election/`, electors limited to dynasty and house for P1 safety, vote weight read from board influence), or record single heir as debt and rename "Executive Succession" so it does not read as a hereditary CEO.

### Unverifiable without in-game test (`-debug_mode`, British Isles sub-mod)
- **T1 / V-G3:** pick Hoël (178) on the map. No "Is unplayable" and no `GAME_OVER_CANNOT_PLAY_*`.
- **T2 / V-G1:** error.log has no "preregistered modifier type" for `eotg_corporation_government`. `database_conflicts.log` shows `KnightCulture` from `eotg_knight_culture.txt`.
- **V-G4:** the realm screen shows Executive Succession as the only order law, with Primogeniture unavailable.
- **T3 / V-G9:** after the death of Konan II on 1066.12.11, the heir holds `d_brittany` as Corporation and has the law. `kill` Hoël, then repeat with a female or minor heir.
- **T4:** a feudal relative inherits. Record the government.
- **T5 / V-G6 / V-G10 / V-G20:** the contract trees show with loc. An AI liege changes a level. A county is granted to a courtier, and castle barons appear. Record their governments.
- **T6 / V-G16:** debug in and out; the law is added and dropped.
- **T7 / V-G11:** after 50 years, the government map mode shows Corporation only in Brittany and its grants or conquests. Count city baronies elsewhere.
- **T8 / V-G12:** no bankruptcy or law churn.
- **T9 / V-G7 / V-G8 / V-G18:** "CEO Hoël", "Operations Chief" for Konan, "Specialist" knights, the teal map colour.
- **V-G15:** Brittany has a royal court.
- **V-G17:** city capital plus held castle with no invalid-holding penalty; the AI builds.
- **T10:** save and reload.

### Verdict: PASS (pending in-game) as a G1 playable reskin. FAILS the "distinct government" bar of the template (Q1–Q5, §3.8, §3.11).
