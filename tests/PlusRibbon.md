# Plus UI and Classic UI: owner procedure

Use this FreeCAD Plus build, rather than installed upstream FreeCAD. Run
`RunComponentDocument.ps1 -RibbonSmoke` with a fresh evidence directory and source
overlays disabled against the grouped payload. WORK_STATE records exact build and
validation status separately from physical owner acceptance.
Cold preference acceptance uses three successive fresh output directories beneath
one isolated parent: `-RibbonStartupPhase Bootstrap`, then `Plus`, then `Classic`.
The runner shares only `ribbon-user.cfg` and the expected Classic visibility file
within that parent. Do not enable source overlays for these phases.

1. A fresh configuration starts in Plus UI; an explicitly saved Classic UI choice
   remains Classic. Open Edit > Preferences > General. UI style offers Plus UI and Classic UI.
   Choose Plus UI and Apply: the ribbon replaces the workbench toolbars immediately.
   Change the selection and Cancel: the last applied style remains. Restart and
   confirm the applied preference persists. Switch to Classic UI to restore the
   native toolbar presentation and previous show/hide choices.
   Restore a saved Classic layout while Plus is selected, switch workbenches,
   and create/show a native toolbar: Classic bars must remain hidden and the
   Plus ribbon visible. With Classic selected, attempting to show the ribbon
   must leave it hidden. Neither style may display both presentations.
2. Design shows Home, Modeling, Surface, Sketch, Assembly, Mesh and View. The
   common small File/Edit/Clipboard bar stays above the ribbon in every mode/tab.
   Design Home, Modeling, Sketch, Assembly and View follow the exact owner layouts in
   `ai-instructions/ui/TOOLBARS.md` and the canonical Word specification. Their
   latest revisions are incorporated in the October 2 batched payload. Use the
   actual New Sketch, Attach Sketch, Edit Sketch and Add Component buttons in a
   component document; preserve task Cancel/OK, ownership, Undo and selection.
   Check button states match the native menu actions, including no document,
   missing selection and active task cases.
3. Modeling contains Sketch, Modeling, Dress-Up and Transformation sections, then
   Primitives. Linear/Circular Pattern are individual buttons; retained native
   Path/Point Pattern commands are checked independently of this ribbon layout.
   Surface/Mesh retain native groups; Sketch/Assembly follow the owner groups; View exposes fit,
   orientation and display in exactly View and Individual Views, with seven ordered
   Standard Views and seven Draw Style choices. Check each dropdown and individual
   camera button. Narrow the window and use horizontal scrolling to
   reach every section without moving the mode dropdown/tab strip.
   Primary operations (including Extrude/Revolve) share one row of large buttons,
   each spanning the three-row grid. Secondary buttons have icons only and fill
   three rows; full and medium captions have a 76 logical pixel button-width limit.
   Full icons are 40px, medium 20px, small 16px; two 38px medium buttons fit a
   column beside a 76px full button. Main uses medium buttons. New Component
   creates an unplaced embedded model and opens its editing tab; it must survive
   Undo/Redo and save/reopen with zero assembly instances.
   Help uses one dropdown. Loft/Pipe/Helix variants share menus. In Sketch,
   Auto Dimension is the primary dimension action; its dropdown offers vertical,
   horizontal, angle, radius, diameter and less common native dimension types.
   Verify full tooltips and native enabled/checked states remain available.
4. Use Draft and CAM modes, and available Assembly/Drawing/other installed modes.
   Non-Design modes have Home, Tools and View; Tools preserves workbench sections.
   FEM is conditional on the registered workbench (the initial 9/28 configuration
   has BUILD_FEM off). A registered 3D printing addon appears as a mode; an absent
   addon must not produce an empty placeholder. No addon installation is implied.
5. During New Sketch, try changing modes: keep the current task and component
   context. Cancel, change mode and return to Design. Also activate a workbench
   through the native menu/command search and check ribbon synchronization.
6. Home Main includes the Coordinate System dropdown (Coordinate System/Plane/Axis/Point);
   Structure retains Variable Set. Home Macro is a single dropdown for record, manager and direct
   execution. Verify their native enabled states and no duplicate full toolbar.
   Drawing > Tools presents Insert Default Page as a large primary button. Iconless
   native actions have ribbon-only artwork; action-state refresh must not blank it.
7. After native incorporation, Pattern offers unified linear/circular plus native
   concentric Circular, Path and Point choices. Run `testRestoredNativePatternBindings`
   for command/view-provider/task opening and cancellation, then exercise valid
   references and acceptance, Undo/Redo and save/reopen in the staged application.
   The existing ten Circular/Path/Point geometry checks do not prove GUI binding.

Automated tests share native QAction instances, invoke actual operation buttons,
exercise mode/tab routing, task blocking, native General Apply/Cancel, compound
dropdowns and Classic visibility restoration. Mocked addon discovery is evidence
for conditional mode mapping only, not acceptance of an installed printing addon.
Physical touch/keyboard, dark themes, screen-reader and multi-monitor DPI behavior
remain owner acceptance gates.

When the owner defers build incorporation, run the source-compatible tests in
`TestPlusRibbon.py` with `FREECAD_PLUS_PROFILE_SOURCE=1`, `-RibbonSmoke` and an
explicit `-TestNames` list. Exclude `testNativeGeneralPreferenceApplyAndCancel`,
which requires a runtime-loaded module, and `testRestoredNativePatternBindings`,
which requires rebuilt C++ bindings. The overlay removes the existing ribbon
object before loading source; test files/settings stay in a new evidence folder.
This verifies source against the fork's native Qt/actions without copying any
changed module into the owner build. Record source validation and deferred
build/payload acceptance separately.

Design Assembly acceptance: verify exactly Assembly and Assembly Joints with every
listed joint button, plus Insert Component, Link Arrays and Gears Joint dropdowns.
Use `testExactOwnerDesignAssemblyLayout` and
`testAssemblyMenusUseNativeContextStatesAndRouting`; verify no task-watcher errors
when leaving assembly edit mode. Routing probes verify bindings and native states,
not complete array/joint/solver geometry acceptance. Source-only checks must load
both `PlusRibbon.py` and the final `UtilsAssembly.py` when verifying the exit guard.
