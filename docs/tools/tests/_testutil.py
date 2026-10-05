"""Shared test helpers.

Temp-dir cleanup on Windows: antivirus (Defender) and the search indexer open a
file the moment it is written, and while they hold it, deleting it raises
PermissionError [WinError 5/32]. shutil.rmtree and TemporaryDirectory then fail
the test that just passed, at random, on Windows only. rmtree() retries with a
short backoff and never fails a test over a leftover temp dir.
"""
import contextlib
import os
import shutil
import stat
import sys
import tempfile
import time

_DELAYS = (0.05, 0.1, 0.25, 0.5, 1.0)
# onerror is deprecated from 3.12 in favour of onexc (same call shape here)
_HANDLER = "onexc" if sys.version_info >= (3, 12) else "onerror"


def _writable(func, path, *_):
    # read-only files (git objects, copied fixtures) block deletion on Windows
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except OSError:
        pass


def rmtree(path, *_ignored):
    """Remove a temp tree; retry transient Windows locks; leak rather than fail."""
    for delay in (0,) + _DELAYS:
        if not os.path.exists(path):
            return
        time.sleep(delay)
        try:
            shutil.rmtree(path, **{_HANDLER: _writable})
        except OSError:
            pass


@contextlib.contextmanager
def tempdir(prefix="eotg_test_"):
    """tempfile.TemporaryDirectory with rmtree()'s cleanup."""
    d = tempfile.mkdtemp(prefix=prefix)
    try:
        yield d
    finally:
        rmtree(d)
