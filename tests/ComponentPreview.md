# Component modeling preview acceptance

REQ-014f covers Extrude, Revolve, Loft, Pipe, Helix and Primitive. Run
`TestComponentPreview.py` through `RunComponentDocument.ps1` against the staged
Plus launcher, without source overlays.

1. Each task offers a Preview type dropdown: None, Overlay, Result. Overlay and
   automatic updates are the defaults.
2. Complete a closed profile (and required sections/path/axis for its operation).
   New Body is blue, Add green, Subtract red. Add/Subtract need no target for an
   overlay. A disjoint target must not suppress or clip that overlay.
3. Set a subtract extrusion to 5 inches through a 1-inch target. Its overlay
   spans all 5 inches; Result shows the cut target with normal body appearance.
   Check offset and two-sided lengths as well.
4. Result validates the actual Boolean. A missing/invalid target removes any old
   preview and reports the error. OK retains its strict validation.
5. Switch Overlay/Result/None while creating and editing. Cancel restores prior
   visibility and transparency. Curves retain their separate task highlights.
6. Reference-defined extents require valid geometric references; do not invent
   limits for Through All, To First/Last, face bounds or sweep paths.

The tests compare complete tool volumes and shapes across all six backends,
including missing and disjoint targets, verify native source isolation and
placement, exercise automatic updates/colors, and check preview/cancel cleanup.
Existing operation suites cover geometry, edit/undo/persistence and routing;
curve and narrow-task suites cover retained selection and vertical scrolling.
WORK_STATE records reports, visual inspection, build identity and delivery.

Shared control regression: the six tasks must instantiate `PreviewControls` from
`ComponentTaskWidgets`; all five curve tasks use its `CurveCollector`, including
both Pipe path roles. The runtime suite checks these actual task instances and
retains automatic colors, timer ownership and preview/cancel behavior.

Run `TestComponentCurveDisplay.py`, `TestComponentCurveProfile.py` and
`TestComponentTaskWidth.py` alongside this suite. The native viewport regression
clicks rectangle edges at 0, 35 and 65 degree view angles, with offsets within
the pick radius. Each native edge notification must add only that edge. Sequential
picks accumulate edges; a repeat removes its edge and leaves no list row selected.
An unobstructed interior click must still collect all four boundary curves.
Native origin axes deliberately remain visible; the sequential probe uses edges
that do not coincide with them. The profile suite separately checks solid occlusion,
origin helpers, placed sketches and region collection. Delete, both Pipe path
roles, section emphasis and 360-pixel vertical-only task scrolling remain covered.
