# SPDX-License-Identifier: LGPL-2.1-or-later
"""Reference/Excluded eligibility at actual component consumer boundaries."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
from freecad_plus import document, display, editing, geometry, hierarchy, panel, movement
import TestComponentPanel as fixtures
from TestComponentMove import TestComponentMove
from TestUnusedModels import TestUnusedModels, visibility
settle = fixtures.settle


class TestComponentEligibility(unittest.TestCase):
    setUp = fixtures.TestComponentPanel.setUp
    tearDown = TestComponentMove.tearDown
    rows = fixtures.TestComponentPanel.rows
    occurrence = fixtures.TestComponentPanel.occurrence
    row = TestComponentMove.row
    task = TestComponentMove.task
    external_fixture = TestUnusedModels.external_fixture

    def sub(self, path):
        body = self.pad.getParentGeoFeatureGroup()
        return hierarchy.subname(path) + body.Name + '.' + self.pad.Name + '.Edge1'

    def access(self, path, active=None, active_path=()):
        return geometry.require_access(self.doc, self.root, self.sub(path),
                                       active=active, active_path=active_path)

    def test_reference_excluded_aggregate_and_shared_occurrence(self):
        vis = visibility(self.doc); ids = {o.Name:o.ID for o in self.doc.Objects}
        display.set_state(self.root, self.first, part_type='Reference')
        with self.assertRaisesRegex(ValueError, 'Add Reference Feature'):
            self.access((self.first, self.nested))
        self.assertEqual(self.access((self.second, self.nested)), self.pad)
        with self.assertRaisesRegex(ValueError, 'Reference'):
            geometry.require_access(self.doc, self.root)
        # A selected whole parent must not leak forbidden nested raw Link shapes.
        display.set_state(self.parent, self.nested, part_type='Excluded')
        with self.assertRaisesRegex(ValueError, 'Excluded'):
            geometry.require_access(self.doc, self.root, self.second.Name + '.')
        self.assertEqual(visibility(self.doc), vis)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, ids)

    def test_edit_override_owned_feature_and_no_foreign_bypass(self):
        display.set_state(self.root, self.first, part_type='Excluded')
        display.set_state(self.parent, self.nested, part_type='Reference')
        route = (self.first, self.nested)
        self.assertEqual(self.access(route, self.child, route), self.pad)
        self.assertEqual(geometry.require_access(self.doc, self.pad, 'Edge1',
                         active=self.child, active_path=route), self.pad)
        with self.assertRaisesRegex(ValueError, 'occurrence'):
            geometry.require_access(self.doc, self.pad, 'Edge1', active=self.parent, active_path=(self.first,))
        # An owned derived feature remains usable despite its source dependency.
        owned = self.doc.addObject('Part::Feature', 'OwnedDerived')
        owned.Shape = Part.makeBox(1,1,1); self.parent.addObject(owned)
        owned.addProperty('App::PropertyLink','Source'); owned.Source = self.pad
        self.doc.recompute()
        self.assertEqual(geometry.require_access(self.doc, owned, 'Edge1',
                         active=self.parent, active_path=(self.first,)), owned)
        self.assertEqual(display.state(self.first)[0], 'Excluded')
        self.assertEqual(display.state(self.nested)[0], 'Reference')

    def test_visibility_is_not_eligibility_and_persistence(self):
        display.set_state(self.root, self.first, shown=False)
        self.assertEqual(self.access((self.first,self.nested)),self.pad)
        display.set_state(self.root, self.first, part_type='Reference')
        with self.assertRaises(ValueError): self.access((self.first,self.nested))
        self.doc.undo(); self.doc.recompute(); settle()
        self.assertEqual(self.access((self.first,self.nested)),self.pad)
        self.doc.redo(); self.doc.recompute(); settle()
        ids={o.Name:o.ID for o in self.doc.Objects}; vis=visibility(self.doc)
        undo=self.doc.UndoCount
        for unused in range(3):
            with self.assertRaises(ValueError): self.access((self.first,self.nested))
        self.assertEqual(self.doc.UndoCount,undo)
        document.save_document(self.doc,self.output/'Eligibility.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':ids,'visibility':vis,
            'first':self.first.Name,'second':self.second.Name,'nested':self.nested.Name,
            'sub':self.sub((self.first,self.nested)),'allowed':self.sub((self.second,self.nested))}))

    def test_external_unused_source_and_occurrence_validation(self):
        source, definition = self.external_fixture()
        imported_child = source.getObject(document.validate(source).Definitions[0].Name)
        link = hierarchy.add_instance(definition, imported_child)
        feature = source.addObject('Part::Feature','ExternalResult')
        feature.Shape=Part.makeBox(1,1,1); imported_child.addObject(feature); source.recompute()
        display.set_state(definition,link,part_type='Reference')
        sub=link.Name+'.'+feature.Name+'.Edge1'
        with self.assertRaisesRegex(ValueError,'Reference'):
            geometry.require_access(self.doc,definition,sub,active=definition)
        with self.assertRaisesRegex(ValueError,'occurrence'):
            geometry.require_access(self.doc,feature,'Edge1',active=definition)
        self.assertEqual(geometry.require_access(self.doc,feature,'Edge1',active=imported_child),feature)
        with self.assertRaisesRegex(ValueError,'invalid'):
            geometry.require_access(self.doc,definition,'Missing.',active=definition)
        self.assertFalse(any('PlusChildPartType' in o.PropertiesList for o in self.doc.Objects))

    def test_consumer_rejects_before_shape_read_but_panel_edit_remains(self):
        # Whole component rows remain navigable; no global SelectionGate is installed.
        display.set_state(self.root,self.first,part_type='Reference');settle()
        item=self.occurrence((self.first,))
        self.assertIn('Add Reference Feature',item.toolTip(0))
        self.widget.edit_row(item.data(0,panel._ROLE));settle()
        self.assertEqual(editing.context_path(self.doc),(self.parent,(self.first,)))
        task=self.task((self.second,))  # File context, moving an ordinary sibling.
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.doc.Name,self.root.Name,self.sub((self.first,self.nested)))
        ids={o.Name:o.ID for o in self.doc.Objects};undo=self.doc.UndoCount
        with patch.object(movement.Part,'getShape',side_effect=AssertionError('Forbidden raw shape read')):
            for callback in (task.pick_direction,task.pick_axis,task.pick_pivot):
                with self.assertRaisesRegex(ValueError,'Reference'):callback()
            with self.assertRaisesRegex(ValueError,'Reference'):task.pick_axis_point(0)
        self.assertIsNone(task.direction_snapshot);self.assertIsNone(task.axis_snapshot)
        self.assertIsNone(task.pivot_snapshot);self.assertEqual(task.axis_points,[None,None])
        self.assertEqual(self.doc.UndoCount,undo)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
        task.finish();settle()
        self.assertEqual(display.state(self.first)[0],'Reference')


def verify_fresh_process(output):
    folder=Path(output)/'test_visibility_is_not_eligibility_and_persistence'
    expected=json.loads((folder/'expected.json').read_text())
    doc=document.open_document(folder/'Eligibility.cadprt')
    try:
        root=document.validate(doc)
        assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
        assert visibility(doc)==expected['visibility']
        try:geometry.require_access(doc,root,expected['sub'])
        except ValueError as error:assert 'Reference' in str(error)
        else:raise AssertionError('Saved Reference geometry was accepted')
        assert geometry.require_access(doc,root,expected['allowed']) is not None
    finally:App.closeDocument(doc.Name)
