$runtime = 'C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus'
$run = Join-Path $runtime 'validation/selection-controls-preview-20261123/interactive'
$profile = Join-Path $run 'profile'
New-Item -ItemType Directory -Force "$profile/data" | Out-Null
if (-not (Test-Path "$profile/user.cfg")) {
    $repo = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
    Copy-Item (Join-Path $repo 'src/Gui/PreferencePacks/FreeCAD Light/FreeCAD Light.cfg') "$profile/user.cfg"
}
$env:FREECAD_USER_HOME = $profile
$env:FREECAD_USER_DATA = "$profile/data"
$env:FREECAD_USER_TEMP = $profile
$env:PLUS_PREVIEW_WORKTREE = 'C:/Users/dgium/Documents/__Apps/_temp builds/app-render-companion/sessions/c81b636d7ce5/candidate'
$env:PLUS_PREVIEW_OUT = $run
$env:PLUS_PREVIEW_IMAGE = "$run/preview.png"
$env:PLUS_PREVIEW_INTERACTIVE = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$macro = Join-Path $PSScriptRoot 'scene.FCMacro'
$process = Start-Process -FilePath "$runtime/app/bin/FreeCAD.exe" -ArgumentList @('-u', ('"' + "$profile/user.cfg" + '"'), '-s', ('"' + "$profile/system.cfg" + '"'), ('"' + $macro + '"')) -WindowStyle Hidden -PassThru
$process.Id | Set-Content "$run/process-id.txt"
Write-Output "Interactive prototype process: $($process.Id)"
