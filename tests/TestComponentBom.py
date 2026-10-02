# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three focused component BOM ownership, participation and persistence workflows."""
import hashlib
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
import AssemblyGui
import CommandCreateBom as Editor
import ComponentModel as Model
import CadDocument
from PySide import QtWidgets
from freecad.gui import ComponentNavigator as Navigator


def rows(bom):
    result = []
    for row in range(2, 30):
        name = bom.getContents("B" + str(row)).lstrip("'")
        if not name:
            break
        result.append((bom.getContents("A" + str(row)).lstrip("'"), name,
                       int(bom.getContents("C" + str(row)).lstrip("'"))))
    return result


class TestComponentBom(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, relative in ((Navigator, "src/Gui/ComponentNavigator.py"),
                                 (Model, "src/Mod/Part/ComponentModel.py"),
                                 (Editor, "src/Mod/Assembly/CommandCreateBom.py")):
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((source / relative).read_bytes()).digest())
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / self._testMethodName
        self.output.mkdir()
        self.task = None
        self.external = Model.new_document("Support")
        self.part = Model.metadata(self.external).RootComponent
        self.body(self.part)
        self.pin_link = Model.add_component(self.part, label="Pin")
        self.pin = self.pin_link.LinkedObject
        self.body(self.pin)
        self.external.saveAs(str(self.output / "Support.cadprt"))
        self.doc = Model.new_document("Assembly")
        self.root = Model.metadata(self.doc).RootComponent
        self.body(self.root)
        self.doc.saveAs(str(self.output / "Assembly.cadprt"))
        self.first = Model.add_component(self.root, self.part)
        self.second = Model.add_component(self.root, self.part)
        self.direct_pin = Model.add_component(self.root, self.pin)
        self.panel = Navigator.show(self.doc)
        self.window = self.panel.mdi.activeSubWindow()
        self.panel.refresh()

    def body(self, component):
        with Model.transaction(component.Document, "Create geometry"):
            obj = component.Document.addObject("Part::Feature", "BodyGeometry")
            Model.register_object(component, obj, "Object", True)
            obj.Shape = Part.makeBox(2, 3, 4)
        return obj

    def bom(self, component):
        with Model.transaction(component.Document, "Create BOM"):
            bom = component.Document.addObject("Assembly::BomObject", "ComponentBOM")
            Model.register_object(component, bom, "Object")
            bom.columnsNames = ["Index", "Name", "Quantity"]
            bom.onlyParts = False
            bom.detailParts = True
        bom.recompute()
        return bom

    def tearDown(self):
        if self.task:
            self.task.reject()
        for doc in reversed(list(App.listDocuments().values())):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def testComponentCountsAndIndependentParticipation(self):
        bom = self.bom(self.root)
        expected = [("1", "Support", 2), ("1.1", "Pin", 1), ("2", "Pin", 1)]
        self.assertEqual(rows(bom), expected)
        Model.set_representation(self.root, [self.first.ObjectId], "Hidden")
        self.first.Visibility = False
        self.first.IncludeInMass = False
        bom.recompute()
        self.assertEqual(rows(bom), expected)
        self.panel.refresh()
        group = self.panel.structure.topLevelItem(0)
        menu = self.panel.build_menu(self.panel.structure, group)
        participation = next(sub for sub in menu.component_submenus if sub.title() == "Bill of Materials")
        next(action for action in participation.actions() if action.text() == "Exclude").trigger()
        bom.recompute()
        self.assertEqual(rows(bom), [("1", "Pin", 1)])
        self.assertFalse(self.first.IncludeInMass)
        self.assertFalse(self.first.Visibility)
        self.assertEqual(Model.representation(self.root, [self.first.ObjectId]), "Hidden")
        self.doc.undo()
        bom.recompute()
        self.assertEqual(rows(bom), expected)
        self.doc.redo()
        bom.recompute()
        self.assertEqual(rows(bom), [("1", "Pin", 1)])
        Model.set_bom_inclusion([self.first, self.second], True)
        # A stored child policy applies to each use of that definition.
        Model.set_bom_inclusion([self.pin_link], False)
        bom.recompute()
        self.assertEqual(rows(bom), [("1", "Support", 2), ("2", "Pin", 1)])
        # Ordinary native Part containers keep the inherited geometry BOM behavior.
        ordinary = App.newDocument("OrdinaryBom")
        part = ordinary.addObject("App::Part", "OrdinaryPart")
        part.newObject("Part::Box", "OrdinaryBox")
        legacy = ordinary.addObject("Assembly::BomObject", "LegacyBOM")
        legacy.columnsNames = ["Index", "Name", "Quantity"]
        legacy.detailParts = True
        ordinary.recompute()
        self.assertEqual(rows(legacy), [("1", "OrdinaryPart", 1), ("1.1", "OrdinaryBox", 1)])

    def testExternalTaskOwnershipCancelAndHistoryEdit(self):
        group = self.panel.structure.topLevelItem(0)
        self.panel.toggle_instances(group)
        self.panel.refresh()
        self.panel.activate_item(self.panel.structure.topLevelItem(0).child(1))
        self.panel.refresh()
        initial = list(self.part.ModelHistory)
        command = Editor.CommandCreateBom()
        command.Activated()
        self.task = command.panel
        self.assertEqual(self.task.doc, self.external)
        self.assertEqual(Model.owner(self.task.bomObj), self.part)
        self.assertEqual(self.task.exclusionScope(), {self.pin_link})
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.external.Name, self.part.Name, self.pin_link.Name + ".")
        self.task.excludeSelection()
        self.assertEqual(list(self.task.bomObj.excludedObjects), [self.pin_link])
        self.task.reject()
        self.task = None
        self.assertEqual(list(self.part.ModelHistory), initial)
        self.assertEqual(self.panel.mdi.activeSubWindow(), self.window)
        self.assertEqual(self.panel.active_path, [self.second.ObjectId])
        command.Activated()
        self.task = command.panel
        bom = self.task.bomObj
        bom.columnsNames = ["Index", "Name", "Quantity"]
        bom.recompute()
        self.assertEqual(rows(bom), [("1", "Pin", 1)])
        self.assertTrue(self.task.accept())
        self.task = None
        self.assertEqual(self.panel.mdi.activeSubWindow(), self.window)
        self.assertEqual(self.panel.active_path, [self.second.ObjectId])
        made = []
        Model.set_bom_inclusion([self.pin_link], False)
        constructor = Editor.TaskAssemblyCreateBom
        def capture(*args, **kwargs):
            panel = constructor(*args, **kwargs)
            made.append(panel)
            return panel
        with patch.object(Editor, "TaskAssemblyCreateBom", side_effect=capture):
            self.panel.edit_history(Navigator.object_key(bom))
        self.task = made[0]
        self.assertEqual(self.task.bomObj, bom)
        self.assertEqual(self.task.component, self.part)
        self.assertEqual(rows(bom), [])
        self.task.form.grab().save(str(self.output / "component-bom-editor.png"))
        self.task.reject()
        self.task = None
        self.assertEqual(self.panel.active_path, [self.second.ObjectId])
        self.external.save()
        self.doc.save()

    def testBOMPolicyReopenAndPerReportExclusions(self):
        bom = self.bom(self.root)
        other = self.bom(self.root)
        bom.excludedObjects = [self.first]
        Model.set_bom_inclusion([self.direct_pin], False)
        bom.recompute()
        other.recompute()
        self.assertEqual(rows(bom), [("1", "Support", 1), ("1.1", "Pin", 1)])
        self.assertEqual(rows(other), [("1", "Support", 2), ("1.1", "Pin", 1)])
        ident, name, other_name = self.direct_pin.ObjectId, bom.Name, other.Name
        self.doc.save()
        for doc in reversed(list(App.listDocuments().values())):
            App.closeDocument(doc.Name)
        self.doc = CadDocument.open(self.output / "Assembly.cadprt")
        self.root = Model.metadata(self.doc).RootComponent
        bom, other = self.doc.getObject(name), self.doc.getObject(other_name)
        bom.recompute()
        other.recompute()
        self.assertEqual(rows(bom), [("1", "Support", 1), ("1.1", "Pin", 1)])
        self.assertEqual(rows(other), [("1", "Support", 2), ("1.1", "Pin", 1)])
        self.assertFalse(next(obj for obj in Model.children(self.root) if obj.ObjectId == ident).IncludeInBOM)
        self.assertIn(bom, Model.history(self.root))
        self.assertEqual(Model.validate(self.doc).RootComponent, self.root)
