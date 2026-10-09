# SPDX-License-Identifier: LGPL-2.1-or-later
"""Owner feedback: creation commands must preserve component ownership/context."""
import os
import sys
from pathlib import Path
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import ComponentModel as Model
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as Navigator
if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    Navigator = sys.modules["freecad.gui.ComponentNavigator"]
from freecad.gui import ComponentSelection as Selection


class TestComponentAddCommand(unittest.TestCase):
    def setUp(self):
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / self._testMethodName
        self.output.mkdir()
        self.doc = Model.new_document("Assembly")
        self.root = Model.metadata(self.doc).RootComponent
        self.doc.saveAs(str(self.output / "Assembly.cadprt"))
        self.panel = Navigator.show(self.doc)
        self.window = self.panel.mdi.activeSubWindow()
        self.warnings = patch.object(QtWidgets.QMessageBox, "warning").start()
        self.addCleanup(patch.stopall)

    def tearDown(self):
        for doc in reversed(list(App.listDocuments().values())):
            App.closeDocument(doc.Name)

    def create(self, command, label):
        with patch.object(QtWidgets.QInputDialog, "getItem", side_effect=lambda *args: (args[3][0], True)), \
                patch.object(QtWidgets.QInputDialog, "getText", return_value=(label, True)):
            Gui.runCommand(command)
        self.assertFalse(self.warnings.called, str(self.warnings.call_args))
        self.panel.refresh()

    def assert_context(self, component, ids):
        self.assertEqual(self.panel.mdi.activeSubWindow(), self.window)
        self.assertEqual(self.panel.root_key, Navigator.object_key(self.root))
        self.assertEqual(self.panel.active_path, ids)
        self.assertEqual(Gui.getDocument(self.doc.Name).activeView().getActiveObject("part", False),
                         (component, self.root, Selection.native_path(self.root, ids)))
        origin_row = self.panel.history.topLevelItem(0)
        self.assertEqual(origin_row.data(0, QtCore.Qt.UserRole), Navigator.object_key(component.Origin))
        self.assertEqual(origin_row.checkState(0), QtCore.Qt.Checked)
        self.assertFalse(origin_row.flags() & QtCore.Qt.ItemIsUserCheckable)
        menu = self.panel.build_menu(self.panel.history, origin_row)
        self.assertNotIn("Suppress Selected Items", [action.text() for action in menu.actions()])
        self.panel.history.clearSelection()
        origin_row.setSelected(True)
        picks = Selection.selected(self.root, Gui.Selection.getSelectionEx("*", 0))
        self.assertEqual([(pick.ids, pick.item) for pick in picks], [(tuple(ids), component.Origin)])
        Gui.Selection.clearSelection()
        Model.validate(self.doc)

    def testStandardCommandAddsUnderRootAndActiveChild(self):
        self.create("Std_Part", "Support")
        support = Model.children(self.root)[0]
        self.assertEqual(support.LinkedObject.Label, "Support")
        self.assert_context(self.root, [])
        self.panel.activate_item(self.panel.structure.topLevelItem(0).child(0))
        self.panel.refresh()
        self.create("Std_Part", "Pin")
        self.assertEqual(len(Model.children(self.root)), 1)
        self.assertEqual(Model.children(support.LinkedObject)[0].LinkedObject.Label, "Pin")
        self.assert_context(support.LinkedObject, [support.ObjectId])
        self.doc.undo()
        self.panel.refresh()
        self.assertEqual(Model.children(support.LinkedObject), [])
        self.assert_context(support.LinkedObject, [support.ObjectId])
        self.doc.redo()
        self.panel.refresh()
        self.assertEqual(len(Model.children(support.LinkedObject)), 1)
        self.assertTrue(all(Model.is_component(obj) for obj in self.doc.Objects if obj.TypeId == "App::Part"))

    def testAssemblyCommandUsesSameComponentRoute(self):
        import CommandInsertNewPart
        self.assertTrue(CommandInsertNewPart.CommandInsertNewPart().IsActive())
        self.create("Assembly_InsertNewPart", "Support")
        support = Model.children(self.root)[0]
        self.panel.activate_item(self.panel.structure.topLevelItem(0).child(0))
        self.panel.refresh()
        self.create("Assembly_InsertNewPart", "Pin")
        self.assertEqual(len(Model.children(support.LinkedObject)), 1)
        self.assert_context(support.LinkedObject, [support.ObjectId])

    def testFileInsertionRestoresExternalOccurrenceOnSuccessAndFailure(self):
        external = Model.new_document("Support")
        support = Model.metadata(external).RootComponent
        external.saveAs(str(self.output / "Support.cadprt"))
        source = Model.new_document("Pin")
        source.saveAs(str(self.output / "Pin.cadprt"))
        App.closeDocument(source.Name)
        Model.add_component(self.root, support)
        second = Model.add_component(self.root, support)
        self.panel.mdi.setActiveSubWindow(self.window)
        self.panel.set_document(self.doc)
        self.panel.toggle_instances(self.panel.structure.topLevelItem(0).child(0))
        self.panel.refresh()
        self.panel.activate_item(self.panel.structure.topLevelItem(0).child(0).child(1))
        self.panel.refresh()
        with patch.object(QtWidgets.QInputDialog, "getItem", side_effect=lambda *args: (args[3][1 if len(args[3]) > 1 else 0], True)), \
                patch.object(QtWidgets.QFileDialog, "getOpenFileName", return_value=(str(self.output / "Pin.cadprt"), "")):
            self.panel.add_component()
        self.assertEqual(len(Model.children(support)), 1)
        self.assert_context(support, [second.ObjectId])
        with patch.object(QtWidgets.QInputDialog, "getItem", side_effect=lambda *args: (args[3][1 if len(args[3]) > 1 else 0], True)), \
                patch.object(QtWidgets.QFileDialog, "getOpenFileName", return_value=(str(self.output / "Assembly.cadprt"), "")):
            with self.assertRaises(ValueError):
                self.panel.add_component()
        self.assert_context(support, [second.ObjectId])
