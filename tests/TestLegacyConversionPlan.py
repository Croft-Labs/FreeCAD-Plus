# SPDX-License-Identifier: LGPL-2.1-or-later
"""Task-one native read-only inventory and geometry recovery planning."""
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest
import FreeCAD as App
import Part
import Sketcher

if os.environ.get("FREECAD_PLUS_PROFILE_SOURCE") == "1":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src/Mod/Part"))
    # Startup may already have imported the delivered persistence module.
    sys.modules.pop("CadDocument", None)
import CadDocument


class TestLegacyConversionPlan(unittest.TestCase):
    def setUp(self):
        import LegacyConversion
        source = Path(__file__).resolve().parents[1]
        identities = {}
        for module in (CadDocument, LegacyConversion):
            digest = hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
            self.assertEqual(digest, hashlib.sha256((source / "src/Mod/Part" / (module.__name__ + ".py")).read_bytes()).hexdigest())
            identities[module.__name__] = {"path": module.__file__, "sha256": digest}
        (Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "legacy-planner-runtime.json").write_text(json.dumps(identities, indent=2))
        self.doc = App.newDocument("LegacyPlan")
        self.doc.UndoMode = 1
        self.created = [self.doc.Name]

    def tearDown(self):
        for name in reversed(self.created):
            if name in App.listDocuments():
                App.closeDocument(name)

    def key(self, obj):
        return obj.Document.Name + ":" + obj.Name

    def test_nested_parts_shared_links_body_history_and_read_only(self):
        part = self.doc.addObject("App::Part", "Part")
        part.Placement.Base = App.Vector(5, 6, 7)
        body = self.doc.addObject("PartDesign::Body", "Body")
        part.addObject(body)
        sketch = body.newObject("Sketcher::SketchObject", "Sketch")
        sketch.addGeometry(Part.Circle(App.Vector(), App.Vector(0, 0, 1), 2), False)
        sketch.addConstraint(Sketcher.Constraint("Diameter", 0, 4))
        pad = body.newObject("PartDesign::Pad", "Pad")
        pad.Profile = sketch
        pad.Length = 8
        body.Tip = pad
        parent = self.doc.addObject("App::Part", "Assembly")
        link1 = self.doc.addObject("App::Link", "First")
        link2 = self.doc.addObject("App::Link", "Second")
        for link in (link1, link2):
            link.setLink(part)
            parent.addObject(link)
        link2.LinkPlacement.Base = App.Vector(30, 0, 0)
        self.doc.recompute()
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "LegacyPlan.FCStd"
        self.doc.saveAs(str(path))
        original = path.read_bytes()
        before = (self.doc.FileName, self.doc.UndoCount, self.doc.HasPendingTransaction,
                  [o.Name for o in self.doc.Objects], body.Group, body.Tip, sketch.ConstraintCount)
        plan = CadDocument.legacy_plan(self.doc)
        (path.parent / "inventory-plan.json").write_text(json.dumps(plan, indent=2))
        again = CadDocument.legacy_plan(self.doc)
        self.assertEqual(plan, again)
        self.assertEqual(before, (self.doc.FileName, self.doc.UndoCount, self.doc.HasPendingTransaction,
                         [o.Name for o in self.doc.Objects], body.Group, body.Tip, sketch.ConstraintCount))
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(plan["source_sha256"], hashlib.sha256(original).hexdigest())
        self.assertEqual({d["source"] for d in plan["definitions"]}, {self.key(part), self.key(parent)})
        for obj in (body, sketch, pad):
            self.assertEqual(plan["history_owner"][self.key(obj)], self.key(part))
        self.assertLess(plan["dependency_order"].index(self.key(sketch)), plan["dependency_order"].index(self.key(pad)))
        self.assertLess(plan["dependency_order"].index(self.key(pad)), plan["dependency_order"].index(self.key(body)))
        uses = [x for x in plan["occurrences"] if x["source"] in (self.key(link1), self.key(link2))]
        self.assertEqual(len(uses), 2)
        self.assertEqual(uses[0]["targets"], uses[1]["targets"])
        self.assertNotEqual(plan["objects"][self.key(link1)]["link_placement"], plan["objects"][self.key(link2)]["link_placement"])
        self.assertEqual(plan["objects"][self.key(body)]["fallback"]["kind"], "dumb_body")
        self.assertFalse(plan["blocked_objects"])
        self.assertFalse(plan["issues"], plan["issues"])
        json.dumps(plan, allow_nan=False)
        name = self.doc.Name
        original_shape = body.getPropertyByName("Shape").copy()
        App.closeDocument(name)
        self.doc = App.openDocument(str(path))
        self.created.append(self.doc.Name)
        reopened = CadDocument.legacy_plan(self.doc)
        restored = self.doc.Body.getPropertyByName("Shape")
        # BREP serialization bytes may change on reopen; prove geometry with
        # native bidirectional differences, not a byte-hash equality claim.
        self.assertAlmostEqual(original_shape.cut(restored).Volume, 0, places=9)
        self.assertAlmostEqual(restored.cut(original_shape).Volume, 0, places=9)
        self.assertEqual([o.Name for o in self.doc.Body.Group], ["Sketch", "Pad"])
        self.assertEqual(self.doc.Body.Tip.Name, "Pad")
        self.assertEqual(self.doc.Sketch.ConstraintCount, 1)

    def test_dumb_recovery_kinds_and_no_geometry(self):
        shapes = [Part.makeBox(1, 2, 3), Part.makePlane(2, 3),
                  Part.makeLine(App.Vector(), App.Vector(2, 0, 0)), Part.Vertex(App.Vector())]
        for index, shape in enumerate(shapes):
            obj = self.doc.addObject("Part::Feature", "Shape" + str(index))
            obj.Shape = shape
        empty = self.doc.addObject("Part::Feature", "Empty")
        self.doc.recompute()
        p = CadDocument.legacy_plan(self.doc)
        for index, kind in enumerate(["dumb_body", "dumb_sheet", "dumb_curve", "dumb_point"]):
            f = p["objects"][self.doc.Name + ":Shape" + str(index)]["fallback"]
            self.assertEqual((f["kind"], f["status"]), (kind, "available_cached"))
            self.assertFalse(f["preserves_parametrics"])
        self.assertEqual(p["objects"][self.key(empty)]["fallback"]["status"], "unavailable")

    def test_stale_geometry_is_not_certified_and_no_recompute(self):
        box = self.doc.addObject("Part::Box", "Box")
        self.doc.recompute()
        old_volume = box.getPropertyByName("Shape").Volume
        box.touch()
        p = CadDocument.legacy_plan(self.doc)
        self.assertEqual(box.getPropertyByName("Shape").Volume, old_volume)
        self.assertIn("Touched", box.State)
        self.assertEqual(p["objects"][self.key(box)]["fallback"]["status"], "cached_unverified")

    def test_expression_dependencies_and_cycles(self):
        a = self.doc.addObject("Part::Box", "SourceBox")
        b = self.doc.addObject("Part::Box", "DependentBox")
        b.setExpression("Length", "SourceBox.Length + 1 mm")
        self.doc.recompute()
        p = CadDocument.legacy_plan(self.doc)
        self.assertIn(self.key(a), p["dependencies"][self.key(b)])
        self.assertLess(p["dependency_order"].index(self.key(a)), p["dependency_order"].index(self.key(b)))
        a.addProperty("App::PropertyLink", "Cycle")
        b.addProperty("App::PropertyLink", "Cycle")
        a.Cycle, b.Cycle = b, a
        p = CadDocument.legacy_plan(self.doc)
        self.assertEqual(set(p["blocked_objects"]), {self.key(a), self.key(b)})
        self.assertTrue(p["issues"])

    def test_external_links_identified_without_converting_source(self):
        external = App.newDocument("ExternalLegacy")
        self.created.append(external.Name)
        box = external.addObject("Part::Box", "Box")
        external.recompute()
        path = Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "External.FCStd"
        external.saveAs(str(path))
        original = path.read_bytes()
        self.doc.saveAs(str(path.parent / "Parent.FCStd"))
        link = self.doc.addObject("App::Link", "ExternalUse")
        link.setLink(box)
        self.doc.recompute()
        p = CadDocument.legacy_plan(self.doc)
        self.assertIn(self.key(box), p["external_objects"])
        self.assertEqual(p["external_files"][self.key(box)], str(path))
        self.assertEqual(path.read_bytes(), original)
        self.assertFalse(any(hasattr(o, "ComponentRole") for o in external.Objects))

    def test_standalone_body_boundary_and_attached_sketch(self):
        body = self.doc.addObject("PartDesign::Body", "Body")
        plane = body.newObject("PartDesign::Plane", "Plane")
        plane.MapMode = "Deactivated"
        plane.Placement.Base = App.Vector(0, 0, 4)
        sketch = body.newObject("Sketcher::SketchObject", "Attached")
        sketch.AttachmentSupport = [(plane, ("",))]
        sketch.MapMode = "FlatFace"
        self.doc.recompute()
        p = CadDocument.legacy_plan(self.doc)
        self.assertEqual([d["source"] for d in p["definitions"]], [self.key(body)])
        self.assertEqual(p["history_owner"][self.key(sketch)], self.key(body))
        self.assertIn(self.key(plane), p["dependencies"][self.key(sketch)])
        self.assertEqual(p["objects"][self.key(sketch)]["links"]["AttachmentSupport"], [self.key(plane)])

    def test_unresolved_link_and_unsupported_payload_remain_present(self):
        link = self.doc.addObject("App::Link", "Missing")
        payload = self.doc.addObject("App::FeaturePython", "Unmapped")
        self.doc.recompute()
        p = CadDocument.legacy_plan(self.doc)
        self.assertIn(self.key(payload), p["objects"])
        self.assertEqual(p["objects"][self.key(payload)]["type"], payload.TypeId)
        self.assertTrue(any(x["object"] == self.key(link) for x in p["issues"]))
        self.assertEqual(len(self.doc.Objects), 2)

    def test_property_snapshot_failure_does_not_drop_valid_body(self):
        from unittest.mock import patch
        import LegacyConversion
        box = self.doc.addObject("Part::Box", "Box")
        self.doc.recompute()
        original = LegacyConversion.hashlib.sha256
        # Exercise a single failed property fingerprint, retaining the native
        # object and independently recoverable evaluated geometry.
        attempts = [0]
        def digest(data):
            attempts[0] += 1
            if attempts[0] == 1:
                raise ValueError("property fingerprint unavailable")
            return original(data)
        with patch.object(LegacyConversion.hashlib, "sha256", digest):
            p = CadDocument.legacy_plan(self.doc)
        self.assertTrue(any(x["stage"].startswith("property:") for x in p["issues"]))
        self.assertEqual(p["objects"][self.key(box)]["fallback"]["kind"], "dumb_body")
        self.assertEqual(self.doc.getObject("Box"), box)
