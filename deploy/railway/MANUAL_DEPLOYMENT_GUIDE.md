# Manual Railway Staging Deployment

This guide deploys the staging environment manually from the Railway dashboard. It does not authorize production use.

## Project files

| Purpose              | File                                       |
| -------------------- | ------------------------------------------ |
| Image build          | `docker/Dockerfile`                        |
| Runtime start script | `scripts/deploy/start-service.sh`          |
| Variable template    | `deploy/env/staging.env.example`           |
| Bootstrap config     | `deploy/railway/bootstrap.railway.toml`    |
| Migration config     | `deploy/railway/migrate.railway.toml`      |
| Web config           | `deploy/railway/web.railway.toml`          |
| WebSocket config     | `deploy/railway/websocket.railway.toml`    |
| Scheduler config     | `deploy/railway/scheduler.railway.toml`    |
| Short-worker config  | `deploy/railway/worker-short.railway.toml` |
| Long-worker config   | `deploy/railway/worker-long.railway.toml`  |

## 1. Publish one image

Publish the locally verified image to Docker Hub, GHCR, Quay or GitLab Container Registry. Use a version tag and record the pushed digest. Create every application service from that exact registry digest, not from a mutable tag.

The Dockerfile fetches Frappe, ERPNext, Education, CRM and Payments at the exact commits declared in `apps.json`; it does not depend on the untracked local `apps/` checkouts. The base Bench image is also pinned by digest. Treat the registry-reported digest of your published result as authoritative for Railway.

## 2. Create data services

### MariaDB

Create a private service from `mariadb:11.8`, attach a persistent volume at `/var/lib/mysql`, and do not generate a public domain or TCP proxy.

Set sealed variables on the MariaDB service:

```dotenv
MARIADB_DATABASE=education_erp_staging
MARIADB_USER=education_erp_staging
MARIADB_PASSWORD=<generated-secret>
MARIADB_ROOT_PASSWORD=<different-generated-secret>
```

Do not use PostgreSQL. Railway's managed MySQL offering is not the verified MariaDB 11.8 baseline for this project.

### Redis

Create three private Redis services named `redis-cache`, `redis-queue`, and `redis-socketio`. Their private `REDIS_URL` variables become the three Frappe Redis variables. One Redis service with separate logical databases is acceptable only for short-lived staging after explicit verification.

## 3. Create shared variables

Create these in the staging environment's Shared Variables page, seal the secret values, and share them with all application services:

```dotenv
SITE_NAME=<final-web-domain>
SITE_ENCRYPTION_KEY=<generated-long-random-secret>
DB_HOST=${{mariadb.RAILWAY_PRIVATE_DOMAIN}}
DB_PORT=3306
DB_NAME=${{mariadb.MARIADB_DATABASE}}
DB_USER=${{mariadb.MARIADB_USER}}
DB_PASSWORD=${{mariadb.MARIADB_PASSWORD}}
REDIS_CACHE=${{redis-cache.REDIS_URL}}
REDIS_QUEUE=${{redis-queue.REDIS_URL}}
REDIS_SOCKETIO=${{redis-socketio.REDIS_URL}}
WEB_WORKERS=2
WEB_THREADS=4
WEB_TIMEOUT=120
```

Do not set `PORT`; Railway injects it separately for public services.

## 4. Create application services

Create seven services from the same published image digest. Do not attach public networking except where stated.

| Service        | Start command                                             | Restart policy        | Public           |
| -------------- | --------------------------------------------------------- | --------------------- | ---------------- |
| `bootstrap`    | `/home/frappe/frappe-bench/start-service.sh bootstrap`    | Never                 | No               |
| `migrate`      | `/home/frappe/frappe-bench/start-service.sh migrate`      | Never                 | No               |
| `web`          | `/home/frappe/frappe-bench/start-service.sh web`          | On failure, 5 retries | Yes              |
| `websocket`    | `/home/frappe/frappe-bench/start-service.sh websocket`    | On failure, 5 retries | No until proxied | No  |
| `scheduler`    | `/home/frappe/frappe-bench/start-service.sh scheduler`    | On failure, 5 retries | No               |
| `worker-short` | `/home/frappe/frappe-bench/start-service.sh worker-short` | On failure, 5 retries | No               |
| `worker-long`  | `/home/frappe/frappe-bench/start-service.sh worker-long`  | On failure, 5 retries | No               |

Set the `web` health-check path to:

```text
/api/method/university_erp.api.health.ready
```

Use a 300-second health-check timeout. Keep `scheduler` at exactly one replica.

Railway Metal healthchecks connect over IPv6 and do not send the public site Host. The published image must bind `[::]:$PORT` and pin `SITE_NAME` in the WSGI factory. A Gunicorn line that only says `Listening at: http://0.0.0.0:8080` will fail this probe with `service unavailable` even though MariaDB and Redis preflight succeeded.

The `web` service is not ready until `bootstrap` and `migrate` have succeeded against the same database. An empty database makes `/api/method/university_erp.api.health.ready` fail after the process is listening.

## 5. Initialize the site

1. Confirm MariaDB and all Redis services are healthy.
2. Add the sealed `SITE_ADMIN_PASSWORD` variable only to `bootstrap`.
3. Deploy `bootstrap` once and wait for a successful exit.
4. Remove `SITE_ADMIN_PASSWORD` and disable or delete `bootstrap`.
5. Deploy `migrate` once and require a successful exit.
6. Start `worker-short`, `worker-long`, `scheduler`, `websocket`, and then `web`.

Never rerun bootstrap against a populated database. Run migration once for each new application image before sending traffic to it.

## 6. Networking

Generate a Railway domain for `web`, then update `SITE_NAME` to the final generated or custom staging hostname and redeploy all application roles.

The WebSocket process correctly binds Railway's assigned `PORT`, but browser realtime requires a same-origin `/socket.io` reverse-proxy route. Keep the WebSocket service private until that route exists. Core HTTP/API testing can proceed without realtime.

## 7. Acceptance checks

```text
GET https://<web-domain>/api/method/university_erp.api.health.live
GET https://<web-domain>/api/method/university_erp.api.health.ready
GET https://<web-domain>/guardian-admission
```

Require HTTP 200 for both health endpoints, and confirm the portal loads its JavaScript and CSS without 404 responses. Then verify:

- login and permissions;
- background jobs and scheduler logs;
- one fake payment flow only;
- private document behavior;
- database persistence after a web redeploy;
- backup creation and a separate restore test.

## Staging limitations

- Production Razorpay, MSG91, SMTP, R2 and Cloudflare credentials are not approved.
- Railway service filesystems are ephemeral. Real document testing requires the approved R2 integration; do not treat local container files as durable.
- Browser realtime is incomplete until same-origin WebSocket routing is configured.
- Human UAT remains tracked in `docs/quality/human-testing-readme.md`.
