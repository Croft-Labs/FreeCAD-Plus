# Pattern layout, previews, shared sizes and task completion

Owner approved the [concrete Qt proposal](../pattern-corrections-preview-20261124/README.md)
with “Approved. Implement”. Companion `6469d946a798` remained fresh with no scope
violations; chat approval is authoritative and tool approval state was not changed.
Implementation baseline: `7aae9779ca`; installed starting code: `9a17cbdd93`.

## Behavior

Pattern controls fit narrow docks. Direction method and reference occupy separate
rows, fields size to available width, labels wrap and independent extents retain
six-decimal values and units. Done is on the left and Apply on the right in Pattern
and Mirror, the two audited task completion pairs. Other OK/Cancel/Apply dialogs and
selection-step Done controls retain their workflows.

Each completed selected pattern direction previews immediately. Adding the remaining
direction expands to the full grid or angular/radial arrangement. Invalid or missing
inputs clear the affected preview; full-operation Apply remains disabled until valid.
Cancel/Escape discards only pending work. Done applies valid pending work and closes
the tool, leaving sketch editing active. Empty Done closes without another apply.
Incomplete or failed Done keeps selections and reports the problem. Apply commits,
clears geometry and reference selections, and retains mode/numeric/options settings.

Spacing lines/arcs are computed by the same chain traversal used for committed
geometry, through a transient geometry collector with no document, constraints or
transactions. A non-pickable Coin overlay uses the native construction color and the
sketch's global placement. Hide spacing chain and Create spacing constraints control
its presence; tool exit, invalid input and Apply clear the overlay. Toggling Hide while
geometry is pending does not change existing saved chain visibility. With no pending
geometry, the prior saved-chain visibility control remains available.

Original diameter, radius and actual line-length drivers remain on the original;
copies receive native Equal constraints instead of duplicated driving measurements.
Source expressions and reference measurements remain intact. Independent spacing
drivers are retained. Unconstrained lines/arcs retain endpoint-based shape relationships:
adding redundant Equal there can reduce source freedom at singular initial positions.
A projected X/Y distance is treated as a curve length only with a driving native
Horizontal/Vertical relationship; otherwise endpoint chains carry the projection
without imposing an extra length constraint. This distinction is covered by a
source-orientation regression, as well as horizontal length and diameter cases.

No new persistence schema. Existing native Equal constraints, construction helpers
and saved helper identities carry the result. Previous unit/precision metadata and
compatible symmetry diagnostics are preserved.

## Validation and delivery

Native build succeeded. All [88 C++ sketch tests](native/tests.txt) and
[68 final installed application checks](installed/tests.txt) pass with zero failures
or errors. The projected-distance regression caught and verified the source-freedom
distinction above. A [fresh process reopened five saved files](fresh-reopen/result.json),
including editing the saved original radius and verifying both Equal copies follow.
The [existing desktop shortcut passed four completion checks](shortcut/result.json).
All six installed hashes match the [delivery manifest](install-manifest.json), which
also records original-file rollback paths. The [build log](build.log) and bounded
[verification harnesses](harness/) are retained.

Actual installed/native screenshots (not simulations):

- [Narrow Pattern task and button order](native-narrow-pattern.png)
- [Visible spacing lines and angular arcs](preview-chains.png)
- [Hide spacing chain enabled](preview-hidden.png)
- [Mirror task](symmetry-ready.png)

Acceptance covers actual narrow task widgets, partial linear/angular/radial previews,
visible/hidden helpers, no preview document mutations, original size propagation,
source freedom, invalid input and apply-failure recovery, Done/Apply/Cancel, native
Mirror options and repeated operation, undo/redo, symmetry, precision/units and
fresh-process saved files. Existing tests were updated only where their expected
Done-discard or Apply-retains-reference behavior was explicitly superseded.

Source scope: Pattern Python task/geometry service, native Mirror handler, focused
tests and CMake test packaging. No unrelated app functionality, coordinate graphics,
preferences, user documents or shortcuts changed. `project.previewfirst.json` is untouched.
Original installed files are backed up; restart FreeCAD Plus to load the native update.
