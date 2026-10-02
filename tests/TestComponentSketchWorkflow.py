# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component sketch creation, support, solver and native editor acceptance."""
import math
import json
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentExtrude as Extrude
from freecad.gui import ComponentSketchTask as Task
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentExtrudeTask as ExtrudeTask
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


class TestComponentSketchWorkflow(unittest.TestCase):
    def setUp(self):
        os.write(2, ("Sketch workflow: " + self._testMethodName + "\n").encode())
        Gui.activateWorkbench("PartDesignWorkbench")
        self.doc = Model.new_document("Sketch workflow")
        self.root = Model.metadata(self.doc).RootComponent
        self.panel = Navigator.show(self.doc)
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        self.messages = []
        self.watchdog = QtCore.QTimer()
        self.watchdog.timeout.connect(self.dismiss_dialogs)
        self.watchdog.start(25)
        Gui.Selection.clearSelection()
        settle()

    def dismiss_dialogs(self):
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if isinstance(widget, QtWidgets.QMessageBox) and widget.isVisible():
                self.messages.append(widget.text())
                widget.done(QtWidgets.QMessageBox.No)

    def tearDown(self):
        if Task._task:
            Task._task.reject()
        if ExtrudeTask._task:
            ExtrudeTask._task.reject()
        for doc in list(App.listDocuments().values()):
            gui = Gui.getDocument(doc.Name)
            if gui.getInEdit():
                gui.resetEdit()
        self.watchdog.stop()
        Gui.Selection.clearSelection()
        for name in reversed(list(App.listDocuments())):
            App.closeDocument(name)
        settle()
        QtWidgets.QApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)
        self.assertEqual(self.messages, [], "Unexpected modal sketch warnings")

    def box(self, component=None):
        obj = self.doc.addObject("Part::Box", "Support")
        Model.register_object(component or self.root, obj, "Object", True)
        obj.Length, obj.Width, obj.Height = 20, 15, 10
        self.doc.recompute()
        return obj

    def assertPlacement(self, actual, expected):
        for point in (App.Vector(), App.Vector(1, 0, 0), App.Vector(0, 1, 0)):
            self.assertLess((actual.multVec(point) - expected.multVec(point)).Length, 1e-6)

    def close_editor(self):
        Gui.activeDocument().resetEdit()
        settle()
        self.assertIsNone(Task._task)

    def accept(self, task):
        Gui.Control.activeTaskDialog().accept()
        settle()
        if Task._task is not None:
            self.fail(task.status.text())
        self.assertIsNotNone(task.result)
        self.assertTrue(Gui.activeDocument().getInEdit())
        self.assertEqual(Model.owner(task.result), self.root)
        return task.result

    def launch(self, command="Sketcher_NewSketch"):
        Gui.runCommand(command)
        settle()
        self.assertIsNotNone(Task._task)
        return Task._task

    def test_origin_planes_native_attachment_and_signed_offsets(self):
        for name in Sketch.ORIGIN_PLANES:
            rotation = Sketch.origin_plane(self.root, name).Placement.Rotation
            for offset in (-7.5, 0, 4.25):
                with self.subTest(plane=name, offset=offset):
                    obj = Sketch.create(self.root, name, offset)
                    self.assertEqual(str(obj.MapMode), "ObjectXY")
                    self.assertEqual(obj.AttachmentSupport[0][0], Sketch.origin_plane(self.root, name))
                    self.assertPlacement(obj.Placement, App.Placement(
                        rotation.multVec(App.Vector(0, 0, offset)), rotation))
        self.assertFalse(any(o.TypeId == "PartDesign::Body" for o in self.doc.Objects))

    def test_both_commands_cancel_and_origin_view_selection(self):
        before = [o.Name for o in self.doc.Objects]
        visibility = [o.Visibility for o in self.root.Origin.OriginFeatures]
        for command in ("PartDesign_NewSketch", "Sketcher_NewSketch"):
            task = self.launch(command)
            for name in Sketch.ORIGIN_PLANES:
                origin = Sketch.origin_plane(self.root, name)
                self.assertTrue(origin.ViewObject.isVisible())
                Gui.Selection.clearSelection()
                Gui.Selection.addSelection(origin)
                settle()
                self.assertEqual(task.plane.currentData(), name)
            task.reject()
            settle()
            self.assertEqual([o.Name for o in self.doc.Objects], before)
            self.assertEqual([o.Visibility for o in self.root.Origin.OriginFeatures], visibility)

    def test_face_preselection_attachment_recompute(self):
        box = self.box()
        Gui.Selection.addSelection(box, "Face6")
        task = self.launch()
        self.assertEqual(task.support, (box, "Face6"))
        task.offset.setProperty("rawValue", 2.5)
        obj = self.accept(task)
        self.close_editor()
        self.assertAlmostEqual(obj.Placement.Base.z, 12.5)
        box.Height = 18
        self.doc.recompute()
        self.assertAlmostEqual(obj.Placement.Base.z, 20.5)

    def test_face_picking_after_task_launch(self):
        box = self.box()
        task = self.launch()
        Gui.Selection.addSelection(box, "Face6")
        settle()
        self.assertEqual(task.plane.currentData(), "Selected planar face")
        self.assertEqual(task.support, (box, "Face6"))
        self.accept(task)
        self.close_editor()

    def test_existing_native_and_part_planes_and_picker(self):
        datum_sketch = Sketch.create(self.root, "Create new plane", 3,
                                    new_plane_base="XZ plane", angles=(15, 20, 30))
        datum = datum_sketch.AttachmentSupport[0][0]
        surface = self.doc.addObject("Part::Plane", "UserPlane")
        Model.register_object(self.root, surface)
        surface.Placement = App.Placement(App.Vector(8, 9, 10), App.Rotation(App.Vector(1, 0, 0), 35))
        self.doc.recompute()
        for support in (datum, surface):
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(support)
            task = self.launch()
            self.assertEqual(task.plane.currentData(), "User plane")
            self.assertEqual(task.user_plane.currentData(), support.Name)
            obj = self.accept(task)
            self.close_editor()
            self.assertPlacement(obj.Placement, support.Placement)

    def test_create_plane_task_cancel_atomic_accept_undo_redo(self):
        task = self.launch()
        task.plane.setCurrentIndex(task.plane.findData("Create new plane"))
        task.base.setCurrentIndex(task.base.findData("XZ plane"))
        task.offset.setProperty("rawValue", 8)
        task.rotations[1].setProperty("rawValue", 25)
        before = [o.Name for o in self.doc.Objects]
        task.form.grab().save(str(self.output / "new-plane-options.png"))
        task.reject()
        self.assertEqual([o.Name for o in self.doc.Objects], before)
        task = self.launch()
        task.plane.setCurrentIndex(task.plane.findData("Create new plane"))
        task.base.setCurrentIndex(task.base.findData("XZ plane"))
        task.offset.setProperty("rawValue", 8)
        task.rotations[1].setProperty("rawValue", 25)
        undo = self.doc.UndoCount
        obj = self.accept(task)
        self.assertEqual(self.doc.UndoCount, undo + 1)
        plane = obj.AttachmentSupport[0][0]
        self.assertEqual(plane.TypeId, "PartDesign::Plane")
        self.assertEqual(plane.Label, "Plane001")
        self.assertEqual(obj.Label, "Sketch001")
        self.assertEqual(Model.history(self.root), [plane, obj])
        self.close_editor()
        # Native Sketcher owns a separate edit transaction. Undo those edit
        # entries first, then verify the creation itself removes both objects.
        while self.doc.UndoCount > undo + 1:
            self.doc.undo()
        self.assertEqual(len(Model.history(self.root)), 2)
        identities = (plane.ObjectId, obj.ObjectId)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual([o.Name for o in self.doc.Objects], before)
        self.doc.redo()
        self.doc.recompute()
        self.assertEqual(tuple(o.ObjectId for o in Model.history(self.root)), identities)

    def test_face_based_new_plane_and_plane_based_chain_recompute(self):
        box = self.box()
        obj = Sketch.create(self.root, "Create new plane", 4, (box, "Face6"),
                            "Selected planar face", (0, 20, 0))
        plane = obj.AttachmentSupport[0][0]
        child = Sketch.create(self.root, "Create new plane", 3, plane, "User plane")
        child_plane = child.AttachmentSupport[0][0]
        self.assertEqual(plane.AttachmentSupport[0][0], box)
        self.assertEqual(child_plane.AttachmentSupport[0][0], plane)
        before = child.Placement.Base
        box.Height = box.Height.Value + 5
        self.doc.recompute()
        self.assertAlmostEqual((child.Placement.Base - before).z, 5)
        self.assertPlacement(child.Placement, child_plane.Placement)

    def test_invalid_supports_and_new_plane_rollback(self):
        box = self.box()
        cylinder = self.doc.addObject("Part::Cylinder", "Cylinder")
        Model.register_object(self.root, cylinder, "Object", True)
        other = Model.add_component(self.root).LinkedObject
        foreign = self.box(other)
        self.doc.recompute()
        before = [o.Name for o in self.doc.Objects]
        for support in (None, (box, "Edge1"), (box, "Face999"), (cylinder, "Face1"), (foreign, "Face6")):
            with self.subTest(support=str(support)):
                with self.assertRaises((ValueError, IndexError, RuntimeError, Part.OCCError)):
                    Sketch.create(self.root, "Create new plane", 0, support, "Selected planar face")
                self.assertEqual([o.Name for o in self.doc.Objects], before)
                self.assertFalse(self.doc.HasPendingTransaction)
        task = self.launch()
        task.plane.setCurrentIndex(task.plane.findData("User plane"))
        self.assertFalse(task.accept())
        self.assertEqual([o.Name for o in self.doc.Objects], before)
        self.assertTrue(Gui.Control.activeDialog())

    def test_new_plane_user_selection_and_local_labels(self):
        first = Sketch.create(self.root, "Create new plane")
        plane = first.AttachmentSupport[0][0]
        task = self.launch()
        task.plane.setCurrentIndex(task.plane.findData("Create new plane"))
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(plane)
        settle()
        self.assertEqual(task.plane.currentData(), "Create new plane")
        self.assertEqual(task.base.currentData(), "User plane")
        obj = self.accept(task)
        self.close_editor()
        self.assertEqual(obj.AttachmentSupport[0][0].Label, "Plane002")
        child = Model.add_component(self.root).LinkedObject
        child_sketch = Sketch.create(child, "Create new plane")
        self.assertEqual(child_sketch.Label, "Sketch001")
        self.assertEqual(child_sketch.AttachmentSupport[0][0].Label, "Plane001")

    def edit(self, obj=None):
        self.sketch = obj or Sketch.create(self.root)
        self.doc.recompute()
        self.assertTrue(Gui.activeDocument().setEdit(self.sketch.Name))
        settle()
        return self.sketch

    def selected_command(self, command, *elements):
        Gui.Selection.clearSelection()
        for element in elements:
            Gui.Selection.addSelection(self.sketch, element)
        Gui.runCommand(command)
        self.doc.recompute()
        settle()

    def test_curve_families_active_construction_and_persistence(self):
        spline = Part.BSplineCurve()
        spline.interpolate([App.Vector(1, 1, 0), App.Vector(4, 6, 0), App.Vector(8, 2, 0)])
        curves = [Part.LineSegment(App.Vector(), App.Vector(10, 0, 0)),
                  Part.Circle(App.Vector(20, 0, 0), App.Vector(0, 0, 1), 3),
                  Part.ArcOfCircle(Part.Circle(App.Vector(30, 0, 0), App.Vector(0, 0, 1), 4), 0, math.pi),
                  Part.Ellipse(App.Vector(44, 0, 0), App.Vector(40, 2, 0), App.Vector(40, 0, 0)), spline]
        obj = Sketch.create(self.root)
        for curve in curves:
            obj.addGeometry(curve, False)
            obj.addGeometry(curve, True)
        self.doc.recompute()
        self.assertEqual(obj.GeometryCount, 10)
        self.assertEqual(len(obj.Shape.Edges), 5)
        flags = [obj.getConstruction(i) for i in range(obj.GeometryCount)]
        self.assertEqual(flags, [False, True] * 5)
        identity = obj.ObjectId
        path = self.output / "curve-families.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.root = Model.metadata(self.doc).RootComponent
        obj = next(o for o in Model.history(self.root) if o.ObjectId == identity)
        self.assertEqual([o.TypeId for o in obj.Geometry], [o.TypeId for o in curves for _ in range(2)])
        self.assertEqual([obj.getConstruction(i) for i in range(10)], flags)
        self.assertEqual(len(obj.Shape.Edges), 5)
        self.edit(obj)
        self.close_editor()

    def test_native_construction_toggle_undo_redo(self):
        obj = Sketch.create(self.root)
        obj.addGeometry(Part.LineSegment(App.Vector(2, 3, 0), App.Vector(12, 8, 0)))
        self.edit(obj)
        undo = self.doc.UndoCount
        self.selected_command("Sketcher_ToggleConstruction", "Edge1")
        self.assertTrue(obj.getConstruction(0))
        self.assertEqual(len(obj.Shape.Edges), 0)
        self.assertEqual(self.doc.UndoCount, undo + 1)
        self.doc.undo()
        self.doc.recompute()
        settle()
        self.assertFalse(obj.getConstruction(0))
        self.doc.redo()
        self.doc.recompute()
        settle()
        self.assertTrue(obj.getConstruction(0))
        self.selected_command("Sketcher_ToggleConstruction", "Edge1")
        self.assertFalse(obj.getConstruction(0))

    def test_native_geometric_constraints_and_solver(self):
        fixtures = [
            ("Sketcher_ConstrainHorizontal", "Horizontal", [((0, 0), (10, 2))], ("Edge1",)),
            ("Sketcher_ConstrainVertical", "Vertical", [((0, 0), (2, 10))], ("Edge1",)),
            ("Sketcher_ConstrainParallel", "Parallel", [((0, 0), (10, 1)), ((0, 5), (10, 8))], ("Edge1", "Edge2")),
            ("Sketcher_ConstrainPerpendicular", "Perpendicular", [((0, 0), (10, 1)), ((0, 5), (2, 14))], ("Edge1", "Edge2")),
            ("Sketcher_ConstrainEqual", "Equal", [((0, 0), (10, 0)), ((0, 5), (7, 5))], ("Edge1", "Edge2")),
            ("Sketcher_ConstrainCoincident", "Coincident", [((0, 0), (10, 0)), ((11, 1), (15, 8))], ("Vertex2", "Vertex3")),
            ("Sketcher_ConstrainPointOnObject", "PointOnObject", [((0, 0), (10, 0)), ((3, 2), (8, 8))], ("Vertex3", "Edge1")),
            ("Sketcher_ConstrainBlock", "Block", [((2, 3), (9, 11))], ("Edge1",)),
        ]
        for command, kind, lines, selection in fixtures:
            with self.subTest(command=command):
                obj = Sketch.create(self.root)
                for start, end in lines:
                    obj.addGeometry(Part.LineSegment(App.Vector(*start, 0), App.Vector(*end, 0)))
                self.edit(obj)
                before = obj.ConstraintCount
                undo = self.doc.UndoCount
                self.selected_command(command, *selection)
                self.assertGreater(obj.ConstraintCount, before)
                self.assertIn(kind, [c.Type for c in obj.Constraints])
                self.assertEqual(obj.solve(), 0)
                self.assertEqual(self.doc.UndoCount, undo + 1)
                self.doc.undo()
                self.doc.recompute()
                self.assertEqual(obj.ConstraintCount, before)
                self.doc.redo()
                self.doc.recompute()
                self.assertIn(kind, [c.Type for c in obj.Constraints])
                self.close_editor()

    def test_tangent_symmetry_and_coincident_constraints(self):
        obj = Sketch.create(self.root)
        obj.addGeometry(Part.LineSegment(App.Vector(-5, -3, 0), App.Vector(5, -3, 0)))
        obj.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 3))
        obj.addConstraint(Sketcher.Constraint("Tangent", 0, 1))
        obj.addConstraint(Sketcher.Constraint("Symmetric", 0, 1, 0, 2, -1, 1))
        self.doc.recompute()
        self.assertEqual(obj.solve(), 0)
        self.edit(obj)
        self.assertEqual(obj.solve(), 0)
        self.close_editor()

    def test_native_driving_and_reference_dimensions(self):
        obj = Sketch.create(self.root)
        obj.addGeometry(Part.Circle(App.Vector(5, 6, 0), App.Vector(0, 0, 1), 3))
        self.edit(obj)
        prefs = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Sketcher")
        old = prefs.GetBool("ShowDialogOnDistanceConstraint", True)
        prefs.SetBool("ShowDialogOnDistanceConstraint", False)
        self.addCleanup(prefs.SetBool, "ShowDialogOnDistanceConstraint", old)
        self.selected_command("Sketcher_ConstrainRadius", "Edge1")
        self.assertEqual(obj.ConstraintCount, 1)
        self.assertTrue(obj.Constraints[0].Driving)
        obj.setDatum(0, App.Units.Quantity("5 mm"))
        self.doc.recompute()
        self.assertAlmostEqual(obj.Geometry[0].Radius, 5)
        self.selected_command("Sketcher_ToggleDrivingConstraint", "Constraint1")
        self.assertFalse(obj.Constraints[0].Driving)
        obj.moveGeometry(0, 0, App.Vector(12, 6, 0), False)
        self.doc.recompute()
        self.assertNotAlmostEqual(obj.Geometry[0].Radius, 5)
        self.assertAlmostEqual(obj.Constraints[0].Value, obj.Geometry[0].Radius)
        self.selected_command("Sketcher_ToggleDrivingConstraint", "Constraint1")
        self.assertTrue(obj.Constraints[0].Driving)
        # Creation mode changes without a selected constraint must create a
        # reference dimension directly, not merely convert an existing one.
        Gui.Selection.clearSelection()
        Gui.runCommand("Sketcher_ToggleDrivingConstraint")
        try:
            self.selected_command("Sketcher_ConstrainDistanceX", "Vertex1")
            self.assertEqual(obj.ConstraintCount, 2)
            self.assertFalse(obj.Constraints[1].Driving)
        finally:
            Gui.Selection.clearSelection()
            Gui.runCommand("Sketcher_ToggleDrivingConstraint")

    def test_dimension_types_measurement_and_construction_solver(self):
        fixtures = [
            (Part.LineSegment(App.Vector(2, 3, 0), App.Vector(12, 7, 0)), Sketcher.Constraint("Distance", 0, 15.)),
            (Part.LineSegment(App.Vector(2, 3, 0), App.Vector(12, 7, 0)), Sketcher.Constraint("DistanceX", 0, 1, 0, 2, 20.)),
            (Part.LineSegment(App.Vector(2, 3, 0), App.Vector(12, 7, 0)), Sketcher.Constraint("DistanceY", 0, 1, 0, 2, 10.)),
            (Part.LineSegment(App.Vector(2, 3, 0), App.Vector(12, 7, 0)), Sketcher.Constraint("Angle", 0, math.pi / 4)),
            (Part.Circle(App.Vector(5, 6, 0), App.Vector(0, 0, 1), 3), Sketcher.Constraint("Radius", 0, 8.)),
            (Part.Circle(App.Vector(5, 6, 0), App.Vector(0, 0, 1), 3), Sketcher.Constraint("Diameter", 0, 12.)),
        ]
        for geometry, constraint in fixtures:
            for construction in (False, True):
                with self.subTest(kind=constraint.Type, construction=construction):
                    obj = Sketch.create(self.root)
                    obj.addGeometry(geometry, construction)
                    index = obj.addConstraint(constraint)
                    self.doc.recompute()
                    self.assertEqual(obj.solve(), 0)
                    self.assertTrue(obj.Constraints[index].Driving)
                    self.assertAlmostEqual(obj.Constraints[index].Value, constraint.Value)
                    obj.setDriving(index, False)
                    self.doc.recompute()
                    self.assertEqual(obj.solve(), 0)
                    self.assertFalse(obj.Constraints[index].Driving)
                    self.assertAlmostEqual(obj.Constraints[index].Value, constraint.Value)
                    self.assertEqual(bool(obj.Shape.Edges), not construction)

    def test_fully_constrained_rectangle_reference_and_extrude_updates(self):
        obj = Sketch.create(self.root, "Create new plane", 4)
        points = [App.Vector(), App.Vector(20, 0, 0), App.Vector(20, 10, 0), App.Vector(0, 10, 0)]
        for i in range(4):
            obj.addGeometry(Part.LineSegment(points[i], points[(i+1)%4]))
        for i in range(4):
            obj.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i+1)%4, 1))
            obj.addConstraint(Sketcher.Constraint("Horizontal" if i%2 == 0 else "Vertical", i))
        obj.addConstraint(Sketcher.Constraint("Coincident", 0, 1, -1, 1))
        width = obj.addConstraint(Sketcher.Constraint("Distance", 0, 20.))
        height = obj.addConstraint(Sketcher.Constraint("Distance", 1, 10.))
        obj.renameConstraint(width, "Width")
        obj.renameConstraint(height, "Height")
        diagonal = obj.addGeometry(Part.LineSegment(points[0], points[2]), True)
        obj.addConstraint(Sketcher.Constraint("Coincident", diagonal, 1, 0, 1))
        obj.addConstraint(Sketcher.Constraint("Coincident", diagonal, 2, 1, 2))
        measurement = obj.addConstraint(Sketcher.Constraint("Distance", diagonal, math.sqrt(500)))
        obj.setDriving(measurement, False)
        self.doc.recompute()
        self.assertEqual(obj.solve(), 0)
        self.assertTrue(obj.FullyConstrained)
        operation, result = Extrude.create(self.root, obj, 5)
        self.assertAlmostEqual(result.Shape.Volume, 1000)
        with Model.transaction(self.doc, "Resize constrained rectangle"):
            obj.setDatum(width, App.Units.Quantity("30 mm"))
        self.assertAlmostEqual(result.Shape.Volume, 1500)
        self.assertAlmostEqual(obj.Constraints[measurement].Value, math.sqrt(1000))
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 1000)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 1500)
        obj.Visibility = True
        self.edit(obj)
        Gui.activeDocument().activeView().fitAll()
        settle()
        Gui.getMainWindow().grab().save(str(self.output / "constrained-reference-sketch.png"))
        self.close_editor()
        identities = obj.ObjectId, obj.AttachmentSupport[0][0].ObjectId, result.ObjectId
        self.doc.saveAs(str(self.output / "constrained-workflow.cadprt"))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(self.output / "constrained-workflow.cadprt"))
        self.root = Model.metadata(self.doc).RootComponent
        obj = next(o for o in Model.history(self.root) if o.ObjectId == identities[0])
        result = next(o for o in self.doc.Objects if getattr(o, "ObjectId", "") == identities[2])
        self.assertEqual(obj.AttachmentSupport[0][0].ObjectId, identities[1])
        self.assertTrue(obj.FullyConstrained)
        self.assertTrue(obj.getConstruction(diagonal))
        self.assertFalse(obj.Constraints[measurement].Driving)
        self.assertAlmostEqual(result.Shape.Volume, 1500)
        self.edit(obj)
        self.close_editor()

    def test_external_projection_is_associative_reference_geometry(self):
        box = self.box()
        obj = Sketch.create(self.root)
        obj.addExternal(box.Name, "Edge9")
        self.doc.recompute()
        self.assertEqual(obj.ExternalGeometry[0], (box, ("Edge9",)))
        self.assertEqual(obj.GeometryCount, 0)
        self.assertEqual(len(obj.Shape.Edges), 0)
        self.edit(obj)
        self.close_editor()
        box.Height = 14
        self.doc.recompute()
        self.assertEqual(obj.ExternalGeometry[0][0], box)
        self.assertNotIn("Invalid", obj.State)

    def draw(self, command, points, construction=False):
        obj = self.edit()
        view = Gui.activeDocument().activeView()
        view.viewTop()
        view.setCameraType("Orthographic")
        settle()
        widgets = [w for w in Gui.getMainWindow().findChildren(QtWidgets.QWidget)
                   if "GL" in w.metaObject().className() and w.width()>100 and w.height()>100]
        viewport = max(widgets, key=lambda w: w.width()*w.height())
        if construction:
            Gui.runCommand("Sketcher_ToggleConstruction")
        Gui.runCommand(command)
        settle()
        for x, y in points:
            sx, sy = view.getPointOnScreen(App.Vector(x, y, 0))
            ratio = viewport.devicePixelRatioF()
            pos = QtCore.QPoint(round(sx/ratio), viewport.height()-round(sy/ratio)-1)
            event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, QtCore.QPointF(pos),
                QtCore.QPointF(viewport.mapToGlobal(pos)), QtCore.Qt.NoButton,
                QtCore.Qt.NoButton, QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(viewport, event)
            settle(50)
            QtTest.QTest.mouseClick(viewport, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, pos)
            settle()
        QtTest.QTest.keyClick(viewport, QtCore.Qt.Key_Escape)
        settle()
        if construction:
            Gui.Selection.clearSelection()
            Gui.runCommand("Sketcher_ToggleConstruction")
        self.doc.recompute()
        return obj

    def test_native_draw_active_line(self):
        obj = self.draw("Sketcher_CreateLine", [(2, 3), (12, 8)])
        self.assertEqual(obj.GeometryCount, 1)
        self.assertFalse(obj.getConstruction(0))
        self.assertEqual(len(obj.Shape.Edges), 1)

    def test_native_draw_reference_circle(self):
        obj = self.draw("Sketcher_CreateCircle", [(-8, 4), (-4, 4)], True)
        self.assertEqual(obj.GeometryCount, 1)
        self.assertTrue(obj.getConstruction(0))
        self.assertEqual(len(obj.Shape.Edges), 0)

    def test_native_draw_rectangle_constraints(self):
        obj = self.draw("Sketcher_CreateRectangle", [(2, 3), (18, 13)])
        self.assertEqual(obj.GeometryCount, 4)
        self.assertTrue({"Coincident", "Horizontal", "Vertical"} <= {c.Type for c in obj.Constraints})
        self.assertEqual(obj.solve(), 0)

    def test_native_draw_arc(self):
        obj = self.draw("Sketcher_CreateArc", [(4, 3), (12, 3), (4, 11)])
        self.assertEqual(obj.GeometryCount, 1)
        self.assertEqual(obj.Geometry[0].TypeId, "Part::GeomArcOfCircle")
        self.assertFalse(obj.getConstruction(0))

    def test_origin_preselection_and_create_plane_origin_pick(self):
        for name in Sketch.ORIGIN_PLANES:
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(Sketch.origin_plane(self.root, name))
            task = self.launch()
            self.assertEqual(task.plane.currentData(), name)
            task.plane.setCurrentIndex(task.plane.findData("Create new plane"))
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(Sketch.origin_plane(self.root, "YZ plane"))
            settle()
            self.assertEqual(task.plane.currentData(), "Create new plane")
            self.assertEqual(task.base.currentData(), "YZ plane")
            task.capture.click()
            self.assertEqual(task.base.currentData(), "YZ plane")
            self.assertIn("Origin plane selected", task.status.text())
            task.reject()
            settle()

    def test_new_plane_from_selected_face_task_and_source_removal_recovery(self):
        box = self.box()
        task = self.launch()
        task.plane.setCurrentIndex(task.plane.findData("Create new plane"))
        Gui.Selection.addSelection(box, "Face6")
        settle()
        self.assertEqual(task.base.currentData(), "Selected planar face")
        task.offset.setProperty("rawValue", -2)
        for i, value in enumerate((10, 20, 30)):
            task.rotations[i].setProperty("rawValue", value)
        obj = self.accept(task)
        plane = obj.AttachmentSupport[0][0]
        self.close_editor()
        self.assertAlmostEqual(plane.Placement.Base.z, 8)
        self.assertPlacement(obj.Placement, plane.Placement)
        task = self.launch()
        task.plane.setCurrentIndex(task.plane.findData("Create new plane"))
        task.base.setCurrentIndex(task.base.findData("Selected planar face"))
        task.support = (box, "Face999")
        before = [o.Name for o in self.doc.Objects]
        self.assertFalse(task.accept())
        self.assertEqual([o.Name for o in self.doc.Objects], before)
        self.assertFalse(self.doc.HasPendingTransaction)
        task.support = (box, "Face6")
        self.accept(task)
        self.close_editor()

    def test_native_dimension_value_dialog_accept_and_cancel(self):
        obj = Sketch.create(self.root)
        obj.addGeometry(Part.Circle(App.Vector(5, 6, 0), App.Vector(0, 0, 1), 3))
        self.edit(obj)
        prefs = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Sketcher")
        old = prefs.GetBool("ShowDialogOnDistanceConstraint", True)
        prefs.SetBool("ShowDialogOnDistanceConstraint", True)
        self.addCleanup(prefs.SetBool, "ShowDialogOnDistanceConstraint", old)
        seen = []
        decision = [True]
        timer = QtCore.QTimer()
        def fill():
            for dialog in QtWidgets.QApplication.topLevelWidgets():
                if isinstance(dialog, QtWidgets.QDialog) and dialog.isVisible() and dialog.windowTitle() == "Insert Radius":
                    seen.append(dialog.windowTitle())
                    field = dialog.findChild(QtWidgets.QWidget, "labelEdit")
                    field.setProperty("rawValue", 9.)
                    dialog.accept() if decision[0] else dialog.reject()
        timer.timeout.connect(fill)
        timer.start(25)
        try:
            before_undo = self.doc.UndoCount
            self.selected_command("Sketcher_ConstrainRadius", "Edge1")
            self.assertTrue(seen)
            self.assertAlmostEqual(obj.Geometry[0].Radius, 9)
            self.assertTrue(obj.Constraints[0].Driving)
            (self.output / "dimension-dialog-transactions.json").write_text(json.dumps({
                "undo_before": before_undo, "undo_after": self.doc.UndoCount,
                "undo_names": self.doc.UndoNames, "pending": self.doc.HasPendingTransaction}, indent=2))
            # FreeCAD's default first-dimension autoscale deliberately owns a
            # separate Scale geometries transaction from constraint insertion.
            self.assertEqual(self.doc.UndoCount, before_undo + 2)
            self.assertEqual(self.doc.UndoNames[:2], ["Scale geometries", "Add radius constraint"])
            Gui.runCommand("Std_Undo")
            self.doc.recompute()
            settle()
            self.assertEqual(obj.ConstraintCount, 1)
            self.assertAlmostEqual(obj.Geometry[0].Radius, 3)
            Gui.runCommand("Std_Undo")
            self.doc.recompute()
            settle()
            self.assertEqual(obj.ConstraintCount, 0)
            self.assertAlmostEqual(obj.Geometry[0].Radius, 3)
            for _ in range(2):
                Gui.runCommand("Std_Redo")
                self.doc.recompute()
                settle()
            self.assertEqual(obj.ConstraintCount, 1)
            self.assertAlmostEqual(obj.Geometry[0].Radius, 9)
            for _ in range(2):
                Gui.runCommand("Std_Undo")
                self.doc.recompute()
                settle()
            decision[0] = False
            self.selected_command("Sketcher_ConstrainRadius", "Edge1")
            self.assertEqual(len(seen), 2)
            self.assertEqual(obj.ConstraintCount, 0)
            self.assertAlmostEqual(obj.Geometry[0].Radius, 3)
        finally:
            timer.stop()

    def test_expression_dimensions_units_and_reference_updates(self):
        obj = Sketch.create(self.root)
        obj.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 3))
        radius = obj.addConstraint(Sketcher.Constraint("Radius", 0, 3.))
        obj.renameConstraint(radius, "Radius")
        diameter = obj.addConstraint(Sketcher.Constraint("Diameter", 0, 6.))
        obj.setDriving(diameter, False)
        obj.setExpression("Constraints.Radius", "0.25 in")
        self.doc.recompute()
        self.assertAlmostEqual(obj.Geometry[0].Radius, 6.35)
        self.assertAlmostEqual(obj.Constraints[diameter].Value, 12.7)
        self.assertEqual(obj.solve(), 0)
        self.assertFalse(obj.Constraints[diameter].Driving)
        obj.setExpression("Constraints.Radius", "10 mm")
        self.doc.recompute()
        self.assertAlmostEqual(obj.Constraints[diameter].Value, 20)
        self.edit(obj)
        self.close_editor()

    def test_deleted_plane_and_pending_task_refusal(self):
        obj = Sketch.create(self.root, "Create new plane")
        plane = obj.AttachmentSupport[0][0]
        task = self.launch()
        with self.assertRaisesRegex(ValueError, "Finish the current task"):
            Task.launch(self.root)
        task.plane.setCurrentIndex(task.plane.findData("User plane"))
        task.user_plane.setCurrentIndex(task.user_plane.findData(plane.Name))
        with Model.transaction(self.doc, "Remove test plane"):
            self.doc.removeObject(obj.Name)
            self.doc.removeObject(plane.Name)
        before = [o.Name for o in self.doc.Objects]
        self.assertFalse(task.accept())
        self.assertEqual([o.Name for o in self.doc.Objects], before)
        self.assertFalse(self.doc.HasPendingTransaction)
        task.plane.setCurrentIndex(task.plane.findData("XY plane"))
        self.accept(task)
        self.close_editor()

    def test_new_plane_sketch_native_extrude_region_acceptance(self):
        obj = Sketch.create(self.root, "Create new plane", 7)
        plane = obj.AttachmentSupport[0][0]
        obj.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 10))
        self.doc.recompute()
        self.assertTrue(plane.Visibility)
        self.assertTrue(obj.Visibility)
        task = ExtrudeTask.launch(self.root)
        task.profile.setCurrentIndex(task.profile.findData(obj.Name))
        task.set_curves([], False)
        task.length.setProperty("rawValue", 5)
        frame = self.root.getGlobalPlacement().multiply(obj.Placement)
        task.view.setCameraOrientation(frame.Rotation.Q)
        task.view.fitAll()
        settle()
        position = task.view.getPointOnViewport(frame.multVec(App.Vector(4, 3, 0)))
        hit = task.view.getObjectInfo(position)
        (self.output / "new-plane-region-hit.json").write_text(json.dumps(hit, indent=2, default=str))
        task.pick_region({"State": "DOWN", "Button": "BUTTON1", "Position": position})
        self.assertEqual(task.curve_names(), ["Edge1"], task.status.text())
        if not task.accept():
            self.fail(task.status.text())
        self.assertAlmostEqual(task.result.Shape.Volume, 500 * math.pi)
        self.assertAlmostEqual(task.result.Shape.BoundBox.ZMin, 7)
        self.assertEqual(obj.AttachmentSupport[0][0], plane)
