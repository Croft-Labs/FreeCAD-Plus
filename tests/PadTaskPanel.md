# FreeCAD Plus: Extrude and Pad task-panel regressions

This file owns the focused regression procedure. Intended behavior belongs in
[UI-001](../ai-instructions/UI_UX_SPEC.md#ui-001-pad-task-pane); current validation
status and remaining acceptance checks belong in the
[roadmap](../ai-instructions/DEVELOPMENT_ROADMAP.md).
For environment setup, use [the development guide](../ai-instructions/DEVELOPMENT_GUIDE.md).

## Regression tests

After building this checkout, run the focused model and GUI suites in the
**built FreeCAD Plus** Python console:

```python
import unittest
from PartDesignTests.TestPadTaskPanel import TestPadTaskPanel
from PartDesignTests.TestExtrude import TestExtrude
from PartDesignTests.TestPad import TestPad
from PartDesignTests.TestPocket import TestPocket
from PartDesignTests.TestExtrudeTaskPanel import TestExtrudeTaskPanel
suite = unittest.TestSuite(
    unittest.defaultTestLoader.loadTestsFromTestCase(case)
    for case in (TestExtrude, TestPad, TestPocket, TestPadTaskPanel, TestExtrudeTaskPanel)
)
unittest.TextTestRunner(verbosity=2).run(suite)
```

Run inside an initialized GUI, with document views available. When using an
isolated automated process started with `--hidden`, initialize the main window
before running the suites synchronously; a deferred startup timer can be skipped
when the hidden event loop exits. For an offscreen Qt test window:

```python
from PySide import QtCore
import FreeCADGui as Gui
main = Gui.getMainWindow()
main.setAttribute(QtCore.Qt.WA_DontShowOnScreen, True)
main.show()
Gui.updateGui()
```

The fixtures use `ViewObject.doubleClicked()` when reopening features so the same
edit transaction as the UI is opened. They locate controls only in the active task
and retain the parent widget while inspecting its layout. These details matter
for Cancel/Undo tests and PySide widget lifetimes.

The cases exercise no preselection, no sketches, preselection, editing, edge
accumulation/removal, duplicate selection, face selection, source replacement,
invalid profiles, selection-mode switching, reference restrictions, Cancel, and
Undo/Redo. Also check viewport picking and preview positioning manually with a
rotated sketch and with both pad directions.

F031 regressions compare profile/axis links, operation, direction/extent parameters
and accepted volumes between
preselection and command-first picking for Extrude, Pad and Pocket in Add/Subtract.
Mixed whole-solid/Body plus sketch selections are tested in both orders; the
active Body stays the scope. Ambiguous profiles and invalid vertex/other-Body
inputs leave a recoverable task with explicit feedback. Create/edit Cancel checks
restore original subelement selection and Body Tip/profile state. These do not
establish future multi-target Boolean or general occurrence-selection support.

F030 collector regressions cover counts after accumulation, duplicate picks,
removal, clear and reopen; whole-profile counting; row and all-entry highlighting;
explicit Profile activation from the start-reference role without reference
assignment; and inspection visibility/selection cleanup on Cancel and OK for
Extrude and Pocket. Physical viewport/high-DPI acceptance remains separate.

The Extrude suites additionally check the first-field Add/Subtract dropdown,
both legacy object types, operation changes, extent names, expression/dependency
retention, no-base recovery, save/reopen, legacy Operation lists, and Common behavior.
Manually confirm that the main menu/toolbar provides one Extrude button; reopen
both Pad and Pocket, switch operations, and check rotated/reference/custom directions,
both sides, taper, start/end references, and downstream patterns. The existing
`TestPad` and `TestPocket` geometry regressions are included in the command above.

Record actual results in the roadmap milestone. Do not use the separately
installed FreeCAD for these checks.

## Start offset and direction buttons

In both new and reopened Extrude tasks, check the visible zero-default Offset
field in One side, Two sides, and Symmetric. Enter a positive distance without
first changing Start; click its adjacent arrow button to negate the distance.
Check preview position against the sketch plane, including a rotated sketch and
a custom direction. The existing reference-start mode remains available.

Check both length buttons in Two sides: either reverses the common axis and both
buttons reflect that state, retaining both lengths. Symmetric Dimension disables
length reversal. Through all and reference extents keep the direction button
next to Type when Length is hidden. Start offset remains signed relative to the
selected extrusion direction, preserving existing saved-feature behavior.

Repeat with Subtract and an existing Pocket. Check expression-bound offset flips,
zero offset, selecting Profile plane to reset, reopening, Cancel, and Undo/Redo.
The automated `TestExtrudeTaskPanel` cases cover these controls and geometry;
physical viewport, keyboard, and high-DPI interaction remain manual acceptance.

`testAddSubtractOffsetGeometryMatrix` exercises 72 combinations through actual task
controls: both Extrude and legacy Pocket commands, Add and Subtract, all three
direction modes, normal and reversed extrusion, and zero/positive/flipped-negative
offsets. It compares valid solids, analytical volumes, bounds, and both geometric
differences against independent box union/cut results. It also checks accepted
feature reopening, another flip, Cancel, and removal through Undo.
