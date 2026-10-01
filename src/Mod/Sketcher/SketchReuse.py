# SPDX-License-Identifier: LGPL-2.1-or-later
"""Independent whole-sketch reuse through native document copying and placement."""
import hashlib
import math
import FreeCAD as App
from BasicShapes.ShapeReferences import require_current
from freecad.gui.DependencyInspector import identity


def tr(text):
    return App.Qt.translate("SketchReuse", text)


def review(sketch):
    if sketch.TypeId != "Sketcher::SketchObject" or sketch.getParentGeoFeatureGroup() is not None:
        raise ValueError(tr("Select a root sketch. Body, Part and occurrence scopes are not supported by this copy tool yet."))
    if (sketch.MapMode != "Deactivated" or sketch.AttachmentSupport or sketch.ExternalGeometry
            or sketch.ExpressionEngine or sketch.OutList):
        raise ValueError(tr("This independent copy requires a free sketch without support, external geometry, expressions or other linked inputs. These references will not be silently dropped."))
    require_current(sketch)
    if not 0 < sketch.GeometryCount <= 500 or sketch.Shape.isNull():
        raise ValueError(tr("Choose a sketch with visible geometry and at most 500 geometry elements."))
    if sketch.ConflictingConstraints or sketch.RedundantConstraints or sketch.MalformedConstraints:
        raise ValueError(tr("Repair the sketch constraints before copying."))
    return {"key": identity(sketch), "content": hashlib.sha256(sketch.Content.encode("utf-8")).hexdigest(),
            "geometry": sketch.GeometryCount, "constraints": sketch.ConstraintCount,
            "dof": sketch.DoF}


def candidate(sketch, expected, offset, angle):
    if review(sketch) != expected:
        raise ValueError(tr("The sketch changed. Review again before copying."))
    if len(offset) != 3 or not all(math.isfinite(value) for value in (*offset, angle)):
        raise ValueError(tr("Enter finite offsets and angle."))
    placement = sketch.Placement.multiply(App.Placement(App.Vector(*offset), App.Rotation(App.Vector(0, 0, 1), angle)))
    shape = sketch.Shape.copy()
    delta = placement.multiply(sketch.Placement.inverse())
    shape.Placement = delta.multiply(shape.Placement)
    return placement, shape


def constraint_signature(sketch):
    fields = ("Type", "First", "FirstPos", "Second", "SecondPos", "Third", "ThirdPos",
              "Value", "Name", "Driving", "IsActive", "InVirtualSpace")
    return [tuple(getattr(constraint, field) for field in fields) for constraint in sketch.Constraints]


def create_copy(sketch, expected, label, offset, angle):
    import FreeCADGui as Gui
    doc = sketch.Document
    if (App.ActiveDocument != doc or Gui.Control.activeDialog() or doc.HasPendingTransaction
            or App.getActiveTransaction()):
        raise ValueError(tr("Activate this document and finish the current task or edit transaction first."))
    if not label.strip() or "\x00" in label:
        raise ValueError(tr("Enter a name for the independent sketch."))
    placement, _shape = candidate(sketch, expected, offset, angle)
    signatures = constraint_signature(sketch)
    construction = [sketch.getConstruction(index) for index in range(sketch.GeometryCount)]
    doc.openTransaction(tr("Copy reusable sketch"))
    try:
        result = doc.copyObject(sketch, False)
        result.Label = label.strip()
        result.Placement = placement
        result.Visibility = True
        doc.recompute()
        review(result)
        if (result.GeometryCount != sketch.GeometryCount or constraint_signature(result) != signatures
                or [result.getConstruction(index) for index in range(result.GeometryCount)] != construction
                or result.DoF != sketch.DoF):
            raise ValueError(tr("The copied sketch did not preserve its internal constraints and construction geometry."))
        doc.commitTransaction()
        return result
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise
