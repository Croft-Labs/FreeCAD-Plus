# SPDX-License-Identifier: LGPL-2.1-or-later
"""Temporary display acceptance on native Parts, Bodies and linked occurrences."""
from pathlib import Path
import tempfile
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtWidgets
from freecad.gui import TemporaryDisplay as Display


class TestTemporaryDisplay(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("TemporaryDisplayTest")
        self.doc.UndoMode = 1
        self.part = self.doc.addObject("App::Part", "Component")
        self.box = self.doc.addObject("Part::Box", "Box")
        self.part.addObject(self.box)
        self.body = self.doc.addObject("PartDesign::Body", "Body")
        self.part.addObject(self.body)
        self.body.Placement.Base.x = 14
        self.base = self.body.newObject("PartDesign::AdditiveBox", "Base")
        self.base.Length = self.base.Width = self.base.Height = 10
        self.hidden = self.doc.addObject("Part::Box", "Hidden")
        self.part.addObject(self.hidden)
        self.hidden.Visibility = False
        self.other = self.doc.addObject("Part::Box", "Other")
        self.other.Placement.Base.x = 30
        self.doc.recompute()
        Gui.Selection.clearSelection()

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.activeTaskDialog().reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()
        self.assertEqual(Display._stacks, {})

    def select(self, obj, subname=""):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(obj, subname)

    def visibility(self):
        return {obj.Name: obj.ViewObject.Visibility for obj in self.doc.Objects}

    def model(self):
        return (self.body.Tip.Name, self.base.Shape.Volume, self.box.Shape.Volume,
                tuple(self.box.Placement.toMatrix().A), tuple(obj.Name for obj in self.part.Group))

    def testMenuCommandsAndNestedRestore(self):
        actions = [action for menu in Gui.getMainWindow().menuBar().findChildren(QtWidgets.QMenu)
                   for action in menu.actions()]
        self.assertTrue(any("Temporarily isolate selection" in action.text() for action in actions))
        original = self.visibility()
        geometry = self.model()
        self.select(self.part)
        Gui.runCommand("Std_TemporaryIsolate")
        self.assertEqual(Display.depth(), 1)
        self.assertFalse(self.other.Visibility)
        self.assertFalse(self.hidden.Visibility)
        self.assertTrue(self.box.Visibility)
        isolated = self.visibility()
        self.select(self.body)
        Gui.runCommand("Std_TemporaryHide")
        self.assertFalse(self.body.Visibility)
        self.assertEqual(Display.depth(), 2)
        Gui.runCommand("Std_RestoreDisplay")
        self.assertEqual(self.visibility(), isolated)
        Gui.runCommand("Std_RestoreDisplay")
        self.assertEqual(self.visibility(), original)
        self.assertEqual(self.model(), geometry)
        self.assertFalse(Gui.Command.get("Std_RestoreDisplay").isActive())

    def testNestedIsolateAndRestoreAll(self):
        original = self.visibility()
        self.select(self.part)
        Display.apply("isolate")
        self.select(self.box, "Face1")
        Display.apply("isolate")
        self.assertEqual(Display.depth(), 2)
        self.assertTrue(self.part.Visibility)
        self.assertTrue(self.box.Visibility)
        self.assertFalse(self.body.Visibility)
        self.assertFalse(self.hidden.Visibility)
        Display.restore(all_levels=True)
        self.assertEqual(self.visibility(), original)
        self.assertEqual(Display.depth(), 0)

    def testBodyFeatureSelectsCurrentResult(self):
        original = self.visibility()
        tip = self.body.Tip
        self.select(self.base, "Face1")
        Display.apply("isolate")
        self.assertTrue(self.body.Visibility)
        self.assertTrue(self.part.Visibility)
        self.assertFalse(self.box.Visibility)
        self.assertEqual(self.body.Tip, tip)
        self.assertAlmostEqual(tip.Shape.Volume, 1000)
        Display.restore()
        self.assertEqual(self.visibility(), original)

    def testWholeLinkedOccurrenceAndSourcePreserved(self):
        link = self.doc.addObject("App::Link", "Occurrence")
        link.setLink(self.part)
        link.Placement.Base.x = 60
        self.doc.recompute()
        original = self.visibility()
        placement = tuple(link.Placement.toMatrix().A)
        self.select(link, "Box.Face1")
        Display.apply("isolate")
        self.assertTrue(link.Visibility)
        self.assertFalse(self.part.Visibility)
        self.assertTrue(self.box.Visibility)
        self.assertTrue(self.body.Visibility)
        self.assertFalse(self.hidden.Visibility)
        self.assertEqual(link.LinkedObject, self.part)
        self.assertEqual(tuple(link.Placement.toMatrix().A), placement)
        Display.restore()
        self.assertEqual(self.visibility(), original)

    def testCreatedDeletedAndReusedNames(self):
        self.select(self.part)
        Display.apply("isolate")
        deleted_name, deleted_id = self.other.Name, self.other.ID
        self.doc.removeObject(deleted_name)
        replacement = self.doc.addObject("Part::Box", deleted_name)
        replacement.Visibility = False
        added = self.doc.addObject("Part::Box", "Added")
        added.Visibility = True
        self.doc.recompute()
        self.assertNotEqual(replacement.ID, deleted_id)
        Display.restore()
        self.assertFalse(replacement.Visibility)
        self.assertTrue(added.Visibility)
        self.assertTrue(self.part.Visibility)

    def testDocumentIsolationAndCloseCleanup(self):
        self.select(self.part)
        Display.apply("isolate")
        second = App.newDocument("SecondDisplay")
        obj = second.addObject("Part::Box", "Box")
        second.recompute()
        self.assertEqual(Display.depth(), 0)
        self.select(obj)
        Display.apply("hide")
        self.assertEqual(Display.depth(), 1)
        App.setActiveDocument(self.doc.Name)
        Display.restore()
        self.assertTrue(self.other.Visibility)
        self.assertFalse(obj.Visibility)
        App.closeDocument(second.Name)
        self.assertNotIn("SecondDisplay", Display._stacks)
        again = App.newDocument("SecondDisplay")
        self.assertEqual(Display.depth(again), 0)

    def testInvalidContextDoesNotMutateOrPush(self):
        original = self.visibility()
        with self.assertRaisesRegex(ValueError, "Select objects"):
            Display.apply("isolate")
        self.select(self.box)
        self.doc.openTransaction("Pending modeling edit")
        self.box.Length = 15
        with self.assertRaisesRegex(ValueError, "pending edit"):
            Display.apply("hide")
        self.doc.abortTransaction()
        self.doc.recompute()
        second = App.newDocument("ForeignSelection")
        foreign = second.addObject("Part::Box", "Foreign")
        second.recompute()
        App.setActiveDocument(self.doc.Name)
        self.select(foreign)
        with self.assertRaisesRegex(ValueError, "active document"):
            Display.apply("hide")
        self.assertEqual(self.visibility(), original)
        self.assertEqual(Display.depth(self.doc), 0)

    def testNoOpAndRestoredSaveReopen(self):
        self.select(self.hidden)
        self.assertFalse(Display.apply("hide"))
        self.assertEqual(Display.depth(), 0)
        original, geometry = self.visibility(), self.model()
        self.select(self.part)
        Display.apply("isolate")
        Display.restore()
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "RestoredDisplay.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.assertEqual(self.visibility(), original)
            self.assertEqual(Display.depth(), 0)
            self.assertEqual(self.doc.Body.Tip.Name, geometry[0])
            self.assertAlmostEqual(self.doc.Base.Shape.Volume, geometry[1])

    def testModelUndoAndOrdinaryHideRemainIndependent(self):
        self.doc.openTransaction("Resize box")
        self.box.Length = 20
        self.doc.recompute()
        self.doc.commitTransaction()
        original = self.visibility()
        self.select(self.part)
        Display.apply("isolate")
        self.select(self.body)
        Gui.runCommand("Std_HideSelection")
        self.assertFalse(self.body.Visibility)
        Display.restore()
        self.assertEqual(self.visibility(), original)
        self.assertAlmostEqual(self.box.Length.Value, 20)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(self.box.Length.Value, 10)
        self.doc.redo()
        self.doc.recompute()
        self.assertAlmostEqual(self.box.Length.Value, 20)
