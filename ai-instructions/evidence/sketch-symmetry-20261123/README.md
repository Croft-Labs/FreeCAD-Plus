# Sketcher symmetry workflow - November 23, 2026

Owner approved the dedicated task preview with a larger Geometry list.
The enlarged native-widget preview was rendered and inspected under session
aef4e2a28b5b, fingerprint
1ce61a8d2dc097e09a48e07851110902b55f88894eca1578fedf97e6bcf5d1ba.
Chat approval is authoritative; tool approval state was not changed.

Mirror now opens without preselection, including in an empty sketch. It has a
large scrollable Geometry list, one symmetry-reference field, existing native
options and Apply/Done. Click adds once; Shift-click removes; Delete/Remove/Clear
work in the collector. Apply previews through native getSymmetric and commits
through addSymmetric, remains open, clears geometry and keeps the reference.
Done/Cancel/Escape leave pending input unapplied and return to sketch editing.
The normal Sketch Edit, Constraints, Elements and advanced solver sections are
hidden only during symmetry and restored to their previous state when it ends.

Native line/curve, construction, standalone point, axis, external line and point
center semantics remain. Native options are mutually exclusive and initially off.
Original deletion remaps surviving references; Undo/Redo clears pending references.
Existing copied constraints remain native; no automatic dimensions are added.
There is no active-Body dependency or new saved object/schema.

## Verification and installation

Native build passed. The development workflow passed 11 checks, followed by the
standalone-point compatibility check after its final adjustment. All 41 installed
checks passed: 12 symmetry cases and 29 related regressions for task buttons,
coordinate visibility, History-tab handling, no automatic dimensions, exit-fit and
single-Enter dimension acceptance. Symmetry coverage includes actual viewport
click/Shift gestures and native axis hover/click, duplicate picks, scrolling,
invalid-axis recovery, repeated Apply, Cancel/Done/Escape, native options,
construction/point geometry, external references, both UI presentations,
Undo/Redo and save/reopen.

The initial checks exposed command enablement still requiring preselection and
the need to carry the shared delayed Shift-pick intent. Both were corrected.
The thin-axis viewport test now locates the native hover hit before clicking;
projection rounding was placing the test click beside the axis. Temporary native
diagnostics were removed. A validation process briefly held a build module open;
it exited and the subsequent final build passed.

Installed SketcherGui.pyd matches the tested build hash. The previous module is
retained under the runtime validation install-backup directory. TestSketchSymmetry.py
is also installed and registered in the build/install lists. Owner config files
and unrelated project.previewfirst.json are preserved.

- [Installed regression log](installed.txt)
- [Installed result](installed.json)
- [Development workflow checks](development.txt)
- [Point compatibility check](point-compatibility.txt)
- [Build log](build.log)
- [Installation and rollback manifest](install-manifest.json)

The existing desktop shortcut passed a separate fresh-process native viewport
add/remove/axis/Apply check with explicit isolated config files. Owner user/system
config hashes are unchanged. [Shortcut verification](shortcut.json), [test log](shortcut.txt).

## Direct installed screenshots

These are working native task panels, not simulations.

- [Ready to apply](symmetry-ready.png)
- [Invalid axis feedback](symmetry-invalid-axis.png)
- [After real viewport selection and Apply](symmetry-applied.png)
