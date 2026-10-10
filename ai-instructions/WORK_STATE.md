# FreeCAD Plus: Current work state

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
Temporary staging is removed after checks. No compilation, runtime test,
owner build, release or shortcut/settings change is claimed. Existing external
builds still run the archived fork.

## Recovery references

Verified source archive and restoration evidence: [ARCHIVE_REFERENCE.md](ARCHIVE_REFERENCE.md).
Previous fork final main: b3d8a0a2fe532ca1693132eac5ab24a2bd1651c2.
Archive tag: archive/freecad-plus-2026-10-10, checkpoint
29496214b34a53fa1d479f35ab5669b41ed4fb18.
The old main history remains available; no force-push or history replacement is used.
