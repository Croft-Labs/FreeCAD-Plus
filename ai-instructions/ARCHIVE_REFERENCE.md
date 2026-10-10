# FreeCAD Plus reference archive

Owner instruction: October 10, 2026. Preserve the existing fork for later/future
reference before preparing a clean official FreeCAD baseline. Archiving is not
approval to carry its implementation choices into that baseline.

## Checkpoint and location

- Preserved checkpoint tag: `archive/freecad-plus-2026-10-10`.
- Archive directory: `C:/Users/GAMING-PC/Documents/__Apps/freecad-archives/freecad-plus-2026-10-10-pre-reset`.
- `freecad-plus-checkout.zip` contains the complete working directory, including
  `.git`, local refs/configuration, initialized submodule repositories and their
  checked-out source, documentation and ignored/untracked files present at capture.
- `manifest.json` records the exact commit, submodule commits, file sizes and
  SHA-256 hashes. `verification.json` and `README.md` beside the archive record
  the completed integrity and restore checks. Use their recorded outcome, not the
  existence of this preparation document, to establish archive completion.
- Archive data stays outside the active checkout and is not committed as a large
  binary to the fork. A published Git tag provides a separate named checkpoint.

## Verification result

Archive completed and restored successfully on October 10, 2026. Checkpoint:
`29496214b34a53fa1d479f35ab5669b41ed4fb18`. All 26,999 source/restored file hashes
match; restored HEAD, clean working tree and all seven recursive submodules pass.
ZIP size: 490,791,599 bytes. SHA-256:
`b3bc602148c1232079fbee95932c5742708d1e3721dcebfeee0cd43d0fade0f5`.
The version of this document inside the ZIP is the pre-capture preparation record;
the external verification files and current WORK_STATE record completion.

## Recovery

1. Check the ZIP SHA-256 against the external verification record.
2. Extract into a new, empty local directory. The ZIP paths start at the checkout
   root and include hidden `.git` data; do not extract over an existing project.
3. Verify file hashes against the manifest, then inspect `git status` and recursive
   submodule status. The restored HEAD must match the manifest checkpoint.
4. Read the specifications through UI_UX_SPEC.md. The unverified-change inventory
   and archived instructions are reference evidence, not automatic implementation
   authorization. Do not run old prompts or recreate the backlog automatically.
5. Restore/build only when needed. Existing build outputs are kept separately;
   copied source is not itself a runnable verified build.

This repository is a partial clone. Its current source and initialized submodule
working trees are included in full, together with all locally present Git data.
Some historical blobs may still require fetching from the recorded remotes.
This ZIP is not advertised as an offline-complete copy of every historical revision.
Local remotes/hooks/configuration are preserved for recovery, not intended for
public distribution or automatic execution in a new project.

## Preserved builds and settings

Existing useful builds remain in `C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds`.
The desktop shortcut and application preferences remain in place. They are not
part of the source ZIP and have not been retargeted or changed by this task.
The separately installed FreeCAD is outside this work.

## Workspace overhead

Generated Python cache directories are ignored as directories, allowing traversal
to skip them. Additional compiler intermediates and accidental in-checkout build,
validation or archive directories are ignored. Tracked source, tests, fixtures,
icons and requirements remain tracked. Actual builds/validation continue to use
the external paths required by AGENTS.md.

Local Git untracked-file caching and a commit graph may be enabled after their
checks succeed; actual results are recorded in WORK_STATE. These improve repository
operations, not FreeCAD rendering. They do not diagnose or fix the reported UI jitter.
Do not broadly ignore source trees or all CAD/document/ZIP files to hide useful data.

The active checkout is retained until its replacement is prepared and verified.
The archive is stored outside it to avoid adding duplicate source to normal project
searches and Git status traversal. No clean clone or feature migration is performed
as part of the archive checkpoint.
