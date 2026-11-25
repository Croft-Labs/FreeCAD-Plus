# Instance quantities and editable patterns — implemented and installed

November 25, 2026. The owner's renewed implementation request authorized the prepared
native navigator and task form. Review ef9fa8610a64 was inspected fresh without scope
violations, fingerprint 9027c86fe3a312851df4dca056c5e4ce1f31059e249a268ff0bd56e209d50046.
Companion approval state was not changed. The unrelated project.previewfirst.json
was preserved.

## Delivered workflow

Add Component > Add existing/new > Next opens Create instances. Choose one of:

- [Quantity](quantity.png): independent native links at a parent-relative position.
- [Linear](linear.png): count, start, direction, spacing and reverse.
- [Grid](grid.png): columns/rows, two directions and spacings.
- [Circular](circular.png): center/axis/radius, start angle, full circle or angular
  spacing, and keep/rotate orientation. Full circle excludes a duplicate endpoint.

These screenshots show real installed Qt controls. Counts are per checked definition,
include the first new link and exclude existing instances. Add new makes one definition
shared by its new links. New Component remains separate. Change parts returns to the
navigator while retaining valid arrangement settings. Preview uses unpickable scene
geometry and never creates objects.

Right-click an individual pattern member > Edit instance pattern reopens the same form.
Pattern edits preserve surviving member identities and block removals with direct or
indirect references or live Edit contexts. Pattern members cannot be independently
moved or newly constrained; use the pattern editor. Quantity links remain independent.
The active assembly stays fixed; placements belong to the destination parent. Shared
subassembly occurrences show the same children, including external parent definitions.

## Persistence and boundaries

Schema 7 adds parent-owned native App::FeaturePython metadata with Configuration,
Members, Seeds and native References. Members remain shared App::Links. New files use
schema 7; schemas 1–6 remain readable, and older files upgrade when a pattern is created.
Undo restores the old schema. Older Plus builds reject schema 7 rather than losing data.
The restored proxy updates positions when direction references change. Native export
remaps pattern metadata and produces editable independent files.

At most 10,000 new links may be created in one operation. Linear allows typed vectors;
other directions use parent axes or straight-edge/axis references. Pattern-member
constraints are intentionally blocked. There is no new individual-removal command,
Clone implementation or pattern dissolution in this change.

## Verification

- Source acceptance: 45/45 quantity, Add Component and part-transfer tests.
- Additional source external-parent test: 1/1.
- Installed regression: 54/54 across quantity, Add Component, part transfer and
  condensed/expanded instance display.
- Final installed quantity/pattern suite: 15/15 after layout/theme corrections,
  including lazy schema migration and Undo/Redo.
- Fresh installed process: saved proxy restoration, member IDs, linked source files,
  populated edit task, count changes with Undo/Redo, independent editable export and
  reference-driven recomputation all pass.
- Existing desktop shortcut: 3/3 native navigator/Change parts/commit, edge selection/
  context-menu editing, and all four layout/preview/error checks pass.
- Thirteen installed Python files match source SHA-256 hashes. See install-manifest.json.
  Previous files retain .before-instance-quantity-20261125 rollback copies. No native
  DLL changes or new build were required.

Initial test-development runs are retained in logs: a successful task acceptance
destroyed its form before a test inspected it; one stale-context fixture tried to edit
a placed definition as unused; an old ribbon test omitted the new second step and was
stopped at its test process; an external-parent assertion initially expected no host
Undo entry, while native linked-document recomputation correctly adds one. Those test
assumptions were corrected. Production screenshots exposed wrapped Circular content
overlap and a native theme mismatch; final sizing and themed container corrections
were verified in the final captures and final suite. No claim of a full repository
test run is made.

Final log review also caught queued layout callbacks after a task was destroyed.
The resize timer is now parented to the form. The repeated 15-test suite, fresh-process
reopen (empty stderr) and shortcut 3/3 pass after this fix. Earlier reopen logs are
retained under installed-reopen-before-timer-fix. Archived text has trailing whitespace
normalized; test outcomes and diagnostic content are unchanged.

## Delivery

Existing shortcut target remains:
C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/Launch FreeCAD Plus.bat
with working directory C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus
and no arguments. Restart the existing FreeCAD Plus app to load these modules.

Logs, final native screenshots, install hashes and bounded helper scripts are retained
here. Generated task validation profiles/documents are removed after archiving; the
existing payload, reusable build, rollback files and preview review worktree remain.
Publication is verified against the origin branch after committing this evidence.
