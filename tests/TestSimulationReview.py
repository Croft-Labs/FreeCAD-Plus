# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native CAM input review with complete preparation before simulator handoff."""
from pathlib import Path as FilePath
import tempfile
from unittest.mock import MagicMock, patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets
from CAMTests.PathTestUtils import PathTestWithAssets
from Path.Main import Job, SimulationReview as Review
from Path.Main.Gui import SimulatorGL as UI
from Path.Op import Custom
from Path.Tool import Controller


class TestSimulationReview(PathTestWithAssets):
    def setUp(self):
        super().setUp()
        Gui.activateWorkbench("CAMWorkbench")
        self.doc = App.newDocument("SimulationReview")
        self.doc.UndoMode = 1
        model = self.doc.addObject("Part::Box", "Model")
        model.Length, model.Width, model.Height = 12, 10, 5
        self.doc.recompute()
        self.job = Job.Create("Job", [model])
        self.tool = self.assets.get("toolbit://5mm_Endmill").attach_to_doc(doc=self.doc)
        self.tc = self.job.Tools.Group[0]
        self.tc.Tool = self.tool
        self.tc.ToolNumber = 1
        self.ops = []
        for name, y in (("ZFirst", 3), ("ASecond", 7)):
            op = Custom.Create(name, parentJob=self.job)
            op.ToolController = self.tc
            op.Gcode = ["G90", "G0 X0 Y%d Z8" % y, "G1 Z3 F120", "G1 X12 F600", "G0 Z8"]
            self.ops.append(op)
        self.doc.recompute()
        self.sim = UI.CAMSimulation()
        self.active = False

    def tearDown(self):
        self.sim.cancel()
        if Gui.Control.activeDialog():Gui.Control.closeDialog()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):App.closeDocument(name)
        # Document-close task disposal is queued by the native task panel.
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(100, loop.quit)
        loop.exec_()
        Gui.updateGui()
        super().tearDown()

    def prepare(self, ops=None):
        return Review.prepare(self.job, self.ops if ops is None else ops, 5, self.sim.GetToolProfile)

    def launch(self):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(self.job)
        self.sim.Activate()
        self.active = True
        return self.sim.taskForm.form

    def test_native_review_order_stock_tools_and_source_preservation(self):
        before = [(o.Name, o.Content) for o in self.doc.Objects]
        undo = self.doc.UndoCount
        review = self.prepare()
        self.assertEqual([e["name"] for e in review["operations"]], [o.Name for o in self.ops])
        self.assertEqual(len(review["tools"]), 1)
        self.assertAlmostEqual(review["tools"][0]["diameter"], 5)
        self.assertGreater(len(review["tools"][0]["profile"]), 4)
        self.assertAlmostEqual(review["stock"].Volume, self.job.Stock.Shape.Volume)
        self.assertIn("ZFirst", Review.describe(review))
        self.assertEqual([(o.Name, o.Content) for o in self.doc.Objects], before)
        self.assertEqual(self.doc.UndoCount, undo)

    def test_missing_second_tool_prevents_any_native_session_reset(self):
        self.launch()
        self.sim.millSim = MagicMock()
        self.ops[1].ToolController = None
        self.doc.recompute()
        self.sim.SimPlay()
        self.sim.millSim.ResetSimulation.assert_not_called()
        self.sim.millSim.BeginSimulation.assert_not_called()
        self.assertIsNone(self.sim.review)
        self.assertIn("Missing tool", self.sim.reviewText.toPlainText())

    def test_selection_follows_job_group_order_and_empty_disables_play(self):
        form = self.launch()
        self.assertEqual(self.sim.operations, self.ops)
        self.job.Operations.Group = list(reversed(self.ops))
        self.doc.recompute()
        self.sim.refreshReview()
        self.assertEqual([e["name"] for e in self.sim.review["operations"]],
                         [op.Name for op in reversed(self.ops)])
        self.assertTrue(form.toolButtonPlay.isEnabled(), self.sim.reviewText.toPlainText())
        for index in range(form.listOperations.count()):
            form.listOperations.item(index).setCheckState(QtCore.Qt.Unchecked)
        self.assertFalse(form.toolButtonPlay.isEnabled())
        self.assertIn("at least one", self.sim.reviewText.toPlainText())
        form.listOperations.item(1).setCheckState(QtCore.Qt.Checked)
        self.assertTrue(form.toolButtonPlay.isEnabled(), self.sim.reviewText.toPlainText())
        self.assertEqual(self.sim.review["operations"][0]["name"], self.ops[1].Name)
        self.assertIn("before postprocessing", self.sim.scopeText.text())
        self.assertIn("not checked", self.sim.scopeText.text())

    def test_tool_number_collision_and_profile_failure(self):
        second_tool = self.assets.get("toolbit://5mm_Endmill").attach_to_doc(doc=self.doc)
        tc = Controller.Create("OtherController", tool=second_tool, toolNumber=1)
        self.job.Tools.addObject(tc)
        self.ops[1].ToolController = tc
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "share tool number"):
            self.prepare()
        tc.ToolNumber = 2
        self.doc.recompute()
        self.assertEqual(len(self.prepare()["tools"]), 2)
        with self.assertRaisesRegex(ValueError, "profile"):
            Review.prepare(self.job, self.ops, 5, lambda *_: [])

    def test_changed_inputs_need_new_review_and_handoff_keeps_tool_sequence(self):
        self.launch()
        sink = self.sim.millSim = MagicMock()
        self.ops[0].Gcode = ["G0 X2 Y3 Z8", "G1 Z2 F100", "G1 X10 F500"]
        self.doc.recompute()
        self.assertFalse(self.sim.taskForm.form.toolButtonPlay.isEnabled())
        self.sim.SimPlay()
        sink.ResetSimulation.assert_not_called()
        self.assertIn("Inputs changed", self.sim.reviewText.toPlainText())
        self.sim.SimPlay()
        sink.BeginSimulation.assert_called_once()
        names = [call[0] for call in sink.method_calls]
        self.assertEqual(names[0], "ResetSimulation")
        self.assertEqual(names.count("AddTool"), 2)
        indexes = [i for i, name in enumerate(names) if name == "AddTool"]
        self.assertGreater(indexes[1], indexes[0] + 1)
        self.assertTrue(all(n == "AddCommand" for n in names[indexes[0]+1:indexes[1]]))
        self.assertEqual(names[-2:], ["BeginSimulation", "SetBaseShape"])

    def test_stale_stock_inactive_and_foreign_operations_refused(self):
        self.job.Stock.ExtXpos = 7
        with self.assertRaisesRegex(ValueError, "not current"):
            self.prepare()
        self.doc.recompute()
        self.ops[0].Active = False
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "inactive"):
            self.prepare()
        with self.assertRaisesRegex(ValueError, "more than once"):
            self.prepare([self.ops[1], self.ops[1]])
        self.assertEqual(len(self.prepare([self.ops[1]])["operations"]), 1)

    def test_reopen_review_uses_saved_operations_and_current_stock(self):
        expected = self.prepare()
        with tempfile.TemporaryDirectory() as folder:
            filename = str(FilePath(folder) / "Simulation.FCStd")
            self.doc.saveAs(filename)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(filename)
            self.job = self.doc.Job
            self.ops = list(self.job.Operations.Group)
            self.doc.recompute()
            reopened = self.prepare()
            self.assertEqual([e["name"] for e in reopened["operations"]], [e["name"] for e in expected["operations"]])
            self.assertAlmostEqual(reopened["stock"].Volume, expected["stock"].Volume)
            self.assertEqual([c.toGCode() for c in reopened["operations"][0]["commands"]],
                             [c.toGCode() for c in expected["operations"][0]["commands"]])

    def test_native_simulator_accepts_prepared_stock_and_paths(self):
        self.launch()
        before = [(o.Name, o.Content) for o in self.doc.Objects]
        self.sim.SimPlay()
        self.assertNotIn("could not start", self.sim.reviewText.toPlainText())
        self.assertIsNotNone(self.sim.review)
        Gui.updateGui()
        self.assertEqual([(o.Name, o.Content) for o in self.doc.Objects], before)
        views = Gui.activeDocument().mdiViewsOfType("CAMSimulator::ViewCAMSimulator")
        self.assertEqual(len(views), 1)
        self.assertEqual(Gui.activeDocument().activeView(), views[0])

    def test_document_close_detaches_input_observer(self):
        self.launch()
        self.assertTrue(self.sim.observing)
        App.closeDocument(self.doc.Name)
        self.assertFalse(self.sim.observing)
        self.assertFalse(Gui.Control.activeDialog())
        # A deleted document must not leave a task registered at a recycled address.
        self.doc = App.newDocument("NextSimulation")
        model = self.doc.addObject("Part::Box", "Model")
        self.doc.recompute()
        self.job = Job.Create("Job", [model])
        self.doc.recompute()
        self.sim = UI.CAMSimulation()
        self.launch()
        self.assertTrue(Gui.Control.activeDialog())
