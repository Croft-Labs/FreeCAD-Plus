# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three feedback workflows for locating moved component files."""
import hashlib
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import zipfile

import FreeCAD as App
import FreeCADGui as Gui
import Part
import CadDocument
import ComponentModel as Model
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as Navigator


class TestComponentFileRecovery(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, relative in [(Model, "src/Mod/Part/ComponentModel.py"),
                                 (Navigator, "src/Gui/ComponentNavigator.py")]:
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((source / relative).read_bytes()).digest())
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / self._testMethodName
        self.output.mkdir()
        external = Model.new_document("Support")
        definition = Model.metadata(external).RootComponent
        bodies = []
        for name, length in (("FirstBody", 2), ("SecondBody", 3)):
            body = external.addObject("Part::Feature", name)
            Model.register_object(definition, body, "Object", True)
            body.Shape = Part.makeBox(length, 3, 4)
            bodies.append(body)
        external.recompute()
        self.source_path = self.output / "Original-Source.cadprt"
        external.saveAs(str(self.source_path))
        self.doc = Model.new_document("Recovery feedback")
        self.root = Model.metadata(self.doc).RootComponent
        self.parent_path = self.output / "Recovery-Parent.cadprt"
        self.doc.saveAs(str(self.parent_path))
        first = Model.add_component(self.root, definition)
        second = Model.add_component(self.root, definition,
            placement=App.Placement(App.Vector(30, 5, 0), App.Rotation(App.Vector(0, 0, 1), 45)))
        references = [Model.add_reference(self.root, link, body) for link, body in zip((first, second), bodies)]
        self.link_names = [first.Name, second.Name]
        self.ref_names = [obj.Name for obj in references]
        self.reference_ids = [obj.ObjectId for obj in references]
        self.source_ids = [obj.SourceObjectId for obj in references]
        self.second_placement = list(second.LinkPlacement.toMatrix().A)
        self.doc.save()
        self.original_parent = self.parent_path.read_bytes()
        self.close_all()
        self.relocated = self.output / "Relocated-Support.cadprt"
        self.source_path.rename(self.relocated)

    def close_all(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def tearDown(self):
        self.close_all()
        Gui.updateGui()

    def open_missing(self):
        self.doc = CadDocument.open(self.parent_path)
        self.root = Model.metadata(self.doc).RootComponent
        self.links = [self.doc.getObject(name) for name in self.link_names]
        self.references = [self.doc.getObject(name) for name in self.ref_names]
        self.panel = Navigator.show(self.doc)
        self.panel.tabs.setCurrentWidget(self.panel.structure)
        self.assertTrue(all(link.LinkedObject is None for link in self.links))
        self.assertTrue(all(obj.Shape.isNull() for obj in self.references))

    def capture(self, name):
        self.panel.refresh()
        self.panel.setFloating(True)
        self.panel.resize(850, 650)
        self.panel.show()
        Gui.updateGui()
        self.panel.grab().save(str(self.output / name))

    def testGroupedLocateUndoAndReopen(self):
        self.open_missing()
        row = self.panel.structure.topLevelItem(0)
        self.assertEqual(row.text(0), "Support")
        self.assertEqual(row.text(2), "x2")
        self.assertEqual(row.text(3), "Missing component")
        menu = self.panel.build_menu(self.panel.structure, row)
        actions = {action.text(): action for action in menu.actions()}
        self.assertFalse(actions["Edit"].isEnabled())
        self.assertFalse(actions["Save to External File"].isEnabled())
        self.assertTrue(actions["Locate Component File"].isEnabled())
        instances = next(sub for sub in menu.component_submenus if sub.title() == "Instances")
        self.assertTrue(all(not action.isEnabled() for action in instances.actions()))
        count = len(self.doc.Objects)
        with self.assertRaisesRegex(ValueError, "Locate"):
            self.panel.add_instance(Navigator.object_key(self.links[0]))
        self.panel.toggle_component(row)
        self.assertEqual(len(self.doc.Objects), count)
        self.panel.toggle_instances(row)
        self.panel.refresh()
        row = self.panel.structure.topLevelItem(0)
        self.assertEqual(row.childCount(), 2)
        self.assertEqual(row.child(1).text(0), "Support#002")
        self.capture("missing-instances.png")
        with patch.object(QtWidgets.QFileDialog, "getOpenFileName", return_value=(str(self.relocated), "")):
            self.panel.repair_component(Navigator.object_key(self.links[0]))
        self.panel.refresh()
        self.assertEqual(self.panel.root_key, Navigator.object_key(self.root))
        self.assertEqual(App.ActiveDocument, self.doc)
        self.assertEqual(self.links[0].LinkedObject, self.links[1].LinkedObject)
        self.assertTrue(all(link.LinkedObject is not None for link in self.links))
        for actual, expected in zip(self.links[1].LinkPlacement.toMatrix().A, self.second_placement):
            self.assertAlmostEqual(actual, expected)
        self.assertEqual([obj.ObjectId for obj in self.references], self.reference_ids)
        self.assertAlmostEqual(Model.current_shape(self.references[0]).Volume, 24)
        self.assertAlmostEqual(Model.current_shape(self.references[1]).Volume, 36)
        self.doc.undo()
        Model.activate(self.root, strict=False)
        self.assertTrue(all(link.LinkedObject is None for link in self.links))
        self.doc.redo()
        Model.activate(self.root)
        self.assertTrue(all(link.LinkedObject is not None for link in self.links))
        self.doc.save()
        self.close_all()
        self.doc = CadDocument.open(self.parent_path)
        self.root = Model.metadata(self.doc).RootComponent
        self.assertTrue(all(self.doc.getObject(name).LinkedObject is not None for name in self.link_names))
        self.assertAlmostEqual(Model.current_shape(self.doc.getObject(self.ref_names[1])).Volume, 36)
        self.panel = Navigator.show(self.doc)
        self.capture("located-instances.png")

    def testMissingGeometryDoesNotBlockFileRecovery(self):
        external = CadDocument.open(self.relocated)
        missing = next(obj for obj in external.Objects if getattr(obj, "ObjectId", "") == self.source_ids[1])
        with Model.transaction(external, "Remove unavailable source body"):
            external.removeObject(missing.Name)
        external.save()
        self.close_all()
        self.open_missing()
        Model.repair_component(self.root, self.links[0], self.relocated)
        self.assertTrue(all(link.LinkedObject is not None for link in self.links))
        healthy, broken = self.references
        self.assertAlmostEqual(Model.current_shape(healthy).Volume, 24)
        self.assertIsNone(broken.SourceObject)
        self.assertEqual(broken.SourceObjectId, self.source_ids[1])
        self.assertEqual(broken.ResultStatus, "Missing source")
        self.assertTrue(broken.Shape.isNull())
        self.assertEqual(broken.ObjectId, self.reference_ids[1])
        self.doc.undo()
        Model.activate(self.root, strict=False)
        self.assertTrue(all(link.LinkedObject is None for link in self.links))
        self.doc.redo()
        Model.activate(self.root, strict=False)
        self.assertEqual(broken.getTypeIdOfProperty("SourceObject"), "App::PropertyXLink")
        self.assertIsNone(broken.SourceObject)
        with Model.transaction(self.doc, "Use recovered reference"):
            mirror = self.doc.addObject("Part::Mirroring", "RecoveredMirror")
            Model.register_object(self.root, mirror, "Operation")
            mirror.Source, mirror.Normal = healthy, App.Vector(1, 0, 0)
            self.doc.recompute()
            result = Model.publish_result(self.root, mirror)
        self.assertAlmostEqual(Model.current_shape(result).Volume, 24)
        self.doc.save()
        with zipfile.ZipFile(self.parent_path) as archive:
            self.assertNotIn(b"Original-Source.cadprt", archive.read("Document.xml"))
        self.close_all()
        self.doc = CadDocument.open(self.parent_path)
        broken = self.doc.getObject(self.ref_names[1])
        self.assertEqual(broken.ResultStatus, "Missing source")
        self.assertTrue(broken.ReferenceError)
        self.assertAlmostEqual(Model.current_shape(self.doc.getObject(self.ref_names[0])).Volume, 24)

    def testWrongFileRefusalRetainsParentContext(self):
        wrong = Model.new_document("Unrelated component")
        wrong_path = self.output / "Wrong-Component.cadprt"
        wrong.saveAs(str(wrong_path))
        self.close_all()
        self.open_missing()
        names = [obj.Name for obj in self.doc.Objects]
        with patch.object(QtWidgets.QFileDialog, "getOpenFileName", return_value=(str(wrong_path), "")):
            with self.assertRaisesRegex(ValueError, "identity"):
                self.panel.repair_component(Navigator.object_key(self.links[0]))
        self.assertEqual(App.ActiveDocument, self.doc)
        self.assertEqual(self.panel.root_key, Navigator.object_key(self.root))
        self.assertEqual([obj.Name for obj in self.doc.Objects], names)
        self.assertTrue(all(link.LinkedObject is None for link in self.links))
        self.assertEqual(self.parent_path.read_bytes(), self.original_parent)
