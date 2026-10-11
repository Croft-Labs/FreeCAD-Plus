# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Python attachment and Extrude reference-input acceptance."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtTest, QtWidgets
from AttachmentEditor import Commands
from freecad_plus import document, display, editing, geometry, hierarchy
from TestComponentPanel import TestComponentPanel, settle
from TestComponentModeling import TestComponentModeling, accept_task
from TestComponentReferences import TestComponentReferences


class TestComponentInputEditors(unittest.TestCase):
    setUp=TestComponentPanel.setUp
    sub=TestComponentModeling.sub
    select=TestComponentModeling.select
    control=TestComponentReferences.control
    plane=TestComponentReferences.plane
    face=TestComponentReferences.face

    def tearDown(self):
        if Gui.Control.activeDialog() and getattr(Commands,'taskd',None):
            task=Commands.taskd
            try:
                if task.form.isVisible():task.reject()
            except RuntimeError:
                pass  # A completed Python task's Qt form may already be deleted.
        TestComponentModeling.tearDown(self)

    def task_button(self,role):
        boxes=Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)
        button=next(box.button(role) for box in boxes if box.isVisible() and box.button(role))
        QtTest.QTest.mouseClick(button,QtCore.Qt.LeftButton);settle()

    def forbidden(self):
        display.set_state(self.root,self.first,part_type='Reference');settle()

    def limit(self,owner=None,name='Limit'):
        box=(owner or self.child).newObject('Part::Box',name)
        box.Length=10;box.Width=10;box.Height=1
        box.Placement.Base=App.Vector(-5,-5,8);self.doc.recompute();return box

    def limit_path(self,first,box,face=''):
        return hierarchy.subname((first,self.nested))+box.Name+'.'+face

    def pick_button(self,name):
        button=self.control(QtWidgets.QToolButton,name)
        if not button.isChecked():button.setChecked(True)
        settle()

    def test_python_attachment_initial_batch_before_transaction(self):
        plane=self.plane();face=self.face();self.forbidden()
        self.select(self.root,self.sub(self.second,self.pad,face))
        Gui.Selection.addSelection(self.doc.Name,self.root.Name,self.sub(self.first,self.pad,face))
        ids={o.Name:o.ID for o in self.doc.Objects};undo=self.doc.UndoCount
        with self.assertRaisesRegex(ValueError,'Reference|Excluded'):
            Commands.editAttachment(plane,take_selection=True)
        self.assertFalse(Gui.Control.activeDialog());self.assertFalse(self.doc.HasPendingTransaction)
        self.assertEqual(self.doc.UndoCount,undo);self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
        self.assertEqual(list(plane.AttachmentSupport),[])

    def test_python_attachment_preview_apply_cancel_and_reopen(self):
        plane=self.plane();face=self.face();self.forbidden();Gui.Selection.clearSelection()
        def history():return {'undo':self.doc.UndoNames,'pending':self.doc.HasPendingTransaction,
                             'references':[(o.Name,list(subs)) for o,subs in plane.AttachmentSupport]}
        trace={'before':history()}
        Commands.editAttachment(plane);settle();task=Commands.taskd
        placement=plane.Placement;undo=self.doc.UndoCount
        self.select(self.root,self.sub(self.first,self.pad,face));settle()
        self.assertFalse(task.attacher.References);self.assertTrue(plane.Placement.isSame(placement,1e-8))
        self.select(self.root,self.sub(self.second,self.pad,face));settle()
        self.assertEqual(task.attacher.References[0][0],self.pad)
        # This editor retains Deactivated until the user chooses an attachment mode.
        modes=task.form.listOfModes
        row=next(i for i in range(modes.count()) if modes.item(i).data(task.KEYmode)=='FlatFace')
        modes.setCurrentRow(row);settle()
        self.assertEqual(task.attacher.Mode,'FlatFace');self.assertAlmostEqual(plane.Placement.Base.z,5)
        references=list(task.attacher.References);placement=plane.Placement
        line=task.refLines[0];text=self.root.Name+':'+self.sub(self.first,self.pad,face)
        line.setText(text);line.textEdited.emit(text);settle()
        self.assertEqual(list(task.attacher.References),references)
        self.assertTrue(plane.Placement.isSame(placement,1e-8))
        self.task_button(QtWidgets.QDialogButtonBox.Apply);self.task_button(QtWidgets.QDialogButtonBox.Ok)
        self.assertTrue(Gui.Control.activeDialog());self.assertEqual(list(plane.AttachmentSupport),[])
        self.assertTrue(self.doc.HasPendingTransaction);self.assertEqual(self.doc.UndoCount,undo)
        text=self.pad.Name+':'+face;line.setText(text);line.textEdited.emit(text);settle()
        self.task_button(QtWidgets.QDialogButtonBox.Apply)
        trace['applied']=history()
        self.assertEqual(plane.AttachmentSupport[0][0],self.pad)
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.assertFalse(Gui.Control.activeDialog());self.assertEqual(plane.AttachmentSupport[0][0],self.pad)
        trace['canceled']=history()
        self.doc.undo();self.doc.recompute();settle();trace['undone']=history()
        self.assertFalse(plane.AttachmentSupport,trace)
        self.doc.redo();self.doc.recompute();settle();self.assertEqual(plane.AttachmentSupport[0][0],self.pad)
        document.save_document(self.doc,self.output/'PythonAttachment.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':{o.Name:o.ID for o in self.doc.Objects},
            'target':plane.Name,'source':self.pad.Name,'face':face}))

    def test_extrude_face_picked_typed_and_reopen(self):
        Gui.activateWorkbench('PartDesignWorkbench');box=self.limit();foreign=self.limit(self.unused,'Foreign')
        self.forbidden();editing.edit_feature(self.doc,self.pad);settle()
        self.control(QtWidgets.QComboBox,'changeMode').setCurrentIndex(3);settle()
        self.pick_button('buttonFace');before=self.pad.UpToFace;undo=self.doc.UndoCount
        self.select(self.root,self.limit_path(self.first,box,'Face6'));settle()
        self.assertEqual(self.pad.UpToFace,before);self.assertEqual(self.doc.UndoCount,undo)
        self.assertTrue(self.control(QtWidgets.QToolButton,'buttonFace').isChecked())
        self.select(self.root,self.limit_path(self.second,box,'Face6'));settle()
        self.assertEqual(self.pad.UpToFace[0],box);self.assertTrue(self.pad.Shape.isValid())
        line=self.control(QtWidgets.QLineEdit,'lineFaceName')
        meta=(line.property('FeatureName'),line.property('FaceName'));reference=self.pad.UpToFace;volume=self.pad.Shape.Volume
        text=foreign.Label+':Face6';line.setText(text);line.textEdited.emit(text);settle()
        self.assertEqual(self.pad.UpToFace,reference)
        self.assertEqual((line.property('FeatureName'),line.property('FaceName')),meta)
        self.assertAlmostEqual(self.pad.Shape.Volume,volume)
        text=box.Label+':Face6';line.setText(text);line.textEdited.emit(text);settle();accept_task()
        self.assertFalse(Gui.Control.activeDialog());self.assertTrue(self.pad.Shape.isValid())
        document.save_document(self.doc,self.output/'UpToFace.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':{o.Name:o.ID for o in self.doc.Objects},
            'target':self.pad.Name,'source':box.Name,'volume':self.pad.Shape.Volume}))

    def test_extrude_shape_and_face_lists_both_sides_cancel(self):
        Gui.activateWorkbench('PartDesignWorkbench');box=self.limit();self.forbidden()
        editing.edit_feature(self.doc,self.pad);settle()
        self.control(QtWidgets.QComboBox,'sidesMode').setCurrentIndex(1);settle()
        for suffix in ('','2'):
            self.control(QtWidgets.QComboBox,'changeMode'+suffix).setCurrentIndex(4);settle()
            self.pick_button('buttonShape'+suffix)
            before=getattr(self.pad,'UpToShape'+suffix)
            self.select(self.root,self.limit_path(self.first,box));settle()
            self.assertEqual(getattr(self.pad,'UpToShape'+suffix),before)
            self.select(self.root,self.limit_path(self.second,box));settle()
            self.assertEqual(getattr(self.pad,'UpToShape'+suffix)[0][0],box)
            self.control(QtWidgets.QCheckBox,'checkBoxAllFaces'+suffix).setChecked(False);settle()
            self.pick_button('buttonShapeFace'+suffix);before=getattr(self.pad,'UpToShape'+suffix)
            self.select(self.root,self.limit_path(self.first,box,'Face6'));settle()
            self.assertEqual(getattr(self.pad,'UpToShape'+suffix),before)
            self.select(self.root,self.limit_path(self.second,box,'Face6'));settle()
            self.assertIn('Face6',getattr(self.pad,'UpToShape'+suffix)[0][1])
        self.task_button(QtWidgets.QDialogButtonBox.Cancel)
        self.assertFalse(self.pad.UpToShape);self.assertFalse(self.pad.UpToShape2)
        self.assertTrue(self.pad.Shape.isValid())

    def test_legacy_python_attachment_and_extrude_bypass(self):
        Gui.activateWorkbench('PartDesignWorkbench');doc=App.newDocument('LegacyInputs')
        box=doc.addObject('Part::Box','Limit');box.Length=10;box.Width=10;box.Height=1
        box.Placement.Base=App.Vector(-5,-5,8)
        plane=doc.addObject('Part::DatumPlane','Plane');doc.recompute();Gui.Selection.clearSelection()
        with patch.object(geometry,'require_modeling_inputs',side_effect=AssertionError('Legacy reached Plus guard')):
            Commands.editAttachment(plane);settle();self.select(box,'Face6');settle()
            self.task_button(QtWidgets.QDialogButtonBox.Ok)
            self.assertEqual(plane.AttachmentSupport[0][0],box)
            body=doc.addObject('PartDesign::Body','Body');sketch=body.newObject('Sketcher::SketchObject','Sketch')
            sketch.addGeometry(Part.Circle(App.Vector(),App.Vector(0,0,1),2),False);doc.recompute()
            pad=body.newObject('PartDesign::Pad','Pad');pad.Profile=sketch;pad.Length=5;doc.recompute()
            Gui.activeDocument().activeView().setActiveObject('pdbody',body)
            Gui.activeDocument().setEdit(pad.Name);settle()
            self.control(QtWidgets.QComboBox,'changeMode').setCurrentIndex(3);settle()
            self.pick_button('buttonFace');self.select(box,'Face6');settle();accept_task()
            self.assertEqual(pad.UpToFace[0],box);self.assertTrue(pad.Shape.isValid())


def verify_fresh_process(output):
    for folder,filename in (('test_python_attachment_preview_apply_cancel_and_reopen','PythonAttachment.cadprt'),
                            ('test_extrude_face_picked_typed_and_reopen','UpToFace.cadprt')):
        path=Path(output)/folder;expected=json.loads((path/'expected.json').read_text())
        doc=document.open_document(path/filename)
        try:
            assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
            target=doc.getObject(expected['target']);source=doc.getObject(expected['source'])
            if 'face' in expected:
                assert target.AttachmentSupport[0][0]==source
                source.Length=7;doc.recompute()
                assert 'Invalid' not in target.State and abs(target.Placement.Base.z-7)<1e-8
            else:
                assert target.UpToFace[0]==source and list(target.UpToFace[1])==['Face6']
                assert abs(target.Shape.Volume-expected['volume'])<1e-8
                source.Placement.Base=App.Vector(-5,-5,10);doc.recompute()
                assert target.Shape.isValid() and abs(target.Shape.Volume-44*3.141592653589793)<1e-8
        finally:App.closeDocument(doc.Name)
