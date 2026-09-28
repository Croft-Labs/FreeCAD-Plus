# FreeCAD Plus: Extrude and Pad task-panel regressions

This file owns the focused regression procedure. Intended behavior belongs in
[UI-001](../ai-instructions/UI_UX_SPEC.md#ui-001-pad-task-pane); current validation
status and pending test corrections belong in the
[roadmap](../ai-instructions/DEVELOPMENT_ROADMAP.md).
For environment setup, use [the development guide](../ai-instructions/DEVELOPMENT_GUIDE.md).

## Regression tests

After building this checkout, run the focused model and GUI suites in the
**built FreeCAD Plus** Python console:

```python
import unittest
from PartDesignTests.TestPadTaskPanel import TestPadTaskPanel
from PartDesignTests.TestExtrude import TestExtrude
from PartDesignTests.TestExtrudeTaskPanel import TestExtrudeTaskPanel
suite = unittest.TestSuite(
    unittest.defaultTestLoader.loadTestsFromTestCase(case)
    for case in (TestExtrude, TestPadTaskPanel, TestExtrudeTaskPanel)
)
unittest.TextTestRunner(verbosity=2).run(suite)
```

The cases exercise no preselection, no sketches, preselection, editing, edge
accumulation/removal, duplicate selection, face selection, source replacement,
invalid profiles, selection-mode switching, reference restrictions, Cancel, and
Undo/Redo. Also check viewport picking and preview positioning manually with a
rotated sketch and with both pad directions.

The Extrude suites additionally check the first-field Add/Subtract dropdown,
both legacy object types, operation changes, extent names, expression/dependency
retention, no-base recovery, save/reopen, legacy Operation lists, and Common behavior.
Manually confirm that the main menu/toolbar provides one Extrude button; reopen
both Pad and Pocket, switch operations, and check rotated/reference/custom directions,
both sides, taper, start/end references, and downstream patterns. Run existing
`TestPad` and `TestPocket` suites as geometry regressions after the build succeeds.

Record actual results in the roadmap milestone. Do not use the separately
installed FreeCAD for these checks.
