# SPDX-License-Identifier: LGPL-2.1-or-later
"""Narrow native legacy history pilot, retained feature and geometry recovery."""
import hashlib
import math
import os
from pathlib import Path
import sys
import unittest
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
from PySide import QtCore, QtWidgets
try:
    from PySide6 import QtTest
except ImportError:
    from PySide2 import QtTest

if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src/Mod/Part"))
import CadDocument
import ComponentModel as Model
import ComponentExtrude as Extrude


class TestLegacyBodyHistory(unittest.TestCase):
    def setUp(self):
        self.names = set(App.listDocuments())
        self.doc = App.newDocument("LegacyHistory")
        self.doc.UndoMode = 1
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])

    def tearDown(self):
        from freecad.gui import ComponentExtrudeTask as Task
        if Task._task:
            Task._task.reject()
        if Gui.Control.activeDialog():
            Gui.Control.closeDialog()
        for name in set(App.listDocuments()) - self.names:
            gui = Gui.getDocument(name)
            if gui.getInEdit():
                gui.resetEdit()
            App.closeDocument(name)

    def build(self, independent=False, x=0):
        part = self.doc.addObject("App::Part", "Part")
        part.Placement = App.Placement(App.Vector(15, 2, 1), App.Rotation(App.Vector(0, 0, 1), 25))
        body = self.doc.addObject("PartDesign::Body", "Body")
        part.addObject(body)
        sketch = self.doc.addObject("Sketcher::SketchObject", "Sketch") if independent else body.newObject("Sketcher::SketchObject", "Sketch")
        if independent:
            part.addObject(sketch)
        sketch.Placement.Base.x = x
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2), False)
        sketch.addConstraint(Sketcher.Constraint("Radius", 0, 2))
        pad = body.newObject("PartDesign::Pad", "Pad")
        pad.Profile = sketch
        pad.Length = 5
        body.Tip = pad
        for i, transform in enumerate((False, True)):
            link = self.doc.addObject("App::Link", "Use" + str(i))
            link.setLink(part)
            link.LinkTransform = transform
            link.LinkPlacement = App.Placement(App.Vector(50 + i * 25, 0, 0), App.Rotation(App.Vector(0, 0, 1), 40))
        self.doc.recompute()
        return part, body, sketch, pad

    def shape(self, obj):
        return Part.getShape(obj, "", needSubElement=False).copy()

    def same(self, before, after):
        self.assertAlmostEqual(before.Volume, after.Volume, places=8)
        self.assertAlmostEqual(before.cut(after).Volume, 0, places=8)
        self.assertAlmostEqual(after.cut(before).Volume, 0, places=8)

    def mapped(self, part, body, sketch, pad):
        self.assertTrue(hasattr(part, "ModelHistory"), str(Model.metadata(self.doc).ConversionReport))
        self.assertEqual([o.Name for o in Model.history(part)], [sketch.Name, pad.Name, body.Name],
                         str(Model.metadata(self.doc).ConversionReport))
        self.assertEqual([Model.owner(o) for o in (sketch, pad, body)], [part] * 3)
        self.assertEqual(body.ComponentRole, "Result")
        self.assertEqual(body.Producer, pad)
        self.assertEqual(body.LegacyTip, pad)
        self.assertEqual(pad.Profile[0], sketch)
        self.assertEqual(body.Group, [body.Tip])
        self.assertEqual(body.Tip.Producer, pad)
        self.assertEqual(Model.finished_results(part), [body])
        self.assertFalse(any(o.Frozen for o in self.doc.Objects if hasattr(o, "Frozen")))
        Model.validate(self.doc)

    def test_native_identities_geometry_shared_undo_redo(self):
        part, body, sketch, pad = self.build(x=3)
        before = {o.Name: self.shape(o) for o in (part, body, self.doc.Use0, self.doc.Use1)}
        keys = [(o.Name, o.TypeId, o.ID) for o in (body, sketch, pad)]
        CadDocument.convert_legacy(self.doc)
        self.mapped(part, body, sketch, pad)
        self.assertEqual(keys, [(o.Name, o.TypeId, o.ID) for o in (body, sketch, pad)])
        for name, shape in before.items():
            self.same(shape, self.shape(self.doc.getObject(name)))
        count = len(self.doc.Objects)
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(len(self.doc.Objects), count)
        self.doc.undo()
        self.assertEqual(body.Group, [sketch, pad])
        self.assertEqual(body.Tip, pad)
        self.assertFalse(hasattr(body, "LegacyHistoryState"))
        self.doc.redo()
        self.doc.recompute()
        self.mapped(part, body, sketch, pad)
        for name, shape in before.items():
            self.same(shape, self.shape(self.doc.getObject(name)))

    def test_edit_sketch_pad_downstream_reference_and_reopen(self):
        part, body, sketch, pad = self.build()
        consumer = self.doc.addObject("Part::Cut", "Consumer")
        tool = self.doc.addObject("Part::Box", "Tool")
        tool.Length = tool.Width = tool.Height = 1
        consumer.Base, consumer.Tool = body, tool
        self.doc.recompute()
        original = self.output / "HistoryOriginal.FCStd"
        self.doc.saveAs(str(original))
        digest = hashlib.sha256(original.read_bytes()).hexdigest()
        CadDocument.convert_legacy(self.doc)
        self.mapped(part, body, sketch, pad)
        ids = {o.Name: o.ObjectId for o in (part, body, sketch, pad)}
        with Model.transaction(self.doc, "Edit converted sketch"):
            sketch.setDatum(0, App.Units.Quantity("3 mm"))
        Extrude.edit(pad, sketch, 7)
        self.assertAlmostEqual(body.Shape.Volume, math.pi * 9 * 7, places=7)
        self.assertEqual(consumer.Base, body)
        self.assertAlmostEqual(consumer.Shape.Volume, body.Shape.Volume - 1, places=7)
        saved = self.output / "HistoryConverted.cadprt"
        self.doc.saveAs(str(saved))
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), digest)
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(saved)
        for name, identity in ids.items():
            self.assertEqual(self.doc.getObject(name).ObjectId, identity)
        self.assertAlmostEqual(self.doc.Body.Shape.Volume, math.pi * 9 * 7, places=7)
        with Model.transaction(self.doc, "Edit reopened sketch"):
            self.doc.Sketch.setDatum(0, App.Units.Quantity("4 mm"))
        self.assertAlmostEqual(self.doc.Body.Shape.Volume, math.pi * 16 * 7, places=7)
        self.assertEqual(self.doc.Consumer.Base, self.doc.Body)

    def test_independent_profile_and_mode_change_guard(self):
        part, body, sketch, pad = self.build(independent=True)
        CadDocument.convert_legacy(self.doc)
        self.mapped(part, body, sketch, pad)
        with self.assertRaisesRegex(ValueError, "downstream result"):
            Extrude.edit(pad, sketch, 5, mode="Subtract", target=body)
        self.assertEqual(body.Producer, pad)

    def test_length_expression_stays_native_editable(self):
        part, body, sketch, pad = self.build()
        pad.setExpression("Length", "Sketch.Constraints[0] * 3")
        self.doc.recompute()
        expression = list(pad.ExpressionEngine)
        CadDocument.convert_legacy(self.doc)
        self.mapped(part, body, sketch, pad)
        self.assertEqual(list(pad.ExpressionEngine), expression)
        with Model.transaction(self.doc, "Edit expression input"):
            sketch.setDatum(0, App.Units.Quantity("3 mm"))
        self.assertAlmostEqual(pad.Length.Value, 9)
        self.assertAlmostEqual(body.Shape.Volume, math.pi * 9 * 9, places=7)
        with self.assertRaisesRegex(ValueError, "expressions"):
            Extrude.edit(pad, sketch, 8)

    def test_unmapped_body_frame_retains_native_output(self):
        part, body, sketch, pad = self.build()
        body.Placement = App.Placement(App.Vector(7, 4, 0), App.Rotation(App.Vector(1, 0, 0), 20))
        self.doc.recompute()
        before = self.shape(self.doc.Use0)
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(body.Group, [sketch, pad])
        self.assertEqual(body.Tip, pad)
        self.assertIn("frame", body.LegacyHistoryState)
        self.same(before, self.shape(self.doc.Use0))
        pad.Length = 6
        self.doc.recompute()
        self.assertAlmostEqual(body.Shape.Volume, math.pi * 4 * 6, places=7)

    def test_mixed_history_retained_honestly(self):
        part, body, sketch, pad = self.build()
        extra = body.newObject("PartDesign::Feature", "UnmappedFeature")
        extra.Shape = Part.makeBox(2, 3, 4)
        body.Tip = extra
        self.doc.recompute()
        CadDocument.convert_legacy(self.doc)
        self.assertEqual(body.Group, [sketch, pad, extra])
        self.assertEqual(body.Tip, extra)
        self.assertTrue(body.LegacyHistoryState.startswith("Retained native:"))
        self.assertEqual(Model.finished_results(part), [body])
        self.assertFalse(any(getattr(o, "LegacyMigration", "") for o in body.Group))

    def test_source_failure_preserves_dumb_geometry_recovery(self):
        part, body, sketch, pad = self.build()
        part.setExpression("Placement.Base.x", "15 mm")
        self.doc.recompute()
        before = self.shape(part)
        CadDocument.convert_legacy(self.doc)
        root = Model.metadata(self.doc).RootComponent
        results = Model.finished_results(root)
        self.assertTrue(results)
        self.same(before, results[0].Shape)
        self.assertIn("parametric history not converted", results[0].LegacyRecovery)
        self.assertEqual(body.Group, [sketch, pad])
        self.assertEqual(body.Tip, pad)

    def test_native_history_ui_sketch_edit_cancel(self):
        from freecad.gui import ComponentNavigator as Navigator
        part, body, sketch, pad = self.build()
        CadDocument.convert_legacy(self.doc)
        panel = Navigator.show(self.doc)
        panel.root_key = Navigator.object_key(part)
        panel.active_key = Navigator.object_key(part)
        panel.refresh()
        keys = [panel.history.topLevelItem(i).data(0, QtCore.Qt.UserRole)
                for i in range(panel.history.topLevelItemCount())]
        self.assertEqual(keys[1:], [Navigator.object_key(o) for o in (sketch, pad, body)])
        self.double_click_history(panel, sketch)
        Gui.updateGui()
        self.assertEqual(Gui.activeDocument().getInEdit().Object, sketch)
        Gui.activeDocument().resetEdit()
        Gui.Control.closeDialog()
        Gui.updateGui()
        self.assertEqual(sketch.ConstraintCount, 1)
        self.assertEqual(pad.Profile[0], sketch)
        self.same(self.shape(body), self.shape(pad))

    def double_click_history(self, panel, obj):
        from freecad.gui import ComponentNavigator as Navigator
        panel.open_component_tab(Navigator.object_key(Model.owner(obj)))
        panel.tabs.setCurrentWidget(panel.history)
        panel.setFloating(True)
        panel.resize(850, 650)
        panel.show()
        Gui.getMainWindow().show()
        Gui.updateGui()
        QtTest.QTest.qWait(100)
        panel.refresh()
        tree = panel.history
        row = next(tree.topLevelItem(i) for i in range(tree.topLevelItemCount())
                   if tree.topLevelItem(i).data(0, QtCore.Qt.UserRole) == Navigator.object_key(obj))
        rect = tree.visualItemRect(row)
        self.assertFalse(rect.isEmpty())
        point = QtCore.QPoint(tree.header().sectionViewportPosition(2) + 18, rect.center().y())
        QtTest.QTest.mouseClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
        panel.refresh()
        QtTest.QTest.mouseDClick(tree.viewport(), QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, point)
        Gui.updateGui()
        QtTest.QTest.qWait(100)

    def test_native_history_pad_dialog_accept_cancel_and_undo(self):
        from freecad.gui import ComponentNavigator as Navigator
        from freecad.gui import ComponentExtrudeTask as Task
        part, body, sketch, pad = self.build()
        CadDocument.convert_legacy(self.doc)
        panel = Navigator.show(self.doc)
        self.double_click_history(panel, pad)
        task = Task._task
        self.assertIsNotNone(task)
        self.assertEqual(task.operation, pad)
        task.length.setProperty("rawValue", 8.)
        accepted = task.accept()
        self.assertTrue(accepted, "Converted Pad task must accept its dimension edit")
        self.assertAlmostEqual(pad.Length.Value, 8)
        self.assertAlmostEqual(body.Shape.Volume, math.pi * 4 * 8, places=7)
        Gui.runCommand("Std_Undo")
        self.doc.recompute()
        self.assertAlmostEqual(pad.Length.Value, 5)
        Gui.runCommand("Std_Redo")
        self.doc.recompute()
        self.assertAlmostEqual(pad.Length.Value, 8)
        self.double_click_history(panel, pad)
        task = Task._task
        self.assertIsNotNone(task)
        task.length.setProperty("rawValue", 12.)
        task.reject()
        self.assertAlmostEqual(pad.Length.Value, 8)
        self.assertEqual(body.Producer, pad)
        self.assertEqual(body.Tip.Producer, pad)
