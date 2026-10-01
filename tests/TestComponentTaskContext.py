# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three task-transition workflows for component-owned sketches and Extrude."""
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
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentSelection as Selection
from freecad.gui import ComponentExtrudeTask as ExtrudeTask
from freecad.gui import ComponentSketchTask as SketchTask


class TestComponentTaskContext(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module in (Navigator, ExtrudeTask, SketchTask):
            name = Path(module.__file__).name
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((source / "src/Gui" / name).read_bytes()).digest())
        Gui.activateWorkbench("PartDesignWorkbench")
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / self._testMethodName
        self.output.mkdir()
        self.external = Model.new_document("Support")
        self.part = Model.metadata(self.external).RootComponent
        self.profile = Sketch.create(self.part)
        self.profile.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        self.external.recompute()
        self.box = self.external.addObject("Part::Feature", "SupportBody")
        Model.register_object(self.part, self.box, "Object", True)
        self.box.Shape = Part.makeBox(4, 5, 6)
        self.external.recompute()
        self.external.saveAs(str(self.output / "Support.cadprt"))
        self.doc = Model.new_document("Task assembly")
        self.root = Model.metadata(self.doc).RootComponent
        self.doc.saveAs(str(self.output / "Assembly.cadprt"))
        self.first = Model.add_component(self.root, self.part)
        self.second = Model.add_component(self.root, self.part,
            placement=App.Placement(App.Vector(30, 0, 0), App.Rotation()))
        self.doc.save()
        self.panel = Navigator.show(self.doc)
        self.window = self.panel.mdi.activeSubWindow()
        self.path = [self.second.ObjectId]
        group = self.panel.structure.topLevelItem(0).child(0)
        self.panel.toggle_instances(group)
        self.panel.refresh()
        self.panel.activate_item(self.panel.structure.topLevelItem(0).child(0).child(1))
        self.panel.refresh()
        Gui.Selection.clearSelection()

    def tearDown(self):
        if ExtrudeTask._task:
            ExtrudeTask._task.reject()
        if SketchTask._task:
            SketchTask._task.reject()
        for doc in list(App.listDocuments().values()):
            gui = Gui.getDocument(doc.Name)
            if gui.getInEdit():
                gui.resetEdit()
        Gui.updateGui()
        for doc in reversed(list(App.listDocuments().values())):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def select(self, obj, element=""):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.doc.Name, self.root.Name,
            Selection.native_path(self.root, self.path, obj) + element)

    def assert_origin(self):
        Gui.updateGui()
        self.assertEqual(App.ActiveDocument, self.doc)
        self.assertEqual(self.panel.mdi.activeSubWindow(), self.window)
        self.assertEqual(self.panel.root_key, Navigator.object_key(self.root))
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.part))
        self.assertEqual(self.panel.active_path, self.path)
        self.assertEqual(Gui.activeDocument().activeView().getActiveObject("part", False),
                         (self.part, self.root, Selection.native_path(self.root, self.path)))

    def testExtrudePreselectionPreviewCancelAndAccept(self):
        self.select(self.profile)
        count = len(self.external.Objects)
        self.panel.new_extrude()
        task = ExtrudeTask._task
        self.assertEqual(task.component, self.part)
        self.assertEqual(task.profile.currentData(), self.profile.Name)
        self.assertEqual(App.ActiveDocument, self.external)
        self.assertTrue(task.preview(), task.status.text())
        task.reject()
        self.assertIsNone(task.ghost)
        self.assertEqual(len(self.external.Objects), count)
        self.assert_origin()
        self.select(self.profile)
        Gui.runCommand("PartDesign_Pad")
        task = ExtrudeTask._task
        task.length.setProperty("rawValue", 5)
        if not task.accept():
            self.fail(task.status.text())
        self.assert_origin()
        self.assertEqual(Model.owner(task.result), self.part)
        self.assertAlmostEqual(task.result.Shape.Volume, 20 * math.pi)
        self.assertEqual(Model.history(self.root), [])
        self.assertEqual(self.first.LinkedObject, self.second.LinkedObject)
        self.external.save()
        self.doc.save()
        self.capture("extrude-returned-history.png")

    def testSketchFacePreselectionAndNativeEditorReturn(self):
        self.select(self.box, "Face6")
        count = len(self.external.Objects)
        self.panel.new_sketch()
        task = SketchTask._task
        self.assertEqual(task.support, (self.box, "Face6"))
        task.reject()
        self.assertEqual(len(self.external.Objects), count)
        self.assert_origin()
        self.select(self.box, "Face6")
        Gui.runCommand("Sketcher_NewSketch")
        task = SketchTask._task
        self.assertEqual(task.support, (self.box, "Face6"))
        if not task.accept():
            self.fail(task.status.text())
        self.assertEqual(App.ActiveDocument, self.external)
        self.assertTrue(Gui.activeDocument().getInEdit())
        self.assertEqual(Model.owner(task.result), self.part)
        Gui.activeDocument().resetEdit()
        self.assert_origin()
        self.assertEqual(str(task.result.MapMode), "FlatFace")
        self.panel.edit_history(Navigator.object_key(task.result))
        self.assertEqual(App.ActiveDocument, self.external)
        Gui.activeDocument().resetEdit()
        self.assert_origin()
        self.external.save()
        self.capture("sketch-returned-history.png")

    def testIsolatedExtrudeHistoryEditingReturnsToSameView(self):
        self.panel.open_component_tab(Navigator.object_key(self.part))
        self.panel.refresh()
        window = self.panel.mdi.activeSubWindow()
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.profile)
        task = ExtrudeTask.launch()
        task.length.setProperty("rawValue", 3)
        if not task.accept():
            self.fail(task.status.text())
        result, identity = task.result, task.result.ObjectId
        self.assertEqual(self.panel.mdi.activeSubWindow(), window)
        self.assertEqual(self.panel.root_key, Navigator.object_key(self.part))
        self.panel.edit_history(Navigator.object_key(result))
        edit = ExtrudeTask._task
        edit.length.setProperty("rawValue", 7)
        if not edit.accept():
            self.fail(edit.status.text())
        self.assertEqual(self.panel.mdi.activeSubWindow(), window)
        self.assertEqual(self.panel.active_path, [])
        self.assertEqual(result.ObjectId, identity)
        self.assertAlmostEqual(result.Shape.Volume, 28 * math.pi)
        self.external.save()

    def capture(self, name):
        self.panel.setFloating(True)
        self.panel.resize(850, 650)
        Gui.updateGui()
        self.panel.grab().save(str(self.output / name))
