# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native sewing tolerance and existing Shape Builder lifecycle."""
import tempfile
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtWidgets
import ShapeSewing as Sewing


def enclosure(doc, name="Sheets", gap=0., open_top=False):
    faces = [face.copy() for face in Part.makeBox(10, 10, 10).Faces]
    top = max(faces, key=lambda face: face.CenterOfMass.z)
    if open_top:
        faces.remove(top)
    else:
        top.translate(App.Vector(0, 0, gap))
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = Part.makeCompound(faces)
    doc.recompute()
    return obj


class TestShapeSewing(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("SewingTest")
        self.doc.UndoMode = 1
        Gui.Selection.clearSelection()

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.closeDialog()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def panel(self, solid=False):
        Gui.runCommand("Part_Builder")
        Gui.updateGui()
        panels = Gui.Control.activeTaskDialog().getDialogContent()
        panel = next(p for p in panels if p.findChild(QtWidgets.QLabel, "sewingStatus"))
        name = "radioButtonSolidFromShell" if solid else "radioButtonShellFromFace"
        panel.findChild(QtWidgets.QRadioButton, name).click()
        panel.findChild(QtWidgets.QCheckBox, "checkRefine").setChecked(False)
        return panel

    def testNativeToleranceActuallyChangesJoin(self):
        obj = enclosure(self.doc, gap=.01)
        low = obj.Shape.copy()
        low.sewShape(1e-6)
        high = obj.Shape.copy()
        high.sewShape(.05)
        self.assertFalse(low.ShapeType == "Shell" and low.isClosed())
        self.assertEqual(high.ShapeType, "Shell")
        self.assertTrue(high.isClosed())
        self.assertTrue(high.isValid())
        self.assertEqual(obj.Shape.ShapeType, "Compound")
        for tolerance in (0, -1, float("nan"), float("inf")):
            with self.subTest(tolerance=tolerance), self.assertRaises(ValueError):
                low.sewShape(tolerance)

    def testClosedOpenAndDisconnectedReports(self):
        complete = enclosure(self.doc)
        shape, report = Sewing.review(self.doc, [(complete.Name, [])])
        self.assertEqual(report["kind"], "Closed shell")
        self.assertEqual(report["free_edges"], [])
        self.assertEqual((report["shells"], report["faces"]), (1, 6))
        refined, refined_report = Sewing.review(self.doc, [(complete.Name, [])], refine=True)
        self.assertEqual(refined_report["kind"], "Closed shell")
        self.assertTrue(refined.isValid())
        opened = enclosure(self.doc, "Open", open_top=True)
        _, report = Sewing.review(self.doc, [(opened.Name, [])])
        self.assertEqual(report["kind"], "Open shell")
        self.assertEqual(len(report["free_edges"]), 4)
        gap = enclosure(self.doc, "Gapped", gap=.01)
        _, report = Sewing.review(self.doc, [(gap.Name, [])], 1e-6)
        self.assertEqual(report["kind"], "Disconnected sheets")
        self.assertEqual(len(report["free_edges"]), 8)
        _, report = Sewing.review(self.doc, [(gap.Name, [])], .05)
        self.assertEqual(report["kind"], "Closed shell")
        self.assertEqual(report["tolerance"], .05)
        self.assertGreater(report["max_tolerance"], 1e-6)

    def testSnapshotPlacementUndoReopenAndSourcePreservation(self):
        obj = enclosure(self.doc)
        obj.Placement.Base = App.Vector(7, 8, 9)
        self.doc.recompute()
        original = obj.Shape.exportBrepToString()
        shell, _ = Sewing.create(self.doc, [(obj.Name, [])])
        solid, report = Sewing.create(self.doc, [(shell.Name, [])], refine=True, solid=True)
        self.assertEqual(report["kind"], "Valid solid")
        self.assertAlmostEqual(solid.Shape.Volume, 1000)
        self.assertAlmostEqual(solid.Shape.BoundBox.XMin, 7)
        self.assertTrue(obj.ViewObject.Visibility)
        self.assertEqual(original, obj.Shape.exportBrepToString())
        solid_name = solid.Name
        self.doc.undo()
        self.assertIsNone(self.doc.getObject(solid_name))
        self.doc.redo()
        obj.Placement.Base = App.Vector(70, 80, 90)
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.getObject(solid_name).Shape.BoundBox.XMin, 7)
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "Sewn.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.doc.recompute()
            self.assertAlmostEqual(self.doc.getObject(solid_name).Shape.Volume, 1000)
            self.assertEqual(self.doc.Shell.SourceFaces, ["Sheets.Face" + str(i) for i in range(1, 7)])
            self.assertAlmostEqual(self.doc.Shell.SewingTolerance.Value, 1e-6)

    def testInvalidInputsAndTransactionsLeaveNoResult(self):
        obj = enclosure(self.doc)
        count = len(self.doc.Objects)
        for tolerance in (0, -1, 2, float("nan")):
            with self.assertRaises(ValueError):
                Sewing.create(self.doc, [(obj.Name, [])], tolerance)
        with self.assertRaises(ValueError):
            Sewing.create(self.doc, [(obj.Name, ["Edge1"])])
        self.doc.openTransaction("Owner")
        with self.assertRaises(ValueError):
            Sewing.create(self.doc, [(obj.Name, [])])
        self.doc.abortTransaction()
        obj.touch()
        with self.assertRaises(ValueError):
            Sewing.create(self.doc, [(obj.Name, [])])
        self.doc.recompute()
        container = self.doc.addObject("App::Part", "Container")
        container.addObject(obj)
        self.doc.recompute()
        before_nested = list(self.doc.Objects)
        with self.assertRaises(ValueError):
            Sewing.create(self.doc, [(obj.Name, [])])
        self.assertEqual(list(self.doc.Objects), before_nested)
        self.assertIsNone(self.doc.getObject("Shell"))

    def testOpenShellCannotBecomeSolid(self):
        obj = enclosure(self.doc, open_top=True)
        shell, _ = Sewing.create(self.doc, [(obj.Name, [])])
        before = len(self.doc.Objects)
        with self.assertRaisesRegex(ValueError, "shell is open"):
            Sewing.create(self.doc, [(shell.Name, [])], solid=True)
        self.assertEqual(len(self.doc.Objects), before)

    def testNativePanelCheckCreateAndClose(self):
        obj = enclosure(self.doc)
        panel = self.panel()
        for i in range(1, 7):
            Gui.Selection.addSelection(obj, "Face" + str(i))
        before = (list(self.doc.Objects), self.doc.UndoCount)
        panel.findChild(QtWidgets.QPushButton, "checkShapeButton").click()
        message = panel.findChild(QtWidgets.QLabel, "sewingStatus")
        self.assertIn("Closed shell", message.text())
        self.assertEqual(before, (list(self.doc.Objects), self.doc.UndoCount))
        panel.findChild(QtWidgets.QPushButton, "createButton").click()
        self.assertIsNotNone(self.doc.getObject("Shell"), message.text())
        # The existing face-only selection gate rejects whole shell selection.
        self.assertEqual(Gui.Selection.getSelection(), [])
        panel.findChild(QtWidgets.QRadioButton, "radioButtonSolidFromShell").click()
        Gui.Selection.addSelection(self.doc.Shell)
        panel.findChild(QtWidgets.QPushButton, "checkShapeButton").click()
        self.assertIn("Valid solid", message.text())
        panel.findChild(QtWidgets.QPushButton, "createButton").click()
        self.assertAlmostEqual(self.doc.Solid.Shape.Volume, 1000)
        Gui.Control.closeDialog()
        self.assertAlmostEqual(self.doc.Solid.Shape.Volume, 1000)

    def testPanelGapFailurePreservesSelectionAndAllowsCorrection(self):
        obj = enclosure(self.doc, gap=.01)
        panel = self.panel()
        panel.findChild(QtWidgets.QCheckBox, "checkFaces").setChecked(True)
        Gui.Selection.addSelection(obj, "Face1")
        check = panel.findChild(QtWidgets.QPushButton, "checkShapeButton")
        message = panel.findChild(QtWidgets.QLabel, "sewingStatus")
        check.click()
        self.assertIn("Disconnected sheets", message.text())
        panel.findChild(QtWidgets.QDoubleSpinBox, "sewingTolerance").setValue(.05)
        self.assertIn("Inputs changed", message.text())
        check.click()
        self.assertIn("Closed shell", message.text())
        Gui.Control.closeDialog()
        self.assertEqual(self.doc.Objects, [obj])
        opened = enclosure(self.doc, "Open", open_top=True)
        shell, _ = Sewing.create(self.doc, [(opened.Name, [])])
        panel = self.panel(solid=True)
        Gui.Selection.addSelection(shell)
        panel.findChild(QtWidgets.QPushButton, "createButton").click()
        self.assertIn("shell is open", panel.findChild(QtWidgets.QLabel, "sewingStatus").text())
        self.assertEqual(Gui.Selection.getSelection(), [shell])
        self.assertIsNone(self.doc.getObject("Solid"))

    def testCurvedSeamIsNotReportedAsFreeBoundary(self):
        obj = self.doc.addObject("Part::Feature", "CylinderSheets")
        obj.Shape = Part.makeCompound([face.copy() for face in Part.makeCylinder(5, 10).Faces])
        self.doc.recompute()
        _, report = Sewing.review(self.doc, [(obj.Name, [])])
        self.assertEqual(report["kind"], "Closed shell")
        self.assertEqual(report["free_edges"], [])
