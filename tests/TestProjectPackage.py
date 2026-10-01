# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native packaging, relocation, source preservation and recoverable refusal."""
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore
from freecad.gui import ProjectPackage as Package


def close_documents():
    for doc in list(App.listDocuments()):
        App.closeDocument(doc)
    Gui.updateGui()
    QtCore.QCoreApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)


def fixture(folder):
    folder = Path(folder)
    for sub in ("parts", "assembly", "root"):
        (folder / sub).mkdir(parents=True, exist_ok=True)
    leaf = App.newDocument("PackagePart")
    box = leaf.addObject("Part::Box", "Box")
    box.Length, box.Width, box.Height = 2, 3, 4
    leaf.recompute()
    leaf.saveAs(str(folder / "parts/part.FCStd"))
    assembly = App.newDocument("PackageAssembly")
    assembly.saveAs(str(folder / "assembly/part.FCStd"))
    group = assembly.addObject("App::Part", "Definition")
    link = assembly.addObject("App::Link", "Nested")
    link.setLink(box)
    group.addObject(link)
    assembly.recompute()
    assembly.saveAs(str(folder / "assembly/part.FCStd"))
    root = App.newDocument("PackageRoot")
    root.UndoMode = 1
    root.saveAs(str(folder / "root/main.FCStd"))
    link = root.addObject("App::Link", "Assembly")
    link.setLink(group)
    repeated = root.addObject("App::Link", "Repeated")
    repeated.setLink(box)
    repeated.Placement.Base.x = 10
    root.recompute()
    root.saveAs(str(folder / "root/main.FCStd"))
    for saved in (leaf, assembly, root):
        Gui.getDocument(saved.Name).save()
    return root, assembly, leaf


def replace_xml(path, old, new):
    with zipfile.ZipFile(path) as archive:
        entries = [(info, archive.read(info)) for info in archive.infolist()]
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for info, data in entries:
            if info.filename == "Document.xml":
                assert old in data
                data = data.replace(old, new)
            archive.writestr(info, data)


class TestProjectPackage(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.temp = tempfile.TemporaryDirectory(prefix="freecad-package-test-")
        self.base = Path(self.temp.name)
        self.doc, self.assembly, self.leaf = fixture(self.base / "original")

    def tearDown(self):
        for dialog in list(Package._dialogs):
            dialog.close()
        close_documents()
        self.temp.cleanup()

    def review(self):
        report = Package.review(self.doc)
        self.assertEqual(report["errors"], [])
        return report

    def testNestedReviewUsesIdentityAndPreservesOriginals(self):
        before = [(doc.Name, doc.FileName, doc.UndoCount, Package.digest(Path(doc.FileName)))
                  for doc in (self.doc, self.assembly, self.leaf)]
        report = self.review()
        self.assertEqual(len(report["files"]), 3)
        self.assertEqual(len(report["references"]), 3)
        self.assertEqual({row["path"] for row in report["files"]},
                         {"documents/root/main.FCStd", "documents/assembly/part.FCStd", "documents/parts/part.FCStd"})
        archive_path = self.base / "project.zip"
        manifest = Package.create_package(self.doc, report, archive_path)
        self.assertEqual(manifest["entrypoint"], "documents/root/main.FCStd")
        with zipfile.ZipFile(archive_path) as archive:
            for row in report["files"]:
                self.assertEqual(archive.read(row["path"]), Path(row["source"]).read_bytes())
            self.assertNotIn(str(self.base), archive.read("manifest.json").decode())
        self.assertEqual(before, [(doc.Name, doc.FileName, doc.UndoCount, Package.digest(Path(doc.FileName)))
                                 for doc in (self.doc, self.assembly, self.leaf)])

    def testRelocatedNestedAssemblyReopensEditsAndSaves(self):
        archive_path = self.base / "project.zip"
        manifest = Package.create_package(self.doc, self.review(), archive_path)
        close_documents()
        # Only this test's known original directory is moved, under its temporary root.
        (self.base / "original").rename(self.base / "original-unavailable")
        relocated = self.base / "relocated"
        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(relocated)
        self.doc = App.openDocument(str(relocated / manifest["entrypoint"]))
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.Assembly.Shape.Volume, 24)
        self.assertAlmostEqual(self.doc.Repeated.Shape.Volume, 24)
        source = self.doc.Repeated.LinkedObject
        self.assertTrue(Path(source.Document.FileName).is_relative_to(relocated))
        self.assertTrue(Path(self.doc.Assembly.LinkedObject.Document.FileName).is_relative_to(relocated))
        source.Length = 5
        source.Document.recompute()
        self.doc.Assembly.LinkedObject.Document.recompute()
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.Assembly.Shape.Volume, 60)
        self.assertAlmostEqual(self.doc.Repeated.Shape.Volume, 60)
        for doc in (source.Document, self.doc.Assembly.LinkedObject.Document, self.doc):
            Gui.getDocument(doc.Name).save()
        path = self.doc.FileName
        close_documents()
        self.doc = App.openDocument(path)
        self.doc.recompute()
        self.assertAlmostEqual(self.doc.Repeated.Shape.Volume, 60)

    def testUnsavedDirtyAndOwnerTransactionAreRefused(self):
        report = self.review()
        self.doc.openTransaction("Owner edit")
        self.doc.Repeated.Label = "Owner label"
        with self.assertRaises(ValueError):
            Package.create_package(self.doc, report, self.base / "dirty.zip")
        self.assertTrue(self.doc.HasPendingTransaction)
        self.assertEqual(self.doc.Repeated.Label, "Owner label")
        self.assertFalse((self.base / "dirty.zip").exists())
        self.doc.abortTransaction()
        unsaved = App.newDocument("Unsaved")
        self.assertIn("Save the root", Package.review(unsaved)["errors"][0])

    def testMissingAndUnloadedSourcesAreDistinguished(self):
        path = Path(self.leaf.FileName)
        close_documents()
        # A root handle is enough for disk review; missing sources are never loaded/repaired.
        class SavedRoot:
            FileName = str(self.base / "original/root/main.FCStd")
        report = Package.review(SavedRoot())
        self.assertEqual(report["errors"], [])
        path.rename(path.with_suffix(".unavailable"))
        report = Package.review(SavedRoot())
        self.assertTrue(any("Missing or inaccessible" in error for error in report["errors"]))
        self.assertEqual(len(report["files"]), 3)
        self.assertEqual(App.listDocuments(), {})

    def testChangedSourceRequiresNewReviewAndNoOverwrite(self):
        report = self.review()
        self.doc.Label = "Revised root"
        Gui.getDocument(self.doc.Name).save()
        target = self.base / "project.zip"
        with self.assertRaisesRegex(ValueError, "changed after review"):
            Package.create_package(self.doc, report, target)
        self.assertFalse(target.exists())
        Package.create_package(self.doc, self.review(), target)
        before = target.read_bytes()
        with self.assertRaisesRegex(ValueError, "already exists"):
            Package.create_package(self.doc, self.review(), target)
        self.assertEqual(target.read_bytes(), before)

    def testUnsupportedAbsoluteLinkAndExternalAssetAreReported(self):
        self.doc.Repeated.addProperty("App::PropertyFile", "ExternalAsset")
        self.doc.Repeated.ExternalAsset = str(self.base / "unbundled.svg")
        self.doc.recompute()
        Gui.getDocument(self.doc.Name).save()
        self.assertTrue(any("External file/path assets" in error for error in Package.review(self.doc)["errors"]))
        path = Path(self.doc.FileName)
        replace_xml(path, b'file="../parts/part.FCStd"', b'file="C:/absolute/part.FCStd"')
        self.assertTrue(any("Absolute external links" in error for error in Package.review(self.doc)["errors"]))

    def testPublishFailureLeavesNoPartialPackage(self):
        report = self.review()
        target = self.base / "project.zip"
        with patch.object(Package.os, "link", side_effect=OSError("Destination does not support atomic publication")):
            with self.assertRaises(OSError):
                Package.create_package(self.doc, report, target)
        self.assertFalse(target.exists())
        self.assertEqual(list(self.base.glob(".freecad-package-*")), [])
        self.assertEqual(Package.review(self.doc), report)

    def testInstalledCommandReviewCancelAndRecovery(self):
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.runCommand("Std_PackageProject")
        Gui.updateGui()
        dialog = Package._dialogs[-1]
        self.assertEqual(dialog.table.topLevelItemCount(), 3)
        self.assertTrue(dialog.createButton.isEnabled())
        dialog.destination.setText(str(self.base / "gui.zip"))
        self.doc.Label = "Changed after review"
        dialog.create()
        self.assertFalse((self.base / "gui.zip").exists())
        Gui.getDocument(self.doc.Name).save()
        dialog.refresh()
        dialog.create()
        self.assertTrue((self.base / "gui.zip").exists())
        self.assertIn("Package created", dialog.message.text())
        dialog.close()
        self.assertFalse(self.doc.HasPendingTransaction)
        Gui.runCommand("Std_PackageProject")
        dialog = Package._dialogs[-1]
        App.closeDocument(self.doc.Name)
        Gui.updateGui()
        self.assertTrue(dialog.closed)
