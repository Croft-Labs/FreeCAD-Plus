# SPDX-License-Identifier: LGPL-2.1-or-later
"""Datum-plane combinations, persistence and the actual shared task controls."""
import hashlib
import importlib
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
import ComponentPlane as Plane
import ComponentSketch as Sketch
from freecad.gui import ComponentPlaneTask as Task
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui.ComponentTaskWidgets import CurveCollector, ReferenceCollector
from PySide import QtCore, QtWidgets, QtGui
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest


class TestComponentPlaneTask(unittest.TestCase):
    def setUp(self):
        for module, folder in ((Plane, 'src/Mod/Part'), (Task, 'src/Gui'),
                               (importlib.import_module('freecad.gui.ComponentTaskWidgets'), 'src/Gui')):
            path = Path(module.__file__)
            self.assertEqual(hashlib.sha256(path.read_bytes()).digest(),
                             hashlib.sha256((Path(os.environ['FREECAD_PLUS_SOURCE']) / folder / path.name).read_bytes()).digest())
        Gui.activateWorkbench('PartDesignWorkbench')
        self.doc = Model.new_document('Datum plane acceptance')
        self.component = Model.metadata(self.doc).RootComponent
        self.origins = {obj.Role: obj for obj in self.component.Origin.OriginFeatures}
        self.box = self.doc.addObject('Part::Box', 'Box')
        Model.register_object(self.component, self.box)
        self.doc.recompute()
        self.output = Path(os.environ['FREECAD_PLUS_VALIDATION_DIR'])
        Gui.Selection.clearSelection()

    def tearDown(self):
        if Task._task:
            Task._task.reject()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def point(self, xyz):
        obj = self.doc.addObject('Part::Feature', 'Point')
        obj.Shape = Part.Vertex(App.Vector(*xyz))
        Model.register_object(self.component, obj)
        self.doc.recompute()
        return obj, 'Vertex1'

    def edge(self, a, b):
        obj = self.doc.addObject('Part::Feature', 'Line')
        obj.Shape = Part.makeLine(App.Vector(*a), App.Vector(*b))
        Model.register_object(self.component, obj)
        self.doc.recompute()
        return obj, 'Edge1'

    def values(self, refs):
        values = Plane.defaults()
        values['references'] = refs
        return values

    def near(self, a, b):
        self.assertLess((a - b).Length, 1e-6, (a, b))

    def testGeometryCombinationsAndInvalidStates(self):
        x = self.edge((0, 0, 4), (10, 0, 4))
        y = self.edge((0, 0, 4), (0, 10, 4))
        a, b, c = [self.point(p) for p in ((0, 0, 4), (10, 0, 4), (0, 10, 4))]
        for refs, z in (([(self.origins['XY_Plane'], '')], 0), ([(self.box, 'Face6')], 10),
                        ([x, y], 4), ([a, b, c], 4), ([x, c], 4),
                        ([(self.origins['X_Axis'], ''), self.edge((0, 1, 0), (0, 4, 0))], 0)):
            with self.subTest(refs=refs):
                placement = Plane.evaluate(self.component, self.values(refs))
                self.near(placement.Base, App.Vector(0, 0, z))
        for refs in ([], [x], [a, b]):
            with self.assertRaises(Plane.UnderDefined):
                Plane.evaluate(self.component, self.values(refs))
        for refs in ([x, self.edge((2, 0, 4), (4, 0, 4))],
                     [x, self.edge((0, 0, 5), (0, 10, 5))], [a, b, self.point((20, 0, 4))],
                     [(self.box, 'Face6'), x]):
            with self.assertRaises(ValueError):
                Plane.evaluate(self.component, self.values(refs))

    def testCurvedGeometryAndCrossComponentRejection(self):
        curve = self.doc.addObject('Part::Feature', 'Curve')
        curve.Shape = Part.makeCircle(4, App.Vector(0, 0, 3))
        Model.register_object(self.component, curve)
        self.doc.recompute()
        placement = Plane.evaluate(self.component, self.values([(curve, 'Edge1'), self.point((0, 0, 3))]))
        self.near(placement.Base, App.Vector(0, 0, 3))
        with self.assertRaises(ValueError):
            Plane.evaluate(self.component, self.values([(curve, 'Edge1'), self.point((0, 0, 8))]))
        other = Model.new_document('Other plane source')
        root = Model.metadata(other).RootComponent
        with self.assertRaises(ValueError):
            Plane.geometry(self.component, (root.Origin.OriginFeatures[0], ''))

    def testOffsetReversalProjectedOriginAndAxis(self):
        values = self.values([(self.box, 'Face6')])
        values.update(offset=3., axis=[(self.origins['Y_Axis'], '')], origin=self.point((2, 7, 30)))
        frame = Plane.evaluate(self.component, values)
        self.near(frame.Base, App.Vector(2, 7, 13))
        self.near(frame.Rotation.multVec(App.Vector(1, 0, 0)), App.Vector(0, 1, 0))
        values.update(reverse_normal=True, reverse_axis=True)
        frame = Plane.evaluate(self.component, values)
        self.near(frame.Base, App.Vector(2, 7, 7))
        self.near(frame.Rotation.multVec(App.Vector(1, 0, 0)), App.Vector(0, -1, 0))
        self.near(frame.Rotation.multVec(App.Vector(0, 0, 1)), App.Vector(0, 0, -1))
        values['axis'] = [self.point((0, 0, 0)), self.point((0, 2, 1))]
        Plane.evaluate(self.component, values)
        values['axis'] = [(self.origins['Z_Axis'], '')]
        with self.assertRaises(ValueError):
            Plane.evaluate(self.component, values)

    def testAssociationEditUndoAndPersistence(self):
        values = self.values([(self.box, 'Face6')])
        plane = Plane.apply(self.component, values)
        identity = plane.ObjectId
        self.box.Height = 17
        self.doc.recompute()
        self.near(plane.Placement.Base, App.Vector(0, 0, 17))
        values['offset'] = 2.
        Plane.apply(self.component, values, plane)
        self.near(plane.Placement.Base, App.Vector(0, 0, 19))
        self.assertEqual(plane.ObjectId, identity)
        self.doc.undo()
        self.doc.recompute()
        self.near(plane.Placement.Base, App.Vector(0, 0, 17))
        self.doc.redo()
        self.doc.recompute()
        sketch = Sketch.create(self.component, 'User plane', support=plane)
        self.near(sketch.Placement.Base, plane.Placement.Base)
        path = self.output / 'DatumPlane.cadprt'
        self.doc.saveAs(str(path))
        name = plane.Name
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.component = Model.metadata(self.doc).RootComponent
        restored = self.doc.getObject(name)
        self.assertEqual(restored.ObjectId, identity)
        self.assertEqual(Plane.read(restored)['offset'], 2.)
        self.doc.getObject('Box').Height = 25
        self.doc.recompute()
        self.near(restored.Placement.Base, App.Vector(0, 0, 27))

    def testSharedCollectorsToggleDeleteAndFilters(self):
        task = Task.launch(self.component)
        self.assertIsInstance(task.plane_collector, CurveCollector)
        self.assertIsInstance(task.axis_collector, ReferenceCollector)
        self.assertEqual(task.mode.currentData(), 'Select geometry')
        self.assertIn('Under-defined', task.plane_collector.status.text())
        first = self.edge((0, 0, 5), (10, 0, 5))
        second = self.edge((0, 0, 5), (0, 10, 5))
        for obj, element in (first, second):
            Gui.Selection.addSelection(obj, element)
        self.assertEqual(len(task.plane_collector.references()), 2)
        self.assertEqual(task.plane_collector.status.text(), 'Defined')
        Gui.Selection.addSelection(*second)
        self.assertEqual(len(task.plane_collector.references()), 1)
        self.assertEqual(task.plane_collector.curves.currentRow(), -1)
        Gui.Selection.addSelection(*second)
        QtTest.QTest.keyClick(task.plane_collector.curves, QtCore.Qt.Key_Delete)
        self.assertEqual(len(task.plane_collector.references()), 1)
        task.activate('axis')
        Gui.Selection.addSelection(self.box, 'Face6')
        self.assertEqual(task.axis_collector.references(), [])
        Gui.Selection.addSelection(self.origins['X_Axis'])
        self.assertEqual(len(task.axis_collector.references()), 1)
        parent = task.origin_field.parentWidget()
        while parent and not isinstance(parent, QtWidgets.QScrollArea):
            parent = parent.parentWidget()
        parent.ensureWidgetVisible(task.origin_field)
        QtTest.QTest.mouseClick(task.origin_field, QtCore.Qt.LeftButton)
        Gui.updateGui()
        Gui.Selection.addSelection(self.box, 'Vertex1')
        self.assertEqual(task.origin_reference[0], self.box)
        QtTest.QTest.keyClick(task.origin_field, QtCore.Qt.Key_Delete)
        self.assertIsNone(task.origin_reference)

    def testNumericPreviewThemeAndNormalization(self):
        task = Task.launch(self.component)
        task.mode.setCurrentIndex(1)
        task.position[2].setProperty('rawValue', 8.)
        task.normal[2].setValue(5.)
        task.offset.setProperty('rawValue', 3.)
        task.reverse_offset.click()
        self.assertEqual(float(task.offset.property('rawValue')), -3.)
        count = len(self.doc.Objects)
        task.preview()
        self.assertIsNotNone(task.ghost, task.status.text())
        self.assertEqual(len(self.doc.Objects), count)
        self.assertEqual(task.form.styleSheet(), '')
        # Qt's application stylesheet can itself set WA_SetPalette while polishing.
        # Compare with an ordinary sibling, not a frozen main-window palette.
        inherited = QtWidgets.QWidget(task.form.parentWidget())
        inherited.ensurePolished()
        for role in (QtGui.QPalette.Window, QtGui.QPalette.WindowText, QtGui.QPalette.Base, QtGui.QPalette.Text):
            self.assertEqual(task.form.palette().color(role), inherited.palette().color(role))
        inherited.deleteLater()
        for actual, expected in zip(task.ghost.node.getChild(2).diffuseColor[0].getValue(), (.65, .25, .85)):
            self.assertAlmostEqual(actual, expected, places=5)
        task.preview_enabled.setChecked(False)
        self.assertIsNone(task.ghost)
        task.automatic.setChecked(False)
        task.preview_enabled.setChecked(True)
        self.assertIsNotNone(task.ghost)
        task.position[2].setProperty('rawValue', 9.)
        self.assertIsNone(task.ghost)
        task.preview()
        Gui.updateGui()
        Gui.getMainWindow().grab().save(str(self.output / 'plane-enter-values.png'))
        if not task.accept():
            self.fail(task.status.text())
        self.near(task.result.ProjectedFrame.Normal, App.Vector(0, 0, 1))
        self.near(task.result.Placement.Base, App.Vector(0, 0, 6))

    def testNativeCommandHistoryEditAndCancel(self):
        Gui.runCommand('PartDesign_Plane')
        task = Task._task
        self.assertIsNotNone(task)
        task.plane_collector.basic.menu().actions()[0].trigger()
        task.preview()
        if not task.accept():
            self.fail(task.status.text())
        plane = task.result
        before = tuple(plane.Placement.toMatrix().A)
        panel = Navigator.show(self.doc)
        panel.edit_history(Navigator.object_key(plane))
        task = Task._task
        self.assertIs(task.operation, plane)
        task.offset.setProperty('rawValue', 30.)
        task.preview()
        task.reject()
        self.assertEqual(tuple(plane.Placement.toMatrix().A), before)
        self.assertFalse(task.highlights)
        self.assertIsNone(task.ghost)

    def testOriginVisibilityAndDoubleScaleRestoration(self):
        from pivy import coin
        def scale(obj):
            action = coin.SoSearchAction()
            action.setType(coin.SoType.fromName('SoShapeScale'))
            action.setSearchingAll(True)
            action.apply(obj.ViewObject.RootNode)
            self.assertIsNotNone(action.getPath())
            return action.getPath().getTail().getField('scaleFactor').getValue()
        Navigator.show(self.doc)
        Gui.updateGui()
        originals = {obj.Name: (obj.Visibility, scale(obj)) for obj in self.component.Origin.OriginFeatures}
        task = Task.launch(self.component)
        for obj in self.component.Origin.OriginFeatures:
            self.assertTrue(obj.Visibility)
            self.assertAlmostEqual(scale(obj), originals[obj.Name][1] * 2)
        task.reject()
        for obj in self.component.Origin.OriginFeatures:
            self.assertEqual(obj.Visibility, originals[obj.Name][0])
            self.assertAlmostEqual(scale(obj), originals[obj.Name][1])

    def testNarrowTaskAndBasicMenus(self):
        task = Task.launch(self.component)
        for index in (0, 1):
            task.mode.setCurrentIndex(index)
            parent = task.form
            scroll = dock = None
            while parent:
                if isinstance(parent, QtWidgets.QScrollArea): scroll = parent
                if isinstance(parent, QtWidgets.QDockWidget): dock = parent
                parent = parent.parentWidget()
            dock.setFloating(True)
            dock.resize(360, 600)
            Gui.updateGui()
            QtTest.QTest.qWait(150)
            self.assertLessEqual(dock.width(), 360)
            self.assertEqual(scroll.horizontalScrollBarPolicy(), QtCore.Qt.ScrollBarAlwaysOff)
            self.assertLessEqual(scroll.widget().width(), scroll.viewport().width())
            self.assertGreater(scroll.verticalScrollBar().maximum(), 0)
            scroll.verticalScrollBar().setValue(0)
            dock.grab().save(str(self.output / ('plane-narrow-' + str(index) + '.png')))
        self.assertEqual(len(task.plane_collector.basic.menu().actions()), 3)
        self.assertEqual(len(task.axis_collector.basic.menu().actions()), 3)
        task.axis_collector.basic.menu().actions()[1].trigger()
        self.assertEqual(task.pick_role, 'axis')
        self.assertEqual(task.axis_collector.curves.currentRow(), 0)

    def testLegacyFrameMigrationAndAtomicFailure(self):
        projected = Sketch.create_plane(self.component, 'XY plane', offset=7.,
                                        frame={'reverse_z': True})
        migrated = Plane.evaluate(self.component, Plane.read(projected), projected)
        self.near(migrated.Base, projected.Placement.Base)
        self.near(migrated.Rotation.multVec(App.Vector(0, 0, 1)),
                  projected.Placement.Rotation.multVec(App.Vector(0, 0, 1)))
        old = Sketch.create_plane(self.component, 'XY plane', angles=(20., 30., 40.))
        before = old.Placement
        identity = old.ObjectId
        Plane.apply(self.component, Plane.read(old), old)
        self.assertEqual(old.ObjectId, identity)
        self.near(old.Placement.Base, before.Base)
        for vector in (App.Vector(1, 0, 0), App.Vector(0, 0, 1)):
            self.near(old.Placement.Rotation.multVec(vector), before.Rotation.multVec(vector))
        values = Plane.read(old)
        values['normal'] = (0., 0., 0.)
        names = [obj.Name for obj in self.doc.Objects]
        with self.assertRaises(ValueError):
            Plane.apply(self.component, values, old)
        self.assertEqual([obj.Name for obj in self.doc.Objects], names)
        self.assertFalse(self.doc.HasPendingTransaction)
        helper_name = old.ProjectedFrame.Name
        with Model.transaction(self.doc, 'Delete plane'):
            self.doc.removeObject(old.Name)
        self.assertIsNone(self.doc.getObject(helper_name))

    def testOriginPlaneNormalsAndReadablePopup(self):
        for role, normal in (('XY_Plane', (0, 0, 1)), ('YZ_Plane', (1, 0, 0)), ('XZ_Plane', (0, -1, 0))):
            frame = Plane.evaluate(self.component, self.values([(self.origins[role], '')]))
            self.near(frame.Rotation.multVec(App.Vector(0, 0, 1)), App.Vector(*normal))
        task = Task.launch(self.component)
        task.plane_collector.basic.menu().actions()[0].trigger()
        task.preview()
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()
        Gui.updateGui()
        task.mode.showPopup()
        QtTest.QTest.qWait(100)
        palette = task.mode.view().palette()
        self.assertGreater(abs(palette.color(QtGui.QPalette.Base).lightness() -
                               palette.color(QtGui.QPalette.Text).lightness()), 100)
        Gui.getMainWindow().grab().save(str(self.output / 'plane-preview-light.png'))
        task.mode.view().window().grab().save(str(self.output / 'plane-dropdown-light.png'))
        task.mode.hidePopup()

    def testViewportFaceToggleAndThemeChanges(self):
        from freecad.gui import PlusRibbon
        # Avoid overlapping the separately pickable origin planes in this probe.
        self.box.Placement.Base = App.Vector(40, 40, 0)
        self.doc.recompute()
        task = Task.launch(self.component)
        view = Gui.activeDocument().activeView()
        view.viewTop()
        view.fitAll()
        Gui.updateGui()
        viewport = max((w for w in Gui.getMainWindow().findChildren(QtWidgets.QWidget)
                        if 'GL' in w.metaObject().className() and w.width() > 100 and w.height() > 100),
                       key=lambda w: w.width() * w.height())
        for expected in ([(self.box, 'Face6')], []):
            sx, sy = view.getPointOnScreen(App.Vector(45, 45, 10))
            ratio = viewport.devicePixelRatioF()
            pos = QtCore.QPoint(round(sx / ratio), viewport.height() - round(sy / ratio) - 1)
            QtWidgets.QApplication.sendEvent(viewport, QtGui.QMouseEvent(
                QtCore.QEvent.MouseMove, QtCore.QPointF(pos), QtCore.QPointF(viewport.mapToGlobal(pos)),
                QtCore.Qt.NoButton, QtCore.Qt.NoButton, QtCore.Qt.NoModifier))
            QtTest.QTest.mouseClick(viewport, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, pos)
            Gui.updateGui()
            self.assertEqual(task.plane_collector.references(), expected, task.status.text())
        window = Gui.getMainWindow()
        original = window.palette()
        try:
            palette = QtGui.QPalette(original)
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#353535'))
            palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor('#f0f0f0'))
            window.setPalette(palette)
            QtTest.QTest.qWait(100)
            page = PlusRibbon._ribbon.scroll.widget()
            self.assertIn('#353535', page.styleSheet())
        finally:
            window.setPalette(original)
            QtTest.QTest.qWait(100)
        self.assertIn(original.color(QtGui.QPalette.Window).name(), PlusRibbon._ribbon.scroll.widget().styleSheet())
