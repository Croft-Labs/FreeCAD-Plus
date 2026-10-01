# SPDX-License-Identifier: LGPL-2.1-or-later
"""Drive the native ray-pick menu; preserve occurrence identity and command gates."""
import sys
import tempfile
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest


def leaves(menu, chain=()):
    result = []
    for action in menu.actions():
        if action.menu():
            result.extend(leaves(action.menu(), chain + ((menu, action),)))
        elif action.isEnabled():
            result.append((menu, action, chain))
    return result


def choose(entry):
    menu, action, chain = entry
    for owner, parent_action in chain:
        owner.setActiveAction(parent_action)
        QtTest.QTest.keyClick(owner, QtCore.Qt.Key_Right)
        QtWidgets.QApplication.processEvents()
    menu.setActiveAction(action)
    QtTest.QTest.keyClick(menu, QtCore.Qt.Key_Return)


class FaceGate:
    def allow(self, doc, obj, sub):
        return sub.startswith("Face")


class ObjectGate:
    def allow(self, doc, obj, sub):
        return not sub


class RejectGate:
    def allow(self, doc, obj, sub):
        return False


class TestClarifySelection(unittest.TestCase):
    def setUp(self):
        self.prefs = App.ParamGet("User parameter:BaseApp/Preferences/Document")
        self.duplicate = self.prefs.GetBool("DuplicateLabels", False)
        self.prefs.SetBool("DuplicateLabels", True)
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("ClarifyTest")
        self.doc.UndoMode = 1
        self.front = self.doc.addObject("Part::Box", "Front")
        self.rear = self.doc.addObject("Part::Box", "Rear")
        self.front.Placement.Base.z = 12
        self.front.Label = self.rear.Label = "Repeated bracket"
        self.assertEqual(self.front.Label, self.rear.Label)
        self.doc.recompute()
        Gui.Selection.clearSelection()
        self.window = Gui.getMainWindow()
        self.window.resize(1200, 800)
        self.window.move(0, 0)
        self.view = Gui.activeDocument().activeView()
        self.view.viewTop()
        self.view.fitAll()
        Gui.updateGui()
        self.cursor = QtGui.QCursor.pos()

    def tearDown(self):
        Gui.Selection.removeSelectionGate()
        Gui.Selection.clearSelection()
        Gui.Selection.clearPreselection()
        QtGui.QCursor.setPos(self.cursor)
        self.prefs.SetBool("DuplicateLabels", self.duplicate)
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def menu(self, callback):
        Gui.updateGui()
        candidates = [w for w in self.window.findChildren(QtWidgets.QWidget)
                      if "GL" in w.metaObject().className() and w.width() > 100 and w.height() > 100]
        self.assertTrue(candidates, "No native OpenGL viewport widget")
        widget = max(candidates, key=lambda w: w.width() * w.height())
        x, y = self.view.getPointOnScreen(App.Vector(5, 5, 5))
        self.assertTrue(self.view.getObjectsInfo((x, y)), "Fixture is not under the pick ray")
        ratio = widget.devicePixelRatioF()
        position = widget.mapToGlobal(QtCore.QPoint(round(x / ratio), widget.height() - round(y / ratio) - 1))
        QtGui.QCursor.setPos(position)
        errors, ran = [], []
        def drive():
            menu = self.window.findChild(QtWidgets.QMenu, "ClarifySelectionMenu")
            if menu is None:
                errors.append(AssertionError("Native Clarify Selection menu did not open"))
                return
            ran.append(True)
            try:
                callback(menu)
            except BaseException:
                errors.append(sys.exc_info()[1])
            finally:
                menu.close()
        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(drive)
        timer.start(50)
        Gui.runCommand("Std_ClarifySelection")
        timer.stop()
        self.assertTrue(ran, "Native command produced no menu at the fixture ray")
        if errors:
            raise errors[0]

    def rows(self, menu, category):
        action = next((a for a in menu.actions() if a.text() == category), None)
        return leaves(action.menu(), ((menu, action),)) if action else []

    def testSameLabelsKeepBothObjectsAndExactHover(self):
        def check(menu):
            rows = self.rows(menu, "Face")
            tips = [a.toolTip() for _, a, _ in rows]
            self.assertTrue(any("#Front.Face" in t for t in tips), tips)
            self.assertTrue(any("#Rear.Face" in t for t in tips), tips)
            self.assertEqual(len(tips), len(set(tips)))
            entry = next(row for row in rows if "#Rear.Face" in row[1].toolTip())
            entry[1].hover()
            pre = Gui.Selection.getPreselection()
            self.assertEqual(pre.ObjectName, "Rear")
            self.assertEqual(pre.SubElementNames[0], entry[1].toolTip().split("#Rear.")[1])
            self.assertTrue(any("#Rear." in row[1].text() for row in self.rows(menu, "Object")))
        self.menu(check)
        self.assertFalse(Gui.Selection.getSelection())
        self.assertFalse(Gui.Selection.getPreselection().ObjectName)

    def testAcceptRearFaceAddsWithoutChangingExistingSelection(self):
        Gui.Selection.addSelection(self.front)
        expected = []
        def select(menu):
            row = next(row for row in self.rows(menu, "Face") if "#Rear.Face" in row[1].toolTip())
            expected.append(row[1].toolTip().split("#Rear.")[1])
            choose(row)
        self.menu(select)
        result = Gui.Selection.getSelectionEx("*", 0)
        self.assertEqual({r.ObjectName for r in result}, {"Front", "Rear"})
        self.assertEqual(next(r for r in result if r.ObjectName == "Rear").SubElementNames, tuple(expected))

    def testEscapeKeepsPriorSelectionAndModel(self):
        Gui.Selection.addSelection(self.front, "Face1")
        before = self.front.Shape.exportBrepToString(), self.rear.Shape.exportBrepToString(), self.doc.UndoCount
        def cancel(menu):
            row = self.rows(menu, "Face")[0]
            row[1].hover()
            QtTest.QTest.keyClick(menu, QtCore.Qt.Key_Escape)
        self.menu(cancel)
        selected = Gui.Selection.getSelectionEx("*", 0)
        self.assertEqual([(s.ObjectName, s.SubElementNames) for s in selected], [("Front", ("Face1",))])
        self.assertEqual(before, (self.front.Shape.exportBrepToString(), self.rear.Shape.exportBrepToString(), self.doc.UndoCount))

    def testFaceAndWholeObjectGates(self):
        Gui.Selection.addSelectionGate(FaceGate())
        def faces(menu):
            self.assertTrue(self.rows(menu, "Face"))
            self.assertEqual([a.text() for a in menu.actions()], ["Face"])
        self.menu(faces)
        Gui.Selection.addSelectionGate(ObjectGate())
        def objects(menu):
            self.assertEqual([a.text() for a in menu.actions()], ["Object"])
            rows = self.rows(menu, "Object")
            self.assertEqual(len(rows), 2)
            choose(next(row for row in rows if "#Rear." in row[1].toolTip()))
        self.menu(objects)
        selected = Gui.Selection.getSelectionEx("*", 0)
        self.assertEqual([(s.ObjectName, s.SubElementNames) for s in selected], [("Rear", ())])

    def testEmptyFilterAndChangedGate(self):
        Gui.Selection.addSelectionGate(RejectGate())
        def empty(menu):
            self.assertEqual(len(menu.actions()), 1)
            self.assertFalse(menu.actions()[0].isEnabled())
            self.assertIn("selection filter", menu.actions()[0].text())
        self.menu(empty)
        Gui.Selection.removeSelectionGate()
        def changed(menu):
            row = self.rows(menu, "Face")[0]
            Gui.Selection.addSelectionGate(RejectGate())
            row[1].hover()
            self.assertFalse(Gui.Selection.getPreselection().ObjectName)
            choose(row)
        self.menu(changed)
        self.assertFalse(Gui.Selection.getSelection())

    def testDeletedCandidateCannotSelectReplacementWithSameName(self):
        def deleted(menu):
            row = next(row for row in self.rows(menu, "Object") if "#Rear." in row[1].toolTip())
            self.doc.removeObject("Rear")
            replacement = self.doc.addObject("Part::Box", "Rear")
            self.doc.recompute()
            self.assertEqual(replacement.Name, "Rear")
            row[1].hover()
            self.assertFalse(Gui.Selection.getPreselection().ObjectName)
            choose(row)
        self.menu(deleted)
        self.assertFalse(Gui.Selection.getSelection())

    def testRepeatedNestedLinksRetainWholeOccurrencePaths(self):
        self.front.ViewObject.Visibility = self.rear.ViewObject.Visibility = False
        assembly = self.doc.addObject("App::Part", "Assembly")
        first = assembly.newObject("App::Link", "First")
        second = assembly.newObject("App::Link", "Second")
        first.setLink(self.rear)
        second.setLink(self.rear)
        first.Label = second.Label = "Repeated bracket"
        first.LinkPlacement.Base.z = 12
        self.doc.recompute()
        self.view.fitAll()
        def check(menu):
            rows = self.rows(menu, "Object")
            tips = [a.toolTip() for _, a, _ in rows]
            self.assertTrue(any("First." in t for t in tips), tips)
            self.assertTrue(any("Second." in t for t in tips), tips)
            self.assertEqual(len(tips), len(set(tips)))
            row = next(row for row in rows if "Second." in row[1].toolTip())
            row[1].hover()
            pre = Gui.Selection.getPreselection()
            self.assertIn("Second", pre.ObjectName + "." + ".".join(pre.SubElementNames))
            choose(row)
        self.menu(check)
        selected = Gui.Selection.getSelectionEx("*", 0)
        self.assertEqual(len(selected), 1)
        self.assertIn("Second", selected[0].ObjectName + "." + ".".join(selected[0].SubElementNames))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "Repeated.FCStd"
            self.doc.saveAs(str(path))
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(str(path))
            self.assertEqual(self.doc.First.LinkedObject, self.doc.Second.LinkedObject)
            self.assertEqual(self.doc.First.LinkPlacement.Base.z, 12)
