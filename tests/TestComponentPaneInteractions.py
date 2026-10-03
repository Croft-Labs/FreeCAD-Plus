# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Qt input and cross-tab lifecycle regressions for Components."""
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest
import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentExtrude as Extrude
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentExtrudeTask as ExtrudeTask


class TestComponentPaneInteractions(unittest.TestCase):
    def setUp(self):
        self.warnings = []
        warning = patch.object(QtWidgets.QMessageBox, "warning",
                               side_effect=lambda *args: self.warnings.append(args[2]))
        warning.start()
        self.addCleanup(warning.stop)
        self.doc = Model.new_document("Pane input")
        self.root = Model.metadata(self.doc).RootComponent
        self.a = Model.add_component(self.root, label="Bracket")
        self.b = Model.add_component(self.root, label="Pin")
        self.box = self.doc.addObject("Part::Box", "Stock")
        Model.register_object(self.root, self.box, "Object", True)
        self.doc.recompute()
        self.panel = Navigator.show(self.doc)
        self.panel.setFloating(True)
        self.panel.resize(780, 600)
        self.panel.show()
        self.settle()

    def tearDown(self):
        if ExtrudeTask._task:
            ExtrudeTask._task.reject()
        if Gui.Control.activeDialog():
            Gui.Control.closeDialog()
        Gui.Selection.clearSelection()
        for doc in reversed(list(App.listDocuments().values())):
            gui = Gui.getDocument(doc.Name)
            if gui.getInEdit():
                gui.resetEdit()
            App.closeDocument(doc.Name)
        self.settle()
        self.assertEqual(self.warnings, [], "Unexpected component operation warning")

    @staticmethod
    def settle():
        Gui.updateGui()
        QtWidgets.QApplication.processEvents()
        QtTest.QTest.qWait(150)  # Navigator coalesces document notifications for 100 ms.

    def tab(self, index):
        bar = self.panel.tabs.tabBar()
        QtTest.QTest.mouseClick(bar, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                               bar.tabRect(index).center())
        self.settle()
        self.assertEqual(self.panel.tabs.currentIndex(), index)

    def model_row(self, obj):
        return next(self.panel.models.topLevelItem(i)
                    for i in range(self.panel.models.topLevelItemCount())
                    if self.panel.models.topLevelItem(i).data(0, QtCore.Qt.UserRole)
                    == Navigator.object_key(obj))

    def history_row(self, obj):
        return next(self.panel.history.topLevelItem(i)
                    for i in range(self.panel.history.topLevelItemCount())
                    if self.panel.history.topLevelItem(i).data(0, QtCore.Qt.UserRole)
                    == Navigator.object_key(obj))

    def click(self, tree, row, column, double=False):
        key = row.data(0, QtCore.Qt.UserRole)
        tree.scrollToItem(row)
        self.settle()
        # Deferred document observers may replace the rows while scrolling.
        iterator = QtWidgets.QTreeWidgetItemIterator(tree)
        row = None
        while iterator.value():
            if iterator.value().data(0, QtCore.Qt.UserRole) == key:
                row = iterator.value()
                break
            iterator += 1
        self.assertIsNotNone(row)
        rect = tree.visualItemRect(row)
        self.assertFalse(rect.isEmpty())
        header = tree.header()
        offset = min(14, header.sectionSize(column) // 2)
        if tree == self.panel.structure and column == 0:
            depth, parent = 1, row.parent()
            while parent:
                depth += 1
                parent = parent.parent()
            offset = tree.indentation() * depth + 14  # Label, beyond the expander.
        point = QtCore.QPoint(header.sectionViewportPosition(column)
                             + offset, rect.center().y())
        QtTest.QTest.mouseClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
        if double:
            QtTest.QTest.mouseDClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
        self.settle()

    def testModelsMouseSelectionRenameAndUndo(self):
        self.tab(0)
        self.click(self.panel.models, self.model_row(self.a.LinkedObject), 0)
        self.assertEqual(Gui.Selection.getSelection(), [self.a.LinkedObject])
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))
        menu = self.panel.build_menu(self.panel.models, self.model_row(self.a.LinkedObject))
        with patch.object(QtWidgets.QInputDialog, "getText", return_value=("Renamed bracket", True)):
            next(action for action in menu.actions() if action.text() == "Rename").trigger()
        self.settle()
        self.assertEqual(self.model_row(self.a.LinkedObject).text(0), "Renamed bracket")
        self.assertEqual(self.panel.structure.topLevelItem(0).child(0).text(0), "Renamed bracket")
        self.doc.undo()
        self.settle()
        self.assertEqual(self.model_row(self.a.LinkedObject).text(0), "Bracket")
        self.doc.redo()
        self.settle()
        self.assertEqual(self.model_row(self.a.LinkedObject).text(0), "Renamed bracket")

    def testModelsDoubleClickAndReturnToAssemblyWindow(self):
        assembly = self.panel.mdi.activeSubWindow()
        objects = len(self.doc.Objects)
        self.tab(0)
        self.click(self.panel.models, self.model_row(self.a.LinkedObject), 0, double=True)
        self.assertEqual(self.panel.tabs.currentWidget(), self.panel.history)
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.a.LinkedObject))
        isolated = self.panel.mdi.activeSubWindow()
        self.assertNotEqual(isolated, assembly)
        self.assertEqual(len(self.doc.Objects), objects)
        self.panel.mdi.setActiveSubWindow(assembly)
        self.settle()
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))
        self.assertEqual(self.panel.structure.topLevelItem(0).childCount(), 2)

    def testPartTreeMouseEditingAndVisibilityUndo(self):
        self.tab(1)
        self.click(self.panel.structure, self.panel.structure.topLevelItem(0).child(0), 1)
        self.assertEqual(Model.representation(self.root, [self.a.ObjectId]), "Hidden")
        self.doc.undo()
        self.settle()
        self.assertEqual(Model.representation(self.root, [self.a.ObjectId]), "Bodies Only")
        self.click(self.panel.structure, self.panel.structure.topLevelItem(0).child(0), 0, double=True)
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.a.LinkedObject))
        self.assertEqual(self.panel.active_path, [self.a.ObjectId])
        self.assertEqual(self.panel.tabs.currentWidget(), self.panel.history)
        self.tab(1)
        self.click(self.panel.structure, self.panel.structure.topLevelItem(0), 0, double=True)
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))
        self.assertEqual(self.panel.active_path, [])

    def testHistoryMouseEyesCheckboxAndUndo(self):
        self.tab(2)
        self.click(self.panel.history, self.history_row(self.box), 1)
        self.assertFalse(self.box.Visibility)
        self.doc.undo()
        self.settle()
        self.assertTrue(self.box.Visibility)
        self.click(self.panel.history, self.history_row(self.box), 0)
        self.assertTrue(self.box.UserSuppressed)
        self.assertEqual(self.history_row(self.box).checkState(0), QtCore.Qt.Unchecked)
        self.doc.undo()
        self.settle()
        self.assertFalse(getattr(self.box, "UserSuppressed", False))
        self.assertEqual(self.history_row(self.box).checkState(0), QtCore.Qt.Checked)
        self.click(self.panel.history, self.history_row(self.root.Origin).child(0), 1)
        self.assertTrue(all(plane.Visibility for plane in Navigator.origin_planes(self.root.Origin)))
        self.doc.undo()
        self.settle()
        self.assertFalse(any(plane.Visibility for plane in Navigator.origin_planes(self.root.Origin)))

    def testHistoryDoubleClickExtrudeCancelPreservesIdentity(self):
        self.box.Visibility = False
        profile = Sketch.create(self.root)
        profile.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        self.doc.recompute()
        operation, result = Extrude.create(self.root, profile, 5)
        self.panel.refresh()
        identity, volume = operation.ObjectId, result.Shape.Volume
        self.tab(2)
        self.click(self.panel.history, self.history_row(operation), 2, double=True)
        self.assertTrue(Gui.Control.activeDialog())
        self.assertIsNotNone(ExtrudeTask._task)
        ExtrudeTask._task.reject()
        self.settle()
        self.assertEqual(operation.ObjectId, identity)
        self.assertAlmostEqual(result.Shape.Volume, volume)
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))

    def testHistoryStatusDoubleClickOpensOperation(self):
        profile = Sketch.create(self.root)
        profile.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        self.doc.recompute()
        operation, result = Extrude.create(self.root, profile, 5)
        self.panel.refresh()
        self.tab(2)
        self.click(self.panel.history, self.history_row(operation), 3, double=True)
        self.assertIsNotNone(ExtrudeTask._task)
        self.assertEqual(ExtrudeTask._task.operation, operation)
        ExtrudeTask._task.reject()

    def testSketchDoubleClickSurvivesRowRefresh(self):
        profile = Sketch.create(self.root)
        profile.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        self.doc.recompute()
        self.panel.refresh()
        self.tab(2)
        tree = self.panel.history
        row = self.history_row(profile)
        point = QtCore.QPoint(tree.header().sectionViewportPosition(2) + 18,
                             tree.visualItemRect(row).center().y())
        QtTest.QTest.mouseClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
        # Model notifications can rebuild the item between the two native clicks.
        self.panel.refresh()
        QtTest.QTest.mouseDClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
        self.settle()
        editing = Gui.getDocument(self.doc.Name).getInEdit()
        self.assertIsNotNone(editing)
        self.assertEqual(editing.Object, profile)
        Gui.getDocument(self.doc.Name).resetEdit()
        self.settle()
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.root))

    def testHistoryDoubleClickNativeFeature(self):
        self.tab(2)
        self.click(self.panel.history, self.history_row(self.box), 2, double=True)
        editing = Gui.getDocument(self.doc.Name).getInEdit()
        self.assertIsNotNone(editing)
        self.assertEqual(editing.Object, self.box)
        self.assertTrue(Gui.Control.activeDialog())
        Gui.getDocument(self.doc.Name).resetEdit()
        self.settle()

    def testModelsRootEditRefusedDuringTask(self):
        self.panel.activate_item(self.panel.structure.topLevelItem(0).child(0))
        self.panel.refresh()
        before = (self.panel.root_key, self.panel.active_key, list(self.panel.active_path))
        task = type("BusyTask", (), {"form": QtWidgets.QWidget(),
                                     "getStandardButtons": lambda self: 0})()
        Gui.Control.showDialog(task)
        menu = self.panel.build_menu(self.panel.models, self.model_row(self.root))
        next(action for action in menu.actions() if action.text() == "Edit").trigger()
        self.settle()
        self.assertEqual((self.panel.root_key, self.panel.active_key, self.panel.active_path), before)
        self.assertEqual(len(self.warnings), 1)
        self.assertIn("Finish", self.warnings.pop())

    def testCrossTabRefreshStressAndCloseLastDocument(self):
        for unused in range(20):
            for index in range(3):
                self.tab(index)
                self.panel.refresh()
                self.assertEqual(self.panel.models.topLevelItemCount(), 3)
                self.assertEqual(self.panel.structure.topLevelItem(0).childCount(), 2)
                self.assertEqual(self.panel.history.topLevelItemCount(), 2)
                self.assertEqual(self.model_row(self.a.LinkedObject).text(1), "1")
        App.closeDocument(self.doc.Name)
        self.settle()
        for tree in (self.panel.models, self.panel.structure, self.panel.history):
            self.assertEqual(tree.topLevelItemCount(), 0)
        self.assertIsNone(self.panel.active_key)
        self.assertIn("Create or open", self.panel.context.text())

    def testOpenContextMenusSurviveDeferredRefresh(self):
        menu = self.panel.build_menu(self.panel.structure, self.panel.structure.topLevelItem(0).child(0))
        self.panel.refresh()
        next(action for action in menu.actions() if action.text() == "Edit").trigger()
        self.settle()
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.a.LinkedObject))
        self.panel.activate_item(self.panel.structure.topLevelItem(0))
        self.panel.refresh()
        menu = self.panel.build_menu(self.panel.history, self.history_row(self.root.Origin))
        self.panel.refresh()
        next(action for action in menu.actions() if action.text() == "Hide").trigger()
        self.settle()
        self.assertFalse(self.root.Origin.Visibility)
        menu = self.panel.build_menu(self.panel.models, self.model_row(self.a.LinkedObject))
        self.panel.refresh()
        next(action for action in menu.actions() if action.text() == "Edit").trigger()
        self.settle()
        self.assertEqual(self.panel.active_key, Navigator.object_key(self.a.LinkedObject))

    def testSharedNestedCountsUnusedModelsAndSaveReopen(self):
        shared = Model.create_definition(self.doc, "Shared fastener")
        for index in range(8):
            link = Model.add_component(self.root, label="Group " + str(index))
            Model.add_component(link.LinkedObject, shared)
            for unused in range(2):
                Model.add_component(self.root, link.LinkedObject)
        unused_models = [Model.create_definition(self.doc, "Unused " + str(index)) for index in range(12)]
        self.doc.recompute()
        self.panel.refresh()
        self.assertEqual(self.model_row(shared).text(1), "24")
        self.assertTrue(all(self.model_row(obj).text(1) == "0" for obj in unused_models))
        identities = {obj.ObjectId: int(self.model_row(obj).text(1)) for obj in Model.definitions(self.doc)}
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "PaneInventory.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.settle()
        self.doc = App.openDocument(str(path))
        self.root = Model.metadata(self.doc).RootComponent
        self.panel.set_document(self.doc)
        self.settle()
        self.assertEqual({obj.ObjectId: int(self.model_row(obj).text(1))
                          for obj in Model.definitions(self.doc)}, identities)
        self.assertEqual(self.panel.structure.topLevelItem(0).childCount(), 10)
        for index in range(self.panel.models.topLevelItemCount()):
            self.assertEqual(self.panel.models.topLevelItem(index).childCount(), 0)
        Model.validate(self.doc)

    def testPlusClassicAndNarrowPaneCaptures(self):
        from freecad.gui import PlusRibbon
        prefs = App.ParamGet("User parameter:BaseApp/Preferences/General")
        original = prefs.GetString("ToolbarUIStyle", "Plus")
        try:
            for style in ("Plus", "Classic"):
                prefs.SetString("ToolbarUIStyle", style)
                PlusRibbon.apply_preferences()
                self.panel.resize(420, 460)
                for index, label in enumerate(("Models", "Part Tree", "History")):
                    self.tab(index)
                    self.assertEqual(self.panel.tabs.tabText(index), label)
                    self.assertTrue(self.panel.tabs.currentWidget().isVisible())
                    output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
                    self.assertTrue(self.panel.grab().save(str(output / (style + "-" + label.replace(" ", "") + ".png"))))
        finally:
            prefs.SetString("ToolbarUIStyle", original)
            PlusRibbon.apply_preferences()
