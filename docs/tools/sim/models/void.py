"""Void Corruption: exposure (eotg_void_exposure) and Hollowing depth, yearly steps.

Reads, through pdx_read (nothing below restates a script number):
  - yearly accrual and relief: eotg_void_yearly_accrual_value
    (common/script_values/eotg_void_values.txt:11-43; the Voidwalker -6 at :35);
  - Hollowing depth start and drift: eotg_void_hollowing_start_value / _drift_value
    (eotg_void_values.txt:46-53);
  - the contact chance with its is_ai branch: eotg_void_contact_chance_value
    (eotg_void_values.txt:60-66; 4 player / 1 AI as merged);
  - the stage gates: eotg_void_susceptible, _whisper_stage, _bargain_ready, _saturated,
    _hollowing_ready (common/scripted_triggers/eotg_void_triggers.txt), evaluated as
    written;
  - the band thresholds: the var comparisons inside eotg_void_refresh_band_effect and
    eotg_void_refresh_depth_band_effect (common/scripted_effects/eotg_void_effects.txt);
  - the yearly pulse: every event slot in eotg_on_yearly_void_check
    (common/on_action/eotg_void_on_actions.txt:33-190): its random chance or
    random_list weight (and sibling total), and the cooldown years it sets (the
    once-a-year, one-roll-per-pulse rule and the cooldown authority live there);
  - every option of the 15 events (events/eotg_void_*.txt): ai_chance base, the
    exposure and depth AMOUNTs, wards, and the stage effects (become touched /
    defiant / hollowed, seat the Voidwalker, step down), walking the eotg_void_*
    scripted effects inline.
The model mirrors the on_action's control flow (accrual, forced Hollowing, one roll
by stage, then the Voidwalker roll only if nothing fired) in Python; the flow is
cited line by line in step().
"""
import numpy as np
import pdx_parse
from pdx_read import Ctx
from common import assume, MORTALITY

EVENTS = ('0001', '0002', '0003', '0004', '0010', '0011', '0020', '0021', '0022', '0023', '0024', '0025',
          '0030', '0031', '0032')
GATE_P = assume('void_option_gate_open', 0.35,
                'an option with a trigger (education, personality, age, heir) is open to a given ruler; '
                'cult-gated options are closed (eotg_void_is_cult_faith is always = no)')
EDU_LEARNING = assume('void_education_learning_share', 0.2, 'one of five educations')
MAD = assume('void_lunatic_or_possessed_share', 0.02, 'lunatic_1/_genetic or possessed_1/_genetic')
PIOUS = assume('void_piety_level_3_share', 0.15, 'piety_level >= 3')
STRESSED = assume('void_stress_200_share', 0.05, 'stress >= 200 in a given year')
START_AGE = assume('void_ruler_start_age', (30, 10), 'a ruler takes the seat at N(30, 10)')
NEAR = assume('void_near_touched', False, 'no Void-Touched courtier, vassal or spouse (a lone realm)')
STAGE_C_OPEN = assume('void_stage_c_slot_open', {'0020': 0.23, '0021': 0.5, '0022': 0.6, '0024': None, '0025': 0.3},
                      'P(the slot trigger holds): at war ~23%, a child under 12, a zealous courtier, a vassal below -20; 0024 reads age')


# ---------------------------------------------------------------- script readers
def _event_node(R, eid):
    return R.node('eotg_void.' + eid)


def _walk(R, nodes, depth=0, skip_scopes=True):
    """pdx_parse.walk with eotg_void_* scripted effects inlined; nodes under another
    character's scope (scope:, primary_heir, every_/random_) are skipped."""
    for n in nodes:
        k = n.key or ''
        if skip_scopes and n.is_block and (k.startswith('scope:') or k in ('primary_heir', 'liege') or
                                           k.startswith('every_') or k.startswith('random_') and k != 'random_list'):
            continue
        yield n
        if n.is_block:
            yield from _walk(R, n.children, depth, skip_scopes)
        elif n.value == 'yes' and k.startswith('eotg_void_') and k in R.defs and \
                R.defs[k][0].startswith('common/scripted_effects/') and depth < 4:
            yield from _walk(R, R.defs[k][1].children, depth + 1, skip_scopes)


def option_table(R, eid):
    """[{name, weight, gate, d_exp, d_depth, ward, touched, defiant, shelter, step_down}]"""
    ev = _event_node(R, eid)
    out = []
    for o in [c for c in ev.children if c.key == 'option']:
        row = {'name': '', 'weight': 0.0, 'gate': 1.0, 'd_exp': 0.0, 'd_depth': 0.0, 'ward': 0.0,
               'touched': False, 'defiant': False, 'shelter': False, 'step_down': False, 'seed': False}
        for c in o.children:
            if c.key == 'name':
                row['name'] = c.value
            elif c.key == 'ai_chance':
                b = [x for x in c.children if x.key == 'base']
                row['weight'] = float(b[0].value) if b else 0.0
            elif c.key == 'trigger':
                txt = ' '.join(f'{n.key}={n.value}' for n, _ in pdx_parse.walk(c.children) if not n.is_block)
                if 'eotg_void_is_cult_faith=yes' in txt:
                    row['gate'] = 0.0
                elif txt.strip() == 'eotg_void_is_cult_faith=no':
                    row['gate'] = 1.0
                else:
                    row['gate'] = GATE_P
        for n in _walk(R, [c for c in o.children if c.key not in ('trigger', 'ai_chance', 'name')]):
            k = n.key or ''
            if k in ('eotg_void_change_exposure_effect', 'eotg_void_change_hollowing_depth_effect') and n.is_block:
                a = [x for x in n.children if x.key == 'AMOUNT'][0].value
                try:
                    v = float(R.resolve(a, Ctx()))
                except Exception:
                    v = 0.0
                row['d_exp' if 'exposure' in k else 'd_depth'] += v
            elif k == 'eotg_void_add_ward_effect' and n.is_block:
                row['ward'] = max(row['ward'], float([x for x in n.children if x.key == 'YEARS'][0].value))
            elif k == 'add_character_modifier' and n.is_block:
                kv = {x.key: x.value for x in n.children if not x.is_block}
                if kv.get('modifier') == 'eotg_mod_void_warded' and 'years' in kv:
                    row['ward'] = max(row['ward'], float(kv['years']))
            elif not n.is_block and n.value == 'yes':
                row['touched'] |= k == 'eotg_void_become_touched_effect'
                row['defiant'] |= k == 'eotg_void_become_defiant_effect'
                row['shelter'] |= k == 'eotg_void_shelter_voidwalker_effect'
                row['step_down'] |= k == 'eotg_void_step_down_effect'
                row['seed'] |= k == 'eotg_void_seed_effect'
        out.append(row)
    return out


def immediate_effects(R, eid):
    ev = _event_node(R, eid)
    imm = [c for c in ev.children if c.key == 'immediate']
    keys = {n.key for n in _walk(R, imm[0].children)} if imm else set()
    return {'touched': 'eotg_void_become_touched_effect' in keys, 'hollowed': 'eotg_void_become_hollowed_effect' in keys}


def pulse_slots(R):
    """{event: {'chance': token or None, 'weight': w or None, 'total': sibling total, 'cooldown': years, 'line'}}"""
    on = R.node('eotg_on_yearly_void_check')
    slots = {}

    def ev_of(block):
        for c in block.children:
            if c.key == 'trigger_event' and c.is_block:
                for x in c.children:
                    if x.key == 'id':
                        return x.value.split('.')[-1]
        return None

    def cd_of(block):
        for c in block.children:
            if c.key == 'add_character_flag' and c.is_block:
                kv = {x.key: x.value for x in c.children if not x.is_block}
                if kv.get('flag') == 'eotg_flag_void_event_cooldown':
                    return float(kv['years'])
        return 0.0

    for n, _ in pdx_parse.walk(on.children):
        if n.key == 'random' and n.is_block:
            e = ev_of(n)
            if e:
                ch = [x for x in n.children if x.key == 'chance'][0].value
                slots[e] = {'chance': ch, 'weight': None, 'total': None, 'cooldown': cd_of(n), 'line': n.line}
        elif n.key == 'random_list' and n.is_block:
            total = sum(float(c.key) for c in n.children)
            for c in n.children:
                e = ev_of(c)
                if e:
                    mods = [(float([x for x in m.children if x.key == 'add'][0].value), m) for m in c.children if m.key == 'modifier']
                    slots[e] = {'chance': None, 'weight': float(c.key), 'total': total, 'mods': mods,
                                'cooldown': cd_of(c), 'line': c.line}
        elif n.key == 'if' and n.is_block:
            e = ev_of(n)
            if e:   # the forced Hollowing (no roll)
                slots[e] = {'chance': '100', 'weight': None, 'total': None, 'cooldown': cd_of(n), 'line': n.line}
    return slots


def accrual_terms(R):
    """{condition text: (add, limit nodes)} for each `if` in eotg_void_yearly_accrual_value
    (eotg_void_values.txt:11-43), keyed by the first trigger in its limit."""
    out = {}
    for c in R.node('eotg_void_yearly_accrual_value').children:
        if c.key == 'if':
            lim = [x for x in c.children if x.key == 'limit'][0]
            add = float([x for x in c.children if x.key == 'add'][0].value)
            first = lim.children[0]
            key = f"{first.key}={first.value}" if not first.is_block else first.key
            out[key] = (add, lim.children)
    return out


def accrual(R, c, n):
    """The script's accrual, plus what-if term overrides: R.overrides['void.term.<key>'] =
    new add for that term (e.g. 'void.term.has_trait=eotg_void_touched')."""
    acc = np.asarray(R.num('eotg_void_yearly_accrual_value', c), float) * np.ones(n)
    for k, (add, lim) in accrual_terms(R).items():
        ok = 'void.term.' + k
        if ok in R.overrides:
            acc = acc + (R.overrides[ok] - add) * (np.asarray(R.eval_trigger(lim, c), bool) * np.ones(n, bool))
    return acc


def voidwalker_gate(R):
    """The limit of the `if` that rolls 0004 (eotg_void_on_actions.txt:175-182)."""
    for n, _ in pdx_parse.walk(R.node('eotg_on_yearly_void_check').children):
        if n.key == 'if' and n.is_block and any(c.key == 'random' and any(
                x.key == 'trigger_event' and any(y.value.endswith('0004') for y in x.children if y.key == 'id')
                for x in c.children) for c in n.children):
            return [c for c in n.children if c.key == 'limit'][0].children
    raise KeyError('0004 gate')


def band_thresholds(R, effect, var):
    vals = set()
    for n, _ in pdx_parse.walk(R.node(effect).children):
        if n.key == 'var:' + var and not n.is_block:
            vals.add(float(n.value))
    return sorted(vals)


# ---------------------------------------------------------------- the model
class Void:
    def __init__(self, R, runs, seed, is_ai, contact_override=None, voidwalker='script'):
        self.R, self.runs, self.is_ai = R, runs, is_ai
        self.rng = np.random.default_rng(seed)
        self.slots = pulse_slots(R)
        self.opts = {e: option_table(R, e) for e in EVENTS}
        self.imm = {e: immediate_effects(R, e) for e in EVENTS}
        self.start = float(R.num('eotg_void_hollowing_start_value'))
        self.drift = float(R.num('eotg_void_hollowing_drift_value'))
        self.contact = contact_override if contact_override is not None else \
            float(R.num('eotg_void_contact_chance_value', Ctx({'is_ai': 1.0 if is_ai else 0.0})))
        self.voidwalker_mode = voidwalker   # 'script' (0004 only), 'never', 'at_contact' (seated when seeded)
        n = runs
        self.exp = np.zeros(n); self.has_exp = np.zeros(n, bool)
        self.seeded = np.zeros(n, bool); self.touched = np.zeros(n, bool); self.defiant = np.zeros(n, bool)
        self.hollow = np.zeros(n, bool); self.depth = np.zeros(n)
        self.ward = np.zeros(n); self.cd = np.zeros(n); self.vw = np.zeros(n, bool)
        self.new_ruler(np.ones(n, bool))
        self.t_seed = np.full(n, np.nan); self.t_touch = np.full(n, np.nan); self.t_hollow = np.full(n, np.nan)
        self.ever_touched = np.zeros(n, bool); self.ever_hollow = np.zeros(n, bool); self.ever_seeded = np.zeros(n, bool)
        self.vw_created = 0; self.fired = {e: 0 for e in EVENTS}; self.rulers = n; self.step_downs = 0

    def new_ruler(self, m, heir_seeded=None):
        r = self.rng
        self.age = np.where(m, r.normal(*START_AGE, self.runs).clip(16, 70), getattr(self, 'age', np.zeros(self.runs)))
        self.learn = np.where(m, r.random(self.runs) < EDU_LEARNING, getattr(self, 'learn', np.zeros(self.runs, bool)))
        self.mad = np.where(m, r.random(self.runs) < MAD, getattr(self, 'mad', np.zeros(self.runs, bool)))
        self.pious = np.where(m, r.random(self.runs) < PIOUS, getattr(self, 'pious', np.zeros(self.runs, bool)))
        for a in ('exp', 'depth', 'ward'):
            setattr(self, a, np.where(m, 0.0, getattr(self, a)))
        for a in ('has_exp', 'seeded', 'touched', 'defiant', 'hollow'):
            setattr(self, a, np.where(m, False, getattr(self, a)))
        self.cd = np.where(m, 0.0, self.cd)
        if heir_seeded is not None:
            self.seeded |= m & heir_seeded
            self.has_exp |= m & heir_seeded

    def ctx(self, extra=None):
        v = {'var:eotg_void_exposure': self.exp, 'has_variable:eotg_void_exposure': self.has_exp,
             'var:eotg_void_hollowing_depth': self.depth,
             'trait:eotg_void_touched': self.touched, 'trait:eotg_void_defiant': self.defiant,
             'trait:eotg_void_hollowed': self.hollow, 'trait:eotg_grip_survivor': False,
             'trait:education_learning': self.learn, 'trait:lunatic_1': self.mad,
             'has_character_flag:eotg_flag_void_seeded': self.seeded,
             'has_character_flag:eotg_flag_void_event_cooldown': self.cd > 0,
             'has_character_modifier:eotg_mod_void_warded': self.ward > 0,
             'trig:eotg_void_has_voidwalker': self.vw, 'trig:eotg_void_near_touched': NEAR,
             'is_landed': 1.0, 'is_ai': 1.0 if self.is_ai else 0.0, 'age': self.age,
             'stress': np.where(self.rng.random(self.runs) < STRESSED, 250.0, 50.0),
             'piety_level': np.where(self.pious, 3.0, 1.0)}
        v.update(extra or {})
        return Ctx(v)

    def trig(self, name, c):
        R = self.R
        return np.asarray(R.eval_trigger(R.node(name).children, c), bool) * np.ones(self.runs, bool)

    def change_exp(self, amt, m):
        amt = np.asarray(amt, float) * np.ones(self.runs)
        self.has_exp |= m
        self.exp = np.where(m, np.clip(self.exp + amt, 0, 100), self.exp)

    def fire(self, eid, m, year):
        if not m.any():
            return
        self.fired[eid] += int(m.sum())
        imm = self.imm[eid]
        if imm['touched']:
            self.become_touched(m, year)
        if imm['hollowed']:
            self.change_exp(100, m)
            self.touched &= ~m
            self.hollow |= m
            self.depth = np.where(m, self.start, self.depth)
            self.ever_hollow |= m
            self.t_hollow = np.where(m & np.isnan(self.t_hollow), year, self.t_hollow)
        if eid == '0004':
            self.vw_created += int(m.sum())   # 0004's immediate creates a Voidwalker every time it fires
        opts = self.opts[eid]
        w = np.array([o['weight'] for o in opts])
        g = np.array([o['gate'] for o in opts])
        avail = self.rng.random((self.runs, len(opts))) < g
        if not avail.any():
            return
        wt = avail * w
        wt[:, -1] = np.where(wt.sum(axis=1) == 0, 1.0, wt[:, -1])   # the last, ungated option is the fallback
        cum = np.cumsum(wt, axis=1)
        pick = (cum < self.rng.random((self.runs, 1)) * cum[:, -1:]).sum(axis=1)
        for i, o in enumerate(opts):
            mi = m & (pick == i)
            if not mi.any():
                continue
            if o['seed']:
                self.seeded |= mi; self.ever_seeded |= mi
                self.t_seed = np.where(mi & np.isnan(self.t_seed), year, self.t_seed)
                self.change_exp(0, mi)
            if o['touched']:
                self.become_touched(mi, year)
            if o['defiant']:
                self.defiant |= mi
            if o['d_exp']:
                self.change_exp(o['d_exp'], mi)
            if o['d_depth']:
                self.depth = np.where(mi & self.hollow, np.clip(self.depth + o['d_depth'], 0, 100), self.depth)
            if o['ward']:
                self.ward = np.where(mi, o['ward'], self.ward)
            if o['shelter'] and self.voidwalker_mode == 'script':
                self.vw |= mi
            if o['step_down']:
                self.step_downs += int(mi.sum())
                self.new_ruler(mi)
                self.rulers += int(mi.sum())

    def become_touched(self, m, year):
        self.defiant &= ~m
        self.touched |= m
        self.ward = np.where(m, 0.0, self.ward)
        self.ever_touched |= m
        self.t_touch = np.where(m & np.isnan(self.t_touch), year, self.t_touch)

    def cd_ready_gate(self, c):
        """0004's limit as written (event ready, exposure >= 20, no Voidwalker, not Hollowed)."""
        return np.asarray(self.R.eval_trigger(voidwalker_gate(self.R), c), bool) * np.ones(self.runs, bool)

    def roll(self, eid, m, c):
        s = self.slots[eid]
        p = float(np.mean(self.R.resolve(s['chance'], c))) / 100.0 if eid != '0001' else self.contact / 100.0
        p = self.R.overrides.get(f'void.slot.{eid}.chance', p * 100) / 100.0   # what-if hook
        hit = m & (self.rng.random(self.runs) < p)
        self.cd = np.where(hit, s['cooldown'], self.cd)
        return hit

    def roll_list(self, eids, m, c, open_p=None):
        """One random_list: each entry's weight (plus modifiers) counts only where its
        trigger holds; the empty entry keeps its weight."""
        total = self.slots[eids[0]]['total']
        ws = []
        for e in eids:
            s = self.slots[e]
            w = np.full(self.runs, s['weight'])
            for add, mod in s.get('mods', []):
                cond = [x for x in mod.children if x.key != 'add']
                w = w + add * np.asarray(self.R.eval_trigger(cond, c), bool)
            if open_p and open_p.get(e) is not None:
                w = w * (self.rng.random(self.runs) < open_p[e])
            elif open_p and e in open_p and open_p[e] is None:   # 0024: age >= 60
                w = w * (self.age >= 60)
            ws.append(w)
        ws = np.array(ws).T
        empty = total - sum(self.slots[e]['weight'] for e in eids)
        full = np.concatenate([ws, np.full((self.runs, 1), empty)], axis=1)
        cum = np.cumsum(full, axis=1)
        pick = (cum < self.rng.random((self.runs, 1)) * cum[:, -1:]).sum(axis=1)
        hits = {}
        for i, e in enumerate(eids):
            h = m & (pick == i)
            self.cd = np.where(h, self.slots[e]['cooldown'], self.cd)
            hits[e] = h
        return hits

    def step(self, year):
        self.cd -= 1; self.ward -= 1; self.age += 1
        c = self.ctx()
        # 1. accrual for the susceptible (on_action :36-39), depth drift (:40-43)
        sus = self.trig('eotg_void_susceptible', c)
        acc = accrual(self.R, c, self.runs)
        self.change_exp(acc, sus)
        self.depth = np.where(self.hollow, np.clip(self.depth + self.drift, 0, 100), self.depth)
        c = self.ctx()
        # 2. the forced Hollowing (:46-50), cooldown set at fire time
        hr = self.trig('eotg_void_hollowing_ready', c)
        self.cd = np.where(hr, self.slots['0030']['cooldown'], self.cd)
        self.fire('0030', hr, year)
        c = self.ctx()
        # 3. one roll by stage (:53-172), only while the cooldown is clear
        ready = (self.cd <= 0)
        d = ready & self.hollow
        for e, h in self.roll_list(['0031', '0032'], d, c).items():
            self.fire(e, h, year)
        cst = ready & ~self.hollow & self.touched & ~self.trig('eotg_void_hollowing_ready', c)
        for e, h in self.roll_list(['0020', '0021', '0022', '0023', '0024', '0025'], cst, c, STAGE_C_OPEN).items():
            self.fire(e, h, year)
        rest = ready & ~self.hollow & ~self.touched
        sat = rest & self.trig('eotg_void_saturated', c)
        self.fire('0011', self.roll('0011', sat, c), year)
        bar = rest & ~sat & self.trig('eotg_void_bargain_ready', c)
        self.fire('0010', self.roll('0010', bar, c), year)
        wh = rest & ~sat & ~bar & self.trig('eotg_void_whisper_stage', c)
        for e, h in self.roll_list(['0002', '0003'], wh, c).items():
            self.fire(e, h, year)
        con = rest & ~sat & ~bar & ~wh & ~self.seeded
        self.fire('0001', self.roll('0001', con, c), year)
        # 4. the Voidwalker at the gate (:175-189): re-reads the cooldown
        if self.voidwalker_mode == 'script':
            c = self.ctx()
            vw = self.cd_ready_gate(c)
            self.fire('0004', self.roll('0004', vw, c), year)
        elif self.voidwalker_mode == 'at_contact':
            self.vw |= self.seeded
        # deaths: the ruler (a new, unseeded ruler takes the seat; the seated Voidwalker
        # stays at court); the Voidwalker courtier dies at the same rate
        dead = self.rng.random(self.runs) < MORTALITY
        self.rulers += int(dead.sum())
        self.new_ruler(dead)
        self.vw &= ~(self.rng.random(self.runs) < MORTALITY) | (self.voidwalker_mode == 'at_contact')


def run_all(R, runs, seed):
    """The H2b outputs: the contact-rate sweep (AI and player rates, plus the script's
    4/1 default), stage timings with and without a seated Voidwalker, 0004's yield."""
    out = {'contact_sweep': [], 'timings': {}, 'script_values': {}}
    out['script_values'] = {
        'contact_player': float(R.num('eotg_void_contact_chance_value', Ctx({'is_ai': 0.0}))),
        'contact_ai': float(R.num('eotg_void_contact_chance_value', Ctx({'is_ai': 1.0}))),
        'hollowing_start': float(R.num('eotg_void_hollowing_start_value')),
        'hollowing_drift': float(R.num('eotg_void_hollowing_drift_value')),
        'exposure_bands': band_thresholds(R, 'eotg_void_refresh_band_effect', 'eotg_void_exposure'),
        'depth_bands': band_thresholds(R, 'eotg_void_refresh_depth_band_effect', 'eotg_void_hollowing_depth'),
        'slots': {e: {k: (v if not isinstance(v, list) else len(v)) for k, v in s.items()} for e, s in pulse_slots(R).items()},
        'accrual_base_unseeded_ai': float(np.mean(R.num('eotg_void_yearly_accrual_value', Ctx({'trait:eotg_void_touched': False, 'trig:eotg_void_has_voidwalker': False, 'trig:eotg_void_near_touched': False, 'stress': 0.0, 'age': 30.0, 'piety_level': 1.0})))),
    }
    rates = [(None, 'script default')] + [(r, f'{r}%') for r in (0.5, 1.0, 2.0, 4.0)]
    for is_ai in (True, False):
        for rate, label in rates:
            m = Void(R, runs, seed, is_ai, contact_override=rate)
            snap = {}
            for y in range(1, 51):
                m.step(y)
                if y in (10, 25, 50):
                    snap[y] = {'touched_now': float(np.mean(m.touched | m.hollow)), 'hollow_now': float(np.mean(m.hollow)),
                               'ever_touched': float(np.mean(m.ever_touched)), 'ever_hollow': float(np.mean(m.ever_hollow)),
                               'ever_seeded': float(np.mean(m.ever_seeded))}
            out['contact_sweep'].append({'ruler': 'ai' if is_ai else 'player', 'rate': label,
                                         'contact_pct': m.contact, 'snap': snap,
                                         'voidwalkers_created_per_100_seat_years': 100 * m.vw_created / (runs * 50),
                                         'step_downs_per_1000_seats': 1000 * m.step_downs / runs,
                                         'fired_per_100_seat_years': {e: 100 * v / (runs * 50) for e, v in m.fired.items()}})
    # timings: from first contact, 100-year horizon, player rate; with/without a Voidwalker
    for mode in ('never', 'script', 'at_contact'):
        m = Void(R, runs, seed, False, voidwalker=mode)
        for y in range(1, 101):
            m.step(y)
        ct = m.t_touch - m.t_seed; th = m.t_hollow - m.t_touch
        def q(x):
            x = x[~np.isnan(x)]
            return [float(v) for v in np.percentile(x, [25, 50, 75])] if len(x) else None
        seeded = ~np.isnan(m.t_seed)
        out['timings'][mode] = {'seeded_share': float(seeded.mean()),
                                'touched_given_seeded': float(np.mean(~np.isnan(m.t_touch[seeded]))) if seeded.any() else None,
                                'hollow_given_touched': float(np.mean(~np.isnan(m.t_hollow[~np.isnan(m.t_touch)]))) if (~np.isnan(m.t_touch)).any() else None,
                                'years_contact_to_touched_q': q(ct), 'years_touched_to_hollow_q': q(th),
                                'voidwalkers_created_per_100_seat_years': 100 * m.vw_created / (runs * 100)}
    # proposals: before/after on a player seat at the script's rate, 100 years, 0004 as scripted
    out['proposals'] = []
    for pid, ov in (('V1', {'void.term.has_trait=eotg_void_touched': 2}),
                    ('V2', {'void.slot.0004.chance': 25}),
                    ('V3', {'void.term.eotg_void_has_voidwalker=yes': -4})):
        row = {'id': pid, 'override': ov}
        for label, o in (('before', {}), ('after', ov)):
            R.overrides = dict(o)
            m = Void(R, runs, seed, False)
            for y in range(1, 101):
                m.step(y)
            th = (m.t_hollow - m.t_touch); th = th[~np.isnan(th)]
            st = ~np.isnan(m.t_seed); tt = ~np.isnan(m.t_touch)
            row[label] = {'stage_c_per_100_seat_years': 100 * sum(m.fired[e] for e in ('0020', '0021', '0022', '0023', '0024', '0025')) / (runs * 100),
                          'touched_years_median': float(np.median(th)) if len(th) else None,
                          'ever_touched_100y': float(np.mean(m.ever_touched)),
                          'ever_hollow_100y': float(np.mean(m.ever_hollow)),
                          'touched_given_seeded': float(np.mean(tt[st])) if st.any() else None,
                          'voidwalkers_per_100_seat_years': 100 * m.vw_created / (runs * 100)}
        R.overrides = {}
        out['proposals'].append(row)
    return out


def tables(v):
    pct = lambda x: f'{100 * x:.1f}%'
    L = ['\n### Void Corruption (`models/void.py`; 50-year seats, contact sweep)\n',
         f"Script values read: contact {v['script_values']['contact_player']:g}% player / {v['script_values']['contact_ai']:g}% AI; "
         f"Hollowing start {v['script_values']['hollowing_start']:g}, drift +{v['script_values']['hollowing_drift']:g}/yr; "
         f"exposure bands {v['script_values']['exposure_bands']}; depth bands {v['script_values']['depth_bands']}.\n",
         '| Ruler | Contact rate | Seeded by 10 / 25 / 50 y | Ever Touched by 10 / 25 / 50 y | Touched or Hollowed now at 50 y | Ever Hollowed by 50 y | Voidwalkers created / 100 seat-years |',
         '|---|---|---|---|---|---|---|']
    for r in v['contact_sweep']:
        s = {int(k): v for k, v in r['snap'].items()}
        L.append(f"| {r['ruler']} | {r['rate']} ({r['contact_pct']:g}%) | {pct(s[10]['ever_seeded'])} / {pct(s[25]['ever_seeded'])} / {pct(s[50]['ever_seeded'])} | "
                 f"{pct(s[10]['ever_touched'])} / {pct(s[25]['ever_touched'])} / {pct(s[50]['ever_touched'])} | {pct(s[50]['touched_now'])} | "
                 f"{pct(s[50]['ever_hollow'])} | {r['voidwalkers_created_per_100_seat_years']:.2f} |")
    L += ['', '**Stage timings** (player rate, 100-year seats; quartiles in years):', '',
          '| Voidwalker | Seeded | Touched, given seeded | Hollowed, given Touched | Contact → Touched (25/50/75) | Touched → Hollowed (25/50/75) |',
          '|---|---|---|---|---|---|']
    names = {'never': 'never seated', 'script': 'as scripted (0004)', 'at_contact': 'seated at contact'}
    for k, t in v['timings'].items():
        L.append(f"| {names[k]} | {pct(t['seeded_share'])} | {pct(t['touched_given_seeded'] or 0)} | {pct(t['hollow_given_touched'] or 0)} | "
                 f"{t['years_contact_to_touched_q']} | {t['years_touched_to_hollow_q']} |")
    if v.get('proposals'):
        L += ['', '**Void proposals, before and after** (player seat, 4% contact, 100 years, 0004 as scripted):', '',
              '| Proposal | Override | Metric | Before | After |', '|---|---|---|---|---|']
        for p in v['proposals']:
            for m in ('stage_c_per_100_seat_years', 'touched_years_median', 'ever_touched_100y', 'ever_hollow_100y', 'touched_given_seeded', 'voidwalkers_per_100_seat_years'):
                b, a = p['before'][m], p['after'][m]
                if b is None or a is None:
                    continue
                L.append(f"| {p['id']} | `{p['override']}` | {m} | {b:.3f} | {a:.3f} |")
    return L


def chart(out, v):
    import os
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for r in v['contact_sweep']:
        sn = {int(k): v for k, v in r['snap'].items()}
        ys = [0] + [sn[y]['ever_touched'] for y in (10, 25, 50)]
        ls = '-' if r['ruler'] == 'ai' else '--'
        ax.plot([0, 10, 25, 50], ys, ls, marker='o', label=f"{r['ruler']} {r['rate']}")
    ax.set_xlabel('Years'); ax.set_ylabel('Share of seats ever Void-Touched')
    ax.set_title('Void: contact-rate sweep (AI solid, player dashed)')
    ax.legend(fontsize=7, ncol=2); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(out, 'chart_void.png'), dpi=110); plt.close(fig)
