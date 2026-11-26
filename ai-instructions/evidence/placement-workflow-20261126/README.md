# Placement display and active-component additions — November 26, 2026

Implemented and installed after the owner's “all approved. implement” instruction.
The [approved placement screenshots](approved-placement.png) supersede the earlier
edge-only proposal. The [approved workflow screenshots](approved-workflow.png)
cover the Parts action and outside-assembly prompt. Companion captures were fresh
and scoped; chat approval was used without editing tool approval state.

## Behavior

- Assembly Add existing/Add new target the active edited component, independently
  of selected source rows. Top-level and nested destinations are supported.
- Parts > Add to active component… opens Create instances with the selected parts;
  multiple sources share one defining-file transaction.
- If the destination is outside the active assembly's definition tree, the native
  prompt offers Make active assembly and add or Cancel. Cancel is the default.
  Confirmation rechecks Edit/file/view/assembly context before switching assembly.
- Placement preview copies native view-provider geometry and colors, follows the
  seven draw-style actions, and gives faces at least 50% transparency. Sources
  already more transparent retain that value. Geometry is unpickable, temporary,
  and removed on Cancel. Native internal placement transforms are retained.
- Existing linked ownership, source-file requirements, cycle guards, geometry,
  component identities, pattern editing, Undo/Redo and serialization are preserved.

Hidden line's native renderer still exposes triangulation edges. This was reproduced
on ordinary geometry with the placement preview off and disclosed before approval;
this change does not claim to repair that renderer. Style following is verified for
the native UI actions; arbitrary Python scripts that directly change viewer override
state without triggering actions were not part of this UI acceptance.

## Verification

- Initial source focused acceptance: 8/8 passed.
- Expanded source run: 65/66 passed; the export test with the longest output path
  failed at native save. The same test passed with the shortened validation path;
  no product export change was made. Both runs are retained.
- Final installed regression: **66/66 passed** across placement workflow, instance
  quantity/patterns, Add Component, active assembly and part transfer.
- Existing desktop shortcut: **10/10 passed**, with owner profile CFG hashes unchanged.
- Fresh installed-process reopening: saved pattern proxies, member identities,
  external links, populated edit task, Undo/Redo, editable exports and referenced
  direction recomputation passed.
- Native preview bounds match the committed link under translated/rotated source
  and parent frames. All seven style clicks refresh; source properties, greater
  transparency, preview toggle and Cancel preservation are covered.
- [Installed native style screenshots](installed-styles/FlatLines.png), test logs,
  bounded helper scripts and five installed SHA-256 hashes are retained here.

Tests use disposable profiles and synthetic documents. The running owner's app and
unsaved assembly were not closed or edited. Validation outputs were archived before
removing task-generated profiles and CAD fixtures. No native rebuild was required.

## Delivery

Five Python files were installed with matching source hashes and rollback copies
for previously existing files. Existing shortcut target and working directory remain
`C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/Launch FreeCAD Plus.bat`
and its parent directory. The shortcut icon remains `app/bin/FreeCADPlus.ico,0`.
Restart FreeCAD Plus to load the updated modules. No release/package was published.
The existing untracked `project.previewfirst.json` was preserved outside this commit.
