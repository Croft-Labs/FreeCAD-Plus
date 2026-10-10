# SPDX-License-Identifier: LGPL-2.1-or-later
"""Filtered component output through real native writers and cached input guards."""
import os
from pathlib import Path
import unittest
import FreeCAD as App
import Part
import Mesh
import ComponentModel as Model


class TestComponentOutput(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_document("OutputTypes")
        self.root = Model.metadata(self.doc).RootComponent
        self.link = Model.add_component(self.root, label="Source")
        self.child = self.link.LinkedObject
        self.body = self.box(self.child, "SourceBody", 2)
        self.local = self.box(self.root, "LocalBody", 1)
        self.local.Placement.Base = App.Vector(20, 0, 0)
        self.link.LinkPlacement.Base = App.Vector(5, 0, 0)
        self.doc.recompute()
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])

    def tearDown(self):
        for doc in reversed(list(App.listDocuments().values())):
            App.closeDocument(doc.Name)

    def box(self, component, name, length):
        obj = component.Document.addObject("Part::Feature", name)
        Model.register_object(component, obj, "Object", True)
        obj.Shape = Part.makeBox(length, 3, 4)
        component.Document.recompute()
        return obj

    def testReferenceAndExcludedDoNotContribute(self):
        for mode in ("Reference", "Excluded"):
            Model.set_part_types(self.root, [(self.link, mode)])
            shapes = Model.output_shapes(self.root)
            self.assertEqual(len(shapes), 1)
            self.assertAlmostEqual(shapes[0].Volume, 12)
            self.assertAlmostEqual(shapes[0].BoundBox.XMin, 20)

    def testPromotedBodyContributesOnceAndUpdates(self):
        Model.set_part_types(self.root, [(self.link, "Reference")])
        reference = Model.add_reference(self.root, self.link, self.body)
        shapes = Model.output_shapes(self.root)
        self.assertEqual(len(shapes), 2)
        self.assertAlmostEqual(sum(s.Volume for s in shapes), 36)
        self.body.Shape = Part.makeBox(4, 3, 4)
        self.doc.recompute()
        Model.activate(self.root)
        self.assertAlmostEqual(sum(s.Volume for s in Model.output_shapes(self.root)), 60)
        self.assertIn(reference, Model.finished_results(self.root))

    def testNestedTypesAndHiddenFinishedResults(self):
        nested = Model.add_component(self.child, label="Nested")
        self.box(nested.LinkedObject, "NestedBody", 3)
        Model.set_part_types(self.child, [(nested, "Excluded")])
        self.body.Visibility = False
        self.link.Visibility = False
        self.assertAlmostEqual(sum(s.Volume for s in Model.output_shapes(self.root)), 36)

    def testOccurrenceTransformAndScale(self):
        self.child.Placement.Base = App.Vector(2, 0, 0)
        self.link.Scale = 2
        self.doc.recompute()
        with Model.export_objects([self.link]) as output:
            expected = Part.getShape(self.link, self.body.Name + ".", transform=True)
            self.assertEqual(len(output), 1)
            self.assertAlmostEqual(output[0].Shape.Volume, expected.Volume)
            self.assertAlmostEqual(output[0].Shape.BoundBox.XMin, expected.BoundBox.XMin)

    def testNativeStepAndStlExcludeUnpromotedSources(self):
        Model.set_part_types(self.root, [(self.link, "Reference")])
        Model.add_reference(self.root, self.link, self.body)
        step = self.output / "filtered.step"
        stl = self.output / "filtered.stl"
        names = set(App.listDocuments())
        with Model.export_objects([self.root]) as output:
            Part.export(output, str(step))
            Part.export(output, str(stl))
        self.assertEqual(set(App.listDocuments()), names)
        shape = Part.read(str(step))
        self.assertEqual(len(shape.Solids), 2)
        self.assertAlmostEqual(shape.Volume, 36)
        mesh = Mesh.Mesh(str(stl))
        self.assertTrue(mesh.isSolid())
        self.assertAlmostEqual(abs(mesh.Volume), 36, places=4)

    def testExplicitExcludedOccurrenceFailsBeforeWriter(self):
        Model.set_part_types(self.root, [(self.link, "Excluded")])
        names = set(App.listDocuments())
        with self.assertRaises(ValueError):
            with Model.export_objects([self.link]):
                self.fail("Excluded occurrence reached writer")
        self.assertEqual(set(App.listDocuments()), names)

    def testTemporaryObjectsCleanUpOnWriterFailure(self):
        names = set(App.listDocuments())
        with self.assertRaisesRegex(RuntimeError, "writer failure"):
            with Model.export_objects([self.root]):
                raise RuntimeError("writer failure")
        self.assertEqual(set(App.listDocuments()), names)
        self.assertEqual(App.ActiveDocument, self.doc)

    def testRawNativeInputCannotPublishCachedResult(self):
        Model.set_part_types(self.root, [(self.link, "Reference")])
        reference = Model.add_reference(self.root, self.link, self.body)
        self.local.Placement.Base = App.Vector(5, 0, 0)
        operation = self.doc.addObject("Part::Fuse", "RawFuse")
        Model.register_object(self.root, operation, "Operation")
        operation.Base, operation.Tool = reference, self.local
        self.doc.recompute()
        result = Model.publish_result(self.root, operation)
        self.doc.recompute()
        self.assertFalse(result.Shape.isNull())
        # Replace the explicit owned reference with a foreign native input.
        operation.Base = self.body
        self.doc.recompute()
        self.assertFalse(operation.Shape.isNull())
        with self.assertRaisesRegex(ValueError, "Reference Feature"):
            Model.current_shape(operation)
        before = set(o.Name for o in self.doc.Objects)
        with self.assertRaisesRegex(ValueError, "Reference Feature"):
            Model.publish_result(self.root, operation)
        self.assertEqual(set(o.Name for o in self.doc.Objects), before)
        self.assertTrue(result.Shape.isNull())
        self.assertEqual(result.ResultStatus, "Unavailable")
        with self.assertRaises(ValueError):
            Model.output_shapes(self.root)

    def testExplicitReferenceAllowsNativeConsumer(self):
        Model.set_part_types(self.root, [(self.link, "Reference")])
        reference = Model.add_reference(self.root, self.link, self.body)
        operation = self.doc.addObject("Part::Fuse", "OwnedFuse")
        Model.register_object(self.root, operation, "Operation")
        operation.Base, operation.Tool = reference, self.local
        self.doc.recompute()
        self.assertAlmostEqual(Model.current_shape(operation).Volume, 36)
