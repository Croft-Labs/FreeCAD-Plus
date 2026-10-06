# Legacy Origins and datum attachment frames

Task four uses `LegacyConversion.migrate_datum_frames` in the existing structural
transaction. Native Origins, OriginFeatures, datum planes, axes, points and
coordinate systems keep their names, types, labels and native identities. Allocate
component UUIDs only where missing. Never replace/reparent Origins or rewrite their
roles, native attachment supports, offsets, reversals or formulas.

Direct component-owned datums remain direct History inputs with role Object. They
are construction frames, not physical solid/sheet results. Body-owned datums keep
their original native owner, attachment engine and dependent native sketches.
History exposes an App::Link with a distinct UUID and a global LegacyDatumSource
reference to the original. The source and the link are not component definitions
or assembly occurrences; shared component instances continue to use one definition.

The link has `LinkTransform=False` and a complete local frame:
`Body.Placement * Datum.Placement`. Native attachment engines read the Link's own
frame; storing only the Body frame would lose datum offsets and rotations. The
native placement expression follows edits to either frame. The Body's and its
siblings' placements, native Group/Tip and all old support pointers remain intact.
Construction links initially have Visibility=False and do not enter ResultObjects.
Their unbounded native datum display faces must not become physical result geometry.

Double-clicking the retained datum or its History link opens the original native
attachment editor. It does not reinterpret legacy attachment modes as the new
PlaneDefinition interface. ComponentPlane.apply refuses destructive redefinition
of these retained inputs; their native editor/property fields remain available.
Invalid native datums can open their editor for repair; missing sources report
Needs repair and cannot supply geometry. ComponentSketch lists linked native planes,
and native/managed attachment calculations use the complete frame. ComponentPlane
resolves plane/axis/point references through the original native datum frame.

## Persistence and upgrades

`LegacyFrameVersion=1` makes mapping idempotent. Previously converted legacy cadprt
files upgrade through `upgrade_datum_frames` after the stored native manifest has
been verified. LegacySource or the recognized structural/recovery conversion report
identifies prior legacy content, including conversions of unsaved native documents.
Ordinary new component documents are not reclassified merely by opening them.
The upgrade is one undoable transaction and changes the in-memory document; saving
writes the updated manifest/history through the existing native persistence guard.
Legacy originals remain protected. Do not treat an old manifest mismatch as an
upgrade candidate or bypass identity/schema validation.

Nonstandard nested owners remain native with explicit conversion reports. Body
feature/sketch promotion, arbitrary expression rebasing, full attachment repair and
feature-family conversion remain tasks five onward. This phase intentionally retains
native datum definitions and associations; it does not claim all native Body feature
histories are flattened. The existing explicit dumb evaluated output policy remains
available for structural failures, preserving native payloads and reporting stale
caches or unavailable geometry. Broader workbench/whole-file consumers remain task twelve.

## Native verification

Run TestLegacyDatumFrames and the legacy inventory/structure/Body suites in the fork
GUI with isolated profiles and explicit source overlays. Run TestComponentPlaneFrame,
TestComponentPlaneTask and TestComponentBackgroundResult for changed shared services.
Record runtime module paths/hashes and actual native exit; do not call source-mode
results installed-payload acceptance. Raw profiles, CAD fixtures, captures and renders
belong only in the owner validation directory and are deleted after evidence is
summarized in WORK_STATE and the roadmap.

Coverage includes native Origin/datum identities, supports and Body Group/Tip;
rotated/transformed frames; shared LinkTransform modes and solid differences;
native planes/axes/points/coordinate systems; datum offset and Body placement edits;
Undo/Redo; cold cadprt reopening and further edits; upgrading older converted content;
new associative component sketches following retained planes; missing-source refusal;
and real Qt History double-click opening the original native datum editor with
support/offset preservation on close. Existing plane workflow, source-file protection,
explicit dumb recovery and background-result regressions remain required.
