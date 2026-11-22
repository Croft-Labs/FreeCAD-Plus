# Extrude visibility and shared tree controls

The owner approved the native storyboard directly in chat; `approval.json` records
the candidate fingerprint. `approved-*.png` are staged previews, not implementation
verification. `installed-*.png` are native captures of the installed implementation.

Run `run-validation.py regression --installed --broad`, then `visual --installed`
and `reopen --installed` using the development runtime's `build/bin/python.exe`.
Each launches a fresh native process with explicit isolated user/system settings.
The regression runner loads test code from the repository; the product modules
remain loaded from the installed app (paths recorded in the results).
No tests use the owner profile. Run GUI checks sequentially to preserve focus.

`install.py` copies checked build files with hash verification and retains original
files under the runtime's `validation/extrude-visibility-20261122/install-backup`.
The install manifest records source/build/app hashes and rollback paths.
The native Gui build log records the NoModify appearance-notification fix.

The tests cover initial filtering without revealing hidden eligible objects,
edit isolation, real History clicks and explicit visibility undo, shared native
task transactions, target field focus and preference color, material restoration,
save during a preview, external source/host ownership, manual preview timing,
planar solid/sheet face input and saved associations. Visual checks additionally
pick a target through the actual native viewport and exercise the installed eye.

The fresh-process reopen check updates a saved sheet face and verifies recompute,
then checks existing sketch Extrudes, downstream features and external sources.
`shortcut.FCMacro` verifies the existing desktop shortcut's installed modules and
explicit isolated config/data paths; it leaves the restarted application open.

Native Pad still requires planar profile faces. Bare solid edges, datum planes,
axes and points are not Extrude profiles. Optional direction/start/end references
retain their existing selection rules and may be shown with the tree eyes.
