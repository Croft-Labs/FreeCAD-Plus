$ErrorActionPreference = 'Stop'
$taskRuntime = 'C:\Users\dgium\Documents\__Apps\_temp builds\FreeCAD-Plus'
$taskOutput = Join-Path $taskRuntime 'validation\selection-button-repair-20261123'
$taskProfile = Join-Path $taskOutput 'profile-shortcut'
$taskShortcutPath = 'C:\Users\dgium\Desktop\freecad plus 0.1.0.lnk'
$taskShortcut = (New-Object -ComObject WScript.Shell).CreateShortcut($taskShortcutPath)
if ($taskShortcut.TargetPath -ne (Join-Path $taskRuntime 'Launch FreeCAD Plus.bat') -or
    $taskShortcut.WorkingDirectory -ne $taskRuntime -or $taskShortcut.Arguments) {
    throw 'The existing desktop shortcut target changed; inspect before launching.'
}
New-Item -ItemType Directory -Force -Path (Join-Path $taskProfile 'data') | Out-Null
Copy-Item -LiteralPath (Join-Path $taskOutput 'profile-installed\user.cfg') -Destination (Join-Path $taskProfile 'user.cfg')
$env:PLUS_TEST_DIR = $taskOutput
$env:FREECAD_USER_DATA = Join-Path $taskProfile 'data'
$env:PYTHONDONTWRITEBYTECODE = '1'
$taskArgs = '-u "{0}" -s "{1}" "{2}"' -f (Join-Path $taskProfile 'user.cfg'),
    (Join-Path $taskProfile 'system.cfg'), (Join-Path $PSScriptRoot 'shortcut.FCMacro')
Start-Process -FilePath $taskShortcutPath -ArgumentList $taskArgs -WorkingDirectory $taskRuntime -WindowStyle Hidden
$taskShortcut | Select-Object TargetPath, Arguments, WorkingDirectory | ConvertTo-Json |
    Set-Content -LiteralPath (Join-Path $taskOutput 'shortcut-target.json')
