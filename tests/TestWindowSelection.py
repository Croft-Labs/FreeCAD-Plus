# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native viewport box selection: enclosure, crossing, filtering and cancellation."""
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets
from freecad.gui import EntitySelectionFilter as Filters
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest


def settle():
    Gui.updateGui()
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(150, loop.quit)
    loop.exec_()


class TestWindowSelection(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("WindowSelection")
        self.doc.UndoMode = 1
        self.box = self.doc.addObject("Part::Box", "Box")
        self.far = self.doc.addObject("Part::Box", "Far")
        self.far.Placement.Base.x = 20
        self.hidden = self.doc.addObject("Part::Box", "Hidden")
        self.hidden.Visibility = False
        self.doc.recompute()
        Filters.set_mode(0)
        Gui.Selection.clearSelection()
        self.window = Gui.getMainWindow()
        self.window.resize(1400, 950)
        self.cursor = QtGui.QCursor.pos()
        self.view = Gui.activeDocument().activeView()
        self.view.setCameraType("Orthographic")
        self.view.viewTop()
        self.view.fitAll()
        settle()
        widgets = [w for w in self.window.findChildren(QtWidgets.QWidget)
                   if "GL" in w.metaObject().className() and w.width() > 100 and w.height() > 100]
        self.viewport = max(widgets, key=lambda w: w.width() * w.height())
        self.original = self.box.Shape.exportBrepToString()
        self.undo = self.doc.UndoCount

    def tearDown(self):
        QtTest.QTest.keyClick(self.viewport, QtCore.Qt.Key_Escape)
        Filters.set_mode(0)
        Gui.Selection.removeSelectionGate()
        Gui.Selection.clearSelection()
        QtGui.QCursor.setPos(self.cursor)
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        settle()
        QtWidgets.QApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)

    def point(self, xy):
        sx, sy = self.view.getPointOnScreen(App.Vector(xy[0], xy[1], 0))
        ratio = self.viewport.devicePixelRatioF()
        return QtCore.QPoint(round(sx / ratio), self.viewport.height() - round(sy / ratio) - 1)

    def drag(self, start, end, element=False, ctrl=False, release=True, command=True):
        if command:
            Gui.runCommand("Std_BoxElementSelection" if element else "Std_BoxSelection")
            settle()
        mods = QtCore.Qt.ControlModifier if ctrl else QtCore.Qt.NoModifier
        a, b = self.point(start), self.point(end)
        QtTest.QTest.mousePress(self.viewport, QtCore.Qt.LeftButton, mods, a)
        settle()
        event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(b),
                                 QtCore.QPointF(self.viewport.mapToGlobal(b)),
                                 QtCore.Qt.NoButton, QtCore.Qt.LeftButton, mods)
        QtWidgets.QApplication.sendEvent(self.viewport, event)
        settle()
        if release:
            QtTest.QTest.mouseRelease(self.viewport, QtCore.Qt.LeftButton, mods, b)
            settle()

    def names(self):
        return {o.Name for o in Gui.Selection.getSelection()}

    def testPartialCenterIsExcludedOnlyByWindowAtTwoZooms(self):
        for factor in (1., 1.7):
            camera = self.view.getCameraNode()
            camera.height.setValue(camera.height.getValue() * factor)
            settle()
            self.drag((2, 2), (8, 8))
            self.assertFalse(self.names())
            self.drag((8, 8), (2, 2))
            self.assertEqual(self.names(), {"Box"})
        self.assertEqual(self.box.Shape.exportBrepToString(), self.original)
        self.assertEqual(self.doc.UndoCount, self.undo)

    def testFullEnclosureHiddenAndOffscreenObjects(self):
        self.drag((-1, -1), (11, 11))
        self.assertEqual(self.names(), {"Box"})
        self.drag((31, 11), (19, -1))
        self.assertEqual(self.names(), {"Far"})

    def testCommandGateDoesNotBypassRectangle(self):
        class AllowBoxes:
            def allow(self, doc, obj, sub):
                return obj.TypeId == "Part::Box" and not sub
        Gui.Selection.addSelectionGate(AllowBoxes())
        self.drag((8, 8), (2, 2))
        self.assertEqual(self.names(), {"Box"})
        self.drag((2, 2), (8, 8))
        self.assertFalse(self.names())

    def testCtrlAddsPlainReplacesAndEscapePreserves(self):
        Gui.Selection.addSelection(self.far)
        self.drag((-1, -1), (11, 11), ctrl=True)
        self.assertEqual(self.names(), {"Box", "Far"})
        self.drag((-1, -1), (11, 11))
        self.assertEqual(self.names(), {"Box"})
        self.drag((19, -1), (31, 11), release=False)
        QtTest.QTest.keyClick(self.viewport, QtCore.Qt.Key_Escape)
        settle()
        self.assertEqual(self.names(), {"Box"})
        self.drag((19, -1), (31, 11))
        self.assertEqual(self.names(), {"Far"})

    def testElementFilterCollectsEdgesInsteadOfWholeObject(self):
        Filters.set_mode(2)
        self.drag((-1, -1), (11, 11), element=True)
        selected = Gui.Selection.getSelectionEx("*", 0)
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].Object, self.box)
        self.assertTrue(selected[0].SubElementNames)
        self.assertTrue(all(n.startswith("Edge") for n in selected[0].SubElementNames))

    def testFaceFilterAndCommandGateIntersect(self):
        class OneFace:
            def allow(self, doc, obj, sub):
                return obj.Name == "Box" and sub == "Face6"
        Filters.set_mode(3)
        Gui.Selection.addSelectionGate(OneFace())
        self.drag((-1, -1), (11, 11), element=True)
        selected = Gui.Selection.getSelectionEx("*", 0)
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].SubElementNames, ("Face6",))
        self.drag((2, 2), (8, 8), element=True)
        self.assertFalse(self.names())

    def testNestedOccurrenceBoundsAndIdentity(self):
        group = self.doc.addObject("App::Part", "Assembly")
        link = self.doc.addObject("App::Link", "Occurrence")
        link.setLink(self.box)
        group.addObject(link)
        group.Placement.Base.y = 20
        self.doc.recompute()
        self.view.fitAll()
        settle()
        # Native aggregate selection changes a BRep ownership flag. Assert the
        # engineering geometry and document state, not serialized flag equality.
        def source_state():
            shape = self.box.Shape
            return (shape.Volume, shape.Area,
                    tuple(tuple(v.Point) for v in shape.Vertexes),
                    str(self.box.Placement), self.doc.UndoCount, tuple(self.box.State))
        before_selection = source_state()
        self.drag((-1, 19), (11, 31))
        selected = Gui.Selection.getSelectionEx("*", 0)
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].Object, group)
        self.assertEqual(link.LinkedObject, self.box)
        self.assertEqual(source_state(), before_selection)

    def testDelayedDragUsesSameEnclosureAndCrossingRules(self):
        self.view.setNavigationType("Gui::CADNavigationStyle")
        self.drag((2, -1), (8, 11), command=False)
        self.assertFalse(self.names())
        self.drag((8, 11), (2, -1), command=False)
        self.assertEqual(self.names(), {"Box"})

    def testBoxZoomRetainsCameraOnlyBehavior(self):
        Gui.Selection.addSelection(self.far)
        height = self.view.getCameraNode().height.getValue()
        Gui.runCommand("Std_ViewBoxZoom")
        settle()
        self.drag((-1, -1), (11, 11), command=False)
        self.assertLess(self.view.getCameraNode().height.getValue(), height)
        self.assertEqual(self.names(), {"Far"})
        self.assertEqual(self.doc.UndoCount, self.undo)
