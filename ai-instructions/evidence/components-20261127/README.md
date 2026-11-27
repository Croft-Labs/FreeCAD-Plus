# Approved Components panel implementation — November 27, 2026

Owner authorized all previewed Components changes in chat. Direct screenshots
are the approval artifacts; companion approval state is not edited.

## Navigation and saved assembly

Review `30a2bb731e86`, fingerprint
`ab8728c6fbd9edac71464463805ba562a111f8030ee5ff28cf06eba2a66c955d`.
Native source validation: 13/13 navigation and existing active-assembly checks pass.
Checks cover retained tab/expansion, normal/native Save, Save As, saved occurrence,
reopening against conflicting preferences and unsaved later choices, stale identity,
per-view choice and preserved geometry/object identity/Undo. Metadata is host-owned
`Document.Meta[FreeCADPlus.ActiveAssembly]`, version 1; no schema or geometry edges.
Installation and integrated validation follow with the other approved groups.

## Assembly controls and full group menus

Review `ae8dafb11414`, fingerprint
`5a69bfb4d52c9bd1fe05376e4a91cdf41492ddc1e9e36fc7e140440791ec7658`.
Native source checks pass 10/10 after correcting per-view grouping on immediate
file switches and submenu QAction lifetime. No hidden dropdown remains. Inline
root controls, per-parent grouping, menu parity, exact occurrence selection,
Copy/Move group targeting, atomic grouped display/Undo, rename and singleton/Undo
transitions pass. Remove instance and pattern editing explicitly select a member
before opening their existing review/editor; they never silently choose one.
Shared-definition Edit/Rename/Open and Paste retain the existing definition semantics.

## Parts file workflows and recovery

Review `e2cefeaaa3b9`, fingerprint
`01658d784c8d20b8c2738350e2b8b1ec29b817d36bbfc5768832824906d91596`.
Create default linked part files, sub-file views, independent dependency copies,
baked geometry, native Locate pickers, cancellable folder search and pre-open
recovery are implemented. Native deep copy retains editable history and shared
dependencies; successful copies are checked for outside references. Baking preserves
geometry placement and materials, including meshes. Source files remain unchanged.
Names receive unique numeric suffixes when the imported originals already reserve them.

Missing-file recovery preflights the complete remapped graph before native restore.
Private temporary archives change only native XLink file paths, preserving native
UUIDs, object IDs and geometry streams; originals remain untouched until normal Save.
Loaded relocation refreshes FreeCAD's cached XLink paths while retaining targets.
Cancel closes the search worker cooperatively and never chooses a candidate implicitly.

Integrated source suite: 102/102 pass (navigation, assembly, file operations,
external definitions, native file workflows, imports, exports and appearance).
Final focused source/fresh-profile checks: 7/7 pass, including independent associative
copy reopening, separately loaded saved active assemblies, and long-path search UI.
## Installed delivery

Seventeen Python payload/test files installed with SHA-256 verification and rollback
copies under the existing build's `validation/components27/rollback`. Owner-profile
CFG files and desktop shortcut hashes remain unchanged. The shortcut still targets
`Launch FreeCAD Plus.bat` in the same build root, which launches `app/bin/FreeCAD.exe`
with the existing owner-test profile. No native rebuild was required; restart needed.

Installed run: 37 actual cases pass, plus one test-loader error caused by an incorrect
Save All test name in the invocation. The corrected existing native Save All case
passes separately: 38 installed cases verified in total. Logs retain the original
invocation error rather than hiding it. Fresh-process copy reopening verifies native
UUIDs/object IDs and a self-contained archive. Direct installed menu/task screenshots,
validation scripts and the installation manifest are archived here.

Navigation and Assembly implementations were pushed as `7499fc010e` and `8f1fbab4ac`.
The final Parts implementation and delivery evidence are committed separately.
