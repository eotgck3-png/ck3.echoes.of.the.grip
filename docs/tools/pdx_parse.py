"""Reusable Paradox-script (CK3) parser with line numbers. Standard library only.

Generalises docs/tools/qa/aug_parse.py (which now delegates to this module):

* nested ``key = value`` and ``key = { ... }`` blocks
* ``#`` comments (outside quotes); optionally kept and attached to nodes
* quoted strings (``"..."``), ``@vars`` and ``@[ inline math ]``
* operators ``=`` ``==`` ``<`` ``<=`` ``>`` ``>=`` ``!=`` ``?=``
* bare list items inside blocks (``tenets = { a b c }``) and anonymous blocks
* tagged blocks such as ``color = hsv { 0.1 0.2 0.3 }``
* a UTF-8 BOM and CRLF line endings
* every node records the 1-based line it starts on

It is tolerant: unbalanced braces or a dangling operator are recorded in
``Document.errors`` instead of raising, so a linter can report and move on.
Tiger stays the authority on syntax; this is a reader, not a validator.

Usage::

    from pdx_parse import parse_file, walk
    doc = parse_file("events/foo.txt")
    for node, parents in walk(doc.nodes):
        print(node.line, node.key, node.op, node.value)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textio  # noqa: E402

__all__ = [
    "Node", "Document", "ParseError", "OPERATORS", "TAGS",
    "tokenize", "parse_text", "parse_file", "read_text",
    "walk", "find", "find_all", "first", "to_tuples", "dump",
]

OPERATORS = ("?=", "<=", ">=", "!=", "==", "=", "<", ">")
# Words that may prefix a value block: ``color = hsv { ... }``
TAGS = ("rgb", "hsv", "hsv360", "hex", "LIST")

_TOKEN_RE = re.compile(
    r'(?P<nl>\r\n|\n|\r)'
    r'|(?P<ws>[ \t\f\v﻿]+)'
    r'|(?P<comment>#[^\r\n]*)'
    r'|(?P<str>"(?:[^"\\\r\n]|\\.)*"?)'
    r'|(?P<math>@\[[^\]]*\]?)'
    r'|(?P<op>\?=|<=|>=|!=|==|=|<|>)'
    r'|(?P<lb>\{)'
    r'|(?P<rb>\})'
    r'|(?P<word>[^\s{}<>=!?"#]+|[!?])'
)


class ParseError(Exception):
    pass


class Token:
    __slots__ = ("kind", "text", "line")

    def __init__(self, kind, text, line):
        self.kind = kind      # word | str | op | lb | rb | comment
        self.text = text
        self.line = line

    def __repr__(self):
        return "Token(%s, %r, %d)" % (self.kind, self.text, self.line)


class Node:
    """One statement.

    * ``key = value``  -> key, op, value (str)
    * ``key = { .. }`` -> key, op, value (list of Node)
    * bare item ``a``  -> key="a", op=None, value=None  (``is_bare``)
    * anonymous ``{ }``-> key=None, op=None, value (list of Node)
    """
    __slots__ = ("key", "op", "value", "line", "end_line", "quoted",
                 "key_quoted", "tag", "comments", "trailing")

    def __init__(self, key, op, value, line, quoted=False, key_quoted=False,
                 tag=None):
        self.key = key
        self.op = op
        self.value = value
        self.line = line
        self.end_line = line
        self.quoted = quoted          # value was a quoted string
        self.key_quoted = key_quoted
        self.tag = tag                # e.g. "hsv" in ``color = hsv { }``
        self.comments = []            # full-line comments directly above
        self.trailing = None          # comment on the same line, after it

    @property
    def is_block(self):
        return isinstance(self.value, list)

    @property
    def is_bare(self):
        return self.op is None and self.value is None and self.key is not None

    @property
    def children(self):
        return self.value if isinstance(self.value, list) else []

    def __repr__(self):
        if self.is_block:
            return "Node(%r %s {%d} @%d)" % (self.key, self.op, len(self.value), self.line)
        return "Node(%r %s %r @%d)" % (self.key, self.op, self.value, self.line)


class Document:
    def __init__(self, nodes, errors, path=None, bom=False):
        self.nodes = nodes
        self.errors = errors        # list of (line, message)
        self.path = path
        self.bom = bom
        self.footer_comments = []   # comments after the last node of the file

    def __iter__(self):
        return iter(self.nodes)


# ------------------------------------------------------------------ console
# FIX 8: a Windows console or pipe in cp1252 cannot encode the arrows and
# section signs the tools print. Every CLI calls utf8_console() first.
ASCII_FALLBACK = {0x2192: "->", 0x2190: "<-", 0x2014: "-", 0x2013: "-", 0x00a7: "S",
                  0x2026: "...", 0x00d7: "x", 0x2265: ">=", 0x2264: "<="}


class _AsciiWriter:
    """Wraps a text stream that cannot be reconfigured: maps the common
    non-ASCII symbols to ASCII and replaces anything else it cannot encode."""

    def __init__(self, stream):
        self._stream = stream
        self.encoding = getattr(stream, "encoding", None) or "ascii"

    def write(self, text):
        text = text.translate(ASCII_FALLBACK)
        text = text.encode(self.encoding, errors="replace").decode(self.encoding, errors="replace")
        return self._stream.write(text)

    def __getattr__(self, name):
        return getattr(self._stream, name)


def _can_encode(stream, sample="\u2192"):
    enc = getattr(stream, "encoding", None)
    if not enc:
        return True     # e.g. io.StringIO: takes any str
    try:
        sample.encode(enc)
        return True
    except (UnicodeEncodeError, LookupError):
        return False


def utf8_console():
    """Make sys.stdout / sys.stderr safe for UTF-8 output: reconfigure to
    UTF-8 (errors=replace) when the stream allows it, else wrap it so the
    tool prints ASCII ("->") instead of crashing."""
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name)
        if stream is None or _can_encode(stream):
            continue
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
            continue
        except (AttributeError, ValueError, OSError):
            pass
        setattr(sys, name, _AsciiWriter(stream))


def read_text(path):
    """Read a script file as text. Returns (text, had_bom). Tolerates bad bytes.
    Every leading BOM is stripped (textio; a stacked BOM is eotg_lint L016's job)."""
    return textio.read_text(path)


def tokenize(text, keep_comments=False):
    """Split text into Tokens. Newlines and whitespace are dropped."""
    text = textio.strip_boms(text)
    tokens = []
    line = 1
    for m in _TOKEN_RE.finditer(text):
        kind = m.lastgroup
        if kind == "nl":
            line += 1
            continue
        if kind == "ws":
            continue
        val = m.group(kind)
        if kind == "comment":
            if keep_comments:
                tokens.append(Token("comment", val, line))
            continue
        if kind == "math":
            kind = "word"
        tokens.append(Token(kind, val, line))
        # a quoted string or inline math may span lines only if malformed;
        # count embedded newlines anyway so later line numbers stay right
        line += val.count("\n")
    return tokens


def _unquote(s):
    if len(s) >= 2 and s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s.strip('"')


class _Parser:
    def __init__(self, tokens, keep_comments):
        self.t = tokens
        self.i = 0
        self.errors = []
        self.keep = keep_comments
        self.last_line = 0

    def peek(self, skip_comments=True):
        j = self.i
        while j < len(self.t):
            if skip_comments and self.t[j].kind == "comment":
                j += 1
                continue
            return self.t[j], j
        return None, j

    def block(self, depth, open_line=0):
        nodes = []
        pending = []
        while self.i < len(self.t):
            tok = self.t[self.i]
            if tok.kind == "comment":
                self.i += 1
                last = nodes[-1] if nodes else None
                if last is not None and not pending and last.trailing is None \
                        and tok.line == last.end_line \
                        and (not last.is_block or last.line == last.end_line):
                    nodes[-1].trailing = tok.text
                else:
                    pending.append(tok.text)
                continue
            if tok.kind == "rb":
                self.i += 1
                if depth > 0:
                    return nodes, pending, tok.line
                self.errors.append((tok.line, "unexpected '}'"))
                continue
            if tok.kind == "lb":
                self.i += 1
                children, tail, end = self.block(depth + 1, tok.line)
                if tail and self.keep:
                    children.append(_comment_node(tail, end))
                n = Node(None, None, children, tok.line)
                n.end_line = end
                self._attach(n, pending)
                pending = []
                nodes.append(n)
                continue
            if tok.kind == "op":
                self.errors.append((tok.line, "operator %r without a key" % tok.text))
                self.i += 1
                continue
            # word or str
            self.i += 1
            nxt, j = self.peek()
            if nxt is not None and nxt.kind == "op":
                self.i = j + 1
                n = self._assignment(tok, nxt, depth)
            else:
                n = Node(_unquote(tok.text), None, None, tok.line,
                         key_quoted=(tok.kind == "str"))
            self._attach(n, pending)
            pending = []
            nodes.append(n)
        if depth > 0:
            self.errors.append((open_line, "unclosed '{' (opened here)"))
        return nodes, pending, (self.t[-1].line if self.t else 0)

    def _attach(self, node, pending):
        if self.keep:
            node.comments = list(pending)

    def _assignment(self, keytok, optok, depth):
        key = _unquote(keytok.text)
        kq = keytok.kind == "str"
        val, j = self.peek()
        if val is None or val.kind == "rb":
            self.errors.append((optok.line, "no value after %s %s" % (key, optok.text)))
            n = Node(key, optok.text, "", keytok.line, key_quoted=kq)
            return n
        if val.kind == "lb":
            self.i = j + 1
            children, tail, end = self.block(depth + 1, val.line)
            if tail and self.keep:
                children.append(_comment_node(tail, end))
            n = Node(key, optok.text, children, keytok.line, key_quoted=kq)
            n.end_line = end
            return n
        if val.kind == "op":
            self.errors.append((val.line, "unexpected operator %r" % val.text))
            self.i = j + 1
            return Node(key, optok.text, "", keytok.line, key_quoted=kq)
        # word / str value; maybe a tagged block: hsv { ... }
        self.i = j + 1
        if val.kind == "word" and val.text in TAGS:
            nxt, k = self.peek()
            if nxt is not None and nxt.kind == "lb":
                self.i = k + 1
                children, tail, end = self.block(depth + 1, nxt.line)
                if tail and self.keep:
                    children.append(_comment_node(tail, end))
                n = Node(key, optok.text, children, keytok.line, key_quoted=kq, tag=val.text)
                n.end_line = end
                return n
        n = Node(key, optok.text, _unquote(val.text), keytok.line,
                 quoted=(val.kind == "str"), key_quoted=kq)
        n.end_line = val.line
        return n


def _comment_node(texts, line):
    """Pseudo-node carrying comments that close a block (key '#')."""
    n = Node("#", None, None, line)
    n.comments = list(texts)
    return n


def parse_text(text, path=None, keep_comments=False):
    """Parse script text into a Document."""
    bom = text.startswith("﻿")
    tokens = tokenize(text, keep_comments=keep_comments)
    p = _Parser(tokens, keep_comments)
    nodes, tail, _ = p.block(0)
    doc = Document(nodes, p.errors, path=path, bom=bom)
    if keep_comments:
        doc.footer_comments = tail
    return doc


def parse_file(path, keep_comments=False):
    text, bom = read_text(path)
    doc = parse_text(text, path=path, keep_comments=keep_comments)
    doc.bom = bom
    return doc


def walk(nodes, parents=()):
    """Depth-first: yields (node, parents_tuple) for every node."""
    for n in nodes:
        if n.key == "#" and n.op is None and n.value is None and n.comments:
            continue  # comment pseudo-node
        yield n, parents
        if isinstance(n.value, list):
            yield from walk(n.value, parents + (n,))


def find(nodes, key):
    """Direct children named key."""
    return [n for n in nodes if n.key == key and not (n.key == "#" and n.op is None)]


def first(nodes, key, default=None):
    for n in nodes:
        if n.key == key:
            return n
    return default


def find_all(nodes, key):
    """Every descendant (any depth) named key."""
    return [n for n, _ in walk(nodes) if n.key == key]


def to_tuples(nodes, keep_quotes=True):
    """Convert to aug_parse's (key, op, value) tuple shape.

    A tagged block ``hsv { }`` becomes the value tag followed by an anonymous
    block, exactly as aug_parse's tokenizer used to produce it.
    """
    out = []
    for n in nodes:
        if n.key == "#" and n.op is None and n.value is None:
            continue
        key = ('"%s"' % n.key) if (n.key_quoted and keep_quotes) else n.key
        if isinstance(n.value, list):
            kids = to_tuples(n.value, keep_quotes)
            if n.tag:
                out.append((key, n.op, n.tag))
                out.append((None, None, kids))
            else:
                out.append((key, n.op, kids))
        elif n.op is None:
            out.append((key, None, None))
        else:
            v = n.value
            if n.quoted and keep_quotes:
                v = '"%s"' % v
            out.append((key, n.op, v))
    return out


# --------------------------------------------------------------------- dump
def _fmt_atom(s, quoted):
    if quoted or s == "" or re.search(r'[\s{}=<>#"]', s):
        return '"%s"' % s
    return s


def _is_simple_list(children):
    return children and all(c.is_bare and not c.comments and not c.trailing
                            and c.key != "#" for c in children)


def dump(nodes, indent=0, tab="\t", inline_lists=True):
    """Serialise nodes back to script text (comments kept if attached)."""
    lines = []
    pad = tab * indent
    for n in nodes:
        for c in n.comments:
            lines.append(pad + c)
        if n.key == "#" and n.op is None and n.value is None:
            continue
        key = _fmt_atom(n.key, n.key_quoted) if n.key is not None else None
        trail = (" " + n.trailing) if n.trailing else ""
        if isinstance(n.value, list):
            head = "{" if key is None else "%s %s %s{" % (key, n.op or "=",
                                                         (n.tag + " ") if n.tag else "")
            if inline_lists and _is_simple_list(n.value) and len(n.value) <= 12:
                items = " ".join(_fmt_atom(c.key, c.key_quoted) for c in n.value)
                lines.append("%s%s %s }%s" % (pad, head, items, trail))
            elif not n.value:
                lines.append("%s%s }%s" % (pad, head, trail))
            else:
                lines.append(pad + head + trail)
                lines.extend(dump(n.value, indent + 1, tab, inline_lists).split("\n"))
                lines.append(pad + "}")
        elif n.op is None:
            lines.append(pad + key + trail)
        else:
            lines.append("%s%s %s %s%s" % (pad, key, n.op, _fmt_atom(n.value, n.quoted), trail))
    return "\n".join(lines)
