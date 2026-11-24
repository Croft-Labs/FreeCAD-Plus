# SPDX-License-Identifier: LGPL-2.1-or-later
"""Spacing relationships and quantity presentation, using the native solver."""
import math
import os
from pathlib import Path
import unittest
import FreeCAD as App
import Part
import Sketcher
from PySide6 import QtOpenGLWidgets  # Register the viewport wrapper before fixtures obtain it.
import TestSketchPattern as pattern_tests
from freecad_plus import sketch_pattern as pattern


extent, linear, circular = pattern_tests.extent, pattern_tests.linear, pattern_tests.circular


class TestSpacingChains(unittest.TestCase):
    setUp = pattern_tests.TestPatternGeometry.setUp
    tearDown = pattern_tests.TestPatternGeometry.tearDown
    assertVector = pattern_tests.TestPatternGeometry.assertVector
    def test_one_length_driver_and_equal_connected_lines(self):
        self.s.addGeometry(Part.Circle(App.Vector(5,3,0),App.Vector(0,0,1),1))
        copies=pattern.apply(self.s,[0],linear(d1=extent(count=5)),True)
        helpers=[i for i in range(self.s.GeometryCount) if self.s.getConstruction(i)]
        lengths=[i for i,c in enumerate(self.s.Constraints) if c.Type=='Distance']
        self.assertEqual(len(helpers),4);self.assertEqual(len(lengths),1)
        self.assertEqual(sum(c.Type=='Equal' and c.First in helpers for c in self.s.Constraints),3)
        self.s.setDatum(lengths[0],App.Units.Quantity('12.123456 mm'));self.doc.recompute()
        for n,i in enumerate(copies,1):
            self.assertAlmostEqual((self.s.Geometry[i].Center-self.s.Geometry[0].Center).x,n*12.123456,places=6)
        for a,b in zip(helpers,helpers[1:]):
            self.assertVector(self.s.getPoint(a,2),tuple(self.s.getPoint(b,1)))

    def test_four_pitch_masters_and_hidden_reopen(self):
        self.s.addGeometry(Part.Circle(App.Vector(5,3,0),App.Vector(0,0,1),1))
        opts=linear(directions='Two directions',hide_spacing=True,
                    d1=extent(mode='Two dimensions',count2=2,value2=7),
                    d2=extent(reference=(-2,0),mode='Two dimensions',count2=2,value=8,value2=6))
        copies=pattern.apply(self.s,[0],opts,True)
        self.assertEqual(len(copies),15)
        self.assertEqual(sum(c.Type=='Distance' for c in self.s.Constraints),4)
        tags=set(self.s.PatternSpacingTags)
        self.assertTrue(all(pattern.visual_layer(f)==2 for f in self.s.GeometryFacadeList if pattern.spacing_tag(f) in tags))
        before=self.s.DoF
        pattern.set_chain_hidden(self.s,False)
        self.assertEqual(self.s.solve(),0);self.assertEqual(self.s.DoF,before)
        self.assertTrue(all(pattern.visual_layer(f)==0 for f in self.s.GeometryFacadeList if pattern.spacing_tag(f) in tags))
        if os.environ.get('PLUS_TEST_DIR'):
            path=str(Path(os.environ['PLUS_TEST_DIR'])/'spacing-hidden.FCStd')
            pattern.set_chain_hidden(self.s,True);self.doc.saveAs(path)
            App.closeDocument(self.doc.Name);self.doc=App.openDocument(path);self.s=self.doc.Sketch
            self.assertEqual(set(self.s.PatternSpacingTags),tags)
            self.assertTrue(pattern.chain_is_hidden(self.s))
            self.assertEqual(sum(pattern.spacing_tag(f) in tags for f in self.s.GeometryFacadeList),len(tags))
            self.assertTrue(all(pattern.visual_layer(f)==2 for f in self.s.GeometryFacadeList if pattern.spacing_tag(f) in tags))

    def test_angular_arcs_radial_lines_and_pitch_edit(self):
        self.s.addGeometry(Part.Circle(App.Vector(20,0,0),App.Vector(0,0,1),1))
        opts=circular(directions='Angular + radial',angular=extent(spacing='Angular pitch',value=30,count=3),
                      radial=extent(reference=(0,3),value=5,count=3),hide_spacing=True)
        copies=pattern.apply(self.s,[0],opts,True)
        self.assertEqual(len(copies),8)
        helpers=[g for i,g in enumerate(self.s.Geometry) if self.s.getConstruction(i)]
        self.assertEqual(sum(isinstance(g,Part.ArcOfCircle) for g in helpers),6)
        self.assertEqual(sum(isinstance(g,Part.LineSegment) for g in helpers),3) # Two pitches plus the reference ray.
        angles=[i for i,c in enumerate(self.s.Constraints) if c.Type=='Angle']
        self.assertEqual(len(angles),6)
        self.assertEqual(len(self.s.ExpressionEngine),5)
        self.s.setDatum(angles[0],App.Units.Quantity('40 deg'));self.doc.recompute()
        for i in angles:self.assertAlmostEqual(self.s.Constraints[i].Value,math.radians(40),places=6)
        self.assertEqual(self.s.solve(),0)


class TestQuantityControls(unittest.TestCase):
    def setUp(self):
        from PySide6 import QtWidgets, QtTest, QtCore
        from freecad_plus.quantity_fields import QuantityNumber
        self.QtWidgets,self.QtTest,self.QtCore=QtWidgets,QtTest,QtCore
        self.window=QtWidgets.QWidget();layout=QtWidgets.QVBoxLayout(self.window)
        self.field=QuantityNumber();self.field.setRange(-100000,100000)
        layout.addWidget(self.field);self.other=QtWidgets.QLineEdit();layout.addWidget(self.other)
        self.window.show();self.QtTest.QTest.qWait(20)

    def tearDown(self):self.window.close()

    def enter(self,text):
        self.field.setFocus();self.field.selectAll()
        self.QtTest.QTest.keyClicks(self.field,text)
        self.other.setFocus();self.QtTest.QTest.qWait(10)

    def test_six_decimals_units_and_steps(self):
        self.enter('1.29999 mm');self.assertAlmostEqual(self.field.value(),1.29999,places=10)
        self.enter('0.100 in');self.assertAlmostEqual(self.field.value(),2.54,places=10)
        self.assertEqual(self.field._unit,'in');self.assertIn('0.100 in',self.field.text())
        self.enter('0.123456 in');self.assertAlmostEqual(self.field.value(),.123456*25.4,places=10)
        self.assertIn('0.123456 in',self.field.text())
        self.field.stepBy(1);self.assertAlmostEqual(self.field.value(),1.123456*25.4,places=10)

    def test_bare_number_uses_current_unit_and_invalid_is_rejected(self):
        self.enter('0.100 in');self.enter('0.200')
        self.assertAlmostEqual(self.field.value(),5.08,places=10)
        self.enter('4 deg');self.assertAlmostEqual(self.field.value(),5.08,places=10)

    def test_existing_precision_and_compatible_expression(self):
        self.field.setValue(1.2345678912345)
        self.field.interpretText();self.assertAlmostEqual(self.field.value(),1.2345678912345,places=13)
        self.assertAlmostEqual(self.field.parse('1 in + 2 mm'),27.4,places=10)
        self.enter('1 in + 2 mm');self.assertAlmostEqual(self.field.value(),27.4,places=10,msg=self.field.text())

    def test_metadata_undo_copy_and_reopen(self):
        from freecad_plus.quantity_fields import save,restore
        doc=App.newDocument('QuantityMetadata');doc.UndoMode=1
        try:
            feature=doc.addObject('PartDesign::Feature','Feature')
            doc.openTransaction('Units');save(feature,{'Length':'in'});doc.commitTransaction()
            self.assertEqual(feature.QuantityPresentationUnits['Length'],'in')
            doc.undo();self.assertNotIn('QuantityPresentationUnits',feature.PropertiesList)
            doc.redo();restore(feature,{'Length':self.field});self.assertEqual(self.field._unit,'in')
            copied=doc.copyObject(feature);self.assertEqual(copied.QuantityPresentationUnits['Length'],'in')
            if os.environ.get('PLUS_TEST_DIR'):
                path=str(Path(os.environ['PLUS_TEST_DIR'])/'quantity-units.FCStd')
                doc.saveAs(path);App.closeDocument(doc.Name);doc=App.openDocument(path)
                self.assertEqual(doc.Feature.QuantityPresentationUnits['Length'],'in')
        finally:App.closeDocument(doc.Name)


class TestNativeUnits(unittest.TestCase):
    def test_bound_native_property_retains_units(self):
        import FreeCADGui as Gui
        from PySide6 import QtWidgets,QtTest
        doc=App.newDocument('BoundUnits');doc.UndoMode=1
        window=QtWidgets.QWidget();layout=QtWidgets.QVBoxLayout(window)
        try:
            obj=doc.addObject('PartDesign::Feature','Feature');obj.addProperty('App::PropertyLength','Length');obj.Length=2.54
            field=Gui.UiLoader().createWidget('Gui::QuantitySpinBox')
            field.setProperty('unit','mm');field.setProperty('rawValue',2.54)
            layout.addWidget(field);other=QtWidgets.QLineEdit();layout.addWidget(other)
            field.setProperty('binding',doc.Name+'#'+obj.Name+'.Length')
            self.assertNotIn('QuantityPresentationUnits',obj.PropertiesList)
            window.show();QtTest.QTest.qWait(20)
            doc.openTransaction('Edit quantity')
            field.setFocus();edit=field.findChild(QtWidgets.QLineEdit);edit.selectAll();QtTest.QTest.keyClicks(edit,'0.100 in')
            other.setFocus();QtTest.QTest.qWait(20);doc.commitTransaction()
            self.assertEqual(obj.QuantityPresentationUnits['Length'],'in')
            field2=Gui.UiLoader().createWidget('Gui::QuantitySpinBox');layout.addWidget(field2)
            field2.setProperty('unit','mm');field2.setProperty('rawValue',2.54)
            field2.setProperty('binding',doc.Name+'#'+obj.Name+'.Length')
            self.assertEqual(field2.findChild(QtWidgets.QLineEdit).text(),'0.100 in')
            doc.undo();self.assertNotIn('QuantityPresentationUnits',obj.PropertiesList)
        finally:window.close();App.closeDocument(doc.Name)

    def test_secondary_preferences(self):
        import FreeCADGui as Gui
        from PySide6 import QtWidgets,QtCore
        seen=[];errors=[]
        def inspect():
            dialog=QtWidgets.QApplication.activeModalWidget()
            if not dialog:return
            secondary=dialog.findChild(QtWidgets.QComboBox,'SecondaryUnits')
            if secondary is None:return
            timer.stop()
            try:
                decimals=dialog.findChild(QtWidgets.QSpinBox,'SecondaryDecimals')
                secondary.setCurrentIndex(3);decimals.setValue(3)
                box=dialog.findChild(QtWidgets.QDialogButtonBox)
                button=box.button(QtWidgets.QDialogButtonBox.Apply)
                self.assertIsNotNone(button);button.click()
                prefs=App.ParamGet('User parameter:BaseApp/Preferences/Units')
                self.assertEqual(prefs.GetInt('SecondarySchema'),3)
                self.assertEqual(prefs.GetInt('SecondaryDecimals'),3)
                seen.append(True)
                if os.environ.get('PLUS_TEST_DIR'):dialog.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'native-general-units.png'))
            except BaseException as error:errors.append(repr(error))
            dialog.reject()
        timer=QtCore.QTimer();timer.timeout.connect(inspect);timer.start(50)
        watchdog=QtCore.QTimer();watchdog.setSingleShot(True)
        watchdog.timeout.connect(lambda: QtWidgets.QApplication.activeModalWidget().reject() if QtWidgets.QApplication.activeModalWidget() else None)
        watchdog.start(8000)
        Gui.runCommand('Std_DlgPreferences');timer.stop();watchdog.stop()
        self.assertFalse(errors,errors);self.assertEqual(seen,[True])

    def test_dimension_editor_and_leaders(self):
        import FreeCADGui as Gui
        from PySide6 import QtWidgets,QtTest,QtCore
        from pivy import coin
        prefs=App.ParamGet('User parameter:BaseApp/Preferences/Units')
        prefs.SetInt('Decimals',2);prefs.SetInt('SecondarySchema',3);prefs.SetInt('SecondaryDecimals',3)
        App.Units.setSchema(0)
        doc=App.newDocument('DimensionPresentation')
        try:
            s=doc.addObject('Sketcher::SketchObject','Sketch')
            for index,(value,unit) in enumerate(((1.29999,'mm'),(2.54,'in'))):
                s.addGeometry(Part.LineSegment(App.Vector(0,index*2,0),App.Vector(value,index*2,0)))
                c=Sketcher.Constraint('Distance',index,value);c.PresentationUnit=unit;s.addConstraint(c)
            doc.recompute();Gui.activateWorkbench('SketcherWorkbench');Gui.activeDocument().setEdit(s.Name)
            Gui.activeDocument().activeView().fitAll();QtTest.QTest.qWait(100)
            search=coin.SoSearchAction();search.setType(coin.SoType.fromName('SoDatumLabel'))
            search.setInterest(coin.SoSearchAction.ALL);search.setSearchingAll(True)
            search.apply(Gui.activeDocument().activeView().getSceneGraph())
            texts=[]
            for path in search.getPaths():texts.extend(path.getTail().getField('string').getValues())
            self.assertIn('1.30 mm',texts);self.assertIn('0.100 in',texts)
            constraints=Gui.getMainWindow().findChild(QtWidgets.QListWidget,'listWidgetConstraints')
            self.assertIsNotNone(constraints)
            errors=[];seen=[]
            def edit():
                dialog=QtWidgets.QApplication.activeModalWidget()
                if not dialog:return
                timer.stop()
                try:
                    field=dialog.findChild(QtWidgets.QWidget,'labelEdit');text=field.findChild(QtWidgets.QLineEdit)
                    seen.append(text.text());self.assertEqual(text.text(),'0.100 in')
                    text.setFocus();text.selectAll();QtTest.QTest.keyClicks(text,'0.123456 in')
                    if os.environ.get('PLUS_TEST_DIR'):dialog.grab().save(str(Path(os.environ['PLUS_TEST_DIR'])/'native-unit-edit.png'))
                    buttons=dialog.findChild(QtWidgets.QDialogButtonBox,'buttonBox')
                    buttons.button(QtWidgets.QDialogButtonBox.Ok).setFocus()
                    buttons.button(QtWidgets.QDialogButtonBox.Ok).click()
                except BaseException as error:errors.append(repr(error));dialog.reject()
            timer=QtCore.QTimer();timer.timeout.connect(edit);timer.start(25)
            watchdog=QtCore.QTimer();watchdog.setSingleShot(True)
            watchdog.timeout.connect(lambda: QtWidgets.QApplication.activeModalWidget().reject() if QtWidgets.QApplication.activeModalWidget() else None)
            watchdog.start(5000)
            constraints.itemActivated.emit(constraints.item(1));timer.stop();watchdog.stop()
            self.assertFalse(errors,errors);self.assertEqual(len(seen),1)
            self.assertEqual(s.Constraints[1].PresentationUnit,'in')
            self.assertAlmostEqual(s.Constraints[1].Value,.123456*25.4,places=10)
            QtTest.QTest.qWait(100)
            if os.environ.get('PLUS_TEST_DIR'):
                from TestComponentFading import capture
                capture(Gui.activeDocument().activeView(),Path(os.environ['PLUS_TEST_DIR'])/'native-unit-leaders.png')
        finally:
            if Gui.activeDocument() and Gui.activeDocument().getInEdit():Gui.activeDocument().resetEdit()
            App.closeDocument(doc.Name)

    def test_shared_native_editors_keep_precision_and_units(self):
        import FreeCADGui as Gui
        from PySide6 import QtWidgets,QtTest
        for kind in ('Gui::QuantitySpinBox','Gui::InputField'):
            window=QtWidgets.QWidget();layout=QtWidgets.QVBoxLayout(window)
            field=Gui.UiLoader().createWidget(kind);field.setProperty('unit','mm')
            field.setProperty('rawValue',1.29999)
            layout.addWidget(field);other=QtWidgets.QLineEdit();layout.addWidget(other)
            window.show();QtTest.QTest.qWait(20)
            edit=field if isinstance(field,QtWidgets.QLineEdit) else field.findChild(QtWidgets.QLineEdit)
            self.assertIn('1.29999',edit.text(),kind)
            field.setFocus();edit.selectAll();QtTest.QTest.keyClicks(edit,'0.100 in')
            other.setFocus();QtTest.QTest.qWait(20)
            self.assertAlmostEqual(field.property('rawValue'),2.54,places=10,msg=kind)
            self.assertEqual(field.property('presentationUnit'),'in',kind)
            field.hide();field.show();self.assertIn('0.100 in',edit.text(),kind)
            field.setFocus();edit.selectAll();QtTest.QTest.keyClicks(edit,'0.123456 in')
            other.setFocus();QtTest.QTest.qWait(20)
            self.assertAlmostEqual(field.property('rawValue'),.123456*25.4,places=10,msg=kind)
            self.assertIn('0.123456 in',edit.text(),kind)
            if kind == 'Gui::InputField':
                field.setProperty('rawText','0.23456789 in')
                self.assertAlmostEqual(field.property('rawValue'),.23456789*25.4,places=12)
                self.assertTrue(edit.text().endswith(' in'))
                self.assertAlmostEqual(App.Units.Quantity(field.property('rawText')).Value,.23456789*25.4,places=12)
                self.assertEqual(field.property('presentationUnit'),'in')
            window.close()

    def test_constraint_metadata_clone_undo_and_reopen(self):
        doc=App.newDocument('NativeUnits');doc.UndoMode=1
        try:
            s=doc.addObject('Sketcher::SketchObject','Sketch')
            s.addGeometry(Part.LineSegment(App.Vector(),App.Vector(2.54,0,0)))
            c=Sketcher.Constraint('Distance',0,2.54);c.PresentationUnit='in'
            doc.openTransaction('Datum');s.addConstraint(c);doc.commitTransaction()
            self.assertEqual(s.Constraints[0].PresentationUnit,'in')
            clone=Sketcher.Constraint();clone.restoreContent(s.Constraints[0].dumpContent())
            self.assertEqual(clone.PresentationUnit,'in')
            with self.assertRaises(ValueError):clone.PresentationUnit='deg'
            doc.undo();self.assertEqual(s.ConstraintCount,0);doc.redo()
            self.assertEqual(s.Constraints[0].PresentationUnit,'in')
            if os.environ.get('PLUS_TEST_DIR'):
                path=str(Path(os.environ['PLUS_TEST_DIR'])/'native-units.FCStd')
                doc.recompute();doc.saveAs(path);App.closeDocument(doc.Name);doc=App.openDocument(path)
                self.assertEqual(doc.Sketch.Constraints[0].PresentationUnit,'in')
                self.assertAlmostEqual(doc.Sketch.Constraints[0].Value,2.54,places=12)
        finally:App.closeDocument(doc.Name)


class TestFeatureQuantityUnits(unittest.TestCase):
    def test_extrude_creation_edit_cancel_and_unit_persistence(self):
        import FreeCADGui as Gui
        from PySide6 import QtWidgets,QtTest
        from freecad_plus import document,modeling,extrude_task,editing,extrusion
        doc=document.new_document('FeatureUnits')
        task=None
        try:
            sketch=modeling.new_sketch(doc)
            sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2));doc.recompute()
            Gui.Selection.clearSelection();Gui.Selection.addSelection(sketch)
            task=extrude_task.show();QtTest.QTest.qWait(100)
            field=task.end1['length'];field.setFocus();field.selectAll()
            QtTest.QTest.keyClicks(field,'0.100 in');task.profiles.setFocus();QtTest.QTest.qWait(50)
            self.assertAlmostEqual(task.values[field],2.54,places=10)
            self.assertTrue(task.accept());feature=task.result;task=None
            self.assertEqual(feature.QuantityPresentationUnits[extrusion.PREFIX+'length'],'in')
            self.assertAlmostEqual(feature.Shape.BoundBox.ZLength,2.54,places=10)
            count=doc.UndoCount
            task=editing.edit_feature(doc,feature);field=task.end1['length']
            self.assertEqual(field.text(),'0.100 in')
            field.setValue(7);task.reject();task=None
            self.assertEqual(doc.UndoCount,count)
            task=editing.edit_feature(doc,feature)
            self.assertEqual(task.end1['length'].text(),'0.100 in');task.reject();task=None
            if os.environ.get('PLUS_TEST_DIR'):
                path=str(Path(os.environ['PLUS_TEST_DIR'])/'feature-units.FCStd')
                name=feature.Name;doc.saveAs(path);App.closeDocument(doc.Name);doc=App.openDocument(path)
                feature=doc.getObject(name)
                self.assertEqual(feature.QuantityPresentationUnits[extrusion.PREFIX+'length'],'in')
        finally:
            if task:task.reject()
            Gui.Selection.clearSelection();App.closeDocument(doc.Name)


class TestChainDisplay(unittest.TestCase):
    setUp = pattern_tests.TestPatternTask.setUp
    tearDown = pattern_tests.TestPatternTask.tearDown
    enter = pattern_tests.TestPatternTask.enter
    pick = pattern_tests.TestPatternTask.pick

    def test_circular_chain_checkbox_and_saved_hidden_state(self):
        from TestComponentFading import capture
        self.enter();self.pick(self.p.items,'Edge2')
        self.p.mode.setCurrentText('Circular');self.p.layout_mode.setCurrentText('Angular + radial')
        self.pick(self.p.center,'RootPoint');self.pick(self.p.radial.reference,'Edge2')
        self.p.angular.count.setValue(3);self.p.angular.value.setValue(30)
        self.p.radial.count.setValue(3);self.p.radial.value.setValue(5)
        self.assertTrue(self.p.lock.isChecked());self.assertFalse(self.p.hide_spacing.isChecked())
        self.assertTrue(self.p.apply.isEnabled(),self.p.status.text())
        self.p.apply.click();self.assertEqual(self.s.solve(),0)
        self.assertTrue(self.s.PatternSpacingTags)
        view=self.Gui.activeDocument().activeView();view.fitAll()
        output=Path(os.environ['PLUS_TEST_DIR'])
        capture(view,output/'native-circular-chains.png')
        self.p.grab().save(str(output/'native-pattern-panel.png'))
        self.p.hide_spacing.click();self.QtTest.QTest.qWait(100)
        tags=set(self.s.PatternSpacingTags)
        self.assertTrue(all(pattern.visual_layer(f)==2 for f in self.s.GeometryFacadeList if pattern.spacing_tag(f) in tags))
        capture(view,output/'native-circular-hidden.png')
        self.doc.saveAs(str(output/'circular-hidden.FCStd'))
        self.p.done.click();self.QtTest.QTest.qWait(100);self.enter()
        self.assertTrue(self.p.hide_spacing.isChecked())
        self.p.hide_spacing.click();self.assertTrue(all(pattern.visual_layer(f)==0 for f in self.s.GeometryFacadeList if pattern.spacing_tag(f) in tags))
        self.p.done.click()
