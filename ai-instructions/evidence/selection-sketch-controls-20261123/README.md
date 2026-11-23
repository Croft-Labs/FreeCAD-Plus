# Selection toolbar and sketch task controls — November 23, 2026

Owner approved the selection-control preview, then explicitly requested implementation
of the already-previewed sketch Cancel/Exit buttons in the same task.

## Implemented behavior

The chain control shows its existing icon and current Single Curve, Connected Curves
or Tangent Curves label. The category filter shows All, a named omitted category,
an omitted count, or a sole category followed by only; its tooltip lists enabled
categories. Select all / reset restores all eight categories. Select 1 arms a
one-category replacement without clearing the current effective filter; choosing
a category commits the singleton, while outside click/Escape/menu dismissal
abandons the pending choice. The final enabled checkbox cannot be cleared.
Older empty saved filters recover to All. Shared configuration updates the native
gate and live buttons; committed settings survive toolbar reconstruction/restart.
Native command gates, taxonomy, chain expansion, directional/persistent behavior,
and Classic selection remain unchanged.

Sketch editing shows Exit Sketch in place of Close. A native ActionRole Cancel
button appears alongside it while a geometry/constraint handler is active. It
delegates one Escape press/release to the existing handler and returns focus to
the modeling view. An unfinished drawing step may reset while the handler stays
active, exactly as keyboard Escape does. Completed geometry/constraints remain.
Exit Sketch retains native rejection/reset/recompute behavior. Both task modes
share these buttons; LeaveSketchWithEscape remains effective for the keyboard.
Tool-state visibility is deferred until transitions complete, including tools
without settings widgets; queued callbacks are bounded by the dialog's lifetime.

## Build and validation

Built SketcherGui and FreeCADPlusScripts in the existing isolated development tree.
All 16 focused build checks and all 39 installed regression checks passed (zero
failures/errors). Build and installed artifacts identify exact module paths.
Eight installed visual cases, a two-process settings save/reopen check and the
existing-shortcut verification passed. The fresh process retained Curves only,
Tangent Curves, both selection-toggle settings and native Classic restoration.

Direct installed screenshots: [toolbar](selection-toolbar.png),
[Select 1 prompt](select-one-menu.png), [Curves only](curves-only-menu.png),
[idle sketch buttons](sketch-idle-buttons.png),
[drawing buttons](sketch-drawing-buttons.png),
[constraint buttons](sketch-constraint-buttons.png),
[drawing task](sketch-drawing-tasks.png).
Toolbar/button images capture native controls with their actual window backdrop;
raw child-widget grabs were transparent. These screenshots establish widget layout,
not OpenGL framebuffer fidelity. Native viewport admission is covered by the tests.

The focused suite exercises real Qt viewport clicks and boxes in models/sketches,
native command-gate intersection, category summaries, reset, singleton replacement,
outside/Escape abandonment, final-category guard, empty-preference recovery,
toolbar rebuild, chain modes/topology, directional behavior and persistence toggle.
Sketch checks cover idle/active geometry and constraint actions in both UI modes,
partial rectangle equivalence to one Escape, keyboard preference, immediate exit
with a queued tool update, completed-geometry preservation, History restoration
and coordinate visibility.

The broader installed suite additionally covers coordinate-system hiding/restoring,
exit fitting and camera orientation, empty/cancelled sketch handling, queued-fit
lifetime, native body and external-source sketches, automatic dimensions, deliberate
numeric entry, and prior-tab restoration through creation/edit workflows.

## Installation and preservation

Five files installed: selection_toolbar.py, category_selection.py, two regression
modules and lib/SketcherGui.pyd. Source/build/installed hashes and prior hashes are
in install-manifest.json. Original and loaded-image rollback copies remain under
the runtime validation directory's install-backup. No owner process was terminated
and no owner settings profile was used. Running sessions cache the earlier Python
modules/native library and need restart to load the changes.

The existing desktop shortcut target/working directory are checked explicitly;
shortcut validation uses separate user/system configuration and app data. Generated
test documents/screenshots/profiles are cleaned after archiving; rollback files
and the shortcut's isolated profile are retained. Unrelated project.previewfirst.json
is preserved and excluded from the commit.

## Approved previews

Selection session c81b636d7ce5, fingerprint
7df145a89e9179dc4c689e1da50fede7f6d1d6360f01e05bc32db8772c4e8898;
sketch session ffd9bec27c7c, fingerprint
f9348b1d29d76b3ae1f096711093b24fe4cc250fd251544912d4b5e182057369.
Both inspected fresh with no scope violations before implementation. Approval
was given directly in chat; tool approval state was not modified.
