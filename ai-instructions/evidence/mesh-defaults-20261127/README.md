# Mixed mesh selection and mesher defaults — revised preview

**Delivered:** The owner subsequently approved the revised mesh proposal. See
[installed implementation and checks](../mesh-settings-delivery-20261127/README.md).
The original preview record below is historical.

November 27, 2026. Supersedes [the initial simple-panel proposal](../mesh-simple-20261127/README.md).
Owner requested removal of Pick/Solid/Surface controls, radio-button mesher selection
in Advanced, defaults there, and main-panel settings appropriate to the selected model.
Concrete revised preview approval is pending. Production code and installed app are unchanged.

## Direct native Qt screenshots

- [Current installed form](before.png)
- [Main form, Standard](main.png)
- [Advanced radio buttons and defaults, Standard](advanced-standard.png)
- [Advanced radio buttons and defaults, Netgen](advanced-netgen.png)
- Main settings: [Mefisto](main-mefisto.png), [Netgen](main-netgen.png), [Gmsh](main-gmsh.png)

## Revised contract

One mixed source list accepts selected solids, sheets and faces without a picker
filter. Preserve exact selected geometry, current ownership/history eligibility,
click/Shift/Delete/Remove/Clear, and one combined mesh result. Do not promote a
selected face to its entire solid; avoid duplicate coverage when a whole source
and its face are collected. Source validation remains active without UI type modes.

Standard is the initial default, showing only linear and angular deviation as its
main numerical settings. Mefisto replaces those with its edge-length controls;
Netgen shows fineness and applicable custom controls/options; Gmsh shows meshing
method and min/max element size. Extra Standard relative/color/segment options and
the Gmsh executable setting remain in Advanced. Preserve units and engine availability.

Advanced uses radio buttons for Standard/Mefisto/Netgen/Gmsh, with the selected
model's default settings below. Proposed OK semantics: apply the selected model
and values to this mesh and save defaults for future new meshes. Main-panel edits
change only the current mesh. Cancel/Escape changes neither the current recipe nor
defaults. Successful Apply clears sources and restores saved defaults; without a
user override those defaults are Standard. Editing existing meshes preserves their
saved recipe rather than replacing it with current defaults. Failed Apply retains
current inputs. Existing Undo/geometry/recompute/appearance behavior stays unchanged.

## Preview evidence

Source checkpoint `642599f4a090c36f6d32064937d4579e7e7917c6`; installed UI unchanged
from `34eb5c576d6fa61a471cab0cd80bb51ae5db083e`. Clean import-adapted UI snapshot
`a8809cee42026a8cfa9dfeb04e9b43605e5d3e69`. Unrelated project.previewfirst.json untouched.
Companion `d4c51081992f`, allowlist only `mesh_ui.py`, fingerprint
`9d8ab7aba64810496bc49188588e2c0cbf9e35a94dd5ae3d3e9aab7e175bd003`.
Inspection is fresh, has no scope violations, and is not approved. No approval
state was changed on the owner's behalf.

Seven UI checks passed: no picker filter/Standard initial fields; radio selection
and Cancel restoration; dynamic fields for Mefisto, Netgen and Gmsh; current-only
main edits with saved-default Apply/reset; unchanged document/object/Undo state.
The prototype uses native FreeCAD Qt widgets with mock source rows, in-memory
defaults and simulated Apply. It does not implement persistence or meshing changes.
Native quantity widgets require rawValue for numeric synchronization. Functional
implementation must test nondefault persisted recipes, defaults vs current overrides,
mixed exact selections/duplicate coverage, Cancel, failures and Apply/reset.
The prior native Netgen failure remains a separately documented limitation.
