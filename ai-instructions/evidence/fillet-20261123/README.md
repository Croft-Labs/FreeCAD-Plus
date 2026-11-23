# Fillet freeze repair — November 23, 2026

Owner reproduction: rectangular sketch, Extrude, open Fillet, delete the automatically
selected edges, then pick an edge. No new task layout was introduced.

## Cause and repair

An isolated installed-baseline run with Connected Curves reproduced the hang after
clearing the list and picking an edge. The [progress log](baseline-hang.txt) stops
at that pick; the harness terminated its own process at the 60-second deadline.
FreeCAD queues selection notifications emitted inside an observer. The Plus chain
selector's recursion guard ended before those queued notifications were delivered.
Fillet clears consumed picks, allowing the observer to repeatedly refill the queue.
Mapped names also caused the seed edge to be added twice and toggled off.

The selector now defers expansion until the seed notification drains, delivers extra
edges under its guard and canonicalizes the seed. Pending keys deduplicate selection
events; document/editor/task checks discard deferred work after task exit. Native
selection gates, filters and occurrence paths remain authoritative. This shared
repair covers consuming feature tasks, including the tested Fillet and Chamfer.

Fillet in Plus component documents no longer implicitly enables Use all edges for
a whole solid. It opens an empty collector ready for explicit picks. Explicit
preselected edges/faces and the opt-in Use all edges control remain. Target routing
uses the selected solid or a sole component result, never Classic's ambient Body;
multiple results require selection. Ordinary legacy documents retain native entry.
Geometry generation, native saved identities and task layout are unchanged.

## Verification and delivery

- [Eight focused final build checks](build-regression.json) passed.
- [All 90 installed regressions](installed-regression.json) passed, including an
  actual viewport mouse click after clearing, repeated connected/tangent picks,
  single-edge recovery, cancellation of deferred picks, multiple solids, native
  legacy entry, Undo/Redo, component admission, selection filters and Sketcher.
- [Installed task audit](audit.json): empty entry, twelve connected edges, clear,
  one edge, valid accepted result of 2397.8539816339744 cubic mm.
- [Separate-process reopen/edit/Cancel](reopen.json) passed. Its fixture is recreated
  by the [existing desktop shortcut check](shortcut.json), which also passed.
- Four payload files installed with [hash verification and retained rollback copies](install-manifest.json).
  Owner documents, running sessions, settings and project.previewfirst.json preserved.
  Older owner processes must restart to load the installed fix.

Direct installed captures: [empty Fillet](fillet-empty.png),
[single edge after clearing](fillet-single-after-clear.png),
[connected viewport pick after clearing](fillet-after-clear.png).

The initial broad run exposed a diagnostic harness timing issue and a component
context message regression; both were corrected before the final checks. The old
multi-solid empty-selection test was updated to assert explicit target selection
instead of relying on Classic's active Body. One build attempt overlapped a diagnostic
process holding a DLL; after that process exited the build completed normally.
Reopen harness now explicitly activates the saved component occurrence before editing.

Harnesses are archived here for evidence; their original execution directory is
`C:/Users/dgium/Documents/__Apps/FreeCAD/fillet-validation`. Generated validation
profiles are isolated from the owner profile; the rollback directory is retained.
