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
G1.2 adds src/Mod/FreeCADPlus and its src/Mod/CMakeLists.txt inclusion. Original native
application/workbench code and submodule pins remain unchanged. Do not restore old
fork modules implicitly.

## Build and validation

The native application has not been compiled locally. G1.2 script-only CMake
copy/install was verified separately with the actual module and repository helper. The official
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

A new owner build must have its executable verified before the existing desktop
`FreeCADPlus.exe - Shortcut.lnk` is retargeted. Preserve the shortcut name, set the
correct executable and working directory, reopen the shortcut and verify both.
Do not remove its previous build until the replacement has been checked. The
source-only checkout does not retarget the shortcut or constitute delivery.

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
component windows and the remaining confirmed panel actions are still pending. See the bounded contract in ARCHITECTURE.md.

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
external-parent refusal are covered. Require zero skipped cases.

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
The module contains seventeen source/test scripts; compare them with the native
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
