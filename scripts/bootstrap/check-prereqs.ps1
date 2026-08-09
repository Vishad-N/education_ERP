Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$commands = @(
  @{ Name = "git"; Expected = "Git" },
  @{ Name = "docker"; Expected = "Docker" },
  @{ Name = "docker"; Args = @("compose", "version"); Expected = "Docker Compose" },
  @{ Name = "node"; Expected = "Node.js" },
  @{ Name = "npm.cmd"; Expected = "npm" }
)

if (-not $env:DOCKER_CONFIG) {
  $dockerConfig = Join-Path (Get-Location) ".docker-cli"
  New-Item -ItemType Directory -Force -Path $dockerConfig | Out-Null
  $env:DOCKER_CONFIG = $dockerConfig
}

foreach ($command in $commands) {
  $exe = Get-Command $command.Name -ErrorAction SilentlyContinue
  if (-not $exe) {
    Write-Error "$($command.Expected) is not available on PATH."
  }

  if ($command.ContainsKey("Args")) {
    & $command.Name @($command.Args)
  } else {
    & $command.Name --version
  }
}

$oldErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& docker info *> $null
$dockerExitCode = $LASTEXITCODE
$ErrorActionPreference = $oldErrorActionPreference
if ($dockerExitCode -eq 0) {
  Write-Host "Docker daemon is reachable."
} else {
  Write-Warning "Docker CLI is installed, but the daemon is not reachable. Start Docker Desktop and retry."
}
