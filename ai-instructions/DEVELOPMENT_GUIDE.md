# Development guide

## Checkout and remotes

Workspace: `C:/Users/GAMING-PC/Documents/__Apps/freecad`.
Branch: `codex/freecad-1.1.4-baseline`.
Official baseline: tag `1.1.4`, commit `4fd3bf320d9566a27e60069fc8387448aaa3a094`.
Local upstream tag alias: `upstream-1.1.4`.
Origin is Croft-Labs/FreeCAD-Plus; upstream is FreeCAD/FreeCAD. Never push to upstream
or force-push. The old main history and archive tag remain available for reference.

## Source verification

Use Git status and recursive submodule status. All release-pinned submodule commits
must match. The original baseline overlay changed only AGENTS.md, .gitignore and ai-instructions.
G1.2 adds src/Mod/FreeCADPlus and its src/Mod/CMakeLists.txt inclusion. G1.6b adds
bounded native per-view context and editing integration. Original workbench source
and submodule pins are retained. Do not restore old fork modules implicitly.

## Build and validation

A bounded native development build passed for G1.6b; WORK_STATE records its targets
and runtime resources. It is not a complete owner package. G1.2 script-only CMake
copy/install was also verified separately with the module and repository helper. The official
portable binary matching this revision has undergone light runtime checks; see
[WORK_STATE](WORK_STATE.md#stable-baseline-inventory-and-light-runtime-check--october-10-2026)
for provenance, installed location, inventory and the completed light display check.
Use this release's
[CMakeLists.txt](../CMakeLists.txt), [presets](../CMakePresets.json) and
[Windows workflow](../.github/workflows/sub_buildWindows.yml) to establish a compatible
build environment when requested. Old build commands, dependency versions and output
paths in the archived guide are evidence, not automatically valid for 1.1.4.

Build trees/dependencies: `C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds`.
Validation output: `C:/Users/GAMING-PC/Documents/_temp/freecad/validation`.
Existing owner builds and settings remain associated with the old fork. Keep a new
baseline build separate. Batch related work before costly builds and record actual
validation in WORK_STATE/roadmap, then remove task-generated validation output.

For isolated runtime checks, create a task directory under the validation root
with its own profile and temp directories. Supply `FREECAD_USER_HOME`,
`FREECAD_USER_DATA` and `FREECAD_USER_TEMP` only to the test process, plus explicit
`-u <profile/user.cfg>` and `-s <profile/system.cfg>` arguments. Run the exact
baseline executable, not an installed FreeCAD or archived Plus payload. A temporary
`.FCMacro` can perform bounded modeling/persistence checks through the real GUI.
Handle first-use welcome dialogs in that profile. Verify visual results separately:
a successful image-save call is not proof of on-screen rendering.

## Viewport capture validation

On the tested FreeCAD 1.1.4 / Qt 6.8.3 / NVIDIA 560.94 configuration,
`QOpenGLWidget.grabFramebuffer()` reproduces corrupted captures while the normal
viewport buffer is clean. `QWidget.grab()` is also unsuitable as sole evidence.
Do not mistake a successful capture call for correct visible rendering or a bad
capture for a confirmed application display defect.

For a diagnostic through the application's GUI thread:

1. Allow normal paint events to complete after camera, workbench or size changes.
   Select the visible viewport's QOpenGLWidget, not a small helper widget.
2. Call `makeCurrent()` and verify the bound framebuffer matches that widget's
   `defaultFramebufferObject()`. Record renderer, dimensions, pixel ratio and errors.
3. Read its existing color buffer using `glReadPixels` into an RGBA8888 image at
   physical pixel dimensions. Use known pixel-pack alignment/row/skip settings,
   preserving previous state, and flip the OpenGL bottom-up rows for inspection.
   Do not call `grabFramebuffer()` or force a special capture redraw first.
4. Release the context, inspect the captured pixels and compare repeated settled
   frames. Exercise rotation, zoom, resizing and workbench transitions separately.
5. If comparing a suspect capture method, bracket it with normal buffer reads.
   Record what was established and distinguish this from physical monitor capture
   or a manual interaction/performance test.

The implementation hook is [CustomGLWidget::paintGL](../src/Gui/Quarter/QuarterWidget.cpp):
widget capture can invoke an additional redraw. [Qt's QScreen documentation](https://doc.qt.io/qt-6.8/qscreen.html#grabWindow)
also explains why desktop-region captures can include covering windows. An occluded
screen capture is not evidence of the target application's viewport. Keep all raw
diagnostic output in the designated validation directory and remove it after recording
results. Do not alter renderer defaults or drivers solely to repair a capture tool.

## Owner delivery

The owner's October 11 decision supersedes the earlier retargeting instruction:
preserve `FreeCADPlus.exe - Shortcut.lnk` and its archived-fork build for reference.
The separate desktop `freecad plus 0.1.0.lnk` targets the latest development build.
Verify the executable, then reopen the saved shortcut and verify target and working
directory after updates. Preserve unrelated shortcuts. This development shortcut
does not imply completed packaging, automatic panel startup or Group 1 acceptance.

## Component pilot validation

The pilot is opt-in; it does not replace File > New or the original workbenches.
In an isolated FreeCAD 1.1.4 GUI test process, add this checkout's
`src/Mod/FreeCADPlus` to `sys.path`, set `sys.dont_write_bytecode = True`, and set
`PLUS_TEST_DIR` to a task directory under the validation root. Set the profile
variables described above before launch. Run:

```python
import unittest
import TestComponentPilot
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestComponentPilot.TestComponentPilot)
result = unittest.TextTestRunner(verbosity=2).run(suite)
assert result.wasSuccessful()
```

In a second isolated process with the same output directory and module path, run
`TestComponentPilot.verify_fresh_process(output_directory)`. It checks the first
process's saved fixture and writes a separate edited file. Without PLUS_TEST_DIR
the suite skips instead of writing fixtures into an owner profile or checkout.

For the native editor check, use `document.new_document()`,
`editing.new_sketch(doc)` and a closed native sketch; enter/exit its original
Sketch editor, select it and invoke `Gui.runCommand("PartDesign_Pad")`. Accept the
existing task's OK button and check valid shape, Body Tip and component ownership.
Use the normal framebuffer procedure above for visual evidence. These adapters
require explicit component Edit and do not globally intercept unrelated commands.

CMake includes the script module when Part, PartDesign and Sketcher are built.
The standalone packaging check uses a temporary `project(... LANGUAGES NONE)`
with `include(AddFileDependencies)`, the repository's FreeCadMacros.cmake, and
`add_subdirectory` pointing to src/Mod/FreeCADPlus. Build FreeCADPlusScripts and
install under the designated test-builds root; compare all copied files to source.
This does not constitute a full native application build or owner delivery.

## Legacy conversion validation

Use the same isolated GUI profile/module-path setup as the pilot. Set PLUS_TEST_DIR
to a fresh task directory under the validation root; conversion deliberately refuses
existing destinations, so do not reuse earlier fixture outputs. Run TestLegacyConversion
alongside TestComponentPilot with unittest. In a second process, run
`TestLegacyConversion.verify_fresh_process(output_directory)` against those fixtures.
The cases include an open source with unsaved edits, expressions, origin attachment,
placement, native IDs, Undo/Redo, curve/empty files, fallback reporting and failures.

The opt-in entry point is:

```python
from freecad_plus.conversion import convert_file
converted_doc, report = convert_file(source_fcstd, new_cadprt_path)
```

Only explicitly requested standalone shape recovery uses
`allow_geometry_fallback=True`; inspect report["warnings"] and the persisted file-root
ConversionReport. Never bulk-convert owner files as a test. Supported structures and
schema/identity boundaries are in ARCHITECTURE.md. The destination's filesystem must
support an exclusive hard link for publication; failure never replaces an existing
file. Full conversion UI and remaining unsupported graph cases are separate work.

## Hierarchy validation

Run TestComponentHierarchy together with TestComponentPilot and TestLegacyConversion
in an isolated GUI process and fresh PLUS_TEST_DIR as described above. In a second
process, run `TestComponentHierarchy.verify_fresh_process(output_directory)`.
It reopens both new and legacy-converted hierarchies and verifies shared edits,
identity, placement and source preservation before saving separate edited files.

The service entry points are `hierarchy.create_definition`, `add_instance`,
`move_instance`, `resolve` and `world_placement`. Use `editing.edit((root_link,
child_link, ...))` for nested Edit; bare nested links are deliberately ambiguous.
Use `editing.context_path(doc)` when a caller needs the complete occurrence.
Older schema files require explicit `hierarchy.upgrade(doc)` before hierarchy
mutations; opening/saving alone never upgrades them.

For native GUI acceptance, select the second root occurrence's child with Edit,
then call `Gui.activeDocument().setEdit(file_root.Name, 0, subname)` using the full
link path followed by Body and Sketch/Pad names. Check getInEdit, close with native
resetEdit, and confirm the occurrence context and geometry remain intact. Inspect
normal framebuffer pixels with the existing capture procedure. Script build/install
checks use the same standalone CMake harness; no native recompilation is required
for this module-only change. Do not treat these checks as full panel delivery.

## External-definition validation

Run TestExternalDefinitions with the preceding three suites in the same isolated
GUI process and a fresh PLUS_TEST_DIR. Then run
`TestExternalDefinitions.verify_fresh_process(output_directory)` in a second process.
It reopens nested native references, checks source identities/object IDs, edits/saves
only the defining file and verifies that reopening the unchanged assembly receives
the saved update. It changes a generated Pad from 5 to 8 mm; use fresh suite output
before repeating this fresh-process acceptance helper.

Create/save the two component documents before `external.import_file(importer,
source_doc)`. Importing does not place geometry; use `hierarchy.add_instance` explicitly.
Older files require `external.upgrade(doc)` before importing. `external.catalog` and
`qualified_label` supply the panel projection. `editing.edit` accepts a full path
across files; Sketch/Pad creation writes to the resolved defining document.
`external.save_definition` saves that owner. Save source definitions/catalog changes
before dependents that reference those new entries. Do not use assembly Save as an
implicit save-all operation. Full contracts/limits are in ARCHITECTURE.md.

For independent copies, provide destination names and an explicit
`placements_to_replace` tuple; do not infer the user's future checklist selection.
The native recursive copy must have no surviving source dependencies. Copy failure
rolls back the destination transaction. Missing-file recovery is restoring the exact
source path/identity then retrying; no automated relocation or name substitution.

For the native editor check, use the saved external-edit fixture's second full
occurrence path followed by the source Body and Sketch/Pad names in the existing
`setEdit(file_root.Name, 0, subname)` procedure. Confirm the current assembly tab,
resolved source feature and occurrence context survive `resetEdit`. When capturing,
import PySide6.QtOpenGLWidgets before querying widgets and restrict the normal
framebuffer read to QOpenGLWidget descendants of the active QMdiSubWindow; another
native editor window can also have an OpenGL widget. These are service/editor checks,
not acceptance of the full panel, mouse-driven flows or long-session jitter.

## Component panel foundation validation

Use the same isolated GUI runtime/profile and a fresh PLUS_TEST_DIR. Run
TestComponentPanel with TestComponentPilot, TestLegacyConversion,
TestComponentHierarchy and TestExternalDefinitions. The panel suite uses PySide6
QtTest mouse events and native document APIs; it requires the actual GUI runtime.
It checks selection versus Edit, occurrence memory, native external ownership,
file-origin visibility, Undo/save/reopen and observer lifecycle. An initial visibility
fixture must explicitly hide the plane as well as its parent Origin before testing
Show; the child's authored visibility can remain true while the Origin is hidden.

The panel is explicitly enabled from the module path with:

```python
from freecad_plus import panel
components = panel.show_panel()
```

It is not installed into an owner executable or automatically enabled at startup.
Closing it unregisters observers; calling show_panel again creates one fresh dock.
Do not hide/remove the legacy tree to make screenshots imply completed replacement.
Domestic and external unused-model Edit are supported in the native context build;
component tabs use additional native views. Other confirmed panel actions remain
separate increments. See the bounded contract in ARCHITECTURE.md.

For a fresh-process visual check, open the generated Panel.cadprt from the visibility
persistence case, show the panel and edit the second shared-child occurrence. Inspect
Models, Part Tree and History, then File Edit History. Compare document object IDs
and Undo count before/after presentation. QWidget.grab on the non-OpenGL Components
dock captures these controls; the viewport itself still requires the separate normal
framebuffer procedure. Inspect saved panel pixels, not just image-save success.

Panel construction is script-only. Use the existing CMake copy/install harness and
compare all module files. Do not treat passing panel tests or packaging as owner
shortcut delivery, completion of G1.6/G1.7, or long-session jitter acceptance.

## Unused-model validation

Use the native development build with `view.setDocumentContext`; the original
binary cannot validate external unused editing. Include TestUnusedModels with the
preceding five suites in an isolated GUI process and a fresh PLUS_TEST_DIR. Its
nine cases cover domestic/external Edit, native viewport picking, temporary rows,
assembly hiding/restoration, History opening Sketch/Pad editors, accepted Pad
Undo/Redo in the defining file, save during isolation, per-view state and cleanup.
Source closure during a native editor, removed imports, unrelated roots and ordinary
external-parent refusal are covered. Require zero skipped cases. Camera tests disable animation on their test-owned view
before rotation/fitAll: a pending native rotation can otherwise overwrite the fitted
camera/clipping range and make geometry disappear. Do not change owner preferences.

In a second process run `TestUnusedModels.verify_fresh_process(output_directory)`
and `TestUnusedModels.verify_external_fresh_process(output_directory)`. They compare
native identities and saved visibility/link inventory, edit a reopened Pad, and
verify the external source saves without changing the assembly archive. The external
check reopens again to prove the source-only edit persisted.

For display acceptance, open Unused.cadprt from the modeling/Undo case. Capture the
normal framebuffer in File Edit, then Edit of its unused definition, then File Edit.
The assembly has two small cylinders; isolation shows only the larger unused
cylinder; exit restores the two originals. Inspect the Part Tree capture for the
last temporary row, active fill and gray selectable assembly rows. A theme can
provide identical active/disabled palette colors, so inspect pixels as well as row
brush state. Use the existing native framebuffer procedure, not grabFramebuffer.
Inspect the external qualified temporary row and the viewport while native Sketch
and Pad editors are open; check that a shortened Pad preview has no stale solid.
The module contains twenty-four source/test scripts; compare them with the native
build's copied module payload.

The bounded native build uses this release's pinned Windows LibPack and the release
preset. Build the application, PartGui, SketcherGui, PartDesignGui and corresponding
script targets, including FreeCADPlusScripts. Required runtime data also includes
FreeCADGui_Resources, Stylesheets_data, Show, MaterialScripts, MaterialToolsLib,
MaterialLib, FluidMaterialLib, AppearanceLib, PatternLib, MachiningLib,
MaterialModelLib, PartDesignHole and WizardShaft. Library compilation alone does
not populate these data targets. Keep all workbench configuration/source intact;
a targeted developer build is not a complete owner package or workbench inventory
acceptance. WORK_STATE owns the current paths, toolchain and actual build results.

## Component-window validation

Run TestComponentWindows with the preceding six Group 1 suites in the isolated
native development runtime/profile. Its six GUI cases exercise both context menus,
exact/remembered occurrence routing, original camera/context preservation, child
Edit without another tab, native editor/stale-row/stale-menu guards, failed-entry
rollback, independent unused isolation, view/source closure, event-driven titles and
panel reopening. External Sketch/Pad creation and native editing stay source-owned;
no App objects or opening-related Undo entries are introduced by the extra view.

Run `TestComponentWindows.verify_fresh_process(output_directory)` against the
combined run's fixtures in a second process. It verifies native identities, absence
of saved isolation, and source-only Pad save/reopen with an unchanged assembly file
checksum. After a hidden process launch, use an explicit hide/showNormal transition and
confirm the test window is exposed before accepting normal rendered pixels. Inspect
normal framebuffer captures for domestic/external component tabs
and the restored original view, plus dock/tab-bar captures for active labels and
History. Update only FreeCADPlusScripts when native sources are unchanged; compare
the copied twenty-four-script payload. This does not deliver an owner build or complete
remaining panel actions, contextual display or responsiveness acceptance.

## Linked-instance Copy/Paste validation

Run TestComponentClipboard with the preceding seven Group 1 suites in the isolated
native development runtime. Six cases exercise real context menus and scoped
Ctrl+C/Ctrl+V, shared geometry and later independent placement movement, parent/child
selection normalization, copied placement/visibility/LinkTransform snapshots, one
Undo/Redo for a batch, cycle/import preflight, late transactional rollback, external
parent ownership, stale menus/source closure and native-editor/pending-transaction
guards. The clipboard is session-only and does not serialize or clone definitions.

Run `TestComponentClipboard.verify_fresh_process(output_directory)` in a second
process against the combined run's fixtures. Check native IDs, unchanged definition
inventory, shared links and placements after reopen. An external parent's pasted
child is saved/moved in its source file without changing the importing assembly's
archive checksum; a second reopen must retain that move. Inspect the saved three
shared-geometry occurrences, expanded Part Tree and real Copy/Paste menu. Disable
animation on test-owned cameras before fitting and use the exposed-window/normal
framebuffer procedure above. Native delayed SyncView selection must settle before
the unrelated document-switch scenario in TestComponentPanel; do not change the
owner's SyncView preference to make tests pass. Update only FreeCADPlusScripts and
compare all twenty-four packaged Python files. No owner delivery is implied.

## Move Components Translate validation

Run TestComponentMove with the preceding eight Group 1 suites in the isolated native
runtime and a new PLUS_TEST_DIR. Its six cases cover the actual Part Tree menu and
Tasks Apply button, transient preview, rotated parent frames, shared children,
rigid sibling movement, direction snapshots/curve rejection, source-owned external
save, persistent selection, list Delete/Remove/Clear, invalid native length input,
method reset, expression/read-only guards, late rollback and task lifecycle cleanup.
Native origin axes are infinite edges: use their tangent rather than assuming
endpoint vertices. Include hidden-reference/occurrence and qualified model-label checks.
Use the quantity widget's `rawValue` property; a dynamic `value` property does not
emit native input signals. Delete must accept ShortcutOverride inside the collector
so the global document Delete command cannot consume it. Native task closure owns
and clears its form. File Edit is valid movement context but deliberately invalid
for the modeling-only `editing.context_path` adapter.

In a second process run `TestComponentMove.verify_fresh_process(output_directory)`.
Check exact domestic/external identities, saved group placements and source-only
save with unchanged assembly checksum; reopen the parent independently as well as
through its assembly. Inspect the real Tasks controls, settled native framebuffer
preview of shared parent occurrences, committed movement and Cancel cleanup. Use
the exposed-window capture procedure and disable animation only on test-owned views.
After Tasks closes and changes viewport layout, request normal view.redraw before
reading its settled buffer; a freshly cleared buffer is not visual acceptance.
Drain delayed native SyncView selection before creating each independent panel fixture.
Only the existing FreeCADPlusScripts copy target is needed for these script changes;
compare all twenty-four Python files with the native development payload. This is
not owner-build delivery, all six Move workflows or complete Group 1 acceptance.

## Move Components Rotate validation

Run TestComponentRotate alongside TestComponentMove first, then the preceding eight
Group 1 suites in the isolated native development runtime. Cover actual task input
and Apply, non-origin pivots, located references under rotated shared parents,
two-point/reversed axes, circle centers/origins, reference snapshot stability,
nonaccumulating preview, rigid relative placements, Translate/Rotate switching,
invalid angles, late rollback, no-op full turns, Undo/Redo and persistence.

Run `TestComponentRotate.verify_fresh_process(output_directory)` in an independent
process. Verify exact IDs, rotated positions/orientations, unchanged feature geometry,
and the external parent opened independently and through the unchanged assembly.
Inspect normal framebuffer pixels for the located arrow/pivot and shared previews,
Cancel cleanup and committed rotation, plus native task fields/units. Retain existing
exposed-window, native redraw and test-camera settling procedures. Tasks focus can
leave activeSubWindow empty: find the MDI subwindow owning the model graphics view
when capturing its normal framebuffer. Compare all twenty-four Python files with the copied script payload. No additional native build
or owner delivery is implied; do not start Point to Point after these checks.

## Saved component display-state validation

Run TestComponentDisplay with the affected pilot, conversion, hierarchy, external,
panel and clipboard suites in the isolated native development runtime. Six new
cases cover real nested menus, self/direct-child ownership, context restoration,
source-owned external writes, schema-4 read-only defaults and undoable upgrade,
Excluded/Shown refusal, stale contexts, rollback, copies and persistence. Then run
`TestComponentDisplay.verify_fresh_process(output_directory)` once independently,
and inspect checked Part Type/Visibility menus. Compare the twenty-four Python
files with the copied payload. This state-only increment requires no new viewport
rendering test; native Visibility/geometry must remain unchanged. Filtering, fading
and eligibility tests belong to the next viewport integration increment. Repeat
only failed/affected checks after a correction; do not rerun completed acceptance
without a new material concern.

## Per-view explicit hiding validation

Build `FreeCADGui` and `FreeCADPlusScripts` in the retained native development tree.
On Windows first call the installed VS 2022 BuildTools `VsDevCmd.bat -arch=x64
-host_arch=x64` in the same command environment; a plain shell lacks the MSVCRT.lib
link search path. Keep helper scripts/logs in the task validation directory. Compare
all twenty-five module Python files with the copied payload after the script target.

Run TestComponentVisibility in an isolated native process. It covers whole-occurrence
ray picking, independent view contexts, Hidden/Excluded/nested Reference, Undo,
recompute, invalid paths, unused isolation, panel/view close and reopening. Run only
relevant existing panel/window/unused-editor/saved-state cases; repeat failed or
changed paths only. Run `TestComponentVisibility.verify_fresh_process(output_directory)`
once independently and inspect original, hidden, separate-view and restored normal
framebuffer captures. Explicitly expose and normally redraw the test window before
reading a buffer; a uniform unpainted buffer is inconclusive. Do not change renderer
settings to compensate for an unpainted capture. Full fading, Bodies Only, eligibility,
long-session responsiveness and owner-delivery checks are separate gates.

## Contextual fading validation

Use the same VS environment and isolated profiles as the hiding increment. Build
FreeCADGui, PartGui and FreeCADPlusScripts: sorted-transparent face material cache
dependencies live in the native Part renderer. Run TestComponentFading: it reads the already-painted normal
framebuffer and compares a single visible face with its normal and background pixels.
This avoids mistaking two transparent surfaces for a single 75% blend. Retain per-face
material arrays, compare separate-view contexts and authored 90% transparency, and
check Undo/recompute, identities, saved properties, hiding and isolation transitions.
The test leaves PNGs only in PLUS_TEST_DIR for visual inspection. Run its fresh-process
verifier once; native persisted colors are rounded 8-bit RGBA, so compare channels
within half a channel step plus float rounding, while identities and transparency
remain exact. Relevant visibility/window/unused-editor regression is proportional.
Compare all twenty-six Python files with the copied payload. Do not repeat completed
checks unless a failure, code correction or specific material concern warrants it.

## Unused-preview saved display validation

Build FreeCADGui and FreeCADPlusScripts together. Run TestUnusedModels and the
existing TestComponentVisibility cases for the shared native hiding implementation.
Cover saved self/child hiding, direct/nested Reference, source-owned external state,
Undo/recompute, separate placed/unused views, invalid paths, cleanup and idle behavior.
Native linked-document undo can create a mirrored assembly entry; verify the defining
file owns the display properties and reversal rather than assuming no mirrored entry.
Drain queued save notifications before asserting idle refresh counts.

Run TestUnusedModels.verify_display_fresh_process(output_directory) once for exact
identity, visibility and saved-filter persistence. Its capture_display_fresh_process
helper performs a separate visual check without repeating persistence assertions.
Import QtOpenGLWidgets before creating test views so PySide binds the native viewport
correctly. Explicitly expose the test main window before capture; an unpainted flat
buffer does not count as evidence. Inspect the normal framebuffer before cleanup.
Stop after affected checks pass; no unrelated suite or next-stage implementation.


## Bodies Only validation

Build FreeCADPlusScripts in the retained native development tree; this increment
changes no native libraries. Compare all 27 Python files to the copied payload.
Run TestComponentBodiesOnly with affected TestComponentVisibility/TestUnusedModels
regressions, using the same bounded isolated native process/profile convention.
The suite covers native Body history, solid/sheet retention and standalone curves,
shared/nested saved choices, external unused ownership, Undo/recompute, exact native
visibility/identity, separate views, native Sketch editing and cleanup. Expose the
normal main window so linked snapshot and paint events occur during checks.

A newly added linked child can initially lack a native detail path. The shared
filter helper synchronizes pending Coin link sensors once on that exact error and
retries once. A persistent error remains a failure; do not hide it with polling or
repeated full-suite runs. Run only failed/affected cases after a correction.

Run TestComponentBodiesOnly.verify_fresh_process(output_directory) independently.
It checks the saved fixture and captures the existing normal framebuffer in Bodies
Only and Full Component. Inspect the pair: body results remain, the edited curve
returns only in Full Component, and the repeated Bodies Only occurrence stays
filtered. Record results in WORK_STATE, delete task validation artifacts, and stop
when this increment's checks pass. Owner delivery remains a separate gate.

## Geometry eligibility validation

Build FreeCADPlusScripts in the retained native development tree; G1.7b3c changes
no C++ libraries. Parse and byte-compare all 29 Python files against that payload.
Run TestComponentEligibility plus the affected existing Move direction, Rotate
located-line/two-point and Excluded display cases, with bounded isolated native
processes/profiles. The consumer checks must reject before Part.getShape, while
actual panel Edit remains available. Native mapped element names can contain dots;
origin axes can resolve as objects without returning a shape.

After a correction, rerun only failed/affected cases. Independently run
TestComponentEligibility.verify_fresh_process(output_directory) for exact saved
identity/visibility and eligibility. Record initial failures and final results in
WORK_STATE, remove task artifacts, and stop. Remaining native consumer integration
and owner-build delivery are separate gates.

## Native export eligibility validation

Build FreeCADGui and FreeCADPlusScripts together in the retained development tree.
Run TestComponentExport with TestComponentEligibility for initial integration;
after a correction rerun only affected cases. TestComponentExport invokes Std_Export
through a bounded Qt dialog handler and an exporter probe backed by Part.export
BREP writing. The handler explicitly sets the fileNameEdit text; selectFile alone
can retain FreeCAD's suggested name in the already-open native wrapper.

Cover Reference/Excluded rejection before options/writer calls, shared eligible
occurrences, whole-file/aggregate and mixed selections, owned derived features,
external unused source routing and legacy export bypass. Verify actual BREP geometry,
not just callback counts. Independently run TestComponentExport.verify_fresh_process
against its saved fixture. Parse/compare all 30 Python payload files, record results
and remove validation artifacts. Do not repeat passed unrelated suites or begin the
next consumer integration after these checks pass. Owner delivery is a separate gate.

## Native modeling intake validation

Build SketcherGui, PartDesignGui and FreeCADPlusScripts together in the retained
native development tree. TestComponentModeling uses actual PartDesign_Pad and
Sketcher_Projection commands, not a mocked feature constructor. Run it with the
existing shared eligibility cases for the initial integration; after corrections,
rerun only affected cases. Native modal notifications are closed by a test-owned
Qt timer within the bounded isolated process.

Cover rejected shared occurrences before feature/transaction creation, accepted
native Pad and Undo/Redo, no-selection profile-picking recheck, legacy bypass,
Sketcher original-occurrence rejection without aborting the existing editor, accepted
native external geometry, and external unused/wrong-consumer context checks. Run
TestComponentModeling.verify_fresh_process independently for native Profile/Tip,
geometry, IDs and external projection persistence/downstream recompute. Choose an
edge that projects to real geometry (the cylinder rim, not its perpendicular seam),
and assert actual projected geometry as well as a surviving reference. These checks
do not establish coverage of all task-dialog reference fields or raw Python writes.

Parse and compare all 31 Python files to the native payload. Record actual results,
remove task-generated validation files, and stop once this increment's checks pass.
Owner packaging and desktop-shortcut delivery remain separate gates.

## Attachment and shared task reference validation

Batch PartGui and PartDesignGui for native collector changes, then synchronize the
FreeCADPlusScripts target. TestComponentReferences drives the native datum attachment
editor and Pad direction picker with original component occurrences. Cover initial
mixed-batch atomicity, picked and typed rejection without losing a prior reference,
Cancel and Undo/Redo, native legacy attachment bypass and allowed axis selection.
Independently reopen the saved attachment/axis fixtures, verify identities/references
and change the source/feature to prove downstream placement and geometry.

Run only affected cases after a correction; do not repeat the prior modeling/export
suites. Parse/compare the 32 Python payload files. Record exact coverage and limits,
then delete this increment's temporary validation directory. These native checks do
not validate the separate Python AttachmentEditor or every task reference control.

## Separate attachment and Extrude input validation

Batch PartDesignGui and PartScripts, then synchronize FreeCADPlusScripts. The changed
AttachmentEditor Python file is part of the Part payload, not the Plus module; compare
it separately alongside all 33 Plus Python files. TestComponentInputEditors drives
the Python task's real selection observer, preview and Apply/OK/Cancel controls and
native Pad face/shape collectors. Explicitly select Flat Face in the Python editor;
it retains Deactivated until the user chooses a mode. Check one-step Undo/Redo after
Apply then Cancel, including lazy transaction cleanup. Cover original occurrences, typed refusal before
mutation, both shape sides, legacy bypass, Undo/Redo and independent saved-file
reopen with downstream attachment placement/Pad geometry changes. Rerun only affected
cases after corrections, record actual boundaries, remove task artifacts and stop.

## Loft/Pipe input validation

Batch PartDesignGui and FreeCADPlusScripts in the retained native development tree.
TestComponentSweepInputs uses native task widgets and selection notifications for
Loft profile/sections and Pipe profile/main path, auxiliary path and sections. Check
original occurrence rejection before mutation, accepted references, removal without
new admission, Cancel, one-step Undo/Redo, ordinary legacy bypass and independent
saved-file reopen/source edits. Compare all 34 Plus Python scripts to the build
payload. Run the focused cases once; after a failure rerun only affected cases.
Record actual results, delete this increment's temporary artifacts and stop.

## Shared dress-up/transformed input validation

Batch PartDesignGui and FreeCADPlusScripts. TestComponentDressUpInputs drives native
Fillet edge toggles, Fillet/Chamfer Add All Edges/Use All Edges and shared Linear
Pattern Original collectors. Cover original occurrence rejection, removal cleanup,
missing Edit context without checkbox/property divergence, accepted inputs,
Undo/Redo, Cancel, legacy bypass and independent saved-file/source-change checks.
Use QAbstractButton for native add/remove controls (the transformation controls are
QPushButtons). Acknowledge and inspect expected modal rejections with the existing
messages() test helper, so notification preferences cannot block unattended runs.
Use the numeric value in a dimensional property's existing units for source edits.
Compare all Plus Python scripts to the retained development payload. Use the
bounded isolated native runner; rerun only cases affected by a concrete correction.
Record actual results and limits, remove task-generated artifacts, and stop.

## Dress-up/transformation command-start validation

Finish CMake/test registration and preserve stored line endings before starting
the batched PartDesignGui/FreeCADPlusScripts build; later CMake-file edits can
trigger configuration and generated GUI rebuilds. TestComponentCommandInputs covers
both shared command helpers, the separate Multi-Transform conversion branch,
unresolved mixed selections, missing Edit with empty selection, native Cancel,
Fillet/Chamfer/Linear Pattern creation and Undo/Redo, legacy bypass and Pattern feedback
routing. Its independent verifier reopens the three saved component fixtures, checks
identities/references/Tip/volumes, then changes source dimensions and recomputes.
Use the isolated bounded runner and `messages()` for expected command rejections.
A rejected command must retain object identities, selection, Tip, shape and Undo/
transaction state. Do not rerun previously passing intake suites for this increment.

## Native Boolean ownership validation

Build FreeCADPlusScripts in the retained native development tree; this ownership
change is Python-only. TestComponentBooleanOwnership drives the native Boolean
command within one component and checks accepted creation, ownership transfer inside
the component, hidden Body History projection, full-path selection and nested input
Edit/Cancel, creation Cancel, one-step Undo/Redo and rejection of unowned dependencies.
Run the affected existing panel projection and owned-feature eligibility cases once.
Its independent verifier reopens the saved file, checks exact identities, tool
ownership, History, Tip and geometry, then changes a source tool and recomputes.
These checks do not certify cross-component intake or all Boolean geometry modes.
Stop after acceptance; retain the build and clean only task-generated validation data.

## Legacy Boolean conversion validation

For Python-only conversion changes, build FreeCADPlusScripts in the retained
native development tree. With PLUS_TEST_DIR pointing to a fresh task validation
directory, run TestLegacyBooleanConversion plus the affected existing native Body
and Part/shared-link conversion cases. The new fixtures cover standalone and Part-
owned Boolean graphs, expressions, exact identities, History, shared links, source
isolation, Undo/Redo and unsupported nested-script/unowned/independent-Body rejection.
Then call TestLegacyBooleanConversion.verify_fresh_process in a separate FreeCAD
process against the saved fixtures to check persisted ownership, placements,
expressions and downstream source edits. Record durable results and remove only the
task validation directory. Passing these bounded checks closes this increment;
additional Boolean modes, deeper nesting and input policy are separate work.

## Placed external export validation

After changing native export dispatch, build FreeCADGui and FreeCADPlusScripts once.
Run TestComponentExternalExport plus the affected owned/external-unused and legacy
cases in TestComponentExport. The native Std_Export dialog is handled with the same
bounded helper and writer probe; check actual BREP output, rejected writer/options,
mixed shared occurrences and source-only payload/no catalog fallback. Then call
TestComponentExternalExport.verify_fresh_process in a separate FreeCAD process to
reopen the saved assembly/source pair and exercise allowed and rejected exports.
Record results before removing the exact task validation directory. Do not repeat
completed unrelated modeling/Boolean suites for this export-only change.

## Component rename validation

Build FreeCADPlusScripts for this Python-only panel/service change. Run
TestComponentRename with PLUS_TEST_DIR set to a fresh task validation directory,
plus the affected TestComponentWindows label-refresh case. The bounded Qt driver
uses actual Rename menu actions and the native text dialog; check shared rows,
Part001, external source ownership, Undo/Redo, same-name/cancel/invalid-name behavior,
read-only names, concurrent rename refusal and native editor protection. Call
TestComponentRename.verify_fresh_process in a separate process for the two saved
domestic/external fixtures. Record evidence, then remove only the task artifacts.
