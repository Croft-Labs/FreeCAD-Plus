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
Probe-precision fixtures preserve sub-0.01 mm XY coordinates and a 0.123456 mm
constant height through the native interpolated surface and corrected path. Identical
XY/Z repeats are deduplicated; differing heights at exactly the same parsed XY
are rejected in either file order, with export rejection and recovery. No implicit
rounding, averaging or near-point merge tolerance is introduced.
External file edits still require recompute; automatic filesystem monitoring and
arbitrary probe-grid quality are not established by these tests.

## Dragknife and Ramp Entry failure checks

`tests/TestCAMInvalidInputs.py` covers Dragknife missing/empty base cleanup and
injected generation failures for both Dragknife and Ramp Entry. Recompute must
leave no old commands; generation failures must block postprocessing through native
error state, and corrected inputs must regenerate/export. Run with nested dressup
postprocessing and `CAMTests.TestPathRampEntryGenerator`. These bounded fixtures
exercise failure handling and recovery, not general dragknife corner geometry or
physical cutter clearance. Native recompute may still skip a downstream consumer
when its producer fails; the shared export guard remains necessary.

## Plunge Milling failure checks

`tests/TestCAMInvalidInputs.py` validates Plunge Milling with a positive-feed native
CAM fixture. Injected edge-conversion failure must clear old output and block export;
zero/negative stepover must produce a native error rather than a valid empty result.
Restoring generation or a 1 mm stepover must recover exported commands. These checks
cover bounded failure handling; they do not certify drilling cycles, holder clearance
or physical plunge-milling suitability.

## Shared dressup lookup compatibility

`tests/TestCAMInvalidInputs.py` checks custom-named nested Array/Mirror objects,
missing-link/default-tool behavior, a restored custom-named Array, and legacy
single-link dressups. Ordinary operations and geometry LinkSubList inputs must not
be traversed just because an internal name contains Dressup. Iterative traversal
is exercised with a 1500-element chain and a cycle; cycles raise a clear error.
Run with nested postprocessing, Array, Dogbone, holding-tag and ramp-generator
suites because they share this helper. Recognition covers current Path.Dressup
proxies and the retained legacy naming/shape contract; arbitrary third-party proxy
namespaces are not automatically certified. No document schema migration is added.

## Shared operation traversal

`tests/TestCAMInvalidInputs.py` verifies property lookup through 1500 Base links,
explicit false/None overrides, missing-property defaults and cycle rejection.
Job traversal visits each operation once in outer-before-base order, including
shared bases and compound groups. Native shared Array bases are checked through
model removal/recovery; deep and cyclic graphs use duck-typed fixtures. Run with
nested dressups, Array, Dogbone, holding tags, ramps and both utility suites. A
job traversal tolerating a cycle for invalidation/cleanup does not make that model
valid for generation or export.

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


## Related profile holding-tag failure regressions

`TestCAMInvalidInputs` also exercises the inherited profile holding-tag dressup,
which is distinct from the stock-bridge tabs used by mesh machining. Removing its
base clears the old path and tag preview data; restoring the base regenerates them.
A deliberately injected processing failure leaves an empty path and native Invalid
state; postprocessing rejects it instead of exporting the untagged base path.
Removing the fault restores generation. Pair this suite with
`CAMTests.TestPathDressupHoldingTags` for the native tag geometry regression group.
These automated checks do not replace simulation or physical-machine acceptance.


## Related Boundary2 failure regressions

`TestCAMInvalidInputs` exercises Boundary2 with a solid boundary around a generated
surface path. An injected late feed-assignment error must clear the previous path,
mark the feature Invalid and block postprocessing. Injected null and planar offset
results must also reject before clipping. Removing each fault must regenerate a
usable path. This supplements the older Boundary dressup checks; native GUI/machine
acceptance remains separate from these automated failure/recovery tests.


## Dressup dependency-readiness regressions

Boundary2 and holding-tag tests attach a real failing producer to their inputs and
retain cached input geometry/path. Native recompute can skip downstream execution,
leaving its old output; the existing postprocessing guard must reject that cache.
Explicit dressup execution must then raise for the invalid dependency and clear
output. Repairing the producer must restore generation/export. These checks cover
`execute` input readiness; they do not establish automatic cache clearing during
skipped native execution or validate every direct task-panel callback.


Direct holding-tag method checks additionally inject createPath failure through
processTags, verify empty output/solid preview data and successful retry, and call
setXyEnabled with a failed upstream dependency. Saved Positions/Disabled must remain
unchanged on that rejection; after repair the new position generates a usable path.
These are native proxy-method checks, not physical task-panel input acceptance.


Holding-tag setup tests inject missing controller/tool and zero/infinite diameter,
requiring empty output plus cleared path/tool caches, export rejection and recovery.
Point-query tests use a failed native upstream producer to ensure pointIsOnPath and
pointAtBottom reject cached input and work after repair. Queries now rebuild path
analysis; interactive performance has not been benchmarked by these checks.


Boundary2 linking checks lower the clipping volume below safe height to remove
original high links, force the real linking generator between separated cuts,
and verify feed moves below safe height plus final clearance retraction. Moving
the boundary entirely away must produce no commands; restoring it must regenerate
cutting moves. These are native path tests, not machine or physical UI acceptance.


Array and Mirror readiness regressions attach a producer to the base path and
exercise both unrecomputed and failed states. Explicit generation must reject
cached inputs, clear output, and recover after recompute/repair; postprocessing
must reject the stale dependency. Mirror additionally checks its disabled-axis
passthrough and failed reference-offset geometry. Native skipped execution can
still retain old output until explicit execution; export rejection is separate.


Axis Map and Z Correction use the same dirty/failed-producer checks as Array and
Mirror: explicit generation must reject cached base paths and recover after
repair/recompute. Z Correction additionally must clear its interpolation surface
when the base is missing or stale, then rebuild that surface on successful retry.
These checks do not establish machine acceptance or change native skipped-recompute
behavior; cached downstream output remains subject to the existing export guard.


Dragknife and Ramp Entry also run the shared dirty/failed-base regression: export
must reject stale dependencies, explicit generation must clear output and raise,
and repaired/recomputed inputs must regenerate usable paths. The existing missing
input and injected generation-error checks remain part of the grouped suite.


Plunge Milling and the original Boundary dressup exercise the same dirty/failed
base rejection and recovery checks. Boundary additionally attaches a failing
producer to its stock, retains cached stock geometry, and verifies that explicit
generation rejects it and clears output; repairing the producer restores paths.
Export rejection remains separate from native skipped-recompute cache behavior.


Dogbone readiness checks reject dirty/failed base paths and clear machining/corner
caches. Invalid-tool checks cover missing controller/tool and zero, negative or
infinite diameter, export rejection and repair. Existing Dogbone corner geometry
unit tests supplement the native SurfaceScan failure fixtures, which do not
exercise actual corner insertion. Test doubles expose clean dependency state.


Plunge Milling motion checks require explicit clearance before the first XY move
and at completion, and a safe-height retract between generated plunge positions.
Drilling cycles carry the controller's vertical feed and cancel with G80 before
subsequent travel. A zero vertical feed must reject output/export and recover when
repaired. These are command-level checks, not postprocessor or machine acceptance.


Plunge cycle variants cover G82 dwell, G83 peck and G73 chip breaking with explicit
feed, expected P/Q and R values, cancellation, safe-height retract and final
clearance. Negative dwell, combined peck+dwell, and chip breaking without
peck depth must clear output, block export and recover after repair. Controller
postprocessing and physical machining remain separate acceptance gates.

Native negative peck-depth assignment is checked as normalization to zero before
execution; it is not claimed as a generator rejection.


Plunge Milling post/persistence probes use its native peck-cycle output with the
real LinuxCNC and Grbl processors in a mock job/configuration wrapper. LinuxCNC
must preserve canned-cycle parameters and cancellation/retract sequences; Grbl
must expand cycles to ordinary moves while retaining retract heights. A disposable
FCStd fixture must preserve cycle settings and regenerate identical commands after
reopen. No controller connection or physical machine is involved.


Holding Tab and Indexed Setup command regressions invoke Command.Activated with
a selected job. Creation must open the owned task transaction; cancellation must
remove created objects, and an unrelated pending transaction must remain intact
when creation is rejected. Holding Tab accept/edit/Undo/Redo are also exercised.


## Indexed per-setup post output

Run `tests/TestIndexedSetupExport.py` through the same source-built GUI harness,
with the checkout's `tests` directory on `sys.path`. Pair it with
`CAMTests.TestMeshMachining`, `CAMTests.TestDressupPost` and
`TestCAMInvalidInputs` when changing indexed operation dependencies.

The fixture imports an STL, creates real 180-degree and 45-degree indexed Jobs,
and posts Parallel/Waterline separately through LinuxCNC and Grbl. It supplies a
three-axis metric machine configuration, six-decimal axes and an explicit
`G17 G90` preamble. These are configured-output checks, not factory-default or
controller certification. The independent linear-motion decoder compares every
XYZ endpoint and rapid/feed mode to the generated operation within 0.000001 mm,
checks final clearance and rejects rotary words. Sampled cutter/tab clearance is
also checked on the exported motion; no material-removal simulator is used.

Shared-tab edits must reject export until recompute and then change both indexed
Waterline outputs. An independent custom-origin edit must preserve the other
setup's path. Reopening must preserve saved commands exactly and allow posting
regenerated operations with the same output/native-path and tab-clearance checks.
Contour repeatability is not closed by this test: the bounded 45-degree Waterline
probe found up to 0.172558 mm bidirectional endpoint/midpoint distance after
regeneration, whereas the 180-degree contour differed only at floating precision.
This remains recorded under roadmap 6.4.3; no unchanged-contour claim is made. With
`FREECAD_PLUS_VALIDATION_DIR` set, the `.nc` fixtures are retained under
`indexed-output` for review. No output is sent to a machine.

Indexed generation consumes recomputed producers; it must not directly execute
model/stock proxies and leave them dirty. Indexed stock is an explicit operation
dependency. Direct generation with stale indexed inputs rejects and clears the
old path; the existing post guard remains in force.
