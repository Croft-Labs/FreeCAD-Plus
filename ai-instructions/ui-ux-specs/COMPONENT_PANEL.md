# Component panel

Status: owner-intent specification, reconstructed 2026-10-10. **Only the confirmed requirements are authoritative.** Material headed **Needs owner confirmation** is preserved for review and must not be treated as an approved change. The current application, agent-written specifications and implementation reports do not establish owner approval. Newer explicit owner decisions supersede older decisions on the same subject. See [evidence and unresolved decisions](EVIDENCE_AND_DECISIONS.md).

Implementation planning and acceptance are owned by the [Group 1 roadmap](../DEVELOPMENT_ROADMAP.md#group-1--component-panel-and-document-structure) and [component contract](../ARCHITECTURE.md). The G1.6a opt-in panel foundation and preceding hierarchy/external-definition services do not establish completion of this panel or approve any deferred UI detail. Domestic and external unused-model editing have bounded native-build validation. Component file tabs have bounded development-build acceptance recorded in WORK_STATE. Linked-instance Copy/Paste is a separate increment tracked there and in the [clipboard contract](../ARCHITECTURE.md#linked-instance-clipboard-g16c2); its selected-parent destination/local-placement convention is an announced implementation choice, not a recovered owner decision. Move Components foundation/Translate is implemented with acceptance tracked in WORK_STATE and the [movement contract](../ARCHITECTURE.md#move-components-foundation-and-translate-g16c3). Its remaining movement methods and other context actions are pending. Implementation boundaries and remaining unused-model/action work are recorded in the linked roadmap and contract. Import/storage/copy services are available to the later panel; their existence does not establish a finished Add Component dialog or placement-selection checklist. Conversion support and its tested boundaries are recorded in the component contract; the legacy-file requirements below remain the intended full behavior.

## Confirmed requirements

### Component, definition and instance

A component serves as both a part and an assembly: it can contain its own sketches, operations/features and other geometry, and linked instances of child components. Models holds definitions; Part Tree holds placed instances. Repeated instances share their definition. Core Bodies are background implementation objects, not objects the user must create, activate or manage independently. The user works with sketches, operations/features and geometry. [Current owner direction](EVIDENCE_AND_DECISIONS.md#current)

### File root and new files

New File creates a domestic **Part001** definition, places one instance beneath the file, and enters Edit for Part001. Part001 is an ordinary component that may be renamed, removed or deleted. An empty file is valid. The **file**, identified by its file name and a FreeCAD icon, is the pinned top-level Part Tree row. [C09](EVIDENCE_AND_DECISIONS.md#c09)

The file owns a fixed Origin and three origin planes defining global coordinates. Its History shows only these, with visibility controls. File-level assembly relationships and placement controls are managed in Part Tree. Sketches, features and modeling geometry must belong to a component. Starting a modeling command while editing the file requires the user to explicitly edit or create a component; do not silently choose one. Existing files gain the file container without another Part001 or changes to existing names, geometry, placements or references. [C09](EVIDENCE_AND_DECISIONS.md#c09)

### Models tab and storage

List domestic definitions first, followed by expandable imported-file groups containing all definitions from each file. Include nested imported files: the later multi-level requirement replaces the earlier single-level outline. Importing a file populates Models; it does not place the entire file in Part Tree. Unused definitions remain available. [C09](EVIDENCE_AND_DECISIONS.md#c09)

New Component allows storage in the current defining file, a new external file, or an existing external file such as Hardware. Use **domestic** and **external** terminology. Names must be unique within a file; equal names in different files remain distinct definitions. Show a domestic name without a qualifier, and an external name as **M3 screw (Hardware)**. Do not silently substitute a domestic definition for an external one with the same name. [C09](EVIDENCE_AND_DECISIONS.md#c09)

Editing an external definition edits and saves its defining file. Other files using it receive the saved change when reopened. Child components must come from the active definition's own file or from files imported into that defining file. An external Hardware component cannot simply acquire a component from the importing assembly's domestic list. Edit Hardware and import the required file there first. Immediately flag and block circular file references and circular component nesting. [C09](EVIDENCE_AND_DECISIONS.md#c09)

Copying between domestic and external storage creates an independent definition; it is not an identity-preserving move. When copying an external definition to domestic storage, prompt the user to choose placements to replace with the new copy. The original external definition remains independently usable. Exact checklist defaults and cancellation behavior have not been confirmed by the accessible owner messages. [C09](EVIDENCE_AND_DECISIONS.md#c09)

### Edit, selection and component tabs

Use **Edit** as the UI term for making a component active. Double-click or context-menu Edit in Models or Part Tree edits the chosen component in the **current file tab** and shows its History. A single click selects only, including on the file row. Double-click activation must work reliably. [C09](EVIDENCE_AND_DECISIONS.md#c09), [C10](EVIDENCE_AND_DECISIONS.md#c10)

Show the active definition in bold with the configured active-item fill color in Models and on **all its Part Tree occurrences**. Keep a separate selection indicator on the occurrence used to enter Edit. Editing a definition from Models reuses its last edited occurrence in that tab, otherwise its first occurrence in Part Tree. [C09](EVIDENCE_AND_DECISIONS.md#c09)

**Open in new window**, offered by right-click in both tabs, opens a new file tab for the component. Ordinary Edit must not open that tab automatically. Viewport context display is specified once in [Model View Window](MODEL_VIEW_WINDOW.md#component-editing-display). [C09](EVIDENCE_AND_DECISIONS.md#c09)

### Editing an unused model

Temporarily show the unused model as the last Part Tree entry, **Component name (unused model)**, retaining any external-file qualifier. Give it active fill and bold text. It supports editing but is not a permanent instance and cannot be reordered as one. Gray the other tree entries while their viewport geometry is temporarily hidden. They remain selectable and available for Edit. [C09](EVIDENCE_AND_DECISIONS.md#c09)

Editing another component or the file removes the temporary entry and restores the previous visibility. Saving retains edits to the definition without saving the temporary entry or hiding state. An unused model must not become an additional permanent tree root. [C09](EVIDENCE_AND_DECISIONS.md#c09)

### Part Type and visibility

Use **Part Type**, replacing Part View. The types are **Full Component**, **Bodies Only**, **Reference**, and **Excluded**. Shown/Hidden is separate visibility state; Excluded is not another name for Hidden and cannot be overridden with Show. [C10](EVIDENCE_AND_DECISIONS.md#c10)

The active component defaults to Full Component; its direct children default to Bodies Only. Save overrides on the component for itself and its direct children, persist them through save/reopen, and restore them when that component is edited again. The parent's definition owns its child choices, so all instances of that parent share them. Do not substitute a global display preference or independent per-occurrence override. [C10](EVIDENCE_AND_DECISIONS.md#c10)

A direct Reference child displays its full geometry while its parent is edited, respecting its own nested exclusions. Editing an ancestor makes that reference behave as Excluded without erasing its saved Reference setting. Reactivating its owner restores Reference. To use an excluded nested component as a reference, add that component separately as a direct Reference child. [C10](EVIDENCE_AND_DECISIONS.md#c10)

**Add Reference Feature is mandatory before reference-child geometry may be used.** It creates an owned, derived and linked reference sketch/body/other feature in the active component. A promoted reference body becomes a body of that component. Unpromoted source geometry is not directly usable for modeling or as final component geometry. This supersedes the suggestion that displayed Reference geometry alone could be used as sketch/attachment inputs. The detailed Add Reference Feature task remains to be defined. [C10](EVIDENCE_AND_DECISIONS.md#c10)

### History and legacy files

Show the active component's sequential sketches, operations/features and other geometry. Background Bodies must not reappear as separately managed rows. A legacy conversion should retain editable features where possible, putting required sketches and producing operations before their results. Move definitions to Models and represent links as Part Tree instances. If a feature cannot be converted parametrically, preserve recoverable final geometry as explicitly identified dumb body/curve geometry rather than losing it. The current backend's conversion limits are not restrictions on the intended workflow. [C06](EVIDENCE_AND_DECISIONS.md#c06), [current owner direction](EVIDENCE_AND_DECISIONS.md#current)

### Context-menu requirements and deferred decisions

| Location | Confirmed action | Required behavior |
| --- | --- | --- |
| Models / Part Tree | Edit | Edit definition in the current tab; retain occurrence context. |
| Models / Part Tree | Open in new window | Open a component file tab. |
| Part Tree | Copy / Paste | Create another linked instance for subsequent movement; do not embed Copy in Move Components. |
| Part Tree instance | Move Components | Open the shared task described in [Task Panel](TASK_PANEL.md#move-components). |
| Models / storage copy | Copy external to domestic | Independent definition; prompt for placements to replace. |

The changed **Add Component** task remains explicitly deferred. Importing external models and placing selected models are separate actions; do not invent a finished placement dialog from the current code. The detailed delete/grounding/fixed-relationship menus, grouped instance presentation, status columns, History drag/drop and suppression rules below need source confirmation where not supported by the cited owner messages.

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
