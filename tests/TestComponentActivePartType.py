# SPDX-License-Identifier: LGPL-2.1-or-later
"""Definition-owned active display overrides and native persistence."""
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import zipfile
import FreeCAD as App
import ComponentModel as Model
import CadDocument
from TestComponentPartTypes import TestComponentPartTypes as Fixture


class TestComponentActivePartType(unittest.TestCase):
    setUp = Fixture.setUp
    tearDown = Fixture.tearDown

    def testDefaultDoesNotMigrateOldFiles(self):
        self.assertEqual(Model.active_part_type(self.root), "Full Component")
        self.assertEqual(Model.effective_part_type(self.root, [], []), "Full Component")
        self.assertNotIn("ActivePartType", self.root.PropertiesList)
        data = json.loads(CadDocument.manifest(self.doc))
        self.assertNotIn("component-active-part-type-v1", data["required"])
        self.assertFalse(any("active_part_type" in d for d in data["definitions"]))

    def testActiveChoiceIsIndependentOfParentTypesAndVisibility(self):
        component = self.top.LinkedObject
        path = [self.assembly.ObjectId, self.top.ObjectId]
        Model.set_part_types(self.parent, [(self.top, "Excluded")])
        Model.set_part_types(component, [(self.top_bottom, "Reference"), (self.top_fan, "Excluded")])
        visibility = self.top.Visibility
        Model.set_active_part_type(component, "Bodies Only")
        self.assertEqual(Model.effective_part_type(self.root, path, path), "Bodies Only")
        self.assertEqual(Model.effective_part_type(self.root, path, []), "Excluded")
        self.assertEqual(Model.effective_part_type(self.root, path + [self.top_bottom.ObjectId], path), "Reference")
        self.assertEqual(Model.effective_part_type(self.root, path + [self.top_fan.ObjectId], path), "Excluded")
        self.assertFalse(Model.part_type_allows_geometry(self.root, path))
        self.assertEqual(self.top.Visibility, visibility)
        self.assertEqual(Model.part_type(self.parent, self.top), "Excluded")
        Model.set_active_part_type(component)
        self.assertEqual(Model.effective_part_type(self.root, path, path), "Full Component")

    def testUndoRedoAndInvalidRequests(self):
        component = self.top.LinkedObject
        before = self.doc.UndoCount
        for value in ("Reference", "Excluded", "Hidden", "", 42):
            with self.assertRaises(ValueError):
                Model.set_active_part_type(component, value)
        with self.assertRaises(ValueError):
            Model.set_active_part_type(self.top, "Bodies Only")
        self.assertEqual(self.doc.UndoCount, before)
        self.assertNotIn("ActivePartType", component.PropertiesList)
        Model.set_active_part_type(component, "Bodies Only")
        self.doc.undo()
        self.assertEqual(Model.active_part_type(component), "Full Component")
        self.doc.redo()
        self.assertEqual(Model.active_part_type(component), "Bodies Only")
        Model.set_active_part_type(component)
        self.doc.undo()
        self.assertEqual(Model.active_part_type(component), "Bodies Only")

    def testFailureRollsBackPropertyCreation(self):
        component = self.top.LinkedObject
        original = Model._property
        def fail(*args, **kwargs):
            original(*args, **kwargs)
            raise RuntimeError("injected")
        with patch.object(Model, "_property", side_effect=fail):
            with self.assertRaisesRegex(RuntimeError, "injected"):
                Model.set_active_part_type(component, "Bodies Only")
        self.assertNotIn("ActivePartType", component.PropertiesList)

    def testSharedAndCopiedDefinitions(self):
        component = self.top.LinkedObject
        repeated = Model.add_component(self.root, component)
        Model.set_active_part_type(component, "Bodies Only")
        ids = [repeated.ObjectId]
        self.assertEqual(Model.effective_part_type(self.root, ids, ids), "Bodies Only")
        copied = Model.copy_definition(component, self.doc)
        self.assertEqual(Model.active_part_type(copied), "Bodies Only")
        Model.set_active_part_type(copied)
        self.assertEqual(Model.active_part_type(component), "Bodies Only")
        independent = Model.make_independent(self.top, "Independent top plate")
        self.assertEqual(Model.active_part_type(independent), "Bodies Only")
        Model.validate(self.doc)

    def testSaveReopenAndCapabilityGuards(self):
        component = self.top.LinkedObject
        Model.set_active_part_type(component, "Bodies Only")
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        path = output / "active-type.cadprt"
        self.doc.saveAs(str(path))
        data = CadDocument.preflight(path)
        capability = "component-active-part-type-v1"
        self.assertIn(capability, data["required"])
        self.assertNotIn("component-part-types-v1", data["required"])
        with patch.object(CadDocument, "CAPABILITIES", tuple(
                c for c in CadDocument.CAPABILITIES if c != capability)):
            with self.assertRaisesRegex(ValueError, "unsupported reader"):
                CadDocument.preflight(path)
        with zipfile.ZipFile(path) as archive:
            entries = {n: archive.read(n) for n in archive.namelist()}
        for mode in ("stripped", "changed", "invalid"):
            modified = json.loads(json.dumps(data))
            for definition in modified["definitions"]:
                if "active_part_type" in definition:
                    if mode == "stripped":
                        del definition["active_part_type"]
                    else:
                        definition["active_part_type"] = "Full Component" if mode == "changed" else "Reference"
            if mode == "stripped":
                modified["required"].remove(capability)
            changed = output / (mode + ".cadprt")
            with zipfile.ZipFile(changed, "w") as archive:
                for name, payload in entries.items():
                    archive.writestr(name, json.dumps(modified).encode() if name == CadDocument.MANIFEST else payload)
            with self.assertRaisesRegex(ValueError, "active component part type"):
                CadDocument.preflight(changed)
        name = component.Name
        App.closeDocument(self.doc.Name)
        reopened = CadDocument.open(str(path))
        restored = reopened.getObject(name)
        self.assertEqual(Model.active_part_type(restored), "Bodies Only")
        self.assertEqual(Model.effective_part_type(restored, [], []), "Bodies Only")
        Model.validate(reopened)

    def testInvalidNativeValueCannotBeSaved(self):
        Model.set_active_part_type(self.root, "Bodies Only")
        self.root.ActivePartType = "Excluded"
        with self.assertRaisesRegex(ValueError, "active component part type"):
            CadDocument.manifest(self.doc)

    def testExternalOccurrenceDoesNotStoreActiveChoice(self):
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        self.doc.saveAs(str(output / "source.cadprt"))
        destination = Model.new_document("ExternalActiveType")
        destination.saveAs(str(output / "parent.cadprt"))
        root = Model.metadata(destination).RootComponent
        component = self.top.LinkedObject
        link = Model.add_component(root, component)
        before = destination.UndoCount
        Model.set_active_part_type(component, "Bodies Only")
        self.assertEqual(destination.UndoCount, before)
        self.assertNotIn("ActivePartType", link.PropertiesList)
        self.assertEqual(Model.effective_part_type(root, [link.ObjectId], [link.ObjectId]), "Bodies Only")
        self.doc.save()
        self.assertIn("component-active-part-type-v1", CadDocument.preflight(self.doc.FileName)["required"])
        destination.save()
        self.assertNotIn("component-active-part-type-v1", CadDocument.preflight(destination.FileName)["required"])