# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three feedback workflows for moving embedded components to an external file."""
import hashlib
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
import CadDocument
import ComponentModel as Model
from PySide import QtWidgets
from freecad.gui import ComponentNavigator as Navigator


class TestComponentExternalization(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, relative in [(Model, "src/Mod/Part/ComponentModel.py"),
                                 (Navigator, "src/Gui/ComponentNavigator.py")]:
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((source / relative).read_bytes()).digest())
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / self._testMethodName
        self.output.mkdir()
        self.doc = Model.new_document("Externalization feedback")
        self.root = Model.metadata(self.doc).RootComponent
        self.first = Model.add_component(self.root, label="Bracket")
        self.part = self.first.LinkedObject
        self.second = Model.add_component(self.root, self.part,
            placement=App.Placement(App.Vector(30, 5, 0), App.Rotation(App.Vector(0, 0, 1), 45)))
        self.child = Model.add_component(self.part, label="Pin")
        pin = self.child.LinkedObject
        with Model.transaction(self.doc, "Create pin"):
            box = self.doc.addObject("Part::Box", "PinBox")
            Model.register_object(pin, box, "Operation")
            box.Length, box.Width, box.Height = 2, 3, 4
            self.doc.recompute()
            self.body = Model.publish_result(pin, box)
        self.peer = Model.add_component(self.root, pin)
        self.local = Model.add_reference(self.part, self.child, self.body)
        self.reference = Model.add_reference(self.root, self.second, self.local)
        with Model.transaction(self.doc, "Mirror reference"):
            mirror = self.doc.addObject("Part::Mirroring", "ParentMirror")
            Model.register_object(self.root, mirror, "Operation")
            mirror.Source, mirror.Normal = self.reference, App.Vector(1, 0, 0)
            self.doc.recompute()
            self.result = Model.publish_result(self.root, mirror)
        self.parent_path = self.output / "Parent.cadprt"
        self.destination = self.output / "Bracket.cadprt"
        self.doc.saveAs(str(self.parent_path))
        self.panel = Navigator.show(self.doc)

    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def testSharedHierarchyReferencesUndoAndReopen(self):
        definition_id, reference_id = self.part.ObjectId, self.reference.ObjectId
        local_id = self.local.ObjectId
        names = [obj.Name for obj in (self.first, self.second, self.peer, self.reference, self.result)]
        placement = list(self.second.LinkPlacement.toMatrix().A)
        order = list(self.root.ModelHistory)
        moved = Model.externalize(self.part, self.destination)
        self.assertEqual(moved.ObjectId, definition_id)
        self.assertEqual(moved.Label, "Bracket")
        self.assertEqual(Model.children(moved)[0].LinkedObject.Label, "Pin")
        self.assertEqual(self.first.LinkedObject, self.second.LinkedObject)
        self.assertEqual(Model.children(moved)[0].LinkedObject, self.peer.LinkedObject)
        self.assertEqual(self.reference.SourceObject.ObjectId, local_id)
        self.assertEqual(self.reference.ObjectId, reference_id)
        self.assertEqual(list(self.root.ModelHistory), order)
        for obj in (self.reference.SourceObject, self.reference, self.result):
            self.assertEqual(Model.history_state(obj), "Ready")
            self.assertAlmostEqual(obj.Shape.Volume, 24)
        self.assertEqual(list(self.second.LinkPlacement.toMatrix().A), placement)
        self.doc.undo()
        Model.activate(self.first.LinkedObject)
        Model.activate(self.root)
        self.assertEqual(self.first.LinkedObject.Document, self.doc)
        self.assertEqual(self.reference.SourceObject.Document, self.doc)
        self.doc.redo()
        Model.activate(self.root)
        self.assertEqual(self.first.LinkedObject.Document, moved.Document)
        self.assertAlmostEqual(self.result.Shape.Volume, 24)
        self.doc.save()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        reopened = CadDocument.open(self.parent_path)
        first, second, peer, reference, result = [reopened.getObject(name) for name in names]
        self.assertEqual(first.LinkedObject.ObjectId, definition_id)
        self.assertEqual(first.LinkedObject, second.LinkedObject)
        self.assertEqual(Model.children(first.LinkedObject)[0].LinkedObject, peer.LinkedObject)
        self.assertEqual(reference.ObjectId, reference_id)
        self.assertAlmostEqual(result.Shape.Volume, 24)
        self.panel = Navigator.show(reopened)
        self.panel.tabs.setCurrentWidget(self.panel.structure)
        self.panel.setFloating(True)
        self.panel.resize(850, 650)
        Gui.updateGui()
        self.panel.grab().save(str(self.output / "external-shared-components.png"))

    def testPreflightLeavesNoFileOrDocument(self):
        documents = set(App.listDocuments())
        count = len(self.doc.Objects)
        self.doc.openTransaction("Unfinished edit")
        self.part.Label = "Unfinished bracket edit"
        try:
            with self.assertRaisesRegex(ValueError, "Finish"):
                Model.externalize(self.part, self.destination)
            with patch.object(QtWidgets.QFileDialog, "getSaveFileName") as picker:
                with self.assertRaisesRegex(ValueError, "Finish"):
                    self.panel.externalize_component(Navigator.object_key(self.first))
                picker.assert_not_called()
        finally:
            self.doc.abortTransaction()
        self.assertFalse(self.destination.exists())
        self.assertEqual(set(App.listDocuments()), documents)
        self.assertEqual(len(self.doc.Objects), count)
        original = self.parent_path.read_bytes()
        with self.assertRaisesRegex(ValueError, "never overwrites"):
            Model.externalize(self.part, self.parent_path)
        self.assertEqual(self.parent_path.read_bytes(), original)
        with patch.object(QtWidgets.QFileDialog, "getSaveFileName", return_value=("", "")):
            self.panel.externalize_component(Navigator.object_key(self.first))
        self.assertEqual(set(App.listDocuments()), documents)
        self.assertEqual(self.first.LinkedObject, self.part)
        self.panel.open_component_tab(Navigator.object_key(self.child))
        with patch.object(QtWidgets.QFileDialog, "getSaveFileName") as picker:
            with self.assertRaisesRegex(ValueError, "Close isolated tabs"):
                self.panel.externalize_component(Navigator.object_key(self.first))
            picker.assert_not_called()
        self.assertFalse(self.destination.exists())

    def testMenuAndEditingContext(self):
        self.panel.refresh()
        row = self.panel.structure.topLevelItem(0).child(0)
        self.panel.activate_item(row)
        root_key, path = self.panel.root_key, list(self.panel.active_path)
        window = self.panel.mdi.activeSubWindow()
        with patch.object(QtWidgets.QFileDialog, "getSaveFileName", return_value=(str(self.destination), "")):
            self.panel.externalize_component(Navigator.object_key(self.first))
        moved = self.first.LinkedObject
        self.assertEqual(App.ActiveDocument, self.doc)
        self.assertEqual(self.panel.mdi.activeSubWindow(), window)
        self.assertEqual(self.panel.root_key, root_key)
        self.assertEqual(self.panel.active_path, path)
        self.assertEqual(Navigator.resolve(self.panel.active_key), moved)
        self.assertEqual(Gui.getDocument(self.doc.Name).activeView().getActiveObject("part"), moved)
        row = self.panel.structure.topLevelItem(0).child(0)
        menu = self.panel.build_menu(self.panel.structure, row)
        action = next(a for a in menu.actions() if a.text() == "Save to External File")
        self.assertFalse(action.isEnabled())
        with patch.object(QtWidgets.QFileDialog, "getSaveFileName") as picker:
            with self.assertRaisesRegex(ValueError, "embedded"):
                self.panel.externalize_component(Navigator.object_key(self.first))
            picker.assert_not_called()
        self.panel.setFloating(True)
        self.panel.resize(850, 650)
        Gui.updateGui()
        self.panel.grab().save(str(self.output / "external-active-history.png"))
