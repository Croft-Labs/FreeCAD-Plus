# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component definition Rename through native Qt menus, owning-file Undo and persistence."""
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


class TestComponentRename(unittest.TestCase):
    setUp = TestComponentPanel.setUp
    tearDown = TestComponentPanel.tearDown
    rows = TestComponentPanel.rows
    model = TestComponentPanel.model
    occurrence = TestComponentPanel.occurrence
    external_fixture = TestUnusedModels.external_fixture

    def rename(self, index, item, label, *, cancel=False, before_accept=None):
        self.widget.tabs.setCurrentIndex(index)
        tree = self.widget.trees[index]; tree.scrollToItem(item); settle()
        observed = []; deadline = time.monotonic() + 8
        timer = QtCore.QTimer()
        def drive():
            popup = QtWidgets.QApplication.activePopupWidget()
            modal = QtWidgets.QApplication.activeModalWidget()
            if time.monotonic() > deadline:
                observed.append('timeout')
                if isinstance(popup, QtWidgets.QMenu): popup.close()
                if isinstance(modal, QtWidgets.QDialog): modal.reject()
                return
            if isinstance(popup, QtWidgets.QMenu) and not observed:
                action = next((a for a in popup.actions() if a.text() == 'Rename'), None)
                if action is None:
                    observed.append('missing Rename'); popup.close(); return
                observed.append('menu')
                QtTest.QTest.mouseClick(popup, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                       popup.actionGeometry(action).center())
            elif isinstance(modal, QtWidgets.QInputDialog) and observed == ['menu']:
                observed.append('dialog')
                modal.setTextValue(label)
                if before_accept: before_accept()
                if cancel: modal.reject()
                else: modal.accept()
        timer.timeout.connect(drive); timer.start(25)
        try: self.widget._menu(tree, tree.visualItemRect(item).center())
        finally: timer.stop(); timer.deleteLater()
        settle()
        self.assertEqual(observed, ['menu', 'dialog'])

    def test_part001_rename_updates_shared_rows_and_undo(self):
        original = self.parent.Label
        ids = {o.Name:o.ID for o in self.doc.Objects}
        context = editing.context_path(self.doc); volume = self.pad.Shape.Volume
        row = self.occurrence((self.first,))
        undo = self.doc.UndoCount
        self.rename(1, row, 'Tower assembly')
        self.assertEqual(self.parent.Label, 'Tower assembly')
        self.assertEqual(self.doc.UndoCount, undo + 1)
        self.assertIs(self.occurrence((self.first,)), row)
        self.assertEqual(editing.context_path(self.doc), context)
        self.assertEqual(self.first.LinkedObject, self.parent)
        self.assertEqual(self.second.LinkedObject, self.parent)
        for _, entry in self.rows(0) + self.rows(1):
            if entry.ref == panel.identity(self.parent): self.assertEqual(entry.label, 'Tower assembly')
        self.doc.undo(); settle(); self.assertEqual(self.parent.Label, original)
        self.doc.redo(); settle(); self.assertEqual(self.parent.Label, 'Tower assembly')
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, ids)
        self.assertAlmostEqual(self.pad.Shape.Volume, volume)
        document.save_document(self.doc, self.output/'Rename.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':ids,'definition':self.parent.Name,
            'label':self.parent.Label,'links':[self.first.Name,self.second.Name],'pad':self.pad.Name,'volume':volume}))

    def test_external_model_rename_belongs_to_source_file(self):
        source, definition = self.external_fixture()
        instance = hierarchy.add_instance(self.root, definition); settle()
        ids = [{o.Name:o.ID for o in d.Objects} for d in (self.doc,source)]
        original = definition.Label
        # Equal labels in different defining files are explicitly allowed.
        label = self.child.Label
        self.rename(0, self.model(definition), label)
        self.assertEqual(definition.Label, label)
        self.assertEqual(self.child.Label, label)
        self.assertEqual(instance.LinkedObject, definition)
        source.undo(); settle(); self.assertEqual(definition.Label, original)
        source.redo(); settle(); self.assertEqual(definition.Label, label)
        self.assertEqual([{o.Name:o.ID for o in d.Objects} for d in (self.doc,source)], ids)
        self.assertEqual(self.model(definition).text(0), label+' (Hardware)')
        external.save_definition(definition); document.save_document(self.doc)
        (self.output/'expected.json').write_text(json.dumps({'ids':ids,'definition':definition.Name,
            'label':label,'instance':instance.Name}))

    def test_cancel_same_name_and_invalid_names_make_no_undo(self):
        label = self.parent.Label; undo = self.doc.UndoCount
        self.rename(0, self.model(self.parent), 'Cancelled', cancel=True)
        self.rename(0, self.model(self.parent), label)
        self.assertEqual(self.parent.Label, label); self.assertEqual(self.doc.UndoCount, undo)
        for invalid in ('   ', self.child.Label):
            self.rename(0, self.model(self.parent), invalid)
            self.assertIn('unique within this file', self.widget.message.text())
            self.assertEqual(self.parent.Label, label); self.assertEqual(self.doc.UndoCount, undo)
        with self.assertRaisesRegex(ValueError, 'definition'):
            hierarchy.rename_definition(self.root, 'File renamed')
        self.parent.setPropertyStatus('Label', 'ReadOnly')
        try:
            with self.assertRaisesRegex(ValueError, 'read-only'):
                hierarchy.rename_definition(self.parent, 'Blocked')
        finally: self.parent.setPropertyStatus('Label', '-ReadOnly')
        self.assertEqual(self.parent.Label, label)

    def test_dialog_rechecks_changed_name_and_native_editor_guard(self):
        with patch.object(self.widget, '_message', wraps=self.widget._message) as feedback:
            self.rename(0, self.model(self.parent), 'Stale name',
                        before_accept=lambda: hierarchy.rename_definition(self.parent, 'Concurrent name'))
        self.assertEqual(self.parent.Label, 'Concurrent name')
        # The observer refresh clears status after the action reports its rejection.
        self.assertTrue(any('name changed' in call.args[0] for call in feedback.call_args_list))
        row = self.model(self.parent).data(0, panel._ROLE)
        editing.edit_feature(self.doc,self.sketch); settle()
        try:
            with self.assertRaisesRegex(ValueError, 'Finish'):
                self.widget.rename_row(row)
        finally: Gui.getDocument(self.doc.Name).resetEdit(); settle()


def verify_fresh_process(output):
    output = Path(output)
    folder = output/'test_part001_rename_updates_shared_rows_and_undo'
    expected = json.loads((folder/'expected.json').read_text())
    doc = document.open_document(folder/'Rename.cadprt')
    try:
        assert {o.Name:o.ID for o in doc.Objects} == expected['ids']
        definition = doc.getObject(expected['definition'])
        assert definition.Label == expected['label']
        assert all(doc.getObject(name).LinkedObject == definition for name in expected['links'])
        assert abs(doc.getObject(expected['pad']).Shape.Volume - expected['volume']) < 1e-8
    finally: App.closeDocument(doc.Name)
    folder = output/'test_external_model_rename_belongs_to_source_file'
    expected = json.loads((folder/'expected.json').read_text())
    doc = document.open_document(folder/'Assembly.cadprt')
    try:
        definition = doc.getObject(expected['instance']).LinkedObject
        assert definition.Name == expected['definition'] and definition.Label == expected['label']
        assert [{o.Name:o.ID for o in d.Objects} for d in (doc,definition.Document)] == expected['ids']
    finally:
        for name in list(App.listDocuments()): App.closeDocument(name)
