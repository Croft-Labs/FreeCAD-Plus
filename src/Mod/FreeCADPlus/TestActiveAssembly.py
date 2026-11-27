# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native active assembly navigation, chooser counts and preservation."""
import json
import unittest
from pathlib import Path
from unittest.mock import patch
import FreeCAD as App, FreeCADGui as Gui
from PySide6 import QtCore, QtGui, QtWidgets, QtTest
from freecad_plus import assembly, document, hierarchy, editing, external, isolation, display, panel
from TestComponentPanel import TestComponentPanel, settle

class TestActiveAssembly(unittest.TestCase):
    setUp = TestComponentPanel.setUp
    tearDown = TestComponentPanel.tearDown
    rows = TestComponentPanel.rows
    model = TestComponentPanel.model

    def assembly_item(self):
        return self.widget.trees[1].topLevelItem(0)

    def choose(self, definition=None, *, cancel=False, inspect=None):
        seen=[];timer=QtCore.QTimer()
        def drive():
            dialog=QtWidgets.QApplication.activeModalWidget()
            if not isinstance(dialog,QtWidgets.QDialog):return
            tree=dialog.findChild(QtWidgets.QTreeWidget)
            if tree is None:return
            timer.stop()
            try:
                rows=[tree.topLevelItem(i) for i in range(tree.topLevelItemCount())]
                if inspect:inspect(dialog,tree,rows)
                if cancel:dialog.reject();seen.append('cancel');return
                allrows=rows+[row.child(i) for row in rows for i in range(row.childCount())]
                item=next(row for row in allrows if row.data(0,panel._ROLE)==panel.identity(definition))
                if item.parent():item.parent().setExpanded(True)
                tree.setCurrentItem(item)
                button=next(b for b in dialog.findChildren(QtWidgets.QPushButton) if b.text()=='Make active assembly')
                button.click();seen.append('accepted')
            except BaseException as error:
                seen.append(error);dialog.reject()
        timer.timeout.connect(drive);timer.start(30)
        try:self.widget.assembly_button.click()
        finally:timer.stop()
        settle()
        self.assertEqual(seen,['cancel' if cancel else 'accepted'],self.widget.message.text())

    def snapshot(self):
        return {o.Name:(o.ID,tuple(x.Name for x in o.OutList),o.Visibility) for o in self.doc.Objects}

    def test_parts_context_menu_sets_root_without_changing_edit_or_model(self):
        self.widget.tabs.setCurrentIndex(0);item=self.model(self.parent)
        before=self.snapshot();context=editing.context_path(self.doc);undo=self.doc.UndoCount
        seen=[];timer=QtCore.QTimer()
        def act():
            menu=QtWidgets.QApplication.activePopupWidget()
            if not isinstance(menu,QtWidgets.QMenu):return
            action=next(a for a in menu.actions() if a.text()=='Make active assembly')
            seen.append(action.text());timer.stop()
            menu.grab().save(str(self.output/'parts-menu.png'))
            QtTest.QTest.mouseClick(menu,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,menu.actionGeometry(action).center())
        timer.timeout.connect(act);timer.start(30)
        tree=self.widget.trees[0];point=tree.visualItemRect(item).center()
        try:
            event=QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse,point,tree.viewport().mapToGlobal(point))
            QtWidgets.QApplication.sendEvent(tree.viewport(),event)
        finally:timer.stop()
        settle();self.assertEqual(seen,['Make active assembly'])
        self.assertEqual([self.widget.tabs.tabText(i) for i in range(3)],['Parts','Assembly','History'])
        self.assertEqual(self.assembly_item().text(0),self.parent.Label)
        self.assertEqual(self.assembly_item().childCount(),1)
        self.assertEqual(self.assembly_item().child(0).text(0),self.child.Label)
        self.assertEqual(self.widget.trees[1].topLevelItemCount(),1)
        self.assertEqual(editing.context_path(self.doc),context)
        self.assertEqual(self.snapshot(),before);self.assertEqual(self.doc.UndoCount,undo)
        self.widget.grab().save(str(self.output/'assembly.png'))
        self.widget.edit_row(self.assembly_item().child(0).data(0,panel._ROLE));settle()
        self.assertEqual(self.assembly_item().text(0),self.parent.Label)
        self.assertEqual(editing.context_path(self.doc)[0],self.child)
        self.assertEqual(self.widget.trees[2].topLevelItem(0).text(0),self.child.Label)

    def test_counts_include_nested_repeated_hidden_but_not_reference_or_excluded(self):
        leaf=hierarchy.create_definition(self.doc,'Leaf')
        hierarchy.add_instance(self.child,leaf)
        hierarchy.add_instance(self.parent,self.child)
        hidden=hierarchy.add_instance(self.parent,leaf);display.set_state(self.parent,hidden,shown=False)
        reference=hierarchy.add_instance(self.parent,self.child);display.set_state(self.parent,reference,part_type='Reference')
        excluded=hierarchy.add_instance(self.parent,self.child);display.set_state(self.parent,excluded,part_type='Excluded')
        self.assertEqual(assembly.counts([self.parent,self.child,leaf,self.unused]),
                         {self.parent:5,self.child:1,leaf:0,self.unused:0})

    def test_chooser_flat_current_parts_counts_collapsed_files_and_cancel(self):
        other=document.new_document('Other catalog');otherroot=document.validate(other)
        otherroot.Definitions[0].Label='External assembly'
        App.setActiveDocument(self.doc.Name);self.widget.refresh()
        self.widget.activate_assembly(self.parent)
        def inspect(dialog,tree,rows):
            self.assertEqual([r.text(0) for r in rows[:3]],[d.Label for d in self.root_definitions()])
            self.assertEqual([r.text(1) for r in rows[:3]],['1','0','0'])
            self.assertEqual(rows[3].childCount(),1);self.assertFalse(rows[3].isExpanded())
            self.assertFalse(rows[3].flags()&QtCore.Qt.ItemIsSelectable)
            dialog.grab().save(str(self.output/'selector-collapsed.png'))
            rows[3].setExpanded(True);QtWidgets.QApplication.processEvents()
            dialog.grab().save(str(self.output/'selector-expanded.png'))
        self.choose(cancel=True,inspect=inspect)
        self.assertEqual(self.assembly_item().text(0),self.parent.Label)
        self.choose(self.unused);self.assertEqual(self.assembly_item().text(0),self.unused.Label)
        self.assertEqual(self.assembly_item().childCount(),0)
        self.choose(otherroot.Definitions[0]);self.assertIn('External assembly',self.assembly_item().text(0))
        self.assertEqual(list(self.root_definitions()),list(document.validate(self.doc).Definitions))
        self.assertNotIn(otherroot,document.validate(self.doc).Imports)

    def root_definitions(self):return document.validate(self.doc).Definitions

    def test_unused_assembly_child_edit_never_uses_unrelated_placed_occurrence(self):
        hierarchy.add_instance(self.unused,self.child)
        before=self.snapshot();self.widget.activate_assembly(self.unused)
        row=self.assembly_item().child(0).data(0,panel._ROLE)
        self.assertTrue(row.anchor)
        self.widget.edit_row(row);settle()
        self.assertEqual(editing.context_path(self.doc),(self.child,()))
        self.assertTrue(isolation.current(Gui.activeDocument().activeView()).allow_placed)
        self.assertEqual(self.assembly_item().text(0),self.unused.Label)
        self.assertEqual(self.snapshot(),before)
        sketch=editing.new_sketch(self.doc);self.assertEqual(document.owned_path(self.child,sketch)[-1],sketch)
        self.assertEqual(editing.context_path(self.doc),(self.child,()))
        mdi=Gui.getMainWindow().findChild(QtWidgets.QMdiArea);original=mdi.activeSubWindow()
        self.widget.open_row(row);settle()
        self.assertEqual(editing.context_path(self.doc),(self.child,()))
        self.assertTrue(isolation.current(Gui.activeDocument().activeView()).allow_placed)
        Gui.Selection.clearSelection();mdi.activeSubWindow().close();settle()
        mdi.setActiveSubWindow(original);settle()

    def test_root_rename_delete_and_undo(self):
        self.widget.activate_assembly(self.unused)
        hierarchy.rename_definition(self.unused,'Renamed assembly');settle()
        self.assertEqual(self.assembly_item().text(0),'Renamed assembly')
        self.assertIn('Renamed assembly',self.widget.assembly_button.text())
        self.doc.undo();settle();self.assertEqual(self.assembly_item().text(0),'Unused component')
        # Closed foreign roots become an empty chooser, never a stale object route.
        other=document.new_document('Temporary catalog');part=document.validate(other).Definitions[0]
        App.setActiveDocument(self.doc.Name);self.widget.refresh();self.widget.activate_assembly(part)
        App.closeDocument(other.Name);settle();self.widget.refresh()
        self.assertEqual(len(self.widget._maps[1]),0)
        self.assertEqual(self.widget.assembly_button.text(),'Choose active assembly...')

    def test_copy_paste_into_selected_unused_assembly_and_stale_child_guard(self):
        self.widget.activate_assembly(self.parent)
        self.widget.copy_rows([self.assembly_item().child(0).data(0,panel._ROLE)])
        context=editing.context_path(self.doc)
        self.widget.activate_assembly(self.unused)
        self.widget.paste_row(self.assembly_item().data(0,panel._ROLE));settle()
        self.assertEqual(editing.context_path(self.doc),context)
        self.assertEqual(self.assembly_item().childCount(),1)
        row=self.assembly_item().child(0).data(0,panel._ROLE)
        self.assertTrue(row.anchor)
        self.assertEqual(self.widget._checked(row)[1],self.child)
        self.assertEqual(assembly.counts([self.unused])[self.unused],1)
        self.widget.copy_rows([row])
        self.assertEqual(len(self.widget._clipboard),1)
        self.doc.undo();settle()
        self.assertEqual(self.assembly_item().childCount(),0)
        with self.assertRaises(ValueError):self.widget._checked(row)

    def test_loaded_unimported_assembly_edits_in_source_without_importing(self):
        other=document.new_document('Loaded source');part=document.validate(other).Definitions[0]
        App.setActiveDocument(self.doc.Name);settle();self.widget.refresh()
        before=self.snapshot();self.widget.activate_assembly(part)
        self.widget.edit_row(self.assembly_item().data(0,panel._ROLE));settle()
        self.assertEqual(App.ActiveDocument,other)
        self.assertEqual(editing.context_path(other)[0],part)
        self.assertEqual(self.snapshot(),before)
        self.assertNotIn(document.validate(other),self.root.Imports)

    def test_pending_task_and_stale_chooser_are_refused(self):
        self.widget.activate_assembly(self.parent)
        self.doc.openTransaction('Pending')
        try:
            with self.assertRaisesRegex(ValueError,'Finish'):self.widget.activate_assembly(self.child)
        finally:self.doc.abortTransaction();App.closeActiveTransaction()
        settle();self.widget.refresh()
        with patch.object(self.widget,'_message',wraps=self.widget._message) as feedback:
            def change(dialog,tree,rows):
                other=document.new_document('Other');App.setActiveDocument(other.Name)
            self.choose(self.child,inspect=change)
        self.assertTrue(any('file tab changed' in c.args[0] for c in feedback.call_args_list))

    def test_per_view_choice_and_saved_reopen_preference(self):
        first=Gui.activeDocument().activeView();mdi=Gui.getMainWindow().findChild(QtWidgets.QMdiArea)
        first_window=mdi.activeSubWindow()
        self.widget.activate_assembly(self.parent)
        Gui.activeDocument().createView('Gui::View3DInventor');editing.edit((self.first,));settle()
        self.widget.activate_assembly(self.unused)
        self.assertEqual(self.assembly_item().text(0),self.unused.Label)
        mdi.setActiveSubWindow(first_window);settle();self.widget.refresh()
        self.assertEqual(self.assembly_item().text(0),self.parent.Label)
        self.widget.activate_assembly(self.parent)
        document.save_document(self.doc,self.output/'Assembly.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'uid':str(self.doc.Uid),'part':self.parent.Name,'id':self.parent.ID,
            'ids':{o.Name:o.ID for o in self.doc.Objects},'pad':self.pad.Name,'volume':self.pad.Shape.Volume}))
        self.assertEqual(assembly.recalled(self.doc),self.parent)
