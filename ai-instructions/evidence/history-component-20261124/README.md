# Active component and Rename in History — November 24, 2026

The active component is now the first History row, above Coordinate System.
Only this tab draws its native icon/name at the far left, spanning the eye/name
columns with the existing active highlight. It has no visibility eye or drag
action. Right-click the icon or name and choose Rename to use the existing
shared-definition dialog. Models/Part Tree labels update together; Undo/Redo,
native identity, geometry and saved names retain their existing contracts.

## Owner approval and preview identity

The owner requested left alignment above the history eyes and confirmed that the
component must have no eye. The revised [native preview](approved-preview.png)
was approved in chat: "Approved implement and also make sure that the user is able
to right click the part row and rename it". [Baseline](baseline.png).

Product baseline: `1b57a219734d017378b19746f26a336f6bcb13ae`.
Clean panel snapshot: `fa6825c4862f5de3368422d6ac8a9aee14138dc4`.
Companion session: `2d88c5b86d50`; allowlist: `panel.py`.
Approved preview fingerprint:
`3e51285a5e403ad1ec288aaecf38f82b6ea6fb0b2b31c7d4f101cb8a2ccc1429`.
Reinspection was fresh with no scope violations. Chat approval is authoritative;
the tool's approval state was not modified. The preview simulated rename; the
installed captures below follow a real document rename through native Qt menus.

## Implementation and verification

`freecad_plus/panel.py` adds a presentation-only component row, full-width native
delegate painting and a Rename-only context menu. The existing rename service
still owns validation, transactions and shared labels. History additionally
rechecks the active component and exact occurrence path. The heading is excluded
from geometry selection, eye updates/toggles and drag sources; drop positions
count only actual feature rows. File-only History and other tabs retain their
previous presentation. No schema, coordinate drawing or native binary changed.

- [Source run](source-tests.txt): 44 checks, no failures/errors.
- [Installed run](installed-tests.txt): the same 44 checks, no failures/errors.
- [Fresh-process reopening](reopen.json): domestic/external names, identity,
  geometry volume and the renamed History heading persist.
- [Existing shortcut](shortcut-tests.txt): five checks passed, including native
  context-menu Rename and New File/New Component in both presentation modes.
- [Install manifest](install-manifest.json): source/installed hashes verified for
  the Python panel and four affected test modules; rollback copies retained.

The suite covers context events over both the far-left icon and name, Cancel,
invalid/duplicate names, stale context, native-editor guards, unused/external
definitions, owning-file Undo/Redo, visibility preservation and dependency-safe
History ordering. The reopen harness initially tried unused-model Edit on a placed
fixture; correcting it to the existing occurrence route passed without app changes.

Direct working UI: [renamed History](installed-history.png),
[Rename dialog](installed-rename-dialog.png). Visual inspection confirms the
approved alignment and no component eye. Qt event tests exercise the actual menu
and dialog; these are not a claim of manual OS mouse testing.

The existing `freecad plus 0.1.0.lnk` still points to the same development launcher
and working directory. No shortcut, owner document/profile or unrelated
`project.previewfirst.json` was changed. Restart an already-running FreeCAD Plus
session to load the Python update. No native build was required.

The bounded validation scripts are retained alongside this record. Disposable
fixtures/profiles used `validation/history-component-20261124` under the current
development runtime, matching recent local project delivery practice.
