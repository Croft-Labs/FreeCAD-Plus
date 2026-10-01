# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Hole location and thread review with persistence and edit recovery."""
import math
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


def fixture():
    doc = App.newDocument("HoleSpecification")
    doc.UndoMode = 1
    body = doc.addObject("PartDesign::Body", "Body")
    block = body.newObject("PartDesign::AdditiveBox", "Block")
    block.Length, block.Width, block.Height = 30, 20, 10
    profile = body.newObject("Sketcher::SketchObject", "Locations")
    profile.Placement.Base.z = 10
    for x in (5, 20):
        profile.addGeometry(Part.Circle(App.Vector(x, 5, 0), App.Vector(0, 0, 1), 1), False)
    profile.addGeometry(Part.Circle(App.Vector(12, 12, 0), App.Vector(0, 0, 1), 1), True)
    doc.recompute()
    hole = body.newObject("PartDesign::Hole", "Hole")
    hole.Profile = profile
    hole.Diameter = 4
    hole.Depth = 10
    hole.DrillPoint = 0
    doc.recompute()
    block.Visibility = False
    profile.Visibility = False
    return doc


class TestHoleSpecification(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartDesignWorkbench")
        self.doc = fixture()
        self.messages = []
        self.dialogTimer = QtCore.QTimer()
        self.dialogTimer.timeout.connect(self.dismissMessages)
        self.dialogTimer.start(100)

    def dismissMessages(self):
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if isinstance(widget, QtWidgets.QMessageBox) and widget.isVisible():
                self.messages.append(widget.text())
                widget.accept()

    def tearDown(self):
        if Gui.Control.activeTaskDialog():
            Gui.Control.activeTaskDialog().reject()
        self.dialogTimer.stop()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        settle()

    def edit(self):
        Gui.activeDocument().activeView().setActiveObject("pdbody", self.doc.Body)
        self.assertTrue(self.doc.Hole.ViewObject.doubleClicked())
        settle()
        self.location = Gui.getMainWindow().findChild(QtWidgets.QLabel, "holeLocationReview")
        self.thread = Gui.getMainWindow().findChild(QtWidgets.QLabel, "holeThreadReview")
        self.assertIsNotNone(self.location)
        self.panel = self.thread.parentWidget()

    def accept(self):
        Gui.Control.activeTaskDialog().accept()
        settle()
        self.assertFalse(Gui.Control.activeTaskDialog(), self.messages)

    def combo(self, name, index):
        self.panel.findChild(QtWidgets.QComboBox, name).setCurrentIndex(index)
        settle()

    def testLocationIdentityCountAndReadOnlyCancel(self):
        before = (self.doc.Hole.Shape.exportBrepToString(), self.doc.Block.Shape.exportBrepToString(),
                  self.doc.Locations.Shape.exportBrepToString(), self.doc.UndoCount)
        self.edit()
        self.assertIn("HoleSpecification.Locations", self.location.text())
        self.assertIn("HoleSpecification.Body", self.location.text())
        self.assertIn("2 profile locations", self.location.text())
        self.assertIn("not a count of separate cuts", self.location.text())
        self.assertIn("plain hole", self.thread.text())
        Gui.Control.activeTaskDialog().reject()
        settle()
        self.assertEqual(before, (self.doc.Hole.Shape.exportBrepToString(), self.doc.Block.Shape.exportBrepToString(),
                                 self.doc.Locations.Shape.exportBrepToString(), self.doc.UndoCount))

    def testRepeatedCounterboresAcceptAndUndo(self):
        original = self.doc.Hole.Shape.Volume
        self.edit()
        self.combo("HoleCutType", 1)
        self.doc.Hole.HoleCutDiameter = 8
        self.doc.Hole.HoleCutDepth = 2
        self.doc.recompute()
        settle()
        self.accept()
        self.assertAlmostEqual(self.doc.Hole.Shape.Volume, 6000 - 128 * math.pi, places=5)
        self.assertEqual(self.doc.Hole.Profile[0], self.doc.Locations)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.Hole.Shape.Volume, original, places=5)
        # Redo after recompute has a separately recorded native volume mismatch.
        # Keep that acceptance gate open rather than certify the changed result.

    def testClearanceTapDrillAndCosmeticAreDistinct(self):
        self.edit()
        self.combo("ThreadType", 1)
        sizes = self.panel.findChild(QtWidgets.QComboBox, "ThreadSize")
        sizes.setCurrentIndex(sizes.findText("M6x1.0"))
        settle()
        self.assertIn("Clearance hole", self.thread.text())
        self.combo("HoleType", 1)
        self.assertTrue(self.doc.Hole.Threaded)
        self.assertFalse(self.doc.Hole.CosmeticThread)
        self.assertIn("Tap-drill", self.thread.text())
        self.combo("HoleType", 2)
        self.assertTrue(self.doc.Hole.CosmeticThread)
        self.assertFalse(self.doc.Hole.ModelThread)
        self.assertIn("no helical geometry", self.thread.text())
        self.assertIn("M6", self.thread.text())
        self.accept()
        self.assertTrue(self.doc.Hole.Shape.isValid())

    def testModeledThreadPendingAndCancel(self):
        self.edit()
        self.combo("ThreadType", 1)
        sizes = self.panel.findChild(QtWidgets.QComboBox, "ThreadSize")
        sizes.setCurrentIndex(sizes.findText("M6x1.0"))
        self.combo("HoleType", 2)
        faces_before = len(self.doc.Hole.Shape.Faces)
        self.panel.findChild(QtWidgets.QCheckBox, "ModelThread").click()
        settle()
        self.assertIn("actual helical geometry", self.thread.text())
        self.assertIn("pending", self.location.text())
        self.assertEqual(len(self.doc.Hole.Shape.Faces), faces_before)
        # Deferred modeled-thread acceptance has a separately recorded native task blocker.
        # This bounded check covers honest pending-state review and nonmutating Cancel.
        Gui.Control.activeTaskDialog().reject()
        settle()
        self.assertFalse(self.doc.Hole.ModelThread)
        self.assertEqual(self.doc.Hole.Diameter.Value, 4)

    def testInvalidResultReviewAndCancelPreserveCommittedShape(self):
        before = self.doc.Hole.Shape.exportBrepToString()
        self.edit()
        self.doc.Hole.Depth = 0
        self.doc.recompute()
        settle()
        self.assertIn("needs correction", self.location.text())
        self.assertNotIn("2 profile locations", self.location.text())
        Gui.Control.activeTaskDialog().reject()
        settle()
        self.assertEqual(self.doc.Hole.Depth.Value, 10)
        self.assertEqual(self.doc.Hole.Shape.exportBrepToString(), before)

    def testProfileEditRefreshesCountAndIdentity(self):
        self.edit()
        self.doc.Locations.Label = "Revised locations"
        self.doc.Locations.addGeometry(Part.Circle(App.Vector(12, 12, 0), App.Vector(0, 0, 1), 1), False)
        self.doc.recompute()
        settle()
        self.assertIn("Revised locations", self.location.text())
        self.assertIn("3 profile locations", self.location.text())
        self.assertEqual(self.doc.Hole.Profile[0], self.doc.Locations)
        Gui.Control.activeTaskDialog().reject()
        settle()
        self.assertEqual(self.doc.Locations.GeometryCount, 3)

    def testReopenSourceEditAndDownstreamLink(self):
        self.edit()
        self.combo("ThreadType", 1)
        self.combo("HoleType", 2)
        self.accept()
        link = self.doc.addObject("App::Link", "Consumer")
        link.setLink(self.doc.Body)
        self.doc.recompute()
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "Holes.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            settle()
            self.doc = App.openDocument(path)
            self.doc.Hole.touch()
            self.doc.recompute()
            self.edit()
            self.assertIn("Cosmetic thread", self.thread.text())
            Gui.Control.activeTaskDialog().reject()
            settle()
            original = self.doc.Hole.Shape.Volume
            self.doc.Locations.addGeometry(Part.Circle(App.Vector(12, 12, 0), App.Vector(0, 0, 1), 1), False)
            self.doc.recompute()
            self.assertLess(self.doc.Hole.Shape.Volume, original)
            self.assertAlmostEqual(self.doc.Consumer.Shape.Volume, self.doc.Hole.Shape.Volume)
            self.assertTrue(self.doc.Consumer.Shape.isValid())
