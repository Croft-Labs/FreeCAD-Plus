# SPDX-License-Identifier: LGPL-2.1-or-later
"""Regression for consuming task picks and explicit Plus Fillet edges."""
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtGui, QtTest, QtWidgets
from freecad_plus import curve_selection, document, extrusion, modeling, selection_toolbar
from TestFeatureCenteredModeling import TestFeatureCenteredModeling
from TestComponentModeling import accept_task, messages


class TestFilletWorkflow(unittest.TestCase):
    def setUp(self):
        TestFeatureCenteredModeling.setUp(self)
        Gui.activateWorkbench('PartDesignWorkbench')
        self.intent = curve_selection.intent()
        curve_selection.apply(True)
        self.sketch = modeling.new_sketch(self.doc)
        points = [App.Vector(0,0,0), App.Vector(20,0,0), App.Vector(20,12,0), App.Vector(0,12,0)]
        for i in range(4):
            self.sketch.addGeometry(Part.LineSegment(points[i], points[(i+1)%4]), False)
        self.doc.recompute()
        self.solid = extrusion.save(self.doc, [(self.sketch,'')], {}, dict(extrusion.DEFAULTS,length=10))
        self.body = self.solid.getParentGeoFeatureGroup()

    def tearDown(self):
        curve_selection._controller.end_pick()
        selection_toolbar.preferences().SetString('CurveIntent', self.intent)
        if Gui.activeDocument() and Gui.activeDocument().getInEdit():
            Gui.activeDocument().resetEdit();self.doc.abortTransaction()
        TestFeatureCenteredModeling.tearDown(self)

    def enter(self, target=None, sub='', command='PartDesign_Fillet'):
        Gui.Selection.clearSelection()
        if target:Gui.Selection.addSelection(target, sub)
        with messages() as errors:Gui.runCommand(command)
        self.assertFalse(errors, errors)
        QtTest.QTest.qWait(100)
        self.feature = Gui.activeDocument().getInEdit().Object
        self.button = Gui.getMainWindow().findChild(QtWidgets.QToolButton,'buttonRefSel')
        self.items = Gui.getMainWindow().findChild(QtWidgets.QListWidget,'listWidgetReferences')
        return self.feature

    def pick(self, edge, mode='Single Curve'):
        selection_toolbar.preferences().SetString('CurveIntent', mode)
        self.button.setChecked(True)
        controller = curve_selection._controller
        controller.picking = True
        QtCore.QTimer.singleShot(0, controller.end_pick)
        Gui.Selection.addSelection(self.solid, edge)
        QtTest.QTest.qWait(100)

    def clear(self):
        self.items.selectAll()
        next(a for a in self.items.actions() if a.text()=='Remove').trigger()
        self.assertFalse(self.feature.Base[1])

    def cancel(self):
        box=next(box for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)
                 if box.isVisible() and box.button(QtWidgets.QDialogButtonBox.Cancel))
        QtTest.QTest.mouseClick(box.button(QtWidgets.QDialogButtonBox.Cancel),QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(50)

    def test_whole_solid_and_empty_entry_require_explicit_edges(self):
        for selected in (self.solid, self.body, None):
            Gui.activeDocument().activeView().setActiveObject('pdbody',None)
            feature = self.enter(selected)
            self.assertEqual(feature.Base[0],self.solid)
            self.assertFalse(feature.Base[1]);self.assertFalse(feature.UseAllEdges)
            self.assertTrue(self.button.isChecked());self.assertTrue(self.items.isEnabled())
            self.pick('Edge1');self.assertEqual(feature.Base[1],['Edge1'])
            self.assertTrue(feature.Shape.isValid())
            self.cancel()

    def test_clear_and_connected_pick_drains_native_notifications_once(self):
        self.enter(self.solid,'Edge1')
        for _ in range(3):
            self.clear()
            self.pick('Edge1','Connected Curves')
            self.assertEqual(set(self.feature.Base[1]),{'Edge'+str(i) for i in range(1,13)})
            self.assertEqual(self.items.count(),12)
            self.assertFalse(self.feature.UseAllEdges)
            self.assertTrue(self.feature.Shape.isValid())
            self.assertFalse(curve_selection._controller.pending)
        self.clear();self.pick('Edge1')
        self.assertEqual(self.feature.Base[1],['Edge1'])
        volume=self.feature.Shape.Volume;name=self.feature.Name;identity=self.feature.ID
        accept_task();self.doc.undo();self.assertIsNone(self.doc.getObject(name))
        self.doc.redo();self.assertEqual(self.doc.getObject(name).ID,identity)
        self.assertAlmostEqual(self.doc.getObject(name).Shape.Volume,volume)
        document.save_document(self.doc,self.output/'Fillet.cadprt')

    def test_tangent_pick_and_shared_chamfer_collector(self):
        for command in ('PartDesign_Fillet','PartDesign_Chamfer'):
            Gui.activeDocument().activeView().setActiveObject('pdbody',self.body)
            self.enter(self.solid,'Edge1',command)
            self.clear();self.pick('Edge1','Tangent Curves')
            self.assertEqual(self.feature.Base[1],['Edge1'])
            self.clear();self.pick('Edge1','Connected Curves')
            self.assertEqual(len(self.feature.Base[1]),12)
            self.assertTrue(self.feature.Shape.isValid())
            self.cancel()

    def test_selected_solid_ignores_other_active_body(self):
        other=self.owner.newObject('PartDesign::Body','OtherBody')
        box=other.newObject('PartDesign::AdditiveBox','OtherBox');self.doc.recompute()
        Gui.activeDocument().activeView().setActiveObject('pdbody',other)
        feature=self.enter(self.solid,'Edge1')
        self.assertEqual(feature.getParentGeoFeatureGroup(),self.body)
        self.assertEqual(other.Tip,box)
        self.assertEqual(Gui.activeDocument().activeView().getActiveObject('pdbody'),other)

    def test_queued_chain_cannot_select_after_task_cancel(self):
        self.enter(self.solid,'Edge1');self.clear();self.button.setChecked(True)
        selection_toolbar.preferences().SetString('CurveIntent','Connected Curves')
        curve_selection._controller.picking=True
        Gui.Selection.addSelection(self.solid,'Edge1')
        self.cancel();Gui.Selection.clearSelection()
        QtTest.QTest.qWait(100)
        self.assertFalse(Gui.Selection.getSelection())
        self.assertFalse(curve_selection._controller.pending)

    def test_real_viewport_pick_after_clearing_edges(self):
        self.enter(self.solid,'Edge1');self.clear();self.button.setChecked(True)
        for obj in self.doc.Objects:
            if obj.TypeId in ('App::Origin','App::Line','App::Plane'):obj.Visibility=False
        selection_toolbar.preferences().SetString('CurveIntent','Connected Curves')
        view=Gui.activeDocument().activeView();view.setCameraType('Orthographic')
        view.setAnimationEnabled(False);view.viewTop();view.fitAll()
        view.getCameraNode().height=40;QtTest.QTest.qWait(150)
        widget=view.graphicsView().viewport();ratio=widget.devicePixelRatioF()
        screen=view.getPointOnScreen(App.Vector(10,0,10))
        position=QtCore.QPoint(round(screen[0]/ratio),widget.height()-1-round(screen[1]/ratio))
        event=QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(position),
                               QtCore.QPointF(widget.mapToGlobal(position)),QtCore.Qt.NoButton,
                               QtCore.Qt.NoButton,QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(widget,event);QtTest.QTest.qWait(80)
        QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,QtCore.Qt.NoModifier,position)
        QtTest.QTest.qWait(150)
        self.assertEqual(set(self.feature.Base[1]),{'Edge'+str(i) for i in range(1,13)})
        self.assertTrue(self.feature.Shape.isValid())
        Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks').grab().save(
            str(self.output/'fillet-after-clear.png'))

    def test_legacy_whole_solid_still_offers_native_all_edges(self):
        legacy=App.newDocument('LegacyFillet')
        body=legacy.addObject('PartDesign::Body','Body')
        box=body.newObject('PartDesign::AdditiveBox','Box');legacy.recompute()
        Gui.activeDocument().activeView().setActiveObject('pdbody',body)
        feature=self.enter(box)
        self.assertTrue(feature.UseAllEdges);self.assertEqual(len(feature.Base[1]),12)
        self.cancel();App.closeDocument(legacy.Name)
