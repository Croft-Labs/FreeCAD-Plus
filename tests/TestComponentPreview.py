# SPDX-License-Identifier: LGPL-2.1-or-later
"""Full tool overlays, normal result appearance and shared preview lifecycle."""
import hashlib
import importlib
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentExtrude as Extrude
import ComponentExtent as Extent
from PySide import QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest


class TestComponentPreview(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartDesignWorkbench")
        self.doc = Model.new_document("Modeling previews")
        self.component = Model.metadata(self.doc).RootComponent
        self.task = None
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        root = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for name in ("Extrude", "Revolve", "Loft", "Pipe", "Helix", "Primitive"):
            for module, folder in (("Component" + name, "src/Mod/Part"),
                                   ("freecad.gui.Component" + name + "Task", "src/Gui")):
                loaded = importlib.import_module(module)
                path = Path(loaded.__file__)
                self.assertEqual(hashlib.sha256(path.read_bytes()).digest(),
                                 hashlib.sha256((root / folder / path.name).read_bytes()).digest())
        Gui.Selection.clearSelection()

    def tearDown(self):
        if self.task:
            self.task.reject()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def rectangle(self, left=2, right=4, top=3, z=0):
        sketch = Sketch.create(self.component, offset=z)
        points = [App.Vector(left, 0, 0), App.Vector(right, 0, 0),
                  App.Vector(right, top, 0), App.Vector(left, top, 0)]
        for a, b in zip(points, points[1:] + points[:1]):
            sketch.addGeometry(Part.LineSegment(a, b))
        self.doc.recompute()
        return sketch

    def target(self, far=False):
        obj = self.doc.addObject("Part::Feature", "Target")
        obj.Shape = Part.makeBox(20, 20, 25.4, App.Vector(1000 if far else 0, 0, 0))
        Model.register_object(self.component, obj, "Operation")
        result = Model.publish_result(self.component, obj)
        self.doc.recompute()
        return result

    def launch(self, name="Extrude", **kwargs):
        self.task = importlib.import_module("freecad.gui.Component" + name + "Task").launch(**kwargs)
        return self.task

    def testAllToolsIgnoreMissingOrDisjointTargets(self):
        profile = self.rectangle()
        end = self.rectangle(z=10)
        helix_profile = self.rectangle(left=2, right=3, top=1)
        path = self.doc.addObject("Part::Feature", "Path")
        path.Shape = Part.makeLine(App.Vector(), App.Vector(0, 0, 10))
        Model.register_object(self.component, path)
        target = self.target(far=True)
        pipe = importlib.import_module("ComponentPipe")
        pipe_options = pipe.defaults()
        pipe_options["spine"] = (path, [])
        helix = importlib.import_module("ComponentHelix")
        helix_options = helix.defaults()
        helix_options.update(pitch=3., height=6., turns=2.)
        cases = [
            ("Extrude", [profile, 127.], {"options": Extent.defaults()}),
            ("Revolve", [profile, 270.], {}),
            ("Loft", [[(profile, None), (end, None)]], {}),
            ("Pipe", [[(profile, None)]], {"options": pipe_options}),
            ("Helix", [[(helix_profile, None)]], {"options": helix_options}),
            ("Primitive", [[]], {}),
        ]
        count = len(self.doc.Objects)
        for name, args, kwargs in cases:
            backend = importlib.import_module("Component" + name)
            expected = backend.preview(self.component, *args, **kwargs)
            for mode in ("New Body", "Add", "Subtract"):
                for body in (None, target):
                    if mode == "New Body" and body:
                        continue
                    with self.subTest(operation=name, mode=mode, target=bool(body)):
                        shape = backend.preview(self.component, *args, mode=mode, target=body,
                                                tool_only=True, **kwargs)
                        self.assertTrue(shape.isValid())
                        self.assertAlmostEqual(shape.Volume, expected.Volume, places=5)
                        self.assertLess(shape.cut(expected).Volume, 1e-6)
                        self.assertEqual(len(self.doc.Objects), count)
                        self.assertEqual(App.ActiveDocument, self.doc)
            with self.assertRaises(ValueError):
                backend.preview(self.component, *args, mode="Subtract", **kwargs)

    def testFiveInchOverlayAndOneInchResult(self):
        profile, target = self.rectangle(), self.target()
        options = Extent.defaults()
        overlay = Extrude.preview(self.component, profile, 127., "Subtract", target,
                                  options=options, tool_only=True)
        result = Extrude.preview(self.component, profile, 127., "Subtract", target, options=options)
        self.assertAlmostEqual(overlay.BoundBox.ZLength, 127.)
        self.assertAlmostEqual(overlay.Volume, 6 * 127.)
        self.assertAlmostEqual(result.BoundBox.ZLength, 25.4)
        self.assertAlmostEqual(result.Volume, target.Shape.Volume - 6 * 25.4)
        options.update(start="Offset", start_offset=12., sides="Two sides", length2=8.)
        overlay = Extrude.preview(self.component, profile, 127., "Subtract",
                                  options=options, tool_only=True)
        self.assertAlmostEqual(overlay.BoundBox.ZMin, 4.)
        self.assertAlmostEqual(overlay.BoundBox.ZMax, 139.)

    def testThroughAllRevolveIsFullToolWithoutTarget(self):
        import ComponentRevolve as Revolve
        profile = self.rectangle()
        expected = Revolve.preview(self.component, profile, 360.)
        distant = self.target(far=True)
        for sides, key in (("One side", "extent"), ("Symmetric", "extent"), ("Two sides", "extent2")):
            options = Revolve.defaults()
            options.update(sides=sides, start="Offset", start_offset=-30.)
            options[key] = "ThroughAll"
            for target in (None, distant):
                shape = Revolve.preview(self.component, profile, 90., "Subtract", target,
                                        options=options, tool_only=True)
                self.assertAlmostEqual(shape.Volume, expected.Volume, places=5)
                self.assertLess(shape.cut(expected).Volume, 1e-6)
            self.assertEqual(options[key], "ThroughAll")

    def testDropdownsAndAutomaticColorsWithoutTarget(self):
        from freecad.gui.ComponentTaskWidgets import CurveCollector, PreviewControls
        profile = self.rectangle()
        for name in ("Extrude", "Revolve", "Loft", "Pipe", "Helix", "Primitive"):
            task = self.launch(name)
            self.assertIsInstance(task.preview_controls, PreviewControls)
            self.assertIs(task.preview_timer.parent(), task.preview_controls)
            if name != "Primitive":
                self.assertIsInstance(task.collector, CurveCollector)
                self.assertIs(task.curves, task.collector.curves)
                self.assertIs(task.profile, task.collector.source)
            if name == "Pipe":
                for fields in task.paths.values():
                    self.assertIsInstance(fields["host"], CurveCollector)
                    self.assertIs(fields["edges"], fields["host"].curves)
            self.assertIsInstance(task.preview_mode, QtWidgets.QComboBox)
            self.assertEqual([task.preview_mode.itemData(i) for i in range(task.preview_mode.count())],
                             ["None", "Overlay", "Result"])
            self.assertEqual(task.preview_mode.currentData(), "Overlay")
            task.reject()
            self.task = None
        task = self.launch()
        task.profile.setCurrentIndex(task.profile.findData(profile.Name))
        task.length.setProperty("rawValue", 127.)
        for mode, color in (("New Body", (0., 0., 1.)), ("Add", (0., 1., 0.)), ("Subtract", (1., 0., 0.))):
            task.mode.setCurrentIndex(task.mode.findData(mode))
            QtTest.QTest.qWait(450)
            Gui.updateGui()
            self.assertIsNotNone(task.ghost, task.status.text())
            self.assertEqual(tuple(task.ghost.node.getChild(2).diffuseColor[0].getValue()), color)
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()
        Gui.updateGui()
        Gui.getMainWindow().grab().save(str(self.output / "subtract-without-target.png"))
        task.preview_mode.setCurrentIndex(task.preview_mode.findData("Result"))
        task.preview_timer.stop()
        self.assertFalse(task.preview())
        self.assertIsNone(task.ghost)
        task.preview_mode.setCurrentIndex(task.preview_mode.findData("None"))
        self.assertIsNone(task.ghost)
        self.assertFalse(task.preview_timer.isActive())

    def testResultAppearanceAndVisibilityRestoration(self):
        profile, target = self.rectangle(), self.target()
        displayed = Model.display_object(target)
        displayed.ViewObject.ShapeColor = (0.7, 0.6, 0.5)
        displayed.ViewObject.Transparency = 10
        task = self.launch(preset="Subtract")
        task.auto_preview.setChecked(False)
        task.profile.setCurrentIndex(task.profile.findData(profile.Name))
        task.target.setCurrentIndex(task.target.findData(target.Name))
        task.length.setProperty("rawValue", 127.)
        original = (displayed.Visibility, displayed.ViewObject.Transparency)
        self.assertTrue(task.preview(), task.status.text())
        self.assertGreaterEqual(displayed.ViewObject.Transparency, 75)
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()
        Gui.updateGui()
        QtTest.QTest.qWait(150)
        Gui.getMainWindow().grab().save(str(self.output / "full-subtract-overlay.png"))
        task.preview_mode.setCurrentIndex(task.preview_mode.findData("Result"))
        self.assertTrue(task.preview(), task.status.text())
        self.assertFalse(displayed.Visibility)
        for actual, expected in zip(task.ghost.node.getChild(2).diffuseColor[0].getValue(), (0.7, 0.6, 0.5)):
            self.assertAlmostEqual(actual, expected, places=5)
        self.assertAlmostEqual(task.ghost.node.getChild(2).transparency[0], 0.1, places=5)
        Gui.updateGui()
        QtTest.QTest.qWait(150)
        Gui.getMainWindow().grab().save(str(self.output / "normal-result-preview.png"))
        task.preview_mode.setCurrentIndex(task.preview_mode.findData("None"))
        self.assertEqual((displayed.Visibility, displayed.ViewObject.Transparency), original)
        task.preview_mode.setCurrentIndex(task.preview_mode.findData("Overlay"))
        task.preview()
        task.reject()
        self.task = None
        self.assertEqual((displayed.Visibility, displayed.ViewObject.Transparency), original)

    def testEditingPreviewCancelRestoresExistingResult(self):
        profile, target = self.rectangle(), self.target()
        operation, result = Extrude.create(self.component, profile, 127., "Subtract", target, options=Extent.defaults())
        original = {obj.Name: (obj.Visibility, obj.ViewObject.Transparency)
                    for obj in (operation, Model.display_object(target))}
        task = self.launch(operation=operation)
        task.auto_preview.setChecked(False)
        for preview in ("Overlay", "Result", "None", "Overlay"):
            task.preview_mode.setCurrentIndex(task.preview_mode.findData(preview))
            self.assertTrue(task.preview(), task.status.text())
        task.reject()
        self.task = None
        for name, state in original.items():
            obj = self.doc.getObject(name)
            self.assertEqual((obj.Visibility, obj.ViewObject.Transparency), state)
        self.assertAlmostEqual(result.Shape.Volume, target.Shape.Volume - 6 * 25.4)
