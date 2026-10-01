# Make occurrence unique: owner workflow test

Use this checkout's development executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Evidence: `D:\Temp\Office-PC\freecad-plus-unique-occurrence-20261001`.
Existing installers do not contain this batch.

1. Open `visual\Shared-Spacers.FCStd`. First and Second are native Link occurrences
   of Spacer, an independent two-circle sketch and solid Part extrusion. The source
   and enclosing assembly both have nontrivial placements.
2. Select First itself in the tree and choose **Tools > Make occurrence unique**.
   Review the occurrence, shared definition, destination document and copied inputs.
   The new label is editable. No objects are created during review or Cancel.
3. Click **Make Unique**. Only First points to the new Part definition. Its world
   position, LinkPlacement and visibility remain unchanged; Second keeps Spacer.
   The copied extrusion references the copied sketch, not the original sketch.
4. Edit the copied sketch's second radius constraint from 2 to 3 mm and recompute.
   The unique spacer volume becomes 48*pi mm3; the original stays 63*pi mm3.
   The ready-made `visual\Independent-Spacers.FCStd` shows this difference.
5. In a separate pass from Shared-Spacers, repeat steps 2-3 and immediately Undo/Redo:
   the copy disappears and First rejoins Spacer, then returns to its unique definition.
   Save/reopen and edit
   the original Profile: only original occurrences follow that edit.
6. Start another review, then change the source. Make Unique disables until you
   recompute and Review again. Pending document edits and active tasks must finish
   before committing. Unsupported input or a failed copy leaves no partial definition.

Scope: one direct unscaled Link to a same-document native App::Part containing exactly
one independent Sketcher sketch and its native Part::Extrusion solid. The command
copies into the same document at its root, preserving the source Part placement.
No external/attached inputs, expressions, arrays, prototype SemanticIdentity fields,
or non-Part consumers of the occurrence are accepted. No references are detached
or guessed. New native names/IDs belong to the independent copy; existing source
objects and other occurrence identities are unchanged. No new persistence schema.

Native copy retains sketch constraints and extrusion history. This is not a generic
copy of arbitrary Body histories or subassemblies, and it does not remap mates, drawing
references or other occurrence consumers. Source editing remains available through
normal native tools; the copied definition stays hidden when the original was hidden.
Whole F019 remains open for broader definitions, external destinations, provenance,
relationship remapping and physical/high-DPI acceptance. Stop here for feedback.
