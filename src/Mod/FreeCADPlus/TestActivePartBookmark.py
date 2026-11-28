# SPDX-License-Identifier: LGPL-2.1-or-later
import os,json,unittest
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui
from PySide6 import QtTest
from freecad_plus import document,editing,hierarchy,panel


class TestActivePartBookmark(unittest.TestCase):
    def setUp(self):
        self.before=set(App.listDocuments());self.doc=document.new_document('ActivePart')
        self.root=document.validate(self.doc);self.parent=self.root.Definitions[0];self.top=self.root.Group[0]
        self.child=hierarchy.create_definition(self.doc,'Child');self.link=hierarchy.add_instance(self.parent,self.child)
        self.path=Path(os.environ['PLUS_TEST_DIR'])/(self._testMethodName+'.cadprt')
        panel.show_panel()
    def tearDown(self):
        for name in set(App.listDocuments())-self.before:App.closeDocument(name)
        QtTest.QTest.qWait(40)
    def reopen(self):
        document.save_document(self.doc,self.path);App.closeDocument(self.doc.Name)
        self.doc=document.open_document(self.path);QtTest.QTest.qWait(100)
        return editing.context_path(self.doc)
    def test_nested_active_part_and_exact_occurrence_saved(self):
        second=hierarchy.add_instance(self.parent,self.child);editing.edit((self.top,second))
        name=second.Name;part=self.child.Name;context=self.reopen()
        self.assertEqual(context[0].Name,part);self.assertEqual(context[1][-1].Name,name)
        self.assertEqual(self.doc.UndoCount,0);self.assertFalse(Gui.getDocument(self.doc.Name).Modified)
    def test_unused_definition_and_isolated_assembly_child_saved(self):
        editing.edit_in_assembly(self.doc,self.parent,(self.link,));part=self.child.Name
        context=self.reopen();self.assertEqual(context[0].Name,part);self.assertEqual(context[1],())
        self.assertEqual(editing.unused_context(self.doc).Name,part)
    def test_native_save_records_active_part(self):
        document.save_document(self.doc,self.path);editing.edit((self.top,self.link));part=self.child.Name
        self.doc.save();App.closeDocument(self.doc.Name);self.doc=document.open_document(self.path)
        self.assertEqual(editing.context_path(self.doc)[0].Name,part)
    def test_saving_background_file_keeps_its_own_active_part(self):
        editing.edit((self.top,self.link));part=self.child.Name
        other=document.new_document('OtherWindow')
        document.save_document(self.doc,self.path)
        self.assertEqual(App.ActiveDocument,other)
        App.closeDocument(self.doc.Name);self.doc=document.open_document(self.path)
        self.assertEqual(editing.context_path(self.doc)[0].Name,part)
    def test_missing_bookmark_uses_safe_multi_part_fallback(self):
        meta=dict(self.doc.Meta);meta[editing.ACTIVE_PART_BOOKMARK]=json.dumps(dict(version=1,mode='placed',part=['missing','Deleted',123],path=[]));self.doc.Meta=meta
        editing.edit_file(self.doc);self.reopen_file_only()
    def reopen_file_only(self):
        document.save_document(self.doc,self.path);App.closeDocument(self.doc.Name);self.doc=document.open_document(self.path)
        with self.assertRaises(ValueError):editing.context_path(self.doc)
