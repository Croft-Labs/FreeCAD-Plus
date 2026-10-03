# SPDX-License-Identifier: LGPL-2.1-or-later
"""Dependency-clamped History ordering, native drag/drop and persistence."""
import hashlib
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentExtrude as Extrude
from freecad.gui import ComponentNavigator as Navigator
from PySide import QtCore, QtGui, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest


class TestComponentHistoryMove(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, relative in ((Model, "src/Mod/Part/ComponentModel.py"),
                                 (Navigator, "src/Gui/ComponentNavigator.py")):
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((source / relative).read_bytes()).digest())
        self.doc = Model.new_document("History ordering")
        self.component = Model.metadata(self.doc).RootComponent
        self.a = self.feature("A")
        self.x = self.feature("X")
        self.b = self.feature("B", self.a)
        self.y = self.feature("Y")
        self.c = self.feature("C", self.b)
        self.z = self.feature("Z")
        self.original = list(self.component.ModelHistory)
        self.panel = Navigator.show(self.doc)
        self.panel.tabs.setCurrentWidget(self.panel.history)
        self.panel.setFloating(True)
        self.panel.resize(700, 600)
        self.panel.show()
        self.settle()

    def tearDown(self):
        Gui.Selection.clearSelection()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        self.settle()

    @staticmethod
    def settle():
        Gui.updateGui()
        QtTest.QTest.qWait(150)

    def feature(self, name, source=None):
        obj = self.doc.addObject("Part::Feature", name)
        obj.Shape = Part.makeBox(2, 3, 4)
        if source:
            obj.addProperty("App::PropertyLink", "Input")
            obj.Input = source
        Model.register_object(self.component, obj)
        self.doc.recompute()
        return obj

    def names(self, *objects):
        return [obj.Name for obj in objects]

    def row(self, obj):
        return next(self.panel.history.topLevelItem(i) for i in range(self.panel.history.topLevelItemCount())
                    if self.panel.history.topLevelItem(i).data(0, QtCore.Qt.UserRole) == Navigator.object_key(obj))

    def assert_topological(self, order):
        objects = [self.doc.getObject(name) for name in order]
        for obj in objects:
            for dep in Model.geometry_dependencies(obj):
                if dep in objects:
                    self.assertLess(objects.index(dep), objects.index(obj), (dep.Name, obj.Name))

    def testNearestPredecessorAndDependentBounds(self):
        cases = [
            ([self.b], 0, (self.a, self.b, self.x, self.y, self.c, self.z)),
            ([self.c], 0, (self.a, self.x, self.b, self.c, self.y, self.z)),
            ([self.a], 6, (self.x, self.a, self.b, self.y, self.c, self.z)),
            ([self.b], 6, (self.a, self.x, self.y, self.b, self.c, self.z)),
            ([self.z], 0, (self.z, self.a, self.x, self.b, self.y, self.c)),
            ([self.x], 6, (self.a, self.b, self.y, self.c, self.z, self.x)),
        ]
        for items, index, expected in cases:
            with self.subTest(items=self.names(*items), index=index):
                planned = Model.history_move_order(self.component, items, index)
                self.assertEqual(planned, self.names(*expected))
                self.assert_topological(planned)
                self.assertEqual(list(self.component.ModelHistory), self.original)

    def testMultipleItemsKeepOrderAcrossInterveningDependencies(self):
        cases = [
            ([self.b, self.c], 0, (self.a, self.b, self.c, self.x, self.y, self.z)),
            ([self.a, self.c], 0, (self.a, self.x, self.b, self.c, self.y, self.z)),
            ([self.a, self.c], 6, (self.x, self.a, self.b, self.y, self.z, self.c)),
            ([self.z, self.x], 0, (self.x, self.z, self.a, self.b, self.y, self.c)),
        ]
        for items, index, expected in cases:
            planned = Model.history_move_order(self.component, items, index)
            self.assertEqual(planned, self.names(*expected))
            self.assert_topological(planned)

    def testAllSelectionsAndGapsPreserveDependencyAndStableOrder(self):
        original = [self.a, self.x, self.b, self.y, self.c, self.z]
        for mask in range(1, 1 << len(original)):
            selected = [obj for i, obj in enumerate(original) if mask & (1 << i)]
            for gap in range(len(original) + 1):
                planned = Model.history_move_order(self.component, selected, gap)
                self.assert_topological(planned)
                chosen = self.names(*selected)
                self.assertEqual([n for n in planned if n in chosen], chosen)
                self.assertEqual([n for n in planned if n not in chosen], [o.Name for o in original if o not in selected])

    def testUndoRedoAndSaveReopenPreserveGeometryAndOrigin(self):
        identity = {o.Name: (o.ObjectId, o.Shape.Volume) for o in Model.history(self.component)}
        result = Model.reorder_history(self.component, [self.z], 0)
        self.assertEqual(result[0], self.z.Name)
        self.doc.undo()
        self.assertEqual(list(self.component.ModelHistory), self.original)
        self.doc.redo()
        self.assertEqual(list(self.component.ModelHistory), result)
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "reordered-history.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.component = Model.metadata(self.doc).RootComponent
        self.panel.set_document(self.doc)
        self.settle()
        self.assertEqual(list(self.component.ModelHistory), result)
        for name, (identifier, volume) in identity.items():
            obj = self.doc.getObject(name)
            self.assertEqual(obj.ObjectId, identifier)
            self.assertAlmostEqual(obj.Shape.Volume, volume)
        self.assertEqual(self.panel.history.topLevelItem(0).data(0, QtCore.Qt.UserRole),
                         Navigator.object_key(self.component.Origin))
        Model.validate(self.doc)

    def testNativeProfileBinderAndBackgroundResultDependencies(self):
        sketch = Sketch.create(self.component)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 1))
        self.doc.recompute()
        operation, result = Extrude.create(self.component, sketch, 5, elements=["Edge1"])
        tail = self.feature("Tail", result)
        before = Model.history_move_order(self.component, [operation], 0)
        self.assertLess(before.index(sketch.Name), before.index(operation.Name))
        self.assertEqual(before.index(result.Name), before.index(operation.Name) + 1)
        after = Model.history_move_order(self.component, [operation], 100)
        self.assertLess(after.index(result.Name), after.index(tail.Name))
        self.assert_topological(after)
        Model.reorder_history(self.component, [operation], 100)
        self.assertAlmostEqual(result.Shape.Volume, 5 * 3.141592653589793)

    def testOriginsForeignItemsAndActiveEditCannotMove(self):
        for obj in [self.component.Origin] + list(self.component.Origin.OriginFeatures):
            with self.assertRaises(ValueError):
                Model.reorder_history(self.component, [obj], 3)
        child = Model.add_component(self.component)
        foreign = self.doc.addObject("Part::Feature", "Foreign")
        Model.register_object(child.LinkedObject, foreign)
        with self.assertRaises(ValueError):
            Model.reorder_history(self.component, [foreign], 0)
        self.doc.openTransaction("Busy")
        try:
            self.z.Label = "Busy edit"  # Native transactions become pending on their first change.
            with self.assertRaises(ValueError):
                Model.reorder_history(self.component, [self.z], 0)
        finally:
            self.doc.abortTransaction()
        self.assertEqual(list(self.component.ModelHistory), self.original)

    def drag(self, objects, target, below=False):
        self.panel.refresh()
        self.panel.history.clearSelection()
        for obj in objects:
            self.row(obj).setSelected(True)
        mime = self.panel.history_move_mime()
        rect = self.panel.history.visualItemRect(self.row(target))
        point = QtCore.QPoint(rect.center().x(), rect.bottom() - 1 if below else rect.top() + 1)
        for cls in (QtGui.QDragEnterEvent, QtGui.QDragMoveEvent):
            event = cls(point, QtCore.Qt.MoveAction, mime, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(self.panel.history.viewport(), event)
            self.assertTrue(event.isAccepted())
        self.assertTrue(self.panel.history_drop_indicator.isVisible())
        drop = QtGui.QDropEvent(QtCore.QPointF(point), QtCore.Qt.MoveAction, mime,
                               QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(self.panel.history.viewport(), drop)
        self.assertTrue(drop.isAccepted())
        self.settle()

    def testNativeDragDropClampsBothDirectionsAndPinsOrigin(self):
        self.drag([self.c], self.component.Origin)
        self.assertEqual(list(self.component.ModelHistory), self.names(self.a, self.x, self.b, self.c, self.y, self.z))
        self.drag([self.a], self.z, below=True)
        self.assertEqual(list(self.component.ModelHistory), self.names(self.x, self.a, self.b, self.c, self.y, self.z))
        self.drag([self.z], self.component.Origin)
        self.assertEqual(self.panel.history.topLevelItem(0), self.row(self.component.Origin))
        self.assertEqual(self.component.ModelHistory[0], self.z.Name)
        self.assertFalse(self.panel.history_drop_indicator.isVisible())
        self.panel.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "reordered-history.png"))

    def testDragThresholdAndOriginCannotStartGesture(self):
        tree = self.panel.history
        def gesture(obj):
            point = QtCore.QPoint(tree.header().sectionViewportPosition(2) + 18,
                                 tree.visualItemRect(self.row(obj)).center().y())
            QtTest.QTest.mousePress(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
            event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(point + QtCore.QPoint(25, 0)),
                                     QtCore.Qt.NoButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(tree.viewport(), event)
            QtTest.QTest.mouseRelease(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
        with patch.object(self.panel, "start_history_drag") as start:
            gesture(self.component.Origin)
            start.assert_not_called()
            gesture(self.x)
            start.assert_called_once()
        self.panel.history.clearSelection()
        self.row(self.component.Origin).setSelected(True)
        with self.assertRaises(ValueError):
            self.panel.history_move_mime()

    def testExpressionDependenciesConstrainOrder(self):
        for obj in (self.a, self.z):
            obj.addProperty("App::PropertyFloat", "DrivingValue")
        self.a.DrivingValue = 12.
        self.z.setExpression("DrivingValue", "<<" + self.a.Label + ">>.DrivingValue * 2")
        self.doc.recompute()
        planned = Model.reorder_history(self.component, [self.z], 0)
        self.assertEqual(planned[:2], self.names(self.a, self.z))
        self.assertAlmostEqual(self.z.DrivingValue, 24.)
        self.assert_topological(planned)

    def testStaleAndForeignDragPayloadsAreRejected(self):
        self.row(self.z).setSelected(True)
        mime = self.panel.history_move_mime()
        original = json.loads(bytes(mime.data(self.panel.HISTORY_MIME)))
        for field in ("id", "items"):
            payload = dict(original)
            payload[field] = "wrong-component" if field == "id" else [(self.z.Name, "stale-object")]
            mime.setData(self.panel.HISTORY_MIME, json.dumps(payload).encode("utf-8"))
            event = QtGui.QDragEnterEvent(QtCore.QPoint(100, 20), QtCore.Qt.MoveAction, mime,
                                          QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(self.panel.history.viewport(), event)
            self.assertFalse(event.isAccepted())
        self.assertEqual(list(self.component.ModelHistory), self.original)

    def testLongHistoryScrollsWhileDraggingAndStopsOnLeave(self):
        for i in range(25):
            self.feature("Extra" + str(i))
        self.panel.resize(500, 300)
        self.panel.refresh()
        self.settle()
        tree = self.panel.history
        tree.clearSelection()
        self.row(self.z).setSelected(True)
        mime = self.panel.history_move_mime()
        tree.verticalScrollBar().setValue(0)
        point = QtCore.QPoint(100, tree.viewport().height() - 4)
        event = QtGui.QDragEnterEvent(point, QtCore.Qt.MoveAction, mime,
                                      QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(tree.viewport(), event)
        self.assertTrue(event.isAccepted())
        QtTest.QTest.qWait(250)
        self.assertGreater(tree.verticalScrollBar().value(), 0)
        QtWidgets.QApplication.sendEvent(tree.viewport(), QtGui.QDragLeaveEvent())
        self.assertFalse(self.panel.history_scroll_timer.isActive())
        self.assertFalse(self.panel.history_drop_indicator.isVisible())
