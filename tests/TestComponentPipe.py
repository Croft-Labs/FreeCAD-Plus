# SPDX-License-Identifier: LGPL-2.1-or-later
"""Unified Pipe acceptance using real native geometry and Tasks controls."""
import hashlib
import math
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentPipe as Pipe
import ComponentNativeOperation as Native
from freecad.gui import ComponentPipeTask as Task
from freecad.gui import ComponentSectionTask as Sections
from freecad.gui import ComponentNavigator as Navigator


class TestComponentPipe(unittest.TestCase):
    def setUp(self):
        root = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, folder in ((Pipe, "src/Mod/Part"), (Native, "src/Mod/Part"), (Task, "src/Gui"), (Sections, "src/Gui"), (Navigator, "src/Gui")):
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((root / folder / Path(module.__file__).name).read_bytes()).digest())
        Gui.activateWorkbench("PartDesignWorkbench")
        self.doc = Model.new_document("Pipe acceptance")
        self.component = Model.metadata(self.doc).RootComponent
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])

    def tearDown(self):
        if Task._task:
            Task._task.reject()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def rectangle(self, left=0, right=4, z=0):
        sketch = Sketch.create(self.component, offset=z)
        points = [App.Vector(left, 0, 0), App.Vector(right, 0, 0), App.Vector(right, 4, 0), App.Vector(left, 4, 0)]
        for a, b in zip(points, points[1:] + points[:1]):
            sketch.addGeometry(Part.LineSegment(a, b))
        self.doc.recompute()
        return sketch

    def circle(self, radius=1, z=0):
        sketch = Sketch.create(self.component, offset=z)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), radius))
        self.doc.recompute()
        return sketch

    def path(self, x=0, length=10, bent=False):
        path = self.doc.addObject("Part::Feature", "Path")
        points = [App.Vector(x, 0, 0), App.Vector(x, 0, length)]
        if bent:
            points.append(App.Vector(x + 10, 0, length))
        path.Shape = Part.makePolygon(points)
        Model.register_object(self.component, path)
        self.doc.recompute()
        return path

    def options(self, path=None, **values):
        options = Pipe.defaults()
        options.update(spine=(path or self.path(), []))
        options.update(values)
        return options

    def testGeometryModesPreviewAndCommon(self):
        sections = [(self.rectangle(), None)]
        options = self.options()
        count = len(self.doc.Objects)
        preview = Pipe.preview(self.component, sections, options=options)
        self.assertAlmostEqual(preview.Volume, 160)
        self.assertEqual(len(self.doc.Objects), count)
        operation, base = Pipe.create(self.component, sections, options=options)
        self.assertEqual(operation.TypeId, "PartDesign::AdditivePipe")
        self.assertFalse(any(o.TypeId == "PartDesign::Body" for o in self.doc.Objects))
        sections = [(self.rectangle(2, 6), None)]
        for mode, boolean, volume in (("Add", "Subtraction", 240), ("Subtract", "Subtraction", 80), ("Subtract", "Common", 80)):
            options["boolean"] = boolean
            preview = Pipe.preview(self.component, sections, mode, base, options)
            overlay = Pipe.preview(self.component, sections, mode, base, options, volume_only=True)
            operation, result = Pipe.create(self.component, sections, mode, base, options)
            self.assertAlmostEqual(result.Shape.Volume, volume)
            self.assertAlmostEqual(preview.Volume, volume)
            self.assertAlmostEqual(overlay.Volume, 80)
            self.assertAlmostEqual(base.Shape.Volume, 160)
            self.assertEqual(operation.Operation, boolean if mode == "Subtract" else "Union")

    def testModeEditIdentityUndoAndCadprt(self):
        options = self.options()
        _, base = Pipe.create(self.component, [(self.rectangle(), None)], options=options)
        sections = [(self.rectangle(2, 6), None)]
        options.update(fuzzy=1e-6, refine=False)
        operation, result = Pipe.create(self.component, sections, "Add", base, options)
        oid, rid, name = operation.ObjectId, result.ObjectId, result.Name
        consumer = self.doc.addObject("Part::Mirroring", "Consumer")
        self.component.addObject(consumer)
        consumer.Source = result
        self.doc.recompute()
        operation = Pipe.edit(operation, sections, "Subtract", base)
        self.assertEqual(operation.ObjectId, oid)
        self.assertEqual(result.ObjectId, rid)
        self.assertAlmostEqual(operation.FuzzyTolerance, 1e-6)
        self.assertFalse(operation.Refine)
        self.assertAlmostEqual(consumer.Shape.Volume, 80)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.getObject(name).Shape.Volume, 240)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.getObject(name).Shape.Volume, 80)
        options["spine"][0].Shape = Part.makePolygon([App.Vector(), App.Vector(0, 0, 12)])
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.getObject("Consumer").Shape.Volume, 96)
        path = self.output / "component-pipe.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        result = self.doc.getObject(name)
        self.assertEqual(result.ObjectId, rid)
        self.assertEqual(result.Producer.ObjectId, oid)
        self.assertEqual(result.Producer.TypeId, "PartDesign::SubtractivePipe")
        self.assertAlmostEqual(self.doc.getObject("Consumer").Shape.Volume, 96)

    def testOrientationTransitionsAndPathSubsets(self):
        profile, path, auxiliary = self.circle(), self.path(), self.path(x=5)
        for mode in Pipe.ORIENTATIONS:
            options = self.options(path, orientation=mode, auxiliary=(auxiliary, []), binormal=(1., 0., 0.))
            preview = Pipe.preview(self.component, [(profile, None)], options=options)
            operation, result = Pipe.create(self.component, [(profile, None)], options=options)
            # Native auxiliary transport approximates the circular surface.
            self.assertAlmostEqual(result.Shape.Volume, 10 * math.pi, delta=0.05 if mode == "Auxiliary" else 1e-6, msg=mode)
            self.assertAlmostEqual(preview.Volume, result.Shape.Volume)
            self.assertEqual(Pipe.read(operation)[3]["orientation"], mode)
        bent = self.path(bent=True)
        for transition in Pipe.TRANSITIONS:
            options = self.options(bent, transition=transition)
            operation, result = Pipe.create(self.component, [(profile, None)], options=options)
            self.assertTrue(result.Shape.isValid())
            self.assertGreater(result.Shape.Volume, 0)
            preview = Pipe.preview(self.component, [(profile, None)], options=options)
            self.assertAlmostEqual(preview.Volume, result.Shape.Volume, places=6)
            self.assertGreater(result.Shape.BoundBox.XMax, 9)
            self.assertGreater(result.Shape.BoundBox.ZMax, 9)
            self.assertEqual(operation.Transition, transition)
        options = self.options(bent)
        options["spine"] = (bent, ["Edge1"])
        operation, result = Pipe.create(self.component, [(profile, None)], options=options)
        self.assertAlmostEqual(result.Shape.Volume, 10 * math.pi)
        self.assertEqual(list(operation.Spine[1]), ["Edge1"])

    def testMultisectionSubsetAssociationAndUnsupportedPoint(self):
        first, last = self.circle(1), self.circle(2, 10)
        first.addGeometry(Part.LineSegment(App.Vector(20, 0, 0), App.Vector(21, 0, 0)))
        self.doc.recompute()
        sections = [(first, ["Edge1"]), (last, None)]
        options = self.options(transformation="Multisection")
        preview = Pipe.preview(self.component, sections, options=options)
        operation, result = Pipe.create(self.component, sections, options=options)
        self.assertAlmostEqual(result.Shape.Volume, 70 * math.pi / 3, places=6)
        self.assertAlmostEqual(preview.Volume, result.Shape.Volume)
        self.assertEqual(Pipe.read(operation)[0], sections)
        options["transformation"] = "Constant"
        operation = Pipe.edit(operation, sections, "New Body", options=options)
        self.assertAlmostEqual(result.Shape.Volume, 10 * math.pi)
        self.assertEqual(len(operation.Sections), 1)
        options["transformation"] = "Multisection"
        operation = Pipe.edit(operation, sections, "New Body", options=options)
        self.assertAlmostEqual(result.Shape.Volume, 70 * math.pi / 3, places=6)
        import Sketcher
        last.addConstraint(Sketcher.Constraint("Radius", 0, 3.))
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 130 * math.pi / 3, places=6)
        tip = self.rectangle(0, 4, 10)
        vertex_sections = [(first, ["Edge1"]), (tip, ["Vertex1"])]
        with self.assertRaisesRegex(ValueError, "point-ended"):
            Pipe.create(self.component, vertex_sections, options=options)
        self.assertAlmostEqual(result.Shape.Volume, 130 * math.pi / 3, places=6)

    def testInvalidRollbackCyclesAndExpressions(self):
        options = self.options()
        _, base = Pipe.create(self.component, [(self.rectangle(), None)], options=options)
        sections = [(self.rectangle(2, 6), None)]
        operation, result = Pipe.create(self.component, sections, "Subtract", base, options)
        distant = [(self.rectangle(20, 24), None)]
        count = len(self.doc.Objects)
        with self.assertRaises(ValueError):
            Pipe.edit(operation, distant, "Subtract", base)
        self.assertEqual(len(self.doc.Objects), count)
        self.assertEqual(Pipe.read(operation)[0], sections)
        self.assertAlmostEqual(result.Shape.Volume, 80)
        with self.assertRaises(ValueError):
            Pipe.edit(operation, sections, "Subtract", result)
        for changes in (dict(spine=None), dict(orientation="Auxiliary"), dict(orientation="Binormal", binormal=(0., 0., 0.)), dict(transformation="Linear")):
            invalid = dict(options, **changes)
            with self.assertRaises(ValueError):
                Pipe.preview(self.component, sections, "Subtract", base, invalid)
        operation.setExpression("Refine", "1 == 1")
        self.doc.recompute()
        with self.assertRaises(ValueError):
            Pipe.edit(operation, sections, "Subtract", base)
        self.assertTrue(operation.ExpressionEngine)

    def testTaskPreselectionHistoryAndCollectors(self):
        profile, path = self.circle(), self.path(bent=True)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(profile)
        Gui.Selection.addSelection(path, "Edge1")
        task = Task.launch()
        task.auto_preview.setChecked(False)
        self.assertEqual([b.isChecked() for b, host, form in task.sections], [True, True, False, True])
        self.assertEqual(task.ordered.count(), 1)
        self.assertEqual(task.path_value("spine"), (path, ["Edge1"]))
        self.assertTrue(task.target.isHidden())
        self.assertEqual(task.preview_mode.currentData(), "Overlay")
        self.assertTrue(task.preview(), task.status.text())
        self.assertEqual(tuple(task.ghost.node.getChild(2).diffuseColor[0].getValue()), (0., 0., 1.))
        task.set_role("spine")
        task.addSelection(self.doc.Name, path.Name, "Edge2")
        self.assertEqual(task.path_value("spine"), (path, ["Edge1", "Edge2"]))
        self.assertEqual(task.ordered.count(), 1)
        task.set_role(None)
        task.preview_mode.setCurrentIndex(task.preview_mode.findData("None"))
        self.assertIsNone(task.ghost)
        self.assertFalse(task.preview_timer.isActive())
        self.assertTrue(task.accept())
        operation = task.operation
        Navigator.show(self.doc).edit_history(Navigator.object_key(task.result))
        task = Task._task
        task.auto_preview.setChecked(False)
        self.assertEqual(task.operation, operation)
        self.assertEqual(task.path_value("spine"), (path, ["Edge1", "Edge2"]))
        Gui.updateGui()
        task.form.grab().save(str(self.output / "pipe-task.png"))
        task.sections[2][0].setChecked(True)
        task.orientation.setCurrentIndex(task.orientation.findData("Auxiliary"))
        Gui.updateGui()
        task.form.grab().save(str(self.output / "pipe-advanced.png"))
        task.reject()

    def testTaskColorsCancelAndRecovery(self):
        options = self.options()
        _, base = Pipe.create(self.component, [(self.rectangle(), None)], options=options)
        profile = self.rectangle(2, 6)
        for mode, color in (("Add", (0., 1., 0.)), ("Subtract", (1., 0., 0.))):
            display = Model.display_object(base)
            visible, transparency = display.Visibility, display.ViewObject.Transparency
            Gui.Selection.clearSelection()
            task = Task.launch(preset=mode)
            task.auto_preview.setChecked(False)
            self.assertFalse(task.accept())
            self.assertIs(Task._task, task)
            task.profile.setCurrentIndex(task.profile.findData(profile.Name))
            task.append_section()
            task.set_path("spine", *options["spine"])
            task.target.setCurrentIndex(task.target.findData(base.Name))
            self.assertTrue(task.preview(), task.status.text())
            self.assertEqual(tuple(task.ghost.node.getChild(2).diffuseColor[0].getValue()), color)
            task.preview_mode.setCurrentIndex(task.preview_mode.findData("Final Result"))
            self.assertTrue(task.preview(), task.status.text())
            self.assertFalse(display.Visibility)
            task.reject()
            self.assertEqual(display.Visibility, visible)
            self.assertEqual(display.ViewObject.Transparency, transparency)

    def testNativeCommandRouting(self):
        for command, mode in (("PartDesign_AdditivePipe", "New Body"), ("PartDesign_SubtractivePipe", "Subtract")):
            Gui.runCommand(command)
            self.assertIsInstance(Task._task, Task.PipeTask)
            self.assertEqual(Task._task.mode.currentData(), mode)
            Task._task.reject()
