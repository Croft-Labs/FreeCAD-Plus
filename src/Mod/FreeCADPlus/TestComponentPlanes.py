# SPDX-License-Identifier: LGPL-2.1-or-later
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, planes, plane_task, modeling, editing, numeric_fields, external, hierarchy


class TestComponentPlanes(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ: self.skipTest('Requires an isolated native profile')
        self.before = set(App.listDocuments())
        self.doc = document.new_document('PlaneTest')
        self.owner = document.validate(self.doc).Definitions[0]
        self.xy = next(obj for obj in self.owner.Origin.OriginFeatures if obj.Role == 'XY_Plane')

    def tearDown(self):
        if plane_task._active: plane_task._active.reject()
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments())-self.before: App.closeDocument(name)
        QtTest.QTest.qWait(50)

    def feature(self, shape):
        obj = self.owner.newObject('Part::Feature','Reference')
        obj.Shape = shape
        self.doc.recompute()
        return obj

    def test_create_undo_recompute_save(self):
        before = len(self.doc.Objects)
        plane = planes.save(self.doc, [(self.xy,'')], 10)
        self.assertEqual(plane.getParentGeoFeatureGroup(),self.owner)
        self.assertEqual(len(self.doc.Objects), before+1)
        self.assertFalse(any(o.TypeId == 'PartDesign::Body' for o in self.doc.Objects))
        self.assertAlmostEqual(plane.Placement.Base.z,10)
        name = plane.Name
        self.doc.undo(); self.doc.recompute(); self.assertIsNone(self.doc.getObject(name))
        self.doc.redo(); self.doc.recompute(); plane = self.doc.getObject(name)
        plane.Offset = 15; self.doc.recompute()
        self.assertAlmostEqual(plane.Shape.BoundBox.ZMin,15)
        document.save_document(self.doc,Path(os.environ['PLUS_TEST_DIR'])/'Plane.cadprt')

    def test_three_points_and_reference_updates(self):
        points = [self.feature(Part.Vertex(App.Vector(*v))) for v in [(0,0,3),(10,0,3),(0,10,3)]]
        plane = planes.save(self.doc,[(o,'Vertex1') for o in points])
        self.assertAlmostEqual(plane.Placement.Base.z,3)
        for point in points: point.Placement.Base.z = 4
        self.doc.recompute(); self.assertAlmostEqual(plane.Placement.Base.z,7)

    def test_axis_origin_flip_and_clear(self):
        point = self.feature(Part.Vertex(App.Vector(5,6,22)))
        edge = self.feature(Part.makeLine(App.Vector(),App.Vector(0,10,0)))
        p = planes.save(self.doc,[(self.xy,'')],10,[(point,'Vertex1')],[(edge,'Edge1')],'Y')
        self.assertTrue(p.Placement.Base.isEqual(App.Vector(5,6,10),1e-7))
        y = p.Placement.Rotation.multVec(App.Vector(0,1,0))
        old = p.Placement.Base
        planes.save(self.doc,[(self.xy,'')],10,[(point,'Vertex1')],[(edge,'Edge1')],'Y',True,p)
        self.assertTrue(p.Placement.Base.isEqual(old,1e-7))
        self.assertTrue(p.Placement.Rotation.multVec(App.Vector(0,1,0)).isEqual(y,1e-7))
        self.assertAlmostEqual(p.Placement.Rotation.multVec(App.Vector(0,0,1)).z,-1)
        planes.save(self.doc,[(self.xy,'')],10,feature=p)
        self.assertTrue(p.Placement.Base.isEqual(App.Vector(0,0,10),1e-7))

    def test_reject_degenerate_and_cycles(self):
        a = self.feature(Part.makeLine(App.Vector(),App.Vector(1,0,0)))
        b = self.feature(Part.makeLine(App.Vector(0,0,1),App.Vector(0,1,1)))
        before = len(self.doc.Objects)
        with self.assertRaises(ValueError): planes.save(self.doc,[(a,'Edge1'),(b,'Edge1')])
        with self.assertRaises(ValueError): planes.save(self.doc,[(self.xy,'')],float('nan'))
        self.assertEqual(before,len(self.doc.Objects))
        p = planes.save(self.doc,[(self.xy,'')])
        with self.assertRaises(ValueError): planes.save(self.doc,[(p,'Face1')],feature=p)

    def test_cancel_and_deferred_numeric_task(self):
        before = (len(self.doc.Objects),self.doc.UndoCount)
        task = plane_task.show(); task.choose('XY Plane')
        QtTest.QTest.qWait(100)
        task.offset.setFocus(); QtTest.QTest.qWait(100); task.offset.selectAll()
        revision = task.revisions
        QtTest.QTest.keyClicks(task.offset,'12.5'); QtTest.QTest.qWait(80)
        self.assertEqual(task.revisions,revision)
        task.references.setFocus(); QtTest.QTest.qWait(50)
        self.assertEqual(task.revisions,revision+1)
        self.assertEqual(task.preview_offset,12.5)
        task.automatic.setChecked(False)
        task.offset.setFocus(); task.offset.selectAll(); QtTest.QTest.keyClicks(task.offset,'20')
        revision = task.revisions
        task.references.setFocus(); QtTest.QTest.qWait(50)
        self.assertEqual(task.revisions,revision)
        task.reject(); self.assertEqual((len(self.doc.Objects),self.doc.UndoCount),before)

    def test_real_picking_and_accept(self):
        point = self.feature(Part.Vertex(App.Vector(8,9,0)))
        edge = self.feature(Part.makeLine(App.Vector(),App.Vector(0,10,0)))
        task = plane_task.show(); task.choose('XY Plane')
        task.frame.header.setChecked(True)
        task.origin_ref.setFocus(); QtTest.QTest.qWait(50)
        Gui.Selection.addSelection(point,'Vertex1')
        self.assertEqual(task.origin_refs,[(point,'Vertex1')])
        task.axis_ref.setFocus(); QtTest.QTest.qWait(50)
        Gui.Selection.addSelection(edge,'Edge1')
        self.assertEqual(task.axis_refs,[(edge,'Edge1')])
        task.flip.click(); self.assertTrue(task.accept())
        self.assertTrue(task.result.Placement.Base.isEqual(App.Vector(8,9,0),1e-7))
        editing.edit_feature(self.doc,task.result)
        self.assertIsNotNone(plane_task._active)
        plane_task._active.reject()

    def test_attached_sketch_recomputes_with_plane(self):
        plane = planes.save(self.doc,[(self.xy,'')],5)
        sketch = modeling.new_sketch(self.doc)
        sketch.AttachmentSupport = (plane,['Face1'])
        sketch.MapMode = 'FlatFace'
        sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2),False)
        self.doc.recompute()
        old = sketch.Placement.Base.z
        plane.Offset = 12; self.doc.recompute()
        self.assertAlmostEqual(sketch.Placement.Base.z-old,7)
        document.save_document(self.doc,Path(os.environ['PLUS_TEST_DIR'])/'AttachedPlane.cadprt')

    def test_edit_reuses_create_task_and_preserves_feature_identity(self):
        point = self.feature(Part.Vertex(App.Vector(5,6,0)))
        edge = self.feature(Part.makeLine(App.Vector(),App.Vector(0,10,0)))
        plane = planes.save(self.doc,[(self.xy,'')],7,[(point,'Vertex1')],[(edge,'Edge1')],'Y',True)
        name, identity = plane.Name, plane.ID
        before = ({obj.Name:obj.ID for obj in self.doc.Objects},self.doc.UndoCount)
        # History Edit and the native tree double-click share the creation task.
        for open_editor in (lambda: editing.edit_feature(self.doc,plane),
                            lambda: plane.ViewObject.Proxy.doubleClicked(plane.ViewObject)):
            open_editor()
            task = plane_task._active
            self.assertIs(type(task),plane_task.PlaneTask)
            self.assertEqual(task.feature,plane)
            self.assertEqual(task.refs,[(self.xy,'')])
            self.assertEqual(task.origin_refs,[(point,'Vertex1')])
            self.assertEqual(task.axis_refs,[(edge,'Edge1')])
            self.assertEqual(task.offset.value(),7)
            self.assertTrue(task.y_choice.isChecked())
            self.assertTrue(task.flip.isChecked())
            task.offset.setValue(11);task.numeric_left()
            self.assertEqual(plane.Offset.Value,7)
            task.reject()
            self.assertEqual(({obj.Name:obj.ID for obj in self.doc.Objects},self.doc.UndoCount),before)
        editing.edit_feature(self.doc,plane)
        task=plane_task._active
        task.offset.setValue(13)
        self.assertTrue(task.accept())
        self.assertEqual(task.result,plane)
        self.assertEqual((plane.Name,plane.ID),(name,identity))
        self.assertEqual({obj.Name:obj.ID for obj in self.doc.Objects},before[0])
        self.assertEqual(plane.Offset.Value,13)
        self.assertEqual(self.doc.UndoCount,before[1]+1)
        self.doc.undo();self.doc.recompute()
        self.assertEqual(self.doc.getObject(name).Offset.Value,7)
        self.doc.redo();self.doc.recompute()
        self.assertEqual(self.doc.getObject(name).Offset.Value,13)

    def test_planar_face_line_point_two_lines(self):
        face = self.feature(Part.makePlane(10,10,App.Vector(0,0,4)))
        p = planes.save(self.doc,[(face,'Face1')])
        self.assertAlmostEqual(p.Placement.Base.z,4)
        line = self.feature(Part.makeLine(App.Vector(0,0,2),App.Vector(10,0,2)))
        point = self.feature(Part.Vertex(App.Vector(0,10,2)))
        p = planes.save(self.doc,[(line,'Edge1'),(point,'Vertex1')])
        self.assertAlmostEqual(p.Placement.Base.z,2)
        parallel = self.feature(Part.makeLine(App.Vector(0,10,2),App.Vector(10,10,2)))
        p = planes.save(self.doc,[(line,'Edge1'),(parallel,'Edge1')])
        self.assertAlmostEqual(p.Placement.Base.z,2)

    def test_command_opens_component_task_without_body(self):
        Gui.runCommand('PartDesign_Plane')
        self.assertIsNotNone(plane_task._active)
        self.assertFalse(any(obj.TypeId == 'PartDesign::Body' for obj in self.doc.Objects))
        plane_task._active.choose('XZ Plane')
        self.assertTrue(plane_task._active.valid,plane_task._active.status.text())
        plane_task._active.reject()

    def test_external_source_and_occurrence_guards(self):
        folder = Path(os.environ['PLUS_TEST_DIR'])
        document.save_document(self.doc,folder/'PlaneAssembly.cadprt')
        source = document.new_document('PlaneSource')
        owner = document.validate(source).Definitions[0]
        document.save_document(source,folder/'PlaneSource.cadprt')
        external.import_file(self.doc,source)
        root = document.validate(self.doc)
        occurrence = hierarchy.add_instance(root,owner,App.Placement(App.Vector(30,0,5),App.Rotation()))
        App.setActiveDocument(self.doc.Name)
        editing.edit((occurrence,))
        xy = next(obj for obj in owner.Origin.OriginFeatures if obj.Role == 'XY_Plane')
        route = hierarchy.subname((occurrence,))+owner.Origin.Name+'.'+xy.Name+'.'
        before = len(self.doc.Objects)
        p = planes.save(self.doc,[(root,route)],8)
        self.assertEqual(p.Document,source)
        self.assertEqual(len(self.doc.Objects),before)
        self.assertAlmostEqual(p.Placement.Base.z,8)
        # Preserve occurrence paths while consuming preselection and subsequent picks.
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(root,route)
        task = plane_task.show()
        self.assertEqual(task.refs,[(xy,'')])
        self.assertFalse(Gui.Selection.getSelection())
        Gui.Selection.addSelection(root,route)
        self.assertEqual(task.refs,[])
        task.reject()
        task = plane_task.show(p); task.reverse_axis.click()
        self.assertTrue(task.accept())
        self.assertTrue(p.ReverseAxis)
        document.save_document(source,folder/'PlaneSource.cadprt')
        document.save_document(self.doc,folder/'PlaneAssembly.cadprt')
        # A raw foreign definition is not an admitted modeling reference.
        with self.assertRaises(ValueError): planes.save(self.doc,[(self.xy,'')])

    def test_body_face_transforms_and_two_point_axis(self):
        sketch = modeling.new_sketch(self.doc)
        sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2),False)
        self.doc.recompute()
        pad = modeling.extrude_new_solid(self.doc,sketch,5)
        body = pad.getParentGeoFeatureGroup()
        body.Placement.Base = App.Vector(10,20,3); self.doc.recompute()
        face = next('Face'+str(i+1) for i,f in enumerate(pad.Shape.Faces)
                    if isinstance(f.Surface,Part.Plane) and f.CenterOfMass.z > 4)
        p = planes.save(self.doc,[(pad,face)])
        self.assertAlmostEqual(p.Placement.Base.z,8)
        a = self.feature(Part.Vertex(App.Vector()))
        b = self.feature(Part.Vertex(App.Vector(10,0,0)))
        p = planes.save(self.doc,[(self.xy,'')],axis_refs=[(a,'Vertex1'),(b,'Vertex1')],axis='Y')
        self.assertTrue(p.Placement.Rotation.multVec(App.Vector(0,1,0)).isEqual(App.Vector(1,0,0),1e-7))

    def test_rotated_definition_projects_universal_origin(self):
        self.owner.Placement=App.Placement(App.Vector(3,4,5),App.Rotation(App.Vector(1,2,3),37))
        self.doc.recompute()
        p=planes.save(self.doc,[(self.xy,'')],2)
        self.assertAlmostEqual(p.Placement.Base.z,2)
        world=self.owner.getGlobalPlacement().multiply(p.Placement)
        normal=world.Rotation.multVec(App.Vector(0,0,1))
        self.assertLess(world.Base.cross(normal).Length,1e-7)

    def test_task_cleans_up_when_document_closes(self):
        task=plane_task.show();task.choose('XY Plane')
        self.assertIsNotNone(task.overlay)
        App.closeDocument(self.doc.Name)
        self.assertTrue(task.closed)
        self.assertIsNone(task.overlay)
        self.assertIsNone(task.highlights)
        self.assertIsNone(plane_task._active)

    def test_partial_input_and_invalid_geometry_have_actionable_guidance(self):
        a = self.feature(Part.Vertex(App.Vector()))
        b = self.feature(Part.Vertex(App.Vector(10,0,0)))
        c = self.feature(Part.Vertex(App.Vector(20,0,0)))
        line = self.feature(Part.makeLine(App.Vector(), App.Vector(10,0,0)))
        cases = [([], 'Choose a plane'), ([(a,'Vertex1')], 'two more points'),
                 ([(a,'Vertex1'),(b,'Vertex1')], 'third point'),
                 ([(line,'Edge1')], 'point / vertex')]
        for refs, message in cases:
            with self.subTest(refs=refs), self.assertRaisesRegex(planes.IncompletePlane, message):
                planes.solve(self.owner, refs)
        for refs, message in [([(a,'Vertex1'),(b,'Vertex1'),(c,'Vertex1')], 'collinear'),
                              ([(self.xy,''),(a,'Vertex1')], 'by itself')]:
            with self.subTest(refs=refs), self.assertRaisesRegex(ValueError, message) as caught:
                planes.solve(self.owner, refs)
            self.assertNotIsInstance(caught.exception, planes.IncompletePlane)
        normal = planes.solve(self.owner, [(line,'Edge1'),(a,'Vertex1')])
        self.assertTrue(normal.Rotation.multVec(App.Vector(0,0,1)).isEqual(App.Vector(1,0,0),1e-7))
        with self.assertRaisesRegex(ValueError,'lies on'):
            planes.solve(self.owner,[(line,'Edge1'),(a,'Vertex1')],normal_to_line=False)

    def test_preselection_toggle_delete_and_highlight_cleanup(self):
        points = [self.feature(Part.Vertex(App.Vector(*v))) for v in [(0,0,3),(10,0,3),(0,10,3)]]
        for obj in points[:2]: Gui.Selection.addSelection(obj,'Vertex1')
        before = ({o.Name:o.ID for o in self.doc.Objects}, self.doc.UndoCount)
        scene = Gui.activeDocument().activeView().getSceneGraph()
        children = scene.getNumChildren()
        task = plane_task.show()
        self.assertFalse(task.valid)
        self.assertIn('third point',task.status.text())
        self.assertIsNotNone(task.highlights)
        self.assertEqual(task.references.item(0).text(),'1. '+points[0].Label+'.Vertex1')
        self.assertFalse(Gui.Selection.getSelection())
        Gui.Selection.addSelection(points[1],'Vertex1')
        self.assertEqual(len(task.refs),1)
        Gui.Selection.addSelection(points[1],'Vertex1')
        Gui.Selection.addSelection(points[2],'Vertex1')
        self.assertTrue(task.valid, task.status.text())
        task.references.setCurrentRow(1); task.references.setFocus()
        QtTest.QTest.keyClick(task.references,QtCore.Qt.Key_Delete)
        self.assertEqual(len(task.refs),2)
        self.assertIn('third point',task.status.text())
        self.assertIsNotNone(self.doc.getObject(points[1].Name))
        task.visible.setChecked(False)
        self.assertIsNone(task.highlights)
        task.visible.setChecked(True)
        task.reject()
        self.assertIsNone(task.highlights)
        self.assertEqual(scene.getNumChildren(),children)
        self.assertEqual(({o.Name:o.ID for o in self.doc.Objects},self.doc.UndoCount),before)

    def test_origin_axis_toggle_and_delete_restore_defaults(self):
        a = self.feature(Part.Vertex(App.Vector(4,5,0)))
        b = self.feature(Part.Vertex(App.Vector(4,15,0)))
        task = plane_task.show(); task.choose('XY Plane')
        task.frame.header.setChecked(True)
        task.origin_ref.setFocus(); QtTest.QTest.qWait(30)
        for expected in ([ (a,'Vertex1') ], []):
            Gui.Selection.addSelection(a,'Vertex1')
            self.assertEqual(task.origin_refs,expected)
        Gui.Selection.addSelection(a,'Vertex1')
        QtTest.QTest.keyClick(task.origin_ref,QtCore.Qt.Key_Delete)
        self.assertEqual(task.origin_refs,[])
        self.assertTrue(task.placement().Base.isEqual(App.Vector(),1e-7))
        task.axis_ref.setFocus(); QtTest.QTest.qWait(30)
        Gui.Selection.addSelection(a,'Vertex1')
        self.assertFalse(task.valid)
        self.assertIn('second distinct point',task.status.text())
        Gui.Selection.addSelection(b,'Vertex1')
        self.assertTrue(task.valid)
        Gui.Selection.addSelection(b,'Vertex1')
        self.assertFalse(task.valid)
        QtTest.QTest.keyClick(task.axis_ref,QtCore.Qt.Key_Delete)
        self.assertEqual(task.axis_refs,[])
        self.assertTrue(task.valid)

    def test_reverse_axis_persists_edits_undo_and_preserves_plane_footprint(self):
        plane = planes.save(self.doc,[(self.xy,'')],7)
        identity, original = plane.ID, App.Placement(plane.Placement)
        corners = [v.Point for v in plane.Shape.Vertexes]
        task = plane_task.show(plane)
        task.reverse_axis.setChecked(True)
        self.assertFalse(plane.ReverseAxis)
        self.assertTrue(task.accept())
        self.assertEqual(plane.ID,identity)
        self.assertTrue(plane.ReverseAxis)
        self.assertTrue(plane.Placement.Base.isEqual(original.Base,1e-7))
        for basis, sign in [(App.Vector(1,0,0),-1),(App.Vector(0,1,0),-1),(App.Vector(0,0,1),1)]:
            self.assertTrue(plane.Placement.Rotation.multVec(basis).isEqual(
                original.Rotation.multVec(basis)*sign,1e-7))
        self.assertTrue(all(any(p.isEqual(v.Point,1e-7) for v in plane.Shape.Vertexes) for p in corners))
        task = plane_task.show(plane)
        self.assertTrue(task.reverse_axis.isChecked())
        task.reverse_axis.click(); task.reject()
        self.assertTrue(plane.ReverseAxis)
        self.doc.undo(); self.doc.recompute()
        self.assertFalse(plane.ReverseAxis)
        self.doc.redo(); self.doc.recompute()
        self.assertTrue(plane.ReverseAxis)
        document.save_document(self.doc,Path(os.environ['PLUS_TEST_DIR'])/'ReversedPlane.cadprt')

    def test_older_plane_defaults_without_mutation_on_open_or_cancel(self):
        plane = planes.save(self.doc,[(self.xy,'')],5)
        plane.removeProperty('ReverseAxis'); plane.touch(); self.doc.recompute()
        self.assertAlmostEqual(plane.Placement.Base.z,5)
        before = (tuple(plane.PropertiesList),self.doc.UndoCount)
        task = plane_task.show(plane)
        self.assertFalse(task.reverse_axis.isChecked())
        task.reverse_axis.click(); task.reject()
        self.assertEqual((tuple(plane.PropertiesList),self.doc.UndoCount),before)
        task = plane_task.show(plane); task.reverse_axis.click()
        self.assertTrue(task.accept())
        self.assertTrue(plane.ReverseAxis)
        self.doc.undo(); self.doc.recompute()
        self.assertNotIn('ReverseAxis',plane.PropertiesList)
        self.doc.redo(); self.doc.recompute()
        self.assertTrue(plane.ReverseAxis)

    def test_reverse_axis_combines_with_flip_and_explicit_y(self):
        edge = self.feature(Part.makeLine(App.Vector(),App.Vector(10,10,0)))
        for axis in ('X','Y'):
            for flip in (False,True):
                with self.subTest(axis=axis,flip=flip):
                    before = planes.solve(self.owner,[(self.xy,'')],3,axis_refs=[(edge,'Edge1')],axis=axis,flipped=flip)
                    after = planes.solve(self.owner,[(self.xy,'')],3,axis_refs=[(edge,'Edge1')],axis=axis,flipped=flip,reversed_axis=True)
                    self.assertTrue(before.Base.isEqual(after.Base,1e-7))
                    self.assertTrue(before.Rotation.multVec(App.Vector(0,0,1)).isEqual(
                        after.Rotation.multVec(App.Vector(0,0,1)),1e-7))
                    self.assertTrue(before.Rotation.multVec(App.Vector(1,0,0)).isEqual(
                        -after.Rotation.multVec(App.Vector(1,0,0)),1e-7))

    def test_infinite_datum_lines_have_finite_highlights_and_plane(self):
        line = self.owner.newObject('PartDesign::Line','SupportLine')
        line.Placement = App.Placement(App.Vector(2,3,0),App.Rotation(App.Vector(0,0,1),App.Vector(1,0,0)))
        point = self.feature(Part.Vertex(App.Vector(0,10,0)))
        task = plane_task.show()
        Gui.Selection.addSelection(line)
        self.assertFalse(task.valid)
        self.assertIsNotNone(task.highlights)
        branch = task.highlights.getChild(2)
        coords = branch.getChild(1)
        for vector in coords.point.getValues():
            self.assertTrue(all(abs(v)<100 for v in vector))
        Gui.Selection.addSelection(point,'Vertex1')
        self.assertTrue(task.valid,task.status.text())
        self.assertTrue(task.placement().Base.isEqual(App.Vector(0,10,0),1e-7))
        self.assertTrue(task.accept())
        self.assertFalse(task.result.Shape.isNull())


class TestNumericCommit(unittest.TestCase):
    def test_shared_editors_wait_for_focus_leave(self):
        numeric_fields.install()
        form = QtWidgets.QWidget(); layout = QtWidgets.QVBoxLayout(form)
        editors = [QtWidgets.QDoubleSpinBox(),QtWidgets.QSpinBox(),
                   Gui.UiLoader().createWidget('Gui::QuantitySpinBox'),Gui.UiLoader().createWidget('Gui::InputField')]
        other = QtWidgets.QLineEdit()
        for editor in editors:
            if editor.inherits('Gui::InputField') or editor.inherits('Gui::QuantitySpinBox'):
                editor.setProperty('unit','mm'); editor.setProperty('rawValue',1.0)
            else: editor.setValue(1)
            layout.addWidget(editor)
        layout.addWidget(other); form.show(); form.activateWindow(); QtTest.QTest.qWait(100)
        try:
            for editor in editors:
                with self.subTest(editor=editor.metaObject().className()):
                    changes = []
                    callback = lambda value: changes.append(value)
                    native = editor.inherits('Gui::InputField') or editor.inherits('Gui::QuantitySpinBox')
                    if native: QtCore.QObject.connect(editor,QtCore.SIGNAL('valueChanged(double)'),callback)
                    else: editor.valueChanged.connect(callback)
                    editor.setFocus(); editor.selectAll()
                    QtTest.QTest.keyClicks(editor,'23'); QtTest.QTest.qWait(100)
                    self.assertEqual(changes,[])
                    other.setFocus(); QtTest.QTest.qWait(50)
                    self.assertEqual(len(changes),1,changes)
                    self.assertAlmostEqual(changes[0],23)
                    if native: QtCore.QObject.disconnect(editor,QtCore.SIGNAL('valueChanged(double)'),callback)
                    else: editor.valueChanged.disconnect(callback)
        finally: form.close()


from TestComponentMove import TestComponentMove
from unittest.mock import patch


class TestMoveNumericCommit(TestComponentMove):
    # Reuse the native movement fixture, without inheriting its test inventory.
    def test_typing_does_not_rebuild_move_preview(self):
        task = self.task(self.first)
        task.distance.setText("6 mm"); task.update_preview()
        task.distance.setFocus(); task.distance.selectAll()
        with patch.object(task,'update_preview',wraps=task.update_preview) as update:
            QtTest.QTest.keyClicks(task.distance,'23'); QtTest.QTest.qWait(50)
            self.assertEqual(update.call_count,0)
            task.direction.setFocus(); QtTest.QTest.qWait(50)
            self.assertEqual(update.call_count,1)


# unittest otherwise discovers inherited regression methods a second time.
for _name in tuple(name for name in dir(TestComponentMove) if name.startswith('test_')):
    setattr(TestMoveNumericCommit, _name, None)
del TestComponentMove
