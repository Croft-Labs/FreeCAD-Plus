# Remove individual instances — implemented and installed

November 25, 2026. The owner's renewed implementation request authorizes the prepared
native review. Review c631e12413ea was inspected fresh without scope violations;
fingerprint b370f2d705dd001d08bda7ed9d43df68d82222d178babe46a84177be57e2fb0c.
Companion approval state was untouched. Unrelated project.previewfirst.json remains
unchanged and outside the commit.

## Workflow and direct screenshots

Right-click an individual Assembly occurrence > Remove instance, or select one
occurrence in that tree and press Delete. Both open the same review:

- [Simple removal](simple.png): owning file/parent, exact selected occurrence and
  remaining count. The part definition and geometry/history stay in Parts.
- [Dependent constraints](constraints.png): explicitly opt in to deleting the listed
  owning-assembly constraints; otherwise removal stays disabled.
- [Shared-parent scope](shared.png): explicit acknowledgement that removing a child
  changes the shared parent everywhere. Removing a whole subassembly instance
  preserves that definition's children and constraints.
- [Blocked reference](blocked.png): named dependency and recovery guidance.
- [Fresh-process imported parent](reopened.png): real restored link and source ownership.

These are screenshots of actual native installed functionality, not simulations.
Cancel is the default, including Enter. Hidden, Reference and Excluded occurrences
can be removed. Condensed groups expose individual children; Delete on a group,
root, collector or multiple selections cannot fall through to native definition
deletion. Pattern-controlled links direct users to Edit instance pattern.

## Ownership and safety contract

The target is one owning-document App::Link, identified by document UID, object name,
native ID and qualified route. A rebuilt plan must match the review at acceptance.
File/view/context changes, renamed components/constraints, changed sibling membership
or references require reopening the review. Active root routes and Edit ancestry
are protected in the panel's open component views.

One transaction removes explicitly included joints, then that link. It preserves
definitions, other links, catalogs/imports, source geometry/history and source files.
Native recomputation runs with SolveOnRecompute temporarily suppressed and restored,
preventing solver-driven repositioning of survivors. A placement invariant and native
transaction rollback protect failure paths. Native Undo/Redo restores exact link and
joint IDs and reference relationships. The empty solver backend can remain, while
the Assembly projection hides its empty collector.

Native direct/hidden links, ancestor-rooted LinkSub paths, reachable expression
references and loaded external consumers block unsupported removal. Dependencies of
included constraints also block. This does not scan unrelated unopened files on disk.
Shared external files follow normal explicit save/reload behavior. There is no new
schema, recursive definition deletion, pattern dissolution, bulk removal or Clone
implementation.

## Verification

- Source final removal suite: 12/12.
- Installed affected regression: 41/41 (12 removal, 15 quantities/patterns,
  eight condensed/expanded display and six affected constraint checks).
- Installed focused removal and persistence fixtures: 12/12.
- Final review checks after complete constraint-state/file-path signatures and wording:
  4/4, including stale dependencies, external consumers, Cancel and last-instance removal.
- Fresh installed process: removed external link stays absent; remaining/native host
  identities persist; restored review can remove the remaining link and Undo/Redo it;
  an unused definition retains its geometry and IDs; deleted constraints stay absent.
- Existing desktop shortcut: 3/3 for real menu/Delete routing, constraints and shared
  scope. Final native screenshots inspected for legibility and enabled states.
- Five installed Python files match source SHA-256 values in install-manifest.json.
  Rollback copies are retained. No native rebuild was needed.

Initial runs are retained honestly: an empty native parameter group returned None,
requiring a guard before reading preference entries; external XLink fixtures needed
both documents saved; a display fixture used an invalid type label; native Undo
restores object IDs but changes the unordered Document.Objects enumeration; switching
tabs required checking the original binding before resolving the old route. These
were corrected. The first test process was stopped when its modal test hit the
preference error. No broad full-repository pass is claimed. Remaining stderr contains
a Qt test-harness deprecation and expected warnings from deliberately invalid
cross-scope reference fixtures; the fresh-process run has no errors.

## Delivery and retention

The existing desktop shortcut still targets
C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/Launch FreeCAD Plus.bat,
with the same working directory and no arguments. Restart FreeCAD Plus to load the
new modules.

Logs, direct screenshots, install hashes and bounded helper scripts are archived here.
Text trailing whitespace is normalized without changing outcomes or diagnostic text.
Disposable task validation profiles/documents are removed after archiving; the
existing app, reusable build, rollback files and preview worktree remain. Publication
is checked against the origin branch after committing this evidence.
