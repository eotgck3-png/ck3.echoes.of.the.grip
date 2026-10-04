"""Generate a console test recipe for every mod event. Python 3, standard library only.

    python docs/tools/gen_test_recipes.py                 # write docs/qa/generated/console_recipes.md
    python docs/tools/gen_test_recipes.py --check         # exit 1 if that file is stale
    python docs/tools/gen_test_recipes.py --event eotg_aug_tier1.005   # one recipe to stdout
    python docs/tools/gen_test_recipes.py --json out.json # every row as JSON
    python docs/tools/gen_test_recipes.py --root OTHER_CHECKOUT

For each event in events/eotg_*.txt it works out, from script alone:
  - FIRE COLD   yes / setup / no: whether `event <id>` works as is, works after
                console setup, or needs a parent event, saved scope, story or
                state that only play creates (and exactly what is missing);
  - SETUP       console lines for the mechanical requirements (traits, tier,
                flags, variables, gold, stress, skills), plain notes for the rest;
  - FIRE        the console line, with the target when the event fires on
                someone other than the player;
  - FIRED BY    every on_action, event, decision, story or effect that reaches it
                (the eotg_lint event graph, eotg_lint.fire_sites);
  - LIVE ROUTE  for FIRE COLD = no, the shortest chain from something the player
                controls (a decision) or the yearly pulse.
Console conventions follow docs/qa/HOW_TO_TEST_IN_GAME.md section 2. Output is
deterministic: the same tree gives byte-identical output.
"""
import argparse
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eotg_lint as L  # noqa: E402
import pdx_parse as P  # noqa: E402

DEFAULT_ROOT = os.path.dirname(os.path.dirname(HERE))
OUT_REL = "docs/qa/generated/console_recipes.md"

# event file stem -> heading (docs/qa/cybernetics_test_plan.md section 4), in order
GROUPS = [
    ("initiation", "Initiation"), ("tier1", "Augmented"), ("tier2", "Enhanced"),
    ("tier3", "Overclocked"), ("countdown", "Countdown (story)"), ("fracture", "Neurofractured"),
    ("heir", "Heir's Arc (story)"), ("endgame", "Endgames"), ("patron", "Patron (story)"),
    ("retinue", "Iron Retinue (story)"), ("nonruler", "Non-ruler lifecycle"),
    ("procedures", "Procedures"), ("interactions", "Interactions"), ("tamper", "Tamper"),
    ("activities", "Activities"),
]

AUG_TRAIT = "eotg_cybernetics"
INITIATE = "effect eotg_aug_initiate_effect = yes"
SKILLS = ("diplomacy", "martial", "stewardship", "intrigue", "learning", "prowess")
TRIVIAL = {("is_alive", "yes"), ("is_adult", "yes"), ("always", "yes")}
CHAR_LINKS = {"primary_heir": "the primary heir", "liege": "the liege", "father": "the father",
              "mother": "the mother", "primary_spouse": "the spouse", "host": "the host",
              "employer": "the employer", "top_liege": "the top liege",
              "player_heir": "the player heir", "betrothed": "the betrothed"}
ROOT_LINKS = {"root", "this", "story_owner"}
ITER_NOUNS = {"knight": "a knight", "courtier": "a courtier", "vassal": "a vassal",
              "child": "a child", "councillor": "a councillor", "spouse": "a spouse",
              "relation": "a relation", "owned_story": "a story", "close_family_member":
              "a close family member", "heir": "an heir", "sibling": "a sibling",
              "prisoner": "a prisoner", "courtier_or_guest": "a courtier or guest",
              "pool_character": "a pool character", "held_title": "a held title",
              "sub_realm_county": "a county in the realm", "consort": "a consort",
              "ally": "an ally", "dynasty_member": "a dynasty member",
              "parent": "a parent", "close_or_extended_family_member": "a family member"}
REL_ROOT = {"is_close_family_of": "your close family", "is_spouse_of": "your spouse",
            "is_child_of": "your child", "is_parent_of": "your parent",
            "is_vassal_of": "your vassal", "is_courtier_of": "your courtier",
            "is_knight_of": "your knight", "is_lover_of": "your lover",
            "is_consort_of": "your consort", "is_heir_of": "your heir"}
SCOPE_SAVERS = ("save_scope_as", "save_temporary_scope_as")
SCOPE_VALUE_SAVERS = ("save_scope_value_as", "save_temporary_scope_value_as")
ENGINE_SCOPES = {"story": "scope:story (set by the story that fires it)",
                 "actor": "scope:actor (set by the interaction)",
                 "recipient": "scope:recipient (set by the interaction)",
                 "activity": "scope:activity (set by the activity)",
                 "scheme": "scope:scheme (set by the scheme)"}
SCOPE_READ_RE = re.compile(r"\bscope:([A-Za-z_]\w*)")
VAR_READ_RE = re.compile(r"(?<![\w:.])var:([A-Za-z_]\w*)")
LOC_SCOPE_RE = re.compile(r"\[([A-Za-z_]\w*)\.")
CMP = {">=": lambda n: n, ">": lambda n: n + 1, "==": lambda n: n, "=": lambda n: n}

# FIX 9b: title (county) scopes. Keys that only make sense on a landed title,
# switches into a title, and iterators over titles.
TITLE_KEYS = {"development_level", "county_control", "has_county_modifier",
              "add_county_modifier", "remove_county_modifier", "change_development_level",
              "change_development_progress", "change_county_control", "title_province",
              "holder", "tier", "is_title_created", "de_jure_liege", "any_county_province",
              "every_county_province", "random_county_province", "ordered_county_province",
              "set_county_culture", "set_county_faith"}
TITLE_LINKS = {"capital_county", "primary_title", "county", "duchy", "kingdom", "empire"}
TITLE_ITER_RE = re.compile(r"^(any|every|random|ordered)_(held_title|realm_county|"
                           r"sub_realm_county|county_in_region|realm_de_jure_county|"
                           r"in_de_jure_hierarchy|de_jure_county)$")
TITLE_TO_CHAR = {"holder", "current_holder"}


def _num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return int(f) if f == int(f) else f


def _fmt(v):
    return str(v)


# ------------------------------------------------------------------ requirements
class Req:
    """One requirement. kind: line (console), note, scope, story, flag, varstate,
    varscope; human is the plain-English phrase; console the console line."""
    __slots__ = ("kind", "name", "human", "console", "order", "default", "scope")

    def __init__(self, kind, name, human, console=None, order=50, default=False, scope=None):
        self.kind, self.name, self.human, self.console, self.order = \
            kind, name, human, console, order
        self.default = default      # a fresh character already meets it
        self.scope = scope          # None = the event's root; else a title scope label

    def key(self):
        return (self.kind, self.name, self.human, self.console, self.scope)


class Model:
    """Everything the recipes need from the loaded mod."""

    def __init__(self, root):
        self.mod = L.Mod(root)
        L.rule_l003(self.mod)          # fills mod.loc
        self.loc = {}
        for rel, line, key, value in L.iter_loc_values(self.mod):
            self.loc.setdefault(key, value)
        self.events = {eid: (rel, node) for rel, eid, node in self.mod.events()}
        self.sites = L.fire_sites(self.mod)
        self.triggers = {}
        for _, doc in self.mod.common_dir("scripted_triggers"):
            for n in doc.nodes:
                if n.is_block and n.key:
                    self.triggers[n.key] = n
        self.effects = self.mod.scripted_effects()
        self.saved_scope = collections.defaultdict(set)    # scope name -> {label}
        self.set_flag = collections.defaultdict(set)       # flag -> {label}
        self.set_var = collections.defaultdict(set)        # var -> {label}
        self.var_kinds = collections.defaultdict(set)      # var -> {"story", "other"}
        self.story_creators = collections.defaultdict(list)   # story -> [(label, site)]
        self.effect_callers = collections.defaultdict(set)    # effect -> {label}
        self.hook_parents = collections.defaultdict(set)      # custom on_action -> {hook}
        self._index()
        self._classify_titles()
        self._index_debug_decisions()

    # --- labels
    def label(self, kind, owner, parents=()):
        if kind == "event":
            opt = next((p for p in parents if p.key == "option"), None)
            where = ""
            if opt is not None:
                nm = P.first(opt.value, "name")
                v = nm.value if nm is not None and isinstance(nm.value, str) else "?"
                where = " option %s" % v.rsplit(".", 1)[-1]
            elif any(p.key == "immediate" for p in parents):
                where = " immediate"
            elif any(p.key == "after" for p in parents):
                where = " after"
            return "event %s%s" % (owner, where)
        return "%s %s" % (kind, owner)

    def _index(self):
        for rel, doc in sorted(self.mod.docs.items()):
            kind = L.file_kind(rel)
            for top in doc.nodes:
                if not top.key:
                    continue
                for n, parents in P.walk([top]):
                    lab = None
                    if n.key in SCOPE_SAVERS and isinstance(n.value, str):
                        self.saved_scope[n.value].add(self.label(kind, top.key, parents))
                    elif n.key in SCOPE_VALUE_SAVERS and n.is_block:
                        nm = P.first(n.value, "name")
                        if nm is not None and isinstance(nm.value, str):
                            self.saved_scope[nm.value].add(self.label(kind, top.key, parents))
                    elif n.key and L.FLAG_SETTERS.match(n.key) and n.key.startswith("add_"):
                        f = n.value if isinstance(n.value, str) else None
                        if n.is_block:
                            ff = P.first(n.value, "flag")
                            f = ff.value if ff is not None and isinstance(ff.value, str) else None
                        if f:
                            self.set_flag[f].add(self.label(kind, top.key, parents))
                    elif n.key in L.VAR_SETTERS or n.key == "change_variable":
                        nm = P.first(n.value, "name") if n.is_block else None
                        v = nm.value if nm is not None else n.value if isinstance(n.value, str) \
                            else None
                        if isinstance(v, str):
                            lab = self.label(kind, top.key, parents)
                            self.set_var[v].add(lab)
                            in_story = kind == "story" or any(
                                p.key == "scope:story" or (p.key or "").endswith("owned_story")
                                for p in parents)
                            self.var_kinds[v].add("story" if in_story else "other")
                    elif n.key == "create_story" and isinstance(n.value, str):
                        self.story_creators[n.value].append(
                            (self.label(kind, top.key, parents), kind, top.key))
                    if n.key in self.effects and top.key != n.key:
                        self.effect_callers[n.key].add(self.label(kind, top.key, parents))
                        for sc in call_saves(self, n):
                            self.saved_scope[sc].add(self.label(kind, top.key, parents))
                    if kind == "on_action" and n.key == "on_actions" and n.is_block:
                        for c in n.value:
                            if c.is_bare:
                                self.hook_parents[c.key].add(top.key)

    # --- FIX 9b: which definitions and saved scopes are titles
    def _title_body(self, nodes):
        """True when these nodes, at their own scope, use a title-only key or a
        mod trigger/effect already known to run on a title."""
        for c in nodes:
            k = c.key
            if not k or k == "#":
                continue
            if k in TITLE_KEYS or k in self.title_defs:
                return True
            if k in ("limit", "trigger", "AND", "OR", "NOT", "NOR", "if", "else_if", "else",
                     "custom_description", "custom_tooltip", "hidden_effect") and c.is_block:
                if self._title_body(c.value):
                    return True
        return False

    def _classify_titles(self):
        self.title_defs = set()          # scripted triggers/effects that run on a title
        defs = dict(self.triggers)
        defs.update(self.effects)
        changed = True
        while changed:
            changed = False
            for name, node in defs.items():
                if name not in self.title_defs and node.is_block and self._title_body(node.value):
                    self.title_defs.add(name)
                    changed = True
        # saved scopes that hold titles: saved inside a title context, or used
        # as scope:x = { <title content> }
        self.title_scopes = set()
        for rel, doc in sorted(self.mod.docs.items()):
            for top in doc.nodes:
                if not top.is_block or not top.key:
                    continue
                start = top.key in self.title_defs and top.key in self.effects
                self._collect_title_scopes(top.value, start)
        for _ in range(3):      # scope:x = { scope:y-content } chains
            for rel, doc in sorted(self.mod.docs.items()):
                for n, _p in P.walk(doc.nodes):
                    if n.is_block and n.key and n.key.startswith("scope:") and \
                            "." not in n.key and self._title_body(n.value):
                        self.title_scopes.add(n.key[6:])

    def _collect_title_scopes(self, nodes, in_title):
        for c in nodes:
            k = c.key
            if not k or k == "#":
                continue
            if k in SCOPE_SAVERS and isinstance(c.value, str) and in_title:
                self.title_scopes.add(c.value)
            if c.is_block:
                inner = in_title
                if self.is_title_switch(k):
                    inner = True
                elif k in TITLE_TO_CHAR or is_scope_switch(k):
                    inner = False
                self._collect_title_scopes(c.value, inner)

    def is_title_switch(self, k, node=None):
        if not k:
            return False
        if k in TITLE_LINKS or k.startswith("title:") or TITLE_ITER_RE.match(k):
            return True
        if k.startswith("scope:") and "." not in k:
            return k[6:] in getattr(self, "title_scopes", ()) or \
                (node is not None and node.is_block and self._title_body(node.value))
        if k.startswith(("every_in_global_list", "any_in_global_list", "random_in_global_list",
                         "ordered_in_global_list")) and node is not None and node.is_block:
            return self._title_body(node.value)
        return False

    def title_label(self, k):
        """How a title scope is named in recipes."""
        return self._title_label(k)

    def _title_label(self, k):
        """How a title scope is named in recipes."""
        if k.startswith("scope:") or k.startswith("title:") or k in TITLE_LINKS:
            return k
        if TITLE_ITER_RE.match(k):
            return "one of your counties (%s)" % k
        return k

    def _index_debug_decisions(self):
        """{variable: decision key} for debug-only decisions whose effect sets it
        (directly or through scripted effects): the recipe can point at them."""
        self.debug_vars = {}
        for rel, doc in self.mod.common_dir("decisions"):
            for d in doc.nodes:
                if not d.is_block:
                    continue
                shown = P.first(d.value, "is_shown")
                if shown is None or not any(n.key == "debug_only" for n, _ in P.walk(shown.value)):
                    continue
                eff = P.first(d.value, "effect")
                for var in self._vars_set(eff.value if eff is not None else [], set()):
                    self.debug_vars.setdefault(var, d.key)

    def _vars_set(self, nodes, seen):
        out = set()
        for n, _ in P.walk(nodes):
            if n.key in L.VAR_SETTERS and n.is_block:
                nm = P.first(n.value, "name")
                if nm is not None and isinstance(nm.value, str):
                    out.add(nm.value)
            elif n.key in self.effects and n.key not in seen:
                seen.add(n.key)
                out |= self._vars_set(self.effects[n.key].value, seen)
        return out

    # --- trigger translation
    def reqs(self, nodes, neg=False, depth=0, own=True, scope=None):
        out = []
        for n in nodes:
            if n.key in (None, "#") or n.key.startswith("@"):
                continue
            for r in self.req(n, neg, depth, own):
                if scope is not None and r.scope is None:
                    r.scope = scope
                out.append(r)
        return out

    def req(self, n, neg, depth, own):
        k, v, op = n.key, n.value, n.op
        sv = v if isinstance(v, str) else None
        if (k, sv) in TRIVIAL and not neg:
            return []
        if k in ("AND", "custom_description", "custom_tooltip") and n.is_block:
            inner = [c for c in n.value if c.key not in ("text", "subject", "object", "value")]
            return self.reqs(inner, neg, depth, own)
        if k in ("NOT", "NOR") and n.is_block:
            kids = [c for c in n.value if c.key != "#"]
            if len(kids) == 1 or k == "NOR":
                return self.reqs(kids, not neg, depth, own)
            return [Req("note", None, "not all of: %s" % self.describe(kids))]
        if k == "OR" and n.is_block:
            kids = [c for c in n.value if c.key != "#"]
            if neg:      # NOT OR = none of them
                return self.reqs(kids, True, depth, own)
            first = self.req(kids[0], False, depth, own) if kids else []
            rest = self.describe(kids[1:])
            if first and all(r.console for r in first):
                return first + ([Req("note", None, "(or instead: %s)" % rest, order=90)]
                                if rest else [])
            return [Req("note", None, "one of: %s" % self.describe(kids))]
        # FIX 9b: inside a title, `holder = { }` is about the title's holder,
        # who is the event's root; marked "@root" so the outer title label
        # does not claim it
        if k in TITLE_TO_CHAR and sv in ("root", "scope:root"):
            return [Req("note", None, "not held by you" if neg else "held by you")]
        if n.is_block and k in TITLE_TO_CHAR:
            out = self.reqs(n.value, neg, depth, own)
            for r in out:
                if r.scope is None:
                    r.scope = "@root"
            return out
        # FIX 9b: a switch into a title: its conditions belong to that title
        if n.is_block and self.is_title_switch(k, n) and not neg:
            label = self.title_label(k)
            inner = [c for c in n.value if c.key not in ("limit", "#", "variable", "order_by")]
            lim = P.first(n.value, "limit")
            if lim is not None and lim.is_block:
                inner = list(lim.value) + inner
            pre = []
            if k.startswith("scope:"):
                pre.append(Req("scope", k[6:], "scope:%s" % k[6:]))
            return pre + self.reqs(inner, False, depth, own, scope=label)
        if k == "development_level" and _num(sv) is not None and op in CMP and not neg:
            x = CMP[op](_num(sv))
            return [Req("line", "development", "development %s+" % x,
                        "effect change_development_level = %s" % x, order=45)]
        if k == "county_control" and _num(sv) is not None and op in CMP and not neg:
            x = CMP[op](_num(sv))
            return [Req("line", "control", "control %s+" % x,
                        "effect change_county_control = %s" % x, order=46)]
        if k == "has_county_modifier" and sv and not neg:
            return [Req("line", sv, "modifier %s" % sv, "effect add_county_modifier = %s" % sv,
                        order=47)]
        if k in ("development_level", "county_control") and sv and not neg:
            return [Req("note", k, "%s %s %s" % (k.replace("_", " "), op, sv))]
        if k and k.startswith("var:") and "." not in k and sv and sv.startswith("flag:") \
                and op in ("=", "==", "?="):
            name = k[4:]
            if neg:
                return [Req("note", name, "%s is not %s" % (name, sv), default=True)]
            return [Req("varflag", name, "%s = %s" % (name, sv),
                        "effect set_variable = { name = %s value = %s }" % (name, sv),
                        order=39)]
        if k == "has_trait" and sv:
            if sv == AUG_TRAIT:
                if neg:
                    return [Req("note", None, "must not be augmented (if you are: "
                                "`effect eotg_aug_remove_all_effect = yes`)", order=5,
                                default=True)]
                return [Req("line", sv, "augmented", INITIATE, order=1)]
            return [Req("line", sv, ("without trait %s" if neg else "has trait %s") % sv,
                        ("remove_trait %s" if neg else "add_trait %s") % sv, order=10,
                        default=neg)]
        if k == "has_trait_xp" and n.is_block:
            t = P.first(n.value, "trait")
            val = P.first(n.value, "value")
            if t is not None and val is not None and _num(val.value) is not None and not neg \
                    and val.op in CMP:
                x = CMP[val.op](_num(val.value))
                tr = t.value
                lines = [Req("line", tr, "%s xp %s+" % (tr, x),
                             "effect add_trait_xp = { trait = %s value = %s }" % (tr, x),
                             order=2)]
                if tr == AUG_TRAIT:
                    lines.insert(0, Req("line", AUG_TRAIT, "augmented", INITIATE, order=1))
                return lines
            return []      # an upper bound: the lower bound sets it
        if k in self.triggers and sv in ("yes", "no"):
            positive = (sv == "yes") != neg
            if depth > 6:
                return [Req("note", None, "%s = %s" % (k, "yes" if positive else "no"))]
            body = [c for c in self.triggers[k].value if c.key != "#"]
            inner = self.reqs(body, not positive, depth + 1, own)
            unaug = [r for r in inner if r.kind == "note" and "must not be augmented" in r.human]
            if unaug:
                return unaug[:1]
            if not positive and len(body) > 1:
                # NOT of an AND: not mechanical; say it in one line
                special = [r for r in inner if r.kind == "note" and "augmented" in r.human]
                return special or [Req("note", k, "%s = no (see common/scripted_triggers)" % k,
                                       default=True)]
            keep = [r for r in inner if r.kind != "note" or r.human.startswith("(or instead")]
            if len(keep) != len(inner):
                # "= no" of a state test (has_patron = no...) holds for a fresh character
                keep.append(Req("note", k, "%s = %s (see common/scripted_triggers)"
                                % (k, "yes" if positive else "no"), default=not positive))
            return keep
        if k in self.triggers and n.is_block:
            return [Req("note", k, "%s = { … } (parameterised scripted trigger)" % k)]
        if k == "has_character_flag" and sv:
            if neg:
                if own:
                    return [Req("line", sv, "without flag %s" % sv,
                                "effect remove_character_flag = %s" % sv, order=30,
                                default=True)]
                return []
            return [Req("flag", sv, "flag %s" % sv, "effect add_character_flag = %s" % sv,
                        order=30)]
        if k == "has_variable" and sv:
            if neg:
                return []
            return [Req("varstate", sv, "variable %s" % sv,
                        "effect set_variable = { name = %s value = 1 }" % sv, order=40)]
        if k and k.startswith("var:") and "." not in k and _num(sv) is not None:
            name = k[4:]
            num = _num(sv)
            o = op
            if neg:
                o = {">=": "<", ">": "<=", "<": ">=", "<=": ">", "=": "!=", "==": "!="}.get(o, o)
            if o in (">=", ">", "=", "=="):
                x = CMP[o](num)
                return [Req("varnum", name, "%s %s %s" % (name, o, _fmt(num)),
                            "effect set_variable = { name = %s value = %s }" % (name, _fmt(x)),
                            order=40)]
            return [Req("varcap", name, "%s %s %s" % (name, o, _fmt(num)), order=41)]
        if k and k.startswith("var:") and (n.is_block or (sv and sv.startswith(("scope:", "var:",
                                                                                 "flag:")))):
            name = k[4:].split(".")[0]
            return [] if neg else [Req("varscope", name, "var:%s" % name)]
        if k == "exists" and sv:
            if neg:
                return []
            if sv.startswith("scope:"):
                return [Req("scope", sv[6:].split(".")[0], "scope:%s" % sv[6:])]
            if sv.startswith("var:"):
                return [Req("varscope", sv[4:].split(".")[0], "var:%s" % sv[4:])]
            if sv in CHAR_LINKS:
                return [Req("note", None, "needs %s" % CHAR_LINKS[sv])]
            return [Req("note", None, "needs %s" % sv)]
        if k and k.startswith("scope:"):
            name = k[6:].split(".")[0]
            return [] if neg else [Req("scope", name, "scope:%s" % name)]
        if k == "any_owned_story" and n.is_block and not neg:
            st = P.first(n.value, "story_type")
            if st is not None and isinstance(st.value, str):
                return [Req("story", st.value, "story %s" % st.value)]
        if (k, sv) == ("this", "root"):
            return [Req("note", None, "not you" if neg else "you")]
        if sv in ("root", "scope:root") and k in REL_ROOT:
            return [Req("note", None, ("not " if neg else "") + REL_ROOT[k])]
        if k == "gold" and sv and _num(sv) is None and not neg:
            return [Req("note", None, "gold %s %s (`effect add_gold = 500` usually covers it)"
                        % (op, sv))]
        if k == "gold" and n.is_block and not neg:
            return [Req("note", None, "enough gold (a script-value check; "
                        "`effect add_gold = 500` usually covers it)")]
        if k == "gold" and _num(sv) is not None and op in CMP and not neg:
            return [Req("line", "gold", "gold %s+" % CMP[op](_num(sv)),
                        "effect add_gold = %s" % CMP[op](_num(sv)), order=60)]
        if k == "stress_level" and _num(sv) is not None and op in CMP and not neg:
            lv = CMP[op](_num(sv))
            return [Req("line", "stress", "stress level %s+" % lv,
                        "effect add_stress = %s" % (lv * 100), order=60)]
        if k == "stress" and _num(sv) is not None and op in CMP and not neg:
            return [Req("line", "stress", "stress %s+" % CMP[op](_num(sv)),
                        "effect add_stress = %s" % CMP[op](_num(sv)), order=60)]
        if k in SKILLS and _num(sv) is not None and op in CMP and not neg:
            x = CMP[op](_num(sv))
            return [Req("line", k, "%s %s+" % (k, x), "effect add_%s_skill = %s" % (k, x),
                        order=70)]
        if k == "opinion" and n.is_block:
            tg = P.first(n.value, "target")
            val = P.first(n.value, "value")
            who = "you" if tg is not None and tg.value in ("root", "scope:root") else \
                (tg.value if tg is not None else "?")
            if val is not None:
                return [Req("note", None, "opinion of %s %s %s" % (who, val.op, val.value))]
        if k in SKILLS and _num(sv) is not None and op in ("<", "<=") and not neg:
            return [Req("note", None, "%s at most %s" % (k, _num(sv) - (1 if op == "<" else 0)))]
        if k == "any_relation" and n.is_block and not neg:
            ty = P.first(n.value, "type")
            if ty is not None and isinstance(ty.value, str) and len(n.value) == 1:
                return [Req("note", None, "needs a %s (relation)" % ty.value)]
        if k == "age" and _num(sv) is not None:
            return [Req("note", None, "aged %s %s" % (op if not neg else "not " + op, sv))]
        simple = {("is_at_war", "yes"): "must be at war", ("is_at_war", "no"): "must be at peace",
                  ("is_married", "yes"): "must be married", ("is_married", "no"):
                  "must be unmarried", ("is_landed", "yes"): "must be landed (a ruler)",
                  ("is_landed", "no"): "must be unlanded", ("is_imprisoned", "no"):
                  "must not be imprisoned", ("is_imprisoned", "yes"): "must be imprisoned",
                  ("is_ruler", "yes"): "must be a ruler", ("is_adult", "no"): "must be a child",
                  ("is_female", "yes"): "must be female", ("is_female", "no"): "must be male",
                  ("is_ai", "no"): "must be the player"}
        if sv in ("yes", "no") and (k, sv) in simple:
            flip = "no" if sv == "yes" else "yes"
            return [Req("note", None, simple.get((k, flip if neg else sv),
                                                 "%s = %s" % (k, flip if neg else sv)))]
        if n.is_block and k and (k.startswith("any_") or k in CHAR_LINKS or
                                 k.startswith("cp:")):
            noun = ITER_NOUNS.get(k[4:], k[4:].replace("_", " ")) if k.startswith("any_") \
                else CHAR_LINKS.get(k) or "your %s" % k[3:].replace("councillor_", "")
            noun = noun.replace("_", " ")
            inner = [c for c in n.value if c.key not in ("count", "percent", "#")]
            what = self.describe(inner)
            text = "%s %s%s" % ("no" if neg else "needs", noun,
                                " who/which: %s" % what if what else "")
            return [Req("note", None, text)]
        return [Req("note", None, ("not: " if neg else "") + self.raw(n))]

    def raw(self, n):
        if n.is_block:
            return "`%s = { … }`" % n.key
        return "`%s %s %s`" % (n.key, n.op or "=", n.value) if n.op else "`%s`" % n.key

    def describe(self, nodes):
        parts = []
        for r in self.reqs([c for c in nodes if c.key != "#"], own=False):
            parts.append("not augmented" if "must not be augmented" in r.human else r.human)
        seen = []
        for p in parts:
            if p not in seen:
                seen.append(p)
        return "; ".join(seen)


# ------------------------------------------------------------------ site analysis
def is_scope_switch(key):
    if not key:
        return False
    if key in ("random_list", "random", "random_valid"):
        return False
    return key.startswith(("scope:", "every_", "random_", "ordered_", "var:")) or \
        key in CHAR_LINKS or key in ROOT_LINKS or key.startswith("cp:")


def _effect_entry_label(model, name):
    """The label of a title-scoped effect's own scope: its first top-level
    save_scope_as, else a description."""
    node = model.effects.get(name)
    if node is not None and node.is_block:
        for c in node.value:
            if c.key in SCOPE_SAVERS and isinstance(c.value, str):
                return "scope:%s" % c.value
    return "the county %s runs on" % name


def site_context(model, site):
    """(target, [Req]) for one fire site: who the event fires on, and the
    conditions on the path from the definition down to the reference.

    FIX 9b: conditions met inside a title scope (a title-scoped scripted
    effect, capital_county / title:x / scope:x holding a title, a held-title
    iterator) keep that scope as their label; `holder = { }` out of a title
    hands the event to that title's holder, which is the event's root.
    """
    scope = "root"          # "root" | a title label | "story" | another character
    if site.kind == "story":
        scope = "story"
    elif site.kind == "effect" and site.owner in model.title_defs:
        scope = _effect_entry_label(model, site.owner)
    title_scope = scope not in ("root", "story")
    reqs = []
    top = site.parents[0] if site.parents else None
    if top is not None and top.is_block and scope == "root":
        heads = {"on_action": ("trigger",), "event": ("trigger",),
                 "decision": ("is_shown", "is_valid")}.get(site.kind, ())
        for h in heads:
            for b in P.find(top.value, h):
                if b.is_block:
                    reqs += model.reqs(b.value, own=False)
    for p in site.parents[1:]:
        k = p.key
        if model.is_title_switch(k, p):
            scope, title_scope = model.title_label(k), True
            lim = P.first(p.value, "limit") if p.is_block else None
            if lim is not None and lim.is_block:
                reqs += model.reqs(lim.value, own=False, scope=scope)
            continue
        if title_scope and k in TITLE_TO_CHAR:
            scope, title_scope = "root", False      # the title's holder gets the event
            continue
        if is_scope_switch(k):
            scope, title_scope = ("root" if k in ROOT_LINKS else k), False
            continue
        if scope not in ("root",) and not title_scope:
            continue
        cond = None
        if k in ("if", "else_if") or (k or "").startswith(("every_", "random_")):
            cond = P.first(p.value, "limit") if p.is_block else None
        elif k and (k.isdigit() or k == "triggered_effect"):
            cond = P.first(p.value, "trigger") if p.is_block else None
        if cond is not None and cond.is_block:
            reqs += model.reqs(cond.value, own=False, scope=scope if title_scope else None)
    target = "root" if title_scope else scope
    if target != "root":
        # conditions on the root were about another character (the pulse's
        # root, an iterator); title facts stay true whoever gets the event
        reqs = [r for r in reqs if r.scope is not None]
    return target, reqs


def _scope_reads(node):
    """Scopes a node reads. A `?=` comparison is a guarded read (true or false
    when the scope is missing, never an error), so it requires nothing."""
    if node.op == "?=":
        return set()
    names = set()
    for text in (node.key or "", node.value if isinstance(node.value, str) else ""):
        names.update(m.group(1) for m in SCOPE_READ_RE.finditer(text))
    return names


def _saves_of(node):
    if node.key in SCOPE_SAVERS and isinstance(node.value, str):
        return {node.value}
    if node.key in SCOPE_VALUE_SAVERS and node.is_block:
        nm = P.first(node.value, "name")
        if nm is not None and isinstance(nm.value, str):
            return {nm.value}
    return set()


PARAM_RE = re.compile(r"^\$([A-Za-z_]\w*)\$$")


def effect_param_saves(model, name):
    """Parameters a scripted effect saves a scope under (save_scope_as = $NAME$)."""
    node = model.effects.get(name)
    out = set()
    if node is None:
        return out
    for n, _ in P.walk(node.value):
        v = None
        if n.key in SCOPE_SAVERS and isinstance(n.value, str):
            v = n.value
        elif n.key in SCOPE_VALUE_SAVERS and n.is_block:
            nm = P.first(n.value, "name")
            v = nm.value if nm is not None and isinstance(nm.value, str) else None
        m = PARAM_RE.match(v or "")
        if m:
            out.add(m.group(1))
    return out


def call_saves(model, node):
    """Scopes a call like `eotg_x_effect = { NAME = eotg_y }` saves through its
    parameters."""
    if node.key not in model.effects or not node.is_block:
        return set()
    params = {c.key: c.value for c in node.value if isinstance(c.value, str)}
    return {params[p] for p in effect_param_saves(model, node.key) if p in params}


def effect_profile(model, name, _stack=None):
    """(reads, saves) of a scripted effect, in order (FIX 9a): `reads` are the
    scopes it reads before saving them itself, i.e. what its caller must
    provide; `saves` everything it (and the effects it calls) saves."""
    _stack = set() if _stack is None else _stack
    if name in _stack or name not in model.effects:
        return set(), set()
    memo = model.__dict__.setdefault("_profiles", {})
    if name in memo:
        return memo[name]
    _stack.add(name)
    reads, saved = _ordered(model, model.effects[name].value, set(), _stack)
    _stack.discard(name)
    memo[name] = (reads, saved)
    return reads, saved


def _ordered(model, nodes, provided, _stack=None, in_duel=False):
    """Walk nodes in script order. Returns (unprovided reads, scopes saved here).
    `provided` is what exists on entry; it is not modified."""
    have = set(provided)
    reads, saved = set(), set()
    for n in nodes:
        if n.key == "#":
            continue
        duel = in_duel or n.key == "duel" or (n.key or "").endswith("_duel")
        for r in _scope_reads(n):
            if r not in have and not (duel and r == "duel_value"):
                reads.add(r)
        sv = _saves_of(n)
        if n.key in model.effects:
            er, es = effect_profile(model, n.key, _stack)
            reads |= er - have
            sv |= {x for x in es if not PARAM_RE.match(x)} | call_saves(model, n)
        if n.is_block:
            cr, cs = _ordered(model, n.value, have, _stack, duel)
            reads |= cr
            sv |= cs
        have |= sv
        saved |= sv
    return reads, saved


def effect_saves(model, name, _seen=None):
    """Scopes a scripted effect saves, through the effects it calls."""
    return effect_profile(model, name)[1]


def event_reads(model, ev):
    """(unprovided scope reads, var names read, scopes provided by immediate).

    FIX 9a, in the order the engine runs an event:
      trigger                 nothing in the event provides anything yet;
      immediate               its own earlier saves (and scripted effects');
      desc, title, portraits,
      option triggers, names  what immediate saved;
      each option's effects   immediate's saves + that option's earlier saves;
      after                   immediate + every option's saves.
    """
    vars_read = set()
    for n, _ in P.walk(ev.value):
        for text in (n.key or "", n.value if isinstance(n.value, str) else ""):
            vars_read.update(m.group(1) for m in VAR_READ_RE.finditer(text))
    unprovided = set()
    guarded = set()
    for n, _ in P.walk(ev.value):
        if n.op == "?=":
            for text in (n.key or "", n.value if isinstance(n.value, str) else ""):
                guarded.update(m.group(1) for m in SCOPE_READ_RE.finditer(text))
    model.__dict__["_last_guarded"] = guarded
    trig = [c for c in ev.value if c.key == "trigger"]
    unprovided |= _ordered(model, trig, set())[0]
    imm = [c for c in ev.value if c.key == "immediate"]
    r, provided = _ordered(model, imm, set())
    unprovided |= r
    option_saves = set()
    for c in ev.value:
        if c.key in ("trigger", "immediate", "option", "after", "#"):
            continue
        unprovided |= _ordered(model, [c], provided)[0]
    for opt in P.find(ev.value, "option"):
        pre = [c for c in opt.value if c.key in ("trigger", "name", "show_as_unavailable")]
        unprovided |= _ordered(model, pre, provided)[0]
        body = [c for c in opt.value if c.key not in ("trigger", "name", "show_as_unavailable",
                                                      "ai_chance")]
        r, sv = _ordered(model, body, provided)
        unprovided |= r
        option_saves |= sv
    aft = [c for c in ev.value if c.key == "after"]
    unprovided |= _ordered(model, aft, provided | option_saves)[0]
    return unprovided, vars_read, provided


def loc_keys_of(ev):
    keys = []
    for c in ev.value:
        if c.key in ("title", "desc"):
            acc = []
            L._loc_refs_in(c, acc)
            keys += [k for k, _ in acc]
    for opt in P.find(ev.value, "option"):
        for c in P.find(opt.value, "name"):
            acc = []
            L._loc_refs_in(c, acc)
            keys += [k for k, _ in acc]
    return keys


def title_of(model, ev):
    t = P.first(ev.value, "title")
    if t is None:
        return ""
    acc = []
    L._loc_refs_in(t, acc)
    for k, _ in acc:
        if k in model.loc:
            v = re.sub(r"\[[^\]]*\]", "…", model.loc[k])
            return re.sub(r"#\w+ |#!", "", v).strip()
    return ""


def _short(labels, n=3):
    labels = sorted(labels)
    s = ", ".join(labels[:n])
    return s + (" … (+%d)" % (len(labels) - n) if len(labels) > n else "")


def hook_chain(model, onaction, depth=0):
    parents = sorted(model.hook_parents.get(onaction, ()))
    if not parents or depth > 4:
        return onaction
    return "%s → %s" % (" / ".join(hook_chain(model, p, depth + 1) for p in parents), onaction)


def site_label(model, site):
    lab = model.label(site.kind, site.owner, site.parents)
    if site.kind == "on_action":
        return "on_action " + hook_chain(model, site.owner)
    if site.kind == "effect":
        callers = {"on_action " + hook_chain(model, c[len("on_action "):])
                   if c.startswith("on_action ") else c
                   for c in model.effect_callers.get(site.owner, set())}
        return lab + (" ← " + _short(callers) if callers else "")
    return lab


# ------------------------------------------------------------------ live route
KIND_PREF = {"decision": 0, "on_action": 1, "story": 2, "event": 3, "effect": 4}


def _upstream(model, kind, owner):
    """[(kind, owner, label)] that lead into a definition."""
    if kind == "event":
        # plain labels: the chain itself names an effect's callers
        return [(s.kind, s.owner, "on_action " + hook_chain(model, s.owner)
                 if s.kind == "on_action" else model.label(s.kind, s.owner, s.parents))
                for s in model.sites.get(owner, [])]
    if kind == "story":
        return [(k, o, "on_action " + hook_chain(model, o) if k == "on_action" else lab)
                for lab, k, o in model.story_creators.get(owner, [])]
    if kind == "effect":
        out = []
        for rel, doc in sorted(model.mod.docs.items()):
            kd = L.file_kind(rel)
            for top in doc.nodes:
                if not top.key or top.key == owner:
                    continue
                for n, parents in P.walk([top]):
                    if n.key == owner:
                        out.append((kd, top.key, model.label(kd, top.key, parents)))
                        break
        return out
    return []


def live_route(model, eid, max_depth=7):
    """Shortest upstream chain to a root the player reaches: a decision first,
    else an on_action (a pulse), else the longest chain found."""
    best = None
    frontier = [("event", eid, [])]
    seen = {("event", eid)}
    for _ in range(max_depth):
        nxt = []
        for kind, owner, chain in frontier:
            for k, o, lab in sorted(_upstream(model, kind, owner), key=lambda u: u[2]):
                if (k, o) in seen:
                    continue
                path = chain + [lab]
                if k in ("decision", "on_action"):
                    cand = (KIND_PREF[k], len(path), path)
                    if best is None or cand < best:
                        best = cand
                    continue
                seen.add((k, o))
                nxt.append((k, o, path))
        if best is not None and best[0] == 0:
            break
        frontier = nxt
        if not frontier:
            break
    if best is None:
        return "no route found in script"
    steps = list(reversed(best[2]))
    timed = any(st.startswith(("story", "on_action")) for st in steps)
    return "%s → this event%s" % (" → ".join(steps),
                                  "; then let time run (yearly pulses and stories pace it)"
                                  if timed else "")


# ------------------------------------------------------------------ recipes
def _root(reqs):
    """`holder = { }` conditions inside a title are the event root's ("@root")."""
    for r in reqs:
        if r.scope == "@root":
            r.scope = None
    return reqs


TITLE_PLACEHOLDER = "<county>"


def _title_placeholder(scope):
    if scope.startswith("title:") or scope in TITLE_LINKS:
        return scope
    return TITLE_PLACEHOLDER


def scoped_console(scope, console):
    """A console line for a title-scoped requirement: `effect <title> = { … }`."""
    inner = console[len("effect "):] if console.startswith("effect ") else console
    return "effect %s = { %s }" % (_title_placeholder(scope), inner)


def _plain(text):
    return re.sub(r"\[[^\]]*\]", "…", text)


def _dedupe(reqs):
    out, seen = [], set()
    numeric = {r.name for r in reqs if r.kind in ("varnum", "varcap", "varscope")}
    reqs = [r for r in reqs if not (r.kind == "varstate" and r.name in numeric)]
    for r in sorted(reqs, key=lambda r: (r.order, r.kind, r.name or "", r.human)):
        if r.key() in seen:
            continue
        seen.add(r.key())
        out.append(r)
    return out


def _upstream_owners(model, eid, depth=5):
    """'kind owner' strings for every definition upstream of an event."""
    seen, frontier = set(), [("event", eid)]
    for _ in range(depth):
        nxt = []
        for kind, owner in frontier:
            for k, o, _lab in _upstream(model, kind, owner):
                if (k, o) not in seen:
                    seen.add((k, o))
                    nxt.append((k, o))
        frontier = nxt
    return ["%s %s" % ko for ko in sorted(seen)]


def _savers(model, name, firer_labels):
    labels = model.saved_scope.get(name, set())
    near = {lab for lab in labels if any(lab == f or lab.startswith(f + " ")
                                         for f in firer_labels)}
    return _short(near or labels) if (near or labels) else "nothing in script"


def recipe(model, eid):
    rel, ev = model.events[eid]
    sites = sorted(model.sites.get(eid, []), key=lambda s: (s.rel, s.line))
    model.__dict__.pop("_last_guarded", None)
    hidden = any(c.key == "hidden" and c.value == "yes" for c in ev.value)
    trig = P.first(ev.value, "trigger")
    own = _root(model.reqs(trig.value) if trig is not None and trig.is_block else [])

    # context: requirements common to every firing path (root scope only)
    targets = collections.OrderedDict()
    ctx_sets = []
    for s in sites:
        tgt, rq = site_context(model, s)
        rq = _root(rq)
        targets.setdefault(tgt, []).append(site_label(model, s))
        ctx_sets.append({r.key(): r for r in rq})
    ctx = []
    if ctx_sets:
        common = set(ctx_sets[0]).intersection(*ctx_sets[1:])
        ctx = [ctx_sets[0][k] for k in sorted(common, key=str)]

    firer_owner_labels = _upstream_owners(model, eid)
    reads, vars_read, provided = event_reads(model, ev)
    for k in loc_keys_of(ev):
        for m in LOC_SCOPE_RE.finditer(model.loc.get(k, "")):
            if m.group(1) in model.saved_scope and m.group(1) not in provided:
                reads.add(m.group(1))

    missing = []
    prereq = []        # state another definition must create first (for LIVE ROUTE)
    numeric = {r.name for r in own if r.kind in ("varnum", "varcap", "varscope")}
    own = [r for r in own if not (r.kind == "varstate" and r.name in numeric)]
    story_names = {r.name for r in own + ctx if r.kind == "story"}
    for r in own:
        if r.kind == "story":
            creators = [lab for lab, _, _ in model.story_creators.get(r.name, [])]
            missing.append("needs story %s running (created by %s)"
                           % (r.name, _short(creators) if creators else "nothing in script"))
        elif r.kind == "varscope":
            missing.append("needs var:%s (holds a character or flag), set by %s"
                           % (r.name, _short(model.set_var.get(r.name, ())) or "nothing in script"))
            prereq.append("var:%s (%s)" % (r.name, _short(model.set_var.get(r.name, ()), 2)))
        elif r.kind == "flag":
            setters = model.set_flag.get(r.name, set())
            if setters:
                missing.append("needs flag %s, set by %s" % (r.name, _short(setters)))
                prereq.append("flag %s (%s)" % (r.name, _short(setters, 2)))
        elif r.kind == "varstate":
            missing.append("needs variable %s, set by %s"
                           % (r.name, _short(model.set_var.get(r.name, ())) or "nothing in script"))
            prereq.append("variable %s (%s)" % (r.name, _short(model.set_var.get(r.name, ()), 2)))
    for name in sorted(reads):
        if name in ENGINE_SCOPES:
            if name == "story" and story_names:
                continue
            missing.append("needs " + ENGINE_SCOPES[name])
            continue
        missing.append("needs scope:%s, saved by %s" % (name, _savers(model, name,
                                                                     firer_owner_labels)))
    if not story_names:
        story_vars = sorted(v for v in vars_read
                            if model.var_kinds.get(v) == {"story"})
        for v in story_vars:
            missing.append("reads story variable var:%s, set by %s"
                           % (v, _short(model.set_var.get(v, ()))))

    # guarded reads (`scope:x ?= …`) of a scope the event does not save: fired
    # cold it runs, but its text or branch falls back (FIX 9a)
    for name in sorted(model.__dict__.get("_last_guarded", set()) - provided - reads):
        if name in model.saved_scope:
            own.append(Req("note", name, "reads scope:%s if present (saved by %s); fired cold, "
                           "its text falls back" % (name, _savers(model, name,
                                                                  firer_owner_labels)),
                           order=95, default=True))
    setup_own = [r for r in own if r.console or r.kind == "note"]
    setup_ctx = [r for r in ctx if (r.console or r.kind == "note")
                 and r.key() not in {o.key() for o in own}]
    if missing:
        status = "no"
    elif any(not r.default for r in setup_own):
        status = "setup"
    else:
        status = "yes"

    def lines(reqs):
        out = []
        hinted = set()
        for r in _dedupe(reqs):
            if r.console and r.scope:
                out.append(("console", scoped_console(r.scope, r.console)))
            elif r.console:
                out.append(("console", r.console))
            elif r.kind == "note":
                out.append(("note", ("on %s: " % r.scope if r.scope else "") + r.human))
            elif r.kind == "varcap":
                out.append(("note", ("on %s: " % r.scope if r.scope else "") +
                            "keep %s" % r.human))
            dec = model.debug_vars.get(r.name) if r.scope else None
            if dec and dec not in hinted:
                hinted.add(dec)
                out.append(("note", "or take the debug decision '%s' (%s), which sets %s"
                            % (_plain(model.loc.get(dec, dec)), dec, r.name)))
        scopes = sorted({r.scope for r in reqs if r.scope and r.console and
                         _title_placeholder(r.scope) == TITLE_PLACEHOLDER})
        for sc in scopes:
            out.insert(0, ("note", "%s: the county the event is about (%s); your capital "
                                   "Region is capital_county, any other is title:<c_key>"
                           % (TITLE_PLACEHOLDER, sc)))
        return out

    setup = lines(setup_own)
    setup_rec = [x for x in lines(setup_ctx) if x not in setup]
    # a "<county>:" header only where a <county> line is left, and only once
    if not any(k == "console" and TITLE_PLACEHOLDER in t for k, t in setup_rec):
        setup_rec = [x for x in setup_rec if not x[1].startswith(TITLE_PLACEHOLDER + ":")]
    elif any(t.startswith(TITLE_PLACEHOLDER + ":") for _, t in setup):
        setup_rec = [x for x in setup_rec if not x[1].startswith(TITLE_PLACEHOLDER + ":")]
    # one initiate line, before anything that needs it
    for lst in (setup, setup_rec):
        if ("console", INITIATE) in lst:
            lst.remove(("console", INITIATE))
            if ("console", INITIATE) not in setup or lst is setup:
                lst.insert(0, ("console", INITIATE))

    others = [t for t in targets if t != "root"]
    fire = "event %s" % eid
    fire_note = ""
    if others and "root" not in targets:
        fire = "event %s <character id>" % eid
        fire_note = ("script fires it on %s; if that is you, plain `event %s` works, "
                     "otherwise hover them for their id" % (" / ".join(others), eid))
    elif others:
        fire_note = "also fired on %s" % " / ".join(others)

    fired_by = sorted({lab for labs in targets.values() for lab in labs})
    return collections.OrderedDict([
        ("id", eid), ("file", rel), ("title", title_of(model, ev)),
        ("fire_cold", status), ("missing", missing),
        ("setup", [list(x) for x in setup]), ("setup_recommended", [list(x) for x in setup_rec]),
        ("fire", fire), ("fire_note", fire_note),
        ("fired_by", fired_by), ("hidden", hidden),
        ("live_route", ("" if status != "no" else
                        ("first get %s; then " % "; ".join(prereq) if prereq else "")
                        + live_route(model, eid))),
    ])


def all_recipes(model):
    return [recipe(model, eid) for eid in sorted(model.events, key=_event_sort)]


def _event_sort(eid):
    ns, num = eid.rsplit(".", 1)
    return (ns, int(num) if num.isdigit() else 0, num)


def group_of(rel):
    stem = os.path.splitext(os.path.basename(rel))[0]
    for i, (key, title) in enumerate(GROUPS):
        if stem.endswith("_" + key) or stem == key:
            return i, title
    return len(GROUPS), stem.replace("eotg_", "").replace("_", " ").title()


# ------------------------------------------------------------------ rendering
def _cell(s):
    return s.replace("|", "\\|").replace("\n", " ")


def _setup_cell(r):
    parts = []
    for kind, text in r["setup"]:
        parts.append("`%s`" % text if kind == "console" else _cell(text))
    if r["setup_recommended"]:
        rec = ["`%s`" % t if k == "console" else _cell(t) for k, t in r["setup_recommended"]]
        parts.append("*for realistic content (its usual context):* " + "<br>".join(rec))
    return "<br>".join(parts) or "—"


def _cold_cell(r):
    if r["fire_cold"] == "no":
        return "**no**: " + "<br>".join(_cell(m) for m in r["missing"])
    return {"yes": "yes", "setup": "after setup"}[r["fire_cold"]]


def _fired_cell(r):
    parts = [_cell(f) for f in r["fired_by"]] or ["nothing (L009)"]
    if r["hidden"]:
        parts.append("*hidden: runs silently, check its effects*")
    return "<br>".join(parts)


def render(recipes, root_label):
    groups = collections.OrderedDict()
    for r in recipes:
        groups.setdefault(group_of(r["file"]), []).append(r)
    order = sorted(groups)
    total = collections.Counter(r["fire_cold"] for r in recipes)
    L_ = ["# Console recipes: every mod event (generated)", "",
          "> **Generated by `docs/tools/gen_test_recipes.py`. Do not edit by hand.** Re-run the "
          "tool after any event change; `python docs/tools/gen_test_recipes.py --check` says "
          "whether this file is current.", "",
          "## How to use this", "",
          "- Set up the game first: [HOW_TO_TEST_IN_GAME.md](../HOW_TO_TEST_IN_GAME.md) §1 "
          "(debug mode, one playset, restart after a batch). The console commands below follow "
          "its §2.",
          "- **Fire cold**: *yes* means `event <id>` works as is. *after setup* means type the "
          "SETUP lines first (the event's own trigger needs them). **no** means the event needs "
          "something only play creates (a saved scope, a running story, state set by another "
          "event); the cell says exactly what, and LIVE ROUTE says how to get there.",
          "- **Setup** lines in `code` are console commands, in the order given; plain text is "
          "what you have to arrange yourself. *For realistic content* lines come from the "
          "event's usual firing context (e.g. the tier its yearly pulse requires); the event "
          "fires without them but its text may not fit.",
          "- **Fire**: `event <id> <character id>` means the event fires on someone else (a "
          "knight, the heir, ...). Hover them in debug mode for their id.",
          "- Quick lookup for one event: `python docs/tools/gen_test_recipes.py --event <id>`.",
          "- This is derived from script, not from play. If a recipe is wrong, the event's "
          "trigger or firing path is unusual: tell the orchestrator, and fire it by its live "
          "route.", "",
          "## Summary", "",
          "| Group | File | Events | Fire cold | After setup | No (needs route) |",
          "|---|---|---|---|---|---|"]
    for g in order:
        rows = groups[g]
        c = collections.Counter(r["fire_cold"] for r in rows)
        files = sorted({r["file"] for r in rows})
        L_.append("| %s | %s | %d | %d | %d | %d |" % (
            g[1], ", ".join("`%s`" % f.split("/")[-1] for f in files), len(rows),
            c["yes"], c["setup"], c["no"]))
    L_.append("| **Total** | | **%d** | **%d** | **%d** | **%d** |" % (
        len(recipes), total["yes"], total["setup"], total["no"]))
    for g in order:
        L_ += ["", "## %s" % g[1], "",
               "| Event | Fire cold | Setup | Fire | Fired by | Live route |",
               "|---|---|---|---|---|---|"]
        for r in groups[g]:
            ev = "`%s`" % r["id"] + ("<br>%s" % _cell(r["title"]) if r["title"] else "")
            fire = "`%s`" % r["fire"] + ("<br>%s" % _cell(r["fire_note"]) if r["fire_note"]
                                         else "")
            L_.append("| %s | %s | %s | %s | %s | %s |" % (
                ev, _cold_cell(r), _setup_cell(r), fire, _fired_cell(r),
                _cell(r["live_route"]) or "—"))
    L_.append("")
    return "\n".join(L_)


def render_one(r):
    out = ["%s  %s" % (r["id"], r["title"]), "file:       %s" % r["file"],
           "fire cold:  %s" % {"yes": "yes", "setup": "after setup", "no": "NO"}[r["fire_cold"]]]
    out += ["  - %s" % m for m in r["missing"]]
    out.append("setup:")
    for k, t in r["setup"] or [("note", "none")]:
        out.append("  %s%s" % ("" if k == "console" else "# ", t))
    if r["setup_recommended"]:
        out.append("for realistic content:")
        for k, t in r["setup_recommended"]:
            out.append("  %s%s" % ("" if k == "console" else "# ", t))
    out.append("fire:       %s%s" % (r["fire"], ("   # " + r["fire_note"]) if r["fire_note"]
                                     else ""))
    out.append("fired by:")
    out += ["  - %s" % f for f in r["fired_by"]] or ["  - nothing"]
    if r["hidden"]:
        out.append("  (hidden: runs silently, check its effects)")
    if r["live_route"]:
        out.append("live route: %s" % r["live_route"])
    return "\n".join(out)


def generate(root):
    model = Model(root)
    recipes = all_recipes(model)
    return recipes, render(recipes, root)


def main(argv=None):
    P.utf8_console()
    ap = argparse.ArgumentParser(description="Console test recipe for every mod event.")
    ap.add_argument("--root", default=DEFAULT_ROOT, help="mod checkout (default: this repo)")
    ap.add_argument("--out", help="output file (default: <root>/%s)" % OUT_REL)
    ap.add_argument("--check", action="store_true", help="exit 1 if the output file is stale")
    ap.add_argument("--event", help="print one event's recipe to stdout")
    ap.add_argument("--json", metavar="FILE", help="also write every row as JSON")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    out = os.path.abspath(args.out) if args.out else os.path.join(root, *OUT_REL.split("/"))
    recipes, text = generate(root)
    if args.event:
        hit = [r for r in recipes if r["id"] == args.event]
        if not hit:
            print("no event %s in %s" % (args.event, root), file=sys.stderr)
            return 2
        print(render_one(hit[0]))
        return 0
    if args.json:
        with open(args.json, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(recipes, fh, indent=1)
            fh.write("\n")
    if args.check:
        cur = ""
        if os.path.exists(out):
            with open(out, "rb") as fh:
                cur = fh.read().decode("utf-8").replace("\r\n", "\n")
        ok = cur == text
        c = collections.Counter(r["fire_cold"] for r in recipes)
        print("console recipes %s: %d events, %d fire cold, %d after setup, %d need a route (%s)"
              % ("are current" if ok else "are STALE", len(recipes), c["yes"], c["setup"],
                 c["no"], out))
        return 0 if ok else 1
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    c = collections.Counter(r["fire_cold"] for r in recipes)
    print("wrote %s: %d events, %d fire cold, %d after setup, %d need a route"
          % (out, len(recipes), c["yes"], c["setup"], c["no"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
