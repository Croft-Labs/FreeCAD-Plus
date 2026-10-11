# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Loft/Pipe occurrence-aware input admission and persistence."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, display, editing, geometry
from TestComponentPanel import TestComponentPanel, settle
from TestComponentModeling import TestComponentModeling, accept_task
from TestComponentInputEditors import TestComponentInputEditors


class TestComponentSweepInputs(unittest.TestCase):
    setUp = TestComponentPanel.setUp
    tearDown = TestComponentModeling.tearDown
    sub = TestComponentModeling.sub
    select = TestComponentModeling.select
    task_button = TestComponentInputEditors.task_button

    def fixture(self, kind, legacy=False):
        Gui.activateWorkbench('PartDesignWorkbench')
        doc = App.newDocument('LegacySweep') if legacy else self.doc
        owner = doc if legacy else self.child
        body = owner.newObject('PartDesign::Body', 'SweepBody') if not legacy else doc.addObject('PartDesign::Body', 'SweepBody')
        def circle(name, z, radius):
            obj = body.newObject('Sketcher::SketchObject', name)
            obj.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), radius), False)
            obj.Placement.Base.z = z
            return obj
        self.profile = circle('SweepProfile', 0, 2)
        self.replacement = circle('ReplacementProfile', 0, 2.5)
        self.section = circle('SweepSection', 10, 2)
        self.extra = circle('ExtraSection', 15, 2)
        def path(name, x):
            obj = body.newObject('Sketcher::SketchObject', name)
            obj.addGeometry(Part.LineSegment(App.Vector(x, 0, 0), App.Vector(x, 5, 0)), False)
            obj.addGeometry(Part.LineSegment(App.Vector(x, 5, 0), App.Vector(x, 10, 0)), False)
            obj.Placement.Rotation = App.Rotation(App.Vector(1, 0, 0), 90)
            return obj
        self.path = path('SweepPath', 0)
        self.aux = path('AuxiliaryPath', 5)
        self.target = body.newObject('PartDesign::Additive' + kind, 'Sweep')
        self.target.Profile = self.profile
        if kind == 'Loft': self.target.Sections = [self.section]
        else: self.target.Spine = (self.path, [])
        doc.recompute()
        self.assertTrue(self.target.Shape.isValid())
        self.assertGreater(self.target.Shape.Volume, 0)
        Gui.Selection.clearSelection()
        if legacy:
            Gui.activeDocument().activeView().setActiveObject('pdbody', body)
            Gui.activeDocument().setEdit(self.target.Name)
        else:
            display.set_state(self.root, self.first, part_type='Reference')
            editing.edit_feature(doc, self.target)
        settle()
        return doc

    def control(self, form, kind, name):
        proxy = Gui.getMainWindow().findChild(QtWidgets.QWidget, 'PartDesignGui__Task' + form)
        self.assertIsNotNone(proxy, form)
        obj = proxy.findChild(kind, name)
        self.assertIsNotNone(obj, name)
        return obj

    def pick(self, form, button, obj, element='', forbidden=False, legacy=False):
        widget = self.control(form, QtWidgets.QToolButton, button)
        if widget.isChecked(): widget.setChecked(False)
        widget.setChecked(True); settle()
        if legacy: self.select(obj, element)
        else: self.select(self.root, self.sub(self.first if forbidden else self.second, obj, element))
        settle()

    def snapshot(self):
        target = self.target
        names = ['Profile', 'Sections'] + (['Spine', 'AuxiliarySpine'] if 'Spine' in target.PropertiesList else [])
        return ([getattr(target, name) for name in names], target.Shape.Volume,
                target.Document.UndoCount, App.getActiveTransaction(),
                {o.Name: o.ID for o in target.Document.Objects},
                [[w.item(i).text() for i in range(w.count())]
                 for w in Gui.getMainWindow().findChildren(QtWidgets.QListWidget, 'listWidgetReferences')])

    def denied(self, form, button, obj, element=''):
        before = self.snapshot()
        original = geometry.require_modeling_inputs
        with patch.object(geometry, 'require_modeling_inputs', wraps=original) as calls:
            self.pick(form, button, obj, element, forbidden=True)
        self.assertTrue(any(refs and refs[0][0] == self.root and refs[0][1].startswith(self.sub(self.first, obj))
                            and (not element or refs[0][1].endswith('.' + element))
                            for call in calls.call_args_list for refs in [call.args[1]]), calls.call_args_list)
        self.assertEqual(self.snapshot(), before)

    def save(self, filename):
        self.assertFalse(Gui.Control.activeDialog())
        self.assertTrue(self.target.Shape.isValid())
        self.assertNotIn('Invalid', self.target.State)
        document.save_document(self.doc, self.output / filename)
        (self.output / 'expected.json').write_text(json.dumps({
            'ids': {o.Name: o.ID for o in self.doc.Objects}, 'target': self.target.Name,
            'profile': self.replacement.Name, 'section': self.section.Name,
            'path': self.path.Name, 'aux': self.aux.Name, 'volume': self.target.Shape.Volume}))

    def test_loft_profile_sections_undo_and_reopen(self):
        self.fixture('Loft')
        for kind in ('Reference', 'Excluded'):
            # Metadata changes belong outside the editor transaction; the fixture starts Reference.
            if kind == 'Excluded':
                self.task_button(QtWidgets.QDialogButtonBox.Cancel)
                display.set_state(self.root, self.first, part_type=kind)
                editing.edit_feature(self.doc, self.target); settle()
            self.denied('LoftParameters', 'buttonProfileBase', self.replacement)
            self.denied('LoftParameters', 'buttonRefAdd', self.extra)
        self.pick('LoftParameters', 'buttonProfileBase', self.replacement)
        self.assertEqual(self.target.Profile[0], self.replacement)
        self.pick('LoftParameters', 'buttonRefAdd', self.extra)
        self.assertEqual([o for o, subs in self.target.Sections], [self.section, self.extra])
        # Removing an existing section is cleanup, not admission of forbidden geometry.
        self.pick('LoftParameters', 'buttonRefRemove', self.extra, forbidden=True)
        self.assertEqual([o for o, subs in self.target.Sections], [self.section])
        accept_task()
        self.doc.undo(); self.doc.recompute(); settle()
        self.assertEqual(self.target.Profile[0], self.profile)
        self.doc.redo(); self.doc.recompute(); settle()
        self.assertEqual(self.target.Profile[0], self.replacement)
        self.save('Loft.cadprt')

    def test_pipe_profile_path_edges_and_cancel(self):
        self.fixture('Pipe')
        self.denied('PipeParameters', 'buttonProfileBase', self.replacement)
        self.denied('PipeParameters', 'buttonSpineBase', self.path)
        self.denied('PipeParameters', 'buttonRefAdd', self.path, 'Edge1')
        self.pick('PipeParameters', 'buttonProfileBase', self.replacement)
        self.assertEqual(self.target.Profile[0], self.replacement)
        self.pick('PipeParameters', 'buttonSpineBase', self.path)
        self.assertEqual(self.target.Spine[0], self.path)
        self.pick('PipeParameters', 'buttonRefAdd', self.path, 'Edge1')
        self.assertIn('Edge1', self.target.Spine[1])
        # Native edge removal also sets the selected source object, so it needs admission.
        self.denied('PipeParameters', 'buttonRefRemove', self.path, 'Edge1')
        self.pick('PipeParameters', 'buttonRefAdd', self.path, 'Edge2')
        self.pick('PipeParameters', 'buttonRefRemove', self.path, 'Edge2')
        self.assertEqual(list(self.target.Spine[1]), ['Edge1'])
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.assertEqual(self.target.Profile[0], self.profile)
        self.assertEqual(list(self.target.Spine[1]), [])
        self.assertTrue(self.target.Shape.isValid())

    def test_pipe_auxiliary_sections_and_reopen(self):
        self.fixture('Pipe')
        self.pick('PipeParameters', 'buttonProfileBase', self.replacement)
        self.control('PipeOrientation', QtWidgets.QComboBox, 'comboBoxMode').setCurrentIndex(3); settle()
        self.denied('PipeOrientation', 'buttonProfileBase', self.aux)
        self.denied('PipeOrientation', 'buttonRefAdd', self.aux, 'Edge1')
        self.pick('PipeOrientation', 'buttonProfileBase', self.aux)
        self.assertEqual(self.target.AuxiliarySpine[0], self.aux)
        self.pick('PipeOrientation', 'buttonRefAdd', self.aux, 'Edge1')
        self.denied('PipeOrientation', 'buttonRefRemove', self.aux, 'Edge1')
        self.pick('PipeOrientation', 'buttonRefAdd', self.aux, 'Edge2')
        self.pick('PipeOrientation', 'buttonRefRemove', self.aux, 'Edge2')
        self.assertEqual(list(self.target.AuxiliarySpine[1]), ['Edge1'])
        self.pick('PipeOrientation', 'buttonProfileBase', self.aux)
        self.control('PipeScaling', QtWidgets.QComboBox, 'comboBoxScaling').setCurrentIndex(1); settle()
        self.denied('PipeScaling', 'buttonRefAdd', self.section)
        self.pick('PipeScaling', 'buttonRefAdd', self.section)
        self.assertEqual(self.target.Sections[0][0], self.section)
        self.pick('PipeScaling', 'buttonRefRemove', self.section, forbidden=True)
        self.assertFalse(self.target.Sections)
        self.pick('PipeScaling', 'buttonRefAdd', self.section)
        accept_task(); self.save('Pipe.cadprt')

    def test_legacy_loft_pipe_bypass(self):
        with patch.object(geometry, 'require_modeling_inputs', side_effect=AssertionError('Legacy reached Plus guard')):
            for kind in ('Loft', 'Pipe'):
                doc = self.fixture(kind, legacy=True)
                self.pick(kind + 'Parameters', 'buttonProfileBase', self.replacement, legacy=True)
                if kind == 'Loft':
                    self.pick('LoftParameters', 'buttonRefAdd', self.extra, legacy=True)
                else:
                    self.pick('PipeParameters', 'buttonSpineBase', self.path, legacy=True)
                    self.pick('PipeParameters', 'buttonRefAdd', self.path, 'Edge1', legacy=True)
                    self.pick('PipeParameters', 'buttonSpineBase', self.path, legacy=True)
                    self.control('PipeOrientation', QtWidgets.QComboBox, 'comboBoxMode').setCurrentIndex(3); settle()
                    self.pick('PipeOrientation', 'buttonProfileBase', self.aux, legacy=True)
                    self.control('PipeScaling', QtWidgets.QComboBox, 'comboBoxScaling').setCurrentIndex(1); settle()
                    self.pick('PipeScaling', 'buttonRefAdd', self.section, legacy=True)
                accept_task()
                self.assertFalse(Gui.Control.activeDialog())
                self.assertEqual(self.target.Profile[0], self.replacement)
                self.assertTrue(self.target.Shape.isValid())
                App.closeDocument(doc.Name)


def verify_fresh_process(output):
    for folder, filename in [('test_loft_profile_sections_undo_and_reopen', 'Loft.cadprt'),
                             ('test_pipe_auxiliary_sections_and_reopen', 'Pipe.cadprt')]:
        path = Path(output) / folder
        expected = json.loads((path / 'expected.json').read_text())
        doc = document.open_document(path / filename)
        try:
            assert {o.Name: o.ID for o in doc.Objects} == expected['ids']
            target = doc.getObject(expected['target'])
            assert target.Profile[0].Name == expected['profile']
            assert target.Sections[0][0].Name == expected['section']
            assert abs(target.Shape.Volume - expected['volume']) < 1e-7
            if 'Spine' in target.PropertiesList:
                assert target.Spine[0].Name == expected['path']
                assert target.AuxiliarySpine[0].Name == expected['aux']
            target.Profile[0].Geometry = [Part.Circle(App.Vector(), App.Vector(0, 0, 1), 3)]
            doc.recompute()
            assert target.Shape.isValid() and 'Invalid' not in target.State
            assert target.Shape.Volume > expected['volume'] + 1
        finally:
            App.closeDocument(doc.Name)
