# FreeCAD Plus: Current work state

## Clean FreeCAD 1.1.4 baseline

Owner requested the clean latest stable source in the existing fork on October 10,
2026. Official releases/latest resolves to 1.1.4; 26.3rc1 is separately labeled a
release candidate. Selected official commit:
4fd3bf320d9566a27e60069fc8387448aaa3a094.

Local branch: codex/freecad-1.1.4-baseline. Source checkout and release-pinned
submodules are present. Original tracked source matched the official tag before
the documentation/ignore overlay. Four stable submodules replace the previous
seven recursive modules. Old dependency/cache remnants were removed only after
3,740 files in 45 directories matched the verified source archive.

Preserved the five UI specifications, source evidence, original documents/icons,
unverified-change inventory and archive reference. Historical implementation
records now live under archive/pre-restart-docs. Active source links in the review
inventory point to the immutable old-fork commit, not similarly named stock files.
No owner requirement has been approved or rejected by this transition.

Integrity checks pass: all original application source matches upstream 1.1.4;
all four pinned submodules are clean; requirement wording in the five specifications
is unchanged apart from evidence-link destinations; 664 historical documents/assets
are byte-preserved. Active documentation links/icons and staged whitespace pass.
Published baseline commit f608ea07afffa1ed3a426b09d207b59bf4e8bfd7 to
origin/codex/freecad-1.1.4-baseline and verified the remote hash. GitHub default
branch and local origin/HEAD now point to this baseline. Old main and the archive
tag remain intact. A final documentation commit records this completed handoff.
Committed archival blob hashes also match all 664 preserved documents/assets.
Temporary source staging was removed after checks. The subsequent runtime check
below uses the official binary; this checkout has not been compiled locally.

## Stable baseline inventory and light runtime check — October 10, 2026

**Result: provenance, source integrity and core functionality pass. Local viewport
visual acceptance remains open. Do not describe this as an entirely verified GUI
baseline or as an owner-ready Plus build.** No application source was changed.

### External release evidence

- [Official FreeCAD 1.1.4 release](https://github.com/FreeCAD/FreeCAD/releases/tag/1.1.4):
  published September 28, 2026; neither draft nor prerelease. The latest-stable
  endpoint selected this release; 26.3 RC1 is a prerelease.
- Release commit `4fd3bf320d9566a27e60069fc8387448aaa3a094` has successful upstream
  [Build Release](https://github.com/FreeCAD/FreeCAD/actions/runs/36432494038) and
  [FreeCAD master CI](https://github.com/FreeCAD/FreeCAD/actions/runs/36431033844)
  workflow runs. This is publisher release/CI evidence, not an independent
  certification of this PC or a guarantee of every operation.
- Original source, workbench definitions, build files and tests still match
  `upstream-1.1.4`. Only the instruction/documentation/ignore overlay differs.
  All four release-pinned submodules are clean.

### Local package inventory

The tested executable is a fresh official portable package on this PC, separate
from older Plus builds and any separately installed FreeCAD. It reports exactly
this checkout's source commit. It is not a locally compiled fork binary.

| Item | Observed value |
| --- | --- |
| Package | `FreeCAD_1.1.4-Windows-x86_64-py311.7z`, 418,088,341 bytes |
| Package SHA256 | `4828741fc91ee37fafcdb97a1abacb18b04ba451ac4372d9ff7a7349b36f4d6d`, matches publisher release digest |
| Executable SHA256 | `7b38c5d5aa2c74f830539c1c5c44cbf6e3e8e157292c718f9ee24ac6d3e12cf6` |
| Windows signature | Valid; The FreeCAD project association AISBL |
| FreeCAD runtime | 1.1.4, revision `20260928 (Git shallow)`, commit `4fd3bf320d9566a27e60069fc8387448aaa3a094` |
| Python / Qt / Open CASCADE | 3.11.14 / 6.8.3 / 7.8.1 |
| Payload after checks | 35,589 files; 2,307,887,823 bytes, including runtime-created caches |
| Local source build | Not configured or compiled; cached 26.3 LibPack is not assumed compatible with 1.1.4 |

Payload directory:
`C:/Users/GAMING-PC/Documents/_temp/freecad/test-builds/freecad_1.1.4_official_baseline/FreeCAD_1.1.4-Windows-x86_64-py311`.
Executable: `bin/freecad.exe` beneath it. The verified download is retained under
`test-builds/dependencies/FreeCAD-1.1.4-official` for reproducible extraction.
Both are useful baseline dependencies, not superseded builds.

All 19 registered workbenches activated successfully: Assembly, BIM, CAM, Draft,
FEM, Inspection, Material, Mesh, OpenSCAD, Part Design, Part, Points, Reverse
Engineering, Robot, Sketcher, Spreadsheet, Surface, TechDraw and Test Framework.
`NoneWorkbench` is additionally registered as the empty workbench.

The package contains 30 module directories: AddonManager, Assembly, BIM, CAM,
Draft, Fem, Help, Idf, Import, Inspection, Material, Measure, Mesh, MeshPart,
OpenSCAD, Part, PartDesign, Plot, Points, ReverseEngineering, Robot, Show, Sketcher,
Spreadsheet, Start, Surface, TechDraw, Test, Tux and Web. Module directories are
not all selectable workbenches: upstream MeshPart does not register its own
workbench, and Start is a command. No Plus workbench filtering was applied.

### Local checks and limits

Checks used the actual GUI executable's Python/Qt APIs with temporary
`FREECAD_USER_HOME`, `FREECAD_USER_DATA`, `FREECAD_USER_TEMP`, user and system
configuration paths. Existing owner preferences and addons were not used.

| Check | Result |
| --- | --- |
| GUI startup, runtime identity and workbench activation | Pass; all 19 registered workbenches loaded |
| Sketch solver and Pad | Pass; constrained 20 x 10 mm rectangle padded 5 mm produced a valid 1,000 mm3 solid |
| Recompute, Undo and Redo | Pass; Pad length 5 -> 8 mm changed volume 1,000 -> 1,600 mm3; Undo and Redo restored both states |
| Pocket | Pass; radius 2 mm, depth 3 mm produced a valid 1,562.300888 mm3 solid |
| Spreadsheet expression and native Link | Pass; cell-driven pocket depth updated model and linked instance; 30 mm instance offset retained |
| Part Boolean | Pass; box/cylinder cut produced a valid solid with expected volume |
| STEP and STL | Pass; STEP export/reimport preserved volume; STL reopened as a solid mesh with 124 facets |
| FCStd persistence | Pass; 15-object model, expression and link survived save/reopen and separate-process restart; subsequent edits recomputed correctly |
| Model image export | Pass; visually inspected image shows both solid instances and their circular pockets correctly |
| Event processing and process exit | Pass; timed Qt callbacks and view switching completed; successful primary and cold runs exited normally with code 0 |
| Visible viewport / jitter acceptance | **Open**; widget and native framebuffer captures showed stippling/colored artifacts; see below |

The primary run passed 10 automated check groups and the fresh-process run passed
four, including repeated startup/render/event-loop checks. Successful capture calls
alone do **not** establish correct visible rendering. The primary run took about
30 seconds, the cold run about 12; these include initialization and test delays,
and are not startup benchmarks. No exhaustive suite, complex real-world assembly,
CAM machining, FEM solver, long-duration interaction or manual jitter comparison
was performed.

Initial automation waited at BIM's normal welcome dialog. Only the task-owned
process was stopped; BIM `FirstTime=false` in the temporary profile allowed the
check to finish. A later capture-only harness used an unavailable compatibility
import; correcting it to PySide6 allowed that probe to finish. Neither interruption
is counted as an application crash.

OpenSCAD's workbench loaded, but reported its external OpenSCAD executable was
not found. Operations requiring that program are not verified or ready. Other
external solvers/toolchains were not validated.

### Remaining display gate and next action

Offscreen model export is correct, while QWidget and native QOpenGLWidget
framebuffer captures show artifacts. A separate run without image export still
showed artifacts in its framebuffer capture. Desktop-region captures were occluded
and cannot establish FreeCAD's visible result. Native window inspection through
the computer-use runtime could not initialize. The cause remains unresolved:
capture/readback versus on-screen graphics behavior has not been distinguished,
and the old fork's reported jitter has not been shown fixed.

Before UI reimplementation, inspect this exact official payload's visible viewport
with an isolated profile and a simple solid: rotate/zoom, switch workbenches and
resize the window. If artifacts occur on screen, investigate the renderer/driver
and relevant FreeCAD settings in a temporary profile before changing source.
No driver, global graphics setting or application-code workaround was applied.

The existing desktop `FreeCADPlus.exe - Shortcut.lnk` still targets
`test-builds/freecad_plus_2026-10-10_part_types_payload/FreeCADPlus.exe`, with that
payload as its working directory. It launches the archived fork, not this baseline.
The official package is retained for baseline verification; no new owner build,
shortcut delivery or release is claimed. Temporary macros, test profiles, models,
logs and captures are removed after recording this durable result.

## Recovery references

Verified source archive and restoration evidence: [ARCHIVE_REFERENCE.md](ARCHIVE_REFERENCE.md).
Previous fork final main: b3d8a0a2fe532ca1693132eac5ab24a2bd1651c2.
Archive tag: archive/freecad-plus-2026-10-10, checkpoint
29496214b34a53fa1d479f35ab5669b41ed4fb18.
The old main history remains available; no force-push or history replacement is used.
