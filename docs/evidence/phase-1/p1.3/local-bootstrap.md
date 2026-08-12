# P1.3 Evidence - Local Development Site Bootstrap

Date: 2026-08-09

Status: Complete with follow-up

## Scope

The local Frappe development stack was started with Docker Compose, and the `erp.localhost` site was created with the required pinned upstream apps plus `university_erp`.

## Runtime Verification

Docker Compose services were running:

- `backend`
- `mariadb`
- `redis-cache`
- `redis-queue`
- `redis-socketio`
- `websocket`
- `scheduler`
- `worker-short`
- `worker-long`

MariaDB reported healthy through Docker Compose.

Site configuration reported:

```text
db_host        mariadb
db_port        3306
redis_cache    redis://redis-cache:6379
redis_queue    redis://redis-queue:6379
redis_socketio redis://redis-socketio:6379
socketio_port  9000
db_type        mariadb
```

Installed apps reported by `bench --site erp.localhost list-apps`:

```text
frappe         16.19.0 HEAD
erpnext        16.22.0 HEAD
payments       0.0.1   HEAD
education      16.0.1  HEAD
crm            1.72.0  HEAD
university_erp 0.0.0   UNVERSIONED
```

HTTP smoke test:

```text
GET http://erp.localhost:8000
StatusCode=200
```

Custom app import smoke test passed in all Python service containers:

```text
backend      0.0.0
scheduler    0.0.0
worker-short 0.0.0
worker-long  0.0.0
```

Docker Compose configuration validation passed:

```text
docker compose config --quiet
compose config ok
```

## Bootstrap Changes

- `scripts/bootstrap/init-site.sh` now installs apps in order: ERPNext, Payments, Education, CRM, `university_erp`.
- `scripts/bootstrap/init-site.sh` installs `university_erp` in editable mode and registers it in `sites/apps.txt`.
- `docker/Dockerfile` copies `apps/university_erp` and installs it in the image build path.
- `.dockerignore` excludes runtime and dependency folders from the Docker build context.

## Follow-up

The local running stack is verified, but rebuilding the updated Docker image exceeded the command timeout twice in this environment. The previously built image had already started the stack successfully; the Dockerfile changes for including `university_erp` need a later clean rebuild confirmation before production-style image evidence is accepted.

Observed non-blocking warnings:

- Frappe printed `Error creating icons 'NoneType' object has no attribute 'startswith'` during app installation for Education, CRM and `university_erp`.
- Initial web request failed until long-running Python services were restarted after installing `university_erp`.
