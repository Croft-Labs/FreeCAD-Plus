# Native Part file Edit guards

Build PartGui before running TestComponentNativeModelingGuards. It exercises 46
registered modeling commands with geometry selected while the file is active,
checking disabled availability and refusal without object, visibility, undo or
transaction changes. Other cases check missing active-part fallback, explicit
component activation with native Box creation/Undo, legacy Box behavior and native
geometry inspection availability. Run the native Part routing and shared file
command suites alongside it. Guard coverage is limited to Command.cpp,
CommandSimple.cpp and CommandParametric.cpp; this is not feature/history migration
or a workbench-wide solver/command compatibility claim.
