# SPDX-License-Identifier: LGPL-2.1-or-later
"""Small feedback-round smoke check, not full component-schema qualification."""
import hashlib
import math
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
import CadDocument
import ComponentModel as Model
import ComponentExtrude as Extrude
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentExtrudeTask as Task


class TestComponentIteration(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, relative in [(Model, "src/Mod/Part/ComponentModel.py"),
                                 (Extrude, "src/Mod/Part/ComponentExtrude.py"),
                                 (Task, "src/Gui/ComponentExtrudeTask.py"),
                                 (Navigator, "src/Gui/ComponentNavigator.py")]:
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((source / relative).read_bytes()).digest())
        Gui.activateWorkbench("PartDesignWorkbench")
        self.doc = Model.new_document("Component feedback")
        self.root = Model.metadata(self.doc).RootComponent
        self.panel = Navigator.show(self.doc)
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])

    def tearDown(self):
        if Task._task:
            Task._task.reject()
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def profile(self, name, radius):
        obj = self.doc.addObject("Sketcher::SketchObject", name)
        Model.register_object(self.root, obj)
        obj.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), radius))
        self.doc.recompute()
        return obj

    def testNativeCommandTaskEditAndReopen(self):
        profile = self.profile("Profile", 2)
        Gui.Selection.clearSelection()
        before = len(self.doc.Objects)
        Gui.runCommand("PartDesign_Extrude")
        task = Task._task
        self.assertIsNotNone(task)
        self.assertIsNone(task.profile.currentData())
        task.profile.setCurrentIndex(task.profile.findData(profile.Name))
        self.assertTrue(task.preview(), task.status.text())
        self.assertEqual(len(self.doc.Objects), before)
        task.reject()
        self.assertEqual(len(self.doc.Objects), before)
        Gui.runCommand("PartDesign_Pad")
        task = Task._task
        task.profile.setCurrentIndex(task.profile.findData(profile.Name))
        Gui.updateGui()
        task.form.grab().save(str(self.output / "component-extrude-task.png"))
        if not task.accept():
            self.fail(task.status.text())
        body = task.result
        self.assertAlmostEqual(body.Shape.Volume, 40 * math.pi)
        self.assertFalse(any(obj.TypeId == "PartDesign::Body" for obj in self.doc.Objects))
        self.panel.edit_history(Navigator.object_key(body))
        task = Task._task
        task.length.setProperty("rawValue", 12.0)
        if not task.accept():
            self.fail(task.status.text())
        self.assertAlmostEqual(body.Shape.Volume, 48 * math.pi)
        hole = self.profile("HoleProfile", 1)
        Gui.runCommand("PartDesign_Pocket")
        task = Task._task
        self.assertEqual(task.mode.currentData(), "Subtract")
        task.profile.setCurrentIndex(task.profile.findData(hole.Name))
        task.target.setCurrentIndex(task.target.findData(body.Name))
        task.length.setProperty("rawValue", 12.0)
        if not task.accept():
            self.fail(task.status.text())
        result = task.result
        identity = result.ObjectId
        self.assertAlmostEqual(result.Shape.Volume, 36 * math.pi)
        path = self.output / "Component-Feedback.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(path)
        result = next(obj for obj in self.doc.Objects if getattr(obj, "ObjectId", "") == identity)
        self.assertAlmostEqual(result.Shape.Volume, 36 * math.pi)
        self.assertEqual(result.Producer.ExtrudeMode, "Subtract")

    def testAddEditSuppressionAndFailureRollback(self):
        profile = self.profile("SharedProfile", 2)
        first, body = Extrude.create(self.root, profile, 5)
        added, result = Extrude.create(self.root, profile, 10, "Add", body)
        self.assertAlmostEqual(result.Shape.Volume, 40 * math.pi)
        identity = result.ObjectId
        Extrude.edit(added, profile, 12)
        self.assertEqual(result.ObjectId, identity)
        self.assertAlmostEqual(result.Shape.Volume, 48 * math.pi)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 40 * math.pi)
        Model.set_suppressed(first, True)
        self.assertEqual(Model.history_state(first), "Suppressed")
        self.assertEqual(Model.history_state(added), "Inactive — dependency")
        self.assertTrue(result.Shape.isNull())
        Model.set_suppressed(first, False)
        self.assertAlmostEqual(result.Shape.Volume, 40 * math.pi)
        remote = self.profile("RemoteProfile", 1)
        remote.Placement.Base.x = 100
        self.doc.recompute()
        count = len(self.doc.Objects)
        with self.assertRaises(ValueError):
            Extrude.create(self.root, remote, 5, "Add", result)
        self.assertEqual(len(self.doc.Objects), count)
        self.assertAlmostEqual(result.Shape.Volume, 40 * math.pi)

    def testAtomicComponentCreationAndNavigatorState(self):
        count = len(self.doc.Objects)
        link = Model.add_component(self.root, label="Child")
        self.assertTrue(Model.is_component(link.LinkedObject))
        self.doc.undo()
        self.assertEqual(len(self.doc.Objects), count)
        self.doc.redo()
        self.panel.refresh()
        root_row = self.panel.structure.topLevelItem(0).child(0)
        root_row.setExpanded(False)
        root_row.setSelected(True)
        self.panel.refresh()
        root_row = self.panel.structure.topLevelItem(0).child(0)
        self.assertFalse(root_row.isExpanded())
        self.assertTrue(root_row.isSelected())
        operation, result = Extrude.create(self.root, self.profile("Profile", 2), 5)
        self.panel.refresh()
        row = self.panel.history.topLevelItem(self.panel.history.topLevelItemCount() - 1)
        row.setSelected(True)
        Model.set_suppressed(operation, True)
        self.panel.refresh()
        selected = self.panel.history.selectedItems()
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].data(0, 256), Navigator.object_key(operation))
        self.panel.tabs.setCurrentWidget(self.panel.history)
        Gui.updateGui()
        self.panel.grab().save(str(self.output / "component-history-states.png"))
