# SPDX-License-Identifier: LGPL-2.1-or-later
"""Domestic hierarchy and shared-instance acceptance in an isolated FreeCAD GUI."""
import hashlib
import json
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from freecad_plus import document as component, hierarchy, editing
from freecad_plus.conversion import convert_file


def matrix_equal(test, a, b):
    test.assertTrue(all(abs(x-y) < 1e-8 for x,y in zip(a.toMatrix().A, b.toMatrix().A)))


class TestComponentHierarchy(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Set PLUS_TEST_DIR to an isolated validation directory')
        self.output = Path(os.environ['PLUS_TEST_DIR'])
        self.before = set(App.listDocuments())
        self.doc = component.new_document('Hierarchy')

    def tearDown(self):
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)

    def hierarchy(self):
        doc = self.doc
        root = component.validate(doc)
        parent = root.Definitions[0]
        child = hierarchy.create_definition(doc, 'Shared child')
        nested = hierarchy.add_instance(parent, child, App.Placement(App.Vector(8, 3, 2), App.Rotation(App.Vector(0,0,1), 20)))
        second = hierarchy.add_instance(root, parent, App.Placement(App.Vector(30, 7, 1), App.Rotation(App.Vector(0,0,1), 40)))
        return root, parent, child, nested, second

    def test_shared_edit_nested_transforms_history_and_persistence(self):
        doc = self.doc
        root, parent, child, nested, second = self.hierarchy()
        first = root.Group[0]
        with component.transaction(doc, 'Parent geometry'):
            own = parent.newObject('Part::Box', 'ParentBox')
            own.Length = 3; own.Width = 3; own.Height = 3
        editing.edit((second, nested))
        sketch = editing.new_sketch(doc)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0,0,1), 2), False)
        doc.recompute()
        pad = editing.pad(doc, sketch, 5)
        self.assertEqual(editing.context_path(doc), (child, (second, nested)))
        view = Gui.activeDocument().activeView()
        self.assertEqual(view.getActiveObject('part', False), (child, root, hierarchy.subname((second, nested))))
        body = pad.getParentGeoFeatureGroup()
        self.assertEqual(view.getActiveObject('pdbody', False), (body, root, hierarchy.subname((second, nested)) + body.Name + '.'))
        self.assertEqual(component.history(doc, parent), [own])
        self.assertEqual(component.history(doc, child), [sketch, pad])
        matrix_equal(self, hierarchy.world_placement(doc, (second, nested)), second.LinkPlacement.multiply(nested.LinkPlacement))
        with component.transaction(doc, 'Shared Pad change'):
            pad.Length = 9
        for top in (first, second):
            shape = root.getSubObject(hierarchy.subname((top,nested)) + pad.getParentGeoFeatureGroup().Name + '.' + pad.Name + '.', 0)
            self.assertAlmostEqual(shape.Volume, 36 * 3.141592653589793)
        old = nested.LinkPlacement
        new = App.Placement(App.Vector(12,5,2), App.Rotation(App.Vector(0,1,0),15))
        hierarchy.move_instance(nested, new)
        for top in (first, second):
            matrix_equal(self, hierarchy.world_placement(doc,(top,nested)), top.LinkPlacement.multiply(new))
        doc.undo(); doc.recompute(); matrix_equal(self, nested.LinkPlacement, old)
        doc.redo(); doc.recompute(); matrix_equal(self, nested.LinkPlacement, new)
        path = component.save_document(doc, self.output/'hierarchy.cadprt')
        expected = dict(uid=str(doc.Uid), identities={o.Name:o.ID for o in doc.Objects},
                        paths=[[first.Name,nested.Name],[second.Name,nested.Name]],
                        placements=[list(hierarchy.world_placement(doc,(top,nested)).toMatrix().A) for top in (first,second)],
                        pad=pad.Name, child=child.Name, parent=parent.Name)
        (self.output/'hierarchy-expected.json').write_text(json.dumps(expected))
        App.closeDocument(doc.Name)
        self.doc=component.open_document(path)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, expected['identities'])
        self.assertEqual(len(component.validate(self.doc).Definitions),2)

    def test_cycle_and_cross_file_preflight_and_rollback(self):
        root,parent,child,nested,second=self.hierarchy()
        before={o.Name for o in self.doc.Objects}; undo=self.doc.UndoCount
        for owner,definition in [(child,parent),(child,child)]:
            with self.assertRaisesRegex(ValueError,'Circular'):
                hierarchy.add_instance(owner,definition)
        self.assertEqual({o.Name for o in self.doc.Objects},before)
        self.assertEqual(self.doc.UndoCount,undo)
        other=component.new_document('Other')
        with self.assertRaises(ValueError): hierarchy.add_instance(parent,component.validate(other).Definitions[0])
        App.setActiveDocument(self.doc.Name)
        with self.assertRaisesRegex(ValueError,'Duplicate component identity'):
            with component.transaction(self.doc,'Invalid catalog'):
                root.Definitions=[parent,child,child]
        self.assertEqual(root.Definitions,[parent,child])
        self.assertEqual({o.Name for o in self.doc.Objects},before)

    def test_occurrence_edit_is_per_view_and_stale_path_is_rejected(self):
        root,parent,child,nested,second=self.hierarchy()
        first=root.Group[0]
        editing.edit((first,nested))
        view=Gui.activeDocument().activeView()
        old=view.getActiveObject('PlusEdit',False)
        Gui.activeDocument().createView('Gui::View3DInventor')
        editing.edit((second,nested))
        self.assertEqual(editing.context_path(self.doc)[1],(second,nested))
        self.assertEqual(view.getActiveObject('PlusEdit',False),old)
        editing.edit_file(self.doc)
        Gui.Selection.addSelection(child)
        with self.assertRaises(ValueError): editing.new_sketch(self.doc)
        Gui.Selection.clearSelection()
        # Bare nested links are ambiguous across repeated parents and must be rejected.
        with self.assertRaises(ValueError): editing.edit(nested)
        editing.edit((second,nested))
        self.doc.undo()  # Remove the second root occurrence.
        with self.assertRaises(ValueError): editing.context_path(self.doc)
        self.doc.redo()
        editing.edit((self.doc.getObject(second.Name),nested))
        self.assertEqual(editing.context_path(self.doc)[0],child)

    def test_explicit_old_schema_upgrade(self):
        root=component.validate(self.doc)
        root.PlusSchema=2
        with self.assertRaisesRegex(ValueError,'explicit upgrade'):
            hierarchy.create_definition(self.doc,'Later')
        hierarchy.upgrade(self.doc)
        self.assertEqual(root.PlusSchema,3)
        self.doc.undo(); self.assertEqual(root.PlusSchema,2)
        self.doc.redo(); self.assertEqual(root.PlusSchema,3)
        hierarchy.create_definition(self.doc,'Later')
        with self.assertRaises(ValueError): hierarchy.create_definition(self.doc,'Later')

    def test_legacy_parts_and_shared_links_keep_frames_geometry_and_identity(self):
        doc=App.newDocument('LegacyAssembly')
        assembly=doc.addObject('App::Part','Assembly')
        assembly.Placement=App.Placement(App.Vector(5,7,9),App.Rotation(App.Vector(0,0,1),20))
        child=doc.addObject('App::Part','Child')
        child.Placement=App.Placement(App.Vector(4,1,0),App.Rotation(App.Vector(0,1,0),15))
        assembly.addObject(child)
        box=child.newObject('Part::Box','Box'); box.Length=2; box.Width=3; box.Height=4
        shared=doc.addObject('App::Link','Shared'); shared.setLink(child)
        shared.LinkTransform=False; shared.LinkPlacement.Base=App.Vector(20,0,0)
        assembly.addObject(shared)
        own=assembly.newObject('Part::Box','OwnGeometry'); own.Placement.Base=App.Vector(-8,0,0)
        repeat=doc.addObject('App::Link','Repeat'); repeat.setLink(assembly)
        repeat.LinkTransform=True; repeat.LinkPlacement=App.Placement(App.Vector(50,0,0),App.Rotation(App.Vector(0,0,1),30))
        doc.recompute()
        original=[assembly.getSubObject('Child.Box.',0), assembly.getSubObject('Shared.Box.',0), repeat.getSubObject('Shared.Box.',0)]
        source=self.output/'assembly.FCStd'; doc.saveAs(str(source))
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        ids={o.Name:o.ID for o in doc.Objects}
        converted,report=convert_file(source,self.output/'assembly.cadprt')
        root=component.validate(converted)
        for name,identity in ids.items(): self.assertEqual(converted.getObject(name).ID,identity)
        self.assertEqual(converted.Shared.LinkedObject,converted.Child)
        matrix_equal(self,converted.Assembly.Placement,assembly.Placement)
        matrix_equal(self,converted.Child.Placement,child.Placement)
        names=report['part_instances']
        paths=[names['Assembly']+'.'+names['Child']+'.Box.',names['Assembly']+'.Shared.Box.','Repeat.Shared.Box.']
        for old,path in zip(original,paths):
            shape=root.getSubObject(path,0)
            self.assertAlmostEqual(old.Volume,shape.Volume)
            self.assertTrue(old.CenterOfMass.isEqual(shape.CenterOfMass,1e-8))
        converted.Box.Length=5; converted.recompute()
        for path in paths: self.assertAlmostEqual(root.getSubObject(path,0).Volume,60)
        component.save_document(converted)
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),digest)
        (self.output/'assembly-expected.json').write_text(json.dumps(dict(paths=paths,ids=ids,source_sha256=digest)))


def verify_fresh_process(output):
    output=Path(output)
    expected=json.loads((output/'hierarchy-expected.json').read_text())
    doc=component.open_document(output/'hierarchy.cadprt')
    assert str(doc.Uid)==expected['uid']
    assert {o.Name:o.ID for o in doc.Objects}==expected['identities']
    root=component.validate(doc)
    for path,matrix in zip(expected['paths'],expected['placements']):
        assert all(abs(a-b)<1e-8 for a,b in zip(hierarchy.world_placement(doc,path).toMatrix().A,matrix))
    pad=doc.getObject(expected['pad'])
    with component.transaction(doc,'Fresh shared edit'): pad.Length=11
    assert pad.Shape.isValid() and abs(pad.Shape.Volume-44*3.141592653589793)<1e-8
    component.save_document(doc,output/'hierarchy-edited.cadprt')
    App.closeDocument(doc.Name)
    legacy=json.loads((output/'assembly-expected.json').read_text())
    doc=component.open_document(output/'assembly.cadprt'); root=component.validate(doc)
    for name,identity in legacy['ids'].items(): assert doc.getObject(name).ID==identity
    doc.Box.Length=7; doc.recompute()
    for path in legacy['paths']: assert abs(root.getSubObject(path,0).Volume-84)<1e-8
    component.save_document(doc,output/'assembly-edited.cadprt')
    assert hashlib.sha256((output/'assembly.FCStd').read_bytes()).hexdigest()==legacy['source_sha256']
    App.closeDocument(doc.Name)
