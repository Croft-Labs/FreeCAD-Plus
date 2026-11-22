# Sketch dimensions and feature-task tabs

`approval.json` records approval of the direct native storyboard. Approved images
are staged previews; installed images are independent captures of actual behavior.
No production code removes constraints after drawing: the shared QuantitySpinBox
fix drains signal-blocked programmatic notifications before their blocker expires.

The regression runner uses isolated native processes and test source from this repo.
Product modules load from the selected build/app payload; paths are recorded.
Run with the development runtime's `build/bin/python.exe`:

    run-validation.py regression --installed --broad
    run-validation.py visual --installed
    run-validation.py reopen --installed

GUI checks run sequentially for reliable focus. Focused cases use actual viewport
clicks for Rectangle, Circle, Line and Arc; verify typed on-view dimensions, blocked
programmatic values, existing dimensions/Undo/Redo, all previous tabs, manual browsing,
sketch placement-to-drawing handoff, custom accept/cancel, native datum editors,
standalone Part creation dialogs without an in-edit feature,
external sources, context/document closure and failed native entry. The broader suite
also checks prior Extrude, visibility, numeric input, Sketch, Plane, Move and Rotate.

Visual and fresh-process reopen checks preserve native sketch geometry/constraints
and exercise History entry/restoration without staged hooks or injected product code.
The shortcut check uses the existing desktop shortcut with explicit isolated config
and data paths. Installation retains rollback files and matching source/build/app hashes.
