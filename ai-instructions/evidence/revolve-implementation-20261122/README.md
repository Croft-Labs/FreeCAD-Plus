# Approved unified Revolve and expanded selection list

Final acceptance: **11 focused build tests and 188 installed native tests passed**,
zero failures/errors. Installed visual checks passed all five Revolve states and both
expanded collectors; screenshots were reviewed. A separate process reopened all five
saved files and verified valid geometry, identities, target flags and angular editor
parameters. Reports: build-regression, regression, visual and reopen JSON/text files.

`approval.json` records the explicit instruction to implement both reviewed changes.
The shared list reserves at least five complete native rows at current font size,
including horizontal-scrollbar space, and scrolls to all selected curves. Both
Extrude and Revolve use it. Native row selection and collector actions are retained.

Revolve reuses the shared task's profile/target selection, temporary display, preview,
accept/reject and History scopes. Its angular editor and evaluator retain native
axis/global links and native Revolution construction. The saved feature remains one
associative operation across New Solid/Add/Subtract edits. The original Extrude schema,
proxy classes and element-name namespace are unchanged. Native/body-owned legacy
Revolution/Groove histories keep native editors; this work does not convert them.

`build-regression.txt` records 11 passing development-build checks: native command
entry points, angle/offset/direction/symmetric/two-sided geometry, targets and invalid
tools, source-owned axis references, transformed sketches, planar solid/sheet profiles,
reference starts and angular limits, creation/editing identity, Undo/Redo and reopening,
external source ownership, downstream recompute and cycle/rerouting rejection, shared
task target/numeric/cancel behavior and the five-row list under long names/larger fonts.

`regression.FCMacro` adds those checks to the previous broad installed suite. Explicit
`--source` diagnostic runs omit only the real-command check while C++ is building;
normal build/installed runs include it. The final reports identify actual module paths.
`visual.FCMacro` uses real installed Revolution/Groove commands and History clicks for
five cases, validates actual tool volumes against native BRep fixtures, saves valid
features, rejects invalid acceptance atomically and captures the live task. `reopen.FCMacro`
loads the five files in a separate process and verifies geometry, identities, target
flags, and prefilled axis/angle/offset values in the shared editor.

Native limitations: To first/To last are unimplemented upstream and remain disabled.
Reference starts/limits must be planes containing the axis; offsets are angular.
Angle, symmetric/two-sided rotation and Through all use native Revolution construction.
Axis crossing, invalid planes, excessive total sweep and invalid Boolean results are
rejected rather than accepted with approximate geometry.

Installation hashes source/build/app copies and retains rollback files. Native modules
are installed to app/lib (build output resides under build/Mod). A first path mismatch
was diagnosed before broad execution; the exact newly misplaced file was removed after
hash verification, the correct native module installed with rollback, and installed
validation restarted. Validation output is cleared before each run to prevent stale
results from masquerading as new evidence. Runtime profiles are isolated; owner settings
are never used. Cleanup retains rollback files and the final shortcut profile.
