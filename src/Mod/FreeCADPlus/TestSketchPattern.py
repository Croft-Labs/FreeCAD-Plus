# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native pattern acceptance; GUI cases require an isolated profile."""
import math
import os
from pathlib import Path
import unittest
import FreeCAD as App
import Part
import Sketcher
from freecad_plus import sketch_pattern as pattern


def extent(**values):
    result = dict(mode='One dimension', count=3, spacing='Pitch', value=10,
                  method='Axis or line', reference=(-1, 0))
    result.update(values)
    return result


def linear(**values):
    result = dict(pattern='Linear', directions='One direction', d1=extent())
    result.update(values)
    return result


def circular(**values):
    result = dict(pattern='Circular', directions='Angular', center=(-1, 1),
                  angular=extent(spacing='Total angle', value=360, count=4))
    result.update(values)
    return result


class TestPatternGeometry(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument('PatternTest')
        self.doc.UndoMode = 1
        self.s = self.doc.addObject('Sketcher::SketchObject', 'Sketch')

    def tearDown(self):
        if self.doc.Name in App.listDocuments(): App.closeDocument(self.doc.Name)

    def line(self):
        return self.s.addGeometry(Part.LineSegment(App.Vector(5, 3, 0), App.Vector(9, 3, 0)))

    def assertVector(self, actual, expected):
        self.assertLess((actual - App.Vector(*expected)).Length, 1e-5)

    def test_extent_counts_pitch_total_reverse_symmetric(self):
        self.assertEqual(pattern.extent_values(extent()), [0, 10, 20])
        self.assertEqual(pattern.extent_values(extent(spacing='Total distance', value=12)), [0, 6, 12])
        self.assertEqual(pattern.extent_values(extent(reverse=True)), [0, -10, -20])
        self.assertEqual(pattern.extent_values(extent(mode='Symmetric', count=5)), [-20, -10, 0, 10, 20])
        self.assertEqual(pattern.extent_values(extent(mode='Two dimensions', count2=2, value2=7)), [-7, 0, 10, 20])
        with self.assertRaises(ValueError): pattern.extent_values(extent(mode='Symmetric', count=4))

    def test_four_independent_linear_extents(self):
        self.line()
        options = linear(directions='Two directions',
                         d1=extent(mode='Two dimensions', count=3, count2=2, value2=7),
                         d2=extent(mode='Two dimensions', count=2, count2=3, value=6, value2=2, reference=(-2, 0)))
        copies = pattern.apply(self.s, [0], options)
        self.assertEqual(len(copies), 15)
        coordinates = {(round(g.StartPoint.x, 5), round(g.StartPoint.y, 5)) for g in self.s.Geometry}
        self.assertEqual(coordinates, {(5+x, 3+y) for x in (-7, 0, 10, 20) for y in (-4, -2, 0, 6)})

    def test_arbitrary_vector_and_two_points(self):
        self.line()
        p = pattern.transforms(self.s, linear(d1=extent(method='Vector', x=3, y=4, count=2, value=5)))
        self.assertVector(p[0][1], (3, 4, 0))
        p = pattern.transforms(self.s, linear(d1=extent(method='Two points', start=(0, 2), end=(0, 1), count=2)))
        self.assertVector(p[0][1], (-10, 0, 0))
        with self.assertRaises(ValueError): pattern.transforms(self.s, linear(directions='Two directions', d2=extent()))

    def test_circular_full_turn_and_angular_pitch(self):
        self.line()
        copies = pattern.apply(self.s, [0], circular())
        self.assertEqual(len(copies), 3)
        self.assertVector(self.s.Geometry[1].StartPoint, (-3, 5, 0))
        self.assertVector(self.s.Geometry[3].StartPoint, (3, -5, 0))
        self.assertEqual(pattern.extent_values(extent(spacing='Angular pitch', value=30), True), [0, 30, 60])
        self.assertEqual(len(pattern.extent_values(extent(spacing='Total angle', value=360, count=5, mode='Symmetric'), True)), 5)

    def test_circular_radial_grid_and_size(self):
        circle = self.s.addGeometry(Part.Circle(App.Vector(20, 0, 0), App.Vector(0, 0, 1), 2), True)
        opts = circular(directions='Angular + radial', radial=extent(reference=(circle, 0), count=3, value=5))
        copies = pattern.apply(self.s, [circle], opts)
        self.assertEqual(len(copies), 11)
        self.assertEqual({round(g.Center.Length) for g in self.s.Geometry}, {20, 25, 30})
        self.assertTrue(all(abs(g.Radius - 2) < 1e-7 for g in self.s.Geometry))
        self.assertTrue(all(self.s.getConstruction(i) for i in copies))

    def test_center_circle_and_invalid_inward_atomic(self):
        self.line()
        self.s.addGeometry(Part.Circle(App.Vector(2, 1, 0), App.Vector(0, 0, 1), 1))
        p = pattern.transforms(self.s, circular(center=(1, 0), angular=extent(spacing='Angular pitch', value=90, count=2)))
        self.assertVector(pattern.transformed(self.s.Geometry[0], p[0]).StartPoint, (0, 4, 0))
        before = self.s.GeometryCount
        with self.assertRaises(ValueError):
            pattern.apply(self.s, [0], circular(directions='Radial', radial=extent(reference=(0, 1), reverse=True)))
        self.assertEqual(self.s.GeometryCount, before)

    def test_constraints_original_construction_and_undo(self):
        self.line(); self.s.toggleConstruction(0)
        index = self.s.addConstraint(Sketcher.Constraint('Horizontal', 0))
        self.s.renameConstraint(index, 'OriginalHorizontal')
        original = self.s.Constraints[0].dumpContent()
        pattern.apply(self.s, [0], linear())
        self.assertEqual(self.s.Constraints[0].dumpContent(), original)
        self.assertEqual(self.s.ConstraintCount, 3)
        self.assertEqual(self.s.solve(), 0)
        self.doc.undo(); self.assertEqual(self.s.GeometryCount, 1)
        self.doc.redo(); self.assertEqual(self.s.GeometryCount, 3)

    def test_dimensioned_translation_tracks_source_without_fixing(self):
        self.line()
        before = self.s.FullyConstrained
        copies = pattern.apply(self.s, [0], linear(d1=extent(count=2)), True)
        self.assertEqual(self.s.solve(), 0)
        self.assertEqual(self.s.FullyConstrained, before)
        self.s.moveGeometry(0, 1, App.Vector(7, 6, 0), 0)
        self.assertEqual(self.s.solve(), 0)
        self.assertVector(self.s.Geometry[copies[0]].StartPoint - self.s.Geometry[0].StartPoint, (10, 0, 0))
        self.assertVector(self.s.Geometry[copies[0]].EndPoint - self.s.Geometry[0].EndPoint, (10, 0, 0))

    def test_dimensioned_rotation_tracks_source_and_radius(self):
        self.s.addGeometry(Part.Circle(App.Vector(20, 4, 0), App.Vector(0, 0, 1), 2))
        copies = pattern.apply(self.s, [0], circular(angular=extent(spacing='Angular pitch', value=90, count=2)), True)
        self.assertEqual(self.s.solve(), 0)
        self.assertFalse(self.s.FullyConstrained)
        self.s.moveGeometry(0, 3, App.Vector(23, 7, 0), 0)
        self.assertEqual(self.s.solve(), 0)
        original = self.s.Geometry[0].Center
        self.assertVector(self.s.Geometry[copies[0]].Center, (-original.y, original.x, 0))
        self.assertAlmostEqual(self.s.Geometry[0].Radius, self.s.Geometry[copies[0]].Radius)

    def test_dimensioned_angular_radial_and_save_reopen(self):
        self.line()
        options = circular(directions='Angular + radial',
                           angular=extent(spacing='Angular pitch', value=90, count=2),
                           radial=extent(reference=(0, 1), count=2, value=3))
        copies = pattern.apply(self.s, [0], options, True)
        self.assertEqual(len(copies), 3)
        self.assertEqual(self.s.solve(), 0)
        if 'PLUS_TEST_DIR' in os.environ:
            path = str(Path(os.environ['PLUS_TEST_DIR']) / 'pattern.FCStd')
            self.doc.recompute(); self.doc.saveAs(path)
            expected = self.s.GeometryCount
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path); self.s = self.doc.getObject('Sketch')
            self.assertEqual(self.s.solve(), 0)
            self.assertEqual(self.s.GeometryCount, expected)

    def test_arc_and_spline_dimensions(self):
        arc = Part.ArcOfCircle(Part.Circle(App.Vector(12, 5, 0), App.Vector(0, 0, 1), 3), 0, math.pi/2)
        self.s.addGeometry(arc)
        curve = Part.BSplineCurve()
        curve.interpolate([App.Vector(5, 2, 0), App.Vector(7, 8, 0), App.Vector(10, 4, 0)])
        self.s.addGeometry(curve)
        copies = pattern.apply(self.s, [0, 1], linear(d1=extent(count=2)), True)
        self.assertGreaterEqual(len(copies), 2)
        self.assertEqual(self.s.solve(), 0)

    def test_dimensioned_clockwise_half_turn_and_origin_endpoint(self):
        self.s.addGeometry(Part.LineSegment(App.Vector(0, 0, 0), App.Vector(9, 3, 0)))
        copies = pattern.apply(self.s, [0], circular(angular=extent(spacing='Angular pitch', value=90, count=4, reverse=True)), True)
        self.assertEqual(self.s.solve(), 0)
        self.assertEqual(self.s.DoF, 4)
        self.s.moveGeometry(0, 1, App.Vector(2, 1, 0), False)
        for index, angle in zip(copies, (-90, -180, -270)):
            rotation = App.Rotation(App.Vector(0, 0, 1), angle)
            self.assertVector(self.s.Geometry[index].StartPoint, tuple(rotation.multVec(self.s.Geometry[0].StartPoint)))

    def test_external_line_and_circle_references(self):
        base = self.doc.addObject('PartDesign::Feature', 'Reference')
        base.Shape = Part.makeCompound([Part.makeLine(App.Vector(2, 1, 0), App.Vector(5, 5, 0)),
                                        Part.makeCircle(3, App.Vector(20, 10, 0))])
        self.doc.recompute()
        self.s.addExternal(base.Name, 'Edge1'); self.s.addExternal(base.Name, 'Edge2')
        self.assertVector(pattern.direction(self.s, {'reference': (-3, 0)}), (.6, .8, 0))
        self.assertVector(pattern.point_reference(self.s, (-4, 0))[0], (20, 10, 0))

    def test_dimensioned_rectangle_and_fixed_source(self):
        points = [App.Vector(x, y, 0) for x, y in ((5, 3), (9, 3), (9, 7), (5, 7))]
        for i in range(4): self.s.addGeometry(Part.LineSegment(points[i], points[(i+1)%4]))
        for i in range(4):
            self.s.addConstraint(Sketcher.Constraint('Coincident', i, 2, (i+1)%4, 1))
            self.s.addConstraint(Sketcher.Constraint('Horizontal' if i%2 == 0 else 'Vertical', i))
        self.s.solve(); before = self.s.DoF
        pattern.apply(self.s, [0, 1, 2, 3], circular(angular=extent(count=2, spacing='Angular pitch', value=35)), True)
        self.assertEqual(self.s.solve(), 0); self.assertEqual(self.s.DoF, before)
        self.s.addConstraint(Sketcher.Constraint('DistanceX', 0, 1, 5.0))
        self.s.addConstraint(Sketcher.Constraint('DistanceY', 0, 1, 3.0))
        self.s.addConstraint(Sketcher.Constraint('Distance', 0, 4.0))
        self.s.addConstraint(Sketcher.Constraint('Distance', 1, 4.0))
        self.assertEqual(self.s.solve(), 0); self.assertEqual(self.s.DoF, 0)
        pattern.apply(self.s, [0, 1, 2, 3], linear(d1=extent(count=2)), True)
        self.assertEqual(self.s.solve(), 0); self.assertEqual(self.s.DoF, 0)

    def test_closed_patterns_support_downstream_extrusion(self):
        points = [App.Vector(x, y, 0) for x, y in ((5, 3), (9, 3), (9, 7), (5, 7))]
        for i in range(4): self.s.addGeometry(Part.LineSegment(points[i], points[(i+1)%4]))
        pattern.apply(self.s, [0, 1, 2, 3], linear(), True)
        face = Part.makeFace(self.s.Shape.Wires, 'Part::FaceMakerBullseye')
        solid = face.extrude(App.Vector(0, 0, 5))
        self.assertTrue(solid.isValid()); self.assertAlmostEqual(solid.Volume, 240)

    def test_reference_angle_preserves_source_freedom(self):
        self.line()
        index = self.s.addConstraint(Sketcher.Constraint('Angle', 0, 0.0))
        self.s.setDriving(index, False); self.s.solve(); before = self.s.DoF
        original = self.s.Constraints[index]
        pattern.apply(self.s, [0], circular(angular=extent(count=2, spacing='Angular pitch', value=45)), True)
        self.assertEqual(self.s.solve(), 0); self.assertEqual(self.s.DoF, before)
        after = self.s.Constraints[index]
        self.assertEqual((after.Type,after.Driving,after.IsActive,after.First),
                         (original.Type,original.Driving,original.IsActive,original.First))
        self.assertAlmostEqual(after.Value,original.Value,places=10)

    def test_dimension_failure_rolls_back(self):
        self.s.addGeometry(Part.ArcOfHyperbola(Part.Hyperbola(), -1, 1))
        self.doc.recompute()
        before = self.s.Geometry[0].toShape().Length
        with self.assertRaisesRegex(ValueError, 'not supported'):
            pattern.apply(self.s, [0], linear(d1=extent(count=2)), True)
        self.assertEqual(self.s.GeometryCount, 1); self.assertEqual(self.s.ConstraintCount, 0)
        self.assertAlmostEqual(self.s.Geometry[0].toShape().Length, before)


class TestPatternTask(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ: self.skipTest('Requires isolated GUI profile')
        import FreeCADGui as Gui
        from PySide6 import QtWidgets, QtTest
        self.Gui, self.QtWidgets, self.QtTest = Gui, QtWidgets, QtTest
        self.doc = App.newDocument('PatternTaskTest'); self.doc.UndoMode = 1
        self.s = self.doc.addObject('Sketcher::SketchObject', 'Sketch')
        self.s.addGeometry(Part.LineSegment(App.Vector(5, 3, 0), App.Vector(9, 3, 0)))
        self.s.addGeometry(Part.Circle(App.Vector(20, 5, 0), App.Vector(0, 0, 1), 2))
        self.doc.recompute(); Gui.activateWorkbench('SketcherWorkbench')
        self.win = Gui.getMainWindow(); self.win.showNormal(); self.win.resize(1600, 1200)
        Gui.activeDocument().setEdit(self.s.Name); QtTest.QTest.qWait(100)
        self.sections = [(w, not w.isHidden()) for w in self.win.findChildren(QtWidgets.QWidget)
                         if w.metaObject().className().split('::')[-1] in
                         ('TaskSketcherMessages', 'TaskSketcherConstraints', 'TaskSketcherElements', 'TaskSketcherSolverAdvanced')]
        Gui.Selection.clearSelection()

    def tearDown(self):
        if self.Gui.activeDocument() and self.Gui.activeDocument().getInEdit(): self.Gui.activeDocument().resetEdit()
        App.closeDocument(self.doc.Name); self.QtTest.QTest.qWait(100)

    def enter(self):
        self.Gui.runCommand('Sketcher_Translate'); self.QtTest.QTest.qWait(200)
        self.p = self.win.findChild(self.QtWidgets.QWidget, 'SketchPatternPanel')
        self.assertIsNotNone(self.p)
        self.assertTrue(self.p.isVisible())
        self.assertTrue(self.p.lock.isChecked())

    def pick(self, field, name, remove=False):
        self.p.activate_pick(field)
        self.Gui.Selection.clearSelection()
        from freecad_plus.selection_list import pick_intent
        with pick_intent(remove): self.Gui.Selection.addSelection(self.s, name)
        self.QtTest.QTest.qWait(50)

    def test_task_picks_apply_undo_done(self):
        self.enter(); self.assertEqual(self.p.items.count(), 0)
        self.assertTrue(all(w.isHidden() for w, _ in self.sections))
        self.pick(self.p.items, 'Edge1'); self.pick(self.p.items, 'Edge1')
        self.assertEqual(self.p.items.count(), 1)
        self.pick(self.p.items, 'Edge1', True); self.assertEqual(self.p.items.count(), 0)
        self.pick(self.p.items, 'Edge1'); self.pick(self.p.d1.reference, 'H_Axis')
        self.p.d1.count.setValue(3); self.assertTrue(self.p.apply.isEnabled(), self.p.status.text())
        self.p.apply.click(); self.assertEqual(sum(not self.s.getConstruction(i) for i in range(self.s.GeometryCount)), 4, self.p.status.text())
        self.assertGreater(self.s.ConstraintCount, 0)
        self.assertEqual(self.p.items.count(), 0); self.assertTrue(self.p.d1.reference.text())
        self.doc.undo(); self.QtTest.QTest.qWait(100); self.assertEqual(self.s.GeometryCount, 2)
        self.doc.redo(); self.QtTest.QTest.qWait(100); self.assertEqual(sum(not self.s.getConstruction(i) for i in range(self.s.GeometryCount)), 4)
        self.p.done.click(); self.QtTest.QTest.qWait(100)
        self.assertTrue(all(not w.isHidden() == visible for w, visible in self.sections))
        self.assertIsNotNone(self.Gui.activeDocument().getInEdit())

    def test_radial_and_angular_reference_and_cancel(self):
        self.enter(); self.pick(self.p.items, 'Edge2')
        self.p.lock.setChecked(False)  # Users can still request unconstrained copies.
        self.p.mode.setCurrentText('Circular'); self.p.layout_mode.setCurrentText('Angular + radial')
        self.pick(self.p.center, 'RootPoint'); self.pick(self.p.radial.reference, 'Edge2')
        self.p.angular.count.setValue(4); self.p.angular.spacing.setCurrentText('Total angle'); self.p.angular.value.setValue(360)
        self.p.radial.count.setValue(2); self.p.radial.value.setValue(5)
        self.assertTrue(self.p.apply.isEnabled(), self.p.status.text())
        self.assertEqual(len(self.p.get_preview()), 7)
        self.win.findChild(self.QtWidgets.QDockWidget, 'Tasks').grab().save(str(Path(os.environ['PLUS_TEST_DIR']) / 'pattern-circular.png'))
        self.p.apply.click(); self.assertEqual(self.s.GeometryCount, 9, self.p.status.text())
        self.win.findChild(self.QtWidgets.QPushButton, 'SketchCancelAction').click(); self.QtTest.QTest.qWait(100)
        self.assertTrue(all(not w.isHidden() == visible for w, visible in self.sections))

    def test_preselection_grid_numeric_input_and_escape(self):
        from PySide6 import QtCore
        self.Gui.Selection.addSelection(self.s, 'Edge1')
        self.enter(); self.assertEqual(self.p.items.count(), 1)
        self.p.layout_mode.setCurrentText('Two directions')
        for e, axis in ((self.p.d1, 'H_Axis'), (self.p.d2, 'V_Axis')):
            self.pick(e.reference, axis)
            e.extent.setCurrentText('Two dimensions'); e.count.setValue(3); e.count2.setValue(2)
            e.value.setValue(10); e.value2.setValue(7)
        self.assertEqual(len(self.p.get_preview()), 15)
        self.p.d2.reverse.setChecked(True)
        self.assertTrue(self.p.apply.isEnabled(), self.p.status.text())
        self.win.findChild(self.QtWidgets.QDockWidget, 'Tasks').grab().save(str(Path(os.environ['PLUS_TEST_DIR']) / 'pattern-linear.png'))
        spin = self.p.d1.value
        spin.setFocus(); spin.selectAll()
        self.QtTest.QTest.keyClicks(spin, '12')
        self.assertEqual(spin.value(), 10)
        self.QtTest.QTest.keyClick(spin, QtCore.Qt.Key_Return)
        self.assertEqual(spin.value(), 12)
        self.p.lock.setChecked(True); self.p.apply.click()
        self.assertEqual(self.s.solve(), 0)
        self.assertEqual(sum(not self.s.getConstruction(i) for i in range(self.s.GeometryCount)), 17, self.p.status.text())
        self.p.items.setFocus(); self.QtTest.QTest.keyClick(self.p.items, QtCore.Qt.Key_Escape)
        self.QtTest.QTest.qWait(100)
        self.assertIsNotNone(self.Gui.activeDocument().getInEdit())
        self.assertTrue(all(not w.isHidden() == visible for w, visible in self.sections))

    def test_radius_pick_invalid_reference_and_removal(self):
        self.s.addConstraint(Sketcher.Constraint('Radius', 1, 2.0))
        self.enter(); self.pick(self.p.items, 'Edge1')
        self.p.mode.setCurrentText('Circular'); self.pick(self.p.center, 'Constraint1')
        self.assertEqual(self.p.references[self.p.center], (1, 3))
        self.assertTrue(self.p.apply.isEnabled(), self.p.status.text())
        self.p.mode.setCurrentText('Linear'); self.pick(self.p.d1.reference, 'H_Axis')
        self.pick(self.p.d1.reference, 'Edge2')
        self.assertFalse(self.p.apply.isEnabled()); self.assertTrue(self.p.status.error)
        self.pick(self.p.d1.reference, 'V_Axis'); self.assertTrue(self.p.apply.isEnabled())
        self.pick(self.p.d1.reference, 'H_Axis', True)
        self.assertTrue(self.p.d1.reference.text())
        self.pick(self.p.d1.reference, 'V_Axis', True)
        self.assertFalse(self.p.d1.reference.text())
        self.p.items.setCurrentRow(0); self.p.remove.click(); self.assertEqual(self.p.items.count(), 0)
        self.pick(self.p.items, 'Edge1'); self.p.clear.click(); self.assertEqual(self.p.items.count(), 0)
        self.p.done.click(); self.QtTest.QTest.qWait(100)

    def test_real_viewport_click_shift_axis_and_apply(self):
        from PySide6 import QtCore, QtGui
        self.enter()
        view = self.Gui.activeDocument().activeView()
        view.setAnimationEnabled(False); view.viewTop(); view.fitAll(); view.getCameraNode().height = 45
        self.QtTest.QTest.qWait(150)
        widget = view.graphicsView().viewport(); ratio = widget.devicePixelRatioF()
        def click(point, shift=False, expected=None):
            screen = view.getPointOnScreen(point)
            seed = QtCore.QPoint(round(screen[0]/ratio), widget.height()-1-round(screen[1]/ratio))
            for offset in (0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5):
                pos = seed + QtCore.QPoint(offset, 0)
                event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(pos),
                    QtCore.QPointF(widget.mapToGlobal(pos)), QtCore.Qt.NoButton, QtCore.Qt.NoButton, QtCore.Qt.NoModifier)
                self.QtWidgets.QApplication.sendEvent(widget, event); self.QtTest.QTest.qWait(70)
                if expected is None or expected in self.Gui.Selection.getPreselection().SubElementNames: break
            if expected: self.assertIn(expected, self.Gui.Selection.getPreselection().SubElementNames)
            self.QtTest.QTest.mouseClick(widget, QtCore.Qt.LeftButton,
                QtCore.Qt.ShiftModifier if shift else QtCore.Qt.NoModifier, pos)
            self.QtTest.QTest.qWait(100)
        click(App.Vector(7, 3, 0)); self.assertEqual(self.p.items.count(), 1)
        click(App.Vector(7, 3, 0)); self.assertEqual(self.p.items.count(), 1)
        click(App.Vector(7, 3, 0), True); self.assertEqual(self.p.items.count(), 0)
        click(App.Vector(7, 3, 0)); self.p.activate_pick(self.p.d1.reference)
        click(App.Vector(0, 7, 0), expected='V_Axis')
        self.assertTrue(self.p.apply.isEnabled(), self.p.status.text())
        self.p.apply.click(); self.assertEqual(sum(not self.s.getConstruction(i) for i in range(self.s.GeometryCount)), 6, self.p.status.text())
        self.win.grab().save(str(Path(os.environ['PLUS_TEST_DIR']) / 'pattern-viewport-applied.png'))
        self.p.done.click(); self.QtTest.QTest.qWait(100)

    def test_empty_sketch_and_component_presentations(self):
        self.Gui.activeDocument().resetEdit(); self.s.deleteAllGeometry()
        self.Gui.activeDocument().setEdit(self.s.Name); self.enter()
        self.assertFalse(self.p.apply.isEnabled()); self.p.done.click(); self.QtTest.QTest.qWait(100)
        self.Gui.activeDocument().resetEdit()
        from freecad_plus import document, modeling
        prefs = App.ParamGet('User parameter:BaseApp/Preferences/General')
        previous = prefs.GetInt('TaskPanelUIMode', 0)
        original = self.s
        try:
            for mode in (0, 1):
                prefs.SetInt('TaskPanelUIMode', mode)
                doc = document.new_document('PatternComponent')
                try:
                    self.s = modeling.new_sketch(doc)
                    self.s.addGeometry(Part.LineSegment(App.Vector(5, 3, 0), App.Vector(9, 3, 0)))
                    doc.recompute(); self.Gui.activeDocument().setEdit(self.s.Name)
                    self.enter(); self.pick(self.p.items, 'Edge1'); self.pick(self.p.d1.reference, 'H_Axis')
                    self.p.d1.count.setValue(2); self.p.apply.click()
                    self.assertEqual(sum(not self.s.getConstruction(i) for i in range(self.s.GeometryCount)), 2, self.p.status.text())
                    self.p.done.click(); self.QtTest.QTest.qWait(100); self.Gui.activeDocument().resetEdit()
                finally: App.closeDocument(doc.Name)
        finally:
            prefs.SetInt('TaskPanelUIMode', previous)
            App.setActiveDocument(self.doc.Name); self.s = original
