# SPDX-License-Identifier: LGPL-2.1-or-later
"""Test-only Make Unique proof for a native sketch/extrusion definition."""
import uuid


def make_unique(occurrence):
    source = occurrence.LinkedObject
    if source.Document != occurrence.Document or not source.isDerivedFrom("App::Part"):
        raise ValueError("Prototype requires a same-document part definition")
    members = list(source.Group)
    sketches = [o for o in members if o.isDerivedFrom("Sketcher::SketchObject")]
    extrusions = [o for o in members if o.isDerivedFrom("Part::Extrusion")]
    if (len(members) != 2 or len(sketches) != 1 or len(extrusions) != 1
            or extrusions[0].Base != sketches[0]):
        raise ValueError("Prototype supports only one independent sketch and its extrusion")
    if any(dep not in members for obj in members for dep in obj.OutList):
        raise ValueError("Prototype does not copy external dependencies")
    for obj in [source] + members:
        if not hasattr(obj, "SemanticIdentity") or not obj.SemanticIdentity:
            raise ValueError("Prototype requires explicit source identities")
    placement = occurrence.LinkPlacement
    doc = occurrence.Document
    doc.openTransaction("Make occurrence unique (prototype)")
    try:
        copied = doc.copyObject(source, True)
        for obj in [copied] + list(copied.Group):
            obj.addProperty("App::PropertyString", "SourceIdentity", "Prototype")
            obj.SourceIdentity = obj.SemanticIdentity
            obj.SemanticIdentity = str(uuid.uuid4())
        occurrence.setLink(copied)
        occurrence.LinkPlacement = placement
        doc.recompute()
        doc.commitTransaction()
        return copied
    except Exception:
        doc.abortTransaction()
        raise
