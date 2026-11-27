# Reference image — installed November 27, 2026

The owner approved the native preview and requested a simpler attachment control:
fundamental or created plane plus distance offset, without a plane-definition
workflow. Preview `ee78e7210c21`, fingerprint
`e76eca3a7e7831ef4b95d5e5adde47dca1f5b1ed49f255ff2c72446a5441a5a6`, was checked fresh
before implementation. Approval was supplied in chat; companion approval state was
not altered. [Approved preview](approved-preview.png).

## Delivered behavior

Design Tasks > Create Geometry > Reference image opens the active component's task.
The dropdown lists fundamental XY/XZ/YZ planes and existing created planes. Offset
is measured along the support normal; attached rotation stays in its plane.
Free placement exposes XYZ position and rotations. Rotation displays two decimals
and steps by 0.01 degrees. Width/height, aspect lock, two-point calibration, nine
anchor presets, a picked image anchor, transparency and temporary preview work.
Changing anchors does not move the image; resizing/rotation keep the anchor fixed.

Done commits and closes. Apply commits and resets fields/lists for another image.
Cancel discards only unapplied edits. History double-click and Edit reference image
reopen the populated task; Hide/Show and Delete use defining-file Undo. Images work
in imported component occurrences and independent native component copies.

[Installed task](reference-task.png) · [Native preview](reference-preview.png) ·
[History](reference-history.png). These are captures of installed functionality.

## Persistence and ownership

Component schema 9 admits component-owned `Image::ImagePlane`. Existing supported
schemas 1–8 still open; accepting an image in an older file upgrades that defining
file inside the same Undo transaction. Older Plus builds reject schema 9, rather
than misreading its new owned content. No owner file was opened or migrated here.

`ImageFile` uses native `PropertyFileIncluded`, so the image survives source-file
removal and save/reopen. Native `Part::AttachExtensionPython`, `ObjectXY`, and
`AttachmentOffset` provide associative recomputation; no Python geometry proxy or
global document observer implements saved attachment. `PlusImageVersion=1` and
`ImageSettings` preserve normalized anchor, position, Euler angles, flip/aspect and
anchor mode. Free rotations compose Z/Y/X. Plane dependencies participate in native
History order; missing plane references remain repairable through the task.

Task previews use separate Coin geometry and a temporary texture. They do not create
document objects or write image placement/materials. Editing masks only the saved
image's render switch, restored on completion or Cancel. Context and revision guards
reject stale commits. Imported edits are owned by the defining source document.

## Verification

- `p1`: native attachment follows an existing plane and survives reopen.
- `s1`–`s3`: found and corrected Qt tuple lookup, native Coin matrix setup, marker
  coordinates, and a test assertion reading the destroyed form after Done.
- `s4`: 65 broader checks, with one image fixture name collision and three older
  plane-test failures. The fixture now uses distinct component names.
- `s5`: all 14 image tests pass, including real orthographic/perspective mouse
  picking, all anchors, calibration, schema/Undo, embedded reopen, imported editing,
  independent export, missing-plane repair, stale context, Apply/reset and Cancel.
- `s6`: actual History Edit/Hide/Show/Delete menu and Undo pass.
- `b1`: all three older plane-test failures reproduce on the unchanged installed
  baseline: duplicate component name fixture and two outdated click-toggle checks.
  No plane implementation was changed by this task.
- Native `PartDesignGui` and `FreeCADPlusScripts` builds pass. Final build log is
  captured after all build processes completed and a sequential refresh completed.
- `i1`: **45/45 installed checks pass** in 45.598 seconds: 15 image tests, native
  idle task-list behavior, mesh import and Appearance/History regressions. Stderr
  is empty. The image is launched by its actual native Tasks action in this run.

Nine Python files and `app/lib/PartDesignGui.pyd` were installed with rollback
copies. Source/build/installed payload hashes match; protected owner profile and
shortcut hashes are unchanged. `FreeCAD Plus 2.0.0.lnk` still targets the existing
`Launch FreeCAD Plus.bat`, with empty arguments and the existing build root as its
working directory. See [manifest](install-manifest.json) and
[verification](verification.json). No app or user document was running at installation.

The checked harnesses, results and screenshots are archived here. Disposable native
test directories are removed after archival; rollback/build/installation evidence
remain in the external `validation/reference-image27` directory.

## Publication

Completed source, tests, specifications and this evidence are committed together
and pushed to the standing authorized fork branch. Remote HEAD is verified after
push; no release or upstream publication is part of this change.
