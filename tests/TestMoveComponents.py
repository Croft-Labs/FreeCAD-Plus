# SPDX-License-Identifier: LGPL-2.1-or-later
"""Real native links, component frames, transactions and Qt task controls."""
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
from PySide import QtCore, QtWidgets
from freecad.gui import MoveComponents as Move
from freecad.gui import MoveComponentsTask as UI
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentSelection as Selection
from freecad.gui import DesignSelection


class TestMoveComponents(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = Model.new_document("Move assembly")
        self.root = Model.metadata(self.doc).RootComponent
        self.a = Model.add_component(self.root, label="Parent")
        self.parent = self.a.LinkedObject
        self.b = Model.add_component(self.root, self.parent)
        self.a.LinkPlacement = App.Placement(App.Vector(40, 20, 10), App.Rotation(App.Vector(0, 0, 1), 90))
        self.b.LinkPlacement = App.Placement(App.Vector(-15, 5, 20), App.Rotation(App.Vector(0, 1, 0), 60))
        self.parent.Placement = App.Placement(App.Vector(3, 4, 5), App.Rotation(App.Vector(1, 0, 0), 15))
        self.first = Model.add_component(self.parent, label="Bracket")
        self.second = Model.add_component(self.parent, self.first.LinkedObject)
        self.second.LinkPlacement.Base = App.Vector(10, 20, 30)
        self.descendant = Model.add_component(self.first.LinkedObject, label="Pin")
        self.box = self.doc.addObject("Part::Feature", "Stock")
        self.box.Shape = Part.makeBox(2, 3, 4)
        Model.register_object(self.descendant.LinkedObject, self.box, "Object", True)
        self.line = self.doc.addObject("Part::Feature", "Direction")
        self.line.Shape = Part.makeLine(App.Vector(), App.Vector(5, 0, 0))
        Model.register_object(self.root, self.line)
        self.doc.recompute()
        self.panel = Navigator.show(self.doc)
        self.panel.root_key = Navigator.object_key(self.root)
        self.panel.active_key = Navigator.object_key(self.root)
        self.panel.active_path = []
        self.panel.refresh()
        Gui.Selection.clearSelection()
        DesignSelection.parameters().SetBool("Active", True)
        DesignSelection.parameters().SetBool("Persistent", True)
        self.paths = [(self.a.ObjectId, self.first.ObjectId), (self.a.ObjectId, self.second.ObjectId)]

    def tearDown(self):
        if UI._task:
            UI._task.reject()
        Gui.Selection.clearSelection()
        for doc in reversed(list(App.listDocuments().values())):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def session(self):
        session = Move.Session(self.root)
        session.add(self.paths)
        return session

    def vector(self, actual, expected):
        self.assertLess((actual - expected).Length, 1e-7)

    def rendered_center(self, parent):
        # Native evaluated path is the oracle, independently of Move's frame conversion.
        path = parent.Name + "." + self.first.Name + "." + self.descendant.Name + "." + self.box.Name + "."
        return Part.getShape(self.root, path, needSubElement=True, transform=True).CenterOfMass

    def test_parent_relative_shared_occurrences_and_implicit_descendants(self):
        session = self.session()
        before = [self.rendered_center(link) for link in (self.a, self.b)]
        frames = [Model._component_frame(self.root, (link.ObjectId,)) for link in (self.a, self.b)]
        child = App.Placement(self.descendant.LinkPlacement)
        geometry = self.box.Shape.hashCode()
        identities = [(obj.Name, obj.ObjectId) for obj in Model.definitions(self.doc)]
        relative = self.first.LinkPlacement.inverse().multiply(self.second.LinkPlacement)
        session.direction, session.distance = App.Vector(1, 0, 0), 7.
        self.assertTrue(session.commit(session.translation()))
        self.vector(self.first.LinkPlacement.Base, App.Vector(7, 0, 0))
        for old, link, frame in zip(before, (self.a, self.b), frames):
            self.vector(self.rendered_center(link) - old, frame.Rotation.multVec(App.Vector(7, 0, 0)))
        self.assertTrue(child.isSame(self.descendant.LinkPlacement, 1e-9))
        self.assertTrue(relative.isSame(self.first.LinkPlacement.inverse().multiply(self.second.LinkPlacement), 1e-9))
        self.assertEqual(geometry, self.box.Shape.hashCode())
        self.assertEqual(identities, [(obj.Name, obj.ObjectId) for obj in Model.definitions(self.doc)])

    def test_standalone_parent_uses_same_owned_child(self):
        session = self.session()
        session.direction, session.distance = App.Vector(0, 1, 0), 6.
        session.commit(session.translation())
        self.panel.open_component_tab(Navigator.object_key(self.parent))
        Gui.updateGui()
        standalone = Move.Session(self.parent)
        standalone.add([(self.first.ObjectId,)])
        self.assertEqual(standalone.links(), [self.first])
        self.vector(standalone.links()[0].LinkPlacement.Base, App.Vector(0, 6, 0))
        standalone.direction, standalone.distance = App.Vector(0, 0, 1), 3.
        standalone.commit(standalone.translation())
        self.vector(self.first.LinkPlacement.Base, App.Vector(0, 6, 3))

    def test_atomic_siblings_only_and_root_rejection(self):
        session = Move.Session(self.root)
        for paths in ([(), self.paths[0]], [self.paths[0], (self.b.ObjectId,)],
                      [self.paths[0], (self.b.ObjectId, self.second.ObjectId)],
                      [self.paths[0], self.paths[0] + (self.descendant.ObjectId,)]):
            with self.assertRaises(ValueError):
                session.add(paths)
            self.assertEqual(session.paths, [])
            self.assertIsNone(session.parent)
        session.add(self.paths)
        with self.assertRaises(ValueError):
            session.add([(self.b.ObjectId,)])
        self.assertEqual(session.paths, self.paths)

    def test_world_reference_rotation_only_and_straight_validation(self):
        session = self.session()
        direction = Move.reference_direction(session, self.root, self.line.Name + ".Edge1")
        self.vector(session.frame().Rotation.multVec(direction), App.Vector(1, 0, 0))
        local = Move.reference_direction(session, self.line, "Edge1")
        self.vector(local, direction)
        self.line.Shape = Part.makeCircle(2)
        with self.assertRaisesRegex(ValueError, "Curved"):
            Move.reference_direction(session, self.line, "Edge1")
        with self.assertRaises(ValueError):
            session.world_direction(App.Vector())

    def test_occurrence_reference_and_native_axis_snapshot(self):
        line = self.doc.addObject("Part::Feature", "ChildLine")
        line.Shape = Part.makeLine(App.Vector(), App.Vector(0, 8, 0))
        Model.register_object(self.first.LinkedObject, line)
        self.doc.recompute()
        session = self.session()
        path = self.b.Name + "." + self.first.Name + "." + line.Name + ".Edge1"
        direction = Move.reference_direction(session, self.root, path)
        edge = Part.getShape(self.root, path, needSubElement=True, transform=True)
        self.vector(session.frame().Rotation.multVec(direction), edge.tangentAt(edge.FirstParameter))
        axis = next(obj for obj in self.root.Origin.OriginFeatures if obj.isDerivedFrom("App::Line"))
        direction = Move.reference_direction(session, axis, "")
        self.assertAlmostEqual(direction.Length, 1.)
        old = tuple(direction)
        line.Placement.Base = App.Vector(30, 40, 50)
        self.assertEqual(tuple(direction), old, "No associative reference was created")

    def test_preview_is_transient_and_group_reverse(self):
        session = self.session()
        ids = [obj.ID for obj in self.doc.Objects]
        placement = App.Placement(self.first.LinkPlacement)
        undo = self.doc.UndoCount
        session.direction, session.distance, session.reverse = App.Vector(2, 0, 0), 5., True
        shapes = session.preview_shapes(session.translation())
        self.assertEqual(len(shapes), 4, "Preview both siblings in both displayed parent occurrences")
        self.assertEqual(ids, [obj.ID for obj in self.doc.Objects])
        self.assertEqual(undo, self.doc.UndoCount)
        self.assertTrue(placement.isSame(self.first.LinkPlacement, 1e-9))
        self.assertTrue(session.commit(session.translation()))
        self.vector(self.first.LinkPlacement.Base, App.Vector(-5, 0, 0))
        self.assertIsNone(session.direction)
        self.assertFalse(session.reverse)
        self.assertEqual(session.distance, 0)

    def test_atomic_undo_redo_save_and_noop(self):
        session = self.session()
        undo = self.doc.UndoCount
        self.assertFalse(session.commit(App.Placement()))
        self.assertEqual(undo, self.doc.UndoCount)
        session.direction, session.distance = App.Vector(0, 0, 1), 9.
        session.commit(session.translation())
        self.assertEqual(self.doc.UndoCount, undo + 1)
        self.doc.undo()
        self.vector(self.first.LinkPlacement.Base, App.Vector())
        self.vector(self.second.LinkPlacement.Base, App.Vector(10, 20, 30))
        self.doc.redo()
        files = []
        name, identity = self.first.Name, self.first.ObjectId
        for extension in ("FCStd", "cadprt"):
            filename = str(Path(tempfile.gettempdir()) / ("move-roundtrip." + extension))
            self.doc.saveAs(filename)
            files.append(filename)
        App.closeDocument(self.doc.Name)
        for filename in files:
            other = App.openDocument(filename)
            self.vector(other.getObject(name).LinkPlacement.Base, App.Vector(0, 0, 9))
            self.assertEqual(other.getObject(name).ObjectId, identity)
            App.closeDocument(other.Name)

    def test_guards_stale_context_and_atomic_failure(self):
        session = self.session()
        session.direction, session.distance = App.Vector(1, 0, 0), 3.
        self.second.setPropertyStatus("LinkPlacement", "ReadOnly")
        with self.assertRaises(ValueError):
            session.commit(session.translation())
        self.vector(self.first.LinkPlacement.Base, App.Vector())
        self.second.setPropertyStatus("LinkPlacement", "-ReadOnly")
        with patch.object(Model, "validate", side_effect=ValueError("transaction failure")):
            with self.assertRaises(ValueError):
                session.commit(session.translation())
        self.vector(self.first.LinkPlacement.Base, App.Vector())
        self.a.LinkPlacement.Base = App.Vector(100, 20, 30)
        with self.assertRaisesRegex(ValueError, "changed"):
            session.commit(session.translation())
        session.reset()
        session.distance = -1
        with self.assertRaises(ValueError):
            session.translation()

    def test_task_apply_ok_cancel_and_persistence(self):
        task = UI.open_task(self.root, self.paths)
        self.assertEqual(tuple(task.workflow.itemText(i) for i in range(6)), Move.WORKFLOWS)
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.parent))
        self.assertEqual(self.panel.active_path, [self.a.ObjectId])
        task.direction.setCurrentIndex(1)
        task.distance.setProperty("rawValue", 4.)
        self.assertTrue(task.ghosts)
        Gui.updateGui()
        apply_button = next(button for button in Gui.getMainWindow().findChildren(QtWidgets.QPushButton)
                            if button.text().replace("&", "") == "Apply" and button.isVisible())
        apply_button.click()  # Exercise the native task-panel clicked(button) adapter.
        self.vector(self.first.LinkPlacement.Base, App.Vector(4, 0, 0))
        self.assertEqual(task.session.paths, self.paths)
        self.assertEqual(task.direction.currentIndex(), 0)
        self.assertEqual(task.distance.property("rawValue"), 0)
        self.assertFalse(task.reverse.isChecked())
        undo = self.doc.UndoCount
        next(button for button in Gui.getMainWindow().findChildren(QtWidgets.QPushButton)
             if button.text().replace("&", "") == "OK" and button.isVisible()).click()
        self.assertTrue(task.closed)
        self.assertEqual(self.doc.UndoCount, undo)
        self.vector(self.first.LinkPlacement.Base, App.Vector(4, 0, 0))
        task = UI.open_task(self.root, self.paths)
        task.direction.setCurrentIndex(2)
        task.distance.setProperty("rawValue", 5.)
        task.apply()
        task.direction.setCurrentIndex(3)
        task.distance.setProperty("rawValue", 100.)
        task.reject()
        self.vector(self.first.LinkPlacement.Base, App.Vector(4, 5, 0))
        self.doc.undo()
        self.vector(self.first.LinkPlacement.Base, App.Vector(4, 0, 0))
        DesignSelection.parameters().SetBool("Persistent", False)
        task = UI.open_task(self.root, self.paths)
        task.direction.setCurrentIndex(1)
        task.distance.setProperty("rawValue", 1.)
        self.assertTrue(task.apply(), task.status.text())
        self.assertEqual(task.session.paths, [])
        self.assertEqual(Gui.Selection.getSelection(), [])
        self.assertEqual(task.session.parent, self.parent)

    def test_task_collectors_errors_workflow_and_lifecycle(self):
        task = UI.open_task(self.root, [self.paths[0]])
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.root, Selection.native_path(self.root, self.paths[1]))
        task.collect()
        self.assertEqual(task.session.paths, self.paths)
        task.direction.setCurrentIndex(1)
        task.distance.setProperty("rawValue", 4.)
        task.workflow.setCurrentIndex(2)
        self.assertFalse(task.ghosts)
        self.assertEqual(task.session.paths, self.paths)
        self.assertIn("Source", task.status.text())
        task.workflow.setCurrentIndex(0)
        task.direction.setCurrentIndex(4)
        Gui.Selection.addSelection(self.line, "Edge1")
        task.collect()
        self.assertIsNotNone(task.session.direction)
        task.distance.setProperty("rawValue", 2.)
        task.collector.curves.item(1).setSelected(True)
        task.remove()
        self.assertEqual(task.session.paths, self.paths[:1])
        task.clear()
        self.assertEqual(task.collector.curves.count(), 0)
        self.assertTrue(task.add_paths([self.paths[0]]))
        self.assertFalse(task.add_paths([(self.b.ObjectId,)]))
        self.assertEqual(task.session.paths, self.paths[:1])
        self.assertIn("siblings", task.status.text())
        App.closeDocument(self.doc.Name)
        self.assertTrue(task.closed)

    def test_native_joint_subpath_and_driven_guards(self):
        # Same native property type as Assembly JointObject.Reference1: the
        # dependency belongs to root while its subpath traverses the moved link.
        joint = self.doc.addObject("App::FeaturePython", "Joint")
        joint.addProperty("App::PropertyXLinkSub", "Reference1")
        joint.Reference1 = (self.root, [self.a.Name + "." + self.first.Name + "." +
                                       self.descendant.Name + "." + self.box.Name + ".Face1"])
        with self.assertRaisesRegex(ValueError, "joint"):
            self.session()
        self.doc.removeObject(joint.Name)
        self.first.setExpression("Placement.Base.x", "2 mm")
        with self.assertRaisesRegex(ValueError, "Driven"):
            self.session()

    def test_precise_selection_and_command_route(self):
        UI.registerCommand()
        with self.assertRaisesRegex(ValueError, "unambiguous"):
            Move.selection_paths(self.root, [SimpleNamespace(Object=self.first, SubElementNames=[])])
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.root, Selection.native_path(self.root, self.paths[0]))
        Gui.runCommand("Std_MoveComponents")
        Gui.updateGui()
        task = UI._task
        self.assertIsNotNone(task)
        self.assertEqual(task.session.paths, self.paths[:1])
        task.form.resize(350, 650)
        task.form.grab().save(str(Path(tempfile.gettempdir()) / "move-task.png"))
        task.direction.setCurrentIndex(2)
        task.distance.setProperty("rawValue", 2.)
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()
        Gui.updateGui()
        Gui.getMainWindow().grab().save(str(Path(tempfile.gettempdir()) / "move-preview.png"))
        self.assertTrue(task.accept())
        self.vector(self.first.LinkPlacement.Base, App.Vector(0, 2, 0))


if __name__ == "__main__":
    unittest.main()
