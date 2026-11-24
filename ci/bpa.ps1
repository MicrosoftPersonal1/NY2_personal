# Findet Tabular Editor 2 automatisch in definierter Reihenfolge.
$teCandidates = @(
    $env:TE_PATH,
    "C:\Program Files (x86)\Tabular Editor\TabularEditor.exe",
    "C:\Program Files\Tabular Editor\TabularEditor.exe"
)
$te = $null
foreach ($candidate in $teCandidates) {
    if ($candidate -and (Test-Path $candidate)) {
        $te = $candidate
        break
    }
}
if (-not $te) {
    $cmd = Get-Command TabularEditor.exe -ErrorAction SilentlyContinue
    if ($cmd) { $te = $cmd.Source }
}
if (-not $te) {
    Write-Host "Tabular Editor 2 wurde nicht gefunden. Bitte TE_PATH setzen oder Tabular Editor 2 unter 'C:\Program Files (x86)\Tabular Editor\' bzw. 'C:\Program Files\Tabular Editor\' installieren." -ForegroundColor Red
    exit 2
}
$rules = "bpa\Rules-NY.json"
Write-Host "Using $te"
$failed = $false
Get-ChildItem workspace -Recurse -Filter "definition.pbism" | ForEach-Object {
    $model = Join-Path $_.Directory.FullName "definition"
    $out   = "bpa-$($_.Directory.BaseName).txt"
    $p = Start-Process $te -Wait -NoNewWindow -PassThru -RedirectStandardOutput $out `
         -ArgumentList "`"$model`" -A `"$rules`""
    Get-Content $out
    if ($p.ExitCode -ne 0) { $failed = $true }
}
if ($failed) { exit 1 }