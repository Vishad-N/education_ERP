#!/usr/bin/env bash
set -euo pipefail

role="${1:-${SERVICE_ROLE:-web}}"
site_name="${SITE_NAME:?SITE_NAME is required}"
db_host="${DB_HOST:?DB_HOST is required}"
db_port="${DB_PORT:-3306}"
db_name="${DB_NAME:?DB_NAME is required}"
db_user="${DB_USER:-${db_name}}"
db_password="${DB_PASSWORD:?DB_PASSWORD is required}"
redis_cache="${REDIS_CACHE:?REDIS_CACHE is required}"
redis_queue="${REDIS_QUEUE:?REDIS_QUEUE is required}"
redis_socketio="${REDIS_SOCKETIO:?REDIS_SOCKETIO is required}"
site_encryption_key="${SITE_ENCRYPTION_KEY:?SITE_ENCRYPTION_KEY is required}"
socketio_port="${SOCKETIO_PORT:-9000}"

if [[ "${role}" == "websocket" ]]; then
  socketio_port="${PORT:-${socketio_port}}"
fi

cd /home/frappe/frappe-bench
mkdir -p sites

SERVICE_ROLE="${role}" \
SITE_NAME="${site_name}" \
DB_HOST="${db_host}" \
DB_PORT="${db_port}" \
DB_NAME="${db_name}" \
DB_USER="${db_user}" \
DB_PASSWORD="${db_password}" \
REDIS_CACHE="${redis_cache}" \
REDIS_QUEUE="${redis_queue}" \
REDIS_SOCKETIO="${redis_socketio}" \
SOCKETIO_PORT="${socketio_port}" \
SITE_ENCRYPTION_KEY="${site_encryption_key}" \
python - <<'PY'
import json
import os
from pathlib import Path

sites = Path("sites")
role = os.environ["SERVICE_ROLE"]
site_name = os.environ["SITE_NAME"]
common = {
    "db_host": os.environ["DB_HOST"],
    "db_port": int(os.environ["DB_PORT"]),
    "redis_cache": os.environ["REDIS_CACHE"],
    "redis_queue": os.environ["REDIS_QUEUE"],
    "redis_socketio": os.environ["REDIS_SOCKETIO"],
    "socketio_port": int(os.environ["SOCKETIO_PORT"]),
    "default_site": site_name,
    "serve_default_site": True,
}
site = {
    "db_name": os.environ["DB_NAME"],
    "db_user": os.environ["DB_USER"],
    "db_password": os.environ["DB_PASSWORD"],
    "encryption_key": os.environ["SITE_ENCRYPTION_KEY"],
}
(sites / "common_site_config.json").write_text(json.dumps(common, indent=2) + "\n")
if role != "bootstrap":
    site_dir = sites / site_name
    site_dir.mkdir(parents=True, exist_ok=True)
    # Frappe RotatingFileHandler opens sites/<site>/logs/*.log on the first
    # request. The web role does not run bench new-site, so create the
    # directories a site needs to answer health probes.
    for child in ("logs", "locks", "private", "public"):
        (site_dir / child).mkdir(exist_ok=True)
    (site_dir / "site_config.json").write_text(json.dumps(site, indent=2) + "\n")
    (sites / "currentsite.txt").write_text(site_name + "\n")
PY

case "${role}" in
  bootstrap)
    site_admin_password="${SITE_ADMIN_PASSWORD:?SITE_ADMIN_PASSWORD is required for bootstrap}"
    bench new-site "${site_name}" \
      --no-setup-db \
      --db-host "${db_host}" \
      --db-port "${db_port}" \
      --db-name "${db_name}" \
      --db-user "${db_user}" \
      --db-password "${db_password}" \
      --admin-password "${site_admin_password}" \
      --install-app erpnext \
      --install-app payments \
      --install-app education \
      --install-app crm \
      --install-app university_erp \
      --set-default
    bench --site "${site_name}" set-config encryption_key "${site_encryption_key}"
    ;;
  web)
    # Log only connection status so managed-service configuration failures are
    # visible in Railway deploy logs without exposing credentials.
    DB_HOST="${db_host}" \
    DB_PORT="${db_port}" \
    DB_NAME="${db_name}" \
    DB_USER="${db_user}" \
    DB_PASSWORD="${db_password}" \
    REDIS_CACHE="${redis_cache}" \
    env/bin/python - <<'PY'
import os
import re
import sys

failed_checks = []


def safe_error(error):
	message = str(error).replace(os.environ["REDIS_CACHE"], "<redis-url>")
	message = re.sub(r"(redis(?:s)?://[^:\s/]+:)[^@\s]+@", r"\1***@", message)
	return f"{type(error).__name__}: {message[:240]}"

try:
	import pymysql

	connection = pymysql.connect(
		host=os.environ["DB_HOST"],
		port=int(os.environ["DB_PORT"]),
		user=os.environ["DB_USER"],
		password=os.environ["DB_PASSWORD"],
		database=os.environ["DB_NAME"],
		connect_timeout=10,
	)
	connection.close()
	print("Startup preflight: MariaDB connection succeeded", flush=True)
except Exception as error:
	failed_checks.append("MariaDB")
	print(f"Startup preflight: MariaDB connection failed ({safe_error(error)})", flush=True)

try:
	from redis import Redis

	Redis.from_url(os.environ["REDIS_CACHE"], socket_connect_timeout=10).ping()
	print("Startup preflight: Redis connection succeeded", flush=True)
except Exception as error:
	failed_checks.append("Redis")
	print(f"Startup preflight: Redis connection failed ({safe_error(error)})", flush=True)

if failed_checks:
	sys.exit(1)
PY
    # Railway Metal healthchecks connect over IPv6. Binding only 0.0.0.0
    # leaves Gunicorn healthy on IPv4 while the probe gets connection refused.
    if [[ -n "${RAILWAY_ENVIRONMENT:-}" || "${WEB_BIND_IPV6:-0}" == "1" ]]; then
      web_bind="[::]:${PORT:-8000}"
    else
      web_bind="${WEB_BIND_HOST:-0.0.0.0}:${PORT:-8000}"
    fi
    echo "Starting web on ${web_bind}"
    exec env/bin/gunicorn \
      --chdir sites \
      --bind "${web_bind}" \
      --threads "${WEB_THREADS:-4}" \
      --workers "${WEB_WORKERS:-2}" \
      --worker-class gthread \
      --worker-tmp-dir /dev/shm \
      --timeout "${WEB_TIMEOUT:-120}" \
      --forwarded-allow-ips="*" \
      --preload \
      "university_erp.wsgi:create_application()"
    ;;
  websocket)
    exec node apps/frappe/socketio.js
    ;;
  scheduler)
    exec bench schedule
    ;;
  worker-short)
    exec bench worker --queue short,default
    ;;
  worker-long)
    exec bench worker --queue long
    ;;
  migrate)
    exec bench --site "${site_name}" migrate
    ;;
  combined)
    # Constrained staging only: one replica runs the scheduler and all queues.
    # Split back to dedicated services before production or peak admissions.
    bench schedule &
    scheduler_pid=$!
    bench worker --queue short,default,long &
    worker_pid=$!
    trap 'kill "${scheduler_pid}" "${worker_pid}" 2>/dev/null || true' EXIT
    wait "${scheduler_pid}" "${worker_pid}"
    ;;
  *)
    echo "Unsupported SERVICE_ROLE: ${role}" >&2
    exit 64
    ;;
esac
