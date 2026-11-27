# Reference image View button — November 27, 2026

The owner requested a View-tab reference-image button and approved the native
preview in chat ("Approved"). Review `538a9d553ad1`, fingerprint
`02fc3bd91759ecaa39d77ca7146af58a82f657627d0ea44bac6c0fc3f6965648`, was valid
with no isolation violations. No companion approval state was changed.

The installed toolbar matches the approved candidate apart from line endings.
A large Reference image button in View > Reference reuses `Plus_ReferenceImage`,
including its native icon, task, active-component resolution and eligibility.

- [Approved native screenshot](approved-preview.png)
- [Installed native screenshot](installed-view-tab.png)
- [Installed smoke result](result.json)
- [Install manifest](install-manifest.json)
- [Build result](build-result.json)

`FreeCADPlusScripts` built successfully. Only `freecad_plus/toolbars.py` was
installed. Source, built and installed hashes match; owner profile/shortcut hashes
are unchanged. The rollback copy remains under the build root's
`validation/view-image-button-installed27/rollback`.

An isolated installed FreeCAD process clicked the actual QToolButton, opened the
existing reference-image task for the expected component, and verified Cancel
preserved object count and Undo count. After closing the component document the
command was inactive. The installed screenshot was inspected. The smoke harness
is retained here; the broader reference-image workflow was already validated in
the preceding delivery and was not changed.

Publication: committed with this change on `codex/freecad-1.1.4-baseline`; the
push and remote SHA are verified at delivery.
