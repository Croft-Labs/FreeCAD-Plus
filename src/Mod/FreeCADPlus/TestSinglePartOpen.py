# SPDX-License-Identifier: LGPL-2.1-or-later
"""Reopening a one-part file establishes Edit without changing saved geometry."""
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtTest
from freecad_plus import document, editing, hierarchy, panel


class TestSinglePartOpen(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Set PLUS_TEST_DIR to an isolated validation directory')
        self.before = set(App.listDocuments())
        self.output = Path(os.environ['PLUS_TEST_DIR']) / self._testMethodName
        self.output.mkdir(exist_ok=True)
        Gui.Selection.clearSelection()
        self.doc = document.new_document('SinglePartOpen')
        self.root = document.validate(self.doc)
        self.part = self.root.Definitions[0]
        self.solid = self.part.newObject('Part::Feature', 'Solid')
        self.solid.Shape = Part.makeBox(10, 20, 5)
        self.doc.recompute()
        self.widget = panel.show_panel()

    def tearDown(self):
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        QtTest.QTest.qWait(100)

    def save_close(self):
        path = self.output / 'part.cadprt'
        document.save_document(self.doc, path)
        App.closeDocument(self.doc.Name)
        QtTest.QTest.qWait(100)
        return path

    def reopened(self, path):
        doc = document.open_document(path)
        QtTest.QTest.qWait(200)
        self.widget.refresh()
        return doc

    def test_reopen_activates_single_part_and_populates_history_without_tab_switch(self):
        name = self.part.Name
        solid_name = self.solid.Name
        route_name = self.root.Group[0].Name
        path = self.save_close()
        self.widget.tabs.setCurrentIndex(0)
        doc = self.reopened(path)
        self.assertEqual(editing.context_path(doc), (doc.getObject(name), (doc.getObject(route_name),)))
        self.assertEqual(self.widget.tabs.currentIndex(), 0)
        history = [item.data(0, panel._ROLE).ref for item in self.widget._maps[2].values()]
        self.assertIn(panel.identity(doc.getObject(solid_name)), history)
        self.assertEqual(self.widget._assembly_context(self.widget._current())[0], doc.getObject(name))
        self.assertEqual(doc.UndoCount, 0)
        self.assertFalse(Gui.getDocument(doc.Name).Modified)
        self.widget.tabs.setCurrentIndex(2)
        self.widget.grab().save(str(self.output / 'reopened-history.png'))

    def test_reopen_preserves_geometry_visibility_and_metadata(self):
        self.root.Group[0].Placement.Base = App.Vector(11, 12, 13)
        self.solid.Visibility = False
        path = self.output / 'part.cadprt'
        document.save_document(self.doc, path)
        def snapshot(doc):
            return [(obj.Name, obj.ID, obj.TypeId, str(getattr(obj, 'Placement', '')),
                     obj.Visibility) for obj in doc.Objects], dict(doc.Meta)
        before = snapshot(self.doc)
        App.closeDocument(self.doc.Name)
        doc = self.reopened(path)
        self.assertEqual(snapshot(doc), before)
        self.assertAlmostEqual(doc.getObject('Solid').Shape.Volume, 1000)
        self.assertIsNotNone(editing.context_path(doc)[0])

    def test_unused_single_definition_opens_without_creating_occurrence(self):
        with document.transaction(self.doc, 'Remove occurrence'):
            self.doc.removeObject(self.root.Group[0].Name)
        path = self.save_close()
        doc = self.reopened(path)
        root = document.validate(doc)
        self.assertEqual(editing.context_path(doc), (root.Definitions[0], ()))
        self.assertEqual(list(root.Group), [])
        self.assertEqual(doc.UndoCount, 0)

    def test_repeated_single_definition_does_not_choose_arbitrary_instance(self):
        hierarchy.add_instance(self.root, self.part, App.Placement(App.Vector(50, 0, 0), App.Rotation()))
        path = self.save_close()
        doc = self.reopened(path)
        root = document.validate(doc)
        self.assertEqual(editing.context_path(doc), (root.Definitions[0], ()))
        self.assertEqual(len(root.Group), 2)

    def test_multiple_definitions_remain_at_file_level(self):
        hierarchy.create_definition(self.doc, 'Other part')
        path = self.save_close()
        doc = self.reopened(path)
        self.assertEqual(self.widget._context(doc, Gui.activeDocument().activeView()), (None, ()))

    def test_hidden_open_keeps_host_context_and_does_not_create_view(self):
        path = self.save_close()
        host = document.new_document('Host')
        context = editing.context_path(host)
        doc = document.open_document(path, hidden=True)
        self.assertEqual(App.ActiveDocument, host)
        self.assertEqual(editing.context_path(host), context)
        self.assertEqual(len(Gui.getDocument(doc.Name).mdiViewsOfType('Gui::View3DInventor')), 0)

    def test_refresh_and_reopening_loaded_file_preserve_explicit_file_edit(self):
        path = self.save_close()
        doc = self.reopened(path)
        editing.edit_file(doc)
        self.widget.refresh()
        self.assertEqual(document.open_document(path), doc)
        self.widget.refresh()
        self.assertEqual(self.widget._context(doc, Gui.activeDocument().activeView()), (None, ()))

    def test_imported_file_new_window_activates_part_without_changing_old_view(self):
        from freecad_plus import external, file_actions_ui
        source = self.doc
        document.save_document(source, self.output / 'source.cadprt')
        editing.edit_file(source)
        previous_view = Gui.activeDocument().activeView()
        host = document.new_document('Host')
        document.validate(host).Definitions[0].Label = 'Host part'
        document.save_document(host, self.output / 'host.cadprt')
        external.import_file(host, source)
        self.widget.refresh()
        row = next(item.data(0, panel._ROLE) for item in self.widget._maps[0].values()
                   if item.data(0, panel._ROLE).kind == 'import')
        file_actions_ui.run_action(self.widget, 'open', row)
        self.assertEqual(editing.context_path(source)[0], self.part)
        self.assertNotEqual(Gui.activeDocument().activeView(), previous_view)
        self.assertEqual(self.widget._context(source, previous_view), (None, ()))

    def test_recovered_file_activates_sole_local_part_with_external_child(self):
        from freecad_plus import external, file_recovery
        source = document.new_document('Source')
        source_part = document.validate(source).Definitions[0]
        source_part.Label = 'External child'
        source_path = self.output / 'source.cadprt'
        document.save_document(source, source_path)
        App.setActiveDocument(self.doc.Name)
        document.save_document(self.doc, self.output / 'part.cadprt')
        external.import_file(self.doc, source)
        hierarchy.add_instance(self.part, source_part)
        path = self.save_close()
        App.closeDocument(source.Name)
        original = path.read_bytes()
        moved = self.output / 'moved.cadprt'
        source_path.rename(moved)
        doc = file_recovery.open_resolved(path, {source_path: moved})
        self.widget.refresh()
        self.assertEqual(editing.context_path(doc)[0], document.validate(doc).Definitions[0])
        self.assertEqual(path.read_bytes(), original)
