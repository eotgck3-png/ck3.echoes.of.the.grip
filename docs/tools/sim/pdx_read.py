"""Script reader for the mechanics simulation (docs/tools/sim/README.md).

Reads the mod's own Paradox script (via docs/tools/pdx_parse.py) and evaluates the
pieces the models need, so no model hard-codes a number:

* script values (`common/script_values/`): constants and formulas, evaluated against a
  context whose entries may be numpy arrays (one entry per simulated ruler);
* scripted triggers and the trigger blocks inside values, decisions and modifiers;
* decisions: cost, cooldown, ai_check_interval_by_tier, ai_potential, ai_will_do;
* character/county modifiers (their lines and `scale`);
* story-cycle effect_group intervals;
* event random_list weights (base + modifiers);
* literal amounts passed to a change effect inside an on_action or effect block.

Anything the script reads from the ENGINE (vanilla named values such as
medium_gold_value, character stats, wars) is resolved through the context. Vanilla
named values that this cloud session cannot read come from VANILLA_DEFAULTS below;
each is an ASSUMPTION and is listed by assumptions_used() for the report.

Vectorised semantics: a value is a float or a numpy array; a trigger is a bool or a
bool array. `if/else_if/else` inside a value is applied per element with np.where.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(TOOLS))
sys.path.insert(0, TOOLS)
import pdx_parse  # noqa: E402

# ASSUMPTION: vanilla named values this session cannot read. Values cited in mod comments
# are marked "cited"; the rest are typical-magnitude guesses. In vanilla the gold values
# scale with realm income (they are script values), so a single number per tier is a
# simplification: see GOLD_BY_TIER.
VANILLA_DEFAULTS = {
    'low_dread': (20, 'cited: eotg_cartel_values.txt -> 00_basic_values.txt:993'),
    'medium_dread': (40, 'cited: 00_basic_values.txt:994'),
    'high_dread': (80, 'cited: 00_basic_values.txt:995'),
    'miniscule_dread_gain': (5, 'cited: Cartel spec §2.5 (Lean liege +5)'),
    'minor_dread_gain': (10, 'ASSUMPTION: between miniscule 5 and medium 20'),
    'medium_dread_gain': (20, 'cited: Cartel spec §2.5 (Lean +20)'),
    'major_dread_gain': (30, 'ASSUMPTION'),
    'massive_dread_gain': (50, 'ASSUMPTION'),
    'miniscule_dread_loss': (-5, 'cited: Cartel spec §2.5 (refusal -5)'),
    'medium_prestige_value': (150, 'cited: Cartel spec §6.2 (00_basic_values.txt:1002)'),
    'major_legitimacy_gain': (200, 'cited: eotg_cartel_values.txt (00_legitimacy_values.txt:174)'),
    # gold values: per-tier ASSUMPTION, overridden in contexts by GOLD_BY_TIER
    'minor_gold_value': (40, 'ASSUMPTION: vanilla scales with income; county-duke mid value'),
    'medium_gold_value': (100, 'ASSUMPTION: vanilla scales with income'),
    'major_gold_value': (250, 'ASSUMPTION: vanilla scales with income'),
    'massive_gold_value': (500, 'ASSUMPTION'),
}
# ASSUMPTION: gold-value scale by highest held tier (2=county, 3=duchy, 4=kingdom, 5=empire)
GOLD_BY_TIER = {2: 0.6, 3: 1.0, 4: 1.8, 5: 3.0}

_assumptions_used = {}


def assumptions_used():
    return dict(_assumptions_used)


class Unknown(Exception):
    pass


class Script:
    def __init__(self, repo=REPO, folders=('common', 'events')):
        self.repo = repo
        self.defs = {}       # key -> (relpath, node)  (top-level definitions)
        self.files = {}
        for folder in folders:
            base = os.path.join(repo, folder)
            for dp, _, fns in os.walk(base):
                for fn in sorted(fns):
                    if not fn.endswith('.txt') or not fn.startswith('eotg_') and not fn.startswith('zz_eotg_'):
                        continue
                    p = os.path.join(dp, fn)
                    rel = os.path.relpath(p, repo).replace('\\', '/')
                    try:
                        doc = pdx_parse.parse_file(p)
                    except Exception:
                        continue
                    self.files[rel] = doc
                    for n in doc.nodes:
                        if n.key and n.op == '=' and n.key not in ('namespace',):
                            # later definitions win, as in the engine (by load order ~ path)
                            self.defs.setdefault(n.key, (rel, n))
        self.trace = {}
        self.overrides = {}   # name -> number: what-if tuning (never written to script)

    # ---------------------------------------------------------------- lookup
    def node(self, name):
        if name not in self.defs:
            raise KeyError(name)
        return self.defs[name][1]

    def where(self, name):
        rel, n = self.defs[name]
        return f'{rel}:{n.line}'

    def has(self, name):
        return name in self.defs

    def num(self, name, ctx=None):
        """A script value as a number (constants, or formulas against ctx)."""
        if name in self.overrides:
            return self.overrides[name]
        return self.eval_value(self.node(name), ctx or Ctx())

    # ---------------------------------------------------------------- values
    def resolve(self, tok, ctx):
        """A value token: number, named value, var:/scope:/local_var:, engine name."""
        if isinstance(tok, (int, float, np.ndarray)):
            return tok
        t = tok.strip()
        try:
            return float(t)
        except ValueError:
            pass
        if t in ('yes', 'no'):
            return 1.0 if t == 'yes' else 0.0
        if t.startswith('flag:'):
            return t
        if t in ctx.values:
            return ctx.values[t]
        if t in self.overrides:
            return self.overrides[t]
        if t in self.defs and self.defs[t][0].startswith('common/script_values'):
            return self.eval_value(self.defs[t][1], ctx)
        if t in VANILLA_DEFAULTS:
            v, why = VANILLA_DEFAULTS[t]
            _assumptions_used[t] = why
            if t.endswith('_gold_value') and 'tier' in ctx.values:
                tiers = np.asarray(ctx.values['tier'])
                scale = np.vectorize(lambda x: GOLD_BY_TIER.get(int(x), 1.0))(tiers) if np.ndim(tiers) else GOLD_BY_TIER.get(int(tiers), 1.0)
                _assumptions_used['GOLD_BY_TIER'] = 'ASSUMPTION: gold values scale by tier ' + repr(GOLD_BY_TIER)
                return v * scale
            return v
        return ctx.lookup(t)

    def eval_value(self, node, ctx):
        """Evaluate a script value node (constant `x = 5` or a block)."""
        if not node.is_block:
            return self.resolve(node.value, ctx)
        return self._eval_ops(node.children, ctx, 0.0)

    def _operand(self, n, ctx):
        if n.is_block:
            return self._eval_ops(n.children, ctx, 0.0)
        return self.resolve(n.value, ctx)

    def _eval_ops(self, nodes, ctx, val):
        i = 0
        taken = None   # for if/else_if/else chains: mask of elements already handled
        while i < len(nodes):
            n = nodes[i]
            k = n.key
            if k in ('if', 'else_if', 'else'):
                if k == 'if':
                    taken = False
                limit = n.children and [c for c in n.children if c.key == 'limit']
                body = [c for c in n.children if c.key != 'limit']
                if k == 'else':
                    mask = np.logical_not(taken)
                else:
                    cond = self.eval_trigger(limit[0].children, ctx) if limit else True
                    mask = np.logical_and(cond, np.logical_not(taken))
                new = self._eval_ops(body, ctx, val)
                val = np.where(mask, new, val) if (np.ndim(mask) or np.ndim(new) or np.ndim(val)) else (new if mask else val)
                taken = np.logical_or(taken, mask)
                i += 1
                continue
            taken = None
            if k == 'value':
                val = self._operand(n, ctx)
            elif k == 'add':
                val = val + self._operand(n, ctx)
            elif k == 'subtract':
                val = val - self._operand(n, ctx)
            elif k == 'multiply':
                val = val * self._operand(n, ctx)
            elif k == 'divide':
                d = self._operand(n, ctx)
                val = val / np.where(np.asarray(d) == 0, 1, d)
            elif k == 'min':
                val = np.maximum(val, self._operand(n, ctx))
            elif k == 'max':
                val = np.minimum(val, self._operand(n, ctx))
            elif k == 'floor' and n.value == 'yes':
                val = np.floor(val)
            elif k == 'ceiling' and n.value == 'yes':
                val = np.ceil(val)
            elif k == 'round' and n.value == 'yes':
                val = np.round(val)
            elif k in ('desc', 'format'):
                pass
            elif k and k.startswith('every_') or k and k.startswith('scope:') or k and k.endswith('_list'):
                # an iterator inside a value: ask the context (e.g. payer counts)
                val = val + ctx.lookup('iter:' + k)
            else:
                ctx.unknown('value-op:' + str(k))
            i += 1
        return val

    # ---------------------------------------------------------------- triggers
    def eval_trigger(self, nodes, ctx):
        """AND of a list of trigger statements."""
        res = True
        for n in nodes:
            res = np.logical_and(res, self._trig(n, ctx))
        return res

    def _cmp(self, a, op, b):
        if op in ('=', '==', '?='):
            return np.asarray(a) == np.asarray(b)
        return {'<': np.less, '<=': np.less_equal, '>': np.greater,
                '>=': np.greater_equal, '!=': np.not_equal}[op](a, b)

    def _trig(self, n, ctx):
        k, op = n.key, n.op
        if k in ('AND', 'trigger'):
            return self.eval_trigger(n.children, ctx)
        if k == 'OR':
            r = False
            for c in n.children:
                r = np.logical_or(r, self._trig(c, ctx))
            return r
        if k == 'NOT':
            return np.logical_not(self.eval_trigger(n.children, ctx))
        if k == 'NOR':
            r = False
            for c in n.children:
                r = np.logical_or(r, self._trig(c, ctx))
            return np.logical_not(r)
        if k == 'NAND':
            return np.logical_not(self.eval_trigger(n.children, ctx))
        if k == 'trigger_else':
            # ASSUMPTION-free approximation: evaluated as its own body (the matching
            # trigger_if's limit is not tracked across siblings)
            return self.eval_trigger(n.children, ctx)
        if k in ('custom_tooltip', 'custom_description', 'trigger_if'):
            body = [c for c in n.children if c.key not in ('text', 'subject', 'object', 'limit')]
            if k == 'trigger_if':
                lim = [c for c in n.children if c.key == 'limit']
                cond = self.eval_trigger(lim[0].children, ctx) if lim else True
                return np.logical_or(np.logical_not(cond), self.eval_trigger(body, ctx))
            return self.eval_trigger(body, ctx)
        if k == 'always':
            return n.value == 'yes'
        if k == 'has_trait' and not n.is_block:
            return ctx.lookup('trait:' + n.value, default=False)
        if k == 'has_game_rule':
            return ctx.lookup('rule:' + n.value, default=False)
        if k in ('has_character_flag', 'has_variable', 'has_character_modifier', 'has_county_modifier'):
            return ctx.lookup(f'{k}:{n.value}', default=False)
        if n.is_block and op in ('<', '<=', '>', '>=', '!=', '=='):
            a = self.resolve(k, ctx)
            return self._cmp(a, op, self._eval_ops(n.children, ctx, 0.0))
        if n.is_block:
            # scope change (liege ?= { ... }, scope:x = { ... }) or a parameterised trigger
            if k in self.defs and self.defs[k][0].startswith('common/scripted_triggers'):
                return ctx.lookup('trig:' + k, default=False)
            sub = ctx.scope(k)
            if sub is None:
                ctx.unknown('scope:' + str(k))
                return False
            return self.eval_trigger(n.children, sub)
        # scripted trigger `x = yes/no`
        if op == '=' and n.value in ('yes', 'no') and k in self.defs and self.defs[k][0].startswith('common/scripted_triggers'):
            key = 'trig:' + k
            if key in ctx.values:
                v = ctx.values[key]
            else:
                body = self.defs[k][1]
                v = self.eval_trigger(body.children, ctx) if body.is_block else False
            return v if n.value == 'yes' else np.logical_not(v)
        if op == '=' and n.value in ('yes', 'no'):
            v = ctx.lookup(k, default=None)
            if v is None:
                ctx.unknown('trigger:' + k)
                return False
            v = np.asarray(v).astype(bool)
            return v if n.value == 'yes' else np.logical_not(v)
        # comparison
        a = self.resolve(k, ctx)
        b = self.resolve(n.value, ctx) if not n.is_block else self._eval_ops(n.children, ctx, 0.0)
        return self._cmp(a, op, b)

    # ---------------------------------------------------------------- decisions
    def decision(self, name):
        n = self.node(name)
        d = {'name': name, 'where': self.where(name), 'cooldown_years': None, 'cost': {},
             'interval': {}, 'ai_will_do': None, 'ai_potential': None, 'is_valid': None}
        for c in n.children:
            if c.key == 'cooldown':
                for cc in c.children:
                    mult = {'years': 1.0, 'months': 1 / 12, 'days': 1 / 365}.get(cc.key)
                    if mult:
                        d['cooldown_years'] = float(cc.value) * mult
            elif c.key == 'cost':
                for cc in c.children:
                    d['cost'][cc.key] = cc
            elif c.key == 'ai_check_interval_by_tier':
                for cc in c.children:
                    d['interval'][cc.key] = float(cc.value)
            elif c.key == 'ai_check_interval':
                d['interval']['all'] = float(c.value)
            elif c.key in ('ai_will_do', 'ai_potential', 'is_valid', 'is_shown'):
                d[c.key] = c
        return d

    def cost_value(self, d, key, ctx):
        c = d['cost'].get(key)
        if c is None:
            return 0.0
        return self.eval_value(c, ctx)

    def ai_will_do(self, d, ctx):
        """`base` + modifiers (add / factor), as _decisions.info: % chance per check."""
        node = d['ai_will_do']
        if node is None:
            return 0.0
        val = 0.0
        for c in node.children:
            if c.key in ('base', 'value'):
                val = self.resolve(c.value, ctx) if not c.is_block else self._eval_ops(c.children, ctx, 0.0)
        for c in node.children:
            if c.key == 'modifier':
                trig = [x for x in c.children if x.key not in ('add', 'factor', 'desc')]
                cond = self.eval_trigger(trig, ctx)
                for x in c.children:
                    if x.key == 'add':
                        amt = self._operand(x, ctx)
                        val = val + np.where(cond, amt, 0.0)
                    elif x.key == 'factor':
                        f = self._operand(x, ctx)
                        val = val * np.where(cond, f, 1.0)
        return val

    def ai_potential(self, d, ctx):
        node = d['ai_potential']
        return True if node is None else self.eval_trigger(node.children, ctx)

    # ---------------------------------------------------------------- blocks
    def find(self, nodes, key):
        return [n for n in nodes if n.key == key]

    def find_deep(self, node, key):
        out = []
        for n, _ in pdx_parse.walk(node.children if node.is_block else []):
            if n.key == key:
                out.append(n)
        return out

    def effect_group_intervals(self, story):
        """[(years, node)] for each effect_group of a story cycle."""
        out = []
        for c in self.node(story).children:
            if c.key == 'effect_group':
                yrs = None
                for cc in c.children:
                    if cc.key in ('years', 'months', 'days'):
                        yrs = float(cc.value) * {'years': 1, 'months': 1 / 12, 'days': 1 / 365}[cc.key]
                out.append((yrs, c))
        return out

    def random_list_entries(self, rl):
        """[(base_weight, [modifier nodes], body nodes)] of a random_list node."""
        out = []
        for c in rl.children:
            try:
                w = float(c.key)
            except (TypeError, ValueError):
                continue
            mods = [x for x in c.children if x.key == 'modifier']
            body = [x for x in c.children if x.key != 'modifier']
            out.append((w, mods, body))
        return out

    def weight(self, base, mods, ctx):
        w = base
        for m in mods:
            trig = [x for x in m.children if x.key not in ('add', 'factor')]
            cond = self.eval_trigger(trig, ctx)
            for x in m.children:
                if x.key == 'add':
                    w = w + np.where(cond, self._operand(x, ctx), 0.0)
                elif x.key == 'factor':
                    w = w * np.where(cond, self._operand(x, ctx), 1.0)
        return np.maximum(w, 0.0)

    def change_calls(self, node, effect):
        """[(conditions, amount_token, line)] for every `effect = { AMOUNT = x }` call under
        node; conditions are the `limit` trigger lists of the enclosing ifs (outermost
        first). else_if/else siblings are returned with their own limits only."""
        out = []

        def rec(nodes, conds):
            for n in nodes:
                if n.key == effect and n.is_block:
                    amt = [c for c in n.children if c.key == 'AMOUNT']
                    if amt:
                        out.append((list(conds), amt[0].value, n.line))
                elif n.is_block and n.key not in ('limit', 'trigger', 'ai_will_do', 'ai_potential', 'is_valid', 'is_shown'):
                    lim = [c for c in n.children if c.key == 'limit']
                    nc = conds + ([lim[0].children] if lim else [])
                    rec(n.children, nc)
        rec(node.children, [])
        return out


class Ctx:
    """Evaluation context: names -> number/array; nested scopes; unknown-name log."""

    def __init__(self, values=None, scopes=None, n=None, strict=False):
        self.values = dict(values or {})
        self.scopes = dict(scopes or {})
        self.n = n
        self.strict = strict
        self.unknowns = set()

    def lookup(self, name, default=Unknown):
        if name in self.values:
            return self.values[name]
        if default is Unknown:
            self.unknown(name)
            return 0.0
        return default

    def unknown(self, name):
        self.unknowns.add(name)
        _assumptions_used['unresolved:' + name] = 'ASSUMPTION: unresolved name evaluated as 0/false'
        if self.strict:
            raise Unknown(name)

    def scope(self, key):
        return self.scopes.get(key.replace('?', ''))

    def child(self, values=None, scopes=None):
        c = Ctx({**self.values, **(values or {})}, {**self.scopes, **(scopes or {})}, self.n, self.strict)
        c.unknowns = self.unknowns
        return c


def per_check_to_annual(pct, months_interval):
    """ai_will_do is a % chance per AI check; checks every `months_interval` months."""
    p = np.clip(np.asarray(pct, dtype=float) / 100.0, 0, 1)
    if months_interval <= 0:
        return np.zeros_like(p)
    checks = 12.0 / months_interval
    return 1 - (1 - p) ** checks
