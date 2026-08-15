Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$requiredPaths = @(
  "deploy/railway/bootstrap.railway.toml",
  "deploy/railway/web.railway.toml",
  "deploy/railway/websocket.railway.toml",
  "deploy/railway/scheduler.railway.toml",
  "deploy/railway/worker-short.railway.toml",
  "deploy/railway/worker-long.railway.toml",
  "deploy/railway/migrate.railway.toml",
  "deploy/compose/staging.compose.yaml",
  "deploy/aws/ecs-task-definition.template.json",
  "deploy/env/staging.env.example",
  "scripts/deploy/start-service.sh"
)

foreach ($path in $requiredPaths) {
  if (-not (Test-Path $path)) {
    Write-Error "Missing deployment artifact: $path"
  }
}

Get-Content "deploy/aws/ecs-task-definition.template.json" -Raw | ConvertFrom-Json | Out-Null

$entrypoint = Get-Content "scripts/deploy/start-service.sh" -Raw
$requiredEntrypointPatterns = @(
  'bootstrap\)',
  '--no-setup-db',
  'socketio_port="\$\{PORT:-\$\{socketio_port\}\}"',
  'bench worker --queue short,default',
  'bench worker --queue long'
)

foreach ($pattern in $requiredEntrypointPatterns) {
  if ($entrypoint -notmatch $pattern) {
    Write-Error "Missing required runtime behavior: $pattern"
  }
}

$forbiddenPatterns = @(
  "(?i)DB_PASSWORD\s*=\s*(?!replace-through-managed-secret-store)",
  "(?i)SITE_ENCRYPTION_KEY\s*=\s*(?!replace-through-managed-secret-store)",
  "(?i)BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY"
)

$deploymentFiles = Get-ChildItem deploy -Recurse -File
foreach ($file in $deploymentFiles) {
  $content = Get-Content $file.FullName -Raw
  foreach ($pattern in $forbiddenPatterns) {
    if ($content -match $pattern) {
      Write-Error "Potential deployment secret found in $($file.FullName)"
    }
  }
}

Write-Host "Deployment artifact check passed."
