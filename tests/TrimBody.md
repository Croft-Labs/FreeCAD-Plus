# Trim Body Tests

Behavior is specified by [UI-004](../ai-instructions/UI_UX_SPEC.md#ui-004-trim-body-task-pane).
Use this checkout's native FreeCAD Plus build and isolated user settings; record
actual results in [the roadmap](../ai-instructions/DEVELOPMENT_ROADMAP.md#trim-body).

## Automated regressions

The task-readiness regression makes a previously valid target fail recompute,
verifies hidden preview and blocked acceptance, then repairs it and accepts the
recovered result. Shared dependency-state validation also serves Isocline.

Replacement checks reject a failed candidate for Target and Tool without changing
stored links or selection mode, then verify successful selection after repair.
Preselection checks skip a failed target, retain its valid tool and accept the
target after repair and explicit selection in the task.

Run model tests with the built FreeCADCmd, or both suites in an initialized GUI:

```python
import unittest
from parttests.TestTrimBody import TestTrimBody
from parttests.TestTrimBodyGui import TestTrimBodyGui
suite = unittest.TestSuite(
    unittest.defaultTestLoader.loadTestsFromTestCase(case)
    for case in (TestTrimBody, TestTrimBodyGui)
)
unittest.TextTestRunner(verbosity=2).run(suite)
```

The 14 model tests verify planar sides and analytical volume/area, closed solids,
cylindrical and exact quadratic B-spline sheets, a connected two-face roof, curved
cuts of sheet targets, invalid/incomplete cuts, stale-output clearing/recovery,
self/dependent references, parameter changes, datum planes, nested container
placements, Body targets with unchanged Tip, and save/reopen/Undo/Redo.

The 10 GUI tests use the real command, selection observer, Qt buttons and edit
transaction. They cover no preselection and field order, missing-input recovery,
reverse and replacement, invalid picks, paused-preview acceptance, solid face
preselection, curved and sheet inputs, save/reopen, Cancel visibility restoration,
Undo/Redo, arrow cleanup, and actual toolbar command invocation in both workbenches.
Toolbar availability is tested independently of a user's saved hidden-toolbar
preference. Also run the existing Pad, Extrude, Revolve, and Pattern task suites in
the same process to detect leaked selection observers, task state, or transactions.

## Manual acceptance

1. Open a solid and a separate plane or surface in the same document. Invoke
   **Trim Body** in Part or Part Design without preselection. An active Body is optional.
2. Pick the target in the viewport or tree, then pick the cutter. Verify the field
   labels and kept preview. A face pick on the target selects its entire owning object;
   a face pick for the tool selects only that face.
3. Flip the adjacent keep-side button. Confirm the green arrow points into the
   retained side and the preview removes the opposite material. Check solids close.
4. Move a small planar tool through the target with planar extension enabled;
   disable extension and confirm an insufficient finite patch is rejected.
5. Test a curved face or connected sheet that fully spans the solid, then a sheet
   target. Confirm both keep sides. A short curved patch must show an error.
6. Accept, double-click the result, replace the target/tool, and change the side.
   Cancel must restore geometry and visibility. Check Undo/Redo and save/reopen.
7. Move or change the cutter and target; recompute and confirm the trim updates.
   Also move an input's parent App::Part. The source Body's Tip remains unchanged;
   the associative Trim Body result is a separate object in the document tree.
8. Check input clearing, wrong-document/dependent picks, failed OK recovery,
   paused preview, and closing a document while editing. No stale preview may be accepted.
9. Check viewport picking, keyboard navigation, tooltips, readable errors, and
   normal/high-DPI layout on the user's display.

The feature uses a single cutter and local oriented normal with reversal. Automatic
extension of curved surfaces is outside this first implementation. Saved features
require the new BOPTools scripts for recomputation; upstream-only installations
may display cached geometry but are not a validated editing environment.
