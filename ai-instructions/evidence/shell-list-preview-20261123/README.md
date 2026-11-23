# Shell face-list amendment — November 23, 2026

Native UI prototype, subsequently approved in chat: "implement all previewed changes,
the shell, radius, etc". Production implementation and acceptance are recorded in
[the implementation evidence](../dressup-lists-20261123/README.md). Supersedes session a5461c3ce973's
target-field proposal. Installed baseline is d9304d889b. No production UI, picking,
geometry engine or installation changed in this amendment.

Owner requested a face list only, no target body field and no Select faces/Confirm
Selection toggle. Clicking the list activates picking (blue border); clicking a
parameter deactivates picking while retaining references. Viewport focus does not
end collection. Delete and Remove delete highlighted rows; Clear faces empties the
list. Source geometry is never deleted. Face labels identify the source and face.
The first face implicitly determines the solid; incompatible inputs keep the task
open and preserve valid rows. Clearing the list allows another solid's faces.

The same interaction is recorded for Fillet/Radius and comparable feature collector
migrations. This capture renders Shell only and does not implement those migrations.
Native thickness, mode, join, direction and preview controls remain in place.

Direct screenshots:

- [Empty active face list](shell-empty.png)
- [Selected faces](shell-faces-selected.png)
- [Delete removes one row](shell-delete-row.png)
- [Parameter editing retains selections](shell-parameter-edit.png)
- [Scrolling selection list](shell-scrolling-list.png)
- [Invalid curve](shell-curve-ignored.png)
- [Mixed-solid guidance](shell-other-solid.png)
- [Installed native baseline](baseline-shell-task.png)

The [prototype checks](candidate-result.json) exercise actual QWidget list clicking,
Delete events, Remove/Clear, parameter focus and scrolling. Face picks are simulated
by the harness, and OK is disabled: no shell geometry or production persistence is
claimed. Baseline captures use the installed command with isolated synthetic data.
Owner documents/settings and unrelated project.previewfirst.json are preserved.

Companion session b5a2f4e5bd58, clean adapter baseline
495c56b220fd461f6ce5d71b3b72a0821d8224dc, allowlist shell_ui.py.
Captured fingerprint ef27c6fb9a5baf86123c4470133d0a41971aea50bfbcef140b1337fcd04ee50f.
Preview inspected as fresh and within scope; approval state remains untouched.
Renderer and harness are archived from FreeCAD/shell-entry-preview; candidate-only
UI code is archived here as evidence, not part of the installed application.
