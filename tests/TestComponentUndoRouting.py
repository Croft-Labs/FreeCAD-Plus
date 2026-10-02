# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three feedback workflows for native component-owner Undo and Redo."""
import hashlib
import math
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentExtrude as Extrude
from PySide import QtWidgets
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentSelection as Selection


class TestComponentUndoRouting(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        self.assertEqual(hashlib.sha256(Path(Navigator.__file__).read_bytes()).digest(),
                         hashlib.sha256((source / "src/Gui/ComponentNavigator.py").read_bytes()).digest())
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / self._testMethodName
        self.output.mkdir()
        self.external = Model.new_document("Support")
        self.part = Model.metadata(self.external).RootComponent
        self.profile = Sketch.create(self.part)
        self.profile.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        self.external.recompute()
        self.operation, self.body = Extrude.create(self.part, self.profile, 5)
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
        group = self.panel.structure.topLevelItem(0)
        self.panel.toggle_instances(group)
        self.panel.refresh()
        self.panel.activate_item(self.panel.structure.topLevelItem(0).child(1))
        self.panel.refresh()
        self.doc.clearUndos()
        self.external.clearUndos()
        with Model.transaction(self.doc, "Parent change"):
            self.root.Label = "Parent change retained"

    def tearDown(self):
        for doc in reversed(list(App.listDocuments().values())):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def command(self, command):
        Gui.runCommand(command)
        self.panel.refresh()
        Gui.updateGui()

    def assert_context(self):
        self.assertEqual(App.ActiveDocument, self.doc)
        self.assertEqual(self.panel.mdi.activeSubWindow(), self.window)
        self.assertEqual(self.panel.active_path, [self.second.ObjectId])
        self.assertEqual(Gui.activeDocument().activeView().getActiveObject("part", False),
                         (self.part, self.root, Selection.native_path(self.root, [self.second.ObjectId])))
        self.assertEqual(self.root.Label, "Parent change retained")
        self.assertEqual(list(self.doc.UndoNames), ["Parent change"])

    def testExternalOperationUndoRedoAndAvailability(self):
        self.assertFalse(Gui.Command.get("Std_Undo").isActive())
        self.assertEqual(Gui.activeDocument().activeView().undoActions(), [])
        self.assertFalse(Gui.Command.get("Std_Redo").isActive())
        self.operation = Extrude.edit(self.operation, self.profile, 9)
        identity = self.body.ObjectId
        self.assertTrue(Gui.Command.get("Std_Undo").isActive())
        self.assertEqual(Gui.activeDocument().activeView().undoActions(), list(self.external.UndoNames))
        self.command("Std_Undo")
        self.assert_context()
        self.assertAlmostEqual(self.body.Shape.Volume, 20 * math.pi)
        self.assertEqual(Model.history_state(self.body), "Ready")
        self.assertFalse(Gui.Command.get("Std_Undo").isActive())
        self.assertTrue(Gui.Command.get("Std_Redo").isActive())
        self.command("Std_Redo")
        self.assert_context()
        self.assertEqual(self.body.ObjectId, identity)
        self.assertAlmostEqual(self.body.Shape.Volume, 36 * math.pi)
        Model.set_suppressed(self.operation, True)
        self.command("Std_Undo")
        self.assertEqual(Model.history_state(self.body), "Ready")
        self.assertFalse(getattr(self.operation, "UserSuppressed", False))
        self.assertAlmostEqual(self.body.Shape.Volume, 36 * math.pi)
        self.command("Std_Redo")
        self.assertTrue(self.operation.UserSuppressed)
        self.assertTrue(self.body.Shape.isNull())
        self.command("Std_Undo")
        self.external.save()
        self.doc.save()
        self.capture("restored-model-history.png")

    def menu(self, name):
        menus = [widget for widget in QtWidgets.QApplication.allWidgets()
                 if isinstance(widget, QtWidgets.QMenu) and widget.metaObject().className().endswith(name)]
        self.assertTrue(menus, name)
        menu = menus[0]
        menu.aboutToShow.emit()
        return menu

    def testToolbarHistoryRangeUsesExternalOwner(self):
        for name, label in (("First support rename", "First support"),
                            ("Second support rename", "Second support")):
            with Model.transaction(self.external, name):
                self.part.Label = label
        undo = self.menu("UndoDialog")
        self.assertEqual([action.text() for action in undo.actions()], list(self.external.UndoNames))
        self.assertNotIn("Parent change", [action.text() for action in undo.actions()])
        undo.actions()[1].trigger()
        self.panel.refresh()
        self.assertEqual(self.part.Label, "Support")
        self.assert_context()
        redo = self.menu("RedoDialog")
        self.assertEqual([action.text() for action in redo.actions()], list(self.external.RedoNames))
        redo.actions()[1].trigger()
        self.panel.refresh()
        self.assertEqual(self.part.Label, "Second support")
        self.assert_context()

    def testEmbeddedIsolatedOwnerAndOrdinaryDocumentFallback(self):
        link = Model.add_component(self.root, label="Embedded pin")
        pin = link.LinkedObject
        self.panel.open_component_tab(Navigator.object_key(link))
        window = self.panel.mdi.activeSubWindow()
        self.doc.clearUndos()
        with Model.transaction(self.doc, "Rename embedded pin"):
            pin.Label = "Changed pin"
        self.command("Std_Undo")
        self.assertEqual(pin.Label, "Embedded pin")
        self.assertEqual(self.panel.mdi.activeSubWindow(), window)
        self.command("Std_Redo")
        self.assertEqual(pin.Label, "Changed pin")
        self.assertEqual(self.panel.active_key, Navigator.object_key(pin))
        ordinary = App.newDocument("Ordinary document")
        ordinary.openTransaction("Ordinary edit")
        ordinary.addObject("Part::Box", "Box")
        ordinary.commitTransaction()
        ordinary.recompute()
        self.assertEqual(Gui.activeDocument().activeView().undoActions(), ["Ordinary edit"])
        Gui.runCommand("Std_Undo")
        self.assertIsNone(ordinary.getObject("Box"))
        Gui.runCommand("Std_Redo")
        self.assertIsNotNone(ordinary.getObject("Box"))
        self.assertEqual(pin.Label, "Changed pin")

    def capture(self, filename):
        self.panel.setFloating(True)
        self.panel.resize(850, 650)
        Gui.updateGui()
        self.panel.grab().save(str(self.output / filename))
