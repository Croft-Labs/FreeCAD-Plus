# Legacy Models and Part Tree conversion

Task two routes `CadDocument.convert_legacy` / standard native File Open through
`LegacyConversion.convert_structure`. Existing App::Part containers become
definitions without replacing native names, Origins or geometry objects. The file
master is permanent and separate. Placed containers become linked occurrences;
existing scalar Links are reused with occurrence-local identities and shared targets.

Standalone Bodies and linked geometry receive component wrappers. Bodies inside
Parts remain native history/result payloads; their Groups, Tips, sketches, constraints
and feature objects are preserved. Links to internal features use definition-owned
geometry links without removing the source from its native Body. Native outputs
are exposed directly in ResultObjects: publishing a second copy would duplicate
Part compound geometry. Operation/result history migration belongs to task three.

Definition frames preserve original native world locations after separation.
Placed container occurrences retain their previous local placement. Existing Links
retain transform/scale modes with frame compensation, including scale conjugation;
their numeric placement may change when required to preserve the same displayed
geometry under the new definition frame. Never drop nonrigid matrix components.
Native Link forwarding must not confuse definition and occurrence ObjectIds: identity
allocation occurs while unbound, followed by restoring target/frame/scale settings.

Each document converts in one undoable native transaction. External documents
convert in memory first, preserving shared references and original file bytes.
Their transactions are independent; this is not an all-files atomic Undo operation.
Protected legacy paths may remain as native reference bases for external relocation.
Save external definitions to new cadprt files before the parent. The manifest refuses
unsaved/non-cadprt external definitions and prevents writing LegacySource originals.
No source archive is automatically overwritten. Standard GUI save dialogs use the
existing component format filter; source-mode acceptance is recorded separately.

Unresolved Links remain missing Part Tree instances with explicit repair reports;
strict save validation requires repair. Link arrays currently retain their native
payloads and recover a validated frozen compound in a component definition, explicitly
labelled geometry-only. Array element identities remain separate from target IDs.
Array instance semantics/parametric adapters are not claimed as fully migrated.

If a structural adapter cannot safely map expression-driven or nonrigid frames,
or a native expression consumes a local Part frame that would change on separation,
conversion retains the original hierarchy/native payloads and exposes captured valid
top-level outputs as explicit dumb geometry. Visible outputs are preferred; hidden
outputs are used when no visible evaluated output exists. Cached output with touched
or invalid dependencies is reported as unverified. If no usable geometry exists,
the report states that rather than fabricating an output. Frozen recovery loses
parametric component editability; retained native objects remain repair evidence.

Run `TestLegacyStructureConversion` plus `TestLegacyConversionPlan` in the native
fork runtime. Checks include rotated/nested Parts, both LinkTransform modes, repeated
definitions, scaled instances, internal Body links, native Body/sketch history,
idempotence, Undo/Redo, primitive recompute, FCStd original protection and cadprt
reopen, external save ordering, missing-instance refusal, arrays and failure recovery.
The GUI checks exercise the actual standard Open dialog and inspect Models/Part Tree
with the permanent master first. Bidirectional native Boolean differences prove
geometry/placement equality; equal volume alone is insufficient. Loaded source
validation is distinct from installed owner payload acceptance. Batch packaging
and broader consumer/reference qualification with subsequent integration.
