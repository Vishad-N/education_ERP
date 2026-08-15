# Hostinger VPS Baseline

Use `deploy/compose/staging.compose.yaml` with the approved immutable image digest and a protected environment file derived from `deploy/env/staging.env.example`.

For the production pilot, place web/WebSocket/workers/scheduler on the application VPS and MariaDB/Redis on the private database VPS described in `docs/operations/hostinger-production-platform.md`. Put Cloudflare in front of the web/WebSocket origin and keep database/cache ports private.

The Compose file deliberately contains no database or Redis containers, bind-mounted source, default passwords or production secrets. Database/PITR, R2, monitoring and restore automation remain P8.1 work.
