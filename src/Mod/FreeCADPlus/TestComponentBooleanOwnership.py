# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Boolean ownership inside one component: persistence and History projection."""
import json
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtWidgets
from freecad_plus import document, editing, geometry, panel
from TestComponentPanel import TestComponentPanel, settle
from TestComponentModeling import TestComponentModeling, accept_task, messages
from TestComponentInputEditors import TestComponentInputEditors


class TestComponentBooleanOwnership(unittest.TestCase):
    setUp = TestComponentPanel.setUp
    tearDown = TestComponentModeling.tearDown
    select = TestComponentModeling.select
    task_button = TestComponentInputEditors.task_button
    rows = TestComponentPanel.rows
    click = TestComponentPanel.click

    def fixture(self):
        Gui.activateWorkbench('PartDesignWorkbench')
        self.tool = self.doc.addObject('PartDesign::Body', 'ToolBody')
        self.child.addObject(self.tool)
        self.tool_box = self.tool.newObject('PartDesign::AdditiveBox', 'ToolBox')
        self.tool_box.Length = 2; self.tool_box.Width = 2; self.tool_box.Height = 2
        self.tool_box.Placement.Base = App.Vector(9, 1, 1)
        self.body = self.doc.addObject('PartDesign::Body', 'ResultBody')
        self.child.addObject(self.body)
        self.base = self.body.newObject('PartDesign::AdditiveBox', 'BaseBox')
        self.base.Length = 10; self.base.Width = 6; self.base.Height = 4
        self.doc.recompute(); editing.edit((self.second, self.nested)); settle()
        document.validate(self.doc)

    def create(self):
        self.select(self.tool)
        with messages() as errors: Gui.runCommand('PartDesign_Boolean'); settle()
        self.assertFalse(errors, errors)
        self.target = Gui.activeDocument().getInEdit().Object
        self.assertEqual(list(self.target.Group), [self.tool])
        document.validate(self.doc)
        accept_task(); self.assertFalse(Gui.Control.activeDialog())
        self.assertTrue(self.target.Shape.isValid()); self.assertAlmostEqual(self.target.Shape.Volume, 244)

    def test_native_creation_history_undo_and_save(self):
        self.fixture(); before_ids = {o.Name: o.ID for o in self.doc.Objects}
        self.create(); name = self.target.Name
        self.assertNotIn(self.tool, self.child.Group)
        self.assertEqual(document.owned_path(self.child, self.tool_box),
                         (self.body, self.target, self.tool, self.tool_box))
        history = document.history(self.doc, self.child)
        self.assertLess(history.index(self.tool_box), history.index(self.target))
        self.assertFalse(any(o.TypeId == 'PartDesign::Body' for o in history))
        self.assertEqual(len(history), len(set(history)))
        self.doc.undo(); self.doc.recompute(); settle()
        self.assertEqual({o.Name: o.ID for o in self.doc.Objects}, before_ids)
        self.assertIn(self.tool, self.child.Group); document.validate(self.doc)
        self.doc.redo(); self.doc.recompute(); settle()
        self.target = self.doc.getObject(name); document.validate(self.doc)
        self.assertEqual(list(self.target.Group), [self.tool])
        document.save_document(self.doc, self.output / 'Boolean.cadprt')
        (self.output / 'expected.json').write_text(json.dumps({
            'ids': {o.Name: o.ID for o in self.doc.Objects}, 'definition': self.child.Name,
            'body': self.body.Name, 'target': name, 'tool': self.tool.Name,
            'source': self.tool_box.Name, 'volume': self.target.Shape.Volume,
            'history': [o.Name for o in document.history(self.doc, self.child)]}))

    def test_nested_history_selection_edit_and_cancel(self):
        self.fixture(); self.create(); self.widget.refresh(); settle()
        item, row = next((item, row) for item, row in self.rows(2) if panel.lookup(row.ref) == self.tool_box)
        self.assertEqual(self.root.getSubObject(row.selection[2], 1), self.tool_box)
        self.click(2, item)
        selected = Gui.Selection.getSelectionEx('*', 0)
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].Object.getSubObject(selected[0].SubElementNames[0], 1), self.tool_box)
        geometry.require_modeling_inputs(self.target, [(self.root, row.selection[2])])
        Gui.Selection.clearSelection()
        old_length = self.tool_box.Length.Value
        editing.edit_feature(self.doc, self.tool_box); settle()
        self.assertEqual(Gui.activeDocument().getInEdit().Object, self.tool_box)
        self.tool_box.Length = old_length + 1; self.doc.recompute()
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.assertAlmostEqual(self.tool_box.Length.Value, old_length)
        document.validate(self.doc)

    def test_cancel_new_boolean_restores_tool_ownership(self):
        self.fixture(); ids = {o.Name: o.ID for o in self.doc.Objects}
        self.select(self.tool)
        with messages() as errors: Gui.runCommand('PartDesign_Boolean'); settle()
        self.assertFalse(errors, errors); document.validate(self.doc)
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.assertEqual({o.Name: o.ID for o in self.doc.Objects}, ids)
        self.assertIn(self.tool, self.child.Group); document.validate(self.doc)

    def test_ownership_does_not_follow_boolean_dependencies(self):
        self.fixture(); self.create()
        self.assertNotIn(self.base, document.owned_children(self.target))
        self.assertIsNone(document.owned_path(self.target, self.base))
        self.assertIsNone(document.owned_path(self.first, self.child))
        # Native Group is ownership; arbitrary source links must not disguise orphans.
        orphan = self.doc.addObject('Part::Feature', 'Orphan')
        self.target.addProperty('App::PropertyLink', 'TestDependency'); self.target.TestDependency = orphan
        with self.assertRaisesRegex(ValueError, 'outside component ownership'): document.validate(self.doc)
        self.target.TestDependency = None; self.doc.removeObject(orphan.Name)
        document.validate(self.doc)


def verify_fresh_process(output):
    path = Path(output) / 'test_native_creation_history_undo_and_save'
    expected = json.loads((path / 'expected.json').read_text())
    doc = document.open_document(path / 'Boolean.cadprt')
    try:
        assert {o.Name: o.ID for o in doc.Objects} == expected['ids']
        target = doc.getObject(expected['target']); tool = doc.getObject(expected['tool'])
        definition = doc.getObject(expected['definition']); source = doc.getObject(expected['source'])
        assert list(target.Group) == [tool] and tool not in definition.Group
        assert [o.Name for o in document.history(doc, definition)] == expected['history']
        assert doc.getObject(expected['body']).Tip == target
        assert abs(target.Shape.Volume - expected['volume']) < 1e-7
        source.Length = source.Length.Value + 1; doc.recompute(); document.validate(doc)
        assert target.Shape.isValid() and 'Invalid' not in target.State
        assert abs(target.Shape.Volume - expected['volume'] - 4) < 1e-7
    finally: App.closeDocument(doc.Name)
