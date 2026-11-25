# Part-owned assembly constraints and component tabs

Implemented and installed November 25, 2026, in the existing FreeCAD Plus payload.
The owner cancelled the separate file import/export request. No new file-transfer
workflow is included in this change.

## Approval and visual contract

Owner requested a collapsed Assembly constraints collector immediately below its
parent, appearing with the first constraint, and the active assembly as the global
reference frame without requiring a grounded child. The owner clarified that every
constrained subcomponent must have its own collector, then approved implementation:
**"approved, implement"**. The accompanying tab change was separately previewed and
approved with **"Approve this tab layout"**. On November 25 the owner directed
continuation of assembly constraints after cancelling the separate import/export work.

- [Baseline screenshot](baseline.png).
- [Approved collector screenshot](approved-collectors.png): native widgets with
  illustrative rows, not a working solver at preview time.
- [Approved tab screenshot](approved-tabs.png): equal padded tabs aligned left.
- [Installed collectors and tabs](installed-collectors.png): real saved native joints;
  the root collector is deliberately expanded, the nested collector remains collapsed.
- [Existing-shortcut capture](shortcut-collectors.png).

Product baseline: `d29d68802b5d5fa79544c5df1e069efcade6aa1f`.
Collector review: session `d3e7fa96f6e8`, snapshot
`bfc0e2bc6ae7a9a5fc353b0af8377fc0792b33fc`, fingerprint
`c2481e37a747498bed296392436db00590d5c23a2a0fefb1669cb6168f0c0fe2`.
Tab review: session `7c7ae1e16791`, snapshot
`8c9c424fed11eee35feb5fdbd173ffb3c08c7ff5`, fingerprint
`59b9851528b0d23a2fbd5ab5da68c8405047121a40d44b643f5103d66fb9cfd1`.
Both single-file `panel.py` previews were reinspected as fresh with no violations.
Chat approval is authoritative; companion approval records were not modified.

## Implementation and delivery

The [component-panel specification](../../ui-ux-specs/COMPONENT_PANEL.md#assembly-constraints-and-padded-tabs--november-25-2026)
owns the visible behavior. The [architecture contract](../../ARCHITECTURE.md#part-owned-native-assembly-constraints--november-25-2026)
owns native solver membership, schema 6, transactions and coordinate frames.
The existing native joint editor creates/edits constraints in the selected assembly,
independently of the component in Edit. Double-click/Edit reuses that editor; Delete
and creation/editing support Undo/Redo. Parent geometry and origin stay fixed; child
links retain their identities and native placements. Disconnected relative constraints
solve without stored child anchors. Native residual checks reject conflicting or
unsupported constraints before publishing placements, while consistent redundancy
remains valid. Classic behavior is guarded separately.

The native Assembly target compiled successfully in the existing build tree; see
[build log](native-build.txt). The update installed one native module and ten Python
files into the existing owner payload, with rollback copies retained outside the
repository. [Install manifest](install-manifest.json) and [delivery verification](delivery.json)
record matching source/payload hashes. The original desktop shortcut still targets
`Launch FreeCAD Plus.bat` with the same working directory. No replacement app or
shortcut was created. Restart existing sessions to load the native/Python update.

## Native verification

- **30/30 new assembly checks pass** in both source and installed runs: fixed parent
  frame/geometry, unanchored islands, face references, revolute freedom, conflict and
  consistent-redundancy handling, nested/repeated collectors, collapse retention,
  live command selection, populated editor/Cancel/in-place acceptance, Undo/Redo,
  deletion, schema upgrade rollback, reference eligibility, existing external-child
  ownership, marker coordinates, active assembly separation and equal padded tabs.
- [Source affected suite](source-regressions-tests.txt): **81/82 pass**.
- [Installed affected suite](installed-tests.txt): **81/82 pass**, same sole error.
  The older `TestComponentPilot.test_structure_context_and_empty_file` directly
  deletes protected component coordinates and raises the existing native guard.
  The identical case fails on the **unchanged prior installed runtime**; see
  [baseline test](prior-runtime-tests.txt) and [module provenance](prior-runtime-result.json).
  It is retained and reported, not skipped or represented as passing.
- [Fresh source reopening](source-reopen.json) and [fresh installed reopening](reopen.json)
  preserve all 62 native IDs, document UID, geometry volume, both collectors and owner
  references. Editing the reopened joint preserves its ID, solves its offset and undoes
  correctly. The installed harness waits for the asynchronous file view to settle before
  invoking the assembly selector; no production guard was relaxed.
- [Existing desktop shortcut](shortcut-tests.txt): **6/6 pass**, including the live
  joint command, nested collectors, editor lifecycle, first-create Undo, tab sizing and
  the existing Add Component dropdown. [Provenance](shortcut-result.json) confirms the
  installed native/Python modules were used, with no source path injection.

These are scoped acceptance checks, not certification of every native joint mechanism,
simulation, or repository test. The older unused-display/cleanup issues already in
WORK_STATE remain separate. GUI validation used isolated settings and disposable files;
owner documents and settings were not used. Durable logs/screenshots are retained here;
task-generated fixture/profile output is removed after verification, with rollback
copies and the reusable build retained.
