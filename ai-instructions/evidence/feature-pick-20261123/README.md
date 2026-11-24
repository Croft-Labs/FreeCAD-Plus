# Click and Shift-click feature selection - November 23, 2026

Owner approved the native-list proposal with "approved". Companion session
19c92fb00c8b was re-inspected: preview valid, violations empty, fingerprint
e07195b4afa79c97923f14b75bd7bb5b8b7d6734db3e35520a17a08e33c0e10a.
Chat approval is authoritative; tool approval state was not modified.

Plain click adds an eligible feature input once; repeated clicks retain it.
Shift-click removes an existing input and never adds an absent one. The gesture
is carried into deferred connected/tangent edge expansion and restored afterward.
Native consuming-picker guards still prevent recursive selection notifications.

Shared Extrude/Revolve, Loft, Thicken, Shell, plane/sketch placement and native
component Fillet/Chamfer/Draft collectors follow this rule. Single-input fields
retain replacement on plain click and clear a matching Shift-click. History
routes the clicked row directly during these feature tasks, preventing native
Shift range selection from removing unrelated rows. Visibility eyes and ordinary
selection outside these tasks retain their existing behavior. Sketch-region picks
add/remove their region's curves. Existing eligibility, predecessor checks,
conflicting-plane replacement, list order, Delete/Remove/Clear and geometry remain.

## Native acceptance and installation

Native build completed. All 12 final focused development checks and all 134
installed regression checks passed (zero failures/errors). The installed suite
includes actual Extrude/Shell/Fillet viewport gestures, connected/tangent expansion,
History clicks, plane/sketch placement, Draft plane/direction clearing, duplicate
and absent-item behavior, region removal, whole-sketch partial deselection,
Cancel/Undo/Redo, saved editing, eligibility and legacy selection preservation.
The existing desktop shortcut launched the installed app with an isolated profile;
its real viewport connected-edge add/remove check passed.

The initial broader development run passed 133/134 tests and exposed mapped versus
ordinary edge names in region removal. That correction passed the final focused
run and the entire installed suite. Earlier viewport investigation also identified
CAD navigation's reserved Shift gesture and a test point obscured by the radius
gizmo. Feature Shift clicks now use native ray-picking and selection gates, preserving
original occurrence paths; test points pick geometry rather than gizmos.

Eleven installed payloads have source/build/installed hash verification (ten Python
files and PartDesignGui.pyd) and retained rollback copies. No persistence schema or
native feature identity changed. Validation profiles were isolated; owner sessions,
settings and unrelated project.previewfirst.json were preserved. Older running
processes need reopening to load the updates.

[Final focused development checks](build-final.txt), [installed regression suite](regression.txt),
[shortcut verification](shortcut.json), and [installation/rollback manifest](install-manifest.json)
record the acceptance. Task-generated output was archived before bounded cleanup;
rollback files and the shortcut's isolated profile remain in the runtime directory.

## Direct installed captures

These are native task panels after real viewport interactions, not the preview
simulation. Layout and controls match the approved scope.

- [Extrude after click and repeated click](Extrude-selected.png)
- [Extrude after removal checks](Extrude-removed.png)
- [Shell after click and repeated click](Shell-selected.png)
- [Shell after Shift-click removal](Shell-removed.png)
