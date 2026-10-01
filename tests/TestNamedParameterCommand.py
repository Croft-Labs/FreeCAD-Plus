# SPDX-License-Identifier: LGPL-2.1-or-later
"""Installed named-parameter command, expression reuse and enclosure acceptance."""
import os
from pathlib import Path
import unittest
from unittest.mock import Mock, patch
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtWidgets
import NamedParameterGui as Editor
from NamedParameters import create_parameter_set, is_parameter_set
from prototypes.ParameterEnclosure import make_enclosure


class TestNamedParameterCommand(unittest.TestCase):
    def setUp(self):
        warning = patch.object(QtWidgets.QMessageBox, "warning",
                               side_effect=lambda *args: self.fail(str(args[-1])))
        warning.start()
        self.addCleanup(warning.stop)
        Gui.activateWorkbench("PartWorkbench")
        self.doc = App.newDocument("NamedParameterWorkflow")
        self.doc.UndoMode = 1
        self.part = self.doc.addObject("App::Part", "Design")
        self.doc.recompute()
        Gui.Selection.clearSelection()

    def tearDown(self):
        for dialog in list(Editor._dialogs.values()):
            dialog.close()
            dialog.deleteLater()
        Gui.Selection.clearSelection()
        Gui.updateGui()
        App.closeDocument(self.doc.Name)

    def launch(self, target):
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(target)
        self.assertTrue(Editor.CommandNamedParameters().IsActive())
        Gui.runCommand("Part_NamedParameters", 0)
        Gui.updateGui()
        params = target if is_parameter_set(target) else next(
            obj for obj in target.Group if is_parameter_set(obj))
        return Editor._dialogs[(self.doc.Name, params.Name)]

    def testMenuCreationReuseAndUndo(self):
        self.assertIn("Part_NamedParameters", Gui.listCommands())
        actions = [action for menu in Gui.getMainWindow().menuBar().findChildren(QtWidgets.QMenu)
                   for action in menu.actions()]
        self.assertTrue(any("Named parameters" in action.text() for action in actions))
        dialog = self.launch(self.part)
        params = dialog.obj
        self.assertTrue(is_parameter_set(params))
        self.assertEqual(dialog.parameter.count(), 0)
        self.assertFalse(dialog.copyReference.isEnabled())
        self.assertIs(self.launch(self.part), dialog)
        self.assertEqual([obj for obj in self.part.Group if is_parameter_set(obj)], [params])
        name = params.Name
        dialog.close()
        self.doc.undo()
        self.doc.recompute()
        self.assertIsNone(self.doc.getObject(name))
        self.doc.redo()
        self.doc.recompute()
        self.assertTrue(is_parameter_set(self.doc.getObject(name)))
        self.assertEqual(self.launch(self.part).obj.Name, name)

    def testCopyReferenceDrivesFeatureAndFollowsRename(self):
        # Verify the requested clipboard payload and use it in a real expression.
        # A shared Windows clipboard can be locked by another desktop process;
        # physical copy/paste remains part of owner acceptance.
        clipboard = Mock()
        clipboard_patch = patch.object(QtWidgets.QApplication, "clipboard", return_value=clipboard)
        clipboard_patch.start()
        self.addCleanup(clipboard_patch.stop)
        dialog = self.launch(self.part)
        dialog.newName.setText("Width")
        dialog.newExpression.setText("1 in")
        dialog.newDescription.setText("Overall width")
        dialog.create.click()
        self.assertEqual(dialog.error.text(), "")
        dialog.copyReference.click()
        reference = clipboard.setText.call_args.args[0]
        self.assertEqual(reference, dialog.obj.Name + ".Width")
        box = self.doc.addObject("Part::Box", "Box")
        self.part.addObject(box)
        box.setExpression("Length", reference)
        self.doc.recompute()
        self.assertAlmostEqual(box.Shape.BoundBox.XLength, 25.4)
        dialog.name.setText("OverallWidth")
        dialog.rename.click()
        self.assertEqual(dialog.error.text(), "")
        dialog.copyReference.click()
        clipboard.setText.assert_called_with(dialog.obj.Name + ".OverallWidth")
        dialog.expression.setText("2 in")
        dialog.apply.click()
        self.assertEqual(dialog.error.text(), "")
        self.assertAlmostEqual(box.Shape.BoundBox.XLength, 50.8)
        dialog.displayUnit.setCurrentText("in")
        self.assertAlmostEqual(float(dialog.value.text().split()[0]), 2)
        self.assertEqual(dialog.description.text(), "Overall width")

    def testExplicitOwnershipAndPendingEdits(self):
        body = self.doc.addObject("PartDesign::Body", "Body")
        link = self.doc.addObject("App::Link", "Occurrence")
        link.setLink(self.part)
        ordinary = self.doc.addObject("App::FeaturePython", "Unrelated")
        self.part.addObject(ordinary)
        self.doc.recompute()
        for target in (body, link, ordinary):
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(target)
            self.assertFalse(Editor.CommandNamedParameters().IsActive())
            with self.assertRaises(ValueError):
                Editor.open_for_target(target)
        params = create_parameter_set(self.part)
        extra = create_parameter_set(self.part)
        with self.assertRaisesRegex(ValueError, "multiple parameter sets"):
            Editor.open_for_target(self.part)
        self.assertEqual(self.launch(params).obj, params)
        self.doc.openTransaction("Unrelated owner edit")
        self.part.Label = "Pending edit"
        with self.assertRaisesRegex(ValueError, "Finish the current edit"):
            Editor.open_for_target(extra)
        self.assertTrue(self.doc.HasPendingTransaction)
        self.doc.abortTransaction()
        self.doc.recompute()

    def testEnclosureReopensThroughInstalledCommand(self):
        params, result, lid, holes = make_enclosure(self.doc, self.part)
        dialog = self.launch(self.part)
        self.assertEqual(dialog.obj, params)
        for name, value in (("Width", "76.2 mm"), ("LidClearance", "1 mm"),
                            ("HoleSpacing", "40 mm")):
            dialog.parameter.setCurrentText(name)
            dialog.expression.setText(value)
            dialog.apply.click()
            self.assertEqual(dialog.error.text(), "")
        self.assertAlmostEqual(result.Shape.BoundBox.XLength, 76.2)
        self.assertAlmostEqual(lid.Shape.BoundBox.XLength, 78.2)
        self.assertAlmostEqual(holes[1].Placement.Base.x - holes[0].Placement.Base.x, 40)
        filename = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "Named-parameters-enclosure.FCStd"
        part_name, params_name, result_name = self.part.Name, params.Name, result.Name
        dialog.close()
        self.doc.recompute()
        self.doc.saveAs(str(filename))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(filename))
        self.doc.recompute()
        self.part = self.doc.getObject(part_name)
        params = self.doc.getObject(params_name)
        self.assertTrue(is_parameter_set(params))
        dialog = self.launch(params)
        dialog.parameter.setCurrentText("Width")
        dialog.expression.setText("80 mm")
        dialog.apply.click()
        self.assertEqual(dialog.error.text(), "")
        self.assertAlmostEqual(self.doc.getObject(result_name).Shape.BoundBox.XLength, 80)
