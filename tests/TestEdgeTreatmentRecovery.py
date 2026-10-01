# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native fillet/chamfer task failure recovery and source preservation."""
import tempfile
from pathlib import Path
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets


def settle():
    Gui.updateGui()
    QtWidgets.QApplication.sendPostedEvents(None, QtCore.QEvent.DeferredDelete)


class TestEdgeTreatmentRecovery(unittest.TestCase):
    def setUp(self):
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("EdgeTreatmentTest")
        self.doc.UndoMode = 1
        self.box = self.doc.addObject("Part::Box", "Source")
        self.doc.recompute()
        self.before = self.box.Shape.exportBrepToString()
        self.temp = tempfile.TemporaryDirectory(prefix="freecad-edge-treatment-")

    def tearDown(self):
        if Gui.Control.activeDialog():
            Gui.Control.activeTaskDialog().reject()
            Gui.Control.closeDialog()
        for name in list(App.listDocuments()):
            App.closeDocument(name)
        settle()
        self.temp.cleanup()

    def task(self, operation="Fillet", edges=("Edge1",), edit=None):
        Gui.Selection.clearSelection()
        if edit:
            Gui.activeDocument().setEdit(edit.Name)
        else:
            for edge in edges:
                Gui.Selection.addSelection(self.box, edge)
            Gui.runCommand("Part_" + operation)
        settle()
        labels = [w for w in Gui.getMainWindow().findChildren(QtWidgets.QLabel, "edgeTreatmentReview")
                  if w.isVisible()]
        self.assertEqual(len(labels), 1)
        self.review = labels[0]
        self.panel = self.review.parentWidget()
        self.tree = self.panel.findChild(QtWidgets.QTreeView, "treeView")
        return self.panel

    def radii(self, first, second=None):
        if second is not None:
            combo = self.panel.findChild(QtWidgets.QComboBox, "filletType")
            combo.setCurrentIndex(1)
            combo.activated.emit(1)
        self.panel.findChild(QtWidgets.QWidget, "filletStartRadius").setProperty("rawValue", first)
        if second is not None:
            self.panel.findChild(QtWidgets.QWidget, "filletEndRadius").setProperty("rawValue", second)
        settle()

    def checked(self):
        model = self.tree.model()
        return [model.index(i, 0).data(QtCore.Qt.UserRole) for i in range(model.rowCount())
                if model.index(i, 0).data(QtCore.Qt.CheckStateRole) == 2]

    def accept(self):
        Gui.Control.activeTaskDialog().accept()
        settle()

    def result(self, operation):
        results = [o for o in self.doc.Objects if o.TypeId == "Part::" + operation]
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].isValid())
        self.assertTrue(results[0].Shape.isValid())
        self.assertGreater(results[0].Shape.Volume, 0)
        self.assertLess(results[0].Shape.Volume, self.box.Shape.Volume)
        return results[0]

    def recovery(self, operation):
        self.task(operation, ("Edge1", "Edge3"))
        checked = self.checked()
        self.assertEqual(len(checked), 2)
        undo = self.doc.UndoCount
        self.radii(100.0)
        self.accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.assertIn("failed for the checked set", self.review.text())
        self.assertIn("Edge1", self.review.text())
        self.assertEqual(checked, self.checked())
        self.assertEqual([o.Name for o in self.doc.Objects], ["Source"])
        self.assertFalse(self.doc.HasPendingTransaction)
        self.assertEqual(undo, self.doc.UndoCount)
        self.assertEqual(self.before, self.box.Shape.exportBrepToString())
        self.assertTrue(self.box.Visibility)
        self.radii(1.25)
        self.accept()
        result = self.result(operation)
        self.assertEqual(self.before, self.box.Shape.exportBrepToString())
        self.assertEqual(len(result.Edges), 2)
        self.assertFalse(self.box.Visibility)
        self.assertEqual(self.doc.UndoCount, undo + 1)
        volume = result.Shape.Volume
        result_name = result.Name
        self.doc.undo()
        self.doc.recompute()
        self.assertIsNone(self.doc.getObject(result_name))
        self.assertTrue(self.box.Visibility)
        self.doc.redo()
        self.doc.recompute()
        restored = self.result(operation)
        self.assertAlmostEqual(restored.Shape.Volume, volume, places=7)

    def test_fillet_failure_keeps_edges_then_retry_undo_redo(self):
        self.recovery("Fillet")

    def test_chamfer_failure_keeps_edges_then_retry_undo_redo(self):
        self.recovery("Chamfer")

    def test_no_edges_and_zero_size_do_not_open_transaction(self):
        self.task()
        self.panel.findChild(QtWidgets.QPushButton, "selectNoneButton").click()
        self.accept()
        self.assertIn("Check at least one", self.review.text())
        self.assertFalse(self.doc.HasPendingTransaction)
        model = self.tree.model()
        model.setData(model.index(0, 0), 2, QtCore.Qt.CheckStateRole)
        self.radii(0.0)
        self.accept()
        self.assertIn("positive finite", self.review.text())
        self.assertFalse(self.doc.HasPendingTransaction)
        self.assertEqual(len(self.doc.Objects), 1)

    def test_changed_source_requires_fresh_edge_review(self):
        self.task()
        self.box.Length = 15
        self.doc.recompute()
        self.accept()
        self.assertIn("source shape changed", self.review.text())
        self.assertEqual(len(self.doc.Objects), 1)

    def test_variable_fillet_and_downstream_reopen(self):
        self.task()
        self.radii(0.75, 1.5)
        self.accept()
        result = self.result("Fillet")
        self.assertEqual(result.Edges, [(1, 0.75, 1.5)])
        consumer = self.doc.addObject("App::Link", "Consumer")
        consumer.setLink(result)
        self.doc.recompute()
        path = Path(self.temp.name) / "Variable-Fillet.FCStd"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(path))
        self.box = self.doc.Source
        self.box.Height = 14
        self.doc.recompute()
        result = self.result("Fillet")
        self.assertAlmostEqual(self.doc.Consumer.Shape.Volume, result.Shape.Volume, places=7)
        self.assertEqual(result.Edges, [(1, 0.75, 1.5)])

    def test_two_distance_chamfer(self):
        self.task("Chamfer")
        self.radii(0.75, 1.5)
        self.accept()
        result = self.result("Chamfer")
        self.assertEqual(result.Edges, [(1, 0.75, 1.5)])
        self.assertEqual(self.before, self.box.Shape.exportBrepToString())

    def test_failed_edit_preserves_previous_result_then_cancel(self):
        result = self.doc.addObject("Part::Fillet", "Fillet")
        result.Base = self.box
        result.Edges = [(1, 1.0, 1.0)]
        self.doc.recompute()
        previous = result.Shape.exportBrepToString()
        self.task(edit=result)
        self.radii(100.0)
        self.accept()
        self.assertTrue(Gui.Control.activeDialog())
        self.assertIn("failed for the checked set", self.review.text())
        self.assertEqual(result.Edges, [(1, 1.0, 1.0)])
        self.assertEqual(result.Shape.exportBrepToString(), previous)
        Gui.Control.activeTaskDialog().reject()
        self.assertEqual(self.before, self.box.Shape.exportBrepToString())

    def test_entered_precision_is_not_display_rounded(self):
        self.task()
        self.radii(1.23456789)
        entered = self.panel.findChild(QtWidgets.QWidget, "filletStartRadius").property("rawValue")
        self.accept()
        result = self.result("Fillet")
        self.assertAlmostEqual(result.Edges[0][1], entered, places=12)
