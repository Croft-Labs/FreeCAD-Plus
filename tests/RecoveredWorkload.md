# Recovered workload grouped acceptance

This is the item 7 acceptance procedure, not a second roadmap. WORK_STATE owns
status. Run the exact classes below using the retained RecoveredAcceptance.FCMacro
and isolated run_acceptance.py harness in evidence task
01a10f79-1a93-7be0-a261-96a6b7e9c425; inspect/adapt their current source before use.
Never add application-source directories to sys.path. Test code alone may come
from this checkout. Record the tests SHA-256 snapshot before execution.

| Module | Classes | Current expected checks |
| --- | --- | ---: |
| TestDesignSelection | TestDesignSelectionNative, TestDesignSelectionToolbar, TestDesignSelectionBoxes | 19 |
| TestDesignLayers | TestDesignLayers | 10 |
| TestConstraintPalette | TestConstraintPaletteNative | 14 |
| TestMoveComponents | TestMoveComponents | 12 |
| TestMoveComponentsRotate | TestMoveComponentsRotate | 8 |
| TestMoveComponentsPoint | TestMoveComponentsPoint | 4 |
| TestMoveComponentsAxes | TestMoveComponentsAxes | 5 |
| TestMoveComponentsFrames | TestMoveComponentsFrames | 5 |
| TestMoveComponentsInteractive | TestMoveComponentsInteractive | 5 |
| TestMoveComponentsIntegration | TestMoveComponentsIntegration | 7 |

Full suite: 89 checks. High-DPI subset: Selection/Layers/palette/Interactive/
integration, 55 checks. Require every suite, no skips, final results.json and
validation.done; partial progress never establishes acceptance. Counts are a
sanity check, not permission to omit new tests. The added Axes/Frames/Interactive
assertions and deferred Escape race case have not run natively yet.

1. Verify the configured grouped Plus build and source/native binary snapshots.
   C++ changes require one batched native compile; preserve prior completed
   ALL_BUILD logs and resource/compiler retry evidence. Do not use upstream
   installed FreeCAD. Check diagnoseConstraintAdditions/setDrivingBatch exist.
2. Refresh/stage the exact current Python modules and compile the repository
   FreeCADPlus.exe launcher. Launch it with isolated user/system settings, test
   temp directory and explicit expected AppHome. Run all 89 checks at system DPR.
   Record App.Version (including its actual embedded compiled revision), paths,
   working directory and source/binary hashes. Do not relabel an old embedded
   revision with the latest documentation commit.
3. Require runtime files inside verified AppHome and byte hashes matching this
   checkout: ComponentModel, DesignSelection, DesignSelectionToolbar,
   DesignLayers/Gui, ConstraintPalette/Gui, MoveComponents/Task/Manipulator,
   PlusRibbon and ComponentNavigator. Record test source hashes separately.
4. Run the 55-check high-DPI subset using QT_SCALE_FACTOR=2 on this host (earlier
   system DPR 1.5 gave effective DPR 3.0). Record actual measured DPR and screen
   geometry. Use new evidence directories; retain earlier failures.
5. Inspect all six narrow Tasks views, live framebuffer and actual axis/plane/ring
   and Edit Pivot captures. Native mouse/release/Escape events are mandatory;
   direct placement writes or numeric-only substitutes do not establish handles.
   Exercise camera navigation and document/tab/mode cleanup. Verify external
   owning-file guards, outside-parent picks and both shared parent occurrences.
6. Confirm native transactions, committed-invalid driving batches, retained
   identities/expressions/geometry, independent Body input sketches, Undo/Redo
   and FCStd/cadprt reopen. Recheck no-op, Cancel/prior Apply and persistence on/off.
7. Synchronize final owner DOCX acceptance, render/inspect affected pages. Update
   the exact desktop FreeCADPlus.exe - Shortcut.lnk per DEVELOPMENT_GUIDE; reopen
   target/workdir, launch the saved link, verify runtime home/workdir and run
   Selection/integration smoke classes (19+7=26 current checks). Record actual
   shortcut verification separately from direct launcher tests.
8. Publish coherent fixes/final evidence to origin only, without force, and verify
   remote branch. Do not report owner-ready until all delivery gates pass.

The item 6 quick check runs the actual deferred Python clear function with a
controlled scheduler in four orderings: valid Escape, superseding click, mode exit
and changed document. It is Python callback evidence only, not Qt/native input
acceptance. Item 7 must execute the corresponding native toolbar regression.
