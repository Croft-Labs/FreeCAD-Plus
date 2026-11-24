$ErrorActionPreference='Stop'
$taskRuntime='C:\Users\dgium\Documents\__Apps\_temp builds\FreeCAD-Plus\validation\feature-pick-20261123'
$taskWorkspace='C:\Users\dgium\Documents\__Apps\FreeCAD\feature-pick-validation'
$taskRemoved=@()
foreach($taskRoot in @($taskRuntime,$taskWorkspace)) {
    $taskResolved=(Resolve-Path -LiteralPath $taskRoot).Path
    if($taskResolved -ne $taskRoot) { throw 'Unexpected validation root' }
    $taskTargets=if($taskRoot -eq $taskRuntime) {
        Get-ChildItem -LiteralPath $taskRoot -Force | Where-Object Name -NotIn @('install-backup','install-manifest.json','profile-shortcut')
    } else { Get-ChildItem -LiteralPath $taskRoot -Directory | Where-Object Name -Like 'run-*' }
    foreach($taskTarget in $taskTargets) {
        $taskPath=(Resolve-Path -LiteralPath $taskTarget.FullName).Path
        if(-not $taskPath.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Cleanup escaped validation root' }
        if($taskTarget.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse target' }
        if($taskTarget.PSIsContainer -and (Get-ChildItem -LiteralPath $taskPath -Recurse -Force | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint })) { throw 'Reparse child' }
        Remove-Item -LiteralPath $taskPath -Recurse -Force
        $taskRemoved += $taskPath
    }
}
@{removed=$taskRemoved;retained=@('install-backup','install-manifest.json','profile-shortcut')} | ConvertTo-Json -Depth 3 |
    Set-Content -LiteralPath 'C:\Users\dgium\Documents\__Apps\FreeCAD\FreeCAD-Plus\ai-instructions\evidence\feature-pick-20261123\cleanup.json'
