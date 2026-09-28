# FreeCAD Plus: Pad task-panel regressions

This file owns the focused regression procedure. Intended behavior belongs in
[UI-001](../ai-instructions/UI_UX_SPEC.md#ui-001-pad-task-pane); current validation
status and pending test corrections belong in the
[roadmap](../ai-instructions/DEVELOPMENT_ROADMAP.md).
For environment setup, use [the development guide](../ai-instructions/DEVELOPMENT_GUIDE.md).

## Regression tests

The GUI suite imports `PartDesignTests.TestPadTaskPanel`. After building this
checkout, run the focused suite in the **built FreeCAD Plus** Python console:

```python
import unittest
from PartDesignTests.TestPadTaskPanel import TestPadTaskPanel
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPadTaskPanel)
unittest.TextTestRunner(verbosity=2).run(suite)
```

The cases exercise no preselection, no sketches, preselection, editing, edge
accumulation/removal, duplicate selection, face selection, source replacement,
invalid profiles, selection-mode switching, reference restrictions, Cancel, and
Undo/Redo. Also check viewport picking and preview positioning manually with a
rotated sketch and with both pad directions.

Record actual results in the roadmap milestone. Do not use the separately
installed FreeCAD for these checks.
