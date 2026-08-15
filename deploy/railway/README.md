# Railway Staging

Railway is the first staging target, not the approved production platform. Deploy the same immutable image as separate services because Railway maps Compose services individually.

## Services

| Railway service | Config file | Public | Role |
|---|---|---|---|
| `bootstrap` | `bootstrap.railway.toml` | No | One-shot first-site initialization against an empty managed database |
| `web` | `web.railway.toml` | Yes | Gunicorn HTTP/API and built portal assets |
| `websocket` | `websocket.railway.toml` | Only through an approved proxy/domain route | Frappe realtime |
| `scheduler` | `scheduler.railway.toml` | No | Singleton scheduler |
| `worker-short` | `worker-short.railway.toml` | No | Short/default jobs |
| `worker-long` | `worker-long.railway.toml` | No | Long jobs |
| `migrate` | `migrate.railway.toml` | No | One-shot controlled schema migration |

Use the custom config path shown above in each service. Configure all values from `deploy/env/staging.env.example` as Railway variables or reference variables. Do not commit resolved values.

The recommended manual deployment source is one published image reference pinned by digest. Configure every service to use exactly the same digest and copy the corresponding start command from its TOML file. The TOML `[build]` sections are a Git-source fallback; Git-based services build independently, so compare their resulting image digests before migration or traffic.

## Data services

- Use a MariaDB-compatible private service with persistent storage and tested backups. Do not substitute PostgreSQL or assume Railway MySQL is equivalent; this baseline is verified against MariaDB 11.8.
- Set `DB_NAME`, `DB_USER` and `DB_PASSWORD` to an empty database and its existing managed user. The bootstrap role uses Frappe's `--no-setup-db` path and does not require a database root credential.
- Use private Redis/Valkey endpoints. Separate cache, queue and realtime instances for production; staging may use isolated logical instances after verification.
- Keep files private in R2/S3-compatible storage. Railway service filesystems are not authoritative storage.

## Staging sequence

1. Build and publish one immutable image digest.
2. Create private database and Redis services/endpoints.
3. Add managed variables and a shared `SITE_ENCRYPTION_KEY` to every role.
4. Add `SITE_ADMIN_PASSWORD` only to `bootstrap`, run that service once against the empty database, confirm success, then remove the variable and disable/delete the bootstrap service.
5. Run the `migrate` service once after every newly published application image and confirm success before starting web traffic.
6. Start workers, scheduler, WebSocket and web.
7. Expose only web and the required WebSocket route.
8. Verify readiness, portals, queues, payment fake mode, private files, backup and restore.

Railway health checks require the web process to bind to `PORT`; `start-service.sh` does this. The readiness endpoint checks both MariaDB and Redis.

Railway also assigns `PORT` to the WebSocket service. The runtime entrypoint writes that value into Frappe's `socketio_port` configuration before Node starts. A same-origin `/socket.io` reverse-proxy route is still required for browser realtime; keep the WebSocket service private until that route is configured.

## Manual acceptance gate

- `bootstrap` exits successfully and the database contains the installed Frappe applications.
- `migrate` exits successfully using the same image digest as every long-running role.
- `web` readiness returns HTTP 200 at `/api/method/university_erp.api.health.ready`.
- `websocket` logs the assigned Railway port and remains private until same-origin routing exists.
- `scheduler` has exactly one replica.
- `worker-short` consumes `short,default`; `worker-long` consumes only `long`.
- A redeploy preserves database records and private files because neither depends on the service filesystem.
