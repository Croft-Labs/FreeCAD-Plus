# FreeCAD Plus 2.0.0 — installed November 27, 2026

The existing development application now identifies as **FreeCAD Plus 2.0.0**.
The Desktop shortcut is **FreeCAD Plus 2.0.0.lnk**, with its original launcher,
arguments, working directory and outlined Plus icon retained. Owner CFG hashes
are unchanged. Relaunch an older running instance to load the native update.

## Approval and result

Owner requests: rename the window/taskbar product, use version 2.0.0 throughout
current product displays, and replace remaining Classic product logos. The owner
approved the [direct preview](proposed.png) with “implement changes.” The
[before capture](before.png) and canonical approval record are linked from
[Default settings](../../ui-ux-specs/DEFAULT_SETTINGS.md#freecad-plus-200-branding--november-27-2026).
The component edit-modes preview remains a separate pending proposal.

Native GUI/embedded startup, About and splash use the Plus identity. Legacy icon,
document-icon, About and all 28 splash resource aliases resolve to the approved
Plus assets. Windows icon resources, installer artwork, Linux icons/desktop
metadata and macOS icons are updated; unrelated command/service icons and
contributor/license credits remain intact. Native binary/module names, app-data
paths, model schema and historical source identifiers remain unchanged.

The central version feeds runtime and CLI reporting. Windows numeric versions
are 2.0.0.0 and display versions are 2.0.0. Resource strings explicitly use the
product's major/minor/patch values: a dependency overwrote generic PACKAGE_VERSION
with 2.13.3 during configuration. Linux release metadata uses the same explicit
components. Packaging display names are separate from executable/registry names.
Download settings retain their former Qt settings key after the display rename.

## Verification and limits

- MSVC native FreeCADMain, FreeCADMainCmd, FreeCADMainPy and FreeCADGuiPy targets
  built successfully. [Final build log](native-build.log).
- Staged native file/navigation regressions: **32/32** passed.
  [Tests](staged-tests.txt), [branding checks](staged-result.json).
- Installed native file/navigation regressions: **32/32** passed.
  [Tests](installed-tests.txt), [initial installed checks](installed-result.json).
- Final GUI-only correction removes an unnecessary explicit Qt display-name
  setter that appended a duplicate product name to the OS caption. The corrected
  native Windows caption is exactly **FreeCAD Plus 2.0.0**. Final installed
  branding and **5/5** navigation checks pass: [result](final-result.json),
  [tests](final-tests.txt). [Native About](installed-about.png),
  [compiled splash asset](installed-splash.png).
- Actual command-line output and both Windows executable properties agree:
  [version evidence](windows-version.json). The taskbar uses the verified native
  caption/product metadata; no separate Explorer taskbar screenshot was captured.
- Seven installed binary hashes match tested build output, with rollback copies:
  [initial manifest](install-manifest.json), [final manifest](install-title-manifest.json).
  [Shortcut verification](shortcut.json). No owner model was opened or changed.
- The first build-runtime suite used stale build-directory Python modules;
  FreeCADPlusScripts refreshed them from the current checkout. A module-level
  loader also picked up imported legacy TestComponentPanel cases. Three retain
  superseded expectations (automatic History switching, no default active tree,
  duplicate component naming) and fail in [legacy results](legacy-tests.txt).
  They were not changed or counted in the passing, explicitly selected classes.
- Installer/macOS/Linux source assets and metadata are updated, but no NSIS,
  macOS or Linux package was built or published. Existing Classic Windows file
  associations were not rewritten. Branch/source history and dependency versions
  are accurate provenance, not product-version labels to replace.

The saved native About/splash SVGs match the approved candidate exactly. The
installed application embeds those resources; no runtime Python branding patch
or owner-profile override is used. Scoped sources and durable evidence are
committed/pushed under standing authorization. Unrelated project.previewfirst.json
is untouched. External rollback binaries remain under validation/branding27.
