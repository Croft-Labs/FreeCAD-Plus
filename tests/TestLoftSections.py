# SPDX-License-Identifier: LGPL-2.1-or-later
"""Installed Part Loft section collection, result validation and persistence."""
from pathlib import Path
import tempfile
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets


def settle():
    Gui.updateGui()
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(150, loop.quit)
    loop.exec_()
    QtCore.QCoreApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)


def section(z, width=10):
    return Part.makePolygon([App.Vector(0, 0, z), App.Vector(width, 0, z),
                             App.Vector(width, 6, z)])


class TestLoftSections(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("LoftSections")
        self.doc.UndoMode = 1
        for i, width in enumerate((8, 10, 6)):
            obj = self.doc.addObject("Part::Feature", "Section%d" % i)
            obj.Label = "Section"  # Duplicate labels must retain separate identities.
            obj.Shape = section(i * 10, width)
        self.doc.recompute()
        self.sections = [self.doc.Section0, self.doc.Section1, self.doc.Section2]

    def tearDown(self):
        if Gui.Control.activeTaskDialog():
            Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        settle()

    def launch(self):
        settle()
        Gui.runCommand("Part_Loft")
        settle()
        self.message = Gui.getMainWindow().findChild(QtWidgets.QLabel, "loftSectionReview")
        self.assertIsNotNone(self.message)
        self.panel = self.message.parentWidget()
        self.available = self.panel.findChild(QtWidgets.QTreeWidget, "availableTreeWidget")
        self.selected = self.panel.findChild(QtWidgets.QTreeWidget, "selectedTreeWidget")

    def collect(self, names=None):
        for name in names or [obj.Name for obj in self.sections]:
            items = [self.available.topLevelItem(i) for i in range(self.available.topLevelItemCount())]
            item = next(item for item in items if item.data(0, QtCore.Qt.UserRole) == name)
            self.available.setCurrentItem(item)
            self.panel.findChild(QtWidgets.QPushButton, "addButton").click()
        settle()

    def option(self, name, value):
        self.panel.findChild(QtWidgets.QCheckBox, name).setChecked(value)

    def accept(self):
        Gui.Control.activeTaskDialog().accept()
        settle()

    def snapshot(self):
        return ([obj.Shape.exportBrepToString() for obj in self.sections],
                [obj.Name for obj in self.doc.Objects], self.doc.UndoCount)

    def testOpenWireSurfaceAndNativeOrder(self):
        before = self.snapshot()
        self.launch()
        self.collect(["Section0", "Section2", "Section1"])
        self.selected.setCurrentItem(self.selected.topLevelItem(2))
        self.panel.findChild(QtWidgets.QPushButton, "upButton").click()
        self.option("checkSolid", False)
        self.assertIn("3 sections", self.message.text())
        self.assertIn("Surface output", self.message.text())
        self.assertEqual(self.snapshot(), before)
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        loft = self.doc.Loft
        self.assertEqual(loft.Sections, self.sections)
        self.assertTrue(loft.Shape.isValid())
        self.assertFalse(loft.Shape.Solids)
        self.assertGreater(loft.Shape.Area, 0)
        self.assertEqual(self.doc.UndoCount, before[-1] + 1)
        for obj in self.sections:
            self.assertLess(obj.Shape.distToShape(loft.Shape)[0], 1e-6)
        self.assertEqual(self.snapshot()[0], before[0])

    def testSingleEdgesAndRuledOutput(self):
        for i, obj in enumerate(self.sections):
            obj.Shape = Part.makeLine(App.Vector(0, 0, i * 10), App.Vector(10, 0, i * 10))
        self.doc.recompute()
        self.launch()
        self.collect()
        self.option("checkSolid", False)
        self.option("checkRuledSurface", True)
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.assertTrue(self.doc.Loft.Ruled)
        self.assertAlmostEqual(self.doc.Loft.Shape.Area, 200, places=5)

    def testClosedProfilesStillCreateSolid(self):
        for i, obj in enumerate(self.sections):
            obj.Shape = Part.Wire([Part.makeCircle(5, App.Vector(0, 0, i * 10))])
        self.doc.recompute()
        self.launch()
        self.collect()
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.assertEqual(len(self.doc.Loft.Shape.Solids), 1)
        self.assertAlmostEqual(self.doc.Loft.Shape.Volume, 3.141592653589793 * 25 * 20, places=4)

    def testInvalidSolidRollsBackAndAllowsSurfaceRetry(self):
        before = self.snapshot()
        self.launch()
        self.collect()
        self.accept()
        self.assertTrue(Gui.Control.activeTaskDialog())
        self.assertIn("Loft was not created", self.message.text())
        self.assertIn("Loft did not produce a valid shape", self.message.text())
        self.assertEqual(self.snapshot(), before)
        self.option("checkSolid", False)
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.assertTrue(self.doc.Loft.Shape.isValid())

    def testCancelAndTooFewSectionsLeaveDocumentAlone(self):
        before = self.snapshot()
        self.launch()
        self.collect(["Section0"])
        self.accept()
        self.assertIn("at least two", self.message.text())
        self.assertTrue(Gui.Control.activeTaskDialog())
        Gui.Control.activeTaskDialog().reject()
        self.assertEqual(self.snapshot(), before)

    def testStaleSectionAndOwnerTransactionArePreserved(self):
        self.launch()
        self.collect()
        self.option("checkSolid", False)
        self.doc.Section1.touch()
        self.accept()
        self.assertIn("not current", self.message.text())
        self.assertIsNone(self.doc.getObject("Loft"))
        self.doc.recompute()
        self.doc.openTransaction("Owner edit")
        self.doc.Section0.Label = "Owner label"
        self.accept()
        self.assertIn("other edit transactions", self.message.text())
        self.assertEqual(self.doc.Section0.Label, "Owner label")
        self.doc.abortTransaction()

    def testUndoRedoReopenAndSectionEdit(self):
        self.launch()
        self.collect()
        self.option("checkSolid", False)
        self.accept()
        self.doc.undo()
        self.assertIsNone(self.doc.getObject("Loft"))
        self.doc.redo()
        self.doc.recompute()
        self.assertEqual(self.doc.Loft.Sections, self.sections)
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "Surface.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.sections = [self.doc.Section0, self.doc.Section1, self.doc.Section2]
            before = self.doc.Loft.Shape.Area
            self.doc.Section1.Shape = section(10, 15)
            self.doc.recompute()
            self.assertTrue(self.doc.Loft.Shape.isValid())
            self.assertNotAlmostEqual(self.doc.Loft.Shape.Area, before)
            self.assertEqual(self.doc.Loft.Sections, self.sections)
            self.assertLess(self.doc.Section1.Shape.distToShape(self.doc.Loft.Shape)[0], 1e-6)

    def testClosingDocumentClosesTask(self):
        self.launch()
        self.collect()
        App.closeDocument(self.doc.Name)
        settle()
        self.assertFalse(Gui.Control.activeTaskDialog())
