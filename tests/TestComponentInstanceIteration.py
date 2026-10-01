# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three feedback workflows for separating an instance without losing its context."""
import hashlib
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
import CadDocument
import ComponentModel as Model
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as Navigator


class TestComponentInstanceIteration(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, relative in [(Model, "src/Mod/Part/ComponentModel.py"),
                                 (Navigator, "src/Gui/ComponentNavigator.py")]:
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((source / relative).read_bytes()).digest())
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        self.doc = Model.new_document("Instance feedback")
        self.root = Model.metadata(self.doc).RootComponent
        self.first = Model.add_component(self.root, label="Support")
        self.part = self.first.LinkedObject
        self.second = Model.add_component(self.root, self.part,
            placement=App.Placement(App.Vector(40, 0, 0), App.Rotation(App.Vector(0, 0, 1), 30)))
        self.operation, self.body = self.box(self.part, "SupportBody", 2)
        self.child = Model.add_component(self.part, label="Pin")
        self.pin_operation, self.pin = self.box(self.child.LinkedObject, "PinBody", 1)
        self.local_reference = Model.add_reference(self.part, self.child, self.pin)
        self.doc.saveAs(str(self.output / (self._testMethodName + ".cadprt")))
        self.panel = Navigator.show(self.doc)

    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def box(self, component, label, length):
        with Model.transaction(component.Document, "Create box"):
            obj = component.Document.addObject("Part::Box", label)
            Model.register_object(component, obj, "Operation")
            obj.Length, obj.Width, obj.Height = length, 3, 4
            component.Document.recompute()
            body = Model.publish_result(component, obj, label + " result")
        return obj, body

    def testParentReferencesFollowOnlyCopiedInstanceAndUndo(self):
        selected = Model.add_reference(self.root, self.second, self.body)
        untouched = Model.add_reference(self.root, self.first, self.body)
        with Model.transaction(self.doc, "Mirror reference"):
            mirror = self.doc.addObject("Part::Mirroring", "ParentMirror")
            Model.register_object(self.root, mirror, "Operation")
            mirror.Source, mirror.Normal = selected, App.Vector(1, 0, 0)
            self.doc.recompute()
            mirrored_body = Model.publish_result(self.root, mirror)
        identity, order = selected.ObjectId, list(self.root.ModelHistory)
        placement = self.second.LinkPlacement.toMatrix()
        copied = Model.make_independent(self.second)
        copied_body = selected.SourceObject
        self.assertEqual(Model.owner(copied_body), copied)
        self.assertEqual(selected.SourceObjectId, copied_body.ObjectId)
        self.assertEqual(selected.ObjectId, identity)
        self.assertEqual(list(self.root.ModelHistory), order)
        self.assertEqual(untouched.SourceObject, self.body)
        self.assertEqual(Model.children(copied)[0].LinkedObject, self.child.LinkedObject)
        copied_reference = next(obj for obj in Model.history(copied) if obj.ComponentRole == "Reference")
        self.assertEqual(copied_reference.SourceOccurrence, Model.children(copied)[0])
        self.assertEqual(copied_reference.SourceObject, self.pin)
        self.assertEqual(copied_reference.ResultStatus, "Ready")
        for actual, expected in zip(self.second.LinkPlacement.toMatrix().A, placement.A):
            self.assertAlmostEqual(actual, expected)
        self.doc.undo()
        Model.activate(self.root)
        self.assertEqual(self.second.LinkedObject, self.part)
        self.assertEqual(selected.SourceObject, self.body)
        self.assertEqual(selected.SourceObjectId, self.body.ObjectId)
        self.doc.redo()
        Model.activate(self.root)
        copied_body = selected.SourceObject
        with Model.transaction(self.doc, "Resize copied support"):
            copied_body.Producer.Length = 5
        Model.activate(self.root)
        self.assertAlmostEqual(selected.Shape.Volume, 60)
        self.assertEqual(mirror.Source, selected)
        self.assertAlmostEqual(mirrored_body.Shape.Volume, 60)
        self.assertAlmostEqual(untouched.Shape.Volume, 24)
        self.assertAlmostEqual(self.body.Shape.Volume, 24)
        self.assertEqual(selected.ObjectId, identity)
        # An unrelated reference inside the copied component is not an input
        # to the parent's mirror of the support body.
        copied_reference = next(obj for obj in Model.history(self.second.LinkedObject)
                                if obj.ComponentRole == "Reference")
        Model.set_suppressed(copied_reference, True)
        Model.activate(self.root)
        self.assertEqual(Model.history_state(mirror), "Ready")
        self.assertAlmostEqual(mirrored_body.Shape.Volume, 60)
        self.doc.saveAs(str(self.output / "Component-Independent-References.cadprt"))

    def testNestedDisplayCopyContextAndReopen(self):
        Model.set_representation(self.part, [self.child.ObjectId], "Bodies Only")
        old_path = [self.second.ObjectId, self.child.ObjectId]
        peer_path = [self.first.ObjectId, self.child.ObjectId]
        Model.set_representation(self.root, old_path, "Hidden")
        Model.set_representation(self.root, peer_path, "Full Component")
        self.panel.active_path = [self.second.ObjectId]
        self.panel.active_key = Navigator.object_key(self.part)
        self.panel.refresh()
        with patch.object(QtWidgets.QInputDialog, "getText", return_value=("Support custom", True)):
            self.panel.copy_part(Navigator.object_key(self.second))
        self.panel.refresh()
        copied = self.second.LinkedObject
        new_child = Model.children(copied)[0]
        new_path = [self.second.ObjectId, new_child.ObjectId]
        self.assertEqual(self.panel.active_key, Navigator.object_key(copied))
        self.assertEqual(Gui.activeDocument().activeView().getActiveObject("part"), copied)
        overrides = json.loads(self.root.RepresentationOverrides)
        self.assertNotIn("/".join(old_path), overrides)
        self.assertEqual(overrides["/".join(new_path)], "Hidden")
        self.assertEqual(overrides["/".join(peer_path)], "Full Component")
        self.assertEqual(Model.representation(copied, [new_child.ObjectId]), "Bodies Only")
        self.assertEqual(new_child.LinkedObject, self.child.LinkedObject)
        self.doc.undo()
        self.doc.recompute()
        self.panel.refresh()
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.part))
        self.assertEqual(Model.representation(self.root, old_path), "Hidden")
        self.doc.redo()
        self.doc.recompute()
        self.panel.refresh()
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.second.LinkedObject))
        path = self.output / "Component-Independent-Assembly.cadprt"
        self.doc.saveAs(str(path))
        second_name = self.second.Name
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(path)
        self.root = Model.metadata(self.doc).RootComponent
        self.second = self.doc.getObject(second_name)
        new_child = Model.children(self.second.LinkedObject)[0]
        self.assertEqual(Model.representation(self.root, [self.second.ObjectId, new_child.ObjectId]), "Hidden")
        self.panel = Navigator.show(self.doc)
        self.panel.active_path = [self.second.ObjectId]
        self.panel.refresh()
        self.panel.tabs.setCurrentWidget(self.panel.structure)
        self.panel.setFloating(True)
        self.panel.resize(850, 650)
        self.panel.structure.expandAll()
        Gui.updateGui()
        self.panel.grab().save(str(self.output / "independent-components.png"))

    def testExternalDefinitionCopyAndAmbiguityPreflight(self):
        external = Model.new_document("External support")
        external_root = Model.metadata(external).RootComponent
        operation, body = self.box(external_root, "ExternalBody", 3)
        source_file = self.output / "External-Original.cadprt"
        external.saveAs(str(source_file))
        original_bytes = source_file.read_bytes()
        link = Model.add_component(self.root, external_root)
        reference = Model.add_reference(self.root, link, body)
        # A native face consumer is deliberately not guessed during separation.
        consumer = self.doc.addObject("Part::FeaturePython", "FaceConsumer")
        Model.register_object(self.root, consumer, "Operation")
        consumer.addProperty("App::PropertyLinkSub", "Input")
        consumer.Input = (reference, ["Face1"])
        self.doc.recompute()
        names = [obj.Name for obj in self.doc.Objects]
        with self.assertRaisesRegex(ValueError, "Face or edge"):
            Model.make_independent(link)
        self.assertEqual([obj.Name for obj in self.doc.Objects], names)
        self.assertEqual(link.LinkedObject, external_root)
        self.assertEqual(reference.SourceObject, body)
        with Model.transaction(self.doc, "Remove face consumer"):
            self.doc.removeObject(consumer.Name)
        copied = Model.make_independent(link)
        self.assertEqual(copied.Document, self.doc)
        self.assertEqual(Model.owner(reference.SourceObject), copied)
        reference.SourceObject.Producer.Length = 6
        self.doc.recompute()
        Model.activate(self.root)
        self.assertAlmostEqual(reference.Shape.Volume, 72)
        self.assertAlmostEqual(body.Shape.Volume, 36)
        self.assertEqual(source_file.read_bytes(), original_bytes)
        self.assertEqual(Model.history(external_root), [operation, body])
        self.doc.saveAs(str(self.output / "Component-Embedded-Copy.cadprt"))
