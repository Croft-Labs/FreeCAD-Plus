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
