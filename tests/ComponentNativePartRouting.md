# Native Part command routing

Build PartGui before running TestComponentNativePartRouting. Source Python overlays
alone cannot validate this native dispatch. The suite invokes Part_Primitives,
Part_Extrude, Part_Revolve, Part_Loft and Part_Sweep through Gui.runCommand and
verifies shared-task invocation, file refusal without mutation, and domestic task
opening/cancellation. The legacy Primitive dialog remains native. Expected file
refusals are printed by the native command exception handler; they must not open
legacy dialogs or create objects. Run TestComponentFileCommands alongside it.
This does not qualify other Part commands or native assembly joint ownership.
