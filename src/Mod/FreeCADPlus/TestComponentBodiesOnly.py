# SPDX-License-Identifier: LGPL-2.1-or-later
"""Bodies Only: real native picking, shared contexts and persisted authored state."""
import json
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtTest, QtWidgets, QtOpenGLWidgets
from freecad_plus import document, display, editing, hierarchy, panel, isolation
import TestComponentPanel as fixtures
from TestUnusedModels import visibility, TestUnusedModels

settle = fixtures.settle


def content(owner):
    doc = owner.Document
    wire = doc.addObject('Part::Feature', 'DisplayCurve')
    wire.Shape = Part.makeLine(App.Vector(8, -2, 1), App.Vector(8, 2, 1))
    owner.addObject(wire)
    face = doc.addObject('Part::Feature', 'DisplaySheet')
    face.Shape = Part.makePlane(2, 2, App.Vector(12, 0, 1))
    owner.addObject(face)
    solid = doc.addObject('Part::Feature', 'DisplaySolid')
    solid.Shape = Part.makeBox(2, 2, 2, App.Vector(16, 0, 0))
    owner.addObject(solid)
    doc.recompute()
    return wire, face, solid


def hit(view, x, y=0):
    return view.getObjectInfoRay(App.Vector(x, y, 30), App.Vector(0, 0, -1))


class TestComponentBodiesOnly(unittest.TestCase):
    def setUp(self):
        fixtures.TestComponentPanel.setUp(self)
        main = Gui.getMainWindow()
        main.hide(); main.showNormal(); QtTest.QTest.qWait(200)
    tearDown = fixtures.TestComponentPanel.tearDown
    rows = fixtures.TestComponentPanel.rows
    occurrence = fixtures.TestComponentPanel.occurrence
    external_fixture = TestUnusedModels.external_fixture

    def test_shared_body_history_and_full_override(self):
        wire, face, solid = content(self.child)
        body = self.pad.getParentGeoFeatureGroup()
        sketch = self.doc.addObject('Sketcher::SketchObject', 'VisibleHistorySketch')
        body.addObject(sketch)
        sketch.addGeometry(Part.LineSegment(App.Vector(5, -2, 1), App.Vector(5, 2, 1)), False)
        body.Tip = self.pad
        self.doc.recompute(); sketch.Visibility = True
        editing.edit((self.first, self.nested)); settle()
        view = Gui.activeDocument().activeView()
        ids = {o.Name: o.ID for o in self.doc.Objects}; vis = visibility(self.doc)
        self.assertIsNotNone(hit(view, 8)); self.assertIsNotNone(hit(view, 5))
        self.assertIsNone(hit(view, 33)); self.assertIsNone(hit(view, 30))
        display.set_state(self.child, part_type='Bodies Only'); settle()
        for x in (5, 8, 30, 33): self.assertIsNone(hit(view, x))
        for x in (.3, 12.3, 16.3, 25.3, 37.3, 41.3):
            self.assertIsNotNone(hit(view, x, .3))
        self.doc.undo(); self.doc.recompute(); settle()
        self.assertIsNotNone(hit(view, 8)); self.assertIsNotNone(hit(view, 5))
        other = self.widget.open_row(self.occurrence((self.second, self.nested)).data(0, panel._ROLE)); settle()
        self.assertIsNotNone(hit(other, 33)); self.assertIsNone(hit(other, 8))
        self.assertIsNotNone(hit(view, 8)); self.assertIsNone(hit(view, 33))
        # An explicit nested Full Component choice survives a Bodies Only parent.
        display.set_state(self.parent, self.nested, part_type='Full Component')
        editing.edit_file(self.doc); settle()
        for x in (5, 8, 30, 33): self.assertIsNotNone(hit(other, x))
        self.pad.Length = 7; self.doc.recompute(); settle()
        self.assertIsNotNone(hit(other, .3, .3))
        self.assertEqual(body.Tip, self.pad)
        self.assertEqual(visibility(self.doc), vis)
        self.assertEqual({o.Name: o.ID for o in self.doc.Objects}, ids)
        self.assertEqual(self.widget.message.text(), '')

    def test_bodies_only_native_sketch_editor(self):
        editing.edit((self.first, self.nested))
        display.set_state(self.child, part_type='Bodies Only'); settle()
        gui = Gui.getDocument(self.doc.Name)
        path = hierarchy.subname((self.first, self.nested))
        body = self.pad.getParentGeoFeatureGroup()
        self.assertTrue(gui.setEdit(self.root, 0, path + body.Name + '.' + self.sketch.Name + '.'))
        try:
            settle()
            self.assertEqual(gui.getInEdit().Object, self.sketch)
            self.assertEqual(self.widget.message.text(), '')
        finally:
            gui.resetEdit(); settle()
        self.assertEqual(editing.context_path(self.doc), (self.child, (self.first, self.nested)))
        self.assertTrue(self.pad.Shape.isValid())
        self.assertEqual(self.widget.message.text(), '')

    def test_persistence_native_visibility_and_cleanup(self):
        wire, face, solid = content(self.child)
        editing.edit((self.first, self.nested)); settle()
        display.set_state(self.child, part_type='Bodies Only'); settle()
        view = Gui.activeDocument().activeView()
        self.assertIsNone(hit(view, 8)); self.assertIsNotNone(hit(view, 16.3, .3))
        vis = visibility(self.doc); ids = {o.Name:o.ID for o in self.doc.Objects}
        document.save_document(self.doc, self.output/'Bodies.cadprt'); settle()
        expected = {'ids':ids, 'visibility':vis, 'child':self.child.Name,
                    'first':self.first.Name, 'nested':self.nested.Name}
        (self.output/'expected.json').write_text(json.dumps(expected))
        count = self.widget.refresh_count
        QtTest.QTest.qWait(250); self.assertEqual(self.widget.refresh_count, count)
        self.widget.close(); settle()
        self.assertIsNotNone(hit(view, 8)); self.assertIsNotNone(hit(view, 33))
        self.assertEqual(visibility(self.doc), vis)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, ids)

    def test_unused_self_nested_and_undo(self):
        content(self.unused)
        child = hierarchy.add_instance(self.unused, self.child,
            App.Placement(App.Vector(25, 0, 0), App.Rotation()))
        content(self.child)
        editing.edit_unused(self.doc, self.unused); settle()
        view = Gui.activeDocument().activeView(); vis = visibility(self.doc)
        self.assertIsNotNone(hit(view, 8)); self.assertIsNone(hit(view, 33))
        self.assertIsNotNone(hit(view, 25.3, .3))
        display.set_state(self.unused, part_type='Bodies Only'); settle()
        self.assertIsNone(hit(view, 8)); self.assertIsNone(hit(view, 33))
        for x in (12.3, 16.3, 25.3, 37.3, 41.3): self.assertIsNotNone(hit(view, x, .3))
        self.doc.undo(); self.doc.recompute(); settle()
        self.assertIsNotNone(hit(view, 8))
        display.set_state(self.unused, child, part_type='Excluded'); settle()
        self.assertIsNone(hit(view, 25.3, .3))
        display.set_state(self.unused, child, part_type='Reference'); settle()
        self.assertIsNotNone(hit(view, 33))
        self.assertEqual(visibility(self.doc), vis)
        self.assertIsNotNone(isolation.current(view))
        self.assertEqual(self.widget.message.text(), '')

    def test_external_unused_source_owned_filter(self):
        source, definition = self.external_fixture()
        content(definition)
        editing.edit_unused(self.doc, definition); settle()
        view = Gui.activeDocument().activeView(); vis = visibility(source)
        ids = {o.Name:o.ID for o in self.doc.Objects}
        self.assertIsNotNone(hit(view, 8))
        display.set_state(definition, part_type='Bodies Only'); settle()
        self.assertIsNone(hit(view, 8)); self.assertIsNotNone(hit(view, 16.3, .3))
        source.undo(); source.recompute(); settle()
        self.assertIsNotNone(hit(view, 8))
        source.redo(); source.recompute(); settle()
        self.assertIsNone(hit(view, 8))
        self.assertEqual(visibility(source), vis)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, ids)
        self.assertFalse(any('PlusSelfPartType' in o.PropertiesList for o in self.doc.Objects))
        self.assertIsNotNone(isolation.current(view))
        self.assertEqual(self.widget.message.text(), '')


def verify_fresh_process(output):
    folder = Path(output)/'test_persistence_native_visibility_and_cleanup'
    expected = json.loads((folder/'expected.json').read_text())
    doc = document.open_document(folder/'Bodies.cadprt')
    widget = panel.show_panel()
    try:
        assert {o.Name:o.ID for o in doc.Objects} == expected['ids']
        assert visibility(doc) == expected['visibility']
        editing.edit((doc.getObject(expected['first']), doc.getObject(expected['nested'])))
        settle(); view = Gui.activeDocument().activeView()
        assert hit(view, 8) is None and hit(view, 33) is None
        for x in (.3, 12.3, 16.3, 25.3): assert hit(view, x, .3) is not None
        # Inspect normal framebuffer images from the same settled view; no special grab.
        from TestComponentFading import capture
        view.setAnimationEnabled(False); view.viewTop(); view.fitAll()
        Gui.getMainWindow().hide(); Gui.getMainWindow().showNormal(); QtTest.QTest.qWait(200)
        capture(view, folder/'bodies_only.png')
        display.set_state(doc.getObject(expected['child']), part_type='Full Component'); settle()
        assert hit(view, 8) is not None and hit(view, 33) is None
        capture(view, folder/'full_component.png')
        assert visibility(doc) == expected['visibility']
    finally:
        widget.close(); settle(); App.closeDocument(doc.Name)
