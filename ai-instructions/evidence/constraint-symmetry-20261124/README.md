# Compatible sketch symmetry redundancy - November 24, 2026

The owner reported that symmetry on a horizontal/vertical rectangle fails even
when the constraints agree. The unchanged application reproduced eight failing
cases ([baseline log](baseline.txt)). This correction changes the solver only;
the existing constraint command, sketch appearance and selection workflow remain.

GCS identifies equations contributed by line/point symmetry and prefers those
equations when diagnosing dependent constraint groups. Only equations satisfied
by the reduced solution are accepted as redundant. They remain in the solver's
redundant equation set for its final residual check, but do not produce redundant
or partially redundant constraint diagnostics. Genuine conflicts and unrelated
redundancy retain their existing error behavior. Saved constraints are not deleted,
deactivated or converted to references; geometry/document formats are unchanged.

Source: `src/Mod/Sketcher/App/planegcs/GCS.cpp` and `GCS.h`.
Regression coverage: `src/Mod/FreeCADPlus/TestSketchConstraintSymmetry.py`, registered
in the existing script copy/install target. Symmetry equation tracking clears with
the system and removes entries when individual constraints are removed.

## Verification

- [Native build](build.log) and [dependent PartDesign GUI rebuild](dependents.log)
  passed. The dependent rebuild keeps consumers of the changed internal solver
  layout consistent. No further production correction was needed.
- [All 88 C++ Sketcher tests passed](native.txt).
- [Installed suite](installed.txt): 40 cases, 39 passed and one existing upstream
  secant test skipped; zero failures/errors. This includes 12 new constraint cases,
  upstream solver coverage, the 12 existing Mirror tests, and native symmetry
  selection retention across Plus/Classic modes.
- New cases cover horizontal/vertical rectangles, construction/oblique axes,
  repeated symmetry, both axes, point symmetry, fully constrained compatibility,
  genuine conflicts, unrelated redundancy, dimension changes, Undo/Redo,
  constraint deletion, save/reopen and a valid 1,000 mm3 downstream extrusion.
- Two initial test assumptions were corrected: a native incompatible `setDatum`
  edit raises and restores the old value, and an undimensioned rectangle may
  change size during solving. The final fixture explicitly constrains its dimensions.
- [Fresh-process shortcut check](shortcut.txt) passed the native rectangle Symmetry
  command using the existing `freecad plus 0.1.0.lnk`. Its unchanged target is
  `_temp builds/FreeCAD-Plus/Launch FreeCAD Plus.bat`, with that parent working
  directory; the launcher opens `app/bin/FreeCAD.exe`.

## Local installation

Installed `Sketcher.pyd`, `SketcherGui.pyd`, the dependent `PartDesignGui.pyd`, and
the new test module. [SHA-256 manifest and rollback paths](install-manifest.json)
record exact source/installed equality and prior native payloads. Checks used
isolated settings; existing owner sessions and the unrelated `project.previewfirst.json`
were preserved. Restart previously opened app processes to load the correction.
This is a local development-build repair, not a published release.
