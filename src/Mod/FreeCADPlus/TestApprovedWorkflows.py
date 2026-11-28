# SPDX-License-Identifier: LGPL-2.1-or-later
import unittest,os,math
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui,Part
from PySide6 import QtTest,QtWidgets
from freecad_plus import document,editing,hierarchy,panel,planes,mesh_shape,trim_body,trim_task,derived_geometry,appearance,intersections


class TestApprovedWorkflows(unittest.TestCase):
    def setUp(self):
        self.before=set(App.listDocuments());Gui.Selection.clearSelection()
        self.doc=document.new_document('WorkflowTests');self.owner=document.validate(self.doc).Definitions[0]
        editing.edit((document.validate(self.doc).Group[0],))
        with document.transaction(self.doc,'Fixture'):
            self.box=self.owner.newObject('Part::Feature','Box');self.box.Shape=Part.makeBox(30,24,20)
            self.sheet=self.owner.newObject('Part::Feature','Boundary');self.sheet.Shape=Part.makePlane(50,50,App.Vector(-10,-10,12))
            self.curve=self.owner.newObject('Part::Feature','Curve');self.curve.Shape=Part.makeCircle(10,App.Vector(10,10,10),App.Vector(0,1,0))
            self.sketch=self.owner.newObject('Sketcher::SketchObject','SectionSketch');self.sketch.Placement.Base=App.Vector(0,0,12)

    def tearDown(self):
        import sys
        for name in ('mesh_task','trim_task','intersection_task','plane_task','sketch_task'):
            task=getattr(sys.modules.get('freecad_plus.'+name),'_active',None)
            if task:task.reject()
        for name in set(App.listDocuments())-self.before:
            try:
                Gui.getDocument(name).resetEdit();App.closeDocument(name)
            except Exception:pass

    def test_trim_finite_offset_reverse_and_invalid_boundary(self):
        settings=dict(mode=0,plane=0,offset=0,reverse=False)
        keep,waste=trim_body.evaluate(self.owner,(self.box,''),[(self.sheet,'')],settings)
        self.assertAlmostEqual(keep.Volume,8640,5);self.assertAlmostEqual(waste.Volume,5760,5)
        settings['reverse']=True
        self.assertAlmostEqual(trim_body.evaluate(self.owner,(self.box,''),[(self.sheet,'')],settings)[0].Volume,5760,5)
        settings['reverse']=False;settings['offset']=2
        self.assertAlmostEqual(trim_body.evaluate(self.owner,(self.box,''),[(self.sheet,'')],settings)[0].Volume,10080,5)
        self.sheet.Shape=Part.makePlane(20,20,App.Vector(2,2,12));self.doc.recompute()
        with self.assertRaises(ValueError):trim_body.evaluate(self.owner,(self.box,''),[(self.sheet,'')],settings)

    def test_trim_commit_edit_undo_and_panel(self):
        undo=self.doc.UndoCount
        result=trim_body.save(self.doc,(self.box,''),[],dict(mode=1,plane=0,offset=12,reverse=False))
        self.assertEqual(result.getTypeIdOfProperty('TrimTarget'),'App::PropertyLinkSubGlobal')
        self.assertAlmostEqual(result.Shape.Volume,8640,5);self.assertEqual(self.doc.UndoCount,undo+1)
        self.doc.undo();self.doc.redo();self.doc.recompute();document.validate(self.doc)
        task=trim_task.show(result);self.assertEqual(task.target,(self.box,''));task.form.offset.setValue(10)
        self.assertTrue(task.apply(),task.form.status.text());self.assertIsNone(task.target);task.reject()
        self.assertAlmostEqual(result.Shape.Volume,7200,5)

    def test_trim_joined_and_curved_boundaries(self):
        with document.transaction(self.doc,'Surface tools'):
            a=self.owner.newObject('Part::Feature','PatchA');a.Shape=Part.makePlane(25,50,App.Vector(-10,-10,12))
            b=self.owner.newObject('Part::Feature','PatchB');b.Shape=Part.makePlane(25,50,App.Vector(15,-10,12))
            curved=self.owner.newObject('Part::Feature','CurvedBoundary');curved.Shape=Part.makeCylinder(40,60,App.Vector(-15,-15,-20)).Faces[0]
        settings=dict(mode=0,offset=0,reverse=False)
        keep,_=trim_body.evaluate(self.owner,(self.box,''),[(a,''),(b,'')],settings)
        self.assertAlmostEqual(keep.Volume,8640,5)
        keep,waste=trim_body.evaluate(self.owner,(self.box,''),[(curved,'')],settings)
        self.assertGreater(keep.Volume,0);self.assertGreater(waste.Volume,0)
        self.assertAlmostEqual(keep.Volume+waste.Volume,self.box.Shape.Volume,5)

    def test_combined_mesh_ownership_and_recompute(self):
        settings=dict(method=0,parameters=dict(LinearDeflection=.1,AngularDeflection=math.radians(30),Relative=False),colors=False,group_colors=False)
        undo=self.doc.UndoCount
        result=mesh_shape.save(self.doc,[(self.box,''),(self.sheet,'')],settings)
        self.assertEqual(result.Mesh.CountFacets,14);self.assertEqual(self.doc.UndoCount,undo+1)
        self.assertIn(result,self.owner.Group);self.assertIn(result,document.history(self.doc,self.owner));document.validate(self.doc)
        self.box.Shape=Part.makeBox(35,24,20);self.doc.recompute();self.assertEqual(result.GeometryError,'')
        self.assertAlmostEqual(result.Mesh.BoundBox.XMax,40,5)
        self.doc.undo();self.doc.redo();document.validate(self.doc)
        path=Path(os.environ['PLUS_TEST_DIR'])/'Meshed.cadprt';document.save_document(self.doc,path)

    def test_mesh_colors_and_failed_compute_is_atomic(self):
        self.box.ViewObject.ShapeAppearance=[App.Material(DiffuseColor=(1,0,0))]
        settings=dict(method=0,parameters=dict(LinearDeflection=.1,AngularDeflection=.5,Relative=False),colors=True,group_colors=True)
        result=mesh_shape.save(self.doc,[(self.box,'Face1'),(self.box,'Face2')],settings)
        self.assertEqual(result.Mesh.CountFacets,4);self.assertEqual(len(result.FaceColors),4)
        before=(len(self.doc.Objects),self.doc.UndoCount)
        with self.assertRaises(ValueError):mesh_shape.save(self.doc,[(self.curve,'')],settings)
        self.assertEqual(before,(len(self.doc.Objects),self.doc.UndoCount))
        gmsh=dict(method=3,algorithm=2,min_size=0,max_size=0,executable=str(Path(os.environ['PLUS_TEST_DIR'])/'missing-gmsh.exe'))
        with self.assertRaisesRegex(ValueError,'Gmsh executable'):mesh_shape.save(self.doc,[(self.box,'')],gmsh)
        self.assertEqual(before,(len(self.doc.Objects),self.doc.UndoCount))

    def test_clone_materials_preserved_and_local_edits_survive(self):
        child=hierarchy.create_definition(self.doc,'Child');link=hierarchy.add_instance(self.owner,child)
        with document.transaction(self.doc,'Colored source'):
            body=child.newObject('PartDesign::Body','SourceBody');solid=body.newObject('PartDesign::Feature','SourceSolid');solid.Shape=Part.makeBox(10,8,6)
            solid.ViewObject.ShapeAppearance=[App.Material(DiffuseColor=(1,0,0),Transparency=.2),App.Material(DiffuseColor=(0,1,0),Transparency=.45)]
        ref=(link,body.Name+'.')
        result=derived_geometry.save(self.doc,[ref])[0]
        mats=appearance.materials(result);original=appearance.materials(solid)
        self.assertEqual([(m.DiffuseColor,m.Transparency) for m in mats],[(m.DiffuseColor,m.Transparency) for m in original])
        appearance.apply(self.owner,[(result,None)],(0,0,1),30)
        solid.Shape=Part.makeBox(12,8,6);self.doc.recompute()
        self.assertEqual(appearance.materials(result)[0].DiffuseColor[:3],(0,0,1));self.assertAlmostEqual(appearance.materials(result)[0].Transparency,.3,5)
        link.ViewObject.OverrideMaterial=True;link.ViewObject.ShapeMaterial=App.Material(DiffuseColor=(1.,1.,0.),Transparency=.35)
        overridden=derived_geometry.save(self.doc,[ref])[0]
        self.assertEqual(appearance.materials(overridden)[0].DiffuseColor[:3],(1,1,0))
        self.assertAlmostEqual(appearance.materials(overridden)[0].Transparency,.35,5)

    def test_plane_creation_defaults_and_scoped_visibility(self):
        from freecad_plus import plane_task
        origin=self.owner.Origin
        self.assertTrue(origin.Visibility)
        self.assertTrue(all(o.Visibility==(o.TypeId!='App::Plane') for o in origin.OriginFeatures))
        task=plane_task.show();self.assertTrue(all(o.Visibility for o in origin.OriginFeatures if o.TypeId=='App::Plane'))
        task.reject();self.assertTrue(all(not o.Visibility for o in origin.OriginFeatures if o.TypeId=='App::Plane'))

    def test_intersection_mixed_and_history_boundary(self):
        refs=[(self.box,''),(self.box,'Face1'),(self.curve,'Edge1')]
        shapes=intersections.section(self.owner,self.sketch,refs)
        self.assertEqual(len(shapes[0].Edges),4);self.assertEqual(len(shapes[2].Vertexes),2);self.assertFalse(shapes[2].Edges)
        later=self.owner.newObject('Part::Feature','Later');later.Shape=Part.makeBox(1,1,1);self.doc.recompute()
        for ref in ((later,''),(self.sketch,'')):
            with self.assertRaises(ValueError):intersections.canonical(self.owner,self.sketch,ref)
        child=hierarchy.create_definition(self.doc,'Other');raw=child.newObject('Part::Feature','Foreign');raw.Shape=Part.makeBox(1,1,1);self.doc.recompute()
        with self.assertRaises(ValueError):intersections.canonical(self.owner,self.sketch,(raw,''))
