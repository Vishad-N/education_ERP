param(
  [switch]$Bootstrap
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$site = if ($env:SITE_NAME) { $env:SITE_NAME } else { "erp.localhost" }

$install = "env/bin/pip install --editable apps/university_erp"
if ($Bootstrap) {
  $setup = "$install && bench new-site $site --admin-password admin --mariadb-root-password admin --db-host mariadb --db-port 3306 --force && bench --site $site install-app erpnext && bench --site $site install-app payments && bench --site $site install-app education && bench --site $site install-app crm && bench --site $site install-app university_erp && bench --site $site set-config allow_tests true"
  docker compose run --rm backend bash -lc $setup
} else {
  docker compose run --rm backend bash -lc "$install && bench --site $site migrate && bench --site $site set-config allow_tests true"
}

docker compose run --rm backend bash -lc "$install && bench --site $site run-tests --app university_erp"
