# Recent Files thumbnails and white icon outline — November 26, 2026

Owner authorization: **"both approved. implement"** after the thumbnail diagnosis
and direct icon comparison. The [icon specification](../../ui-ux-specs/TOOLBARS_AND_BUTTONS.md#freecad-plus-application-and-file-icon--november-26-2026)
records the exact preview identity and approval; [approved artwork](approved-outline.png).
The original untracked `project.previewfirst.json` remains untouched.

## Recent Files thumbnails

`DisplayedFilesModel::addFile` now sends both `fcstd` and `cadprt` suffixes through
the existing embedded-thumbnail reader. Lowercasing already makes this work for
uppercase extensions. Previously `.cadprt` took the external F3D route, which
returned no preview, leaving the system file icon. The existing archive contents,
card layout/order/click action, Classic behavior and missing-preview fallback are
unchanged. There is no file-format migration or owner-document resave.

Native regression reproduces the omission on the prior installed app for both
`.cadprt` and `.CADPRT`: [baseline result](baseline-corrected-result.json) and
[test output](baseline-corrected-tests.txt). The additional expected icon assertion
also fails against the old resource. An initial harness assertion used a nonexistent
document API; it was corrected to the existing `document.validate` before this
baseline and all acceptance runs.

The updated installed app passes **6/6** focused tests: exact embedded PNG bytes
for both Plus suffix cases, Classic thumbnail preservation, painted fallback for
missing thumbnails/macros, unchanged source files/order, exact approved icon
resources and real mouse-click opening of a Plus card.
[Results](installed-result.json), [tests](installed-tests.txt),
[real native Start page with disposable documents](installed-recent-files.png).

## Icon outline

The installed SVG exactly matches the approved candidate. A white underlay follows
the original silhouette, using the same effective stroke width as the plus sign;
one-unit viewBox padding prevents clipping. Original colored paths and the green
plus group are unchanged. The generated Windows ICO contains ten transparent PNG
frames from 16 through 256 pixels. Executable resources and the GUI SVG resource
were rebuilt. Classic artwork and associations remain intact.

Existing icon/file workflow regressions pass **30/30** in the updated app:
[results](regression-result.json), [tests](regression-tests.txt).
[Installed native app/executable/file icons](installed-icons.png) show the actual
resource/provider outputs, not a design mockup.

## Existing shortcut and owner documents

Launching through the existing `freecad plus 0.1.0.lnk` passes **10/10** checks:
the six focused checks, three Windows icon/association checks, and a read-only
check of all four owner Recent Files entries. Every model image role exactly
matches its archived PNG; all four document hashes and the owner configuration
hash remain unchanged. [Shortcut results](shortcut-result.json),
[tests](shortcut-tests.txt), [owner preservation result](owner-check.json).
Private owner filenames/artwork were not copied into Git evidence.

One of the four owner archives contains a uniform, blank saved PNG. The corrected
loader faithfully displays that blank preview; regenerating its saved view is a
separate document action. The other three show saved model images. No owner file
was opened or saved by this read-only check.

The [shortcut target, working directory and icon reference](shortcut.json) are
unchanged. Windows received its standard association/icon refresh notification.

## Build and installation

The existing native Windows Release build passes: [build log](build.log).
Nine native/resource payload files were installed into the existing owner app;
all installed hashes match the build/source [manifest](install-manifest.json).
Rollback copies use `.before-thumbnails-outline-20261126`. Running old processes
retain their loaded resources until restart; no owner process was terminated.

[Final checks](final-checks.json) verify exact approved SVG bytes, preserved original
artwork/plus groups, decoded transparent ICO frames and all nine installed hashes.
Source diff checks pass with CR-at-EOL permitted, preserving existing C++ CRLF
line endings. [Harnesses](helpers) retain build/install/regression provenance.
Task-generated validation profiles/fixtures were removed after archiving results;
useful build trees, installed payload and rollback files remain.

Completed source/evidence changes are committed and pushed to the configured
origin fork under standing authorization. This is not an upstream push or release.
