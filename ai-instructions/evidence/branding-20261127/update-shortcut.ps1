$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\dgium\Documents\__Apps\_temp builds\FreeCAD-Plus'
$taskDesktop = [Environment]::GetFolderPath('Desktop')
$taskOld = Join-Path $taskDesktop 'freecad plus 0.1.0.lnk'
$taskNew = Join-Path $taskDesktop 'FreeCAD Plus 2.0.0.lnk'
$taskBackup = Join-Path $taskRoot 'validation\branding27\rollback\freecad plus 0.1.0.lnk'
$taskShell = New-Object -ComObject WScript.Shell
if (!(Test-Path -LiteralPath $taskOld)) { throw 'Expected development shortcut is missing.' }
if (Test-Path -LiteralPath $taskNew) { throw 'New shortcut already exists; inspect it before replacing.' }
$taskLink = $taskShell.CreateShortcut($taskOld)
$taskExpected = Join-Path $taskRoot 'Launch FreeCAD Plus.bat'
if ($taskLink.TargetPath -ne $taskExpected) { throw 'Unexpected launcher; preserve this shortcut.' }
$taskBefore = [ordered]@{TargetPath=$taskLink.TargetPath;Arguments=$taskLink.Arguments;WorkingDirectory=$taskLink.WorkingDirectory;IconLocation=$taskLink.IconLocation}
Copy-Item -LiteralPath $taskOld -Destination $taskBackup
Copy-Item -LiteralPath $taskOld -Destination $taskNew
$taskLink = $taskShell.CreateShortcut($taskNew)
$taskLink.Description = 'FreeCAD Plus 2.0.0'
$taskLink.Save()
$taskLink = $taskShell.CreateShortcut($taskNew)
foreach ($taskKey in $taskBefore.Keys) {
    if ($taskLink.$taskKey -ne $taskBefore[$taskKey]) { throw "Shortcut changed protected field $taskKey" }
}
# Only remove this exact old shortcut after the replacement has been checked.
if ((Split-Path ([IO.Path]::GetFullPath($taskOld))) -ne $taskDesktop) { throw 'Desktop path check failed.' }
Remove-Item -LiteralPath $taskOld
[ordered]@{Old=$taskOld;New=$taskNew;Properties=$taskBefore;Description=$taskLink.Description} |
    ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $taskRoot 'validation\branding27\shortcut.json')
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class PlusBrandingShell {
    [DllImport("shell32.dll")] public static extern void SHChangeNotify(uint eventId, uint flags, IntPtr item1, IntPtr item2);
}
'@
[PlusBrandingShell]::SHChangeNotify(0x08000000,0,[IntPtr]::Zero,[IntPtr]::Zero)
Write-Output 'Verified FreeCAD Plus 2.0.0 shortcut; launcher, arguments, working directory and icon preserved.'
