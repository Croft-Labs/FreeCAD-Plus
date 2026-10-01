# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native New Job source identity, dimensional review and setup handoff."""
from pathlib import Path
import tempfile
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Mesh
import Part
from PySide import QtCore, QtWidgets
from Path.Main import Job
from Path.Main.Gui import Job as JobGui, JobDlg


def settle():
    Gui.updateGui()
    QtCore.QCoreApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)


class TestJobModelReview(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("CAMWorkbench")
        self.doc = App.newDocument("JobModelReview")
        self.doc.UndoMode = 1
        self.dialogs = []
        self.prefs = App.ParamGet("User parameter:BaseApp/Preferences/Document")
        self.duplicate_labels = self.prefs.GetBool("DuplicateLabels", False)
        self.prefs.SetBool("DuplicateLabels", True)

    def tearDown(self):
        for dialog in self.dialogs:
            dialog.dialog.reject()
            dialog.dialog.deleteLater()
        if Gui.Control.activeDialog():
            Gui.Control.closeDialog()
        Gui.Selection.clearSelection()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        self.prefs.SetBool("DuplicateLabels", self.duplicate_labels)
        settle()

    def box(self, name="Model", length=12):
        obj = self.doc.addObject("Part::Box", name)
        obj.Length, obj.Width, obj.Height = length, 10, 5
        self.doc.recompute()
        return obj

    def mesh(self):
        obj = self.doc.addObject("Mesh::Feature", "ImportedMesh")
        obj.Mesh = Mesh.Mesh(Part.makeBox(12, 10, 5).tessellate(0.1))
        obj.Placement.Base = App.Vector(17, 13, 2)
        self.doc.recompute()
        return obj

    def picker(self, selected=None, job=None):
        Gui.Selection.clearSelection()
        for obj in selected or []:
            Gui.Selection.addSelection(obj)
        dialog = JobDlg.JobCreate()
        self.dialogs.append(dialog)
        if not job:
            dialog.dialog.jobTemplate.addItem("No template", "")
            dialog.dialog.templateGroup.show()
            dialog.reviewTemplate()
        dialog.setupModel(job)
        return dialog

    def snapshot(self):
        return ([o.Name for o in self.doc.Objects], self.doc.UndoCount, self.doc.UnitSystem)

    def testDuplicateLabelsSelectOnlyIntendedIdentity(self):
        first, second = self.box(), self.box("Other", 30)
        first.Label = second.Label = "Same label"
        self.assertEqual(first.Label, second.Label)
        dialog = self.picker([second])
        self.assertEqual(dialog.getModels(), [second])
        self.assertIn("[Other]", dialog.modelReview.toPlainText())
        self.assertNotIn("[Model]", dialog.modelReview.toPlainText())
        self.assertIn("30 x 10 x 5 mm", dialog.modelReview.toPlainText())
        tips = [dialog.itemsSolid.child(i).toolTip() for i in range(2)]
        self.assertIn("Same label [Other]", tips)

    def testMeshBoundsAndUnitDisplayDoNotRescale(self):
        obj = self.mesh()
        before = (self.snapshot(), obj.Mesh.Topology, tuple(obj.Placement.toMatrix().A))
        dialog = self.picker([obj])
        self.assertEqual(dialog.itemsMesh.rowCount(), 1)
        self.assertEqual(dialog.getModels(), [obj])
        text = dialog.modelReview.toPlainText()
        self.assertIn("12 x 10 x 5 mm", text)
        self.assertIn("min (17, 13, 2) mm", text)
        self.assertIn("STL has no declared units", text)
        combo = dialog.dialog.unitSchemaCombo
        combo.setCurrentIndex((combo.currentIndex() + 1) % combo.count())
        self.assertIn("12 x 10 x 5 mm", dialog.modelReview.toPlainText())
        self.assertEqual(before, (self.snapshot(), obj.Mesh.Topology, tuple(obj.Placement.toMatrix().A)))

    def testExistingJobEditorRetainsCountsByIdentity(self):
        first, second = self.box(), self.box("Other", 30)
        first.Label = second.Label = "Same label"
        self.assertEqual(first.Label, second.Label)
        job = Job.Create("Job", [second, second])
        self.doc.recompute()
        dialog = self.picker(job=job)
        self.assertEqual(dialog.getModels(), [second, second])
        self.assertTrue(dialog.dialog.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).isEnabled())
        self.assertIn("BRep x 2", dialog.modelReview.toPlainText())
        dialog.acceptReviewedTemplate()
        self.assertEqual(dialog.dialog.result(), 1)

    def testEmptyStaleAndDeletedInputsCannotAccept(self):
        first, second = self.box(), self.box("Other")
        dialog = self.picker()
        self.assertFalse(dialog._modelReady)
        self.assertIn("Select at least one", dialog.modelReview.toPlainText())
        # Template refresh cannot re-enable an empty model selection.
        dialog.reviewTemplate()
        self.assertFalse(dialog.dialog.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).isEnabled())
        selected = self.picker([first])
        first.touch()
        selected.acceptReviewedTemplate()
        self.assertNotEqual(selected.dialog.result(), 1)
        self.doc.recompute()
        self.assertTrue(selected.reviewModels())
        self.doc.removeObject(first.Name)
        selected.acceptReviewedTemplate()
        self.assertNotEqual(selected.dialog.result(), 1)
        self.assertIn("Cannot use selected models", selected.modelReview.toPlainText())

    def testChangedShapeRequiresRenewedReview(self):
        obj = self.box()
        dialog = self.picker([obj])
        obj.Length = 25
        self.doc.recompute()
        before = self.snapshot()
        dialog.acceptReviewedTemplate()
        self.assertNotEqual(dialog.dialog.result(), 1)
        self.assertIn("Models changed", dialog.modelReview.toPlainText())
        self.assertIn("25 x 10 x 5 mm", dialog.modelReview.toPlainText())
        dialog.acceptReviewedTemplate()
        self.assertEqual(dialog.dialog.result(), 1)
        self.assertEqual(before, self.snapshot())

    def testModalSelectionUpdatesReviewAndCancelPreservesUnits(self):
        first, second = self.box(), self.box("Other", 25)
        dialog = self.picker([first])
        before = self.snapshot()
        observed = []
        def interact():
            for i in range(dialog.itemsSolid.rowCount()):
                item = dialog.itemsSolid.child(i)
                if item.data(dialog.DataObject) == second:
                    item.setCheckState(QtCore.Qt.Checked)
            combo = dialog.dialog.unitSchemaCombo
            combo.setCurrentIndex((combo.currentIndex() + 1) % combo.count())
            observed.append(dialog.modelReview.toPlainText())
            dialog.dialog.reject()
        QtCore.QTimer.singleShot(100, interact)
        self.assertEqual(dialog.exec_(), 0)
        self.assertIn("25 x 10 x 5 mm", observed[0])
        self.assertEqual(before, self.snapshot())

    def testModelContextChangeIsRefused(self):
        obj = self.box()
        dialog = self.picker([obj])
        other = App.newDocument("OtherDoc")
        dialog.acceptReviewedTemplate()
        self.assertNotEqual(dialog.dialog.result(), 1)
        self.assertIn("original model document", dialog.modelReview.toPlainText())

    def testReviewedMeshAndSolidJobsPersistWithNativeResources(self):
        mesh, solid = self.mesh(), self.box()
        with tempfile.TemporaryDirectory() as folder:
            names = []
            for source in (mesh, solid):
                dialog = self.picker([source])
                dialog.acceptReviewedTemplate()
                self.assertEqual(dialog.dialog.result(), 1)
                job = JobGui.Create(dialog.getModels(), dialog.getTemplateSettings(), openTaskPanel=False)
                self.assertIsNotNone(job)
                names.append(job.Name)
                self.assertEqual(job.Proxy.baseObject(job, job.Model.Group[0]), source)
                self.assertAlmostEqual(job.Model.Group[0].Placement.Base.x, source.Placement.Base.x)
                self.assertTrue(job.Stock.Shape.isValid())
                self.assertTrue(job.Tools.Group)
                self.doc.undo()
                self.assertIsNone(self.doc.getObject(names[-1]))
                self.doc.redo()
                self.doc.recompute()
            filename = str(Path(folder) / "ReviewedJobs.FCStd")
            self.doc.saveAs(filename)
            App.closeDocument(self.doc.Name)
            self.doc = App.openDocument(filename)
            self.doc.recompute()
            for name in names:
                job = self.doc.getObject(name)
                self.assertTrue(job.Stock.Shape.isValid())
                self.assertTrue(job.Tools.Group)
                self.assertEqual(job.Operations.Group, [])
            self.assertAlmostEqual(self.doc.getObject(names[0]).Model.Group[0].Mesh.BoundBox.XMin, 17)
