# Mesh from Shape — diagnosis and pending preview

**Awaiting owner approval. No production implementation or installation.**
Source: `8d7c2293f43a3bbaeb335921ec5710d208b1c378`.
Companion: `bd66e52a54b7`, UI allowlist `mesh_ui.py`.
Fingerprint: `1dd42642e4633db7431d3e6e18f12dda0482b88d3550d1985421321332b09b15`.
Inspection: current, scope valid, approval false. Never set approval for the owner.

## Reproduced failure

The installed `MeshPart_Mesher` task was opened without preselection in a
disposable Plus document. A real mouse click on a finished feature in History
successfully selected it after opening. A whole Body was subsequently selected
and the real native OK button clicked. The native task produced a valid 12-facet
`Mesh::Feature` at the document root with **no component owner**.

Validation raised `Document contains content outside component ownership`.
Parts/Assembly/History top-level counts changed from `[1, 1, 4]` to `[0, 1, 0]`;
the Assembly count includes a retained header, not proof of valid content.
This is invalid ownership and failed panel projection, not a reproduced CPU deadlock.
The task closed and Undo count increased by one.

Assigning that same mesh to the component **only in the disposable fixture** made
validation pass, restored counts to `[1, 1, 5]`, and included the mesh in History.
No owner files or running documents were opened or repaired. See `diagnose/result.json`.

`src/Mod/MeshPart/Gui/Tessellation.cpp` creates root meshes in both its regular and
Gmsh paths. `freecad_plus/document.py` requires ownership; `panel.py` rejects
invalid projection. Mesh file import already uses `document_import.insert_mesh`,
but Mesh from Shape bypasses that adapter. Accepting orphans in the validator
would conceal the defect.

## Proposed workflow and change contract

- Existing Mesh from Shape entry opens with an empty list or eligible preselection.
  A persistent collector accepts one/many solids, sheets and faces after opening.
- Solid picking selects the finished solid; Surface picking selects faces or
  sheets. Mode changes retain mixed entries and set the selection-toolbar domain.
  Do not expand all predecessor features. Keep distinct solid subshapes and exact
  occurrence placements; reject/deduplicate covered-face inputs to avoid duplicates.
- Click adds once; Shift-click removes existing inputs only. Delete, Remove, Clear
  and list activation follow the established Plus collector pattern.
- Preview assumes **one combined mesh**. The optional output-count question is
  unanswered at delivery; approval may confirm or revise it. Disconnected surfaces
  are valid inputs and are not implicitly fused.
- Preserve Standard/Mefisto/Netgen/Gmsh methods, capability availability, units and
  color/segment settings. Preserve originals/materials, coordinate visuals, other
  tasks and legacy non-Plus workflows.
- Bottom Done/Apply/Cancel replaces Leave panel open. Successful Apply commits one
  Undo, clears sources and restores fresh defaults. Failed Apply retains inputs
  and shows the shared prominent inline error. Empty Done closes; populated Done
  applies/closes. Cancel discards only unapplied work.
- Result belongs to the active component in its defining file and appears in
  History, independent of native `pdbody`. Save references/settings to reopen the
  creation task for editing. Missing/invalid sources fail safely. Reuse existing
  reference/ownership rules for imported components; do not weaken validation or
  change schema without defining compatibility.
- After approval, implement command/task routing and component-owned outputs for
  every offered method. Verify one/many solids, sheets/faces, atomic failure and
  cancellation (including asynchronous Gmsh), Undo/Redo, edit-in-place, save/reopen,
  child/imported placement, and live panel selection/visibility after completion.

## Preview evidence and limits

Screenshots: [current](baseline/current.png), [selected](candidate/selected.png),
[empty](candidate/empty.png), [invalid](candidate/invalid-source.png),
[after Apply](candidate/after-apply.png).

The prototype reuses installed native Tessellation Qt controls inside an isolated
task-like wrapper. Collector rows/actions use fixture data: **no production picking
or meshing backend**. Both renders use the same light outer background; standalone
windows otherwise inherit a dark Windows palette outside the styled native controls.
The baseline wraps native settings/standard buttons; the wrapper is not installed.

Ten widget check groups pass: empty collector, mixed rows, deduplication, Shift
removal, errors preserving inputs, Remove/Delete/Clear, Apply reset, empty Done,
Cancel, and unchanged geometry/Undo. These are UI checks, not meshing acceptance.
Methods beyond Standard have not been exercised for the proposed task.

Initial diagnostic attempts required explicit `MeshPartGui` import, corrected Qt
object discovery and a real button click (`Gui.Control.accept` does not exist).
Only the final successful run is failure reproduction evidence.
Private generated documents/profiles are removed after archiving; review worktrees
remain available. Main source, installed payload, owner profile/shortcut and
unrelated `project.previewfirst.json` remain untouched.
