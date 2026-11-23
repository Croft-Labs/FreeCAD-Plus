# Component creation and modeling task updates — November 23, 2026

All three proposals were approved together in chat: "approved. also put a note
into the feature migration...". Approval was confirmed against fresh companion
inspections; no tool approval flag was changed on the owner's behalf.

| Preview | Session | Fingerprint |
| --- | --- | --- |
| New component activation/History | `96e077810961` | `3526496763a3b1d6fc09b16449499db2f093e195c95dff548ec11b4b2b124412` |
| Remove New Body task card | `2a58ba5b7e21` | `0ec7bc653838963774b88ff82eab08f92097cd5ffa05cd36c4275b7f13a9725a` |
| Plus/Classic sketch tasks | `b886cd6595c6` | `a0c7240bf520b3d51eb0cae2df3d97e39f6c82065e156130a8b730f30a4b62d8` |

## Implemented behavior

- New File and New Component activate the created component and select History.
  New File retains its initial linked instance. New Component remains definition-
  only, including empty files and externally owned definitions. Generic definition
  factories, import and copy retain existing navigation. Classic model presentation
  stays hidden while sharing the updated active context and stored History tab.
- The native Start Part/New Body watcher registration is removed in all task modes.
  Other contextual actions and actual feature editors remain available.
- Single-sketch Modeling Tools uses Extrude and Revolve in Plus task mode. Classic
  retains Pad/Pocket and Revolve/Groove, opening shared component tasks. Subtractive
  entries select Subtract. Existing profile/target defaults and legacy native-input
  compatibility remain unchanged. Task mode is independent of toolbar/model mode.
- Future combined additive/subtractive workflows must combine their Plus task
  entries too, while retaining Classic entry points routed to the shared workflow.
  The roadmap and guidelines explicitly cover Loft, Pipe, Helix and similar work.
  No additional feature workflow is implemented by this change.

## Verification and installed screenshots

- `build-focused.json/txt`: 8/8 focused native checks passed, including creation,
  external ownership, Undo/Redo, both presentations, actual task actions, mode
  switching, generic factory preservation and task tab restoration.
- `installed-regression.json/txt`: 113/113 passed, zero failures/errors. Covers
  Components, History visibility, native creation, mixed UI modes, shared Extrude/
  Revolve, design interactions, sequential History/attachment and task visibility.
- `installed-startup.json/txt`: 5/5 separate fresh-process startup checks passed.
- `visual.json`: real installed command creation and native watcher screenshots;
  no prototype watcher replacement or widget hiding. Part002 is active on History,
  both ordered action lists are correct and New Body is absent.
- `approved-comparison.json`: the installed Plus task image is byte-identical to
  its approved preview. Classic and component images were visually inspected;
  native dock/card widths differ from their prototype capture sizes, with approved
  actions, icons and layout preserved.
- `shortcut.json` and `shortcut-target.json`: the existing desktop shortcut opens
  the installed app with explicit isolated settings and updated Python modules.

Screenshots: [New component](new-component.png), [Plus tasks](plus-tools.png),
[Classic tasks](classic-tools.png), [No New Body card](no-new-body.png).

An initial focused test observed the idle watcher before native selection updates
settled. The fixture now reproduces the selection/clear sequence used by panel Edit
and waits for the native event cycle; the final eight checks and installed suite pass.
No production hiding, polling workaround or prototype watcher was introduced.

## Build, installation and reproduction

`build.cmd` builds PartDesignGui and FreeCADPlusScripts. CMake regeneration after
test registration rebuilt dependent native targets; `build.log` and `build-final.log`
record the successful builds (trailing log whitespace normalized for Git).
`install.py` verifies script source/build hashes and all build/install hashes.
`install-manifest.json` records eight Python files and eleven native dependency/
PartDesign outputs, with original rollback paths. Loaded originals are retained
when replacing binaries so existing owner processes need not be stopped.

Use `run-validation.py regression --repair` for focused build checks,
`regression --installed` for the installed suite, `visual --installed` for native
screenshots, and `regression --installed --ui-modes` for fresh startup checks.
The runner enforces a 420-second deadline and 120-second inactivity limit.
All validation uses task-specific profiles and synthetic documents under
`C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/validation/component-task-updates-20261123`.

`restart-shortcut.ps1` verifies the existing shortcut target and launches an isolated
instance; it does not close owner sessions. Existing processes must be saved and
restarted to load cached DLL/Python changes. `cleanup.ps1` checks resolved paths and
reparse points before removing generated fixtures and archived screenshots, retaining
`install-backup` and the running `profile-shortcut`. `cleanup.json` records removal.
Unrelated untracked `project.previewfirst.json` is preserved.
