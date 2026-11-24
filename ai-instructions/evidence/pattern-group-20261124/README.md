# Pattern groups and fixed-length grid speed — November 24, 2026

Starting source/install: `d15bc42713098bb0e298205e76e9da1310712ba2`.
The owner approved the single Pattern icon/list entry and complete hidden-chain
presentation in chat: “Approve this presentation”. The approved images were Qt
simulations, not installed functionality. [Baseline](preview/baseline.png) and
[approved proposal](preview/proposed.png) are retained separately from actual captures.

## Implementation

Fixed-length linear and radial-only line patterns retain native original-to-copy Equal
constraints and relative Parallel orientation. Both endpoint spacing lines and all
coincident connections remain. The second endpoint chain omits length/orientation
equations already implied by the first endpoint translation and copied line shape.
This avoids expensive redundant-system diagnosis without disabling conflict checks,
fixing source geometry, or discarding the spacing helpers. A projected X/Y distance
qualifies only when its source is already horizontal/vertical, respectively. Free
projected lengths and angular patterns retain their prior solver path.

Each newly created pattern's constraints have optional native XML attributes
`PatternGroup` (UUID), `PatternLabel`, and `PatternDriver`. Native solver equation
types, individual constraint identities and expression indices remain unchanged.
The real equations are retained; rendering uses cached display-only proxies and the
existing array icon. Only one row is exposed, with no expandable children. Original
source constraints remain separate. New patterns made from previously patterned
geometry get independent identities. Constraint cloning/Undo/persistence preserves
metadata; independent native constraint copies start without group metadata.

Group selection in the list includes its relationships. Standard GUI Delete expands
the group and removes its constraints in one batch, retaining geometry; Undo restores
it. Scalar/list visibility and virtual-space updates expand to the group. Native
low-level deletion remains individual for solver repair. Filtering considers a group
visible if any member matches. Double-click the group to choose a pitch and open the
existing native dimension editor, preserving six-decimal entry and explicit units.

Hide spacing chain hides every helper plus all grouped constraint graphics, including
pitch dimensions and Equal icons; the Pattern list entry remains available. Showing
restores one icon. The source's own dimensions remain visible. Existing legacy files
load without group attributes and retain their original independent constraints;
there is no speculative regrouping of older patterns. Legacy helper-related labels
are hidden with their chain. No new feature type or solver constraint type is added.

## Verification and delivery

The [installed application suite](installed/result.json) passed 66 checks and the
[Mirror regression suite](installed-mirror/result.json) passed 13: **79 total**, zero
failures/errors. [All 88 native Sketcher tests](native/tests.txt) passed after rebuilding.
[Fresh-process acceptance](fresh-reopen/result.json) covered saved fixed-line and
circle grids, renumbered groups and an older ungrouped file. The existing shortcut
passed [both real task/editor checks](shortcut/result.json).

| Installed operation | Apply time |
| --- | ---: |
| Fixed-length 12-by-12 lines, service | 3.811 s |
| Fixed-length 12-by-12 lines, task button | 4.116 s |
| Same line task through existing desktop shortcut | 4.042 s |
| Diameter-constrained 12-by-12 circles, task button | 1.365 s |

The previous fixed-line measurement was 57.284 seconds. These are local measurements,
not universal runtime guarantees. The line grid retains 430 geometry elements,
286 construction helpers, 1,145 constraints, 143 Equal copy lengths and two driving
pitches. Tests edit source length, source orientation and both pitches, inspect every
copy and coincident helper endpoint, check source freedom, toggle visibility, select
and delete the whole group, Undo, save and reopen. Native scenegraph assertions count
exactly one enabled group icon (plus the original dimension); hiding leaves only the
original dimension. The list contains one nonexpandable Pattern row.

The [initial optimization profile](initial-profile/profile.txt), taken before grouping,
records five explicit solves instead of the previous 40. Final installed timings above
include persistence and group rendering. Copied circle grids remain fast.

Build note: an intermediate relink encountered a locked DLL because an owned test
process was still using the build runtime. After the process exited, the final native
build succeeded. Early visibility test harness errors (ZIP/XML decoding and Qt OpenGL
binding initialization) were corrected before the passing installed runs. No product
failure or pending test is being omitted.
Actual native captures: [shown](installed/pattern-shown.png),
[hidden](installed/pattern-hidden.png), [constraint list](installed/pattern-list.png).
The original build and installation are retained. Four updated installed files have
SHA-256 verification and rollback backups in [the manifest](install-manifest.json).
Restart FreeCAD Plus to load the native/Python update. The existing desktop shortcut
and unrelated `project.previewfirst.json` are preserved.
