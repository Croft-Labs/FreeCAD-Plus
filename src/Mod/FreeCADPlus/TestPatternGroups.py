# SPDX-License-Identifier: LGPL-2.1-or-later
"""Pattern groups preserve solver relationships, editing and native display."""
import json
import os
import time
import unittest
from pathlib import Path
import FreeCAD as App
import Part
import Sketcher
from PySide6 import QtOpenGLWidgets
import TestSketchPattern as fixtures
from freecad_plus import sketch_pattern as pattern


def visible(c):
    import io
    import zipfile
    import xml.etree.ElementTree as ET
    with zipfile.ZipFile(io.BytesIO(c.dumpContent())) as archive:
        root=ET.fromstring(archive.read(archive.namelist()[0]))
    node=next(node for node in root.iter() if 'IsVisible' in node.attrib)
    return node.get('IsVisible') == '1'


class TestPatternGroups(unittest.TestCase):
    setUp = fixtures.TestPatternGeometry.setUp
    tearDown = fixtures.TestPatternGeometry.tearDown

    def line(self, projected=False, horizontal=False):
        self.s.addGeometry(Part.LineSegment(App.Vector(5,3,0),App.Vector(9,3,0)))
        if horizontal: self.s.addConstraint(Sketcher.Constraint('Horizontal',0))
        self.s.addConstraint(Sketcher.Constraint('DistanceX' if projected else 'Distance',0,4.))

    def test_fixed_length_grid12_no_fallback_and_edit(self):
        self.line();s=self.s;before=s.DoF
        options=fixtures.linear(directions='Two directions',d1=fixtures.extent(count=12),
                                d2=fixtures.extent(count=12,reference=(-2,0)))
        # The previously expensive binary isolation must never run on this grid.
        started=time.perf_counter()
        copies=pattern.apply(s,[0],options,True)
        elapsed=time.perf_counter()-started
        self.assertLess(elapsed,20.,'12 by 12 fixed line grid regressed')
        self.assertEqual((s.GeometryCount,s.ConstraintCount),(430,1145))
        self.assertEqual(s.solve(),0);self.assertEqual(s.DoF,before)
        cs=s.Constraints;group={c.PatternGroup for c in cs[1:]}
        self.assertEqual(len(group),1);self.assertNotIn('',group)
        self.assertEqual(cs[0].PatternGroup,'')
        self.assertEqual(sum(c.Type=='Equal' and c.First==0 for c in cs),143)
        self.assertEqual(sum(c.Type=='Parallel' and c.First==0 for c in cs),143)
        self.assertEqual(sum(s.getConstruction(i) for i in range(s.GeometryCount)),286)
        drivers=[i for i,c in enumerate(cs) if c.PatternDriver]
        self.assertEqual(len(drivers),2)
        s.setDatum(0,App.Units.Quantity('6 mm'))
        s.setDatum(drivers[0],App.Units.Quantity('11 mm'))
        s.setDatum(drivers[1],App.Units.Quantity('13 mm'))
        angle=s.addConstraint(Sketcher.Constraint('Angle',0,0.5))
        self.doc.recompute();self.assertEqual(s.solve(),0)
        origin=s.Geometry[0].StartPoint;vector=s.Geometry[0].EndPoint-origin
        self.assertAlmostEqual(vector.y,6.*__import__('math').sin(0.5),places=5)
        for n,i in enumerate([0]+copies):
            g=s.Geometry[i]
            self.assertLess((g.EndPoint-g.StartPoint-vector).Length,1e-5)
            self.assertLess((g.StartPoint-origin-App.Vector(n//12*11,n%12*13,0)).Length,1e-5)
        for c in s.Constraints:
            if c.Type=='Coincident':
                self.assertLess((s.getPoint(c.First,c.FirstPos)-s.getPoint(c.Second,c.SecondPos)).Length,1e-5)
        s.delConstraint(angle);self.assertEqual(s.solve(),0);self.assertEqual(s.DoF,before)
        if os.environ.get('PLUS_TEST_DIR'):
            out=Path(os.environ['PLUS_TEST_DIR'])
            self.doc.saveAs(str(out/'fixed-line-grid12.FCStd'))
            (out/'fixed-line-grid12-timing.json').write_text(json.dumps(dict(seconds=elapsed,
                geometries=s.GeometryCount,constraints=s.ConstraintCount,helpers=286,equal_sizes=143,drivers=2)))

    def test_hide_group_visibility_and_renumber_save(self):
        self.line();pattern.apply(self.s,[0],fixtures.linear(),True)
        identity=self.s.Constraints[1].PatternGroup
        for hidden in (True,False):
            pattern.set_chain_hidden(self.s,hidden)
            self.assertEqual(pattern.chain_is_hidden(self.s),hidden)
            self.assertTrue(all(visible(c)==(not hidden) for c in self.s.Constraints if c.PatternGroup))
            self.assertTrue(visible(self.s.Constraints[0]))
        self.s.setVisibility(1,False)
        self.assertTrue(all(not visible(c) for c in self.s.Constraints if c.PatternGroup))
        self.s.setVisibility([2],True)
        self.assertTrue(all(visible(c) for c in self.s.Constraints if c.PatternGroup))
        self.s.delConstraint(0)
        self.assertTrue(all(c.PatternGroup==identity for c in self.s.Constraints))
        self.assertEqual(self.s.solve(),0)
        if os.environ.get('PLUS_TEST_DIR'):
            path=Path(os.environ['PLUS_TEST_DIR'])/'group-renumber.FCStd'
            self.doc.saveAs(str(path));name=self.doc.Name;App.closeDocument(name)
            self.doc=App.openDocument(str(path));self.s=self.doc.getObject('Sketch')
            self.assertTrue(all(c.PatternGroup==identity for c in self.s.Constraints))
            self.assertEqual(self.s.solve(),0)

    def test_second_pattern_separate_and_undo(self):
        self.line();copies=pattern.apply(self.s,[0],fixtures.linear(),True)
        first={c.PatternGroup for c in self.s.Constraints if c.PatternGroup}
        pattern.apply(self.s,[copies[-1]],fixtures.linear(d1=fixtures.extent(reference=(-2,0))),True)
        self.assertEqual(len({c.PatternGroup for c in self.s.Constraints if c.PatternGroup}),2)
        self.doc.undo()
        self.assertEqual({c.PatternGroup for c in self.s.Constraints if c.PatternGroup},first)
        self.doc.redo();self.assertEqual(self.s.solve(),0)

    def test_projected_length_requires_direction_and_radial_fixed_line(self):
        self.line(projected=True)
        self.assertEqual(pattern._fixed_length_lines(self.s,[0]),set())
        self.s.addConstraint(Sketcher.Constraint('Horizontal',0))
        self.assertEqual(pattern._fixed_length_lines(self.s,[0]),{0})
        before=self.s.DoF
        pattern.apply(self.s,[0],fixtures.circular(directions='Radial',
            radial=fixtures.extent(reference=(0,1),count=5,value=8)),True)
        self.assertEqual(self.s.solve(),0);self.assertEqual(self.s.DoF,before)
        self.assertEqual(len([c for c in self.s.Constraints if c.PatternDriver]),1)

    def test_angular_radial_drivers(self):
        self.s.addGeometry(Part.Circle(App.Vector(20,0,0),App.Vector(0,0,1),2))
        self.s.addConstraint(Sketcher.Constraint('Diameter',0,4.))
        pattern.apply(self.s,[0],fixtures.circular(directions='Angular + radial',
            angular=fixtures.extent(spacing='Angular pitch',value=30),
            radial=fixtures.extent(reference=(0,3),count=3,value=5)),True)
        self.assertEqual(self.s.solve(),0)
        self.assertEqual({c.PatternDriver for c in self.s.Constraints if c.PatternDriver},
                         {'Angular pitch','Radial pitch'})
        pattern.set_chain_hidden(self.s,True)
        self.assertTrue(all(not visible(c) for c in self.s.Constraints if c.PatternGroup))


class TestPatternElements(unittest.TestCase):
    setUp = fixtures.TestPatternTask.setUp
    tearDown = fixtures.TestPatternTask.tearDown

    def listing(self):
        return self.win.findChild(self.QtWidgets.QListWidget,'listWidgetElements')

    def groups(self):
        from PySide6 import QtCore
        rows=self.listing()
        return [rows.item(i) for i in range(rows.count()) if rows.item(i).data(QtCore.Qt.UserRole+1)]

    def seed(self,n=4,hidden=True):
        self.s.addConstraint(Sketcher.Constraint('Diameter',1,4.))
        options=fixtures.linear(directions='Two directions',hide_spacing=hidden,
            d1=fixtures.extent(count=n),d2=fixtures.extent(count=n,reference=(-2,0)))
        pattern.apply(self.s,[1],options,True)
        self.QtTest.QTest.qWait(100)
        self.assertEqual(self.listing().count(),3)
        self.assertEqual(len(self.groups()),1)
        self.assertEqual(self.groups()[0].text(),'Pattern 1 — %d × %d'%(n,n))
        return self.groups()[0].data(257)

    def click(self,row=None,checkbox=False,double=False):
        from PySide6 import QtCore
        rows=self.listing();row=row or self.groups()[0]
        rows.scrollToItem(row);rows.setFocus()
        rect=rows.visualItemRect(row)
        pos=QtCore.QPoint(10,rect.center().y()) if checkbox else rect.center()
        self.QtTest.QTest.mouseClick(rows.viewport(),QtCore.Qt.LeftButton,pos=pos)
        if double:self.QtTest.QTest.mouseDClick(rows.viewport(),QtCore.Qt.LeftButton,pos=pos)
        self.QtTest.QTest.qWait(150)

    def test_dense_grids_single_row_preserve_geometry(self):
        from freecad_plus import sketch_pattern_edit as editing
        for n in (12,20):
            with self.subTest(n=n):
                group=self.seed(n)
                record,ids,options=editing.load(self.s,group)
                self.assertEqual(len(record['instances']),n*n-1)
                self.assertEqual(len(record['helpers']),n*n-1)
                self.assertEqual(self.s.GeometryCount,2+2*(n*n-1))
                self.assertEqual(sum(c.Type=='Equal' and c.First==1 for c in self.s.Constraints),n*n-1)
                self.assertEqual(self.s.solve(),0)
                if os.environ.get('PLUS_TEST_DIR'):
                    out=Path(os.environ['PLUS_TEST_DIR'])
                    self.doc.saveAs(str(out/('elements-grid%d.FCStd'%n)))
                    rows=self.listing()
                    rows.grab().save(str(out/('elements-grid%d.png'%n)))
                self.doc.undo();self.QtTest.QTest.qWait(80)
                self.assertEqual(self.listing().count(),2)
                self.doc.redo();self.QtTest.QTest.qWait(80)
                self.assertEqual(self.listing().count(),3)
                self.doc.undo();self.s.delConstraint(0)

    def test_visibility_selection_delete_and_undo(self):
        from freecad_plus import sketch_pattern_edit as editing
        group=self.seed()
        record,_,_=editing.load(self.s,group);indexed=editing.identities(self.s)
        members={indexed[t] for t in editing.owned(record)}
        helpers={indexed[t] for t in record['helpers']}
        self.click()
        selected={int(name[4:])-1 for entry in self.Gui.Selection.getSelectionEx()
                  for name in entry.SubElementNames if name.startswith('Edge')}
        self.assertEqual(selected,members)
        self.click(checkbox=True)
        self.assertTrue(all(pattern.visual_layer(self.s.GeometryFacadeList[i])==2 for i in members))
        self.assertEqual(pattern.visual_layer(self.s.GeometryFacadeList[0]),0)
        self.assertEqual(pattern.visual_layer(self.s.GeometryFacadeList[1]),0)
        self.click(checkbox=True)
        self.assertTrue(all(pattern.visual_layer(self.s.GeometryFacadeList[i])==(2 if i in helpers else 0) for i in members))
        pattern.set_chain_hidden(self.s,False);self.QtTest.QTest.qWait(80)
        self.click(checkbox=True);self.click(checkbox=True)
        self.assertTrue(all(pattern.visual_layer(self.s.GeometryFacadeList[i])==0 for i in members))
        self.click();self.Gui.runCommand('Std_Delete');self.QtTest.QTest.qWait(100)
        self.assertEqual(self.s.GeometryCount,2)
        self.assertEqual(self.s.ConstraintCount,1)
        self.assertEqual(self.listing().count(),2)
        self.assertFalse(self.s.PatternDefinitions)
        self.doc.undo();self.QtTest.QTest.qWait(100)
        self.assertEqual(self.listing().count(),3)
        self.assertEqual(len(self.s.PatternDefinitions),1)
        self.assertEqual(self.s.solve(),0)
        # The row's Delete action still targets the group after a partial viewport pick.
        from PySide6 import QtCore
        self.Gui.Selection.clearSelection();self.Gui.Selection.addSelection(self.s,'Edge3')
        self.QtTest.QTest.qWait(80)
        QtCore.QMetaObject.invokeMethod(self.listing(),'deleteSelectedItems')
        self.QtTest.QTest.qWait(80)
        self.assertEqual(self.s.GeometryCount,2);self.assertFalse(self.s.PatternDefinitions)
        self.doc.undo();self.QtTest.QTest.qWait(80)
        self.assertEqual(self.listing().count(),3)

    def test_multiple_patterns_filter_and_viewport_selection(self):
        from PySide6 import QtCore
        self.seed(3,False)
        pattern.apply(self.s,[0],fixtures.linear(),True);self.QtTest.QTest.qWait(100)
        self.assertEqual(self.listing().count(),4)
        self.assertEqual(len(self.groups()),2)
        self.Gui.Selection.addSelection(self.s,'Edge3')
        self.Gui.Selection.addSelection(self.s,'Edge4')
        self.Gui.Selection.removeSelection(self.s,'Edge3');self.QtTest.QTest.qWait(100)
        self.assertTrue(self.groups()[0].isSelected())
        self.Gui.Selection.clearSelection();self.QtTest.QTest.qWait(100)
        self.assertFalse(any(row.isSelected() for row in self.groups()))
        panel=self.listing().parentWidget()
        checkbox=panel.findChild(self.QtWidgets.QCheckBox,'filterBox');checkbox.setChecked(True)
        button=panel.findChild(self.QtWidgets.QToolButton,'filterButton')
        filter_action=button.actions()[0]
        filters=filter_action.defaultWidget()
        # Circle-only filtering retains the circle pattern, without helper child rows.
        for i in range(5,filters.count()):filters.item(i).setCheckState(QtCore.Qt.Checked if i==7 else QtCore.Qt.Unchecked)
        self.QtTest.QTest.qWait(100)
        self.assertEqual(sum(not row.isHidden() for row in self.groups()),1)
        checkbox.setChecked(False)
        self.assertEqual(sum(not row.isHidden() for row in self.groups()),2)

    def test_free_copies_remain_one_editable_pattern(self):
        from freecad_plus import sketch_pattern_edit as editing
        pattern.apply(self.s,[1],fixtures.linear(),False)
        self.QtTest.QTest.qWait(100)
        self.assertEqual(self.s.ConstraintCount,0)
        self.assertEqual(self.listing().count(),3)
        group=self.groups()[0].data(257)
        record,ids,options=editing.load(self.s,group)
        self.assertFalse(record['dimensions']);self.assertEqual(ids,[1])
        self.click(double=True)
        panel=self.win.findChild(self.QtWidgets.QWidget,'SketchPatternPanel')
        self.assertTrue(panel.isVisible());self.assertFalse(panel.lock.isChecked())
        panel.d1.count.setValue(5);panel.done.click();self.QtTest.QTest.qWait(100)
        self.assertEqual(self.s.GeometryCount,6)
        self.assertEqual(self.s.ConstraintCount,0)
        self.assertEqual(self.listing().count(),3)
        self.assertIn('5',self.groups()[0].text())
        if os.environ.get('PLUS_TEST_DIR'):
            self.doc.saveAs(str(Path(os.environ['PLUS_TEST_DIR'])/'elements-free.FCStd'))
        pattern.apply(self.s,[0],fixtures.linear(),True);self.QtTest.QTest.qWait(80)
        self.assertEqual({r.text().split(' — ')[0] for r in self.groups()},{'Pattern 1','Pattern 2'})

    def test_angular_radial_membership_survives_renumber(self):
        from freecad_plus import sketch_pattern_edit as editing
        options=fixtures.circular(directions='Angular + radial',
            angular=fixtures.extent(spacing='Angular pitch',value=30,count=4),
            radial=fixtures.extent(reference=(1,3),value=5,count=3))
        pattern.apply(self.s,[1],options,True);self.QtTest.QTest.qWait(80)
        self.assertEqual(self.listing().count(),3)
        self.assertEqual(self.groups()[0].text(),'Pattern 1 — 4 × 3')
        group=self.groups()[0].data(257)
        self.s.delGeometry(0);self.doc.recompute();self.QtTest.QTest.qWait(80)
        self.assertEqual(self.listing().count(),2)
        self.assertEqual(editing.load(self.s,group)[1],[0])
        self.assertEqual(self.s.solve(),0)
        if os.environ.get('PLUS_TEST_DIR'):
            self.doc.saveAs(str(Path(os.environ['PLUS_TEST_DIR'])/'elements-angular-radial.FCStd'))

    def test_double_click_edit_cancel_apply_done_and_keyboard(self):
        from PySide6 import QtCore
        self.seed()
        before=self.s.GeometryCount
        self.click(double=True)
        panel=self.win.findChild(self.QtWidgets.QWidget,'SketchPatternPanel')
        self.assertIsNotNone(panel);self.assertTrue(panel.isVisible())
        self.assertEqual(panel.d1.count.value(),4)
        panel.d1.count.setValue(5)
        self.QtTest.QTest.keyClick(panel.d1.count,QtCore.Qt.Key_Escape);self.QtTest.QTest.qWait(120)
        self.assertEqual(self.s.GeometryCount,before)
        self.click(double=True)
        panel=self.win.findChild(self.QtWidgets.QWidget,'SketchPatternPanel')
        panel.d1.count.setValue(5);panel.done.click();self.QtTest.QTest.qWait(120)
        self.assertEqual(self.groups()[0].text(),'Pattern 1 — 5 × 4')
        rows=self.listing();rows.setCurrentItem(self.groups()[0]);rows.setFocus()
        self.QtTest.QTest.keyClick(rows,QtCore.Qt.Key_Return);self.QtTest.QTest.qWait(150)
        panel=self.win.findChild(self.QtWidgets.QWidget,'SketchPatternPanel')
        self.assertTrue(panel.isVisible());panel.d2.count.setValue(3);panel.apply.click()
        self.assertEqual(panel.items.count(),0,panel.status.text())
        panel.done.click();self.QtTest.QTest.qWait(120)
        self.assertEqual(self.groups()[0].text(),'Pattern 1 — 5 × 3')


class TestPatternGroupView(unittest.TestCase):
    setUp = fixtures.TestPatternTask.setUp
    tearDown = fixtures.TestPatternTask.tearDown
    enter = fixtures.TestPatternTask.enter
    pick = fixtures.TestPatternTask.pick

    def test_dense_inch_grid_defers_labels_and_preserves_chains(self):
        from PySide6 import QtTest
        s=self.s
        s.delGeometry(1);s.delGeometry(0)
        s.addGeometry(Part.Circle(App.Vector(1.27,1.27,0),App.Vector(0,0,1),.325))
        s.addGeometry([Part.LineSegment(App.Vector(1.27,1.27,0),App.Vector(1.27,0,0)),
                       Part.LineSegment(App.Vector(1.27,1.27,0),App.Vector(0,1.27,0))],True)
        s.addConstraint([Sketcher.Constraint('Coincident',1,1,0,3),
                         Sketcher.Constraint('PointOnObject',1,2,-1),Sketcher.Constraint('Vertical',1),
                         Sketcher.Constraint('Coincident',2,1,0,3),
                         Sketcher.Constraint('PointOnObject',2,2,-2),Sketcher.Constraint('Horizontal',2),
                         Sketcher.Constraint('Equal',1,2),Sketcher.Constraint('DistanceY',1,2,1,1,1.27),
                         Sketcher.Constraint('Diameter',0,.65)])
        self.assertEqual(s.solve(),0);self.assertEqual(s.DoF,0)
        # Zoomed out enough to merge ungrouped constraint labels. These
        # intermediate labels formerly overflowed Coin's signed-short image width.
        view=self.Gui.activeDocument().activeView()
        view.setCamera('#Inventor V2.1 ascii\nOrthographicCamera { position 25 25 87 orientation 0 0 1 0 nearDistance 1 farDistance 200 focalDistance 87 height 100 }')
        self.enter();self.pick(self.p.items,'Edge1')
        self.p.layout_mode.setCurrentText('Two directions')
        self.pick(self.p.d1.reference,'H_Axis');self.pick(self.p.d2.reference,'V_Axis')
        for direction in (self.p.d1,self.p.d2):
            direction.count.setValue(20)
            field=direction.value.lineEdit();field.setFocus();field.selectAll()
            QtTest.QTest.keyClicks(field,'0.100 in');self.p.items.setFocus()
            direction.value.interpretText();direction.value.committed.emit()
        for axis in ('d1','d2'):
            self.assertAlmostEqual(self.p.options()[axis]['value'],2.54,places=10)
            self.assertEqual(self.p.options()[axis]['unit'],'in')
        self.p.hide_spacing.setChecked(True)
        self.p.apply.click();self.assertEqual(self.p.items.count(),0,self.p.status.text())
        self.p.done.click();QtTest.QTest.qWait(100)
        self.assertEqual((s.GeometryCount,s.ConstraintCount,s.DoF),(801,2004,0))
        self.assertEqual(len(s.PatternSpacingTags),399)
        self.assertEqual(sum(c.Type=='Equal' and c.First==0 for c in s.Constraints),399)
        self.assertTrue(all(not visible(c) for c in s.Constraints if c.PatternGroup))
        self.assertEqual(sum(r.text().startswith('Pattern') for r in self.rows()[1]),1)
        circles=[i for i,g in enumerate(s.Geometry) if isinstance(g,Part.Circle)]
        drivers=[i for i,c in enumerate(s.Constraints) if c.PatternDriver]
        self.assertEqual(len(drivers),2)
        s.setDatum(8,App.Units.Quantity('.8 mm'))
        for i in drivers:
            self.assertEqual(s.Constraints[i].PresentationUnit,'in')
            s.setDatum(i,App.Units.Quantity('.12 in'))
        self.doc.recompute();self.assertEqual(s.solve(),0);self.assertEqual(s.DoF,0)
        for n,i in enumerate(circles):
            self.assertAlmostEqual(s.Geometry[i].Radius,.4,places=8)
            self.assertLess((s.Geometry[i].Center-App.Vector(1.27+n//20*3.048,1.27+n%20*3.048,0)).Length,1e-6)
        for c in s.Constraints:
            if c.Type=='Coincident':
                self.assertLess((s.getPoint(c.First,c.FirstPos)-s.getPoint(c.Second,c.SecondPos)).Length,1e-6)
        for hidden in (False,True):
            pattern.set_chain_hidden(s,hidden)
            self.assertEqual(pattern.chain_is_hidden(s),hidden)
            self.assertTrue(all(visible(c)!=hidden for c in s.Constraints if c.PatternGroup))
        if os.environ.get('PLUS_TEST_DIR'):
            self.doc.saveAs(str(Path(os.environ['PLUS_TEST_DIR'])/'dense-grid20.FCStd'))
        self.doc.undo();self.assertEqual((s.GeometryCount,s.ConstraintCount),(3,9))
        self.doc.redo();self.assertEqual((s.GeometryCount,s.ConstraintCount),(801,2004))
        self.assertEqual(s.solve(),0)

    def nodes(self):
        from pivy import coin
        search=coin.SoSearchAction();search.setName('ConstraintGroup')
        search.setSearchingAll(True);search.apply(self.Gui.activeDocument().activeView().getSceneGraph())
        self.assertIsNotNone(search.getPath())
        return search.getPath().getTail()

    def rows(self):
        widget=self.win.findChild(self.QtWidgets.QListWidget,'listWidgetConstraints')
        self.assertIsNotNone(widget)
        return widget,[widget.item(i) for i in range(widget.count()) if not widget.item(i).isHidden()]

    def test_single_icon_list_hide_selection_delete_undo(self):
        from PySide6 import QtCore,QtTest,QtOpenGLWidgets
        self.s.addConstraint(Sketcher.Constraint('Distance',0,4.))
        self.enter();self.pick(self.p.items,'Edge1')
        self.p.layout_mode.setCurrentText('Two directions')
        self.pick(self.p.d1.reference,'H_Axis');self.pick(self.p.d2.reference,'V_Axis')
        self.p.d1.count.setValue(12);self.p.d2.count.setValue(12)
        start=time.perf_counter();self.p.apply.click();elapsed=time.perf_counter()-start
        self.assertEqual(self.p.items.count(),0,self.p.status.text())
        self.assertLess(elapsed,20.)
        self.p.done.click();QtTest.QTest.qWait(100)
        self.assertEqual(self.s.solve(),0)
        widget,rows=self.rows()
        self.assertEqual(len(rows),2,[r.text() for r in rows])
        row=next(r for r in rows if r.text().startswith('Pattern'))
        self.assertIn('12 × 12',row.text())
        self.assertFalse(row.flags() & QtCore.Qt.ItemIsEditable)
        node=self.nodes()
        self.assertEqual(sum(bool(v) for v in node.enable.getValues()),2)
        view=self.Gui.activeDocument().activeView();view.viewTop();view.fitAll()
        if os.environ.get('PLUS_TEST_DIR'):
            from TestComponentFading import capture
            out=Path(os.environ['PLUS_TEST_DIR'])
            capture(view,out/'pattern-shown.png')
            widget.grab().save(str(out/'pattern-list.png'))
            (out/'fixed-line-grid12-task-timing.json').write_text(json.dumps(dict(seconds=elapsed)))
        pattern.set_chain_hidden(self.s,True);QtTest.QTest.qWait(100)
        self.assertEqual(sum(bool(v) for v in self.nodes().enable.getValues()),1)
        self.assertEqual(len(self.rows()[1]),2)
        if os.environ.get('PLUS_TEST_DIR'):
            capture(view,out/'pattern-hidden.png')
        pattern.set_chain_hidden(self.s,False);QtTest.QTest.qWait(100)
        self.assertEqual(sum(bool(v) for v in self.nodes().enable.getValues()),2)

        widget,rows=self.rows();row=next(r for r in rows if r.text().startswith('Pattern'))
        QtTest.QTest.mouseClick(widget.viewport(),QtCore.Qt.LeftButton,pos=widget.visualItemRect(row).center())
        QtTest.QTest.qWait(100)
        selections=self.Gui.Selection.getSelectionEx()
        selected=[n for entry in selections for n in entry.SubElementNames if n.startswith('Constraint')]
        self.assertEqual(len(selected),self.s.ConstraintCount-1)
        before=self.s.GeometryCount
        self.Gui.runCommand('Std_Delete');QtTest.QTest.qWait(100)
        self.assertEqual(self.s.GeometryCount,before)
        self.assertEqual(self.s.ConstraintCount,1)
        self.doc.undo();QtTest.QTest.qWait(100)
        self.assertEqual(self.s.ConstraintCount,1145)
        self.assertEqual(len(self.rows()[1]),2)
        self.assertEqual(sum(bool(v) for v in self.nodes().enable.getValues()),2)

    def test_group_pitch_editor_preserves_units(self):
        from PySide6 import QtTest,QtWidgets
        self.s.addConstraint(Sketcher.Constraint('Distance',0,4.))
        pattern.apply(self.s,[0],fixtures.linear(),True)
        widget,rows=self.rows();row=next(r for r in rows if r.text().startswith('Pattern'))
        widget.itemActivated.emit(row);QtTest.QTest.qWait(200)
        panel=self.win.findChild(QtWidgets.QWidget,'SketchPatternPanel')
        self.assertIsNotNone(panel)
        self.assertTrue(panel.edit_group)
        field=panel.d1.value.lineEdit();field.setFocus();field.selectAll()
        QtTest.QTest.keyClicks(field,'0.123456 in');panel.items.setFocus();QtTest.QTest.qWait(50)
        panel.done.click();QtTest.QTest.qWait(100)
        c=next(c for c in self.s.Constraints if c.PatternDriver)
        self.assertEqual(c.PresentationUnit,'in');self.assertAlmostEqual(c.Value,.123456*25.4,places=10)
        self.assertEqual(self.s.solve(),0)
