# SPDX-License-Identifier: LGPL-2.1-or-later
"""Planar sketch support changes using native attachment, transactions and placement.

Direct supports stay in the sketch's native container. Occurrence/cross-container
reference creation is deliberately outside this installed pilot.
"""
import FreeCAD as App
import Part


def reattach_planar(sketch, support, face_name, policy="preserve-local"):
    """Explicitly replace a sketch's support with a same-container planar face."""
    return _reattach_planar(sketch, support, face_name, policy)


def preview_planar(sketch, support, face_name, policy="preserve-local"):
    """Evaluate attachment placement in a disposable document, not the live model.

    Only planar placement is evaluated, not sketch constraints or downstream solids.
    Application observers can see the temporary document's lifecycle.
    """
    _validate(sketch, support, face_name, policy)
    active = App.ActiveDocument
    trial = App.newDocument("ReattachmentPreview", hidden=True, temp=True)
    try:
        trial_support = trial.addObject("Part::Feature", "Support")
        shape = support.Shape.copy()
        parent = support.getGlobalPlacement().multiply(support.Placement.inverse())
        shape.transformShape(parent.toMatrix())
        trial_support.Shape = shape
        trial_sketch = trial.addObject("Sketcher::SketchObject", "Sketch")
        trial_sketch.Placement = sketch.getGlobalPlacement()
        trial_sketch.AttachmentOffset = sketch.AttachmentOffset
        trial_sketch.MapReversed = sketch.MapReversed
        trial.recompute()
        return _reattach_planar(trial_sketch, trial_support, face_name, policy)
    finally:
        App.closeDocument(trial.Name)
        App.setActiveDocument(active.Name if active else "")


def _validate(sketch, support, face_name, policy, allow_cross=False, allow_pending=False):
    if not sketch.isDerivedFrom("Sketcher::SketchObject"):
        raise ValueError("A sketch is required")
    if policy not in ("preserve-local", "preserve-world"):
        raise ValueError("Unknown reattachment placement policy")
    doc = sketch.Document
    if doc.HasPendingTransaction and not allow_pending:
        raise ValueError("Finish the current transaction before reattaching")
    if policy == "preserve-world" and ("Invalid" in sketch.State or "Touched" in sketch.State):
        raise ValueError("Preserve-world requires a valid recomputed sketch placement")
    if policy == "preserve-world" and any(
            path.lstrip(".") == "AttachmentOffset"
            or path.lstrip(".").startswith("AttachmentOffset.")
            for path, expression in sketch.ExpressionEngine):
        raise ValueError("Preserve-world cannot replace an expression-driven attachment offset")
    if support.Document != sketch.Document or support == sketch:
        raise ValueError("Support must be another object in the same document")
    if support.isDerivedFrom("App::Link"):
        raise ValueError("Occurrence support requires an explicit definition/occurrence policy")
    if sketch in support.OutListRecursive:
        raise ValueError("Support depends on this sketch; reattachment would create a cycle")
    if any("Invalid" in obj.State or "Touched" in obj.State
           for obj in [support] + list(support.OutListRecursive)):
        raise ValueError("Support and its dependencies must be valid and recomputed")
    try:
        face = support.Shape.getElement(face_name)
    except (AttributeError, IndexError, RuntimeError, Part.OCCError) as exc:
        raise ValueError("Support face is unavailable") from exc
    if not isinstance(face, Part.Face) or not isinstance(face.Surface, Part.Plane):
        raise ValueError("Support must be a planar face")
    if not allow_cross and sketch.getParentGeoFeatureGroup() != support.getParentGeoFeatureGroup():
        raise ValueError("Cross-container support requires an explicit reference adapter")


def _reattach_planar(sketch, support, face_name, policy, own_transaction=True):
    _validate(sketch, support, face_name, policy, allow_pending=not own_transaction)
    doc = sketch.Document
    old_placement = sketch.Placement
    old_offset = sketch.AttachmentOffset
    if own_transaction:
        doc.openTransaction("Reattach sketch to planar face")
    try:
        sketch.AttachmentSupport = [(support, face_name)]
        sketch.MapMode = "FlatFace"
        doc.recompute()
        if "Invalid" in sketch.State:
            raise ValueError("Sketch attachment failed")
        if policy == "preserve-world":
            # With unchanged parent, preserving parent-local placement also
            # preserves world placement. Native attachment computes P = A * O.
            # Recover A from the new placement and retained old offset, then
            # solve O_new = A^-1 * P_old without guessing face axes.
            sketch.AttachmentOffset = old_offset.multiply(
                sketch.Placement.inverse()).multiply(old_placement)
            doc.recompute()
            if "Invalid" in sketch.State:
                raise ValueError("Sketch attachment failed")
        candidate = (sketch.getGlobalPlacement(), sketch.AttachmentOffset)
        if own_transaction:
            doc.commitTransaction()
        return candidate
    except Exception:
        if own_transaction:
            doc.abortTransaction()
            doc.recompute()
        raise
