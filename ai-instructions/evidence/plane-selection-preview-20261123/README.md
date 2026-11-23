# Plane selection proposal — November 23, 2026

Status: native UI demonstration awaiting screenshot approval. Production and installed
code are unchanged. The owner requests compatible reference accumulation, replacement
of conflicting references, and a plane through a point normal to a selected line for
both datum-plane creation and sketch-plane designation. The follow-up explicitly makes
planes/flat faces, lines/edges, and points/vertices interchangeable. Straight edges and
planar faces supply the equivalent geometry.

## Direct screenshots

- [Current XY then XZ behavior](before.png): both references remain and the sketch plane is invalid.
- [Proposed XY then XZ](replace-plane.png): only XZ remains, with its valid preview.
- [Compatible line and straight edge](coplanar-lines.png): both remain and define their common plane.
- [Normal through a point/vertex](normal-through-point.png): the plane passes through the vertex and is perpendicular to the edge.
- [Planar face replacing a plane](planar-face.png): the flat face behaves like a plane.

All images are native application screenshots with explicit specimen callbacks. The
Qt window capture's OpenGL area is replaced by the same live viewport's pixel readback
using the existing TestComponentFading.capture helper, correcting Qt capture artifacts.
No geometry or difference between baseline and candidate is painted over or hidden.

## Scope and provenance

- Product baseline: `985f7aeb299bc6ad478aa1cf751f5bcc50186e92`.
- Exact two-file UI snapshot: `2394849cebbb38dc06658ad7f48eb45d1f7c854e` in
  `C:/Users/dgium/Documents/__Apps/FreeCAD/plane-selection-preview/review-source`.
  The original untracked `project.previewfirst.json` is untouched.
- Review session: `cc6496002256`; fingerprint
  `3dd056488e4bcc7aa4487ac6d0a28129621057edb87b8311af39e40803862ea5`.
- Final inspection: preview fresh, no scope violations, approval false. Only candidate
  `plane_task.py` and `sketch_task.py` differ. Their archived snapshots are included here.
- Renderer: `C:/Users/dgium/Documents/__Apps/FreeCAD/plane-selection-preview/render.py`
  with `scene.FCMacro`, also archived here. It uses the installed development FreeCAD
  executable and explicit isolated configurations under runtime
  `validation/plane-selection-preview-20261123`, never the owner profile.

[Baseline](baseline.json) and [candidate](candidate.json) results cover eight scenarios
per task: XY→XZ, plane→flat face, coplanar line/edge, line/point, edge/vertex,
point-first line selection, skew-line replacement, and three points/vertices. All 16
candidate UI-state checks pass. Incompatible skew lines leave the new line selected
and correctly under-defined. IDs and visibility return to their prior states on Cancel.
No task is accepted. This is not a functional solver, persistence or installation test.

## Work after approval

Replace the specimen callbacks with shared geometric compatibility and intake logic.
Keep compatible incomplete inputs; discard prior defining references only for a
geometric conflict, not for foreign/unsupported/later input or unrelated invalid
origin/axis/offset settings. Apply existing ownership and sequential checks before
mutating collected references. Extend sketch-plane construction beyond a single
support plane/face, retaining the existing support-frame defaults for that case.

Add the normal-through-point construction in either pick order, including a point on
the line. Preserve existing saved line-plus-point *containing-plane* geometry through
explicit compatible persistence/versioning; do not reinterpret old saved references.
Preserve selection/visibility cleanup, source ownership, offsets, frame controls,
Undo/Redo, associative recompute, and saved identities. Verify native picking,
replacement/accumulation, normal/point geometry, editing, external context and reopen
before installation, shortcut restart, commit and push.
