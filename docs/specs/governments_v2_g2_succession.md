# Spec: Governments v2, G2 succession (CB-53): elective succession for the Corporation, Trade Oligarchy and Cartel

**Author:** eotg-architect, 2026-10-20. **Status:** draft. Next: eotg-scripter (batch SU1), then eotg-localizer (SU2), then eotg-qa (SU3, in game).
**Ruling:** CB-53, owner, 2026-10-20: build elective succession laws for the governments whose fiction contradicts single-heir succession. Assess the PMC separately.
**Parent specs:** `docs/specs/governments_v2.md` §5, §7.1–7.2, §11; `docs/specs/government_template.md` §1.1 (P1, P3, P5) and §9.2 item 6; `docs/specs/governments_v2_g2_cartel.md` §2.2, §6.3 and the row at :475. **Assessment:** `docs/qa/government_assessment_2026-10-11/` (corporation.md :15, :78; gobcorp.md :19, :43, :66; cartel.md :35, :61; pmc.md :21, :65).
**Vanilla:** CK3 **1.20.1.1**. `G/` means `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/`.

---

## 1. Purpose & gate

Three governments are told as collective rule but pass everything to the oldest child:
- the Corporation: "run by a board", law "Executive Succession";
- the Trade Oligarchy (`eotg_gobcorp_*`): "no single head", law "Charter Succession";
- the Cartel: "a council of bosses", law "Council Succession".

This pass turns each of those three laws into an **election**. The government's own electors choose the successor from the ruler's **dynasty**, so a player always continues as a member of their own dynasty (template P1). Each election script weights votes by what that government values:
- the Corporation by seats on the board;
- the Trade Oligarchy by wealth;
- the Cartel by fear.

The PMC keeps single heir with corrected text (§11).

**Gate: 2, under the mod-exclusive exemption** (owner, 2026-10-08; `CLAUDE.md`). **Not blocked by Gate 1.** All script is map-agnostic: no title, province, culture, faith or character key. It is tested on the British Isles sub-mod:
- Corporation: Hoël, k_brittany, with Konan of d_brittany below him;
- Trade Oligarchy: Bertrand, d_provence;
- Cartel: Alfonso, k_leon, with Rodrigo of d_asturias and Pedru of c_pravia below him (`isles_assignments.csv:69-77`).

**Soft dependency: CB-49.** The G1 in-game checks V-G3 and V-G4 should pass first, because this pass changes the law that V-G4 inspects. SU1 can be built and statically checked now.

---

## 2. Signature resource

**The vote: `elector_vote_strength` in each election script.** Every elector's weight and every AI vote reads the government's own measure of standing. Where that measure is a G2 resource, the vote reads the resource.

| Government | Vote weight reads | Status of the resource |
|---|---|---|
| Cartel | **`dread`**: the elector's dread raises their own weight, and the holder's dread makes intimidated bosses follow the holder's pick (§5.3) | built (`governments_v2_g2_cartel.md` §2) |
| Corporation | a board seat: being a councillor or a powerful vassal | `eotg_corp_board_influence` is reserved (`governments_v2.md:73`) and not built. Its G2 pass replaces the proxy modifier `eotg_corporation_su_vote_board` with a read of the variable. |
| Trade Oligarchy | `gold` | `eotg_gobcorp_market_share` is reserved (`governments_v2.md:35`: "vote weight is derived from it") and not built. Its G2 pass replaces `eotg_gobcorp_su_vote_wealth_*` with a read of the variable. |

**No events** are added (owner rule). The pass therefore has no flavour events that would need to move the resource. Suggested events for the owner are listed in §12.

---

## 3. Mechanism decision: realm law with `order_of_succession = election`

### 3.1 Options

| | A. Realm law election (**chosen**) | B. Title law election ("crown law") | C. Realm law appointment |
|---|---|---|---|
| Shape | `theocratic_elective_succession_law`: a `succession_order_laws` law with `order_of_succession = election`, `election_type`, `can_title_have = { always = yes }` (`G/common/laws/00_succession_laws.txt:727-765`) | `feudal_elective_succession_law` in `title_succession_laws`, put on a title with `add_title_law` (`G/common/laws/01_title_succession_laws.txt:2-34`; `G/common/on_action/game_start.txt:2490`) | `meritocratic_*` / `celestial_*` appointment (`00_succession_laws.txt:1333+, 1711+`; `G/common/succession_appointment/`) |
| Whole realm passes together | **yes**: every title resolves through the same realm law (see 3.2) | **no**: only titles carrying the law are elected. Domain counties stay on the realm law (oldest child), so the realm **splits** whenever the winner is not the oldest child. | yes (`keep_top_tier_titles_together`) |
| Tier | every tier, so a count is covered too | duchy and up (`can_title_have_law_general_trigger`, `G/common/scripted_triggers/00_law_triggers.txt:545-548`) | every tier |
| Vote window | `window_title.gui:2563` shows the vote button whenever `Title.HasSuccessionOrder('election')` | yes | none: a score list plus influence investment, which is admin-coded |
| Existing whitelists, safety net, keys | **unchanged**: the same three law keys get a new `succession` block | a second law per title to add, keep and clean up | unchanged keys |
| Save migration | none (§8) | a title-law back-fill | none |
| Risk | `_laws.info:366-385` lists `election` as "Title only". Vanilla contradicts it with a realm-group election law, and **vanilla wins** (`CLAUDE.md` precedence). Unverified outside PAM: V-SU1. | the split | no vote, so it fails the ruling |

**A is chosen.** It is the only option that is elective and never splits the realm.

**Reported contradiction:** `G/common/laws/_laws.info:366-385` ("Title only: … election") against `00_succession_laws.txt:727-765` (a realm law using election) and the realm-level hooks below. Follow vanilla, and let V-SU1 confirm it.

### 3.2 Why A is expected to work
- **A realm-group law with `order_of_succession = election` exists and is in use.** `theocratic_elective_succession_law` (`00_succession_laws.txt:727-765`) is added as a **realm** law with `add_realm_law_skip_effects` (`G/common/on_action/game_start.txt:2546`, `G/common/on_action/title_on_actions.txt:319-322`) and in history (`G/history/characters/italian.txt:738`).
- **Title-scope succession checks resolve the holder's realm laws.**
  - `has_order_of_succession`: "resolves the holder's realm laws" (`G/common/scripted_triggers/pam_scripted_triggers.txt:459`).
  - The grandeur branch "Grandeur in elective realms" (`G/common/on_action/death.txt:323-334`) tests `primary_title = { has_order_of_succession = election }`. This is what a realm-law election makes true.
- **Shape to copy verbatim:** the theocratic law sets `can_title_have = { always = yes }`, sets **no** `can_realm_have`, and sets `flag = elective_succession_law` and `title_allegiance_opinion = 10`. The mod laws copy all four.
- **Every title elects the same person.** No elector set, candidate set or score in §5 reads `scope:title`. They read only `scope:holder`, `scope:candidate` and `scope:holder_candidate`. So if the engine runs one election per held title, all of them have the same electors, candidates and AI votes, and the same winner. The only exception is a player who deliberately nominates differently on different titles. That is the player's choice, and V-SU2 records it.

### 3.3 Fallback if V-SU1 or V-SU2 fails
1. **First fallback: C, appointment.** It is realm-wide and has no split. The owner must re-rule, because there is no vote (OQ3).
2. **Second fallback: B, title law.** It needs the domain-split behaviour measured, plus a title-law back-fill in the safety net.

The architect writes the fallback as an addendum. Nothing is built speculatively.

---

## 4. Identifier table

| Type | Key | File | Owner |
|---|---|---|---|
| election type | `eotg_corporation_elective` | `common/succession_election/eotg_government_elections.txt` | scripter |
| election type | `eotg_gobcorp_elective` | same | scripter |
| election type | `eotg_cartel_elective` | same | scripter |
| character set (electors) | `eotg_corporation_electors_holder`, `eotg_corporation_electors_board` | same | scripter |
| character set (electors) | `eotg_gobcorp_electors_holder`, `eotg_gobcorp_electors_princes` | same | scripter |
| character set (electors) | `eotg_cartel_electors_holder`, `eotg_cartel_electors_bosses` | same | scripter |
| character set (candidates) | `eotg_<gov>_candidates_dynasty`, `eotg_<gov>_candidates_fallback` (×3 governments) | same | scripter |
| law (**edited in place**, key unchanged) | `eotg_corporation_succession_law`, `eotg_gobcorp_succession_law`, `eotg_cartel_succession_law` | `common/laws/eotg_government_succession_laws.txt` | scripter |
| law (script unchanged) | `eotg_pmc_succession_law` | same | — |
| scripted trigger | `eotg_gov_su_dynastic_candidate_trigger` (root = candidate; reads `scope:holder`) | `common/scripted_triggers/eotg_government_triggers.txt` | scripter |
| scripted trigger | `eotg_gov_su_holder_has_dynastic_candidate_trigger` (root = holder) | same | scripter |
| scripted trigger | `eotg_gov_su_fallback_candidate_trigger` (root = candidate) | same | scripter |
| scripted trigger | `eotg_corporation_su_board_member_trigger`, `eotg_gobcorp_su_prince_trigger`, `eotg_cartel_su_boss_trigger` (root = elector) | same | scripter |
| script value | `eotg_corporation_su_board_priority_value` | `common/script_values/eotg_government_succession_values.txt` (new file) | scripter |
| script value | `eotg_corporation_su_candidate_skill_value` | same | scripter |
| script value | `eotg_gobcorp_su_prince_priority_value` | same | scripter |
| script value | `eotg_gobcorp_su_candidate_wealth_value` | same | scripter |
| script value | `eotg_cartel_su_candidate_menace_value` | same | scripter |
| loc (vote and score tooltips) | §9.2 | `localization/english/eotg_government_l_english.yml` | localizer |

**No new scripted modifiers, effects, on_actions, variables, flags or events.** The per-government MTTH modifiers are written inline in the election file. The vanilla scripted modifiers are reused by name (§5.4), so `common/scripted_modifiers/` is **not** added to the mod.

**Placement table update (orchestrator, `CLAUDE.md`):** add `common/succession_election/` (shape: vanilla folder, `_succession_election.info`).

---

## 5. The three elections

**General shape** (cite for the scripter): `G/common/succession_election/02_gaelic_elective.txt:9-123` (Tanistry; dynasty-only candidates at `:113-121`). The `max` and `priority` on electors come from `01_princely_elective.txt:62-150` (`max = 8` at `:63`, `priority` MTTH at `:92-150`). Fields are listed in `_succession_election.info`.

**Engine rules that apply to all three** (`_succession_election.info`):
- only rulers can be electors;
- the current holder is never a candidate;
- the gender and faith laws filter candidates on top of script. Vanilla `male_preference_law` stays the default gender law.

### 5.0 Shared candidate filter (P1: play continues)

`eotg_gov_su_dynastic_candidate_trigger` (root = candidate, `scope:holder` set):
```
save_temporary_scope_as = potential_candidate                          # as 00_elective_triggers.txt:239-240
exists = dynasty
dynasty = scope:holder.dynasty                                         # P1: never outside the dynasty
OR = {                                                                 # no government erosion through the vote
    is_ruler = no                                                      # unlanded: takes the government via use_as_base_on_landed (governments_v2.md §5.0)
    has_same_government = scope:holder                                 # as 00_elective_triggers.txt:160-164
}
OR = {                                                                 # in the realm, unlanded, or the title is independent; shape :241-258
    is_ruler = no
    any_liege_or_above = { this = scope:holder }
    scope:holder = { top_liege = this }
}
NOT = { any_heir_title = { holder ?= { has_unelectable_government_trigger = yes } } }   # :259-265
has_unelectable_trait_trigger = no                                     # vanilla, 00_elective_triggers.txt:16-29
has_unelectable_government_trigger = no                                # :31-38
```
- **Deviation from Tanistry:** the grandchild block (`:267-325`) is **omitted**. A corporate board or a council of bosses picks among the whole house, so a grandchild may stand while their parent lives.
- **Deviation from vanilla's landed-candidate rule:** a landed candidate must share the holder's government. Without this, a feudal cousin elected to a Cartel throne turns the realm feudal, and `can_keep` then drops the law (`governments_v2.md` §7.2). Vanilla uses the same test for landed candidates (`:160-164`).

`eotg_gov_su_holder_has_dynastic_candidate_trigger` (root = holder; only ever called as `scope:holder = { … }` from inside an election, where the engine has set `scope:holder`):
```
dynasty ?= {
    any_dynasty_member = {
        this != scope:holder
        eotg_gov_su_dynastic_candidate_trigger = yes     # reads the engine's scope:holder; never re-save it
    }
}
```
**Cost:** it iterates the dynasty once per fallback-set character, and that set is only same-government direct vassals. This is acceptable, and Tanistry already iterates `holder_dynasty`. The scripter orders the fallback limit so the cheap checks (`is_vassal_of`, `has_same_government`) run before this trigger.

`eotg_gov_su_fallback_candidate_trigger` (root = candidate), in this order:
- `is_vassal_of = scope:holder`, `has_same_government = scope:holder`;
- `scope:holder = { eotg_gov_su_holder_has_dynastic_candidate_trigger = no }`;
- the vanilla `has_unelectable_*` triggers are `no`.

**The fallback set fires only when the dynasty has no valid member.** That is the case where single heir would also end a player's game. It keeps AI realms alive instead of handing the title to the engine's default. It never applies while a dynastic candidate exists, so P1 holds.

Each election's `candidates` block:
```
candidates = {
    character_sets = {
        eotg_<gov>_candidates_dynasty  = { type = holder_dynasty         limit = { eotg_gov_su_dynastic_candidate_trigger = yes } }  # gaelic :115-120
        eotg_<gov>_candidates_fallback = { type = holder_direct_vassals  limit = { eotg_gov_su_fallback_candidate_trigger = yes } }
    }
    # candidate_policy defaults to include_all_candidates (.info)
}
```

### 5.1 Corporation, `eotg_corporation_elective`: the board

**Fiction:** the board seats the next chief from the house, and judges candidates on administration and dealing.

**Electors.** At most 7: the chair plus six directors. Set `max = 7`, as in princely `:63`.
```
electors = {
    max = 7
    character_sets = {
        eotg_corporation_electors_holder = { type = holder }
        eotg_corporation_electors_board  = { type = holder_direct_vassals  limit = { eotg_corporation_su_board_member_trigger = yes } }
    }
    priority_value = eotg_corporation_su_board_priority_value
}
```
- `eotg_corporation_su_board_member_trigger`: `is_vassal_of = scope:holder`, plus `OR = { is_councillor_of = scope:holder  is_powerful_vassal_of = scope:holder }`.
  - Vanilla call sites: `is_councillor_of`, `G/common/activities/activity_types/chariot_race.txt:1112`; `is_powerful_vassal_of`, `G/common/activities/intents/shared_intents.txt:458`.
  - **Not `holder_council_members`.** That set type is listed in `.info` but has no vanilla call site, and the 2026-10-08 lesson is that `.info` alone is not proof. A councillor who is unlanded cannot vote anyway ("only rulers can be electors").
- `eotg_corporation_su_board_priority_value` (root = elector):

  | Condition | Add |
  |---|---|
  | `this = scope:holder` | 200 (princely `:94-97`) |
  | councillor | 50 |
  | powerful vassal | 30 |
  | per tier | `highest_held_title_tier × 5` |

**Vote strength** (`elector_vote_strength`, MTTH; desc keys in §9.2):

| Modifier | Add | Condition |
|---|---|---|
| base | 1 | |
| `eotg_gov_su_vote_chair` | +1 | `this = scope:holder` |
| `eotg_corporation_su_vote_board` | +1 | councillor of the holder (**the board-influence hook**, §2) |
| `tooltip_feudal_vote_strength_powerful_vassal` (vanilla loc) | +1 | powerful vassal (`00_feudal_elective.txt:35-49`, without the military-strength bonus) |
| `tooltip_feudal_vote_strength_king_tier` / `_duke_tier` (vanilla loc) | +2 / +1 | tier (`00_feudal_elective.txt:25-34`) |

**AI vote** (`candidate_score`, MTTH, base 0):
- vanilla `elector_self_voting_pattern_feudal_elective_modifier`;
- vanilla `holder_voting_pattern_feudal_elective_modifier`;
- vanilla `elector_voting_pattern_traits_feudal_elective_modifier`;
- vanilla `elector_voting_pattern_opinion_feudal_elective_modifier`;
- `eotg_corporation_su_score_skill`: add `eotg_corporation_su_candidate_skill_value`, which is `(scope:candidate.stewardship + scope:candidate.diplomacy) × 1.5 + scope:candidate.intrigue × 0.5`, capped at 60;
- `eotg_gov_su_score_minor`: −40 if `scope:candidate.is_adult = no`.

Where these are defined: `G/common/scripted_modifiers/00_elective_successions_scripted_modifiers.txt` `:1`, `:188`, `:929` and `:2199`.

### 5.2 Trade Oligarchy, `eotg_gobcorp_elective`: the richest princes

**Fiction:** the charter counts money. The richest Princes vote, and they favour a candidate who can keep the books and the market.

**Electors.** At most 9: the First Prince plus the eight richest. Set `max = 9`.
```
electors = {
    max = 9
    character_sets = {
        eotg_gobcorp_electors_holder  = { type = holder }
        eotg_gobcorp_electors_princes = { type = holder_direct_vassals  limit = { eotg_gobcorp_su_prince_trigger = yes } }
    }
    priority_value = eotg_gobcorp_su_prince_priority_value
}
```
- `eotg_gobcorp_su_prince_trigger`: `is_vassal_of = scope:holder`, `gold > 0`.
- `eotg_gobcorp_su_prince_priority_value`: 1000 if the holder, otherwise `gold`, clamped to 0–999. **This is the wealth sort.**

**Vote strength:**

| Modifier | Add | Condition |
|---|---|---|
| base | 1 | |
| `eotg_gov_su_vote_chair` | +1 | holder |
| `eotg_gobcorp_su_vote_wealth_1` | +1 | `gold >= 100` |
| `eotg_gobcorp_su_vote_wealth_2` | +1 | `gold >= 300` |
| `eotg_gobcorp_su_vote_wealth_3` | +1 | `gold >= 1000` |

The wealth modifiers are **the market-share hook** (§2). A G2 Trade Oligarchy pass replaces the gold reads with `var:eotg_gobcorp_market_share` bands.

**AI vote:**
- the same four vanilla patterns as §5.1;
- `eotg_gobcorp_su_score_wealth`: add `eotg_gobcorp_su_candidate_wealth_value`, which is `scope:candidate.stewardship × 2` (cap 40) plus `scope:candidate.gold / 25` (cap 20);
- `eotg_gov_su_score_minor` (−40).

### 5.3 Cartel, `eotg_cartel_elective`: the bosses, weighted by fear

**Fiction:** the council of bosses decides. A feared Overboss gets his pick, and a weak one has it taken from him.

**Electors.** No cap: every boss votes.
```
electors = {
    character_sets = {
        eotg_cartel_electors_holder = { type = holder }
        eotg_cartel_electors_bosses = { type = holder_direct_vassals  limit = { eotg_cartel_su_boss_trigger = yes } }
    }
}
```
- `eotg_cartel_su_boss_trigger`: `is_vassal_of = scope:holder`, plus `OR = { highest_held_title_tier >= tier_county  is_councillor_of = scope:holder }`.
- Barons are excluded, as Tanistry excludes them ("vassals above the rank of baron", `succession_laws_l_english.yml:78`).
- A count-tier Cartel with no bosses lets the holder decide alone. That fits a crew boss.

**Vote strength (reads the resource):**

| Modifier | Add | Condition |
|---|---|---|
| base | 1 | |
| `eotg_gov_su_vote_chair` | +1 | holder |
| `eotg_cartel_su_vote_dread_1` | +1 | `dread >= low_dread` (20) |
| `eotg_cartel_su_vote_dread_2` | +1 | `dread >= medium_dread` (40) |
| `eotg_cartel_su_vote_dread_3` | +1 | `dread >= high_dread` (80) |

The thresholds are `G/common/script_values/00_basic_values.txt:993-995`, and the dread modifiers apply to the holder too. A feared Overboss carries up to 5 votes. A boss with no fear behind him carries 1.

**AI vote:**
- the same four vanilla patterns;
- `eotg_cartel_su_score_follow_fear`: add 30 if `scope:candidate = scope:holder_candidate`, the elector `has_dread_level_towards = { target = scope:holder level = 1 }`, and the elector is not the holder. Add **another** 30 at `level = 2`. Trigger shape: `00_tributary_interactions.txt:3847-3863`. **This is the dread–succession link.**
- `eotg_cartel_su_score_menace`: add `eotg_cartel_su_candidate_menace_value`, which is `scope:candidate.dread / 3` (cap 30) plus `scope:candidate.prowess × 1.5` (cap 30);
- `eotg_gov_su_score_minor` (−40).

**Compatibility with Cartel G2** (`governments_v2_g2_cartel.md` §2.2, §6.3; `common/on_action/eotg_cartel_on_actions.txt:95-110`):
- The succession grace is set on `primary_heir` in `on_death`. Under an election, `primary_heir` is the current leader of the vote, and the vote is resolved at death with those same votes. So the grace lands on the actual successor.
- Payer contracts follow the suzerain's primary heir (`suzerain_heir_succession`), so they land on the same person.
- **No change to the Cartel files.** V-SU7 verifies both points.

### 5.4 Vanilla scripted modifiers reused
`elector_self_voting_pattern_feudal_elective_modifier` (`:1`), `holder_voting_pattern_feudal_elective_modifier` (`:188`), `elector_voting_pattern_traits_feudal_elective_modifier` (`:929`), `elector_voting_pattern_opinion_feudal_elective_modifier` (`:2199`).

**Not reused:**
- `_circumstances_feudal_` reads title gender laws and feudal circumstances;
- `_circumstances_misc_` is feudal-specific;
- `_prestige_piety_` (`:842`) would pull Cartel and Corporation votes towards piety, which is off-fiction.

**Tiger note:** these modifiers touch `rite`. Expect the known-benign `rite` / strict-scopes family listed in `CLAUDE.md`, not new errors.

---

## 6. The laws (edited in place)

Keep everything in each of the three laws (`eotg_government_succession_laws.txt:65-151`) **except**:
```
    can_title_have = { always = yes }              # theocratic_elective :737-739; title-level resolution of a realm election
    succession = {
        order_of_succession = election             # :741
        election_type = eotg_<gov>_elective        # :742
    }
    flag = elective_succession_law                 # :746 (replaces advanced_succession_law)
    title_allegiance_opinion = 10                  # :747; _laws.info:140-144
```
- **Remove** `traversal_order`, `rank` and `title_division`. They are invalid with `election` (`_laws.info:220-226`).
- **Keep** `potential`, `can_have`, `can_keep`, `should_start_with`, `can_pass`, the costs and `ai_will_do`. The government-flag whitelists are unchanged, so §7 needs no edit.
- **Why the flag changes:** vanilla readers of `advanced_succession_law` are all `has_title_law_flag` checks (demand-church succession, the major decisions, `00_decisions_effects.txt:1841+`). Under an election realm law they don't apply either way. The theocratic precedent carries `elective_succession_law`.
- **Update the file header:** state that three of the four laws are elective (with this spec's path), and keep the default-law notes.
- **The PMC law is untouched** (§11).

---

## 7. Wiring and interactions

| Area | Effect of this pass | Action |
|---|---|---|
| Safety net (`eotg_gov_ensure_succession_law_effect`; on_game_start, on_game_start_after_lobby, on_government_change, on_title_gain in `eotg_government_on_actions.txt`) | Same keys, same triggers | **none**. The net still adds the government's own law, which is now elective. |
| `can_keep` / `can_have` / `potential` | Unchanged, flag-gated | none |
| Partition and tier-up inheritance (`_laws.info:300-303`; assessment G1) | An heir who inherits a higher tier takes the dead ruler's laws unchecked. The on_title_gain net already corrects a law of the wrong government. | none |
| Cooldown authority (invariant 4) | No content pulses, no cooldowns | n/a |
| Tier gating (v1 lesson 4) | The realm law applies at every tier. At count tier the electorate is usually the holder alone, so the vote reduces to the holder's choice. | none |
| Vote UI | `window_title.gui:2563-2585` shows the vote button on any title where `Title.HasSuccessionOrder('election')`. `window_title_election.gui` is generic. `window_my_realm.gui:4012-4050` lists elective titles with vote buttons. | **no GUI work.** Unverified for a realm-law election outside PAM: V-SU1. |
| Election loc in the window | The window reads `<election_type>_candidates`, `_candidates_tooltip`, `_electors` and `_electors_tooltip` (`G/localization/english/succession_laws_l_english.yml:86-99, 329-332`) | §9 |
| Designate Heir (`designate_heir_interaction`, code-referenced, `G/common/character_interactions/00_heir.txt:1`) | Available at crown authority 3 (`can_designate_heir_trigger`, `00_legal_triggers.txt:150-171`; `crown_authority_3` flag, `00_realm_laws.txt:216-232`). Its election block reads `has_title_law_flag` (`00_heir.txt:31-35`) and may not see a realm law. | **V-SU12 records** whether it is shown and whether it overrides the vote. If it overrides, the architect writes an addendum. Don't override the vanilla interaction speculatively. |
| Court grandeur | `death.txt:323-334` copies grandeur to `primary_heir` in elective realms | expected to work; part of V-SU2 |
| Cartel tribute and grace | §5.3 | none |

---

## 8. Save migration

- **The law keys are unchanged.** A save stores the law key, and the `succession` block is read from the definition on load. Existing rulers move from single heir to election on load, with no script.
- **Electors cast their first votes after load.** Vanilla behaves the same when a title's law changes. V-SU10 checks that the window fills within a month and that no "Anarchy" or law reset appears.
- **A designated heir set before the change** may persist on the character. V-SU10 records whether it affects the vote. If it does, the fix is a one-time `clear_designated_heir` (vanilla effect, 8 call sites) in the existing `on_game_start_after_lobby` net, guarded by the government flag. That fix is not built unless V-SU10 fails.
- **No variable, flag or title law needs back-filling.**

---

## 9. Loc surface (eotg-localizer)

Canadian English. B2 ban list (`governments_v2.md` §11) applies. **No nation names**: no Helix, P&D, Gob-Ogre Trade League or Concrete Cartel. The Trade Oligarchy text is species-neutral. Its top rank is **First Prince**, and the Cartel's top rank is **Overboss** (§8 of the parent spec). Concept links follow vanilla (`[title_heir|E]`, `[elector|E]`, `[dynasty|E]`).

### 9.1 Law text (edit existing keys; one definition per key)

| Key | Now | Wanted |
|---|---|---|
| `eotg_corporation_succession_law` | "Executive Succession" | **keep the name** (the board chooses the executive) |
| `eotg_corporation_succession_law_subname` | "Oldest Child Inherits" | the board elects from the house (draft: "Board Election") |
| `eotg_corporation_succession_law_effects` | single-heir text | a vanilla-shaped effects line (`succession_laws_l_english.yml:78`): the ruler and the board (councillors and powerful vassals, up to seven) nominate a title heir from the ruler's dynasty; votes favour skill in stewardship and diplomacy |
| `eotg_gobcorp_succession_law` | "Charter Succession" | **keep** |
| `eotg_gobcorp_succession_law_subname` | "Oldest Child Inherits" | draft: "Weighted by Wealth" |
| `eotg_gobcorp_succession_law_effects` | single-heir text | the First Prince and the richest Princes (up to nine) nominate from the dynasty; wealth adds voting power |
| `eotg_cartel_succession_law` | "Council Succession" | **keep** |
| `eotg_cartel_succession_law_subname` | "Oldest Child Inherits" | draft: "The Bosses Decide" |
| `eotg_cartel_succession_law_effects` | single-heir text | the Overboss and every boss above the rank of baron nominate from the dynasty; dread adds voting power, and intimidated bosses follow the Overboss's pick |
| `eotg_pmc_succession_law_subname` | "Oldest Child Inherits" | draft: "Chain of Command" |
| `eotg_pmc_succession_law_effects` | as now | add that, with enough crown authority, the commander may name any child as successor (`[designated_heir|E]`). The rest stays true. |
| `eotg_pmc_government_desc` | "…and rank is earned by results in the field." | narrow the clause to contractors (draft: "…and contractors earn their rank by results in the field."). This is the only desc change. |

### 9.2 New keys (3 elections × 4, plus the modifier descs)
- `eotg_corporation_elective_candidates`, `_candidates_tooltip`, `_electors`, `_electors_tooltip`, and the same four for `eotg_gobcorp_elective` and `eotg_cartel_elective` (12 keys). Shape: `succession_laws_l_english.yml:96-99`.
- Vote strength descs, in the form "`<label>: $VALUE|=+0$`" (vanilla `elective_succession_l_english.yml:123`):
  - `eotg_gov_su_vote_chair`;
  - `eotg_corporation_su_vote_board`;
  - `eotg_gobcorp_su_vote_wealth_1` / `_2` / `_3`;
  - `eotg_cartel_su_vote_dread_1` / `_2` / `_3`.
- Candidate score descs:
  - `eotg_corporation_su_score_skill`;
  - `eotg_gobcorp_su_score_wealth`;
  - `eotg_cartel_su_score_follow_fear`;
  - `eotg_cartel_su_score_menace`;
  - `eotg_gov_su_score_minor`.
- **Character-set keys** (`eotg_*_electors_*`, `eotg_*_candidates_*`): vanilla gives loc only to the PAM sets shown in its own window (`cardinals_window_l_english.yml:40-45`). **Write none.** Add them only if error.log or PX reports them missing (V-SU0).
- Reused vanilla keys (no override): `tooltip_feudal_vote_strength_powerful_vassal`, `_king_tier`, `_duke_tier`, and the vanilla pattern descs.
- **No `replace/` overrides.**

---

## 10. Lore constraints (route doubts to eotg-lore-keeper)
- **Corporation:**
  - "a board" is a generic form word and is allowed (`governments_v2.md` §11).
  - Never Helix: Helix at 866 is not board-and-CEO (ERRATA "HELIX CORPORATION").
  - Never "shareholders", "stock" or a market in shares unless the lore-keeper clears it. The 866 economy is not established as having equity markets. **LQ-SU1.**
- **Trade Oligarchy:**
  - "no single head": the election picks a **First Prince**, the first among equals, never a "Director-General" (`governments_v2.md:694`);
  - the text is species-neutral;
  - "fifty princes" as a description of the form only.
- **Cartel:**
  - the B2 list is banned (Don, capo, consigliere, underboss, "the Family", …);
  - the ranks are Route Boss, Ringleader and Overboss;
  - no Concrete Cartel or Slate Syndicate.
- **No authority above the polity** (ERRATA "LAW AT 866"). Elections are internal to the realm: no registry, court or League certifies them.
- **PMC:** no 7th Legion and no LFTx in the text (`governments_v2.md` §5.1).

---

## 11. PMC: recommendation

**Keep single heir, fix the text, and add no election.** Reasons:
1. **The desc clause is about vassals, not the throne.** "Rank is earned by results in the field" reads naturally as the contractors' ladder. Narrowing it (§9.1) removes the contradiction without a mechanic.
2. **Vanilla already gives a merit lever that fits a command.** With crown authority 3 (`flag = can_designate_heirs`, `00_realm_laws.txt:216-232`), the commander can **designate** any child as successor (`designate_heir_interaction`; `can_designate_heir_trigger`, `00_legal_triggers.txt:150-171`). The PMC carries `government_uses_crown_authority` (`governments_v2.md` §5.0), so this works today. "The commander names a successor on results" is that interaction.
3. **No mirroring.** The PMC is the proto-corporate form, standing to the Corporation as tribal stands to feudal (`governments_v2.md` §5.1). If the PMC also elected, the step from PMC to Corporation would lose one of its two differences. The design principle "don't mirror one system's structure onto another" applies.
4. **The cost is nothing.** Loc only (§9.1), and V-SU13 checks it.

**Considered and rejected:** a military-merit election (officers vote, weighted by prowess or martial). It would use the same machinery as §5.3, which is fear and prowess. It would blur the PMC into the Cartel and add a fourth election for little gain. Revisit only if the PMC G2 pass builds `eotg_pmc_standing` and wants succession to read it.

---

## 12. Suggested events (owner's call; not specified for build)
- A Corporation "board meeting" when the projected winner changes. It would move the future `eotg_corp_board_influence`.
- A Cartel "show of force" option that spends dread to win over a boss who opposes the holder's pick. It would move dread through `eotg_cartel_change_dread_effect`.
- A Trade Oligarchy "buy a vote" option that spends gold on one elector. It would move gold and, later, market share.

---

## 13. Batches

| Batch | Agent | Content | Checks |
|---|---|---|---|
| **SU1** | eotg-scripter | `common/succession_election/eotg_government_elections.txt` (§5); the 6 triggers in `eotg_government_triggers.txt`; `common/script_values/eotg_government_succession_values.txt` (5 values); the in-place edit of the 3 laws (§6) and the laws-file header. No other files. | Tiger, `px_lsp_diagnostics.js`, `px_vocab_check.py`. Tiger 1.17 may not know `common/succession_election/`: record what it reports. A hand check against `_succession_election.info` and `02_gaelic_elective.txt` (eotg-vanilla-scout or QA). |
| **SU2** | eotg-localizer | §9.1 edits, §9.2 keys. | PX loc coverage; one definition per key. |
| **SU3** | eotg-qa (in game, British Isles sub-mod) | V-SU1–V-SU14 | If V-SU1 or V-SU2 fails, stop. The architect writes the §3.3 addendum. |
| SU4 (conditional) | eotg-scripter | the V-SU10 designated-heir clear, or a V-SU12 addendum, only if those tests fail | — |

---

## 14. Definition of done and tests (V-SU*)

**Done when:**
- SU1 and SU2 are merged;
- Tiger, PX and the vocab check are clean except the `CLAUDE.md` known-benign list. Any new `succession_election` noise is recorded and added to the benign list only by QA;
- V-SU1–V-SU8, V-SU10, V-SU11 and V-SU13 pass;
- V-SU9, V-SU12 and V-SU14 are recorded.

| # | Test | Pass condition |
|---|---|---|
| V-SU0 | error.log and `database_conflicts.log` after load | no "election", "succession" or law errors from mod files; no missing loc on mod keys |
| V-SU1 | Corporation, Hoël (k_brittany): realm screen and title window | the realm law shows "Executive Succession / <subname>". The title window shows the vote button. The election window lists **only Hoël's dynasty** as candidates, and Hoël plus at most 6 councillors or powerful vassals as electors, with vote strengths matching §5.1. |
| V-SU2 | `kill` Hoël | **all** his titles go to one character, the election winner (no split). The player continues as that character. The government is still Corporation, with `eotg_corporation_succession_law`. The grandeur variable is on the heir (`death.txt:323-334`). |
| V-SU3 | Candidate filter | a landed dynasty member with another government is not a candidate. An unlanded one is. A non-dynasty powerful vassal is not, while any dynastic candidate exists. |
| V-SU4 | Player nomination | nominate a younger dynasty member and raise their votes (the holder's vote plus `add_opinion` on electors). `kill`: that member inherits everything. |
| V-SU5 | Trade Oligarchy, Bertrand (d_provence) | at most 9 electors, ordered by gold. `add_gold = 1000` on a non-elector vassal brings them in at +3 wealth strength. `kill`: there is one winner from the dynasty. |
| V-SU6 | Cartel, Alfonso (k_leon) | Rodrigo is an elector. Pedru is an elector only if he is a direct vassal of Alfonso. With Alfonso's dread at 80 or more, an intimidated Rodrigo votes for Alfonso's pick, and the score tooltip shows `eotg_cartel_su_score_follow_fear`. With dread at 0 and Rodrigo dread-free, Rodrigo's vote follows menace or opinion. Vote strength shows the dread bands. |
| V-SU7 | Cartel, with payers (needs the Cartel G2 tribute built) | `kill` Alfonso: the succession grace and every payer contract are on the **same** character, the election winner |
| V-SU8 | Count tier (Pedru, c_pravia, if Cartel; otherwise make a debug Cartel count) | the election runs with the holder as the only elector. `kill`: a dynasty member inherits. |
| V-SU9 | No dynastic candidate (debug: a ruler whose dynasty has no other living member) | the fallback set lists same-government direct vassals. The realm passes to one of them, not to a generated or foreign character. Record the result. **Also (QA SU1, 2026-10-20):** (a) a dynasty whose only members fail the realm gender or faith law (e.g. only women under `male_only_law`) must fall through to the fallback set, which `eotg_gov_su_law_eligible_trigger` mirrors; (b) with no valid dynasty member and no eligible same-government direct vassal the candidate list is empty (no vanilla-shaped last resort exists: no primary-heir set type, and `primary_heir` under an election is the vote leader). Record what the engine does with zero candidates. |
| V-SU10 | Save migration: a save made before SU1 with all three governments | the election windows fill within one month. No Anarchy, no law reset. Record any pre-existing `designated_heir`, and whether it overrides the vote (SU4 trigger). |
| V-SU11 | Safety net | `eotg_decision_gov_debug_become_corporation` on a feudal ruler gives the elective law and the vote button. "Become feudal" drops it (`can_keep`), and the feudal default applies. |
| V-SU12 | Designate Heir under an election (crown authority 3) | record whether the interaction is shown, and whether a designated child wins over the vote. **Record only.** |
| V-SU13 | PMC | the law shows the new subname and effects. At crown authority 3, Designate Heir is available, and the designated child inherits on `kill`. |
| V-SU14 | 50-year observer run (with V-G12) | no ruler without a succession law; no non-dynasty successor while the dynasty had a valid member; no realm split at an elective succession; all three governments still hold at least their starting realms' top titles, or the loss is explained by war |

---

## 15. Deferred
- **Board influence and market share as vote weights.** Their slots are reserved (§2), and they are built in each government's G2 pass. Building them here would create two writers for one resource.
- **Electors limited to the dynasty** (OQ1). Not done: P1 needs only dynastic **candidates**.
- **A PMC election** (§11, rejected).
- **Events around elections** (§12; owner rule).
- **Title-law or appointment fallback** (§3.3). Written only if V-SU1 or V-SU2 fails.
- **Unsworn succession (G3)** is out of scope and tracked separately.

---

## 16. Owner questions

**Ruled 2026-10-20 (owner):** Q1 **candidates only** are limited to the ruling family, and electors are unrestricted. Q2 the limit is by **dynasty**. Q3 only applies if V-SU1 fails, so it is still open.
- **OQ1. Electors from the dynasty only?** The ruling text says "electors and candidates are limited to the dynasty or house". This spec limits **candidates** to the dynasty, which is what keeps the player in play. **Electors** are the board, the richest princes or the bosses, whoever their family. If electors were also limited to the dynasty, most realms would reduce to the holder voting alone, and the board, charter and council fiction would disappear. **Recommendation: candidates only.** If the owner wants dynasty-only electors, it is one `dynasty = scope:holder.dynasty` line per elector set.
- **OQ2. House or dynasty?** This spec uses the **dynasty**: Tanistry's `holder_dynasty`, which is also the CK3 game-over unit. A house-only rule would be tighter, so cadet branches could not win, but vanilla has no `holder_house` set type, so it would be a `house = scope:holder.house` filter. **Recommendation: dynasty.**
- **OQ3 (conditional).** If V-SU1 shows that a realm-law election doesn't work outside PAM, is a **vote-less appointment** (fallback C, realm-wide and no split) acceptable for these governments? Or is a title-law election that splits the domain on a non-eldest winner (fallback B) preferred?

---

## Handoff

```
HANDOFF
- from: eotg-architect
- to: eotg-scripter
- spec: docs/specs/governments_v2_g2_succession.md
- ask: Build batch SU1 (§13): common/succession_election/eotg_government_elections.txt (3 elections, §5), 6 triggers in common/scripted_triggers/eotg_government_triggers.txt, common/script_values/eotg_government_succession_values.txt (5 values), and the in-place edit of eotg_corporation/gobcorp/cartel_succession_law (§6: election_type, can_title_have = always yes, flag = elective_succession_law, title_allegiance_opinion = 10; drop traversal/rank/division). PMC law untouched. No events, no on_action or safety-net changes.
- then: eotg-localizer SU2 (§9), eotg-qa SU3 (V-SU0–V-SU14, British Isles sub-mod).
- blockers: none for SU1/SU2. SU3 should follow CB-49 V-G3/V-G4. OQ1–OQ2 have recommended defaults built in; OQ3 only if V-SU1 fails.
- orchestrator: add common/succession_election/ to the CLAUDE.md placement table; update CB-53 to "ruled, spec written".
```
