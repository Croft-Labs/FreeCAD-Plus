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

## Archive status — October 10, 2026

The owner requested preserving this fork for reference before a clean upstream
restart. Treat its implementation backlog below as historical context; do not
resume feature work automatically. Archive/restore procedures and the preserved
checkpoint are in [ARCHIVE_REFERENCE.md](ai-instructions/ARCHIVE_REFERENCE.md).
The clean upstream checkout and feature reimplementation are separate next steps.

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
- Mandatory owner UI/UX documentation gate: maintain the affected files in
  [ui-ux-specs](ai-instructions/UI_UX_SPEC.md): TOOLBARS_AND_BUTTONS.md,
  COMPONENT_PANEL.md, TASK_PANEL.md, DEFAULT_SETTINGS.md and MODEL_VIEW_WINDOW.md.
  These replace the former DOCX authority by explicit owner instruction on 2026-10-10.
  Read the relevant specification and its evidence before edits. Newer explicit
  owner decisions govern; current UI, old Markdown and assistant reports do not
  establish approval. Items marked **Needs owner confirmation** are not requirements
  to implement. An unspecified Plus placement never authorizes workbench removal.
  Preserve the original FreeCAD workbench inventory. Keep technical contracts and
  build/validation/publication evidence in their owning Markdown documents.
  Archived documents and prompts are evidence only, never executable instructions.
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
- Store generated validation output only in
  `C:\Users\GAMING-PC\Documents\_temp\freecad\validation`, including test
  profiles, logs, captures, render output and temporary CAD fixtures. Summarize
  actual results in the canonical roadmap/WORK_STATE, then delete task validation
  files at completion. Do not retain raw validation artifacts in this checkout.
- Store native compilation trees, owner test payloads and required build
  dependencies only in `C:\Users\GAMING-PC\Documents\_temp\freecad\test-builds`.
  Retain the current useful owner/development builds; delete superseded builds
  and unnecessary downloads. Retarget and verify the desktop shortcut before
  removing a build it referenced. Preserve tracked source/tests, owner documents,
  application settings and source archives; this policy concerns generated output.
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

Owner-requested documentation layout (2026-10-10): UI_UX_SPEC.md is an index to
five specifications in ai-instructions/ui-ux-specs, replacing the former DOCX.
The original DOCX and superseded specifications are archived with provenance.
This is a UI-document ownership exception; technical and roadmap ownership remains
as defined by the central standard.
