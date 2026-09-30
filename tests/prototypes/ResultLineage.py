# SPDX-License-Identifier: LGPL-2.1-or-later
"""Bounded planar split / primary merge proof. Not an installed schema/API."""
import uuid
import FreeCAD as App
import Part
from BasicShapes.ShapeReferences import validate_link
from PartHistoryAdapters import PersistentProxy, BodyResult


class StatusProxy(PersistentProxy):
    def execute(self, obj):
        obj.ErrorMessage = ""
        try:
            self.evaluate(obj)
        except (ValueError, Part.OCCError) as error:
            # Expected invalid input must still complete native recompute so
            # dependent result adapters can clear their cached live geometry.
            obj.ErrorMessage = str(error)


class PlanarSplit(StatusProxy):
    def __init__(self, obj, source):
        obj.addProperty("App::PropertyLink", "Source", "Prototype")
        obj.addProperty("App::PropertyFloat", "CutX", "Prototype")
        obj.addProperty("App::PropertyString", "FeatureIdentity", "Prototype")
        obj.addProperty("App::PropertyString", "ParentIdentity", "Prototype")
        obj.addProperty("App::PropertyString", "ResultStatus", "Prototype")
        obj.addProperty("App::PropertyString", "ErrorMessage", "Prototype")
        for role in ("Left", "Right"):
            obj.addProperty("Part::PropertyPartShape", role + "Output", "Prototype")
        obj.Source = source
        obj.CutX = 5
        obj.FeatureIdentity = str(uuid.uuid4())
        obj.ParentIdentity = source.BodyIdentity
        obj.Proxy = self

    def evaluate(self, obj):
        obj.Shape = Part.Shape()
        obj.LeftOutput = Part.Shape()
        obj.RightOutput = Part.Shape()
        obj.ResultStatus = "Failed"
        validate_link(obj, obj.Source)
        if obj.Source.BodyIdentity != obj.ParentIdentity:
            raise ValueError("Source lineage changed; explicit repair required")
        if obj.Source.getParentGeoFeatureGroup() != obj.getParentGeoFeatureGroup():
            raise ValueError("Prototype requires source in the same part")
        shape = obj.Source.Shape
        if shape.isNull() or not shape.isValid() or len(shape.Solids) != 1:
            raise ValueError("Prototype requires one valid source solid")
        point = App.Vector(obj.CutX, 0, 0)
        boundary = Part.Face(Part.Plane(point, App.Vector(1, 0, 0)))
        outputs = []
        for sign in (-1, 1):
            side = shape.common(boundary.makeHalfSpace(point + App.Vector(sign, 0, 0)))
            if not side.Solids:
                outputs.append(Part.Shape())
            elif not side.isValid() or len(side.Solids) != 1:
                raise ValueError("Multiple solids in one semantic side; explicit repair required")
            else:
                outputs.append(side)
        obj.LeftOutput, obj.RightOutput = outputs
        obj.Shape = Part.makeCompound([s for s in outputs if not s.isNull()])
        obj.ResultStatus = "Ready"


class PrimaryMerge(StatusProxy):
    def __init__(self, obj, sources, primary):
        obj.addProperty("App::PropertyLinkList", "Sources", "Prototype")
        obj.addProperty("App::PropertyLink", "Primary", "Prototype")
        obj.addProperty("App::PropertyString", "BodyIdentity", "Prototype")
        obj.addProperty("App::PropertyStringList", "ParentIdentities", "Prototype")
        obj.addProperty("App::PropertyString", "ResultStatus", "Prototype")
        obj.addProperty("App::PropertyString", "ErrorMessage", "Prototype")
        obj.Sources, obj.Primary = sources, primary
        obj.BodyIdentity = primary.BodyIdentity if primary else str(uuid.uuid4())
        obj.Proxy = self

    def evaluate(self, obj):
        obj.Shape = Part.Shape()
        obj.ResultStatus = "Failed"
        if len(obj.Sources) < 2 or len(set(obj.Sources)) != len(obj.Sources):
            raise ValueError("Select distinct source results")
        if obj.Primary and (obj.Primary not in obj.Sources
                            or obj.Primary.BodyIdentity != obj.BodyIdentity):
            raise ValueError("Primary lineage changed; explicit repair required")
        for source in obj.Sources:
            validate_link(obj, source)
            if (source.getParentGeoFeatureGroup() != obj.getParentGeoFeatureGroup()
                    or source.ResultStatus != "Ready" or source.Shape.isNull()):
                raise ValueError("Required result is unavailable or outside this part")
        ids = [source.BodyIdentity for source in obj.Sources]
        if len(set(ids)) != len(ids):
            raise ValueError("Ambiguous source identities")
        shape = obj.Sources[0].Shape.fuse([s.Shape for s in obj.Sources[1:]]).removeSplitter()
        if not shape.isValid() or len(shape.Solids) != 1:
            raise ValueError("Merge requires one valid solid")
        obj.ParentIdentities = sorted(ids)
        obj.Placement = shape.Placement
        obj.Shape = shape
        obj.ResultStatus = "Ready"


def split(part, source):
    obj = part.Document.addObject("Part::FeaturePython", "PlanarSplit")
    part.addObject(obj)
    PlanarSplit(obj, source)
    results = []
    for role in ("Left", "Right"):
        result = part.Document.addObject("Part::FeaturePython", role + "Child")
        part.addObject(result)
        BodyResult(result, obj, role)
        result.addProperty("App::PropertyString", "ParentIdentity", "Prototype")
        result.ParentIdentity = source.BodyIdentity
        results.append(result)
    return obj, results


def merge(part, results, primary=None):
    obj = part.Document.addObject("Part::FeaturePython", "MergedResult")
    part.addObject(obj)
    PrimaryMerge(obj, results, primary)
    return obj
