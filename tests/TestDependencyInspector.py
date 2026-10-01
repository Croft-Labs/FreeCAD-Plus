# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native graph and installed dependency-inspection workflows."""
from pathlib import Path
import tempfile
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
import TechDraw
from PySide import QtCore, QtWidgets
from freecad.gui import DependencyInspector as Inspector


def make_fixture():
    doc = App.newDocument("DependencyWorkflow")
    doc.UndoMode = 1
    sketch = doc.addObject("Sketcher::SketchObject", "SharedProfile")
    sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 5))
    sketch.addConstraint(Sketcher.Constraint("Radius", 0, 5))
    for name, length in (("ShortExtrusion", 10), ("TallExtrusion", 20)):
        feature = doc.addObject("Part::Extrusion", name)
        feature.Base = sketch
        feature.DirMode = "Normal"
        feature.LengthFwd = length
        feature.Solid = True
    doc.recompute()
    fillet = doc.addObject("Part::Fillet", "EdgeFillet")
    fillet.Base = doc.ShortExtrusion
    rim = next(i for i, edge in enumerate(doc.ShortExtrusion.Shape.Edges, 1)
               if isinstance(edge.Curve, Part.Circle))
    fillet.Edges = [(rim, 0.5, 0.5)]
    drawing = doc.addObject("TechDraw::DrawViewPart", "DrawingView")
    drawing.Source = [fillet]
    doc.recompute()
    sketch.Visibility = False
    doc.ShortExtrusion.Visibility = False
    doc.TallExtrusion.Placement.Base.x = 15
    doc.recompute()
    return doc


class TestDependencyInspector(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = make_fixture()
        Gui.Selection.clearSelection()

    def tearDown(self):
        for dialog in list(Inspector._dialogs):
            dialog.close()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        Gui.updateGui()

    def launch(self, obj=None):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(obj or self.doc.SharedProfile)
        Gui.runCommand("Std_InspectDependencies")
        Gui.updateGui()
        return Inspector._dialogs[-1]

    def rows(self, root, direction="consumers", **options):
        return Inspector.inspect_graph(root, direction, **options)["rows"]

    def findRow(self, dialog, name, tab=1):
        dialog.tabs.setCurrentIndex(tab)
        table = dialog.tables[tab]
        for n in range(table.topLevelItemCount()):
            item = table.topLevelItem(n)
            if item.data(0, QtCore.Qt.UserRole)["key"][1] == name:
                table.setCurrentItem(item)
                return item
        self.fail("Missing dependency row: " + name)

    def testNativeSharedSketchFilletAndDrawing(self):
        for obj in (self.doc.ShortExtrusion, self.doc.TallExtrusion, self.doc.EdgeFillet):
            self.assertNotIn("Invalid", obj.State)
            self.assertGreater(obj.Shape.Volume, 0)
        graph = Inspector.inspect_graph(self.doc.SharedProfile, "consumers")
        self.assertFalse(graph["cycle"])
        self.assertFalse(graph["truncated"])
        rows = {row["key"][1]: row for row in graph["rows"]}
        self.assertEqual(rows["ShortExtrusion"]["depth"], 1)
        self.assertEqual(rows["TallExtrusion"]["depth"], 1)
        self.assertEqual(rows["EdgeFillet"]["depth"], 2)
        self.assertEqual(rows["DrawingView"]["depth"], 3)
        self.assertIn("Base", rows["ShortExtrusion"]["reason"])
        self.assertIn("Source", rows["DrawingView"]["reason"])
        inputs = self.rows(self.doc.DrawingView, "inputs")
        self.assertEqual({r["key"][1] for r in inputs},
                         {"EdgeFillet", "ShortExtrusion", "SharedProfile"})
        self.assertEqual({r["key"][1] for r in self.rows(self.doc.SharedProfile, transitive=False)},
                         {"ShortExtrusion", "TallExtrusion"})

    def testNativeExpressionsAndExternalLink(self):
        self.doc.TallExtrusion.setExpression("LengthFwd", "ShortExtrusion.LengthFwd * 2")
        self.doc.recompute()
        rows = self.rows(self.doc.TallExtrusion, "inputs")
        self.assertTrue(any("ExpressionEngine" in r["reason"] and "LengthFwd" in r["reason"] for r in rows))
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.doc.saveAs(str(Path(directory.name) / "Source.FCStd"))
        other = App.newDocument("OccurrenceDocument")
        other.saveAs(str(Path(directory.name) / "Occurrence.FCStd"))
        link = other.addObject("App::Link", "ExternalPart")
        link.setLink(self.doc.EdgeFillet)
        other.recompute()
        row = next(r for r in self.rows(link, "inputs") if r["key"][1] == "EdgeFillet")
        self.assertTrue(row["external"])
        self.assertIn("LinkedObject", row["reason"])
        downstream = self.rows(self.doc.EdgeFillet)
        self.assertTrue(any(r["key"] == Inspector.identity(link) and r["external"] for r in downstream))

    def testCyclesAndBoundedTraversal(self):
        one = self.doc.addObject("App::FeaturePython", "CycleOne")
        two = self.doc.addObject("App::FeaturePython", "CycleTwo")
        one.addProperty("App::PropertyLink", "Input")
        two.addProperty("App::PropertyLink", "Input")
        one.Input, two.Input = two, one
        # Inspect an invalid graph without triggering its execution.
        graph = Inspector.inspect_graph(one, "inputs")
        self.assertTrue(graph["cycle"])
        self.assertEqual(len(graph["rows"]), 2)
        graph = Inspector.inspect_graph(self.doc.SharedProfile, "consumers", max_edges=1)
        self.assertTrue(graph["truncated"])
        self.assertEqual(len(graph["rows"]), 1)
        self.assertTrue(Inspector.inspect_graph(self.doc.DrawingView, "inputs", max_depth=1)["truncated"])
        two.Input = None
        self.assertFalse(Inspector.inspect_graph(one, "inputs")["cycle"])

    def testCommandNavigationDoesNotChangeModelOrVisibility(self):
        def model_state():
            return [(o.Name, tuple(s for s in o.State if s in ("Touched", "Invalid")), o.Visibility)
                    for o in self.doc.Objects]
        before = model_state()
        shape = self.doc.EdgeFillet.Shape.exportBrepToString()
        dialog = self.launch()
        menu = next(m for m in Gui.getMainWindow().menuBar().findChildren(QtWidgets.QMenu)
                    if m.title().replace("&", "") == "Tools")
        self.assertIn("Inspect dependencies...", [a.text().replace("&", "") for a in menu.actions()])
        self.findRow(dialog, "EdgeFillet")
        dialog.selectButton.click()
        self.assertEqual(Gui.Selection.getSelection(), [self.doc.EdgeFillet])
        dialog.inspectButton.click()
        self.assertEqual(dialog.root, Inspector.identity(self.doc.EdgeFillet))
        self.findRow(dialog, "SharedProfile", tab=0)
        dialog.selectButton.click()
        self.assertEqual(Gui.Selection.getSelection(), [self.doc.SharedProfile])
        self.assertFalse(self.doc.SharedProfile.Visibility)
        dialog.close()
        # Native selection may expand tree items; that is presentation, not recompute state.
        self.assertEqual(model_state(), before)
        self.assertEqual(self.doc.EdgeFillet.Shape.exportBrepToString(), shape)
        self.assertFalse(self.doc.HasPendingTransaction)

    def testRefreshAfterEditUndoAndPersistence(self):
        dialog = self.launch()
        self.doc.openTransaction("Change consumer")
        self.doc.TallExtrusion.Base = None
        self.doc.recompute()
        self.doc.commitTransaction()
        self.assertFalse(dialog._fresh)
        self.assertFalse(dialog.selectButton.isEnabled())
        dialog.refreshButton.click()
        self.assertNotIn("TallExtrusion", {r["key"][1] for r in self.rows(self.doc.SharedProfile)})
        self.doc.undo()
        self.doc.recompute()
        self.assertFalse(dialog._fresh)
        dialog.refreshButton.click()
        self.findRow(dialog, "TallExtrusion")
        self.doc.SharedProfile.Label = "Renamed shared profile"
        self.assertFalse(dialog._fresh)
        dialog.refreshButton.click()
        self.assertIn("Renamed shared profile", dialog.heading.text())
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "Dependencies.FCStd")
            self.doc.saveAs(path)
            App.closeDocument(self.doc.Name)
            self.assertTrue(dialog._closed)
            self.doc = App.openDocument(path)
            self.assertEqual({r["key"][1] for r in self.rows(self.doc.SharedProfile)},
                             {"ShortExtrusion", "TallExtrusion", "EdgeFillet", "DrawingView"})

    def testBrokenSupportShowsNativeErrorAndRepair(self):
        plane = self.doc.addObject("Part::Plane", "Support")
        sketch = self.doc.SharedProfile
        sketch.AttachmentSupport = [(plane, "Face99")]
        sketch.MapMode = "FlatFace"
        self.doc.recompute()
        self.assertIn("Invalid", sketch.State)
        dialog = self.launch(self.doc.ShortExtrusion)
        self.findRow(dialog, "SharedProfile", tab=0)
        self.assertIn("Invalid", dialog.tables[0].currentItem().text(3))
        self.assertIn(sketch.getStatusString(), dialog.details.text())
        sketch.AttachmentSupport = [(plane, "Face1")]
        self.doc.recompute()
        self.assertFalse(dialog._fresh)
        dialog.refreshButton.click()
        self.assertNotIn("Invalid", sketch.State)
        self.findRow(dialog, "SharedProfile", tab=0)
        self.assertNotIn("Invalid", dialog.tables[0].currentItem().text(3))

    def testDeletionDoesNotRetargetAndRootCloseDetaches(self):
        dialog = self.launch()
        old = Inspector.identity(self.doc.TallExtrusion)
        self.findRow(dialog, "TallExtrusion")
        self.doc.removeObject("TallExtrusion")
        replacement = self.doc.addObject("Part::Extrusion", "TallExtrusion")
        self.assertNotEqual(replacement.ID, old[2])
        with self.assertRaises(ValueError):
            Inspector.resolve(old)
        self.assertFalse(dialog._fresh)
        self.assertEqual(dialog.tables[1].topLevelItemCount(), 0)
        self.doc.removeObject("SharedProfile")
        self.assertTrue(dialog._closed)
        self.assertNotIn(dialog, Inspector._dialogs)
