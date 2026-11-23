# Sketch dimension single Enter preview - November 23, 2026

Requested: one Enter after typing a dimensional constraint value applies it and
closes the dialog. The shared numeric_fields.NumericCommitFilter currently consumes
Enter and moves focus. The native-widget baseline reproduces this with plain 25.
QuantitySpinBox also has a separate normalization path for arithmetic expressions.

Proposed: main Enter and keypad Enter accept a valid dimension once, including
creation/editing and length/radius/diameter/angle. Retain native units, expressions,
invalid-input validation, Cancel/Escape, name/reference controls and layout. Other
numeric task fields retain their blur/arrow behavior. Intended implementation scope
is numeric_fields.py and, only if needed, Sketcher EditDatumDialog.cpp, with focused
native regression tests. No production code or installed payload changed yet.

[Current behavior after one Enter](baseline.png) and
[proposed one-press completion](proposed.png) are UI-only simulations using the
native InsertDatum widgets. The displayed sketch width is mocked; no solver or
constraint persistence has been implemented or validated by this preview.

Companion session: e494680daf44. Adapter baseline:
a5f23b50a3db8c50312a8726646a287b52f69763. Fingerprint:
9bb46843f4a61f0648d7d6c78affaa18ede84fba99b56fc518f15d14bf8bfac1.
Allowed candidate file: dimension_ui.py. Capture is valid, violations empty;
explicit owner preview approval is pending. Approval state has not been modified.
The earlier ad69ed082ec7 session was abandoned after embedded Python generated
bytecode in its baseline; the fresh renderer disables bytecode before importing.
