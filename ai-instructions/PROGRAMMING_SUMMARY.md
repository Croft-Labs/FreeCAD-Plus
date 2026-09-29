# FreeCAD Plus: Programming Summary

## Project at a glance

FreeCAD Plus is Croft-Labs' FreeCAD fork, a desktop parametric CAD application
using C++, Python, Qt, OpenCASCADE, and Coin; the GUI executable enters through
[`src/Main/MainGui.cpp`](../src/Main/MainGui.cpp).

## Where to go

| Task or question | Start here | Related reference |
| --- | --- | --- |
| Product intent and boundaries | [Product specification](PRODUCT_SPEC.md) | [UI scope](UI_UX_SPEC.md#interface-scope) |
| Pad creation without preselection | [`Command.cpp`](../src/Mod/PartDesign/Gui/Command.cpp), `CmdPartDesignPad::activated` and `prepareProfileBased` | [Pad UI](UI_UX_SPEC.md#ui-001-pad-task-pane) |
| Unified Extrude command and Add/Subtract | [`Command.cpp`](../src/Mod/PartDesign/Gui/Command.cpp), `CmdPartDesignExtrude`; [`TaskPadParameters.cpp`](../src/Mod/PartDesign/Gui/TaskPadParameters.cpp), shared by Pad/Pocket | [Extrude UI](UI_UX_SPEC.md#ui-001-pad-task-pane) |
| Combined Linear/Circular Pattern | [`FeaturePattern.cpp`](../src/Mod/PartDesign/App/FeaturePattern.cpp), [`TaskMultiTransformParameters.cpp`](../src/Mod/PartDesign/Gui/TaskMultiTransformParameters.cpp), `CmdPartDesignPattern` | [Pattern UI](UI_UX_SPEC.md#ui-002-pattern-task-pane), [tests](../tests/PatternTaskPanel.md) |
| Operation persistence and geometry | [`FeatureExtrude.cpp`](../src/Mod/PartDesign/App/FeatureExtrude.cpp), `setupExtrusionOperations`, `computeDirection`, `buildExtrusion` | [Regressions](../src/Mod/PartDesign/PartDesignTests/TestExtrude.py) |
| Extrude profile list and selection | [`TaskPadParameters.cpp`](../src/Mod/PartDesign/Gui/TaskPadParameters.cpp), `TaskPadParameters`, `ExtrudeProfileSelection` | [Extrude UI](UI_UX_SPEC.md#ui-001-pad-task-pane) |
| Reopen an existing Pad | [`ViewProviderPad.cpp`](../src/Mod/PartDesign/Gui/ViewProviderPad.cpp), `getEditDialog` | [Requirements](PRODUCT_SPEC.md#capabilities-and-requirements) |
| Build or verify changes | [Development guide](DEVELOPMENT_GUIDE.md#commands) | [Pad test procedure](../tests/PadTaskPanel.md) |
| Priorities, completion, and blockers | [Roadmap](DEVELOPMENT_ROADMAP.md) | [Current focus](DEVELOPMENT_ROADMAP.md#current-focus) |
| Agent instructions | [Root entry point](../AGENTS.md) | [Shared standard](../../ai-instructions/AGENTS_TEMPLATE.md) |

## Folder and module map

All code paths are relative to the project root.

| Path | Responsibility | Key entry point |
| --- | --- | --- |
| `src/Main/` | GUI and command-line launch | `MainGui.cpp`, `MainCmd.cpp` |
| `src/App/` | Documents, properties, transactions, persistence | [`Document.cpp`](../src/App/Document.cpp) |
| `src/Gui/` | Application shell, selection, task view | [`Control.cpp`](../src/Gui/Control.cpp) |
| `src/Mod/PartDesign/App/` | Parametric feature models and geometry | [`FeaturePad.cpp`](../src/Mod/PartDesign/App/FeaturePad.cpp) |
| `src/Mod/PartDesign/Gui/` | Commands, view providers, task panels | `Command.cpp`, `TaskPadParameters.cpp` |
| `src/Mod/PartDesign/PartDesignTests/` | Python application and GUI regressions | [`TestPadTaskPanel.py`](../src/Mod/PartDesign/PartDesignTests/TestPadTaskPanel.py) |
| `tests/src/Mod/PartDesign/App/` | C++ feature tests | [`Pad.cpp`](../tests/src/Mod/PartDesign/App/Pad.cpp) |
| `cMake/`, `.github/workflows/` | Build configuration and upstream CI recipes | [`CMakeLists.txt`](../CMakeLists.txt) |
| `ai-instructions/` | Fork requirements, development guidance, and planning | This index |

## Common code and libraries

| Capability | Canonical implementation | Reuse guidance |
| --- | --- | --- |
| Pad/Pocket parameter controls | [`TaskExtrudeParameters`](../src/Mod/PartDesign/Gui/TaskExtrudeParameters.cpp), [`TaskPadPocketParameters.ui`](../src/Mod/PartDesign/Gui/TaskPadPocketParameters.ui) | Preserve Pocket behavior when changing the common base. |
| Sketch-based selection and visibility | [`TaskSketchBasedParameters`](../src/Mod/PartDesign/Gui/TaskSketchBasedParameters.cpp) | Coordinate selector lifetimes and visibility restoration. |
| Pattern parameters and transformations | [`TaskPatternParameters`](../src/Mod/PartDesign/Gui/TaskPatternParameters.cpp), [`MultiTransform`](../src/Mod/PartDesign/App/FeatureMultiTransform.cpp) | Reuse the Linear/Polar engines and parameter widgets; keep result identity separate from retained mode settings. |
| Task acceptance, rejection, and transactions | [`TaskFeatureParameters`](../src/Mod/PartDesign/Gui/TaskFeatureParameters.cpp) | Reuse existing recompute and undo/cancel handling. |
| Geometry reference checks | [`ReferenceSelection`](../src/Mod/PartDesign/Gui/ReferenceSelection.cpp) | Preserve document/body and dependency restrictions. |
| Profile and extrusion model | [`FeatureSketchBased.cpp`](../src/Mod/PartDesign/App/FeatureSketchBased.cpp), [`FeatureExtrude.cpp`](../src/Mod/PartDesign/App/FeatureExtrude.cpp) | UI changes must respect model constraints. |
| Dependency and submodule ownership | [`pixi.toml`](../pixi.toml), [`pixi.lock`](../pixi.lock), [`.gitmodules`](../.gitmodules) | Use declared dependencies; do not copy or edit vendor code for a UI task. |

## Data and contracts

| Area | Authoritative source | Related explanation |
| --- | --- | --- |
| Pad profile and dimensions | [`FeatureSketchBased.h`](../src/Mod/PartDesign/App/FeatureSketchBased.h), [`FeaturePad.h`](../src/Mod/PartDesign/App/FeaturePad.h), [`FeatureExtrude.h`](../src/Mod/PartDesign/App/FeatureExtrude.h) | Profile is one object with optional subelement references. |
| Document links and transactions | [`PropertyLinks.h`](../src/App/PropertyLinks.h), [`Document.cpp`](../src/App/Document.cpp) | Preserve persisted identities and undo semantics. |
| Build/version configuration | [`version.json`](../version.json), [`CMakeLists.txt`](../CMakeLists.txt) | Manifest versions are authoritative. |

No new app-to-app or cloud contract is part of the current fork scope.

## Critical conventions and boundaries

- The source checkout and separately installed FreeCAD are distinct; follow the
  [development guide](DEVELOPMENT_GUIDE.md#prerequisites-and-setup).
- Preserve existing preselection workflows while adding task-pane selection.
- Keep shared helpers reusable without applying Pad behavior to other operations
  before their requirements and validation are defined.

## Additional references

- [Upstream human-facing overview](../README.md)
- [Contribution guidance](../CONTRIBUTING.md), [AI policy](../AI_POLICY.md), [license](../LICENSE)
- [Pad regression procedure](../tests/PadTaskPanel.md)
