# SPDX-License-Identifier: LGPL-2.1-or-later
"""Test-only creation proposal and committed-intent proof, not a production API.

Restricted to single solids directly owned by one App::Part. No occurrences,
sheets, multi-target execution, general lineage or tolerance hysteresis is claimed.
"""
import FreeCAD as App
import Part
from BasicShapes.ShapeReferences import validate_link
from PartHistoryAdapters import PersistentProxy


def solid(shape):
    return not shape.isNull() and shape.isValid() and len(shape.Solids) == 1


def eligible(part, obj):
    return (obj is not None and obj.Document == part.Document
            and obj.getParentGeoFeatureGroup() == part
            and obj.isDerivedFrom("Part::Feature")
            and not obj.isDerivedFrom("App::Link"))


def propose(part, tool, candidates, tolerance=1e-7):
    """Return an uncommitted mode, concrete candidates and explanation.

    Tolerance is an explicit fixture-scale distance in mm; production must define
    scale-aware contact policy. Contact is deliberately sent for review here.
    """
    if not solid(tool) or tolerance <= 0:
        return "Review", [], "A valid single solid and positive tolerance are required"
    hits = []
    for obj in dict.fromkeys(candidates):
        if not eligible(part, obj):
            continue
        shape = obj.Shape
        if not solid(shape):
            return "Review", [obj], "Candidate geometry is unavailable or unsupported"
        try:
            overlap = tool.common(shape).Volume
            if overlap <= tolerance ** 3:
                if tool.distToShape(shape)[0] <= tolerance:
                    return "Review", [obj], "Contact needs deliberate operation selection"
                continue
            hits.append(obj)
        except Part.OCCError:
            return "Review", [obj], "Intersection could not be evaluated"
    if not hits:
        return "NewBody", [], "No eligible intersecting body"
    if len(hits) > 1:
        return "ChooseTargets", hits, "Multiple eligible bodies intersect"
    try:
        if not solid(tool.fuse(hits[0].Shape)):
            return "Review", hits, "Union does not produce one valid solid"
    except Part.OCCError:
        return "Review", hits, "Union could not be evaluated"
    return "Unite", hits, "One eligible body forms a valid union"


class CommittedOperation(PersistentProxy):
    def __init__(self, obj, tool, operation, targets):
        obj.addProperty("App::PropertyLink", "Tool", "Prototype")
        obj.addProperty("App::PropertyLinkList", "Targets", "Prototype")
        obj.addProperty("App::PropertyEnumeration", "Operation", "Prototype")
        obj.Operation = ["NewBody", "Unite", "Subtract", "Intersect"]
        obj.addProperty("App::PropertyString", "ResultStatus", "Prototype")
        obj.Tool, obj.Targets, obj.Operation = tool, targets, operation
        obj.Proxy = self

    def execute(self, obj):
        # Evaluation consumes saved intent only; it never calls propose().
        obj.Shape = Part.Shape()
        obj.ResultStatus = "Failed"
        part = obj.getParentGeoFeatureGroup()
        if not part or not eligible(part, obj.Tool):
            raise ValueError("Tool must be a direct solid in the edited part")
        validate_link(obj, obj.Tool)
        if not solid(obj.Tool.Shape):
            raise ValueError("Tool is unavailable")
        shape = obj.Tool.Shape.copy()
        if obj.Operation == "NewBody":
            if obj.Targets:
                raise ValueError("New Body has no Boolean targets")
        else:
            if len(obj.Targets) != 1 or not eligible(part, obj.Targets[0]):
                raise ValueError("Select one explicit target in this part")
            target = obj.Targets[0]
            validate_link(obj, target)
            if not solid(target.Shape) or shape.common(target.Shape).Volume <= 1e-21:
                raise ValueError("Saved target no longer intersects; repair the feature")
            if obj.Operation == "Unite":
                shape = target.Shape.fuse(shape)
            elif obj.Operation == "Subtract":
                shape = target.Shape.cut(shape)
            else:
                shape = target.Shape.common(shape)
        if not solid(shape):
            raise ValueError("Operation does not produce one valid solid")
        obj.Placement = shape.Placement
        obj.Shape = shape
        obj.ResultStatus = "Ready"


def commit(part, tool, operation, targets):
    obj = part.Document.addObject("Part::FeaturePython", "CommittedOperation")
    part.addObject(obj)
    CommittedOperation(obj, tool, operation, targets)
    return obj
