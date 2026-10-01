# SPDX-License-Identifier: LGPL-2.1-or-later
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore


def settle():
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(1800, loop.quit)
    loop.exec_()
    Gui.updateGui()


def make_fixture():
    doc = App.newDocument("DrawingSetup")
    doc.UndoMode = 1
    box = doc.addObject("Part::Box", "Blank")
    box.Length, box.Width, box.Height = 40, 25, 12
    hole = doc.addObject("Part::Cylinder", "Bore")
    hole.Radius, hole.Height = 4, 12
    hole.Placement.Base = App.Vector(10, 10, 0)
    result = doc.addObject("Part::Cut", "Bracket")
    result.Base, result.Tool = box, hole
    doc.recompute()
    box.Visibility = hole.Visibility = False
    doc.recompute()
    return doc


class TestDrawingSetup(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("TechDrawWorkbench")
        from TechDrawTools import DrawingSetup
        self.setup = DrawingSetup
        self.doc = make_fixture()

    def tearDown(self):
        for dialog in list(self.setup._dialogs):
            dialog.reject()
        Gui.Selection.clearSelection()
        settle()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def launch(self):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.doc.Bracket)
        Gui.runCommand("TechDraw_DrawingSetup")
        Gui.updateGui()
        return self.setup._dialogs[-1]

    def create(self, **changes):
        kwargs = dict(source=self.doc.Bracket, expected=self.setup.review(self.doc.Bracket),
                      template="A4 landscape", scale=1., orientation=list(self.setup.ORIENTATIONS)[0],
                      convention="Third angle", projected=True)
        kwargs.update(changes)
        page = self.setup.create_drawing(**kwargs)
        settle()
        return page

    def width(self, view):
        edges = view.getVisibleEdges()
        self.assertTrue(edges)
        return Part.makeCompound(edges).BoundBox.XLength

    def testInstalledCommandAndProjectedGeometry(self):
        volume = self.doc.Bracket.Shape.Volume
        dialog = self.launch()
        self.assertTrue(dialog.createButton.isEnabled(), dialog.message.text())
        dialog.convention.setCurrentText("Third angle")
        dialog.createButton.click()
        self.assertTrue(dialog.closed, dialog.message.text())
        settle()
        page = dialog.page
        group = page.Views[0]
        self.assertEqual(len(group.Views), 3)
        self.assertEqual(group.Source, [self.doc.Bracket])
        self.assertEqual(str(group.ProjectionType), "Third angle")
        self.assertAlmostEqual(self.width(group.Anchor), 40, places=5)
        top, right = group.getItemByLabel("Top"), group.getItemByLabel("Right")
        self.assertGreater(top.Y.Value, 0)
        self.assertGreater(right.X.Value, 0)
        self.assertTrue(top.getVisibleEdges())
        self.assertAlmostEqual(self.doc.Bracket.Shape.Volume, volume)
        self.assertTrue(self.doc.Bracket.Visibility)

    def testFirstAngleScaleAndSingleViewOrientation(self):
        page = self.create(convention="First angle", scale=0.5)
        group = page.Views[0]
        self.assertAlmostEqual(self.width(group.Anchor), 20, places=5)
        self.assertLess(group.getItemByLabel("Top").Y.Value, 0)
        self.assertLess(group.getItemByLabel("Right").X.Value, 0)
        other = self.create(template="A3 landscape", projected=False,
                            orientation=list(self.setup.ORIENTATIONS)[1])
        self.assertEqual(len(other.Views[0].Views), 1)
        self.assertEqual(other.Views[0].Anchor.Direction, App.Vector(0, 0, 1))
        self.assertAlmostEqual(other.Template.Width, 420)

    def testEditUndoRedoAndReopen(self):
        original = {obj.Name for obj in self.doc.Objects}
        page = self.create()
        name = page.Name
        self.doc.undo()
        self.doc.recompute()
        settle()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, original)
        self.doc.redo()
        self.doc.recompute()
        settle()
        self.doc.Blank.Length = 50
        self.doc.recompute()
        settle()
        self.assertAlmostEqual(self.width(self.doc.getObject(name).Views[0].Anchor), 50, places=5)
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "Drawing.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.doc.recompute()
            settle()
            group = self.doc.getObject(name).Views[0]
            self.assertEqual(group.Source, [self.doc.Bracket])
            self.assertEqual(str(group.ProjectionType), "Third angle")
            self.doc.Blank.Length = 45
            self.doc.recompute()
            settle()
            self.assertAlmostEqual(self.width(group.Anchor), 45, places=5)

    def testCancelStaleAndOwnerTransaction(self):
        names = {obj.Name for obj in self.doc.Objects}
        dialog = self.launch()
        dialog.reject()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
        dialog = self.launch()
        self.doc.Blank.Length = 45
        self.assertFalse(dialog.createButton.isEnabled())
        self.doc.recompute()
        dialog.refresh()
        self.assertTrue(dialog.createButton.isEnabled())
        self.doc.openTransaction("Owner edit")
        self.doc.Bracket.Label = "Owner label"
        with self.assertRaisesRegex(ValueError, "transaction"):
            self.create()
        self.assertTrue(self.doc.HasPendingTransaction)
        self.doc.abortTransaction()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
        self.doc.removeObject("Bracket")
        self.assertTrue(dialog.closed)

    def testInvalidOptionsAndAtomicFailure(self):
        names = {obj.Name for obj in self.doc.Objects}
        for scale in (0, -1, float("nan"), 10):
            with self.assertRaises(ValueError):
                self.create(scale=scale)
        with patch.object(self.setup.Path, "is_file", return_value=False):
            with self.assertRaisesRegex(ValueError, "missing"):
                self.create()
        # Fail after Page/template/group creation, while setting the anchor direction.
        with patch.object(self.setup.App, "Vector", side_effect=RuntimeError("injected")):
            with self.assertRaisesRegex(RuntimeError, "injected"):
                self.create()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, names)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.assertEqual(len(self.create().Views[0].Views), 3)

    def testUnsupportedAndStaleSource(self):
        expected = self.setup.review(self.doc.Bracket)
        self.doc.Blank.Length = 41
        with self.assertRaises(ValueError):
            self.setup.review(self.doc.Bracket)
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "changed"):
            self.create(expected=expected)
        container = self.doc.addObject("App::Part", "Container")
        container.addObject(self.doc.Bracket)
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "root"):
            self.setup.review(self.doc.Bracket)

    def testWholeBodyPreservesTipAndSourcePlacement(self):
        body = self.doc.addObject("PartDesign::Body", "Body")
        tip = body.newObject("PartDesign::Feature", "BodyResult")
        tip.Shape = Part.makeBox(20, 15, 8)
        body.Tip = tip
        body.Placement.Base = App.Vector(7, 4, 2)
        self.doc.recompute()
        before = App.Placement(body.Placement)
        page = self.create(source=body, expected=self.setup.review(body), projected=False)
        self.assertEqual(page.Views[0].Source, [body])
        self.assertAlmostEqual(self.width(page.Views[0].Anchor), 20, places=5)
        self.assertEqual(body.Placement, before)
        self.assertEqual(body.Tip, tip)
