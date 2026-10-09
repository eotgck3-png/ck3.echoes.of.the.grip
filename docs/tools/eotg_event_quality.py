"""Event quality scorecard: the mod's events against vanilla's, feature by feature.

    python docs/tools/eotg_event_quality.py                 # write docs/qa/generated/event_quality.{md,json}
    python docs/tools/eotg_event_quality.py --check         # exit 1 if the committed report is stale
    python docs/tools/eotg_event_quality.py --vanilla       # also re-measure vanilla (needs the game)
    python docs/tools/eotg_event_quality.py --event eotg_aug_tier1.005   # one event's breakdown

docs/specs/event_quality_v1.md W0b and §15. Ported from the loc-review session's evq.py
(docs/qa/event_quality_vs_vanilla_2026-10-08.md), keeping its parsing: comment strip,
brace blocks, the non-hidden filter, and desc key resolution through loc. Added per event:
override_background / override_effect_2d / window, letter type with sender and opening,
send_interface_toast / send_interface_message / play_music_cue counts (anywhere in the event,
`after` and options included), add_internal_flag values, triggered_animation count and the
distinct animation set, outfit_tags, random_valid, Custom()/Custom2() and #EMP and \\n\\n in
the desc text, a voice label for the main desc, and each option's gate axis.

**Voice classifier** (main desc key = the first desc key the event names that has text):
speech is stripped first (`"..."` pairs, `\\"...\\"`, and legacy '...' pairs found by
eotg_quote_convert), then `[...]`; first-person words (I, me, my, mine, myself) are counted
against second-person words (you, your, yours, yourself). More first -> `1st`, more second
-> `2nd`, otherwise `neutral` (`none` when the event has no desc text). Pinned in
tests/test_eotg_event_quality.py. This is the spec's definition; it measures the mod at about
74% second person, not the report's 52% (whose hand count is not reproducible from evq.json).

**Gate axes per option** (from the option's `trigger`, root only: a trait check counts only
when every block between it and `trigger` is a logic block such as OR/AND/trigger_if, never
NOT/NOR or a scope change):
  personality  root needs a `category = personality` trait (vanilla common/traits/00_traits.txt;
               the list is cached in docs/tools/eotg_personality_traits.json so the tool and
               eotg_lint L017 run without the game; --vanilla refreshes it);
  education    root needs an education_* trait, a skill threshold, or the option has `skill =`;
  tier         `highest_held_title_tier` in the trigger;
  other        some other trigger; options with no trigger are `ungated`.

**Vanilla columns.** With --vanilla the game's non-hidden character events are measured too
("all", and "DLC" = events/dlc/), the denominator of the 2026-10-08 report; the summaries are stored in the JSON, so later runs without the game (and
--check) reuse them. Standard library only.
"""
import argparse
import collections
import glob
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pdx_parse  # noqa: E402
import textio  # noqa: E402
import eotg_quote_convert as Q  # noqa: E402

DEFAULT_ROOT = os.path.dirname(os.path.dirname(HERE))
DEFAULT_GAME = os.environ.get("EOTG_CK3_GAME",
                              "D:/SteamLibrary/steamapps/common/Crusader Kings III/game")
OUT_MD = "docs/qa/generated/event_quality.md"
OUT_JSON = "docs/qa/generated/event_quality.json"
TRAITS_FILE = os.path.join(HERE, "eotg_personality_traits.json")


# ------------------------------------------------------------------ evq.py parsing (kept)
def load_loc(root):
    d = {}
    for f in sorted(glob.glob(root + "/localization/english/**/*.yml", recursive=True)):
        text, _ = textio.read_text(f, errors="ignore")
        for line in text.splitlines():
            m = re.match(r'\s+([\w.\-]+):\d*\s+"(.*)"\s*(#.*)?$', line)
            if m:
                d[m.group(1)] = m.group(2)
    return d


def strip_comments(s):
    return re.sub(r"#[^\n]*", "", s)


def block(s, i):
    d = 0
    j = s.find("{", i)
    for k in range(j, len(s)):
        c = s[k]
        if c == "{":
            d += 1
        elif c == "}":
            d -= 1
            if d == 0:
                return s[j:k + 1]
    return s[j:]


def subblocks(b, name):
    return [block(b, m.start()) for m in re.finditer(r"(?<![\w.])" + name + r"\s*=\s*\{", b)]


LETTER_WINDOWS = ("letter_event", "anonymous_letter_event")


def words(t):
    t = re.sub(r"\[[^\]]*\]", "X", t)
    t = re.sub(r"#\w+|#!|\n|\$\w+\$", " ", t)
    return len(re.findall(r"[A-Za-z']+", t))


# evq.py's dialogue detector (report caveat: +-5 points). B7 review: the
# opening-quote lookahead also takes `[`, so speech that opens on a loc
# function ("[ROOT.Char.GetFirstName], ...") counts.
SPEECH = re.compile(r'\\"|“|”|(?<=[\s:,])"(?=[A-Z\[])|(?<![A-Za-z])\'[A-Z][^\']{6,}\'')


# ------------------------------------------------------------------ voice
FIRST = re.compile(r"\b(I|me|my|mine|myself)\b")
FIRST_CI = re.compile(r"\b(me|my|mine|myself)\b", re.I)
SECOND = re.compile(r"\b(you|your|yours|yourself)\b", re.I)


def strip_speech(value):
    """The value with speech and [functions] blanked: legacy '...' pairs, \\"...\\", "..."."""
    chars = list(value)
    for a, b in Q.analyze_value(value).speechlike:
        for k in range(a, b + 1):
            chars[k] = " "
    t = "".join(chars)
    t = re.sub(r'\\".*?\\"', " ", t)
    t = re.sub(r'"[^"]*"', " ", t)
    t = re.sub(r"\[[^\]]*\]", " ", t)
    return t.replace("\\n", " ")


def voice_counts(value):
    t = strip_speech(value)
    first = len(re.findall(r"\bI\b", t)) + len(FIRST_CI.findall(t))
    return first, len(SECOND.findall(t))


def voice_label(value):
    if not value:
        return "none"
    f, s = voice_counts(value)
    if f > s:
        return "1st"
    if s > f:
        return "2nd"
    return "neutral"


# ------------------------------------------------------------------ gates
LOGIC_KEYS = {"OR", "AND", "trigger_if", "trigger_else_if", "trigger_else", "limit", "root",
              "calc_true_if", "custom_description", "custom_tooltip", "show_as_tooltip"}
SKILLS = {"diplomacy", "martial", "stewardship", "intrigue", "learning", "prowess"}


def load_personality_traits(path=TRAITS_FILE):
    if not os.path.exists(path):
        return set()
    return set(json.loads(textio.read_text(path)[0])["traits"])


def vanilla_personality_traits(game):
    """`category = personality` traits in vanilla common/traits/00_traits.txt, sorted."""
    p = os.path.join(game, "common", "traits", "00_traits.txt")
    s = strip_comments(textio.read_text(p, errors="ignore")[0])
    out = []
    for m in re.finditer(r"^([A-Za-z_]\w*)\s*=\s*\{", s, re.M):
        if re.search(r"(?<![\w.])category\s*=\s*personality\b", block(s, m.start())):
            out.append(m.group(1))
    return sorted(set(out))


def _root_path(parents):
    return all(p.key in LOGIC_KEYS for p in parents)


def option_gates(option, personality):
    """Gate axes of one option (a pdx_parse Node). Returns a dict:
    personality [trait...], education bool, tier bool, trigger bool, axis str."""
    res = {"personality": [], "education": False, "tier": False, "trigger": False}
    if pdx_parse.first(option.value, "skill") is not None:
        res["education"] = True
    for trg in pdx_parse.find(option.value, "trigger"):
        if not trg.is_block:
            continue
        res["trigger"] = res["trigger"] or bool(trg.value)
        for n, parents in pdx_parse.walk(trg.value):
            if not _root_path(parents):
                continue
            if n.key == "has_trait" and isinstance(n.value, str) and n.op == "=":
                if n.value in personality:
                    res["personality"].append(n.value)
                elif n.value.startswith("education_"):
                    res["education"] = True
            elif n.key in SKILLS and isinstance(n.value, str) and n.op in (">=", ">"):
                res["education"] = True
            elif n.key == "highest_held_title_tier":
                res["tier"] = True
    res["personality"] = sorted(set(res["personality"]))
    if res["personality"]:
        res["axis"] = "personality"
    elif res["education"]:
        res["axis"] = "education"
    elif res["tier"]:
        res["axis"] = "tier"
    elif res["trigger"]:
        res["axis"] = "other"
    else:
        res["axis"] = "ungated"
    return res


def _parse_option(text):
    doc = pdx_parse.parse_text(text)
    for n in doc.nodes:
        if n.is_block:
            return n
    return pdx_parse.Node("option", "=", list(doc.nodes), 1)


# ------------------------------------------------------------------ analysis
FLAG_KEYS = ["theme", "override_background", "override_effect_2d", "override_sound",
             "override_icon", "window", "widget", "orphan", "cooldown", "after",
             "on_trigger_fail", "artifact", "court_scene", "sender", "opening", "signature"]
PORTRAIT_RE = re.compile(r"(?<![\w.])(left_portrait|right_portrait|lower_left_portrait|"
                         r"lower_center_portrait|lower_right_portrait|center_portrait)\s*=")


def _value_of(b, key):
    m = re.search(r"(?<![\w.])" + key + r"\s*=\s*([\w.\-]+)", b)
    return m.group(1) if m else None


def _ref_values(b, key):
    """Values of `key = { reference = X }` / `key = X` blocks in b."""
    out = []
    for m in re.finditer(r"(?<![\w.])" + key + r"\s*=\s*", b):
        rest = b[m.end():]
        if rest.startswith("{"):
            blk = block(b, m.start())
            out += re.findall(r"(?<![\w.])reference\s*=\s*([\w.\-]+)", blk)
        else:
            v = re.match(r"[\w.\-]+", rest)
            if v:
                out.append(v.group(0))
    return out


def analyze_event(eid, b, rel, loc, personality):
    r = {"id": eid, "file": rel}
    tm = re.search(r"\btype\s*=\s*(\w+)", b)
    r["type"] = tm.group(1) if tm else "?"
    for k in FLAG_KEYS:
        r[k] = bool(re.search(r"(?<![\w.])" + k + r"\s*=", b))
    r["backgrounds"] = sorted(set(_ref_values(b, "override_background")))
    r["effects_2d"] = sorted(set(_ref_values(b, "override_effect_2d")))
    r["window_value"] = _value_of(b, "window")
    ports = PORTRAIT_RE.findall(b)
    r["portraits"] = len(ports)
    r["animation"] = len(re.findall(r"(?<![\w.])(animation|triggered_animation)\s*=", b))
    r["triggered_animation"] = len(re.findall(r"(?<![\w.])triggered_animation\s*=", b))
    r["animations"] = sorted(set(re.findall(r"(?<![\w.])animation\s*=\s*(\w+)", b)))
    r["outfit"] = bool(re.search(r"outfit_tags\s*=", b))
    r["camera"] = bool(re.search(r"camera\s*=", b))
    r["toasts"] = len(re.findall(r"(?<![\w.])send_interface_toast\s*=", b))
    r["messages"] = len(re.findall(r"(?<![\w.])send_interface_message\s*=", b))
    r["music_cues"] = len(re.findall(r"(?<![\w.])play_music_cue\s*=", b))
    r["internal_flags"] = sorted(set(re.findall(r"(?<![\w.])add_internal_flag\s*=\s*(\w+)", b)))
    # A letter is the letter type or a letter window: vanilla
    # events/_events.info:18,23 and gui/event_windows/{anonymous_,}letter_event.gui
    r["letter"] = (r["type"] == "letter_event"
                   or (r["window_value"] or "").strip('"') in LETTER_WINDOWS)
    # desc (evq.py)
    dm = re.search(r"(?<![\w.])desc\s*=", b)
    descblk = ""
    if dm:
        after = b[dm.end():].lstrip()
        descblk = block(b, dm.start()) if after.startswith("{") else (after.split() or [""])[0]
    dkeys = (re.findall(r"(?<![\w.])desc\s*=\s*([\w.\-]+)", descblk)
             if descblk.startswith("{") else [descblk])
    r["triggered_desc"] = descblk.count("triggered_desc")
    r["random_valid"] = "random_valid" in descblk
    texts = [loc.get(k, "") for k in dkeys]
    wl = [words(t) for t in texts if t]
    r["desc_keys"] = len(dkeys)
    r["desc_words_main"] = max(wl) if wl else 0
    r["desc_words_total"] = sum(wl)
    r["speech"] = any(SPEECH.search(t) for t in texts)
    r["desc_has_scope_text"] = any("[" in t for t in texts)
    r["custom_loc"] = any(re.search(r"\bCustom2?\(", t) for t in texts)
    r["emp"] = any("#EMP" in t for t in texts)
    r["formatting"] = any(re.search(r"#(?!!)[A-Za-z]", t) for t in texts)
    r["paragraphs"] = any("\\n\\n" in t for t in texts)
    # The "main" desc skips Seamless-only branches (a triggered_desc whose
    # trigger has `has_trait = eotg_total_integration`; event_quality_v1
    # §12.5 S3 puts them first in first_valid), else a Seamless-first event
    # reads as neutral. If every keyed branch is Seamless, fall back.
    seamless = set()
    if descblk.startswith("{"):
        for td in subblocks(descblk, "triggered_desc"):
            if re.search(r"has_trait\s*=\s*eotg_total_integration\b", td):
                seamless.update(re.findall(r"(?<![\w.])desc\s*=\s*([\w.\-]+)", td))
    pairs = [(k, t) for k, t in zip(dkeys, texts) if t]
    pick = [(k, t) for k, t in pairs if k not in seamless] or pairs
    main = pick[0][1] if pick else ""
    r["main_desc_key"] = pick[0][0] if pick else (dkeys[0] if dkeys else "")
    r["voice"] = voice_label(main)
    r["voice_counts"] = list(voice_counts(main)) if main else [0, 0]
    opening = _value_of(b, "opening")
    r["opening_key"] = opening
    # options
    opts = subblocks(b, "option")
    r["options"] = len(opts)
    r["opt_trait"] = sum(1 for o in opts
                         if re.search(r"(?<![\w.])trait\s*=\s*\w+", o.split("{", 1)[1][:300]))
    r["opt_skill"] = sum(1 for o in opts if re.search(r"(?<![\w.])skill\s*=\s*\w+", o[:400]))
    r["opt_ai"] = sum(1 for o in opts if "ai_chance" in o)
    r["opt_stress"] = sum(1 for o in opts if "stress_impact" in o)
    r["opt_flavor"] = sum(1 for o in opts if re.search(r"(?<![\w.])flavor\s*=", o))
    r["opt_flag"] = sum(1 for o in opts if "add_internal_flag" in o)
    r["opt_highlight"] = sum(1 for o in opts if "highlight_portrait" in o)
    r["opt_unavail"] = sum(1 for o in opts if "show_as_unavailable" in o)
    ow = []
    gates = []
    for o in opts:
        nm = re.search(r"(?<![\w.])name\s*=\s*([\w.\-]+)", o)
        name = nm.group(1) if nm else None
        if name and name in loc:
            ow.append(words(loc[name]))
        g = option_gates(_parse_option("option = " + o), personality)
        gates.append({"name": name, "axis": g["axis"], "personality": g["personality"]})
    r["opt_words_avg"] = round(statistics.mean(ow), 1) if ow else 0
    r["option_gates"] = gates
    r["gate_axes"] = dict(collections.Counter(g["axis"] for g in gates))
    r["personality_gates"] = sum(1 for g in gates if g["axis"] == "personality")
    tk = re.search(r"(?<![\w.])title\s*=\s*([\w.\-]+)", b)
    r["title_words"] = words(loc.get(tk.group(1), "")) if tk else 0
    return r


def analyze(root, loc, personality, event_glob="events/**/*.txt"):
    rows = []
    for f in sorted(glob.glob(os.path.join(root, event_glob), recursive=True)):
        try:
            s = strip_comments(textio.read_text(f, errors="ignore")[0])
        except OSError:
            continue
        rel = os.path.relpath(f, root).replace(os.sep, "/")
        for m in re.finditer(r"^([A-Za-z_][\w]*\.\d+)\s*=\s*\{", s, re.M):
            b = block(s, m.start())
            if re.search(r"\bhidden\s*=\s*yes", b[:400]):
                continue
            rows.append(analyze_event(m.group(1), b, rel, loc, personality))
    return rows


# ------------------------------------------------------------------ summary
def _pct(n, d):
    return round(100.0 * n / d, 1) if d else 0.0


def _pctile(vals, p):
    if not vals:
        return 0
    vals = sorted(vals)
    k = max(0, min(len(vals) - 1, int(round(p / 100.0 * (len(vals) - 1)))))
    return vals[k]


def _num(x):
    x = float(x)
    return int(x) if x.is_integer() else round(x, 1)


def summarize(rows):
    n = len(rows)
    opts = sum(r["options"] for r in rows)
    with_opts = [r for r in rows if r["options"]]
    words_main = [r["desc_words_main"] for r in rows if r["desc_words_main"]]
    voice = collections.Counter(r["voice"] for r in rows)
    axes = collections.Counter()
    for r in rows:
        axes.update(r["gate_axes"])
    anims = set()
    for r in rows:
        anims.update(r["animations"])
    types = collections.Counter(r["type"] for r in rows)
    return {
        "events": n,
        "types": dict(sorted(types.items())),
        "theme_pct": _pct(sum(r["theme"] for r in rows), n),
        "override_background_pct": _pct(sum(r["override_background"] for r in rows), n),
        "override_effect_2d_uses": sum(1 for r in rows if r["override_effect_2d"]),
        "three_plus_portraits_pct": _pct(sum(r["portraits"] >= 3 for r in rows), n),
        "distinct_animations": len(anims),
        "triggered_animation_per_event": round(sum(r["triggered_animation"] for r in rows) / n, 2) if n else 0,
        "outfit_tags_pct": _pct(sum(r["outfit"] for r in rows), n),
        "camera_pct": _pct(sum(r["camera"] for r in rows), n),
        "dialogue_pct": _pct(sum(r["speech"] for r in rows), n),
        "voice_1st_pct": _pct(voice["1st"], n),
        "voice_2nd_pct": _pct(voice["2nd"], n),
        "voice_neutral_pct": _pct(voice["neutral"], n),
        "voice_none_pct": _pct(voice["none"], n),
        "custom_loc_pct": _pct(sum(r["custom_loc"] for r in rows), n),
        "emp_pct": _pct(sum(r["emp"] for r in rows), n),
        "formatting_pct": _pct(sum(r["formatting"] for r in rows), n),
        "paragraphs_pct": _pct(sum(r["paragraphs"] for r in rows), n),
        "random_valid_pct": _pct(sum(r["random_valid"] for r in rows), n),
        "triggered_desc_pct": _pct(sum(r["triggered_desc"] > 0 for r in rows), n),
        "desc_words_median": _num(statistics.median(words_main)) if words_main else 0,
        "desc_words_p10": _pctile(words_main, 10),
        "desc_words_p90": _pctile(words_main, 90),
        "options_median": _num(statistics.median([r["options"] for r in with_opts])) if with_opts else 0,
        "options_p90": _pctile([r["options"] for r in with_opts], 90),
        "option_trait_icon_pct": _pct(sum(r["opt_trait"] for r in rows), opts),
        "option_skill_icon_pct": _pct(sum(r["opt_skill"] for r in rows), opts),
        "ai_chance_every_option_pct": _pct(sum(r["opt_ai"] == r["options"] for r in with_opts),
                                           len(with_opts)),
        "stress_on_an_option_pct": _pct(sum(r["opt_stress"] > 0 for r in with_opts), len(with_opts)),
        "internal_flag_pct": _pct(sum(bool(r["internal_flags"]) for r in rows), n),
        "flavor_pct": _pct(sum(r["opt_flavor"] > 0 for r in rows), n),
        "toasts_per_event": round(sum(r["toasts"] for r in rows) / n, 2) if n else 0,
        "messages": sum(r["messages"] for r in rows),
        "music_cues": sum(r["music_cues"] for r in rows),
        "letter_events": sum(r["letter"] for r in rows),
        "after_pct": _pct(sum(r["after"] for r in rows), n),
        "window_set": sum(1 for r in rows if r["window_value"]),
        "gate_axes_options": {k: axes.get(k, 0) for k in
                              ("personality", "education", "tier", "other", "ungated")},
        "events_2plus_personality_gates": sum(r["personality_gates"] >= 2 for r in rows),
        "events_3plus_personality_gates": sum(r["personality_gates"] >= 3 for r in rows),
    }


ROWS = [  # (label, key, fmt)
    ("Events (non-hidden)", "events", "{}"),
    ("Theme set", "theme_pct", "{}%"),
    ("`override_background`", "override_background_pct", "{}%"),
    ("`override_effect_2d` events", "override_effect_2d_uses", "{}"),
    ("Three or more portraits", "three_plus_portraits_pct", "{}%"),
    ("Distinct animations", "distinct_animations", "{}"),
    ("`triggered_animation` per event", "triggered_animation_per_event", "{}"),
    ("`outfit_tags`", "outfit_tags_pct", "{}%"),
    ("`camera`", "camera_pct", "{}%"),
    ("Spoken dialogue in the desc", "dialogue_pct", "{}%"),
    ("Voice: first person", "voice_1st_pct", "{}%"),
    ("Voice: second person", "voice_2nd_pct", "{}%"),
    ("Voice: neutral", "voice_neutral_pct", "{}%"),
    ("Voice: no desc text", "voice_none_pct", "{}%"),
    ("`Custom()` in the desc", "custom_loc_pct", "{}%"),
    ("`#EMP` in the desc", "emp_pct", "{}%"),
    ("Any `#` formatting in the desc", "formatting_pct", "{}%"),
    ("`\\n\\n` in the desc", "paragraphs_pct", "{}%"),
    ("`random_valid` desc", "random_valid_pct", "{}%"),
    ("`triggered_desc` used", "triggered_desc_pct", "{}%"),
    ("Median desc words (main key)", "desc_words_median", "{}"),
    ("Desc words p10 / p90", ("desc_words_p10", "desc_words_p90"), "{} / {}"),
    ("Options defined: median, p90", ("options_median", "options_p90"), "{}, p90 {}"),
    ("Options with a trait icon", "option_trait_icon_pct", "{}%"),
    ("Options with a `skill =` icon", "option_skill_icon_pct", "{}%"),
    ("`ai_chance` on every option", "ai_chance_every_option_pct", "{}%"),
    ("Stress on an option", "stress_on_an_option_pct", "{}%"),
    ("`add_internal_flag`", "internal_flag_pct", "{}%"),
    ("Option `flavor =`", "flavor_pct", "{}%"),
    ("Toasts per event", "toasts_per_event", "{}"),
    ("`send_interface_message`", "messages", "{}"),
    ("`play_music_cue`", "music_cues", "{}"),
    ("Letter events", "letter_events", "{}"),
    ("`window =` set", "window_set", "{}"),
    ("`after = {}` block", "after_pct", "{}%"),
    ("Events with 2+ personality-gated options (L017)", "events_2plus_personality_gates", "{}"),
    ("Events with 3+ personality-gated options", "events_3plus_personality_gates", "{}"),
]


def _fmt(summary, key, fmt):
    if summary is None:
        return "–"
    if isinstance(key, tuple):
        return fmt.format(*(summary.get(k, "–") for k in key))
    return fmt.format(summary.get(key, "–"))


def build(root, personality, vanilla=None, traits_source=None):
    loc = load_loc(root)
    rows = analyze(root, loc, personality)
    rows.sort(key=lambda r: (r["file"], r["id"]))
    per_file = collections.OrderedDict()
    for f in sorted({r["file"] for r in rows}):
        per_file[f] = summarize([r for r in rows if r["file"] == f])
    data = {
        "version": 1,
        "tool": "docs/tools/eotg_event_quality.py",
        "spec": "docs/specs/event_quality_v1.md §15",
        "personality_traits": sorted(personality),
        "personality_traits_source": traits_source,
        "summary": {"mod": summarize(rows),
                    "vanilla_all": (vanilla or {}).get("vanilla_all"),
                    "vanilla_dlc": (vanilla or {}).get("vanilla_dlc")},
        "vanilla_source": (vanilla or {}).get("vanilla_source"),
        "per_file": per_file,
        "events": rows,
    }
    return data


def render_md(data):
    s = data["summary"]
    out = ["# Event quality scorecard",
           "",
           "Generated by `python docs/tools/eotg_event_quality.py` (docs/specs/event_quality_v1.md "
           "W0b, §15); do not edit by hand. `--check` fails when this file is stale; "
           "`--vanilla` re-measures the vanilla columns from the game; "
           "`--event <id>` prints one event. Data: `event_quality.json`.",
           "",
           "Detection is pattern-based (dialogue and voice to about ±5 points). Counts are of "
           "options as **defined**, not as shown to one player. Percentages are of non-hidden "
           "events, except option rows (of options) and the `ai_chance`/stress rows (of events "
           "with options).",
           "",
           "Vanilla source: %s" % (data.get("vanilla_source") or "not measured yet (run --vanilla)"),
           "",
           "## Totals",
           "",
           "| Feature | Vanilla, all | Vanilla, DLC | **Mod** |",
           "|---|---|---|---|"]
    for label, key, fmt in ROWS:
        out.append("| %s | %s | %s | **%s** |" % (label, _fmt(s["vanilla_all"], key, fmt),
                                                  _fmt(s["vanilla_dlc"], key, fmt),
                                                  _fmt(s["mod"], key, fmt)))
    ax = s["mod"]["gate_axes_options"]
    out += ["",
            "**Mod option gate axes** (options): personality %(personality)d, education/skill "
            "%(education)d, tier %(tier)d, other trigger %(other)d, ungated %(ungated)d." % ax,
            "",
            "## Per file (mod)",
            "",
            "| File | Events | Background | Dialogue | Voice 1st / 2nd / neutral | Trait icons | "
            "Toasts/event | `\\n\\n` | `#EMP` | `Custom()` | 2+ personality gates |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    for f, x in data["per_file"].items():
        out.append("| `%s` | %d | %s%% | %s%% | %s / %s / %s%% | %s%% | %s | %s%% | %s%% | %s%% | %d |" % (
            f, x["events"], x["override_background_pct"], x["dialogue_pct"], x["voice_1st_pct"],
            x["voice_2nd_pct"], x["voice_neutral_pct"], x["option_trait_icon_pct"],
            x["toasts_per_event"], x["paragraphs_pct"], x["emp_pct"], x["custom_loc_pct"],
            x["events_2plus_personality_gates"]))
    stacked = [r for r in data["events"] if r["personality_gates"] >= 2]
    out += ["", "## Events with 2+ personality-gated options (%d)" % len(stacked), "",
            "Feeds eotg_lint L017 and the W5 re-gating batches (§13).", ""]
    for r in stacked:
        traits = sorted({t for g in r["option_gates"] for t in g["personality"]})
        out.append("- `%s` (%s): %d gated, %s" % (r["id"], r["file"], r["personality_gates"],
                                                 ", ".join(traits)))
    return "\n".join(out).rstrip("\n") + "\n"


def render_json(data):
    return json.dumps(data, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def event_breakdown(data, eid):
    for r in data["events"]:
        if r["id"] == eid:
            lines = ["%s (%s)" % (eid, r["file"])]
            for k in sorted(r):
                if k not in ("option_gates", "id", "file"):
                    lines.append("  %-26s %s" % (k, r[k]))
            lines.append("  options:")
            for g in r["option_gates"]:
                lines.append("    %-36s %-12s %s" % (g["name"], g["axis"],
                                                     ", ".join(g["personality"])))
            return "\n".join(lines)
    return None


def _norm(t):
    return t.replace("\r\n", "\n")


def main(argv=None):
    pdx_parse.utf8_console()
    ap = argparse.ArgumentParser(description="Event quality scorecard (mod against vanilla).")
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--game", default=DEFAULT_GAME)
    ap.add_argument("--vanilla", action="store_true",
                    help="re-measure vanilla and refresh the personality trait list (needs the game)")
    ap.add_argument("--check", action="store_true", help="exit 1 if the committed report is stale")
    ap.add_argument("--event", metavar="ID", help="print one event's breakdown and exit")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    md_path = os.path.join(root, *OUT_MD.split("/"))
    json_path = os.path.join(root, *OUT_JSON.split("/"))

    old = None
    if os.path.exists(json_path):
        try:
            old = json.loads(textio.read_text(json_path)[0])
        except ValueError:
            old = None
    personality = load_personality_traits()
    traits_source = "docs/tools/eotg_personality_traits.json"
    vanilla = None
    if old:
        vanilla = {"vanilla_all": old["summary"].get("vanilla_all"),
                   "vanilla_dlc": old["summary"].get("vanilla_dlc"),
                   "vanilla_source": old.get("vanilla_source")}
    if args.vanilla:
        if not os.path.isdir(args.game):
            ap.error("--vanilla needs the game at %s (or set EOTG_CK3_GAME)" % args.game)
        personality = set(vanilla_personality_traits(args.game))
        textio.write_text(TRAITS_FILE, json.dumps({
            "_comment": "Root personality traits for eotg_event_quality.py gate axes and eotg_lint "
                        "L017. Generated by `eotg_event_quality.py --vanilla`; do not edit.",
            "source": "vanilla common/traits/00_traits.txt, category = personality",
            "traits": sorted(personality)}, indent=1) + "\n", bom=False)
        vloc = load_loc(args.game)
        vrows = analyze(args.game, vloc, personality)
        # the report's denominator: vanilla character events (6,631 / 2,242 DLC in 1.20.0.3);
        # letter events are counted over every type, since none is a character_event
        vchar = [r for r in vrows if r["type"] == "character_event"]
        vdlc = [r for r in vchar if r["file"].startswith("events/dlc/")]
        ver = ""
        ls = os.path.join(os.path.dirname(args.game), "launcher", "launcher-settings.json")
        if os.path.exists(ls):
            try:
                ver = json.loads(textio.read_text(ls)[0]).get("rawVersion", "")
            except ValueError:
                ver = ""
        va, vd = summarize(vchar), summarize(vdlc)
        va["letter_events"] = sum(r["letter"] for r in vrows)
        vd["letter_events"] = sum(r["letter"] for r in vrows if r["file"].startswith("events/dlc/"))
        vanilla = {"vanilla_all": va, "vanilla_dlc": vd,
                   "vanilla_source": "CK3 %s game files: non-hidden character events (DLC = "
                                     "events/dlc/); letter events over every type" % (ver or "install")}
    if not personality:
        ap.error("no personality trait list: run once with --vanilla")

    data = build(root, personality, vanilla, traits_source)
    if args.event:
        b = event_breakdown(data, args.event)
        if b is None:
            print("no non-hidden event %s" % args.event)
            return 1
        print(b)
        return 0
    md, js = render_md(data), render_json(data)
    if args.check:
        stale = []
        for path, text in ((md_path, md), (json_path, js)):
            if not os.path.exists(path) or _norm(textio.read_text(path)[0]) != _norm(text):
                stale.append(os.path.relpath(path, root).replace(os.sep, "/"))
        m = data["summary"]["mod"]
        line = ("mod: %d events, background %s%%, dialogue %s%%, voice %s/%s%% 1st/2nd, trait "
                "icons %s%%, toasts %s/event, %d events with 2+ personality gates" % (
                    m["events"], m["override_background_pct"], m["dialogue_pct"],
                    m["voice_1st_pct"], m["voice_2nd_pct"], m["option_trait_icon_pct"],
                    m["toasts_per_event"], m["events_2plus_personality_gates"]))
        if stale:
            print("STALE: %s (re-run docs/tools/eotg_event_quality.py)\n%s" % (", ".join(stale), line))
            return 1
        print("current; " + line)
        return 0
    textio.write_text(md_path, md, bom=False, makedirs=True)
    textio.write_text(json_path, js, bom=False, makedirs=True)
    m = data["summary"]["mod"]
    print("wrote %s and %s: %d mod events" % (OUT_MD, OUT_JSON, m["events"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
