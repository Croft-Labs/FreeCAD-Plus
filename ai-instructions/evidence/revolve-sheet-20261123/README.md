# Revolve Solid and Sheet — November 23, 2026

Owner approved the [native preview](../revolve-sheet-preview-20261123/README.md)
and explicitly requested implementation. Revolve shares Extrude's Solid/Sheet
controls: Solid default on the left, New/Add/Subtract on the right. Sheet selects
and locks New, disables all operation buttons and clears the target. Returning
to Solid re-enables the operations and leaves New selected. Axis and angle
controls retain their existing layout. The preview label becomes Revolution preview.

Sheet revolves native wires without filling the profile or adding caps. Open and
closed curves, selected edges and planar face boundaries are supported. Curves
must share a plane with the rotation axis; degenerate output is rejected. Sketch
axes, component axes and selected straight edges/axes remain supported. Length is
not involved: Angle, Through all (360 degrees), reverse, angular start offset,
reference start, symmetric angle, two sides and angular limiting planes use the
existing Revolve meanings. Limits/start planes must contain the rotation axis;
two angles total at most 360 degrees. No solid volume is fabricated for a Sheet.

The saved Revolve_output property defaults older features to Solid. Shared
persistence adds the property on edit, preserves identities, references, ownership,
sequential history and Undo/Redo. New is enforced at both UI and evaluator boundaries.
Task visibility restores only initially visible curves when Sheet is selected;
hidden curves remain hidden and manual History-eye choices retain their meaning.
The axis guide uses profile bounds so compound curve profiles remain supported.

Eight new native acceptance tests cover open/full/partial rotation, angles and
directions, offsets/reference planes/axes, multiple curves and face boundaries,
closed-profile Solid/Sheet changes, legacy defaults, native command/task/edit,
target clearing, hidden-curve visibility, cancellation, identity, Undo/Redo,
save/reopen, associativity and sequential-input rejection. The initial seven-test
run had one test-only error asking a Compound for CenterOfMass; the corrected
assertion reads the generated face's centroid. That initial log is retained.

All **96 build and 96 installed regression checks passed**, covering the eight
new Sheet tests, Sheet/Solid Extrude, Solid Revolve, visibility, task entry and
plane/history behavior. Native interaction, separate-process reopen/recompute
and existing-shortcut checks also passed; results are stored alongside this file.
The native interaction check creates a 270-degree sheet from a 15 mm line at
radius 10 mm, then double-click edits it to 180 degrees, retaining its identity.
The fresh process reopens it through the Plus document route and moves the sketch.
Six Python files are installed with source/build/installed hashes and retained
rollback copies. Owner sessions/settings remain untouched; existing processes
need restart to load the changed modules. Generated validation fixtures are
removed after evidence archival, retaining rollback and the shortcut profile.
Unrelated project.previewfirst.json remains untracked and untouched.

Direct installed screenshots: [Solid default](installed-solid-operation.png),
[Sheet with New locked](installed-sheet-operation.png),
[Revolve task](installed-sheet-task.png),
[actual accepted 270-degree sheet](installed-sheet-result.png).
These images show the implemented native controls and accepted feature, not the
earlier UI prototype. The specimen is one face with zero solids; the later edit
to 180 degrees has area 471.238898 mm² and retains the same feature identity.
