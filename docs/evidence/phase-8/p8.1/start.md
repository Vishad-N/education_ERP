# P8.1 Multi-Provider Staging Start

Date: 2026-08-15

## Decision

Railway is the first staging target under ADR-0015. Hostinger VPS remains the current production baseline and AWS ECS/Fargate remains a portable alternative. No paid resource, DNS record, credential or external environment was created.

## Initial implementation

- Added one role-based container entrypoint for web, WebSocket, scheduler, short worker, long worker and migration jobs.
- Added runtime-generated Frappe site/common configuration sourced from managed environment variables.
- Added database/cache readiness and liveness API probes.
- Added Railway config-as-code files for each process role.
- Added immutable-image Compose for Hostinger or other Docker hosts.
- Added an AWS ECS/Fargate task-definition baseline with explicit health checks and Secrets Manager references.
- Added staging environment variable template and deployment policy validation.

## Verification

- Railway TOML parsed successfully.
- AWS ECS task-definition JSON parsed successfully.
- Portable staging Compose rendered successfully using only placeholder values.
- Service entrypoint passed `bash -n` syntax validation.
- `p21.localhost` migration passed and all 10 custom-app tests passed, including database/cache readiness.
- An initial `docker compose --progress plain build backend` reached the pinned CRM Vite production build before Docker Desktop terminated the BuildKit connection with `rpc error: code = Unavailable ... EOF`. The engine exposes about 3.5 GB RAM, making local engine memory pressure the likely cause; no application compile error was reported before the disconnect.
- The Dockerfile now caches upstream dependency installation, each upstream asset build and the custom app in separate layers. The CRM Node heap is capped at 1.5 GB so a constrained builder fails locally without exhausting the BuildKit daemon.
- The follow-up build completed successfully, including pinned upstream assets and the `university_erp` portal build. The runtime entrypoint syntax, executable bit and `sites/apps.txt` registration passed in a disposable container that was automatically removed.
- A cached follow-up build previously generated native BuildKit SBOM and provenance attestations. Its image digest was `sha256:0a4f01de1dcdaab2b746e25d901d2ae5b608ad28e7ecd19bce27528a6296fb76`, but it is superseded by the Railway snapshot fix below and must not be published or deployed.
- Docker Desktop settings, existing containers, volumes and networks were not changed. The only persistent Docker outputs are normal build cache, the BuildKit SBOM scanner cache and the newly built local image.

## Manual Railway readiness corrections

- Added a one-shot `bootstrap` role that initializes an empty managed MariaDB database through Frappe's `--no-setup-db` path and installs the pinned applications.
- Added explicit `DB_USER` support and ensured bootstrap adopts the shared managed `SITE_ENCRYPTION_KEY`.
- Corrected the WebSocket role so Railway's assigned `PORT` is written to Frappe configuration before Node starts.
- Isolated `worker-long` to the `long` queue while `worker-short` handles `short,default`.
- Updated the runbook to require one published digest across every service and to distinguish digest deployment from independent Git builds.
- Verified the rebuilt Linux image with `bash -n`, standard runtime config generation, managed database-user config and WebSocket port propagation. All disposable verification containers used `--rm`.

## Railway Git snapshot correction

- Railway build logs showed that the Git snapshot does not contain local `apps/erpnext`, `apps/education` or `apps/crm` directories, and Payments is only a submodule pointer. The Dockerfile now fetches ERPNext, Education, CRM and Payments directly from their upstream repositories at the exact SHAs in `apps.json`.
- The mutable `frappe/bench:v5.31.0` tag is now pinned to the tested base-image digest.
- Bench requires each upstream app's `.git` metadata while running `bench setup requirements`; cleanup now occurs only after the upstream builds complete.
- No build was run after this correction at the user's request. A fresh image build, SBOM/provenance generation, digest recording and Railway redeploy remain required before accepting the current source as deployable.

## Open P8.1 work

- Publish the attested immutable image to the approved registry and verify the SBOM from the registry reference.
- Deploy the Railway staging services using approved project access and managed variables.
- Add Cloudflare edge/R2 configuration templates.
- Add database backup/PITR and restore automation.
- Add Prometheus/Grafana/Loki/Uptime Kuma or provider-equivalent monitoring.
- Execute and record a staging restore test.

## Current external gates

- Railway CLI is not installed and no authenticated Railway project context or managed staging variables are available in this workspace.
- Local `imagetools` SBOM extraction is unavailable because it resolves registry references; registry verification follows image publication.

## External platform references

- [Railway config as code](https://docs.railway.com/config-as-code)
- [Railway Docker Compose service mapping](https://docs.railway.com/guides/docker-compose)
- [Railway health checks](https://docs.railway.com/deployments/healthchecks)
- [Amazon ECS container health checks](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/healthcheck.html)
