# Finds Tabular Editor 2 (free) automatically. Override: $env:TE_PATH = "C:\...\TabularEditor.exe"
$candidates = @(
    $env:TE_PATH,
    "C:\Program Files (x86)\Tabular Editor\TabularEditor.exe",
    "C:\Program Files\Tabular Editor\TabularEditor.exe",
    "C:\Tools\TabularEditor\TabularEditor.exe",
    "$env:LOCALAPPDATA\TabularEditor\TabularEditor.exe"
) | Where-Object { $_ -and (Test-Path $_) }
if (-not $candidates) {
    $cmd = Get-Command TabularEditor.exe -ErrorAction SilentlyContinue
    if ($cmd) { $candidates = @($cmd.Source) }
}
if (-not $candidates) {
    Write-Host "Tabular Editor 2 not found. Install it (github.com/TabularEditor/TabularEditor/releases) or set TE_PATH." -ForegroundColor Red
    exit 2
}
$te    = @($candidates)[0]
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