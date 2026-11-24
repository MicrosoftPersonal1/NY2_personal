param(
    [string]$Branch = "feature/report-umsatz-land",
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    Write-Host "Kein Git-Repository gefunden." -ForegroundColor Red
    exit 1
}

if (-not $Force) {
    Write-Host "Dieses Skript verwirft lokale, nicht commitete Änderungen und untracked Dateien." -ForegroundColor Yellow
    Write-Host "Ziel-Branch: $Branch"
    $answer = Read-Host "Zum Fortfahren exakt 'JA' eingeben"
    if ($answer -ne "JA") {
        Write-Host "Abgebrochen."
        exit 0
    }
}

git switch $Branch
if ($LASTEXITCODE -ne 0) {
    Write-Host "Branch '$Branch' konnte nicht gewechselt werden." -ForegroundColor Red
    exit 1
}

git restore --staged --worktree .
if ($LASTEXITCODE -ne 0) {
    Write-Host "git restore ist fehlgeschlagen." -ForegroundColor Red
    exit 1
}

git clean -fd
if ($LASTEXITCODE -ne 0) {
    Write-Host "git clean ist fehlgeschlagen." -ForegroundColor Red
    exit 1
}

Write-Host "Demo-Stand wurde zurückgesetzt (Branch: $Branch)." -ForegroundColor Green
