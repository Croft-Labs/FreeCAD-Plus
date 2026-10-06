# Legacy extrusion conversion

Task six extends `LegacyConversion` and the shared component Extrude services.
Run `TestLegacyExtrusions` against this fork's native GUI with the current source
Part modules and exact `freecad.gui.ComponentNavigator` / `ComponentExtrudeTask`
modules loaded. Initialize GUI startup before overlays; GUI package attributes can
otherwise still refer to an older installed module. Assert the edited task's actual
source path. Use the designated validation directory for all profiles and fixtures.

## Mapping and identity

Qualified native identity-frame Body histories consisting of independent sketches
and a sequential Pad/Pocket chain move their original inputs/operations into component
History. Preserve names, native types/IDs, UUIDs, labels, expressions and native
extent properties. Each feature's original previous BaseFeature is mapped to a new
explicit published result; ConsumedResults records the target. Intermediate results
are hidden/background objects. The original Body remains the final Result, with its
native Origin/view provider and internal child-scoped Tip bridge to the last producer.
Original feature names still serve direct downstream references. Every migrated
feature and final Body passes volume and bidirectional native solid differences.

Admission checks complete Group/Tip, actual BaseFeature chain, profile ownership,
native state and valid single-solid output. Preserve native Length/ThroughAll/ToFirst/
ToLast, symmetric/two-sided lengths, start offsets, taper, normal vectors,
reverse and refine without translating their enumerations or rewriting formulas.
The shared editor reads native Pocket extents and profiles. Pocket's legacy inverse
normal is normalized at the UI boundary and reversed back when configuring Pocket;
the original Pocket native type is retained. Pad/Pocket mode/target edits use the same
object and update consumption; New Body clears its target. Self/downstream target
cycles and expression overwrites are rejected. The prior pilot's temporary mode gate
is superseded by this qualified native engine path; its self-target refusal remains.

Independent normal, positive one-sided solid Part Extrusions keep their native
object/profile/direction and gain a published editable result. Their native operation
kind remains New Body; changing it would require a different Boolean object, so create
a separate operation. Custom directions, reverse-side lengths, taper and sheet/curve
outputs retain native properties/editor rather than silently normalizing them.

## Retained histories and upgrade

Nonidentity/expressed Body frames, Body-attached/dependent sketches, mixed families,
selected profile subelements, custom vectors/linked axes, referenced start/limit definitions, signed
lengths and invalid/unverified outputs retain native ownership and parameters.
Hidden distinct-UUID History links open the original Pad/Pocket editor. LinkTransform
is false; native Body.Placement * Feature.Placement preserves the complete frame.
LegacyExtrudeTarget records the conversion-time native BaseFeature; the original
feature's BaseFeature remains authoritative after native edits. These links are
editable access to retained engines, not promoted component operations/results.
Missing/mismatched/invalid source links show Needs repair. No fake solid or frozen
replacement is created for a valid native feature awaiting its family/frame mapping.
The shared explicit evaluated dumb recovery policy remains available for failed
structural mapping; unavailable/stale outputs remain reported.
Native custom-vector Pocket output retains the original engine: an experimental
shared scratch preview lost the profile's elevated frame and is not qualified.
Preserve native directions/parameters and editing instead of claiming equivalent
preview or freezing the available body. Further custom-frame promotion remains an
integration gate; the retained native output and parameter edits are tested.

LegacyExtrudeVersion=1 makes conversion idempotent. Recognized older converted files
upgrade in the existing post-manifest native transaction. Earlier sketch UUIDs and
access-link identities survive promotion; old links become hidden Internal references
following the independent sketch frame, while History presents the original sketch.
Ordinary new component documents remain outside the legacy upgrade. Original FCStd
files stay protected; save converted content to new cadprt files.

Explicitly reopening a known definition tab rebinds its requested component context
after native Undo has restored a master view context. This changes view metadata,
not model ownership, component placement or saved geometry.

## Acceptance and remaining integration

The focused suite covers original identities/labels, explicit results/consumption,
shared LinkTransform world geometry, native Add/Subtract/New Body mode changes,
retargeting, expression edits/refusal, through-all, two-sided taper, conversion/edit
Undo/Redo, original bytes, cold reopen/further edits, older-file identity upgrade,
retained attached frames/targets, standalone extrusion and missing-source repair.
Actual Qt History double-clicks exercise shared Pocket Accept/Cancel and native
retained Pocket editor close. Reopen the definition tab after Undo/Redo using the
real panel path; do not substitute direct task launch for that event check.

Rerun prior migration, component edit-rollback and curve-profile regressions for
shared-service changes. WORK_STATE owns final counts, source hashes and publication.
Owner DOCX contains only affected interaction requirements. Source-mode acceptance
does not qualify the installed owner payload; packaging remains batched. Arbitrary
mixed feature/reference-frame promotion and cross-workbench/external-consumer
qualification remain later adapters and task twelve.
