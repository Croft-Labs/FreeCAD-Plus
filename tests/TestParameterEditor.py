# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native Qt checks for the uninstalled parameter editor prototype."""
import unittest
import math
import os
from pathlib import Path
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

    def testCreateParameterCorrectsErrorsAndSelectsNewProperty(self):
        self.editor.newName.setText("Clearance")
        self.editor.newExpression.setText("30 deg")
        self.editor.create.click()
        self.assertTrue(self.editor.error.text())
        self.assertEqual(self.editor.newName.text(), "Clearance")
        self.assertNotIn("Clearance", self.parameters.PropertiesList)
        self.editor.newExpression.setText("2 mm")
        self.editor.create.click()
        self.assertEqual(self.editor.error.text(), "")
        self.assertEqual(self.editor.parameter.currentText(), "Clearance")
        self.assertAlmostEqual(self.parameters.Clearance.Value, 2)
        self.assertEqual(self.editor.newName.text(), "")
        self.assertEqual(self.editor.newExpression.text(), "")
        self.editor.newName.setText("Clearance")
        self.editor.newExpression.setText("3 mm")
        self.editor.create.click()
        self.assertIn("already exists", self.editor.error.text())
        self.assertAlmostEqual(self.parameters.Clearance.Value, 2)
        self.editor.newName.setText("DraftAngle")
        self.editor.newType.setCurrentText("Angle")
        self.editor.newExpression.setText("5 deg")
        self.editor.create.click()
        self.assertEqual(self.editor.error.text(), "")
        self.assertEqual(self.editor.parameter.currentText(), "DraftAngle")
        self.assertAlmostEqual(self.parameters.DraftAngle.Value, 5)

    def testDisplayUnitsDoNotChangeParameterMeaningOrExpressions(self):
        self.editor.expression.setText("25.4 mm")
        self.editor.apply.click()
        before = self.parameters.ExpressionEngine
        self.editor.displayUnit.setCurrentText("in")
        self.assertIn("1", self.editor.value.text())
        self.assertTrue(self.editor.value.text().endswith(" in"))
        self.assertEqual(self.parameters.ExpressionEngine, before)
        self.assertAlmostEqual(self.parameters.Width.Value, 25.4)
        self.assertAlmostEqual(self.box.Shape.BoundBox.XLength, 25.4)
        self.assertFalse(self.doc.HasPendingTransaction)
        self.editor.parameter.setCurrentIndex(self.editor.parameter.findText("Tilt"))
        self.editor.displayUnit.setCurrentText("rad")
        self.assertTrue(self.editor.value.text().endswith(" rad"))
        self.assertAlmostEqual(self.parameters.Tilt.Value, 30)
        self.assertEqual(self.parameters.ExpressionEngine, before)
        self.editor.newName.setText("LidGap")
        self.editor.newExpression.setText("2 mm")
        self.editor.newDescription.setText("Lid clearance")
        self.editor.create.click()
        self.assertEqual(self.editor.error.text(), "")
        self.assertEqual(self.editor.description.text(), "Lid clearance")
        self.assertTrue(self.editor.description.isReadOnly())
        self.assertEqual(self.editor.newDescription.text(), "")

    def enclosureEditor(self):
        from prototypes.ParameterEnclosure import make_enclosure
        self.editor.close()
        self.editor.deleteLater()
        Gui.updateGui()
        part = self.doc.addObject("App::Part", "EnclosureDefinition")
        self.parameters, result, lid, holes = make_enclosure(self.doc, part)
        self.editor = ParameterEditor(self.parameters)
        self.editor.show()
        Gui.updateGui()
        return result, lid, holes

    def testEnclosureEditorBenchmarkEditsRenameAndDisplayUnits(self):
        result, lid, holes = self.enclosureEditor()
        for name, expression in (("Width", "76.2 mm"), ("LidClearance", "1 mm"),
                                 ("HoleSpacing", "40 mm")):
            self.editor.parameter.setCurrentIndex(self.editor.parameter.findText(name))
            self.editor.expression.setText(expression)
            self.editor.apply.click()
            self.assertEqual(self.editor.error.text(), "")
        self.assertAlmostEqual(result.Shape.Volume, 76.2 * 30 * 20 - 72.2 * 26 * 18 - 16 * math.pi, places=5)
        self.assertAlmostEqual(lid.Shape.BoundBox.XLength, 78.2)
        self.assertAlmostEqual(holes[1].Placement.Base.x - holes[0].Placement.Base.x, 40)
        self.editor.parameter.setCurrentIndex(self.editor.parameter.findText("Width"))
        self.editor.name.setText("EnclosureWidth")
        self.editor.rename.click()
        self.assertEqual(self.editor.error.text(), "")
        self.assertEqual(self.editor.parameter.currentText(), "EnclosureWidth")
        before = self.parameters.ExpressionEngine
        self.editor.displayUnit.setCurrentText("in")
        self.assertAlmostEqual(float(self.editor.value.text().split()[0]), 3)
        self.assertEqual(self.parameters.ExpressionEngine, before)
        self.assertAlmostEqual(result.Shape.BoundBox.XLength, 76.2)
        self.editor.expression.setText("90 mm")
        self.editor.closeButton.click()
        self.assertAlmostEqual(result.Shape.BoundBox.XLength, 76.2)

    def testEnclosureEditorRejectsFailuresThenReopensSavedModel(self):
        result, lid, holes = self.enclosureEditor()
        self.editor.parameter.setCurrentIndex(self.editor.parameter.findText("Width"))
        volume = result.Shape.Volume
        for expression in ("30 deg", lid.Name + ".Length", "0 mm"):
            self.editor.expression.setText(expression)
            self.editor.apply.click()
            self.assertTrue(self.editor.error.text())
            self.assertTrue(self.editor.isVisible())
            self.assertEqual(self.editor.expression.text(), expression)
            self.assertAlmostEqual(result.Shape.Volume, volume)
            self.assertNotIn("Invalid", result.State)
            self.assertFalse(self.doc.HasPendingTransaction)
        self.editor.expression.setText("80 mm")
        self.editor.apply.click()
        self.assertEqual(self.editor.error.text(), "")
        names = [obj.Name for obj in (self.parameters, result, lid)]
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "EnclosureEditorBenchmark.FCStd"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.assertTrue(self.editor._closed)
        self.editor.deleteLater()
        Gui.updateGui()
        self.doc = App.openDocument(str(path))
        self.doc.recompute()
        self.parameters, result, lid = [self.doc.getObject(name) for name in names]
        self.editor = ParameterEditor(self.parameters)
        self.editor.show()
        self.editor.parameter.setCurrentIndex(self.editor.parameter.findText("Width"))
        self.assertIn("80 mm", self.editor.expression.text())
        self.editor.expression.setText("85 mm")
        self.editor.apply.click()
        self.assertEqual(self.editor.error.text(), "")
        self.assertAlmostEqual(result.Shape.BoundBox.XLength, 85)
        self.assertAlmostEqual(lid.Shape.BoundBox.XLength, 86)
        self.assertTrue(result.Shape.isValid())

    def testExplicitPartEditorTargetsSuppliedDocumentRatherThanActiveDocument(self):
        from prototypes.NamedParameters import create_parameter_set
        from prototypes.ParameterEditor import edit_parameter_set
        part = self.doc.addObject("App::Part", "WorkPart")
        self.doc.recompute()
        other_doc = App.newDocument("OtherActiveDocument")
        other = None
        try:
            other_part = other_doc.addObject("App::Part", "OtherPart")
            other_doc.recompute()
            before = {obj.Name for obj in other_doc.Objects}
            params = create_parameter_set(part)
            self.assertEqual(params.Document, self.doc)
            other = edit_parameter_set(params)
            self.assertEqual(other.parameter.count(), 0)
            other.newName.setText("Width")
            other.newExpression.setText("42 mm")
            other.create.click()
            self.assertEqual(other.error.text(), "")
            self.assertAlmostEqual(params.Width.Value, 42)
            self.assertEqual({obj.Name for obj in other_doc.Objects}, before)
            self.assertEqual(other_part.Group, [])
            other.closeButton.click()
            self.assertIsNotNone(self.doc.getObject(params.Name))
            with self.assertRaisesRegex(ValueError, "explicit Part"):
                edit_parameter_set(self.parameters)
        finally:
            if other is not None:
                other.close()
                other.deleteLater()
            App.closeDocument(other_doc.Name)
            App.setActiveDocument(self.doc.Name)
            Gui.updateGui()
