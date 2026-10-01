# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three feedback workflows for reference recovery, identity and independent work."""
import hashlib
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import FreeCAD as App
import FreeCADGui as Gui
import Part
import CadDocument
import ComponentModel as Model
import ComponentExtrude as Extrude
import ComponentSketch as Sketch
from PySide import QtCore, QtWidgets
from freecad.gui import ComponentNavigator as Navigator


class TestComponentReferenceRecovery(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, relative in [(Model, "src/Mod/Part/ComponentModel.py"),
                                 (CadDocument, "src/Mod/Part/CadDocument.py"),
                                 (Extrude, "src/Mod/Part/ComponentExtrude.py"),
                                 (Sketch, "src/Mod/Part/ComponentSketch.py"),
                                 (Navigator, "src/Gui/ComponentNavigator.py")]:
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((source / relative).read_bytes()).digest())
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        self.doc = Model.new_document("Reference recovery")
        self.root = Model.metadata(self.doc).RootComponent
        self.link = Model.add_component(self.root, label="Sources")
        self.child = self.link.LinkedObject
        self.source = self.body(self.child, "Original", 2)
        self.replacement = self.body(self.child, "Replacement", 4)
        self.reference = Model.add_reference(self.root, self.link, self.source)
        self.panel = Navigator.show(self.doc)
        self.panel.tabs.setCurrentWidget(self.panel.history)

    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def body(self, component, name, length):
        obj = self.doc.addObject("Part::Feature", name)
        Model.register_object(component, obj, "Object", True)
        obj.Shape = Part.makeBox(length, 3, 4)
        self.doc.recompute()
        return obj

    def break_reference(self):
        self.reference.SourceObject = None
        self.doc.recompute()

    def testBrokenReferenceOpenAndIndependentRefresh(self):
        healthy = Model.add_reference(self.root, self.link, self.replacement)
        self.break_reference()
        self.assertEqual(self.reference.ResultStatus, "Missing source")
        self.assertTrue(self.reference.Shape.isNull())
        self.replacement.Shape = Part.makeBox(5, 3, 4)
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "Original reference"):
            Model.activate(self.root)
        self.assertAlmostEqual(healthy.Shape.Volume, 60)
        self.assertEqual(healthy.ResultStatus, "Ready")
        # A broken reference must not prevent new work on independent inputs.
        sketch = Sketch.create(self.root)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 1))
        self.doc.recompute()
        operation, result = Extrude.create(self.root, sketch, 3)
        self.assertGreater(result.Shape.Volume, 9)
        identity, healthy_id = self.reference.ObjectId, healthy.ObjectId
        path = self.output / "Component-Broken-Reference.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(path)
        reference = next(obj for obj in self.doc.Objects if getattr(obj, "ObjectId", "") == identity)
        healthy = next(obj for obj in self.doc.Objects if getattr(obj, "ObjectId", "") == healthy_id)
        self.assertEqual(reference.ResultStatus, "Missing source")
        self.assertTrue(reference.ReferenceError)
        self.assertTrue(reference.Shape.isNull())
        self.assertAlmostEqual(healthy.Shape.Volume, 60)
        self.assertEqual(healthy.ResultStatus, "Ready")

    def testRepairPreservesDownstreamIdentityUndoAndRefusesAmbiguity(self):
        tool = self.body(self.root, "Tool", 0.5)
        operation = self.doc.addObject("Part::Cut", "ParentCut")
        Model.register_object(self.root, operation, "Operation")
        operation.Base, operation.Tool = self.reference, tool
        self.doc.recompute()
        result = Model.publish_result(self.root, operation)
        self.doc.recompute()
        identity, output_id, order = self.reference.ObjectId, result.ObjectId, list(self.root.ModelHistory)
        repaired = Model.repair_reference(self.root, self.reference, self.link, self.replacement)
        self.assertEqual(repaired, self.reference)
        self.assertEqual(repaired.ObjectId, identity)
        self.assertEqual(result.ObjectId, output_id)
        self.assertEqual(list(self.root.ModelHistory), order)
        self.assertEqual(operation.Base, repaired)
        self.assertAlmostEqual(result.Shape.Volume, 42)
        self.assertAlmostEqual(self.source.Shape.Volume, 24)
        self.doc.undo()
        Model.activate(self.root)
        self.assertEqual(self.reference.SourceObject, self.source)
        self.assertAlmostEqual(result.Shape.Volume, 18)
        self.doc.redo()
        Model.activate(self.root)
        self.assertAlmostEqual(result.Shape.Volume, 42)
        holder = self.doc.addObject("App::FeaturePython", "FaceConsumer")
        Model.register_object(self.root, holder, "Operation")
        holder.addProperty("App::PropertyLinkSub", "Support")
        holder.Support = (self.reference, ["Face1"])
        self.doc.recompute()
        with self.assertRaisesRegex(ValueError, "Face or edge consumers"):
            Model.repair_reference(self.root, self.reference, self.link, self.source)
        self.assertEqual(self.reference.SourceObject, self.replacement)
        self.assertEqual(holder.Support[0], self.reference)
        self.assertAlmostEqual(result.Shape.Volume, 42)

    def testHistoryRepairRefreshAndSuppression(self):
        self.break_reference()
        self.panel.refresh()
        row = self.panel.history.topLevelItem(0)
        menu = self.panel.build_menu(self.panel.history, row)
        self.assertIn("Repair Reference Object", [action.text() for action in menu.actions()])
        self.assertIn("Refresh References", [action.text() for action in menu.actions()])
        self.assertTrue(row.toolTip(3))
        self.assertIn("need repair", self.panel.reference_notice.text())
        self.panel.resize(650, 450)
        Gui.updateGui()
        self.panel.grab().save(str(self.output / "reference-needs-repair.png"))
        Gui.Selection.clearSelection()
        def choose(parent, title, prompt, labels, index, editable):
            self.assertEqual(title, "Repair Reference Object")
            return next(label for label in labels if self.replacement.Name in label), True
        with patch.object(QtWidgets.QInputDialog, "getItem", side_effect=choose):
            self.panel.edit_history(Navigator.object_key(self.reference))
        self.assertEqual(self.reference.SourceObject, self.replacement)
        self.assertEqual(self.reference.ResultStatus, "Ready")
        self.assertFalse(self.reference.ReferenceError)
        self.replacement.Shape = Part.makeBox(6, 3, 4)
        self.doc.recompute()
        self.assertEqual(self.reference.ResultStatus, "Pending")
        self.panel.refresh_references()
        self.assertAlmostEqual(self.reference.Shape.Volume, 72)
        Model.set_suppressed(self.reference, True)
        Model.repair_reference(self.root, self.reference, self.link, self.source)
        self.assertTrue(self.reference.UserSuppressed)
        self.assertEqual(self.reference.ResultStatus, "Suppressed")
        self.assertTrue(self.reference.Shape.isNull())
        Model.set_suppressed(self.reference, False)
        self.assertAlmostEqual(self.reference.Shape.Volume, 24)
        self.panel.refresh()
        self.assertFalse(self.panel.reference_notice.isVisible())
        Gui.updateGui()
        self.panel.grab().save(str(self.output / "reference-repaired.png"))
        self.doc.saveAs(str(self.output / "Component-Repaired-Reference.cadprt"))
