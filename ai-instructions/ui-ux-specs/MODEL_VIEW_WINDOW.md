# Model view window

Status: owner-intent specification, reconstructed 2026-10-10. **Only the confirmed requirements are authoritative.** Material headed **Needs owner confirmation** is preserved for review and must not be treated as an approved change. The current application, agent-written specifications and implementation reports do not establish owner approval. Newer explicit owner decisions supersede older decisions on the same subject. See [evidence and unresolved decisions](EVIDENCE_AND_DECISIONS.md).

## Confirmed requirements

### Startup and workspace stability

Show recent files in the main viewing area at startup and New File/Open in Tasks. Initialize the chosen interface and theme without displaying a sequence of old/different interfaces. Tasks is docked on the right by default. Restore the user's customized panel and toolbar positions on later startups. [C06](EVIDENCE_AND_DECISIONS.md#c06)

The owner reports a jittery interface on October 10. Smooth, stable interaction is a requirement to assess; the cause has not been diagnosed by this documentation task. Preserve this fork as reference if a clean reimplementation is later chosen; no restart or code migration has been authorized by that discussion. [Current owner direction](EVIDENCE_AND_DECISIONS.md#current)

### Component editing display

While editing one occurrence, keep its geometry and descendants at their authored appearance. Fade all other visible geometry, including other occurrences of the same definition, to **at least 75% transparency**, preserving greater existing transparency. Restore normal appearance when the context changes. Active styling in the tree does not imply every occurrence remains opaque. When editing the file, show all components at normal transparency. [C09](EVIDENCE_AND_DECISIONS.md#c09), [C10](EVIDENCE_AND_DECISIONS.md#c10)

Editing an unused model temporarily hides the existing assembly and shows that model. Visibility controls must not override the temporary hiding. Restore the previous visibility on exit; do not save this temporary state. Part Type and Reference eligibility follow [Component Panel](COMPONENT_PANEL.md#part-type-and-visibility). [C09](EVIDENCE_AND_DECISIONS.md#c09)

### Selection behavior

The Design Selection toolbar's categories and controls are in [Toolbars and Buttons](TOOLBARS_AND_BUTTONS.md#selection-toolbar). Apply curve intent to drawing curves and body edges. Connected/Tangent traversal must not cross independent sketches or bodies merely because they overlap on screen. Command input filters still apply. [R03](EVIDENCE_AND_DECISIONS.md#r03)

Directional Selection on: left-to-right requires full enclosure; right-to-left also selects intersected geometry. Off: both directions require full enclosure. Enclosure and crossing boxes must look different. [R03](EVIDENCE_AND_DECISIONS.md#r03)

Persistent Selection retains surviving selected entities after operations, allowing Equal followed by Construction without reselection. Deleted items leave the selection; failures preserve usable inputs. Escape and an ordinary empty-space click clear selection even with persistence on. Persistence must not turn plain clicks into additive selection. In Sketcher, a plain click selects only the clicked item; Ctrl/Shift permits multiple selection. A plain empty click clears selection; modified empty clicks preserve native multiselection behavior. [R03](EVIDENCE_AND_DECISIONS.md#r03), [C06](EVIDENCE_AND_DECISIONS.md#c06)

When selecting an origin plane for New Sketch, highlight only that plane, not the entire Origin and all three planes. [C06](EVIDENCE_AND_DECISIONS.md#c06)

### Contextual Constraint Palette

A geometry click during sketch editing opens the palette for the **whole current selection**. Further clicks update it. Box selection alone does not open it. Prefer above the pointer, repositioning to keep the entire palette within the viewport. Keep its position stable during updates unless viewport bounds require adjustment. [R03](EVIDENCE_AND_DECISIONS.md#r03)

Keep it visible indefinitely while the pointer is inside the palette or a small travel corridor from the click. Leaving starts a **one-second** grace period; reentry cancels dismissal. This replaces the earlier five-second proposal. Dismissing by pointer travel leaves selection intact. [R03](EVIDENCE_AND_DECISIONS.md#r03)

Use native toolbar **icons and the same hover tooltips**, including on disabled actions. Remove the lingering tooltip/shadow when an action is chosen or the palette closes. Show only applicable constraints, Construction Geometry and separate Make Driving/Make Reference actions; hide inapplicable actions and disable known conflicting/redundant ones with an explanation. Merely selecting geometry or assessing unapplied constraints must not emit solver errors or alter the sketch. Actual committed operations retain diagnostics. [R03](EVIDENCE_AND_DECISIONS.md#r03), [C06](EVIDENCE_AND_DECISIONS.md#c06)

For a mixed normal/construction selection, the first toggle makes all normal and the next makes all construction. Uniform selections toggle together. Make Driving and Make Reference operate on multiple dimensions as one undoable action. Explicit exception: a Make Driving operation that produces an invalid sketch remains committed with its error so the user can Undo or repair it. [R03](EVIDENCE_AND_DECISIONS.md#r03)

With Persistent Selection on, successful actions keep selection and update the palette in place. Off clears selection and closes it after success. Escape/empty click clear and close it; sketch exit, deletion and document/task transitions clean it up. Uncommitted failures preserve selection. [R03](EVIDENCE_AND_DECISIONS.md#r03)

### Movement feedback

The placement preview, arrows, translation-plane handles, rings, numeric entry and Edit Pivot interaction belong to the shared [Move Components task](TASK_PANEL.md#move-components). Releasing a drag leaves a preview; Apply/OK commits it. Editing the pivot alone does not move geometry. This is distinct from the still-deferred feature handles for editing modeling dimensions. [R03 and adopted movement prompts](EVIDENCE_AND_DECISIONS.md#r03)

## Transferred DOCX requirements — Needs owner confirmation

The following source candidates are not instructions to implement. Exact values, added restrictions and implementation-derived details need owner confirmation. D numbers identify the archived DOCX paragraphs; [the coverage record](archive/2026-10-10/docx-coverage.json) accounts for every source block. Confirmed rules above override conflicting candidate wording. Implementation reports remain archival only.

### Startup content

**D2795 — Needs owner confirmation:** Show native recent-file cards in the viewing window at startup, without New File option cards or example files. An empty list shows No recent files. New File and Open remain visible in Tasks. Prepare the selected theme, toolbar style and restored workspace before exposing the main window; do not cycle through workbenches after it appears. Home loads only its required native command modules. Explicit theme and Plus/Classic choices persist.

### Initial left-panel arrangement

**D2797 — Needs owner confirmation:** Show Components above Attributes at the left with approximately a two-thirds/one-third height split.

### Status controls

**D2802 — Needs owner confirmation:** Keep the notification/status control, navigation-style selector and units selector present and functional.

### Sketch shading and collector emphasis

**D2852 — Needs owner confirmation:** October 3 ribbon and sketch feedback: the ribbon background must match surrounding panels in the active theme. Leaving sketch edit displays unfilled curves. During component Extrude region collection, closed sketch areas use translucent light blue, distinct from solid shading. An interior click can choose a sketch without first selecting it in the Profile field and collects all boundary curves, including holes, in Selected curves. Turning region picking off or closing the task removes its temporary fill. Retain individual edge selection, green/red volume previews and the shared profile collectors in Revolve, Loft, Pipe and Helix.

**D2858 — Needs owner confirmation:** Curve-selection feedback: throughout component Extrude, Revolve, Helix, Loft and Pipe tasks, collected curves stay highlighted in the selection color, including while editing an existing operation, changing fields or showing a solid preview. After the first curve is collected, other sketches show light-medium gray curves and no area shading. Keep light-blue region shading only on the active sketch when region picking is enabled. Loft retains highlights for all collected sections; Pipe includes its profile, sweep path and active auxiliary path. Changing collectors updates the emphasis. Clearing every collected input restores normal sketch colors and candidate region shading. OK and Cancel remove all temporary emphasis and restore prior display state. Do not persist temporary colors or create document geometry for highlighting. Preserve native edge and interior-region picking, validation and geometry semantics;

### Selection implementation choices

**D2867 — Needs owner confirmation:** Selection categories: Surfaces are sheets not associated with bodies; Faces and Edges belong to bodies. Curves are drawing items, including sketch curves and standalone three-dimensional curves such as isoclines. Points include sketch points, reference points and origins; Vertices are body corners. A sketch remains drawing geometry even when owned by or used to construct a body. Preserve full occurrence paths. A sheet boundary remains in the Surface category; solid result objects are selectable Bodies even when their native type is not PartDesign Body.

**D2868 — Needs owner confirmation:** Curve intent: Connected Curves follows endpoint connections within the picked sketch or shape, including every branch and closed multi-edge loop, without crossing separate objects. Tangent Curves follows endpoint-connected tangents and stops at branches or tangent discontinuities. Use 0.0000001 mm endpoint tolerance and 0.00001 radian tangent-angle tolerance, independent of zoom. A closed periodic curve remains one item; its parameter seam does not connect it to other curves. Sketch construction geometry retains its native geometry indices. Feature collectors retain ownership of their reference-picking behavior.

### Palette details

**D2876 — Needs owner confirmation:** Contextual Constraint Palette: Only a click while editing a sketch in Plus Design mode opens the palette. Use the entire native selection, including additional selection clicks; box or programmatic selection alone never opens it. Place above the click where possible, otherwise below or clamp within the viewport. Use logical pixels for DPI scaling. Keep a 24-pixel-wide travel corridor to the actual palette rectangle, with a 12-pixel anchor allowance and a 4-pixel palette margin. Remain visible indefinitely inside; outside starts a one-second grace timer and reentry cancels it. New clicks restart the travel context. Action updates retain position unless viewport clamping requires movement. Dismissal by pointer travel leaves selection intact. Choosing an action removes its native tooltip frame immediately, before solving. Refresh and close hide retired controls immediately; native icons, hover text and the one-second pointer-travel grace remain unchanged.

**D2877 — Needs owner confirmation:** Contextual Constraint Palette: The palette contains only applicable native constraints/dimensions, Construction Geometry and separate Make Driving/Make Reference actions. Display icon-only buttons using each corresponding native toolbar action icon and the exact native hover tooltip, including translated descriptions and shortcuts. Follow native icon and tooltip changes. Retain separate accessible names and the existing batch behavior for Make Driving and Make Reference. Structurally inapplicable actions are absent. Existing constraints and known conflicts/redundancies remain disabled. Show the unchanged native tooltip on disabled buttons too; show the palette-specific reason in the status bar on hover and retain it as the accessible description. A cloned native Sketch solver diagnoses additions without changing committed geometry, constraints or the live solver. Nonconvergence alone is unknown feasibility and does not disable an action. No hover action adds constraints. Revalidate the live sketch and full selection before execution; native dimension dialogs retain their normal units and command safeguards.

**D2878 — Needs owner confirmation:** Contextual Constraint Palette: Mixed construction selections become all normal, then all construction. Uniform selections toggle together. Dimension states are separate from construction flags. Dimension conversion validates all inputs, applies one native batch and solves once, as one undoable change. Preserve constraint order, names, identities, values and expressions. Making an expression-driven dimension reference is disabled because native conversion would remove its expression; the user must explicitly remove that expression first. Native external-only driving restrictions remain in force.

### Sketch selection and diagnostic correction

**D2897 — Needs owner confirmation:** October 6 sketch-edit selection correction: in Plus Design, a plain point/edge/constraint click replaces the selected item; a repeated plain click retains that item. Ctrl or Shift permits native multi-selection. A plain empty-space click clears selection, while Ctrl/Shift empty clicks retain it. Persistent Selection controls retention after operations and must not turn plain clicks into multi-selection. Dragging, box selection, context-menu picks and Classic native behavior retain their own semantics. Palette feasibility checks use cloned solver data and must not report errors or warnings for unapplied hypothetical constraints. Quiet handling belongs only to that probe; actual modeling/constraint operations retain native diagnostics and Undo behavior. Both defects reproduce on the preceding delivered build: two plain point clicks accumulate selection, and the hypothetical coincidence of a line's endpoints repeatedly reports failed solvers and geometry errors.


### Inherited viewport and task cleanup

**D2909 — Needs owner confirmation:** Inherited interface requirements: the TechDraw face-color preference explains that it affects projected faces; existing saved colors remain respected. The Start Page must not leave an overlay dock covering its content, and overlay menu colors follow the active theme. Sketch editing preserves the saved non-edit toolbar layout. Closing a document removes its task dialog and any attachment or feature-picker callbacks.
