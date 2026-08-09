#!/usr/bin/env bash
set -euo pipefail

site_name="${SITE_NAME:-erp.localhost}"
admin_password="${ADMIN_PASSWORD:-admin}"
db_root_password="${DB_ROOT_PASSWORD:-admin}"

bench new-site "$site_name" \
  --admin-password "$admin_password" \
  --mariadb-root-password "$db_root_password" \
  --db-host "${DB_HOST:-mariadb}" \
  --db-port "${DB_PORT:-3306}" \
  --force

bench --site "$site_name" install-app erpnext
bench --site "$site_name" install-app education
bench --site "$site_name" install-app crm

if [ -f "apps/university_erp/university_erp/hooks.py" ]; then
  bench --site "$site_name" install-app university_erp
else
  echo "university_erp has not been generated yet; skipping custom app install."
fi

bench --site "$site_name" migrate
