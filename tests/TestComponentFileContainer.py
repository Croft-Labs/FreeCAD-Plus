# SPDX-License-Identifier: LGPL-2.1-or-later
"""Explicit and open-time file-root migration preserve native identities."""
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
        occurrence_name = occurrence.Name
        Model.ensure_file_container(self.doc)
        self.assertEqual(occurrence.LinkedObject, self.part)
        Model.validate(consumer)
        self.doc.save()
        consumer.save()
        App.closeDocument(consumer.Name)
        App.closeDocument(self.doc.Name)
        consumer = CadDocument.open(str(self.output / "consumer.cadprt"))
        restored = consumer.getObject(occurrence_name).LinkedObject
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

    def testExternalCopyHasFileRootAndIndependentPlacedDefinition(self):
        source_ids = {obj.Name: getattr(obj, "ObjectId", None) for obj in self.doc.Objects}
        filename = self.output / "independent-copy.cadprt"
        copied = Model.copy_to_external_file(self.part, filename)
        destination = copied.Document
        root = Model.metadata(destination).RootComponent
        self.assertTrue(Model.is_file_container(root))
        self.assertFalse(Model.is_file_container(copied))
        self.assertEqual(Model.children(root)[0].LinkedObject, copied)
        self.assertNotEqual(copied.ObjectId, self.part.ObjectId)
        self.assertEqual(copied.Placement.toMatrix(), self.part.Placement.toMatrix())
        self.assertEqual(Model.children(root)[0].LinkPlacement.toMatrix(), copied.Placement.toMatrix())
        self.assertEqual(destination.UndoCount, 0)
        self.assertEqual(source_ids, {obj.Name: getattr(obj, "ObjectId", None) for obj in self.doc.Objects})
        ids = root.ObjectId, copied.ObjectId
        App.closeDocument(destination.Name)
        reopened = CadDocument.open(str(filename))
        root = Model.metadata(reopened).RootComponent
        self.assertEqual((root.ObjectId, Model.children(root)[0].LinkedObject.ObjectId), ids)
        self.assertEqual(len([obj for obj in Model.definitions(reopened) if obj.Label == "Part001"]), 0)

    def testLegacyExternalizeKeepsReturnedDefinitionBelowFile(self):
        self.doc.saveAs(str(self.output / "externalize-owner.cadprt"))
        source_id = self.child.LinkedObject.ObjectId
        moved = Model.externalize(self.child.LinkedObject, self.output / "externalized-child.cadprt")
        root = Model.metadata(moved.Document).RootComponent
        self.assertTrue(Model.is_file_container(root))
        self.assertEqual(Model.children(root)[0].LinkedObject, moved)
        self.assertEqual(moved.ObjectId, source_id)
        self.assertEqual(self.child.LinkedObject, moved)
        self.assertEqual(moved.Document.UndoCount, 0)
        Model.validate(self.doc)

    def testOpenUpgradesVerifiedOldFileWithoutChangingOriginal(self):
        filename = self.output / "open-old-file.cadprt"
        self.doc.saveAs(str(filename))
        original = filename.read_bytes()
        part_name, part_id = self.part.Name, self.part.ObjectId
        identities = {obj.Name: getattr(obj, "ObjectId", None) for obj in self.doc.Objects}
        placement = list(self.part.Placement.toMatrix().A)
        box_name = self.box.Name
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(filename)
        root = Model.metadata(self.doc).RootComponent
        self.assertTrue(Model.is_file_container(root))
        self.assertEqual(list(root.ModelHistory), [])
        part = self.doc.getObject(part_name)
        self.assertEqual(part.ObjectId, part_id)
        self.assertEqual(part.Label, "Existing assembly")
        self.assertEqual(list(part.Placement.toMatrix().A), placement)
        self.assertEqual(Model.owner(self.doc.getObject(box_name)), part)
        self.assertEqual(Model.children(root)[0].LinkedObject, part)
        self.assertEqual(list(Model.children(root)[0].LinkPlacement.toMatrix().A), placement)
        for name, identity in identities.items():
            self.assertEqual(getattr(self.doc.getObject(name), "ObjectId", None), identity)
        self.assertEqual(filename.read_bytes(), original)
        if App.GuiUp:
            import sys
            from PySide import QtCore
            navigator = sys.modules["freecad.gui.ComponentNavigator"]
            panel = navigator.show(self.doc)
            panel.refresh()
            self.assertEqual(panel.active_key, navigator.object_key(root))
            self.assertEqual(panel.structure.topLevelItemCount(), 1)
            self.assertEqual(panel.structure.topLevelItem(0).text(0), self.doc.Label)
            self.assertEqual(panel.history.topLevelItemCount(), 1)  # File Origin only.
            models = [panel.models.topLevelItem(i).data(0, QtCore.Qt.UserRole)
                      for i in range(panel.models.topLevelItemCount())]
            self.assertIn(navigator.object_key(part), models)
            self.assertNotIn(navigator.object_key(root), models)
            panel.grab().save(str(self.output / "migrated-file-panel.png"))
        self.doc.undo()
        self.assertEqual(Model.metadata(self.doc).RootComponent, root)
        root_id = root.ObjectId
        self.doc.save()
        self.assertEqual(CadDocument.preflight(filename)["file_container"], root_id)
        count = len(self.doc.Objects)
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(filename)
        self.assertEqual(Model.metadata(self.doc).RootComponent.ObjectId, root_id)
        self.assertEqual(len(self.doc.Objects), count)

    def testFailedOpenMigrationRollsBackNewGraphOnly(self):
        filename = self.output / "failed-old-open.cadprt"
        self.doc.saveAs(str(filename))
        original = filename.read_bytes()
        App.closeDocument(self.doc.Name)
        retained = Model.new_document("Unsaved user document")
        before = [(obj.Name, getattr(obj, "ObjectId", None)) for obj in retained.Objects]
        with patch.object(Model, "ensure_file_container", side_effect=RuntimeError("migration failed")):
            with self.assertRaisesRegex(RuntimeError, "migration failed"):
                CadDocument.open(filename)
        self.assertEqual(list(App.listDocuments()), [retained.Name])
        self.assertEqual(App.ActiveDocument, retained)
        self.assertEqual([(obj.Name, getattr(obj, "ObjectId", None)) for obj in retained.Objects], before)
        self.assertEqual(filename.read_bytes(), original)

    def testOpenMigratesDependenciesAndPreservesExternalTargets(self):
        source_path = self.output / "old-dependency.cadprt"
        self.doc.saveAs(str(source_path))
        source_id = self.part.ObjectId
        consumer = Model.new_document("Old consumer")
        target_path = self.output / "old-consumer.cadprt"
        consumer.saveAs(str(target_path))
        occurrence = Model.add_component(Model.metadata(consumer).RootComponent, self.part)
        name, occurrence_id = occurrence.Name, occurrence.ObjectId
        consumer.save()
        source_bytes, target_bytes = source_path.read_bytes(), target_path.read_bytes()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        consumer = CadDocument.open(target_path)
        occurrence = consumer.getObject(name)
        source = occurrence.LinkedObject.Document
        self.assertTrue(Model.is_file_container(Model.metadata(consumer).RootComponent))
        self.assertTrue(Model.is_file_container(Model.metadata(source).RootComponent))
        self.assertEqual(occurrence.ObjectId, occurrence_id)
        self.assertEqual(occurrence.LinkedObject.ObjectId, source_id)
        self.assertFalse(Model.is_file_container(occurrence.LinkedObject))
        self.assertEqual(source_path.read_bytes(), source_bytes)
        self.assertEqual(target_path.read_bytes(), target_bytes)
        Model.validate(consumer)

    def testFileActivationRefreshesNestedDomesticReferences(self):
        import Part
        middle = self.child.LinkedObject
        inner = Model.add_component(middle, label="Source")
        shape = self.doc.addObject("Part::Feature", "ReferenceSource")
        shape.Shape = Part.makeBox(2, 3, 4)
        Model.register_object(inner.LinkedObject, shape, "Object", True)
        self.doc.recompute()
        intermediate = Model.add_reference(middle, inner, shape)
        outer = Model.add_reference(self.part, self.child, intermediate)
        root = Model.ensure_file_container(self.doc)
        shape.Shape = Part.makeBox(5, 3, 4)
        self.doc.recompute()
        Model.activate(root)
        self.assertAlmostEqual(Model.current_shape(intermediate).Volume, 60)
        self.assertAlmostEqual(Model.current_shape(outer).Volume, 60)
        self.assertEqual(list(root.ModelHistory), [])
        self.assertEqual(Model.owner(intermediate), middle)
        self.assertEqual(Model.owner(outer), self.part)
