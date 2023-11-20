# -*- coding: utf-8 -*-

# 3rd party imports
import pytest


def test_import_version():
    try:
        from phabfive import __version__  # noqa
    except ImportError:
        pytest.fail("Unexpected ImportError")


def test_import_phabfive():
    try:
        from phabfive.core import Phabfive  # noqa
    except ImportError:
        pytest.fail("Unexpected ImportError")
