# FreeCAD Plus: Agent Entry Point

## Start here

1. First project reference: read [the programming summary](ai-instructions/PROGRAMMING_SUMMARY.md).
2. Read section 2 of [the central standard](../ai-instructions/AGENTS_TEMPLATE.md)
   once per session; read section 5 for shared-code work and the relevant templates
   when maintaining documentation.
3. Read [the workspace instructions](../AGENTS.md) and follow their linked
   [operational rules](../CODEX_WORKSPACE_RULES.md), unless already loaded.
4. Read [the adopted development guidelines](ai-instructions/DEVELOPMENT_GUIDELINES.md),
   including their repository adoption rules and task-relevant sections. Consult the supplied planning baseline
   only for the relevant contracts and gates; it does not start new implementation.
5. Follow the summary to the task's requirements, source, tests, and roadmap.
   Inspect applicable scoped instructions before edits. Continue authorized work
   through relevant verification and documentation updates.

Central references are relative to this checkout. If unavailable, report the
limitation once, follow accessible local guidance, and continue independent work.
Do not claim to have read missing guidance or maintain an independent master copy.

## Project boundaries

- Work on this FreeCAD Plus checkout. Ignore the separately installed FreeCAD;
  do not modify it or use it as evidence for this fork's changes.
- Current owner priority is the component/document migration in roadmap 7.8:
  Component Structure, Model History, shared embedded/external definitions and
  versioned `.cadprt` persistence. Follow the approved component contract; continue
  its integration and acceptance work before unrelated feature rotation.
- Current implementation scope includes unified Pad/Pocket Extrude and the
  owner-requested combined Additive/Subtractive Loft, Pipe, Helix and Primitive component workflows, and the
  user-requested Linear/Circular Pattern task workflow, and signed angular start
  offsets/direction buttons for Revolution and Groove, and the user-requested
  associative Trim Body workflow and draft-angle Isocline Curves in Part and Part Design.
  Both create separate results and preserve source Body Tips. Scope also includes
  direct STL CAM Parallel/Waterline machining, editable stock-to-part holding tabs,
  and separate manually indexed setups sharing model/stock/tab transforms.
  The user also authorizes prioritized work on `ai-instructions/FREECAD_ISSUES.md`;
  check inherited fixes and changed UI applicability before modifying code.
  Other operations
  remain future scope; the roadmap does not authorize them automatically.
- Preserve FreeCAD document/property identities, geometry semantics, licensing,
  and submodule ownership. See [development conventions](ai-instructions/DEVELOPMENT_GUIDE.md#development-conventions).
- Record implementation, build, GUI validation, and publication separately in
  [the roadmap](ai-instructions/DEVELOPMENT_ROADMAP.md). A local commit is not a release.
- Mandatory owner-change documentation gate: every change made for the owner MUST
  update [FreeCAD Plus UI & UX.docx](ai-instructions/ui/FreeCAD%20Plus%20UI%20%26%20UX.docx)
  with the affected requirements, retained behavior, defaults or validation status.
  Read the current file first and preserve owner edits, its DOCX format, heading
  structure and native automatic numbering. Never replace numbering with text or
  convert this document to Markdown. Render and verify edited pages before handoff;
  do not report owner changes complete while this document is out of sync.
- Mandatory owner-build delivery gate: every new build intended for the owner
  MUST update the existing desktop `FreeCADPlus.exe - Shortcut.lnk` to that
  build's verified `FreeCADPlus.exe`, then reopen the shortcut and verify its
  target and working directory. Do not report the build ready until this passes.
  Preserve the shortcut name and unrelated shortcuts. Follow the
  [shortcut delivery procedure](ai-instructions/DEVELOPMENT_GUIDE.md#owner-build-shortcut).
- Batch related authorized changes before a costly build and test pass; do not
  rebuild after every change or just to close one feature task. Keep quick checks
  running and record deferred validation. Follow the
  [build batching policy](ai-instructions/DEVELOPMENT_GUIDE.md#build-and-test-batching).
- The user authorizes periodic pushes to the configured `origin` GitHub fork.
  Push coherent, validated commits at completed milestones and clean stopping points;
  verify the remote branch afterward. Do not force-push. This does not authorize
  releases, deployments, or pushing to `upstream`.

## Development approach

Preserve this fork and reuse existing geometry, links, solvers and shared services.
Decide ownership, identity, persistence and reference contracts early; prove them
with a narrow end-to-end pilot before migrating commands. Prioritize dependency-ready
work by user impact, feasibility and validation cost. A dialog or successful build
alone does not establish recompute, undo, save/reopen or downstream correctness.
Use the [canonical roadmap](ai-instructions/DEVELOPMENT_ROADMAP.md#planning-baseline-adoption)
for phase mapping and status; do not create duplicate programming/status roadmaps.

## Project exceptions

None to the central organization standard. The initial specifications cover the
fork's changed workflow; inherited interfaces remain linked to upstream sources.
