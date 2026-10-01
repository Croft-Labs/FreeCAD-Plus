# Saved exploded-view output (F080)

Use the source-built FreeCAD Plus fork, Assembly workbench. The existing native
exploded-view command and saved Move objects are retained. This checkpoint covers
solid occurrences, successive translation/rotation/radial steps, transformed
structural parents and explicit TechDraw consumption. It is ready for owner
workflow testing; it is not full F080 acceptance.

1. Create an assembly containing two linked solid parts. A definition with its own
   translation/rotation is useful. Try both settings of the link's LinkTransform.
2. Activate the assembly and choose **Exploded View**. Move one occurrence away,
   then add another movement of that same occurrence in a different direction.
   The second trail should start at the preceding step's endpoint. Try rotation
   and radial movement as separate variations.
3. Accept the task. The model returns to its assembled placements; the exploded
   view keeps its separate steps. Double-click that saved view to inspect/edit it.
   Cancel an edited step: the previous step values and assembled placements return.
4. Create a TechDraw page, select the saved exploded-view object, and insert a
   view. Check the occurrence geometry and trails against the native task preview.
   The drawing's Source must be the saved exploded view, not the normal assembly.
5. Undo/Redo a step change, save the document, and reopen. Verify the assembled
   model and the reopened exploded task/drawing. Try a translated/rotated assembly
   in an App Part. Check that source definitions and the other occurrence did not
   move. Missing move references should report an error, not produce a partial
   drawing silently.

Evidence and fixture: `D:\Temp\Office-PC\freecad-plus-exploded-output-20261001`;
`visual-accepted/Exploded-Arrangement.FCStd` contains two saved steps and a drawing using the
saved view explicitly. The roadmap 12.7a/b entry owns accepted build/staging,
regression and visual evidence. Run `TestExplodedViewOutput` with `tests` on
`sys.path` and `AssemblyTests.TestCommandCreateView` in the source-built GUI.

This batch does not change document/property identities or add an arrangement
engine. Existing visibility filters still determine drawn parts. Mixed parent and
child moves inside subassemblies, external/unloaded links, arrays, scaled links,
complex visibility, flexible/joint-driven motion, BOM arrangement choice and
physical owner acceptance remain unverified. Visual motion is not a dynamics
simulation. No installer or release was produced. Rotate to another family after
this checkpoint; refine this workflow from owner feedback or a demonstrated blocker.
