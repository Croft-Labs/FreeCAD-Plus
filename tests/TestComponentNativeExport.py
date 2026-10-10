# SPDX-License-Identifier: LGPL-2.1-or-later
"""Real native export entry points, not adapter-only calls."""
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Mesh
import Import
import ImportGui
import CadDocument
import ComponentModel as Model
import TestComponentOutput as Fixture
from PySide import QtCore, QtWidgets


class TestComponentNativeExport(unittest.TestCase):
    setUp = Fixture.TestComponentOutput.setUp
    tearDown = Fixture.TestComponentOutput.tearDown
    box = Fixture.TestComponentOutput.box

    def prepare(self):
        Model.set_part_types(self.root, [(self.link, "Reference")])
        Model.add_reference(self.root, self.link, self.body)

    def check_step(self, path):
        shape = Part.read(str(path))
        self.assertEqual(len(shape.Solids), 2)
        self.assertAlmostEqual(shape.Volume, 36)

    def testDirectPartExport(self):
        self.prepare()
        path = self.output / "native-part.step"
        Part.export([self.root], str(path))
        self.check_step(path)

    def testDirectImportKeywordsAndLegacy(self):
        self.prepare()
        for legacy in (False, True):
            path = self.output / ("native-import-" + str(legacy) + ".step")
            Import.export(obj=[self.root], name=str(path), exportHidden=True,
                          legacy=legacy, keepPlacement=True)
            self.check_step(path)

    def testDirectImportGuiOptions(self):
        self.prepare()
        path = self.output / "native-import-gui.step"
        ImportGui.export([self.root], str(path),
                         {"exportHidden": True, "legacy": False, "keepPlacement": True})
        self.check_step(path)

    def testDirectMeshKeywords(self):
        self.prepare()
        path = self.output / "native-mesh.stl"
        Mesh.export(objectList=[self.root], filename=str(path), tolerance=0.05)
        mesh = Mesh.Mesh(str(path))
        self.assertTrue(mesh.isSolid())
        self.assertAlmostEqual(abs(mesh.Volume), 36, places=4)

    def testAllWritersRefuseExcludedBeforeCreatingOutput(self):
        Model.set_part_types(self.root, [(self.link, "Excluded")])
        names = set(App.listDocuments())
        for writer, suffix in ((Part, ".step"), (Import, ".step"),
                               (ImportGui, ".step"), (Mesh, ".stl")):
            path = self.output / (writer.__name__ + "-excluded" + suffix)
            with self.subTest(writer=writer.__name__):
                with self.assertRaises(Exception):
                    writer.export([self.link], str(path))
                self.assertFalse(path.exists())
                self.assertEqual(set(App.listDocuments()), names)

    def testOrdinaryObjectsBypassAdapter(self):
        ordinary = App.newDocument("OrdinaryExport")
        body = ordinary.addObject("Part::Feature", "Box")
        body.Shape = Part.makeBox(2, 3, 4)
        ordinary.recompute()
        with patch.object(Model, "export_objects", side_effect=AssertionError("unexpected routing")):
            for writer, suffix in ((Part, ".step"), (Import, ".step"),
                                   (ImportGui, ".step"), (Mesh, ".stl")):
                path = self.output / (writer.__name__ + "-ordinary" + suffix)
                writer.export([body], str(path))
                self.assertTrue(path.is_file())

    def testWriterFailureRestoresDocumentAndCleansScratch(self):
        self.prepare()
        names = set(App.listDocuments())
        path = self.output / "missing-directory" / "failure.step"
        with self.assertRaises(Exception):
            Part.export([self.root], str(path))
        self.assertEqual(set(App.listDocuments()), names)
        self.assertEqual(App.ActiveDocument, self.doc)

    def testNativeSaveRetainsReferences(self):
        self.prepare()
        path = self.output / "native-save.cadprt"
        self.doc.saveAs(str(path))
        data = CadDocument.preflight(path)
        self.assertIn("component-part-types-v1", data["required"])
        self.assertEqual(Model.part_type(self.root, self.link), "Reference")
        self.assertEqual(len(Model.history(self.child)), 1)

    def testColorTuplesCannotBypassPolicy(self):
        self.prepare()
        path = self.output / "tuple.step"
        with self.assertRaisesRegex(ValueError, "face-color tuples"):
            Import.export([(self.root, [(1.0, 0.0, 0.0)])], str(path))
        self.assertFalse(path.exists())

    def testRepeatedSelectionDoesNotDuplicateOutput(self):
        self.prepare()
        path = self.output / "duplicate-selection.step"
        Part.export([self.root, self.root], str(path))
        self.check_step(path)

    def testMixedOrdinaryColorTupleIsPreserved(self):
        self.prepare()
        ordinary = App.newDocument("ColoredOrdinary")
        box = ordinary.addObject("Part::Feature", "Box")
        box.Shape = Part.makeBox(1, 1, 1)
        box.Placement.Base = App.Vector(40, 0, 0)
        ordinary.recompute()
        path = self.output / "mixed-colors.step"
        Import.export([self.root, (box, [(1.0, 0.0, 0.0)])], str(path))
        shape = Part.read(str(path))
        self.assertEqual(len(shape.Solids), 3)
        self.assertAlmostEqual(shape.Volume, 37)

    def testRawNativeCacheIsRefused(self):
        Model.set_part_types(self.root, [(self.link, "Reference")])
        operation = self.doc.addObject("Part::Fuse", "RawNative")
        Model.register_object(self.root, operation, "Operation")
        operation.Base, operation.Tool = self.body, self.local
        self.doc.recompute()
        self.assertFalse(operation.Shape.isNull())
        for writer, suffix in ((Part, ".step"), (Import, ".step"),
                               (ImportGui, ".step"), (Mesh, ".stl")):
            path = self.output / (writer.__name__ + "-raw" + suffix)
            with self.subTest(writer=writer.__name__):
                with self.assertRaises(Exception):
                    writer.export([operation], str(path))
                self.assertFalse(path.exists())

    def testStandardFileExportUsesNativePolicy(self):
        self.prepare()
        App.ParamGet("User parameter:BaseApp/Preferences/Dialog").SetBool("DontUseNativeDialog", True)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.root)
        path = self.output / "standard-export.stl"
        errors = []
        attempts = [0]
        stage = [0]
        timer = QtCore.QTimer()
        def fill():
            attempts[0] += 1
            for widget in QtWidgets.QApplication.topLevelWidgets():
                if isinstance(widget, QtWidgets.QMessageBox) and widget.isVisible():
                    errors.append(widget.text())
                    widget.accept()
                if isinstance(widget, QtWidgets.QFileDialog) and widget.isVisible():
                    filters = [f for f in widget.nameFilters() if "*.stl" in f.lower()]
                    if not filters:
                        errors.append("No STL export filter")
                        widget.reject()
                    elif stage[0] == 0:
                        widget.selectNameFilter(filters[0])
                        stage[0] = 1
                    elif stage[0] == 1:
                        widget.setDirectory(str(path.parent))
                        widget.findChild(QtWidgets.QLineEdit, "fileNameEdit").setText(path.name)
                        stage[0] = 2
                    else:
                        timer.stop()
                        widget.accept()
            if attempts[0] > 100:
                errors.append("Export dialog timed out")
                for widget in QtWidgets.QApplication.topLevelWidgets():
                    if isinstance(widget, QtWidgets.QDialog) and widget.isVisible():
                        widget.reject()
                timer.stop()
        timer.timeout.connect(fill)
        timer.start(100)
        try:
            Gui.runCommand("Std_Export")
        finally:
            timer.stop()
        self.assertEqual(errors, [])
        self.assertTrue(path.is_file())
        mesh = Mesh.Mesh(str(path))
        self.assertTrue(mesh.isSolid())
        self.assertAlmostEqual(abs(mesh.Volume), 36, places=4)
