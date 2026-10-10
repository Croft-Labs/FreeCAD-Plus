# FreeCAD upstream issue watchlist

Reviewed against GitHub issue/PR metadata and this checkout on 2026-09-29.
This is a small, prioritized working list, not an upstream issue export.
Order reflects data loss, system impact, incorrect results, then workflow friction.
Closed upstream does not prove local runtime validation. See the
[roadmap](DEVELOPMENT_ROADMAP.md#upstream-issue-work) for evidence and pending checks.

| Order | Issue | Basic problem | FreeCAD Plus disposition |
| --- | --- | --- | --- |
| 1 | [#18044](https://github.com/FreeCAD/FreeCAD/issues/18044) | Corrupted newer project can hide crash recovery data. | Closed; [recovery checks](https://github.com/FreeCAD/FreeCAD/pull/24123) and [writer hardening](https://github.com/FreeCAD/FreeCAD/pull/27355) inherited. UI changes do not obsolete recovery. Five isolated startup fixtures pass: damaged ZIP/model XML/GUI XML recover; newer/older valid controls behave correctly; original files remain unchanged. |
| 2 | [#29376](https://github.com/FreeCAD/FreeCAD/issues/29376) | Intermittent OS-wide slowdown. | Open, high impact. Frame limiter already inherited; no deterministic local reproduction. Needs affected-session GPU evidence, not a speculative UI rewrite. |
| 3 | [#32690](https://github.com/FreeCAD/FreeCAD/issues/32690) | CAM offset can flip an arc and generate wrong geometry. | Closed; [fix](https://github.com/FreeCAD/FreeCAD/pull/32703) inherited. Still relevant to CAM backend. All 43 offset-suite tests pass in existing build, including mixed-normal arc regression. |
| 4 | [#32717](https://github.com/FreeCAD/FreeCAD/issues/32717) | Numeric arrow/wheel edits lost on focus change. | Closed; shared [quantity-input fix](https://github.com/FreeCAD/FreeCAD/pull/32707) inherited. New task panes still use these widgets; not obsolete. Arrow and wheel focus-loss checks pass in the existing fork. |
| 5 | [#32718](https://github.com/FreeCAD/FreeCAD/issues/32718) | Task field edits fail to update model. | Closed; same shared fix inherited. Unified Add/Subtract keyboard edits update properties and geometry on create and reopen; 19 Extrude task tests pass. |
| 6 | [#32700](https://github.com/FreeCAD/FreeCAD/issues/32700) | Numeric input ignores document/display units. | Closed; same shared fix inherited. Document-inch implicit input passes with the global schema set to millimetres. Still relevant to stock and modeling dimensions. |
| 7 | [#32706](https://github.com/FreeCAD/FreeCAD/issues/32706) | Mirror plane ignores enclosing Body placement. | Open upstream; fixed locally and built with a targeted Part update. Six geometry/persistence and two task-pane selection tests pass in the 75-test batch. Linear/Circular Pattern does not replace Part Mirror. |
| 8 | [#28412](https://github.com/FreeCAD/FreeCAD/issues/28412) | Tree expansion accidentally selects other objects. | Closed 2026-09-22; [fix](https://github.com/FreeCAD/FreeCAD/pull/29687) inherited. Existing tree remains in use. Native mouse-event expand/collapse checks pass without changing model selection; not obsolete through planned NX history. |
| 9 | [#10584](https://github.com/FreeCAD/FreeCAD/issues/10584) | Legacy MillFace ignores approach start point. | Closed as won't-fix because Mill Facing replaces it. Current toolbar uses Mill Facing, so superseded for new tasks. Legacy saved MillFace operations still carry this risk; do not silently migrate paths. |
| 10 | [#27751](https://github.com/FreeCAD/FreeCAD/issues/27751) | Surface/Waterline CAM refactoring umbrella. | Open. Modern PlanarSurface and modular generators already inherited and used by our STL workflow. Modern avoidance failure handling is now fixed and validated (67 CAM tests). Three open child reports are tracked below; the wider epic stays open. |

Inherited fix ancestry checked at `a501be8d1c`: recovery `864cde5aed` / `74e1d71c65`,
quantity input `c15232437e`, arc offset `3708e7c27`, tree `8390598d5c`.
Source inspection agrees with these commits. No inherited fix was reapplied.

## Remaining CAM cases under #27751

Seven linked children reviewed on 2026-09-29; four are closed. Open cases, in
impact order for the current workflow:

- [#27950](https://github.com/FreeCAD/FreeCAD/issues/27950): external avoidance faces
  crash or lose coverage in legacy Surface. The modern planar open-face case
  passes. Fixed related modern boundary-failure fallbacks and strategy switching
  that could discard exclusions; eight focused tests pass. Original curved
  GeomFillSurface object remains unverified: the supplied attachment actually has
  a mirrored Pad face, and this build has `BUILD_SURFACE=OFF`. Its saved BReps
  generate a path with PlanarSurface; a generated curved B-spline exclusion passes
  coverage checks. Further fixed partial-region loss: failed individual/group
  projection or union now stops generation instead of dropping selected regions.
  Also rejected the lossy outline fallback that filled holes after avoidance
  projection failed. All 81 focused/related CAM checks pass in one batch (U.22),
  including primary hole preservation and stale-path removal. Avoidance requiring
  that fallback now reports an error; legacy backend unchanged. Exact
  GeomFillSurface acceptance remains open; the #26300 generation correction is below.
- [#26300](https://github.com/FreeCAD/FreeCAD/issues/26300): freeform surfacing hangs
  or crashes. Reproduced in PlanarSurface despite UI changes, then corrected locally
  with tolerance-controlled mesh projection for freeform cutting boundaries (U.23).
  The saved geometry/face selections now generate in 14 seconds instead of timing
  out at 120 seconds. All 91 CAM checks pass, including geometric controls and
  4,118 fixture cutting endpoints inside the mask. Native cancellation, legacy
  operation replay and machine/post acceptance remain separate pending checks;
  this does not close the upstream report.
- [#6864](https://github.com/FreeCAD/FreeCAD/issues/6864): line-pattern stepover can
  leave the final strip uncut. Reproduced in the replacement C++ generator;
  fixed locally with additional clipped passes at each contour's transverse
  limits. Nonintegral stepovers, disconnected/rotated regions, reverse order and
  hole exclusion pass; all 77 focused/related CAM tests pass after a targeted
  module compile/relink. Legacy Surface backend unchanged; no machine/post claim.

## Links for later review

- [Open blockers](https://github.com/FreeCAD/FreeCAD/issues?q=is%3Aissue%20is%3Aopen%20label%3ABlocker)
- [Open high-priority issues](https://github.com/FreeCAD/FreeCAD/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22Priority%3A%20High%22)
- [Open Part Design issues](https://github.com/FreeCAD/FreeCAD/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22Mod%3A%20Part%20Design%22)
- [Open CAM issues](https://github.com/FreeCAD/FreeCAD/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22Mod%3A%20CAM%22)
- [Open topological-reference issues](https://github.com/FreeCAD/FreeCAD/issues?q=is%3Aissue%20is%3Aopen%20topological)

Keep this file concise. Follow links for reproductions, attachments and discussion;
record accepted tasks and validation in the roadmap.
