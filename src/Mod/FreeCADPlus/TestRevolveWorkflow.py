# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native checks for the combined Revolve and shared selection collector."""
import math
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, modeling, revolution, revolve_task, extrude_task, extrusion, editing, panel, planes
from TestFeatureCenteredModeling import TestFeatureCenteredModeling


class TestRevolveWorkflow(unittest.TestCase):
    circle = TestFeatureCenteredModeling.circle
    snapshot = TestFeatureCenteredModeling.snapshot

    def setUp(self):
        TestFeatureCenteredModeling.setUp(self)
        self.prefs = App.ParamGet('User parameter:BaseApp/Preferences/General')
        self.previous = self.prefs.GetInt('TaskPanelUIMode', 0);self.prefs.SetInt('TaskPanelUIMode', 0)
        Gui.activateWorkbench('PartDesignWorkbench')

    def tearDown(self):
        if extrude_task._active:extrude_task._active.reject()
        self.prefs.SetInt('TaskPanelUIMode', self.previous)
        TestFeatureCenteredModeling.tearDown(self)

    def profile(self, x=2, z=1):
        sketch = modeling.new_sketch(self.doc)
        sketch.Placement = App.Placement(App.Vector(), App.Rotation(App.Vector(1, 0, 0), 90))
        points = [(x,z),(x+1,z),(x+2,z),(x+2,z+1),(x+2,z+2),(x+1,z+2),(x,z+2),(x,z+1)]
        for i,p in enumerate(points):
            q = points[(i+1)%8];sketch.addGeometry(Part.LineSegment(App.Vector(*p,0),App.Vector(*q,0)),False)
        self.doc.recompute();return sketch

    def values(self, **kwargs):return dict(revolution.DEFAULTS, axis='Component Z axis', **kwargs)

    def evaluate(self, sketch, links=None, **kwargs):
        return revolution.evaluate(self.owner, [(sketch,'')], links or {}, self.values(**kwargs))

    def save(self, sketch, links=None, feature=None, **kwargs):
        return revolution.save(self.doc, [(sketch,'')], links or {}, self.values(**kwargs), feature)

    def target(self):return modeling.extrude_new_solid(self.doc,self.circle(5),2)

    def task(self, sketch, mode='New Solid', target=None):
        Gui.Selection.clearSelection();Gui.Selection.addSelection(sketch)
        task = revolve_task.show();task.axis.setCurrentText('Component Z axis');task.modes[mode].click()
        if target:
            task.fields['target'].setFocus();QtTest.QTest.qWait(50);Gui.Selection.addSelection(target);QtTest.QTest.qWait(50)
        return task

    def test_angles_offset_reverse_symmetric_and_two_sides(self):
        sketch=self.profile();before=self.snapshot();docs=set(App.listDocuments())
        for values in (dict(angle=90),dict(angle=90,reverse=True),dict(angle=90,sides='Symmetric'),
                       dict(angle=45,angle2=45,sides='Two sides'),dict(angle=90,start='Offset',start_offset=15)):
            result,tool,_=self.evaluate(sketch,**values)
            self.assertTrue(result.isValid());self.assertAlmostEqual(tool.Volume,6*math.pi,places=5)
        self.assertEqual(self.snapshot(),before);self.assertEqual(set(App.listDocuments()),docs)
        forward=self.evaluate(sketch,angle=90)[0];reverse=self.evaluate(sketch,angle=90,reverse=True)[0]
        self.assertGreater(forward.CenterOfMass.y,0);self.assertLess(reverse.CenterOfMass.y,0)
        symmetric=self.evaluate(sketch,angle=90,sides='Symmetric')[0];self.assertAlmostEqual(symmetric.CenterOfMass.y,0,places=5)
        with self.assertRaises(ValueError):self.evaluate(sketch,angle=300,angle2=90,sides='Two sides')

    def test_add_subtract_and_invalid_tools(self):
        target=self.target();sketch=self.profile();links={'target':(target,'')}
        add=self.evaluate(sketch,links,operation='Add',angle=90)[0]
        cut=self.evaluate(sketch,links,operation='Subtract',angle=90)[0]
        self.assertAlmostEqual(add.Volume-target.Shape.Volume,3*math.pi,places=5)
        self.assertAlmostEqual(target.Shape.Volume-cut.Volume,3*math.pi,places=5)
        far=self.profile(x=8,z=5)
        for operation in ('Add','Subtract'):
            with self.assertRaises(revolution.InvalidResult) as caught:self.evaluate(far,links,operation=operation,angle=90)
            self.assertTrue(caught.exception.tool.isValid())
        self.assertAlmostEqual(self.evaluate(sketch,links,operation='Subtract',end='Through all')[1].Volume,24*math.pi,places=5)

    def test_save_edit_identity_undo_and_reopen(self):
        target=self.target();sketch=self.profile();links={'target':(target,'')}
        feature=self.save(sketch,links,operation='Add',angle=90);identity=feature.ID;name=feature.Name
        self.save(sketch,links,feature,operation='Subtract',angle=180)
        self.assertEqual(feature.ID,identity);self.assertEqual(feature.Revolve_operation,'Subtract')
        self.doc.undo();self.doc.recompute();self.assertEqual(feature.Revolve_operation,'Add')
        self.doc.redo();self.doc.recompute();self.assertEqual(feature.Revolve_operation,'Subtract')
        volume=feature.Shape.Volume;path=self.output/'Revolve.cadprt';document.save_document(self.doc,path)
        App.closeDocument(self.doc.Name);self.doc=document.open_document(path);feature=self.doc.getObject(name)
        self.doc.recompute();self.assertEqual(feature.ID,identity);self.assertAlmostEqual(feature.Shape.Volume,volume)
        self.assertTrue(revolution.is_revolution(feature));self.assertEqual(feature.Proxy.__class__.__name__,'Revolve')

    def test_axis_references_and_transformed_sketch(self):
        sketch=self.profile();shape=self.evaluate(sketch,angle=90)[0]
        ref=self.owner.newObject('PartDesign::Line','RotationAxis');ref.Placement.Base.x=0
        self.doc.recompute()
        values=dict(self.values(angle=90),axis='Selected axis / line')
        result=revolution.evaluate(self.owner,[(sketch,'')],{'axis':(ref,'')},values)[0]
        self.assertAlmostEqual(result.Volume,shape.Volume)
        values=dict(self.values(angle=90),axis='Sketch vertical axis')
        sketch.Placement.Base=App.Vector(10,3,2);self.doc.recompute()
        result=revolution.evaluate(self.owner,[(sketch,'')],{},values)[0]
        self.assertAlmostEqual(result.Volume,shape.Volume)
        self.assertGreater(result.BoundBox.XMin,9)
        with self.assertRaises(ValueError):self.evaluate(sketch,angle=90)

    def test_face_profile_and_invalid_axis(self):
        sketch=self.profile();face=extrusion.profile_shape(self.owner,[(sketch,'')])[0]
        sheet=self.owner.newObject('Part::Feature','Sheet');sheet.Shape=face;self.doc.recompute()
        result=revolution.evaluate(self.owner,[(sheet,'Face1')],{},self.values(angle=90))[0]
        self.assertAlmostEqual(result.Volume,6*math.pi,places=5)
        with self.assertRaises(ValueError):revolution.evaluate(self.owner,[(sheet,'Face1')],{},dict(self.values(),axis='Component Y axis'))
        crossing=self.profile(x=-1)
        with self.assertRaises(ValueError):self.evaluate(crossing,angle=90)

    def test_reference_start_and_face_limit(self):
        sketch=self.profile()
        limit=self.owner.newObject('PartDesign::Plane','Limit')
        limit.Placement=App.Placement(App.Vector(),App.Rotation(App.Vector(0,1,0),90));self.doc.recompute()
        result,tool,_=self.evaluate(sketch,{'limit':(limit,'')},end='Up to face',angle=90)
        self.assertTrue(result.isValid());self.assertAlmostEqual(tool.Volume,6*math.pi,places=4)
        result=self.evaluate(sketch,{'limit':(limit,'')},end='Up to face',offset=15)[0]
        self.assertAlmostEqual(result.Volume,7*math.pi,places=4)
        result=self.evaluate(sketch,{'start':(limit,'')},start='Reference',angle=45)[0]
        self.assertAlmostEqual(result.Volume,3*math.pi,places=4)

    def test_real_commands_shared_edit_history_and_cancel(self):
        sketch=self.profile();dock=panel.show_panel();dock.tabs.setCurrentIndex(0)
        Gui.Selection.clearSelection();Gui.Selection.addSelection(sketch);Gui.runCommand('PartDesign_Revolution')
        task=extrude_task._active;self.assertIsInstance(task,revolve_task.RevolveTask)
        self.assertEqual(dock.tabs.currentIndex(),2);task.axis.setCurrentText('Component Z axis')
        self.assertTrue(task.valid,task.status.text());self.assertTrue(task.accept());feature=task.result
        self.assertEqual(dock.tabs.currentIndex(),0)
        editing.edit_feature(self.doc,feature);task=extrude_task._active
        self.assertEqual(task.axis.currentText(),'Component Z axis');self.assertTrue(task.valid)
        task.reject();self.assertEqual(dock.tabs.currentIndex(),0)
        Gui.Selection.clearSelection();Gui.Selection.addSelection(sketch);Gui.runCommand('PartDesign_Groove')
        task=extrude_task._active;self.assertEqual(task.mode(),'Subtract');task.reject()

    def test_task_target_colors_invalid_accept_and_numeric_commit(self):
        target=self.target();sketch=self.profile();target.Visibility=False
        task=self.task(sketch,'Add',target);self.assertTrue(task.valid,task.status.text())
        self.assertIsNotNone(task.target_overlay);self.assertFalse(target.Visibility)
        field=task.end1['length'];field.setFocus();QtTest.QTest.qWait(50);revision=task.revisions
        field.selectAll();QtTest.QTest.keyClicks(field,'90');self.assertEqual(task.revisions,revision)
        task.reverse.setFocus();QtTest.QTest.qWait(50);self.assertEqual(task.values[field],90)
        task.reject();self.assertFalse(target.Visibility)
        far=self.profile(x=8,z=5)
        for mode in ('Add','Subtract'):
            task=self.task(far,mode,target);self.assertFalse(task.valid)
            self.assertIsNotNone(task.tool_preview);self.assertIsNotNone(task.target_overlay)
            before=self.snapshot();self.assertFalse(task.accept());self.assertEqual(self.snapshot(),before);task.reject()

    def test_selection_list_five_rows_long_names_font_and_scrolling(self):
        sketch=self.profile();sketch.Label='Long radial profile '+('name '*20)
        for factory in (extrude_task.show,revolve_task.show):
            Gui.Selection.clearSelection();Gui.Selection.addSelection(sketch);task=factory()
            task.refs=[(sketch,'Edge'+str(i)) for i in range(1,9)];task.refresh_fields();QtTest.QTest.qWait(60)
            rows=task.profiles;font=rows.font();font.setPointSize(font.pointSize()+3);rows.setFont(font);QtTest.QTest.qWait(60)
            rows.scrollToTop();QtTest.QTest.qWait(40)
            self.assertGreaterEqual(sum(0 <= rows.visualItemRect(rows.item(i)).top() and rows.visualItemRect(rows.item(i)).bottom() < rows.viewport().height() for i in range(8)),5)
            rows.scrollToBottom();self.assertTrue(rows.viewport().rect().intersects(rows.visualItemRect(rows.item(7))))
            self.assertEqual(rows.item(7).toolTip(),rows.item(7).text());task.reject()

    def test_cycles_rerouting_and_downstream_references(self):
        sketch=self.profile();feature=self.save(sketch,angle=90);identity=feature.ID
        target=self.target();self.save(sketch,{'target':(target,'')},feature,operation='Add',angle=90)
        self.assertEqual(feature.ID,identity);self.assertEqual(feature.getParentGeoFeatureGroup(),target.getParentGeoFeatureGroup())
        with self.assertRaises(ValueError):self.save(sketch,{'target':(feature,'')},feature,operation='Add',angle=90)
        downstream=extrusion.save(self.doc,[(self.circle(1),'')],{'target':(feature,'')},dict(extrusion.DEFAULTS,operation='Add',length=3))
        self.save(sketch,{'target':(target,'')},feature,operation='Add',angle=180)
        self.assertTrue(downstream.Shape.isValid());self.assertEqual(feature.ID,identity)
        with self.assertRaises(ValueError):self.save(sketch,feature=feature,angle=90)

    def test_external_source_ownership_and_recompute(self):
        from freecad_plus import external
        document.save_document(self.doc,self.output/'Host.cadprt')
        source=document.new_document('RevolveSource');owner=document.validate(source).Definitions[0]
        document.save_document(source,self.output/'Source.cadprt');external.import_file(self.doc,source)
        App.setActiveDocument(self.doc.Name);editing.edit_unused(self.doc,owner);self.owner=owner
        sketch=self.profile();source.recompute()
        feature=self.save(sketch,angle=90);self.assertEqual(feature.Document,source)
        identity=feature.ID;self.assertAlmostEqual(feature.Shape.Volume,6*math.pi,places=5)
        task=revolve_task.show(feature);self.assertTrue(task.valid,task.status.text());task.reject()
        sketch.Placement.Base.z=2;source.recompute()
        self.assertEqual(feature.ID,identity);self.assertAlmostEqual(feature.Shape.Volume,6*math.pi,places=5)
        self.assertAlmostEqual(feature.Shape.BoundBox.ZMin,3,places=5)
