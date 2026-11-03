"""Confluence Legacies: the v2 design (docs/specs/legacies_v2.md), driven by the v1 numbers.

    python docs/tools/sim/models/legacies.py [--sites 20000] [--years 100] [--seed 20261103] [--md OUT.md] [--json OUT.json]
    (about 2 minutes for the default 20,000 sites x 11 scenarios; numpy only)

Reads the v1 files through pdx_read (Script(repo='OLD PROJECT VERSION')):
  - every option of the 16 events (events/eotg_legacy_events.txt): ai_chance base, gate
    kind, attention and integrity AMOUNTs, condition writes, direct integrity sets (0104),
    seeding and discovery calls, random_list branches inside options (0002.a), follow-up
    trigger_event ids (0011/0021/0031/0041);
  - the survey decision (common/decisions/eotg_legacy_decisions.txt): ai_will_do,
    ai_check_interval, cost, and the fallback random_list (0004/0002/0003 weights and the
    skill modifiers on 0004);
  - the yearly pulse (common/on_action/eotg_legacy_on_actions.txt): the attention decay
    AMOUNT, the three aftermath chances and their site cooldowns, the aftermath flag years;
  - the seed family weights (eotg_se_legacy_seed_random) and the start integrity
    (eotg_se_legacy_seed).
It models the v2 DESIGN, not v1's script:
  - discovery is by survey only (the Exodus path is dropped);
  - the site cooldown is set at fire time (3 years on discovery; the on_action's years);
  - 0104 fires once, on the crossing to 0;
  - the yearly pulse is live (yearly_playable_pulse).
The model is site-centric: one seeded site per simulated holder, which is the common case
at about 3% density (spec Q9). Everything not read from script is an assume().
"""
import os, sys, argparse
import numpy as np
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from pdx_read import Script, Ctx
import pdx_parse
from common import assume, MORTALITY, per_check_to_annual

V1 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), 'OLD PROJECT VERSION')
EVENTS = ('0002', '0003', '0004', '0010', '0011', '0020', '0021', '0030', '0031', '0040', '0041',
          '0101', '0102', '0103', '0104', '0105')
FAMILY_EVENT = {1: '0010', 2: '0020', 3: '0030', 4: '0040'}
GATE_P = assume('legacy_option_gate_open', 0.30, 'an education- or personality-gated option is open to the holder')
SKILL12 = assume('legacy_skill_12_share', 0.35, 'learning or stewardship >= 12 (each), read by the survey and its fallback')
POWERFUL = assume('legacy_has_powerful_vassal', 0.5, 'any_vassal = { is_powerful_vassal = yes } for 0102')
PLAYER_SURVEY_YEARS = assume('legacy_player_surveys_every', 5, 'a player surveys whenever the 5-year cooldown allows')
SURVEY_COOLDOWN = assume('legacy_survey_cooldown_years', 5, 'v2 decision cooldown = { years = 5 } (v1 flag, 5 years)')
DISCOVERY_CD = assume('legacy_discovery_site_cooldown', 3, 'v2: fire_discovery sets the 3-year site cooldown')


def _num(R, tok):
    try:
        return float(R.resolve(tok, Ctx()))
    except Exception:
        return 0.0


# ---------------------------------------------------------------- readers (v1 files)
def option_table(R, eid):
    ev = R.node('eotg_legacy.' + eid)
    out = []
    for o in [c for c in ev.children if c.key == 'option']:
        row = {'name': '', 'weight': 0.0, 'gate': 1.0, 'cond_gate': None, 'body': [c for c in o.children if c.key not in ('name', 'trigger', 'ai_chance')]}
        for c in o.children:
            if c.key == 'name':
                row['name'] = c.value
            elif c.key == 'ai_chance':
                b = [x for x in c.children if x.key == 'base']
                row['weight'] = float(b[0].value) if b else 0.0
            elif c.key == 'trigger':
                leaves = [(n.key, n.value) for n, _ in pdx_parse.walk(c.children) if not n.is_block]
                conds = [v for k, v in leaves if k == 'CONDITION']
                if conds:
                    row['cond_gate'] = int(float(conds[0]))
                rest = [k for k, v in leaves if k not in ('CONDITION',)]
                if any(k.startswith(('has_trait', 'eotg_st_edu', 'learning', 'stewardship')) for k in rest):
                    row['gate'] = GATE_P
        out.append(row)
    return out


def survey_fallback(R):
    """[(event, weight, [(add, cond)])] from the survey decision's fallback random_list."""
    out = []
    for n, _ in pdx_parse.walk(R.node('eotg_decision_survey_legacies').children):
        if n.key == 'random_list' and n.is_block:
            for c in n.children:
                ev = [x for x, _ in pdx_parse.walk(c.children) if x.key == 'id']
                mods = [(float([y for y in m.children if y.key == 'add'][0].value), [y for y in m.children if y.key != 'add'])
                        for m in c.children if m.key == 'modifier']
                out.append((ev[0].value.split('.')[-1] if ev else None, float(c.key), mods))
    return out


def pulse_numbers(R):
    on = R.node('eotg_on_yearly_legacy_pulse')
    decay = None; chances = []
    for n, _ in pdx_parse.walk(on.children):
        if n.key == 'eotg_se_legacy_add_attention' and n.is_block and decay is None:
            decay = _num(R, [x for x in n.children if x.key == 'AMOUNT'][0].value)
        if n.key == 'random' and n.is_block:
            ch = float([x for x in n.children if x.key == 'chance'][0].value)
            ev = [x.value.split('.')[-1] for x, _ in pdx_parse.walk(n.children) if x.key == 'id']
            cd = [float([y for y in x.children if y.key == 'YEARS'][0].value) for x, _ in pdx_parse.walk(n.children)
                  if x.key == 'eotg_se_legacy_cooldown' and x.is_block]
            flag = [float({y.key: y.value for y in x.children if not y.is_block}.get('years', 0)) for x, _ in pdx_parse.walk(n.children)
                    if x.key == 'add_character_flag' and x.is_block]
            chances.append({'event': ev[0] if ev else None, 'chance': ch, 'site_cd': cd[0] if cd else 0.0,
                            'flag_years': flag[0] if flag else 0.0})
    return {'decay': decay, 'aftermath': [c for c in chances if c['event'] in ('0101', '0102', '0103')]}


def seed_numbers(R):
    seed = R.node('eotg_se_legacy_seed')
    integ = [float(c.value) for c in seed.children if c.key == 'set_variable' and False]
    for c in seed.children:
        if c.key == 'set_variable' and c.is_block:
            kv = {x.key: x.value for x in c.children if not x.is_block}
            if kv.get('name') == 'eotg_legacy_integrity':
                integ = float(kv['value'])
    rl = [n for n, _ in pdx_parse.walk(R.node('eotg_se_legacy_seed_random').children) if n.key == 'random_list'][0]
    fam = [(float(c.key), int(float([x for x, _ in pdx_parse.walk(c.children) if x.key == 'FAMILY'][0].value))) for c in rl.children]
    return {'start_integrity': integ, 'families': fam}


# ---------------------------------------------------------------- one site
class Site:
    __slots__ = ('family', 'known', 'cond', 'integ', 'att', 'cd', 'zeroed', 'zero_year', 'disc_year', 'aftermath', 'events')


def apply_body(R, nodes, s, rng, year, queue, log):
    """Interpret an option body against one site (v2 rules): writers clamp, 0104 on the
    crossing, cooldown writes ignored (v2 moves them to firing points)."""
    for n in nodes:
        k = n.key or ''
        if k == 'random_list' and n.is_block:
            ws = np.array([float(c.key) for c in n.children]); c = n.children[rng.choice(len(ws), p=ws / ws.sum())]
            apply_body(R, c.children, s, rng, year, queue, log)
        elif k == 'if' and n.is_block:
            lim = [c for c in n.children if c.key == 'limit']
            ok = True
            if lim:
                conds = [x.value for x, _ in pdx_parse.walk(lim[0].children) if x.key == 'CONDITION']
                if conds:
                    ok = s.cond == int(float(conds[0]))
            if ok:
                apply_body(R, [c for c in n.children if c.key != 'limit'], s, rng, year, queue, log)
        elif k in ('else', 'else_if'):
            continue
        elif k.startswith('scope:') and n.is_block:
            apply_body(R, n.children, s, rng, year, queue, log)
        elif k == 'eotg_se_legacy_add_attention' and n.is_block:
            s.att = min(100.0, max(0.0, s.att + _num(R, [x for x in n.children if x.key == 'AMOUNT'][0].value)))
        elif k == 'eotg_se_legacy_add_integrity' and n.is_block:
            change_integrity(s, _num(R, [x for x in n.children if x.key == 'AMOUNT'][0].value), year, queue)
        elif k == 'set_variable' and n.is_block:
            kv = {x.key: x.value for x in n.children if not x.is_block}
            if kv.get('name') == 'eotg_legacy_integrity':   # 0104's direct sets: through the writer in v2
                change_integrity(s, float(kv['value']) - s.integ, year, queue)
        elif k == 'eotg_se_legacy_set_condition' and n.is_block:
            s.cond = int(float([x for x in n.children if x.key == 'CONDITION'][0].value))
        elif k in ('eotg_se_legacy_fire_discovery', 'eotg_se_legacy_make_known') and n.value == 'yes':
            if not s.known:
                s.known = True; s.disc_year = year
                if s.cond == 1:
                    s.cond = 2
                if k == 'eotg_se_legacy_fire_discovery':
                    s.cd = DISCOVERY_CD
                    queue.append(FAMILY_EVENT[s.family])
        elif k == 'trigger_event' and n.is_block:
            ids = [x.value for x in n.children if x.key == 'id']
            if ids:
                queue.append(ids[0].split('.')[-1])
        elif n.is_block and k not in ('limit', 'trigger', 'ai_chance', 'modifier', 'stress_impact', 'else', 'else_if'):
            apply_body(R, n.children, s, rng, year, queue, log)   # hidden_effect and other wrappers


def change_integrity(s, amt, year, queue):
    before = s.integ
    s.integ = min(100.0, max(0.0, s.integ + amt))
    if before > 0 and s.integ <= 0:      # v2 MED-2: the crossing only
        s.cond = 6
        s.zeroed += 1
        if s.zero_year is None:
            s.zero_year = year
        queue.append('0104')


def choose(rng, opts, s):
    w = []
    for o in opts:
        open_ = o['cond_gate'] is None or o['cond_gate'] == s.cond
        w.append(o['weight'] * (1.0 if not open_ else (1.0 if rng.random() < o['gate'] else 0.0)) * (1.0 if open_ else 0.0))
    w = np.array(w, float)
    if w.sum() <= 0:
        cand = [i for i, o in enumerate(opts) if o['cond_gate'] is None or o['cond_gate'] == s.cond]
        return opts[cand[-1]] if cand else None
    return opts[rng.choice(len(opts), p=w / w.sum())]


def fire(R, eid, s, rng, year, tables):
    queue = [eid]
    guard = 0
    while queue and guard < 10:
        e = queue.pop(0); guard += 1
        s.events[e] = s.events.get(e, 0) + 1
        o = choose(rng, tables[e], s)
        if o is not None:
            apply_body(R, o['body'], s, rng, year, queue, None)


def run(R, n_sites, years, seed, is_ai, overrides=None):
    rng = np.random.default_rng(seed)
    ov = overrides or {}
    tables = {e: option_table(R, e) for e in EVENTS}
    pn = pulse_numbers(R); sn = seed_numbers(R)
    D = R.decision('eotg_decision_survey_legacies')
    p_ai = float(per_check_to_annual(np.mean([R.ai_will_do(D, Ctx({'stewardship': st, 'learning': le, 'trait:curious': False, 'trait:content': False}))
                                              for st in (8, 14) for le in (8, 14)]), D['interval']['all']))
    p_ai = ov.get('survey_ai_annual', p_ai)
    fam_w = np.array([w for w, f in sn['families']]); fams = [f for w, f in sn['families']]
    decay = ov.get('decay', pn['decay'])
    sites = []
    for i in range(n_sites):
        s = Site(); s.family = fams[rng.choice(len(fams), p=fam_w / fam_w.sum())]
        s.known = False; s.cond = 1; s.integ = sn['start_integrity']; s.att = 0.0; s.cd = 0.0
        s.zeroed = 0; s.zero_year = None; s.disc_year = None; s.aftermath = 0; s.events = {}
        sites.append(s)
    att_hist = np.full((n_sites, years), np.nan); cond_end = np.zeros(n_sites, int)
    flag = np.zeros(n_sites); survey_cd = rng.integers(0, SURVEY_COOLDOWN, n_sites).astype(float)
    for y in range(years):
        for i, s in enumerate(sites):
            s.cd -= 1; flag[i] -= 1; survey_cd[i] -= 1
            # holder death: the heir gains the county (on_title_gain -> 0105 if known and ready)
            if rng.random() < MORTALITY:
                survey_cd[i] = 0
                same_dynasty = rng.random() < ov.get('heir_same_dynasty_share', 0.0)   # what-if: 0105 skips inheritance
                if s.known and s.cd <= 0 and not same_dynasty:
                    s.cd = 3.0
                    fire(R, '0105', s, rng, y, tables)
            # survey (the only discovery path in v2)
            if not s.known and survey_cd[i] <= 0:
                take = (rng.random() < p_ai) if is_ai else True
                if take:
                    survey_cd[i] = SURVEY_COOLDOWN
                    s.known = True; s.disc_year = y; s.cond = 2; s.cd = DISCOVERY_CD
                    fire(R, FAMILY_EVENT[s.family], s, rng, y, tables)
            if s.known:
                floor = ov.get('decay_floor', 0.0)    # what-if: decay stops at this attention
                if s.att > floor:
                    s.att = max(floor, s.att + decay)
                if flag[i] <= 0:
                    a = {c['event']: c for c in pn['aftermath']}
                    ready = s.cd <= 0
                    if ready and s.att >= ov.get('gate_0101', 50):
                        c = a['0101']
                        if rng.random() < ov.get('chance_0101', c['chance']) / 100:
                            flag[i] = c['flag_years']; s.cd = c['site_cd']; s.aftermath += 1
                            fire(R, '0101', s, rng, y, tables)
                    elif ready and s.cond == 4 and rng.random() < POWERFUL:
                        c = a['0102']
                        if rng.random() < c['chance'] / 100:
                            flag[i] = c['flag_years']; s.cd = c['site_cd']; s.aftermath += 1
                            fire(R, '0102', s, rng, y, tables)
                    elif ready and s.integ <= 50 and s.cond in (3, 5):
                        c = a['0103']
                        if rng.random() < c['chance'] / 100:
                            flag[i] = c['flag_years']; s.cd = c['site_cd']; s.aftermath += 1
                            fire(R, '0103', s, rng, y, tables)
                # what-if: passive drain on Extracted sites (spec Q8)
                if s.cond == 4 and ov.get('extracted_drain'):
                    change_integrity(s, ov['extracted_drain'], y, [])
                att_hist[i, y] = s.att
        if y == years - 1:
            for i, s in enumerate(sites):
                cond_end[i] = s.cond if s.known else 1
    disc = np.array([s.disc_year if s.disc_year is not None else np.nan for s in sites])
    zero = np.array([(s.zero_year - s.disc_year) if (s.zero_year is not None and s.disc_year is not None) else np.nan for s in sites])
    known_att = att_hist[:, -20:]
    out = {
        'discovered_by': {t: float(np.mean(disc < t)) for t in (10, 25, 50, 100) if t <= years},
        'years_to_discovery_median': float(np.nanmedian(disc)) if np.any(~np.isnan(disc)) else None,
        'condition_at_end': {c: float(np.mean(cond_end == c)) for c in range(1, 7)},
        'reached_integrity_0': float(np.mean(~np.isnan(zero))),
        'years_discovery_to_0_median': float(np.nanmedian(zero)) if np.any(~np.isnan(zero)) else None,
        'attention_known_last20_median': float(np.nanmedian(known_att)) if np.any(~np.isnan(known_att)) else None,
        'attention_known_last20_share_ge50': float(np.nanmean(known_att >= 50)) if np.any(~np.isnan(known_att)) else None,
        'aftermath_per_site_century': float(np.mean([s.aftermath for s in sites]) * 100 / years),
        'zero_crossings_per_site': float(np.mean([s.zeroed for s in sites])),
        'events_per_site_century': {e: float(np.mean([s.events.get(e, 0) for s in sites]) * 100 / years) for e in EVENTS},
        'survey_ai_annual': p_ai, 'decay': decay, 'start_integrity': sn['start_integrity'],
    }
    return out


def survey_seed_yield(R):
    """Expected new sites per survey that finds no hidden site: the fallback weights times
    each event's seeding options, read from the script (option weights, all gates open)."""
    fb = survey_fallback(R)
    total = sum(w for e, w, m in fb)
    out = {}
    for e, w, mods in fb:
        opts = option_table(R, e)
        seeds = 0.0; wsum = sum(o['weight'] for o in opts) or 1.0
        for o in opts:
            txt = [x.key for x, _ in pdx_parse.walk(o['body'])]
            p_seed = 0.0
            for x, _ in pdx_parse.walk(o['body']):
                if x.key == 'random_list' and x.is_block:
                    ws = [float(c.key) for c in x.children]
                    hit = [float(c.key) for c in x.children if any(y.key in ('eotg_se_legacy_seed', 'eotg_se_legacy_seed_random') for y, _ in pdx_parse.walk(c.children))]
                    p_seed = sum(hit) / sum(ws)
                    break
            else:
                p_seed = 1.0 if any(k in ('eotg_se_legacy_seed', 'eotg_se_legacy_seed_random') for k in txt) else 0.0
            seeds += o['weight'] / wsum * p_seed
        out[e] = {'weight_share': w / total, 'p_new_site': seeds}
    return {'per_event': out, 'p_new_site_per_empty_survey': sum(v['weight_share'] * v['p_new_site'] for v in out.values())}


def report(res):
    pct = lambda x: f'{100 * x:.1f}%'
    L = ['| Scenario | Discovered by 10 / 25 / 50 y | Median years to discovery | Integrity reached 0 | Years discovery → 0 (median) | Attention, known sites (median; share ≥ 50) | Aftermath events / site-century |',
         '|---|---|---|---|---|---|---|']
    for k, r in res['runs'].items():
        d = r['discovered_by']
        L.append(f"| {k} | {pct(d[10])} / {pct(d[25])} / {pct(d[50])} | {r['years_to_discovery_median']} | {pct(r['reached_integrity_0'])} | "
                 f"{r['years_discovery_to_0_median']} | {r['attention_known_last20_median']:.1f}; {pct(r['attention_known_last20_share_ge50'])} | {r['aftermath_per_site_century']:.2f} |")
    L += ['', '| Scenario | Dormant | Exposed | Governed | Extracted | Sealed | Unstable |', '|---|---|---|---|---|---|---|']
    for k, r in res['runs'].items():
        c = r['condition_at_end']
        L.append(f"| {k} | " + ' | '.join(pct(c[i]) for i in range(1, 7)) + ' |')
    sy = res['survey_yield']
    L += ['', '**Events per site-century** (AI holder, v2 design): ' + ', '.join(f"{e} {v:.2f}" for e, v in res['runs']['AI holder (v2 design)']['events_per_site_century'].items() if v > 0) + '.']
    L += ['', f"**Survey uptake:** an AI ruler surveys with probability {res['survey_ai_annual']:.3f} a year (read from `ai_will_do` and `ai_check_interval`); a player every {PLAYER_SURVEY_YEARS} years (ASSUMPTION)."]
    L += ['', f"**Dynamic seeding:** a survey that finds no hidden site creates a new site with probability {sy['p_new_site_per_empty_survey']:.2f} "
          f"({', '.join(f'{e}: weight {100 * v['weight_share']:.0f}%, seeds {v['p_new_site']:.2f}' for e, v in sy['per_event'].items())})."]
    dens = res['density']
    L += ['', '**Seeding density (Q9):** sites per 100 counties at game start, and discovered sites per 100 counties after 25 / 50 years (AI holders):', '',
          '| Seed chance | Sites / 100 counties | Discovered by 25 y | by 50 y |', '|---|---|---|---|']
    for row in dens:
        L.append(f"| {row['chance']}% | {row['chance']:.1f} | {row['disc25']:.2f} | {row['disc50']:.2f} |")
    return '\n'.join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sites', type=int, default=20000)
    ap.add_argument('--years', type=int, default=100)
    ap.add_argument('--seed', type=int, default=20261103)
    ap.add_argument('--md')
    ap.add_argument('--json')
    a = ap.parse_args()
    R = Script(repo=V1)
    res = {'runs': {}}
    res['runs']['AI holder (v2 design)'] = run(R, a.sites, a.years, a.seed, True)
    res['runs']['player holder (v2 design)'] = run(R, a.sites, a.years, a.seed, False)
    res['runs']['AI, Q8 extracted drain -2/yr'] = run(R, a.sites, a.years, a.seed, True, {'extracted_drain': -2})
    res['runs']['AI, attention decay -1/yr'] = run(R, a.sites, a.years, a.seed, True, {'decay': -1})
    res['runs']['AI, Q8 extracted drain -1/yr'] = run(R, a.sites, a.years, a.seed, True, {'extracted_drain': -1})
    res['runs']['AI, 0101 gate at attention 25'] = run(R, a.sites, a.years, a.seed, True, {'gate_0101': 25})
    res['runs']['AI, 0105 only outside the dynasty (90% of deaths are inheritance)'] = run(R, a.sites, a.years, a.seed, True, {'heir_same_dynasty_share': 0.9})
    res['runs']['AI, decay stops at 25 (Rumoured floor)'] = run(R, a.sites, a.years, a.seed, True, {'decay_floor': 25})
    res['runs']['AI, 0101 gate 25 + attention floor 25'] = run(R, a.sites, a.years, a.seed, True, {'gate_0101': 25, 'decay_floor': 25})
    res['runs']['AI, recommended package (0105 outside dynasty, drain -1, gate 25, floor 25)'] = run(
        R, a.sites, a.years, a.seed, True, {'heir_same_dynasty_share': 0.9, 'extracted_drain': -1, 'decay_floor': 25, 'gate_0101': 25})
    res['survey_yield'] = survey_seed_yield(R)
    res['survey_ai_annual'] = res['runs']['AI holder (v2 design)']['survey_ai_annual']
    ai = res['runs']['AI holder (v2 design)']['discovered_by']
    res['density'] = [{'chance': c, 'disc25': c * ai[25], 'disc50': c * ai[50]} for c in (1, 3, 5)]
    md = report(res)
    if a.md:
        open(a.md, 'w', encoding='utf-8').write(md + '\n')
    print(md)
    import json
    if a.json:
        json.dump(res, open(a.json, 'w', encoding='utf-8'), indent=1, default=float)


if __name__ == '__main__':
    main()
