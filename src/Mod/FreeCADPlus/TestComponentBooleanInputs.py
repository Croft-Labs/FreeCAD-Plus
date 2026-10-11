# SPDX-License-Identifier: LGPL-2.1-or-later
"""Boolean command/picker admission retains original component occurrences."""
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtWidgets
from freecad_plus import document, display, editing, geometry, hierarchy
from TestComponentPanel import TestComponentPanel, settle
from TestComponentModeling import TestComponentModeling, messages, accept_task
from TestComponentBooleanOwnership import TestComponentBooleanOwnership
from TestComponentReferences import TestComponentReferences
from TestComponentInputEditors import TestComponentInputEditors


class TestComponentBooleanInputs(unittest.TestCase):
    setUp = TestComponentPanel.setUp
    tearDown = TestComponentModeling.tearDown
    fixture = TestComponentBooleanOwnership.fixture
    select = TestComponentModeling.select
    control = TestComponentReferences.control
    task_button = TestComponentInputEditors.task_button

    def reference_child(self):
        definition = hierarchy.create_definition(self.doc, 'Reference source')
        self.reference_body = self.doc.addObject('PartDesign::Body', 'ReferenceBody')
        definition.addObject(self.reference_body)
        self.reference_box = self.reference_body.newObject('PartDesign::AdditiveBox', 'ReferenceBox')
        self.reference_link = hierarchy.add_instance(self.child, definition)
        display.set_state(self.child, self.reference_link, part_type='Reference')
        self.doc.recompute(); editing.edit((self.second, self.nested)); settle()
        return (hierarchy.subname((self.second, self.nested, self.reference_link))
                + self.reference_body.Name + '.')

    def snapshot(self):
        return ({o.Name:o.ID for o in self.doc.Objects}, self.body.Tip,
                self.doc.UndoCount, App.getActiveTransaction(),
                [(o.Name, tuple(x.Name for x in document.owned_children(o))) for o in self.doc.Objects],
                [(o.Name, o.Visibility) for o in self.doc.Objects if hasattr(o, 'Visibility')])

    def command_denied(self, reason):
        before = self.snapshot()
        with messages() as errors: Gui.runCommand('PartDesign_Boolean'); settle()
        self.assertTrue(any(reason in error for error in errors), errors)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(Gui.Control.activeDialog())
        document.validate(self.doc)

    def test_command_reference_excluded_and_mixed_batch_are_atomic(self):
        self.fixture(); path = self.reference_child()
        self.select(self.root, path)
        self.command_denied('Add Reference Feature')
        # A valid first item must not be consumed when a later reference is refused.
        self.select(self.tool); Gui.Selection.addSelection(self.doc.Name, self.root.Name, path)
        self.command_denied('Add Reference Feature')
        display.set_state(self.child, self.reference_link, part_type='Excluded'); settle()
        self.select(self.root, path); self.command_denied('Excluded')
        # The same tool definition selected through a forbidden shared occurrence
        # must not inherit permission from its currently edited occurrence.
        display.set_state(self.root, self.first, part_type='Excluded'); settle()
        self.select(self.root, hierarchy.subname((self.first,self.nested))+self.tool.Name+'.')
        self.command_denied('Excluded')

    def test_empty_selection_requires_component_context(self):
        self.fixture(); view = Gui.activeDocument().activeView()
        resolved, parent, sub = view.getActiveObject('PlusEdit', False)
        view.setActiveObject('PlusEdit', None); self.select(self.tool)
        self.command_denied('Edit a component')
        view.setActiveObject('PlusEdit', parent, sub)
        Gui.Selection.clearSelection(); before = self.snapshot()
        with messages() as errors: Gui.runCommand('PartDesign_Boolean'); settle()
        self.assertFalse(errors, errors); self.assertTrue(Gui.Control.activeDialog())
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.assertEqual(self.snapshot(), before)

    def test_picker_rejects_reference_then_allows_owned_tool_and_cleanup(self):
        self.fixture(); path = self.reference_child()
        Gui.Selection.clearSelection()
        with messages() as errors: Gui.runCommand('PartDesign_Boolean'); settle()
        self.assertFalse(errors, errors)
        target = Gui.activeDocument().getInEdit().Object
        button = self.control(QtWidgets.QAbstractButton, 'buttonBodyAdd')
        button.setChecked(True); settle()
        before = self.snapshot(); groups = list(target.Group)
        original = geometry.require_modeling_inputs; denied = []; inputs_seen = []
        def observe(consumer, inputs=None):
            inputs_seen.append(inputs)
            try: return original(consumer, inputs)
            except ValueError as error: denied.append(str(error)); raise
        with patch.object(geometry, 'require_modeling_inputs', side_effect=observe), messages():
            self.select(self.root, path); settle()
        self.assertTrue(any('Add Reference Feature' in error for error in denied), denied)
        self.assertTrue(any(refs and refs[0] == (self.root,path) for refs in inputs_seen), inputs_seen)
        self.assertEqual(self.snapshot(), before); self.assertEqual(list(target.Group),groups)
        self.assertEqual(self.control(QtWidgets.QListWidget,'listWidgetBodies').count(),0)
        self.assertTrue(button.isChecked())
        self.select(self.tool); settle()
        self.assertEqual(list(target.Group),[self.tool]); self.assertTrue(target.Shape.isValid())
        self.assertAlmostEqual(target.Shape.Volume,244)
        remove = self.control(QtWidgets.QAbstractButton,'buttonBodyRemove'); remove.setChecked(True); settle()
        with patch.object(geometry,'require_modeling_inputs',side_effect=AssertionError('Removal reached admission')):
            self.select(self.tool); settle()
        self.assertFalse(target.Group)
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.assertIn(self.tool,self.child.Group); document.validate(self.doc)

    def test_legacy_command_and_picker_bypass_component_policy(self):
        Gui.activateWorkbench('PartDesignWorkbench')
        doc = App.newDocument('LegacyBooleanInputs')
        tool = doc.addObject('PartDesign::Body','LegacyTool')
        box = tool.newObject('PartDesign::AdditiveBox','ToolBox'); box.Length=2; box.Width=2; box.Height=2
        box.Placement.Base=App.Vector(9,1,1)
        body = doc.addObject('PartDesign::Body','LegacyResult')
        base = body.newObject('PartDesign::AdditiveBox','BaseBox'); base.Length=10; base.Width=6; base.Height=4
        doc.recompute(); Gui.activeDocument().activeView().setActiveObject('pdbody',body)
        Gui.Selection.clearSelection()
        with patch.object(geometry,'require_modeling_inputs',side_effect=AssertionError('Legacy reached Plus policy')):
            with messages() as errors: Gui.runCommand('PartDesign_Boolean'); settle()
            self.assertFalse(errors,errors)
            target = Gui.activeDocument().getInEdit().Object
            self.control(QtWidgets.QAbstractButton,'buttonBodyAdd').setChecked(True); settle()
            self.select(tool); settle(); self.assertEqual(list(target.Group),[tool])
            accept_task()
        self.assertTrue(target.Shape.isValid()); self.assertAlmostEqual(target.Shape.Volume,244)
