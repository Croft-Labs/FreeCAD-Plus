# SPDX-License-Identifier: LGPL-2.1-or-later
"""Subset geometry, associative persistence and task collector regressions."""
import importlib.util
import math
import os
from pathlib import Path
import sys
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher

# Explicit opt-in allows geometry checks before the next grouped native build.
if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    root = Path(os.environ["FREECAD_PLUS_SOURCE"])
    for name in ("ComponentModel", "ComponentResultView", "ComponentSketch", "ComponentProfile", "ComponentExtent", "ComponentExtrude"):
        spec = importlib.util.spec_from_file_location(name, root / "src/Mod/Part" / (name + ".py"))
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    name = "freecad.gui.ComponentSelection"
    spec = importlib.util.spec_from_file_location(name, root / "src/Gui/ComponentSelection.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    import freecad.gui
    freecad.gui.ComponentSelection = module
    name = "freecad.gui.OccurrenceMove"
    spec = importlib.util.spec_from_file_location(name, root / "src/Gui/OccurrenceMove.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    freecad.gui.OccurrenceMove = module

import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentProfile as Profile
import ComponentExtrude as Extrude
import ComponentExtent as Extent


def task_module():
    if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") != "1":
        from freecad.gui import ComponentExtrudeTask
        return ComponentExtrudeTask
    path = Path(os.environ["FREECAD_PLUS_SOURCE"]) / "src/Gui/ComponentExtrudeTask.py"
    spec = importlib.util.spec_from_file_location("CurveProfileTaskOverlay", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestComponentCurveProfile(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_document("Part")
        self.component = Model.metadata(self.doc).RootComponent
        self.sketch = Sketch.create(self.component)
        for center, radius in ((App.Vector(), 10), (App.Vector(), 5), (App.Vector(30, 0, 0), 2)):
            self.sketch.addGeometry(Part.Circle(center, App.Vector(0, 0, 1), radius))
        self.sketch.addGeometry(Part.LineSegment(App.Vector(40, 0, 0), App.Vector(45, 0, 0)))
        self.doc.recompute()

    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def testRegionsAndRejectedContours(self):
        self.assertAlmostEqual(Profile.face(self.sketch, ["Edge1", "Edge2"]).Area, 75 * math.pi)
        self.assertEqual(Profile.region(self.sketch, App.Vector(7, 0, 0)), ["Edge1", "Edge2"])
        self.assertEqual(Profile.region(self.sketch, App.Vector()), ["Edge2"])
        for elements in ([], ["Edge4"], ["Edge1", "Edge3"], ["Vertex1"], ["Edge99"]):
            with self.assertRaises(ValueError):
                Profile.face(self.sketch, elements)
        crossing = Sketch.create(self.component)
        for center in (App.Vector(), App.Vector(3, 0, 0)):
            crossing.addGeometry(Part.Circle(center, App.Vector(0, 0, 1), 2))
        self.doc.recompute()
        with self.assertRaises(ValueError):
            Profile.face(crossing, ["Edge1", "Edge2"])
        for center in (App.Vector(60, 0, 0), App.Vector(63, 0, 0)):
            self.sketch.addGeometry(Part.Circle(center, App.Vector(0, 0, 1), 2))
        self.doc.recompute()
        self.assertEqual(Profile.region(self.sketch, App.Vector(7, 0, 0)), ["Edge1", "Edge2"])
        bow = Sketch.create(self.component)
        points = [App.Vector(0, 0, 0), App.Vector(4, 4, 0), App.Vector(0, 4, 0), App.Vector(4, 0, 0)]
        for a, b in zip(points, points[1:] + points[:1]):
            bow.addGeometry(Part.LineSegment(a, b))
        self.doc.recompute()
        with self.assertRaises(ValueError):
            Profile.face(bow, ["Edge1", "Edge2", "Edge3", "Edge4"])

    def testNativeEngineWithoutBody(self):
        import PartDesign
        pad = self.doc.addObject("PartDesign::Pad", "NativeExtentProbe")
        self.component.addObject(pad)
        pad.Profile = (Profile.bind(self.component, self.sketch, ["Edge1", "Edge2"]), [])
        pad.Length = 4
        self.doc.recompute()
        self.assertNotIn("Invalid", pad.State, str(pad.State))
        self.assertAlmostEqual(pad.Shape.Volume, 300 * math.pi)
        pad.SideType = "Symmetric"
        pad.Length = 6
        self.doc.recompute()
        self.assertAlmostEqual(pad.Shape.Volume, 450 * math.pi)
        self.assertAlmostEqual(pad.Shape.BoundBox.ZMin, -3)
        self.assertAlmostEqual(pad.Shape.BoundBox.ZMax, 3)
        self.assertFalse(any(obj.TypeId == "PartDesign::Body" for obj in self.doc.Objects))

    def target_box(self):
        box = self.doc.addObject("Part::Feature", "TargetBox")
        box.Shape = Part.makeBox(40, 40, 12, App.Vector(-20, -20, 0))
        Model.register_object(self.component, box, "Result", True)
        self.doc.recompute()
        return box

    def testDimensionalExtentsAndLegacyEditMigration(self):
        options = Extent.defaults()
        options.update(start="Offset", start_offset=2.)
        operation, body = Extrude.create(self.component, self.sketch, 4, elements=["Edge2"], options=options)
        self.assertAlmostEqual(body.Shape.BoundBox.ZMin, 2)
        self.assertAlmostEqual(body.Shape.BoundBox.ZMax, 6)
        identity = body.ObjectId
        options.update(sides="Symmetric")
        operation = Extrude.edit(operation, self.sketch, 6, elements=["Edge2"], options=options)
        self.assertAlmostEqual(body.Shape.BoundBox.ZMin, -1)
        self.assertAlmostEqual(body.Shape.BoundBox.ZMax, 5)
        options.update(sides="Two sides", length2=3.)
        operation = Extrude.edit(operation, self.sketch, 4, elements=["Edge2"], options=options)
        self.assertAlmostEqual(body.Shape.BoundBox.ZMin, -1)
        self.assertAlmostEqual(body.Shape.BoundBox.ZMax, 6)
        self.assertEqual(body.ObjectId, identity)
        legacy, old_body = Extrude.create(self.component, self.sketch, 4, elements=["Edge2"])
        old_id, old_operation_id = old_body.ObjectId, legacy.ObjectId
        updated = Extrude.edit(legacy, self.sketch, 6, elements=["Edge2"], options=options)
        self.assertEqual(updated.TypeId, "PartDesign::Pad")
        self.assertEqual(updated.ObjectId, old_operation_id)
        self.assertEqual(old_body.ObjectId, old_id)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(old_body.Producer.TypeId, "Part::Extrusion")
        self.doc.redo()
        self.doc.recompute()
        self.assertEqual(old_body.Producer.TypeId, "PartDesign::Pad")

    def testSurfaceOffsetsAndAssociativeReferences(self):
        plane = self.doc.addObject("Part::Feature", "LimitSurface")
        plane.Shape = Part.makePlane(50, 50, App.Vector(-25, -25, 8))
        Model.register_object(self.component, plane)
        self.doc.recompute()
        options = Extent.defaults()
        options.update(extent="UpToFace", limit=(plane, ["Face1"]), offset=2.)
        operation, body = Extrude.create(self.component, self.sketch, 4, elements=["Edge2"], options=options)
        self.assertAlmostEqual(body.Shape.BoundBox.ZMax, 10)
        plane.Placement.Base = App.Vector(0, 0, 3)
        self.doc.recompute()
        self.assertAlmostEqual(body.Shape.BoundBox.ZMax, 13)
        options.update(extent="UpToShape", limit=(plane, []), offset=0.)
        operation = Extrude.edit(operation, self.sketch, 4, elements=["Edge2"], options=options)
        self.assertAlmostEqual(body.Shape.BoundBox.ZMax, 11)
        options.update(limit=(plane, ["Face1"]), offset=-1.)
        operation = Extrude.edit(operation, self.sketch, 4, elements=["Edge2"], options=options)
        self.assertAlmostEqual(body.Shape.BoundBox.ZMax, 10)
        self.assertEqual(Extent.read(operation)["limit"][0], plane)
        preview = Extrude.preview(self.component, self.sketch, 4, elements=["Edge2"], options=options)
        self.assertAlmostEqual(preview.Volume, body.Shape.Volume)
        options.update(start="Reference", start_reference=(plane, ["Face1"]), start_offset=-9.,
                       extent="Length", limit=None)
        operation = Extrude.edit(operation, self.sketch, 4, elements=["Edge2"], options=options)
        self.assertAlmostEqual(body.Shape.BoundBox.ZMin, 2)
        self.assertAlmostEqual(body.Shape.BoundBox.ZMax, 6)
        identity, name, plane_name = body.ObjectId, operation.Name, plane.Name
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "ExtentReferences.cadprt"
        self.doc.saveAs(str(output))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(output))
        self.doc.recompute()
        operation = self.doc.getObject(name)
        self.assertEqual(Extent.read(operation)["start_reference"][0].Name, plane_name)
        self.assertEqual(next(obj for obj in self.doc.Objects if getattr(obj, "Producer", None) == operation).ObjectId, identity)

    def testTargetExtentsAndRemovedVolume(self):
        box = self.target_box()
        for kind in ("UpToFirst", "UpToLast", "ThroughAll"):
            options = Extent.defaults()
            options.update(extent=kind)
            shape = Extrude.preview(self.component, self.sketch, 4, "Subtract", box,
                                    elements=["Edge2"], options=options)
            self.assertAlmostEqual(shape.Volume, box.Shape.Volume - 300 * math.pi)
            removed = Extrude.preview(self.component, self.sketch, 4, "Subtract", box,
                                      elements=["Edge2"], options=options, volume_only=True)
            self.assertAlmostEqual(removed.Volume, 300 * math.pi)
            with self.assertRaises(ValueError):
                Extrude.preview(self.component, self.sketch, 4, elements=["Edge2"], options=options)
        options = Extent.defaults()
        self.sketch.Placement.Base = App.Vector(0, 0, 12)
        self.doc.recompute()
        added = Extrude.preview(self.component, self.sketch, 4, "Add", box,
                                elements=["Edge2"], options=options, volume_only=True)
        self.assertAlmostEqual(added.Volume, 100 * math.pi)

    def testTaperDirectionAndInvalidLimits(self):
        options = Extent.defaults()
        options.update(taper=3.)
        shape = Extrude.preview(self.component, self.sketch, 4, elements=["Edge2"], options=options)
        self.assertNotAlmostEqual(shape.Volume, 100 * math.pi)
        options.update(taper=0., custom=True, direction=(0.5, 0., 1.), along_normal=True)
        shape = Extrude.preview(self.component, self.sketch, 4, elements=["Edge2"], options=options)
        self.assertAlmostEqual(shape.BoundBox.ZLength, 4)
        options.update(direction=(0., 0., 0.))
        with self.assertRaises(ValueError):
            Extrude.preview(self.component, self.sketch, 4, elements=["Edge2"], options=options)
        options = Extent.defaults()
        options.update(extent="UpToFace")
        with self.assertRaises(ValueError):
            Extrude.create(self.component, self.sketch, 4, elements=["Edge2"], options=options)
        self.assertFalse(any(getattr(obj, "OperationKind", "") == "Extrude" for obj in self.doc.Objects))

    def testPreviewColorsControlsAndCancel(self):
        from pivy import coin
        from PySide import QtCore
        module = task_module()
        box = self.target_box()
        box.ViewObject.Transparency = 12
        Gui.Selection.clearSelection()
        task = module.ExtrudeTask(self.component)
        Gui.Control.showDialog(task)
        task.start_selection()
        try:
            task.profile.setCurrentIndex(task.profile.findData(self.sketch.Name))
            task.set_curves(["Edge2"], False)
            self.assertTrue(task.preview(), task.status.text())
            material = task.ghost.node.getChild(2)
            self.assertEqual(tuple(material.diffuseColor[0]), (0., 1., 0.))
            self.assertEqual(task.ghost.node.getChild(1).style.getValue(), coin.SoDrawStyle.FILLED)
            task.view.viewAxonometric()
            task.view.fitAll()
            Gui.updateGui()
            output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
            Gui.getMainWindow().grab().save(str(output / "Extrude-green-volume.png"))
            task.mode.setCurrentIndex(task.mode.findData("Subtract"))
            task.target.setCurrentIndex(task.target.findData(box.Name))
            task.extent.setCurrentIndex(task.extent.findData("ThroughAll"))
            # Exercise the debounced automatic preview rather than pressing Preview.
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(500, loop.quit)
            loop.exec()
            self.assertIsNotNone(task.ghost, task.status.text())
            self.assertEqual(tuple(task.ghost.node.getChild(2).diffuseColor[0]), (1., 0., 0.))
            self.assertEqual(box.ViewObject.Transparency, 75)
            Gui.updateGui()
            Gui.getMainWindow().grab().save(str(output / "Extrude-red-volume.png"))
            task.sides.setCurrentIndex(task.sides.findData("Two sides"))
            self.assertTrue(task.extent2.isEnabled())
            task.sides.setCurrentIndex(task.sides.findData("Symmetric"))
            self.assertEqual(task.form.layout().labelForField(task.length).text(), "Total length")
            self.assertFalse(task.extent2.isEnabled())
            self.assertEqual(box.ViewObject.Transparency, 12)
            task.reject()
            self.assertFalse(task.observing)
            self.assertEqual(box.ViewObject.Transparency, 12)
        finally:
            if Gui.Control.activeDialog():
                task.reject()

    def testAssociativityEditUndoAndPersistence(self):
        self.sketch.addConstraint(Sketcher.Constraint("Radius", 0, 10.0))
        self.doc.recompute()
        operation, body = Extrude.create(self.component, self.sketch, 4, elements=["Edge1", "Edge2"])
        self.assertAlmostEqual(body.Shape.Volume, 300 * math.pi)
        identity, body_name, operation_name = body.ObjectId, body.Name, operation.Name
        self.sketch.setDatum(0, App.Units.Quantity("12 mm"))
        self.doc.recompute()
        self.assertAlmostEqual(body.Shape.Volume, 476 * math.pi)
        Extrude.edit(operation, self.sketch, 4, elements=["Edge2"])
        self.assertAlmostEqual(body.Shape.Volume, 100 * math.pi)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.getObject(body_name).Shape.Volume, 476 * math.pi)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.getObject(body_name).Shape.Volume, 100 * math.pi)
        with self.assertRaises(ValueError):
            Extrude.edit(self.doc.getObject(operation_name), self.sketch, 4, elements=["Edge1", "Edge3"])
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "CurveProfile.cadprt"
        self.doc.saveAs(str(output))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(output))
        self.doc.recompute()
        body = self.doc.getObject(body_name)
        self.assertEqual(body.ObjectId, identity)
        self.assertAlmostEqual(body.Shape.Volume, 100 * math.pi)
        source, elements = Profile.selection(Extrude.parameters(self.doc.getObject(operation_name))[0])
        self.assertEqual(elements, ["Edge2"])
        self.assertTrue(source.isDerivedFrom("Sketcher::SketchObject"))
        Model.validate(self.doc)

    def testTaskCollectorAndVisibility(self):
        module = task_module()
        Gui.Selection.clearSelection()
        self.sketch.Visibility = False
        task = module.ExtrudeTask(self.component)
        try:
            task.profile.setCurrentIndex(task.profile.findData(self.sketch.Name))
            self.assertTrue(self.sketch.Visibility)
            task.start_selection()
            Gui.Selection.addSelection(self.doc.Name, self.sketch.Name, "Edge1")
            Gui.Selection.addSelection(self.doc.Name, self.sketch.Name, "Edge2")
            Gui.updateGui()
            self.assertEqual(task.curve_names(), ["Edge1", "Edge2"],
                             str([(entry.Object.Name, entry.SubElementNames) for entry in Gui.Selection.getSelectionEx("*", 0)]) + " / " + task.status.text())
            task.curves.item(1).setSelected(True)
            task.remove_selected_curves()
            self.assertEqual(task.curve_names(), ["Edge1"])
            other = Sketch.create(self.component)
            task.use_selection([(self.sketch, "Edge1"), (other, "Edge1")])
            self.assertEqual(task.curve_names(), ["Edge1"])
            self.assertIn("same sketch", task.status.text())
            task.set_curves([], False)
            view = task.view
            view.viewTop()
            view.fitAll()
            Gui.updateGui()
            point = self.component.getGlobalPlacement().multVec(App.Vector(7, 0, 0))
            position = view.getPointOnViewport(point)
            task.pick_region({"State": "DOWN", "Button": "BUTTON1", "Position": position})
            self.assertEqual(task.curve_names(), ["Edge1", "Edge2"],
                             task.status.text() + " / " + str((position, view.getObjectInfo(position), self.sketch.Visibility)))
            self.assertTrue(task.preview(), task.status.text())
        finally:
            task.stop_selection()
            task.clear_preview()
            task.restore_profile_visibility()
        self.assertFalse(task.observing)
        self.assertIsNone(task.mouse_callback)
        self.assertFalse(self.sketch.Visibility)

    def testPlacedSketchRegionAndNativeAcceptance(self):
        module = task_module()
        self.component.Placement = App.Placement(App.Vector(80, 20, 10), App.Rotation(App.Vector(0, 0, 1), 25))
        self.sketch.Placement = App.Placement(App.Vector(10, 20, 30), App.Rotation(App.Vector(1, 0, 0), 90))
        self.doc.recompute()
        Gui.Selection.clearSelection()
        task = module.ExtrudeTask(self.component)
        Gui.Control.showDialog(task)
        task.start_selection()
        try:
            task.profile.setCurrentIndex(task.profile.findData(self.sketch.Name))
            task.set_curves([], False)
            frame = self.component.getGlobalPlacement().multiply(self.sketch.Placement)
            task.view.setCameraOrientation(frame.Rotation.Q)
            task.view.fitAll()
            Gui.updateGui()
            position = task.view.getPointOnViewport(frame.multVec(App.Vector(7, 0, 0)))
            task.pick_region({"State": "DOWN", "Button": "BUTTON1", "Position": position})
            self.assertEqual(task.curve_names(), ["Edge1", "Edge2"], task.status.text())
            Gui.Control.activeTaskDialog().accept()
            Gui.updateGui()
            self.assertIsNotNone(task.result)
            self.assertAlmostEqual(task.result.Shape.Volume, 750 * math.pi)
            bounds = task.result.Shape.BoundBox
            center = task.result.Shape.CenterOfMass
            self.assertLess((center - App.Vector(10, 15, 30)).Length, 1e-6, str((center, bounds)))
            # OCC's rotated circular bounds can include polygon approximation.
            for actual, expected in ((bounds.XMin, 0), (bounds.XMax, 20), (bounds.YMin, 10),
                                     (bounds.YMax, 20), (bounds.ZMin, 20), (bounds.ZMax, 40)):
                self.assertAlmostEqual(actual, expected, delta=0.05)
            self.assertFalse(self.sketch.Visibility)
            self.assertFalse(task.observing)
            self.assertFalse(Gui.Control.activeDialog())
        finally:
            task.stop_selection()
            task.clear_preview()
            if Gui.Control.activeDialog():
                task.reject()
