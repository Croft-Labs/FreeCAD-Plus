param(
    [Parameter(Mandatory=$true)][string]$CMake,
    [Parameter(Mandatory=$true)][string]$BuildDirectory,
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [switch]$ScriptsOnly,
    [switch]$AssemblyConsumer
)
$ErrorActionPreference = 'Stop'
if (Test-Path -LiteralPath $OutputDirectory) { throw 'Use a new build evidence directory.' }
New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
$targets = @('FreeCADApp', 'FreeCADGui', 'FreeCADGui_Resources', 'PartDesignGui', 'SketcherGui', 'PartScripts')
if ($ScriptsOnly) { $targets = @('FreeCADGui_Resources', 'PartScripts') }
if ($AssemblyConsumer) { $targets += @('AssemblyGui', 'AssemblyTests') }
$showTarget = Test-Path -LiteralPath (Join-Path $BuildDirectory 'src/Mod/Show/Show.vcxproj')
if ($showTarget) { $targets += 'Show' }
$argsList = @('--build', ('"' + $BuildDirectory + '"'), '--config', 'Release', '--target') + $targets + @('--parallel', '3')
$process = Start-Process -FilePath $CMake -ArgumentList $argsList -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput "$OutputDirectory\build.log" `
    -RedirectStandardError "$OutputDirectory\build-errors.log"
$processHandle = $process.Handle
$deadline = (Get-Date).AddMinutes(30)
$lastProgress = Get-Date
$lastLength = 0
while (-not $process.WaitForExit(1000)) {
    $length = (Get-Item "$OutputDirectory\build.log").Length + (Get-Item "$OutputDirectory\build-errors.log").Length
    if ($length -ne $lastLength) { $lastProgress = Get-Date; $lastLength = $length }
    if ((Get-Date) -gt $deadline -or ((Get-Date) - $lastProgress).TotalSeconds -gt 300) {
        Stop-Process -Id $process.Id
        throw 'Build exceeded deadline or five minutes without output; inspect child build processes before retrying.'
    }
}
@{exit_code=$process.ExitCode; build=$BuildDirectory} | ConvertTo-Json |
    Set-Content "$OutputDirectory\build-result.json"
if ($process.ExitCode -ne 0) { throw "Build failed: $($process.ExitCode)." }
if (-not $showTarget) {
    # This validation configuration disables BUILD_SHOW. Native Sketcher still
    # imports its Python visibility helpers; stage those without a native rebuild.
    $showSource = Join-Path (Split-Path -Parent $PSScriptRoot) 'src/Mod/Show'
    $showDestination = Join-Path $BuildDirectory 'Mod/Show'
    foreach ($folder in @('', 'SceneDetails')) {
        $sourceFolder = if ($folder) { Join-Path $showSource $folder } else { $showSource }
        $destinationFolder = if ($folder) { Join-Path $showDestination $folder } else { $showDestination }
        New-Item -ItemType Directory -Path $destinationFolder -Force | Out-Null
        Get-ChildItem -LiteralPath $sourceFolder -Filter '*.py' -File | ForEach-Object {
            Copy-Item -LiteralPath $_.FullName -Destination $destinationFolder
        }
    }
}
Write-Output "Build passed. Evidence: $OutputDirectory"
