# Extrude Solid and Sheet — November 23, 2026

Owner approved the [native preview](../extrude-sheet-preview-20261123/README.md)
and explicitly requested implementation. Solid/Sheet appear on the left of
Operation, New/Add/Subtract on the right. Solid is the default. Sheet selects
New, disables all operation choices and clears any target. Returning to Solid
re-enables the choices and leaves New selected. Revolve retains its existing UI.

Sheet uses native Part extrusion with Solid disabled. Open sketch curves,
selected edges, standalone curves with an explicit direction, and face boundaries
produce uncapped faces/shells. A line produces one face with no thickness; a closed
profile also remains uncapped. The output type persists on the existing shared
Extrude feature; older features without the property continue as Solid. Editing
preserves identity, references, native Undo/Redo and sequential-history checks.
Backend Bodies remain internal results and no new Body-creation step is exposed.

Sheet forces New at both UI and evaluator boundaries. Existing hidden curves
stay hidden when Sheet becomes available. Initially visible standalone curves
become available in Sheet mode; manual History-eye choices are retained. Solid
and Revolve behavior is covered by the related regression suite.

Supported Sheet extents include length, reverse, start offset/reference,
symmetric length, two independent sides, explicit direction and measurement
along the profile normal. Up to face/shape currently requires a forward planar
face spanning the complete end; symmetric limits require switching to One side
or Two sides. Taper is supported for closed profiles with Length. Open-curve taper
is rejected explicitly because native Part extrusion does not produce that sheet.
Target-dependent end conditions are disabled in Sheet; switching from one resets
the end to Length. Unsupported combinations show the existing highlighted error.

Validation uses isolated build/installed profiles and synthetic documents. The
initial eight focused checks passed after correcting a Compound center lookup.
The expanded initial build run passed 87 of 88 checks; its sole error exposed
native open-curve taper's unsupported output. The final code rejects that case
with a specific message, and all ten focused checks then passed. Initial and
corrected logs are retained. All **88 installed regressions pass** (ten Sheet,
existing Solid/Revolve, task entry, visibility and plane/history checks). Separate
installed checks invoke the native Pad command, click Sheet, accept a 30 x 8 mm
sheet, double-click edit it to 12 mm, then save it. Another process opens the file
through the Plus document route, enters its component, moves the sketch and verifies
the same feature recomputes to 360 mm² with one face and zero solids. The initial
reopen harness used raw App.openDocument without entering the component; existing
modeling-intake checks rejected that context. Correcting the harness to match the
supported Plus route resolved it without production changes. The initial failure
is retained as reopen-initial.json. The existing-shortcut check also passed.

Direct installed screenshots: [Solid](installed-solid-operation.png),
[Sheet with New locked](installed-sheet-operation.png),
[full Sheet task](installed-sheet-task.png),
[actual accepted line-to-sheet result](installed-sheet-result.png).
The result image renders the actual accepted feature, framed to its bounds; it
is not the earlier preview fixture. Numeric/topological checks verify zero solids.

Four Python files are installed with source/build/installed SHA-256 verification
and retained rollback copies in install-manifest.json. Existing owner processes
and settings are preserved. Already-running processes need restart to load the
new module. The existing desktop shortcut is verified and launched with a separate
validation profile. Generated fixture documents/profiles are removed after
archiving evidence; rollback files and the shortcut profile are retained.
Unrelated project.previewfirst.json is preserved and excluded from the commit.
