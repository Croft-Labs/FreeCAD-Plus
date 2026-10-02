# Components pane regression procedure

Use the source-built FreeCAD Plus executable and fresh evidence directories.
The runner isolates preferences and documents; disable source overlays. Never use
the separately installed upstream FreeCAD as validation evidence.

| Tab or boundary | Coverage |
| --- | --- |
| Models | Flat definition inventory, unused models, nested/repeated use counts, selection, rename/Undo/Redo, Add Instance, double-click isolated editing and return to assembly |
| Part Tree | Permanent first root, grouped instances, exact occurrence editing/selection, visibility/representations, BOM inclusion, instance-only deletion, active-parent fallback, copy/externalize/repair, Cut/Paste, drag/drop events, ordering/reparenting and placement |
| History | Active owner, origin and planes visibility/deletion protection, public operations with background results hidden, selection, checkbox suppression/dependencies, bulk Undo, double-click task editing/Cancel, references/repair, conversion and BOM |
| Cross-tab lifecycle | Deferred refresh during menu lifetime, open-task edit refusal, repeated tab/refresh cycles, close-last-document reset, shared hierarchy persistence and native Attributes |
| Display and persistence | Plus and Classic UI, narrow-pane screenshots, owning-file save/Undo, external documents, missing files, `.cadprt` save/reopen and cold-process standard New/Open/Save |

Run `tests/RunComponentDocument.ps1` with `-Executable`, a fresh
`-OutputDirectory` and one suite switch per process:

- `-FeedbackSmoke`: 44 checks, including source/build payload identity and native Attributes.
- `-IntegrationSmoke`: 24 external/edit/display/save/Undo/reference/BOM checks.
- `-CoreSmoke`: 39 ownership/geometry/history/conversion/persistence checks.
- `-TreeMoveSmoke`: nine clipboard/drop/order/reparenting checks.
- `-PaneInteractions`: ten workflows using native Qt mouse input, context actions,
  task locks, 60 tab/refresh cycles, 24 shared nested uses and both UI styles.
- `-ColdFixtureDirectory <CoreSmoke output>`: six fresh-process checks, including
  reopened Models counts, occurrence-only Part Tree, origin/reference History and
  camera commands across closing/restoring views.
- `-RibbonSmoke`: seven UI integration checks, including deferred rendering while
  native Sketcher initializes its Python workbench wrapper.

Each run retains `results.json`, per-suite logs and a process result. Strict pass
requires no failures, errors or skips and process exit zero. Feedback also requires
loaded modules to come from the build, match source hashes, and native Attributes
to hide the old Model tree. Additional runtime modules must not invalidate that
identity check. Do not count reruns as additional distinct tests.
The runner also rejects unhandled GUI camera exceptions, uninitialized workbench
wrapper errors and deleted Qt row diagnostics in stderr; test assertions alone
must not declare those runs clean. Missing-file and inactive-geometry messages
from deliberately broken recovery/suppression fixtures remain expected evidence.

`WORK_STATE.md` records the current incorporation and exact evidence. Qt input,
native drop events and captured widgets establish automated GUI coverage;
physical desktop gestures, other DPI/theme combinations and very large assemblies
remain separate acceptance work.
