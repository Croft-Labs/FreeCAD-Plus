# Entered-unit persistence — November 28, 2026

Owner: save dimension presentation so editing later reopens in the entered units.
Baseline a7e80e1ba9. This extends the existing unit-entry contract; no layout changes.

## Repair

- Mesh: preserve per-field presentation units in MeshSettings and Advanced defaults;
  synchronize main/native controls even when only the units change at equal physical
  value. Advanced Cancel and recipe restore retain units. Legacy metadata is optional.
- Reference images: preserve mixed width/height/position units and calibration
  distance in ImageSettings. Apply validates/commits lengths, saves atomically, then
  resets presentation with the existing defaults. Reopen restores each field.
- Component instance patterns: preserve native InputField presentation in the
  existing Configuration recipe and restore it after loading physical values.
- Sketch-plane offset: save SketchPlaneOffset presentation through the shared
  QuantityPresentationUnits map inside creation/edit transactions and restore it.

Physical values remain in FreeCAD's native units; display-unit metadata is separate.
No migration or identity change is required. Older files without metadata retain
their numeric values and prior default-unit presentation; historical entered units
cannot be inferred when the earlier version did not save them.

Extrude/Revolve, datum planes, Shell/Thicken, sketch patterns, body transformations,
Trim Body and bound native quantity controls already have persistence paths. Those
paths are preserved. Movement/quantity-only placement creates no editable operation
recipe; this repair does not invent a movement-history feature.

## Verification

All 59 source checks passed, including five new save/reopen cases, existing instance,
image and mesh regressions, inch entry, body patterns and native bound quantities.
After adding user-facing handling for an invalid mesh value before opening Advanced,
all 10 mesh checks passed again. Mixed in/cm/mm fields, physical dimensions, same-value
unit changes, defaults, Cancel, Undo/redo, in-place edit and legacy recipes are covered.
Tests use isolated settings and generated files. Gmsh unit controls are tested without
claiming an external Gmsh generation run.

## Delivery and concurrent work

Changes were prepared in an isolated sparse checkout because another task was editing
result-name controls in the main checkout. Integration preserves those uncommitted
edits; they are not included in the unit-persistence commit or payload.

Installation initially waited for closure of the owner FreeCAD session. The committed
payload was subsequently installed with the approved feature-result naming update;
all five installed persistence checks pass. No running owner app files were replaced.
See [installation evidence](../result-names-20261128/README.md).
