# FreeCAD Plus reference archive

## Component naming review — November 25, 2026

Reviewed local tag `archive/freecad-plus-2026-10-10`, checkpoint
`29496214b34a53fa1d479f35ab5669b41ed4fb18`, `src/Mod/Part/ComponentModel.py`.
Its `component_label` returns domestic labels directly and qualifies external
definitions with their defining-file stem (full path for ambiguous basenames).
Its `definition_label` uses case-insensitive domestic name checks. Current
assembly.py already implements the owner's requested source-qualified tree;
the new naming.py extends uniqueness across imported catalogs and reverse importers.
No archived implementation was restored or executed.

## Move Components review — November 25, 2026

At the owner's request, reviewed local tag `archive/freecad-plus-2026-10-10`,
checkpoint `29496214b34a53fa1d479f35ab5669b41ed4fb18`: `src/Gui/MoveComponents.py`,
`src/Gui/MoveComponentsTask.py`, `src/Gui/MoveComponentsManipulator.py`, and
`tests/MoveComponents.md`. The ZIP location documented below is historical;
the local Git tag supplied this review. The old application and archived tests
were not executed. Historical acceptance claims are not current validation.

The archive supplied six methods: Translate, Rotate, Point to Point, Align Axes,
Align Coordinate Systems and Interactive. It included parent-frame movement,
common pivot/group transforms, source/destination collectors, axis alignment
modes, expandable origin/Z/X frame definitions, arrows/plane handles/rings,
component versus pivot manipulation, numeric handle input and distance/angle
snapping. Apply/OK/Cancel, temporary previews and constraints/read-only checks
are useful concepts to retain. The archived manipulator called
`createTransformDragger`, which is absent from the current View3DPy source;
its integration cannot simply be assumed compatible with this baseline.

The [new task proposal](ui-ux-specs/TASK_PANEL.md#move-components) groups these
methods under Move/Rotate/Align and adapts ownership to the fixed active assembly
and immediate parent placements. It was independently written as a UI-only
candidate. Current production `movement.py` supplies only Translate/Rotate and
still uses older file-root occurrence routing. No archived code was restored to
production. Approval and functional implementation remain pending.

## Extrude workflow review — November 21, 2026

The owner requested concepts from the abandoned Extrude workflow, a preview before
implementation, and no copying of the old code. Reviewed checkpoint
`29496214b34a53fa1d479f35ab5669b41ed4fb18` (`archive/freecad-plus-2026-10-10`):
`src/Gui/ComponentExtrudeTask.py`, `src/Gui/ComponentTaskWidgets.py`,
`src/Mod/Part/ComponentExtrude.py`, `src/Mod/Part/ComponentExtent.py` and
`tests/TestComponentCurveProfile.py`. These were read as historical source, not
executed. Archived tests are evidence of intended coverage, not current acceptance.

Useful concepts: select an entire sketch or a connected closed region/curve set
with optional holes; retain visible collected-profile emphasis and easy removal;
require explicit current results for Add/Subtract; separate start position from
end condition; provide independent two-side limits and explicit symmetric total
length; offer taper/custom direction without crowding ordinary extrusion; distinguish
colored tool-volume overlays from evaluated final-result previews; restore temporary
preview appearance; and share creation/editing with saved associative references.
The archive covered Length, Up to face/shape, To first/last and Through all, plus
start offsets/references and offsets from limits. Its validation required explicit
targets for target-dependent extents, rejected open/disconnected/intersecting
profiles, and reported no-material Subtract results.

Adaptations for the current design: retain New Solid terminology and current
feature-centered backend ownership; use direct picked-reference fields rather
than typed object identifiers; put advanced controls behind collapsible sections;
replace archived timer/valueChanged recompute with focus-leave commits and an
explicit Update preview button. Do not restore old metadata/result-wrapper objects,
operation-replacement migrations or user-managed Bodies. Production work must
preserve current feature identity, downstream references, external source ownership,
native Undo/Redo and the shared editing contract.

The [new isolated proposal](ui-ux-specs/TASK_PANEL.md#archive-guided-extrude-proposal--november-21-2026)
was written independently in a candidate worktree. No archived implementation was
ported into it or the current application. It supersedes the earlier length-only
proposal for review; approval and production implementation remain pending.

## Plane workflow review — November 21, 2026

The owner requested guidance from the abandoned fork, starting with Create Plane.
Reviewed the local `archive/freecad-plus-2026-10-10` checkpoint
`29496214b34a53fa1d479f35ab5669b41ed4fb18`, particularly
`src/Gui/ComponentPlaneTask.py`, `src/Gui/ComponentTaskWidgets.py`,
`src/Mod/Part/ComponentPlane.py` and `tests/TestComponentPlaneTask.py`.
The old ZIP path below is historical and unavailable on this machine; the local
Git archive supplied the source. Archived tests were read, not executed, and the
old application was not launched. Detailed Sketch/Extrude reviews remain future work.

### Useful behavior to recover

- Distinguish incomplete input from invalid geometry. Two points should request
  a third noncollinear point; one line should request another suitable reference.
  Conflicting plane-plus-other selections should explain what to remove.
- Keep selected references visible with temporary highlights. The old collector
  supported click-again toggling and Delete, alongside Remove/Clear. The new
  preview adds readable numbered labels and matching amber point markers.
- Offer independent axis reversal. This changes the in-plane direction without
  moving the origin or reversing Z; Flip normal remains a separate operation.
- Manage temporary visibility as part of the task lifecycle: make origin planes
  available while picking, restore their prior visibility/scale afterward, and
  avoid displaying both the saved plane and its edit preview. These lifecycle
  changes are recommendations, not implemented by this preview.

### Preserve newer decisions

Do not restore the archived selection-mode dropdown, numeric coordinate/vector
forms or separate sections. Keep the combined Origin and Orientation section,
point-only origin, universal-origin projection for planes and numeric recompute
only after leaving the field. The archived timer could update while typing.
Its normal reversal also reversed the offset direction, moving an offset plane;
the current rule deliberately preserves plane position when flipping Z.
Keep the current single component-owned associative plane and shared create/edit
task; do not restore the old helper-object arrangement or implicitly migrate files.

### Later geometry work

The archive accepted additional planar curved-edge combinations using sampling
and a native planarity check. That merits separate solver tests before adoption.
Its curved-edge axis used a midpoint tangent, which needs an explicit direction
rule. Its largest-projection default-axis heuristic can improve near-perpendicular
cases but can also switch axes; do not silently replace current defaults.

An isolated native [proposal and checks](ui-ux-specs/TASK_PANEL.md#archive-guided-plane-proposal--november-21-2026)
demonstrate the first three interaction improvements. The owner subsequently
approved implementing these concepts without copying archived code. The current
task/solver received a fresh implementation; see [acceptance](WORK_STATE.md#plane-guidance-implementation--november-21-2026).

Owner instruction: October 10, 2026. Preserve the existing fork for later/future
reference before preparing a clean official FreeCAD baseline. Archiving is not
approval to carry its implementation choices into that baseline.

## Checkpoint and location

- Preserved checkpoint tag: `archive/freecad-plus-2026-10-10`.
- Archive directory: `C:/Users/GAMING-PC/Documents/__Apps/freecad-archives/freecad-plus-2026-10-10-pre-reset`.
- `freecad-plus-checkout.zip` contains the complete working directory, including
  `.git`, local refs/configuration, initialized submodule repositories and their
  checked-out source, documentation and ignored/untracked files present at capture.
- `manifest.json` records the exact commit, submodule commits, file sizes and
  SHA-256 hashes. `verification.json` and `README.md` beside the archive record
  the completed integrity and restore checks. Use their recorded outcome, not the
  existence of this preparation document, to establish archive completion.
- Archive data stays outside the active checkout and is not committed as a large
  binary to the fork. A published Git tag provides a separate named checkpoint.

## Verification result

Archive completed and restored successfully on October 10, 2026. Checkpoint:
`29496214b34a53fa1d479f35ab5669b41ed4fb18`. All 26,999 source/restored file hashes
match; restored HEAD, clean working tree and all seven recursive submodules pass.
ZIP size: 490,791,599 bytes. SHA-256:
`b3bc602148c1232079fbee95932c5742708d1e3721dcebfeee0cd43d0fade0f5`.
The version of this document inside the ZIP is the pre-capture preparation record;
the external verification files and current WORK_STATE record completion.

## Recovery

1. Check the ZIP SHA-256 against the external verification record.
2. Extract into a new, empty local directory. The ZIP paths start at the checkout
   root and include hidden `.git` data; do not extract over an existing project.
3. Verify file hashes against the manifest, then inspect `git status` and recursive
   submodule status. The restored HEAD must match the manifest checkpoint.
4. Read the specifications through UI_UX_SPEC.md. The unverified-change inventory
   and archived instructions are reference evidence, not automatic implementation
   authorization. Do not run old prompts or recreate the backlog automatically.
5. Restore/build only when needed. Existing build outputs are kept separately;
   copied source is not itself a runnable verified build.

This repository is a partial clone. Its current source and initialized submodule
working trees are included in full, together with all locally present Git data.
Some historical blobs may still require fetching from the recorded remotes.
This ZIP is not advertised as an offline-complete copy of every historical revision.
Local remotes/hooks/configuration are preserved for recovery, not intended for
public distribution or automatic execution in a new project.

## Preserved builds and settings

Existing useful builds remain in `C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds`.
The desktop shortcut and application preferences remain in place. They are not
part of the source ZIP and have not been retargeted or changed by this task.
The separately installed FreeCAD is outside this work.

## Workspace overhead

Generated Python cache directories are ignored as directories, allowing traversal
to skip them. Additional compiler intermediates and accidental in-checkout build,
validation or archive directories are ignored. Tracked source, tests, fixtures,
icons and requirements remain tracked. Actual builds/validation continue to use
the external paths required by AGENTS.md.

Local Git untracked-file caching and a commit graph may be enabled after their
checks succeed; actual results are recorded in WORK_STATE. These improve repository
operations, not FreeCAD rendering. They do not diagnose or fix the reported UI jitter.
Do not broadly ignore source trees or all CAD/document/ZIP files to hide useful data.

The active checkout has now moved to the clean 1.1.4 baseline. The prior fork is
retained in the verified external archive, old main history and published tag.
The archive is stored outside it to avoid adding duplicate source to normal project
searches and Git status traversal. No clean clone or feature migration is performed
as part of the archive checkpoint.
