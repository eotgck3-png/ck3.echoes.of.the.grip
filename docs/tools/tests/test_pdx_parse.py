"""Tests for docs/tools/pdx_parse.py.  Run: python -m unittest discover docs/tools/tests"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pdx_parse as P  # noqa: E402


class ParseBasics(unittest.TestCase):
    def test_nested_blocks_and_lines(self):
        doc = P.parse_text("a = 1\nb = {\n  c = d\n  e = { f = g }\n}\n")
        self.assertEqual(doc.errors, [])
        a, b = doc.nodes
        self.assertEqual((a.key, a.op, a.value, a.line), ("a", "=", "1", 1))
        self.assertTrue(b.is_block)
        self.assertEqual(b.line, 2)
        self.assertEqual(b.end_line, 5)
        c = P.first(b.value, "c")
        self.assertEqual((c.value, c.line), ("d", 3))
        f = P.find_all(doc.nodes, "f")[0]
        self.assertEqual((f.value, f.line), ("g", 4))

    def test_comments_ignored_outside_quotes(self):
        doc = P.parse_text('a = "x # not a comment" # real comment\nb = 2 # c')
        self.assertEqual(doc.nodes[0].value, "x # not a comment")
        self.assertTrue(doc.nodes[0].quoted)
        self.assertEqual(len(doc.nodes), 2)

    def test_operators(self):
        doc = P.parse_text("t = { a < 1 b <= 2 c > 3 d >= 4 e != 5 f ?= 6 g == 7 }")
        ops = [(n.key, n.op) for n in doc.nodes[0].value]
        self.assertEqual(ops, [("a", "<"), ("b", "<="), ("c", ">"), ("d", ">="),
                               ("e", "!="), ("f", "?="), ("g", "==")])

    def test_question_equals_without_spaces(self):
        doc = P.parse_text("t = { var:x?=flag:y }")
        n = doc.nodes[0].value[0]
        self.assertEqual((n.key, n.op, n.value), ("var:x", "?=", "flag:y"))

    def test_bare_list_items(self):
        doc = P.parse_text("tenets = { tenet_a tenet_b tenet_c }")
        items = doc.nodes[0].value
        self.assertTrue(all(i.is_bare for i in items))
        self.assertEqual([i.key for i in items], ["tenet_a", "tenet_b", "tenet_c"])

    def test_vars_and_inline_math(self):
        doc = P.parse_text("@cost = 50\nx = { gold = @cost y = @[ cost * 2 ] }")
        self.assertEqual(doc.nodes[0].key, "@cost")
        x = doc.nodes[1].value
        self.assertEqual(x[0].value, "@cost")
        self.assertEqual(x[1].value, "@[ cost * 2 ]")
        self.assertEqual(doc.errors, [])

    def test_tagged_color_block(self):
        doc = P.parse_text("color = hsv { 0.1 0.2 0.3 }\nc2 = { 1 2 3 }")
        c = doc.nodes[0]
        self.assertEqual(c.tag, "hsv")
        self.assertEqual([i.key for i in c.value], ["0.1", "0.2", "0.3"])
        self.assertIsNone(doc.nodes[1].tag)

    def test_bom_and_crlf(self):
        doc = P.parse_text("﻿a = 1\r\nb = {\r\n c = 2\r\n}\r\n")
        self.assertEqual(doc.errors, [])
        self.assertEqual(doc.nodes[0].key, "a")
        self.assertEqual(P.first(doc.nodes[1].value, "c").line, 3)

    def test_file_with_bom(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "f.txt")
            with open(p, "wb") as fh:
                fh.write(b"\xef\xbb\xbfa = 1\r\n")
            doc = P.parse_file(p)
            self.assertTrue(doc.bom)
            self.assertEqual(doc.nodes[0].key, "a")

    def test_errors_are_recorded_not_raised(self):
        doc = P.parse_text("a = {\n b = c\n")
        self.assertTrue(any("unclosed" in m for _, m in doc.errors))
        doc = P.parse_text("}\na = 1")
        self.assertTrue(any("unexpected '}'" in m for _, m in doc.errors))
        self.assertEqual(doc.nodes[0].key, "a")
        doc = P.parse_text("a = }")
        self.assertTrue(doc.errors)

    def test_anonymous_block(self):
        doc = P.parse_text("list = { { a = 1 } { a = 2 } }")
        kids = doc.nodes[0].value
        self.assertEqual(len(kids), 2)
        self.assertIsNone(kids[0].key)
        self.assertTrue(kids[0].is_block)

    def test_walk_parents(self):
        doc = P.parse_text("a = { b = { c = 1 } }")
        got = {n.key: [p.key for p in parents] for n, parents in P.walk(doc.nodes)}
        self.assertEqual(got["c"], ["a", "b"])


class TupleCompat(unittest.TestCase):
    """to_tuples must reproduce docs/tools/qa/aug_parse's historical shape."""

    def test_shape(self):
        doc = P.parse_text('a = 1 b = { c d } e = "q" { f = 2 } color = hsv { 1 2 3 }')
        self.assertEqual(P.to_tuples(doc.nodes), [
            ("a", "=", "1"),
            ("b", "=", [("c", None, None), ("d", None, None)]),
            ("e", "=", '"q"'),
            (None, None, [("f", "=", "2")]),
            ("color", "=", "hsv"),
            (None, None, [("1", None, None), ("2", None, None), ("3", None, None)]),
        ])

    def test_aug_parse_delegates(self):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "qa"))
        import aug_parse
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "f.txt")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write("x = { y ?= z }  # c\n")
            self.assertEqual(aug_parse.load(p), [("x", "=", [("y", "?=", "z")])])


class Comments(unittest.TestCase):
    def test_keep_comments_and_dump_roundtrip(self):
        src = ("# header\n"
               "a = {\n"
               "\t# lead\n"
               "\tb = c # trail\n"
               "\tlist = { x y }\n"
               "\t# closing\n"
               "}\n")
        doc = P.parse_text(src, keep_comments=True)
        a = doc.nodes[0]
        self.assertEqual(a.comments, ["# header"])
        b = P.first(a.value, "b")
        self.assertEqual(b.comments, ["# lead"])
        self.assertEqual(b.trailing, "# trail")
        out = P.dump(doc.nodes) + "\n"
        self.assertEqual(out, src)

    def test_comment_on_closing_brace_line_not_moved_to_head(self):
        doc = P.parse_text("a = {\n b = 1\n} # end of a\nc = 2", keep_comments=True)
        self.assertIsNone(doc.nodes[0].trailing)
        self.assertEqual(doc.nodes[1].comments, ["# end of a"])


if __name__ == "__main__":
    unittest.main()
