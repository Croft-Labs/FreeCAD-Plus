# SPDX-License-Identifier: LGPL-2.1-or-later
"""Models import UI: catalogs only, source ownership, native Undo and persistence."""
import json
import time
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, editing, external, hierarchy, panel
from TestComponentPanel import TestComponentPanel, settle
from TestUnusedModels import TestUnusedModels


class TestComponentImport(unittest.TestCase):
    setUp = TestComponentPanel.setUp
    tearDown = TestComponentPanel.tearDown
    external_fixture = TestUnusedModels.external_fixture
    rows = TestComponentPanel.rows
    model = TestComponentPanel.model

    def file(self, name):
        doc = document.new_document(name)
        root = document.validate(doc)
        root.Definitions[0].Label = name + ' component'
        box = root.Definitions[0].newObject('Part::Box', 'CatalogBox')
        doc.recompute(); document.save_document(doc, self.output/(name+'.cadprt'))
        return doc

    def choose(self, path, *, cancel=False, before_accept=None, item=None):
        self.widget.tabs.setCurrentIndex(0)
        tree = self.widget.trees[0]; settle()
        point = tree.visualItemRect(item).center() if item else QtCore.QPoint(5,tree.viewport().height()-5)
        observed=[];deadline=time.monotonic()+10
        old=QtWidgets.QApplication.testAttribute(QtCore.Qt.AA_DontUseNativeDialogs)
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_DontUseNativeDialogs,True)
        timer=QtCore.QTimer()
        def drive():
            popup=QtWidgets.QApplication.activePopupWidget();modal=QtWidgets.QApplication.activeModalWidget()
            if time.monotonic()>deadline:
                observed.append('timeout')
                if isinstance(popup,QtWidgets.QMenu):popup.close()
                if isinstance(modal,QtWidgets.QDialog):modal.reject()
                return
            if isinstance(popup,QtWidgets.QMenu) and not observed:
                action=next((a for a in popup.actions() if a.text()=='Import Models from File'),None)
                if action is None:observed.append('missing');popup.close();return
                observed.append('menu')
                QtTest.QTest.mouseClick(popup, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                       popup.actionGeometry(action).center())
            elif isinstance(modal,QtWidgets.QFileDialog) and observed==['menu']:
                observed.append(modal.windowTitle())
                if before_accept:before_accept()
                if cancel:modal.reject()
                else:
                    # A visible QFileDialog may not have populated its directory model yet.
                    # Enter the absolute path exactly as a user would in its filename field.
                    field=modal.findChild(QtWidgets.QLineEdit,'fileNameEdit')
                    field.setText(QtCore.QDir.toNativeSeparators(str(path)))
                    modal.accept()
        timer.timeout.connect(drive);timer.start(25)
        try:self.widget._menu(tree,point)
        finally:
            timer.stop();timer.deleteLater()
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_DontUseNativeDialogs,old)
        settle()
        self.assertEqual(len(observed),2,observed)
        self.assertEqual(observed[0],'menu')
        self.assertTrue(observed[1].startswith('Import Models into '),observed)
        return observed[1]

    def test_closed_nested_catalog_import_undo_and_persistence(self):
        nested=self.file('Fasteners');source=self.file('Hardware')
        external.import_file(source,nested);document.save_document(source)
        source_ids={o.Name:o.ID for o in source.Objects}
        source_name=source.Name;nested_name=nested.Name
        App.closeDocument(source_name);App.closeDocument(nested_name)
        App.setActiveDocument(self.doc.Name);settle()
        document.save_document(self.doc,self.output/'Assembly.cadprt')
        context=editing.context_path(self.doc)
        ids={o.Name:o.ID for o in self.doc.Objects};placed=list(self.root.Group)
        mdi=Gui.getMainWindow().findChild(QtWidgets.QMdiArea)
        count=len(mdi.subWindowList());view=Gui.activeDocument().activeView();undo=self.doc.UndoCount
        self.choose(self.output/'Hardware.cadprt')
        self.assertEqual(len(self.root.Imports),1,self.widget.message.text())
        source=self.root.Imports[0].Document
        self.assertEqual({o.Name:o.ID for o in source.Objects},source_ids)
        self.assertEqual(len(self.root.Imports[0].Imports),1)
        self.assertEqual(list(self.root.Group),placed)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
        self.assertEqual(Gui.activeDocument().activeView(),view)
        self.assertEqual(editing.context_path(self.doc),context)
        self.assertEqual(len(mdi.subWindowList()),count)
        self.assertEqual(self.doc.UndoCount,undo+1)
        imports=[r.label for _,r in self.rows(0) if r.kind=='import']
        self.assertEqual(imports,['Hardware','Fasteners'])
        self.doc.undo();settle();self.assertFalse(self.root.Imports)
        self.doc.redo();settle();self.assertEqual(len(self.root.Imports),1)
        document.save_document(self.doc)
        (self.output/'expected.json').write_text(json.dumps({'ids':ids,'source_ids':source_ids,
            'placed':[o.Name for o in placed]}))

    def test_external_edit_imports_into_its_defining_file(self):
        source,definition=self.external_fixture()
        library=self.file('Library');App.setActiveDocument(self.doc.Name);settle()
        editing.edit_unused(self.doc,definition);settle()
        assembly_imports=list(self.root.Imports);placements=list(self.root.Group)
        source_root=document.validate(source)
        title=self.choose(library.FileName,item=self.model(definition))
        self.assertIn('Hardware',title)
        self.assertEqual(list(source_root.Imports),[document.validate(library)],self.widget.message.text())
        self.assertEqual(list(self.root.Imports),assembly_imports)
        self.assertEqual(list(self.root.Group),placements)
        self.assertEqual(editing.context_path(self.doc),(definition,()))
        source.undo();settle();self.assertFalse(source_root.Imports)
        source.redo();settle();self.assertEqual(len(source_root.Imports),1)
        external.save_definition(definition);document.save_document(self.doc)

    def test_cancel_duplicate_and_cycle_preserve_catalog(self):
        document.save_document(self.doc,self.output/'Assembly.cadprt')
        source=self.file('Library');App.setActiveDocument(self.doc.Name);settle()
        names=set(App.listDocuments());undo=self.doc.UndoCount
        self.choose(source.FileName,cancel=True)
        self.assertEqual(set(App.listDocuments()),names);self.assertFalse(self.root.Imports)
        self.assertEqual(self.doc.UndoCount,undo)
        self.choose(source.FileName);undo=self.doc.UndoCount
        self.choose(source.FileName)
        self.assertEqual(len(self.root.Imports),1);self.assertEqual(self.doc.UndoCount,undo)
        document.save_document(self.doc)
        editing.edit_unused(self.doc,document.validate(source).Definitions[0]);settle()
        with patch.object(self.widget,'_message',wraps=self.widget._message) as feedback:
            self.choose(self.doc.FileName)
        self.assertTrue(any('Circular' in c.args[0] for c in feedback.call_args_list))
        self.assertFalse(document.validate(source).Imports)
        self.assertEqual(set(App.listDocuments()),names)

    def test_context_change_and_invalid_archive_are_atomic(self):
        document.save_document(self.doc,self.output/'Assembly.cadprt')
        source=self.file('Library');App.setActiveDocument(self.doc.Name);settle()
        with patch.object(self.widget,'_message',wraps=self.widget._message) as feedback:
            self.choose(source.FileName,before_accept=lambda:editing.edit_file(self.doc))
        self.assertTrue(any('context changed' in c.args[0] for c in feedback.call_args_list))
        self.assertFalse(self.root.Imports)
        invalid=self.output/'Invalid.cadprt';invalid.write_text('not a native archive')
        names=set(App.listDocuments());undo=self.doc.UndoCount
        with patch.object(self.widget,'_message',wraps=self.widget._message) as feedback:
            self.choose(invalid)
        self.assertTrue(any('Cannot import component file' in c.args[0] for c in feedback.call_args_list))
        self.assertEqual(set(App.listDocuments()),names)
        self.assertFalse(self.root.Imports);self.assertEqual(self.doc.UndoCount,undo)


def verify_fresh_process(output):
    output=Path(output)
    folder=output/'test_closed_nested_catalog_import_undo_and_persistence'
    expected=json.loads((folder/'expected.json').read_text())
    doc=document.open_document(folder/'Assembly.cadprt')
    try:
        root=document.validate(doc)
        assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
        assert [o.Name for o in root.Group]==expected['placed']
        assert len(root.Imports)==1 and len(root.Imports[0].Imports)==1
        assert {o.Name:o.ID for o in root.Imports[0].Document.Objects}==expected['source_ids']
    finally:
        for name in list(App.listDocuments()):App.closeDocument(name)
    folder=output/'test_external_edit_imports_into_its_defining_file'
    doc=document.open_document(folder/'Assembly.cadprt')
    try:
        root=document.validate(doc)
        assert len(root.Imports)==1
        assert Path(root.Imports[0].Document.FileName).stem=='Hardware'
        assert len(root.Imports[0].Imports)==1
        assert Path(root.Imports[0].Imports[0].Document.FileName).stem=='Library'
    finally:
        for name in list(App.listDocuments()):App.closeDocument(name)
