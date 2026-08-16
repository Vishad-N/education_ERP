#!/usr/bin/env bash
# Logical MariaDB backup for staging or production-like sites.
# Does not print passwords. Writes a .sql.gz file and a sibling .sha256 checksum.
set -euo pipefail

db_host="${DB_HOST:?DB_HOST is required}"
db_port="${DB_PORT:-3306}"
db_name="${DB_NAME:?DB_NAME is required}"
db_user="${DB_USER:?DB_USER is required}"
db_password="${DB_PASSWORD:?DB_PASSWORD is required}"
backup_dir="${BACKUP_DIR:-/backups}"
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "${backup_dir}"

target="${backup_dir}/${db_name}-${stamp}.sql.gz"
checksum="${target}.sha256"

export MYSQL_PWD="${db_password}"
mysqldump \
  --host="${db_host}" \
  --port="${db_port}" \
  --user="${db_user}" \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  --hex-blob \
  --set-gtid-purged=OFF \
  "${db_name}" \
  | gzip -c > "${target}"
unset MYSQL_PWD

if command -v sha256sum >/dev/null 2>&1; then
  sha256sum "${target}" > "${checksum}"
else
  shasum -a 256 "${target}" > "${checksum}"
fi

bytes="$(wc -c < "${target}" | tr -d ' ')"
if [[ "${bytes}" -lt 1024 ]]; then
  echo "Backup file is too small (${bytes} bytes)" >&2
  exit 1
fi

echo "Backup written: ${target}"
echo "Checksum written: ${checksum}"
echo "Bytes: ${bytes}"
