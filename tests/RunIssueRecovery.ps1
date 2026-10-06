param(
    [Parameter(Mandatory=$true)][string]$Executable,
    [Parameter(Mandatory=$true)][string]$OutputDirectory
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '../tools/FreeCADArtifactPaths.ps1')
$OutputDirectory = Resolve-FreeCADArtifactPath -Path $OutputDirectory
if (Test-Path -LiteralPath $OutputDirectory) { throw 'Use a new, empty evidence directory.' }
New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
$OutputDirectory = (Resolve-Path -LiteralPath $OutputDirectory).Path
$env:FREECAD_PLUS_VALIDATION_DIR = $OutputDirectory
$env:FREECAD_PLUS_SOURCE = Split-Path -Parent $PSScriptRoot
$env:FREECAD_USER_HOME = $OutputDirectory
$env:FREECAD_USER_DATA = $OutputDirectory
$env:FREECAD_USER_TEMP = $OutputDirectory
$env:TEMP = $env:TMP = $OutputDirectory
$env:PYTHONDONTWRITEBYTECODE = '1'
foreach ($phase in @('prepare', 'verify')) {
    $env:FREECAD_PLUS_RECOVERY_PHASE = $phase
    $launchArgs = @('--user-cfg', ('"' + $OutputDirectory + '\user.cfg"'),
                    '--system-cfg', ('"' + $OutputDirectory + '\system.cfg"'))
    if ($phase -eq 'prepare') {
        $launchArgs += @('--hidden', ('"' + $PSScriptRoot + '\ValidateIssueRecovery.FCMacro"'))
    }
    # --hidden skips native crash recovery, so verify uses the ordinary event loop.
    $process = Start-Process -FilePath $Executable -ArgumentList $launchArgs -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput "$OutputDirectory\$phase-stdout.log" `
        -RedirectStandardError "$OutputDirectory\$phase-stderr.log"
    $processHandle = $process.Handle
    $deadline = (Get-Date).AddSeconds(120)
    while (-not $process.WaitForExit(1000)) {
        if ((Get-Date) -gt $deadline) {
            Stop-Process -Id $process.Id
            throw "Recovery $phase exceeded 120 seconds."
        }
    }
    if ($process.ExitCode -ne 0) { throw "Recovery $phase exited $($process.ExitCode)." }
    if ($phase -eq 'prepare' -and -not (Test-Path "$OutputDirectory\prepared.json")) {
        throw 'Recovery preparation did not finish.'
    }
}
$result = Get-Content "$OutputDirectory\recovery-results.json" -Raw | ConvertFrom-Json
if (-not $result.passed) { throw "Recovery validation failed: $($result.error)" }
Write-Output "PASS: five recovery fixtures; evidence in $OutputDirectory"
