# Sketcher symmetry task preview - November 23, 2026

Owner requests a task-panel workflow for creating symmetric sketch geometry with
a geometry list, a single-line symmetry-axis field and adjacent Apply/Done buttons.

Current native Sketcher_Symmetry (Mirror) requires geometry preselection and uses
the viewport axis/point pick to commit. Its tool panel exposes Delete original
geometries and Create symmetry constraints. Proposed workflow:

- Show a dedicated symmetry task: temporarily hide Sketch Edit, Constraints,
  Elements/lines and advanced solver sections. Restore prior section visibility
  when leaving symmetry. Keep viewport geometry visible for selection.
- Open with no preselection or prefill eligible selected internal sketch geometry.
- Five-row scrollable Geometry list; activate it to collect, click adds once,
  Shift-click removes; retain Delete/Remove/Clear, without Select/Confirm toggles.
- Activate the single-line Axis of symmetry field to pick a sketch horizontal or
  vertical axis, straight sketch/construction/external line; retain native point
  center symmetry. A new valid reference replaces the old; Shift-click clears a match.
- Preview the mirrored result until Apply. Enable Apply only for eligible geometry
  and a valid reference. Invalid picks preserve valid inputs and show inline errors.
- Apply through native addSymmetric and its transaction/Undo behavior. Keep existing
  Delete original geometries and Create symmetry constraints options, defaults and
  mutual exclusion. No automatic dimensions are introduced.
- Owner clarified: Apply stays in symmetry, clears the geometry list and retains
  the axis for the next set. Done closes symmetry and returns to sketch editing.
  Apply alone creates geometry; Done discards pending preview without creating
  another copy. Previously applied sets remain.
- Cancel/Escape discards only uncommitted picks/preview and keeps sketch editing;
  Exit Sketch retains its existing behavior. Preserve native geometry/constraints,
  original geometry by default, coordinate graphics and unrelated sketch controls.

## Direct preview and limits

[Current native task](baseline.png), [proposed task ready to Apply](proposed.png),
[empty input](empty.png), [invalid axis feedback](invalid-axis.png), and
[post-Apply state](after-apply.png), and [Done returns to sketch editing](after-done.png).

The prototype replaces the symmetry tool widget in an isolated actual FreeCAD
sketch editor. Its list/axis and Apply interactions are simulated; no mirrored
geometry is committed. Native fixture geometry count stays unchanged in baseline
and candidate. Checks confirm empty/invalid disabling, duplicate-add suppression,
Shift removal, recovery, post-Apply reset and Done returning to sketch editing without a commit. Normal sections are verified hidden during symmetry and restored after Done. These are UI checks,
not proof of working command integration, picking, geometry, Undo or persistence.
No production source or installed payload changed. The simulation footer is preview
annotation, not a proposed product control.

Companion session aef4e2a28b5b supersedes c5ec4798c9a1 with the dedicated task layout; adapter baseline
be7bf70c1f925f182d1eb8fc6c90b3109d049cb4; fingerprint
8cbe727921cf6509587d4c22e9fdc7286e6f428349daf9cc5d13b53068f9fd96.
Only symmetry_ui.py changed in candidate. Preview valid, scope violations empty.
Owner preview approval is pending; tool approval state was not modified.

Implementation should extend the existing native symmetry handler/controller so
its task participates in native sketch tool lifecycle and Cancel/Exit behavior.
Verify no-preselection entry, native sketch geometry IDs (including construction
and external references), axis replacement/removal, invalid geometry recovery,
click/Shift and chain selection, Apply-only mutation, native solver/constraints,
repeated Apply, Done with pending inputs, Undo/Redo and cancellation in both task presentations. Validation
must use isolated profiles; preserve unrelated project.previewfirst.json.
