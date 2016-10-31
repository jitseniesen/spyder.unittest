# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Developers
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Tests for unittestgui.py."""

# Standard library imports
import os

# Third party imports
from pytestqt import qtbot
from qtpy.QtCore import Qt

# Local imports
from spyder_unittest.widgets.unittestgui import UnitTestWidget


def test_run_tests_and_display_results(qtbot, tmpdir):
    os.chdir(tmpdir.strpath)
    testfilename = tmpdir.join('test_foo.py').strpath
    with open(testfilename, 'w') as f:
        f.write("def test_ok(): assert 1+1 == 2\n"
                "def test_fail(): assert 1+1 == 3\n")

    widget = UnitTestWidget(None)
    qtbot.addWidget(widget)
    widget.analyze(tmpdir.strpath)
    qtbot.wait(1000) # wait for tests to run

    datatree = widget.datatree
    itemcount = datatree.topLevelItemCount()
    assert itemcount == 2
    assert datatree.topLevelItem(0).data(0, Qt.DisplayRole) == 'ok'
    assert datatree.topLevelItem(0).data(1, Qt.DisplayRole) == 'test_foo.test_ok'
    assert datatree.topLevelItem(0).data(2, Qt.DisplayRole) is None
    assert datatree.topLevelItem(1).data(0, Qt.DisplayRole) == 'failure'
    assert datatree.topLevelItem(1).data(1, Qt.DisplayRole) == 'test_foo.test_fail'
    assert datatree.topLevelItem(1).data(2, Qt.DisplayRole) == 'assert (1 + 1) == 3'
