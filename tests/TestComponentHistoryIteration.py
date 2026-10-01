# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three bounded feedback checks for dependency-aware history suppression."""
import hashlib
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import CadDocument
import ComponentModel as Model
from PySide import QtCore
from freecad.gui import ComponentNavigator as Navigator


class TestComponentHistoryIteration(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, relative in [(Model, "src/Mod/Part/ComponentModel.py"),
                                 (Navigator, "src/Gui/ComponentNavigator.py")]:
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((source / relative).read_bytes()).digest())
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        self.doc = Model.new_document("History feedback")
        self.root = Model.metadata(self.doc).RootComponent
        self.base = self.body("Stock", 10)
        self.tool = self.body("SharedTool", 1)
        self.second_tool = self.body("SecondTool", 2)
        self.first, self.first_result = self.cut("FirstCut", self.base, self.tool)
        self.second, self.second_result = self.cut("SecondCut", self.first_result, self.second_tool)
        self.independent_base = self.body("IndependentStock", 5)
        self.independent, self.independent_result = self.cut("IndependentCut", self.independent_base, self.tool)
        self.panel = Navigator.show(self.doc)
        self.panel.tabs.setCurrentWidget(self.panel.history)

    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def body(self, name, length):
        obj = self.doc.addObject("Part::Feature", name)
        Model.register_object(self.root, obj, "Object", True)
        obj.Shape = Part.makeBox(length, 3, 4)
        obj.Visibility = True
        self.doc.recompute()
        return obj

    def cut(self, name, base, tool):
        # Native commands hide their inputs as links are assigned. The command's
        # transaction captures the visibility before that happens.
        with Model.transaction(self.doc, name):
            obj = self.doc.addObject("Part::Cut", name)
            Model.register_object(self.root, obj, "Operation")
            obj.Base, obj.Tool = base, tool
            self.doc.recompute()
            result = Model.publish_result(self.root, obj, name + " body")
        return obj, result

    def row(self, obj):
        self.panel.refresh()
        return next(self.panel.history.topLevelItem(i) for i in range(self.panel.history.topLevelItemCount())
                    if self.panel.history.topLevelItem(i).data(0, QtCore.Qt.UserRole) == Navigator.object_key(obj))

    def testBranchRestorationAndSharedConsumer(self):
        Model.set_suppressed(self.first, True)
        self.assertTrue(self.base.Visibility)
        self.assertTrue(self.second_tool.Visibility)
        self.assertFalse(self.tool.Visibility)  # Still consumed by the independent cut.
        self.assertTrue(self.first_result.Shape.isNull())
        self.assertTrue(self.second_result.Shape.isNull())
        self.assertAlmostEqual(self.independent_result.Shape.Volume, 48)
        self.assertIn(self.base, Model.finished_results(self.root))
        self.assertNotIn(self.tool, Model.finished_results(self.root))
        self.assertEqual(self.row(self.second).checkState(0), QtCore.Qt.PartiallyChecked)
        self.assertIn(self.first.Label, self.row(self.second).toolTip(3))
        # Explicitly suppress an already inactive item. Restoring the upstream
        # item must not clear that decision, or resurrect the later body.
        Model.set_suppressed(self.second, True)
        Model.set_suppressed(self.first, False)
        self.assertTrue(self.second.UserSuppressed)
        self.assertTrue(self.first_result.Visibility)
        self.assertIn(self.first_result, Model.finished_results(self.root))
        self.assertTrue(self.second_result.Shape.isNull())
        Model.set_suppressed(self.second, False)
        self.assertFalse(self.first_result.Visibility)
        self.assertTrue(self.second_result.Visibility)
        self.assertAlmostEqual(self.second_result.Shape.Volume, 96)
        self.assertIn(self.second_result, Model.finished_results(self.root))

    def testSelectedHistoryItemsSingleUndoAndReopen(self):
        self.panel.refresh()
        keys = [Navigator.object_key(self.first), Navigator.object_key(self.independent)]
        rows = [self.panel.history.topLevelItem(i) for i in range(self.panel.history.topLevelItemCount())
                if self.panel.history.topLevelItem(i).data(0, QtCore.Qt.UserRole) in keys]
        for row in rows:
            row.setSelected(True)
        menu = self.panel.build_menu(self.panel.history, rows[0])
        next(action for action in menu.actions() if action.text() == "Suppress Selected Items").trigger()
        self.assertTrue(self.first.UserSuppressed)
        self.assertTrue(self.independent.UserSuppressed)
        self.assertTrue(self.tool.Visibility)  # Both consumers are now inactive.
        self.doc.undo()
        self.doc.recompute()
        self.assertFalse(getattr(self.first, "UserSuppressed", False))
        self.assertFalse(getattr(self.independent, "UserSuppressed", False))
        self.assertAlmostEqual(self.second_result.Shape.Volume, 96)
        self.assertFalse(self.tool.Visibility)
        self.doc.redo()
        self.doc.recompute()
        self.assertTrue(self.first.UserSuppressed)
        self.assertTrue(self.independent.UserSuppressed)
        path = self.output / "Component-History-Suppressed.cadprt"
        self.doc.saveAs(str(path))
        first_name, second_name, result_name = self.first.Name, self.second.Name, self.second_result.Name
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(path)
        self.first = self.doc.getObject(first_name)
        self.second = self.doc.getObject(second_name)
        self.root = Model.metadata(self.doc).RootComponent
        self.panel = Navigator.show(self.doc)
        self.panel.tabs.setCurrentWidget(self.panel.history)
        self.assertTrue(self.first.UserSuppressed)
        self.assertEqual(Model.history_state(self.second), "Inactive \u2014 dependency")
        self.assertNotIn(self.doc.getObject(result_name), Model.finished_results(self.root))
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()
        self.panel.setFloating(True)
        self.panel.resize(850, 650)
        self.panel.show()
        Gui.updateGui()
        self.panel.grab().save(str(self.output / "history-suppressed.png"))

    def testPrimitiveSuppressionAndVisibilityRemainSeparate(self):
        self.base.Visibility = False
        Model.set_suppressed(self.base, True)
        self.assertTrue(self.second_result.Shape.isNull())
        self.assertNotIn(self.base, Model.finished_results(self.root))
        self.assertEqual(Model.history_state(self.first), "Inactive \u2014 dependency")
        self.assertFalse(getattr(self.first, "UserSuppressed", False))
        Model.set_suppressed(self.base, False)
        self.assertFalse(self.base.Visibility)
        self.assertAlmostEqual(self.second_result.Shape.Volume, 96)
        self.assertTrue(self.second_result.Visibility)
        # An independent manually hidden object stays hidden through the batch.
        independent = self.body("HiddenObject", 3)
        independent.Visibility = False
        Model.set_items_suppressed([self.first, independent], True)
        Model.set_items_suppressed([self.first, independent], False)
        self.assertFalse(independent.Visibility)
        self.assertAlmostEqual(self.second_result.Shape.Volume, 96)
        self.tool.Visibility = True  # Deliberately inspect an intermediate input.
        Model.set_suppressed(independent, True)
        self.assertTrue(self.tool.Visibility)
        Model.set_suppressed(independent, False)
        self.assertTrue(self.tool.Visibility)
        self.doc.saveAs(str(self.output / "Component-History-Restored.cadprt"))
