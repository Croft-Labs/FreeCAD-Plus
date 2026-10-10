# FreeCAD Plus: Programming Summary

## Current baseline

This is the clean official **FreeCAD 1.1.4** source at
`4fd3bf320d9566a27e60069fc8387448aaa3a094`, plus owner documentation, an agent entry
point and focused generated-file ignore rules. Branch: `codex/freecad-1.1.4-baseline`.
No previous Plus application changes have been carried into this branch. Group 1
has begun with its structural contract; its first application pilot is next.
The official 26.3 RC1 is a prerelease, not the stable version selected by the owner.

## Where to go

| Task | Reference |
| --- | --- |
| Component/document target contract | [Architecture](ARCHITECTURE.md), [Group 1 stages](DEVELOPMENT_ROADMAP.md#group-1--component-panel-and-document-structure) |
| Intended UI/workflows | [UI specification index](UI_UX_SPEC.md) |
| Unconfirmed implemented ideas from old fork | [Review inventory](ui-ux-specs/UNVERIFIED_IMPLEMENTED_CHANGES.md) |
| Conversation evidence and conflicts | [Evidence ledger](ui-ux-specs/EVIDENCE_AND_DECISIONS.md) |
| Prior fork recovery | [Archive reference](ARCHIVE_REFERENCE.md) |
| Current work/status | [Roadmap](DEVELOPMENT_ROADMAP.md), [WORK_STATE](WORK_STATE.md) |
| Stable baseline inventory and local checks | [Runtime inventory and completed display check](WORK_STATE.md#stable-baseline-inventory-and-light-runtime-check--october-10-2026) |
| Execution/build guidance | [Development guidelines](DEVELOPMENT_GUIDELINES.md), [guide](DEVELOPMENT_GUIDE.md) |
| Product scope | [Product specification](PRODUCT_SPEC.md) |
| Old implementation records | [Historical documents](archive/pre-restart-docs/README.md) |

## Source map

- src/App and src/Gui: upstream document/application and desktop services.
- src/Mod: original workbench modules; retain their source and availability.
- tests and per-workbench tests: upstream test infrastructure.
- CMakeLists.txt, CMakePresets.json and .github/workflows: this release's build definitions.
- .gitmodules: this release's pinned GSL, OndselSolver, AddonManager and GoogleTest.

Existing external FreeCAD Plus builds use the archived implementation. They do not
validate or represent this clean checkout. Reimplementation begins only from an
explicit task and confirmed requirements; historical backlog entries do not restart work.
