# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native surface topology, persistence and task lifecycle regressions."""
import unittest
import FreeCAD as App, FreeCADGui as Gui, Part
from PySide6 import QtCore, QtWidgets, QtTest
from TestDerivedGeometry import TestDerivedGeometry
from freecad_plus import document, hierarchy, editing, panel, derived_geometry as derived


class TestJoinedExtraction(unittest.TestCase):
    setUp=TestDerivedGeometry.setUp
    tearDown=TestDerivedGeometry.tearDown
    snapshot=TestDerivedGeometry.snapshot
    ref=TestDerivedGeometry.ref

    def box(self):
        obj=self.owner.newObject('Part::Box','LocalSolid')
        obj.Length=10;obj.Width=8;obj.Height=6;self.doc.recompute()
        return obj

    def extract(self,obj,faces,join=True,feature=None):
        return derived.save(self.doc,[(obj,'Face'+str(i)) for i in faces],'Extract',feature,join=join)

    def test_connected_chain_closed_shell_and_source_update(self):
        box=self.box();undo=self.doc.UndoCount
        result=self.extract(box,[1,3,2])[0]  # Opposite faces connected by a third face.
        self.assertEqual(result.Shape.ShapeType,'Shell');self.assertTrue(result.Shape.isValid())
        self.assertEqual(len(result.Shape.Faces),3);self.assertFalse(result.Shape.Solids)
        self.assertEqual(self.doc.UndoCount,undo+1)
        self.assertEqual(derived.saved_refs(result),[(box,'Face'+str(i)) for i in (1,3,2)])
        self.assertEqual([o for o in document.history(self.doc,self.owner) if derived.is_derived(o)],[result])
        self.assertEqual(len(result.Shape.Edges),10)  # Shared edges really sewn, not 12 loose edges.
        box.Width=12;self.doc.recompute()
        self.assertFalse(result.GeometryError);self.assertAlmostEqual(result.Shape.Area,2*12*6+10*6)
        closed=self.extract(box,range(1,7))[0]
        self.assertEqual(closed.Shape.ShapeType,'Shell');self.assertTrue(closed.Shape.isClosed())
        self.assertFalse(closed.Shape.Solids);self.assertEqual(len(closed.Shape.Faces),6)
        self.assertAlmostEqual(box.Shape.Volume,720)

    def test_disconnected_point_contact_and_overlap_are_atomic(self):
        box=self.box();before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'disconnected'):self.extract(box,[1,2])
        self.assertEqual(self.snapshot(),before)
        first=self.owner.newObject('Part::Feature','FirstSheet');first.Shape=Part.makePlane(10,10)
        second=self.owner.newObject('Part::Feature','SecondSheet');second.Shape=Part.makePlane(10,10,App.Vector(10,10,0))
        self.doc.recompute();before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'disconnected'):
            derived.save(self.doc,[(first,'Face1'),(second,'Face1')],'Extract',join=True)
        self.assertEqual(self.snapshot(),before)
        second.Shape=first.Shape.copy();self.doc.recompute();before=self.snapshot()
        with self.assertRaises(ValueError):
            derived.save(self.doc,[(first,'Face1'),(second,'Face1')],'Extract',join=True)
        self.assertEqual(self.snapshot(),before)

    def test_separate_history_and_undo_redo(self):
        box=self.box();before=self.snapshot();results=self.extract(box,[1,2],False)
        self.assertEqual([o.Label for o in results],['extracted surface','extracted surface (2)'])
        self.assertTrue(all(o.Shape.ShapeType=='Face' and not o.JoinSurfaces for o in results))
        self.assertEqual([o for o in document.history(self.doc,self.owner) if derived.is_derived(o)],results)
        names=[o.Name for o in results];self.doc.undo();self.doc.recompute()
        self.assertEqual(self.snapshot(),before)
        self.doc.redo();self.doc.recompute()
        self.assertTrue(all(self.doc.getObject(n).Shape.isValid() for n in names));document.validate(self.doc)

    def test_curved_faces_and_moved_body_coordinates(self):
        clone=derived.save(self.doc,[self.ref(self.body)])[0]
        result=self.extract(clone,[1,3])[0]
        from freecad_plus import planes
        expected=[planes.shape(self.owner,(clone,'Face'+str(i))) for i in (1,3)]
        self.assertAlmostEqual(result.Shape.Area,sum(face.Area for face in expected))
        self.assertTrue(result.Shape.BoundBox.Center.isEqual(Part.makeCompound(expected).BoundBox.Center,1e-6))
        self.link.Placement.Base+=App.Vector(0,20,0);self.doc.recompute()
        self.assertFalse(result.GeometryError)
        expected=[planes.shape(self.owner,(clone,'Face'+str(i))) for i in (1,3)]
        self.assertTrue(result.Shape.BoundBox.Center.isEqual(Part.makeCompound(expected).BoundBox.Center,1e-6))
        cylinder=self.owner.newObject('Part::Cylinder','Cylinder');self.doc.recompute()
        curved=self.extract(cylinder,[1,2])[0]
        self.assertEqual(len(curved.Shape.Faces),2);self.assertTrue(curved.Shape.isValid())
        self.assertFalse(curved.Shape.Solids)

    def test_multiple_objects_placement_save_reopen_and_export(self):
        from freecad_plus import part_transfer_ops
        first=self.owner.newObject('Part::Feature','FirstSheet');first.Shape=Part.makePlane(10,10)
        second=self.owner.newObject('Part::Feature','SecondSheet');second.Shape=Part.makePlane(10,10)
        second.Placement.Base=App.Vector(10,0,0);self.doc.recompute()
        result=derived.save(self.doc,[(first,'Face1'),(second,'Face1')],'Extract',join=True)[0]
        self.assertAlmostEqual(result.Shape.Area,200);self.assertEqual(len(result.Shape.Edges),7)
        self.assertEqual(result.ExtractSourceObjects,[first,second])
        export=self.out/'Exported.cadprt';part_transfer_ops.export_parts([self.owner],export)
        exported=document.open_document(export);copy=next(o for o in exported.Objects if derived.is_derived(o))
        self.assertEqual(len(derived.saved_refs(copy)),2)
        self.assertTrue(all(o.Document==exported for o,_ in derived.saved_refs(copy)))
        copy.touch();exported.recompute();self.assertAlmostEqual(copy.Shape.Area,200)
        App.closeDocument(exported.Name)
        path=self.out/'Joined.cadprt';name=result.Name;box_name=first.Name
        document.save_document(self.doc,path);App.closeDocument(self.doc.Name)
        self.doc=document.open_document(path);result=self.doc.getObject(name);self.owner=derived.owner(result)
        self.assertEqual(len(derived.saved_refs(result)),2);self.assertTrue(result.JoinSurfaces)
        result.touch();self.doc.recompute();self.assertFalse(result.GeometryError)
        self.doc.getObject(box_name).Placement.Base.z=5;self.doc.recompute()
        self.assertTrue(result.Shape.isNull());self.assertIn('disconnected',result.GeometryError)

    def test_edit_join_split_identity_downstream_cancel_and_cycle(self):
        from freecad_plus import clone_task
        box=self.box();result=self.extract(box,[1,3])[0];identity=result.ID
        consumer=self.extract(result,[1],False)[0]
        task=clone_task.show(feature=result);self.assertTrue(task.form.join.isChecked())
        self.assertEqual(task.refs,[(box,'Face1'),(box,'Face3')]);before=self.snapshot()
        task.form.join.setChecked(False);task.reject();self.assertEqual(self.snapshot(),before)
        task=clone_task.show(feature=result);task.pick(box,'Face2')
        self.assertTrue(task.accept());self.assertEqual(result.ID,identity);self.assertEqual(len(result.Shape.Faces),3)
        undo=self.doc.UndoCount;task=clone_task.show(feature=result);task.form.join.setChecked(False)
        self.assertTrue(task.accept());self.assertEqual(task.results[0],result)
        self.assertEqual(len(task.results),3);self.assertEqual(result.ID,identity)
        self.assertEqual(derived.saved_ref(consumer)[0],result);self.assertTrue(consumer.Shape.isValid())
        self.assertEqual(self.doc.UndoCount,undo+1);self.doc.undo();self.doc.recompute()
        self.assertEqual(len(result.Shape.Faces),3);self.assertTrue(result.JoinSurfaces)
        before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'downstream'):
            self.extract(consumer,[1],True,result)
        self.assertEqual(self.snapshot(),before)

    def test_task_default_error_recovery_gestures_and_no_preview_writes(self):
        from freecad_plus import clone_task,selection_scope,selection_list
        box=self.box();before=self.snapshot();task=clone_task.show(extract=True)
        self.assertTrue(task.form.join.isChecked());self.assertEqual(selection_scope.current()[0],'surface')
        Gui.Selection.addSelection(box,'Face1');QtTest.QTest.qWait(80)
        Gui.Selection.addSelection(box,'Face2');QtTest.QTest.qWait(80)
        self.assertEqual(len(task.refs),2);self.assertTrue(task.form.status.error)
        self.assertIsNone(task.overlay);self.assertFalse(task.accept());self.assertEqual(self.snapshot(),before)
        dock=Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks')
        button=next(box.button(QtWidgets.QDialogButtonBox.Ok) for box in dock.findChildren(QtWidgets.QDialogButtonBox)
                    if box.button(QtWidgets.QDialogButtonBox.Ok))
        self.assertFalse(button.isEnabled())
        dock.grab().save(str(self.out/'disconnected.png'))
        task.form.join.setChecked(False);QtTest.QTest.qWait(60)
        self.assertFalse(task.form.status.error);self.assertIsNotNone(task.overlay)
        self.assertTrue(button.isEnabled())
        dock.grab().save(str(self.out/'separate.png'))
        with selection_list.pick_intent(True):Gui.Selection.addSelection(box,'Face2')
        QtTest.QTest.qWait(80);self.assertEqual(task.refs,[(box,'Face1')])
        task.pick(box,'Face3');task.form.join.setChecked(True);QtTest.QTest.qWait(60)
        self.assertFalse(task.form.status.error);self.assertEqual(self.snapshot(),before)
        dock.grab().save(str(self.out/'joined.png'))
        task.form.preview.setChecked(False);self.assertIsNone(task.overlay)
        self.assertTrue(task.accept());self.assertEqual(len(task.results),1)
        self.assertEqual(len(task.results[0].Shape.Faces),2)

    def test_legacy_load_and_stale_source_guard(self):
        from freecad_plus import clone_task
        box=self.box()
        with document.transaction(self.doc,'Legacy extraction'):
            old=self.owner.newObject('Part::FeaturePython','OldExtract')
            derived.Derived(old,'Extract','surface');derived.ViewDerived(old.ViewObject)
            old.Source=(box,['Face1']);old.SourceObject=box
        self.assertEqual(old.DerivedGeometryFormat,derived.MARKER)
        task=clone_task.show(feature=old);self.assertFalse(task.form.join.isChecked());task.reject()
        task=clone_task.show(feature=old);task.form.join.setChecked(True);task.pick(box,'Face3')
        self.assertTrue(task.accept());self.assertEqual(old.DerivedGeometryFormat,derived.EXTRACT_MARKER)
        task=clone_task.show(feature=old)
        old.JoinSurfaces=False;before=self.snapshot()
        self.assertFalse(task.accept());self.assertIn('source changed',task.form.status.text())
        self.assertEqual(self.snapshot(),before);task.reject();old.JoinSurfaces=True

    def test_deleted_secondary_source_is_not_silently_dropped(self):
        from freecad_plus import clone_task
        first=self.owner.newObject('Part::Feature','FirstSheet');first.Shape=Part.makePlane(10,10)
        second=self.owner.newObject('Part::Feature','SecondSheet');second.Shape=Part.makePlane(10,10,App.Vector(10,0,0))
        self.doc.recompute()
        result=derived.save(self.doc,[(first,'Face1'),(second,'Face1')],'Extract',join=True)[0]
        self.doc.removeObject(second.Name);self.doc.recompute()
        self.assertTrue(result.GeometryError);self.assertTrue(result.Shape.isNull())
        task=clone_task.show(feature=result);self.assertEqual(len(task.refs),2)
        self.assertTrue(task.form.status.error);self.assertFalse(task.accept())
        task.form.objects.topLevelItem(1).setSelected(True);task.remove_inputs()
        self.assertTrue(task.accept());self.assertEqual(result.Shape.ShapeType,'Face')
        self.assertEqual(result.ExtractFaceCount,1)

    def test_external_component_owns_join_and_repeated_occurrences(self):
        source=document.new_document('SurfaceLibrary');owner=document.validate(source).Definitions[0]
        box=owner.newObject('Part::Box','Solid');source.recompute()
        document.save_document(source,self.out/'Library.cadprt')
        document.save_document(self.doc,self.out/'Host.cadprt')
        App.setActiveDocument(self.doc.Name);QtTest.QTest.qWait(80)
        links=[hierarchy.add_children(self.owner,[owner])[0] for _ in range(2)]
        editing.edit((self.top,links[1]));before={o.Name:o.ID for o in self.doc.Objects};undo=source.UndoCount
        from freecad_plus import clone_task
        task=clone_task.show(extract=True);task.pick(box,'Face1');task.pick(box,'Face3')
        self.assertTrue(task.accept());result=task.results[0]
        self.assertEqual(result.Document,source);self.assertEqual(derived.owner(result),owner)
        self.assertEqual(source.UndoCount,undo+1);self.assertEqual({o.Name:o.ID for o in self.doc.Objects},before)
        document.save_document(source);document.save_document(self.doc)
