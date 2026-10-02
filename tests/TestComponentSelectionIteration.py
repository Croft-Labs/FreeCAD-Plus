# SPDX-License-Identifier: LGPL-2.1-or-later
"""Bounded native selection, reference and view-context feedback checks."""
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
import CadDocument
import ComponentModel as Model
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentSelection as Selection


class TestComponentSelectionIteration(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, relative in [(Model, "src/Mod/Part/ComponentModel.py"),
                                 (Navigator, "src/Gui/ComponentNavigator.py"),
                                 (Selection, "src/Gui/ComponentSelection.py")]:
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((source / relative).read_bytes()).digest())
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        self.doc = Model.new_document("Selection feedback")
        self.root = Model.metadata(self.doc).RootComponent
        self.first = Model.add_component(self.root, label="Support")
        self.part = self.first.LinkedObject
        self.second = Model.add_component(self.root, self.part,
            placement=App.Placement(App.Vector(40, 0, 0), App.Rotation()))
        self.body = self.box(self.part, "SupportBody")
        self.child = Model.add_component(self.part, label="Pin")
        self.pin = self.box(self.child.LinkedObject, "PinBody")
        self.panel = Navigator.show(self.doc)
        self.panel.tabs.setCurrentWidget(self.panel.structure)
        Gui.Selection.clearSelection()
        Gui.updateGui()

    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def box(self, component, name):
        obj = self.doc.addObject("Part::Feature", name)
        Model.register_object(component, obj, "Object", True)
        obj.Shape = Part.makeBox(10, 8, 6)
        self.doc.recompute()
        return obj

    def pick(self, ids, item=None, element=""):
        Gui.Selection.clearSelection()
        path = Selection.native_path(self.root, ids, item)
        Gui.Selection.addSelection(self.doc.Name, self.root.Name, path + element)
        self.panel.sync_selection()
        return Gui.Selection.getSelectionEx("*", 0)

    def selected_row(self):
        rows = self.panel.structure.selectedItems()
        self.assertEqual(len(rows), 1)
        return rows[0]

    def testNestedSelectionRoundTripAndHistory(self):
        ids = [self.second.ObjectId, self.child.ObjectId]
        entries = self.pick(ids, self.pin, "Face1")
        picks = Selection.selected(self.root, entries)
        self.assertEqual(len(picks), 1)
        self.assertEqual(picks[0].ids, tuple(ids))
        self.assertEqual(picks[0].item, self.pin)
        self.assertEqual(picks[0].element, "Face1")
        row = self.selected_row()
        self.assertEqual(row.text(0), "Pin")
        self.assertEqual(list(row.data(0, QtCore.Qt.UserRole)[1]), ids)
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))
        self.panel.select_structure()
        selected = Gui.Selection.getSelectionEx("*", 0)
        self.assertEqual(list(selected[0].SubElementNames), [Selection.native_path(self.root, ids)])
        self.panel.activate_item(row)
        self.panel.refresh()
        item = self.panel.history.topLevelItem(1)
        item.setSelected(True)
        selected = Gui.Selection.getSelectionEx("*", 0)
        self.assertEqual(list(selected[0].SubElementNames), [Selection.native_path(self.root, ids, self.pin)])
        self.pick(ids, self.pin, "Edge1")
        self.assertEqual(self.panel.history.selectedItems()[0].text(2), self.pin.Label)
        self.assertEqual(self.panel.active_path, ids)
        self.panel.tabs.setCurrentWidget(self.panel.structure)
        Gui.updateGui()
        self.panel.grab().save(str(self.output / "component-nested-selection.png"))
        Gui.Selection.clearSelection()
        self.panel.sync_selection()
        self.assertFalse(self.panel.structure.selectedItems())
        self.assertFalse(self.panel.history.selectedItems())

    def testReferencePreselectionDoesNotGuessSharedOrGrandchild(self):
        # Native addSelection may canonicalize a bare source to a Link path first.
        # Check the mapper's ambiguous-input boundary before that normalization.
        entries = [SimpleNamespace(Object=self.body, SubElementNames=[])]
        self.assertEqual(len(Selection.selected(self.root, entries)), 2)
        self.assertIsNone(Selection.reference_choice(self.root, self.root, entries))
        entries = self.pick([self.second.ObjectId], self.body, "Face1")
        self.assertEqual(Selection.reference_choice(self.root, self.root, entries), (self.second, self.body))
        observed = []
        def choose(parent, title, prompt, labels, index, editable):
            observed.append((prompt, labels[index]))
            return labels[index], True
        with patch.object(QtWidgets.QInputDialog, "getItem", side_effect=choose):
            self.panel.add_reference()
        reference = Model.history(self.root)[-1]
        self.assertEqual(reference.SourceOccurrence, self.second)
        self.assertEqual(reference.SourceObject, self.body)
        self.assertAlmostEqual(reference.Shape.BoundBox.XMin, 40)
        self.assertIn("whole evaluated geometry", observed[0][0])
        entries = self.pick([self.second.ObjectId, self.child.ObjectId], self.pin, "Face1")
        self.assertIsNone(Selection.reference_choice(self.root, self.root, entries))
        count = len(self.doc.Objects)
        with patch.object(QtWidgets.QInputDialog, "getItem", side_effect=choose):
            self.panel.add_reference()
        self.assertEqual(len(self.doc.Objects), count)
        identity, occurrence_id = reference.ObjectId, self.second.ObjectId
        path = self.output / "Component-Selection-Feedback.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(path)
        reference = next(obj for obj in self.doc.Objects if getattr(obj, "ObjectId", "") == identity)
        self.assertEqual(reference.SourceOccurrence.ObjectId, occurrence_id)
        self.assertAlmostEqual(reference.Shape.BoundBox.XMin, 40)

    def testGroupedUndoAndComponentTabContext(self):
        group = self.panel.structure.topLevelItem(0)
        group.setSelected(True)
        selected = Gui.Selection.getSelectionEx("*", 0)
        self.assertEqual(set(selected[0].SubElementNames),
                         {self.first.Name + ".", self.second.Name + "."})
        self.panel.set_part_view(group, "Full Component")
        self.assertTrue(all(Model.representation(self.root, [link.ObjectId]) == "Full Component"
                            for link in (self.first, self.second)))
        self.doc.undo()
        self.assertTrue(all(Model.representation(self.root, [link.ObjectId]) == "Bodies Only"
                            for link in (self.first, self.second)))
        self.doc.redo()
        self.panel.set_part_view(group, "Hidden")
        hidden = self.root.RepresentationOverrides
        self.panel.toggle_component(group)
        self.assertTrue(all(Model.representation(self.root, [link.ObjectId]) == "Bodies Only"
                            for link in (self.first, self.second)))
        self.doc.undo()
        self.assertEqual(json.loads(self.root.RepresentationOverrides), json.loads(hidden))
        self.doc.redo()
        self.pick([self.second.ObjectId])
        self.panel.activate_item(self.selected_row())
        self.panel.refresh()
        original_window = self.panel.mdi.activeSubWindow()
        view = self.panel.open_component_tab(Navigator.object_key(self.child))
        self.panel.refresh()
        isolated_window = self.panel.mdi.activeSubWindow()
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.child.LinkedObject))
        count = len(self.panel.mdi.subWindowList())
        self.assertEqual(self.panel.open_component_tab(Navigator.object_key(self.child)), view)
        self.assertEqual(len(self.panel.mdi.subWindowList()), count)
        self.panel.mdi.setActiveSubWindow(original_window)
        Gui.updateGui()
        self.assertEqual(self.panel.root_key, Navigator.object_key(self.root))
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.part))
        self.assertEqual(self.panel.active_path, [self.second.ObjectId])
        self.assertEqual(Gui.activeDocument().activeView().getActiveObject("part"), self.part)
        self.panel.mdi.setActiveSubWindow(isolated_window)
        Gui.updateGui()
        self.assertEqual(self.panel.root_key, Navigator.object_key(self.child.LinkedObject))
        self.assertEqual(Gui.activeDocument().activeView().getActiveObject("part"), self.child.LinkedObject)
        self.panel.grab().save(str(self.output / "component-restored-tab.png"))
