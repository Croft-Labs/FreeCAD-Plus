# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native File > Export must preserve component occurrence eligibility."""
import json
from pathlib import Path
import sys
import time
import types
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide6 import QtCore, QtWidgets
from freecad_plus import document, display, editing, geometry, hierarchy
from TestComponentPanel import TestComponentPanel, settle
from TestUnusedModels import TestUnusedModels, visibility


class TestComponentExport(unittest.TestCase):
    setUp = TestComponentPanel.setUp
    tearDown = TestComponentPanel.tearDown
    external_fixture = TestUnusedModels.external_fixture

    def select(self, obj, sub=''):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(obj.Document.Name, obj.Name, sub)

    def sub(self, first):
        return hierarchy.subname((first, self.nested)) + self.pad.getParentGeoFeatureGroup().Name + '.' + self.pad.Name + '.'

    def export(self, name):
        return native_export(self.output / name)

    def test_shared_reference_and_allowed_geometry(self):
        editing.edit_file(self.doc)
        display.set_state(self.root, self.first, part_type='Reference'); settle()
        ids = {o.Name:o.ID for o in self.doc.Objects}; vis = visibility(self.doc)
        undo = self.doc.UndoCount
        self.select(self.root, self.sub(self.first))
        denied = self.export('reference.g1export')
        self.assertIn('Reference', denied['error']); self.assertEqual(denied['calls'], [])
        self.assertFalse((self.output/'reference.g1export.brep').exists())
        self.select(self.root, self.sub(self.second))
        allowed = self.export('normal.g1export')
        self.assertEqual(allowed['error'], ''); self.assertEqual(allowed['calls'], ['options', 'writer'])
        shape = Part.Shape(); shape.read(str(self.output/'normal.g1export.brep'))
        self.assertTrue(shape.isValid()); self.assertAlmostEqual(shape.Volume, self.pad.Shape.Volume)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, ids)
        self.assertEqual(visibility(self.doc), vis); self.assertEqual(self.doc.UndoCount, undo)
        document.save_document(self.doc, self.output/'Export.cadprt')
        (self.output/'expected.json').write_text(json.dumps({'ids':ids,'visibility':vis,
            'blocked':self.sub(self.first),'allowed':self.sub(self.second),'volume':self.pad.Shape.Volume}))

    def test_aggregate_mixed_selection_and_no_catalog_fallback(self):
        display.set_state(self.parent,self.nested,part_type='Excluded'); settle()
        editing.edit_file(self.doc)
        self.select(self.root,self.first.Name+'.')
        denied=self.export('aggregate.g1export')
        self.assertIn('Excluded',denied['error']);self.assertEqual(denied['calls'],[])
        # Editing the excluded descendant must not grant whole-file export access.
        editing.edit((self.first,self.nested));self.select(self.root)
        denied=self.export('whole-file.g1export')
        self.assertIn('Excluded',denied['error']);self.assertEqual(denied['calls'],[])
        # A good member in the same selection cannot grant access to a bad aggregate.
        self.select(self.pad)
        Gui.Selection.addSelection(self.doc.Name,self.root.Name,'')
        denied=self.export('mixed.g1export')
        self.assertTrue(denied['error']);self.assertEqual(denied['calls'],[])
        Gui.Selection.clearSelection()
        with self.assertRaisesRegex(ValueError,'Select a component'):
            geometry.require_export(self.doc,self.doc.Objects)

    def test_active_owned_feature_and_external_unused(self):
        display.set_state(self.root,self.second,part_type='Reference');settle()
        editing.edit((self.second,self.nested))
        self.select(self.pad)
        self.assertEqual(self.export('edited.g1export')['calls'],['options','writer'])
        owned=self.doc.addObject('Part::Feature','OwnedReferenceResult')
        owned.Shape=Part.makeBox(1,2,3);self.child.addObject(owned)
        owned.addProperty('App::PropertyLink','Source');owned.Source=self.pad;self.doc.recompute()
        self.select(owned)
        self.assertEqual(self.export('owned.g1export')['calls'],['options','writer'])
        source, definition=self.external_fixture()
        result=source.addObject('Part::Feature','UnusedResult')
        result.Shape=Part.makeBox(1,2,3);definition.addObject(result);source.recompute()
        editing.edit_unused(self.doc,definition);settle();self.select(result)
        accepted=self.export('external.g1export')
        self.assertEqual(accepted['error'],'');self.assertEqual(accepted['calls'],['options','writer'])
        self.assertFalse(any('PlusChildPartType' in o.PropertiesList for o in self.doc.Objects if o not in (self.second,)))

    def test_payload_mismatch_and_legacy_export(self):
        editing.edit_file(self.doc);self.select(self.root,self.sub(self.second))
        with self.assertRaisesRegex(ValueError,'selection changed'):
            geometry.require_export(self.doc,[self.root])
        legacy=App.newDocument('LegacyExport')
        box=legacy.addObject('Part::Box','Box');legacy.recompute();self.select(box)
        with patch.object(geometry,'require_export',side_effect=AssertionError('Legacy export entered Plus policy')):
            result=self.export('legacy.g1export')
        self.assertEqual(result['error'],'');self.assertEqual(result['calls'],['options','writer'])
        shape=Part.Shape();shape.read(str(self.output/'legacy.g1export.brep'))
        self.assertAlmostEqual(shape.Volume,box.Shape.Volume)


def native_export(destination):
    """Drive the real standard command with a bounded dialog handler and writer probe."""
    destination=Path(destination)
    result={'calls':[],'error':'','file_dialog':False,'timeout':False}
    module=types.ModuleType('PlusExportAcceptance')
    def options(filename):
        result['calls'].append('options');return {}
    def writer(objects,filename,options):
        result['calls'].append('writer');Part.export(objects,filename+'.brep')
    module.exportOptions=options;module.export=writer
    sys.modules[module.__name__]=module
    filter_name='Component export acceptance (*.g1export)'
    App.addExportType(filter_name,module.__name__)
    prefs=App.ParamGet('User parameter:BaseApp/Preferences/General')
    previous=prefs.GetString('FileExportFilter','')
    prefs.SetString('FileExportFilter',filter_name)
    attribute=QtCore.Qt.AA_DontUseNativeDialogs
    native=QtWidgets.QApplication.testAttribute(attribute)
    QtWidgets.QApplication.setAttribute(attribute,True)
    deadline=time.monotonic()+12
    timer=QtCore.QTimer()
    def dialogs():
        modal=QtWidgets.QApplication.activeModalWidget()
        if isinstance(modal,QtWidgets.QMessageBox):
            result['error']+=modal.text();modal.accept()
        elif isinstance(modal,QtWidgets.QFileDialog):
            if time.monotonic()>deadline:
                result['timeout']=True;modal.reject();return
            if not result['file_dialog']:
                result['file_dialog']=True
                modal.selectNameFilter(filter_name)
                modal.setDirectory(str(destination.parent))
                filename=modal.findChild(QtWidgets.QLineEdit,'fileNameEdit')
                assert filename is not None
                filename.setText(destination.name)
                modal.accept()
        elif time.monotonic()>deadline:
            result['timeout']=True
            if isinstance(modal,QtWidgets.QDialog):modal.reject()
    timer.timeout.connect(dialogs);timer.start(25)
    try:
        Gui.runCommand('Std_Export');settle()
    finally:
        timer.stop();timer.deleteLater()
        prefs.SetString('FileExportFilter',previous)
        QtWidgets.QApplication.setAttribute(attribute,native)
        sys.modules.pop(module.__name__,None)
    assert not result['timeout'],result
    assert result['file_dialog'],result
    return result


def verify_fresh_process(output):
    folder=Path(output)/'test_shared_reference_and_allowed_geometry'
    expected=json.loads((folder/'expected.json').read_text())
    doc=document.open_document(folder/'Export.cadprt')
    try:
        root=document.validate(doc);editing.edit_file(doc)
        assert {o.Name:o.ID for o in doc.Objects}==expected['ids']
        assert visibility(doc)==expected['visibility']
        Gui.Selection.clearSelection();Gui.Selection.addSelection(doc.Name,root.Name,expected['blocked'])
        denied=native_export(folder/'reopened-blocked.g1export')
        assert 'Reference' in denied['error'] and not denied['calls'],denied
        Gui.Selection.clearSelection();Gui.Selection.addSelection(doc.Name,root.Name,expected['allowed'])
        accepted=native_export(folder/'reopened-allowed.g1export')
        assert not accepted['error'] and accepted['calls']==['options','writer'],accepted
        shape=Part.Shape();shape.read(str(folder/'reopened-allowed.g1export.brep'))
        assert shape.isValid() and abs(shape.Volume-expected['volume'])<1e-8
    finally:
        Gui.Selection.clearSelection();App.closeDocument(doc.Name)
