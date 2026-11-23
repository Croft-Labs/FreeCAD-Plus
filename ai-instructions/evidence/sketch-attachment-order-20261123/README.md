# Attach Sketch sequential-order repair — November 23, 2026

The owner reported creating a sketch, then a plane, and successfully attaching the
earlier sketch to that later plane. They identified the button as
`Sketcher_MapSketch`. Required behavior: reject the later input before changing
attachment, instruct the user to reorder History, and allow retry after reordering.
This repairs the approved strict sequential-input contract; no task layout changes.

## Cause and repair

The native command's circular-dependency test did not enforce History position.
Assigning `AttachmentSupport` then made the topologically sorted History move the
sketch after its support, concealing the original forward reference. The shared
Plus placement task already guarded later picks; the native command path bypassed it.

`CmdSketcherMapSketch::activated` now uses `Gui::componentGeometryError` after the
existing sketch is identified, before offering attachment modes, and rechecks before
mutation. Rejection preserves support, map mode, placement, History and Undo count.
The message names the input and sketch and says: "Reorder History to put the input
before this feature, then try again."

Sketch `AttachmentSupport`/`Support` and managed placement-reference properties also
join the native property-dialog admission guard via `geometry.is_component_input_property`.
Unrelated properties retain their existing behavior; this does not apply Part-only
ownership restrictions to sketches. Classic non-Plus documents retain native attachment.

## Evidence

- `baseline-failure.txt`: the unchanged installed native command accepted the later
  support without an order warning in the regression fixture.
- `build-focused.json/txt`: 67/67 native build checks passed, including the actual
  `Gui.runCommand('Sketcher_MapSketch')` path, rejection before the attachment-mode
  dialog, explicit plane reorder and successful retry, Undo/Redo, the managed sketch
  task route, the support-property dialog, and classic document compatibility.
- `installed-broad.json/txt`: 217/217 regression checks passed against the installed binaries.
- `installed-startup.json/txt`: 5/5 separate fresh-process startup checks passed.
- `visual.json/txt` and [native warning screenshot](attach-sketch-rejected.png): the
  actual installed command's warning, captured while running reject/reorder/retry.
  Native SketcherGui and PartGui module paths are recorded to distinguish installed
  binaries from the development build. This is an actual widget, not a mockup.
- `install-manifest.json`: source/build/install hashes for three Python files and
  build/install hashes for nine linked native outputs. Original and loaded images
  are retained under the runtime's task-specific `install-backup` directory.
- `shortcut.json` / `shortcut-target.json`: the existing desktop shortcut launches
  the updated installed app with explicit isolated user/system/data settings.

The first installer attempt discovered that build modules live under `Mod/...`
while the installed runtime uses `lib`. One misplaced task-created Materials.pyd
was verified against the build hash and moved to backup; all final destinations
were then preflighted and hash-verified. Automatic review rejected the initial
unbacked deletion proposal; the checked backup move was approved and completed.

The owner's existing regular-profile process was left running with its existing
loaded images. No owner document or profile was used for validation or closed.
**That session must be saved and restarted to load the native fix.** A separate
isolated shortcut launch verifies the installed result without disturbing it.

## Reproduce

`build.cmd` builds FreeCADGui, SketcherGui and FreeCADPlusScripts in the existing
external runtime. `run-validation.py regression` runs focused build checks;
`--installed --broad` runs the installed broader suite, and `--installed --ui-modes`
runs fresh startup checks. `run-validation.py visual --installed` captures the
warning and repeats the exact native command case. All launches have isolated
profiles, finite deadlines and inactivity limits. `cleanup.ps1` removes only
verified task-generated temporary fixtures after evidence is archived, retaining
rollback files and the restarted shortcut profile.

Unrelated untracked `project.previewfirst.json` was preserved.
