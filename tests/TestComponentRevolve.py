# SPDX-License-Identifier: LGPL-2.1-or-later
"""Unified Revolve geometry, history identity, persistence and Tasks acceptance."""
import hashlib
import math
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentProfile as Profile
import ComponentRevolve as Revolve
from freecad.gui import ComponentRevolveTask as Task
from freecad.gui import ComponentNavigator as Navigator


class TestComponentRevolve(unittest.TestCase):
    def setUp(self):
        root = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, folder in ((Revolve, "src/Mod/Part"), (Profile, "src/Mod/Part"), (Task, "src/Gui"), (Navigator, "src/Gui")):
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((root / folder / Path(module.__file__).name).read_bytes()).digest())
        Gui.activateWorkbench("PartDesignWorkbench")
        self.doc = Model.new_document("Revolve acceptance")
        self.component = Model.metadata(self.doc).RootComponent
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])

    def tearDown(self):
        if Task._task:
            Task._task.reject()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def rectangle(self, left=2, right=4, bottom=0, top=3):
        sketch = Sketch.create(self.component)
        points = [App.Vector(left, bottom, 0), App.Vector(right, bottom, 0), App.Vector(right, top, 0), App.Vector(left, top, 0)]
        for first, second in zip(points, points[1:] + points[:1]):
            sketch.addGeometry(Part.LineSegment(first, second))
        self.doc.recompute()
        return sketch

    def testNativeGeometryAndPreviews(self):
        profile = self.rectangle()
        count = len(self.doc.Objects)
        shape = Revolve.preview(self.component, profile, 360)
        self.assertAlmostEqual(shape.Volume, 36 * math.pi)
        self.assertEqual(len(self.doc.Objects), count)
        operation, body = Revolve.create(self.component, profile, 360)
        self.assertEqual(operation.TypeId, "PartDesign::Revolution")
        self.assertFalse(any(obj.TypeId == "PartDesign::Body" for obj in self.doc.Objects))
        self.assertAlmostEqual(body.Shape.Volume, shape.Volume)
        cutter = self.rectangle(2, 3)
        for mode, expected in (("Subtract", 21 * math.pi),):
            preview = Revolve.preview(self.component, cutter, 360, mode, body)
            cut, result = Revolve.create(self.component, cutter, 360, mode, body)
            self.assertEqual(cut.TypeId, "PartDesign::Groove")
            self.assertAlmostEqual(result.Shape.Volume, expected)
            self.assertAlmostEqual(preview.Volume, result.Shape.Volume)
        addition = self.rectangle(3, 5)
        add, added = Revolve.create(self.component, addition, 360, "Add", result)
        self.assertEqual(add.TypeId, "PartDesign::Revolution")
        self.assertAlmostEqual(added.Shape.Volume, 48 * math.pi)

    def testEditTypeIdentityRollbackUndoAndReopen(self):
        base_profile = self.rectangle()
        base_op, base = Revolve.create(self.component, base_profile, 360)
        profile = self.rectangle(3, 5)
        operation, result = Revolve.create(self.component, profile, 180, "Add", base)
        identifier, result_id, name = operation.ObjectId, result.ObjectId, result.Name
        operation = Revolve.edit(operation, profile, 180, "Subtract", base)
        self.assertEqual(operation.TypeId, "PartDesign::Groove")
        self.assertEqual(operation.ObjectId, identifier)
        self.assertEqual(result.ObjectId, result_id)
        self.assertEqual(result.Producer, operation)
        volume = result.Shape.Volume
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(self.doc.getObject(name).Producer.TypeId, "PartDesign::Revolution")
        self.doc.redo()
        self.doc.recompute()
        result = self.doc.getObject(name)
        operation = result.Producer
        self.assertEqual(operation.TypeId, "PartDesign::Groove")
        self.assertEqual(operation.ObjectId, identifier)
        self.assertAlmostEqual(result.Shape.Volume, volume)
        distant = self.rectangle(10, 12)
        objects = len(self.doc.Objects)
        with self.assertRaises(ValueError):
            Revolve.edit(operation, distant, 180, "Subtract", base)
        self.assertEqual(len(self.doc.Objects), objects)
        self.assertAlmostEqual(result.Shape.Volume, volume)
        self.assertEqual(Profile.selection(operation)[0], profile)
        path = self.output / "unified-revolve.FCStd"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        result = self.doc.getObject(name)
        self.assertEqual(result.ObjectId, result_id)
        self.assertEqual(result.Producer.ObjectId, identifier)
        self.assertEqual(result.Producer.TypeId, "PartDesign::Groove")
        self.assertAlmostEqual(result.Shape.Volume, volume)

    def testSubsetAngularOffsetsAndAxes(self):
        profile = self.rectangle()
        profile.addGeometry(Part.LineSegment(App.Vector(10, 0, 0), App.Vector(12, 0, 0)))
        self.doc.recompute()
        elements = ["Edge1", "Edge2", "Edge3", "Edge4"]
        for sides, total in (("One side", 90), ("Two sides", 135), ("Symmetric", 90)):
            for reverse in (False, True):
                options = Revolve.defaults()
                options.update(sides=sides, angle2=45, start="Offset", start_offset=-30)
                preview = Revolve.preview(self.component, profile, 90, reverse=reverse, elements=elements, options=options)
                operation, body = Revolve.create(self.component, profile, 90, reverse=reverse, elements=elements, options=options)
                self.assertAlmostEqual(body.Shape.Volume, 36 * math.pi * total / 360)
                self.assertAlmostEqual(preview.Volume, body.Shape.Volume)
                self.assertLess(preview.cut(body.Shape).Volume, 1e-7)
                self.assertEqual(Profile.selection(operation), (profile, elements))
                self.assertEqual(Revolve.read(operation)["start_offset"], -30)
        options = Revolve.defaults()
        options.update(axis="Reference", axis_reference=(profile, ["Edge4"]))
        operation, body = Revolve.create(self.component, profile, 180, elements=elements, options=options)
        self.assertAlmostEqual(body.Shape.Volume, 6 * math.pi)
        self.assertAlmostEqual(Revolve.preview(self.component, profile, 180, elements=elements, options=options).Volume, body.Shape.Volume)

    def testTaskSectionsPreviewAndEdit(self):
        profile = self.rectangle()
        before = len(self.doc.Objects)
        task = Task.launch()
        task.auto_preview.setChecked(False)
        self.assertEqual([button.isChecked() for button, body, layout in task.sections], [True, True, False, True])
        self.assertTrue(task.target.isHidden())
        self.assertEqual(task.preview_mode.currentData(), "Overlay")
        task.profile.setCurrentIndex(task.profile.findData(profile.Name))
        self.assertTrue(task.preview(), task.status.text())
        self.assertEqual(tuple(task.ghost.node.getChild(2).diffuseColor[0].getValue()), (0., 0., 1.))
        self.assertEqual(len(self.doc.Objects), before)
        task.preview_mode.setCurrentIndex(task.preview_mode.findData("None"))
        self.assertIsNone(task.ghost)
        self.assertFalse(task.preview_timer.isActive())
        task.preview_mode.setCurrentIndex(task.preview_mode.findData("Final Result"))
        self.assertTrue(task.preview(), task.status.text())
        task.offset.setProperty("rawValue", 25.)
        self.assertEqual(task.start.currentData(), "Offset")
        task.start.setCurrentIndex(task.start.findData("Profile plane"))
        self.assertEqual(task.offset.property("rawValue"), 0.)
        task.offset.setProperty("rawValue", 25.)
        task.offset_reverse.click()
        self.assertEqual(task.offset.property("rawValue"), -25.)
        task.angle.setProperty("rawValue", 180.)
        Gui.updateGui()
        task.form.grab().save(str(self.output / "revolve-task.png"))
        if not task.accept():
            self.fail(task.status.text())
        operation, result = task.operation, task.result
        panel = Navigator.show(self.doc)
        panel.edit_history(Navigator.object_key(result))
        task = Task._task
        self.assertIsNotNone(task)
        self.assertEqual(task.operation, operation)
        self.assertEqual(task.angle.property("rawValue"), 180.)
        self.assertEqual(task.offset.property("rawValue"), -25.)
        self.assertTrue(task.preview(), task.status.text())
        task.reject()
        self.assertIsNone(Task._task)
        self.assertTrue(result.Visibility)

    def testReferenceFramesAndStartReference(self):
        profile = self.rectangle()
        reference = self.doc.addObject("Part::Feature", "StartReference")
        reference.Shape = Part.Face(Part.makePolygon([App.Vector(0, -1, -1), App.Vector(0, 4, -1), App.Vector(0, 4, -5), App.Vector(0, -1, -5), App.Vector(0, -1, -1)]))
        Model.register_object(self.component, reference)
        self.doc.recompute()
        options = Revolve.defaults()
        options.update(start="Reference", start_reference=(reference, ["Face1"]), start_offset=15)
        shape = Revolve.preview(self.component, profile, 30, options=options)
        operation, result = Revolve.create(self.component, profile, 30, options=options)
        self.assertLess(shape.cut(result.Shape).Volume, 1e-7)
        self.assertAlmostEqual(result.Shape.Volume, 3 * math.pi)
        for axis in self.component.Origin.OriginFeatures:
            if getattr(axis, "Role", "") == "Y_Axis":
                options = Revolve.defaults()
                options.update(axis="Reference", axis_reference=(axis, [""]))
                shape = Revolve.preview(self.component, profile, 90, options=options)
                operation, result = Revolve.create(self.component, profile, 90, options=options)
                self.assertLess(shape.cut(result.Shape).Volume, 1e-7)
                self.assertAlmostEqual(shape.Volume, result.Shape.Volume)
                break
        else:
            self.fail("Component Y origin axis missing")

    def testPreviewColorsVisibilityAndCancel(self):
        profile = self.rectangle()
        operation, body = Revolve.create(self.component, profile, 360)
        cutter = self.rectangle(3, 5)
        for mode, color in (("Add", (0., 1., 0.)), ("Subtract", (1., 0., 0.))):
            display = Model.display_object(body)
            visibility, transparency = display.Visibility, display.ViewObject.Transparency
            task = Task.launch(preset=mode)
            task.auto_preview.setChecked(False)
            task.profile.setCurrentIndex(task.profile.findData(cutter.Name))
            task.target.setCurrentIndex(task.target.findData(body.Name))
            self.assertFalse(task.target.isHidden())
            task.angle.setProperty("rawValue", 90.)
            self.assertTrue(task.preview(), task.status.text())
            self.assertEqual(tuple(task.ghost.node.getChild(2).diffuseColor[0].getValue()), color)
            task.preview_mode.setCurrentIndex(task.preview_mode.findData("Final Result"))
            self.assertTrue(task.preview(), task.status.text())
            self.assertFalse(display.Visibility)
            task.reject()
            self.assertEqual(display.Visibility, visibility)
            self.assertEqual(display.ViewObject.Transparency, transparency)

    def testNativeCommandRouting(self):
        self.rectangle()
        for command, mode in (("PartDesign_Revolution", "New Body"), ("PartDesign_Groove", "Subtract")):
            Gui.runCommand(command)
            self.assertIsNotNone(Task._task)
            self.assertEqual(Task._task.mode.currentData(), mode)
            Task._task.reject()
