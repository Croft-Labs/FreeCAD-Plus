# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Sweep path capture, atomic output and association."""
from pathlib import Path
import math
import tempfile
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets


def settle():
    Gui.updateGui()
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(120, loop.quit)
    loop.exec_()
    QtCore.QCoreApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)


class TestSweepInputs(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("SweepInputs")
        self.doc.UndoMode = 1
        self.profile = self.doc.addObject("Part::Feature", "Profile")
        self.profile.Shape = Part.Wire([Part.makeCircle(2)])
        self.path = self.doc.addObject("Part::Feature", "Path")
        self.path.Shape = Part.makeLine(App.Vector(0, 0, 0), App.Vector(0, 0, 20))
        self.doc.recompute()

    def tearDown(self):
        if Gui.Control.activeTaskDialog():
            Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        settle()

    def launch(self):
        Gui.Selection.clearSelection()
        Gui.runCommand("Part_Sweep")
        settle()
        self.message = Gui.getMainWindow().findChild(QtWidgets.QLabel, "sweepInputReview")
        self.assertIsNotNone(self.message)
        self.panel = self.message.parentWidget()
        self.available = self.panel.findChild(QtWidgets.QTreeWidget, "availableTreeWidget")
        self.selected = self.panel.findChild(QtWidgets.QTreeWidget, "selectedTreeWidget")

    def collect(self, names=None):
        for name in names or [self.profile.Name]:
            item = next(self.available.topLevelItem(i) for i in range(self.available.topLevelItemCount())
                        if self.available.topLevelItem(i).data(0, QtCore.Qt.UserRole) == name)
            self.available.setCurrentItem(item)
            self.panel.findChild(QtWidgets.QPushButton, "addButton").click()
        settle()

    def capture(self, obj=None, subs=None):
        button = self.panel.findChild(QtWidgets.QPushButton, "buttonPath")
        button.click()
        obj = obj or self.path
        if subs:
            for sub in subs:
                Gui.Selection.addSelection(obj, sub)
        else:
            Gui.Selection.addSelection(obj)
        button.click()
        settle()

    def accept(self):
        Gui.Control.activeTaskDialog().accept()
        settle()

    def snapshot(self):
        return ([o.Name for o in self.doc.Objects], self.doc.UndoCount,
                self.profile.Shape.exportBrepToString(), self.path.Shape.exportBrepToString())

    def testCapturedPathSurvivesProfileAndGlobalSelection(self):
        before = self.snapshot()
        self.launch()
        self.capture()
        self.collect()
        self.assertIn("[Path]", self.panel.findChild(QtWidgets.QLabel, "labelPath").text())
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.profile)
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.assertEqual(self.doc.Sweep.Spine[0], self.path)
        self.assertEqual(self.doc.Sweep.Sections, [self.profile])
        self.assertTrue(self.doc.Sweep.Shape.isValid())
        self.assertAlmostEqual(self.doc.Sweep.Shape.Volume, math.pi * 4 * 20, places=5)
        self.assertEqual(self.snapshot()[2:], before[2:])
        self.assertEqual(self.doc.UndoCount, before[1] + 1)

    def testMultipleEdgesAreRetainedAndDisconnectedCaptureRefused(self):
        self.path.Shape = Part.makePolygon([App.Vector(0, 0, 0), App.Vector(0, 0, 10), App.Vector(0, 0, 20)])
        wrong = self.doc.addObject("Part::Feature", "Disconnected")
        wrong.Shape = Part.makeCompound([Part.makeLine(App.Vector(0,0,0), App.Vector(0,0,10)),
                                         Part.makeLine(App.Vector(10,0,10), App.Vector(10,0,20))])
        self.doc.recompute()
        self.launch()
        self.collect()
        self.capture(wrong, ["Edge1", "Edge2"])
        self.assertIn("No path captured", self.message.text())
        self.accept()
        self.assertTrue(Gui.Control.activeTaskDialog())
        self.capture(self.path, ["Edge1", "Edge2"])
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.assertEqual(list(self.doc.Sweep.Spine[1]), ["Edge1", "Edge2"])
        self.assertAlmostEqual(self.doc.Sweep.Shape.Volume, math.pi * 4 * 20, places=5)

    def testOpenProfileSolidRollbackAndSurfaceRetry(self):
        self.profile.Shape = Part.makeLine(App.Vector(-4,0,0), App.Vector(4,0,0))
        self.doc.recompute()
        before = self.snapshot()
        self.launch()
        self.collect()
        self.capture()
        self.accept()
        self.assertTrue(Gui.Control.activeTaskDialog())
        self.assertIn("Sweep was not created", self.message.text())
        self.assertEqual(self.snapshot(), before)
        self.panel.findChild(QtWidgets.QCheckBox, "checkSolid").setChecked(False)
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.assertTrue(self.doc.Sweep.Shape.isValid())
        self.assertFalse(self.doc.Sweep.Shape.Solids)
        self.assertAlmostEqual(self.doc.Sweep.Shape.Area, 160, places=5)

    def testStaleAndReplacedCapturedPathAreRefused(self):
        self.launch()
        self.collect()
        self.capture()
        self.path.touch()
        self.accept()
        self.assertIn("captured path", self.message.text())
        self.doc.recompute()
        self.doc.removeObject(self.path.Name)
        self.path = self.doc.addObject("Part::Feature", "Path")
        self.path.Shape = Part.makeLine(App.Vector(0,0,0), App.Vector(0,0,20))
        self.doc.recompute()
        self.accept()
        self.assertIn("replaced", self.message.text())
        self.assertIsNone(self.doc.getObject("Sweep"))
        self.capture()
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())

    def testMissingSectionAndSameProfilePathAreRefused(self):
        self.launch()
        self.capture()
        self.accept()
        self.assertIn("at least one section", self.message.text())
        self.collect([self.path.Name])
        self.accept()
        self.assertIn("cannot also", self.message.text())
        Gui.Control.activeTaskDialog().reject()
        settle()
        self.launch()
        self.collect()
        self.capture()
        self.profile.touch()
        self.accept()
        self.assertIn("section is", self.message.text())
        self.assertIsNone(self.doc.getObject("Sweep"))

    def testCancelWhilePickingAndDocumentClose(self):
        before = self.snapshot()
        self.launch()
        self.collect()
        self.panel.findChild(QtWidgets.QPushButton, "buttonPath").click()
        Gui.Control.activeTaskDialog().reject()
        settle()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.assertEqual(self.snapshot(), before)
        # A fresh native selection works after collector cleanup.
        box = self.doc.addObject("Part::Box", "SelectionProbe")
        self.doc.recompute()
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(box)
        self.assertEqual(Gui.Selection.getSelection(), [box])
        self.launch()
        App.closeDocument(self.doc.Name)
        settle()
        self.assertFalse(Gui.Control.activeTaskDialog())

    def testOwnerTransactionAndDocumentSwitchArePreserved(self):
        self.launch()
        self.collect()
        self.capture()
        self.doc.openTransaction("Owner edit")
        self.profile.Label = "Owner label"
        self.accept()
        self.assertIn("other edit transactions", self.message.text())
        self.assertEqual(self.profile.Label, "Owner label")
        self.doc.abortTransaction()
        App.newDocument("Other")
        settle()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.assertIsNone(self.doc.getObject("Sweep"))

    def testUndoRedoReopenPathEditAndDownstream(self):
        self.launch()
        self.collect()
        self.capture()
        self.panel.findChild(QtWidgets.QCheckBox, "checkFrenet").setChecked(False)
        self.accept()
        self.assertFalse(Gui.Control.activeTaskDialog())
        self.doc.undo()
        self.assertIsNone(self.doc.getObject("Sweep"))
        self.doc.redo()
        self.doc.recompute()
        link = self.doc.addObject("App::Link", "Consumer")
        link.setLink(self.doc.Sweep)
        self.doc.recompute()
        with tempfile.TemporaryDirectory() as folder:
            filename = str(Path(folder) / "Sweep.FCStd")
            self.doc.saveAs(filename)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(filename)
            self.doc.Path.Shape = Part.makeLine(App.Vector(0,0,0), App.Vector(0,0,30))
            self.doc.recompute()
            self.assertFalse(self.doc.Sweep.Frenet)
            self.assertEqual(self.doc.Sweep.Spine[0], self.doc.Path)
            self.assertTrue(self.doc.Sweep.Shape.isValid())
            self.assertAlmostEqual(self.doc.Sweep.Shape.Volume, math.pi * 4 * 30, places=5)
            self.assertAlmostEqual(self.doc.Consumer.Shape.Volume, math.pi * 4 * 30, places=5)
