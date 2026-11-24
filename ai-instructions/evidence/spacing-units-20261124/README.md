# Spacing chains and quantity presentation

Owner approved the [direct UI previews](../spacing-units-preview-20261124/README.md)
in chat: “Approved. Implement”. Source baseline was `882a1ace52`.

## Implementation

Sketch Pattern creates construction-line chains for linear/radial spacing and
construction arcs for angular spacing. Consecutive endpoints are coincident.
Line chains share Equal/Parallel relationships with one length driver per independent
pitch; selected lines/axes and two-point/radial references remain associative.
Independent forward/backward extents have separate masters; symmetric extents share
one. Angular chains use one angular master and native expressions for matching spans
at different radii: equal radii alone would not constrain arc angles. Expression-driven
follower labels are hidden. The existing nonsingular relative-rotation construction
handles an anchor exactly at the center without fixing the source geometry.

Create spacing constraints defaults on. Hide spacing chain defaults off for new
sketches and reflects saved helper visibility on reopening the task. It operates on
stable helper identities stored in an optional hidden `PatternSpacingTags` property
and a named `Part::GeometryStringExtension` on each helper. Native runtime geometry
tags change across processes, so they are not used as the persistent identity.
Helpers use the native **visual** geometry extension/layer, not the unrelated semantic
GeometryLayerId. Hiding leaves their solver equations, construction status and driving
dimensions active, and hides their nondimensional relationship markers. Ordinary
profile geometry and its own constraints remain visible. Changes participate in Undo.

Shared native InputField/QuantitySpinBox editors and Plus dimensional task controls
retain six-decimal entry independently of display rounding. Native property commits
use full double precision. Older/more precise values are not truncated when opening
an editor. Compatible suffixes and arithmetic use the native unit/expression parser;
bare numbers use the current presentation unit. Integer counts remain integers.
The native DoubleSpinBox default and the shared numeric event filter also enable
six-place entry in ordinary floating-point task controls.

General preferences add Secondary unit system and Display decimals, defaulting to
Imperial decimal / 3 when absent. Existing primary settings are preserved. Explicit
units matching the secondary schema use secondary precision; primary/shared units
use primary precision. Unit selection and physical numeric values are separate.

Sketch constraints own an optional `PresentationUnit` XML attribute, included in
native clone/copy/Undo and exposed to Python with dimensional validation. Their
leaders, constraint list and datum dialog honor it. Legacy files without the attribute
continue using document units. Bound native feature inputs and Plus feature tasks use
an optional hidden `App::PropertyMap` named `QuantityPresentationUnits`, keyed by
property path. Plus creation/edit acceptance writes this map in the feature's existing
transaction; Cancel does not change it. Property identities and numeric schemas stay
unchanged. Existing files are not rewritten until edited/saved.

Main sources: `sketch_pattern.py`, `sketch_pattern_task.py`, shared
`quantity_fields.py`, native `Gui/QuantityPresentation.h`, `InputField.cpp`,
`QuantitySpinBox.cpp`, General preferences, and Sketcher constraint persistence,
datum editor and label rendering. Extrude/Revolve/Thicken, Shell and plane tasks
share the quantity/persistence service.

## Validation and delivery

- Native build succeeded; all 88 C++ Sketcher regression tests passed.
- Rebuilt-app acceptance: 130 tests passed, covering new unit/chain cases plus
  pattern geometry/UI, source freedoms, downstream solids, Extrude/Revolve/Thicken,
  Shell, plane placement/history and one-Enter dimensional editing.
- Further native display checks verified the actual visible/hidden curves, restored
  checkbox state, native property binding, and exact values versus rounded leaders.
- Three legacy plane-selection tests fail in the unchanged installed baseline because
  they expect click-to-toggle removal, superseded by the owner's click-add/Shift-remove
  workflow. They were not treated as regressions or changed in this task. The real-pick
  and deferred-value tests pass in the rebuilt app.
- The initial source-overlay run mixed cached installed shared modules with new source;
  authoritative acceptance uses a fresh process with rebuilt/installed modules.
- A fresh-process check caught regenerated runtime geometry tags. The final code uses
  persistent geometry extensions, and the regression asserts nonempty helper matching.
  Raw-text input restoration also avoids the old display-rounding conversion.

Final delivery build and installation succeeded. All 144 installed application tests
passed, including the 12 symmetry regressions; all 88 native C++ tests passed. A fresh
process reopened four saved documents (explicit sketch units, hidden linear chains,
hidden angular/radial chains and feature units). The existing desktop shortcut passed
both native pattern and shared-editor checks. All 18 installed file hashes match the
delivery manifest; original files are backed up for rollback. Restart FreeCAD Plus to
load the updated native modules. No release or EAS/Expo build was created.
Unrelated `project.previewfirst.json` remains untouched.

The existing `freecad plus 0.1.0.lnk` still targets
`C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/Launch FreeCAD Plus.bat`,
which launches `app/bin/FreeCAD.exe` with the existing owner profile. Validation used
explicit isolated profiles and did not alter that shortcut.

### Actual native screenshots

- [General unit preferences](native-general-units.png)
- [Rounded dimension leaders](native-unit-leaders.png) and [full-precision editor](native-unit-edit.png)
- [Pattern controls](native-pattern-panel.png)
- [Angular/radial chains visible](native-circular-chains.png) and [hidden](native-circular-hidden.png)

Logs/results are in `native`, `installed`, `fresh-reopen` and `shortcut`.
`install-manifest.json` records installed hashes and rollback paths. `harness` contains
the bounded build, installation and verification scripts used for this delivery.
