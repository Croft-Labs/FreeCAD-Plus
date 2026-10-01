# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three feedback workflows for shared-component display across open windows."""
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
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as Navigator


class TestComponentDisplayContext(unittest.TestCase):
    def setUp(self):
        self.warnings = []
        warning = patch.object(QtWidgets.QMessageBox, "warning",
                               side_effect=lambda *args: self.warnings.append(args[2]))
        warning.start()
        self.addCleanup(warning.stop)
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        self.assertEqual(hashlib.sha256(Path(Navigator.__file__).read_bytes()).digest(),
                         hashlib.sha256((source / "src/Gui/ComponentNavigator.py").read_bytes()).digest())
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / self._testMethodName
        self.output.mkdir()
        self.external = Model.new_document("Support")
        self.part = Model.metadata(self.external).RootComponent
        self.body = self.geometry(self.part, "SupportBody", Part.makeBox(2, 3, 4), True)
        self.curve = self.geometry(self.part, "Guide", Part.makeLine(App.Vector(0, 0, 6), App.Vector(5, 0, 6)))
        self.child = Model.add_component(self.part, label="Pin")
        self.pin = self.child.LinkedObject
        self.pin_body = self.geometry(self.pin, "PinBody", Part.makeBox(2, 2, 8), True)
        self.child.LinkPlacement = App.Placement(App.Vector(15, 0, 0), App.Rotation())
        self.external.recompute()
        self.external.saveAs(str(self.output / "Support.cadprt"))
        self.doc = Model.new_document("Assembly")
        self.root = Model.metadata(self.doc).RootComponent
        self.doc.saveAs(str(self.output / "Assembly.cadprt"))
        self.first = Model.add_component(self.root, self.part)
        self.second = Model.add_component(self.root, self.part,
            placement=App.Placement(App.Vector(30, 0, 0), App.Rotation()))
        self.doc.save()
        self.panel = Navigator.show(self.doc)
        self.window = self.panel.mdi.activeSubWindow()
        self.panel.refresh()

    def geometry(self, component, name, shape, result=False):
        with Model.transaction(component.Document, "Create geometry"):
            obj = component.Document.addObject("Part::Feature", name)
            Model.register_object(component, obj, "Object", result)
            obj.Shape = shape
        return obj

    def tearDown(self):
        for doc in reversed(list(App.listDocuments().values())):
            App.closeDocument(doc.Name)
        Gui.updateGui()
        self.assertEqual(self.warnings, [], "Unexpected component warning")

    def paths(self, link):
        return set(link.ViewObject.LinkView.SubNames)

    def menu(self, row):
        menu = self.panel.build_menu(self.panel.structure, row)
        view = next(sub for sub in menu.component_submenus if sub.title() == "Part View")
        return menu, {action.text(): action for action in view.actions()}

    def testBackgroundAssemblyAndIsolatedInheritance(self):
        pin_path = self.child.Name + "." + self.pin_body.Name + "."
        full = {self.body.Name + ".", pin_path}
        self.assertEqual(self.paths(self.first), full)
        self.assertEqual(self.paths(self.second), full)
        Model.set_representation(self.root, [self.second.ObjectId, self.child.ObjectId], "Full Component")
        view = self.panel.open_component_tab(Navigator.object_key(self.part))
        isolated = self.panel.mdi.activeSubWindow()
        self.panel.refresh()
        child_row = self.panel.structure.topLevelItem(0).child(0)
        source_visibility = (self.body.Visibility, self.pin_body.Visibility, self.child.Visibility)
        volume = self.first.Shape.Volume
        self.panel.set_part_view(child_row, "Hidden")
        self.panel.refresh()
        # Parent is inactive: inherited child hiding updates its native LinkView,
        # while the second occurrence's outer override remains visible.
        self.assertEqual(self.paths(self.first), {self.body.Name + "."})
        self.assertEqual(self.paths(self.second), full)
        snapshot = next(entry["snapshot"] for entry in self.panel.component_views if entry["view"] == view)
        self.assertEqual(set(snapshot.SubNames), {self.body.Name + ".", self.curve.Name + "."})
        self.assertEqual((self.body.Visibility, self.pin_body.Visibility, self.child.Visibility), source_visibility)
        self.assertAlmostEqual(self.first.Shape.Volume, volume)
        self.assertTrue(self.first.IncludeInBOM and self.first.IncludeInMass)
        self.external.undo()
        self.panel.refresh()
        self.assertEqual(self.paths(self.first), full)
        self.external.redo()
        self.panel.refresh()
        self.assertEqual(self.paths(self.first), {self.body.Name + "."})
        self.panel.mdi.setActiveSubWindow(self.window)
        Gui.updateGui()
        self.panel.refresh()
        self.assertEqual(self.paths(self.first), {self.body.Name + "."})
        self.panel.mdi.setActiveSubWindow(isolated)
        Gui.updateGui()
        self.panel.refresh()
        self.assertEqual(self.paths(self.second), full)
        self.external.save()
        self.doc.save()
        view.viewAxonometric()
        view.fitAll()
        view.saveImage(str(self.output / "isolated-display.png"), 800, 600, "Current")

    def testPartViewMenusAndActiveOccurrence(self):
        group = self.panel.structure.topLevelItem(0).child(0)
        menu, actions = self.menu(group)
        self.assertTrue(actions["Bodies Only"].isChecked())
        self.assertFalse(actions["Reset to Inherited"].isEnabled())
        self.panel.toggle_instances(group)
        self.panel.refresh()
        group = self.panel.structure.topLevelItem(0).child(0)
        self.panel.activate_item(group.child(1))
        self.panel.refresh()
        group = self.panel.structure.topLevelItem(0).child(0)
        self.assertTrue(group.font(0).bold())
        self.assertFalse(group.child(0).font(0).bold())
        self.assertTrue(group.child(1).font(0).bold())
        menu, actions = self.menu(group.child(1))
        self.assertFalse(actions["Hidden"].isEnabled())
        self.panel.set_part_view(group.child(0), "Full Component")
        self.panel.refresh()
        group = self.panel.structure.topLevelItem(0).child(0)
        self.assertEqual(group.text(3), "Mixed")
        self.assertIn("Mixed inherited", group.toolTip(3))
        menu, actions = self.menu(group)
        self.assertFalse(any(actions[mode].isChecked() for mode in Model.TYPES))
        menu, actions = self.menu(group.child(0))
        self.assertTrue(actions["Full Component"].isChecked())
        self.assertTrue(actions["Reset to Inherited"].isEnabled())
        self.assertIn(self.curve.Name + ".", self.paths(self.first))
        self.assertNotIn(self.curve.Name + ".", self.paths(self.second))
        actions["Reset to Inherited"].trigger()
        self.assertNotIn(self.curve.Name + ".", self.paths(self.first))
        self.panel.tabs.setCurrentWidget(self.panel.structure)
        self.panel.setFloating(True)
        self.panel.resize(850, 620)
        Gui.updateGui()
        self.panel.grab().save(str(self.output / "active-occurrence.png"))

    def testUnavailableHistoryAndReopenedRepresentations(self):
        reference = Model.add_reference(self.part, self.child, self.pin_body)
        Model.set_representation(self.root, [self.first.ObjectId], "Full Component")
        self.panel.open_component_tab(Navigator.object_key(self.part))
        self.panel.refresh()
        self.assertIn(reference.Name + ".", self.paths(self.first))
        # A pending reference can retain its last native shape, but that snapshot
        # must not be exposed as current geometry by Full Component or the eye.
        reference.ResultStatus = "Pending"
        self.assertFalse(reference.Shape.isNull())
        self.panel.refresh()
        self.assertNotIn(reference.Name + ".", self.paths(self.first))
        row = next(self.panel.history.topLevelItem(i) for i in range(self.panel.history.topLevelItemCount())
                   if self.panel.history.topLevelItem(i).data(0, QtCore.Qt.UserRole) == Navigator.object_key(reference))
        self.assertEqual(row.toolTip(1), "Geometry is unavailable. Restore or repair the item and its inputs.")
        before = reference.Visibility
        self.panel.toggle_item_view(row)
        self.assertEqual(reference.Visibility, before)
        Model.activate(self.part)
        self.panel.refresh()
        self.assertIn(reference.Name + ".", self.paths(self.first))
        Model.set_representation(self.root, [self.second.ObjectId], "Hidden")
        self.panel.refresh()
        self.assertIsNone(self.second.ViewObject.LinkView.LinkedView)
        ids = self.first.ObjectId, self.second.ObjectId
        body_name, curve_name = self.body.Name + ".", self.curve.Name + "."
        self.external.save()
        self.doc.save()
        for doc in reversed(list(App.listDocuments().values())):
            App.closeDocument(doc.Name)
        self.doc = CadDocument.open(self.output / "Assembly.cadprt")
        self.root = Model.metadata(self.doc).RootComponent
        self.panel = Navigator.show(self.doc)
        self.panel.refresh()
        links = {link.ObjectId: link for link in Model.children(self.root)}
        self.assertTrue({body_name, curve_name}.issubset(self.paths(links[ids[0]])))
        self.assertIsNone(links[ids[1]].ViewObject.LinkView.LinkedView)
        self.assertEqual(Model.representation(self.root, [ids[0]]), "Full Component")
        self.assertEqual(Model.representation(self.root, [ids[1]]), "Hidden")
