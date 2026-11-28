# November 27: History operation colors and labels installed

The approved palette correction is installed: yellow New/Add and red Subtract,
with display-only `(new body)`, `(new surface)`, `(add)` and `(subtract)` suffixes.
Saved names, native source/toolbar icons and History reference identities remain
unchanged. All 20 source and 20 installed checks pass; three payload hashes match,
owner settings/shortcut are unchanged. See [evidence](evidence/history-operations-20261127/README.md).
Transformation workflow `57a9ef350816` and plane visibility `40f73afdef86` remain
separately pending approval.

# November 27: Assembly visibility, Clone picking and Appearance edges installed

All three approved previews are implemented and installed. Assembly child eyes
follow tree indentation, with no eye/hide action for the active root. Anchored
assembly children use normal text. Clone accepts face/edge clicks as whole-source
picks without Browse, preserving direct-child occurrence identity. Appearance
selection/preselection retains its preference fill with contrasting true edges.
All 63 installed checks pass; 14 source/build/app payload hashes match and owner
settings/shortcut are unchanged. See [evidence](evidence/assembly-selection-20261127/README.md).

# November 27: Single-part opening correction installed

One-part files now activate their part and populate History when opened. The bug
was unconditional file-level Edit, despite the separate sole-part active-assembly
default. Normal opening, recovered files and sub-file windows share the correction.
All 17 installed checks pass; source/build/installed payload hashes match. Owner
settings and shortcut are unchanged. See [evidence](evidence/single-part-open-20261127/README.md).
Saved active-part bookmarks for multi-part files remain pending separately.

# November 27: Reference image View button installed

The approved View > Reference > Reference image button is installed. Native click,
Cancel/document preservation and no-component eligibility checks pass. Source,
build and installed hashes match; owner settings and shortcut are unchanged.
See [delivery evidence](evidence/view-image-button-20261127/README.md).

# November 27: Reference image workflow installed

The approved task is implemented and installed, with the owner's final simple
fundamental/created-plane attachment and offset correction. Native image storage,
attachment recompute, all anchors, 0.01-degree rotations, calibration/transparency,
History editing/visibility/deletion and Apply/reset are verified. All 45 installed
checks pass; nine Python payloads and PartDesignGui match, with protected settings
and shortcut unchanged. See [evidence](evidence/reference-image-20261127/README.md).
Three broader legacy plane-test failures reproduce in the untouched baseline.

# November 27: Design toolbar changes installed

The approved Home/common/Assembly/Modeling changes are installed, including Part's
exact Boolean group, functional Appearance and Clone's sheep icon. All 12 final
installed regressions pass; seven payloads match with preserved settings/shortcut.
See [delivery evidence](evidence/design-toolbar-20261127/README.md).
The later approved reference-image workflow is delivered above.

# November 27: History Appearance and face highlighting installed

Approved History menu and face-selection corrections are implemented, script-built
and installed. All 22 installed regressions pass; seven payload hashes match and
owner settings/shortcut are preserved. See [delivery evidence](evidence/history-appearance-20261127/README.md).
The single-part opening fallback is now delivered above. The separately previewed
saved active-part restoration remains pending.

# November 27: Joined surface extraction installed

Modeling > Other > Extract geometry now defaults Join surfaces on, creating one
connected surface/shell History feature. Turning it off creates one entry per face.
Disconnected, point-only, overlapping and invalid shell inputs are rejected before
a transaction. Saved multi-face references, native recompute, History editing,
split-in-place, missing-source recovery, Cancel and Undo are implemented. Native
script build and 32 source/32 installed regressions pass; final button-state checks
are recorded in [delivery evidence](evidence/joined-extraction-20261127/README.md).
Five Python payloads are installed with rollback copies; settings and shortcut are
unchanged. Restart FreeCAD Plus to load the workflow in an already-running window.

# November 27: All six pending workflow groups installed

Implemented the approved assembly edit modes, single-local-part default assembly,
Sketcher Symmetry defaults/on-axis constraints, responsive toolbar tabs, Plus task
Apply/reset/footer behavior and preference-based face highlights, and contextual
surface selection. Native build and focused source checks pass. The installed run
passed 89/91; both viewport misses passed in a fresh isolated rerun, alongside
the surface gesture check. Six older isolation assertions also fail on the
unchanged baseline and remain a recorded limitation. All 31 installed payloads
match source/build hashes; owner settings and shortcut are unchanged. Rollback
copies are retained. The owner saved and closed the app before installation;
FreeCAD Plus can now be reopened. See
[delivery evidence](evidence/pending-workflows-20261127/README.md).

# November 27: Corrected Assembly instance views installed

Arrow-free condensed groups stay folded; explicit per-group/global expansion
restores numbered native occurrences. Real assembly disclosure, exact selection,
menu parity and model/Undo state are preserved. Final installed checks pass 26/26;
three payload hashes match, with rollback and unchanged settings/shortcut.
See [delivery evidence](evidence/instance-views-20261127/README.md).
Edit-mode menus, single-part default assembly and Sketcher Symmetry were subsequently installed above.

# November 27: Approved Components panel changes installed

All three approved previews are implemented: retained navigation/saved assembly,
compact Assembly controls and full group menus, and Parts file creation/copy/search/
recovery. Source integration passes 102/102, final focused/fresh checks 7/7, and
38 installed cases pass. Seventeen payload hashes match; rollback copies retained;
owner settings and shortcut are unchanged. Restart required. See
[Components delivery evidence](evidence/components-20261127/README.md).

# November 27: Appearance installed

Approved Appearance task and Parts menu grouping are installed. Native source
regressions pass 43/43 and installed checks 11/11; renderer confirms whole-Body
and selected-face colors. Eight payload hashes match with rollback copies.
Owner CFG/shortcut preserved. Restart required. See
[delivery evidence](evidence/appearance-20261127/README.md).
Navigation/tab retention and saved active assembly were subsequently implemented above.

# November 26: Save All and Hidden line installed

Both reviewed changes are installed after chat approval. The native renderer
removes internal triangle lines while retaining CAD edges, silhouettes, selection
and placement style behavior. Save All sits between Save and Save As and saves
all open/imported documents. Native build, 49 staged checks, 14 installed checks
and separate installed render/save exercises pass. Three hashes verified; restart
required. See [delivery evidence](evidence/save-hidden-20261126/README.md).

# November 26: Mesh import repair installed

Native File and Mesh import now preserve component ownership and mesh History.
Native build and source/installed focused checks pass 26/26; fresh reopening and
original STL import pass. The repaired copy preserves mesh/sketch bytes and all
identities; original owner file unchanged. Six payload hashes verified; restart
required. See [evidence and baseline comparison](evidence/mesh-import-20261126/README.md).
Save All and Hidden line were subsequently approved and installed; see above.

# November 26: Placement display and active-component additions installed

Approved native style-following/translucent placement and Parts/Assembly destination
workflow are installed. All 66 installed regressions, ten existing-shortcut checks
and fresh-process saved pattern/edit/Undo checks pass. Five installed Python hashes
match; owner CFG settings remain unchanged. Restart required. The previously
disclosed native Hidden line artifact remains. See
[delivery evidence](evidence/placement-workflow-20261126/README.md).

# November 26: Recent Files thumbnails and icon outline installed

Both owner-approved changes are installed. Native build passes; focused 6/6,
file/icon regressions 30/30 and existing-shortcut 10/10 pass. All four owner
embedded previews load without document/settings changes; one saved PNG is blank.
Nine installed hashes match, with rollback copies retained. Restart FreeCAD Plus.
See [implementation and limits](evidence/thumbnails-outline-20261126/README.md).

# November 25: file chooser and cursor correction installed

## FreeCAD Plus icon B - installed November 25, 2026

The approved lower-right green plus now identifies the application, desktop shortcut
and .cadprt files. Transparent ICO frames cover 16-256 px; original Classic assets
and .FCStd association remain intact. Native build/resources pass, all 27 file
workflow checks pass, focused icon checks pass 3/3 and existing-shortcut checks pass
3/3. Ten installed payload hashes match. Current-user association uses a separate
FreeCADPlus.Document ProgID with a rollback snapshot. Restart the app to see its
updated window icon. See [evidence](evidence/plus-icon-20261125/README.md).


Combined `.cadprt`/`.FCStd` Open/Import defaults and idle conversion pointer are
implemented. Native build passes; source 27/27, installed 27/27, shortcut 5/5.
Five installed payload hashes match; rollback copies retained. Restart required.
See [evidence](evidence/file-dialog-fix-20261125/README.md).

# FreeCAD Plus: Current work state

## FreeCAD Plus 2.0.0 branding — installed November 27, 2026

Name, version, About/splash and remaining product logos are updated. Native
Windows caption and both executable property versions are verified. Desktop
shortcut renamed with launcher/profile preserved. Build, 32 staged and 32
installed regressions pass; final GUI correction passes branding and 5 navigation
checks. See [evidence](evidence/branding-20261127/README.md). Restart an older
running instance. Component edit modes were subsequently installed above.

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

## Assembly-wide component names — installed November 25, 2026

Complete imported catalogs now enforce unique definition names across local and
external files; repeated instances are allowed. Existing source-qualified tree
labels remain. Imports, renames, creation/copies and native saves share the guard.
Older conflicts can be repaired without losing document access. Installed 81/81,
source focused 15/15, fresh reopen and existing shortcut 5/5 pass. Sixteen installed
hashes verified; restart the app. See [evidence](evidence/component-names-20261125/README.md).
Quantity/patterns and individual instance removal are now installed.

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

Owner's renewed implementation instruction authorizes the prepared layout.
Assembly > Instances now switches numbered occurrences and collapsed identity
groups, preserving individual actions, selection and model/Undo/Edit state.
Preference, imports and identity pass fresh-process reopening. Final focused 9/9
and desktop-shortcut 3/3 checks pass; three Python files installed and hash verified.
Restart required. Broad checks retain baseline clipboard/name-fixture failures and
an order-sensitive viewport ring check (passes alone on baseline and final code).
See [full evidence](evidence/instance-display-20261125/README.md).

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

## Native file formats and Classic conversion — installed November 25, 2026

Owner instruction "implement file extensions and conversions" approved the
previously rendered workflow. Native App/GUI format handling and explicit Classic
conversion are installed in the existing owner payload, with retained rollback
files and all eleven installed hashes verified. Format is content-based: Plus
`.cadprt`, Classic `.FCStd`. Native Open/Save/Save As/Save Copy/Save All/close and
component import/add/export follow that distinction. Repair preserves originals;
unsupported Classic structures remain explicit conversion errors.

The App/GUI build succeeds. Final installed acceptance passes 61/61, including
22 new native/GUI workflow cases and existing conversion, import/export and
external-definition coverage. Source regression passes 60/60 and the final
transaction safeguard passes all 22 workflow cases. Six outputs reopen in a fresh installed
process with geometry editing/Undo and original Classic content preserved.
Four existing-shortcut checks also pass. The owning
[evidence record](evidence/file-formats-20261125/README.md) records the
reviewed screenshots, source/runtime provenance and bounded
conversion limitations. Restart running sessions for the native update.

## Responsive component tabs — installed November 25, 2026

Approved sizing is installed: equal tabs shrink to a common text-fit minimum and
retain their previous padded maximum. Native source, installed and existing-shortcut
checks pass; all tabs remain readable/clickable at minimum. Only panel.py changed
in the runtime; its hash is verified and a rollback copy is retained. Restart the app.
See [evidence](evidence/responsive-tabs-20261125/README.md).

## Part-file transfer — installed November 25, 2026

The owner renewed the external-file/export request and approved both native dialogs.
Batch Add existing and independent selected-part `.cadprt` export are implemented
and installed. Shared children and native constraints survive copying; no source-file
dependency remains in an export. Cancel, transactional rollback, recursive/file-cycle
guards and exclusive new-file publication are verified. All 80 installed affected
checks, source/installed fresh reopening and five existing-shortcut checks pass.
The Python-only update retains rollback files; all nine installed hashes match.
Restart running sessions. See [evidence](evidence/part-transfer-20261125/README.md).

## Assembly constraints and component tabs — installed

November 25: the owner-approved native joint integration, recursive collectors and
equal padded left-aligned tabs are installed. Active assembly and Edit remain separate;
parent-local frames replace mandatory child grounding. Schema 6 and one native Assembly
module were delivered with rollback copies and matching hashes for all 11 payload files.
All 30 new cases pass; source/installed affected runs both pass 81/82. The sole error is
the older pilot test deleting protected coordinates, reproduced on the prior installed
runtime. Source/installed saved reopening and all six existing-shortcut checks pass.
See [evidence and screenshots](evidence/assembly-constraints-20261125/README.md).
Restart existing sessions. The separate file import/export request was cancelled;
no new transfer workflow was implemented. The older unrelated failures below remain open.

## Add Component — installed

November 24: approved always-open dropdown and separate existing/new child dialogs
are installed with rollback copies. All 55 affected native checks pass, including
13 new workflow cases, hierarchy/import regressions, standalone New Component,
active assembly, History rename and toolbar behavior. Domestic/external saved
children reopen with native IDs, geometry and linked ownership intact; add/Undo
also works after reopening. All six existing-shortcut checks pass. No native rebuild or schema migration was needed.
See [evidence](evidence/add-component-20261124/README.md). Restart running sessions.
The older unused-display/cleanup issues recorded below remain a separate scope.

## Active assembly selection — installed

November 24: owner-approved Parts/Assembly/History tabs, selected-part assembly
root, Parts context action and counted selector are installed with rollback copies.
All nine new assembly cases pass; the final source assembly/creation run passes
13 checks. Installed affected run: 68/75 pass, seven pre-existing unused-part
display/cleanup assertions fail on both old and new runtime. These remain open,
not skipped or represented as passing. Fresh-process reopening preserves the
local choice, native IDs and geometry; all 14 existing-shortcut checks pass. See
[approval, direct screenshots and validation](evidence/active-assembly-20261124/README.md).
Restart existing sessions. No native rebuild or document migration was needed.

## History component heading — installed

November 24: approved far-left active component row and right-click Rename are
installed. Source/installed 44-case suites, fresh-process save/reopen checks and
five existing-shortcut checks pass. Restart running sessions. See
[evidence and screenshots](evidence/history-component-20261124/README.md).

## Single Pattern item in Elements — installed

November 24, 2026. Owner directed completion of the existing preview. Native
Elements now represents generated curves and spacing helpers with one actual
non-expandable Pattern row. Source/unrelated geometry stays separate; selection,
visibility, member filtering and the existing editor are integrated. Free-copy
patterns retain operation identity without acquiring constraints. Deleting an
operation removes its recipe with the geometry in the same Undo transaction.
All 102 affected regression checks pass, followed by six focused checks on the
final installation, four saved-file edit/reopen cases and the existing shortcut.
12-by-12 and 20-by-20 grids retain chains, Equal sizes and one Elements operation
row. Restart FreeCAD Plus to load the native update. See
[implementation and results](evidence/pattern-elements-20261124/README.md).

## Persistent pattern memory error — reproduced, corrected and installed

November 24, 2026. The owner's saved sketch reproduces the allocation error at
20 by 20 with verified 0.100 in pitches. Generated constraint labels were rendered
before Pattern grouping, creating oversized intermediate images. Newly inserted
constraints now remain hidden until final grouping sets their intended visibility.
The installed exact-file Apply passes in 16.86 seconds, retaining spacing chains,
Equal relationships, source constraints and units. All 96 installed regression
tests pass, plus fresh-process editing/reopening at 420 instances and the existing
desktop shortcut check. The original desktop file is unchanged. Restart the app.
Earlier GUI reproduction probes accidentally retained 20 mm pitches; the harness
now commits and asserts actual inch values. See
[correction and validation](evidence/pattern-label-allocation-20261124/README.md).
The subsequent Elements-list implementation is tracked above.

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

November 24, 2026. Owner approved batching and asked to repeat the 12-by-12 test.
The Python service batches copied geometry/constraints and linear/radial-only chain
additions, protects source/accepted Equal constraints during redundancy fallback,
and sends one native visibility update instead of redrawing per helper constraint.
The installed circle grid applies in 1.409 seconds through the service and 1.568
seconds through the task button (1.539 via the existing shortcut). All 72 installed
checks pass, plus fresh-process saved-grid diameter/pitch edits and shortcut acceptance.
Both installed file hashes match the manifest; the previous service is backed up.
Restart FreeCAD Plus to load it. Fixed-length line grids still have expensive native
redundancy checks: the additional 12-by-12 line benchmark took 57.28 seconds. No
claim of universal 1.5-second performance or changed native solver is made. See
[evidence and remaining performance limit](evidence/pattern-batching-20261124/README.md).

## Pattern/task corrections — installed

November 24, 2026. The owner approved the concrete Qt proposal with “Approved. Implement”.
Pattern fields now fit narrow docks; completed directions and visible spacing helpers
preview independently. Original size drivers feed copied Equal relationships while
projected distances preserve source freedom. Pattern and Mirror have Done on the left
(apply then close) and Apply on the right (apply then clear selections/references).
Invalid Done retains inputs; empty Done closes; Cancel discards pending work.
All 68 installed application checks, 88 native tests, five fresh-process saved-file
checks and four existing-shortcut checks pass. Six installed file hashes match the
delivery manifest; original installed files are backed up. Restart FreeCAD Plus.
See [scope, actual native screenshots and verification](evidence/pattern-corrections-20261124/README.md).

## Spacing chains and quantities — installed

November 24, 2026. Owner-approved implementation is installed. All 88 native tests,
144 installed application tests, four fresh-process file checks and two shortcut
checks pass. Saved helper identities survive process changes; hidden chains retain
their driving equations. Restart FreeCAD Plus to load the native update. See
[implementation, metadata contracts and acceptance](evidence/spacing-units-20261124/README.md).

## Sketch Pattern installed - November 24, 2026

Owner requests a dedicated Mirror-style task replacing Move / Array Transform.
Clarified counts include the original; circular spacing supports angular pitch or
total angle. Linear has one/two directions; each direction independently offers
One dimension, Two dimensions (separate forward/backward values), or Symmetric.
Circular has the same extent modes and Angular, Radial, or Angular + radial.

Owner approved the [screenshots and workflow](evidence/sketch-pattern-preview-20261124/README.md)
in chat: "approved. implement". The native tool bridge, Python task/geometry services,
reference selection, live preview, optional relative dimensions and native transactions
are implemented. Counts include the original; symmetric counts are odd, and full-circle
totals do not duplicate the endpoint. Ordinary sketch panels restore on leaving the tool.

Existing native build succeeded; 23 pattern cases and all 53 installed acceptance/
regression cases passed. The unchanged desktop shortcut passed Apply/Undo/Done;
a fresh process reopened the dimensioned native sketch with 4 source degrees of
freedom. Installed files have verified hashes and native rollback copies. See
[acceptance, limitations and screenshots](evidence/sketch-pattern-20261124/README.md).
No release or EAS/Expo build occurred. Unrelated project.previewfirst.json remains untouched.

## Compatible symmetry redundancy installed - November 24, 2026

The solver accepts compatible full/partial symmetry redundancy without removing
saved constraints. Actual conflicts and unrelated redundancy still report errors.
The existing command, appearance and selection workflow are unchanged.

Native Sketcher and dependent PartDesign builds passed, with 88 C++ tests and
39 installed checks passing (one existing upstream skip). The desktop shortcut's
fresh-process native constraint check passed. Three native modules and the new
test script are installed with hash verification and retained rollback copies.
Restart existing processes. See [implementation and evidence](evidence/constraint-symmetry-20261124/README.md).

## Sketcher symmetry workflow installed - November 23, 2026

Approved dedicated task with an enlarged scrollable Geometry list, single-line
symmetry reference and Apply/Done. Mirror opens without preselection. Apply creates
the set and stays open; Done closes only symmetry. Native sketch sections hide
during the tool and restore afterward. Click adds, Shift-click removes, and native
geometry/options/Undo remain. No automatic dimensions are introduced.

All 41 installed regression checks passed, including 12 symmetry cases and 29
related sketch regressions. The existing desktop shortcut also passed a fresh-process
check; owner config hashes are unchanged. Installed native module hash matches the build and its
previous version is retained for rollback. See [acceptance and direct screenshots](evidence/sketch-symmetry-20261123/README.md).

## Feature click/Shift-click selection installed - November 23, 2026

Approved: plain click adds eligible feature inputs once; Shift-click removes them.
Shared Extrude/Revolve, Loft, Thicken, Shell, Fillet/Chamfer/Draft and plane/sketch
placement collectors apply the rule, including History and connected/tangent picks.
Single-reference inputs clear on matching Shift-click; region and whole-sketch
edge removal preserve native mapped references. Existing list controls remain.

All 12 final focused development and 134 installed regression checks passed, plus
the existing desktop shortcut's fresh-process viewport gesture check. Eleven
payloads have verified hashes and retained rollback copies. Owner sessions/settings
and unrelated project.previewfirst.json were preserved. Restart older processes.
See [native acceptance and captures](evidence/feature-pick-20261123/README.md).

## Sketch dimension single Enter installed - November 23, 2026

Approved: one main/keypad Enter applies a valid sketch dimension and closes the
native dialog, including edits, units and arithmetic. Invalid text stays focused
and open. Native validation, Cancel and reference controls are retained.

All seven focused installed regression checks passed, covering dimension types,
Plus/Classic, selection persistence, Undo/Redo, invalid recovery and unrelated
numeric fields. A fresh process through the existing desktop shortcut also passed.
Two Python payloads were installed with hash checks and retained rollback copies;
validation used isolated profiles. No owner settings or unrelated files changed.
See [implementation and native acceptance](evidence/dimension-enter-20261123/README.md).

## Shell and shared list controls installed - November 23, 2026

Approved Shell opens empty or with invalid preselection and collects faces without
a target field or Select/Confirm toggle. Fillet/Radius, Chamfer and Draft use the
same list activation, Delete/Remove and Clear controls. Repeated picks add once;
Clear disables Use all edges. All modified workflows use component-owned inputs,
independent of Classic active Body. Shell retains native Thickness identities.

Twenty focused build checks and all 99 installed regression checks passed, plus
actual viewport picking, final-preview/list switching, fresh-process reopen/edit
and the existing desktop shortcut. Eight payloads were installed with hash checks
and retained rollback copies. Validation used isolated profiles; owner settings
and unrelated project.previewfirst.json were preserved.
See [implementation, native captures and acceptance](evidence/dressup-lists-20261123/README.md).

## Fillet selection freeze repaired and installed — November 23, 2026

Fixed a reproducible selection-notification loop when clearing Fillet edges and
picking again with curve-chain selection. Mapped seed edges are no longer toggled
twice. Plus Fillet opens whole-solid inputs with no automatic all-edge selection
and uses explicit/sole component targets independently of Classic active Body.

Eight focused build checks and all 90 installed checks passed, including actual
viewport picking, Cancel and Undo/Redo. Installed audit, fresh-process reopen/edit
and the existing desktop shortcut passed. Four payload files have rollback copies;
owner sessions/settings remain untouched. Restart older processes to load the fix.
See [repair and direct captures](evidence/fillet-20261123/README.md).


## Unified Loft installed — November 23, 2026

Owner approved the amended Solid/Sheet proposal. Shared Loft creation/editing now
offers New/Add/Subtract, ordered sections and native Loft options. Sheet forces
and locks New. Plus task entries are combined; Classic aliases dispatch to shared
Add/Subtract in component documents, independent of ambient native Body state.
Saved native Lofts retain native editing/identities. All shared target, History,
visibility, validity-color and transaction conventions apply.

Broad build suite 118 checks, expanded build Loft suite 17, installed broad suite
120 and final installed Loft suite 17 passed. Installed UI/color/drag-model audit,
binder entries, fresh-process recompute and existing shortcut verified. Ten payload
files installed with rollback/hash checks; owner sessions/settings and unrelated
project.previewfirst.json preserved. [Acceptance and direct screenshots](evidence/loft-20261123/README.md).

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

## Shell, Thicken and Modeling Surface section installed — November 23, 2026

Owner approved the combined preview and requested implementation. Surface's six
native tools and the new Thicken now share a Surface section in Modeling; the Plus
Surface tab is removed. Native Surface/Classic access remains. Thickness is named
Shell in the native command/task; existing identities/properties/labels remain.
Invalid sheets are rejected before Shell creates a feature, and declined/failed
initial task entry rolls back its transaction.

Thicken provides associative New/Add/Subtract from one sheet or connected faces,
total thickness, Along/Opposite normal/Symmetric, and Sharp/Rounded joins. It reuses
target visibility/colors, scrolling selections, History/eyes, deferred typing,
creation/editing and atomic persistence. Saved recompute is independent of active
editing context; interactive input keeps ownership and strict-order admission.

Eleven focused build and eleven final installed checks pass, in addition to the
106-case installed broad regression run (107 distinct cases overall). Installed
native UI capture, separate-process reopen/recompute and the existing shortcut
check passed. Eleven payload files have retained rollback copies. Owner sessions
and settings were preserved; existing processes need restart to load new modules.
See [implementation and direct screenshots](evidence/thicken-20261123/README.md).

## Revolve Solid/Sheet installed — November 23, 2026

Owner approved implementation. Revolve now shares Extrude's Solid/Sheet choices:
Solid defaults on; Sheet selects and locks New and clears the target. Returning
to Solid re-enables New/Add/Subtract. Native curve rotation produces uncapped
sheets; axis, angular offset, angle, reverse, symmetric/two-side and reference
controls remain. Existing saved Revolves default to Solid.

All 96 build and 96 installed regression checks passed, including eight new Sheet
Revolve tests and existing Extrude, Solid Revolve, visibility and history checks.
Native command/mouse/accept/edit, fresh-process reopen/recompute and existing
shortcut verification also passed. Six scripts installed with rollback copies.
Owner sessions/settings were preserved; existing processes need restart to load
the changes. See [evidence and installed images](evidence/revolve-sheet-20261123/README.md).

## Extrude Solid/Sheet installed — November 23, 2026

Owner approved implementation. Extrude now has Solid/Sheet on the left (Solid
default), New/Add/Subtract on the right. Sheet selects and locks New, removes any
target and produces uncapped native sheets from open or closed curves. Solid
re-enables the operations. Existing Extrudes default to Solid; Revolve is unchanged.

Ten focused build checks and all 88 installed regressions pass. Installed command,
mouse selection, double-click edit, separate-process save/reopen/recompute and
existing-shortcut checks passed. Four scripts installed with retained rollback
copies; owner sessions/settings preserved. Existing sessions need restart to load
the changes. Sheet limits currently require forward planar faces; taper requires
closed profiles and Length. See [evidence and installed screenshots](evidence/extrude-sheet-20261123/README.md).

## Selection button appearance/click repair — November 23, 2026

Owner reported the curve-intent control was dark in Light and opened only through
its arrow. It now copies the selected menu item's label/icon without inheriting
its checked state, and uses a full-button popup. Menu checkmarks and saved intent
are retained. Native Light/Dark previews preceded the repair; five build and five
installed checks passed, including icon/label/arrow clicks and native curve picking.
Two scripts installed with rollback copies. See
[evidence and installed images](evidence/selection-button-repair-20261123/README.md).

## Selection toolbar and sketch buttons installed — November 23, 2026

Owner approved both previews. Chain control now shows its current icon/name;
category filter summarizes All/omitted/only, with Select all/reset and transactional
Select 1 category replacement. Outside/Escape dismissal keeps the prior filter;
the last checkbox cannot be cleared, and older empty saved filters recover to All.
Sketch tasks now show Exit Sketch and an adjacent Cancel while an action is active.
Cancel follows one native Escape pair, including partial-step reset, in both modes.

SketcherGui and scripts built successfully. All 16 build and 39 installed regression
checks passed, along with eight installed visual cases, fresh-process persistence
and existing-shortcut verification. Five installed files have retained rollback
copies. Owner sessions/settings were preserved; existing sessions need restart to
load cached code. See [implementation and screenshots](evidence/selection-sketch-controls-20261123/README.md).

## Selection toolbar preview — November 23, 2026

Owner requests named curve-intent controls, category summaries, Select all/reset,
Select 1 category replacement, and a nonempty-filter safeguard. Owner clarified
Select 1 chooses one category. Native Qt UI prototype checks passed for labels,
summaries, singleton replacement, outside/Escape cancellation, reset and final-
category protection. Geometry admission and saved preferences are disconnected.
Subsequently approved and implemented in the increment above. See
[original screenshots and scope](evidence/selection-controls-preview-20261123/README.md).

## Sketch Exit/Cancel control preview — November 23, 2026

Owner requests Exit Sketch instead of Close and an adjacent Cancel while a sketch
action is active, behaving like Escape without leaving sketch edit. Native-widget
prototype covers idle, rectangle and constraint states; Cancel preserves the open
sketch/completed geometry and Exit Sketch closes it. Automatic active-tool detection
was fixture-driven in this prototype. Subsequently approved and implemented above
with native active-handler detection.
See [preview and native implementation scope](evidence/sketch-exit-preview-20261123/README.md).

## Creation selection repair installed — November 23, 2026

Owner reported that new-component navigation left selection active and hid idle
tasks. The creation helper now clears all selection after opening History and
synchronizes tree highlights. The new component remains active; Plus Create Geometry
shows New Sketch and datum actions. No delayed clearing affects subsequent picks.
Eight focused build checks, eight installed regressions and all three installed
creation-path visual checks passed. Python-only installation retains rollback files;
the existing shortcut was verified with isolated settings. Existing owner processes
were preserved and need restart to load cached modules. See [evidence](evidence/creation-selection-20261123/README.md).

## Component creation and modeling task updates installed — November 23, 2026

Owner approved all three pending previews. New File/New Component activate the new
component and select History, including empty files and externally owned definitions;
generic factories/import/copy preserve their existing navigation. No extra instance
is placed. The Start Part/New Body task card is removed across modes. Plus single-
sketch Modeling Tools shows Extrude and Revolve; Classic retains Pad/Pocket and
Revolve/Groove, opening shared component tasks with the matching operation. Other
tools and native legacy compatibility remain intact. Future additive/subtractive
workflow migrations must consolidate Plus task entries too (e.g. Loft), as recorded
in the roadmap and development guidelines.

Eight focused build checks, **113 installed regressions**, five separate startup
checks and installed native visual checks passed. PartDesignGui and dependencies
were built/installed with original and loaded-image rollback backups. Owner sessions
were preserved; existing processes need restart to load updated modules. See
[implementation and delivery evidence](evidence/component-task-updates-20261123/README.md).

## Sketch Modeling Tools preview — November 23, 2026

Plus task mode should consolidate Pad/Pocket to Extrude and Revolve/Groove to
Revolve; Classic keeps its buttons but opens the shared workflows in component
documents. Both native prototype lists and six command-entry routes pass, with
selected-profile prefill and Cancel preservation. Historical preview, subsequently
approved and implemented above.
See [scope, screenshots and routing evidence](evidence/sketch-tools-preview-20261123/README.md).

## Remove New Body task prompts preview — November 23, 2026

Owner requests removal of all New Body Tasks starting prompts. The single Start Part
watcher registration is isolated for removal across panel modes. Native-widget
simulation checks three contexts and preserves Create Geometry. Historical preview,
subsequently approved and implemented above. See [scope and evidence](evidence/no-body-task-preview-20261123/README.md).

## New component navigation preview — November 23, 2026

Owner requests newly created components become active with Components > History
selected. Native UI-only cases for existing and empty files pass activation/tab/
ID/link checks. Historical preview, subsequently approved and implemented above.
See [preview and next implementation scope](evidence/new-component-preview-20261123/README.md).

## Prominent task errors installed — November 23, 2026

The owner approved the native amber-error preview. The shared `TaskStatus` widget is
implemented and installed for Plane/Sketch placement and Extrude/Revolve selection,
validation, preview/result and acceptance errors. It uses the approved target-field
colors, padding, semibold plain text and wrapping. Newly raised errors scroll into
view without changing focus; one bounded follow-up handles native task-group resizing.
Repeating the same error does not keep scrolling. Valid recovery restores ordinary
styling; long messages reveal their beginning. No geometry, reference, History,
visibility, document schema or task acceptance semantics changed.

All three focused native widget checks passed, followed by **122 installed regression
checks**, five separate fresh startup checks and four installed visual/recovery cases.
The tests cover focus, repeated scrolling, wrapping/literal labels, valid recovery,
queued close cleanup and the affected modeling workflows. Source/build/install hashes
match for all five Python files; original rollback files are retained. Only the
FreeCADPlusScripts target was needed. The existing shortcut launches the update with
isolated settings. Open owner sessions remain untouched and need a restart to load
their cached Python modules. The shared style is now required for future inline task
errors in DEVELOPMENT_GUIDELINES. See [implementation evidence](evidence/task-errors-20261123/README.md).

## Prominent task-error preview pending — November 23, 2026

Owner requests amber highlighting for the insufficiently prominent attachment error
and the same treatment for future implemented errors. The native UI candidate uses
the existing Extrude target palette, padding, wrapped semibold text and shared error
classification across Plane/Sketch and Extrude/Revolve. Newly raised offscreen errors
scroll into view with a bounded native-layout follow-up; successful validation clears
the highlight. All four candidate scenarios pass visibility/recovery checks and
preserve references, IDs and saved visibility. No feature task is accepted.

**Historical preview, subsequently approved and implemented above.**
Session `16176df60dd2`, fingerprint
`4f5aa46a46bf63433fa196c22609ad24163c52d38805f2ac1a0544c6c4581511`.
See [screenshots, candidate sources and implementation scope](evidence/task-error-preview-20261123/README.md).
The preview preserves owner sessions and untracked `project.previewfirst.json`.

## Attach Sketch sequential-order repair — November 23, 2026

Owner clarified the failing route is the Attach Sketch button (`Sketcher_MapSketch`).
The native command checked cycles but not History position before support assignment;
the resulting dependency sort could then silently move the sketch after a later plane.
The command now checks the chosen existing sketch against the original selection
before attachment modes and again before changing support. Sketch support-property
picks share the guard. Rejection preserves support, map mode, placement, order and
Undo count and says to reorder History, then try again. Explicitly moving the plane
before the sketch permits retry. Classic documents retain their native behavior.

Native FreeCADGui/SketcherGui and dependencies were rebuilt and installed with
source/build/install hashes and retained original/loaded-image backups. All 67 focused
build checks and 217 installed regressions passed, including the actual native command,
reorder/retry, Undo/Redo, managed sketch task, support-property rejection and classic
document compatibility. Five separate startup checks also passed. The installed
fresh-process warning was captured and inspected.
See [repair evidence](evidence/sketch-attachment-order-20261123/README.md).

The owner's regular-profile process (PID 21716 during installation) was preserved;
its loaded libraries remain backed up. **Save and restart that session to load the
native fix.** Validation and the separate shortcut launch use isolated profiles.
Unrelated `project.previewfirst.json` remains untouched. Installation briefly created
one module at the build-style location; it was hash-verified and moved into backup,
then all twelve final installed outputs were verified at their actual runtime paths.

## Plane/Sketch placement and History reordering installed — November 23, 2026

Owner approved both previews: "implement the plane and sketch placement as well as
the reordering of the history tab". Both are implemented and installed. Compatible
plane picks accumulate; conflicts replace the defining set. Plane/face,
line/straight-edge and point/vertex inputs are interchangeable. New line+point
construction is through the point, normal to the line. Older saved containing-plane
geometry is preserved by an additive construction flag, including on Cancel/open.

History keeps Coordinate System first and fixed. One-feature drags persist a preferred
order while retaining all transitive dependencies. Invalid moves are corrected before
the first consumer (or after the last input), with a popup naming the blocker.
Source-owned transactions support Undo/Redo; native links, ownership and geometry
remain unchanged. Active tasks/transactions and stale drag contexts are refused.

Validation: 62 focused build tests passed. The installed broad suite passed 212 of
213; its remaining external-source fixture was corrected and passed separately,
giving 213/213 covered checks. Five separate fresh startup checks also passed, and
the final installed focused rerun passed 63/63 after a helper-text correction.
Installed Qt drop/popup and native selection fixtures passed, plus fresh-process
save/reopen of order, identities, new construction and legacy geometry. OS-level
mouse drag could not be checked: both computer-control tools failed to attach to
the isolated FreeCAD window with the same window-owner mismatch. This is a tooling
limitation, not a claimed mouse-test pass. See [full evidence](evidence/plane-history-20261123/README.md).

Scripts were installed with source/build/app hash matching and retained rollback
backups. The existing desktop shortcut launched the update with isolated settings.
Unrelated `project.previewfirst.json` remains untouched. No native rebuild was needed.

## History drag-reorder preview — November 23, 2026

The owner requests a fixed first Coordinate System, all defining inputs before their
consumers, and manual drag ordering within those constraints. Dropping an input after
a dependent must put it immediately before its first dependent and show a naming/
explanation popup. The [native UI proposal](evidence/history-reorder-preview-20261123/README.md)
demonstrates a valid independent move, a support plane moved back before its sketch,
and an extrusion kept after its input sketch. Three Qt drop-event cases pass; the
coordinate subtree is non-draggable. Native IDs, visibility, references and model order
remain unchanged. Direct [corrected History](evidence/history-reorder-preview-20261123/corrected-order.png)
and [popup](evidence/history-reorder-preview-20261123/cannot-move-after.png).

**Historical preview, subsequently approved and implemented above.** Session
`661e846aab01`, fingerprint `ae4db163f725c584d967a4f790112838a342f4fe6d8c363df4a8a47528357acf`.
The candidate uses explicit specimen order outcomes. Persistent preferred ordering,
dependency clamps, transaction handling and complete native drag validation remain
implementation work at that preview stage. The owner subsequently approved both.

## Plane selection preview — November 23, 2026

The owner requests matching reference collection for datum planes and sketch planes:
compatible picks accumulate; a conflicting pick replaces the prior defining set.
XY→XZ should leave only XZ. Line+point defines a plane through the point normal to
the line. Planes/planar faces, lines/straight edges and points/vertices are equivalent.
The [native UI proposal](evidence/plane-selection-preview-20261123/README.md) passes
all 16 specimen UI-state checks across both tasks, with unchanged IDs/visibility
after Cancel. Screenshots: [replacement](evidence/plane-selection-preview-20261123/replace-plane.png),
[coplanar lines](evidence/plane-selection-preview-20261123/coplanar-lines.png),
[normal through point](evidence/plane-selection-preview-20261123/normal-through-point.png),
[flat face](evidence/plane-selection-preview-20261123/planar-face.png).

**Historical preview, subsequently approved and implemented above.** Session
`cc6496002256`, fingerprint `3dd056488e4bcc7aa4487ac6d0a28129621057edb87b8311af39e40803862ea5`.
The two UI candidate files use fixture collection/placement callbacks. Production
work must preserve old saved line-plus-point containing-plane geometry when adding
the new normal-through-point semantics. See the evidence's implementation scope.

## Target selection and coordinate-system persistence — November 23, 2026

The owner approved and both changes are implemented and installed. Extrude/Revolve
Add/Subtract select the sole eligible current solid automatically, preserving a valid
existing target. Otherwise Target solid receives the approved amber highlight and
inline guidance, without a popup. Profile/region picking and acceptance require a
target. Deliberate Clear persists through numeric/preview updates. Hidden targets
use the existing selected-solid display while History eyes remain unchanged.

The base native Coordinate System, Origin point, axes and planes now have document-level
deletion protection in Plus files, in addition to their native GUI veto. Existing files
gain protection without migration or replacement objects. Visibility, native identities,
whole-owner deletion, Undo/Redo and cancellation remain intact; custom datums and legacy
documents retain their existing behavior. File and backend Body frames are protected too.

Validation: all 16 focused build checks, 202 installed regression tests and 5 separate
fresh-startup tests passed. Twelve installed UI cases cover zero/one/two targets across
both tools and Add/Subtract. A fresh process reopened the saved file and rejected all
24 frame-object deletion attempts without changing IDs or visibility. The app was
restarted through the existing desktop shortcut using explicitly isolated settings;
rollback copies are retained. No owner-profile process was running during installation.

Direct installed screenshots: [multiple solids](evidence/target-coordinate-20261123/multiple-solids.png),
[sole solid](evidence/target-coordinate-20261123/sole-solid.png),
[no solid](evidence/target-coordinate-20261123/no-solid.png),
[Revolve](evidence/target-coordinate-20261123/revolve-target.png).
See [implementation/build/installed evidence](evidence/target-coordinate-20261123/README.md).

## Target highlighting and sole-solid preview — November 23, 2026

The owner revised the unapproved popup to field highlighting and automatic choice
of the sole body. The native Extrude/Revolve candidate selects one available solid;
multiple candidates get a focused amber Target solid field with inline guidance;
zero candidates get an inline explanation. No modal dialog appears.
All 12 fixture UI cases (zero/one/two candidates, both features and Add/Subtract)
rendered as intended, including unchanged hidden-target eyes and restoration of
native IDs/visibility after Cancel. The renderer supplies candidate lists; actual
eligibility enumeration and full intake/lifecycle guards are pending implementation.
Direct [multiple solids](evidence/target-highlight-preview-20261123/multiple-solids.png),
[sole solid](evidence/target-highlight-preview-20261123/sole-solid.png),
[no solid](evidence/target-highlight-preview-20261123/no-solid.png).
**Subsequently approved and implemented with coordinate-system persistence above.**
See [scope/provenance](evidence/target-highlight-preview-20261123/README.md).

## Target-first Add/Subtract prompt preview — November 22, 2026

The owner requests a missing-target error before selecting profile curves in Add/
Subtract. A native candidate shared by Extrude/Revolve shows the immediate popup
and focuses Target solid after OK. All four mode/feature combinations show it;
preview updates and modes with an existing target do not repeat it. Document IDs
remain unchanged. Direct [Add popup](evidence/target-first-preview-20261122/add-popup.png),
[Subtract popup](evidence/target-first-preview-20261122/subtract-popup.png), and
[target focus](evidence/target-first-preview-20261122/target-focus.png).
**Superseded by the November 23 field-highlight/sole-solid proposal above. Do not implement the popup.**
The candidate is a UI demonstration; direct command startup, intake guards,
cleared/invalid target handling and complete dialog lifecycle are implementation work.
See [preview provenance and scope](evidence/target-first-preview-20261122/README.md).

## Strict sequential History — November 22, 2026

The owner approved strict sequential History and preventing sketches or other inputs
from appearing after their consumers. The production projection now orders native
dependencies across Body boundaries, including expression links and Body result
references, with creation IDs breaking independent ties. Profiles stay before their
Extrude/Revolve operations. Existing saved graphs display in dependency order without
rewriting their geometry, ownership, visibility, identity or schema.

Shared input admission rejects later/self inputs before supported editor mutations.
It covers Extrude/Revolve, sketch placement, planes and the native modeling input
paths. Coordinate layout/eyes and other tabs are retained. No drag-reorder action
was introduced; future ordering actions must obey predecessor constraints.
See [technical contract](ARCHITECTURE.md#creation-editing-and-history) and
[implementation evidence](evidence/sequential-history-20261122/README.md).

All **28 targeted development checks** and **165 unique installed native checks**
passed. Six conversion checks initially encountered existing test destinations;
all nine conversion checks passed in a fresh directory. Five startup/UI-mode checks
ran in a separate fresh process. [Aggregate acceptance](evidence/sequential-history-20261122/acceptance.json)
retains the original run and verifies every failed case has a passing retry.
Separate installed processes confirmed [actual History order and input clicks](evidence/sequential-history-20261122/visual.json)
and [fresh reopen](evidence/sequential-history-20261122/reopen.json), preserving IDs and volumes.
Reviewed [installed screenshot](evidence/sequential-history-20261122/history.png).
The Python payload is installed with rollback copies and matching source/build/app hashes.
The existing shortcut launched and verified a separate isolated updated instance;
disposable fixtures were removed, retaining rollback and the active profile.
The owner's already-open window still contains an unsaved Unnamed document and was
left untouched; that older process needs a restart after the owner saves it.
Unrelated project.previewfirst.json remains untouched.

## History coordinate icons and collapsed defaults — November 22, 2026

The owner approved the direct native preview with **"implement"**. Axes/Planes now
use their children's native icons. Coordinate System and descendants start collapsed;
ordinary refreshes preserve manual expansion choices. Source and installed payload
match the approved candidate. All **14 existing native panel/History checks passed**,
including eyes, task-time clicks, selection, Undo, source ownership and saved visibility.
A separate installed process confirmed defaults, identical icon images, preserved
manual expansion and unchanged geometry visibility. Reviewed installed screenshots:
[default](evidence/history-icons-20261122/default.png),
[root opened](evidence/history-icons-20261122/groups.png),
[child icon comparison](evidence/history-icons-20261122/children.png).
See [implementation evidence](evidence/history-icons-20261122/README.md) and
[preview provenance](evidence/history-icons-preview-20261122/README.md).
The Python payload was refreshed and installed with rollback retained. The existing
desktop shortcut was restarted and verified with isolated user/system/data paths;
the app remains open. Disposable validation fixtures and inactive profiles were removed.
The owner profile and unrelated project.previewfirst.json were untouched.

## Unified Revolve implementation — November 22, 2026

The owner approved: **"implement the expanded selection list and revolves"**.
The shared Extrude/Revolve profile list now reserves at least five complete native
rows and scrolls through every selection, including long labels and larger fonts.
Revolution and Groove commands share the feature-centered Revolve task with New Solid,
Add and Subtract, axis selection/guide, degree-based start/end offsets and rotation
angles, symmetric/two-sided sweeps, shared target visibility/colors and History scope.
History editing uses the same populated task and retains feature identity.

Source, native build and installation are complete, with rollback retained:
[manifest](evidence/revolve-implementation-20261122/install-manifest.json).
All **11 focused development-build checks** and **188 installed native tests** passed:
[focused](evidence/revolve-implementation-20261122/build-regression.txt),
[installed](evidence/revolve-implementation-20261122/regression.txt).
Separate installed processes passed five native operation/validity visual cases,
actual History target clicks, both expanded lists, atomic invalid rejection and
fresh saved-file reopening with identities and prefilled angular parameters intact:
[visual](evidence/revolve-implementation-20261122/visual.json),
[reopen](evidence/revolve-implementation-20261122/reopen.json).
Reviewed live screenshots: [Revolve list/axis](evidence/revolve-implementation-20261122/overview.png),
[angular controls](evidence/revolve-implementation-20261122/add-valid.png),
[Extrude list](evidence/revolve-implementation-20261122/extrude-selections.png).
See [evidence](evidence/revolve-implementation-20261122/README.md).
The existing desktop shortcut was restarted and verified with isolated user/system/
data paths: [launch](evidence/revolve-implementation-20261122/shortcut.json). The app
remains open. Disposable test files and inactive profiles were removed after acceptance;
rollback copies and the active shortcut profile are retained. The owner profile was
never used, and unrelated project.previewfirst.json remains untouched.
The native limitation is explicit: To first/To last remain disabled; angular reference
starts/limits require a plane through the axis. Legacy native editors are preserved.

## Unified Revolve preview — November 22, 2026

The owner requested Extrude's workflow for New Solid/new body, Add and Subtract
Revolve, combining Revolution/Groove and replacing linear offset/distance with
angular offset/rotation about an identified axis. The native staged proposal is
ready: [profile list and axis](evidence/revolve-workflow-preview-20261122/overview.png),
[angular controls and Add](evidence/revolve-workflow-preview-20261122/add-valid.png),
[Subtract](evidence/revolve-workflow-preview-20261122/subtract-valid.png).
It includes the still-pending larger selection list from the preceding request.
All five native BRep fixture cases (New Solid, Add valid/invalid, Subtract valid/invalid)
passed the preview's geometry/visibility assertions; invalid cases disable OK.
These are native staged screenshots, not an implemented Revolve task or regression
coverage for persistence/selection/editing. The baseline is installed Extrude as the
shared-layout reference. **Subsequently approved; see implementation status above.**
At preview capture, production source and installed files were unchanged. See the
[preview record](evidence/revolve-workflow-preview-20261122/README.md) for provenance,
limitations and the subsequent implementation/validation scope.

## Shared display rule and selected-curves preview — November 22, 2026

The owner's instruction to carry selected-target visibility and additive/subtractive
validity colors into future similar feature workflows is now recorded in
[Task panel](ui-ux-specs/TASK_PANEL.md#shared-selected-target-and-validity-display--november-22-2026)
and the development guidelines. This documents future acceptance requirements; it
does not retrofit unrelated workflows.

The owner also requested at least five visible selected-curve rows with scrolling
or expansion. A native staged Extrude list preview is ready for chat approval:
[top](evidence/extrude-selection-preview-20261122/proposed-top.png),
[scrolled to the final selection](evidence/extrude-selection-preview-20261122/proposed-scrolled.png).
It shows six complete rows at the current native font, satisfying the five-row
minimum, and scrolls through all eight selected edges. The real Extrude remains valid.
The [preview record](evidence/extrude-selection-preview-20261122/README.md) identifies
the isolated candidate and exact fingerprint. **Subsequently approved with Revolve;
see implementation status above.**

## Extrude selected targets and validity colors — November 22, 2026

The owner [approved the native screenshot preview](evidence/extrude-validity-20261122/approval.json).
Selecting a hidden Add/Subtract target in History now displays it in the configured
selection color without changing its History eye. It is opaque while picking the
target and translucent after leaving that field. Already-visible targets keep native
face/edge picking. The target display remains available with Show preview or automatic
preview updates off, and clears when the target or operation no longer needs it.

Add tools are green when valid and yellow when invalid; Subtract tools are red when
valid and pink when invalid. Invalid final operations retain their actual native tool
for display, report the error and cannot be accepted. Invalid Result display falls
back to that colored tool. Malformed inputs clear stale tool geometry. Saved source
visibility, materials and native transaction behavior remain intact.

Four Python files were built and installed with matching source/build/app hashes
and retained rollback copies: [manifest](evidence/extrude-validity-20261122/install-manifest.json).
All **8 focused build tests** and **177 installed native tests** passed with no
failures/errors: [focused report](evidence/extrude-validity-20261122/build-regression.txt),
[installed report](evidence/extrude-validity-20261122/regression.txt).
Separate installed processes passed actual History-click selection, all four colors,
valid acceptance, invalid atomic rejection and fresh saved-file reopening:
[visual results](evidence/extrude-validity-20261122/visual.json),
[reopen results](evidence/extrude-validity-20261122/reopen.json).
Reviewed installed screenshots: [selected target](evidence/extrude-validity-20261122/installed-target-selected.png),
[valid Add](evidence/extrude-validity-20261122/installed-add-valid.png),
[invalid Add](evidence/extrude-validity-20261122/installed-add-invalid.png),
[valid Subtract](evidence/extrude-validity-20261122/installed-subtract-valid.png),
[invalid Subtract](evidence/extrude-validity-20261122/installed-subtract-invalid.png).

The existing desktop shortcut was restarted and verified against the installed app
with isolated user/system/data paths: [launch check](evidence/extrude-validity-20261122/shortcut.json).
The app remains open. Disposable fixtures and inactive profiles were removed; rollback
copies and the active isolated profile remain under runtime validation/extrude-validity-20261122.
The owner profile was never used.

## View fitting after sketch exit — November 22, 2026

The owner [approved the direct native preview](evidence/sketch-exit-fit-20261122/approval.json).
Leaving a new or existing nonempty sketch now fits the visible model to include the
whole sketch, retaining the normal post-exit camera orientation. Fitting follows
native camera, coordinate visibility and task cleanup. It preserves object visibility,
selection, History restoration, geometry, constraints and native transactions.
Empty/deleted sketches, cancelled placement, replacement editors and closed views
or documents do not cause a stale camera adjustment.

The panel and regression module were built and installed with source/build/app
hash verification and retained rollback copies:
[manifest](evidence/sketch-exit-fit-20261122/install-manifest.json).
Seven focused native build cases passed:
[report](evidence/sketch-exit-fit-20261122/build-regression.txt).
All **169 installed native tests** passed with no failures/errors:
[report](evidence/sketch-exit-fit-20261122/regression.txt).
Separate installed processes passed the actual Close-button/large-sketch visual
check and saved-sketch reopening with axonometric orientation retained:
[visual result](evidence/sketch-exit-fit-20261122/visual.json),
[reopen result](evidence/sketch-exit-fit-20261122/reopen.json).
The reviewed [installed exit screenshot](evidence/sketch-exit-fit-20261122/installed-exited.png)
shows the complete rectangle after fitting, matching the approved native preview.

The existing desktop shortcut was restarted and verified with isolated user/system/
data paths: [launch check](evidence/sketch-exit-fit-20261122/shortcut.json).
The app remains open. Rollback copies and the active isolated profile remain under
runtime validation/sketch-exit-fit-20261122. Disposable test fixtures and inactive
profiles were removed after acceptance; the owner profile was never used.

## Sketch coordinate-system visibility — November 22, 2026

The owner [approved the native preview](evidence/sketch-coordinate-visibility-20261122/approval.json)
for hiding the Coordinate System when opening a sketch. New sketch drawing and
existing sketch editing now hide the component Origin, axes and planes temporarily.
New Sketch plane selection still shows planes; Sketcher's red/green drawing axes
remain visible. Exit restores prior display. History eyes remain usable, and explicit
eye choices retain native accept/abort/Undo semantics. Other geometry stays unchanged.

The implementation masks native render switches rather than Visibility properties,
keeping automatic hiding outside document transactions and saved files. It covers
body-owned sketches, external source components, panel disposal and context/document
closure. No C++ build, schema change or preference override was required.

Three Python files were built and installed with matching source/build/app hashes
and retained rollback copies: [manifest](evidence/sketch-coordinate-visibility-20261122/install-manifest.json).
All **162 development-build tests** passed: [report](evidence/sketch-coordinate-visibility-20261122/build-regression.txt).
The final installed suite also passed **162 tests**, with no failures/errors:
[report](evidence/sketch-coordinate-visibility-20261122/regression.txt).

Separate installed processes passed real rectangle drawing, saved geometry and
constraint identity, coordinate hiding/restoration, History tab restoration, and
reopening an existing sketch: [GUI check](evidence/sketch-coordinate-visibility-20261122/visual.json),
[reopen check](evidence/sketch-coordinate-visibility-20261122/reopen.json).
Reviewed native screenshots: [plane selection](evidence/sketch-coordinate-visibility-20261122/installed-placement.png),
[drawing](evidence/sketch-coordinate-visibility-20261122/installed-drawing.png),
[after exit](evidence/sketch-coordinate-visibility-20261122/installed-after.png).

The existing desktop shortcut was restarted and verified against the installed
payload with isolated user/system/data settings, without using the owner profile:
[launch check](evidence/sketch-coordinate-visibility-20261122/shortcut.json).
The restarted app remains open. Rollback copies and its isolated profile are retained
under runtime validation/sketch-coordinate-visibility-20261122; disposable test
fixtures and inactive validation profiles were removed after acceptance.

## Sketch dimensions and feature-task History — November 22, 2026

The owner [approved both changes](evidence/sketch-task-behavior-20261122/approval.json)
after the direct native storyboard. Mouse-only sketch creation no longer adds
unsolicited dimensions. Applicable geometric constraints remain; deliberate typed
sizes and explicit dimension commands still work, and existing dimensions survive
edit entry. The fix drains programmatic QuantitySpinBox notifications while their
signal blocker is active; it does not delete constraints or disable auto-constraints.

Entering feature creation/edit selects Components History and leaving restores the
previous Models/Part Tree/History tab. Sketch placement-to-drawing keeps one saved
tab. Manual browsing during a task remains possible. Custom Sketch/Plane/Extrude,
native feature/datum editors, and standalone Part creation dialogs share the scope.
External-source tasks, context/document teardown and failed native entry clean it up.

The native build passed. Five changed Python modules/tests and FreeCADGui.dll were
installed with source/build/app hash checks and retained rollback copies:
[manifest](evidence/sketch-task-behavior-20261122/install-manifest.json).
Nine focused build cases passed. The final installed suite passed **155 tests** with
no failures/errors: [report](evidence/sketch-task-behavior-20261122/regression.txt).
Coverage includes actual mouse-only Rectangle/Circle/Line/Arc, deliberately typed
on-view dimensions, existing dimensions/Undo/Redo, all prior tabs, manual browsing,
sketch handoff, native Part dialogs, external sources, and existing Extrude, Sketch,
Plane, visibility, numeric commit, Move and Rotate workflows.

Separate installed processes passed real rectangle creation, History transitions,
save/reopen and existing-sketch edit restoration without injected product code:
[GUI check](evidence/sketch-task-behavior-20261122/visual.json),
[reopen check](evidence/sketch-task-behavior-20261122/reopen.json).
Reviewed native captures: [placement](evidence/sketch-task-behavior-20261122/installed-placement.png),
[drawing](evidence/sketch-task-behavior-20261122/installed-drawing.png),
[previous tab restored](evidence/sketch-task-behavior-20261122/installed-after.png).

The existing desktop shortcut was restarted and verified against the installed
payload using explicit isolated user/system/data paths; no owner profile was used:
[shortcut check](evidence/sketch-task-behavior-20261122/shortcut.json).
The restarted app remains open. Rollback backups and its isolated profile remain
under the development runtime's validation/sketch-task-behavior-20261122 directory.

## Extrude visibility and shared tree controls — November 22, 2026

The owner [approved the direct native storyboard](evidence/extrude-visibility-20261122/approval.json)
and requested implementation. History eyes and Part Tree visibility remain usable
through shared feature workflows, including native editors, without accepting or
replacing their active transactions. Extrude entry hides unusable geometry without
revealing hidden eligible inputs. Edit entry shows only profile and target geometry.
Visible solids become translucent, opaque while choosing a target, and use the
configured selection color for the target. Leaving the target field restores its
translucency while keeping that color. Automatic display/material changes restore
on exit/save; explicit eye choices remain undoable. Planar solid/sheet face profiles
are associative; nonplanar faces report the native planar-profile limitation.

The native build passed and 14 changed modules/tests plus the Gui library (15 files
total) were installed with verified hashes and retained rollback copies:
[manifest](evidence/extrude-visibility-20261122/install-manifest.json).
Temporary appearance changes honor NoModify in the native geometry provider;
transient visibility also guards group/link notification properties. No false dirty
flag or temporary material survives opening/cancelling the task or saving during it.

The focused build suite passed 25 cases. The final installed suite passed **134 tests**
with no failures/errors, covering Extrude, Sketch, Plane/datum tasks, shared tree
visibility, external sources, component visibility, Move and Rotate:
[report](evidence/extrude-visibility-20261122/regression.txt).
Fixture corrections account for managed-dock disposal, visible origin defaults and
native focus settling; these do not change those workflows' product behavior.

Separate installed processes passed actual viewport target picking and History eye
clicks, display/material restoration, planar face previews, and saved face/downstream/
external-source reopening and recompute:
[GUI results](evidence/extrude-visibility-20261122/visual.json),
[reopen results](evidence/extrude-visibility-20261122/reopen.json).
Reviewed native captures: [new](evidence/extrude-visibility-20261122/installed-new.png),
[target](evidence/extrude-visibility-20261122/installed-target.png),
[leaving target](evidence/extrude-visibility-20261122/installed-leave-target.png),
[edit](evidence/extrude-visibility-20261122/installed-edit.png).

All checks use isolated settings. The app was restarted through the existing
`freecad plus 0.1.0.lnk`, verifying its launcher, working directory, installed modules
and explicit isolated config/data paths; the restarted app remains open:
[shortcut check](evidence/extrude-visibility-20261122/shortcut.json).
Rollback backups and the active isolated shortcut profile remain in the development
runtime's validation/extrude-visibility-20261122 directory.

## Coordinate System History — November 22, 2026

The owner approved the [direct native preview](evidence/coordinate-history-20261122/approved.png)
and requested implementation in [chat](evidence/coordinate-history-20261122/approval.json).
History now contains Coordinate System → Origin, Axes → X/Y/Z Axis, and Planes →
XY/XZ/YZ Plane. All rows keep far-left eyes, including each individual datum.
Group eyes hide all visible members or show all hidden/mixed members, using a
mixed-state eye. Origin is the existing native App::Point at local (0,0,0).
New-component creation enables all seven native frame objects. Existing saved
visibility, native identities, geometry and file-level History remain intact.

The native build passed. Six changed Python modules/tests were installed into the
existing development payload with rollback backups and matching source/build/app
hashes: [manifest](evidence/coordinate-history-20261122/install-manifest.json).
Validation uses disposable profiles, never the owner profile. The existing desktop
shortcut still targets the development launcher and working directory.

The final native suite passed **63 tests**, covering History projection, real group
and individual clicks, mixed states, one-step Undo/Redo, external source ownership,
creation defaults, saved visibility, sketch placement/cancellation/drawing,
component hierarchy, native creation and existing feature workflows.
See [report](evidence/coordinate-history-20261122/coordinate_history_regression.txt).
Initial broader-suite failures exposed test assumptions: managed docks hide rather
than dispose on close, replacement fixtures must retain managed status, numeric
focus must settle before typing, and conversion fixtures require fresh destinations.
Those test setup issues were corrected without changing product behavior.

A separate installed process checked saved hidden groups, external source visibility,
and real group/individual clicks, and captured the shipped UI without code injection:
[checks](evidence/coordinate-history-20261122/coordinate_history_installed.json),
[shown](evidence/coordinate-history-20261122/installed-shown.png),
[planes hidden](evidence/coordinate-history-20261122/installed-planes-hidden.png),
[individual plane](evidence/coordinate-history-20261122/installed-one-plane.png).
Task-generated disposable files are removed after preserving evidence; installation
rollback copies remain in validation/coordinate-history-20261122/install-backup.

## Design toolbar layout — November 22, 2026

The owner approved the nine native Design-tab previews and explicitly requested
removing unnecessary right-hand space in those renders before implementation.
This was a preview correction, not a reported spacing defect in the installed app.
See [chat approval](evidence/toolbar-layout-20261122/approval.json) and the
[UI contract](ui-ux-specs/TOOLBARS_AND_BUTTONS.md#bordered-controls-and-separate-dropdown-columns--november-22-2026).
The finalized isolated candidate was captured again in both themes before delivery;
no Companion approval state was written on the owner's behalf.

`toolbars.py` now draws an outer icon border, reserves a distinct right arrow area,
and partitions buttons stably within existing logical subgroups. Standard Constraints
dropdowns occupy one column. One-pixel section dividers appear between groups.
The spacing correction removes forced 82-pixel large-caption widths, stops grid
columns stretching into spare label space, centers large icons over captions and
keeps internal separators narrow. Natural button widths are retained when the page
scrolls, preventing icon/arrow compression. Native actions, menus, Classic widgets,
selection semantics and feature tasks remain in their existing owners.

The [native build](evidence/toolbar-layout-20261122/native-build.log) passed; a final
FreeCADPlusScripts build copied the two Python files. Source/build/payload hashes
match in the [install manifest](evidence/toolbar-layout-20261122/install-manifest.json).
Only `toolbars.py` and `TestPlusToolbars.py` were installed into the current owner
payload. Rollback copies remain under its validation/toolbar-layout-20261122/
install-backup directory. The existing
[desktop shortcut](evidence/toolbar-layout-20261122/shortcut.json) still targets the
same development launcher and working directory; the owner profile was not used.

All **13 installed native regression cases passed** with zero failures/errors:
[report](evidence/toolbar-layout-20261122/toolbar_layout_regression.txt),
[result](evidence/toolbar-layout-20261122/toolbar_layout_regression.json).
Coverage includes all nine tabs in Light/Dark at 1300/1000 logical pixels, arrow
space, compact columns, Constraints grouping, complete captions at increased font
size, real mouse menu/main clicks, last choice across rebuild, disabled-main/enabled-
alternative behavior, theme backgrounds, dynamic/custom toolbars, Classic restore,
Spreadsheet widgets and BIM status ownership. Initial new assertions incorrectly
treated generic Qt style subcontrol/hit-test results as QToolButton's click routing;
the final check uses its reserved menu rectangle, with real clicks verified by the
existing interaction cases. The narrow-page check also caught actual split-button
compression, corrected by retaining natural button widths before installation.

The [final preview checks](evidence/toolbar-layout-20261122/spacing-preview-checks.json)
record all 18 tab/theme captures and zero mixed button-type columns. Geometry,
document behavior and unrelated feature workflows were not changed by this task.

Independent installed-app [restart verification](evidence/toolbar-layout-20261122/toolbar_persist_verify.json)
passed after a separate process saved the isolated profile. Saved Plus choices,
selection preferences and Classic visibility survived. A further fresh installed
process, without candidate-code injection, passed actual Circle/Ellipse menu and
main-icon clicks and captured all nine tabs in both themes:
[checks](evidence/toolbar-layout-20261122/installed.png.json).
All nine installed screenshot sheets are byte-identical to the final candidate
[comparison](evidence/toolbar-layout-20261122/installed-preview-comparison.json).
Direct installed captures:
[Home](evidence/toolbar-layout-20261122/installed-home.png),
[Modeling](evidence/toolbar-layout-20261122/installed-modeling.png),
[Sketch](evidence/toolbar-layout-20261122/installed-sketch.png),
[Surface](evidence/toolbar-layout-20261122/installed-surface.png),
[Assembly](evidence/toolbar-layout-20261122/installed-assembly.png),
[Mesh](evidence/toolbar-layout-20261122/installed-mesh.png),
[View](evidence/toolbar-layout-20261122/installed-view.png),
[Part](evidence/toolbar-layout-20261122/installed-part.png),
[All Tools](evidence/toolbar-layout-20261122/installed-all-tools.png).

## Extrude rendering and sketch visibility correction — November 22, 2026

The owner reported triangular side shading in a rectangle extrusion preview and
existing geometry disappearing on entering a subsequent sketch. Both reproduced
in an isolated native fixture. After reviewing the two direct screenshots, the
owner explicitly replied "Approve both corrections"; see
[approval](evidence/render-visibility-fix-20261122/approval.json) and the
[UI contract](ui-ux-specs/TASK_PANEL.md#extrude-rendering-and-sketch-visibility-correction--november-22-2026).

Extrude now declares solid face winding/culling and uses sorted-triangle transparency
for its preview. The diagonal rear-face artifacts are removed while geometry,
controls, colors, material opacity and tool-overlay behavior remain unchanged.

Native component sketch entry no longer automatically hides dependents or reveals
supports/external geometry. The failure was in the definition's rendered
LinkVisibility, despite unchanged feature Visibility flags and open History eyes.
Both new and existing component sketches now preserve those states. No saved
visibility-automation properties or preferences are rewritten. Ordinary documents
retain native automation; native camera/editor behavior and History eye changes
remain functional.

The [native build](evidence/render-visibility-fix-20261122/native-build.log) and
[final incremental build](evidence/render-visibility-fix-20261122/final-build.log)
succeeded. The focused 12 cases passed, followed by all **107 installed regression
checks**, zero failures/errors:
[report](evidence/render-visibility-fix-20261122/render_fix_regression.txt).
New coverage compares both saved and rendered visibility on features/containers,
new/existing sketches, hidden support/external geometry, external source/host
contexts, History changes, Undo and unchanged ordinary-document automation.

The [installed GUI check](evidence/render-visibility-fix-20261122/render_fix_visual.json)
verified the rectangle's unchanged volume/preview Undo and the prior visible sketch,
visible solid and hidden reference through native drawing. Inspected captures:
[corrected Extrude](evidence/render-visibility-fix-20261122/installed-extrude.png),
[preserved sketch visibility](evidence/render-visibility-fix-20261122/installed-sketch.png).
The [fresh-process check](evidence/render-visibility-fix-20261122/render_fix_reopen.json)
passed for re-entered sketch visibility, persisted IDs, local/external extrusion
geometry and dependents, History visibility and datum editing.

Three payload files were backed up and installed with verified hashes:
[manifest](evidence/render-visibility-fix-20261122/installation.json).
The existing desktop shortcut still targets this app; owner profile/documents and
the unrelated untracked `project.previewfirst.json` remain untouched. Restart the
app to load the updated native Sketcher library.

## Design interaction implementation — November 22, 2026

The owner approved all three direct previews together: automatic sketch planes
and History visibility, four Design task actions, and immediate numeric arrow
updates. These changes are implemented in the installed development app.

New Sketch temporarily reveals the edited component's XY/XZ/YZ planes. Automatic
changes restore on completion, Cancel, context change and document close without
creating objects, Undo records or a dirty document. Explicit History choices persist
and remain undoable. History eyes work during placement and native sketch drawing;
drawing changes join the existing sketch transaction without ending the editor.
Source-owned visibility and the original occurrence context are preserved.

With an editable component and no selection/operation, Design offers New Sketch,
Datum Plane, Datum Line and Datum Point. Line/Point use their native attachment
creation/editing tasks and belong directly to the component; no Body is introduced.
Their native editors now close cleanly after acceptance or cancellation in component
documents. Classic/native document watchers retain their existing behavior.

Typing numeric values still waits for field leave. Ordinary Qt spin editors,
shared Plane/Sketch/Extrude numeric controls and native QuantitySpinBox publish
explicit arrow steps immediately while focused. A later blur does not repeat the
same update. Automatic preview off remains manual; InputField expression handling
is unchanged.

The native rebuild succeeded. All **103 installed regression checks passed**:
[report](evidence/design-interactions-20261122/design_regression.txt),
[result](evidence/design-interactions-20261122/design_regression.json).
Coverage includes geometry/targets, sketch preselection/placement, native drawing,
local/external source ownership, datum create/edit/Cancel, visibility Undo/Redo,
document cleanup, typed-versus-stepped values and manual preview.
The [fresh-process check](evidence/design-interactions-20261122/design_reopen.json)
passed for extrusion identity/dependents, external geometry, saved History visibility
and component datum reopen/edit/Cancel.

The [installed UI exercise](evidence/design-interactions-20261122/design_visual.json)
verified the exact four idle links and selection guard, command-opened sketch planes,
real History clicks and focused numeric steps. Inspected screenshots show
[Design idle](evidence/design-interactions-20261122/installed-design-idle.png),
[automatic planes](evidence/design-interactions-20261122/installed-sketch-planes.png),
[History hiding](evidence/design-interactions-20261122/installed-sketch-history-hidden.png),
[typed value](evidence/design-interactions-20261122/installed-numeric-typing.png), and
[arrow-up preview](evidence/design-interactions-20261122/installed-numeric-arrow.png).
These are working installed functionality, separate from the approved simulations.

Eleven payload files were backed up, installed and hash-verified:
[manifest](evidence/design-interactions-20261122/installation.json).
The unchanged [desktop shortcut](evidence/design-interactions-20261122/shortcut.json)
points to this payload. The user's owner profile and documents were not used by the
isolated tests. Restart FreeCAD Plus to load the updated native libraries.
The unrelated untracked `project.previewfirst.json` is preserved and excluded.

## Numeric arrow-step preview — November 22, 2026

Historical preview record; subsequently approved and implemented above.

The owner refined numerical preview timing across Extrude and other features:
typing remains deferred until field leave, while spin-button Up/Down updates
immediately. The [native proposal](ui-ux-specs/TASK_PANEL.md#typed-values-versus-arrow-steps--november-22-2026)
demonstrates actual arrow clicks while editing Extrude. Prototype checks passed
for typed-versus-stepped values, focus retention, no duplicate blur, manual mode,
unchanged saved feature geometry and Undo. No production/payload changes.

Implementation after approval must address the shared Qt numeric filter,
DeferredNumber step notification, Extrude's focused-field exclusion, and native
QuantitySpinBox emission policy. InputField must preserve deferred typed values
and expression semantics. Verify other feature/task consumers and automatic-off
behavior. This refinement joins the two pending proposals below; approval has
not yet been received for the combined change.

## Design idle actions preview — November 22, 2026

Historical preview record; subsequently approved and implemented above.

The owner extended the pending sketch visibility work with four Design idle actions:
New Sketch, Datum Plane, Datum Line, Datum Point. The native
[proposal](ui-ux-specs/TASK_PANEL.md#design-idle-actions-proposal--november-22-2026)
replaces Start Part/New Body with those four links under Create Geometry while no
selection or operation is active. Stub activation, exact order, selection/task
guards and unchanged model/Undo passed in a disposable native fixture. Both this
preview and the previous sketch visibility preview await direct chat approval;
production source, installed payload and unrelated work remain unchanged.

## Sketch visibility preview — November 22, 2026

Historical preview record; subsequently approved and implemented above.

The owner requested automatically visible fundamental planes during New Sketch and
usable History visibility eyes while creating the sketch. Current History explicitly
blocks eye actions whenever a task is open. An isolated native
[proposal](ui-ux-specs/TASK_PANEL.md#sketch-planes-and-history-visibility-proposal--november-22-2026)
shows XY/XZ/YZ on entry and demonstrates hiding/showing a solid and a plane through
the existing left-margin eyes without closing placement or changing its support.
Native fixture checks passed, restoring visibility and preserving object inventory
and Undo. Direct screenshots await approval under the owner's preview-first rule.
No application source or installed payload was changed. Production transaction,
native drawing-phase visibility, external-source and lifecycle handling remain
implementation work after approval. The unrelated `project.previewfirst.json`
remains untracked and untouched.

## Extrude implementation — November 22, 2026

Owner authorization: “make the operation a radio button option stacked vertically,
new solid, add, subtract. then implement.” The approved archive-guided workflow
is implemented with that amendment. The archive supplied concepts only; no old
implementation was copied. See the [approved task contract](ui-ux-specs/TASK_PANEL.md#extrude-implementation--november-22-2026).

Plus Extrude now has one creation/edit task with preselection, sketch/curve/region
picking, explicit Add/Subtract targets, start offsets/references, length and
reference-based ends, one/symmetric/independent sides, direction, taper and
tool/result preview. Numerical fields recompute after focus leaves. Preview and
Cancel preserve model inventory, saved visibility and Undo. Accepted operations
retain native identity across edits, with native linked references and internal
Bodies supplied by feature operations. Classic and legacy native editors remain.

The [native rebuild](evidence/extrude-20261122/final-build.log) succeeded. All 90
installed Extrude, Plane/numeric, feature-centered modeling and Sketch-placement
checks [passed](evidence/extrude-20261122/extrude_check.txt). These include geometry,
holes, explicit targets, operation changes, rotated Body coordinates, native
pattern polarity, invalid-input atomicity, deferred/manual updates and document
cleanup. The earlier development run also [passed](evidence/extrude-20261122/build-check.txt).
Installed validation corrected a payload path (native modules belong in app/lib),
an exact-BRep snapshot cast, and test-window activation. The final harness keeps
docked tasks active without stealing focus from standalone numeric test windows;
no Plane/Sketch production changes were needed.

[Fresh-process checks](evidence/extrude-20261122/extrude_reopen.json) verified local
and external-source persistence, shared task prefill, stable feature IDs,
downstream native features and a plane attached to an Extrude face after dimensional
editing. Temporary evaluation IDs are excluded from published tool element names.
This verifies the covered edits, not universal topology migration.

The [installed GUI exercise](evidence/extrude-20261122/extrude_visual.json) verified
real viewport region clicks, target/face picks, read-only preview, native command
dispatch, creation, shared editing and identity through Undo/Redo. Inspected
captures: [New Solid](evidence/extrude-20261122/installed-new-solid.png),
[Add to face](evidence/extrude-20261122/installed-add-face.png),
[Subtract tool](evidence/extrude-20261122/installed-subtract-tool.png),
[Subtract result](evidence/extrude-20261122/installed-subtract-result.png), and
[editing](evidence/extrude-20261122/installed-edit.png).

Eight payload files were backed up and installed with matching hashes:
[manifest](evidence/extrude-20261122/installation.json). The unchanged
[desktop shortcut](evidence/extrude-20261122/shortcut.json) launches this payload.
The final rebuild refreshed Python files and rebuilt the unchanged native semantics
after restoring source line endings; its native payload was checked again by the
fresh-process and GUI exercises. Tests used disposable documents/profiles, leaving
owner documents and settings untouched.

Scope remains closed planar profiles producing one valid solid, and native current
Body results as targets. Start references must parallel the profile; taper needs
Length; whole-shape limits resolve the first intersected forward boundary subject
to native face coverage. Cross-body rerouting after downstream operations is
rejected. Arbitrary imported targets and legacy operation migration remain separate.

## Archive-guided Extrude review and preview — November 21, 2026

Reviewed the archived Extrude task, extent/profile collectors, solver adapter and
tests; [findings](ARCHIVE_REFERENCE.md#extrude-workflow-review--november-21-2026).
A fresh [native prototype](ui-ux-specs/TASK_PANEL.md#archive-guided-extrude-proposal--november-21-2026)
extends the earlier length-only proposal with start/end conditions, independent
sides, conditional reference picking, advanced direction/taper and tool/result
preview modes. Archived code was not ported or executed. Representative fixture
checks passed with unchanged object inventory/Undo and restored visibility.
General geometry, region picking, persistence and shared operation editing were
not implemented by this prototype. The owner subsequently approved implementation
with vertically stacked operation radios; see the November 22 implementation above.

## Sketch offset and orange axes implementation — November 21, 2026

The owner approved the [direct preview](ui-ux-specs/TASK_PANEL.md#sketch-offset-and-local-axes-proposal--november-21-2026).
New Sketch and placement editing now share saved Offset/Reverse offset controls.
Signed offset follows the support's unflipped normal; Flip normal preserves position.
Native drawing handoff remains intact. Older managed sketches use zero offset
without property migration on open/Cancel. The shared Plane/Sketch preview uses
the approved orange, thicker, longer local axes and larger bold labels, leaving
fundamental/global axes unchanged. Numeric preview still commits only on focus leave.

All 61 affected plane/numeric, feature-centered modeling and Sketch-placement
checks passed in both the [development build](evidence/sketch-offset-20261121/build-check.txt)
and [installed app](evidence/sketch-offset-20261121/sketch_offset_check.txt).
This Python-only change required no C++ rebuild. Tests cover signed offsets,
point-origin overrides, normal flips, rotated support/component transforms,
internal Body transfer, native OK/drawing, shared editing, old-property compatibility,
Cancel, Undo/Redo and nonfinite-input rejection before mutation.

[Fresh-process reopen checks](evidence/sketch-offset-20261121/sketch_offset_reopen.json)
verified saved offsets, downstream extrusion updates and identity, and populated
edit tasks in local and external source files. The [installed GUI exercise](evidence/sketch-offset-20261121/sketch_offset_visual.json)
verified deferred updates, automatic-off, Reverse offset, real creation/drawing,
shared editing/Undo, and the common local-axis style in both tasks. Inspected
[Sketch](evidence/sketch-offset-20261121/installed-sketch.png),
[editing](evidence/sketch-offset-20261121/installed-sketch.png.edit.png) and
[Plane](evidence/sketch-offset-20261121/installed-sketch.png.plane.png) captures match
the approved appearance; [coincident axes](evidence/sketch-offset-20261121/installed-sketch.png.axes.png)
were also captured.

Four payload files were backed up and installed with verified source hashes:
[manifest](evidence/sketch-offset-20261121/installation.json). The existing
[desktop shortcut](evidence/sketch-offset-20261121/shortcut.json) still targets the
development payload with its original working directory. Owner documents/profile
were untouched; checks used isolated profiles and disposable documents.

## Sketch offset and orange axes preview — November 21, 2026

The owner reported missing Sketch offset and overlapping local/fundamental axes.
An isolated [native proposal](ui-ux-specs/TASK_PANEL.md#sketch-offset-and-local-axes-proposal--november-21-2026)
adds Offset/Reverse offset and a thicker orange local indicator with larger bold
labels and slightly longer arms. Numeric updates remain focus-leave; Flip normal
does not move the offset plane. Prototype checks passed without model/Undo changes.
The owner subsequently approved this proposal; implementation and installed
acceptance are recorded above. The isolated candidate remains historical preview evidence.

## Plane guidance implementation — November 21, 2026

Owner approval: “implement the concepts, do not copy over the code.” The current
plane task/solver now implement next-pick guidance, readable numbered references,
persistent amber point/line highlights, repeat-pick toggling, Delete removal and
independent Reverse axis. This is fresh implementation in current modules, not
copied archived code. Creation and editing use the same task. Axis reversal is
saved, preserves origin/normal/offset/display footprint, and follows native
Undo/Redo. Older planes default to false and are not modified on open or Cancel.
The approved layout and numeric focus-leave rule remain; Sketch UI opts out of
the plane-specific controls. See [UI approval](ui-ux-specs/TASK_PANEL.md#archive-guided-plane-proposal--november-21-2026)
and [architecture](ARCHITECTURE.md#component-construction-planes-and-numeric-commits--november-21-2026).

All 57 plane/numeric, feature-centered modeling and Sketch-placement checks passed
in both the [development build](evidence/plane-guidance-20261121/build-check.txt)
and [installed app](evidence/plane-guidance-20261121/plane_guidance_check.txt).
The source change is Python-only; no C++ rebuild was required. Checks cover
partial/invalid geometry, preselection and original occurrence paths, repeated
picks/Delete, origin defaults, bounded highlights for infinite datum lines,
cleanup, shared editing, old-plane compatibility, Cancel and Undo/Redo.
The validation harness initially raced a test's expected error-dialog handler;
removing its redundant modal watchdog resolved that harness failure. Final full
runs passed without it; the runner retained its finite process timeout.

A [fresh installed process](evidence/plane-guidance-20261121/plane_guidance_reopen.json)
reopened saved reversal, verified shared edit prefill, changed reversal and checked
downstream managed sketches, and recomputed external source-owned planes.
The [installed GUI exercise](evidence/plane-guidance-20261121/plane_guidance_visual.json)
checked staging without model changes, real creation/edit acceptance and identity
through Undo/Redo. Inspected captures match the approved layout:
[next-pick guidance](evidence/plane-guidance-20261121/installed-plane.png),
[reversed frame](evidence/plane-guidance-20261121/installed-plane.png.frame.png) and
[editing](evidence/plane-guidance-20261121/installed-plane.png.edit.png).

Four payload files were backed up and installed with matching source hashes;
[installation manifest](evidence/plane-guidance-20261121/installation.json).
The existing [desktop shortcut](evidence/plane-guidance-20261121/shortcut.json)
still launches this payload with its original working directory. Owner documents
and profile were untouched; validation used disposable documents and profiles.
Temporary origin-plane visibility and broader planar-curve support remain separate
recommendations; the earlier Extrude preview remains pending approval.

## Archived plane workflow review — November 21, 2026

Reviewed the preserved fork's plane solver, task, reference collector and tests.
The [findings](ARCHIVE_REFERENCE.md#plane-workflow-review--november-21-2026)
separate useful interactions from obsolete UI and conflicting origin/offset rules.
An isolated [native proposal](ui-ux-specs/TASK_PANEL.md#archive-guided-plane-proposal--november-21-2026)
shows next-pick guidance, numbered persistent references, reference toggling/Delete
and independent axis reversal. Prototype checks passed, including focus-leave
numeric updates and unchanged model inventory/Undo count. The owner subsequently
approved fresh implementation, recorded above. The earlier Extrude
proposal remains pending too. Detailed archived Sketch/Extrude review is not yet done.

## Extrude task preview — November 21, 2026

The owner requested a preview of a unified task with New Solid/Add/Subtract and
target selection. An isolated native candidate matches the existing section style
and shows profile preselection, explicit target picking, length/sides/direction
and deferred numeric preview controls. New Solid, Add, Subtract and missing-target
renders are recorded in the [owning UI proposal](ui-ux-specs/TASK_PANEL.md#extrude-task-proposal--november-21-2026).
Prototype interaction checks passed with unchanged model inventory and Undo count.
Only presentation simulation and review documentation are complete; approval,
production task integration and editing/persistence work remain pending. The
installed native Pad/Pocket workflows and feature-centered backend are unchanged.

## New Sketch placement implementation — November 21, 2026

The approved task is implemented and installed in the development payload used by
`freecad plus 0.1.0.lnk`. Both New Sketch commands populate preselected plane/face
references. A plane supplies its origin and orientation; a planar face uses the
projected part-local origin and X. Overrides and Flip normal persist, and clearing
an override restores automatic defaults. OK enters native sketch drawing without
creating a Body. Reorient/Attach Sketch and attachment editing reopen the same
placement task with saved inputs; ordinary sketch drawing remains native.
The [owning task specification](ui-ux-specs/TASK_PANEL.md#new-sketch-placement-workflow--november-21-2026)
records the approved exact preview. The [architecture](ARCHITECTURE.md#associative-native-sketch-placement--november-21-2026)
records persistence and compatibility; existing sketches are not implicitly migrated.

**Build and native acceptance:** Sketcher, SketcherGui, PartGui and PartDesignGui
built successfully. All 11 focused checks passed in both the build and installed
app: real OK-button handoff, saved editing, Cancel, identity-preserving Undo/Redo,
native Placement-property entry, preselection, plane/face defaults, projected-axis rejection/recovery,
point/two-point picking, external source ownership and transformed target Body
placement. [Installed results](evidence/sketch-20261121/sketch_check.txt).
All 39 affected New Plane/numeric and feature-centered Sketch/Extrude/Add/Subtract
regressions passed in the build. [Regression results](evidence/sketch-20261121/sketch_regression.txt).

**Persistence and visuals:** independent installed-app processes reopened local
and external component files, changed support geometry, verified downstream
extrusion placement and preserved identities, and reopened saved placement tasks.
[Reopen evidence](evidence/sketch-20261121/sketch_reopen.json).
The installed [face defaults](evidence/sketch-20261121/installed-face.png),
[plane defaults](evidence/sketch-20261121/installed-plane.png) and
[placement editing](evidence/sketch-20261121/installed-edit.png) were captured; face
and edit renders were inspected against the approved form. The GUI exercise also
created a real sketch, entered drawing and reopened its placement task.
[GUI evidence](evidence/sketch-20261121/sketch_visual.json).

**Delivery:** eleven changed payload files were backed up and installed with matching
source/build hashes. [Manifest](evidence/sketch-20261121/installation.json).
The existing desktop shortcut still targets `Launch FreeCAD Plus.bat` in the
external FreeCAD-Plus build root, which launches `app/bin/FreeCAD.exe`. Owner
documents and profile were untouched; validation used isolated profiles.

## Shared creation and editing tasks — November 21, 2026

The owner requires editing every feature/operation to reopen its creation workflow
in the task panel. The [shared task contract](ui-ux-specs/TASK_PANEL.md#shared-task-patterns)
and development guidelines now make this a standing implementation and acceptance rule.
Existing plane routes already share `PlaneTask`; no production/UI patch was needed.
A focused installed-app regression exercised History Edit and the native-tree
double-click handler with saved plane references, origin point, Y direction, offset
and flipped normal. Both restored all settings in the same task class. Cancel
preserved object inventory and Undo count; acceptance updated the original object
without changing identity, and Undo/Redo restored/reapplied its offset.
[Result](evidence/plane-20261121/plane_edit_check.txt).
The updated test module was copied to the installed payload. Other feature editors
have not all been individually audited by this check.

## New Plane implementation — November 21, 2026

The owner approved the simplified combined section and explicitly requested
implementation. The [task specification](ui-ux-specs/TASK_PANEL.md#new-plane-workflow-revision--november-21-2026)
owns approval, screenshots and exact UI scope. The existing `PartDesign_Plane`
command now opens the approved right-hand task for component documents. The
component owns an associative plane directly; no Body is required or created.
Real geometry selection, origin/axis assignment, normal flip, Cancel, source-owned
Undo/Redo, History editing and persistence are implemented. The separately requested
History-plane-to-New-Sketch entry workflow is now covered by the sketch task above.

**Native acceptance:** final installed `TestComponentPlanes` ran 15 checks with
zero failures/errors. Coverage includes native command entry, actual point/edge
selection, face/three-point/line-based construction, rotated Body/definition
references, external occurrence/source ownership, attached sketch recompute,
degenerate/cyclic rejection, Cancel, Undo/Redo and document-close cleanup.
Shared integer, decimal, unit-aware spin box and InputField checks verify zero
value notifications while typing and one on focus leave; a Move preview check
verifies no redraw while typing. New Plane's automatic-update-off behavior also
passed. [Focused results](evidence/plane-20261121/plane_check.txt).

**Regression limits:** the affected Sketch/Extrude/Add/Subtract and Move/Rotate
run completed 48 tests: 46 passed, two dock-close lifecycle assertions failed.
Both failures were reproduced independently against the unchanged installed
baseline before installation. They concern closing the managed component dock,
not numeric editing or plane creation, and remain unresolved outside this scope.
[Regression results](evidence/plane-20261121/plane_regression.txt),
[baseline comparison](evidence/plane-20261121/plane_baseline.txt).
The final two focused additions test rotated universal-origin projection and task
cleanup and passed in the installed 15-test run; the broader suite predates them.

**Persistence/GUI:** independent installed-app processes reopened domestic and
external saved files, changed a plane offset, and verified downstream sketch/source
recompute. [Reopen evidence](evidence/plane-20261121/plane_reopen.json).
The installed command's [task](evidence/plane-20261121/implemented-task.png),
[normal flip](evidence/plane-20261121/implemented-flip.png) and
[created History plane](evidence/plane-20261121/created-plane.png) were inspected.
The camera harness reports only a known Pivy deprecation warning.

**Installation:** built native GUI/PartDesign modules and Python modules/tests were
installed into the existing `_temp builds/FreeCAD-Plus/app` payload with backups.
[SHA-256 manifest](evidence/plane-20261121/installation.json) records all 11 files.
The existing `freecad plus 0.1.0.lnk` still points through the existing launcher to
that executable and owner profile; no shortcut or owner settings were rewritten.
This certifies the tested shared editor families and affected workflows, not every
third-party custom numeric editor or every native dialog.

## Grouped History and left-margin visibility — November 21, 2026

**Authority/implementation:** the owner approved the direct preview and explicitly
requested implementation. The
[component specification](ui-ux-specs/COMPONENT_PANEL.md#history-and-legacy-files)
records the exact approval, screenshot, session and fingerprint. Component Edit
from Models or Part Tree now switches to History. An expandable native Origin
groups X/Y/Z axes and XY/XZ/YZ planes ahead of sketches/features. Every part History
row has an open/crossed eye in a fixed far-left column, independent of nesting,
expansion or dock width. The name/icon column retains selection and native editing.
No document objects/schema changes or backend Body rows were added. The native
origin's additional point object is not a separate row in the approved grouping.

Eye/Space actions use effective internal ownership visibility and source-owned
transactions. Showing a child reveals necessary native Origin/Body containers;
hiding retains native child flags. Context/occurrence identity, pending-operation
and task/editor guards run before mutation. Eyes do not change selection or open
editors. Existing file History checkboxes and viewport coordinate graphics remain
unchanged. Native cross-file Undo forwarding markers remain available in the
active assembly, while the visibility change belongs to its defining file.

**Validation:** 40 native tests passed in the retained build (58.137 s) and
installed app (58.135 s), zero failures/errors/skips. Five new History cases cover
empty parts, grouping, fixed-column alignment through resize/collapse, real mouse
and keyboard visibility, selection/geometry preservation, hidden parent containers,
Undo/Redo, stale occurrence/pending/task guards and external ownership/save.
Six existing panel tests and the prior 29 modeling/command compatibility cases
also passed. Updated expectations account for the approved frame rows, native
Origin's extra point object, nonempty pending transactions and native Undo
forwarding; implementation behavior was checked directly rather than treating
those initial assertion mismatches as acceptance. Logs:
[build](evidence/history-20261121/build-tests.txt) and
[installed](evidence/history-20261121/installed-tests.txt).

An independent installed process reopened the saved assembly/source pair and
verified source identities, persisted axis/Origin visibility, grouped rows and
eye state. It exited 0 with empty stderr. The native installed UI was rendered
with real eye clicks and inspected against the approved screenshot. The
[installed screenshot](evidence/history-20261121/installed.png) and
[acceptance artifact](evidence/history-20261121/acceptance.json) record runtime
provenance, checks and source/build/app hashes. Suite diagnostics are unchanged
deliberate negative modeling/editor cases, recorded in acceptance.

**Build/delivery:** FreeCADPlusScripts synchronized successfully. Updated panel
and test modules are installed in `__Apps/_temp builds/FreeCAD-Plus/app`; this
increment needs no C++ rebuild. The launcher/desktop shortcut are unchanged.
The owner session/documents/settings were preserved; restart loads the updated
Python panel. Task-generated validation files were removed after retaining
durable evidence. Unrelated `project.previewfirst.json` stays excluded.

## Feature-centered Add/Subtract targets — November 21, 2026

**Implementation:** existing Pad/Pocket commands route standalone component
sketches to owned current PartDesign results. Sketch-only Pad remains New Solid;
sketch plus result selects Add. Pocket uses the explicit target or the sole
eligible result. Ambiguity, stale results, foreign ownership and ineligible
occurrences are rejected before mutation. Target and edit context survive the
native profile picker and are rechecked before starting the task. The active Body
does not choose the target. No labels, controls, forms, toolbar or dock layouts
were changed. The [architecture](ARCHITECTURE.md#feature-centered-addsubtract-targets--november-21-2026)
owns API semantics and scope, including the current single-solid PartDesign target
boundary and remaining consumed-profile/imported-target work.

Native Pad/Pocket tasks own the source-file transaction. Free sketch placement is
preserved when entering a transformed target Body, attachment support remains
native, and result appearance follows the target. Cancel restores original
profile and target visibility, including initially hidden objects, without the
legacy show-defaults overriding rollback. Native reference collectors receive the
actual target Body while editing. Existing Body-owned chains retain compatibility.

**Validation:** 29 native tests passed in both the retained build (41.679 s) and
installed app (41.828 s), with zero failures/errors/skips. Eleven target cases
cover Add/Subtract geometry, several independent results, active-Body independence,
transformed and attached profiles, picker retention/context changes, ownership
and original-occurrence guards, hidden-state Cancel, source-owned external edits,
Undo/Redo and saves. The preceding 18 backend/command/compatibility cases also
passed. See [build results](evidence/feature-centered-targets-20261121/build-tests.txt)
and [installed results](evidence/feature-centered-targets-20261121/installed-tests.txt).
Initial test assertions were corrected for floating-point recompute noise and
the existing Reference/Excluded diagnostic; the final runs above passed.

Separate build and installed processes reopened the saved domestic/external
models, checked identities, Profile/BaseFeature/Tip relationships, and recomputed
geometry after changing lengths. Both exited 0; the final installed reopen had
empty stderr. Expected suite diagnostics are the deliberately disconnected Add,
two open wires, an excluded-geometry refusal and the existing external-editor
guard called without its required context. The
[acceptance artifact](evidence/feature-centered-targets-20261121/acceptance.json)
records results, diagnostics and source/build/app hashes.

**Build/delivery:** the native build succeeded; the updated PartDesignGui and
Python modules are installed in `__Apps/_temp builds/FreeCAD-Plus/app`. The desktop
shortcut still targets the retained launcher with its original working directory.
`PartDesignGui.before-feature-targets-20261121.pyd` and earlier native backups are
retained for the owner's open session. No owner document/settings were changed.
Restart is required to load this native update. Temporary validation output was
removed after preserving evidence. Unrelated `project.previewfirst.json` remains
excluded from the commit. Routine publication targets the configured origin fork.

## Feature-centered command integration — November 21, 2026

**Implementation:** the existing ribbon New Sketch (`Sketcher_NewSketch`) and
new-solid Extrude (`PartDesign_Pad`) commands now reach the feature-centered backend
in component documents. Native orientation/attachment choices, profile picking,
Sketcher editing and Pad parameters remain unchanged. The command transaction
contains the provisional Body, original-profile ownership move and feature, so
native Cancel/Undo removes the Body and restores the sketch. Preselected curves,
initial sketch visibility and external defining-file ownership are preserved.
The native picker gained an internal component-profile route without its prior
Body prerequisite. Cancellation uses weak Body references to avoid accessing a
Body removed by rollback. External Sketcher selection restoration now names the
edit parent's source document instead of its hosting assembly view.

The [architecture](ARCHITECTURE.md#feature-centered-command-integration--november-21-2026)
owns the routing and compatibility boundary. No labels, icons, dialogs/forms,
field lists, toolbar layout or dock layout were changed. Existing Body-owned Pad
chains, Pocket and the separate PartDesign New Sketch workflow remain native
compatibility paths. Add/Subtract result targeting, source-profile reuse, deletion
cleanup and removal of idle New Body prompts remain separate work requiring a
preview before any UI changes.

**Validation:** all 18 native tests passed in both the retained build (27.975 s)
and installed app (27.955 s), with zero failures/errors/skips. The six new command
cases exercise actual orientation accept/cancel, attached sketches, native editor
completion, multiple-profile picker accept/cancel, preselected curves, invalid
task OK followed by Cancel, visible/hidden profile rollback, one-step Undo/Redo
and external source-file operations/reselection. Six backend cases and six native
compatibility/input/editor cases also passed. The earlier external `Object not
found` selection diagnostic is resolved. Remaining diagnostics are deliberate
negative cases: two open-wire failures, excluded-geometry refusal and an existing
external-editor guard test that intentionally calls setEdit without its required
context. Logs are retained with the
[build results](evidence/feature-centered-commands-20261121/build-tests.txt) and
[installed results](evidence/feature-centered-commands-20261121/installed-tests.txt).

An independent process using the final installed app reopened backend-created and
native-command-created domestic/external files, checked persistent identities,
Profile/Tip ownership and recomputed geometry after changing feature lengths. It
exited 0 with empty stderr. See the
[acceptance artifact](evidence/feature-centered-commands-20261121/acceptance.json).

**Build/delivery:** SketcherGui, PartDesignGui and FreeCADPlusScripts built
successfully using the retained current-machine compiler/build configuration.
The installed native modules match the build hashes; Python source/build/app copies
match as recorded in acceptance. The owner payload remains under
`__Apps/_temp builds/FreeCAD-Plus/app`. Its launcher/desktop shortcut are unchanged.
Previous native binaries are retained as `*.before-feature-commands-20261121.pyd`
because the owner session may still have them loaded. Open documents/settings
were preserved; restart is required to load the new native commands. Temporary
validation profiles were removed after retaining durable evidence. Unrelated
`project.previewfirst.json` remains excluded from the commit.

## Feature-centered modeling foundation — November 21, 2026

**Authority/scope:** the owner named original FreeCAD's method body-centered
modeling and FreeCAD Plus's method feature-centered modeling, authorized continued
backend work and required previews before any UI changes. This increment changes
no UI source or command routing. No UI preview was necessary for the backend API.

**Implementation:** `modeling.new_sketch` creates a standalone component-owned
Sketcher sketch. `modeling.extrude_new_solid` creates its native Body and Pad in one
source-owned transaction, moving the original sketch into the native profile scope.
The result must be one valid solid. Failure and Undo restore the prior sketch and
remove generated objects; Redo, constraints and native downstream recompute work.
The [architecture](ARCHITECTURE.md#feature-centered-modeling-foundation--november-21-2026)
owns the API contract and remaining integration boundaries.

**Native validation:** eight tests passed against the installed app (4.282 seconds,
zero failures/errors/skips): six new feature-centered cases and two existing
component History/native Pad-Pocket regressions. Coverage includes body-free
sketch creation/Undo, atomic extrusion/Undo/Redo, stable sketch identity/placement,
constraint-driven recompute, independent solids, wrong component/File Edit,
pending caller transaction preservation, invalid lengths/open-profile rollback,
and external unused-definition source ownership/Undo. The deliberately open wire
produced the expected native `Pad: Wire is not closed.` diagnostic; no unexpected
errors or profile-scope warnings occurred. An independent process reopened sketch-only,
extruded and external-component files, verified identities/Profile/Tip, and changed
parameters to validate downstream geometry. It exited 0 with empty stderr.
Durable results: [acceptance](evidence/feature-centered-20261121/acceptance.json)
and [native test log](evidence/feature-centered-20261121/tests.txt).

**Build/delivery:** CMake regeneration and FreeCADPlusScripts passed in the retained
`__Apps/_temp builds/FreeCAD-Plus/build` tree. New backend/test modules and test
registration are installed in the existing app payload, with matching source/build/app
hashes recorded in the acceptance artifact. The owner's open session and documents
were preserved. The ordinary New Sketch/Extrude commands still use the existing
body-centered path; no end-user workflow switch or completed conversion is claimed.
Next work is command transaction integration, followed by feature-result targeting
and deletion/reuse lifecycle. Unrelated `project.previewfirst.json` remains excluded.

## Right-hand Tasks dock — November 21, 2026

**Implementation:** the approved Tasks dock starts on the right at 320 logical
pixels, beside the viewport. `ui_modes` removes only Tasks from native overlay
membership, preserving other members and their corresponding size entries, then
waits for the native asynchronous reload before docking. A persisted
`FreeCADPlus/Workspace/TasksDockedRight` marker makes this a one-time default for
new and existing profiles. Later mode/workbench changes and restarts preserve the
user's location, size, floating state and visibility. Task contents, native
commands and document ownership are unchanged. The
[task specification](ui-ux-specs/TASK_PANEL.md#right-hand-tasks-dock--november-21-2026)
owns the approval evidence.

**Validation:** two isolated installed-app profiles passed four native tests each:
right-hand startup, subsequent custom layouts, all mixed UI modes/backend
preservation, and real Pad/Pocket operations with presentation changes and Undo/Redo.
One profile started fresh; the other had explicit `Report view,Tasks,` overlay
membership. Migration preserved `Report view,`. Each profile passed two separate
process restarts: the default remained right/docked at width 320; a later hidden,
floating Tasks panel retained its 380-by-460 size. All six processes exited 0,
without failures, errors, skips or stderr. Results are retained in
[acceptance.json](ui-ux-specs/evidence/tasks-dock-20261121/acceptance.json).
Inspected installed native captures while
[idle](ui-ux-specs/evidence/tasks-dock-20261121/native-idle.png) and during
[Pad](ui-ux-specs/evidence/tasks-dock-20261121/native-task.png) match the approved
layout. Captures use QScreen to include the actual OpenGL viewport. The native
New Body idle prompt remains; the component-first workflow is a separate milestone.

**Build/delivery:** FreeCADPlusScripts completed successfully. Source, build and
installed `ui_modes.py` match SHA-256
`2799dce71e2b1e98e32ea7f5f49c442fe78e69bd62a34ebdce8b50c5b945d312`.
The current machine's retained build/payload is under
`__Apps/_temp builds/FreeCAD-Plus`, superseding the old GAMING-PC paths for this run.
The existing desktop shortcut still targets that payload's launcher and working
directory. The owner's running app/documents were preserved; restart is required
to load the updated script. Unrelated `project.previewfirst.json` remains excluded.


## Ribbon theme background — November 21, 2026

**Implementation:** the Plus ribbon scroll viewport and each newly installed
content page no longer fill with the underlying Qt palette. The existing themed
toolbar paints their background. No fixed colors, theme-specific branches,
command/state changes, geometry changes or UI layout changes were introduced.
Production UI code matches the approved candidate, with repository line endings
preserved. The [toolbar specification](ui-ux-specs/TOOLBARS_AND_BUTTONS.md#ribbon-theme-background--november-21-2026)
owns the approval and preview evidence.

**Validation:** the new pixel-based native regression first reproduced the bug
against the old installed module: content `#3c3c3c` versus Light toolbar `#f0f0f0`.
After the fix, all six focused cases passed in the installed app (30.100 seconds,
zero failures/errors/skips): existing/rebuilt ribbon pages during Light/Dark/Light
switching, Classic restoration and independent preferences, modes/tabs/idle,
narrow-window captions, native arc split/last-used behavior, and Spreadsheet
native color controls. The test compares actual rendered backgrounds and confirms
Light differs from Dark and returns to the original Light color. Inspected native
[Light](ui-ux-specs/evidence/ribbon-theme-20261121/native-light.png) and
[Dark](ui-ux-specs/evidence/ribbon-theme-20261121/native-dark.png) widget captures
confirm the corrected content background; viewport rendering is outside this task.
The isolated app exited 0 with empty stderr. Owner settings/documents were untouched.

**Build/delivery:** FreeCADPlusScripts copied both changed Python files successfully;
no C++ rebuild was required. The source, retained build and installed toolbar module
match byte-for-byte (SHA-256
`eda49c1bd46c1f45d96714ef4fd66d45dcbfc0bfb63142f76192a54aabfffe5e`).
The app remains at `__Apps/_temp builds/FreeCAD-Plus/app`; its existing launcher and
shortcut were not changed. The already-running owner session needs a restart to
load the module. Unrelated `project.previewfirst.json` remains untracked/excluded.

## Unified startup component card — November 20, 2026

**Implementation:** the Start page now offers New Component in place of Parametric
Body and Assembly. It runs the existing Std_New component-document initializer,
then opens Design with the initial component active. It adds neither a Body nor a
separate assembly object. Remaining startup actions, settings, native workbench
availability, document schema and geometry services are unchanged. The approved
workflow and isolated Qt preview are recorded in
[Model View Window](ui-ux-specs/MODEL_VIEW_WINDOW.md#startup-and-workspace-stability).

**Build and runtime:** targeted StartGui compilation/linking passed in the current
machine's retained `__Apps/_temp builds/FreeCAD-Plus/build` tree (the older
GAMING-PC paths elsewhere in these instructions do not describe this machine).
All four TestNativeComponentCreation cases passed against the build and the
updated app, with no failures, errors or skips. The new case clicks the actual
native card in both model-panel presentations, verifies the five card labels and
icon, one definition/instance, active component, no eager Body, Design workbench,
and preservation of a pre-existing document. Existing native creation, Undo/Redo,
external ownership and legacy checks also passed. Separate fresh-process checks
passed against both payloads: saved own geometry and a child component survive
reopen, and existing native creation fixture identities remain unchanged.

**Visual and delivery:** inspected the
[native startup-card capture](ui-ux-specs/evidence/startup-component-20261120/native.png)
against the approved mockup. Labels, icon and ordering match; the native capture
uses the app's dark theme and display scaling. This is a Qt widget capture of the
card region, not a viewport geometry/framebuffer claim. The installed
`app/lib/StartGui.pyd` matches the compiled module byte-for-byte (SHA-256
`ed985575ce82dbb9d13c02cdc7f1303a4b63e6e21f676b0d08b9d861a60f4eaf`).
The installed-app tests and independent reopen exited successfully with empty
stderr. The desktop `freecad plus 0.1.0.lnk` still targets the existing launch batch
file and its working directory, whose app executable exists. No shortcut changed.
The owner's running process was preserved; it needs a restart to load the update.
Its loaded previous module remains under `StartGui.previous-20261120.pyd` for
safe rollback. Unrelated `project.previewfirst.json` remains untracked and excluded.
This updates the local development app; it is not a release or deployment.

## Authorized objective and stopping boundary

The owner continued Plus toolbar work after complete Classic coverage. TB.2a,
TB.2a1, TB.2a2, TB.2b, TB.2c1 and TB.2c2a through TB.2c2k below are implemented
and validated in the development payload.
All nineteen Classic workbenches plus None remain included. TB.2 as a whole is not
complete: persistence for other operations, Layers and Plus-only workflows need
their own implementation, while unconfirmed precise tab placements remain review material.
Do not repeat completed checks unless new changes justify them. Group 1 remains
incomplete and is not activated by this toolbar continuation.

## TB.2a2 Split-button availability — October 12, 2026

**Implementation/build:** Plus-only combined command groups keep their menu arrow
usable when the remembered action is unavailable but another visible choice is
enabled. Native QAction availability is unchanged; an unavailable icon does not
execute, available menu choices execute once, and an available default executes
immediately. All-unavailable groups disable. The remembered command survives state
changes and tab rebuilds. A small QToolButton subclass updates aggregate enablement
from native action events/signals without polling, page rebuilding, proxy actions
or custom painting. Native Classic split groups remain unchanged. FreeCADPlusScripts
synchronized into the retained development tree; no C++ rebuild was needed.

**Native acceptance:** the new native Python-command fixture reproduced the blocked
arrow before the fix (3.061 seconds in unittest, 8.218 with setup). Its first fixed
run exposed a stale QAction reference in the test's popup callback and was stopped
using the uniquely identified isolated process's executable/start time. Callback
cleanup now hides the menu in finally and reports errors. A second fixture failure
at the post-rebuild identity assertion (5.152/10.313 seconds) confirmed that retired
wrappers must not be compared; the test reads current menu/native actions and checks
stable command data after rebuilding. No native action lifetime implementation changed.

The final focused case passed (10.314/15.484 seconds), covering three alternating
availability changes, all-disabled states, unavailable-icon clicks, actual menu and
icon dispatch counts, native enabled states, icons, preference memory and tab
rebuilds. The inspected Qt captures show the remembered icon/arrow and native menu
with Choice A disabled and Choice B enabled. Eleven affected regressions passed
(66.443/71.531 seconds): arc split/default memory, Plus group memory, captions,
Classic restoration, native widgets/Spreadsheet colors, added/custom toolbars,
BIM status ownership, mode/idle behavior and duplicate workbench labels. These are
12 distinct cases with no final failures, errors, skips or timeouts; the suite now
has 64 cases. Final focused/regression stderr is empty and processes exited 0.
Unrelated geometry-operation cases were not rerun.

**Preservation/restart:** all nineteen Classic workbenches plus None passed the
native inventory audit: 240 toolbar groups and 1169 per-workbench command entries,
with no unavailable Classic-command placeholders and preserved native ownership/
restoration (58.110 seconds). Audit stderr contains only the known missing external
OpenSCAD executable notice. Separate prepare/restart passed (5.266/0.985 seconds),
with empty stderr and exit 0, preserving saved dropdown/selection preferences and
independent Classic toolbar visibility. All 51 Plus Python files parse and match
the payload byte-for-byte. Edited files preserve CRLF; whitespace checks pass.
Both shortcut targets and working directories were reread and remain unchanged;
the development and archived reference executables exist.

**Delivery/limits:** this is a local development increment, not publication or an
owner-ready package. Classic source, workbench/toolbar definitions, submodule pins
and licensing are unchanged. Owned validation/plus_split_availability output was
removed after recording evidence. Layers, the contextual palette and other Plus
operation integrations remain unfinished.

## TB.2a1 Workbench mode identity — October 12, 2026

**Implementation/build:** Plus routes modes by their native registered workbench
identity instead of display text. An added workbench named Design no longer gets
Design tabs/selection policy, and duplicate labels cannot select another mode's
row. Label changes refresh without changing the route. Existing native identifiers,
labels, actions, toolbar definitions and saved preferences are unchanged. Only the
Plus Python adapter changed; FreeCADPlusScripts synchronized successfully into the
retained development tree. No C++ rebuild was needed.

**Native acceptance:** the new regression first reproduced the wrong selector
owner for a Design-named workbench (2.503 seconds in unittest, 7.656 with setup).
After the fix, the case passed (17.051/22.141 seconds), exercising four added
workbenches: Design, CAM and two identical custom labels. It verifies selector and
native activation, non-Design tabs/policy, actual native command-button dispatch,
complete toolbar inventory/Classic restoration, active-label rename and return to
actual Design. The inspected ribbon capture shows the renamed mode, its own toolbar
and Home/Tools/View/All Tools tabs without Design selection controls.

All 14 affected regressions passed (65.149/70.234 seconds): native arc split/default
memory, Plus grouped-command memory, native widgets and Spreadsheet colors, added
and live custom toolbars, BIM status ownership, Classic independent preferences,
caption sizing, tabs/idle refresh and category/curve/directional/persistent control
scope. Together these are 15 distinct cases with no failures, errors, skips or
timeouts; the suite now contains 63 cases. Unaffected native geometry operations
were not rerun. Focused/regression stderr is empty and every native process exited 0.

**Preservation/restart:** all nineteen baseline workbenches plus None passed the
full native inventory audit: 240 toolbar groups and 1169 per-workbench command
entries, with no unavailable Classic-command placeholders and preserved native
ownership/restoration (57.766 seconds). Audit stderr contains only the known missing
external OpenSCAD executable notice. Separate prepare/restart passed (5.265/0.969
seconds) with empty stderr, preserving selection preferences, remembered Pocket
choice and independent Classic toolbar visibility. All 51 Plus Python files parse
and match the payload byte-for-byte; original CRLF endings and whitespace checks
pass. Both shortcut targets/working directories were reread; development and
archived executables exist and shortcuts remain unchanged.

**Delivery/limits:** this is a local development increment, not publication or an
owner-ready package. No Classic source, submodule pin or license changed. The
native audit certifies toolbar coverage, not every modeling/CAM/FEM operation.
Owned validation/plus_mode_identity output was removed after recording evidence.
Layers, the contextual palette and other Plus operation integrations remain open.

## TB.2c2k Delete All Constraints — October 12, 2026

**Implementation/build:** the native menu-only command now keeps usable Plus idle
inputs through confirmation/completion and prunes deleted constraint references.
Geometry is not cleared/replayed. Persistent off clears after actual deletion;
Cancel/no-op preserves Plus inputs. Native dialogs, transactions, solver/recompute
and Classic cleanup remain unchanged. The native Constraints-list refresh now
blocks programmatic row-removal signals only in idle Plus, preventing the selected
row's removal from clearing surviving viewport geometry. Normal list clicks are
unblocked immediately. SketcherGui and FreeCADPlusScripts rebuilt successfully in
the retained development tree with concurrency 3.

**Focused acceptance:** all three cases passed (54.565 seconds in unittest, 54.984
with runner setup), native exit 0 and empty stderr. This covers mixed edge/vertex/
origin/constraint inputs, constraint-only input, Cancel/no-op, both AutoRecompute
settings, nested Part edit paths, geometry/solver validity, Undo/Redo and real
Constraints-list clicks after Undo. The inspected framebuffer shows the retained
green line, endpoint and origin with constraint symbols removed.

The first run passed Cancel/no-op, then exposed an incorrect test assumption about
raw names: FreeCAD stores the nested edge with its mapped name. Comparing that
actual name exposed the programmatic list-row removal that cleared all selection.
A first exact-text patch missed the file's CRLF endings and led to one unchanged
repeat of that failure; the actual signal fix preserves the original line endings
and passed after rebuilding. Native model geometry/transaction code was not changed.

**Affected regressions:** all 12 core cases passed in 272.745 seconds (273.094 with
setup), covering B-spline elevation, basic/point/concentric constraints, interactive
picking, rejected/no-op inputs, state toggles and tangency substitutions. All 11
UI cases passed in 99.573 seconds (99.922 with setup): contextual/named dimension
Cancel/no-op, Classic restoration, Equal/Construction, native constraint picking,
mode routing, arc split/default memory, native widgets, custom/added-workbench
coverage, live customization and Plus group memory. Together with the focused
cases, 26 distinct cases passed with no failures, errors, skips or timeouts. The
suite now has 62 cases; unrelated completed cases were not rerun. Every final
native process exited 0. Focused/UI stderr is empty; core stderr contains exactly
three expected non-dimensional Driving rejection tracebacks and no other output.

**Preservation/restart:** the native audit passed all nineteen Classic workbenches
plus None: 240 toolbar groups and 1169 per-workbench command entries, with no
unavailable Classic-command placeholders and preserved native ownership/restoration.
Audit took 54.235 seconds; stderr contains only the known external OpenSCAD missing-
executable notice. Separate prepare/restart passed in 0.531/1.031 seconds with empty
stderr, preserving selection preferences, remembered Pocket choice and independent
Classic File/Edit visibility. Native build stderr is empty. All 51 Plus Python files
parse and match the payload byte-for-byte, native non-ASCII text is preserved and
whitespace checks pass.

**Delivery/limits:** both shortcut targets and working directories were reread and
verified; the development executable exists and the archived reference shortcut is
unchanged. Task-owned validation/plus_delete_constraints files were removed after
recording these results. No Classic toolbar/workbench definition, submodule pin or
licensing changed. This is a local development increment, not publication or an
owner-ready package. Cancel/no-op and native Undo/Redo passed; arbitrary native
exception/abort paths were not fault-injected. Other deletion/renumbering operations,
Layers and the contextual palette remain unfinished.

## TB.2c2j B-spline degree elevation — October 12, 2026

**Implementation:** native Increase B-spline Degree now honors Persistent Selection
for idle Plus Design sketches. On retains the actual selected entities; off clears
after a degree/helper-geometry change. A no-op retains usable Plus inputs. Native
curve identity, helper creation, warnings, recompute, transactions and Classic
cleanup remain unchanged. No selection replay, Classic toolbar/workbench definition,
submodule pin or licensing change was introduced. Degree reduction, knot changes
and conversion retain their separate native paths.

**Build:** SketcherGui and FreeCADPlusScripts built successfully in the retained
freecad_1.1.4_context development tree with concurrency 3 and empty build stderr.
All 51 Plus Python files parse and match the synchronized payload byte-for-byte;
native non-ASCII text is preserved and the whitespace check passes.

**Validation:** the first endpoint-only case stopped on its incorrect assumption
that a native no-op adds no Undo entry (12.703 seconds, native exit 0). The original
commit/recompute path records one entry even without a degree change. Corrected
the expectation without changing production transaction code; the final matrix
confirmed the same entry in Plus on/off and Classic.

Both focused native cases then passed (43.521 seconds in unittest; 43.937 including
runner setup). Coverage includes single and mixed line/two-spline inputs, two
successive elevations without reselection when enabled, native degrees and sampled
curve shape, solver/shape validity, selection names, helper counts and Undo/Redo.
Endpoint-only no-op retention passed in all three modes. Native framebuffer capture
was inspected: both splines and the selected line remain green after elevation,
with the native curvature combs, blue helper circles and constraint markers visible.
This does not certify every rational/periodic spline or maximum-degree kernel failure.

Ten affected toolbar regressions passed (52.780 seconds in unittest; 53.140 with
setup): Classic restoration, mode routing, Persistent Selection controls and
Equal/Construction, Curve Intent, native arc split/default memory, native widgets,
added-workbench/custom-toolbar coverage, live customization and Plus group memory.
There were no failures, errors, skips or timeouts in the final focused/regression
runs; both native processes exited 0 with empty stderr. The full suite now contains
59 cases; the unrelated completed cases were not rerun for this scoped change.

**Preservation/restart:** the native audit passed all nineteen Classic workbenches
plus None: 240 toolbar groups and 1169 per-workbench command entries, no unavailable
Classic-command placeholders, preserved action/widget ownership and Classic
restoration. Audit took 62.391 seconds, native exit 0; stderr contains only the known
external OpenSCAD executable-not-found notice. Separate prepare/restart processes
passed (0.594/1.016 seconds), native exit 0, empty stderr, including saved selection
preferences, remembered Pocket choice and independent Classic File/Edit visibility.

**Delivery/remaining:** the development executable and both shortcut targets/working
directories were reread and verified; the archived reference shortcut is unchanged.
Task-generated validation files were removed after recording this evidence. This is
a local development increment, not a release or completed owner package. Layers,
the contextual palette and other operation integrations remain unfinished. Classic
workbench/toolbar inclusion is complete and requires no duplicate implementation.

## TB.2c2i Preselected contextual Dimension — October 12, 2026

**Implementation:** contextual Dimension now preserves Plus preselection through
native view-provider activation and returns a completed preselected operation to
ordinary sketch picking. Persistent on retains inputs; off clears them after a
commit. Cancel/no-op preserves usable Plus inputs. Native M-key alternatives,
datum dialogs, constraint creation and transaction ownership remain unchanged.
The existing purgeHandler service has an optional clearSelection argument with
its original true default for every existing caller. Native Classic and sequences
started without preselection retain continuous creation. Escape/Undo resets the
new preselection flag before subsequent picks. No Classic toolbar/workbench
definition, submodule pin or licensing changed.

**Build:** SketcherGui and FreeCADPlusScripts built successfully in the retained
freecad_1.1.4_context development tree with concurrency 3. The corrected activation
path was rebuilt successfully before rerunning native acceptance.

**Validation corrections:** the initial run exposed that native ActivateHandler
clears selection before activating the handler; merely preserving selection at
completion was insufficient. The Plus preselected command now uses the same native
view-provider purge/activate services with clearing disabled. The generated test
profile also had a missing closing XML element; repaired it and parsed the XML
before launching. Native datum autoscaling survived Undo and moved later placement
clicks outside the viewport, so each contextual fixture now normalizes the top view
and camera extent before dispatch.

The initial runner continued through failed active-preview placement assertions;
later edit reset reported an access violation, followed by repeated native paint/
RTTI diagnostics. Only the precisely identified task-owned validation process was
stopped; no complete result was claimed. The runner now stops on the first failure
to avoid continuing through a failed preview sequence. The next run passed Cancel/
no-op but stopped on an Undo-count assertion after circular completion (47.156 seconds,
native exit 0, no native diagnostics). An independent Classic/Plus comparison showed
both produce the same two native transactions when first-dimension autoscaling is
on: Add radius constraint, then Scale geometries. First Undo restores the unscaled
geometry while leaving its constraint; second removes the constraint. Plus retains
the selected edge while Classic clears it. No transaction behavior was changed.
Ordinary completion fixtures now disable autoscale in isolated preferences, with a
separate native-autoscale Undo/Redo matrix retaining the real default behavior.
The corrected run passed Cancel/no-op, circular/M-key geometric modes and repeated
continuous/Escape behavior, then stopped on the autoscale radius tolerance
(107.031 seconds, native exit 0). Native formatted scaling produced 6.666667 rather
than the exact fraction 20/3; the assertion now uses six decimal places. The three
remaining cases (native autoscale, preselected length, reference/no-dialog) passed
in 87.875 seconds, native exit 0, empty stderr, no failures/errors/skips or watchdog
interventions. The earlier paint/access-violation diagnostics did not recur in the
corrected runs. The inspected native framebuffer shows the retained green line with
its red 22 mm dimension and the other unselected white line.

**Combined native/visual acceptance:** all 57 toolbar cases passed in four
non-overlapping isolated native processes: 14 in 210.985 seconds, 14 in 292.704,
14 in 206.203 and 15 in 265.234 (975.126 total). Recorded IDs exactly match the
source inventory, with no duplicates, failures, errors, skips or popup-watchdog
interventions. All processes exited 0. First/third/fourth stderr are empty; second
contains exactly the three expected native non-dimensional Driving rejection
messages from TB.2c2h and nothing else. The final native framebuffer was inspected:
the 22 mm line remains green, its dimension is red and the other line is white.
The initial paint/access-violation diagnostics did not recur.

Runtime coverage includes line and circular dimensions, M-key geometric alternatives,
Cancel/no-op, reference/no-dialog, native autoscale, repeated continuous picking and
Escape, with native solve/shape checks and Undo/Redo. It does not certify every
contextual geometry combination or multi-datum/external-geometry dialog sequence.
Native transaction/solver behavior is retained rather than replaced.

**Complete inventory/restart:** the separate audit passed all nineteen Classic
workbenches plus None: 240 native toolbar-group instances and 1,169 per-workbench
command occurrences, native exit 0. Its only stderr notice was the known missing
external OpenSCAD executable. Separate prepare/restart processes passed with exit 0
and empty stderr, retaining Persistent/Directional off, Tangent Curves, Faces
unchecked, remembered Pocket choice and hidden File/shown Edit Classic settings.
Both shortcuts were reopened/read: the development executable and working directory
still point to freecad_1.1.4_context/bin; the archived-fork reference target and
working directory remain unchanged and exist.

**Source/publication/cleanup:** all 51 Plus Python files parse and match the
retained development payload. Native non-ASCII text and source whitespace checks
pass. No push, release or owner-ready packaging is claimed. The owned
`C:/Users/GAMING-PC/Documents/_temp/freecad/validation/plus_contextual_dimension`
validation directory was removed after recording these durable results; all native
validation processes exited. Useful builds, settings,
dependencies and reference shortcuts are retained. This increment is prepared as a
focused local commit. Layers, the contextual palette and other operation persistence
remain unfinished; TB.2 and Group 1 remain incomplete.

## TB.2c2h Constraint states and Refraction — October 12, 2026

**Implementation:** native Toggle Driving/Reference and Toggle Active now use the
existing Plus completion policy, retaining selected constraints and any accompanying
geometry when persistence is on. A separate applied flag preserves rejected/no-op
Plus inputs even with persistence off without changing native commit/abort counting.
Creation-mode toggling, command icons, constraint identities and the Classic cleanup
path remain native. Refraction still uses its original menu, ratio dialog, solver,
transaction and helper-constraint creation; successful completion observes Plus
persistence. An invalid-object/empty-selection branch now returns after its native
warning instead of accessing selection[0]. No Classic workbench/toolbar definition,
submodule pin or licensing changed.

**Build:** SketcherGui and FreeCADPlusScripts built successfully in the retained
freecad_1.1.4_context tree, MSVC 19.44 / Qt 6.8.3 / Python 3.12, concurrency 3.
All 51 Plus Python files parse and match the development payload byte for byte.
Native non-ASCII text is preserved.

**Focused validation and corrections:** the first six-case run completed in
100.609 seconds, exit 0. Creation-mode icons, both repeated constraint toggles,
rejected/no-op selection, Refraction acceptance and Undo/Redo passed. The Refraction
rejection fixture incorrectly expected an enabled menu action with empty selection;
native isCreateConstraintActive disables it. Corrected that assertion and added an
enabled mixed-object rejection case for the safety guard. The fixture also deleted
a warning timer already owned by unittest cleanup; removed that duplicate deletion.
The two corrected Refraction cases passed in 34.156 seconds, native exit 0, empty
stderr, no failures/errors/skips or popup-watchdog interventions.

The intentionally rejected non-dimensional Driving toggle emits its native ValueError
and command diagnostic once in each Plus-on, Plus-off and Classic matrix case.
These expected diagnostics are retained; production error handling is unchanged.
The inspected native framebuffer shows green selected reference-dimension symbols
and the additionally selected first edge; the other edge remains unselected.

**Combined native/visual acceptance:** all 51 TestPlusToolbars cases passed in three
non-overlapping isolated native processes: 17 in 273.187 seconds, 17 in 227.407
seconds and 17 in 292.171 seconds (792.765 total). Recorded IDs match the source
inventory exactly, with no duplicates, failures, errors, skips or popup-watchdog
interventions. All three processes exited 0. First/third stderr are empty; second
stderr contains exactly the three expected native rejection diagnostics described
above and no other output. The final native framebuffer was inspected and confirms
retained green constraint symbols and first-edge selection.

**Complete inventory/restart:** the separate audit passed all nineteen Classic
workbenches plus None: 240 native toolbar-group instances and 1,169 per-workbench
command occurrences, native exit 0. Its only stderr notice was the previously known
missing external OpenSCAD executable. Separate prepare/restart processes passed with
exit 0 and empty stderr, retaining Persistent/Directional off, Tangent Curves,
Faces unchecked, remembered Pocket choice and hidden File/shown Edit Classic settings.
Both desktop shortcuts were reopened/read: development targets
freecad_1.1.4_context/bin/FreeCAD.exe with that bin directory as working directory;
the archived-fork reference target/working directory remain unchanged and exist.

**Source/publication/cleanup:** final Python parse/payload parity and whitespace
checks pass. No push, release or owner-ready packaging is claimed. The owned
`C:/Users/GAMING-PC/Documents/_temp/freecad/validation/plus_constraint_states`
validation directory was removed after recording these durable results; all native
validation processes exited. Useful builds, settings, dependencies
and reference shortcuts are retained. This increment is prepared as a focused local
commit. Layers, the contextual palette, contextual Sketcher_Dimension and other
operation persistence remain unfinished. TB.2 and Group 1 remain incomplete.

## TB.2c2g Direct Tangent/Perpendicular retention — October 12, 2026

**Implementation:** native preselected Tangent/Perpendicular cleanup now uses
finishConstraintSelection for edge pairs, endpoint pairs, endpoint-to-curve and
via-point forms, plus native constraint substitutions and helper-point conics.
The four conic tangency helpers return their native commit/abort outcome; transaction,
solver, recompute and geometry ownership remain native. Continuous handlers retain
their original source and STATUS_NONE-guarded substitution cleanup. Unsupported direct
B-spline tangency preserves Plus input selection on rejection even with persistence
off. No Classic workbench/toolbar definition, submodule pin or licensing changed.
**Build:** SketcherGui and dependencies built successfully in the retained development
tree, MSVC 19.44 / Qt 6.8.3 / Python 3.12, concurrency 3.

**Validation corrections:** the first six-case run completed in 143.125 seconds.
Conic helper-point Undo/Redo, continuous picking, preselected forms, B-spline rejection
and native substitutions passed. All six via-point matrix assertions expected two
constraints, but native IsPointAlreadyOnCurve uses geometric membership: a point
already on both curves needs no extra PointOnObject constraints in either Plus or
Classic. Corrected that assertion and added an independent off-curve point fixture.
A transient native DogLeg/degenerate-line diagnostic occurred although final solve/
shape checks passed. Continuous and preselected fixtures now use geometry near their
intended tangent/perpendicular orientation. Production solver behavior is unchanged.
A second run also exposed fixture-document interference in selection setup after
Undo; each completed fixture now closes its document before the next is created.
The corrected three-case rerun passed in 119.835 seconds, no failures/errors/
skips or watchdog interventions, native exit 0 and empty stderr. It covers all
preselected forms, geometrically-on-curve and independent off-curve via-points, plus
repeated continuous picks, valid solves/shapes and Undo.

The temporary runner attempted to serialize unittest subtest objects after failures,
preventing its result write/close. Only the precisely identified task-owned validation
process was stopped. The runner now serializes test names and tracebacks. Source checks preserve native
non-ASCII text and unchanged continuous handler bodies; all 51 Plus Python files
parse and match the development payload byte for byte.

Conic runtime fixtures exercise ellipse/circle tangency and ellipse/line
perpendicularity, including helper-point creation and Undo/Redo. The arc-of-ellipse,
hyperbola and parabola helper outcome changes compile with their native consumers;
this increment does not claim exhaustive runtime coverage of every conic pair,
B-spline endpoint/knot or external-geometry combination. Native diagnostics remain
visible; a committed but unsolved sketch is not relabeled as a successful solve.

**Final native/visual acceptance:** all 45 TestPlusToolbars cases passed in two
non-overlapping isolated processes: 22 in 345.871 seconds and 23 in 338.631 seconds.
The recorded case IDs exactly match the source test inventory, with no duplicates,
failures, errors, skips or popup-watchdog interventions. Both processes exited 0
with empty stderr. This includes all six new constraint cases and all 39 preceding
ribbon, native split-button/default-memory, category/directional, persistent,
dimension, Classic-restore, custom-toolbar and specialized-widget regressions.
The final native framebuffer was inspected: the line and arc remain green after
Tangent, with the native constraint glyph visible. Final runs did not reproduce
the diagnostic from the early unstable fixture.

**Complete inventory/restart:** the separate audit passed all nineteen Classic
workbenches plus None, 240 native toolbar-group instances and 1,169 per-workbench
command occurrences, exit 0. Its only stderr notice was the previously known
missing external OpenSCAD executable. Both independent prepare/restart processes
passed with exit 0 and empty stderr, retaining Persistent/Directional off, Tangent
Curves, Faces unchecked, remembered Pocket choice and hidden File/shown Edit Classic
preferences. The two desktop shortcuts were reopened/read: development still targets
freecad_1.1.4_context/bin/FreeCAD.exe with that bin directory as working directory;
the archived-fork reference target and working directory remain unchanged and exist.

**Source/publication/cleanup:** whitespace and source/payload checks pass. No push,
release or owner-ready packaging is claimed. The owned
`C:/Users/GAMING-PC/Documents/_temp/freecad/validation/plus_tangent_selection`
validation directory was removed after recording results. Native validation processes
exited; useful build payloads, settings, dependencies and reference shortcuts remain.
This increment is prepared as a focused validated local commit. Layers, the contextual palette, contextual
Sketcher_Dimension and other operation persistence remain unfinished; exact unconfirmed
placements remain review material. This completes TB.2c2g only; TB.2 and Group 1
remain incomplete.

## TB.2c2f Preselected dimensions and Curve Intent sizing — October 12, 2026

**Implementation:** the native finishDatumConstraint path now observes the dialog's
actual commit-success flag and uses the existing Plus completion policy. Named
preselected distance, angle and circular dimensions retain native inputs with
Persistent on; off and Classic clear. Cancel keeps usable Plus input selection with
either toggle value. Both native dialog constructors initialize the success flag.
Removed Radius/Diameter/Radiam's redundant post-completion clear; their continuous
handlers keep native cleanup. Transaction, solver, expression, autoscale, command,
geometry identity and icon/menu ownership remain native. No Classic toolbar/workbench
definition, submodule pin or license changed. Architecture owns the scope and contracts.

The combined audit exposed a separate Curve Intent sizing defect in the active Qt
style: its 25-pixel button allocated 17 pixels to the arrow, leaving an 8-pixel main
hit area. The Plus button now reserves a square icon area plus the native arrow
width through sizeHint, preserving native painting and popup behavior. Tests wait
for layout after rebuilding, verify adequate main hit area and click that area.
A temporary popup watchdog recorded the blocked call and failed the diagnostic
instead of allowing an open menu to hang indefinitely. Layout settling alone did
not fix the native style allocation; the production size hint does.

**Build:** SketcherGui and dependencies built successfully in the retained
freecad_1.1.4_context tree with MSVC 19.44, Qt 6.8.3, Python 3.12 and existing libpack,
concurrency 3. Final script synchronization and source checks are recorded below.

**Focused checks:** batch radius/Equal with Undo/Redo, Plus-on/off/Classic Cancel,
circular values and repeated continuous picks passed. Corrected distance/angle and
reference/no-dialog cases passed together in 68.805 seconds, zero failures, errors
or skips, exit 0 and empty stderr. Tests dispatch real native dropdown actions,
quantity-field input and dialog buttons, and require native solve success, valid
geometry, expected values, selection and Undo behavior.

**Validation corrections and limits:** the first harness used the XML namespace
instead of Qt's generated SketcherGui__InsertDatum object name, leaving the dialog
open. Only the identified task-owned process was stopped. A subsequent attempt
reported an access violation and exited -1073740791; Windows Application Error
identified nvoglv64.dll 32.0.15.6094, exception 0xc0000409, as the faulting module.
The exact trigger is unknown. The same traced batch case passed in 9.214 seconds
without a source fix, and later focused runs did not reproduce the crash. No driver
or graphics settings were changed; this does not establish long-session stability.

The next complete focused run exposed test assertions that compared native radians
to degrees and missed the checkbox indicator. Those were corrected, including
native reference-state verification; failed matrix cases now undo their operation
before the next case. No production changes were required for those fixture fixes.
The first dimension capture was too small to accept: native autoscaling changes
camera scale while Undo restores geometry only. The capture fixture now refits the
view and captures the first dimension before repeated camera/label autoscaling;
final visual acceptance is separate from command assertions.

**Final combined/visual/source acceptance:** all 39 TestPlusToolbars cases passed
in 511.119 seconds, zero failures, errors, skips or popup-watchdog interventions,
normal exit 0 and empty stderr. This includes the six dimension cases, Curve Intent
split-area regression, native arc/group memory, categories, directional selection,
Classic restoration, custom toolbars, BIM status ownership and Spreadsheet widgets.
The final focused Curve Intent/dimension pair also passed in 51.277 seconds with
clean diagnostics. Inspected final-code captures show a green retained edge with
its 25 mm dimension and distinct native icon/arrow areas on Curve Intent. All 51
Plus Python files parse and match the synchronized development payload byte for byte;
whitespace checks pass. The early driver fault did not recur in these final runs,
but its precise trigger and long-session stability remain unestablished.

**Inventory/restart acceptance:** the independent audit passed all twenty registered
workbenches (nineteen baseline Classic workbenches plus None), 240 toolbar-group
instances and 1,169 per-workbench command occurrences. No omissions, stolen native
widgets/actions or Classic restoration failures were found. Exit was 0; stderr has
only the existing missing OpenSCAD executable notice. Separate prepare/shutdown and
restart processes passed with exit 0 and empty stderr. Persistent and Directional
off, Tangent Curves, Faces unchecked, Pocket default and hidden File/shown Edit
Classic toolbar preferences survived independent restart.

**Delivery boundary:** the contextual Sketcher_Dimension drawing handler, direct
Tangent/Perpendicular and other operations, Layers and separately owned Plus workflows
remain unfinished. Native specialized weight/refraction/external combinations are
not exhaustively certified. Both retained shortcut targets and working directories
were reverified unchanged. This is a development increment, not owner packaging.
The coherent changes are committed locally; no remote publication or release was
performed. Task-generated validation output is removed after recording these results;
useful builds, both shortcuts and owner settings remain preserved.

## TB.2c2e Basic preselected constraint persistence — October 12, 2026

**Implementation:** extended the Design Persistent Selection setting to native
Horizontal/Vertical/HorVer, Parallel, Block, coincidence/concentric, Point on Object
and all three Symmetric input forms. Equal shares the native completion helper.
These commands retain existing input geometry selection after success with the
setting on; off and Classic retain native clearing. Native coincidence/Point-on-
Object tangency substitutions keep selected geometry while replacing constraints.
Rejected Block point/external inputs and an already-coincident abort retain Plus
inputs even with persistence off. Continuous handlers keep their native reset
sequence through an explicit idle-Sketcher check. No selection replay, native action
replacement, geometry identity change, toolbar definition or submodule-pin change
was introduced. Architecture owns the completion contract and limits.

**Build/source checks:** SketcherGui and dependencies built successfully in the
retained freecad_1.1.4_context tree with MSVC 19.44, Qt 6.8.3, Python 3.12 and the
existing libpack, concurrency 3. Final FreeCADPlusScripts synchronization passed.
All 51 Plus Python files parse and match the development payload byte for byte.

**Focused native acceptance:** six new cases passed in 138.151 seconds, zero
failures, errors or skips and normal exit 0. Tests compare Plus on, Plus off and
Classic, verifying constraint types, geometry counts, one native transaction for
each tested operation, Undo/Redo and selection. They cover edge and point alignment,
concentric curves, every Symmetric input form, rejected inputs without new Undo,
endpoint tangency substitutions, repeated continuous picks and Escape cleanup.
The inspected normal-framebuffer capture shows both selected parallel lines and
native constraint symbols.

**Validation correction:** the first focused run had eleven assertions caused by
a test assumption that Horizontal/Vertical were standalone buttons. The default
Classic layout exposes them through Sketcher_CompHorVer. The test helper now opens
the real arrow and selects the native menu action. All six corrected cases passed;
no production change was needed for this fixture correction.

The 33-case combined suite passed its original assertions in 348.459 seconds,
with no test failures, errors or skips and normal exit 0. Its stderr exposed a
second fixture problem: Vertical alignment of opposing endpoints could collapse a
line in the native solver. A traced follow-up with explicit solve/geometry checks
caught this failure; subsequent subcases then accumulated constraints because that
failed assertion preceded Undo. The fixture now selects corresponding endpoints,
and the matrix requires native solve success and valid geometry. Final affected
acceptance is recorded below; no application code changed for this correction.

**Final affected acceptance:** all six corrected cases passed in 137.866 seconds,
zero failures, errors or skips, normal exit 0 and empty stderr. The final matrix
requires native solve success and valid geometry as well as constraint/selection,
Undo/Redo and mode behavior. All 51 final Python files parse and byte-match the
payload; whitespace checks pass. The 27 unchanged cases already passed in the
combined run above; only test fixtures/assertions changed afterward.

**Inventory/restart acceptance:** the independent audit passed all twenty registered
workbenches (nineteen baseline workbenches plus None), 240 native toolbar-group
instances and 1,169 per-workbench command occurrences. No missing Plus commands,
widget ownership or Classic restoration failures were found. Audit exit was 0;
stderr contains only the existing missing OpenSCAD executable notice, so external
tool availability is not certified. Separate prepare/shutdown and restart processes
passed with exit 0 and empty stderr. Persistent and Directional off, Tangent Curves,
Faces unchecked, Pocket default and hidden File/shown Edit Classic toolbar
preferences survived restart. The native application was unchanged by subsequent
fixture-only corrections.

**Delivery/stopping boundary:** dimensions, direct Tangent/Perpendicular and other
operation integrations, Layers and separately owned Plus workflows remain unfinished.
Both retained desktop shortcut targets and working directories are verified and
unchanged. No remote publication or release was performed. This is development
payload validation, not owner packaging. The coherent increment is committed locally;
task-generated validation output is removed after recording these durable results.
Useful builds, owner settings and both reference/development shortcuts are retained.

## TB.2c2d Equal/Construction persistence and status controls — October 12, 2026

**Implementation:** added the saved, default-on Persistent Selection control to
Plus Design. Native Equal and Toggle Construction retain their existing selected
sketch entities at successful completion when it is on; off and Classic retain
native post-command clearing. This enables the confirmed Equal-to-Construction
sequence without reselection. No stale selection names are replayed. Other native
operations and the contextual palette remain unintegrated, and the tooltip states
the current command scope. Architecture owns the policy and completion contract.

The exposed-window inventory audit also identified that BIM's status widget uses
the same Gui::ToolBar class as ribbon toolbars. Plus now recognizes status-bar
ownership and keeps a transient marker through upstream reparenting. Such controls
never acquire Plus visibility bookkeeping or suppression. Native actions, parent,
location and workbench-driven hide/show remain authoritative. Classic command
behavior and toolbar/workbench definitions are preserved. No submodule pin,
document identity or geometry service changed.

**Build/source checks:** SketcherGui and dependencies built successfully in the
retained freecad_1.1.4_context tree with MSVC 19.44, Qt 6.8.3, Python 3.12 and the
existing libpack, concurrency 3. Final Plus scripts were synchronized afterward.
All 51 Plus Python files parse and match the development payload byte for byte;
whitespace checks pass.

**Native/visual acceptance:** four focused persistence cases passed in 33.901
seconds. The focused BIM status-control case passed in 6.235 seconds. The final
27-case TestPlusToolbars suite passed in 204.516 seconds, zero failures, errors or
skips, normal exit 0 and empty stderr. Tests use native Plus button clicks and viewport picks to
verify Equal followed by Construction, retained construction indices, one Undo
entry per command, Undo/Redo, off/Classic behavior, rejected inputs with no Undo,
plain replacement, Escape, empty click, Delete and sketch-exit cleanup. The saved
toggle's default, rebuild and Design-only scope pass. The BIM case verifies native
parent/actions and visibility through presentation and workbench changes. Existing
categories, Curve Intent, directional boxes, native split defaults, custom toolbars,
Spreadsheet controls, captions and idle behavior also pass.

The inspected final native framebuffer shows both dashed construction lines
selected with native Equal constraint symbols. The earlier focused image was blank
and was not accepted as visual evidence; the combined run produced visible geometry.

**Validation corrections:** the initial operation fixtures picked nothing because
an animated camera retained inconsistent position/clipping while the native window
was unexposed. The sketch fixture now disables animation before camera setup; the
isolated runner explicitly hide/shows and exposes its own Qt window. A diagnostic
then verified native picks and exposure. The first exposed inventory run found the
BIM status-toolbar ownership bug corrected above. The first focused BIM assertion
also assumed a visible status-bar parent; the test now shows that parent and restores
its original state. Neither fixture correction changes application preferences or
production rendering. Final combined acceptance includes the production fixes.

**Inventory/restart acceptance:** the separate audit passed all twenty registered
workbenches (nineteen baseline workbenches plus None), 240 native toolbar-group
instances and 1,169 per-workbench command occurrences. No omissions, stolen native
widgets/actions or Classic restoration failures remain in this audit. Exit was 0;
stderr contains only the existing missing OpenSCAD executable notice, so external
executable availability is not certified. Separate prepare/shutdown and restart
processes both passed with exit 0 and empty stderr. Persistent and Directional off,
Tangent Curves, Faces unchecked, Pocket default and hidden File/shown Edit Classic
toolbar preferences survived independent restart.

**Delivery/stopping boundary:** full Persistent Selection across operations, Layers,
remaining confirmed placements and separately owned Plus operations/tasks are still
unfinished. Both development/reference shortcut targets and working directories
remain verified; neither shortcut was changed. No remote publication or release was
performed. This is a development-payload increment, not owner packaging. Remove only
this task's generated validation output after recording results and committing.

## TB.2c2c Plus Sketcher click selection — October 11–12, 2026

**Implementation:** completed plain point/edge/constraint clicks in Plus Design now
replace the preceding selection; repeated plain clicks retain the clicked item.
Ctrl/Shift retain native multiselection and modified empty clicks preserve the
selection. An ordinary empty click clears it. Escape with an idle selection clears
it without exiting sketch edit. Drawing-handler/drag Escape behavior remains native.
The existing Design presence flag scopes these rules independently of Directional
Selection's checked state. Classic keeps its original click/toggle behavior.

Replacement occurs on release after native click/drag classification and retains
hover metadata needed to commit the native pick. It does not preempt drag starts,
box selection or right-click handling. Native admission, mapped names, occurrence
paths and Curve Intent expansion remain in use. No document identities, geometry,
properties, command wrappers or saved preferences were added. This implements the
confirmed click prerequisite; it does not implement operation retention or expose
a nonfunctional Persistent Selection toggle. Architecture owns the detailed scope.

**Build/source checks:** SketcherGui and its required dependencies built in the
retained `freecad_1.1.4_context` tree with the existing MSVC 19.44, Qt 6.8.3,
Python 3.12/libpack configuration and concurrency 3. Final FreeCADPlusScripts
synchronization passed. All 51 Plus Python files parsed and match the payload byte
for byte; whitespace checks passed. The only production source change is the
scoped ViewProviderSketch integration. Classic toolbar/workbench definitions,
submodule pins and licensing are unchanged.

**Native/visual acceptance:** three focused cases passed in 36.828 seconds. All
22 TestPlusToolbars cases then passed together in 158.107 seconds, zero failures,
errors or skips, normal exit 0 and empty stderr. New native mouse/key tests cover
sequential/repeated point, edge and constraint picks; Ctrl/Shift addition/removal
and empty clicks; plain empty clearing; selected Escape remaining in edit; Classic
toggling; Directional-off independence; Connected Curves replacing prior picks;
and multi-curve box selection followed by a plain replacement. The constraint case
locates the rendered native symbol through bounded hover before clicking it.
Inspected viewport pixels show only the newly clicked third curve highlighted,
with the previously selected connected pair unselected. Existing categories,
directional selection, native split buttons, custom toolbars, Spreadsheet widgets,
caption layout and idle behavior also pass.

The separate audit passed all twenty registered workbenches with exit 0: 240
Classic toolbar-group instances and 1,169 per-workbench command occurrences, no
omissions, preserved native action/widget ownership and restored visibility. Audit
stderr contains only the existing missing OpenSCAD executable notice; this does
not certify external executable availability. Separate prepare/shutdown and restart
processes both exited 0 with empty stderr. Saved category/Curve Intent/Directional,
Pocket default and hidden File/shown Edit Classic toolbar preferences persisted.

**Validation corrections:** source review identified that the ordinary selection
clear also resets hover; replacement now explicitly retains that native metadata.
The first focused run exposed malformed temporary profile XML and the existing
synthetic box-after-click fixture ordering issue. The isolated profile is now
created and parsed with ElementTree, and the established box-before-click sequence
verifies the intended native interaction. Final focused and full results include
these corrections; the point/edge/modifier/Escape and rendered-constraint cases
also passed before the fixture correction.

**Delivery/stopping boundary:** Persistent Selection, Layers, remaining curated
placements and separately owned Plus operation/task workflows remain unfinished.
This is not completion of TB.2 or owner packaging. Both development/reference
shortcuts' targets and working directories remain verified. No remote publication
or release was performed. Remove only task-generated validation output after
recording results, retaining the development build, reference build and settings.

## TB.2c2b Design selection categories — October 11, 2026

**Implementation:** the separate Plus Selection row now includes the confirmed
checkbox menu for Planes, Bodies, Surfaces, Faces, Edges, Curves, Points and
Vertices. All start checked to preserve existing access; changes are saved across
ribbon rebuilds, presentation changes and independent restart. Classification uses
native geometry, mapped element resolution and linked occurrence ownership. Sketch
endpoints remain independently selectable as Points when Curves is off. Objects
outside this geometry taxonomy retain their native admission.

A dedicated native Plus gate intersects command rules for viewport hover and
single/batch selection, including Sketcher's existing box-selection path. It never
replaces the command gate; removing a command gate leaves category filtering
intact. The scope exists only during native viewport input in Plus Design. Classic,
other modes and programmatic/tree selections retain their native behavior. Existing
selection is not retroactively cleared by checkbox changes. No geometry, document
properties, identities, ownership or Undo state change. Architecture owns the gate
lifetime, event scope and classification contract.

**Build/source checks:** FreeCADGui and FreeCADPlusScripts built successfully in
the retained full `freecad_1.1.4_context` tree using the existing MSVC 19.44,
Qt 6.8.3, Python 3.12 and libpack configuration, concurrency 3. The final corrected
scripts were synchronized afterward. All 51 Plus Python files parsed and match the
payload byte for byte; whitespace checks passed. Native changes are confined to
the shared Selection integration. Classic toolbar/workbench definitions, submodule
pins and licensing are unchanged.

**Native/visual acceptance:** four focused category cases passed together in
30.264 seconds. The complete nineteen-case TestPlusToolbars suite then passed in
120.922 seconds, zero failures/errors/skips, normal exit 0 and empty stderr. New
checks cover real checkbox-menu clicks, all eight geometry classifications, linked
paths, native hover and command-gate intersection, standard object/element box
selection, mapped Sketcher clicks, Sketcher batch selection and independent Points/
Curves filtering. Classic/programmatic selection and command-gate ownership are
preserved. Existing split-button defaults, custom toolbars, Spreadsheet widgets,
Curve Intent, Directional Selection, captions and idle behavior also pass. Inspected
native captures confirm all eight checkbox labels/check states, the top Selection
row and the Sketcher enclosure rectangle.

The separate audit passed all twenty registered workbenches with exit 0: 240 native
toolbar-group instances and 1,169 per-workbench command occurrences, no omissions,
preserved action/widget ownership and restored Classic visibility. This verifies
command/control inclusion. Audit stderr contains only the existing missing OpenSCAD
executable notice; external executable availability is not certified. Separate
prepare/shutdown and restart processes both exited 0; Faces
unchecked, Tangent Curves, Directional Selection off, the Pocket default and hidden
File/shown Edit Classic toolbar preferences persisted.

**Validation corrections:** the first run exposed an incorrect preselection-clear
API name; the controller/test now use native `clearPreselection`. The Sketcher
fixture now supplies explicit hover and exercises box selection before its click
assertion so the intended rubber-band input is realized. Its rejection assertion
was corrected to preserve independently enabled endpoint Points; disabling Points
as well produces an empty box selection. Native traces and the inspected rectangle
confirmed actual batch admission. Final focused/full results include these changes;
no production Sketcher source changes were required.

**Delivery/stopping boundary:** Persistent Selection, Layers, remaining curated
placements and separately owned Plus operation/task workflows are unfinished; TB.2
is not complete. The development and retained reference shortcuts' exact targets
and working directories were re-read and verified. This is a development-payload
increment, not a packaged release. No remote publication was performed. Remove only
this task's temporary validation output after recording evidence; preserve both
builds and unrelated settings.

## TB.2c2a Design Curve Intent — October 11, 2026

**Implementation:** the separate Plus Selection row now includes a native-icon
split button for Single Curve, Connected Curves and Tangent Curves. The arrow opens
all choices, selecting one changes the main icon/action, and the saved choice
survives tab rebuilds and presentation changes. Single Curve is the default.
Expansion applies to viewport edge picks in Plus Design only; Classic, other modes
and scripted command/collector selections retain their existing behavior.

Native geometry supplies endpoint topology, tolerances and tangents. Traversal
stays within the selected owner/occurrence, stops at tangent branches or corners,
and keeps closed single curves separate. Solid edges require shared vertices.
Mapped element names use native resolution; edited sketches retain construction
geometry indices while normal views use displayed shape indices. Every expanded
entry goes through native selection admission. A per-input-event adjacency cache
avoids repeated graph construction during box selection and is discarded before
later edits. No document geometry, identities, ownership or Undo state changes.
Architecture owns the detailed contract and implementation tolerances.

**Build/source checks:** CMake generation and FreeCADPlusScripts synchronization
passed in the retained full `freecad_1.1.4_context` development tree. All 50 Plus
Python files parsed and match the payload byte for byte; whitespace checks passed.
This increment changes Plus Python code/tests/manifests only. Native workbench
source, Classic toolbar definitions, submodule pins and licensing are unchanged;
the existing full native build remains applicable.

**Native/visual acceptance:** all fifteen TestPlusToolbars cases passed together in
84.587 seconds, zero failures/errors/skips, normal exit 0 and empty stderr. New
cases cover actual split-menu/icon clicks, default/saved state, mode scope, native
line/arc tangent chains, branches, closed curves, overlapping independent solids,
linked occurrence paths and Sketcher construction indices. Real model box picks
exercise all three intents and native filter rejection; a real Sketcher click
exercises mapped names and connected construction geometry. Programmatic selections
and Classic remain unchanged. Existing directional selection, native arc defaults,
custom toolbars, Spreadsheet widgets, captions and idle behavior also pass.
The inspected native ribbon capture confirms the separate icon/arrow control in
the top Selection row with the original ribbon groups intact.

The separate native audit passed all twenty registered workbenches with exit 0:
240 toolbar-group instances and 1,169 per-workbench command occurrences, no
omissions, preserved Classic action/widget ownership and restored visibility.
The existing OpenSCAD external-executable notice remains; this verifies toolbar
coverage, not external solver availability. Separate prepare/shutdown and restart
processes both exited 0. Tangent Curves, Directional Selection off, the Pocket
default and hidden File/shown Edit Classic toolbar preferences all persisted.

**Validation corrections:** the first Sketcher click fixture overlapped its axis
and needed explicit hover motion. Subsequent native clicks exposed mapped names
that the initial plain-edge parser missed; native element resolution corrected
this. The construction-index case also distinguished edited geometry from normal
Shape edge numbering; the implementation now follows the active native context.
Final focused and full-suite results above include these fixes.

**Delivery/stopping boundary:** Category filtering, Persistent Selection and Layers
remain unfinished, as do separately owned Plus operation/task workflows. This
increment is not completion of TB.2. Both development/reference shortcut targets
and working directories were re-read and verified. No remote publication or release
was performed. Remove task-generated validation output after recording results;
retain the development build, reference payload and unrelated settings.

## TB.2c1 Design Directional Selection — October 11, 2026

**Implementation:** the separate Plus module now provides the confirmed Directional
Selection control beside the common Design tools. It defaults on and saves its
choice. The transient policy is removed in Classic and other modes. Standard native
Box Selection/Box Element Selection and Sketcher's existing selection mechanism
apply full enclosure left-to-right and crossing right-to-left when on; off requires
full enclosure in either direction. Native traversal, geometry extraction and
command selection gates remain authoritative. Classic retains its original center/
crossing behavior. Crossing and enclosure have distinct dashed/solid colored
feedback. The standard-tool marker is cleared on completion/Escape; Box Zoom and
feature-specific pickers retain their own native behavior. No document identities,
properties, geometry or source ownership change. Architecture owns the integration
contract. Curve intent, category filtering, operation persistence and Layers remain
unimplemented; this does not complete TB.2 or the Selection toolbar.

**Build/source checks:** FreeCADGui, SketcherGui and FreeCADPlusScripts built
successfully in the retained `freecad_1.1.4_context` tree with the existing MSVC/
Qt/Python/libpack configuration and concurrency 3. Final script synchronization
passed. All 49 Plus Python files parsed and match the development payload byte for
byte. Diff whitespace checks passed. Original toolbar definitions, workbench
availability, submodule pins and licensing remain intact.

**Native/visual acceptance:** all twelve TestPlusToolbars cases passed together in
60.725 seconds, zero failures/errors/skips, normal application exit 0. New actual
mouse drags validate partial/full enclosure for model objects, subelements and
sketch edges, saved/default toggle state, Design-only scope, Classic restoration,
command gate rejection and Escape/Box Zoom cleanup. Existing split-arrow/icon clicks,
last-used choices, specialized widgets, custom groups and caption checks also pass.
Inspected normal-framebuffer captures show green dashed crossing and solid enclosure
rectangles around the actual model and sketch geometry.

The separate all-workbench audit also passed with normal exit 0: all nineteen
Classic workbenches plus None, 240 toolbar-group instances and 1,169 per-workbench
command occurrences, without omissions. Classic action/widget ownership, visibility
restoration and Plus suppression passed. The OpenSCAD external-executable notice
remains; toolbar coverage does not certify external CAD/CAM/FEM executables.

Independent prepare/normal shutdown and restart processes both exited 0. Directional
Selection remained off after restart, while the saved Pocket choice and hidden File/
shown Edit Classic toolbar preferences also survived. Both shortcut targets and
working directories were re-read and verified; the new development shortcut still
points to the retained development executable and the archived reference shortcut
remains intact.

**Validation corrections:** ordinary Qt viewport grabs returned black images. The
existing Windows normal-framebuffer reader was extended to capture an active drag
without changing selection/mouse position and to restore the prior OpenGL context.
Initially releasing that context caused a native release-event exception and left
the standard box tool active; the isolated case and final full suite pass after
the helper correction, with empty final stderr. An isolated capture was blank;
final suite captures were inspected for actual geometry and rectangle feedback.
A legacy Windows PowerShell wrapper lost the completed audit's process exit code;
its inventory assertions passed, and the final audit passed with exit 0 using the
established PowerShell runtime. These were harness corrections, not additional product behavior.

**Delivery/stopping boundary:** this is a validated development increment. No remote
publication or release was performed. Preserve the complete Classic inventory and
continue remaining confirmed Selection/Layers work separately. Remove this task's
generated validation output after the durable record; retain the useful build and
all unrelated profiles/reference payloads.

## TB.2b Complete captions and icon-only unavailable controls — October 11, 2026

**Implementation:** the separate Plus ribbon now keeps unavailable medium/small
controls icon-only, using the existing native forbidden icon with their complete
accessible names and explanatory tooltips. They remain disabled. Available commands
retain their original icons, shared actions and split menus. Large-button and group
captions use literal text with at most two balanced lines; long words retain their
natural width. The ribbon reserves enough height for its content and horizontal
scrollbar, so bottom captions remain visible. This implements the existing confirmed
presentation rules; no new pixel-size specification, operation or geometry behavior
is introduced.

**Build/source checks:** FreeCADPlusScripts synchronization passed in the retained
complete `freecad_1.1.4_context` development tree. All 48 Plus Python files parsed
and match that payload byte for byte. Diff whitespace checks passed. This change
is Python presentation/test code only; the prior full native build remains applicable.

**Native/visual acceptance:** all nine TestPlusToolbars cases passed together in
31.014 seconds, zero failures/errors/skips and normal application exit 0. The new
case requests a 1000 by 760 logical-pixel window and checks the normal font and a
1.5-times font. Actual FEM captions retain their complete text in at most two lines,
fit their rendered width/height and remain above the scrollbar; overflow still
scrolls to the final groups. Modeling placeholders have native icons, disabled state,
tooltips and accessible names. Inspected final narrow/enlarged FEM and Modeling
captures confirm these behaviors. Existing actual arc clicks, remembered choices,
Classic restoration, custom groups, specialized widgets and no-idle-rebuild tests
also passed.

A separate native audit passed all twenty registered workbenches after the shared
layout changes: the same 240 toolbar-group instances and 1,169 per-workbench command
occurrences as TB.2a, no missing commands or widget controls, and preserved Classic
parents/actions/visibility. These repeated common groups are not unique command totals.
An OpenSCAD external-executable-not-found notice was recorded; it did not affect
workbench/toolbar inclusion and this audit does not certify external CAD/CAM solvers.
Independent preference restart was already validated in TB.2a and was not repeated
for this presentation-only change.

**Validation corrections:** the first generated test profile had malformed XML;
it was corrected and parsed before the final fresh-profile run. The first caption
assertion incorrectly measured a multiline string as one line; the final check
measures each rendered line and its combined height. Programmatic workbench switches
now explicitly refresh presentation before captures, matching native queued UI refresh.
These were harness corrections; they do not establish pre-existing application faults.

**Delivery:** both shortcut targets and working directories were re-read and verified.
Use `freecad plus 0.1.0.lnk` for the updated development payload. The archived shortcut,
reference build, original workbench source, native toolbar definitions and submodules
remain untouched. No remote publication or release was performed. Task-generated
validation output is removed after this durable record; useful builds are retained.

## TB.2a Complete Classic workbench/toolbar inclusion — October 11, 2026

**Implementation:** All Tools copies the complete ordered native toolbar inventory
into Plus-owned groups, including common/global groups, workbench/global custom
bars, separators, expanded command groups and specialized controls. All registered
workbenches retain mode/tab routes; opening the selector discovers later registrations.
Closing Customize refreshes live changes. Native command/widget factories create
separate workbench selectors and Spreadsheet color pickers without moving Classic
widgets. Icons, native split menus, command state and dispatch remain shared.
Plus combined groups remember stable command IDs across native wrapper recreation.
Original workbench source, baseline build flags, submodule pins, licensing and
Classic toolbar ownership remain unchanged.

**Build:** retained `freecad_1.1.4_context` under the mandated test-builds root;
`cmake --build ... --target src/all data/all --parallel 3` finished all 4,225 steps
with exit 0. This uses the existing MSVC 19.44, Qt 6.8.3/Python 3.12 libpack 3.1.1.3
configuration. The final SpreadsheetGui adapter rebuild and FreeCADPlusScripts
synchronization also passed. No official Python 3.11 binaries were mixed into this
payload. All 48 Plus Python files parsed and match the deployed scripts byte for byte.

**Native acceptance:** eight TestPlusToolbars cases passed together in 24.110 seconds,
zero failures/errors/skips, normal application exit 0. Coverage includes actual
Sketcher dropdown-arrow/menu/icon clicks, last-used icons, editor navigation guards,
Home/tab navigation, independent preferences, Classic contextual restoration,
separate native controls, expanded groups, later-added workbenches, global and live
custom toolbars, and no idle rebuild. Spreadsheet foreground/background selections
changed actual A1 cell colors, each through one native handler dispatch and one
Undo entry; Undo restored state and the originals kept their parents.

A separate native process audited every registered workbench (nineteen plus None).
All passed: no missing commands, missing widget copies, substitute placeholders for
registered commands, or omitted workbench routes. Native action identity, separate
widget class/ownership, original toolbar parents/actions, restored visibility and
Plus suppression were checked. Counts below are per workbench; common groups and
commands recur across rows (240 group instances, 1,169 command occurrences total).

| Workbench | Native/Plus groups | Commands |
| --- | ---: | ---: |
| Assembly | 11 | 53 |
| BIM | 18 | 142 |
| CAM | 13 | 55 |
| Draft | 14 | 96 |
| Fem | 19 | 99 |
| Inspection | 9 | 34 |
| Material | 10 | 35 |
| Mesh | 15 | 66 |
| None | 0 | 0 |
| OpenSCAD | 11 | 47 |
| PartDesign | 13 | 62 |
| Part | 12 | 68 |
| Points | 10 | 40 |
| ReverseEngineering | 10 | 35 |
| Robot | 10 | 44 |
| Sketcher | 16 | 86 |
| Spreadsheet | 10 | 49 |
| Surface | 10 | 40 |
| TechDraw | 19 | 80 |
| Test | 10 | 38 |

**Restart and visual acceptance:** prepare/normal shutdown and a separate restart
both exited 0. The saved Pocket default reappeared in Plus; Classic restored hidden
File and shown Edit toolbars. Inspected Modeling, CAM, Assembly, Draft, FEM, Drawing
and Spreadsheet ribbon captures: original icons and split arrows, named groups,
separate native workbench selector/color widgets and reachable overflow groups.
FEM and Drawing end positions visibly expose the rightmost groups through horizontal
scrolling. These are Qt ribbon captures, not 3D-rendering or every-operation evidence.

**Failures resolved during validation:** a dynamic workbench exposed a stale
QStandardItem wrapper, so the selector now owns plain mode data in a QAbstractListModel.
The combined test then reproduced an invalid captured QAction wrapper with the same
native pointer as the live menu action; remembering native command data fixes selection
persistence without changing shared Qt wrapper infrastructure. The live custom-bar
fixture now explicitly shows its initial native bar before testing visibility restore.
Spreadsheet's legacy test selection API requires integer flags; passing a Qt 6 enum
caused native failures. Using `.value` fixes the test; native editor code is unchanged.
The copied picker is attached/owned directly by its separate native QToolBar.
Final combined, audit and independent-restart runs passed after these corrections.

**Development delivery and limits:** `freecad plus 0.1.0.lnk` still targets this
build's `bin/FreeCAD.exe` with its `bin` working directory, and the target exists.
The archived `FreeCADPlus.exe - Shortcut.lnk` and reference payload remain unchanged.
Restart using the development shortcut to load the complete workbench build.
This closes Classic inventory coverage, not every underlying CAD/CAM/FEM operation,
remaining curated Plus layouts, Selection/Layers, or unfinished Plus-only commands.
No release, deployment or remote publication was performed. Task-generated validation
files are removed after this durable record; the complete build and unrelated saved
profiles/reference builds remain available.

## TB.1 Separate Plus toolbar foundation — October 11, 2026

Historical acceptance below used the earlier partial payload. TB.2a above supersedes
its workbench/widget coverage limits; its original evidence remains recorded.

**Implementation:** Plus owns its layout and widget tree in toolbar_layout.py and
toolbars.py. It copies ordinary native toolbar actions/menus without moving Classic
widgets, duplicating command callbacks or adding shortcut copies. Design has the
six-group Modeling arrangement plus Home/Sketch/Surface/Assembly/Mesh/View and
retained Part/More access. Other registered modes use copied native groups with
Home/Tools/View. File/Edit/Clipboard remain above the ribbon. Mode/tab navigation
uses native workbench activation and protects active tasks/editors. Missing
workbenches are disabled, while all registered workbenches remain selectable.

Native group menus retain Classic right-arrow/main-icon behavior and last-used
choice. Separate Plus combined groups persist their selected command. Primitives
keeps the unimplemented Tab option disabled without changing Classic's menu.
Unimplemented Add Reference Object is disabled. The toolbar preference remains
independent of model and task preferences. A narrowly scoped native guard preserves
Classic logical visibility during existing native workbench setup/save/restore and
Sketcher context operations; ARCHITECTURE owns this contract.

**Build:** FreeCADGui and FreeCADPlusScripts passed in the retained
`test-builds/freecad_1.1.4_context` tree (exit 0; 33 native build steps). Final script
synchronization passed. This required no new dependency or submodule changes.

**Native validation:** final four-case run passed, zero failures/errors/skips,
12.288 seconds, normal process exit 0. Covered real mouse clicks on the native arc
arrow, child menu choice and main icon; exactly one invocation, remembered icon,
unchanged menu contents, Classic/Plus switching inside a live sketch and correct
native contextual toolbars after leaving edit; widget/action ownership; independent
preferences; mode/tab navigation and active-task guard; disabled unavailable
workbenches; preserved native primitive menu with Plus-only disabled Tab; saved
combined-group selection and no idle page rebuilds. Modeling, Sketch and View Qt
widget captures were inspected. This does not claim viewport/framebuffer acceptance.

**Independent restart:** normal close preparation and a second native process both
passed (exit 0). Plus reopened, Pocket remained the selected Extrude-group action,
and switching to Classic restored the saved hidden File and shown Edit toolbars.
No geometry/persistence suites were repeated for this presentation-only change.

**Corrections and limits:** the first event-filter implementation caused a native
access violation on workbench change; it was replaced by a narrow visibility signal
handler and the failed arc case then passed. A later assertion incorrectly expected
Sketcher's context-only Geometries toolbar outside editing. Inspection also exposed
native SaveState persistence under Plus suppression; the opt-in native guard fixes
that path while retaining the native policy branches. The final suite includes both
in-edit and out-of-edit restoration. Logs retain the known missing Std_Measure notices
in this partial development payload; the corresponding ribbon control is disabled.
CAM, Draft/Drawing, FEM, Surface, Assembly and Mesh runtime coverage is not claimed:
this payload registers None, Material, Part, PartDesign and Sketcher only. Full
workbench build coverage, precise remaining tab layouts/sizing, single-widget custom
toolbar controls, Selection/Layers and unfinished Plus operations remain TB.2/separate
operation work. Native menus retain access to original commands.

**Development delivery:** the existing `freecad plus 0.1.0.lnk` was reopened and
verified to target this tree's `bin/FreeCAD.exe`, with its `bin` working directory
and executable present. The archived `FreeCADPlus.exe - Shortcut.lnk` and its
`freecad_plus_2026-10-10_part_types_payload/FreeCADPlus.exe` target were preserved.
Restart through the development shortcut to load the rebuilt native library and
scripts. No release packaging or remote publication was performed. Task-generated
validation output is removed after this durable record; the useful build/profile
outside this task's validation directory is retained.

## Native New Part catalog correction - October 11, 2026

**Owner decision:** New Part creates a Models definition only; Part Tree placement
is a different action. See the evidence ledger and Component Panel specification.

**Reproduction:** native Std_New + Std_Part created an ordinary App::Part without
PlusFormat, leaving both Models and Part Tree empty. Calling the established
component document initializer populated both tabs. The defect was missing native
command integration, not a missing panel refresh.

**Implementation:** Std_New uses the existing component initializer in both UI
presentations, preserving the separately confirmed Part001/initial-instance/Edit
contract. Std_Part uses hierarchy.new_part in component/empty documents, creating
one uniquely named definition only. It preserves current Edit/selection and creates
no occurrence or temporary unused-edit row. External editing targets the defining
file's catalog and Undo stack. Empty native files initialize a frame plus unused
definition atomically. Nonempty legacy files retain native ownership; implicit
migration is not part of this correction. The full storage chooser and separate
placement task remain unfinished. ARCHITECTURE owns the technical boundary.

**Build:** FreeCADGui and FreeCADPlusScripts passed, exit 0, retained
`test-builds/freecad_1.1.4_context`. Native build log ended at 144.848 seconds.
A command quoting error was corrected before compilation; no application defect.
The completed test script was then deployed with FreeCADPlusScripts only.

**Acceptance:** three focused native cases passed on the first test run in 3.095
seconds (process exit 0, 8.23 seconds). Covered actual Std_New/Std_Part entry points,
Plus and Classic, automatic Part001, repeated unique definitions, Models refresh,
unchanged instance count/Edit/object identities, one-step Undo/Redo, empty native
initialization, external source-owned creation and Undo, and existing legacy
ownership preservation. Independent reopen passed in 5.14 seconds, exit 0: exact
object identities, three Models definitions, and only the original Part Tree
instance. Logs contain the already-known Std_Measure notices. No unrelated geometry
or operation suites were repeated. All scoped acceptance checks are complete.

**Development delivery:** modified Python sources parse and match the retained
payload; native source line endings and whitespace were checked. The reopened
`freecad plus 0.1.0.lnk` targets that build's bin/FreeCAD.exe with bin working
directory; the old shortcut remains unchanged. Restart using the current shortcut
and create a new document to use this corrected path. Existing nonempty legacy
files still require their separately scoped conversion flow. No release package
was created. Task-owned `g1_component_creation` artifacts are removed after this
record. Stop; next implementation is the separately scoped placement workflow or
remaining normal component-document integration, only when requested.

## Components above Properties follow-up - October 11, 2026

**Authority and implementation:** the owner explicitly places Components at the
left top with Properties below. The presentation controller establishes a vertical
left dock split on Plus startup, return from Classic, or a changed native property
dock. Routine workbench refreshes do not repeat docking or resize the split.
Both combined and independent native property layouts use their existing editor.

**Build and bounded check:** FreeCADPlusScripts deployment passed (exit 0).
One isolated native process passed all four placement checks in 7.50 seconds,
exit 0: combined startup, PartDesign workbench switch, Classic-to-Plus return,
and independent Property view. Both docks were visible, in the left dock area,
aligned at the same width and vertically separated rather than tabbed. At startup
Components occupied y=124..397 and Properties y=402..818; workbench activation
retained the exact geometry. No unrelated geometry suites were repeated.

**Delivery:** source syntax and payload byte equality checked; the existing
`freecad plus 0.1.0.lnk` still targets this retained development build and bin working
directory. The archived shortcut remains unchanged. Restart the application from
the current shortcut to load the correction. This is development build delivery,
not a separate release. Validation artifacts in `g1_components_dock_order` are
removed after recording these results. All scoped checks passed; stop here.

## G1.6d Independent Classic/Plus UI sections - October 11, 2026

**Authority:** direct owner instruction, recorded in the [evidence ledger](ui-ux-specs/EVIDENCE_AND_DECISIONS.md#independent-classic-and-plus-ui-sections---october-11-2026).
Three independent dropdowns lead General/Application: model/components, toolbars,
and task-panel workflows. All default to Plus. This supersedes the developer-only
startup boundary. Both presentations share the updated backend; toolbar/task Plus
presentations start from Classic definitions and are redesigned later.

**Implementation:** native General preferences persist the three choices. InitGui
installs an event-driven presentation controller. Plus shows Components and keeps
the native property editor; Classic restores the native tree. Both combined and
independent native tree/property layouts are handled. Components has a normal
Panels-menu toggle. Hiding or switching its managed dock retains backend observers,
Edit context and active tasks. Workbench changes restore its menu availability;
there is no idle polling. Toolbar/task options share the existing native command
and task definitions initially, avoiding a second callback/modeling engine.

Pad and Pocket already route to the same native FeatureExtrude engine with their
additive/subtractive options. Existing component admission rules remain independent
of presentation. This increment preserves that route; it does not claim a completed
consolidated Plus Extrude task or all future Classic adapters. The [technical
contract](ARCHITECTURE.md#independent-ui-presentations-g16d) records the boundary.

**Build:** FreeCADGui + FreeCADPlusScripts passed, exit 0, 207.42 seconds, in the
retained `test-builds/freecad_1.1.4_context` tree. Original native source line endings
were retained. Later changes needed only script deployment; no native corrective
build was required.

**Bounded validation and corrections:** the first harness looked for Preferences
before it was ready and left its modal call waiting. Only that recorded test PID
was stopped after 55.39 seconds; this is not an application crash. Dialog discovery
now uses top-level widgets and a finite readiness retry. The four-case run then took
8.399 seconds (native exit 0, 13.09 seconds overall): startup/defaults/Cancel, all
eight combinations and Apply/persistence passed; the task test used a direct Length
assignment that the native dialog replaced on acceptance. It now sets the actual
length field. The affected task case and persistence fixture passed in 4.816 seconds
(native exit 0, 9.52 seconds). No production correction was needed for those failures.

Source review identified the existing independent tree/property layout as a second
native tree presentation. The controller now also hides/restores that standalone
tree without hiding Properties. Its one focused case passed in 2.800 seconds
(native exit 0, 7.44 seconds). All five acceptance groups have passed; completed
unrelated geometry suites were not repeated.

Covered normal Plus startup, actual Preferences row order/text/defaults, Cancel,
Apply, mixed settings, all eight combinations, unchanged object IDs/Undo/Edit and
toolbar command identities, menu close/reopen, workbench changes, both native tree
layouts, and live native Pad/Pocket tasks across mode switches. The cylinder and
pocket volumes were 20*pi and 19.5*pi; Pocket Undo/Redo and Reference refusal in both
presentations passed. The actual Application-group capture was visually inspected:
three aligned dropdowns precede Theme and existing settings; no clipping. The capture
shows the cancelled Classic draft; default Plus values were separately asserted.

Independent restart passed, native exit 0, 5.45 seconds: Classic/Plus/Classic choices
persisted, saved object identities and feature links survived, and increasing the
pocket depth to 3 recomputed the valid model to 19.25*pi. Final logs retain known
Std_Measure notices. No long-session jitter or complete Group 1 acceptance is claimed.

**Development delivery:** reopened both desktop shortcuts. `freecad plus 0.1.0.lnk`
points to the rebuilt `freecad_1.1.4_context/bin/FreeCAD.exe`, with that bin directory
as its working directory. The old `FreeCADPlus.exe - Shortcut.lnk` still points to
`freecad_plus_2026-10-10_part_types_payload/FreeCADPlus.exe`. Both targets exist;
no shortcut or owner settings were changed during validation. The new shortcut now
loads automatic UI-mode integration on its next launch. No separate release package
was created. Earlier manual-activation-only delivery notes below are historical.

**Final checks:** all 45 Plus Python scripts parse and match the retained payload;
UI XML parses; original native LF/CRLF choices are retained and whitespace passes.
Test mode acceptance skips outside an explicitly isolated PLUS_TEST_DIR. The final
test guard/docstring-only edits were deployed and syntax checked; runtime work is
complete. Task artifacts `g1_ui_modes` are removed after recording durable results.


**Publication:** source/acceptance checkpoint
`8cbfa2cad86b8c0f4f00e7c156e71a65d7c5a023` pushed to
origin/codex/freecad-1.1.4-baseline; exact remote revision verified. Development
shortcut delivery is verified above; no separate release package. This publication
record is a separate documentation commit.


## Separate development shortcut - October 11, 2026

At the owner's explicit request, created desktop `freecad plus 0.1.0.lnk` targeting
`C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds/freecad_1.1.4_context/bin/FreeCAD.exe`,
with the same `bin` directory as its working directory. Reopened the saved shortcut
and verified both paths and executable existence. The original desktop
`FreeCADPlus.exe - Shortcut.lnk` still targets the archived fork; its SHA256 was
identical before and after creation. Preserve that link/build for future reference.

This is access to the latest development executable and deployed G1.7b3t
implementation, not a new package or Group 1 completion. No executable rebuild or
additional runtime test was performed for this shortcut-only request. The component
panel remains explicitly enabled; this direct executable shortcut adds no startup
macro or automatic activation. Current shortcut instructions now preserve both links.


## G1.7b3t Split/join property-editor admission - October 11, 2026

**Authority and scope:** applies the owner's Reference prerequisite and existing
edited-component ownership contract to native property input editing. No new design
choice or operation workflow was needed. Tree drop/replacement is a separate entry
point and remains next. See the [technical contract](ARCHITECTURE.md#splitjoin-property-editor-admission-g17b3t).

**Implementation:** the existing native link-dialog/property-item preflight uses an
explicit mapping of seven upstream Python proxy types and eleven input properties:
Fragments/XOR/Connect Objects, Slice Base/Tools, Embed/Cutout Base/Tool and generated
CompoundFilter Base/Stencil. It checks additions before mutation, keeps the dialog
open on refusal, permits removal, and checks every selected target before any
multi-feature write. Only local inputs in the edited definition's defining file
are supported. Legacy documents bypass the Plus import; unrelated Python feature
properties retain native behavior. Native algorithms and dependency links remain.

**Build:** FreeCADGui + FreeCADPlusScripts passed, exit 0, 153.62 seconds, using the
retained `test-builds/freecad_1.1.4_context` tree. No production corrections or
additional native builds were needed after this build.

**Harness corrections and bounded runs:** the initial six cases ran in 25.089
seconds (native exit 0, 30.09 seconds overall): four passed, two stopped on harness
issues. An accepted dialog may already be destroyed, so its lifetime check was
corrected. The replacement fixture now preserves the replaced box's offset, avoiding
an unintended empty XOR. A two-case rerun took 9.662 seconds (native 14.55 seconds)
and exposed missing property-click transaction setup and an unopened Base editor.
The new tests now click the actual property cell and explicitly finish its native
transaction before Undo; their unrelated-feature fixture uses an ordinary local
input rather than a nested Body feature. Four affected new cases then took 24.257
seconds (native 28.91 seconds): two passed, while the two Base-editor cases exposed
a category/property naming collision. Source inspection confirmed the default
category is also called Base. The helper now selects only an editable property row.
This was test-harness work, not repeated unrelated regression or a product redesign.

**Final acceptance:** all six planned cases have passed: two original Compound
regressions from the initial run, two context/refusal cases from the corrected
four-case run, and the final two cases after the Base-row fix. That last run had
zero failures/errors/skips, 42.339 seconds (native exit 0, 46.95 seconds overall).
The complete eleven-property case tests refusal without state mutation, continued
acceptance in the same dialog, valid geometry, retained ownership, Undo/Redo and
save. Other cases cover Excluded and unsupported Full Component input; file/wrong
Edit refusal; removal outside component Edit; atomic multi-feature rejection;
legacy list/single/filter properties; and unrelated Python feature bypass. The
existing Compound dialog and legacy checks passed without production changes.

Independent fresh-process reopen/source-edit passed, native exit 0, 6.58 seconds.
All saved object identities, edited input links and owners survived. Increasing
local box heights from 4 to 6 recomputed all eleven valid results to 1.5 times their
saved volumes with unchanged solid counts. Runtime checks stop here. Final logs
retain the known Std_Measure notices. Earlier harness runs also produced editor
activation notices and one scoped-link warning from the superseded Body fixture.
No warning-free claim is made.

**Limits:** these are actual native Qt property dialogs, with API-driven selection
and new-case property-cell mouse activation. No tree drag/replacement coverage,
raw Python assignment interception, new Add Reference Feature workflow, owner
package or shortcut delivery is claimed. Group 1 remains incomplete.

**Final checks:** all 43 Plus Python scripts parse and match the development
payload byte-for-byte. All 126 local links in changed Markdown resolve; whitespace
checks pass. The native edited file retains its original Git LF line endings.
Task artifacts `g1_7b3t_split_properties` are removed after recording these results.
Useful builds remain; no additional runtime work.


**Publication:** source/acceptance checkpoint
`3d6e6ddfdfa73ca2866bc8108ed2333f0ed59bac` pushed to
origin/codex/freecad-1.1.4-baseline; exact remote revision verified. No release,
owner package or shortcut delivery. This publication record is a separate docs commit.


## G1.7b3s Split/join creation integration - October 11, 2026

**Authority:** applies the owner's explicit Reference prerequisite and existing
component feature/History ownership contract. No new design choice was required.
See the [technical contract](ARCHITECTURE.md#splitjoin-creation-integration-g17b3s).

**Implementation:** Boolean Fragments, Slice to Compound, Slice Apart, XOR, Connect,
Embed and Cutout check unresolved occurrence context before a transaction. Accepted
local native results belong to the edited definition; inputs stay owned there.
Slice Apart owns its intermediate Slice and individual native filters directly.
Legacy behavior, native geometry algorithms and Abort/Continue dialogs remain.

**Build and correction:** PartScripts + FreeCADPlusScripts deployment passed in the
retained `test-builds/freecad_1.1.4_context` tree, exit 0, 8.08 seconds. No native
compilation was needed. The initial five native cases took 19.022 seconds (process
exit 0, 23.67 seconds overall): four passed and Slice Apart failed validation.
A targeted diagnostic took 2.106 seconds (process 6.70 seconds) and established
that the generated pieces had the intended owner but duplicate entries within its
Group. Source inspection identified native batch insertion expanding overlapping
coordinate-system links before membership was updated. Sequential native insertion
corrected this; an explicit unique-membership assertion remains. Script deployment
passed after correction. Temporary console-variable cleanup also tolerates an empty
result list; that cleanup-only adjustment was inspected and redeployed.

**Final validation:** all five focused cases have passed: two unaffected initial
cases plus the three ownership/Abort cases rerun after correction, zero failures,
errors or skips, 9.427 seconds (native exit 0, 14.00 seconds overall). Covered all
seven commands' Reference/Excluded/unsupported foreign and file-Edit refusal before
mutation; accepted occurrence-qualified inputs; valid expected volumes and solid
counts; source/result ownership and History; source hiding; Undo/Redo; forced native
Abort rollback including nested Slice Apart; and ordinary legacy policy bypass and
Slice Apart grouping. Earlier Boolean/Compound tests were not repeated.

Independent fresh-process reopen/source-edit passed, native exit 0, 6.19 seconds.
Exact saved object identities, links and owners survived. Raising both input box
heights from 4 to 6 recomputed all six core results to 1.5 times their original
volumes with unchanged solid counts. Slice Apart filters remained valid and their
combined volume changed from 64 to 96. Final logs contain the existing Std_Measure
notices; duplicate-child notices from the failed initial run are absent after the
correction. No warning-free or pointer-driven interaction claim is made.

**Limits and stop:** this covers command creation only. Later split/join property
input edits remain next, and other consumers remain unfinished. Same local-input /
defining-file support boundary as the preceding increments. No reference promotion,
raw assignment hook, owner package, shortcut update or Group 1 completion is claimed.
Runtime work stops here. All 43 Plus scripts and the three changed Part scripts
parse and match the retained development payload byte-for-byte. All 124 local links
in changed Markdown resolve, and whitespace checks pass. Task validation artifacts
`g1_7b3s_split_join` are removed after recording these results; useful builds remain.


**Publication:** source/acceptance checkpoint
`6416f489b13181e13986765c8c92150a58d442ac` pushed to
origin/codex/freecad-1.1.4-baseline; exact remote revision verified. No release,
owner package or shortcut delivery. This publication record is a separate docs commit.


## G1.7b3r Compound link-edit admission - October 11, 2026

**Authority:** applies the confirmed Reference prerequisite and component ownership
contract to existing native Compound inputs. No new operation workflow, reference
promotion or cross-component transfer decision is inferred. See the
[technical contract](ARCHITECTURE.md#compound-link-edit-admission-g17b3r).

**Implementation:** native Compound drop, replacement and Links-property additions
preflight the actual inputs and edited owner. Qualified drops preserve occurrence
context; tree replacement checks that context before its identity-only mutation.
Component compounds force drop-only behavior to retain input ownership. The property
editor checks every selected target before writing any, and its dialog stays open
when admission fails. Removal/reordering does not admit new geometry and bypasses
the addition check. Other property types and legacy behavior remain unchanged.

**Build and corrections:** initial PartGui + FreeCADPlusScripts build passed,
395.88 seconds. Pre-runtime review found that tree replacement lost occurrence
context; its preflight was added and an incremental build passed, 115.55 seconds.
Both used the retained `test-builds/freecad_1.1.4_context` tree.

The initial six native cases ran in 18.286 seconds (native exit 0, 23.17 seconds
wall time): four passed; two failed. The drop case exposed the native extension's
transfer permission despite the base provider's default; component Compound now
explicitly overrides that permission while preserving legacy behavior. The removal
case exposed SubObjectT equality comparing a cached label that picker references
do not populate. A single targeted diagnostic (5.159 seconds, native 10.00 seconds)
confirmed the same target/input identities; admission now compares stable document,
object and subpath identity. Diagnostic instrumentation was removed. The corrective
build passed, exit 0, 289.12 seconds. No further production correction was needed.

**Final validation:** all six focused cases have passed: the two unaffected cases
from the initial run plus four affected cases rerun after correction, zero failures/
errors/skips, 10.685 seconds (native exit 0, 15.56 seconds overall). Covered
Reference/Excluded occurrence rejection, a shared source through a different
Reference occurrence, unsupported foreign input, missing/wrong Edit, drop-only
ownership, native replacement, cleanup, actual Links-dialog refusal/continuation/
removal, atomic multi-property refusal, legacy bypass/transfer behavior, Undo/Redo
and save. Previous creation/Boolean/Section tests were not repeated.

Independent fresh-process reopen/source-edit passed, native exit 0, 5.31 seconds.
Exact identities, source/result owners and ordered Links survived; changing the
added source height from 4 to 6 recomputed the valid two-solid Compound from volume
128 to 160. Runtime work stops here. Logs contain the existing Std_Measure notices
and one Qt `edit: editing failed` notice when the harness requests editing an already
open property editor; its actual dialog continuation/removal assertions passed.
No claim of warning-free logs.

**Limits:** native drop/replacement hooks are exercised through their GUI Python
APIs; no end-to-end pointer drag is claimed. Property editing uses the actual Qt
editor/dialog. This GUI consumer boundary does not hook raw Python assignments,
file restoration or recompute. Same local-input/defining-file support limit as
Compound creation; other geometry consumers remain unfinished. No owner delivery.

**Final checks:** all 43 Plus Python scripts parse and match the retained development
payload byte-for-byte; 122 local links in changed Markdown resolve; whitespace passes.
Task artifacts `g1_7b3r_compound_links` were removed after recording the results.
Useful builds remain. No additional runtime work. Before publication, three native
files' original Git LF endings were restored to remove checkout-induced formatting
churn; code text was unchanged. Other native files retain their original CRLF.

**Publication:** source/acceptance checkpoint
`0dae6b5743f924e85489f52b95a6480806a09e10` pushed to
origin/codex/freecad-1.1.4-baseline; exact remote revision verified. No release,
owner package or shortcut delivery. This publication record is a separate docs commit.

## G1.7b3q Part Compound creation integration - October 11, 2026

**Authority:** applies the owner's explicit Reference prerequisite and confirmed
component-owned feature/History contract. No new operation workflow or design
decision was required. Existing compound dependencies are not component ownership.

**Implementation:** Part_Compound checks the complete unresolved selection before
native normalization and transaction creation. The component path creates its
Part::Compound in the edited definition, retaining original source ownership,
ordered/deduplicated Links and the native shape algorithm. Native source hiding and
appearance propagation remain in ViewProviderCompound. Ordinary legacy creation
bypasses Plus policy and retains its upstream behavior. See the
[contract](ARCHITECTURE.md#part-compound-integration-g17b3q).

**Build:** one PartGui + FreeCADPlusScripts build passed in retained
`test-builds/freecad_1.1.4_context`, exit 0, 265.42 seconds. No corrective source,
build or test-harness changes were needed after the build began.

**Validation:** four focused native cases passed first run, zero failures/errors/
skips, 11.020 seconds; native exit 0, 16.05 seconds overall. Covered atomic rejection
of Reference/Excluded, unsupported foreign Full Component input and missing Edit;
accepted occurrence-selected inputs with repeated face selections; ordered unique
Links; retained source and result ownership; History order; native input hiding;
Undo/Redo; save; unused-model single-input creation; and unchanged legacy behavior
with Plus preflight explicitly bypassed. The previous Boolean/Section cases were
not rerun. Native logs contain only the existing Std_Measure notices alongside
normal startup output.

Independent fresh-process reopen/source-edit passed, native exit 0, 6.31 seconds.
Exact document identities, ownership and ordered Links survived. The two-solid
compound retained volume 128; increasing one source box's height from 4 to 6
recomputed a valid two-solid compound with volume 160. Runtime checks stop here.

**Limits:** this covers command creation only. Existing-compound link edits and
drag/drop require their own intake integration. The same local-input/defining-file
support limit as G1.7b3o remains. No cross-component transfer/copy policy, automatic
reference promotion, new Compound workflow or complete consumer coverage is implied.
No manual visual acceptance, owner package or desktop shortcut delivery.

**Final checks:** all 43 Plus Python scripts parse and match the retained payload
byte-for-byte; 120 local links in changed Markdown resolve; whitespace passes.
Task artifacts `g1_7b3q_compound` were removed after recording these results. Useful
builds remain. No further runtime work.

**Publication:** source/acceptance checkpoint
`abcfa2a26008347147ece76ca2be30e50da7925b` pushed to
origin/codex/freecad-1.1.4-baseline; exact remote revision verified. No release,
owner package or shortcut delivery. This publication record is a separate docs commit.

## G1.7b3p direct Part Section integration - October 11, 2026

**Authority:** applies the owner's confirmed Reference prerequisite and the existing
component-owned feature/History contract. No new design choice or operation
workflow was needed. The direct command had its own result creation path, separate
from the previously guarded dialog and Boolean commands.

**Implementation:** Part_Section checks unresolved inputs before transaction
creation. Component files reuse BOPFeatures.make_section to preserve source
ownership and own the new native result in the edited definition. The base shape's
line material is retained. Ordinary legacy files execute the original command body,
including its parenting. The shared component-document probe was factored out of
the existing bridge without policy changes. See the
[contract](ARCHITECTURE.md#direct-part-section-integration-g17b3p).

**Build:** one PartGui + FreeCADPlusScripts build passed in retained
`test-builds/freecad_1.1.4_context`, exit 0, 251.59 seconds. No corrective native
build was needed. Before the first runtime run, the test's appearance assertion
was refined to compare actual material color values, with a distinctive base color;
that test script was copied to the retained payload. No production correction.

**Validation:** four focused native cases passed first run, zero failures/errors/
skips, 7.767 seconds; native exit 0, 12.58 seconds overall. Covered Reference/Excluded
and missing-Edit rejection with unchanged state, owned native Section dependencies,
History order, source visibility, line-color inheritance, Undo/Redo and save, the
existing dialog's Section Apply/Undo, and unchanged legacy parenting/policy bypass.
The previous Boolean cases were not rerun. Logs contain the existing Std_Measure
notice. The legacy grouped-input probe also emitted the native link-scope warning
for its unparented Section referencing features inside LegacyPart; this unchanged
legacy behavior is preserved, not claimed fixed by the component integration.

Independent fresh-process reopen/source-edit passed, native exit 0, 5.47 seconds.
Exact identities, source/result ownership and native Base/Tool links survived.
The section of a 4 x 4 box at z=2 retained length 16; changing the source length to
3 recomputed a valid section of length 14. Runtime checks stop here.

**Limits:** same supported local inputs/defining-document destination as G1.7b3o.
No cross-component transfer/copy policy, new geometry algorithm or complete consumer
coverage. Compound/split/join and direct exporter/view-output integration remain.
No manual visual acceptance, owner package or shortcut delivery.

**Final checks:** all 43 Plus Python scripts parse and match the retained payload
byte-for-byte; 118 local links in changed Markdown resolve; whitespace passes.
Task artifacts `g1_7b3p_section` were removed after recording these results. Useful
builds remain. No further runtime work.

**Publication:** source/acceptance checkpoint
`e6b3183c69808957c2e889bc3ebd0cdd4eef9e41` pushed to
origin/codex/freecad-1.1.4-baseline and exact remote revision verified. No release,
owner package or shortcut delivery. This publication record is a separate docs commit.

## G1.7b3o core Part Boolean eligibility and ownership - October 11, 2026

**Authority:** the latest explicit in-chat Reference prerequisite and the confirmed
component contract require eligible inputs and component-owned sketches/features/
geometry. No new owner operation workflow is inferred. Inspection found that native
BOPFeatures removes inputs from their parents; treating its Base/Tool dependencies
as ownership would leave component content outside the established ownership graph.
The local component path now preserves those inputs and owns the result explicitly.

**Implementation:** Cut/Common/Fuse preflight unresolved selections before shape
checks/transactions; the Boolean dialog checks actual list inputs before Apply.
The shared Reference/Excluded policy, explicit Edit requirement and current local
ownership support boundary are enforced by require_part_boolean_inputs. BOPFeatures
also preflights before object creation, preserves input containers, hides consumed
inputs and adds the native result to the edited definition. Legacy files retain
the upstream service behavior. See the
[contract](ARCHITECTURE.md#part-boolean-eligibility-and-ownership-g17b3o).

**Build:** one PartGui + PartScripts + FreeCADPlusScripts build passed in retained
`test-builds/freecad_1.1.4_context`, exit 0, 433.83 seconds. CMake regeneration also
rebuilt generated resources and GUI dependencies. No corrective build or source
correction was required after runtime began. No owner delivery.

**Validation:** all four focused native cases passed first run, zero failures/errors/
skips, 11.180 seconds; native exit 0, 16.16 seconds overall. Covered Reference and
Excluded mixed command input refusal, missing Edit, unchanged identities/ownership/
visibility/Undo on refusal, accepted Cut/Common/Fuse with expected volumes, preserved
input containers and History, native Undo/Redo, dialog foreign-input refusal followed
by successful local Apply, and legacy command/dialog bypass. The ordinary legacy
checks assert the Plus policy is never called.

Independent fresh-process reopen/source-edit recompute passed, native exit 0,
5.59 seconds. Exact object identities and ownership survived; all three saved native
results retained expected volumes, and increasing both input heights from 4 to 6
produced valid results at 1.5 times each original volume. Runtime validation stops
here. Logs contain the existing Std_Measure startup notice.

**Limits:** this supported path requires owned local inputs and a result in the
edited defining document. Cross-component bare catalog inputs and foreign source
routing through an importing assembly are refused, not given invented transfer/copy
semantics. The dialog supports native section creation through the same service,
but its Section mode was not independently exercised. Direct Part_Section and other
compound/split/join consumers remain separate work. No manual visual acceptance or
claim of complete Reference enforcement, Group 1 completion, or owner delivery.

**Final checks:** all 43 Plus Python scripts and BOPFeatures parse and match the
retained development payload byte-for-byte; 161 local links in changed Markdown
resolve; whitespace passes. Task artifacts `g1_7b3o_part_boolean` were removed after
recording these results. Useful development builds remain. No further runtime work.

**Publication:** source/acceptance checkpoint
`eae09d917762147a5ee65f744960055e36a55c03` pushed to
origin/codex/freecad-1.1.4-baseline and exact remote revision verified. No release,
owner package or shortcut delivery. This publication record is a separate docs commit.

## G1.7b3n PartDesign Boolean input admission - October 11, 2026

**Authority:** the owner's latest in-chat statement requires Add Reference Feature
in the active component's History before any use of Reference geometry. Rechecked
C10's latest related chat; no newer owner decision changes this rule or settles
Full Component tool transfer. This increment implements eligibility at existing
Boolean intake, without inventing that ownership policy or a new operation workflow.

**Implementation:** PartDesign_Boolean checks the entire unresolved selection and
active consumer before opening a transaction or calling native addObjects. Its
TaskBooleanParameters Add picker checks the original selection event before Body
resolution or mutation, retaining occurrence-specific Reference/Excluded state.
Refusal preserves IDs, tool ownership, list, visibility and transaction; Add remains
active. Removal bypasses admission as cleanup. Ordinary legacy documents bypass
the component policy. See the [contract](ARCHITECTURE.md#boolean-input-admission-g17b3n).

**Build:** one PartDesignGui + FreeCADPlusScripts build in retained
`test-builds/freecad_1.1.4_context` passed, exit 0, 814.19 seconds. CMake regeneration
rebuilt generated resources and GUI/workbench dependencies as well as the two
changed native files. It progressed within its 900-second deadline; no restart or
corrective build was needed. This is a development payload, not owner delivery.

**Validation:** six native cases passed on their first run, zero failures/errors/
skips, 14.145 seconds; native exit 0, 21.44 seconds including startup/shutdown.
Four new cases cover direct Reference and Excluded command rejection, mixed-batch
atomicity, forbidden shared occurrences, missing Edit context, empty-selection
Cancel, original-occurrence picker refusal, subsequent owned-tool acceptance,
removal cleanup and legacy command/picker bypass. Two affected ownership cases
confirm accepted Boolean geometry/History, Undo/Redo, save and Cancel restoration.

Independent fresh-process reopen/source-edit recompute passed, native exit 0,
5.83 seconds: exact identities, tool ownership, History, Body Tip and volume were
retained; changing the tool recomputed the valid Boolean to its expected new volume.
Logs contain the existing Std_Measure startup notice and the expected Reference
rejection message. No repeated runtime tests or visual capture were necessary.

**Limits:** PartDesign command-start and Add-picker intake only. No blanket claim
for all geometry consumers, direct Python property edits, existing dependency
rewrites, Part-workbench Boolean commands or the future Add Reference Feature
workflow. Native same-component ownership and existing legacy behavior remain.
Foreign Full Component tool transfer/copy remains a separate design question.

**Final checks:** all 42 Plus Python files parse and match the retained development
payload byte-for-byte; all 158 local links in changed Markdown resolve; whitespace
passes. The exact task validation directory `g1_7b3n_boolean_inputs` was removed
after recording durable results. Useful development builds remain. Stop here.

**Publication:** source/acceptance checkpoint
`751e77cbb2b246fe618b8ec8b09bb702e065a81b` pushed to
origin/codex/freecad-1.1.4-baseline and exact remote revision verified. No release,
owner package or shortcut delivery. This publication record is a separate docs commit.

## G1.6c6 Models file import - October 11, 2026

**Authority:** reread C09's original October 9 owner records: 14:03:43 UTC permits
importing files into an externally edited component's defining file; 19:00:28 UTC
separates importing a catalog into Models from placing components. Nested file
catalogs and immediate cycle rejection are confirmed. The menu wording/location
is a disclosed implementation choice. The new in-chat Reference prerequisite is
recorded separately in the evidence ledger, Component Panel and Task Panel specs;
it does not change this independent import action.

**Implementation:** Import Models from File is available on Models rows and its
background. The chooser names the target defining file. It uses the existing
saved-file/identity/cycle preflight and native import transaction. Closed sources
load hidden; the edited tab/context, domestic IDs and Part Tree placements remain.
External Edit imports into its own defining file. Cancel, duplicate import and
refusal create no transaction; native Undo/Redo belongs to the importing file.
Expected malformed archive/file errors are shown as panel feedback. Failed loads
close only documents newly opened by that attempt. See the
[contract](ARCHITECTURE.md#models-file-import-g16c6).

**Build:** FreeCADPlusScripts passed in retained
`test-builds/freecad_1.1.4_context`, exit 0, 59.11 seconds including configuration.
This is a Python-only increment; no native C++ rebuild or owner delivery.

**Validation:** five distinct native cases are complete, zero skips. Initial run:
one affected Rename menu regression passed; four new import cases timed out because
the test driver used selectFile before the visible chooser's directory model was
ready. Five cases, 63.887 seconds; native exit 0, 71.95 seconds overall. Corrected
the driver to enter the filename field and reran only the four unfinished cases:
three passed; one encountered an identity mismatch in a stale generated nested
fixture from the first run. Four cases, 18.968 seconds; native exit 0, 25.09 seconds
overall. Removed only that case's generated folder and reran it: passed, 4.709
seconds; native exit 0, 11.11 seconds overall. Neither correction required a
production change or another build; the corrected test script was copied to the
retained payload.

Covered actual Qt menus/chooser, closed nested catalogs without extra views,
unchanged IDs/placements/Edit, owning-file Undo/Redo, external unused Edit import,
Cancel, duplicate import, circular import refusal, stale editing context and invalid
archive feedback. Independent fresh-process reopen of both saved domestic and
externally owned catalog fixtures passed, native exit 0, 8.38 seconds. Exact domestic
and source identities and nested catalog ownership survived. Runtime checks stop
here. Native logs contain the existing Std_Measure startup notice.

**Limits:** accepts saved .cadprt catalogs, not arbitrary legacy-file conversion or
placement. No Add Component dialog, source relocation, new save UI or owner build.
Full Reference eligibility and Group 1 remain incomplete. Native chooser behavior
was exercised with Qt's non-platform dialog for deterministic automation; no manual
visual acceptance or platform shell-dialog coverage is claimed.

**Final checks:** all 41 Plus Python files parse and match the retained development
payload byte-for-byte. All 161 local links in changed Markdown resolve; whitespace
passes. Task artifacts `g1_6c6_import` were removed after recording the results;
the useful development build is retained. No further runtime work.

**Publication:** source/acceptance checkpoint
`6eda0296fcd867d61f77cbacafac99e8521afaca` pushed to
origin/codex/freecad-1.1.4-baseline and exact remote revision verified. No release,
owner package or shortcut delivery. This record is a separate documentation commit.

## G1.6c5 component definition Rename - October 11, 2026

**Authority:** reread the original C09 owner message of October 9, 18:52 UTC:
Part001 is an ordinary component that can be renamed, removed or deleted. The
confirmed Models contract requires names unique within a defining file, allows equal
names in separate files and assigns external edits to their source. The latest
related chat has no newer Boolean ownership decision. Rename is independent of that
pending question. Its menu placement is a disclosed implementation choice, not a
recovered exact owner menu layout.

**Implementation:** Models/Part Tree and the unused row expose Rename; the dialog
states that the name applies to all instances. hierarchy.rename_definition writes
only the defining object's Label in one defining-file transaction. Native names,
IDs, links, placements and geometry remain. Empty/duplicate/read-only names are
refused; unchanged names/Cancel do not create Undo. Dialog acceptance rechecks tab,
identity, catalog availability, current label and native task/transaction state.
Existing observers refresh shared rows and component window titles. See the
[contract](ARCHITECTURE.md#definition-rename-g16c5).

**Build:** FreeCADPlusScripts passed in the retained
`test-builds/freecad_1.1.4_context`, exit 0, 38.86 seconds including configuration.
Python-only increment; no native C++ rebuild or owner package/shortcut delivery.

**Validation:** initial native run: 5 cases, 4 passed and 1 failed status observation,
zero errors/skips, 9.900 seconds; native exit 0, 14.44 seconds including startup/
shutdown. Shared Part001 rename, stable rows, unchanged editing context/geometry/IDs,
one-step Undo/Redo, external defining-file edits, equal names in different files,
Cancel/unchanged/invalid/read-only checks and the existing window-title/no-polling
regression passed. The stale-dialog case preserved the concurrent name correctly;
its expected feedback was cleared by the existing queued observer refresh before the
assertion. The test now captures the rejection when emitted. Reran only that unfinished
case: 1 passed, zero failures/errors/skips, 2.472 seconds; native exit 0, 7.23 seconds
including startup/shutdown. This also completed the native editor guard check. No
production correction or second build was needed. All five distinct cases are complete.

Independent fresh-process reopen passed both domestic and external fixtures: names,
exact identities in the defining/assembly files, shared targets and domestic geometry
were retained. Native exit 0, 5.77 seconds including startup/shutdown. Runtime checks
stop here. Logs contain the existing Std_Measure startup notice.

**Limits:** this is shared definition Rename, not per-instance aliases, file rename,
delete/removal, storage transfer or a new naming convention. Native status feedback
is cleared by subsequent observer refresh as before. Stale-tab/catalog guards are
implemented; their full interaction matrix was not separately exercised. Group 1
remains incomplete and no owner build was delivered.

**Final checks:** all 40 Plus Python scripts parse and match the development
payload byte-for-byte; 123 local file links in changed Markdown resolve; whitespace
passes. Task artifacts `g1_6c5_rename` are removed after recording these results;
the useful development build is retained. No further runtime work.

**Publication:** source milestone `50d9d1c4ab5f6f6eda9c223eae42f8c3df184bf7`
pushed to `origin/codex/freecad-1.1.4-baseline`; exact remote revision verified.
No owner delivery. This increment is complete; stop here.

## G1.7b3m placed external export context - October 11, 2026

**Authority/finding:** checked the latest relevant chat, "Fix component activation
and part," plus the existing confirmed C09 source ownership and C10 Reference-use
rules. No newer cross-component Boolean decision was present. The native export
probe confirmed that an allowed placed external feature failed with "Select a
component occurrence or an owned feature to export": the resolved source file
had no original selection. Initial reproduction: one expected failing case,
3.302 seconds, native exit 0, 8.22 seconds including startup/shutdown.

**Implementation:** geometry.export_objects retains the originating assembly
selection when a selected external feature resolves into its defining file.
Native export dispatch obtains the resolved, deduplicated payload from that
selection and applies the existing require_export checks before options/writing.
Empty source selections never cause export of the source catalog. Ordinary legacy
dispatch and source-owned unused editing retain their existing behavior. See the
[contract](ARCHITECTURE.md#placed-external-export-context-g17b3m).

**Build:** one FreeCADGui/FreeCADPlusScripts build passed in the retained
`test-builds/freecad_1.1.4_context`, native exit 0, 205.56 seconds including
configuration and generated resources. The final added test case was copied into
the script payload before acceptance. No second native build, owner package or
shortcut delivery.

**Validation:** initial reproduction is recorded above. After the fix, three new
external export cases and two affected existing regressions all passed in one run:
5 passed, zero failures/errors/skips, 11.263 seconds; native exit 0, 16.17 seconds
including startup/shutdown. Actual Std_Export, its dialog, exporter options/writer
probe and BREP output exercised allowed external geometry, blocked Reference and
mixed Excluded occurrences, exact object identities, unchanged visibility and Undo,
source-only deduplication, no catalog fallback and bare foreign-member refusal.
Existing active-owned/derived, external-unused and ordinary legacy export passed.
Logs contain intentional eligibility rejection traces, the existing Std_Measure
startup notice and the existing OwnedReferenceResult/Pad scope warning fixture.

Independent fresh-process reopen of the assembly/source pair passed exact IDs in
both files, allowed BREP export with valid expected geometry, and Reference rejection
before writer/options. Native exit 0, 6.17 seconds including startup/shutdown.
Runtime checks are complete; no further tests are required for this increment.

**Limits:** whole-object native selection payload and a BREP-backed exporter probe;
this does not certify every format, occurrence-placement semantics, direct Python
writers, view-image/PDF output or arbitrary mixed-file export workflows. No modeling
operations or ownership policies changed. Group 1 remains incomplete.

**Final checks:** all 39 Plus Python scripts parse and match the development
payload byte-for-byte; 121 local file links in changed Markdown resolve; whitespace
passes. Task artifacts `g1_7b3m_external_export` are removed after recording these
results; the useful native development build is retained. No further runtime work.

**Publication:** source milestone `b9d36924725bc8fcf10907d856e16255605f311c`
pushed to `origin/codex/freecad-1.1.4-baseline`; exact remote revision verified.
No owner delivery. This increment is complete; stop here.

## G1.7b3l legacy Boolean conversion - October 11, 2026

**Authority/finding:** the confirmed C06 editable legacy conversion requirement and
current owner compatibility direction apply. Standalone conversion counted nested
Boolean-owned tool Bodies as independent roots, while Part conversion inspected
only direct Body features. Both rejected otherwise supported native editable graphs.
This work preserves existing authored content and makes no new cross-component
Boolean intake decision. The earlier pending owner question remains unanswered.

**Implementation:** both paths reuse legacy_hierarchy.body_objects and the canonical
document.owned_children structural contract. One outer Body can contain Boolean-owned
tool Bodies; Part/shared-link conversion retains them within the original definition.
Nested scripted features, unsupported/unowned content and independent outer Bodies
remain refused. No geometry algorithm, command/picker, native schema or UI workflow
was changed. See the [contract](ARCHITECTURE.md#legacy-boolean-tool-ownership-g17b3l).

**Build:** FreeCADPlusScripts passed in the retained
`test-builds/freecad_1.1.4_context`, exit 0, 38.86 seconds including configuration.
Python payload only; no native C++ compilation, owner package or shortcut delivery.

**Validation:** four new conversion cases and two affected native Body/Part shared-
link regressions passed first run: 6 passed, zero failures/errors/skips, 5.620 seconds;
native exit 0, 10.88 seconds including startup/shutdown. Checked exact original
names/types/IDs/labels, expressions, authored placements, Boolean Group, Body Tips,
History without Body rows, shared definition identity, editing and one-step Undo/Redo.
Live unsaved source edits were neither converted nor overwritten; source hashes
remained unchanged. Nested scripted features are refused even with explicit fallback;
general linked dependencies do not legitimize unowned geometry and independent root
Bodies remain refused without output. Logs contain expected UUID reassignment on
isolated restore, native scope warnings for deliberately unowned negative fixtures,
and the existing Std_Measure startup notice. No correction or repeated test run.

Separate fresh-process reopen of both converted Boolean fixtures passed exact IDs,
History, ownership, expressions, placements and geometry; changing the source tool's
expression input recomputed valid results with the expected volume increase.
Native exit 0, 5.67 seconds including startup/shutdown. Runtime checks are complete.

**Limits:** representative native Fuse with one nested tool Body, standalone and
inside a shared Part definition. Other Boolean modes, deeper nesting, external
legacy graphs and new cross-component Boolean tool intake are not certified here.
No owner files were converted. Group 1 remains incomplete.

**Final checks:** all 38 Plus Python scripts parse and match the development
payload byte-for-byte; 119 local file links in changed Markdown resolve; whitespace
passes. Runtime validation is closed. Task artifacts `g1_7b3l_legacy_boolean` are
removed after recording these results; the useful development build is retained.

**Publication:** source milestone `82028b9c0a859412cc9286d460cef01f034e959c`
pushed to `origin/codex/freecad-1.1.4-baseline`; exact remote revision verified.
No owner delivery. This increment is complete; stop here.

## G1.7b3k native Boolean ownership prerequisite - October 11, 2026

**Finding/authority:** inspection of native GeoFeatureGroup addObjects showed that
Boolean tools move into the Boolean's ownership group. The component validator
recognized only Part/Body/Origin ownership, so an accepted same-component operation
could leave its tools classified as orphans and prevent save. Reviewed preserved
owner messages C06 (editable sequential feature preservation), C09 (definitions and
ownership), C10/U069 (mandatory promoted Reference features), and the current
backend-Body direction. Checked the latest relevant chat, “Fix component activation
and part,” and preserved owner sources. No explicit Boolean cross-component transfer
policy was found. The disconnected old-computer source remains unavailable.

**Outstanding owner question:** native Boolean tools from a different Full Component
would leave their source definition and change all its instances. Should FC Plus
require an owned linked reference first (recommended), create one automatically, or
allow that transfer? Asked via the conversation's pending clarification. No answer
has been assumed. The same-component ownership prerequisite is independent of it.

**Implementation:** document.owned_children/owned_path own the native traversal
contract, including Boolean-owned tools. Validation and geometry eligibility share
it; general feature dependencies and component links are not ownership. History
places owned tool features before the consuming Boolean and hides Body containers.
Panel selection and native feature Edit use the complete ownership path. No native
operation algorithm, cross-component intake policy or document schema was changed.
See the [contract](ARCHITECTURE.md#native-boolean-ownership-within-a-component-g17b3k).

**Build:** FreeCADPlusScripts payload build passed in the retained
`test-builds/freecad_1.1.4_context`, exit 0, 44.55 seconds including configuration.
No native C++ changes/recompilation, owner package or desktop shortcut delivery.

**Validation:** four new native GUI cases and two affected existing regressions
passed in one run: 6 passed, zero failures/errors/skips, 9.983 seconds, native exit
0 (14.98 seconds including startup/shutdown). Verified valid same-component Fuse,
Boolean tool ownership, hidden Body History ordering, nested feature selection and
native Edit/Cancel, creation Cancel, one-step Undo/Redo, unchanged existing object
IDs, no general-dependency ownership traversal, and orphan rejection. Existing panel
projection and edited-component eligibility regression cases passed. The existing
OwnedDerived/Pad regression fixture emitted a native link-scope warning; startup
also reported the existing Std_Measure notice. No test correction or repeated suite.

Independent fresh-process reopen passed exact IDs, stored Boolean tools, History,
Body Tip and saved volume; changing the source tool length produced a valid result
with the expected volume increase. Native exit 0, 5.83 seconds including startup/
shutdown. Runtime checks are complete; no more are required for this increment.

**Limits:** same-component native Fuse and one level of Boolean tool nesting were
exercised. Other Boolean modes, deeper nesting, foreign/external tools and removal
of consumed tools are not certified here. Boolean command/picker input admission
remains pending, along with the cross-component decision. This prerequisite does
not make all Boolean workflows or Group 1 complete.

**Final checks:** all 37 Plus Python scripts parse and match the development
payload byte-for-byte; 150 local links in changed Markdown resolve; whitespace
passes. Task artifacts `g1_7b3k_boolean_ownership` are removed after recording these
results; the useful development build is retained. No further runtime work.

**Publication:** source milestone `2c48da7f9d8ae7272e419f8a01a340def0b0e9cf`
pushed to `origin/codex/freecad-1.1.4-baseline`; exact remote revision verified.
No owner delivery. This prerequisite increment is complete; stop here.

## G1.7b3j dress-up/transformation command admission - October 11, 2026

**Implementation:** shared dress-up and transformation command starts validate the
active component consumer and full unresolved selection before clearing, expansion,
Feature filtering or document mutation. The separate Multi-Transform conversion
branch uses the same check before changing Originals or Tip. Empty selection still
requires explicit Edit. Pattern Add/Remove Original picks no longer fall through to
direction/axis parsing; duplicates and rejected additions retain their picker.
Chamfer now clears selection only after shared preparation succeeds. See the
[contract](ARCHITECTURE.md#dress-up-and-transformation-command-admission-g17b3j).
Existing C09/C10 requirements suffice; no new design decision was required.

**Build:** initial batched PartDesignGui/FreeCADPlusScripts build passed, exit 0,
935.83 seconds. The runtime-discovered Chamfer cleanup issue required a second
native build, which passed with exit 0 in 685.25 seconds. CMake-file line-ending
normalization performed after the first build
started caused configuration/generated GUI dependencies to rebuild again; future
increments must finish that normalization before launching the build. The retained
`test-builds/freecad_1.1.4_context` remains the development tree. No owner package or
shortcut delivery.

**Validation:** the first launch macro had a quoting error before any test
ran; the exact isolated process was closed after identifying it (70.38 seconds).
Corrected launcher: 7 cases, 5 passed and 2 failed expectations, zero errors/skips,
17.907 seconds, native exit 0. Both expected Reference wording, while these
occurrences correctly become effectively Excluded outside their owner's Edit
context. Correcting that expectation and rerunning only those two cases gave
1 pass and 1 failure, 4.663 seconds, native exit 0. The remaining failure exposed
Chamfer's unconditional selection clear after rejected preparation. Corrective
checks cover that actual defect, the unfinished command batch, accepted Chamfer
creation/Undo and the extended legacy case. Earlier unrelated passing suites remain
closed. The corrective three-case run gave 2 passes (accepted Chamfer with Undo/
Redo and extended legacy bypass) and 1 test-driver error, 7.937 seconds, native exit
0: `PartDesign_Scaled` exists in source but is deliberately not registered upstream.
No command availability was changed. Removing that unavailable command from the
rejection matrix and rerunning only the unfinished case gave 1 pass, zero failures/
errors/skips, 5.196 seconds, native exit 0. All eight distinct focused cases are now
complete; no additional native fix or build was needed after the Chamfer correction.

Coverage includes all eight registered commands using these shared helpers with
configured Reference/effectively Excluded and Excluded occurrences, an unresolved
mixed batch, empty-selection Edit rejection and Cancel, unchanged identities/Tip/
geometry/selection/Undo/transaction on rejection, and rejected Multi-Transform
conversion without Originals mutation. Fillet/Chamfer/Linear Pattern accepted
creation and one-step Undo/Redo pass; ordinary legacy creation bypasses Plus policy.
Pattern rejected/duplicate Originals do not invoke direction parsing; accepted
Original additions and removal cleanup remain available.

Independent fresh-process reopen passed all three saved component fixtures: exact
object identities, Base/Originals, Body Tip and volumes were retained. Changing the
source box length recomputed valid results with increased volume. Native exit 0,
6.58 seconds including application startup/shutdown. Final logs contain the existing
Std_Measure startup notice, without a new application error. Runtime checks stop here.

**Limits:** representative successful geometry uses Fillet, Chamfer and Linear
Pattern; command admission covers the shared helpers and Multi-Transform conversion
rejection. This is not certification of every operation's geometry, nested
transformation or external context. Native active-Body resolution still precedes
these checks. Other collectors/command families, direct exporters/view output,
raw property/Python writes and retrospective dependency reclassification remain
outside this increment. Scale command runtime coverage is unavailable because
upstream does not register it. Group 1 is incomplete.

**Final checks:** all 36 Plus Python scripts parse and match the retained development
payload byte-for-byte; 147 local links in changed Markdown resolve; whitespace passes.
Task-generated `g1_7b3j_commands` validation artifacts are removed after recording
these results; the useful native build is retained. No more runtime work is needed.

**Publication:** source milestone `b35f8423e1eece2f1f687bbff84beab2317c1b8b`
pushed to `origin/codex/freecad-1.1.4-baseline`; exact remote revision verified.
No owner delivery. This increment is complete; stop here.

## G1.7b3i shared dress-up/transformed inputs - October 11, 2026

**Implementation:** shared native dress-up edge/face additions, Add All Edges and
Fillet/Chamfer Use All Edges require eligible component inputs before mutation;
rejected checkbox enabling restores the prior UI state. Shared transformed-feature
Original additions check original occurrences before list/property/transaction
changes. Existing-entry removal remains available. See the
[contract](ARCHITECTURE.md#shared-dress-up-and-transformed-feature-intake-g17b3i).
The owner's latest clarification keeps this as component-rule integration, not
operation workflow implementation. No new design choice required clarification.

**Build:** one batched PartDesignGui/FreeCADPlusScripts build passed in the retained
`test-builds/freecad_1.1.4_context` tree, native exit 0. All changed native files
compiled and linked. Later corrections affected only the test driver/verifier and
were copied to the development payload; no additional native build was needed.
No owner package or desktop shortcut delivery.

**Validation:** initial four-case run: 2 passed (dress-up pick/cleanup/Undo and
Fillet/Chamfer whole-edge routes/context loss/Cancel), 2 errors, zero failures/skips,
11.812 seconds, native exit 0. The two transformation cases stopped at the driver's
QToolButton lookup; those native controls are QPushButtons. The driver now uses
QAbstractButton for the shared lookup. The first affected-case rerun reached the
expected Ineligible geometry modal notification and hit the runner's 180-second
deadline; the isolated process was terminated by that deadline. This was a test
acknowledgment omission, not a stuck modeling operation. The driver now uses the
existing `messages()` helper and checks that captured dialogs contain the expected
rejection reason. It also supports the whole-edge test's expected context errors.
Only the two unfinished cases were rerun: 2 passed, zero failures/errors/skips,
5.886 seconds, native exit 0. Earlier passing cases and unrelated suites were not
repeated. No production correction was needed after the initial build.

Actual native checks prove original-occurrence rejection before stored references,
list entries, preview volume, Undo/transaction or object identities change; accepted
Fillet edges and Linear Pattern Originals; removal of existing entries via an
ineligible occurrence; one-step Undo/Redo; both Fillet/Chamfer whole-edge rejection
when Edit context is lost, including checkbox/enablement consistency; accepted
whole-edge actions and Cancel restoration; and ordinary legacy bypass.

The first independent reopen stopped in the verifier's source edit because it added
a dimensionless number to a FreeCAD Quantity. The driver now sets the numeric value
in the property's existing units. The corrected fresh process passed exact IDs,
stored Fillet Base/Pattern Originals and saved volumes, then changed each source
box's length and obtained valid recomputed results with increased volume. Exit 0.

**Limits:** the shared collector is exercised through Fillet and Linear Pattern,
with both Fillet/Chamfer whole-edge controls. Other dress-up geometry variants and
nested MultiTransform are not separately certified. Command-start preselection,
other collectors, raw property/Python writes and retrospective reclassification of
existing dependencies remain outside this increment. No operation redesign, schema
change, workbench removal or rendering/performance claim; Group 1 remains incomplete.
The unchanged Pattern selection handler falls through to its direction parser after
an Original is rejected and emits a secondary invalid-selection notice. The tests
confirm unchanged stored state; feedback routing remains a follow-up alongside
command-start admission. Completed logs otherwise contain expected eligibility
notifications and the pre-existing Std_Measure startup notice.

**Final checks:** all 35 Plus Python scripts parse and match the development payload
byte-for-byte; 145 local links in changed Markdown resolve; whitespace checks pass.
Task artifacts `g1_7b3i_collectors` were deleted after recording these results. The
useful development build is retained. No further runtime work is required.

**Publication:** source milestone `4a047f0cb36e7f0716b4f3fea1b61a06e6cd2176`
pushed to `origin/codex/freecad-1.1.4-baseline`; exact remote revision verified.
No owner delivery. This increment is complete; stop here.

## G1.7b3h Loft/Pipe reference admission - October 11, 2026

**Implementation:** original-occurrence component eligibility before native Loft
profile/section and Pipe profile/main-path/auxiliary-path/section mutation. Section
removal remains cleanup; picked Pipe edge removal needs eligibility because it also
assigns the selected source. Native picker behavior and legacy bypass are retained.
See the [contract](ARCHITECTURE.md#loftpipe-profile-section-and-path-intake-g17b3h).
Existing C10/U069 requirements suffice; no new design decision was required.

**Build:** one batched PartDesignGui/FreeCADPlusScripts build passed in the retained
`test-builds/freecad_1.1.4_context` tree, native exit 0. Both changed collector files
compiled and linked. Later test-driver corrections were copied to the development
payload; no further native build was needed. No owner package/shortcut delivery.

**Validation:** initial four-case native run stopped at a shared test-driver form
lookup mismatch (Qt generates `PartDesignGui__Task...` names): 4 failures, zero
errors/skips, 6.188 seconds, native exit 0. Corrected run: 2 passed (Loft and legacy
Loft/Pipe), 2 Pipe assertion failures, zero errors/skips, 10.338 seconds, exit 0.
The two assertions expected unmapped edge names; actual calls correctly retained
the original occurrence with FreeCAD's mapped sketch-edge suffix. The driver now
checks occurrence/object path and edge suffix. Only those two Pipe cases were rerun:
2 passed, zero failures/errors/skips, 7.028 seconds, exit 0. No production correction
was needed after the first build; passing cases and previous suites were not repeated.

Actual native collectors prove rejection before profile/path/section/list, preview
volume, Undo/transaction or object-identity mutation; correct original-occurrence
admission; accepted Loft/Pipe profiles/sections and main/auxiliary paths/edges;
existing-section removal; Pipe Cancel restoration; Loft one-step Undo/Redo; and
ordinary legacy bypass. An independent fresh process reopened both saved `.cadprt`
fixtures and passed exact object IDs, stored references and volumes, then changed
each source profile and obtained valid recomputed results with increased volume.
Native exit 0. Expected ineligible-geometry notifications and the pre-existing
`Std_Measure` startup notice were the only messages in the completed native logs.

**Limits:** this tests additive native Loft/Pipe; the shared collector code also
serves their subtractive variants, but separate subtractive geometry acceptance is
not claimed. This increment is picked-input admission, not retrospective policing
of existing dependencies, property/Python writes or every other collector. No new
operation workflow, schema, workbench removal, rendering/performance claim or owner
build delivery. The original C10/U069 owner message was re-read; its rule suffices.
Group 1 remains incomplete.

**Final checks:** all 34 Plus Python scripts parse and match the retained development
payload byte-for-byte; 143 local links in changed Markdown resolve; whitespace checks
pass. Task validation artifacts `g1_7b3h_sweeps` were deleted after recording these
results; the development build is retained. No further runtime work is required.

**Publication:** source milestone `0fdfdbf08a48d3418e8a03fdb056a0a2320ebe67`
pushed to `origin/codex/freecad-1.1.4-baseline`; exact remote revision verified.
No owner delivery. This increment is complete; stop here.

## G1.7b3g separate attachment and Extrude inputs - October 11, 2026

**Implementation:** component checks before Python attachment initial mutations,
original picked-path shortening, parsed-reference preview and Apply/OK; native
Extrude guards both sides' face/shape picks and typed face ownership before the
mutating native parser. Rejection preserves previous references/preview. Component
attachment Cancel now closes Apply's lazy application transaction before display
restoration, preventing a cleanup-only Undo entry. Legacy files retain their previous
confirmation/transaction path. See the
[contract](ARCHITECTURE.md#python-attachment-and-extrude-faceshape-intake-g17b3g).
Existing C10/U069 rules govern; no further design choice was needed.

**Build:** batched PartDesignGui/PartScripts native build passed in the retained
`test-builds/freecad_1.1.4_context` tree. FreeCADPlusScripts/PartScripts synchronization
passed. The later cancellation correction was Python-only and copied to the Part
payload; no additional native build was needed. No owner package/shortcut delivery.

**Validation:** initial five-case run: 4 passed, 1 failure, zero errors/skips, native
exit 0 (15.505 seconds). Native Extrude face/typed input, both sides' shape/face lists,
legacy Python attachment/Extrude bypass and initial mixed-batch rejection all passed.
The attachment Apply/Cancel case failed one-step Undo. One affected-case diagnostic
showed Apply left a lazy transaction with no document changes; document-only abort
could not close it before display restoration. The component-specific application
transaction close fixed it; that case passed (2.810 seconds). The four passing cases
were not repeated.

The first independent reopen then found the driver had left the Python editor in
Deactivated mode. It now explicitly selects Flat Face and asserts actual preview
placement before testing rejection and confirmation. Final affected-case run passed
(1 case, 2.870 seconds, zero failures/errors/skips, native exit 0). Independent fresh
reopen of both fixtures passed exact IDs/references, attachment following changed
source height and valid up-to-face Pad volume after moving its limit, native exit 0.

Checks drive actual selection observers, Qt text/control signals and native editors.
They prove no initial transaction/object mutation on mixed rejection; original
occurrence distinctions; typed rejection before property/metadata or preview change;
blocked Python Apply/OK retaining the task; accepted Apply, Cancel and one-step
Undo/Redo; and native legacy bypass. Both Extrude shape sides are checked for input
admission and cancellation, not successful two-sided machining geometry. No previous
modeling/export/native attachment suites were repeated.

**Limits:** the native Pad still reports an out-of-Body link-scope warning for the
fixture's owned limit box outside its backend Body (also seen in the ordinary legacy
fixture). Measured geometry/reopen/source updates pass; this increment does not
resolve that native scope warning or certify all cross-Body dependency handling.
Loft/Pipe and other collectors, stored combo references, property-editor/raw Python
writes, existing-dependency reclassification and direct exporter/view-output paths
remain unfinished. No rendering/performance change is claimed; Group 1 is incomplete.

**Final checks:** 33 Plus Python scripts and the changed Part attachment script
parse and match the retained development payload byte-for-byte; 141 local links
in changed Markdown resolve; whitespace checks pass. Task validation artifacts
`g1_7b3g_inputs` were deleted after recording these results; the development build
is retained. No further runtime work is required for this increment.

**Publication:** source milestone `7bf802ac7a07ff8c6d8a220beed7925ada0a1353`
pushed to `origin/codex/freecad-1.1.4-baseline`; exact remote revision verified.
No owner delivery. This increment is complete; stop here.

## G1.7b3f attachment and shared task references - October 11, 2026

**Implementation:** native TaskAttacher prechecks the entire initial reference batch,
individual picks and typed references before AttachmentSupport/RefName mutation.
Shared getReferencedSelection checks the original occurrence before the native
external reference/copy dialog. Rejected input preserves the current reference and
transaction. Legacy documents retain the native path. See the
[contract](ARCHITECTURE.md#attachment-and-shared-task-reference-intake-g17b3f).
Existing C10/U069 promotion rules govern; no new design decision was needed.

**Build:** one bounded batched PartGui/PartDesignGui build passed in the retained
`test-builds/freecad_1.1.4_context` tree; FreeCADPlusScripts synchronization passed.
Both changed native files compiled and linked. Subsequent corrections affected only
test drivers and were copied to that payload. No owner package or shortcut delivery.

**Validation:** initial four-case run: 3 failures, 1 error, zero skips, native exit 0
(5.876 seconds). The driver used a non-attachable App::Plane instead of Part::DatumPlane,
expected native datum acceptance to clear edit mode, omitted the direction combo's
activated signal, and compared a legacy origin reference without resolving its native
container path. These were test assumptions; no production correction was needed.
The corrected four-case run passed, zero failures/errors/skips, native exit 0
(7.265 seconds). No prior modeling/export suites were rerun.

Actual native checks prove: a mixed initial batch reaches the policy with both
unresolved references and mutates neither; rejected picked and typed occurrences
leave support, RefName, placement and editor transaction unchanged; accepted native
attachment supports Cancel and Undo/Redo; the Pad direction picker rejects the
forbidden shared occurrence before mutation and accepts the eligible occurrence;
and ordinary legacy attachment bypasses the component guard. The datum editor's
native lingering edit mode is explicitly reset after successful acceptance in the
driver, not changed by this increment.

Independent fresh-process reopen passed exact saved object IDs, attachment support
and axis identities. Changing source Pad Length moved the attached plane to the new
height; changing the axis-driven Pad Length retained valid geometry and expected
volume. Native exit 0. No viewport rendering or performance change is claimed.

**Limits:** runtime coverage drives native attachment and Pad direction, not every
shared collector caller. Revolution/Groove, Helix, Draft, Mirrored and Pattern use
the inspected shared resolver. The separate Python AttachmentEditor, other task
collectors, stored combo references, property-editor/raw Python writes and existing
dependency reclassification remain outside this increment. Full Group 1 is unfinished.

**Final checks:** all 32 Python files parse and byte-match the development payload;
139 local documentation link targets resolve and whitespace checks pass. Temporary
profiles, fixtures, logs and launchers in `validation/g1_7b3f_references` were deleted
after recording results. The useful native development build is retained.

**Publication:** source milestone `5212b219b3af00a0188417e21457ba286f353e5a`
was pushed to origin `codex/freecad-1.1.4-baseline`; the exact remote revision was
verified. No owner package, desktop-shortcut update, release or deployment.

## G1.7b3e native modeling intake - October 11, 2026

**Implementation:** shared ComponentGeometry.h bridge applies the existing occurrence
policy to native PartDesign profile preparation and Sketcher Projection/Intersection
intake. PartDesign checks unresolved selection and the later actual profile-picker
candidate before feature creation. Sketcher checks the original occurrence before
addExternal; rejection preserves the current editor transaction. Explicit component
Edit and consumer ownership are required. Legacy documents bypass the Python guard.
No global selection filter, schema change or new operation dialog. See the
[native intake contract](ARCHITECTURE.md#native-modeling-intake-eligibility-g17b3e).

**Owner source:** original C10/U068-U069 messages in **Fix component activation and
part** were rechecked. U069's required promotion of Reference geometry governs;
no further design decision was needed for these existing input consumers.

**Build:** one batched SketcherGui/PartDesignGui/FreeCADPlusScripts build passed in
`test-builds/freecad_1.1.4_context`. Subsequent corrections affected only the test
fixture/driver and were copied to that payload. No owner package or shortcut delivery.

**Validation:** initial 9-case native modeling/shared-policy run: 6 passed, 3 errors,
zero failures/skips, native exit 0 (11.839 seconds). All five existing eligibility
cases and the external-unused service-context case passed. The three errors were a
test helper colliding with the inherited fixture's sketch attribute, before commands
ran. Renaming the helper resolved them; the affected 3-case run passed with zero
failures/errors/skips, native exit 0 (7.292 seconds). Passing policy cases were not rerun.

These checks drive actual PartDesign_Pad task acceptance and Sketcher_Projection
selection. They cover shared Reference/Excluded refusal before mutation, allowed
occurrences, Pad shape/Tip and Undo/Redo, no-selection profile-picker recheck, native
legacy Pad bypass, original Sketcher selection and preserved editor transaction.
External unused/wrong-consumer checks exercise the shared service, not a complete
native external Pad workflow. Other profile commands and Intersection share the
reviewed native path but were not separately driven.

Independent Pad reopen passed exact IDs, native visibility, Profile/Tip and volume.
Projection reopen initially exposed a tuple/list comparison error in the test;
normalizing the reference representation then exposed the fixture's cylindrical
seam losing its reference after a Length change. A bounded ordinary legacy-document
reproduction in this same build showed the same loss without invoking the Plus guard.
The seam projects to a point in this plane; it did not prove real projected geometry.
The fixture now chooses a circular rim and asserts two actual sketch edges. The
corrected native projection case passed (1 case, 2.862 seconds, zero failures/errors/
skips, native exit 0). Its independent fresh-process reopen/source-Length update
passed exact IDs/reference, two projected/local edges and updated Pad volume, native
exit 0. The passing Pad checks were not repeated. The inherited seam-reference loss
remains unfixed; do not treat this increment as its resolution or general topology
stability certification. No viewport/rendering change or performance claim.

**Limits:** task-dialog reference fields, attachment, other non-profile commands,
raw Python writes and existing-dependency reclassification are outside this increment.
Full G1.7b3 and Group 1 remain unfinished. Add Reference Feature is separate operation
work. No owner build is being delivered.

**Final checks:** all 31 Python files parse and byte-match the native payload; 137
local documentation link targets resolve and diff whitespace checks pass. Task
profiles, fixtures, logs and launchers in `validation/g1_7b3e_modeling` were deleted
after recording results. The useful native development build is retained.

**Publication:** source milestone `8aeb91a3057b1dbbe59816772a9b4b2f15df698e`
was pushed to origin `codex/freecad-1.1.4-baseline`; the exact remote revision was
verified. No owner package, shortcut update, release or deployment.

## G1.7b3d native export eligibility - October 11, 2026

**Implementation:** native File > Export now checks component occurrence eligibility
before exporter import/options/writing. It verifies both unresolved selections and
the resolved object payload, rejects forbidden aggregates/mixed selections and
refuses the all-document catalog fallback. Whole-file export cannot inherit a
branch's temporary Edit override. Legacy files keep the original export dispatch.
The native command also recognizes the existing ExternalEditContext source selection
when editing an unused external component from the assembly tab. Document Save keeps
Reference source content. See the [export contract](ARCHITECTURE.md#native-export-eligibility-g17b3d).

**Owner source:** rechecked the original U068/U069 user messages in **Fix component
activation and part**, October 10 10:52/10:56 EDT. The later explicit prohibition on
using unpromoted Reference geometry governs. No new operation workflow was inferred.

**Build:** FreeCADGui and FreeCADPlusScripts passed in the retained native development
tree, including a corrective build for external unused selection routing. The initial
launcher quoting issue occurred before compilation and was corrected. Native patches
are limited to export dispatch/routing; no owner package or shortcut delivery.

**Validation:** initial 9-case export/shared-eligibility run: 6 passed, 1 failure,
2 errors, zero skips, native exit 0 (15.122 seconds). All five existing eligibility
cases and aggregate rejection passed. Two errors were the test file dialog retaining
FreeCAD's suggested filename; explicitly setting fileNameEdit fixed the driver.
The remaining failure exposed native Export ignoring the source selection while
an assembly tab edited an unused external component; the context routing fix above
resolved it. Final affected run: all 4 export cases passed, zero failures/errors/skips,
native exit 0 (8.570 seconds). The passing five shared-policy cases were not repeated.

Checks drive Std_Export's actual dialogs and prove rejection before exporter options
or writer calls, successful native BREP output/volume, shared occurrence distinctions,
owned source-linked results, source-owned unused geometry, exact identity/visibility,
no new Undo entries, payload mismatch refusal and legacy export bypass. Independent
fresh-process reopen passed blocked/allowed native exports, actual BREP geometry and
exact saved identities/native visibility, native exit 0. All 30 Python files parse
and byte-match the development payload. No viewport rendering change or new display
performance claim.

**Limits:** aggregates containing forbidden geometry are refused, not filtered into
replacement geometry. Direct exporter-module/Python calls, view-image/PDF paths and
native modeling consumers are not universally guarded. Full G1.7b3 and Group 1
acceptance remain unfinished. Add Reference Feature is separate operation work.

**Final checks:** all 30 Python files parse and match the native payload; 108
local documentation link targets resolve and diff whitespace checks pass. Task
profiles, CAD/BREP fixtures, logs and launcher files under
`validation/g1_7b3d_export` were deleted after recording the results. The useful
native development build is retained.

**Publication:** source milestone `8baa8ca44e45070882ef5fcc2711b1d4fc5fc322` was pushed to origin
`codex/freecad-1.1.4-baseline`; the exact remote revision was verified. No owner
package, shortcut update, release or deployment.

## G1.7b3c shared geometry eligibility - October 11, 2026

**Owner source:** reread the original user messages in **Fix component activation
and part** (`01a12645-26b9-7d32-b338-529e73a9c0d4`), retained as U067-U069/C10.
U069, October 10 10:56 EDT, requires Add Reference Feature before reference-child
geometry can be used in any way. This overrides the earlier any-visible-geometry
reference allowance; owned derived features remain usable without traversing their
outgoing source dependencies.

**Implementation:** new read-only `geometry.require_access` resolves the originating
view's Edit context and native occurrence chain. It rejects Reference/Excluded
branches, bare foreign members and aggregates containing forbidden descendants,
while preserving shared-instance distinctions, source-owned unused definitions and
the active editing override. Hidden is separate from eligibility. Existing Move
Components direction, axis, axis-point and pivot consumers call the guard before
reading a shape. Panel tooltips state the restriction; selection and Edit still work.
No global selection gate, native shape override, schema or geometry mutation, new
operation workflow, or Add Reference Feature dialog is introduced. See the
[contract](ARCHITECTURE.md#geometry-eligibility-g17b3c).

**Build:** FreeCADPlusScripts completed in the retained native development tree;
existing native libraries were reused. No C++ change or owner-build/shortcut delivery.

**Validation:** initial 9-case eligibility/Move/Rotate/display run passed 8, with
one error, zero failures/skips, native exit 0 (12.824 seconds). All five new cases
passed. The remaining direction regression exposed mapped topology names containing
dots; a focused correction then exposed native origin axes lacking a direct shape.
The final resolver uses FreeCAD's native object-chain parser and object-identity
lookup. Final affected run: all five eligibility cases and that Move regression
passed (6 cases, zero failures/errors/skips, 8.630 seconds, native exit 0).
Independent fresh-process reopen passed saved Reference rejection, allowed shared
occurrence access and exact object IDs/native visibility, native exit 0.

Checks include domestic/external unused ownership, active Edit overrides, aggregates,
foreign-member bypass prevention, owned source-linked features, Undo/Redo, read-only
queries and actual panel navigation/tooltips. Consumer tests fail deliberately if
forbidden geometry reaches Part.getShape; direction/axis/point/pivot rejection occurs
before that boundary. The successful Rotate/display regressions were not repeated.
No viewport rendering changed; this increment makes no new visual-performance claim.

**Limits:** the shared policy is not yet wired into all native modeling or export
consumers and does not intercept arbitrary direct Python shape reads. Full Reference
eligibility, Add Reference Feature and Group 1 acceptance remain unfinished.

**Final checks/cleanup:** all 29 Python files parse and byte-match the development
payload; 136 local documentation link targets exist and whitespace checks pass.
Task profiles, fixtures, logs and diagnostic output under
`validation/g1_7b3c_eligibility` were deleted after recording the results. The useful
development build is retained.

**Publication:** source milestone `10ae70841366fda1d12e710c6ff98fef515840ba` was pushed to origin
`codex/freecad-1.1.4-baseline`; the exact remote revision was verified. No owner
package, shortcut update, release or deployment.

## G1.7b3b Bodies Only filtering - October 11, 2026

**Implementation:** saved Bodies Only choices now filter native display paths in
placed and domestic/external unused views. Native Body Tips and standalone
face-bearing results remain; visible origins, non-Tip Body history, standalone
curves and points are filtered without persistent Visibility, geometry, placement,
identity or schema changes. Ordinary nested components remain subject to their own
saved types; explicit Full Component and contextual Reference/Excluded behavior
are preserved. See the [contract](ARCHITECTURE.md#bodies-only-content-filtering-g17b3b).

**Resolved defect:** newly added native link children could have stale Coin
snapshots when the filter ran. `display.apply_hidden` handles only the native
"temporarily unavailable" path condition by draining the queued Coin sensors once
and retrying once. A Qt post-paint retry alone did not resolve that ordering; the
extra retry machinery was removed. No polling, recurring timer or native C++ change.

**Build:** FreeCADPlusScripts completed in the retained native development tree.
The existing verified native libraries were reused; no C++ recompilation was needed.
All 27 Python files parse and exactly match the development payload. This is not
an owner build or shortcut delivery.

**Validation:** initial 21-case Bodies Only/visibility/unused-model suite: 19 passed,
one failure and one error, zero skips, native exit 0, 48.203 seconds. Both failures
were the native snapshot ordering defect above. After the final bounded fix, the
two affected cases plus four relevant editor/view lifecycle regressions passed
(6 cases, zero failures/errors/skips, 13.677 seconds, native exit 0). A separate new
Bodies Only native Sketch editor check passed (1 case, 2.413 seconds, native exit 0).
No complete successful suite was repeated. These runs cover all five new cases
and the 17 existing visibility/unused-model cases across the initial/focused runs.

Covered shared/repeated occurrences, nested saved Full/Reference/Excluded choices,
Body history, solid/sheet retention, curve filtering, Undo/Redo, recompute, independent
views, domestic/external unused editing, source-owned state, exact identity/native
visibility, idle refresh stability, editor entry/exit and panel/view cleanup.
Independent fresh-process reopen passed exact saved identity/visibility and resolved
filter checks, native exit 0. Inspected 2301x1278 normal-framebuffer images show the
active and faded repeated solid/sheet results retained, curves absent in Bodies Only,
and the edited occurrence's curve restored by Full Component while the other stays
filtered. This is bounded native-buffer evidence, not physical-monitor or long-session
responsiveness certification.

**Limits:** whole-object filtering does not split mixed solid/curve compounds into
new geometry. Native Body Tips remain authoritative. Reference-use eligibility,
Add Reference Feature operation design and full Group 1 acceptance remain unfinished.

**Final checks/cleanup:** all 27 Python files parse and byte-match the development
payload; 130 local link targets in the affected canonical documents resolve and
whitespace checks pass. Task profiles, fixtures, logs and captures under
`validation/g1_7b3b_bodies` were deleted after recording/inspecting the evidence.
The useful development build and dependencies are retained.

**Publication:** source milestone `93f6ac4f388af962a527297da3a94402b7e92576`
was pushed to origin `codex/freecad-1.1.4-baseline`; the exact remote revision was
verified. No owner package, desktop shortcut update, release or deployment.

## G1.7b3a unused-preview saved display — October 11, 2026

**Implementation:** unused-model previews now apply saved self Shown/Hidden/Excluded
and child Hidden/Excluded/nested Reference choices through the existing resolver and
native per-view selection context. A direct Reference remains visible; its own nested
exclusions remain hidden. The catalog definition's native visibility is still bypassed
only for temporary display. No new instances, identity/placement/geometry writes or
native Visibility changes. External choices remain source-owned. Recompute, Undo,
context exit and panel/view/source closure clear or reapply the temporary filtering.

`setComponentPreviewHiddenPaths` shares the existing native hide implementation,
using a separate scene context around PlusUnusedPreview. Resolution starts at the
first borrowed child provider to bypass the unused definition's hidden catalog switch.
Each preview has its own native key; other placed views retain their own visibility.
Refresh clears the wrapper before replacing borrowed display nodes; native wrapper
teardown clears its secondary entries. A private preview switch applies the self choice.
Bodies Only filtering and reference-use eligibility are not implemented by this increment.

**Build:** one batched FreeCADGui/FreeCADPlusScripts build passed in the retained
`C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds/freecad_1.1.4_context` tree.
Subsequent scripts-only copies corrected test expectations/capture setup; production
code did not change after that build. No owner package or shortcut delivery.

**Validation:** the initial 17-case unused-model/placed-visibility run passed 15,
with two assertion failures, zero errors/skips, native exit 0 (32.901 seconds). All
existing unused-model/native-editor/window/source cleanup and all five placed-visibility
cases passed. The new separate-view filtering case also passed. Source-owned external
state, Undo and visibility passed after correcting the test's assumption that native
linked documents cannot receive a mirrored undo entry. A trace confirmed source-owned
PlusChild properties and the native assembly entry `-> Change component display setting`.

The remaining domestic test passed in a focused run (2.676 seconds), zero errors,
failures/skips, native exit 0. Its corrections drain a queued save refresh before the
idle check and expect saved nested Reference exclusion when returning to File Edit.
It covers self/child hiding, Excluded, direct/nested Reference, Undo/recompute, native
picking, invalid-path preservation, exact identities/native visibility, save, idle
stability and final cleanup/restoration. No successful suite was rerun.

**Independent reopen and visual check:** exact IDs, saved choices, unchanged native
visibility and correct filtered ray picking passed in a separate process, native exit 0.
QtOpenGLWidgets must be imported before views are created, otherwise PySide can retain
a generic viewport wrapper. The first successful buffer read was unpainted and was
not accepted. Only capture was repeated after explicitly exposing/redrawing the window.
The inspected 1521 x 1128 normal framebuffer shows only the component's own box top;
the excluded child and nested Reference geometry are absent. This does not claim a
physical-monitor or long-session performance test. No further runtime checks followed.

**Static checks/cleanup:** all 26 Python scripts parse and byte-match the development
payload; 283 canonical local Markdown paths resolve, and whitespace checks pass.
Task output in validation/g1_7b3_unused is removed after recording these results.
Useful native builds/dependencies remain. No further runtime checks or implementation.

**Publication:** source milestone `ad4fa8d26a643dac90f979bd4beba500a987a39f`
pushed to origin/codex/freecad-1.1.4-baseline; exact remote revision verified.
Task validation output was deleted. No release or owner-build delivery.

## G1.7b2 contextual fading — October 11, 2026

**Implementation:** per-view native occurrence context, 75% transparency floor outside
its edited occurrence and descendants, preserved authored higher transparency, and
context/file/panel cleanup. No saved material/geometry/identity writes. The native
traversal callback and stack element preserve the authored render state. Missing native
linked draw paths preserve panel rows and receive one post-paint retry per invalidation,
without idle polling. Active Qt window tracking handles native wrapper teardown.

**Resolved defect:** actual draw-path tracing showed correct active/inactive matching
and authored [0,0.9] face transparency in both ordinary and transparent passes. Sorted
transparent triangles bypass the ordinary Part face draw. Coin's primitive color cache
was built without a material dependency: another occurrence could reuse its faded
per-face colors. SoBrepFaceSet::generatePrimitives now registers that dependency with
SoGLLazyElement::sendOnlyDiffuseColor during GL rendering. Native sorting, buffers and
preferences remain intact. Temporary diagnostics were removed. Earlier VBO/material-ID
hypotheses alone did not fix the defect and are not recorded as its cause.

**Build:** final FreeCADGui, PartGui and FreeCADPlusScripts build passed in
`C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds/freecad_1.1.4_context`.
The development executable is bin/FreeCAD.exe. The subsequent scripts-only refresh
changed the reopen verifier, not production code. No owner package or shortcut change.

**Runtime acceptance:** all five TestComponentFading cases passed, zero failures,
errors or skips, native exit 0 (18.274 seconds). These cover the exact single-face 75%
blend, active descendants/context switching, shared mixed per-face opacity, authored
90% transparency, independent views and panel closure, unavailable-path recovery with
zero idle refresh, identity/picking/recompute/Undo/hiding/isolation/save. The corrected
mixed-material normal framebuffer was inspected: the inactive red face fades while
the active red face remains opaque; both authored transparent blue faces retain their
appearance. This is normal-buffer inspection, not a physical-monitor or long-session
performance claim.

All six window cases, all nine unused-model cases and its window-cleanup prerequisite,
and all five explicit-hiding cases passed in the preceding affected runs. They were
not repeated after the narrowly targeted primitive material-cache correction.

**Independent reopen:** passed, native exit 0, exact native IDs and saved visibility,
zero saved transparency and preserved authored color at native serialization precision.
The first reopen failed an exact floating-point color comparison. Native
PropertyMaterialList stores rounded 8-bit RGBA; the verifier now permits only half an
8-bit channel step plus float rounding. Only this failed reopen was repeated. No
persistence implementation or saved fixture was changed.

**Checks and cleanup:** all 26 Python scripts parse and byte-match the development
payload; 283 canonical local Markdown paths resolve, and the whitespace check passes.
Task validation profiles, fixtures, diagnostics and captures under the approved
`validation/g1_7b2_fading` directory are removed after recording these results. The useful
native development build and required dependencies remain. No additional runtime tests
or subsequent implementation are authorized by completion of this increment.

**Publication:** source milestone `fbcecf84401b0f28675a4976035a880bcbaf75a8`
pushed to origin/codex/freecad-1.1.4-baseline; exact remote revision verified.
Task validation output was deleted after recording results. No release or owner delivery.

## G1.7b1 explicit per-view hiding — October 10, 2026

**Implementation:** Hidden/Excluded and nested Reference are resolved per occurrence
and applied through a unique native view context around existing geometry. No saved
native Visibility, identity or placement changes. Context transitions, Undo/recompute,
unused isolation and panel/view cleanup restore or reapply the appropriate paths.
The same saved shared-parent choice can produce different visibility in different
Edit views. Active self/ancestor traversal conventions are stated in ARCHITECTURE.
Fading, Bodies Only content filtering, Reference-use eligibility and saved display
choices inside unused previews are not implemented. Group 1/G1.7b remain incomplete.

**Build:** FreeCADGui and FreeCADPlusScripts passed in the retained development tree
with the VS BuildTools environment. The first plain-shell attempt lacked MSVCRT.lib;
initializing the compiler environment resolved that setup failure. The final native
wrapper-teardown rebuild also passed. No owner package/shortcut delivery.

**Validation:** initial four new cases passed (6.563 seconds). The affected 27-case
panel/window/unused-editor/saved-state run passed 25 and found two failures caused
by a missing/deleted Edit context in another visited view clearing panel rows.
The per-view update now uses the same file projection fallback as the tree. Review
also found an active-view unused lookup where an explicit view was required; corrected
and covered with simultaneous isolated/filtered views. Eight focused follow-up cases
passed (14.540 seconds), zero errors/failures/skips, native exit 0. This rerun covered
the four new cases, both failures and two affected external/window cleanup cases.
No complete Group 1 rerun was performed.

Independent reopen passed with exact IDs, saved display choices, unchanged native
visibility and recomputed Pad length. The initial framebuffer captures were uniform
unpainted buffers, not visual acceptance. Only the capture harness was repeated after
exposing and normally redrawing the test window; persistence was not repeated.
Inspected normal buffers show two original cylinders, one filtered occurrence with
the other intact, separate component-view context with both visible, and restored
geometry after panel closure. Native selection highlighting remains visible. Captures
were 1521 x 1128 on NVIDIA GTX 970, correct per-widget FBO, OpenGL error 0. This is
normal-buffer inspection, not a physical-monitor or long-session performance claim.

Native secondary Hide entries live on shared provider nodes. A final wrapper-destructor
cleanup and close/reopen case were added to prevent stale entries after view teardown.
The final five display/lifecycle cases all passed (8.309 seconds), zero errors, failures
or skips, native exit 0. No additional runtime tests followed. All twenty-five Python
files parse and match the development payload; 238 checked local Markdown targets
resolve and diff whitespace passes. The bounded payload's known unavailable Std_Measure
warning remains unrelated to this increment.

**Cleanup:** task profiles, fixtures, logs, helper scripts and captures in
`C:/Users/GAMING-PC/Documents/_temp/freecad/validation/g1_7b_visibility` are removed
after recording these results. Useful native development build/dependencies remain.

**Publication:** source milestone `8b7b382834` pushed to
`origin/codex/freecad-1.1.4-baseline`; exact remote revision verified. No owner delivery,
shortcut change, release or deployment.

## G1.7a saved display state — October 10, 2026

**Implementation:** schema-5 optional self/direct-child choices, old-schema defaults
without read-time migration, source-owned transactions, context-qualified checked
menus/tooltips, Excluded/Shown guard and non-destructive nested Reference resolution.
Structural Copy/Paste and independent definition copies preserve choices. Viewport
filtering/fading, reference-use enforcement and export integration are not implemented
by this increment. Existing native Visibility and geometry remain unchanged.

**Build:** FreeCADPlusScripts copy target passed in the existing development tree;
no native rebuild or owner delivery.

**Validation:** all six new saved-state cases passed, including real nested-menu
selection, self/direct-child defaults, shared context restoration, Excluded/Shown
refusal, schema-4 lazy reads and Undo/Redo upgrade, source-owned external state,
atomic rollback, independent copies and copied-instance choices. The initial run
passed all 35 existing affected pilot/conversion/hierarchy/external/panel/clipboard
cases before the menu harness stalled; that process was stopped and is not reported
as a completed passing suite. Follow-up checks were restricted to failures and code
affected by fixes. The final 18-case display/clipboard/window run passed 17 cases
and exposed one Copy-menu variable collision. After correcting it, both affected
Copy and Move menu cases passed (4.354 seconds), zero failures/errors/skips, native
exit 0. No unrelated complete-suite rerun was performed.

Corrections: internal metadata is hidden rather than marked read-only, allowing
panel edits while retaining actual read-only protection; the copy fixture supplies
unique nested definition labels; menu automation uses bounded native keyboard
navigation. Nested QAction wrappers were invalidated at popup return, so dispatch
captures the Python callback from the native triggered signal. Its callback list
has a distinct name from the selected component rows. Existing component-window,
stale-menu, native-editor and Copy/Move routing checks passed after relevant changes.

The independent process retained exact native identities and display choices for
domestic and external documents, both standalone and imported; the assembly checksum
was unchanged by source-only save, and Pad geometry was unchanged. Native exit 0.
Inspected actual menu captures show all four Part Types with Reference checked,
separate Visibility with Shown disabled for Excluded, and the intact tree hierarchy.
No viewport-rendering claim is made: no filtering/fading was implemented or tested.
All twenty-four Python files parse and match the copied development payload; whitespace
checks passed. Planned runtime verification is finished; do not repeat it absent a
new failure, change or material concern.

**Cleanup:** task profiles, fixtures, logs and captures were removed from
`C:/Users/GAMING-PC/Documents/_temp/freecad/validation/g1_7a_display` after results
were recorded. Useful native build/dependencies and tracked tests remain. All 121
checked local Markdown file targets resolve.

**Publication:** source milestone `47f766073d` pushed to
`origin/codex/freecad-1.1.4-baseline`; remote revision verified. No owner delivery,
shortcut change, release or deployment.

## Scope correction and parked operation — October 10, 2026

Point to Point implementation began after the owner allowed necessary new work,
but was stopped when the owner corrected its classification. Its unfinished source
and five proposed regression cases are preserved on local branch
`codex/point-to-point-parked`, commit `288f99e69c`; the branch was not pushed.
Python parsing and the script-copy target passed. **No runtime tests ran** and
no functional acceptance is claimed. The baseline checkout retains the previously
validated Translate/Rotate implementation. The development payload's twenty-two
scripts were restored byte-for-byte from that baseline and the new test copy removed;
no owner package, settings or shortcut was changed. Future CMake builds must use
the active branch's source configuration, as usual.

Group 1 owns panel/document structure and menu integration. Task-operation behavior
is tracked separately even where launched by that menu; its completion is not a
Group 1 gate. The roadmap preserves historical operation IDs/evidence without using
them as the next panel queue. For subsequent increments, run only relevant acceptance
checks once; repeat only in response to a failure, a fix or a material new concern.

## G1.6c4 Rotate — October 10, 2026

**Implementation:** the existing native task supports located parent/picked/two-point
axes, an optional picked pivot, native angular magnitude and Reverse. Both positions
and orientations change through one parent-frame rigid transform. Point references
include vertices/points, origins and circular-edge centers; references remain snapshots.
The view-only preview includes an axis arrow/pivot marker and corresponding shared
occurrences. Translate now uses the same placement-transform path. Existing atomic
source-owned Apply, Undo, reset, Persistent Selection, OK/Cancel and lifecycle guards
are reused. No modeling feature, joint, definition copy or persistence schema is added.

**Build:** FreeCADPlusScripts passed in the retained G1.6b native development tree.
Only the script payload changed; no native rebuild or owner/shortcut delivery.

**Validation:** **12/12 focused Translate/Rotate cases** passed (24.327 seconds),
then **62/62 combined Group 1 cases** passed (98.016 seconds). Both runs had zero
failures/errors/skips and normal native application exit. Coverage includes non-origin
pivots, located axes under rotated shared parents, two-point/reversed axes, circle
centers/origins, snapshot stability, rigid relative placement, nonaccumulating preview,
method switching, invalid angles, atomic rollback, full-turn no-op and Undo/Redo.

An independent process retained exact native IDs, rotated positions/orientations and
unchanged feature geometry. External source rotation survived standalone and assembly
reopen; source-only save left the assembly checksum unchanged. Inspected normal
framebuffer captures show clean shared previews with a located cyan axis arrow,
Cancel restoring original geometry without ghosts/axis overlay, and committed rigid
rotation matching the preview. Native task and Part Tree captures show the intended
controls, units and shared hierarchy. Camera, document identities and Undo state were
checked across preview/Cancel/Apply. The initial capture harness assumed an active
MDI subwindow while Tasks had focus; selecting the subwindow owning the model view
resolved that capture-only failure. The independent persistence verifier had already
passed and was not repeated. No renderer or owner-setting changes were made.

**Packaging/checks:** all twenty-two Python source/test scripts parse and match the
copied native development payload. All 117 checked local Markdown file targets
resolve; diff whitespace passed. Complete Group 1, remaining Move methods, original
workbench and long-session responsiveness acceptance remain unfinished. The bounded
development payload's known unavailable Std_Measure warning remains a limitation.
No further feature implementation or runtime tests followed planned acceptance.

**Cleanup:** task-only profiles, fixtures, captures and logs were removed from
`C:/Users/GAMING-PC/Documents/_temp/freecad/validation/g1_6c_rotate`
after recording results. Useful native build/dependencies and tracked tests remain.

**Publication:** source milestone `b14a8bc724` pushed to
`origin/codex/freecad-1.1.4-baseline`; remote revision verified. No owner-build
delivery, desktop shortcut change, release or deployment.

## G1.6c3 Move Components foundation and Translate — October 10, 2026

**Implementation:** the Part Tree action opens native Tasks. Whole sibling instances
move in their immediate parent's coordinates; shared/external parents own changes
in their defining file. Translate uses parent axes or a snapshot of a visible straight
reference, one nonnegative unit-aware length and Reverse. A temporary, unpickable
wire outline previews corresponding shared occurrences without document mutations.
Apply is one atomic Undo group; no-op, reset, Persistent Selection, Cancel after
Apply and OK behavior follow the confirmed workflow. Other workflow entries explain
that they await later implementation. No definitions/geometry/schema are copied.
The technical contract is in ARCHITECTURE, owner behavior in TASK_PANEL.

**Build:** existing G1.6b native development tree; FreeCADPlusScripts passed. Script
changes only, no native rebuild, owner package or desktop shortcut change.

**Validation:** **56/56 combined Group 1 cases** passed, zero failures/errors/skips,
normal application exit (79.406 seconds). After final preview-visibility and component
label corrections, the affected six movement cases passed again (14.677 seconds,
zero failures/errors/skips). Native context-menu entry and the Tasks Apply button,
preview without document mutations, rigid sibling movement, rotated/shared parents,
reverse, no-op, Apply/OK/Cancel, selection retention/removal and atomic Undo/Redo are
covered. Picked lines and infinite origin axes convert to parent coordinates; curved
or hidden references and invalid lengths are refused. Expression/read-only guards,
late-failure rollback, panel/file/Edit-context cleanup and external source ownership
also passed. Scaled frames remain explicitly unsupported; other Move methods and
complete Group 1/workbench/long-session responsiveness acceptance remain unfinished.

The independent fresh process retained exact native IDs, domestic placements and
external-source placements when opened both independently and through the assembly.
A further source-only save left the assembly archive checksum unchanged; a second
reopen retained that movement. Inspected viewport captures show temporary cyan wire
previews for shared children in differently rotated parents, restored original
placements after Cancel, and corresponding committed movement after Apply. Part Tree
shows the shared parent Edit state and the exact selected child; Tasks shows the
component's qualified model label, controls and unit-aware distance. Camera orientation
and document identities were retained. No owner settings or renderer changes were made.

Initial failures led to corrections for native form ownership, file-root context,
InputField rawValue/signals, Delete ShortcutOverride and qualified expression paths.
The first combined run had one old clipboard-fixture failure from delayed native
SyncView selection; draining that event before each independent fixture resolved it.
A final source review caught infinite axes without endpoints and preview of hidden
occurrences. Visual inspection caught internal link labels and a blank framebuffer
after the Tasks layout transition. The label is fixed; normal view.redraw before
capture produced clean Cancel pixels. That blank capture is not accepted evidence
of a renderer or on-screen display defect. No new feature work followed acceptance.

**Packaging/checks:** all twenty-one Python source/test scripts parse and match the
copied native development payload. All 115 checked local Markdown file targets
resolve. Diff whitespace passed. Task-only profiles, fixtures, captures and logs
were removed from
`C:/Users/GAMING-PC/Documents/_temp/freecad/validation/g1_6c_translate`
after recording results. Useful native build/dependencies and tracked tests remain.

**Publication:** source milestone `6e18b9289d` pushed to
`origin/codex/freecad-1.1.4-baseline`; remote revision verified. No owner-build
delivery, desktop shortcut change, release or deployment.

## G1.6c2 linked-instance Copy/Paste — October 10, 2026

**Implementation:** context-menu Copy/Paste and focused-tree Ctrl+C/Ctrl+V create
native links to the same definitions. A copied parent includes its children through
that shared definition; descendant selections are not pasted again. Repeated visible
occurrences remain distinct selections. Clipboard snapshots use document UUID/object
Name/ID plus copied local placement, LinkTransform and visibility. Paste preflights
all definitions and cycles, then creates the whole batch in one defining-document
transaction. External destinations require their own file's catalog/imports. No
implicit import, definition clone, schema change or system-clipboard override.
Failed transactions roll back all new links. New occurrences are selected; Edit,
History and camera remain unchanged. Native editors/pending operations and stale
menus/rows are guarded; panel closure discards its transient clipboard.

**Destination convention:** the owner notes confirm shared Copy/Paste followed by
movement but do not specify the exact Paste destination. An optional clarification
was asked; no answer had arrived when implementation began. The announced default
is the explicitly selected file/component parent, with copied placements retained
relative to that parent. This is an implementation convention, not recovered owner
approval. The technical contract records it; newer owner direction supersedes it.

**Build:** FreeCADPlusScripts passed in the existing native G1.6b development tree.
Only scripts changed; no native rebuild, owner delivery or shortcut change.

**Validation:** six focused cases and **50/50 combined Group 1 cases** passed,
zero failures/errors/skips, normal application exit (combined run 60.597 seconds). Two initial fixture assumptions
were corrected: a missing imported source removes invalid panel rows, and an empty
native transaction need not report HasPendingTransaction. Tests now retain the stale
row before closure and make an actual caller change before testing its transaction
guard. The first combined run's existing tab-switch check also required native
delayed SyncView selection to finish before starting its independent new-document
scenario; the isolated diagnostic confirmed this without changing application
preferences or selection behavior. A subsequent combined run exposed a real dock
reopen error: activeSubWindow could be temporarily absent while a native view still
existed. Panel state now finds the subwindow owning that view, and the singleton
releases the retiring panel before constructing its replacement. The clipboard's
panel-reopen case explicitly covers an absent activeSubWindow. The final combined
run passed after these fixes.

An independent process reopened domestic and external `.cadprt` fixtures with exact
native IDs, shared definitions/links and copied placements retained. A subsequent
external source-only change saved without changing the importing assembly checksum;
a second reopen retained that change. Clipboard contents correctly did not persist.
Inspected normal OpenGL pixels show three clean shared cylinders; the Part Tree
shows three parent occurrences with their shared children. The context menu shows
Copy and the expected disabled Paste after fresh startup. No owner preference or
renderer changes were made. These checks finish this increment; no further feature
implementation or runtime testing follows.

**Packaging/checks:** nineteen Python source/test files parse and match the copied
native development payload byte for byte. All 93 checked local Markdown file targets
resolve. Final diff whitespace passed. Task-only profiles, fixtures, captures and
logs were removed from
`C:/Users/GAMING-PC/Documents/_temp/freecad/validation/g1_6c_clipboard`
after recording the results; useful native build/dependencies and tracked tests remain.

**Publication:** source milestone `e092033275` pushed to
`origin/codex/freecad-1.1.4-baseline`; remote revision verified.
No owner build, shortcut delivery, release or deployment was performed.

## G1.6c1 component file tabs — October 10, 2026

**Implementation:** the two component context menus offer Open in new window.
It creates another native view of the current file with the selected occurrence's
Edit context, or the existing view-only isolation for an unused definition. Models
uses the originating tab's remembered occurrence. The original tab's context/camera
are retained, the new tab is labeled for its edited component, and the same native
source objects/transactions/save services are reused. No new document, placement,
model property, schema or permanent window record is introduced. Native feature
editors/pending operations block opening; stale menu actions are rejected. Failed
entry closes only the new view and returns to the original. View closure clears
panel state; panel reopening recognizes component tabs through a transient Qt property.
The component-window contract is in ARCHITECTURE.md.

**Build:** the existing native G1.6b development payload is reused; only the
FreeCADPlusScripts target changed. Its copy target passed. No native recompilation,
owner build, desktop shortcut change, release or deployment is part of this increment.

**Validation:** six focused GUI cases passed, followed by **44/44 combined Group 1
cases**, zero failures/errors/skips, normal application exit. These cover Models and
Part Tree menus, exact/remembered occurrence paths, child Edit in the same new tab,
original camera/context, source-owned Sketch/Pad and Undo/Redo, pending-editor and
stale-menu/row refusal, failed-open rollback, independent isolation, source/view
closure, event-driven labels and panel reopening.

The independent fresh-process verifier retained native IDs and source ownership,
changed a source Pad from 7 to 9 mm, saved it without changing the importing assembly's
archive checksum, then reopened again to confirm 9 mm. Inspected normal OpenGL
captures show the domestic component tab with its assembly context, a clean isolated
external cylinder, and the original two-cylinder assembly restored. Panel/tab-bar
captures show component/qualified external labels, active rows and Sketch/Pad History.
The original camera and Edit context remained intact. Contextual fading is still G1.7.

Two initial test expectations were corrected: native coordinated Undo legitimately
adds forwarding entries in dependent files for source changes (opening adds none),
and routine panel refresh clears transient menu feedback. The first combined runs'
sole picking failure was traced to the test fitting geometry before native camera
animation completed, producing an invalid camera/clipping combination. Test-owned
views now disable animation before rotation/fitAll; application defaults are unchanged.
The first visual harness also needed camera settling and an explicit hide/showNormal
transition after the hidden process launch before normal rendered pixels were
available. Renderer/read/draw framebuffer state was checked; final exposed-window
captures were clean. Earlier blank/widget-grab captures are not application display
acceptance. No renderer/driver/owner-preference change was made.

**Packaging/checks:** eighteen Python source/test files parse and match the copied
native-build payload byte for byte; 115 local Markdown link targets resolve. Diff
whitespace passed. Task-only profiles, fixtures, captures, probes and logs were
removed from `C:/Users/GAMING-PC/Documents/_temp/freecad/validation/g1_6c_windows`
after recording the results. Useful native build/dependencies and tracked tests remain.

**Publication/cleanup:** source milestone `a7c3adf4927648fb50213d95bda180af796b3654`
was committed and pushed to origin/codex/freecad-1.1.4-baseline; the remote revision
was verified. Task validation cleanup is complete. No broader
G1.6 completion, full-workbench inventory or long-session jitter acceptance claimed.
The development payload is retained; no owner delivery or shortcut change.

## G1.6b external completion and native acceptance — October 10, 2026

**Implementation:** unused external definitions stay in the assembly view for Models
selection, Edit, native Sketch/Pad History editing and viewport picking. Native
per-view catalog/edit contexts validate ownership and imported reachability, remain
silent/transient, and clear safely on view/panel/source/object teardown. A view-only
separator borrows live native display children rather than detached copies, preserving
picking and live editor preview. History starts the same active transaction as native
feature double-click, so accepted parameter edits support source-owned Undo/Redo.
No temporary App objects/links, visibility writes by isolation or schema changes.
The [architecture](ARCHITECTURE.md#unused-definitions-g16b) owns the contract.

**Build:** native development targets passed in
`C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds/freecad_1.1.4_context`.
Release-pinned LibPack 3.1.1.3 was taken from this tag's Windows workflow; local tools
were MSVC 19.44, CMake 3.31.6, Ninja, Python 3.12 and Qt/PySide 6.8.3. The release
preset kept default workbench options; three compile jobs and native precompiled
headers were used. One internal MSVC C1001 in unchanged TaskDressUpParameters.cpp
passed an unchanged single-file retry; the remaining build then passed.

Application/Part/Sketcher/PartDesign native libraries and script targets were built,
plus FreeCADPlusScripts and the standard materials, appearance/models, Show,
stylesheet/interface and Part Design data targets listed in DEVELOPMENT_GUIDE.
The initial narrow payload lacked material data and Show/styles; those setup gaps
were corrected before acceptance. Native configuration also exposed the old Plus
module condition `BUILD_PARTDESIGN`; src/Mod/CMakeLists.txt now correctly uses
`BUILD_PART_DESIGN`, so its script target participates in the native build.

**Validation:** the final focused run passed **9/9** cases, and the combined pilot,
legacy conversion, hierarchy, external-file, panel and unused-model suite passed
**38/38**, with **zero skips**. All loaded modeling/interface modules came from the
new development build. Two actual workflow failures were found and fixed: History
entry lacked the native command transaction, and detached display copies were not
natively pickable. Tests now cover source-owned accepted Pad Undo/Redo, real viewport
selection retaining the assembly tab, per-view contexts, invalid/removed imports,
ordinary external-parent refusal, and closing the source during a native Sketch edit.

Fresh-process domestic/external reopen checks passed with object identities intact.
An external Pad changed from 7 to 9 mm and saved through its defining file; the
assembly archive checksum stayed unchanged, and another reopen retained 9 mm.
Normal OpenGL framebuffer captures were inspected: two assembly cylinders before
isolation, one external cylinder during isolation, clean native Sketch editing,
a shortened native Pad preview without an old solid, and the original two cylinders
restored afterward. The qualified temporary Part Tree row was bold/active and last;
other rows remained gray/selectable. Capture used the normal framebuffer, not
QOpenGLWidget.grabFramebuffer.

**Packaging/checks:** all seventeen Python source/test files parsed and matched the
native build's copied payload byte for byte. Diff whitespace and 115 local Markdown
link targets passed. Task-only profiles, fixtures, logs and captures were removed
from `C:/Users/GAMING-PC/Documents/_temp/freecad/validation/g1_6b_external` after
recording the results. The extracted pinned LibPack and useful native development
build remain; the unneeded downloaded LibPack archive was removed.

**Publication/delivery:** source milestone `54ea2843a3f8c3fe89d2a495964fa290274708cf`
was committed and pushed to origin/codex/freecad-1.1.4-baseline; the remote revision
was verified. No release, deployment or owner-build delivery. This bounded development payload is not full-workbench or
long-session responsiveness acceptance. The existing owner desktop shortcut was
not changed; original workbench source/configuration remains intact.

## G1.6b domestic increment and acceptance - October 10, 2026

Historical checkpoint: its external-editing limitations are resolved by the native
completion record above; the following preserves the earlier evidence.

**Implementation:** unused domestic definitions support Edit in the current view,
a temporary last Part Tree child, active fill/bold text, gray selectable assembly
rows, native History and Sketch/Pad adapters. Native display groups are hidden by
view-only scene switches while a detached native definition display is shown.
No temporary App objects, instance links, authored Visibility writes or Undo entries
are used for isolation. File/placed Edit and panel/view/document close clean up;
definition removal clears isolation and Undo does not reopen it. The
[architecture](ARCHITECTURE.md#unused-definitions-g16b) owns details.

**Runtime:** all thirty-five combined tests passed in 34.668 seconds using this
checkout's scripts in the verified 1.1.4 GUI runtime with an isolated profile.
Six new cases cover actual Qt domestic Edit/selection, temporary row placement,
native visibility commands remaining hidden, restoration, native Sketch editor and
context-exit guard, geometry/History ownership, Undo/Redo, save while isolated,
per-view state, panel/view/document cleanup and source-removal recovery. IDs, native
link inventory and authored visibility survive saving; no temporary instance is
serialized. External-unused Edit is tested for refusal without mutation or losing
an existing domestic isolation session. All twenty-nine earlier regressions passed,
including legacy conversion and placed-external editing.

**Known remaining case:** two focused attempts at external unused Edit failed when
native selection activated the source tab. A trace localized the switch after panel
Edit returned; native Tree sync and Document::trySetEdit's local-parent requirement
explain why an unplaced external definition does not have the same editor route as
a placed link. The unsupported route is now refused before isolation starts, with
a message directing editing to the defining file. Selecting its catalog row can
still activate that source tab. This is a bounded partial implementation, not a
change to owner requirements or a passed external-unused workflow. The next task
is to finish that integration, including source-only save and Undo checks.

**Fresh process / visual:** the saved isolated fixture reopened without isolation,
with all IDs, visibility and native link names intact. Editing its unused Pad from
7 to 9 mm produced valid 81*pi mm3 geometry and saved a separate file. Inspected
3441 x 1767 normal framebuffer captures show two assembly cylinders before editing,
only the larger unused cylinder during editing and both originals after exit.
The initial panel capture exposed a theme whose disabled text was white; explicit
gray inactive-row styling corrects that confirmed presentation requirement.
The repeated fresh-process/visual check passed and the final panel pixels show gray
assembly rows and the green/bold temporary last child. These are bounded automated
checks, not complete panel or long-session responsiveness acceptance.

**Build / delivery:** CMake script copy/install and syntax checks passed for all
seventeen module/test scripts. Native C++ was not rebuilt. No owner executable was
delivered or desktop shortcut changed; the panel remains developer opt-in.

**Publication / cleanup:** this domestic increment is committed and pushed to
origin/codex/freecad-1.1.4-baseline with remote hash verification at handoff. Task-only
profiles, fixtures, captures, logs and script packaging outputs are removed after
recording these results. Tracked code/tests and useful baseline builds are retained.

## G1.6a implementation and acceptance - October 10, 2026

**Implementation:** opt-in Components dock with Models/Part Tree/History, nested
external catalogs, one pinned file row, placed-component Edit, full occurrence
tracking and native selection. All shared occurrences/model rows have active fill
and bold text; the edited occurrence has a separate outline. Models reuses the last
occurrence per view. File History has undoable Origin/plane visibility controls.
Rows retain identity across updates; document/GUI events coalesce, idle has no polling,
invalid/stale actions are refused and closing unregisters observers. The
[architecture](ARCHITECTURE.md#panel-foundation-g16a) owns the detailed contract.
Unused-model editing, component windows, remaining context actions, Part Type and
contextual fading are not implemented by this increment.

**Runtime:** all twenty-nine combined tests passed in 24.228 seconds in the verified
1.1.4 GUI runtime with the checkout's scripts and an isolated profile. Six panel
cases joined all twenty-three prior regressions. Actual Qt mouse events checked
single-click selection without Edit, double-click Edit, occurrence memory and shared
highlighting. Tests also covered row preservation across rename/refresh, independent
view contexts, changed-tab/stale-row refusal, Undo of occurrence removal, external
Edit staying in the assembly, origin visibility Undo/Redo/save/reopen, observer cleanup
and no idle refresh. Twenty rename events coalesced into at most two refreshes.
Panel presentation created no native objects or Undo transactions.

The first focused run had a click-selection failure and an origin fixture that
assumed a hidden Origin implied a hidden plane. The fixture now explicitly hides
the plane before Show. The click failure did not reproduce in the next focused run
or the full suite; no speculative application fix is claimed for that first result.
The two final suites exited normally with no panel observer errors. Baseline regression
logs contained their expected invalid-Pad and source-copy UUID diagnostics.

**GUI/fresh process:** a separate process opened the saved panel fixture, retained
all native object IDs and Undo count through panel interaction, and returned to the
four file-origin History rows. Inspected captures of Models, Part Tree, component
History and file History were clean/readable. Both shared-child occurrences were
highlighted and the second had the Edit outline; History showed Sketch/Pad without
Body rows. This is bounded automated interaction evidence, not long-session jitter
acceptance or full panel completion.

**Build/delivery:** CMake script copy/install passed and all fifteen module/test
scripts matched source; syntax and whitespace passed. Native C++ was not rebuilt.
The developer panel is opt-in and the original tree/workbenches remain. No owner
executable was delivered or desktop shortcut changed. Reproduction is in the
[guide](DEVELOPMENT_GUIDE.md#component-panel-foundation-validation).

**Publication/cleanup:** the coherent G1.6a milestone is committed and pushed to
origin/codex/freecad-1.1.4-baseline, with remote hash verification at handoff. Task-only
profiles, generated CAD fixtures, captures, logs and script packaging outputs are
removed after recording results. Tracked implementation and tests are retained.

## G1.5 implementation and acceptance - October 10, 2026

**Implementation:** schema 4 adds native imported-file catalogs with persisted
source UUIDs and pre-restore dependency checks. Importing includes nested catalogs
without placing geometry. Native linked occurrences resolve across defining files;
Sketch/Pad edits transact in the source file while retaining the assembly tab/context.
Explicit source Save writes only that file. Independent recursive copies preserve
native graphs and require an explicit placement-replacement selection. Circular
imports/nesting are refused before mutation. Schemas 1-3 remain supported with an
explicit undoable upgrade before external imports. Full contracts, save ordering,
exact-path recovery and remaining UI boundaries are in [ARCHITECTURE](ARCHITECTURE.md).

**Runtime:** twenty-three tests passed in 14.221 seconds in the verified official
1.1.4 GUI runtime using this checkout's module and an isolated profile: seven new
external-definition cases and all sixteen prior regressions. They cover nested
unused catalogs, same-name distinct definitions, source-only geometry ownership,
source Undo/Redo, domestic/external independent copies with nested shared links,
explicit selected-placement replacement and Undo/Redo, unimported targets, file and
component cycles, schema upgrade, unsaved files, missing/wrong/future dependencies,
missing definition targets, failed defining-file saves and recovery. A review-found
save-order case now refuses unsaved intermediate import catalogs before overwriting
the assembly. Native dependent-file Undo entries are expected, not evidence that
model geometry moved into the importing file.

A separate process reopened the Assembly -> Hardware -> Fasteners fixture, retained
native source UUID/object IDs and full occurrence paths, changed the external Pad
from 5 to 8 mm and saved only Fasteners. The assembly archive hash stayed unchanged;
its two occurrences updated to 32*pi mm3 and retained the 8 mm length on reopen.
Missing dependency recovery restored the original exact file/path and retried;
identity mismatches never fell back to same-named definitions. Failure preflight
opened no documents and preserved fixture archives. No owner files were touched.

**GUI:** native Sketch and Pad editors entered/exited through the second nested
external occurrence using setEdit/resetEdit. The assembly stayed active; resolved
source feature and Edit path remained correct. The normal framebuffer (3441 x 1767)
showed exactly two clean cylinder instances. Initial capture-harness attempts found
an additional native OpenGL widget and an unloaded Qt binding; selecting the active
MDI window and importing QtOpenGLWidgets resolved capture, without product changes.
This does not claim full panel, mouse-driven flow or long-session jitter acceptance.

**Build/delivery:** script-only CMake copy/install passed; all thirteen module/test
scripts matched source and syntax/whitespace passed. Native C++ was not rebuilt.
No new owner executable or panel is delivered; the desktop shortcut remains on the
archived fork. G1.6 and other groups have not begun. Reproduction is documented in
[external-definition validation](DEVELOPMENT_GUIDE.md#external-definition-validation).

**Publication/cleanup:** the coherent G1.5 milestone is committed and pushed to
origin/codex/freecad-1.1.4-baseline, with the remote hash verified at handoff.
Task-generated profiles, fixtures, captures, logs and temporary script-build outputs
are removed after the recorded checks; tracked tests remain available.

## G1.4 implementation and acceptance - October 10, 2026

**Implementation:** schema 3 supports nested domestic definitions and shared native
App::Link instances, parent-owned local placements, full occurrence paths and cycle
preflight. Native Plus Edit, Part and Body contexts carry the selected path; History
omits child links and Body rows. Legacy Part/link trees convert with native IDs,
frames and shared targets preserved, with intentional group-edge replacements
recorded. Schemas 1/2 retain their previous bounds until an explicit undoable upgrade.
The [architecture](ARCHITECTURE.md) owns the full contract and remaining limitations.

**Runtime:** sixteen tests passed in 7.358 seconds using the verified official
1.1.4 GUI runtime, an isolated profile and this checkout's scripts. Five hierarchy
cases joined all eleven existing pilot/conversion regressions. They covered shared
Pad edits in repeated parents, composed rotations/translations, moving one child
placement across all parent occurrences, Undo/Redo, cycle/cross-file rejection,
rollback, independent view contexts, stale/ambiguous paths and explicit schema upgrade.
Definitions could retain their own geometry and child components simultaneously.

A second process reopened both a newly created hierarchy and a converted legacy
assembly, retained object IDs/paths/placements, edited shared geometry and saved
separate results. In the native fixture a 2 mm radius Pad changed from 9 to 11 mm;
in the converted fixture three occurrence paths reflected Box lengths of 5 then
7 mm (volumes 60 then 84 mm3). Legacy Part and link placements, native transform
modes, geometry centers and shared targets survived conversion. The source FCStd
hash remained unchanged. No owner files were converted.

**GUI:** original Sketch and Pad editors opened through the second repeated
occurrence and exited using native resetEdit. The full Edit path remained selected
and the original 9 mm Pad remained valid. A normal viewport framebuffer capture
(2301 x 1202) showed exactly two parent boxes and two shared child cylinders, with
no extra visible stored definitions or capture corruption. The check did not claim
full panel interaction, mouse-driven acceptance or long-session jitter testing.

**Build/delivery:** script-only CMake copy/install passed; all eleven module/test
scripts matched source and syntax/whitespace passed. Native C++ was not rebuilt.
No new owner executable or full panel is delivered; the desktop shortcut remains
on the archived fork. External-file work and panel construction have not started.

**Publication/cleanup:** the coherent G1.4 milestone is committed and pushed to
origin/codex/freecad-1.1.4-baseline with the remote hash verified at handoff.
Task-generated fixtures, profiles, captures, logs and temporary script-build outputs
were removed after results were recorded. Tracked tests are reproducible through
the [guide](DEVELOPMENT_GUIDE.md#hierarchy-validation).

## G1.3 implementation and acceptance - October 10, 2026

**Implementation:** isolated `conversion.convert_file` plus schema-2 support for
native standalone geometry. Preserves native single-Body features, sketch attachment
and profile references, expressions, names, labels, object IDs and placements.
Empty files, native Boxes and static shapes/curves are supported. Unknown standalone
Part-derived geometry requires explicit fallback; loss reporting persists in the
new file. Unsupported graphs fail without an output file. The [architecture](ARCHITECTURE.md)
owns the complete conversion and schema contract.

**Runtime:** eleven tests passed in 5.253 seconds in the matching official 1.1.4 GUI
process: five conversion tests and the six existing pilot tests. A separate process
then passed reopen/edit/recompute/save of the converted Body. Final processes exited
normally with code 0. Checks used only generated fixtures in an isolated profile.
No owner document was converted or modified.

The native Body fixture retained translation/rotation, an origin-plane sketch
attachment, Pad Profile and an expression-driven Length. The converted input changed
from 5 to 7 with Length changing from 10 to 14 mm; Undo/Redo restored those values.
A fresh process verified identity/reference/placement persistence and changed the
input to 8, producing Length 16 mm and valid geometry before saving a separate file.
The original FCStd hash remained unchanged. An open source's deliberately different,
unsaved input stayed at 9 and remained dirty; conversion used the saved disk version.

Other checks covered an editable native Box, a static curve, a valid empty file,
explicit geometry-only recovery and persisted warnings after reopen, rejection of
multiple roots, injected save failure, existing-destination protection and staging
cleanup. Schema-1 files reopened and saved without upgrading. Adding a new sketch
to a converted direct-geometry component still creates the backend Body correctly.
The new converted file deliberately has a distinct Document.Uid, with source/output
UUIDs recorded in ConversionReport; native object IDs remain stable except for the
explicitly reported replacement of a geometry-only fallback object.

**Build and delivery:** script-only CMake build/install passed; all eight scripts
matched source byte-for-byte and syntax/whitespace checks passed. Native C++ was
not rebuilt. No new owner executable, conversion dialog or full panel is delivered;
the desktop shortcut remains on the archived fork. No unrelated workbench/UI
behavior was changed or baseline display testing repeated.

**Publication/cleanup:** the coherent G1.3 milestone is committed and pushed to
origin/codex/freecad-1.1.4-baseline with the remote hash verified at handoff.
Task-generated profiles, fixtures, logs and temporary script-build outputs were
removed after recording results. Tracked fixtures remain reproducible through the
[guide](DEVELOPMENT_GUIDE.md#legacy-conversion-validation).

## G1.2 implementation and acceptance — October 10, 2026

**Implementation:** a new opt-in script module under src/Mod/FreeCADPlus and its
CMake inclusion. One native file root, domestic Part001 catalog definition and
linked occurrence; native per-view explicit Edit; automatically owned backend Body;
native Sketch/Pad adapters; Body-free history projection; validated schema-1 `.cadprt`
open/save. No archived application code was restored. Original native application
and workbench source and submodule pins remain unchanged. The [architecture](ARCHITECTURE.md)
owns metadata, invariants and pilot limits.

**Runtime validation:** this checkout's scripts loaded into the verified official
1.1.4 executable listed below, with an isolated temporary profile. Six regression
cases passed in 2.109 seconds: structure/empty file, per-view Edit isolation,
modeling/ownership/rollback/Undo/Redo, persistence, future-schema/failed-save
protection, and unchanged native legacy modeling. All final test processes exited 0.

The rectangle Sketch -> Pad produced 1000 mm3 at 5 mm and 1600 mm3 at 8 mm;
Undo/Redo restored both states. Invalid Pad and unowned geometry transactions
rolled back. A valid empty component file saved successfully. Selecting a component
while in File Edit did not grant the adapter an editing target. Independent views
retained separate contexts.

Exact `.cadprt` filenames, preserved CheckExtension, idempotent reopen, native
Document.Uid/object names/IDs, linked targets and rotated/translated occurrence
placement passed. A second process reopened the saved pilot, changed its native
Pad to 7 mm (1400 mm3), recomputed and saved a separate edited file. Future-schema
files were refused without content changes; a native save failure preserved the
prior valid file, pending edit and dirty state. A renamed FCStd was refused as
unversioned. A normal FCStd native Body/Sketch/Pad control remained functional.

**GUI validation:** the pilot sketch entered/exited the original Sketch editor.
The original PartDesign_Pad command opened its native task and accepted through
its existing OK button, producing a valid 2000 mm3 solid and the correct Body Tip.
The normal viewport buffer (2301 x 1202) showed one clean solid with definition
hidden and linked instance visible. Capture used the previously established
framebuffer-read procedure. Full panel, physical monitor and long-session jitter
acceptance are not claimed.

**Build:** this script-only module configured, copied and installed successfully
using the repository's CMake helper and existing Ninja. No unchanged native C++
code was rebuilt. Build/install outputs were byte-compared to source. No new owner
executable was produced; the desktop shortcut still targets the archived fork.
This is a development pilot, not a delivered component-panel UI. Original file and
workbench commands are not globally overridden. The full panel is G1.6.

**Publication and cleanup:** the coherent G1.2 milestone is committed and pushed
to origin/codex/freecad-1.1.4-baseline, with the remote hash verified at handoff.
Task-generated profiles, fixtures, captures, logs and the temporary script-build
harness/output were removed after recording these results. Tracked tests remain
reproducible using the [development guide](DEVELOPMENT_GUIDE.md#component-pilot-validation).

## Clean FreeCAD 1.1.4 baseline

Owner requested the clean latest stable source in the existing fork on October 10,
2026. Official releases/latest resolves to 1.1.4; 26.3rc1 is separately labeled a
release candidate. Selected official commit:
4fd3bf320d9566a27e60069fc8387448aaa3a094.

Local branch: codex/freecad-1.1.4-baseline. Source checkout and release-pinned
submodules are present. Original tracked source matched the official tag before
the documentation/ignore overlay. Four stable submodules replace the previous
seven recursive modules. Old dependency/cache remnants were removed only after
3,740 files in 45 directories matched the verified source archive.

Preserved the five UI specifications, source evidence, original documents/icons,
unverified-change inventory and archive reference. Historical implementation
records now live under archive/pre-restart-docs. Active source links in the review
inventory point to the immutable old-fork commit, not similarly named stock files.
No owner requirement has been approved or rejected by this transition.

Integrity checks pass: all original application source matches upstream 1.1.4;
all four pinned submodules are clean; requirement wording in the five specifications
is unchanged apart from evidence-link destinations; 664 historical documents/assets
are byte-preserved. Active documentation links/icons and staged whitespace pass.
Published baseline commit f608ea07afffa1ed3a426b09d207b59bf4e8bfd7 to
origin/codex/freecad-1.1.4-baseline and verified the remote hash. GitHub default
branch and local origin/HEAD now point to this baseline. Old main and the archive
tag remain intact. A final documentation commit records this completed handoff.
Committed archival blob hashes also match all 664 preserved documents/assets.
Temporary source staging was removed after checks. The subsequent runtime check
below uses the official binary; this checkout has not been compiled locally.

## Stable baseline inventory and light runtime check â€” October 10, 2026

**Result: provenance, source integrity, core functionality and the light baseline
display check pass.** The earlier viewport artifacts were reproduced only through
the capture method; direct display-buffer reads are clean. This is a bounded
baseline check, not exhaustive GUI acceptance or an owner-ready Plus build.
No application source was changed.

### External release evidence

- [Official FreeCAD 1.1.4 release](https://github.com/FreeCAD/FreeCAD/releases/tag/1.1.4):
  published September 28, 2026; neither draft nor prerelease. The latest-stable
  endpoint selected this release; 26.3 RC1 is a prerelease.
- Release commit `4fd3bf320d9566a27e60069fc8387448aaa3a094` has successful upstream
  [Build Release](https://github.com/FreeCAD/FreeCAD/actions/runs/36432494038) and
  [FreeCAD master CI](https://github.com/FreeCAD/FreeCAD/actions/runs/36431033844)
  workflow runs. This is publisher release/CI evidence, not an independent
  certification of this PC or a guarantee of every operation.
- Original source, workbench definitions, build files and tests still match
  `upstream-1.1.4`. Only the instruction/documentation/ignore overlay differs.
  All four release-pinned submodules are clean.

### Local package inventory

The tested executable is a fresh official portable package on this PC, separate
from older Plus builds and any separately installed FreeCAD. It reports exactly
this checkout's source commit. It is not a locally compiled fork binary.

| Item | Observed value |
| --- | --- |
| Package | `FreeCAD_1.1.4-Windows-x86_64-py311.7z`, 418,088,341 bytes |
| Package SHA256 | `4828741fc91ee37fafcdb97a1abacb18b04ba451ac4372d9ff7a7349b36f4d6d`, matches publisher release digest |
| Executable SHA256 | `7b38c5d5aa2c74f830539c1c5c44cbf6e3e8e157292c718f9ee24ac6d3e12cf6` |
| Windows signature | Valid; The FreeCAD project association AISBL |
| FreeCAD runtime | 1.1.4, revision `20260928 (Git shallow)`, commit `4fd3bf320d9566a27e60069fc8387448aaa3a094` |
| Python / Qt / Open CASCADE | 3.11.14 / 6.8.3 / 7.8.1 |
| Payload after checks | 35,589 files; 2,307,887,823 bytes, including runtime-created caches |
| Local source build | Not configured or compiled; cached 26.3 LibPack is not assumed compatible with 1.1.4 |

Payload directory:
`C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds/freecad_1.1.4_official_baseline/FreeCAD_1.1.4-Windows-x86_64-py311`.
Executable: `bin/freecad.exe` beneath it. The verified download is retained under
`test-builds/dependencies/FreeCAD-1.1.4-official` for reproducible extraction.
Both are useful baseline dependencies, not superseded builds.

All 19 registered workbenches activated successfully: Assembly, BIM, CAM, Draft,
FEM, Inspection, Material, Mesh, OpenSCAD, Part Design, Part, Points, Reverse
Engineering, Robot, Sketcher, Spreadsheet, Surface, TechDraw and Test Framework.
`NoneWorkbench` is additionally registered as the empty workbench.

The package contains 30 module directories: AddonManager, Assembly, BIM, CAM,
Draft, Fem, Help, Idf, Import, Inspection, Material, Measure, Mesh, MeshPart,
OpenSCAD, Part, PartDesign, Plot, Points, ReverseEngineering, Robot, Show, Sketcher,
Spreadsheet, Start, Surface, TechDraw, Test, Tux and Web. Module directories are
not all selectable workbenches: upstream MeshPart does not register its own
workbench, and Start is a command. No Plus workbench filtering was applied.

### Local checks and limits

Checks used the actual GUI executable's Python/Qt APIs with temporary
`FREECAD_USER_HOME`, `FREECAD_USER_DATA`, `FREECAD_USER_TEMP`, user and system
configuration paths. Existing owner preferences and addons were not used.

| Check | Result |
| --- | --- |
| GUI startup, runtime identity and workbench activation | Pass; all 19 registered workbenches loaded |
| Sketch solver and Pad | Pass; constrained 20 x 10 mm rectangle padded 5 mm produced a valid 1,000 mm3 solid |
| Recompute, Undo and Redo | Pass; Pad length 5 -> 8 mm changed volume 1,000 -> 1,600 mm3; Undo and Redo restored both states |
| Pocket | Pass; radius 2 mm, depth 3 mm produced a valid 1,562.300888 mm3 solid |
| Spreadsheet expression and native Link | Pass; cell-driven pocket depth updated model and linked instance; 30 mm instance offset retained |
| Part Boolean | Pass; box/cylinder cut produced a valid solid with expected volume |
| STEP and STL | Pass; STEP export/reimport preserved volume; STL reopened as a solid mesh with 124 facets |
| FCStd persistence | Pass; 15-object model, expression and link survived save/reopen and separate-process restart; subsequent edits recomputed correctly |
| Model image export | Pass; visually inspected image shows both solid instances and their circular pockets correctly |
| Event processing and process exit | Pass; timed Qt callbacks and view switching completed; successful primary and cold runs exited normally with code 0 |
| Baseline viewport rendering and responsiveness | Pass in the focused follow-up below; capture-induced artifacts isolated, camera/resize/workbench checks clean. No comprehensive jitter benchmark claimed |

The primary run passed 10 automated check groups and the fresh-process run passed
four, including repeated startup/render/event-loop checks. Successful capture calls
alone do **not** establish correct visible rendering. The primary run took about
30 seconds, the cold run about 12; these include initialization and test delays,
and are not startup benchmarks. No exhaustive suite, complex real-world assembly,
CAM machining, FEM solver, long-duration interaction or manual jitter comparison
was performed.

Initial automation waited at BIM's normal welcome dialog. Only the task-owned
process was stopped; BIM `FirstTime=false` in the temporary profile allowed the
check to finish. A later capture-only harness used an unavailable compatibility
import; correcting it to PySide6 allowed that probe to finish. Neither interruption
is counted as an application crash.

OpenSCAD's workbench loaded, but reported its external OpenSCAD executable was
not found. Operations requiring that program are not verified or ready. Other
external solvers/toolchains were not validated.

### Display gate resolved â€” October 10, 2026

The owner requested resolution and was unavailable for manual tests. The agent
completed an automated comparison and interaction check using the same official
binary with fresh temporary settings. Native computer-use inspection still failed
to initialize (Windows sandbox helper setup), so FreeCAD's own GUI/OpenGL APIs
provided the evidence. No owner visual test or mouse-driven test is claimed.

**Finding:** `QOpenGLWidget.grabFramebuffer()` produces the stippled/colored image
on this system. Reading the existing viewport framebuffer directly with
`glReadPixels`, without invoking a capture-triggered redraw, produces the correct
image, including both blue solids, circular pockets, navigation cube and axes.
The normal display buffers before capture, after capture and after an ordinary
redraw were visually clean and byte-identical. This isolates the observed defect
to the capture path; it does not establish the precise underlying Qt/Coin/driver
fault. No application or graphics-driver workaround was necessary.

| Evidence | Observed result |
| --- | --- |
| Renderer | NVIDIA GeForce GTX 970/PCIe/SSE2; OpenGL 4.6.0 NVIDIA 560.94 |
| Qt / display scaling | Qt 6.8.3; device pixel ratio 1.5 |
| Initial display buffer | Default FBO 2 was bound; color attachment read; no OpenGL read error |
| Clean before/after/redraw images | All SHA256 `798ad968468a15cfc27962dcabf38c17f78e8baaea4834a6d165fd881a6ea040` |
| Corrupt Qt capture | SHA256 `9fb219e96b5cdf5ee91f865e2aa79dc63e906e1d79f05c14bc09569222b68133` |
| Camera changes | Front view, 13 orientation updates through 48 degrees, zoom to 80% of prior camera height, and restored isometric view completed |
| Window resizing | 1280 x 900 -> 1100 x 760 -> 1280 x 900 logical window sizes; viewport resized correctly |
| Workbench changes | Part -> Sketcher -> Part Design completed with clean viewport buffers |
| Display captures | Eight interaction-stage buffer reads, all without OpenGL errors; inspected front, rotated, zoomed, resized, switched-workbench and restored views were clean |
| Idle stability | Final view and repeat after a one-second idle interval were byte-identical: SHA256 `057eba7ce2c0cf4f4f4adea10f3feda72f22864970fb965b1f7307c38cc44252` |
| Event processing | 262 callbacks on a 50 ms timer; largest observed gap 0.344 seconds, including workbench initialization/capture overhead |
| Geometry and exit | Sample remained a valid solid at its expected volume; successful diagnostic and interaction runs exited with code 0 |

The first interaction harness omitted the Pivy camera binding import and stopped
advancing at zoom. Only its own process was terminated; importing the binding made
the complete rerun pass. This was a probe error, not an application crash. A Pivy
SWIG deprecation warning did not affect the completed check.

This closes the light baseline display gate without requiring owner testing.
It establishes clean rendered viewport contents and bounded API-driven interaction
on this PC; it is not a monitor/video capture, frame-rate benchmark, long-session
stress test, or proof about the archived fork's unrelated UI jitter. No source,
owner settings, global graphics settings or driver changes were made. The
[development guide](DEVELOPMENT_GUIDE.md#viewport-capture-validation) records the
capture method for future checks.

The existing desktop `FreeCADPlus.exe - Shortcut.lnk` still targets
`test-builds/freecad_plus_2026-10-10_part_types_payload/FreeCADPlus.exe`, with that
payload as its working directory. It launches the archived fork, not this baseline.
The official package is retained for baseline verification; no new owner build,
shortcut delivery or release is claimed. Temporary macros, test profiles, models,
logs and captures are removed after recording this durable result.

## Recovery references

Verified source archive and restoration evidence: [ARCHIVE_REFERENCE.md](ARCHIVE_REFERENCE.md).
Previous fork final main: b3d8a0a2fe532ca1693132eac5ab24a2bd1651c2.
Archive tag: archive/freecad-plus-2026-10-10, checkpoint
29496214b34a53fa1d479f35ab5669b41ed4fb18.
The old main history remains available; no force-push or history replacement is used.
