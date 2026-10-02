# SPDX-License-Identifier: LGPL-2.1-or-later
"""Native component ownership, geometry, identity and persistence regressions."""
import json
import hashlib
import importlib.util
import math
import os
from pathlib import Path
import sys
import unittest
import zipfile

import FreeCAD as App
import Part
import Sketcher

if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src/Mod/Part"))
import ComponentModel as Model
import CadDocument


class TestComponentDocument(unittest.TestCase):
    def setUp(self):
        self.doc = Model.new_document("Root component")
        self.root = Model.metadata(self.doc).RootComponent
        self.child = Model.create_definition(self.doc, "Child")
        self.link = Model.add_component(self.root, self.child)
        self.output = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"])
        source = Path(__file__).resolve().parents[1]
        identities = []
        for module, relative in [(Model, "src/Mod/Part/ComponentModel.py"),
                                 (CadDocument, "src/Mod/Part/CadDocument.py")]:
            digest = hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
            self.assertEqual(digest, hashlib.sha256((source / relative).read_bytes()).hexdigest())
            identities.append({"source": relative, "loaded": module.__file__, "sha256": digest})
        (self.output / "module-identities.json").write_text(json.dumps(identities, indent=2))

    def tearDown(self):
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)

    def box(self, component=None):
        component = component or self.child
        box = self.doc.addObject("Part::Box", "Box")
        box.Length, box.Width, box.Height = 2, 3, 4
        Model.register_object(component, box, "Operation")
        self.doc.recompute()
        result = Model.publish_result(component, box)
        self.doc.recompute()
        return box, result

    def testSharedDefinitionsAndCycleRefusal(self):
        box, result = self.box()
        second = Model.add_component(self.root, self.child,
                                     placement=App.Placement(App.Vector(20, 0, 0), App.Rotation()))
        self.assertEqual(second.LinkedObject, self.link.LinkedObject)
        self.assertNotEqual(second.ObjectId, self.link.ObjectId)
        self.assertEqual(str(second.Representation), "Bodies Only")
        count = len(self.doc.Objects)
        with self.assertRaises(ValueError):
            Model.add_component(self.child, self.root)
        self.assertEqual(len(self.doc.Objects), count)
        box.Length = 7
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 84)
        self.assertEqual(second.LinkPlacement.Base.x, 20)
        Model.validate(self.doc)

    def testDirectChildReferenceDelayedRefreshAndParentEdit(self):
        box, result = self.box()
        self.link.LinkPlacement = App.Placement(App.Vector(12, 0, 0), App.Rotation())
        self.doc.recompute()
        ref = Model.add_reference(self.root, self.link, result)
        self.assertAlmostEqual(ref.Shape.BoundBox.XMin, 12)
        self.assertAlmostEqual(ref.Shape.Volume, 24)
        self.assertEqual(ref.ResultStatus, "Ready")
        snapshot = Model.extract_dumb(self.root, ref)
        box.Length = 5
        self.doc.recompute()
        self.assertEqual(ref.ResultStatus, "Pending")
        with self.assertRaises(ValueError):
            Model.current_shape(ref)
        Model.activate(self.root)
        self.assertEqual(ref.ResultStatus, "Ready")
        self.assertAlmostEqual(ref.Shape.Volume, 60)
        self.assertAlmostEqual(snapshot.Shape.Volume, 24)
        snapshot.Placement.Base = App.Vector(99, 0, 0)
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 60)
        self.assertEqual(box.Placement.Base.x, 0)

    def testGrandchildAndUnrelatedReferencesRefused(self):
        box, result = self.box()
        grandchild = Model.create_definition(self.doc, "Grandchild")
        grandlink = Model.add_component(self.child, grandchild)
        grandbox, grandresult = self.box(grandchild)
        for link, source in [(self.link, grandresult), (grandlink, grandresult),
                             (self.link, box)]:
            with self.assertRaises(ValueError):
                Model.add_reference(self.root, link, source)

    def testDumbSketchReferenceContainsNoConstraints(self):
        sketch = self.doc.addObject("Sketcher::SketchObject", "Sketch")
        Model.register_object(self.child, sketch)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        sketch.addConstraint(Sketcher.Constraint("Radius", 0, 2))
        self.doc.recompute()
        ref = Model.add_reference(self.root, self.link, sketch)
        self.assertEqual(ref.GeometryKind, "Dumb Sketch")
        self.assertFalse(hasattr(ref, "Constraints"))
        operation, result = Model.extrude(self.root, ref, 3)
        self.assertAlmostEqual(result.Shape.Volume, math.pi * 4 * 3)
        sketch.setDatum(0, App.Units.Quantity("3 mm"))
        self.doc.recompute()
        Model.activate(self.root)
        self.assertAlmostEqual(result.Shape.Volume, math.pi * 9 * 3)

    def testSheetsCurvesAndOccurrenceTransforms(self):
        sheet = self.doc.addObject("Part::Feature", "Sheet")
        sheet.Shape = Part.makePlane(4, 3)
        Model.register_object(self.child, sheet, result=True)
        curve = self.doc.addObject("Part::Feature", "Curve")
        curve.Shape = Part.makeLine(App.Vector(), App.Vector(0, 7, 0))
        Model.register_object(self.child, curve)
        self.root.Placement = App.Placement(App.Vector(100, 20, -6), App.Rotation(App.Vector(0, 0, 1), 27))
        self.child.Placement = App.Placement(App.Vector(4, 5, 6), App.Rotation(App.Vector(1, 0, 0), 20))
        self.link.LinkTransform = True
        self.link.LinkPlacement = App.Placement(App.Vector(10, 0, 0), App.Rotation(App.Vector(0, 1, 0), 35))
        self.doc.recompute()
        for source, kind in [(sheet, "Sheet"), (curve, "Curve")]:
            ref = Model.add_reference(self.root, self.link, source)
            self.assertEqual(ref.GeometryKind, kind)
            expected = self.root.getSubObject(self.link.Name + "." + source.Name + ".")
            actual = self.root.getSubObject(ref.Name + ".")
            self.assertAlmostEqual(actual.distToShape(expected)[0], 0, places=6)
            self.assertAlmostEqual(actual.CenterOfMass.x, expected.CenterOfMass.x, places=6)
            self.assertAlmostEqual(actual.CenterOfMass.y, expected.CenterOfMass.y, places=6)
            self.assertAlmostEqual(actual.CenterOfMass.z, expected.CenterOfMass.z, places=6)
            self.assertAlmostEqual(actual.Length, expected.Length, places=6)

    def testOccurrenceOverrideInheritanceAndHiddenAncestor(self):
        grandchild = Model.create_definition(self.doc, "Grandchild")
        grandlink = Model.add_component(self.child, grandchild)
        other = Model.add_component(self.root, self.child)
        Model.set_representation(self.child, [grandlink.ObjectId], "Full Component")
        path = [self.link.ObjectId, grandlink.ObjectId]
        self.assertEqual(Model.representation(self.root, path), "Full Component")
        Model.set_representation(self.root, path, "Hidden")
        self.assertEqual(Model.representation(self.root, path), "Hidden")
        self.assertEqual(Model.representation(self.root, [other.ObjectId, grandlink.ObjectId]), "Full Component")
        Model.set_representation(self.root, path)
        self.assertEqual(Model.representation(self.root, path), "Full Component")
        Model.set_representation(self.root, [self.link.ObjectId], "Hidden")
        self.assertEqual(Model.representation(self.root, path), "Hidden")

    def testDeleteParametersRetainsSharedProducerAndUndo(self):
        box, result = self.box()
        second = Model.publish_result(self.child, box, "Other body")
        self.doc.recompute()
        identity = result.ObjectId
        Model.delete_parameters(self.child, result)
        self.assertIsNone(result.Producer)
        self.assertEqual(result.ObjectId, identity)
        self.assertEqual(second.Producer, box)
        box.Length = 9
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 24)
        self.assertAlmostEqual(second.Shape.Volume, 108)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(result.Producer, box)
        self.assertEqual(result.ObjectId, identity)

    def testExclusiveProducerPrunedButDownstreamIdentityRetained(self):
        box, result = self.box()
        name, identity = box.Name, result.ObjectId
        consumer = self.doc.addObject("Part::Mirroring", "Mirror")
        self.child.addObject(consumer)
        consumer.Source = result
        consumer.Normal = App.Vector(1, 0, 0)
        self.doc.recompute()
        Model.delete_parameters(self.child, result)
        self.assertIsNone(self.doc.getObject(name))
        self.assertEqual(consumer.Source, result)
        self.assertEqual(result.ObjectId, identity)
        self.assertAlmostEqual(consumer.Shape.Volume, 24)
        self.doc.undo()
        self.doc.recompute()
        self.assertIsNotNone(self.doc.getObject(name))

    def testVersionedNativeSaveAndReopen(self):
        box, result = self.box()
        ref = Model.add_reference(self.root, self.link, result)
        identity = result.ObjectId
        path = self.output / "Components.cadprt"
        self.doc.saveAs(str(path))
        self.assertEqual(self.doc.FileName, str(path))
        self.assertTrue(path.is_file())
        data = CadDocument.preflight(path)
        self.assertEqual(data["root"], self.root.ObjectId)
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(path)
        restored = next(
            o for o in self.doc.Objects if getattr(o, "ObjectId", "") == identity)
        self.assertAlmostEqual(restored.Shape.Volume, 24)
        restored.Producer.Length = 8
        self.doc.recompute()
        Model.activate(Model.metadata(self.doc).RootComponent)
        reference = next(o for o in self.doc.Objects if getattr(o, "ComponentRole", "") == "Reference")
        self.assertAlmostEqual(reference.Shape.Volume, 96)

    def testUnsupportedAndRenamedLegacyFilesRefused(self):
        path = self.output / "Unsupported.cadprt"
        data = json.loads(CadDocument.manifest(self.doc))
        data["required"].append("unknown-required-capability")
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("Document.xml", "<Document/>")
            archive.writestr(CadDocument.MANIFEST, json.dumps(data))
        with self.assertRaises(ValueError):
            CadDocument.preflight(path)
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("Document.xml", "<Document/>")
        with self.assertRaises(ValueError):
            CadDocument.preflight(path)

    def testMakeIndependentKeepsChildDefinitionsShared(self):
        box, result = self.box()
        grand = Model.create_definition(self.doc, "Grandchild")
        grandlink = Model.add_component(self.child, grand)
        other = Model.add_component(self.root, self.child)
        copied = Model.make_independent(self.link)
        self.assertNotEqual(copied.ObjectId, self.child.ObjectId)
        self.assertEqual(other.LinkedObject, self.child)
        self.assertEqual(Model.children(copied)[0].LinkedObject, grand)
        copied_box = next(o for o in copied.Group if o.TypeId == "Part::Box")
        copied_result = next(o for o in copied.Group if getattr(o, "ComponentRole", "") == "Result")
        self.assertEqual(copied_result.Producer, copied_box)
        copied_box.Length = 10
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 24)
        self.assertAlmostEqual(copied_result.Shape.Volume, 120)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(self.link.LinkedObject, self.child)

    def testDeleteReferenceParametersStopsUpdatesAndUndoRestoresLink(self):
        box, result = self.box()
        ref = Model.add_reference(self.root, self.link, result)
        identity = ref.ObjectId
        Model.delete_parameters(self.root, ref)
        box.Length = 10
        self.doc.recompute()
        Model.activate(self.root)
        self.assertEqual(ref.ObjectId, identity)
        self.assertAlmostEqual(ref.Shape.Volume, 24)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(ref.ComponentRole, "Reference")
        self.assertEqual(ref.SourceObject, result)
        Model.activate(self.root)
        self.assertEqual(ref.ResultStatus, "Ready")

    def testSuppressionBlocksDependentsNotIndependentBranches(self):
        box, result = self.box()
        independent, independent_result = self.box()
        mirror = self.doc.addObject("Part::Mirroring", "Mirror")
        Model.register_object(self.child, mirror, "Operation")
        mirror.Source = result
        mirror.Normal = App.Vector(1, 0, 0)
        self.doc.recompute()
        output = Model.publish_result(self.child, mirror)
        self.doc.recompute()
        Model.set_suppressed(mirror, True)
        Model.set_suppressed(box, True)
        self.assertTrue(result.Shape.isNull())
        self.assertTrue(output.Shape.isNull())
        self.assertAlmostEqual(independent_result.Shape.Volume, 24)
        Model.set_suppressed(box, False)
        self.assertAlmostEqual(result.Shape.Volume, 24)
        self.assertTrue(output.Shape.isNull())
        self.assertTrue(mirror.UserSuppressed)
        Model.set_suppressed(mirror, False)
        self.assertAlmostEqual(output.Shape.Volume, 24)

    def testExternalComponentReferenceSaveReopen(self):
        external = Model.new_document("External")
        extroot = Model.metadata(external).RootComponent
        shape = external.addObject("Part::Feature", "ExternalShape")
        Model.register_object(extroot, shape, result=True)
        shape.Shape = Part.makeBox(3, 4, 5)
        external.recompute()
        extpath = self.output / "External.cadprt"
        external.saveAs(str(extpath))
        path = self.output / "ExternalParent.cadprt"
        self.doc.saveAs(str(path))
        occurrence = Model.add_component(self.root, extroot)
        ref = Model.add_reference(self.root, occurrence, shape)
        self.assertAlmostEqual(ref.Shape.Volume, 60)
        self.doc.saveAs(str(path))
        parent_id = Model.metadata(self.doc).ObjectId
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        self.doc = CadDocument.open(path)
        self.assertEqual(Model.metadata(self.doc).ObjectId, parent_id)
        reference = next(o for o in self.doc.Objects if getattr(o, "ComponentRole", "") == "Reference")
        Model.activate(Model.metadata(self.doc).RootComponent)
        self.assertAlmostEqual(reference.Shape.Volume, 60)

    def testLegacyConversionPreservesOriginalAndEditableFeatures(self):
        legacy = App.newDocument("Legacy")
        box = legacy.addObject("Part::Box", "Box")
        box.Length, box.Width, box.Height = 2, 3, 4
        legacy.recompute()
        original = self.output / "Legacy.FCStd"
        legacy.saveAs(str(original))
        digest = hashlib.sha256(original.read_bytes()).hexdigest()
        App.closeDocument(legacy.Name)
        converted = CadDocument.open_legacy(original)
        self.assertEqual(converted.FileName, "")
        meta = Model.metadata(converted)
        self.assertEqual(Path(meta.LegacySource).resolve(), original.resolve())
        self.assertTrue(meta.ConversionReport)
        result = next(o for o in converted.Objects if getattr(o, "ComponentRole", "") == "Result")
        converted.Box.Length = 7
        converted.recompute()
        self.assertAlmostEqual(result.Shape.Volume, 84)
        target = self.output / "Converted.cadprt"
        converted.saveAs(str(target))
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), digest)
        with self.assertRaises(Exception):
            converted.saveCopy(str(original))
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), digest)
        App.closeDocument(converted.Name)
        reopened = CadDocument.open(target)
        self.assertAlmostEqual(reopened.Box.Shape.Volume, 84)

    def testFailedSavePreservesExistingArchive(self):
        self.box()
        target = self.output / "Atomic.cadprt"
        self.doc.saveAs(str(target))
        original = target.read_bytes()
        self.child.ObjectId = self.root.ObjectId
        with self.assertRaises(Exception):
            self.doc.save()
        self.assertEqual(target.read_bytes(), original)

    def testRequiredSchemaCheckedForRecoveryAndRenamedFiles(self):
        self.box()
        native = self.output / "RecoverySource.cadprt"
        self.doc.saveAs(str(native))
        App.closeDocument(self.doc.Name)
        for suffix in ("FCBak", "FCStd"):
            altered = self.output / ("UnsupportedSchema." + suffix)
            with zipfile.ZipFile(native) as source, zipfile.ZipFile(altered, "w") as target:
                for entry in source.infolist():
                    payload = source.read(entry.filename)
                    if entry.filename == CadDocument.MANIFEST:
                        manifest = json.loads(payload)
                        manifest["required"].append("unsupported-reader-capability")
                        payload = json.dumps(manifest).encode()
                    target.writestr(entry, payload)
            with self.assertRaises(Exception):
                App.openDocument(str(altered))

    def testExternalizeLeafPreservesIdentityAndAllInstances(self):
        box, result = self.box()
        second = Model.add_component(self.root, self.child)
        ref = Model.add_reference(self.root, self.link, result)
        identity = self.child.ObjectId
        result_identity = result.ObjectId
        parent_path = self.output / "BeforeExternalize.cadprt"
        self.doc.saveAs(str(parent_path))
        new_root = Model.externalize(self.child, self.output / "Externalized.cadprt")
        self.assertEqual(new_root.ObjectId, identity)
        self.assertEqual(self.link.LinkedObject, new_root)
        self.assertEqual(second.LinkedObject, new_root)
        self.assertEqual(ref.SourceObject.ObjectId, result_identity)
        ref.SourceObject.Producer.Length = 9
        new_root.Document.recompute()
        Model.activate(self.root)
        self.assertAlmostEqual(ref.Shape.Volume, 108)
        new_root.Document.save()
        self.doc.save()
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(self.link.LinkedObject.Document, self.doc)
        self.assertEqual(self.link.LinkedObject.ObjectId, identity)

    def testExternalizeAssemblyPreservesSharedChildAndReferences(self):
        grandchild = Model.create_definition(self.doc, "Shared grandchild")
        inner = Model.add_component(self.child, grandchild)
        peer = Model.add_component(self.root, grandchild)
        box, body = self.box(grandchild)
        ref = Model.add_reference(self.child, inner, body)
        self.doc.saveAs(str(self.output / "AssemblyOwner.cadprt"))
        moved = Model.externalize(self.child, self.output / "AssemblyExternal.cadprt")
        self.assertEqual(self.link.LinkedObject, moved)
        inner = Model.children(moved)[0]
        self.assertEqual(inner.LinkedObject, peer.LinkedObject)
        self.assertEqual(inner.LinkedObject.Document, moved.Document)
        ref = next(o for o in Model.history(moved) if o.ComponentRole == "Reference")
        self.assertEqual(ref.SourceObject.Document, moved.Document)
        Model.activate(moved)
        self.assertAlmostEqual(Model.current_shape(ref).Volume, 24)
        Model.validate(self.doc)
        self.doc.save()
        owner_path = self.doc.FileName
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        self.doc = CadDocument.open(owner_path)
        self.root = Model.metadata(self.doc).RootComponent
        links = Model.children(self.root)
        moved = links[0].LinkedObject
        self.assertEqual(Model.children(moved)[0].LinkedObject, links[1].LinkedObject)

    def testMakeExternalDefinitionIndependentKeepsChildShared(self):
        grandchild = Model.create_definition(self.doc, "Shared child")
        Model.add_component(self.child, grandchild)
        self.box(self.child)
        self.box(grandchild)
        self.doc.saveAs(str(self.output / "IndependentOwner.cadprt"))
        moved = Model.externalize(self.child, self.output / "IndependentExternal.cadprt")
        original_body = next(o for o in Model.history(moved) if o.ComponentRole == "Result")
        independent = Model.make_independent(self.link)
        self.assertEqual(independent.Document, self.doc)
        self.assertNotEqual(independent.ObjectId, moved.ObjectId)
        self.assertEqual(Model.children(independent)[0].LinkedObject, Model.children(moved)[0].LinkedObject)
        independent_body = next(o for o in Model.history(independent) if o.ComponentRole == "Result")
        independent_body.Producer.Length = 8
        self.doc.recompute()
        self.assertAlmostEqual(independent_body.Shape.Volume, 96)
        self.assertAlmostEqual(original_body.Shape.Volume, 24)
        Model.validate(self.doc)

    def testNativeCreationJoinsHistoryInTheSameUndoStep(self):
        self.doc.openTransaction("Native box command")
        box = self.doc.addObject("Part::Box", "NativeBox")
        self.child.addObject(box)
        box.Length, box.Width, box.Height = 2, 3, 4
        self.doc.recompute()
        self.doc.commitTransaction()
        result = next(o for o in self.child.Group if getattr(o, "ComponentRole", "") == "Result")
        self.assertEqual(result.Producer, box)
        self.assertEqual(len(Model.history(self.child)), 2)
        identity = result.ObjectId
        self.assertAlmostEqual(result.Shape.Volume, 24)
        self.doc.undo()
        self.doc.recompute()
        self.assertEqual(Model.history(self.child), [])
        self.assertEqual(len(self.child.Group), 0)
        self.doc.redo()
        self.doc.recompute()
        restored = next(o for o in self.child.Group if getattr(o, "ComponentRole", "") == "Result")
        self.assertEqual(restored.ObjectId, identity)
        self.assertAlmostEqual(restored.Shape.Volume, 24)

    def testMissingExternalComponentCanBeRepairedByIdentity(self):
        external = Model.new_document("RepairSource")
        definition = Model.metadata(external).RootComponent
        body = external.addObject("Part::Feature", "RepairBody")
        body.Shape = Part.makeBox(2, 3, 4)
        Model.register_object(definition, body, result=True)
        external.recompute()
        source_path = self.output / "RepairSource.cadprt"
        external.saveAs(str(source_path))
        parent_path = self.output / "RepairParent.cadprt"
        self.doc.saveAs(str(parent_path))
        link = Model.add_component(self.root, definition)
        reference = Model.add_reference(self.root, link, body)
        reference_id = reference.ObjectId
        self.doc.save()

        original = parent_path.read_bytes()
        for doc in list(App.listDocuments().values()):
            App.closeDocument(doc.Name)
        relocated = self.output / "RelocatedSource.cadprt"
        source_path.rename(relocated)
        self.doc = CadDocument.open(parent_path)
        self.root = Model.metadata(self.doc).RootComponent
        reference = next(o for o in self.doc.Objects if getattr(o, "ObjectId", "") == reference_id)
        self.assertIsNone(reference.SourceObject)
        self.assertTrue(reference.Shape.isNull())
        with self.assertRaises(Exception):
            self.doc.save()
        self.assertEqual(parent_path.read_bytes(), original)
        Model.repair_component(self.root, reference.SourceOccurrence, relocated)
        self.assertEqual(reference.ObjectId, reference_id)
        self.assertAlmostEqual(Model.current_shape(reference).Volume, 24)
        self.doc.save()


    def testRejectedSaveAsPreservesLocationAndLabel(self):
        self.box()
        original = self.output / "BeforeFailedSave.cadprt"
        self.doc.saveAs(str(original))
        previous_label = self.doc.Label
        before = original.read_bytes()
        Model.metadata(self.doc).SchemaVersion = 999
        with self.assertRaises(Exception):
            self.doc.saveAs(str(self.output / "RejectedSave.cadprt"))
        self.assertEqual(Path(self.doc.FileName), original)
        self.assertEqual(self.doc.Label, previous_label)
        self.assertEqual(original.read_bytes(), before)
        self.assertFalse((self.output / "RejectedSave.cadprt").exists())
        Model.metadata(self.doc).SchemaVersion = Model.SCHEMA

    def testSharedSketchTwoResultsAndLaterBooleanHistory(self):
        sketch = self.doc.addObject("Sketcher::SketchObject", "SharedSketch")
        Model.register_object(self.child, sketch)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        sketch.addConstraint(Sketcher.Constraint("Radius", 0, 2))
        self.doc.recompute()
        first_op, first = Model.extrude(self.child, sketch, 3)
        second_op, second = Model.extrude(self.child, sketch, 5)
        with Model.transaction(self.doc, "Union results"):
            union = self.doc.addObject("Part::MultiFuse", "Union")
            Model.register_object(self.child, union, "Operation")
            self.assertTrue(first.Visibility, "First result visible before union inputs assigned")
            union.Shapes = [first, second]
            self.doc.recompute()
            result = Model.publish_result(self.child, union)
        self.assertEqual(Model.finished_results(self.child), [result])
        self.assertEqual(len([o for o in self.doc.Objects if o.isDerivedFrom("Sketcher::SketchObject")]), 1)
        self.assertFalse(any(o.TypeId == "PartDesign::Body" for o in self.doc.Objects))
        sketch.setDatum(0, App.Units.Quantity("3 mm"))
        self.doc.recompute()
        self.assertAlmostEqual(result.Shape.Volume, math.pi * 9 * 5)
        Model.set_suppressed(union, True)
        self.assertEqual(set(Model.finished_results(self.child)), {first, second})
        self.assertTrue(first.Visibility, union.PreviousVisibility)
        self.assertTrue(second.Visibility)
        self.assertTrue(result.Shape.isNull())
        Model.set_suppressed(union, False)
        self.assertFalse(first.Visibility)
        self.assertAlmostEqual(result.Shape.Volume, math.pi * 9 * 5)

    def testDraftAndCAMConsumeCurrentPublishedGeometryAfterReopen(self):
        from draftmake.make_clone import make_clone
        from Path.Main import Job
        box, body = self.box(self.root)
        clone = make_clone(body, forcedraft=True)
        clone.Label = "Consumer clone"
        job = Job.Create("ComponentJob", [body])
        self.doc.recompute()
        cam_model = job.Model.Group[0]
        self.assertAlmostEqual(clone.Shape.Volume, 24)
        self.assertAlmostEqual(cam_model.Shape.Volume, 24)
        Model.set_suppressed(box, True)
        self.assertTrue(clone.Shape.isNull())
        self.assertTrue(cam_model.Shape.isNull())
        Model.set_suppressed(box, False)
        path = self.output / "ConsumerResults.cadprt"
        self.doc.saveAs(str(path))
        names = box.Name, clone.Name, job.Name
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(path)
        box, clone, job = [self.doc.getObject(name) for name in names]
        box.Length = 8
        self.doc.recompute()
        self.assertAlmostEqual(clone.Shape.Volume, 96)
        self.assertAlmostEqual(job.Model.Group[0].Shape.Volume, 96)

    def testDrawingConsumesPublishedResultAfterReopen(self):
        from PySide import QtCore
        import time
        import TechDraw
        def wait_for(predicate):
            deadline = time.monotonic() + 8
            while time.monotonic() < deadline:
                QtCore.QCoreApplication.processEvents()
                if predicate():
                    return
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(25, loop.quit)
                loop.exec_()
            self.fail("TechDraw did not update its component result in eight seconds")
        sketch = self.doc.addObject("Sketcher::SketchObject", "DrawingProfile")
        Model.register_object(self.root, sketch)
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2))
        sketch.addConstraint(Sketcher.Constraint("Radius", 0, 2))
        self.doc.recompute()
        operation, body = Model.extrude(self.root, sketch, 3)
        page = self.doc.addObject("TechDraw::DrawPage", "Page")
        template = self.doc.addObject("TechDraw::DrawSVGTemplate", "Template")
        template.Template = App.getResourceDir() + "Mod/TechDraw/Templates/ISO/A3_Landscape_blank.svg"
        page.Template = template
        view = self.doc.addObject("TechDraw::DrawViewPart", "ResultView")
        view.Source = [body]
        view.Direction = App.Vector(0, 0, 1)
        page.addView(view)
        self.doc.recompute()
        wait_for(lambda: len(view.getVisibleEdges()) == 1)
        self.assertAlmostEqual(view.getVisibleEdges()[0].Curve.Radius, 2)
        path = self.output / "DrawingResults.cadprt"
        self.doc.saveAs(str(path))
        App.closeDocument(self.doc.Name)
        self.doc = CadDocument.open(path)
        view = self.doc.ResultView
        wait_for(lambda: len(view.getVisibleEdges()) == 1)
        self.doc.DrawingProfile.setDatum(0, App.Units.Quantity("3 mm"))
        self.doc.recompute()
        view = self.doc.ResultView
        wait_for(lambda: len(view.getVisibleEdges()) == 1 and abs(view.getVisibleEdges()[0].Curve.Radius - 3) < 1e-6)
        self.assertNotIn("Invalid", view.State)

    def testNavigatorRootIsComponentAndHistoryIsSeparate(self):
        import FreeCADGui as Gui
        from PySide import QtCore, QtWidgets
        path = Path(__file__).resolve().parents[1] / "src/Gui/ComponentNavigator.py"
        spec = importlib.util.spec_from_file_location("ComponentNavigatorTest", path)
        navigator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(navigator)
        self.box()
        panel = navigator.show(self.doc)
        try:
            self.assertEqual(panel.tabs.tabText(0), "Models")
            self.assertEqual(panel.tabs.tabText(1), "Assembly Structure")
            self.assertEqual(panel.tabs.tabText(2), "Model History")
            self.assertEqual(panel.structure.topLevelItemCount(), 1)
            root = panel.structure.topLevelItem(0)
            self.assertEqual(root.text(0), self.child.Label)
            self.assertFalse(root.icon(0).isNull())
            self.assertEqual(root.childCount(), 0)
            result = next(o for o in self.child.Group if getattr(o, "ComponentRole", "") == "Result")
            self.assertEqual(list(self.link.ViewObject.LinkView.SubNames), [Model.display_object(result).Name + "."])
            Model.set_representation(self.root, [self.link.ObjectId], "Hidden")
            panel.refresh()
            self.assertIsNone(self.link.ViewObject.LinkView.LinkedView)
            self.assertTrue(result.Visibility)
            Model.set_representation(self.root, [self.link.ObjectId])
            panel.refresh()
            root = panel.structure.topLevelItem(0)
            panel.activate_item(root)
            panel.refresh()
            self.assertEqual(panel.active_key, navigator.object_key(self.child))
            self.assertEqual(panel.history.topLevelItemCount(), 2)  # Origin plus public operation.
            panel.tabs.setCurrentWidget(panel.structure)
            panel.resize(560, 700)
            Gui.updateGui()
            panel.grab().save(str(self.output / "component-structure.png"))
            panel.tabs.setCurrentWidget(panel.history)
            Gui.updateGui()
            panel.grab().save(str(self.output / "model-history.png"))
            count = len(self.doc.Objects)
            isolated = panel.open_component_tab(navigator.object_key(self.child))
            panel.refresh()
            self.assertEqual(len(self.doc.Objects), count)
            self.assertEqual(isolated.getActiveObject("part"), self.child)
            self.assertEqual(panel.structure.topLevelItemCount(), 0)
            self.assertEqual(list(panel.component_views[0]["snapshot"].SubNames), [Model.display_object(result).Name + "."])
            Gui.updateGui()
            from pivy import coin
            bounds = coin.SoGetBoundingBoxAction(coin.SbViewportRegion(640, 480))
            bounds.apply(panel.component_views[0]["snapshot"].RootNode)
            self.assertFalse(bounds.getBoundingBox().isEmpty(), "Isolated component scene must contain geometry")
            isolated.saveImage(str(self.output / "isolated-component.png"), 640, 480, "Current")
        finally:
            App.removeDocumentObserver(panel)
            panel.deleteLater()
            QtWidgets.QApplication.processEvents()
