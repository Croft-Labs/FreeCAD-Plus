# File Edit command guards

Run TestComponentFileCommands in this fork's native runtime with source GUI
modules loaded consistently. It checks file refusal for Extrude, Revolve, Loft,
Pipe, Helix, Primitive, Sketch and Plane launchers; explicit file destination
refusal before task context creation; datum availability following Edit rather
than selection; ordinary component sketch/plane launch and cancel; and occurrence
movement under the file with Undo/Redo and no file-owned modeling history.
Native assembly joints and remaining native command routes are a separate gate
in roadmap 7.8.13e2. These tests do not establish that broader compatibility.
