# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native mesh review, copy isolation and installed CAM command checks."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Mesh
import Part
from Path.Main import MeshPreparation as Prep
from Path.Main.Gui import MeshPreparation as UI


def box_mesh(inward=False):
    mesh = Mesh.Mesh(Part.makeBox(12, 10, 5).tessellate(0.1))
    if inward:
        mesh.flipNormals()
    return mesh


class TestMeshPreparation(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("CAMWorkbench")
        self.doc = App.newDocument("MeshPreparation")
        self.doc.UndoMode = 1
        self.source = self.doc.addObject("Mesh::Feature", "ImportedMesh")
        self.source.Mesh = box_mesh()
        self.source.Placement = App.Placement(App.Vector(17, 13, 2), App.Rotation(App.Vector(0, 0, 1), 30))
        self.doc.recompute()
        self.dialogs = []

    def tearDown(self):
        for dialog in self.dialogs + list(UI._dialogs):
            if not dialog.closed:
                dialog.reject()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def set_mesh(self, mesh):
        self.source.Mesh = mesh
        self.doc.recompute()

    def test_placed_closed_mesh_review_is_read_only(self):
        before = (len(self.doc.Objects), self.doc.UndoCount, self.doc.RecomputesFrozen,
                  self.source.Mesh.Topology, tuple(self.source.Placement.toMatrix().A))
        report = Prep.inspect(self.source)
        self.assertTrue(report["closed"])
        self.assertAlmostEqual(report["signed_volume"], 600, places=4)
        self.assertEqual(report["components"], 1)
        self.assertFalse(report["can_flip"])
        self.assertEqual(report["boundary"], 0)
        self.assertEqual(report["bounds"][0], self.source.Mesh.BoundBox.XMin)
        self.assertEqual(before, (len(self.doc.Objects), self.doc.UndoCount, self.doc.RecomputesFrozen,
                                 self.source.Mesh.Topology, tuple(self.source.Placement.toMatrix().A)))

    def test_open_disconnected_and_inconsistent_fixtures(self):
        vertices, faces = box_mesh().Topology
        self.set_mesh(Mesh.Mesh((vertices, faces[:-2])))
        report = Prep.inspect(self.source)
        self.assertEqual(report["boundary"], 4)
        self.assertFalse(report["closed"])
        self.assertFalse(report["can_flip"])
        mesh = box_mesh()
        second = box_mesh(True)
        second.translate(30, 0, 0)
        mesh.addMesh(second)
        self.set_mesh(mesh)
        report = Prep.inspect(self.source)
        self.assertEqual(report["components"], 2)
        self.assertEqual(report["orientation"], Prep.tr("Undetermined"))
        self.assertFalse(report["can_flip"])
        faces[0] = tuple(reversed(faces[0]))
        self.set_mesh(Mesh.Mesh((vertices, faces)))
        self.assertGreater(Prep.inspect(self.source)["inconsistent"], 0)

    def test_degenerate_duplicate_and_nonmanifold_edges(self):
        mesh = Mesh.Mesh()
        mesh.addFacets(([App.Vector(*point) for point in
                        ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1))],
                        [(0, 1, 2), (0, 1, 2), (1, 0, 3), (0, 1, 4), (0, 1, 1)]), False)
        self.set_mesh(mesh)
        report = Prep.inspect(self.source)
        self.assertGreater(report["nonmanifold"], 0)
        self.assertEqual(report["degenerate"], 1)
        self.assertEqual(report["duplicate"], 1)
        self.assertFalse(report["can_flip"])

    def test_dense_mesh_review_and_limit_do_not_decimate(self):
        side = 225
        points = [App.Vector(x, y, 0) for y in range(side) for x in range(side)]
        faces = []
        for y in range(side - 1):
            for x in range(side - 1):
                first = y * side + x
                faces.extend(((first, first + 1, first + side),
                              (first + 1, first + side + 1, first + side)))
        self.set_mesh(Mesh.Mesh((points, faces)))
        report = Prep.inspect(self.source)
        self.assertTrue(report["dense"])
        self.assertEqual(report["facets"], 100352)
        self.assertEqual(report["boundary"], 896)
        with patch.object(Prep, "MAX_FACETS", 100000), self.assertRaises(ValueError):
            Prep.inspect(self.source)
        self.assertEqual(self.source.Mesh.CountFacets, 100352)

    def test_inward_copy_preserves_source_placement_job_and_undo_reopen(self):
        self.set_mesh(box_mesh(True))
        from Path.Main import MeshModel
        job_model = MeshModel.create(self.doc, self.source)
        self.doc.recompute()
        expected = Prep.inspect(self.source)
        original = self.source.Mesh.Topology
        undo = self.doc.UndoCount
        result = Prep.reversed_copy(self.source, expected)
        result_name = result.Name
        self.assertEqual(self.doc.UndoCount, undo + 1)
        self.assertTrue(result.Placement.isSame(self.source.Placement, 1e-8))
        self.assertEqual(self.source.Mesh.Topology, original)
        self.assertEqual(job_model.Objects, [self.source])
        self.assertEqual(result.OutList, [])
        self.assertEqual(Prep.inspect(result)["bounds"], expected["bounds"])
        self.assertAlmostEqual(Prep.inspect(result)["signed_volume"], 600, places=4)
        self.doc.undo()
        self.assertIsNone(self.doc.getObject(result_name))
        self.assertEqual(self.source.Mesh.Topology, original)
        self.doc.redo()
        self.doc.recompute()
        with tempfile.TemporaryDirectory() as folder:
            filename = str(Path(folder) / "ReviewedMesh.FCStd")
            self.doc.saveAs(filename)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(filename)
            self.assertTrue(Prep.inspect(self.doc.ImportedMesh)["can_flip"])
            self.assertGreater(Prep.inspect(self.doc.getObject(result_name))["signed_volume"], 0)
            self.doc.ImportedMesh.Mesh = box_mesh()
            self.doc.recompute()
            self.assertEqual(self.doc.getObject(result_name).OutList, [])

    def test_stale_nested_and_transaction_inputs_refused(self):
        self.set_mesh(box_mesh(True))
        expected = Prep.inspect(self.source)
        self.source.Placement.Base = App.Vector(100, 0, 0)
        self.doc.recompute()
        with self.assertRaises(ValueError):
            Prep.reversed_copy(self.source, expected)
        self.doc.openTransaction("Owner edit")
        with self.assertRaises(ValueError):
            Prep.reversed_copy(self.source, Prep.inspect(self.source))
        self.assertEqual(App.getActiveTransaction()[0], "Owner edit")
        self.source.Label = "Owner edit still open"
        with self.assertRaises(ValueError):
            Prep.reversed_copy(self.source, Prep.inspect(self.source))
        self.assertTrue(self.doc.HasPendingTransaction)
        self.doc.abortTransaction()
        self.source.touch()
        with self.assertRaises(ValueError):
            Prep.inspect(self.source)
        self.doc.recompute()
        group = self.doc.addObject("App::Part", "Container")
        group.addObject(self.source)
        self.doc.recompute()
        with self.assertRaises(ValueError):
            Prep.inspect(self.source)

    def test_copy_failure_rolls_back(self):
        self.set_mesh(box_mesh(True))
        expected = Prep.inspect(self.source)
        count, undo = len(self.doc.Objects), self.doc.UndoCount
        native = Prep.inspect
        def fail_result(obj):
            if obj != self.source:
                raise ValueError("Injected result validation failure")
            return native(obj)
        with patch.object(Prep, "inspect", side_effect=fail_result), self.assertRaises(ValueError):
            Prep.reversed_copy(self.source, expected)
        self.assertEqual(len(self.doc.Objects), count)
        self.assertEqual(self.doc.UndoCount, undo)
        self.assertEqual(Prep.inspect(self.source), expected)

    def test_installed_command_refresh_cancel_copy_and_close_lifecycle(self):
        self.set_mesh(box_mesh(True))
        self.assertIn("CAM_MeshPreparation", Gui.listCommands())
        Gui.Selection.addSelection(self.source)
        Gui.runCommand("CAM_MeshPreparation", 0)
        dialog = UI._dialogs[-1]
        self.assertTrue(dialog.copyButton.isEnabled())
        before = self.doc.UndoCount
        self.source.Label = "Changed input"
        self.assertIsNone(dialog.expected)
        self.assertFalse(dialog.copyButton.isEnabled())
        self.assertEqual(dialog.table.topLevelItemCount(), 0)
        self.doc.recompute()
        dialog.review()
        dialog.reject()
        self.assertEqual(self.doc.UndoCount, before)
        self.assertEqual(len(self.doc.Objects), 1)
        dialog = UI.ReviewDialog(self.source)
        self.dialogs.append(dialog)
        dialog.createCopy()
        self.assertIsNotNone(self.doc.getObject("OrientedMesh"))
        self.assertFalse(dialog.copyButton.isEnabled())
        App.closeDocument(self.doc.Name)
        self.assertTrue(dialog.closed)
