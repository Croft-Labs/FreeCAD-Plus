# Move Components acceptance

Run `TestMoveComponents` in the Plus GUI runtime. The focused source-overlay suite
uses real native App::Links, component documents, native path transforms, Coin
previews, Qt task controls and transactions. It does not replace packaged acceptance.

Run `TestMoveComponentsRotate` alongside it: eight updated native checks cover
offset axes, world reference locations/directions, native points/circle centers,
two-point/degenerate axes and invalid angles, stable previews and 360-degree no-op,
successive Translate/Rotate with Undo/Redo and both saved formats, reference-role
isolation, resets/persistence, invalid task text, pending picks and workflow changes.
October 6 native and packaged Plus evidence passes all eight updated Rotate checks
and all twelve Translate checks without application source overlays or skips.
See `packaged-final` results/logs and reviewed Rotate task captures in the recovery
evidence task `01a10f79-1a93-7be0-a261-96a6b7e9c425`. Recovery item 1 is complete;
items 2–7 require separate owner follow-up prompts. This is not final build delivery.

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

Separate recovery item 3: retained Align Axes passed 5/5 in packaged-final on this
host before this test edit. The same five tests now explicitly check parallel
identity roll, coincident no-op without target-origin sliding, deterministic
antiparallel roll, repeated baseline previews and sibling/descendant LinkPlacement
round trips in FCStd and cadprt. These added assertions are syntax-checked only;
run all five in recovery item 7. Existing shared Move/Rotate checks cover exact
paths, guards, persistence, Cancel and geometry/identity preservation; final
integration must verify these retained contracts together. Do not count earlier
5/5 evidence as execution of the new assertions.
