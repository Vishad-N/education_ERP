Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$requiredPaths = @(
  "deploy/railway/bootstrap.railway.toml",
  "deploy/railway/MANUAL_DEPLOYMENT_GUIDE.md",
  "deploy/railway/web.railway.toml",
  "deploy/railway/websocket.railway.toml",
  "deploy/railway/scheduler.railway.toml",
  "deploy/railway/worker-short.railway.toml",
  "deploy/railway/worker-long.railway.toml",
  "deploy/railway/migrate.railway.toml",
  "deploy/railway/backup.railway.toml",
  "deploy/railway/combined.railway.toml",
  "deploy/compose/staging.compose.yaml",
  "deploy/aws/ecs-task-definition.template.json",
  "deploy/env/staging.env.example",
  "deploy/cloudflare/README.md",
  "deploy/cloudflare/dns-records.example.yaml",
  "deploy/cloudflare/waf-rate-limits.example.yaml",
  "deploy/cloudflare/r2-bucket.example.json",
  "deploy/monitoring/README.md",
  "deploy/monitoring/uptime-probes.example.yaml",
  "deploy/monitoring/alert-rules.example.yaml",
  "scripts/deploy/start-service.sh",
  "scripts/operations/backup-mariadb.sh",
  "scripts/operations/restore-mariadb.sh",
  "scripts/operations/restore-proof.py",
  "docker/backup.Dockerfile",
  "docs/operations/rollback-and-forward-fix.md",
  "docs/operations/hypercare-plan.md",
  "docs/releases/p8-staging-manifest.md",
  "docs/releases/p8-source.cdx.json"
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
  'university_erp\.wsgi:create_application\(\)',
  'web_bind="\[::\]:\$\{PORT:-8000\}"',
  'for child in \("logs", "locks", "private", "public"\):',
  'bench worker --queue short,default',
  'bench worker --queue long',
  'combined\)',
  'bench worker --queue short,default,long'
)

foreach ($pattern in $requiredEntrypointPatterns) {
  if ($entrypoint -notmatch $pattern) {
    Write-Error "Missing required runtime behavior: $pattern"
  }
}

$forbiddenPatterns = @(
  '(?i)DB_PASSWORD\s*=\s*(?!(replace-through-managed-secret-store|\$\{\{|<))',
  '(?i)SITE_ENCRYPTION_KEY\s*=\s*(?!(replace-through-managed-secret-store|\$\{\{|<))',
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
