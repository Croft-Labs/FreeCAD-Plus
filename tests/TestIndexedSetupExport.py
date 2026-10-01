# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native indexed STL jobs through real posts; no machine connection."""

import importlib
import os
from pathlib import Path as FilePath
import re
import tempfile
import unittest

import FreeCAD as App
import Path
from CAMTests.PathTestUtils import PathTestWithAssets
from Machine.models.machine import Machine, Toolhead, ToolheadType
from Path.Main import HoldingTab, IndexedSetup
from Path.Post.Processor import PostProcessorFactory
from Path.Post.CAMErrors import CAMValueError


MeshTests = importlib.import_module("CAMTests.TestMeshMachining")


class TestIndexedSetupExport(PathTestWithAssets):
    # Reuse the STL/operation fixtures without inheriting their test cases.
    def setUp(self):
        super().setUp()
        self.doc = App.newDocument("IndexedExportTest")

    def tearDown(self):
        App.closeDocument(self.doc.Name)
        super().tearDown()

    make_job = MeshTests.TestMeshMachining.make_job
    assert_tabs_clear = MeshTests.TestMeshMachining.assert_tabs_clear

    def make_op(self, job, strategy):
        op = MeshTests.TestMeshMachining.make_op(self, job, strategy)
        # The shared fixture explicitly calls Proxy.execute for path assertions;
        # native recompute must finish that edit before invoking an exporter.
        self.doc.recompute()
        return op

    def processor(self, job, name):
        post = PostProcessorFactory.get_post_processor(job, name)
        post._machine = Machine.create_3axis_config()
        post._machine.output.remote_post = False
        post._machine.output.precision.axis = 6
        post._machine.output.comments.include_operation_labels = True
        post._machine.toolheads = [Toolhead(
            name="Fixture spindle", toolhead_type=ToolheadType.ROTARY,
            min_rpm=0, max_rpm=24000, max_power_kw=1.0)]
        # Declare the fixture's coordinate convention explicitly; this tests
        # configured output, not each controller's factory defaults.
        post._machine.postprocessor_properties["preamble"] = "G17 G90"
        post.apply_configuration_bundle()
        return post

    def movements(self, code):
        """Decode modal linear metric motion independently of the CAM parser."""
        position, mode, commands = {}, None, []
        for line in code.splitlines():
            line = re.sub(r"\([^)]*\)", "", line).split(";")[0]
            words = re.findall(r"([A-Z])\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))", line)
            values = {key: float(value) for key, value in words}
            self.assertFalse(set(values) & set("ABC"), line)
            for key, value in words:
                if key != "G":
                    continue
                number = float(value)
                self.assertNotIn(number, (2, 3, 20, 91), line)
                if number in (0, 1):
                    mode = "G" + str(int(number))
            axes = {key: values[key] for key in "XYZ" if key in values}
            if axes:
                self.assertIsNotNone(mode, line)
                position.update(axes)
                commands.append(Path.Command(mode, dict(position)))
        return commands

    def native_movements(self, op):
        position, commands = {}, []
        for command in op.Path.Commands:
            if command.Name not in ("G0", "G1"):
                continue
            axes = {key: command.Parameters[key] for key in "XYZ"
                    if key in command.Parameters}
            if axes:
                position.update(axes)
                commands.append(Path.Command(command.Name, dict(position)))
        return commands

    def check_export(self, job, op, postname, stage):
        before = op.Path.toGCode()
        sections = self.processor(job, postname).export2()
        self.assertEqual(len(sections), 1)
        code = sections[0][1]
        self.assertTrue(code)
        output = os.environ.get("FREECAD_PLUS_VALIDATION_DIR")
        if output:
            folder = FilePath(output) / "indexed-output"
            folder.mkdir(exist_ok=True)
            (folder / f"{stage}-{job.Name}-{op.Strategy}-{postname}.nc").write_text(code)
        self.assertRegex(code, r"\bG21\b")
        self.assertRegex(code, r"\bG90\b")
        commands = self.movements(code)
        expected = self.native_movements(op)
        self.assertEqual(len(commands), len(expected))
        for actual, native in zip(commands, expected):
            self.assertEqual(actual.Name, native.Name)
            self.assertEqual(set(actual.Parameters), set(native.Parameters))
            for axis, value in native.Parameters.items():
                self.assertAlmostEqual(actual.Parameters[axis], value, delta=1e-6)
        self.assertEqual(op.Path.toGCode(), before)
        for tab in job.HoldingTabs:
            self.assert_tabs_clear(commands, tab, 2.5)
        self.assertAlmostEqual(commands[-1].Parameters["Z"], op.ClearanceHeight.Value,
                               delta=1e-6)
        return [(c.Name, dict(c.Parameters)) for c in commands]

    def setups(self):
        source, _ = self.make_job()
        tab = HoldingTab.create(source, App.Vector(19, 16, 3))
        tab.Length, tab.Width, tab.Height = 8, 3, 2
        self.doc.recompute()
        jobs = [IndexedSetup.create(source, "X", angle) for angle in (180, 45)]
        return source, tab, jobs

    def test_opposing_and_oblique_jobs_post_both_strategies_separately(self):
        source, tab, jobs = self.setups()
        for job in jobs:
            for strategy in ("SurfaceScan", "Waterline"):
                op = self.make_op(job, strategy)
                # Post one strategy at a time, using the real job operation list.
                for other in job.Operations.Group:
                    other.Active = other == op
                self.doc.recompute()
                for postname in ("linuxcnc", "grbl"):
                    with self.subTest(angle=job.IndexFrame.Angle.Value,
                                      strategy=strategy, post=postname):
                        self.check_export(job, op, postname, "initial")

    def test_shared_tab_and_independent_origin_edits_reach_export(self):
        source, tab, jobs = self.setups()
        ops = [self.make_op(job, "Waterline") for job in jobs]
        before = [self.check_export(job, op, "linuxcnc", "before-edit")
                  for job, op in zip(jobs, ops)]
        tab.Width = 6
        with self.assertRaisesRegex(ValueError, "Indexed setup input"):
            ops[0].Proxy.execute(ops[0])
        self.assertFalse(ops[0].Path.Commands)
        for job in jobs:
            with self.assertRaises(CAMValueError):
                self.processor(job, "linuxcnc").export2()
        self.doc.recompute()
        for job, op, previous in zip(jobs, ops, before):
            current = self.check_export(job, op, "linuxcnc", "tab-edit")
            self.assertNotEqual(current, previous)
            self.assertAlmostEqual(job.HoldingTabs[0].Shape.Volume, tab.Shape.Volume)
        untouched = ops[0].Path.toGCode()
        jobs[1].IndexFrame.Origin = "Custom"
        jobs[1].IndexFrame.CustomOrigin = App.Vector(2, 3, 4)
        with self.assertRaises(CAMValueError):
            self.processor(jobs[1], "grbl").export2()
        self.doc.recompute()
        self.assertEqual(ops[0].Path.toGCode(), untouched)
        self.assertEqual(jobs[1].IndexFrame.Transform.Base, App.Vector(-2, -3, -4))
        self.check_export(jobs[1], ops[1], "grbl", "origin-edit")

    def test_reopen_preserves_saved_paths_and_posts_regenerated_setups(self):
        source, tab, jobs = self.setups()
        ops = [self.make_op(job, "Waterline") for job in jobs]
        names = [(job.Name, op.Name) for job, op in zip(jobs, ops)]
        saved_paths = [op.Path.toGCode() for op in ops]
        for job, op in zip(jobs, ops):
            self.check_export(job, op, "grbl", "before-save")
        with tempfile.TemporaryDirectory() as temp:
            filename = os.path.join(temp, "indexed-output.FCStd")
            self.doc.saveAs(filename)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(filename)
            for (_, op_name), saved in zip(names, saved_paths):
                op = self.doc.getObject(op_name)
                self.assertEqual(op.Path.toGCode(), saved)
                op.touch()
            self.doc.recompute()
            for job_name, op_name in names:
                job, op = self.doc.getObject(job_name), self.doc.getObject(op_name)
                # Regenerated output must match its current native operation
                # and retain tab clearance. Waterline contour repeatability
                # across reopen is a separate, still-open acceptance gate.
                self.check_export(job, op, "grbl", "reopened")



if __name__ == "__main__":
    unittest.main()
