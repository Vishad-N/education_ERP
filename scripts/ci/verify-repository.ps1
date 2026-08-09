Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$requiredPaths = @(
  "AGENTS.md",
  "README.md",
  "apps.json",
  "compose.yaml",
  ".env.example",
  ".editorconfig",
  ".gitignore",
  ".pre-commit-config.yaml",
  "docker/Dockerfile",
  "scripts/bootstrap/check-prereqs.ps1",
  "scripts/bootstrap/init-site.sh",
  "apps/university_erp"
)

foreach ($path in $requiredPaths) {
  if (-not (Test-Path $path)) {
    Write-Error "Missing required path: $path"
  }
}

$secretPatterns = @(
  "RAZORPAY_KEY_SECRET\s*=",
  "MSG91_AUTH_KEY\s*=",
  "AWS_SECRET_ACCESS_KEY\s*=",
  "(?i)(secret|token|api[_-]?key)\s*=\s*['""][^'""]{8,}"
)

$files = Get-ChildItem -Recurse -File |
  Where-Object {
    $_.FullName -notmatch "\\node_modules\\" -and
    $_.FullName -notmatch "\\.git\\"
  }

foreach ($file in $files) {
  $content = Get-Content -Raw $file.FullName
  foreach ($pattern in $secretPatterns) {
    if ($content -match $pattern) {
      Write-Error "Potential secret pattern found in $($file.FullName): $pattern"
    }
  }
}

Write-Host "Repository foundation check passed."
