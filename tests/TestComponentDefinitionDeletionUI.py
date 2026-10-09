# SPDX-License-Identifier: LGPL-2.1-or-later
"""Models/native deletion releases editing views and preserves the file."""
import importlib
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets, QtGui
import ComponentModel as Model
Navigator = importlib.import_module('freecad.gui.ComponentNavigator')


class TestComponentDefinitionDeletionUI(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_file_document()
        self.root = Model.metadata(self.doc).RootComponent
        self.part = Model.children(self.root)[0].LinkedObject
        self.name = self.part.Name
        self.panel = Navigator.show(self.doc)
        Gui.updateGui()
        Model.remove_instances(Model.children(self.root))
        self.panel.refresh()

    def tearDown(self):
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()): App.closeDocument(name)
        QtWidgets.QApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)

    def row(self):
        return self.panel.models.topLevelItem(0)

    def testModelsDeleteUnusedEditRestoresFileAndUndo(self):
        self.panel.edit_model(self.row())
        self.assertIsNotNone(self.panel.unused_edit())
        self.panel.delete_model(Navigator.object_key(self.part))
        self.assertIsNone(self.doc.getObject(self.name))
        self.assertIsNone(self.panel.unused_edit())
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))
        self.assertEqual(self.panel.models.topLevelItemCount(), 0)
        self.assertEqual(self.panel.structure.topLevelItemCount(), 1)
        self.doc.undo(); Gui.updateGui(); self.panel.refresh()
        self.assertEqual(self.panel.models.topLevelItemCount(), 1)
        self.doc.redo(); Gui.updateGui(); self.panel.refresh()
        self.assertEqual(self.panel.models.topLevelItemCount(), 0)

    def testIsolatedTabClosesAndFileRemains(self):
        self.panel.open_component_tab(Navigator.object_key(self.part))
        Gui.updateGui()
        self.assertEqual(len(self.panel.component_views), 1)
        self.panel.delete_model(Navigator.object_key(self.part))
        Gui.updateGui()
        self.assertEqual(self.panel.component_views, [])
        self.assertIsNotNone(App.getDocument(self.doc.Name))
        self.assertEqual(self.panel.root_key, Navigator.object_key(self.root))
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))

    def testNativeDeleteAndFileProtection(self):
        Gui.Selection.addSelection(self.part)
        Gui.runCommand('Std_Delete', 0)
        Gui.updateGui(); self.panel.refresh()
        self.assertIsNone(self.doc.getObject(self.name))
        Gui.Selection.addSelection(self.root)
        Gui.runCommand('Std_Delete', 0)
        self.assertEqual(Model.metadata(self.doc).RootComponent, self.root)

    def testModelsKeyboardAndMenu(self):
        row = self.row(); row.setSelected(True)
        menu = self.panel.build_menu(self.panel.models, row)
        self.assertIn('Delete component', [action.text() for action in menu.actions()])
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Delete, QtCore.Qt.NoModifier)
        self.panel.eventFilter(self.panel.models, event)
        self.assertIsNone(self.doc.getObject(self.name))

    def testRefusalKeepsEditedViewAndNativeSelectionConsumed(self):
        Model.add_component(self.root, self.part)
        self.panel.refresh(); self.panel.edit_model(self.row())
        active = self.panel.active_key
        with self.assertRaises(ValueError): self.panel.delete_model(Navigator.object_key(self.part))
        self.assertEqual(self.panel.active_key, active)
        Gui.Selection.clearSelection(); Gui.Selection.addSelection(self.part)
        with patch.object(QtWidgets.QMessageBox, 'warning') as warning:
            Navigator.delete_selected_instances()
        warning.assert_called_once()
        self.assertEqual(Gui.Selection.getSelection(), [])
        self.assertIsNotNone(self.doc.getObject(self.name))

    def testLastIsolatedTabCreatesFileViewBeforeDeletion(self):
        file_window = self.panel.mdi.activeSubWindow()
        self.panel.open_component_tab(Navigator.object_key(self.part))
        Gui.updateGui()
        file_window.close()
        Gui.updateGui()
        self.panel.delete_model(Navigator.object_key(self.part))
        Gui.updateGui()
        self.assertIsNone(self.doc.getObject(self.name))
        self.assertEqual(self.panel.root_key, Navigator.object_key(self.root))
        self.assertTrue(self.panel.mdi.subWindowList())
