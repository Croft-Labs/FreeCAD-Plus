# SPDX-License-Identifier: LGPL-2.1-or-later
"""Actual Qt interaction and native ownership checks for the component panel."""
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, hierarchy, editing, external, panel


def settle():
    QtTest.QTest.qWait(60)


class TestComponentPanel(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Set PLUS_TEST_DIR to an isolated validation directory')
        self.output = Path(os.environ['PLUS_TEST_DIR']) / self._testMethodName
        self.output.mkdir(exist_ok=True)
        self.before = set(App.listDocuments())
        self.doc = document.new_document('PanelFixture')
        self.root = document.validate(self.doc)
        self.parent = self.root.Definitions[0]
        self.child = hierarchy.create_definition(self.doc, 'Shared child')
        self.nested = hierarchy.add_instance(self.parent, self.child)
        self.first = self.root.Group[0]
        self.second = hierarchy.add_instance(self.root, self.parent,
                                            App.Placement(App.Vector(25, 0, 0), App.Rotation()))
        editing.edit((self.second, self.nested))
        self.sketch = editing.new_sketch(self.doc)
        self.sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2), False)
        self.doc.recompute()
        self.pad = editing.pad(self.doc, self.sketch, 5)
        self.unused = hierarchy.create_definition(self.doc, 'Unused component')
        self.widget = panel.show_panel()
        self.widget.resize(380, 650)
        settle()

    def tearDown(self):
        self.widget.close()
        settle()
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        settle()

    def rows(self, index):
        return [(item, item.data(0, panel._ROLE)) for item in self.widget._maps[index].values()]

    def occurrence(self, path):
        key = tuple(panel.identity(o) for o in path)
        return next(item for item, row in self.rows(1) if row.path == key)

    def model(self, definition):
        return next(item for item, row in self.rows(0) if row.ref == panel.identity(definition) and row.kind == 'model')

    def click(self, tree_index, item, double=False, modifier=QtCore.Qt.NoModifier):
        self.widget.tabs.setCurrentIndex(tree_index)
        tree = self.widget.trees[tree_index]
        tree.scrollToItem(item)
        settle()
        point = tree.visualItemRect(item).center()
        QtTest.QTest.mouseClick(tree.viewport(), QtCore.Qt.LeftButton, modifier, point)
        if double:
            QtTest.QTest.mouseDClick(tree.viewport(), QtCore.Qt.LeftButton, modifier, point)
        settle()

    def test_projection_ownership_and_history_without_body_rows(self):
        before = [(o.Name, o.ID) for o in self.doc.Objects]
        undo = self.doc.UndoCount
        self.assertEqual([self.widget.tabs.tabText(i) for i in range(3)], ['Models', 'Part Tree', 'History'])
        self.assertEqual(self.widget.trees[1].topLevelItemCount(), 1)
        self.assertFalse(self.widget.trees[1].topLevelItem(0).icon(0).isNull())
        self.assertEqual(len([r for _, r in self.rows(0) if r.kind == 'model']), 3)
        self.assertEqual(len([r for _, r in self.rows(1) if r.kind == 'occurrence']), 4)
        history = [panel.lookup(r.ref) for _, r in self.rows(2)]
        self.assertEqual(history, [self.sketch, self.pad])
        self.assertNotIn('PartDesign::Body', [o.TypeId for o in history])
        # A repeated refresh must not recreate rows, geometry or transactions.
        row = self.occurrence((self.second, self.nested))
        self.widget.refresh()
        self.assertIs(self.occurrence((self.second, self.nested)), row)
        self.assertEqual([(o.Name, o.ID) for o in self.doc.Objects], before)
        self.assertEqual(self.doc.UndoCount, undo)

    def test_mouse_selection_double_click_edit_and_model_occurrence_memory(self):
        initial = editing.context_path(self.doc)
        first_child = self.occurrence((self.first, self.nested))
        self.click(1, first_child)
        self.assertEqual(editing.context_path(self.doc), initial)
        selected = Gui.Selection.getSelectionEx(self.doc.Name, 0)
        self.assertTrue(selected, f'{self.widget.message.text()} selectedRows={len(self.widget.trees[1].selectedItems())} rect={self.widget.trees[1].visualItemRect(first_child)} visible={self.widget.trees[1].isVisible()} selection={Gui.Selection.getSelectionEx()}')
        self.assertEqual(tuple(selected[0].SubElementNames), (hierarchy.subname((self.first, self.nested)),))
        # An observer update between clicks retains the same row and intended target.
        self.parent.Label = 'Renamed parent'
        settle()
        self.assertIs(first_child, self.occurrence((self.first, self.nested)))
        self.click(1, first_child, double=True)
        self.assertEqual(editing.context_path(self.doc), (self.child, (self.first, self.nested)))
        for item, row in self.rows(1):
            if row.kind == 'occurrence' and row.ref == panel.identity(self.child):
                self.assertTrue(item.font(0).bold())
                self.assertTrue(item.data(0, panel._ACTIVE))
        self.assertTrue(self.model(self.child).font(0).bold())
        self.assertTrue(first_child.data(0, panel._EDITED))
        self.click(1, self.occurrence((self.second, self.nested)), double=True)
        self.click(1, self.occurrence((self.first,)), double=True)
        self.click(0, self.model(self.child), double=True)
        self.assertEqual(editing.context_path(self.doc)[1], (self.second, self.nested))
        file_item = self.widget.trees[1].topLevelItem(0)
        self.click(1, file_item)
        self.assertEqual(editing.context_path(self.doc)[0], self.child)
        self.click(1, file_item, double=True)
        with self.assertRaises(ValueError): editing.context_path(self.doc)
        self.assertEqual(len(self.rows(2)), 4)
        before = len(self.doc.Objects)
        self.widget.edit_row(self.model(self.unused).data(0, panel._ROLE))
        self.assertEqual(editing.context_path(self.doc), (self.unused, ()))
        self.assertEqual(len(self.doc.Objects), before)

    def test_tab_guard_stale_rows_and_per_view_context(self):
        old_row = self.occurrence((self.second, self.nested)).data(0, panel._ROLE)
        old_view = Gui.activeDocument().activeView()
        first_subwindow = Gui.getMainWindow().findChild(QtWidgets.QMdiArea).activeSubWindow()
        Gui.activeDocument().createView('Gui::View3DInventor')
        editing.edit((self.first, self.nested)); settle()
        self.widget.edit_row(self.model(self.parent).data(0, panel._ROLE))
        self.widget.edit_row(self.model(self.child).data(0, panel._ROLE))
        self.assertEqual(editing.context_path(self.doc)[1], (self.first, self.nested))
        Gui.getMainWindow().findChild(QtWidgets.QMdiArea).setActiveSubWindow(first_subwindow)
        settle()
        self.assertEqual(Gui.activeDocument().activeView(), old_view)
        self.assertEqual(editing.context_path(self.doc)[1], (self.second, self.nested))
        other = document.new_document('OtherPanelFile')
        with self.assertRaises(ValueError): self.widget.edit_row(old_row)
        settle()
        self.assertEqual(self.widget._binding[0], other)
        App.setActiveDocument(self.doc.Name); settle()
        with document.transaction(self.doc, 'Remove occurrence'):
            self.doc.removeObject(self.second.Name)
        settle()
        with self.assertRaises(ValueError): self.widget.edit_row(old_row)
        self.doc.undo(); self.doc.recompute(); settle()
        restored = self.doc.getObject(old_row.path[0][2])
        self.assertIsNotNone(restored)
        self.assertEqual(len([r for _, r in self.rows(1) if r.kind == 'occurrence']), 4)

    def test_nested_import_labels_and_external_edit_remain_in_assembly(self):
        document.save_document(self.doc, self.output / 'Assembly.cadprt')
        source = document.new_document('Hardware')
        source_root = document.validate(source)
        source_root.Definitions[0].Label = self.child.Label
        document.save_document(source, self.output / 'Hardware.cadprt')
        leaf = document.new_document('Fasteners')
        document.save_document(leaf, self.output / 'Fasteners.cadprt')
        external.import_file(source, leaf)
        document.save_document(source)
        external.import_file(self.doc, source)
        link = hierarchy.add_instance(self.root, source_root.Definitions[0])
        App.setActiveDocument(self.doc.Name); settle()
        labels = [r.label for _, r in self.rows(0)]
        self.assertIn('Shared child (Hardware)', labels)
        self.assertIn('Part001 (Fasteners)', labels)
        self.assertIn('Hardware', labels)
        self.assertIn('Fasteners', labels)
        self.click(0, self.model(source_root.Definitions[0]), double=True)
        self.assertEqual(App.ActiveDocument, self.doc)
        self.assertEqual(editing.context_path(self.doc), (source_root.Definitions[0], (link,)))
        sketch = editing.new_sketch(self.doc); settle()
        self.assertEqual(sketch.Document, source)
        self.assertEqual([panel.lookup(r.ref) for _, r in self.rows(2)], [sketch])

    def test_file_origin_visibility_persistence_and_no_display_model_mutation(self):
        editing.edit_file(self.doc); settle()
        origin = self.root.Origin
        origin.Visibility = False; settle()
        plane_item = next(item for item, row in self.rows(2) if panel.lookup(row.ref).TypeId == 'App::Plane')
        plane = panel.lookup(plane_item.data(0, panel._ROLE).ref)
        plane.Visibility = False; settle()
        plane_item.setCheckState(0, QtCore.Qt.Checked); settle()
        self.assertTrue(plane.Visibility)
        self.assertTrue(origin.Visibility)
        self.doc.undo(); self.doc.recompute(); settle()
        self.assertFalse(origin.Visibility)
        self.doc.redo(); self.doc.recompute(); settle()
        self.assertTrue(origin.Visibility)
        path = document.save_document(self.doc, self.output / 'Panel.cadprt')
        ids = {o.Name: o.ID for o in self.doc.Objects}
        self.widget.close(); App.closeDocument(self.doc.Name)
        self.doc = document.open_document(path)
        self.widget = panel.show_panel(); settle()
        self.assertEqual({o.Name: o.ID for o in self.doc.Objects}, ids)
        self.assertEqual(self.widget.trees[1].topLevelItemCount(), 1)
        self.assertEqual(len(self.rows(2)), 4)

    def test_event_coalescing_idle_and_observer_cleanup(self):
        before = self.widget.refresh_count
        for i in range(20): self.child.Label = 'Child ' + str(i)
        settle()
        self.assertLessEqual(self.widget.refresh_count - before, 2)
        self.assertEqual(self.model(self.child).text(0), 'Child 19')
        before = self.widget.refresh_count
        QtTest.QTest.qWait(350)
        self.assertEqual(self.widget.refresh_count, before)
        callbacks = len(editing._context_observers)
        self.widget.close(); settle()
        self.assertEqual(len(editing._context_observers), callbacks - 1)
        before = self.widget.refresh_count
        self.child.Label = 'After close'; self.doc.recompute(); settle()
        self.assertEqual(self.widget.refresh_count, before)
        self.widget = panel.show_panel(); settle()
        self.assertEqual(len(editing._context_observers), callbacks)
