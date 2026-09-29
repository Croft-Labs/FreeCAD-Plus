# SPDX-License-Identifier: LGPL-2.1-or-later
"""#28412: expanding/collapsing a container must not drag-select model objects."""
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets


class TestIssueTreeSelection(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("IssueTreeSelection")
        self.group = self.doc.addObject("App::Part", "IssueExpandContainer")
        self.child = self.doc.addObject("Part::Box", "IssueTreeChild")
        self.group.addObject(self.child)
        self.other = self.doc.addObject("Part::Box", "IssueTreeOther")
        self.doc.recompute()
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(300, loop.quit)
        loop.exec()
        Gui.updateGui()
        matches = []
        for tree in Gui.getMainWindow().findChildren(QtWidgets.QTreeWidget):
            items = tree.findItems(self.group.Label, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
            if items:
                matches.append((tree, items[0]))
        self.assertTrue(matches, "Model tree/container not found")
        self.tree = matches[0][0]
        self.tree.expandAll()
        Gui.updateGui()
        self.tree.scrollToItem(self.item())

    def item(self):
        # Tree expansion/selection can rebuild native items; reacquire after events.
        items = self.tree.findItems(
            self.group.Label, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
        self.assertTrue(items)
        return items[0]

    def tearDown(self):
        Gui.Selection.clearSelection()
        App.closeDocument(self.doc.Name)

    def mouse(self, kind, point, button, buttons):
        viewport = self.tree.viewport()
        QtWidgets.QApplication.sendEvent(viewport, QtGui.QMouseEvent(
            kind, QtCore.QPointF(point), QtCore.QPointF(viewport.mapToGlobal(point)),
            button, buttons, QtCore.Qt.NoModifier))
        Gui.updateGui()

    def selected(self):
        return {(obj.Document.Name, obj.Name) for obj in Gui.Selection.getSelection()}

    def testExpandCollapseDragPreservesSelection(self):
        for expanded in (False, True):
            with self.subTest(expanded=expanded):
                self.item().setExpanded(expanded)
                Gui.Selection.clearSelection()
                Gui.Selection.addSelection(self.other)
                Gui.updateGui()
                original = self.selected()
                self.assertEqual(original, {(self.doc.Name, self.other.Name)})
                rect = self.tree.visualItemRect(self.item())
                arrow = QtCore.QPoint(rect.left() - self.tree.indentation() // 2, rect.center().y())
                self.mouse(QtCore.QEvent.MouseButtonPress, arrow, QtCore.Qt.LeftButton, QtCore.Qt.LeftButton)
                self.assertEqual(self.item().isExpanded(), not expanded, "Arrow click did not toggle")
                destination = QtCore.QPoint(rect.left() + 40, rect.bottom() + 8)
                self.mouse(QtCore.QEvent.MouseMove, destination, QtCore.Qt.NoButton, QtCore.Qt.LeftButton)
                self.mouse(QtCore.QEvent.MouseButtonRelease, destination, QtCore.Qt.LeftButton, QtCore.Qt.NoButton)
                self.assertEqual(self.selected(), original)
