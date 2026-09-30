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
