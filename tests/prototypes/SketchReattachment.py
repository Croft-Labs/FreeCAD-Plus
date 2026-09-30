# SPDX-License-Identifier: LGPL-2.1-or-later
"""Test-only planar reattachment operation for roadmap 11.7.

Not installed. Call with no transaction already open. Reuses native attachment
and Undo; preserves the local attachment offset, not the old world placement.
"""
import Part


def reattach_planar(sketch, support, face_name):
    """Explicitly replace a sketch's support with a same-document planar face."""
    if not sketch.isDerivedFrom("Sketcher::SketchObject"):
        raise ValueError("A sketch is required")
    if support.Document != sketch.Document or support == sketch:
        raise ValueError("Support must be another object in the same document")
    try:
        face = support.Shape.getElement(face_name)
    except (AttributeError, IndexError, RuntimeError, Part.OCCError) as exc:
        raise ValueError("Support face is unavailable") from exc
    if not isinstance(face, Part.Face) or not isinstance(face.Surface, Part.Plane):
        raise ValueError("Support must be a planar face")
    doc = sketch.Document
    doc.openTransaction("Reattach sketch to planar face")
    try:
        sketch.AttachmentSupport = [(support, face_name)]
        sketch.MapMode = "FlatFace"
        doc.recompute()
        if "Invalid" in sketch.State:
            raise ValueError("Sketch attachment failed")
        doc.commitTransaction()
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise
