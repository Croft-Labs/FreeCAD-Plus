# Simplified mesh settings — preview pending November 27, 2026

Superseded by the [mixed selection/defaults revision](../mesh-defaults-20261127/README.md).

Owner requests a Standard-by-default Mesh from Shape task with only linear and
angular deviation visible. Move other algorithms and extra settings behind an
Advanced settings button opening a pop-up. This is the requested direction;
approval of the concrete rendered workflow remains pending. No production code,
installed application, owner profile or documents were changed.

## Direct native Qt screenshots

- [Current installed form](before.png)
- [Proposed main form](main.png)
- [Advanced settings — Standard](advanced-standard.png)
- [Advanced settings — another generator](advanced-other.png)
- [Main form after an advanced generator is selected](advanced-active.png)
- [After simulated Apply/reset](reset.png)

## Contract

Keep source selection and its solid/surface modes, one combined owned mesh result,
status and bottom Done/Apply/Cancel. Main settings contain only Linear deviation,
Angular deviation and Advanced settings. Use Standard and absolute deviation for
fresh tasks; put relative deviation, colors/segments and alternate algorithms in
the modal Advanced dialog. Preserve native engine availability and user units.

Advanced OK retains draft changes; Cancel/Escape restores all prior values and
generator. Switching back to Standard synchronizes the deviation values. Disable
the main deviation fields when the chosen advanced algorithm does not use them,
with a tooltip directing the user to Advanced settings. Do not add algorithm names
or technical summaries to the main form. Apply resets to Standard and clears inputs.
Editing an existing mesh must retain its saved advanced recipe until changed.

## Provenance and checks

Production baseline: `34eb5c576d6fa61a471cab0cd80bb51ae5db083e`.
Unrelated untracked `project.previewfirst.json` remains untouched. A clean isolated
snapshot of installed mesh_ui.py (import-only adaptation) is the review baseline:
`a8809cee42026a8cfa9dfeb04e9b43605e5d3e69`.
Companion session `9cf58b893465`, exact allowlist `mesh_ui.py`.
Fingerprint `2b1acb4746c1776f5cdf07e41bfbc01e5276408b9c009533a59c9a202cc4ff55`.
Inspection: preview current, no scope violations, not approved. Approval state was
not changed on the owner's behalf.

Six UI checks passed: hidden algorithms on main; Advanced Cancel restoration;
acceptance and disabled inapplicable fields; return-to-Standard synchronization;
simulated Apply reset; unchanged document/object/Undo state. These are real Qt
widgets in an isolated FreeCAD process, with mock source rows and simulated Apply.
No new meshing backend behavior is implemented or validated by this preview.

Implementation must use native quantity controls/units and synchronize via
QuantitySpinBox.rawValue for numeric updates (setting its typed value property to
a bare float silently fails). Verify nondefault settings through save/edit/reopen,
advanced Cancel, successful/failed meshing, Apply reset, and existing advanced recipes.
Preserve the documented Netgen baseline limitation; no engine repair is implied.
