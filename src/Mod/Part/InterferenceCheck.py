# SPDX-License-Identifier: LGPL-2.1-or-later
"""Read-only pair inspection of explicitly selected, current native solids."""
import itertools
import math

import FreeCAD as App
from BasicShapes.ShapeReferences import linked_shape, require_current


MAX_INPUTS = 12


class Reference:
    """Keep selection paths and identities; never silently retarget after deletion."""
    def __init__(self, root, sub=""):
        if sub and not sub.endswith("."):
            raise ValueError("Select whole solid objects or occurrences, not faces or edges.")
        self.document = root.Document.Name
        self.root = root.Name
        self.sub = sub
        path = root.getSubObjectList(sub) if sub else [root]
        if not path:
            raise ValueError("The selected object path cannot be resolved.")
        self.identities = [(obj.Name, obj.ID) for obj in path]
        self.label = "{} [{}{}]".format(path[-1].Label, root.Name, "." + sub if sub else "")
        self.key = (self.document, self.root, self.sub)

    def resolve(self):
        doc = App.getDocument(self.document)
        root = doc.getObject(self.root)
        if root is None:
            raise ValueError("Selected object was deleted. Replace the input selection.")
        path = root.getSubObjectList(self.sub) if self.sub else [root]
        if [(obj.Name, obj.ID) for obj in path] != self.identities:
            raise ValueError("Selected identity changed. Replace the input selection.")
        return root, path

    def shape(self):
        root, path = self.resolve()
        if any(obj.TypeId != "App::Part" for obj in path[:-1]):
            raise ValueError("Paths through another occurrence are not supported by this pilot.")
        obj = path[-1]
        target = obj
        if obj.TypeId == "App::Link":
            if obj.ElementCount:
                raise ValueError("Link arrays require individual supported occurrences.")
            target = obj.LinkedObject
        if (target is None or not hasattr(target, "Document")
                or target.Document != root.Document or not target.isDerivedFrom("Part::Feature")):
            raise ValueError("Requires a loaded same-document solid or direct shape/Body link.")
        for node in path[:-1]:
            if "Invalid" in node.State or "Touched" in node.State:
                raise ValueError("Container placement is not current. Recompute or repair it first.")
        require_current(obj)
        require_current(target)
        # Resolve from the selected structural root so native Link placement and
        # enclosing Part placement are both retained by the shared shape service.
        shape = linked_shape((root, [self.sub] if self.sub else []))
        for candidate in (target.Shape, shape):
            pending = [candidate]
            while pending:
                member = pending.pop()
                if member.ShapeType == "Compound":
                    pending.extend(member.childShapes())
                elif member.ShapeType not in ("Solid", "CompSolid"):
                    raise ValueError("Input contains sheet, wire or other non-solid geometry.")
            if candidate.isNull() or not candidate.Solids or not candidate.isValid():
                raise ValueError("Input is not a valid solid result.")
        return shape


def inspect(references, clearance=1.0, tolerance=0.000001):
    """Return every pair, including unresolved inputs; no recompute or model edits."""
    if not 2 <= len(references) <= MAX_INPUTS:
        raise ValueError("Choose 2 to {} included inputs for this inspection.".format(MAX_INPUTS))
    if (not math.isfinite(clearance) or not math.isfinite(tolerance)
            or tolerance <= 0 or clearance < tolerance):
        raise ValueError("Required clearance must be at least the positive contact tolerance.")
    if len({ref.key for ref in references}) != len(references):
        raise ValueError("The same input is listed more than once.")
    if len({ref.document for ref in references}) != 1:
        raise ValueError("Choose inputs from one document.")
    doc = App.getDocument(references[0].document)
    if doc.HasPendingTransaction:
        raise ValueError("Finish the pending edit transaction before checking.")
    shapes, errors = {}, {}
    for index, ref in enumerate(references):
        try:
            shapes[index] = ref.shape()
        except Exception as error:
            errors[index] = str(error)
    rows = []
    for a, b in itertools.combinations(range(len(references)), 2):
        row = {"a": a, "b": b, "status": "Unresolved", "distance": None,
               "volume": None, "detail": ""}
        try:
            if a in errors or b in errors:
                raise ValueError("; ".join(references[i].label + ": " + errors[i]
                                           for i in (a, b) if i in errors))
            first, second = shapes[a], shapes[b]
            common = first.common(second)
            if not common.isNull() and not common.isValid():
                raise ValueError("Kernel returned an invalid intersection.")
            volume = sum(solid.Volume for solid in common.Solids)
            distance = first.distToShape(second)[0]
            if not math.isfinite(volume) or not math.isfinite(distance) or distance < 0 or volume < 0:
                raise ValueError("Kernel returned an invalid distance or volume.")
            row.update(distance=distance, volume=volume)
            if volume > 0:
                row.update(status="Overlap", detail="Positive common solid volume.")
            elif distance <= tolerance:
                row.update(status="Contact / within tolerance",
                           detail="No common solid volume; separation is within contact tolerance.")
            elif distance < clearance:
                row.update(status="Below clearance", detail="Separation is below the required clearance.")
            else:
                row.update(status="Clear", detail="Separation meets the required clearance.")
        except Exception as error:
            row["detail"] = str(error)
        rows.append(row)
    return rows
