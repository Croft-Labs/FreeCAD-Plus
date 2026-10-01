# CAM Simulator input review (F095)

Use **CAM > CAM Simulator** in the source-built FreeCAD Plus fork. This checkpoint
covers the current OpenGL simulator's input preparation and review. The Legacy CAM
Simulator is unchanged. It does not complete collision or removal-accuracy acceptance.

1. Open a native CAM job with recomputed BRep model/stock, two active operations and
   valid solid cutters. Select the job and open CAM Simulator. The review lists stock
   dimensions in millimeters, quality level, selected operations in saved job order,
   command counts, tool numbers and cutter diameters.
2. Check/uncheck operations. The review follows those choices; no checked operations
   disables Play. The existing visibility-following option is retained. Quality is
   identified as an engine display setting, not a certified geometric tolerance.
3. Press Play. All selected paths and native cutter profiles are prepared before the
   current simulator session is reset. Tool selections are submitted before their
   corresponding operations. Inputs and toolpath objects are not edited.
4. Change a path, cutter or stock parameter while the task is open. Play disables and
   the old review clears. Recompute and click **Review inputs**. Inspect the new
   values, then restart. The simulator view still reflects its last submitted inputs;
   the task does not claim it follows later model edits automatically.
5. Remove the second operation's tool assignment, or give two different cutters the
   same tool number. Review should show the problem and disable Play, without
   resetting the previous simulator session. Repair and review again. Stale inputs,
   empty toolpaths, invalid stock/tool geometry and non-finite parameters are refused.
6. Close, save/reopen the document, and review it again. Selection/visibility policy
   remains native; the reviewed operations and stock come from the reopened job.

The coverage statement stays visible: selected job paths are used before
postprocessing. This review performs no holder, fixture or machine-envelope
clearance checks and provides no real-machine safety certification. Unsupported
controller behavior is not made valid by passing input preflight. Actual stock
removal accuracy, gouges, collision classification and machine/controller coverage
remain open under full F095.

Run `TestSimulationReview` and `TestSetupTemplates` in the source-built GUI with
`tests` on `sys.path`. Roadmap 14.3a/b owns staging, native handoff and GUI evidence.
The test distinguishes a real native simulator startup from mocked submission
checks used to prove that failed preparation cannot reset/feed a prior session.
No machine run, installer or release is implied. Stop at this usable owner-test
checkpoint and rotate; refine after workflow feedback or a demonstrated blocker.

Accepted evidence: `D:\Temp\Office-PC\freecad-plus-simulation-review-20261001`.
One grouped PathScripts staging pass; 17 distinct checks and five reviewed captures.
The visual-final/ folder contains Simulation-Review.FCStd and Simulation-Reviewed-Stock.FCStd.
These fixtures demonstrate input review and native startup, not proven collision
classification or quantitative material-removal accuracy.
