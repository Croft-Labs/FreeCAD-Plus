# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native BOM scope, per-parent quantities and explicit inclusion policy."""
import csv
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import FreeCAD as App
import FreeCADGui as Gui
import CommandCreateBom as Editor


def make_fixture():
    doc = App.newDocument("AssemblyBomScope")
    doc.UndoMode = 1
    bolt = doc.addObject("Part::Box", "Bolt")
    bolt.Length, bolt.Width, bolt.Height = 4, 4, 12
    unique = doc.addObject("Part::Box", "UniqueBolt")
    unique.Length, unique.Width, unique.Height = 6, 6, 12
    sub = doc.addObject("App::Part", "ModuleDefinition")
    inner = sub.newObject("App::Link", "InnerBolt")
    inner.setLink(bolt)
    assembly = doc.addObject("Assembly::AssemblyObject", "Product")
    for name, source in (("ModuleOne", sub), ("ModuleTwo", sub),
                         ("OutsideOne", bolt), ("OutsideTwo", bolt),
                         ("HiddenBolt", bolt), ("UniqueOccurrence", unique)):
        link = assembly.newObject("App::Link", name)
        link.setLink(source)
    doc.HiddenBolt.Visibility = False
    other = doc.addObject("Assembly::AssemblyObject", "OtherProduct")
    other.newObject("Part::Box", "Unrelated")
    group = assembly.newObject("Assembly::BomGroup", "BillsOfMaterials")
    bom = group.newObject("Assembly::BomObject", "ProductBOM")
    bom.columnsNames = ["Index", "Name", "Quantity"]
    bom.onlyParts = False
    bom.detailParts = True
    bom.detailSubAssemblies = True
    doc.recompute()
    bom.recompute()
    return doc, bom


def rows(bom):
    result = []
    for row in range(2, 50):
        try:
            label = bom.getContents(f"B{row}").lstrip("'")
        except Exception:
            break
        if not label:
            break
        result.append((bom.getContents(f"A{row}").lstrip("'"), label,
                       int(bom.getContents(f"C{row}"))))
    return result


class TestAssemblyBomScope(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("AssemblyWorkbench")
        self.doc, self.bom = make_fixture()
        self.task = None

    def tearDown(self):
        if self.task is not None and self.doc.Name in App.listDocuments():
            self.task.reject()
        if Gui.Control.activeDialog():
            Gui.Control.closeDialog()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def launch(self):
        self.task = Editor.TaskAssemblyCreateBom(self.bom)
        Gui.Control.showDialog(self.task)
        return self.task

    def exclude(self, *objects):
        Gui.Selection.clearSelection()
        for obj in objects:
            Gui.Selection.addSelection(obj)
        self.task.excludeSelection()

    def test_group_scope_and_per_parent_repeated_quantities(self):
        data = rows(self.bom)
        self.assertEqual(data, [("1", "ModuleDefinition", 2), ("1.1", "Bolt", 1),
                                ("2", "Bolt", 3), ("3", "UniqueBolt", 1)])
        self.assertFalse(any("Unrelated" in row or "OtherProduct" in row for row in data))
        self.doc.OutsideOne.Visibility = False
        self.doc.ModuleOne.Visibility = False
        self.bom.recompute()
        self.assertEqual(rows(self.bom), data)

    def test_per_bom_exclusion_and_definition_child_policy(self):
        second = self.doc.BillsOfMaterials.newObject("Assembly::BomObject", "SecondBOM")
        second.columnsNames = self.bom.columnsNames
        self.doc.recompute()
        original = rows(second)
        self.bom.excludedObjects = [self.doc.OutsideOne]
        self.doc.recompute()
        self.assertIn(("2", "Bolt", 2), rows(self.bom))
        self.assertEqual(rows(second), original)
        self.assertTrue(self.doc.OutsideOne.Visibility)
        self.assertFalse(self.doc.HiddenBolt.Visibility)
        self.bom.excludedObjects = [self.doc.InnerBolt]
        self.doc.recompute()
        self.assertEqual(rows(self.bom), [("1", "ModuleDefinition", 2), ("2", "Bolt", 3),
                                         ("3", "UniqueBolt", 1)])

    def test_mirror_grouping_plain_features_and_unique_definitions(self):
        mirror = self.doc.Product.newObject("App::Link", "Reflected")
        mirror.setLink(self.doc.Bolt)
        mirror.Scale = -1
        ordinary = self.doc.Product.newObject("Part::Box", "DirectSolid")
        self.doc.recompute()
        self.bom.recompute()
        data = rows(self.bom)
        self.assertIn(("2", "Bolt", 3), data)
        self.assertEqual([row[2] for row in data if "mirrored" in row[1]], [1])
        self.assertTrue(any(row[1] == ordinary.Label for row in data))
        self.assertTrue(any(row[1] == "UniqueBolt" and row[2] == 1 for row in data))

    def test_task_exclude_include_cancel_preserves_source_and_quantities(self):
        original = rows(self.bom)
        undo = self.doc.UndoCount
        self.launch()
        self.exclude(self.doc.HiddenBolt, self.doc.OutsideOne)
        self.assertEqual(self.task.exclusionList.count(), 2)
        self.assertIn(("2", "Bolt", 1), rows(self.bom))
        self.task.exclusionList.item(0).setSelected(True)
        self.task.includeSelected()
        self.assertEqual(len(self.bom.excludedObjects), 1)
        self.assertIn(("2", "Bolt", 2), rows(self.bom))
        self.task.reject()
        self.task = None
        self.doc.recompute()
        self.bom.recompute()
        self.assertEqual(self.bom.excludedObjects, [])
        self.assertEqual(rows(self.bom), original)
        self.assertEqual(self.doc.UndoCount, undo)
        self.assertFalse(self.doc.HiddenBolt.Visibility)
        self.assertTrue(self.doc.OutsideOne.Visibility)

    def test_accept_undo_redo_reopen_and_export(self):
        self.launch()
        self.exclude(self.doc.OutsideOne)
        self.assertTrue(self.task.accept())
        self.task = None
        self.assertIn(("2", "Bolt", 2), rows(self.bom))
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(self.bom.excludedObjects, [])
        self.doc.redo()
        self.doc.recompute()
        self.assertEqual(self.bom.excludedObjects, [self.doc.OutsideOne])
        with tempfile.TemporaryDirectory() as folder:
            filename = str(Path(folder) / "Assembly-BOM.FCStd")
            self.doc.saveAs(filename)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(filename)
            self.bom = self.doc.ProductBOM
            self.bom.recompute()
            self.assertEqual(self.bom.excludedObjects, [self.doc.OutsideOne])
            self.assertIn(("2", "Bolt", 2), rows(self.bom))
            target = Path(folder) / "Assembly-BOM.csv"
            self.bom.exportFile(str(target), ",", '"', "\\")
            with target.open(encoding="utf-8-sig", newline="") as stream:
                exported = list(csv.reader(stream))
            self.assertEqual(exported[0], ["Index", "Name", "Quantity"])
            self.assertIn(["2", "Bolt", "2"], exported)

    def test_invalid_scope_and_owner_transaction_preserved(self):
        self.doc.openTransaction("Owner edit")
        with self.assertRaisesRegex(ValueError, "transaction"):
            Editor.TaskAssemblyCreateBom(self.bom)
        self.assertEqual(App.getActiveTransaction()[0], "Owner edit")
        self.doc.abortTransaction()
        self.launch()
        self.exclude(self.doc.Unrelated)
        self.assertEqual(self.bom.excludedObjects, [])
        self.assertIn("scope", self.task.exclusionStatus.text())
        self.exclude(self.doc.Product)
        self.assertEqual(self.bom.excludedObjects, [])
        self.exclude(self.doc.Bolt)
        self.assertEqual(self.bom.excludedObjects, [])
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.doc.Bolt, "Face1")
        self.task.excludeSelection()
        self.assertEqual(self.bom.excludedObjects, [])

    def test_command_create_cancel_leaves_no_bom_or_group(self):
        original = {obj.Name for obj in self.doc.Objects}
        command = Editor.CommandCreateBom()
        with patch.object(Editor.UtilsAssembly, "activeAssembly", return_value=self.doc.OtherProduct):
            command.Activated()
        self.task = command.panel
        created = self.task.bomObj
        self.assertTrue(any(obj.TypeId == "Assembly::BomGroup" for obj in created.InList))
        self.assertTrue(command.panel.exclusionList.count() == 0)
        self.task.reject()
        self.task = None
        self.assertEqual({obj.Name for obj in self.doc.Objects}, original)

    def test_document_wide_picker_uses_native_tree_roots(self):
        self.bom = self.doc.addObject("Assembly::BomObject", "DocumentBOM")
        self.bom.columnsNames = ["Index", "Name", "Quantity"]
        self.doc.recompute()
        self.launch()
        scope = self.task.exclusionScope()
        self.assertIn(self.doc.Bolt, scope)
        self.assertIn(self.doc.Unrelated, scope)
        self.exclude(self.doc.Unrelated)
        self.assertEqual(self.bom.excludedObjects, [self.doc.Unrelated])
        self.assertFalse(any(row[1] == "Unrelated" for row in rows(self.bom)))
