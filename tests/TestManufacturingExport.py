# SPDX-License-Identifier: LGPL-2.1-or-later
"""Dimensioned STL handoff, occurrence placement and reusable quality acceptance."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Mesh
import Part
from PySide import QtWidgets
import ManufacturingExport as Export
import ManufacturingExportGui as Editor


class TestManufacturingExport(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("ManufacturingExportTest")
        self.box = self.doc.addObject("Part::Box", "Box")
        self.box.Length, self.box.Width, self.box.Height = 12, 8, 6
        self.doc.recompute()
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "part.stl"
        Gui.Selection.clearSelection()
        self.old_presets = App.ParamGet(Export.PREFS).GetString("Presets", "{}")
        Export.reset_presets()

    def tearDown(self):
        for dialog in list(Editor._dialogs):
            dialog.close()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        App.ParamGet(Export.PREFS).SetString("Presets", self.old_presets)
        Gui.updateGui()

    def export(self, objects=None, **kwargs):
        return Export.export_stl(objects or [self.box], str(self.path), **kwargs)

    def mesh_bounds(self):
        mesh = Mesh.Mesh(str(self.path))
        self.assertTrue(mesh.isSolid())
        bounds = mesh.BoundBox
        return mesh, (bounds.XMin, bounds.YMin, bounds.ZMin, bounds.XMax, bounds.YMax, bounds.ZMax)

    def testDimensionsAndNestedWorldPlacement(self):
        part = self.doc.addObject("App::Part", "Part")
        part.addObject(self.box)
        part.Placement = App.Placement(App.Vector(20, 10, 5), App.Rotation(App.Vector(0, 0, 1), 90))
        self.box.Placement.Base = App.Vector(2, 3, 4)
        self.doc.recompute()
        original_objects = [(obj.Name, obj.ID) for obj in self.doc.Objects]
        report = self.export()
        mesh, bounds = self.mesh_bounds()
        for actual, expected in zip(bounds, (9, 12, 9, 17, 24, 15)):
            self.assertAlmostEqual(actual, expected, places=5)
        self.assertAlmostEqual(mesh.Volume, 12 * 8 * 6, places=4)
        self.assertEqual(report["units"], "mm")
        self.assertEqual(report["frame"], "World")
        self.assertEqual(report["objects"], ["Box"])
        self.assertEqual([(obj.Name, obj.ID) for obj in self.doc.Objects], original_objects)

    def testSelectedOccurrencesKeepTransformsAndExcludeSource(self):
        first = self.doc.addObject("App::Link", "First")
        second = self.doc.addObject("App::Link", "Second")
        for link, x in ((first, 30), (second, 60)):
            link.setLink(self.box)
            link.Placement = App.Placement(App.Vector(x, 0, 0), App.Rotation(App.Vector(0, 0, 1), 90))
        self.doc.recompute()
        report = self.export([first, second])
        mesh, bounds = self.mesh_bounds()
        for actual, expected in zip(bounds, (22, 0, 0, 60, 12, 6)):
            self.assertAlmostEqual(actual, expected, places=5)
        self.assertAlmostEqual(mesh.Volume, 2 * 12 * 8 * 6, places=4)
        self.assertEqual(report["objects"], ["First", "Second"])
        self.assertEqual(first.LinkedObject, self.box)
        self.assertAlmostEqual(self.box.Shape.Volume, 576)

    def testCoarseAndFineRoundTrip(self):
        sphere = self.doc.addObject("Part::Sphere", "Sphere")
        sphere.Radius = 10
        self.doc.recompute()
        coarse = self.export([sphere], linear=0.5, angular=30)
        coarse_mesh = Mesh.Mesh(str(self.path))
        fine = self.export([sphere], linear=0.02, angular=5, overwrite=True)
        fine_mesh, bounds = self.mesh_bounds()
        self.assertGreater(fine["facets"], coarse["facets"])
        exact = sphere.Shape.Volume
        self.assertLess(abs(fine_mesh.Volume - exact), abs(coarse_mesh.Volume - exact))
        for actual, expected in zip(bounds, (-10, -10, -10, 10, 10, 10)):
            self.assertAlmostEqual(actual, expected, delta=0.03)

    def testStaleAndUnsupportedInputsPreserveExistingFile(self):
        self.path.write_bytes(b"existing output")
        self.box.Length = 20
        with self.assertRaisesRegex(ValueError, "not current"):
            self.export(overwrite=True)
        self.assertEqual(self.path.read_bytes(), b"existing output")
        self.doc.recompute()
        part = self.doc.addObject("App::Part", "Container")
        with self.assertRaisesRegex(ValueError, "individual solids"):
            self.export([part], overwrite=True)
        self.assertEqual(self.path.read_bytes(), b"existing output")
        with self.assertRaises(FileExistsError):
            self.export()
        self.assertFalse(list(self.path.parent.glob(".freecad-export-*")))

    def testMixedSolidAndLooseGeometryIsDisclosed(self):
        mixed = self.doc.addObject("Part::Feature", "MixedInput")
        mixed.Shape = Part.makeCompound([
            self.box.Shape, Part.makeLine(App.Vector(30, 0, 0), App.Vector(40, 0, 0))])
        self.doc.recompute()
        self.path.write_bytes(b"keep existing output")
        with self.assertRaisesRegex(ValueError, "solid-only"):
            self.export([mixed], overwrite=True)
        self.assertEqual(self.path.read_bytes(), b"keep existing output")

    def testQualityValidationPresetsAndReset(self):
        for values in ((0, 10), (float("nan"), 10), (0.1, float("inf")), (0.1, 0)):
            with self.assertRaises(ValueError):
                self.export(linear=values[0], angular=values[1])
        self.assertFalse(self.path.exists())
        Export.save_preset("Printer", 0.05, 8)
        self.assertEqual(Export.presets()["Printer"], (0.05, 8))
        self.assertNotIn("objects", App.ParamGet(Export.PREFS).GetString("Presets"))
        with self.assertRaises(ValueError):
            Export.save_preset("Fine", 0.1, 5)
        Export.reset_presets()
        self.assertEqual(Export.presets(), Export.DEFAULTS)

    def testMenuDialogFrozenSelectionAndCorrection(self):
        actions = [action for menu in Gui.getMainWindow().menuBar().findChildren(QtWidgets.QMenu)
                   for action in menu.actions()]
        self.assertTrue(any("Manufacturing export" in action.text() for action in actions))
        Gui.Selection.addSelection(self.box, "Face1")
        Gui.runCommand("Part_ManufacturingExport")
        dialog = Editor._dialogs[-1]
        self.assertFalse(dialog.exportButton.isEnabled())
        self.assertIn("whole objects", dialog.status.text())
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.box)
        dialog.useSelection.click()
        self.assertTrue(dialog.exportButton.isEnabled())
        self.assertIn("12.000 x 8.000 x 6.000 mm", dialog.inputs.toPlainText())
        other = self.doc.addObject("Part::Sphere", "Unrelated")
        self.doc.recompute()
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(other)
        dialog.path.setText(str(self.path))
        dialog.exportButton.click()
        self.assertIn("Exported", dialog.status.text())
        mesh, bounds = self.mesh_bounds()
        self.assertAlmostEqual(mesh.Volume, 576)
        before = self.path.read_bytes()
        with patch.object(QtWidgets.QMessageBox, "question", return_value=QtWidgets.QMessageBox.No):
            dialog.exportButton.click()
        self.assertEqual(self.path.read_bytes(), before)
        dialog.presetName.setText("Workshop")
        dialog.linear.setValue(0.03)
        dialog.savePreset.click()
        self.assertEqual(Export.presets()["Workshop"][0], 0.03)
        dialog.close()
        Gui.runCommand("Part_ManufacturingExport")
        self.assertGreaterEqual(Editor._dialogs[-1].preset.findText("Workshop"), 0)

    def testDeletedInputCannotRetargetReusedName(self):
        Gui.Selection.addSelection(self.box)
        Gui.runCommand("Part_ManufacturingExport")
        dialog = Editor._dialogs[-1]
        dialog.path.setText(str(self.path))
        self.doc.removeObject("Box")
        self.doc.addObject("Part::Box", "Box")
        self.doc.recompute()
        dialog.exportButton.click()
        self.assertFalse(self.path.exists())
        self.assertNotIn("Exported", dialog.status.text())

    def testWholeNestedTreeSelectionAndLinkedMemberGate(self):
        part = self.doc.addObject("App::Part", "Part")
        part.addObject(self.box)
        link = self.doc.addObject("App::Link", "LinkedPart")
        link.setLink(part)
        self.doc.recompute()
        Gui.Selection.addSelection(part, "Box.")
        Gui.runCommand("Part_ManufacturingExport")
        dialog = Editor._dialogs[-1]
        self.assertEqual(dialog.targets, (self.box,))
        self.assertTrue(dialog.exportButton.isEnabled())
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(link, "Box.")
        dialog.useSelection.click()
        self.assertFalse(dialog.exportButton.isEnabled())
        self.assertIn("whole local occurrence", dialog.status.text())
