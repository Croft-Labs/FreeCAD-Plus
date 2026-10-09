param(
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [string]$ColdFixtureDirectory,
    [switch]$IterationSmoke,
    [switch]$PanelSmoke,
    [switch]$SelectionSmoke,
    [switch]$ReferenceSmoke,
    [switch]$HistorySmoke,
    [switch]$InstanceSmoke,
    [switch]$ConversionSmoke,
    [switch]$RecoverySmoke,
    [switch]$ExternalizationSmoke,
    [switch]$EditContextSmoke,
    [switch]$TaskContextSmoke,
    [switch]$SaveRoutingSmoke,
    [switch]$UndoRoutingSmoke,
    [switch]$DisplayContextSmoke,
    [switch]$BomSmoke,
    [switch]$AddComponentSmoke,
    [switch]$LocalNameSmoke,
    [switch]$CurveProfileSmoke,
    [switch]$BackgroundResultSmoke,
    [switch]$ModelsPaneSmoke,
    [switch]$FeedbackSmoke,
    [switch]$IntegrationSmoke,
    [switch]$CoreSmoke,
    [switch]$AssemblyStructureSmoke,
    [switch]$TreeMoveSmoke,
    [switch]$PaneInteractions,
    [switch]$PaneLayoutSmoke,
    [switch]$StartActionsSmoke,
    [switch]$RecentFilesSmoke,
    [switch]$StatusControlsSmoke,
    [switch]$SketchWorkflow,
    [switch]$SketchRegression,
    [switch]$SketchSolver,
    [string]$SketchColdFixtureDirectory,
    [string]$TestNames,
    [string]$TestFiles,
    [switch]$RibbonSmoke,
    [switch]$DetachedLauncher,
    [ValidateSet('Bootstrap','Plus','Classic')][string]$RibbonStartupPhase,
    [ValidateRange(30,600)][int]$TimeoutSeconds = 180
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '../tools/FreeCADArtifactPaths.ps1')
$OutputDirectory = Resolve-FreeCADArtifactPath -Path $OutputDirectory
if (Test-Path -LiteralPath $OutputDirectory) { throw 'Use a new evidence directory.' }
$Executable = (Resolve-Path -LiteralPath $Executable).Path
New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
$OutputDirectory = (Resolve-Path -LiteralPath $OutputDirectory).Path
$env:FREECAD_PLUS_VALIDATION_DIR = $OutputDirectory
$env:FREECAD_PLUS_SOURCE = Split-Path -Parent $PSScriptRoot
$env:FREECAD_USER_HOME = $OutputDirectory
$env:FREECAD_USER_DATA = $OutputDirectory
$env:FREECAD_USER_TEMP = $OutputDirectory
$env:TEMP = $env:TMP = $OutputDirectory
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentDocument.py'
$env:FREECAD_PLUS_TEST_NAMES = $TestNames
$env:FREECAD_PLUS_VERIFY_PAYLOAD = '0'
if ($IterationSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentIteration.py' }
if ($PanelSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentPanelIteration.py' }
if ($SelectionSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentSelectionIteration.py' }
if ($ReferenceSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentReferenceRecovery.py' }
if ($HistorySmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentHistoryIteration.py' }
if ($InstanceSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentInstanceIteration.py' }
if ($ConversionSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentConversionIteration.py' }
if ($RecoverySmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentFileRecovery.py' }
if ($ExternalizationSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentExternalization.py' }
if ($EditContextSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentEditContext.py' }
if ($TaskContextSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentTaskContext.py' }
if ($SaveRoutingSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentSaveRouting.py' }
if ($UndoRoutingSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentUndoRouting.py' }
if ($DisplayContextSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentDisplayContext.py' }
if ($BomSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentBom.py' }
if ($AddComponentSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentAddCommand.py' }
if ($LocalNameSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentLocalNames.py' }
if ($CurveProfileSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentCurveProfile.py' }
if ($BackgroundResultSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentBackgroundResult.py' }
if ($ModelsPaneSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentModelsPane.py' }
if ($FeedbackSmoke) {
    $env:FREECAD_PLUS_PROFILE_SOURCE = '0'
    $env:FREECAD_PLUS_VERIFY_PAYLOAD = '1'
    $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentLocalNames.py,tests/TestComponentAddCommand.py,tests/TestComponentCurveProfile.py,tests/TestComponentBackgroundResult.py,tests/TestComponentModelsPane.py,tests/TestComponentPanelIteration.py,tests/TestComponentTaskContext.py,tests/TestComponentSelectionIteration.py'
}
if ($IntegrationSmoke) {
    $env:FREECAD_PLUS_PROFILE_SOURCE = '0'
    $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentDisplayContext.py,tests/TestComponentEditContext.py,tests/TestComponentExternalization.py,tests/TestComponentFileRecovery.py,tests/TestComponentReferenceRecovery.py,tests/TestComponentSaveRouting.py,tests/TestComponentUndoRouting.py,tests/TestComponentBom.py'
}
if ($CoreSmoke) {
    $env:FREECAD_PLUS_PROFILE_SOURCE = '0'
    $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentDocument.py,tests/TestComponentIteration.py,tests/TestComponentHistoryIteration.py,tests/TestComponentInstanceIteration.py,tests/TestComponentConversionIteration.py'
}
if ($AssemblyStructureSmoke) {
    $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentModelsPane.py,tests/TestComponentPanelIteration.py,tests/TestComponentSelectionIteration.py,tests/TestComponentEditContext.py,tests/TestComponentTaskContext.py,tests/TestComponentSaveRouting.py,tests/TestComponentUndoRouting.py,tests/TestComponentDisplayContext.py,tests/TestComponentBom.py,tests/TestComponentExternalization.py,tests/TestComponentFileRecovery.py,tests/TestComponentAddCommand.py'
}
if ($TreeMoveSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentTreeMove.py' }
if ($PaneLayoutSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentPaneLayout.py' }
if ($StartActionsSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentStartActions.py' }
if ($RecentFilesSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentRecentFiles.py' }
if ($StatusControlsSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestPlusStatusControls.py' }
if ($PaneInteractions) {
    $env:FREECAD_PLUS_PROFILE_SOURCE = '0'
    $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentPaneInteractions.py'
}
if ($SketchWorkflow) {
    $env:FREECAD_PLUS_PROFILE_SOURCE = '0'
    $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentSketchWorkflow.py'
}
if ($SketchRegression) {
    $env:FREECAD_PLUS_PROFILE_SOURCE = '0'
    $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentPanelIteration.py,tests/TestComponentTaskContext.py,tests/TestSketchFreedom.py,tests/TestSketchSupportCommand.py,tests/TestSketchRepairReview.py,tests/TestConstraintRepair.py,tests/TestSketchReuse.py,tests/TestTrimGesture.py'
}
if ($SketchSolver) {
    $env:FREECAD_PLUS_PROFILE_SOURCE = '0'
    $env:FREECAD_PLUS_ISSUE_TESTS = 'src/Mod/Sketcher/SketcherTests/TestSketcherSolver.py'
}
if ($SketchColdFixtureDirectory) {
    $env:FREECAD_PLUS_PROFILE_SOURCE = '0'
    $env:FREECAD_PLUS_SKETCH_FIXTURES = (Resolve-Path -LiteralPath $SketchColdFixtureDirectory).Path
    $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentSketchCold.py'
}
if ($RibbonSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestPlusRibbon.py' }
if ($RibbonStartupPhase) {
    $env:FREECAD_PLUS_RIBBON_PHASE = $RibbonStartupPhase
    $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestPlusRibbonStartup.py'
}
if ($ColdFixtureDirectory) {
    $env:FREECAD_PLUS_COMPONENT_FIXTURES = (Resolve-Path -LiteralPath $ColdFixtureDirectory).Path
    $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestInstalledComponentDocument.py'
}
if ($TestFiles) { $env:FREECAD_PLUS_ISSUE_TESTS = $TestFiles }
$userConfig = if ($RibbonStartupPhase) { Join-Path (Split-Path -Parent $OutputDirectory) 'ribbon-user.cfg' } else { Join-Path $OutputDirectory 'user.cfg' }
$launchArgs = @('--hidden', '--user-cfg', ('"' + $userConfig + '"'),
    '--system-cfg', ('"' + $OutputDirectory + '\system.cfg"'),
    ('"' + $PSScriptRoot + '\ValidateUpstreamIssues.FCMacro"'))
$process = Start-Process -FilePath $Executable -ArgumentList $launchArgs -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput "$OutputDirectory\stdout.log" `
    -RedirectStandardError "$OutputDirectory\stderr.log"
$processHandle = $process.Handle
$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
$lastProgress = Get-Date
$lastCpu = 0
while (-not $process.WaitForExit(1000)) {
    $process.Refresh()
    $cpu = $process.TotalProcessorTime.TotalSeconds
    if ($cpu -ne $lastCpu) { $lastProgress = Get-Date; $lastCpu = $cpu }
    # The launcher waits while its native child runs; its CPU can stay idle.
    $latestLog = Get-ChildItem -LiteralPath $OutputDirectory -Filter *.log |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latestLog -and $latestLog.LastWriteTime -gt $lastProgress) {
        $lastProgress = $latestLog.LastWriteTime
    }
    if ((Get-Date) -gt $deadline -or ((Get-Date) - $lastProgress).TotalSeconds -gt 60) {
        # Stop only native children of this timed-out test launcher.
        Get-CimInstance Win32_Process -Filter "ParentProcessId = $($process.Id)" |
            Where-Object { $_.Name -eq 'FreeCAD.exe' -and
                $_.CommandLine.Contains($OutputDirectory + '\user.cfg') } |
            ForEach-Object { Stop-Process -Id $_.ProcessId -ErrorAction SilentlyContinue }
        Stop-Process -Id $process.Id -ErrorAction SilentlyContinue
        throw 'Component validation exceeded its bounded deadline.'
    }
}
if ($DetachedLauncher -and $process.ExitCode -eq 0) {
    # FreeCADPlus.exe launches the native child and returns immediately. Wait for
    # the macro's completion marker rather than treating launcher exit as GUI exit.
    while (-not (Test-Path -LiteralPath "$OutputDirectory\validation.done")) {
        if ((Get-Date) -gt $deadline) {
            throw 'Detached owner launcher validation exceeded its bounded deadline.'
        }
        Start-Sleep -Milliseconds 500
    }
}
@{executable=$Executable; exit_code=$process.ExitCode} | ConvertTo-Json |
    Set-Content "$OutputDirectory\process-result.json"
if ($process.ExitCode -ne 0) { throw "FreeCAD exited $($process.ExitCode)." }
$result = Get-Content "$OutputDirectory\results.json" -Raw | ConvertFrom-Json
$diagnostics = @(Select-String -LiteralPath "$OutputDirectory\stderr.log" -Pattern @(
    'Unhandled (Base::Exception|std::exception) caught in GUIApplication::notify',
    'AttributeError: .*__Workbench__',
    'libshiboken: Internal C\+\+ object .*already deleted') | ForEach-Object { $_.Line })
$result | Add-Member -NotePropertyName unexpected_gui_diagnostics -NotePropertyValue $diagnostics -Force
if ($diagnostics.Count) { $result.passed = $false }
$result | ConvertTo-Json -Depth 30 | Set-Content "$OutputDirectory\results.json"
if (-not $result.passed) {
    Set-Content "$OutputDirectory\validation.done" 'FAIL'
    throw 'Component validation failed; see results.json.'
}
Write-Output "PASS: $($result.tests_run) component checks; evidence in $OutputDirectory"
