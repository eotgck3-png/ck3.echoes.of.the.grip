"""Tests for the shared test helper: temp-dir cleanup survives transient Windows locks.

Run: python -m unittest discover docs/tools/tests
"""
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _testutil as T  # noqa: E402


class Cleanup(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="eotg_tu_")
        with open(os.path.join(self.d, "f.txt"), "w") as fh:
            fh.write("x")

    def tearDown(self):
        shutil.rmtree(self.d, ignore_errors=True)

    def test_retries_a_transient_lock(self):
        real, calls = shutil.rmtree, []

        def flaky(path, **kw):
            calls.append(path)
            if len(calls) < 3:
                raise PermissionError(32, "being used by another process", path)
            return real(path, **kw)

        with mock.patch.object(T.shutil, "rmtree", flaky), mock.patch.object(T.time, "sleep"):
            T.rmtree(self.d)
        self.assertEqual(len(calls), 3)
        self.assertFalse(os.path.exists(self.d))

    def test_a_lasting_lock_leaks_instead_of_failing(self):
        def locked(path, **kw):
            raise PermissionError(32, "being used by another process", path)

        with mock.patch.object(T.shutil, "rmtree", locked), mock.patch.object(T.time, "sleep"):
            T.rmtree(self.d)   # no exception
        self.assertTrue(os.path.exists(self.d))

    def test_tempdir_removes_its_tree(self):
        with T.tempdir() as d:
            open(os.path.join(d, "a"), "w").close()
        self.assertFalse(os.path.exists(d))


if __name__ == "__main__":
    unittest.main()
