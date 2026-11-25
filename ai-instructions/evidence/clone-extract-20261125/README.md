# Clone and Extract geometry: implemented and installed

November 25, 2026. The owner renewed “implement the clone and extract geometry
workflow” after the prepared native proposal. Review `4a3678c76c7b` was inspected
fresh with no scope violations (fingerprint
`a74982217414f97465e8e4d10887fffb42efe054dab2c7eb6e1685f292193db8`). Chat authorization
governs; companion approval state was not changed. The earlier
[proposal](../unified-clone-proposal-20261125/README.md) remains historical UI evidence.

## Delivered behavior

- Modeling > Other: **Clone** replaces Add Reference Object, beside **Extract geometry**.
- Clone selects complete geometric objects from exact direct-child occurrences.
  Native Body/feature containers are allowed; grandchildren, component aggregates
  and subelements are rejected. Reference children are eligible; Excluded children
  cannot supply new inputs.
- Results are parent-owned `cloned body`, `cloned surface`, `cloned sketch`,
  `cloned plane` (numeric suffixes for repeated names). Whole BRep curve/point
  objects are also supported. Child construction history stays in the child.
- Native features and Booleans consume clones. Sketches contain geometry without
  copied constraints. Source geometry and occurrence placement changes update them.
- Extract accepts parent-owned faces, creating one `extracted surface` per face;
  clone a child object first. No edge/point extraction modes or implicit extraction.
- Shared create/edit forms, direct-child browser, native unresolved selection,
  Shift-remove, Remove/Delete/Clear, prominent errors and scene-only preview.
  Cancel creates no objects/Undo entry; OK is one defining-file transaction.
- History editing preserves result identity. Missing/replaced sources are explicit
  repair errors; same-name objects cannot silently replace them. Native topology
  mapping is retained; no separate geometry matching algorithm is claimed.
- Schema 8 stores native source associations. Schemas 1–7 remain readable; first
  creation upgrades lazily and Undo restores the prior schema. Display changes
  preserve higher schema versions. Archive/runtime foreign-reference guards allow
  only the explicit Clone source association through a declared direct-child link.

## Direct screenshots of working native controls

- [Clone creation](clone-create.png) and [existing Clone editing](clone-edit.png).
- [Direct-child occurrence browser](direct-child-browser.png).
- [Extract geometry creation](extract-create.png) and [existing Extract editing](extract-edit.png).
- [Modeling command group](modeling-commands.png).
- [Extract editor after fresh reopening](reopened-extract-editor.png).

These screenshots are actual installed Qt controls, not simulations. Source and
installed tests use isolated preferences and generated documents. Whole-viewport
captures showed native graphics artifacts in the validation environment and are
not offered as polished viewport evidence; geometry/placement assertions and task
screenshots establish the bounded checks below.

## Verification

| Run | Result |
| --- | --- |
| Source final workflow | 13/13 pass (`logs/source-verified`) |
| Installed regression | 85/87 initially pass; two pre-existing duplicate-default-name fixtures rejected by the naming rule (`logs/installed`) |
| Installed final focused | 15/15 pass: all 13 workflow tests plus the two corrected external-file fixtures (`logs/installed-final`) |
| Final native sketch routing/modeling | 7/7 pass (`logs/installed-profile-routing`) |
| Fresh installed process | Four types/proxies, live sketch/native feature updates, extracted faces, shared editor, external source/parent and independent export pass (`logs/installed-reopen`) |
| Existing desktop shortcut | 3/3 pass; real ribbon button, picking, browser and create/edit forms (`logs/shortcut`) |

The 87-case installed set covers Clone/Extract, native modeling, reference admission,
native Boolean picker guards, part transfer, display settings, external definitions,
instance quantities and individual removal. The two older fixture corrections only
give source defaults unique component labels; no naming policy was relaxed. All 87
distinct cases have passing evidence across the regression and focused rerun.

Checks include transformed/repeated sources, native fillet and Boolean consumption,
sketch constraints staying in the child, parent-local frames, exact browser identity,
Reference/Excluded admission, rejected face/grandchild Clone input, missing-source
repair, tampered external source rejection, stale task context, preview/Cancel,
atomic Undo/Redo, same-result editing, export remapping and fresh reopening.

Development failures are retained in the logs: native Sketcher proxy execution and
shape placements required correction; schema display downgrade and saved external
source preflight were fixed; the archive helper was moved to its proper scope.
Additional fixtures were corrected to use native Boolean ownership and source-driven
recompute after manual reparenting. These earlier runs are not acceptance evidence.

## Installation and preservation

Nineteen Python files are installed in the existing payload at
`C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/app`. Source and installed
SHA-256 hashes match [the manifest](install-manifest.json); AST parsing passes for
all 19. CMake source/install manifests and Init registrations include the new modules
and test. No native rebuild was needed. Rollback copies are retained alongside
replaced payload files; useful build/dependency trees were preserved.

The existing `freecad plus 0.1.0.lnk` still targets `Launch FreeCAD Plus.bat`, with
the retained FreeCAD-Plus directory as working directory and no stored arguments.
The archived reference shortcut was untouched. [Final checks](final-checks.json)
record this and the installed hashes. Restart FreeCAD Plus to load the changes.

Helpers are preserved in [helpers](helpers). Durable logs/screenshots were copied
here before removing only the task-generated `validation/clone-extract-20261125`
directory. Unrelated `project.previewfirst.json` remains untracked and untouched.
Publication follows standing commit/push authorization to the configured origin
fork; no upstream push, force-push or release is part of this task.
