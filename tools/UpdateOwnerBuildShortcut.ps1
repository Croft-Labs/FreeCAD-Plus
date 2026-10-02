param([Parameter(Mandatory=$true)][string]$Executable)
$ErrorActionPreference = 'Stop'
$taskLauncher = (Resolve-Path -LiteralPath $Executable).Path
if ([IO.Path]::GetFileName($taskLauncher) -ne 'FreeCADPlus.exe') {
    throw 'Owner shortcut must target the FreeCAD Plus launcher.'
}
$taskShortcut = Join-Path ([Environment]::GetFolderPath('Desktop')) 'FreeCADPlus.exe - Shortcut.lnk'
if (-not (Test-Path -LiteralPath $taskShortcut -PathType Leaf)) {
    throw "Existing owner shortcut not found: $taskShortcut"
}
$taskShell = New-Object -ComObject WScript.Shell
$taskLink = $taskShell.CreateShortcut($taskShortcut)
$taskLink.TargetPath = $taskLauncher
$taskLink.WorkingDirectory = Split-Path -Parent $taskLauncher
$taskLink.Save()
$taskVerified = $taskShell.CreateShortcut($taskShortcut)
if ($taskVerified.TargetPath -ne $taskLauncher -or
    $taskVerified.WorkingDirectory -ne (Split-Path -Parent $taskLauncher)) {
    throw 'Saved shortcut target/working directory verification failed.'
}
@{shortcut=$taskShortcut; target=$taskVerified.TargetPath;
  working_directory=$taskVerified.WorkingDirectory; verified=$true} | ConvertTo-Json
