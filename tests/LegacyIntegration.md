# Grouped legacy migration integration and owner delivery

Task twelve qualifies a bounded whole-file corpus on the installed owner payload,
without application source overlays. It does not promise conversion of every
possible legacy workbench object or physical flattening of retained native histories.

## Corpus and invariants

`TestLegacyIntegration` combines independent Sketch/Pad mapping with native
Fillet/Linear Pattern retention in one nested assembly, repeated instances with both
LinkTransform modes and a parent-owned sibling. Original native object identities,
UUIDs, geometry, placements, ownership, formulas and FCStd bytes must survive
conversion, Undo/Redo and cadprt save/reopen. Shared definition edits update all
instances; sibling placements remain independent.

External mixed definitions use two shared occurrences. Native FreeCAD requires the
owning legacy document to be saved before binding an external link. Conversion must
refuse parent save before external cadprt save. Save children before parents;
relocate both files together and prove full source restoration and shared updates.
Original child and parent FCStd files remain protected.

Legacy Draft clones and CAM Job model clones must consume the original migrated
Body after conversion, edits, Undo/Redo and restore. A pre-existing TechDraw view
keeps its original Body reference and refreshes its projected circle after a sketch
dimension edit. These tests do not qualify generated toolpaths, drawing dimensions
through arbitrary topology changes, or finite-element solver output.

Expression-driven structural recovery retains native hierarchy/history and exposes
explicitly reported evaluated dumb output. Validate geometry before and after
cadprt restore. No unavailable shape or stale cache becomes fabricated success.
The existing structure suite covers missing definitions/save refusal, arrays,
scaled/shared placements, internal Body links and source protection.

## Native GUI, cold processes and delivery

Exercise actual standard Open and History double-clicks, native editor rejection,
native radius Accept/Cancel/Undo, and shared modeling previews. Record every loaded
application module's payload path and source hash; test files may load from this
checkout. `TestLegacyIntegrationCold` restores the previously generated mixed,
relocated external and recovery documents in another process. Startup checks inspect
native file actions, recent-files view and default Tasks docking.

Compatible Python-only changes reuse the verified native binaries. The portable
`tools/FreeCADPlusLauncher.cs` forwards quoted arguments and native exit status,
uses the payload's own bin/FreeCAD.exe and retains the fork icon. Compile with the
Windows Framework compiler into the designated test-builds payload. The grouped
manifest separates application source identity, compiled native identity, launcher
source/hash and installed module hashes. Verify the complete file inventory.

Retarget the existing desktop shortcut with `UpdateOwnerBuildShortcut.ps1`, reopen
it and verify target/working directory. Launch the actual saved link with isolated
test arguments, restore its original arguments, then reopen/verify the final owner
link. Preserve useful rollback builds until the new link launches successfully.

## Boundaries and evidence

Native FEM is disabled in the existing build configuration. Track native FEM
constraint/mesh/solver acceptance as an explicit separate unavailable gate; do not
substitute fake FEM objects or skipped tests. Custom Path/Point variants, exhaustive
mixed-family permutations and physical owner feedback remain wider qualification
work. WORK_STATE and the canonical roadmap own actual execution counts, failed
attempts, hashes, warnings, DOCX visual inspection, shortcut verification, cleanup
and GitHub publication. UI/UX requirements alone remain in the owner DOCX.
