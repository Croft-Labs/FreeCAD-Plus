# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Qt checks for the uninstalled parameter editor prototype."""
import unittest
import FreeCAD as App
import FreeCADGui as Gui
from prototypes.ParameterEditor import ParameterEditor
from prototypes.NamedParameters import set_length_expression


class TestParameterEditor(unittest.TestCase):
    def setUp(self):
        self.doc = App.newDocument("ParameterEditorProof")
        self.doc.UndoMode = 1
        self.parameters = self.doc.addObject("App::FeaturePython", "Parameters")
        self.parameters.addProperty("App::PropertyLength", "Width", "Dimensions")
        self.parameters.Width = "25 mm"
        self.parameters.addProperty("App::PropertyAngle", "Tilt", "Dimensions")
        self.parameters.Tilt = "30 deg"
        self.box = self.doc.addObject("Part::Box", "Consumer")
        set_length_expression(self.box, "Length", "Parameters.Width")
        self.doc.recompute()
        self.editor = ParameterEditor(self.parameters)
        self.editor.show()
        self.editor.parameter.setCurrentIndex(self.editor.parameter.findText("Width"))
        Gui.updateGui()

    def tearDown(self):
        self.editor.close()
        self.editor.deleteLater()
        Gui.updateGui()
        if self.doc is not None:
            App.closeDocument(self.doc.Name)

    def testApplyAndCloseHaveExplicitCommitBoundaries(self):
        self.assertTrue(self.editor.value.isReadOnly())
        self.editor.expression.setText("40 mm")
        self.assertAlmostEqual(self.parameters.Width.Value, 25)
        self.editor.apply.click()
        self.assertEqual(self.editor.error.text(), "")
        self.assertAlmostEqual(self.box.Shape.BoundBox.XLength, 40)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.editor.expression.setText("55 mm")
        self.editor.closeButton.click()
        self.assertAlmostEqual(self.parameters.Width.Value, 40)
        self.doc.undo()
        self.doc.recompute()
        self.assertAlmostEqual(self.box.Length.Value, 25)

    def testInvalidExpressionAndGeometryRemainEditable(self):
        for expression in ("30 deg", "0 mm"):
            self.editor.expression.setText(expression)
            self.editor.apply.click()
            self.assertTrue(self.editor.error.text())
            self.assertTrue(self.editor.isVisible())
            self.assertEqual(self.editor.expression.text(), expression)
            self.assertAlmostEqual(self.box.Shape.BoundBox.XLength, 25)
            self.assertFalse(self.doc.HasPendingTransaction)
        self.editor.expression.setText("35 mm")
        self.editor.apply.click()
        self.assertEqual(self.editor.error.text(), "")
        self.assertAlmostEqual(self.box.Shape.BoundBox.XLength, 35)
        self.editor.parameter.setCurrentIndex(self.editor.parameter.findText("Tilt"))
        self.editor.expression.setText("45 deg")
        self.editor.apply.click()
        self.assertEqual(self.editor.error.text(), "")
        self.assertAlmostEqual(self.parameters.Tilt.Value, 45)

    def testRenameFailureThenCorrectionRefreshesSelection(self):
        self.editor.name.setText("Tilt")
        self.editor.rename.click()
        self.assertTrue(self.editor.error.text())
        self.assertEqual(self.editor.parameter.currentText(), "Width")
        self.editor.name.setText("PanelWidth")
        self.editor.rename.click()
        self.assertEqual(self.editor.error.text(), "")
        self.assertEqual(self.editor.parameter.currentText(), "PanelWidth")
        self.assertIn("Parameters.PanelWidth", str(self.box.ExpressionEngine))
        self.editor.expression.setText("32 mm")
        self.editor.apply.click()
        self.assertAlmostEqual(self.box.Shape.BoundBox.XLength, 32)

    def testExternalEditRequiresExplicitRefreshBeforeApplyOrRename(self):
        self.editor.expression.setText("40 mm")
        self.parameters.Width = "28 mm"
        self.doc.recompute()
        self.editor.apply.click()
        self.assertIn("Refresh", self.editor.error.text())
        self.assertEqual(self.editor.expression.text(), "40 mm")
        self.assertAlmostEqual(self.parameters.Width.Value, 28)
        self.editor.name.setText("PanelWidth")
        self.editor.rename.click()
        self.assertIn("Refresh", self.editor.error.text())
        self.assertIn("Width", self.parameters.PropertiesList)
        self.editor.refreshButton.click()
        self.assertEqual(self.editor.error.text(), "")
        self.assertEqual(self.editor.name.text(), "Width")
        self.assertEqual(self.editor.expression.text(), "")
        self.editor.expression.setText("41 mm")
        self.editor.apply.click()
        self.assertAlmostEqual(self.box.Length.Value, 41)
        self.doc.undo()
        self.doc.recompute()
        self.editor.apply.click()
        self.assertIn("Refresh", self.editor.error.text())
        self.editor.refreshButton.click()
        self.assertIn("28", self.editor.value.text())

    def testParameterDeletionClosesEditorAndDisablesFurtherActions(self):
        self.doc.removeObject(self.parameters.Name)
        Gui.updateGui()
        self.assertFalse(self.editor.isVisible())
        self.assertTrue(self.editor._closed)
        self.editor.applyExpression()
        self.editor.renameParameter()
        self.editor.refresh()
        self.assertFalse(self.doc.HasPendingTransaction)

    def testDocumentClosureClosesEditor(self):
        name = self.doc.Name
        App.closeDocument(name)
        self.doc = None
        Gui.updateGui()
        self.assertFalse(self.editor.isVisible())
        self.assertTrue(self.editor._closed)
        self.editor.applyExpression()
        self.editor.renameParameter()
        self.editor.refresh()

    def testExternalPropertyRenameAndRemovalRequireRefresh(self):
        self.parameters.renameProperty("Width", "PanelWidth")
        self.doc.recompute()
        self.editor.parameter.setCurrentIndex(self.editor.parameter.findText("Tilt"))
        self.assertIn("Refresh", self.editor.error.text())
        self.assertFalse(self.editor.apply.isEnabled())
        self.assertFalse(self.editor.rename.isEnabled())
        self.assertEqual(self.editor.value.text(), "")
        self.editor.refreshButton.click()
        self.assertEqual(self.editor.parameter.findText("Width"), -1)
        self.editor.parameter.setCurrentIndex(self.editor.parameter.findText("PanelWidth"))
        self.editor.expression.setText("33 mm")
        self.editor.apply.click()
        self.assertEqual(self.editor.error.text(), "")
        self.assertAlmostEqual(self.box.Length.Value, 33)
        self.parameters.removeProperty("Tilt")
        self.editor.loadParameter()
        self.assertIn("Refresh", self.editor.error.text())
        self.editor.refreshButton.click()
        self.assertEqual(self.editor.parameter.count(), 1)
        self.assertTrue(self.editor.apply.isEnabled())

    def testEmptyParameterListAndExternalAdditionRecover(self):
        self.doc.removeObject(self.box.Name)
        self.parameters.removeProperty("Width")
        self.parameters.removeProperty("Tilt")
        self.doc.recompute()
        self.editor.refreshButton.click()
        self.assertEqual(self.editor.parameter.count(), 0)
        self.assertFalse(self.editor.apply.isEnabled())
        self.assertFalse(self.editor.rename.isEnabled())
        self.assertEqual(self.editor.value.text(), "")
        self.parameters.addProperty("App::PropertyLength", "NewWidth", "Dimensions")
        self.parameters.NewWidth = "17 mm"
        self.doc.recompute()
        self.editor.refreshButton.click()
        self.assertEqual(self.editor.parameter.currentText(), "NewWidth")
        self.assertTrue(self.editor.apply.isEnabled())
        self.editor.expression.setText("19 mm")
        self.editor.apply.click()
        self.assertEqual(self.editor.error.text(), "")
        self.assertAlmostEqual(self.parameters.NewWidth.Value, 19)

    def testTwoEditorsPreserveEachOthersCommitsAndLifecycle(self):
        other = ParameterEditor(self.parameters)
        try:
            other.show()
            other.parameter.setCurrentIndex(other.parameter.findText("Width"))
            other.expression.setText("50 mm")
            self.editor.expression.setText("36 mm")
            self.editor.apply.click()
            other.apply.click()
            self.assertIn("Refresh", other.error.text())
            self.assertEqual(other.expression.text(), "50 mm")
            self.assertAlmostEqual(self.box.Length.Value, 36)
            other.refreshButton.click()
            other.expression.setText("38 mm")
            other.apply.click()
            self.assertEqual(other.error.text(), "")
            self.assertAlmostEqual(self.box.Length.Value, 38)
            self.editor.apply.click()
            self.assertIn("Refresh", self.editor.error.text())
            self.editor.closeButton.click()
            self.assertTrue(other.isVisible())
            self.doc.removeObject(self.parameters.Name)
            Gui.updateGui()
            self.assertFalse(other.isVisible())
            self.assertTrue(other._closed)
        finally:
            other.close()
            other.deleteLater()
            Gui.updateGui()
