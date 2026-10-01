# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native assembly solver guidance and relationship navigation."""
from pathlib import Path
import tempfile
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import JointObject
from PySide import QtCore, QtWidgets


def settle():
    Gui.updateGui()
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(200, loop.quit)
    loop.exec_()
    # A macro keeps the outer event loop occupied across tests. Deliver native
    # deleteLater events before looking up a new document's contextual widgets.
    QtCore.QCoreApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)


class TestAssemblyFreedom(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("AssemblyWorkbench")
        self.doc = App.newDocument("AssemblyFreedom")
        self.doc.UndoMode = 1
        self.assembly = self.doc.addObject("Assembly::AssemblyObject", "Product")
        self.joints = self.assembly.newObject("Assembly::JointGroup", "Joints")
        for name, x in (("Base", 0), ("Slider", 20), ("Free", 40)):
            obj = self.assembly.newObject("Part::Box", name)
            obj.Placement.Base = App.Vector(x, 0, 0)
        ground = self.joints.newObject("App::FeaturePython", "Ground")
        JointObject.GroundedJoint(ground, self.doc.Base)
        JointObject.ViewProviderGroundedJoint(ground.ViewObject)
        self.doc.recompute()

    def tearDown(self):
        if Gui.Control.activeTaskDialog():
            Gui.Control.closeDialog()
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        settle()

    def edit(self):
        settle()  # Let native document/task watchers register before entering edit mode.
        self.assertTrue(Gui.activeDocument().setEdit(self.assembly.Name))
        self.refresh()
        window = Gui.getMainWindow()
        self.message = window.findChild(QtWidgets.QLabel, "assemblyFreedomExplanation")
        self.grounded = window.findChild(QtWidgets.QPushButton, "selectAssemblyGrounded")
        self.unconnected = window.findChild(QtWidgets.QPushButton, "selectAssemblyUnconnected")
        self.assertIsNotNone(self.message)

    def refresh(self):
        self.doc.recompute()
        self.assembly.solve()
        self.doc.recompute()
        settle()

    def joint(self, kind="Slider", target="Slider"):
        obj = self.joints.newObject("App::FeaturePython", "Joint")
        JointObject.Joint(obj, JointObject.JointTypes.index(kind))
        JointObject.ViewProviderJoint(obj.ViewObject)
        obj.Proxy.setJointConnectors(obj, [[self.doc.Base, ["Face6", "Vertex7"]],
                                         [self.doc.getObject(target), ["Face6", "Vertex7"]]])
        self.refresh()
        return obj

    def selection(self):
        return {obj.Name for obj in Gui.Selection.getSelection()}

    def snapshot(self):
        return [(obj.Name, obj.Placement.toMatrix().A, obj.Shape.Volume)
                for obj in (self.doc.Base, self.doc.Slider, self.doc.Free)], self.doc.UndoCount

    def testGroundedAndUnconnectedSelectionDoesNotEdit(self):
        self.edit()
        before = self.snapshot()
        self.grounded.click()
        self.assertEqual(self.selection(), {"Base"})
        self.unconnected.click()
        self.assertEqual(self.selection(), {"Slider", "Free"})
        self.assertEqual(self.snapshot(), before)
        self.assertIn("not each component", self.message.text())

    def testSliderFreedomIsNotMistakenForDisconnected(self):
        self.edit()
        joint = self.joint()
        self.assertTrue(self.unconnected.isEnabled())
        self.assertIn("connected sliders", self.message.text())
        self.unconnected.click()
        self.assertEqual(self.selection(), {"Free"})
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.doc.Slider)
        Gui.runCommand("Assembly_SelectJointsOfComponent")
        self.assertIn(joint.Name, self.selection())

    def testFullyConstrainedAndGroundingRemainDistinct(self):
        self.edit()
        self.joint("Fixed")
        self.joint("Fixed", "Free")
        self.assertFalse(self.unconnected.isEnabled())
        self.assertIn("no remaining assembly freedom", self.message.text())
        self.grounded.click()
        self.assertIn("Base", self.selection())

    def testRedundantJointsDoNotAdvertiseFreedom(self):
        self.edit()
        self.joint("Fixed")
        joint = self.joint("Fixed")
        self.assertFalse(self.unconnected.isEnabled())
        self.assertIn("Resolve the solver issue", self.message.text())
        Gui.Selection.clearSelection()
        self.unconnected.click()
        self.assertFalse(self.selection())
        self.doc.removeObject(joint.Name)
        self.refresh()
        self.assertTrue(self.unconnected.isEnabled())

    def testStaleAssemblyRefusesSelection(self):
        self.edit()
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.doc.Base)
        self.assembly.touch()
        self.unconnected.click()
        self.assertEqual(self.selection(), {"Base"})
        self.assertIn("Recompute", self.message.text())
        self.refresh()
        self.unconnected.click()
        self.assertEqual(self.selection(), {"Slider", "Free"})

    def testContextPanelSurvivesTaskDialog(self):
        self.edit()
        self.assertTrue(self.message.isVisible())

        class TemporaryTask:
            def __init__(self):
                self.form = QtWidgets.QWidget()

            def getStandardButtons(self):
                return QtWidgets.QDialogButtonBox.Cancel.value

            def reject(self):
                return True

        Gui.Control.showDialog(TemporaryTask())
        settle()
        self.assertTrue(self.message.isVisible())
        Gui.Control.closeDialog()
        settle()
        self.assertTrue(self.message.isVisible())
        self.grounded.click()
        self.assertEqual(self.selection(), {"Base"})

    def testOtherDocumentDoesNotShowAssemblyContext(self):
        self.edit()
        other = App.newDocument("OtherDocument")
        settle()
        labels = Gui.getMainWindow().findChildren(QtWidgets.QLabel, "assemblyFreedomExplanation")
        self.assertFalse(any(label.isVisible() for label in labels))
        App.setActiveDocument(self.doc.Name)
        Gui.activeDocument().activeView()
        settle()
        if not Gui.activeDocument().getInEdit():
            self.edit()
        self.refresh()
        self.message = Gui.getMainWindow().findChild(QtWidgets.QLabel, "assemblyFreedomExplanation")
        self.assertTrue(self.message.isVisible())
        App.closeDocument(other.Name)

    def testJointUndoRedoAndReopen(self):
        self.edit()
        self.doc.openTransaction("Connect slider")
        self.joint()
        self.doc.commitTransaction()
        self.unconnected.click()
        self.assertEqual(self.selection(), {"Free"})
        self.doc.undo()
        self.refresh()
        self.unconnected.click()
        self.assertEqual(self.selection(), {"Slider", "Free"})
        self.doc.redo()
        self.refresh()
        self.unconnected.click()
        self.assertEqual(self.selection(), {"Free"})
        Gui.activeDocument().resetEdit()
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "Assembly.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.assembly, self.joints = self.doc.Product, self.doc.Joints
            self.edit()
            self.unconnected.click()
            self.assertEqual(self.selection(), {"Free"})
            self.grounded.click()
            self.assertEqual(self.selection(), {"Base"})
