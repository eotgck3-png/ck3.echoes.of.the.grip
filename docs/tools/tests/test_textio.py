"""Tests for docs/tools/textio.py: at most one BOM, only at byte 0 (docs/pitfalls.md §14).

Run: python -m unittest discover docs/tools/tests
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _testutil import rmtree  # noqa: E402
import textio as T  # noqa: E402

B = T.BOM


class TextIO(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="eotg_textio_")
        self.addCleanup(rmtree, self.d)
        self.p = os.path.join(self.d, "f.txt")

    def raw(self):
        with open(self.p, "rb") as fh:
            return fh.read()

    def put(self, data):
        with open(self.p, "wb") as fh:
            fh.write(data)

    def test_read_strips_every_leading_bom(self):
        self.put(B * 3 + b"a = 1\n")
        self.assertEqual(T.read_text(self.p), ("a = 1\n", True))
        self.put(b"a = 1\n")
        self.assertEqual(T.read_text(self.p), ("a = 1\n", False))

    def test_write_one_bom_or_none(self):
        T.write_text(self.p, "a = 1\n", bom=True)
        self.assertEqual(self.raw(), B + b"a = 1\n")
        T.write_text(self.p, "﻿﻿a = 1\n", bom=True)   # stacked in the text: one out
        self.assertEqual(self.raw(), B + b"a = 1\n")
        T.write_text(self.p, "﻿a = 1\n", bom=False)
        self.assertEqual(self.raw(), b"a = 1\n")

    def test_the_bug_cannot_recur(self):
        # the 2026-10-04 crash: read a BOM file, write it back with a BOM, twice
        self.put(B + b"x = 1\n")
        for _ in range(2):
            T.write_text(self.p, T.read_text(self.p)[0], bom=True)
        self.assertEqual(T.count_boms(self.raw()), 1)
        self.assertTrue(self.raw().startswith(B))

    def test_write_refuses_a_mid_text_bom(self):
        with self.assertRaises(ValueError) as cm:
            T.write_text(self.p, "a = 1\nb﻿ = 2\n", bom=True)
        self.assertIn("line 2", str(cm.exception))
        self.assertFalse(os.path.exists(self.p))

    def test_bom_must_be_explicit(self):
        with self.assertRaises(TypeError):
            T.write_text(self.p, "x", bom=None)

    def test_newlines(self):
        T.write_text(self.p, "a\r\nb\n", bom=False)
        self.assertEqual(self.raw(), b"a\nb\n")
        T.write_text(self.p, "a\nb\n", bom=False, newline="\r\n")
        self.assertEqual(self.raw(), b"a\r\nb\r\n")
        T.write_text(self.p, "a\r\nb\n", bom=False, newline=None)
        self.assertEqual(self.raw(), b"a\r\nb\n")

    def test_stray_offsets(self):
        self.assertEqual(T.stray_bom_offsets(B + b"x"), [])
        self.assertEqual(T.stray_bom_offsets(B * 3 + b"x"), [3, 6])
        self.assertEqual(T.stray_bom_offsets(b"ab" + B + b"c"), [2])
        self.assertEqual(T.count_boms(B * 2 + b"x" + B), 3)
        self.assertEqual(T.count_boms(b"x"), 0)

    def test_read_lines_matches_file_iteration(self):
        self.put(B + "a\r\nb c\nd".encode("utf-8"))
        with open(self.p, encoding="utf-8-sig") as fh:
            want = [l.rstrip("\n") for l in fh]
        self.assertEqual(T.read_lines(self.p), want)
        self.assertEqual(T.read_lines(self.p), ["a", "b c", "d"])


if __name__ == "__main__":
    unittest.main()
