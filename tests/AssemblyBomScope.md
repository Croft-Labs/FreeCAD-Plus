# Assembly BOM inclusion owner check (F104)

Use this fork's source-built application with the Assembly workbench enabled. Open
the existing **Assembly > Bill of Materials** command for the active assembly, or
double-click its saved BOM. The document-wide command remains available when no
assembly is active. A BOM stored in an assembly's Bills of Materials group now
uses that assembly's scope.

1. Make an assembly with two links to a module definition, one bolt inside that
   module, three additional links to the same bolt, and one unique bolt definition.
   Include an unrelated assembly in the document. With **Parts children** enabled,
   the module row should have quantity 2, its child bolt quantity 1, the direct bolt
   row quantity 3 and the unique bolt quantity 1. The unrelated assembly is absent.
   Quantities are **per parent**, not flattened totals: the module contributes two
   bolts overall. A later sibling must never increase an earlier nested child row.
2. Hide one direct bolt or a module in the tree and refresh the BOM by opening its
   editor. Counts should remain unchanged. Visibility is not an inclusion rule.
3. Select a whole occurrence in the tree and choose **Exclude tree selection** in
   **Excluded from this BOM**. The list identifies the omitted object by label and
   internal name. The source stays visible or hidden exactly as before; only this
   BOM changes. A different BOM keeps its own inclusion policy.
4. Select a row in the exclusion list and choose **Include again**. Cancel restores
   the previous exclusion list and counts. Accept saves the list in the existing
   native BOM object; Undo/Redo should restore the corresponding policy.
5. Save/reopen, inspect the exclusions and export through the existing spreadsheet
   export. The exported rows should match the scoped counts. Excluding a child
   occurrence stored inside a reused module definition affects every use of that
   child; it is not an override for just one path through a repeated subassembly.

This is a per-BOM exclusion policy, not a new global component role or suppression
system. Item numbers regenerate after structure/inclusion changes. The bounded
checks cover ordinary native links, unique definitions and uniformly mirrored
links. Arrays, suppression/configurations, per-occurrence subassembly overrides,
external/unloaded inputs, custom-column identity preservation, persistent balloon
numbering and exploded documentation remain open under F104. A BOM is refreshed
by its existing recompute/editor workflow; no new automatic assembly change tracker
is claimed. Physical owner acceptance remains pending.

Automated coverage: `TestAssemblyBomScope`, grouped with `AssemblyTests.TestCore`.
Fixtures exercise grouped scope, per-parent quantities, hidden components,
independent BOM policies, include/exclude, cancel, transactions, Undo/Redo,
save/reopen and native CSV export. Exact results are under roadmap 15.4a/b.
