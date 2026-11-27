# Design toolbar update — installed November 27, 2026

The [owning specification](../../ui-ux-specs/TOOLBARS_AND_BUTTONS.md#design-toolbar-simplification--approved-november-27-2026)
records the combined preview and the owner's implementation approval, including
the explicit correction to copy Boolean Tools exactly from the current Part tab.
The [reviewed preview](reviewed-preview.png) included a stub Appearance entry;
the installed implementation below opens the real existing task. No companion
approval state was edited.

## Delivered behavior

- Design no longer has All Tools. Home retains only Check geometry, New component,
  New group, Variables, native Macro buttons and Help.
- The native `Std_Part` New component command is available immediately after Save
  As in Design's common toolbar, and in Assembly. Its existing semantics remain.
- Modeling's Plus Clone uses the existing sheep icon. Extract keeps its icon.
- Modeling's Boolean Tools uses Part's inventory and native command controls,
  preserving the exact button positions, sizes, dropdown modes and menu entries.
  Cold startup creates equivalent hidden native controls without changing the
  active workbench. Cached native actions are re-created when FreeCAD replaces
  them during workbench changes. Boolean operation semantics are unchanged.
- Modeling > Other > Appearance opens the existing Plus task for the active
  component. It retains explicit eligible body/face selections, including imported
  source geometry; empty selection stays empty. No eligible component or another
  active task disables the action. Existing native Undo and face materials remain.
- Classic, non-Design Plus modes, native action ownership, saved UI preferences,
  responsive tab sizing, overflow scrolling and other toolbar groups are preserved.

## Native evidence

[Installed Modeling](modeling.png), [Home](home.png), [Assembly](assembly.png).
Compare [Modeling Boolean Tools](modeling-boolean.png) with
[Part Boolean Tools](part-boolean.png). These are actual installed Qt controls.

| Run | Result |
| --- | --- |
| s1 | Startup exposed that Part's native toolbar inventory is unavailable before its first activation; fallback added. |
| s2 | 6/6 new workflow checks passed. |
| s3 | Broader checks found native actions invalidated during workbench changes, old test assumptions, and a source-reload customization hook conflict. |
| s4 | 9/9 checks passed after action-cache correction and updated tests for the approved removal of Design All Tools. |
| b1 | Unchanged installed customization baseline passed. |
| s5–s6 | Customization source-reload check still failed because the replaced startup controller retained QAction observation. |
| s7 | Customization passed after detaching the old controller's startup hooks in the isolated harness. No production customization change was needed. |
| i1 | All **12/12 installed checks passed** in a fresh process, including all six broader regressions. |

Coverage includes cold-start/Part/Modeling group equivalence, tab switching and
native popup state, Home command allowlist, save-button order, single native New
component dispatch, sheep artwork, Appearance face Apply/Undo/empty selection,
active child/imported source resolution, disabled contexts, native widget reuse,
live customization, narrow layouts, light/dark themes and Classic preservation.
Tests intentionally retained native command semantics rather than reimplementing
Boolean operations. The complete application test suite was not run.

`FreeCADPlusScripts` builds successfully; no native binaries changed. All seven
installed files match source/build hashes in `install-manifest.json`. Owner profile
CFG and shortcut hashes are unchanged. The desktop shortcut still points to the
existing launcher with empty arguments and the original working directory.
Rollback copies remain under external `validation/design-toolbar-update27/rollback`.
Only disposable documents/profiles were used; no owner model/session was altered.
Disposable run folders are removed after archiving these results. Restart an
already-running FreeCAD Plus process to load the changed modules.

Unrelated `project.previewfirst.json` remains untouched. Reference-image support
and saved active-part restoration are outside this implementation. Completed
changes and evidence are committed/pushed to the configured origin branch, with
remote HEAD verified after publication.
