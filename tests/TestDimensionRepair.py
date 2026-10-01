# SPDX-License-Identifier: LGPL-2.1-or-later
"""Exercise the installed native TechDraw dimension repair task."""
from pathlib import Path
import tempfile
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets


def settle():
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(1800, loop.quit)
    loop.exec_()
    Gui.updateGui()


def make_fixture():
    doc = App.newDocument("DimensionRepair")
    doc.UndoMode = 1
    small = doc.addObject("Part::Cylinder", "Small")
    large = doc.addObject("Part::Cylinder", "Large")
    small.Radius, large.Radius = 5, 8
    large.Placement.Base = App.Vector(25, 0, 0)
    page = doc.addObject("TechDraw::DrawPage", "Page")
    template = doc.addObject("TechDraw::DrawSVGTemplate", "Template")
    template.Template = App.getResourceDir() + "Mod/TechDraw/Templates/ISO/A4_Landscape_ISO5457_notitleblock.svg"
    page.Template = template
    view = doc.addObject("TechDraw::DrawViewPart", "View")
    view.Source = [small, large]
    view.Direction = App.Vector(0, 0, 1)
    page.addView(view)
    doc.recompute()
    settle()
    edge = next("Edge%d" % i for i, e in enumerate(small.Shape.Edges, 1)
                if isinstance(e.Curve, Part.Circle))
    dim = doc.addObject("TechDraw::DrawViewDimension", "Diameter")
    dim.Type = "Diameter"
    dim.References2D = [(view, "")]
    dim.References3D = [(small, edge)]
    dim.MeasureType = "True"
    page.addView(dim)
    dim.X, dim.Y = 140, 120
    doc.recompute()
    settle()
    return doc, edge


def projected_circle(view, radius):
    for i in range(20):
        name = "Edge%d" % i
        try:
            edge = view.getEdgeBySelection(name)
            if isinstance(edge.Curve, Part.Circle) and abs(edge.Curve.Radius - radius) < 1e-6:
                return name
        except (ValueError, RuntimeError):
            pass
    raise AssertionError("No projected circle with radius %s" % radius)


class TestDimensionRepair(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("TechDrawWorkbench")
        self.doc, self.source_edge = make_fixture()
        self.dim = self.doc.Diameter
        self.assertAlmostEqual(self.dim.getRawValue(), 10)
        self.small = projected_circle(self.doc.View, 5)
        self.large = projected_circle(self.doc.View, 8)

    def tearDown(self):
        if Gui.Control.activeTaskDialog():
            Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def launch(self):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.dim)
        Gui.runCommand("TechDraw_DimensionRepair")
        Gui.updateGui()
        self.status = Gui.getMainWindow().findChild(QtWidgets.QLabel, "dimensionRepairStatus")
        self.assertIsNotNone(self.status)
        self.panel = self.status.parentWidget()

    def choose(self, obj, *subnames):
        Gui.Selection.clearSelection()
        for sub in subnames:
            Gui.Selection.addSelection(obj, sub)
        self.panel.findChild(QtWidgets.QPushButton, "pbSelection").click()
        Gui.updateGui()

    def accept(self):
        Gui.Control.activeTaskDialog().accept()
        Gui.updateGui()

    def state(self):
        return (self.dim.References2D, self.dim.References3D, str(self.dim.MeasureType),
                self.dim.getRawValue(), self.doc.UndoCount)

    def testProjectedSwitchClearsOld3DAndPreservesModel(self):
        volumes = [self.doc.Small.Shape.Volume, self.doc.Large.Shape.Volume]
        before = self.state()
        self.launch()
        self.choose(self.doc.View, self.large)
        self.assertEqual(self.state(), before)
        self.assertIn("projected 2D", self.status.text())
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.assertFalse(self.dim.References3D)
        self.assertEqual(str(self.dim.MeasureType), "Projected")
        self.assertAlmostEqual(self.dim.getRawValue(), 16)
        self.assertEqual(self.doc.UndoCount, before[-1] + 1)
        self.assertEqual(volumes, [self.doc.Small.Shape.Volume, self.doc.Large.Shape.Volume])

    def testTrue3DSwitchPreservesFormatting(self):
        self.dim.References3D = []
        self.dim.References2D = [(self.doc.View, self.large)]
        self.dim.MeasureType = "Projected"
        self.dim.FormatSpec = "Diameter %.2f"
        self.doc.recompute()
        self.launch()
        self.choose(self.doc.Small, self.source_edge)
        self.assertIn("true 3D", self.status.text())
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.assertEqual(str(self.dim.MeasureType), "True")
        self.assertAlmostEqual(self.dim.getRawValue(), 10)
        self.assertEqual(self.dim.FormatSpec, "Diameter %.2f")

    def testCancelHasNoMutationOrUndo(self):
        before = self.state()
        self.launch()
        self.choose(self.doc.View, self.large)
        Gui.Control.activeTaskDialog().reject()
        self.assertEqual(self.state(), before)

    def testFailedReferenceFormRestoresAndAllowsRetry(self):
        before = self.state()
        self.launch()
        self.choose(self.doc.View, self.small, self.large)
        self.accept()
        self.assertTrue(Gui.Control.activeTaskDialog())
        self.assertIn("Original references were restored", self.status.text())
        self.assertEqual(self.state(), before)
        self.choose(self.doc.View, self.large)
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.assertAlmostEqual(self.dim.getRawValue(), 16)

    def testNoSelectionStaysOpen(self):
        before = self.state()
        self.launch()
        self.accept()
        self.assertTrue(Gui.Control.activeTaskDialog())
        self.assertIn("Use Selection", self.status.text())
        self.assertEqual(self.state(), before)

    def testOtherTransactionIsPreserved(self):
        self.launch()
        self.choose(self.doc.View, self.large)
        self.doc.openTransaction("Owner edit")
        self.doc.Small.Label = "Owner label"
        self.accept()
        self.assertTrue(Gui.Control.activeTaskDialog())
        self.assertIn("other edit transaction", self.status.text())
        self.assertAlmostEqual(self.dim.getRawValue(), 10)
        self.assertEqual(self.doc.Small.Label, "Owner label")
        self.doc.abortTransaction()

    def testUndoRedoReopenAndAssociativeEdit(self):
        self.launch()
        self.choose(self.doc.View, self.large)
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.doc.undo()
        self.doc.recompute()
        self.assertTrue(self.dim.References3D)
        self.assertAlmostEqual(self.dim.getRawValue(), 10)
        self.doc.redo()
        self.doc.recompute()
        self.assertFalse(self.dim.References3D)
        self.assertAlmostEqual(self.dim.getRawValue(), 16)
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "Repaired.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.dim = self.doc.Diameter
            self.doc.recompute()
            settle()  # Finish the asynchronous restored-view projection before editing it.
            self.assertAlmostEqual(self.dim.getRawValue(), 16)
            self.doc.Large.Radius = 9
            self.doc.recompute()
            settle()
            self.assertFalse(self.dim.References3D)
            self.assertAlmostEqual(self.dim.getRawValue(), 18)
            self.assertAlmostEqual(self.doc.Small.Radius.Value, 5)
