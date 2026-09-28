# FreeCAD Plus: Pad task workflow

Pad creation and editing use the same parameter panel. Its first section is
**Profile**, followed by the existing Pad parameters and preview controls.

- With an active body, click Pad without preselection to open an empty editor.
  This also works when no sketch exists yet; Cancel removes the pending Pad.
- Preselected geometry still initializes the profile normally.
- In the Profile section, click Select, then select a whole sketch in the tree
  or individual edges/faces in the model. An empty new Pad starts in selection
  mode automatically. Ordinary clicks accumulate references without requiring Ctrl.
- Done exits profile selection. Remove deletes highlighted list entries; Clear
  empties the profile and starts selection again. Selectors for direction, start
  reference, and end references remain mutually exclusive with profile selection.
- Reopening an existing Pad shows the same controls and its current references.
- Profiles retain FreeCAD's single-source-object model: several curves/faces may
  belong to that source. Clear before changing source objects. Curves must form
  closed profiles. Cross-body, self, and dependent-object references are rejected.
- OK uses the existing geometry validation and transaction. An empty or invalid
  profile cannot be accepted. Cancel restores the existing feature, or removes
  a newly created Pad. Temporarily shown profile geometry is restored on exit.

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

## Validation status (2026-09-28)

C++ formatting and Python syntax were checked. GUI regressions have **not** run.
Windows CMake configuration found MSVC 19.44 but stopped because no FreeCAD
LibPack is configured. Set `FREECAD_LIBPACK_DIR` to a dependency bundle compatible
with this checkout and build outside the Google Drive source directory before
running the suite. The separately installed FreeCAD was not used for validation.
