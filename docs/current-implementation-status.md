# Current Implementation Status

## Purpose

This document distinguishes files that currently exist from capabilities that are actually implemented and verified. Agents must not treat scaffolding, empty directories, configuration examples, or installed JavaScript dependencies as completed product functionality.

## Current milestone

| Field | Current value |
|---|---|
| Product state | Phase 1 repository structure baseline complete; functional implementation remains unstarted |
| Roadmap state | `P1.2` is the next governing execution step in `PROJECT_IMPLEMENTATION_PLAN.md` |
| Production readiness | Not production ready |
| Upstream source repositories | Pulled into `apps/` at pinned commits for local reference and later Bench setup |
| Custom Frappe app | Directory skeleton exists; Bench-generated app is not complete |
| Business modules | Not implemented |
| Production infrastructure | Not provisioned |
| Real integrations | Not implemented or approved |
| Automated product tests | Not implemented |

## Existing repository assets

- Product, architecture, security, development, testing and operations documentation.
- Phase 0 source baseline manifest at `docs/releases/p0-source-baseline.md`.
- Phase 0 provider ownership ADR at `docs/adr/0012-institution-owned-provider-accounts.md`.
- Pilot scope baseline at `docs/requirements/pilot-scope.md`.
- Phase 1 repository-structure evidence at `docs/evidence/phase-1/p1.1/repository-structure-baseline.md`.
- Root tooling configuration and documentation formatting scripts.
- `apps.json` containing intended Frappe, ERPNext, Education, CRM, Payments and custom-app sources.
- Local upstream source checkouts under `apps/`:
  - `apps/frappe` at `ba18090b141740e75d52aa97bfc525ff2f831f6c`
  - `apps/erpnext` at `054b20a2ae1bdea44694cca72d17412945171cab`
  - `apps/education` at `1c29e646bf943c2a5f696cb81cb48c8a072cbebc`
  - `apps/crm` at `bf1b7f07ac01b6ac435f25db7ccef6b52807720e`
  - `apps/payments` at `cca07d9f9392e2ea0e521c5975151db9e4b6c321`
  - `apps/frappe_docker` at `616ffd417797031f760e7a6c9669923a5febed66`
- Local-development `compose.yaml` with MariaDB, three Redis services, backend, WebSocket, scheduler and workers.
- Development Dockerfile and common Frappe site configuration.
- Bootstrap prerequisite, site initialization and repository verification scripts.
- `university_erp` folder structure, Python package metadata and Vue/Vite package metadata.
- Placeholder infrastructure, migration, operations, contract, E2E, performance and security folders.
- Previous local Docker Compose containers and network were removed on 2026-08-09; named project volumes were intentionally retained.

## Known gaps before local platform bootstrap completion

- Dockerfile uses a concrete `frappe/bench:v5.31.0` bootstrap tag, but the final production image digest/SBOM is not recorded yet.
- Docker build still depends on network fetches, although it now checks out/verifies exact app SHAs.
- The custom app has not been generated and installed through Bench; expected Frappe files such as `hooks.py` are absent.
- Local Compose is a development topology, not Hostinger production topology.
- Redis persistence, production secrets, TLS, proxy, health/readiness and backup behavior are not production configured.
- No Git-hosted CI workflow, SBOM, image signature, vulnerability policy or release manifest exists.
- No domain DocTypes, APIs, workflows, provider adapters, translations or business logic exist.
- No automated unit, integration, permission, migration, browser, performance or security tests exist.
- No infrastructure-as-code or production monitoring implementation exists.
- No production Razorpay, MSG91/DLT, Hostinger SMTP or Cloudflare R2 configuration is approved.

## Interpretation rules for agents

- Empty folders represent intended ownership, not completed modules.
- A dependency in `package.json` represents an intended tool, not a verified integration.
- A Compose service represents local orchestration, not production availability.
- Example/default passwords are local-development values only.
- A roadmap step becomes `DONE` only when its artifacts and verification gate pass.
- Do not advance the execution roadmap merely because a file or folder already has the expected name.

## Immediate next action

Follow `PROJECT_IMPLEMENTATION_PLAN.md` starting at `P1.2`. The next work is to generate the real Bench-created `university_erp` app files, including `hooks.py`, `modules.txt`, and `patches.txt`.
