# Single Pattern item in Elements — November 24, 2026

Starting source/install: 0d70468d713e9e52aac06076913e958f42a13e63.
Owner instructed: “also finish making the pattern show as a single item in the
elements list instead of listing all the curves”. This authorizes completing the
previously presented native-widget prototype. Companion session 8aa0a38df7a0,
fingerprint 690ef0769a6580e879ec0fc901f53c2cff83f7d7742b570526cbed808ee66c6d,
was inspected: preview valid, no scope violations. No companion approval state
was changed on the owner's behalf. The [baseline](preview/baseline.png) is native;
the [proposal](preview/proposed.png) is a UI-only delegate overlay, not functionality.

## Implementation

TaskSketcherElements resolves the existing version-1 PatternDefinitions records
against persistent native geometry IDs and creates one actual QListWidget item
for each operation. Generated curves and helpers do not have individual hidden
or expandable child items. Original inputs and unrelated geometry retain their
ordinary native rows. The existing Pattern icon and authored counts label the row.
Unknown recipe versions and sketches without saved membership retain ordinary
rows; no geometric-position or type heuristic invents pattern membership.

Selection expands to native member subelements and viewport selection updates
the aggregate row. Filtering considers all member geometry types/states. The
checkbox and group context menu update geometry layers in a batch, honoring hidden
spacing helpers. Double-click/Return uses the existing deferred native editPattern
route and dedicated task. Done, Apply and Cancel keep their established behavior.
Deletion uses native geometry deletion and its Undo transaction; fully deleted
recipes are removed so later reused IDs cannot claim unrelated new geometry.
Constraint-list deletion continues to remove constraints while retaining geometry.

Patterns created without generated constraints now also save their operation UUID
and recipe, with an optional label in the existing version-1 record. They remain
free geometry, acquire no fake solver constraints, and can reopen through Elements.
Existing recipes need no migration. Pattern label allocation accounts for both
constrained and free operations. The original sketch, solver equations, spacing
chains, Equal constraints, units and native geometry data remain intact.

## Verification and delivery

The [installed affected suite](installed/result.json) passes all **102 tests**,
zero failures/errors, in 268.64 seconds. It includes the dense 20-by-20, 0.100 in
memory regression, spacing chains, Equal sizes, units, pattern editing, symmetry
and mirror preservation. Six focused native Elements scenarios cover 12-by-12
and 20-by-20 grids, free copies, angular/radial patterns, multiple groups, filtering,
viewport selection, visibility, deletion, Undo, renumbering and task completion.
The final Delete-action correction and ordinary-geometry visibility fast return
are followed by the [final installed six-case rerun](installed-final/result.json).
The solver itself was not changed; native C++ solver tests were not rerun.

[Fresh-process acceptance](fresh-reopen/result.json) opens, edits through the
actual Elements row, saves and reopens four files: a new 20-by-20 grid, free copies,
angular/radial geometry and the pre-update dense inch-grid fixture. Both grids
edit to 21-by-20 while keeping one operation row. The fixture's original circle
and source construction lines remain separate. Original owner documents are not
modified. The [existing desktop shortcut](shortcut/result.json) checks the row's
double-click/Return entry, Cancel, Done and Apply behavior.

Actual native captures: [12-by-12](installed-final/elements-grid12.png) and
[20-by-20](installed-final/elements-grid20.png). These show three actual rows:
one unrelated line, the source circle and the Pattern operation. They are working
native widgets, not the earlier preview overlay. Measured full-suite task Apply
times remain 4.35 seconds for the fixed-line 12-by-12 and 15.82 seconds for the
400-circle benchmark; these are local measurements, not universal guarantees.

Four installed files have SHA-256 hashes and original rollback backups recorded
in install-manifest.json. Native compilation is recorded in build.log. The existing
shortcut target and working directory are unchanged. Restart FreeCAD Plus to load
the native/Python update. The bounded harness uses isolated profiles; owner files,
private preferences, executables and build outputs are not committed. The unrelated
project.previewfirst.json remains untouched.
