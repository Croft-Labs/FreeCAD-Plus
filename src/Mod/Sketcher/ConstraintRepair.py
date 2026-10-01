# SPDX-License-Identifier: LGPL-2.1-or-later
"""Review native constraint deactivation on an isolated temporary sketch copy."""
import hashlib
import FreeCAD as App
from freecad.gui.DependencyInspector import identity
from SketchReuse import constraint_signature


def tr(text):
    return App.Qt.translate("ConstraintRepair", text)


def snapshot(sketch):
    if sketch.TypeId != "Sketcher::SketchObject" or sketch.getParentGeoFeatureGroup() is not None:
        raise ValueError(tr("Select a root sketch; Body, Part and occurrence members are not supported yet."))
    if (sketch.MapMode != "Deactivated" or sketch.AttachmentSupport or sketch.ExternalGeometry
            or sketch.ExpressionEngine or sketch.OutList):
        raise ValueError(tr("This repair supports free sketches without external geometry, support, expressions or linked inputs."))
    if not 0 < sketch.GeometryCount <= 200 or not 0 < sketch.ConstraintCount <= 400:
        raise ValueError(tr("Choose a sketch with 1-200 geometry elements and 1-400 constraints."))
    # Invalid/conflicting sketches are deliberately accepted. Diagnose the authored
    # geometry/constraints on a native copy rather than trusting a stale Shape.
    return identity(sketch), hashlib.sha256(sketch.Content.encode("utf-8")).hexdigest()


def ready(sketch):
    import FreeCADGui as Gui
    doc = sketch.Document
    if (App.ActiveDocument != doc or Gui.Control.activeDialog()
            or Gui.activeDocument().getInEdit() or doc.HasPendingTransaction or App.getActiveTransaction()):
        raise ValueError(tr("Activate this document and finish the sketch edit, task or pending transaction first."))


def solver_info(sketch):
    status = sketch.solve()
    groups = {name: list(getattr(sketch, attr)) for name, attr in (
        ("Conflicting", "ConflictingConstraints"), ("Redundant", "RedundantConstraints"),
        ("Partially redundant", "PartiallyRedundantConstraints"), ("Malformed", "MalformedConstraints"))}
    ok = status == 0 and not any(groups.values())
    state = ("Fully constrained" if sketch.DoF == 0 else "Underconstrained") if ok else (
        ", ".join(name for name, ids in groups.items() if ids) or "Solver failed")
    return {"status": status, "ok": ok, "state": state, "dof": sketch.DoF, "groups": groups}


def probe(sketch, expected, disabled=()):
    """Return native before/after diagnostics and copied result shape; no source edits."""
    ready(sketch)
    if snapshot(sketch) != expected:
        raise ValueError(tr("The sketch changed. Review again before previewing or applying repair."))
    disabled = tuple(sorted(set(disabled)))
    for index in disabled:
        if (isinstance(index, bool) or not isinstance(index, int)
                or not 0 <= index < sketch.ConstraintCount or not sketch.Constraints[index].IsActive):
            raise ValueError(tr("Choose active constraints from the current review."))
    owner = sketch.Document
    scratch = App.newDocument("ConstraintRepairPreview", hidden=True, temp=True)
    try:
        clone = scratch.copyObject(sketch, False)
        if constraint_signature(clone) != constraint_signature(sketch):
            raise ValueError(tr("The temporary copy did not preserve the source constraints."))
        before = solver_info(clone)
        for index in disabled:
            clone.setActive(index, False)
        after = solver_info(clone)
        scratch.recompute()
        return {"expected": expected, "disabled": disabled, "before": before, "after": after,
                "shape": clone.Shape.copy() if after["ok"] else None}
    finally:
        App.closeDocument(scratch.Name)
        if App.ActiveDocument != owner:
            App.setActiveDocument(owner.Name)


def apply(sketch, preview):
    ready(sketch)
    if not preview or not preview["disabled"] or not preview["after"]["ok"]:
        raise ValueError(tr("Preview a successful repair before applying it."))
    # Re-evaluate on an isolated copy before opening the owner's transaction.
    checked = probe(sketch, preview["expected"], preview["disabled"])
    if not checked["after"]["ok"] or checked["after"]["dof"] != preview["after"]["dof"]:
        raise ValueError(tr("The proposed repair no longer matches its preview. Review again."))
    doc = sketch.Document
    doc.openTransaction(tr("Deactivate reviewed sketch constraints"))
    try:
        for index in checked["disabled"]:
            sketch.setActive(index, False)
        result = solver_info(sketch)
        if not result["ok"] or result["dof"] != checked["after"]["dof"]:
            raise ValueError(tr("The source solve did not match the reviewed repair."))
        doc.recompute()
        if "Invalid" in sketch.State or "Touched" in sketch.State:
            raise ValueError(tr("The repaired sketch did not recompute successfully."))
        doc.commitTransaction()
        return result
    except Exception:
        doc.abortTransaction()
        doc.recompute()
        raise
