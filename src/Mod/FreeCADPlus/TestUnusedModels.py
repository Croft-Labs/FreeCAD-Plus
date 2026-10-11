# SPDX-License-Identifier: LGPL-2.1-or-later
"""Unused-definition editing, transient display and save/recovery acceptance."""
import json
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from pivy import coin
from freecad_plus import document, hierarchy, editing, external, panel, isolation
import TestComponentPanel as panel_tests
from TestComponentPanel import settle


def visibility(doc):
    return {obj.Name: bool(obj.Visibility) for obj in doc.Objects if hasattr(obj, 'Visibility')}


class TestUnusedModels(unittest.TestCase):
    setUp = panel_tests.TestComponentPanel.setUp
    tearDown = panel_tests.TestComponentPanel.tearDown
    rows = panel_tests.TestComponentPanel.rows
    model = panel_tests.TestComponentPanel.model
    occurrence = panel_tests.TestComponentPanel.occurrence
    click = panel_tests.TestComponentPanel.click

    def activate(self):
        self.click(0, self.model(self.unused), double=True)
        self.assertEqual(editing.context_path(self.doc), (self.unused, ()))
        return isolation.current(Gui.activeDocument().activeView())

    def geometry(self):
        sketch = editing.new_sketch(self.doc)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 3), False)
        sketch.Document.recompute()
        pad = editing.pad(self.doc, sketch, 7)
        settle()
        return sketch, pad

    def test_temporary_row_is_not_an_instance_and_restores_display(self):
        original = visibility(self.doc)
        ids = {o.Name: o.ID for o in self.doc.Objects}
        undo = self.doc.UndoCount
        session = self.activate()
        self.assertIsNotNone(session)
        rows = self.rows(1)
        temp = [(item, row) for item, row in rows if row.kind == 'unused']
        self.assertEqual(len(temp), 1)
        item, row = temp[0]
        self.assertEqual(row.label, 'Unused component (unused model)')
        file_item = self.widget.trees[1].topLevelItem(0)
        self.assertIs(file_item.child(file_item.childCount()-1), item)
        self.assertTrue(item.font(0).bold())
        self.assertFalse(item.flags() & QtCore.Qt.ItemIsDragEnabled)
        self.assertEqual(self.widget.trees[1].topLevelItemCount(), 1)
        for other, other_row in rows:
            if other_row.kind in ('file', 'occurrence'):
                self.assertTrue(other.flags() & QtCore.Qt.ItemIsSelectable)
                self.assertNotEqual(other.foreground(0).style(), QtCore.Qt.NoBrush)
        self.assertEqual({o.Name: o.ID for o in self.doc.Objects}, ids)
        self.assertEqual(visibility(self.doc), original)
        self.assertEqual(self.doc.UndoCount, undo)
        self.assertTrue(all(switch.whichChild.getValue() == coin.SO_SWITCH_NONE for _, switch in session.hidden))
        # Native show/selection cannot bypass the view's assembly-hiding switch.
        self.first.Visibility = False; self.first.Visibility = original[self.first.Name]
        self.click(1, self.occurrence((self.first,)))
        self.assertEqual(editing.context_path(self.doc), (self.unused, ()))
        self.assertTrue(all(switch.whichChild.getValue() == coin.SO_SWITCH_NONE for _, switch in session.hidden))
        self.click(1, self.occurrence((self.first,)), double=True)
        self.assertTrue(session.closed)
        self.assertIsNone(isolation.current(Gui.activeDocument().activeView()))
        self.assertFalse(any(r.kind == 'unused' for _, r in self.rows(1)))
        self.assertEqual(visibility(self.doc), original)
        self.assertTrue(all(session.scene.findChild(node) >= 0 for node, _ in session.hidden))

    def test_modeling_undo_and_save_during_isolation(self):
        original = visibility(self.doc)
        links = [o.Name for o in self.doc.Objects if o.TypeId == 'App::Link']
        self.activate()
        sketch, pad = self.geometry()
        self.assertEqual(pad.Document, self.doc)
        self.assertAlmostEqual(pad.Shape.Volume, 63 * 3.141592653589793)
        self.assertEqual(pad.getParentGeoFeatureGroup().Tip, pad)
        self.assertEqual(document.history(self.doc, self.unused), [sketch, pad])
        self.assertEqual([o.Name for o in self.doc.Objects if o.TypeId == 'App::Link'], links)
        name = pad.Name
        self.doc.undo(); self.doc.recompute(); settle()
        self.assertIsNone(self.doc.getObject(name))
        self.doc.redo(); self.doc.recompute(); settle()
        pad = self.doc.getObject(name)
        saved = document.save_document(self.doc, self.output/'Unused.cadprt')
        self.assertIsNotNone(isolation.current(Gui.activeDocument().activeView()))
        self.assertEqual({name: visibility(self.doc)[name] for name in original}, original)
        expected = {'ids': {o.Name:o.ID for o in self.doc.Objects}, 'visibility': visibility(self.doc),
                    'definition': self.unused.Name, 'pad': pad.Name, 'links': links}
        (self.output/'expected.json').write_text(json.dumps(expected))
        self.widget.close(); App.closeDocument(self.doc.Name)
        self.doc = document.open_document(saved)
        self.widget = panel.show_panel(); settle()
        self.assertEqual(visibility(self.doc), expected['visibility'])
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, expected['ids'])
        self.assertFalse(any(r.kind == 'unused' for _, r in self.rows(1)))

    def test_external_unused_refused_without_mutation_or_context_change(self):
        document.save_document(self.doc, self.output/'Assembly.cadprt')
        source = document.new_document('Hardware')
        definition = hierarchy.create_definition(source, 'Unused screw')
        document.save_document(source, self.output/'Hardware.cadprt')
        external.import_file(self.doc, source)
        App.setActiveDocument(self.doc.Name); settle()
        self.activate()
        original = visibility(source)
        ids = {o.Name:o.ID for o in self.doc.Objects}
        session = isolation.current(Gui.activeDocument().activeView())
        with self.assertRaisesRegex(ValueError, 'defining file'):
            self.widget.edit_row(self.model(definition).data(0, panel._ROLE))
        self.assertEqual(editing.context_path(self.doc), (self.unused, ()))
        self.assertEqual(App.ActiveDocument, self.doc)
        self.assertIs(isolation.current(Gui.activeDocument().activeView()), session)
        self.assertEqual(visibility(source), original)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, ids)
        self.assertIn('Unused screw (Hardware)', [r.label for _,r in self.rows(0)])

    def test_isolation_is_per_view_and_panel_close_cleans_up(self):
        first_view = Gui.activeDocument().activeView()
        session = self.activate()
        Gui.activeDocument().createView('Gui::View3DInventor')
        second_view = Gui.activeDocument().activeView()
        editing.edit((self.first,)); settle()
        self.assertIsNone(isolation.current(second_view))
        self.assertIs(isolation.current(first_view), session)
        scene = second_view.getSceneGraph()
        self.assertTrue(any(str(scene.getChild(i).getName()) == 'ObjectGroup' for i in range(scene.getNumChildren())))
        self.widget.close(); settle()
        self.assertTrue(session.closed)
        self.assertFalse(isolation._sessions)
        self.assertEqual(first_view.getActiveObject('PlusEdit'), self.root)
        self.widget = panel.show_panel()

    def test_native_sketch_editor_and_guarded_context_exit(self):
        session = self.activate()
        sketch, pad = self.geometry()
        gui = Gui.getDocument(self.doc.Name)
        body = pad.getParentGeoFeatureGroup()
        self.assertTrue(gui.setEdit(self.unused, 0, body.Name+'.'+sketch.Name+'.'))
        settle()
        self.assertEqual(gui.getInEdit().Object, sketch)
        with self.assertRaisesRegex(ValueError, 'Finish'):
            editing.edit_file(self.doc)
        self.assertFalse(session.closed)
        gui.resetEdit(); settle()
        self.assertEqual(editing.context_path(self.doc), (self.unused, ()))
        self.assertTrue(pad.Shape.isValid())
        editing.edit_file(self.doc); settle()
        self.assertTrue(session.closed)

    def test_removal_and_view_close_discard_transient_state(self):
        session = self.activate()
        name = self.unused.Name
        with document.transaction(self.doc, 'Remove unused definition'):
            self.root.Definitions = [d for d in self.root.Definitions if d != self.unused]
            self.doc.removeObject(name)
        settle()
        self.assertTrue(session.closed)
        self.assertFalse(any(r.kind == 'unused' for _, r in self.rows(1)))
        self.doc.undo(); self.doc.recompute(); settle()
        self.unused = self.doc.getObject(name)
        self.assertIsNotNone(self.unused)
        self.assertFalse(isolation._sessions)
        session = self.activate()
        # Closing the view/doc must detach observers and restore scene nodes safely.
        App.closeDocument(self.doc.Name); settle()
        self.assertTrue(session.closed)
        self.assertFalse(isolation._sessions)


def verify_fresh_process(output):
    folder = Path(output)/'test_modeling_undo_and_save_during_isolation'
    expected = json.loads((folder/'expected.json').read_text())
    doc = document.open_document(folder/'Unused.cadprt')
    widget = panel.show_panel(); settle()
    assert {o.Name:o.ID for o in doc.Objects} == expected['ids']
    assert visibility(doc) == expected['visibility']
    assert [o.Name for o in doc.Objects if o.TypeId == 'App::Link'] == expected['links']
    assert not isolation._sessions
    definition = doc.getObject(expected['definition'])
    editing.edit_unused(doc, definition)
    with document.transaction(doc, 'Fresh unused edit'): doc.getObject(expected['pad']).Length = 9
    doc.recompute(); settle()
    assert abs(doc.getObject(expected['pad']).Shape.Volume - 81*3.141592653589793) < 1e-8
    document.save_document(doc, folder/'Unused-edited.cadprt')
    widget.close(); App.closeDocument(doc.Name)
