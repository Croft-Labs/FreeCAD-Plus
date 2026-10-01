# SPDX-License-Identifier: LGPL-2.1-or-later
"""Part Mirror's explicit associative versus independent result workflow."""
from pathlib import Path
import tempfile
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets


def make_fixture():
    doc = App.newDocument("MirrorResultWorkflow")
    doc.UndoMode = 1
    body = doc.addObject("PartDesign::Body", "Bracket")
    box = body.newObject("PartDesign::AdditiveBox", "Base")
    box.Length, box.Width, box.Height = 10, 6, 4
    notch = body.newObject("PartDesign::SubtractiveBox", "Notch")
    notch.Length, notch.Width, notch.Height = 3, 2, 2
    notch.Placement.Base = App.Vector(1, 1, 2)
    doc.recompute()
    body.Placement = App.Placement(App.Vector(20, 3, 2), App.Rotation(App.Vector(0, 0, 1), 20))
    doc.recompute()
    body.ViewObject.ShapeAppearance = [App.Material(DiffuseColor=(0.2, 0.6, 0.9))]
    return doc


class TestMirrorResultMode(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = make_fixture()
        self.body = self.doc.Bracket
        Gui.Selection.clearSelection()

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def widget(self, kind, name):
        for panel in Gui.Control.activeTaskDialog().getDialogContent():
            found = panel.findChild(kind, name)
            if found is not None:
                return found
        self.fail("Missing Mirror widget " + name)

    def launch(self, independent=False, sources=None):
        sources = sources or [self.body]
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(sources[0])
        Gui.runCommand("Part_Mirror")
        Gui.updateGui()
        tree = self.widget(QtWidgets.QTreeWidget, "shapes")
        tree.clearSelection()
        for i in range(tree.topLevelItemCount()):
            item = tree.topLevelItem(i)
            if item.data(0, QtCore.Qt.UserRole) in [obj.Name for obj in sources]:
                item.setSelected(True)
        self.widget(QtWidgets.QComboBox, "comboBox").setCurrentIndex(2)
        self.widget(QtWidgets.QComboBox, "resultMode").setCurrentIndex(int(independent))

    def accept(self):
        Gui.Control.activeTaskDialog().accept()
        Gui.updateGui()

    def result(self, independent=False):
        if independent:
            return next(o for o in self.doc.Objects if o.Name.startswith("MirrorSnapshot"))
        return next(o for o in self.doc.Objects if o.TypeId == "Part::Mirroring")

    def assertSameShape(self, first, second):
        self.assertTrue(first.isValid())
        self.assertAlmostEqual(first.Volume, second.Volume, places=6)
        self.assertAlmostEqual(first.common(second).Volume, second.Volume, places=6)

    def testBothModesReflectAsymmetricBodyAndPreserveSource(self):
        original = self.body.Shape.copy()
        tip = self.body.Tip
        self.assertAlmostEqual(original.Volume, 228)
        expected = original.mirror(App.Vector(), App.Vector(1, 0, 0))
        self.launch()
        self.accept()
        self.assertFalse(Gui.Control.activeDialog())
        associative = self.result()
        self.assertEqual(associative.Source, self.body)
        self.assertSameShape(associative.Shape, expected)
        self.launch(True)
        self.accept()
        self.assertFalse(Gui.Control.activeDialog())
        snapshot = self.result(True)
        self.assertEqual(snapshot.TypeId, "Part::Feature")
        self.assertNotIn("Source", snapshot.PropertiesList)
        self.assertEqual(snapshot.OutList, [])
        self.assertIn("independent snapshot", snapshot.Label)
        self.assertSameShape(snapshot.Shape, expected)
        self.assertEqual(self.body.Tip, tip)
        self.assertTrue(self.body.Visibility)
        self.assertSameShape(self.body.Shape, original)
        self.assertEqual(len([o for o in self.doc.Objects if o.TypeId == "Part::Mirroring"]), 1)

    def testSourceEditUndoRedoAndPersistenceKeepChosenRelationship(self):
        self.launch()
        self.accept()
        self.launch(True)
        self.accept()
        snapshot = self.result(True)
        snapshot_name = snapshot.Name
        frozen = snapshot.Shape.copy()
        self.doc.undo()
        self.assertIsNone(self.doc.getObject(snapshot_name))
        self.assertEqual(len([o for o in self.doc.Objects if o.TypeId == "Part::Mirroring"]), 1)
        self.doc.redo()
        self.doc.recompute()
        snapshot = self.result(True)
        self.assertEqual(snapshot.OutList, [])
        self.doc.Base.Length = 12
        self.doc.recompute()
        self.assertAlmostEqual(self.result().Shape.Volume, 276)
        self.assertSameShape(snapshot.Shape, frozen)
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "MirrorModes.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.body = self.doc.Bracket
            self.assertEqual(self.result().Source, self.body)
            self.assertSameShape(self.result(True).Shape, frozen)
            self.assertEqual(self.result(True).OutList, [])
            self.doc.Base.Length = 14
            self.doc.recompute()
            self.assertAlmostEqual(self.result().Shape.Volume, 324)
            self.assertSameShape(self.result(True).Shape, frozen)

    def testReferencePlaneUpdatesOnlyAssociativeResult(self):
        plane = self.doc.addObject("Part::Plane", "MirrorPlane")
        plane.Placement.Rotation = App.Rotation(App.Vector(0, 1, 0), 90)
        self.doc.recompute()
        for independent in (False, True):
            self.launch(independent)
            self.widget(QtWidgets.QComboBox, "comboBox").setCurrentIndex(3)
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(plane)
            self.accept()
            self.assertFalse(Gui.Control.activeDialog())
        self.assertEqual(self.result().MirrorPlane[0], plane)
        frozen = self.result(True).Shape.copy()
        before = self.result().Shape.Solids[0].CenterOfMass
        plane.Placement.Base.x = 5
        self.doc.recompute()
        self.assertAlmostEqual(self.result().Shape.Solids[0].CenterOfMass.x, before.x + 10)
        self.assertSameShape(self.result(True).Shape, frozen)

    def testCancelAndUnsupportedSnapshotScopeLeaveModelUntouched(self):
        before = [o.Name for o in self.doc.Objects]
        original = self.body.Shape.copy()
        self.launch(True)
        Gui.Control.activeTaskDialog().reject()
        self.assertEqual([o.Name for o in self.doc.Objects], before)
        self.assertSameShape(self.body.Shape, original)
        link = self.doc.addObject("App::Link", "Occurrence")
        link.setLink(self.body)
        self.doc.recompute()
        self.launch(True, [link])
        self.accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.assertIn("document-root", self.widget(QtWidgets.QLabel, "resultStatus").text())
        self.assertFalse([o for o in self.doc.Objects if o.TypeId == "Part::Mirroring"])
        self.assertFalse(self.doc.HasPendingTransaction)

    def testMissingAndInvalidPlaneRollbackThenRecover(self):
        invalid = self.doc.addObject("App::FeaturePython", "InvalidPlane")
        self.doc.recompute()
        self.launch(True)
        self.widget(QtWidgets.QComboBox, "comboBox").setCurrentIndex(3)
        Gui.Selection.clearSelection()
        before = [o.Name for o in self.doc.Objects]
        self.accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.assertIn("Select one valid", self.widget(QtWidgets.QLabel, "resultStatus").text())
        Gui.Selection.addSelection(invalid)
        self.accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.assertIn("no results were kept", self.widget(QtWidgets.QLabel, "resultStatus").text())
        self.assertEqual([o.Name for o in self.doc.Objects], before)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.widget(QtWidgets.QComboBox, "comboBox").setCurrentIndex(2)
        self.accept()
        self.assertFalse(Gui.Control.activeDialog())
        self.assertTrue(self.result(True).Shape.isValid())

    def testDirtySourcesPendingEditsAndReplacedIdentityReject(self):
        self.launch(True)
        self.doc.Base.Length = 12
        self.accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.assertIn("recompute", self.widget(QtWidgets.QLabel, "resultStatus").text())
        self.doc.recompute()
        self.doc.openTransaction("Other edit")
        self.body.Label = "Pending"
        self.accept()
        self.assertIn("transaction", self.widget(QtWidgets.QLabel, "resultStatus").text())
        self.assertTrue(self.doc.HasPendingTransaction)
        self.doc.abortTransaction()
        Gui.Control.activeTaskDialog().reject()
        source = self.doc.addObject("Part::Box", "Replaceable")
        self.doc.recompute()
        self.launch(True, [source])
        self.doc.removeObject("Replaceable")
        replacement = self.doc.addObject("Part::Box", "Replaceable")
        self.doc.recompute()
        self.assertEqual(replacement.Name, "Replaceable")
        self.accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.assertIn("deleted or replaced", self.widget(QtWidgets.QLabel, "resultStatus").text())
        self.assertFalse(self.doc.HasPendingTransaction)
