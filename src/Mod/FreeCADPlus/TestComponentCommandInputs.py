# SPDX-License-Identifier: LGPL-2.1-or-later
"""Command-start component admission before selection normalization and mutation."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtWidgets
from freecad_plus import document, display, editing, geometry
from TestComponentPanel import TestComponentPanel, settle
from TestComponentModeling import TestComponentModeling, accept_task, messages
from TestComponentDressUpInputs import TestComponentDressUpInputs


class TestComponentCommandInputs(unittest.TestCase):
    setUp = TestComponentPanel.setUp
    tearDown = TestComponentModeling.tearDown
    sub = TestComponentModeling.sub
    select = TestComponentModeling.select
    control = TestComponentDressUpInputs.control
    task_button = TestComponentDressUpInputs.task_button
    pick = TestComponentDressUpInputs.pick

    def fixture(self, legacy=False):
        Gui.activateWorkbench('PartDesignWorkbench')
        doc = App.newDocument('LegacyCommands') if legacy else self.doc
        body = doc.addObject('PartDesign::Body', 'CommandBody')
        if not legacy: self.child.addObject(body)
        self.base = body.newObject('PartDesign::AdditiveBox', 'CommandBox')
        self.base.Length = 10; self.base.Width = 6; self.base.Height = 4
        doc.recompute()
        if legacy: Gui.activeDocument().activeView().setActiveObject('pdbody', body)
        else: editing.edit((self.second, self.nested))
        Gui.Selection.clearSelection(); settle()
        return doc, body

    def state(self, body):
        return ({o.Name: o.ID for o in body.Document.Objects}, body.Tip,
                body.Shape.Volume, body.Document.UndoCount, App.getActiveTransaction(),
                [(s.ObjectName, list(s.SubElementNames)) for s in Gui.Selection.getSelectionEx('*', 0)])

    def denied(self, command, body, reason):
        before = self.state(body)
        with messages() as errors: Gui.runCommand(command); settle()
        # A Reference ancestor outside its owner's Edit context is effectively Excluded.
        reasons = ('Reference', 'Excluded') if reason == 'Reference' else (reason,)
        self.assertTrue(any(term in error for error in errors for term in reasons), (command, errors))
        self.assertIsNone(Gui.activeDocument().getInEdit())
        self.assertEqual(self.state(body), before, command)

    def test_shared_command_rejection_and_mixed_batch(self):
        doc, body = self.fixture()
        for kind in ('Reference', 'Excluded'):
            display.set_state(self.root, self.first, part_type=kind); settle()
            for name in ('Fillet', 'Chamfer', 'Draft', 'Thickness', 'Mirrored',
                         'LinearPattern', 'PolarPattern', 'MultiTransform'):
                self.select(self.root, self.sub(self.first, self.base, 'Edge1'))
                self.denied('PartDesign_' + name, body, 'Excluded' if kind == 'Excluded' else 'Reference')
        # The disallowed sketch is dropped by the native Feature filter, so the
        # original mixed batch must be checked before that filtering happens.
        self.select(self.root, self.sub(self.second, self.base))
        Gui.Selection.addSelection(doc.Name, self.root.Name, self.sub(self.first, self.sketch))
        self.denied('PartDesign_LinearPattern', body, 'Excluded')

    def test_empty_selection_context_and_cancel(self):
        doc, body = self.fixture()
        view = Gui.activeDocument().activeView()
        resolved, parent, sub = view.getActiveObject('PlusEdit', False)
        view.setActiveObject('PlusEdit', None)
        for name in ('Fillet', 'LinearPattern'):
            self.denied('PartDesign_' + name, body, 'Edit a component')
        view.setActiveObject('PlusEdit', parent, sub)
        for name in ('Fillet', 'LinearPattern'):
            Gui.Selection.clearSelection(); before = self.state(body)[:4]
            with messages() as errors: Gui.runCommand('PartDesign_' + name); settle()
            self.assertFalse(errors, errors)
            self.assertIsNotNone(Gui.activeDocument().getInEdit())
            self.task_button(QtWidgets.QDialogButtonBox.Cancel)
            self.assertEqual(self.state(body)[:4], before)

    def create_and_save(self, kind):
        doc, body = self.fixture()
        display.set_state(self.root, self.first, part_type='Reference')
        self.select(self.root, self.sub(self.second, self.base, 'Edge1' if kind in ('Fillet', 'Chamfer') else ''))
        with messages() as errors: Gui.runCommand('PartDesign_' + kind); settle()
        self.assertFalse(errors, errors)
        target = Gui.activeDocument().getInEdit().Object
        accept_task(); self.assertTrue(target.Shape.isValid(), target.State)
        name = target.Name; volume = target.Shape.Volume
        self.assertEqual(body.Tip, target)
        doc.undo(); doc.recompute(); settle(); self.assertIsNone(doc.getObject(name))
        doc.redo(); doc.recompute(); settle(); target = doc.getObject(name)
        self.assertEqual(body.Tip, target); self.assertAlmostEqual(target.Shape.Volume, volume)
        document.save_document(doc, self.output / 'Command.cadprt')
        (self.output / 'expected.json').write_text(json.dumps({
            'ids': {o.Name: o.ID for o in doc.Objects}, 'target': name, 'source': self.base.Name,
            'body': body.Name, 'kind': kind, 'volume': volume}))

    def test_fillet_creation_undo_and_save(self): self.create_and_save('Fillet')

    def test_chamfer_creation_undo_and_save(self): self.create_and_save('Chamfer')

    def test_pattern_creation_undo_and_save(self): self.create_and_save('LinearPattern')

    def test_multitransform_conversion_rejects_original_occurrence(self):
        doc, body = self.fixture()
        pattern = body.newObject('PartDesign::LinearPattern', 'ExistingPattern')
        pattern.Originals = [self.base]
        axis = next(o for o in body.Origin.OriginFeatures if o.Name.startswith('X_Axis'))
        pattern.Direction = (axis, ['']); pattern.Length = 1; pattern.Occurrences = 2
        doc.recompute()
        display.set_state(self.root, self.first, part_type='Reference')
        self.select(self.root, self.sub(self.first, pattern))
        originals = list(pattern.Originals)
        self.denied('PartDesign_MultiTransform', body, 'Reference')
        self.assertEqual(list(pattern.Originals), originals)

    def test_pattern_rejection_stays_in_original_picker(self):
        TestComponentDressUpInputs.fixture(self, 'LinearPattern')
        before = (list(self.target.Originals), self.target.Direction, self.target.Direction2)
        with patch.object(geometry, 'require_modeling_inputs', wraps=geometry.require_modeling_inputs) as calls, messages():
            self.pick('buttonAddFeature', self.boss, forbidden=True)
        self.assertEqual(calls.call_count, 1, calls.call_args_list)
        self.assertEqual((list(self.target.Originals), self.target.Direction, self.target.Direction2), before)
        self.assertTrue(self.control(QtWidgets.QAbstractButton, 'buttonAddFeature').isChecked())
        self.pick('buttonAddFeature', self.boss)
        self.assertEqual(list(self.target.Originals), [self.base, self.boss])
        self.pick('buttonRemoveFeature', self.boss, forbidden=True)
        self.assertEqual(list(self.target.Originals), [self.base])
        with patch.object(geometry, 'require_modeling_inputs', wraps=geometry.require_modeling_inputs) as calls:
            self.pick('buttonAddFeature', self.base)
        self.assertEqual(calls.call_count, 0, calls.call_args_list)
        self.assertEqual((list(self.target.Originals), self.target.Direction, self.target.Direction2), before)
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)

    def test_legacy_command_bypass(self):
        with patch.object(geometry, 'require_modeling_inputs', side_effect=AssertionError('Legacy reached Plus guard')):
            for kind in ('Fillet', 'Chamfer', 'LinearPattern'):
                doc, body = self.fixture(legacy=True)
                self.select(self.base, 'Edge1' if kind in ('Fillet', 'Chamfer') else '')
                with messages() as errors: Gui.runCommand('PartDesign_' + kind); settle()
                self.assertFalse(errors, errors); accept_task()
                self.assertTrue(body.Tip.Shape.isValid()); App.closeDocument(doc.Name)


def verify_fresh_process(output):
    for folder in ('test_fillet_creation_undo_and_save', 'test_chamfer_creation_undo_and_save', 'test_pattern_creation_undo_and_save'):
        path = Path(output) / folder
        expected = json.loads((path / 'expected.json').read_text())
        doc = document.open_document(path / 'Command.cadprt')
        try:
            assert {o.Name: o.ID for o in doc.Objects} == expected['ids']
            target = doc.getObject(expected['target']); source = doc.getObject(expected['source'])
            assert doc.getObject(expected['body']).Tip == target
            if expected['kind'] in ('Fillet', 'Chamfer'): assert target.Base == (source, ['Edge1'])
            else: assert list(target.Originals) == [source]
            assert abs(target.Shape.Volume - expected['volume']) < 1e-7
            source.Length = source.Length.Value + 2; doc.recompute()
            assert target.Shape.isValid() and 'Invalid' not in target.State
            assert target.Shape.Volume > expected['volume'] + 1
        finally: App.closeDocument(doc.Name)
