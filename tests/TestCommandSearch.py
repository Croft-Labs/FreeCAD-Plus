# SPDX-License-Identifier: LGPL-2.1-or-later
"""Command-palette routing and real native task lifecycle; requires the built GUI."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtGui, QtWidgets
from freecad.gui import CommandSearch as Search


def key_click(widget, key, modifiers=QtCore.Qt.NoModifier):
    for kind in (QtCore.QEvent.KeyPress, QtCore.QEvent.KeyRelease):
        QtWidgets.QApplication.sendEvent(widget, QtGui.QKeyEvent(kind, key, modifiers))


class TestCommandSearch(unittest.TestCase):
    def setUp(self):
        warning = patch.object(QtWidgets.QMessageBox, "warning",
                               side_effect=lambda *args: self.fail(str(args[-1])))
        warning.start()
        self.addCleanup(warning.stop)
        Gui.activateWorkbench("PartDesignWorkbench")
        self.doc = App.newDocument("CommandSearchTest")
        self.doc.UndoMode = 1
        Gui.Selection.clearSelection()

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.activeTaskDialog().reject()
        if Search._dialog:
            Search._dialog.close()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def launch(self, query):
        Gui.runCommand("Std_CommandSearch")
        Gui.updateGui()
        dialog = Search._dialog
        dialog.query.setText(query)
        return dialog

    def fixture(self):
        body = self.doc.addObject("PartDesign::Body", "Body")
        base = body.newObject("PartDesign::AdditiveBox", "Base")
        base.Length = base.Width = base.Height = 10
        sketch = body.newObject("Sketcher::SketchObject", "Profile")
        points = [(2, 2), (6, 2), (6, 6), (2, 6)]
        for start, end in zip(points, points[1:] + points[:1]):
            sketch.addGeometry(Part.LineSegment(App.Vector(*start, 0), App.Vector(*end, 0)))
        sketch.Placement.Base.z = 5
        self.doc.recompute()
        Gui.activeDocument().activeView().setActiveObject("pdbody", body)
        Gui.Selection.addSelection(sketch)
        return body, base, sketch

    def testStandardMenuAndShortcut(self):
        command = Gui.Command.get("Std_CommandSearch")
        self.assertIsNotNone(command)
        self.assertEqual(command.getShortcut(), "Ctrl+K")
        self.assertEqual(Gui.Command.listByShortcut("Ctrl+K"), ["Std_CommandSearch"])
        actions = [action for menu in Gui.getMainWindow().menuBar().findChildren(QtWidgets.QMenu)
                   for action in menu.actions()]
        self.assertTrue(any("Command search" in action.text() for action in actions))
        dialog = self.launch("pocket")
        self.assertTrue(dialog.isVisible())
        self.assertIs(self.launch("revolved cut"), dialog)

    def testAliasesAndLiveShortcut(self):
        rows = Search.catalog()
        self.assertEqual(len(rows), len({row[0] for row in rows}))
        for query, name in (("pocket", "PartDesign_Pocket"),
                            ("CUT-EXTRUDE", "PartDesign_Pocket"),
                            ("boss-extrude", "PartDesign_Pad"),
                            ("revolved cut", "PartDesign_Groove"),
                            ("PartDesign_Revolution", "PartDesign_Revolution"),
                            ("linear pattern", "PartDesign_Pattern")):
            with self.subTest(query=query):
                self.assertEqual(Search.matching_rows(rows, query)[0][0], name)
        command = Gui.Command.get("PartDesign_Extrude")
        original = command.getShortcut()
        try:
            command.setShortcut("Ctrl+Alt+9")
            dialog = self.launch("Ctrl+Alt+9")
            self.assertEqual(dialog.selected()[0], "PartDesign_Extrude")
            self.assertEqual(dialog.selected()[5], "Ctrl+Alt+9")
        finally:
            command.setShortcut(original)

    def testKeyboardNavigationEmptyAndEscape(self):
        dialog = self.launch("revolve")
        self.assertGreater(dialog.results.topLevelItemCount(), 1)
        key_click(dialog.query, QtCore.Qt.Key_Down)
        self.assertEqual(dialog.results.indexOfTopLevelItem(dialog.results.currentItem()), 1)
        key_click(dialog.query, QtCore.Qt.Key_Up)
        self.assertEqual(dialog.results.indexOfTopLevelItem(dialog.results.currentItem()), 0)
        dialog.query.setText("no_such_operation_98765")
        self.assertEqual(dialog.results.topLevelItemCount(), 0)
        self.assertFalse(dialog.runButton.isEnabled())
        self.assertIn("No matching", dialog.detail.toPlainText())
        key_click(dialog.query, QtCore.Qt.Key_Return)
        self.assertTrue(dialog.isVisible())
        key_click(dialog.query, QtCore.Qt.Key_Escape)
        self.assertFalse(dialog.isVisible())

    def testExplicitWorkbenchSwitch(self):
        Gui.activateWorkbench("PartWorkbench")
        before = list(self.doc.Objects)
        dialog = self.launch("pocket")
        self.assertFalse(dialog.runButton.isEnabled())
        self.assertTrue(dialog.switchButton.isEnabled())
        dialog.switchButton.click()
        self.assertEqual(Gui.activeWorkbench().name(), "PartDesignWorkbench")
        self.assertEqual(dialog.selected()[0], "PartDesign_Pocket")
        self.assertTrue(dialog.runButton.isEnabled())
        self.assertEqual(list(self.doc.Objects), before)

    def testStaleAvailabilityAndMissingDocument(self):
        dialog = self.launch("pocket")
        self.assertTrue(dialog.runButton.isEnabled())
        App.closeDocument(self.doc.Name)
        with patch.object(Gui, "runCommand") as run:
            dialog.runSelected()
            run.assert_not_called()
        self.assertFalse(dialog.runButton.isEnabled())
        self.assertIn("Open a document", dialog.detail.toPlainText())
        self.assertTrue(dialog.isVisible())

    def testAssemblyContext(self):
        dialog = self.launch("Assembly_Insert")
        if "AssemblyWorkbench" in Gui.listWorkbenches():
            self.assertTrue(dialog.switchButton.isEnabled())
            dialog.switchButton.click()
            self.assertEqual(Gui.activeWorkbench().name(), "AssemblyWorkbench")
        else:
            self.assertFalse(dialog.switchButton.isEnabled())
            self.assertIn("workbench is not installed", dialog.detail.toPlainText())
        self.assertFalse(dialog.runButton.isEnabled())
        self.assertIn("Create or activate an Assembly", dialog.detail.toPlainText())
        self.assertEqual(self.doc.Objects, [])

    def testPocketKeyboardGeometryUndoAndReopen(self):
        body, base, sketch = self.fixture()
        dialog = self.launch("Pocket")
        key_click(dialog.query, QtCore.Qt.Key_Return)
        Gui.updateGui()
        self.assertFalse(dialog.isVisible())
        self.assertTrue(Gui.Control.activeDialog())
        pocket = self.doc.getObject("Pocket")
        self.assertIsNotNone(pocket)
        self.assertEqual(pocket.Operation, "Subtraction")
        self.assertEqual(pocket.Profile[0], sketch)
        active = Gui.Control.activeTaskDialog()
        combos = [panel.findChild(QtWidgets.QComboBox, "comboOperation")
                  for panel in active.getDialogContent()]
        combo = next(widget for widget in combos if widget is not None)
        self.assertEqual(combo.currentData(), "Subtraction")
        blocked = self.launch("pad")
        self.assertFalse(blocked.runButton.isEnabled())
        self.assertIn("Finish or cancel", blocked.detail.toPlainText())
        blocked.close()
        active.accept()
        self.doc.recompute()
        self.assertAlmostEqual(pocket.Shape.Volume, 920)
        self.assertEqual(body.Tip, pocket)
        self.doc.undo()
        self.doc.recompute()
        self.assertIsNone(self.doc.getObject("Pocket"))
        self.assertAlmostEqual(body.Tip.Shape.Volume, 1000)
        self.doc.redo()
        self.doc.recompute()
        with tempfile.TemporaryDirectory() as folder:
            filename = str(Path(folder) / "SearchPocket.FCStd")
            self.doc.saveAs(filename)
            App.closeDocument(self.doc.Name)
            reopened = App.openDocument(filename)
            reopened.recompute()
            self.assertAlmostEqual(reopened.Pocket.Shape.Volume, 920)
            self.assertEqual(reopened.Pocket.Operation, "Subtraction")
            self.assertEqual(reopened.Body.Tip, reopened.Pocket)

    def testOfflineHelpAndUncuratedFallbackLeaveDocumentAlone(self):
        box = self.doc.addObject("Part::Box", "Box")
        self.doc.recompute()
        Gui.Selection.addSelection(box)
        before = (box.Shape.Volume, tuple(box.Placement.toMatrix().A),
                  self.doc.UndoCount, list(self.doc.Objects))
        dialog = self.launch("pocket")
        with patch.object(Gui, "activateWorkbench") as switch, patch.object(Gui, "runCommand") as run:
            dialog.helpButton.setChecked(True)
            for name in Search.HELP:
                dialog.query.setText(name)
                self.assertEqual(dialog.selected()[0], name)
                self.assertIn(Search.help_text(dialog.selected()), dialog.detail.toPlainText())
            dialog.query.setText("Std_New")
            self.assertIn("No extended local guide", dialog.detail.toPlainText())
            self.assertNotIn("Partial copying", dialog.detail.toPlainText())
            switch.assert_not_called()
            run.assert_not_called()
        self.assertEqual(Gui.Selection.getSelection(), [box])
        self.assertEqual(before, (box.Shape.Volume, tuple(box.Placement.toMatrix().A),
                                 self.doc.UndoCount, list(self.doc.Objects)))
        self.assertFalse(self.doc.HasPendingTransaction)

    def testHelpKeyboardReadingAndReturnToSearch(self):
        dialog = self.launch("Sketcher_CopyReusable")
        dialog.helpButton.setChecked(False)
        dialog.query.setFocus()
        key_click(dialog.query, QtCore.Qt.Key_F1)
        Gui.updateGui()
        self.assertTrue(dialog.helpButton.isChecked())
        self.assertTrue(dialog.detail.hasFocus())
        with patch.object(Gui, "runCommand") as run:
            key_click(dialog.detail, QtCore.Qt.Key_Return)
            key_click(dialog.detail, QtCore.Qt.Key_PageDown)
            run.assert_not_called()
        key_click(dialog.detail, QtCore.Qt.Key_L, QtCore.Qt.ControlModifier)
        Gui.updateGui()
        self.assertTrue(dialog.query.hasFocus())
        self.assertEqual(dialog.query.selectedText(), "Sketcher_CopyReusable")
        key_click(dialog.query, QtCore.Qt.Key_F1)
        self.assertFalse(dialog.helpButton.isChecked())
        key_click(dialog.query, QtCore.Qt.Key_Tab)
        self.assertTrue(dialog.results.hasFocus())
        key_click(dialog.results, QtCore.Qt.Key_Tab)
        self.assertTrue(dialog.detail.hasFocus())
        key_click(dialog.detail, QtCore.Qt.Key_Escape)
        self.assertFalse(dialog.isVisible())
        self.assertFalse(dialog.contextTimer.isActive())

    def testLiveContextAndHelpAreSeparateFromEligibility(self):
        dialog = self.launch("Pocket")
        dialog.helpButton.setChecked(True)
        guide = Search.help_text(dialog.selected())
        self.assertTrue(dialog.contextTimer.isActive())
        other = App.newDocument("OtherSearchDocument")
        dialog.contextTimer.timeout.emit()
        self.assertIn(other.Label, dialog.detail.toPlainText())
        App.closeDocument(other.Name)
        App.closeDocument(self.doc.Name)
        dialog.contextTimer.timeout.emit()
        self.assertFalse(dialog.runButton.isEnabled())
        self.assertIn("Open a document", dialog.detail.toPlainText())
        self.assertIn(guide, dialog.detail.toPlainText())
        self.assertIn("Active document: None", dialog.detail.toPlainText())

    def testEnlargedTextScrollAndLayoutRecovery(self):
        dialog = self.launch("CAM_MeshPreparation")
        original = QtGui.QFont(dialog.font())
        original_style = dialog.styleSheet()
        font = QtGui.QFont(original)
        font.setPointSize(20)
        try:
            dialog.setFont(font)
            # FreeCAD's application stylesheet can override inherited widget fonts.
            # Exercise actual rendered enlargement, not just QDialog.font().
            dialog.setStyleSheet("QWidget { font-size: 20pt; }")
            dialog.resize(740, 640)
            dialog.helpButton.setChecked(True)
            dialog.splitter.setSizes([300, 80])
            Gui.updateGui()
            self.assertEqual(dialog.detail.font().pointSize(), 20)
            self.assertEqual(dialog.runButton.font().pointSize(), 20)
            bar = dialog.detail.verticalScrollBar()
            self.assertGreater(bar.maximum(), 0)
            bar.setValue(bar.maximum())
            dialog.describe()
            self.assertEqual(bar.value(), bar.maximum())
            for control in (dialog.query, dialog.results, dialog.detail, dialog.runButton,
                            dialog.switchButton, dialog.refreshButton, dialog.helpButton,
                            dialog.resetButton, dialog.closeButton):
                rect = QtCore.QRect(control.mapTo(dialog, QtCore.QPoint()), control.size())
                self.assertTrue(dialog.rect().contains(rect), control.objectName() or control.__class__.__name__)
            before = (App.ActiveDocument, list(self.doc.Objects), dialog.query.text(),
                      Gui.Command.get("Std_CommandSearch").getShortcut())
            dialog.resetButton.click()
            Gui.updateGui()
            self.assertFalse(dialog.helpButton.isChecked())
            self.assertEqual(dialog.font().pointSize(), 20)
            self.assertEqual(dialog.detail.font().pointSize(), 20)
            self.assertTrue(all(size > 0 for size in dialog.splitter.sizes()))
            self.assertEqual(before, (App.ActiveDocument, list(self.doc.Objects), dialog.query.text(),
                                     Gui.Command.get("Std_CommandSearch").getShortcut()))
        finally:
            dialog.setStyleSheet(original_style)
            dialog.setFont(original)
            dialog.resetLayout()
