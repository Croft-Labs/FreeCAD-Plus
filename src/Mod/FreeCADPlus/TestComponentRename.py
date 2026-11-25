# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component definition Rename through native Qt menus, owning-file Undo and persistence."""
import json
import time
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtGui, QtTest, QtWidgets
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

    def rename(self, index, item, label, *, cancel=False, before_accept=None, context_x=None):
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
        try:
            point = tree.visualItemRect(item).center()
            if context_x is None:
                self.widget._menu(tree, point)
            else:
                point.setX(context_x)
                event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse, point,
                                                tree.viewport().mapToGlobal(point))
                QtWidgets.QApplication.sendEvent(tree.viewport(), event)
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
        # Imported and domestic definitions now share the viewing file's scope.
        undo = source.UndoCount
        self.rename(0, self.model(definition), self.child.Label)
        self.assertEqual(definition.Label, original)
        self.assertEqual(source.UndoCount, undo)
        label = 'Imported shared child'
        self.rename(0, self.model(definition), label)
        self.assertEqual(definition.Label, label)
        self.assertNotEqual(self.child.Label, label)
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

    def test_history_heading_context_menu_rename_undo_and_save(self):
        tree = self.widget.trees[2]; self.widget.tabs.setCurrentIndex(2); settle()
        heading = tree.topLevelItem(0)
        self.assertEqual(heading.text(0), self.child.Label)
        self.assertEqual(heading.data(0, panel._ROLE).kind, 'history_component')
        self.assertTrue(heading.font(0).bold()); self.assertTrue(heading.icon(1).isNull())
        self.assertFalse(heading.flags() & QtCore.Qt.ItemIsDragEnabled)
        before = {o.Name:(o.ID, o.Visibility) for o in self.doc.Objects}
        context = editing.context_path(self.doc); original = self.child.Label; undo = self.doc.UndoCount
        self.widget.grab().save(str(self.output/'history-before.png'))
        def dialog_capture():
            QtWidgets.QApplication.activeModalWidget().grab().save(str(self.output/'rename-dialog.png'))
        # Dispatch native context events on the far-left icon and on its name.
        self.rename(2, heading, 'Mounting plate', context_x=8, before_accept=dialog_capture)
        self.assertEqual(self.child.Label, 'Mounting plate')
        self.assertIs(tree.topLevelItem(0), heading)
        self.assertEqual(heading.text(0), 'Mounting plate')
        self.assertEqual(self.doc.UndoCount, undo+1)
        self.assertEqual(editing.context_path(self.doc), context)
        for _, row in self.rows(0)+self.rows(1)+self.rows(2):
            if row.ref == panel.identity(self.child): self.assertEqual(row.label, 'Mounting plate')
        self.widget.grab().save(str(self.output/'history-renamed.png'))
        self.doc.undo(); settle(); self.assertEqual(heading.text(0), original)
        self.doc.redo(); settle(); self.assertEqual(heading.text(0), 'Mounting plate')
        self.rename(2, heading, 'Cancelled name', cancel=True, context_x=60)
        self.assertEqual(heading.text(0), 'Mounting plate')
        self.assertEqual({o.Name:(o.ID, o.Visibility) for o in self.doc.Objects}, before)
        document.save_document(self.doc, self.output/'HistoryRename.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'definition':self.child.Name,
            'label':self.child.Label, 'ids':{o.Name:o.ID for o in self.doc.Objects},
            'pad':self.pad.Name, 'volume':self.pad.Shape.Volume}))

    def test_history_heading_has_no_visibility_or_feature_selection(self):
        tree = self.widget.trees[2]; self.widget.tabs.setCurrentIndex(2); settle()
        heading = tree.topLevelItem(0); before = {o.Name:o.Visibility for o in self.doc.Objects}
        undo = self.doc.UndoCount
        point = QtCore.QPoint(8, tree.visualItemRect(heading).center().y())
        QtTest.QTest.mouseClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
        tree.setCurrentItem(heading); QtTest.QTest.keyClick(tree, QtCore.Qt.Key_Space); settle()
        self.widget._refresh_history_eyes(self.child)
        self.assertTrue(heading.icon(1).isNull())
        self.assertFalse(Gui.Selection.getSelection())
        self.assertEqual({o.Name:o.Visibility for o in self.doc.Objects}, before)
        self.assertEqual(self.doc.UndoCount, undo)
        self.assertFalse(self.widget.message.text())

    def test_history_rename_validation_and_stale_context(self):
        heading = self.widget.trees[2].topLevelItem(0)
        name = self.child.Label; undo = self.doc.UndoCount
        for label in (' ', self.parent.Label):
            self.rename(2, heading, label, context_x=8)
            self.assertEqual(self.child.Label, name); self.assertEqual(self.doc.UndoCount, undo)
            self.assertIn('unique within this file', self.widget.message.text())
        with patch.object(self.widget, '_message', wraps=self.widget._message) as feedback:
            self.rename(2, heading, 'Stale', before_accept=lambda:editing.edit((self.first,)))
        self.assertEqual(self.child.Label, name)
        self.assertTrue(any('active component changed' in call.args[0] for call in feedback.call_args_list))
        self.widget.refresh()
        self.assertEqual(self.widget.trees[2].topLevelItem(0).text(0), self.parent.Label)
        editing.edit_file(self.doc); settle()
        self.assertFalse(any(row.kind == 'history_component' for _, row in self.rows(2)))

    def test_history_unused_and_external_definition_rename(self):
        editing.edit_unused(self.doc, self.unused); settle()
        self.rename(2, self.widget.trees[2].topLevelItem(0), 'Spare plate', context_x=8)
        self.assertEqual(self.unused.Label, 'Spare plate')
        source, definition = self.external_fixture()
        App.setActiveDocument(self.doc.Name); editing.edit_unused(self.doc, definition); settle()
        original = definition.Label
        self.rename(2, self.widget.trees[2].topLevelItem(0), 'External plate', context_x=60)
        self.assertEqual(definition.Label, 'External plate')
        self.assertIn('External plate', self.widget.trees[2].topLevelItem(0).text(0))
        source.undo(); settle(); self.assertEqual(definition.Label, original)


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
