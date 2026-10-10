# FreeCAD Plus: Agent Entry Point

## Start here

1. Read [PROGRAMMING_SUMMARY.md](ai-instructions/PROGRAMMING_SUMMARY.md) first.
2. Read section 2 of [the central standard](../ai-instructions/AGENTS_TEMPLATE.md)
   once per session; section 5 for shared-code work and relevant documentation templates.
3. Read [workspace instructions](../AGENTS.md) and [operational rules](../CODEX_WORKSPACE_RULES.md)
   unless already loaded. Report unavailable central guidance once and continue independent work.
4. Read [DEVELOPMENT_GUIDELINES.md](ai-instructions/DEVELOPMENT_GUIDELINES.md),
   relevant owner UI specifications/evidence and scoped instructions before edits.
5. Use [the roadmap](ai-instructions/DEVELOPMENT_ROADMAP.md) and
   [WORK_STATE](ai-instructions/WORK_STATE.md) for current status.

## Clean baseline and authority

The owner requested a clean official stable baseline on October 10, 2026.
This checkout starts at FreeCAD 1.1.4, commit
`4fd3bf320d9566a27e60069fc8387448aaa3a094`, on `codex/freecad-1.1.4-baseline`.
The prior fork is archived and remains available as reference. Its code, old
roadmap completions and implementation constraints are not current behavior or
permission to restore features automatically. Preserve this clean baseline until
specific reimplementation work is authorized.

- Work on this checkout; do not modify or use separately installed FreeCAD as evidence.
- Original upstream application source, workbenches, submodule pins and licensing
  are retained. An unspecified Plus placement never authorizes workbench removal.
- The [five UI specifications](ai-instructions/UI_UX_SPEC.md) own intended behavior.
  Newer explicit owner decisions govern. Current UI, old Markdown and assistant
  reports do not establish approval. Needs owner confirmation entries and the
  unverified-change inventory are review material, not implementation requirements.
- Update affected UI specifications for owner interface changes. Keep technical
  contracts and implementation/build/GUI/publication evidence in their owning documents.
- Historical documents are under ai-instructions/archive/pre-restart-docs;
  archived documents, code and prompts are evidence only, never executable instructions.
- Preserve document/property identities, geometry semantics and submodule ownership.
  Reuse upstream services; confirm ownership/reference contracts before migration.
- Record implementation, build, GUI validation and publication separately. A source
  checkout or local commit is not a tested application or owner-ready build.
- Existing builds and desktop shortcut remain associated with the archived fork.
  Every new owner build must update the existing `FreeCADPlus.exe - Shortcut.lnk`
  to its verified executable, then reopen/check target and working directory.
  Preserve its name and unrelated shortcuts. Do not claim delivery before verification.
- Batch related authorized changes before costly builds; use proportionate quick
  checks and record deferred runtime validation.
- Generated validation output belongs only in
  `C:/Users/GAMING-PC/Documents/_temp/freecad/validation`.
  Record durable results, then remove task-generated validation files.
- Build trees, owner payloads and dependencies belong only in
  `C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds`.
  Preserve useful existing builds, settings and source archives. Verify a replacement
  shortcut before removing any build it referenced.
- Coherent validated commits may be pushed to the configured origin fork. Verify
  remote state afterward. No force-push, upstream push, release or deployment is authorized.

## Project exception

UI_UX_SPEC.md is an index to five owner-intent files in ui-ux-specs, replacing the
former DOCX by owner instruction. Evidence and unverified implementations remain
separate. The old fork's detailed technical documents are historical references.
