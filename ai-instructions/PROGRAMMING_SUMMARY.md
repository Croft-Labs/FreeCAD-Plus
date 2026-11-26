# FreeCAD Plus: Programming Summary

## Recent thumbnails and icon outline — installed November 26, 2026

Start reads embedded previews from `.cadprt` and `.CADPRT` through the native
FCStd reader. The app/shortcut/file icon has the approved white outer outline.
Native build, focused 6/6, file/icon regressions 30/30 and existing-shortcut 10/10
pass; all four owner preview bytes and unchanged files/settings are verified.
One owner file contains a blank saved PNG. Nine installed hashes match. Restart
FreeCAD Plus. See [evidence](evidence/thumbnails-outline-20261126/README.md).

## FreeCAD Plus icon B - installed November 25, 2026

The approved lower-right green plus now identifies the application, desktop shortcut
and .cadprt files. Transparent ICO frames cover 16-256 px; original Classic assets
and .FCStd association remain intact. Native build/resources pass, all 27 file
workflow checks pass, focused icon checks pass 3/3 and existing-shortcut checks pass
3/3. Ten installed payload hashes match. Current-user association uses a separate
FreeCADPlus.Document ProgID with a rollback snapshot. Restart the app to see its
updated window icon. See [evidence](evidence/plus-icon-20261125/README.md).


## Clone and Extract geometry - installed November 25, 2026

Modeling > Other now offers Clone and Extract geometry. Whole objects from direct
children become parent-owned associative dumb geometry; selected parent-owned faces
become extracted surfaces. History uses the same edit form. Child history remains
intact; native features/Booleans can consume the results. Atomic Undo, scene-only
preview, exact occurrence/source identities and schema-8 persistence are implemented.
Source tests pass 13/13. Installed regression checked 87 cases: two old duplicate-name
fixtures were corrected and pass in the final focused 15/15 run. Final profile-routing
checks pass 7/7, fresh-process reopen checks pass, and existing-shortcut checks pass 3/3.
Nineteen Python files installed with matching hashes and rollback copies. No native
rebuild required. Restart FreeCAD Plus. See [evidence](evidence/clone-extract-20261125/README.md).


## Open/import and conversion cursor correction — installed November 25, 2026

Open, Plus Import and component source choosers default to both `.cadprt` and
`.FCStd` together. Conversion/repair dialogs retain the normal pointer while idle;
acceptance shows busy and restores the cursor on success, error and Cancel.
Source and installed checks pass 27/27 each; existing shortcut checks pass 5/5.
Five installed hashes verified. Restart FreeCAD Plus. See
[evidence](evidence/file-dialog-fix-20261125/README.md).

## Assembly-wide component names — installed November 25, 2026

Unique definition names now span the full imported catalog, with reverse-importer
checks on source edits. Repeated instances remain valid; local/external tree labels
retain the owner's filename convention. Creation/import/rename/copy and native
saves enforce normalized uniqueness; old conflicts remain repairable. Installed
acceptance passes 81/81, source focused 15/15, fresh reopening and shortcut 5/5.
All 16 installed hashes match. Restart FreeCAD Plus. See
[evidence and boundaries](evidence/component-names-20261125/README.md).

## Remove individual instances — installed November 25, 2026

Assembly occurrence context menu > Remove instance and Assembly Delete now open the
same native review. One link and explicitly included dependent constraints are removed
in one owning-file transaction; definitions, other links, imports and geometry survive.
Shared-parent changes require acknowledgement. References, pattern-controlled members,
Edit ancestry, active roots and stale reviews are protected. No solver-driven movement
of survivors occurs during removal. Installed regressions pass 41/41, focused removal
12/12, final review checks 4/4, fresh reopening and shortcut 3/3. Five Python files
installed with verified hashes and rollback copies. Restart required. See
[implementation and evidence](evidence/instance-removal-20261125/README.md).

## Instance quantity and patterns — installed November 25, 2026

Add Component > Add existing/new > Next opens Quantity, Linear, Grid or Circular.
Counts apply per selected definition; Add new creates one definition. Patterns
remain editable through a member's Edit instance pattern menu. Shared native links,
parent-local placements, scene-only preview, atomic Undo and dependency guards are
implemented. Schema 7 persists parent-owned pattern metadata; schemas 1–6 remain
readable. Installed regressions pass 54/54; final shortcut checks 3/3 and fresh-process
reopen/reference/export checks pass. Thirteen Python files installed with verified
hashes and rollback copies. Restart required. See
[implementation and evidence](evidence/instance-quantity-20261125/README.md).

## Condensed/expanded instances — installed November 25, 2026

Assembly > Instances switches Expanded numbered siblings and Condensed quantity
groups, retaining native occurrence identity, selection and individual actions.
The view preference persists; imported labels and per-occurrence constraint
collectors remain intact. Final focused checks pass 9/9, fresh reopening and
existing-shortcut checks 3/3. Three Python files installed with verified hashes.
Restart FreeCAD Plus. Older clipboard/name fixtures fail on the unchanged baseline;
a viewport drag check fails in the combined suite but passes alone on both versions.
See [checks and boundaries](evidence/instance-display-20261125/README.md).

## Move Components — installed November 25, 2026

The approved Move/Rotate/Align workflow is installed in the existing owner payload.
Use the Assembly move button or a child occurrence's Move Components context menu.
Distance/vector, point-to-point, axis/angle, axes/frames and native drag handles
preserve the fixed active assembly, parent-relative/shared ownership and Edit context.
Preview, snapping, Apply/OK/Cancel and atomic Undo are implemented. All 22 affected
movement/reference/numeric checks pass; fresh reopening, six native method captures
and four existing-shortcut checks pass. The broader run passes 60/61, with one
order-dependent constraint-preselection check still unresolved (it passes alone).
See [exact evidence and limitation](evidence/move-components-20261125/README.md).
Eleven Python files were installed with hash verification and rollback copies;
no native rebuild. Restart FreeCAD Plus.

## Terminology

Owner clarification, November 25: a **component** can be a **part**, an **assembly**,
or **both**. Combining modeled geometry and child components is supported but not
recommended. This corrects potentially reversed terminology in the November 24
discussion. Follow the [canonical component terminology](ui-ux-specs/COMPONENT_PANEL.md#component-terminology--owner-clarification-november-25-2026).

## Native file formats and Classic conversion — installed

Plus saves/opens `.cadprt`; Classic uses `.FCStd`, independently of UI mode. Native
Open, Save/Save As/Save Copy/Save All and save-on-close follow this distinction.
Classic Open offers explicit conversion or Open Classic. Component import and Add
existing can convert Classic sources; export remains `.cadprt`. Mislabelled Plus
`.FCStd` files can be repaired into a new `.cadprt` without changing the original.
Conversion preserves supported editable content and refuses unsupported structures
without silent flattening or replacement. Native external links survive Save As,
Save Copy and repair to another directory. All 61 affected checks pass in the
installed app, as do six fresh-process reopen/edit/Undo cases and four shortcut
checks. Source regression and final workflow checks also pass. Restart FreeCAD
Plus to load the native DLL update. See [delivery evidence](evidence/file-formats-20261125/README.md).

## Unified Clone and Extract geometry — native preview prepared

November 25 owner direction: one Clone workflow selects geometric objects from
direct children only and creates native history-free geometry in the edited
parent. Child construction history remains in the child; only parent feature
operations modify/combine cloned geometry. This defines the earlier Add Reference
Feature concept. Follow the [current Clone contract](ui-ux-specs/COMPONENT_PANEL.md#clone-from-direct-children--november-25-2026);
Owner's latest refinement requires whole objects only and default labels cloned
body/surface/sketch/plane. Separate Extract geometry turns a face on cloned body
into extracted surface. Native create/edit task and browser screenshots are ready
for direct layout approval; runtime implementation remains pending. See
[proposal evidence](evidence/unified-clone-proposal-20261125/README.md).

## Responsive component tabs — installed

Parts/Assembly/History now shrink equally to the longest complete label, including
its selected bold state. The current padded width remains the maximum; tabs stay
left aligned. Source, installed-app and existing-shortcut native checks pass at
wide/intermediate/minimum widths, including clicks and overflow below minimum.
Restart FreeCAD Plus. See [evidence](evidence/responsive-tabs-20261125/README.md).

## Multi-part insertion and editable export — installed

Add Component > Add existing now opens other `.cadprt` files and adds checked parts
as linked children in one Undo step. Parts multi-selection offers Export parts to
file for independent editable copies, including shared children, history, expressions
and assembly constraints. Native File > Import is catalog-only. Source files and
Edit/active assembly remain unchanged; existing outputs are never replaced.
All 80 installed affected checks, fresh-process export/batch reopening, exported
constraint editing/Undo and five existing-shortcut checks pass. Nine Python payload
files were installed with rollback copies and verified hashes; no native rebuild.
Restart FreeCAD Plus. See [approval and delivery](evidence/part-transfer-20261125/README.md).

## Part-owned assembly constraints — installed

Every constrained part/subcomponent has a first-child, initially collapsed Assembly
constraints collector. Native joint creation/editing and Solve use the active assembly's
frame, with no mandatory child anchoring. Parts/Assembly/History tabs are equally padded
and left aligned. Schema 6 preserves native part/link identities and joint ownership.
All 30 new checks, saved reopening and six existing-shortcut checks pass. The broader
suite passes 81/82; the sole older coordinate-deletion assertion also fails unchanged
on the prior runtime. Restart FreeCAD Plus. See [approval and delivery](evidence/assembly-constraints-20261125/README.md).

## Add Component dropdown and child placement — installed

Add Component always opens **Add existing / Add new**. Both add one child beneath
the edited component; Add new creates its definition and instance together.
Standalone New Component remains definition-only and activates the new component.
New Assembly is removed from Plus tools; the active-assembly selector remains.
Cycle/stale-context checks, atomic Undo and external ownership are verified.
All 55 installed affected checks, two fresh-process reopen cases and six existing-shortcut checks pass. Restart
FreeCAD Plus. See [approval, screenshots and delivery](evidence/add-component-20261124/README.md).

## Active assembly selector — installed

Parts offers **Make active assembly**; Assembly shows the chosen part as its root
and has a selector button. The chooser lists current-file parts with nested instance
counts and collapsed groups for other loaded component files. Edit remains separate,
and the local workspace recalls the last explicit assembly choice. The approved
History heading/Rename remain intact. All nine new assembly checks and 13 final
source checks pass. The installed 75-case run passes 68; seven older unused-display
and cleanup failures also reproduce on the prior runtime. Fresh reopening and all
14 existing-shortcut checks pass. See
[screenshots, exact checks and delivery](evidence/active-assembly-20261124/README.md).
Restart running FreeCAD Plus sessions to load the Python update.

## Active component and Rename in History — installed

History now starts with the active component's icon/name aligned at the far left,
above the visibility eyes. The heading has no eye and offers right-click Rename.
Existing naming validation, shared labels, Undo/Redo, geometry and History ordering
are preserved. All 44 source and installed checks, fresh-process reopening and
five existing-shortcut checks passed. Restart the app. See
[approval, implementation and screenshots](evidence/history-component-20261124/README.md).

## Single Pattern item in Elements — installed

Native Elements groups saved pattern membership into one row, preserving originals
and unrelated rows, aggregate selection/visibility/filtering, native Delete/Undo
and the populated pattern editor. Free copies now save a recipe without adding
constraints. Fully deleted recipes are removed transactionally. The 102-case
affected suite, final six-case Elements rerun, four saved-file edits/reopens and
existing-shortcut check pass. Restart the app. See
[the owning evidence](evidence/pattern-elements-20261124/README.md).

## Persistent memory error — corrected and installed

The saved owner sketch reproduces the failure at verified 0.100 in pitches.
Suppressing temporary generated constraint labels before solve prevents oversized
intermediate image allocation; final Pattern grouping restores intended visibility.
The exact installed 20-by-20 Apply succeeds in 16.86 seconds. All 96 application
tests, fresh-process save/reopen/edit to 420 instances and the existing shortcut
pass. Chains, Equal sizes, pitch drivers, units and Undo/Redo remain verified.
Earlier GUI probes retained 20 mm pitches; corrected tests assert committed values.
No native rebuild was needed. See
[implementation and evidence](evidence/pattern-label-allocation-20261124/README.md).

## Large circle-pattern memory — installed

November 24, 2026. Owner reported an allocation error after applying a 20-by-20
circle grid. Sparse solver diagnosis now avoids dense Jacobian/factor copies and
reduces only needed dependency columns; factorization memory is reused sequentially.
The installed task completes in 17.43 seconds versus 32.78,
with peak private memory reduced from 1.54 GB to 1.21 GB.
All spacing/Equal relationships, conflict checks, pitch edits, hiding and Undo remain.
The exact original allocation error did not reproduce in the isolated fixture;
these are verified reductions in memory pressure, not a universal OOM guarantee.
91 native tests and 94 build-runtime application checks pass; 75 installed
cases have no failures/errors and one upstream skip. Saved-grid reopening and the
existing shortcut pass too. Restart the app.
See [measurements, implementation and limits](evidence/pattern-memory-20261124/README.md).

## Existing Sketch Pattern editing — installed

November 24, 2026. Owner approved the populated editor and Apply/Done/Cancel
workflow. Double-click either the single Pattern icon or constraint-list entry to
edit original geometry, counts, spacing and directions, including angular/radial
patterns and explicit units. Preview replaces the old instances without changing
the document. Done updates/closes; Apply updates/clears; Cancel discards pending
edits. Persistent native geometry IDs preserve definitions across save/reopen;
surviving copy identities and native spacing/Equal relationships are retained.
Recoverable older grouped patterns open with an equivalent layout; ambiguous or
dependent cases explain the blocker rather than discarding geometry.
All 93 installed application checks and 88 native tests pass, plus four
fresh-process saved-file edits and three existing-shortcut checks. A fixed-length
12-by-12 grid applies in 4.04 seconds and edits in 3.80 seconds locally.
Restart FreeCAD Plus to load the update. See
[implementation, native captures and delivery](evidence/pattern-edit-20261124/README.md).

## Pattern groups and fixed-length grid speed — installed

November 24, 2026. The owner approved one Pattern entry/icon without expandable
children. Fixed-length 12-by-12 line grids now apply in 4.12 seconds through the
installed task (3.81 seconds through the service), versus the previous 57.28 seconds.
Both endpoint spacing chains, 143 Equal copy lengths and two pitch drivers remain;
source length/orientation and pitch edits propagate correctly. Hide spacing chain
also hides all grouped constraint graphics while retaining the Pattern list entry.
Double-click the entry to edit its pitches with the normal unit-aware editor.
All 79 installed application checks and 88 native Sketcher tests pass. Fresh-process
reopening verifies grouped line/circle grids, renumbered constraints and legacy files.
The existing desktop shortcut passed both task/editor checks (4.04-second Apply).
Restart FreeCAD Plus to load the native update. See
[implementation, captures and delivery](evidence/pattern-group-20261124/README.md).

## Pattern batching — prior update (line slowdown resolved above)

November 24, 2026. Owner-approved batching groups geometry, constraints and spacing
visibility updates. The installed 12-by-12 circle grid applies in 1.54–1.57 seconds
through the task panel; the prior benchmark did not finish within its 100-second
deadline. Spacing chains, Equal size relationships, pitch/diameter edits and Undo
remain intact. All 72 installed application checks, fresh-process saved-grid editing
and existing-shortcut acceptance pass. Fixed-length line grids remain slower because
of redundancy checks (12-by-12 measured 57.28 seconds). See
[implementation, measurements and limits](evidence/pattern-batching-20261124/README.md).

## Pattern/task corrections — installed

November 24, 2026. Owner-approved narrow fields, partial-direction previews including
spacing helpers, Equal sizes instead of repeated copy dimensions, and Done-left/apply-close
versus Apply-right/apply-reset are installed. All 68 installed application checks and
88 native sketch tests pass, plus five fresh-process saved-file checks and four
existing-shortcut checks. Restart FreeCAD Plus to load the native update. See
[implementation and actual native screenshots](evidence/pattern-corrections-20261124/README.md).

## Spacing chains and quantities — installed

November 24, 2026. Owner-approved line/arc spacing chains, persistent hide control, shared six-decimal
entry, explicit units and secondary display preferences are installed. Native build,
88 C++ solver tests, 144 installed application checks, four fresh-process saved-file
checks and two existing-shortcut checks pass. Restart FreeCAD Plus to load the native
update; see [implementation and evidence](evidence/spacing-units-20261124/README.md).

## Sketch Pattern installed - November 24, 2026

Approved dedicated linear/circular task with independent one/two/symmetric extents,
total instance counts, angular/radial directions and optional native dimensions.
All 53 installed acceptance/regression checks passed, plus the existing shortcut
and fresh-process reopen. See [implementation, screenshots and delivery evidence](evidence/sketch-pattern-20261124/README.md).

## Compatible symmetry redundancy installed - November 24, 2026

Rectangle symmetry now accepts verified redundant equations while retaining all
constraints and actual conflict detection. Native build, 88 C++ tests, 39 installed
checks (one upstream skip), and the existing shortcut passed. See
[solver correction and acceptance](evidence/constraint-symmetry-20261124/README.md).

## Sketcher symmetry task installed - November 23, 2026

Approved dedicated symmetry task with enlarged Geometry list, reference field and
Apply/Done. Native geometry, constraints and Undo remain; normal sketch sections
restore on leaving the tool. All 41 installed regression checks passed.
See [acceptance and native captures](evidence/sketch-symmetry-20261123/README.md).

## Consistent feature input gestures installed - November 23, 2026

Plain click adds without duplicates; Shift-click removes feature inputs. Shared
Python collectors, native component dress-ups, History and deferred curve chains
carry the gesture consistently. All 134 installed checks and the existing shortcut
passed. See [acceptance and source scope](evidence/feature-pick-20261123/README.md).

## Fillet selection repair installed — November 23, 2026

Deferred guarded curve-chain delivery prevents the native consuming-picker loop;
canonical seed names prevent double toggles. Plus Fillet opens whole-solid inputs
with an empty edge list and routes by selected/sole component result, not ambient
Body. Eight build and 90 installed checks, viewport picking, reopen/edit and shortcut
checks passed. See [repair evidence](evidence/fillet-20261123/README.md).

## Unified Loft installed — November 23, 2026

Loft combines Solid/Sheet and New/Add/Subtract in one creation/edit task with
ordered sections. Plus task entries are combined; Classic aliases use shared
component routing without active-Body dependence. Native saved features retain
their native editors. Installed broad suite 120 checks and final Loft suite 17
passed, with native UI/colors, binder-entry, fresh-reopen and shortcut verification.
See [acceptance and screenshots](evidence/loft-20261123/README.md) and
[architecture](ARCHITECTURE.md#unified-loft--november-23-2026).

## Component-only routing repair installed — November 23, 2026

Shell now resolves the selected solid's Body regardless of Classic active-Body state;
empty Plus selection asks for a solid instead of silently using that state. Older
Body-owned sketches stay in shared Extrude/Revolve tasks. The owner's rule that
Plus has an active Component and no active Body is recorded for every modified
workflow and future feature migration.

All 31 build and 31 installed checks pass, plus the native multi-solid/migrated-
creation audit, fresh-process reopen and existing shortcut check. Four payload
files have rollback copies; owner sessions/settings were preserved. See
[repair, audit and screenshots](evidence/shell-routing-20261123/README.md).

## Installed Shell, Thicken and Surface layout — November 23, 2026

Modeling now contains the six native Surface actions plus Thicken, replacing the
Plus Surface tab. PartDesign Thickness is presented as Shell, with invalid-input
preflight and failed-entry cleanup. Thicken shares the feature task/persistence
services for New/Add/Subtract sheet offsets and associative editing. Native build,
107 distinct installed regression cases, direct UI, fresh-process recompute and
shortcut checks passed. See [acceptance](evidence/thicken-20261123/README.md).


## Installed Revolve Solid/Sheet — November 23, 2026

Revolve now shares Extrude's approved Solid/Sheet controls. Sheet forces New and
rotates curves into uncapped sheets; Solid remains default and preserves legacy
features. Axis and angular workflows, edit identity and task visibility remain.
All 96 build and 96 installed checks pass, plus native task interaction, separate
process persistence/recompute and shortcut verification. See
[acceptance](evidence/revolve-sheet-20261123/README.md).

## Installed Extrude Solid/Sheet — November 23, 2026

Approved output choices now create native uncapped sheets from open/closed curves.
Sheet forces and locks New; Solid remains default and keeps New/Add/Subtract.
Persisted output defaults older features to Solid. Shared edit, identity, history,
visibility and Revolve behavior are preserved. Ten focused build and 88 installed
checks pass, plus native command/edit, fresh-process recompute and shortcut checks.
See [acceptance and supported extents](evidence/extrude-sheet-20261123/README.md).

## Installed selection-button correction — November 23, 2026

The curve-intent setting is a full-button dropdown with a normal theme background;
the selected checkmark remains in its menu. Five build and five installed checks
pass, including both themes and native picking. See
[repair evidence](evidence/selection-button-repair-20261123/README.md).

## Installed selection toolbar and sketch task controls — November 23, 2026

Named chain settings, readable category summaries, Select all/reset and safe
Select 1 category replacement are installed. Empty filters are prevented/repaired.
Sketch tasks show Exit Sketch and action-only Cancel with native Escape semantics
in both modes. All 16 build and 39 installed checks, visual cases, fresh-process
settings and existing-shortcut checks passed. See
[acceptance](WORK_STATE.md#selection-toolbar-and-sketch-buttons-installed--november-23-2026).

## Installed creation selection repair — November 23, 2026

New-component navigation now clears selection after opening History while retaining
the active component, restoring the approved idle geometry tasks. Eight installed
checks and three native creation-path checks pass. See [acceptance](WORK_STATE.md#creation-selection-repair-installed--november-23-2026).

## Installed component/task workflow updates — November 23, 2026

New components activate with History selected. New Body starting task cards are
removed. Plus sketch tasks use Extrude/Revolve; Classic buttons open the same shared
component workflows. Future additive/subtractive migrations must combine Plus task
entries too. Eight focused checks, 113 installed regressions, five startup checks
and native visual checks passed. See [acceptance](WORK_STATE.md#component-creation-and-modeling-task-updates-installed--november-23-2026).

## Installed prominent task-error styling — November 23, 2026

The owner approved shared amber error emphasis matching the Extrude target field.
`task_status.TaskStatus` is installed in Plane, Sketch, Extrude and Revolve, with
bounded reveal, focus preservation and valid-state recovery. Future inline task errors
reuse it. All 122 installed regression checks, five fresh startup checks and four
installed visual cases passed. See [acceptance](WORK_STATE.md#prominent-task-errors-installed--november-23-2026).

## Attach Sketch sequential-order repair — November 23, 2026

The owner-reported `Sketcher_MapSketch` bypass is repaired: validate support against
History before native attachment mutates dependencies, with reorder-and-retry guidance.
Sketch support-property picks share the boundary. See [repair status and acceptance](WORK_STATE.md#attach-sketch-sequential-order-repair--november-23-2026).

## Latest Plane/Sketch placement and History reordering — November 23, 2026

Both approved workflows are installed: shared compatible/conflicting reference
collection and normal-through-point placement, plus persistent dependency-safe
History dragging with corrected-position popups and a fixed first Coordinate System.
Older saved plane construction, native identities/references and source ownership
are preserved. Undo/Redo and fresh-process save/reopen passed.

Validation covers 213 installed regression checks (212 broad plus the repaired
external-source fixture), five startup checks, 62 build checks and installed Qt
drop/selection cases. Actual OS mouse dragging remains unverified because both
computer tools failed window attachment. See [current acceptance](WORK_STATE.md#planesketch-placement-and-history-reordering-installed--november-23-2026).

## Historical History drag preview — November 23, 2026

The owner requests manual feature order constrained by dependencies, a fixed first
Coordinate System, and correction before the earliest dependent plus a popup for
invalid downward moves. The native UI demonstration passes its three specimen drop
cases and coordinate-subtree lock. Both proposals were later approved and implemented
in the increment above.
See [current preview and scope](WORK_STATE.md#history-drag-reorder-preview--november-23-2026).

## Historical plane-selection preview — November 23, 2026

The owner requests shared compatible/conflicting selection behavior for Plane and
Sketch placement, line+point normal-through-point construction, and equivalent
plane/face, line/straight-edge and point/vertex inputs. All 16 native UI specimen
cases pass. The owner later approved implementation together with History ordering.
See [current preview and next scope](WORK_STATE.md#plane-selection-preview--november-23-2026).

## Latest target selection and coordinate-system protection — November 23, 2026

Approved changes are installed: Extrude/Revolve Add/Subtract automatically select the
sole eligible solid; otherwise they highlight Target solid with inline guidance before
curve selection. Existing valid targets and hidden-target display are preserved. The
native base coordinate frame and its point/axes/planes cannot be deleted individually
in Plus documents, including through the document API. Whole-owner deletion, Undo/Redo,
custom datums and legacy documents remain supported.

All 16 focused build checks and 207 installed regression/startup tests passed, plus
12 installed UI cases and fresh-process save/reopen protection checks. The existing
shortcut launched the updated application with isolated settings; rollback files remain.
See [acceptance](WORK_STATE.md#target-selection-and-coordinate-system-persistence--november-23-2026).

## Latest strict sequential History — November 22, 2026

The approved change is installed: component History follows native dependencies
across Body boundaries, keeping sketches and other inputs before their consumers.
Shared editors reject later/self inputs before mutation. Existing graphs retain
geometry, identity, ownership and saved schema. All 28 targeted development and
165 unique installed checks passed, plus actual History-click and fresh-reopen checks.
A separate updated app was launched through the existing shortcut with isolated settings.
The owner's unsaved Unnamed window was preserved and needs a restart after saving.
See [acceptance](WORK_STATE.md#strict-sequential-history--november-22-2026).

## Latest History coordinate presentation — November 22, 2026

The approved change is installed: Axes/Planes use their children's native icons;
Coordinate System and descendants start collapsed. Refresh preserves manual expansion
choices and geometry visibility. All 14 existing native panel/History checks and a
separate installed visual check passed. The existing shortcut was restarted with
isolated settings. See
[acceptance](WORK_STATE.md#history-coordinate-icons-and-collapsed-defaults--november-22-2026).

## Latest unified Revolve and selection lists — November 22, 2026

Approved changes are installed. Extrude and Revolve share an at-least-five-row
scrollable profile collector. Revolution/Groove commands now share New Solid/Add/
Subtract creation and editing for component profiles, with axis references/guide,
degree-based offsets and angles, symmetric/two-sided rotation, selected-target display
and validity colors. Native saved links, identity, source ownership and Undo remain
intact. All 11 focused build checks and 188 installed tests passed, plus separate
native visual and saved-file reopen checks. Native To first/To last remain disabled;
angular references require planes through the axis. See
[acceptance](WORK_STATE.md#unified-revolve-implementation--november-22-2026).

## Latest Extrude target and preview colors — November 22, 2026

The approved change is installed: hidden targets selected in History display in the
configured selection color while their eyes remain unchanged. Visible targets retain
native reference picking. Add tools are green/yellow for valid/invalid results;
Subtract tools are red/pink. Invalid native operations retain the actual tool for
preview but remain impossible to accept. Source visibility/materials and transactions
are preserved. Eight focused build tests, all 177 installed native tests, four native
visual cases and fresh save/reopen checks passed. The existing shortcut was restarted
with isolated settings. See
[acceptance](WORK_STATE.md#extrude-selected-targets-and-validity-colors--november-22-2026).

## Latest sketch exit framing — November 22, 2026

The approved change is installed: leaving a new or existing nonempty sketch fits
the visible model to include the full sketch while retaining exit orientation.
It runs after native cleanup and skips empty/deleted sketches, cancelled placement
and stale views/editors. Visibility, selection, History restoration and Undo remain
intact. Seven focused build tests, all 169 installed tests, and separate native
Close-button/save-reopen checks passed. See
[acceptance](WORK_STATE.md#view-fitting-after-sketch-exit--november-22-2026).

## Latest sketch coordinate visibility — November 22, 2026

The approved change is installed: entering new or existing sketch drawing hides
the component Coordinate System temporarily. Plane selection still shows planes;
Sketcher's axes and other geometry remain visible as before. History eyes remain
usable, and exit restores prior display with native semantics for explicit choices.
Automatic hiding changes no saved visibility or transaction data. All 162 tests
passed in both build and installed payloads; separate drawing/save-reopen checks
and the existing shortcut restart passed with isolated settings. See
[acceptance](WORK_STATE.md#sketch-coordinate-system-visibility--november-22-2026).

## Latest sketch/task update — November 22, 2026

Approved changes are installed: mouse-only sketch creation adds no unsolicited
dimensions while geometric constraints and deliberate dimensions remain available.
Feature creation/edit temporarily selects History and restores the prior tab on
exit, including sketch placement-to-drawing and standalone native Part dialogs.
All 155 installed tests and separate GUI/save-reopen checks passed. The app was
restarted through the existing shortcut with isolated settings. See
[acceptance](WORK_STATE.md#sketch-dimensions-and-feature-task-history--november-22-2026).

## Latest Extrude update — November 22, 2026

Approved Extrude visibility behavior and shared task tree controls are installed.
New tasks filter unusable geometry; edits isolate profile/target; solids become
translucent with target-field selection coloring. Planar solid/sheet faces are
associative profiles. Temporary display restores cleanly; explicit eye choices
remain undoable. All 134 installed native tests plus separate GUI/reopen checks
passed, and the existing shortcut was restarted with isolated settings. See
[acceptance](WORK_STATE.md#extrude-visibility-and-shared-tree-controls--november-22-2026).

## Latest History update — November 22, 2026

Approved Coordinate System hierarchy is implemented and installed: native Origin
point, Axes and Planes subgroups, group and individual left-margin visibility eyes.
New components show their origin/axes/planes; existing saved visibility is retained.
63 native checks and installed fresh-process verification passed. See
[acceptance](WORK_STATE.md#coordinate-system-history--november-22-2026).

## Current baseline

November 22 approved toolbar layout is installed across all nine Design tabs:
bordered icons, separate icon/arrow segments, logical groups with separate dropdown
columns, and vertical section dividers. The three Constraints menus share a column.
Surplus spacing in the proposed renders was removed before installation; compact
natural-width buttons retain their arrow area on narrow scrolling pages. Thirteen
installed native regression cases passed. See
[acceptance](WORK_STATE.md#design-toolbar-layout--november-22-2026).

November 22 approved corrections are installed: rectangular Extrude previews no
longer show diagonal rear-face shading, and new/existing component sketch editing
preserves shown/hidden geometry, including native rendered LinkVisibility. The
previous checks covered saved flags but missed this rendering distinction. All 107
expanded native checks and independent GUI/save-reopen checks passed; see
[acceptance](WORK_STATE.md#extrude-rendering-and-sketch-visibility-correction--november-22-2026).

November 22 approved Design interactions are installed: New Sketch automatically
shows fundamental planes; History eyes remain usable during placement and native
drawing; idle Design offers New Sketch, Datum Plane, Datum Line and Datum Point.
Typed numeric values wait for field leave; arrow steps update immediately with
focus retained, including native quantity editors. Line/Point reuse native tasks
with component ownership. All 103 affected native checks and independent reopen/UI
verification passed; see [acceptance](WORK_STATE.md#design-interaction-implementation--november-22-2026).

November 22 approved Extrude is implemented and installed, including vertically
stacked New Solid/Add/Subtract radio buttons. The shared creation/edit task uses
explicit targets, sketch/curve/region picks, start/end references, independent
sides, direction/taper and transient tool/result previews. Numerical recompute
waits for field leave for typed values; explicit arrow steps update immediately. Managed operations retain native feature identity and use
internal Bodies. The native build, 90 installed checks, fresh-process persistence
and actual GUI acceptance passed; see [acceptance and boundaries](WORK_STATE.md#extrude-implementation--november-22-2026).

November 21 approved Sketch Offset/Reverse offset and orange local Plane/Sketch
axes are implemented. Offset persists in the shared creation/editing task, follows
the support normal and is unaffected by sketch normal reversal. Typed numeric previews
still wait for field leave; older managed sketches default to zero. See
[acceptance](WORK_STATE.md#sketch-offset-and-orange-axes-implementation--november-21-2026).

November 21 archive-guided plane improvements implement the approved concepts
afresh in current modules: next-pick guidance, numbered reference highlights,
repeat-pick/Delete removal and saved independent axis reversal. Creation/editing
share the task; older planes remain unchanged until acceptance. See
[acceptance](WORK_STATE.md#plane-guidance-implementation--november-21-2026).

November 21 approved New Sketch placement is installed: plane/face preselection,
automatic plane-frame inheritance or part-origin/X projection, editable references,
and the shared placement-edit task. Sketches retain native identity and drawing;
placement remains associative after extrusion and save/reopen. See
[installed acceptance](WORK_STATE.md#new-sketch-placement-implementation--november-21-2026).

Owner rule: every feature/operation must reuse its creation task for editing, with
saved inputs prefilled, identity-preserving acceptance and unchanged Cancel. Plane
editing has been verified through both existing entry routes; follow the
[shared task contract](ui-ux-specs/TASK_PANEL.md#shared-task-patterns) for all further work.

November 21 approved New Plane workflow is installed: the existing command opens
the right-hand task panel for Plus components, with associative geometry references,
point-only origin, X/Y direction assignment and Flip normal. Planes belong directly
to the component; no Body is created. Shared numerical editors and Move/Rotate
previews defer updates until focus leaves. See
[WORK_STATE](WORK_STATE.md#new-plane-implementation--november-21-2026) for installed
acceptance, persistence evidence and two independently reproduced baseline test failures.

November 21 approved History UI: component activation opens History, with native
Origin grouping its three axes and three fundamental planes. Every part History
item has a fixed left-margin visibility eye. Source-owned native visibility,
parent containers, task/context guards and Undo/Redo remain in use. See
[WORK_STATE](WORK_STATE.md#grouped-history-and-left-margin-visibility--november-21-2026)
for installed/native evidence and the component specification for direct approval.

November 21 owner terminology: original FreeCAD uses **body-centered modeling**;
FreeCAD Plus uses **feature-centered modeling**. The new backend module
`freecad_plus/modeling.py` creates sketches without Bodies and atomically supplies
a native Body when extruding a new solid. The existing ribbon New Sketch and
Extrude commands initially routed to these services. The approved sketch placement
task replaces the initial native placement dialog; drawing stays native. The
November 22 Plus Extrude task now owns creation/editing of managed operations and
explicit Add/Subtract targets. Classic commands and existing Body-owned chains
retain native compatibility through the original routing adapters.
See [architecture](ARCHITECTURE.md#feature-centered-modeling-foundation--november-21-2026)
for API scope and [WORK_STATE](WORK_STATE.md#feature-centered-modeling-foundation--november-21-2026)
for initial native acceptance and the newer
[command integration](WORK_STATE.md#feature-centered-command-integration--november-21-2026)
for command/installed-app validation. The newer
[Add/Subtract increment](WORK_STATE.md#feature-centered-addsubtract-targets--november-21-2026)
records target routing, Cancel/Undo/Redo and persistence acceptance. Arbitrary
imported Part targets, consumed-profile reuse and feature deletion remain
outstanding; this is not a completed replacement of every body-centered workflow.

This checkout starts from official **FreeCAD 1.1.4** source at
`4fd3bf320d9566a27e60069fc8387448aaa3a094`, plus owner documentation, an agent entry
point and focused generated-file ignore rules. Branch: `codex/freecad-1.1.4-baseline`.
No previous Plus application changes have been carried into this branch. Group 1
now has validated, opt-in domestic/external catalogs, hierarchy, shared-instance,
independent-copy and legacy-conversion services under src/Mod/FreeCADPlus.
G1.6a adds an opt-in Models/Part Tree/History panel foundation with placed-component
Edit and native selection. G1.6b domestic/external unused-model editing is validated
in the native development build, including source-owned Undo/save, picking and
per-view cleanup. G1.6c1 component file tabs are validated in the development
build; WORK_STATE records tests, fresh-process persistence and inspected captures.
G1.6c2 Part Tree linked-instance Copy/Paste is validated in the development build;
WORK_STATE records 50 combined tests, fresh-process persistence and inspected captures.
The November 25 Move Components workflow supersedes the earlier Translate/Rotate
foundation and parked Point to Point increment. It supplies all approved Move,
Rotate and Align methods, native dynamic handles and active-assembly routing.
Move Components remains operation/task-panel work. G1.7a saved Part Type
and visibility state is validated in the development payload; WORK_STATE records
acceptance and limits. G1.7b1 adds view-local explicit hiding/restoration; WORK_STATE
records its validation. G1.7b2 contextual fading is validated in the development
payload, including shared mixed face materials and independent reopen. Its planned
checks are complete. G1.7b3a saved self/child display in domestic/external unused
previews is also validated. G1.7b3b Bodies Only filtering is validated in placed
and unused views, with bounded native link-snapshot synchronization. G1.7b3c adds
validated occurrence-aware Reference/Excluded eligibility and guards the existing
Move Components reference consumers. G1.7b3d guards native File > Export before
options/writing and fixes source selection for external unused component exports.
G1.7b3e adds native PartDesign profile and Sketcher Projection/Intersection input
eligibility. Its focused native tests and independent reopen/source-update checks
passed. G1.7b3f native attachment and shared picked axis/direction/plane references
also passed focused native and independent reopen/downstream checks. G1.7b3g covers
the separate attachment editor and Extrude face/shape intake, with validated Apply/
Cancel cleanup and independent downstream checks. G1.7b3h Loft/Pipe picked profiles,
sections and main/auxiliary paths passed focused native and independent reopen checks.
G1.7b3i shared dress-up/transformed input guards, including whole-edge controls,
passed targeted native and independent reopen checks. G1.7b3j command-start
selection checks and Pattern feedback routing passed focused native and independent
reopen checks, including the Chamfer rejected-selection cleanup correction.
G1.7b3k same-component native Boolean ownership, History and nested edit paths passed
focused native and independent reopen checks. G1.7b3l extends isolated legacy
conversion to those native Boolean-owned tool graphs; focused conversion and
independent reopen/source-edit checks passed. G1.7b3m placed external export context
passed native build, focused export and independent reopen checks. Stop here.
WORK_STATE owns acceptance evidence. Boolean Reference/Excluded command and picker
admission passed focused native and independent reopen checks in G1.7b3n;
ownership of tools from another Full Component is
still undefined. Direct exporter/view-output paths still need integration. Check latest
owner conversations before asking design questions. Full G1.7b and Group 1
remain incomplete. WORK_STATE owns acceptance evidence.
G1.6c5 shared definition Rename passed native menu/dialog, source-owned Undo and
independent reopen checks. The complete G1.6 panel is unfinished.
G1.6c6 Models file import passed native menus/chooser, source-owned catalog/Undo,
closed-source hidden loading and independent reopen. It creates no placed instances.
The October 11 owner clarification explicitly requires all Reference geometry to
enter the active component's History through Add Reference Feature before any use.
G1.7b3o core Part Boolean admission and retained input/result ownership passed native
and independent reopen/source-edit checks. G1.7b3p direct Part Section also passed
native command/dialog and independent reopen/source-edit checks. G1.7b3q Compound
creation passed four focused native cases and independent reopen/source-edit.
G1.7b3r Compound drop/replacement and Links-editor intake passed six focused native
cases after two targeted corrections, plus independent reopen/source-edit.
G1.7b3s split/join command admission and result ownership passed five focused native
cases after correcting related-filter insertion, plus independent reopen/source-edit.
G1.7b3t split/join property editing passed four focused native cases, two affected
Compound regressions and independent reopen/source-edit. Next: split/join tree drop
and replacement. Other consumers remain unfinished; WORK_STATE owns support/stopping
boundaries.
The official 26.3 RC1 is a prerelease, not the stable version selected by the owner.

G1.6d supersedes the developer-only startup boundary: General/Application now has
independent model/components, toolbar and task-workflow selectors, all Plus by
default. InitGui installs the panel presentation controller; Classic preserves the
same component backend. Plus toolbars now have a separate ribbon module; tasks still share Classic definitions. Native
Pad/Pocket share FeatureExtrude; a consolidated Plus task is still future work.
WORK_STATE records startup, mixed-mode, active-task and persistence acceptance.
G1.6e connects native New File to document.new_document and New Part to
hierarchy.new_part: a catalog definition only, with placement kept separate.
WORK_STATE records bounded native command/Undo/reopen acceptance.

TB.2a completes Classic workbench/toolbar inclusion in the separate Plus module.
The full native development build now contains all nineteen baseline workbenches
plus None; All Tools preserves native groups, commands, specialized widgets and
custom toolbars. Eight interaction tests, every-workbench inventory audit and
independent restart passed. WORK_STATE owns evidence and the stopping boundary;
remaining curated layouts and Plus-only workflows are still separate work.
TB.2a1 routes modes by native workbench identity so duplicate/renamed labels preserve
added-workbench access and Design-only control scope; WORK_STATE owns acceptance.
TB.2a2 keeps enabled alternatives reachable in Plus split groups when the remembered
command is unavailable, without changing native command state or last-choice memory.
TB.2b adds validated complete two-line captions and icon-only unavailable controls;
nine interaction/layout cases and all-workbench coverage passed. TB.2c1 adds the
saved Design Directional Selection control and native model/Sketcher behavior.
TB.2c2a adds the saved Single/Connected/Tangent Curve Intent split button with native
viewport edge traversal and mapped Sketcher/occurrence handling. WORK_STATE owns
build and runtime evidence. TB.2c2b adds saved category-checkbox filtering with an
independent native selection gate, including model and Sketcher batch admission.
TB.2c2c corrects Plus Sketcher plain-click replacement, modified empty clicks and
selected Escape handling. Native build and focused point/edge/constraint interaction
checks passed; WORK_STATE owns combined acceptance and coverage evidence.
TB.2c2d adds the saved Persistent Selection toggle and native Equal-to-Construction
retention, plus a correction that preserves BIM status-toolbar ownership. WORK_STATE
owns native acceptance. TB.2c2e extends retention to basic preselected sketch
constraints, including point alignment, coincidence, symmetry and native tangency
substitutions. Continuous constraint picking retains its own cleanup. WORK_STATE
owns acceptance. TB.2c2f integrates named preselected distance, angle and circular
dimensions through native dialog completion, including Cancel and reference/no-dialog
paths, and fixes Curve Intent icon/arrow sizing under native styles. Continuous
dimension picking keeps native sequence cleanup. TB.2c2g connects direct Tangent/
Perpendicular completion and conic commit outcomes to the same retention policy;
WORK_STATE owns native acceptance and geometry-family limits. TB.2c2h extends
retention to selected Driving/Reference and Active toggles and menu-only Refraction,
including rejection/no-op handling and native creation-mode preservation. All 51
toolbar cases, full Classic inventory and independent restart passed; WORK_STATE
owns evidence. TB.2c2i integrates preselected contextual Dimension through native
activation, dialog/commit and handler teardown while preserving continuous picking
and native autoscale transactions. All 57 toolbar cases, complete Classic inventory
and independent restart passed; WORK_STATE owns acceptance limits. TB.2c2j adds
idle B-spline degree-elevation retention through the existing native identity and
transaction services. TB.2c2k retains surviving geometry through Delete All Constraints
and prevents native list refresh from clearing idle Plus selection. Native cleanup
uses original selection references for deleted constraints, including nested paths.
WORK_STATE owns targeted acceptance and preservation checks. Other operation integrations, Layers and unfinished Plus workflows remain outstanding.

## Where to go

| Task | Reference |
| --- | --- |
| Component/document target contract | [Architecture](ARCHITECTURE.md), [Group 1 stages](DEVELOPMENT_ROADMAP.md#group-1--component-panel-and-document-structure) |
| Intended UI/workflows | [UI specification index](UI_UX_SPEC.md) |
| Unconfirmed implemented ideas from old fork | [Review inventory](ui-ux-specs/UNVERIFIED_IMPLEMENTED_CHANGES.md) |
| Conversation evidence and conflicts | [Evidence ledger](ui-ux-specs/EVIDENCE_AND_DECISIONS.md) |
| Prior fork recovery | [Archive reference](ARCHIVE_REFERENCE.md) |
| Current work/status | [Roadmap](DEVELOPMENT_ROADMAP.md), [WORK_STATE](WORK_STATE.md) |
| Stable baseline inventory and local checks | [Runtime inventory and completed display check](WORK_STATE.md#stable-baseline-inventory-and-light-runtime-check--october-10-2026) |
| Execution/build guidance | [Development guidelines](DEVELOPMENT_GUIDELINES.md), [guide](DEVELOPMENT_GUIDE.md) |
| Product scope | [Product specification](PRODUCT_SPEC.md) |
| Old implementation records | [Historical documents](archive/pre-restart-docs/README.md) |

## Source map

- src/Mod/FreeCADPlus/freecad_plus/toolbars.py: separate Plus ribbon widgets, native action/menu adapters and Classic visibility restoration.
- src/Mod/FreeCADPlus/freecad_plus/selection_toolbar.py and src/Gui/Selection/PlusSelection.h: saved Design selection toggle and transient native selection policy.
- src/Mod/FreeCADPlus/freecad_plus/toolbar_layout.py: Plus mode/tab/group definitions.
- src/Mod/FreeCADPlus/freecad_plus/curve_selection.py: viewport-only native curve/edge connectivity and tangent traversal.
- src/Mod/FreeCADPlus/TestPlusToolbars.py: native split-button, mode/tab, independent preference and Classic restoration acceptance.

- src/App and src/Gui: upstream document/application and desktop services.
- src/Mod: original workbench modules; retain their source and availability.
- src/Mod/FreeCADPlus/freecad_plus/document.py: schema, native owned_children/owned_path traversal, History projection and creation/open/save.
- src/Mod/FreeCADPlus/TestPartBooleanInputs.py: native Part Boolean/Section/Compound admission, input/result ownership, Undo, dialog Apply, legacy bypass and persistence.
- src/Mod/Part/Gui/ComponentBoolean.h and src/Mod/Part/BOPTools/BOPFeatures.py: Part Boolean preflight bridge and component-owned native result creation.
- src/Mod/Part/Gui/ViewProviderCompound.cpp and src/Gui/Dialogs/DlgPropertyLink.cpp: Compound native input-edit admission; Tree and PropertyItem preflight context/multi-target edits.
- src/Mod/FreeCADPlus/TestComponentBooleanInputs.py: Boolean command/picker occurrence admission, atomic rejection, cleanup and legacy bypass.
- src/Mod/FreeCADPlus/TestComponentBooleanOwnership.py: same-component Boolean ownership, nested History/Edit, Undo/Cancel and independent persistence checks.
- src/Mod/FreeCADPlus/freecad_plus/editing.py: per-view Edit, backend Body and native feature adapters.
- src/Mod/FreeCADPlus/TestComponentPilot.py: G1.2 regression suite and fresh-process check.
- src/Mod/FreeCADPlus/freecad_plus/conversion.py: isolated legacy conversion and persisted loss report.
- src/Mod/FreeCADPlus/TestLegacyBooleanConversion.py: native Boolean graph conversion, source isolation and independent persistence checks.
- src/Mod/FreeCADPlus/TestLegacyConversion.py: G1.3 fixtures and fresh-process acceptance.
- src/Mod/FreeCADPlus/freecad_plus/hierarchy.py: domestic graph, placement and occurrence paths.
- src/Mod/FreeCADPlus/freecad_plus/legacy_hierarchy.py: native Part/link conversion.
- src/Mod/FreeCADPlus/TestComponentHierarchy.py: G1.4 regression and fresh-process checks.
- src/Mod/FreeCADPlus/freecad_plus/external.py: native import catalogs, file identity/preflight, defining-file saves and independent copies.
- src/Mod/FreeCADPlus/TestExternalDefinitions.py: G1.5 regression and fresh-process checks.
- src/Mod/FreeCADPlus/freecad_plus/panel.py: opt-in panel, stable row projection, selection/Edit and native document observers.
- src/Mod/FreeCADPlus/TestComponentImport.py: Models import menus/chooser, nested catalogs, external ownership, guards and independent reopen.
- src/Mod/FreeCADPlus/TestComponentRename.py: shared definition Rename, native menus/dialogs, source-owned Undo and persistence.
- src/Mod/FreeCADPlus/TestComponentPanel.py: G1.6a actual Qt interaction, lifecycle and persistence tests.
- src/Mod/FreeCADPlus/freecad_plus/isolation.py: transient per-view unused-definition display and cleanup.
- src/Mod/FreeCADPlus/TestUnusedModels.py: unused-model interaction, native editors/picking, source-owned Undo/save and lifecycle checks.
- src/Mod/FreeCADPlus/TestComponentWindows.py: component-tab menus, per-view context/camera, guards, cleanup and fresh-process persistence.
- src/Mod/FreeCADPlus/TestComponentClipboard.py: linked Copy/Paste menus/keys, batch Undo, shared identity, source ownership and save/reopen.
- src/Mod/FreeCADPlus/freecad_plus/geometry.py: occurrence-aware Reference/Excluded geometry eligibility, independent of display/selection.
- src/Mod/FreeCADPlus/TestComponentEligibility.py: consumer guard, shared/external ownership and fresh-process acceptance.
- src/Gui/ComponentGeometry.h: shared native modeling eligibility bridge for PartDesign/Sketcher.
- src/Mod/FreeCADPlus/TestComponentCommandInputs.py: native dress-up/transformation command starts, Pattern routing and independent persistence checks.
- src/Mod/FreeCADPlus/TestComponentDressUpInputs.py: native dress-up/transformed admission, whole-edge context guards, transactions and independent persistence checks.
- src/Mod/PartDesign/Gui/TaskDressUpParameters.cpp and TaskTransformedParameters.cpp: shared picked-input guards; TaskFilletParameters.cpp and TaskChamferParameters.cpp also guard Use All Edges.
- src/Mod/FreeCADPlus/TestComponentSweepInputs.py: Loft/Pipe reference admission, native transactions and independent recompute/persistence checks.
- src/Mod/PartDesign/Gui/TaskLoftParameters.cpp and TaskPipeParameters.cpp: picked profile, section and main/auxiliary path admission.
- src/Mod/FreeCADPlus/TestComponentInputEditors.py: Python attachment/Extrude input acceptance, confirmation/Undo and independent downstream checks.
- src/Mod/Part/AttachmentEditor/TaskAttachmentEditor.py and src/Mod/PartDesign/Gui/TaskExtrudeParameters.cpp: component admission for remaining attachment and Extrude face/shape inputs.
- src/Mod/FreeCADPlus/TestComponentReferences.py: native attachment/axis collector, atomic rejection, legacy bypass and downstream acceptance.
- src/Mod/Part/Gui/TaskAttacher.cpp and src/Mod/PartDesign/Gui/ReferenceSelection.cpp: component input guards for native attachment/shared picked references.
- src/Mod/FreeCADPlus/TestComponentModeling.py: native intake, transactions, legacy bypass and independent reopen checks.
- src/Mod/FreeCADPlus/TestComponentExternalExport.py: original external export occurrences, source payload and independent reopen checks.
- src/Mod/FreeCADPlus/TestComponentExport.py: native File > Export rejection, BREP/legacy/source-owned export and independent reopen.
- src/Gui/Application.cpp and CommandDoc.cpp: component-only export preflight and external unused source-selection routing.
- src/Mod/FreeCADPlus/freecad_plus/movement.py: active-assembly Move/Rotate/Align task, transient preview and atomic commit.
- src/Mod/FreeCADPlus/TestComponentMove.py: task/placement/source ownership and fresh-process persistence checks.
- src/Mod/FreeCADPlus/freecad_plus/display.py: schema-5 saved self/direct-child choices and occurrence hide-path resolution.
- src/Gui/View3DPy.cpp: native per-view hide wrapper and fading context; no saved display-property changes.
- src/Gui/Selection/SoFCSelectionAction.cpp: per-view transparency floor in native shape rendering.
- src/Mod/FreeCADPlus/TestComponentFading.py: normal-framebuffer blending, separate views, material/identity and reopen checks.
- src/Mod/FreeCADPlus/TestComponentVisibility.py: hiding, independent views, cleanup, recompute and reopen checks.
- src/Mod/FreeCADPlus/TestComponentBodiesOnly.py: content filtering, native editor, nested/shared/unused contexts and reopen checks.
- src/Mod/FreeCADPlus/TestComponentDisplay.py: panel/state ownership, migration, copy and persistence checks.
- src/Mod/FreeCADPlus/TestComponentRotate.py: located-axis/pivot rotation, shared placement and fresh-process acceptance.
- tests and per-workbench tests: upstream test infrastructure.
- CMakeLists.txt, CMakePresets.json and .github/workflows: this release's build definitions.
- .gitmodules: this release's pinned GSL, OndselSolver, AddonManager and GoogleTest.

Existing external FreeCAD Plus builds use the archived implementation. They do not
validate or represent this clean checkout. Reimplementation begins only from an
explicit task and confirmed requirements; historical backlog entries do not restart work.
