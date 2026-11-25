# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native task, parent-frame placement, transient preview and persistence checks."""
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, editing, external, hierarchy, movement, panel
import TestComponentPanel as fixtures
import TestComponentClipboard as clipboard_tests

settle = fixtures.settle

class MovementFixture(unittest.TestCase):
    setUp = fixtures.TestComponentPanel.setUp
    rows = fixtures.TestComponentPanel.rows
    occurrence = fixtures.TestComponentPanel.occurrence
    click = fixtures.TestComponentPanel.click
    menu = clipboard_tests.TestComponentClipboard.menu

    def tearDown(self):
        if movement._active: movement._active.finish()
        fixtures.TestComponentPanel.tearDown(self)

    def row(self, path): return self.occurrence(path).data(0, panel._ROLE)

    def task(self, *paths):
        task = self.widget.move_rows([self.row(p) for p in paths]); settle()
        self.assertFalse(task.closed)
        for i, path in enumerate(paths):
            self.assertEqual(task.components.item(i).text(),self.row(path).label)
        return task


# The full workflow replaces the original two-method regression inventory.
from TestMoveWorkflow import TestMoveWorkflow as TestComponentMove
