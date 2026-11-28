# SPDX-License-Identifier: LGPL-2.1-or-later
import os,unittest
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui,Part
from PySide6 import QtCore,QtWidgets,QtTest,QtGui
from freecad_plus import document,editing,transforms,transform_task,mesh_task,intersection_task,intersections


class TestApprovedNative(unittest.TestCase):
    def setUp(self):
        self.before=set(App.listDocuments());Gui.Selection.clearSelection()
        self.doc=document.new_document('NativeWorkflows');self.owner=document.validate(self.doc).Definitions[0]
        editing.edit((document.validate(self.doc).Group[0],))
        with document.transaction(self.doc,'Fixture'):
            self.box=self.owner.newObject('Part::Feature','Box');self.box.Shape=Part.makeBox(20,14,10,App.Vector(0,0,-5))
            self.curve=self.owner.newObject('Part::Feature','Curve');self.curve.Shape=Part.makeCircle(5,App.Vector(5,5,0),App.Vector(0,1,0))
            self.sketch=self.owner.newObject('Sketcher::SketchObject','Section')
    def tearDown(self):
        for module in (transform_task,mesh_task,intersection_task):
            if module._active:module._active.reject()
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments())-self.before:
            try:Gui.getDocument(name).resetEdit();App.closeDocument(name)
            except Exception:pass
        QtTest.QTest.qWait(30)

    def test_all_native_buttons_bypass_classic_body_gate(self):
        for command,kind in zip(('Mirrored','LinearPattern','PolarPattern','MultiTransform'),transforms.KINDS):
            Gui.Selection.clearSelection();Gui.Selection.addSelection(self.box)
            Gui.runCommand('PartDesign_'+command);QtTest.QTest.qWait(80)
            task=transform_task._active;self.assertIsNotNone(task,command);self.assertEqual(task.kind,kind)
            self.assertEqual(task.refs,[(self.box,'')]);self.assertFalse(any(o.TypeId=='PartDesign::Body' for o in self.doc.Objects))
            path=Path(os.environ['PLUS_TEST_DIR'])/(command+'.png');task.form.grab().save(str(path));task.reject()

    def test_mesh_button_post_open_selection_and_apply(self):
        import MeshPartGui
        Gui.runCommand('MeshPart_Mesher');task=mesh_task._active
        self.assertIsNotNone(task);self.assertEqual(task.refs,[])
        self.assertTrue(task.form.tess.isVisibleTo(task.form))
        task.addSelection(self.doc.Name,self.box.Name,'Face1');self.assertEqual(task.refs,[(self.box,'')])
        task.form.surface.setChecked(True);task.addSelection(self.doc.Name,self.box.Name,'Face2')
        self.assertEqual(len(task.refs),2)
        QtTest.QTest.qWait(100)
        (Path(os.environ['PLUS_TEST_DIR'])/'mesh-layout.txt').write_text(str({
            'form':task.form.size().toTuple(),'minimum':task.form.minimumSizeHint().toTuple(),
            'tess':task.form.tess.size().toTuple(),'tess_minimum':task.form.tess.minimumSizeHint().toTuple()}))
        task.form.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'Mesh.png'))
        self.assertTrue(task.apply(),task.form.status.text());self.assertEqual(task.refs,[])
        self.assertTrue(task.form.solid.isChecked());self.assertIn(task.result,self.owner.Group)
        self.assertIn('Coloring',task.result.ViewObject.PropertiesList);document.validate(self.doc)
        feature=task.result;task.reject();mesh_task.show(feature);self.assertEqual(len(mesh_task._active.refs),2)

    def test_whole_intersection_updates_plane_and_source(self):
        intersections.apply(self.owner,self.sketch,[(self.box,'')])
        self.assertEqual(len(self.sketch.ExternalGeometry),1)
        self.assertEqual(len(self.sketch.Shape.Edges),4)
        self.box.Shape=Part.makeBox(30,14,10,App.Vector(0,0,-5));self.doc.recompute()
        self.assertAlmostEqual(self.sketch.Shape.BoundBox.XLength,30,5)
        self.sketch.Placement=App.Placement(App.Vector(0,7,0),App.Rotation(App.Vector(1,0,0),90));self.doc.recompute()
        self.assertEqual(len(self.sketch.Shape.Edges),4)
        self.assertAlmostEqual(self.sketch.Shape.BoundBox.ZLength,10,5)
        self.assertAlmostEqual(self.sketch.Shape.BoundBox.YLength,0,5)
        path=Path(os.environ['PLUS_TEST_DIR'])/'Intersection.cadprt';document.save_document(self.doc,path)
        App.closeDocument(self.doc.Name);self.doc=document.open_document(path)
        sketch=self.doc.getObject('Section');self.doc.recompute();self.assertEqual(len(sketch.Shape.Edges),4)

    def test_intersection_task_keeps_sketch_edit(self):
        Gui.activeDocument().setEdit(self.sketch.Name);QtTest.QTest.qWait(150)
        Gui.runCommand('Sketcher_Intersection');task=intersection_task._active;self.assertIsNotNone(task)
        task.addSelection(self.doc.Name,self.box.Name,'')
        task.addSelection(self.doc.Name,self.curve.Name,'Edge1');self.assertEqual(len(task.refs),2)
        self.assertIsNotNone(task.preview.node,task.status.text())
        task.form.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'IntersectionTask.png'))
        self.assertTrue(task.apply(),task.status.text());self.assertEqual(task.refs,[])
        task.reject();self.assertEqual(Gui.activeDocument().getInEdit().Object,self.sketch)
        self.assertEqual(len(self.sketch.ExternalGeometry),2)

    def test_document_tabs_at_top(self):
        mdi=Gui.getMainWindow().findChild(QtWidgets.QMdiArea)
        self.assertEqual(mdi.tabPosition(),QtWidgets.QTabWidget.North)

    def test_available_native_mesh_engines(self):
        import MeshPartGui,MeshPart,json
        Gui.runCommand('MeshPart_Mesher');task=mesh_task._active
        exercised=[];baseline={}
        for method in range(3):
            if not task.form.method.isTabEnabled(method):continue
            task.form.method.setCurrentIndex(method)
            config=task.settings()
            native=MeshPart.meshFromShape(Shape=self.box.Shape,**config['parameters'])
            baseline[method]={'parameters':config['parameters'],'native_facets':native.CountFacets}
            task.addSelection(self.doc.Name,self.box.Name,'')
            if native.CountFacets:
                self.assertTrue(task.apply(),task.form.status.text());self.assertGreater(task.result.Mesh.CountFacets,0)
            else:
                count=len(self.doc.Objects);undo=self.doc.UndoCount
                self.assertFalse(task.apply());self.assertEqual(len(self.doc.Objects),count);self.assertEqual(self.doc.UndoCount,undo)
                self.assertTrue(task.refs);task.clear()
            exercised.append(method)
        self.assertIn(0,exercised)
        (Path(os.environ['PLUS_TEST_DIR'])/'mesh-engines.txt').write_text(json.dumps(baseline,indent=2))

    def test_intersection_body_frame(self):
        with document.transaction(self.doc,'Placed source'):
            body=self.owner.newObject('PartDesign::Body','PlacedBody');body.Placement.Base=App.Vector(40,0,5)
            solid=body.newObject('PartDesign::Feature','PlacedSolid');solid.Shape=Part.makeBox(10,8,10)
            sketch=self.owner.newObject('Sketcher::SketchObject','PlacedSection');sketch.Placement.Base=App.Vector(0,0,8)
        intersections.apply(self.owner,sketch,[(solid,'')]);self.doc.recompute()
        self.assertEqual(len(sketch.Shape.Edges),4)
        self.assertAlmostEqual(sketch.Shape.BoundBox.XMin,40,5);self.assertAlmostEqual(sketch.Shape.BoundBox.XMax,50,5)

    def test_intersection_native_viewport_pick(self):
        win=Gui.getMainWindow();win.showNormal();win.resize(1500,1000)
        self.curve.Visibility=False
        Gui.activeDocument().setEdit(self.sketch.Name);QtTest.QTest.qWait(150)
        view=Gui.activeDocument().activeView();view.viewTop();view.fitAll();QtTest.QTest.qWait(250)
        Gui.runCommand('Sketcher_Intersection');task=intersection_task._active
        point=view.getPointOnScreen(App.Vector(15,10,5));widget=view.graphicsView().viewport();ratio=widget.devicePixelRatioF()
        pos=QtCore.QPoint(round(point[0]/ratio),widget.height()-1-round(point[1]/ratio))
        event=QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(pos),QtCore.QPointF(widget.mapToGlobal(pos)),QtCore.Qt.NoButton,QtCore.Qt.NoButton,QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(widget,event);QtTest.QTest.qWait(100)
        QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,pos);QtTest.QTest.qWait(150)
        self.assertTrue(task.refs,task.status.text())
        self.assertEqual(task.refs[0][0],self.box);self.assertTrue(task.refs[0][1].startswith('Face'))
