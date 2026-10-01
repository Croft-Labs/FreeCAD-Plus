# SPDX-License-Identifier: LGPL-2.1-or-later
"""Whole-link appearance editing through the installed standard View command."""
from pathlib import Path
import tempfile
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtGui, QtWidgets
from freecad.gui import OccurrenceAppearance as Editor


def make_fixture():
    doc = App.newDocument("OccurrenceAppearanceWorkflow")
    doc.UndoMode = 1
    source = doc.addObject("Part::Box", "SharedBracket")
    source.Length, source.Width, source.Height = 10, 7, 5
    source.ViewObject.ShapeAppearance = [App.Material(DiffuseColor=(0.2, 0.4, 0.9))]
    assembly = doc.addObject("App::Part", "Assembly")
    assembly.Placement = App.Placement(App.Vector(0, 5, 0), App.Rotation(App.Vector(0, 0, 1), 15))
    for name, x in (("OccurrenceA", 0), ("OccurrenceB", 16), ("OccurrenceC", 32)):
        link = doc.addObject("App::Link", name)
        link.setLink(source)
        assembly.addObject(link)
        link.LinkPlacement.Base.x = x
    doc.recompute()
    source.Visibility = False
    return doc


class TestOccurrenceAppearance(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = make_fixture()
        Gui.Selection.clearSelection()

    def tearDown(self):
        for dialog in list(Editor._dialogs):
            dialog.close()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def launch(self, link=None):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(link or self.doc.OccurrenceA)
        Gui.runCommand("Std_OccurrenceAppearance")
        Gui.updateGui()
        return Editor._dialogs[-1]

    def edit(self, dialog, visible=True, override=True):
        dialog.visible.setChecked(visible)
        dialog.override.setChecked(override)
        dialog.setColor(QtGui.QColor("#E64020"))
        dialog.transparency.setValue(25)

    def testCommandStagingAndCloseLeaveSourceAndLinksUntouched(self):
        before = [Editor.state(self.doc.getObject(name)) for name in ("OccurrenceA", "OccurrenceB")]
        dialog = self.launch()
        menus = [m for m in Gui.getMainWindow().menuBar().findChildren(QtWidgets.QMenu)
                 if m.title().replace("&", "") == "View"]
        self.assertIn("Occurrence appearance...",
                      [a.text().replace("&", "") for menu in menus for a in menu.actions()])
        self.assertIn("SharedBracket", dialog.identity.text())
        self.edit(dialog, visible=False)
        self.assertEqual(Editor.state(self.doc.OccurrenceA), before[0])
        dialog.close()
        self.assertEqual([Editor.state(self.doc.getObject(name)) for name in ("OccurrenceA", "OccurrenceB")], before)
        self.assertFalse(self.doc.HasPendingTransaction)

    def testApplyUndoRedoAndPersistenceKeepSharingAndPlacement(self):
        link = self.doc.OccurrenceA
        before = Editor.state(link)
        other = Editor.state(self.doc.OccurrenceB)
        world = tuple(self.doc.Assembly.Placement.multiply(link.LinkPlacement).toMatrix().A)
        shape = self.doc.SharedBracket.Shape.exportBrepToString()
        dialog = self.launch()
        self.edit(dialog, visible=False)
        dialog.applyButton.click()
        self.assertIn("applied", dialog.message.text())
        self.assertFalse(link.Visibility)
        self.assertTrue(link.ViewObject.OverrideMaterial)
        self.assertAlmostEqual(link.ViewObject.ShapeAppearance[0].Transparency, 0.25)
        self.assertAlmostEqual(link.ViewObject.ShapeAppearance[0].DiffuseColor[0], 230 / 255, places=5)
        self.assertEqual(Editor.state(self.doc.OccurrenceB), other)
        self.assertEqual(tuple(self.doc.Assembly.Placement.multiply(link.LinkPlacement).toMatrix().A), world)
        self.assertEqual(self.doc.SharedBracket.Shape.exportBrepToString(), shape)
        self.assertEqual(link.LinkedObject, self.doc.OccurrenceB.LinkedObject)
        self.doc.undo()
        self.assertEqual(Editor.state(link), before)
        self.doc.redo()
        self.assertTrue(link.ViewObject.OverrideMaterial)
        self.assertFalse(link.Visibility)
        dialog.close()
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "Appearance.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            link = self.doc.OccurrenceA
            self.assertTrue(link.ViewObject.OverrideMaterial)
            self.assertFalse(link.Visibility)
            self.assertAlmostEqual(link.ViewObject.ShapeAppearance[0].Transparency, 0.25)
            self.assertEqual(link.LinkedObject, self.doc.OccurrenceB.LinkedObject)
            self.assertFalse(self.doc.OccurrenceB.ViewObject.OverrideMaterial)
            self.assertEqual(tuple(self.doc.Assembly.Placement.multiply(link.LinkPlacement).toMatrix().A), world)

    def testResetUsesNativeInheritanceAndKeepsVisibilityIndependent(self):
        dialog = self.launch()
        self.edit(dialog, visible=False)
        dialog.applyButton.click()
        dialog.inherit.click()
        self.assertTrue(self.doc.OccurrenceA.ViewObject.OverrideMaterial)
        dialog.applyButton.click()
        self.assertFalse(self.doc.OccurrenceA.ViewObject.OverrideMaterial)
        self.assertFalse(self.doc.OccurrenceA.Visibility)
        self.doc.SharedBracket.ViewObject.ShapeAppearance = [App.Material(DiffuseColor=(0.0, 1.0, 0.0))]
        dialog.reloadButton.click()
        self.assertEqual(dialog.color.name(), "#00ff00")
        self.assertFalse(dialog.colorButton.isEnabled())
        self.assertFalse(self.doc.OccurrenceB.ViewObject.OverrideMaterial)

    def testStaleAppearanceAndRelinkRequireReload(self):
        dialog = self.launch()
        self.edit(dialog)
        self.doc.OccurrenceA.Visibility = False
        dialog.applyButton.click()
        self.assertIn("Reload", dialog.message.text())
        self.assertFalse(self.doc.OccurrenceA.ViewObject.OverrideMaterial)
        dialog.reloadButton.click()
        self.edit(dialog)
        replacement = self.doc.addObject("Part::Box", "Replacement")
        self.doc.recompute()
        self.doc.OccurrenceA.setLink(replacement)
        dialog.applyButton.click()
        self.assertIn("Reload", dialog.message.text())
        self.assertFalse(self.doc.OccurrenceA.ViewObject.OverrideMaterial)
        dialog.reloadButton.click()
        self.assertIn("Replacement", dialog.identity.text())
        self.edit(dialog)
        dialog.applyButton.click()
        self.assertTrue(self.doc.OccurrenceA.ViewObject.OverrideMaterial)

    def testScopeAndPendingTransactionRejectWithoutMutation(self):
        with self.assertRaises(ValueError):
            Editor.validate(self.doc.SharedBracket)
        link = self.doc.OccurrenceA
        before = Editor.state(link)
        self.doc.openTransaction("Other edit")
        self.doc.SharedBracket.Label = "Pending source edit"
        self.assertTrue(self.doc.HasPendingTransaction)
        with self.assertRaises(ValueError):
            Editor.apply(link, before, False, True, (1.0, 0.0, 0.0), 25)
        self.doc.abortTransaction()
        self.assertEqual(Editor.state(link), before)
        link.ElementCount = 2
        with self.assertRaises(ValueError):
            Editor.validate(link)
        link.ElementCount = 0
        Gui.Selection.addSelection(self.doc.OccurrenceB, "Face1")
        with self.assertRaises(ValueError):
            Editor.selected_link()
        Gui.Selection.clearSelection()
        container_link = self.doc.addObject("App::Link", "AssemblyOccurrence")
        container_link.setLink(self.doc.Assembly)
        self.doc.recompute()
        Gui.Selection.addSelection(container_link, "OccurrenceB.")
        with self.assertRaises(ValueError):
            Editor.selected_link()

    def testBodyOccurrencePreservesTipAndGeometry(self):
        body = self.doc.addObject("PartDesign::Body", "Body")
        base = body.newObject("PartDesign::AdditiveBox", "Base")
        self.doc.recompute()
        link = self.doc.addObject("App::Link", "BodyOccurrence")
        link.setLink(body)
        self.doc.recompute()
        volume = body.Shape.Volume
        dialog = self.launch(link)
        self.edit(dialog)
        dialog.applyButton.click()
        self.assertIn("applied", dialog.message.text())
        self.assertEqual(body.Tip, base)
        self.assertEqual(body.Shape.Volume, volume)
        self.assertEqual(link.LinkedObject, body)

    def testDeletionAndDocumentCloseDetachEditor(self):
        dialog = self.launch()
        self.doc.removeObject("SharedBracket")
        self.assertFalse(dialog.applyButton.isEnabled())
        self.assertIn("deleted", dialog.message.text())
        self.doc.removeObject("OccurrenceA")
        self.assertTrue(dialog._closed)
        self.assertNotIn(dialog, Editor._dialogs)
        source = self.doc.addObject("Part::Box", "NewSource")
        self.doc.OccurrenceB.setLink(source)
        self.doc.recompute()
        dialog = self.launch(self.doc.OccurrenceB)
        App.closeDocument(self.doc.Name)
        self.assertTrue(dialog._closed)
        self.assertNotIn(dialog, Editor._dialogs)
