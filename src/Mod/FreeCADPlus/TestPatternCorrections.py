# SPDX-License-Identifier: LGPL-2.1-or-later
import math,os,unittest
from pathlib import Path
import FreeCAD as App,Part,Sketcher
from PySide6 import QtCore,QtWidgets,QtTest,QtOpenGLWidgets
import TestSketchPattern as fixtures
from freecad_plus import sketch_pattern as pattern


class TestPatternSizes(unittest.TestCase):
    setUp=fixtures.TestPatternGeometry.setUp
    tearDown=fixtures.TestPatternGeometry.tearDown

    def test_projected_length_preserves_free_orientation(self):
        self.s.addGeometry(Part.LineSegment(App.Vector(10,3,0),App.Vector(16,3,0)))
        self.s.addConstraint(Sketcher.Constraint('DistanceX',0,6.))
        before=self.s.DoF
        copies=pattern.apply(self.s,[0],fixtures.linear(d1=fixtures.extent(count=2)),True)
        self.assertEqual(self.s.DoF,before)
        self.s.moveGeometry(0,2,App.Vector(16,7,0),False)
        self.assertEqual(self.s.solve(),0)
        self.assertLess(((self.s.Geometry[copies[0]].EndPoint-self.s.Geometry[copies[0]].StartPoint)-
                         (self.s.Geometry[0].EndPoint-self.s.Geometry[0].StartPoint)).Length,1e-6)

    def test_equal_circle_line_arc_sizes_and_source_edits(self):
        for kind in ('circle','diameter','line','horizontal','arc'):
            with self.subTest(kind=kind):
                self.s.deleteAllGeometry()
                line=kind in ('line','horizontal')
                if line:
                    g=Part.LineSegment(App.Vector(10,3,0),App.Vector(16,3,0));c=Sketcher.Constraint('DistanceX' if kind=='horizontal' else 'Distance',0,6.)
                else:
                    g=Part.Circle(App.Vector(20,3,0),App.Vector(0,0,1),3)
                    if kind=='arc':g=Part.ArcOfCircle(g,0,math.pi/2)
                    c=Sketcher.Constraint('Diameter' if kind=='diameter' else 'Radius',0,6. if kind=='diameter' else 3.)
                self.s.addGeometry(g);self.s.addConstraint(c)
                if kind=='horizontal':self.s.addConstraint(Sketcher.Constraint('Horizontal',0))
                copies=pattern.apply(self.s,[0],fixtures.linear(d1=fixtures.extent(count=3)),True)
                self.assertEqual(self.s.solve(),0)
                for i in copies:
                    self.assertTrue(any(c.Type=='Equal' and {c.First,c.Second}=={0,i} for c in self.s.Constraints))
                    self.assertFalse(any(c.Driving and c.Type in ('Radius','Diameter','Distance','DistanceX','DistanceY') and c.First==i for c in self.s.Constraints))
                self.s.setDatum(0,App.Units.Quantity('8 mm' if line or kind=='diameter' else '4 mm'));self.doc.recompute()
                self.assertEqual(self.s.solve(),0)
                for i in copies:
                    actual=self.s.Geometry[i]
                    self.assertAlmostEqual((actual.EndPoint-actual.StartPoint).Length if line else actual.Radius,8 if line else 4,places=6)
        if os.environ.get('PLUS_TEST_DIR'):
            self.doc.saveAs(str(Path(os.environ['PLUS_TEST_DIR'])/'equal-pattern.FCStd'))

    def test_preview_helpers_match_committed_chains_without_mutations(self):
        self.s.addGeometry(Part.Circle(App.Vector(20,0,0),App.Vector(0,0,1),2))
        for options in (fixtures.linear(directions='Two directions',d2=fixtures.extent(reference=(-2,0))),
                        fixtures.circular(directions='Angular + radial',angular=fixtures.extent(spacing='Angular pitch',value=30),radial=fixtures.extent(reference=(0,3),value=5))):
            before=(self.s.GeometryCount,self.s.ConstraintCount,self.doc.UndoCount,tuple(self.s.PropertiesList))
            helpers=[];copies=pattern.preview(self.s,[0],options,True,helpers)
            self.assertTrue(helpers);self.assertTrue(copies)
            self.assertEqual(before,(self.s.GeometryCount,self.s.ConstraintCount,self.doc.UndoCount,tuple(self.s.PropertiesList)))
            hidden=[];pattern.preview(self.s,[0],dict(options,hide_spacing=True),True,hidden);self.assertEqual(hidden,[])
            pattern.apply(self.s,[0],options,True)
            tags=set(self.s.PatternSpacingTags)
            actual=[f.Geometry for f in self.s.GeometryFacadeList if pattern.spacing_tag(f) in tags]
            self.assertEqual(len(helpers),len(actual))
            for a,b in zip(helpers,actual):
                self.assertEqual(type(a),type(b))
                self.assertAlmostEqual(a.toShape().Length,b.toShape().Length,places=5)
            self.doc.undo();self.assertEqual(self.s.GeometryCount,1)


class TestPatternCompletion(unittest.TestCase):
    setUp=fixtures.TestPatternTask.setUp
    tearDown=fixtures.TestPatternTask.tearDown
    enter=fixtures.TestPatternTask.enter
    pick=fixtures.TestPatternTask.pick

    def test_partial_directions_helpers_hide_and_narrow_fields(self):
        from TestComponentFading import capture
        self.enter();self.pick(self.p.items,'Edge2')
        before=(self.s.GeometryCount,self.s.ConstraintCount,self.doc.UndoCount)
        self.p.layout_mode.setCurrentText('Two directions');self.pick(self.p.d1.reference,'H_Axis')
        self.assertFalse(self.p.apply.isEnabled());self.assertEqual(len(self.p._preview),4)
        self.assertEqual(len(self.p._helper_preview),4)
        self.p.hide_spacing.setChecked(True);self.assertEqual(self.p._helper_preview,[])
        self.p.hide_spacing.setChecked(False);self.assertEqual(len(self.p._helper_preview),4)
        self.pick(self.p.d2.reference,'V_Axis');self.assertEqual(len(self.p._preview),24)
        self.assertTrue(self.p.apply.isEnabled())
        self.p.d1.reference.clear();self.assertEqual(len(self.p._preview),4);self.assertFalse(self.p.apply.isEnabled())
        self.assertEqual(before,(self.s.GeometryCount,self.s.ConstraintCount,self.doc.UndoCount))
        self.p.done.click();self.assertTrue(self.p.isVisible());self.assertEqual(self.s.GeometryCount,before[0])
        self.p.mode.setCurrentText('Circular');self.p.layout_mode.setCurrentText('Angular + radial')
        self.pick(self.p.center,'RootPoint');self.p.angular.value.setValue(30);self.p.angular.count.setValue(3)
        self.assertEqual(len(self.p._preview),2);self.assertEqual(len(self.p._helper_preview),2)
        self.pick(self.p.radial.reference,'Edge2');self.p.radial.count.setValue(3);self.p.radial.value.setValue(5)
        self.assertEqual(len(self.p._preview),8);self.assertEqual(len(self.p._helper_preview),9)
        self.assertEqual(before,(self.s.GeometryCount,self.s.ConstraintCount,self.doc.UndoCount))
        view=self.Gui.activeDocument().activeView();view.getCameraNode().height=90
        QtTest.QTest.qWait(150);capture(view,Path(os.environ['PLUS_TEST_DIR'])/'preview-chains.png')
        self.p.hide_spacing.setChecked(True);QtTest.QTest.qWait(100)
        capture(view,Path(os.environ['PLUS_TEST_DIR'])/'preview-hidden.png')
        dock=self.win.findChild(QtWidgets.QDockWidget,'Tasks')
        dock.setMinimumWidth(0);self.win.resizeDocks([dock],[380],QtCore.Qt.Horizontal);QtTest.QTest.qWait(100)
        for w in self.p.findChildren(QtWidgets.QWidget):
            if w.isVisible() and isinstance(w,(QtWidgets.QComboBox,QtWidgets.QAbstractSpinBox,QtWidgets.QLineEdit,QtWidgets.QPushButton)):
                x=w.mapTo(self.p,QtCore.QPoint()).x()
                self.assertLessEqual(x+w.width(),self.p.width())
        self.assertLess(self.p.done.x(),self.p.apply.x())
        dock.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'native-narrow-pattern.png'))

    def test_apply_reset_done_commit_empty_close_and_cancel(self):
        self.enter();self.pick(self.p.items,'Edge2');self.pick(self.p.d1.reference,'H_Axis')
        self.p.d1.count.setValue(3);self.p.d1.value.setValue(12)
        self.p.apply.click()
        self.assertEqual(self.p.items.count(),0);self.assertFalse(self.p.d1.reference.text())
        self.assertEqual(self.p.d1.value.value(),12);self.assertEqual(self.p.d1.count.value(),3)
        self.assertEqual(self.p._preview,[]);self.assertIsNone(self.p._helper_node)
        count=self.s.GeometryCount;self.p.done.click();QtTest.QTest.qWait(100)
        self.assertEqual(self.s.GeometryCount,count);self.assertIsNotNone(self.Gui.activeDocument().getInEdit())
        self.enter();self.pick(self.p.items,'Edge2');self.pick(self.p.d1.reference,'H_Axis')
        self.p.done.click();QtTest.QTest.qWait(100)
        self.assertGreater(self.s.GeometryCount,count);self.assertFalse(self.p.isVisible())
        self.assertIsNone(self.p._helper_node)
        count=self.s.GeometryCount
        self.enter();self.pick(self.p.items,'Edge2');self.pick(self.p.d1.reference,'H_Axis')
        QtTest.QTest.keyClick(self.p.items,QtCore.Qt.Key_Escape);QtTest.QTest.qWait(100)
        self.assertEqual(self.s.GeometryCount,count);self.assertIsNone(self.p._helper_node)

    def test_invalid_entry_and_failed_done_preserve_pending_input(self):
        self.enter();self.pick(self.p.items,'Edge1');self.pick(self.p.d1.reference,'H_Axis')
        field=self.p.d1.value;field.setFocus();field.selectAll();QtTest.QTest.keyClicks(field,'invalid')
        self.assertFalse(self.p.apply.isEnabled());self.assertEqual(self.p._preview,[])
        self.assertIsNone(self.p._helper_node)
        field.selectAll();QtTest.QTest.keyClicks(field,'12 mm');self.p.items.setFocus();QtTest.QTest.qWait(30)
        self.assertTrue(self.p.apply.isEnabled())
        self.s.addConstraint(Sketcher.Constraint('Distance',0,4.))
        conflict=self.s.addConstraint(Sketcher.Constraint('Distance',0,5.))
        count=self.s.GeometryCount
        self.p.done.click();QtTest.QTest.qWait(50)
        self.assertTrue(self.p.isVisible());self.assertEqual(self.p.items.count(),1)
        self.assertTrue(self.p.d1.reference.text());self.assertEqual(self.s.GeometryCount,count)
        self.assertTrue(self.p.status.error)
        self.s.delConstraint(conflict);self.p.sync();self.p.done.click();QtTest.QTest.qWait(100)
        self.assertFalse(self.p.isVisible());self.assertGreater(self.s.GeometryCount,count)
