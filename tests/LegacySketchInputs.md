# Legacy sketch inputs

Task five uses `LegacyConversion.migrate_sketch_inputs` inside structural conversion
or the existing post-manifest legacy-input upgrade transaction. It retains native
sketch objects, names/types/native IDs, constraints, expressions, external geometry,
attachment engines, offsets and consumers. It does not copy a sketch per instance.

Component-owned sketches stay independent Object inputs. The narrow identity-frame
Sketch/first-Pad pilot now accepts native dimensional constraint expressions and
external inputs outside its Body history. It refuses native attachments, frame/property
expressions and dependencies on its own Body or Body-owned features, preserving the
editable native history until the corresponding feature adapter can map that frame.
Body placement, Pad extent and freshness guards still apply. No expression rewriting
or attachment-mode substitution is performed.

Other Body-owned sketches remain in their native Body Group/Tip dependency context.
Component History exposes a hidden App::Link with its own UUID, a global
LegacySketchSource reference and a complete native expression
Body.Placement * Sketch.Placement. LinkTransform=False strips the target frame,
so both display geometry and native consumers see the complete input frame.
These are input access links, not assembly occurrences or promoted operations.
They are not added to ResultObjects and do not duplicate physical output by default.
Sketch-to-sketch access links follow native dependency order before their Body.
Cyclic dependencies and nonstandard nested/unmapped owners are reported; retained
native payloads are not claimed as flattened histories.

History double-click edits the original sketch. Shared consumers and repeated
instances keep their original references. Missing/mismatched/invalid sources show
Needs repair; a missing source cannot open an editor. Native invalid sketches can
still be opened for repair. LegacySketchVersion=1 prevents duplicate conversion;
older recognized converted files upgrade only after manifest/identity verification.
Ordinary new component files are outside this upgrade. Undo restores the pre-upgrade
file in memory; save/reopen uses the existing versioned cadprt manifest.

The recovery order remains mapped editable features, retained editable native
features, then explicitly reported evaluated dumb body/sheet/curve/point where needed.
This task retains available native Body outputs and does not freeze a valid sketch
merely because its later feature adapter is pending. Original FCStd files stay protected.

## Native acceptance

Run `TestLegacySketchInputs` in this fork's native GUI runtime, explicitly loading
the current Part modules and ComponentNavigator from source. Confine profiles,
fixtures, logs and renders to the owner's validation directory. The suite covers:

- Original identities, rotated nested Body/component frames, native attachments,
  dimensional expressions, external references and both shared LinkTransform modes.
- Safe component Sketch/Pad mapping with dimensional expressions/external geometry.
- Native parameter/frame edits, recompute, Undo/Redo, protected original bytes,
  cold cadprt reopen, retained UUIDs and further edits.
- One independent sketch shared by native Pad and Part Extrusion, with both updating.
- Older-file idempotent, undoable upgrade; explicit missing-source repair.
- Native sketch dependency order and actual Qt History double-click/open/close of
  the original sketch with its native inputs unchanged.

Rerun the prior datum, Body, structure and inventory suites when changing migration
admission/metadata. WORK_STATE owns final counts, hashes and actual publication.
Source-mode acceptance does not qualify installed payloads. Physical promotion of
attached Body feature histories belongs to subsequent feature adapters; whole-file
mixed-feature/external-consumer qualification and owner packaging remain separate.
