# SPDX-License-Identifier: LGPL-2.1-or-later
"""Prevent direct native geometry use while preserving explicitly owned references."""
import os
from pathlib import Path
import unittest

import FreeCAD as App
import Part
import CadDocument
import ComponentModel as Model
from BasicShapes import ShapeReferences as Shapes


class TestComponentGeometryAccess(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_document("GeometryAccess")
        self.root = Model.metadata(self.doc).RootComponent
        self.link = Model.add_component(self.root, label="Child")
        self.child = self.link.LinkedObject
        self.source = self.body(self.child, "Source", 2)
        self.local = self.body(self.root, "Local", 1)
        Model.set_part_types(self.root, [(self.link, "Reference")])

    def tearDown(self):
        for doc in reversed(list(App.listDocuments().values())):
            App.closeDocument(doc.Name)

    def body(self, component, name, size):
        obj = self.doc.addObject("Part::Feature", name)
        Model.register_object(component, obj, "Object", True)
        obj.Shape = Part.makeBox(size, 3, 4)
        self.doc.recompute()
        return obj

    def testDirectLinkAndNativePathRefused(self):
        for mode in ("Reference", "Excluded"):
            Model.set_part_types(self.root, [(self.link, mode)])
            self.link.Visibility = True
            for obj, sub in ((self.link, ""), (self.link, self.source.Name + ".Face1"),
                             (self.root, self.link.Name + "." + self.source.Name + ".Face1")):
                with self.subTest(mode=mode, obj=obj.Name, sub=sub):
                    with self.assertRaisesRegex(Shapes.ReferenceError, "Reference Feature"):
                        Shapes.linked_shape((obj, [sub] if sub else []))
            with self.assertRaises(ValueError):
                Model.current_shape(self.link)

    def testUnfilteredAggregateRefusedButOwnedResultAllowed(self):
        with self.assertRaisesRegex(ValueError, "whole native shape"):
            Shapes.linked_shape((self.root, []))
        shape = Shapes.linked_shape((self.root, [self.local.Name + "."]))
        self.assertAlmostEqual(shape.Volume, 12)
        self.assertAlmostEqual(Model.current_shape(self.local).Volume, 12)

    def testForeignBareSourceRequiresExplicitReference(self):
        feature = self.doc.addObject("Part::Feature", "Consumer")
        Model.register_object(self.root, feature, "Object")
        with self.assertRaisesRegex(Shapes.ReferenceError, "Reference Feature"):
            Shapes.validate_link(feature, self.source)
        # The source remains usable when working inside its own definition.
        Shapes.validate_link(self.source, self.child.Origin.OriginFeatures[0])
        self.assertAlmostEqual(Model.current_shape(self.source).Volume, 24)

    def testPromotedBodyRemainsUsableAndUpdates(self):
        reference = Model.add_reference(self.root, self.link, self.source)
        self.assertEqual(Model.owner(reference), self.root)
        self.assertIn(reference, Model.finished_results(self.root))
        Shapes.validate_link(self.local, reference)
        self.assertAlmostEqual(Shapes.linked_shape((reference, [])).Volume, 24)
        self.source.Shape = Part.makeBox(5, 3, 4)
        self.doc.recompute()
        Model.activate(self.root)
        self.assertAlmostEqual(Model.current_shape(reference).Volume, 60)
        # Excluding the display source must not sever an already explicit dependency.
        Model.set_part_types(self.root, [(self.link, "Excluded")])
        Model.activate(self.root)
        self.assertAlmostEqual(Model.current_shape(reference).Volume, 60)

    def testNestedAggregateAndSiblingPaths(self):
        outer = Model.add_component(self.root, label="Outer")
        nested = Model.add_component(outer.LinkedObject, self.child)
        allowed = self.body(outer.LinkedObject, "Allowed", 3)
        Model.set_part_types(outer.LinkedObject, [(nested, "Excluded")])
        with self.assertRaisesRegex(ValueError, "whole native shape"):
            Shapes.linked_shape((outer, []))
        self.assertAlmostEqual(Shapes.linked_shape((outer, [allowed.Name + "."])).Volume, 36)
        with self.assertRaisesRegex(Shapes.ReferenceError, "Reference Feature"):
            Shapes.linked_shape((outer, [nested.Name + "." + self.source.Name + "."]))

    def testSharedChildCanStillBeUsedThroughAllowedOccurrence(self):
        other = Model.add_component(self.root, self.child)
        self.assertAlmostEqual(Shapes.linked_shape((other, [self.source.Name + "."])).Volume, 24)
        with self.assertRaises(ValueError):
            Shapes.linked_shape((self.link, [self.source.Name + "."]))

    def testOwnedReferenceSurvivesSaveReopenAndUndo(self):
        reference = Model.add_reference(self.root, self.link, self.source)
        names = self.root.Name, self.link.Name, reference.Name
        Model.set_part_types(self.root, [(self.link, "Excluded")])
        self.doc.undo()
        Model.activate(self.root)
        self.assertEqual(Model.part_type(self.root, self.link), "Reference")
        self.assertAlmostEqual(Model.current_shape(reference).Volume, 24)
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "reference-geometry.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(str(path))
        root, link, reference = [self.doc.getObject(name) for name in names]
        Model.activate(root)
        self.assertAlmostEqual(Model.current_shape(reference).Volume, 24)
        with self.assertRaises(ValueError):
            Shapes.linked_shape((link, []))

    def testOrdinaryNativeObjectsRetainWorldPlacement(self):
        doc = App.newDocument("OrdinaryGeometry")
        parent = doc.addObject("App::Part", "Container")
        obj = doc.addObject("Part::Feature", "Box")
        parent.addObject(obj)
        obj.Shape = Part.makeBox(2, 3, 4)
        parent.Placement.Base = App.Vector(10, 0, 0)
        doc.recompute()
        shape = Shapes.linked_shape((obj, []))
        self.assertAlmostEqual(shape.Volume, 24)
        self.assertAlmostEqual(shape.BoundBox.XMin, 10)
