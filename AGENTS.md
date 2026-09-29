# FreeCAD Plus: Agent Entry Point

## Start here

1. First project reference: read [the programming summary](ai-instructions/PROGRAMMING_SUMMARY.md).
2. Read section 2 of [the central standard](../ai-instructions/AGENTS_TEMPLATE.md)
   once per session; read section 5 for shared-code work and the relevant templates
   when maintaining documentation.
3. Read [the workspace instructions](../AGENTS.md) and follow their linked
   [operational rules](../CODEX_WORKSPACE_RULES.md), unless already loaded.
4. Follow the summary to the task's requirements, source, tests, and roadmap.
   Inspect applicable scoped instructions before edits. Continue authorized work
   through relevant verification and documentation updates.

Central references are relative to this checkout. If unavailable, report the
limitation once, follow accessible local guidance, and continue independent work.
Do not claim to have read missing guidance or maintain an independent master copy.

## Project boundaries

- Work on this FreeCAD Plus checkout. Ignore the separately installed FreeCAD;
  do not modify it or use it as evidence for this fork's changes.
- Current implementation scope includes unified Pad/Pocket Extrude and the
  user-requested Linear/Circular Pattern task workflow, and signed angular start
  offsets/direction buttons for Revolution and Groove, and the user-requested
  associative Trim Body workflow for solids and sheets in Part and Part Design.
  Trim Body creates a separate result; it does not change a source Body Tip. Other operations
  remain future scope; the roadmap does not authorize them automatically.
- Preserve FreeCAD document/property identities, geometry semantics, licensing,
  and submodule ownership. See [development conventions](ai-instructions/DEVELOPMENT_GUIDE.md#development-conventions).
- Record implementation, build, GUI validation, and publication separately in
  [the roadmap](ai-instructions/DEVELOPMENT_ROADMAP.md). A local commit is not a release.

## Project exceptions

None to the central organization standard. The initial specifications cover the
fork's changed workflow; inherited interfaces remain linked to upstream sources.
