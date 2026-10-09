# SPDX-License-Identifier: LGPL-2.1-or-later
"""Deletion owns payloads, preserves shared models and refuses consumers."""
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import ComponentModel as Model
import CadDocument


class TestComponentDefinitionDeletion(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_file_document()
        self.root = Model.metadata(self.doc).RootComponent
        self.part = Model.children(self.root)[0].LinkedObject

    def tearDown(self):
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def unused(self):
        Model.remove_instances(Model.children(self.root))

    def testInitialPartDeletionUndoRedoAndEmptyReopen(self):
        self.unused()
        names = {obj.Name for obj in self.doc.Objects}
        removed = {obj.Name for obj in Model.definition_deletion_plan(self.part)}
        identity = self.part.ObjectId
        part_name = self.part.Name
        Model.delete_definition(self.part)
        self.assertEqual(Model.definitions(self.doc), [self.root])
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names - removed)
        self.doc.undo()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
        self.assertEqual(self.doc.getObject(part_name).ObjectId, identity)
        self.doc.redo()
        Model.validate(self.doc)
        path = Path(os.environ['FREECAD_PLUS_VALIDATION_DIR']) / 'Empty.cadprt'
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        reopened = CadDocument.open(path)
        self.assertEqual(len(Model.definitions(reopened)), 1)
        self.assertEqual(Model.children(Model.metadata(reopened).RootComponent), [])

    def testPlacedAndFileRootRefused(self):
        before = {obj.Name for obj in self.doc.Objects}
        for obj in (self.part, self.root):
            with self.assertRaises(ValueError): Model.delete_definition(obj)
        self.assertEqual({obj.Name for obj in self.doc.Objects}, before)

    def testOwnedGeometryAndOriginRemovedButLinkedDefinitionRetained(self):
        self.unused()
        other = Model.create_definition(self.doc, 'Shared')
        Model.add_component(self.part, other)
        box = self.doc.addObject('Part::Box', 'Box')
        Model.register_object(self.part, box, 'Operation')
        self.doc.recompute()
        owned_names = {obj.Name for obj in Model.definition_deletion_plan(self.part)}
        other_id = other.ObjectId
        Model.delete_definition(self.part)
        self.assertTrue(owned_names.isdisjoint({obj.Name for obj in self.doc.Objects}))
        self.assertEqual(other.ObjectId, other_id)
        self.assertEqual(set(Model.definitions(self.doc)), {self.root, other})
        self.doc.undo()
        self.assertTrue(owned_names.issubset({obj.Name for obj in self.doc.Objects}))
        Model.validate(self.doc)

    def testGeometryConsumerAndExternalOccurrenceRefused(self):
        self.unused()
        box = self.doc.addObject('Part::Box', 'Box')
        Model.register_object(self.part, box, 'Operation')
        consumer = self.doc.addObject('Part::Cut', 'Consumer')
        consumer.Base = box
        with self.assertRaisesRegex(ValueError, 'outside references'):
            Model.delete_definition(self.part)
        self.doc.removeObject(consumer.Name)
        external = Model.new_file_document()
        parent = Model.metadata(external).RootComponent
        folder = Path(os.environ['FREECAD_PLUS_VALIDATION_DIR'])
        self.doc.saveAs(str(folder / 'Source.cadprt'))
        external.saveAs(str(folder / 'Parent.cadprt'))
        Model.add_component(parent, self.part)
        with self.assertRaisesRegex(ValueError, 'outside references'):
            Model.delete_definition(self.part)

    def testRollbackAfterDeletion(self):
        self.unused()
        names = {obj.Name for obj in self.doc.Objects}
        with patch.object(Model, 'validate', side_effect=RuntimeError('Injected failure')):
            with self.assertRaisesRegex(RuntimeError, 'Injected failure'):
                Model.delete_definition(self.part)
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
        Model.validate(self.doc)
        self.assertFalse(self.doc.HasPendingTransaction)

    def testPendingEditRefused(self):
        self.unused()
        self.doc.openTransaction('Owner edit')
        self.part.Label = 'Edited'
        with self.assertRaises(ValueError): Model.delete_definition(self.part)
        self.assertIsNotNone(self.doc.getObject(self.part.Name))
        self.doc.abortTransaction()

    def testExpressionConsumerAndNativeBodyOwnership(self):
        self.unused()
        body = self.doc.addObject('PartDesign::Body', 'Body')
        Model.register_object(self.part, body, 'Object')
        box = body.newObject('PartDesign::AdditiveBox', 'Box')
        body.Tip = box
        consumer = self.doc.addObject('Part::Box', 'Consumer')
        consumer.setExpression('Length', 'Box.Length')
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, 'outside references'):
            Model.delete_definition(self.part)
        self.doc.removeObject(consumer.Name)
        names = {obj.Name for obj in Model.definition_deletion_plan(self.part)}
        self.assertIn(box.Name, names)
        Model.delete_definition(self.part)
        self.assertTrue(names.isdisjoint({obj.Name for obj in self.doc.Objects}))
        self.doc.undo()
        self.assertEqual(self.doc.Body.Tip, self.doc.Box)
        Model.validate(self.doc)
