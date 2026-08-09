# Local Development

The repository's current Compose and bootstrap assets are development scaffolding only. They must not be used as production deployment artifacts; review the [current implementation status](../current-implementation-status.md) before running them.

## Supported model

Use Linux or WSL2 on Windows. Prefer the project container/Compose workflow based on the pinned `frappe_docker` commit so local services match CI and production. A native Bench is allowed only when its versions match the release manifest.

## Prerequisites

- Git and Docker with Compose support.
- WSL2/Ubuntu for Windows development.
- Sufficient resources for MariaDB, Redis/Valkey, Frappe services, and frontend builds; start with 4 CPU and 8 GB RAM available to containers.
- Access to the pinned application repositories/releases.
- No production credentials or production student data.

Frappe v16 currently requires the runtime family documented in `AGENTS.md`; use image-provided versions instead of installing moving local versions.

## Repository bootstrap sequence

1. Clone the product repository.
2. Copy `.env.example` to the developer-local environment file and set only non-secret development values.
3. Build the pinned custom image from `docker/Dockerfile` and the release application manifest.
4. Start MariaDB, Redis/Valkey, backend, frontend, realtime, scheduler, and worker services.
5. Create a development site such as `erp.localhost`.
6. Install ERPNext, Education, CRM, then `university_erp` in the tested order.
7. Run migrations and load approved fixtures/seed data.
8. Build assets and execute smoke tests.
9. Create a non-Administrator test user for daily workflow verification.

Exact commands belong in version-controlled scripts under `scripts/bootstrap/` once the repository bootstrap is implemented. Avoid undocumented manual setup steps.

## Required development configuration

- `developer_mode` enabled only on local development sites.
- Tests enabled only outside production.
- Email and SMS routed to local capture/fake providers.
- Payments use provider sandbox or a deterministic fake adapter.
- Object storage uses an isolated development bucket/emulator.
- Malware scanning uses a local scanner or deterministic fake with explicit test modes.
- Scheduler and all queue types run so asynchronous behavior is tested.
- Timezone, currency, academic session, and locale mirror a representative pilot institution.

## Seed data

Provide repeatable factories or fixtures for:

- one university, two campuses, colleges and departments;
- one academic session with UG/PG programs, curriculum, classes and sections;
- categories, reservation rules, intake and seat matrix;
- applicants across eligible/ineligible/waitlisted paths;
- students with guardian, consent and document states;
- fee policies, installments, concessions and accounting dimensions;
- users for every role and campus scope;
- provider responses for success, duplicate, timeout, failure and reversal.

Synthetic data must be obviously fake and safe to export or screenshot.

## Daily checks

Before opening a pull request:

- migrations apply to a fresh site and an upgraded site;
- domain unit/integration tests pass;
- generated DocType metadata and fixtures are committed;
- formatting, lint, type/static checks and secret scanning pass;
- changed UI paths are exercised at desktop and mobile widths;
- no upstream app source or developer-local configuration is included.

## Reset and recovery

Development reset scripts must name the exact local site and require explicit confirmation. Never use broad deletion targets. Prefer recreating a disposable local site over manually deleting individual framework tables.

## Troubleshooting evidence

When reporting setup failures, include image digest/app SHAs, operating environment, failing service, sanitized command, exit code, relevant sanitized log lines, and whether a fresh-site bootstrap reproduces it.
