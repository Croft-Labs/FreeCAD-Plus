# Legacy Helix and primitive migration acceptance

Task ten implements two bounded adapters, sharing native chain publication and
retained-operation access while keeping their parameter laws separate.

## Helix contract

Independent native AdditiveHelix/SubtractiveHelix histories retain original
profile/axis references, names/types/native IDs/UUIDs/labels, native parameter mode,
pitch/height/turns/angle/growth, handedness, direction, tolerances, refine and
expressions. Supported sketch axes and already-authored native parameter laws map
without resetting initialization. Body-dependent/attached/external/non-sketch axes,
whole-sketch subelement ambiguities, uninitialized/deprecated settings, unsupported
or stale outputs retain their native ownership, editor and available geometry.
Standalone Part Helix remains a native curve with its original controls.

## Primitive contract

Box/Cylinder/Sphere/Cone/Ellipsoid/Torus/Prism/Wedge additive/subtractive histories
retain native dimensions, placements, shape types and identities. Independent
placement maps; attachment/frame expressions and unsupported histories remain
native. Converted shape changes require a separate operation so the original type
and name survive. New Plus shape replacement remains unchanged. Standalone Part
primitives keep their native engines/editors and original finished outputs directly.
Do not add a duplicate Shape carrier to native compounds or external wrappers.
Tab is not a native primitive and remains deferred.

## Common persistence and recovery

Both adapters use the existing qualified native chain publisher, including bounded
mixed prior-family chains. Profiles precede operations; intermediate results provide
explicit BaseFeature/ConsumedResults targets. Original final Body, Origin and view
provider survive through the existing child-scoped Tip bridge. Every mapped feature
and final Body must pass volume and bidirectional solid differences. Parent/shared
instance placements and original FCStd bytes remain protected.

Converted Add/Subtract/New Body edits retain original native types through persisted
Boolean presets. Formula-driven settings use properties; cyclic targets and invalid
or ineffective edits fail without corrupting saved parameters. Retained History
links have distinct identities and complete Body/feature placement expressions;
missing/mismatched/invalid sources show Needs repair. Native Common/no-material and
unverified histories stay editable rather than being reinterpreted.

LegacyHelixVersion/LegacyPrimitiveVersion=1 upgrade recognized older conversions
after manifest validation, preserving earlier input/access identities and labels.
Ordinary new Plus documents are excluded. Native editability precedes shared explicit
dumb body/sheet/curve/point recovery; stale or missing output remains reported.
Whole-file/external consumer qualification and owner packaging are later integration
gates, not established by a dialog or source-mode tests.

## Verification

`TestLegacyHelixPrimitives` exercises all four Helix modes and eight placed primitive
shapes, exact axis references, native geometry/previews, shared instances, original
types/identities, explicit targets, mode changes, conversion/edit Undo/Redo, cold
cadprt restore/further recompute, original FCStd bytes, formula protection, shape
switch refusal, rollback, retained native editor events, attachment/reference-axis
retention, stale output, standalone solids/curves and previous-file upgrades.
Actual shared History events cover Preview/Accept/Cancel and reopening after undo.

Run full shared Helix/Primitive and prior Pipe/Loft/migration/recovery suites for
the common publisher/editor changes. WORK_STATE owns actual counts/hashes,
diagnostics, DOCX render/inspection, cleanup and verified publication. Owner DOCX
contains only affected UI/UX; technical contracts and evidence stay in Markdown.
