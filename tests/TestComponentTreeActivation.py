# SPDX-License-Identifier: LGPL-2.1-or-later
"""Part Tree native double clicks survive row replacement and keep occurrence identity."""
import unittest
from unittest.mock import patch
import FreeCADGui as Gui
import ComponentModel as Model
from PySide import QtCore, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest
from freecad.gui import ComponentNavigator as Navigator
from TestComponentActiveEditing import TestComponentActiveEditing as Fixture


class TestComponentTreeActivation(unittest.TestCase):
    setUp = Fixture.setUp
    tearDown = Fixture.tearDown

    def show_tree(self):
        self.panel.tabs.setCurrentWidget(self.panel.structure)
        self.panel.structure.expandAll()
        Gui.updateGui()

    def find(self, ids):
        iterator = QtWidgets.QTreeWidgetItemIterator(self.panel.structure)
        while iterator.value():
            item = iterator.value()
            value = item.data(0, QtCore.Qt.UserRole)
            if value and list(value[1]) == ids:
                return item
            iterator += 1
        self.fail("Occurrence missing from Part Tree")

    def click(self, ids, double=True, refresh_between=True):
        self.show_tree()
        tree = self.panel.structure
        row = self.find(ids)
        tree.scrollToItem(row)
        rect = tree.visualItemRect(row)
        self.assertFalse(rect.isEmpty())
        point = QtCore.QPoint(min(rect.left() + 55, tree.columnWidth(0) - 8),
                              rect.center().y())
        QtTest.QTest.mouseClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
        if refresh_between:
            self.panel.refresh()
        if double:
            QtTest.QTest.mouseDClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
            # Also replace rows before the queued activation runs.
            self.panel.refresh()
        Gui.updateGui()
        QtTest.QTest.qWait(80)

    def testDoubleClickAfterRefreshActivatesOnceInCurrentTab(self):
        with patch.object(self.panel, "activate_item", wraps=self.panel.activate_item) as activate:
            self.click([self.first.ObjectId])
            self.assertEqual(activate.call_count, 1)
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.part))
        self.assertEqual(self.panel.active_path, [self.first.ObjectId])
        self.assertEqual(self.panel.mdi.activeSubWindow(), self.window)
        self.assertEqual(len(self.panel.mdi.subWindowList()), self.windows)
        self.assertEqual(self.panel.tabs.currentWidget(), self.panel.history)

    def testSingleClickDoesNotActivate(self):
        self.click([self.first.ObjectId], double=False)
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))
        self.assertEqual(self.panel.active_path, [])

    def testRepeatedInstanceKeepsItsOwnPath(self):
        self.panel.toggle_instances(self.panel.structure.topLevelItem(0).child(0))
        self.panel.refresh()
        self.click([self.second.ObjectId])
        self.assertEqual(self.panel.active_path, [self.second.ObjectId])
        remembered = self.window.property("ComponentEditPaths")
        self.assertEqual(remembered[self.part.ObjectId], [self.second.ObjectId])

    def testNestedInstanceActivates(self):
        child = Model.add_component(self.part, label="Nested")
        self.panel.refresh()
        self.panel.toggle_instances(self.panel.structure.topLevelItem(0).child(0))
        self.panel.refresh()
        ids = [self.second.ObjectId, child.ObjectId]
        self.click(ids)
        self.assertEqual(self.panel.active_key, Navigator.object_key(child.LinkedObject))
        self.assertEqual(self.panel.active_path, ids)

    def testActiveTaskStillBlocksDoubleClick(self):
        class Task:
            form = QtWidgets.QWidget()
        Gui.Control.showDialog(Task())
        try:
            with patch.object(QtWidgets.QMessageBox, "warning") as warning:
                self.click([self.first.ObjectId])
                self.assertEqual(warning.call_count, 1)
            self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))
        finally:
            Gui.Control.closeDialog()

    def testDeferredClickCannotActivateDeletedRowOrChangedContext(self):
        item = self.find([self.first.ObjectId])
        key = self.panel.row_key(item)
        context = (self.panel.root_key, self.panel.active_key, tuple(self.panel.active_path))
        Model.remove_instances([self.first])
        self.panel.refresh()
        self.panel.activate_tree_row(key, context, self.window)
        self.assertEqual(self.panel.active_path, [])
        item = self.find([self.second.ObjectId])
        key = self.panel.row_key(item)
        self.panel.activate_item(item)
        self.panel.activate_tree_row(key, context, self.window)
        self.assertEqual(self.panel.active_path, [self.second.ObjectId])