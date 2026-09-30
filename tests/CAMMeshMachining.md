# CAM STL and holding-tab validation

Use the source-built FreeCAD Plus application, never the separately installed
FreeCAD. This procedure covers REQ-021 through REQ-024 and UI-006. Automated
geometry and GUI tests are separate from native interaction and machining evidence.

## Build and automated tests

Enable `BUILD_CAM`, `BUILD_DRAFT`, `BUILD_MESH_PART`, `BUILD_TECHDRAW`,
`BUILD_SPREADSHEET`, and `BUILD_IMPORT` in the existing development configuration.
Build with the source-pinned LibPack; it provides OpenCAMLib. New Python modules
and tests are listed in CAM's CMakeLists.txt. Keep outputs outside Google Drive.

Set `FREECAD_PLUS_VALIDATION_DIR` to a fresh external output folder; point
`FREECAD_USER_HOME` and `FREECAD_USER_DATA` at an isolated directory. Launch
`tests/ValidateCAM.FCMacro` with the development `FreeCAD.exe`, isolated
`--user-cfg` / `--system-cfg` files, and `--hidden`. The macro initializes the
GUI, writes `results.json` and per-module logs, then exits. Require successful
process exit, PASS, and no skipped tests for the focused workflow suite. Record
optional inherited-test skips separately; the strict aggregate marker remains
FAIL if any suite skips a test. `FREECAD_PLUS_CAM_TESTS` optionally
selects comma-separated CAMTests module names; default `TestMeshMachining`.

The suite covers actual STL file input, mesh clones and setup placement, stock
bounds, Parallel/Waterline on mesh and CAD jobs, tab geometry changes,
save/reopen, unsupported-strategy stale-path clearing, and the tab create/edit
transactions. Analytical path splitting is checked with long crossings having
no interior path point, rotated and overlapping bridges, vertical moves inside
bridges, reversed traversals, unsupported arcs and insufficient safe height.
An independent sampled swept-cylinder check compares generated motion against
the tab's local solid bounds. Mixed translated mesh/CAD models and preservation
of block-delete annotations are also checked. These checks do not prove
machine/holder safety.

Relevant inherited regressions: `TestPlanarSurfaceOp`, `TestSurfaceMeshGenerator`,
`TestPathStock`, `TestPathDressupHoldingTags`, and the shared CAM job/operation
tests. Record exact suites actually run in the roadmap.

## Boundary dressup failure checks

`tests/TestCAMInvalidInputs.py` runs against the source-built application alongside
`CAMTests.TestDressupPost` and `CAMTests.TestMeshMachining`. Its Boundary fixtures
check that offset/clipping exceptions clear cached commands, missing/non-geometric/
null boundaries block postprocessing, and repair restores generation/export.
Injected empty offset results cover both inclusion and exclusion before clipping;
these are failure-handling checks, not a proof of arbitrary offset geometry quality.
Missing base input produces an empty native Path and recovers when reattached.

## Array and Dogbone failure checks

Run `tests/TestCAMInvalidInputs.py` with `CAMTests.TestPathDressupArray`,
`CAMTests.TestPathDressupDogboneII` and `CAMTests.TestDressupPost` after synchronizing
both dressup modules to the development build. Array fixtures cover missing/empty
base paths during execution and generator exceptions; Dogbone covers generation exceptions and
clearing its corner/maneuver caches. Native error state must block export on failed
generation, and corrected inputs must regenerate/export successfully. The Dogbone
failure fixture seeds corner caches deliberately; inherited geometry tests cover
normal corner generation separately. When a producer fails, native recompute can
skip downstream execution: the Array fixture verifies the existing export guard
rejects the cache, then explicitly executes the dressup to check empty-path cleanup.
It does not prove eager invalidation of every skipped consumer. These checks do
not establish machine safety.

## Mirror placement and failure checks

`tests/TestCAMInvalidInputs.py` also covers Mirror's disabled-axis passthrough with
translation/rotation, combined base/mirrored output for identity and translated
placements, unchanged source G-code/native state, generation failure/export rejection,
and corrected-input recovery. An injected assembly failure verifies that the base
portion is not published before the complete result is ready. Run alongside nested
postprocessing, Array and Dogbone regressions. These checks are separate from
viewport interaction and machining acceptance.

## Axis Map failure and conversion checks

Run `tests/TestCAMInvalidInputs.py` with the nested-dressup and rotary-post
regressions. Axis Map tests cover zero/negative-radius error and export rejection,
arc-conversion failure clearing, and regeneration after correction. Analytical
checks cover all six X/Y-to-A/B/C mappings in both directions on a linear path,
with unchanged source G-code. Radius must be finite and positive; Reverse controls
rotation direction. The rotary-post fixture deliberately injects compound/split
path snapshots; before export it recomputes inputs, checks operation validity and
clean/valid recursive inputs, then restores and acknowledges only the fixture
output edit. The production export
guard is unchanged and independently covered by invalid-input tests.
This validates the inherited mapping operation, not a new
simultaneous-multiaxis workflow or physical machine/post compatibility.

## Z Correction probe validity checks

`tests/TestCAMInvalidInputs.py` creates an isolated four-point probe grid with a
constant 0.5 mm correction and verifies the corrected cutting height. It covers
missing files, insufficient/collinear probe data, a valid grid too small for the
path, interpolation exceptions, error-state export rejection, and repaired-input
recovery. Explicitly clearing the probe filename retains the existing uncorrected
placed-base behavior and clears the old surface. A specified but unusable probe
file must never silently reuse an older surface or export an uncorrected fallback.
Additional numeric cases reject NaN/+infinity/-infinity in each probe coordinate
and zero/negative interpolation settings, then verify recovery/export. Source-line
lengths 0.5, 1, 1.01, 2 and 2.5 mm with a 1 mm segment setting check subdivision
counts, final endpoints and maximum spacing before Z correction. Surface slope can
increase corrected 3D segment length; these tests do not claim adaptive chord error.
External file edits still require recompute; automatic filesystem monitoring and
arbitrary probe-grid quality are not established by these tests.

## Native acceptance

1. Import an STL, select it, create a Job. Check stock size and placement. Move,
   rotate and center the job model, then verify model/path/stock alignment.
2. Select a suitable tool and feeds. Create **Parallel / Waterline**, choose
   Parallel / surface scan with ZigZag, set depths and stepover, and inspect paths.
   Repeat with Waterline and a coarse enough step-down to inspect each level.
3. Use **Holding Tab**, position it across the model edge into stock, and set
   length, width, height and angle. Test viewport picking and numeric entry.
   Check that cutting passes and connecting moves rise above the bridge.
4. Add a second bridge, including an overlapping/rotated example. Edit one
   after paths exist; confirm the regenerated paths preserve both.
5. Cancel creation and editing; check Undo/Redo, then save/reopen and recompute.
   Attempt an unsupported operation and an unsafe-height tab; confirm there is
   an actionable error and no retained old path.
6. Create an Indexed Setup at 180 degrees and another at 45 degrees. Confirm model, stock and tabs stay registered; change the frame origin and a shared tab, then regenerate both strategies. Cancel frame edits and save/reopen.
7. Inspect material removal with a representative simulation, including residual
   stock connecting the model to surrounding stock. Record the simulator and its
   limitations. Software acceptance does not authorize sending code to a machine.

Each job uses three-axis machining; Indexed Setup creates additional manually indexed sides. Geometric tabs are shared only
by supported Parallel/Waterline operations; they deliberately leave extra stock
at corners and retract over bridges. They are not clamps, fixtures, or holders.
An indexed job shares its source stock/model/tabs, with a 180-degree flip by default, configurable X/Y/Z axis and angle, and stock-top or custom work origin. Generate/post each job separately; no rotary motion is inferred. Tilted bridges use conservative XY envelopes and may leave additional stock.
Mesh-clone/tab recomputation requires the FreeCAD Plus Python modules.
