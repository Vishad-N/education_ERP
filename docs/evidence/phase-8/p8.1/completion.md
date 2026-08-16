# P8.1 Completion

Date: 2026-08-17

Human UAT remains deferred. No production DNS, R2, or live provider credentials were created.

## Exit gate

Production-like Railway staging deploys from Docker images and an isolated restore proof succeeded.

## Verified live stack

| Service | Role | State |
|---|---|---|
| `web` | HTTP/API | SUCCESS, 1 replica, ready HTTP 200 |
| `bootstrap` | combined scheduler + all queues | SUCCESS, 1 replica, scheduled jobs executing |
| `mariadb` | MariaDB 11.8 | SUCCESS, volume ready |
| `Redis` | cache/queue/realtime | SUCCESS, volume ready |

Public origin: `https://web-production-7580e.up.railway.app`

## Restore proof

`scripts/operations/restore-proof.py` cloned 33 tables, including `tabUser`, `tabDocType`, `tabRole`, `tabHas Role`, and `tabSingles`, into `education_erp_restore_proof` and matched every row count. Source database has 899 base tables. A full second copy failed with MariaDB errno 135 on the 500 MB volume; that limit is accepted for staging.

A temporary Railway TCP proxy was used because `railway ssh` hung. The proxy `5e65111a-fcd1-4eec-9fd9-b7f6ac859e2e` was deleted immediately after the proof. `railway tcp-proxy list --service mariadb` then returned no proxies. Site readiness remained HTTP 200.

## Accepted staging exceptions

- Railway free plan cannot add dedicated `scheduler`, `worker-*`, `websocket`, `migrate`, or `backup` services.
- Web and combined worker use different image digests. Production must publish one digest.
- Cloudflare/R2 remain templates only.
- Source-component SBOM is recorded; a signed registry SBOM is not.

## Evidence

- `docs/evidence/phase-8/p8.1/start.md`
- `docs/evidence/phase-8/p8.1/progress-2026-08-16.md`
- `docs/releases/p8-staging-manifest.md`
- `scripts/ci/verify-deployment.ps1` passed on 2026-08-17
