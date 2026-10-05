"""Static linter for the Echoes of the Grip mod. Python 3, standard library only.

    python docs/tools/eotg_lint.py [paths ...] [--rule L005] [--json out.json]
                                   [--baseline docs/tools/eotg_lint_baseline.json]
                                   [--write-baseline FILE] [--root REPO]

The whole mod tree is always loaded (several rules are cross-file); ``paths``
only filter which files findings are reported for. Exit status is 1 when a
finding is not covered by the baseline (or, with no baseline, when there is
any finding), 0 otherwise. Rules and their CK3 rationale: eotg_lint.md.
"""
import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx_parse  # noqa: E402
import textio  # noqa: E402

ERROR = "ERROR"
WARNING = "WARNING"

RULES = {
    "L000": (WARNING, "script file does not parse cleanly"),
    "L001": (ERROR, "mod-defined identifier without the eotg_ prefix"),
    "L002": (ERROR, "v1 title key form eotg_[ekdcb]_ (must be tier-first)"),
    "L003": (ERROR, "localization file problem (BOM, header, [scope:, duplicate key)"),
    "L004": (ERROR, "dead or non-additive vanilla on_action hook"),
    "L005": (WARNING, "unguarded removal on a visible path"),
    "L006": (WARNING, "raw flag/variable check shown as a decision requirement"),
    "L007": (WARNING, "event option whose only effects are deferred (shows an empty tooltip)"),
    "L008": (ERROR, "skill effect without the _skill suffix"),
    "L009": (WARNING, "event defined but never fired"),
    "L010": (ERROR, "loc key referenced but not defined"),
    "L011": (WARNING, "single named character referred to as they/them (house rule: gendered)"),
    "L012": (ERROR, "cybernetics loc: never-name (ERROR) or register word to triage (WARNING)"),
    "L013": (WARNING, "loc house style: dash, non-Canadian spelling, stray space, appended desc without \\n\\n"),
    "L014": (WARNING, "eotg_ loc key defined but never referenced"),
    "L016": (ERROR, "BOM (U+FEFF) anywhere but byte 0: a stacked or mid-file BOM"),
}

SCRIPT_DIRS = ("common", "events")
TEXT_SCAN_DIRS = ("common", "events", "history", "localization", "map_data", "gfx")
TEXT_SCAN_EXT = (".txt", ".yml", ".gui", ".csv", ".mod", ".asset")

# L016: every mod text file has at most one BOM, at byte 0 (docs/pitfalls.md §14)
BOM_SCAN_DIRS = ("common", "events", "localization", "history", "docs/test_map")
BOM_SCAN_EXT = (".txt", ".yml", ".mod", ".csv", ".settings", ".gui")

# common/<dir> whose top-level keys are mod-defined identifiers (L001)
DEFINITION_DIRS = {
    "scripted_effects": "scripted effect",
    "scripted_triggers": "scripted trigger",
    "modifiers": "static modifier",
    "opinion_modifiers": "opinion modifier",
    "decisions": "decision",
    "traits": "trait",
    "story_cycles": "story cycle",
    "script_values": "script value",
    "deathreasons": "death reason",
    "scripted_character_templates": "character template",
}
FLAG_SETTERS = re.compile(r"^(add|set)_\w*flag$")
FLAG_SETTER_EXCLUDE = {"add_internal_flag"}
VAR_SETTERS = {"set_variable", "set_global_variable", "add_to_variable_list",
               "add_to_global_variable_list"}

EVENT_ID_RE = re.compile(r"^[A-Za-z_][\w]*\.\d+$")
TITLE_RE = re.compile(r"eotg_[ekdcb]_")
LOC_KEY_RE = re.compile(r'^\s+([^\s:#"]+):\d*\s*"')
SKILL_BARE = {"add_diplomacy", "add_martial", "add_stewardship", "add_intrigue",
              "add_learning", "add_prowess"}
DEAD_HOOKS = {"on_yearly_playable"}

# L005
REMOVALS = {"remove_character_modifier": "has_character_modifier",
            "remove_trait": "has_trait",
            "remove_opinion": "has_opinion_modifier"}
HIDING_BLOCKS = {"hidden_effect", "custom_tooltip", "custom_description"}

# L006
# is_shown is NOT here: a failed is_shown hides the decision, so nothing renders
L006_BLOCKS = ("is_valid", "is_valid_showing_failures_only")
L006_KEYS = {"has_character_flag", "has_variable", "has_global_variable"}
L006_WRAPPERS = {"custom_description", "custom_tooltip"}

# L007
OPTION_META = {"name", "trigger", "trait", "skill", "ai_chance", "highlight_portrait",
               "flavor", "show_as_unavailable", "fallback", "exclusive", "clicksound",
               "add_internal_flag", "reason", "is_cancel_option", "#"}
SILENT_EFFECTS = {
    "trigger_event", "hidden_effect",
    "add_character_flag", "remove_character_flag", "set_global_flag", "remove_global_flag",
    "add_dynasty_flag", "remove_dynasty_flag", "add_house_flag", "remove_house_flag",
    "set_variable", "change_variable", "remove_variable", "clamp_variable",
    "set_global_variable", "change_global_variable", "remove_global_variable",
    "clamp_global_variable",
    "set_local_variable", "change_local_variable", "remove_local_variable",
    "add_to_variable_list", "remove_list_variable", "clear_variable_list",
    "add_to_global_variable_list", "remove_list_global_variable",
    "add_to_local_variable_list", "add_to_list", "add_to_temporary_list",
    "save_scope_as", "save_temporary_scope_as", "save_scope_value_as",
    "save_temporary_scope_value_as",
    "create_story", "end_story", "make_story_owner",
}
CONTAINER_KEYS = {"if", "else_if", "else", "while", "random", "random_list",
                  "root", "prev", "this", "switch", "trigger_if", "trigger_else"}
CONTAINER_PREFIX = ("scope:", "every_", "random_", "ordered_", "var:")
NON_EFFECT_IN_CONTAINER = {"limit", "trigger", "weight", "modifier", "count",
                           "max", "min", "order_by", "position", "check_range_bounds",
                           "chance", "base", "alternative_limit", "value", "#"}
TOOLTIP_KEYS = {"custom_tooltip", "custom_description", "custom_description_no_bullet",
                "show_as_tooltip", "send_interface_toast", "send_interface_message"}

# L009: blocks whose bare items / values fire events
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(os.path.dirname(HERE))
ALLOWLIST = os.path.join(HERE, "eotg_lint_loc_allowlist.txt")
PRONOUN_ALLOWLIST = os.path.join(HERE, "eotg_lint_pronoun_allowlist.txt")
REGISTER_FILE = os.path.join(HERE, "eotg_lint_register.json")
STYLE_FILE = os.path.join(HERE, "eotg_lint_style.json")
CONVENTIONS_FILE = os.path.join(HERE, "eotg_lint_loc_conventions.json")


class Finding:
    __slots__ = ("rule", "severity", "file", "line", "message")

    def __init__(self, rule, file, line, message, severity=None):
        self.rule = rule
        self.severity = severity or RULES[rule][0]
        self.file = file
        self.line = line
        self.message = message

    def key(self):
        return (self.rule, self.file, self.message)

    def as_dict(self):
        return {"rule": self.rule, "severity": self.severity, "file": self.file,
                "line": self.line, "message": self.message}

    def __str__(self):
        return "%s:%d: %s %s %s" % (self.file, self.line, self.severity, self.rule, self.message)


def _rel(root, path):
    return os.path.relpath(path, root).replace(os.sep, "/")


def _iter_files(root, top, exts):
    base = os.path.join(root, top)
    if not os.path.isdir(base):
        return
    for d, dirs, files in os.walk(base):
        dirs.sort()
        for f in sorted(files):
            if f.lower().endswith(exts):
                yield os.path.join(d, f)


def _str_value(node):
    return node.value if isinstance(node.value, str) else None


class Mod:
    """The loaded mod tree: parsed script and raw loc."""

    def __init__(self, root):
        self.root = os.path.abspath(root)
        self.docs = {}      # rel -> Document
        self.findings = []
        for top in SCRIPT_DIRS:
            for f in _iter_files(self.root, top, (".txt",)):
                rel = _rel(self.root, f)
                doc = pdx_parse.parse_file(f)
                self.docs[rel] = doc
                for line, msg in doc.errors:
                    self.findings.append(Finding("L000", rel, line, msg))
        self.loc_files = [_rel(self.root, f) for f in
                          _iter_files(self.root, "localization", (".yml",))]
        self.loc = collections.defaultdict(dict)   # lang -> key -> (rel, line)
        self.skipped = collections.defaultdict(list)   # rule -> [what was not checked]

    # --- helpers
    def files_in(self, prefix):
        return [(r, d) for r, d in sorted(self.docs.items()) if r.startswith(prefix)]

    def common_dir(self, name):
        return self.files_in("common/%s/" % name)

    def events(self):
        """[(rel, event_id, node)] for every event definition."""
        out = []
        for rel, doc in self.files_in("events/"):
            for n in doc.nodes:
                if n.is_block and n.key and EVENT_ID_RE.match(n.key):
                    out.append((rel, n.key, n))
        return out

    def scripted_effects(self):
        out = {}
        for rel, doc in self.common_dir("scripted_effects"):
            for n in doc.nodes:
                if n.is_block and n.key:
                    out[n.key] = n
        return out


# ------------------------------------------------------------------ rules
def rule_l001(mod):
    out = []
    for rel, doc in mod.files_in("events/"):
        for n in doc.nodes:
            if n.key == "namespace" and isinstance(n.value, str) \
                    and not n.value.startswith("eotg_"):
                out.append(Finding("L001", rel, n.line,
                                   "event namespace '%s' lacks eotg_ prefix" % n.value))
    for d, what in sorted(DEFINITION_DIRS.items()):
        for rel, doc in mod.common_dir(d):
            for n in doc.nodes:
                if n.key is None or n.key.startswith("@") or n.key == "#":
                    continue
                if not n.key.startswith("eotg_"):
                    out.append(Finding("L001", rel, n.line,
                                       "%s '%s' lacks eotg_ prefix" % (what, n.key)))
    # custom on_actions: top-level on_action keys referenced in some on_actions = { }
    called = set()
    for rel, doc in mod.docs.items():
        for n, _ in pdx_parse.walk(doc.nodes):
            if n.key == "on_actions" and n.is_block:
                called |= {c.key for c in n.value if c.is_bare}
            if n.key == "on_action" and isinstance(n.value, str):
                called.add(n.value)
    for rel, doc in mod.common_dir("on_action"):
        for n in doc.nodes:
            if n.key in called and not n.key.startswith("eotg_"):
                out.append(Finding("L001", rel, n.line,
                                   "custom on_action '%s' lacks eotg_ prefix" % n.key))
    # flags and variables set anywhere
    for rel, doc in sorted(mod.docs.items()):
        for n, _ in pdx_parse.walk(doc.nodes):
            name = None
            kind = None
            if n.key and FLAG_SETTERS.match(n.key) and n.key not in FLAG_SETTER_EXCLUDE:
                kind = "flag"
                if isinstance(n.value, str):
                    name = n.value
                elif n.is_block:
                    f = pdx_parse.first(n.value, "flag")
                    name = f and _str_value(f)
            elif n.key in VAR_SETTERS:
                kind = "variable"
                if isinstance(n.value, str):
                    name = n.value
                elif n.is_block:
                    f = pdx_parse.first(n.value, "name")
                    name = f and _str_value(f)
            if name and not name.startswith("eotg_") and "$" not in name \
                    and ":" not in name and not name.startswith("@"):
                out.append(Finding("L001", rel, n.line,
                                   "%s '%s' (via %s) lacks eotg_ prefix" % (kind, name, n.key)))
    return out


def rule_l002(mod):
    out = []
    for top in TEXT_SCAN_DIRS:
        for f in _iter_files(mod.root, top, TEXT_SCAN_EXT):
            rel = _rel(mod.root, f)
            text, _ = pdx_parse.read_text(f)
            for i, line in enumerate(text.splitlines(), 1):
                for m in TITLE_RE.finditer(line):
                    tail = re.match(r"[\w]*", line[m.start():]).group(0)
                    out.append(Finding("L002", rel, i,
                                       "v1 title key '%s' (use tier-first e_eotg_/k_eotg_/...)" % tail))
    return out


def rule_l003(mod):
    out = []
    seen = collections.defaultdict(dict)    # lang -> key -> (rel, line)
    # base files before replace/ so the "first definition" is stable and readable
    order = sorted(mod.loc_files, key=lambda r: ("/replace/" in r, r))
    for rel in order:
        path = os.path.join(mod.root, rel)
        with open(path, "rb") as fh:
            raw = fh.read()
        if not raw.startswith(b"\xef\xbb\xbf"):
            out.append(Finding("L003", rel, 1, "missing UTF-8 BOM"))
        m = re.search(r"_l_(\w+)\.yml$", rel)
        lang = m.group(1) if m else "english"
        text, _ = textio.decode(raw)
        lines = text.splitlines()
        header = None
        for i, line in enumerate(lines, 1):
            s = line.strip()
            if s and not s.startswith("#"):
                header = (i, s)
                break
        want = "l_%s:" % lang
        if header is None or header[1] != want:
            out.append(Finding("L003", rel, header[0] if header else 1,
                               "first line must be '%s' (found %r)" % (want, header and header[1])))
        for i, line in enumerate(lines, 1):
            code = line.split("#", 1)[0] if '"' not in line else line
            if "[scope:" in code:
                out.append(Finding("L003", rel, i,
                                   "'[scope:' in loc (use bare [x.GetName])"))
            km = LOC_KEY_RE.match(line)
            if km:
                k = km.group(1)
                if k in seen[lang]:
                    prev = seen[lang][k]
                    out.append(Finding("L003", rel, i,
                                       "duplicate loc key '%s' (first defined in %s:%d)"
                                       % (k, prev[0], prev[1])))
                else:
                    seen[lang][k] = (rel, i)
    mod.loc = seen
    return out


def bom_scan_files(root):
    """L016's files: BOM_SCAN_DIRS recursively, plus descriptor-type files at the root."""
    for top in BOM_SCAN_DIRS:
        yield from _iter_files(root, top, BOM_SCAN_EXT)
    for f in sorted(os.listdir(root)):
        p = os.path.join(root, f)
        if os.path.isfile(p) and f.lower().endswith(BOM_SCAN_EXT):
            yield p


def rule_l016(mod):
    """A second BOM right after the first (EF BB BF EF BB BF): CK3 strips one and reads
    the next as part of the first key, which in common/script_values/ broke every named
    value in the game. A BOM mid-file is a pasted-in file. Reported by byte offset."""
    out = []
    for f in bom_scan_files(mod.root):
        with open(f, "rb") as fh:
            raw = fh.read()
        offsets = textio.stray_bom_offsets(raw)
        if not offsets:
            continue
        rel = _rel(mod.root, f)
        lead = 0
        while raw.startswith(textio.BOM * (lead + 1)):
            lead += 1
        if lead > 1:
            out.append(Finding("L016", rel, 1, "file starts with %d stacked BOMs (bytes 0-%d); "
                               "keep exactly one" % (lead, 3 * lead - 1)))
        for off in offsets:
            if off < 3 * lead:
                continue
            out.append(Finding("L016", rel, raw.count(b"\n", 0, off) + 1,
                               "BOM at byte %d (only byte 0 may hold one)" % off))
    return out


def rule_l004(mod):
    out = []
    for rel, doc in mod.common_dir("on_action"):
        for n in doc.nodes:
            if n.key in DEAD_HOOKS:
                out.append(Finding("L004", rel, n.line,
                                   "'%s' is not a real hook; use yearly_playable_pulse" % n.key))
            if n.is_block and n.key and not n.key.startswith("eotg_"):
                for c in n.value:
                    if c.key in ("effect", "trigger") and c.is_block:
                        out.append(Finding(
                            "L004", rel, c.line,
                            "top-level '%s' in vanilla hook '%s' overwrites vanilla; "
                            "use on_actions = { } / events = { }" % (c.key, n.key)))
    return out


def _removal_target(n):
    if n.key == "remove_opinion":
        if n.is_block:
            m = pdx_parse.first(n.value, "modifier")
            return m and _str_value(m)
        return None
    if isinstance(n.value, str):
        return n.value
    if n.is_block:
        m = pdx_parse.first(n.value, "modifier") or pdx_parse.first(n.value, "trait")
        return m and _str_value(m)
    return None


def _limit_checks(limit_node, check_key, target):
    for c, _ in pdx_parse.walk(limit_node.value if limit_node.is_block else []):
        if c.key != check_key:
            continue
        if isinstance(c.value, str) and c.value == target:
            return True
        if c.is_block:
            m = pdx_parse.first(c.value, "modifier")
            if m and _str_value(m) == target:
                return True
    return False


def _guarded(parents, check_key, target):
    for p in parents:
        if p.key in HIDING_BLOCKS:
            return True
        if p.is_block:
            for lim in pdx_parse.find(p.value, "limit"):
                if _limit_checks(lim, check_key, target):
                    return True
            # random_list entry `10 = { trigger = { has_trait = X } remove_trait = X }`:
            # an entry whose trigger fails gets weight 0 (UNVERIFIED-VANILLA: and is
            # left out of the tooltip)
            if p.key and p.key.isdigit():
                for trg in pdx_parse.find(p.value, "trigger"):
                    if _limit_checks(trg, check_key, target):
                        return True
    return False


def _visible_roots(mod):
    """(rel, label, node) blocks whose effects show in a tooltip."""
    for rel, eid, ev in mod.events():
        if any(c.key == "hidden" and c.value == "yes" for c in ev.value):
            continue
        for opt in pdx_parse.find(ev.value, "option"):
            yield rel, "%s option" % eid, opt
    for rel, doc in mod.common_dir("decisions"):
        for d in doc.nodes:
            if d.is_block:
                for eff in pdx_parse.find(d.value, "effect"):
                    yield rel, "decision %s" % d.key, eff
    for rel, doc in mod.common_dir("scripted_effects"):
        for se in doc.nodes:
            if se.is_block:
                yield rel, "scripted effect %s" % se.key, se
    for rel, doc in mod.common_dir("character_interactions"):
        for ia in doc.nodes:
            if ia.is_block:
                for k in ("on_accept", "on_send", "on_auto_accept"):
                    for b in pdx_parse.find(ia.value, k):
                        yield rel, "interaction %s" % ia.key, b


def rule_l005(mod):
    out = []
    for rel, label, root in _visible_roots(mod):
        for n, parents in pdx_parse.walk(root.value, (root,)):
            if n.key not in REMOVALS:
                continue
            target = _removal_target(n)
            if not target:
                continue
            if not _guarded(parents, REMOVALS[n.key], target):
                out.append(Finding("L005", rel, n.line,
                                   "%s = %s in %s is not inside an if/limit checking %s "
                                   "(or hidden_effect)" % (n.key, target, label, REMOVALS[n.key])))
    return out


def rule_l006(mod):
    out = []
    for rel, doc in mod.common_dir("decisions"):
        for d in doc.nodes:
            if not d.is_block:
                continue
            for blk in d.value:
                if blk.key not in L006_BLOCKS or not blk.is_block:
                    continue
                for n, parents in pdx_parse.walk(blk.value, (blk,)):
                    if n.key in L006_KEYS and not any(p.key in L006_WRAPPERS for p in parents):
                        out.append(Finding(
                            "L006", rel, n.line,
                            "%s = %s in %s of %s renders as a raw requirement; wrap it in "
                            "custom_description" % (n.key, n.value if isinstance(n.value, str)
                                                    else "{...}", blk.key, d.key)))
    return out


# L007: an option whose consequence only arrives later (an event, a story, a scheme)
DEFERRED_EFFECTS = {"trigger_event", "create_story", "start_scheme"}
# bookkeeping that passes scopes along; neither a consequence nor a hidden resource
NEUTRAL_EFFECTS = {"save_scope_as", "save_temporary_scope_as", "save_scope_value_as",
                   "save_temporary_scope_value_as"}


class _Deferral:
    """Classify an effect node: 'deferred' | 'neutral' | 'other'.

    Containers (if/else, hidden_effect, random_list entries, scope switches,
    list builders) and mod scripted effects take the kind of their contents:
    any 'other' -> other; else any 'deferred' -> deferred; else neutral.
    Hidden resource moves (flags, variables, eotg_add_fracture_risk...) are
    'other': the hidden-risk design keeps them silent on purpose.
    """

    def __init__(self, mod):
        self.effects = mod.scripted_effects()
        self.memo = {}

    @staticmethod
    def combine(kinds):
        kinds = list(kinds)
        if "other" in kinds:
            return "other"
        return "deferred" if "deferred" in kinds else "neutral"

    def node(self, n, depth=0):
        if n.key in DEFERRED_EFFECTS:
            return "deferred"
        if n.key in NEUTRAL_EFFECTS:
            return "neutral"
        if n.key in TOOLTIP_KEYS:
            return "other"
        if n.key in self.effects and depth < 20:
            return self.effect(n.key, depth)
        if not n.is_block:
            return "other"
        is_container = (n.key in CONTAINER_KEYS or n.key == "hidden_effect" or n.key is None
                        or n.key.isdigit() or n.key.startswith(CONTAINER_PREFIX))
        if is_container:
            return self.block(n.value, depth + 1)
        return "other"

    def block(self, nodes, depth=0):
        eff = [c for c in nodes if c.key not in NON_EFFECT_IN_CONTAINER]
        return self.combine(self.node(c, depth) for c in eff)

    def effect(self, name, depth):
        if name not in self.memo:
            self.memo[name] = "other"    # cycle guard
            self.memo[name] = self.block(self.effects[name].value, depth + 1)
        return self.memo[name]


def rule_l007(mod):
    out = []
    cls = _Deferral(mod)
    for rel, eid, ev in mod.events():
        if any(c.key == "hidden" and c.value == "yes" for c in ev.value):
            continue
        options = pdx_parse.find(ev.value, "option")
        if len(options) < 2:
            continue
        for opt in options:
            effects = [c for c in opt.value if c.key not in OPTION_META]
            if not effects:
                continue
            if any(n.key in TOOLTIP_KEYS for n, _ in pdx_parse.walk(opt.value)):
                continue
            if cls.block(effects) == "deferred":
                nm = pdx_parse.first(opt.value, "name")
                label = _str_value(nm) if nm else "?"
                out.append(Finding("L007", rel, opt.line,
                                   "option %s of %s only defers its consequence (%s) and has no "
                                   "custom_tooltip; it looks identical to a do-nothing option"
                                   % (label, eid, ", ".join(sorted({c.key for c in effects})))))
    return out


def rule_l008(mod):
    out = []
    for rel, doc in sorted(mod.docs.items()):
        for n, _ in pdx_parse.walk(doc.nodes):
            if n.key in SKILL_BARE:
                out.append(Finding("L008", rel, n.line,
                                   "'%s' should be '%s_skill'" % (n.key, n.key)))
    return out


FOLDER_KINDS = (("events/", "event"), ("common/on_action/", "on_action"),
                ("common/decisions/", "decision"), ("common/story_cycles/", "story"),
                ("common/scripted_effects/", "effect"),
                ("common/character_interactions/", "interaction"),
                ("common/schemes/", "scheme"), ("common/activities/", "activity"))


class FireSite:
    """One place that references (fires) an event: the event-graph edge.

    kind/owner name the top-level definition that holds the reference
    (event, on_action, decision, story, effect, ...); parents are the blocks
    from that definition down to ``node`` (the definition first)."""
    __slots__ = ("event", "rel", "line", "kind", "owner", "parents", "node")

    def __init__(self, event, rel, line, kind, owner, parents, node):
        self.event, self.rel, self.line = event, rel, line
        self.kind, self.owner, self.parents, self.node = kind, owner, parents, node


def file_kind(rel):
    for prefix, kind in FOLDER_KINDS:
        if rel.startswith(prefix):
            return kind
    return rel.split("/")[1] if rel.startswith("common/") else rel.split("/")[0]


def fire_sites(mod):
    """{event_id: [FireSite]} for every reference to a defined event outside its
    own definition (a string value or a bare list item equal to the id)."""
    defined = {eid for _, eid, _ in mod.events()}
    sites = collections.defaultdict(list)
    for rel, doc in sorted(mod.docs.items()):
        kind = file_kind(rel)
        for top in doc.nodes:
            own = top.key if (top.key in defined and rel.startswith("events/")) else None
            for n, parents in pdx_parse.walk([top]):
                if n is top and own:
                    continue
                cand = []
                if isinstance(n.value, str):
                    cand.append(n.value)
                if n.is_bare:
                    cand.append(n.key)
                for c in cand:
                    if c in defined and c != own:
                        sites[c].append(FireSite(c, rel, n.line, kind, top.key, parents, n))
    return sites


def rule_l009(mod):
    out = []
    sites = fire_sites(mod)
    for rel, eid, node in sorted(mod.events(), key=lambda e: e[1]):
        if eid not in sites:
            out.append(Finding("L009", rel, node.line,
                               "event %s is defined but nothing fires it" % eid))
    return out


def _loc_refs_in(node, acc):
    """Collect loc keys from desc/title/name values, recursing through
    first_valid / triggered_desc / random_valid and skipping trigger/limit."""
    if isinstance(node.value, str):
        acc.append((node.value, node.line))
        return
    for c in node.children:
        if c.key in ("trigger", "limit"):
            continue
        if c.key in ("desc", "title", "name") or c.key in ("first_valid", "triggered_desc",
                                                           "random_valid"):
            _loc_refs_in(c, acc)


def _looks_like_key(v):
    return v and " " not in v and "[" not in v and "$" not in v and not v.startswith("@")


def load_allowlist(path=ALLOWLIST):
    keys = set()
    if os.path.exists(path):
        for line in textio.read_lines(path):
            s = line.split("#", 1)[0].strip()
            if s:
                keys.add(s)
    return keys


def rule_l010(mod, allowlist=None):
    if not mod.loc:
        rule_l003(mod)
    known = set(mod.loc.get("english", {}))
    allow = load_allowlist() if allowlist is None else allowlist
    refs = []   # (rel, line, key, what)
    for rel, eid, ev in mod.events():
        for c in ev.value:
            if c.key in ("title", "desc"):
                acc = []
                _loc_refs_in(c, acc)
                refs += [(rel, ln, k, "%s %s" % (eid, c.key)) for k, ln in acc]
        for opt in pdx_parse.find(ev.value, "option"):
            for c in pdx_parse.find(opt.value, "name"):
                acc = []
                _loc_refs_in(c, acc)
                refs += [(rel, ln, k, "%s option name" % eid) for k, ln in acc]
    for rel, doc in mod.common_dir("decisions"):
        for d in doc.nodes:
            if not d.is_block:
                continue
            for fld, implied in (("title", d.key), ("desc", d.key + "_desc"),
                                 ("selection_tooltip", None), ("confirm_text", None)):
                nodes = pdx_parse.find(d.value, fld)
                if nodes:
                    for c in nodes:
                        acc = []
                        _loc_refs_in(c, acc)
                        refs += [(rel, ln, k, "decision %s %s" % (d.key, fld)) for k, ln in acc]
                elif implied:
                    refs.append((rel, d.line, implied, "decision %s implied %s" % (d.key, fld)))
    for rel, doc in mod.common_dir("traits"):
        for t in doc.nodes:
            if not t.is_block or t.key.startswith("@"):
                continue
            for fld, implied in (("name", "trait_" + t.key), ("desc", "trait_%s_desc" % t.key)):
                nodes = pdx_parse.find(t.value, fld)
                if nodes:
                    for c in nodes:
                        acc = []
                        _loc_refs_in(c, acc)
                        refs += [(rel, ln, k, "trait %s %s" % (t.key, fld)) for k, ln in acc]
                else:
                    refs.append((rel, t.line, implied, "trait %s implied %s" % (t.key, fld)))
    for rel, doc in mod.common_dir("modifiers"):
        for m in doc.nodes:
            if m.is_block and m.key and not m.key.startswith("@"):
                refs.append((rel, m.line, m.key, "modifier %s name" % m.key))
                refs.append((rel, m.line, m.key + "_desc", "modifier %s desc" % m.key))
    out = []
    for rel, line, key, what in refs:
        if not _looks_like_key(key):
            continue
        if key in known or key in allow:
            continue
        out.append(Finding("L010", rel, line, "loc key '%s' (%s) is not defined" % (key, what)))
    return out


# ------------------------------------------------------------------ loc text rules
LOC_VALUE_RE = re.compile(r'^\s+([^\s:#"]+):\d*\s*"(.*)"\s*(#.*)?$')
CHAR_NAME_FUNCS = ("GetName", "GetFirstName", "GetFirstNameNicknamed", "GetFullName",
                   "GetTitledFirstName", "GetTitledFirstNameNoTooltip", "GetFirstNameNoTooltip",
                   "GetNameNoTooltip", "GetShortUIName", "GetUIName", "GetFullNameNicknamed")
CHAR_REF_RE = re.compile(r"\[([A-Za-z_][\w.:]*?)\.(%s)\b" % "|".join(CHAR_NAME_FUNCS))
GENDER_FUNC_RE = re.compile(r"\[[^\]]*\.Get(SheHe|HerHim|HerHis|HerselfHimself|HersHis|"
                            r"WomanMan|DaughterSon|WifeHusband|SisterBrother|MotherFather|"
                            r"GirlBoy|LadyLord|QueenKing)")
THEY_RE = re.compile(r"\b(they|them|their|themself|theirs)\b", re.I)


def _visible_text(value):
    """Loc value with [functions], $keys$, #formatting# and \\n removed."""
    v = re.sub(r"\[[^\]]*\]", " ", value)
    v = re.sub(r"\$[^$]*\$", " ", v)
    v = re.sub(r"#[A-Za-z_]+\s|#!", " ", v)
    return v.replace("\\n", " ")


def iter_loc_values(mod, pattern="*.yml"):
    """Yield (rel, line, key, value) for every loc entry."""
    import fnmatch
    for rel in sorted(mod.loc_files):
        if not fnmatch.fnmatch(os.path.basename(rel), pattern):
            continue
        text, _ = pdx_parse.read_text(os.path.join(mod.root, rel))
        for i, line in enumerate(text.splitlines(), 1):
            m = LOC_VALUE_RE.match(line)
            if m:
                yield rel, i, m.group(1), m.group(2)


def load_keylist(path):
    return load_allowlist(path)


def rule_l011(mod, allowlist=None):
    allow = load_keylist(PRONOUN_ALLOWLIST) if allowlist is None else allowlist
    out = []
    for rel, line, key, value in iter_loc_values(mod, "eotg_*.yml"):
        if key in allow:
            continue
        scopes = {m.group(1) for m in CHAR_REF_RE.finditer(value)}
        if len(scopes) != 1:
            continue
        if GENDER_FUNC_RE.search(value):
            continue
        words = sorted({w.lower() for w in THEY_RE.findall(_visible_text(value))})
        if words:
            scope = scopes.pop()
            out.append(Finding("L011", rel, line,
                               "%s names one character ([%s]) but uses %s; use [%s.GetSheHe] / "
                               "GetHerHim / GetHerHis (or allowlist the key if plural)"
                               % (key, scope, "/".join(words), scope)))
    return out


def load_register(path=REGISTER_FILE):
    data = json.loads(textio.read_text(path)[0])
    compiled = {"key_prefixes": tuple(data["key_prefixes"])}
    for sev in ("error", "warning"):
        compiled[sev] = [(t["term"], re.compile(t["regex"], 0 if t.get("case") else re.I),
                          t.get("source", "")) for t in data[sev]]
    return compiled


def rule_l012(mod, register=None):
    reg = load_register() if register is None else register
    out = []
    for rel, line, key, value in iter_loc_values(mod):
        if not key.startswith(reg["key_prefixes"]):
            continue
        text = _visible_text(value)
        for sev, severity in (("error", ERROR), ("warning", WARNING)):
            for term, rx, src in reg[sev]:
                if rx.search(text):
                    kind = "never-name" if sev == "error" else "register word (triage)"
                    out.append(Finding("L012", rel, line,
                                       "%s: %s '%s'%s" % (key, kind, term,
                                                         " (%s)" % src if src else ""),
                                       severity=severity))
    return out


# ------------------------------------------------------------------ L013 / L014
def load_style(path=STYLE_FILE):
    data = json.loads(textio.read_text(path)[0])
    sp = data["spelling"]

    def words(kind, entries):
        return [(re.compile(r"\b(%s)\b" % w["regex"], re.I), kind, w["canadian"]) for w in entries]
    return {
        "dashes": tuple(data["dashes"]["chars"]),
        # (regex, what the form is, the Canadian form); house standard: Canadian English
        "words": words("American spelling", sp["american_forms"])
        + words("British spelling", sp.get("british_forms_not_canadian", [])),
        "ise": re.compile(r"\b(%s)\b" % sp["ise_regex"], re.I),
        "ise_canadian": sp.get("ise_canadian", "-ize"),
        "ise_exceptions": {w.lower() for w in sp["ise_exceptions"]},
        "exceptions": list(sp.get("exceptions", [])),
        "append_prefix": data["append"]["prefix"],
    }


def _ise_base(word):
    return re.sub(r"is(e|ed|es|ing|ation|ations)$", "ise", word.lower())


def appended_desc_keys(mod):
    """Classify event desc keys by position in a desc = { } concatenation.

    Returns (appended {key: (rel, line, event)}, skipped [str]). A key is
    'appended' when it is the desc of a triggered_desc (or a plain desc) that
    is a direct child of an event's desc block and not its first segment.
    first_valid / random_valid alternatives are never appended when they open
    the block; later ones (an alternative appended as a whole), nested desc
    blocks, and keys that also appear in another role are skipped.
    """
    roles = collections.defaultdict(set)
    where = {}
    skipped = []
    for rel, eid, ev in mod.events():
        for d in pdx_parse.find(ev.value, "desc"):
            if not d.is_block:
                roles[d.value].add("opener")
                continue
            segs = [c for c in d.value if c.key != "#"]
            for i, seg in enumerate(segs):
                if seg.key == "triggered_desc" and seg.is_block:
                    inner = pdx_parse.first(seg.value, "desc")
                    if inner is None:
                        continue
                    if inner.is_block:
                        skipped.append("%s: nested desc block in triggered_desc (line %d)"
                                       % (eid, seg.line))
                        continue
                    role = "opener" if i == 0 else "appended"
                    roles[inner.value].add(role)
                    where.setdefault(inner.value, (rel, inner.line, eid))
                elif seg.key == "desc" and isinstance(seg.value, str):
                    roles[seg.value].add("opener" if i == 0 else "appended")
                    where.setdefault(seg.value, (rel, seg.line, eid))
                elif seg.key in ("first_valid", "random_valid") and seg.is_block:
                    acc = []
                    _loc_refs_in(seg, acc)
                    for k, ln in acc:
                        if i == 0:
                            roles[k].add("alternative")
                        else:
                            roles[k].add("ambiguous")
                            skipped.append("%s: %s inside a %s that follows the opener (line %d)"
                                           % (eid, k, seg.key, ln))
                else:
                    skipped.append("%s: unrecognised desc segment '%s' (line %d)"
                                   % (eid, seg.key, seg.line))
    appended = {}
    for k, r in sorted(roles.items()):
        if r == {"appended"}:
            appended[k] = where[k]
        elif "appended" in r:
            skipped.append("%s: used both appended and as %s" % (
                k, "/".join(sorted(r - {"appended"}))))
    return appended, sorted(set(skipped))


def rule_l013(mod, style=None):
    st = load_style() if style is None else style
    out = []
    values = {}
    for rel, line, key, value in iter_loc_values(mod, "eotg_*.yml"):
        values[key] = (rel, line, value)
        for ch in st["dashes"]:
            if ch in value:
                out.append(Finding("L013", rel, line, "L013a %s: %s in value (house style: no em/en "
                                   "dashes)" % (key, "em dash" if ch == "\u2014" else
                                                "en dash" if ch == "\u2013" else repr(ch))))
        text = _visible_text(value)
        for ex in st["exceptions"]:
            text = text.replace(ex, " ")
        hits = []
        for rx, kind, canadian in st["words"]:
            hits += [(m.group(1), kind, canadian) for m in rx.finditer(text)]
        for m in st["ise"].finditer(text):
            if _ise_base(m.group(1)) not in st["ise_exceptions"]:
                hits.append((m.group(1), "-ise spelling", st["ise_canadian"]))
        for word, kind, canadian in sorted(set(hits), key=lambda h: h[0].lower()):
            out.append(Finding("L013", rel, line, "L013b %s: %s '%s' (Canadian: %s)"
                               % (key, kind, word, canadian)))
        probs = []
        if "  " in value:
            probs.append("double space")
        if value[:1].isspace():
            probs.append("leading whitespace")
        if value[-1:].isspace():
            probs.append("trailing whitespace")
        if probs:
            out.append(Finding("L013", rel, line, "L013c %s: %s inside the quoted value"
                               % (key, ", ".join(probs))))
    appended, skipped = appended_desc_keys(mod)
    mod.skipped["L013d"] = skipped
    for key, (srel, sline, eid) in sorted(appended.items()):
        if key not in values:
            continue        # undefined key: L010's job
        rel, line, value = values[key]
        if not value.startswith(st["append_prefix"]):
            out.append(Finding("L013", rel, line,
                               "L013d %s: appended after the opener in %s (%s:%d) but does not "
                               "start with \\n\\n" % (key, eid, srel, sline)))
    return out


def load_conventions(path=CONVENTIONS_FILE):
    data = json.loads(textio.read_text(path)[0])
    return data


def _convention_regex(conv, mod):
    """One regex matching every loc key implied by a defined object."""
    alts = []
    for folder, spec in sorted(conv["folders"].items()):
        keys = [n.key for _, doc in mod.common_dir(folder) for n in doc.nodes
                if n.is_block and n.key and not n.key.startswith("@")]
        for key in keys:
            for pat in spec["patterns"]:
                alts.append(re.escape(pat).replace(r"\{key\}", re.escape(key))
                            .replace(r"\{n\}", r"\d+"))
    if not alts:
        return None
    return re.compile(r"^(?:%s)$" % "|".join(alts))


def script_tokens(mod):
    """Every key and string value in script, plus identifier-like words in .gui files."""
    toks = set()
    for doc in mod.docs.values():
        for n, _ in pdx_parse.walk(doc.nodes):
            if n.key:
                toks.add(n.key)
            if isinstance(n.value, str):
                toks.add(n.value)
    for f in _iter_files(mod.root, "gfx", (".gui",)):
        text, _ = pdx_parse.read_text(f)
        toks |= set(re.findall(r"[A-Za-z_][\w.\-]*", text))
    return toks


def rule_l014(mod, conventions=None):
    conv = load_conventions() if conventions is None else conventions
    defined = {}
    loc_refs = set()
    ref_res = [re.compile(r) for r in conv.get("loc_reference_regexes", [])]
    for rel, line, key, value in iter_loc_values(mod):
        if "eotg_" in key:
            defined.setdefault(key, (rel, line))
        for rx in ref_res:
            loc_refs |= {m.group(1) for m in rx.finditer(value)}
    if not defined:
        return []
    used = script_tokens(mod) | loc_refs
    implied = _convention_regex(conv, mod)
    out = []
    for key, (rel, line) in sorted(defined.items()):
        if key in used or (implied and implied.match(key)):
            continue
        out.append(Finding("L014", rel, line,
                           "loc key '%s' is defined but nothing references it (script, "
                           "naming convention or $KEY$)" % key))
    return out


# ------------------------------------------------------------------ suppression
ALLOW_RE = re.compile(r"#\s*eotg_lint:\s*allow\b(.*)$")
ALLOW_ARGS_RE = re.compile(r"^\s*((?:L\d{3})(?:\s*,\s*L\d{3})*)\s*(.*)$")


def scan_allows(mod):
    """{rel: {line: set(rules)}} for valid allows, plus L000 findings for bad ones."""
    allows, bad = {}, []
    files = list(mod.docs) + list(mod.loc_files)
    for rel in sorted(set(files)):
        text, _ = pdx_parse.read_text(os.path.join(mod.root, rel))
        for i, line in enumerate(text.splitlines(), 1):
            m = ALLOW_RE.search(line)
            if not m:
                continue
            a = ALLOW_ARGS_RE.match(m.group(1))
            if not a:
                bad.append(Finding("L000", rel, i, "eotg_lint allow without a rule id "
                                   "(use '# eotg_lint: allow L007 <reason>')"))
                continue
            rules = {r.strip() for r in a.group(1).split(",")}
            unknown = rules - set(RULES)
            if unknown:
                bad.append(Finding("L000", rel, i, "eotg_lint allow names unknown rule(s) %s"
                                   % ", ".join(sorted(unknown))))
                continue
            if not a.group(2).strip():
                bad.append(Finding("L000", rel, i, "eotg_lint allow %s without a reason"
                                   % ",".join(sorted(rules))))
                continue
            allows.setdefault(rel, {})[i] = rules
    return allows, bad


# Rules an inline allow cannot silence: a stray BOM is a load-time crash, never a choice.
UNSUPPRESSABLE = {"L016"}


def apply_allows(findings, allows):
    kept = []
    for f in findings:
        if f.rule in UNSUPPRESSABLE:
            kept.append(f)
            continue
        lines = allows.get(f.file, {})
        if f.rule in lines.get(f.line, ()) or f.rule in lines.get(f.line - 1, ()):
            continue
        kept.append(f)
    return kept


RULE_FUNCS = [
    ("L001", rule_l001), ("L002", rule_l002), ("L003", rule_l003), ("L004", rule_l004),
    ("L005", rule_l005), ("L006", rule_l006), ("L007", rule_l007), ("L008", rule_l008),
    ("L009", rule_l009), ("L010", rule_l010), ("L011", rule_l011), ("L012", rule_l012),
    ("L013", rule_l013), ("L014", rule_l014), ("L016", rule_l016),
]


def lint(root, rules=None, allowlist=None, stats=None):
    """Run the rules over the mod at root. Returns a sorted list of Findings.

    ``stats``, if a dict, receives {"skipped": {rule: [items not checked]}}."""
    mod = Mod(root)
    out = [f for f in mod.findings if not rules or "L000" in rules]
    for rid, fn in RULE_FUNCS:
        if rules and rid not in rules:
            # L003 fills mod.loc, which L010 needs, even if L003 is not selected
            if rid == "L003" and "L010" in rules:
                rule_l003(mod)
            continue
        res = fn(mod, allowlist) if rid == "L010" else fn(mod)
        out.extend(res)
    allows, bad = scan_allows(mod)
    out = apply_allows(out, allows)
    if not rules or "L000" in rules:
        out.extend(bad)
    out.sort(key=lambda f: (f.file, f.line, f.rule, f.message))
    if stats is not None:
        stats["skipped"] = {k: list(v) for k, v in sorted(mod.skipped.items())}
    return out


def filter_paths(findings, root, paths):
    if not paths:
        return findings
    norm = []
    for p in paths:
        ap = os.path.abspath(p if os.path.isabs(p) else os.path.join(os.getcwd(), p))
        if not os.path.exists(ap):
            ap = os.path.abspath(os.path.join(root, p))
        norm.append(_rel(root, ap).rstrip("/"))
    keep = []
    for f in findings:
        for n in norm:
            if n in (".", "") or f.file == n or f.file.startswith(n + "/"):
                keep.append(f)
                break
    return keep


def load_baseline(path):
    data = json.loads(textio.read_text(path)[0])
    items = data.get("findings", data) if isinstance(data, dict) else data
    return collections.Counter((i["rule"], i["file"], i["message"]) for i in items)


def split_baseline(findings, baseline):
    """Return (new, known) honouring multiplicity."""
    budget = collections.Counter(baseline)
    new, known = [], []
    for f in findings:
        if budget[f.key()] > 0:
            budget[f.key()] -= 1
            known.append(f)
        else:
            new.append(f)
    return new, known


def write_json(path, findings, stats=None):
    data = {"version": 1,
            "tool": "docs/tools/eotg_lint.py",
            "findings": [f.as_dict() for f in findings]}
    if stats:
        data["skipped"] = stats.get("skipped", {})
    textio.write_text(path, json.dumps(data, indent=1, sort_keys=True) + "\n", bom=False)


def main(argv=None):
    pdx_parse.utf8_console()
    ap = argparse.ArgumentParser(description="Static linter for the Echoes of the Grip mod.")
    ap.add_argument("paths", nargs="*", help="only report findings under these paths")
    ap.add_argument("--root", default=DEFAULT_ROOT, help="mod repo root (default: this repo)")
    ap.add_argument("--rule", action="append", default=[],
                    help="only run these rules (repeatable or comma-separated, e.g. L005)")
    ap.add_argument("--json", metavar="OUT", help="write all findings as JSON")
    ap.add_argument("--baseline", metavar="FILE", help="known findings; only new ones fail")
    ap.add_argument("--write-baseline", metavar="FILE", help="write current findings as baseline")
    ap.add_argument("--quiet", action="store_true", help="print only the summary")
    args = ap.parse_args(argv)

    rules = set()
    for r in args.rule:
        rules |= {x.strip().upper() for x in r.split(",") if x.strip()}
    unknown = rules - set(RULES)
    if unknown:
        ap.error("unknown rule(s): %s" % ", ".join(sorted(unknown)))

    root = os.path.abspath(args.root)
    stats = {}
    findings = filter_paths(lint(root, rules or None, stats=stats), root, args.paths)

    if args.json:
        write_json(args.json, findings, stats)
    if args.write_baseline:
        write_json(args.write_baseline, findings)

    if args.baseline:
        new, known = split_baseline(findings, load_baseline(args.baseline))
    else:
        new, known = findings, []

    if not args.quiet:
        for f in new:
            print(f)
    by_rule = collections.Counter(f.rule for f in findings)
    new_by_rule = collections.Counter(f.rule for f in new)
    print("\n%-5s %-8s %6s %6s  %s" % ("rule", "severity", "total", "new", "description"))
    sev_by_rule = collections.defaultdict(set)
    for f in findings:
        sev_by_rule[f.rule].add(f.severity)
    for rid in sorted(RULES):
        if by_rule[rid] or new_by_rule[rid]:
            sev = "/".join(sorted(sev_by_rule[rid])) or RULES[rid][0]
            print("%-5s %-8s %6d %6d  %s" % (rid, sev, by_rule[rid],
                                             new_by_rule[rid], RULES[rid][1]))
    print("total: %d finding(s), %d new%s" % (len(findings), len(new),
                                             " (vs baseline)" if args.baseline else ""))
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main())
