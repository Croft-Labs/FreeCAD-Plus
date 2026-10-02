# SPDX-License-Identifier: LGPL-2.1-or-later
"""Part Tree ordering, native reparenting, clipboard/drop and atomic refusal."""
import importlib.util
import os
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets

if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    spec = importlib.util.spec_from_file_location("TreeMoveOverlay", Path(__file__).with_name("TestComponentModelsPane.py"))
    overlay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(overlay)

import ComponentModel as Model
from freecad.gui import ComponentNavigator as Navigator


class TestComponentTreeMove(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_document()
        self.root = Model.metadata(self.doc).RootComponent
        self.a = Model.add_component(self.root, label="A")
        self.b = Model.add_component(self.root, label="B")
        self.c = Model.add_component(self.root, label="C")
        self.panel = Navigator.show(self.doc)

    def tearDown(self):
        QtWidgets.QApplication.clipboard().clear()
        Gui.Selection.clearSelection()
        Gui.updateGui()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def row(self, ids=()):
        iterator = QtWidgets.QTreeWidgetItemIterator(self.panel.structure)
        while iterator.value():
            row = iterator.value()
            if any(tuple(value[1]) == tuple(ids) for value in self.panel.members(row)):
                return row
            iterator += 1
        self.fail("Missing tree path " + repr(ids))

    def testSiblingOrderingUndoPersistenceAndGrouping(self):
        identity = self.c.ObjectId
        Model.move_instances(self.root, [(self.c.ObjectId,)], (), self.a)
        self.assertEqual(Model.children(self.root), [self.c, self.a, self.b])
        self.assertEqual(self.c.ObjectId, identity)
        self.doc.undo()
        self.assertEqual(Model.children(self.root), [self.a, self.b, self.c])
        self.doc.redo()
        self.assertEqual(Model.children(self.root), [self.c, self.a, self.b])
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "Moved.cadprt"
        names = [obj.Name for obj in Model.children(self.root)]
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.root = Model.metadata(self.doc).RootComponent
        self.assertEqual([obj.Name for obj in Model.children(self.root)], names)

    def testReparentPreservesFrameIdentityAndActiveDescendant(self):
        self.root.Placement = App.Placement(App.Vector(8, 2, 1), App.Rotation(App.Vector(0, 0, 1), 15))
        self.a.LinkPlacement = App.Placement(App.Vector(30, 4, 2), App.Rotation(App.Vector(0, 0, 1), 45))
        self.a.LinkedObject.Placement = App.Placement(App.Vector(3, 0, 0), App.Rotation())
        self.c.LinkPlacement = App.Placement(App.Vector(-2, 9, 3), App.Rotation(App.Vector(0, 1, 0), 25))
        child = Model.add_component(self.c.LinkedObject, label="Nested")
        self.doc.recompute()
        before = Model._component_frame(self.root, [self.c.ObjectId])
        self.panel.refresh()
        self.panel.activate_item(self.row([self.c.ObjectId, child.ObjectId]))
        self.panel.refresh()
        self.row([self.c.ObjectId]).setSelected(True)
        mime = self.panel.move_mime()
        self.panel.paste_instances(self.row([self.a.ObjectId]), mime)
        self.assertEqual(Model.owner(self.c), self.a.LinkedObject)
        self.assertTrue(before.isSame(Model._component_frame(self.root, [self.a.ObjectId, self.c.ObjectId]), 1e-8))
        self.assertEqual(self.panel.active_path, [self.a.ObjectId, self.c.ObjectId, child.ObjectId])
        self.doc.undo()
        self.assertEqual(Model.owner(self.c), self.root)
        self.doc.redo()
        Model.validate(self.doc)

    def testKeyboardCutPasteAndMenu(self):
        row = self.row([self.c.ObjectId])
        row.setSelected(True)
        QtWidgets.QApplication.sendEvent(self.panel.structure,
            QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_X, QtCore.Qt.ControlModifier))
        self.assertEqual(Model.children(self.root), [self.a, self.b, self.c], "Cut must not delete")
        self.panel.structure.clearSelection()
        self.panel.structure.setCurrentItem(self.row([self.a.ObjectId]))
        QtWidgets.QApplication.sendEvent(self.panel.structure,
            QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_V, QtCore.Qt.ControlModifier))
        Gui.updateGui()
        self.assertEqual(Model.owner(self.c), self.a.LinkedObject)
        self.assertFalse(QtWidgets.QApplication.clipboard().mimeData().hasFormat(Navigator.PartTree.MIME))
        root_menu = self.panel.build_menu(self.panel.structure, self.row())
        self.assertNotIn("Cut", [action.text() for action in root_menu.actions()])
        self.assertIn("Paste", [action.text() for action in root_menu.actions()])

    def testDropRoutesNativeMutation(self):
        self.row([self.c.ObjectId]).setSelected(True)
        mime = self.panel.move_mime()
        self.panel.tabs.setCurrentWidget(self.panel.structure)
        self.panel.resize(700, 550)
        Gui.updateGui()
        point = self.panel.structure.visualItemRect(self.row([self.a.ObjectId])).center()
        event = QtGui.QDropEvent(QtCore.QPointF(point), QtCore.Qt.MoveAction, mime,
                                QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        # Exercise the actual drop handler; indicator belongs to the drag gesture.
        self.panel.drop_position = QtWidgets.QAbstractItemView.OnItem
        self.panel.drop_instances(event)
        Gui.updateGui()
        self.assertTrue(event.isAccepted())
        self.assertEqual(Model.owner(self.c), self.a.LinkedObject)

    def testDragEventsAboveSiblingAndMultiCutOrdering(self):
        self.row([self.c.ObjectId]).setSelected(True)
        mime = self.panel.move_mime()
        self.panel.tabs.setCurrentWidget(self.panel.structure)
        self.panel.resize(700, 550)
        Gui.updateGui()
        rect = self.panel.structure.visualItemRect(self.row([self.a.ObjectId]))
        point = QtCore.QPoint(rect.center().x(), rect.top() + 1)
        enter = QtGui.QDragEnterEvent(point, QtCore.Qt.MoveAction, mime,
                                     QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        move = QtGui.QDragMoveEvent(point, QtCore.Qt.MoveAction, mime,
                                   QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(self.panel.structure.viewport(), enter)
        QtWidgets.QApplication.sendEvent(self.panel.structure.viewport(), move)
        self.assertTrue(enter.isAccepted())
        self.assertTrue(move.isAccepted())
        self.assertEqual(self.panel.drop_position, QtWidgets.QAbstractItemView.AboveItem)
        drop = QtGui.QDropEvent(QtCore.QPointF(point), QtCore.Qt.MoveAction, mime,
                               QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtWidgets.QApplication.sendEvent(self.panel.structure.viewport(), drop)
        Gui.updateGui()
        self.assertTrue(drop.isAccepted())
        self.assertEqual(Model.children(self.root), [self.c, self.a, self.b])
        self.panel.structure.clearSelection()
        self.row([self.c.ObjectId]).setSelected(True)
        self.row([self.a.ObjectId]).setSelected(True)
        self.panel.cut_instances()
        self.panel.paste_instances(self.row())
        self.assertEqual(Model.children(self.root), [self.b, self.c, self.a])

    def testGroupedInstancesMoveWithoutCopies(self):
        second = Model.add_component(self.root, self.c.LinkedObject)
        identities = {self.c.ObjectId, second.ObjectId}
        self.panel.refresh()
        group = self.row([self.c.ObjectId])
        self.assertEqual(len(self.panel.members(group)), 2)
        group.setSelected(True)
        mime = self.panel.move_mime()
        self.panel.paste_instances(self.row([self.a.ObjectId]), mime)
        self.assertEqual({link.ObjectId for link in Model.children(self.a.LinkedObject)}, identities)
        self.assertEqual(Model.instance_counts(self.root)[self.c.LinkedObject], 2)
        self.assertEqual(len(Model.definitions(self.doc)), 4)
        self.panel.refresh()
        self.panel.grab().save(str(Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "part-tree-moved.png"))

    def testExistingNumbersAndRepeatedRebuilds(self):
        existing = Model.add_component(self.a.LinkedObject, self.c.LinkedObject)
        original = existing.InstanceNumber
        Model.move_instances(self.root, [(self.c.ObjectId,)], (self.a.ObjectId,), existing)
        self.assertEqual(existing.InstanceNumber, original)
        self.assertNotEqual(self.c.InstanceNumber, original)
        self.panel.refresh()
        for unused in range(8):
            self.panel.structure.clearSelection()
            self.row([self.a.ObjectId, self.c.ObjectId]).setSelected(True)
            self.panel.cut_instances()
            self.panel.paste_instances(self.row())
            self.panel.structure.clearSelection()
            self.row([self.c.ObjectId]).setSelected(True)
            self.panel.cut_instances()
            self.panel.paste_instances(self.row([self.a.ObjectId]))
            Gui.updateGui()
        self.assertEqual(existing.InstanceNumber, original)
        Model.validate(self.doc)

    def testDropBelowSiblingAndEmptySpace(self):
        self.row([self.a.ObjectId]).setSelected(True)
        mime = self.panel.move_mime()
        self.panel.paste_instances(self.row([self.b.ObjectId]), mime,
                                   QtWidgets.QAbstractItemView.BelowItem)
        self.assertEqual(Model.children(self.root), [self.b, self.a, self.c])
        self.panel.structure.clearSelection()
        self.row([self.c.ObjectId]).setSelected(True)
        self.panel.paste_instances(self.row([self.a.ObjectId]), self.panel.move_mime())
        self.panel.structure.clearSelection()
        self.row([self.a.ObjectId, self.c.ObjectId]).setSelected(True)
        self.panel.paste_instances(None, self.panel.move_mime(),
                                   QtWidgets.QAbstractItemView.OnViewport)
        self.assertEqual(Model.children(self.root), [self.b, self.a, self.c])
        self.assertEqual(Model.owner(self.c), self.root)

    def testAtomicCycleReferencesOverridesAndStaleClipboardRefusal(self):
        with self.assertRaisesRegex(ValueError, "top-level"):
            Model.move_instances(self.root, [()])
        with self.assertRaisesRegex(ValueError, "itself"):
            Model.move_instances(self.root, [(self.a.ObjectId,)], (self.a.ObjectId,))
        Model.set_representation(self.root, [self.c.ObjectId], "Full Component")
        with self.assertRaisesRegex(ValueError, "overrides"):
            Model.move_instances(self.root, [(self.c.ObjectId,)], (self.a.ObjectId,))
        Model.set_representation(self.root, [self.c.ObjectId])
        import Part
        shape = self.doc.addObject("Part::Feature", "Geometry")
        Model.register_object(self.c.LinkedObject, shape, "Object", True)
        shape.Shape = Part.makeBox(2, 3, 4)
        self.doc.recompute()
        reference = Model.add_reference(self.root, self.c, shape)
        with self.assertRaisesRegex(ValueError, "references"):
            Model.move_instances(self.root, [(self.c.ObjectId,)], (self.a.ObjectId,))
        Model.move_instances(self.root, [(self.c.ObjectId,)], (), self.a)
        self.assertEqual(reference.SourceOccurrence, self.c)
        self.assertAlmostEqual(reference.Shape.Volume, 24)
        self.assertEqual(Model.owner(self.c), self.root)
        self.panel.refresh()
        self.row([self.b.ObjectId]).setSelected(True)
        mime = self.panel.move_mime()
        Model.remove_instances([self.b])
        self.panel.refresh()
        with self.assertRaises(ValueError):
            self.panel.paste_instances(self.row(), mime)
        Model.validate(self.doc)
