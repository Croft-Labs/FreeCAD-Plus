# SPDX-License-Identifier: LGPL-2.1-or-later
# Owner-approved output roots; relative paths are relative to the selected root.
function Resolve-FreeCADArtifactPath {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [ValidateSet('validation','test-builds')][string]$Kind = 'validation'
    )
    $taskRoot = [IO.Path]::GetFullPath((Join-Path $env:USERPROFILE "Documents\_temp\freecad\$Kind")).TrimEnd('\')
    $taskPath = [IO.Path]::GetFullPath($(if ([IO.Path]::IsPathRooted($Path)) { $Path } else { Join-Path $taskRoot $Path }))
    if (-not $taskPath.StartsWith($taskRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "FreeCAD $Kind output must be a child of $taskRoot."
    }
    # Refuse junctions/symlinks that could redirect generated output elsewhere.
    $taskAncestor = $taskPath
    while ($taskAncestor.Length -ge $taskRoot.Length) {
        if (Test-Path -LiteralPath $taskAncestor) {
            if ((Get-Item -LiteralPath $taskAncestor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "Reparse points are not supported in FreeCAD output paths: $taskAncestor"
            }
        }
        $taskAncestor = Split-Path -Parent $taskAncestor
    }
    return $taskPath
}
