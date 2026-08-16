#!/usr/bin/env bash
# Restore a gzipped logical dump into a target database.
# Default target is a disposable verification database, not the live site.
set -euo pipefail

db_host="${DB_HOST:?DB_HOST is required}"
db_port="${DB_PORT:-3306}"
db_user="${DB_USER:?DB_USER is required}"
db_password="${DB_PASSWORD:?DB_PASSWORD is required}"
source_db="${DB_NAME:?DB_NAME is required}"
dump_file="${1:?Usage: restore-mariadb.sh <dump.sql.gz> [target-db]}"
target_db="${2:-${source_db}_restore_$(date -u +%Y%m%dT%H%M%SZ)}"

if [[ ! -f "${dump_file}" ]]; then
  echo "Dump file not found: ${dump_file}" >&2
  exit 1
fi

if [[ "${target_db}" == "${source_db}" && "${ALLOW_LIVE_RESTORE:-0}" != "1" ]]; then
  echo "Refusing to restore over live database ${source_db}. Set ALLOW_LIVE_RESTORE=1 to override." >&2
  exit 2
fi

checksum_file="${dump_file}.sha256"
if [[ -f "${checksum_file}" ]]; then
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum -c "${checksum_file}"
  else
    expected="$(awk '{print $1}' "${checksum_file}")"
    actual="$(shasum -a 256 "${dump_file}" | awk '{print $1}')"
    [[ "${expected}" == "${actual}" ]]
  fi
fi

mysql_cmd=(mysql --host="${db_host}" --port="${db_port}" --user="${db_user}")
export MYSQL_PWD="${db_password}"

"${mysql_cmd[@]}" -e "CREATE DATABASE IF NOT EXISTS \`${target_db}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
gzip -dc "${dump_file}" | "${mysql_cmd[@]}" "${target_db}"

source_tables="$("${mysql_cmd[@]}" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='${source_db}';")"
target_tables="$("${mysql_cmd[@]}" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='${target_db}';")"
unset MYSQL_PWD

echo "Restored ${dump_file} into ${target_db}"
echo "Source table count (${source_db}): ${source_tables}"
echo "Target table count (${target_db}): ${target_tables}"

if [[ "${source_tables}" != "${target_tables}" ]]; then
  echo "Table-count mismatch after restore" >&2
  exit 3
fi
