# SPDX-License-Identifier: LGPL-2.1-or-later
"""Definition inventory, occurrence-only assembly and safe instance deletion."""
import importlib.util
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtGui, QtWidgets

if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    spec = importlib.util.spec_from_file_location("ModelsOverlay", Path(__file__).with_name("TestComponentBackgroundResult.py"))
    overlay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(overlay)

import ComponentModel as Model
from freecad.gui import ComponentNavigator as Navigator


class TestComponentModelsPane(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_document("Assembly")
        self.root = Model.metadata(self.doc).RootComponent
        self.first = Model.add_component(self.root, label="Bracket")
        self.part = self.first.LinkedObject
        self.shape = self.doc.addObject("Part::Feature", "BracketGeometry")
        Model.register_object(self.part, self.shape, "Object", True)
        self.shape.Shape = Part.makeBox(10, 8, 6)
        self.doc.recompute()
        self.panel = Navigator.show(self.doc)

    def tearDown(self):
        Gui.Selection.clearSelection()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def model_row(self, obj):
        return next(self.panel.models.topLevelItem(i) for i in range(self.panel.models.topLevelItemCount())
                    if self.panel.models.topLevelItem(i).data(0, QtCore.Qt.UserRole) == Navigator.object_key(obj))

    def testLayoutAndSingleOccurrence(self):
        self.assertEqual([self.panel.tabs.tabText(i) for i in range(3)],
                         ["Models", "Assembly Structure", "Model History"])
        self.assertEqual(self.panel.models.topLevelItemCount(), 2)
        self.assertFalse(self.panel.models.itemsExpandable())
        for i in range(2):
            self.assertEqual(self.panel.models.topLevelItem(i).childCount(), 0)
        self.assertEqual(self.model_row(self.part).text(1), "1")
        self.assertEqual(self.model_row(self.root).text(1), "0")
        self.assertEqual(self.panel.structure.topLevelItemCount(), 1)
        row = self.panel.structure.topLevelItem(0)
        for key, path in self.panel.members(row):
            self.assertEqual(Navigator.resolve(key).ComponentRole, "Occurrence")
            self.assertEqual(path, [self.first.ObjectId])
        attributes = Gui.getMainWindow().findChild(QtWidgets.QDockWidget, "Model")
        self.assertEqual(attributes.windowTitle(), "Attributes")
        trees = [w for w in attributes.findChildren(QtWidgets.QWidget)
                 if w.metaObject().className().endswith("TreePanel")]
        self.assertTrue(trees)
        self.assertTrue(all(not w.isVisibleTo(attributes) for w in trees))
        tab_labels = {tabs.tabText(i) for tabs in attributes.findChildren(QtWidgets.QTabWidget)
                      for i in range(tabs.count())}
        self.assertTrue({"View", "Data"}.issubset(tab_labels), str(tab_labels))
        self.panel.resize(650, 420)
        self.panel.tabs.setCurrentWidget(self.panel.models)
        Gui.updateGui()
        self.panel.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "models.png"))
        self.panel.tabs.setCurrentWidget(self.panel.structure)
        Gui.updateGui()
        self.panel.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "assembly-structure.png"))

    def testDeleteAllRetainModelUndoReopenAndReuse(self):
        second = Model.add_component(self.root, self.part)
        identity, shape_identity = self.part.ObjectId, self.shape.ObjectId
        first_name, second_name = self.first.Name, second.Name
        Model.remove_instances([self.first])
        self.panel.refresh()
        self.assertEqual(self.model_row(self.part).text(1), "1")
        self.assertIsNone(self.doc.getObject(first_name))
        self.assertEqual(second.LinkedObject, self.part)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(len(Model.children(self.root)), 2)
        Model.remove_instances(Model.children(self.root))
        self.panel.refresh()
        self.assertEqual(self.panel.structure.topLevelItemCount(), 0)
        self.assertEqual(self.model_row(self.part).text(1), "0")
        self.assertEqual(self.part.ObjectId, identity)
        self.assertEqual(self.shape.ObjectId, shape_identity)
        self.assertAlmostEqual(self.shape.Shape.Volume, 480)
        part_name = self.part.Name
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "UnusedModel.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.root = Model.metadata(self.doc).RootComponent
        self.part = self.doc.getObject(part_name)
        self.panel.set_document(self.doc)
        self.assertEqual(self.part.ObjectId, identity)
        self.assertEqual(self.model_row(self.part).text(1), "0")
        menu = self.panel.build_menu(self.panel.models, self.model_row(self.part))
        next(action for action in menu.actions() if action.text() == "Add Instance").trigger()
        self.assertEqual(Model.children(self.root)[0].LinkedObject.ObjectId, identity)
        self.panel.refresh()
        self.assertEqual(self.model_row(self.part).text(1), "1")
        self.assertIsNone(self.doc.getObject(second_name))
        Model.validate(self.doc)

    def testNestedCountsAndReferenceRepair(self):
        child = Model.add_component(self.part, label="Pin").LinkedObject
        second = Model.add_component(self.root, self.part)
        reference = Model.add_reference(self.root, self.first, self.shape)
        reference_identity = reference.ObjectId
        self.assertEqual(Model.instance_counts(self.root)[child], 2)
        Model.remove_instances([self.first])
        self.assertEqual(Model.instance_counts(self.root)[child], 1)
        self.assertEqual(reference.ResultStatus, "Missing source")
        self.assertTrue(reference.Shape.isNull())
        self.assertFalse(self.shape.Shape.isNull())
        self.assertEqual(second.LinkedObject, self.part)
        self.doc.undo()
        Model.activate(self.root, strict=False)
        self.assertEqual(reference.ObjectId, reference_identity)
        self.assertEqual(reference.ResultStatus, "Ready")
        self.assertEqual(Model.instance_counts(self.root)[child], 2)
        self.doc.redo()
        Model.activate(self.root, strict=False)
        self.assertEqual(reference.ResultStatus, "Missing source")
        Model.remove_instances([second])
        self.panel.refresh()
        self.assertEqual(self.model_row(child).text(1), "0")
        self.assertEqual(len(Model.children(self.part)), 1)
        self.assertEqual(len(Model.definitions(self.doc)), 3)

    def testKeyboardDeleteAndActiveFallback(self):
        row = self.panel.structure.topLevelItem(0)
        self.panel.activate_item(row)
        self.panel.refresh()
        row = self.panel.structure.topLevelItem(0)
        row.setSelected(True)
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Delete, QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(self.panel.structure, event)
        self.assertEqual(Model.children(self.root), [])
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))
        self.assertIsNotNone(self.doc.getObject(self.part.Name))
        model_row = self.model_row(self.part)
        model_row.setSelected(True)
        QtWidgets.QApplication.sendEvent(self.panel.models,
            QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Delete, QtCore.Qt.NoModifier))
        self.assertIsNotNone(self.doc.getObject(self.part.Name))

    def testUnplacedModelEditing(self):
        Model.remove_instances([self.first])
        self.panel.refresh()
        self.panel.edit_model(self.model_row(self.part))
        self.panel.refresh()
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.part))
        self.assertEqual(self.panel.tabs.currentWidget(), self.panel.history)
        self.assertEqual(self.panel.component_views[-1]["key"], Navigator.object_key(self.part))
        self.assertEqual(self.model_row(self.part).text(1), "0")

    def testStandardDeleteAdapter(self):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.doc.Name, self.root.Name, self.first.Name + ".")
        if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
            self.assertTrue(Navigator.delete_selected_instances())
        else:
            Gui.runCommand("Std_Delete")
        self.assertEqual(Model.children(self.root), [])
        self.assertIsNotNone(self.doc.getObject(self.part.Name))
        Gui.Selection.addSelection(self.part)
        self.assertFalse(Navigator.delete_selected_instances())
        if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") != "1":
            Gui.runCommand("Std_Delete")
        self.assertIsNotNone(self.doc.getObject(self.part.Name))
