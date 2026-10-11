# SPDX-License-Identifier: LGPL-2.1-or-later
"""Saved Part Type and visibility state; viewport filtering is a later increment."""
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, display, editing, hierarchy, external, panel
import TestComponentPanel as fixtures
settle=fixtures.settle

class TestComponentDisplay(unittest.TestCase):
    setUp=fixtures.TestComponentPanel.setUp
    tearDown=fixtures.TestComponentPanel.tearDown
    rows=fixtures.TestComponentPanel.rows
    occurrence=fixtures.TestComponentPanel.occurrence

    def row(self,path):return self.occurrence(path).data(0,panel._ROLE)

    def choose(self,path,group,title):
        self.widget.tabs.setCurrentIndex(1);tree=self.widget.trees[1];item=self.occurrence(path)
        tree.scrollToItem(item);settle();observed=[]
        def click():
            menu=QtWidgets.QApplication.activePopupWidget()
            try:
                action=next(a for a in menu.actions() if a.text()==group)
                menu.setActiveAction(action)
                QtTest.QTest.keyClick(menu,QtCore.Qt.Key_Right)
                QtTest.QTest.qWait(100)
                sub=action.menu()
                if not sub.isVisible(): raise RuntimeError('Nested menu did not open')
                choice=next(a for a in sub.actions() if a.text()==title)
                observed.append(choice.isEnabled())
                sub.setActiveAction(choice)
                QtTest.QTest.keyClick(sub,QtCore.Qt.Key_Return)
            except Exception as error:
                observed.append(str(error));menu.close()
        deadline=QtCore.QTimer(self.widget);deadline.setSingleShot(True)
        deadline.timeout.connect(lambda: QtWidgets.QApplication.activePopupWidget().close()
                                 if QtWidgets.QApplication.activePopupWidget() else None)
        deadline.start(2000)
        QtCore.QTimer.singleShot(50,click)
        self.widget._menu(tree,tree.visualItemRect(item).center());deadline.stop();deadline.deleteLater();settle()
        self.assertEqual(observed,[True])

    def test_menu_shared_owner_reset_context_undo_and_persistence(self):
        editing.edit((self.second,));settle()
        before={o.Name:o.ID for o in self.doc.Objects};undo=self.doc.UndoCount
        visibility={o.Name:bool(o.Visibility) for o in (self.first,self.second,self.nested,self.pad)}
        self.assertEqual(display.state(self.parent),('Full Component',True))
        self.assertEqual(display.state(self.nested),('Bodies Only',True))
        self.choose((self.second,self.nested),'Part Type','Reference')
        self.assertEqual(display.state(self.nested),('Reference',True),self.widget.message.text());self.assertEqual(self.doc.UndoCount,undo+1)
        self.assertIn('Reference',self.occurrence((self.second,self.nested)).toolTip(0))
        self.choose((self.second,self.nested),'Visibility','Hidden')
        self.assertEqual(display.state(self.nested),('Reference',False))
        self.doc.undo();self.doc.recompute();settle();self.assertEqual(display.state(self.nested),('Reference',True))
        self.doc.redo();self.doc.recompute();settle();self.assertEqual(display.state(self.nested),('Reference',False))
        editing.edit_file(self.doc);settle()
        self.assertEqual(display.resolved(self.nested,direct=False),('Excluded',False))
        self.assertIn('saved: Reference',self.occurrence((self.second,self.nested)).toolTip(0))
        editing.edit((self.first,));settle();self.assertIn('Reference',self.occurrence((self.first,self.nested)).toolTip(0))
        self.widget.set_display(self.row((self.first,)),part_type='Bodies Only')
        self.assertEqual(display.state(self.parent),('Bodies Only',True))
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},before)
        self.assertEqual({o.Name:bool(o.Visibility) for o in (self.first,self.second,self.nested,self.pad)},visibility)
        document.save_document(self.doc,self.output/'Display.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':before,'parent':self.parent.Name,'child':self.nested.Name,'pad':self.pad.Name}))

    def test_excluded_show_guard_noop_and_stale_context(self):
        editing.edit((self.second,));settle();row=self.row((self.second,self.nested))
        self.widget.set_display(row,part_type='Excluded');undo=self.doc.UndoCount
        with self.assertRaisesRegex(ValueError,'Excluded'):self.widget.set_display(row,shown=True)
        self.assertEqual(self.doc.UndoCount,undo);self.assertEqual(display.state(self.nested),('Excluded',True))
        self.widget.set_display(row,part_type='Excluded');self.assertEqual(self.doc.UndoCount,undo)
        expected=(panel.identity(self.parent),panel.identity(self.nested))
        editing.edit((self.second,self.nested));settle()
        with self.assertRaisesRegex(ValueError,'context changed'):self.widget.set_display(row,shown=False,expected=expected)
        editing.edit_file(self.doc);settle()
        with self.assertRaisesRegex(ValueError,'immediate parent'):self.widget.set_display(row,part_type='Reference')
        self.assertEqual(self.doc.UndoCount,undo)

    def test_schema_four_lazy_defaults_and_undo_upgrade(self):
        self.root.PlusSchema=4;self.doc.recompute();undo=self.doc.UndoCount
        for unused in range(3):self.widget.refresh();display.state(self.parent);display.state(self.nested)
        self.assertEqual(self.root.PlusSchema,4);self.assertNotIn(display.CHILD[0],self.nested.PropertiesList)
        self.assertEqual(self.doc.UndoCount,undo)
        display.set_state(self.parent,self.nested,part_type='Reference')
        self.assertEqual(self.root.PlusSchema,5);self.doc.undo();self.doc.recompute();settle()
        self.assertEqual(self.root.PlusSchema,4);self.assertNotIn(display.CHILD[0],self.nested.PropertiesList)
        self.doc.redo();self.doc.recompute();settle();self.assertEqual(display.state(self.nested),('Reference',True))

    def test_copy_native_ids_and_saved_choices(self):
        display.set_state(self.parent,part_type='Bodies Only')
        display.set_state(self.parent,self.nested,part_type='Reference',shown=False)
        editing.edit((self.second,));settle()
        self.widget.copy_rows([self.row((self.second,self.nested))])
        copied=self.widget.paste_row(self.row((self.second,)))[0]
        self.assertEqual(display.state(copied),('Reference',False));self.assertEqual(copied.LinkedObject,self.child)
        independent=external.copy_definition(self.parent,self.doc,'Independent',placements_to_replace=(),child_labels={self.child:'Independent child'})
        self.assertEqual(display.state(independent),('Bodies Only',True))
        children=[o for o in independent.Group if o.TypeId=='App::Link']
        self.assertEqual([display.state(o) for o in children],[('Reference',False)]*2)
        self.assertTrue(all(o.LinkedObject!=self.child for o in children));document.validate(self.doc)

    def test_invalid_state_and_atomic_rollback(self):
        undo=self.doc.UndoCount
        with self.assertRaisesRegex(ValueError,'valid Part Type'):display.set_state(self.parent,self.nested,part_type='Hidden')
        with self.assertRaisesRegex(ValueError,'direct child'):display.set_state(self.parent,self.first,shown=False)
        real=document.validate
        def failure(doc):
            if display.CHILD[0] in self.nested.PropertiesList:raise ValueError('Controlled display failure')
            return real(doc)
        with patch.object(document,'validate',side_effect=failure):
            with self.assertRaisesRegex(ValueError,'Controlled'):display.set_state(self.parent,self.nested,part_type='Reference')
        self.assertNotIn(display.CHILD[0],self.nested.PropertiesList);self.assertEqual(self.doc.UndoCount,undo)
        display.set_state(self.parent,self.nested,part_type='Reference')
        self.nested.setPropertyStatus(display.CHILD[0],'ReadOnly')
        with self.assertRaisesRegex(ValueError,'read-only'):display.set_state(self.parent,self.nested,shown=False)
        self.nested.setPropertyStatus(display.CHILD[0],'-ReadOnly')

    def test_external_source_owned_undo_and_save(self):
        document.save_document(self.doc,self.output/'Assembly.cadprt')
        source=document.new_document('Hardware');root=document.validate(source);parent=root.Definitions[0]
        child=hierarchy.create_definition(source,'Pin');link=hierarchy.add_instance(parent,child)
        document.save_document(source,self.output/'Hardware.cadprt');external.import_file(self.doc,source)
        imported=hierarchy.add_instance(self.root,parent);document.save_document(self.doc)
        checksum=hashlib.sha256(Path(self.doc.FileName).read_bytes()).hexdigest()
        App.setActiveDocument(self.doc.Name);editing.edit((imported,));settle();undo=source.UndoCount
        self.widget.set_display(self.row((imported,link)),part_type='Reference',shown=False)
        self.assertEqual(source.UndoCount,undo+1);self.assertEqual(display.state(link),('Reference',False))
        external.save_definition(parent);self.assertEqual(hashlib.sha256(Path(self.doc.FileName).read_bytes()).hexdigest(),checksum)
        (self.output/'expected.json').write_text(json.dumps({'ids':{o.Name:o.ID for o in source.Objects},'uuid':source.Uid,'link':link.Name,'checksum':checksum}))

def verify_fresh_process(output, external_output=None):
    output=Path(output);before=set(App.listDocuments())
    try:
        folder=output/'test_menu_shared_owner_reset_context_undo_and_persistence'
        expected=json.loads((folder/'expected.json').read_text());doc=document.open_document(folder/'Display.cadprt')
        assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
        assert display.state(doc.getObject(expected['parent']))==('Bodies Only',True)
        assert display.state(doc.getObject(expected['child']))==('Reference',False)
        assert doc.getObject(expected['pad']).Length.Value==5
        folder=Path(external_output or output)/'test_external_source_owned_undo_and_save';expected=json.loads((folder/'expected.json').read_text())
        source=document.open_document(folder/'Hardware.cadprt')
        assert {o.Name:o.ID for o in source.Objects}==expected['ids']
        assert display.state(source.getObject(expected['link']))==('Reference',False)
        App.closeDocument(source.Name)
        assembly=document.open_document(folder/'Assembly.cadprt')
        source=next(d for d in App.listDocuments().values() if d.Uid==expected['uuid'])
        assert {o.Name:o.ID for o in source.Objects}==expected['ids']
        assert display.state(source.getObject(expected['link']))==('Reference',False)
        assert hashlib.sha256(Path(assembly.FileName).read_bytes()).hexdigest()==expected['checksum']
    finally:
        for name in set(App.listDocuments())-before:App.closeDocument(name)
