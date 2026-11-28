# Linked sketch patterns — installed November 28, 2026

The owner approved implementation with Advanced options and Make independent side
by side. No further UI approval was required or requested. The corrected preview
was recaptured before integration; the screenshots below show working native code.

Implementation commit: `c4896c3764`.

- [Installed editor with horizontal actions](linked-pattern-edit.png)
- [Native generated geometry and group symbol](linked-icon-before.png)

## Behavior

New patterns default to Linked. Editable source geometry is solved first, exact
transformed copies are generated, and one-way downstream sketch geometry is solved
afterward. Copies introduce neither constraints nor independent degrees of freedom.
Source movement, real mouse dragging, dimensions and construction status propagate.
Linear/grid, two-sided/symmetric/reverse and angular/radial layouts retain the existing
parameter controls. Persistent facade IDs keep surviving curve references stable.

The Elements row and native viewport symbol open the saved pattern. Symbols use
display-only facades, never document/solver constraints. Apply resets inputs.
Advanced Cancel leaves the document untouched. Existing constraint patterns remain
legacy until explicit conversion. Make independent preserves current geometry,
breaks the link and adds no constraints, in one Undo step.

Source feedback and independent driving constraints on copies are rejected.
Trim/Split/fillet/extend, construction changes and internal-geometry editing require
independence for generated copies. Source deletion, partial-group deletion and
removal of referenced outputs are guarded before mutation. Explicit LinkSub consumers
are handled conservatively; whole-sketch modeling remains supported.

## Verification and installation

- Reusable native build: Sketcher, SketcherGui, FreeCADPlusScripts; successful exit.
- Exact final staged runtime: 35 passing tests.
- Exact installed runtime: 35 passing tests.
- Earlier broader geometry, grouping, legacy editing and batching run: 60 passing tests.
- Previous-build comparison: 6 passing legacy editing/batching tests.
- Installed two native PYDs and five Python/test files atomically, with rollback.
- All seven source/build/installed payloads match; profile and shortcut hashes unchanged.
- Native mouse source dragging, icon selection/double-click, actual Make independent,
  Advanced cancellation, Apply/reset, Undo/Redo, save/reopen, exact arcs/splines,
  one-way dependencies, chains, reference dimensions and deletion guards checked.

The earlier broad run logged one caught GUI access-violation notification while
still passing its assertions. It did not recur in the final staged run, installed
verification or isolated previous-build comparison. Logs are retained rather than
silently omitting that observation. No owner CAD document was opened or modified.

## Measured synthetic circle pattern

| Mode | Total instances | Constraints | Creation ms | Solve ms |
|---|---:|---:|---:|---:|
| Linked | 10 | 0 | 4.01 | 0.52 |
| Linked | 50 | 0 | 10.76 | 1.39 |
| Linked | 100 | 0 | 18.52 | 2.52 |
| Legacy | 10 | 45 | 9.97 | 0.84 |
| Legacy | 50 | 245 | 301.75 | 36.57 |

Linked runs retain the original circle's three degrees of freedom at every tested
size. These are local single-run measurements, not a general speed guarantee.
No failing owner sketch was supplied, so its particular solver issue is not diagnosed.

## Reproduction

Native tests are in `TestLinkedSketchPattern.py`. The final installation suite also
includes `TestSketchPattern.TestPatternTask` (explicit legacy mode) and
`TestApprovedNative.TestApprovedNative`. Harness scripts and complete result/log
files are archived here. Temporary app/profile/model fixtures are removed after
archival; reusable build, installed app and rollback files are retained.
