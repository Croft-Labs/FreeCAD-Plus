# SPDX-License-Identifier: LGPL-2.1-or-later
"""Actual native profile and Sketcher external-input component boundaries."""
from contextlib import contextmanager
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, display, editing, geometry, hierarchy
from TestComponentPanel import TestComponentPanel, settle
from TestUnusedModels import TestUnusedModels, visibility


@contextmanager
def messages():
    seen=[]
    timer=QtCore.QTimer()
    def close_message():
        modal=QtWidgets.QApplication.activeModalWidget()
        if isinstance(modal,QtWidgets.QMessageBox):
            seen.append(modal.text());modal.accept()
    timer.timeout.connect(close_message);timer.start(25)
    try:yield seen
    finally:timer.stop();timer.deleteLater()


def accept_task():
    buttons=[box.button(QtWidgets.QDialogButtonBox.Ok)
             for box in Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)]
    button=next(b for b in buttons if b and b.isVisible())
    QtTest.QTest.mouseClick(button,QtCore.Qt.LeftButton);settle()


class TestComponentModeling(unittest.TestCase):
    setUp=TestComponentPanel.setUp
    external_fixture=TestUnusedModels.external_fixture

    def tearDown(self):
        for name in App.listDocuments():
            gui=Gui.getDocument(name)
            if gui.getInEdit():gui.resetEdit()
        if App.getActiveTransaction():App.closeActiveTransaction(True)
        TestComponentPanel.tearDown(self)

    def sub(self,first,obj,element=''):
        return hierarchy.subname((first,self.nested))+obj.getParentGeoFeatureGroup().Name+'.'+obj.Name+'.'+element

    def select(self,obj,sub=''):
        Gui.Selection.clearSelection();Gui.Selection.addSelection(obj.Document.Name,obj.Name,sub)

    def new_profile(self):
        sketch=editing.new_sketch(self.doc)
        sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),1),False)
        self.doc.recompute();settle();return sketch

    def test_profile_shared_occurrence_rejection_and_native_pad(self):
        Gui.activateWorkbench('PartDesignWorkbench')
        sketch=self.new_profile();body=sketch.getParentGeoFeatureGroup()
        for kind in ('Reference','Excluded'):
            display.set_state(self.root,self.first,part_type=kind);settle()
            self.select(self.root,self.sub(self.first,sketch))
            ids={o.Name:o.ID for o in self.doc.Objects};undo=self.doc.UndoCount
            with messages() as errors:Gui.runCommand('PartDesign_Pad');settle()
            self.assertTrue(any('Reference' in error or 'Excluded' in error for error in errors),errors)
            self.assertIsNone(Gui.getDocument(self.doc.Name).getInEdit())
            self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
            self.assertEqual(self.doc.UndoCount,undo)
        self.select(self.root,self.sub(self.second,sketch))
        with messages() as errors:Gui.runCommand('PartDesign_Pad');settle()
        self.assertFalse(errors,errors)
        feature=Gui.getDocument(self.doc.Name).getInEdit().Object
        accept_task();self.assertIsNone(Gui.getDocument(self.doc.Name).getInEdit())
        self.assertTrue(feature.Shape.isValid());self.assertEqual(body.Tip,feature)
        name=feature.Name;volume=feature.Shape.Volume
        self.doc.undo();self.doc.recompute();settle();self.assertIsNone(self.doc.getObject(name))
        self.doc.redo();self.doc.recompute();settle();feature=self.doc.getObject(name)
        self.assertEqual(body.Tip,feature);self.assertAlmostEqual(feature.Shape.Volume,volume)
        document.save_document(self.doc,self.output/'Modeling.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':{o.Name:o.ID for o in self.doc.Objects},
            'visibility':visibility(self.doc),'feature':name,'profile':sketch.Name,'volume':volume}))

    def test_sketch_projection_checks_original_occurrence_before_mutation(self):
        Gui.activateWorkbench('SketcherWorkbench')
        target=self.new_profile()
        # The cylinder seam projects to a point in this sketch plane. Use a
        # circular rim so acceptance proves real downstream projected geometry.
        edge=next('Edge'+str(i) for i,e in enumerate(self.pad.Shape.Edges,1)
                  if isinstance(e.Curve,Part.Circle))
        display.set_state(self.root,self.first,part_type='Reference');settle()
        editing.edit_feature(self.doc,target);settle()
        Gui.runCommand('Sketcher_Projection');settle()
        original=geometry.require_modeling_inputs;errors=[];calls=[]
        def observe(consumer,inputs=None):
            calls.append(inputs)
            try:return original(consumer,inputs)
            except ValueError as error:errors.append(str(error));raise
        before=list(target.ExternalGeometry);transaction=App.getActiveTransaction();undo=self.doc.UndoCount
        with patch.object(geometry,'require_modeling_inputs',side_effect=observe), messages():
            self.select(self.root,self.sub(self.first,self.pad,edge));settle()
        self.assertTrue(any('Reference' in error or 'Excluded' in error for error in errors),(errors,calls))
        self.assertEqual(list(target.ExternalGeometry),before)
        self.assertEqual(App.getActiveTransaction(),transaction);self.assertEqual(self.doc.UndoCount,undo)
        self.assertIsNotNone(Gui.getDocument(self.doc.Name).getInEdit())
        with messages():self.select(self.root,self.sub(self.second,self.pad,edge));settle()
        self.assertEqual(len(target.ExternalGeometry),1)
        self.assertEqual(target.ExternalGeometry[0][0],self.pad)
        Gui.runCommand('Sketcher_LeaveSketch');settle()
        self.assertIsNone(Gui.getDocument(self.doc.Name).getInEdit())
        self.doc.recompute()
        self.assertNotIn('Invalid',target.State)
        self.assertEqual(len(target.Shape.Edges),2)
        document.save_document(self.doc,self.output/'Projection.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':{o.Name:o.ID for o in self.doc.Objects},
            'target':target.Name,'source':self.pad.Name,'references':list(target.ExternalGeometry[0][1])}))

    def test_empty_selection_picker_and_legacy_passthrough(self):
        Gui.activateWorkbench('PartDesignWorkbench')
        sketch=self.new_profile();self.select(self.root,self.sub(self.second,sketch));Gui.Selection.clearSelection()
        original=geometry.require_modeling_inputs;calls=[]
        def observe(consumer,inputs=None):calls.append(inputs);return original(consumer,inputs)
        with patch.object(geometry,'require_modeling_inputs',side_effect=observe),messages() as errors:
            Gui.runCommand('PartDesign_Pad');settle()
        self.assertFalse(errors,errors);self.assertTrue(any(refs for refs in calls),calls)
        accept_task()
        legacy=App.newDocument('LegacyProfile');body=legacy.addObject('PartDesign::Body','Body')
        sketch=body.newObject('Sketcher::SketchObject','Sketch')
        sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),1),False);legacy.recompute()
        Gui.activeDocument().activeView().setActiveObject('pdbody',body)
        self.select(sketch)
        with patch.object(geometry,'require_modeling_inputs',side_effect=AssertionError('Legacy reached Plus guard')),messages() as errors:
            Gui.runCommand('PartDesign_Pad');settle()
        self.assertFalse(errors,errors);accept_task();self.assertTrue(body.Tip.Shape.isValid())

    def test_external_unused_context_and_wrong_consumer(self):
        source,definition=self.external_fixture();editing.edit_unused(self.doc,definition)
        sketch=editing.new_sketch(self.doc);settle()
        geometry.require_modeling_inputs(sketch,[(sketch,'')])
        with self.assertRaisesRegex(ValueError,'edited component'):
            geometry.require_modeling_inputs(self.pad,[(sketch,'')])
        editing.edit_file(self.doc)
        with self.assertRaisesRegex(ValueError,'Edit a component'):
            geometry.require_modeling_inputs(sketch,[(sketch,'')])
        self.assertEqual(sketch.Document,source)


def verify_fresh_process(output, only=None):
    for folder_name,filename in (('test_profile_shared_occurrence_rejection_and_native_pad','Modeling.cadprt'),
                                 ('test_sketch_projection_checks_original_occurrence_before_mutation','Projection.cadprt')):
        if only is not None and filename != only:continue
        folder=Path(output)/folder_name;expected=json.loads((folder/'expected.json').read_text())
        doc=document.open_document(folder/filename)
        try:
            assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
            if 'feature' in expected:
                assert visibility(doc)==expected['visibility']
                feature=doc.getObject(expected['feature']);doc.recompute()
                assert feature.Shape.isValid() and abs(feature.Shape.Volume-expected['volume'])<1e-8
                assert feature.Profile[0]==doc.getObject(expected['profile'])
                assert feature.getParentGeoFeatureGroup().Tip==feature
            else:
                target=doc.getObject(expected['target']);source=doc.getObject(expected['source'])
                actual=[(obj,list(subs)) for obj,subs in target.ExternalGeometry]
                assert actual==[(source,expected['references'])], repr(actual)
                source.Length=6;doc.recompute()
                assert 'Invalid' not in target.State and len(target.ExternalGeometry)==1
                assert len(target.Shape.Edges)==2
                assert source.Shape.isValid() and abs(source.Shape.Volume-24*3.141592653589793)<1e-8
        finally:App.closeDocument(doc.Name)
