$ErrorActionPreference='Stop'
$taskRoot=[IO.Path]::GetFullPath('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus/validation/thicken-20261123')
$taskResolved=(Resolve-Path -LiteralPath $taskRoot).Path
if ($taskResolved -ne $taskRoot) { throw 'Unexpected validation root' }
$taskItems=Get-ChildItem -LiteralPath $taskResolved -Force
if ((Get-Item -LiteralPath $taskResolved).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse root' }
$removed=@()
foreach ($taskItem in $taskItems) {
    if ($taskItem.Name -in @('install-backup','profile-shortcut','install-manifest.json')) { continue }
    $taskPath=[IO.Path]::GetFullPath($taskItem.FullName)
    if ([IO.Path]::GetDirectoryName($taskPath) -ne $taskResolved) { throw 'Unexpected cleanup target' }
    if ($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse target' }
    if ($taskItem.PSIsContainer) {
        $taskLinks=Get-ChildItem -LiteralPath $taskPath -Recurse -Force | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }
        if ($taskLinks) { throw 'Reparse descendant' }
        Remove-Item -LiteralPath $taskPath -Recurse -Force
    } else { Remove-Item -LiteralPath $taskPath -Force }
    $removed+=$taskItem.Name
}
@{removed=$removed;retained=@('install-backup','profile-shortcut','install-manifest.json')} | ConvertTo-Json | Set-Content -LiteralPath 'C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus/ai-instructions/evidence/thicken-20261123/cleanup.json'
