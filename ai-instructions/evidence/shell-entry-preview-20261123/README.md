# Shell selection after opening: proposed UI

November 23, 2026. UI prototype only; awaiting owner approval. Installed baseline
is 068fc7d5819f7219ddb627efa0ae3f5ad687e777. No production code or install changed.

The installed command currently rejects empty selection before opening Shell;
an independent curve produces a Body-related modal. The proposal opens the task
in both cases, keeps incompatible-pick guidance inline and allows picking faces
after entry. A face can establish the target and first face to remove directly.

Direct screenshots:

- [Empty task](shell-empty.png)
- [Curve ignored, task stays open](shell-curve-ignored.png)
- [Face establishes target](shell-face-selected.png)
- [Invalid pick preserves existing face](shell-invalid-pick-keeps-faces.png)
- [Another solid's face](shell-other-solid.png)
- [Sheet guidance](shell-sheet-guidance.png)
- Baseline: [empty selection](baseline-empty.png), [curve](baseline-curve.png),
  [existing native task](baseline-shell-task.png).

Native FreeCAD QWidget rendering uses the existing TaskThicknessParameters.ui,
the installed shared status widget, isolated profiles and synthetic documents.
The candidate adds only simulated target/face collection and guidance. OK is
disabled; no shell kernel, persistence, production selection observer or edit
integration is implemented. The preview check flags verify simulated state changes,
not real feature acceptance. See candidate-result.json and baseline-result.json.

Implementation scope after approval: valid preselection initializes target/faces;
empty, ambiguous or incompatible geometry leaves the task open. Pick a solid then
faces, or a face directly. Explicit target change clears old faces; wrong-solid
and incompatible picks preserve valid inputs. No arbitrary or active Body target.
Preserve native thickness/mode/join/intersection/direction options and native
PartDesign::Thickness identity. Validate faces, positive thickness and native result
before acceptance. Shared create/edit, History navigation/restoration, tree eyes,
selected-target display, numeric blur/immediate arrows and prominent errors apply.
Atomic acceptance, clean Cancel, Undo/Redo, reopen and failed-entry cleanup must
be checked. Ordinary legacy documents retain native behavior.

Companion session a5461c3ce973, adapter baseline
495c56b220fd461f6ce5d71b3b72a0821d8224dc, candidate allowlist shell_ui.py.
Captured fingerprint 1fcd142dec6472503ec6a80a15af88bb3c69693227705c5528fa8277d8a16da0.
Capture is valid and in scope; approval state remains untouched. Archived renderer
expects its original adapter location and the installed runtime paths.
