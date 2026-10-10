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
must match. Changes from upstream-1.1.4 are restricted to AGENTS.md, .gitignore and
ai-instructions for this source-only baseline task; no original source, workbench,
build definition or test is changed. The old fork's extra modules are absent.

## Build and validation

The source checkout has not been configured or compiled locally. The official
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
