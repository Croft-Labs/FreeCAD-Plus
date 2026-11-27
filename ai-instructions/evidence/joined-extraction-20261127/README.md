# Joined surface extraction — November 27, 2026

Owner approval: “approved. implement the join surfaces workflow”. The approved
preview is session `af9bee845167`, fingerprint
`0266609ac85ce587421185bccf60d77bbb69444f399df50b3a688adf78c1fb5f`.
Inspection confirmed a fresh preview and no file-scope violations; approval was
given in chat, not written into companion approval state.

## Delivered workflow

Modeling > Other > Extract geometry has **Join surfaces**, checked for a new task.
One face or a connected face set creates one `extracted surface` History entry.
Joining uses native Part shell construction and preserves surfaces rather than
creating a solid, even when all faces of a closed solid are selected. The source
solid is retained. Connectivity can pass through other selected faces and must
include shared edges; isolated islands and point-only contact fail. Overlapping
faces and invalid shells fail before the Undo transaction. The prominent error
explains how to correct the selection or turn joining off; OK is disabled until
the selection is valid, with acceptance also independently validated.

Unchecked creates one feature per selected face in selection order, with unique
`extracted surface`, `extracted surface (2)`, etc. labels. Disconnected faces are
allowed in this mode. All results are committed in one Undo step.

History Edit restores every saved face and the join mode. Editing keeps the
existing feature identity; splitting a joined result retains it for the first
face and creates the remaining independent features. Existing references to that
first feature survive. Invalid input and Cancel leave it unchanged. Source changes
recompute all selected faces. Deleted secondary sources remain invalid/repairable
instead of silently disappearing from the joined result. Original Clone admission,
component ownership, imported-component ownership, selection gestures, contextual
surface toolbar, preview controls and native save/Undo behavior remain in effect.

## Persistence and compatibility

Legacy `FreeCADPlus.DerivedGeometry.1` Clone and one-face Extract objects still
load without migration. New/edited Extract objects use feature marker
`FreeCADPlus.DerivedGeometry.2`, with global-scope `ExtractSources` link/subelement
list, `ExtractSourceObjects` identity list, `ExtractFaceCount`, and `JoinSurfaces`.
The primary legacy Source/SourceObject fields remain consistent with the first
source. The stored count detects links dropped by native object deletion. Global
scope permits eligible component-owned features nested inside Bodies; local
ownership and cross-file checks are still enforced before creation/recompute.
Existing file schema 8 remains; older feature validators reject the newer marker
instead of treating a joined result as a one-face extraction. An old extraction is
upgraded only when its edit is accepted, inside the same Undo transaction.

## Screenshots

These three captures show the installed native task using disposable geometry:

- [Joined extraction](joined.png)
- [Separate extraction](separate.png)
- [Disconnected selection error](disconnected.png)

[Approved UI preview](approved-preview.png) used Qt controls and simulated History
results. The installed captures and tests above exercise real geometry and tasks.

## Validation

| Run | Result |
| --- | --- |
| s1 | Initial 21-case source run: 19 pass. Exposed acceptance of overlapping faces and an ignored primary-source mutation; both corrected. |
| s2 | 22/22 source cases pass, including deleted secondary-source recovery. |
| s3 | 32/32 final source cases pass, including global link scopes, curved/moved geometry and selection integration. |
| s4 | 1/1 focused source case passes after final native OK-button state correction. |
| i1 | 32/32 installed regressions pass. |
| i2 | 1/1 installed task case passes after final button-state correction; screenshot source. |
| i3 | 3/3 fresh installed process checks restore/recompute the saved joined file, exported copy and imported-component host created by i1. |

Coverage includes transitive adjacency, opposite faces, point contact, coincident
overlap, true shared shell edges, single/separate faces, complete closed shells,
curved faces, transformed Bodies, source recompute, History order, split/edit identity,
downstream reference preservation and cycle rejection, atomic failure, Cancel,
Undo/Redo, legacy loading/upgrading, stale tasks, deleted sources, native selection/
Shift removal, disabled preview, cross-file ownership, export and native restoration.
Expected invalid-source recompute messages are retained in stderr logs.

The existing `FreeCADPlusScripts` target builds successfully. No native binary
changes were required. The retained build log is the final incremental script
copy check. All five installed Python files match source/build SHA-256 values;
`verification.json` also checks preserved owner CFG and shortcut hashes. Original
payloads are retained under
`C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/validation/extract-join27/rollback`.
No owner model was opened or saved. Restart an already-running FreeCAD Plus window
to load the updated modules. Unrelated `project.previewfirst.json` is preserved.
