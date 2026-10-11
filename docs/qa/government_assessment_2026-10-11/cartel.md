## QA report: Cartel government (eotg_cartel_government), deep assessment, 2026-10-11
Tools: PX LSP 0 real findings (6 known-benign building_walls_*). px_vocab 0 findings. eotg_lint 0 (0 new). Tiger was not run, as instructed. Logs: scratchpad/govassess/cartel_{px_lsp,vocab,lint}.txt
Key: V/ = vanilla game root. GT = 00_government_types.txt. GI = _governments.info. TI = 00_tributary_interactions.txt.

### Scorecard
| Area | Verdict | Evidence | Ref |
|---|---|---|---|
| P0 not on the playable blacklist | MEETS | flags at cartel:66-72. None of the flags blocked at V/common/scripted_rules/00_rules.txt:157-208 | §1 P0 |
| P1/P2 dynastic | MEETS | cartel:35-36. inherit_from_dynastic_government is left unset | P1, P2 |
| P3 succession law | MEETS (untested, V-G4) | own law at laws:121-150. Safety net at effects:42-50 and on_actions:10-51. Every vanilla order law rejects the Cartel (00_law_triggers.txt:268-280, 343-397). Gender laws are not government-gated | P3, §3.5 |
| P5 heir keeps the government | MEETS (untested) | cartel:40-41. Per GI:73-77, use_as_base_on_landed copies the government of the old holder, so a courtier granted a Cartel-held county becomes Cartel | P5 |
| P6 GOVERNMENT_TYPES | MEETS | All 20 vanilla keys match 00_defines.txt:550-573 exactly. Key at defines:45. The sub-mod copy is in step (it adds only the offmap key) | P6 |
| P7 can_get_government / fallback | PARTIAL | Neither is set, which is correct (no fallback). Leakage is untested (T7) | P7 |
| P8 bookmark / designer | FAILS (accepted) | The sub-mod bookmarks use vanilla governments only (bookmarks/00_bookmarks.txt:22-90). Map pick only | P8, §4.4 |
| P10 DLC | MEETS | Offer Tributary Status is_available has no DLC gate (TI:4463-4470) | P10 |
| Tribute lapse on death | CONFIRMED in script; engine behaviour unverified | TI:4628 → mandala_embrace_tributary_effect (tgp_mandala_scripted_effects.txt:2130) → start_tributary_interaction_effect falls through to the final else (00_interaction_effects.txt:2981-2984) → tributary_subjugated with suzerain_heir_succession = no (subject_contract_groups.txt:103-106) | spec §5.4 |
| §3.1 field validity | MEETS | Every field has a vanilla .txt call site: GT:7-25, 458, 462, 934, 938, 60-61. Nothing is .info-only. allow_accolades, vassal_contract_group and realm_mask_* are vanilla-only fields and valid | §3.1, §4.6 |
| §3.2 flags | MEETS | Identity flag read in 7 places. No government_is_feudal. Crown authority 1 grants can_have_tributaries (00_realm_laws.txt:64, cumulative group) | §3.2 |
| §3.3 contracts | MEETS (min) | groups:47-55. Trees at obligations:403-529 match spec §6 numbers. AI desire is flat (no feudal branch) | §3.3 |
| §3.4 laws, §3.6 holdings | MEETS (min) | crown authority. Castle shape cartel:49-51 = GT:18-20 | §3.4, §3.6 |
| §3.7 MAA / levies / knights | FAILS (min) | No military line in character_modifier (cartel:55-60) | §3.7 |
| §3.8 decisions / interactions | PARTIAL | Only vanilla Offer Tributary Status, plus a debug decision (debug_decisions:106-134) | §3.8 |
| §3.13 character_modifier | MEETS | cartel:55-60. No top_liege_character_modifier | §3.13 |
| §3.14 AI / grants | PARTIAL | use_legends only. No grant_vassal_ai_will_do or possible_grant_vassal_governments | §3.14 |
| §3.15 GUI | MEETS | Dread uses the vanilla UI | §3.15 |
| §3.16 loc | MEETS | 15 government keys (loc:47-61), 3 law keys (:71-73), 22 contract keys (:140-161), group (:312-313), 25 rank keys (:231-253), 8 knight keys (:278-285). BOM present. No [scope:. No duplicates | §3.16 |
| Icon | PARTIAL | 70×70, byte-identical to vanilla clan_government.dds | §3.16 |
| Text icon | PARTIAL | Borrows @government_type_clan! (loc:51), which exists at V/gui/texticons.gui:4715 | §3.17 |
| Flavourization | MEETS | flavorization:885-1158. All three ladders present, top_liege = no, priority 60/61 | §3.18 |
| on_actions | MEETS (min) | Additive only. Succession net only; no resource init (dread needs none) | §3.19 |
| Knight term "Brute" | MEETS | knight_culture:47-52. All 7 child suffixes match vanilla | §3.21 |
| Q1 core verb | PARTIAL | Only "tribute" differs from feudal, and it is the vanilla mandala interaction | §2 Q1 |
| Q2 resource (dread) | PARTIAL | Gain +25% and decay +25% (cartel:58-59). No source or sink of its own | Q2, §3.11 |
| Q3 vassal model | PARTIAL | Feudal-shaped trees. No opinion_of_liege | Q3 |
| Q4 succession fits identity | PARTIAL | Primogeniture, but named "Council Succession" | Q4 |
| Q5 entry / exit | FAILS | Debug decisions only | Q5 |
| Q6 AI | PARTIAL | Vanilla tribute AI. Nothing reads dread | Q6 |

**What actually differs from feudal:**
- It drops government_is_feudal, so no feudal special contracts and no partition.
- ask_for_tribute and count_tributaries_for_title_requirements (cartel:42-43).
- It spreads via use_as_base_on_landed and sticky_government.
- dynasty_named_realms = no.
- intrigue +2, diplomacy -2, dread ±25%.
- Its own tax curve, up to 0.30.
- Its own ranks, knight term and colour.

Everything else is feudal. In short, it is a reskin with one borrowed mechanic.

### BLOCKERS
None at the static level. Every playability "MEETS" is unproven until CB-49 runs.

### GAPS
1. **Dread and tribute never touch** (owner: eotg-architect). The two pillars of the government are disconnected:
   - The interaction costs **piety** (TI:4532-4562).
   - The AI accepts based on mandala radiance, piety level (mandala-only, tgp_mandala_scripted_modifiers.txt:18-27), military threat, tier and faith (TI:4737-4950). **Nothing reads dread.**
   - A Cartel offering tribute gets base -50 and none of the positive mandala terms. Expect few acceptances.
2. **Dread has no Cartel source or sink** (architect). Faster decay is a penalty: vanilla uses negative dread_decay_mult as a bonus (court_positions:6853-6869). Net effect: more churn, not more identity.
3. **The tribute network is lost every generation** (architect). suzerain_heir_succession = no, the heir must pay piety again, and the AI acceptance odds are low (gap 1). Combined, the signature expansion may never accumulate. Measure it in V-G12/V-G13.
4. **No entry or exit decisions** (Q5). Debug only (architect, then scripter).
5. **Succession contradicts the fiction** (architect, then localizer). The law is "Council Succession" with subname "Oldest Child Inherits" (loc:71-72), under a description that says "A council of bosses rules" (loc:50). Either rename the law or build the G2 takeover law.
6. **Missing per §3.7, §3.14, §3.1:**
   - no military modifier;
   - no top_liege_character_modifier;
   - no opinion_of_liege;
   - no grant_vassal_ai_will_do or possible_grant_vassal_governments.

   Owner: architect.
7. **P8:** no bookmark entry (cartographer, optional).

### POLISH
- **"Tribute" means two things** (localizer). "Territory Tribute / Massive Tribute" is the *levy* obligation (loc:151-161, soldier_icon at obligations:469), while the realm also has real tributaries. Suggest "Turf Levy".
- **The icon and text icon are clan copies**, so the Cartel reads as Clan in the character window (human art).
- **Comments cite other mods**, which the owner rule of 2026-10-11 forbids:
  - defines:11 cites After the End;
  - knight_culture.txt:8-9 cites TFE.

  Also, knight_culture.txt:18 still says "PENDING OWNER", but OQ1 was ruled on 2026-10-08. Owner: scripter.
- **has_government = feudal_government** at debug_decisions:155. This is a §5.1 item 5 / §4.3 exception; it is debug-only.
- **The empire title rank "Cartel"** (loc:235) duplicates the government name. Acceptable, noted.

### Spec conformance (governments_v2 §5.4, §6, §8, §10)
- The block matches §5.4 line for line.
- deny_powerful_vassal is absent, as ruled. Note that mandala sets it at GT:936.
- No mechanic_type. The interaction is confirmed to read only government_allows = ask_for_tribute (TI:4464).
- Contract numbers match the §6 table.
- Ranks match the §8 table.
- B2 vocabulary: clean.
- **One spec inaccuracy (architect):** §5.4 says the tributary group is chosen in start_tributary_interaction_effect. That is true, but it is reached through mandala_embrace_tributary_effect, which also fires char_interaction.0362 and consume_all_criminal_reasons_effect. Benign, but undocumented.
- **Fiction fit:**
  - The description is canon-safe, names no nation and is in Canadian English.
  - Weak points: dread versus piety-paid tribute (gap 1), and the "council" versus primogeniture mismatch (gap 5).

### Top 3 recommendations
1. **Run CB-49 for the Cartel first**: T1-T3 and V-G13 on k_leon. Every playability verdict rests on them.
2. **G2: couple dread to tribute** (architect). A Cartel-gated tribute interaction that costs or scales on dread, in place of piety, plus at least one dread-spending decision. The alternative route is a §16-style key override of the acceptance path, but an own interaction is cleaner.
3. **Fix the loc and succession mismatch now** (localizer). Rename "Council Succession" and "Territory Tribute". Record the takeover law as G2 debt.

### Unverifiable without an in-game test
- **T1:** pick Alfonso VI (k_leon). There should be no GAME_OVER tooltip and no remap.
- **T2:** error.log has nothing from the Cartel files. database_conflicts.log shows the KnightCulture override.
- **T3 + V-G4:**
  - At start, the law window shows "Council Succession" and not partition.
  - kill Alfonso. The heir is Cartel, holds the law, and play continues.
  - Repeat with a female heir.
- **T4:** the heir is a landed feudal relative. Record the resulting government.
- **T5:** grant a Cartel-held county to a courtier. Expect Cartel (GI:73-77).
- **T6:** debug in and out. The law is added and then dropped.
- **T7:** 50-year observer run. Cartel appears only in seeded realms and their grants.
- **T8:** record the AI Cartel dread level over time. Check whether +25% decay pins it near 0.
- **V-G13:**
  - Offer Tributary Status to Toledo, Cordoba, Gipuzkoa and Barcelona. A piety cost is shown.
  - The result is tributary_subjugated.
  - Tributary land counts toward title creation.
  - kill the ruler and confirm the tribute lapses. Record whether the heir AI re-offers within 5 years, and its acceptance rate.
- **New:** the realm-window "tributarization chance" map mode that ask_for_tribute enables (GI:265-266). Check that it renders sensibly without radiance.
- **T9:**
  - Rodrigo reads "Ringleader".
  - An independent ruler reads "Grand Underlord" at any tier.
  - "Brute" appears in the Knights tab and in lowercase, plural and possessive forms.
  - The map colour is crimson.
- **T10:** save, then reload.

### Audits run: §5.1 items 2-8 (PX LSP, vocab, lint, hand field check, defines diff, flag/has_government grep, loc BOM/dupes/scope, ai_will_do present on law and contract levels). Skipped: Tiger (instructed); events/reachability (none exist for the Cartel).
### Verdict: PASS (pending in-game). A playable feudal reskin with a borrowed tribute mechanic. It is not yet distinct, because dread and tribute are uncoupled.
