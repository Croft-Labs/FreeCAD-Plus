# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native primitive acceptance: geometry, lifecycle, attachment and Tasks routing."""
import hashlib
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
import ComponentPrimitive as Primitive
import ComponentNativeOperation as Native
from freecad.gui import ComponentPrimitiveTask as Task
from freecad.gui import ComponentNavigator as Navigator


class TestComponentPrimitive(unittest.TestCase):
    def setUp(self):
        root = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, folder in ((Primitive, "src/Mod/Part"), (Native, "src/Mod/Part"), (Task, "src/Gui"), (Navigator, "src/Gui")):
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((root / folder / Path(module.__file__).name).read_bytes()).digest())
        Gui.activateWorkbench("PartDesignWorkbench")
        self.doc = Model.new_document("Primitive acceptance")
        self.component = Model.metadata(self.doc).RootComponent
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])

    def tearDown(self):
        if Task._task:
            Task._task.reject()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def target(self):
        obj = self.doc.addObject("Part::Feature", "Base")
        obj.Shape = Part.makeBox(30, 40, 40, App.Vector(-30, -20, -20))
        Model.register_object(self.component, obj, "Operation")
        result = Model.publish_result(self.component, obj)
        self.doc.recompute()
        return result

    def options(self, kind="Box"):
        values = Primitive.defaults(kind)
        values["placement"] = App.Placement(App.Vector(-1, 1, 1), App.Rotation(App.Vector(0, 0, 1), 15))
        return values

    def testEightShapesAllModesPreviewAndDimensions(self):
        base = self.target()
        for kind in Primitive.PARAMETERS:
            options = self.options(kind)
            tool = Primitive.preview(self.component, [], options=options)
            for mode, boolean in (("New Body", "Subtraction"), ("Add", "Subtraction"), ("Subtract", "Subtraction"), ("Subtract", "Common")):
                with self.subTest(kind=kind, mode=mode, boolean=boolean):
                    options["boolean"] = boolean
                    target = None if mode == "New Body" else base
                    count = len(self.doc.Objects)
                    preview = Primitive.preview(self.component, [], mode, target, options)
                    self.assertEqual(count, len(self.doc.Objects))
                    operation, result = Primitive.create(self.component, [], mode, target, options)
                    # Native primitives perform Booleans in the primitive's local
                    # frame. Match that frame, especially for B-spline ellipsoids.
                    local_base, local_tool = base.Shape.copy(), tool.copy()
                    local_base.Placement = options["placement"].inverse().multiply(local_base.Placement)
                    local_tool.Placement = options["placement"].inverse().multiply(local_tool.Placement)
                    expected = local_tool if target is None else local_base.fuse(local_tool) if mode == "Add" else local_base.common(local_tool) if boolean == "Common" else local_base.cut(local_tool)
                    if kind == "Ellipsoid":
                        # Compare directly with a Classic native feature: transformed
                        # B-spline Boolean/refinement integration differs from Part.fuse.
                        check = App.newDocument("ClassicPrimitiveBaseline", hidden=True, temp=True)
                        try:
                            native = check.addObject("PartDesign::" + ("Subtractive" if mode == "Subtract" else "Additive") + kind, "Ellipsoid")
                            if target:
                                copied = check.addObject("Part::Feature", "Base")
                                copied.Shape = target.Shape
                                native.BaseFeature = copied
                            native.Placement = options["placement"]
                            for key, value in options["dimensions"].items():
                                setattr(native, key, value)
                            native.Refine = options["refine"]
                            native.FuzzyTolerance = options["fuzzy"]
                            if mode == "Subtract":
                                native.Operation = boolean
                            check.recompute()
                            self.assertAlmostEqual(result.Shape.Volume, native.Shape.Volume, places=6)
                        finally:
                            App.closeDocument(check.Name)
                            App.setActiveDocument(self.doc.Name)
                    else:
                        self.assertAlmostEqual(result.Shape.Volume, expected.Volume, places=4)
                    self.assertLess(preview.cut(result.Shape).Volume, 1e-5)
                    self.assertEqual(Primitive.read(operation)[3]["dimensions"], options["dimensions"])
                    self.assertTrue(result.Shape.isValid())
        self.assertFalse(any(obj.TypeId == "PartDesign::Body" for obj in self.doc.Objects))

    def testShapeModeIdentityUndoPersistenceAndDownstream(self):
        base = self.target()
        operation, result = Primitive.create(self.component, [], "Add", base, self.options())
        oid, rid, name, volume = operation.ObjectId, result.ObjectId, result.Name, result.Shape.Volume
        consumer = self.doc.addObject("Part::Mirroring", "Consumer")
        self.component.addObject(consumer)
        consumer.Source = result
        self.doc.recompute()
        options = self.options("Cylinder")
        options.update(refine=False, fuzzy=1e-6)
        operation = Primitive.edit(operation, [], "Subtract", base, options)
        self.assertEqual(operation.ObjectId, oid)
        self.assertEqual(result.ObjectId, rid)
        self.assertEqual(operation.TypeId, "PartDesign::SubtractiveCylinder")
        self.assertLess(consumer.Shape.Volume, base.Shape.Volume)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.getObject(name).Shape.Volume, volume)
        self.doc.redo()
        self.doc.recompute()
        result = self.doc.getObject(name)
        before = result.Shape.Volume
        result.Producer.Radius = 8
        self.doc.recompute()
        self.assertNotAlmostEqual(result.Shape.Volume, before)
        path = self.output / "component-primitive.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        result = self.doc.getObject(name)
        self.assertEqual(result.ObjectId, rid)
        self.assertEqual(result.Producer.ObjectId, oid)
        self.assertAlmostEqual(result.Shape.Volume, self.doc.getObject("Consumer").Shape.Volume)
        self.assertFalse(result.Producer.Refine)

    def testAttachmentRecomputePreviewAndModeEdit(self):
        plane = self.doc.addObject("PartDesign::Plane", "Plane")
        Model.register_object(self.component, plane, "Object")
        plane.Placement = App.Placement(App.Vector(2, 3, 4), App.Rotation(App.Vector(0, 1, 0), 35))
        self.doc.recompute()
        options = Primitive.defaults()
        options.update(map_mode="ObjectXY", support=[(plane, [""])], offset=App.Placement(App.Vector(1, 2, 3), App.Rotation(15, 0, 0)), reverse=True)
        preview = Primitive.preview(self.component, [], options=options)
        operation, result = Primitive.create(self.component, [], options=options)
        self.assertLess(preview.cut(result.Shape).Volume, 1e-5)
        before = result.Shape.CenterOfMass
        plane.Placement.Base = App.Vector(4, 3, 4)
        self.doc.recompute()
        self.assertGreater((result.Shape.CenterOfMass - before).Length, 1.)
        values = Primitive.read(operation)[3]
        values.update(kind="Sphere", dimensions=dict(Primitive.PARAMETERS["Sphere"]))
        operation = Primitive.edit(operation, [], "New Body", options=values)
        self.assertEqual(operation.AttachmentSupport[0][0], plane)
        self.assertTrue(operation.MapReversed)
        self.assertEqual(operation.MapMode, "ObjectXY")
        self.assertTrue(plane.Visibility)

    def testInvalidRollbackAndExpressions(self):
        base = self.target()
        operation, result = Primitive.create(self.component, [], "Subtract", base, self.options())
        count, volume = len(self.doc.Objects), result.Shape.Volume
        options = self.options("Cone")
        options["dimensions"].update(Radius1=0., Radius2=0.)
        with self.assertRaises(ValueError):
            Primitive.edit(operation, [], "Subtract", base, options)
        self.assertEqual(len(self.doc.Objects), count)
        self.assertAlmostEqual(result.Shape.Volume, volume)
        with self.assertRaises(ValueError):
            Primitive.edit(operation, [], "Subtract", result)
        operation.setExpression("Length", "10 mm")
        with self.assertRaises(ValueError):
            Primitive.edit(operation, [], "Subtract", base)
        self.assertTrue(operation.ExpressionEngine)

    def testTaskTemplateShapesHistoryPreviewAndCancel(self):
        task = Task.launch()
        task.auto_preview.setChecked(False)
        self.assertEqual([b.isChecked() for b, host, form in task.sections], [True, True, False, True])
        self.assertEqual(task.preview_mode.currentData(), "Overlay")
        self.assertTrue(task.target.isHidden())
        for kind in Primitive.PARAMETERS:
            task.kind.setCurrentIndex(task.kind.findData(kind))
            self.assertEqual(set(task.fields), set(Primitive.PARAMETERS[kind]))
            self.assertTrue(task.preview(), task.status.text())
        Gui.updateGui()
        self.assertTrue(all(field.height() >= field.minimumSizeHint().height() for field in task.fields.values()))
        task.form.grab().save(str(self.output / "primitive-wedge.png"))
        self.assertTrue(task.accept())
        Navigator.show(self.doc).edit_history(Navigator.object_key(task.result))
        task = Task._task
        task.auto_preview.setChecked(False)
        self.assertEqual(task.kind.currentData(), "Wedge")
        task.sections[2][0].setChecked(True)
        task.kind.setCurrentIndex(task.kind.findData("Cylinder"))
        task.fields["FirstAngle"].setProperty("rawValue", 12.)
        self.assertTrue(task.preview(), task.status.text())
        Gui.updateGui()
        task.form.grab().save(str(self.output / "primitive-advanced.png"))
        task.reject()
        base = self.target()
        for mode, color in (("Add", (0., 1., 0.)), ("Subtract", (1., 0., 0.))):
            display = Model.display_object(base)
            visible, transparency = display.Visibility, display.ViewObject.Transparency
            task = Task.launch(preset=mode)
            task.auto_preview.setChecked(False)
            self.assertFalse(task.accept())
            task.target.setCurrentIndex(task.target.findData(base.Name))
            task.placement_fields["x"].setProperty("rawValue", -2.)
            self.assertTrue(task.preview(), task.status.text())
            self.assertEqual(tuple(task.ghost.node.getChild(2).diffuseColor[0].getValue()), color)
            task.preview_mode.setCurrentIndex(task.preview_mode.findData("Final Result"))
            self.assertTrue(task.preview(), task.status.text())
            self.assertFalse(display.Visibility)
            task.reject()
            self.assertEqual(display.Visibility, visible)
            self.assertEqual(display.ViewObject.Transparency, transparency)

    def testTaskAttachmentReferences(self):
        plane = next(obj for obj in self.component.Origin.OriginFeatures if obj.Role == "XY_Plane")
        task = Task.launch(kind="Sphere")
        task.auto_preview.setChecked(False)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(plane)
        task.add_references()
        self.assertEqual(task.support.count(), 1)
        task.map_mode.setCurrentIndex(task.map_mode.findData("ObjectXY"))
        task.placement_fields["z"].setProperty("rawValue", 7.)
        self.assertTrue(task.preview(), task.status.text())
        self.assertTrue(task.accept())
        self.assertAlmostEqual(task.operation.Shape.CenterOfMass.z, 7.)
        Navigator.show(self.doc).edit_history(Navigator.object_key(task.result))
        task = Task._task
        self.assertEqual(task.support.item(0).text(), plane.Name)
        self.assertAlmostEqual(float(task.placement_fields["z"].property("rawValue")), 7.)
        task.reject()

    def testNativeCommandRouting(self):
        for command, mode in (("PartDesign_CompPrimitiveAdditive", "New Body"), ("PartDesign_CompPrimitiveSubtractive", "Subtract")):
            for index, kind in enumerate(Primitive.PARAMETERS):
                Gui.runCommand(command, index)
                self.assertIsInstance(Task._task, Task.PrimitiveTask)
                self.assertEqual(Task._task.mode.currentData(), mode)
                self.assertEqual(Task._task.kind.currentData(), kind)
                Task._task.reject()
