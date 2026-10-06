# Legacy Body history foundation and Sketch to Pad pilot

Task three extends `LegacyConversion.convert_structure` inside its existing native
transaction. `body_history_plan` admits only the proven independent Sketch → first
Pad history. `migrate_body_histories` preserves native Sketch, Pad and Body names,
types, labels, document identities and downstream references. Component History
orders the original sketch and Pad before the original Body, which is the final
result carrier. Multiple occurrences continue to share that definition.

The native Body Tip property has child scope. A hidden internal
`PartDesign::FeaturePython` bridge remains inside the original Body and copies the
editable Pad output, including its placement. Its `PropertyLinkGlobal` producer
points to the component-owned Pad. The Body retains its native Origin and native
view provider. `LegacyTip` and `LegacyBodyHistory` record the old Tip and native
membership; `Producer` records the editable Pad. This is not a frozen output or
a replacement Body. No native feature implementation or persistence schema is
replaced. The bridge proxy persists through the existing native archive envelope.

Registration must not re-add an object already owned by its component: native
group addition can expand local-scope dependencies and move a Pad out of its
Body. Structural legacy registration uses explicit membership for unowned
objects, retaining sources of pre-existing cross-Part consumers. Native result
views lacking a Python Proxy remain native. These ownership and display fixes
are shared prerequisites, rather than a second migration model.

## Admitted boundary and retained payloads

The pilot accepts an identity Body frame, one native Pad Tip without a BaseFeature,
an independent native sketch owned by that Body or its component, and a one-sided
normal length extrusion without taper or attachment/external/subelement sketch
inputs. Sketch placement is retained, including a nonzero offset. The pre-edit
geometry freshness snapshot distinguishes stale source caches from normal touches
caused by structural annotation. Conversion verifies the output with volume and
bidirectional native solid differences before committing.

Pad length expressions stay native and respond to upstream constraint edits.
The shared Extrude editor refuses to overwrite expressions, and operation/target
mode changes for this pilot are refused until task six qualifies the full adapter.
Normal dimension editing, Sketcher editing, Cancel, Undo/Redo and cold reopening
use the existing component task and native recompute services.

Other Body histories remain native and editable with an explicit
`LegacyHistoryState` and conversion report. This includes nonidentity Body frames,
attached sketches, complex or unrecognized histories, unsupported extents and
unverified/invalid source geometry. Preserve available final output; do not claim
these retained native payloads are flattened or fully migrated. Task four now
exposes retained native datum frames without moving their dependent Body inputs;
see [datum frames](LegacyDatumFrames.md). Tasks five to eleven continue ownership
and feature adapters. If a mapping fails after admission, the structural
transaction aborts and the existing validated dumb body/sheet/curve/point recovery
path retains native payloads. Unverified cached output and unavailable geometry
remain explicitly reported, as specified in `LegacyStructureConversion.md`.

## Verification

Run `TestLegacyBodyHistory`, `TestLegacyStructureConversion` and
`TestLegacyConversionPlan` in the fork GUI, with an isolated profile and
`FREECAD_PLUS_VALIDATION_DIR` beneath the authorized validation directory.
Source-mode runs explicitly load the checkout's ComponentModel,
ComponentResultView, ComponentExtrude, CadDocument and LegacyConversion modules
and record module paths/hashes. Run `TestComponentBackgroundResult` for the shared
registration/view changes. Source overlays are separate from installed acceptance.

The pilot covers native identities, placed geometry and both shared LinkTransform
modes, independent sketch ownership, retained mixed histories and Body frames,
length expressions, original-file byte protection, downstream native Body
references, upstream constraint/dimension edits, cold cadprt reopening and edits
after reopening. Actual Qt History double-click events open Sketcher and the
shared Extrude task; Pad Accept/Cancel and native Undo/Redo preserve the result
carrier and internal bridge. Structural Undo/Redo is followed by native recompute,
then geometry comparison. A failure case exercises explicit dumb geometry recovery
while retaining the original native history.

The roadmap and WORK_STATE own actual results and publication evidence. Batch
owner packaging with later integration; no task-three source-mode result certifies
the current desktop payload. Later full extrusion/attachment/feature families,
topological repair across arbitrary histories and whole-file consumer acceptance
remain separate tasks.
