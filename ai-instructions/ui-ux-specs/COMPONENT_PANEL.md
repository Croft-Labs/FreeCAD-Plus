# Component panel

## Opening and activation camera stability — corrected November 27, 2026

Ordinary component activation preserves the current camera. Opening an additional
isolated component view fits its geometry in one transition. Opening a Plus file
restores its saved camera without a second automatic zoom. A new camera operation
supersedes an older animation; normal navigation animation preferences remain in
effect. Screen-sized coordinate graphics do not drive fit bounds, but retain
their visibility, rendering and picking behavior. See
[verification](../evidence/camera-transitions-20261127/README.md).

## History modeling operation display — approved November 27, 2026

Modeling feature icons use **yellow for both New and Add**, and **red for Subtract**.
This owner correction supersedes the earlier blue/green/red proposal. Retain the
recognizable tool glyph, shading and outlines; keep normal row text color.
Append the saved operation as a display-only suffix: `extrude001 (new body)`,
`extrude002 (add)`, `extrude003 (subtract)`. New sheets use `(new surface)`.

Apply to Plus Extrude, Revolve, Loft and Thicken and explicitly supported native
modeling equivalents. Classify native additive features using their preceding
solid, not their name. Refresh when operation/output or custom label changes.
Do not alter stored Label/Name, source icons, toolbar icons or reference identities.
Coordinates, sketches and features without a supported operation retain their
presentation. History editing, selection, eyes, menus and reorder retain their
existing behavior. See [delivery evidence](../evidence/history-operations-20261127/README.md).

## Assembly visibility eyes and row text — approved November 27, 2026

The active assembly root has no visibility eye and remains visible. Its Hidden
and Excluded actions are unavailable in Components menus. Choosing an assembly
that was previously hidden temporarily exposes its route without rewriting its
saved visibility setting.

Children have an inline eye after the native expand/collapse triangle and before
the component icon. The eye follows tree indentation; only assemblies have branch
triangles. Condensed instance groups use a mixed state when needed and toggle all
members in one Undo transaction. Excluded instances must change Part Type before
they can be shown. Eye clicks preserve selection, Edit context and tree expansion.
Nested/imported children update their actual defining parent's file. Visibility
uses the existing saved display metadata, including its shared-definition scope.

Children displayed under an isolated/unplaced assembly use normal text rather than
the grey reserved for file occurrences outside the edited definition.
See [delivery evidence](../evidence/assembly-selection-20261127/README.md).

## Active part on opening a one-part file — November 27, 2026

Opening a file with exactly one local component definition makes that component
the active Edit part and populates its History. Use its sole occurrence when
unambiguous; an unplaced definition or a repeated definition opens in definition
isolation without adding an occurrence or arbitrarily choosing a placement.
Imported catalogs and feature/Body objects do not count as extra local parts.

Apply this initialization to normal opening, recovered-file opening and the
Parts sub-file menu's Open file in new window. Hidden imports do not change the
host's active part. Preserve the current Components tab, native document data,
Undo and active-assembly rules. Do not reapply the default on refresh or override
an explicit file-level Edit in an already-open view. Multi-part files retain their
current opening behavior; saved active-part restoration is a separate pending item.
See [correction evidence](../evidence/single-part-open-20261127/README.md).

## Reference image History — approved November 27, 2026

Reference images belong to the active component's History, including when that
component is edited through an imported-file occurrence. Double-click or Edit
reference image opens the same populated task used for creation. The context menu
offers Edit reference image, Hide/Show, and Delete. Visibility and deletion use
native Undo in the defining file. Plane dependencies participate in History order.
See the [reference image workflow](TASK_PANEL.md#reference-image--approved-november-27-2026).

## History Appearance — approved November 27, 2026

History's part header retains Rename and adds Appearance. Its right-click action
preserves the bodies/faces selected before the click; an empty selection stays empty.
Geometric feature rows offer Appearance with exactly that feature preselected,
including older Body features. Do not substitute the current Body tip. Sketches,
origins and coordinate groups without editable surface/mesh geometry have no such
action. Opening Appearance does not change visibility, active component/assembly,
the selected Components tab or document Undo state.

The owner approved companion `f336305f1145` with “approved. implement the history
appearance menu and the face highlighting correction”. The reviewed fingerprint
was `a8aa6bf2633e54f4940909a0c4f73313872a6f994870ca30cf04deb893ce938b`.
Direct screenshots were approved in chat; companion approval state was not edited.
See [delivery evidence](../evidence/history-appearance-20261127/README.md).

## Assembly edit modes and default assembly — approved November 27, 2026

Parts and Assembly component menus offer **Edit within assembly** and **Edit in
isolation**. Within assembly preserves surrounding components and the exact chosen
occurrence; isolation shows the selected component and its descendants. Within
assembly is disabled for components outside the fixed active assembly. Double-click
on an assembly member uses within-assembly editing. Condensed groups edit their
representative occurrence without expanding or acquiring disclosure arrows.
Unplaced and imported assembly anchors preserve their native child coordinate frame.
A loaded, unimported assembly is edited in its defining file without importing it.

With no valid saved/manual assembly choice, a file containing exactly one local
component definition automatically uses it as its active assembly. Bodies, native
feature history and imported catalogs do not count as additional local components.
Valid saved/manual choices win; empty/stale cached choices are reconsidered. The
existing file bookmark persists this choice on save. Edit context, selected tab,
tree expansion, model visibility and Undo remain independent of assembly navigation.

These approved rules replace the earlier generic Edit menu item and supersede the
historical pending-preview statements below.

## Appearance and Parts context menu — November 27, 2026

Owner approved implementation of the reviewed Appearance task workflow. Component
rows in Parts use these groups, with separators before, between, and after them:

1. Edit; Make active assembly; Add to active component; Open in new window; Rename.
2. Appearance; Part Type; Visibility.
3. Import; Export.

Appearance opens the shared task described in TASK_PANEL.md. Right-clicking the
component preserves eligible faces previously selected in the viewport. Part Type
and Visibility retain their existing ownership restrictions and are disabled when
the current edit context cannot change them. Other tree menus retain their behavior.

The separately previewed navigation/tab retention and saved active-assembly changes
are not included in this appearance implementation approval.

## Imported meshes in History — November 26, 2026

Owner clarification: a mesh imported into a part is an item in that part's History.
File > Import and Mesh > Import Mesh must attach native mesh features to the active
edited component, including child and externally defined components. Keep mesh
data intact; importing a mesh does not create a component definition or occurrence.
Parts, Assembly and History must remain available after import. Undo/Redo includes
ownership, and cancellation or a failed reader must not leave orphan objects.
Use the existing History row, native mesh icon, selection and visibility behavior.
See [bug repair and verification](../evidence/mesh-import-20261126/README.md).

## Component terminology — owner clarification, November 25, 2026

**Component** is the general entity. A component can serve as a **part**, an
**assembly**, or **both**. A part provides modeled geometry; an assembly contains
child components. A component may contain both its own geometry and child
components, although combining these roles is not recommended. Mixed components
remain supported.

The owner clarified that the terminology may have been reversed in the November 24
discussion. Use this definition when interpreting those messages and in future
project guidance. Existing approved behavior and UI labels remain in effect.
See [the owner statement](EVIDENCE_AND_DECISIONS.md#component-terminology--november-25-2026).

## Classic and Plus file formats — November 25, 2026

The owner selected icon option **B**: a green plus with white outline over the
lower-right of the existing FreeCAD artwork. FreeCAD Plus and `.cadprt` share this
icon, including file/catalog rows and the desktop shortcut. Classic `.FCStd` keeps
its existing association and icon. The November 26 refinement adds the matching
white outer border; see the [current icon specification](TOOLBARS_AND_BUTTONS.md#freecad-plus-application-and-file-icon--november-26-2026).

The owner approved implementation with "implement file extensions and conversions".
**FreeCAD Plus document** uses `.cadprt`; **FreeCAD Classic document** uses `.FCStd`.
Format follows document content, independently of Classic/Plus presentation mode.
Open and Plus Import default to a combined **FreeCAD documents (*.cadprt *.FCStd)**
filter, so both types are visible together. The component import/Add existing source
chooser uses the same combined default. Separate format filters and other geometry
importers remain available. Save,
Save As, Save Copy, Save All and save-on-close use the document's native extension.
A mismatched native suffix is corrected for a new filename; ordinary Save cannot
overwrite a mismatched-format filename. Extension preferences cannot disable this
distinction.

Opening Classic offers **Convert and open**, **Open Classic**, or Cancel. Conversion
chooses a separate new `.cadprt`, preserves supported editable content, and leaves
the original `.FCStd` unchanged. It reads the saved source rather than unsaved live
edits. Existing destinations are not replaced. Unsupported structures show an
explicit error; do not silently flatten them into dumb geometry. Open Classic
remains available for ordinary native editing/saving.

Parts import offers both types, with **Convert and import** for Classic. Add
Component > Add existing > Open file offers **Convert and select parts**. Conversion
alone does not place children or change Edit/active assembly. Component export
remains independent editable `.cadprt` output only. Previously mislabelled Plus
content in `.FCStd` offers **Save .cadprt copy**; repair preserves the original,
uses a new document identity, and retains external links even in another directory.
Owner correction November 25: conversion/repair dialogs use the ordinary pointer
while waiting for a choice, including destination browsing. Busy starts only when
the user accepts conversion or **Save .cadprt copy**, and ends on completion or
error. Cancel and errors must leave no lingering busy cursor.
See [approval and acceptance evidence](../evidence/file-formats-20261125/README.md).

## Clone from direct children — November 25, 2026

Owner refinement: **only whole objects** can be cloned. Default result labels are
lowercase `cloned body`, `cloned surface`, `cloned sketch`, `cloned plane`, according
to geometry type. Do not reuse the child's source label as the result's default.
These geometry labels do not create or rename component definitions.

To obtain a face from child geometry, clone the whole body first, then use the
separate **Extract geometry** operation in the parent. A selected face becomes an
`extracted surface`; the cloned body remains. There is no face/edge/vertex Clone
mode and no implicit extraction during Clone. Source history remains in the child.

The owner renewed **“implement the clone and extract geometry workflow”** after
these native proposals. Modeling > Other contains **Clone** and **Extract geometry**.
Clone uses one whole-object collector and a direct-child occurrence browser. Extract
uses a face collector on parent-owned geometry. Both use the same form for creation
and History editing; editing replaces one result's source in place. Source/result
columns, Remove/Delete/Clear, click-add/Shift-click-remove and preview controls follow
the shared collector pattern. Cancel leaves the model and Undo history unchanged;
OK creates the selected results in one owning-file Undo step.

Reference children may supply Clone inputs; Excluded children cannot supply new
inputs. Saved clones retain their association even if display choices later change.
Source edits and the chosen occurrence's placement update the parent result. A missing
or replaced source produces an explicit repair error, never label-based reassignment.
Default duplicate result names receive a numeric suffix. Recompute on update controls
the temporary preview; saved results remain associative. Extract creates one separate
`extracted surface` per selected face; edge/point extraction is outside this workflow.
See [implementation and native checks](../evidence/clone-extract-20261125/README.md).

The owner specifies one operation named **Clone**, without separate single-element
and whole-part modes. While editing a parent component, the user may choose
geometric objects (sketches, bodies, sheets and other geometry) owned by a **direct
child**. Do not traverse another component boundary: geometry owned by a child's
child is ineligible, even if visible in the parent view. Native feature/body
containers within the direct child are not themselves additional component levels.
Choose the source through its child occurrence so repeated instances retain the
correct placement relative to the parent. Selecting a component must not silently
flatten its descendant geometry.

Clone creates native, history-free geometry owned by the edited parent. The child's
source geometry and all its defining sketches, constraints and modeling operations
remain with the child; do not copy or relocate that construction history into the
parent. A sketch clone supplies its geometric result, not the child's driving
dimensions/constraint history. The parent's History records Clone and subsequent
parent-owned operations.

Parent feature operations may modify the cloned result and incorporate a cloned
body into another parent body, for example through Boolean or other applicable
modeling features. Clone alone does not merge bodies. Do not achieve this by
reparenting the original child body, moving the child's history, or directly editing
the child's definition from the parent. Downstream parent operations affect the
parent's result; editing the source child remains a separate shared-definition edit.

This is the newly specified workflow for the earlier **Add Reference Feature**
promotion prerequisite. That earlier name and undefined-task wording below are
superseded by **Clone** for this component workflow. The prerequisite of an explicit
parent-owned feature remains: ordinary parent modeling must not silently create a
clone or consume unpromoted Reference geometry. This does not rename unrelated
upstream Draft, Sketcher, PartDesign or BIM commands without a separate UI decision.

The earlier contract requires an owned, derived, linked result. Retain that source
association unless the owner explicitly requests a detached snapshot; "dumb"
geometry here means no transferred construction history. Source geometry and
child-placement changes recompute Clone in the
parent frame, then recompute parent operations; parent operations never write back
to the child. Missing sources or invalid downstream results must be reported, not
silently converted into detached geometry. The renewed implementation instruction
authorizes the prepared controls and these associative semantics.

## Shared instances and names — November 25, 2026

The owner clarified that a part name must be unique in an assembly: `part2`
denotes the same shared definition in every occurrence, including occurrences
in other assemblies and linked imports into another file. Editing its definition
edits that part wherever referenced. Occurrence placement is independent of
definition geometry. Naming uniqueness applies to distinct definitions; repeated
instances of the same definition retain the same name.

This supersedes the older rule below wherever it allowed distinct definitions
with equal names from different files to coexist in an assembly merely by showing
a filename qualifier. November 25 implementation enforces uniqueness across the
open file's full component catalog, including unused and transitively imported
definitions. Comparison ignores case and surrounding whitespace and normalizes
Unicode. Repeated instances/import paths of one identity remain valid. Loaded
reverse importers also constrain source edits; unrelated open files do not.
Use persistent definition identity for links, not display-name matching. Do not
silently merge unrelated source definitions because their names happen to match.
Conflicting imports and renames identify both files and require a source Rename
before retrying. No automatic source renaming. Older conflicting files remain
navigable for repair, but cannot be saved until conflicts are resolved. Undo and
restore remain intact; restored conflicts must be repaired before saving.
Independent export currently creates detached copies;
it must not be described as a shared linked import or globally synchronized edit.
Closed dependent files see saved source changes when reopened/refreshed; this
requirement does not imply rewriting every closed file at edit time.

The reiterated tree convention is retained: domestic definitions show `part_3`;
external definitions show `part_4 (file_name_A)`. Each nested row identifies its
actual defining file, including `part_7 (file_name_B)` and `part_8 (file_name_C)`
inside an imported subassembly. Suffixes identify origin, not a separate name
namespace. Closed importers are checked on reopening rather than rewritten when
their source changes. See [implementation evidence](../evidence/component-names-20261125/README.md).

The owner also asked about condensed/expanded instances, adding more instances,
and removing one instance without deleting the part. Source audit at
`e9297f7b4572540481d810f8bd997be25bb166e6` found:

- Assembly projection emits one row per native link, using the definition label.
  There is no repeated-instance grouping toggle or numbered occurrence label.
- Add Component > Add existing can add the same definition again; Assembly
  Copy/Paste creates more links. The existing picker has no quantity control.
- The custom Assembly menu has no explicit Remove instance action. Native Delete
  fallback is not verified as a safe occurrence-only workflow.
- Each link has its own placement; its linked definition is shared. Linked imports
  preserve the source definition. Export parts to file creates independent copies.

November 25: the owner's renewed **implement Condensed/expanded instances** request
authorizes the [prepared native layout](../evidence/instance-display-proposal-20261125/README.md).
The Assembly tab's Instances selector defaults to Expanded and remembers the user's
choice across files and restarts. Group repeated sibling links by definition
identity beneath their immediate parent, never by matching labels. Condensed
shows `part2 ×3`; Expanded shows `part2 (1)`, `part2 (2)`, `part2 (3)`. Numbers are
display ordinals, not persistent occurrence identifiers or definition renames.
Singletons retain their names; imported labels retain their source filename.
The November 27 corrections below supersede the original expandable collectors:
condensed groups remain folded without disclosure arrows. Use Expand instances
to restore original occurrence rows and their own constraint collectors. Groups
retain the complete context menu and have no visibility eye.
Switching modes preserves exact selection and existing subtree folds; selecting a
hidden occurrence keeps its group condensed until explicitly expanded. No definitions, placements, Edit/active
assembly state, or Undo entries change. Keep individual instances reachable for
placement, constraint and visibility actions. See
[implementation and verification](../evidence/instance-display-20261125/README.md).

Quantity creation and the separate Remove instance workflow are implemented below.
Remove instance must remove selected links only, preserve the shared
definition and other links, and handle dependent constraints explicitly in one
Undo operation. A condensed group must not ambiguously delete every instance.
Definition deletion remains a separate action. Editing the contents of a shared
subassembly (including removing its child link) changes every occurrence of that
subassembly; a unique variant is needed to change just one copy's contents.

## Remove individual instances — approved November 25, 2026

Owner also requested Remove individual instances. Its separate
[native review proposal](../evidence/instance-removal-proposal-20261125/README.md)
was authorized by the owner’s renewed implementation request: right-click one Assembly occurrence, Remove
instance, review parent/instance/remaining count, then remove the link in one Undo
step. The component definition and other links remain. Explicitly include listed
dependent constraints or leave removal disabled; unsupported references block
with actionable feedback. Cancel is the default.

Removing a child inside a shared parent changes that parent's assembly contents
everywhere, so acknowledge that scope explicitly. Removing a whole subassembly
occurrence preserves its definition and children. Protect active root/Edit ancestry,
collectors and definition rows; do not treat condensed groups as remove-all.
Assembly Delete uses this same scoped review and consumes Delete for ineligible
roots/groups/multiple selections, without native definition-deletion fallback.
Hidden, Reference and Excluded instances are eligible. Pattern-controlled members
defer to Edit instance pattern. Revalidate document/view, Edit/assembly context,
owning file, exact link identity, sibling counts and dependency details at acceptance.
Unsupported geometry, expression, loaded external references or dependents of listed
constraints block removal. Preserve selection outside the removed route and prevent
solver-driven motion during this transaction. Implemented and installed; see
[acceptance](../evidence/instance-removal-20261125/README.md).

## Instance quantities and patterns — approved November 25, 2026

Owner requested creation of several instances at once, including patterns.
The [native workflow proposal](../evidence/instance-quantity-proposal-20261125/README.md)
was authorized by the owner’s renewed implementation instruction. Add existing keeps its navigator, then opens
Create instances with Quantity, Linear, Grid or Circular arrangement. Add new
creates one shared definition and the requested instances; New Component remains
the separate definition-creation command. Counts are per selected definition,
include the first new placement, and exclude existing links.

Quantity places independent links at the entered parent-relative position.
Patterns expose spacing/directions or center/axis/radius/angle/orientation, show
the total and preview, and save editable parameters in the destination component.
Edit instance pattern reopens the same controls. Preserve surviving link identities
and explicitly block removal of referenced members. One Undo step, unchanged Cancel,
recursive nesting guards and the fixed active assembly are required. Pattern members
cannot be moved or newly constrained independently; use Edit instance pattern.
Directions can use parent axes or native straight-edge/axis references; Linear also
accepts a typed vector. The operation supports at most 10,000 new links total.
Implemented and installed; see [acceptance](../evidence/instance-quantity-20261125/README.md).
Condensed/expanded display and name enforcement were delivered separately;
Remove instance is implemented in its separate workflow above.

## Fixed active assembly — November 25, 2026

The owner reiterated that the active assembly automatically becomes the locked
component and that every child is positioned relative to its immediate parent.
The active assembly supplies the fixed global frame for that assembly context;
it cannot be moved by Move Components while it is the active root. No child needs
to be grounded merely to establish that frame. Selecting a different active
assembly must not rewrite saved child placements or ground another child.
An assembly can still be positioned as a child within a different parent assembly.
Edit context and active assembly remain separate choices.

The owner approved implementation of the reviewed [Move Components](TASK_PANEL.md#move-components)
workflow on November 25. Assembly has a compact Move Components button beside its
selector, and child occurrence context menus offer the same task. Implementation
and native verification are tracked in [delivery evidence](../evidence/move-components-20261125/README.md).

## Responsive tab widths — November 25, 2026

Owner-approved native preview: Parts, Assembly and History shrink together with
the panel, using a common minimum that fits the longest label in normal and bold
selected states, with only native text-edge spacing. Their common maximum remains
the existing padded width. Keep the tabs left aligned and do not stretch beyond
that maximum. Native scroll arrows are needed only below the combined text-fit
minimum. This refines the earlier equal-width/padding approval; it does not change
tab labels, heights, styling, navigation or component workflows.

The owner approved the wide/medium/minimum screenshots with **"approved. implement"**.
See [native sizing and delivery evidence](../evidence/responsive-tabs-20261125/README.md).

## Transfer sets of parts — November 25, 2026

The owner renewed the previously cancelled import/export request and approved the
native dialog screenshots with **"approved. implement"**. This approval supersedes
the earlier cancellation for this scope.

**Add Component > Add existing** keeps its always-open dropdown and adds **Open
file…** plus checkboxes for multiple parts. Current-file parts appear directly;
other loaded `.cadprt` files are collapsed groups with eligible-part selection.
Component counts and blocked self/ancestor rows remain. Add the selected parts as
linked children at the edited component's origin in one Undo operation, including
necessary catalog imports. Preserve Edit, active assembly, source identities and
the separate Add new/New Component behavior. Opening a source alone places nothing;
Cancel closes only unused files opened by this chooser. Both files must already be
saved for external linking; never save a source implicitly.

In **Parts**, select one or more part rows and right-click **Export parts to file…**.
The dialog reviews the selected parts and component counts, then chooses a new
`.cadprt` filename. Export independent editable definitions with their complete child
graphs, history, expressions, display/reference states and assembly constraints.
Copy shared child definitions once; distinct definitions with conflicting labels
receive unique destination labels. Place each explicitly selected definition once
in the output file, using its local component frame. Source files and placements
remain unchanged, as do the current Edit and active-assembly contexts.

Do not replace an existing output file or append into one. Validate and finish the
new native archive before publishing it; remove temporary output on failure. Export
must have no remaining source-file dependencies. File > Import for `.cadprt` uses
the existing catalog-only import service; geometry-only File > Export is unchanged.

See [approval, implementation and runtime evidence](../evidence/part-transfer-20261125/README.md).

## Assembly constraints and padded tabs — November 25, 2026

Every part with assembly constraints has an **Assembly constraints** collector as
its first child in Assembly, before its component instances. This applies at every
nesting level and to every occurrence of a shared subassembly. Each collector lists
only its owning part's constraints. It appears when the first constraint is added,
starts collapsed, retains the user's expansion through refresh, and disappears when
the last constraint is deleted. Constraint rows support double-click/Edit and Delete.

The selected active assembly supplies the global reference frame for its assembly
operations. Its origin and own geometry remain fixed; no child must be anchored to
begin. Subassemblies retain their own local frames and constraints. Choosing another
active assembly changes navigation/operation context without rewriting stored
placements or changing the independently edited component. This supersedes older
wording that made the internal file container the user's assembly reference frame.

Parts, Assembly and History have equal widths with extra horizontal label padding.
The tab group is left aligned and does not stretch to fill the panel. Preserve native
tab height, styling, navigation and scrolling when the panel becomes narrow.

Owner approved the collector preview, clarified that every constrained subcomponent
needs its own collector, and then said **"approved, implement"**. The additional tab
preview was separately approved with **"Approve this tab layout"**. On November 25
the owner cancelled the separate file import/export request and directed continuation
of constraints. See [approval, native screenshots and verification](../evidence/assembly-constraints-20261125/README.md).

## Add Component — November 24, 2026

Owner-approved: **Add Component** in the Plus Assembly tools always opens a dropdown
with **Add existing** and **Add new**, including clicks on the main icon. It never
repeats the last choice. Add existing opens the part navigator with component counts,
current defining-file parts and collapsed groups for other loaded component files.
Add new opens a separate name/create dialog. There are no mode tabs in these dialogs.

Both paths target the active (edited) component. The November 26 contract below
adds assembly containment confirmation and the Parts context-menu entry.
Keep that parent in Edit. New Assembly is removed from the Plus Assembly
tools; the active-assembly selector remains. Standalone **New Component** retains
its existing definition-only creation and activation behavior, without placement.
Add new creates a definition and a child instance together; it is a different action.

Block self-reference and any direct/indirect parent-child cycle, including through
Reference/Excluded links, and block circular file dependencies. Recheck context and
eligibility at acceptance. Cancel and validation failures leave the graph unchanged.
Undo removes an entire addition, including its new definition or required catalog
import. Loaded external sources retain their defining-file identity; required files
must be saved before importing, without implicit saves.

Approved in chat: "Approved. Implement" after the revised always-open dropdown and
explicit distinction from New Component. See
[preview and native evidence](../evidence/add-component-20261124/README.md).

## Active-component additions and placement display — November 26, 2026

Owner approved the revised direct screenshots with “all approved. implement”.
Assembly Add existing/Add new always target the active component, including the
top level or a child of the active assembly. Parts > Add to active component… uses
the selected part definitions as sources and opens the existing instance task.
Selection does not change the destination. Multiple selected parts share one Undo.

If the active component is outside the active assembly, offer **Make active assembly
and add** or **Cancel**. Cancel is the default and changes nothing. Acceptance makes
the active component the assembly root, retains Edit, and continues adding. Nested
membership follows shared component definitions, including external children;
adding to a shared parent affects its occurrences as before. Keep cycle, saved-file,
identity, transaction and stale-context protections.

During placement, follow the current native draw style and update when the style
buttons are clicked. Preserve source colors. Normally opaque faces are 50%
transparent; retain greater source transparency. Do not change saved source
materials, visibility or geometry. Preview toggling and Cancel remove only the
temporary scene. The subsequently approved [Hidden line correction](TOOLBARS_AND_BUTTONS.md#save-all-and-hidden-line--approved-november-26-2026)
removes the native triangulation artifact, which also affected ordinary geometry.

See [implementation and verification](../evidence/placement-workflow-20261126/README.md).

## Active assembly — November 24, 2026

Owner-approved revised preview: the visible tabs are **Parts**, **Assembly** and
**History**. Assembly has a button showing the current assembly and opening its
selector. Right-click a definition in Parts and choose **Make active assembly**
to make that part the sole top-level Assembly row. Its children are component
instances. The file name is no longer an assembly or pinned tree root.

The selector lists all domestic parts from the current file directly, with a
**Components** count beside each. Other loaded component files are expandable
groups, collapsed by default, containing all their parts and counts. Counts include
every nested instance, including repeats and hidden components, excluding Reference
and Excluded branches. Select a part and press **Make active assembly**; Cancel
preserves the choice. Do not add count sorting or a default-assembly setting.

Assembly selection and component Edit are separate. Double-clicking a component
edits it and shows History without changing the selected assembly. Unused parts
remain in Parts and can be selected as assemblies; editing them does not append
temporary rows to Assembly. The approved History component heading and Rename
remain unchanged. This supersedes the older file-root and temporary-unused-row
requirements below. It does not change stored membership, placement or geometry.

Approved in chat: "Approved" after the revised selector preview. See
[preview and implementation evidence](../evidence/active-assembly-20261124/README.md).

## Active component in History — November 24, 2026

Owner-approved: show the active component as History's first row, above Coordinate
System. In this tab only, its native icon and name start at the far left, above the
history items' visibility eyes. Use the existing active bold/highlight treatment.
The component row has no visibility eye and cannot be hidden or reordered here.
Right-click anywhere on that row, including its far-left icon, to Rename using
the existing shared-definition dialog. Renaming updates all instances, supports
Undo/Redo and save/reopen, and retains the current component/occurrence context.
Cancel and invalid names retain the previous name. File-only History has no
component heading. Feature eyes/editing and coordinate graphics retain their
existing behavior. The active-assembly update above subsequently renames the other tabs.

Approved in chat: "Approved implement and also make sure that the user is able to
right click the part row and rename it" following the requested left alignment.
[Preview identity, direct screenshots and implementation evidence](../evidence/history-component-20261124/README.md).

## New component navigation — November 23, 2026

Owner approved that creating a component activates the new part and selects
Components > History. See [approved preview and implementation scope](../evidence/new-component-preview-20261123/README.md).
Creation ownership and instance counts retain their existing contracts.

Owner correction: after activating the newly created component and opening History,
clear all selection. The component stays active for editing; Coordinate System and
other rows must not remain selected. This permits the approved idle geometry tasks
to appear. Apply to New File, New Component and creation in an empty file; do not
clear subsequent user selections with a delayed callback.

Status: owner-intent specification, reconstructed 2026-10-10. **Only the confirmed requirements are authoritative.** Material headed **Needs owner confirmation** is preserved for review and must not be treated as an approved change. The current application, agent-written specifications and implementation reports do not establish owner approval. Newer explicit owner decisions supersede older decisions on the same subject. See [evidence and unresolved decisions](EVIDENCE_AND_DECISIONS.md).

Implementation planning and acceptance are owned by the [Group 1 roadmap](../DEVELOPMENT_ROADMAP.md#group-1--component-panel-and-document-structure) and [component contract](../ARCHITECTURE.md). The G1.6a opt-in panel foundation and preceding hierarchy/external-definition services do not establish completion of this panel or approve any deferred UI detail. Domestic and external unused-model editing have bounded native-build validation. Component file tabs have bounded development-build acceptance recorded in WORK_STATE. Linked-instance Copy/Paste is a separate increment tracked there and in the [clipboard contract](../ARCHITECTURE.md#linked-instance-clipboard-g16c2); its selected-parent destination/local-placement convention is an announced implementation choice, not a recovered owner decision. Move Components foundation/Translate is implemented with acceptance tracked in WORK_STATE and the [movement contract](../ARCHITECTURE.md#move-components-foundation-and-translate-g16c3). Rotate extends that shared task with its [located-axis/pivot contract](../ARCHITECTURE.md#rotate-g16c4); acceptance is recorded in WORK_STATE. The November 25 approved workflow adds the remaining movement methods; pending panel actions stay in Group 1. Implementation boundaries and remaining unused-model/action work are recorded in the linked roadmap and contract. Import/storage/copy services are available to the later panel; their existence does not establish a finished Add Component dialog or placement-selection checklist. Conversion support and its tested boundaries are recorded in the component contract; the legacy-file requirements below remain the intended full behavior.

## Scope boundary: panel behavior and launched operations

Owner-approved November 22, 2026: an Extrude target chosen from History remains
displayed as a selected solid even while its eye is off. The temporary task display
does not change the eye's persistent visibility intent. Eyes remain usable and
source-owned. See [Extrude target display and colors](TASK_PANEL.md#extrude-selected-targets-and-validity-colors--november-22-2026).

Owner-approved November 22, 2026: entering native sketch drawing/editing hides
the component Coordinate System temporarily. History eyes reflect this display
and remain usable. Exit restores saved visibility except for explicit eye choices,
which retain native task transactions. Plane-selection visibility and Sketcher's
own drawing axes remain available. See
[sketch coordinate visibility](TASK_PANEL.md#sketch-coordinate-system-visibility--november-22-2026).

Owner-approved November 22, 2026: entering part-feature creation/edit temporarily
selects History. Finishing or cancelling restores the tab selected before the task,
including Models, Part Tree or History. New Sketch placement-to-drawing is one
continuous task. Users may browse tabs during it; refreshes must not force History
again. Scope restoration to the originating panel/view and clean up abandoned or
closed tasks. This temporary behavior does not replace component Edit navigation.
See [feature-task interaction requirements](TASK_PANEL.md#sketch-dimensions-and-feature-task-history--november-22-2026).

The owner clarified that an operation is not Component Panel implementation merely
because it is conveniently offered by right-click. This panel owns its tabs, tree
and History presentation, component/document structure, selection/Edit context,
component windows, structural instance actions and appropriate menu access.
The behavior of Move Components (including Point to Point) belongs to
[TASK_PANEL.md](TASK_PANEL.md#move-components). Panel acceptance checks that the
entry opens the intended task with the correct selection/context; it does not require
implementing every workflow in that task. Operation completion is not a Group 1 gate.

## Confirmed requirements

### History drag ordering and corrected invalid moves — November 23, 2026

The fundamental Coordinate System must always be first; its native subtree is fixed.
All defining inputs precede their consumers, directly and transitively. For example,
a custom datum plane precedes the sketch placed on it, and that sketch precedes its
Extrude/Revolve. Allow feature rows to be clicked and dragged into valid order.

If an input is dropped after a dependent, move it immediately before its first
dependent in History, then display a popup stating that it cannot be moved after
that dependent. Name the moved feature and blocking dependent, and explain the
corrected position. Conversely, a dependent cannot move before its required inputs;
place it after the latest required predecessor and explain the correction. A valid
independent move needs no popup. Preserve unaffected row order, visibility controls,
selection/edit behavior and native geometry/reference identity.

Owner approved implementation together with Plane/Sketch placement. Installed History
supports one feature per drag, dependency-safe correction and the naming popup.
The preferred order persists with the source component and supports Undo/Redo and
save/reopen; it does not rewrite native feature links or ownership. Reordering requires
finishing any active feature task/transaction. Stale or cross-context drags are rejected.
This does not approve every archived drag/reorder behavior. See
[implementation evidence](../evidence/plane-history-20261123/README.md), including the
documented limitation of OS mouse verification in this session.

### Strict sequential feature History — November 22, 2026

Owner decision: sketches remain predecessors of the Extrude/Revolve or other feature
that uses them, and must never be reorderable after a consuming feature. Modeling is
strictly sequential. History must express feature/input sequence across backend Body
containers; flattening each Body ahead of later component sketches is incorrect.
Apply the same predecessor rule to other feature inputs. New features follow their
inputs; editing must not introduce forward or cyclic dependencies. Any eventual
reordering must preserve direct and transitive predecessor/dependent order.

This confirms the dependency restriction, not every interaction in the historical
D2864 reordering proposal. The November 23 decision above now authorizes and
implements single-feature History drag reordering within these constraints.
The owner approved the [native ordering preview](../evidence/sequential-history-preview-20261122/README.md)
and implementation with "approved, implement strict sequential history and prevent
sketches or other inputs from being ordered after the features that use them".
Source/build/install acceptance lives in WORK_STATE.

### Persistent base coordinate system — November 23, 2026

The owner approved protecting the base coordinate system created with every part.
Its Coordinate System, native Origin point, axes and planes cannot be deleted
individually, including through History. Visibility controls remain usable. Keep
the existing native objects and identities; do not replace them after deletion.
Normal deletion of the owning component, Undo/Redo and cancellation still work.
User-created datum geometry remains deletable. Existing saved component files
receive the same protection without migration.

See [implementation evidence](../evidence/target-coordinate-20261123/README.md).

### History coordinate icons and initial expansion — November 22, 2026

Owner request: Axes and Planes groups use the same native icons as their respective
children, replacing folder icons. Coordinate System and its descendants start collapsed.
Apply the collapse default when creating their History rows; ordinary refreshes retain
the user's later expand/collapse choices. Preserve visibility eyes, geometry visibility,
labels, source ownership and the other tabs. The owner approved the direct native
[preview](../evidence/history-icons-preview-20261122/README.md) with "implement".
Installed acceptance is recorded in
[WORK_STATE](../WORK_STATE.md#history-coordinate-icons-and-collapsed-defaults--november-22-2026).

### Component, definition and instance

A component serves as both a part and an assembly: it can contain its own sketches, operations/features and other geometry, and linked instances of child components. Models holds definitions; Part Tree holds placed instances. Repeated instances share their definition. Core Bodies are background implementation objects, not objects the user must create, activate or manage independently. The user works with sketches, operations/features and geometry. [Current owner direction](EVIDENCE_AND_DECISIONS.md#current)

### File root and new files

New File creates a domestic **Part001** definition, places one instance beneath the file, and enters Edit for Part001. Part001 is an ordinary component that may be renamed, removed or deleted. An empty file is valid. The November 24 active-assembly decision supersedes C09's pinned filename row: the selected part is now the Assembly root. The native file container remains internal. [C09](EVIDENCE_AND_DECISIONS.md#c09)

The file owns a fixed Origin and three origin planes defining global coordinates. Its History shows only these, with visibility controls. File-level assembly relationships and placement controls are managed in Part Tree. Sketches, features and modeling geometry must belong to a component. Starting a modeling command while editing the file requires the user to explicitly edit or create a component; do not silently choose one. Existing files gain the file container without another Part001 or changes to existing names, geometry, placements or references. [C09](EVIDENCE_AND_DECISIONS.md#c09)

### Models tab and storage

List domestic definitions first, followed by expandable imported-file groups containing all definitions from each file. Include nested imported files: the later multi-level requirement replaces the earlier single-level outline. Importing a file populates Models; it does not place the entire file in Part Tree. Unused definitions remain available. [C09](EVIDENCE_AND_DECISIONS.md#c09)

The Models **Import Models from File** action imports a saved component catalog
into the file owning the edited definition, including while editing an external
component. It keeps the editing tab/context and creates no placed instances.
The menu placement and label are implementation choices for C09's confirmed
import behavior, not a recovered exact owner layout. The chooser states the target
file. See the [import contract](../ARCHITECTURE.md#models-file-import-g16c6).

**New Part creates a definition without placing an instance.** Placement in Part
Tree remains a separate action. The November 23 owner update now activates the new
definition for editing and selects History automatically, superseding the former
requirement to preserve the previous editing context after creation.

New Component allows storage in the current defining file, a new external file, or an existing external file such as Hardware. Use **domestic** and **external** terminology. The historical C09 rule allowed equal names in different files as distinct definitions, qualified as **M3 screw (Hardware)**. The [November 25 shared-name clarification](#shared-instances-and-names--november-25-2026) supersedes that allowance within an assembly. Filename qualifiers may communicate source, but cannot resolve a conflicting part identity. Do not silently substitute a domestic definition for an external one with the same name. [C09](EVIDENCE_AND_DECISIONS.md#c09)

Editing an external definition edits and saves its defining file. Other files using it receive the saved change when reopened. Child components must come from the active definition's own file or from files imported into that defining file. An external Hardware component cannot simply acquire a component from the importing assembly's domestic list. Edit Hardware and import the required file there first. Immediately flag and block circular file references and circular component nesting. [C09](EVIDENCE_AND_DECISIONS.md#c09)

Copying between domestic and external storage creates an independent definition; it is not an identity-preserving move. When copying an external definition to domestic storage, prompt the user to choose placements to replace with the new copy. The original external definition remains independently usable. Exact checklist defaults and cancellation behavior have not been confirmed by the accessible owner messages. [C09](EVIDENCE_AND_DECISIONS.md#c09)

### Edit, selection and component tabs

Use **Edit** as the UI term for making a component active. Double-click or context-menu Edit in Models or Part Tree edits the chosen component in the **current file tab** and shows its History. A single click selects only, including on the file row. Double-click activation must work reliably. [C09](EVIDENCE_AND_DECISIONS.md#c09), [C10](EVIDENCE_AND_DECISIONS.md#c10)

Show the active definition in bold with the configured active-item fill color in Models and on **all its Part Tree occurrences**. Keep a separate selection indicator on the occurrence used to enter Edit. Editing a definition from Models reuses its last edited occurrence in that tab, otherwise its first occurrence in Part Tree. [C09](EVIDENCE_AND_DECISIONS.md#c09)

**Open in new window**, offered by right-click in both tabs, opens a new file tab for the component. Ordinary Edit must not open that tab automatically. Viewport context display is specified once in [Model View Window](MODEL_VIEW_WINDOW.md#component-editing-display). [C09](EVIDENCE_AND_DECISIONS.md#c09)

### Editing an unused model

The November 24 active-assembly decision supersedes C09's temporary unused-model
tree entry. Editing an unused definition retains the selected Assembly root and
shows the edited part in Parts and History. Existing isolated viewport editing
and display restoration remain. Saving retains definition edits, not temporary
display state. An unused definition becomes the Assembly root only when selected
as the active assembly. [C09](EVIDENCE_AND_DECISIONS.md#c09)

### Part Type and visibility

Implementation boundary: G1.7a adds saved self/direct-child state and contextual
menu controls/tooltips in the opt-in development panel; see the
[saved-state contract](../ARCHITECTURE.md#saved-part-type-and-visibility-state-g17a).
G1.7b1 adds explicit view-local Hidden/Excluded and nested Reference filtering and
restoration; see the [view-local contract](../ARCHITECTURE.md#view-local-explicit-hiding-g17b1).
G1.7b2 contextual fading is validated in the development payload, including shared
mixed face materials; Model View Window and WORK_STATE state its acceptance boundary.
G1.7b3a applies saved self/child visibility and nested Reference choices in domestic
and external unused previews; its validation is recorded in WORK_STATE. G1.7b3b
Bodies Only content filtering is validated in placed and unused development views;
see the [technical contract](../ARCHITECTURE.md#bodies-only-content-filtering-g17b3b).
G1.7b3c adds the shared eligibility guard and applies it to existing Move Components
reference reads; navigation/Edit remain available. The [technical contract](../ARCHITECTURE.md#geometry-eligibility-g17b3c)
states the boundary. G1.7b3d adds the native File > Export preflight: a selection
containing unpromoted Reference/Excluded geometry is rejected before exporter options
or writing. Mixed aggregates are refused rather than silently rewritten. This bounded
integration does not establish filtering for every export format or modeling command;
see the [export contract](../ARCHITECTURE.md#native-export-eligibility-g17b3d). G1.7b3m preserves
the original assembly occurrence when exporting a placed external member; the
[source-context contract](../ARCHITECTURE.md#placed-external-export-context-g17b3m)
records the integration boundary. This does not change the export workflow.
G1.7b3e adds native PartDesign profile and Sketcher Projection/Intersection intake
checks. G1.7b3f extends the same rules to native attachment and the shared picked
axis/direction/plane collector; [Task Panel](TASK_PANEL.md#shared-task-patterns)
records these integration boundaries, including G1.7b3g's separate attachment editor
and Extrude face/shape inputs, G1.7b3h's Loft/Pipe input admission and G1.7b3i's
shared dress-up/transformed input checks, followed by G1.7b3j command-start admission. Full Reference-use enforcement remains pending. The descendant interpretation is recorded
in the [Part Type source recheck](EVIDENCE_AND_DECISIONS.md#part-type-source-recheck---october-11-2026).
Saved metadata alone does not establish the full behavior below. WORK_STATE owns validation.

Use **Part Type**, replacing Part View. The types are **Full Component**, **Bodies Only**, **Reference**, and **Excluded**. Shown/Hidden is separate visibility state; Excluded is not another name for Hidden and cannot be overridden with Show. [C10](EVIDENCE_AND_DECISIONS.md#c10)

The active component defaults to Full Component; its direct children default to Bodies Only. Save overrides on the component for itself and its direct children, persist them through save/reopen, and restore them when that component is edited again. The parent's definition owns its child choices, so all instances of that parent share them. Do not substitute a global display preference or independent per-occurrence override. [C10](EVIDENCE_AND_DECISIONS.md#c10)

The owner's fan-assembly example retains ordinary nested component contents and
excludes reference copies according to context. For Bodies Only implementation,
interpret this as retaining eligible descendant bodies while respecting the saved
child types and exclusions, rather than discarding every nested component. This
descendant rule is inferred from the owner's example; see the
[source recheck](EVIDENCE_AND_DECISIONS.md#part-type-source-recheck---october-11-2026).

A direct Reference child displays its full geometry while its parent is edited, respecting its own nested exclusions. Editing an ancestor makes that reference behave as Excluded without erasing its saved Reference setting. Reactivating its owner restores Reference. To use an excluded nested component as a reference, add that component separately as a direct Reference child. [C10](EVIDENCE_AND_DECISIONS.md#c10)

**Clone is mandatory before reference-child geometry may be used.** Earlier C10 called this **Add Reference Feature**: an owned, derived and linked reference sketch/body/other feature in the active component. The [November 25 Clone clarification](#clone-from-direct-children--november-25-2026) supplies its current name, direct-child source restriction and history-free result contract. A cloned body becomes geometry of the parent component; unpromoted source geometry is not directly usable for modeling or as final component geometry. Displayed Reference geometry alone cannot be used as sketch/attachment inputs. The task's detailed controls and implementation remain pending. [C10](EVIDENCE_AND_DECISIONS.md#c10)

### History and legacy files

November 22, 2026 approved replacement: part History starts with **Coordinate
System**, containing **Origin** (the native point at component-local 0,0,0), an
**Axes** subgroup (X Axis, Y Axis, Z Axis), and a **Planes** subgroup (XY Plane,
XZ Plane, YZ Plane). Every group and individual item keeps a visibility eye fixed
at the far-left margin. A group eye hides all its members when all are visible;
otherwise it shows all. Mixed groups use an open eye with a horizontal pupil.
Individual toggles remain independent. New components start with the origin,
three axes and three planes visible; existing saved visibility is preserved.
This supersedes the older Origin hierarchy/defaults below. Approval was given
in chat for companion session `a738581b957c`, fingerprint
`c682681f99f6fe438156e200e5b7435db452b8554db97c9249f041c18443b832`.
See [implementation evidence](../WORK_STATE.md#coordinate-system-history--november-22-2026).

November 21, 2026 owner-approved History update: activating a part with double-click
or Edit in Models or Part Tree opens its History in the current file tab. History
starts with an expandable Origin containing X Axis, Y Axis, Z Axis, XY Plane,
XZ Plane and YZ Plane, including for empty components. Existing sketches and
features follow. Use these clean display labels without changing native identities.
Each part History row, including Origin and every child, has a visibility eye in
a fixed column at the far-left margin. Tree depth affects only the name/icon column;
eyes stay aligned when Origin expands/collapses or the dock is resized. Open eyes
mean shown; crossed eyes mean hidden. Clicking an eye toggles visibility without
selecting a different item or entering an editor. Tooltips identify Show/Hide and
the item; Space on a History item performs the same action. Visibility uses native
Origin/Body parent semantics and defining-file Undo/Redo/save. File-level History
retains its existing controls; coordinate graphics and initial visibility defaults
are unchanged.

November 22 correction, explicitly approved after native previews: entering sketch
editing must preserve the current shown/hidden state of other geometry, including
linked component rendering. Native support/dependent visibility automation must
not override History choices. See the
[correction contract](TASK_PANEL.md#extrude-rendering-and-sketch-visibility-correction--november-22-2026).

November 22 refinement, approved in chat: History eyes remain usable during New
Sketch placement and native sketch drawing. They preserve the selected support and
active editor. Automatic fundamental-plane reveal is temporary; explicit visibility
choices retain native persistence/Undo semantics. See the
[Sketch visibility contract](TASK_PANEL.md#sketch-planes-and-history-visibility-proposal--november-22-2026).

Approval: the owner said "approved. implement the history changes with the grouped
origin, axes and planes, and the visibility eyes fixed to the left margin." in this
chat on November 21. This approves the direct
[screenshot](../evidence/history-20261121/approved.png), companion session
`13924304d75b`, fingerprint
`5b74dd441f12f6e86c40dfdca5ff43072fd2a7c143584086364ec59349995841`.
The isolated panel snapshot matches source commit `2b42f56e03`; its snapshot commit
is `2aabfa2316a400c39c64b564a6c766286b5e01e7`. Approval was given directly in chat;
no companion approval state was changed on the owner's behalf. This supersedes
earlier flat-plane/right-eye previews and conflicting unconfirmed origin proposals
below. [WORK_STATE](../WORK_STATE.md#grouped-history-and-left-margin-visibility--november-21-2026)
records implementation and native acceptance separately.

Show the active component's sequential sketches, operations/features and other geometry. Background Bodies must not reappear as separately managed rows. A legacy conversion should retain editable features where possible, putting required sketches and producing operations before their results. Move definitions to Models and represent links as Part Tree instances. If a feature cannot be converted parametrically, preserve recoverable final geometry as explicitly identified dumb body/curve geometry rather than losing it. The current backend's conversion limits are not restrictions on the intended workflow. [C06](EVIDENCE_AND_DECISIONS.md#c06), [current owner direction](EVIDENCE_AND_DECISIONS.md#current)

Implementation boundary: G1.7b3k recognizes native Boolean-owned tools in the
component file and projects their features before the Boolean in History, keeping
backend Bodies hidden and retaining full selection/Edit paths. See the
[native ownership contract](../ARCHITECTURE.md#native-boolean-ownership-within-a-component-g17b3k).
G1.7b3n checks command/tool intake against the Reference/Excluded prerequisite;
[its contract](../ARCHITECTURE.md#boolean-input-admission-g17b3n) records that bounded
integration. This does not establish the unsettled handling of Boolean tools from
another Full Component. G1.7b3l extends legacy conversion to preserve these
editable native graphs in standalone Bodies and existing Part/shared-link structures;
its tested boundaries are in the [conversion contract](../ARCHITECTURE.md#legacy-boolean-tool-ownership-g17b3l).
This is preservation of authored content, not a new Boolean operation workflow.

The owner reaffirmed on October 11 that **all geometry from a Reference component
must first be added to the active component's History through Add Reference
Feature before it can be used in that component in any way**. This is a mandatory
prerequisite for every geometry consumer, including Boolean inputs; direct source
use or automatic reference creation does not satisfy it. See the
[latest owner clarification](EVIDENCE_AND_DECISIONS.md#reference-geometry-prerequisite---october-11-2026).

Part Boolean results and their inputs retain ownership in the edited definition;
the original source features remain in History. G1.7b3o implements this for its
supported local Part Boolean path; see the [ownership contract](../ARCHITECTURE.md#part-boolean-eligibility-and-ownership-g17b3o).
This preserves the existing component/feature model rather than treating native
Boolean dependencies as another component container.

### Context-menu requirements and deferred decisions

| Location | Confirmed action | Required behavior |
| --- | --- | --- |
| Models / Part Tree | Edit | Edit definition in the current tab; retain occurrence context. |
| Models / Part Tree | Open in new window | Open a component file tab. |
| Models / Part Tree | Rename | Rename the shared definition in its defining file; update all occurrences, retain identity and support Undo. Names remain unique across each affected file's complete imported catalog. |
| Part Tree | Copy / Paste | Create another linked instance for subsequent movement; do not embed Copy in Move Components. |
| Part Tree instance | Move Components | Open the shared task described in [Task Panel](TASK_PANEL.md#move-components). |
| Models / storage copy | Copy external to domestic | Independent definition; prompt for placements to replace. |

G1.6c5 offers Rename through these menus and the temporary unused row. This menu
placement is an implementation choice for the confirmed C09 rename permission;
its exact position was not recovered from owner messages. The dialog states that
all instances share the name. Cancellation and unchanged names make no edit.
See the [rename contract](../ARCHITECTURE.md#definition-rename-g16c5).

The November 24 Add Component approval above supersedes the former deferral of
that workflow. Catalog-only Import Models remains separate; Add Component may
register a required saved source catalog while placing the selected child in one
Undo transaction. The detailed delete/grounding/fixed-relationship menus, grouped
instance presentation, status columns, History drag/drop and suppression rules
below need source confirmation where not supported by the cited owner messages.

## Transferred DOCX requirements — Needs owner confirmation

The following source candidates are not instructions to implement. Exact values, added restrictions and implementation-derived details need owner confirmation. D numbers identify the archived DOCX paragraphs; [the coverage record](archive/2026-10-10/docx-coverage.json) accounts for every source block. Confirmed rules above override conflicting candidate wording. Implementation reports remain archival only.

### Definitions and background geometry

**D3 — Needs owner confirmation:** Components

**D5 — Needs owner confirmation:** Separate the component definition from its instances. Creating one placed component must create exactly one linked instance, without displaying its definition as an additional assembly instance.

**D6 — Needs owner confirmation:** New Component creates a domestic or external definition without a placed instance. Add Component creates or selects a definition and places one linked instance under the active component.

**D7 — Needs owner confirmation:** Bodies, excluding independently imported dumb bodies

**D9 — Needs owner confirmation:** A modeling feature owns its background result. Deleting or changing the feature must maintain valid result ownership; a visible solid must not remain detached from its background Body.

### Panel structure

**D10 — Needs owner confirmation:** Component panel

**D11 — Needs owner confirmation:** Replace the Model pane with Components and a separate Attributes pane.

**D13 — Needs owner confirmation:** Keep a component definition in the file even when every linked instance has been removed. Removing an instance must not remove its definition or leave orphaned links.

**D14 — Needs owner confirmation:** Deleting a definition from Models, when supported, is a distinct operation from deleting an instance from Part Tree; it must not happen implicitly.

**D15 — Needs owner confirmation:** Part Tree replaces Component Structure and Assembly Structure. It lists linked component instances only.

**D17 — Needs owner confirmation:** Allow Cut/Paste and drag/drop to rearrange the tree. Move existing instances without creating duplicate definitions or losing their links.

**D18 — Needs owner confirmation:** History replaces Model History and Part History. Show the sequential history of the active component.

**D19 — Needs owner confirmation:** Origin is always the first item, visible by default for the active component, and cannot be deleted.

**D20 — Needs owner confirmation:** Origin Planes is a separate child under Origin, hidden by default, and cannot be deleted.

**D21 — Needs owner confirmation:** Keep background Bodies out of both the component tree and History.

### Names and numbering

**D22 — Needs owner confirmation:** Names and numbering

**D23 — Needs owner confirmation:** Use untitled001 as the default file name.

**D25 — Needs owner confirmation:** Number feature labels within each component. The first sketch is Sketch001 and the first background Body is Body001 in every component.

**D26 — Needs owner confirmation:** Use Origin rather than exposing globally suffixed labels such as Origin001. Preserve the internal identities required by FreeCAD separately from the displayed labels.

### Classic panel outline

**D2640 — Needs owner confirmation:** Models: domestic definitions first, followed by nested imported-file groups and component instance counts.

**D2641 — Needs owner confirmation:** Part Tree: the file is the pinned top-level container, identified by its file name and FreeCAD icon. Linked component instances appear beneath it. The file container is not a component model in Models. Renaming the file row changes the file display name without renaming any component.

**D2642 — Needs owner confirmation:** In the Classic panel outline, history may be collapsed under each component instance. Editing a shared component definition affects all its instances.

**D2643 — Needs owner confirmation:** Do not show background Bodies as separately deletable objects.

**D2644 — Needs owner confirmation:** Attributes provides the former Model pane View and Data tabs.

### Edit state and Part Type details

**D2647 — Needs owner confirmation:** A new document creates a domestic Part001 definition, places its first occurrence beneath the file, and enters Edit for that component. Part001 is ordinary: it can be renamed, removed or deleted. An empty file is valid. Existing documents gain the file container without adding another Part001 or changing component identities, geometry, placements or references. Opening an older .cadprt file adds this container in memory after checking the saved file. The original on disk stays unchanged until Save. The added file row stays pinned through Undo; reopening an upgraded file does not add another container. In Models, select one unused domestic definition and choose Delete component or press Delete. Remove its occurrences and outside references first; otherwise explain why deletion is blocked. Imported definitions must be opened in their defining file before deletion. Deleting the edited unused model restores the file view and closes its isolated component tab. Undo restores the definition and geometry without reopening that tab. Part Tree Delete removes occurrences only; the file row remains protected. Reference checks cover open files, not other closed assemblies on disk.

**D2648 — Needs owner confirmation:** Edit is the user-facing term for making a component active. Double-click or Edit in Models or Part Tree changes the active component and displays its History within the current file tab. Single-click only selects. Open in new window is available in both context menus and opens a component in a new file tab. Opening, closing or switching component tabs preserves the original tabâ€™s edited occurrence and camera view. A child component can also be edited in the separate tab, with the same contextual transparency behavior. In Part Tree, double-click the component name or icon to edit that exact occurrence, including a nested or repeated instance. Activation must work when the tree refreshes between clicks. A pending click must not change another tab or activate a removed occurrence. Finish an open modeling task before editing a different component.

**D2650 — Needs owner confirmation:** Part Tree uses Part Type for Full Component, Bodies Only, Reference and Excluded. Visibility is a separate Shown or Hidden choice. Excluded geometry cannot be shown through visibility; change its Part Type first. The active component and its parent branch cannot be hidden. Editing an excluded component restores its own editing display without changing the exclusion saved by its parent.

**D2651 — Needs owner confirmation:** Part Type choices are saved on the active component for itself and its direct children, shared by every instance of that component and retained through save/reopen. The active component defaults to Full Component; its children default to Bodies Only. The active component may use Full Component or Bodies Only. Reset to Default restores the applicable default. Edit a deeper component's owner before changing that child's type. Switching the active component restores its saved choices.

**D2653 — Needs owner confirmation:** Existing nested display overrides remain effective until the affected child receives an explicit Part Type. New Part Type choices take precedence without changing another component's saved data. Parent and sibling geometry remains at least 75% transparent while the edited component and its descendants retain authored appearance.

**D2654 — Needs owner confirmation:** Geometry outside the chosen active occurrence and all its descendants is at least 75% transparent, preserving any greater existing transparency. Other occurrences of the same definition are also faded. Restore normal appearance when the edit context changes; authored visibility and transparency are preserved. Preserve component and individual face colors. Apply the transparency floor separately to each material, retaining faces already more transparent than 75%. This display belongs to the current file tab and does not change saved appearance settings.

### File editing and command availability

**D2655 — Needs owner confirmation:** Editing the file row shows only its fixed Origin and origin planes in History, with visibility controls. These establish global coordinates and support placement and assembly alignment. Geometry creation and editing require explicitly activating a component. Every component retains its own origin. When the file is active, all components use their normal transparency. File Edit refreshes references within its domestic component assembly without creating file-owned geometry or History entries. The Datum Plane action is disabled while the file is being edited; selecting a component alone does not enable it. Sketch and datum-plane commands must refuse the file as their destination before opening a task or changing the document. Move Components can change occurrence placements beneath the file, with Undo and Redo, without adding modeling History to the file. In a component document, the Part workbench Primitive, Extrude, Revolve, Loft and Sweep commands use the shared component tasks; Sweep opens Pipe. They require an edited component and must not fall back to a legacy dialog when file Edit refuses modeling. Legacy documents retain their existing Part dialogs. Native Part Boolean, copy, shape, datum, direct primitive and link-array commands are disabled during file Edit. Selecting geometry does not enable them. Direct invocation must leave objects, visibility and undo history unchanged. Inspection and display controls remain available.

### Placement and relationship menus

**D2659 — Needs owner confirmation:** Part Tree: linked component instances support Cut/Paste and drag/drop rearrangement beneath the pinned file container. File-level assembly relationships and placement controls are managed here without file-owned modeling geometry. With the file in Edit, right-click one top-level occurrence to Ground component at its current position or Unground component. Grounding applies to that occurrence, including occurrences of external models, and does not change the shared definition. Expand grouped instances to choose one occurrence. Nested or multiple selections, component Edit, unused-model Edit and unfinished tasks cannot change file grounding. Selecting the file once does not enter Edit. Grounding and ungrounding support Undo/Redo and keep the current tab and origin-only Model History. Changing Edit context while a menu is open cancels that action.

**D2660 — Needs owner confirmation:** Fixed relationships: while the file is in Edit, select two individual top-level occurrences and choose Fix relative position. Their current positions and orientations are retained; at least one must already be grounded or connected to a ground. Right-click the file or an occurrence and choose Assembly relationships to review Ground and Fixed relationships. Entries identify components by qualified name and occurrence number. Selecting entries highlights their components without changing Edit context or Model History. Edit fixed offset changes the second component relative to the first using X, Y and Z in millimeters and yaw, pitch and roll in degrees. Cancel or accepting unchanged values makes no change. Remove selected removes relationships, keeping the components; removing a ground releases its placement lock. Applied changes support Undo/Redo. Changing Edit context or deleting a listed relationship prevents a stale dialog from applying changes. These controls keep the current file tab and origin-only file History.

### Panel layout and controls

**D2662 — Needs owner confirmation:** Origin is first, visible by default and protected from deletion.

**D2663 — Needs owner confirmation:** Origin Planes is its own child, hidden by default and protected from deletion.

**D2665 — Needs owner confirmation:** On first startup, Components is visible at the top left and occupies about two-thirds of the left panel height. Attributes is below it and occupies about one-third. Tasks is docked on the right and shows New File and Open with no document. Subsequent startups restore the user-customized positions, floating state and sizing of panels and toolbars instead of resetting this initial layout.

**D2666 — Needs owner confirmation:** Attributes retains functional View and Data tabs.

### History editing, ordering and temporary suppression

**D2863 — Needs owner confirmation:** Components panel double-click editing: in History, double-click an operation or feature name, icon or status area to open its existing edit task; double-click a sketch to enter Sketcher edit mode directly. Editing must still work if a document notification rebuilds the History rows between the clicks. Resolve the selected document object before opening the editor, preserving the component and occurrence context. Keep single-click selection, visibility eyes, suppression checkboxes, Models and Part Tree component editing, and context-menu Edit unchanged. Origins remain protected and another active task must be finished before opening a different editor. Closing or cancelling the editor returns to the original component context.

**D2864 — Needs owner confirmation:** Model History ordering: drag feature/object names, icons or status areas to reorder within the active component. Drop above or below a row; empty space means the end. Clamp an invalid drop to the closest valid position after all predecessor objects and before all dependents, following transitive geometry and expression dependencies, including hidden profile binders and published results. The native part Origin remains the first displayed item and cannot be dragged; its origin planes remain protected. Dropping near the origin places a movable item at its earliest legal position below it. Multiple selected items retain their existing relative order, as do unselected items; an intervening dependency remains between selected items when needed. Show the actual allowed insertion line and scroll long histories at viewport edges. Store the change as one undoable History-order edit, preserving geometry, links, object/result identities, ownership and save/reopen behavior. Background results travel with their visible producer. Refuse cross-component, stale and active-edit moves. Keep existing selection, double-click editing, visibility and suppression behavior.


### Editing an earlier History item

**D2865 — Needs owner confirmation:** Editing Model History: temporarily suppress every subsequent feature or object in the active component, following the current reordered History sequence. Editing item 5 of 10 suppresses items 6 through 10, including independent later items and their background results. Keep the edited item, earlier items and native Origin available. Apply this shared behavior to sketches, native feature editors and combined modeling tasks. Later items show an unchecked Suppressed during edit state, are hidden and are unavailable as evaluated component inputs or results until editing ends. Keep existing authored suppression unchanged. Accept or Cancel restores prior suppression and display choices; a failed validation keeps the edit and temporary suppression active, while failed editor startup restores them. Refresh downstream results after completion. Temporary state must not create an Undo entry, alter object identities or persist when saving during an edit. Preserve component and occurrence context on return.

## Classic and Plus presentation

Plus UI Mode presents the Components panel (Models, Part Tree, History); Classic
UI Mode presents the native Model tree. The choice belongs to the model/components
selector and is independent of toolbar and task workflow choices. Both operate on
the same updated component/document backend; switching presentation must not
recreate objects, change ownership or discard Edit/task context. The property
editor remains available. In Plus UI Mode, Components occupies the top of the left
dock area, with Properties directly below it. Components must be available through normal startup and
the panel menu, not only a developer Python call.

See [the October 11 owner decision](EVIDENCE_AND_DECISIONS.md#independent-classic-and-plus-ui-sections---october-11-2026) and [mode defaults](DEFAULT_SETTINGS.md#independent-ui-modes).
# Approved Parts file workflows — November 27, 2026

The same owner approval covers Parts file-actions review `e2cefeaaa3b9`, fingerprint
`01658d784c8d20b8c2738350e2b8b1ec29b817d36bbfc5768832824906d91596`.
Create new part file appears above Import and uses the native Save picker. It
creates a default part and links its catalog into the current file without placing
an assembly instance. Sub-file menus offer Open file in new window, Import models
to file, and Search folders; a missing sub-file also offers Locate file and disables
Open/Copy until recovered. Independent copying targets the current file even while
editing an imported component. Dependent copies prompt for copying the editable
dependency graph, baking final shapes/meshes with placements, or Cancel. Shared
dependencies are copied once; unique domestic labels avoid imported-name collisions.

Search folders uses the approved task with multiple locations, recursive search,
Stop, verified candidates, explicit Use selected file, and optional locations saved
in the host. Pre-open missing-file prompts reuse Locate/Search/Cancel. Recovery
checks file UUID, required object names, graph validity and cycles. Searches never
change files. Relocations preserve loaded native object identities and become
durable on normal Save; originals are not rewritten during recovery.

# Approved Assembly controls — November 27, 2026

Owner approval covers review `ae8dafb11414`, fingerprint
`5a69bfb4d52c9bd1fe05376e4a91cdf41492ddc1e9e36fc7e140440791ec7658`.
The first assembly row has inline Expand all instances, Condense all instances,
Choose active assembly, and Move Components icons. The old Instances dropdown
and large chooser are removed. Repeated siblings can be condensed per parent.
Condensed menus retain all occurrence actions, replacing Condense with Expand.
Copy/Move and display choices address the grouped siblings; single-instance
removal/pattern actions explicitly choose an instance before the existing review.
Group display changes are atomic and reflect mixed values without false checkmarks.

## Corrected condensed and expanded views — November 27, 2026

Owner: “implement the corrected condensed and expanded instances views in the
assembly tree.” This approves the instance-view portion of review `5826d20f99b1`,
fingerprint `03fda706509a442b0c616aa334b6b8f154c2275a62a119f7f8e1a1eccd98bc68`.
The separate Edit within assembly/Edit in isolation menu revision remains pending.

Condensed groups are presentation rows with no disclosure arrow; double-click,
keyboard expansion, bulk tree expansion and viewport selection do not open them.
Expand instances and Expand all instances restore numbered occurrence rows;
real assembly branches keep their normal disclosure controls. Exact selection
survives both mode changes, including nested/imported occurrences. Full group
menus remain available when one member is being edited; grouped display actions
are disabled when all members cannot be addressed in that edit context.
Geometry, placements, object identities, active assembly, selected tab and Undo
are unchanged by presentation switches.

# Approved Components navigation — November 27, 2026

Owner: “implement all components tab changes previewed.” Approval covers native
review `30a2bb731e86` (fingerprint
`ab8728c6fbd9edac71464463805ba562a111f8030ee5ff28cf06eba2a66c955d`).
Component activation and Add existing/new retain the selected panel tab. Assembly
parent activation retains tree expansion. Standalone New Part still opens History;
modeling/sketch tasks retain their existing temporary History routing.

The active assembly and preferred occurrence are saved with the host document,
separately from the edited component. Saved choices override workspace history;
unavailable targets do not bind by label or a reused object name. Different views
retain their choices; saving uses the current view for that file. Older files remain
readable. See `evidence/components-20261127` for implementation validation.
