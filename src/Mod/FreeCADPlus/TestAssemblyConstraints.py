# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native part-owned joints, local frames, lifecycle, and recursive collectors."""
import os
import unittest
from pathlib import Path
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import constraints, document, hierarchy, editing, panel


def ref(obj, sub=''):
    return (obj, [sub, sub])


class TestAssemblyConstraints(unittest.TestCase):
    def setUp(self):
        self.before = set(App.listDocuments())
        self.output = Path(os.environ['PLUS_TEST_DIR']) / self._testMethodName
        self.output.mkdir(exist_ok=True)
        Gui.Selection.clearSelection()
        self.doc = document.new_document('ConstraintFixture')
        self.root = document.validate(self.doc)
        self.owner = self.root.Definitions[0]; self.owner.Label = 'Machine'
        self.child = hierarchy.create_definition(self.doc, 'Drive unit')
        self.grand = hierarchy.create_definition(self.doc, 'Mounting plate')
        self.link = hierarchy.add_instance(self.owner, self.child)
        self.nested = hierarchy.add_instance(self.child, self.grand)
        self.link.LinkPlacement = App.Placement(App.Vector(20, 10, 5), App.Rotation())
        self.doc.recompute()
        editing.edit((self.root.Group[0], self.link))
        self.dock = panel.show_panel(); self.dock.activate_assembly(self.owner)
        Gui.getMainWindow().resizeDocks([self.dock],[370],QtCore.Qt.Horizontal)
        self.dock.tabs.setCurrentIndex(1)
        QtTest.QTest.qWait(80)

    def tearDown(self):
        import JointObject
        if JointObject.activeTask:
            JointObject.activeTask.reject()
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        QtTest.QTest.qWait(80)

    def fixed(self, owner=None, link=None):
        owner = owner or self.owner; link = link or self.link
        return constraints.create(owner, 'Fixed', [ref(owner.Origin), ref(link)])

    def test_fixed_parent_frame_without_grounded_children(self):
        occurrence = self.root.Group[0]
        occurrence.LinkPlacement = App.Placement(App.Vector(85, 20, 30), App.Rotation(App.Vector(0,0,1), 35))
        before = App.Placement(occurrence.LinkPlacement)
        joint = self.fixed()
        self.assertTrue(self.link.LinkPlacement.isSame(App.Placement(), 1e-7))
        self.assertTrue(before.isSame(occurrence.LinkPlacement, 1e-9))
        solver = constraints.solver_for(self.owner)
        self.assertFalse(solver.isPartGrounded(self.link))
        self.assertFalse(any('ObjectToGround' in o.PropertiesList for o in self.doc.Objects))
        self.assertEqual(joint.Reference1[0], self.owner.Origin)
        self.assertEqual(document.validate(self.doc), self.root)

    def test_parent_geometry_is_stationary(self):
        with document.transaction(self.doc, 'Parent geometry'):
            box = self.owner.newObject('Part::Box', 'ParentSolid')
            box.Placement.Base = App.Vector(8, 3, 2)
        before = App.Placement(box.Placement)
        constraints.create(self.owner, 'Fixed', [ref(box), ref(self.link)])
        self.assertTrue(before.isSame(box.Placement, 1e-7))
        self.assertTrue(self.link.Placement.isSame(box.Placement, 1e-7))

    def test_unanchored_island_solves_without_saved_ground(self):
        other = hierarchy.add_instance(self.owner, self.grand)
        other.LinkPlacement.Base = App.Vector(7, 9, 11)
        joint = constraints.create(self.owner, 'Fixed', [ref(self.link), ref(other)])
        self.assertTrue(self.link.Placement.isSame(other.Placement, 1e-7))
        self.link.LinkPlacement.Base = App.Vector(44, 12, 9)
        self.doc.recompute()
        self.assertTrue(self.link.Placement.isSame(other.Placement, 1e-7))
        self.assertFalse(constraints.solver_for(self.owner).isPartGrounded(self.link))
        self.assertFalse(any('ObjectToGround' in o.PropertiesList for o in self.doc.Objects))
        self.assertIn(joint, constraints.joints(self.owner))

    def test_nested_collectors_first_collapsed_and_independent(self):
        first = self.fixed(); second = self.fixed(self.child, self.nested)
        self.dock.refresh()
        root = self.dock.trees[1].topLevelItem(0)
        group = root.child(0); nested = root.child(1).child(0)
        self.assertEqual(group.text(0), 'Assembly constraints')
        self.assertEqual(nested.text(0), 'Assembly constraints')
        self.assertFalse(group.isExpanded()); self.assertFalse(nested.isExpanded())
        self.assertEqual(group.child(0).data(0,panel._ROLE).ref, panel.identity(first))
        self.assertEqual(nested.child(0).data(0,panel._ROLE).ref, panel.identity(second))
        group.setExpanded(True); self.dock.refresh(); self.assertTrue(group.isExpanded())
        self.dock.grab().save(str(self.output/'nested-collectors.png'))
        constraints.remove(first); self.dock.refresh()
        self.assertEqual(root.child(0).text(0), self.child.Label)
        self.assertEqual(root.child(0).child(0).text(0), 'Assembly constraints')

    def test_repeated_instances_have_distinct_collectors(self):
        hierarchy.add_instance(self.owner, self.child)
        self.fixed(self.child, self.nested); self.dock.refresh()
        root = self.dock.trees[1].topLevelItem(0)
        groups = [root.child(i).child(0) for i in range(root.childCount())]
        self.assertEqual(len(groups), 2)
        self.assertNotEqual(groups[0].data(0,panel._ROLE).key, groups[1].data(0,panel._ROLE).key)
        self.assertEqual(groups[0].child(0).data(0,panel._ROLE).ref, groups[1].child(0).data(0,panel._ROLE).ref)

    def test_atomic_first_create_undo_redo_and_schema_upgrade(self):
        self.root.PlusSchema = 5
        objects = {o.Name:o.ID for o in self.doc.Objects}
        before = App.Placement(self.link.LinkPlacement)
        joint = self.fixed(); name = joint.Name
        self.doc.undo(); self.doc.recompute()
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, objects)
        self.assertEqual(self.root.PlusSchema, 5)
        self.assertTrue(before.isSame(self.link.LinkPlacement,1e-9))
        self.doc.redo(); self.doc.recompute()
        self.assertEqual(constraints.joints(self.owner)[0].Name, name)
        self.assertEqual(document.validate(self.doc).PlusSchema, 6)

    def test_delete_undo_preserves_constraint_identity(self):
        joint = self.fixed(); identity = panel.identity(joint)
        constraints.remove(joint)
        self.assertFalse(constraints.joints(self.owner))
        self.doc.undo(); self.doc.recompute()
        self.assertEqual(panel.identity(constraints.joints(self.owner)[0]), identity)

    def test_reject_cross_owner_and_self_references_atomically(self):
        objects = {o.Name:o.ID for o in self.doc.Objects}
        for refs in ([ref(self.link),ref(self.nested)], [ref(self.link),ref(self.link)]):
            with self.assertRaises(ValueError): constraints.create(self.owner, 'Fixed', refs)
            self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, objects)
            document.validate(self.doc)

    def test_history_excludes_constraint_backend(self):
        self.fixed()
        self.assertEqual(document.history(self.doc, self.owner), [])
        self.assertNotIn(constraints.solver_for(self.owner), document.history(self.doc,self.owner))

    def test_switch_active_assembly_preserves_placements_and_edit(self):
        self.fixed(); self.fixed(self.child, self.nested)
        before = [(o.Name, str(o.Placement)) for o in self.doc.Objects if hasattr(o,'Placement')]
        context = editing.context_path(self.doc)
        self.dock.activate_assembly(self.child); self.dock.activate_assembly(self.owner)
        self.assertEqual(before, [(o.Name,str(o.Placement)) for o in self.doc.Objects if hasattr(o,'Placement')])
        self.assertEqual(context, editing.context_path(self.doc))

    def test_selection_mapping_through_occurrence_and_nested_owner(self):
        self.fixed(); solver = constraints.solver_for(self.owner)
        prefix = self.root.Group[0].Name + '.'
        self.assertEqual(constraints.component_reference(solver,self.root,prefix+self.link.Name+'.'),(self.link,''))
        self.assertEqual(constraints.component_reference(solver,self.root,prefix+self.owner.Origin.Name+'.'),(self.owner.Origin,''))
        self.fixed(self.child,self.nested); solver = constraints.solver_for(self.child)
        self.assertEqual(constraints.component_reference(solver,self.root,prefix+self.link.Name+'.'+self.nested.Name+'.'),(self.nested,''))

    def test_create_editor_cancel_removes_backend_and_preserves_pose(self):
        objects = {o.Name:o.ID for o in self.doc.Objects}
        before = str(self.link.LinkPlacement)
        task = constraints.open_task()
        task.refs = [ref(self.owner.Origin), ref(self.link)]; task.updateJoint()
        self.assertIsNone(task.error)
        task.reject()
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, objects)
        self.assertEqual(str(self.link.LinkPlacement), before)

    def test_editor_accept_edit_cancel_and_accept_in_place(self):
        task = constraints.open_task()
        task.refs = [ref(self.owner.Origin), ref(self.link)]; task.updateJoint()
        accepted = task.accept()
        self.assertTrue(accepted, task.error)
        joint = constraints.joints(self.owner)[0]; identity = panel.identity(joint)
        task = constraints.open_task(joint=joint)
        task.joint.Offset2 = App.Placement(App.Vector(0,0,8),App.Rotation())
        task.updateJoint(); task.reject()
        self.assertEqual(panel.identity(joint), identity)
        self.assertAlmostEqual(joint.Offset2.Base.z, 0)
        task = constraints.open_task(joint=joint)
        task.joint.Offset2 = App.Placement(App.Vector(0,0,4),App.Rotation())
        task.updateJoint(); self.assertTrue(task.accept(),task.error)
        self.assertEqual(panel.identity(joint), identity)
        self.assertAlmostEqual(joint.Offset2.Base.z,4)
        self.assertAlmostEqual(self.link.Placement.Base.z,-4)

    def test_incomplete_editor_stays_open_with_error(self):
        task = constraints.open_task()
        self.assertFalse(task.accept()); self.assertTrue(task.status.error)
        self.assertTrue(self.doc.HasPendingTransaction)
        task.reject()

    def test_native_commands_follow_active_assembly_not_edited_child(self):
        import CommandCreateJoint
        self.assertEqual(editing.context_path(self.doc)[0], self.child)
        self.assertTrue(CommandCreateJoint.CommandCreateJointFixed().IsActive())
        self.assertTrue(CommandCreateJoint.CommandCreateJointRevolute().IsActive())
        task = constraints.open_task()
        self.assertEqual(task.owner, self.owner)
        task.reject()

    def test_equal_padded_tabs_left_aligned(self):
        bar = self.dock.tabs.tabBar()
        QtTest.QTest.qWait(80)
        widths = [bar.tabRect(i).width() for i in range(3)]
        self.assertEqual(len(set(widths)),1)
        self.assertGreater(widths[0],bar.fontMetrics().horizontalAdvance('Assembly')+20)
        self.assertLess(bar.mapTo(self.dock.tabs,QtCore.QPoint()).x(),4)
        self.dock.grab().save(str(self.output/'tabs.png'))

    def test_save_fixture_for_fresh_reopen(self):
        self.fixed(); self.fixed(self.child,self.nested)
        with document.transaction(self.doc,'Add geometry'):
            shape = self.child.newObject('Part::Box','SavedSolid')
            shape.Length = 3; shape.Width = 4; shape.Height = 5
        document.save_document(self.doc, self.output/'Constrained assembly.cadprt')
        self.assertTrue((self.output/'Constrained assembly.cadprt').exists())
        import json
        (self.output/'fixture.json').write_text(json.dumps({
            'uid':str(self.doc.Uid),'owner':self.owner.Name,'child':self.child.Name,
            'link':self.link.Name,'nested':self.nested.Name,'shape':shape.Name,
            'objects':{o.Name:o.ID for o in self.doc.Objects}},indent=2))

    def test_classic_solver_has_no_component_owner(self):
        doc = App.newDocument('Classic')
        native = doc.addObject('Assembly::AssemblyObject','Assembly')
        self.assertIsNone(constraints.owner_of(native))
        self.assertFalse(constraints.is_plus_document(doc))

    def test_native_command_and_live_selection_create_real_joint(self):
        import CommandCreateJoint, JointObject
        CommandCreateJoint.activateJoint(0)
        task = JointObject.activeTask
        prefix = self.root.Group[0].Name + '.'
        Gui.Selection.addSelection(self.doc.Name,self.root.Name,prefix+self.owner.Origin.Name+'.')
        Gui.Selection.addSelection(self.doc.Name,self.root.Name,prefix+self.link.Name+'.')
        QtTest.QTest.qWait(80)
        self.assertEqual([r[0] for r in task.refs],[self.owner.Origin,self.link])
        self.assertIsNone(task.error)
        task.form.grab().save(str(self.output/'native-constraint-task.png'))
        self.assertTrue(task.accept(),task.error)
        self.dock.refresh()
        self.assertEqual(self.dock.trees[1].topLevelItem(0).child(0).text(0),'Assembly constraints')

    def test_selected_parent_and_child_are_initial_references(self):
        Gui.Selection.addSelection(self.owner)
        Gui.Selection.addSelection(self.link)
        task = constraints.open_task()
        self.assertEqual([r[0] for r in task.refs],[self.owner.Origin,self.link])
        self.assertTrue(task.accept(),task.error)

    def test_revolute_joint_retains_rotation_freedom(self):
        joint = constraints.create(self.owner,'Revolute',[ref(self.owner.Origin),ref(self.link)])
        self.link.LinkPlacement = App.Placement(App.Vector(),App.Rotation(App.Vector(0,0,1),32))
        self.doc.recompute()
        self.assertLess(self.link.Placement.Base.Length,1e-6)
        self.assertAlmostEqual(self.link.Placement.Rotation.Angle,32*3.141592653589793/180,places=6)
        self.assertEqual(joint.JointType,'Revolute')

    def test_constraint_frame_cannot_be_moved(self):
        self.fixed(); solver = constraints.solver_for(self.owner)
        with self.assertRaises(ValueError):
            with document.transaction(self.doc,'Bad solver placement'):
                solver.Placement = App.Placement(App.Vector(1,2,3),App.Rotation())
        self.assertTrue(solver.Placement.isSame(App.Placement(),1e-9))

    def test_conflicting_editor_does_not_commit_or_move_parent(self):
        self.fixed()
        before = App.Placement(self.link.Placement)
        task = constraints.open_task(0)
        task.refs = [ref(self.owner.Origin),ref(self.link)]
        task.joint.Offset2 = App.Placement(App.Vector(0,0,10),App.Rotation())
        accepted = task.accept()
        details = [(j.Label,str(j.Offset2),str(j.Placement1),str(j.Placement2),str(j.State),j.Suppressed) for j in constraints.joints(self.owner)]
        self.assertFalse(accepted, str(details))
        self.assertTrue(task.status.error)
        task.reject()
        self.assertEqual(len(constraints.joints(self.owner)),1)
        self.assertTrue(self.link.Placement.isSame(before,1e-7))

    def test_solve_command_uses_active_assembly(self):
        import CommandSolveAssembly
        command = CommandSolveAssembly.CommandSolveAssembly()
        self.assertFalse(command.IsActive())
        self.fixed()
        self.assertTrue(command.IsActive())
        self.link.LinkPlacement = App.Placement(App.Vector(9,2,4),App.Rotation())
        command.Activated()
        self.assertTrue(self.link.LinkPlacement.isSame(App.Placement(),1e-7))

    def test_consistent_redundancy_is_not_a_conflict(self):
        self.fixed(); self.fixed()
        self.assertEqual(len(constraints.joints(self.owner)),2)
        self.assertEqual(constraints.solver_for(self.owner).solve(),0)

    def test_joint_markers_use_owner_coordinates(self):
        self.root.Group[0].LinkPlacement = App.Placement(App.Vector(50,40,30),App.Rotation(App.Vector(0,0,1),45))
        joint = self.fixed()
        joint.ViewObject.Proxy.redrawJointPlacements(joint)
        translation = joint.ViewObject.Proxy.switch_JCS2.transform.translation.getValue()
        self.assertLess(App.Vector(*translation.getValue()).Length,1e-7)

    def test_face_references_in_nested_geometry(self):
        with document.transaction(self.doc,'Shape references'):
            box = self.child.newObject('Part::Box','ChildSolid')
            parent = self.owner.newObject('Part::Box','ParentSolid')
            parent.Placement = App.Placement(App.Vector(5,2,1),App.Rotation())
        joint = constraints.create(self.owner,'Fixed',[
            ref(parent,'Face1'),ref(self.link,box.Name+'.Face1')])
        import UtilsAssembly
        solver = constraints.solver_for(self.owner)
        a=UtilsAssembly.getJcsGlobalPlc(joint.Placement1,joint.Reference1,solver)
        b=UtilsAssembly.getJcsGlobalPlc(joint.Placement2,joint.Reference2,solver)
        self.assertTrue(a.isSame(b,1e-6))
        self.assertEqual(joint.Reference2[0],self.link)

    def test_reference_and_excluded_children_are_rejected(self):
        from freecad_plus import display
        # Exercise the shared saved state API rather than only the picker.
        for kind in ('Reference','Excluded'):
            display.set_state(self.owner, self.link, part_type=kind)
            with self.assertRaises(ValueError): self.fixed()

    def test_existing_external_child_constraints_write_only_owning_file(self):
        document.save_document(self.doc,self.output/'Host.cadprt')
        source=document.new_document('Existing library')
        part=document.validate(source).Definitions[0]
        with document.transaction(source,'Library geometry'):
            box=part.newObject('Part::Box','Solid')
        document.save_document(source,self.output/'Library.cadprt')
        snapshot={o.Name:(o.ID,str(o.Placement) if hasattr(o,'Placement') else '') for o in source.Objects}
        App.setActiveDocument(self.doc.Name)
        link=hierarchy.add_child(self.owner,part)
        joint=constraints.create(self.owner,'Fixed',[ref(self.owner.Origin),ref(link,box.Name+'.')])
        self.assertEqual(joint.Document,self.doc)
        self.assertEqual(joint.Reference2[0],link)
        self.assertEqual({o.Name:(o.ID,str(o.Placement) if hasattr(o,'Placement') else '') for o in source.Objects},snapshot)
        document.validate(self.doc)

    def test_constraint_row_double_click_reuses_editor(self):
        joint=self.fixed();self.dock.refresh()
        item=self.dock.trees[1].topLevelItem(0).child(0).child(0)
        self.dock._edit_clicked(item)
        import JointObject
        self.assertEqual(JointObject.activeTask.joint,joint)
        self.assertFalse(JointObject.activeTask.creating)
        JointObject.activeTask.reject()
