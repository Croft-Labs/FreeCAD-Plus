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


class TestPatternGroupView(unittest.TestCase):
    setUp = fixtures.TestPatternTask.setUp
    tearDown = fixtures.TestPatternTask.tearDown
    enter = fixtures.TestPatternTask.enter
    pick = fixtures.TestPatternTask.pick

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
