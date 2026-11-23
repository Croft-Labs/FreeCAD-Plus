$ErrorActionPreference = 'Stop'
$taskRoot = (Resolve-Path -LiteralPath 'C:\Users\dgium\Documents\__Apps\_temp builds\FreeCAD-Plus\validation\task-error-preview-20261123').Path
$taskTargets = @('baseline', 'candidate') | ForEach-Object { Join-Path $taskRoot $_ }
foreach ($taskTarget in $taskTargets) {
    $taskResolved = (Resolve-Path -LiteralPath $taskTarget).Path
    if ([IO.Path]::GetDirectoryName($taskResolved) -ne $taskRoot -or
        -not $taskResolved.StartsWith($taskRoot + '\', [StringComparison]::OrdinalIgnoreCase) -or
        (Get-Item -LiteralPath $taskResolved).Attributes -band [IO.FileAttributes]::ReparsePoint) {
        throw "Unsafe preview cleanup target: $taskResolved"
    }
    if (@(Get-ChildItem -LiteralPath $taskResolved -Recurse -Force |
        Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
        throw 'Preview cleanup target contains a reparse point'
    }
}
foreach ($taskTarget in $taskTargets) { Remove-Item -LiteralPath $taskTarget -Recurse -Force }
@{ removed = $taskTargets; archived = 'ai-instructions/evidence/task-error-preview-20261123' } |
    ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskRoot 'cleanup.json')
