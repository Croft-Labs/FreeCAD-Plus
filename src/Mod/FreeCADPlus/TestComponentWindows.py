# SPDX-License-Identifier: LGPL-2.1-or-later
"""Component file tabs: native views, menu dispatch and shared persistence."""
import json
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, editing, hierarchy, external, isolation, panel
import TestComponentPanel as panel_tests
import TestUnusedModels as unused_tests
from TestComponentPanel import settle


class TestComponentWindows(unittest.TestCase):
    setUp = panel_tests.TestComponentPanel.setUp
    tearDown = panel_tests.TestComponentPanel.tearDown
    rows = panel_tests.TestComponentPanel.rows
    model = panel_tests.TestComponentPanel.model
    occurrence = panel_tests.TestComponentPanel.occurrence
    click = panel_tests.TestComponentPanel.click
    external_fixture = unused_tests.TestUnusedModels.external_fixture
    geometry = unused_tests.TestUnusedModels.geometry

    def mdi(self):
        return Gui.getMainWindow().findChild(QtWidgets.QMdiArea)

    def open_menu(self, index, item, before_choose=None):
        self.widget.tabs.setCurrentIndex(index)
        tree = self.widget.trees[index]
        tree.scrollToItem(item); settle()
        observed = []
        def choose():
            menu = QtWidgets.QApplication.activePopupWidget()
            if not isinstance(menu, QtWidgets.QMenu):
                observed.append('No menu')
                return
            action = next((a for a in menu.actions() if a.text() == 'Open in new window'), None)
            if action is None:
                observed.append('No action'); menu.close(); return
            observed.append(action.text())
            if before_choose:
                before_choose()
            QtTest.QTest.mouseClick(menu, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                   menu.actionGeometry(action).center())
        QtCore.QTimer.singleShot(50, choose)
        self.widget._menu(tree, tree.visualItemRect(item).center())
        settle()
        self.assertEqual(observed, ['Open in new window'])
        return Gui.activeDocument().activeView()

    def test_models_menu_preserves_original_context_camera_and_native_identity(self):
        original = Gui.activeDocument().activeView()
        window = self.mdi().activeSubWindow()
        original.setAnimationEnabled(False)
        original.viewTop(); original.fitAll(); settle()
        camera = original.getCamera()
        context = editing.context_path(self.doc)
        ids = {o.Name:o.ID for o in self.doc.Objects}
        undo = self.doc.UndoCount
        names = set(App.listDocuments())
        count = len(self.mdi().subWindowList())
        new = self.open_menu(0, self.model(self.child))
        new_window = self.mdi().activeSubWindow()
        self.assertNotEqual(new, original)
        self.assertEqual(len(self.mdi().subWindowList()), count + 1)
        self.assertEqual(editing.context_path(self.doc), context)
        self.assertIn(self.child.Label, new_window.windowTitle())
        self.assertEqual([r.ref for _,r in self.rows(2)], [panel.identity(self.sketch), panel.identity(self.pad)])
        # Ordinary Edit stays in the newly opened tab, including child Edit.
        self.click(1, self.occurrence((self.first,)), double=True)
        self.click(1, self.occurrence((self.first, self.nested)), double=True)
        self.assertEqual(Gui.activeDocument().activeView(), new)
        new.setAnimationEnabled(False)
        new.viewAxonometric(); new.fitAll(); settle()
        self.mdi().setActiveSubWindow(window); settle()
        self.assertEqual(Gui.activeDocument().activeView(), original)
        self.assertEqual(editing.context_path(self.doc), context)
        self.assertEqual(original.getCamera(), camera)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, ids)
        self.assertEqual(self.doc.UndoCount, undo)
        self.assertEqual(set(App.listDocuments()), names)
        self.mdi().setActiveSubWindow(new_window); new_window.close(); settle()
        self.assertEqual(len(self.mdi().subWindowList()), count)
        self.assertFalse(any(bound[1] == new for bound, _ in self.widget._states))
        self.assertEqual(editing.context_path(self.doc), context)
        self.assertEqual(original.getCamera(), camera)

    def test_part_tree_menu_uses_exact_occurrence_and_relabels_without_polling(self):
        original = Gui.activeDocument().activeView()
        view = self.open_menu(1, self.occurrence((self.first, self.nested)))
        self.assertNotEqual(view, original)
        self.assertEqual(editing.context_path(self.doc), (self.child, (self.first, self.nested)))
        self.assertTrue(self.occurrence((self.first, self.nested)).data(0, panel._EDITED))
        with document.transaction(self.doc, 'Rename component'):
            self.child.Label = 'Renamed component'
        settle()
        self.assertIn('Renamed component', self.mdi().activeSubWindow().windowTitle())
        count = self.widget.refresh_count
        QtTest.QTest.qWait(350)
        self.assertEqual(self.widget.refresh_count, count)
        self.doc.undo(); settle()
        self.assertIn('Shared child', self.mdi().activeSubWindow().windowTitle())

    def test_unused_windows_have_independent_isolation_and_close_cleanup(self):
        self.widget.edit_row(self.model(self.unused).data(0, panel._ROLE)); settle()
        original = Gui.activeDocument().activeView()
        first = isolation.current(original)
        view = self.open_menu(0, self.model(self.unused))
        second = isolation.current(view)
        self.assertIsNot(first, second)
        self.assertFalse(first.closed)
        self.assertFalse(second.closed)
        self.assertEqual(editing.context_path(self.doc), (self.unused, ()))
        self.mdi().activeSubWindow().close(); settle()
        self.assertTrue(second.closed)
        self.assertFalse(first.closed)
        self.assertEqual(Gui.activeDocument().activeView(), original)
        self.assertEqual(editing.context_path(self.doc), (self.unused, ()))
        self.widget.close(); settle()
        self.assertTrue(first.closed)
        self.assertFalse(isolation._sessions)
        self.widget = panel.show_panel()

    def test_external_tab_edits_save_to_source_and_no_persistent_window_objects(self):
        source, definition = self.external_fixture()
        original = Gui.activeDocument().activeView()
        ids = {o.Name:o.ID for o in self.doc.Objects}
        undo = self.doc.UndoCount
        view = self.open_menu(0, self.model(definition))
        self.assertNotEqual(view, original)
        self.assertEqual(App.ActiveDocument, self.doc)
        self.assertIn('Unused screw (Hardware)', self.mdi().activeSubWindow().windowTitle())
        self.assertEqual(self.doc.UndoCount, undo)  # Opening a view is presentation only.
        sketch, pad = self.geometry()
        self.assertEqual(pad.Document, source)
        pad_name = pad.Name
        source.undo(); source.recompute(); settle()
        self.assertIsNone(source.getObject(pad_name))
        source.redo(); source.recompute(); settle()
        pad = source.getObject(pad_name)
        self.assertTrue(pad.Shape.isValid())
        # Native coordinated Undo may add forwarding entries in dependent files;
        # the geometry and transaction remain owned by the defining source.
        history = next(item for item,row in self.rows(2) if row.ref == panel.identity(sketch))
        self.click(2, history, double=True)
        self.assertEqual(Gui.getDocument(self.doc.Name).getInEdit().Object, sketch)
        Gui.getDocument(self.doc.Name).resetEdit(); settle()
        external.save_definition(definition)
        document.save_document(self.doc)
        expected = {'assembly':ids, 'source':{o.Name:o.ID for o in source.Objects},
                    'definition':definition.Name, 'pad':pad.Name, 'source_uid':str(source.Uid)}
        (self.output/'window-expected.json').write_text(json.dumps(expected))
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, ids)
        self.assertFalse(any('window' in p.lower() for o in self.doc.Objects for p in o.PropertiesList))
        # Source deletion ends isolation and never leaves a stale editable root.
        source_name = source.Name
        App.closeDocument(source_name); settle()
        self.assertIsNone(isolation.current(view))
        self.assertIsNone(view.getActiveObject('ExternalEditContext'))

    def test_guards_reject_stale_menu_and_open_during_native_editor(self):
        count = len(self.mdi().subWindowList())
        row = self.model(self.child).data(0, panel._ROLE)
        editing.edit_feature(self.doc, self.sketch); settle()
        with self.assertRaisesRegex(ValueError, 'Finish'):
            self.widget.open_row(row)
        self.assertEqual(len(self.mdi().subWindowList()), count)
        Gui.getDocument(self.doc.Name).resetEdit(); settle()
        other = document.new_document('OtherComponentWindow')
        App.setActiveDocument(self.doc.Name); settle()
        count = len(self.mdi().subWindowList())
        self.open_menu(0, self.model(self.child), lambda: App.setActiveDocument(other.Name))
        self.assertEqual(len(self.mdi().subWindowList()), count)
        self.assertEqual(App.ActiveDocument, other)
        App.setActiveDocument(self.doc.Name); settle()
        row = self.occurrence((self.second, self.nested)).data(0, panel._ROLE)
        with document.transaction(self.doc, 'Remove selected occurrence'):
            self.doc.removeObject(self.second.Name)
        settle()
        with self.assertRaises(ValueError):
            self.widget.open_row(row)
        self.assertEqual(len(self.mdi().subWindowList()), count)

    def test_failed_open_rolls_back_only_new_view_and_panel_reopen_tracks_titles(self):
        from unittest.mock import patch
        old = Gui.activeDocument().activeView()
        context = editing.context_path(self.doc)
        count = len(self.mdi().subWindowList())
        row = self.model(self.child).data(0, panel._ROLE)
        with patch.object(editing, 'edit', side_effect=ValueError('Controlled edit failure')):
            with self.assertRaisesRegex(ValueError, 'Controlled'):
                self.widget.open_row(row)
        settle()
        self.assertEqual(len(self.mdi().subWindowList()), count)
        self.assertEqual(Gui.activeDocument().activeView(), old)
        self.assertEqual(editing.context_path(self.doc), context)
        view = self.widget.open_row(row); settle()
        self.widget.close(); settle()
        self.widget = panel.show_panel(); settle()
        with document.transaction(self.doc, 'Rename with reopened panel'):
            self.child.Label = 'Still tracked'
        settle()
        self.assertEqual(Gui.activeDocument().activeView(), view)
        self.assertIn('Still tracked', self.mdi().activeSubWindow().windowTitle())


def verify_fresh_process(output):
    from pathlib import Path
    import hashlib
    folder = Path(output)/'test_external_tab_edits_save_to_source_and_no_persistent_window_objects'
    expected = json.loads((folder/'window-expected.json').read_text())
    filename = folder/'Assembly.cadprt'
    digest = hashlib.sha256(filename.read_bytes()).hexdigest()
    doc = document.open_document(filename)
    source = next(d for d in App.listDocuments().values() if str(d.Uid) == expected['source_uid'])
    widget = panel.show_panel(); settle()
    assert {o.Name:o.ID for o in doc.Objects} == expected['assembly']
    assert {o.Name:o.ID for o in source.Objects} == expected['source']
    assert not isolation._sessions
    assert source.getObject(expected['pad']).Length.Value == 7
    definition = source.getObject(expected['definition'])
    row = next(item.data(0,panel._ROLE) for item in widget._maps[0].values()
               if item.data(0,panel._ROLE).ref == panel.identity(definition))
    widget.open_row(row); settle()
    with document.transaction(source, 'Edit through reopened component tab'):
        source.getObject(expected['pad']).Length = 9
    source.recompute(); external.save_definition(definition)
    assert hashlib.sha256(filename.read_bytes()).hexdigest() == digest
    widget.close(); App.closeDocument(doc.Name); App.closeDocument(source.Name)
    reopened = document.open_document(filename)
    source = next(d for d in App.listDocuments().values() if str(d.Uid) == expected['source_uid'])
    assert source.getObject(expected['pad']).Length.Value == 9
    App.closeDocument(reopened.Name); App.closeDocument(source.Name)
