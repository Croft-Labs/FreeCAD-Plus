# Pattern task-pane regression procedure

Use this checkout's rebuilt FreeCAD Plus, with the matching PartDesign test modules.
Do not use the installed FreeCAD. Requirements are defined in
[UI-002](../ai-instructions/UI_UX_SPEC.md#ui-002-pattern-task-pane); current evidence
belongs to [roadmap 3.7](../ai-instructions/DEVELOPMENT_ROADMAP.md#combined-pattern-workflow).

## Automated checks

Run the model suites in FreeCADCmd or the built GUI's Python console:

```python
import unittest
from PartDesignTests.TestPattern import TestPattern
from PartDesignTests.TestLinearPattern import TestLinearPattern
from PartDesignTests.TestPolarPattern import TestPolarPattern
from PartDesignTests.TestMultiTransform import TestMultiTransform

suite = unittest.TestSuite(
    unittest.defaultTestLoader.loadTestsFromTestCase(case)
    for case in (TestPattern, TestLinearPattern, TestPolarPattern, TestMultiTransform)
)
unittest.TextTestRunner(verbosity=2).run(suite)
```

In the GUI, run the task-pane suite and the existing Extrude selection regressions:

```python
from PartDesignTests.TestPatternTaskPanel import TestPatternTaskPanel
from PartDesignTests.TestPadTaskPanel import TestPadTaskPanel
from PartDesignTests.TestExtrudeTaskPanel import TestExtrudeTaskPanel

suite = unittest.TestSuite(
    unittest.defaultTestLoader.loadTestsFromTestCase(case)
    for case in (TestPatternTaskPanel, TestPadTaskPanel, TestExtrudeTaskPanel)
)
unittest.TextTestRunner(verbosity=2).run(suite)
```

The model suite checks both geometry engines, stable result and reference identity,
expressions, independent settings, second direction, suppression, empty inputs,
save/reopen, and Undo/Redo. GUI checks use the active task's Qt controls and open edit
transactions through `ViewObject.doubleClicked()`. They do not substitute for physical
mouse/keyboard interaction or broad cross-platform validation.

F030 collector checks cover Originals counts and accepted types, duplicate/removal
updates, Whole body retention, reopen and explicit Clear. Clear preserves both
pattern settings, blocks empty acceptance and supports replacement, Cancel and
Undo/Redo. Direction picking and Originals Add/Remove/Clear are checked in both
transition directions: one selection changes only the intended role. These controls
are scoped to the combined Pattern; legacy model/task regressions remain included.
Additional F030/F031 checks inspect duplicate-label originals by identity, highlight
all entries without model mutation, switch inspection/type/reference roles, restore
visibility on OK/Cancel, and restore original subelement selections plus model state
after creation/edit Cancel. General assembly occurrence behavior remains separate.
F031 parity checks compare Linear/Circular definitions for preselection and later
picks, including reversed input order and duplicate face picks. Mixed and invalid-only
preselection retains valid originals and explains rejected Body/sketch/foreign inputs.
Later scope/dependency/duplicate/removal rejections keep picking active; correction
or Clear dismisses feedback. Cross-document checks cover both selection orders.
Reference collector checks cover Direction/Direction 2/Axis counts and active state,
empty-reference correction, exact subelement inspection without assignment, isolation
from other picking roles, visibility on type changes/OK/Cancel and initial-selection
restoration. Highlight is disabled for an empty reference.
Pending-reference checks cover leaving through Add/Remove/Clear, scope/type switches
and OK for primary/secondary/axis roles. Saved links survive each transition, later
picks cannot fill an abandoned role, and edit Cancel restores selection and model.
Body/sketch/datum Originals rejection uses type feedback before dependency feedback.




## Manual acceptance

1. Create a base plate and an attached additive or subtractive feature. Clear selection
   and click **Pattern**. Confirm Linear/Circular is the first field, followed by the
   feature controls and then direction/axis and repetition parameters.
2. Choose Circular first, then Add Feature and pick the feature in the tree or viewport.
   Select a Body axis and then a straight-edge/datum reference. Set angle/spacing and
   count. Confirm the preview agrees with the chosen axis and direction.
3. Switch to Linear. Pick a direction, change total length/spacing and count, enable
   the second direction, and reverse it. Switch back and confirm Circular settings
   were retained. Check a rotated Body and sketch construction axes.
4. Add several features, remove them through the list and model selection, and re-add
   them. Try a feature in another Body and a downstream dependent feature; neither
   may become an original. Removing all originals must keep OK from accepting.
   Give two originals the same label and select each list row: the correct object
   must highlight without changing the pattern. Clear the row selection and click
   Highlight to inspect all originals. Verify inspection ends direction picking.
5. Toggle Whole body, then Selected features. Confirm the retained feature list returns.
   Change between reference selection and feature selection; verify only the intended
   selector responds and temporary geometry visibility is restored.
   Check the reference count and picking state for Direction, Direction 2 and Circular
   Axis. Highlight each stored reference, including an edge, while another picker is
   active. Confirm the exact reference highlights without changing any saved input.
6. Accept, double-click the Pattern, and confirm the same complete pane opens with
   its saved type. Edit dimensions and type, Cancel, then verify the original result.
   Start with a face selected; inspect and clear Originals, then Cancel. Verify the
   initial face selection returns for both creation and editing, with source/result
   visibility restored according to the normal editor lifecycle.
   Repeat with OK, Undo, and Redo. Save/reopen and repeat both modes.
7. Verify the toolbar/menu has one Pattern entry. Open existing Linear/Polar and
   MultiTransform documents and confirm their stored feature types and parameters
   still work. Legacy type conversion is outside this change.
8. Check tab order, keyboard-only selection/accept/cancel, tooltips, translated labels,
   viewport clicks, and task layout at normal and high DPI. Record any remaining
   visual or interaction defects in roadmap 3.7.

## Compatibility

The new result is `PartDesign::Pattern`, derived from the existing MultiTransform
engine. It owns two retained settings objects and selects one for computation.
Switching never replaces the result feature or rewrites downstream links. Helpers
belong to the same Body, are grouped beneath Pattern, and are removed with it.
The word Circular here means the existing Polar rotation engine, not the separate
concentric-circle `PartDesign::CircularPattern` model type.

Existing Linear/Polar objects remain editable through their existing parameter pane;
they are not migrated. Unmodified upstream versions do not recognize the new Pattern
type. Cross-version recomputation and release packaging are not validated here.
