# Move Components acceptance

Run `TestMoveComponents` in the Plus GUI runtime. The focused source-overlay suite
uses real native App::Links, component documents, native path transforms, Coin
previews, Qt task controls and transactions. It does not replace packaged acceptance.

Run `TestMoveComponentsRotate` alongside it: eight updated native checks cover
offset axes, world reference locations/directions, native points/circle centers,
two-point/degenerate axes and invalid angles, stable previews and 360-degree no-op,
successive Translate/Rotate with Undo/Redo and both saved formats, reference-role
isolation, resets/persistence, invalid task text, pending picks and workflow changes.
The recovered run predates the final test edits; rerun all eight on this host.

Coverage: nested rotated/translated parents, multiple transformed uses of one parent,
standalone parent tab, sibling-only whole selection and implicit descendants,
unchanged definitions/shape identities, atomic rejection/rollback, normalized and
reversed translation, whole-group relative transforms, native reference axes/edges,
curved/ambiguous/zero input safeguards, root-plus-subpath joint guards and driven
placements, native Undo/Redo, no-op transactions and FCStd/cadprt reopen. Task tests
exercise the registered command, actual selection collection, Apply/OK/Cancel,
workflow changes, persistence settings, list removal and document cleanup.

Preview uses native evaluated geometry in every visible occurrence of the owning
parent. Screenshots in the source evidence directory are test artifacts, not owner
payload acceptance. WORK_STATE owns the exact count, results and runtime identity.

Prompt 10 must repeat this suite with the installed modules, verify Design Assembly
and Part Tree entry points, real viewport reference picks with Selection filters and
Layers, joint-driven assemblies, external-parent own-file editing, saved document
data, narrow/high-DPI Tasks, tab/mode transitions and every completed Move workflow.
Complete all six workflows before publishing an owner payload, verify the owner
shortcut, render/inspect affected DOCX pages and keep physical acceptance separate.

Recovery suites: TestMoveComponentsPoint (4), TestMoveComponentsAxes (5),
TestMoveComponentsFrames (4), TestMoveComponentsInteractive (4). These are
prepared native tests, not current pass counts. The Interactive event case picks
the rendered native Coin arrow and sends Qt mouse/Escape events; direct placement
writes or numeric-only checks cannot satisfy this acceptance gate.
