# SPDX-License-Identifier: LGPL-2.1-or-later
"""Preserve archived legacy geometry and identities through installed conversion."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import unittest
import FreeCAD as App
import Part
import CadDocument
import ComponentModel as Model
from LegacyConversion import is_datum


class TestLegacyArchivedFiles(unittest.TestCase):
    def tearDown(self):
        for name in list(App.listDocuments()):
            App.closeDocument(name)

    def same(self, before, after):
        self.assertFalse(after.isNull())
        self.assertEqual((len(before.Solids), len(before.Faces), len(before.Edges), len(before.Vertexes)),
                         (len(after.Solids), len(after.Faces), len(after.Edges), len(after.Vertexes)))
        for attr in ('Volume', 'Area', 'Length'):
            value = getattr(before, attr)
            self.assertAlmostEqual(value, getattr(after, attr), delta=max(1e-7, abs(value) * 1e-8))
        # Cached display triangulation can overestimate bounds of curved legacy
        # shapes. Compare geometry-derived bounds in both documents instead.
        before_box = before.optimalBoundingBox(False, False)
        after_box = after.optimalBoundingBox(False, False)
        for attr in ('XMin', 'YMin', 'ZMin', 'XMax', 'YMax', 'ZMax'):
            self.assertAlmostEqual(getattr(before_box, attr), getattr(after_box, attr), places=6)
        if before.Solids and before.isValid() and after.isValid():
            tolerance = max(1e-7, before.Volume * 1e-8)
            self.assertLessEqual(before.cut(after).Volume, tolerance)
            self.assertLessEqual(after.cut(before).Volume, tolerance)
        elif not before.Solids:
            for source, target in ((before, after), (after, before)):
                for edge in source.Edges:
                    for point in edge.discretize(Number=21):
                        self.assertLessEqual(Part.Vertex(point).distToShape(target)[0], 1e-6)

    def check_file(self, relative):
        source = Path(os.environ['FREECAD_PLUS_SOURCE']) / relative
        digest = hashlib.sha256(source.read_bytes()).digest()
        output = Path(os.environ['FREECAD_PLUS_VALIDATION_DIR']) / 'archived'
        output.mkdir(exist_ok=True)
        original = output / source.name
        shutil.copy2(source, original)
        doc = App.openDocument(str(original))
        doc.recompute()
        identities = {o.Name: (o.TypeId, o.ID, o.Label) for o in doc.Objects}
        frames = {o.Name: App.Placement(o.getGlobalPlacement()) for o in doc.Objects if is_datum(o)}
        shapes = {o.Name: Part.getShape(o).copy() for o in doc.Objects
                  if not is_datum(o) and 'Shape' in o.PropertiesList and not o.Shape.isNull()}
        self.assertTrue(shapes, 'Fixture must contain evaluated geometry')
        baseline_states = {o.Name: list(o.State) for o in doc.Objects
                           if 'Invalid' in o.State or 'Touched' in o.State}
        CadDocument.convert_legacy(doc)
        Model.validate(doc)
        report = list(Model.metadata(doc).ConversionReport)
        for name, state in baseline_states.items():
            if 'Invalid' in state:
                label = doc.getObject(name).Label
                self.assertTrue(any(label in line and ('repair' in line or 'unverified' in line)
                                    for line in report), name)
        (output / (source.stem + '-audit.json')).write_text(json.dumps({
            'source': relative, 'original_objects': len(identities),
            'evaluated_shapes': len(shapes), 'baseline_unready_objects': baseline_states,
            'datum_frames': len(frames),
            'invalid_baseline_shapes': [name for name, shape in shapes.items() if not shape.isValid()],
            'conversion_report': report,
            'finished_results': {c.Name: [o.Name for o in Model.finished_results(c)]
                                 for c in Model.definitions(doc)},
        }, indent=2))
        for name, identity in identities.items():
            obj = doc.getObject(name)
            self.assertIsNotNone(obj, name)
            self.assertEqual((obj.TypeId, obj.ID, obj.Label), identity, name)
        for name, shape in shapes.items():
            with self.subTest(stage='converted', object=name):
                self.same(shape, Part.getShape(doc.getObject(name)))
        for name, frame in frames.items():
            self.assertTrue(doc.getObject(name).getGlobalPlacement().isSame(frame, 1e-8), name)
        ids = {o.Name: o.ObjectId for o in doc.Objects if 'ObjectId' in o.PropertiesList}
        saved = output / (source.stem + '.cadprt')
        doc.saveAs(str(saved))
        App.closeDocument(doc.Name)
        doc = CadDocument.open(saved)
        Model.validate(doc)
        for name, oid in ids.items():
            self.assertEqual(doc.getObject(name).ObjectId, oid, name)
        for name, shape in shapes.items():
            with self.subTest(stage='restored', object=name):
                self.same(shape, Part.getShape(doc.getObject(name)))
        for name, frame in frames.items():
            self.assertTrue(doc.getObject(name).getGlobalPlacement().isSame(frame, 1e-8), name)
        self.assertEqual(hashlib.sha256(source.read_bytes()).digest(), digest)
        self.assertEqual(hashlib.sha256(original.read_bytes()).digest(), digest)

    def test_pad(self):
        self.check_file('data/tests/PadTest.fcstd')

    def test_pocket(self):
        self.check_file('data/tests/PocketTest.fcstd')

    def test_old_part_design(self):
        self.check_file('tests/src/Mod/PartDesign/App/TestModels/ModelFromV021.FCStd')

    def test_part_design_example(self):
        self.check_file('data/examples/PartDesignExample.FCStd')

    def test_engine_block(self):
        self.check_file('data/examples/EngineBlock.FCStd')

    def test_crank(self):
        self.check_file('data/tests/Crank.fcstd')


class TestLegacyArchivedFilesCold(TestLegacyArchivedFiles):
    """Run separately after the archive suite, in a fresh native process."""
    def check_file(self, relative):
        source = Path(os.environ['FREECAD_PLUS_SOURCE']) / relative
        digest = hashlib.sha256(source.read_bytes()).digest()
        output = Path(os.environ['FREECAD_PLUS_VALIDATION_DIR']) / 'archived'
        original = output / source.name
        baseline = App.openDocument(str(original))
        baseline.recompute()
        identities = {o.Name: (o.TypeId, o.Label) for o in baseline.Objects}
        frames = {o.Name: App.Placement(o.getGlobalPlacement()) for o in baseline.Objects if is_datum(o)}
        shapes = {o.Name: Part.getShape(o).copy() for o in baseline.Objects
                  if not is_datum(o) and 'Shape' in o.PropertiesList and not o.Shape.isNull()}
        self.assertTrue(shapes)
        App.closeDocument(baseline.Name)
        doc = CadDocument.open(output / (source.stem + '.cadprt'))
        Model.validate(doc)
        for name, identity in identities.items():
            obj = doc.getObject(name)
            self.assertIsNotNone(obj, name)
            self.assertEqual((obj.TypeId, obj.Label), identity, name)
        for name, shape in shapes.items():
            with self.subTest(object=name):
                self.same(shape, Part.getShape(doc.getObject(name)))
        for name, frame in frames.items():
            self.assertTrue(doc.getObject(name).getGlobalPlacement().isSame(frame, 1e-8), name)
        self.assertEqual(hashlib.sha256(source.read_bytes()).digest(), digest)
        self.assertEqual(hashlib.sha256(original.read_bytes()).digest(), digest)
