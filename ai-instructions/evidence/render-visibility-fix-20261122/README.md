# Extrude render and sketch visibility acceptance

Direct native previews were approved in chat before implementation. Before/proposed
screenshots and approval.json retain that evidence separately from installed results.

Installed regression: 107 tests, zero failures/errors. Native invalid-geometry
cases intentionally print errors. Four new cases compare Visibility and
LinkVisibility, exercising new/existing sketches, hidden support/reference inputs,
source/host editing, History clicks, Undo and ordinary native documents.

Installed screenshots use screen capture (including the OpenGL viewport). The
rectangle has unchanged volume 7680 mm^3. The second sketch retains prior visible
sketch/solid and a hidden reference. Fresh-process checks reopen the saved model,
enter the sketch again and verify identical visibility and object identities.
The native edited-sketch overlay remains independent of its ordinary view provider.

Run render_fix_regression.FCMacro and render_fix_visual.FCMacro before
render_fix_reopen.FCMacro, using a disposable PLUS_TEST_DIR and user profile.
No production documents or owner settings were used. Build logs are whitespace
normalized native build transcripts; compiler output was checked live.
