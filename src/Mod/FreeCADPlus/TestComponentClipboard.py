# SPDX-License-Identifier: LGPL-2.1-or-later
"""Part Tree Copy/Paste: shared identities, native transactions and persistence."""
import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, editing, hierarchy, external, panel
import TestComponentPanel as panel_tests
from TestComponentPanel import settle


class TestComponentClipboard(unittest.TestCase):
    setUp = panel_tests.TestComponentPanel.setUp
    tearDown = panel_tests.TestComponentPanel.tearDown
    rows = panel_tests.TestComponentPanel.rows
    model = panel_tests.TestComponentPanel.model
    occurrence = panel_tests.TestComponentPanel.occurrence
    click = panel_tests.TestComponentPanel.click

    def row(self, path=None):
        item = self.occurrence(path) if path else self.widget.trees[1].topLevelItem(0)
        return item.data(0, panel._ROLE)

    def menu(self, item, title, before_choose=None):
        self.widget.tabs.setCurrentIndex(1)
        tree = self.widget.trees[1]
        tree.scrollToItem(item); settle()
        observed = []
        def choose():
            menu = QtWidgets.QApplication.activePopupWidget()
            action = next((a for a in menu.actions() if a.text() == title), None)
            observed.append(bool(action and action.isEnabled()))
            if not observed[-1]: menu.close(); return
            if before_choose: before_choose()
            QtTest.QTest.mouseClick(menu, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                   menu.actionGeometry(action).center())
        QtCore.QTimer.singleShot(50, choose)
        self.widget._menu(tree, tree.visualItemRect(item).center()); settle()
        self.assertEqual(observed, [True])

    def test_context_copy_paste_shared_geometry_movement_and_persistence(self):
        context = editing.context_path(self.doc)
        ids = {o.Name:o.ID for o in self.doc.Objects}
        definitions = list(self.root.Definitions)
        undo = self.doc.UndoCount
        self.menu(self.occurrence((self.first,)), 'Copy')
        self.assertEqual(self.doc.UndoCount, undo)
        self.menu(self.widget.trees[1].topLevelItem(0), 'Paste')
        added = [o for o in self.doc.Objects if o.Name not in ids]
        self.assertEqual(len(added), 1)
        copied = added[0]
        self.assertEqual(copied.TypeId, 'App::Link')
        self.assertEqual(copied.LinkedObject, self.parent)
        self.assertEqual(list(self.root.Definitions), definitions)
        self.assertEqual(self.doc.UndoCount, undo + 1)
        self.assertEqual(editing.context_path(self.doc), context)
        self.assertTrue(self.occurrence((copied,)).isSelected())
        name = copied.Name
        self.doc.undo(); self.doc.recompute(); settle()
        self.assertIsNone(self.doc.getObject(name))
        self.doc.redo(); self.doc.recompute(); settle()
        copied = self.doc.getObject(name)
        self.assertEqual(copied.LinkedObject, self.parent)
        hierarchy.move_instance(copied, App.Placement(App.Vector(50,0,0),App.Rotation()))
        with document.transaction(self.doc,'Edit shared geometry'):
            self.pad.Length = 9
        body = self.pad.getParentGeoFeatureGroup()
        for top in (self.first, self.second, copied):
            sub = hierarchy.subname((top,self.nested))+body.Name+'.'+self.pad.Name+'.'
            self.assertAlmostEqual(self.root.getSubObject(sub,0).Volume,36*3.141592653589793)
        document.save_document(self.doc,self.output/'Clipboard.cadprt')
        expected = {'ids':{o.Name:o.ID for o in self.doc.Objects}, 'copy':copied.Name,
                    'definition':self.parent.Name,'nested':self.nested.Name,'pad':self.pad.Name,
                    'definitions':[o.Name for o in definitions], 'placement':list(copied.LinkPlacement.toMatrix().A)}
        (self.output/'expected.json').write_text(json.dumps(expected))

    def test_keyboard_batch_deduplicates_descendants_and_undo_is_atomic(self):
        tree = self.widget.trees[1]
        self.click(1,self.occurrence((self.first,)))
        self.click(1,self.occurrence((self.first,self.nested)),modifier=QtCore.Qt.ControlModifier)
        self.click(1,self.occurrence((self.second,)),modifier=QtCore.Qt.ControlModifier)
        before = {o.Name:o.ID for o in self.doc.Objects}
        undo = self.doc.UndoCount
        tree.setFocus(); QtTest.QTest.keyClick(tree,QtCore.Qt.Key_C,QtCore.Qt.ControlModifier); settle()
        self.assertEqual(len(self.widget._clipboard),2)
        self.click(1,tree.topLevelItem(0))
        tree.setFocus(); QtTest.QTest.keyClick(tree,QtCore.Qt.Key_V,QtCore.Qt.ControlModifier); settle()
        added = [o for o in self.doc.Objects if o.Name not in before]
        self.assertEqual(len(added),2,self.widget.message.text())
        self.assertEqual(self.doc.UndoCount,undo+1)
        self.assertTrue(all(o.LinkedObject==self.parent for o in added))
        self.assertEqual(self.parent.Group,[self.nested])
        self.doc.undo();self.doc.recompute();settle()
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},before)
        self.doc.redo();self.doc.recompute();settle()
        self.assertEqual(len(self.doc.Objects),len(before)+2)

    def test_nested_target_owns_copy_and_placements_are_snapshots(self):
        placement = App.Placement(App.Vector(8,3,2),App.Rotation(App.Vector(0,0,1),20))
        hierarchy.move_instance(self.nested,placement);settle()
        self.nested.Visibility = False
        self.widget.copy_rows([self.row((self.second,self.nested))])
        hierarchy.move_instance(self.nested,App.Placement(App.Vector(2,1,0),App.Rotation()))
        self.nested.Visibility = True;settle()
        copied, = self.widget.paste_row(self.row((self.first,)))
        self.assertIn(copied,self.parent.Group)
        self.assertTrue(copied.LinkPlacement.isSame(placement,1e-9))
        self.assertFalse(copied.Visibility)
        self.assertTrue(copied.LinkTransform)
        for top in (self.first,self.second):
            self.assertEqual(hierarchy.resolve(self.doc,(top,copied))[0],self.child)
        # Legacy links that don't inherit definition transforms retain that semantic.
        copied.LinkTransform=False;settle()
        self.widget.copy_rows([self.row((self.first,copied))])
        legacy,=self.widget.paste_row(self.row())
        self.assertFalse(legacy.LinkTransform)
        self.assertTrue(legacy.LinkPlacement.isSame(placement,1e-9))

    def test_whole_batch_cycle_preflight_and_failed_transaction_roll_back(self):
        self.widget.copy_rows([self.row((self.first,self.nested)),self.row((self.second,))])
        before={o.Name:o.ID for o in self.doc.Objects};undo=self.doc.UndoCount
        with self.assertRaisesRegex(ValueError,'Circular'):
            self.widget.paste_row(self.row((self.first,)))
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},before)
        self.assertEqual(self.doc.UndoCount,undo)
        self.widget.copy_rows([self.row((self.first,)),self.row((self.second,))])
        # Inject a post-creation validation failure; native abort must remove every link.
        with patch.object(document,'validate',side_effect=ValueError('Controlled transaction failure')):
            with self.assertRaisesRegex(ValueError,'Controlled'):
                hierarchy.add_instances(self.root,[(self.parent,None,True,True)]*2)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},before)
        self.assertEqual(self.doc.UndoCount,undo)

    def test_external_parent_ownership_save_and_import_boundaries(self):
        document.save_document(self.doc,self.output/'Assembly.cadprt')
        source = document.new_document('Hardware')
        source_root=document.validate(source)
        parent=source_root.Definitions[0]
        child=hierarchy.create_definition(source,'Screw')
        link=hierarchy.add_instance(parent,child)
        document.save_document(source,self.output/'Hardware.cadprt')
        external.import_file(self.doc,source)
        imported=hierarchy.add_instance(self.root,parent)
        document.save_document(self.doc)
        checksum=hashlib.sha256(Path(self.doc.FileName).read_bytes()).hexdigest()
        App.setActiveDocument(self.doc.Name);settle()
        before={o.Name:o.ID for o in self.doc.Objects};source_undo=source.UndoCount
        self.widget.copy_rows([self.row((imported,link))])
        copied,=self.widget.paste_row(self.row((imported,)))
        self.assertEqual(copied.Document,source)
        self.assertEqual(copied.LinkedObject,child)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},before)
        self.assertEqual(source.UndoCount,source_undo+1)
        name=copied.Name
        source.undo();source.recompute();settle();self.assertIsNone(source.getObject(name))
        source.redo();source.recompute();settle();copied=source.getObject(name)
        external.save_definition(parent)
        self.assertEqual(hashlib.sha256(Path(self.doc.FileName).read_bytes()).hexdigest(),checksum)
        expected={'source_uid':str(source.Uid),'copy':copied.Name,'child':child.Name,
                  'parent':parent.Name,'assembly_ids':before,'source_ids':{o.Name:o.ID for o in source.Objects}}
        (self.output/'external-expected.json').write_text(json.dumps(expected))
        self.widget.copy_rows([self.row((self.first,self.nested))])
        source_before={o.Name:o.ID for o in source.Objects};undo=source.UndoCount
        with self.assertRaisesRegex(ValueError,'Import'):
            self.widget.paste_row(self.row((imported,)))
        self.assertEqual({o.Name:o.ID for o in source.Objects},source_before)
        self.assertEqual(source.UndoCount,undo)
        self.widget.copy_rows([self.row((imported,link))])
        destination=self.row()
        App.closeDocument(source.Name);settle()
        with self.assertRaises((ValueError,RuntimeError,ReferenceError)):
            self.widget.paste_row(destination)

    def test_native_editor_pending_transaction_and_stale_menu_guards(self):
        self.widget.copy_rows([self.row((self.first,))])
        root_row=self.row();before={o.Name:o.ID for o in self.doc.Objects}
        editing.edit_feature(self.doc,self.sketch);settle()
        with self.assertRaisesRegex(ValueError,'Finish'):self.widget.paste_row(root_row)
        Gui.getDocument(self.doc.Name).resetEdit();settle()
        self.doc.openTransaction('Pending caller')
        self.first.Label = 'Pending caller change'
        try:
            with self.assertRaisesRegex(ValueError,'Finish'):self.widget.paste_row(root_row)
            self.assertTrue(self.doc.HasPendingTransaction)
        finally:self.doc.abortTransaction()
        other=document.new_document('OtherClipboardFile')
        App.setActiveDocument(self.doc.Name);settle()
        self.menu(self.widget.trees[1].topLevelItem(0),'Paste',lambda:App.setActiveDocument(other.Name))
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},before)
        self.assertEqual(App.ActiveDocument,other)
        # No implicit import or same-label substitution in another file.
        with self.assertRaisesRegex(ValueError,'Import'):self.widget.paste_row(self.row())
        self.widget.close();settle()
        mdi=Gui.getMainWindow().findChild(QtWidgets.QMdiArea)
        mdi.setActiveSubWindow(None)
        self.assertIsNone(mdi.activeSubWindow())
        self.widget=panel.show_panel();settle()
        self.assertEqual(self.widget._binding[0],other)
        with self.assertRaisesRegex(ValueError,'Copy'):self.widget.paste_row(self.row())


def verify_fresh_process(output):
    output=Path(output)
    folder=output/'test_context_copy_paste_shared_geometry_movement_and_persistence'
    expected=json.loads((folder/'expected.json').read_text())
    doc=document.open_document(folder/'Clipboard.cadprt')
    root=document.validate(doc)
    assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
    assert [o.Name for o in root.Definitions]==expected['definitions']
    copied=doc.getObject(expected['copy'])
    assert copied.LinkedObject==doc.getObject(expected['definition'])
    assert list(copied.LinkPlacement.toMatrix().A)==expected['placement']
    assert doc.getObject(expected['pad']).Length.Value==9
    widget=panel.show_panel();settle();assert not widget._clipboard
    widget.close();App.closeDocument(doc.Name)
    folder=output/'test_external_parent_ownership_save_and_import_boundaries'
    expected=json.loads((folder/'external-expected.json').read_text())
    filename=folder/'Assembly.cadprt';checksum=hashlib.sha256(filename.read_bytes()).hexdigest()
    doc=document.open_document(filename)
    source=next(d for d in App.listDocuments().values() if str(d.Uid)==expected['source_uid'])
    assert {o.Name:o.ID for o in doc.Objects}==expected['assembly_ids']
    assert {o.Name:o.ID for o in source.Objects}==expected['source_ids']
    copied=source.getObject(expected['copy'])
    assert copied.LinkedObject==source.getObject(expected['child'])
    assert copied in source.getObject(expected['parent']).Group
    hierarchy.move_instance(copied,App.Placement(App.Vector(11,0,0),App.Rotation()))
    external.save_definition(source.getObject(expected['parent']))
    assert hashlib.sha256(filename.read_bytes()).hexdigest()==checksum
    App.closeDocument(doc.Name);App.closeDocument(source.Name)
    doc=document.open_document(filename)
    source=next(d for d in App.listDocuments().values() if str(d.Uid)==expected['source_uid'])
    assert source.getObject(expected['copy']).LinkPlacement.Base.x==11
    App.closeDocument(doc.Name);App.closeDocument(source.Name)
