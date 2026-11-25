<# Register the Plus-only file type for the current user. Classic associations
   and protected Windows UserChoice entries are never rewritten. #>
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$Executable,
    [string]$Icon,
    [string]$UserConfig,
    [Parameter(Mandatory=$true)][string]$BackupFile
)
$ErrorActionPreference = 'Stop'
$Executable = (Resolve-Path -LiteralPath $Executable).Path
if (-not $Icon) { $Icon = Join-Path (Split-Path $Executable) 'FreeCADPlus.ico' }
$Icon = (Resolve-Path -LiteralPath $Icon).Path
if ($UserConfig) { $UserConfig = (Resolve-Path -LiteralPath $UserConfig).Path }
$progId = 'FreeCADPlus.Document'
$choicePath = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.cadprt\UserChoice'
if (Test-Path -LiteralPath $choicePath) {
    $choice = (Get-ItemProperty -LiteralPath $choicePath).ProgId
    if ($choice -and $choice -ne $progId) {
        throw "Windows has an explicit .cadprt default ($choice). Select FreeCAD Plus through Windows Default Apps first."
    }
}
$command = '"' + $Executable + '" --single-instance'
if ($UserConfig) { $command += ' --user-cfg "' + $UserConfig + '"' }
$command += ' "%1"'
$entries = @(
    @{Path='Software\Classes\.cadprt'; Name=''; Value=$progId; Kind='String'},
    @{Path='Software\Classes\.cadprt\OpenWithProgids'; Name=$progId; Value=[byte[]]@(); Kind='None'},
    @{Path="Software\Classes\$progId"; Name=''; Value='FreeCAD Plus document'; Kind='String'},
    @{Path="Software\Classes\$progId"; Name='FriendlyTypeName'; Value='FreeCAD Plus document'; Kind='String'},
    @{Path="Software\Classes\$progId\DefaultIcon"; Name=''; Value=('"'+$Icon+'",0'); Kind='String'},
    @{Path="Software\Classes\$progId\shell\open\command"; Name=''; Value=$command; Kind='String'}
)
if (Test-Path -LiteralPath $BackupFile) { throw 'Choose a new association backup filename.' }
$backup = foreach ($entry in $entries) {
    $key = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey($entry.Path)
    $exists = $key -and ($key.GetValueNames() -contains $entry.Name)
    [pscustomobject]@{Path=$entry.Path; Name=$entry.Name; KeyExisted=($null -ne $key); ValueExisted=[bool]$exists;
        Kind=$(if ($exists) {$key.GetValueKind($entry.Name).ToString()} else {$null});
        Value=$(if ($exists) {$key.GetValue($entry.Name)} else {$null})}
    if ($key) { $key.Dispose() }
}
$backup | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $BackupFile -Encoding utf8
foreach ($entry in $entries) {
    $key = [Microsoft.Win32.Registry]::CurrentUser.CreateSubKey($entry.Path)
    try { $key.SetValue($entry.Name, $entry.Value, [Microsoft.Win32.RegistryValueKind]$entry.Kind) }
    finally { $key.Dispose() }
}
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class PlusShellAssociation {
    [DllImport("shell32.dll")] public static extern void SHChangeNotify(uint eventId, uint flags, IntPtr item1, IntPtr item2);
}
'@
[PlusShellAssociation]::SHChangeNotify(0x08000000, 0, [IntPtr]::Zero, [IntPtr]::Zero)
[pscustomobject]@{Extension='.cadprt'; ProgId=$progId; Icon=$Icon; OpenCommand=$command; Backup=$BackupFile} | ConvertTo-Json
