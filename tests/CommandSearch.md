# Command search: owner workflow test

This F033 pilot adds **Tools > Command search...**, default shortcut **Ctrl+K**,
to the source-built FreeCAD Plus. It searches registered command names, familiar
aliases and current shortcuts. This is ready for workflow feedback; it does not
complete favorites, all-workbench context explanations or physical accessibility
acceptance.

Use this checkout's development launcher:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The separately installed FreeCAD and previously published installers do not contain
this change. Evidence is under
`D:\Temp\Office-PC\freecad-plus-command-search-20260930`.
The `visual\Search-Pocket.FCStd` example contains a Body, solid and sketch for
step 2; select Profile before searching Pocket.

1. In Part, open a document and press Ctrl+K. Search **Pocket** or **Cut-Extrude**.
   The result says **Pocket (Extrude: Subtract)** and offers **Switch workbench**.
   Switching activates Part Design without creating a feature. Press Enter to run
   the selected result; the existing Extrude editor opens with Subtract selected.
2. With a Body containing a solid and a suitable sketch, select that sketch and
   repeat Pocket. Complete a cut, Undo/Redo it, save and reopen. The search entry
   should behave like the existing Pocket command.
3. Search **Boss-Extrude** for Pad, **Revolved Cut** for Groove, or **linear pattern**
   for the combined Pattern editor. The result describes its intent. Those aliases
   retain the native command's selection requirements and task validation.
4. Search **Insert Component**. This development build excludes Assembly, so
   the result explains the missing workbench and disables Run/Switch. In builds
   with Assembly, switching is offered and the result explains that an Assembly
   must be created or activated. That active-Assembly path remains unverified.
   Search itself never creates an Assembly.
5. Use Up/Down to choose results while typing, Enter to run, Tab to reach buttons,
   and Escape to close. An unmatched query shows a clear empty state. An active
   task must be finished/cancelled before launching another command.
6. Change a command's shortcut in **Tools > Customize > Keyboard**, reopen search,
   and search its new shortcut. The palette uses the existing per-user shortcut
   manager; reset/conflict handling remains in Customize. Ctrl+K can be changed
   there as **Std_CommandSearch**. Existing user shortcut assignments are preserved.

Please report whether the names, result order and keyboard handoff suit your
workflow before further refinement. Known limits: aliases cover the listed pilot
families; other workbenches must be loaded before their commands are indexed.
Generic unavailable commands use a context hint rather than a command-specific
diagnosis. There are no favorites or navigation presets in this pilot. Use Refresh
after changing selection/context while the palette is open; Run rechecks context
even without Refresh. Physical input, screen readers, localization and high-DPI
layout still need acceptance.

Automated acceptance: `TestCommandSearch` covers menu/shortcut registration,
alias identity and updated shortcuts, keyboard navigation/empty state/Escape,
explicit workbench switching, stale availability, missing-Assembly guidance, and a native
Pocket operation with subtractive editor/geometry, Undo/Redo and save/reopen.
One grouped native build passed. Final accepted results comprise 7 palette tests
in `search-final/` and 52 existing checks in `verified/` (43 Extrude task, 5 Revolve
task and 4 parameter-command tests). Use `acceptance-summary.json`; the initial
palette failures retained in `verified/` are superseded by `search-final/`.
