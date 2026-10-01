# Replace occurrence source: owner workflow test

This F022 pilot adds **Tools > Replace occurrence source...** for one unconstrained
native Link to a single solid or whole root Body in the same document. It reuses
the replacement definition; it does not copy it or modify the old definition.

Use this checkout's development build:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
The separately installed FreeCAD and published installers are unchanged.

1. Select a whole free Link occurrence in the tree, then open the command. The
   occurrence may be inside ordinary structural Part containers. Its current
   source and the replacement must be root solids/whole root Bodies.
2. Choose the replacement from **Replacement source**. Names include internal
   identifiers to distinguish equal labels. Unsupported or stale choices report
   the problem inline and disable Preview/Replace.
3. Check **Source placement: Included/Ignored**. The existing native setting is
   retained. Included uses the replacement's source placement as well as the
   occurrence's placement; Ignored uses its local solid geometry. Replacement does
   not invent a new alignment between differently designed parts.
4. Click **Preview**. The teal wireframe shows the proposed geometry in the existing
   occurrence frame, including nested structural Part transforms. Sources and
   document objects stay unchanged; Cancel removes the overlay.
5. Click **Replace**. Only the selected occurrence changes source. Its native ID,
   label, placement, visibility and uniform appearance override remain. If appearance
   was inherited, it follows the replacement source. Other occurrences continue to
   reference the old definition. Replace makes one Undo step and closes the dialog.
6. Undo/Redo, save and reopen, then edit the replacement's dimensions. The replaced
   occurrence follows those edits; instances of the old source remain unchanged.
7. Change a source or parent placement while the dialog is open. The preview clears
   and **Review again** is required after recompute. Deleting the selected occurrence
   or closing its document closes the dialog and removes the preview.

Limits: one occurrence, one solid, same document, unscaled direct Links only.
Driven/consumed occurrences, native assembly relationships, arrays, external sources,
copy-on-change, per-element appearance, nested source definitions and face-level
reference remapping are refused. This does not preserve or remap mates. Multiple
replacements, deliberate realignment, joint/datum mapping, macro recording and
physical/high-DPI acceptance remain open. Whole F022 is not complete.

The regression suite `TestOccurrenceReplace.py` compares previews with native
assembly-path geometry for both source-placement settings, tests whole Body sources,
appearance/isolation, Cancel/stale cleanup, unsupported inputs, owner transactions,
rollback, Undo/Redo and save/reopen. Move and appearance regressions are grouped
with the new tests because this workflow reuses their services.


Both tasks preceded one FreeCADGui/FreeCADGui_Resources Release build, exit 0.
Evidence: `D:\Temp\Office-PC\freecad-plus-occurrence-replace-20261001`.
Initial `grouped/` passed seven movement and seven appearance checks, plus four of
eight replacement checks. Qt findData did not match stored Python identity tuples;
replaced it with explicit key comparison. A test quantity increment also needed its
native length value. Only OccurrenceReplace.py was restaged; no second native build.
`replacement-verified/` passes all eight. **22 distinct selected passes** across
accepted suites, zero failures/errors/skips in accepted suites, native exits 0.
Initial failed aggregate remains recorded. Five reviewed `visual/` captures and
Occurrence-Replacement-Source.FCStd / Occurrence-Replacement-Result.FCStd provide
the owner fixture. Native assembly-path geometry agrees with preview for both
source-placement settings; whole Body sources, preserved appearance/placement,
other-occurrence isolation, Cancel/stale cleanup, unsupported consumers, rollback,
Undo/Redo and save/reopen pass. Later replacement edits update only its instances.
FreeCADGui SHA256: `8F48A425D59BFE4A5182B2F3CEDB920932AAFDB1104A5658B9CE2F63A529AE8A`.
validated-identities.json and acceptance-summary.json identify exact source/runtime
and accepted checks; historical About metadata is not this source identity.
No installer/release update. Whole F022/12.6 remains open for mate/interface remapping,
multiple targets, realignment, external/mixed sources, arrays, broader appearance,
macro recording and physical acceptance. Stop at this checkpoint and rotate.
