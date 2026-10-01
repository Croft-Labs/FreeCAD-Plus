# Command search: owner workflow test

This F033/F123 pilot adds **Tools > Command search...**, default shortcut **Ctrl+K**,
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
4. Search **Insert Component**. The current local development build includes Assembly.
   Switching is offered and the result explains that an Assembly must be created
   or activated. Search itself never creates an Assembly. Builds without Assembly
   explain the missing workbench and disable Run/Switch.
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
diagnosis. There are no favorites or navigation presets in this pilot. Availability and active-document text refresh while the palette is open; Run
rechecks context immediately. Use Refresh to reload the command/shortcut catalog. Physical input, screen readers, localization and high-DPI
layout still need acceptance.

Automated acceptance: `TestCommandSearch` covers menu/shortcut registration,
alias identity and updated shortcuts, keyboard navigation/empty state/Escape,
explicit workbench switching, stale availability, missing-Assembly guidance, and a native
Pocket operation with subtractive editor/geometry, Undo/Redo and save/reopen.
One grouped native build passed. Final accepted results comprise 7 palette tests
in `search-final/` and 52 existing checks in `verified/` (43 Extrude task, 5 Revolve
task and 4 parameter-command tests). Use `acceptance-summary.json`; the initial
palette failures retained in `verified/` are superseded by `search-final/`.


## F123 local help and accessibility batch (phase 10, tasks 10.9a/b)

1. Open **Tools > Command search** with Ctrl+K. Search **Pocket**, then press F1
   or **Local help**. Read selection, operation, Cancel/Undo and limitation guidance
   in the lower pane. The guide works offline and does not run the command.
2. Search **copy sketch**, **move component**, **document updates**, **export STL**
   or **mesh preparation**. Thirteen curated command entries have local guides;
   other commands explicitly show their native description and a fallback notice.
   Wrong-workbench results keep the guide readable and offer an explicit switch.
3. Use F1 to toggle the guide and Ctrl+L to return to the search field. Tab reaches
   results, the scrollable guidance pane and buttons. Arrows/Page Up/Page Down read
   the guidance pane; Enter there does not run a modeling command. Enter in the
   search/results runs the selected command. Escape closes the palette.
4. Drag the divider to give the guide more space, resize the window, and try your
   normal enlarged application font/display settings. **Reset layout** restores
   this window's size and divider, hides extended help and focuses search. It keeps
   the query, application fonts, customized shortcuts and document intact.
5. Switch/close the active document while search is open. The context/availability
   updates automatically; the guide is still readable. "Available to open" means
   the command can be invoked; its own editor validates the actual inputs.

Current evidence: `D:\Temp\Office-PC\freecad-plus-command-help-20261001`.
The two tasks preceded one successful FreeCADGui_Resources build/staging pass;
no native C++ recompilation was needed. Initial `grouped/` has seven passing
DocumentUpdates tests and ten of eleven CommandSearch tests; F1 failed its
keyboard check. The Python correction was restaged without another build.
`help-verified/` passes all eleven, including the native Pocket task, geometry,
Undo/Redo and reopen. Visual review found the inherited font was overridden by
application styling; the stress check now verifies actual rendered 20-point text.
`enlarged-verified/` is the final eleven-test result. Eighteen distinct selected
checks pass across accepted suites; zero failures/errors/skips in accepted suites.

`visual-accepted/` contains six reviewed captures and `Command-Help-Example.FCStd`.
The initial `visual/` captures remain as evidence of the ineffective inherited-font
stress setting. Whole F123 remains open: keyboard modeling/downstream task coverage,
physical keyboard/screen-reader and multi-monitor/high-DPI acceptance, localization,
all-command explanations and unified workspaces. This is ready for your workflow
feedback, with no installer or release update. Stop here and rotate families.
