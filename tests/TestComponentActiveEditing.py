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
        self.panel = Navigator.show(self.doc)
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
