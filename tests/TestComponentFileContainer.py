# SPDX-License-Identifier: LGPL-2.1-or-later
"""Opt-in file-root migration preserves native components and archive identities."""
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import zipfile
import FreeCAD as App
import ComponentModel as Model
import CadDocument


class TestComponentFileContainer(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_document("Existing assembly")
        self.part = Model.metadata(self.doc).RootComponent
        self.part.Placement = App.Placement(App.Vector(13, 4, 2), App.Rotation(App.Vector(0, 0, 1), 30))
        self.child = Model.add_component(self.part, label="Child")
        self.box = self.doc.addObject("Part::Box", "Box")
        Model.register_object(self.part, self.box, "Operation")
        self.doc.recompute()
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])

    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def testMigrationPreservesIdentityPlacementAndReferences(self):
        identities = {obj.Name: getattr(obj, "ObjectId", None) for obj in self.doc.Objects}
        before = self.part.Placement.toMatrix()
        history = list(self.part.ModelHistory)
        bounds = self.part.getSubObject(self.box.Name + ".").BoundBox
        root = Model.ensure_file_container(self.doc)
        self.assertTrue(Model.is_file_container(root))
        self.assertTrue(root.Placement.isIdentity())
        self.assertEqual(self.part.Label, "Existing assembly")
        self.assertIsNotNone(root.Origin)
        link = Model.children(root)[0]
        self.assertEqual(link.LinkedObject, self.part)
        self.assertEqual(Model.representation(root, [link.ObjectId]), "Full Component")
        self.assertEqual(Model.representation(root, [link.ObjectId, self.child.ObjectId]),
                         Model.representation(self.part, [self.child.ObjectId]))
        self.assertEqual(link.LinkPlacement.toMatrix(), before)
        self.assertEqual(self.part.Placement.toMatrix(), before)
        self.assertEqual(self.part.ModelHistory, history)
        placed = root.getSubObject(link.Name + "." + self.box.Name + ".").BoundBox
        for field in ("XMin", "XMax", "YMin", "YMax", "ZMin", "ZMax"):
            self.assertAlmostEqual(getattr(placed, field), getattr(bounds, field))
        self.assertEqual(Model.owner(self.box), self.part)
        self.assertEqual(Model.owner(self.child), self.part)
        for name, ident in identities.items():
            self.assertEqual(getattr(self.doc.getObject(name), "ObjectId", None), ident)
        count = len(self.doc.Objects)
        self.assertEqual(Model.ensure_file_container(self.doc), root)
        self.assertEqual(len(self.doc.Objects), count)
        self.assertEqual(Model.validate(self.doc).RootComponent, root)

    def testUndoRedoAndFailureAreAtomic(self):
        names = {obj.Name for obj in self.doc.Objects}
        with patch.object(Model, "_add_occurrence", side_effect=RuntimeError("injected")):
            with self.assertRaises(RuntimeError):
                Model.ensure_file_container(self.doc)
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
        root = Model.ensure_file_container(self.doc)
        ident = root.ObjectId
        self.doc.undo()
        self.assertEqual(Model.metadata(self.doc).RootComponent, self.part)
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
        self.doc.redo()
        self.assertEqual(Model.validate(self.doc).RootComponent.ObjectId, ident)

    def testEmptyFileAndContainerGuards(self):
        root = Model.ensure_file_container(self.doc)
        with self.assertRaises(ValueError):
            Model.add_component(self.part, root)
        with self.assertRaises(ValueError):
            Model.register_object(root, self.box)
        Model.remove_instances(Model.children(root))
        self.assertEqual(Model.children(root), [])
        Model.validate(self.doc)
        root.Placement.Base = App.Vector(1, 0, 0)
        with self.assertRaises(ValueError):
            Model.validate(self.doc)

    def testSaveReopenAndCapabilityTamper(self):
        root = Model.ensure_file_container(self.doc)
        root_id, part_id = root.ObjectId, self.part.ObjectId
        filename = self.output / "file-container.cadprt"
        self.doc.saveAs(str(filename))
        data = CadDocument.preflight(filename)
        with patch.object(CadDocument, "CAPABILITIES", CadDocument.BASE_CAPABILITIES):
            with self.assertRaises(ValueError):
                CadDocument.preflight(filename)
        self.assertEqual(data["file_container"], root_id)
        App.closeDocument(self.doc.Name)
        reopened = CadDocument.open(str(filename))
        self.assertEqual(Model.metadata(reopened).RootComponent.ObjectId, root_id)
        self.assertEqual(Model.children(Model.metadata(reopened).RootComponent)[0].LinkedObject.ObjectId, part_id)
        with zipfile.ZipFile(filename) as archive:
            entries = {name: archive.read(name) for name in archive.namelist()}
        data["required"].remove("component-file-container-v1")
        del data["file_container"]
        entries[CadDocument.MANIFEST] = json.dumps(data).encode("utf-8")
        tampered = self.output / "missing-capability.cadprt"
        with zipfile.ZipFile(tampered, "w") as archive:
            for name, payload in entries.items():
                archive.writestr(name, payload)
        with self.assertRaises(ValueError):
            CadDocument.preflight(tampered)

    def testExistingExternalUsesKeepTheirDefinition(self):
        filename = self.output / "external-original.cadprt"
        self.doc.saveAs(str(filename))
        consumer = Model.new_document("Consumer")
        consumer.saveAs(str(self.output / "consumer.cadprt"))
        occurrence = Model.add_component(Model.metadata(consumer).RootComponent, self.part)
        part_id = self.part.ObjectId
        source_name = self.part.Name
        Model.ensure_file_container(self.doc)
        self.assertEqual(occurrence.LinkedObject, self.part)
        Model.validate(consumer)
        self.doc.save()
        consumer.save()
        App.closeDocument(consumer.Name)
        App.closeDocument(self.doc.Name)
        consumer = CadDocument.open(str(self.output / "consumer.cadprt"))
        restored = Model.children(Model.metadata(consumer).RootComponent)[0].LinkedObject
        self.assertEqual(restored.ObjectId, part_id)
        self.assertEqual(restored.Name, source_name)
        self.assertFalse(Model.is_file_container(restored))

    def testPendingTransactionRefusesMigration(self):
        names = {obj.Name for obj in self.doc.Objects}
        self.doc.openTransaction("Unfinished edit")
        self.box.Length = 7
        try:
            with self.assertRaises(ValueError):
                Model.ensure_file_container(self.doc)
            self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
        finally:
            self.doc.abortTransaction()
