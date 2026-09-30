# SPDX-License-Identifier: LGPL-2.1-or-later
"""Test-only planar reattachment operation for roadmap 11.7.

Not installed. Rejects calls with a transaction already open. Reuses native attachment
and Undo. The sketch stays in its existing container for both placement policies.
"""
import Part


def reattach_planar(sketch, support, face_name, policy="preserve-local"):
    """Explicitly replace a sketch's support with a same-document planar face."""
    if not sketch.isDerivedFrom("Sketcher::SketchObject"):
        raise ValueError("A sketch is required")
    if policy not in ("preserve-local", "preserve-world"):
        raise ValueError("Unknown reattachment placement policy")
    doc = sketch.Document
    if doc.HasPendingTransaction:
        raise ValueError("Finish the current transaction before reattaching")
    if policy == "preserve-world" and ("Invalid" in sketch.State or "Touched" in sketch.State):
        raise ValueError("Preserve-world requires a valid recomputed sketch placement")
    if support.Document != sketch.Document or support == sketch:
        raise ValueError("Support must be another object in the same document")
    try:
        face = support.Shape.getElement(face_name)
    except (AttributeError, IndexError, RuntimeError, Part.OCCError) as exc:
        raise ValueError("Support face is unavailable") from exc
    if not isinstance(face, Part.Face) or not isinstance(face.Surface, Part.Plane):
        raise ValueError("Support must be a planar face")
    old_placement = sketch.Placement
    old_offset = sketch.AttachmentOffset
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
        doc.commitTransaction()
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise
