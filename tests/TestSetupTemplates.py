# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native CAM setup-template reuse, review and isolation."""
import copy
import json
import tempfile
from pathlib import Path as FilePath
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
import Path
from PySide import QtWidgets
from CAMTests.PathTestUtils import PathTestWithAssets
from Path.Main import Job, Template
from Path.Main.Gui import Job as JobGui, JobCmd, JobDlg


class TestSetupTemplates(PathTestWithAssets):
    def setUp(self):
        super().setUp()
        Gui.activateWorkbench("CAMWorkbench")
        self.doc = App.newDocument("SetupTemplates")
        self.doc.UndoMode = 1
        self.directory = tempfile.TemporaryDirectory()
        self.filename = FilePath(self.directory.name) / "job_owner's_setup.json"
        self.dialogs = []

    def tearDown(self):
        for dialog in self.dialogs:
            dialog.dialog.reject()
        if Gui.Control.activeDialog():
            Gui.Control.closeDialog()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        self.directory.cleanup()
        super().tearDown()

    def model(self, length=12):
        model = self.doc.addObject("Part::Box", "Model")
        model.Length, model.Width, model.Height = length, 10, 5
        self.doc.recompute()
        return model

    def fixture(self):
        model = self.model()
        job = Job.Create("Job", [model])
        tool = self.assets.get("toolbit://5mm_Endmill").attach_to_doc(doc=self.doc)
        controller = job.Tools.Group[0]
        controller.Tool = tool
        controller.HorizFeed, controller.VertFeed = "600 mm/min", "120 mm/min"
        job.Stock.ExtXneg, job.Stock.ExtXpos = 2, 3
        job.Stock.ExtYneg, job.Stock.ExtYpos = 1, 1
        job.Stock.ExtZneg, job.Stock.ExtZpos = 0, 2
        posts = Path.Preferences.allEnabledLegacyPostProcessors()
        self.assertTrue(posts)
        job.PostProcessor = "linuxcnc" if "linuxcnc" in posts else posts[0]
        job.PostProcessorArgs = "--no-show-editor"
        job.Description = "Reusable 5 mm cutter and model-bound stock"
        self.doc.recompute()
        JobCmd.CommandJobTemplateExport.Execute(job, self.filename)
        return job, model, Template.read(self.filename)

    def write(self, attrs):
        self.filename.write_text(json.dumps(attrs), encoding="utf-8")

    def picker(self, attrs):
        self.write(attrs)
        dialog = JobDlg.JobCreate()
        self.dialogs.append(dialog)
        dialog.dialog.jobTemplate.addItem("Fixture", str(self.filename))
        dialog.dialog.templateGroup.show()
        dialog.setupModel()
        dialog.reviewTemplate()
        return dialog

    def testExportMetadataAndEditableNativeReuse(self):
        source, old_model, attrs = self.fixture()
        self.assertEqual(attrs["TemplateInfo"]["Units"], Template.UNITS)
        new_model = self.model(30)
        original = old_model.Shape.exportBrepToString()
        new = JobGui.Create([new_model], str(self.filename), openTaskPanel=False)
        self.assertIsNotNone(new)
        self.assertEqual(new.PostProcessor, source.PostProcessor)
        self.assertEqual(new.PostProcessorArgs, source.PostProcessorArgs)
        self.assertEqual(new.TemplateName, source.Label)
        self.assertEqual(new.TemplateRevision, "1")
        self.assertEqual(new.Proxy.baseObject(new, new.Model.Group[0]), new_model)
        self.assertAlmostEqual(new.Stock.Shape.BoundBox.XLength, 35)
        self.assertAlmostEqual(source.Stock.Shape.BoundBox.XLength, 17)
        self.assertAlmostEqual(new.Tools.Group[0].HorizFeed.Value, 10)
        self.assertEqual(new.Operations.Group, [])
        self.assertNotEqual(new.Tools.Group[0].Tool, source.Tools.Group[0].Tool)
        self.assertEqual(original, old_model.Shape.exportBrepToString())
        attrs["PostArgs"] = "changed later"
        self.write(attrs)
        self.doc.recompute()
        self.assertEqual(new.PostProcessorArgs, "--no-show-editor")

    def testInvalidCompatibilityBeforeAnyResourceCreation(self):
        model = self.model()
        cases = [
            {"Version": 9},
            {"Version": 1, "Post": "missing_post_xyz"},
            {"Version": 1, "Tolerance": "0"},
            {"Version": 1, "TemplateInfo": {"Units": "inch"}},
            {"Version": 1, "Operations": ["OldPocket"]},
            {"Version": 1, "Stock": {"version": 1, "create": "FromBase", "xneg": 2}},
            {"Version": 1, "SetupSheet": {"StartDepthExpression": "OldModel.Height"}},
            {"Version": 1, "ToolController": [{"version": 1, "tool": {"version": 1}}]},
        ]
        before = (list(self.doc.Objects), self.doc.UndoCount, model.Shape.exportBrepToString())
        for attrs in cases:
            with self.subTest(attrs=attrs):
                self.write(attrs)
                with self.assertRaises(ValueError):
                    Job.Create("RejectedJob", [model], self.filename)
                self.assertEqual(before, (list(self.doc.Objects), self.doc.UndoCount,
                                          model.Shape.exportBrepToString()))

    def testPortableSetupExpressionsRebindToNewJob(self):
        source, _, attrs = self.fixture()
        attrs["SetupSheet"] = {
            "SafeHeightExpression": "OpStockZMax+${SetupSheet}.SafeHeightOffset",
            "SafeHeightOffset": "4 mm",
        }
        new = JobGui.Create([self.model(22)], attrs, openTaskPanel=False)
        self.assertIsNotNone(new)
        self.assertIn(new.SetupSheet.Name + ".SafeHeightOffset", new.SetupSheet.SafeHeightExpression)
        self.assertNotEqual(new.SetupSheet, source.SetupSheet)
        self.assertAlmostEqual(new.SetupSheet.SafeHeightOffset.Value, 4)

    def testReviewInvalidChangedFileAndAcceptedSnapshot(self):
        self.model()
        dialog = self.picker({"Version": 1, "Post": "missing_post_xyz"})
        ok = dialog.dialog.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        self.assertFalse(ok.isEnabled())
        self.assertIn("Cannot use", dialog.templateReview.toPlainText())
        attrs = {"Version": 1, "TemplateInfo": {"Name": "Metric fixture", "Revision": "A"}}
        self.write(attrs)
        self.assertTrue(dialog.reviewTemplate())
        self.assertTrue(ok.isEnabled())
        self.assertIn("No operation sequence", dialog.templateReview.toPlainText())
        attrs["TemplateInfo"]["Revision"] = "B"
        self.write(attrs)
        dialog.acceptReviewedTemplate()
        self.assertNotEqual(dialog.dialog.result(), 1)
        self.assertIn("Template changed", dialog.templateReview.toPlainText())
        dialog.acceptReviewedTemplate()
        self.assertEqual(dialog.dialog.result(), 1)
        attrs["TemplateInfo"]["Revision"] = "C"
        self.write(attrs)
        new = JobGui.Create([self.model(24)], dialog.getTemplateSettings(), openTaskPanel=False)
        self.assertEqual(new.TemplateRevision, "B")

    def testExportDialogMetadataAndPostExclusion(self):
        job, _, _ = self.fixture()
        job.PostProcessorPropertyOverrides = '{"fixture": "value"}'
        dialog = JobDlg.JobTemplateExport(job)
        self.dialogs.append(dialog)
        dialog.nameEdit.setText("Owner fixture")
        dialog.revisionEdit.setText("B2")
        dialog.dialog.postProcessingGroup.setChecked(False)
        JobCmd.CommandJobTemplateExport.Execute(job, self.filename, dialog)
        attrs = Template.read(self.filename)
        self.assertEqual(attrs["TemplateInfo"]["Name"], "Owner fixture")
        self.assertEqual(attrs["TemplateInfo"]["Revision"], "B2")
        self.assertNotIn("Post", attrs)
        self.assertNotIn("PostPropertyOverrides", attrs)
        self.assertNotIn("TemplateName", job.PropertiesList)

    def testUndoRedoSaveReopenAndModelUpdate(self):
        _, _, attrs = self.fixture()
        model = self.model(25)
        new = JobGui.Create([model], attrs, openTaskPanel=False)
        name, model_name = new.Name, model.Name
        self.doc.undo()
        self.assertIsNone(self.doc.getObject(name))
        self.doc.redo()
        self.doc.recompute()
        filename = str(FilePath(self.directory.name) / "ReusedSetup.FCStd")
        self.doc.saveAs(filename)
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(filename)
        self.doc.getObject(model_name).Length = 40
        self.doc.recompute()
        new = self.doc.getObject(name)
        self.assertEqual(new.TemplateRevision, "1")
        self.assertAlmostEqual(new.Stock.Shape.BoundBox.XLength, 45)
        self.assertAlmostEqual(new.Tools.Group[0].HorizFeed.Value, 10)
        self.assertEqual(new.Operations.Group, [])

    def testInstantiationFailureRollsBackNativeGuiTransaction(self):
        _, _, attrs = self.fixture()
        model = self.model(24)
        before = set(o.Name for o in self.doc.Objects)
        with patch("Path.Main.Stock.CreateFromTemplate", side_effect=RuntimeError("fixture failure")):
            new = JobGui.Create([model], attrs, openTaskPanel=False)
        self.assertIsNone(new)
        self.assertEqual(set(o.Name for o in self.doc.Objects), before)

    def testLegacyTemplateAndCommandLiteralQuoting(self):
        self.model()
        dialog = self.picker({"Version": "1", "Desc": "Legacy fixture"})
        self.assertIn("legacy convention", dialog.templateReview.toPlainText())
        self.assertIn("Not recorded", dialog.templateReview.toPlainText())
        with patch.object(Gui, "doCommand") as command:
            JobCmd.CommandJobCreate.Execute([self.doc.Model], str(self.filename))
        import ast
        expression = ast.parse(command.call_args.args[0]).body[0].value
        self.assertEqual(ast.literal_eval(expression.args[1]), str(self.filename))
        dialog.dialog.reject()
        self.assertEqual(len(self.doc.Objects), 1)
