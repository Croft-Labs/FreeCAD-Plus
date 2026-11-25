# Add Component dropdown and child placement — November 24, 2026

**Add Component** always opens **Add existing / Add new**, even after a prior
choice. It has no primary/default action and does not repeat a remembered command.
Add existing opens the counted component navigator; Add new opens a separate
create-and-add dialog. Both place one child at the edited component's origin and
retain the parent Edit context and selected assembly root.

Standalone **New Component** still creates an unplaced definition and activates it.
The Plus New Assembly button is removed; Components' active-assembly selector and
Classic native commands remain. Other split buttons keep their original behavior.

## Approval and preview

The owner requested that Add Component always drop down, then clarified that it
must differ from New Component. The revised native UI preview was approved in chat
with **"Approved. Implement"**. Direct previews:
[dropdown](approved-dropdown.png), [existing](approved-existing-component.png),
[new child](approved-new-component.png); [baseline toolbar](baseline.png).

Product baseline: `2ac7c4e350296d24b564097c1a27f9e512e8a91b`.
Clean UI snapshot: `1fa2a90e50ac379b3f67b94053e3669cd60530c5`.
Companion session: `413250405770`; allowlist: `toolbars.py`, `add_component_preview.py`.
Approved fingerprint:
`356d63438b5b870cb7121677bcb1b79ecee7686b12b3fd3d417b899a2093159c`.
Reinspection was fresh with no scope violations. Chat approval is authoritative;
the tool's approval state was not modified. Preview placement was simulated;
the installed captures/tests below use real native definition and link changes.

## Implementation

`component_add` creates the `InstantPopup` button and two modal pickers. Existing
parts use native identity tokens, current defining-file rows, component-instance
counts and collapsed loaded-file groups. Invalid choices have explanatory tooltips.
Both paths capture document UID, native view, edited definition ID and occurrence
route, then recheck them along with native tasks/transactions at acceptance.

`hierarchy.add_child` performs complete preflight before one native defining-file
transaction. It reuses factored definition/instance creation with existing hierarchy
and clipboard services. Add new writes the definition, coordinates and link in one
Undo step. Add existing may register a required saved catalog and its child link
in the same transaction, retaining the source definition identity. Failure rolls
back every partial object and import property. No implicit saves or schema changes.

Nesting validation follows all links, including Reference and Excluded branches;
direct/indirect self-containment and circular file imports are rejected. Source-file
preflight is shared with catalog-only Import through `external.prepare_import`.
Files changed/corrupted on disk produce recoverable errors without partial imports.
Editing an external parent writes into its defining file. Unused parents can accept
children without creating a file-root placement. Assembly selection is independent.

## Native verification

- [Source workflow/toolbar rerun](source-final-tests.txt): 14/14 pass.
- [Installed affected suite](installed-tests.txt): **55/55 pass**, no failures/errors.
  Includes 13 Add Component cases, hierarchy, external catalogs/import, active
  assembly, native component creation, History rename and representative toolbar
  behavior. These are scoped acceptance checks, not a claim about every repository test.
- [Fresh-process reopen](reopen.json): domestic and externally linked children retain
  IDs, volume, child membership and source identity. A further add and Undo succeeds.
- [Existing desktop shortcut](shortcut-tests.txt): 6/6 pass, verifying the real dropdown, the
  distinction from standalone New Component, and creation in both presentation modes.
- [Install manifest](install-manifest.json): source/payload hashes verified for four
  Python modules and two test files; previous files retained as rollback copies.

The actual Qt main-button area was clicked three times, selecting Add existing,
Add new, then Add existing/Cancel. Every click opened the menu. The native test
also confirms removal of the Plus New Assembly control. Tests cover duplicate/blank
names, live context changes, deleted selections, newly introduced cycles, pending
transactions, unsaved external files, atomic import/creation rollback, Undo/Redo,
hidden/reference/excluded relationships and unchanged parent Edit state.

The initial broader source run found a stale toolbar expectation omitting the
previously approved Surface group and an assertion that every menu must be a
split button. Expectations now include Surface and explicitly check Add Component's
InstantPopup exception; other split-button hit-area/last-action checks still pass.
The runner's source-suffix routing was corrected before the final source checks.
The older unused-display/cleanup failures documented in the active-assembly task
were not changed or represented as resolved by this task.

Actual installed UI: [dropdown](installed-dropdown.png),
[existing component](installed-existing.png), [new child](installed-new.png).
Visual inspection matches the approved flow and native icons. Tests send real Qt
events to actual widgets; they do not claim manual OS mouse verification.

## Delivery

The existing `C:/Users/dgium/Desktop/freecad plus 0.1.0.lnk` retains its target
`C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/Launch FreeCAD Plus.bat`
and working directory. Validation uses explicit isolated profiles, preserving owner
documents/settings and other sessions. Restart FreeCAD Plus to load the Python
update. No native rebuild was needed.

Bounded validation scripts are retained here. Task output used
`validation/add-component-20261124` under the current development runtime;
disposable fixtures/profiles are removed after evidence archival, with rollback
copies retained. The unrelated `project.previewfirst.json` is excluded.
