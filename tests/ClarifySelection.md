# Clarify Selection: owner workflow test

This F037 increment improves the existing **Clarify Selection** command
(`Std_ClarifySelection`, shortcut **G, G**). It uses the native ray-pick and
selection system; it does not add a second picker or modify model geometry.

Use this checkout's development build:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The separately installed FreeCAD and published installers are unchanged.

1. Place the pointer over overlapping shapes and press **G, G**, or use Clarify
   Selection from the native 3D-view context menu at that location.
2. Choose a category such as **Face** or **Object**. Candidates retain their label
   and show `[document#root.occurrence.path.]` context. Hover a candidate to preview
   that exact element or whole occurrence; its tooltip includes the full path.
   Larger lists retain the native per-object submenus, now with distinct paths.
3. Pick the rear face or the intended repeated occurrence. Equal labels and equal
   face numbers on different objects no longer collapse into one candidate.
   Acceptance **adds** to existing selection, preserving native collector behavior.
   Clear selection beforehand if you want only the new target.
4. Open the menu again, hover another entry, then press **Escape**. The existing
   selection stays unchanged and the transient highlight clears.
5. When a modeling command installs a native selection gate, only allowed candidate
   roles appear. A face-only gate omits whole objects; an object-only gate still
   offers whole objects derived from face hits. If nothing passes, the disabled
   message explains that the current selection filter excluded all candidates.
   Leave the owning command to restore its normal selection policy.

Ordering remains the native type, label and internal-path grouping, not a nearest-
depth ranking. Ray picking includes obstructed geometry that participates in the
rendered scene; intentionally hidden objects are not made pickable. Existing scope,
selection-gate resolution and navigation shortcuts remain owned by their native
services. The menu does not create, replace or remove a command's gate. Eligibility
and root object identity are checked again for hover and acceptance, including
deletion/recreation with the same name while the menu is open.

No model/property/visibility changes or Undo entries are created. Save/reopen
preserves native occurrence links and placements; menu state is transient.
Bounded session entity filters (F035) are now available; see
[Selection filters](EntitySelectionFilter.md). Separate object categories,
new assembly scopes (F036), depth ranking,
live menu rebuilding after topology changes, and physical/high-DPI/mouse-preset
acceptance remain open. Full F037 is not claimed complete.

`TestClarifySelection.py` drives the native ray picker and Qt menus for equal-label
roots, exact hover/accept, additive selection, Escape, face/object/reject gates,
changed gates, deleted/recreated objects, and repeated nested Links with reopen.
Both implementation tasks preceded one FreeCADGui/FreeCADGui_Resources Release
build, exit 0. Evidence: `D:\Temp\Office-PC\freecad-plus-clarify-selection-20261001`.
Initial `grouped/` stopped before any tests because the PySide compatibility wrapper
has no QtTest export. The test now imports the bundled PySide6 QtTest (PySide2 fallback);
no implementation change or second build was needed. `grouped-native/` passes all
seven native Clarify Selection checks and nine temporary-display regressions:
**16 selected passes**, zero failures/errors/skips, native exit 0. Five `visual/`
captures were reviewed: equal-label face choices, rear-face highlight, face-only
filter, all-filtered explanation and distinct repeated occurrence paths.
Overlapping-Equal-Labels.FCStd and Overlapping-Occurrences.FCStd are owner fixtures.
The native picker exposes Front/Rear Face5/Face6 separately and Assembly.First. /
Assembly.Second. as separate whole occurrences. Exact hover/accept, additive
selection, Escape preservation, face/object/reject gates, changed-gate refusal,
deleted/recreated-name protection and native Link save/reopen pass.
FreeCADGui SHA256: `19FE903A46ABEFC2A34F0AECBA86F2BAA6C331A2663685C0DD797032A1EF80C8`.
validated-identities.json and acceptance-summary.json identify exact source/runtime
and accepted evidence; the historical About stamp is not this source identity.
No installer/release update. Full F037 remains open for broader topology/live-menu
changes and physical/high-DPI/navigation-preset acceptance. Global filter controls
(F035), new selection scopes (F036) and depth ranking are separate work.
Stop at this functional checkpoint for owner testing and rotate to another family.
