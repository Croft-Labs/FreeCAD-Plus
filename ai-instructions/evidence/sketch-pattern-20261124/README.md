# Sketch Pattern implementation - November 24, 2026

Owner approved the [native-widget proposal and workflow](../sketch-pattern-preview-20261124/README.md)
in chat: **"approved. implement"**. Companion approval state was not modified.

## Implementation

`Sketcher_Translate` retains its command identity, icon and W shortcut, and opens
the dedicated **Sketch Pattern** task. Empty entry and eligible preselection work.
Native tool ownership supplies viewport/selection picking and temporary drawing;
the Python task uses the approved controls and shared inline error presentation.
Normal sketch sections restore their previous visibility on leaving the tool.
The separate move-only command and Mirror remain intact.

- Linear: one/two arbitrary directions, axis/line, two-point and vector references.
- Circular: angular, radial or combined directions; point, circle/arc center and
  radius/diameter references. Radial translation preserves geometry size.
- Independent one/two/symmetric extents, pitch/total values, instance counts
  including the original, and reverse. Symmetric requires an odd total count.
- Full-circle totals omit the duplicated endpoint; other overlapping angular
  extents, parallel grid directions, zero vectors and inward crossing are rejected.
- Geometry click-add/Shift-remove, Delete/Remove/Clear, reference activation,
  live preview, Apply/Done/Cancel/Escape, native Undo/Redo and deferred numeric entry.

Apply creates native Sketcher geometry and transferable constraints in one
transaction. Construction geometry and original constraints are preserved.
Optional dimensions relate copied anchors to their originals; circular placement
uses native construction radii and angular/equal constraints. Zero-radius anchors
use consistent offsets so the original can still move away from the center.
Native internal geometry supplies ellipse/spline anchors. Only a just-added
derived equation is removed when existing equations already imply it; existing
constraints are never deleted to make a pattern succeed.

No new saved pattern feature, property schema or custom solver equation is used.
References and direction vectors are evaluated when Apply runs; output is editable
native sketch geometry/constraints, rather than a persistent pattern-parameter object.
Optional dimensions may add construction helpers. Unsupported dimensioned geometry
fails atomically with an inline error. Preview/apply bounds are 1,000 instances and
10,000 generated geometry elements.

## Validation and delivery

Acceptance covers independent extents and coordinates, full circles and radial
rows, construction state, original constraint names/content, relative dimensions
and source degrees of freedom, clockwise/half-turn/center-point cases, external
references, arcs/splines, native Undo/Redo, save/reopen and downstream solids.
GUI cases cover empty/preselected entry, real viewport clicks, Shift removal,
radius reference selection, error recovery, numeric commit, component sketches
in Plus/Classic presentations, task isolation and Escape retaining sketch edit.

The final native [build completed](build.log), and all [23 pattern cases passed](build-result.json).
All **53 installed acceptance/regression checks passed**: [result](installed-result.json),
[test listing](installed-tests.txt). The unchanged desktop shortcut passed native
Apply/Undo/Redo/Done: [shortcut result](shortcut-result.json). A [fresh process](fresh-reopen.json)
reopened 4 ordinary pattern elements, 10 construction helpers and 48 constraints,
with 4 remaining source degrees of freedom and no redundant-constraint error.

Direct screenshots of the **working installed task**, not simulations:

- [Linear: two directions with independent forward/backward extents](linear.png).
- [Circular: angular and radial directions](circular.png).

Native viewport picking is covered by behavioral tests. The full-window Qt grab
has unreliable OpenGL pixels on this machine and is not used as geometry-image evidence.
The earlier broad toolbar run reached its 300-second deadline before completion;
it is not counted as a completed regression pass. Its detected Escape issue was
fixed and is covered by the final pattern suite. Unrelated untracked
`project.previewfirst.json` was preserved.

The existing local FreeCAD Plus native build and owner app payload are used;
this is not an EAS/Expo build, a separate app clone or a release. Installation
retains the previous native module for rollback and verifies copied hashes.
The existing `freecad plus 0.1.0.lnk` remains the delivery shortcut. Target and working
directory were reread: `_temp builds/FreeCAD-Plus/Launch FreeCAD Plus.bat` and
`_temp builds/FreeCAD-Plus`, respectively; the launcher runs `app/bin/FreeCAD.exe`.
[Installed file hashes and rollback location](install-manifest.json).
