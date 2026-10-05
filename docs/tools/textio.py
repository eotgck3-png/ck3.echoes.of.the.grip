"""Text file I/O for the tools: at most one BOM, only at byte 0, and only on request.

Why (docs/pitfalls.md §14): re-saving a file that already starts with a BOM through
``encoding="utf-8-sig"`` without stripping the old one stacks a second BOM. CK3 strips
one and reads the next as part of the first key; in common/script_values/ that broke the
named-value table (~26,000 parse errors, then a crash on load). So every tool reads and
writes text through here:

    text, had_bom = read_text(path)              # every leading BOM stripped
    write_text(path, text, bom=True)             # exactly one BOM, at byte 0
    write_text(path, text, bom=False)            # none

``write_text`` refuses text that holds U+FEFF anywhere but the very start, so a stray BOM
can't be written back out silently. Standard library only.
"""
import os

BOM = b"\xef\xbb\xbf"
BOM_CHAR = "﻿"


def strip_boms(text):
    """Drop every leading U+FEFF (one, or a stacked run)."""
    return text.lstrip(BOM_CHAR)


def decode(raw, errors="replace"):
    """bytes -> (text, had_bom). Every leading BOM is stripped; had_bom says if any was there."""
    had = raw.startswith(BOM)
    return strip_boms(raw.decode("utf-8", errors=errors)), had


def read_text(path, errors="replace"):
    """Read a UTF-8 text file. Returns (text, had_bom), every leading BOM stripped."""
    with open(path, "rb") as fh:
        return decode(fh.read(), errors)


def read_lines(path, errors="replace"):
    """The lines of a text file, as iterating an open file would give them (universal
    newlines; only \\n, \\r\\n and \\r end a line), without the line ends."""
    text = read_text(path, errors)[0].replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def encode(text, bom, newline="\n"):
    """text -> bytes with exactly one BOM (bom=True) or none (bom=False).

    Leading BOMs in ``text`` are dropped first; U+FEFF anywhere else raises ValueError.
    ``newline``: "\\n" or "\\r\\n" normalises line endings; None leaves them as they are."""
    if bom not in (True, False):
        raise TypeError("bom must be True or False, not %r" % (bom,))
    text = strip_boms(text)
    at = text.find(BOM_CHAR)
    if at >= 0:
        line = text.count("\n", 0, at) + 1
        raise ValueError("U+FEFF inside the text (line %d, char %d); refusing to write it" % (line, at))
    if newline is not None:
        text = text.replace("\r\n", "\n")
        if newline != "\n":
            text = text.replace("\n", newline)
    return (BOM if bom else b"") + text.encode("utf-8")


def write_text(path, text, bom, newline="\n", makedirs=False):
    """Write ``text`` with exactly one BOM (bom=True) or none (bom=False). See encode()."""
    data = encode(text, bom, newline)
    if makedirs:
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)


def stray_bom_offsets(raw):
    """Byte offsets of every BOM in ``raw`` except a single one at byte 0.

    A stacked BOM (EF BB BF EF BB BF ...) reports offset 3 (and 6, ...)."""
    out, i = [], raw.find(BOM, 1)
    while i >= 0:
        out.append(i)
        i = raw.find(BOM, i + len(BOM))
    return out


def count_boms(raw):
    return (1 if raw.startswith(BOM) else 0) + len(stray_bom_offsets(raw))
