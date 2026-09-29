# SPDX-License-Identifier: LGPL-2.1-or-later
"""Opt-in upstream fixture probe; set FREECAD_PLUS_27950_FIXTURE to its FCStd.

Read only saved BReps, not restored Python proxies or old toolpaths. Never save
or modify the supplied document. Run separately from generated regressions.
"""
import os
import unittest
import zipfile
import FreeCAD as App
import Part
from CAMTests.PathTestUtils import PathTestWithAssets
from Path.Main import Job
from Path.Op import PlanarSurface


class TestIssue27950Fixture(PathTestWithAssets):
    def testSavedExternalMirrorFaceInReplacementOperation(self):
        fixture = os.environ["FREECAD_PLUS_27950_FIXTURE"]
        doc = App.newDocument("Issue27950SavedGeometry")
        try:
            with zipfile.ZipFile(fixture) as archive:
                shapes = []
                for name in ("Clone", "Part__Mirroring"):
                    obj = doc.addObject("Part::Feature", name)
                    shape = Part.Shape()
                    shape.importBrepFromString(archive.read(name + ".Shape.brp").decode())
                    obj.Shape = shape
                    self.assertTrue(shape.isValid())
                    shapes.append(obj)
            job = Job.Create("Job", [shapes[0]])
            job.Tools.Group[0].Tool = self.assets.get("toolbit://5mm_Endmill").attach_to_doc(doc=doc)
            doc.recompute()
            op = PlanarSurface.Create("ModernSurface", parentJob=job)
            op.Base = [(job.Model.Group[0], ["Face3"]), (shapes[1], ["Face3"])]
            op.AvoidLastX_Faces = 1
            op.CutPattern = "ZigZag"
            op.SampleInterval = 1
            op.StepOver = 99
            self.assertNotIn(shapes[1], job.Model.Group)
            op.Proxy.execute(op)
            self.assertTrue(op.Path.Commands, "Replacement produced no path")
            self.assertTrue(any(c.Name == "G1" for c in op.Path.Commands))
        finally:
            App.closeDocument(doc.Name)
