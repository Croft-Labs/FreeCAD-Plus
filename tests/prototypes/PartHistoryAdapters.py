# SPDX-License-Identifier: LGPL-2.1-or-later
"""Test-only adapters for roadmap 7.1.3. Not installed or a supported file schema.

Two explicit output roles exercise semantic identity without pretending to solve
general split/merge correspondence. Geometry is limited to one planar closed wire
in the part's local frame. Native transactions/persistence own all stored state.
"""
import uuid
import FreeCAD as App
import Part
from BasicShapes.ShapeReferences import validate_link


class PersistentProxy:
    def dumps(self):
        return None

    def loads(self, state):
        pass


class TwoResults(PersistentProxy):
    def __init__(self, obj, profile):
        obj.addProperty("App::PropertyLink", "Profile", "Prototype")
        obj.addProperty("App::PropertyLength", "Length", "Prototype")
        obj.addProperty("App::PropertyBool", "RightEnabled", "Prototype")
        obj.addProperty("Part::PropertyPartShape", "LeftOutput", "Prototype")
        obj.addProperty("Part::PropertyPartShape", "RightOutput", "Prototype")
        obj.addProperty("App::PropertyString", "FeatureIdentity", "Prototype")
        obj.addProperty("App::PropertyString", "ResultStatus", "Prototype")
        obj.Profile = profile
        obj.Length = 3
        obj.RightEnabled = True
        obj.FeatureIdentity = str(uuid.uuid4())
        obj.Proxy = self

    def execute(self, obj):
        obj.LeftOutput = Part.Shape()
        obj.RightOutput = Part.Shape()
        obj.Shape = Part.Shape()
        obj.ResultStatus = "Failed"
        validate_link(obj, obj.Profile)
        if obj.Length.Value <= 0 or len(obj.Profile.Shape.Wires) != 1:
            raise ValueError("Prototype requires positive length and one closed profile")
        left = Part.Face(obj.Profile.Shape.Wires[0]).extrude(App.Vector(0, 0, obj.Length.Value))
        right = left.copy()
        right.translate(App.Vector(10, 0, 0))
        obj.LeftOutput = left
        if obj.RightEnabled:
            obj.RightOutput = right
        obj.Shape = Part.makeCompound([left, right] if obj.RightEnabled else [left])
        obj.ResultStatus = "Ready"


class BodyResult(PersistentProxy):
    def __init__(self, obj, producer, role):
        if role not in ("Left", "Right"):
            raise ValueError("Unknown prototype output role")
        obj.addProperty("App::PropertyLink", "Producer", "Prototype")
        obj.addProperty("App::PropertyString", "OutputRole", "Prototype")
        obj.addProperty("App::PropertyString", "BodyIdentity", "Prototype")
        obj.addProperty("App::PropertyString", "ResultStatus", "Prototype")
        obj.Producer = producer
        obj.OutputRole = role
        obj.BodyIdentity = str(uuid.uuid4())
        obj.setEditorMode("BodyIdentity", 1)
        obj.setEditorMode("OutputRole", 1)
        obj.Proxy = self

    def execute(self, obj):
        obj.Shape = Part.Shape()
        obj.ResultStatus = "Unavailable"
        validate_link(obj, obj.Producer)
        if obj.Producer.ResultStatus != "Ready":
            return
        if obj.OutputRole not in ("Left", "Right"):
            raise ValueError("Unknown output role; explicit repair required")
        shape = getattr(obj.Producer, obj.OutputRole + "Output")
        if shape.isNull():
            return
        # Part::Feature enforces the object's Placement during recompute. Keep it
        # aligned with the published output instead of resetting that location.
        obj.Placement = shape.Placement
        obj.Shape = shape.copy()
        obj.ResultStatus = "Ready"


class ResultUnion(PersistentProxy):
    def __init__(self, obj, sources):
        obj.addProperty("App::PropertyLinkList", "Sources", "Prototype")
        obj.addProperty("App::PropertyString", "ResultStatus", "Prototype")
        obj.Sources = sources
        obj.Proxy = self

    def execute(self, obj):
        obj.Shape = Part.Shape()
        obj.ResultStatus = "Failed"
        for source in obj.Sources:
            validate_link(obj, source)
            if source.ResultStatus != "Ready" or source.Shape.isNull():
                raise ValueError("Required body result is unavailable")
        if len(obj.Sources) < 2:
            raise ValueError("Prototype union requires at least two explicit results")
        obj.Shape = obj.Sources[0].Shape.fuse([source.Shape for source in obj.Sources[1:]])
        obj.ResultStatus = "Ready"


def part_results(part, profile):
    doc = part.Document
    feature = doc.addObject("Part::FeaturePython", "TwoResults")
    part.addObject(feature)
    TwoResults(feature, profile)
    results = []
    for role in ("Left", "Right"):
        result = doc.addObject("Part::FeaturePython", role + "Result")
        part.addObject(result)
        BodyResult(result, feature, role)
        results.append(result)
    consumer = doc.addObject("Part::FeaturePython", "ResultUnion")
    part.addObject(consumer)
    ResultUnion(consumer, results)
    return feature, results, consumer


def body_adapter(part, profile, name, length, reverse=False):
    body = part.Document.addObject("PartDesign::Body", name)
    part.addObject(body)
    binder = body.newObject("PartDesign::SubShapeBinder", name + "Profile")
    binder.Support = [(profile, ("",))]
    part.Document.recompute()
    pad = body.newObject("PartDesign::Pad", name + "Pad")
    pad.Profile = binder
    pad.Length = length
    pad.Reversed = reverse
    return body, binder, pad
