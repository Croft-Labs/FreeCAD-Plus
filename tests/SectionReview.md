# Reviewed intersection curves (F069)

In the source-built FreeCAD Plus fork, open **Part > Review intersection curves**.
This is a reviewed entry into the existing native Part::Section feature. The older
Section command remains available. The result intersects the inputs' surfaces; it
is not a projection, material cut, or saved viewport clipping plane.

1. Create a 10 x 8 x 6 mm box and a planar face crossing it at Z = 3 mm. Select
   both whole objects in the tree before launching, or capture each role in the
   dialog. Root Part shapes and whole root Bodies are supported, up to 200 faces
   per input. Links, nested members and individual face selections are refused.
2. Press **Preview curves**. Expect four edges totaling 36 mm around the box.
   A temporary colored wire shows the native result without creating document
   objects. Sources retain their geometry, placements, visibility and Body Tips.
3. Try the native **Approximate output curves** option. Changing it clears the old
   preview; preview again before creation. Coplanar surfaces may yield boundary
   edges rather than a unique intersection curve; inspect the actual result.
4. Move the face above the box, recompute, recapture it and preview. The dialog
   reports no curves and disables Create. Point-only contact is reported separately
   by its vertex count. Return the face and recapture before continuing.
5. Preview and choose **Create intersection**. A green native Section appears with
   editable Base, Tool and Approximation properties. Sources remain visible. Cancel
   before creation removes the overlay and leaves no result or Undo entry.
6. Undo/Redo creation. Save/reopen, enlarge the box to 20 mm long, and recompute.
   The intersection should become 56 mm long. Downstream features use the saved
   associative Section, not a preview snapshot. Native errors must be repaired if
   later inputs become unusable.

A source or document edit invalidates the displayed preview. Capture changed
inputs again before previewing or creating. This avoids applying a review to
geometry that has since changed. Creation is one transaction and rolls back when
native output does not match the reviewed result.

Run `TestSectionReview` in the source-built GUI with `tests` on `sys.path`, alongside
`TestSurfaceDeviation` for the shared temporary-overlay and shape-reference checks.
Roadmap 13.4a/b owns build, runtime and capture evidence.

Full F069 remains open for associative edge/face extraction, projection, nested and
external reference scopes, richer curve selection, live-topology repair and wider
kernel cases. Physical workflow acceptance is pending. No installer/release is
implied. Rotate to another family after this checkpoint and refine from owner
feedback or a demonstrated dependency.

Accepted evidence: `D:\Temp\Office-PC\freecad-plus-section-review-20261001`.
One grouped PartGui/PartScripts build, 18 distinct accepted checks and six reviewed
captures. The visual/ folder contains Intersection-Sources.FCStd (source fixture),
Intersection-Result.FCStd (created native section), and Intersection-Edited.FCStd
(reopened source enlarged to 20 mm). No physical acceptance or release is claimed.
