# Vanilla research for Unclaimed Regions (vanilla-scout, 2026-10-06)

Input for docs/specs/frontier_unclaimed_regions.md. CK3 1.20.0.3; G = game root.
**Confidence:** file contents and line numbers are verbatim. The following are inferred, not verified:
herder playability, the map-colour source, redirects_wars_to_overlord, the semantics of supply_limit_mult_for_others,
and whether hostile_county_attrition works in county scope.

## 1. Placeholder government
- `herder_government` is at G/common/governments/00_government_types.txt:733-792.
  - government_rules: court_generate_spouses=no, council=no, create_cadet_branches=no,
    rulers_should_have_dynasty=no, uses_county_fertility=yes, replenishes_county_fertility=yes,
    deny_powerful_vassal=yes, redirects_wars_to_overlord=yes, buildings=no, allow_accolades=no.
  - character_modifier: knight_limit -100, county_opinion_add 100, monthly_income_mult -10.
  - ai = { use_lifestyle=no arrange_marriage=no use_goals=no use_decisions=no use_scripted_guis=no use_legends=no
    perform_religious_reformation=no }.
  - flags = { government_is_herder government_has_herd government_is_in_steppe ignores_faith_marriage_penalties };
    mechanic_type = herder.
  - herder_holding parameters: no_buildings, no_levies, county_fertility (00_holdings.txt:199-212).
- **Vanilla herders are real history characters.** G/history/titles/k_angara.txt:15-16 has
  `holder = fictional_kirghiz_19`, `government = herder_government`. Herders die and are replaced.
- **Avoid:** mechanic_type = herder and uses_county_fertility (they bring herd and fertility behaviour, the herd
  defines at 00_defines.txt:132-144, and the MPO flows). Also, the game_start.txt:1254-1263 conversion turns
  herder_government into tribal when the MPO DLC is missing.
- **A custom government WITHOUT mechanic_type works** (it's optional).
  - Useful rules: council, create_cadet_branches, rulers_should_have_dynasty, court_generate_spouses, buildings,
    allow_accolades, deny_powerful_vassal, inherit_from_dynastic_government (no = fenced off, as holy orders are),
    landless_playable.
  - AI flags as above, plus use_great_projects.
  - `supply_limit_mult_for_others` (_governments.info:434-438) applies to army owners of a different government
    type. Vanilla uses -0.5 for tribal (:199) and wanua (:272). **This is the best attacker-only attrition knob.**
- Playability: only loc evidence: government_l_english.yml:285 `government_is_herder: "Is unplayable"`
  (shared with mercenary and holy_order). This is engine behaviour.

## 2. Immunity
- **War.** Nearly every CB group (00_casus_belli_groups.txt: 19,39,50,58,70,77,89,95,105,115,126,136,160,166,178,186,194)
  uses `herders_and_tributary_constraints = yes`. That trigger (00_war_and_peace_triggers.txt:1144-1160) blocks
  defenders with government_has_flag = government_is_herder.
  - The `independence` (150) and `migration` (171) groups are not covered.
  - Options:
    - reuse the government_is_herder flag (side effects across about 40 vanilla files);
    - or override that scripted trigger with our own flag (a non-additive vanilla override).
- **Vassalization and offers.** `cannot_be_vassal_or_liege` (a flags entry; mercenary and holy order use it) is
  checked in 00_character_interactions.txt:55,577, 00_grant_titles_interaction.txt:33,
  00_tributary_interactions.txt:273,904,4483, and the CB types (00_tributarize.txt:20-30).
- **Events.** There is no "hidden dummy" pattern. Yearly pulses need basic_is_valid_for_yearly_events_trigger
  (00_available_for_events_triggers.txt:802-816), which includes is_playable_character = yes.
- **Buildings and levies:** buildings = no, plus holding parameters. AI marriage: ai arrange_marriage = no (others can
  still propose). Schemes: not blocked generically.

## 3. Game start
- There is no vanilla county without a holder. The _governments.info `fallback` comment suggests the engine fills
  empty counties itself; this project saw it generate rulers (2026-10-05 test variant D).
- **History can assign a county to a history character, with `government =` (the k_angara pattern).**
- The script creation pattern is 09_dlc_mpo_scripted_effects.txt:6650-6710: create_character (template) →
  create_title_and_vassal_change { type = granted add_claim_on_loss = no } → change_title_holder_include_vassals →
  resolve_title_and_vassal_change → change_government.

## 4. Map colour
- The political map mode is engine-driven (map_modes.txt:276-277 color_mode = realms). Inference: the realm colour
  comes from the top liege's primary title, so an independent count shows its county title colour.
- Runtime effects: `set_color_from_title = <title>` (00_major_decisions_scripted_effects_3.txt:233,
  01_puppet_interactions.txt:1938) and `set_title_color = { r g b }` (00_major_decisions_scripted_effects.txt:254).
- **Plan:** give unclaimed county titles a neutral colour in landed_titles; on claim, recolour. Persistence in
  saves is unverified.

## 5. Claiming
- create_title_and_vassal_change (type granted 191 uses; usurped/conquest for a warlike flavour) +
  change_title_holder + resolve.
- The old holder stays alive. Remove it with death = { death_reason = death_vanished } (00_event_deaths.txt:224;
  00_nomadic_faction.txt:383).

## 6. Attrition
- `hostile_county_attrition` (00_definitions.txt:2191) is a character modifier on the army owner. There is no
  county-scope precedent.
- supply_limit / supply_limit_mult: province or county, symmetric (they hit everyone).
  - Examples: terrain (00_terrains.txt:100,129), county corruption modifier -0.3
    (00_county_corruption_modifiers.txt:16), epidemics.
  - MINIMUM_SUPPLY_LIMIT = 1000; attrition only starts when supply is at 0 (00_defines.txt:655-681).
- **supply_limit_mult_for_others is the only attacker-targeted knob** (government field). Its scope semantics are
  untested.

## Risks we can't control
1. Playability and event pulses are hard-coded.
2. War immunity needs a trigger override; independence and migration still apply.
3. Vanilla `has_government = herder_government` checks won't see a custom government.
4. The engine's empty-county behaviour.
5. The map-colour source and whether it persists.
6. The attrition semantics, and the 1000 supply floor.
7. Leftover placeholder characters if they aren't vanished.
8. Tiger and PX don't validate 1.20 government fields.
