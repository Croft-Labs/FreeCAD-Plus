# Unified Revolve and Native Angular Offset Tests

## Plus component workflow

`tests/TestComponentRevolve.py` covers the shared `ComponentRevolveTask` reached
from Revolution and Groove in component documents and from Model History editing.
Run with `tests/RunComponentDocument.ps1 -TestFiles tests/TestComponentRevolve.py`
against the packaged candidate, using a fresh external evidence directory.

Acceptance checks New Body/Add/Subtract native geometry without a Body container,
selected sketch curves, one/two/symmetric angles, signed start offsets, reference
axes and starts, preview/result agreement, four collapsible sections and defaults,
blue/green/red overlays, None/Final Result, visibility restoration on Cancel,
additive/subtractive type changes preserving published result identity, rollback,
Undo/Redo, save/reopen and both native command entry points. Runtime module hashes
must match the source with source overlays disabled.

The existing suites below retain coverage of legacy Body documents. Physical
pointer/keyboard and high-DPI acceptance remain separate from scripted Qt checks.

Behavior is specified by [UI-003](../ai-instructions/UI_UX_SPEC.md).
Record actual evidence and remaining manual checks in
[the roadmap](../ai-instructions/DEVELOPMENT_ROADMAP.md). Use this checkout's built
FreeCAD Plus, with [isolated GUI setup](../ai-instructions/DEVELOPMENT_GUIDE.md#validation).

## Automated regressions

Run inside an initialized GUI with document views:

```python
import unittest
from PartDesignTests.TestRevolve import TestRevolve
from PartDesignTests.TestRevolveTaskPanel import TestRevolveTaskPanel
from PartDesignTests.TestExtrudeTaskPanel import TestExtrudeTaskPanel
suite = unittest.TestSuite(
    unittest.defaultTestLoader.loadTestsFromTestCase(case)
    for case in (TestRevolveTaskPanel, TestRevolve, TestExtrudeTaskPanel)
)
unittest.TextTestRunner(verbosity=2).run(suite)
```

The new GUI suite exercises actual Revolution and Groove commands with a preselected
profile and a selected sketch axis. Its 84-case geometry matrix covers both types,
all three direction modes, normal/reversed revolution, and offsets of 0, +45, -45,
+180, -180, +360, and -360 degrees. Negative cases use the flip button. It compares
valid single solids, analytical volumes, exact bounds, and both shape differences
against independent cylindrical-sector unions/cuts. Exact bounds exclude display
triangulation so rendering/reopening cannot change the numerical oracle.

Other checks cover visibility/default/range, both angle buttons, creation/editing,
Cancel, Undo/Redo, expression flipping and reset/rollback, and save/reopen for both
feature types. Existing Revolve model tests cover face profiles and start references.

## Manual acceptance

1. Create a Revolution and a Groove with a preselected sketch and valid axis/base.
2. Confirm Offset is visible and starts at 0 degrees in One sided, Two sided, and
   Symmetric. Enter an angle without choosing Start first; verify live preview.
3. Flip the offset. Check positive/negative angles against the original sketch,
   including -360 and +360 remaining visible as entered while matching 0 geometry.
4. Reverse using either angle button in Two sided; both button states update and
   both magnitudes remain unchanged. Confirm symmetric angular reversal is disabled.
5. Exercise rotated sketches, picked axes, reference starts, and end references;
   confirm viewport gizmos follow the shifted angular start.
6. Reopen accepted features, edit offsets/expressions, then check Cancel and Undo/Redo.
7. Inspect keyboard focus/tooltips and task layout at normal and high-DPI scaling.

In legacy Body documents, Revolution remains additive and Groove subtractive.
In Plus component documents, both enter the unified Revolve task; Groove presets
Subtract. Geometry still uses the corresponding native feature type.
