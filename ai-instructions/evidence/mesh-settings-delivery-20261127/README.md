# Approved mesh settings and remaining workflow delivery

November 27, 2026. The owner approved implementation of the revised preview and
the remaining named workflows. This delivers companion `d4c51081992f`, fingerprint
`9d8ab7aba64810496bc49188588e2c0cbf9e35a94dd5ae3d3e9aab7e175bd003`.
Chat approval is authoritative; no tool approval state was changed on the owner's behalf.

## Delivered behavior

- Mesh From Shape has one mixed list, no picker modes, and exact solids/sheets/faces.
  Whole-source coverage removes duplicate face coverage. One Apply creates one
  component-owned mesh History feature; its native source geometry remains.
- Standard starts with linear/angular deviation. Advanced uses mesher radio buttons
  and model defaults; main fields follow the chosen model. Native quantity controls
  retain units. Advanced OK applies and saves defaults; Cancel restores the draft.
  Main edits affect the current recipe. Apply clears inputs and restores saved defaults.
- Saved meshes reopen their own recipe through History, without overwriting defaults.
  Native control names/types/ranges are checked. Executable paths are user preferences,
  never trusted from a CAD document. Existing older numeric recipes are accepted.
- History edit explicitly reopens Mesh, Transform and Trim creation tasks. Transform
  editing accepts omitted optional settings using the same defaults as its evaluator.
- The last active part and exact occurrence/isolation context are saved in document
  metadata and restored on opening. Invalid/missing identities use the established
  one-part or file-level fallback. Native Save and saving a background file are covered.
  Hidden imports and live file-level Edit preserve their current context.

The earlier [approved batch](../approved-workflows-20261127/README.md) already installed
unified linked intersections, whole-shape transformations, clone appearance inheritance,
Trim Body, top file tabs and scoped plane visibility. This delivery verifies those
workflows again, including clicks on all four actual Modeling ribbon buttons.

## Real installed screenshots

- [Mesh main panel](mesh-main.png)
- [Advanced model/defaults dialog](mesh-advanced.png)

These are native working task widgets captured from the installed app, not simulations.

## Verification and installation

`FreeCADPlusScripts` built successfully. The exact staged application passed all
48 tests; the installed application passed the same 48 tests. These cover mixed
mesh creation, defaults, Cancel, Apply/reset, saved recipe reopening, colors,
ownership, recompute, linked intersections and native viewport picking, all four
transformation commands and actual ribbon clicks, trim validity/editing, whole/per-face
clone appearance, active-part save/restore, hidden imports and one-part fallback.
See [staged tests](stage-tests.txt) and [installed tests](installed-tests.txt).

Initial focused checks exposed a missing optional pattern setting on edit and a test
click before native command-state refresh. Both are corrected. The first broader
run had two old no-bookmark expectations; those fixtures now explicitly enter
file-level Edit, preserving fallback coverage alongside new persistence tests.

Eleven Python payloads were installed atomically after confirming the owner app was
closed. [Source/build/app hashes](verified-hashes.json) all agree. Owner profile and
desktop shortcut hashes are unchanged. Rollback copies remain outside the checkout.
Native libraries are unchanged from the earlier approved batch. Tests used isolated
profiles and generated fixture documents, never owner documents.

Standard and Mefisto generation pass. Netgen still has the recorded upstream/native
failure on this runtime; failure leaves the document unchanged. This UI work does
not repair that engine. Gmsh settings and missing-executable failure are covered;
successful external Gmsh generation remains unverified.

Implementation commit: `4ebb42f48d`. Documentation/evidence is a separate commit.
Both are pushed to the configured origin fork only after checking this evidence.
Remote verification is recorded in the delivery response; this document alone
is not proof of publication.
