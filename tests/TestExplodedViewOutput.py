# SPDX-License-Identifier: LGPL-2.1-or-later
"""Saved native exploded-view geometry, sequence and drawing consumer checks."""
from pathlib import Path
import tempfile
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import CommandCreateView as Editor
import UtilsAssembly


def fixture():
    doc = App.newDocument("ExplodedOutput")
    doc.UndoMode = 1
    source = doc.addObject("Part::Box", "Definition")
    source.Length, source.Width, source.Height = 12, 8, 5
    source.Placement = App.Placement(App.Vector(4, 3, 2), App.Rotation(App.Vector(0, 0, 1), 20))
    assembly = doc.addObject("Assembly::AssemblyObject", "Product")
    for name, x in (("First", 0), ("Second", 25)):
        link = assembly.newObject("App::Link", name)
        link.setLink(source)
        link.LinkTransform = True
        link.LinkPlacement = App.Placement(App.Vector(x, 0, 0), App.Rotation())
    source.Visibility = False
    group = UtilsAssembly.getViewGroup(assembly)
    view = group.newObject("App::FeaturePython", "ExplodedView")
    Editor.ExplodedView(view)
    Editor.ViewProviderExplodedView(view.ViewObject)
    doc.recompute()
    return doc, assembly, view


def add_move(doc, assembly, view, target, vector, radial=False, rotation=None):
    move = assembly.newObject("App::FeaturePython", "Move")
    Editor.ExplodedViewStep(move, int(radial))
    Editor.ViewProviderExplodedViewStep(move.ViewObject)
    move.References = (assembly, [target.Name + "."])
    move.MovementTransform = App.Placement(vector, rotation or App.Rotation())
    view.addObject(move)
    move.Visibility = False
    doc.recompute()
    return move


class TestExplodedViewOutput(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("AssemblyWorkbench")
        self.doc, self.assembly, self.view = fixture()

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.closeDialog()
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def assertVector(self, actual, expected):
        self.assertLess((actual - expected).Length, 1e-6)

    def snapshot(self):
        return [(obj.Name, obj.Placement.toMatrix().A, obj.Visibility,
                 obj.Shape.exportBrepToString())
                for obj in (self.doc.Definition, self.doc.First, self.doc.Second)]

    def test_group_owner_and_occurrence_definition_transform(self):
        self.assertEqual(self.view.Proxy.getAssembly(self.view), self.assembly)
        for use_source in (False, True):
            self.doc.First.LinkTransform = use_source
            self.doc.recompute()
            before = self.snapshot()
            shape = self.view.Proxy.getExplodedShape(self.view)
            self.assertEqual(len(shape.Solids), 2)
            self.assertVector(shape.Solids[0].CenterOfGravity, self.doc.First.Shape.CenterOfGravity)
            self.assertVector(shape.Solids[1].CenterOfGravity, self.doc.Second.Shape.CenterOfGravity)
            self.assertEqual(self.snapshot(), before)

    def test_repeated_moves_trails_and_preview_agree(self):
        first = self.doc.First
        initial = first.Shape.BoundBox.Center
        add_move(self.doc, self.assembly, self.view, first, App.Vector(10, 0, 0))
        add_move(self.doc, self.assembly, self.view, first, App.Vector(0, 15, 0))
        before = self.snapshot()
        placements, lines = self.view.Proxy._calculateExplodedPlacements(self.view)
        self.assertVector(lines[0][0], initial)
        self.assertVector(lines[0][1], initial + App.Vector(10, 0, 0))
        self.assertVector(lines[1][0], lines[0][1])
        self.assertVector(lines[1][1], initial + App.Vector(10, 15, 0))
        result = self.view.Proxy.getExplodedShape(self.view)
        self.assertEqual(self.snapshot(), before)
        saved = UtilsAssembly.saveAssemblyPartsPlacements(self.assembly)
        self.view.Proxy.applyMoves(self.view)
        self.assertEqual(first.Placement, placements[first])
        self.assertVector(result.Solids[0].CenterOfGravity, first.Shape.CenterOfGravity)
        UtilsAssembly.restoreAssemblyPartsPlacements(self.assembly, saved)
        for step in self.view.Group:
            step.Visibility = False
        self.assertEqual(self.snapshot(), before)

    def test_rotation_and_transformed_parent(self):
        container = self.doc.addObject("App::Part", "Container")
        container.addObject(self.assembly)
        container.Placement = App.Placement(App.Vector(100, 10, 0), App.Rotation(App.Vector(0, 0, 1), 35))
        self.assembly.Placement = App.Placement(App.Vector(7, 9, 2), App.Rotation(App.Vector(1, 0, 0), 25))
        add_move(self.doc, self.assembly, self.view, self.doc.First, App.Vector(10, 0, 0))
        add_move(self.doc, self.assembly, self.view, self.doc.First, App.Vector(), rotation=App.Rotation(App.Vector(0, 0, 1), 40))
        before = self.snapshot()
        result = self.view.Proxy.getExplodedShape(self.view)
        _, lines = self.view.Proxy._calculateExplodedPlacements(self.view)
        self.assertVector(lines[0][1], lines[1][0])
        self.view.Proxy.applyMoves(self.view)
        expected = self.doc.First.Shape.copy()
        expected.Placement = container.Placement * self.assembly.Placement * expected.Placement
        self.assertVector(result.Solids[0].CenterOfGravity, expected.CenterOfGravity)
        self.assertVector(lines[-1][1], expected.BoundBox.Center)
        self.assertNotEqual(self.snapshot(), before)

    def test_sequential_radial_moves_match_live_preview(self):
        self.assembly.Placement = App.Placement(App.Vector(100, 20, 5), App.Rotation(App.Vector(0, 0, 1), 90))
        add_move(self.doc, self.assembly, self.view, self.doc.First, App.Vector(5, 0, 0))
        add_move(self.doc, self.assembly, self.view, self.doc.First, App.Vector(3, 0, 0), radial=True)
        add_move(self.doc, self.assembly, self.view, self.doc.First, App.Vector(2, 0, 0), radial=True)
        Gui.updateGui()
        calculated, lines = self.view.Proxy._calculateExplodedPlacements(self.view)
        self.assertVector(lines[0][1], lines[1][0])
        self.assertVector(lines[1][1], lines[2][0])
        com, size = UtilsAssembly.getComAndSize(self.assembly)
        self.view.Proxy.applyMoves(self.view, com, size)
        self.assertVector(self.doc.First.Placement.Base, calculated[self.doc.First].Base)

    def test_visibility_identity_and_zero_length_trail(self):
        self.doc.First.Label = self.doc.Second.Label = "Same label"
        self.doc.Second.Visibility = False
        add_move(self.doc, self.assembly, self.view, self.doc.First, App.Vector())
        shape = self.view.Proxy.getExplodedShape(self.view)
        self.assertEqual(len(shape.Solids), 1)
        self.assertEqual(len(shape.Edges), 12)
        self.assertVector(shape.CenterOfGravity, self.doc.First.Shape.CenterOfGravity)

    def test_missing_reference_is_reported_not_silently_omitted(self):
        move = add_move(self.doc, self.assembly, self.view, self.doc.First, App.Vector(10, 0, 0))
        move.References = (self.assembly, ["MissingOccurrence."])
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "unavailable part"):
            self.view.Proxy.getExplodedShape(self.view)
        self.assertEqual(self.snapshot(), before)

    def test_undo_redo_and_reopen_preserve_assembled_state(self):
        before = self.snapshot()
        self.doc.openTransaction("Add exploded movement")
        add_move(self.doc, self.assembly, self.view, self.doc.First, App.Vector(20, 0, 0))
        self.doc.commitTransaction()
        center = self.view.Proxy.getExplodedShape(self.view).Solids[0].CenterOfGravity
        self.doc.undo()
        self.assertEqual(len(self.view.Group), 0)
        self.doc.redo()
        self.assertVector(self.view.Proxy.getExplodedShape(self.view).Solids[0].CenterOfGravity, center)
        self.assertEqual(self.snapshot(), before)
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "Exploded.FCStd")
            self.doc.recompute()
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(path)
            self.assembly, self.view = self.doc.Product, self.doc.ExplodedView
            self.assertEqual(self.snapshot(), before)
            self.assertVector(self.view.Proxy.getExplodedShape(self.view).Solids[0].CenterOfGravity, center)

    def test_native_task_accept_and_cancel_restore_assembled_state(self):
        move = add_move(self.doc, self.assembly, self.view, self.doc.First, App.Vector(20, 0, 0))
        before = self.snapshot()
        Gui.activeDocument().setEdit(self.assembly.Name)
        task = Editor.TaskAssemblyCreateView(self.view)
        Gui.Control.showDialog(task)
        Gui.updateGui()
        self.assertNotEqual(self.snapshot(), before)
        task.accept()
        self.assertEqual(self.snapshot(), before)
        task = Editor.TaskAssemblyCreateView(self.view)
        Gui.Control.showDialog(task)
        move.MovementTransform = App.Placement(App.Vector(50, 0, 0), App.Rotation())
        task.onMovesChanged()
        task.reject()
        self.assertVector(move.MovementTransform.Base, App.Vector(20, 0, 0))
        self.assertEqual(self.snapshot(), before)
        Gui.activeDocument().resetEdit()

    def test_native_techdraw_uses_explicit_saved_view(self):
        import TechDraw
        add_move(self.doc, self.assembly, self.view, self.doc.First, App.Vector(-30, 0, 0))
        before = self.snapshot()
        drawing = self.doc.addObject("TechDraw::DrawViewPart", "Drawing")
        page = self.doc.addObject("TechDraw::DrawPage", "Page")
        template = self.doc.addObject("TechDraw::DrawSVGTemplate", "Template")
        template.Template = App.getResourceDir() + "Mod/TechDraw/Templates/ISO/A4_Landscape_ISO5457_notitleblock.svg"
        page.Template = template
        page.addView(drawing)
        drawing.Source = [self.view]
        drawing.Direction = App.Vector(0, 0, 1)
        self.doc.recompute()
        drawing.recompute()
        from PySide import QtCore
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(1800, loop.quit)
        loop.exec_()
        Gui.updateGui()
        self.assertNotIn("Invalid", drawing.State)
        edges = drawing.getVisibleEdges()
        self.assertGreater(len(edges), 0)
        bounds = Part.makeCompound(edges).BoundBox
        expected = self.view.Proxy.getExplodedShape(self.view).BoundBox
        self.assertAlmostEqual(bounds.XLength, expected.XLength, places=5)
        self.assertEqual(self.snapshot(), before)
