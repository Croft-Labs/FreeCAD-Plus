# SPDX-License-Identifier: LGPL-2.1-or-later
"""Direct-child part type policy and native persistence; UI integration is separate."""
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import zipfile

import FreeCAD as App
import ComponentModel as Model
import CadDocument


class TestComponentPartTypes(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_document("PartTypes")
        self.root = Model.metadata(self.doc).RootComponent
        self.assembly = Model.add_component(self.root, label="Fan assembly")
        self.parent = self.assembly.LinkedObject
        self.fan = Model.add_component(self.parent, label="Fan")
        self.bottom = Model.add_component(self.parent, label="Bottom plate")
        self.bottom_fan = Model.add_component(self.bottom.LinkedObject, self.fan.LinkedObject)
        self.top = Model.add_component(self.parent, label="Top plate")
        self.top_bottom = Model.add_component(self.top.LinkedObject, self.bottom.LinkedObject)
        self.top_fan = Model.add_component(self.top.LinkedObject, self.fan.LinkedObject)

    def tearDown(self):
        for doc in reversed(list(App.listDocuments().values())):
            App.closeDocument(doc.Name)

    def types(self):
        Model.set_part_types(self.bottom.LinkedObject, [(self.bottom_fan, "Excluded")])
        Model.set_part_types(self.top.LinkedObject, [
            (self.top_bottom, "Reference"), (self.top_fan, "Reference")])

    def testDefaultsAndDirectOwnership(self):
        self.assertEqual(Model.effective_part_type(self.root, []), "Full Component")
        self.assertEqual(Model.part_type(self.parent, self.fan), "Bodies Only")
        before = self.doc.UndoCount
        with self.assertRaisesRegex(ValueError, "direct child"):
            Model.set_part_types(self.parent, [(self.top_fan, "Reference")])
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            Model.set_part_types(self.parent, [(self.fan, "Hidden")])
        self.assertEqual(self.doc.UndoCount, before)
        self.assertNotIn("PartType", self.fan.PropertiesList)

    def testOwnerExamplesAndContextRestoration(self):
        self.types()
        top = [self.assembly.ObjectId, self.top.ObjectId]
        bottom = top + [self.top_bottom.ObjectId]
        fan = top + [self.top_fan.ObjectId]
        nested = bottom + [self.bottom_fan.ObjectId]
        for active in ([], [self.assembly.ObjectId]):
            self.assertEqual(Model.effective_part_type(self.root, bottom, active), "Excluded")
            self.assertEqual(Model.effective_part_type(self.root, fan, active), "Excluded")
        self.assertEqual(Model.effective_part_type(self.root, top, top), "Full Component")
        self.assertEqual(Model.effective_part_type(self.root, bottom, top), "Reference")
        self.assertEqual(Model.effective_part_type(self.root, fan, top), "Reference")
        self.assertEqual(Model.effective_part_type(self.root, nested, top), "Excluded")
        self.assertEqual(Model.part_type(self.top.LinkedObject, self.top_bottom), "Reference")

    def testGeometryGateAndVisibilityIndependence(self):
        self.types()
        path = [self.assembly.ObjectId, self.top.ObjectId, self.top_bottom.ObjectId]
        self.assertFalse(Model.part_type_allows_geometry(self.root, path))
        self.assertFalse(Model.part_type_allows_geometry(
            self.root, path + [self.bottom_fan.ObjectId]))
        self.assertTrue(Model.part_type_allows_geometry(
            self.root, [self.assembly.ObjectId, self.fan.ObjectId]))
        before = self.bottom_fan.Visibility
        self.bottom_fan.Visibility = True
        self.assertEqual(Model.effective_part_type(self.bottom.LinkedObject,
            [self.bottom_fan.ObjectId]), "Excluded")
        self.assertTrue(self.bottom_fan.IncludeInBOM)
        self.assertTrue(self.bottom_fan.IncludeInMass)
        self.bottom_fan.Visibility = before

    def testActivePartIgnoresOuterExclusion(self):
        Model.set_part_types(self.parent, [(self.top, "Excluded")])
        top = [self.assembly.ObjectId, self.top.ObjectId]
        self.assertEqual(Model.effective_part_type(self.root, top, top), "Full Component")
        self.assertEqual(Model.effective_part_type(
            self.root, top + [self.top_fan.ObjectId], top), "Bodies Only")
        self.assertEqual(Model.part_type(self.parent, self.top), "Excluded")

    def testAtomicUndoRedoAndReset(self):
        parent = self.top.LinkedObject
        count = self.doc.UndoCount
        Model.set_part_types(parent, [(self.top_bottom, "Reference"), (self.top_fan, "Excluded")])
        self.assertEqual(self.doc.UndoCount, count + 1)
        self.doc.undo()
        self.assertEqual(Model.part_type(parent, self.top_bottom), "Bodies Only")
        self.assertEqual(Model.part_type(parent, self.top_fan), "Bodies Only")
        self.doc.redo()
        self.assertEqual(Model.part_type(parent, self.top_bottom), "Reference")
        self.assertEqual(Model.part_type(parent, self.top_fan), "Excluded")
        Model.set_part_types(parent, [(self.top_bottom, None)])
        self.assertEqual(Model.part_type(parent, self.top_bottom), "Bodies Only")

    def testBatchValidationAndFailureRollback(self):
        parent = self.top.LinkedObject
        with self.assertRaises(ValueError):
            Model.set_part_types(parent, [(self.top_bottom, "Reference"), (self.fan, "Excluded")])
        self.assertNotIn("PartType", self.top_bottom.PropertiesList)
        original = Model._property
        def fail(obj, *args):
            if obj == self.top_fan:
                raise RuntimeError("injected")
            return original(obj, *args)
        with patch.object(Model, "_property", side_effect=fail):
            with self.assertRaisesRegex(RuntimeError, "injected"):
                Model.set_part_types(parent, [
                    (self.top_bottom, "Reference"), (self.top_fan, "Excluded")])
        self.assertNotIn("PartType", self.top_bottom.PropertiesList)

    def testLegacyRulesAreReadWithoutMigration(self):
        Model.set_representation(self.parent, [self.bottom.ObjectId], "Hidden")
        Model.set_representation(self.parent,
            [self.top.ObjectId, self.top_fan.ObjectId], "Hidden")
        before = self.parent.RepresentationOverrides
        self.assertEqual(Model.part_type(self.parent, self.bottom), "Excluded")
        self.assertEqual(Model.part_type(self.top.LinkedObject, self.top_fan), "Bodies Only")
        self.assertEqual(self.parent.RepresentationOverrides, before)
        self.assertNotIn("component-part-types-v1", json.loads(CadDocument.manifest(self.doc))["required"])

    def testSharedParentAndIndependentCopy(self):
        self.types()
        repeated = Model.add_component(self.root, self.top.LinkedObject)
        self.assertEqual(Model.part_type(repeated.LinkedObject, self.top_fan), "Reference")
        self.assertEqual(Model.part_type(self.parent, self.fan), "Bodies Only")
        copy = Model.copy_definition(self.top.LinkedObject, self.doc)
        copied = Model.children(copy)
        self.assertEqual([Model.part_type(copy, c) for c in copied], ["Reference", "Reference"])
        Model.set_part_types(copy, [(copied[0], "Excluded")])
        self.assertEqual(Model.part_type(self.top.LinkedObject, self.top_bottom), "Reference")
        Model.validate(self.doc)

    def testSaveReopenCapabilityAndTamper(self):
        self.types()
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        filename = output / "part-types.cadprt"
        self.doc.saveAs(str(filename))
        data = CadDocument.preflight(filename)
        self.assertIn("component-part-types-v1", data["required"])
        with patch.object(CadDocument, "CAPABILITIES", tuple(
                c for c in CadDocument.CAPABILITIES if c != "component-part-types-v1")):
            with self.assertRaisesRegex(ValueError, "unsupported reader"):
                CadDocument.preflight(filename)
        with zipfile.ZipFile(filename) as archive:
            entries = {name: archive.read(name) for name in archive.namelist()}
        data["required"].remove("component-part-types-v1")
        for definition in data["definitions"]:
            for occurrence in definition["occurrences"]:
                occurrence.pop("part_type", None)
        tampered = output / "stripped-part-types.cadprt"
        with zipfile.ZipFile(tampered, "w") as archive:
            for name, payload in entries.items():
                archive.writestr(name, json.dumps(data).encode() if name == CadDocument.MANIFEST else payload)
        with self.assertRaisesRegex(ValueError, "part type.*manifest"):
            CadDocument.preflight(tampered)
        name, child_name = self.top.LinkedObject.Name, self.top_bottom.Name
        App.closeDocument(self.doc.Name)
        reopened = CadDocument.open(str(filename))
        self.assertEqual(Model.part_type(reopened.getObject(name), reopened.getObject(child_name)), "Reference")
        Model.validate(reopened)

    def testExternalChildStoresTypeOnlyInParent(self):
        self.types()
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        self.doc.saveAs(str(output / "type-source.cadprt"))
        external = Model.new_document("ExternalTypes")
        external.saveAs(str(output / "type-parent.cadprt"))
        parent = Model.metadata(external).RootComponent
        link = Model.add_component(parent, self.top.LinkedObject)
        before = self.top_bottom.PartType, self.top_fan.PartType, self.doc.UndoCount
        Model.set_part_types(parent, [(link, "Excluded")])
        self.assertEqual((self.top_bottom.PartType, self.top_fan.PartType, self.doc.UndoCount), before)
        self.assertEqual(Model.part_type(parent, link), "Excluded")
        external.save()
        CadDocument.preflight(external.FileName)
