# SPDX-License-Identifier: LGPL-2.1-or-later
"""Existing sketch pattern editing, identity, rollback and native task acceptance."""
import copy
import json
import os
import time
import unittest
from pathlib import Path
import FreeCAD as App
import Part
import Sketcher
from PySide6 import QtOpenGLWidgets
import TestSketchPattern as fixture
from freecad_plus import sketch_pattern as pattern,sketch_pattern_edit as editing


def persisted(obj):
    import io,zipfile
    with zipfile.ZipFile(io.BytesIO(obj.dumpContent())) as archive:
        return {name:archive.read(name) for name in archive.namelist()}


class TestPatternEditing(unittest.TestCase):
    setUp=fixture.TestPatternGeometry.setUp
    tearDown=fixture.TestPatternGeometry.tearDown

    def seed(self,line=False):
        self.s.addGeometry(Part.LineSegment(App.Vector(20,3,0),App.Vector(24,3,0)) if line else
                           Part.Circle(App.Vector(20,3,0),App.Vector(0,0,1),2))
        self.s.addConstraint(Sketcher.Constraint('Distance' if line else 'Diameter',0,4.))

    def group(self):return next(c.PatternGroup for c in self.s.Constraints if c.PatternGroup)

    def test_grid_counts_directions_identity_undo_and_save(self):
        self.seed(True);s=self.s;before=s.DoF
        options=fixture.linear(directions='Two directions',d1=fixture.extent(count=4),d2=fixture.extent(count=3,reference=(-2,0)))
        pattern.apply(s,[0],options,True);group=self.group()
        record,ids,current=editing.load(s,group);old={tuple(x['slot']):x['geometry'] for x in record['instances']}
        options['d1'].update(count=5,value=7,method='Vector',x=1,y=1)
        options['d2'].update(count=2,value=11)
        count=self.doc.UndoCount
        result=editing.update(s,group,ids,options,True)
        self.assertEqual(self.doc.UndoCount,count+1);self.assertEqual(len(result),9)
        self.assertEqual(s.solve(),0);self.assertEqual(s.DoF,before)
        updated,ids,current=editing.load(s,group)
        self.assertEqual(self.group(),group)
        for item in updated['instances']:
            if tuple(item['slot']) in old:self.assertEqual(item['geometry'],old[tuple(item['slot'])])
        vector=s.Geometry[0].EndPoint-s.Geometry[0].StartPoint
        for geo,transform in zip(result,pattern.transforms(s,options)):
            self.assertLess((s.Geometry[geo].StartPoint-s.Geometry[0].StartPoint-transform[1]).Length,1e-5)
            self.assertLess((s.Geometry[geo].EndPoint-s.Geometry[geo].StartPoint-vector).Length,1e-5)
        self.doc.undo();self.assertEqual(len(editing.load(s,group)[0]['instances']),11)
        self.doc.redo();self.assertEqual(len(editing.load(s,group)[0]['instances']),9)
        if os.environ.get('PLUS_TEST_DIR'):
            self.doc.saveAs(str(Path(os.environ['PLUS_TEST_DIR'])/'edited-pattern.FCStd'))

    def test_total_units_refresh_and_symmetric_negative_extents(self):
        self.seed();s=self.s
        options=fixture.linear(d1=fixture.extent(mode='Two dimensions',count=4,count2=3,value=12,value2=5,spacing='Total distance',unit='in'))
        pattern.apply(s,[0],options,True);group=self.group()
        driver=next(i for i,c in enumerate(s.Constraints) if c.PatternDriver=='Direction 1 pitch (+)')
        s.setDatum(driver,App.Units.Quantity('0.25 in'));self.doc.recompute()
        record,ids,current=editing.load(s,group)
        self.assertAlmostEqual(current['d1']['value'],6.35*3)
        self.assertEqual(current['d1']['unit'],'in')
        current['d1'].update(mode='Symmetric',count=5,spacing='Pitch',value=3.175)
        copies=editing.update(s,group,ids,current,True)
        self.assertEqual(len(copies),4);self.assertEqual(s.solve(),0)
        offsets=sorted(round(s.Geometry[i].Center.x-s.Geometry[0].Center.x,6) for i in copies)
        self.assertEqual(offsets,[-6.35,-3.175,3.175,6.35])

    def test_angular_radial_edit_and_mode_change(self):
        self.seed();s=self.s
        options=fixture.circular(directions='Angular + radial',angular=fixture.extent(spacing='Angular pitch',count=3,value=30),
                                 radial=fixture.extent(count=2,value=5,reference=(0,3)))
        pattern.apply(s,[0],options,True);group=self.group();record,ids,current=editing.load(s,group)
        current['angular'].update(count=4,value=40,reverse=True);current['radial'].update(count=3,value=6)
        copies=editing.update(s,group,ids,current,True)
        self.assertEqual(len(copies),11);self.assertEqual(s.solve(),0)
        for i,transform in zip(copies,pattern.transforms(s,current)):
            expected=pattern.transformed(s.Geometry[0],transform)
            self.assertLess((s.Geometry[i].Center-expected.Center).Length,1e-5)
        copies=editing.update(s,group,ids,fixture.linear(d1=fixture.extent(reference=(-2,0),reverse=True,count=4)),True)
        self.assertEqual(len(copies),3);self.assertEqual(s.solve(),0)

    def test_unrelated_geometry_and_constraint_dependency_rollback(self):
        self.seed();s=self.s
        copies=pattern.apply(s,[0],fixture.linear(d1=fixture.extent(count=4)),True);group=self.group()
        unrelated=s.addGeometry(Part.LineSegment(App.Vector(0,40,0),App.Vector(3,40,0)))
        s.addConstraint(Sketcher.Constraint('Horizontal',unrelated));tag=s.Geometry[unrelated].Tag
        s.addConstraint(Sketcher.Constraint('DistanceX',copies[-1],3,50.))
        snapshot=[persisted(c) for c in s.Constraints];geometry=[g.Tag for g in s.Geometry];undo=self.doc.UndoCount
        with self.assertRaisesRegex(ValueError,'other constraints'):
            editing.update(s,group,[0],fixture.linear(d1=fixture.extent(count=3)),True)
        self.assertEqual([persisted(c) for c in s.Constraints],snapshot)
        self.assertEqual([g.Tag for g in s.Geometry],geometry);self.assertEqual(self.doc.UndoCount,undo)
        s.delConstraint(s.ConstraintCount-1)
        editing.update(s,group,[0],fixture.linear(d1=fixture.extent(count=3)),True)
        index=next(i for i,g in enumerate(s.Geometry) if g.Tag==tag)
        self.assertTrue(any(c.Type=='Horizontal' and c.First==index and not c.PatternGroup for c in s.Constraints))

    def test_recover_older_grouped_linear_and_circular(self):
        self.seed();s=self.s
        for options in (fixture.linear(directions='Two directions',d1=fixture.extent(count=4),d2=fixture.extent(count=3,reference=(-2,0))),
                        fixture.circular(directions='Angular + radial',angular=fixture.extent(count=4,spacing='Angular pitch',value=30),radial=fixture.extent(count=3,value=5,reference=(0,3)))):
            pattern.apply(s,[0],options,True);group=self.group();s.PatternDefinitions={}
            record,ids,current=editing.load(s,group)
            self.assertTrue(record['recovered']);self.assertEqual(len(record['instances']),11)
            editing.update(s,group,ids,current,True);self.assertEqual(s.solve(),0)
            self.doc.undo();self.doc.undo()
            # Undo recipe clearing is not a transaction; pattern creation is.
            if s.GeometryCount!=1:
                self.doc.undo()

    def test_grid12_edit_timing(self):
        self.seed(True);s=self.s
        options=fixture.linear(directions='Two directions',d1=fixture.extent(count=12),d2=fixture.extent(count=12,reference=(-2,0)))
        pattern.apply(s,[0],options,True);group=self.group();options['d1']['value']=13
        start=time.perf_counter();editing.update(s,group,[0],options,True);elapsed=time.perf_counter()-start
        self.assertLess(elapsed,20.)
        self.assertEqual((s.GeometryCount,s.ConstraintCount),(430,1145));self.assertEqual(s.solve(),0)
        self.assertEqual(sum(c.Type=='Equal' and c.First==0 for c in s.Constraints),143)
        if os.environ.get('PLUS_TEST_DIR'):
            (Path(os.environ['PLUS_TEST_DIR'])/'grid12-edit-timing.json').write_text(json.dumps(dict(seconds=elapsed)))

    def test_legacy_reversed_grid_and_expression_guard(self):
        self.seed();s=self.s
        pattern.apply(s,[0],fixture.linear(d1=fixture.extent(count=4,reverse=True)),True)
        group=self.group();s.PatternDefinitions={}
        record,ids,current=editing.load(s,group)
        before={i['geometry'][record['inputs'][0]] for i in record['instances']}
        editing.update(s,group,ids,current,True)
        after=editing.load(s,group)[0]
        self.assertEqual(before,{i['geometry'][after['inputs'][0]] for i in after['instances']})
        driver=next(i for i,c in enumerate(s.Constraints) if c.PatternDriver)
        s.setExpression('Constraints[%d]' % driver,'7 mm');self.doc.recompute()
        snapshot=[persisted(c) for c in s.Constraints]
        with self.assertRaisesRegex(ValueError,'expression'):
            editing.update(s,group,ids,fixture.linear(),True)
        self.assertEqual(snapshot,[persisted(c) for c in s.Constraints])

    def test_reference_and_other_pattern_survive_geometry_renumbering(self):
        self.seed();s=self.s
        pattern.apply(s,[0],fixture.linear(d1=fixture.extent(count=5)),True);group=self.group()
        source=s.addGeometry(Part.Circle(App.Vector(50,30,0),App.Vector(0,0,1),1))
        source_tag=s.Geometry[source].Tag
        pattern.apply(s,[source],fixture.linear(d1=fixture.extent(count=3,reference=(-2,0))),True)
        second=next(c.PatternGroup for c in s.Constraints if c.PatternGroup and c.PatternGroup!=group)
        editing.update(s,group,[0],fixture.linear(d1=fixture.extent(count=3)),True)
        record,ids,options=editing.load(s,second)
        self.assertEqual(s.Geometry[ids[0]].Tag,source_tag)
        options['d1']['count']=4
        editing.update(s,second,ids,options,True)
        self.assertEqual(s.solve(),0);self.assertEqual(len(editing.load(s,second)[0]['instances']),3)

    def test_rebuild_failure_restores_existing_pattern(self):
        from unittest.mock import patch
        self.seed();s=self.s
        copies=pattern.apply(s,[0],fixture.linear(d1=fixture.extent(count=3)),True);group=self.group()
        self.assertEqual(s.solve(),0)
        before=[persisted(c) for c in s.Constraints];geometry=[persisted(g) for g in s.Geometry]
        definition=dict(s.PatternDefinitions);undo=self.doc.UndoCount
        def fail(*args,**kwargs):
            self.assertFalse(any(c.PatternGroup==group for c in s.Constraints))
            self.assertLess(s.GeometryCount,len(geometry))
            raise RuntimeError('Rebuild failed after removing the previous chains')
        with patch.object(pattern,'apply',side_effect=fail):
            with self.assertRaisesRegex(RuntimeError,'Rebuild failed'):
                editing.update(s,group,[0],fixture.linear(d1=fixture.extent(count=3,value=13)),True)
        self.assertEqual([persisted(c) for c in s.Constraints],before)
        self.assertEqual([persisted(g) for g in s.Geometry],geometry)
        self.assertEqual(dict(s.PatternDefinitions),definition);self.assertEqual(self.doc.UndoCount,undo)
        self.assertEqual(s.solve(),0)

    def test_whole_sketch_extrusion_survives_count_edit(self):
        self.seed();s=self.s
        pattern.apply(s,[0],fixture.linear(d1=fixture.extent(count=3)),True);group=self.group()
        solid=self.doc.addObject('Part::Extrusion','Extrusion');solid.Base=s
        solid.Dir=App.Vector(0,0,5);solid.Solid=True;self.doc.recompute()
        original=solid.Shape.Volume
        editing.update(s,group,[0],fixture.linear(d1=fixture.extent(count=4)),True)
        self.doc.recompute()
        self.assertTrue(solid.Shape.isValid());self.assertAlmostEqual(solid.Shape.Volume,original*4/3,places=5)

    def test_external_direction_recipe_roundtrip(self):
        self.seed();s=self.s
        base=self.doc.addObject('PartDesign::Feature','Reference')
        base.Shape=Part.makeCompound([Part.makeLine(App.Vector(0,0,0),App.Vector(1,1,0)),
                                     Part.makeLine(App.Vector(0,10,0),App.Vector(0,20,0))])
        self.doc.recompute();s.addExternal(base.Name,'Edge1');s.addExternal(base.Name,'Edge2')
        options=fixture.linear(d1=fixture.extent(reference=(-4,0)))
        pattern.apply(s,[0],options,True);group=self.group()
        record,ids,current=editing.load(s,group)
        self.assertEqual(current['d1']['reference'],(-4,0))
        current['d1']['count']=4;copies=editing.update(s,group,ids,current,True)
        self.assertEqual(s.solve(),0)
        self.assertAlmostEqual(s.Geometry[copies[-1]].Center.y-s.Geometry[0].Center.y,30.)
        if os.environ.get('PLUS_TEST_DIR'):
            self.doc.saveAs(str(Path(os.environ['PLUS_TEST_DIR'])/'external-pattern.FCStd'))

    def test_save_close_reopen_definition_and_visibility(self):
        import tempfile
        self.seed(True);s=self.s
        pattern.apply(s,[0],fixture.linear(d1=fixture.extent(count=4),hide_spacing=True),True)
        group=self.group();record,ids,options=editing.load(s,group)
        with tempfile.TemporaryDirectory() as directory:
            path=str(Path(directory)/'pattern.FCStd');self.doc.saveAs(path)
            App.closeDocument(self.doc.Name);self.doc=App.openDocument(path);self.s=self.doc.Sketch;s=self.s
            reopened,newids,restored=editing.load(s,group)
            self.assertEqual(reopened,record);self.assertEqual(newids,ids)
            self.assertTrue(restored['hide_spacing'])
            restored['d1']['count']=5;editing.update(s,group,newids,restored,True)
            self.assertEqual(s.solve(),0);self.assertTrue(pattern.chain_is_hidden(s))
            self.assertEqual(len(s.PatternSpacingTags),8)


class TestPatternEditingTask(unittest.TestCase):
    setUp=fixture.TestPatternTask.setUp
    tearDown=fixture.TestPatternTask.tearDown

    def seed(self):
        self.s.addConstraint(Sketcher.Constraint('Distance',0,4.))
        options=fixture.linear(directions='Two directions',d1=fixture.extent(count=4,value=10),d2=fixture.extent(count=3,value=12,reference=(-2,0)))
        pattern.apply(self.s,[0],options,True)
        self.group=next(c.PatternGroup for c in self.s.Constraints if c.PatternGroup)
        self.QtTest.QTest.qWait(100)

    def open_row(self):
        from PySide6 import QtCore
        rows=self.win.findChild(self.QtWidgets.QListWidget,'listWidgetConstraints')
        row=next(rows.item(i) for i in range(rows.count()) if not rows.item(i).isHidden() and rows.item(i).text().startswith('Pattern'))
        rows.scrollToItem(row)
        rows.setFocus()
        self.QtTest.QTest.mouseClick(rows.viewport(),QtCore.Qt.LeftButton,pos=rows.visualItemRect(row).center())
        self.QtTest.QTest.mouseDClick(rows.viewport(),QtCore.Qt.LeftButton,pos=rows.visualItemRect(row).center())
        self.QtTest.QTest.qWait(200)
        self.p=self.win.findChild(self.QtWidgets.QWidget,'SketchPatternPanel')
        self.assertIsNotNone(self.p)
        self.assertEqual(self.p.edit_group,self.group)
        self.assertTrue(self.p.apply.isEnabled(),self.p.status.text())

    def test_list_reopens_populated_cancel_done_apply_and_undo(self):
        from PySide6 import QtCore
        self.seed();count=self.doc.UndoCount
        constraints=[persisted(c) for c in self.s.Constraints];facades=[persisted(f.Geometry) for f in self.s.GeometryFacadeList]
        self.open_row()
        self.assertEqual((self.p.d1.count.value(),self.p.d2.count.value()),(4,3))
        self.assertEqual((self.p.d1.value.value(),self.p.d2.value.value()),(10,12))
        self.assertEqual(self.p.geometry_ids(),[0]);self.assertIn('X axis',self.p.d1.reference.text())
        self.assertTrue(all(w.isHidden() for w,_ in self.sections))
        self.assertEqual(len(self.p.get_hidden_geometry()),33)
        self.p.d1.count.setValue(5);self.p.d1.value.setValue(8)
        self.assertEqual(len(self.p.get_preview()),14)
        # Inspect the actual native drawing nodes, not just Python preview data.
        from pivy import coin
        def node(name):
            search=coin.SoSearchAction();search.setName(name);search.setSearchingAll(True)
            search.apply(self.Gui.activeDocument().activeView().getSceneGraph())
            return search.getPath().getTail()
        lengths=list(node('EditCurveLineSet').numVertices.getValues())
        points=list(node('EditCurvesCoordinate').point.getValues())
        self.assertEqual(len(lengths),14)
        offset=0
        for length,g in zip(lengths,self.p.get_preview()):
            self.assertAlmostEqual(points[offset][0],g.StartPoint.x,places=4)
            self.assertAlmostEqual(points[offset][1],g.StartPoint.y,places=4)
            self.assertAlmostEqual(points[offset+length-1][0],g.EndPoint.x,places=4)
            offset+=length
        self.assertEqual(self.doc.UndoCount,count)
        self.assertEqual([persisted(c) for c in self.s.Constraints],constraints)
        self.assertEqual([persisted(f.Geometry) for f in self.s.GeometryFacadeList],facades)
        if os.environ.get('PLUS_TEST_DIR'):
            out=Path(os.environ['PLUS_TEST_DIR'])
            # Grab the painted ancestor so transparent task children retain its background.
            self.win.grab(QtCore.QRect(self.p.mapTo(self.win,QtCore.QPoint()),self.p.size())).save(str(out/'pattern-edit-panel.png'))
            from TestComponentFading import capture
            self.Gui.activeDocument().activeView().viewTop();self.Gui.activeDocument().activeView().fitAll()
            capture(self.Gui.activeDocument().activeView(),out/'pattern-edit-preview.png')
        self.QtTest.QTest.keyClick(self.p.d1.count,QtCore.Qt.Key_Escape);self.QtTest.QTest.qWait(150)
        self.assertEqual([persisted(c) for c in self.s.Constraints],constraints)
        self.assertEqual([persisted(f.Geometry) for f in self.s.GeometryFacadeList],facades)
        self.open_row();self.p.d1.count.setValue(5);self.p.done.click();self.QtTest.QTest.qWait(150)
        self.assertEqual(len(editing.load(self.s,self.group)[0]['instances']),14)
        self.assertEqual(self.doc.UndoCount,count+1)
        self.doc.undo();self.QtTest.QTest.qWait(100)
        self.assertEqual(len(editing.load(self.s,self.group)[0]['instances']),11)
        self.open_row();self.p.d2.count.setValue(2);self.p.apply.click();self.QtTest.QTest.qWait(100)
        self.assertFalse(self.p.edit_group);self.assertEqual(self.p.items.count(),0)
        self.assertEqual(len(editing.load(self.s,self.group)[0]['instances']),7)
        self.p.done.click();self.QtTest.QTest.qWait(100)

    def test_viewport_icon_double_click(self):
        from PySide6 import QtCore,QtGui,QtWidgets,QtTest
        from pivy import coin
        self.seed();view=self.Gui.activeDocument().activeView();view.viewTop();view.fitAll();QtTest.QTest.qWait(100)
        search=coin.SoSearchAction();search.setName('ConstraintGroup');search.setSearchingAll(True);search.apply(view.getSceneGraph())
        node=search.getPath().getTail()
        head=next(i for i,c in enumerate(self.s.Constraints) if c.PatternGroup==self.group)
        translation=node.getChild(head).getChild(1)
        point=translation.getField('abPos').getValue()
        screen=view.getPointOnScreen(App.Vector(*point));widget=view.graphicsView().viewport();ratio=widget.devicePixelRatioF()
        seed=QtCore.QPoint(round(screen[0]/ratio),widget.height()-1-round(screen[1]/ratio))
        target='Constraint'+str(head+1);found=None
        for dy in range(-18,19,3):
            for dx in range(-18,19,3):
                position=seed+QtCore.QPoint(dx,dy)
                event=QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(position),QtCore.QPointF(widget.mapToGlobal(position)),QtCore.Qt.NoButton,QtCore.Qt.NoButton,QtCore.Qt.NoModifier)
                QtWidgets.QApplication.sendEvent(widget,event)
                if target in self.Gui.Selection.getPreselection().SubElementNames:found=position;break
            if found is not None:break
        self.assertIsNotNone(found,'Pattern icon must have a real viewport hover hit')
        QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,pos=found)
        QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,pos=found)
        QtTest.QTest.qWait(200)
        panel=self.win.findChild(QtWidgets.QWidget,'SketchPatternPanel')
        self.assertIsNotNone(panel);self.assertEqual(panel.edit_group,self.group)
        self.assertEqual(panel.d1.count.value(),4)
        panel.done.click();QtTest.QTest.qWait(100)
