# SPDX-License-Identifier: LGPL-2.1-or-later
"""Mesh file intake preserves component ownership, History and native Undo."""
import os
from pathlib import Path
import time
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Mesh
from PySide6 import QtCore, QtTest, QtWidgets
from freecad import module_io
from freecad_plus import document, document_import, editing, external, hierarchy, panel


class TestMeshImport(unittest.TestCase):
    def setUp(self):
        if 'PLUS_TEST_DIR' not in os.environ:
            self.skipTest('Set PLUS_TEST_DIR to an isolated validation directory')
        self.output = Path(os.environ['PLUS_TEST_DIR']) / self._testMethodName
        self.output.mkdir(exist_ok=True)
        self.before = set(App.listDocuments())
        self.doc = document.new_document('MeshFixture')
        self.root = document.validate(self.doc)
        self.owner = self.root.Definitions[0]
        self.owner.Label = 'Mesh component'
        self.path = (self.root.Group[0],)
        editing.edit(self.path)
        self.file = self.output / 'sample.stl'
        Mesh.createBox(3, 4, 5).write(str(self.file))

    def tearDown(self):
        if App.getActiveTransaction():
            App.closeActiveTransaction(True)
        Gui.Selection.clearSelection()
        for name in set(App.listDocuments()) - self.before:
            App.closeDocument(name)
        QtTest.QTest.qWait(100)

    def insert(self):
        module_io.OpenInsertObject('Mesh', str(self.file), 'insert', self.doc.Name)
        return next(o for o in self.owner.Group if o.isDerivedFrom('Mesh::Feature'))

    def _native_import(self, command):
        old = QtWidgets.QApplication.testAttribute(QtCore.Qt.AA_DontUseNativeDialogs)
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_DontUseNativeDialogs, True)
        timer = QtCore.QTimer();deadline = time.monotonic() + 10;seen = []
        def choose():
            modal = QtWidgets.QApplication.activeModalWidget()
            if isinstance(modal, QtWidgets.QFileDialog):
                seen.append(modal.windowTitle())
                modal.selectNameFilter('STL Mesh (*.stl *.STL *.ast *.AST)')
                modal.findChild(QtWidgets.QLineEdit, 'fileNameEdit').setText(str(self.file))
                modal.accept()
            elif time.monotonic() > deadline and isinstance(modal, QtWidgets.QDialog):
                modal.reject()
        ids = {o.Name:o.ID for o in self.doc.Objects};undo = self.doc.UndoCount
        timer.timeout.connect(choose);timer.start(30)
        try: Gui.runCommand(command)
        finally:
            timer.stop()
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_DontUseNativeDialogs, old)
        self.assertTrue(seen)
        mesh = next(o for o in self.owner.Group if o.isDerivedFrom('Mesh::Feature'))
        self.assertIn(mesh, document.history(self.doc, self.owner))
        widget = panel.show_panel();widget.activate_assembly(self.owner);widget.refresh()
        self.assertTrue(all(t.topLevelItemCount() for t in widget.trees))
        self.assertEqual(editing.context_path(self.doc), (self.owner, self.path))
        self.assertEqual(self.doc.UndoCount, undo + 1)
        self.assertAlmostEqual(mesh.Mesh.Volume, 60)
        self.doc.undo();document.validate(self.doc)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, ids)
        self.doc.redo();document.validate(self.doc)
        self.assertTrue(any(o.isDerivedFrom('Mesh::Feature') for o in self.owner.Group))

    def test_native_import_dialog_history_and_atomic_undo(self):
        self._native_import('Std_Import')

    def test_mesh_workbench_import_dialog_history_and_atomic_undo(self):
        Gui.activateWorkbench('MeshWorkbench')
        self._native_import('Mesh_Import')

    def test_child_target_not_parent_or_native_body(self):
        parent = self.owner
        self.owner = hierarchy.create_definition(self.doc, 'Child')
        link = hierarchy.add_instance(parent, self.owner)
        body = parent.newObject('PartDesign::Body', 'OtherBody')
        self.path = (*self.path, link);editing.edit(self.path)
        Gui.activeDocument().activeView().setActiveObject('pdbody', body)
        mesh = self.insert()
        self.assertEqual(mesh.getParentGeoFeatureGroup(), self.owner)
        self.assertNotIn(mesh, document.history(self.doc, parent))
        self.assertIn(mesh, document.history(self.doc, self.owner))

    def test_external_unused_target_uses_defining_document(self):
        document.save_document(self.doc, self.output/'host.cadprt')
        source = document.new_document('Source')
        self.owner = document.validate(source).Definitions[0];self.owner.Label = 'External mesh'
        document.save_document(source, self.output/'source.cadprt')
        external.import_file(self.doc, source)
        App.setActiveDocument(self.doc.Name);editing.edit_unused(self.doc, self.owner)
        ids = {o.Name:o.ID for o in self.doc.Objects};undo = source.UndoCount
        mesh = self.insert()
        self.assertEqual(mesh.Document, source)
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, ids)
        self.assertEqual(source.UndoCount, undo + 1)
        self.assertEqual(editing.context_path(self.doc), (self.owner, ()))
        source.undo();document.validate(self.doc)
        self.assertFalse(any(o.isDerivedFrom('Mesh::Feature') for o in source.Objects))

    def test_missing_edit_does_not_create_orphan(self):
        editing.edit_file(self.doc)
        ids = {o.Name:o.ID for o in self.doc.Objects};undo = self.doc.UndoCount
        with self.assertRaisesRegex(ValueError, 'Edit a component'):
            self.insert()
        self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, ids)
        self.assertEqual(self.doc.UndoCount, undo)

    def test_failed_or_cancelled_reader_rolls_back(self):
        ids = {o.Name:o.ID for o in self.doc.Objects};undo = self.doc.UndoCount
        for error in (RuntimeError('bad mesh'), App.Base.AbortIOException('cancel')):
            def fail(filename, name, **kwargs):
                App.getDocument(name).addObject('Mesh::Feature', 'PartialImport')
                raise error
            with patch.object(Mesh, 'insert', side_effect=fail):
                if isinstance(error, App.Base.AbortIOException):
                    module_io.OpenInsertObject('Mesh', str(self.file), 'insert', self.doc.Name)
                else:
                    with self.assertRaisesRegex(RuntimeError, 'bad mesh'):self.insert()
            document.validate(self.doc)
            self.assertEqual({o.Name:o.ID for o in self.doc.Objects}, ids)
            self.assertEqual(self.doc.UndoCount, undo)

    def test_pending_edit_is_preserved(self):
        self.doc.openTransaction('Existing operation');self.owner.Label = 'Pending edit'
        with self.assertRaisesRegex(ValueError, 'Finish the current operation'):
            self.insert()
        self.assertTrue(self.doc.HasPendingTransaction)
        self.assertEqual(self.owner.Label, 'Pending edit')
        self.assertFalse(any(o.isDerivedFrom('Mesh::Feature') for o in self.doc.Objects))
        self.doc.abortTransaction()

    def test_save_reopen_preserves_mesh_and_identity(self):
        mesh = self.insert();uid = str(self.doc.Uid);mesh_id = mesh.ID
        mesh.Placement.Base = App.Vector(2, 3, 4)
        filename = self.output/'mesh.cadprt';document.save_document(self.doc, filename)
        name = mesh.Name;owner_name = self.owner.Name
        App.closeDocument(self.doc.Name)
        self.doc = document.open_document(filename)
        self.assertEqual(str(self.doc.Uid), uid)
        mesh = self.doc.getObject(name)
        self.assertEqual(mesh.ID, mesh_id)
        self.assertAlmostEqual(mesh.Mesh.Volume, 60)
        self.assertTrue(mesh.Placement.Base.isEqual(App.Vector(2,3,4), 1e-9))
        self.assertIn(mesh, document.history(self.doc, self.doc.getObject(owner_name)))

    def test_classic_document_retains_native_mesh_import(self):
        classic = App.newDocument('ClassicMesh')
        module_io.OpenInsertObject('Mesh', str(self.file), 'insert', classic.Name)
        self.assertEqual(len(classic.Objects), 1)
        self.assertTrue(classic.Objects[0].isDerivedFrom('Mesh::Feature'))
        self.assertIsNone(classic.Objects[0].getParentGeoFeatureGroup())
