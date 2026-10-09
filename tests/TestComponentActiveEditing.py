# SPDX-License-Identifier: LGPL-2.1-or-later
"""Edit stays in the current view and resolves shared occurrences deterministically."""
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import ComponentModel as Model
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as Navigator


class TestComponentActiveEditing(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_document("Active editing")
        self.root = Model.metadata(self.doc).RootComponent
        self.first = Model.add_component(self.root, label="Bracket")
        self.part = self.first.LinkedObject
        self.second = Model.add_component(self.root, self.part)
        Gui.updateGui()
        self.panel = Navigator.show(self.doc)
        Gui.updateGui()
        self.panel.refresh()
        self.window = self.panel.mdi.activeSubWindow()
        self.windows = len(self.panel.mdi.subWindowList())

    def tearDown(self):
        Gui.Selection.clearSelection()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def row(self, definition):
        iterator = QtWidgets.QTreeWidgetItemIterator(self.panel.models)
        while iterator.value():
            row = iterator.value()
            if row.data(0, QtCore.Qt.UserRole) == Navigator.object_key(definition):
                return row
            iterator += 1
        self.fail("Definition missing from Models")

    def testModelsEditReusesCurrentTabAndLastOccurrence(self):
        self.panel.edit_model(self.row(self.part))
        self.assertEqual(self.panel.active_path, [self.first.ObjectId])
        self.panel.refresh()
        group = self.panel.structure.topLevelItem(0).child(0)
        self.panel.toggle_instances(group)
        self.panel.refresh()
        group = self.panel.structure.topLevelItem(0).child(0)
        self.panel.activate_item(group.child(1))
        self.panel.edit_model(self.row(self.root))
        self.panel.edit_model(self.row(self.part))
        self.assertEqual(self.panel.active_path, [self.second.ObjectId])
        self.assertEqual(self.panel.mdi.activeSubWindow(), self.window)
        self.assertEqual(len(self.panel.mdi.subWindowList()), self.windows)
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.part))
        self.assertEqual(self.panel.tabs.currentWidget(), self.panel.history)

    def testDeletedRememberedOccurrenceFallsBack(self):
        self.window.setProperty("ComponentEditPaths", {self.part.ObjectId: [self.second.ObjectId]})
        Model.remove_instances([self.second])
        self.panel.refresh()
        self.panel.edit_model(self.row(self.part))
        self.assertEqual(self.panel.active_path, [self.first.ObjectId])

    def testAllOccurrencesUseActivePreferenceAndSelectionDoesNotEdit(self):
        prefs = App.ParamGet("User parameter:BaseApp/Preferences/TreeView")
        previous = prefs.GetUnsigned("TreeActiveColor", 1538528255)
        prefs.SetUnsigned("TreeActiveColor", 0x28B45AFF)
        try:
            self.panel.edit_model(self.row(self.part))
            self.panel.refresh()
            self.panel.toggle_instances(self.panel.structure.topLevelItem(0).child(0))
            self.panel.refresh()
            group = self.panel.structure.topLevelItem(0).child(0)
            for row in [self.row(self.part), group, group.child(0), group.child(1)]:
                self.assertTrue(row.font(0).bold())
                self.assertEqual(row.background(0).color().name(), "#28b45a")
            self.row(self.root).setSelected(True)
            self.panel.select_models()
            self.assertEqual(self.panel.active_key, Navigator.object_key(self.part))
            self.assertEqual(self.panel.active_path, [self.first.ObjectId])
        finally:
            prefs.SetUnsigned("TreeActiveColor", previous)

    def testExplicitOpenAvailableInBothMenus(self):
        for tree in (self.panel.models, self.panel.structure):
            row = (self.row(self.part) if tree == self.panel.models else
                   self.panel.structure.topLevelItem(0).child(0))
            menu = self.panel.build_menu(tree, row)
            action = next(a for a in menu.actions() if a.text() == "Open in new window")
            with patch.object(self.panel, "open_component_tab") as opened:
                action.trigger()
                opened.assert_called_once()

    def testNestedOccurrenceFoundWithoutExpandedTree(self):
        nested = Model.add_component(self.part, label="Nested")
        self.panel.refresh()
        self.panel.edit_model(self.row(nested.LinkedObject))
        self.assertEqual(self.panel.active_path, [self.first.ObjectId, nested.ObjectId])
        self.assertEqual(len(self.panel.mdi.subWindowList()), self.windows)


    def testUnusedModelStaysInTabWithoutSavedVisibilityChanges(self):
        before = {obj.Name: obj.Visibility for obj in self.doc.Objects if hasattr(obj, "Visibility")}
        unused = Model.create_definition(self.doc, "Unused")
        count = len(Model.children(self.root))
        self.panel.refresh()
        self.panel.edit_model(self.row(unused))
        self.panel.refresh()
        self.assertEqual(self.panel.mdi.activeSubWindow(), self.window)
        self.assertEqual(len(self.panel.mdi.subWindowList()), self.windows)
        self.assertEqual(self.panel.active_key, Navigator.object_key(unused))
        self.assertEqual(len(Model.children(self.root)), count)
        self.assertEqual(self.panel.structure.topLevelItemCount(), 2)
        temporary = self.panel.structure.topLevelItem(1)
        self.assertEqual(temporary.text(0), "Unused (unused model)")
        self.assertFalse(temporary.flags() & QtCore.Qt.ItemIsDragEnabled)
        self.assertFalse(temporary.flags() & QtCore.Qt.ItemIsDropEnabled)
        regular = self.panel.structure.topLevelItem(0)
        self.assertTrue(self.panel.temporarily_hidden(regular))
        self.assertEqual(regular.foreground(0).color().name(), "#808080")
        self.assertEqual(regular.child(0).foreground(0).color().name(), "#808080")
        self.panel.toggle_component(regular)
        with self.assertRaises(ValueError):
            self.panel.set_part_view(regular.child(0), "Hidden")
        for name, visible in before.items():
            self.assertEqual(self.doc.getObject(name).Visibility, visible, name)
        self.panel.activate_item(regular)
        self.panel.refresh()
        self.assertIsNone(self.panel.unused_edit())
        self.assertEqual(self.panel.structure.topLevelItemCount(), 1)
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))

    def testUnusedDefinitionEditAndSaveDoesNotInsertOccurrence(self):
        import os
        from pathlib import Path
        import Part
        unused = Model.create_definition(self.doc, "Unused")
        self.panel.refresh()
        self.panel.edit_model(self.row(unused))
        body = self.doc.addObject("Part::Feature", "UnusedBody")
        Model.register_object(unused, body, "Object", True)
        body.Shape = Part.makeBox(2, 3, 4)
        self.doc.recompute()
        self.panel.refresh()
        filename = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "UnusedEditing.cadprt"
        self.doc.saveAs(str(filename))
        self.assertEqual(len(Model.children(self.root)), 2)
        self.assertAlmostEqual(body.Shape.Volume, 24)
        self.panel.edit_model(self.row(self.part))
        self.panel.refresh()
        self.assertIsNone(self.panel.unused_edit())
        self.assertEqual(self.panel.active_path, [self.first.ObjectId])
        self.assertTrue(all("unused model" not in self.panel.structure.topLevelItem(i).text(0)
                            for i in range(self.panel.structure.topLevelItemCount())))
        import CadDocument
        App.closeDocument(self.doc.Name)
        reopened = CadDocument.open(str(filename))
        root = Model.metadata(reopened).RootComponent
        self.assertTrue(Model.is_file_container(root))
        self.assertEqual(len(Model.children(root)), 1)
        original = Model.children(root)[0].LinkedObject
        self.assertEqual(len(Model.children(original)), 2)
        retained = next(obj for obj in Model.definitions(reopened) if obj.Label == "Unused")
        self.assertEqual(Model.instance_counts(root).get(retained, 0), 0)
        self.assertAlmostEqual(reopened.getObject("UnusedBody").Shape.Volume, 24)

    def testUnusedChildEditKeepsTemporaryView(self):
        unused = Model.create_definition(self.doc, "Unused")
        child = Model.add_component(unused, label="Child")
        self.panel.refresh()
        self.panel.edit_model(self.row(unused))
        self.panel.refresh()
        self.panel.activate_item(self.panel.structure.topLevelItem(1).child(0))
        self.panel.refresh()
        self.assertIsNotNone(self.panel.unused_edit())
        self.assertEqual(self.panel.active_key, Navigator.object_key(child.LinkedObject))
        self.assertEqual(self.panel.active_path, [child.ObjectId])
        self.assertEqual(len(self.panel.mdi.subWindowList()), self.windows)


    def testExternalUnusedModelUsesCurrentViewAndRestoresOnSourceClose(self):
        import os
        from pathlib import Path
        from freecad.gui.ComponentExtrudeTask import active_component
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        external = Model.new_document("Hardware")
        unused = Model.metadata(external).RootComponent
        external.saveAs(str(output / "Hardware.cadprt"))
        self.doc.saveAs(str(output / "AssemblyExternal.cadprt"))
        Model.import_file(self.doc, external)
        App.setActiveDocument(self.doc.Name)
        Gui.updateGui()
        self.panel.set_document(self.doc)
        window = self.panel.mdi.activeSubWindow()
        count = len(self.panel.mdi.subWindowList())
        self.panel.edit_model(self.row(unused))
        self.panel.refresh()
        self.assertEqual(self.panel.mdi.activeSubWindow(), window)
        self.assertEqual(len(self.panel.mdi.subWindowList()), count)
        self.assertEqual(active_component(), unused)
        context = Navigator.TaskContext(unused)
        context.enter()
        context.restore()
        self.assertEqual(self.panel.mdi.activeSubWindow(), window)
        self.assertEqual(active_component(), unused)
        self.assertIn("Hardware", self.panel.structure.topLevelItem(1).text(0))
        self.assertEqual(len(Model.children(self.root)), 2)
        App.closeDocument(external.Name)
        Gui.updateGui()
        self.panel.refresh()
        self.assertIsNone(self.panel.unused_edit())
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))
