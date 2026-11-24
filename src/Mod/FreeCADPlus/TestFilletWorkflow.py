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
        QtTest.QTest.keyRelease(Gui.getMainWindow(),QtCore.Qt.Key_Shift)
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

    def gesture(self, obj, sub='', remove=False, chain=False):
        from freecad_plus.selection_list import pick_intent
        controller = curve_selection._controller
        if chain:controller.picking = True
        with pick_intent(remove):Gui.Selection.addSelection(obj, sub)
        # Release modifier before queued chain delivery; intent must survive.
        controller.end_pick()
        QtTest.QTest.qWait(100)

    def test_shift_native_lists_and_delayed_chain(self):
        for command in ('PartDesign_Fillet', 'PartDesign_Chamfer', 'PartDesign_Draft'):
            self.enter(self.solid, command=command)
            self.clear()
            refs = ['Face1','Face2'] if command.endswith('Draft') else ['Edge1','Edge2']
            selection_toolbar.preferences().SetString('CurveIntent','Single Curve')
            self.gesture(self.solid,refs[0]);self.gesture(self.solid,refs[1])
            self.gesture(self.solid,refs[0])
            self.assertEqual(self.feature.Base[1],refs)
            self.gesture(self.solid,refs[0],True);self.assertEqual(self.feature.Base[1],[refs[1]])
            self.gesture(self.solid,refs[0],True);self.assertEqual(self.feature.Base[1],[refs[1]])
            self.gesture(self.solid,refs[1],True);self.assertFalse(self.feature.Base[1])
            if not command.endswith('Draft'):
                selection_toolbar.preferences().SetString('CurveIntent','Connected Curves')
                self.gesture(self.solid,'Edge1',chain=True);self.assertEqual(len(self.feature.Base[1]),12)
                self.gesture(self.solid,'Edge1',chain=True);self.assertEqual(len(self.feature.Base[1]),12)
                self.gesture(self.solid,'Edge1',True,True);self.assertFalse(self.feature.Base[1])
                self.assertFalse(curve_selection._controller.pending)
                self.assertFalse(curve_selection._controller.busy)
            if command.endswith('Draft'):
                for button_name,sub,prop in (('buttonPlane','Face3','NeutralPlane'),('buttonLine','Edge1','PullDirection')):
                    button=Gui.getMainWindow().findChild(QtWidgets.QToolButton,button_name)
                    button.setChecked(True)
                    self.gesture(self.solid,sub);self.assertEqual(getattr(self.feature,prop)[0],self.solid)
                    self.gesture(self.solid,sub,True);self.assertIsNone(getattr(self.feature,prop))
                    self.gesture(self.solid,sub,True);self.assertIsNone(getattr(self.feature,prop))
            self.cancel()

    def test_shift_python_profiles_and_single_references(self):
        from freecad_plus import extrude_task,revolve_task,loft_task,thicken_task,shell_task
        other = modeling.new_sketch(self.doc)
        for geo in self.sketch.Geometry:other.addGeometry(geo,False)
        other.Placement.Base.z=20;self.doc.recompute()
        sheet=self.owner.newObject('Part::Feature','Sheet');sheet.Shape=Part.makePlane(8,8);self.doc.recompute()
        for module,refs in ((extrude_task,[(self.sketch,'Edge1'),(self.sketch,'Edge2')]),
                            (revolve_task,[(self.sketch,'Edge1'),(self.sketch,'Edge2')]),
                            (loft_task,[(self.sketch,''),(other,'')]),
                            (thicken_task,[(sheet,'Face1')]),
                            (shell_task,[(self.solid,'Face1'),(self.solid,'Face2')])):
            Gui.Selection.clearSelection();task=module.show()
            try:
                if module in (extrude_task,revolve_task):task.outputs['Sheet'].click()
                for obj,sub in refs:self.gesture(obj,sub)
                expected=list(task.refs);self.assertEqual(len(expected),len(refs),(module.__name__,task.status.text()))
                self.gesture(*refs[0]);self.assertEqual(task.refs,expected)
                self.gesture(*refs[0],remove=True);self.assertEqual(task.refs,expected[1:])
                self.gesture(*refs[0],remove=True);self.assertEqual(task.refs,expected[1:])
                self.gesture(*refs[0]);self.assertEqual(task.refs,expected[1:]+expected[:1])
            finally:task.reject()
        task=extrude_task.show()
        try:
            task.modes['Add'].click();task.pick='target'
            self.gesture(self.solid);self.assertEqual(task.links['target'],(self.solid,''))
            task.pick='target';self.gesture(self.solid,remove=True)
            self.assertNotIn('target',task.links);task.changed();self.assertNotIn('target',task.links)
            task.pick='target';self.gesture(self.solid,remove=True);self.assertNotIn('target',task.links)
        finally:task.reject()

    def test_shift_placement_references_and_history_clicks(self):
        from freecad_plus import plane_task,sketch_task,panel,loft_task
        xy=next(o for o in self.owner.Origin.OriginFeatures if o.Role=='XY_Plane')
        xz=next(o for o in self.owner.Origin.OriginFeatures if o.Role=='XZ_Plane')
        point=self.owner.newObject('Part::Feature','Point');point.Shape=Part.Vertex(App.Vector(2,3,0));self.doc.recompute()
        for module in (plane_task,sketch_task):
            Gui.Selection.clearSelection();task=module.show()
            try:
                self.gesture(xy);self.gesture(xy);self.assertEqual(task.refs,[(xy,'')])
                self.gesture(xz);self.assertEqual(task.refs,[(xz,'')])
                self.gesture(xy,remove=True);self.assertEqual(task.refs,[(xz,'')])
                self.gesture(xz,remove=True);self.assertFalse(task.refs)
                self.gesture(xy);task.pick_target='origin'
                self.gesture(point,'Vertex1');self.gesture(point,'Vertex1');self.assertEqual(len(task.origin_refs),1)
                self.gesture(point,'Vertex1',True);self.assertFalse(task.origin_refs)
                task.pick_target='axis';self.gesture(self.sketch,'Edge1');self.gesture(self.sketch,'Edge1')
                self.assertEqual(len(task.axis_refs),1);self.gesture(self.sketch,'Edge1',True);self.assertFalse(task.axis_refs)
            finally:task.reject()
        other=modeling.new_sketch(self.doc);other.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2),False)
        self.doc.recompute();Gui.Selection.clearSelection();task=loft_task.show()
        try:
            p=panel._panel;p.refresh();QtTest.QTest.qWait(150);tree=p.trees[2]
            def click(obj,shift=False):
                p.refresh();QtTest.QTest.qWait(60)
                item=p._maps[2][('history',panel.identity(obj))];tree.scrollToItem(item)
                rect=tree.visualItemRect(item);pos=QtCore.QPoint(rect.left()+80,rect.center().y())
                QtTest.QTest.mouseClick(tree.viewport(),QtCore.Qt.LeftButton,
                                       QtCore.Qt.ShiftModifier if shift else QtCore.Qt.NoModifier,pos)
                QtTest.QTest.qWait(100)
            click(self.sketch);click(other);click(self.sketch)
            self.assertEqual([ref[0] for ref in task.refs],[self.sketch,other])
            click(other,True);self.assertEqual([ref[0] for ref in task.refs],[self.sketch])
            click(other,True);self.assertEqual([ref[0] for ref in task.refs],[self.sketch])
            click(self.sketch,True);self.assertFalse(task.refs)
        finally:task.reject()

    def test_real_shift_viewport_removes_connected_edges(self):
        self.enter(self.solid)
        for obj in self.doc.Objects:
            if obj.TypeId in ('App::Origin','App::Line','App::Plane','App::Point'):obj.Visibility=False
        selection_toolbar.preferences().SetString('CurveIntent','Connected Curves')
        view=Gui.activeDocument().activeView();view.setCameraType('Orthographic')
        view.setAnimationEnabled(False);view.viewTop();view.fitAll();view.getCameraNode().height=40
        QtTest.QTest.qWait(150)
        widget=view.graphicsView().viewport();ratio=widget.devicePixelRatioF()
        screen=view.getPointOnScreen(App.Vector(4,0,10))
        position=QtCore.QPoint(round(screen[0]/ratio),widget.height()-1-round(screen[1]/ratio))
        def click(shift=False):
            move=QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(position),
                QtCore.QPointF(widget.mapToGlobal(position)),QtCore.Qt.NoButton,QtCore.Qt.NoButton,QtCore.Qt.NoModifier)
            QtWidgets.QApplication.sendEvent(widget,move);QtTest.QTest.qWait(80)
            QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,
                                   QtCore.Qt.ShiftModifier if shift else QtCore.Qt.NoModifier,position)
            QtTest.QTest.qWait(150)
        click();self.assertEqual(len(self.feature.Base[1]),12)
        click();self.assertEqual(len(self.feature.Base[1]),12)
        click(True);self.assertFalse(self.feature.Base[1])
        click(True);self.assertFalse(self.feature.Base[1])
        click();self.assertEqual(len(self.feature.Base[1]),12)
        self.assertTrue(self.feature.Shape.isValid())

    def test_real_shift_extrude_and_shell_viewport(self):
        from freecad_plus import extrude_task,shell_task
        selection_toolbar.preferences().SetString('CurveIntent','Single Curve')
        for module,point in ((extrude_task,App.Vector(4,0,0)),(shell_task,App.Vector(10,6,10))):
            for obj in self.doc.Objects:
                if obj.TypeId in ('App::Origin','App::Line','App::Plane','App::Point'):obj.Visibility=False
            self.sketch.Visibility=module is extrude_task
            self.solid.Visibility=module is shell_task;self.body.Visibility=module is shell_task
            Gui.Selection.clearSelection();task=module.show()
            try:
                if module is extrude_task:task.outputs['Sheet'].click()
                view=Gui.activeDocument().activeView();view.setCameraType('Orthographic')
                view.setAnimationEnabled(False);view.viewTop();view.fitAll();view.getCameraNode().height=40
                QtTest.QTest.qWait(150)
                widget=view.graphicsView().viewport();ratio=widget.devicePixelRatioF()
                screen=view.getPointOnScreen(point)
                pos=QtCore.QPoint(round(screen[0]/ratio),widget.height()-1-round(screen[1]/ratio))
                def click(shift=False):
                    move=QtGui.QMouseEvent(QtCore.QEvent.MouseMove,QtCore.QPointF(pos),
                        QtCore.QPointF(widget.mapToGlobal(pos)),QtCore.Qt.NoButton,QtCore.Qt.NoButton,QtCore.Qt.NoModifier)
                    QtWidgets.QApplication.sendEvent(widget,move);QtTest.QTest.qWait(80)
                    QtTest.QTest.mouseClick(widget,QtCore.Qt.LeftButton,
                        QtCore.Qt.ShiftModifier if shift else QtCore.Qt.NoModifier,pos)
                    QtTest.QTest.qWait(150)
                click();self.assertEqual(len(task.refs),1,(module.__name__,task.status.text()))
                before=list(task.refs);click();self.assertEqual(task.refs,before)
                Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks').grab().save(str(self.output/(task.title+'-selected.png')))
                click(True);self.assertFalse(task.refs)
                click(True);self.assertFalse(task.refs)
                if module is extrude_task:
                    for i in range(4):self.gesture(self.sketch,'Edge'+str(i+1))
                    screen=view.getPointOnScreen(App.Vector(10,6,0))
                    pos=QtCore.QPoint(round(screen[0]/ratio),widget.height()-1-round(screen[1]/ratio))
                    click(True);self.assertFalse(task.refs)
                    self.gesture(self.sketch)
                    self.gesture(self.sketch,'Edge1');self.assertEqual(task.refs,[(self.sketch,'')])
                    screen=view.getPointOnScreen(App.Vector(4,0,0))
                    pos=QtCore.QPoint(round(screen[0]/ratio),widget.height()-1-round(screen[1]/ratio))
                    click(True);self.assertEqual(len(task.refs),3)
                    task.clear_profile()
                Gui.getMainWindow().findChild(QtWidgets.QDockWidget,'Tasks').grab().save(str(self.output/(task.title+'-removed.png')))
            finally:task.reject()

    def test_legacy_whole_solid_still_offers_native_all_edges(self):
        legacy=App.newDocument('LegacyFillet')
        body=legacy.addObject('PartDesign::Body','Body')
        box=body.newObject('PartDesign::AdditiveBox','Box');legacy.recompute()
        Gui.activeDocument().activeView().setActiveObject('pdbody',body)
        feature=self.enter(box)
        self.assertTrue(feature.UseAllEdges);self.assertEqual(len(feature.Base[1]),12)
        self.cancel();App.closeDocument(legacy.Name)
