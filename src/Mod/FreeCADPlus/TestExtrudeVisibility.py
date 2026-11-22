# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native regression for approved task visibility and face profiles."""
import json
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtWidgets, QtTest
from freecad_plus import document, modeling, extrusion, extrude_task, plane_task, idle_tasks, panel, editing
from TestDesignInteractions import TestDesignInteractions, settle


class TestExtrudeVisibility(TestDesignInteractions):
    def materials(self, obj):
        return (obj.ViewObject.Transparency, [(tuple(m.DiffuseColor), tuple(m.AmbientColor), m.Transparency)
                                             for m in obj.ViewObject.ShapeAppearance])

    def scene(self):
        target=modeling.extrude_new_solid(self.doc,self.circle(),5)
        profile=self.circle();profile.Placement.Base.z=5
        hidden=self.circle();hidden.Visibility=False
        sheet=self.owner.newObject('Part::Feature','Sheet');sheet.Shape=Part.makePlane(4,3,App.Vector(10,0,0))
        wire=self.owner.newObject('Part::Feature','Wire');wire.Shape=Part.makeLine(App.Vector(),App.Vector(10,0,0))
        self.doc.recompute()
        return target,profile,hidden,sheet,wire

    def open(self, profile):
        Gui.Selection.clearSelection();Gui.Selection.addSelection(profile)
        task=extrude_task.show();settle()
        return task

    def test_new_filter_and_cancel_restore_without_undo(self):
        target,profile,hidden,sheet,wire=self.scene()
        first=App.Material();first.DiffuseColor=(.9,.1,.2);first.Transparency=.25
        second=App.Material();second.DiffuseColor=(.1,.3,.8);second.Transparency=.8
        target.ViewObject.ShapeAppearance=[first,second]
        self.doc.recompute();settle()  # Finish the fixture's authored material/link update.
        before=self.snapshot();appearance=self.materials(target);Gui.activeDocument().Modified=False
        task=self.open(profile)
        self.assertTrue(profile.Visibility);self.assertTrue(target.Visibility);self.assertTrue(sheet.Visibility)
        self.assertFalse(hidden.Visibility);self.assertFalse(wire.Visibility)
        self.assertTrue(all(not obj.Visibility for obj in self.owner.Origin.OriginFeatures))
        self.assertEqual(target.ViewObject.Transparency,65)
        self.assertEqual(self.doc.UndoCount,before[-1]);self.assertFalse(self.doc.HasPendingTransaction)
        self.assertFalse(Gui.activeDocument().Modified)
        task.reject();settle()
        self.assertEqual(self.snapshot(),before);self.assertEqual(self.materials(target),appearance)
        self.assertFalse(Gui.activeDocument().Modified)

    def test_eye_clicks_persist_and_remain_undoable(self):
        target,profile,hidden,sheet,wire=self.scene();task=self.open(profile)
        self.eye(target);self.assertFalse(target.Visibility);self.assertFalse(task.closed)
        self.eye(hidden);self.assertTrue(hidden.Visibility)
        self.eye(wire);self.assertTrue(wire.Visibility)
        plane=next(o for o in self.owner.Origin.OriginFeatures if o.Role=='XY_Plane')
        self.eye(plane);self.assertTrue(plane.Visibility)
        task.end1['length'].setValue(7);task.commit_numbers();settle()
        self.assertTrue(wire.Visibility);self.assertTrue(plane.Visibility)
        task.reject()
        self.assertFalse(target.Visibility);self.assertTrue(hidden.Visibility)
        self.assertTrue(wire.Visibility);self.assertTrue(plane.Visibility)
        self.doc.undo();settle();self.assertFalse(hidden.Visibility)
        self.doc.undo();settle();self.assertTrue(target.Visibility)
        self.doc.redo();settle();self.assertFalse(target.Visibility)

    def test_target_field_color_focus_and_original_material_on_accept(self):
        target,profile,hidden,sheet,wire=self.scene()
        prefs=App.ParamGet('User parameter:BaseApp/Preferences/View')
        saved=prefs.GetUnsigned('SelectionColor',0x1CAD1CFF);prefs.SetUnsigned('SelectionColor',0xC04090FF)
        target.ViewObject.ShapeColor=(.2,.6,.4);appearance=self.materials(target)
        try:
            task=self.open(profile);task.modes['Add'].click();task.fields['target'].setFocus();settle()
            self.assertEqual(target.ViewObject.Transparency,0)
            Gui.Selection.addSelection(target);settle()
            self.assertEqual(task.links['target'][0],target)
            for actual,expected in zip(target.ViewObject.ShapeColor[:3],(192/255,64/255,144/255)):
                self.assertAlmostEqual(actual,expected,places=5)
            task.end1['length'].setFocus();settle()
            self.assertEqual(target.ViewObject.Transparency,65)
            self.assertFalse(hidden.Visibility)
            self.assertTrue(task.accept())
            self.assertEqual(self.materials(target),appearance)
            self.assertEqual(self.materials(task.result),appearance)
        finally:prefs.SetUnsigned('SelectionColor',saved)

    def test_edit_shows_only_profile_target_and_restores_cancel(self):
        target,profile,hidden,sheet,wire=self.scene()
        feature=extrusion.save(self.doc,[(profile,'')],{'target':(target,'')},dict(extrusion.DEFAULTS,operation='Add'))
        before=self.snapshot();appearance=self.materials(target)
        task=extrude_task.show(feature);settle()
        self.assertTrue(profile.Visibility);self.assertTrue(target.Visibility)
        self.assertFalse(feature.Visibility);self.assertFalse(hidden.Visibility)
        self.assertFalse(sheet.Visibility);self.assertFalse(wire.Visibility)
        self.assertEqual(target.ViewObject.Transparency,65)
        task.reject();self.assertEqual(self.snapshot(),before);self.assertEqual(self.materials(target),appearance)
        task=extrude_task.show(feature);self.eye(sheet);self.assertTrue(sheet.Visibility)
        self.assertTrue(task.accept());self.assertTrue(sheet.Visibility)
        self.assertFalse(target.Visibility);self.assertTrue(feature.Visibility)

    def test_planar_sheet_face_associativity_and_save_fixture(self):
        sheet=self.owner.newObject('Part::Feature','SheetProfile')
        sheet.Shape=Part.makePlane(4,3)
        sheet.Placement=App.Placement(App.Vector(7,2,3),App.Rotation(App.Vector(0,1,0),35))
        self.doc.recompute()
        Gui.Selection.clearSelection();Gui.Selection.addSelection(sheet,'Face1')
        task=extrude_task.show();settle();self.assertTrue(task.valid,task.status.text())
        self.assertEqual(task.refs,[(sheet,'Face1')]);self.assertTrue(task.accept())
        feature=task.result;identity=feature.ID
        self.assertAlmostEqual(feature.Shape.Volume,96,places=5);self.assertTrue(sheet.Visibility)
        before=feature.Shape.CenterOfMass;sheet.Placement.Base.x+=5;self.doc.recompute()
        self.assertAlmostEqual(feature.Shape.CenterOfMass.x-before.x,5,places=5)
        task=extrude_task.show(feature);settle()
        self.assertFalse(sheet.Visibility);self.assertTrue(task.valid,task.status.text())
        task.end1['length'].setValue(3);self.assertTrue(task.accept())
        self.assertEqual(feature.ID,identity);self.assertAlmostEqual(feature.Shape.Volume,36,places=5)
        folder=__import__('pathlib').Path(__import__('os').environ['PLUS_TEST_DIR'])/'face-persistence'
        folder.mkdir(exist_ok=True)
        document.save_document(self.doc,folder/'Face.cadprt')
        (folder/'expected.json').write_text(json.dumps(dict(feature=feature.Name,id=identity,sheet=sheet.Name)))

    def test_solid_face_normalizes_body_and_supports_add(self):
        target=modeling.extrude_new_solid(self.doc,self.circle(),5);body=target.getParentGeoFeatureGroup()
        face=next('Face'+str(i+1) for i,f in enumerate(target.Shape.Faces)
                  if isinstance(f.Surface,Part.Plane) and f.normalAt(0,0).z>.99)
        Gui.Selection.clearSelection();Gui.Selection.addSelection(body,face)
        task=extrude_task.show();settle();self.assertEqual(task.refs,[(target,face)])
        task.modes['Add'].click();task.fields['target'].setFocus();settle();Gui.Selection.addSelection(target)
        self.assertTrue(task.accept())
        self.assertGreater(task.result.Shape.Volume,target.Shape.Volume)
        self.assertEqual(task.result.ProfileReferences[0][0],target)
        self.assertNotIn('Invalid',task.result.State)

    def test_reject_standalone_edges_datums_and_nonplanar_faces(self):
        target,profile,hidden,sheet,wire=self.scene()
        task=self.open(profile);task.clear_profile()
        Gui.Selection.addSelection(wire,'Edge1');settle();self.assertFalse(task.refs)
        datum=next(o for o in self.owner.Origin.OriginFeatures if o.Role=='XY_Plane')
        Gui.Selection.addSelection(datum);settle();self.assertFalse(task.refs)
        side=next('Face'+str(i+1) for i,f in enumerate(target.Shape.Faces) if not isinstance(f.Surface,Part.Plane))
        Gui.Selection.addSelection(target,side);settle()
        self.assertFalse(task.valid);self.assertIn('planar',task.status.text())
        before=self.snapshot();self.assertFalse(task.accept());self.assertFalse(task.closed)
        self.assertEqual(self.snapshot()[:1],before[:1]);task.reject()

    def test_plane_and_native_datum_tasks_keep_history_controls(self):
        solid=modeling.extrude_new_solid(self.doc,self.circle(),5)
        task=plane_task.show();self.eye(solid);self.assertFalse(solid.Visibility)
        self.assertFalse(task.closed);task.reject();self.assertFalse(solid.Visibility)
        for kind in ('Line','Point'):
            feature=idle_tasks.create_datum(kind);settle()
            transaction=App.getActiveTransaction();undo=self.doc.UndoCount
            self.eye(solid)
            self.assertEqual(App.getActiveTransaction(),transaction);self.assertEqual(self.doc.UndoCount,undo)
            self.assertEqual(Gui.activeDocument().getInEdit().Object,feature)
            self.dialog(QtWidgets.QDialogButtonBox.Cancel)
            self.assertFalse(solid.Visibility)

    def test_visibility_does_not_recompute_manual_preview(self):
        target,profile,hidden,sheet,wire=self.scene();task=self.open(profile)
        task.automatic.setChecked(False);revision=task.revisions;volume=task.tool_shape.Volume
        task.end1['length'].setValue(17);task.commit_numbers()
        self.eye(target)
        self.assertFalse(target.Visibility);self.assertEqual(task.revisions,revision)
        self.assertEqual(task.tool_shape.Volume,volume);task.reject()

    def test_replacing_clearing_and_disabling_target_restores_color(self):
        target,profile,hidden,sheet,wire=self.scene()
        other=modeling.extrude_new_solid(self.doc,self.circle(),4)
        original={obj:tuple(obj.ViewObject.ShapeColor) for obj in (target,other)}
        task=self.open(profile);task.modes['Add'].click();task.fields['target'].setFocus();settle()
        Gui.Selection.addSelection(target);settle();chosen=tuple(target.ViewObject.ShapeColor)
        self.assertNotEqual(chosen,original[target])
        Gui.Selection.addSelection(other);settle()
        self.assertEqual(tuple(target.ViewObject.ShapeColor),original[target])
        self.assertEqual(tuple(other.ViewObject.ShapeColor),chosen)
        task.clear_reference('target')
        self.assertEqual(tuple(other.ViewObject.ShapeColor),original[other])
        Gui.Selection.addSelection(target);settle();task.modes['New Solid'].click();settle()
        self.assertEqual(tuple(target.ViewObject.ShapeColor),original[target])
        self.assertEqual(target.ViewObject.Transparency,65);task.reject()

    def test_save_during_preview_stores_original_material_and_visibility(self):
        from pathlib import Path
        import os,zipfile,xml.etree.ElementTree as ET
        target,profile,hidden,sheet,wire=self.scene();before=self.snapshot();appearance=self.materials(target)
        task=self.open(profile)
        path=Path(os.environ['PLUS_TEST_DIR'])/'during-preview.FCStd'
        self.doc.saveAs(str(path))
        self.assertFalse(task.closed);self.assertFalse(wire.Visibility);self.assertEqual(target.ViewObject.Transparency,65)
        task.reject();self.assertEqual(self.snapshot(),before);self.assertEqual(self.materials(target),appearance)
        with zipfile.ZipFile(path) as archive:
            tree=ET.fromstring(archive.read('Document.xml'))
        saved=tree.find(".//ObjectData/Object[@name='"+wire.Name+"']/Properties/Property[@name='Visibility']/Bool")
        self.assertIsNotNone(saved);self.assertEqual(saved.attrib['value'],'true')

    def test_external_extrude_restores_source_and_host_and_keeps_eye_intent(self):
        from freecad_plus import external,hierarchy
        from pathlib import Path
        import os
        folder=Path(os.environ['PLUS_TEST_DIR'])/'external-visibility';folder.mkdir(exist_ok=True)
        document.save_document(self.doc,folder/'Host.cadprt')
        source=document.new_document('ExternalDisplay')
        owner=document.validate(source).Definitions[0]
        document.save_document(source,folder/'Source.cadprt');external.import_file(self.doc,source)
        App.setActiveDocument(self.doc.Name);editing.edit_unused(self.doc,owner)
        profile=modeling.new_sketch(self.doc);profile.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),3),False)
        source.recompute();solid=modeling.extrude_new_solid(self.doc,profile,5)
        other=modeling.new_sketch(self.doc);other.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),1),False)
        source.recompute()
        source_before=self.snapshot(source);host_before=self.snapshot();appearance=self.materials(solid)
        Gui.getDocument(source.Name).Modified=False;Gui.getDocument(self.doc.Name).Modified=False
        Gui.Selection.clearSelection();Gui.Selection.addSelection(other);task=extrude_task.show();settle()
        self.assertEqual(task.owner,owner);self.assertEqual(solid.ViewObject.Transparency,65)
        self.assertFalse(Gui.getDocument(source.Name).Modified);self.assertFalse(Gui.getDocument(self.doc.Name).Modified)
        task.reject();self.assertEqual(self.snapshot(source),source_before);self.assertEqual(self.snapshot(),host_before)
        self.assertEqual(self.materials(solid),appearance)
        task=extrude_task.show();self.panel.refresh()
        row=next(i.data(0,panel._ROLE) for i in self.panel._maps[2].values() if panel.lookup(i.data(0,panel._ROLE).ref)==solid)
        self.panel.toggle_history_visibility(row);task.reject();self.assertFalse(solid.Visibility)
        self.assertEqual(self.snapshot()[:2],host_before[:2])

    def test_part_tree_visibility_joins_native_task_transaction(self):
        from freecad_plus import display
        feature=idle_tasks.create_datum('Line');settle()
        self.panel.refresh()
        row=next(i.data(0,panel._ROLE) for i in self.panel._maps[1].values()
                 if i.data(0,panel._ROLE).kind=='occurrence')
        transaction=App.getActiveTransaction();undo=self.doc.UndoCount
        self.panel.set_display(row,shown=False)
        self.assertEqual(App.getActiveTransaction(),transaction);self.assertEqual(self.doc.UndoCount,undo)
        self.assertEqual(Gui.activeDocument().getInEdit().Object,feature)
        self.assertFalse(display.state(self.owner)[1])
        self.dialog(QtWidgets.QDialogButtonBox.Cancel)
        self.assertTrue(display.state(self.owner)[1])


def verify_face_reopen(output):
    from pathlib import Path
    folder=Path(output)/'face-persistence';expected=json.loads((folder/'expected.json').read_text())
    doc=document.open_document(folder/'Face.cadprt')
    feature=doc.getObject(expected['feature']);sheet=doc.getObject(expected['sheet'])
    assert feature.ID==expected['id'] and feature.ProfileReferences[0][0]==sheet
    assert feature.Shape.isValid() and abs(feature.Shape.Volume-36)<1e-5
    owner=extrusion.owner(feature)
    from freecad_plus import isolation
    routes=isolation.occurrences(doc,owner)
    if routes:editing.edit(routes[0])
    else:editing.edit_unused(doc,owner)
    task=extrude_task.show(feature);assert task.valid,task.status.text();task.reject()
    before=feature.Shape.CenterOfMass;sheet.Placement.Base.y+=2;doc.recompute()
    assert abs(feature.Shape.CenterOfMass.y-before.y-2)<1e-6
    App.closeDocument(doc.Name)
