# Legacy dress-up, transformation and Boolean acceptance

Task eleven consists of three bounded native compatibility adapters. These expose
original operations in component History; they do not flatten native Body ownership
or reinterpret topology references as new shared Python operations.

## Dress-up

Part Design Fillet, Chamfer, Draft and Thickness retain original Base subelements,
neutral plane/pull direction, dimensions, formulas and native owners. Standalone
Part Fillet, Chamfer, Thickness, Refine and Defeaturing remain direct native outputs.
No topology spelling, feature identity or upstream geometry is replaced.

## Pattern and transformation

Linear, Polar, Circular, Path and Point Pattern, Mirrored, Scaled, MultiTransform
and combined Pattern retain native engines, Originals, transform modes, ordered
Transformations and references. Combined Pattern keeps both active and inactive
settings and authored suppression. History access rows follow the original Body
Group order across feature families where compatible with input dependencies;
referenced sketches precede consumers even when created later. Mutually connected
native transformation helpers retain authored order. Group, Tip and Origin remain intact.
Preservation coverage for Path/Point variants does not establish every custom path
or point-array editor behavior; whole-file qualification remains task twelve.

## Boolean

Part Design Boolean keeps its native Fuse/Cut/Common operation, original target,
tool Body references and legacy placement compatibility flag. Standalone Cut,
Fuse, Common, MultiFuse and MultiCommon retain their native inputs and outputs.
No separate Shape carrier duplicates native compound or external wrapper geometry.

## Identity, persistence and recovery

Hidden History access links have distinct UUIDs, explicit global original-source
and target references, and complete Body-times-feature placement expressions.
Original names/types/IDs/labels, formulas and source FCStd bytes are protected.
Shared instances continue to consume their original model. Native parameter edits
use the existing editor and transaction semantics; missing, mismatched or invalid
sources show Needs repair. Stale caches are reported without claiming freshness.

LegacyDressUpVersion, LegacyTransformVersion and LegacyBooleanVersion=1 upgrade
recognized older conversions after manifest validation. Upgrades are undoable and
idempotent; ordinary new Plus documents are excluded. Preserve editable native
features before the existing explicit dumb body/sheet/curve/point structural
recovery ladder. Missing output must never become a fabricated successful result.

## Verification

`TestLegacyFinishing` covers native references and identities, placed shared
instances, geometry differences, conversion/edit undo/redo, formula edits, protected
FCStd bytes, cold cadprt restore, prior-file upgrades, missing sources and stale
output. Actual Qt History double-clicks open native Fillet, Linear Pattern and
Boolean editors; the native Fillet radius control exercises Accept, Cancel and
Undo/Redo. MultiTransform ordering and mixed-family History order, combined
Pattern inactive settings/suppression and direct standalone compounds are checked.

Use common migration suites for source-resolution and History-order regressions.
WORK_STATE records actual counts, source hashes, diagnostics and publication; owner
DOCX contains affected UI/UX only. Source-mode acceptance is separate from batched
owner packaging, physical/high-DPI editing and task-twelve whole-file/external
consumer qualification.
