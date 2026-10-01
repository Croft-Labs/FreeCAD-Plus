# Mirror result behavior: owner workflow test

Use this checkout's development executable:
`D:\Temp\Office-PC\freecad-plus-validation-20260928\build\bin\FreeCAD.exe`.
Published installers and the separately installed FreeCAD do not contain this batch.
Evidence: `D:\Temp\Office-PC\freecad-plus-mirror-modes-20260930`.

1. Open `visual\Mirror-Modes.FCStd` and activate Part. The asymmetric Bracket Body
   has a 10 × 6 × 4 mm base and a 3 × 2 × 2 mm notch, volume 228 mm³. It is translated
   and rotated away from the origin.
2. Select Bracket and choose **Part > Mirror**. Select the YZ plane and keep
   **Associative mirror**. OK creates a separate reflected result with a Source link.
   It does not fuse into another body, change Bracket's Tip or hide Bracket.
3. Repeat with **Independent shape snapshot**. The labelled snapshot is a native
   Part::Feature with reflected geometry but no Source or MirrorPlane links. It
   contains no copied feature history. Both modes initially produce the same shape.
4. Change Base.Length to 12 mm and recompute. The associative mirror updates to
   276 mm³; the independent result stays at 228 mm³. Save/reopen and repeat with
   Length 14 mm: the associative volume becomes 324 mm³, the snapshot remains 228 mm³.
5. Undo/Redo snapshot creation: it is one document operation and leaves no temporary
   associative mirror behind. Starting a new Mirror task and Cancel creates nothing.
6. Choose **Use selected reference** with a Part plane. An associative mirror tracks
   later plane movement; a snapshot retains the reflected geometry captured at OK.
   Choosing this mode without a reference keeps the task open with inline guidance.
7. A source needing recompute/repair or a pending edit transaction blocks creation.
   Update/finish the edit and retry. Deleted/replaced source identities require
   Cancel and reselection. Invalid mirror geometry aborts the whole creation transaction;
   correct the plane or sources and retry without accepting partial results.

Snapshot scope: document-root Part shapes and whole Body results. Select the Body,
not its nested feature. Links, Part containers and nested features are rejected in
snapshot mode; use the existing associative mode where supported. Existing native
source/plane coordinate conventions remain. The mode adds no new persistent type or
custom schema: associative results remain Part::Mirroring, snapshots Part::Feature.
Snapshot labels explicitly identify their independent behavior. Creation does not
offer a graphical preview, automatic Boolean fusion or mirrored feature reevaluation.

Whole F057 remains open for broader feature/occurrence workflows, nested snapshots,
target/handedness preview and physical/high-DPI acceptance. Stop here for owner feedback.
