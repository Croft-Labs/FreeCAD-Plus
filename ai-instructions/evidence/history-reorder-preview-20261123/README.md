# History drag-order proposal — November 23, 2026

Status: direct native UI screenshots awaiting approval. No production, backend,
persistence or installed application change. The earlier Plane/Sketch reference
selection proposal remains separately pending.

## Requested behavior

The fundamental Coordinate System always comes first. Defining inputs must precede
their consumers, including a custom datum plane followed by its sketch and solid
operation. Feature rows can be dragged to other valid positions. Dropping a defining
feature after a dependent places it immediately before the first dependent, then
shows a popup naming the feature that prevents the requested move. The complementary
case, moving a consumer before its inputs, must also preserve dependency order.

## Direct screenshots

- [Initial native History](initial.png): Coordinate System, support plane, sketch,
  extrusion, independent plane.
- [Valid independent-plane move](valid-move.png): placed between support and sketch,
  with no popup.
- [Corrected invalid move](corrected-order.png): support plane dropped after the
  extrusion is placed immediately before its first dependent, the sketch.
- [Requested popup](cannot-move-after.png): names both items and states the corrected
  position. It appears after the tree is updated.
- [Consumer-before-input popup](cannot-move-before.png): the extrusion remains after
  its sketch, with the corresponding explanation.

## Scope and provenance

Product baseline `b5b1e53a616b66e91a3adf0b904a5533a405b3a2`; exact UI snapshot
`224e6e0e2a5ea18fb45ba5dae1cdb5a2d3e0bc96` in
`C:/Users/dgium/Documents/__Apps/FreeCAD/history-reorder-preview/review-source`.
The original untracked `project.previewfirst.json` is untouched.

Session `661e846aab01`, fingerprint
`ae4db163f725c584d967a4f790112838a342f4fe6d8c363df4a8a47528357acf`.
Final inspection: preview fresh, no scope violations, approval false. Only the candidate
`panel.py` changes. Its snapshot and the rendering scripts are archived here.

The native renderer builds a real datum-plane → sketch → extrusion dependency chain
using the installed APIs. An isolated UI subclass handles Qt drag-enter/drop events;
the renderer supplies explicit specimen order outcomes and native QMessageBox dialogs.
All three drop cases and the complete coordinate-subtree drag lock pass. Native order,
object IDs, visibility and reference links remain unchanged. See [baseline](baseline.json)
and [candidate](candidate.json) results. This verifies UI outcomes, not a production
reorder service, saved ordering or a complete operating-system mouse-drag gesture.

The renderer uses explicit isolated settings under the development runtime's
`validation/history-reorder-preview-20261123`; it never uses the owner profile.

## Implementation after approval

Retain the existing native dependency-based History and structural coordinate prefix.
Add source-owned, persistent preferred ordering without rewriting native ownership,
feature references or geometry and without introducing artificial dependency links.
Files without saved preferred order retain their existing deterministic sequence.
Respect direct and transitive geometry/expression dependencies, including hidden native
inputs and Body-result producers. Maintain stable ordering of unaffected rows.

Resolve the requested insertion against the latest graph: clamp an input before its
earliest dependent, or a consumer after its latest predecessor; update the tree before
showing the naming/explanation popup. Coordinate objects remain non-draggable and
features cannot be inserted ahead of them or nested beneath each other. Reject stale
identity/context, cross-component and external drag data. Preserve eye-column clicks,
selection, double-click editing, active task transactions and other panel tabs.

Verify actual mouse dragging, chains/multiple consumers, independent moves, Undo/Redo,
save/reopen, external source ownership, native reference/identity/shape preservation,
new/deleted features and pending-task behavior before build/install/shortcut restart.
