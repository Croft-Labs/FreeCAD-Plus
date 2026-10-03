# SPDX-License-Identifier: LGPL-2.1-or-later
"""Unified Helix acceptance with the real native engine and Tasks controls."""
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
import ComponentHelix as Helix
import ComponentNativeOperation as Native
from freecad.gui import ComponentHelixTask as Task
from freecad.gui import ComponentOperationTask as Shared
from freecad.gui import ComponentNavigator as Navigator


class TestComponentHelix(unittest.TestCase):
    def setUp(self):
        root = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, folder in ((Helix, "src/Mod/Part"), (Native, "src/Mod/Part"), (Task, "src/Gui"), (Shared, "src/Gui"), (Navigator, "src/Gui")):
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((root / folder / Path(module.__file__).name).read_bytes()).digest())
        Gui.activateWorkbench("PartDesignWorkbench")
        self.doc = Model.new_document("Helix acceptance")
        self.component = Model.metadata(self.doc).RootComponent
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])

    def tearDown(self):
        if Task._task:
            Task._task.reject()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def profile(self, x=2):
        profile = Sketch.create(self.component)
        points = [App.Vector(x, 0, 0), App.Vector(x + 1, 0, 0), App.Vector(x + 1, 1, 0), App.Vector(x, 1, 0)]
        for a, b in zip(points, points[1:] + points[:1]):
            profile.addGeometry(Part.LineSegment(a, b))
        self.doc.recompute()
        return profile

    def options(self, **values):
        options = Helix.defaults()
        options.update(pitch=3., height=6., turns=2.)
        options.update(values)
        return options

    def target(self):
        producer = self.doc.addObject("Part::Feature", "Cylinder")
        producer.Shape = Part.makeCylinder(2.5, 10, App.Vector(0, -1, 0), App.Vector(0, 1, 0))
        Model.register_object(self.component, producer, "Operation")
        result = Model.publish_result(self.component, producer)
        self.doc.recompute()
        return result

    def testNativeParameterModesAndDirection(self):
        sections = [(self.profile(), None)]
        for mode in Helix.INPUT_MODES:
            options = self.options(input_mode=mode)
            preview = Helix.preview(self.component, sections, options=options)
            operation, result = Helix.create(self.component, sections, options=options)
            self.assertAlmostEqual(result.Shape.Volume, 10 * math.pi, places=3)
            self.assertAlmostEqual(preview.Volume, result.Shape.Volume, places=6)
            self.assertEqual(operation.Mode, mode)
            self.assertAlmostEqual(operation.Pitch.Value, 3.)
            self.assertAlmostEqual(operation.Height.Value, 6.)
            self.assertAlmostEqual(operation.Turns, 2.)
        for left, reverse in ((True, False), (False, True), (True, True)):
            operation, result = Helix.create(self.component, sections, options=self.options(left=left, reversed=reverse))
            self.assertAlmostEqual(result.Shape.Volume, 10 * math.pi, places=3)
            self.assertEqual(operation.LeftHanded, left)
            self.assertEqual(operation.Reversed, reverse)
            if reverse:
                self.assertLess(result.Shape.BoundBox.YMin, -5)
        for values in (dict(angle=10.), dict(input_mode=Helix.INPUT_MODES[3], height=0., growth=2., turns=2.)):
            options = self.options(**values)
            preview = Helix.preview(self.component, sections, options=options)
            _, result = Helix.create(self.component, sections, options=options)
            self.assertTrue(result.Shape.isValid())
            self.assertAlmostEqual(result.Shape.Volume, preview.Volume, places=6)
        self.assertFalse(any(obj.TypeId == "PartDesign::Body" for obj in self.doc.Objects))

    def testBooleansPreviewsAndCommon(self):
        sections, base = [(self.profile(), None)], self.target()
        options = self.options()
        original = base.Shape.Volume
        count = len(self.doc.Objects)
        tool = Helix.preview(self.component, sections, options=options)
        self.assertEqual(len(self.doc.Objects), count)
        for mode, boolean in (("Add", "Subtraction"), ("Subtract", "Subtraction"), ("Subtract", "Common")):
            options["boolean"] = boolean
            expected = base.Shape.fuse(tool) if mode == "Add" else base.Shape.common(tool) if boolean == "Common" else base.Shape.cut(tool)
            preview = Helix.preview(self.component, sections, mode, base, options)
            overlay = Helix.preview(self.component, sections, mode, base, options, volume_only=True)
            operation, result = Helix.create(self.component, sections, mode, base, options)
            self.assertAlmostEqual(result.Shape.Volume, expected.Volume, places=4)
            self.assertAlmostEqual(preview.Volume, result.Shape.Volume, places=6)
            self.assertGreater(overlay.Volume, 0)
            self.assertAlmostEqual(base.Shape.Volume, original)
            self.assertEqual(operation.Operation, boolean if mode == "Subtract" else "Union")

    def testEditIdentityUndoPersistenceAndRecompute(self):
        sections, base = [(self.profile(), None)], self.target()
        options = self.options(refine=False, tolerance=.2, fuzzy=1e-6)
        operation, result = Helix.create(self.component, sections, "Add", base, options)
        oid, rid, name, volume = operation.ObjectId, result.ObjectId, result.Name, result.Shape.Volume
        consumer = self.doc.addObject("Part::Mirroring", "Consumer")
        self.component.addObject(consumer)
        consumer.Source = result
        self.doc.recompute()
        operation = Helix.edit(operation, sections, "Subtract", base)
        self.assertEqual(operation.ObjectId, oid)
        self.assertEqual(result.ObjectId, rid)
        self.assertAlmostEqual(operation.Tolerance, .2)
        self.assertAlmostEqual(operation.FuzzyTolerance, 1e-6)
        self.assertFalse(operation.Refine)
        self.assertLess(consumer.Shape.Volume, base.Shape.Volume)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.getObject(name).Shape.Volume, volume)
        self.doc.redo()
        self.doc.recompute()
        result = self.doc.getObject(name)
        old = result.Shape.Volume
        result.Producer.Pitch = 4.
        self.doc.recompute()
        self.assertNotAlmostEqual(result.Shape.Volume, old, places=3)
        path = self.output / "component-helix.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        result = self.doc.getObject(name)
        self.assertEqual(result.ObjectId, rid)
        self.assertEqual(result.Producer.ObjectId, oid)
        self.assertAlmostEqual(result.Shape.Volume, self.doc.getObject("Consumer").Shape.Volume)

    def testSelectedCurvesConstructionAndReferenceAxes(self):
        profile = self.profile()
        profile.addGeometry(Part.LineSegment(App.Vector(0, -2, 0), App.Vector(0, 8, 0)), True)
        self.doc.recompute()
        options = self.options(axis="Axis0")
        whole_preview = Helix.preview(self.component, [(profile, None)], options=options)
        whole, whole_result = Helix.create(self.component, [(profile, None)], options=options)
        self.assertAlmostEqual(whole_result.Shape.Volume, whole_preview.Volume, places=5)
        self.assertEqual(Helix.read(whole)[3]["axis"], "Axis0")
        profile = self.profile()
        profile.addGeometry(Part.LineSegment(App.Vector(0, -2, 0), App.Vector(0, 8, 0)), True)
        profile.addGeometry(Part.LineSegment(App.Vector(20, 0, 0), App.Vector(21, 0, 0)))
        self.doc.recompute()
        sections = [(profile, ["Edge1", "Edge2", "Edge3", "Edge4"])]
        options = self.options(axis="Axis0")
        preview = Helix.preview(self.component, sections, options=options)
        operation, result = Helix.create(self.component, sections, options=options)
        self.assertAlmostEqual(preview.Volume, result.Shape.Volume, places=6)
        self.assertEqual(Helix.read(operation)[0], sections)
        self.assertEqual(Helix.read(operation)[3]["axis"], "Axis0")
        self.assertTrue(operation.ReferenceAxis[0].AxisSource)
        count = len(self.doc.Objects)
        operation = Helix.edit(operation, sections, "New Body", options=options)
        self.assertEqual(len(self.doc.Objects), count)
        import Sketcher
        profile.addConstraint(Sketcher.Constraint("Vertical", 4))
        profile.addConstraint(Sketcher.Constraint("DistanceX", 4, 1, -1.))
        self.doc.recompute()
        self.assertGreater(result.Shape.Volume, preview.Volume)
        names = profile.Name, operation.Name, result.Name
        path = self.output / "helix-construction-axis.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.component = Model.metadata(self.doc).RootComponent
        profile, operation, result = [self.doc.getObject(name) for name in names]
        sections = [(profile, ["Edge1", "Edge2", "Edge3", "Edge4"])]
        self.assertEqual(Helix.read(operation)[3]["axis"], "Axis0")
        self.assertGreater(result.Shape.Volume, preview.Volume)
        for origin in self.component.Origin.OriginFeatures:
            if getattr(origin, "Role", "") == "Y_Axis":
                axis = origin
                break
        else:
            self.fail("Component Y axis missing")
        options = self.options(axis="Reference", axis_reference=(axis, []))
        preview = Helix.preview(self.component, sections, options=options)
        operation = Helix.edit(operation, sections, "New Body", options=options)
        self.assertAlmostEqual(preview.Volume, result.Shape.Volume, places=6)
        edge = self.doc.addObject("Part::Feature", "AxisEdge")
        edge.Shape = Part.makeLine(App.Vector(0, -1, 0), App.Vector(0, 10, 0))
        Model.register_object(self.component, edge)
        self.doc.recompute()
        options["axis_reference"] = (edge, ["Edge1"])
        operation = Helix.edit(operation, sections, "New Body", options=options)
        self.assertAlmostEqual(result.Shape.Volume, 10 * math.pi, places=3)

    def testPlacedProfilesAndDatumAxes(self):
        profile = self.profile()
        profile.AttachmentOffset = App.Placement(App.Vector(4, 5, 6), App.Rotation(App.Vector(1, 0, 0), 45))
        self.doc.recompute()
        for elements in (None, ["Edge1", "Edge2", "Edge3", "Edge4"]):
            sections = [(profile, elements)]
            options = self.options()
            preview = Helix.preview(self.component, sections, options=options)
            _, result = Helix.create(self.component, sections, options=options)
            self.assertAlmostEqual(preview.Volume, result.Shape.Volume, places=6)
            self.assertLess(preview.cut(result.Shape).Volume, 1e-5)
        datum = self.doc.addObject("PartDesign::Line", "DatumAxis")
        Model.register_object(self.component, datum)
        datum.Placement = App.Placement(profile.Placement.Base, App.Rotation(App.Vector(0, 0, 1), profile.Placement.Rotation.multVec(App.Vector(0, 1, 0))))
        self.doc.recompute()
        options = self.options(axis="Reference", axis_reference=(datum, []))
        preview = Helix.preview(self.component, sections, options=options)
        _, result = Helix.create(self.component, sections, options=options)
        self.assertAlmostEqual(preview.Volume, result.Shape.Volume, places=6)
        self.assertLess(preview.cut(result.Shape).Volume, 1e-5)

    def testInvalidRollbackAndExpressions(self):
        sections, base = [(self.profile(), None)], self.target()
        operation, result = Helix.create(self.component, sections, "Subtract", base, self.options())
        distant = [(self.profile(20), None)]
        count, volume = len(self.doc.Objects), result.Shape.Volume
        with self.assertRaises(ValueError):
            Helix.edit(operation, distant, "Subtract", base)
        self.assertEqual(len(self.doc.Objects), count)
        self.assertAlmostEqual(result.Shape.Volume, volume)
        with self.assertRaises(ValueError):
            Helix.edit(operation, sections, "Subtract", result)
        for changes in (dict(pitch=0.), dict(angle=90.), dict(axis="Reference"), dict(tolerance=0.), dict(turns=0., input_mode=Helix.INPUT_MODES[1])):
            with self.assertRaises(ValueError):
                Helix.preview(self.component, sections, options=self.options(**changes))
        operation.setExpression("Pitch", "3 mm")
        with self.assertRaises(ValueError):
            Helix.edit(operation, sections, "Subtract", base)
        self.assertTrue(operation.ExpressionEngine)

    def testTaskTemplateHistoryAndModeConversion(self):
        profile = self.profile()
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(profile)
        task = Task.launch()
        self.assertTrue(task.auto_preview.isChecked())
        task.auto_preview.setChecked(False)
        self.assertEqual([b.isChecked() for b, host, form in task.sections], [True, True, False, True])
        self.assertEqual(task.profile.currentData(), profile.Name)
        self.assertTrue(task.target.isHidden())
        self.assertEqual(task.preview_mode.currentData(), "Overlay")
        task.fields["pitch"].setProperty("rawValue", 3.)
        task.fields["height"].setProperty("rawValue", 6.)
        task.input_mode.setCurrentIndex(1)
        self.assertAlmostEqual(float(task.fields["turns"].property("rawValue")), 2.)
        self.assertTrue(task.fields["height"].isHidden())
        self.assertTrue(task.preview(), task.status.text())
        self.assertEqual(tuple(task.ghost.node.getChild(2).diffuseColor[0].getValue()), (0., 0., 1.))
        Gui.updateGui()
        task.form.grab().save(str(self.output / "helix-task.png"))
        self.assertTrue(task.accept())
        Navigator.show(self.doc).edit_history(Navigator.object_key(task.result))
        task = Task._task
        task.auto_preview.setChecked(False)
        self.assertEqual(task.input_mode.currentIndex(), 1)
        self.assertAlmostEqual(task.operation.Turns, 2.)
        origin = next(obj for obj in self.component.Origin.OriginFeatures if getattr(obj, "Role", "") == "Y_Axis")
        task.axis.setCurrentIndex(task.axis.findData("Origin:" + origin.Name))
        self.assertEqual(task.values()[3]["axis_reference"][0], origin)
        self.assertTrue(task.preview(), task.status.text())
        task.axis.setCurrentIndex(task.axis.findData("Reference"))
        task.begin_reference_pick(task.axis_reference)
        task.addSelection(self.doc.Name, origin.Name, "")
        self.assertEqual(task.axis_reference.text(), origin.Name)
        self.assertIsNone(task.reference_pick)
        task.sections[2][0].setChecked(True)
        task.input_mode.setCurrentIndex(3)
        Gui.updateGui()
        task.form.grab().save(str(self.output / "helix-advanced.png"))
        task.preview_mode.setCurrentIndex(task.preview_mode.findData("None"))
        self.assertIsNone(task.ghost)
        self.assertFalse(task.preview_timer.isActive())
        task.reject()

    def testTaskColorsCancelAndRecovery(self):
        profile, base = self.profile(), self.target()
        for mode, color in (("Add", (0., 1., 0.)), ("Subtract", (1., 0., 0.))):
            display = Model.display_object(base)
            visible, transparency = display.Visibility, display.ViewObject.Transparency
            Gui.Selection.clearSelection()
            task = Task.launch(preset=mode)
            task.auto_preview.setChecked(False)
            self.assertFalse(task.accept())
            self.assertIs(Task._task, task)
            task.profile.setCurrentIndex(task.profile.findData(profile.Name))
            task.target.setCurrentIndex(task.target.findData(base.Name))
            task.fields["pitch"].setProperty("rawValue", 3.)
            task.fields["height"].setProperty("rawValue", 6.)
            self.assertTrue(task.preview(), task.status.text())
            self.assertEqual(tuple(task.ghost.node.getChild(2).diffuseColor[0].getValue()), color)
            task.preview_mode.setCurrentIndex(task.preview_mode.findData("Result"))
            self.assertTrue(task.preview(), task.status.text())
            self.assertFalse(display.Visibility)
            task.reject()
            self.assertEqual(display.Visibility, visible)
            self.assertEqual(display.ViewObject.Transparency, transparency)

    def testNativeCommandRouting(self):
        for command, mode in (("PartDesign_AdditiveHelix", "New Body"), ("PartDesign_SubtractiveHelix", "Subtract")):
            Gui.runCommand(command)
            self.assertIsInstance(Task._task, Task.HelixTask)
            self.assertEqual(Task._task.mode.currentData(), mode)
            Task._task.reject()
