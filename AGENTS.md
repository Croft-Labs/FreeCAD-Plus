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
- Batch related authorized changes before a costly build and test pass; do not
  rebuild after every change or just to close one feature task. Keep quick checks
  running and record deferred validation. Follow the
  [build batching policy](ai-instructions/DEVELOPMENT_GUIDE.md#build-and-test-batching).
- The user authorizes periodic pushes to the configured `origin` GitHub fork.
  Push coherent, validated commits at completed milestones and clean stopping points;
  verify the remote branch afterward. Do not force-push. This does not authorize
  releases, deployments, or pushing to `upstream`.

## Project exceptions

None to the central organization standard. The initial specifications cover the
fork's changed workflow; inherited interfaces remain linked to upstream sources.
