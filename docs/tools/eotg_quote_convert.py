"""Convert single-quoted speech in loc values to vanilla's unescaped double quotes.

    python docs/tools/eotg_quote_convert.py [paths ...] [--report OUT.md] [--apply] [--root REPO]

docs/specs/event_quality_v1.md W0e and §12.2. The house form for speech is an unescaped
straight double quote inside the loc string, as vanilla writes it:

    key:0 "Narration. "Speech," [x.GetSheHe] says."

CK3's loc reader takes the value as running to the last `"` on the line, so the inner
quotes need no escape. The mod's older text wrote speech as '...'; this tool converts it.

**Dry-run by default.** It prints a unified diff per file, the AUTO count and the REVIEW
list, and writes nothing. ``--report`` also writes all of that as Markdown. ``--apply``
writes the AUTO conversions (never the REVIEW ones) through docs/tools/textio.py: one BOM
if the file had one, line endings kept, every byte outside the converted quote characters
unchanged. Default paths: localization/ (every *.yml under it).

How a value is read (one line, ` key:N "value" # comment`): from the first `"` after the
key to the last `"` before an optional trailing comment. A line whose comment itself holds
a `"` is ambiguous and goes to REVIEW (eotg_lint L013e reports it as an ERROR).

Detection, per value:
  - masked first, so nothing in them is ever touched: `[ ... ]` data functions (so
    Custom('X') is safe), `$KEY$`, `#FMT` / `#!` tokens, literal `\\n`;
  - a `'` with a letter or digit on BOTH sides (don't, Konan's) is skipped outright;
  - opener: a `'` at value start or after whitespace, `\\n`, `(` or `:`, followed by a
    non-space;
  - AUTO closer: a `'` right after one of . , ! ? and followed by the end, whitespace, `\\n`
    or one of , . ; : )
  - a value converts automatically only when every `'` in it falls into opener + AUTO-closer
    pairs on one paragraph with no masked token inside. Anything else sends the whole value
    to REVIEW, unconverted: a closer after a letter (a quoted single word 'we', a
    possessive plural soldiers'), an unpaired or word-initial `'` ('em), a pair spanning
    `\\n\\n`, a pair with a masked token inside;
  - converts to an unescaped `"`, never `\\"`;
  - post-check on every converted value: the inner `"` count is even, there is no `\\"`, no
    `'` delimiter is left inside a converted span, and swapping the new `"` back to `'`
    gives the old value byte for byte.

Standard library only. Library use: ``analyze_value(value)`` -> Analysis (eotg_lint L013e,
docs/tools/qa/loc_mechanical.py and eotg_event_quality.py share it).
"""
import argparse
import difflib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import textio  # noqa: E402

DEFAULT_ROOT = os.path.dirname(os.path.dirname(HERE))

# ` key:N "value"  # comment` ; group 'value' is greedy, up to the last quote on the line
LINE_RE = re.compile(r'^(?P<pre>\s+[^\s:#"]+:\d*\s*")(?P<value>.*)(?P<post>"\s*(?:#.*)?)$')
# a trailing comment holding a quote: `..." # say "hi"` makes the greedy value wrong
COMMENT_QUOTE_RE = re.compile(r'"\s+#(?:\s|$)[^"]*"')

AUTO_PREV = ".,!?"
AUTO_NEXT = ",.;:)"


class Issue:
    __slots__ = ("kind", "pos", "message")

    def __init__(self, kind, pos, message):
        self.kind, self.pos, self.message = kind, pos, message

    def __repr__(self):
        return "Issue(%s@%d)" % (self.kind, self.pos)


class Analysis:
    """What one loc value holds.

    pairs: [(open, close)] AUTO-shaped speech pairs (indices into the value);
    issues: [Issue] anything that stops automatic conversion;
    proposed: the converted value if every pair-like span were converted (None if no pair);
    auto: True when the value converts automatically (pairs, no issues)."""

    def __init__(self, value, pairs, issues, proposed, speechlike):
        self.value = value
        self.pairs = pairs
        self.issues = issues
        self.proposed = proposed
        self.speechlike = speechlike     # [(open, close)] every paired span, AUTO or not

    @property
    def auto(self):
        return bool(self.pairs) and not self.issues

    @property
    def has_single_quote_speech(self):
        """True when the value holds '...' used as quotation (what L013e warns on)."""
        return bool(self.speechlike)


def mask(value):
    """A list of booleans, True where the character is inside a masked token."""
    m = [False] * len(value)
    i, n = 0, len(value)
    while i < n:
        c = value[i]
        if c == "[":
            depth, j = 0, i
            while j < n:
                if value[j] == "[":
                    depth += 1
                elif value[j] == "]":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            j = min(j, n - 1)
            for k in range(i, j + 1):
                m[k] = True
            i = j + 1
            continue
        if c == "$":
            j = value.find("$", i + 1)
            if j > i + 1 and re.match(r"^[A-Za-z0-9_.\-|]+$", value[i + 1:j]):
                for k in range(i, j + 1):
                    m[k] = True
                i = j + 1
                continue
        if c == "#":
            t = re.match(r"#(!|[A-Za-z_][A-Za-z0-9_;]*)", value[i:])
            if t:
                for k in range(i, i + len(t.group(0))):
                    m[k] = True
                i += len(t.group(0))
                continue
        if c == "\\" and i + 1 < n and value[i + 1] == "n":
            m[i] = m[i + 1] = True
            i += 2
            continue
        i += 1
    return m


def _prev_raw(value, i):
    return value[i - 1] if i > 0 else ""


def _after_newline(value, i):
    return i >= 2 and value[i - 2:i] == "\\n"


def _before_newline(value, i):
    return value[i + 1:i + 3] == "\\n"


def classify(value, i, m=None):
    """Kind of the ' at value[i]: intraword | opener | auto_close | letter_close |
    other_close | stray. ``m`` is mask(value); a masked neighbour ([x.GetName], $KEY$)
    counts as a word character, so [x.GetName]'s is a possessive, never a quote. A literal
    \n before or after counts as whitespace."""
    m = mask(value) if m is None else m
    n = len(value)
    if _after_newline(value, i):
        p = " "
    elif i > 0 and m[i - 1] and value[i - 1] in "]$":
        p = "a"
    else:
        p = _prev_raw(value, i)
    if _before_newline(value, i):
        nx = " "
    elif i + 1 < n and m[i + 1] and value[i + 1] in "[$":
        nx = "a"
    else:
        nx = value[i + 1] if i + 1 < n else ""
    if p.isalnum() and nx.isalnum():
        return "intraword"
    opener_ctx = i == 0 or p.isspace() or p in "(:"
    if opener_ctx and nx and not nx.isspace():
        return "opener"
    end_ctx = nx == "" or nx.isspace()
    if p and not p.isspace() and (end_ctx or nx in AUTO_NEXT or nx in "!?"):
        if p in AUTO_PREV and (end_ctx or nx in AUTO_NEXT):
            return "auto_close"
        if p.isalnum():
            return "letter_close"
        return "other_close"
    return "stray"


def analyze_value(value):
    m = mask(value)
    pairs, issues, speechlike = [], [], []
    open_at = None
    for i, c in enumerate(value):
        if c != "'" or m[i]:
            continue
        kind = classify(value, i, m)
        if kind == "intraword":
            continue
        if kind == "opener":
            if open_at is None:
                open_at = i
            else:
                issues.append(Issue("word-initial", i, "a word-initial ' (like 'em) or nested "
                                    "quote inside an open quote"))
            continue
        if kind == "stray":
            issues.append(Issue("stray", i, "a ' that is neither an opener nor a closer"))
            continue
        # a closer
        if open_at is None:
            if kind == "letter_close":
                issues.append(Issue("possessive", i, "a ' after a letter with no opener: "
                                    "possessive plural (soldiers') or an unpaired closer"))
            else:
                issues.append(Issue("unpaired-close", i, "a closing ' with no opener"))
            continue
        span = value[open_at:i + 1]
        speechlike.append((open_at, i))
        if kind == "letter_close":
            issues.append(Issue("single-word", open_at, "closer after a letter: a quoted single "
                                "word ('we') or a possessive inside speech"))
        elif kind == "other_close":
            issues.append(Issue("odd-close", i, "closer after punctuation other than . , ! ?"))
        elif "\\n\\n" in span:
            issues.append(Issue("paragraphs", open_at, "speech spans \\n\\n (multi-paragraph)"))
        elif any(m[open_at:i + 1]):
            issues.append(Issue("masked-inside", open_at, "a [function], $KEY$, #format or \\n "
                                "inside the speech"))
        else:
            pairs.append((open_at, i))
        open_at = None
    if open_at is not None:
        issues.append(Issue("unpaired-open", open_at, "an opening ' with no closer"))
    proposed = None
    if speechlike:
        chars = list(value)
        for a, b in speechlike:
            chars[a] = chars[b] = '"'
        proposed = "".join(chars)
    return Analysis(value, pairs, issues, proposed, speechlike)


class PostCheckError(AssertionError):
    pass


def convert_value(value):
    """(new_value, analysis). new_value == value unless the value converts automatically."""
    a = analyze_value(value)
    if not a.auto:
        return value, a
    chars = list(value)
    for o, c in a.pairs:
        chars[o] = chars[c] = '"'
    new = "".join(chars)
    post_check(value, new, a.pairs)
    return new, a


def post_check(old, new, pairs):
    if len(old) != len(new):
        raise PostCheckError("length changed")
    changed = [i for i, (x, y) in enumerate(zip(old, new)) if x != y]
    want = sorted(i for p in pairs for i in p)
    if changed != want or any(old[i] != "'" or new[i] != '"' for i in changed):
        raise PostCheckError("characters other than the paired quotes changed")
    if new.count('"') % 2:
        raise PostCheckError("odd number of inner double quotes")
    if '\\"' in new:
        raise PostCheckError('escaped \\" in the converted value')
    m = mask(new)
    for o, c in pairs:
        for k in range(o + 1, c):
            if new[k] == "'" and not m[k] and classify(new, k, m) != "intraword":
                raise PostCheckError("a ' delimiter is left inside a converted span")


def split_line(line):
    """(pre, value, post) of a loc line, or None. `line` has no line ending."""
    m = LINE_RE.match(line)
    if not m:
        return None
    return m.group("pre"), m.group("value"), m.group("post")


def key_of(pre):
    return pre.strip().split(":", 1)[0]


class FileResult:
    def __init__(self, rel):
        self.rel = rel
        self.old_lines = []
        self.new_lines = []
        self.auto = []      # (line_no, key, old, new)
        self.review = []    # (line_no, key, value, [Issue], proposed)


def process_text(text, rel="<text>"):
    """text (no BOM) -> FileResult. Line endings are kept on every line."""
    res = FileResult(rel)
    lines = text.splitlines(keepends=True)
    for no, raw in enumerate(lines, 1):
        body = raw.rstrip("\r\n")
        end = raw[len(body):]
        res.old_lines.append(raw)
        parts = split_line(body)
        if parts is None or "'" not in parts[1]:
            res.new_lines.append(raw)
            continue
        pre, value, post = parts
        key = key_of(pre)
        if COMMENT_QUOTE_RE.search(body):
            res.review.append((no, key, value, [Issue("comment-quote", 0, "a trailing # comment "
                               "holds a \" so the value boundary is ambiguous")], None))
            res.new_lines.append(raw)
            continue
        new, a = convert_value(value)
        if a.auto:
            new_body = pre + new + post
            assert new_body.replace('"', "'") == body.replace('"', "'"), rel
            res.auto.append((no, key, value, new))
            res.new_lines.append(new_body + end)
        else:
            if a.issues and (a.speechlike or any(i.kind in ("unpaired-open", "word-initial",
                                                               "possessive", "unpaired-close",
                                                               "stray", "odd-close")
                                                    for i in a.issues)):
                res.review.append((no, key, value, a.issues, a.proposed))
            res.new_lines.append(raw)
    return res


def iter_paths(root, paths):
    targets = paths or [os.path.join(root, "localization")]
    for t in targets:
        t = t if os.path.isabs(t) else os.path.join(root, t)
        if os.path.isfile(t):
            yield t
            continue
        for d, dirs, files in os.walk(t):
            dirs.sort()
            for f in sorted(files):
                if f.lower().endswith(".yml"):
                    yield os.path.join(d, f)


def _rel(root, p):
    return os.path.relpath(p, root).replace(os.sep, "/")


def run(root, paths=(), apply=False):
    results = []
    for p in iter_paths(root, list(paths)):
        text, had_bom = textio.read_text(p)
        res = process_text(text, _rel(root, p))
        res.had_bom = had_bom
        res.path = p
        results.append(res)
        if apply and res.auto:
            new_text = "".join(res.new_lines)
            # every changed byte is a ' -> " swap
            assert len(new_text) == len(text) and new_text.replace('"', "'") == \
                text.replace('"', "'"), p
            textio.write_text(p, new_text, bom=had_bom, newline=None)
    return results


def diff_text(res):
    return "".join(difflib.unified_diff(
        [l if l.endswith("\n") else l + "\n" for l in (x.rstrip("\r\n") + "\n" for x in res.old_lines)],
        [l if l.endswith("\n") else l + "\n" for l in (x.rstrip("\r\n") + "\n" for x in res.new_lines)],
        "a/" + res.rel, "b/" + res.rel, n=0))


def summary(results):
    auto = sum(len(r.auto) for r in results)
    review = sum(len(r.review) for r in results)
    return auto, review


def format_report(results, applied=False, command=None):
    auto, review = summary(results)
    out = ["# Quote conversion %s (event_quality_v1 W0e)" % ("applied" if applied else "dry run"),
           "",
           "Generated by `%s`. " % (command or "python docs/tools/eotg_quote_convert.py --report <file>") +
           "%s Rules: `docs/tools/eotg_quote_convert.py` docstring and "
           "`docs/specs/event_quality_v1.md` W0e." % (
               "Written to disk." if applied else "**Nothing was written**; `--apply` converts the AUTO keys only."),
           "",
           "**AUTO (converted automatically): %d key(s). REVIEW (left unchanged, resolve by hand): %d key(s).**"
           % (auto, review),
           "",
           "| File | AUTO | REVIEW |", "|---|---|---|"]
    for r in results:
        if r.auto or r.review:
            out.append("| `%s` | %d | %d |" % (r.rel, len(r.auto), len(r.review)))
    groups = (("Quotation: needs a decision", lambda e: e[4] is not None),
              ("Apostrophe only (possessive plural, word-initial ', unpaired): most need no "
               "change", lambda e: e[4] is None))
    out += ["", "## REVIEW list", "",
            "Each entry: file:line, key, why, and the value. *Proposed* converts every paired "
            "span, for the localizer to accept or edit; it was **not** applied.", ""]
    n = 0
    for title, pick in groups:
        entries = [(r, e) for r in results for e in r.review if pick(e)]
        out += ["### %s (%d)" % (title, len(entries)), ""]
        for r, (no, key, value, issues, proposed) in entries:
            n += 1
            why = "; ".join(sorted({"%s (%s)" % (i.kind, i.message) for i in issues}))
            out.append("%d. `%s:%d` **%s**: %s" % (n, r.rel, no, key, why))
            out.append("   - value: `%s`" % value.replace("`", "'"))
            if proposed is not None and proposed != value:
                out.append("   - proposed: `%s`" % proposed.replace("`", "'"))
        if not entries:
            out.append("(none)")
        out.append("")
    out += ["## Unified diff (AUTO conversions)", ""]
    for r in results:
        if r.auto:
            out += ["```diff", diff_text(r).rstrip("\n"), "```", ""]
    return "\n".join(out).rstrip("\n") + "\n"


def main(argv=None):
    try:
        import pdx_parse
        pdx_parse.utf8_console()
    except ImportError:
        pass
    ap = argparse.ArgumentParser(description="Convert '...' speech in loc to unescaped \"...\" "
                                 "(dry run unless --apply).")
    ap.add_argument("paths", nargs="*", help="files or folders (default: localization/)")
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--apply", action="store_true", help="write the AUTO conversions")
    ap.add_argument("--report", metavar="OUT.md", help="also write the diff and REVIEW list")
    ap.add_argument("--quiet", action="store_true", help="print only the counts")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    results = run(root, args.paths, apply=args.apply)
    if not args.quiet:
        for r in results:
            d = diff_text(r)
            if d:
                print(d, end="")
        for r in results:
            for no, key, value, issues, proposed in r.review:
                print("REVIEW %s:%d %s: %s" % (r.rel, no, key,
                                               ", ".join(sorted({i.kind for i in issues}))))
    if args.report:
        cmd = "python docs/tools/eotg_quote_convert.py %s" % " ".join(
            (list(args.paths) or []) + (["--apply"] if args.apply else [])
            + ["--report", args.report.replace(os.sep, "/")])
        textio.write_text(args.report, format_report(results, args.apply, cmd), bom=False,
                          makedirs=True)
    auto, review = summary(results)
    print("%s: AUTO %d key(s), REVIEW %d key(s)%s" % (
        "applied" if args.apply else "dry run", auto, review,
        "" if args.apply else " (nothing written; --apply converts AUTO only)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
