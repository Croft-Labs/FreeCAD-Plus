# SPDX-License-Identifier: LGPL-2.1-or-later
"""Part Type controls, independent visibility and owner editing contexts."""
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as Navigator
from TestComponentPartTypes import TestComponentPartTypes as Fixture


class TestComponentPartTypeUI(unittest.TestCase):
    tearDown = Fixture.tearDown
    types = Fixture.types

    def setUp(self):
        Fixture.setUp(self)
        for component in (self.root, self.parent, self.fan.LinkedObject,
                          self.bottom.LinkedObject, self.top.LinkedObject):
            body = self.doc.addObject("Part::Feature", component.Name + "Body")
            Model.register_object(component, body, "Object", True)
            body.Shape = Part.makeBox(2, 3, 4)
            body.Visibility = True
            guide = self.doc.addObject("Part::Feature", component.Name + "Guide")
            Model.register_object(component, guide, "Object", False)
            guide.Shape = Part.makeLine(App.Vector(), App.Vector(1, 0, 6))
            guide.Visibility = True
        self.doc.recompute()
        Gui.updateGui()
        self.panel = Navigator.show(self.doc)
        self.panel.refresh()
        self.top_path = [self.assembly.ObjectId, self.top.ObjectId]

    def row(self, ids):
        iterator = QtWidgets.QTreeWidgetItemIterator(self.panel.structure)
        while iterator.value():
            row = iterator.value()
            value = row.data(0, QtCore.Qt.UserRole)
            if value and list(value[1]) == ids:
                return row
            iterator += 1
        self.fail("Missing occurrence")

    def edit(self, ids):
        self.panel.activate_item(self.row(ids))
        self.panel.refresh()

    def paths(self, active):
        return {path: floor for path, obj, floor in Navigator.context_display_plan(self.root, active)}

    def testMenusAndSavedDirectChildTypes(self):
        self.edit(self.top_path)
        row = self.row(self.top_path + [self.top_bottom.ObjectId])
        menu = self.panel.build_menu(self.panel.structure, row)
        types = next(m for m in menu.component_submenus if m.title() == "Part Type")
        actions = {a.text(): a for a in types.actions()}
        self.assertEqual(set(actions), set(Model.PART_TYPES) | {"Reset to Default"})
        actions["Reference"].trigger()
        self.assertEqual(Model.part_type(self.top.LinkedObject, self.top_bottom), "Reference")
        self.assertEqual(self.panel.structure.headerItem().text(3), "Part Type")
        menu = self.panel.build_menu(self.panel.structure, self.row(self.top_path))
        own = next(m for m in menu.component_submenus if m.title() == "Part Type")
        self.assertFalse(next(a for a in own.actions() if a.text() == "Excluded").isEnabled())

    def testVisibilityCannotChangeExcludedType(self):
        self.edit(self.top_path)
        ids = self.top_path + [self.top_bottom.ObjectId]
        self.panel.set_part_type(self.row(ids), "Excluded")
        self.top_bottom.Visibility = True
        self.panel.refresh()
        with self.assertRaisesRegex(ValueError, "Excluded"):
            self.panel.set_component_visibility(self.row(ids), True)
        self.assertEqual(Model.part_type(self.top.LinkedObject, self.top_bottom), "Excluded")
        self.assertFalse(self.panel.path_visible(self.root, ids))
        self.panel.set_part_type(self.row(ids), "Bodies Only")
        self.panel.set_component_visibility(self.row(ids), False)
        self.assertFalse(self.top_bottom.Visibility)
        self.panel.set_component_visibility(self.row(ids), True)
        self.assertTrue(self.top_bottom.Visibility)
        self.assertEqual(Model.part_type(self.top.LinkedObject, self.top_bottom), "Bodies Only")

    def testOwnerReferenceExampleAndFade(self):
        self.types()
        self.edit(self.top_path)
        reference = self.assembly.Name + "." + self.top.Name + "." + self.top_bottom.Name + "."
        nested = reference + self.bottom_fan.Name + "."
        explicit_fan = self.assembly.Name + "." + self.top.Name + "." + self.top_fan.Name + "."
        plan = self.paths(self.top_path)
        self.assertTrue(any(p.startswith(reference) and p.endswith("Guide.") for p in plan))
        self.assertFalse(any(p.startswith(nested) for p in plan))
        self.assertTrue(any(p.startswith(explicit_fan) for p in plan))
        self.assertTrue(all(f == 0 for p, f in plan.items() if p.startswith(reference)))
        self.assertEqual(plan[self.root.Name + "Body."], .75)
        self.edit([self.assembly.ObjectId])
        self.assertFalse(any(p.startswith(reference) for p in self.paths([self.assembly.ObjectId])))
        self.assertEqual(Model.part_type(self.top.LinkedObject, self.top_bottom), "Reference")
        self.edit(self.top_path)
        self.assertTrue(any(p.startswith(reference) for p in self.paths(self.top_path)))

    def testActiveSelfRestoresWithoutChangingParent(self):
        self.edit(self.top_path)
        self.panel.set_part_type(self.row(self.top_path), "Bodies Only")
        prefix = self.assembly.Name + "." + self.top.Name + "."
        guide = prefix + self.top.LinkedObject.Name + "Guide."
        self.assertNotIn(guide, self.paths(self.top_path))
        self.edit([])
        self.edit(self.top_path)
        self.assertEqual(self.row(self.top_path).text(3), "Bodies Only")
        self.assertNotIn(guide, self.paths(self.top_path))
        self.panel.set_part_type(self.row(self.top_path), None)
        self.assertIn(guide, self.paths(self.top_path))

    def testExcludedAncestorDoesNotBlockEditingOrGetRewritten(self):
        Model.set_part_types(self.root, [(self.assembly, "Excluded")])
        self.edit(self.top_path)
        prefix = self.assembly.Name + "." + self.top.Name + "."
        self.assertTrue(any(p.startswith(prefix) for p in self.paths(self.top_path)))
        self.assertEqual(Model.part_type(self.root, self.assembly), "Excluded")
        self.edit([])
        self.assertFalse(any(p.startswith(self.assembly.Name + ".") for p in self.paths([])))

    def testDeeperTypesRequireEditingTheirOwner(self):
        with self.assertRaisesRegex(ValueError, "owning component"):
            self.panel.set_part_type(self.row(self.top_path), "Excluded")
        self.assertNotIn("PartType", self.top.PropertiesList)

    def testExplicitTypesSupersedeOnlyTheirLegacyPathRules(self):
        path = self.top_path + [self.top_bottom.ObjectId]
        Model.set_representation(self.root, path, "Hidden")
        before = self.root.RepresentationOverrides
        self.assertEqual(Model.effective_part_type(self.root, path), "Excluded")
        Model.set_part_types(self.top.LinkedObject, [(self.top_bottom, "Bodies Only")])
        self.assertEqual(Model.effective_part_type(self.root, path), "Bodies Only")
        self.assertEqual(self.root.RepresentationOverrides, before)
        self.doc.undo()
        self.assertEqual(Model.effective_part_type(self.root, path), "Excluded")

    def testRootBodiesOnlyUsesViewLocalScene(self):
        self.panel.set_part_type(self.row([]), "Bodies Only")
        self.panel.refresh()
        self.assertTrue(self.panel.context_views)
        self.assertFalse(any(p.endswith("Guide.") and "." not in p[:-1] for p in self.paths([])))
        self.panel.set_part_type(self.row([]), None)
        self.panel.refresh()
        self.assertFalse(self.panel.context_views)

    def testCaptureTree(self):
        self.types()
        self.edit(self.top_path)
        self.panel.tabs.setCurrentWidget(self.panel.structure)
        self.panel.setFloating(True)
        self.panel.resize(850, 620)
        self.panel.structure.expandAll()
        Gui.updateGui()
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "part-types-tree.png"
        self.assertTrue(self.panel.grab().save(str(path)))
        self.panel.setFloating(False)
    def testStaleTypeMenuCannotWriteToNewActiveOwner(self):
        row = self.row([self.assembly.ObjectId])
        context = (self.panel.active_key, tuple(self.panel.active_path))
        self.edit([self.assembly.ObjectId])
        with self.assertRaisesRegex(ValueError, "edited component changed"):
            self.panel.set_part_type(self.row([self.assembly.ObjectId]), "Bodies Only", context)
        self.assertNotIn("ActivePartType", self.parent.PropertiesList)
        self.assertNotIn("PartType", self.assembly.PropertiesList)
    def testSaveContextForColdReopen(self):
        self.types()
        self.edit(self.top_path)
        self.panel.set_part_type(self.row(self.top_path), "Bodies Only")
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "part-type-context.cadprt"
        self.doc.saveAs(str(path))
        self.assertEqual(Model.active_part_type(self.top.LinkedObject), "Bodies Only")