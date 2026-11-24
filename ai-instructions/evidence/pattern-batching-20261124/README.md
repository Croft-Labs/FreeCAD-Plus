# Batched Sketch Pattern creation — November 24, 2026

Owner approved the batching correction and requested a repeated 12-by-12 test with
spacing chains and Equal constraints preserved. Starting source/install: `47a622cb87`.
This is a nonvisual performance correction; task layout, completion actions, preview,
count/extent semantics and saved-data contracts remain unchanged.

## Implementation

The Python service groups copied geometry into native list additions while preserving
ordering and construction flags. Copied constraints and Equal size relationships are
validated in batches. Linear and radial-only spacing helpers are staged in memory,
then added with their equations as batches. Angular helpers retain their ordered
expression indices; their individual checks now avoid the scalar API's extra solve.

Each successful constraint batch needs one explicit solve. If validation reports
redundancy, only fully redundant newly added equations named by native diagnostics
can be removed together. Existing/source constraints and previously accepted Equal
relationships are protected. Remaining failures split into smaller groups; genuine
conflicts still raise and the outer pattern transaction rolls back. A partially
redundant successful solve can move geometry, so rejected groups restore the geometry
snapshot in that case. Native nonzero solve returns do not update geometry and need
no repeated geometry-property reset.

Spacing-constraint visibility uses one native list update. The former 570 individual
updates consumed about 19.3 seconds in the real sketch-edit circle-grid test because
each triggered a complete redraw. This correction also applies to Hide spacing chain.
One driving dimension per independent pitch and the existing helper identity/units
metadata are preserved. No native binary or persistence-schema change is required.

## Measurements and limits

The original installed 12-by-12 circle benchmark was still unfinished at its
100-second process deadline. The same circle grid with batching and spacing enabled
completed in about 1.5 seconds. Final installed timings:

| Check | Apply time |
| --- | ---: |
| [Service: diameter-constrained 12-by-12 circles](installed/grid12-timing.json) | 1.409 s |
| [Actual task button in sketch-edit mode](installed/grid12-task-timing.json) | 1.568 s |
| [Task button through the existing desktop shortcut](shortcut/grid12-task-timing.json) | 1.539 s |

The task fixture also contains one unrelated line. These are local measurements,
not universal runtime guarantees. The [task profile](installed/grid12-task-profile.txt)
records five explicit solves, two geometry-list additions and one visibility update.
The [earlier visibility profile](benchmarks/before-bulk-visibility.txt) and
[last baseline progress](benchmarks/baseline-grid12-last-progress.json) are retained.

The grid contains 144 circles, 143 construction spacing lines, 716 constraints,
143 original-to-copy Equal size relationships, 141 Equal spacing relationships,
143 parallel spacing relationships and two driving pitches. Tests edit the original
diameter and both pitches, inspect every copy and coincident helper endpoint, verify
remaining source freedom, toggle visibility, undo/redo and save the result.

Timing depends on geometry and redundancy. An additional 12-by-12 fixed-length line
grid [completed in 57.28 seconds](benchmarks/source-grid12-line-refined/result.json)
with 430 geometry elements and 1,145 constraints.
It needed 40 explicit solves, mostly to resolve redundant endpoint relationships
while protecting the earlier Equal length equations. This remains a slow case;
the circle timing is not a claim that every 144-instance sketch finishes as quickly.
No change to the native solver or analytical simplification of spacing topology is
included in this batching correction.

## Acceptance and delivery

The source suite passed 72 application checks; [27 focused checks](source-final/tests.txt)
passed after the final redundancy refinement. The [final installed suite](installed/tests.txt)
passed all 72 checks with zero failures or errors, without a source overlay.
[Fresh-process reopening](fresh-reopen/result.json) verified the saved 144-instance
grid, all 143 Equal copies, all spacing helpers, edits to the original diameter and
both pitches, and hidden/visible chain states. The existing desktop shortcut passed
[the real 12-by-12 Apply test](shortcut/result.json). Its target remains the existing
`Launch FreeCAD Plus.bat` in the retained `_temp builds/FreeCAD-Plus` installation.
The native C++ code is unchanged; the prior 88-test native result is historical
evidence, not a new run for this Python-only correction.

Production scope is `freecad_plus/sketch_pattern.py`, a focused native regression
module and its CMake packaging. Both installed hashes match the
[SHA-256 manifest](install-manifest.json); the service has an original-file rollback
backup. Bounded [validation harnesses](harness/) are retained.
Restart FreeCAD Plus to load the updated Python service. The
unrelated `project.previewfirst.json` and the existing shortcut are preserved.
