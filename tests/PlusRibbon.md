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
2. Design shows Home, Modeling, Surface, Sketch, Mesh and View. Home has File,
   Edit, Clipboard, Structure, Sketch, common Tools and Help sections. Use the
   actual New Sketch, Attach Sketch, Edit Sketch and Add Component buttons in a
   component document; preserve task Cancel/OK, ownership, Undo and selection.
   Check button states match the native menu actions, including no document,
   missing selection and active task cases.
3. Modeling starts with Modeling, Transformation and Dress-Up sections, with
   helpers following. Native grouped operations keep their dropdown choices.
   Surface/Sketch/Mesh show their native toolbar groups; View exposes fit,
   orientation and display. Narrow the window and use horizontal scrolling to
   reach every section without moving the mode dropdown/tab strip.
4. Use Draft and CAM modes, and available Assembly/Drawing/other installed modes.
   Non-Design modes have Home, Tools and View; Tools preserves workbench sections.
   FEM is conditional on the registered workbench (the initial 9/28 configuration
   has BUILD_FEM off). A registered 3D printing addon appears as a mode; an absent
   addon must not produce an empty placeholder. No addon installation is implied.
5. During New Sketch, try changing modes: keep the current task and component
   context. Cancel, change mode and return to Design. Also activate a workbench
   through the native menu/command search and check ribbon synchronization.

Automated tests share native QAction instances, invoke actual operation buttons,
exercise mode/tab routing, task blocking, native General Apply/Cancel, compound
dropdowns and Classic visibility restoration. Mocked addon discovery is evidence
for conditional mode mapping only, not acceptance of an installed printing addon.
Physical touch/keyboard, dark themes, screen-reader and multi-monitor DPI behavior
remain owner acceptance gates.
