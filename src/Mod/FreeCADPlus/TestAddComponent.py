# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Add Component dropdown, transactional children and unchanged New Component."""
import json
import unittest
from pathlib import Path
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import component_add, document, editing, hierarchy, external, panel, toolbars, display
from TestComponentPanel import TestComponentPanel, settle


class TestAddComponent(unittest.TestCase):
    setUp = TestComponentPanel.setUp
    tearDown = TestComponentPanel.tearDown

    def snapshot(self, doc=None):
        doc = doc or self.doc
        return {o.Name: (o.ID, tuple((x.Document.Name, x.Name) for x in o.OutList), o.Visibility)
                for o in doc.Objects}

    def links(self, owner):
        return [o for o in owner.Group if o.TypeId == 'App::Link']

    def row(self, dialog, part):
        iterator = QtWidgets.QTreeWidgetItemIterator(dialog.choices)
        while iterator.value():
            item = iterator.value()
            if item.data(0, QtCore.Qt.UserRole) == panel.identity(part):
                return item
            iterator += 1
        self.fail('Missing component row')

    def library(self):
        document.save_document(self.doc, self.output/'Host.cadprt')
        source = document.new_document('Library')
        part = document.validate(source).Definitions[0]
        part.Label = 'Hardware'
        document.save_document(source, self.output/'Library.cadprt')
        App.setActiveDocument(self.doc.Name); settle(); self.widget.refresh()
        return source, part

    def test_existing_child_preserves_edit_assembly_identity_and_undo(self):
        self.widget.activate_assembly(self.parent)
        context = editing.context_path(self.doc); before = self.snapshot(); undo = self.doc.UndoCount
        _, token = component_add.target()
        instance = component_add.add(token, self.unused)
        self.assertIn(instance, self.child.Group)
        self.assertEqual(instance.LinkedObject, self.unused)
        self.assertTrue(instance.LinkPlacement.isIdentity())
        self.assertEqual(len(self.root.Definitions), 3)
        self.assertEqual(editing.context_path(self.doc), context)
        self.assertEqual(self.widget.trees[1].topLevelItem(0).data(0,panel._ROLE).ref, panel.identity(self.parent))
        self.assertEqual(self.doc.UndoCount, undo+1)
        self.assertEqual({name:self.snapshot()[name] for name in before if name!=self.child.Name},
                         {name:value for name,value in before.items() if name!=self.child.Name})
        name=instance.Name
        self.doc.undo();settle();self.assertEqual(self.snapshot(),before)
        self.doc.redo();settle();self.assertEqual(self.doc.getObject(name).LinkedObject,self.unused)

    def test_new_child_is_atomic_and_standalone_new_component_remains_unplaced(self):
        context=editing.context_path(self.doc);before=self.snapshot();undo=self.doc.UndoCount
        _,token=component_add.target()
        instance=component_add.add(token,label='Support bracket')
        name,definition=instance.Name,instance.LinkedObject
        definition_name=definition.Name
        self.assertEqual(definition.Label,'Support bracket')
        self.assertIn(definition,self.root.Definitions);self.assertIn(instance,self.child.Group)
        self.assertEqual(editing.context_path(self.doc),context)
        self.assertEqual(self.doc.UndoCount,undo+1)
        self.doc.undo();settle();self.assertEqual(self.snapshot(),before)
        self.assertIsNone(self.doc.getObject(definition_name))
        self.doc.redo();settle();self.assertEqual(self.doc.getObject(name).LinkedObject.Name,definition_name)
        document.save_document(self.doc,self.output/'DomesticChild.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'child':self.child.Name,'link':name,
            'definition':definition_name,'ids':{o.Name:o.ID for o in self.doc.Objects},
            'pad':self.pad.Name,'volume':self.pad.Shape.Volume}))
        links=[o.Name for o in self.doc.Objects if o.TypeId=='App::Link']
        Gui.runCommand('Std_Part');settle()
        standalone=editing.context_path(self.doc)[0]
        self.assertNotEqual(standalone.Name,definition_name)
        self.assertEqual([o.Name for o in self.doc.Objects if o.TypeId=='App::Link'],links)
        self.assertFalse(any(o.LinkedObject==standalone for o in self.doc.Objects if o.TypeId=='App::Link'))

    def test_self_ancestor_and_excluded_reference_cycles_are_rejected_without_changes(self):
        for kind in ('Reference','Excluded'):
            display.set_state(self.parent,self.nested,part_type=kind)
            before=self.snapshot();undo=self.doc.UndoCount
            for definition in (self.child,self.parent):
                with self.assertRaisesRegex(ValueError,'cycle'):
                    hierarchy.add_child(self.child,definition)
                self.assertEqual(self.snapshot(),before);self.assertEqual(self.doc.UndoCount,undo)

    def test_failed_creation_and_import_roll_back_every_object_and_metadata(self):
        before=self.snapshot();undo=self.doc.UndoCount
        with patch.object(hierarchy,'_place_instance',side_effect=RuntimeError('fixture failure')):
            with self.assertRaisesRegex(RuntimeError,'fixture failure'):
                hierarchy.add_child(self.child,label='Rolled back')
        self.assertEqual(self.snapshot(),before);self.assertEqual(self.doc.UndoCount,undo)
        source,part=self.library();before=self.snapshot();undo=self.doc.UndoCount
        with patch.object(hierarchy,'_place_instance',side_effect=RuntimeError('fixture failure')):
            with self.assertRaises(RuntimeError):hierarchy.add_child(self.child,part)
        self.assertEqual(self.snapshot(),before);self.assertEqual(self.doc.UndoCount,undo)
        self.assertNotIn(document.validate(source),self.root.Imports)

    def test_loaded_file_import_and_child_are_one_undo_and_save_reopen(self):
        source,part=self.library();source_before=self.snapshot(source);before=self.snapshot();undo=self.doc.UndoCount
        _,token=component_add.target();instance=component_add.add(token,part)
        self.assertIn(document.validate(source),self.root.Imports)
        self.assertIn(instance,self.child.Group);self.assertEqual(self.doc.UndoCount,undo+1)
        self.assertEqual(self.snapshot(source),source_before)
        name=instance.Name
        self.doc.undo();settle();self.assertEqual(self.snapshot(),before)
        self.doc.redo();settle();instance=self.doc.getObject(name)
        document.save_document(self.doc)
        (self.output/'expected.json').write_text(json.dumps({'child':self.child.Name,'link':name,
            'source_uid':str(source.Uid),'source_part':part.Name,'ids':{o.Name:o.ID for o in self.doc.Objects},
            'pad':self.pad.Name,'volume':self.pad.Shape.Volume}))

    def test_external_parent_owns_new_child_and_cannot_import_host(self):
        source,part=self.library();external.import_file(self.doc,source)
        host_before=self.snapshot();editing.edit_unused(self.doc,part);settle()
        context=editing.context_path(self.doc);_,token=component_add.target()
        instance=component_add.add(token,label='External child')
        self.assertEqual(instance.Document,source);self.assertEqual(instance.LinkedObject.Document,source)
        self.assertIn(instance,part.Group);self.assertEqual(self.snapshot(),host_before)
        self.assertEqual(editing.context_path(self.doc),context)
        with self.assertRaisesRegex(ValueError,'Circular file'):
            component_add.add(token,self.unused)
        self.assertEqual(self.snapshot(),host_before)

    def test_unused_parent_accepts_geometry_child_without_creating_root_placement(self):
        editing.edit_unused(self.doc,self.unused);settle()
        self.widget.activate_assembly(self.unused)
        roots=tuple(self.root.Group);context=editing.context_path(self.doc)
        _,token=component_add.target();instance=component_add.add(token,self.child);settle()
        self.assertEqual(tuple(self.root.Group),roots)
        self.assertEqual(editing.context_path(self.doc),context)
        self.assertEqual(self.widget.trees[1].topLevelItem(0).childCount(),1)
        self.assertIn(instance,self.unused.Group)
        self.assertAlmostEqual(instance.Shape.Volume,self.pad.Shape.Volume)

    def test_unsaved_loaded_file_is_disabled_and_never_silently_saved(self):
        source=document.new_document('Unsaved library');part=document.validate(source).Definitions[0]
        App.setActiveDocument(self.doc.Name);settle()
        dialog=component_add.Picker(Gui.getMainWindow())
        try:
            item=self.row(dialog,part)
            self.assertFalse(item.flags()&QtCore.Qt.ItemIsEnabled)
            self.assertIn('Save both defining files',item.toolTip(0))
            with self.assertRaisesRegex(ValueError,'Save both'):hierarchy.add_child(self.child,part)
            self.assertFalse(source.FileName);self.assertFalse(self.doc.FileName)
        finally:dialog.deleteLater()

    def test_picker_counts_blocked_rows_loaded_groups_and_cancel(self):
        source,part=self.library();before=self.snapshot();undo=self.doc.UndoCount
        dialog=component_add.Picker(Gui.getMainWindow());dialog.show();settle()
        try:
            tree=dialog.choices
            self.assertEqual([tree.topLevelItem(i).text(0) for i in range(3)],[p.Label for p in self.root.Definitions])
            self.assertEqual([tree.topLevelItem(i).text(1) for i in range(3)],['1','0','0'])
            self.assertFalse(self.row(dialog,self.parent).flags()&QtCore.Qt.ItemIsEnabled)
            self.assertFalse(self.row(dialog,self.child).flags()&QtCore.Qt.ItemIsEnabled)
            group=self.row(dialog,part).parent();self.assertIsNotNone(group);self.assertFalse(group.isExpanded())
            self.row(dialog,self.unused).setCheckState(0,QtCore.Qt.Checked);self.assertTrue(dialog.submit.isEnabled())
            self.assertIsNone(dialog.findChild(QtWidgets.QTabWidget))
            dialog.grab().save(str(self.output/'existing.png'))
            dialog.reject();self.assertEqual(self.snapshot(),before);self.assertEqual(self.doc.UndoCount,undo)
        finally:dialog.deleteLater()

    def test_external_file_changed_on_disk_reports_error_without_partial_import(self):
        source,part=self.library();path=Path(source.FileName);original=path.read_bytes()
        dialog=component_add.Picker(Gui.getMainWindow())
        try:
            self.row(dialog,part).setCheckState(0,QtCore.Qt.Checked);before=self.snapshot();undo=self.doc.UndoCount
            path.write_bytes(b'Invalid fixture archive')
            dialog.accept()
            self.assertTrue(dialog.status.error)
            self.assertIn('Cannot import component file',dialog.status.text())
            self.assertEqual(self.snapshot(),before);self.assertEqual(self.doc.UndoCount,undo)
        finally:
            path.write_bytes(original);dialog.deleteLater()

    def test_dialog_rechecks_context_deleted_part_and_new_cycle(self):
        dialog=component_add.Picker(Gui.getMainWindow())
        try:
            self.row(dialog,self.unused).setCheckState(0,QtCore.Qt.Checked)
            hierarchy.add_instance(self.unused,self.child)
            before=self.snapshot();dialog.accept()
            self.assertIn('cycle',dialog.status.text());self.assertEqual(self.snapshot(),before)
            editing.edit((self.first,));dialog.accept()
            self.assertIn('changed',dialog.status.text());self.assertEqual(self.snapshot(),before)
        finally:dialog.deleteLater()
        dialog=component_add.Picker(Gui.getMainWindow())
        try:
            self.row(dialog,self.unused).setCheckState(0,QtCore.Qt.Checked)
            with document.transaction(self.doc,'Delete unused fixture'):
                self.root.Definitions=[p for p in self.root.Definitions if p!=self.unused]
                for child in list(self.unused.Group):self.doc.removeObject(child.Name)
                self.doc.removeObject(self.unused.Name)
            before=self.snapshot();dialog.accept()
            self.assertTrue(dialog.status.error);self.assertEqual(self.snapshot(),before)
        finally:dialog.deleteLater()

    def test_invalid_duplicate_name_and_pending_operation_preserve_model(self):
        dialog=component_add.Picker(Gui.getMainWindow(),True)
        try:
            before=self.snapshot();undo=self.doc.UndoCount
            for value in (' ',self.parent.Label):
                dialog.name.setText(value);dialog.accept()
                self.assertTrue(dialog.status.error);self.assertEqual(self.snapshot(),before)
                self.assertEqual(self.doc.UndoCount,undo)
            dialog.name.setText('Valid name');dialog.show();settle()
            dialog.grab().save(str(self.output/'new.png'))
            dialog.reject();self.assertEqual(self.snapshot(),before)
        finally:dialog.deleteLater()
        _,token=component_add.target();self.doc.openTransaction('Pending')
        try:
            with self.assertRaisesRegex(ValueError,'Finish'):component_add.add(token,label='Blocked')
        finally:self.doc.abortTransaction();App.closeActiveTransaction()

    def test_ribbon_always_dropdown_both_real_add_paths_and_cancel(self):
        Gui.activateWorkbench('AssemblyWorkbench');settle();toolbars._controller.refresh();settle()
        ribbon=toolbars._controller
        self.assertIsNone(ribbon.host.findChild(QtWidgets.QToolButton,'Plus_Assembly_CreateAssembly'))
        button=ribbon.host.findChild(QtWidgets.QToolButton,'Plus_AddComponent')
        self.assertIsNotNone(button)
        self.assertEqual(button.popupMode(),QtWidgets.QToolButton.InstantPopup)
        self.assertIsNone(button.defaultAction())
        context=editing.context_path(self.doc);observed=[]
        def drive_dialog(mode,cancel):
            dialog=QtWidgets.QApplication.activeModalWidget()
            try:
                self.assertIsInstance(dialog,component_add.Picker)
                if cancel:dialog.reject()
                elif mode=='Add existing':
                    self.row(dialog,self.unused).setCheckState(0,QtCore.Qt.Checked);dialog.submit.click()
                else:dialog.name.setText('Menu child');dialog.submit.click()
                self.assertEqual(dialog.result(),QtWidgets.QDialog.Rejected if cancel else QtWidgets.QDialog.Accepted,
                                 dialog.status.text())
                observed.append(mode)
            except BaseException as error:
                observed.append(str(error))
                if dialog:dialog.reject()
        def choose(mode,cancel):
            menu=QtWidgets.QApplication.activePopupWidget()
            if not isinstance(menu,QtWidgets.QMenu):observed.append('Missing menu');return
            self.assertEqual([a.text() for a in menu.actions()],['Add existing','Add new'])
            menu.grab().save(str(self.output/'dropdown.png'))
            action=next(a for a in menu.actions() if a.text()==mode)
            QtCore.QTimer.singleShot(100,lambda:drive_dialog(mode,cancel))
            QtTest.QTest.mouseClick(menu,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,menu.actionGeometry(action).center())
        for mode,cancel in (('Add existing',False),('Add new',False),('Add existing',True)):
            before=self.snapshot()
            QtCore.QTimer.singleShot(100,lambda m=mode,c=cancel:choose(m,c))
            QtTest.QTest.mouseClick(button,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,button.rect().center())
            QtTest.QTest.qWait(160)
            if cancel:self.assertEqual(self.snapshot(),before)
        self.assertEqual(observed,['Add existing','Add new','Add existing'])
        self.assertEqual(editing.context_path(self.doc),context)
        self.assertEqual([o.LinkedObject.Label for o in self.links(self.child)],['Unused component','Menu child'])
        self.assertTrue(Gui.Command.get('Assembly_CreateAssembly'))  # Classic command remains native.
        Gui.activateWorkbench('PartDesignWorkbench');settle()
