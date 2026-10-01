# Dependency inspection: owner workflow test

Select one object, then choose **Tools > Inspect dependencies...** in any workbench.
The same command is searchable through Ctrl+K. This uses this checkout's development
application at `D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Existing published installers and the separately installed FreeCAD lack this batch.

Evidence and the example are under
`D:\Temp\Office-PC\freecad-plus-dependencies-20260930`.

1. Open `visual-accepted\Dependency-Inspection.FCStd`. Select **SharedProfile** and open the
   inspector. Consumers shows **ShortExtrusion** and **TallExtrusion** as direct,
   **EdgeFillet** as transitive depth 2, and **DrawingView** as transitive depth 3.
2. Select a row to read its native type, status, dependency path and source file.
   The Native link column identifies the actual property, such as Base or Source.
   Uncheck **Include transitive dependencies** to see only immediate links.
3. Select EdgeFillet's row, then **Inspect this row**. Inputs shows its upstream
   extrusion and shared sketch. Consumers shows the drawing view. Inspection
   follows native dependencies; it does not infer relationships from tree order.
4. Select the SharedProfile row and **Select in model**. Native selection changes,
   but the hidden sketch stays hidden. Existing visible objects use native selection
   highlighting. **Inspect selected object** explicitly changes the inspection root.
5. Change an extrusion's input, rename an object or recompute. The old rows clear;
   click **Refresh** for current dependencies. Undo the edit and refresh again.
6. Inspect a feature with a broken reference. Native Invalid state and status text
   remain visible, including on upstream rows. Repair it through its existing editor
   and refresh. This inspector neither repairs nor recomputes the model.
7. Close the root document: its inspector closes. Delete a related object: rows
   invalidate. Reusing its internal name does not retarget an old selection.

The view includes native container membership and expressions, not only geometric
inputs. Each row represents a native property edge; shared nodes may appear more
than once through different properties. Direction and depth are relative to the
inspected root. Native links to other loaded documents are marked External and
include their source file; inspection does not open unloaded files.

Traversal is bounded to 500 edges and 8 levels per direction. A partial-view notice
states when a limit is reached; inspecting a row continues from that object. Cycles
in the inspected portion receive an explicit warning. Null optional links are not
guessed to be errors; unresolved or missing references use native object status.

This F015 pilot supports impact inspection, not deletion planning or repair. Dedicated
target-role classification, unloaded-reference diagnostics, integrated navigator
tabs/highlights and physical/high-DPI acceptance remain open. Stop here for owner
feedback before extending the workflow.

`TestDependencyInspector` covers native shared-sketch consumers, a real fillet and
TechDraw source, expressions, loaded external links, cycles, limits, model/visibility
preservation, selection/navigation, broken support repair, Undo/save/reopen and
deletion/close lifecycle. The grouped pass also exercises command search and temporary
display, which share the standard GUI initialization and menu.
