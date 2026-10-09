# SPDX-License-Identifier: LGPL-2.1-or-later
"""File-owned native relationship identities, save/reopen and structural guards."""
import json
import os
from pathlib import Path
from unittest.mock import patch
import zipfile
import FreeCAD as App
import ComponentModel as Model
import CadDocument
import TestComponentAssemblySolver as Pilot


class TestComponentAssemblyPersistence(Pilot.TestComponentAssemblySolver):
    def testContextCreationIsIdempotentAndUndoable(self):
        other = Model.new_file_document("EmptyContext")
        names = {o.Name for o in other.Objects}
        context = Model.ensure_assembly_context(other)
        identity = context.ObjectId
        self.assertEqual(Model.ensure_assembly_context(other), context)
        other.undo()
        self.assertIsNone(Model.assembly_context(other))
        self.assertEqual({o.Name for o in other.Objects}, names)
        other.redo()
        self.assertEqual(Model.assembly_context(other).ObjectId, identity)
        Model.validate(other)

    def testFailedContextCreationRollsBack(self):
        other = Model.new_file_document("ContextFailure")
        names = {o.Name for o in other.Objects}
        with patch.object(Model, "_identity", side_effect=RuntimeError("injected")):
            with self.assertRaisesRegex(RuntimeError, "injected"):
                Model.ensure_assembly_context(other)
        self.assertEqual({o.Name for o in other.Objects}, names)
        self.assertIsNone(Model.assembly_context(other))
        Model.validate(other)

    def testRelationshipRemovalAndReparentGuards(self):
        self.fixed()
        self.doc.recompute()
        before = {o.Name for o in self.doc.Objects}, self.doc.UndoCount
        with self.assertRaisesRegex(ValueError, "relationships"):
            Model.remove_instances([self.second])
        with self.assertRaisesRegex(ValueError, "relationships"):
            Model.move_instances(self.root, [[self.second.ObjectId]], [self.first.ObjectId])
        self.assertEqual(({o.Name for o in self.doc.Objects}, self.doc.UndoCount), before)
        self.assertOwnership()

    def testInvalidEndpointAndContextRefuseSave(self):
        joint = self.fixed()
        joint.Reference2 = (self.definition, ["", ""])
        with self.assertRaisesRegex(ValueError, "direct occurrences"):
            CadDocument.manifest(self.doc)
        joint.Reference2 = (self.second, ["", ""])
        self.context.ComponentRoot = self.definition
        with self.assertRaisesRegex(ValueError, "context ownership"):
            CadDocument.manifest(self.doc)
        self.context.ComponentRoot = self.root
        self.assertOwnership()

    def testSaveReopenAndManifestTamper(self):
        self.first.setEditorMode("LinkPlacement", 1)
        self.fixed()
        self.assertEqual(self.context.solve(), 0)
        self.doc.recompute()
        expected = Model.assembly_record(self.doc)
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        filename = output / "file-relationships.cadprt"
        self.doc.saveAs(str(filename))
        data = CadDocument.preflight(filename)
        self.assertEqual(data["assembly"], expected)
        with patch.object(CadDocument, "CAPABILITIES", tuple(
                c for c in CadDocument.CAPABILITIES if c != "component-file-assembly-v1")):
            with self.assertRaisesRegex(ValueError, "unsupported reader"):
                CadDocument.preflight(filename)
        with zipfile.ZipFile(filename) as archive:
            entries = {name: archive.read(name) for name in archive.namelist()}
        stripped = dict(data)
        stripped["required"] = [c for c in data["required"] if c != "component-file-assembly-v1"]
        del stripped["assembly"]
        stripped_file = output / "missing-assembly-capability.cadprt"
        with zipfile.ZipFile(stripped_file, "w") as archive:
            for name, payload in entries.items():
                archive.writestr(name, json.dumps(stripped).encode("utf-8")
                                 if name == CadDocument.MANIFEST else payload)
        with self.assertRaisesRegex(ValueError, "manifest"):
            CadDocument.preflight(stripped_file)
        data["assembly"]["root"] = self.definition.Name
        entries[CadDocument.MANIFEST] = json.dumps(data).encode("utf-8")
        tampered = output / "wrong-relationship-root.cadprt"
        with zipfile.ZipFile(tampered, "w") as archive:
            for name, payload in entries.items():
                archive.writestr(name, payload)
        with self.assertRaisesRegex(ValueError, "manifest"):
            CadDocument.preflight(tampered)
        App.closeDocument(self.doc.Name)
        doc = CadDocument.open(str(filename))
        self.assertEqual(Model.assembly_record(doc), expected)
        self.assertEqual(Model.assembly_context(doc).solve(), 0)
        root = Model.metadata(doc).RootComponent
        self.assertEqual(root.ModelHistory, [])
        self.assertEqual(root.ResultObjects, [])
        self.assertAlmostEqual(Model.children(root)[1].LinkPlacement.Base.x, 15, places=5)
