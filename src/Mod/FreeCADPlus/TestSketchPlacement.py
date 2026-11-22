# SPDX-License-Identifier: LGPL-2.1-or-later
import os
import unittest
from pathlib import Path
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, planes, sketch_placement as placement, sketch_task, modeling, editing, hierarchy, external


class TestSketchPlacement(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Requires an isolated native profile')
        self.before = set(App.listDocuments())
        self.doc = document.new_document('SketchPlacementTest')
        self.owner = document.validate(self.doc).Definitions[0]
        self.xy = next(o for o in self.owner.Origin.OriginFeatures if o.Role == 'XY_Plane')

    def tearDown(self):
        if sketch_task._active:
            sketch_task._active.reject()
        if Gui.Control.activeDialog():
            buttons = [box.button(QtWidgets.QDialogButtonBox.Cancel)
                       for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)]
            for button in buttons:
                if button and button.isVisible():
                    button.click(); QtTest.QTest.qWait(50); break
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit()
        if App.getActiveTransaction():
            App.closeActiveTransaction(True)
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        QtTest.QTest.qWait(50)

    def shape(self, shape):
        obj = self.owner.newObject('Part::Feature', 'Reference')
        obj.Shape = shape
        self.doc.recompute()
        return obj

    def sketch(self, refs=None):
        return placement.save(self.doc, refs or [(self.xy, '')])

    def test_inherited_plane_frame_and_associative_update(self):
        support = self.owner.newObject('PartDesign::Plane', 'Support')
        support.Placement = App.Placement(App.Vector(8, 5, 10), App.Rotation(App.Vector(0, 0, 1), 30))
        self.doc.recompute()
        sketch = self.sketch([(support, '')])
        self.assertEqual(sketch.TypeId, 'Sketcher::SketchObject')
        self.assertTrue(sketch.Placement.isSame(support.Placement, 1e-7))
        self.assertFalse(any(o.TypeId == 'PartDesign::Body' for o in self.doc.Objects))
        support.Placement = App.Placement(App.Vector(3, 7, 12), App.Rotation(App.Vector(1, 2, 3), 43))
        self.doc.recompute()
        self.assertTrue(sketch.Placement.isSame(support.Placement, 1e-7))

    def test_face_defaults_part_local_and_degenerate_projection(self):
        face = self.shape(Part.makePlane(20, 30, App.Vector(8, 9, 6)))
        self.owner.Placement = App.Placement(App.Vector(3, 4, 5), App.Rotation(App.Vector(1, 2, 3), 23))
        self.doc.recompute()
        sketch = self.sketch([(face, 'Face1')])
        self.assertTrue(sketch.Placement.Base.isEqual(App.Vector(0, 0, 6), 1e-7))
        self.assertTrue(sketch.Placement.Rotation.multVec(App.Vector(1, 0, 0)).isEqual(App.Vector(1, 0, 0), 1e-7))
        side = self.shape(Part.makePlane(20, 30, App.Vector(5, 0, 0), App.Vector(1, 0, 0)))
        count = len(self.doc.Objects)
        with self.assertRaisesRegex(ValueError, 'perpendicular'):
            self.sketch([(side, 'Face1')])
        self.assertEqual(count, len(self.doc.Objects))
        edge = self.shape(Part.makeLine(App.Vector(), App.Vector(0, 10, 0)))
        recovered = placement.save(self.doc, [(side, 'Face1')], axis_refs=[(edge, 'Edge1')])
        self.assertAlmostEqual(recovered.Placement.Base.x, 5)

    def test_origin_axis_flip_saved_edit_cancel_and_undo(self):
        point = self.shape(Part.Vertex(App.Vector(4, 5, 9)))
        edge = self.shape(Part.makeLine(App.Vector(), App.Vector(0, 10, 0)))
        sketch = placement.save(self.doc, [(self.xy, '')], [(point, 'Vertex1')], [(edge, 'Edge1')], 'Y', True)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2), False)
        self.doc.recompute()
        initial = sketch.Placement
        count, undo = len(self.doc.Objects), self.doc.UndoCount
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(sketch)
        Gui.runCommand('Sketcher_ReorientSketch'); QtTest.QTest.qWait(100)
        task = sketch_task._active
        self.assertIsInstance(task, sketch_task.SketchPlacementTask)
        self.assertEqual(task.feature, sketch)
        self.assertEqual(task.origin_refs, [(point, 'Vertex1')])
        self.assertTrue(task.y_choice.isChecked()); self.assertTrue(task.flip.isChecked())
        task.clear_origin(); task.clear_axis(); task.flip.setChecked(False)
        task.reject()
        self.assertTrue(sketch.Placement.isSame(initial, 1e-7))
        self.assertEqual((len(self.doc.Objects), self.doc.UndoCount), (count, undo))
        task = sketch_task.show(sketch)
        task.clear_origin(); task.clear_axis(); task.flip.setChecked(False)
        self.assertTrue(task.accept())
        self.assertEqual(task.result, sketch); self.assertEqual(sketch.GeometryCount, 1)
        self.assertEqual(count, len(self.doc.Objects))
        self.assertTrue(sketch.Placement.isSame(App.Placement(), 1e-7))
        self.doc.undo(); self.doc.recompute()
        self.assertTrue(sketch.Placement.isSame(initial, 1e-7))
        self.doc.redo(); self.doc.recompute()
        self.assertTrue(sketch.Placement.isSame(App.Placement(), 1e-7))

    def test_native_command_preselection_cancel_and_drawing(self):
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(self.xy)
        count, undo = len(self.doc.Objects), self.doc.UndoCount
        Gui.runCommand('Sketcher_NewSketch'); QtTest.QTest.qWait(80)
        task = sketch_task._active
        self.assertEqual(task.refs, [(self.xy, '')])
        self.assertEqual(task.origin_ref.text(), self.xy.Label + ' origin')
        task.reject()
        self.assertEqual((len(self.doc.Objects), self.doc.UndoCount), (count, undo))
        task = sketch_task.show(); task.choose('XY Plane')
        QtTest.QTest.qWait(80)
        task.automatic.setChecked(False)
        task.offset.setFocus(); task.offset.selectAll(); QtTest.QTest.keyClicks(task.offset,'4')
        button = next(box.button(QtWidgets.QDialogButtonBox.Ok)
                      for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)
                      if box.button(QtWidgets.QDialogButtonBox.Ok) and box.isVisible())
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(150)
        self.assertTrue(task.closed)
        sketch = task.result
        self.assertEqual(sketch.SketchPlaneOffset.Value,4)
        self.assertAlmostEqual(sketch.Placement.Base.z,4)
        self.assertEqual(Gui.activeDocument().getInEdit().Object, sketch)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2), False)
        Gui.activeDocument().resetEdit(); App.closeActiveTransaction()
        self.doc.recompute()
        self.assertFalse(any(o.TypeId == 'PartDesign::Body' for o in self.doc.Objects))
        name = sketch.Name
        self.doc.undo(); self.assertIsNone(self.doc.getObject(name))
        self.doc.redo(); self.assertTrue(placement.is_managed(self.doc.getObject(name)))
        self.assertEqual(self.doc.getObject(name).SketchPlaneOffset.Value,4)

    def test_attachment_editor_and_partdesign_entry_share_task(self):
        Gui.Selection.clearSelection()
        Gui.runCommand('PartDesign_NewSketch'); QtTest.QTest.qWait(80)
        self.assertIsInstance(sketch_task._active, sketch_task.SketchPlacementTask)
        sketch_task._active.reject()
        sketch = self.sketch()
        from AttachmentEditor import Commands
        task = Commands.editAttachment(sketch)
        self.assertIsInstance(task, sketch_task.SketchPlacementTask)
        self.assertEqual(task.feature, sketch)
        task.reject()
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(sketch)
        Gui.runCommand('Sketcher_MapSketch'); QtTest.QTest.qWait(80)
        self.assertEqual(sketch_task._active.feature, sketch)
        sketch_task._active.reject()

    def test_picking_two_points_and_clear_defaults(self):
        a = self.shape(Part.Vertex(App.Vector(4, 5, 8)))
        b = self.shape(Part.Vertex(App.Vector(4, 15, 8)))
        task = sketch_task.show(); task.choose('XY Plane')
        task.frame.header.setChecked(True)
        task.origin_ref.setFocus(); QtTest.QTest.qWait(50)
        Gui.Selection.addSelection(a, 'Vertex1')
        self.assertEqual(task.origin_refs, [(a, 'Vertex1')])
        task.axis_ref.setFocus(); QtTest.QTest.qWait(50)
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(a, 'Vertex1'); Gui.Selection.addSelection(b, 'Vertex1')
        task.y_choice.setChecked(True); task.flip.setChecked(True)
        self.assertTrue(task.valid, task.status.text())
        self.assertTrue(task.placement().Base.isEqual(App.Vector(4, 5, 0), 1e-7))
        self.assertTrue(task.placement().Rotation.multVec(App.Vector(0, 1, 0)).isEqual(App.Vector(0, 1, 0), 1e-7))
        task.clear_origin(); task.clear_axis(); task.flip.setChecked(False)
        self.assertTrue(task.placement().isSame(App.Placement(), 1e-7))
        task.reject()

    def test_placement_property_opens_shared_task(self):
        sketch = self.sketch()
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(sketch)
        QtTest.QTest.qWait(150)
        tabs = Gui.getMainWindow().findChild(QtWidgets.QTabWidget, 'propertyTab')
        if tabs: tabs.setCurrentIndex(1)
        tree = Gui.getMainWindow().findChild(QtWidgets.QTreeView, 'propertyEditorData')
        self.assertIsNotNone(tree)
        model = tree.model()
        def find(parent=QtCore.QModelIndex()):
            for row in range(model.rowCount(parent)):
                index = model.index(row, 0, parent)
                if model.data(index) == 'Placement': return index
                found = find(index)
                if found is not None: return found
            return None
        index = find(); self.assertIsNotNone(index)
        value = index.siblingAtColumn(1)
        tree.expand(index.parent()); tree.scrollTo(value); tree.setCurrentIndex(value); tree.edit(value)
        QtTest.QTest.qWait(100)
        editor = next(w for w in tree.findChildren(QtWidgets.QWidget)
                      if w.metaObject().className().endswith('PlacementEditor'))
        button = editor.findChild(QtWidgets.QAbstractButton)
        self.assertIsNotNone(button)
        QtTest.QTest.mouseClick(button, QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(100)
        self.assertIsInstance(sketch_task._active, sketch_task.SketchPlacementTask)
        self.assertEqual(sketch_task._active.feature, sketch)
        sketch_task._active.reject()

    def test_external_placement_edit_is_source_owned(self):
        folder = Path(os.environ['PLUS_TEST_DIR'])
        document.save_document(self.doc, folder / 'SketchAssembly.cadprt')
        source = document.new_document('SketchSource')
        definition = document.validate(source).Definitions[0]
        xy = next(o for o in definition.Origin.OriginFeatures if o.Role == 'XY_Plane')
        support = planes.save(source, [(xy, '')], 7)
        document.save_document(source, folder / 'SketchSource.cadprt')
        external.import_file(self.doc, source)
        App.setActiveDocument(self.doc.Name)
        editing.edit_unused(self.doc, definition)
        assembly_ids = {o.Name: o.ID for o in self.doc.Objects}
        sketch = placement.save(self.doc, [(support, '')])
        self.assertEqual(sketch.Document, source)
        task = sketch_task.show(sketch); task.flip.setChecked(True)
        task.offset.setValue(3)
        self.assertTrue(task.accept())
        self.assertTrue(sketch.FlipNormal)
        self.assertAlmostEqual(sketch.Placement.Base.z,10)
        source.undo(); source.recompute(); self.assertFalse(sketch.FlipNormal)
        self.assertEqual(sketch.SketchPlaneOffset.Value,0)
        source.redo(); source.recompute(); self.assertTrue(sketch.FlipNormal)
        self.assertEqual(sketch.SketchPlaneOffset.Value,3)
        self.assertEqual({o.Name: o.ID for o in self.doc.Objects}, assembly_ids)
        document.save_document(source); document.save_document(self.doc)

    def test_target_body_frame_after_add(self):
        base_sketch = modeling.new_sketch(self.doc)
        base_sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 3), False)
        self.doc.recompute()
        base = modeling.extrude_new_solid(self.doc, base_sketch, 5)
        body = base.getParentGeoFeatureGroup()
        body.Placement = App.Placement(App.Vector(2, 0, 0), App.Rotation(App.Vector(0, 0, 1), 20))
        self.doc.recompute()
        support = planes.save(self.doc, [(self.xy, '')], 5)
        sketch = placement.save(self.doc, [(support, '')], offset=-2)
        sketch.addGeometry(Part.Circle(App.Vector(2, 0, 0), App.Vector(0, 0, 1), 2), False)
        self.doc.recompute()
        expected = sketch.getGlobalPlacement()
        result = modeling.extrude(self.doc, sketch, 3, operation='add', target=base)
        self.assertTrue(result.Shape.isValid())
        self.assertTrue(sketch.getGlobalPlacement().isSame(expected, 1e-7))
        self.assertEqual(sketch.getParentGeoFeatureGroup(), body)

    def test_downstream_extrude_recompute_and_cycle_rejection(self):
        support = planes.save(self.doc, [(self.xy, '')], 5)
        sketch = placement.save(self.doc, [(support, '')], offset=2)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2), False)
        self.doc.recompute()
        pad = modeling.extrude_new_solid(self.doc, sketch, 10)
        self.assertAlmostEqual(pad.Shape.BoundBox.ZMin, 7)
        support.Offset = 12; self.doc.recompute()
        self.assertAlmostEqual(pad.Shape.BoundBox.ZMin, 14)
        with self.assertRaisesRegex(ValueError, 'downstream'):
            placement.save(self.doc, [(pad, 'Face1')], feature=sketch)
        task = sketch_task.show(sketch)
        self.assertTrue(task.valid, task.status.text()); task.reject()
        document.save_document(self.doc, Path(os.environ['PLUS_TEST_DIR']) / 'SketchPlacement.cadprt')

    def test_missing_ambiguous_and_foreign_refs_are_atomic(self):
        task = sketch_task.show()
        self.assertFalse(task.valid)
        task.refs = [(self.xy, ''), (next(o for o in self.owner.Origin.OriginFeatures if o.Role == 'XZ_Plane'), '')]
        task.update(); self.assertFalse(task.valid); task.reject()
        sketch = self.sketch()
        with self.assertRaisesRegex(ValueError, 'itself'):
            placement.save(self.doc, [(sketch, '')], feature=sketch)
        other = document.new_document('Other')
        foreign = document.validate(other).Definitions[0].Origin.OriginFeatures[0]
        Gui.activeDocument().activeView()
        App.setActiveDocument(self.doc.Name)
        with self.assertRaises(ValueError):
            placement.save(self.doc, [(foreign, '')], feature=sketch)

    def test_signed_offset_face_point_override_and_flip(self):
        face = self.shape(Part.makePlane(20,30,App.Vector(8,9,6)))
        point = self.shape(Part.Vertex(App.Vector(4,5,20)))
        for offset in (0,5,-3):
            for flipped in (False,True):
                with self.subTest(offset=offset,flipped=flipped):
                    result = placement.solve(self.owner,[(face,'Face1')],[(point,'Vertex1')],
                                             flipped=flipped,offset=offset)
                    self.assertTrue(result.Base.isEqual(App.Vector(4,5,6+offset),1e-7))
                    self.assertAlmostEqual(result.Rotation.multVec(App.Vector(0,0,1)).z,-1 if flipped else 1)
        before = (len(self.doc.Objects),self.doc.UndoCount)
        for offset in (float('nan'),float('inf'),float('-inf')):
            with self.assertRaisesRegex(ValueError,'finite'):
                placement.save(self.doc,[(face,'Face1')],offset=offset)
        self.assertEqual((len(self.doc.Objects),self.doc.UndoCount),before)

    def test_offset_follows_rotated_plane_and_component(self):
        support = self.owner.newObject('PartDesign::Plane','Support')
        support.Placement = App.Placement(App.Vector(3,7,12),App.Rotation(App.Vector(1,2,3),43))
        self.doc.recompute()
        sketch = placement.save(self.doc,[(support,'')],offset=5)
        for angle in (20,70):
            self.owner.Placement = App.Placement(App.Vector(12,8,6),App.Rotation(App.Vector(1,2,1),angle))
            support.Placement = App.Placement(App.Vector(2,9,11),App.Rotation(App.Vector(2,1,3),angle))
            self.doc.recompute()
            expected = support.getGlobalPlacement()
            expected.Base += expected.Rotation.multVec(App.Vector(0,0,5))
            self.assertTrue(sketch.getGlobalPlacement().isSame(expected,1e-7))

    def test_offset_task_defers_typing_and_edits_same_sketch(self):
        sketch = placement.save(self.doc,[(self.xy,'')],offset=2)
        sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2),False)
        self.doc.recompute()
        identity, undo = sketch.ID,self.doc.UndoCount
        task = sketch_task.show(sketch); QtTest.QTest.qWait(80)
        self.assertFalse(task.offset.isHidden())
        self.assertEqual(task.offset.value(),2)
        task.offset.setFocus();task.offset.selectAll();revision=task.revisions
        QtTest.QTest.keyClicks(task.offset,'5');QtTest.QTest.qWait(60)
        self.assertEqual(task.revisions,revision)
        task.references.setFocus();QtTest.QTest.qWait(60)
        self.assertEqual(task.revisions,revision+1)
        self.assertEqual(task.preview_offset,5)
        task.reverse_offset();self.assertEqual(task.preview_offset,-5)
        task.flip.click();self.assertAlmostEqual(task.placement().Base.z,-5)
        task.reject()
        self.assertEqual(sketch.SketchPlaneOffset.Value,2)
        self.assertEqual(self.doc.UndoCount,undo)
        task = sketch_task.show(sketch)
        task.automatic.setChecked(False)
        task.offset.setValue(-5);task.numeric_left()
        self.assertEqual(task.preview_offset,2)
        self.assertTrue(task.accept())
        self.assertEqual((sketch.ID,sketch.GeometryCount),(identity,1))
        self.assertEqual(sketch.SketchPlaneOffset.Value,-5)
        self.doc.undo();self.doc.recompute();self.assertEqual(sketch.SketchPlaneOffset.Value,2)
        self.doc.redo();self.doc.recompute();self.assertEqual(sketch.SketchPlaneOffset.Value,-5)
        task=sketch_task.show(sketch);self.assertEqual(task.offset.value(),-5);task.reject()

    def test_old_managed_sketch_defaults_without_migration_on_cancel(self):
        sketch = self.sketch()
        sketch.removeProperty('SketchPlaneOffset');sketch.touch();self.doc.recompute()
        before = (tuple(sketch.PropertiesList),self.doc.UndoCount)
        self.assertEqual(placement.saved_offset(sketch),0)
        task=sketch_task.show(sketch);self.assertEqual(task.offset.value(),0)
        task.offset.setValue(5);task.reject()
        self.assertEqual((tuple(sketch.PropertiesList),self.doc.UndoCount),before)
        task=sketch_task.show(sketch);task.offset.setValue(5);self.assertTrue(task.accept())
        self.assertEqual(sketch.SketchPlaneOffset.Value,5)
        self.doc.undo();self.doc.recompute();self.assertNotIn('SketchPlaneOffset',sketch.PropertiesList)
        self.doc.redo();self.doc.recompute();self.assertEqual(sketch.SketchPlaneOffset.Value,5)
