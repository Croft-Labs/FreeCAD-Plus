param(
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$Fixture,
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [ValidateRange(30,600)][int]$TimeoutSeconds = 120
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '../tools/FreeCADArtifactPaths.ps1')
$OutputDirectory = Resolve-FreeCADArtifactPath -Path $OutputDirectory
if (Test-Path -LiteralPath $OutputDirectory) { throw 'Use a new evidence directory.' }
$Fixture = (Resolve-Path -LiteralPath $Fixture).Path
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
$env:FREECAD_PLUS_26300_FIXTURE = $Fixture
$env:FREECAD_PLUS_ISSUE_TESTS = 'tests/TestIssue26300Fixture.py'
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
$report = @{ executable=$Executable; fixture=$Fixture; timeout_seconds=$TimeoutSeconds }
while (-not $process.WaitForExit(1000)) {
    $process.Refresh()
    $cpu = $process.TotalProcessorTime.TotalSeconds
    if ($cpu -ne $lastCpu) { $lastProgress = Get-Date; $lastCpu = $cpu }
    if ((Get-Date) -gt $deadline -or ((Get-Date) - $lastProgress).TotalSeconds -gt 60) {
        Stop-Process -Id $process.Id
        $report.status = 'TIMEOUT'
        $report.cpu_seconds = $cpu
        $report | ConvertTo-Json | Set-Content "$OutputDirectory\process-result.json"
        throw 'Freeform reproduction exceeded its deadline or 60 seconds without CPU progress. See freeform-stack.log.'
    }
}
$report.status = 'EXITED'
$report.exit_code = $process.ExitCode
$report | ConvertTo-Json | Set-Content "$OutputDirectory\process-result.json"
if ($process.ExitCode -ne 0) { throw "FreeCAD exited $($process.ExitCode)." }
$result = Get-Content "$OutputDirectory\results.json" -Raw | ConvertFrom-Json
if (-not $result.passed) { throw 'Freeform regression failed; see results.json.' }
Write-Output "PASS: freeform generation; evidence in $OutputDirectory"
