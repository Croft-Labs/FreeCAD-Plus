# SPDX-License-Identifier: LGPL-2.1-or-later
"""Opt-in #26300 saved-geometry probe, run with an external process deadline.

Set FREECAD_PLUS_26300_FIXTURE to the downloaded FCStd. No external proxies or
legacy operations are restored; only saved geometry and explicit settings load.
"""
import faulthandler
import hashlib
import json
import math
import os
from pathlib import Path
import time
import xml.etree.ElementTree as ET
import zipfile
from unittest.mock import patch
import FreeCAD as App
import Part
from CAMTests.PathTestUtils import PathTestWithAssets
from Path.Main import Job
from Path.Op import PlanarSurface
from Path.Base.Generator import surface_common


class TestIssue26300Fixture(PathTestWithAssets):
    def testFreeformSelectedFacesGenerateWithoutHanging(self):
        fixture = Path(os.environ["FREECAD_PLUS_26300_FIXTURE"])
        doc = App.newDocument("Issue26300SavedGeometry")
        try:
            with zipfile.ZipFile(fixture) as archive:
                root = ET.fromstring(archive.read("Document.xml"))
                objects = {o.get("name"): o for o in root.find("ObjectData")}
                shape = Part.Shape()
                shape.importBrepFromString(archive.read("Clone.Shape.brp").decode())
                placement = objects["Clone"].find("Properties/Property[@name='Placement']/PropertyPlacement")
                shape.Placement = App.Placement(
                    App.Vector(*(float(placement.get(k)) for k in ("Px", "Py", "Pz"))),
                    App.Rotation(*(float(placement.get(k)) for k in ("Q0", "Q1", "Q2", "Q3"))))
                settings = objects["Surface"].find("Properties")
                links = settings.find("Property[@name='Base']/LinkSubList")
                self.assertTrue(all(link.get("obj") == "Clone" for link in links))
                faces = [link.get("sub") for link in links]
                self.assertEqual(len(faces), 9)
                def number(name):
                    return float(settings.find(f"Property[@name='{name}']/Float").get("value"))
                parameters = {name: number(name) for name in
                              ("SampleInterval", "StepOver", "StartDepth", "FinalDepth", "StepDown")}
            self.assertTrue(shape.isValid())
            model = doc.addObject("Part::Feature", "SavedModel")
            model.Shape = shape
            job = Job.Create("Job", [model])
            job.Tools.Group[0].Tool = self.assets.get("toolbit://5mm_Endmill").attach_to_doc(doc=doc)
            doc.recompute()
            op = PlanarSurface.Create("ModernSurface", parentJob=job)
            op.Base = [(job.Model.Group[0], faces)]
            op.CutPattern = "Line"
            # Modern selected-face masking replaces legacy BoundaryEnforcement.
            for name, value in parameters.items():
                op.setExpression(name, None)
                setattr(op, name, value)
            started = time.monotonic()
            masks = []
            generate_mask = surface_common.generate_pattern_mask

            def capture_mask(*args, **kwargs):
                mask = generate_mask(*args, **kwargs)
                self.assertTrue(mask.isValid())
                self.assertGreater(mask.Area, 0, "Projection produced no filled machining region")
                masks.append(mask)
                return mask

            with (Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "freeform-stack.log").open("w") as trace:
                faulthandler.dump_traceback_later(20, repeat=True, file=trace)
                try:
                    with patch.object(surface_common, "generate_pattern_mask", side_effect=capture_mask):
                        op.Proxy.execute(op)
                finally:
                    faulthandler.cancel_dump_traceback_later()
            elapsed = time.monotonic() - started
            commands = op.Path.Commands
            cuts = [c for c in commands if c.Name == "G1"]
            self.assertTrue(cuts, "Replacement produced no cutting moves")
            self.assertTrue(all(math.isfinite(v) for c in commands for v in c.Parameters.values()))
            self.assertGreater(len({c.Parameters.get("Z") for c in cuts if "Z" in c.Parameters}), 2,
                               "Freeform path has no height variation")
            self.assertTrue(masks)
            position = App.Vector()
            checked = 0
            for command in commands:
                position = App.Vector(*(command.Parameters.get(axis, getattr(position, axis.lower()))
                                        for axis in "XYZ"))
                if command.Name == "G1" and ("X" in command.Parameters or "Y" in command.Parameters):
                    point = App.Vector(position.x, position.y, 0)
                    self.assertTrue(any(mask.isInside(point, 0.01, True) for mask in masks),
                                    f"Cutting endpoint outside selected-face mask: {point}")
                    checked += 1
            self.assertGreater(checked, 0)
            evidence = {"fixture_sha256": hashlib.sha256(fixture.read_bytes()).hexdigest(),
                        "faces": faces, "parameters": parameters, "seconds": elapsed,
                        "commands": len(commands), "cutting_commands": len(cuts),
                        "shape_faces": len(shape.Faces), "shape_volume": shape.Volume,
                        "mask_areas": [mask.Area for mask in masks],
                        "cutting_endpoints_checked": checked}
            (Path(os.environ["FREECAD_PLUS_VALIDATION_DIR"]) / "freeform-details.json").write_text(
                json.dumps(evidence, indent=2))
        finally:
            App.closeDocument(doc.Name)
