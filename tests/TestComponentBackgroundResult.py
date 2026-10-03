# SPDX-License-Identifier: LGPL-2.1-or-later
"""Operation display/deletion and protected result identity regressions."""
import importlib.util
import os
from pathlib import Path
import sys
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore, QtWidgets

root = Path(os.environ["FREECAD_PLUS_SOURCE"])
if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    spec = importlib.util.spec_from_file_location("BackgroundOverlay", root / "tests/TestComponentCurveProfile.py")
    overlay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(overlay)
    name = "freecad.gui.ComponentNavigator"
    spec = importlib.util.spec_from_file_location(name, root / "src/Gui/ComponentNavigator.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    import freecad.gui
    freecad.gui.ComponentNavigator = module

import ComponentModel as Model
import ComponentSketch as Sketch
import ComponentExtrude as Extrude
import ComponentExtent as Extent
from freecad.gui import ComponentNavigator as Navigator
from freecad.gui import ComponentSelection as Selection


class TestComponentBackgroundResult(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_document("Background result")
        self.component = Model.metadata(self.doc).RootComponent
        self.sketch = Sketch.create(self.component)
        self.sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 5))
        self.doc.recompute()
        self.operation, self.body = Extrude.create(self.component, self.sketch, 4,
                                                   elements=["Edge1"], options=Extent.defaults())

    def tearDown(self):
        Gui.Selection.clearSelection()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def assert_display(self, operation, body):
        self.assertTrue(Model.background_result(body))
        self.assertFalse(body.ViewObject.ShowInTree)
        self.assertEqual(body.ViewObject.DisplayMode, "Background")
        self.assertTrue(operation.Visibility, str((body.Visibility, body.ResultStatus, body.State, operation.State)))
        self.assertTrue(body.Visibility)
        self.assertFalse(body.Shape.isNull())
        self.assertEqual(Model.result_for_operation(operation), body)

    def testDisplaySelectionVisibilityAndReopen(self):
        self.assert_display(self.operation, self.body)
        panel = Navigator.show(self.doc)
        panel.refresh()
        keys = [panel.history.topLevelItem(i).data(0, QtCore.Qt.UserRole)
                for i in range(panel.history.topLevelItemCount())]
        self.assertIn(Navigator.object_key(self.operation), keys)
        self.assertNotIn(Navigator.object_key(self.body), keys)
        paths = Navigator.visible_paths(self.component, self.component, [])
        self.assertIn(self.operation.Name + ".", paths)
        self.assertNotIn(self.body.Name + ".", paths)
        pick = Selection.resolve(self.component, self.operation, "Face1")[0]
        self.assertEqual(pick.item, self.body)
        self.assertEqual(pick.element, "Face1")
        self.operation.Visibility = False
        self.assertFalse(self.body.Visibility)
        self.operation.Visibility = True
        self.assertTrue(self.body.Visibility)
        self.body.Visibility = False
        self.assertFalse(self.operation.Visibility)
        self.body.Visibility = True
        self.assertTrue(self.operation.Visibility)
        names = self.operation.Name, self.body.Name
        identity = self.body.ObjectId
        output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "Background.cadprt"
        self.doc.saveAs(str(output))
        App.closeDocument(self.doc.Name)
        self.doc = App.openDocument(str(output))
        self.component = Model.metadata(self.doc).RootComponent
        self.doc.recompute()
        Model.prepare_result_display(self.component)
        self.operation, self.body = (self.doc.getObject(name) for name in names)
        self.assertEqual(self.body.ObjectId, identity)
        self.assert_display(self.operation, self.body)
        Model.validate(self.doc)

    def testProtectedDeletionAndOperationUndo(self):
        prompts = []
        watchdog = QtCore.QTimer()
        def dismiss():
            for widget in QtWidgets.QApplication.topLevelWidgets():
                if isinstance(widget, QtWidgets.QMessageBox) and widget.isVisible():
                    prompts.append(widget.text())
                    widget.reject()
        watchdog.timeout.connect(dismiss)
        watchdog.start(100)
        try:
            Gui.Selection.addSelection(self.body)
            Gui.runCommand("Std_Delete")
            self.assertIsNotNone(self.doc.getObject(self.body.Name))
            Gui.Selection.clearSelection()
            names = self.operation.Name, self.body.Name
            identities = self.operation.ObjectId, self.body.ObjectId
            Gui.Selection.addSelection(self.operation)
            Gui.runCommand("Std_Delete")
            self.assertFalse(prompts, str(prompts))
            self.assertIsNone(self.doc.getObject(names[0]))
            self.assertIsNone(self.doc.getObject(names[1]))
            self.assertTrue(self.sketch.Visibility)
            self.assertFalse(any(hasattr(obj, "ProfileSource") for obj in self.doc.Objects))
            self.doc.undo()
            self.doc.recompute()
            operation, body = (self.doc.getObject(name) for name in names)
            Model.prepare_result_display(self.component)
            self.assertEqual((operation.ObjectId, body.ObjectId), identities)
            self.assert_display(operation, body)
            self.assertFalse(self.sketch.Visibility)
            self.doc.redo()
            self.doc.recompute()
            self.assertTrue(self.sketch.Visibility)
            from freecad.gui.ComponentExtrudeTask import ExtrudeTask
            task = ExtrudeTask(self.component)
            task.start_selection()
            try:
                Gui.Selection.clearSelection()
                Gui.Selection.addSelection(self.doc.Name, self.sketch.Name, "Edge1")
                self.assertEqual(task.curve_names(), ["Edge1"], task.status.text())
                self.assertTrue(task.accept(), task.status.text())
                self.assertTrue(task.result.Shape.isValid())
            finally:
                task.stop_selection()
                task.clear_preview()
        finally:
            watchdog.stop()

    def testDeletePreservesSharedProfileAndSketch(self):
        other, result = Extrude.create(self.component, self.sketch, 6,
                                       elements=["Edge1"], options=Extent.defaults())
        unused = other.Profile[0].Name
        shared = self.operation.Profile[0]
        with Model.transaction(self.doc, "Share profile fixture"):
            other.Profile = self.operation.Profile
            self.doc.removeObject(unused)
        with Model.transaction(self.doc, "Delete Extrude"):
            self.doc.removeObject(self.operation.Name)
        self.assertIsNotNone(self.doc.getObject(shared.Name))
        self.assertFalse(self.sketch.Visibility)
        self.assertAlmostEqual(result.Shape.Volume, 150 * 3.141592653589793)
        with Model.transaction(self.doc, "Delete last Extrude"):
            self.doc.removeObject(other.Name)
        self.assertTrue(self.sketch.Visibility)
        self.assertFalse(any(hasattr(obj, "ProfileSource") for obj in self.doc.Objects))

    def testAdoptionAndDumbConversion(self):
        identity = self.body.ObjectId
        self.body.ViewObject.Proxy = 0
        self.body.removeProperty("BackgroundResult")
        self.operation.Visibility = False
        self.body.Visibility = True
        self.doc.recompute()
        Model.prepare_result_display(self.component)
        self.doc.recompute()
        self.assertEqual(self.body.ObjectId, identity)
        self.assert_display(self.operation, self.body)
        frozen = Model.delete_parameters(self.component, self.body)
        self.assertFalse(Model.background_result(frozen))
        self.assertTrue(frozen.ViewObject.ShowInTree)
        self.assertEqual(frozen.ViewObject.DisplayMode, "Flat Lines")
        self.assertEqual(frozen.ObjectId, identity)
        self.assertFalse(frozen.Shape.isNull())

    def testSuppressionAndDownstreamResult(self):
        Model.set_items_suppressed([self.operation], True)
        self.doc.recompute()
        self.assertFalse(self.operation.Visibility)
        self.assertTrue(self.body.SuppressionVisibility)  # Remember the pre-suppression display.
        Model.set_items_suppressed([self.operation], False)
        self.doc.recompute()
        self.assert_display(self.operation, self.body)
        sketch = Sketch.create(self.component)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        self.doc.recompute()
        operation, body = Extrude.create(self.component, sketch, 4, mode="Subtract", target=self.body,
                                        elements=["Edge1"], options=Extent.defaults())
        self.assert_display(operation, body)
        self.assertFalse(self.operation.Visibility)
        self.assertFalse(self.body.Visibility)
        self.assertAlmostEqual(body.Shape.Volume, 84 * 3.141592653589793)
        Model.set_items_suppressed([operation], True)
        self.doc.recompute()
        self.assertTrue(self.operation.Visibility)
        self.assertFalse(operation.Visibility)

    def testPublicTargetPreviewTransparency(self):
        from freecad.gui.ComponentExtrudeTask import ExtrudeTask
        sketch = Sketch.create(self.component)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        self.doc.recompute()
        self.operation.ViewObject.Transparency = 12
        task = ExtrudeTask(self.component)
        Gui.Control.showDialog(task)
        task.start_selection()
        try:
            task.profile.setCurrentIndex(task.profile.findData(sketch.Name))
            task.set_curves(["Edge1"], False)
            task.length.setProperty("rawValue", 4.)
            task.mode.setCurrentIndex(task.mode.findData("Subtract"))
            task.target.setCurrentIndex(task.target.findData(self.body.Name))
            self.assertEqual(task.target.currentText(), self.operation.Label)
            self.assertTrue(task.preview(), task.status.text())
            self.assertEqual(self.operation.ViewObject.Transparency, 75)
        finally:
            task.reject()
        self.assertEqual(self.operation.ViewObject.Transparency, 12)
        self.assert_display(self.operation, self.body)
