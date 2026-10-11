# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native attachment and shared PartDesign reference collector acceptance."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide6 import QtCore, QtTest, QtWidgets
from freecad_plus import document, display, editing, geometry, hierarchy
from TestComponentPanel import TestComponentPanel, settle
from TestComponentModeling import TestComponentModeling, messages, accept_task


class TestComponentReferences(unittest.TestCase):
    setUp=TestComponentPanel.setUp
    tearDown=TestComponentModeling.tearDown
    sub=TestComponentModeling.sub
    select=TestComponentModeling.select

    def control(self,kind,name):
        return next(w for w in Gui.getMainWindow().findChildren(kind,name) if w.isVisible())

    def plane(self):
        body=self.pad.getParentGeoFeatureGroup()
        plane=body.newObject('PartDesign::Plane','Attachment')
        self.doc.recompute();return plane

    def face(self):
        return 'Face'+str(max(enumerate(self.pad.Shape.Faces,1),key=lambda x:x[1].CenterOfMass.z)[0])

    def reference_button(self):
        button=self.control(QtWidgets.QPushButton,'buttonRef1')
        if not button.isChecked():QtTest.QTest.mouseClick(button,QtCore.Qt.LeftButton)
        settle()

    def test_attachment_picked_typed_and_persistence(self):
        Gui.activateWorkbench('PartDesignWorkbench');plane=self.plane();face=self.face()
        display.set_state(self.root,self.first,part_type='Reference');settle()
        editing.edit_feature(self.doc,plane);settle();self.reference_button()
        before=App.getActiveTransaction();undo=self.doc.UndoCount
        self.select(self.root,self.sub(self.first,self.pad,face));settle()
        self.assertEqual(list(plane.AttachmentSupport),[])
        self.assertTrue(any('Excluded' in w.text() or 'Reference' in w.text()
                            for w in Gui.getMainWindow().findChildren(QtWidgets.QLabel)))
        self.assertEqual(App.getActiveTransaction(),before);self.assertEqual(self.doc.UndoCount,undo)
        self.select(self.root,self.sub(self.second,self.pad,face));settle()
        self.assertEqual(plane.AttachmentSupport[0][0],self.pad)
        support=list(plane.AttachmentSupport);placement=plane.Placement
        # Typed occurrence text must be checked before changing Support or RefName.
        line=self.control(QtWidgets.QLineEdit,'lineRef1');refname=line.property('RefName')
        text=self.root.Name+':'+self.sub(self.first,self.pad,face)
        line.setText(text);line.textEdited.emit(text);settle()
        self.assertEqual(list(plane.AttachmentSupport),support);self.assertEqual(line.property('RefName'),refname)
        self.assertTrue(plane.Placement.isSame(placement,1e-8))
        text=self.pad.Name+':'+face;line.setText(text);line.textEdited.emit(text);settle()
        accept_task();self.assertFalse(Gui.Control.activeDialog())
        self.assertFalse(App.getActiveTransaction())
        Gui.getDocument(self.doc.Name).resetEdit();settle()
        self.assertNotEqual(plane.MapMode,'Deactivated');self.assertNotIn('Invalid',plane.State)
        self.doc.undo();self.doc.recompute();settle();self.assertEqual(list(plane.AttachmentSupport),[])
        self.doc.redo();self.doc.recompute();settle();self.assertEqual(plane.AttachmentSupport[0][0],self.pad)
        document.save_document(self.doc,self.output/'Attachment.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':{o.Name:o.ID for o in self.doc.Objects},
            'target':plane.Name,'source':self.pad.Name,'face':face}))

    def test_attachment_initial_mixed_batch_is_atomic_and_cancel(self):
        Gui.activateWorkbench('PartDesignWorkbench');face=self.face()
        # This native attachment entry retains the preselection; the older
        # PartDesign datum editor clears it before constructing TaskAttacher.
        plane=self.doc.addObject('Part::DatumPlane','BatchAttachment')
        self.pad.getParentGeoFeatureGroup().addObject(plane);self.doc.recompute()
        display.set_state(self.root,self.first,part_type='Excluded');settle()
        self.select(self.root,self.sub(self.second,self.pad,face))
        Gui.Selection.addSelection(self.doc.Name,self.root.Name,self.sub(self.first,self.pad,face))
        original=geometry.require_modeling_inputs;calls=[]
        def observe(consumer,inputs=None):calls.append(inputs);return original(consumer,inputs)
        self.doc.openTransaction('Edit attachment')
        with patch.object(geometry,'require_modeling_inputs',side_effect=observe):
            plane.ViewObject.doubleClicked();settle()
        self.assertTrue(any(refs and len(refs)==2 for refs in calls),calls)
        self.assertEqual(list(plane.AttachmentSupport),[])
        self.reference_button();self.select(self.root,self.sub(self.second,self.pad,face));settle()
        self.assertTrue(plane.AttachmentSupport)
        buttons=Gui.getMainWindow().findChildren(QtWidgets.QDialogButtonBox)
        cancel=next(box.button(QtWidgets.QDialogButtonBox.Cancel) for box in buttons
                    if box.isVisible() and box.button(QtWidgets.QDialogButtonBox.Cancel))
        QtTest.QTest.mouseClick(cancel,QtCore.Qt.LeftButton);settle()
        self.assertEqual(list(plane.AttachmentSupport),[])

    def test_axis_picker_original_occurrence_and_reopen(self):
        Gui.activateWorkbench('PartDesignWorkbench')
        display.set_state(self.root,self.first,part_type='Reference');settle()
        body=self.pad.getParentGeoFeatureGroup()
        axis=next(o for o in body.Origin.OriginFeatures if o.Name.startswith('Z_Axis'))
        def path(first):return hierarchy.subname((first,self.nested))+body.Name+'.'+body.Origin.Name+'.'+axis.Name+'.'
        editing.edit_feature(self.doc,self.pad);settle()
        combo=self.control(QtWidgets.QComboBox,'directionCB');combo.setCurrentIndex(1);combo.activated.emit(1);settle()
        before=self.pad.ReferenceAxis;transaction=App.getActiveTransaction();ids={o.Name:o.ID for o in self.doc.Objects}
        with messages() as errors:self.select(self.root,path(self.first));settle()
        self.assertTrue(any('Excluded' in error or 'Reference' in error for error in errors),errors)
        self.assertEqual(self.pad.ReferenceAxis,before);self.assertEqual(App.getActiveTransaction(),transaction)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects},ids)
        with messages() as errors:self.select(self.root,path(self.second));settle()
        self.assertFalse(errors,errors);self.assertEqual(self.pad.ReferenceAxis[0],axis)
        accept_task();self.assertTrue(self.pad.Shape.isValid())
        document.save_document(self.doc,self.output/'Axis.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':{o.Name:o.ID for o in self.doc.Objects},
            'target':self.pad.Name,'axis':axis.Name,'volume':self.pad.Shape.Volume}))

    def test_legacy_attachment_bypasses_component_guard(self):
        Gui.activateWorkbench('PartDesignWorkbench')
        doc=App.newDocument('LegacyAttachment');body=doc.addObject('PartDesign::Body','Body')
        plane=body.newObject('PartDesign::Plane','Plane');doc.recompute()
        Gui.activeDocument().activeView().setActiveObject('pdbody',body)
        axis=next(o for o in body.Origin.OriginFeatures if o.Name.startswith('XY_Plane'))
        Gui.Selection.clearSelection();Gui.activeDocument().setEdit(plane.Name);settle()
        self.reference_button()
        with patch.object(geometry,'require_modeling_inputs',side_effect=AssertionError('Legacy reached Plus guard')):
            self.select(axis);settle()
        support=plane.AttachmentSupport
        self.assertEqual(support[0][0].getSubObject(support[0][1][0],1),axis,
                         [(o.Name,list(subs)) for o,subs in support]);accept_task()
        self.assertNotIn('Invalid',plane.State)


def verify_fresh_process(output):
    for folder,filename in (('test_attachment_picked_typed_and_persistence','Attachment.cadprt'),
                            ('test_axis_picker_original_occurrence_and_reopen','Axis.cadprt')):
        path=Path(output)/folder;expected=json.loads((path/'expected.json').read_text())
        doc=document.open_document(path/filename)
        try:
            assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
            target=doc.getObject(expected['target'])
            if 'face' in expected:
                source=doc.getObject(expected['source'])
                assert target.AttachmentSupport[0][0]==source and list(target.AttachmentSupport[0][1])==[expected['face']]
                source.Length=7;doc.recompute()
                assert 'Invalid' not in target.State and abs(target.Placement.Base.z-7)<1e-8
            else:
                assert target.ReferenceAxis[0]==doc.getObject(expected['axis'])
                assert abs(target.Shape.Volume-expected['volume'])<1e-8
                target.Length=7;doc.recompute();assert target.Shape.isValid()
                assert abs(target.Shape.Volume-28*3.141592653589793)<1e-8
        finally:App.closeDocument(doc.Name)
