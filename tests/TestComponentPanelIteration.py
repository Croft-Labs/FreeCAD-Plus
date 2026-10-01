# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three bounded feedback checks for the component panel and sketch/edit batch."""
import hashlib
import math
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import CadDocument
import ComponentModel as Model
import ComponentExtrude as Extrude
import ComponentSketch as Sketch
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentExtrudeTask as ExtrudeTask
from freecad.gui import ComponentSketchTask as SketchTask


class TestComponentPanelIteration(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, relative in [
            (Model, "src/Mod/Part/ComponentModel.py"),
            (Extrude, "src/Mod/Part/ComponentExtrude.py"),
            (Sketch, "src/Mod/Part/ComponentSketch.py"),
            (Navigator, "src/Gui/ComponentNavigator.py"),
            (ExtrudeTask, "src/Gui/ComponentExtrudeTask.py"),
            (SketchTask, "src/Gui/ComponentSketchTask.py"),
        ]:
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((source / relative).read_bytes()).digest())
        Gui.activateWorkbench("PartDesignWorkbench")
        self.doc = Model.new_document("Component panel feedback")
        self.root = Model.metadata(self.doc).RootComponent
        self.panel = Navigator.show(self.doc)
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])

    def tearDown(self):
        if SketchTask._task:
            SketchTask._task.reject()
        if ExtrudeTask._task:
            ExtrudeTask._task.reject()
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def profile(self, radius):
        obj = Sketch.create(self.root)
        obj.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), radius))
        self.doc.recompute()
        return obj

    def testSketchCommandsAndFaceAttachment(self):
        Gui.Selection.clearSelection()
        before = len(self.doc.Objects)
        Gui.runCommand("PartDesign_NewSketch")
        self.assertIsNotNone(SketchTask._task)
        SketchTask._task.reject()
        self.assertEqual(len(self.doc.Objects), before)
        Gui.runCommand("Sketcher_NewSketch")
        task = SketchTask._task
        self.assertIsNotNone(task)
        task.plane.setCurrentIndex(task.plane.findData("XZ plane"))
        task.offset.setProperty("rawValue", 3.0)
        Gui.updateGui()
        task.form.grab().save(str(self.output / "component-sketch-task.png"))
        if not task.accept():
            self.fail(task.status.text())
        sketch = task.result
        self.assertEqual(Model.owner(sketch), self.root)
        self.assertTrue(Gui.activeDocument().getInEdit())
        Gui.activeDocument().resetEdit()
        self.assertAlmostEqual(sketch.Placement.Base.y, -3.0)
        self.assertFalse(any(obj.TypeId == "PartDesign::Body" for obj in self.doc.Objects))
        box = self.doc.addObject("Part::Box", "Box")
        Model.register_object(self.root, box, "Object", True)
        self.doc.recompute()
        attached = Sketch.create(self.root, "Selected planar face", 1.0, (box, "Face6"))
        self.assertEqual(str(attached.MapMode), "FlatFace")
        self.assertAlmostEqual(attached.Placement.Base.z, 11.0)
        box.Height = 12
        self.doc.recompute()
        self.assertAlmostEqual(attached.Placement.Base.z, 13.0)

    def testExtrudeModeTargetIdentityAndReopen(self):
        profile = self.profile(2)
        first, body = Extrude.create(self.root, profile, 5)
        second, other = Extrude.create(self.root, profile, 6)
        hole = self.profile(1)
        operation, result = Extrude.create(self.root, hole, 10)
        identity, operation_id = result.ObjectId, operation.ObjectId
        position = list(self.root.ModelHistory).index(operation.Name)
        self.panel.edit_history(Navigator.object_key(result))
        task = ExtrudeTask._task
        self.assertTrue(task.mode.isEnabled())
        task.mode.setCurrentIndex(task.mode.findData("Subtract"))
        task.target.setCurrentIndex(task.target.findData(body.Name))
        if not task.accept():
            self.fail(task.status.text())
        operation = result.Producer
        self.assertEqual(operation.ExtrudeMode, "Subtract")
        self.assertEqual(operation.ObjectId, operation_id)
        self.assertEqual(self.root.ModelHistory[position], operation.Name)
        self.assertEqual(result.ObjectId, identity)
        self.assertAlmostEqual(result.Shape.Volume, 15 * math.pi)
        operation = Extrude.edit(operation, hole, 10, mode="Subtract", target=other)
        self.assertAlmostEqual(result.Shape.Volume, 18 * math.pi)
        self.assertTrue(body.Visibility)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 15 * math.pi)
        operation = Extrude.edit(result.Producer, hole, 10, mode="New Body")
        self.assertAlmostEqual(result.Shape.Volume, 10 * math.pi)
        self.assertEqual(result.ObjectId, identity)
        self.assertTrue(body.Visibility)
        with self.assertRaises(ValueError):
            Extrude.edit(operation, hole, 10, mode="Add", target=result)
        path = self.output / "Component-Edit-Feedback.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(path)
        result = next(obj for obj in self.doc.Objects if getattr(obj, "ObjectId", "") == identity)
        self.assertAlmostEqual(result.Shape.Volume, 10 * math.pi)
        self.assertEqual(result.Producer.ObjectId, operation_id)

    def testGroupedInstancesMenusAndHistoryControls(self):
        link = Model.add_component(self.root, label="support angle")
        definition = link.LinkedObject
        box = self.doc.addObject("Part::Box", "Support")
        Model.register_object(definition, box, "Object", True)
        self.doc.recompute()
        for number in range(1, 5):
            Model.add_component(self.root, definition,
                                placement=App.Placement(App.Vector(15 * number, 0, 0), App.Rotation()))
        self.panel.refresh()
        root_row = self.panel.structure.topLevelItem(0)
        group = root_row.child(0)
        self.assertEqual(group.text(0), "support angle")
        self.assertEqual(group.text(2), "x5")
        self.assertEqual(group.childCount(), 0)
        self.assertTrue(root_row.font(0).bold())
        menu = self.panel.build_menu(self.panel.structure, root_row)
        labels = [action.text() for action in menu.actions()]
        self.assertEqual(labels[0], "Edit")
        self.assertNotIn("Open Component in Tab", labels)
        self.assertIn("Add Component", labels)
        self.assertFalse(any(button.text() in ("Add Component", "Add Reference Object")
                             for button in self.panel.findChildren(QtWidgets.QPushButton)))
        with self.assertRaises(ValueError):
            self.panel.toggle_component(root_row)
        self.panel.toggle_instances(group)
        self.panel.refresh()
        group = self.panel.structure.topLevelItem(0).child(0)
        self.assertEqual(group.childCount(), 5)
        self.assertTrue(group.isExpanded())
        self.assertEqual(group.child(4).text(0), "support_angle#005")
        instance = group.child(4)
        self.panel.activate_item(instance)
        self.panel.refresh()
        group = self.panel.structure.topLevelItem(0).child(0)
        self.assertTrue(group.child(4).font(0).bold())
        with self.assertRaises(ValueError):
            self.panel.set_part_view(group, "Hidden")
        last = Model.children(self.root)[4]
        last.Visibility = False
        self.assertTrue(last.Visibility)
        first = group.child(0)
        self.panel.toggle_component(first)
        self.assertEqual(Model.representation(self.root, [link.ObjectId]), "Hidden")
        self.panel.toggle_component(first)
        self.assertEqual(Model.representation(self.root, [link.ObjectId]), "Bodies Only")
        menu = self.panel.build_menu(self.panel.structure, group.child(4))
        self.assertIn("Save to External File", [a.text() for a in menu.actions()])
        submenus = {child.title(): child for child in menu.component_submenus}
        self.assertEqual([a.text() for a in submenus["Instances"].actions()],
                         ["Add Instance", "Copy to New Part"])
        self.assertEqual([a.text() for a in submenus["Part View"].actions()],
                         ["Full Component", "Bodies Only", "Hidden", "Reset to Inherited"])
        submenus["Instances"].popup(QtCore.QPoint(100, 100))
        Gui.updateGui()
        submenus["Instances"].grab().save(str(self.output / "component-instances-menu.png"))
        submenus["Instances"].hide()
        self.panel.tabs.setCurrentWidget(self.panel.structure)
        self.panel.resize(600, 500)
        Gui.updateGui()
        self.panel.grab().save(str(self.output / "component-grouped-instances.png"))
        self.panel.activate_item(self.panel.structure.topLevelItem(0))
        profile = self.profile(2)
        operation, result = Extrude.create(self.root, profile, 5)
        self.panel.refresh()
        row = next(self.panel.history.topLevelItem(i) for i in range(self.panel.history.topLevelItemCount())
                   if self.panel.history.topLevelItem(i).data(0, QtCore.Qt.UserRole) == Navigator.object_key(profile))
        self.assertEqual(row.text(2), profile.Label)
        self.assertEqual(row.checkState(0), QtCore.Qt.Checked)
        self.panel.toggle_item_view(row)
        self.assertTrue(profile.Visibility)
        row.setCheckState(0, QtCore.Qt.Unchecked)
        self.assertTrue(profile.UserSuppressed)
        self.assertEqual(Model.history_state(operation), "Inactive \u2014 dependency")
        self.assertTrue(result.Shape.isNull())
        self.panel.tabs.setCurrentWidget(self.panel.history)
        Gui.updateGui()
        self.panel.grab().save(str(self.output / "component-history-controls.png"))
        Model.set_suppressed(profile, False)
        self.assertAlmostEqual(result.Shape.Volume, 20 * math.pi)
        self.assertTrue(profile.Visibility)
        self.doc.saveAs(str(self.output / "Component-Panel-Feedback.cadprt"))
        self.assertNotIn(".cadprt", self.panel.context.text())
