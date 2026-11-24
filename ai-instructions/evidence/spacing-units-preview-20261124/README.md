# Spacing chains, precision and explicit units — UI review

November 24, 2026. **Preview only; awaiting approval of these new interface changes.**
Production source, native solver, installed application and saved documents are unchanged.
The prior approval for the first Sketch Pattern implementation does not approve
this subsequently requested interface. The owner has confirmed **one driving
length per independent pitch**, instead of a freely resizable equal-line chain.

## Requested behavior

Replace the pattern's repeated coordinate dimensions with native construction
spacing chains. Keep Create spacing constraints selected by default. Linear and
radial chains use equal lengths, parallel/collinear direction relationships and
coincident adjoining endpoints. A driving length controls each independent pitch.
Independent positive/negative pitches and the two grid directions retain their
own groups; symmetric extents share their pitch. Preserve the existing pitch/total,
instance-count, direction, reverse, symmetry, Apply and Undo semantics.

For angular spacing, use construction arcs with coincident adjoining endpoints,
centers coincident to the rotation center and equal angular spans. One driving
angular pitch controls each independent angular extent. Equal radius alone does
not enforce equal arc span and is insufficient. Concentric rings have the same
angular pitch and different arc lengths. Radial spacing across the rings uses
construction-line chains. Full-circle closure must not duplicate instances.

Add **Hide spacing chain**, initially unchecked, immediately below Create spacing
constraints. It hides line/arc helpers and their relationship markers, retaining
the actual pattern, constraints and driving dimensions. The hidden state must
survive save/reopen and be reversible without deleting helpers or changing them
into ordinary profile geometry. The control is disabled when chain creation is off.
Actual per-geometry visibility and persistence still require implementation.

All task-panel numeric value and dimension fields must support six-decimal entry,
independently of dimension-leader display precision. Preserve full stored values,
including existing higher-precision data; do not round model geometry when formatting.
Whole-number instance/count controls remain integers. Dimensionless values accept
decimal precision but must not accept incompatible physical units.

Dimensional fields accept compatible explicit unit suffixes. Store the chosen
presentation unit with the parameter/constraint and restore it when reopening
the editor, changing document units, copying, undoing and saving/reopening.
Bare numbers use the field's current unit. Expressions, dimensional validation,
native conversions, signed values, focus/Return commit and immediate spin stepping
must remain intact. Explicit alternate units must remain visible on leaders.

Preferences → General adds **Secondary unit system** and its **Display decimals**.
The existing primary system and its precision remain. The preview uses primary
millimeters/2 decimals and secondary decimal inches/3 decimals; preserve existing
primary preferences during rollout. Explicit units matching the secondary system
use secondary precision; primary and other compatible units use primary precision
without converting away from the explicitly chosen unit. Units shared by both
systems, such as degrees, use primary precision.

| Entered/stored presentation | Leader | Reopened editor |
| --- | --- | --- |
| `1.29999 mm` | `1.30 mm` | `1.29999 mm` |
| `0.100 in` | `0.100 in` | `0.100 in` |
| `0.123456 in` | `0.123 in` | `0.123456 in` |

This scope covers shared native quantity controls and the dimensional plain-spin
fields used by Plus task operations, not just Sketch Pattern. Existing labels,
values and features without explicit-unit metadata retain normal document-unit
behavior. Optional presentation metadata must be backward compatible and separate
from native numeric values; no expression or document/property identity migration.

## Direct preview screenshots

- [General preferences](preferences.png); [baseline preference section](baseline-preferences.png).
- [Six-decimal entry, leader precision and retained editing units](values.png).
- [Linear spacing chain](spacing.png); [same chain hidden](spacing-hidden.png).
- [Angular arcs and radial lines](circular.png); [same chains hidden](circular-hidden.png).

These are native Qt **UI simulations** using the installed FreeCAD runtime and an
isolated settings profile. General's existing `.ui` supplies the preference section;
numeric examples and diagrams are fixtures, not functioning solver/persistence
changes. Blue diagram lines/arcs represent construction helpers. The annotations
and simulation footer are review material, not extra production task controls.
Hide toggles operate on diagram items only. [Render result](result.json).

## Implementation investigation and acceptance requirements

Current `sketch_pattern._offset_point` adds coordinate dimensions per copied anchor.
`_transform_point` uses construction radii with equality/angle constraints. Replace
the placement relationships with chain groups while retaining source degrees of
freedom, independent extents, correct copies and rollback for invalid constraints.

Native `Gui::InputField` and `Gui::QuantitySpinBox` have quantity precision APIs;
Plus's plane/pattern controls still contain two-decimal `QDoubleSpinBox` fields.
Use a shared quantity-editing contract and audit callers; simply raising the global
UnitsApi decimals would also change leaders and would not retain entered units.
Sketcher `EditDatumDialog` initializes a quantity from the native datum;
`EditModeConstraintCoinManager` formats `getPresentationValue().getUserString()`
through global units. Both editing and labeling need persistent unit presentation.
Audit constraint lists/property editors and other task dimensions using these services.
General preferences live in `src/Gui/PreferencePages/DlgSettingsGeneral.{ui,cpp,h}`.

Required checks: linear/two-direction/independent/symmetric chains; angular/radial/
combined chains; editable master pitch and equal successors; source freedoms;
hidden helpers remain active and excluded from profiles; Undo/Redo, fresh reopen
and native downstream solids; six-decimal input across native and Plus tasks;
mm/in and degree/radian validation, exact stored values, rounded leaders and
full-precision edit reopening; explicit units survive document-unit changes;
expressions, copies, legacy documents, Plus/Classic and existing sketch workflows.

## Provenance

Companion session `2f5b603ce170`; clean fixture baseline
`b4e68770f65d28c73f988f043f1cc97b6bd12a46`; production baseline `80d830646b`.
Candidate allowlist: `General.ui`, `quantity_ui.py`. Final fingerprint:
`07824c6aa1e2695c8dda21f937fb9187156e63ad03566863017e39af76a10d6a`.
Capture/inspection: valid preview, no scope violations; approval false, never altered.
Fixture: `../spacing-units-preview/review-source`. Render harness copies are included
here for provenance; the active harness is in `../spacing-units-preview` and resolves
the production checkout as its sibling. No new app build or app clone was created.
Unrelated `project.previewfirst.json` is preserved.
