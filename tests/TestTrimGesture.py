# SPDX-License-Identifier: LGPL-2.1-or-later
"""Drive native sketch Trim gestures through viewport mouse events."""
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
from PySide import QtCore, QtGui, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest


def settle(ms=150):
    Gui.updateGui()
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(ms, loop.quit)
    loop.exec_()


class TestTrimGesture(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("SketcherWorkbench")
        self.doc = App.newDocument("TrimGestureTest")
        self.doc.UndoMode = 1
        self.sketch = self.doc.addObject("Sketcher::SketchObject", "Profile")
        for x in (-8, 0, 8):
            self.sketch.addGeometry(Part.LineSegment(App.Vector(x, -10, 0), App.Vector(x, 10, 0)))
        for y in (-5, 5):
            self.sketch.addGeometry(Part.LineSegment(App.Vector(-12, y, 0), App.Vector(12, y, 0)))
        self.sketch.addConstraint(Sketcher.Constraint("Distance", 0, 20.0))
        self.sketch.renameConstraint(0, "LeftLength")
        self.doc.recompute()
        self.before = self.geometry()
        self.window = Gui.getMainWindow()
        self.window.resize(1400, 950)
        self.cursor = QtGui.QCursor.pos()
        self.prefs = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Sketcher")
        self.continuous = self.prefs.GetBool("ContinuousCreationMode", True)
        self.prefs.SetBool("ContinuousCreationMode", True)
        Gui.activeDocument().setEdit(self.sketch.Name)
        settle()
        self.view = Gui.activeDocument().activeView()
        self.view.viewTop()
        self.view.fitAll()
        settle()
        widgets = [w for w in self.window.findChildren(QtWidgets.QWidget)
                   if "GL" in w.metaObject().className() and w.width() > 100 and w.height() > 100]
        self.viewport = max(widgets, key=lambda w: w.width() * w.height())
        Gui.runCommand("Sketcher_Trimming")
        settle()
        self.undo_before = self.doc.UndoCount

    def tearDown(self):
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        self.prefs.SetBool("ContinuousCreationMode", self.continuous)
        QtGui.QCursor.setPos(self.cursor)
        settle()
        QtWidgets.QApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)

    def geometry(self):
        return [g.toShape().exportBrepToString() for g in self.sketch.Geometry]

    def point(self, x, y=2):
        sx, sy = self.view.getPointOnScreen(App.Vector(x, y, 0))
        ratio = self.viewport.devicePixelRatioF()
        return QtCore.QPoint(round(sx / ratio), self.viewport.height() - round(sy / ratio) - 1)

    def move(self, x, y=2, held=False):
        pos = self.point(x, y)
        event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(pos),
                                 QtCore.QPointF(self.viewport.mapToGlobal(pos)),
                                 QtCore.Qt.NoButton,
                                 QtCore.Qt.LeftButton if held else QtCore.Qt.NoButton,
                                 QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(self.viewport, event)
        settle()
        return pos

    def stroke(self, xs=(-8, 0, 8), release=True):
        start = self.move(xs[0])
        QtTest.QTest.mousePress(self.viewport, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, start)
        settle()
        for x in xs[1:]:
            self.move(x, held=True)
        if release:
            QtTest.QTest.mouseRelease(self.viewport, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                      self.point(xs[-1]))
            settle()

    def notice(self):
        return "\n".join(w.text() for w in self.window.findChildren(QtWidgets.QLabel)
                         if w.isVisible() and ("Trimmed" in w.text() or "Trimming gesture" in w.text()))

    def test_drag_is_one_undo_step_and_redo_restores_result(self):
        self.stroke()
        self.assertNotEqual(self.before, self.geometry())
        self.assertEqual(self.sketch.GeometryCount, 8)
        self.assertEqual(self.doc.UndoCount, self.undo_before + 1)
        self.assertIn("Trimmed 3", self.notice())
        after = self.geometry()
        self.doc.undo()
        self.doc.recompute()
        settle()
        self.assertEqual(self.before, self.geometry())
        self.doc.redo()
        self.doc.recompute()
        settle()
        self.assertEqual(after, self.geometry())

    def test_escape_rolls_back_only_in_progress_gesture(self):
        self.stroke((-8,))
        completed = self.geometry()
        undo = self.doc.UndoCount
        self.stroke((0, 8), release=False)
        self.assertNotEqual(completed, self.geometry())
        QtTest.QTest.keyClick(self.viewport, QtCore.Qt.Key_Escape)
        settle()
        self.doc.recompute()
        self.assertEqual(completed, self.geometry())
        self.assertEqual(undo, self.doc.UndoCount)

    def test_click_does_not_trim_a_second_edge_on_release(self):
        self.stroke((-8,))
        self.assertEqual(self.sketch.GeometryCount, 6)
        self.assertEqual(self.doc.UndoCount, self.undo_before + 1)
        self.assertIn("Trimmed 1", self.notice())
        self.assertIn("LeftLength", self.notice())
        self.assertIn("removed or replaced", self.notice())
        # Native trim may retain the name on a new constraint identity.
        self.assertTrue(any(c.Name == "LeftLength" for c in self.sketch.Constraints))
        labels = [w for w in self.window.findChildren(QtWidgets.QLabel, "notice") if w.isVisible()]
        self.assertTrue(labels)
        self.assertTrue(all(w.wordWrap() for w in labels))

    def test_empty_drag_creates_no_undo_entry(self):
        self.stroke((-16, -15, -14))
        self.assertEqual(self.before, self.geometry())
        self.assertEqual(self.doc.UndoCount, self.undo_before)

    def test_leaving_edit_cancels_unfinished_drag(self):
        self.stroke((-8, 0), release=False)
        self.assertNotEqual(self.before, self.geometry())
        Gui.activeDocument().resetEdit()
        self.doc.recompute()
        self.assertEqual(self.before, self.geometry())
