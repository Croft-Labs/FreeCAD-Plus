# SPDX-License-Identifier: LGPL-2.1-or-later
import json, os, unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
import FreeCAD as App, FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, hierarchy, editing, panel, constraints, display, instance_patterns
from freecad_plus import instance_remove as removal
from freecad_plus.instance_remove_ui import RemoveDialog


class TestInstanceRemoval(unittest.TestCase):
    def setUp(self):
        self.before = set(App.listDocuments())
        self.out = Path(os.environ['PLUS_TEST_DIR']) / self._testMethodName; self.out.mkdir(exist_ok=True)
        Gui.Selection.clearSelection()
        self.doc = document.new_document('Removal')
        self.root = document.validate(self.doc); self.owner = self.root.Definitions[0]; self.owner.Label = 'Machine'
        self.part = hierarchy.create_definition(self.doc, 'Motor')
        with document.transaction(self.doc, 'Geometry'):
            self.box = self.part.newObject('Part::Box', 'Solid')
        self.links = [hierarchy.add_instance(self.owner, self.part,
                      App.Placement(App.Vector(i * 20, 3, 4), App.Rotation())) for i in range(3)]
        self.top = self.root.Group[0]; editing.edit((self.top,))
        self.dock = panel.show_panel(); QtTest.QTest.qWait(80)
        self.dock.activate_assembly(self.owner, (self.top,)); self.dock.tabs.setCurrentIndex(1)
        self.dialogs = []

    def tearDown(self):
        for dialog in self.dialogs: dialog.reject(); dialog.deleteLater()
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before: App.closeDocument(name)
        QtTest.QTest.qWait(80)

    def row(self, link):
        self.dock.refresh()
        return next(item.data(0,panel._ROLE) for item in self.dock._maps[1].values()
                    if item.data(0,panel._ROLE).kind == 'occurrence'
                    and item.data(0,panel._ROLE).path[-1] == panel.identity(link))

    def snapshot(self, doc=None):
        doc = doc or self.doc
        return (tuple((o.Name,o.ID,tuple(panel.identity(v) for v in o.OutList),
                       tuple(o.Placement.toMatrix().A) if hasattr(o,'Placement') else None,
                       repr(getattr(o,'ExpressionEngine',None))) for o in sorted(doc.Objects,key=lambda o:o.Name)),
                doc.UndoCount, editing.context_path(self.doc),
                self.dock._assembly_context(self.dock._binding))

    def dialog(self, link):
        dialog = RemoveDialog(self.dock, self.row(link)); self.dialogs.append(dialog); return dialog

    def fixed(self, link):
        return constraints.create(self.owner,'Fixed',[(self.owner.Origin,['','']), (link,['',''])])

    def test_single_last_cancel_undo_redo_and_selection(self):
        first, selected, last = self.links
        before = self.snapshot(); dialog = self.dialog(selected)
        self.assertTrue(dialog.remove.isEnabled()); self.assertFalse(dialog.remove.isDefault())
        dialog.show(); QtTest.QTest.qWait(80); dialog.grab().save(str(self.out/'simple.png'))
        dialog.reject(); self.assertEqual(self.snapshot(),before)
        row = self.row(selected); other = self.row(first)
        Gui.Selection.addSelection(*row.selection); Gui.Selection.addSelection(*other.selection)
        name, identity = selected.Name, selected.ID; geometry = self.box.Shape.Volume
        expected = removal.plan(self.dock,row); removal.remove(self.dock,expected)
        self.assertIsNone(self.doc.getObject(name)); self.assertEqual(self.doc.UndoCount,before[1]+1)
        self.assertEqual(len([o for o in self.owner.Group if o.TypeId=='App::Link']),2)
        self.assertIn(self.part,self.root.Definitions); self.assertEqual(self.box.Shape.Volume,geometry)
        selections = [(s.DocumentName,s.ObjectName,tuple(s.SubElementNames)) for s in Gui.Selection.getSelectionEx('',0)]
        self.assertTrue(any(other.selection[2] in s[2] for s in selections),selections)
        self.doc.undo(); self.doc.recompute()
        self.assertEqual(self.doc.getObject(name).ID,identity); self.assertEqual(self.snapshot()[0],before[0])
        self.doc.redo(); self.doc.recompute(); self.assertIsNone(self.doc.getObject(name))
        for link in (first,last): removal.remove(self.dock,removal.plan(self.dock,self.row(link)))
        self.assertIn(self.part,self.root.Definitions); self.assertIn(self.box,document.history(self.doc,self.part))
        document.save_document(self.doc,self.out/'UnusedPart.cadprt')
        (self.out/'reopen.json').write_text(json.dumps(dict(file=self.doc.FileName,part=self.part.Name,
            part_id=self.part.ID,box=self.box.Name,box_id=self.box.ID,volume=self.box.Shape.Volume)))

    def test_constraints_opt_in_survivors_fixed_and_collector(self):
        target = self.links[0]; joint = self.fixed(target); survivor = self.fixed(self.links[1])
        self.links[1].LinkPlacement = App.Placement(App.Vector(90,20,1),App.Rotation())
        pose = App.Placement(self.links[1].LinkPlacement)
        before=self.snapshot(); dialog=self.dialog(target)
        self.assertEqual(dialog.plan.constraints,(panel.identity(joint),))
        self.assertFalse(dialog.remove.isEnabled()); self.assertIsNotNone(dialog.constraints)
        dialog.show(); QtTest.QTest.qWait(80); dialog.grab().save(str(self.out/'constraints.png'))
        with self.assertRaisesRegex(ValueError,'Include'): removal.remove(self.dock,dialog.plan)
        self.assertEqual(self.snapshot(),before)
        names=(target.Name,joint.Name); ids=(target.ID,joint.ID)
        prefs=App.ParamGet('User parameter:BaseApp/Preferences/Mod/Assembly'); original=prefs.GetBool('SolveOnRecompute',True)
        dialog.constraints.setChecked(True); dialog.accept()
        self.assertEqual(dialog.result(),QtWidgets.QDialog.Accepted,dialog.status.text())
        self.assertTrue(self.links[1].LinkPlacement.isSame(pose,1e-9))
        self.assertEqual(constraints.joints(self.owner),(survivor,))
        self.assertEqual(prefs.GetBool('SolveOnRecompute',True),original)
        self.doc.undo()
        self.assertEqual(tuple(self.doc.getObject(n).ID for n in names),ids)
        self.assertEqual(self.doc.getObject(names[1]).Reference2[0],self.doc.getObject(names[0]))
        self.doc.redo(); document.validate(self.doc)
        removal.remove(self.dock,removal.plan(self.dock,self.row(self.links[1])),include_constraints=True)
        self.assertFalse(constraints.joints(self.owner))
        root=self.dock.trees[1].topLevelItem(0)
        self.assertFalse(any(root.child(i).text(0)=='Assembly constraints' for i in range(root.childCount())))
        document.save_document(self.doc,self.out/'RemovedConstraints.cadprt')

    def test_block_direct_hidden_indirect_expression_and_constraint_dependents(self):
        target=self.links[0]
        consumer_part=hierarchy.create_definition(self.doc,'Reference consumer')
        for kind in ('direct','hidden','indirect','expression','constraint'):
            joint=self.fixed(target) if kind=='constraint' else None
            with document.transaction(self.doc,'Consumer fixture'):
                consumer=consumer_part.newObject('Part::Feature','Consumer')
                if kind=='expression':
                    consumer.addProperty('App::PropertyLength','Length')
                    consumer.setExpression('Length',target.Name+'.Placement.Base.x')
                else:
                    prop={'direct':'App::PropertyLink','hidden':'App::PropertyLinkHidden',
                          'indirect':'App::PropertyLinkSub','constraint':'App::PropertyLink'}[kind]
                    consumer.addProperty(prop,'Source')
                    consumer.Source=(self.owner,target.Name+'.'+self.box.Name+'.Face1') if kind=='indirect' else (joint or target)
            before=self.snapshot(); expected=removal.plan(self.dock,self.row(target))
            self.assertTrue(expected.blocked,kind)
            with self.assertRaisesRegex(ValueError,'Consumer'):
                removal.remove(self.dock,expected,include_constraints=True)
            self.assertEqual(self.snapshot(),before)
            if kind=='indirect':
                dialog=self.dialog(target); dialog.show(); QtTest.QTest.qWait(80)
                dialog.grab().save(str(self.out/'blocked.png')); dialog.reject()
            with document.transaction(self.doc,'Remove fixture'):
                self.doc.removeObject(consumer.Name)
                if joint: self.doc.removeObject(joint.Name)

    def test_shared_parent_acknowledgement_and_entire_subassembly_preserved(self):
        child=hierarchy.create_definition(self.doc,'Bolt')
        nested=hierarchy.add_instance(self.part,child)
        nested_joint=constraints.create(self.part,'Fixed',[(self.part.Origin,['','']),(nested,['',''])])
        before=self.snapshot(); dialog=self.dialog(nested)
        self.assertTrue(dialog.plan.shared); self.assertFalse(dialog.remove.isEnabled())
        dialog.show(); QtTest.QTest.qWait(80); dialog.grab().save(str(self.out/'shared.png'))
        dialog.constraints.setChecked(True)
        self.assertFalse(dialog.remove.isEnabled()); dialog.shared.setChecked(True)
        dialog.accept(); self.assertEqual(dialog.result(),QtWidgets.QDialog.Accepted,dialog.status.text())
        self.assertTrue(all(not [o for o in link.LinkedObject.Group if o.TypeId=='App::Link'] for link in self.links))
        self.doc.undo(); document.validate(self.doc)
        self.assertIn(nested,self.part.Group); self.assertIn(nested_joint,constraints.joints(self.part))
        removal.remove(self.dock,removal.plan(self.dock,self.row(self.links[0])))
        self.assertIn(nested,self.part.Group); self.assertIn(nested_joint,constraints.joints(self.part))
        self.assertIn(child,self.root.Definitions)

    def test_stale_plan_context_root_group_pattern_and_edit_guards(self):
        row=self.row(self.links[0]); expected=removal.plan(self.dock,row)
        added=hierarchy.add_instance(self.owner,self.part)
        before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'plan changed'): removal.remove(self.dock,expected)
        self.assertEqual(self.snapshot(),before)
        editing.edit((self.top,self.links[0]))
        with self.assertRaisesRegex(ValueError,'Edit ancestor'): removal.plan(self.dock,row)
        editing.edit((self.top,))
        rootrow=self.dock.trees[1].topLevelItem(0).data(0,panel._ROLE)
        with self.assertRaisesRegex(ValueError,'individual child'): removal.plan(self.dock,rootrow)
        self.dock.instance_mode.setCurrentText('Condensed')
        group=next(item.data(0,panel._ROLE) for item in self.dock._maps[1].values() if item.data(0,panel._ROLE).kind=='instance_group')
        with self.assertRaisesRegex(ValueError,'individual child'): removal.plan(self.dock,group)
        links,_=instance_patterns.create(self.owner,[self.part],
            dict(mode='Linear',count=2,position=[0,0,0],direction=[1,0,0],spacing=10))
        expected=removal.plan(self.dock,self.row(links[0])); self.assertIn('Edit instance pattern',expected.blocked[0])
        with self.assertRaisesRegex(ValueError,'pattern'): removal.remove(self.dock,expected)
        expected=removal.plan(self.dock,self.row(self.links[0]))
        other=document.new_document('Other'); document.validate(other).Definitions[0].Label='Other part'
        with self.assertRaisesRegex(ValueError,'tab changed'): removal.remove(self.dock,expected)

    def test_transaction_failure_rolls_back_constraints_link_selection_and_preferences(self):
        link=self.links[0]; self.fixed(link); row=self.row(link)
        Gui.Selection.addSelection(*row.selection); before=self.snapshot()
        expected=removal.plan(self.dock,row); original=document.transaction
        prefs=App.ParamGet('User parameter:BaseApp/Preferences/Mod/Assembly')
        value=prefs.GetBool('SolveOnRecompute',True)
        @contextmanager
        def failing(doc,label):
            with original(doc,label):
                yield
                raise RuntimeError('Injected failure after removal')
        with patch.object(document,'transaction',failing):
            with self.assertRaisesRegex(RuntimeError,'Injected'):
                removal.remove(self.dock,expected,include_constraints=True)
        self.assertEqual(self.snapshot(),before); self.assertEqual(prefs.GetBool('SolveOnRecompute',True),value)
        self.assertTrue(Gui.Selection.getSelectionEx('',0))

    def test_hidden_reference_excluded_and_condensed_singletons(self):
        self.dock.instance_mode.setCurrentText('Condensed')
        for link,kind in zip(self.links,('Full Component','Reference','Excluded')):
            display.set_state(self.owner,link,part_type=kind,shown=False)
            removal.remove(self.dock,removal.plan(self.dock,self.row(link)))
        self.assertIn(self.part,self.root.Definitions); self.assertEqual(len(self.owner.Group),0)

    def test_external_parent_and_source_preservation_fresh_reopen_fixture(self):
        source=document.new_document('Library'); owner=document.validate(source).Definitions[0]; owner.Label='Gearbox'
        child=hierarchy.create_definition(source,'External bolt')
        nested=[hierarchy.add_instance(owner,child) for _ in range(2)]
        document.save_document(source,self.out/'Library.cadprt')
        document.save_document(self.doc,self.out/'Host.cadprt'); App.setActiveDocument(self.doc.Name)
        QtTest.QTest.qWait(100); self.dock.refresh()
        imported=hierarchy.add_child(self.owner,owner); target=nested[0]; name=target.Name
        keep_id=nested[1].ID; before=self.snapshot(); original=source.UndoCount
        expected=removal.plan(self.dock,self.row(target)); self.assertTrue(expected.shared)
        removal.remove(self.dock,expected,acknowledge_shared=True)
        self.assertIsNone(source.getObject(name)); self.assertEqual(source.UndoCount,original+1)
        self.assertEqual(self.snapshot()[0],before[0]); self.assertEqual(self.snapshot()[2:],before[2:])
        self.assertIn(child,document.validate(source).Definitions); self.assertEqual(nested[1].ID,keep_id)
        document.save_document(source); document.save_document(self.doc)
        content=Path(source.FileName).read_bytes()
        removal.remove(self.dock,removal.plan(self.dock,self.row(imported)))
        self.assertEqual(Path(source.FileName).read_bytes(),content)
        self.assertIn(document.validate(source),self.root.Imports)
        self.doc.undo(); document.save_document(self.doc)
        (self.out/'reopen.json').write_text(json.dumps(dict(host=self.doc.FileName,source=source.FileName,
            removed=name,owner=owner.Name,child=child.Name,remaining=nested[1].Name,remaining_id=keep_id,
            host_ids={o.Name:o.ID for o in self.doc.Objects})))

    def test_external_dependent_and_changed_constraint_plan(self):
        target=self.links[0]
        document.save_document(self.doc,self.out/'Target.cadprt')
        other=App.newDocument('ConsumerFile')
        consumer=other.addObject('App::FeaturePython','OutsideConsumer')
        other.saveAs(str(self.out/'Consumer.FCStd'))
        consumer.addProperty('App::PropertyXLinkSub','Source'); consumer.Source=(target,[''])
        App.setActiveDocument(self.doc.Name); QtTest.QTest.qWait(80); self.dock.refresh()
        expected=removal.plan(self.dock,self.row(target)); self.assertTrue(expected.blocked)
        App.closeDocument(other.Name)
        joint=self.fixed(target); expected=removal.plan(self.dock,self.row(target))
        with document.transaction(self.doc,'Rename joint'): joint.Label='Reviewed constraint changed'
        with self.assertRaisesRegex(ValueError,'plan changed'):
            removal.remove(self.dock,expected,include_constraints=True)

    def test_unused_assembly_and_pattern_reference_and_pending_task(self):
        unused=hierarchy.create_definition(self.doc,'Unused assembly')
        child=hierarchy.add_instance(unused,self.part)
        editing.edit_unused(self.doc,unused); self.dock.activate_assembly(unused)
        removal.remove(self.dock,removal.plan(self.dock,self.row(child)))
        self.assertIn(unused,self.root.Definitions); self.assertEqual(unused.Group,[])
        self.assertEqual(editing.context_path(self.doc),(unused,()))
        editing.edit((self.top,)); self.dock.activate_assembly(self.owner,(self.top,))
        instance_patterns.create(self.owner,[self.part],dict(mode='Linear',count=2,
            position=[0,0,0],direction=[1,0,0],spacing=10,reference_keys=['direction']),
            refs=[(self.links[0],[self.box.Name+'.Edge1'])])
        expected=removal.plan(self.dock,self.row(self.links[0]))
        self.assertTrue(any('pattern' in reason for reason in expected.blocked))
        from freecad_plus import instance_task
        task=instance_task.open_task([self.part])
        try:
            with self.assertRaisesRegex(ValueError,'current task'):
                removal.plan(self.dock,self.row(self.links[1]))
        finally: task.reject()

    def test_dialog_stale_dependencies_and_cancel_default(self):
        dialog=self.dialog(self.links[0]); before=self.snapshot()
        dialog.show(); QtTest.QTest.qWait(50)
        QtTest.QTest.keyClick(dialog,QtCore.Qt.Key_Return)
        self.assertEqual(dialog.result(),QtWidgets.QDialog.Rejected)
        self.assertEqual(self.snapshot(),before)
        dialog=self.dialog(self.links[0]); self.fixed(self.links[0]); before=self.snapshot()
        dialog.accept()
        self.assertEqual(dialog.result(),QtWidgets.QDialog.Rejected)
        self.assertIn('plan changed',dialog.status.text()); self.assertEqual(self.snapshot(),before)

    def test_native_menu_delete_cancel_and_ineligible_delete_routing(self):
        target=self.links[0]; row=self.row(target); item=self.dock._maps[1][row.key]
        tree=self.dock.trees[1]; tree.setCurrentItem(item); tree.scrollToItem(item); tree.setFocus()
        errors=[]; seen=[]
        def review_cancel():
            dialog=QtWidgets.QApplication.activeModalWidget()
            try:
                self.assertIsInstance(dialog,RemoveDialog); seen.append('review'); dialog.reject()
            except BaseException as error:
                errors.append(error)
                if dialog: dialog.reject()
        before=self.snapshot(); QtCore.QTimer.singleShot(100,review_cancel)
        QtTest.QTest.keyClick(tree,QtCore.Qt.Key_Delete)
        self.assertFalse(errors); self.assertEqual(seen,['review']); self.assertEqual(self.snapshot(),before)
        def choose_menu():
            menu=QtWidgets.QApplication.activePopupWidget()
            try:
                action=next(a for a in menu.actions() if a.text()=='Remove instance…')
                QtCore.QTimer.singleShot(100,review_cancel); action.trigger(); menu.close()
            except BaseException as error:
                errors.append(error)
                if menu: menu.close()
        QtCore.QTimer.singleShot(100,choose_menu)
        self.dock._menu(tree,tree.visualItemRect(item).center())
        self.assertFalse(errors); self.assertEqual(len(seen),2); self.assertEqual(self.snapshot(),before)
        tree.clearSelection(); tree.setCurrentItem(tree.topLevelItem(0))
        QtTest.QTest.keyClick(tree,QtCore.Qt.Key_Delete); self.assertEqual(self.snapshot(),before)
        self.assertIn('individual child',self.dock.message.text())
        self.dock.instance_mode.setCurrentText('Condensed')
        group=next(i for i in self.dock._maps[1].values() if i.data(0,panel._ROLE).kind=='instance_group')
        tree.setCurrentItem(group); QtTest.QTest.keyClick(tree,QtCore.Qt.Key_Delete)
        self.assertEqual(self.snapshot(),before)
        tree.clearSelection(); item.setSelected(True)
        other=self.dock._maps[1][self.row(self.links[1]).key]; other.setSelected(True)
        QtTest.QTest.keyClick(tree,QtCore.Qt.Key_Delete); self.assertEqual(self.snapshot(),before)
        self.assertIn('Select one',self.dock.message.text()); tree.clearSelection()
        tree.setCurrentItem(item); name=target.Name
        def accept():
            dialog=QtWidgets.QApplication.activeModalWidget()
            if isinstance(dialog,RemoveDialog):
                dialog.remove.click()
                if dialog.result()!=QtWidgets.QDialog.Accepted:
                    errors.append(dialog.status.text()); dialog.reject()
            else: errors.append('Missing removal dialog')
        QtCore.QTimer.singleShot(100,accept); QtTest.QTest.keyClick(tree,QtCore.Qt.Key_Delete)
        self.assertFalse(errors); self.assertIsNone(self.doc.getObject(name))
