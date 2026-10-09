# SPDX-License-Identifier: LGPL-2.1-or-later
"""Fresh native-process acceptance of file imports and independent definitions."""
import hashlib
import json
import os
import shutil
from pathlib import Path
import unittest

import FreeCAD as App
import ComponentModel as Model
import CadDocument


class TestComponentFileHierarchyCold(unittest.TestCase):
    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def testInstalledNestedHierarchyAndSharedEditsAcrossProcesses(self):
        self.assertFalse(App.listDocuments(), "Run cold acceptance in a fresh process")
        self.assertNotEqual(os.environ.get("FREECAD_PLUS_PROFILE_SOURCE"), "1")
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        application = Path(App.ConfigGet("AppHomePath")).resolve()
        for module in (Model, CadDocument):
            installed = Path(module.__file__).resolve()
            self.assertTrue(installed.is_relative_to(application))
            self.assertEqual(hashlib.sha256(installed.read_bytes()).hexdigest(),
                hashlib.sha256((source / "src/Mod/Part" / installed.name).read_bytes()).hexdigest())
        fixtures = Path(os.environ["FREECAD_PLUS_COMPONENT_FIXTURES"])
        expected = json.loads((fixtures / "cold-hierarchy.json").read_text(encoding="utf-8"))
        # Keep the writer's fixture immutable so repeated cold/shortcut runs start
        # from the same saved state and edit only their own validation copies.
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        for name in ("ColdAssembly", "ColdHardware", "ColdCoatings", "ColdOtherAssembly"):
            shutil.copy2(fixtures / (name + ".cadprt"), output / (name + ".cadprt"))
        filename = output / "ColdAssembly.cadprt"
        assembly = CadDocument.open(filename)
        hardware = Model.external_documents(assembly)[0]
        coatings = Model.external_documents(hardware)[0]
        self.assertEqual([Model.metadata(d).ObjectId for d in (assembly, hardware, coatings)],
                         [expected[key] for key in ("assembly", "hardware", "coatings")])
        self.assertIn(expected["zinc"], [c.ObjectId for c in Model.definitions(coatings)])
        root = Model.metadata(assembly).RootComponent
        links = {link.ObjectId: link for link in Model.children(root)}
        domestic = links[expected["replaced"]].LinkedObject
        screw = links[expected["shared"]].LinkedObject
        self.assertEqual((domestic.ObjectId, screw.ObjectId),
                         (expected["domestic"], expected["screw"]))
        self.assertEqual(links[expected["replaced"]].LinkPlacement.Base, App.Vector(12, 3, 4))
        self.assertEqual(domestic.Document, assembly)
        self.assertEqual(screw.Document, hardware)
        self.assertEqual(Model.history(domestic)[0].Length.Value, 3)
        self.assertEqual(Model.history(screw)[0].Length.Value, 7)
        other = CadDocument.open(output / "ColdOtherAssembly.cadprt")
        self.assertEqual(Model.children(Model.metadata(other).RootComponent)[0].LinkedObject, screw)
        shape = Model.history(screw)[0]
        shape.Length = 11
        hardware.recompute()
        hardware.save()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        assembly = CadDocument.open(filename)
        links = {link.ObjectId: link for link in Model.children(Model.metadata(assembly).RootComponent)}
        self.assertEqual(Model.history(links[expected["shared"]].LinkedObject)[0].Length.Value, 11)
        self.assertEqual(Model.history(links[expected["replaced"]].LinkedObject)[0].Length.Value, 3)
        Model.validate(assembly)
