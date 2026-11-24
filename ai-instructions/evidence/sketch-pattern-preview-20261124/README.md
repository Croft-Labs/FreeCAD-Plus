# Sketch Pattern proposal - November 24, 2026

Status: rendered UI proposal, awaiting explicit owner approval. No production
source, installed application, native build, geometry or saved document changed.

## Requested workflow and scope

Replace the existing Move / Array Transform presentation with Sketch Pattern,
retaining its command identity where compatible. Open without preselection, or
prefill eligible sketch geometry. Like the approved Mirror task, hide ordinary
Sketch Edit, Constraints, Elements and advanced-solver sections while active;
restore their previous visibility on Done/Cancel. Keep Cancel and Exit Sketch.

The compact geometry collector supports click to add once, Shift-click to remove,
Delete, Remove and Clear. Selecting a reference field switches the active collector;
no Select/Confirm toggles. Invalid picks preserve valid input and use existing
inline error styling. Pattern results preview before Apply. Apply is the only
operation that creates geometry, stays open, clears the geometry list and retains
parameters. Done/Cancel/Escape discard pending picks/preview, retain earlier applied
sets and return to sketch editing. Exit Sketch retains its native behavior.

Choose Linear or Circular. All counts are **Instances**, including the original,
per the owner's explicit clarification. Each direction independently offers
**One dimension**, **Two dimensions**, or **Symmetric**. Two dimensions means
independent positive and negative spacing/counts, not a second direction.

- Linear: one or two independent directions. Each direction accepts a sketch axis,
  straight sketch/construction/external line, two distinct points or a nonzero
  vector. Reverse swaps its sense. Each extent offers Pitch or Total distance.
  X and Y can each have independent forward/backward values: four extents in total.
- Circular: Angular, Radial, or Angular + radial, as subsequently requested.
  Rotation center accepts a point or the center of a circle/arc; a selected radius
  dimension should resolve to its owning circle/arc center during implementation.
  Angular extents offer Angular pitch or Total angle independently for clockwise
  and counterclockwise sides. Radial extents offer Pitch or Total distance
  independently outward/inward. The center-to-radial-reference vector defines
  outward. A point or circle/arc center can supply that reference. Radial copies
  translate without scaling, and angular copies rotate; combined results form
  concentric rows of the selected geometry set.
- One dimension: N includes the original; total distance/partial angle spans the
  original through the final instance, so pitch is total/(N-1).
- Two dimensions: each side's count includes the shared original; unique total
  is Nforward + Nbackward - 1. Each side has its own pitch/total choice and value.
- Symmetric: a shared pitch/count or total span distributes equally around the
  original; this proposal requires an odd count. Reverse is disabled as it has no
  effect. Total span covers both sides. This count interpretation is a proposal
  for approval, not a separately confirmed owner decision.
- Full-circle total angle is a closed distribution: 360/N spacing, with no duplicate
  at 360 degrees. Implementation must prevent duplicate transforms where angular
  extents meet, and reject degenerate references/inward placement through the
  center rather than silently generating duplicate or undefined geometry.
- Combined direction totals multiply. The linear specimen is (5+3-1) × (4+2-1)
  = 35 instances. Circular specimen is (5+3-1) × (3+2-1) = 28 instances.
- Create dimensions is optional and off by default. It should constrain the copies'
  spacing/angles and placement relative to the source, preserving source freedom
  rather than introducing an unsolicited absolute block on original geometry.

Preserve sketch geometry types, construction state, source geometry/constraints,
document identity, coordinate graphics, unrelated commands, workbenches, user
settings and native transactions. The existing native move-only command is not
removed. Production scope after approval is the Translate command/handler and
necessary native copy/transform support, task lifecycle, reference collectors,
constraint creation, tests and owning documentation. Reuse native Sketcher APIs;
the current addCopy API's perpendicular second direction is insufficient by itself
for all independently chosen directions. No new persisted pattern-object schema
is assumed. Existing Mirror behavior remains unchanged.

## Direct screenshots

- [Current Move / Array Transform task](baseline.png)
- [Linear: two directions, four independent extents](linear-grid.png)
- [Circular: angular and radial, both with two dimensions](circular-radial.png)
- [Linear: one direction](linear-one.png)
- [Linear: mixed two-dimension and symmetric extents](linear-symmetric.png)
- [Circular: full-circle total angle](circular-total.png)
- [Radial only: symmetric](radial-symmetric.png)
- [Two-point direction](two-points.png)
- [Empty input](empty.png), [invalid symmetric count](invalid-count.png),
  [after simulated Apply](after-apply.png), [Done restores sketch sections](after-done.png).

These are native Qt UI simulations inside the installed FreeCAD sketch editor,
not a working pattern implementation. The preview footer is an annotation, not
a proposed product control. Geometry/reference picks and Apply are stubbed;
the specimen geometry count remains unchanged. UI checks confirm empty/invalid
disabling, duplicate-add suppression, Shift removal, independent extent counts,
mode switching, post-Apply clearing and Done restoring native sections.
[UI result](result.json). Geometry, constraint/solver behavior, real viewport
selection, persistence and native Undo still require implementation and validation.

## Provenance and review gate

Companion session `a58cd852b03d`; clean adapter baseline
`e19ce3c39c3b4f0309edb74ad8e547c457ac734f`; installed application source baseline
`68b781c3e5`. Final fingerprint:
`f96413ae3bd6358c150480e5baf48874c25cfc8d258b9c8784bb83d11d541e47`.
Exact candidate allowlist: `pattern_ui.py`. Capture and inspection passed with
no scope violations; approval remains false and was not modified by the agent.
[Candidate UI source](pattern_ui.py), [render adapter](render.py),
[native scene and UI checks](scene.FCMacro).

Adapter source lives in `../sketch-pattern-preview/review-source` relative to the
main checkout, because unrelated `project.previewfirst.json` remains untracked.
Only the UI candidate is changed; no commit is made in either companion worktree.
The superseded first session was invalidated by generated Python bytecode;
the final macro explicitly disables bytecode and its baseline remains clean.

Obtain approval of these screenshots and semantics before functional work, under
the preview-first skill and shared APP_DEVELOPMENT_POLICY. Chat approval is
authoritative; do not change companion approval state on the owner's behalf.
The new EAS/Expo build policy was read; this preview uses the existing native
FreeCAD executable and creates no app build or test-app clone.
