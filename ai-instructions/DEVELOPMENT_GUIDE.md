# FreeCAD Plus: Development Guide

## Prerequisites and setup

Work from the FreeCAD Plus checkout with recursive submodules initialized.
`origin` is `Croft-Labs/FreeCAD-Plus`; `upstream` is `FreeCAD/FreeCAD`.
Inspect current remotes and status before commits or authorized pushes.

For Windows, use the source-defined CMake/MSVC configuration and a compatible
LibPack. The [LibPack workflow](../.github/workflows/actions/windows/getLibpack/action.yml)
owns the current bundle reference; [build options](../cMake/FreeCAD_Helpers/InitializeFreeCADBuildOptions.cmake)
own configuration requirements. [CMakeLists.txt](../CMakeLists.txt),
[pixi.toml](../pixi.toml), and [pixi.lock](../pixi.lock) own tool/dependency requirements.
Do not substitute libraries from the separately installed FreeCAD.

Keep dependency bundles and generated build output outside the Google Drive
source tree. A suitable local build location is `$env:LOCALAPPDATA\FreeCADPlus\build`;
choose and record a compatible LibPack directory before configuring. Default
CMake presets place output inside the source tree, so override their build path.
These locations are a development convention, not evidence of an existing build.

Ignore the separately installed FreeCAD: do not modify it, launch it to validate
this fork, or use its behavior as proof that these source changes work.

## Commands

Commands below use PowerShell from the repository root unless stated otherwise.
Resolve executable paths in the current environment; tool availability and
successful execution are separate facts.

| Purpose | Working directory / shell | Command or authoritative procedure | Prerequisites and evidence |
| --- | --- | --- | --- |
| Inspect work and remotes | Root / PowerShell | `git status --short --branch`; `git remote -v` | Verified during setup and documentation adoption. |
| Inspect submodules | Root / PowerShell | `git submodule status --recursive` | Verified during clone setup. |
| Initialize submodules | Root / PowerShell | `git submodule update --init --recursive` | Requires network access and permission to write Git metadata. |
| C++ style | Root / PowerShell | `clang-format --dry-run --Werror src/Mod/PartDesign/Gui/TaskPadParameters.cpp src/Mod/PartDesign/Gui/TaskPadParameters.h src/Mod/PartDesign/Gui/TaskExtrudeParameters.h` | Formatting checked with clang-format 19.1.5; repository hooks specify their own version. |
| Python syntax | Root / PowerShell | `python -c "import ast,pathlib; ast.parse(pathlib.Path('src/Mod/PartDesign/PartDesignTests/TestPadTaskPanel.py').read_text())"` | Syntax checked; does not import or execute FreeCAD. |
| Whitespace | Root / PowerShell | `git -c core.whitespace=cr-at-eol diff --check` | Accommodates existing tracked CRLF files without normalizing unrelated lines. |
| Configure/build | Root / PowerShell | Windows procedure below; [upstream build workflow](../.github/workflows/sub_buildWindows.yml) | Focused native targets built; [results](DEVELOPMENT_ROADMAP.md#extrude-validation-evidence). |
| Run focused GUI tests | Built fork / Python console | [Pad test procedure](../tests/PadTaskPanel.md) | Requires the rebuilt application and matching copied test modules; [results](DEVELOPMENT_ROADMAP.md#extrude-validation-evidence). |
| Run Pattern regressions | Built fork / Python console or FreeCADCmd | [Pattern test procedure](../tests/PatternTaskPanel.md) | Requires rebuilt PartDesign App/Gui and matching test modules; results belong to roadmap 3.7. |
| Broader regression gates | Built fork / upstream CI procedures | [Python tests](../.github/workflows/actions/runPythonTests/action.yml), [C++ tests](../.github/workflows/actions/runCPPTests/runAllTests/action.yml) | Choose relevant cases; no remote workflow dispatch is authorized by these references. |

Focused Windows configuration for the Extrude and Pattern workflows. In a shell with CMake
available, set `FREECAD_LIBPACK_DIR` to the source-pinned LibPack directory first.
This omits unrelated workbenches and the C++ developer test framework; Python
model and GUI regressions remain available:

```powershell
if (-not $env:FREECAD_LIBPACK_DIR -or -not (Test-Path -LiteralPath $env:FREECAD_LIBPACK_DIR)) {
    throw 'Set FREECAD_LIBPACK_DIR to a compatible LibPack directory first.'
}
$freecadPlusBuild = Join-Path $env:LOCALAPPDATA 'FreeCADPlus\build'
$freecadPlusOptions = @(
    '-DBUILD_GUI=ON', '-DBUILD_PART=ON', '-DBUILD_SKETCHER=ON', '-DBUILD_PART_DESIGN=ON',
    '-DFREECAD_RELEASE_PDB=OFF', '-DENABLE_DEVELOPER_TESTS=OFF',
    '-DFREECAD_COPY_DEPEND_DIRS_TO_BUILD=ON', '-DFREECAD_COPY_LIBPACK_BIN_TO_BUILD=ON',
    '-DFREECAD_COPY_PLUGINS_BIN_TO_BUILD=ON', '-DFREECAD_3DCONNEXION_SUPPORT=None'
)
$unusedWorkbenches = @(
    'FEM', 'ADDONMGR', 'BIM', 'DRAFT', 'HELP', 'IMPORT', 'INSPECTION', 'MESH_PART',
    'FLAT_MESH', 'OPENSCAD', 'CAM', 'ASSEMBLY', 'PLOT', 'POINTS', 'REVERSEENGINEERING',
    'ROBOT', 'SHOW', 'SPREADSHEET', 'START', 'TECHDRAW', 'TUX', 'WEB', 'SURFACE'
)
$freecadPlusOptions += $unusedWorkbenches | ForEach-Object { "-DBUILD_$_=OFF" }
cmake -S . -B $freecadPlusBuild -G 'Visual Studio 17 2022' -A x64 "-DFREECAD_LIBPACK_DIR=$env:FREECAD_LIBPACK_DIR" @freecadPlusOptions
if ($LASTEXITCODE -ne 0) { throw 'FreeCAD Plus configuration failed.' }
cmake --build $freecadPlusBuild --config Release --parallel 3
if ($LASTEXITCODE -ne 0) { throw 'FreeCAD Plus build failed.' }
```

Identify the resulting executable from the actual build output; do not resolve
an unrelated `FreeCAD` on PATH. Bound build operations by a finite hard deadline
and an inactivity timeout, and inspect progress at least once per minute.
Keep MSBuild file tracking enabled for normal incremental builds. The validation
rebuild with `TrackFileAccess=false` recompiled dependencies. If only a
C++ implementation file changes and all dependencies are already built, MSBuild's
`ClCompile` target with `SelectedFiles` can compile that file, then `PrepareForBuild;_Link`
can relink its project with `BuildProjectReferences=false`. This assumes unchanged
headers/generated files and all required objects/resources exist; missing resources
must also be compiled. Do not treat a compiler-only exit code as a completed build.

## Development conventions

- Reuse the shared task/selection/transaction classes indexed in
  [the programming summary](PROGRAMMING_SUMMARY.md#common-code-and-libraries).
- Preserve `PartDesign::Pad`, `Profile`, other persisted identifiers, existing
  geometry semantics, and upstream module boundaries. Brand naming is not a schema migration.
- Keep public text translatable and retain unit/expression handling.
- Follow [formatter configuration](../.clang-format), [pre-commit configuration](../.pre-commit-config.yaml),
  [contribution guidance](../CONTRIBUTING.md), and [AI disclosure policy](../AI_POLICY.md).
  Upstream PR submission requirements do not constitute authorization to submit one.
- Preserve file line endings and avoid unrelated formatting. Keep dependencies
  and generated output out of source edits. Do not modify submodules incidentally.
- Put durable task status in the roadmap and screen behavior in the UI specification.

## Validation

Source formatting, syntax, build success, passing GUI tests, visual acceptance,
and published artifacts are separate evidence levels. For this native GUI change,
run tests in the actual rebuilt fork and manually verify model selection and
preview behavior. Check Pocket when shared extrusion code changes.

Run the five suites in [the test procedure](../tests/PadTaskPanel.md) against matching
source-built modules. The GUI must have initialized document views. The fixtures
reopen through `ViewObject.doubleClicked()` to include the user edit transaction;
calling `Gui.Document.setEdit()` directly is not equivalent for Cancel/Undo tests.
Results and remaining manual checks are owned by [milestone 2.2](DEVELOPMENT_ROADMAP.md#pad-validation).

Changes to `TaskPadPocketParameters.ui` require Qt autogen followed by recompiling
both `TaskExtrudeParameters.cpp` and `TaskPadParameters.cpp`, which consume the
generated header, then linking PartDesignGui. Replacing a widget requires updating
both consumers. The start-offset/reversal regressions live in the existing
`TestExtrudeTaskPanel` suite; native geometry assertions and saved-file checks run
inside the built GUI. Their procedure is in [start-offset tests](../tests/PadTaskPanel.md#start-offset-and-direction-buttons).

For Revolution/Groove angular controls, regenerate Qt autogen and compile
`TaskRevolutionParameters.cpp`, the consumer of `TaskRevolutionParameters.ui`,
then link PartDesignGui. Run [the Revolve task tests](../tests/RevolveTaskPanel.md)
against the matching GUI module. For curved-solid bounds after GUI rendering,
use `Shape.optimalBoundingBox(False)` to avoid display-triangulation approximations;
retain exact volume and bidirectional shape-difference assertions.

For Trim Body, install the new `BOPTools/TrimAPI.py`, `TrimFeatures.py`, `TrimGui.py`,
and `TrimBody.svg` through Part's CMake script list. Update both workbench InitGui
scripts and rebuild/link the PartGui and PartDesignGui Workbench.cpp entries.
The existing Part/BOPTools geometry kernel is reused; no new dependency is needed.
Run [Trim Body model and GUI regressions](../tests/TrimBody.md), followed by the
existing task suites to check selection, transaction, and scene-graph cleanup.
The model suite is also registered with TestPartApp; GUI tests with TestPartGui.
Keep source and runtime test files synchronized. A main executable's older About
stamp does not identify the incrementally rebuilt GUI modules.

Trim results are `Part::FeaturePython` objects linked to original inputs. The hidden
PlacementSupport links trigger recomputation for moved parent containers. Validate
links before geometry execution and clear stale Shape on failure. Cancel must abort
the transaction before GUI resetEdit, which otherwise commits the pending edit.
New saved results need these Python modules for recomputation in another installation.

## Release and recovery

No fork release or installer is part of the current task. Local commits do not
imply a push, passing CI, or distribution. Pushes, remote builds, releases, and
upstream submissions require task-specific authorization under the workspace rules.
Use focused commits and non-destructive recovery; preserve unrelated changes.
Any future package must retain upstream attribution and document compatibility.

## Known development issues

- Configuration needs a compatible LibPack even when MSVC/CMake are installed.
  Use the source-owned dependency references above; tested setup is recorded in 2.2.
- Set `FREECAD_USER_HOME`, `FREECAD_USER_DATA`, and `FREECAD_USER_TEMP` to existing
  isolated directories and pass separate `--user-cfg` / `--system-cfg` files for
  automated runs. Startup still creates a standard versioned cache directory;
  this required authorized filesystem access in the validation sandbox.
- MSBuild warns about incremental builds under the system temporary directory
  (MSB8029). Prefer the stable local build directory shown above for ongoing work.
- Google Drive is the source location; use the local-output convention above for builds.
- Shared instruction files live outside this Git root. A fresh clone elsewhere
  needs accessible central guidance or an explicit missing-guidance report.
