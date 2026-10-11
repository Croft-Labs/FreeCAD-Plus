# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native shared dress-up/transformation component input boundaries."""
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
from TestComponentReferences import TestComponentReferences
from TestComponentInputEditors import TestComponentInputEditors


class TestComponentDressUpInputs(unittest.TestCase):
    setUp = TestComponentPanel.setUp
    tearDown = TestComponentModeling.tearDown
    sub = TestComponentModeling.sub
    select = TestComponentModeling.select
    control = TestComponentReferences.control
    task_button = TestComponentInputEditors.task_button

    def fixture(self, kind='Fillet', legacy=False):
        Gui.activateWorkbench('PartDesignWorkbench')
        doc = App.newDocument('LegacyDressUp') if legacy else self.doc
        body = doc.addObject('PartDesign::Body', 'InputBody')
        if not legacy: self.child.addObject(body)
        self.base = body.newObject('PartDesign::AdditiveBox', 'InputBox')
        self.base.Length = 10; self.base.Width = 6; self.base.Height = 4
        doc.recompute()
        if kind == 'LinearPattern':
            self.boss = body.newObject('PartDesign::AdditiveBox', 'InputBoss')
            self.boss.Length = 2; self.boss.Width = 2; self.boss.Height = 2
            self.boss.Placement.Base = App.Vector(2, 2, 4)
            doc.recompute()
        self.target = body.newObject('PartDesign::' + kind, 'InputResult')
        if kind == 'LinearPattern':
            axis = next(o for o in body.Origin.OriginFeatures if o.Name.startswith('X_Axis'))
            self.target.Originals = [self.base]
            self.target.Direction = (axis, [''])
            self.target.Length = 1; self.target.Occurrences = 2
        else:
            self.target.Base = (self.base, ['Edge1'])
            if kind == 'Fillet': self.target.Radius = 0.2
            else: self.target.Size = 0.2
        doc.recompute(); self.assertTrue(self.target.Shape.isValid(), self.target.State)
        Gui.Selection.clearSelection()
        if legacy:
            Gui.activeDocument().activeView().setActiveObject('pdbody', body)
            Gui.activeDocument().setEdit(self.target.Name)
        else:
            display.set_state(self.root, self.first, part_type='Reference')
            editing.edit_feature(doc, self.target)
        settle()
        return doc

    def pick(self, button, obj, element='', forbidden=False, legacy=False):
        widget = self.control(QtWidgets.QAbstractButton, button)
        if not widget.isChecked(): widget.setChecked(True)
        settle()
        if legacy: self.select(obj, element)
        else: self.select(self.root, self.sub(self.first if forbidden else self.second, obj, element))
        settle()

    def snapshot(self):
        target = self.target
        values = list(target.Originals) if 'Originals' in target.PropertiesList else (target.Base, target.UseAllEdges)
        return (values, target.Shape.Volume, target.Document.UndoCount, App.getActiveTransaction(),
                {o.Name: o.ID for o in target.Document.Objects},
                [[w.item(i).text() for i in range(w.count())] for w in Gui.getMainWindow().findChildren(QtWidgets.QListWidget)
                 if w.objectName() in ('listWidgetReferences', 'listWidgetFeatures')])

    def denied_pick(self, button, obj, element=''):
        before = self.snapshot()
        with patch.object(geometry, 'require_modeling_inputs', wraps=geometry.require_modeling_inputs) as calls, messages() as errors:
            self.pick(button, obj, element, forbidden=True)
        self.assertTrue(any(refs and refs[0][0] == self.root and refs[0][1].startswith(self.sub(self.first, obj))
                            for call in calls.call_args_list for refs in [call.args[1]]), calls.call_args_list)
        self.assertTrue(all('Reference' in error or 'Excluded' in error for error in errors), errors)
        self.assertEqual(self.snapshot(), before)

    def save(self, filename):
        self.assertFalse(Gui.Control.activeDialog())
        self.assertTrue(self.target.Shape.isValid())
        self.assertNotIn('Invalid', self.target.State)
        document.save_document(self.doc, self.output / filename)
        (self.output / 'expected.json').write_text(json.dumps({
            'ids': {o.Name: o.ID for o in self.doc.Objects}, 'target': self.target.Name,
            'source': self.base.Name, 'volume': self.target.Shape.Volume,
            'references': [o.Name for o in self.target.Originals] if 'Originals' in self.target.PropertiesList else list(self.target.Base[1])}))

    def test_dressup_pick_cleanup_undo_and_reopen(self):
        self.fixture()
        self.denied_pick('buttonRefSel', self.base, 'Edge2')
        self.pick('buttonRefSel', self.base, 'Edge2')
        self.assertEqual(set(self.target.Base[1]), {'Edge1', 'Edge2'})
        self.pick('buttonRefSel', self.base, 'Edge2', forbidden=True)
        self.assertEqual(list(self.target.Base[1]), ['Edge1'])
        self.pick('buttonRefSel', self.base, 'Edge2')
        accept_task()
        self.doc.undo(); self.doc.recompute(); settle()
        self.assertEqual(list(self.target.Base[1]), ['Edge1'])
        self.doc.redo(); self.doc.recompute(); settle()
        self.assertEqual(set(self.target.Base[1]), {'Edge1', 'Edge2'})
        self.save('Fillet.cadprt')

    def test_whole_edge_routes_context_loss_and_cancel(self):
        for kind in ('Fillet', 'Chamfer'):
            self.fixture(kind)
            refs = self.control(QtWidgets.QListWidget, 'listWidgetReferences')
            add_all = next(a for a in refs.actions() if a.text() == 'Add All Edges')
            checkbox = self.control(QtWidgets.QCheckBox, 'checkBoxUseAllEdges')
            picker = self.control(QtWidgets.QToolButton, 'buttonRefSel')
            view = Gui.activeDocument().activeView()
            resolved, parent, sub = view.getActiveObject('PlusEdit', False)
            view.setActiveObject('PlusEdit', None)
            before = self.snapshot()
            with messages() as errors:
                add_all.trigger(); settle()
                checkbox.setChecked(True); settle()
            self.assertTrue(all('Edit a component' in error for error in errors), errors)
            self.assertEqual(self.snapshot(), before)
            self.assertFalse(checkbox.isChecked()); self.assertTrue(refs.isEnabled()); self.assertTrue(picker.isEnabled())
            view.setActiveObject('PlusEdit', parent, sub)
            add_all.trigger(); self.doc.recompute(); settle()
            self.assertEqual(len(self.target.Base[1]), 12)
            checkbox.setChecked(True); settle()
            self.assertTrue(self.target.UseAllEdges); self.assertTrue(self.target.Shape.isValid())
            view.setActiveObject('PlusEdit', None)
            checkbox.setChecked(False); settle()
            self.assertFalse(self.target.UseAllEdges)
            view.setActiveObject('PlusEdit', parent, sub)
            self.task_button(QtWidgets.QDialogButtonBox.Cancel)
            self.assertEqual(list(self.target.Base[1]), ['Edge1'])
            self.assertFalse(self.target.UseAllEdges); self.assertTrue(self.target.Shape.isValid())

    def test_transformed_originals_cleanup_undo_and_reopen(self):
        self.fixture('LinearPattern')
        self.denied_pick('buttonAddFeature', self.boss)
        self.pick('buttonAddFeature', self.boss)
        self.assertEqual(list(self.target.Originals), [self.base, self.boss])
        self.pick('buttonRemoveFeature', self.boss, forbidden=True)
        self.assertEqual(list(self.target.Originals), [self.base])
        self.pick('buttonAddFeature', self.boss)
        accept_task()
        self.doc.undo(); self.doc.recompute(); settle()
        self.assertEqual(list(self.target.Originals), [self.base])
        self.doc.redo(); self.doc.recompute(); settle()
        self.assertEqual(list(self.target.Originals), [self.base, self.boss])
        self.save('Pattern.cadprt')

    def test_legacy_dressup_and_transformed_bypass(self):
        with patch.object(geometry, 'require_modeling_inputs', side_effect=AssertionError('Legacy reached Plus guard')):
            for kind in ('Fillet', 'LinearPattern'):
                doc = self.fixture(kind, legacy=True)
                if kind == 'Fillet':
                    self.pick('buttonRefSel', self.base, 'Edge2', legacy=True)
                    refs = self.control(QtWidgets.QListWidget, 'listWidgetReferences')
                    next(a for a in refs.actions() if a.text() == 'Add All Edges').trigger(); doc.recompute(); settle()
                    self.control(QtWidgets.QCheckBox, 'checkBoxUseAllEdges').setChecked(True); settle()
                    self.assertEqual(len(self.target.Base[1]), 12); self.assertTrue(self.target.UseAllEdges)
                else:
                    self.pick('buttonAddFeature', self.boss, legacy=True)
                    self.assertEqual(list(self.target.Originals), [self.base, self.boss])
                accept_task(); self.assertFalse(Gui.Control.activeDialog())
                self.assertTrue(self.target.Shape.isValid()); App.closeDocument(doc.Name)


def verify_fresh_process(output):
    for folder, filename in [('test_dressup_pick_cleanup_undo_and_reopen', 'Fillet.cadprt'),
                             ('test_transformed_originals_cleanup_undo_and_reopen', 'Pattern.cadprt')]:
        path = Path(output) / folder
        expected = json.loads((path / 'expected.json').read_text())
        doc = document.open_document(path / filename)
        try:
            assert {o.Name: o.ID for o in doc.Objects} == expected['ids']
            target = doc.getObject(expected['target']); source = doc.getObject(expected['source'])
            if 'Originals' in target.PropertiesList:
                assert [o.Name for o in target.Originals] == expected['references']
            else:
                assert target.Base[0] == source and list(target.Base[1]) == expected['references']
            assert abs(target.Shape.Volume - expected['volume']) < 1e-7
            source.Length = source.Length.Value + 2; doc.recompute()
            assert target.Shape.isValid() and 'Invalid' not in target.State
            assert target.Shape.Volume > expected['volume'] + 1
        finally: App.closeDocument(doc.Name)
