"""Generate the in-game test harness sub-mod (docs/qa/TEST_HARNESS.md).

    python docs/tools/gen_test_harness.py [output_root]

Test content never ships (owner decision, 2026-11-03), so the harness is its own sub-mod. The output
root defaults to docs/test_submods/test_harness/ and receives descriptor.mod, README.md,
common/decisions/eotg_test_harness_decisions.txt, events/eotg_test_harness.txt and
localization/english/eotg_test_harness_l_english.yml (one BOM each on the script and loc files).
Add a test with T(...) below. Output is deterministic: a second run is byte-identical.
"""
import os, sys, textwrap
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if len(sys.argv) > 1 and sys.argv[1].startswith('-'):
    sys.exit('usage: gen_test_harness.py [OUTPUT_ROOT]  (default: docs/test_submods/test_harness)')
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'docs', 'test_submods', 'test_harness')
BOM = '﻿'

def ind(s, n): return textwrap.indent(textwrap.dedent(s).strip('\n'), ' ' * n)
def log(msg): return f'debug_log = "EOTG_TEST {msg}"'
def check(tid, trig, ok, bad):
    return f"""if = {{
    limit = {{
{ind(trig, 8)}
    }}
    {log(f'{tid} PASS: {ok}')}
}}
else = {{
    {log(f'{tid} FAIL: {bad}')}
}}"""

TESTS = []   # (id, key_suffix, name, desc, tooltip, plan_refs, decision_effect, [(event_id, body)])
EVENTS = []

def T(tid, suffix, name, desc, refs, effect, events=()):
    TESTS.append(dict(tid=tid, suffix=suffix, name=name, desc=desc, refs=refs, effect=effect))
    EVENTS.extend(events)

def ev(eid, body): return (eid, body)
AUGMENTED = "OR = { has_trait = eotg_cybernetics has_trait = eotg_neurofractured has_trait = eotg_total_integration }"

# ---------------------------------------------------------------- Cybernetics
T('CY1', 'cy1_tier_ladder', 'CY1: Tier Ladder',
  'Initiates you, then raises you to Enhanced and Overclocked a day apart, and checks the tier and the prowess total at each step (+2, +4, +8). Start from an unaugmented character.',
  'IGSP E-10, C2, C3, C4; CTP §3',
  f"""
{log('CY1 START: tier ladder')}
if = {{
    limit = {{ {AUGMENTED} }}
    {log('CY1 SKIP: start from an unaugmented character')}
}}
else = {{
    # UNVERIFIED-VANILLA: `value = prowess` (a skill trigger read as a value,
    # as the Cartel reads `dread`, eotg_cartel_values.txt). If it errors, the
    # prowess checks fail loudly; the tier checks still stand.
    set_variable = {{ name = eotg_test_prowess_base  value = prowess }}
    eotg_aug_initiate_effect = yes
    trigger_event = {{ id = eotg_test.101  days = 1 }}
}}""",
  [ev('eotg_test.101', f"""
{check('CY1.1', 'eotg_is_aug_tier1 = yes', 'Augmented (tier 1)', 'not tier 1 after eotg_aug_initiate_effect')}
{check('CY1.2', 'prowess >= { value = var:eotg_test_prowess_base add = 2 }\nprowess <= { value = var:eotg_test_prowess_base add = 2 }', 'prowess +2 at Augmented', 'prowess is not base +2 at Augmented')}
eotg_aug_set_integration_effect = {{ XP = 50 }}
trigger_event = {{ id = eotg_test.102  days = 1 }}"""),
   ev('eotg_test.102', f"""
{check('CY1.3', 'eotg_is_aug_tier2 = yes', 'Enhanced (tier 2)', 'not tier 2 after XP 50')}
{check('CY1.4', 'prowess >= { value = var:eotg_test_prowess_base add = 4 }\nprowess <= { value = var:eotg_test_prowess_base add = 4 }', 'prowess +4 at Enhanced (track stacks)', 'prowess is not base +4 at Enhanced (E-10: does the track stack?)')}
eotg_aug_set_integration_effect = {{ XP = 100 }}
trigger_event = {{ id = eotg_test.103  days = 1 }}"""),
   ev('eotg_test.103', f"""
{check('CY1.5', 'eotg_is_aug_tier3 = yes', 'Overclocked (tier 3)', 'not tier 3 after XP 100')}
{check('CY1.6', 'prowess >= { value = var:eotg_test_prowess_base add = 8 }\nprowess <= { value = var:eotg_test_prowess_base add = 8 }', 'prowess +8 at Overclocked', 'prowess is not base +8 at Overclocked')}
remove_variable = eotg_test_prowess_base
{log('CY1 LOOK: the Overclocked trait tooltip and portrait; save as S2_oc if you follow the session plan')}
{log('CY1 DONE')}""")])

T('CY2', 'cy2_neurofractured', 'CY2: Neurofractured End State',
  'As a ruler with the cybernetics trait: adds the Neurofractured trait, as the session plan does, and checks that it replaced the cybernetics trait. Run CY1 first.',
  'IGSP C5',
  f"""
{log('CY2 START: Neurofractured end state')}
if = {{
    limit = {{ NOT = {{ has_trait = eotg_cybernetics }} }}
    {log('CY2 SKIP: needs the cybernetics trait, so the replacement can be seen; run CY1 first')}
}}
else = {{
    add_trait = eotg_neurofractured
    trigger_event = {{ id = eotg_test.111  days = 1 }}
}}""",
  [ev('eotg_test.111', f"""
{check('CY2.1', 'has_trait = eotg_neurofractured', 'Neurofractured', 'eotg_neurofractured was not added')}
{check('CY2.2', 'NOT = { has_trait = eotg_cybernetics }', 'the cybernetics trait is gone (opposites)', 'still has eotg_cybernetics beside eotg_neurofractured')}
{log('CY2 LOOK: the trait tooltip; the Neurofractured yearly pool over the next years (C5)')}
{log('CY2 DONE')}""")])

T('CY3', 'cy3_seamless', 'CY3: Seamless End State',
  'Adds the Seamless trait with 3 residue, as the session plan does, and checks the trait. The Frontier flavour exclusion is a look check.',
  'IGSP C6; frontier_v5 §3.7',
  f"""
{log('CY3 START: Seamless end state')}
add_trait = eotg_total_integration
set_variable = {{ name = eotg_aug_residue  value = 3 }}
trigger_event = {{ id = eotg_test.121  days = 1 }}""",
  [ev('eotg_test.121', f"""
{check('CY3.1', 'has_trait = eotg_total_integration', 'Seamless', 'eotg_total_integration was not added')}
{log('CY3.2 LOOK: no first-person Frontier flavour event reaches you from now on (eotg_frontier_can_hear_flavor reads this trait, so script cannot check it independently)')}
{log('CY3 LOOK: the log-register event text in the Seamless pool (C6)')}
{log('CY3 DONE')}""")])

T('CY4', 'cy4_cascade_threshold', 'CY4: Neural Cascade at the Threshold',
  'As an Overclocked ruler: sets the fracture risk to the threshold (80) and runs the yearly Overclocked pulse once, then checks that the Neural Cascade made you Neurofractured and reset the risk. Run CY1 first.',
  'IGSP C4; cybernetics_v2 phase 3 §1',
  f"""
{log('CY4 START: Neural Cascade at the threshold')}
if = {{
    limit = {{ eotg_is_aug_tier3 = no }}
    {log('CY4 SKIP: needs an Overclocked character, run CY1 first')}
}}
else = {{
    set_variable = {{ name = eotg_fracture_risk  value = 80 }}
    # The real yearly path (eotg_augmentation_on_actions.txt): accrual, then
    # the threshold check, then eotg_trigger_neurofracture. trigger_event with
    # on_action: confirmed in v2 (eotg_frontier_on_actions.txt:90, V12).
    trigger_event = {{ on_action = eotg_on_yearly_aug_overclocked_check }}
    trigger_event = {{ id = eotg_test.131  days = 1 }}
}}""",
  [ev('eotg_test.131', f"""
{check('CY4.1', 'has_trait = eotg_neurofractured\nNOT = { has_trait = eotg_cybernetics }', 'the pulse cascaded: Neurofractured, cybernetics trait gone', 'no cascade from the yearly pulse at risk 80 (threshold check or eotg_trigger_neurofracture)')}
{check('CY4.2', 'var:eotg_fracture_risk ?= 0', 'the cascade reset the fracture risk to 0', 'the fracture risk was not reset after the cascade')}
{log('CY4 LOOK: the cascade event eotg_fracture.0001 arrives today or tomorrow')}
{log('CY4 DONE')}""")])

T('CY5', 'cy5_track_ai_values', 'CY5: Track AI Values on a Courtier',
  'Initiates an unaugmented adult AI courtier, then raises them a tier every 3 days. Hover them in debug mode at each step and note the AI values.',
  'IGSP E-13; SI T1',
  f"""
{log('CY5 START: per-level ai_ values (look test)')}
random_courtier = {{
    limit = {{
        is_ai = yes
        is_adult = yes
        NOT = {{ {AUGMENTED} }}
    }}
    save_scope_as = eotg_test_subject
}}
if = {{
    limit = {{ exists = scope:eotg_test_subject }}
    {log('CY5 LOOK: hover the chosen courtier NOW and note energy, honour, zeal before the change (debug block)')}
    trigger_event = {{ id = eotg_test.141  days = 1 }}
}}
else = {{
    {log('CY5 SKIP: no unaugmented adult AI courtier at your court')}
}}""",
  [ev('eotg_test.141', f"""
scope:eotg_test_subject = {{ eotg_aug_initiate_effect = yes }}
{log('CY5 LOOK: Augmented now; expect energy +2, zeal -1, honour -1 against the first reading')}
trigger_event = {{ id = eotg_test.142  days = 3 }}"""),
   ev('eotg_test.142', f"""
scope:eotg_test_subject = {{ eotg_aug_set_integration_effect = {{ XP = 50 }} }}
{log('CY5 LOOK: Enhanced now; expect energy +3, zeal -2, honour -1')}
trigger_event = {{ id = eotg_test.143  days = 3 }}"""),
   ev('eotg_test.143', f"""
scope:eotg_test_subject = {{ eotg_aug_set_integration_effect = {{ XP = 100 }} }}
{log('CY5 LOOK: Overclocked now; expect energy +4, zeal -3, honour -2. If every stage shows the Augmented line, the track ai_ lines are ignored (SI T1)')}
{log('CY5 DONE')}""")])

WOUND_STEP = '''    if = {
        limit = { NOT = { has_trait = wounded_3 } }
        increase_wounds_effect = { REASON = attacked }
    }
'''
T('CY6', 'cy6_wound_repair', 'CY6: Wound Rank 3 and the Repair Offer',
  'As an augmented ruler: clears the real repair cooldown (eotg_flag_aug_repair_cooldown), raises your wound to rank 3 without ever passing it, then checks that the repair hook saw the wound.',
  'IGSP E-11; PROC §4.9',
  f"""
{log('CY6 START: wound rank 3 and on_trait_gained')}
if = {{
    limit = {{ eotg_is_augmented_any = no }}
    {log('CY6 SKIP: needs an augmented character, run CY1 first')}
}}
else_if = {{
    limit = {{ has_trait = wounded_3 }}
    {log('CY6 SKIP: already at wound rank 3; heal first')}
}}
else = {{
    if = {{
        limit = {{ has_character_flag = eotg_flag_aug_repair_cooldown }}
        remove_character_flag = eotg_flag_aug_repair_cooldown
    }}
    # increase_wounds_effect calls death on a character already at rank 3
    # (vanilla 20_health_effects.txt:1342-1351), so each call is guarded:
    # a fragile_bones character can jump two ranks in one call. The repair
    # hook fires on wounded_3 only, so the test cannot stop at wounded_2.
{WOUND_STEP}{WOUND_STEP}{WOUND_STEP}    trigger_event = {{ id = eotg_test.151  days = 2 }}
}}""",
  [ev('eotg_test.151', f"""
{check('CY6.1', 'has_trait = wounded_3', 'wound rank 3 reached', 'three guarded increase_wounds_effect calls did not reach wounded_3')}
{check('CY6.2', 'var:eotg_aug_repair_injury ?= flag:wounded', 'on_trait_gained fired for wounded_3: the repair is queued', 'no repair queued: change_trait_rank does not fire on_trait_gained for wounded_3 (PROC §4.9 engine question)')}
{log('CY6 LOOK: eotg_aug_proc.003 should arrive within 30 days')}
{log('CY6 DONE')}""")])

# ---------------------------------------------------------------- Frontier
for sfx, typ, nm, refs in (('a', 'military', 'Military', 'IGSP E-1 step 1, E-12 setup; F1 §1'),
                            ('b', 'settlement', 'Settlement', 'IGSP E-4 setup, G-2 setup; F1 §1'),
                            ('c', 'religious', 'Religious', 'IGSP FX-2 setup, G-2 setup; F1 §1')):
    tid = f'FR1{sfx}'
    T(tid, f'fr1{sfx}_start_{typ}', f'FR1{sfx}: Start a {nm} Frontier',
      f'Marks your capital Shoal Unsettled and starts a {nm} Frontier there with you as the founder, then checks the state.',
      refs,
      f"""
{log(f'{tid} START: start a {typ} Frontier on the capital')}
capital_county = {{ save_scope_as = eotg_test_county }}
if = {{
    limit = {{ eotg_frontier_holds_frontier = yes }}
    {log(f'{tid} SKIP: a Frontier is already running in your realm (one at a time, as Establish a Frontier allows); complete it with FR2 first')}
}}
else_if = {{
    limit = {{ scope:eotg_test_county = {{ eotg_frontier_is_unknown = yes }} }}
    {log(f'{tid} SKIP: the capital is Unknown, and an Unknown Shoal cannot be established; take FR5 to the end (it clears exploration) or pick a known capital')}
}}
else = {{
    scope:eotg_test_county = {{
        eotg_frontier_mark_unsettled_effect = yes
        eotg_frontier_start_effect = {{ TYPE = {typ}  FOUNDER = root }}
    }}
    trigger_event = {{ id = eotg_test.20{ "abc".index(sfx) + 1 }  days = 1 }}
}}""",
      [ev(f'eotg_test.20{"abc".index(sfx) + 1}', f"""
{check(f'{tid}.1', f'scope:eotg_test_county = {{\n    eotg_frontier_is_frontier = yes\n    var:eotg_frontier_type ?= flag:{typ}\n}}', f'the capital is a {typ} Frontier', 'the capital is not a Frontier of that type (was it Abandoned and not resettlable?)')}
{check(f'{tid}.2', 'scope:eotg_test_county = { eotg_frontier_has_valid_founder = yes }', 'you are its valid founder', 'no valid founder recorded')}
{log(f'{tid} LOOK: the Shoal shows Frontier: Outpost; (Debug) Frontier Readout gives progress and strain')}
{log(f'{tid} DONE')}""")])

T('FR2', 'fr2_force_completion', 'FR2: Force Frontier Completion',
  'On the Frontier at your capital: sets progress to 100, raises development by 5 and control to 100, runs one Frontier year, then checks a week later that it completed. Answer the completion event as soon as it appears.',
  'IGSP E-4, E-12; SI V8; with FR1c: FX-2; as a PMC: G-2',
  f"""
{log('FR2 START: force completion on the capital Frontier')}
capital_county = {{ save_scope_as = eotg_test_county }}
if = {{
    limit = {{ scope:eotg_test_county = {{ eotg_frontier_is_frontier = no }} }}
    {log('FR2 SKIP: the capital is not a Frontier; run FR1a, FR1b or FR1c first')}
}}
else = {{
    scope:eotg_test_county = {{
        set_variable = {{ name = eotg_test_type  value = var:eotg_frontier_type }}
        set_variable = {{ name = eotg_frontier_progress  value = 100 }}
        change_development_level = 5
        change_county_control = 100
        eotg_frontier_tick_effect = yes
    }}
    # 7 days, not 1: completion goes through an event the player answers;
    # a 1-day check raced it (QA 2026-11-03). Answer it at once.
    trigger_event = {{ id = eotg_test.211  days = 7 }}
}}""",
  [ev('eotg_test.211', f"""
{check('FR2.1', 'scope:eotg_test_county = {\n    NOT = { has_variable = eotg_frontier_state }\n}', 'the Frontier completed and cleared (normal play takes over)', 'still a Frontier a week later: the completion event was left unanswered, or the development or control floor was not met; see the Readout')}
if = {{
    limit = {{ scope:eotg_test_county = {{ var:eotg_test_type ?= flag:military }} }}
    {log('FR2 LOOK: E-12 / SI V8: hover the new Bastion barony, note who holds it and whether a stray character was created')}
}}
else_if = {{
    limit = {{ scope:eotg_test_county = {{ var:eotg_test_type ?= flag:religious }} }}
    {log('FR2 LOOK: FX-2: note the new Sanctum holder gender (expected male under a male-only clergy); G-2: note their government and the vassal contract')}
}}
else = {{
    {log('FR2 LOOK: E-4: which holding appeared and who holds it (never the founder unless they rule); G-2: the Local Ruler government and contract')}
}}
scope:eotg_test_county = {{
    if = {{
        limit = {{ has_variable = eotg_test_type }}
        remove_variable = eotg_test_type
    }}
}}
{log('FR2 DONE')}""")])

T('FR3', 'fr3_clamps', 'FR3: Progress and Strain Clamps',
  'On the Frontier at your capital: pushes progress past 100, strain past 8 and progress below 0 through the real change effects, a day apart, and checks the clamps.',
  'IGSP E-6; F2 §0.2',
  f"""
{log('FR3 START: progress and strain clamps')}
capital_county = {{ save_scope_as = eotg_test_county }}
if = {{
    limit = {{ scope:eotg_test_county = {{ eotg_frontier_is_frontier = no }} }}
    {log('FR3 SKIP: the capital is not a Frontier; run FR1a first')}
}}
else = {{
    scope:eotg_test_county = {{
        set_variable = {{ name = eotg_frontier_progress  value = 98 }}
        eotg_frontier_add_progress_effect = {{ AMOUNT = 4 }}
    }}
    trigger_event = {{ id = eotg_test.221  days = 1 }}
}}""",
  [ev('eotg_test.221', f"""
{check('FR3.1', 'scope:eotg_test_county = { var:eotg_frontier_progress <= 100 }', 'progress 98 + 4 is clamped at 100', 'progress went above 100')}
scope:eotg_test_county = {{
    set_variable = {{ name = eotg_frontier_strain  value = 8 }}
    eotg_frontier_add_strain_effect = {{ CAUSE = hardship }}
}}
trigger_event = {{ id = eotg_test.222  days = 1 }}"""),
   ev('eotg_test.222', f"""
{check('FR3.2', 'scope:eotg_test_county = { var:eotg_frontier_strain <= 8 }', 'strain 8 + 1 is clamped at 8', 'strain went above 8')}
scope:eotg_test_county = {{
    set_variable = {{ name = eotg_frontier_strain  value = 0 }}
    set_variable = {{ name = eotg_frontier_progress  value = 1 }}
    eotg_frontier_add_progress_effect = {{ AMOUNT = -3 }}
}}
trigger_event = {{ id = eotg_test.223  days = 1 }}"""),
   ev('eotg_test.223', f"""
{check('FR3.3', 'scope:eotg_test_county = { var:eotg_frontier_progress >= 0 }', 'progress 1 - 3 is clamped at 0', 'progress went below 0')}
{log('FR3 DONE (strain reset to 0; progress left at 0)')}""")])

T('FR4A', 'fr4a_persistence_mark', 'FR4a: Mark Persistence Probes',
  'On the Frontier at your capital: adds the Remote trait and records the progress. Then save, quit to the menu, reload, and run FR4b.',
  'IGSP E-1 steps 2-3, E-2',
  f"""
{log('FR4A START: persistence probes')}
capital_county = {{ save_scope_as = eotg_test_county }}
if = {{
    limit = {{ scope:eotg_test_county = {{ eotg_frontier_is_frontier = no }} }}
    {log('FR4A SKIP: the capital is not a Frontier; run FR1a first')}
}}
else = {{
    scope:eotg_test_county = {{
        if = {{
            limit = {{ NOT = {{ has_county_modifier = eotg_frontier_trait_remote }} }}
            add_county_modifier = eotg_frontier_trait_remote
        }}
        set_variable = {{ name = eotg_test_persist_progress  value = var:eotg_frontier_progress }}
    }}
    {log('FR4A LOOK: now save, quit to the menu, reload, then take FR4b')}
}}""")

T('FR4B', 'fr4b_persistence_check', 'FR4b: Check Persistence',
  'After a save and reload: checks that the capital is still a Frontier with the same progress and the Remote trait. Run FR4a first.',
  'IGSP E-1 step 3, E-2 step 3',
  f"""
{log('FR4B START: persistence check after reload')}
capital_county = {{ save_scope_as = eotg_test_county }}
if = {{
    limit = {{ scope:eotg_test_county = {{ NOT = {{ has_variable = eotg_test_persist_progress }} }} }}
    {log('FR4B SKIP: no probe recorded; run FR4a, save and reload first')}
}}
else = {{
    {check('FR4B.1', 'scope:eotg_test_county = { eotg_frontier_is_frontier = yes }', 'still a Frontier after reload', 'the Frontier state was lost')}
    {check('FR4B.2', 'scope:eotg_test_county = {\n    var:eotg_frontier_progress >= var:eotg_test_persist_progress\n    var:eotg_frontier_progress <= var:eotg_test_persist_progress\n}', 'progress unchanged', 'progress differs from the recorded value')}
    {check('FR4B.3', 'scope:eotg_test_county = { has_county_modifier = eotg_frontier_trait_remote }', 'the county modifier survived', 'the Remote county modifier was lost')}
    scope:eotg_test_county = {{ remove_variable = eotg_test_persist_progress }}
    {log('FR4B LOOK: E-1 steps 4-6 (holder change) remain manual')}
    {log('FR4B DONE')}
}}""")

T('FR5', 'fr5_exploration', 'FR5: Mark the Capital Unexplored',
  'Marks your capital Shoal Unknown with the real effect, checks the exploration state, then clears it again so the capital is not left Unknown. Skipped while the capital is a Frontier.',
  'IGSP E-3; F3 §0.1',
  f"""
{log('FR5 START: exploration state')}
capital_county = {{ save_scope_as = eotg_test_county }}
if = {{
    limit = {{ scope:eotg_test_county = {{ eotg_frontier_is_frontier = yes }} }}
    {log('FR5 SKIP: a Frontier is running on the capital, and eotg_frontier_mark_unknown_effect leaves a Frontier as it is; complete it with FR2 first')}
}}
else_if = {{
    limit = {{
        scope:eotg_test_county = {{
            OR = {{
                eotg_frontier_is_abandoned = yes
                has_variable = eotg_frontier_explored
            }}
        }}
    }}
    {log('FR5 SKIP: the capital is Abandoned or already has an exploration state, which the effect leaves as it is')}
}}
else = {{
    scope:eotg_test_county = {{ eotg_frontier_mark_unknown_effect = yes }}
    trigger_event = {{ id = eotg_test.251  days = 1 }}
}}""",
  [ev('eotg_test.251', f"""
{check('FR5.1', 'scope:eotg_test_county = { eotg_frontier_is_unknown = yes }', 'the capital is Unknown', 'the exploration variable was not set')}
{log('FR5 LOOK: the Unexplored Shoal tooltip itself is session-plan check 0-1 (c_tortoli on playset A)')}
scope:eotg_test_county = {{ eotg_frontier_clear_exploration_effect = yes }}
{check('FR5.2', 'scope:eotg_test_county = { eotg_frontier_is_unknown = no }', 'exploration cleared again: the capital is Known (it stays Unsettled)', 'eotg_frontier_clear_exploration_effect left the capital Unknown')}
{log('FR5 DONE')}""")])

# ---------------------------------------------------------------- Governments
T('GV1', 'gv1_cartel_schedule', 'GV1: Cartel Payment Schedule',
  'As an independent Cartel ruler: tops up your dread, puts one independent neighbour on the payment schedule through the real effect, and checks the contract, the payer count and that the baseline rose by 4.',
  'Cartel spec V-C4, V-C19',
  f"""
{log('GV1 START: Cartel tribute lifecycle, start')}
if = {{
    limit = {{ eotg_cartel_role_top = no }}
    {log('GV1 SKIP: needs an independent Cartel ruler; take (Debug) Become a Cartel first')}
}}
else = {{
    # UNVERIFIED-VANILLA: the random_ form of any_neighboring_top_liege_realm_owner
    # (the any_ form is used in v2 script). If the iterator is unknown, error.log
    # names it and the test logs SKIP (no target).
    random_neighboring_top_liege_realm_owner = {{
        limit = {{
            is_independent_ruler = yes
            is_tributary = no
            highest_held_title_tier >= tier_county
            NOT = {{ government_has_flag = cannot_be_vassal_or_liege }}
        }}
        save_scope_as = eotg_test_target
    }}
    if = {{
        limit = {{ eotg_cartel_schedule_scale_value >= 40 }}
        {log('GV1 SKIP: the dread baseline is already at its cap of 40 (10 payers), so a new payer cannot raise it; run GV2 first')}
    }}
    else_if = {{
        limit = {{ exists = scope:eotg_test_target }}
        set_variable = {{ name = eotg_test_scale_before  value = eotg_cartel_schedule_scale_value }}
        eotg_cartel_change_dread_effect = {{ AMOUNT = 40 }}
        # The scope names eotg_cartel_start_schedule_effect reads (it is called
        # from the interaction, where the engine sets them)
        save_scope_as = actor
        scope:eotg_test_target = {{ save_scope_as = recipient }}
        eotg_cartel_start_schedule_effect = yes
        trigger_event = {{ id = eotg_test.301  days = 1 }}
    }}
    else = {{
        {log('GV1 SKIP: no independent neighbouring ruler to put on the schedule')}
    }}
}}""",
  [ev('eotg_test.301', f"""
{check('GV1.1', 'scope:eotg_test_target = { has_subject_contract_group = eotg_cartel_tributary }', 'the neighbour is a payer in eotg_cartel_tributary', 'the neighbour is not in the Cartel contract group')}
{check('GV1.2', 'eotg_cartel_payer_count_value >= 1', 'the payer count sees the new payer', 'eotg_cartel_payer_count_value is 0')}
{check('GV1.3', 'eotg_cartel_schedule_scale_value >= { value = var:eotg_test_scale_before add = 4 }\neotg_cartel_schedule_scale_value <= { value = var:eotg_test_scale_before add = 4 }', 'the dread baseline mirror rose by exactly 4 for the new payer', 'eotg_cartel_schedule_scale did not rise by exactly 4')}
remove_variable = eotg_test_scale_before
{log('GV1 LOOK: the character window shows +4 Dread baseline per payer; the Payment Schedule story counter matches your dread')}
{log('GV1 DONE')}""")])

T('GV2', 'gv2_cartel_walk_off', 'GV2: Cartel Walk-Off',
  'As a Cartel ruler with payers: runs the dread walk-off once, as the yearly tick would, and checks that exactly one payer left.',
  'Cartel spec V-C12',
  f"""
{log('GV2 START: Cartel tribute lifecycle, walk-off')}
if = {{
    limit = {{
        OR = {{
            eotg_cartel_role_top = no
            eotg_cartel_payer_count_value < 1
        }}
    }}
    {log('GV2 SKIP: needs a Cartel ruler with at least one payer; run GV1 first')}
}}
else = {{
    set_variable = {{ name = eotg_test_payers_before  value = eotg_cartel_payer_count_value }}
    eotg_cartel_walk_off_effect = yes
    trigger_event = {{ id = eotg_test.311  days = 1 }}
}}""",
  [ev('eotg_test.311', f"""
{check('GV2.1', 'eotg_cartel_payer_count_value < var:eotg_test_payers_before', 'one payer walked off', 'the payer count did not fall')}
{check('GV2.2', 'eotg_cartel_payer_count_value >= { value = var:eotg_test_payers_before add = -1 }', 'no more than one payer left', 'more than one payer left in a single walk-off')}
remove_variable = eotg_test_payers_before
{log('GV2 LOOK: the A Payer Walks toast named the payer; the baseline modifier dropped by 4')}
{log('GV2 DONE')}""")])

T('GV3', 'gv3_elective_candidate', 'GV3: Elective Candidate Rule',
  'As a Corporation, Trade Oligarchy or Cartel ruler: checks that the projected successor is of your dynasty (candidates are limited to the dynasty; electors are not).',
  'Succession spec V-SU3, V-SU9',
  f"""
{log('GV3 START: elective succession candidate rule')}
if = {{
    limit = {{
        NOR = {{
            government_has_flag = eotg_government_is_corporation
            government_has_flag = eotg_government_is_gobcorp
            government_has_flag = eotg_government_is_cartel
        }}
    }}
    {log('GV3 SKIP: needs a Corporation, Trade Oligarchy or Cartel ruler')}
}}
else_if = {{
    limit = {{ NOT = {{ exists = primary_heir }} }}
    {log('GV3 FAIL: no projected successor at all (V-SU9 fallback should name a same-government vassal)')}
}}
else = {{
    {check('GV3.1', 'primary_heir = { dynasty = root.dynasty }', 'the projected successor is of your dynasty', 'the projected successor is outside your dynasty: correct ONLY if no dynasty member is a valid candidate (V-SU9)')}
    {log('GV3 LOOK: open the title vote window: candidates listed are your dynasty; electors may be anyone the law names')}
    {log('GV3 DONE')}
}}""")

T('GV4', 'gv4_cartel_core', 'GV4: Cartel Resource Core',
  'As a landed Cartel ruler: checks the Payment Schedule story and the baseline modifier that init gives every landed Cartel ruler.',
  'Cartel spec V-C2',
  f"""
{log('GV4 START: Cartel story and modifier')}
if = {{
    limit = {{ eotg_cartel_is_landed_cartel = no }}
    {log('GV4 SKIP: needs a landed Cartel ruler')}
}}
else = {{
    {check('GV4.1', 'any_owned_story = { story_type = eotg_story_cartel_schedule }', 'the Payment Schedule story exists', 'no eotg_story_cartel_schedule (init did not run: game start, government change or title gain)')}
    {check('GV4.2', 'has_character_modifier = eotg_cartel_schedule_modifier', 'the schedule modifier is present', 'no eotg_cartel_schedule_modifier')}
    {log('GV4 DONE')}
}}""")

# ---------------------------------------------------------------- Alerts
T('AL1', 'al1_frontier_breaking', 'AL1: Alert: Frontier at Breaking Strain',
  'On the Frontier at your capital: sets strain to 6 and checks the alert condition. Then look at the top bar.',
  'integration_v1 §4.2 (INT1 alert 1)',
  f"""
{log('AL1 START: breaking-strain alert')}
capital_county = {{ save_scope_as = eotg_test_county }}
if = {{
    limit = {{ scope:eotg_test_county = {{ eotg_frontier_is_frontier = no }} }}
    {log('AL1 SKIP: the capital is not a Frontier; run FR1a first')}
}}
else = {{
    scope:eotg_test_county = {{ set_variable = {{ name = eotg_frontier_strain  value = 6 }} }}
    trigger_event = {{ id = eotg_test.401  days = 1 }}
}}""",
  [ev('eotg_test.401', f"""
{check('AL1.1', 'scope:eotg_test_county = { eotg_frontier_strain_is_breaking = yes }', 'the alert condition holds (strain 6)', 'eotg_frontier_strain_is_breaking is false at strain 6')}
{log('AL1 LOOK: the top bar shows the breaking-strain alert; clicking it opens the Shoal')}
{log('AL1 DONE')}""")])

T('AL2', 'al2_frontier_founderless', 'AL2: Alert: Frontier Without a Founder',
  'On the Frontier at your capital: removes the founder record and checks the alert condition. Then look at the top bar.',
  'integration_v1 §4.2 (INT1 alert 2)',
  f"""
{log('AL2 START: founderless alert')}
capital_county = {{ save_scope_as = eotg_test_county }}
if = {{
    limit = {{ scope:eotg_test_county = {{ eotg_frontier_is_frontier = no }} }}
    {log('AL2 SKIP: the capital is not a Frontier; run FR1a first')}
}}
else = {{
    scope:eotg_test_county = {{
        if = {{
            limit = {{ has_variable = eotg_frontier_founder }}
            remove_variable = eotg_frontier_founder
        }}
    }}
    trigger_event = {{ id = eotg_test.411  days = 1 }}
}}""",
  [ev('eotg_test.411', f"""
{check('AL2.1', 'scope:eotg_test_county = { eotg_frontier_has_valid_founder = no }', 'the alert condition holds (no founder)', 'the county still reports a valid founder')}
{log('AL2 LOOK: the top bar shows the founderless alert; clicking it opens Appoint a Founder')}
{log('AL2 DONE')}""")])

T('AL3', 'al3_establish_ready', 'AL3: Alert: A Frontier Can Be Established',
  'Marks your capital Shoal Unsettled (if it has no Frontier state) and checks the alert condition. Then look at the top bar. Skipped while a Frontier runs or the capital is Unknown.',
  'integration_v1 §4.2 (INT1 alert 3)',
  f"""
{log('AL3 START: establish-ready alert')}
capital_county = {{ save_scope_as = eotg_test_county }}
if = {{
    limit = {{ eotg_frontier_holds_frontier = yes }}
    {log('AL3 SKIP: a Frontier is running in your realm, and the alert is off by design while one runs; complete it with FR2 first')}
}}
else_if = {{
    limit = {{ scope:eotg_test_county = {{ eotg_frontier_is_unknown = yes }} }}
    {log('AL3 SKIP: the capital is Unknown, and an Unknown Shoal cannot be established; take FR5 to the end (it clears exploration) first')}
}}
else = {{
    scope:eotg_test_county = {{ eotg_frontier_mark_unsettled_effect = yes }}
    trigger_event = {{ id = eotg_test.421  days = 1 }}
}}""",
  [ev('eotg_test.421', f"""
{check('AL3.1', 'eotg_frontier_establish_alertable = yes', 'the alert condition holds', 'eotg_frontier_establish_alertable is false (not enough gold, at war, or the capital is occupied or Unclaimed)')}
{log('AL3 LOOK: the top bar shows the establish alert; clicking it opens Establish a Frontier')}
{log('AL3 DONE')}""")])

T('AL4', 'al4_calibration_lapsed', 'AL4: Alert: Implant Calibration Lapsed',
  'As a ruler with the cybernetics trait: removes the calibration modifier, then says whether the top-bar alert should show. A look test.',
  'integration_v1 §4.2 (INT1 alert 5)',
  f"""
{log('AL4 START: calibration-lapsed alert')}
if = {{
    limit = {{ has_trait = eotg_cybernetics }}
    if = {{
        limit = {{ has_character_modifier = eotg_mod_implant_calibrated }}
        remove_character_modifier = eotg_mod_implant_calibrated
    }}
    trigger_event = {{ id = eotg_test.431  days = 1 }}
}}
else = {{
    {log('AL4 SKIP: needs the cybernetics trait; run CY1 first')}
}}""",
  [ev('eotg_test.431', f"""
if = {{
    limit = {{ can_execute_decision = eotg_decision_maintenance_protocol }}
    {log('AL4.1 LOOK: Maintenance Protocol can be taken, so the top bar should show the calibration alert (unless you marked the decision important)')}
}}
else = {{
    {log('AL4.1 LOOK: Maintenance Protocol cannot be taken now (cost or cooldown), so the top bar should NOT show the calibration alert')}
}}
{log('AL4 DONE')}""")])

# ---------------------------------------------------------------- Game rules
def rule_block(tid, rule, settings):
    ors = '\n'.join(f'    has_game_rule = {s}' for s in settings)
    lines = []
    first = True
    for s in settings:
        kw = 'if' if first else 'else_if'
        lines.append(f"""{kw} = {{
    limit = {{ has_game_rule = {s} }}
    {log(f'{tid} INFO: {rule} = {s}')}
}}""")
        first = False
    lines.append(f"""else = {{
    {log(f'{tid} FAIL: {rule} reads no known setting (a renamed key goes silently false in old saves)')}
}}""")
    return '\n'.join(lines)
RULES = [
 ('eotg_aug_event_frequency', ['eotg_aug_events_normal', 'eotg_aug_events_low', 'eotg_aug_events_high', 'eotg_aug_events_off']),
 ('eotg_aug_ai_uptake', ['eotg_aug_ai_uptake_normal', 'eotg_aug_ai_uptake_low', 'eotg_aug_ai_uptake_high']),
 ('eotg_frontier_difficulty', ['eotg_frontier_difficulty_normal', 'eotg_frontier_difficulty_easy', 'eotg_frontier_difficulty_hard']),
 ('eotg_race_half_races', ['eotg_race_half_races_off', 'eotg_race_half_races_as_own_race']),
 ('eotg_race_crossbreeding', ['eotg_race_crossbreeding_free']),
]
T('GR1', 'gr1_game_rules', 'GR1: Read the Game Rules',
  'Logs the active setting of every mod game rule, and fails any rule that reads no known setting.',
  'integration_v2 §6 (INT5); races_framework_v1 §8-§9',
  log('GR1 START: game rules') + '\n' + '\n'.join(rule_block('GR1', r, s) for r, s in RULES) + '\n' +
  log('GR1 LOOK: compare with the lobby settings you chose; behaviour checks are in the specs named in the README') + '\n' + log('GR1 DONE'))

# ---------------------------------------------------------------- G2 resources (PMC, Corporation, Trade Oligarchy)
# Added 2026-11-03 (final H1). Each resource has one writer; these tests drive the
# writer and assert what follows from it (the story counter the sync effect writes,
# the scaled modifier's presence, the election-band LOOKs), never the variable alone.
def eq(lhs, rhs):
    """Exact equality of two values, written as the harness always does (>= and <=)."""
    return f'{lhs} >= {rhs}\n{lhs} <= {rhs}'
def delta_to(name, target, current):
    """Save scope:<name> = target - current, so a writer can be driven to an exact value."""
    return f"""save_scope_value_as = {{
    name = {name}
    value = {{
        value = {target}
        subtract = {current}
    }}
}}"""
def clamp_expect(var, base, delta):
    """set_variable var = clamp(base + delta, 0, 100): the expected writer result."""
    return f"""set_variable = {{
    name = {var}
    value = {{
        value = {base}
        add = {delta}
        min = 0
        max = 100
    }}
}}"""

G2 = [
 # tid, key, Name, role trigger, writer, value, variable, story, shown var, modifier, spec ids
 ('GP1', 'gp1_pmc_standing', 'PMC', 'eotg_pmc_is_landed_pmc', 'eotg_pmc_change_standing_effect',
  'eotg_pmc_standing_value', 'eotg_pmc_standing', 'eotg_story_pmc_standing', 'eotg_pmc_standing_shown',
  'eotg_pmc_standing_modifier', 'PMC spec V-P2, V-P3', 'standing', '(Debug) Become a PMC, or play Raoul'),
 ('GC1', 'gc1_corp_influence', 'Corporation', 'eotg_corporation_is_landed_corporation', 'eotg_corporation_change_board_influence_effect',
  'eotg_corporation_board_influence_value', 'eotg_corp_board_influence', 'eotg_story_corporation_board', 'eotg_corporation_board_shown',
  'eotg_corporation_board_modifier', 'Corporation spec V-CO2, V-CO3', 'board influence', 'play Hoel or Konan'),
 ('GT1', 'gt1_gobcorp_share', 'Trade Oligarchy', 'eotg_gobcorp_is_landed_gobcorp', 'eotg_gobcorp_change_market_share_effect',
  'eotg_gobcorp_market_share_value', 'eotg_gobcorp_market_share', 'eotg_story_gobcorp_market', 'eotg_gobcorp_market_share_shown',
  'eotg_gobcorp_market_share_modifier', 'Trade Oligarchy spec V-TO2, V-TO3', 'market share', 'play Bertrand'),
]
for n, (tid, key, gname, role, writer, val, var, story, shown, mod, refs, noun, who) in enumerate(G2):
    e1, e2 = f'eotg_test.{321 + 10 * n}', f'eotg_test.{322 + 10 * n}'
    counter = f'any_owned_story = {{\n    story_type = {story}\n    {eq(f"var:{shown}", f"root.var:{var}").replace(chr(10), chr(10) + "    ")}\n}}'
    T(tid, key, f'{tid}: {gname} Resource Follows a Change',
      f'As a landed {gname} ruler: reads your {noun}, moves it by +10 (or -10 near the top) through its only writer, then by 120 past the cap, and checks the story counter, the modifier and the clamp each time.',
      refs,
      f"""
{log(f'{tid} START: {noun} writer, story counter and modifier')}
if = {{
    limit = {{ {role} = no }}
    {log(f'{tid} SKIP: needs a landed {gname} ruler; {who}')}
}}
else = {{
    set_variable = {{ name = eotg_test_before  value = {val} }}
    if = {{
        limit = {{ {val} > 90 }}
        save_scope_value_as = {{ name = eotg_test_delta  value = -10 }}
    }}
    else = {{
        save_scope_value_as = {{ name = eotg_test_delta  value = 10 }}
    }}
    set_variable = {{ name = eotg_test_delta  value = scope:eotg_test_delta }}
    {writer} = {{ AMOUNT = scope:eotg_test_delta }}
    trigger_event = {{ id = {e1}  days = 1 }}
}}""",
      [ev(e1, f"""
{check(f'{tid}.1', eq(val, '{ value = var:eotg_test_before add = var:eotg_test_delta }'), f'{noun} moved by exactly the delta', f'{noun} did not move by exactly the delta through the writer')}
{check(f'{tid}.2', counter, 'the story counter mirrors the new value (sync effect ran)', f'the {story} counter does not match the value after a write')}
{check(f'{tid}.3', f'has_character_modifier = {mod}', 'the scaled modifier is present after the write (re-applied)', f'{mod} is missing after a write')}
{log(f'{tid}.4 LOOK: hover {mod}: its numbers must match the new value, not the old one (a scaled modifier is computed when added; the writer re-applies it)')}
{writer} = {{ AMOUNT = 120 }}
trigger_event = {{ id = {e2}  days = 1 }}"""),
       ev(e2, f"""
{check(f'{tid}.5', eq(val, '100'), f'{noun} +120 clamps at 100', f'{noun} is not 100 after +120')}
{check(f'{tid}.6', counter, 'the story counter follows the clamp', 'the story counter does not show the clamped value')}
save_scope_value_as = {{ name = eotg_test_back  value = {{ value = var:eotg_test_before subtract = 100 }} }}
{writer} = {{ AMOUNT = scope:eotg_test_back }}
{check(f'{tid}.7', eq(val, 'var:eotg_test_before'), f'{noun} restored to the baseline', f'{noun} not restored to the baseline')}
remove_variable = eotg_test_before
remove_variable = eotg_test_delta
{log(f'{tid} DONE')}""")])

# PMC battle feed (V-P6). The on_action root is a combat side, which a decision
# cannot build, so the test drives the writer with the on_action's own named
# values and leaves the wiring to a LOOK (fight a battle as war leader).
T('GP2', 'gp2_pmc_battle_feed', 'GP2: PMC Battle Feed Values',
  'As a landed PMC ruler with standing between 3 and 97: applies the battle-won value, then the battle-lost value, through the standing writer, and checks +2 then -3 exactly. The battle hook itself is a look check.',
  'PMC spec V-P6',
  f"""
{log('GP2 START: battle feed values')}
if = {{
    limit = {{ eotg_pmc_is_landed_pmc = no }}
    {log('GP2 SKIP: needs a landed PMC ruler; (Debug) Become a PMC, or play Raoul')}
}}
else_if = {{
    limit = {{
        OR = {{
            eotg_pmc_standing_value < 3
            eotg_pmc_standing_value > 97
        }}
    }}
    {log('GP2 SKIP: standing is within 3 of a clamp, so the exact deltas cannot show; run GP1 or wait')}
}}
else = {{
    set_variable = {{ name = eotg_test_before  value = eotg_pmc_standing_value }}
    eotg_pmc_change_standing_effect = {{ AMOUNT = eotg_pmc_battle_won_value }}
    trigger_event = {{ id = eotg_test.351  days = 1 }}
}}""",
  [ev('eotg_test.351', f"""
{check('GP2.1', eq('eotg_pmc_standing_value', '{ value = var:eotg_test_before add = 2 }'), 'a won battle is worth +2', 'eotg_pmc_battle_won_value did not move standing by +2')}
eotg_pmc_change_standing_effect = {{ AMOUNT = eotg_pmc_battle_lost_value }}
{check('GP2.2', eq('eotg_pmc_standing_value', '{ value = var:eotg_test_before add = -1 }'), 'a lost battle is worth -3 (net -1 from the baseline)', 'eotg_pmc_battle_lost_value did not move standing by -3')}
save_scope_value_as = {{ name = eotg_test_back  value = 1 }}
eotg_pmc_change_standing_effect = {{ AMOUNT = scope:eotg_test_back }}
remove_variable = eotg_test_before
{log('GP2.3 LOOK: the hook: fight a battle as war leader (console: add armies near an enemy); standing +2 on a win, -3 on a loss, read from the story counter')}
{log('GP2 DONE')}""")])

# Court the Board (V-CO8 and the 2026-11-03 erosion fix). The decision is taken
# by a Corporation VASSAL and its effect is inline, so the harness brackets the
# real decision: a record step before, a check step after. GC2b pre-marks the
# liege as eroded this year (the decision's own guard variable) to prove the
# second courting of a year costs the liege nothing.
COURT_RECORD = """
set_variable = {{ name = eotg_test_own_before  value = eotg_corporation_board_influence_value }}
set_variable = {{ name = eotg_test_projected  value = eotg_corporation_court_projected_value }}
liege = {{
    set_variable = {{ name = eotg_test_liege_before  value = eotg_corporation_board_influence_value }}
    {mark}
    if = {{
        limit = {{ has_variable = eotg_corp_board_eroded }}
        set_variable = {{ name = eotg_test_liege_eroded  value = 1 }}
    }}
    else = {{
        set_variable = {{ name = eotg_test_liege_eroded  value = 0 }}
    }}
}}"""
for sfx, mark, nm, desc in (
    ('A', '', 'Record (Normal Path)', 'records your influence, the projected value and your liege\'s influence and erosion state'),
    ('B', 'set_variable = { name = eotg_corp_board_eroded  years = 1 }', 'Record (Liege Already Eroded)', 'marks your liege as already eroded this year (the decision\'s own guard), then records the same values')):
    T(f'GC2{sfx}', f'gc2{sfx.lower()}_court_board_record', f'GC2{sfx.lower()}: Court the Board, {nm}',
      f'As a Corporation vassal under a Corporation liege: {desc}. Then take Court the Board yourself, and run GC2c the next day.',
      'Corporation spec V-CO8; QA 2026-11-03 erosion fix',
      f"""
{log(f'GC2{sfx} START: Court the Board, record')}
if = {{
    limit = {{
        OR = {{
            eotg_corporation_role_vassal = no
            NOT = {{ liege ?= {{ eotg_corporation_role_top = yes }} }}
        }}
    }}
    {log(f'GC2{sfx} SKIP: needs a Corporation vassal under a Corporation liege; play Konan')}
}}
# UNVERIFIED-VANILLA: is_decision_on_cooldown (a character trigger in 1.20 .info)
else_if = {{
    limit = {{ NOT = {{ is_decision_on_cooldown = eotg_decision_corporation_court_board }} }}
{ind(COURT_RECORD.format(mark=mark), 4)}
    {log(f'GC2{sfx} LOOK: now take Court the Board, then GC2c tomorrow')}
}}
else = {{
    {log(f'GC2{sfx} SKIP: Court the Board is on its 5-year cooldown; reload a save from before you took it')}
}}""")
T('GC2C', 'gc2c_court_board_check', 'GC2c: Court the Board, Check',
  'After GC2a or GC2b and the real Court the Board: checks your gain and that your liege lost exactly 5 only if not already eroded this year and only if your projected value was above theirs.',
  'Corporation spec V-CO8; QA 2026-11-03 erosion fix',
  f"""
{log('GC2C START: Court the Board, check')}
if = {{
    limit = {{ NOT = {{ has_variable = eotg_test_projected }} }}
    {log('GC2C SKIP: nothing recorded; run GC2a or GC2b, then take Court the Board')}
}}
else = {{
    {check('GC2C.1', eq('eotg_corporation_board_influence_value', 'var:eotg_test_projected'), 'your influence is the projected value (+15, clamped)', 'your influence is not the recorded projection: was Court the Board taken?')}
    liege = {{
        if = {{
            limit = {{
                var:eotg_test_liege_eroded = 0
                var:eotg_test_liege_before < root.var:eotg_test_projected
            }}
            {check('GC2C.2', eq('eotg_corporation_board_influence_value', '{ value = var:eotg_test_liege_before add = -5 max = 100 min = 0 }'), 'the liege lost exactly 5 (not eroded yet, director projected above the CEO)', 'the liege did not lose exactly 5 on an eligible courting')}
            {check('GC2C.3', 'has_variable = eotg_corp_board_eroded', 'the liege is marked eroded for the year', 'no eotg_corp_board_eroded on the liege after erosion')}
        }}
        else = {{
            {check('GC2C.4', eq('eotg_corporation_board_influence_value', 'var:eotg_test_liege_before'), 'the liege lost nothing (already eroded this year, or the CEO was at or above your projection)', 'the liege lost influence when the guard should have held')}
        }}
        remove_variable = eotg_test_liege_before
        remove_variable = eotg_test_liege_eroded
    }}
    remove_variable = eotg_test_own_before
    remove_variable = eotg_test_projected
    {log('GC2C DONE')}
}}""")

# Corner the Market (V-TO7). Taken by the top Trade Oligarch; inline effect,
# so the same bracket. GT2a pre-marks the first vassal Prince as cornered this
# year (the decision's own guard) when there are two or more.
T('GT2A', 'gt2a_corner_record', 'GT2a: Corner the Market, Record',
  'As the top Trade Oligarch with Trade Oligarchy vassals: records your share and each vassal Prince\'s, and marks one Prince as already cornered this year when you have two or more. Then take Corner the Market, and run GT2b the next day.',
  'Trade Oligarchy spec V-TO7',
  f"""
{log('GT2A START: Corner the Market, record')}
if = {{
    limit = {{
        OR = {{
            eotg_gobcorp_role_top = no
            NOT = {{ any_vassal = {{ government_has_flag = eotg_government_is_gobcorp }} }}
        }}
    }}
    {log('GT2A SKIP: needs the top Trade Oligarch with Trade Oligarchy vassals (V-TO9: grant counties by console)')}
}}
# UNVERIFIED-VANILLA: is_decision_on_cooldown (as GC2a)
else_if = {{
    limit = {{ is_decision_on_cooldown = eotg_decision_gobcorp_corner_market }}
    {log('GT2A SKIP: Corner the Market is on its cooldown; reload a save from before you took it')}
}}
else = {{
    set_variable = {{ name = eotg_test_own_before  value = eotg_gobcorp_market_share_value }}
    if = {{
        limit = {{ any_vassal = {{ count >= 2  government_has_flag = eotg_government_is_gobcorp }} }}
        random_vassal = {{
            limit = {{ government_has_flag = eotg_government_is_gobcorp }}
            set_variable = {{ name = eotg_gobcorp_cornered  years = 1 }}
        }}
    }}
    every_vassal = {{
        limit = {{ government_has_flag = eotg_government_is_gobcorp }}
        set_variable = {{ name = eotg_test_share_before  value = eotg_gobcorp_market_share_value }}
        if = {{
            limit = {{ has_variable = eotg_gobcorp_cornered }}
            set_variable = {{ name = eotg_test_was_cornered  value = 1 }}
        }}
    }}
    {log('GT2A LOOK: now take Corner the Market, then GT2b tomorrow')}
}}""")
T('GT2B', 'gt2b_corner_check', 'GT2b: Corner the Market, Check',
  'After GT2a and the real Corner the Market: checks your gain, that every Prince not yet cornered lost exactly 5 and is now marked, and that the pre-marked Prince lost nothing.',
  'Trade Oligarchy spec V-TO7',
  f"""
{log('GT2B START: Corner the Market, check')}
if = {{
    limit = {{ NOT = {{ has_variable = eotg_test_own_before }} }}
    {log('GT2B SKIP: nothing recorded; run GT2a, then take Corner the Market')}
}}
else = {{
    {check('GT2B.1', eq('eotg_gobcorp_market_share_value', '{ value = var:eotg_test_own_before add = 15 max = 100 }'), 'your share rose by 15 (clamped)', 'your share did not rise by 15: was Corner the Market taken?')}
    if = {{
        limit = {{
            any_vassal = {{
                has_variable = eotg_test_share_before
                NOT = {{ has_variable = eotg_test_was_cornered }}
                NOT = {{ {eq('eotg_gobcorp_market_share_value', '{ value = var:eotg_test_share_before add = -5 min = 0 }').replace(chr(10), ' ')} }}
            }}
        }}
        {log('GT2B.2 FAIL: a Prince not yet cornered did not lose exactly 5')}
    }}
    else = {{
        {log('GT2B.2 PASS: every Prince not yet cornered lost exactly 5')}
    }}
    if = {{
        limit = {{
            any_vassal = {{
                has_variable = eotg_test_was_cornered
                NOT = {{ {eq('eotg_gobcorp_market_share_value', 'var:eotg_test_share_before').replace(chr(10), ' ')} }}
            }}
        }}
        {log('GT2B.3 FAIL: a Prince already cornered this year was drained again')}
    }}
    else_if = {{
        limit = {{ any_vassal = {{ has_variable = eotg_test_was_cornered }} }}
        {log('GT2B.3 PASS: the Prince already cornered this year was not drained again')}
    }}
    else = {{
        {log('GT2B.3 SKIP: only one Prince, so the once-a-year guard was not exercised (V-TO9: make a second)')}
    }}
    {check('GT2B.4', 'NOT = { any_vassal = { has_variable = eotg_test_share_before NOT = { has_variable = eotg_gobcorp_cornered } } }', 'every Prince is marked cornered for the year', 'a Prince has no eotg_gobcorp_cornered after Corner the Market')}
    every_vassal = {{
        limit = {{ has_variable = eotg_test_share_before }}
        remove_variable = eotg_test_share_before
        if = {{
            limit = {{ has_variable = eotg_test_was_cornered }}
            remove_variable = eotg_test_was_cornered
        }}
    }}
    remove_variable = eotg_test_own_before
    {log('GT2B DONE')}
}}""")

# Election bands (V-CO13, V-TO13). Vote strength cannot be read in script, so the
# test drives the ruler's value to each band edge through the writer, a day
# apart, and the player reads the title's vote tooltip at each LOOK line.
for tid, key, gname, role, writer, val, bands, refs, label in (
    ('GE1', 'ge1_corp_bands', 'Corporation', 'eotg_corporation_is_landed_corporation', 'eotg_corporation_change_board_influence_effect',
     'eotg_corporation_board_influence_value', ['eotg_corporation_board_vote_band_1_value', 'eotg_corporation_board_vote_band_2_value'],
     'Corporation spec V-CO13', ['Hold on the board (+1)', 'the second board bonus (+1 more)']),
    ('GE2', 'ge2_gobcorp_bands', 'Trade Oligarchy', 'eotg_gobcorp_is_landed_gobcorp', 'eotg_gobcorp_change_market_share_effect',
     'eotg_gobcorp_market_share_value', ['eotg_gobcorp_vote_band_1_value', 'eotg_gobcorp_vote_band_2_value', 'eotg_gobcorp_vote_band_3_value'],
     'Trade Oligarchy spec V-TO13', ['the first share band (+1)', 'the second (+2)', 'the third (+3)'])):
    base = 361 if tid == 'GE1' else 371
    steps = []
    targets = [(f'{{ value = {bands[0]} add = -1 }}', 'just below the first band: no band line')] + [(b, f'at {b}: expect {l}') for b, l in zip(bands, label)]
    for i, (tgt, what) in enumerate(targets):
        nxt = f'trigger_event = {{ id = eotg_test.{base + i + 1}  days = 1 }}' if i + 1 < len(targets) else ''
        steps.append(ev(f'eotg_test.{base + i}', f"""
{delta_to('eotg_test_delta', tgt, val)}
{writer} = {{ AMOUNT = scope:eotg_test_delta }}
{check(f'{tid}.{i + 1}', eq(val, tgt), 'the value sits on the band edge', 'the writer did not land on the band edge')}
{log(f'{tid}.{i + 1} LOOK: open your primary title succession tooltip: {what}')}
{nxt}"""))
    steps[-1] = ev(steps[-1][0], steps[-1][1] + f"""
save_scope_value_as = {{ name = eotg_test_back  value = {{ value = var:eotg_test_before subtract = {val} }} }}
{writer} = {{ AMOUNT = scope:eotg_test_back }}
remove_variable = eotg_test_before
{log(f'{tid} LOOK: a landless councillor shows no band line (V-CO13); gold no longer adds vote strength (V-TO13)')}
{log(f'{tid} DONE (value restored)')}""")
    T(tid, key, f'{tid}: {gname} Election Bands',
      f'As a landed {gname} ruler: moves your value to each vote-strength band edge, a day apart, and says what the succession tooltip should show. Then restores the value.',
      refs,
      f"""
{log(f'{tid} START: election bands')}
if = {{
    limit = {{ {role} = no }}
    {log(f'{tid} SKIP: needs a landed {gname} ruler')}
}}
else = {{
    set_variable = {{ name = eotg_test_before  value = {val} }}
    trigger_event = {{ id = eotg_test.{base}  days = 1 }}
}}""", steps)

# ---------------------------------------------------------------- Void Corruption (docs/specs/void_corruption_v2.md §10)
VOID_BANDS = ('eotg_mod_void_whispers', 'eotg_mod_void_pressure', 'eotg_mod_void_saturation')
def only_band(keep, mods=VOID_BANDS):
    return '\n'.join((f'has_character_modifier = {m}' if m == keep else f'NOT = {{ has_character_modifier = {m} }}') for m in mods)
def void_to(target):
    return delta_to('eotg_test_delta', target, 'var:eotg_void_exposure') + '\neotg_void_change_exposure_effect = { AMOUNT = scope:eotg_test_delta }'

T('VD1', 'vd1_void_bands', 'VD1: Void Exposure Bands',
  'As a ruler who is not Hollowed: moves Void exposure through 24, 25, 50 and 75 with its only writer, a day apart, and checks that exactly the right band modifier follows each time. Then restores your exposure.',
  'Void spec V-V3',
  f"""
{log('VD1 START: exposure bands')}
if = {{
    limit = {{ has_trait = eotg_void_hollowed }}
    {log('VD1 SKIP: the Hollowed carry no exposure band; use a ruler who is not Hollowed')}
}}
else = {{
    eotg_void_change_exposure_effect = {{ AMOUNT = 0 }}
    set_variable = {{ name = eotg_test_before  value = var:eotg_void_exposure }}
{ind(void_to(24), 4)}
    trigger_event = {{ id = eotg_test.501  days = 1 }}
}}""",
  [ev('eotg_test.501', f"""
{check('VD1.1', only_band('none'), 'exposure 24: no band', 'a band modifier is present at exposure 24')}
{void_to(25)}
trigger_event = {{ id = eotg_test.502  days = 1 }}"""),
   ev('eotg_test.502', f"""
{check('VD1.2', only_band(VOID_BANDS[0]), 'exposure 25: Void Whispers only', 'exposure 25 is not Whispers alone')}
{void_to(50)}
trigger_event = {{ id = eotg_test.503  days = 1 }}"""),
   ev('eotg_test.503', f"""
{check('VD1.3', only_band(VOID_BANDS[1]), 'exposure 50: Void Pressure only (Whispers removed)', 'exposure 50 is not Pressure alone')}
{void_to(75)}
trigger_event = {{ id = eotg_test.504  days = 1 }}"""),
   ev('eotg_test.504', f"""
{check('VD1.4', only_band(VOID_BANDS[2]), 'exposure 75: Void Saturation only', 'exposure 75 is not Saturation alone')}
{void_to('var:eotg_test_before')}
if = {{
    limit = {{ var:eotg_void_exposure < 25 }}
    {check('VD1.5', only_band('none'), 'restored below 25: no band', 'a band survived the restore')}
}}
else = {{
    {check('VD1.5', 'OR = { ' + ' '.join(f'has_character_modifier = {m}' for m in VOID_BANDS) + ' }', 'restored: a band matches the restored exposure', 'no band after restoring an exposure of 25 or more')}
}}
remove_variable = eotg_test_before
{log('VD1 LOOK: the band modifier tooltip text (Whispers, Pressure, Saturation)')}
{log('VD1 DONE (exposure restored; VD1 may have advanced Void events: the on_action reads exposure yearly)')}""")])

T('VD2', 'vd2_void_hollowing_path', 'VD2: The Hollowing Through the Yearly Pulse',
  'Makes you Void-Touched with exposure 100 through the system\'s own effects, clears the Void event cooldown, runs the real yearly Void pulse once, and checks that the pulse set the cooldown itself. The Hollowing event follows: answer it (avoid stepping down if you want to keep playing this ruler), then run VD3. Skips if a Voidwalker is at court (VD4 leaves one). This ruler stays Hollowed: throwaway save.',
  'Void spec V-V8, V-V17 (cooldown authority in the on_action)',
  f"""
{log('VD2 START: the Hollowing through the yearly pulse')}
if = {{
    limit = {{ has_trait = eotg_void_hollowed }}
    {log('VD2 SKIP: already Hollowed; run VD3')}
}}
else_if = {{
    limit = {{ eotg_void_has_voidwalker = yes }}
    {log('VD2 SKIP: a Voidwalker is at court (VD4 leaves one); reload a save from before VD4')}
}}
else = {{
    eotg_void_become_touched_effect = yes
    eotg_void_change_exposure_effect = {{ AMOUNT = 100 }}
    if = {{
        limit = {{ has_character_flag = eotg_flag_void_event_cooldown }}
        remove_character_flag = eotg_flag_void_event_cooldown
    }}
    trigger_event = {{ on_action = eotg_on_yearly_void_check }}
    trigger_event = {{ id = eotg_test.511  days = 1 }}
}}""",
  [ev('eotg_test.511', f"""
{check('VD2.1', 'has_character_flag = eotg_flag_void_event_cooldown', 'the on_action set the event cooldown when it fired the Hollowing (no event sets it)', 'no cooldown flag after the pulse fired: the on_action is not the cooldown authority, or the Hollowing branch did not fire')}
{check('VD2.2', 'var:eotg_void_exposure >= 100', 'exposure is still at the cap after the pulse (no Voidwalker at court, so the accrual is not negative)', 'exposure fell below 100 after the pulse')}
{log('VD2 LOOK: The Hollowing (eotg_void.0030) arrives within 10 days; answer it, then take VD3')}
{log('VD2 DONE')}""")])

T('VD3', 'vd3_void_depth', 'VD3: Hollowing Depth Bands and Drift',
  'As a Hollowed ruler (run VD2 first): checks the Hollowed state, moves Hollowing depth through 50, 85 and 10 with its only writer and checks the depth band each time, then runs the yearly Void pulse once and checks the +4 drift. Restores your depth.',
  'Void spec V-V9, V-V10, V-V11, V-V12',
  f"""
{log('VD3 START: Hollowing depth bands and drift')}
if = {{
    limit = {{ NOT = {{ has_trait = eotg_void_hollowed }} }}
    {log('VD3 SKIP: needs the Hollowed trait; run VD2 and answer The Hollowing')}
}}
else = {{
    {check('VD3.1', 'NOT = { has_trait = eotg_void_touched }\nvar:eotg_void_exposure >= 100\n' + only_band('none'), 'Hollowed state: Touched removed, exposure 100, no exposure band', 'the Hollowed state is wrong (Touched kept, exposure below 100, or a band left)')}
    # UNVERIFIED-VANILLA: has_opinion_modifier = {{ modifier target }} (vanilla trigger)
    if = {{
        limit = {{ any_courtier = {{ count >= 1 }} }}
        {check('VD3.2', 'any_courtier = { has_opinion_modifier = { modifier = eotg_opinion_void_unreachable target = root } }', 'the court holds the Unreachable opinion of you', 'no courtier has eotg_opinion_void_unreachable')}
    }}
    set_variable = {{ name = eotg_test_before  value = var:eotg_void_hollowing_depth }}
{ind(delta_to('eotg_test_delta', 50, 'var:eotg_void_hollowing_depth'), 4)}
    eotg_void_change_hollowing_depth_effect = {{ AMOUNT = scope:eotg_test_delta }}
    trigger_event = {{ id = eotg_test.521  days = 1 }}
}}""",
  [ev('eotg_test.521', f"""
{check('VD3.3', only_band('eotg_mod_void_hollow_far', ('eotg_mod_void_hollow_far', 'eotg_mod_void_hollow_quiet')), 'depth 50: Far Off only', 'depth 50 is not Far Off alone')}
{delta_to('eotg_test_delta', 85, 'var:eotg_void_hollowing_depth')}
eotg_void_change_hollowing_depth_effect = {{ AMOUNT = scope:eotg_test_delta }}
trigger_event = {{ id = eotg_test.522  days = 1 }}"""),
   ev('eotg_test.522', f"""
{check('VD3.4', only_band('eotg_mod_void_hollow_quiet', ('eotg_mod_void_hollow_far', 'eotg_mod_void_hollow_quiet')), 'depth 85: Gone Quiet only (Far Off removed)', 'depth 85 is not Gone Quiet alone')}
{delta_to('eotg_test_delta', 10, 'var:eotg_void_hollowing_depth')}
eotg_void_change_hollowing_depth_effect = {{ AMOUNT = scope:eotg_test_delta }}
trigger_event = {{ id = eotg_test.523  days = 1 }}"""),
   ev('eotg_test.523', f"""
{check('VD3.5', 'NOT = { has_character_modifier = eotg_mod_void_hollow_far }\nNOT = { has_character_modifier = eotg_mod_void_hollow_quiet }', 'depth 10: no depth band', 'a depth band survived at depth 10')}
# The real pulse: depth drift +4. The Hollowing set a 5-year cooldown, so no
# stage-D event should roll; if the cooldown has lapsed, 0031 or 0032 may follow.
trigger_event = {{ on_action = eotg_on_yearly_void_check }}
trigger_event = {{ id = eotg_test.524  days = 1 }}"""),
   ev('eotg_test.524', f"""
{check('VD3.6', eq('var:eotg_void_hollowing_depth', '14'), 'the yearly pulse drifted depth by exactly +4', 'depth did not drift by exactly +4 in one pulse')}
{delta_to('eotg_test_delta', 'var:eotg_test_before', 'var:eotg_void_hollowing_depth')}
eotg_void_change_hollowing_depth_effect = {{ AMOUNT = scope:eotg_test_delta }}
remove_variable = eotg_test_before
{log('VD3 LOOK: the Far Off and Gone Quiet tooltips')}
{log('VD3 DONE (depth restored)')}""")])

T('VD4', 'vd4_voidwalker', 'VD4: The Voidwalker at Court',
  'Creates and seats a Voidwalker with the same effects as option a of The Voidwalker at the Gate, then checks that the yearly accrual fell by exactly 6 and that the Voidwalker Ward decision can be taken.',
  'Void spec V-V13 (the v1 Voidwalker bug)',
  f"""
{log('VD4 START: the Voidwalker courtier')}
if = {{
    limit = {{ eotg_void_has_voidwalker = yes }}
    {log('VD4 SKIP: a Voidwalker is already at your court, so the accrual change cannot show; reload a save without one')}
}}
else = {{
    set_variable = {{ name = eotg_test_before  value = eotg_void_yearly_accrual_value }}
    eotg_void_create_voidwalker_effect = yes
    eotg_void_shelter_voidwalker_effect = yes
    trigger_event = {{ id = eotg_test.531  days = 1 }}
}}""",
  [ev('eotg_test.531', f"""
{check('VD4.1', 'any_courtier = { has_character_flag = eotg_flag_void_voidwalker }', 'the Voidwalker is a flagged courtier (the flag is no longer on the ruler)', 'no courtier carries eotg_flag_void_voidwalker')}
{check('VD4.2', eq('eotg_void_yearly_accrual_value', '{ value = var:eotg_test_before add = -6 }'), 'the yearly accrual fell by exactly 6', 'the accrual did not fall by 6 with a Voidwalker at court')}
if = {{
    limit = {{
        has_trait = eotg_void_hollowed
    }}
    {log('VD4.3 SKIP: the Hollowed cannot take the Voidwalker Ward')}
}}
else_if = {{
    limit = {{
        OR = {{
            has_character_flag = eotg_flag_void_ward_cooldown
            gold < 100
        }}
    }}
    {log('VD4.3 SKIP: the ward cooldown is running or you have under 100 gold; the decision should still be listed, greyed out (LOOK)')}
}}
else = {{
    {check('VD4.3', 'can_execute_decision = eotg_decision_void_voidwalker_ward', 'the Voidwalker Ward decision can be taken', 'the Voidwalker Ward decision cannot be taken with a Voidwalker at court')}
}}
remove_variable = eotg_test_before
{log('VD4 LOOK: the Decisions tab lists Ask the Voidwalker for the Old Ward')}
{log('VD4 DONE')}""")])

def skill_sum():
    # UNVERIFIED-VANILLA: skills read as values (as CY1 reads prowess)
    return '{ value = diplomacy add = martial add = stewardship add = intrigue add = learning add = prowess }'
T('VD5', 'vd5_void_insight', 'VD5: One Insight per Character',
  'Runs the Void Insight effect twice and checks that both runs gave their +2 skill but only one Insight modifier was ever added.',
  'Void spec V-V16',
  f"""
{log('VD5 START: Insight re-application guard')}
if = {{
    limit = {{ eotg_void_has_any_insight = yes }}
    {log('VD5 SKIP: you already hold an Insight; reload a save without one')}
}}
else = {{
    set_variable = {{ name = eotg_test_before  value = {skill_sum()} }}
    eotg_void_insight_effect = yes
    eotg_void_insight_effect = yes
    trigger_event = {{ id = eotg_test.541  days = 1 }}
}}""",
  [ev('eotg_test.541', f"""
set_variable = {{ name = eotg_test_after  value = {skill_sum()} }}
{check('VD5.1', eq('var:eotg_test_after', '{ value = var:eotg_test_before add = 4 }'), 'two Insights gave +2 skill each (+4 total)', 'the skill total did not rise by exactly 4')}
{check('VD5.2', 'eotg_void_has_any_insight = yes', 'an Insight modifier is held', 'no Insight modifier after the effect')}
remove_variable = eotg_test_before
remove_variable = eotg_test_after
{log('VD5.3 LOOK: the character window lists ONE Insight modifier, not two copies')}
{log('VD5 DONE')}""")])

# ================================================================ write files
DEC_HDR = """# -- eotg_test_harness_decisions.txt -------------------------------------------
# GENERATED by docs/tools/gen_test_harness.py: never hand-edit; change the generator and re-run.
# In-game test harness (docs/qa/TEST_HARNESS.md), in the test sub-mod
# docs/test_submods/test_harness (test content never ships). DEBUG ONLY: every decision is
# `debug_only = yes` (visible only under -debug_mode), never alerts, and the AI
# never takes one. Gating copied from the shipped debug decisions
# (eotg_government_debug_decisions.txt:9-41; eotg_frontier_decisions.txt:748-790).
# Each decision sets up one check through the systems' OWN effects and, where
# the result can be read in script, fires a hidden eotg_test event days later
# that writes `EOTG_TEST <id> PASS|FAIL|LOOK|INFO|SKIP|START|DONE: ...` to
# logs/debug.log with debug_log. Visual checks only log LOOK lines.
# These decisions MUTATE the save (traits, Frontier state, payers, dread):
# use a throwaway save.
# Tiger and PX checked locally (2026-11-03); not yet run in game.
# -----------------------------------------------------------------------------
"""
dec = [DEC_HDR]
loc = ['l_english:', ' # In-game test harness (docs/qa/TEST_HARNESS.md). Debug only. GENERATED by docs/tools/gen_test_harness.py.']
for t in TESTS:
    k = f"eotg_decision_test_{t['suffix']}"
    dec.append(f"""
# {t['tid']}: {t['name'].split(': ',1)[1]}. Plan: {t['refs']}.
{k} = {{
    picture = {{
        reference = "gfx/interface/illustrations/decisions/decision_realm.dds"
    }}
    desc = {k}_desc
    selection_tooltip = {k}_tooltip
    confirm_text = {k}_confirm
    should_create_alert = {{ always = no }}
    ai_check_interval_by_tier = {{
        barony = 0
        county = 0
        duchy = 0
        kingdom = 0
        empire = 0
        hegemony = 0
    }}

    is_shown = {{
        debug_only = yes
        is_landed = yes
    }}

    effect = {{
        custom_tooltip = eotg_decision_test_effect_tt
        hidden_effect = {{
{ind(t['effect'], 12)}
        }}
    }}

    ai_potential = {{
        always = no
    }}
    ai_will_do = {{
        base = 0
    }}
}}
""")
    loc.append(f' {k}:0 "(Test) {t["name"]}"')
    loc.append(f' {k}_desc:0 "Testing only. {t["desc"]} Results go to logs/debug.log on lines starting EOTG_TEST {t["tid"]}."')
    loc.append(f' {k}_tooltip:0 "Testing only: {t["name"].split(": ",1)[1]}"')
    loc.append(f' {k}_confirm:0 "Run the test"')
loc.append(' eotg_decision_test_effect_tt:0 "Sets up the test scenario on this save and writes the result to logs/debug.log. Use a throwaway save."')

EV_HDR = """# -- eotg_test_harness.txt ------------------------------------------------------
# GENERATED by docs/tools/gen_test_harness.py: never hand-edit; change the generator and re-run.
# In-game test harness: the delayed assertions (docs/qa/TEST_HARNESS.md).
# Every event here is HIDDEN and fired ONLY by an eotg_decision_test_*
# decision (common/decisions/eotg_test_harness_decisions.txt in this sub-mod), which are
# debug_only (invariant 4: always fired by something; no on_action hook).
# Root = the decision taker. Scopes saved by the decision (eotg_test_county,
# eotg_test_target, eotg_test_subject, actor, recipient) carry into the delayed
# event, as the mod's own chains rely on (e.g. eotg_aug_heir.006 reads
# scope:eotg_heir days later).
# Assertions read the systems' own scripted triggers and values only.
# UNVERIFIED-VANILLA: debug_log writes its literal string to logs/debug.log (the
#   effect is used in v2 script, eotg_race_effects.txt, with data functions;
#   the strings here are plain text on purpose).
# Tiger and PX checked locally (2026-11-03); not yet run in game.
# -----------------------------------------------------------------------------

namespace = eotg_test
"""
evs = [EV_HDR]
for eid, body in EVENTS:
    evs.append(f"""
{eid} = {{
    type = character_event
    hidden = yes

    immediate = {{
{ind(body, 8)}
    }}
}}
""")

def w(path, text):
    p = os.path.join(ROOT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(BOM + text)
def w_plain(path, text):   # no BOM: the descriptor and README (as docs/test_submods/races)
    p = os.path.join(ROOT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(text)
w('common/decisions/eotg_test_harness_decisions.txt', ''.join(dec))
w('events/eotg_test_harness.txt', ''.join(evs))
w('localization/english/eotg_test_harness_l_english.yml', '\n'.join(loc) + '\n')
# The dependency is the main mod's descriptor name (echoes_of_the_grip.mod), as the other test sub-mods
w_plain('descriptor.mod', '''version="0.1.0"
tags={
	"Utilities"
}
name="EotG Test: In-Game Test Harness"
dependencies={
	"Echoes of the Grip"
}
supported_version="1.20.*"
''')
w_plain('README.md', '''# EotG Test: In-Game Test Harness (sub-mod)

**Test only, never shipped.** GENERATED by `docs/tools/gen_test_harness.py`: never hand-edit anything in this
folder; change the generator and re-run it.

The full guide (install, playsets, reading `logs/debug.log`, every test) is `docs/qa/TEST_HARNESS.md`.
''')
print(len(TESTS), 'tests,', len(EVENTS), 'events ->', ROOT)
