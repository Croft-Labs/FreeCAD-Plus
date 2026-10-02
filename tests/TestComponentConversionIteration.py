# SPDX-License-Identifier: LGPL-2.1-or-later
"""Three bounded conversion workflows for the component feedback round."""
import hashlib
import math
import os
from pathlib import Path
import unittest

import FreeCAD as App
import FreeCADGui as Gui
import Part
import CadDocument
import ComponentModel as Model
from PySide import QtWidgets
from freecad.gui import ComponentNavigator as Navigator


class TestComponentConversionIteration(unittest.TestCase):
    def setUp(self):
        source = Path(os.environ["FREECAD_PLUS_SOURCE"])
        for module, relative in [(Model, "src/Mod/Part/ComponentModel.py"),
                                 (Navigator, "src/Gui/ComponentNavigator.py")]:
            self.assertEqual(hashlib.sha256(Path(module.__file__).read_bytes()).digest(),
                             hashlib.sha256((source / relative).read_bytes()).digest())
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        self.doc = Model.new_document("Conversion feedback")
        self.root = Model.metadata(self.doc).RootComponent
        self.link = Model.add_component(self.root, label="Source component")
        self.child = self.link.LinkedObject
        with Model.transaction(self.doc, "Create source body"):
            self.box = self.doc.addObject("Part::Box", "SourceBox")
            Model.register_object(self.child, self.box, "Operation")
            self.box.Length, self.box.Width, self.box.Height = 2, 3, 4
            self.doc.recompute()
            self.body = Model.publish_result(self.child, self.box)
        self.reference = Model.add_reference(self.root, self.link, self.body)
        self.panel = Navigator.show(self.doc)

    def tearDown(self):
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if isinstance(widget, Navigator.ConversionDialog):
                widget.reject()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        Gui.updateGui()

    def mirror(self, source, name):
        with Model.transaction(self.doc, "Mirror geometry"):
            operation = self.doc.addObject("Part::Mirroring", name)
            Model.register_object(self.root, operation, "Operation")
            operation.Source, operation.Normal = source, App.Vector(1, 0, 0)
            self.doc.recompute()
            # Refresh explicitly delayed reference snapshots before publishing
            # another operation that consumes the evaluated result.
            Model.activate(self.root)
            result = Model.publish_result(self.root, operation, name + " body")
        return operation, result

    def testPruningKeepsChildComponentAndDownstreamIdentity(self):
        producer, result = self.mirror(self.reference, "ParentMirror")
        consumer, downstream = self.mirror(result, "DownstreamMirror")
        identity, result_name = result.ObjectId, result.Name
        child_names = [obj.Name for obj in self.child.Group]
        removed_names = {producer.Name, self.reference.Name}
        plan = Model.parameter_removal_plan(self.root, result)
        self.assertEqual({obj.Name for obj in plan["remove"]}, removed_names)
        self.assertNotIn(self.link, plan["remove"])
        Model.delete_parameters(self.root, result)
        self.assertTrue(result.Frozen)
        self.assertEqual(result.ObjectId, identity)
        self.assertEqual(consumer.Source, result)
        self.assertEqual([obj.Name for obj in self.child.Group], child_names)
        self.assertEqual(Model.children(self.root), [self.link])
        self.assertAlmostEqual(downstream.Shape.Volume, 24)
        self.assertTrue(all(self.doc.getObject(name) is None for name in removed_names))
        self.doc.undo()
        self.doc.recompute()
        Model.activate(self.root)
        self.assertFalse(result.Frozen)
        self.assertAlmostEqual(Model.current_shape(downstream).Volume, 24)
        self.assertTrue(all(self.doc.getObject(name) is not None for name in removed_names))
        self.doc.redo()
        self.doc.recompute()
        self.box.Length = 8
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 24)
        self.assertAlmostEqual(downstream.Shape.Volume, 24)
        self.assertAlmostEqual(self.body.Shape.Volume, 96)
        path = self.output / "Component-Converted-Body.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(path)
        self.root = Model.metadata(self.doc).RootComponent
        result = self.doc.getObject(result_name)
        self.assertEqual(result.ObjectId, identity)
        self.assertTrue(result.Frozen)
        self.assertEqual(len(Model.children(self.root)), 1)
        self.assertAlmostEqual(result.Shape.Volume, 24)

    def testReviewCancelExtractionAndSharedSketch(self):
        sketch = self.doc.addObject("Sketcher::SketchObject", "SharedProfile")
        Model.register_object(self.root, sketch)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        self.doc.recompute()
        first, body = Model.extrude(self.root, sketch, 3)
        second, other = Model.extrude(self.root, sketch, 5)
        names = [obj.Name for obj in self.doc.Objects]
        history = list(self.root.ModelHistory)
        dialog = Navigator.ConversionDialog(self.root, body, self.panel)
        actions = [(dialog.items.topLevelItem(i).text(0), dialog.items.topLevelItem(i).text(1))
                   for i in range(dialog.items.topLevelItemCount())]
        self.assertIn(("Remove", first.Label), actions)
        self.assertIn(("Keep shared", sketch.Label), actions)
        dialog.show()
        Gui.updateGui()
        dialog.grab().save(str(self.output / "conversion-review.png"))
        dialog.reject()
        self.assertEqual([obj.Name for obj in self.doc.Objects], names)
        self.assertEqual(list(self.root.ModelHistory), history)
        self.assertEqual(body.Producer, first)
        extract = Navigator.ConversionDialog(self.root, body, self.panel)
        extract.choice.setCurrentIndex(1)
        extract.accept()
        independent = extract.result_object
        self.assertIsNotNone(independent)
        self.assertFalse(hasattr(independent, "Producer"))
        self.assertAlmostEqual(independent.Shape.Volume, 12 * math.pi)
        self.assertEqual(body.Producer, first)
        independent_name = independent.Name
        self.doc.undo()
        self.doc.recompute()
        self.assertIsNone(self.doc.getObject(independent_name))
        conversion = Navigator.ConversionDialog(self.root, body, self.panel)
        conversion.accept()
        self.assertEqual(conversion.result_object, body, conversion.summary.text())
        self.assertIsNone(body.Producer)
        self.assertEqual(second.Base, sketch)
        second.LengthFwd = 7
        self.doc.recompute()
        self.assertAlmostEqual(body.Shape.Volume, 12 * math.pi)
        self.assertAlmostEqual(other.Shape.Volume, 28 * math.pi)
        self.assertIn("Independent geometry", Model.history_detail(body))
        self.doc.saveAs(str(self.output / "Component-Shared-History.cadprt"))

    def testReferenceDetachAndDumbSketchExtraction(self):
        identity, source_id = self.reference.ObjectId, self.reference.SourceObjectId
        Model.delete_parameters(self.root, self.reference)
        self.assertTrue(self.reference.Frozen)
        self.assertEqual(self.reference.ObjectId, identity)
        self.assertEqual(self.reference.SourceObjectId, "")
        self.assertIsNone(self.reference.SourceOccurrence)
        self.assertEqual(Model.children(self.root), [self.link])
        self.doc.undo()
        self.doc.recompute()
        Model.activate(self.root)
        self.assertEqual(self.reference.SourceObjectId, source_id)
        self.assertEqual(self.reference.SourceOccurrence, self.link)
        self.assertEqual(self.reference.ComponentRole, "Reference")
        sketch = self.doc.addObject("Sketcher::SketchObject", "ChildSketch")
        Model.register_object(self.child, sketch)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        self.doc.recompute()
        reference = Model.add_reference(self.root, self.link, sketch)
        dialog = Navigator.ConversionDialog(self.root, reference, self.panel)
        self.assertFalse(dialog.buttons.button(QtWidgets.QDialogButtonBox.Ok).isEnabled())
        self.assertIn("bodies and sheets", dialog.summary.text())
        dialog.choice.setCurrentIndex(1)
        dialog.accept()
        copy = dialog.result_object
        self.assertIsNotNone(copy)
        self.assertEqual(copy.GeometryKind, "Dumb Sketch")
        self.assertFalse(hasattr(copy, "SourceObject"))
        sketch.delGeometry(0)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 3))
        self.doc.recompute()
        Model.activate(self.root)
        self.assertAlmostEqual(reference.Shape.Length, 6 * math.pi)
        self.assertAlmostEqual(copy.Shape.Length, 4 * math.pi)
        self.doc.saveAs(str(self.output / "Component-Dumb-Sketch.cadprt"))
