# Isocline Curve Tests

Behavior: [UI-005](../ai-instructions/UI_UX_SPEC.md#ui-005-isocline-curve-task-pane).
Actual build/test evidence: [roadmap](../ai-instructions/DEVELOPMENT_ROADMAP.md#isocline-curve).
Use this checkout's rebuilt Part, PartGui and PartDesignGui modules with isolated
user settings. The separately installed FreeCAD is outside this validation.

## Automated regressions

Startup failure injection covers a factory exception after object creation and
editor refusal: neither leaves an object or pending transaction; retry succeeds.

The task-readiness regression makes a previously valid source fail recompute,
verifies hidden preview and blocked acceptance, then repairs it and accepts the
recovered curve. Shared dependency-state validation also serves Trim Body.

Replacement checks reject a failed candidate for Faces and Direction Reference
without changing links or selection mode, then verify selection after repair.
Mixed preselection checks omit failed face objects, retain valid ones and allow
repaired faces to be added before acceptance.

Run inside the initialized source-built GUI:

```python
import unittest
from parttests.TestIsocline import TestIsocline
from parttests.TestIsoclineGui import TestIsoclineGui
from parttests.TestTrimBody import TestTrimBody
from parttests.TestTrimBodyGui import TestTrimBodyGui
suite = unittest.TestSuite(
    unittest.defaultTestLoader.loadTestsFromTestCase(case)
    for case in (TestIsocline, TestIsoclineGui, TestTrimBody, TestTrimBodyGui)
)
unittest.TextTestRunner(verbosity=2).run(suite)
```

The nine Isocline model tests also run under FreeCADCmd. They compare curve length
and independently sampled normal-dot-direction residuals with analytical answers.
At each sampled point, distance to the trimmed face is checked as well as the
angle condition. Cases cover spheres with five draft angles and three pull vectors,
reversed face orientation, cylinders including the 90-degree limit, quadratic
B-splines (including a boundary contour and a closed loop), and clipping around a
hole. Empty/nonunique solutions, invalid angles/vectors, source parameter changes,
multiple faces, datum/edge direction references, nested placements, dependency
restrictions, save/reopen and Undo/Redo are exercised.

Seven GUI tests use actual selections and Qt controls for no-preselection creation,
face accumulation/removal, direction references and custom vectors, angle and reverse,
invalid-state recovery, paused preview, Cancel, Undo/Redo, save/reopen, and both
workbenches' toolbar actions. Command enablement uses a delayed timer, so action
checks allow the event loop to settle without forcing actions enabled.

Trim Body tests protect the extracted shared reference and edit/arrow helpers.
Also run the existing Pad, Extrude, Revolve and Pattern task suites together once
after integration to check that task and selection state do not leak.

## Manual acceptance

1. Open a sphere or curved sheet and invoke **Isocline Curve** without preselection
   from Part or Part Design. Confirm Target faces comes first and Draft angle starts
   at 0 degrees. Add one or more faces by normal viewport clicks.
2. With a sphere and Z pull, confirm 0 degrees traces the equator. At 30 degrees,
   the curve lies at half the sphere radius above its center. Reverse moves it below.
3. Switch to Reference, choose a plane or planar face, and confirm pull follows its
   normal. Exercise a datum axis and a straight edge, then a custom vector.
4. Use an organic/freeform sheet and a surface with a hole. Inspect the red contour
   and ensure it does not bridge excluded surface regions. Inspect the green pull arrow.
5. Accept and double-click the result. Change faces/direction/angle in the same pane.
   Cancel must restore the original curve; Undo/Redo and save/reopen must retain it.
6. Change source dimensions and direction-reference placement, recompute, and confirm
   the curve moves. Source bodies remain intact and their Tips do not change.
7. Exercise an empty selection, zero custom vector, no-solution angle, matching
   planar face, and the isolated sphere pole at 90 degrees. Errors must remain
   editable and cannot accept stale geometry. A cylinder can have a valid 90-degree line.
8. Check keyboard focus, tooltips, target/reference picking and normal/high-DPI layout.
   Capture the native window for arrow evidence; viewport image export omits annotations.

The convention is **n dot d = sin(angle)** for unit oriented normal n and unit pull d.
Each feature has one angle. Curves use source-surface parameter curves and a 3D
approximation tolerance; a sampled fit check is not a completeness guarantee for
arbitrary or singular surfaces. Splitting faces/bodies and stepped angle series are
separate future workflows. Saved results require the FreeCAD Plus scripts and native
Isocline API for recomputation.
