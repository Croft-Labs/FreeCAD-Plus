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
| Configure/build | Root / PowerShell | Windows procedure below; [upstream build workflow](../.github/workflows/sub_buildWindows.yml) | Configuration reached the missing-LibPack gate; successful build unverified. |
| Run focused GUI tests | Built fork / Python console | [Pad test procedure](../tests/PadTaskPanel.md) | Requires the rebuilt application and its copied test modules; not run yet. |
| Broader regression gates | Built fork / upstream CI procedures | [Python tests](../.github/workflows/actions/runPythonTests/action.yml), [C++ tests](../.github/workflows/actions/runCPPTests/runAllTests/action.yml) | Choose relevant cases; no remote workflow dispatch is authorized by these references. |

Windows procedure, not yet validated end-to-end. In a shell with CMake available,
set `FREECAD_LIBPACK_DIR` to the compatible dependency directory first:

```powershell
if (-not $env:FREECAD_LIBPACK_DIR -or -not (Test-Path -LiteralPath $env:FREECAD_LIBPACK_DIR)) {
    throw 'Set FREECAD_LIBPACK_DIR to a compatible LibPack directory first.'
}
$freecadPlusBuild = Join-Path $env:LOCALAPPDATA 'FreeCADPlus\build'
cmake -S . -B $freecadPlusBuild -G 'Visual Studio 17 2022' -A x64 -DBUILD_GUI=ON "-DFREECAD_LIBPACK_DIR=$env:FREECAD_LIBPACK_DIR"
if ($LASTEXITCODE -ne 0) { throw 'FreeCAD Plus configuration failed.' }
cmake --build $freecadPlusBuild --config Release --parallel
```

Identify the resulting executable from the actual build output; do not resolve
an unrelated `FreeCAD` on PATH. Bound build operations by a finite hard deadline
and an inactivity timeout, and inspect progress at least once per minute.

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

The focused test code is [TestPadTaskPanel.py](../src/Mod/PartDesign/PartDesignTests/TestPadTaskPanel.py).
Use [the test procedure](../tests/PadTaskPanel.md); current gaps and the known
test-selector mismatch are tracked only in [milestone 2.2](DEVELOPMENT_ROADMAP.md#pad-validation).

## Release and recovery

No fork release or installer is part of the current task. Local commits do not
imply a push, passing CI, or distribution. Pushes, remote builds, releases, and
upstream submissions require task-specific authorization under the workspace rules.
Use focused commits and non-destructive recovery; preserve unrelated changes.
Any future package must retain upstream attribution and document compatibility.

## Known development issues

- Configuration needs a compatible LibPack even when MSVC/CMake are installed.
  Use the source-owned dependency references above; current status is in milestone 2.2.
- Google Drive is the source location; use the local-output convention above for builds.
- Shared instruction files live outside this Git root. A fresh clone elsewhere
  needs accessible central guidance or an explicit missing-guidance report.
