# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component Loft geometry, ordered selection, persistence and shared-task regressions."""
import hashlib
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentLoft as Loft
from freecad.gui import ComponentLoftTask as Task
from freecad.gui import ComponentOperationTask as Shared
from freecad.gui import ComponentNavigator as Navigator


class TestComponentLoft(unittest.TestCase):
    def setUp(self):
        root = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, folder in ((Loft, "src/Mod/Part"), (Task, "src/Gui"), (Shared, "src/Gui"), (Navigator, "src/Gui")):
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((root / folder / Path(module.__file__).name).read_bytes()).digest())
        Gui.activateWorkbench("PartDesignWorkbench")
        self.doc = Model.new_document("Loft acceptance")
        self.component = Model.metadata(self.doc).RootComponent
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])

    def tearDown(self):
        if Task._task:
            Task._task.reject()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def rectangle(self, z, left=0, right=4, bottom=0, top=4):
        sketch = Sketch.create(self.component, offset=z)
        points = [App.Vector(left, bottom, 0), App.Vector(right, bottom, 0), App.Vector(right, top, 0), App.Vector(left, top, 0)]
        for a, b in zip(points, points[1:] + points[:1]):
            sketch.addGeometry(Part.LineSegment(a, b))
        self.doc.recompute()
        return sketch

    def pair(self, left=0, right=4):
        return [(self.rectangle(z, left, right), None) for z in (0, 10)]

    def testModesNativeGeometryAndPreviewIsolation(self):
        sections = self.pair()
        count = len(self.doc.Objects)
        preview = Loft.preview(self.component, sections)
        self.assertEqual(len(self.doc.Objects), count)
        self.assertAlmostEqual(preview.Volume, 160)
        op, base = Loft.create(self.component, sections)
        self.assertEqual(op.TypeId, "PartDesign::AdditiveLoft")
        self.assertFalse(any(o.TypeId == "PartDesign::Body" for o in self.doc.Objects))
        tool = self.pair(2, 6)
        for mode, volume, kind in (("Add", 240, "PartDesign::AdditiveLoft"), ("Subtract", 80, "PartDesign::SubtractiveLoft")):
            count = len(self.doc.Objects)
            preview = Loft.preview(self.component, tool, mode, base)
            overlay = Loft.preview(self.component, tool, mode, base, volume_only=True)
            self.assertEqual(len(self.doc.Objects), count)
            operation, result = Loft.create(self.component, tool, mode, base)
            self.assertEqual(operation.TypeId, kind)
            self.assertAlmostEqual(result.Shape.Volume, volume)
            self.assertAlmostEqual(preview.Volume, volume)
            self.assertAlmostEqual(overlay.Volume, 80)
            self.assertAlmostEqual(base.Shape.Volume, 160)

    def testModeEditIdentityDownstreamUndoAndCadprt(self):
        _, base = Loft.create(self.component, self.pair())
        sections = self.pair(2, 6)
        options = dict(ruled=False, closed=False, refine=False, fuzzy=1e-6)
        operation, result = Loft.create(self.component, sections, "Add", base, options)
        identifier, result_id, name = operation.ObjectId, result.ObjectId, result.Name
        consumer = self.doc.addObject("Part::Mirroring", "Consumer")
        self.component.addObject(consumer)
        consumer.Source = result
        self.doc.recompute()
        operation = Loft.edit(operation, sections, "Subtract", base)
        self.assertEqual(operation.ObjectId, identifier)
        self.assertEqual(result.ObjectId, result_id)
        self.assertEqual(result.Producer, operation)
        self.assertAlmostEqual(operation.FuzzyTolerance, 1e-6)
        self.assertFalse(operation.Refine)
        self.assertAlmostEqual(consumer.Shape.Volume, 80)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.getObject(name).Shape.Volume, 240)
        self.doc.redo()
        self.doc.recompute()
        result = self.doc.getObject(name)
        self.assertAlmostEqual(result.Shape.Volume, 80)
        self.assertEqual(result.Producer.TypeId, "PartDesign::SubtractiveLoft")
        path = self.output / "component-loft.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        result = self.doc.getObject(name)
        self.assertEqual(result.ObjectId, result_id)
        self.assertEqual(result.Producer.ObjectId, identifier)
        self.assertEqual(Loft.read(result.Producer)[1], "Subtract")
        self.assertAlmostEqual(self.doc.getObject("Consumer").Shape.Volume, 80)

    def testSelectedCurvesRecomputeAndReorder(self):
        sections = self.pair()
        edges = ["Edge1", "Edge2", "Edge3", "Edge4"]
        for obj, elements in sections:
            obj.addGeometry(Part.LineSegment(App.Vector(20, 0, 0), App.Vector(21, 0, 0)))
        self.doc.recompute()
        sections = [(obj, edges) for obj, elements in sections]
        options = dict(ruled=True, closed=False, refine=False)
        preview = Loft.preview(self.component, sections, options=options)
        operation, result = Loft.create(self.component, sections, options=options)
        self.assertAlmostEqual(result.Shape.Volume, 160)
        self.assertLess(preview.cut(result.Shape).Volume, 1e-7)
        self.assertEqual(Loft.read(operation)[0], sections)
        operation = Loft.edit(operation, list(reversed(sections)), "New Body", options=options)
        self.assertEqual(Loft.read(operation)[0], list(reversed(sections)))
        self.assertAlmostEqual(result.Shape.Volume, 160)
        sketch = sections[1][0]
        offset = sketch.AttachmentOffset
        offset.Base.z = 15
        sketch.AttachmentOffset = offset
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 240)
        self.assertFalse(operation.Refine)
        self.assertTrue(operation.Ruled)

    def testInvalidEditRollsBackAndRejectsCycles(self):
        _, base = Loft.create(self.component, self.pair())
        sections = self.pair(2, 6)
        operation, result = Loft.create(self.component, sections, "Subtract", base)
        distant = self.pair(20, 24)
        count = len(self.doc.Objects)
        with self.assertRaises(ValueError):
            Loft.edit(operation, distant, "Subtract", base)
        self.assertEqual(len(self.doc.Objects), count)
        self.assertAlmostEqual(result.Shape.Volume, 80)
        self.assertEqual(Loft.read(operation)[0], sections)
        with self.assertRaises(ValueError):
            Loft.edit(operation, sections, "Subtract", result)
        for bad in ([], sections[:1], [sections[0], sections[0]]):
            with self.assertRaises(ValueError):
                Loft.create(self.component, bad)
        with self.assertRaises(ValueError):
            Loft.create(self.component, sections, options=dict(ruled=False, closed=True, refine=True))
        self.assertEqual(len(self.doc.Objects), count)

    def testTaskPreselectionOrderPreviewAndHistory(self):
        sections = self.pair()
        Gui.Selection.clearSelection()
        for obj, elements in sections:
            Gui.Selection.addSelection(obj)
        task = Task.launch()
        task.auto_preview.setChecked(False)
        self.assertEqual(task.ordered.count(), 2)
        self.assertEqual([button.isChecked() for button, body, layout in task.sections], [True, True, False, True])
        self.assertTrue(task.target.isHidden())
        self.assertEqual(task.preview_mode.currentData(), "Overlay")
        self.assertTrue(task.preview(), task.status.text())
        self.assertEqual(tuple(task.ghost.node.getChild(2).diffuseColor[0].getValue()), (0., 0., 1.))
        task.ordered.setCurrentRow(1)
        task.move_section(-1)
        self.assertEqual(task.values()[0][0][0], sections[1][0])
        task.reverse_sections()
        self.assertEqual(task.values()[0], sections)
        task.preview_mode.setCurrentIndex(task.preview_mode.findData("None"))
        self.assertIsNone(task.ghost)
        self.assertFalse(task.preview_timer.isActive())
        task.preview_mode.setCurrentIndex(task.preview_mode.findData("Final Result"))
        self.assertTrue(task.preview(), task.status.text())
        self.assertTrue(task.accept())
        operation = task.operation
        dock = Navigator._dock
        self.assertIsNotNone(dock)
        dock.edit_history(Navigator.object_key(operation))
        self.assertIsInstance(Task._task, Task.LoftTask)
        self.assertEqual(Task._task.values()[0], sections)
        Task._task.auto_preview.setChecked(False)
        Gui.updateGui()
        Task._task.form.resize(390, 900)
        Task._task.form.grab().save(str(self.output / "loft-task.png"))
        Task._task.reject()

    def testTaskColorsCancelAndFailedAcceptanceRecovery(self):
        _, base = Loft.create(self.component, self.pair())
        sections = self.pair(2, 6)
        for mode, color in (("Add", (0., 1., 0.)), ("Subtract", (1., 0., 0.))):
            display = Model.display_object(base)
            visible, transparency = display.Visibility, display.ViewObject.Transparency
            task = Task.launch(preset=mode)
            task.auto_preview.setChecked(False)
            task.clear_sections()
            self.assertFalse(task.accept())
            self.assertIs(Task._task, task)
            for obj, elements in sections:
                task.profile.setCurrentIndex(task.profile.findData(obj.Name))
                task.append_section()
            task.target.setCurrentIndex(task.target.findData(base.Name))
            self.assertFalse(task.target.isHidden())
            self.assertTrue(task.preview(), task.status.text())
            self.assertEqual(tuple(task.ghost.node.getChild(2).diffuseColor[0].getValue()), color)
            task.preview_mode.setCurrentIndex(task.preview_mode.findData("Final Result"))
            self.assertTrue(task.preview(), task.status.text())
            self.assertFalse(display.Visibility)
            task.reject()
            self.assertEqual(display.Visibility, visible)
            self.assertEqual(display.ViewObject.Transparency, transparency)

    def testNativeCommandRouting(self):
        for command, mode in (("PartDesign_AdditiveLoft", "New Body"), ("PartDesign_SubtractiveLoft", "Subtract")):
            Gui.runCommand(command)
            self.assertIsInstance(Task._task, Task.LoftTask)
            self.assertEqual(Task._task.mode.currentData(), mode)
            Task._task.reject()

    def testPlacedSectionsAndNativeVertexTip(self):
        sections = [(self.rectangle(z), None) for z in (5, 15)]
        preview = Loft.preview(self.component, sections)
        operation, result = Loft.create(self.component, sections)
        self.assertAlmostEqual(preview.Volume, 160)
        self.assertAlmostEqual(preview.BoundBox.ZMin, 5)
        self.assertAlmostEqual(result.Shape.BoundBox.ZMin, 5)
        self.assertLess(preview.cut(result.Shape).Volume, 1e-7)
        tip = self.rectangle(15, 2, 6, 2, 6)
        sections = [(sections[0][0], None), (tip, ["Vertex1"])]
        preview = Loft.preview(self.component, sections)
        operation, result = Loft.create(self.component, sections)
        self.assertAlmostEqual(result.Shape.Volume, 160 / 3)
        self.assertAlmostEqual(preview.Volume, result.Shape.Volume)
        self.assertEqual(Loft.read(operation)[0], sections)

    def testClosedNativeSectionsAndExpressionProtection(self):
        sections = []
        for plane, x in (("XZ plane", -40), ("YZ plane", -40), ("XZ plane", 40), ("YZ plane", 40)):
            sketch = Sketch.create(self.component, plane=plane)
            sketch.addGeometry(Part.Circle(App.Vector(x, 0, 0), App.Vector(0, 0, 1), 10))
            sections.append((sketch, None))
        self.doc.recompute()
        options = dict(ruled=False, closed=True, refine=True)
        preview = Loft.preview(self.component, sections, options=options)
        operation, result = Loft.create(self.component, sections, options=options)
        self.assertGreater(result.Shape.Volume, 80000)
        self.assertAlmostEqual(preview.Volume, result.Shape.Volume)
        self.assertTrue(Loft.read(operation)[3]["closed"])
        operation.setExpression("Refine", "1 == 1")
        self.doc.recompute()
        with self.assertRaises(ValueError):
            Loft.edit(operation, sections, "New Body", options=options)
        self.assertTrue(operation.ExpressionEngine)
