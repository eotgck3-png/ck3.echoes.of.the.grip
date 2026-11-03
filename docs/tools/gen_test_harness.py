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
