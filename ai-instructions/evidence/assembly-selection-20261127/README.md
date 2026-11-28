# Assembly visibility, Clone picking and Appearance edges — November 27, 2026

The owner's **implement all** authorizes these three pending previews. No companion
approval state was changed. This delivery does not include the separate pending
multi-part saved active-part bookmark proposal.

## Approved previews

- Revised inline Assembly eyes: `a95f3284527c`, fingerprint
  `a9bb94267c70703f6058d3c11fc509bb138aea014c28a82b3acfbb234e13b310`.
  [Screenshot](approved-assembly-eyes.png). Supersedes the earlier far-left column
  preview; the active assembly has no eye.
- Normal Assembly row text and Clone viewport picks: `84bd54687009`, fingerprint
  `ed14839614d8212112959078b01509b70ddc0175b3fe67d759fffbd235837818`.
  [Screenshot](approved-clone.png).
- Contrasting Appearance boundaries: `f07de651e58c`, fingerprint
  `434f477bffa0be96bd0d88731cfd4f0245033423f8690522409f3fe07c65ca20`.
  [Screenshot](approved-appearance-edges.png).

## Behavior

Assembly eyes follow the native indentation between triangle and component icon.
The active root has no eye; hiding/excluding it is blocked in Components menus.
Previously hidden chosen assemblies are exposed through transient view protection
without rewriting saved settings. Nested child changes belong to their actual
defining parent, including imported files. Condensed groups change atomically with
mixed-state indication and Excluded guards. Native display metadata retains its
existing shared-definition scope. Eye clicks preserve selection, Edit and expansion.

Clone normalizes topology picks to whole direct-child sources, promotes a Body's
current Tip to the Body, and retains exact occurrence placements. Picking works
through isolated definitions and nested Edit routes; duplicate/Shift-removal and
eligibility checks remain intact. Anchored assembly children no longer receive
the grey file-occurrence text style.

Appearance keeps the selected/preselected preference fill and draws only actual
boundary edges with black/white contrast, including hole perimeters. These overlays
do not alter source materials, native picking, document transactions or Undo.

## Verification

Source `s1` exposed two test-harness issues (Qt enum owner and Coin field access),
both corrected. Source `s2` passed 60 of 61 checks; the remaining older test expected
Clone to reject face picks. It now verifies the approved whole-Body normalization.
Source `s3` passed all six focused checks, including a real Qt viewport click without
Browse and the corrected older assertion. Source `s4` passed three additional
checks covering imported nested visibility and selected/hovered perforated-face
outlines. Logs are retained rather than omitting these intermediate failures.

Installed `i1`: **all 63 checks pass**, with zero failures/errors. Coverage includes
native eye/triangle clicks, group Undo, root protection, external defining-parent
transactions, real viewport Clone picking, repeated placements, historical face
appearance, cleanup and existing navigation behavior. Inspected native captures:
[expanded eyes](expanded-eyes.png), [condensed eyes](condensed-eyes.png),
[viewport Clone result](viewport-clone.png), [selected face](appearance-selected-edges.png)
and [hovered face](appearance-hover-edges.png).
The harness uses isolated profiles and disposable fixtures, never owner documents.
To rerun, use the archived harness from the workspace's `approved-ui-validation`
directory; its preference-pack path is relative to that directory. Build/install
paths deliberately identify this Windows installation.
Trailing whitespace in the archived build log is normalized for repository checks.

## Installation

`FreeCADPlusScripts` built successfully. Fourteen Python payloads were installed
with matching source/build/app hashes after the owner saved and closed FreeCAD.
Owner settings and desktop shortcut hashes are unchanged. Exact rollback copies
remain under `validation/approved-ui27/rollback` in the external build root.
See [install manifest](install-manifest.json) and [build result](build-result.json).
