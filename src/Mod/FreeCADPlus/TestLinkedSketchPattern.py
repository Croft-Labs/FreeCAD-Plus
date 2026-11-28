# SPDX-License-Identifier: LGPL-2.1-or-later
import json,math,os,time,unittest
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui,Part,Sketcher
from PySide6 import QtCore,QtWidgets,QtTest
from freecad_plus import sketch_pattern as pattern,sketch_pattern_edit as editing,sketch_pattern_linked as linked


def options(count=5,pitch=10):
    return dict(pattern='Linear',directions='One direction',hide_spacing=False,
                d1=dict(method='Vector',x=1,y=0,mode='One dimension',count=count,spacing='Pitch',value=pitch))


class TestLinkedSketchPattern(unittest.TestCase):
    def setUp(self):
        self.before=set(App.listDocuments());self.doc=App.newDocument('LinkedSketchPattern');self.doc.UndoMode=1
        self.s=self.doc.addObject('Sketcher::SketchObject','Sketch')
        self.s.addGeometry(Part.Circle(App.Vector(2,3,0),App.Vector(0,0,1),2))
        self.doc.recompute();self.out=Path(os.environ['PLUS_TEST_DIR'])
        Gui.activateWorkbench('SketcherWorkbench')
        window=Gui.getMainWindow();window.showNormal();window.resize(1600,1200)
        QtTest.QTest.qWait(50)
    def tearDown(self):
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():Gui.activeDocument().resetEdit()
        for name in set(App.listDocuments())-self.before:App.closeDocument(name)
        QtTest.QTest.qWait(30)
    def generated(self,key):
        return [editing.identities(self.s)[t] for item in linked.records(self.s)[key]['instances'] for t in item['geometry'].values()]

    def test_copies_have_no_constraints_or_unknowns_and_follow_source(self):
        original=self.s.FullyConstrained;dof=self.s.DoF
        key=linked.save(self.s,[0],options(20));self.assertEqual(self.s.ConstraintCount,0)
        self.assertEqual(self.s.FullyConstrained,original);self.assertEqual(self.s.solve(),0)
        self.assertEqual(self.s.DoF,dof)
        self.assertTrue(all(self.s.GeometryFacadeList[i].testGeometryMode('PatternGenerated') for i in self.generated(key)))
        self.s.moveGeometry(0,3,App.Vector(7,8,0));self.doc.recompute()
        for n,i in enumerate(self.generated(key),1):
            self.assertAlmostEqual(self.s.Geometry[i].Center.x,7+10*n)
            self.assertAlmostEqual(self.s.Geometry[i].Center.y,8)
        self.s.addConstraint(Sketcher.Constraint('Radius',0,4));self.doc.recompute()
        self.assertEqual(self.s.ConstraintCount,1)
        self.assertTrue(all(abs(self.s.Geometry[i].Radius-4)<1e-7 for i in self.generated(key)))

    def test_source_constraints_and_identity_preserved_on_edit(self):
        self.s.addConstraint(Sketcher.Constraint('Radius',0,2));key=linked.save(self.s,[0],options())
        record=linked.records(self.s)[key];tags=[i['geometry'].copy() for i in record['instances']]
        undo=self.doc.UndoCount;linked.save(self.s,[0],options(7,12),key)
        self.assertEqual(self.doc.UndoCount,undo+1);self.assertEqual(self.s.ConstraintCount,1)
        self.assertEqual([i['geometry'] for i in linked.records(self.s)[key]['instances']][:4],tags)
        self.assertAlmostEqual(self.s.Geometry[self.generated(key)[0]].Center.x,14)
        self.doc.undo();self.assertEqual(self.s.GeometryCount,5);self.assertEqual(self.s.solve(),0)
        self.doc.redo();self.assertEqual(self.s.GeometryCount,7);self.assertEqual(self.s.solve(),0)

    def test_direction_reference_updates_and_circular_radial(self):
        line=self.s.addGeometry(Part.LineSegment(App.Vector(0,0,0),App.Vector(1,0,0)),True)
        self.s.addConstraint(Sketcher.Constraint('Coincident',line,1,-1,1))
        value=options(3);value['d1'].update(method='Axis or line',reference=(line,0))
        key=linked.save(self.s,[0],value)
        self.s.moveGeometry(line,2,App.Vector(0,1,0));self.doc.recompute()
        copy=self.s.Geometry[self.generated(key)[0]]
        self.assertAlmostEqual(copy.Center.x,2,places=5);self.assertAlmostEqual(copy.Center.y,13,places=5)
        value=dict(pattern='Circular',directions='Angular',center=(-1,1),angular=dict(mode='One dimension',count=4,value=360,spacing='Total angle'))
        key2=linked.save(self.s,[0],value)
        self.assertAlmostEqual(self.s.Geometry[self.generated(key2)[0]].Center.x,-3,places=5)
        self.assertAlmostEqual(self.s.Geometry[self.generated(key2)[0]].Center.y,2,places=5)

    def test_downstream_constraints_are_one_way_and_feedback_rejected(self):
        key=linked.save(self.s,[0],options(3));copy=self.generated(key)[0]
        point=self.s.addGeometry(Part.Point(App.Vector(12,3,0)))
        self.s.addConstraint(Sketcher.Constraint('Coincident',point,1,copy,3));self.doc.recompute()
        self.s.moveGeometry(0,3,App.Vector(9,10,0));self.doc.recompute()
        self.assertAlmostEqual(self.s.Geometry[point].X,19);self.assertAlmostEqual(self.s.Geometry[point].Y,10)
        bad=self.s.addConstraint(Sketcher.Constraint('Equal',0,copy))
        with self.assertRaisesRegex(ValueError,'cycle'):linked.plan(self.s)
        self.s.delConstraint(bad);self.assertEqual(self.s.solve(),0)

    def test_chained_patterns_update_in_dependency_order(self):
        first=linked.save(self.s,[0],options(3));seed=self.generated(first)[1]
        value=options(3,5);value['d1'].update(x=0,y=1)
        second=linked.save(self.s,[seed],value)
        self.s.moveGeometry(0,3,App.Vector(4,6,0));self.doc.recompute()
        self.assertEqual(self.s.ConstraintCount,0)
        self.assertAlmostEqual(self.s.Geometry[self.generated(second)[0]].Center.x,24)
        self.assertAlmostEqual(self.s.Geometry[self.generated(second)[0]].Center.y,11)
        # The second pattern uses the last copy; removing that source is refused.
        with self.assertRaises(ValueError):linked.save(self.s,[0],options(2),first)

    def test_save_reopen_and_downstream_shape(self):
        key=linked.save(self.s,[0],options());self.doc.recompute()
        identities=[f.Id for f in self.s.GeometryFacadeList]
        path=self.out/'linked-pattern.FCStd';self.doc.saveAs(str(path));App.closeDocument(self.doc.Name)
        self.doc=App.openDocument(str(path));self.s=self.doc.getObject('Sketch');self.doc.recompute()
        self.assertEqual(self.s.solve(),0);self.assertEqual([f.Id for f in self.s.GeometryFacadeList],identities)
        self.assertEqual(len(self.s.Shape.Edges),5);self.assertEqual(self.s.ConstraintCount,0)
        for wire in self.s.Shape.Wires:self.assertAlmostEqual(Part.Face(wire).Area,math.pi*4,places=5)

    def test_independent_preserves_positions_and_is_undoable(self):
        key=linked.save(self.s,[0],options());before=[g.Center for g in self.s.Geometry];undo=self.doc.UndoCount
        linked.independent(self.s,key)
        self.assertEqual(self.doc.UndoCount,undo+1);self.assertEqual(self.s.ConstraintCount,0)
        self.assertFalse(linked.records(self.s));self.assertEqual([g.Center for g in self.s.Geometry],before)
        self.s.moveGeometry(0,3,App.Vector(50,0,0));self.assertEqual(self.s.Geometry[1].Center,before[1])
        self.doc.undo();self.s.solve();self.assertIn(key,linked.records(self.s))

    def test_legacy_conversion_preserves_source_and_surviving_copies(self):
        self.s.addConstraint(Sketcher.Constraint('Radius',0,2));pattern.apply(self.s,[0],options(3),True)
        key=next(iter(linked.records(self.s)));old=linked.records(self.s)[key]
        targets={t for item in old['instances'] for t in item['geometry'].values()};undo=self.doc.UndoCount
        linked.save(self.s,[0],options(3),key)
        self.assertEqual(self.doc.UndoCount,undo+1);self.assertEqual(self.s.ConstraintCount,1)
        self.assertTrue(linked.is_linked(linked.records(self.s)[key]));self.assertTrue(targets<=editing.identities(self.s).keys())
        self.doc.undo();self.assertFalse(linked.is_linked(linked.records(self.s)[key]));self.assertGreater(self.s.ConstraintCount,1)

    def test_native_task_defaults_buttons_and_apply_reset(self):
        Gui.activeDocument().setEdit(self.s.Name);QtTest.QTest.qWait(100)
        Gui.runCommand('Sketcher_Translate');QtTest.QTest.qWait(100)
        from freecad_plus import sketch_pattern_task
        forms=[w for w in Gui.getMainWindow().findChildren(QtWidgets.QWidget) if isinstance(w,sketch_pattern_task.PatternTask) and not w.closed]
        self.assertEqual(len(forms),1);task=forms[0];self.assertTrue(task.linked)
        task.pick(0,0);task.d1.method.setCurrentIndex(2);task.sync()
        self.assertTrue(task.apply_pattern(),task.status.text())
        self.assertEqual(self.s.ConstraintCount,0);self.assertFalse(task.items.count());self.assertTrue(task.linked)
        task.set_editing(True);QtTest.QTest.qWait(50)
        self.assertEqual(task.advanced.y(),task.make_independent.y())
        window=Gui.getMainWindow()
        window.grab(QtCore.QRect(task.mapTo(window,QtCore.QPoint()),task.size())).save(str(self.out/'linked-pattern-task.png'))

    def test_growth_does_not_add_constraints(self):
        data=[]
        for n in (10,50,100):
            start=time.perf_counter();key=linked.save(self.s,[0],options(n));created=time.perf_counter()-start
            start=time.perf_counter();self.assertEqual(self.s.solve(),0);elapsed=time.perf_counter()-start
            self.assertEqual(self.s.ConstraintCount,0)
            self.assertEqual(self.s.DoF,3)
            data.append(dict(instances=n,create_seconds=created,solve_seconds=elapsed,constraints=self.s.ConstraintCount))
            linked.independent(self.s,key)
            self.s.delGeometries(list(range(1,self.s.GeometryCount)),True)
        (self.out/'linked-pattern-timings.json').write_text(json.dumps(data,indent=2))

    def test_reference_dimensions_and_unrelated_geometry(self):
        key=linked.save(self.s,[0],options(3));copy=self.generated(key)[0]
        dimension=self.s.addConstraint(Sketcher.Constraint('Radius',copy,2.))
        self.s.setDriving(dimension,False)
        line=self.s.addGeometry(Part.LineSegment(App.Vector(0,40,0),App.Vector(7,41,0)))
        self.s.addConstraint(Sketcher.Constraint('Horizontal',line))
        self.s.addConstraint(Sketcher.Constraint('Radius',0,4.));self.doc.recompute()
        self.assertEqual(self.s.solve(),0);self.assertAlmostEqual(self.s.getDatum(dimension).Value,4.)
        self.assertAlmostEqual(self.s.Geometry[line].StartPoint.y,self.s.Geometry[line].EndPoint.y)

    def test_native_deletion_guards_and_group_undo(self):
        key=linked.save(self.s,[0],options(3));before=self.s.GeometryCount
        with self.assertRaises(Exception):self.s.delGeometry(0)
        with self.assertRaises(Exception):self.s.delGeometry(self.generated(key)[0])
        self.assertEqual(self.s.GeometryCount,before);self.assertEqual(self.s.solve(),0)
        self.doc.openTransaction('Delete test pattern')
        self.s.delGeometries(self.generated(key),True);self.doc.commitTransaction()
        self.assertEqual(self.s.GeometryCount,1);self.assertFalse(linked.records(self.s))
        self.doc.undo();self.assertEqual(self.s.GeometryCount,before);self.assertEqual(self.s.solve(),0)

    def test_legacy_comparison_measurement(self):
        data=[]
        for count in (10,50):
            start=time.perf_counter();pattern.apply(self.s,[0],options(count),True)
            created=time.perf_counter()-start;start=time.perf_counter();self.assertEqual(self.s.solve(),0)
            data.append(dict(instances=count,create_seconds=created,solve_seconds=time.perf_counter()-start,
                             constraints=self.s.ConstraintCount,dof=self.s.DoF))
            self.doc.undo();self.assertEqual(self.s.GeometryCount,1)
        (self.out/'legacy-pattern-timings.json').write_text(json.dumps(data,indent=2))

    def test_exact_arcs_splines_construction_and_grid_layouts(self):
        arc=Part.ArcOfCircle(Part.Circle(App.Vector(3,4,0),App.Vector(0,0,1),3),.2,2.4)
        spline=Part.BSplineCurve();spline.interpolate([App.Vector(0,0,0),App.Vector(2,4,0),App.Vector(6,1,0)])
        self.s.addGeometry([arc,spline]);self.s.toggleConstruction(1)
        value=options(3);value.update(directions='Two directions',d2=dict(value['d1'],x=0,y=1,count=2))
        key=linked.save(self.s,[0,1,2],value)
        for instance,transform in zip(linked.records(self.s)[key]['instances'],pattern.transforms(self.s,value)):
            for src,target in instance['geometry'].items():
                index=editing.identities(self.s);a=index[src];b=index[target]
                expected=pattern.transformed(self.s.Geometry[a],transform).toShape();actual=self.s.Geometry[b].toShape()
                self.assertLess(actual.distToShape(expected)[0],1e-7)
                self.assertAlmostEqual(actual.Length,expected.Length,places=6)
                self.assertEqual(self.s.getConstruction(a),self.s.getConstruction(b))
        self.assertEqual(self.s.ConstraintCount,0)

    def test_linked_legacy_round_trip_and_cancel_advanced(self):
        key=linked.save(self.s,[0],options(3));tags=editing.owned(linked.records(self.s)[key])
        editing.update(self.s,key,[0],options(3),True)
        self.assertFalse(linked.is_linked(linked.records(self.s)[key]));self.assertGreater(self.s.ConstraintCount,0)
        linked.save(self.s,[0],options(3),key)
        self.assertEqual(self.s.ConstraintCount,0);self.assertEqual(editing.owned(linked.records(self.s)[key]),tags)
        Gui.activeDocument().setEdit(self.s.Name);Gui.runCommand('Sketcher_Translate');QtTest.QTest.qWait(100)
        task=Gui.getMainWindow().findChild(QtWidgets.QWidget,'SketchPatternPanel');undo=self.doc.UndoCount
        task.open_options();task.constraint_radio.setChecked(True);task.hide_spacing.setChecked(True)
        task.options_dialog.reject();self.assertTrue(task.linked);self.assertFalse(task.hide_spacing.isChecked())
        self.assertEqual(self.doc.UndoCount,undo);self.assertEqual(self.s.ConstraintCount,0)

    def test_unused_reference_is_not_a_dependency(self):
        line=self.s.addGeometry(Part.LineSegment(App.Vector(0,0,0),App.Vector(1,0,0)),True)
        value=options(3);value['d1']['reference']=(line,0);value['center']=(line,1)
        key=linked.save(self.s,[0],value);self.s.delGeometry(line);self.doc.recompute()
        self.assertEqual(self.s.solve(),0)
        self.s.moveGeometry(0,3,App.Vector(8,9,0))
        self.assertAlmostEqual(self.s.Geometry[self.generated(key)[0]].Center.x,18)

    def test_generated_geometry_tools_are_guarded_and_construction_follows_source(self):
        key=linked.save(self.s,[0],options(3));copy=self.generated(key)[0]
        for operation in (lambda:self.s.trim(copy,App.Vector(14,3,0)),
                          lambda:self.s.split(copy,App.Vector(14,3,0)),
                          lambda:self.s.toggleConstruction(copy)):
            with self.assertRaisesRegex(Exception,'independent'):operation()
            self.assertEqual(self.s.GeometryCount,3);self.assertEqual(self.s.ConstraintCount,0)
        self.s.toggleConstruction(0);self.doc.recompute()
        self.assertTrue(all(self.s.getConstruction(i) for i in range(3)))
        linked.independent(self.s,key);self.s.toggleConstruction(copy)
        self.assertFalse(self.s.getConstruction(copy))

    def test_linked_layout_edits(self):
        import TestSketchPattern as fixture
        cases=[fixture.linear(d1=fixture.extent(mode='Symmetric',count=5,value=3.175,unit='in')),
               fixture.linear(d1=fixture.extent(mode='Two dimensions',count=3,count2=2,value=10,value2=7,reverse=True)),
               fixture.circular(directions='Angular + radial',angular=fixture.extent(count=3,spacing='Angular pitch',value=30,reverse=True),
                                radial=fixture.extent(count=2,value=5,reference=(0,3)))]
        key=linked.save(self.s,[0],options(3))
        for value in cases:
            linked.save(self.s,[0],value,key);self.assertEqual(self.s.ConstraintCount,0)
            self.assertEqual(self.s.solve(),0)
            for i,transform in zip(self.generated(key),pattern.transforms(self.s,value)):
                self.assertLess((self.s.Geometry[i].Center-pattern.transformed(self.s.Geometry[0],transform).Center).Length,1e-6)

    def test_native_group_icon_opens_edit_and_detaches(self):
        from pivy import coin
        from PySide6 import QtGui
        key=linked.save(self.s,[0],options(4))
        Gui.activeDocument().setEdit(self.s.Name);view=Gui.activeDocument().activeView()
        view.viewTop();view.fitAll();QtTest.QTest.qWait(1000)
        view.setCamera('#Inventor V2.1 ascii\nOrthographicCamera { position 17 3 87 orientation 0 0 1 0 nearDistance 1 farDistance 200 focalDistance 87 height 45 }')
        QtTest.QTest.qWait(100)
        search=coin.SoSearchAction();search.setName('ConstraintGroup');search.setSearchingAll(True);search.apply(view.getSceneGraph())
        self.assertIsNotNone(search.getPath());node=search.getPath().getTail()
        self.assertEqual(node.getNumChildren(),1,'One display icon and zero solver constraints')
        point=node.getChild(0).getChild(1).getField('abPos').getValue()
        screen=view.getPointOnScreen(App.Vector(*point));widget=view.graphicsView().viewport();ratio=widget.devicePixelRatioF()
        seed=QtCore.QPoint(round(screen[0]/ratio),widget.height()-1-round(screen[1]/ratio));found=None
        target='Edge'+str(self.generated(key)[-1]+1)
        view.saveImage(str(self.out/'linked-icon-before.png'),1200,800,'Current')
        for dy in sorted(range(-25,26,3),key=abs):
            for dx in sorted(range(-25,26,3),key=abs):
                position=seed+QtCore.QPoint(dx,dy)
                event=QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(position),QtCore.QPointF(widget.mapToGlobal(position)),QtCore.Qt.NoButton,QtCore.Qt.NoButton,QtCore.Qt.NoModifier)
                QtWidgets.QApplication.sendEvent(widget,event)
                if target in Gui.Selection.getPreselection().SubElementNames:
                    QtTest.QTest.qWait(QtWidgets.QApplication.doubleClickInterval()+10)
                    QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,pos=position)
                    selected=Gui.Selection.getSelectionEx()
                    if selected and len(selected[0].SubElementNames)==3:found=position;break
            if found is not None:break
        self.assertIsNotNone(found,'Linked icon has a viewport hover hit')
        self.assertEqual(len(Gui.Selection.getSelectionEx()[0].SubElementNames),3)
        QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,pos=found);QtTest.QTest.qWait(150)
        task=Gui.getMainWindow().findChild(QtWidgets.QWidget,'SketchPatternPanel')
        self.assertIsNotNone(task);self.assertEqual(task.edit_group,key);self.assertTrue(task.linked)
        self.assertEqual(task.advanced.y(),task.make_independent.y())
        window=Gui.getMainWindow()
        window.grab(QtCore.QRect(task.mapTo(window,QtCore.QPoint()),task.size())).save(str(self.out/'linked-pattern-edit.png'))
        task.make_independent.click();task.independent_dialog.reject();self.assertIn(key,linked.records(self.s))
        task.make_independent.click();task.independent_dialog.accept();self.assertFalse(linked.records(self.s))
        self.assertEqual(self.s.ConstraintCount,0);self.assertFalse(task.items.count())
        self.doc.undo();self.assertIn(key,linked.records(self.s))

    def test_native_drag_source_updates_copies_without_accumulation(self):
        from PySide6 import QtGui
        key=linked.save(self.s,[0],options(3))
        Gui.activeDocument().setEdit(self.s.Name);view=Gui.activeDocument().activeView()
        view.viewTop();view.fitAll();QtTest.QTest.qWait(150)
        widget=view.graphicsView().viewport();ratio=widget.devicePixelRatioF()
        def screen(p):
            value=view.getPointOnScreen(p)
            return QtCore.QPoint(round(value[0]/ratio),widget.height()-1-round(value[1]/ratio))
        def motion(position,buttons=QtCore.Qt.NoButton):
            QtWidgets.QApplication.sendEvent(widget,QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(position),
                QtCore.QPointF(widget.mapToGlobal(position)),QtCore.Qt.NoButton,buttons,QtCore.Qt.NoModifier))
            QtWidgets.QApplication.processEvents()
        start=screen(self.s.Geometry[0].Center);motion(start)
        self.assertIn('Vertex1',Gui.Selection.getPreselection().SubElementNames)
        QtTest.QTest.mousePress(widget,QtCore.Qt.LeftButton,pos=start)
        for point in (App.Vector(4,4,0),App.Vector(6,5,0),App.Vector(8,7,0)):
            motion(screen(point),QtCore.Qt.LeftButton)
        QtTest.QTest.mouseRelease(widget,QtCore.Qt.LeftButton,pos=screen(App.Vector(8,7,0)))
        QtTest.QTest.qWait(100)
        self.assertLess((self.s.Geometry[0].Center-App.Vector(8,7,0)).Length,.2)
        for n,i in enumerate(self.generated(key),1):
            self.assertLess((self.s.Geometry[i].Center-self.s.Geometry[0].Center-App.Vector(10*n,0,0)).Length,1e-5)
        self.assertEqual(self.s.ConstraintCount,0)
