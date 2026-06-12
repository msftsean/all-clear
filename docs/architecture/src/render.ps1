# Renders the architecture diagram HTML sources to PNGs (headless Edge, 2x).
# Usage:  pwsh docs/architecture/src/render.ps1
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$src  = $PSScriptRoot
$out  = Split-Path $src -Parent   # docs/architecture

$jobs = @(
  @{ html = "deployment-infrastructure.html"; png = "allclear-deployment-infrastructure.png"; w = 2000; h = 1000 },
  @{ html = "agent-workflow.html";            png = "allclear-agent-workflow.png";            w = 2000; h = 1000 }
)

foreach ($j in $jobs) {
  $in  = Join-Path $src $j.html
  if (-not (Test-Path $in)) { Write-Host "skip (no source): $($j.html)"; continue }
  $png = Join-Path $out $j.png
  $uri = "file:///" + ($in -replace '\\','/')
  & $edge --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 `
    --screenshot="$png" --window-size="$($j.w),$($j.h)" $uri | Out-Null
  Write-Host "rendered $($j.png)"
}
