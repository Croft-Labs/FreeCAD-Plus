# Task panel

Status: owner-intent specification, reconstructed 2026-10-10. **Only the confirmed requirements are authoritative.** Material headed **Needs owner confirmation** is preserved for review and must not be treated as an approved change. The current application, agent-written specifications and implementation reports do not establish owner approval. Newer explicit owner decisions supersede older decisions on the same subject. See [evidence and unresolved decisions](EVIDENCE_AND_DECISIONS.md).

## Confirmed requirements

### Idle task panel

Before a document exists, show **New File** and **Open**. Dock Tasks at the right initially and preserve the user's later customized location. The DOCX's proposed actions after New File are retained below for confirmation. Do not derive additional idle actions from whichever commands the current build happens to display. [C06](EVIDENCE_AND_DECISIONS.md#c06)

### Shared task patterns

Use sketches, operations/features and other geometry as the user's modeling vocabulary. Background Body ownership must not require independent Body management. Feature selection lists, collapsible sections, preview choices and their exact defaults are preserved in the DOCX-derived sections below; most earlier authorizing conversations are unavailable. Do not silently remove fields just because a toolbar action is consolidated. [Current owner direction](EVIDENCE_AND_DECISIONS.md#current)

A modeling operation requires an edited component. The pinned file cannot own sketches or modeling geometry; selecting a component once does not enter Edit. Definitions, storage, external edits and the deferred Add Component workflow follow [Component Panel](COMPONENT_PANEL.md). [C09](EVIDENCE_AND_DECISIONS.md#c09)

### Layers

Open Layers in Tasks from the Design-only toolbar. Support create, rename, delete, assignment and choosing the active layer. Double-click a layer to activate it; show bold text and a check mark. Provide an eye on each row for visibility. Base is permanent and cannot be deleted or renamed; Origin stays on Base. [R03](EVIDENCE_AND_DECISIONS.md#r03)

Each independent object has one layer. A sketch and a body consuming it are separate units and may use different layers. A body's building operations stay with that body; moving its layer does not move input sketches. Selecting a body-producing operation for assignment resolves its result unit; do not require the user to manage an exposed backend Body container. New independent objects use the active layer; operations on an existing result retain its layer. [R03](EVIDENCE_AND_DECISIONS.md#r03), [current owner direction](EVIDENCE_AND_DECISIONS.md#current)

Hide/show preserves individual visibility choices and must not reveal intermediate results. Deleting a layer moves its members to Base and never deletes geometry. Deleting the active layer activates Base. Save/reopen and Undo/Redo preserve layers, assignments, visibility and active choice. [R03](EVIDENCE_AND_DECISIONS.md#r03)

### Move Components

This is one task panel for whole linked **component instances**, including descendants. Copy is performed separately through Part Tree Copy/Paste. The first field is Workflow, in this order: **Translate, Rotate, Point to Point, Align Axes, Align Coordinate Systems, Interactive**. Next is the Components list with selection, Remove/Delete and Clear. [R03](EVIDENCE_AND_DECISIONS.md#r03)

The first movable instance establishes its immediate parent as the active editing context; then accept only siblings under that parent. Listed children carry their descendants implicitly. Several siblings move as one rigid group. A parent definition owns its children's relative placements: moving them changes corresponding children in every instance of that parent. Any visible geometry may supply a reference, but resulting placement stays relative to the parent. Do not introduce global/local mode switches or individual child frames. [R03](EVIDENCE_AND_DECISIONS.md#r03)

Provide **Apply, OK, Cancel**. Preview does not commit geometry or placement. Apply commits one undoable group movement, keeps the task open and resets movement inputs. With Persistent Selection on, retain the component list; off clears it. OK applies pending movement and closes; after Apply it only closes. Cancel discards the pending preview but leaves earlier applied moves available through Undo. A no-op creates no Undo entry. Switching methods discards uncommitted movement inputs while retaining eligible siblings and context. Explain invalid selections inline; do not move an unexpected subset. [R03](EVIDENCE_AND_DECISIONS.md#r03)

| Method | Fields and reference choices | Interaction and reset |
| --- | --- | --- |
| Translate | Parent X/Y/Z or straight visible line/edge/axis; nonnegative Distance; Reverse | One direction and distance, not XYZ displacement fields. Apply clears direction, zeros distance and turns Reverse off. |
| Rotate | Parent axis through its origin, picked located line/axis, or two points; optional pivot; angle magnitude; Reverse | Positive follows the displayed axis/right-hand rule. Rotate both positions and orientations about the common pivot. Apply clears axis/pivot/angle and Reverse. |
| Point to Point | Separate Source and Destination point collectors; vertices, sketch/reference points, origins or well-defined centers | Pure translation; keep orientation. Source may be outside moved set. Coincident points are a no-op. Clear both references on Apply. |
| Align Axes | Source/Target line, reference, circular or cylindrical axes; Make Parallel / Make Coincident; Reverse Target Direction | Default Coincident maps source anchor to closest target-axis point. Parallel preserves source anchor. Use minimal rotation; no arbitrary axial slide or hidden roll. Reset picks and method defaults after Apply. |
| Align Coordinate Systems | Source and Target frames; existing origins/datums, Parent frame, or expandable Origin/Z/X definitions | Align origin and all axes including roll. Reject degenerate, reflected or scaled frames. Show triads, not matrices. Clear frame inputs on Apply. |
| Interactive | Translation arrows and plane handles, rotation rings, Move Components / Edit Pivot, Reset Pivot, numeric active-handle input, optional snapping | Parent-aligned group-center pivot initially. Pivot editing alone changes no geometry or Undo. Drag release leaves pending preview. Escape cancels the current drag before broader selection handling. Apply commits composed movement and resets/recenters the pivot for retained selection. |

References are snapshots for a one-time placement edit, not new joints or associative features. Respect constrained/read-only instances. Preview must remain stable as references on moving objects are picked. Preserve camera interaction and clean up handles and capture on task/mode/document exit. [R03 and adopted prompts 4–9](EVIDENCE_AND_DECISIONS.md#r03)

The owner explicitly allowed extrapolation **within the remaining Move Components workflows**. That permission does not authorize extrapolating other operation dialogs. The detailed adopted prompts are source evidence, not a queue to run again.

### Operation coverage and unconfirmed workflows

Every original toolbar command remains cataloged in [Toolbars and Buttons](TOOLBARS_AND_BUTTONS.md#section-3-combined-button-catalog-by-original-workbench). Unless a confirmed change appears here, its original upstream workflow is retained as the baseline; this does not approve the fork's later custom editor. Task fields not yet defined must remain explicitly unspecified.

The following transferred DOCX material covers New Component, Coordinate System/Plane/Axis/Point, New Sketch/attachment, Extrude, Revolve, Loft, Pipe, Helix, Primitive, Pattern, native dress-ups/transformations and CAM. Do not infer a new custom workflow for placeholders such as New Group or Variable Set. Sketch Freedom and Constraint Repair, Interactive Feature Handles, and Broken Reference Repair were explicitly deferred in the recovered discussion; their appearance in an old roadmap or implementation is not approval. [R03](EVIDENCE_AND_DECISIONS.md#r03)

## Transferred DOCX requirements — Needs owner confirmation

The following source candidates are not instructions to implement. Exact values, added restrictions and implementation-derived details need owner confirmation. D numbers identify the archived DOCX paragraphs; [the coverage record](archive/2026-10-10/docx-coverage.json) accounts for every source block. Confirmed rules above override conflicting candidate wording. Implementation reports remain archival only.

### Shared modeling task sections

**D2668 — Needs owner confirmation:** Combine the specified additive and subtractive Part Design operations into shared feature workflows. Preserve their native parameters and the additional fields specified here. A change in icon, toolbar grouping or task layout must not silently remove a required field or choice.

**D2669 — Needs owner confirmation:** Use the same task pane for creating and editing a feature.

**D2670 — Needs owner confirmation:** Section 1: Main Parameters, expanded by default.

**D2671 — Needs owner confirmation:** Boolean choice: New Body, Add or Subtract. Show the target Body selector for Add and Subtract only; the selected target remains a background result object.

**D2672 — Needs owner confirmation:** Profile selection: Whole Sketch or Selected Curves, with a list of the selected curves.

**D2673 — Needs owner confirmation:** Keep Mode and Type as separate fields: Mode controls sidedness; Type controls the extent or termination.

**D2674 — Needs owner confirmation:** Section 2: Dimensions, expanded by default.

**D2675 — Needs owner confirmation:** Retain the applicable direction selector, sketch-normal default, length and reverse-direction arrow buttons.

**D2676 — Needs owner confirmation:** Retain Offset and the other dimensions native to the selected operation, including taper or angular fields where applicable.

**D2677 — Needs owner confirmation:** Section 3: Advanced/Optional, collapsed by default. Keep applicable native controls available rather than deleting them to simplify the main section.

**D2678 — Needs owner confirmation:** Section 4: Preview, expanded by default.

**D2679 — Needs owner confirmation:** Retain Recompute on Change and the preview choices None, Overlay and Result. Overlay is the default.

**D2680 — Needs owner confirmation:** Overlay colors: blue for New Body, green for Add and red for Subtract. Show the full tool even without a target or Boolean intersection.

**D2681 — Needs owner confirmation:** Keep preview behavior consistent when fields, profile selection, direction or termination change.

### Common actions

**D2684 — Needs owner confirmation:** The common toolbar retains New File, Open, Save, Save As, Undo, Redo, Recompute, Cut, Copy and Paste. New File uses the native New Document icon. Detailed command placement and the complete button descriptions are now in TOOLBARS_AND_BUTTONS.md (the original reference is archived).

### Component creation and storage

**D2686 — Needs owner confirmation:** Use the component definition/instance distinction for structure actions. Do not create both a visible definition and a linked occurrence as two assembly instances when the user requests one.

**D2689 — Needs owner confirmation:** New Component offers domestic storage in the active componentâ€™s defining file, a new external file, or an existing external file. Choose a location for a new file or select the existing file, then enter a unique component name. Creation does not place an instance in the current assembly. A new external file contains the named component beneath its pinned file row, without an extra Part001. Add Component places one linked instance under the active component.

**D2691 — Needs owner confirmation:** Name automatically added parts Part001, Part002, Part003 and so on, using the next available number.

**D2692 — Needs owner confirmation:** Deleting an instance from Part Tree leaves its definition available in Models.

**D2693 — Needs owner confirmation:** Domestic components belong to the current file. External components belong to imported files. Display a domestic name as M3 screw and an external name as M3 screw (Hardware). The qualifier is the source filename; use its path when identical filenames would be ambiguous. Names must be unique within a file, but different files may contain components with the same name.

**D2694 — Needs owner confirmation:** Import Component File adds a collapsible file group to Models without placing a component. Show all components in that file, including unused components, and nested file imports beneath its definitions. Removing the last placed instance retains the imported file in Models. A missing file remains visible with Locate Component File for recovery.

**D2697 — Needs owner confirmation:** Copy to Domestic Components creates a separate definition and copies its domestic subcomponent hierarchy. Existing external child definitions remain shared. Prompt with a checklist of placements in the domestic file to replace; leave all unchecked by default. Cancel keeps the new copy and leaves placements unchanged. Preserve placement positions when replacing. Explain any downstream reference or display override that must be repaired before replacement.

**D2698 — Needs owner confirmation:** Copy to External File creates an independent file definition and retains the original definition and its placements. Do not offer an identity-preserving move between domestic and external storage. Editing a copied definition does not change the original definition. The destination file places the copied component beneath its pinned file row, without creating an extra Part001.

### Coordinate System and Datum Plane

**D2700 — Needs owner confirmation:** Provide a Coordinate System action in the new-file Tasks pane and as a medium Home action.

**D2701 — Needs owner confirmation:** Its dropdown offers Plane, Axis and Point.

**D2703 — Needs owner confirmation:** Make Datum Plane available from the new-file Tasks pane and within New Sketch creation.

**D2704 — Needs owner confirmation:** Section 1: Plane orientation and location. Select geometry is the default; Enter values is the alternative. The shared selection list accepts an origin/user plane, flat face, two coplanar non-collinear body edges or lines (including an origin axis with a line), three non-collinear points, or a line and an off-line point. Planar curves may participate; reject contradictory or non-coplanar geometry. An adjacent [...] menu offers XY, YZ and XZ planes. Show Under-defined, Defined or Invalid with an explanation. Enter values exposes X/Y/Z offsets and x'/y'/z' normal components, normalized on acceptance. Provide Reverse normal direction and a signed Offset distance with its own Reverse button.

**D2705 — Needs owner confirmation:** Section 2: Orientation. Use the same shared selection list for the projected X direction. Accept one body edge, line or origin axis, or two points including curve endpoints. The adjacent [...] menu offers X, Y and Z axes. Show Under-defined, Defined or Invalid. An empty list defaults to the component axis closest to the plane; break ties X, then Y, then Z. Project the chosen direction onto the plane; reject a zero projection. Provide Reverse direction for +X versus -X; derive Y to keep a right-handed frame.

**D2706 — Needs owner confirmation:** Section 3: Origin selection. A single-item selection textbox defaults to the part origin projected onto the plane. Clicking the field activates picking of an origin, point or curve endpoint. Project the selected point onto the plane. Delete clears the reference and restores the default.

**D2707 — Needs owner confirmation:** Section 4: Preview. Preview enables a translucent purple plane overlay; Recompute on update controls automatic updates. Both checkboxes default on. The overlay creates no document object and cannot intercept selections. When automatic updates are off, toggling Preview off/on refreshes it; OK always validates and recomputes the saved plane.

**D2708 — Needs owner confirmation:** A plane created while preparing a sketch becomes an available sketch attachment in the same workflow.

**D2835 — Needs owner confirmation:** Datum-plane create/edit uses the four sections specified above from the standalone Plus Plane action, native Datum Plane command in a component document, and component History editing. Both geometry lists reuse the modeling curve collector with broader reference filters, latest-item highlighting, repeat-click deselection, Remove/Clear and Delete. Plane inputs accept faces, planes, axes, edges, curves and points; orientation accepts edges, axes and points. Retain associative native dependencies, Undo/Redo, save/reopen, public PartDesign plane identity and hidden-helper cleanup. Opening older planes preserves their frame; legacy arbitrary rotations are retained as explicit values with stored origin and X direction. Existing sketch attachment and embedded Create Datum Plane behavior remain available. All task forms inherit Qt and active-theme colors. Prohibit task-level stylesheets that force foreground/background palette colors across child widgets, and copied form palettes that freeze colors. Preserve native dropdown, disabled-text and live theme handling; ribbon colors refresh with palette changes. Keep origin axes and planes small normally; show axes, planes and the origin point at twice normal size during plane and sketch placement editors, then restore prior size and visibility. Use a narrow task panel with vertical scrolling only.

### Other structure actions

**D2710 — Needs owner confirmation:** Keep Axis available from the Coordinate System dropdown. No additional task-field changes have been specified.

**D2712 — Needs owner confirmation:** Keep Point available from the Coordinate System dropdown. No additional task-field changes have been specified.

**D2714 — Needs owner confirmation:** No additional New Group changes are specified.

**D2716 — Needs owner confirmation:** Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

**D2718 — Needs owner confirmation:** Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

**D2720 — Needs owner confirmation:** Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

**D2722 — Needs owner confirmation:** Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

**D2724 — Needs owner confirmation:** Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

**D2726 — Needs owner confirmation:** Proposed consolidation: these link actions may be replaced by Add Instance or Add Reference Object. This remains a proposal; replacement behavior has not yet been specified.

**D2728 — Needs owner confirmation:** No additional Variable Set changes are specified.

### New Sketch and attachments

**D2732 — Needs owner confirmation:** Open a sketch creation task without requiring a Body or attachment to another object.

**D2733 — Needs owner confirmation:** Show the origin XY, XZ and YZ planes when New Sketch is clicked. Clicking a plane selects and highlights only that plane and updates the task selector. Keep the other planes visible without selecting the whole Origin container. Retain temporary visibility restoration on Cancel and Base layer hiding of individual datums.

**D2734 — Needs owner confirmation:** Choose an origin plane, an existing user-created plane, one planar body face, two coplanar edges of one body, or Independent plane. Independent plane defines the sketch origin X, Y and Z and its orientation with rotation angles or explicit in-plane and normal directions, in component coordinates. Creating a separate datum plane remains available.

**D2735 — Needs owner confirmation:** Retain the plane selector and Offset field. Follow support is enabled by default; turn it off to copy the selected frame once without an attachment. Independent plane has no support. Reject collinear or non-coplanar edge pairs that do not define one flat plane.

**D2736 — Needs owner confirmation:** On OK, close the creation task before opening Sketcher. Do not show the prompt that another task dialog is already open.

**D2737 — Needs owner confirmation:** Retain New Sketch, Attach Sketch and Edit Sketch actions. For a body face, two-edge or user-plane attachment, save the last valid support plane location and orientation and the sketch origin and axes. Follow valid support movement. If the support is deleted, missing or unavailable because of an upstream error, keep the sketch at exactly its last valid frame and allow editing and downstream modeling. Resume following when the same support is repaired or restored by Undo; never attach to an unrelated replacement with the same name. Preserve the frame and support references through save/reopen.

**D2738 — Needs owner confirmation:** In Sketcher, retain active and reference curves, active and reference dimensions, and geometric constraints.

**D2739 — Needs owner confirmation:** Use Sketch001 for the first sketch in each component, independently of sketches in other components.

### Extrude

**D2741 — Needs owner confirmation:** The following sections capture the specified shared modeling workflows and the fields that must remain available.

**D2743 — Needs owner confirmation:** Combine Classic Pad and Pocket into Extrude, using the Pad icon. Classic Pad opens Add; Classic Pocket opens Subtract.

**D2744 — Needs owner confirmation:** Section 1: Main Parameters.

**D2745 — Needs owner confirmation:** Boolean: New Body, Add or Subtract; target Body selector for Add and Subtract only.

**D2746 — Needs owner confirmation:** Profile choice: Whole Sketch or Selected Curves. List all chosen curves in the task pane and allow a subset of a sketch.

**D2747 — Needs owner confirmation:** Selected curves must belong to the same sketch and form closed, non-self-intersecting boundaries.

**D2748 — Needs owner confirmation:** Require one connected region, with optional holes. Separate disconnected regions are not accepted as one extrusion.

**D2749 — Needs owner confirmation:** Clicking the area between two sets of closed curves in the viewport adds both boundary sets to the selected-curves list.

**D2750 — Needs owner confirmation:** Mode: One Sided, Two Sided and Symmetric. Preserve the familiar one-dimension, two-dimension and symmetric choices.

**D2751 — Needs owner confirmation:** Type: Dimension, To Last, To First, Up to Face/Surface and Up to Shape, with the native termination choices applicable to the operation retained.

**D2752 — Needs owner confirmation:** Section 2: Dimensions.

**D2753 — Needs owner confirmation:** Direction defaults to Sketch Normal; retain direction selection and reverse arrow buttons.

**D2754 — Needs owner confirmation:** Retain Length, the second length for Two Sided mode, Taper Angle and Offset, with the applicable termination reference fields.

**D2755 — Needs owner confirmation:** Section 3: Advanced/Optional. Keep applicable native Extrude settings available.

**D2756 — Needs owner confirmation:** Section 4: Preview.

**D2757 — Needs owner confirmation:** Retain Recompute on Change and None, Overlay and Result; default to Overlay.

**D2758 — Needs owner confirmation:** Show blue New Body, green Add and red Subtract preview volumes.

**D2759 — Needs owner confirmation:** Document window interaction.

**D2760 — Needs owner confirmation:** Show the selected preview and allow the specified handles to change Length and Taper Angle.

**D2761 — Needs owner confirmation:** Keep the background Body attached to its parent Extrude. Do not permit independent pane deletion to leave a visible orphaned solid.

### Revolve

**D2763 — Needs owner confirmation:** Combine Revolve and Groove into a shared additive/subtractive revolve workflow.

**D2764 — Needs owner confirmation:** Use the common task sections, preserving the native axis, angular extent, direction, target and termination fields applicable to the operation.

**D2765 — Needs owner confirmation:** Keep the colored Add/Subtract preview and the applicable native fields when changing the toolbar presentation. Additional angular-field changes are not specified here.

**D2836 — Needs owner confirmation:** Unified Revolve: Plus combines additive Revolution and subtractive Groove in one Tasks workflow for both creation and history editing. Main parameters, Dimensions, Advanced and Preview are collapsible sections. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters provides New Body, Add or Subtract, a target body shown only for Add or Subtract, a whole-sketch or selected-curves list, One angle / Two angles / Symmetric mode and native applicable extent types.

**D2837 — Needs owner confirmation:** Dimensions retains sketch vertical or horizontal axes and picked local axis references, angle values with synchronized direction arrows, and signed angular offsets from -360 through +360 degrees with an offset-flip arrow. Symmetric disables direction reversal. Entering a nonzero offset selects Offset automatically. Reference starts, first/last or surface termination, axis projection and refinement remain available where applicable. The rotational axis replaces the extrusion-only sketch-normal direction and angle replaces linear length.

**D2838 — Needs owner confirmation:** Preview offers Recompute on change, enabled by default, and None, Overlay or Result; Overlay is the default and uses blue for New Body, green for Add and red for Subtract. Cancel restores visibility and removes preview geometry. Native Revolution and Groove features retain geometry semantics. Type-changing edits preserve the component operation identity and published result references through undo/redo and save/reopen. Expression-driven definitions remain protected from task overwrites and can be edited through their native properties.

### Loft

**D2767 — Needs owner confirmation:** Combine Additive Loft and Subtractive Loft into the shared Loft workflow.

**D2768 — Needs owner confirmation:** Preserve the native section selection and applicable Loft fields, together with the common Boolean, target and preview controls.

**D2839 — Needs owner confirmation:** Unified Loft: Plus combines Additive Loft and Subtractive Loft in one component Tasks workflow for creation and History editing. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters has New Body, Add or Subtract, a target shown only for Add or Subtract, ordered sections, and Smooth or Ruled interpolation. Sections accept whole profiles, selected closed sketch regions with optional holes, or native end vertices. Retain ordered preselection and empty startup. Provide append, replace, remove, clear and section inspection.

**D2840 — Needs owner confirmation:** Loft Dimensions provides Move up, Move down and Reverse order. Section placements define the span; extrusion lengths, angular extents and offsets do not apply. Advanced retains Closed, Refine and Fuzzy tolerance: zero uses the native default; negative values request automatic tolerance. Preview has Recompute on change enabled and None, Overlay or Result. Default Overlay is blue for New Body, green for Add and red for Subtract. Cancel removes previews and restores visibility. Retain native geometry, associative sections and component result identities through edits, Boolean mode changes, undo/redo and save/reopen. Reject invalid or ineffective Booleans and protect expression-driven definitions from task overwrites.

### Helix

**D2770 — Needs owner confirmation:** Combine Additive Helix and Subtractive Helix into the shared Helix workflow.

**D2771 — Needs owner confirmation:** Preserve the native Helix geometry and dimension fields and the common Boolean, target and preview controls.

**D2845 — Needs owner confirmation:** Unified Helix: Plus combines Additive Helix and Subtractive Helix in one Tasks workflow for creation and History editing, with one Helix ribbon button and no additive/subtractive dropdown. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters provides New Body, Add or Subtract, an explicit target only for Add or Subtract, whole-profile or selected closed sketch-curve collection, and the four native modes Pitch-Height-Angle, Pitch-Turns-Angle, Height-Turns-Angle and Height-Turns-Growth. Helix has no independent sidedness or extent Type. Retain empty startup, preselection and curve add/remove/clear controls.

**D2846 — Needs owner confirmation:** Helix Dimensions retains sketch vertical (default), horizontal, normal and construction axes, direct component X/Y/Z choices, and picked or typed datum/origin/straight-edge/circular-edge axes. Show the selected mode's pitch, height, turns, cone angle or radial growth fields; derive dependent values when changing modes. Preserve the separate axial reverse arrow and Left handed choice. Suggest pitch and height from the profile uses the native bounds heuristic, also applied to initial preselection. Without a profile, defaults are pitch 10 mm, height 30 mm, 3 turns and zero angle/growth. Height-Turns-Growth supports native flat spirals. Advanced retains Subtraction/Common, Refine, fusion tolerance factor (default 0.1) and Fuzzy tolerance; the fusion factor is not a length. Do not invent extrusion-only length offsets or termination choices.

**D2847 — Needs owner confirmation:** Helix Preview retains Recompute on change enabled and None/Overlay/Result, default Overlay with blue/green/red for New Body/Add/Subtract. Cancel restores visibility. Preserve native geometry, associative references, component operation and published result identities, downstream consumers, undo/redo and save/reopen. Invalid geometry, stale/cyclic inputs and ineffective Booleans cannot be accepted; failed edits roll back and expressions remain protected.

### Primitive

**D2773 — Needs owner confirmation:** Combine additive and subtractive primitives into the shared Primitive workflow.

**D2774 — Needs owner confirmation:** Preserve the selected primitive type and its native dimensions, with the common Boolean, target and preview controls.

**D2848 — Needs owner confirmation:** Unified Primitive: Plus combines Additive and Subtractive Box, Cylinder, Sphere, Cone, Ellipsoid, Torus, Prism and Wedge into one creation and History editing task. Modeling retains one Primitive action and the Primitives dropdown presets a shape in the same task. Classic documents retain native Body tasks. Tab remains disabled because no native Tab feature exists. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters contains New Body, Add or Subtract, an explicit target only for Add or Subtract, and the shape selector. No sketch profile is required.

**D2849 — Needs owner confirmation:** Primitive Dimensions preserves every native shape property and default, including cylinder/prism X and Y skew, prism sides, angular limits and all ten wedge bounds. Shape switches retain the drafts dimensions during the task. Advanced retains the native attachment modes, ordered references with Add selected, Remove and Clear, reversal, path parameter and offset. Unattached primitives expose component-local XYZ and yaw/pitch/roll; attached primitives expose their offset. Defaults are Box, unattached, zero placement, Refine enabled and fuzzy tolerance zero. Subtract retains Subtraction or Common. Native attachment and dimension properties remain associative and editable.

**D2850 — Needs owner confirmation:** Primitive Preview uses Recompute on change enabled and None, Overlay or Result, default Overlay, with blue/green/red for New Body/Add/Subtract. Cancel restores display state. Shape or mode changes preserve operation and published-result identity, downstream consumers and History order. Native geometry, attachments, undo/redo and save/reopen remain intact; invalid solids, ineffective Booleans, stale/cyclic inputs and expressions are guarded.

### Dress-ups and transformations

**D2776 — Superseded placement:** The October 6 owner outline places Delete Face/Defeaturing in Other. The older DOCX Dress-Up placement is superseded; see [Modeling tab](TOOLBARS_AND_BUTTONS.md#confirmed-design-modeling-tab).

**D2778 — Needs owner confirmation:** Keep Part Design transformation operations in the Modeling Transformation group.

**D2779 — Needs owner confirmation:** Pattern editing must show individual instance suppression controls immediately on opening. Suppress or restore a selected copy without losing direction, reference collectors or the shared Linear/Circular settings; accepting with live preview disabled must still apply the final parameters. MultiTransform supports Circular, Path and Point Pattern entries and opens the matching native parameter editor. Preserve the Plus unified Pattern entry and its existing ribbon groups.

### Inherited workbench workflows

**D2781 — Needs owner confirmation:** No additional feature workflow changes are specified for this workbench in this outline.

**D2783 — Needs owner confirmation:** No additional feature workflow changes are specified for this workbench in this outline.

**D2785 — Needs owner confirmation:** No additional feature workflow changes are specified for this workbench in this outline.

**D2787 — Needs owner confirmation:** No additional feature workflow changes are specified for this workbench in this outline.

**D2789 — Needs owner confirmation:** No additional feature workflow changes are specified for this workbench in this outline.

**D2791 — Needs owner confirmation:** Preserve the existing CAM workflows while applying the inherited controls and behavior below.

**D2792 — Needs owner confirmation:** CAM operations and dress-ups use the selected work plane origin and orientation consistently in preview, inspection and post-processing. Avoid Faces keeps the selected regions protected with the corrected Safe STL clearance. Missing or invalid inputs must clear the generated toolpath and report the failure, including failed holding-tag generation and probe-map points outside the valid area. The CAM Job preferences include the Sanity report output-file setting; Mill Facing offers Circular clearing, and Simple Copy opens its native task.

### Idle actions after New File

**D2799 — Needs owner confirmation:** The Tasks pane offers New Sketch, Coordinate System, Datum Plane and Add Component.

### Pipe

**D2842 — Needs owner confirmation:** Unified Pipe: Plus combines Additive Pipe and Subtractive Pipe in one component Tasks workflow for creation and History editing, with one Pipe button after Loft in Modeling. Main parameters, Dimensions and Preview start expanded; Advanced starts collapsed. Main parameters provides New Body, Add or Subtract, a target only for Add or Subtract, ordered whole-profile or selected closed sketch-curve sections, append/replace/remove/clear, Constant or Multisection mode, and Transformed/Right corner/Round corner transition type. Constant retains additional sections for later Multisection use. Allow empty startup and ordered profile/path/section preselection.

**D2843 — Needs owner confirmation:** Pipe Dimensions collects the sweep path as a whole curve object or selected edges from one local object, with pick/remove/clear controls and section reordering. Path geometry and section placements define length and direction; extrusion lengths and offsets do not apply. Advanced retains Standard/Fixed/Frenet/Auxiliary/Binormal orientation, a separate auxiliary-path collector, curvilinear equivalence, binormal XYZ, native Subtraction/Common, Refine and Fuzzy tolerance. Preserve inactive options and stored tangent flags; native tangent expansion and Linear/S-shape/Interpolation scaling laws are not implemented. The inherited Pipe engine requires closed sections and cannot accept point-ended sections; report this clearly. Preserve native orientation and corner semantics.

**D2844 — Needs owner confirmation:** Pipe Preview retains Recompute on change enabled, None/Overlay/Result, and default Overlay colors blue/green/red for New Body/Add/Subtract. Cancel restores visibility. Preserve native associative profile/path links, component operation and result identities, downstream references, undo/redo and save/reopen through edits and Boolean type changes. Reject invalid, stale or cyclic inputs and ineffective Booleans atomically; protect expressions.

### Shared selection, preview, deletion and compact layout

**D2853 — Needs owner confirmation:** Deleting an Extrude must preserve its source sketch, remove unused internal profile helpers and make the sketch available again when no other operation consumes it. Both edge and region selection must support creating another Extrude. Delete, Undo and Redo retain geometry and visibility consistently; shared inputs remain protected.

**D2854 — Needs owner confirmation:** Compact Tasks panels: component Extrude, Revolve, Loft, Pipe, Helix, Primitive and Sketch/Datum Plane forms must remain usable in a narrow panel. Use vertical scrolling when the controls exceed the available height; do not require horizontal scrolling. Labels wrap above fields when space is limited. Long object names and attachment descriptions must not force the panel wider; dropdowns and curve lists retain full text in tooltips. Arrange vector components vertically, group collection buttons in short rows, and retain usable reference entry fields with Pick/Clear below them. Preserve all field values, native units, section defaults and create/edit/preview behavior.

**D2855 — Needs owner confirmation:** Narrow-panel acceptance covers a 360 logical-pixel Tasks dock with all applicable sections expanded, two-sided Extrude and custom direction, Primitive Wedge dimensions and attachment, and Sketch axis directions. Every displayed field must remain horizontally within the viewport and reachable by vertical scrolling. Retain the native task scroller and OK/Cancel controls.

**D2859 — Needs owner confirmation:** Component operation entry: starting Extrude or another component operation automatically displays the active component's History tab as its creation task opens. This applies to the shared Sketch, Extrude, Revolve, Loft, Pipe, Helix and Primitive workflows, including entry from Models or Part Tree. If the Components panel is hidden, reveal it. Preserve profile preselection, the active component and occurrence context, and return to the original component view on OK or Cancel. History editing continues to use the same task.

**D2860 — Needs owner confirmation:** Curve-list interaction: in every shared component modeling curve collector, highlight and scroll to the most recently picked curve in the task list. Picking a collected curve again removes it and leaves no row highlighted. Give the curve list keyboard focus after a viewport pick so Delete removes its highlighted entries immediately; Delete with no highlighted entries does nothing and never deletes the source sketch. Apply the same behavior to Extrude, Revolve, Helix, Loft and Pipe profile curves and Pipe sweep/auxiliary path edges. Remove the redundant Add selected curves, Add selected and Use selected capture buttons; retain automatic collection, preselection, Remove, Clear, Use all/Use whole and the explicit Pipe path-role picker. Region picking continues to collect the complete boundary and highlights its last collected entry. Keep persistent viewport emphasis for the remaining collected curves, preview validation and OK/Cancel restoration.

**D2862 — Needs owner confirmation:** Modeling preview types: Extrude, Revolve, Loft, Pipe, Helix and Primitive use a dropdown with None, Overlay (default) and Result. Automatic updates remain enabled by default. Once the required closed profile and other geometric inputs are complete, Overlay shows the full native tool in blue for New Body, green for Add or red for Subtract. Add/Subtract overlays do not require a target or Boolean intersection and are not clipped to the target: a 5-inch subtract extrusion remains 5 inches long through a 1-inch body. Reference-defined extents still require their geometric references. Result shows the evaluated final geometry in normal body appearance without operation colors; it requires valid targets and a valid result. None removes the preview. Switching types, failed previews and Cancel restore prior visibility and transparency; collected curves retain their task highlights. OK continues to validate the actual operation and preserve native geometry, undo and persistence.

### Layers details

**D2872 — Needs owner confirmation:** Design Layers: Each document has permanent Base and exactly one active layer, initially Base. Base cannot be renamed or deleted. Origin and origin features always belong to Base. New independent model objects take the active layer; missing or foreign assignments in an existing document migrate to Base. Layer IDs, labels, visibility, active choice and assignments are native saved properties, with undo/redo. Layer metadata has NoRecompute semantics and introduces no document dependency links.

**D2873 — Needs owner confirmation:** Design Layers: A sketch is indivisible and remains independent of every body that consumes it, including a sketch nested in a native Body. A Body and its building operations share a layer. Native Body membership and explicit Plus Producer/ConsumedResults relationships define the body unit; arbitrary dependency recursion is forbidden. Selecting several operations of one body resolves to one assignment owner. Sketch selection moves only that sketch. New operations inherit their existing body's layer. Same-document occurrences resolve the shared definition's model objects; external definitions are edited in their owning document, not implicitly reparented.

**D2875 — Needs owner confirmation:** Design Layers: The task panel creates, renames, deletes, assigns and activates layers. Double-click a layer to activate it; active text is bold with a check. An eye control toggles each row's visibility. Layer hiding gates scene geometry without changing individual Visibility properties or taking snapshots. Hidden intermediate results remain hidden, individual changes while hidden are respected, and independently layered sketches remain traversable in the Body's native Group display. Native container Visibility and native Through/Tip display choices continue to govern their own scene traversal. Delete moves assignments to Base, never deletes geometry, and activates Base when the deleted layer was active. Changes are individually undoable from the task panel.

### Movement details and historical constraints

**D2881 — Needs owner confirmation:** Move Components: Move Components opens one Tasks panel from Design Assembly or the Part Tree instance context menu. It moves whole linked component instances and their descendants. Models, permanent master/root contexts and geometry subelements are not movable instances. Copy remains a separate Part Tree operation. The first field is Workflow, ordered Translate, Rotate, Point to Point, Align Axes, Align Coordinate Systems, Interactive.

The permanent-master wording is superseded by C09’s pinned file container and ordinary Part001.

**D2882 — Needs owner confirmation:** Move Components: The next control is the Components list, using the existing add-selection, Remove/Delete and Clear collector conventions. The first valid batch establishes the immediate parent definition and its exact displayed occurrence path as the active editing context. Only direct siblings under that same displayed parent are accepted; mixed batches are rejected in full with inline explanation. Descendants are implicit and receive no second placement change. Clearing the list retains the parent context. Ordinary component clicks outside the task do not activate parents. External parent definitions must be opened in their owning file.

**D2883 — Needs owner confirmation:** Move Components: A parent definition owns its children's relative LinkPlacement values. Moving children changes them in every occurrence of that parent, including its standalone component tab. Preserve the selected parent occurrence path for reference conversion; do not create a display-path placement override, reparent links, copy definitions or change source shapes/history. The task displays this shared-parent consequence. Driven, read-only, grounded and relationship-owned instances are refused, including native assembly joint references that traverse a root plus a deep subpath.

**D2884 — Needs owner confirmation:** Move Components: Translate uses one normalized direction, one nonnegative unit-aware Distance and a Reverse toggle, initially direction unset, zero length and Reverse off. Directions are Parent X, Parent Y, Parent Z or a picked straight edge, line/reference axis from visible geometry. Picked occurrence/world vectors transform by the inverse parent rotation only; parent translation does not affect a direction. Reject curved, undefined, zero or ambiguous bare shared references. Snapshot the direction without adding associative dependencies. All selected siblings receive the same parent-frame rigid transform. Reverse changes sign while retaining Distance.

**D2885 — Needs owner confirmation:** Move Components: Teal, non-pickable geometry previews intended placements without writing document properties or creating document objects/undo records. Show the effects in every displayed occurrence of the shared parent, using each occurrence's native frame. Apply commits all siblings in one transaction and keeps the panel open. It resets Direction, Distance and Reverse; Persistent Selection on retains the list/highlights, off clears both. No-op Apply creates no undo record. OK applies a valid nonzero pending move and closes; after Apply it simply closes. Cancel discards only the pending preview, retaining earlier Apply transactions for Undo. Switching workflows discards uncommitted parameters/preview while retaining siblings and parent context.

**D2886 — Needs owner confirmation:** Move Components: Errors remain inline in the task. A changed parent or selected placement invalidates the pending preview and requires Reset movement inputs; stale placements are never silently applied. Selection changes and removals reset movement inputs. Close the task and release observers/preview on document or component-view exit; deleted instances leave the list, and deletion of the parent context closes the task.

**D2887 — Needs owner confirmation:** Move Components: Rotate uses Parent X/Y/Z through the parent origin, a picked straight line with its location and direction, or two distinct points. An optional picked pivot relocates a parallel axis. Vertex, native sketch/reference point, origin and analytic circle center picks retain their displayed occurrence transforms. Angle is a finite magnitude from 0 to 360 degrees; positive follows the right-hand rule and Reverse negates it. Rotate applies one common rigid delta to sibling positions and orientations. The transient preview labels the parent-frame pivot, positive axis and signed angle. Apply clears axis, pivot and angle and turns Reverse off.

**D2888 — Needs owner confirmation:** Move Components: Point to Point snapshots a Source and Destination vertex, sketch/reference point, origin or analytic circle center from any visible displayed occurrence. The Source need not belong to the moved group. Convert both to the active parent frame and translate every sibling by Destination minus Source, preserving orientations, group spacing and descendants. Show labeled points and distance with transient markers/vector; no joints, constraints or lasting references are created. Coincident points create no undo entry. Missing, invalid or deleted references prevent Apply. Apply clears both point inputs; selection follows Persistent. Reset/method switch/Cancel remove pending preview.

**D2889 — Needs owner confirmation:** Move Components: Align Axes snapshots Source and Target straight/reference axes, analytic circular axes or cylindrical-face axes through exact displayed occurrences. Default Make Coincident uses minimal-angle rotation and maps the Source anchor to its closest point on the Target axis; Make Parallel rotates about and retains the Source anchor. Reverse Target Direction explicitly negates Target. Opposite directions use Source cross the least-aligned parent X/Y/Z basis, with X winning ties, for a stable 180-degree rotation. Show resolved Source/Target direction arrows and transformed Source; all siblings receive one rigid parent-frame delta. Apply clears picks and restores Coincident/Reverse-off defaults. No joints, associations or arbitrary axial slide.

**D2890 — Needs owner confirmation:** Move Components: Align Coordinate Systems maps a complete Source rigid frame to a complete Target frame, including origin and roll, with one Target times inverse Source delta shared by siblings. Pick existing native component origins/datums, explicitly choose Parent, or expand Origin/Z/X definitions. Normalize Z, project X perpendicular to Z and derive right-handed Y. Reject zero/parallel directions and scaled, sheared, reflected or nonfinite frames. Show Source/Target triads and origins, without exposing matrices. Picks snapshot displayed occurrences against unchanged geometry; Apply clears definitions and references, and Cancel removes only pending preview.

### Legacy conversion interactions

**D2899 — Needs owner confirmation:** When a legacy file opens, Models lists its part definitions and Part Tree shows linked instances beneath the pinned file row. Repeated instances reference the same model. Review legacy conversion explains incomplete mappings, missing instances and any geometry-only recovery. Label recovered outputs as recovered geometry and explain that their parametric history has not been converted. Missing instances remain visible for repair. Save converted external parts as new .cadprt files before the parent, leaving legacy originals untouched. For supported simple Sketch and Pad histories, History lists the sketch, Pad operation and original Body result in that order, preserving their labels. Double-click the sketch to edit its constraints or Pad to open the Extrude task. Repeated instances update from the shared model. Review legacy conversion identifies histories that remain native and editable. Retained expressions use the property editor; operation and target changes reject downstream self-references and preserve the original feature identity. Legacy datum planes, axes, points and coordinate systems retain their labels and native attachment settings. Body-owned datums appear as hidden links in component History. Double-click opens the original attachment editor; Cancel preserves supports and offsets. Retained planes are available to New Sketch and follow their native offsets and frame changes. Missing or invalid datum sources show Needs repair. Origins and their planes keep their existing names and permanent controls. Retained Body-owned sketches appear as hidden links before their Body in History. Double-click edits the original sketch and its existing constraints; all consumers and repeated instances use that same sketch. Existing attachments, external references and expression-driven dimensions remain editable in their native controls. Missing or invalid sketch sources show Needs repair; repair the original input before using it.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2900 — Needs owner confirmation:** Supported legacy Pad and Pocket chains appear in History as independent sketches and Extrude operations with explicit target bodies, ending in the original Body result. Double-click a converted Pocket opens the shared Extrude task with Subtract, its existing target and the correct direction selected. Accept updates the operation; Cancel leaves its saved parameters and target unchanged. Existing expression-driven parameters remain available in the property editor. Converted Pad/Pocket modes and targets can be edited while keeping the original feature. Standalone native Part Extrusion retains New Body; create a separate operation to change its operation kind. Retained native Pad/Pocket histories appear as hidden History links; double-click opens the original native editor with its attachments and extent references intact. Missing or invalid retained operation sources show Needs repair. Supported independent Part Extrusions also open in the shared task; custom direction, taper and sheet or curve outputs retain their native controls.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2901 — Needs owner confirmation:** Supported legacy Revolution and Groove histories show their original sketches, Revolve operations, target bodies and final Body in History. Double-click opens the shared Revolve task with saved axes, angles, direction and signed start offset. Accept updates the operation; Cancel preserves saved settings. Preview follows rotated sketches and construction axes. Converted features retain their native Revolution or Groove type; create a separate operation to switch additive/subtractive type. Formulas remain editable in properties. Attached or reference-dependent histories and standalone Part Revolution retain their native editors and signed-axis controls. Missing or invalid retained sources show Needs repair. Review legacy conversion distinguishes mapped operations from retained native histories. Undo/Redo restores conversion and edits without stale component views.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2902 — Needs owner confirmation:** Supported legacy Lofts show their original section sketches before Loft operations, explicit target bodies and the final Body in History. Double-click opens the shared Loft task with sections in their saved order and existing Smooth/Ruled, Closed, Refine and tolerance settings. Preview section reorder or replacement before Accept; Cancel preserves saved sections and targets. Converted Loft modes and targets can change while keeping the original Loft. Vertex end sections retain their picks. Formula-driven settings use properties. Attached histories, native Common operations and legacy sketch-edge references that mean the whole sketch retain the original native editor. Standalone Part Loft retains its native degree, linearization and solid/sheet controls. Missing or invalid retained sources show Needs repair. Undo/Redo restores conversion and edits; repeated instances update from the shared model.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2903 — Needs owner confirmation:** Supported legacy Pipes show their original profile sections and path sketches before Pipe operations, explicit target bodies and the final Body in History. Double-click opens the shared Pipe task with saved section order, path and auxiliary edge picks, orientation, corner transition and Constant/Multisection settings. Preview changes before Accept; Cancel preserves saved references and targets. Converted Pipe modes and targets can change while keeping the original feature. Formula-driven settings use properties. Attached or unsupported histories, native Common operations and whole-sketch edge references retain the original native editor. Standalone Part Sweep retains its native solid/sheet, Frenet and linearization controls. Missing or invalid retained sources show Needs repair; unavailable selected path edges give a repair message. Review legacy conversion identifies stale outputs requiring recompute. Undo/Redo restores conversion and edits; repeated instances update from their shared model.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2904 — Needs owner confirmation:** Supported legacy Helix histories show original profiles before Helix operations, explicit targets and the final Body in History. Double-click opens the shared Helix task with saved parameter mode, pitch, height, turns, cone angle or growth, axis, handedness and direction. Preview changes before Accept; Cancel preserves saved settings and references. Converted modes and targets retain the original Helix feature. Formula-driven parameters remain editable in properties. Attached or unsupported axes and histories retain their native editors and available geometry. Standalone Part Helix retains its native curve controls. Review legacy conversion identifies unverified output requiring recompute; missing retained sources show Needs repair. Undo/Redo restores conversion and edits; repeated instances update from the shared model.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2905 — Needs owner confirmation:** Supported legacy Box, Cylinder, Sphere, Cone, Ellipsoid, Torus, Prism and Wedge histories show Primitive operations with explicit targets and the final Body in History. Double-click opens the shared Primitive task with the saved shape, native dimensions and placement. Preview changes before Accept; Cancel preserves saved settings. Converted Add/Subtract/New Body modes and targets retain the original primitive; create a separate operation to change its shape type. Formula-driven dimensions use properties. Attached or unsupported histories retain the original native editor. Standalone Part primitives retain their native controls. Review legacy conversion identifies stale or unavailable output; missing retained sources show Needs repair. Undo/Redo restores conversion and edits; shared instances update together.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2906 — Needs owner confirmation:** Legacy Fillet, Chamfer, Draft and Thickness operations appear in component History while retaining their native Body and selected faces or edges. Double-click opens the original native editor with saved settings. Standalone Part dress-ups retain their original controls and outputs. Missing or invalid retained sources show Needs repair; Review legacy conversion identifies unverified output requiring recompute.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.

**D2907 — Needs owner confirmation:** Legacy patterns and transformations appear in History with referenced inputs before consumers, retaining authored order where compatible. Double-click opens the native editor with saved originals, direction or axis references and transformation settings. MultiTransform preserves its ordered transformations; combined Pattern retains both Linear and Circular settings and suppressed copies. Boolean History opens the original native editor with its saved operation, target and tool Bodies. Native owners and geometry remain retained; these operations are not presented as newly flattened shared operations. Undo/Redo restores conversion and edits; saved files preserve the original model shared by repeated instances.

Backend Body rows described in this historical conversion passage are superseded by the owner’s current background-Body requirement; the remaining conversion UI details still need confirmation.


### File Open and legacy conversion

**D2908 — Needs owner confirmation:** Open legacy FCStd files through File > Open. Models contains definitions, Part Tree contains linked instances, and History shows inputs, operations and finished results. Mapped operations use the shared task; retained operations open their original native editor. Save converted content to a new cadprt file, saving external definitions before their parent. Legacy originals remain protected. Missing definitions remain visible; right-click and choose Locate Component File to repair them before saving. Review legacy conversion identifies retained native histories, unverified caches and explicit dumb geometry recovery. Geometry-only recovery preserves available output while reporting loss of parametric component editing. Repeated instances share model edits; instance placements remain independent. Conversion and geometry-only recovery both add the pinned file row, with its global Origin, above the converted domestic component. Recovered outputs belong to that component; the file has no modeling geometry. The file row is excluded from Models. One Undo reverses the entire conversion, including the file container, and Redo restores it. No additional Part001 is created.

Any exposed backend Body rows in historical conversion descriptions are superseded by the current background-Body requirement.

## Older Markdown-only workflows — Needs owner confirmation

The former [UI specification](archive/2026-10-10/UI_UX_SPEC.md) retains detailed custom dialogs for Trim Body, Isocline, CAM/STL machining and holding tabs, named parameters, command search, temporary display, export, sketch support, dependency inspection, measurement, occurrence appearance, interference, sketch repair, Mirror, section planes, feature organization, Make Unique, drawing setup, document updates, mesh preparation, reusable sketches, BOM, Shape Builder, source replacement, face deviation, Select Other, thickening, CAM templates/simulation, exploded views, intersection curves, freedom guidance, dimension repair, joints, ordered Loft sections, CAM model review, state columns, Sweep, project packaging, Hole, selection filters, fillet/chamfer recovery, Trim gestures, Shell and face extension. These are preserved **only as archived candidates**; no accessible original owner message confirms their detailed custom UI. Native upstream workflows remain the baseline unless a confirmed owner requirement above changes them.

The removed [component-contract UI passages](archive/2026-10-10/superseded-passages/ai-instructions/architecture/COMPONENT_DOCUMENT_CONTRACT.md) similarly preserve proposed instance grouping, deletion/reparenting, context menus, Add Reference Object, missing-file repair and dumb conversion details. Use them to ask targeted confirmation questions, never to infer approval from implementation.
