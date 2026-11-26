# Save All and Hidden line correction — November 26, 2026

Implemented after the owner approved the pending changes in chat. Save As already
existed; the pending toolbar request was Save All between Save and Save As, with
the explicitly chosen scope of every open file in the window, including imports.
See the [approval ledger](../../ui-ux-specs/EVIDENCE_AND_DECISIONS.md#save-all-and-hidden-line-correction--november-26-2026).

## Review provenance

The direct [approved toolbar screenshot](approved-toolbar.png) and
[approved Hidden line screenshot](approved-hidden.png) were presented before
implementation. Sessions 38e412ce3308 and 9c418841bda1 were re-inspected: previews
valid, no scope violations, exact fingerprints recorded in the approval ledger.
Chat approval was used without altering companion approval state. All four affected
main-source files matched their reviewed baselines after the intervening mesh fix;
the exact reviewed candidates were applied without changing the proposed behavior.

## Save All

The Plus common toolbar now orders Save, Save All, Save As. Its new button uses the
existing native Std_SaveAll QAction, icon, enablement and save backend. Native
dependency ordering, file types, dialogs, cancellation and errors are retained.
An actual click saved four modified documents: an assembly, its hidden imported
library, a nested imported fastener file, and another unrelated open file. Changed
archive hashes and serialized lengths verified writes. Object/file identities,
Undo counts, active document and Edit context remained unchanged.

See [installed toolbar](installed-toolbar.png), [save results](save-all-result.json)
and [native exercise](save.FCMacro). Save As and Classic behavior are preserved.

## Hidden line

Coin's native two-pass Hidden line renderer forced BRep triangle polygons into
lines. The viewer now enables real CAD edge nodes. Faces write the depth prepass;
edge nodes skip that prepass to avoid self-occlusion. During the line pass, faces
emit curved silhouettes and marked-face boundaries instead of triangle diagonals.
Topological CAD seams remain real edges. Mesh tessellation display is not rewritten.

Installed native renders verify ordinary and placement geometry, orthographic and
perspective cameras, planar outlines, curved silhouettes, top-view occlusion and
selection outlines. The flat-face interior diagnostic changed from 191 artifact
pixels to zero; 5,202 outline pixels and 5,144 selected-face outline pixels remain.
Placement toggling/Cancel and style changes preserve source appearance, identities
and Undo. Normally opaque placement faces retain the existing 50% transparency floor.

See [before](before-hidden.png), [installed rendering](installed-hidden.png),
[render results](hidden-result.json), and [native exercise](hidden.FCMacro).
The other six styles remain visually consistent: the largest significant raster
difference is 116 of 969,048 pixels (0.012%); Shaded is identical in this fixture.
This is not a claim of pixel identity for every style or a large-model performance
benchmark. See [comparison](style-comparison.json).

## Build, checks and installation

- Full existing native targets FreeCADGui and PartGui built successfully with MSVC;
  [build log](native-build.log) retained. Only the two required binaries and one
  Python toolbar file were installed; unchanged rebuilt dependency outputs were
  not deployed.
- Isolated staged runtime: **49/49** file workflow, placement, toolbar and mesh
  regressions passed. See [staged checks](staged-tests.txt).
- Installed runtime: **14/14** targeted Save As/Save All, Cancel, external-link,
  style-refresh and mesh-import checks passed. See [installed checks](installed-tests.txt).
- Separate installed rendering and four-document Save All exercises also passed.
  They use the actual installed toolbar method and native DLLs, without monkeypatches.
- Three installed hashes match tested artifacts, with rollback copies retained.
  Owner CFG settings are unchanged. The existing shortcut target, working directory,
  arguments and icon were rechecked unchanged. The owner's live documents/session
  were not closed or modified. See [manifest](install-manifest.json).

Restart FreeCAD Plus to load the update. No package/release was published.
Disposable validation profiles, synthetic CAD files and isolated runtime were
removed after archiving evidence; build outputs and rollback files were retained.
An older hidden-line preview DLL hardlink is still locked by the running app and
was left in place; no process was terminated to remove it.
The unrelated untracked project.previewfirst.json remains untouched.
