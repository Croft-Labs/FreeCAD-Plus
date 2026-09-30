# SPDX-License-Identifier: LGPL-2.1-or-later
"""Direct STL jobs and geometric stock-bridge regression tests."""

import os
import tempfile
import unittest

import FreeCAD as App
import Mesh
import Part
import Path
from CAMTests.PathTestUtils import PathTestWithAssets
from Path.Main import Job, Stock, HoldingTab, IndexedSetup
from Path.Op import PlanarSurface


class TestMeshMachining(PathTestWithAssets):
    def setUp(self):
        super().setUp()
        self.doc = App.newDocument("MeshMachiningTest")

    def tearDown(self):
        App.closeDocument(self.doc.Name)
        super().tearDown()

    def make_job(self, mesh=True, shape=None):
        if shape is None:
            shape = Part.makeBox(12, 10, 5)
        model = self.doc.addObject("Mesh::Feature" if mesh else "Part::Feature", "Model")
        if mesh:
            # Exercise real STL import, not just an in-memory geometry stub.
            with tempfile.TemporaryDirectory() as temp:
                filename = os.path.join(temp, "model.stl")
                Mesh.Mesh(shape.tessellate(0.1)).write(filename)
                model.Mesh = Mesh.Mesh(filename)
        else:
            model.Shape = shape
        model.Placement.Base = App.Vector(7, 11, 3)
        self.doc.recompute()
        job = Job.Create("Job", [model])
        tool = self.assets.get("toolbit://5mm_Endmill").attach_to_doc(doc=self.doc)
        job.Tools.Group[0].Tool = tool
        job.Tools.Group[0].HorizFeed = "400 mm/min"
        job.Tools.Group[0].VertFeed = "100 mm/min"
        self.doc.recompute()
        return job, model

    def make_op(self, job, strategy):
        op = PlanarSurface.Create("Surface", parentJob=job)
        op.Strategy = strategy
        op.CutPattern = "ZigZag"
        op.BoundBox = "Stock"
        op.SampleInterval = 0.5
        op.StepOver = 40
        op.setExpression("StepDown", None)
        op.StepDown = 1
        if strategy == "Waterline":
            op.LayerMode = "Multi-pass"
        op.KeepToolDown = False
        self.doc.recompute()
        op.Proxy.execute(op)
        self.assertGreater(len(op.Path.Commands), 5)
        self.assertTrue(any(c.Name == "G1" and ("X" in c.Parameters or "Y" in c.Parameters)
                            for c in op.Path.Commands), "No actual cutting passes were generated")
        return op

    def test_curved_stl_parallel_follows_surface_and_waterline_has_layers(self):
        shape = Part.makeSphere(6).common(Part.makeBox(12, 12, 6, App.Vector(-6, -6, 0)))
        job, _ = self.make_job(shape=shape)
        parallel = self.make_op(job, "SurfaceScan")
        heights = {round(c.Parameters["Z"], 3) for c in parallel.Path.Commands
                   if c.Name == "G1" and "Z" in c.Parameters}
        self.assertGreater(len(heights), 8, sorted(heights))
        self.assertAlmostEqual(max(heights), 9, delta=0.2)
        waterline = self.make_op(job, "Waterline")
        heights = {round(c.Parameters["Z"], 3) for c in waterline.Path.Commands
                   if c.Name == "G1" and "Z" in c.Parameters}
        self.assertGreaterEqual(len(heights), 3,
                                (sorted(heights), waterline.StartDepth.Value,
                                 waterline.FinalDepth.Value, waterline.StepDown.Value))

    def test_mesh_clone_stock_placement_and_edit(self):
        job, model = self.make_job()
        clone = job.Model.Group[0]
        self.assertTrue(hasattr(clone, "Mesh"))
        self.assertEqual(model.Mesh.CountFacets, clone.Mesh.CountFacets)
        for prop in ("XMin", "YMin", "ZMin", "XMax", "YMax", "ZMax"):
            self.assertAlmostEqual(getattr(model.Mesh.BoundBox, prop),
                                   getattr(Stock.shapeBoundBox(clone), prop))
        clone.Placement.Base = App.Vector(20, 30, 4)
        model.Mesh = Mesh.Mesh(Part.makeBox(15, 10, 5).tessellate(0.1))
        self.doc.recompute()
        self.assertAlmostEqual(clone.Mesh.BoundBox.XMin, 20)
        self.assertAlmostEqual(clone.Mesh.BoundBox.XLength, 15)

    def test_parallel_includes_every_translated_mesh_and_cad_model(self):
        original_job, first = self.make_job()
        second = self.doc.addObject("Mesh::Feature", "SecondMesh")
        second.Mesh = Mesh.Mesh(Part.makeBox(6, 10, 8).tessellate(0.1))
        second.Placement.Base = App.Vector(30, 11, 3)
        third = self.doc.addObject("Part::Feature", "CADModel")
        third.Shape = Part.makeBox(6, 10, 12)
        third.Placement.Base = App.Vector(45, 11, 3)
        job = Job.Create("MixedJob", [first, second, third])
        job.Tools.Group[0].Tool = original_job.Tools.Group[0].Tool
        job.Tools.Group[0].HorizFeed = "400 mm/min"
        job.Tools.Group[0].VertFeed = "100 mm/min"
        self.doc.recompute()
        op = self.make_op(job, "SurfaceScan")
        position = {}
        heights = [[], [], []]
        for command in op.Path.Commands:
            if command.Name not in ("G0", "G1"):
                continue
            previous = dict(position)
            position.update({k: v for k, v in command.Parameters.items() if k in "XYZ"})
            if command.Name == "G1" and all(k in previous for k in "XYZ"):
                # Optimized paths may span a flat top without interior vertices.
                for fraction in (j / 50 for j in range(51)):
                    point = {k: previous[k] + fraction * (position[k] - previous[k])
                             for k in "XYZ"}
                    for i, (left, right) in enumerate(((7, 19), (30, 36), (45, 51))):
                        if left < point["X"] < right and 11 < point["Y"] < 21:
                            heights[i].append(point["Z"])
        for samples, expected in zip(heights, (8, 11, 15)):
            self.assertTrue(samples)
            # Feed plunges begin above the model; the lowest sampled cutter tip
            # must reach its top without cutting below it.
            self.assertAlmostEqual(min(samples), expected, delta=0.1)

    def assert_tabs_clear(self, commands, tab, radius):
        # Independent sampled swept-cylinder check in tab coordinates. Dense
        # samples complement the exact segment intersection unit regressions.
        if getattr(tab, "SetupFrame", None):
            bb = tab.Shape.BoundBox
            inverse = App.Placement(bb.Center, App.Rotation()).inverse()
            length, width, height = bb.XLength, bb.YLength, bb.ZLength / 2
        else:
            inverse = tab.Placement.inverse()
            length, width, height = tab.Length.Value, tab.Width.Value, tab.Height.Value
        position = {}
        checked = 0
        for command in commands:
            if command.Name not in ("G0", "G1"):
                continue
            end = dict(position)
            end.update({k: v for k, v in command.Parameters.items() if k in "XYZ"})
            if len(position) == 3 and len(end) == 3:
                a, b = App.Vector(*(position[k] for k in "XYZ")), App.Vector(*(end[k] for k in "XYZ"))
                for i in range(101):
                    p = inverse.multVec(a + (b - a) * (i / 100))
                    dx = max(abs(p.x) - length / 2, 0)
                    dy = max(abs(p.y) - width / 2, 0)
                    self.assertFalse(p.z < height - 1e-6
                                     and dx * dx + dy * dy < radius * radius - 1e-6,
                                     f"Cutter intersects tab at {p}")
                    checked += 1
            position = end
        self.assertGreater(checked, 0)

    def test_stl_parallel_and_waterline_with_tabs(self):
        job, model = self.make_job()
        tab = HoldingTab.create(job, App.Vector(19, 16, 3))
        tab.Length, tab.Width, tab.Height = 8, 3, 2
        tab.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), 25)
        self.doc.recompute()
        for strategy in ("SurfaceScan", "Waterline"):
            with self.subTest(strategy=strategy):
                op = self.make_op(job, strategy)
                self.assert_tabs_clear(op.Path.Commands, tab, 2.5)
                self.assertIn(tab, op.HoldingTabs)
                # Geometry changes must invalidate the operation, not just its UI.
                tab.Width = tab.Width.Value + 0.5
                self.doc.recompute()
                self.assert_tabs_clear(op.Path.Commands, tab, 2.5)

    def test_cad_parallel_and_waterline_with_tabs(self):
        job, model = self.make_job(mesh=False)
        tab = HoldingTab.create(job, App.Vector(19, 16, 3))
        for strategy in ("SurfaceScan", "Waterline"):
            op = self.make_op(job, strategy)
            self.assert_tabs_clear(op.Path.Commands, tab, 2.5)

    def test_persistence(self):
        job, model = self.make_job()
        tab = HoldingTab.create(job)
        op = self.make_op(job, "Waterline")
        names = job.Name, tab.Name, op.Name
        with tempfile.TemporaryDirectory() as temp:
            filename = os.path.join(temp, "mesh-tabs.FCStd")
            self.doc.recompute()
            self.doc.saveAs(filename)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(filename)
            job, tab, op = (self.doc.getObject(name) for name in names)
            op.touch()
            self.doc.recompute()
            self.assertIn(tab, job.HoldingTabs)
            self.assertIn(tab, op.HoldingTabs)
            self.assertGreater(len(op.Path.Commands), 5)
            self.assert_tabs_clear(op.Path.Commands, tab, 2.5)

    def test_unsupported_strategy_clears_old_path(self):
        job, _ = self.make_job()
        op = self.make_op(job, "Waterline")
        HoldingTab.create(job)
        op.Strategy = "ZLevelHybrid"
        with self.assertRaisesRegex(ValueError, "holding tabs"):
            op.Proxy.execute(op)
        self.assertEqual(len(op.Path.Commands), 0)

    def test_opposite_side_and_oblique_index_share_geometry(self):
        job, model = self.make_job()
        original = HoldingTab.create(job, App.Vector(19, 16, 3))
        for angle in (180, 45):
            with self.subTest(angle=angle):
                indexed = IndexedSetup.create(job, "X", angle)
                transform = indexed.IndexFrame.Transform
                source_points, _ = job.Model.Group[0].Mesh.Topology
                expected = App.BoundBox()
                for point in source_points:
                    expected.add(transform.multVec(point))
                actual = indexed.Model.Group[0].Mesh.BoundBox
                for prop in ("XMin", "YMin", "ZMin", "XMax", "YMax", "ZMax"):
                    self.assertAlmostEqual(getattr(actual, prop), getattr(expected, prop), places=5)
                self.assertAlmostEqual(indexed.Stock.Shape.BoundBox.ZMax, 0, places=5)
                self.assertAlmostEqual(indexed.Stock.Shape.Volume, job.Stock.Shape.Volume, places=5)
                tab = indexed.HoldingTabs[0]
                shape = original.Shape.copy()
                shape.Placement = transform.multiply(shape.Placement)
                self.assertLess(shape.cut(tab.Shape).Volume + tab.Shape.cut(shape).Volume, 1e-6)
                for strategy in ("SurfaceScan", "Waterline"):
                    op = self.make_op(indexed, strategy)
                    self.assert_tabs_clear(op.Path.Commands, tab, 2.5)
                original.Width = original.Width.Value + 1
                self.doc.recompute()
                self.assertAlmostEqual(tab.Shape.Volume, original.Shape.Volume, places=5)
                self.assert_tabs_clear(op.Path.Commands, tab, 2.5)

    def test_new_tabs_propagate_to_existing_indexed_setup(self):
        job, _ = self.make_job()
        indexed = IndexedSetup.create(job)
        original = HoldingTab.create(job)
        self.doc.recompute()
        self.assertEqual(len(indexed.HoldingTabs), 1)
        self.assertEqual(indexed.HoldingTabs[0].Objects[0], original)

    def test_indexed_setup_save_reopen_and_custom_origin(self):
        job, _ = self.make_job()
        HoldingTab.create(job)
        indexed = IndexedSetup.create(job, "Y", 90, "Custom", App.Vector(2, 3, 4))
        self.assertEqual(indexed.IndexFrame.Transform.Base, App.Vector(-2, -3, -4))
        name = indexed.Name
        with tempfile.TemporaryDirectory() as temp:
            filename = os.path.join(temp, "indexed.FCStd")
            self.doc.saveAs(filename)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(filename)
            indexed = self.doc.getObject(name)
            indexed.IndexFrame.Angle = 180
            self.doc.recompute()
            op = self.make_op(indexed, "Waterline")
            self.assert_tabs_clear(op.Path.Commands, indexed.HoldingTabs[0], 2.5)


class TestTabProtection(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("TabProtectionTest")
        self.tab = self.doc.addObject("Part::FeaturePython", "Tab")
        HoldingTab.HoldingTab(self.tab)
        self.tab.Length, self.tab.Width, self.tab.Height = 4, 2, 2
        self.doc.recompute()

    def tearDown(self):
        App.closeDocument(self.doc.Name)

    def protect(self, tail, tabs=None):
        start = [Path.Command("G0", {"Z": 10}), Path.Command("G0", {"X": -20, "Y": 0}),
                 Path.Command("G1", {"Z": 0, "F": 100})]
        return HoldingTab.protect(start + tail, tabs or [self.tab], 1, 10, 100)

    def test_crossing_narrow_tab_with_no_interior_sample(self):
        result = self.protect([Path.Command("G1", {"X": 20, "F": 400})])
        TestMeshMachining.assert_tabs_clear(self, result, self.tab, 1)
        self.assertTrue(any(c.Parameters.get("X") == 20 and c.Parameters.get("Z") == 0
                            for c in result))

    def test_inserted_bridge_moves_preserve_block_delete_annotations(self):
        commands = [Path.Command("G0", {"Z": 10}),
                    Path.Command("G0", {"X": -20, "Y": 0}),
                    Path.Command("G1", {"Z": 0, "F": 100}),
                    Path.Command("G1", {"X": 20, "F": 400})]
        for command in commands:
            command.Annotations = {"BlockDelete": True}
        result = HoldingTab.protect(commands, [self.tab], 1, 10, 100)
        self.assertGreater(len(result), len(commands))
        self.assertTrue(all(c.Annotations.get("BlockDelete") for c in result))

    def test_inside_endpoints_vertical_moves_and_reverse_crossing(self):
        result = self.protect([Path.Command("G1", {"X": 0}),
                               Path.Command("G1", {"Z": -3}),
                               Path.Command("G1", {"X": 1}),
                               Path.Command("G1", {"X": -20})])
        TestMeshMachining.assert_tabs_clear(self, result, self.tab, 1)

    def test_rotated_and_overlapping_tabs(self):
        self.tab.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), 40)
        other = self.doc.addObject("Part::FeaturePython", "OtherTab")
        HoldingTab.HoldingTab(other)
        other.Placement.Base = App.Vector(4, 0, 0)
        other.Height = 4
        self.doc.recompute()
        result = self.protect([Path.Command("G0", {"X": 20})], [self.tab, other])
        for tab in (self.tab, other):
            TestMeshMachining.assert_tabs_clear(self, result, tab, 1)

    def test_arcs_and_unsafe_heights_rejected(self):
        with self.assertRaisesRegex(ValueError, "linear three-axis"):
            self.protect([Path.Command("G2", {"X": 20, "I": 10})])
        self.tab.Height = 11
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "heights"):
            self.protect([])

    def test_tilted_tab_rejected(self):
        self.tab.Placement.Rotation = App.Rotation(App.Vector(1, 0, 0), 30)
        with self.assertRaisesRegex(ValueError, "XY"):
            self.protect([])


@unittest.skipUnless(App.GuiUp, "GUI required")
class TestHoldingTabGui(PathTestWithAssets):
    def setUp(self):
        super().setUp()
        import FreeCADGui as Gui
        from Path.Main.Gui import HoldingTab as TabGui

        self.Gui = Gui
        self.TabGui = TabGui
        self.doc = App.newDocument("HoldingTabGuiTest")
        self.doc.UndoMode = 1
        shape = self.doc.addObject("Part::Feature", "Box")
        shape.Shape = Part.makeBox(10, 10, 5)
        self.job = Job.Create("Job", [shape])
        self.doc.recompute()

    def tearDown(self):
        if self.Gui.Control.activeDialog():
            self.Gui.activeDocument().resetEdit()
        App.closeDocument(self.doc.Name)
        super().tearDown()

    def test_workbench_exposes_mesh_and_setup_commands(self):
        self.Gui.activateWorkbench("CAMWorkbench")
        commands = self.Gui.listCommands()
        for name in ("CAM_PlanarSurface", "CAM_HoldingTab", "CAM_IndexedSetup"):
            self.assertIn(name, commands)

    def test_create_cancel_edit_pick_and_undo(self):
        self.Gui.Selection.clearSelection()
        self.Gui.Selection.addSelection(self.job)
        self.TabGui.Command().Activated()
        tab = self.job.HoldingTabs[-1]
        name = tab.Name
        task = tab.ViewObject.Proxy.task
        task.fields["Width"].setValue(7)
        task.pick.setChecked(True)
        task.addSelection(self.doc.Name, "Box", "Face1", (11, 6, 5))
        self.assertAlmostEqual(tab.Placement.Base.x, 11)
        self.assertAlmostEqual(tab.Placement.Base.y, 6)
        self.assertTrue(task.accept())
        self.assertAlmostEqual(tab.Width.Value, 7)
        self.assertTrue(tab.ViewObject.Proxy.doubleClicked(tab.ViewObject))
        task = tab.ViewObject.Proxy.task
        task.fields["Width"].setValue(9)
        task.reject()
        self.assertAlmostEqual(tab.Width.Value, 7)
        self.doc.undo()
        self.assertIsNone(self.doc.getObject(name))
        self.doc.redo()
        self.assertIsNotNone(self.doc.getObject(name))

    def test_cancel_creation_removes_job_link(self):
        self.Gui.Selection.clearSelection()
        self.Gui.Selection.addSelection(self.job)
        self.TabGui.Command().Activated()
        tab = self.job.HoldingTabs[-1]
        name = tab.Name
        tab.ViewObject.Proxy.task.reject()
        self.assertIsNone(self.doc.getObject(name))
        self.assertFalse(getattr(self.job, "HoldingTabs", []))

    def test_indexed_setup_command_cancel_removes_created_objects(self):
        from Path.Main.Gui import IndexedSetup as SetupGui
        before = {obj.Name for obj in self.doc.Objects}
        self.Gui.Selection.clearSelection()
        self.Gui.Selection.addSelection(self.job)
        SetupGui.Command().Activated()
        indexed = next(obj for obj in self.doc.Objects
                       if getattr(obj, "SourceJob", None) == self.job)
        self.assertIsNotNone(indexed.IndexFrame.ViewObject.Proxy.task)
        indexed.IndexFrame.ViewObject.Proxy.task.reject()
        self.assertEqual({obj.Name for obj in self.doc.Objects}, before)

    def test_creation_commands_preserve_unrelated_transaction(self):
        from Path.Main.Gui import IndexedSetup as SetupGui
        self.doc.openTransaction("Unrelated edit")
        self.job.Label = "Pending job label"
        before = {obj.Name for obj in self.doc.Objects}
        self.Gui.Selection.clearSelection()
        self.Gui.Selection.addSelection(self.job)
        for command in (self.TabGui.Command(), SetupGui.Command()):
            with self.assertRaisesRegex(RuntimeError, "current transaction"):
                command.Activated()
            self.assertTrue(self.doc.HasPendingTransaction)
            self.assertEqual(self.job.Label, "Pending job label")
            self.assertEqual({obj.Name for obj in self.doc.Objects}, before)
        self.doc.abortTransaction()

    def test_indexed_setup_editor_cancel_and_accept(self):
        indexed = IndexedSetup.create(self.job)
        frame = indexed.IndexFrame
        before = indexed.Stock.Shape.copy()
        self.assertTrue(frame.ViewObject.Proxy.doubleClicked(frame.ViewObject))
        task = frame.ViewObject.Proxy.task
        task.angle.setValue(45)
        task.reject()
        self.assertAlmostEqual(frame.Angle.Value, 180)
        self.assertLess(before.cut(indexed.Stock.Shape).Volume, 1e-6)
        frame.ViewObject.Proxy.doubleClicked(frame.ViewObject)
        task = frame.ViewObject.Proxy.task
        task.angle.setValue(90)
        task.origin.setCurrentIndex(task.origin.findData("Stock top corner"))
        self.assertTrue(task.accept())
        self.assertAlmostEqual(frame.Angle.Value, 90)
        self.assertAlmostEqual(indexed.Stock.Shape.BoundBox.XMin, 0, places=5)
        self.assertAlmostEqual(indexed.Stock.Shape.BoundBox.YMin, 0, places=5)
        self.assertAlmostEqual(indexed.Stock.Shape.BoundBox.ZMax, 0, places=5)

    def test_delete_shared_tab_removes_indexed_copy(self):
        tab = HoldingTab.create(self.job)
        indexed = IndexedSetup.create(self.job)
        copy_name = indexed.HoldingTabs[0].Name
        self.assertTrue(tab.ViewObject.Proxy.onDelete(tab.ViewObject, []))
        self.doc.removeObject(tab.Name)
        self.doc.recompute()
        self.assertIsNone(self.doc.getObject(copy_name))
        self.assertFalse(indexed.HoldingTabs)

    def test_indexed_job_editor_cancel_keeps_job_and_stock_transform(self):
        indexed = IndexedSetup.create(self.job, "Y", 45)
        name = indexed.Name
        before = indexed.Stock.Shape.copy()
        self.Gui.activeDocument().setEdit(name)
        task = indexed.ViewObject.Proxy.taskPanel
        task.refreshStock()
        self.assertLess(before.cut(indexed.Stock.Shape).Volume
                        + indexed.Stock.Shape.cut(before).Volume, 1e-6)
        task.reject()
        self.assertIsNotNone(self.doc.getObject(name))
