# FreeCAD Plus: Current work state

## Authorized objective and stopping boundary

Continue Group 1 only. **G1.7b3s split/join creation integration and its planned
checks are complete.** Stop runtime work here. Next: split/join input editing
admission through existing native link/property editors. Group 1 remains incomplete.
Add Reference Feature and cross-component Full Component transfer workflows remain
separately unresolved. No owner delivery.

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
