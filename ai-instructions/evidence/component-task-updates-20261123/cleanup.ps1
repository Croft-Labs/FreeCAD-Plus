$ErrorActionPreference = 'Stop'
$taskRoot = (Resolve-Path -LiteralPath 'C:\Users\dgium\Documents\__Apps\_temp builds\FreeCAD-Plus\validation\component-task-updates-20261123').Path
$taskKeep = @('install-backup', 'profile-shortcut')
$taskTargets = @(Get-ChildItem -LiteralPath $taskRoot -Directory | Where-Object Name -NotIn $taskKeep)
$taskTargets += @(Get-ChildItem -LiteralPath $taskRoot -File | Where-Object Extension -In @('.cadprt', '.FCStd', '.FCBak', '.png'))
# Validate every resolved target before any recursive deletion. Retain installed
# rollback files, durable evidence and the profile used by the restarted app.
foreach ($taskTarget in $taskTargets) {
    $taskResolved = (Resolve-Path -LiteralPath $taskTarget.FullName).Path
    if ([IO.Path]::GetDirectoryName($taskResolved) -ne $taskRoot -or
        -not $taskResolved.StartsWith($taskRoot + '\', [StringComparison]::OrdinalIgnoreCase) -or
        ($taskTarget.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        throw "Unsafe cleanup target: $taskResolved"
    }
    if ($taskTarget.PSIsContainer -and
        @(Get-ChildItem -LiteralPath $taskResolved -Force -Recurse |
            Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
        throw "Cleanup target contains a reparse point: $taskResolved"
    }
}
foreach ($taskTarget in $taskTargets) {
    Remove-Item -LiteralPath $taskTarget.FullName -Recurse -Force
}
@{ root = $taskRoot; removed = @($taskTargets.Name); retained = $taskKeep } |
    ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $taskRoot 'cleanup.json')
