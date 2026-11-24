# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native symmetry task acceptance. Run only with an isolated GUI profile."""
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtWidgets, QtTest, QtGui


class TestSketchSymmetry(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Requires an isolated GUI profile')
        self.doc = App.newDocument('SymmetryTest')
        self.doc.UndoMode = 1
        self.sketch = self.doc.addObject('Sketcher::SketchObject', 'Sketch')
        for a,b in (((5,3),(15,3)), ((15,3),(15,11)), ((15,11),(5,11))):
            self.sketch.addGeometry(Part.LineSegment(App.Vector(*a,0), App.Vector(*b,0)), False)
        self.sketch.addGeometry(Part.Circle(App.Vector(23,6,0), App.Vector(0,0,1),2),False)
        self.doc.recompute()
        Gui.activateWorkbench('SketcherWorkbench')
        self.win = Gui.getMainWindow()
        self.win.showNormal(); self.win.resize(1400,1100)
        Gui.activeDocument().setEdit(self.sketch.Name)
        self.settle()
        view = Gui.activeDocument().activeView()
        view.setAnimationEnabled(False);view.viewTop();view.fitAll()
        self.settle()
        self.sections = [(w,not w.isHidden()) for w in self.win.findChildren(QtWidgets.QWidget)
                         if w.metaObject().className().split('::')[-1] in
                         ('TaskSketcherMessages','TaskSketcherConstraints','TaskSketcherElements')]
        Gui.Selection.clearSelection()

    def tearDown(self):
        QtTest.QTest.keyRelease(self.win, QtCore.Qt.Key_Shift)
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit()
        if App.getActiveTransaction():App.closeActiveTransaction(True)
        Gui.Selection.clearSelection()
        App.closeDocument(self.doc.Name)
        self.settle()

    def settle(self):
        QtTest.QTest.qWait(100)

    def child(self, kind, name):
        result = self.win.findChild(kind, name)
        self.assertIsNotNone(result, name)
        return result

    def enter(self, preselect=()):
        for sub in preselect:Gui.Selection.addSelection(self.sketch,sub)
        Gui.runCommand('Sketcher_Symmetry');self.settle()
        self.items = self.child(QtWidgets.QListWidget,'SymmetryGeometry')
        self.axis = self.child(QtWidgets.QLineEdit,'SymmetryAxis')
        self.apply = self.child(QtWidgets.QPushButton,'SymmetryApply')
        self.done = self.child(QtWidgets.QPushButton,'SymmetryDone')
        self.assertTrue(self.items.isVisible())

    def focus(self, widget):
        QtTest.QTest.mouseClick(widget.viewport() if isinstance(widget,QtWidgets.QListWidget) else widget,
                               QtCore.Qt.LeftButton);self.settle()

    def pick(self, sub, axis=False, shift=False):
        self.focus(self.axis if axis else self.items)
        Gui.Selection.clearSelection()
        from freecad_plus.selection_list import pick_intent
        with pick_intent(shift):
            Gui.Selection.addSelection(self.sketch,sub);self.settle()

    def assert_restored(self):
        self.settle()
        self.assertIsNotNone(Gui.activeDocument().getInEdit())
        self.assertFalse(self.items.isVisible())
        for widget, visible in self.sections:self.assertEqual(not widget.isHidden(), visible)

    def capture(self,name):
        out=Path(os.environ['PLUS_TEST_DIR'])
        self.win.findChild(QtWidgets.QDockWidget,'Tasks').grab().save(str(out/(name+'.png')))

    def test_empty_entry_large_list_and_done_restore(self):
        self.enter()
        self.assertFalse(self.apply.isEnabled())
        self.assertGreaterEqual(self.items.height(),360)
        self.assertTrue(all(w.isHidden() for w,visible in self.sections))
        self.pick('Edge1');self.pick('V_Axis',axis=True)
        self.assertTrue(self.apply.isEnabled());self.capture('symmetry-ready')
        self.assertEqual(self.sketch.GeometryCount,4)
        self.done.click();self.assert_restored()
        self.assertEqual(self.sketch.GeometryCount,4)

    def test_apply_repeated_and_undo_redo(self):
        self.enter(('Edge1','Edge2'))
        self.assertEqual(self.items.count(),2)
        self.pick('V_Axis',axis=True);self.apply.click();self.settle()
        self.assertEqual(self.sketch.GeometryCount,6)
        self.assertAlmostEqual(self.sketch.Geometry[4].StartPoint.x,-5)
        self.assertEqual(self.sketch.ConstraintCount,0)
        self.assertEqual(self.items.count(),0);self.assertTrue(self.items.isVisible())
        self.assertTrue(self.axis.text())
        self.pick('Edge3');self.apply.click();self.settle()
        self.assertEqual(self.sketch.GeometryCount,7)
        self.doc.undo();self.settle();self.assertEqual(self.sketch.GeometryCount,6)
        self.doc.redo();self.settle();self.assertEqual(self.sketch.GeometryCount,7)
        self.pick('Edge1');self.done.click();self.assert_restored()
        self.assertEqual(self.sketch.GeometryCount,7)

    def test_shift_delete_clear_and_invalid_axis_recovery(self):
        self.enter()
        self.pick('Edge1');self.pick('Edge1');self.assertEqual(self.items.count(),1)
        self.pick('Edge2',shift=True);self.assertEqual(self.items.count(),1)
        self.pick('Edge1',shift=True);self.assertEqual(self.items.count(),0)
        self.pick('Edge1');self.pick('Edge2')
        self.items.setCurrentRow(0)
        QtTest.QTest.keyClick(self.items,QtCore.Qt.Key_Delete);self.settle()
        self.assertEqual(self.items.count(),1)
        self.pick('V_Axis',axis=True);self.assertTrue(self.apply.isEnabled())
        previous=self.axis.text()
        self.pick('Edge4',axis=True)
        self.assertEqual(self.axis.text(),previous);self.assertFalse(self.apply.isEnabled())
        self.assertIn('#bd780b',self.child(QtWidgets.QLabel,'SymmetryStatus').styleSheet())
        self.capture('symmetry-invalid-axis')
        self.pick('H_Axis',axis=True);self.assertTrue(self.apply.isEnabled())
        self.pick('H_Axis',axis=True,shift=True);self.assertFalse(self.axis.text())
        self.child(QtWidgets.QPushButton,'SymmetryClear').click()
        self.assertEqual(self.items.count(),0)
        self.done.click()

    def test_native_options_construction_and_point_center(self):
        self.sketch.toggleConstruction(0)
        self.enter(('Edge1',))
        delete=self.child(QtWidgets.QCheckBox,'SymmetryDeleteOriginal')
        constraints=self.child(QtWidgets.QCheckBox,'SymmetryConstraints')
        self.assertFalse(delete.isChecked());self.assertFalse(constraints.isChecked())
        delete.setChecked(True);constraints.setChecked(True);self.assertFalse(delete.isChecked())
        delete.setChecked(True);self.assertFalse(constraints.isChecked())
        delete.setChecked(False)
        self.pick('RootPoint',axis=True);self.apply.click();self.settle()
        self.assertEqual(self.sketch.GeometryCount,5)
        self.assertTrue(self.sketch.getConstruction(4))
        self.assertAlmostEqual(self.sketch.Geometry[4].StartPoint.y,-3)
        self.done.click()

    def test_delete_original_and_axis_remapping(self):
        self.enter(('Edge1',))
        self.pick('Edge3',axis=True)
        self.child(QtWidgets.QCheckBox,'SymmetryDeleteOriginal').setChecked(True)
        self.apply.click();self.settle()
        self.assertEqual(self.sketch.GeometryCount,4)
        self.assertEqual(self.axis.text(),'Edge2')
        self.assertAlmostEqual(self.sketch.Geometry[3].StartPoint.y,19)
        self.done.click()

    def test_constraints_cancel_escape_and_other_tool(self):
        self.enter(('Edge1',))
        self.child(QtWidgets.QCheckBox,'SymmetryConstraints').setChecked(True)
        self.pick('V_Axis',axis=True);self.apply.click();self.settle()
        self.assertGreater(self.sketch.ConstraintCount,0)
        count=self.sketch.GeometryCount
        self.pick('Edge2')
        self.child(QtWidgets.QPushButton,'SketchCancelAction').click();self.assert_restored()
        self.assertEqual(self.sketch.GeometryCount,count)
        self.enter()
        self.focus(self.axis);QtTest.QTest.keyClick(self.axis,QtCore.Qt.Key_Escape)
        self.assert_restored()
        Gui.runCommand('Sketcher_CreateLine');self.settle()
        self.assertTrue(all(not w.isHidden()==visible for w,visible in self.sections))
        self.child(QtWidgets.QPushButton,'SketchCancelAction').click()

    def test_real_viewport_click_and_shift(self):
        self.enter()
        view=Gui.activeDocument().activeView()
        view.getCameraNode().height=70;self.settle()
        widget=view.graphicsView().viewport();ratio=widget.devicePixelRatioF()
        def click(point,shift=False,expected=None):
            screen=view.getPointOnScreen(point)
            position=QtCore.QPoint(round(screen[0]/ratio),widget.height()-1-round(screen[1]/ratio))
            self.assertTrue(widget.rect().contains(position),str(position))
            event=QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(position),
                QtCore.QPointF(widget.mapToGlobal(position)),QtCore.Qt.NoButton,
                QtCore.Qt.NoButton,QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(widget,event);self.settle()
            if expected:
                # Locate a thin axis's actual hover hit after native viewport rounding.
                seed=QtCore.QPoint(position)
                found=False
                for offset in (0,1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,-7,8,-8):
                    position=seed+QtCore.QPoint(offset,0)
                    event=QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(position),
                        QtCore.QPointF(widget.mapToGlobal(position)),QtCore.Qt.NoButton,
                        QtCore.Qt.NoButton,QtCore.Qt.NoModifier)
                    QtWidgets.QApplication.sendEvent(widget,event);self.settle()
                    if expected in Gui.Selection.getPreselection().SubElementNames:
                        found=True;break
                self.assertTrue(found,'Native axis hover must be hit')
            QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,
                QtCore.Qt.ShiftModifier if shift else QtCore.Qt.NoModifier,position)
            self.settle()
        click(App.Vector(10,3,0));self.assertEqual(self.items.count(),1)
        click(App.Vector(10,3,0));self.assertEqual(self.items.count(),1)
        click(App.Vector(10,3,0),True);self.assertEqual(self.items.count(),0)
        click(App.Vector(10,3,0));self.focus(self.axis)
        click(App.Vector(0,7,0),expected='V_Axis')
        self.win.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'axis-pick.png'))
        self.assertTrue(self.apply.isEnabled(),str((self.items.count(),self.axis.text(),
            self.child(QtWidgets.QLabel,'SymmetryStatus').text())))
        self.apply.click();self.settle();self.assertEqual(self.sketch.GeometryCount,5)
        self.capture('symmetry-applied')
        self.done.click()

    def test_save_reopen(self):
        self.enter(('Edge1','Edge2','Edge3'))
        self.pick('V_Axis',axis=True);self.apply.click();self.settle()
        self.done.click();Gui.activeDocument().resetEdit()
        path=str(Path(os.environ['PLUS_TEST_DIR'])/'symmetry.FCStd')
        self.doc.recompute();self.doc.saveAs(path)
        name=self.doc.Name;App.closeDocument(name)
        self.doc=App.openDocument(path);self.sketch=self.doc.getObject('Sketch')
        self.assertEqual(self.sketch.GeometryCount,7)
        self.assertTrue(self.sketch.Shape.isValid())

    def test_external_line_reference_and_scrollable_many_inputs(self):
        base=self.doc.addObject('Part::Feature','ReferenceLine')
        base.Shape=Part.makeLine(App.Vector(0,-20,0),App.Vector(0,20,0))
        self.doc.recompute()
        self.sketch.addExternal(base.Name,'Edge1')
        for i in range(24):
            self.sketch.addGeometry(Part.LineSegment(App.Vector(30+i,2,0),App.Vector(30+i,4,0)),False)
        self.doc.recompute();self.settle()
        count=self.sketch.GeometryCount
        self.enter(tuple('Edge'+str(i+1) for i in range(count)))
        self.assertEqual(self.items.count(),count)
        self.assertGreater(self.items.verticalScrollBar().maximum(),0)
        self.items.scrollToBottom();self.settle()
        self.assertGreater(self.items.verticalScrollBar().value(),0)
        self.pick('ExternalEdge1',axis=True);self.assertTrue(self.apply.isEnabled())
        self.apply.click();self.settle()
        self.assertEqual(self.sketch.GeometryCount,count*2)
        self.assertAlmostEqual(self.sketch.Geometry[count].StartPoint.x,-5)
        self.done.click()

    def test_empty_sketch_can_open_and_cancel(self):
        Gui.activeDocument().resetEdit()
        self.sketch.deleteAllGeometry();self.doc.recompute()
        Gui.activeDocument().setEdit(self.sketch.Name);self.settle()
        self.enter();self.assertFalse(self.apply.isEnabled())
        self.done.click();self.assertIsNotNone(Gui.activeDocument().getInEdit())

    def test_component_sketch_both_presentations(self):
        Gui.activeDocument().resetEdit()
        from freecad_plus import document, modeling
        original=self.doc
        prefs=App.ParamGet('User parameter:BaseApp/Preferences/General')
        previous=prefs.GetInt('TaskPanelUIMode',0)
        try:
            for mode in (0,1):
                prefs.SetInt('TaskPanelUIMode',mode)
                component_doc=document.new_document('SymmetryComponent')
                try:
                    sketch=modeling.new_sketch(component_doc)
                    sketch.addGeometry(Part.LineSegment(App.Vector(5,3,0),App.Vector(15,3,0)),False)
                    component_doc.recompute();Gui.activeDocument().setEdit(sketch.Name);self.settle()
                    self.sketch=sketch
                    self.enter();self.pick('Edge1');self.pick('V_Axis',axis=True)
                    self.apply.click();self.settle()
                    self.assertEqual(sketch.GeometryCount,2)
                    self.done.click();Gui.activeDocument().resetEdit()
                finally:
                    App.closeDocument(component_doc.Name)
        finally:
            prefs.SetInt('TaskPanelUIMode',previous)
            App.setActiveDocument(original.Name)
            self.sketch=original.getObject('Sketch')

    def test_standalone_point_selected_after_open(self):
        point_id=self.sketch.addGeometry(Part.Point(App.Vector(8,6,0)),False)
        self.doc.recompute();self.settle();self.enter()
        vertex=next('Vertex'+str(i+1) for i in range(self.sketch.GeometryCount*3)
                    if self.sketch.getGeoVertexIndex(i)[0]==point_id)
        self.pick(vertex)
        self.assertEqual(self.items.count(),1)
        self.pick('RootPoint',axis=True);self.apply.click();self.settle()
        self.assertEqual(self.sketch.GeometryCount,6)
        self.assertAlmostEqual(self.sketch.Geometry[5].X,-8)
        self.assertAlmostEqual(self.sketch.Geometry[5].Y,-6)
        self.done.click()
