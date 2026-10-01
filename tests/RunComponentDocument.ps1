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
    [ValidateRange(30,600)][int]$TimeoutSeconds = 180
)
$ErrorActionPreference = 'Stop'
if (Test-Path -LiteralPath $OutputDirectory) { throw 'Use a new evidence directory.' }
$Executable = (Resolve-Path -LiteralPath $Executable).Path
New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
$OutputDirectory = (Resolve-Path -LiteralPath $OutputDirectory).Path
$env:FREECAD_PLUS_VALIDATION_DIR = $OutputDirectory
$env:FREECAD_PLUS_SOURCE = Split-Path -Parent $PSScriptRoot
$env:FREECAD_USER_HOME = $OutputDirectory
$env:FREECAD_USER_DATA = $OutputDirectory
$env:FREECAD_USER_TEMP = $OutputDirectory
$env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentDocument.py'
if ($IterationSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentIteration.py' }
if ($PanelSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentPanelIteration.py' }
if ($SelectionSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentSelectionIteration.py' }
if ($ReferenceSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentReferenceRecovery.py' }
if ($HistorySmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentHistoryIteration.py' }
if ($InstanceSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentInstanceIteration.py' }
if ($ConversionSmoke) { $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestComponentConversionIteration.py' }
if ($ColdFixtureDirectory) {
    $env:FREECAD_PLUS_COMPONENT_FIXTURES = (Resolve-Path -LiteralPath $ColdFixtureDirectory).Path
    $env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestInstalledComponentDocument.py'
}
$launchArgs = @('--hidden', '--user-cfg', ('"' + $OutputDirectory + '\user.cfg"'),
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
    if ((Get-Date) -gt $deadline -or ((Get-Date) - $lastProgress).TotalSeconds -gt 60) {
        Stop-Process -Id $process.Id
        throw 'Component validation exceeded its bounded deadline.'
    }
}
@{executable=$Executable; exit_code=$process.ExitCode} | ConvertTo-Json |
    Set-Content "$OutputDirectory\process-result.json"
if ($process.ExitCode -ne 0) { throw "FreeCAD exited $($process.ExitCode)." }
$result = Get-Content "$OutputDirectory\results.json" -Raw | ConvertFrom-Json
if (-not $result.passed) { throw 'Component validation failed; see results.json.' }
Write-Output "PASS: $($result.tests_run) component checks; evidence in $OutputDirectory"
